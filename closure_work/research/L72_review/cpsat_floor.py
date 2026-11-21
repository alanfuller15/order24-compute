"""CP-SAT (uncertified) check of the pure model: n vertices, triangle-free,
every 12-subset spans >= 12 edges, total edges <= m (or == m with --exact).
No symmetry breaking, no redundant constraints. SAT witnesses are re-checked in plain Python."""
import sys, itertools, json, time, argparse
from ortools.sat.python import cp_model
ap = argparse.ArgumentParser(); ap.add_argument('n', type=int); ap.add_argument('m', type=int)
ap.add_argument('--exact', action='store_true'); ap.add_argument('--floors', default=''); ap.add_argument('--degsort', action='store_true'); ap.add_argument('--tl', type=float, default=1800)
a = ap.parse_args(); n, m = a.n, a.m
M = cp_model.CpModel()
x = {p: M.NewBoolVar(f'x{p}') for p in itertools.combinations(range(n), 2)}
for i, j, k in itertools.combinations(range(n), 3):
    M.AddBoolOr([x[i, j].Not(), x[i, k].Not(), x[j, k].Not()])
for T in itertools.combinations(range(n), 12):
    M.Add(sum(x[p] for p in itertools.combinations(T, 2)) >= 12)
# optional hereditary floors k:f (assumed lemmas, e(U) >= f for every k-subset U)
for kv in filter(None, a.floors.split(',')):
    k, f = map(int, kv.split(':'))
    for U in itertools.combinations(range(n), k):
        M.Add(sum(x[p] for p in itertools.combinations(U, 2)) >= f)
if a.degsort:  # sound symmetry break: some labelling has d(0) >= d(1) >= ... >= d(n-1)
    deg = [sum(x[tuple(sorted((v, u)))] for u in range(n) if u != v) for v in range(n)]
    for v in range(n - 1): M.Add(deg[v] >= deg[v + 1])
tot = sum(x.values())
M.Add(tot == m) if a.exact else M.Add(tot <= m)
S = cp_model.CpSolver(); S.parameters.num_workers = 1; S.parameters.max_time_in_seconds = a.tl
t0 = time.time(); st = S.Solve(M)
r = {'degsort': a.degsort, 'floors': a.floors, 'n': n, 'm': m, 'exact': a.exact, 'status': S.StatusName(st), 'secs': round(time.time() - t0, 1)}
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    E = [p for p in x if S.Value(x[p])]
    adj = {v: set() for v in range(n)}
    for i, j in E: adj[i].add(j); adj[j].add(i)
    assert all(not (adj[i] & adj[j]) for i, j in E)
    assert all(sum(1 for i, j in E if i in T and j in T) >= 12 for T in map(set, itertools.combinations(range(n), 12)))
    r.update(edges=E, num_edges=len(E), degrees=sorted(len(adj[v]) for v in range(n)), witness_rechecked=True)
print(json.dumps(r), flush=True)
