#!/bin/bash
# lanes/supervise.sh N - self-healing supervisor for Codex lane N (producer side; nothing here is trusted by the audit).
# Start:  cd /workspace/r && setsid nohup bash lanes/supervise.sh N > /dev/null 2>&1 < /dev/null &   (safe to run twice)
# Every SV_TICK (60) s:
#   1. git fetch origin main + merge --ff-only (main only); sha256sum -c SHA256SUMS, and lanes/supervise.sh and worker.sh must be pinned there.
#      On failure nothing is started; MODE run stops the solvers once the failure has lasted SV_SHA_GRACE (120) s
#      (never one that is stitching its final proof); MODE fill stops nothing and raises an ALERT. A changed, verified
#      supervise.sh that passes bash -n replaces this process (exec, same pid) without touching the solvers.
#   2. lanes/assign/N.txt: lines TAG FORMULAS_FILE PUBLISHER_BRANCH [OUTDIR|-] [CUBE_DEPTH=..] [EXT_TIMEOUT=..]
#      [PYSAT_CAP=..] [SEED_WAVE=..]; 'ENV K=V ..' sets lane defaults; 'MODE run' (default) or 'MODE fill'.
#      run : start missing assigned solvers (resuming from their state folder), stop unassigned ones (folders kept),
#            restart assigned ones when lanes/VERSION changes.
#      fill: start missing assigned solvers into free slots only; never stop or restart anything.
#   3. heartbeat: one-commit branch lane-status-N (status.txt, line 2 ALIVE=<ccc90.py processes>) every SV_BEAT (300) s
#      and on any change. Publisher: every UNSAT record in a known OUTDIR (assigned tag or not) goes to its branch as
#      codex/<wave>/<TAG>.* (ingest_branch.py layout), appended on top of the branch (never force), < 2 GB per push.
#   4. ORIGINAL_MODEL_FOUND in any known OUTDIR (ORIGINAL_MODEL_FOUND.json, a results line, a solver log line, or
#      'TAG ccc exit 2' in ccc.log): every other solver is stopped at once (the finder gets 30 s to exit by itself),
#      the evidence is pushed, and nothing starts until a person removes $SV_DIR/HALT_OMF. A tag with OMF evidence is
#      never started again by this script.
# Known OUTDIRs: those of running solvers, of $SV_DIR/run/*.out, explicit assignment OUTDIRs, and $SV_BASE/*/ with cube/.
# Gentle stops: a solver is killed right after its log.jsonl gains an event (the tree is saved before the event is
# written), or after SV_SOFT_MAX (1800) s; one whose tree has no open cube is never stopped for a retarget or upgrade.
# State folders are never deleted or moved.
# Encoders: an assignment entry is a (TAG, ENCODER) pair, ENCODER=cegar90c (v7, default) or cegar90e (v9); a tag may
# be listed once per encoder, each pair its own solver, folder and slot. A state folder is resumed only by its own
# encoder (tree.json "encoder"; ccc90.py refuses others); a v9 pair without a v9 folder starts in $SV_BASE/out_sv_TAG_v9.
# 'ENV V7_FRESH=no': a v7 pair is only resumed from an existing v7 folder, never started fresh (skipped with a NOTE).
# A solver's encoder: ENCODER in /proc/PID/environ, else its tree's label. Free slots go to stitch-ready pairs (tree
# with no open cube) first, then to the pairs in file order.
# 'STOP TAG [ENCODER]': stop that tag's in-scope solver(s) at a cube boundary (never a stitching one), never restart the
# tag, keep its folders, publish its record: THE ONLY WAY MODE fill STOPS A SOLVER.
set -u
N=${1:-}; [[ $N =~ ^[0-9]{1,3}$ ]] || { echo "usage: supervise.sh LANE_NUMBER"; exit 2; }
SELF=$(cd "$(dirname "$0")" && pwd)/$(basename "$0"); R=$(cd "$(dirname "$0")/.." && pwd)
BASE=${SV_BASE:-/workspace}; W=${SV_DIR:-$BASE/sv}; SCOPE=${SV_SCOPE-$BASE/}
isnum() { [[ ${1:-} =~ ^[0-9]+$ ]]; }
envnum() { isnum "$2" && echo "$2" || echo "$3"; }   # NAME VALUE DEFAULT
TICK=$(envnum TICK "${SV_TICK:-}" 60); BEAT=$(envnum BEAT "${SV_BEAT:-}" 300); MAXS=$(envnum MAX "${SV_MAX:-}" 3)
SOFT_MAX=$(envnum SOFT "${SV_SOFT_MAX:-}" 1800); SHA_GRACE=$(envnum GRACE "${SV_SHA_GRACE:-}" 120)
WINDOW=$(envnum WIN "${SV_WINDOW:-}" 86400); BATCH=$(envnum BATCH "${SV_BATCH:-}" 15); FAST=$(envnum FAST "${SV_FASTFAIL:-}" 180)
HOLD=$(envnum HOLD "${SV_HOLD:-}" 1800); MAXFAIL=$(envnum MAXFAIL "${SV_MAXFAIL:-}" 3); PART=${SV_PART:-90M}
TAGRE='^L[0-9]{2}_s[0-9]+a[0-9]+b[0-9]+c[0-9]+_[0-9]{4}$'
mkdir -p "$W/run" "$W/pub" "$W/jobs" || exit 2
LOG=$W/supervise.log
say() { echo "$(date -u +%FT%TZ) $*" >> "$LOG" 2>/dev/null; }
num() { local v; v=$(cat "$1" 2>/dev/null); v=${v%% *}; isnum "$v" && echo "$v" || echo "${2-0}"; }   # FILE DEFAULT
pstart() { sed 's/^.*) //' "/proc/$1/stat" 2>/dev/null | awk '{print $20}'; }   # field 22: start time in ticks

# ---- one instance per lane. flock guards only the check-and-claim (no child inherits a held lock). The pid file holds
# pid + start time, so a recycled pid (container restart) is not mistaken for a running supervisor.
exec 9>>"$W/supervise.lock"; flock -w 30 9 || { echo "supervise.sh $N: lock busy"; exit 1; }
OLD=$(num "$W/supervise.pid" ""); OLDST=$(num "$W/supervise.pidstart" "")
if [ -n "$OLD" ] && [ "$OLD" != $$ ] && [ -n "$OLDST" ] && [ "$(pstart "$OLD")" = "$OLDST" ] \
   && tr '\0' ' ' 2>/dev/null < "/proc/$OLD/cmdline" | grep -Eq "supervise\.sh $N( |$)"; then
  echo "supervise.sh $N already running (pid $OLD)"; exit 0; fi
echo $$ > "$W/supervise.pid"; pstart $$ > "$W/supervise.pidstart"; exec 9>&-

PY_INFO='
import sys, json, os
# stdin: TAG STATEDIR per line -> TAG closed open logsize encoder ("-" without a tree; a tree without the key is v7)
for l in sys.stdin:
    p = l.split()
    if len(p) < 2: continue
    t, st = p[:2]; c = o = "-"; e = "-"
    try:
        tr = json.load(open(os.path.join(st, "tree.json"))); c = str(len(tr["done"])); o = str(len(tr["open"])); e = str(tr.get("encoder", "v7"))
    except Exception:
        if os.path.isdir(st): o = "initializing"
    try: sz = os.path.getsize(os.path.join(st, "log.jsonl"))
    except Exception: sz = 0
    print(t, c, o, sz, e)
'
PY_RECS='
import sys, json, os, re
# argv: CACHE OUTDIR... -> "TAG OUTDIR ENC" for every UNSAT record line (cached by size and mtime of results.jsonl)
cache_p = sys.argv[1]; rx = re.compile(r"^L[0-9]{2}_s[0-9]+a[0-9]+b[0-9]+c[0-9]+_[0-9]{4}$")
try: cache = json.load(open(cache_p))
except Exception: cache = {}
new = {}
for od in sys.argv[2:]:
    p = os.path.join(od, "results.jsonl")
    try: s = os.stat(p)
    except Exception: continue
    k = f"{s.st_size}:{s.st_mtime_ns}"
    if p in cache and cache[p][0] == k: tags = cache[p][1]
    else:
        tags = []
        try:
            for x in open(p, errors="replace"):
                if "UNSAT" not in x[:200]: continue
                try: d = json.loads(x)
                except Exception: continue
                te = [d.get("tag"), str(d.get("encoder", "v7"))]
                if d.get("status") == "UNSAT" and rx.match(str(d.get("tag", ""))) and te not in tags: tags.append(te)
        except Exception: pass
    new[p] = [k, tags]
    for t, e in tags: print(t, od, e)
try:
    open(cache_p + ".tmp", "w").write(json.dumps(new)); os.replace(cache_p + ".tmp", cache_p)
except Exception: pass
'
PY_FIND='
import sys, json, glob, os
# best existing state folder of TAG made with encoder LABEL: most closed cubes (tree.json), then newest; prints OUTDIR
t, base, w, lab = sys.argv[1:5]; best = None
for tp in set(glob.glob(f"{base}/out*/cube/{t}/tree.json") + glob.glob(f"{base}/*/cube/{t}/tree.json")):
    if tp.startswith(w + "/"): continue
    try: tr = json.load(open(tp)); k = (len(tr["done"]), os.path.getmtime(tp))
    except Exception: continue
    if tr.get("tag") == t and str(tr.get("encoder", "v7")) == lab and (best is None or k > best[0]): best = (k, os.path.dirname(os.path.dirname(os.path.dirname(tp))))
