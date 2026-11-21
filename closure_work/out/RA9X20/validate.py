#!/usr/bin/env python3
"""Check retained compressed DIMACS against recorded uncompressed certificate inputs."""
import pathlib,json,lzma,hashlib
ROOT=pathlib.Path(__file__).resolve().parent
rows=[]
for b in range(4):
 for kind in ('producer','independent'):
  name=f'{kind}_B{16+b}';record=json.loads((ROOT/'logs'/(name+'.json')).read_text())
  assert record['verified'] and record['solver_exit']==20 and record['cake_exit']==0 and record['cake_stdout']=='s VERIFIED UNSAT\n'
  assert record['cake_lpr_sha256']=='29e02af756c1f0fc4ccac78e9a908e0d8ef01201786f257f1b27b26603390798'
  assert record['cadical_sha256']=='eae671d6fab57f7bf909e621adee2a2bd550a0ae0b561065c815f599c7696fe8'
  digest=hashlib.sha256();count=0;nv=None;maxvar=0
  with lzma.open(ROOT/'cnf'/(name+'.cnf.xz'),'rb') as f:
   for line in f:
    digest.update(line)
    if line.startswith(b'p '):
     _,_,v,c=line.split();nv=int(v);nc=int(c)
    else:
     a=list(map(int,line.split()));assert a[-1]==0 and all(a[:-1]);count+=1
     maxvar=max(maxvar,max(map(abs,a),default=0))
  assert count==nc and maxvar<=nv and digest.hexdigest()==record['cnf_sha256']
  rows.append({'name':name,'vars':nv,'clauses':nc,'maxvar':maxvar,'sha256':digest.hexdigest(),'cake_acceptance_record':True})
print(json.dumps({'status':'PASS','inputs':rows},indent=2))
