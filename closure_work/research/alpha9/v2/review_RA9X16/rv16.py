#!/usr/bin/env python3
"""RA9X16 independent re-implementation (std lib only) for Case B (4^13,5^2) [B18] and (4^12,5^3) [B19], 8+7 split.

Setting (MATH.md): Theorem 1 (x~y iff masks disjoint), 4f.1 (G[O] bipartite), 4g.2 (classes X (8), Y (7), both
independent => masks pairwise intersect inside a class).  Necessary conditions used (all PROVED in MATH.md):
  MULT  low multiplicity <= 2 (N3, b <= 6)          Q   q4_ij <= 3 over low masks (M1)
  R     r_i <= 8 over all 15 masks (Delta <= 8, F4)  DEG low d_O <= 4, high d_O <= 2 (Delta, N3)
  MAX   a high mask H has the low mask I\\H in the other class ((MAX)+(F4)+F1; Theorem 1 puts it in the other class)
  12-set floors: X u U (U in Y, |U| = 4): sum d_X >= 12; X u Z u K (Z in Y, K in I): sum_Z d_X + sigma(r(X u Z)) >= 12;
  Y u K (|K| = 5): sigma_5(r(Y)) >= 12.  Budget: 12-set B u X gives sum_X |M n C| <= 20 + h_X.
At every Y leaf a FULL exact check (fullcheck): every 12-set of V, alpha <= 9, Delta <= 8, edge-maximality (MAX).

--part 1 : degree-4 split.  y in Y low with d_X(y) = 4, M_y = B = {0..3}, C = {4..8}; c = # high X with mask C,
           4-c low X neighbours = 4-subsets of C (patterns up to S_5(C)); other 4 X masks meet B (and all X);
           exact search for the other 6 Y vertices (h_Y high, complements of low X masks).  No symmetry on extras.
--part 2 : degree-3 seeded search (assumes part 1: all Y low, d_X = 3).  x high in X with mask C, y in Y with B.
           Extras = b-c further high masks (orbit reps with --sym, all multisets without).  Exact Y search +
           optimistic capacity count.
Controls: --q --mult --rmax --thr (12-set threshold used in floors/Y conditions; full check unchanged) --nobudget
"""
import sys, itertools, time
from collections import Counter
argv = sys.argv[1:]
def opt(n, d, t=int): return t(argv[argv.index(n) + 1]) if n in argv else d
PART = opt('--part', 1); BS = [int(v) for v in opt('--b', '2,3', str).split(',')]
QMAX = opt('--q', 3); MMAX = opt('--mult', 2); RMAX = opt('--rmax', 8); THR = opt('--thr', 12)
BUDGET = '--nobudget' not in argv; SYM = '--sym' in argv; ONLY = opt('--only', None, str)
NOFLOOR = '--nofloor' in argv; LIMIT = opt('--limit', 20)
N = 9; FULL = 511; B = 0b000001111; C = 0b111110000
def pc(x): return bin(x).count('1')
M4 = [m for m in range(512) if pc(m) == 4]; M5 = [m for m in range(512) if pc(m) == 5]
EL = [[i for i in range(N) if m >> i & 1] for m in range(512)]
PIDX = {}
for t, (i, j) in enumerate(itertools.combinations(range(N), 2)): PIDX[(i, j)] = t
PR = [[PIDX[p] for p in itertools.combinations(EL[m], 2)] for m in range(512)]
def sig(v, k): return sum(sorted(v)[:k])

class St:
    """global counters over all placed outside vertices"""
    def __init__(s): s.r = [0] * N; s.q = [0] * 36; s.mu = [0] * 512
    def ok(s, m, hi, t=1):
        if not hi and s.mu[m] + t > MMAX: return False
        if any(s.r[i] + t > RMAX for i in EL[m]): return False
        if not hi and any(s.q[p] + t > QMAX for p in PR[m]): return False
        return True
    def add(s, m, hi, d):
        for i in EL[m]: s.r[i] += d
        if not hi:
            for p in PR[m]: s.q[p] += d
            s.mu[m] += d
    def cap(s, m):
        c = MMAX - s.mu[m]
        for i in EL[m]: c = min(c, RMAX - s.r[i])
        for p in PR[m]: c = min(c, QMAX - s.q[p])
        return max(c, 0)

