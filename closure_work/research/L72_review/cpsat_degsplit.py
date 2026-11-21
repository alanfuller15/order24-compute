"""Uncertified CP-SAT check of 'no 17-vertex triangle-free graph with m edges (m in args) in which every
12-set spans >= 12 edges', split by degree sequence. Sound split: every such graph has a labelling with
nonincreasing degrees; sequences enumerated with max degree <= m - L(16) = m-24 and top pair
d1+d2-1 <= m - L(15) (both are consequences of the floors, which are also imposed as constraints).
Floors imposed for every k-set (k=12..16): 12,15,18,21,24 (L(13..16) from the averaging recurrence)."""
import sys, itertools, json, time
from ortools.sat.python import cp_model
n = 17; FL = {12: 12, 13: 15, 14: 18, 15: 21, 16: 24}
def seqs(k, s, mx):
    if k == 0:
        if s == 0: yield ()
        return
    for d in range(min(mx, s), -1, -1):
        if d * k < s: break
        for r in seqs(k - 1, s - d, d): yield (d,) + r
def solve(m, q, tl):
    M = cp_model.CpModel()
    x = {p: M.NewBoolVar('') for p in itertools.combinations(range(n), 2)}
    X = lambda u, v: x[(u, v) if u < v else (v, u)]
    for i, j, k in itertools.combinations(range(n), 3):
        M.AddBoolOr([x[i, j].Not(), x[i, k].Not(), x[j, k].Not()])
    for k, f in FL.items():
        for U in itertools.combinations(range(n), k):
            M.Add(sum(x[p] for p in itertools.combinations(U, 2)) >= f)
    for v in range(n): M.Add(sum(X(v, u) for u in range(n) if u != v) == q[v])
    M.Add(sum(x.values()) == m)
    S = cp_model.CpSolver(); S.parameters.num_workers = 1; S.parameters.max_time_in_seconds = tl
    return S.StatusName(S.Solve(M))
for m in map(int, sys.argv[1:]):
    S = [q for q in seqs(n, 2 * m, m - 24) if q[0] + q[1] - 1 <= m - 21]
    cnt = {}
    for q in S:
        t0 = time.time(); st = solve(m, q, 300)
        cnt[st] = cnt.get(st, 0) + 1
        print(json.dumps({'m': m, 'seq': q, 'status': st, 'secs': round(time.time() - t0, 2)}), flush=True)
    print(json.dumps({'m': m, 'sequences': len(S), 'summary': cnt}), flush=True)
