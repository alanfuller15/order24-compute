# RA9X9: model check of Case A profile (4^13, 9^2) (v1 index 86), standard library only.
# Assumptions used (all accepted/verified elsewhere, NOT claims 3/4 of round 9):
#  * Theorem 1: low-low adjacency = disjoint masks; the two a=9 vertices (v, z) are isolated in G[O]  [(P11)]
#  * F = G[O \ {v,z}] (13 low vertices) is bipartite (claim 1, via 4f.1 + M1 in Case A), classes X (6), Y (7)
#    (alpha(F) <= 7)
#  * outside degree of an a=4 vertex <= 5 (deg <= 9)
#  * M1 (q4 <= 3), hence multiplicity <= 3 (multiplicity <= 2 is NOT assumed)
# Search: x = a vertex of maximum degree d in X (d >= 4 since every 10-set Y + 3 of X spans >= 12, avg >= 4).
# WLOG mask(x) = {0,1,2,3}; its Y-neighbours are d 4-subsets of C = {4..8} (multisets enumerated, q4 <= 3 filtered).
# Remaining Y vertices: masks meeting mask(x) (not adjacent to x) and every other Y mask (Y independent).
# Remaining X vertices: masks meeting mask(x) and each other, Y-degree in [2, d]  (degree >= 2: triple rule with cap 5).
# Leaves: q4 <= 3 on all 13, mult <= 3, all degrees <= 5, alpha(F) <= 7, every 10-subset of F spans >= 12 edges,
# r4_i <= 7; survivors (if any) get a full check of the 24-vertex graph (triangle-free, alpha <= 9, all 12-sets).
from itertools import combinations, combinations_with_replacement as cwr
import sys, time
I = range(9)
M4 = [sum(1 << i for i in c) for c in combinations(I, 4)]
A = 0b1111
C = [4,5,6,7,8]
subC = [sum(1 << i for i in c) for c in combinations(C, 4)]
PAIRS = [(1 << i) | (1 << j) for i, j in combinations(I, 2)]
def q4ok(fam):
    for p in PAIRS:
        if sum(1 for m in fam if m & p == p) > 3: return False
    return True
def multok(fam):
    return all(fam.count(m) <= 3 for m in set(fam))
def alpha_le(fam, k):
    # is there an independent (pairwise meeting) set of size k+1 ?
    n = len(fam)
    adj = [[(fam[a] & fam[b]) == 0 for b in range(n)] for a in range(n)]
    def rec(start, chosen, need):
        if need == 0: return True
        for v in range(start, n):
            if all(not adj[v][u] for u in chosen):
                if rec(v + 1, chosen + [v], need - 1): return True
        return False
    return not rec(0, [], k + 1)
def tenset_ok(fam):
    n = len(fam)
    edges = [(a, b) for a in range(n) for b in range(a+1, n) if fam[a] & fam[b] == 0]
    for out in combinations(range(n), n - 10):
        s = set(out)
        if sum(1 for a, b in edges if a not in s and b not in s) < 12: return False
    return True
def full_check(fam):
    # vertices: 0..8 = I, 9 = v, 10 = z, 11.. = low
    V = 11 + len(fam)
    adj = [set() for _ in range(V)]
    def add(a, b): adj[a].add(b); adj[b].add(a)
    for w in (9, 10):
        for i in I: add(w, i)
    for k, m in enumerate(fam):
        for i in I:
            if m >> i & 1: add(11 + k, i)
        for l in range(k):
            if m & fam[l] == 0: add(11 + k, 11 + l)
    for a in range(V):
        for b in adj[a]:
            if adj[a] & adj[b]: return "triangle"
    if max(len(adj[a]) for a in range(V)) > 9: return "degree"
    E = [(a, b) for a in range(V) for b in adj[a] if a < b]
    for S in combinations(range(V), 12):
        s = set(S)
        if sum(1 for a, b in E if a in s and b in s) < 12: return "12-set"
    return "SURVIVES"
stats = dict(nbr=0, ysets=0, xsets=0, leaves=0, q4=0, deg=0, alpha=0, ten=0, r=0, surv=0)
t0 = time.time()
survivors = []
for d in (5, 4):
    nbrs = [ms for ms in cwr(subC, d) if q4ok(list(ms))]
    # reduce under S5 on C: canonical = sorted tuple min over perms
    from itertools import permutations
    def act(m, p):
        r = m & A
        for i, c in enumerate(C):
            if m >> c & 1: r |= 1 << p[i]
        return r
    reps = {}
    for ms in nbrs:
        key = min(tuple(sorted(act(m, p) for m in ms)) for p in permutations(C))
        reps.setdefault(key, ms)
    for ms in reps.values():
        stats['nbr'] += 1
        Yfix = list(ms)
        ycands = [m for m in M4 if (m & A) and all(m & y for y in Yfix)]
        for yext in cwr(ycands, 7 - d):
            if any((a & b) == 0 for a, b in combinations(yext, 2)): continue
            Y = Yfix + list(yext)
            if not q4ok(Y) or not multok(Y): continue
            stats['ysets'] += 1
            ydeg = {}
            xc = []
            for m in M4:
                if not (m & A): continue
                dg = sum(1 for y in Y if (m & y) == 0)
                if 2 <= dg <= d: xc.append((m, dg))
            xm = [m for m, _ in xc]
            for xext in cwr(range(len(xm)), 5):
                ms5 = [xm[k] for k in xext]
                if any((a & b) == 0 for a, b in combinations(ms5, 2)): continue
                X = [A] + ms5
                stats['xsets'] += 1
                degs = [sum(1 for y in Y if (x & y) == 0) for x in X]
                if sum(degs) < 24:  # triple averaging (10 e >= 240); implied by tenset check too
                    continue
                if any(sum(sorted(degs)[:3]) < 12 for _ in [0]): continue
                fam = X + Y
                stats['leaves'] += 1
                if not q4ok(fam) or not multok(fam): stats['q4'] += 1; continue
                if any(sum(1 for o in fam if (o & y) == 0) > 5 for y in Y): stats['deg'] += 1; continue
                if any(bin(sum(1 for f in fam if f >> i & 1)).count('1') and sum(1 for f in fam if f >> i & 1) > 7 for i in I):
                    stats['r'] += 1; continue
                if not alpha_le(fam, 7): stats['alpha'] += 1; continue
                if not tenset_ok(fam): stats['ten'] += 1; continue
                res = full_check(fam)
                stats['surv'] += 1
                survivors.append((fam, res))
print("stats:", stats)
print("survivors before full 24-vertex check:", len(survivors))
for fam, res in survivors[:20]:
    print([sorted(i for i in I if m >> i & 1) for m in fam], res)
print("time %.1fs" % (time.time() - t0))
