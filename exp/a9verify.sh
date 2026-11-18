#!/bin/bash
# a9verify.sh -- independent replay of ONE production shard's artifact on a GitHub runner (exp.yml with inputs
# run_id = the production run's id, artifact = its artifact name). Rebuilds every leaf CNF from (profile, cube, lazy
# list) with exp/a9core.py, compares SHA-256 with the record, re-runs CaDiCaL and cake_lpr; output exp_out/verify.log.
# Coverage of all 430 profiles is NOT expected here (one shard); the global coverage check is run on the merged results.
set -u
export A9_CAKE_HEAP=${A9_CAKE_HEAP:-8000}
mkdir -p exp_out in
gh run download "$RUN_ID" -n "$ARTIFACT" -D in
export CAD=$PWD/bin/cadical CAKE=$PWD/bin/cake_lpr
python3 -I -B exp/a9check.py in/results.jsonl in/lazy exp_out/chk '.' 2>&1 | grep -v '^{"tag".*"pass": true}' | tee exp_out/verify.log
