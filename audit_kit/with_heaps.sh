#!/bin/bash
# with_heaps.sh HEAPS M TAGS_REGEX -- run_audit.sh with the pinned checker's cake_lpr heap list set to HEAPS.
# Used by audit.yml only when its optional input cake_heaps is non-empty; with it empty, audit.yml runs
# audit_kit/run_audit.sh exactly as before and this file is not used.
#
# Why: run_audit.sh starts gcert<M>.py under `env -i`, so the checker always uses its default heaps "2000,4000"
# (gcert<M>.py reads CAKE_HEAPS, documented in its docstring: "CAKE_HEAPS, default 2000,4000"). Some recorded proofs
# need a larger heap (L82_s10a4b18c60_0001: heap exhausted at 2000 and 4000, verified at 12000).
#
# What: audit_kit/run_audit.sh stays byte-identical in the repo (its SHA-256 is pinned by exp/rep_proof.sh and counted by
# exp/rep_proof/collect.py). This script checks that SHA-256, writes a copy with ONE changed line -- CAKE_HEAPS=HEAPS
# added to the checker's `env -i` list -- and runs that copy. The checker, its code hash, the formulas, cake_lpr and
# the negative controls are unchanged. The change is logged in aout/ (uploaded with the audit outputs):
#   aout/cake_heaps.txt        the heap list used
#   aout/run_audit_heaps.diff  diff of run_audit.sh -> the copy run (exactly one line removed, one added)
#   aout/run_audit_heaps.sha256  SHA-256 of both
# The checker writes the heap that gave its verdict per formula (cake_heap_mb in CHECK_RESULTS.jsonl).
# HEAPS: 1 to 4 comma-separated integers in MB, each 1000..16000, no spaces, no leading zeros; anything else is refused
# (exit 2) before anything runs.
set -u
RUN_AUDIT_SHA=69e79abe66e68205153f78b97e132d13d7bf31515b9f7b365c12be16760868f5   # audit_kit/run_audit.sh at 30091e7
H=${1:-}; [ $# -eq 3 ] || { echo "usage: with_heaps.sh HEAPS M TAGS_REGEX" >&2; exit 2; }
shift
[[ "$H" =~ ^[1-9][0-9]{3,4}(,[1-9][0-9]{3,4}){0,3}$ ]] || { echo "cake heaps '$H' refused: need 1-4 comma-separated integers (MB)" >&2; exit 2; }
for h in ${H//,/ }; do [ "$h" -ge 1000 ] && [ "$h" -le 16000 ] || { echo "cake heap $h refused: outside 1000..16000 MB" >&2; exit 2; }; done
R=$PWD; S=$R/audit_kit/run_audit.sh; P=$R/work/run_audit_heaps.sh
echo "$RUN_AUDIT_SHA  $S" | sha256sum -c --quiet || { echo "audit_kit/run_audit.sh is not the pinned script" >&2; exit 2; }
mkdir -p "$R/work" "$R/aout"
sed "s|HOME=\$HOME PARTIAL_RECORDS=1 python3 |HOME=\$HOME PARTIAL_RECORDS=1 CAKE_HEAPS=$H python3 |" "$S" > "$P"
diff "$S" "$P" > "$R/aout/run_audit_heaps.diff"
[ "$(grep -c '^[<>]' "$R/aout/run_audit_heaps.diff")" = 2 ] && [ "$(grep -c "CAKE_HEAPS=$H python3 " "$P")" = 1 ] \
  || { echo "run_audit.sh rewrite did not change exactly one line" >&2; exit 2; }
echo "$H" > "$R/aout/cake_heaps.txt"; sha256sum "$S" "$P" > "$R/aout/run_audit_heaps.sha256"
exec bash "$P" "$@"
