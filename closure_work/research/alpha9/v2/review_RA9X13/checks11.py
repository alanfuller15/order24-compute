#!/usr/bin/env python3
"""RA9X13 finite sanity checks for the hand steps of 1.1 / 1.2 / the floor (std-lib)."""
import itertools
I=range(9); B=frozenset({0,1,2,3}); C=frozenset({4,5,6,7,8})
M=[frozenset(c) for c in itertools.combinations(I,4)]
def qok(fam,Q=3,mult=2):
    from collections import Counter
    if max(Counter(fam).values())>mult: return False
    for p in itertools.combinations(I,2):
        if sum(1 for m in fam if set(p)<=m)>Q: return False
    return True
subC=[m for m in M if m<=C]
# (a) four neighbour masks of a degree-4 y: multisets of 4 four-subsets of C, q<=3, mult<=2
fams=[f for f in itertools.combinations_with_replacement(subC,4) if qok(list(f))]
print('(a) admissible 4-multisets inside C:',len(fams),'all distinct:',all(len(set(f))==4 for f in fams),
      'common element sizes:',sorted({len(frozenset.intersection(*f)) for f in fams}))
# (b) other X masks: meet every neighbour mask, total |M cap C| over 4 others <=4 -> each exactly {c}
f=(C-{4},C-{5},C-{6},C-{7}); c=8
meet=[m for m in M if all(m&x for x in f)]
print('(b) masks meeting all four with |m cap C|=1:',sorted(map(sorted,[m for m in meet if len(m&C)==1])))
print('    min |m cap C| among masks meeting all four:',min(len(m&C) for m in meet))
# (c) 4 masks {c}+3-subset of B with q_{cb}<=3 (with the four C-masks, all containing c) -> all distinct
G2=[m for m in M if len(m&C)==1 and c in m]
ok=[g for g in itertools.combinations_with_replacement(G2,4) if qok(list(f)+list(g))]
print('(c) admissible completions:',len(ok),[sorted(map(sorted,g)) for g in ok])
X=list(f)+list(ok[0])
print('    r_c(X)=',sum(1 for m in X if c in m))
degs={}
for D in M:
    if c in D: continue
    d=sum(1 for x in X if not (x&D))
    degs.setdefault(d,[]).append(D)
print('(d) Y-mask degree classes (masks avoiding c):',{d:len(v) for d,v in sorted(degs.items())},
      'degree>=3:',[sorted(D) for d in degs if d>=3 for D in degs[d]])
for D in [B,C-{c}]:
    print('    max extra copies of',sorted(D),'in Y:',min(3-sum(1 for m in X if set(p)<=m) for p in itertools.combinations(sorted(D),2)) - (1 if D==B else 0),'(B count excludes y itself)')
# (e) floor equivalence: sum of 5 largest <=20 <=> 4 smallest >=12 when total 32 (trivial) ; 1.2 averaging trivial
print('(e) floor: 32 - 20 = 12 OK')
