"""CEGAR SAT check: is there a triangle-free graph on n vertices with <= m edges
(or == m with --exact) such that every 12-vertex induced subgraph spans >= 12 edges?
Lazy 12-set constraints; on UNSAT writes the final CNF (triangle clauses + global card
+ all lazily added 12-set constraints, a subset of the full formula => UNSAT is sound)."""
import sys, itertools, argparse, json, time
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

ap = argparse.ArgumentParser()
ap.add_argument('n', type=int); ap.add_argument('m', type=int)
ap.add_argument('--exact', action='store_true')
ap.add_argument('--out', default=None)
ap.add_argument('--floors', default='12:12')
a = ap.parse_args()
n, m, K = a.n, a.m, 12
pool = IDPool()
E = {}
for i, j in itertools.combinations(range(n), 2):
    E[(i, j)] = E[(j, i)] = pool.id(('e', i, j))
evars = [E[(i, j)] for i, j in itertools.combinations(range(n), 2)]
cnf = CNF()
for i, j, k in itertools.combinations(range(n), 3):
    cnf.append([-E[(i, j)], -E[(i, k)], -E[(j, k)]])
enc = CardEnc.equals if a.exact else CardEnc.atmost
cnf.extend(enc(evars, bound=m, vpool=pool, encoding=EncType.seqcounter).clauses)
S = Solver(name='cadical195', bootstrap_with=cnf.clauses)
FL = [tuple(map(int, kv.split(':'))) for kv in a.floors.split(',')]
subsets = [(T, f) for k, f in FL for T in itertools.combinations(range(n), k)]
added = []
t0 = time.time(); it = 0
while True:
    it += 1
    if not S.solve():
        res = 'UNSAT'; break
    mod = set(l for l in S.get_model() if l > 0)
    adj = [0] * n
    for i, j in itertools.combinations(range(n), 2):
        if E[(i, j)] in mod: adj[i] |= 1 << j; adj[j] |= 1 << i
    new = 0
    for T, f in subsets:
        mask = 0
        for v in T: mask |= 1 << v
        e2 = sum(bin(adj[v] & mask).count('1') for v in T)
        if e2 < 2 * f:
            sv = [E[(i, j)] for i, j in itertools.combinations(T, 2)]
            cl = CardEnc.atleast(sv, bound=f, vpool=pool, encoding=EncType.seqcounter).clauses
            S.append_formula(cl); cnf.extend(cl); added.append(T); new += 1
            if new >= 50: break
    if new == 0:
        res = 'SAT'; break
r = {'floors': a.floors, 'n': n, 'm': m, 'exact': a.exact, 'result': res, 'iters': it, 'lazy_sets': len(added),
     'secs': round(time.time() - t0, 1)}
if res == 'SAT':
    edges = [(i, j) for i, j in itertools.combinations(range(n), 2) if E[(i, j)] in mod]
    r['edges'] = edges; r['num_edges'] = len(edges)
    # independent re-check of witness
    adjs = {v: set() for v in range(n)}
    for i, j in edges: adjs[i].add(j); adjs[j].add(i)
    assert all(not (adjs[i] & adjs[j]) for i, j in edges), 'triangle'
    assert all(sum(1 for i, j in edges if i in T and j in T) >= K for T in map(set, itertools.combinations(range(n), K)))
    r['witness_rechecked'] = True
if res == 'UNSAT' and a.out:
    cnf.to_file(a.out); r['cnf'] = a.out; r['nv'] = cnf.nv; r['ncls'] = len(cnf.clauses)
print(json.dumps(r))