if best: print(best[1])
'

# ---- processes: "PID TAG STATEDIR OUTDIR" for every real solver: a python running ccc90.py FORMULAS.json TAG
# /abs/OUTDIR/cube/TAG /abs/OUTDIR, whose state folder starts with SV_SCOPE (default $SV_BASE/).
procs() { ps -wweo pid=,args= 2>/dev/null | awk -v sc="$SCOPE" '
  $2 ~ /python/ { script = 0
    for (i = 3; i <= NF; i++) { if ($i == "-c" || $i == "-m") break; if ($i == "-X" || $i == "-W") { i++; continue }
      if ($i ~ /^-/) continue; script = i; break }
    if (script) { i = script; if ($i ~ /ccc90\.py$/) {
      t = $(i+2); st = $(i+3); od = $(i+4)
      if (i + 4 <= NF && $(i+1) ~ /\.json$/ && t ~ /^L[0-9][0-9]_s[0-9]+a[0-9]+b[0-9]+c[0-9]+_[0-9][0-9][0-9][0-9]$/ \
          && substr(st, 1, 1) == "/" && st == od "/cube/" t && (sc == "" || index(st, sc) == 1)) print $1, t, st, od } } }'; }
# Loose match (F1): any python with a ccc90.py argument followed by a tag; "PID TAG STATEDIR LIKE", STATEDIR resolved
# against /proc/PID/cwd (or -). It blocks starts and shows in the status. LIKE=1 only if ccc90.py is the script python
# runs (only interpreter options before it) and the next argument ends in .json (H1): only such a process counts as a
# writer (ALIVE, slots, duplicate guard). Kills always use the strict match.
lprocs() { local pid rest a seen t st cwd like k
  ps -wweo pid=,args= 2>/dev/null | awk '$2 ~ /python/ && /ccc90\.py/' | while read -r pid rest; do
    set -f; set -- $rest; set +f; seen=0; t=""; st=""; like=0
    shift   # the interpreter
    k=1; while [ $k -le $# ]; do a=${!k}
      case $a in -c|-m) break;; -X|-W) k=$((k+2)); continue;; -*) k=$((k+1)); continue;; esac
      if [[ $a == *ccc90.py ]]; then local nx=$((k+1)); [[ ${!nx:-} == *.json ]] && like=1; fi; break; done
    for a in "$@"; do if [ $seen = 0 ]; then [[ $a == *ccc90.py ]] && seen=1
      elif [ -z "$t" ]; then [[ $a =~ $TAGRE ]] && t=$a; else st=$a; break; fi; done
    [ -n "$t" ] || continue
    if [ -n "$st" ]; then
      if [[ $st != /* ]]; then cwd=$(readlink "/proc/$pid/cwd" 2>/dev/null); [ -n "$cwd" ] && st=$cwd/$st; fi
      st=$(realpath -m -- "$st" 2>/dev/null || echo "$st")
    else st=-; fi
    echo "$pid $t $st $like"
  done; }
alive() { local n=0 a b c d; while read -r a b c d; do [ -n "${a:-}" ] && [ "${d:-0}" = 1 ] && [ -d "$c" ] && n=$((n+1)); done <<< "${1-$(lprocs)}"; echo $n; }   # loose solvers whose state folder exists
rpath() { realpath -m -- "$1" 2>/dev/null || echo "$1"; }
kill_tree() { local p=$1 c; kill -STOP "$p" 2>/dev/null; for c in $(ps -o pid= --ppid "$p" 2>/dev/null); do kill_tree "$c"; done; kill -KILL "$p" 2>/dev/null; kill -CONT "$p" 2>/dev/null; }
mark_killed() { touch "$W/run/$1.killed" 2>/dev/null; rm -f "$W/run/$1.t0"; }
tree_open() { python3 -I -c 'import json,sys; print(len(json.load(open(sys.argv[1]))["open"]))' "$1/tree.json" 2>/dev/null || echo 1; }
stop_some() {   # WHY KEEP_STITCHING(0/1) SPARE_TAGS... : kill solvers, optionally sparing stitching trees and given tags
  local why=$1 keep=$2 p t st; shift 2; local spare=" $* "
  while read -r p t st _; do [ -n "${p:-}" ] || continue
    [[ $spare == *" $t "* ]] && continue
    [ "$keep" = 1 ] && [ "$(tree_open "$st")" = 0 ] && continue
    local k; k=$(pbof "$p" "$t" "$st"); kill_tree "$p"; mark_killed "$k"; rm -f "$W/run/$k.stop"; say "stopped $t pid $p ($why)"
  done <<< "$(procs)"; }

# ---- push methods. git: the lane clone's own remote and credentials. gh: GitHub's git-data REST API through the
# `gh` CLI (blobs, trees, commits, refs), for lanes whose git HTTPS write authentication fails. SV_PUSH=auto (default:
# git, switching to gh for the rest of this run when a git push fails with an authentication error), git or gh.
# Both keep the same layout; publication never forces (gh: ref PATCH with force=false); only lane-status-N is forced.
URL() { echo "${SV_PUSH_URL:-$(git -C "$R" remote get-url --push origin)}"; }
gid() { git -c user.name="lane$N" -c user.email="lane$N@users.noreply.github.com" "$@"; }
PUSHM=${SV_PUSH:-auto}; case $PUSHM in auto|git|gh) ;; *) PUSHM=auto;; esac
PM=git; [ "$PUSHM" = gh ] && PM=gh; PMWHY=""
GHREPO=${SV_GH_REPO:-$(git -C "$R" remote get-url origin 2>/dev/null | sed -nE 's#^.*github\.com[:/]+([A-Za-z0-9._-]+/[A-Za-z0-9._-]+)$#\1#p' | sed 's/\.git$//')}
[[ $GHREPO =~ ^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$ ]] || GHREPO=""
is_auth_err() { grep -qiE 'authentication failed|could not read username|permission to .* denied|invalid username or password|terminal prompts disabled|returned error: 40[13]|403 forbidden|access denied' "$1" 2>/dev/null; }
gitpush() {   # git push ARGS... (in the dir of -C); on an auth error in auto mode, switch to gh
  local e=$W/run/push.err rc; timeout 3600 git "$@" 2> "$e"; rc=$?; cat "$e" >> "$LOG" 2>/dev/null
  if [ $rc != 0 ] && [ "$PUSHM" = auto ] && [ "$PM" = git ] && is_auth_err "$e"; then
    if command -v gh > /dev/null && [ -n "$GHREPO" ] && gh_ok; then PM=gh; PMWHY="git auth failed"; GHFAILS=0; say "git push: authentication error -> using gh api (repo $GHREPO) from now on"
    else PMWHY="git auth failed; gh not usable (missing, not logged in, or repo $GHREPO not reachable)"; say "git push: authentication error; $PMWHY"; fi; fi
  return $rc; }
ghapi() { timeout 1800 gh api "$@" 2>> "$LOG"; }
gh_ok() { timeout 60 gh auth status > /dev/null 2>&1 && ghapi "repos/$GHREPO" > /dev/null; }
gh_result() {   # RC: count consecutive gh failures; after 3 in a row (auto mode) go back to git
  if [ "$1" = 0 ]; then GHFAILS=0; return 0; fi
  GHFAILS=$(( ${GHFAILS:-0} + 1 ))
  if [ $GHFAILS -ge 3 ] && [ "$PUSHM" = auto ]; then PM=git; PMWHY="gh failed 3 times in a row: back to git"; GHFAILS=0; say "$PMWHY"; fi
  return "$1"; }
jget() { python3 -I -c 'import sys,json
d=json.load(sys.stdin)
for k in sys.argv[1].split("."): d=d[k]
print(d)' "$1" 2>/dev/null; }
jbody() { python3 -I -c 'import sys,json; json.dump(json.loads(sys.argv[1]), open(sys.argv[2], "w"))' "$1" "$2"; }
gh_tip() { ghapi "repos/$GHREPO/git/ref/heads/$1" | jget object.sha; }
gh_blob() {   # FILE -> blob sha (base64 body streamed to a temp file; the API takes blobs up to 100 MB)
  local j=$W/run/blob.json s; python3 -I -c 'import sys,base64
with open(sys.argv[1],"rb") as fi, open(sys.argv[2],"w") as fo:
    fo.write("{\"encoding\": \"base64\", \"content\": \""); fo.write(base64.b64encode(fi.read()).decode()); fo.write("\"}")' "$1" "$j" || return 1
  s=$(ghapi -X POST "repos/$GHREPO/git/blobs" --input "$j" | jget sha); rm -f "$j"; [ -n "$s" ] && echo "$s"; }
gh_commit() {   # BASE_TREE|- ENTRIES_FILE PARENT|- MESSAGE -> commit sha
  local j=$W/run/tree.json t c
  python3 -I -c 'import sys,json
b, ef, out = sys.argv[1:4]; ents = [l.split(" ", 1) for l in open(ef).read().splitlines() if l.strip()]
o = {"tree": [{"path": p, "mode": "100644", "type": "blob", "sha": (None if s == "null" else s)} for s, p in ents]}
if b != "-": o["base_tree"] = b
json.dump(o, open(out, "w"))' "$1" "$2" "$j" || return 1
  t=$(ghapi -X POST "repos/$GHREPO/git/trees" --input "$j" | jget sha); [ -n "$t" ] || return 1
  if [ "$3" = - ]; then jbody "{\"message\": \"$4\", \"tree\": \"$t\", \"parents\": []}" "$j"; else jbody "{\"message\": \"$4\", \"tree\": \"$t\", \"parents\": [\"$3\"]}" "$j"; fi
  c=$(ghapi -X POST "repos/$GHREPO/git/commits" --input "$j" | jget sha); rm -f "$j"; [ -n "$c" ] && echo "$c"; }
gh_setref() {   # BRANCH SHA EXISTS(0/1) FORCE(true/false)
  local j=$W/run/ref.json
  if [ "$3" = 1 ]; then jbody "{\"sha\": \"$2\", \"force\": $4}" "$j"; ghapi -X PATCH "repos/$GHREPO/git/refs/heads/$1" --input "$j" > /dev/null
  else jbody "{\"ref\": \"refs/heads/$1\", \"sha\": \"$2\"}" "$j"; ghapi -X POST "repos/$GHREPO/git/refs" --input "$j" > /dev/null; fi; }
tel_files() {   # 2026-11-19 telemetry: snapshot each running pair's cube log -> "FILE NAME" lines (NAME tel_TAG[.v9].log.jsonl, sorted)
  # Read by the manager's opt/telemetry_collect.py (gh api, read-only). Off: SV_TEL=0. Logs above SV_TEL_MAX bytes are left out.
  [ "${SV_TEL:-1}" = 0 ] && return 0   # default on for all lanes (canary lane 4 OK 2026-11-19 04:47Z)
  local T=$W/run/tel; mkdir -p "$T" && rm -f "$T"/tel_* 2>/dev/null
  sed -n 's/^\(L[0-9][0-9]_[A-Za-z0-9]*_[0-9][0-9][0-9][0-9]\) run=running enc=\(v[79]\) .* state=\(\/[^ ]*\).*/\1 \2 \3/p' "$W/status.txt" | sort -u |
  while read -r t e d; do
    f=$d/cube/$t/log.jsonl; [ -f "$f" ] || continue
    [ "$(stat -c %s "$f" 2>/dev/null || echo 0)" -le "${SV_TEL_MAX:-3000000}" ] || continue
    n=tel_$t$([ "$e" = v9 ] && echo .v9).log.jsonl
    python3 -I -c 'import sys; b=open(sys.argv[1],"rb").read(); open(sys.argv[2],"wb").write(b[:b.rfind(b"\n")+1])' "$f" "$T/$n" 2>/dev/null || continue
    echo "$T/$n $n"
  done | LC_ALL=C sort -k2; }
beat_push() {   # one-commit branch lane-status-N holding status.txt (+ tel_TAG*.log.jsonl, see tel_files)
  local b t c rt e tf
  tf=$W/run/tel.ents; tel_files > "$tf" 2>/dev/null || : > "$tf"
  if [ "$PM" = git ]; then
    b=$(git -C "$R" hash-object -w "$W/status.txt") || return 1
    t=$( { printf '100644 blob %s\tstatus.txt\n' "$b"; while read -r f n; do x=$(git -C "$R" hash-object -w "$f") && printf '100644 blob %s\t%s\n' "$x" "$n"; done < "$tf"; } | git -C "$R" mktree) || return 1
    c=$(echo "lane $N status $(date -u +%FT%TZ)" | gid -C "$R" commit-tree "$t") || return 1
    rt=$(timeout 60 git -C "$R" ls-remote "$(URL)" "refs/heads/lane-status-$N" 2>/dev/null | awk '{print $1}')
    if [ -n "${LASTPUSHED:-}" ] && [ -n "$rt" ] && [ "$rt" != "$LASTPUSHED" ]; then OTHERWRITER=1; say "lane-status-$N moved by another writer"; fi
    gitpush -C "$R" push -q -f "$(URL)" "$c:refs/heads/lane-status-$N" && { LASTPUSHED=$c; return 0; }
    [ "$PM" = gh ] || return 1     # just switched: fall through and push the same status through gh
  fi
  rt=$(gh_tip "lane-status-$N")
  if [ -n "${LASTPUSHED:-}" ] && [ -n "$rt" ] && [ "$rt" != "$LASTPUSHED" ]; then OTHERWRITER=1; say "lane-status-$N moved by another writer"; fi
  b=$(gh_blob "$W/status.txt") || return 1; e=$W/run/beat.ents; echo "$b status.txt" > "$e"
  while read -r f n; do x=$(gh_blob "$f") && echo "$x $n" >> "$e"; done < "$tf"
  c=$(gh_commit - "$e" - "lane $N status $(date -u +%FT%TZ)") || return 1
  gh_setref "lane-status-$N" "$c" "$([ -n "$rt" ] && echo 1 || echo 0)" true && LASTPUSHED=$c
}
beat_gh_wrapped() { local was=$PM rc; beat_push; rc=$?; [ "$was" = gh ] || [ "$PM" = gh ] && gh_result $rc; return $rc; }
bytes() { local v=$1 m=1; case $v in *K) m=1024; v=${v%K};; *M) m=1048576; v=${v%M};; *G) m=1073741824; v=${v%G};; esac
  isnum "$v" && echo $((v * m)) || echo 94371840; }

