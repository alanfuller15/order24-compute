#!/bin/bash
# a9tel_sample.sh PART WORKERS -- EXPERIMENTAL telemetry sample (branch speedups). Not a claim, no gate, no GATE_PASS.
# Replays the leaves of PART (e.g. 0/256, leaf partition = an even spread over all profiles) with exp/a9check_tel.py
# and writes per-stage percentiles to exp_out/TELEMETRY.md and exp_out/telemetry.json.
set -u -o pipefail
PART=$1; W=$2; mkdir -p exp_out in
gh api --paginate "repos/$GH_REPO/actions/artifacts?per_page=100" -q '.artifacts[] | "\(.workflow_run.id) \(.name) \(.expired)"' > exp_out/artifacts.txt
grep -E ' a9v2(r[0-9]+)?_s[0-9]+ false$' exp_out/artifacts.txt | sort -u > exp_out/selected.txt
RES=""; LAZ=""
while read -r RID NAME EXP; do
  D="in/${NAME}_${RID}"; gh run download "$RID" -n "$NAME" -D "$D" || continue
  [ -f "$D/results.jsonl" ] || continue
  RES="${RES:+$RES,}gh=$D/results.jsonl"; LAZ="${LAZ:+$LAZ,}$D/lazy"
done < exp_out/selected.txt
export CAD=$PWD/bin/cadical CAKE=$PWD/bin/cake_lpr TRIM=$PWD/bin/lrat-trim A9_CAKE_HEAP=${A9_CAKE_HEAP:-6000}
T0=$(date +%s)
python3 -I -B exp/a9check_tel.py "$RES" "$LAZ" exp_out/chk --final --partition leaves --part "$PART" --workers "$W" > exp_out/tel_full.log 2>&1
echo "checker exit $? after $(( $(date +%s) - T0 )) s" | tee exp_out/tel_exit.txt
python3 -I - exp_out/tel_full.log <<'PY' | tee exp_out/TELEMETRY.md
import json, sys, statistics as S
rows = []
for l in open(sys.argv[1]):
    if l.startswith('{') and '"stage_seconds"' in l:
        try: rows.append(json.loads(l))
        except Exception: pass
def pct(v, q):
    v = sorted(v); return v[min(len(v)-1, int(q*len(v)))] if v else None
stages = sorted({k for r in rows for k in r['stage_seconds']})
out = {'leaves': len(rows), 'pass': sum(1 for r in rows if r.get('pass')), 'stages': {}}
print(f"# A9 telemetry sample: {len(rows)} leaves, {out['pass']} pass\n\n| stage | p50 s | p95 s | p99 s | max s | total s |\n|---|---|---|---|---|---|")
for k in stages + ['seconds']:
    v = [r['stage_seconds'].get(k, 0) if k != 'seconds' else r['seconds'] for r in rows]
    out['stages'][k] = {'p50': pct(v, .5), 'p95': pct(v, .95), 'p99': pct(v, .99), 'max': max(v), 'total': round(sum(v), 1)}
    s = out['stages'][k]; print(f"| {k} | {s['p50']} | {s['p95']} | {s['p99']} | {s['max']} | {s['total']} |")
for k in ('proof_bytes_raw', 'proof_bytes_checked', 'children_maxrss_kb'):
    v = [r[k] for r in rows if r.get(k)]
    if v: print(f"\n{k}: p50 {pct(v,.5)}, p95 {pct(v,.95)}, max {max(v)}")
json.dump(out, open('exp_out/telemetry.json', 'w'), indent=1)
PY
