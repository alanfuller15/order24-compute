#!/bin/bash
# exp/lratcatch_trial.sh LAYER [K] [BLOCK] [cake_text] [noneg]   (research only: nothing here produces or approves a record)
#
# Can lrat-catcher (github.com/leansolving/lrat-catcher, MIT, Lean 4 v4.30.0) check one of our recorded LRAT proofs,
# as an independent second checker next to cake_lpr, with memory bounded by the live clauses?
#
# Inputs (environment, set by exp.yml from its dispatch inputs):
#   TAG       the record's tag (e.g. L79_s10a4b18c57_0007)
#   RUN_ID    producer run id holding the artifact, ARTIFACT its name (e.g. m79c-h02); GH_TOKEN (actions:read) and
#             GH_REPO for `gh run download`. Without RUN_ID, IN_DIR must name a folder with results.jsonl and proofs/.
#   K         compaction period in feed blocks (arg 2, default 64); BLOCK lines per feed block (arg 3, default 4096,
#             lrat-catcher's own default; the feed and the renumbering tool must use the same value).
#   options (args 4..): cake_text = CAKE_TEXT=1, noneg = NEG=0.
#   NEG=1     (default) also run a negative control: the same stream with one addition's hints replaced by "1"
#             (must be rejected).  CAKE_TEXT=1 (default 0): also run the pinned cake_lpr on the converted TEXT proof,
#             showing cake_lpr accepts the same text that was fed (after renumbering) to lrat-catcher.
#   WORK      work folder (default /mnt/lratcatch when it can be made, else $RUNNER_TEMP/lratcatch, else ./exp_work).
#
# Steps: pins of audit_kit/l<LAYER>; download the artifact; take the one record with TAG; rebuild its CNF with the
# pinned checker's own module (exp/lratcatch_cnf.py: audit_kit/l<LAYER>/code/gcert<LAYER>.py, its ENC table and the
# exact to_fp bytes) and stop unless its SHA-256 is the record's cnf_sha256; stop unless the proof file's SHA-256 is the
# record's proof_sha256; install elan + Lean v4.30.0 (commit pinned below), clone lrat-catcher at a pinned commit and
# build LRATCatcher.StreamOracle and lratcatch-compact-renumber; then stream
#     xz -dc proof | lratcatch_bin2txt | lratcatch-compact-renumber base.cnf - - K --block BLOCK  >  FIFO
# into a generated module that runs
#     lrat_stream_cnf_compact trial_unsat (LRATCatcher.parseDimacs (include_str "base.cnf")) "FIFO" K
# (checkStreamCnfC: the clause array is compacted every K blocks, so memory follows the live clauses, not the id
# space). Nothing of the proof is stored on disk. Recorded in exp_out/: summary.json (verdict, wall times, peak RSS,
# disk use, axioms), check.log (lake/lean output: theorem and #print axioms), *.time (/usr/bin/time -v), mem.log
# (5 s samples), converter and renumbering statistics. SIGINT/SIGTERM (exp.yml's timeout) stops every child and still
# writes summary.json with "interrupted": true.
set -u -o pipefail
ROOT=$PWD; OUT=$ROOT/exp_out; mkdir -p "$OUT"
LAYER=${1:-}; K=${2:-64}; BLOCK=${3:-4096}; TAG=${TAG:-}; RUN_ID=${RUN_ID:-}; ARTIFACT=${ARTIFACT:-}
NEG=${NEG:-1}; CAKE_TEXT=${CAKE_TEXT:-0}
for a in "${@:4}"; do case "$a" in cake_text) CAKE_TEXT=1;; noneg) NEG=0;; *) echo "unknown option $a"; exit 2;; esac; done
LC_URL=https://github.com/leansolving/lrat-catcher
LC_COMMIT=cbc980a934cfcfbd942462c7b6db2e88750e4874          # main on 2026-11-13 ("Tests: two streamed imports ...")
LEAN_TC=leanprover/lean4:v4.30.0
LEAN_COMMIT=d024af099ca4bf2c86f649261ebf59565dc8c622        # `lean --version` of v4.30.0
CAKE_PIN=29e02af756c1f0fc4ccac78e9a908e0d8ef01201786f257f1b27b26603390798
S=$OUT/summary.kv; : > "$S"; T0=$(date +%s.%N); INTERRUPTED=0; STAGE=start