# ---- publisher: TAG OUTDIR STATEDIR BRANCH [omf]. Backends: up_init (branch tip, already-published check), up_add
# (one file), up_flush (commit + append-only push); the files, their order and the batching are the same for both.
stale_parts() {   # paths of this tag's part files on the branch numbered >= UPNP (the new part count); parts below it
  # are overwritten in place (one entry per path per request). Fixed-string prefix match (a "." in a wave name is literal).
  awk -v pre="codex/$WV/$T.lrat.xz.part" -v np="${UPNP:-0}" 'index($0, pre) == 1 { n = substr($0, length(pre) + 1)
    if (n ~ /^[0-9]+$/ && n + 0 >= np + 0) print }' "$P/existing" 2>/dev/null; }
up_init() {
  UPPAR=-; UPTREE=-; UPHAS=0; UPN=0; : > "$P/ents"
  if [ "$PM" = git ]; then
    git init -q "$P" || return 1
    git -C "$R" config --get-regexp '^(http|credential|url)\.' 2>/dev/null | while read -r k v; do git -C "$P" config --add "$k" "$v"; done
    local tip; tip=$(timeout 120 git ls-remote "$(URL)" "refs/heads/$BR" 2>>"$LOG" | awk '{print $1}')
    if [ -n "$tip" ]; then
      timeout 900 git -C "$P" fetch -q --depth 1 --filter=blob:none "$(URL)" "$BR" 2>>"$LOG" || { say "publish $T: fetch $BR failed"; return 1; }
      git -C "$P" read-tree FETCH_HEAD || return 1; UPPAR=$(git -C "$P" rev-parse FETCH_HEAD); UPHAS=1
      git -C "$P" ls-tree -r --name-only FETCH_HEAD > "$P/existing"
      [ "$KIND" = proof ] && stale_parts | while read -r f; do git -C "$P" update-index --force-remove "$f"; done
    fi
  else
    local tip; tip=$(gh_tip "$BR")
    if [ -n "$tip" ]; then UPPAR=$tip; UPHAS=1; UPTREE=$(ghapi "repos/$GHREPO/git/commits/$tip" | jget tree.sha); [ -n "$UPTREE" ] || return 1
      ghapi "repos/$GHREPO/git/trees/$UPTREE?recursive=1" | python3 -I -c 'import sys,json; [print(e["path"]) for e in json.load(sys.stdin)["tree"]]' > "$P/existing" || return 1
      [ "$KIND" = proof ] && stale_parts | sed 's/^/null /' >> "$P/ents"; fi
  fi
  return 0; }
up_add() {   # FILE NAME
  if [ "$PM" = git ]; then git -C "$P" update-index --add --cacheinfo "100644,$(git -C "$P" hash-object -w "$1"),codex/$WV/$2"
  else local s; s=$(gh_blob "$1") || { say "publish $T: blob upload of $2 failed"; return 1; }; echo "$s codex/$WV/$2" >> "$P/ents"; fi
  UPN=$((UPN+1)); }
up_flush() {   # MESSAGE
  local c
  if [ "$PM" = git ]; then
    c=$(echo "lane $N: $KIND $T ($1)" | gid -C "$P" commit-tree "$(git -C "$P" write-tree)" $([ "$UPPAR" != - ] && echo "-p $UPPAR")) || return 1
    gitpush -C "$P" push -q "$(URL)" "$c:refs/heads/$BR" || { say "publish $T: push to $BR failed (retry next tick)"; return 1; }
  else
    c=$(gh_commit "$UPTREE" "$P/ents" "$UPPAR" "lane $N: $KIND $T ($1)") || { say "publish $T: commit through gh failed"; return 1; }
    gh_setref "$BR" "$c" "$UPHAS" false || { say "publish $T: ref update of $BR rejected (not a fast forward? retry next tick)"; return 1; }
    UPTREE=$(ghapi "repos/$GHREPO/git/commits/$c" | jget tree.sha); [ -n "$UPTREE" ] || return 1; : > "$P/ents"
  fi
  UPPAR=$c; UPHAS=1; UPN=0; }
publish() {   # wrapper: counts gh failures (not waits for disk or a record)
  local was=$PM rc; publish_do "$@"; rc=$?
  [ $rc = 2 ] && return 1
  if [ "$was" = gh ]; then [ $rc != 0 ] && PUBNOTE="${PUBNOTE:+$PUBNOTE; }gh publish of $1 aborted: blobs it uploaded stay unreferenced on GitHub until its gc (harmless)"; gh_result $rc; fi
  return $rc; }
