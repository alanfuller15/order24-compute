#!/usr/bin/env python3
"""Check the seed reduction: multisets of k 4-subsets of C={4..8} (mult <= 2), k=0..3, admissible for q4 <= 3
(pairs counted over the k masks; y = B is disjoint from C so adds nothing), up to S_5 on C.
Also checks: the C-budget forces k <= 3, and every orbit is represented by the seeds used in b17.py."""
import itertools
C = [4, 5, 6, 7, 8]
seeds = {0: [()], 1: [(8,)], 2: [(7, 8), (8, 8)], 3: [(6, 7, 8), (7, 8, 8)]}
def masks(miss): return [frozenset(set(C) - {e}) for e in miss]
def admissible(miss):
    ms = masks(miss)
    from collections import Counter
    if any(v > 2 for v in Counter(ms).values()): return False
    q = Counter(p for m in ms for p in itertools.combinations(sorted(m), 2))
    return all(v <= 3 for v in q.values())
def canon(miss):
    return min(tuple(sorted(p[C.index(e)] for e in miss)) for p in itertools.permutations(C))
for k in range(0, 6):
    allms = [m for m in itertools.combinations_with_replacement(C, k) if admissible(m)]
    orbs = sorted({canon(m) for m in allms})
    budget = 5 + 4 * k + (7 - k) <= 21
    rep = sorted(canon(s) for s in seeds.get(k, []))
    print('k=%d admissible multisets %d orbits %s budget_ok %s seeds %s match %s' %
          (k, len(allms), orbs, budget, rep, orbs == rep if budget else (rep == [])))
