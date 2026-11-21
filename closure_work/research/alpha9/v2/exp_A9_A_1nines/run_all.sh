#!/bin/bash
# exp:A9-A-1nines runner: one process at a time, nice 19, ulimit -v 1500000, <= 1800 s wall per profile,
# waits for >= 2000 MB available before each run.
cd "$(dirname "$0")"
for m in "$@"; do
  while [ "$(free -m | awk '/Mem/{print $7}')" -lt 2000 ]; do echo "waiting for memory ($(free -m | awk '/Mem/{print $7}') MB)"; sleep 30; done
  echo "=== m=$m start $(date -u +%FT%TZ) avail $(free -m | awk '/Mem/{print $7}') MB"
  ( ulimit -v 1500000; /usr/bin/time -f "cpu_user %U cpu_sys %S wall %e maxrss_kb %M" timeout 1800 nice -n 19 python3 model_1nines.py $m ) > model_m${m}_out.txt 2>&1
  echo "exit $? : $(tail -2 model_m${m}_out.txt | tr '\n' ' ')"
done