publish_do() {
  local T=$1 O=$2 S=$3 BR=$4 KIND=${5:-proof} P=$W/pub/work WV f i psha size pb avail np
  WV=${BR#codex-}; mkdir -p "$W/pub"
  if [ "$PM" = gh ]; then pb=$(bytes "${SV_GH_PART:-32M}"); [ "$pb" -gt 94371840 ] && pb=94371840   # gh: 32 MiB default (H2)
  else pb=$(bytes "$PART"); fi
  if [ "$KIND" = proof ]; then
    size=$(stat -c %s "$O/proofs/$T.lrat.xz" 2>/dev/null); isnum "$size" || { say "publish $T: no proof file"; return 2; }
    avail=$(df -P -B1 "$W" 2>/dev/null | awk 'NR == 2 {print $4}'); isnum "$avail" || avail=0
    if [ "$avail" -lt $(( size + 3 * pb + 104857600 )) ]; then PUBNOTE="publish $T waits: $((avail / 1048576)) MB free at $W, needs $(( (size + 3 * pb) / 1048576 + 100 )) MB"; say "$PUBNOTE"; return 2; fi
  fi
  rm -rf "$P"; mkdir -p "$P/x" || return 1
  UPNP=0; [ "$KIND" = proof ] && UPNP=$(( (size + pb - 1) / pb ))
  up_init || return 1
  if [ "$KIND" = proof ] && grep -q "/$T\.sha256$" "$P/existing" 2>/dev/null; then say "publish $T: already on $BR"; rm -rf "$P"; return 0; fi
  if [ "$KIND" = omf ]; then
    grep -h -F "\"$T\"" "$O/results.jsonl" 2>/dev/null | grep -F ORIGINAL_MODEL_FOUND > "$P/x/$T.result.json"
    cp "$S/ORIGINAL_MODEL_FOUND.json" "$P/x/$T.ORIGINAL_MODEL_FOUND.json" 2>/dev/null
    tail -n 20 "$S.log" > "$P/x/$T.solver_log_tail.txt" 2>/dev/null
    [ -s "$P/x/$T.result.json" ] || echo "{\"status\": \"ORIGINAL_MODEL_FOUND\", \"tag\": \"$T\", \"lane\": $N, \"note\": \"evidence only in the files next to this one\"}" > "$P/x/$T.result.json"
    for f in $(cd "$P/x" && ls); do up_add "$P/x/$f" "$f" || return 1; done; up_flush "evidence" || return 1
  else
    psha=$(sha256sum "$O/proofs/$T.lrat.xz" | cut -c1-64)
    python3 -I -c 'import sys,json
t, want = sys.argv[1], sys.argv[3]
for x in open(sys.argv[2], errors="replace"):
    if t not in x: continue
    try: d=json.loads(x)
    except Exception: continue
    if d.get("tag")==t and d.get("status")=="UNSAT" and d.get("proof_sha256")==want: sys.stdout.write(x if x.endswith("\n") else x+"\n"); break' "$T" "$O/results.jsonl" "$psha" > "$P/x/$T.result.json"
    [ -s "$P/x/$T.result.json" ] || { PUBNOTE="publish $T: no UNSAT record in $O/results.jsonl matches the proof file's sha256 ${psha:0:12}"; say "$PUBNOTE"; rm -rf "$P"; return 2; }
    echo "$psha  $T.lrat.xz" > "$P/x/$T.sha256"
    cp "$S/log.jsonl" "$P/x/$T.log.jsonl" 2>/dev/null
    np=$(( (size + pb - 1) / pb ))
    for ((i = 0; i < np; i++)); do   # one part on disk at a time: cut, upload/hash, delete
      f=$(printf '%s.lrat.xz.part%03d' "$T" "$i")
      dd if="$O/proofs/$T.lrat.xz" of="$P/x/$f" bs="$pb" skip="$i" count=1 status=none iflag=fullblock 2>>"$LOG" || return 1
      up_add "$P/x/$f" "$f" || return 1; rm -f "$P/x/$f"
      if [ $UPN -ge "$BATCH" ]; then up_flush "parts to $((i+1))/$np" || return 1; fi
    done
    for f in "$T.sha256" "$T.log.jsonl" "$T.result.json"; do [ -f "$P/x/$f" ] && { up_add "$P/x/$f" "$f" || return 1; }; done   # record last
    up_flush "$np parts + record" || return 1
  fi
  say "published $KIND $T -> $BR (via $PM)"; rm -rf "$P"; return 0
}

# ---- assignment
declare -A A_FF A_BR A_OUT A_D A_E A_P A_SW A_PUB A_ENC A_TAG A_STOP
read_assign() {
  local F=$R/lanes/assign/$N.txt line t ff br od kv k v d e p sw
  A_TAGS=(); A_FF=(); A_BR=(); A_OUT=(); A_D=(); A_E=(); A_P=(); A_SW=(); A_PUB=(); A_ENC=(); A_TAG=(); A_STOP=(); V7FRESH=yes; MODE=run; BAD=""
  local DD=7 DE=1500 DP=240 DS="" DN=cegar90c en
  [ -f "$F" ] || { BAD="no assignment file lanes/assign/$N.txt"; return; }
  while read -r line; do
    line=${line%%#*}; set -f; set -- $line; set +f; [ $# -eq 0 ] && continue
    if [ "$1" = PUBLISH ]; then   # PUBLISH TAG [BRANCH]: opt-in publication of a record not found in a folder this loop ran
      if [[ ${2:-} =~ $TAGRE ]] && { [ -z "${3:-}" ] || [[ $3 =~ ^codex-[A-Za-z0-9._-]{1,60}$ ]]; }; then A_PUB[$2]=${3:-codex-m${2:1:2}-lane$N}
      else BAD="$BAD bad PUBLISH line;"; fi; continue; fi
    if [ "$1" = STOP ]; then   # STOP TAG [ENCODER]
      if [[ ${2:-} =~ $TAGRE ]]; then case ${3:-} in "") A_STOP[$2]="${A_STOP[$2]:-} *";; cegar90c) A_STOP[$2]="${A_STOP[$2]:-} v7";;
          cegar90e) A_STOP[$2]="${A_STOP[$2]:-} v9";; *) BAD="$BAD bad STOP encoder '$3';";; esac
      else BAD="$BAD bad STOP line;"; fi; continue; fi
    if [ "$1" = MODE ]; then case ${2:-} in run|fill) MODE=$2;; *) BAD="$BAD bad MODE;";; esac; continue; fi
    if [ "$1" = ENV ]; then shift; for kv in "$@"; do k=${kv%%=*}; v=${kv#*=}
        case $k in CUBE_DEPTH) [[ $v =~ ^[0-9]{1,2}$ ]] && DD=$v;; EXT_TIMEOUT) [[ $v =~ ^[0-9]{1,6}$ ]] && DE=$v;;
          PYSAT_CAP) [[ $v =~ ^[0-9]{1,6}$ ]] && DP=$v;; SEED_WAVE) [[ $v =~ ^m[0-9a-z]{1,20}$ ]] && DS=$v;;
          ENCODER) case $v in cegar90c|cegar90e) DN=$v;; *) BAD="$BAD bad ENV ENCODER '$v';";; esac;;
          V7_FRESH) case $v in yes|no) V7FRESH=$v;; *) BAD="$BAD bad ENV V7_FRESH '$v';";; esac;; *) BAD="$BAD bad ENV $kv;";; esac; done; continue; fi
    t=$1; ff=${2:-}; br=${3:-}; od=${4:--}; shift; [ $# -gt 0 ] && shift; [ $# -gt 0 ] && shift; [ $# -gt 0 ] && shift
    d=$DD; e=$DE; p=$DP; sw=$DS; en=$DN
    [[ $t =~ $TAGRE ]] || { BAD="$BAD bad tag '$t';"; continue; }
    [[ $ff =~ ^formulas[0-9]{2}_c[0-9]{2}\.json$ ]] && [ -f "$R/data/$ff" ] || { BAD="$BAD $t: bad formulas file '$ff';"; continue; }
    [[ $br =~ ^codex-[A-Za-z0-9._-]{1,60}$ ]] || { BAD="$BAD $t: bad branch '$br';"; continue; }
    if [[ $od == *=* ]]; then set -- "$od" "$@"; od=-; fi
    [ "$od" = - ] || { [[ $od =~ ^/[A-Za-z0-9._/-]+$ ]] && [[ $od != *..* ]]; } || { BAD="$BAD $t: bad outdir '$od';"; continue; }
    od=${od%/}; [ -z "$od" ] && od=-
    for kv in "$@"; do k=${kv%%=*}; v=${kv#*=}
      case $k in CUBE_DEPTH) [[ $v =~ ^[0-9]{1,2}$ ]] && d=$v;; EXT_TIMEOUT) [[ $v =~ ^[0-9]{1,6}$ ]] && e=$v;;
        PYSAT_CAP) [[ $v =~ ^[0-9]{1,6}$ ]] && p=$v;; SEED_WAVE) [[ $v =~ ^m[0-9a-z]{1,20}$ ]] && sw=$v;;
        ENCODER) case $v in cegar90c|cegar90e) en=$v;; *) BAD="$BAD $t: bad ENCODER '$v';"; continue 2;; esac;; *) BAD="$BAD $t: bad option $kv;";; esac; done
    local K=$t; [ "$en" = cegar90e ] && K=$t.v9   # pair key = file base in sv/run and sv/jobs (v7 keeps the plain tag)
    [ -n "${A_FF[$K]:-}" ] && { BAD="$BAD $t listed twice with encoder $en;"; continue; }
    A_TAGS+=("$K"); A_TAG[$K]=$t; A_FF[$K]=$ff; A_BR[$K]=$br; A_OUT[$K]=$od; A_D[$K]=$d; A_E[$K]=$e; A_P[$K]=$p; A_SW[$K]=$sw; A_ENC[$K]=$en
    [ -n "${A_BR[$t]:-}" ] || A_BR[$t]=$br   # per-tag branch (OMF evidence, records): the tag's first pair
  done < "$F"
}
okpath() { [[ ${1:-} =~ ^/[A-Za-z0-9._/-]+$ ]] && [[ $1 != *..* ]]; }
enclab() { case ${1:-} in cegar90c) echo v7;; cegar90e) echo v9;; cegar90b) echo v6;; *) echo "?";; esac; }
folder_enc() {   # STATEDIR -> encoder label of its tree.json (a tree without the key: v7), or - without a tree
  python3 -I -c 'import json,sys
try: print(json.load(open(sys.argv[1] + "/tree.json")).get("encoder", "v7"))
except Exception: print("-")' "$1"; }
penc() {   # PID STATEDIR -> the encoder a running solver really uses: ENCODER in its environment; without it the tree's
  # label (an unlabelled tree is v7), and with no tree v7 (worker.sh and ccc90.py default to cegar90c). "?" only when
  # the environment cannot be read and there is no tree.
  local env e; env=$(tr '\0' '\n' 2>/dev/null < "/proc/$1/environ") || env=UNREADABLE
  [ -r "/proc/$1/environ" ] || env=UNREADABLE
  e=$(echo "$env" | sed -n 's/^ENCODER=//p' | head -1)
  if [ -n "$e" ]; then enclab "$e"; return; fi
  e=$(folder_enc "$2"); if [ "$e" != - ]; then echo "$e"; elif [ "$env" = UNREADABLE ]; then echo "?"; else echo v7; fi; }
stopped_by() { [[ " ${A_STOP[$1]:-} " == *" $2 "* || " ${A_STOP[$1]:-} " == *" * "* ]]; }   # TAG LABEL: a STOP line covers this solver
pbof() { [ "$(penc "$1" "$3")" = v9 ] && echo "$2.v9" || echo "$2"; }   # PID TAG STATEDIR -> pair key of a running solver
outdir_for() {   # KEY: sticky, encoder-aware choice of the state folder for a pair (never one of another encoder)
  local K=$1 T=${A_TAG[$1]} WL; WL=$(enclab "${A_ENC[$1]:-cegar90c}"); local o p st fe
  [ "${A_OUT[$K]}" != - ] && { echo "${A_OUT[$K]}"; return; }
  while read -r p _ st o; do [ -n "${p:-}" ] && [ "$(penc "$p" "$st")" = "$WL" ] && { echo "$o"; return; }; done <<< "$(procs | awk -v t="$T" '$2 == t')"
  o=$(head -c 4096 "$W/run/$K.out" 2>/dev/null | head -1)
  if okpath "$o"; then fe=$(folder_enc "$o/cube/$T"); { [ "$fe" = "$WL" ] || { [ "$fe" = - ] && [ "$(head -c 8 "$W/run/$K.enc" 2>/dev/null)" = "$WL" ]; }; } && { echo "$o"; return; }; fi
  o=$(python3 -I -c "$PY_FIND" "$T" "$BASE" "$W" "$WL"); okpath "$o" && { echo "$o"; return; }
  o=$BASE/out_sv_$T; [ "$WL" = v7 ] || o=${o}_$WL
  fe=$(folder_enc "$o/cube/$T"); { [ "$fe" = - ] || [ "$fe" = "$WL" ]; } || o=${o}_$WL
  echo "$o"
}
known_outdirs() {
  { procs | awk '{print $4}'; for f in "$W"/run/*.out; do [ -f "$f" ] && head -1 "$f"; done; awk '{print $1}' "$W/run/seen_pairs" 2>/dev/null
    for t in "${A_TAGS[@]}"; do [ "${A_OUT[$t]}" != - ] && echo "${A_OUT[$t]}"; done
    for d in "$BASE"/*/; do [ -d "$d/cube" ] && echo "${d%/}"; done; } 2>/dev/null | while read -r d; do okpath "$d" && [ "$d" != "$W" ] && echo "$d"; done | sort -u
}
omf_scan() {   # OUTDIR... -> "TAG STATEDIR OUTDIR" for every piece of ORIGINAL_MODEL_FOUND evidence
  local O f t
  for O in "$@"; do
    for f in "$O"/cube/*/ORIGINAL_MODEL_FOUND.json; do [ -f "$f" ] || continue; t=${f%/ORIGINAL_MODEL_FOUND.json}; t=${t##*/}; echo "$t $O/cube/$t $O"; done
    [ -f "$O/results.jsonl" ] && grep -F ORIGINAL_MODEL_FOUND "$O/results.jsonl" | grep -o '"tag": *"[^"]*"' | cut -d'"' -f4 | sort -u | while read -r t; do echo "$t $O/cube/$t $O"; done
    for f in $(grep -l -s -F ORIGINAL_MODEL_FOUND "$O"/cube/*.log 2>/dev/null); do t=${f##*/}; t=${t%.log}; echo "$t $O/cube/$t $O"; done
    [ -f "$O/ccc.log" ] && grep -E '^L[0-9]{2}_[^ ]+ ccc exit 2$' "$O/ccc.log" | awk -v o="$O" '{print $1, o "/cube/" $1, o}'
  done | while read -r t st o; do [[ $t =~ $TAGRE ]] && echo "$t $st $o"; done | sort -u
}
has_omf() { local T=$1 O=$2; [ -f "$O/cube/$T/ORIGINAL_MODEL_FOUND.json" ] && return 0
  grep -F "\"$T\"" "$O/results.jsonl" 2>/dev/null | grep -qF ORIGINAL_MODEL_FOUND && return 0
  grep -qxF "$T ccc exit 2" "$O/ccc.log" 2>/dev/null; }

