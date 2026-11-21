#!/usr/bin/env python3
"""Exhaustive gate/counter sanity checks independent of UNSAT outcomes."""
import itertools,json
from independent import Encoding
from pysat.formula import IDPool
from pysat.solvers import Solver
checks=0
# Exercise encoder primitives without constructing a profile.
def fresh(n):
 e=Encoding.__new__(Encoding);e.pool=IDPool();e.clauses=[];e.counts={};e.family='test'
 return e,[e.atom(('input',i)) for i in range(n)]
for n in range(1,8):
 for bound in range(n+1):
  e,x=fresh(n);e.atmost(x,bound)
  with Solver(name='cadical153',bootstrap_with=e.clauses) as s:
   for bits in itertools.product([False,True],repeat=n):
    assert s.solve(assumptions=[a if b else -a for a,b in zip(x,bits)])==(sum(bits)<=bound)
    checks+=1
for n in range(1,5):
 e,x=fresh(2*n);e.lex(x[:n],x[n:],'testlex')
 with Solver(name='cadical153',bootstrap_with=e.clauses) as s:
  for bits in itertools.product([False,True],repeat=2*n):
   assert s.solve(assumptions=[a if b else -a for a,b in zip(x,bits)])==(bits[:n]<=bits[n:]);checks+=1
# AND gate exactness, including signed literals.
for signs in itertools.product([-1,1],repeat=3):
 e,x=fresh(3);z=e.land([a*b for a,b in zip(x,signs)],'and')
 with Solver(name='cadical153',bootstrap_with=e.clauses) as s:
  for bits in itertools.product([False,True],repeat=3):
   intended=all(b==(sign==1) for b,sign in zip(bits,signs));ass=[a if b else -a for a,b in zip(x,bits)]
   assert s.solve(assumptions=ass+[z if intended else -z]);assert not s.solve(assumptions=ass+[-z if intended else z]);checks+=2
print(json.dumps({'status':'PASS','assignments_checked':checks,'scope':['seqcounter atmost n<=7','lex length<=4','signed AND3']}))
