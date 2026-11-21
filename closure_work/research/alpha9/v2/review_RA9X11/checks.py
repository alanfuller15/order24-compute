# RA9X11 independent checks for MATH.md section 4h (standard library only)
from itertools import combinations, combinations_with_replacement as cwr
from fractions import Fraction as Fr
from math import ceil
ok=True
def chk(c,msg):
    global ok
    print(("OK  " if c else "FAIL"),msg); ok&=bool(c)
I=range(9)
def q4ok(fam):
    for p in combinations(I,2):
        if sum(1 for m in fam if set(p)<=m)>3: return False
    return True
# profiles on the list
prof={84:(14,0,1),85:(13,1,1),87:(12,2,1),90:(11,3,1),94:(10,4,1),98:(9,5,1),101:(8,6,1),104:(7,7,1),
      86:(13,0,2),88:(12,1,2),91:(11,2,2),95:(10,3,2),99:(9,4,2),102:(8,5,2),105:(7,6,2)}
chk(all(s+m+t==15 and m+t<=8 for s,m,t in prof.values()),"15 profiles: s+m+t=15, |H|<=8")
# 4h.1 count: (s-4)+m+t = 11
chk(all((s-4)+m+t==11 for s,m,t in prof.values()),"4h.1 independent set size 11 for all 15")
# 4h.2 (iii) averaging
for t,need in ((1,20),(2,21)):
    n=15-t;k=12-t; b=Fr(12*n*(n-1),k*(k-1))
    chk(ceil(b)==need,f"4h.2(iii) t={t}: bound {b} = {float(b):.3f}, ceil {ceil(b)}")
# bound table
for (s,m,t) in sorted(prof.values(),key=lambda x:(-x[2],x[1])):
    need=20 if t==1 else 21
    if s<9: print(f"     t={t} m={m} s={s}<9: no odd cycle"); continue
    r=s-9; B=9+r*r//4+m*max(1,r)
    chk(B<need,f"4h.2 table t={t} m={m} r={r}: 9+{r*r//4}+{m*max(1,r)}={B} < {need}")
# 4h.3 averaging
chk(Fr(12*20,10)==24 and sum(1 for U in combinations(range(6),3) if 0 in U)==10,"4h.3: 20 triples, each x in 10, 240/10=24")
# 4h.4 / 4h.6(a): multisets of 5 / 4 four-subsets of a 5-set C with q4<=3
C=frozenset(range(5)); A=frozenset(range(5,9))
subs=[frozenset(c) for c in combinations(C,4)]
ms5=[f for f in cwr(subs,5) if q4ok(f)]
chk(len(list(cwr(subs,5)))==126 and len(ms5)==1 and len(set(ms5[0]))==5,"4h.4: of 126 five-multisets only the 5 distinct subsets pass")
ms4=[f for f in cwr(subs,4) if q4ok(f)]
chk(len(list(cwr(subs,4)))==70 and len(ms4)==5 and all(len(set(f))==4 for f in ms4),"4h.6(a): of 70 four-multisets 5 pass, all distinct")
allm=[frozenset(c) for c in combinations(I,4)]
add=[B for B in allm if q4ok(subs+[B])]
chk(len(add)==21 and all(len(B&C)<=1 for B in add) and all(B&B2 for B,B2 in combinations(add,2)) and all(len(B&A)>=3 for B in add),
    "4h.4: 21 addable masks, |B∩C|<=1, pairwise meeting")
# 4h.6(b): B != A disjoint from <=1 of any 4 distinct 4-subsets of C (actually of all 5)
chk(all(sum(1 for y in subs if not (B&y))<=1 for B in allm if B!=A) and all(not(A&y) for y in subs),
    "4h.6(b): mask != A disjoint from <= 1 four-subset of C")
# 4h.6(c): two distinct masks have <= 1 common disjoint 4-mask
chk(all(sum(1 for W in allm if not(W&(B|B2)))<=1 for B,B2 in combinations(allm,2)),"4h.6(c): distinct B,B'' have <=1 common disjoint 4-set")
# 4h.5: masks addable to a tripled mask
T=[A,A,A]; add3=[B for B in allm if q4ok(T+[B])]
chk(len(add3)==45 and all(len(B&A)<=1 for B in add3) and all(B&B2 for B,B2 in combinations(add3,2)),"4h.5: 45 addable masks, |B∩A|<=1, pairwise meeting")
# 4h.5 scope: s+t>=13 iff m<=2
sc=sorted(k for k,(s,m,t) in prof.items() if s+t>=13)
chk(sc==[84,85,86,87,88,91],f"4h.5 scope (s+t>=13): {sc}")
print("     s-3+t for others:",{k:s-3+t for k,(s,m,t) in prof.items() if s+t<13})
# 4h.4 consequence: s-5+t
print("     s-5+t:",{k:s-5+t for k,(s,m,t) in prof.items()})
chk(prof[86][0]-5+prof[86][2]==10 and prof[84][0]-5+prof[84][2]==10,"4h.4: 86 and 84 give 10")
# Kneser K(9,4) odd girth = 9 (BFS on odd cycles via bipartite double cover)
idx={m:i for i,m in enumerate(allm)}
adj=[[idx[b] for b in allm if not(a&b)] for a in allm]
from collections import deque
def oddgirth():
    best=99
    for s in range(len(allm)):
        dist={(s,0):0};dq=deque([(s,0)])
        while dq:
            v,p=dq.popleft()
            for w in adj[v]:
                if (w,1-p) not in dist: dist[(w,1-p)]=dist[(v,p)]+1;dq.append((w,1-p))
        best=min(best,dist.get((s,1),99))
    return best
chk(oddgirth()==9,"4b.11: shortest odd closed walk in K(9,4) has length 9")
# ledger
openA=sorted(set(prof)-{86})
chk(openA==[84,85,87,88,90,91,94,95,98,99,101,102,104,105],f"ledger Case A open {len(openA)}: {openA}")
print("ALL OK" if ok else "SOME FAIL")
