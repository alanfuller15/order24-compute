#!/usr/bin/env python3
"""exp/fast_ab.py (EXPERIMENT; producer-side research, not part of any check, not used for records).
Question: do explicit IMPLIED clauses make the hard (10,4,18,c) formulas faster for CaDiCaL?
Variant A = the pinned base formula (cegar90c.build) + the tag's seeded lazy items (as ccc90.py starts).
Variant B = A + for every T-vertex v:  d_S(v) >= 4  and  d_S(v) <= 4 + (c - 56)   (sequential counters).
Soundness sketch (profile s=10, a=4, b=18, c<=65; to be reviewed before any production use): the base formula has the
12-set floor on S+{u,v} for all u,v in T: 4 + p(u) + p(v) + [uv] >= 12 (p = d_S). Summing over u != v for fixed v:
c >= 104 - 12 p(v) - q(v) (q = d_T); strict cut gives q(v) <= p(v) - 1; so p(v) <= 3 would force c >= 66. Hence p(v) >= 4
for all 14 T-vertices, and sum p = c gives p(v) <= 4 + (c - 56).
Method: the same cubes (ccc90.initial_tree at depth DEPTH, every STEP-th leaf, at most N) are solved under both variants
by bin/cadical with a time limit; times and outcomes are compared pairwise. Nothing is recorded or proved here.
Usage: MASKS12=data/masks12.npy python3 -I -B exp/fast_ab.py FORMULAS.json TAG SEEDS.jsonl.xz OUT.json [N=12] [TIMEOUT=600] [DEPTH=6] [JOBS=3]"""
import sys, os, json, lzma, time, subprocess, tempfile, itertools as it
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(HERE); sys.path.insert(0, os.path.join(R, 'code'))
os.environ.setdefault('ENCODER', 'cegar90c'); os.environ.setdefault('MASKS12', os.path.join(R, 'data', 'masks12.npy'))
import cegar90c as C, ccc90 as K
from pysat.card import CardEnc, EncType
fpath, tag, seedp, outp = sys.argv[1:5]
N = int(sys.argv[5]) if len(sys.argv) > 5 else 12; TO = int(sys.argv[6]) if len(sys.argv) > 6 else 600
DEPTH = int(sys.argv[7]) if len(sys.argv) > 7 else 6; JOBS = int(sys.argv[8]) if len(sys.argv) > 8 else 3
CAD = os.environ.get('CAD', os.path.join(R, 'bin', 'cadical'))
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
def formula(extra):
    pool, cnf, E = C.build(f)
    for x in items: cnf.extend(C.lazy_clauses(x, E, pool))
    nbase = len(cnf.clauses)
    if extra:
        for v in range(s, 24):
            xs = [E[k, v] for k in range(s)]
            cnf.extend(CardEnc.atleast(xs, bound=4, vpool=pool, encoding=EncType.seqcounter).clauses)
            if 4 + c - 56 < s: cnf.extend(CardEnc.atmost(xs, bound=4 + c - 56, vpool=pool, encoding=EncType.seqcounter).clauses)
    return pool, cnf, E, nbase
pA, cA, E, nA = formula(False); pB, cB, _, _ = formula(True)
assert cB.clauses[:nA] == cA.clauses, 'B must extend A'
cand, d8 = K.candidates(f, cA, E); t0 = time.time(); leaves, splits = K.initial_tree(cA.clauses, cand, DEPTH)
step = max(1, len(leaves) // N); cubes = leaves[::step][:N]
print(f'{tag}: {len(items)} seed items; A {len(cA.clauses)} clauses / {pA.top} vars; B +{len(cB.clauses) - nA} clauses / {pB.top} vars; '
      f'{len(leaves)} leaves at depth {DEPTH} ({time.time() - t0:.0f} s); testing {len(cubes)} cubes, timeout {TO} s', flush=True)
tmp = tempfile.mkdtemp(prefix='fastab_')
def run(job):
    i, var = job; cnf, top = (cA, pA.top) if var == 'A' else (cB, pB.top); p = os.path.join(tmp, f'{i}{var}.cnf')
    with open(p, 'w') as fo:
        fo.write(f'p cnf {top} {len(cnf.clauses) + len(cubes[i])}\n')
        for cl in cnf.clauses: fo.write(' '.join(map(str, cl)) + ' 0\n')
        for l in cubes[i]: fo.write(f'{l} 0\n')
    t = time.time(); r = subprocess.run([CAD, '-q', '-n', '-t', str(TO), p], capture_output=True); dt = time.time() - t; os.remove(p)
    st = {10: 'SAT', 20: 'UNSAT'}.get(r.returncode, 'TIMEOUT')
    print(f'cube {i} {var}: {st} {dt:.1f} s', flush=True); return i, var, st, round(dt, 1)
res = {}
with ThreadPoolExecutor(JOBS) as ex:
    for i, var, st, dt in ex.map(run, [(i, v) for i in range(len(cubes)) for v in 'AB']): res.setdefault(i, {})[var] = (st, dt)
both = [i for i in res if res[i]['A'][0] == 'UNSAT' and res[i]['B'][0] == 'UNSAT']
summ = {'tag': tag, 'c': c, 'cubes': len(cubes), 'timeout': TO, 'depth': DEPTH, 'seed_items': len(items),
        'A_solved': sum(1 for i in res if res[i]['A'][0] != 'TIMEOUT'), 'B_solved': sum(1 for i in res if res[i]['B'][0] != 'TIMEOUT'),
        'SAT_seen': sum(1 for i in res for v in 'AB' if res[i][v][0] == 'SAT'),
        'A_total_s': round(sum(res[i]['A'][1] for i in res), 1), 'B_total_s': round(sum(res[i]['B'][1] for i in res), 1),
        'both_unsat': len(both), 'A_s_on_both': round(sum(res[i]['A'][1] for i in both), 1), 'B_s_on_both': round(sum(res[i]['B'][1] for i in both), 1),
        'per_cube': {str(i): {'cube': cubes[i], 'A': res[i]['A'], 'B': res[i]['B']} for i in sorted(res)}}
json.dump(summ, open(outp, 'w'), indent=1); print('SUMMARY', json.dumps({k: v for k, v in summ.items() if k != 'per_cube'}))
