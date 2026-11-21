#!/usr/bin/env python3
"""Pinned checker positive control and wrong-CNF rejection, using a tiny LRAT."""
import pathlib,sys,subprocess,hashlib,json
ROOT=pathlib.Path(__file__).resolve().parent;REPO=ROOT.parents[2];WORK=pathlib.Path(sys.argv[1]);unsat=WORK/'checker_unsat.cnf';sat=WORK/'checker_sat.cnf';proof=WORK/'checker.lrat'
unsat.write_text('p cnf 1 2\n1 0\n-1 0\n');sat.write_text('p cnf 1 2\n1 0\n1 0\n')
cmd=[str(REPO/'bin/cadical'),'-q','--lrat=true','--binary=true',str(unsat),str(proof)];r=subprocess.run(cmd,capture_output=True,text=True);assert r.returncode==20
out={'solver_exit':r.returncode,'command':cmd,'proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),'proof_bytes':proof.stat().st_size}
for name,cnf in [('positive',unsat),('wrong_cnf',sat)]:
 r=subprocess.run([str(REPO/'bin/cake_lpr'),'--CML_HEAP_SIZE=2000',str(cnf),str(proof)],capture_output=True,text=True)
 out[name]={'cnf_sha256':hashlib.sha256(cnf.read_bytes()).hexdigest(),'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
assert out['positive']['exit']==0 and out['positive']['stdout'].splitlines()==['s VERIFIED UNSAT']
assert out['wrong_cnf']['stdout'].splitlines()!=['s VERIFIED UNSAT']
proof.unlink();unsat.unlink();sat.unlink();out['proof_deleted_after_verification']=True
(ROOT/'checker_controls.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