# ---------------- full exact check of a complete configuration ----------------
def fullcheck(X, Y):
    """X, Y: lists of (mask, hi).  Builds G on 24 vertices (I = 0..8, O = 9..23) by Theorem 1 and checks every
    defining property.  Returns '' if G is a genuine member (would refute the claim), else the first failure."""
    O = X + Y
    if len(X) != 8 or len(Y) != 7: return 'size'
    n = 24; adj = [0] * n
    for k, (m, h) in enumerate(O):
        for i in EL[m]: adj[i] |= 1 << (9 + k); adj[9 + k] |= 1 << i
    for k in range(15):
        for l in range(k + 1, 15):
            if O[k][0] & O[l][0] == 0: adj[9 + k] |= 1 << (9 + l); adj[9 + l] |= 1 << (9 + k)
    if max(pc(a) for a in adj) > 8: return 'Delta'
    for u in range(n):
        for v in range(u + 1, n):
            if adj[u] >> v & 1:
                if adj[u] & adj[v]: return 'triangle'
            elif not (adj[u] & adj[v]): return 'notmaximal'
    # 12-sets: S subset of O (bits), then the best I-part = 12-|S| least r_i(S)
    eO = [0] * (1 << 15); rS = {}
    for S in range(1, 1 << 15):
        low = S & -S; k = low.bit_length() - 1; R = S ^ low
        eO[S] = eO[R] + pc((adj[9 + k] >> 9) & R)
    for S in range(1 << 15):
        s = pc(S)
        if s > 12: continue
        r = [0] * 9
        for k in range(15):
            if S >> k & 1:
                for i in EL[O[k][0]]: r[i] += 1
        if eO[S] + sig(r, 12 - s) < 12: return '12set'
    # alpha <= 9: max independent set
    best = [0]
    def mis(P, sz):
        if sz + pc(P) <= best[0]: return
        if P == 0: best[0] = max(best[0], sz); return
        v = P.bit_length() - 1
        mis(P & ~adj[v] & ~(1 << v), sz + 1); mis(P & ~(1 << v), sz)
    mis((1 << n) - 1, 0)
    if best[0] > 9: return 'alpha'
    return ''

tot = Counter(); survivors = []

# ---------------- Y search ----------------
def ysearch(st, X, Yfix, need, hiY, cand, dtarget, loc):
    """Exact search: choose `need` more Y vertices (multiset from cand, each (mask, hi, dX)) with exactly hiY high in
    total; Yfix already placed (and charged in st).  dtarget: None (part 1, 4-sum condition) or 3 (part 2)."""
    lowX = [(m, h) for m, h in X]
    dY = [sum(1 for z, _ in Yfix if z & m == 0) for m, _ in X]
    Y = list(Yfix); degs = [sum(1 for m, _ in X if m & z == 0) for z, _ in Yfix]
    nh = [sum(1 for _, h in Yfix if h)]
    found = [0]
    def rec(start, left):
        loc['Ynodes'] += 1
        if left == 0:
            if nh[0] != hiY: return
            if sig(degs, 4) < THR: return
            rY = [sum(1 for z, _ in Y if z >> i & 1) for i in range(N)]
            if sig(rY, 5) < THR: return
            loc['Yleaves'] += 1
            res = fullcheck(X, Y)
            loc['full_' + (res or 'PASS')] += 1
            if not res: found[0] += 1
            if len(survivors) < LIMIT: survivors.append(([EL[m] for m, _ in X], [EL[m] for m, _ in Y], res))
            return
        for t in range(start, len(cand)):
            m, hi, d = cand[t]
            if dtarget is None and sig(degs + [d] * left, 4) < THR: break  # cand sorted by d desc
            if hi and nh[0] >= hiY: continue
            if any(m & z == 0 for z, _ in Y): continue
            if not st.ok(m, hi): continue
            bad = False
            for j, (x, xh) in enumerate(X):
                if x & m == 0 and dY[j] + 1 > (2 if xh else 4): bad = True; break
            if bad: continue
            st.add(m, hi, 1); Y.append((m, hi)); degs.append(d); nh[0] += hi
            for j, (x, _) in enumerate(X):
                if x & m == 0: dY[j] += 1
            rec(t, left - 1)
            for j, (x, _) in enumerate(X):
                if x & m == 0: dY[j] -= 1
            st.add(m, hi, -1); Y.pop(); degs.pop(); nh[0] -= hi
    rec(0, need)
    return found[0]

def xfloors(X, Z):
    """12-set floors X u Z u K for every subset Z' of Z (Z = list of Y masks already known), |K| = 4 - |Z'|."""
    if NOFLOOR: return True
    rX = [sum(1 for m, _ in X if m >> i & 1) for i in range(N)]
    for j in range(0, min(len(Z), 3) + 1):
        for Zs in itertools.combinations(Z, j):
            r = rX[:]
            for z in Zs:
                for i in EL[z]: r[i] += 1
            if sum(sum(1 for m, _ in X if m & z == 0) for z in Zs) + sig(r, 4 - j) < THR: return False
    return True

