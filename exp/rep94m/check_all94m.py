#!/usr/bin/env python3
"""Independent replay of every class certificate from the shipped files alone.
For each record of results94m.jsonl: rebuild the CNF from classes94m.json + lazy/<tag>.lazy.json.gz (rebuild94m.py),
compare its SHA-256 with the record, generate an LRAT proof with CaDiCaL 3.0.1, compare the proof SHA-256 with the
record (informational: a differing proof is still checked), and run cake_lpr; accept only the exact line
"s VERIFIED UNSAT". Proof bytes are checked, not hashes: a class passes only on cake_lpr's verdict for the formula
whose hash equals the record. Writes CHECK_RESULTS.jsonl; exit 0 iff every class passes and all 1,848 are covered.
Usage: python3 -I check_all94m.py classes94m.json results94m.jsonl LAZYDIR WORKDIR [workers] [tag-regex]"""
import sys, os, re, json, gzip, hashlib, subprocess, fcntl, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import rebuild94m as RB
CAD = os.environ.get('CAD', os.path.expanduser('~/tools/cadical/build/cadical'))
CAKE = os.environ.get('CAKE', os.path.expanduser('~/tools/cake_lpr/cake_lpr'))
PIN = {'cadical': 'eae671d6fab57f7bf909e621adee2a2bd550a0ae0b561065c815f599c7696fe8',     # CaDiCaL 3.0.1 used here
       'cake_lpr': '29e02af756c1f0fc4ccac78e9a908e0d8ef01201786f257f1b27b26603390798'}    # cake_lpr used here

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

def one(a):
    cls_path, rec, lazydir, work = a
    sh = json.load(open(cls_path))[rec['shape']]; tag = rec['tag']
    lazy = json.load(gzip.open(os.path.join(lazydir, tag + '.lazy.json.gz')))
    f = os.path.join(work, tag + '.cnf'); p = os.path.join(work, tag + '.lrat')
    RB.rebuild(sh, sh['classes'][rec['class_index']], lazy).to_file(f)
    out = {'tag': tag, 'cnf_match': sha(f) == rec['cnf_sha256']}
    if out['cnf_match']:
        cp = subprocess.run([CAD, '-q', '--lrat=true', '--binary=false', f, p], capture_output=True)
        out['cadical_exit'] = cp.returncode
        out['proof_match'] = sha(p) == rec['proof_sha256']
        # one cake_lpr at a time (file lock): two 4 GB CakeML heaps at once can exhaust an 8 GB machine, and a
        # killed cake_lpr prints no verdict (seen once in the producer's re-run; the class verified when re-run alone)
        with open(os.path.join(work, '.cake.lock'), 'w') as lk:
            fcntl.flock(lk, fcntl.LOCK_EX)
            ck = subprocess.run([CAKE, '--CML_HEAP_SIZE=4000', '--CML_STACK_SIZE=256', f, p], capture_output=True, text=True)
        out['cake_exit'] = ck.returncode
        if 's VERIFIED UNSAT' not in ck.stdout.splitlines(): out['cake_tail'] = (ck.stdout + ck.stderr)[-300:]
        # cake_lpr exits 0 even when it rejects: only its exact stdout line counts
        out['cake_lpr'] = 's VERIFIED UNSAT' if 's VERIFIED UNSAT' in ck.stdout.splitlines() else 'NOT VERIFIED'
    for x in (f, p):
        if os.path.exists(x): os.remove(x)
    out['pass'] = out['cnf_match'] and out.get('cadical_exit') == 20 and out.get('cake_lpr') == 's VERIFIED UNSAT'
    return out

if __name__ == '__main__':
    cls_path, res_path, lazydir, work = sys.argv[1:5]
    nw = int(sys.argv[5]) if len(sys.argv) > 5 else 2; rx = re.compile(sys.argv[6]) if len(sys.argv) > 6 else None
    os.makedirs(work, exist_ok=True)
    recs = [json.loads(l) for l in open(res_path)]
    data = json.load(open(cls_path)); total = sum(len(v['classes']) for v in data.values())
    keys = {(r['shape'], r['class_index']) for r in recs}
    full = {(n, i) for n in data for i in range(len(data[n]['classes']))}
    if not (keys == full and len(recs) == total == len(keys)):
        sys.exit('results do not cover every class exactly once')
    if not all(r['status'] == 'UNSAT' for r in recs): sys.exit('a record is not UNSAT')
    for name, path in (('cadical', CAD), ('cake_lpr', CAKE)):
        h = sha(path); print(f'{name}: {path} sha256 {h}' + ('' if h == PIN[name] else '  (differs from the binary used here)'))
    todo = [r for r in recs if not rx or rx.search(r['tag'])]
    outp = os.path.join(work, 'CHECK_RESULTS.jsonl'); n = ok = 0
    with mp.Pool(nw) as pool, open(outp, 'w') as fo:
        for o in pool.imap_unordered(one, [(cls_path, r, lazydir, work) for r in todo]):
            n += 1; ok += o['pass']; fo.write(json.dumps(o) + '\n'); fo.flush()
            if not o['pass']: print('FAIL', o, flush=True)
    print(f'checked {n} classes (of {total} recorded): {ok} pass; proofs byte-identical to the record: '
          f'{sum(1 for l in open(outp) if json.loads(l).get("proof_match"))}')
    if rx: print(f'PARTIAL RUN: {n} of {total} classes selected by the tag filter; this is not a full check')
    sys.exit(0 if (ok == n and (rx or n == total)) else 1)
