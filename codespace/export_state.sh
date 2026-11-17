#!/bin/bash
# codespace/export_state.sh FOLDER TAG [FOLDER TAG ...] — producer side. Before a codespace is lost (quota, deletion), save the cube
# state of a formula so another worker can resume it: stop that job, tar its state folder (without work/), split into 90 MB parts and
# push them with their sha256 to branch cs-state-<FOLDER>-<last 4 of TAG>. Resume elsewhere: fetch the branch, `sha256sum -c SHA256`,
# `cat TAG.tar.* | tar -xf - -C OUT` (gives OUT/cube/TAG), then run worker.sh ccc with that OUT as usual.
R=$(cd "$(dirname "$0")/.." && pwd); W=${CS_DIR:-$HOME/cs}; URL=$(git -C $R remote get-url origin)
while [ $# -ge 2 ]; do F=$1; T=$2; shift 2
  pkill -f "worker.sh ccc $W/jobs/$F/" ; pkill -f "ccc90.py.*$T .*out_$F" ; pkill -f "ccc90.py.*$T"; sleep 3
  [ -f $W/out_$F/cube/$T/tree.json ] || { echo "NO STATE: $F $T"; continue; }
  S=$W/state_git_$F; rm -rf $S; mkdir -p $S && cd $S && git init -q || continue
  tar -C $W/out_$F -cf - --exclude=work cube/$T | split -b 90M - $T.tar. && sha256sum $T.tar.* > SHA256
  python3 -c "import json;t=json.load(open('$W/out_$F/cube/$T/tree.json'));print('$T', len(t['done']),'closed',len(t['open']),'open')" > INFO.txt
  git add -A && git -c user.name=codespace -c user.email=codespace@users.noreply.github.com commit -qm "cube state of $T from codespace job $F ($(cat INFO.txt))" \
    && git push -q -f $URL HEAD:refs/heads/cs-state-$F-${T: -4} && echo "PUSHED cs-state-$F-${T: -4}: $(du -sm . | cut -f1) MB, $(cat INFO.txt)" || echo "PUSH FAILED: $F $T"
  cd $R
done