put() { printf '%s\t%s\n' "$1" "$2" >> "$S"; }                 # put KEY JSON-VALUE
puts() { put "$1" "$(python3 -I -c 'import json,sys; print(json.dumps(sys.argv[1]))' "$2")"; }
putf() { put "$1" "$(python3 -I -c 'import json,sys; print(json.dumps(json.load(open(sys.argv[1]))))' "$2")"; }   # a JSON file
now() { date +%s.%N; }
el() { python3 -I -c 'import sys; print(round(float(sys.argv[2]) - float(sys.argv[1]), 1))' "$1" "$(now)"; }
log() { echo "$(date -u +%T) [$STAGE] $*"; }
killtree() { local p; for p in $(pgrep -P "$1" 2>/dev/null); do killtree "$p"; done; kill -TERM "$1" 2>/dev/null; }
finish() {
  local rc=$?
  [ -n "${SAMP:-}" ] && kill "$SAMP" 2>/dev/null
  for p in $(jobs -p); do killtree "$p"; done
  put interrupted "$([ $INTERRUPTED = 1 ] && echo true || echo false)"; puts stopped_at_stage "$STAGE"
  put total_seconds "$(el "$T0")"; put script_exit "$rc"
  df -B1 --output=target,used,avail / /mnt 2>/dev/null > "$OUT/df_end.txt"
  python3 -I - "$S" "$OUT/summary.json" <<'EOF'
import json, sys
d = {}
for line in open(sys.argv[1]):
    k, _, v = line.rstrip('\n').partition('\t')
    try: d[k] = json.loads(v)
    except ValueError: d[k] = v
json.dump(d, open(sys.argv[2], 'w'), indent=1); print(json.dumps(d, indent=1))
EOF
}
on_int() { INTERRUPTED=1; log "interrupted"; for p in $(jobs -p); do killtree "$p"; done; exit 130; }
trap finish EXIT; trap on_int INT TERM
stop() { puts verdict "STOPPED: $*"; log "STOP: $*"; exit 1; }
# run a long step in the background and wait for it, so that SIGINT is handled at once (bash defers traps while a
# foreground child runs)
bgw() { "$@" & local p=$!; wait $p; }

case "$LAYER" in ''|*[!0-9]*) stop "usage: lratcatch_trial.sh LAYER [K] [BLOCK] (TAG, RUN_ID, ARTIFACT in the environment)";; esac
case "$K$BLOCK" in *[!0-9]*) stop "K and BLOCK must be numbers";; esac
[[ "$TAG" =~ ^L${LAYER}_s[0-9]+a[0-9]+b[0-9]+c[0-9]+_[0-9]{4}$ ]] || stop "TAG '$TAG' is not a layer-$LAYER tag"
[ "$K" -ge 1 ] && [ "$BLOCK" -ge 1 ] || stop "K and BLOCK must be >= 1"
puts tag "$TAG"; put layer "$LAYER"; put K "$K"; put block "$BLOCK"; put neg_enabled "$NEG"; put cake_text_enabled "$CAKE_TEXT"; puts run_id "$RUN_ID"; puts artifact "$ARTIFACT"
puts lrat_catcher_commit "$LC_COMMIT"; puts lean_toolchain "$LEAN_TC"; puts mode "lrat_stream_cnf_compact (checkStreamCnfC)"
nproc > "$OUT/machine.txt"; free -m >> "$OUT/machine.txt"; df -h / /mnt >> "$OUT/machine.txt" 2>&1; uname -a >> "$OUT/machine.txt"
df -B1 --output=target,used,avail / /mnt 2>/dev/null > "$OUT/df_start.txt"

# ---- work folder (/mnt has the most room on GitHub runners)
if [ -z "${WORK:-}" ]; then
  if sudo -n mkdir -p /mnt/lratcatch 2>/dev/null && sudo -n chown "$(id -u):$(id -g)" /mnt/lratcatch; then WORK=/mnt/lratcatch
  elif [ -n "${RUNNER_TEMP:-}" ]; then WORK=$RUNNER_TEMP/lratcatch; else WORK=$ROOT/exp_work; fi
