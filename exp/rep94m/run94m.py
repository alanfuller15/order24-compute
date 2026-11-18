#!/usr/bin/env python3
"""Driver: for every class of classes94m.json, run cegar95 (CEGAR to UNSAT), then certify the final CNF:
CaDiCaL 3.0.1 LRAT proof + cake_lpr (accept only the exact line "s VERIFIED UNSAT"). Records hashes and the verdict in
results94m.jsonl; keeps the lazy list (regenerates the CNF byte for byte with rebuild95.py) and deletes the CNF and the
proof afterwards (disk). Resumable: tags already in results94m.jsonl are skipped.
Usage: python3 -I run94m.py classes94m.json OUTDIR [workers] [budget_s] [shape_prefix]"""
import sys, os, json, subprocess, hashlib, time, gzip, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cegar_shape as C   # the audited mixed-pattern encoder, unchanged
CAD = os.environ.get('CAD') or os.path.expanduser('~/tools/cadical/build/cadical'); CAKE = os.environ.get('CAKE') or os.path.expanduser('~/tools/cake_lpr/cake_lpr')
# GitHub port (2026-11-18): CAD/CAKE from the environment; SHARD=k/N keeps every N-th task; DONE=file of tags to skip;
# CAKE_FAST=1: cake_lpr at the 2000 MB heap without the lock, retried at 4000 MB under the lock if it gives no verdict.

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

def work(a):
    data_path, name, i, out, budget = a
    sh = json.load(open(data_path))[name]; tag = f'{name}_{i:04d}'
    r = C.run(sh, sh['classes'][i], out, tag=tag, budget_s=budget)
    r.pop('edges', None) if r['status'] != 'ORIGINAL_MODEL_FOUND' else None
    r.update({'shape': name, 'class_index': i})
    if r['status'] == 'UNSAT':
        f = os.path.join(out, tag + '.cnf'); p = os.path.join(out, tag + '.lrat')
        r['cnf_sha256'] = sha(f); t1 = time.time()
        cp = subprocess.run([CAD, '-q', '--lrat=true', '--binary=false', f, p], capture_output=True)
        r['cadical_exit'] = cp.returncode; r['proof_sha256'] = sha(p); r['proof_bytes'] = os.path.getsize(p)
        # one cake_lpr at a time (file lock): two 4 GB CakeML heaps alongside CaDiCaL can exhaust the 8 GB machine,
        # and a killed cake_lpr prints no verdict (this happened once, to M10_a_e3_0004, before the lock was added)
        import fcntl
        ck = None
        if os.environ.get('CAKE_FAST') == '1':
            ck = subprocess.run([CAKE, '--CML_HEAP_SIZE=2000', '--CML_STACK_SIZE=256', f, p], capture_output=True, text=True); r['cake_heap_mb'] = 2000
        if ck is None or 's VERIFIED UNSAT' not in ck.stdout.splitlines():
            with open(os.path.join(out, '.cake.lock'), 'w') as lk:
                fcntl.flock(lk, fcntl.LOCK_EX)
                ck = subprocess.run([CAKE, '--CML_HEAP_SIZE=4000', '--CML_STACK_SIZE=256', f, p], capture_output=True, text=True); r['cake_heap_mb'] = 4000
        r['cake_exit'] = ck.returncode
        lines = ck.stdout.splitlines()
        r['cake_lpr'] = 's VERIFIED UNSAT' if 's VERIFIED UNSAT' in lines else 'NOT VERIFIED: ' + (ck.stdout + ck.stderr)[-160:]
        if r['cake_lpr'] != 's VERIFIED UNSAT':   # keep the files of a failed check for inspection
            return r
        r['cert_seconds'] = round(time.time() - t1, 1)
        lz = os.path.join(out, tag + '.lazy.json')
        with open(lz, 'rb') as src, gzip.open(lz + '.gz', 'wb', compresslevel=9) as dst: dst.write(src.read())
        os.remove(lz); os.remove(f); os.remove(p)
    return r

if __name__ == '__main__':
    data_path, out = sys.argv[1], sys.argv[2]
    nw = int(sys.argv[3]) if len(sys.argv) > 3 else 2; budget = float(sys.argv[4]) if len(sys.argv) > 4 else 1800
    pref = sys.argv[5] if len(sys.argv) > 5 else ''
    os.makedirs(out, exist_ok=True); res_path = os.path.join(out, 'results94m.jsonl')
    done = set()
    if os.path.exists(res_path):
        for l in open(res_path): d = json.loads(l); done.add((d['shape'], d['class_index']))
    data = json.load(open(data_path))
    tasks = [(data_path, n, i, out, budget) for n in data if n.startswith(pref) for i in range(len(data[n]['classes']))
             if (n, i) not in done]
    if os.environ.get('DONE') and os.path.exists(os.environ['DONE']):
        dn = set(open(os.environ['DONE']).read().split()); tasks = [t for t in tasks if f'{t[1]}_{t[2]:04d}' not in dn]
    if os.environ.get('SHARD'):
        k, n = map(int, os.environ['SHARD'].split('/')); tasks = [t for j, t in enumerate(tasks) if j % n == k]
    print(f'{len(tasks)} tasks', flush=True)
    with mp.Pool(nw, maxtasksperchild=20) as pool, open(res_path, 'a') as fo:
        for r in pool.imap_unordered(work, tasks):
            fo.write(json.dumps(r) + '\n'); fo.flush()
            if r['status'] != 'UNSAT' or r.get('cake_lpr') != 's VERIFIED UNSAT':
                print('ATTENTION', json.dumps(r)[:400], flush=True)
