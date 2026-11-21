#!/usr/bin/env python3
"""RA9X15 independent re-implementation (standard library only) for Case B profile (4^14, 5), 8+7 bipartition.

Setting (MATH.md 4g.2 + review part 1): h in X (the 8-class), M_h = C = {4..8} (WLOG by S_9);
(MAX) for h and i in B = {0,1,2,3} gives a low y in Y with M_y = B.  k := number of low X masks inside C
(= d_X(y) - 1).  Low X masks other than those k all meet B and C.

Modes
  --mode gpt     : ChatGPT round 11 statement: k = 2 only (seeds D, R), the constraints of 2.3, and at a completed X
                   the optimistic count of degree-3 Y types with residual capacity.
  --mode general : k = 0..3 (all seeds up to S_5 on C), NO degree-3 assumption; at a completed X an exact
                   backtracking search for the remaining 6 Y masks under necessary conditions (see check_Y).
Relaxation flags (controls): --q Q (pair cap, default 3), --mult M (default 2), --rmax R (default 8),
  --f8 T (8-set floor threshold, default 12), --f9 T (9-set floor threshold, default 12), --nobudget,
  --y4 T (threshold for degree sums of 4-subsets of Y, default 12), --dmax D (max d_X of a Y vertex, default 4),
  --yfloor T (Y-floor threshold, default 12), --seeds NAMES (comma list), --limit N (stop after N Y-survivors).
"""
import sys, itertools, time
from collections import Counter

argv = sys.argv[1:]
def opt(name, default, typ=int):
    return typ(argv[argv.index(name) + 1]) if name in argv else default
MODE = opt('--mode', 'general', str)
QMAX = opt('--q', 3); MMAX = opt('--mult', 2); RMAX = opt('--rmax', 8)
F8 = opt('--f8', 12); F9 = opt('--f9', 12); BUDGET = '--nobudget' not in argv
Y4 = opt('--y4', 12); DMAX = opt('--dmax', 4); YFL = opt('--yfloor', 12)
SEEDSEL = opt('--seeds', None, str); PROG = opt('--prog', 0); NOY = '--noY' in argv; LIMIT = opt('--limit', 10**9)

N = 9
B = 0b000001111
C = 0b111110000
H = C                                   # mask of h
M4 = [sum(1 << i for i in c) for c in itertools.combinations(range(N), 4)]
IDX = {m: t for t, m in enumerate(M4)}
EL = {m: [i for i in range(N) if m >> i & 1] for m in M4}
EL[H] = [i for i in range(N) if H >> i & 1]
PAIRS = list(itertools.combinations(range(N), 2)); PI = {p: t for t, p in enumerate(PAIRS)}
PR = {m: [PI[p] for p in itertools.combinations(EL[m], 2)] for m in M4}
def pc(x): return bin(x).count('1')

subC = [m for m in M4 if m & B == 0]            # the five 4-subsets of C
def comp_mask(e): return C & ~(1 << e)          # C \ {e}

def seed_list():
    # multisets of k 4-subsets of C, multiplicity <= 2 (N3), up to S_5 on C: represented by missing elements
    S = {0: [('k0', [])], 1: [('k1', [8])], 2: [('D', [7, 8]), ('R', [8, 8])],
         3: [('T3', [6, 7, 8]), ('T21', [8, 8, 7])]}
    if MODE == 'gpt':
        out = S[2]
    else:
        out = [s for k in range(4) for s in S[k]]
    if SEEDSEL:
        out = [s for s in out if s[0] in SEEDSEL.split(',')]
    return [(nm, [comp_mask(e) for e in miss]) for nm, miss in out]

class State:
    def __init__(self):
        self.r = [0] * N        # incidences over all placed outside vertices (X, y, later Y)
        self.rX = [0] * N       # incidences over X only (h included)
        self.q = [0] * 36       # low masks containing a pair
        self.mu = Counter()     # multiplicity of low masks
    def ok(self, m):
        if self.mu[m] >= MMAX: return False
        r = self.r; q = self.q
        for i in EL[m]:
            if r[i] >= RMAX: return False
        for t in PR[m]:
            if q[t] >= QMAX: return False
        return True
    def add(self, m, s, inX):
        for i in EL[m]:
            self.r[i] += s
            if inX: self.rX[i] += s
        for t in PR[m]: self.q[t] += s
        self.mu[m] += s

tot = Counter()
ysurv = []

