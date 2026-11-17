#!/usr/bin/env python3
"""exp/fast_cegar.py (EXPERIMENT; research only, nothing is recorded or proved): the CEGAR loop of the pipeline on
variant B = pinned base formula + seeded lazy items + explicit implied clauses d_S(v) >= 4 and d_S(v) <= 4 + (c - 56)
for every T-vertex v (soundness sketch in exp/fast_ab.py). Each model adds the lazy items it violates (ccc90.violated,
the pipeline's rule); the loop ends with UNSAT (the strengthened formula has no model), ORIGINAL_MODEL (a model with no
violated item: STOP and report), or the time limit. With EXTRA=0 the same loop runs on the unmodified formula (variant A).
Usage: python3 -I -B exp/fast_cegar.py FORMULAS.json TAG SEEDS.jsonl.xz OUT.json [LIMIT_S=3600]   (env EXTRA=1|0)"""
import sys, os, json, lzma, time
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(HERE); sys.path.insert(0, os.path.join(R, 'code'))
os.environ.setdefault('ENCODER', 'cegar90c'); os.environ.setdefault('MASKS12', os.path.join(R, 'data', 'masks12.npy'))
import cegar90c as C, ccc90 as K
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
fpath, tag, seedp, outp = sys.argv[1:5]; LIMIT = float(sys.argv[5]) if len(sys.argv) > 5 else 3600
EXTRA = os.environ.get('EXTRA', '1') == '1'
f = json.load(open(fpath))[tag]; s, c = f['s'], f['c']; assert (s, f['a'], f['b']) == (10, 4, 18) and c <= 65, 'profile'
items = []; got = set()
for l in lzma.open(seedp, 'rt'):
    try: o = json.loads(l)
    except ValueError: continue
    its = o.get('items', o.get('lazy')) if isinstance(o, dict) else None
    if isinstance(its, list) and o.get('tag') == tag:
        for x in its:
            kk = (x['kind'], tuple(x['W']))
            if kk not in got: got.add(kk); items.append(x)
pool, cnf, E = C.build(f)
for x in items: cnf.extend(C.lazy_clauses(x, E, pool))
if EXTRA:
    for v in range(s, 24):
        xs = [E[k, v] for k in range(s)]
        cnf.extend(CardEnc.atleast(xs, bound=4, vpool=pool, encoding=EncType.seqcounter).clauses)
        if 4 + c - 56 < s: cnf.extend(CardEnc.atmost(xs, bound=4 + c - 56, vpool=pool, encoding=EncType.seqcounter).clauses)
M = C.masks12(); sol = Solver(name='cadical195', bootstrap_with=cnf.clauses); t0 = time.time(); it_n = 0; status = 'LIMIT'; seed_n = len(items)
print(f'{tag} c={c} EXTRA={int(EXTRA)}: {seed_n} seed items, {len(cnf.clauses)} clauses', flush=True)
while time.time() - t0 < LIMIT:
    sol.conf_budget(2000000); ans = sol.solve_limited()
    if ans is False: status = 'UNSAT'; break
    if ans is None: continue
    new, edges = K.violated(E, M, set(l for l in sol.get_model() if l > 0))
    if not new: status = 'ORIGINAL_MODEL'; json.dump({'tag': tag, 'edges': edges}, open(outp + '.model.json', 'w')); break
    for x in new:
        kk = (x['kind'], tuple(x['W'])); assert kk not in got, 'repeat'; got.add(kk); items.append(x)
        for cl in C.lazy_clauses(x, E, pool): sol.add_clause(cl)
    it_n += 1
    if it_n % 10 == 0: print(f'  iter {it_n}: {len(items)} items, {time.time() - t0:.0f} s, conflicts {sol.accum_stats().get("conflicts")}', flush=True)
res = {'tag': tag, 'c': c, 'extra': EXTRA, 'status': status, 'seconds': round(time.time() - t0, 1), 'iterations': it_n, 'seed_items': seed_n,
       'items': len(items), 'conflicts': sol.accum_stats().get('conflicts')}
json.dump(res, open(outp, 'w')); print('RESULT', json.dumps(res), flush=True)
