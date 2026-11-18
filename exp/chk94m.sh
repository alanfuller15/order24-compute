#!/bin/bash
# exp/chk94m.sh K [MINUTES]: independent-replay shard K (of 12) of the (6,7^2,8^21) replication, with the UNMODIFIED checker
# exp/rep94m/check_all94m.py (= f94m/scripts/check_all94m.py): for every class of the shard it rebuilds the CNF from
# classes94m.json + the recorded lazy list, compares its SHA-256 with the record, makes a fresh CaDiCaL 3.0.1 LRAT proof and
# accepts only cake_lpr's exact line "s VERIFIED UNSAT". The shard is selected with the checker's own tag-regex argument
# (exp/rep94m/shard_regex/K.txt), so each run is a PARTIAL run (exit 1 from the checker's last line unless every selected
# class passes, in which case exit 0 with a PARTIAL RUN line). Two negative controls on the shard's first class follow.
set -u; K=$1; MIN=${2:-330}; R=$PWD
mkdir -p exp_out work exp/lowcheck; cp data/masks12.npy exp/lowcheck/masks12.npy
tar -xf exp/rep94m/merged.tar -C work
sha256sum exp/chk94m.sh exp/rep94m/check_all94m.py exp/rep94m/rebuild94m.py exp/rep94m/cegar_shape.py exp/rep94m/classes94m.json exp/rep94m/merged.tar exp/rep94m/shard_regex/$K.txt work/run_merged/results94m.jsonl bin/cadical bin/cake_lpr > exp_out/inputs.sha256
RX=$(cat exp/rep94m/shard_regex/$K.txt)
cd exp/rep94m
CAD=$R/bin/cadical CAKE=$R/bin/cake_lpr timeout --signal=INT $(( MIN * 60 )) python3 -I -B check_all94m.py classes94m.json $R/work/run_merged/results94m.jsonl $R/work/run_merged $R/work/chk 4 "$RX" > $R/exp_out/main.stdout 2> $R/exp_out/main.stderr
echo $? > $R/exp_out/main.exit; cp $R/work/chk/CHECK_RESULTS.jsonl $R/exp_out/CHECK_RESULTS.jsonl 2>/dev/null
tail -3 $R/exp_out/main.stdout
# negative controls on the first class of the shard
T=$(python3 -c "import re,sys; print(open('shard_regex/$K.txt').read()[2:].split('|')[0])")
python3 - "$T" $R/work <<'PY'
import sys, json, gzip, os, shutil
t, w = sys.argv[1], sys.argv[2]
R = [json.loads(l) for l in open(f'{w}/run_merged/results94m.jsonl')]
A = [dict(r, cnf_sha256='0' * 64) if r['tag'] == t else r for r in R]            # negA: the record names another CNF hash
open(f'{w}/results_negA.jsonl', 'w').write(''.join(json.dumps(r) + '\n' for r in A))
os.makedirs(f'{w}/lazy_negB', exist_ok=True)                                      # negB: the lazy list gets one extra 9-set
lz = json.load(gzip.open(f'{w}/run_merged/{t}.lazy.json.gz'))
lz2 = lz + [{'kind': 9, 'W': [0, 1, 2, 3, 4, 5, 6, 7, 8]}] if not lz else lz[:-1]
json.dump(lz2, gzip.open(f'{w}/lazy_negB/{t}.lazy.json.gz', 'wt'))
json.dump({'tag': t, 'lazy_items': len(lz), 'negB': 'one item removed' if lz else 'one 9-set added'}, open(f'{w}/neg_info.json', 'w'))
PY
cp $R/work/neg_info.json $R/exp_out/
CAD=$R/bin/cadical CAKE=$R/bin/cake_lpr python3 -I -B check_all94m.py classes94m.json $R/work/results_negA.jsonl $R/work/run_merged $R/work/negA 1 "^($T)\$" > $R/exp_out/negA.stdout 2>&1; echo $? > $R/exp_out/negA.exit; cp $R/work/negA/CHECK_RESULTS.jsonl $R/exp_out/negA_CHECK_RESULTS.jsonl 2>/dev/null
CAD=$R/bin/cadical CAKE=$R/bin/cake_lpr python3 -I -B check_all94m.py classes94m.json $R/work/run_merged/results94m.jsonl $R/work/lazy_negB $R/work/negB 1 "^($T)\$" > $R/exp_out/negB.stdout 2>&1; echo $? > $R/exp_out/negB.exit; cp $R/work/negB/CHECK_RESULTS.jsonl $R/exp_out/negB_CHECK_RESULTS.jsonl 2>/dev/null
echo "exits: main $(cat $R/exp_out/main.exit) negA $(cat $R/exp_out/negA.exit) negB $(cat $R/exp_out/negB.exit)"
