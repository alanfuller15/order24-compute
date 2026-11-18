#!/bin/bash
# a9verify.sh [workers] -- independent replay of ONE production shard's artifact (exp.yml inputs run_id = that run's
# id, artifact = its artifact name). Rebuilds every leaf CNF from (profile, cube, lazy list) with exp/a9core.py,
# compares SHA-256 with the record, re-runs CaDiCaL and cake_lpr. Output exp_out/verify.log.
# Version 3 (RA9C item 5): exits 1 and writes exp_out/GATE_FAIL unless the line "checked n leaves: n pass" has equal
# numbers, a9check exits 0, and no MODEL record / MODEL_FOUND.json is present. Coverage is NOT expected (one shard).
set -u
export A9_CAKE_HEAP=${A9_CAKE_HEAP:-6000}
W=${1:-4}
mkdir -p exp_out in
gh run download "$RUN_ID" -n "$ARTIFACT" -D in || { echo "download failed" > exp_out/GATE_FAIL; exit 1; }
export CAD=$PWD/bin/cadical CAKE=$PWD/bin/cake_lpr
python3 -I -B exp/a9check.py in/results.jsonl in/lazy exp_out/chk --workers "$W" > exp_out/verify_full.log 2>&1
CHK=$?
grep -v '"pass": true' exp_out/verify_full.log > exp_out/verify.log      # failures and summary lines only
grep -c '"pass": true' exp_out/verify_full.log; rm -f exp_out/verify_full.log
cat exp_out/verify.log | tail -n 5
FAIL=""
[ "$CHK" = 0 ] || FAIL="a9check exit $CHK"
python3 -I -B exp/a9gate.py exp_out/verify.log in exp_out || FAIL="${FAIL:+$FAIL; }gate"
if [ -n "$FAIL" ]; then echo "$FAIL" > exp_out/GATE_FAIL; echo "GATE FAIL: $FAIL"; exit 1; fi
echo "GATE PASS"