start_solver() {   # KEY OUTDIR: non-blocking; the worker's pid is kept so a start in progress is not repeated
  local K=$1 T=${A_TAG[$1]} O=$2 wave J EN=${A_ENC[$1]:-cegar90c}
  wave=${A_SW[$K]:-m${T:1:2}e5}; [ -f "$R/ckpt/$wave.jsonl.xz" ] || wave=m${T:1:2}sv
  J=$W/jobs/$K/$wave; mkdir -p "$J" "$O" || return 1; echo "$T" > "$J/h01.txt" || return 1
  echo "$O" > "$W/run/$K.out"; echo "$VER" > "$W/run/$K.ver"; date +%s > "$W/run/$K.t0"; rm -f "$W/run/$K.killed"
  enclab "$EN" > "$W/run/$K.enc"
  grep -c "^$T ccc exit " "$O/ccc.log" 2>/dev/null > "$W/run/$K.nexit" || echo 0 > "$W/run/$K.nexit"
  ( cd "$R" && exec setsid nohup env ENCODER="$EN" FORMULAS_FILE="${A_FF[$K]}" CUBE_DEPTH="${A_D[$K]}" EXT_TIMEOUT="${A_E[$K]}" \
      PYSAT_CAP="${A_P[$K]}" PAR=1 WINDOW="$WINDOW" PREV="$BASE/none" bash worker.sh ccc "$J/h01.txt" "$O" \
      >> "$O.sv_$T.nohup" 2>&1 < /dev/null ) &
  echo "$!" > "$W/run/$K.wpid"
  say "started $T in $O (encoder $EN, depth ${A_D[$K]}, ext ${A_E[$K]}, cap ${A_P[$K]}, seeds $wave, version $VER, worker pid $!)"
}
other_start_in() {   # KEY OUTDIR: another assigned tag's worker is still starting in the same OUTDIR (worker.sh todo.txt race)
  local x; for x in "${A_TAGS[@]}"; do [ "$x" != "$1" ] && starting "$x" && [ "$(head -1 "$W/run/$x.out" 2>/dev/null)" = "$2" ] && return 0; done; return 1; }
starting() {   # KEY: true while the worker we started is alive (it may not have reached ccc90.py yet)
  local w; w=$(num "$W/run/$1.wpid" ""); [ -n "$w" ] && tr '\0' ' ' 2>/dev/null < "/proc/$w/cmdline" | grep -qF "worker.sh ccc $W/jobs/$1/"; }

