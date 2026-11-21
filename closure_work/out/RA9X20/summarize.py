#!/usr/bin/env python3
"""Build verdict tables only from exact pinned-checker acceptance records."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
rows=[];hashes=[];records=[]
for b in range(4):
 verdict='ACCEPT';per=[]
 for kind in ('producer','independent'):
  name=f'{kind}_B{16+b}';p=ROOT/'logs'/(name+'.json')
  d=json.loads(p.read_text()) if p.exists() else {'status':'UNKNOWN','verified':False}
  accepted=d.get('verified') and d.get('solver_exit')==20 and d.get('cake_exit')==0 and d.get('cake_stdout')=='s VERIFIED UNSAT\n'
  if not accepted:verdict='REJECT (certificate incomplete; '+d.get('status','UNKNOWN')+')'
  per.append(d);records.append(d)
  if accepted:
   hashes.append(f'### {name}\n\n- CNF SHA256: `{d["cnf_sha256"]}`\n- Binary LRAT SHA256: `{d["proof_sha256"]}`\n- LRAT bytes: {d["proof_bytes"]}; proof deleted only after pinned cake verification.\n')
 rows.append(f'| B{16+b} | 4^{15-b} 5^{b} | {verdict} | '+ ' | '.join('VERIFIED UNSAT' if d.get('verified') else d.get('status','UNKNOWN') for d in per)+' |')
text='''# T2b certification verdicts

The scope and dependency review are in [REPORT.md](REPORT.md). These verdicts
apply only to the four indicated unconditional models, without 4f.1 or 4g.2.
ACCEPT requires the reviewed graph-to-CNF implication plus both proof checks;
no larger order-24 theorem is asserted.

| Profile (v1) | Incidence profile | Verdict | Producer CNF | Independent CNF |
|---|---|---|---|---|
'''+ '\n'.join(rows)+'''

## Binary pins

- `bin/cadical`: `eae671d6fab57f7bf909e621adee2a2bd550a0ae0b561065c815f599c7696fe8` (3.0.1)
- `bin/cake_lpr`: `29e02af756c1f0fc4ccac78e9a908e0d8ef01201786f257f1b27b26603390798`

## Full uncompressed CNF / binary-LRAT hashes

'''+ '\n'.join(hashes)+'''
## Controls

All four known relaxed candidates give SAT in the independent encoding, with
every CNF clause checked against the returned assignment. The independent
24-vertex graph checker confirms triangle-free, degree <=8, alpha=9 and (MAX).
It enumerates all 2,704,156 twelve-sets per candidate. Minima B16/B17/B18/B19:
5/4/4/6 edges. B16–B18 use threshold 0 and drop M1; B19 uses threshold 6 and
retains M1. Floors are off. These are not threshold-12 counterexamples.

The primitive tests pass 2,260 assignments. The pinned cake checker verifies a
tiny genuine LRAT and rejects it against a changed SAT CNF, despite returning
exit 0 in the negative control. Acceptance therefore requires its exact stdout.

`INPUT_SHA256SUMS` pins reviewed inputs relative to the repository root;
`SHA256SUMS` pins all retained deliverables relative to this directory. The
per-certificate JSON and full solver/checker logs are under `logs/`; all eight
static CNFs are retained as `cnf/*.cnf.xz`. No LRAT is committed, as requested.
'''
(ROOT/'RESULTS.md').write_text(text)
(ROOT/'verdicts.json').write_text(json.dumps({'profiles':[{'profile':f'B{16+b}','verdict':'ACCEPT' if all(records[2*b+i].get('verified') for i in range(2)) else 'REJECT','producer':records[2*b],'independent':records[2*b+1]} for b in range(4)]},indent=2)+'\n')
