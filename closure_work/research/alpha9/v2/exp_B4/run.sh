#!/bin/bash
# exp:B4 runner: one process at a time, nice 19, ulimit -v 1500000, <= 1800 s wall per run,
# waits for >= 2000 MB available before each run. Usage: run.sh OUTNAME b [model args...]
cd "$(dirname "$0")"
out=$1; shift
while [ "$(free -m | awk '/Mem/{print $7}')" -lt 2000 ]; do echo "waiting for memory ($(free -m | awk '/Mem/{print $7}') MB)" >> runner_log.txt; sleep 30; done
echo "=== $out ($*) start $(date -u +%FT%TZ) avail $(free -m | awk '/Mem/{print $7}') MB" >> runner_log.txt
( ulimit -v 1500000; /usr/bin/time -f "cpu_user %U cpu_sys %S wall %e maxrss_kb %M" timeout 1800 nice -n 19 python3 model_B4.py "$@" ) > ${out}_out.txt 2>&1
echo "exit $? : $(tail -2 ${out}_out.txt | tr '\n' ' ')" >> runner_log.txt
