# RA9X10: exhaustive F-level model check of the pure Case A profiles 4^(13-m) 5^m 9^2, m = 0..6
# (v1 86, 88, 91, 95, 99, 102, 105). Standard library only.  usage: python3 model_n9_2.py m [noq4]
#
# Assumptions (accepted results only; NONE of ChatGPT's round-9 part-2 lemmas, NOT Repair B):
#  * Theorem 1 (4b.2): two O-vertices adjacent iff masks disjoint.  Hence low(a=4)-low adjacency = disjoint masks,
#    an a=5 vertex h (write T(h) = I \ N_I(h), a 4-set) is adjacent exactly to the a=4 vertices of mask T(h);
#    a=5 vertices pairwise non-adjacent.  The two a=9 vertices v, z are isolated in G[O]  (P11).
#  * F = G[O \ {v,z}] (13 vertices) is bipartite (RA9X9 claim 1); alpha(F) <= 7 (alpha(G) <= 9 with v, z) so the
#    classes are X (6), Y (7) for any bipartition.  We fix one bipartition and enumerate (config, bipartition) pairs.
#  * deg <= 9: a=4 vertex has F-degree <= 5; a=5 vertex <= 4 (automatic); r_i := #F-masks containing i <= 7
#    (i has neighbours v, z).  Free a=5 vertices (T not a low mask anywhere) are wildcards: r_i is not checked for them
#    (a relaxation, sound).
#  * every 12-set spans >= 12 edges, used as: every 10-subset of F spans >= 12 edges ({v,z} + 10 of F).
#    Consequences used for pruning (all re-derived here): any 3 vertices of X have degree sum >= 12, so e(F) >= 24,
#    max X-degree d >= 4, and at most one X vertex has degree < 4 when d <= 5.
#  * M1 for pure Case A (RA9X9 Repair A): q4_ij <= 3 over the a=4 masks, hence low multiplicity <= 3, hence every
#    a=5 vertex has F-degree <= 3.  (Multiplicity <= 2 is NOT assumed for any m.)
# Search: x = a vertex of maximum degree d in X; d >= 4 > 3 >= any a=5 degree, so x is a=4; WLOG N_I(x) = A = {0,1,2,3}.
#  N(x) = dl low copies of 4-subsets of C = {4..8} (multiset, reduced under S5 on C) + h_A a=5 vertices with T = A
#  (ALL a=5 vertices with T = A are adjacent to x, so they all lie in Y).  Then the other Y lows (masks meeting A and all
#  Y-low masks, pairwise meeting), the other X lows (pairwise meeting, meeting A), then the remaining a=5 vertices:
#  Y ones attached to a low type occurring in X only, or free; X ones attached to a low type in Y only, or free.
# Leaf checks: q4 <= 3, degrees (X <= d, Y lows <= 5), 3-sums in X >= 12, every 10-subset of F >= 12 edges,
#  alpha(F) <= 7 (Koenig), r_i <= 7.
from itertools import combinations, combinations_with_replacement as cwr, permutations
import sys, time
m = int(sys.argv[1]); USE_Q4 = not (len(sys.argv) > 2 and sys.argv[2] == 'noq4')
I = range(9)
M4 = [sum(1 << i for i in c) for c in combinations(I, 4)]
A = 0b1111
C = [4, 5, 6, 7, 8]
subC = [sum(1 << i for i in c) for c in combinations(C, 4)]
PAIRIDX = {}
for k, (i, j) in enumerate(combinations(I, 2)): PAIRIDX[(i, j)] = k
MP = {M: [PAIRIDX[p] for p in combinations([i for i in I if M >> i & 1], 2)] for M in M4}
MAXMULT = 3 if USE_Q4 else 99
def q4ok(fam):
    if not USE_Q4: return True
    cnt = [0] * 36
    for M in fam:
        for p in MP[M]:
            cnt[p] += 1
            if cnt[p] > 3: return False
    return True
