#!/bin/bash
# exp/rep_proof.sh LAYER [RUN:ARTIFACT ...] -- replay of RECORDED proofs straight from their producer artifacts, before the
# artifacts expire. Research only (exp.yml): it records nothing and approves nothing; its output is read by a reviewer.
#
# For each producer artifact (the pairs given as arguments, or RUN_ID + ARTIFACT from exp.yml when no pair is given):
#   1. download it (gh run download, as exp/a9verify.sh and exp/lratcatch_trial.sh do);
#   2. bind it to the record: the formulas to check are the lines of exp/rep_proof/manifest.jsonl (one per recorded
#      formula, made from layers/l*/audit/G*/records.jsonl) that name this run and artifact (and TAG, if exp.yml gives one);
#      each must occur exactly once in the artifact's results.jsonl, and that line must equal the record (canonical JSON
#      SHA-256, the record minus its "gha" field), with the same cnf_sha256 and proof_sha256, and the proof file's SHA-256
#      must equal proof_sha256;
#   3. run the audit's own script audit_kit/run_audit.sh (pinned below) on exactly those tags: the PINNED checker
#      audit_kit/l<M>/code/gcert<M>.py, unmodified, rebuilds every CNF with the pinned encoder of its record ("encoder"
#      field), compares its SHA-256 with the record, checks the proof SHA-256 and runs the pinned cake_lpr (29e02af7...,
#      heaps 2000 then 4000 MB); then negative control A (one lazy item changed -> the rebuilt CNF differs -> must fail)
#      and negative control B (the first proof tampered -> must fail). ONE change to run_audit.sh, made at run time with
#      sed and logged: control B flips byte len(prefix)//2 instead of byte 4,500,000 of the 9,000,000-byte prefix. For a
#      proof of 9,000,000 bytes or more that is the same byte; most recorded proofs (15,106 of 16,085) are smaller than
#      4.5 MB, where the original line raises IndexError and leaves the proof untampered;
#   4. write one JSON line per formula to exp_out/results.jsonl. "result" is "s VERIFIED UNSAT" only if: the binding
#      held, the checker's main exit is 0 or 3 (partial run), the formula has exactly one CHECK_RESULTS line with pass
#      true, cnf_match, proof_match, cake_lpr "s VERIFIED UNSAT", cake_exit 0 and the manifest's hashes, and both
#      negative controls exited 1. Otherwise "result" is "FAIL" with a reason, and exp_out/GATE_FAIL is written.
# Environment (exp.yml): RUN_ID, ARTIFACT, TAG (optional), GH_TOKEN, GH_REPO. REP_IN_DIR=<dir> (local tests only) skips the
# download and uses <dir>/<RUN>_<ARTIFACT>/ (results.jsonl + proofs/). REP_MANIFEST overrides the manifest (tests only;
# its SHA-256 is in exp_out/inputs.sha256 either way).
set -u
R=$PWD; O=$R/exp_out; mkdir -p "$O/pairs"
RUN_AUDIT_SHA=69e79abe66e68205153f78b97e132d13d7bf31515b9f7b365c12be16760868f5   # audit_kit/run_audit.sh at 30091e7
CAKE_SHA=29e02af756c1f0fc4ccac78e9a908e0d8ef01201786f257f1b27b26603390798
MAN=${REP_MANIFEST:-$R/exp/rep_proof/manifest.jsonl}
gate() { echo "$*" >> "$O/GATE_FAIL"; echo "GATE_FAIL: $*"; }
die()  { gate "$*"; exit 1; }
echo "incomplete: job did not reach its clean end (removed only there)" > "$O/GATE_FAIL"   # RRP should-fix 1: a timeout/kill leaves the job red
M=${1:-}; shift || true
case "$M" in ''|*[!0-9]*) die "usage: rep_proof.sh LAYER [RUN:ARTIFACT ...]";; esac
[ "$M" -ge 51 ] && [ "$M" -le 87 ] || die "layer $M out of range"
K=$R/audit_kit/l$M
[ -f "$MAN" ] || die "no manifest $MAN"
[ -d "$K" ] || die "no audit kit audit_kit/l$M"
if [ $# -gt 0 ]; then PAIRS=("$@"); else
  [ -n "${RUN_ID:-}" ] && [ -n "${ARTIFACT:-}" ] || die "no pairs and no RUN_ID/ARTIFACT"; PAIRS=("$RUN_ID:$ARTIFACT"); fi
TAG=${TAG:-}
[[ -z "$TAG" || "$TAG" =~ ^L[0-9]{2}_s[0-9]+a[0-9]+b[0-9]+c[0-9]+_[0-9]{4}$ ]] || die "bad TAG"

# pins (as audit.yml): kit, cake_lpr, the audit script; tools where run_audit.sh expects them
( cd "$K" && sha256sum -c PINS.sha256 ) > "$O/pins_check.txt" 2>&1 || die "kit pins do not match (pins_check.txt)"
echo "$CAKE_SHA  bin/cake_lpr" | sha256sum -c >> "$O/pins_check.txt" 2>&1 || die "bin/cake_lpr is not the pinned binary"
echo "$RUN_AUDIT_SHA  audit_kit/run_audit.sh" | sha256sum -c >> "$O/pins_check.txt" 2>&1 || die "audit_kit/run_audit.sh is not the pinned script"
[ -x /usr/bin/time ] || sudo apt-get install -y -q time > /dev/null 2>&1 || die "cannot install /usr/bin/time"
mkdir -p ~/tools/cake_lpr && cp bin/cake_lpr ~/tools/cake_lpr/cake_lpr && chmod +x ~/tools/cake_lpr/cake_lpr
mkdir -p "$R/work"; RA=$R/work/run_audit_rep.sh
sed 's|b\[4500000\]^=1|b[len(b)//2]^=1|' audit_kit/run_audit.sh > "$RA"
diff audit_kit/run_audit.sh "$RA" > "$O/run_audit.diff"; [ "$(grep -c '^[<>]' "$O/run_audit.diff")" = 2 ] || die "run_audit.sh rewrite did not change exactly one line"
sha256sum exp/rep_proof.sh "$MAN" audit_kit/run_audit.sh "$RA" "$K"/code/*.py "$K"/formulas*.json bin/cake_lpr > "$O/inputs.sha256"
{ echo "layer=$M pairs=${PAIRS[*]} tag=$TAG"; echo "commit=${GITHUB_SHA:-local} job_run=${GITHUB_RUN_ID:-local}"; nproc; free -m; python3 -I -c 'import pysat; print("pysat", pysat.__version__)'; } > "$O/env.txt" 2>&1

# disk: gh run download keeps the zip and its extraction (up to 2 x 6 GB); free preinstalled toolchains on a hosted runner
df -BG / > "$O/df_before.txt"
if [ "${GITHUB_ACTIONS:-}" = true ] && [ "$(df -BG --output=avail / | tail -1 | tr -dc 0-9)" -lt 25 ]; then
  sudo rm -rf /usr/local/lib/android /usr/share/dotnet /opt/ghc /usr/local/.ghcup /opt/hostedtoolcache/CodeQL 2>/dev/null; df -BG / > "$O/df_after_cleanup.txt"; fi

NFAIL=0; NOK=0
for P in "${PAIRS[@]}"; do
  RID=${P%%:*}; ART=${P#*:}
  [[ "$RID" =~ ^[0-9]+$ && "$ART" =~ ^[A-Za-z0-9_.-]+$ ]] || { gate "bad pair $P"; NFAIL=$((NFAIL+1)); continue; }
  PO=$O/pairs/${RID}_$ART; mkdir -p "$PO"; rm -rf "$R/in" "$R/aout" "$R/negB"
  date -u +%FT%TZ > "$PO/start.txt"
  if [ -n "${REP_IN_DIR:-}" ]; then cp -r "$REP_IN_DIR/${RID}_$ART" "$R/in" || { gate "$P: no local input"; NFAIL=$((NFAIL+1)); continue; }
  else
    ok=0; for i in 1 2 3; do gh run download "$RID" -n "$ART" -D "$R/in" > "$PO/download.log" 2>&1 && { ok=1; break; }; rm -rf "$R/in"; sleep 30; done
    [ $ok = 1 ] || { gate "$P: download failed (download.log)"; NFAIL=$((NFAIL+1)); continue; }
  fi
  du -sb "$R/in" > "$PO/in_size.txt"
  # bind the artifact to the records; writes the tag regex (in results.jsonl order) and the expected lines
  python3 -I - "$MAN" "$R/in" "$RID" "$ART" "$M" "$TAG" "$PO" <<'PY'
import json, sys, hashlib, os
man, ind, rid, art, m, tag, po = sys.argv[1:8]
def canon(r):
    r = dict(r); r.pop('gha', None)
    return hashlib.sha256(json.dumps(r, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
def fsha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()
want = {}
for l in open(man):
    x = json.loads(l)
    if x['run'] == rid and x['artifact'] == art and x['layer'] == int(m) and (not tag or x['tag'] == tag): want[x['tag']] = x
bad = []; seen = {}; order = []
for l in open(os.path.join(ind, 'results.jsonl')):
    if not l.strip(): continue
    try: r = json.loads(l)
    except ValueError: continue
    t = r.get('tag')
    if t in want:
        seen[t] = seen.get(t, 0) + 1
        if seen[t] == 1: order.append(t)
        x = want[t]
        if canon(r) != x['record_canon_sha256']: bad.append(f'{t}: artifact line differs from the record')
        if r.get('cnf_sha256') != x['cnf_sha256'] or r.get('proof_sha256') != x['proof_sha256']: bad.append(f'{t}: hashes differ from the record')
for t in want:
    if seen.get(t, 0) != 1: bad.append(f'{t}: {seen.get(t, 0)} lines in results.jsonl (need exactly 1)')
    else:
        p = os.path.join(ind, 'proofs', t + '.lrat.xz')
        if not os.path.isfile(p) or os.path.islink(p): bad.append(f'{t}: no regular proof file')
        elif fsha(p) != want[t]['proof_sha256']: bad.append(f'{t}: proof file SHA-256 differs from the record')
json.dump({'selected': sorted(want), 'order': order, 'binding_errors': bad}, open(os.path.join(po, 'binding.json'), 'w'), indent=1)
if not want: bad.append('no manifest line names this run/artifact/layer/tag')
open(os.path.join(po, 'regex.txt'), 'w').write('^(' + '|'.join(order) + ')$' if order else '')
sys.exit(1 if bad else 0)
PY
  BIND=$?
  RX=$(cat "$PO/regex.txt" 2>/dev/null)
  if [ $BIND = 0 ] && [ -n "$RX" ]; then
    ( bash "$RA" "$M" "$RX" ) > "$PO/run_audit.log" 2>&1
    cp -r "$R/aout" "$PO/aout" 2>/dev/null
  fi
  # verdict per formula
  python3 -I - "$MAN" "$PO" "$RID" "$ART" "$M" "$BIND" "$O/results.jsonl" "${GITHUB_RUN_ID:-local}" "${GITHUB_SHA:-local}" <<'PY'
import json, sys, os, time
man, po, rid, art, m, bind, out, jrun, sha = sys.argv[1:10]
B = json.load(open(os.path.join(po, 'binding.json'))) if os.path.exists(os.path.join(po, 'binding.json')) else {'selected': [], 'binding_errors': ['binding did not run']}
X = {}
for l in open(man):
    x = json.loads(l)
    if x['tag'] in B['selected']: X[x['tag']] = x
A = os.path.join(po, 'aout')
def rd(n):
    try: return open(os.path.join(A, n)).read().strip()
    except OSError: return None
def lines(n):
    try: return [json.loads(l) for l in open(os.path.join(A, n)) if l.strip()]
    except OSError: return []
ex = {k: rd(k + '.exit') for k in ('main', 'negA', 'negB')}
CR = lines('run_main/CHECK_RESULTS.jsonl')
nA, nB = lines('run_negA/CHECK_RESULTS.jsonl'), lines('run_negB/CHECK_RESULTS.jsonl')   # RRP should-fix 2: semantic controls
negs_ok = (ex['negA'] == '1' and ex['negB'] == '1' and len(nA) == 1 and len(nB) == 1
           and not nA[0].get('pass') and nA[0].get('cnf_match') is False
           and not nB[0].get('pass') and nB[0].get('cnf_match') is True and nB[0].get('proof_match') is False)
nok = nf = 0
with open(out, 'a') as f:
    for t in B['selected']:
        x = X[t]; why = []
        if bind != '0': why += B['binding_errors'] or ['binding failed']
        if ex['main'] not in ('0', '3'): why.append(f"checker main exit {ex['main']}")
        mine = [o for o in CR if o.get('tag') == t]
        if len(mine) != 1: why.append(f'{len(mine)} CHECK_RESULTS lines')
        else:
            o = mine[0]
            if not (o.get('pass') is True and o.get('cnf_match') is True and o.get('proof_match') is True and o.get('cake_lpr') == 's VERIFIED UNSAT'
                    and o.get('cake_exit') == 0 and o.get('cnf_sha256') == x['cnf_sha256'] and o.get('proof_sha256') == x['proof_sha256']):
                why.append('checker line does not pass')
        if not negs_ok: why.append(f"negative controls not both rejected (negA {ex['negA']}, negB {ex['negB']})")
        o = mine[0] if len(mine) == 1 else {}
        res = {'tag': t, 'layer': int(m), 'run': rid, 'artifact': art, 'encoder': x['encoder'], 'cnf_sha256': x['cnf_sha256'],
               'proof_sha256': x['proof_sha256'], 'record_canon_sha256': x['record_canon_sha256'],
               'result': 'FAIL' if why else 's VERIFIED UNSAT', 'reason': '; '.join(why),
               'cake_heap_mb': o.get('cake_heap_mb'), 'code_sha256': o.get('code_sha256'), 'exits': ex,
               'replay_run': jrun, 'replay_commit': sha, 'time': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
        f.write(json.dumps(res) + '\n')
        nok += not why; nf += bool(why)
open(os.path.join(po, 'verdict.txt'), 'w').write(f'{nok} {nf}\n')
PY
  read a b < "$PO/verdict.txt" 2>/dev/null || { a=0; b=1; }
  [ "$BIND" = 0 ] || [ "$b" != 0 ] || b=1
  NOK=$((NOK+a)); NFAIL=$((NFAIL+b)); [ "$b" = 0 ] || gate "$P: $b formula(s) not verified"
  date -u +%FT%TZ > "$PO/end.txt"
  rm -rf "$R/in" "$R/aout" "$R/negB"
done
echo "{\"layer\": $M, \"pairs\": ${#PAIRS[@]}, \"verified\": $NOK, \"failed\": $NFAIL}" > "$O/RESULT.json"
cat "$O/RESULT.json"
[ "$NFAIL" = 0 ] && [ "$NOK" -gt 0 ] || { gate "verified $NOK, failed $NFAIL"; exit 1; }
[ "$(cat "$O/GATE_FAIL")" = "incomplete: job did not reach its clean end (removed only there)" ] && rm -f "$O/GATE_FAIL"   # clean end: only the start marker is present
