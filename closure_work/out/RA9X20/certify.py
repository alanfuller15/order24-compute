#!/usr/bin/env python3
"""Regenerate static CNFs; binary LRAT; pinned cake; hash before deleting verified proof."""
import pathlib,subprocess,sys,json,hashlib,time,lzma,resource
ROOT=pathlib.Path(__file__).resolve().parent
REPO=ROOT.parents[2];WORK=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else REPO/'work/RA9X20'
PIN='29e02af756c1f0fc4ccac78e9a908e0d8ef01201786f257f1b27b26603390798'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
 return h.hexdigest()
def limits():resource.setrlimit(resource.RLIMIT_FSIZE,(750*1024**2,750*1024**2))
assert sha(REPO/'bin/cake_lpr')==PIN
WORK.mkdir(parents=True,exist_ok=True);(ROOT/'logs').mkdir(exist_ok=True);(ROOT/'cnf').mkdir(exist_ok=True)
for b in range(4):
 for kind,script in [('producer','dump_producer.py'),('independent','independent.py')]:
  name=f'{kind}_B{16+b}';result=ROOT/'logs'/(name+'.json')
  if '--rerun' not in sys.argv and result.exists() and json.loads(result.read_text()).get('verified'):continue
  cnf=WORK/(name+'.cnf');proof=WORK/(name+'.lrat')
  if proof.exists():raise RuntimeError('Preserving existing unverified proof; choose new scratch: '+str(proof))
  with (ROOT/'logs'/(name+'.build.log')).open('w') as f:
   subprocess.run([sys.executable,str(ROOT/script),str(b),str(cnf)],stdout=f,stderr=subprocess.STDOUT,check=True)
  command=[str(REPO/'bin/cadical'),'--lrat=true','--binary=true',str(cnf),str(proof)]
  start=time.monotonic();print('SOLVING',name,flush=True)
  with (ROOT/'logs'/(name+'.cadical.log')).open('w') as f:
   try:r=subprocess.run(command,stdout=f,stderr=subprocess.STDOUT,timeout=1800,preexec_fn=limits());rc=r.returncode
   except subprocess.TimeoutExpired:rc='TIMEOUT'
  data={'profile':f'B{16+b}','b':b,'encoding':kind,'cnf_sha256':sha(cnf),'cnf_bytes':cnf.stat().st_size,'cadical_sha256':sha(REPO/'bin/cadical'),'cake_lpr_sha256':PIN,'command':command,'solver_exit':rc,'solver_seconds':round(time.monotonic()-start,3),'verified':False,'status':'UNKNOWN'}
  if proof.exists():data.update(proof_sha256=sha(proof),proof_bytes=proof.stat().st_size)
  if rc==20:
   check=[str(REPO/'bin/cake_lpr'),'--CML_HEAP_SIZE=2000','--CML_STACK_SIZE=256',str(cnf),str(proof)]
   t=time.monotonic()
   try:
    r=subprocess.run(check,capture_output=True,text=True,timeout=1800);exitcode=r.returncode;stdout=r.stdout;stderr=r.stderr
   except subprocess.TimeoutExpired:
    exitcode='TIMEOUT';stdout='';stderr='Checker timed out; proof preserved\n'
   (ROOT/'logs'/(name+'.cake.log')).write_text(stdout+stderr)
   data.update(cake_command=check,cake_exit=exitcode,cake_seconds=round(time.monotonic()-t,3),cake_stdout=stdout)
   data['verified']=exitcode==0 and stdout.splitlines()==['s VERIFIED UNSAT']
   if data['verified']:data['status']='UNSAT';proof.unlink();data['proof_deleted_after_verification']=True
  result.write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data),flush=True)
  with cnf.open('rb') as f,lzma.open(ROOT/'cnf'/(name+'.cnf.xz'),'wb',preset=1) as g:
   for c in iter(lambda:f.read(1024*1024),b''):g.write(c)
  if not data['verified']:raise SystemExit('Certificate incomplete; UNKNOWN preserved: '+name)
