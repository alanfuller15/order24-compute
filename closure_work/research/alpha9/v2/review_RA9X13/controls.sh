#!/bin/bash
cd "$(dirname "$0")"; ulimit -v 1500000
for opts in "--seed D --q 4 --mult 3" "--seed D --floorthr 10" "--seed D --q 4 --mult 3 --floorthr 10"; do
  while [ $(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo) -lt 2000 ]; do sleep 10; done
  echo "=== $opts" >> controls_out.txt
  /usr/bin/time -f "cpu %U s" nice -n 19 python3 -I search415c.py $opts >> controls_out.txt 2>&1
done
echo DONE >> controls_out.txt
