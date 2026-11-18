#!/bin/bash
# gh_probe.sh [OWNER/REPO] - one-shot smoke test of the gh-api publishing path, to run ONCE by hand on a lane.
# Creates one small blob and one 32 MiB blob (random bytes, sent base64), a throw-away tree holding both, a second
# tree from it with the large file deleted (base_tree + sha null, as the publisher does) and a parentless commit. It creates NO ref: nothing becomes visible on any branch, and the objects stay
# unreferenced until GitHub's garbage collection. Prints OK or the first error, with sizes and timings.
# Default repo: read from the origin remote of /workspace/r. Override the large size with GH_PROBE_MB (default 32).
set -u
REPO=${1:-$(git -C /workspace/r remote get-url origin 2>/dev/null | sed -nE 's#^.*github\.com[:/]+([A-Za-z0-9._-]+/[A-Za-z0-9._-]+)$#\1#p' | sed 's/\.git$//')}
MB=${GH_PROBE_MB:-32}
[[ $REPO =~ ^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$ ]] || { echo "ERROR: repo unknown (give OWNER/REPO)"; exit 2; }
[[ $MB =~ ^[0-9]{1,3}$ ]] || { echo "ERROR: GH_PROBE_MB must be a number of MiB"; exit 2; }
command -v gh > /dev/null || { echo "ERROR: gh is not installed"; exit 1; }
D=$(mktemp -d) || exit 1; trap 'rm -rf "$D"' EXIT
t() { date +%s.%N; }
dt() { python3 -c "import sys; print(f'{float(sys.argv[2]) - float(sys.argv[1]):.2f} s')" "$1" "$2"; }
fail() { echo "ERROR at $1: $(tail -c 600 "$D/err" 2>/dev/null)"; exit 1; }
jget() { python3 -I -c 'import sys,json
d=json.load(sys.stdin)
for k in sys.argv[1].split("."): d=d[k]
print(d)' "$1"; }
blobjson() { python3 -I -c 'import sys,base64
with open(sys.argv[1],"rb") as fi, open(sys.argv[2],"w") as fo:
    fo.write("{\"encoding\": \"base64\", \"content\": \""); fo.write(base64.b64encode(fi.read()).decode()); fo.write("\"}")' "$1" "$2"; }
echo "repo $REPO, large blob $MB MiB"
gh auth status > "$D/err" 2>&1 || fail "gh auth status"
a=$(t); gh api "repos/$REPO" > "$D/repo.json" 2> "$D/err" || fail "GET repos/$REPO"; b=$(t)
echo "GET repos/$REPO: ok ($(dt $a $b)), push permission: $(jget permissions.push < "$D/repo.json" 2>/dev/null || echo unknown)"
echo "gh_probe small blob $(date -u +%FT%TZ)" > "$D/small"
head -c $((MB * 1048576)) /dev/urandom > "$D/large" || fail "making the $MB MiB file"
for f in small large; do
  blobjson "$D/$f" "$D/$f.json" || fail "encoding $f"
  a=$(t); gh api -X POST "repos/$REPO/git/blobs" --input "$D/$f.json" > "$D/$f.out" 2> "$D/err" || fail "POST git/blobs ($f)"; b=$(t)
  s=$(jget sha < "$D/$f.out") || fail "reading the $f blob sha"
  [ "$s" = "$(git hash-object "$D/$f")" ] || { echo "ERROR: the $f blob sha $s differs from the local git hash"; exit 1; }
  echo "blob $f: $(stat -c %s "$D/$f") bytes, request body $(stat -c %s "$D/$f.json") bytes, $(dt $a $b), sha $s (matches git hash-object)"
  eval "SHA_$f=$s"
done
printf '{"tree": [{"path": "probe/small.txt", "mode": "100644", "type": "blob", "sha": "%s"}, {"path": "probe/large.bin", "mode": "100644", "type": "blob", "sha": "%s"}]}' "$SHA_small" "$SHA_large" > "$D/tree.json"
a=$(t); gh api -X POST "repos/$REPO/git/trees" --input "$D/tree.json" > "$D/tree.out" 2> "$D/err" || fail "POST git/trees"; b=$(t)
TREE=$(jget sha < "$D/tree.out"); echo "tree: $TREE ($(dt $a $b))"
printf '{"base_tree": "%s", "tree": [{"path": "probe/large.bin", "mode": "100644", "type": "blob", "sha": null}]}' "$TREE" > "$D/tree2.json"
a=$(t); gh api -X POST "repos/$REPO/git/trees" --input "$D/tree2.json" > "$D/tree2.out" 2> "$D/err" || fail "POST git/trees (delete probe/large.bin via sha null)"; b=$(t)
TREE2=$(jget sha < "$D/tree2.out")
gh api "repos/$REPO/git/trees/$TREE2?recursive=1" > "$D/tree2.list" 2> "$D/err" || fail "GET git/trees (after the deletion)"
LEFT=$(python3 -I -c 'import sys,json; print(" ".join(sorted(e["path"] for e in json.load(open(sys.argv[1]))["tree"] if e["type"] == "blob")))' "$D/tree2.list")
[ "$LEFT" = "probe/small.txt" ] || { echo "ERROR: null deletion did not work: the new tree holds: $LEFT"; exit 1; }
echo "tree with probe/large.bin deleted (base_tree + sha null): $TREE2 ($(dt $a $b)); holds only probe/small.txt"
printf '{"message": "gh_probe throw-away commit (no ref points here)", "tree": "%s", "parents": []}' "$TREE" > "$D/commit.json"
a=$(t); gh api -X POST "repos/$REPO/git/commits" --input "$D/commit.json" > "$D/commit.out" 2> "$D/err" || fail "POST git/commits"; b=$(t)
echo "commit: $(jget sha < "$D/commit.out") ($(dt $a $b)); no ref was created"
echo "OK"
