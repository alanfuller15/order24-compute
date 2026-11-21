#!/bin/bash
# a9final.sh PART WORKERS [RUN_ID ...] -- the final claim (RA9C item 4): download every production artifact
# (a9v2_s<K> and round-2+ a9v2r<R>_s<K>), then run  a9check --final --part PART  over exactly that set.
#   PART = K/N: this job replays UNSAT records with record position mod N == K (all for 0/1).
#   This splits large profiles across parts. Every part checks whole-tree structural coverage;
#   foreign leaves are provisional until ALL N parts pass their assigned replays (leaves-v1).
#   The final claim is exactly the N jobs K = 0..N-1 (same N), with the SAME input digest and the SAME code digest
#   (exp_out/code.sha256), each printing
#   "A9 FINAL VERDICT (part K/N, input digest D, ...): COVERED AND VERIFIED".
#   RUN_IDs: optional; without them the artifacts are found by name through the API (GH_TOKEN, GH_REPO from exp.yml).
# Local records (out/*) are never included. One source ("gh"); inside it a9check picks one results file per unit.
# Exits 1 and writes exp_out/GATE_FAIL unless the verdict is COVERED AND VERIFIED and the gate passes.
set -u
# A timeout or interruption must leave a durable failure marker for exp.yml (which masks pipeline exits).
mkdir -p exp_out
echo "A9 final has not completed" > exp_out/GATE_FAIL
export A9_CAKE_HEAP=${A9_CAKE_HEAP:-6000}
if [ $# -lt 2 ]; then echo "usage: a9final.sh PART WORKERS [RUN_ID ...] (PART and WORKERS are required)"; mkdir -p exp_out; echo "bad arguments" > exp_out/GATE_FAIL; exit 1; fi
PART=$1; W=$2; shift 2
case "$PART" in */*) ;; *) echo "PART must be K/N"; mkdir -p exp_out; echo "bad PART" > exp_out/GATE_FAIL; exit 1;; esac
case "$W" in ''|*[!0-9]*) echo "WORKERS must be a number"; mkdir -p exp_out; echo "bad WORKERS" > exp_out/GATE_FAIL; exit 1;; esac
mkdir -p exp_out in
# code identity of this part: all parts of one claim must show the same sums
sha256sum exp/*.py exp/*.sh bin/cadical bin/cake_lpr bin/lrat-trim | tee exp_out/code.sha256
echo "code digest: $(sha256sum exp_out/code.sha256 | cut -c1-16)  part $PART" | tee -a exp_out/code.sha256
if [ $# -gt 0 ]; then
  for RID in "$@"; do
    gh api "repos/$GH_REPO/actions/runs/$RID/artifacts" -q '.artifacts[] | "\(.workflow_run.id) \(.name) \(.expired)"'
  done > exp_out/artifacts.txt
else
  gh api --paginate "repos/$GH_REPO/actions/artifacts?per_page=100" \
     -q '.artifacts[] | "\(.workflow_run.id) \(.name) \(.expired)"' > exp_out/artifacts.txt
fi
grep -E ' a9v2(r[0-9]+)?_s[0-9]+ ' exp_out/artifacts.txt | sort -u > exp_out/selected.txt
if grep -q ' true$' exp_out/selected.txt; then echo "expired artifact among the selected" > exp_out/GATE_FAIL; cat exp_out/selected.txt; exit 1; fi
cat exp_out/selected.txt
NS=$(grep -cE ' a9v2_s([0-9]|1[0-5]) ' exp_out/selected.txt)
echo "round-1 shard artifacts found: $NS (expected 16)"
RES=""; LAZ=""
while read -r RID NAME EXP; do
  D="in/${NAME}_${RID}"
  gh run download "$RID" -n "$NAME" -D "$D" || { echo "download $NAME $RID failed" > exp_out/GATE_FAIL; exit 1; }
  [ -f "$D/results.jsonl" ] || continue
  RES="${RES:+$RES,}gh=$D/results.jsonl"; LAZ="${LAZ:+$LAZ,}$D/lazy"
done < exp_out/selected.txt
export CAD=$PWD/bin/cadical CAKE=$PWD/bin/cake_lpr
python3 -I -B exp/a9check.py "$RES" "$LAZ" exp_out/chk --final --partition leaves --part "$PART" --workers "$W" > exp_out/final_full.log 2>&1
CHK=$?
grep -v '"pass": true' exp_out/final_full.log > exp_out/final.log
tail -n 6 exp_out/final.log
FAIL=""
[ "$CHK" = 0 ] || FAIL="a9check --final exit $CHK"
grep -q "COVERED AND VERIFIED" exp_out/final.log || FAIL="${FAIL:+$FAIL; }no COVERED verdict"
python3 -I -B exp/a9gate.py exp_out/final.log in exp_out || FAIL="${FAIL:+$FAIL; }gate"
if [ -n "$FAIL" ]; then echo "$FAIL" > exp_out/GATE_FAIL; echo "GATE FAIL: $FAIL"; exit 1; fi
rm -f exp_out/GATE_FAIL
echo "GATE PASS"