def xcomplete(st, X, need_hi, need_lo, hcands, lcands, hX, Yforced_fn, leaf, loc):
    """enumerate multisets of need_hi high masks (from hcands) then need_lo low masks (from lcands), each meeting
    every X mask, with caps and budget; call leaf(X) on each completed X."""
    lim = 20 + hX
    def cb(): return sum(pc(m & C) for m, _ in X)
    def rec_lo(cl, left):
        loc['Xnodes'] += 1
        if BUDGET and cb() + left > lim: return
        if left == 0:
            loc['Xcompleted'] += 1; leaf(X); return
        for t, m in enumerate(cl):
            if not st.ok(m, False): continue
            if not Yforced_fn(m): continue
            st.add(m, False, 1); X.append((m, False))
            rec_lo([z for z in cl[t:] if z & m], left - 1)
            X.pop(); st.add(m, False, -1)
    def rec_hi(start, left):
        if left == 0:
            rec_lo([m for m in lcands if all(m & x for x, _ in X)], need_lo); return
        for t in range(start, len(hcands)):
            m = hcands[t]
            if not all(m & x for x, _ in X): continue
            if not st.ok(m, True): continue
            st.add(m, True, 1); X.append((m, True))
            rec_hi(t, left - 1)
            X.pop(); st.add(m, True, -1)
    rec_hi(0, need_hi)

# ---------------- part 1 ----------------
def sub(e): return C & ~(1 << e)
P1SEEDS = {0: [('1111', [4, 5, 6, 7])], 1: [('111', [6, 7, 8]), ('21', [8, 8, 7])],
           2: [('11', [7, 8]), ('2', [8, 8])], 3: [('1', [8])]}
def part1(b):
    for hX in range(b + 1):
        hY = b - hX
        for c in range(0, min(hX, 3) + 1):
            for nm, miss in P1SEEDS[c]:
                key = 'b%d_hX%d_hY%d_c%d_%s' % (b, hX, hY, c, nm)
                if ONLY and ONLY not in key: continue
                loc = Counter(); t0 = time.time()
                st = St(); st.add(B, False, 1)
                X = []
                ok = True
                for _ in range(c):
                    if not st.ok(C, True): ok = False
                    st.add(C, True, 1); X.append((C, True))
                for e in miss:
                    m = sub(e)
                    if not st.ok(m, False): ok = False
                    st.add(m, False, 1); X.append((m, False))
                if not ok: print(key, 'seed violates caps', flush=True); continue
                hc = [m for m in M5 if m != C and (m & B) != B]   # (MAX): I\\H in Y must meet B
                lc = [m for m in M4 if m & B]
                def leaf(X):
                    hiX = [m for m, h in X if h]
                    forced = sorted(set(FULL ^ m for m in hiX if m != C))
                    # forced Y masks (complements of high X masks other than C), at least one copy each
                    for z in forced:
                        if not (z & B): return
                    for z1, z2 in itertools.combinations(forced, 2):
                        if not (z1 & z2): return
                    if not xfloors(X, [B]): return
                    loc['Xfloor'] += 1
                    Yfix = [(B, False)]
                    added = []
                    good = True
                    for z in forced:
                        d = sum(1 for m, _ in X if m & z == 0)
                        if d > 4 or not st.ok(z, False): good = False; break
                        st.add(z, False, 1); added.append(z); Yfix.append((z, False))
                    if good:
                        dY = [sum(1 for z, _ in Yfix if z & m == 0) for m, _ in X]
                        if any(dY[j] > (2 if h else 4) for j, (m, h) in enumerate(X)): good = False
                    if good:
                        lowXm = set(m for m, h in X if not h)
                        cand = []
                        for m in M4:
                            if all(m & z for z, _ in Yfix):
                                d = sum(1 for x, _ in X if x & m == 0)
                                if d <= 4: cand.append((m, False, d))
                        for L in lowXm:
                            H = FULL ^ L
                            if all(H & z for z, _ in Yfix):
                                cand.append((H, True, sum(1 for x, _ in X if x & H == 0)))
                        cand.sort(key=lambda t: (-t[2], t[1], t[0]))
                        if ysearch(st, X, Yfix, 7 - len(Yfix), hY, cand, None, loc): loc['Ysurvivors'] += 1
                    for z in added: st.add(z, False, -1)
                xcomplete(st, X, hX - c, 4 - (hX - c), hc, lc, hX, lambda m: True, leaf, loc)
                print(key, dict(sorted(loc.items())), '%.1fs' % (time.time() - t0), flush=True)
                for k, v in loc.items(): tot['b%d_' % b + k] += v

