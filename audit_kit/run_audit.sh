#!/bin/bash
# run_audit.sh M TAGS_REGEX — runs the PINNED checker audit_kit/l<M>/code/gcert<M>.py, unmodified, on the records of the
# downloaded producer artifact (in/results.jsonl, in/proofs/) whose tag fully matches TAGS_REGEX; then two negative
# controls that must exit 1. Everything it produces goes to aout/ (uploaded as an artifact). No producer code is used.
set -u
M=$1; RX=$2; ROOT=$PWD; K=$ROOT/audit_kit/l$M; O=$ROOT/aout; mkdir -p $O
F=$K/formulas${M}_c$((M-23)).json; G=$K/code/gcert$M.py
date -u +%FT%TZ > $O/start.txt
python3 -I -c 'import json,re,sys; rx=re.compile(sys.argv[2]); open(sys.argv[3],"w").writelines(l for l in open(sys.argv[1]) if l.strip() and rx.fullmatch(json.loads(l)["tag"]))' $ROOT/in/results.jsonl "$RX" $O/records.jsonl
echo "$RX" > $O/regex.txt; wc -l < $O/records.jsonl > $O/n_records.txt
(cd $ROOT/in && sha256sum results.jsonl proofs/*) > $O/inputs.sha256; sha256sum $O/records.jsonl $G $K/code/*.py $F $HOME/tools/cake_lpr/cake_lpr >> $O/inputs.sha256
( while true; do echo "$(date -u +%T) $(free -m | awk '/Mem:/{print "used="$3" avail="$7}') $(for p in $(pgrep -f CML_HEAP_SIZE); do grep VmHWM /proc/$p/status 2>/dev/null | tr -s ' '; done | tr '\n' ' ')"; sleep 5; done ) > $O/mem.log 2>&1 &
SAMP=$!
run() { # run NAME RECORDS PROOFS
  ( cd $K && /usr/bin/time -v -o $O/$1.time env -i PATH=/usr/bin:/bin HOME=$HOME PARTIAL_RECORDS=1 python3 -I -B $G $F $2 $3 $O/run_$1 1 "$RX" > $O/$1.stdout 2> $O/$1.stderr ); echo $? > $O/$1.exit; }
run main $O/records.jsonl $ROOT/in/proofs
T=$(python3 -I -c 'import json,sys; print(json.loads(open(sys.argv[1]).readline())["tag"])' $O/records.jsonl)
# negative control (a): one lazy item of the first record changed to a different valid set (or one item added if empty); proofs untouched
python3 -I -c '
import json,sys,itertools
r=json.loads(open(sys.argv[1]).readline()); L=r["lazy"]; have={tuple(x["W"]) for x in L}
if L:
    x=L[-1]; W=list(x["W"])
    for i,v in itertools.product(range(len(W)),range(24)):
        if v in W: continue
        Z=sorted(W[:i]+[v]+W[i+1:])
        if tuple(Z) not in have: x["W"]=Z; break
else:
    L.append({"kind":12,"W":list(range(12))})
open(sys.argv[2],"w").write(json.dumps(r)+"\n")' $O/records.jsonl $O/records_negA.jsonl
RXsave=$RX; RX="^($T)$"
run negA $O/records_negA.jsonl $ROOT/in/proofs
# negative control (b): 9,000,000-byte prefix of the first record's proof with byte 4,500,000 flipped; record untouched
mkdir -p $ROOT/negB && head -c 9000000 $ROOT/in/proofs/$T.lrat.xz > $ROOT/negB/$T.lrat.xz && python3 -I -c '
import sys; p=sys.argv[1]; b=bytearray(open(p,"rb").read()); b[4500000]^=1; open(p,"wb").write(b)' $ROOT/negB/$T.lrat.xz
python3 -I -c 'import json,sys; [sys.stdout.write(l) for l in open(sys.argv[1]) if json.loads(l)["tag"]==sys.argv[2]]' $O/records.jsonl $T > $O/records_negB.jsonl
sha256sum $O/records_negA.jsonl $O/records_negB.jsonl $ROOT/negB/$T.lrat.xz >> $O/inputs.sha256
run negB $O/records_negB.jsonl $ROOT/negB
RX=$RXsave
kill $SAMP; date -u +%FT%TZ > $O/end.txt
grep -h . $O/*.exit | paste -sd' ' > $O/exits.txt; cat $O/main.stdout $O/exits.txt
