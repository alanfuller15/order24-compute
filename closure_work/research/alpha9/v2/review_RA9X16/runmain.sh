#!/bin/bash
ulimit -v 1500000
cd "$(dirname "$0")"
for a in "2 2 --sym" "2 3 --sym" "2 2" "2 3" "1 2" "1 3"; do
  f=main_$(echo $a | tr ' ' '_' | tr -d '-')_out.txt
  /usr/bin/time -f "cpu_user %U wall %e maxrss_kb %M" nice -n 19 ./rv16c $a > $f 2>&1
done
echo ALLDONE
