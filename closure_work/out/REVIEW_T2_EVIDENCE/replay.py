import pathlib,lzma,hashlib,subprocess,json,time,resource
R=pathlib.Path('/workspace/r');W=pathlib.Path('/workspace/work/review-t2');T=R/'closure_work/out/RA9X20'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def lim():resource.setrlimit(resource.RLIMIT_FSIZE,(200*1024**2,200*1024**2))
rows=[]
for kind in ['independent','producer']:
 name=kind+'_B16';cnf=W/(name+'.cnf');proof=W/(name+'.lrat')
 cnf.write_bytes(lzma.decompress((T/'cnf'/(name+'.cnf.xz')).read_bytes()))
 old=json.loads((T/'logs'/(name+'.json')).read_text());assert sha(cnf)==old['cnf_sha256']
 data={'name':name,'cnf_sha256':sha(cnf),'cadical_sha256':sha(R/'bin/cadical'),'cake_sha256':sha(R/'bin/cake_lpr')}
 start=time.monotonic()
 with (W/(name+'.cadical.log')).open('w') as f:
  s=subprocess.run([str(R/'bin/cadical'),'--lrat=true','--binary=true',str(cnf),str(proof)],stdout=f,stderr=subprocess.STDOUT,timeout=300,preexec_fn=lim)
 data.update(solver_exit=s.returncode,solver_seconds=time.monotonic()-start)
 assert s.returncode==20
 data.update(proof_sha256=sha(proof),proof_bytes=proof.stat().st_size,proof_matches_submission=sha(proof)==old['proof_sha256'])
 p=subprocess.run([str(R/'bin/cake_lpr'),'--CML_HEAP_SIZE=2000','--CML_STACK_SIZE=256',str(cnf),str(proof)],capture_output=True,text=True,timeout=300)
 (W/(name+'.cake.log')).write_text(p.stdout+p.stderr)
 data.update(cake_exit=p.returncode,cake_stdout=p.stdout,cake_stderr=p.stderr)
 assert p.returncode==0 and p.stdout=='s VERIFIED UNSAT\n'
 rows.append(data);(W/'replay.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(data),flush=True)
 # Submission did not retain proofs; reviewer only deletes their own scratch proof after successful validation.
 proof.unlink();cnf.unlink()
