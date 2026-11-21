#!/bin/bash
# non-vacuity sweep for the --sides model: per case, thresholds 0,4,6,8,10,11 ascending; stop at the first UNSAT.
cd "$(dirname "$0")"
for bh in "0 0" "1 0" "1 1" "2 0" "2 1" "2 2" "3 0" "3 1" "3 2" "3 3"; do
  set -- $bh
  for T in 0 4 6 8 10 11; do
    ./run.sh ctl_sides_b$1_h$2_thr$T $1 --nocore --sides $2 --thr $T
    if grep -q '"survivors": 0' ctl_sides_b$1_h$2_thr${T}_out.txt; then echo "b=$1 h=$2: thr $T UNSAT" >> ctl_sweep_summary.txt; break; fi
    if grep -q 'control candidate' ctl_sides_b$1_h$2_thr${T}_out.txt; then echo "b=$1 h=$2: thr $T SAT (candidate_b$1_thr${T}_bip_sides$2.json)" >> ctl_sweep_summary.txt; else echo "b=$1 h=$2: thr $T OTHER (see out)" >> ctl_sweep_summary.txt; break; fi
  done
done
