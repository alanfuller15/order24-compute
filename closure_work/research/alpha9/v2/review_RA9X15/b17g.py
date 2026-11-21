#!/usr/bin/env python3
"""RA9X15: replacement for ChatGPT's "117-case check" (part 1 of round 11): Case B (4^14,5), 8+7 split, h in X.
Claim checked: no vertex of Y has d_X = 4.  Exhaustive split (every case uses only necessary conditions):
  IIa  a degree-4 Y vertex adjacent to h.  WLOG M_h = C = {4..8}; that vertex is y with mask B = {0,1,2,3}; its 3 low
       X-neighbours are 4-subsets of C (k = 3; seeds T3 = C-6,C-7,C-8 and T21 = C-8,C-8,C-7 up to S_5, see
       seeds_orbits.py); the other 4 low X masks meet B and C.
  IIb  a degree-4 Y vertex z not adjacent to h.  WLOG M_z = B' = {0,1,2,3}, C' = {4..8}; its 4 X-neighbours are low,
       4-subsets of C', distinct (q4 <= 3, N3), so = C'-p for p in C' - {c}; WLOG c = 8 (S_5 on C').  The other
       3 low X masks and h meet B' (else adjacent to z: degree 5, or z ~ h) and meet every X mask; h is a 5-set.
Then for every completed X (all floors) an exact backtracking search for the other 6 Y masks.
Necessary conditions used everywhere: X, Y pairwise-intersecting families (independent; Theorem 1); low mult <= 2
(N3); q4 <= 3 over low masks (M1); r_i <= 8 (deg(i) <= 8, F4); 8-set floor: every 4-set K of I has
sum_K r_i(X) >= 12 (12-set X u K); 9-set floor: d_X(w) + sum_K r_i(X u {w}) >= 12 for |K| = 3 (w = anchor);
Y: d_X <= 4, d_Y(x) <= 4 for low x in X, sum of d_X over any 4 Y vertices >= 12 (12-set X u U), Y-floor
sum_K r_i(Y) >= 12 for |K| = 5 (12-set Y u K); (MAX) for h: some Y mask = I - M_h.
Control flags: --q --mult --rmax --y4 --yfloor --nomaxh --case IIa|IIb --limit N."""
import sys, itertools, time
from collections import Counter
argv = sys.argv[1:]
def opt(n, d, t=int): return t(argv[argv.index(n) + 1]) if n in argv else d
QMAX = opt('--q', 3); MMAX = opt('--mult', 2); RMAX = opt('--rmax', 8); Y4 = opt('--y4', 12)
YFL = opt('--yfloor', 12); F8 = opt('--f8', 12); F9 = opt('--f9', 12); MAXH = '--nomaxh' not in argv
CASES = opt('--case', 'IIa,IIb', str).split(','); LIMIT = opt('--limit', 10**9)
N = 9; FULL = (1 << N) - 1
B = 0b000001111; C = 0b111110000
M4 = [sum(1 << i for i in c) for c in itertools.combinations(range(N), 4)]
M5 = [sum(1 << i for i in c) for c in itertools.combinations(range(N), 5)]
EL = {m: [i for i in range(N) if m >> i & 1] for m in M4 + M5}
PI = {p: t for t, p in enumerate(itertools.combinations(range(N), 2))}
PR = {m: [PI[p] for p in itertools.combinations(EL[m], 2)] for m in M4}
def pc(x): return bin(x).count('1')
tot = Counter(); surv = []

class St:
    def __init__(s): s.r = [0] * N; s.q = [0] * 36; s.mu = Counter()
    def ok(s, m):
        return s.mu[m] < MMAX and all(s.r[i] < RMAX for i in EL[m]) and all(s.q[t] < QMAX for t in PR[m])
    def add(s, m, d, low=True):
        for i in EL[m]: s.r[i] += d
        if low:
            for t in PR[m]: s.q[t] += d
            s.mu[m] += d

def floors(X, anchor):
    rX = [sum(1 for x in X if x >> i & 1) for i in range(N)]
    if sum(sorted(rX)[:4]) < F8: return False
    dA = sum(1 for x in X if x & anchor == 0)
    rXa = [rX[i] + (anchor >> i & 1) for i in range(N)]
    return dA + sum(sorted(rXa)[:3]) >= F9