def check_Y(st, X):
    """Exact search for Y = {y=B} + 6 low masks, all necessary conditions; returns number of Y completions found
    (stops at the first).  Conditions: Y pairwise intersecting (Y independent, Theorem 1); mult <= MMAX, q4 <= QMAX,
    r_i <= RMAX over all 15 masks; d_X(z) <= DMAX for z in Y; d_Y(x) <= 4 for low x in X (h: its Y-neighbours are
    copies of B, bounded by mult); every 4-subset U of Y: sum d_X >= Y4 (12-set X u U, X,Y independent);
    Y-floor: every 5-set K of I: sum_K r_i(Y) >= YFL (12-set Y u K)."""
    lowX = X[1:]
    def dX(m): return sum(1 for x in X if x & m == 0)
    d0 = dX(B)
    cands = [m for m in M4 if m & B and dX(m) <= DMAX]
    deg = {m: dX(m) for m in cands}
    # cheap necessary condition: at least 4 Y vertices with d_X >= 3 when Y4 = 12 (d4 >= 3 since d <= 4)
    need_hi = max(0, Y4 - 3 * DMAX)   # 4 smallest sum >= Y4 and each <= DMAX => 4th smallest >= Y4 - 3*DMAX
    cap_hi = 0
    for m in cands:
        if deg[m] >= need_hi:
            c = min([MMAX - st.mu[m]] + [RMAX - st.r[i] for i in EL[m]] + [QMAX - st.q[t] for t in PR[m]])
            if c > 0: cap_hi += c
    have = 1 if d0 >= need_hi else 0
    if have + cap_hi < 4:
        tot['Y_cheap_reject'] += 1
        return 0
    tot['Y_exact_calls'] += 1
    dY = [0] * len(lowX)
    Y = [B]; degs = [d0]; rY = [1 if B >> i & 1 else 0 for i in range(N)]
    for j, x in enumerate(lowX):
        if x & B == 0: dY[j] += 1
    found = [0]
    def foursmall_ok(ds):
        if len(ds) < 4: return True
        return sum(sorted(ds)[:4]) >= Y4
    def rec(start, left):
        tot['Y_nodes'] += 1
        if left == 0:
            # Y-floor: four largest r_i(Y) <= 28 - YFL  <=> every 5-set has sum >= YFL
            if sum(sorted(rY)[:5]) < YFL: return
            found[0] += 1
            ysurv.append((list(X), list(Y)))
            return
        for t in range(start, len(cands)):
            m = cands[t]
            if not st.ok(m): continue
            if any(m & z == 0 for z in Y): continue
            # degree caps of low X vertices
            bad = False
            for j, x in enumerate(lowX):
                if x & m == 0 and dY[j] >= 4: bad = True; break
            if bad: continue
            degs.append(deg[m])
            if not foursmall_ok(degs):
                degs.pop(); continue
            st.add(m, 1, False); Y.append(m)
            for i in EL[m]: rY[i] += 1
            for j, x in enumerate(lowX):
                if x & m == 0: dY[j] += 1
            rec(t, left - 1)
            for j, x in enumerate(lowX):
                if x & m == 0: dY[j] -= 1
            for i in EL[m]: rY[i] -= 1
            Y.pop(); st.add(m, -1, False); degs.pop()
            if found[0]: return
    rec(0, 6)
    return found[0]

def gpt_leaf(st, X):
    # optimistic: 4-masks with exactly 3 neighbours in X, residual capacity
    capsum = 0; types = 0; extra_types = 0
    for m in M4:
        if sum(1 for x in X if x & m == 0) != 3: continue
        types += 1
        c = min([MMAX - st.mu[m]] + [RMAX - st.r[i] for i in EL[m]] + [QMAX - st.q[t] for t in PR[m]])
        if m != B: extra_types += 1
        if m != B:
            tot['extra_deg3_any'] += 1
            if m & B: tot['extra_deg3_meeting_B_any'] += 1
        if c > 0:
            capsum += c
            if m != B:
                tot['extra_deg3_positive_cap'] += 1
                if m & B: tot['extra_deg3_positive_cap_meeting_B'] += 1
            else:
                tot['B_positive_cap'] += 1
    tot['deg3types_hist_%d' % types] += 1
    tot['capsum_%d' % capsum] += 1
    if capsum >= 6: tot['gpt_relax_survivors'] += 1

def run_seed(name, seed):
    st = State()
    k = len(seed)
    # place h and y
    for i in EL[H]: st.r[i] += 1; st.rX[i] += 1
    st.add(B, 1, False)                  # y is low, in Y
    for m in seed:
        if not st.ok(m): tot['seed_rejected'] += 1; return
        st.add(m, 1, True)
    X = [H] + list(seed)
    d0 = 1 + k
    rest = 7 - k
    # candidates for the other low X masks: meet B and C, meet h (automatic) and every seed mask
    cands = [m for m in M4 if m & B and m & C and all(m & s for s in seed)]
    loc = Counter(); t0 = time.time()
    def leaf():
        loc['completed_X'] += 1
        rX = st.rX
        if sum(sorted(rX)[:4]) < F8: return
        loc['pass_f8'] += 1
        rXy = [rX[i] + (B >> i & 1) for i in range(N)]
        if d0 + sum(sorted(rXy)[:3]) < F9: return
        loc['pass_both'] += 1
        if MODE == 'gpt':
            gpt_leaf(st, X)
        elif not NOY:
            if check_Y(st, X):
                loc['Y_survivors'] += 1
    def rec(cl, left):
        loc['nodes'] += 1
        if PROG and loc['nodes'] % PROG == 0:
            print('  progress', name, dict(sorted(loc.items())), dict(sorted(tot.items())), '%.0fs' % (time.time() - t0), flush=True)
        if left == 0:
            leaf(); return
        if BUDGET:
            cb = sum(st.rX[i] for i in EL[C]) if False else sum(st.rX[4:9])
            if cb + left > 21: return          # each remaining mask adds >= 1 to C
        for t in range(len(cl)):
            m = cl[t]
            if not st.ok(m): continue
            if BUDGET and sum(st.rX[4:9]) + pc(m & C) + (left - 1) > 21: continue
            st.add(m, 1, True); X.append(m)
            ncl = [z for z in cl[t:] if z & m]
            rec(ncl, left - 1)
            X.pop(); st.add(m, -1, True)
            if len(ysurv) >= LIMIT: return
    rec(cands, rest)
    print(name, 'k=%d' % k, dict(sorted(loc.items())), 'time %.1fs' % (time.time() - t0), flush=True)
    for key, v in loc.items(): tot[key] += v

def main():
    print('args', argv, 'mode', MODE, flush=True)
    for name, seed in seed_list():
        run_seed(name, seed)
        if len(ysurv) >= LIMIT: break
    print('TOTAL', dict(sorted(tot.items())), flush=True)
    for X, Y in ysurv[:5]:
        print('example X', [EL[m] for m in X], 'Y', [EL[m] for m in Y])
    print('Y survivors', len(ysurv))

main()
