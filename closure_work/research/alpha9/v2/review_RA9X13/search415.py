#!/usr/bin/env python3
"""RA9X13 independent re-implementation of round-10 claim 1.3 (Case B, 4^15, 8+7 split).
Standard library only. Written from the mathematical statement, not from ChatGPT's code.

Setting: X = 8-class (independent), Y = 7-class (independent); all masks 4-subsets of I={0..8};
adjacency iff masks disjoint (Theorem 1). Facts used (all proved upstream):
  mult(mask) <= 2 over O (N3, b=0); q_ij <= 3 over O (M1); r_i <= 8 (deg(i) <= 8, Case B);
  X masks pairwise intersect (X independent); every Y vertex has exactly 3 neighbours, all in X (1.2);
  12-set (I\\C) u X, |C|=5: sum_{i in C} r_i(X) <= 20  <=> four smallest r_i(X) sum >= 12.
y in Y fixed with mask B={0,1,2,3}; its 3 X-neighbours have masks inside C={4..8}; the other 5 X masks meet B.
Options (argv): --q Q  (pair bound, default 3), --mult M (default 2), --nofloor, --nomeetB, --rmax R (default 8),
  --ycount K (Y vertices needed, default 7), --ydeg d (required X-degree of Y masks, default 3)
"""
import sys, itertools
args = sys.argv[1:]
def opt(name, default, typ=int):
    if name in args: return typ(args[args.index(name)+1])
    return default
QMAX = opt('--q', 3); MMAX = opt('--mult', 2); RMAX = opt('--rmax', 8)
YNEED = opt('--ycount', 7); YDEG = opt('--ydeg', 3)
FLOOR = '--nofloor' not in args; MEETB = '--nomeetB' not in args
EXACTY = '--exacty' in args   # optional: exact Y completion (pairwise intersecting Y masks etc.)

I = range(9)
MASKS = [frozenset(c) for c in itertools.combinations(I, 4)]
IDX = {m: k for k, m in enumerate(MASKS)}
PAIRS = list(itertools.combinations(I, 2))
B = frozenset({0,1,2,3}); C = frozenset({4,5,6,7,8})
def Cm(e): return C - {e}
SEEDS = {'D': [Cm(4), Cm(5), Cm(6)], 'R': [Cm(4), Cm(4), Cm(5)]}

def run(seedname):
    seed = SEEDS[seedname]
    # candidate remaining masks: meet B (non-neighbours of y), intersect every seed mask
    cands = [m for m in MASKS if (not MEETB or (m & B)) and all(m & s for s in seed)]
    if not MEETB:
        # without meet-B the remaining masks could be disjoint from B; still must intersect seeds
        pass
    stats = dict(nodes=0, leaves=0, floor_pass=0, survivors=0, maxcap=0, cand_types=set(), capdist={})
    r = [0]*9; q = {p: 0 for p in PAIRS}; mult = {}
    def add(m, s):
        for i in m: r[i] += s
        for p in itertools.combinations(sorted(m), 2): q[p] += s
        mult[m] = mult.get(m, 0) + s
    def ok(m):
        if mult.get(m, 0) + 1 > MMAX: return False
        if any(r[i] + 1 > RMAX for i in m): return False
        if any(q[p] + 1 > QMAX for p in itertools.combinations(sorted(m), 2)): return False
        return True
    for s in seed:
        assert ok(s); add(s, 1)
    X = list(seed)
    survivors = []
    def leaf():
        stats['leaves'] += 1
        if FLOOR and sum(sorted(r)[:4]) < 12: return
        stats['floor_pass'] += 1
        total = 0; types = []
        for D in MASKS:
            deg = sum(1 for x in X if not (x & D))
            if deg != YDEG: continue
            cap = MMAX - mult.get(D, 0)
            for i in D: cap = min(cap, RMAX - r[i])
            for p in itertools.combinations(sorted(D), 2): cap = min(cap, QMAX - q[p])
            if cap > 0:
                stats['cand_types'].add(D); types.append((D, cap)); total += cap
        stats['maxcap'] = max(stats['maxcap'], total)
        stats['capdist'][total] = stats['capdist'].get(total, 0) + 1
        if total >= YNEED:
            stats['survivors'] += 1
            if len(survivors) < 5: survivors.append((list(map(sorted, X)), [(sorted(D), c) for D, c in types]))
    def rec(start, k):
        stats['nodes'] += 1
        if k == 0: leaf(); return
        for j in range(start, len(cands)):
            m = cands[j]
            if not all(m & x for x in X): continue
            if not ok(m): continue
            add(m, 1); X.append(m)
            rec(j, k-1)   # nondecreasing index: multisets
            X.pop(); add(m, -1)
    rec(0, 5)
    return stats, survivors

if __name__ == '__main__':
    print('options', dict(QMAX=QMAX, MMAX=MMAX, RMAX=RMAX, FLOOR=FLOOR, MEETB=MEETB, YNEED=YNEED, YDEG=YDEG))
    tot = 0
    for sn in ('D', 'R'):
        st, sv = run(sn)
        tot += st['survivors']
        print(f"seed {sn}: nodes {st['nodes']} leaves {st['leaves']} floor_pass {st['floor_pass']} "
              f"candidate_types {len(st['cand_types'])} max_capacity {st['maxcap']} survivors {st['survivors']}")
        print('   capacity distribution', dict(sorted(st['capdist'].items())))
        for s in sv[:2]: print('   example survivor', s)
    print('TOTAL survivors', tot)
