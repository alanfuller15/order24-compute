#!/usr/bin/env python3
"""Plant known relaxed candidates; pinned CaDiCaL SAT; check every CNF clause and full graph."""
import pathlib,json,sys,subprocess,hashlib,itertools
from independent import Encoding
ROOT=pathlib.Path(__file__).resolve().parent;REPO=ROOT.parents[2];WORK=pathlib.Path(sys.argv[1]);SOURCE=REPO/'closure_work/research/alpha9/v2/exp_B4'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checker=WORK/'check_graph';subprocess.run(['g++','-O2','-std=c++17',str(ROOT/'check_graph.cpp'),'-o',str(checker)],check=True)
results=[]
for b in range(4):
 name=f'control_B{16+b}';src=SOURCE/(f'ablate_main_b{b}_thr0_dropM1_candidate.json' if b<3 else 'candidate_b3_thr6_v2.json')
 record=json.loads(src.read_text());threshold=record['thr'];e=Encoding(b,threshold,drop_m1=b<3)
 for x,mask in enumerate(record['masks']):
  for i in range(9):e.add([e.m[x][i] if i in mask else -e.m[x][i]])
 cnf=WORK/(name+'.cnf');e.write(cnf)
 p=subprocess.run([str(REPO/'bin/cadical'),'-q',str(cnf)],capture_output=True,text=True,timeout=300)
 (ROOT/'logs'/(name+'.sat.log')).write_text(p.stdout+p.stderr)
 assert p.returncode==10,(name,p.returncode)
 model={int(x) for line in p.stdout.splitlines() if line.startswith('v ') for x in line[2:].split() if int(x)}
 assert not any(-l in model for l in model),'inconsistent assignment'
 assert all(any(l in model for l in c) for c in e.clauses),'unsatisfied clause'
 masks=[sum(1<<i for i in m) for m in record['masks']]
 g=subprocess.run([str(checker)],input=' '.join(map(str,masks)),capture_output=True,text=True,check=True)
 verified=json.loads(g.stdout)
 assert verified['triangle_free'] and verified['max_degree']<=8 and verified['alpha']==9 and verified['nonmaximal_pairs']==0 and verified['min_edges_12']>=threshold
 out=ROOT/(name+'.candidate.json');out.write_text(json.dumps(record,indent=2)+'\n')
 results.append({'name':name,'source_candidate':str(src.relative_to(REPO)),'source_candidate_sha256':sha(src),'threshold':threshold,'drop_m1':b<3,'floors_enabled':False,'cnf_sha256':sha(cnf),'vars':e.pool.top,'clauses':len(e.clauses),'solver_exit':p.returncode,'all_clauses_checked':True,'graph':verified,'binary_sha256':sha(checker)})
 cnf.unlink();print(json.dumps(results[-1]),flush=True)
(ROOT/'controls.json').write_text(json.dumps(results,indent=2)+'\n')
