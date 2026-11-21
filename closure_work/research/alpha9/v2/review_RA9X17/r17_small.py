#!/usr/bin/env python3
"""RA9X17 independent small checks for MATH.md 4j (std-lib, frozenset based, written from the text)."""
from itertools import combinations, combinations_with_replacement, permutations
I=range(9); B=frozenset(range(4)); C=frozenset(range(4,9))
M4=[frozenset(c) for c in combinations(I,4)]
# 4j.3(b)/(c): candidate X masks for seeds D, R
D=[C-{4},C-{5},C-{6}]; R=[C-{4},C-{4},C-{5}]
for nm,s in (('D',D),('R',R)):
    print('4j.3 cand',nm,sum(1 for m in M4 if m&B and all(m&x for x in s)))
# orbits of 3-multisets of 4-subsets of C under S5 (mult<=2)
sub=[C-{p} for p in C]
def orbits(k):
    ms=[t for t in combinations_with_replacement(sorted(C),k) if max(t.count(e) for e in t)<=2] if k else [()]
    seen=set(); res=[]
    for t in ms:
        if t in seen: continue
        orb=set()
        for p in permutations(sorted(C)):
            mp=dict(zip(sorted(C),p)); orb.add(tuple(sorted(mp[e] for e in t)))
        seen|=orb; res.append((t,len(orb)))
    return len(ms),res
for k in (2,3): print('omitted-element multisets k=%d'%k, orbits(k))
# 4j.2: windmill X, degrees, multiplicities
c=8; Co=C-{c}
X=[C-{p} for p in Co]+[frozenset({c})|(B-{j}) for j in B]
assert all(a&b for a in X for b in X)
r=[sum(i in x for x in X) for i in I]; print('windmill r',r)
deg={}
for m in M4:
    if c in m: continue
    deg.setdefault(sum(1 for x in X if not m&x),[]).append(m)
print('4j.2(d) degrees',{d:len(v) for d,v in sorted(deg.items())}, [sorted(m) for m in deg[4]])
def q(fam,pair): return sum(1 for x in fam if pair<=x)
print('max q over pairs in B, X+w:',max(q(X+[B],frozenset(p)) for p in combinations(B,2)),
      ' pairs in Co, X:',[q(X,frozenset(p)) for p in combinations(Co,2)])
# uniqueness of windmill: enumerate 4 extra masks with |m&C|=1 meeting all four C-{p}, with M1 (q<=3 incl. w=B), N3
four=[C-{p} for p in Co]
ex=[m for m in M4 if len(m&C)==1 and all(m&f for f in four)]
sols=[s for s in combinations_with_replacement(ex,4) if all(a&b for a in s for b in s)
      and max(s.count(m) for m in s)<=2 and all(q(list(s)+four+[B],frozenset(p))<=3 for p in combinations(I,2))]
print('4j.2(c) completions',len(sols))
# 4j.2(a): non-distinct 4-multisets of 4-subsets of a 5-set all violate N3 or M1
bad=0
for s in combinations_with_replacement(sub,4):
    if len(set(s))==4: continue
    if max(s.count(m) for m in s)>=3: continue
    if all(q(list(s),frozenset(p))<=3 for p in combinations(C,2)): bad+=1
print('4j.2(a) non-distinct admissible',bad)