# ---- one tick
tick() {
  NOTES=(); ALERTS=(); PUBNOTE=""; local now; now=$(date +%s)
  # 1. code
  local pulled=OK
  { timeout 120 git -C "$R" fetch -q --no-tags origin main 2>>"$LOG" && git -C "$R" merge -q --ff-only FETCH_HEAD 2>>"$LOG"; } || pulled=FAILED   # main only: a plain pull also fetches the GB-sized codex-* proof branches (lane 8, 08:31Z: RPC failed / early EOF)
  [ $pulled = OK ] || NOTES+=("git pull failed (running the current verified code)")
  VER=$(head -c 64 "$R/lanes/VERSION" 2>/dev/null | tr -dc 'A-Za-z0-9._-'); VER=${VER:-0}
  read_assign; [ -n "$BAD" ] && NOTES+=("assignment:$BAD")
  SHAOK=1; SHAMSG=OK; local out f
  out=$( (cd "$R" && sha256sum -c --quiet SHA256SUMS) 2>&1 ) || { SHAOK=0; SHAMSG="FAIL($(echo "$out" | grep -v ': OK$' | head -3 | tr '\n' ' ' | cut -c1-200))"; }
  if [ $SHAOK = 1 ]; then for f in lanes/supervise.sh worker.sh; do
      awk '{sub(/^\*/, "", $2); print $2}' "$R/SHA256SUMS" | grep -qxF "$f" || { SHAOK=0; SHAMSG="FAIL($f not in SHA256SUMS)"; }; done; fi
  if [ $SHAOK = 1 ]; then rm -f "$W/sha_fail_since"
    local newsum; newsum=$(sha256sum "$R/lanes/supervise.sh" | cut -c1-64)
    if [ "$newsum" != "$MYSUM" ]; then
      if bash -n "$R/lanes/supervise.sh" 2>>"$LOG"; then say "supervise.sh changed (${MYSUM:0:12} -> ${newsum:0:12}): exec new version"; SV_EXEC=1 exec bash "$R/lanes/supervise.sh" "$N"
      else ALERTS+=("new lanes/supervise.sh ${newsum:0:12} fails bash -n: still running ${MYSUM:0:12}"); fi
    fi
  else
    [ -f "$W/sha_fail_since" ] || { date +%s > "$W/sha_fail_since" 2>/dev/null; say "SHA256SUMS check failed: $SHAMSG"; }
    local since; since=$(num "$W/sha_fail_since" ""); [ -n "$since" ] || { since=$now; NOTES+=("cannot record the SHA failure time (disk full?): grace restarts every tick"); }
    local el=$((now - since))
    if [ "$MODE" = fill ]; then ALERTS+=("SHA256SUMS FAILED for ${el} s (mode fill: nothing stopped, nothing started)")
    elif [ $el -ge "$SHA_GRACE" ]; then
      [ -n "$(procs)" ] && stop_some "SHA256SUMS failed: $SHAMSG" 1
      ALERTS+=("SHA256SUMS FAILED: solvers stopped (stitching ones kept), nothing started until it passes")
    else NOTES+=("SHA256SUMS failing for ${el} s (grace $SHA_GRACE s): nothing started"); fi
  fi
  # 2. ORIGINAL_MODEL_FOUND (in every known OUTDIR)
  local KO; KO=$(known_outdirs); local omf; omf=$(omf_scan $KO)
  local omfnew; omfnew=$(comm -23 <(echo "$omf" | sed '/^$/d') <(sort -u "$W/omf_ack" 2>/dev/null))
  if [ ! -f "$W/HALT_OMF" ] && [ -f "$W/omf_seen" ]; then   # a person removed HALT_OMF: what it held is acknowledged
    cat "$W/omf_seen" >> "$W/omf_ack"; rm -f "$W/omf_seen"; say "HALT_OMF removed by a person: evidence acknowledged (those tags are still never started)"
    omfnew=$(comm -23 <(echo "$omf" | sed '/^$/d') <(sort -u "$W/omf_ack" 2>/dev/null)); fi
  if [ -n "$omfnew" ]; then
    if [ -n "$(comm -23 <(echo "$omfnew") <(sort -u "$W/HALT_OMF" 2>/dev/null))" ]; then
      echo "$omfnew" | sort -u - "$W/HALT_OMF" 2>/dev/null | sort -u > "$W/HALT_OMF.new"; mv -f "$W/HALT_OMF.new" "$W/HALT_OMF"; cp -f "$W/HALT_OMF" "$W/omf_seen"
      stop_some "ORIGINAL_MODEL_FOUND" 0 $(awk '{print $1}' "$W/HALT_OMF"); say "ORIGINAL_MODEL_FOUND: $(tr '\n' ';' < "$W/HALT_OMF")"; FORCEBEAT=1; fi
  fi
  if [ -f "$W/HALT_OMF" ]; then
    local age=$(( now - $(stat -c %Y "$W/HALT_OMF" 2>/dev/null || echo "$now") ))
    if [ $age -ge 30 ]; then [ -n "$(procs)" ] && stop_some "ORIGINAL_MODEL_FOUND halt" 0
    else [ -n "$(procs)" ] && stop_some "ORIGINAL_MODEL_FOUND halt" 0 $(awk '{print $1}' "$W/HALT_OMF"); fi
    local t st od; while read -r t st od; do [ -n "${t:-}" ] || continue; [ -f "$W/pub/$t.omf.done" ] && continue
      publish "$t" "$od" "$st" "${A_BR[$t]:-codex-m${t:1:2}-lane$N}" omf && touch "$W/pub/$t.omf.done"; done < "$W/HALT_OMF"
    ALERTS+=("HALTED: ORIGINAL_MODEL_FOUND (remove $W/HALT_OMF only after a person has examined it)")
  fi
  declare -A OMFT=(); local t st od; while read -r t st od; do [ -n "${t:-}" ] && OMFT[$t]=1; done <<< "$omf"
  # 3. records anywhere in a known OUTDIR
  # loose view of every solver (F1). Publication eligibility is per (OUTDIR, TAG) pair (F2/G1): a pair seen running
  # (loose view), started or adopted (run/TAG.out), or given explicitly in the assignment; kept in run/seen_pairs.
  local LP; LP=$(lprocs); declare -A LRUN=(); local lp lt ls e et ot
  while read -r lp lt ls ll; do [ -n "${lp:-}" ] || continue; LRUN[$lt]="${LRUN[$lt]:-}$lp "
    [ "${ll:-0}" = 1 ] || { NOTES+=("pid $lp has $lt in its arguments but is not a ccc90.py solver: blocks starts of $lt, never touched"); continue; }
    [[ $ls == */cube/$lt ]] && echo "${ls%/cube/*} $lt" >> "$W/run/seen_pairs"; done <<< "$LP"
  for f in "$W"/run/*.out; do [ -f "$f" ] || continue; ot=$(basename "$f" .out); ot=${ot%.v9}; [[ $ot =~ $TAGRE ]] || continue
    e=$(head -1 "$f"); okpath "$e" && echo "$(rpath "$e") $ot" >> "$W/run/seen_pairs"; done 2>/dev/null
  for t in "${A_TAGS[@]}"; do [ "${A_OUT[$t]}" != - ] && echo "$(rpath "${A_OUT[$t]}") ${A_TAG[$t]}" >> "$W/run/seen_pairs"; done 2>/dev/null
  [ -f "$W/run/seen_pairs" ] && { sort -u "$W/run/seen_pairs" > "$W/run/seen_pairs.new" 2>/dev/null && mv -f "$W/run/seen_pairs.new" "$W/run/seen_pairs"; }
  declare -A ELIG=()
  while read -r e et; do [ -n "${et:-}" ] && ELIG["$e $et"]=1; done < <(cat "$W/run/seen_pairs" 2>/dev/null)
  declare -A REC=() RECENC=(); local re; while read -r t od re; do [ -n "${t:-}" ] || continue
      if [ -z "${REC[$t]:-}" ] || { [ -z "${ELIG["$(rpath "${REC[$t]}") $t"]:-}" ] && [ -n "${ELIG["$(rpath "$od") $t"]:-}" ]; }; then REC[$t]=$od; RECENC[$t]=${re:-v7}; fi
    done <<< "$(python3 -I -c "$PY_RECS" "$W/rescache2.json" $KO 2>/dev/null)"
  # 4. solvers
  local P; P=$(procs); local O info c o sz pid
  declare -A RUN=(); while read -r pid t st od; do [ -n "${pid:-}" ] && [ -n "${t:-}" ] && RUN[$t]="${RUN[$t]:-}$pid "; done <<< "$P"
  # duplicate guard on resolved state folders (loose view). Only strict matches are ever killed: keep the one running
  # longest; if a newer duplicate is outside scope, kill our (strict) ones instead, so one writer remains (costs <= 1 cube).
  local dup s q grp others nout allstrict; declare -A STRICTP=(); for q in $(echo "$P" | awk '{print $1}'); do STRICTP[$q]=1; done
  dup=$(echo "$LP" | awk '$3 != "-" && $4 == 1 {print $3}' | sort | uniq -d)   # writers only (H1)
  for s in $dup; do
    { date -u +%FT%TZ; echo "$LP" | awk -v s="$s" '$3 == s'; } >> "$s/DUPLICATE_WRITERS" 2>/dev/null
    grp=$(echo "$LP" | awk -v s="$s" '$3 == s && $4 == 1 {print $1}' | while read -r q; do echo "$(ps -o etimes= -p "$q" 2>/dev/null | tr -d ' ') $q"; done | sort -rn | awk '{print $2}')
    others=$(echo "$grp" | tail -n +2); allstrict=1; for q in $others; do [ -n "${STRICTP[$q]:-}" ] || allstrict=0; done
    if [ $allstrict = 1 ]; then for pid in $others; do mark_killed "$(pbof "$pid" "$(echo "$LP" | awk -v p="$pid" '$1 == p {print $2}')" "$s")"; kill_tree "$pid"; say "killed duplicate solver $pid on $s"; NOTES+=("killed a duplicate solver on $s"); done
    else
      for pid in $grp; do [ -n "${STRICTP[$pid]:-}" ] && { mark_killed "$(pbof "$pid" "$(echo "$LP" | awk -v p="$pid" '$1 == p {print $2}')" "$s")"; kill_tree "$pid"; say "killed our solver $pid on $s: a newer solver outside scope writes the same folder"; NOTES+=("killed our solver on $s (a newer solver outside scope writes it)"); }; done
      nout=0; for q in $grp; do [ -n "${STRICTP[$q]:-}" ] || nout=$((nout+1)); done
      [ $nout -gt 1 ] && ALERTS+=("$nout solvers outside scope write $s: stop all but one by hand")
    fi; done
  [ -n "$dup" ] && LP=$(lprocs)
  P=$(procs); RUN=(); while read -r pid t st od; do [ -n "${pid:-}" ] && [ -n "${t:-}" ] && RUN[$t]="${RUN[$t]:-}$pid "; done <<< "$P"
  local running; running=$(alive "$LP")   # slots: loose solvers with a real state folder
  LRUN=(); while read -r lp lt ls ll; do [ -n "${lp:-}" ] && LRUN[$lt]="${LRUN[$lt]:-}$lp "; done <<< "$LP"
  local can=1; [ $SHAOK = 1 ] || can=0; [ -f "$W/HALT_OMF" ] && can=0
  # per-pair view of the strict solvers: RUNK[KEY] pids (KEY = TAG for v7, TAG.v9 for v9), their folder and encoder
  declare -A RUNK=() KST=() KOD=() KENC=() RUNT=(); local pp pt pst pod pk pe
  while read -r pp pt pst pod; do [ -n "${pp:-}" ] && [ -n "${pt:-}" ] || continue; pe=$(penc "$pp" "$pst"); pk=$pt; [ "$pe" = v9 ] && pk=$pt.v9
    RUNK[$pk]="${RUNK[$pk]:-}$pp "; KST[$pk]=$pst; KOD[$pk]=$pod; KENC[$pk]=$pe; RUNT[$pt]=1; done <<< "$P"
  declare -A ISA=() ISAP=(); local k; for k in "${A_TAGS[@]}"; do ISA[${A_TAG[$k]}]=1; ISAP[$k]=1; done
  declare -A STARTOUT=()
  STATUS_LINES=()
  # STOP TAG [ENCODER] (every mode, the only way MODE fill stops a solver): stop at a cube boundary, never a stitching tree
  local stopnote
  stop_req() {   # KEY WHY -> sets stopnote
    local K=$1 xs=${KST[$1]} xp; xp=$(echo ${RUNK[$1]} | awk '{print $1}')
    if [ "$(tree_open "$xs")" = 0 ]; then stopnote="($2 waits: pid $xp is stitching)"; return 1; fi
    [ -f "$W/run/$K.stop" ] || { echo "$2 $now $(stat -c %s "$xs/log.jsonl" 2>/dev/null || echo 0) $xp $xs" > "$W/run/$K.stop"; say "$2: stop requested for ${K%.v9} pid $xp (${KENC[$K]}), at its next cube boundary"; }
    stopnote="($2: stops at its next cube boundary)"; return 0; }
  # 4a. running solvers whose (tag, encoder) pair is not listed
  for pk in "${!RUNK[@]}"; do [ -n "${ISAP[$pk]:-}" ] && continue; pt=${pk%.v9}
    info=$(echo "$pt ${KST[$pk]}" | python3 -I -c "$PY_INFO"); read -r _ c o sz _ <<< "$info"
    local base_l="$pt run=running enc=${KENC[$pk]} closed=$c open=$o recorded=$([ -n "${REC[$pt]:-}" ] && echo yes || echo no) pid=$(echo ${RUNK[$pk]} | tr ' ' ,) state=${KOD[$pk]} UNASSIGNED"
    if stopped_by "$pt" "${KENC[$pk]}"; then stop_req "$pk" STOP && base_l=${base_l/run=running/run=stopping}; STATUS_LINES+=("$base_l $stopnote")
    elif [ "$MODE" = run ] && [ $can = 1 ]; then stop_req "$pk" unassigned && base_l=${base_l/run=running/run=stopping}; STATUS_LINES+=("$base_l $stopnote")
    else STATUS_LINES+=("$base_l kept(mode $MODE)"); fi
  done
  for t in "${!LRUN[@]}"; do [ -n "${ISA[$t]:-}" ] || [ -n "${RUNT[$t]:-}" ] && continue
    STATUS_LINES+=("$t run=running-outside-scope running outside scope (pid $(echo ${LRUN[$t]} | tr ' ' ,)) UNASSIGNED, not touched"); done
  # 4b. listed pairs: stitch-ready ones (tree with no open cube) first, then file order
  declare -A KOUT=(); local ORDER=() RDY=()
  for k in "${A_TAGS[@]}"; do KOUT[$k]=$(outdir_for "$k")
    if [ -z "${RUNK[$k]:-}" ] && [ "$(tree_open "${KOUT[$k]}/cube/${A_TAG[$k]}")" = 0 ]; then RDY+=("$k"); else ORDER+=("$k"); fi; done
  for k in "${RDY[@]}" "${ORDER[@]}"; do
    t=${A_TAG[$k]}; local WL; WL=$(enclab "${A_ENC[$k]:-cegar90c}")
    [ -f "$W/run/$k.stop" ] && grep -q '^unassigned' "$W/run/$k.stop" && { rm -f "$W/run/$k.stop"; say "stop cancelled: $k listed again"; }
    O=${KOUT[$k]}; [ -n "${RUNK[$k]:-}" ] && O=${KOD[$k]}; st=$O/cube/$t
    info=$(echo "$t $st" | python3 -I -c "$PY_INFO"); read -r _ c o sz tenc <<< "$info"
    local pids=${RUNK[$k]:-} ver; ver=$(head -c 64 "$W/run/$k.ver" 2>/dev/null | tr -dc 'A-Za-z0-9._-'); ver=${ver:-adopted}
    local rec=no; [ -n "${REC[$t]:-}" ] && rec=yes
    local line="$t closed=$c open=$o recorded=$rec pid=$(echo ${pids:--} | tr ' ' ,) state=$O" RS=stopped
    # outside-scope solvers of this tag that may use this encoder (unknown counts as this one): block the start
    # (a strict-matched solver is already accounted for as its own (TAG, ENCODER) pair: it never blocks another pair)
    local LX="" x xe xs; for x in ${LRUN[$t]:-}; do [ -n "${STRICTP[$x]:-}" ] && continue
      xs=$(echo "$LP" | awk -v p="$x" '$1 == p {print $3; exit}'); xe=$(penc "$x" "$xs"); { [ "$xe" = "$WL" ] || [ "$xe" = "?" ]; } && LX="$LX$x "; done
    if [ -n "$pids" ]; then
      [ -f "$W/run/$k.ver" ] || { echo "$VER" > "$W/run/$k.ver"; echo "$O" > "$W/run/$k.out"; echo "$WL" > "$W/run/$k.enc"; ver=$VER; say "adopted running $t (pid $pids, $WL) in $O at version $VER"; }
      [ -f "$W/run/$k.nexit" ] || { grep -c "^$t ccc exit " "$O/ccc.log" 2>/dev/null > "$W/run/$k.nexit" || echo 0 > "$W/run/$k.nexit"; }
      RS=running; line="$line ver=$ver"
      if stopped_by "$t" "$WL"; then stop_req "$k" STOP && RS=stopping; line="$line $stopnote"
      elif [ "$ver" != "$VER" ]; then
        if [ "$MODE" = run ] && [ $can = 1 ]; then stop_req "$k" upgrade && RS=stopping; line="$line $stopnote"
        else line="$line upgrade pending ($ver -> $VER; mode $MODE restarts nothing)"; fi
      fi
    elif stopped_by "$t" "$WL"; then line="$line (STOP)"
    elif [ -n "$LX" ]; then RS=running-outside-scope; line="$line running outside scope (pid $(echo $LX | tr ' ' ,)): not started, not touched"
    elif [ "$rec" = yes ]; then :   # reported with the records below
    elif starting "$k"; then RS=starting; line="$line starting (worker $(num "$W/run/$k.wpid"))"
    else
      # a solver this run started or adopted has gone: judge how it ended (ccc.log 'TAG ccc exit N' lines since then)
      if [ -f "$W/run/$k.nexit" ]; then
        local n0 n1 code; n0=$(num "$W/run/$k.nexit"); n1=$(grep -c "^$t ccc exit " "$O/ccc.log" 2>/dev/null); isnum "$n1" || n1=0
        code=none; [ "$n1" -gt "$n0" ] && code=$(grep "^$t ccc exit " "$O/ccc.log" | tail -1 | awk '{print $4}')
        rm -f "$W/run/$k.nexit" "$W/run/$k.wpid"
        if [ -f "$W/run/$k.killed" ]; then rm -f "$W/run/$k.killed"
        elif [ "$code" = 0 ] || [ "$code" = 3 ]; then rm -f "$W/run/$k.fails"
        else
          local fl; fl=$(( $(num "$W/run/$k.fails") + 1 )); echo $fl > "$W/run/$k.fails"
          local t0; t0=$(num "$W/run/$k.t0" 0); say "$t ($WL) ended badly (exit $code, $((now - t0)) s after start; $fl in a row)"
          [ $fl -ge "$MAXFAIL" ] && { echo $((now + HOLD)) > "$W/run/$k.hold"; say "$t ($WL): $fl bad exits in a row: held for $HOLD s"; }
        fi
      fi
      local held; held=$(num "$W/run/$k.hold" 0)
      if [ -n "${OMFT[$t]:-}" ] || has_omf "$t" "$O"; then line="$line NOT STARTED (ORIGINAL_MODEL_FOUND evidence for this tag)"
      elif [ "$held" -gt "$now" ]; then
        line="$line HELD($(num "$W/run/$k.fails") bad exits; retry in $((held - now)) s): $(tail -n 2 "$O/cube/$t.log" 2>/dev/null | tr '\n' ' ' | cut -c1-160)"
      elif [ $can = 0 ]; then line="$line NOT STARTED (halted)"
      elif [ "$tenc" != - ] && [ "$tenc" != "$WL" ]; then line="$line NOT STARTED (state folder $st holds an encoder $tenc state; listed as $WL: give another OUTDIR)"
      elif [ "$WL" = v7 ] && [ "$V7FRESH" = no ] && [ "$tenc" != v7 ]; then
        line="$line skipped (no v7 folder; V7_FRESH=no: a v7 pair only resumes)"; NOTES+=("$t (v7): no v7 state folder to resume, pair skipped (V7_FRESH=no)")
      elif [ "$running" -ge "$MAXS" ]; then line="$line waiting for a free slot ($running/$MAXS running)"
      elif [ -n "${STARTOUT[$O]:-}" ] || other_start_in "$k" "$O"; then
        line="$line waiting (another start in $O)"
      else
        rm -f "$W/run/$k.hold"; start_solver "$k" "$O"; running=$((running+1)); STARTOUT[$O]=1; FORCEBEAT=1
        line="$line STARTED ver=$VER"; RS=starting
      fi
    fi
    if [ -f "$O/failed_attempts.jsonl" ] && grep -qF "\"$t\"" "$O/failed_attempts.jsonl"; then
      ALERTS+=("$t: $(grep -cF "\"$t\"" "$O/failed_attempts.jsonl") cake_lpr-rejected stitch(es) in $O/failed_attempts.jsonl"); fi
    line="$t run=$RS enc=$WL ${line#"$t "}"   # run=running|stopping|starting|running-outside-scope|stopped (recorded tags: below)
    [ "$rec" = yes ] || STATUS_LINES+=("$line")
  done
  for t in "${!A_STOP[@]}"; do [ -n "${ISA[$t]:-}" ] || [ -n "${RUNT[$t]:-}" ] || [ -n "${REC[$t]:-}" ] || STATUS_LINES+=("$t run=stopped enc=- (STOP)"); done
  # 4c. records (assigned or not) and their publication
  local old=""
  for t in "${!REC[@]}"; do
    od=${REC[$t]}; local br=${A_PUB[$t]:-${A_BR[$t]:-codex-m${t:1:2}-lane$N}} pl
    if [ ! -f "$W/pub/$t.done" ] && [ -z "${ELIG["$(rpath "$od") $t"]:-}" ] && [ -z "${A_PUB[$t]:-}" ]; then   # old record (F2/G1)
      old="$old $t"; [ -n "${ISA[$t]:-}" ] && STATUS_LINES+=("$t run=recorded enc=${RECENC[$t]:-v7} recorded=yes published=no (old record in $od, not published automatically) state=$od"); continue; fi
    if [ ! -f "$W/pub/$t.done" ]; then
      if [ -f "$od/proofs/$t.lrat.xz" ]; then publish "$t" "$od" "$od/cube/$t" "$br" && { echo "$br" > "$W/pub/$t.done"; FORCEBEAT=1; }
      else NOTES+=("$t recorded in $od but $od/proofs/$t.lrat.xz is missing"); fi
    fi
    if [ -f "$W/pub/$t.done" ]; then pl="published=$(head -1 "$W/pub/$t.done" | tr -dc 'A-Za-z0-9._-')"
      [ -n "${ISA[$t]:-}" ] && { STATUS_LINES+=("$t run=recorded enc=${RECENC[$t]:-v7} recorded=yes $pl state=$od"); NOTES+=("$t recorded: take it out of lanes/assign/$N.txt"); }
    else STATUS_LINES+=("$t run=recorded enc=${RECENC[$t]:-v7} recorded=yes published=no (to $br) state=$od$([ -n "${ISA[$t]:-}" ] || echo ' UNASSIGNED')"); fi
  done
  [ -n "$PUBNOTE" ] && NOTES+=("$PUBNOTE")
  [ -n "$old" ] && NOTES+=("$(echo $old | wc -w) old records not published (found only by the $BASE/*/ scan):$old; add 'PUBLISH TAG' to lanes/assign/$N.txt to publish one")
  [ ${#A_TAGS[@]} -gt "$MAXS" ] && NOTES+=("${#A_TAGS[@]} (tag, encoder) pairs listed, $MAXS slots: fill order = stitch-ready first, then file order")
  for f in $(for d in $KO; do ls "$d"/cube/*/DUPLICATE_WRITERS 2>/dev/null; done); do
    ALERTS+=("DUPLICATE_WRITERS in ${f%/DUPLICATE_WRITERS}: two solvers wrote this state; check it before trusting a stitch, then delete the file"); done
  [ "${OTHERWRITER:-0}" = 1 ] && ALERTS+=("another writer pushes lane-status-$N (an old heartbeat loop still running?)")
  # 5. status (kept as it was if it cannot be written, e.g. full disk)
  if { date -u +%FT%TZ; echo "ALIVE=$(alive)"; printf '%s\n' "${STATUS_LINES[@]}"
      echo "SUPERVISOR lane=$N version=$VER sv=${MYSUM:0:12} head=$(git -C "$R" rev-parse --short HEAD 2>/dev/null) assign=$(sha256sum "$R/lanes/assign/$N.txt" 2>/dev/null | cut -c1-8) mode=$MODE sha256sums=$SHAMSG pull=$pulled push=$PM${PMWHY:+($PMWHY)} up=$(( now - START ))s pid=$$"
      for x in "${ALERTS[@]}"; do echo "ALERT $x"; done; for x in "${NOTES[@]}"; do echo "NOTE $x"; done
      [ -f "$W/HALT_OMF" ] && sed 's/^/ORIGINAL_MODEL_FOUND /' "$W/HALT_OMF"; true
    } > "$W/status.txt.new" 2>/dev/null && grep -q '^SUPERVISOR' "$W/status.txt.new" 2>/dev/null; then
    local key; key=$(sed 1d "$W/status.txt.new" | sed -E 's/closed=[0-9]+ open=[0-9]+//; s/ up=[0-9]+s//; s/[0-9]+ s/N s/g')
    mv -f "$W/status.txt.new" "$W/status.txt"
    if [ "${FORCEBEAT:-0}" = 1 ] || [ "$key" != "${LASTKEY:-}" ] || [ $((now - ${LASTBEAT:-0})) -ge "$BEAT" ]; then
      if beat_gh_wrapped; then LASTBEAT=$now; LASTKEY=$key; FORCEBEAT=0; else say "heartbeat push failed"; fi
    fi
  else rm -f "$W/status.txt.new" 2>/dev/null; say "status.txt could not be written"; fi
}

# ---- between ticks: gentle stops (poll every 5 s)
soft_stops() {   # stop files run/KEY.stop: "WHY T0 LOGSIZE PID STATEDIR"; only that pid (a strict match) is killed
  local f K why t0 sz0 xp xs sz P
  P=$(procs)
  for f in "$W"/run/*.stop; do [ -f "$f" ] || continue; K=$(basename "$f" .stop); read -r why t0 sz0 xp xs < "$f"
    isnum "${t0:-}" || t0=$(date +%s); isnum "${sz0:-}" || sz0=0
    echo "$P" | awk -v p="${xp:-x}" '$1 == p {f=1} END {exit !f}' || { rm -f "$f"; continue; }
    [ "$(tree_open "$xs")" = 0 ] && continue                       # stitching the final proof: never interrupted
    sz=$(stat -c %s "$xs/log.jsonl" 2>/dev/null || echo 0)
    if [ "$sz" != "$sz0" ] || [ $(( $(date +%s) - t0 )) -ge "$SOFT_MAX" ]; then
      [ "$sz" != "$sz0" ] && { sleep 1; [ "$(tree_open "$xs")" = 0 ] && continue; }
      mark_killed "$K"; kill_tree "$xp"; rm -f "$f"; say "stopped ${K%.v9} pid $xp ($why, $([ "$sz" != "$sz0" ] && echo "at a cube boundary" || echo "no cube boundary within $SOFT_MAX s"))"; fi
  done
}

main() {
  START=$(date +%s); MYSUM=$(sha256sum "$SELF" | cut -c1-64)
  if [ -x "${SV_VENV:-$BASE/sat-venv}/bin/python3" ]; then export PATH="${SV_VENV:-$BASE/sat-venv}/bin:$PATH"; fi
  git -C "$R" config core.fileMode false 2>/dev/null
  echo "$N" > "$W/lane" 2>/dev/null   # read by an environment maintenance script, which is shared by all lanes and cannot know N
  # fresh start (not a self-upgrade): solvers that died with the previous supervisor are not counted as failures
  [ "${SV_EXEC:-}" = 1 ] || rm -f "$W"/run/*.nexit "$W"/run/*.wpid "$W"/run/*.killed
  unset SV_EXEC
  say "supervise.sh $N start (pid $$, sv ${MYSUM:0:12}, repo $R, base $BASE, scope '${SCOPE}')"
  FORCEBEAT=1
  while :; do
    tick
    local k; for k in $(seq 1 $(( (TICK + 4) / 5 ))); do sleep 5; soft_stops; done
    [ "$(stat -c %s "$LOG" 2>/dev/null || echo 0)" -gt 5000000 ] && mv -f "$LOG" "$LOG.1"
  done
}
main "$@"; exit
