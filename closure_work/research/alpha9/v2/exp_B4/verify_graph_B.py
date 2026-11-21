"""Independent brute-force check of a candidate JSON written by model_B4.py (cross-check of its checker).
Builds the 24-vertex Case B graph: I = 0..8 (independent), O = 9..23 with N_I(x) = mask, x ~ y in O iff masks
disjoint (Theorem 1). Reports triangle-freeness, max degree (Case B needs <= 8), alpha (exact), edge-maximality
((MAX)), bipartiteness of G[O] and its class sizes, and the exact minimum number of edges over all C(24,12) 12-sets.
Usage: verify_graph_B.py candidate.json"""
import json
import sys
import itertools as it

rec = json.load(open(sys.argv[1]))
masks = [sum(1 << i for i in mk) for mk in rec['masks']]
assert len(masks) == 15
N = 24
adj = [0] * N


def edge(a, c):
    adj[a] |= 1 << c
    adj[c] |= 1 << a


for k, mk in enumerate(masks):
    for i in range(9):
        if mk >> i & 1:
            edge(9 + k, i)
for k, l in it.combinations(range(15), 2):
    if masks[k] & masks[l] == 0:
        edge(9 + k, 9 + l)
tri = any(adj[a] & adj[c] for a in range(N) for c in range(a + 1, N) if adj[a] >> c & 1)
maxdeg = max(bin(a).count('1') for a in adj)
nonmax = [(a, c) for a in range(N) for c in range(a + 1, N) if not adj[a] >> c & 1 and not adj[a] & adj[c]]


def alpha(P):
    if not P:
        return 0
    v = (P & -P).bit_length() - 1
    return max(alpha(P & ~(1 << v)), 1 + alpha(P & ~(1 << v) & ~adj[v]))


al = alpha((1 << N) - 1)
# bipartiteness of G[O] by BFS 2-colouring
col = {}
bip = True
for st in range(9, 24):
    if st in col:
        continue
    col[st] = 0
    q = [st]
    while q:
        u = q.pop()
        for w in range(9, 24):
            if adj[u] >> w & 1:
                if w not in col:
                    col[w] = 1 - col[u]
                    q.append(w)
                elif col[w] == col[u]:
                    bip = False
best = 10 ** 9
arg = None
for S in it.combinations(range(N), 12):
    bm = 0
    for x in S:
        bm |= 1 << x
    e = sum(bin(adj[x] & bm).count('1') for x in S) // 2
    if e < best:
        best = e
        arg = S
print(f"profile {rec['profile']} thr {rec['thr']}: triangle-free {not tri}, max degree {maxdeg}, alpha {al}, "
      f"non-adjacent pairs without common neighbour {len(nonmax)}, G[O] bipartite {bip} "
      f"(one 2-colouring: class sizes {sum(1 for v in col.values() if v == 0)}+{sum(1 for v in col.values() if v == 1)}), "
      f"edges in O {sum(bin(adj[x] >> 9).count('1') for x in range(9, 24)) // 2}, "
      f"min edges over 12-sets {best} (e.g. {arg})")
