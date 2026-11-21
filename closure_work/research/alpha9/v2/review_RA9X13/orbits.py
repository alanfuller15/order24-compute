#!/usr/bin/env python3
"""Seed orbit check: admissible multisets of 3 four-subsets of C={4..8} (mult<=2, q<=3) under S_5 on C."""
import itertools
C=(4,5,6,7,8); subC=[frozenset(c) for c in itertools.combinations(C,4)]
def adm(f):
    if max(f.count(m) for m in f)>2: return False
    return all(sum(1 for m in f if set(p)<=m)<=3 for p in itertools.combinations(C,2))
seeds=[f for f in itertools.combinations_with_replacement(subC,3) if adm(list(f))]
def canon(f):
    best=None
    for p in itertools.permutations(C):
        mp=dict(zip(C,p)); g=tuple(sorted(tuple(sorted(mp[i] for i in m)) for m in f))
        best=g if best is None or g<best else best
    return best
orb={}
for f in seeds: orb.setdefault(canon(f),[]).append(f)
print('admissible seeds',len(seeds),'(of 35; tripled ones rejected:',35-len(seeds),') orbits',len(orb))
for k,v in orb.items(): print('  orbit rep',k,'size',len(v))
