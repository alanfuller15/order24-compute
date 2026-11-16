#!/bin/bash
# worker.sh MODE CHUNKFILE OUTDIR — one GitHub Actions job (4 cores, ~16 GB, 6 h cap).
#   MODE=grun: grun90.py (CEGAR search + CaDiCaL LRAT proof + cake_lpr self-check) on the chunk's tags, 4 workers.
#   MODE=ccc : ccc90.py (cube-and-conquer) on the chunk's tags, up to 4 at a time; state in OUTDIR/cube/TAG (resumable).
# Seeds: ckpt/*.jsonl lines (records or checkpoints with "tag" and "lazy") are copied into OUTDIR/lazy_ckpt.jsonl / used as
# ccc seeds. Nothing here is trusted: every record is re-checked by gcert90d.py (pinned) by an independent auditor.
set -u
MODE=$1; CHUNK=$2; OUT=$3; R=$(cd $(dirname $0) && pwd); FORMULAS=$R/data/${FORMULAS_FILE:-formulas89_c66.json}
export MASKS12=$R/data/masks12.npy CAD=$R/bin/cadical TRIM=$R/bin/lrat-trim CAKE=$R/bin/cake_lpr
export PROOFS=$OUT/proofs CAKE_LOCK=$OUT/.cake.lock CAKE_SLOTS=2
mkdir -p $OUT/proofs; cp $CHUNK $OUT/chunk.txt
cat $R/ckpt/*.jsonl 2>/dev/null | python3 -c "
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
    timeout --signal=KILL $(( HARD - $(date +%s) )) python3 -I -B $R/code/grun90.py $FORMULAS $OUT 4 14400 > $OUT/grun.log 2>&1
  echo "grun exit $?" >> $OUT/grun.log
else
  run1() { T=$1; mkdir -p $OUT/cube/$T; grep "\"$T\"" $OUT/seed.jsonl > $OUT/cube/seed_$T.jsonl || true
    S=""; [ -s $OUT/cube/seed_$T.jsonl ] && S=$OUT/cube/seed_$T.jsonl
    ENCODER=cegar90c CONF=20000 GROW=16 CAD_OPTS= DEADLINE=$(( HARD - 300 )) CUBE_DEPTH=${CUBE_DEPTH:-4} EXT_TIMEOUT=1500 PYSAT_CAP=240 \
      timeout --signal=KILL $(( HARD - $(date +%s) )) python3 -I -B $R/code/ccc90.py $FORMULAS $T $OUT/cube/$T $OUT $S > $OUT/cube/$T.log 2>&1
    echo "$T ccc exit $?" >> $OUT/ccc.log; }
  export -f run1; export OUT HARD R
  grep -v '^$' $CHUNK | xargs -P ${PAR:-4} -I{} bash -c 'run1 {}'
fi
ls $OUT/proofs | wc -l > $OUT/n_proofs.txt
