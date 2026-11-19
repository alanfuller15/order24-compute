#!/usr/bin/env python3
"""collect.py MANIFEST DIR [OUT] -- merge the outputs of the rep_proof.sh jobs (each downloaded exp artifact rp-<job> unpacked
under DIR/<name>/, i.e. DIR/<name>/results.jsonl, inputs.sha256, GATE_FAIL?) into one coverage report. Run as python3 -I.
A formula counts as replayed only if (RRP should-fix 3):
  - exactly one distinct passing line exists for it across all jobs, and NO failing line for it exists anywhere;
  - that line has result "s VERIFIED UNSAT", empty reason, the manifest's run, artifact, cnf_sha256, proof_sha256 and
    record_canon_sha256, exits negA = negB = 1 and main in {0, 3};
  - its code_sha256 equals the audits' checker code hash for that layer (exp/rep_proof/code_sha.json);
  - the job that wrote it has no GATE_FAIL file at all (conservative: any failure in a job voids all its lines; re-dispatch);
  - the job used the same rep_proof.sh, manifest and run_audit.sh hashes as every other counted job.
Exit 0 only when every manifest formula is covered."""
import json, sys, os, glob, collections
man_p, d = sys.argv[1], sys.argv[2]; out = sys.argv[3] if len(sys.argv) > 3 else 'REPLAY_COVERAGE.json'
CODE = json.load(open(os.path.join(os.path.dirname(os.path.abspath(man_p)), 'code_sha.json')))
MAN = {}
for l in open(man_p):
    if l.strip():
        x = json.loads(l); MAN[x['tag']] = x
ok = collections.defaultdict(set); fails = collections.defaultdict(list); jobs = {}; hashes = collections.Counter()
for rp in sorted(glob.glob(os.path.join(d, '*', 'results.jsonl'))):
    jd = os.path.dirname(rp); name = os.path.basename(jd)
    ins = {}
    for l in open(os.path.join(jd, 'inputs.sha256')):
        h, p = l.split(None, 1); ins[os.path.basename(p.strip())] = h
    key = (ins.get('rep_proof.sh'), ins.get('manifest.jsonl'), ins.get('run_audit.sh'))
    gf = os.path.exists(os.path.join(jd, 'GATE_FAIL'))
    hashes[key] += 1; jobs[name] = {'inputs': key, 'gate_fail': gf}
    for l in open(rp):
        if not l.strip(): continue
        o = json.loads(l); x = MAN.get(o.get('tag'))
        ex = o.get('exits', {}) or {}
        good = (x is not None and not gf and o.get('result') == 's VERIFIED UNSAT' and o.get('reason') == '' and
                all(o.get(k) == x[k] for k in ('run', 'artifact', 'cnf_sha256', 'proof_sha256', 'record_canon_sha256')) and
                ex.get('negA') == '1' and ex.get('negB') == '1' and ex.get('main') in ('0', '3') and
                o.get('code_sha256') == CODE.get(str(x['layer'])))
        if good: ok[o['tag']].add((name, key, json.dumps(o, sort_keys=True)))
        else: fails[o.get('tag')].append((name, o.get('result'), o.get('reason'), gf))
main_key = hashes.most_common(1)[0][0] if hashes else None
def counts(t):
    v = [e for e in ok.get(t, ()) if e[1] == main_key]
    return len({e[0] for e in v}) == 1 and len({e[2] for e in v}) == 1 and not fails.get(t)
covered = sorted(t for t in MAN if counts(t))
missing = sorted(t for t in MAN if t not in covered)
rep = {'manifest': man_p, 'formulas': len(MAN), 'covered': len(covered), 'missing': len(missing),
       'by_layer': {L: [sum(1 for t in covered if MAN[t]['layer'] == L), sum(1 for t in MAN if MAN[t]['layer'] == L)]
                    for L in sorted({x['layer'] for x in MAN.values()})},
       'input_hash_sets': {' '.join(map(str, k)): n for k, n in hashes.items()}, 'counted_inputs': main_key,
       'failed_lines': {str(t): v for t, v in fails.items()}, 'missing_tags': missing[:2000],
       'jobs': len(jobs), 'jobs_with_gate_fail': sorted(n for n, j in jobs.items() if j['gate_fail'])}
json.dump(rep, open(out, 'w'), indent=1)
print(f"covered {len(covered)} of {len(MAN)}; missing {len(missing)}; jobs {len(jobs)}; jobs with GATE_FAIL {len(rep['jobs_with_gate_fail'])}; input-hash sets {len(hashes)}")
sys.exit(0 if not missing else 1)
