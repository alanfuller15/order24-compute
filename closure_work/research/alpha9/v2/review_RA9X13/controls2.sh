#!/bin/bash
cd "$(dirname "$0")"; ulimit -v 1500000
until grep -q DONE controls_out.txt; do sleep 10; done
for opts in "--seed D --q 99 --exacty" "--seed R --q 99 --exacty"; do
  while [ $(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo) -lt 2000 ]; do sleep 10; done
  echo "=== $opts" >> controls2_out.txt
  /usr/bin/time -f "cpu %U s" nice -n 19 python3 -I search415c.py $opts >> controls2_out.txt 2>&1
done
echo DONE >> controls2_out.txt
