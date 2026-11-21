"""Independent brute-force check of a candidate JSON written by model_1nines.py (cross-check of its checker).
Builds the 24-vertex graph: I = 0..8 (independent), v = 9 (adjacent to all of I), F = 10..23 with
N_I(x) = mask, x ~ y in F iff masks disjoint, v isolated in O. Reports triangle-freeness, max degree,
alpha (exact), edge-maximality ((MAX)), and the exact minimum number of edges over all C(24,12) 12-sets.
Usage: verify_graph.py candidate.json"""
import json
import sys
import itertools as it

rec = json.load(open(sys.argv[1]))
masks = [sum(1 << i for i in mk) for mk in rec['masks']]
N = 24
adj = [0] * N
def edge(a, b):
    adj[a] |= 1 << b
    adj[b] |= 1 << a
for i in range(9):
    edge(9, i)
for k, mk in enumerate(masks):
    for i in range(9):
        if mk >> i & 1:
            edge(10 + k, i)
for k, l in it.combinations(range(14), 2):
    if masks[k] & masks[l] == 0:
        edge(10 + k, 10 + l)
tri = any(adj[a] & adj[b] for a in range(N) for b in range(a + 1, N) if adj[a] >> b & 1)
maxdeg = max(bin(a).count('1') for a in adj)
nonmax = [(a, b) for a in range(N) for b in range(a + 1, N) if not adj[a] >> b & 1 and not adj[a] & adj[b]]
def alpha(P):
    if not P:
        return 0
    v = (P & -P).bit_length() - 1
    return max(alpha(P & ~(1 << v)), 1 + alpha(P & ~(1 << v) & ~adj[v]))
al = alpha((1 << N) - 1)
best = 10 ** 9
for S in it.combinations(range(N), 12):
    bm = 0
    for x in S:
        bm |= 1 << x
    e = sum(bin(adj[x] & bm).count('1') for x in S) // 2
    if e < best:
        best = e
        arg = S
print(f"profile {rec['profile']} thr {rec['thr']}: triangle-free {not tri}, max degree {maxdeg}, alpha {al}, "
      f"non-adjacent pairs without common neighbour {len(nonmax)}, min edges over 12-sets {best} (e.g. {arg})")
