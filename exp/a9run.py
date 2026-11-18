#!/usr/bin/env python3
"""a9run.py K N OUTDIR [budget_s] [workers] [units] -- certified run of shard K of N of the alpha = 9 cubes.
Units: for every (case, profile index) of the version-2 list, Case B first (131), then Case A (299): the root cube []
unless the profile is one of the 33 strong profiles with all entries >= 4 (the hard ones); for those every leaf of the static split on the incidence columns
1 and 2 (a9cubes.gen).  Unit number u belongs to shard u mod N.  A cube whose CEGAR exceeds the budget is split
further (a9cubes.next_split) and its children are solved in the same unit.  All leaves are leaves of one binary tree
per profile (a9check.py re-checks completeness from the records alone).
Every UNSAT leaf: final CNF written, CaDiCaL LRAT proof, cake_lpr; only the exact line "s VERIFIED UNSAT" counts.
Records: OUTDIR/results.jsonl (one line per solved cube; TIMEOUT lines are inner nodes) + OUTDIR/lazy/<tag>.json.gz.
A model satisfying every floor stops everything: OUTDIR/MODEL_FOUND.json."""
import sys, os, json, gzip, time, subprocess, fcntl, hashlib, itertools as it, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import a9core as C, a9solve as S, a9cubes as Q

def tool(name, env, home):
    for p in (os.environ.get(env), os.path.expanduser(home), os.path.join(HERE, '..', 'bin', name)):
        if p and os.path.exists(p): return p
    raise SystemExit('missing tool ' + name)

def hard(case, idx):   # strong profiles without an entry <= 3 are pre-split; all others start from the root cube
    return idx < C.nstrong(case) and C.profiles(case)[idx][0] >= 4

def units():
    U = []
    for c in 'BA':
        for k, p in enumerate(C.profiles(c)):
            if hard(c, k): U += [(c, k, cube) for cube, _ in Q.gen(c, p, [1, 2])]
            else: U.append((c, k, []))
    return U

def tag_of(case, idx, cube):
    s = ''.join('%s%d' % ('p' if l > 0 else 'n', abs(l)) for l in cube)
    if len(s) > 40: s = 'h' + hashlib.sha256(s.encode()).hexdigest()[:24]
    return '%s%03d_%s' % (case, idx, s or 'root')

def verify_model(E):
    """independent check of a claimed counterexample (plain Python, no masks): triangle-free, floors, alpha."""
    Es = {tuple(sorted(e)) for e in E}; adj = [set() for _ in range(24)]
    for u, v in Es: adj[u].add(v); adj[v].add(u)
    tri = any(adj[u] & adj[v] for u, v in Es)
    mn = min(sum(1 for p in it.combinations(c, 2) if p in Es) for c in it.combinations(range(24), 12))
    return {'triangle_free': not tri, 'min_12set_edges': mn, 'edges': len(Es), 'has_independent_10set': bool(S.ind10(sorted(Es)))}

def work(a):
    case, idx, cube0, out, budget = a
    CAD = tool('cadical', 'CAD', '~/tools/cadical/build/cadical'); CAKE = tool('cake_lpr', 'CAKE', '~/tools/cake_lpr/cake_lpr')
    prof = C.profiles(case)[idx]; stack = [list(cube0)]; recs = []
    while stack:
        cube = stack.pop(); tag = tag_of(case, idx, cube)
        r, f = S.run(case, prof, cube, budget)
        rec = {'list_version': 2, 'tag': tag, 'case': case, 'idx': idx, 'prof': list(prof), 'unit': list(cube0), 'cube': cube, 'status': r['status'],
               'iters': r['iters'], 'cegar_seconds': r['seconds'], 'lazy_items': len(r['lazy']), 'nv': f.nv, 'ncl': len(f.cl)}
        if r['status'] == 'MODEL':
            rec['edges'] = r['edges']; rec['verify'] = verify_model(r['edges'])
            json.dump(rec, open(os.path.join(out, 'MODEL_FOUND.json'), 'w')); recs.append(rec); return recs
        if r['status'] == 'TIMEOUT':
            ch = Q.next_split(case, prof, cube); stack.extend(reversed(ch)); rec['children'] = len(ch); recs.append(rec); continue
        cnf = os.path.join(out, tag + '.cnf'); prf = os.path.join(out, tag + '.lrat')
        b = C.dimacs(f); open(cnf, 'wb').write(b); rec['cnf_sha256'] = C.sha(b); rec['cnf_bytes'] = len(b); del b, f
        t1 = time.time()
        cp = subprocess.run([CAD, '-q', '--lrat=true', '--binary=false', cnf, prf], capture_output=True)
        rec['cadical_exit'] = cp.returncode; rec['cadical_seconds'] = round(time.time() - t1, 1)
        rec['proof_bytes'] = os.path.getsize(prf) if os.path.exists(prf) else 0
        if cp.returncode == 20:
            h = hashlib.sha256()
            with open(prf, 'rb') as fh:
                for blk in iter(lambda: fh.read(1 << 20), b''): h.update(blk)
            rec['proof_sha256'] = h.hexdigest(); t2 = time.time()
            with open(os.environ.get('A9_LOCK', os.path.join(out, '.cake.lock')), 'w') as lk:   # one cake_lpr at a time (memory; A9_LOCK shares it between runs)
                fcntl.flock(lk, fcntl.LOCK_EX)
                ck = subprocess.run([CAKE, '--CML_HEAP_SIZE=' + os.environ.get('A9_CAKE_HEAP', '3000'), '--CML_STACK_SIZE=256', cnf, prf], capture_output=True, text=True)
            rec['cake_lpr'] = 's VERIFIED UNSAT' if 's VERIFIED UNSAT' in ck.stdout.splitlines() else 'NOT VERIFIED: ' + (ck.stdout + ck.stderr)[-200:]
            rec['cake_seconds'] = round(time.time() - t2, 1)
        else:
            rec['cake_lpr'] = 'NOT RUN (cadical exit %d)' % cp.returncode
        with gzip.open(os.path.join(out, 'lazy', tag + '.json.gz'), 'wt', compresslevel=9) as g: json.dump(r['lazy'], g, separators=(',', ':'))
        if rec['cake_lpr'] == 's VERIFIED UNSAT':
            for p in (cnf, prf): os.remove(p)
        recs.append(rec)
    return recs

