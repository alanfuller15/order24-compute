#!/bin/bash
# exp/rep94m.sh K N [MINUTES] [BUDGET_S]: shard K of N of the (6,7^2,8^21) replication (f94m format: cegar_shape.py + CaDiCaL 3.0.1
# LRAT + cake_lpr "s VERIFIED UNSAT"). Producer-side: results + lazy lists go to exp_out/run; they count for nothing until an
# independent replay (check_all94m.py) has re-checked them.
set -u; K=$1; N=$2; MIN=${3:-330}; B=${4:-1800}; R=$PWD
mkdir -p exp/lowcheck exp_out/run; cp data/masks12.npy exp/lowcheck/masks12.npy
sha256sum exp/rep94m/cegar_shape.py exp/rep94m/run94m.py exp/rep94m/classes94m.json bin/cadical bin/cake_lpr > exp_out/inputs.sha256
cd exp/rep94m
CAD=$R/bin/cadical CAKE=$R/bin/cake_lpr CAKE_FAST=1 SHARD=$K/$N DONE=$PWD/done_local.txt timeout --signal=INT $(( MIN * 60 )) python3 -I -B run94m.py classes94m.json $R/exp_out/run 4 $B
echo "driver exit $?"
cd $R/exp_out/run; rm -f -- *.cnf *.lrat *.lazy.json .cake.lock 2>/dev/null; wc -l results94m.jsonl; grep -c 's VERIFIED UNSAT' results94m.jsonl; ls | wc -l
