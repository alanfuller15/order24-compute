import pathlib,sys,subprocess,json,hashlib,itertools
R=pathlib.Path('/workspace/r');T=R/'closure_work/out/RA9X20';W=pathlib.Path('/workspace/work/review-t2');sys.path.insert(0,str(T))
from independent import Encoding
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Rebuild all exact submitted static formulas, sequentially, no submission writes.
rebuilt=[]
for b in range(4):
 for kind,script in [('independent','independent.py'),('producer','dump_producer.py')]:
  name=f'{kind}_B{16+b}';cnf=W/(name+'.rebuild.cnf')
  p=subprocess.run([sys.executable,str(T/script),str(b),str(cnf)],capture_output=True,text=True,check=True)
  h=H(cnf);d=json.loads((T/'logs'/(name+'.json')).read_text());assert h==d['cnf_sha256']
  assert (T/'logs'/(name+'.cake.log')).read_text()=='s VERIFIED UNSAT\n'
  assert 's UNSATISFIABLE' in (T/'logs'/(name+'.cadical.log')).read_text()
  rebuilt.append({'name':name,'cnf_sha256':h,'build_output':p.stdout.strip(),'retained_logs_consistent':True});cnf.unlink()
(W/'rebuild.json').write_text(json.dumps(rebuilt,indent=2)+'\n');print('ALL 8 REBUILDS MATCH',flush=True)
# Rerun submitted graph checker + planted-model checks without altering original control logs.
checker=W/'graph-check';subprocess.run(['g++','-O2','-std=c++17',str(T/'check_graph.cpp'),'-o',str(checker)],check=True)
controls=[]
for b in range(4):
 record=json.loads((T/f'control_B{16+b}.candidate.json').read_text());thr=record['thr'];e=Encoding(b,thr,drop_m1=b<3)
 assert [len(m) for m in record['masks']]==[4]*(15-b)+[5]*b
 for x,mask in enumerate(record['masks']):
  for i in range(9):e.add([e.m[x][i] if i in mask else -e.m[x][i]])
 cnf=W/f'control{b}.cnf';e.write(cnf)
 p=subprocess.run([str(R/'bin/cadical'),'-q',str(cnf)],capture_output=True,text=True,timeout=90)
 model={int(x) for l in p.stdout.splitlines() if l.startswith('v ') for x in l[2:].split() if int(x)}
 assert p.returncode==10 and all(any(l in model for l in c) for c in e.clauses)
 g=subprocess.run([str(checker)],input=' '.join(str(sum(1<<i for i in m)) for m in record['masks']),capture_output=True,text=True,check=True)
 d=json.loads(g.stdout);old=json.loads((T/'controls.json').read_text())[b]
 assert d==old['graph'] and H(cnf)==old['cnf_sha256'];cnf.unlink()
 controls.append({'profile':f'B{16+b}','threshold':thr,'drop_m1':b<3,'solver_exit':p.returncode,'all_clauses_checked':True,'graph':d});print('CONTROL',b,d,flush=True)
(W/'controls.json').write_text(json.dumps(controls,indent=2)+'\n')
# Fresh checker positive and wrong-CNF negative control, with acceptance based on exact stdout.
u=W/'tiny-unsat.cnf';s=W/'tiny-sat.cnf';proof=W/'tiny.lrat';u.write_text('p cnf 1 2\n1 0\n-1 0\n');s.write_text('p cnf 1 2\n1 0\n1 0\n')
p=subprocess.run([str(R/'bin/cadical'),'-q','--lrat=true','--binary=true',str(u),str(proof)],capture_output=True);assert p.returncode==20
checks={}
for name,cnf in [('positive',u),('wrong_cnf',s)]:
 p=subprocess.run([str(R/'bin/cake_lpr'),'--CML_HEAP_SIZE=2000',str(cnf),str(proof)],capture_output=True,text=True,timeout=30)
 checks[name]={'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
assert checks['positive']['exit']==0 and checks['positive']['stdout']=='s VERIFIED UNSAT\n' and checks['wrong_cnf']['stdout']!='s VERIFIED UNSAT\n'
(W/'checker-controls.json').write_text(json.dumps(checks,indent=2)+'\n')
print('CHECKER CONTROLS',checks,flush=True)