fi
mkdir -p "$WORK"; W=$WORK; puts work_dir "$W"
[ -x /usr/bin/time ] || sudo -n apt-get install -y -q time > /dev/null 2>&1 || true
[ -x /usr/bin/time ] || stop "/usr/bin/time is needed (apt-get install time)"

# ---- memory sampler: total memory and every lean / pipeline process, every 5 s
( while true; do
    echo "$(date -u +%T) $(free -m | awk '/Mem:/{print "used="$3" avail="$7}') $(for p in $(pgrep -x lean; pgrep -f lratcatch-compact-renumber; pgrep -f lratcatch_bin2txt; pgrep -x cake_lpr); do echo "$(cat /proc/$p/comm 2>/dev/null):$p $(grep -h -E 'VmRSS|VmHWM' /proc/$p/status 2>/dev/null | tr -s ' ' | tr '\n' ' ')"; done | tr '\n' ';')"
    sleep 5; done ) > "$OUT/mem.log" 2>&1 &
SAMP=$!

# ---- 1. pins of the audit kit (the encoder sources the CNF rebuild uses)
STAGE=pins; t=$(now)
(cd "audit_kit/l$LAYER" && sha256sum -c PINS.sha256) > "$OUT/pins.txt" 2>&1 || stop "audit_kit/l$LAYER pins do not match"
echo "$CAKE_PIN  bin/cake_lpr" | sha256sum -c >> "$OUT/pins.txt" 2>&1 || stop "bin/cake_lpr is not the pinned binary"

# ---- 2. the producer artifact
STAGE=download; t=$(now)
if [ -n "$RUN_ID" ]; then
  [ -n "$ARTIFACT" ] || stop "RUN_ID given without ARTIFACT"
  [[ "$RUN_ID" =~ ^[0-9]+$ && "$ARTIFACT" =~ ^[A-Za-z0-9_.-]+$ ]] || stop "bad RUN_ID or ARTIFACT"
  IN=$W/in; rm -rf "$IN"
  log "gh run download $RUN_ID -n $ARTIFACT"
  bgw gh run download "$RUN_ID" -n "$ARTIFACT" -D "$IN" > "$OUT/download.log" 2>&1 || stop "artifact download failed (see download.log)"
else
  IN=${IN_DIR:-$ROOT/in}; [ -d "$IN" ] || stop "no RUN_ID and no IN_DIR"
fi
put download_seconds "$(el "$t")"; put artifact_bytes "$(du -sb "$IN" | cut -f1)"
P=$IN/proofs/$TAG.lrat.xz
[ -f "$P" ] && [ ! -L "$P" ] || stop "$P is not a regular file"
[ -f "$IN/results.jsonl" ] || stop "no results.jsonl in the artifact"
python3 -I - "$IN/results.jsonl" "$TAG" "$OUT/record.json" <<'EOF' || stop "the artifact does not hold exactly one record with this tag"
import json, sys, hashlib
lines = [l for l in open(sys.argv[1]) if l.strip() and json.loads(l).get('tag') == sys.argv[2]]
if len(lines) != 1: sys.exit(1)
r = json.loads(lines[0]); n = len(r.pop('lazy'))
r['lazy_items'] = n; r['record_line_sha256'] = hashlib.sha256(lines[0].rstrip('\n').encode()).hexdigest()
json.dump(r, open(sys.argv[3], 'w'), indent=1)
EOF
REC() { python3 -I -c 'import json,sys; v=json.load(open(sys.argv[1])).get(sys.argv[2]); print("" if v is None else v)' "$OUT/record.json" "$1"; }
putf record "$OUT/record.json"

# ---- 3. the CNF, rebuilt as the audit does; its SHA-256 must be the record's
STAGE=cnf; t=$(now)
python3 -I -B exp/lratcatch_cnf.py "$LAYER" "$IN/results.jsonl" "$TAG" "$W/base.cnf" "$OUT/cnf_info.json" > "$OUT/cnf.log" 2>&1 \
  || { cat "$OUT/cnf.log"; stop "CNF rebuild failed or its SHA-256 differs from the record's cnf_sha256"; }
