#!/bin/bash
# codespace/run.sh — started by .devcontainer postStartCommand on every codespace (re)start. Producer-side only.
# Runs worker.sh ccc (unchanged pipeline, pinned binaries checked by SHA256SUMS) for each line of codespace/jobs.txt,
# resuming from /workspaces/cs/out_<folder> after a stop; a watcher pushes every newly recorded proof to branch
# cs-<folder> (90 MB parts + sha256) so it can be audited independently. ORIGINAL_MODEL_FOUND stops everything.
R=$(cd "$(dirname "$0")/.." && pwd); W=${CS_DIR:-$HOME/cs}; mkdir -p $W || W=$R/.cs; mkdir -p $W; exec >> $W/run.log 2>&1; export CS_DIR=$W
echo "== start $(date -u +%FT%TZ) nproc=$(nproc)"
git -C $R pull -q --ff-only origin main || true
beat() { S=$W/beat_git; rm -rf $S; mkdir -p $S && ( cd $S && git init -q && { echo "$1"; date -u +%FT%TZ; id; echo "W=$W R=$R"; nproc; free -m; tail -20 $W/run.log; } > status.txt 2>&1 && git add status.txt && git -c user.name=codespace -c user.email=codespace@users.noreply.github.com commit -q -m "codespace status" && git push -q -f $(git -C $R remote get-url origin) HEAD:refs/heads/cs-status ) || echo "beat push failed"; }
beat "run.sh started"
cd $R && sha256sum -c --quiet SHA256SUMS || { echo "SHA256SUMS FAILED"; exit 1; }
chmod +x bin/* worker.sh
[ -x $W/venv/bin/python3 ] || { python3 -m venv $W/venv && $W/venv/bin/pip install -q "python-sat==1.9.dev21" numpy networkx; }
export PATH=$W/venv/bin:$PATH
grep -v '^#' codespace/jobs.txt | while read F FF PAR TAGS; do
  [ -z "$F" ] && continue
  mkdir -p $W/jobs/$F; printf '%s\n' $TAGS > $W/jobs/$F/h01.txt
  pgrep -f "worker.sh ccc $W/jobs/$F/" >/dev/null && continue
  setsid nohup env FORMULAS_FILE=$FF CUBE_DEPTH=7 PAR=$PAR WINDOW=604800 PREV=$W/none bash worker.sh ccc $W/jobs/$F/h01.txt $W/out_$F > $W/out_$F.nohup 2>&1 &
  echo "started $F ($TAGS)"
done
beat "workers launched"
pgrep -f codespace/watch.sh >/dev/null || CS_DIR=$W setsid nohup bash $R/codespace/watch.sh > /dev/null 2>&1 &