def searchY(st, X, anchor):
    """st holds X (h with low=False) and the anchor (low).  Exact search for 6 more Y masks, chosen in
    nonincreasing d_X order (candidates sorted by degree desc, multiset = nondecreasing position)."""
    h = X[0]; lowX = X[1:]
    def dX(m): return sum(1 for x in X if x & m == 0)
    cands = sorted([m for m in M4 if m & anchor and dX(m) <= 4], key=lambda m: (-dX(m), m))
    deg = [dX(m) for m in cands]
    tot['Ycand_maxdeg_%d' % (deg[0] if deg else -1)] += 1
    tot['Ycand_n_deg>=3_%d' % sum(1 for d in deg if d >= 3)] += 1
    dY = [sum(1 for x in lowX if x & anchor == 0)] if False else [1 if x & anchor == 0 else 0 for x in lowX]
    Y = [anchor]; degs = [dX(anchor)]; rY = [anchor >> i & 1 for i in range(N)]
    found = [0]
    def rec(start, left):
        tot['Y_nodes'] += 1
        if left == 0:
            if sum(sorted(rY)[:5]) < YFL: return
            if sum(sorted(degs)[:4]) < Y4: return
            if MAXH and (FULL & ~h) not in Y: return
            found[0] += 1; surv.append((list(X), list(Y))); return
        for t in range(start, len(cands)):
            m = cands[t]; d = deg[t]
            # all later picks have degree <= d: optimistic completion
            if sum(sorted(degs + [d] * left)[:4]) < Y4: break
            if not st.ok(m) or any(m & z == 0 for z in Y): continue
            if any(x & m == 0 and dY[j] >= 4 for j, x in enumerate(lowX)): continue
            st.add(m, 1); Y.append(m); degs.append(d)
            for i in EL[m]: rY[i] += 1
            for j, x in enumerate(lowX):
                if x & m == 0: dY[j] += 1
            rec(t, left - 1)
            for j, x in enumerate(lowX):
                if x & m == 0: dY[j] -= 1
            for i in EL[m]: rY[i] -= 1
            degs.pop(); Y.pop(); st.add(m, -1)
            if found[0] or len(surv) >= LIMIT: return
    rec(0, 6)
    return found[0]

def caseIIa():
    for name, miss in (('T3', (6, 7, 8)), ('T21', (8, 8, 7))):
        loc = Counter(); t0 = time.time()
        st = St(); st.add(C, 1, low=False); st.add(B, 1)
        seed = [C & ~(1 << e) for e in miss]
        okseed = True
        for m in seed:
            if not st.ok(m): okseed = False
            st.add(m, 1)
        if not okseed: print(name, 'seed rejected'); continue
        X = [C] + seed
        cands = [m for m in M4 if m & B and m & C and all(m & s for s in seed)]
        def rec(cl, left):
            loc['nodes'] += 1
            if left == 0:
                loc['completed_X'] += 1
                if not floors(X, B): return
                loc['pass_floors'] += 1
                if searchY(st, X, B): loc['Y_survivors'] += 1
                return
            cb = sum(pc(x & C) for x in X)
            for t, m in enumerate(cl):
                if cb + pc(m & C) + (left - 1) > 21: continue
                if not st.ok(m): continue
                st.add(m, 1); X.append(m)
                rec([z for z in cl[t:] if z & m], left - 1)
                X.pop(); st.add(m, -1)
        rec(cands, 4)
        print('IIa', name, dict(sorted(loc.items())), '%.1fs' % (time.time() - t0), flush=True)
        for k, v in loc.items(): tot['IIa_' + k] += v

def caseIIb():
    loc = Counter(); t0 = time.time()
    Bp, Cp = B, C
    st = St(); st.add(Bp, 1)                      # z, low, in Y
    four = [Cp & ~(1 << p) for p in (4, 5, 6, 7)]  # common element c = 8
    for m in four: st.add(m, 1)
    cands = [m for m in M4 if m & Bp and all(m & f for f in four)]
    hc = [m for m in M5 if m & Bp and all(m & f for f in four)]
    X = list(four)
    def budget(Xall): return sum(pc(x & Cp) for x in Xall)
    def rec(cl, left):
        loc['nodes'] += 1
        if budget(X) + left + 1 > 21: return          # each remaining low mask and h add >= 1 to C'
        if left == 0:
            for hm in hc:
                if not all(hm & x for x in X): continue
                if budget(X) + pc(hm & Cp) > 21: continue
                if not all(st.r[i] < RMAX for i in EL[hm]): continue
                loc['completed_X'] += 1
                XX = [hm] + X
                if not floors(XX, Bp): continue
                loc['pass_floors'] += 1
                st.add(hm, 1, low=False)
                if searchY(st, XX, Bp): loc['Y_survivors'] += 1
                st.add(hm, -1, low=False)
            return
        for t, m in enumerate(cl):
            if not st.ok(m): continue
            st.add(m, 1); X.append(m)
            rec([z for z in cl[t:] if z & m], left - 1)
            X.pop(); st.add(m, -1)
    rec(cands, 3)
    print('IIb', dict(sorted(loc.items())), '%.1fs' % (time.time() - t0), flush=True)
    for k, v in loc.items(): tot['IIb_' + k] += v

print('args', argv, flush=True)
if 'IIa' in CASES: caseIIa()
if 'IIb' in CASES: caseIIb()
print('TOTAL', dict(sorted(tot.items())))
for X, Y in surv[:3]:
    print('example X', [EL[m] for m in X], 'Y', [EL[m] for m in Y])
print('survivors', len(surv))