putf cnf "$OUT/cnf_info.json"; put cnf_seconds "$(el "$t")"
CNF_SHA=$(REC cnf_sha256); MAXVAR=$(python3 -I -c 'import json,sys; print(json.load(open(sys.argv[1]))["max_var"])' "$OUT/cnf_info.json")
NCL=$(python3 -I -c 'import json,sys; print(json.load(open(sys.argv[1]))["clauses"])' "$OUT/cnf_info.json")
CNF_BYTES=$(stat -c %s "$W/base.cnf")
[ "$(sha256sum < "$W/base.cnf" | cut -d' ' -f1)" = "$CNF_SHA" ] || stop "base.cnf on disk differs from cnf_sha256"
chmod 444 "$W/base.cnf"

# ---- 4. the proof file's SHA-256 must be the record's
STAGE=proof_hash; t=$(now)
PSHA=$(sha256sum < "$P" | cut -d' ' -f1)
puts proof_sha256_file "$PSHA"
[ "$PSHA" = "$(REC proof_sha256)" ] || stop "proof SHA-256 differs from the record's proof_sha256"
put proof_xz_bytes_file "$(stat -c %s "$P")"; put proof_hash_seconds "$(el "$t")"

# ---- 5. Lean toolchain and lrat-catcher at the pinned commit
STAGE=toolchain; t=$(now)
export PATH=$HOME/.elan/bin:$PATH
if ! command -v elan > /dev/null; then
  curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -o "$W/elan-init.sh" || stop "elan download failed"
  puts elan_init_sha256 "$(sha256sum < "$W/elan-init.sh" | cut -d' ' -f1)"
  bgw sh "$W/elan-init.sh" -y --default-toolchain none > "$OUT/elan.log" 2>&1 || stop "elan install failed"
fi
bgw elan toolchain install "$LEAN_TC" >> "$OUT/elan.log" 2>&1 || stop "toolchain install failed"
LC=$W/lc; rm -rf "$LC"
bgw git clone -q "$LC_URL" "$LC" > "$OUT/clone.log" 2>&1 || stop "clone failed"
git -C "$LC" checkout -q "$LC_COMMIT" || stop "pinned commit not found"
[ "$(git -C "$LC" rev-parse HEAD)" = "$LC_COMMIT" ] || stop "HEAD is not the pinned commit"
[ "$(tr -d '[:space:]' < "$LC/lean-toolchain")" = "$LEAN_TC" ] || stop "lrat-catcher's lean-toolchain is not $LEAN_TC"
LV=$(cd "$LC" && lean --version); puts lean_version "$LV"
[[ "$LV" == *"$LEAN_COMMIT"* ]] || stop "lean is not the pinned v4.30.0 build"
put toolchain_seconds "$(el "$t")"
STAGE=build; t=$(now)
(cd "$LC" && bgw lake build LRATCatcher.StreamOracle lratcatch-compact-renumber) > "$OUT/lake_build.log" 2>&1 || stop "lake build failed"
put build_seconds "$(el "$t")"
gcc -O2 -Wall -o "$W/bin2txt" exp/lratcatch_bin2txt.c > "$OUT/gcc.log" 2>&1 || stop "converter does not compile"
RENUM=$LC/.lake/build/bin/lratcatch-compact-renumber
mkdir -p "$LC/LRATCatcher/Trial"; cp "$W/base.cnf" "$LC/LRATCatcher/Trial/base.cnf"; chmod 444 "$LC/LRATCatcher/Trial/base.cnf"

