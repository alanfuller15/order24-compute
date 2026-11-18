#!/bin/bash
# a9shard.sh K N [budget_s] [workers] -- one shard of the alpha = 9 certified run on a GitHub runner (exp.yml).
# Run from the repository root (exp.yml does: bash exp/a9shard.sh $ARGS). Uses bin/cadical, bin/cake_lpr,
# data/masks12.npy. Output: exp_out/ (results.jsonl, lazy/*.json.gz, shard log), uploaded by exp.yml.
# Stops after A9_STOP seconds (default: the workflow's MIN minus 15 minutes, else 330 min) so that the cleanup and
# the coverage summary run before exp.yml's own timeout; finished units are always recorded.
set -u
export A9_CAKE_HEAP=${A9_CAKE_HEAP:-6000}   # 16 GB runner; one cake_lpr at a time per job
K=$1; N=$2; B=${3:-150}; W=${4:-4}
mkdir -p exp_out
sha256sum bin/cadical bin/cake_lpr data/masks12.npy exp/a9*.py | tee exp_out/inputs.sha256
python3 -I -B exp/enum_profiles.py | tee exp_out/profiles.txt
[ -f exp/a9_done.txt ] && export A9_DONE=exp/a9_done.txt   # round 2+: unit tags finished in earlier rounds
A9_STOP=${A9_STOP:-$(( ( ${MIN:-345} - 15 ) * 60 ))} python3 -I -B exp/a9run.py "$K" "$N" exp_out "$B" "$W" 2>&1 | tee exp_out/shard.log
pkill -f 'bin/cadical' ; pkill -f 'bin/cake_lpr' ; sleep 2   # solver children of units cut off by A9_STOP
rm -f exp_out/*.cnf exp_out/*.lrat          # leftovers of a cube that was in flight at the stop, or failed checks (logged)
python3 -I -B exp/a9check.py exp_out/results.jsonl exp_out/lazy exp_out/chk 'NONE^' > exp_out/coverage.txt 2>&1 || true
ls exp_out | head; wc -l exp_out/results.jsonl
