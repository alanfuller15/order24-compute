#!/usr/bin/env python3
"""Independent MATH.md re-encoding. No imports of producer code; no bipartition.
135 mask membership bits, shared-element ANDs and complement-OR edge gates.
Cardinality auxiliaries use sequential counters (no producer totalizers).
"""
import itertools as it, json, pathlib, sys
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
class Encoding:
 def __init__(self,b,threshold=12,drop_m1=False):
  self.b=b; self.s=15-b; self.threshold=threshold;self.drop_m1=drop_m1
  self.pool=IDPool(); self.clauses=[];self.counts={};self.family=''
  self.m=[[self.pool.id(('m',x,i)) for i in range(9)] for x in range(15)]
  self.edge={}
  self.build()
 def add(self,c):
  self.clauses.append(c);self.counts[self.family]=self.counts.get(self.family,0)+1
 def atom(self,label): return self.pool.id(label)
 def land(self,args,label):
  z=self.atom(label)
  for a in args:self.add([-z,a])
  self.add([z]+[-a for a in args]);return z
 def atmost(self,lits,k):
  if k>=len(lits):return
  if k<0:self.add([]);return
  for c in CardEnc.atmost(lits,bound=k,vpool=self.pool,encoding=EncType.seqcounter).clauses:self.add(c)
 def atleast(self,lits,k):self.atmost([-x for x in lits],len(lits)-k)
 def exactly(self,lits,k):self.atmost(lits,k);self.atleast(lits,k)
 def lex(self,a,b,label):
  # exact prefix equality gates, unlike producer's one-direction gates
  prefix=None
  for i,(u,v) in enumerate(zip(a,b)):
   self.add(([-prefix] if prefix else [])+[-u,v])
   eq=self.atom((label,'equal',i))
   for c in [[-eq,-u,v],[-eq,u,-v],[eq,u,v],[eq,-u,-v]]:self.add(c)
   prefix=eq if prefix is None else self.land([prefix,eq],(label,'prefix',i))
 def y(self,x,z):return self.edge.get(tuple(sorted((x,z))))
 def build(self):
  m=self.m;s=self.s
  self.family='profile'
  for x in range(15):self.exactly(m[x],4 if x<s else 5)
  self.family='disjointness'
  for x,z in it.combinations(range(15),2):
   shared=[self.land([m[x][i],m[z][i]],('meet',x,z,i)) for i in range(9)]
   y=self.atom(('edge',x,z));self.edge[x,z]=y
   for t in shared:self.add([-y,-t])
   self.add([y]+shared)
   if x>=s:self.add([-y])
  self.family='symmetry'
  for i in range(8):self.lex([m[x][i] for x in range(15)],[m[x][i+1] for x in range(15)],('row',i))
  for x in range(14):
   if x+1!=s:self.lex(m[x],m[x+1],('column',x))
  for i in range(9):self.add([m[0][i] if i>=5 else -m[0][i]])
  self.family='degree'
  for i in range(9):self.atmost([m[x][i] for x in range(15)],8)
  for x in range(15):self.atmost([self.y(x,z) for z in range(15) if x!=z],4 if x<s else 2)
  self.family='maximality'
  for x in range(15):
   for i in range(9):
    cover=[self.land([self.y(x,z),m[z][i]],('cover',x,z,i)) for z in range(15) if z!=x]
    self.add([m[x][i]]+cover)
  for i,j in it.combinations(range(9),2):
   pairs=[self.land([m[x][i],m[x][j]],('pair',x,i,j)) for x in range(15)]
   self.add(pairs)
   if not self.drop_m1:self.atmost(pairs[:s],3)
  self.family='multiplicity'
  # Ordered columns imply three equal low masks occur consecutively.
  for x in range(s-2):
   different=[]
   for i in range(9):
    u,v=m[x][i],m[x+2][i];d=self.atom(('diff',x,i));different.append(d)
    for c in [[-d,u,v],[-d,-u,-v],[d,-u,v],[d,u,-v]]:self.add(c)
   self.add(different)
  self.family='floors'
  if self.threshold>=12:
   self.atleast(list(self.edge.values()),20)
   self.atleast([y for (x,z),y in self.edge.items() if z<s],[20,18,16,14][self.b])
  self.family='outside12'
  for subset in it.combinations(range(15),12):self.atleast([self.y(x,z) for x,z in it.combinations(subset,2)],self.threshold)
 def write(self,path):
  with pathlib.Path(path).open('w') as f:
   f.write(f'p cnf {self.pool.top} {len(self.clauses)}\n')
   for c in self.clauses:f.write(' '.join(map(str,c))+' 0\n')
if __name__=='__main__':
 e=Encoding(int(sys.argv[1]),int(sys.argv[3]) if len(sys.argv)>3 else 12,'--drop-m1' in sys.argv);e.write(sys.argv[2]);print(json.dumps({'b':e.b,'threshold':e.threshold,'drop_m1':e.drop_m1,'vars':e.pool.top,'clauses':len(e.clauses),'families':e.counts}))