def act(M, p):
    r = M & A
    for i, c in enumerate(C):
        if M >> c & 1: r |= 1 << p[i]
    return r
def maxmatch(adjX, nY):  # adjX: list of lists of Y indices
    match = [-1] * nY
    def aug(u, seen):
        for w in adjX[u]:
            if not seen[w]:
                seen[w] = True
                if match[w] < 0 or aug(match[w], seen):
                    match[w] = u; return True
        return False
    return sum(1 for u in range(len(adjX)) if aug(u, [False] * nY))
FREE = -1
stats = dict(nreps=0, ysets=0, xnodes=0, xleaves=0, attach=0, deg=0, three=0, ten=0, alpha=0, r=0, surv=0)
survivors = []
t0 = time.time()

def leaf_checks(XL, YL, Yh, Xh, d):
    # XL, YL: lists of low masks; Yh, Xh: lists of T (4-mask) or FREE for a=5 vertices in Y / X
    Xv = [('L', M) for M in XL] + [('H', T) for T in Xh]
    Yv = [('L', M) for M in YL] + [('H', T) for T in Yh]
    def adj(a, b):
        if a[0] == 'L' and b[0] == 'L': return (a[1] & b[1]) == 0
        if a[0] == 'H' and b[0] == 'H': return False
        if a[0] == 'H': a, b = b, a
        return b[1] != FREE and a[1] == b[1]
    adjX = [[j for j, y in enumerate(Yv) if adj(x, y)] for x in Xv]
    degX = [len(r) for r in adjX]
    degY = [sum(1 for r in adjX if j in r) for j in range(7)]
    # degree caps
    for v, dg in zip(Xv, degX):
        if dg > d or (v[0] == 'H' and dg > 4): stats['deg'] += 1; return False
    for v, dg in zip(Yv, degY):
        if (v[0] == 'L' and dg > 5) or (v[0] == 'H' and dg > 4): stats['deg'] += 1; return False
    if sum(sorted(degX)[:3]) < 12: stats['three'] += 1; return False
    # every 10-subset of F spans >= 12 edges: remove each 3-set R
    deg = degX + degY
    E = [(i, 6 + j) for i in range(6) for j in adjX[i]]
    e = len(E)
    Eset = set(E)
    for R in combinations(range(13), 3):
        eR = sum(1 for a, b in combinations(R, 2) if (a, b) in Eset)
        if e - (deg[R[0]] + deg[R[1]] + deg[R[2]] - eR) < 12: stats['ten'] += 1; return False
    if 13 - maxmatch(adjX, 7) > 7: stats['alpha'] += 1; return False
    r = [0] * 9
    for t, M in Xv + Yv:
        if t == 'L': S = M
        elif M == FREE: continue
        else: S = 511 ^ M
        for i in I:
            if S >> i & 1: r[i] += 1
    if max(r) > 7: stats['r'] += 1; return False
    return True