# ---------------- part 2 ----------------
SB = list(itertools.permutations(range(4))); SC = list(itertools.permutations(range(4, 9)))
def perm_mask(m, p):
    r = 0
    for i in EL[m]: r |= 1 << p[i]
    return r
def stabiliser(seedmasks):
    key = sorted(seedmasks); G = []
    for a in SB:
        for bb in SC:
            p = list(a) + list(bb)
            if sorted(perm_mask(m, p) for m in seedmasks) == key: G.append(p)
    return G
def orbit_reps(cands, k, G):
    reps = []
    seen = set()
    for combo in itertools.combinations_with_replacement(cands, k):
        canon = min(tuple(sorted(perm_mask(m, p) for m in combo)) for p in G)
        if canon not in seen: seen.add(canon); reps.append(combo)
    return reps
P2SEEDS = {1: [('distinct', [7, 8]), ('doubled', [8, 8])], 2: [('one', [8])], 3: [('none', [])]}
def part2(b):
    for c in range(1, b + 1):
        for nm, miss in P2SEEDS[c]:
            key = 'b%d_c%d_%s' % (b, c, nm)
            if ONLY and ONLY not in key: continue
            loc = Counter(); t0 = time.time()
            seed = [(C, True)] * c + [(sub(e), False) for e in miss]
            hc = [m for m in M5 if m != C and (m & B) != B]
            G = stabiliser([m for m, _ in seed])
            if SYM: roots = orbit_reps(hc, b - c, G)
            else: roots = list(itertools.combinations_with_replacement(hc, b - c))
            loc['roots'] = len(roots); loc['stab'] = len(G)
            for root in roots:
                st = St(); st.add(B, False, 1)
                X = []
                ok = True
                for m, h in seed + [(H, True) for H in root]:
                    if not all(m & x for x, _ in X) or not st.ok(m, h): ok = False
                    st.add(m, h, 1); X.append((m, h))
                comp = [B] + sorted(set(FULL ^ H for H in root))
                for z in comp[1:]:
                    if not st.ok(z, False): ok = False
                    st.add(z, False, 1)
                if any(not (z1 & z2) for z1, z2 in itertools.combinations(comp, 2)): ok = False
                if any(sum(1 for m, _ in X if m & z == 0) > 3 for z in comp): ok = False
                if not ok:
                    loc['roots_dead'] += 1; continue
                lc = [m for m in M4 if m & B]
                def fy(m):
                    # adding low X mask m: compulsory Y degrees stay <= 3, d_Y(m) <= 4
                    for z in comp:
                        if z & m == 0 and sum(1 for x, _ in X if x & z == 0) + 1 > 3: return False
                    return sum(1 for z in comp if z & m == 0) <= 4
                def leaf(X):
                    if any(sum(1 for m, _ in X if m & z == 0) != 3 for z in comp): return
                    loc['Xdeg3'] += 1
                    if not xfloors(X, []): return
                    loc['Xfloor4'] += 1
                    if not xfloors(X, comp): return
                    loc['Xfloor5'] += 1
                    # optimistic capacity: degree-3 low masks meeting every compulsory mask
                    dYc = [sum(1 for z in comp if z & m == 0) for m, _ in X]
                    cand = []; capsum = 0
                    for m in M4:
                        if not all(m & z for z in comp): continue
                        if sum(1 for x, _ in X if x & m == 0) != 3: continue
                        cp = st.cap(m)
                        for j, (x, h) in enumerate(X):
                            if x & m == 0: cp = min(cp, (2 if h else 4) - dYc[j])
                        cp = max(cp, 0)
                        if cp > 0: cand.append((m, False, 3)); capsum += cp
                    need = 7 - len(comp)
                    loc['cap_%d' % min(capsum, 9)] += 1
                    if capsum >= need: loc['cap_ok'] += 1
                    Yfix = [(z, False) for z in comp]
                    if ysearch(st, X, Yfix, need, 0, cand, 3, loc): loc['Ysurvivors'] += 1
                xcomplete(st, X, 0, 5 - (b - c), [], lc, b, fy, leaf, loc)
            print(key, dict(sorted(loc.items())), '%.1fs' % (time.time() - t0), flush=True)
            for k, v in loc.items(): tot['b%d_' % b + k] += v

print('args', argv, flush=True)
for b in BS:
    (part1 if PART == 1 else part2)(b)
print('TOTAL', dict(sorted(tot.items())))
for s in survivors[:LIMIT]: print('example', s)