# ---- 6. the streamed check
# gen_module NAME THEOREM FIFO: a fresh module (a nonce in a comment: Lake replays earlier failed builds of identical
# source from its cache)
gen_module() {
  cat > "$LC/LRATCatcher/Trial/$1.lean" <<EOF
import LRATCatcher.StreamOracle
-- lratcatch trial: tag $TAG, cnf_sha256 $CNF_SHA, proof_sha256 $PSHA, K $K, block $BLOCK, nonce $(date +%s%N)
namespace LRATCatcher.Trial

lrat_stream_cnf_compact $2 (LRATCatcher.parseDimacs (include_str "base.cnf")) "$3" $K

/-- the statement, spelled out: the DIMACS bytes of base.cnf, parsed by lrat-catcher's parseDimacs, are unsatisfiable -/
theorem $2_stmt : (LRATCatcher.parseDimacs (include_str "base.cnf")).Unsat := $2

#print axioms $2_stmt
#eval s!"cnf_bytes_in_statement {(include_str "base.cnf").utf8ByteSize}"

end LRATCatcher.Trial
EOF
}
# run_check NAME THEOREM FILTER: stream the proof through FILTER (a shell command between the converter and the
# renumbering; "cat" for the real check) into a FIFO read by `lake build LRATCatcher.Trial.NAME:olean`
run_check() {
  local name=$1 thm=$2 filt=$3 fifo=$W/$1.fifo
  rm -f "$fifo"; mkfifo "$fifo"; gen_module "$name" "$thm" "$fifo"
  ( xz -T1 -dc "$P" | "$W/bin2txt" "$MAXVAR" "$NCL" "$OUT/${name}_bin2txt.json" | bash -c "$filt" \
      | "$RENUM" "$W/base.cnf" - - "$K" --block "$BLOCK" 2> "$OUT/${name}_renumber.log" > "$fifo"
    echo "${PIPESTATUS[*]}" > "$OUT/${name}_pipe.status" ) &
  local pipe=$!
  ( cd "$LC" && ulimit -s unlimited 2>/dev/null; LRATCATCHER_STREAM_BLOCK=$BLOCK \
      /usr/bin/time -v -o "$OUT/${name}.time" lake build "LRATCatcher.Trial.$name:olean" > "$OUT/${name}.log" 2>&1 ) &
  local lk=$!; wait $lk; local lrc=$?
  sleep 2; if kill -0 $pipe 2>/dev/null; then killtree $pipe; fi; wait $pipe 2>/dev/null
  rm -f "$fifo"; return $lrc
}
# analyse NAME THEOREM LAKE_EXIT: axioms, sorry, statement size, peak RSS, converter statistics -> summary
analyse() {
python3 -I - "$OUT" "$1" "$2" "$CNF_BYTES" "$3" >> "$S" <<'EOF'
import json, re, sys, os
out, name, thm, cnf_bytes, rc = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
log = open(os.path.join(out, name + '.log'), errors='replace').read()
flat = re.sub(r'\s+', ' ', log)
m = re.search(r"'LRATCatcher\.Trial\.%s_stmt' depends on axioms: \[([^\]]*)\]" % thm, flat)
ax = [a.strip() for a in m.group(1).split(',')] if m else None
std = {'propext', 'Classical.choice', 'Quot.sound'}
nat = [a for a in (ax or []) if a not in std]
ax_ok = ax is not None and std <= set(ax) and len(nat) == 1 and re.fullmatch(r'(LRATCatcher\.Trial\.)?%s\._native\.native_decide\.ax_1(_1)?' % thm, nat[0]) is not None
mb = re.search(r'cnf_bytes_in_statement (\d+)', flat)
tv = {}
try:
    for l in open(os.path.join(out, name + '.time')):
        k, _, v = l.strip().rpartition(': ')
        tv[k] = v
except OSError: pass
def j(k, v): print(f'{k}\t{json.dumps(v)}')
st = {}
try: st = json.load(open(os.path.join(out, name + '_bin2txt.json')))
except (OSError, ValueError): pass
j(name + '_axioms', ax); j(name + '_axioms_ok', ax_ok); j(name + '_sorry', 'sorryAx' in log)
j(name + '_errors', len(re.findall(r'(?m)^error', log)))
j(name + '_cnf_bytes_in_statement', int(mb.group(1)) if mb else None)
j(name + '_peak_rss_kb', int(tv['Maximum resident set size (kbytes)']) if 'Maximum resident set size (kbytes)' in tv else None)
j(name + '_wall', tv.get('Elapsed (wall clock) time (h:mm:ss or m:ss)'))
j(name + '_converter', st)
# a failed native_decide prints the whole statement (the CNF as a string literal): keep the log readable and small
with open(os.path.join(out, name + '.log'), 'w') as fo:
    for l in log.split('\n'):
        fo.write((l if len(l) <= 4000 else l[:2000] + f' ...[{len(l) - 2000} characters cut by lratcatch_trial.sh]') + '\n')
ok = rc == 0 and ax_ok and 'sorryAx' not in log and mb is not None and int(mb.group(1)) == cnf_bytes and st.get('empty_clauses', 0) >= 1
j(name + '_verified', ok)
EOF
}
STAGE=check; t=$(now); log "streaming check, K=$K block=$BLOCK"
bgw run_check Check trial_unsat cat; CRC=$?
put check_seconds "$(el "$t")"; put check_lake_exit "$CRC"
[ "$(sha256sum < "$LC/LRATCatcher/Trial/base.cnf" | cut -d' ' -f1)" = "$CNF_SHA" ] && put cnf_unchanged_after_check true || put cnf_unchanged_after_check false
analyse Check trial_unsat "$CRC"
cp "$LC/LRATCatcher/Trial/Check.lean" "$OUT/Check.lean.txt" 2>/dev/null
puts renumber_log "$(cat "$OUT/Check_renumber.log" 2>/dev/null)"
puts pipe_status "$(cat "$OUT/Check_pipe.status" 2>/dev/null)"
VER=$(grep -P '^Check_verified\t' "$S" | cut -f2)
if [ "$VER" = true ]; then puts verdict "VERIFIED: lrat-catcher proved (parseDimacs <base.cnf bytes>).Unsat"; else puts verdict "NOT VERIFIED (see Check.log)"; fi
log "check: lake exit $CRC, verified=$VER"