for d in (5, 4):
    for dl in range(0, d + 1):
        hA = d - dl
        if hA > m: continue
        nbrs = [ms for ms in cwr(subC, dl) if q4ok(list(ms)) and all(ms.count(x) <= MAXMULT for x in set(ms))]
        reps = {}
        for ms in nbrs:
            key = min(tuple(sorted(act(M, p) for M in ms)) for p in permutations(C))
            reps.setdefault(key, ms)
        for ms in reps.values():
            stats['nreps'] += 1
            Ynb = list(ms)
            for mY in range(hA, m + 1):
                mX = m - mY
                eY = 7 - mY - dl
                if eY < 0 or 6 - mX < 1: continue
                f = mY - hA
                k = 5 - mX
                ycands = [M for M in M4 if (M & A) and all(M & y for y in Ynb) and not (hA > 0 and M == A)]
                seenY = set()
                for yext in cwr(ycands, eY):
                    if any((a & b) == 0 for a, b in combinations(yext, 2)): continue
                    YL = Ynb + list(yext)
                    if not q4ok(YL) or any(YL.count(x) > MAXMULT for x in set(YL)): continue
                    stats['ysets'] += 1
                    Ytypes = set(YL)
                    multY = {T: YL.count(T) for T in Ytypes}
                    hpotX = max(multY.values()) if multY else 0   # upper bound on an X a=5 vertex's degree
                    base = {}
                    cands = []
                    for B in M4:
                        if not (B & A): continue
                        b = sum(1 for y in YL if (B & y) == 0)
                        if B == A: b += hA; pot = b
                        else: pot = b + (f if B not in Ytypes else 0)
                        if b > d or pot < 2: continue
                        base[B] = b
                        cands.append((B, pot))
                    nc = len(cands)
                    # X a=5 vertices: each has degree <= hpotX; count those below 4 (3-sum rule: at most one X vertex < 4)
                    low_init = mX if hpotX < 4 else 0
                    if low_init > 1: continue
                    ydeg0 = [sum(1 for y in [A] if (y & yy) == 0) for yy in YL]
                    cnt0 = [0] * 36
                    if USE_Q4:
                        for M in YL + [A]:
                            for p in MP[M]: cnt0[p] += 1
                        if max(cnt0) > 3: continue
                    chosen = []
                    def dfs(start, lowc, ydeg, cnt, need):
                        stats['xnodes'] += 1
                        if len(chosen) == k:
                            process(chosen)
                            return
                        for ci in range(start, nc):
                            B, pot = cands[ci]
                            if any((B & c) == 0 for c in chosen): continue
                            # multiplicity (<= 3 in q4 mode) is enforced by the incremental q4 count below
                            nl = lowc + (1 if pot < 4 else 0)
                            if nl > 1: continue
                            nd = [ydeg[j] + (1 if (B & YL[j]) == 0 else 0) for j in range(len(YL))]
                            if any(x > 5 for x in nd): continue
                            nn = need
                            if B not in chosen and B != A and B not in Ytypes:
                                nn = need + max(0, 2 - base[B])
                                if nn > f: continue
                            if USE_Q4:
                                c2 = cnt[:]
                                bad = False
                                for p in MP[B]:
                                    c2[p] += 1
                                    if c2[p] > 3: bad = True; break
                                if bad: continue
                            else: c2 = cnt
                            chosen.append(B)
                            dfs(ci, nl, nd, c2, nn)
                            chosen.pop()
                    def process(ch):
                        stats['xleaves'] += 1
                        XL = [A] + list(ch)
                        if not USE_Q4:
                            pass
                        Xtypes = set(XL)
                        yopts = sorted(T for T in Xtypes if T != A and T not in Ytypes) + [FREE]
                        xopts = sorted(T for T in Ytypes if T not in Xtypes) + [FREE]
                        for yh in cwr(yopts, f):
                            for xh in cwr(xopts, mX):
                                stats['attach'] += 1
                                Yh = [A] * hA + list(yh)
                                if leaf_checks(XL, YL, Yh, list(xh), d):
                                    stats['surv'] += 1
                                    if len(survivors) < 50: survivors.append((XL, YL, Yh, list(xh)))
                    dfs(0, low_init, ydeg0, cnt0, 0)
def fmt(M): return ''.join(str(i) for i in I if M >> i & 1)
print("profile 4^%d 5^%d 9^2  q4=%s" % (13 - m, m, USE_Q4))
print("stats:", stats)
print("F-level survivors:", stats['surv'])
for XL, YL, Yh, Xh in survivors[:10]:
    print(" X lows", [fmt(x) for x in XL], "X a5 T", [fmt(t) if t != FREE else '*' for t in Xh],
          "| Y lows", [fmt(y) for y in YL], "Y a5 T", [fmt(t) if t != FREE else '*' for t in Yh])
print("time %.1fs" % (time.time() - t0))
