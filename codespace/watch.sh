#!/bin/bash
# watch.sh: every 5 min, push newly recorded proofs to branch cs-<folder>; stop all on ORIGINAL_MODEL_FOUND.
R=$(cd "$(dirname "$0")/.." && pwd); W=${CS_DIR:-$HOME/cs}; exec >> $W/watch.log 2>&1
while true; do
  if grep -rqs ORIGINAL_MODEL_FOUND $W/out_*/results.jsonl $W/out_*/cube/*/ 2>/dev/null; then echo "ORIGINAL_MODEL_FOUND $(date -u)"; pkill -f worker.sh; pkill -f ccc90.py; exit 0; fi
  for O in $W/out_*; do F=${O##*/out_}; [ -f $O/results.jsonl ] || continue
    for T in $(python3 -c 'import json,sys; [print(json.loads(l)["tag"]) for l in open(sys.argv[1]) if l.strip()]' $O/results.jsonl); do
      [ -f $W/pushed_$T ] && continue; P=$O/proofs/$T.lrat.xz; [ -f $P ] || continue
      G=$W/git_$F; [ -d $G ] || git clone -q --depth 1 $(git -C $R remote get-url origin) $G
      ( cd $G && git checkout -q -B cs-$F && mkdir -p codex/$F && grep "\"$T\"" $O/results.jsonl > codex/$F/$T.result.json && split -b 90M -d -a 3 $P codex/$F/$T.lrat.xz.part && (cd $O/proofs && sha256sum $T.lrat.xz) > codex/$F/$T.sha256 && cp $O/cube/$T/log.jsonl codex/$F/$T.log.jsonl && git add codex/$F && git -c user.name=codespace -c user.email=codespace@users.noreply.github.com commit -q -m "codespace: recorded $T ($F)" && git push -q -f origin cs-$F && touch $W/pushed_$T && echo "pushed $T $(date -u)" )
    done; done
  i=$((${i:-0}+1)); if true; then   # heartbeat every 5 min: one-commit branch cs-status
    S=$W/status_git; rm -rf $S; mkdir -p $S && cd $S && git init -q && { date -u +%FT%TZ; uptime; nproc; free -m; df -h /workspaces | tail -1; pgrep -fa "worker.sh|ccc90" | cut -c1-160; for L in $W/out_*/cube/*.log; do echo "== $L"; tail -2 $L; done; for J in $W/out_*/cube/*/log.jsonl; do echo "$J closed=$(grep -c '"closed"' $J)"; done; tail -5 $W/watch.log; } > status.txt 2>&1 && git add status.txt && git -c user.name=codespace -c user.email=codespace@users.noreply.github.com commit -q -m "codespace status $(date -u +%FT%TZ)" && git push -q -f $(git -C $R remote get-url origin) HEAD:refs/heads/cs-status-${CODESPACE_NAME:-x}; cd /; fi
  sleep 300
done
