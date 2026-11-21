#!/usr/bin/env python3
"""RA9X16: completeness of seed patterns (part 1: 4-c low 4-subsets of C; part 2: 3-c) up to S_5(C), with the
caps MULT <= 2 and q4 <= 3 (q4 counted over the seed and y's mask B, which contains no pair of C), and orbit counts
of the extra high masks (5-sets != C, not containing B) under the stabiliser of each part-2 seed in S_4(B) x S_5(C).
Also: c = 3 (b = 3) low masks with exactly one element in C form one orbit under S_4(B) x S_5(C)."""
import itertools
C = list(range(4, 9)); B = list(range(4))
def msk(s): return sum(1 << i for i in s)
subs = [msk([x for x in C if x != e]) for e in C]
def q4ok(ms):
    for p in itertools.combinations(range(9), 2):
        if sum(1 for m in ms if all(m >> i & 1 for i in p)) > 3: return False
    return True
def canonS5(ms):
    best = None
    for p in itertools.permutations(C):
        mp = {C[k]: p[k] for k in range(5)}
        t = tuple(sorted(sum(1 << mp.get(i, i) for i in range(9) if m >> i & 1) for m in ms))
        best = t if best is None or t < best else best
    return best
for k in range(0, 5):
    orbs = set()
    for ms in itertools.combinations_with_replacement(subs, k):
        if any(ms.count(m) > 2 for m in ms): continue
        if not q4ok(ms): continue
        orbs.add(canonS5(ms))
    print('k=%d low 4-subsets of C: %d orbits:' % (k, len(orbs)),
          [[sorted(set(C) - {i for i in range(9) if m >> i & 1}) for m in o] for o in sorted(orbs)])
# extra high masks orbits
SB = list(itertools.permutations(B)); SC = list(itertools.permutations(C))
def pm(m, p): return sum(1 << p[i] for i in range(9) if m >> i & 1)
Cm = msk(C); Bm = msk(B)
hc = [m for m in range(512) if bin(m).count('1') == 5 and m != Cm and (m & Bm) != Bm]
def stab(seed):
    G = []
    for a in SB:
        for b in SC:
            p = list(a) + list(b)
            if sorted(pm(m, p) for m in seed) == sorted(seed): G.append(p)
    return G
seeds = {'c1 distinct': [Cm, subs[3], subs[4]], 'c1 doubled': [Cm, subs[4], subs[4]], 'c2': [Cm, Cm, subs[4]],
         'c3': [Cm, Cm, Cm]}
print('extra high candidates:', len(hc))
for nm, seed in seeds.items():
    G = stab(seed)
    for k in (1, 2):
        orbs = set(); n = 0
        for combo in itertools.combinations_with_replacement(hc, k):
            n += 1
            orbs.add(min(tuple(sorted(pm(m, p) for m in combo)) for p in G))
        print('%s |stab| = %d, %d extra high masks: %d multisets, %d orbits' % (nm, len(G), k, n, len(orbs)))
one = [m for m in range(512) if bin(m).count('1') == 4 and bin(m & Cm).count('1') == 1]
G = stab([Cm])
print('c3: masks with |M n C| = 1:', len(one), 'orbits:', len({min(pm(m, p) for p in G) for m in one}),
      'contains {0,1,2,4}:', msk([0, 1, 2, 4]) in one)
