#!/bin/bash
# worker.sh MODE CHUNKFILE OUTDIR — one GitHub Actions job (4 cores, ~16 GB, 6 h cap).
#   MODE=grun: grun90.py (CEGAR search + CaDiCaL LRAT proof + cake_lpr self-check) on the chunk's tags, 4 workers.
#   MODE=ccc : ccc90.py (cube-and-conquer) on the chunk's tags, up to 4 at a time; state in OUTDIR/cube/TAG (resumable).
# Seeds: ckpt/*.jsonl lines and ckpt/<wave>.jsonl.xz (the chunk's wave; lazy items carried from a higher layer, see code/make_packs.py)
# and other ckpt lines (records or checkpoints with "tag" and "lazy") are copied into OUTDIR/lazy_ckpt.jsonl / used as
# ccc seeds. Nothing here is trusted: every record is re-checked by gcert90d.py (pinned) by an independent auditor.
set -u
MODE=$1; CHUNK=$2; OUT=$3; R=$(cd $(dirname $0) && pwd); FORMULAS=$R/data/${FORMULAS_FILE:-formulas89_c66.json}
if [ "${FORMULAS_FILE:-}" = auto ]; then M=$(basename $CHUNK .txt | tr -dc 0-9); FORMULAS=$R/data/formulas${M}_c$((M-23)).json; fi   # chunk m<layer>.txt
export MASKS12=$R/data/masks12.npy CAD=${CAD_BIN:-$R/bin/cadical} TRIM=${TRIM_BIN:-$R/bin/lrat-trim} CAKE=${CAKE_BIN:-$R/bin/cake_lpr}
export PROOFS=$OUT/proofs CAKE_LOCK=$OUT/.cake.lock CAKE_SLOTS=2
mkdir -p $OUT/proofs; cp $CHUNK $OUT/chunk.txt
{ cat $R/ckpt/*.jsonl 2>/dev/null; xz -dc $R/ckpt/$(basename $(dirname $CHUNK)).jsonl.xz 2>/dev/null; } | python3 -c "
import sys,json
tags=set(l.strip() for l in open('$CHUNK') if l.strip())
ck=open('$OUT/seed_ckpt.jsonl','w'); pa=open('$OUT/seed_partial.jsonl','w'); sd=open('$OUT/seed.jsonl','w')
for l in sys.stdin:
    try: d=json.loads(l)
    except Exception: continue
    if not isinstance(d,dict) or d.get('tag') not in tags: continue
    if isinstance(d.get('lazy'),list): ck.write(json.dumps({'tag':d['tag'],'lazy':d['lazy']})+chr(10)); sd.write(json.dumps({'tag':d['tag'],'lazy':d['lazy']})+chr(10))
    elif isinstance(d.get('items'),list): pa.write(l if l.endswith(chr(10)) else l+chr(10)); sd.write(json.dumps({'tag':d['tag'],'items':d['items']})+chr(10))
"
T0=$(date +%s); HARD=$(( T0 + ${WINDOW:-20400} ))
if [ "$MODE" = grun ]; then
  cp $OUT/seed_ckpt.jsonl $OUT/lazy_ckpt.jsonl; cp $OUT/seed_partial.jsonl $OUT/lazy_partial.jsonl
  TODO_FILE=$CHUNK CONF=20000 GROW=4 CAD_OPTS= STOP_AFTER=${STOP_AFTER:-15000} \
    timeout --signal=KILL $(( HARD - $(date +%s) )) python3 -I -B $R/code/${GRUN:-grun90.py} $FORMULAS $OUT 4 14400 > $OUT/grun.log 2>&1
  echo "grun exit $?" >> $OUT/grun.log
else
  run1() { T=$1; mkdir -p $OUT/cube/$T; grep "\"$T\"" $OUT/seed.jsonl > $OUT/cube/seed_$T.jsonl || true
    S=""; [ -s $OUT/cube/seed_$T.jsonl ] && S=$OUT/cube/seed_$T.jsonl
    ENCODER=cegar90c CONF=20000 GROW=16 CAD_OPTS= DEADLINE=$(( HARD - 300 )) CUBE_DEPTH=${CUBE_DEPTH:-4} EXT_TIMEOUT=${EXT_TIMEOUT:-1500} PYSAT_CAP=${PYSAT_CAP:-240} \
      timeout --signal=KILL $(( HARD - $(date +%s) )) python3 -I -B $R/code/ccc90.py $FORMULAS $T $OUT/cube/$T $OUT $S > $OUT/cube/$T.log 2>&1
    echo "$T ccc exit $?" >> $OUT/ccc.log; }
  export -f run1; export OUT HARD R FORMULAS   # FORMULAS: ccc90.py argv[1] (was missing: every GHA ccc run failed with shifted arguments)
  # Chaining (workflow input prev_run): PREV holds the artifact of this chunk from an earlier ccc job. A formula recorded
  # there is skipped (its record and proof are in that artifact); otherwise its cube state folder (tree, items, proved
  # cube segments) is copied in and ccc90.py resumes from it, so no work is lost at the 6-h job limit.
  if [ "$MODE" = merge ]; then   # join the shard states of each tag (ccc_merge.py), then stitch them with ccc90.py
    unset CUBE_SHARD; PREV=/nonexistent
    for T in $(grep -v '^$' $CHUNK); do
      ENCODER=cegar90c python3 -I -B $R/code/ccc_merge.py $FORMULAS $T $OUT/cube/$T $(ls -d $R/shards/*/cube/$T 2>/dev/null) >> $OUT/ccc.log 2>&1 \
        || echo "$T merge FAILED" >> $OUT/ccc.log
    done
  fi
  PREV=${PREV:-$R/prev}; : > $OUT/todo.txt
  for T in $(grep -v '^$' $CHUNK); do
    if [ "$MODE" = merge ] && [ ! -f $OUT/cube/$T/tree.json ]; then echo "$T: no merged state: skipped" >> $OUT/ccc.log; continue; fi
    if [ -f $PREV/results.jsonl ] && python3 -c "import json,sys; sys.exit(0 if any(json.loads(l).get('tag')==sys.argv[1] for l in open(sys.argv[2]) if l.strip()) else 1)" $T $PREV/results.jsonl; then
      echo "$T recorded in the previous job: skipped" >> $OUT/ccc.log; continue; fi
    if [ -f $PREV/cube/$T/tree.json ]; then mkdir -p $OUT/cube; cp -r $PREV/cube/$T $OUT/cube/$T; rm -rf $OUT/cube/$T/work
      echo "$T resumed from the previous job's state ($(ls $PREV/cube/$T | wc -l) files)" >> $OUT/ccc.log; fi
    echo $T >> $OUT/todo.txt
  done
  xargs -P ${PAR:-4} -I{} bash -c 'run1 {}' < $OUT/todo.txt
fi
ls $OUT/proofs | wc -l > $OUT/n_proofs.txt
