#!/bin/bash
# a9shard.sh K N [budget_s] [workers] -- one shard of the alpha = 9 certified run on a GitHub runner (exp.yml).
# Version 3: identical solving (exp/a9run.py unchanged); adds the job gate (RA9C item 5): a model record or a
# MODEL_FOUND.json writes exp_out/GATE_FAIL and exits 1 (the job turns red only with the exp.yml gate step,
# see exp_stage_v3/exp.yml.patch, because exp.yml runs the script with "|| true").
# Run from the repository root. Uses bin/cadical, bin/cake_lpr, data/masks12.npy. Output: exp_out/.
set -u
export A9_CAKE_HEAP=${A9_CAKE_HEAP:-6000}   # 16 GB runner; one cake_lpr at a time per job
K=$1; N=$2; B=${3:-150}; W=${4:-4}
mkdir -p exp_out
sha256sum bin/cadical bin/cake_lpr data/masks12.npy exp/a9*.py | tee exp_out/inputs.sha256
python3 -I -B exp/enum_profiles.py | tee exp_out/profiles.txt
[ -f exp/a9_done.txt ] && export A9_DONE=exp/a9_done.txt   # round 2+: unit tags finished in earlier rounds
A9_STOP=${A9_STOP:-$(( ( ${MIN:-345} - 15 ) * 60 ))} python3 -I -B exp/a9run.py "$K" "$N" exp_out "$B" "$W" 2>&1 | tee exp_out/shard.log
RUN_EXIT=${PIPESTATUS[0]}
pkill -f 'bin/cadical' ; pkill -f 'bin/cake_lpr' ; sleep 2   # solver children of units cut off by A9_STOP
rm -f exp_out/*.cnf exp_out/*.lrat          # leftovers of a cube in flight at the stop, or of failed checks (logged)
python3 -I -B exp/a9check.py exp_out/results.jsonl exp_out/lazy exp_out/chk --coverage-only > exp_out/coverage.txt 2>&1
wc -l exp_out/results.jsonl
FAIL=""
[ "$RUN_EXIT" = 3 ] && FAIL="a9run exit 3 (model)"
grep -q "MODEL FOUND" exp_out/shard.log && FAIL="MODEL FOUND in shard.log"
grep -q "ATTENTION" exp_out/shard.log && FAIL="${FAIL:+$FAIL; }unverified leaf (ATTENTION) in shard.log"
python3 -I -B exp/a9gate.py - exp_out || FAIL="${FAIL:+$FAIL; }MODEL_FOUND.json"
if [ -n "$FAIL" ]; then echo "$FAIL" > exp_out/GATE_FAIL; echo "GATE FAIL: $FAIL"; exit 1; fi
echo "GATE PASS"