if __name__ == '__main__':
    K, N, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    budget = float(sys.argv[4]) if len(sys.argv) > 4 else 300; nw = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    only = sys.argv[6] if len(sys.argv) > 6 else None     # optional filter (tests): tag prefix, e.g. B017 ; or "limit=20", or "easy" (the root units of the strong profiles), or "extra" (the weak-extra profiles)
    os.makedirs(os.path.join(out, 'lazy'), exist_ok=True); res = os.path.join(out, 'results.jsonl')
    U = units(); done = set()
    if os.path.exists(res):
        for l in open(res):
            d = json.loads(l); k2 = C.index_of(d['case'], tuple(d['prof']))      # records are matched by profile tuple
            if k2 is not None: done.add(tag_of(d['case'], k2, d['unit']))
    dl = os.environ.get('A9_DONE')                       # optional file of unit tags already finished elsewhere (round 2+)
    if dl and os.path.exists(dl): done |= {l.strip() for l in open(dl) if l.strip()}
    todo = [(c, k, cube, out, budget) for u, (c, k, cube) in enumerate(U) if u % N == K and tag_of(c, k, cube) not in done]
    if only and only.startswith('limit='): todo = todo[:int(only[6:])]
    elif only == 'easy': todo = [t for t in todo if not hard(t[0], t[1]) and t[1] < C.nstrong(t[0])]
    elif only == 'extra': todo = [t for t in todo if t[1] >= C.nstrong(t[0])]
    elif only: todo = [t for t in todo if tag_of(t[0], t[1], t[2]).startswith(only)]
    print(f'shard {K}/{N}: {len(todo)} units to do, of {len(U)} units in all', flush=True); t0 = time.time(); bad = n = 0
    with mp.Pool(nw, maxtasksperchild=1) as pool, open(res, 'a') as fo:
        stop = float(os.environ.get('A9_STOP', '0'))     # optional wall-clock limit (s): stop cleanly, unfinished units are simply not recorded
        itr = pool.imap_unordered(work, todo); stopped = False
        while True:
            try:
                recs = itr.next(timeout=20)
            except StopIteration:
                break
            except mp.TimeoutError:
                if stop and time.time() - t0 > stop: stopped = True; break
                continue
            n += 1
            for r in recs:                    # a unit's records are written together, when the whole unit is finished
                fo.write(json.dumps(r) + '\n')
                if r['status'] == 'MODEL': fo.flush(); print('MODEL FOUND -- EXAMINE:', json.dumps(r), flush=True); pool.terminate(); sys.exit(3)
                if r['status'] == 'UNSAT' and r['cake_lpr'] != 's VERIFIED UNSAT': bad += 1; print('ATTENTION', json.dumps(r)[:300], flush=True)
            fo.flush(); r = recs[0]
            print(f"{n}/{len(todo)} {r['tag']} {len(recs)} cube(s), cegar {sum(x['cegar_seconds'] for x in recs):.0f}s, "
                  f"cadical {sum(x.get('cadical_seconds', 0) for x in recs):.0f}s, cake {sum(x.get('cake_seconds', 0) for x in recs):.0f}s, t={time.time()-t0:.0f}", flush=True)
            if stop and time.time() - t0 > stop: stopped = True; break
        if stopped:
            pool.terminate()
            print(f'A9_STOP reached after {time.time()-t0:.0f}s: finished units are recorded, the other units of this shard are left for a re-run', flush=True)
    print(f'shard {K}/{N} {"STOPPED" if stopped else "finished"}: {n} units, not verified {bad}', flush=True)
