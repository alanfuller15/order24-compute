#!/bin/bash
# RA9X12 certify: for each CNF: wait >= 2000 MB available; CaDiCaL (repo binary) with binary LRAT, nice 19,
# timeout 1800 s; if exit 20, cake_lpr; record sha256 of CNF, proof, checker output; delete proof > 500 MB.
# Usage: certify.sh LOG cnf1 cnf2 ...   (one process at a time)
SP=/tmp/claude-0/-home-claude/4a72079e-a9db-5726-b10c-aeb759ad214f/scratchpad
B=$SP/gh/order24-compute/bin
LOG=$1; shift
for f in "$@"; do
  while [ "$(free -m | awk '/Mem/{print $7}')" -lt 2000 ]; do sleep 20; done
  p=${f%.cnf}.lrat; o=${f%.cnf}.cadical.txt; k=${f%.cnf}.cake.txt
  s0=$(date +%s)
  /usr/bin/time -f "cpu_user %U wall %e maxrss_kb %M" timeout 1800 nice -n 19 $B/cadical -q --lrat=true --binary=true "$f" "$p" > "$o" 2>&1
  ce=$?; s1=$(date +%s)
  line="$(basename $f) cnf_sha256=$(sha256sum "$f" | cut -c1-64) cadical_exit=$ce solve_s=$((s1-s0)) [$(tail -1 $o)]"
  if [ $ce -eq 20 ]; then
    psz=$(stat -c %s "$p"); psha=$(sha256sum "$p" | cut -c1-64)
    while [ "$(free -m | awk '/Mem/{print $7}')" -lt 2000 ]; do sleep 20; done
    /usr/bin/time -f "cpu_user %U wall %e maxrss_kb %M" timeout 1800 nice -n 19 $B/cake_lpr --CML_HEAP_SIZE=${CAKE_HEAP:-1000} --CML_STACK_SIZE=256 "$f" "$p" > "$k" 2>&1
    ke=$?; s2=$(date +%s)
    ver=$(grep -x 's VERIFIED UNSAT' "$k" >/dev/null && echo VERIFIED || echo NOT_VERIFIED)
    line="$line proof_bytes=$psz proof_sha256=$psha cake_exit=$ke cake=$ver check_s=$((s2-s1)) cake_out_sha256=$(sha256sum "$k" | cut -c1-64)"
    if [ $psz -gt 500000000 ]; then rm -f "$p"; line="$line proof_deleted"; fi
  fi
  echo "$line" >> "$LOG"
done
echo DONE >> "$LOG"
