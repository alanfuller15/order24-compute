#!/usr/bin/env python3
"""lratcatch_cnf.py (research only; not part of any check that counts): rebuild one record's CNF exactly as the pinned
audit checker does, and write it to a file for lrat-catcher.

It loads audit_kit/l<M>/code/gcert<M>.py itself as a module (not as __main__, so its main() does not run). That module's
top level reads its own source and the encoder sources, refuses any encoder that is not pinned (ENCODER_PINS) and
compiles them from the hashed bytes (from_source). The CNF bytes are then made by the checker's own line
    ENC[enc].rebuild(F[tag], rec['lazy']).to_fp(buf); data = buf.getvalue().encode('ascii')
and must hash to the record's cnf_sha256. The formulas file must hash to the checker's FORMULAS_PIN.

It also reports what lrat-catcher needs from a base CNF: no duplicate-literal and no tautological clause (the core
converter would drop such a clause and shift every clause position; lratcatch-compact-renumber refuses them), no
empty clause, and the largest variable.

Usage: python3 -I -B lratcatch_cnf.py M RESULTS.jsonl TAG OUT.cnf OUT_info.json
Exit 0: written and the hash matches; 1: anything else (nothing is written on a mismatch)."""
import sys, os, io, json, hashlib, importlib.util

def main():
    M, rpath, tag, outp, infop = sys.argv[1:6]
    root = os.getcwd(); kit = os.path.join(root, 'audit_kit', f'l{M}')
    gpath = os.path.join(kit, 'code', f'gcert{M}.py'); fpath = os.path.join(kit, f'formulas{M}_c{int(M) - 23}.json')
    spec = importlib.util.spec_from_file_location(f'gcert{M}', gpath)
    G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)   # pins checked at its top level
    rawF = open(fpath, 'rb').read()
    if hashlib.sha256(rawF).hexdigest() != G.FORMULAS_PIN: sys.exit('formulas file is not the pinned one')
    F = json.loads(rawF)
    recs = [json.loads(l) for l in open(rpath) if l.strip()]
    recs = [r for r in recs if r.get('tag') == tag]
    if len(recs) != 1: sys.exit(f'{len(recs)} records with tag {tag} in {rpath} (need exactly 1)')
    rec = recs[0]; enc = rec.get('encoder', 'v4')
    if enc not in G.ENC: sys.exit(f'unknown encoder {enc}')
    f = F[tag]
    if any(rec.get(k) != f[k] for k in ('s', 'a', 'b', 'c', 'h_index')): sys.exit('record does not match its formula')
    buf = io.StringIO(); G.ENC[enc].rebuild(f, rec['lazy']).to_fp(buf)
    data = buf.getvalue().encode('ascii'); del buf
    sha = hashlib.sha256(data).hexdigest()
    info = {'tag': tag, 'layer': int(M), 'encoder': enc, 'cnf_sha256': sha, 'record_cnf_sha256': rec['cnf_sha256'],
            'cnf_match': sha == rec['cnf_sha256'], 'cnf_bytes': len(data), 'gcert_sha256': hashlib.sha256(open(gpath, 'rb').read()).hexdigest(),
            'proof_sha256': rec.get('proof_sha256'), 'proof_xz_bytes': rec.get('proof_xz_bytes'),
            'proof_raw_bytes': rec.get('proof_raw_bytes'), 'proof_trimmed': rec.get('proof_trimmed'),
            'cubes': rec.get('cubes'), 'cake_seconds': rec.get('cake_seconds'), 'cake_heap_mb': rec.get('cake_heap_mb')}
    nclauses = 0; maxvar = 0; dup = taut = empty = 0; header = None
    for line in data.decode('ascii').split('\n'):
        t = line.strip()
        if not t: continue
        if t.startswith('p '): header = t; continue
        if not (t[0].isdigit() or t[0] == '-'): continue
        lits = [int(x) for x in t.split()]
        if lits[-1] != 0 or 0 in lits[:-1]: sys.exit('a clause line that is not one clause ending in 0')
        c = lits[:-1]; nclauses += 1
        if not c: empty += 1
        s = set(c)
        if len(s) != len(c): dup += 1
        if any(-l in s for l in s): taut += 1
        if c: maxvar = max(maxvar, max(abs(l) for l in c))
    info.update({'header': header, 'clauses': nclauses, 'max_var': maxvar, 'dup_literal_clauses': dup,
                 'tautologies': taut, 'empty_clauses': empty})
    json.dump(info, open(infop, 'w'), indent=1)
    print(json.dumps(info))
    if not info['cnf_match']: sys.exit('CNF SHA-256 differs from the record: stop')
    if dup or taut or empty: sys.exit('the CNF has duplicate-literal, tautological or empty clauses: lrat-catcher positions would shift')
    with open(outp, 'wb') as fo: fo.write(data)

if __name__ == '__main__':
    main()
