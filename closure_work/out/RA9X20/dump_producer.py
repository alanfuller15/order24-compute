#!/usr/bin/env python3
"""Capture the unmodified producer's static CNF, before any solving/lazy steps."""
import sys, runpy, pathlib, hashlib, json
import pysat.solvers
class DumpDone(Exception): pass
b=int(sys.argv[1]); dest=pathlib.Path(sys.argv[2]); source=pathlib.Path(__file__).resolve().parents[2]/'research/alpha9/v2/exp_B4/model_B4.py'
# parents[2] is closure_work
class Capture:
 def __init__(self, *args, bootstrap_with, **kwargs):
  clauses=bootstrap_with; nv=max(abs(l) for c in clauses for l in c)
  with dest.open('w') as f:
   f.write(f'p cnf {nv} {len(clauses)}\n')
   for c in clauses: f.write(' '.join(map(str,c))+' 0\n')
  print(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'b':b,'vars':nv,'clauses':len(clauses),'cnf_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'argv':[str(b),'--nocore'],'bip':False}),flush=True)
  raise DumpDone
pysat.solvers.Solver=Capture
sys.argv=[str(source),str(b),'--nocore']
try: runpy.run_path(str(source),run_name='__main__')
except DumpDone: pass
