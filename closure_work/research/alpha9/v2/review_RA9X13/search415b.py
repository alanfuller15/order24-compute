#!/usr/bin/env python3
"""RA9X13 second (bit-mask) implementation of the 1.3 search, with NO seed symmetry reduction option:
   --allseeds : enumerate every admissible multiset of 3 neighbour masks inside C (not just D, R reps)
   --seed D|R : only that representative.  Other options as search415.py (--q, --mult, --rmax, --nofloor,
   --ycount, --ydeg).  --exacty : instead of capacity relaxation, exactly test whether 7 Y masks exist
   (pairwise intersecting, each with exactly YDEG disjoint X masks, global mult/q/r bounds, Y contains B).
Std-lib only."""
import sys, itertools
from collections import Counter
a = sys.argv[1:]
def opt(n, d, t=int): return t(a[a.index(n)+1]) if n in a else d
QMAX=opt('--q',3); MMAX=opt('--mult',2); RMAX=opt('--rmax',8); YNEED=opt('--ycount',7); YDEG=opt('--ydeg',3)
FLOOR='--nofloor' not in a; EXACTY='--exacty' in a
M=[sum(1<<i for i in c) for c in itertools.combinations(range(9),4)]
PAIRS=list(itertools.combinations(range(9),2)); PI={p:k for k,p in enumerate(PAIRS)}
EL={m:[i for i in range(9) if m>>i&1] for m in M}
PR={m:[PI[p] for p in itertools.combinations(EL[m],2)] for m in M}
Bm=0b1111; Cm=0b111110000
subC=[m for m in M if m & Bm==0]
def seeds():
    if '--allseeds' in a:
        return [('all',s) for s in itertools.combinations_with_replacement(sorted(subC),3)]
    D=[Cm&~(1<<4),Cm&~(1<<5),Cm&~(1<<6)]; R=[Cm&~(1<<4),Cm&~(1<<4),Cm&~(1<<5)]
    s=opt('--seed',None,str)
    out=[('D',D),('R',R)]
    return [o for o in out if s is None or o[0]==s]
def main():
    tot=Counter()
    for name,seed in seeds():
        r=[0]*9; q=[0]*36; mu=Counter()
        def ok(m):
            return mu[m]<MMAX and all(r[i]<RMAX for i in EL[m]) and all(q[k]<QMAX for k in PR[m])
        def add(m,s):
            for i in EL[m]: r[i]+=s
            for k in PR[m]: q[k]+=s
            mu[m]+=s
        good=True
        for s in seed:
            if not ok(s): good=False; break
            add(s,1)
        if not good: tot['seed_rejected']+=1; continue
        tot['seeds']+=1
        cands=[m for m in M if m&Bm and all(m&s for s in seed)]
        X=list(seed)
        def leaf():
            tot['leaves']+=1
            if FLOOR and sum(sorted(r)[:4])<12: return
            tot['floor_pass']+=1
            types=[]
            for D in M:
                if sum(1 for x in X if x&D==0)!=YDEG: continue
                cap=min([MMAX-mu[D]]+[RMAX-r[i] for i in EL[D]]+[QMAX-q[k] for k in PR[D]])
                if cap>0: types.append((D,cap))
            capsum=sum(c for _,c in types)
            tot['cap_%d'%capsum]+=1
            if capsum>=YNEED:
                tot['relax_survivors']+=1
                if EXACTY and exact(types): tot['exact_survivors']+=1
        def exact(types):
            # choose YNEED masks (multiset) from types, containing Bm, pairwise intersecting, global bounds
            T=[D for D,_ in types]
            if Bm not in T: return False
            Y=[]
            def ok2(D): return ok(D) and all(D&z for z in Y)
            def rec2(j,k):
                if k==0: return True
                for jj in range(j,len(T)):
                    D=T[jj]
                    if ok2(D):
                        add(D,1); Y.append(D)
                        f=rec2(jj,k-1)
                        Y.pop(); add(D,-1)
                        if f: return True
                return False
            if not ok(Bm): return False
            add(Bm,1); Y.append(Bm); f=rec2(0,YNEED-1); Y.pop(); add(Bm,-1)
            return f
        def rec(j,k):
            tot['nodes']+=1
            if k==0: leaf(); return
            for jj in range(j,len(cands)):
                m=cands[jj]
                if all(m&x for x in X) and ok(m):
                    add(m,1); X.append(m); rec(jj,k-1); X.pop(); add(m,-1)
        rec(0,5)
        if name!='all': print(name, dict(sorted(tot.items()))); tot=Counter()
    if '--allseeds' in a: print('allseeds', dict(sorted(tot.items())))
main()