# ---- 7. negative control: one addition's hints replaced by the single hint 1, just after the first compaction (or at
#      the middle line of a proof shorter than K*BLOCK lines)
if [ "$NEG" = 1 ]; then
  STAGE=negative; t=$(now)
  NL=$(python3 -I -c 'import json,sys; print(json.load(open(sys.argv[1])).get("lines", 0))' "$OUT/Check_bin2txt.json" 2>/dev/null || echo 0)
  N=$(( K * BLOCK + 3 )); [ "$NL" -gt 4 ] && [ $(( NL / 2 )) -lt "$N" ] && N=$(( NL / 2 ))   # after the first compaction, or mid-proof
  put neg_line "$N"
  bgw run_check Neg neg_unsat "awk -v n=$N 'NR>=n && !d && \$2!=\"d\" { for (i=2;i<=NF;i++) if (\$i==\"0\") break; s=\$1; for (k=2;k<=i;k++) s=s\" \"\$k; print s\" 1 0\"; d=1; next } 1'"; NRC=$?
  put neg_seconds "$(el "$t")"; put neg_lake_exit "$NRC"
  analyse Neg neg_unsat "$NRC"
  if [ "$NRC" != 0 ] && [ "$(grep -P '^Neg_verified\t' "$S" | cut -f2)" = false ]; then put neg_control_rejected true; else put neg_control_rejected false; fi
fi

# ---- 8. optional cross-check: cake_lpr on the converted text proof (the text the renumbering started from)
if [ "$CAKE_TEXT" = 1 ]; then
  STAGE=cake_text; t=$(now)
  bgw bash -c "xz -T1 -dc '$P' | '$W/bin2txt' $MAXVAR $NCL '$OUT/cake_bin2txt.json' > '$W/proof.txt'"
  put text_proof_bytes "$(stat -c %s "$W/proof.txt")"
  for heap in 4000 8000; do
    bgw /usr/bin/time -v -o "$OUT/cake_text.time" bin/cake_lpr --CML_HEAP_SIZE=$heap --CML_STACK_SIZE=256 "$W/base.cnf" "$W/proof.txt" > "$OUT/cake_text.out" 2>&1
    grep -q '^s ' "$OUT/cake_text.out" && break
  done
  puts cake_text_result "$(head -c 300 "$OUT/cake_text.out")"; put cake_text_heap_mb "$heap"; put cake_text_seconds "$(el "$t")"
  rm -f "$W/proof.txt"
fi

STAGE=done
put disk_lean_toolchain_bytes "$(du -sb "$HOME/.elan" 2>/dev/null | cut -f1)"
put disk_lrat_catcher_bytes "$(du -sb "$LC" 2>/dev/null | cut -f1)"
put disk_work_bytes "$(du -sb "$W" 2>/dev/null | cut -f1)"
[ "$VER" = true ]
