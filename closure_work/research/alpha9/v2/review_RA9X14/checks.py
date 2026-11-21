# RA9X14 standard-library checks for MATH.md section 4i
from itertools import combinations, product, combinations_with_replacement as cwr
I=range(9); M=[frozenset(c) for c in combinations(I,4)]
ok=True
def rep(name,cond):
    global ok; ok&=bool(cond); print(("OK  " if cond else "FAIL"),name)
def q4ok(fam):
    for p in combinations(I,2):
        if sum(1 for a in fam if set(p)<=a)>3: return False
    return True
A0=frozenset({0,1,2,3}); C0=frozenset(I)-A0
sub=[frozenset(c) for c in combinations(sorted(C0),4)]
# (L1) k=4,5 low nbrs: q4-admissible multisets (incl. x itself and with x's copies irrelevant) distinct
for k in (4,5):
    bad=[ms for ms in cwr(sub,k) if q4ok(list(ms)) and len(set(ms))<k]
    rep(f"(L1) k={k}: admissible multisets of {k} 4-subsets of C are sets",not bad)
# (L1) also with x itself in the family
for k in (4,5):
    bad=[ms for ms in cwr(sub,k) if q4ok(list(ms)+[A0]) and len(set(ms))<k]
    rep(f"(L1) k={k} with A in family",not bad)
# (L2)
rep("(L2) <=1 4-set disjoint from two distinct 4-sets", max(sum(1 for c in M if not (c&a) and not (c&b)) for a,b in combinations(M,2))<=1)
# (L3) general: x type A has >=4 low nbrs (distinct 4-subsets of C, any admissible), x' type B shares 2 of them -> B=A
bad=0
for k in (4,5):
  for S in combinations(sub,k):
    if not q4ok(list(S)+[A0]): continue
    for B in M:
        if B!=A0 and sum(1 for s in S if not (s&B))>=2: bad+=1
rep("(L3) no B != A disjoint from 2 nbr types of a dense star",bad==0)
# (L4)
bad=0; badd=0
for a,b in combinations(M,2):
    for ma in (1,2,3):
        for mb in (1,2,3):
            if ma+mb<4: continue
            if not q4ok([a]*ma+[b]*mb): continue
            if a&b and len(a&b)!=1: bad+=1
            if not (a&b): continue  # disjoint types adjacent: excluded by independence of X
            if any(not(c&a) and not(c&b) for c in M): badd+=1
rep("(L4) |A&B|>=2 impossible under q4<=3 when mu sum>=4",bad==0)
rep("(L4) |A&B|=1 -> no 4-set disjoint from both",badd==0)
# (L5)
rep("(L5)", all(len(a&b)>=3 for a,b in combinations(M,2) for c in M if not(a&c) and not(b&c)))
# m=5 (II): two distinct types A,B both disjoint from one 4-set, total copies>=4 -> violates q4
bad=[(a,b) for a,b in combinations(M,2) if any(not(a&c) and not(b&c) for c in M) and
     any(q4ok([a]*ma+[b]*mb) for ma in (1,2,3) for mb in (1,2,3) if ma+mb>=4)]
rep("m=5(II): no admissible A,B (mult sum>=4) with a common disjoint 4-set",not bad)
# (f): degree sequences of X, entries 0..5, every triple sum >= 12
seqs=[s for s in product(range(6),repeat=6) if all(sum(t)>=12 for t in combinations(s,3))]
rep("(f1) min deg >= 2", all(min(s)>=2 for s in seqs))
rep("(f2) <=1 entry <=3", all(sum(1 for d in s if d<=3)<=1 for s in seqs))
rep("(f3a) one <=3 -> >=4 fives", all(sum(1 for d in s if d==5)>=4 for s in seqs if min(s)<=3))
rep("(f3b) one <=2 -> five fives", all(sum(1 for d in s if d==5)>=5 for s in seqs if min(s)<=2))
rep("(b) sum >= 24", all(sum(s)>=24 for s in seqs))
# (f4): highs deg<=3 -> at most one in X: immediate from (f2)
# capacities
rep("m=2 r=3: 5*4+2+1=23<24", 5*4+2+1==23)
rep("m=3 (i): 6+3a<=15 for a<=3, +9 =24", max(6+3*a for a in (1,2,3))+9==24)
rep("m=3 (i) two tripled: 3*4=12<15", 12<15)
rep("m=4 (I): 3*5=15, need 9 from 4 highs, 4*2=8", 24-15==9 and 4*2==8)
rep("m=5 (I): cap 25; highs>=14; 3*3+2*2=13", 5*3+2*5==25 and 24-2*5==14 and 3*3+2*2==13)
rep("m=5 (I) two tripled: 15+6=21", 5*3+2*3==21)
rep("m=6 (I): 23", 6*3+5==23)
rep("m=6 (II): 27>25", 2+25>2*5+5*3)
# m=3 (ii): types with total copies>=5, each <=3, count 2 or 3 -> two largest >=4
bad=[t for k in (2,3) for t in product((1,2,3),repeat=k) if sum(t)>=5 and sum(sorted(t)[-2:])<4]
rep("m=3 (ii) two largest multiplicities sum >= 4",not bad)
# composition counts
for m in range(1,7):
    s=13-m
    rep(f"m={m}: (I) lY={7-m}, (II) lY={8-m}", s-6==7-m and s-5==8-m)
# 4h.5 scope: 15-m>=13 iff m<=2
rep("4h.5 scope", all((15-m>=13)==(m<=2) for m in range(7)))
print("ALL OK" if ok else "SOME FAIL")
