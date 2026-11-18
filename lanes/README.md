# lanes/: self-healing supervisor for the Codex lanes

Each Codex lane runs one `lanes/supervise.sh N` loop (N = lane number) in its clone `/workspace/r`. The loop reads
what to run from this folder, so a retarget or a code upgrade is a commit here, not a message to the lane. The one
message a lane still needs is the REPAIR line after its container was restarted (the restart kills every process).

## Files

| file | what | who edits |
|---|---|---|
| `supervise.sh` | the loop; it and `worker.sh` must be listed in `SHA256SUMS` (else nothing starts) | manager, pinned |
| `VERSION` | one token; any change restarts every assigned solver from its saved state (MODE run only) | manager |
| `assign/N.txt` | lane N's solvers | manager |

`assign/N.txt`, one solver per line (comments with `#`):

```
MODE run                                   # or: fill
ENV CUBE_DEPTH=7 EXT_TIMEOUT=3600 PYSAT_CAP=60    # lane defaults for starts (resumed trees keep their own depth)
L83_s10a4b18c61_0000 formulas83_c60.json codex-m83-lane4
L84_s10a4b18c62_0000 formulas84_c61.json codex-m84-lane4 /workspace/out84x CUBE_DEPTH=9 SEED_WAVE=m84e5
```

- 4th field OUTDIR: `-` or absent = the existing folder `/workspace/out*/cube/TAG` (or `/workspace/*/cube/TAG`)
  with the most closed cubes, else a new `/workspace/out_sv_TAG`. The choice is remembered (`/workspace/sv/run/TAG.out`).
- `MODE run`: start missing tags, stop running solvers whose tag is not listed (state folders kept), restart on a
  VERSION change, stop solvers on a lasting SHA256SUMS failure (except stitching ones).
  `MODE fill`: only start listed tags into free slots (`SV_MAX`, default 3); never stops or restarts anything (a VERSION
  change shows `upgrade pending`, a SHA256SUMS failure raises an `ALERT` and blocks starts).
  The first assignment files are best guesses and use `fill`; switch a lane to `run` once its status agrees.
- A recorded tag (UNSAT line in the results.jsonl of any known OUTDIR) is never restarted. Known OUTDIRs: those of
  running solvers, `sv/run/*.out`, folders where a solver was ever seen running (`sv/run/seen_pairs`), explicit
  assignment OUTDIRs, and every `/workspace/*/` with a `cube/` folder (all of them are scanned for ORIGINAL_MODEL_FOUND).
- Publication is automatic only for a record of tag T in folder D when the pair (D, T) was seen: a solver of T seen
  running in D, started or adopted there, or D given as T's explicit assignment OUTDIR (`sv/run/seen_pairs`) (assigned or not; unassigned ones go to `codex-m<layer>-lane<N>`); such a record keeps a
  `TAG recorded=yes published=no` line until it is published. Older records found only by the `/workspace/*/` scan are
  listed in one NOTE and published only after a line `PUBLISH TAG [BRANCH]` is added to the assignment file.
  WARNING: the BRANCH of a `PUBLISH TAG BRANCH` line must be this lane's own (`codex-m<layer>-lane<N>`, the default)
  and never another publisher's branch: a proof publish removes stale part files of that tag in the same wave folder
  (`codex/<branch without codex->/`), which would delete a part another publisher is uploading there.
- Lines are checked strictly (tag, `formulas*_c*.json` present in data/, `codex-*` branch, absolute path); a bad
  line is skipped and named in the status.

## Encoders (v7 and v9), pairs and STOP

- **An assignment line is a (TAG, ENCODER) pair**: `ENCODER=cegar90c` (encoder v7, the default) or `ENCODER=cegar90e`
  (v9), per line or as an `ENV` default; anything else is rejected. A tag may be listed once per encoder; each pair is
  its own solver, with its own state folder and its own slot (files `sv/run/TAG.*` for v7, `sv/run/TAG.v9.*` for v9).
  A running v7 solver is never stopped because a v9 line exists; it runs on as the (TAG, cegar90c) pair if that pair
  is listed (otherwise it is an unlisted solver: kept in MODE fill, stopped in MODE run). Two pairs of one tag use
  different folders, so the duplicate guard does not fire.
- **Folders**: a state folder is only ever resumed by its own encoder (`tree.json` carries `"encoder": "v7"|"v9"`;
  ccc90.py refuses a mismatch; a tree without the key counts as v7). A v9 pair without a v9 folder starts in
  `/workspace/out_sv_TAG_v9`. An explicit OUTDIR holding another encoder's tree is refused. v7 folders are never
  deleted or touched. A solver's encoder is ENCODER in `/proc/PID/environ`, else its tree's label.
- **`ENV V7_FRESH=no`**: a v7 pair only resumes an existing v7 folder and is never started fresh; without one it is
  skipped (`run=stopped … skipped (no v7 folder …)` and a NOTE). Default `yes` (old behaviour).
- **Fill order**: free slots go first to stitch-ready pairs (a tree with no open cube: the stitch is cheap), then to
  the listed pairs in file order.
- **`STOP TAG [ENCODER]`** (every mode): the tag's in-scope solver(s) of that encoder (all encoders without one) stop
  at their next cube boundary (or after SV_SOFT_MAX), never while stitching (`STOP waits: pid … is stitching`); the
  tag is never restarted, even if it is also listed; its folders are kept and any record of it is still published.
  Status: `run=stopping … (STOP: …)`, then `run=stopped enc=- (STOP)`. **STOP is the only way MODE fill stops a
  solver.** A process outside scope is never stopped (it blocks starts of its encoder's pair; unknown encoder blocks).
- A tag recorded under either encoder is never started again; records and publishing work per tag as before (a second
  record of the same tag is not published again: the branch already holds `TAG.sha256`). Status lines carry
  `enc=v7|v9` per pair.

## What one tick does (every 60 s)

1. `git fetch --no-tags origin main && git merge --ff-only FETCH_HEAD`, then `sha256sum -c SHA256SUMS` plus a check that `lanes/supervise.sh` and `worker.sh` are
   pinned. On failure nothing starts; in MODE run a failure lasting 120 s stops the solvers (not stitching ones); in
   MODE fill nothing is stopped and the status carries `ALERT SHA256SUMS FAILED`. A changed, verified `supervise.sh`
   that passes `bash -n` replaces the running loop (exec, same pid); solvers keep running.
2. ORIGINAL_MODEL_FOUND (an `ORIGINAL_MODEL_FOUND.json`, a results line, a solver log line, or `TAG ccc exit 2` in
   ccc.log, in any known OUTDIR): every other solver is killed at once (the finder gets 30 s to exit by itself), a tag
   with OMF evidence is never started again by the loop, the evidence is pushed (status + `TAG.result.json` and
   `TAG.ORIGINAL_MODEL_FOUND.json` on the publisher branch, which also makes `ingest_branch.py` stop), and the lane
   stays halted until a person deletes `/workspace/sv/HALT_OMF` (that evidence is then acknowledged; new evidence
   halts again).
3. Starts: `worker.sh ccc` with one tag per worker (`PAR=1 WINDOW=86400 PREV=/workspace/none`, FORMULAS_FILE,
   CUBE_DEPTH, EXT_TIMEOUT, PYSAT_CAP), job file `/workspace/sv/jobs/TAG/<wave>/h01.txt` (wave = SEED_WAVE or
   `m<layer>e5`, which picks the seed file `ckpt/<wave>.jsonl.xz` for a first start). Starts do not block the loop;
   only one start at a time per OUTDIR. A solver the lane started itself is adopted (not restarted). Two solvers on
   one state folder: the one running longest is kept. Two views of the processes:
   strict (used for every kill, adoption and restart): a python whose script (first argument after interpreter
   options) is `ccc90.py`, run as `ccc90.py X.json TAG /abs/OUTDIR/cube/TAG /abs/OUTDIR` with the state folder under
   `SV_SCOPE` (default `/workspace/`); loose (blocks starts, shows in the status): any python with a `ccc90.py`
   argument followed by a tag, its state path resolved through `/proc/PID/cwd` and `realpath`. Only a loose match whose
   script is ccc90.py with a `.json` next argument counts as a writer (ALIVE, free slots, duplicate guard); a
   `python -c`/`-m` or other-script process is never a reason to kill anything. A tag seen only loosely shows `running outside scope (pid ..)` and
   is never started or touched. If a newer duplicate on the same resolved folder is outside scope, the loop kills its
   own (strict) solver there instead, so one writer remains (at most one cube lost); 2+ outside-scope writers: ALERT.
   Any duplicate also writes `DUPLICATE_WRITERS` into that state folder, and the status carries an ALERT until a person
   has checked the state (two writers may have overwritten each other's segments) and deleted the file.
   A tag whose solver ends badly (`TAG ccc exit N` with N not 0/3, or no exit line) 3 times in a row is held for
   30 min; cake_lpr rejections in `failed_attempts.jsonl` raise an ALERT.
4. Stops (retarget, upgrade) are gentle: the solver is killed right after its `log.jsonl` gains an event (ccc90.py
   saves the tree before writing the event, so only seconds are lost), at the latest after 30 min. A solver whose tree
   has no open cube (stitching the final proof) is not interrupted for a retarget or upgrade.
5. Heartbeat: one-commit branch `lane-status-N`, `status.txt` = UTC time, `ALIVE=<ccc90.py processes>`, one line per
   tag (`TAG closed= open= recorded= pid= state= ...`), `SUPERVISOR lane= version= sv= head= assign= mode=
   sha256sums= pull=`, `NOTE ...` lines, and `ORIGINAL_MODEL_FOUND ...` last if any. Pushed every 5 min and at once on
   any change. The watcher's existing checks (`ALIVE=0`, `ORIGINAL_MODEL_FOUND`, age) work unchanged.
6. Publisher: a recorded proof goes to its line's branch as `codex/<branch without codex->/TAG.lrat.xz.partNNN`
   (90 MB), `TAG.sha256`, `TAG.result.json`, `TAG.log.jsonl` (the layout `ingest_branch.py` reads). It is appended on
   top of the branch from a blobless fetch (never a force push, so another publisher's files stay), 15 parts per push
   (below GitHub's 2 GB push limit), one part on disk at a time, only if free space at `/workspace/sv` exceeds the
   proof + 2 parts + 100 MB. The record line used is the one whose `proof_sha256` equals the proof file's.
   Skipped if the branch already holds `TAG.sha256`.

Push methods (`push=` in the SUPERVISOR line): `git` uses the lane clone's own remote and credentials (`git -C
/workspace/r push origin ...`; the heartbeat commit is built with plumbing, so the work tree is never touched). When a
git push fails with an authentication error (as on lane 11), the loop switches to `gh`, only if `gh auth status`
succeeds and `GET repos/<repo>` works, and shows `push=gh(git auth failed)`; after 3 gh failures in a row it goes back
to git. gh path: GitHub's git-data REST API through the `gh` CLI (blobs, trees, commits, refs), same layout, parts of
32 MiB (`SV_GH_PART`; about 43 MiB of base64 body each; the git path keeps 90 MB), codex-* refs updated with
`force: false` only (append-only; a moved branch is retried next tick), lane-status-N replaced as before. Part files
of the same tag left on the branch by an earlier, aborted upload are removed in the first commit. An aborted gh
publish leaves its uploaded blobs unreferenced until GitHub's gc (harmless; a NOTE says so). Before relying on gh on
a lane, run `bash gh_probe.sh` there once (in research/lanes/: one small and one 32 MiB blob, a tree, a commit, no ref). `SV_PUSH=git|gh|auto` forces a method;
`SV_GH_REPO=owner/repo` if it cannot be read from the clone's remote URL. `gh` must be logged in on the lane.

Each tag line starts `TAG run=STATE`: `running`, `stopping` (soft stop pending), `starting`, `running-outside-scope`
(a solver this loop may not touch), `stopped` (not running; the reason follows: waiting for a slot, HELD, halted,
ORIGINAL_MODEL_FOUND evidence), or `recorded`. `core.fileMode` is set to false in the
clone so `chmod +x` cannot block `git pull`.

Files of the loop: `/workspace/sv/` (`supervise.log`, `status.txt`, `run/` per-tag state, `pub/` publish marks,
`jobs/`). Logs of solvers it started: `<OUTDIR>.sv_TAG.nohup` and, as before, `OUTDIR/cube/TAG.log`.

Settings (environment, for tests): `SV_BASE` (/workspace), `SV_DIR`, `SV_TICK` 60, `SV_BEAT` 300, `SV_MAX` 3,
`SV_SOFT_MAX` 1800, `SV_SHA_GRACE` 120, `SV_WINDOW` 86400, `SV_PART` 90M, `SV_BATCH` 15, `SV_MAXFAIL` 3,
`SV_HOLD` 1800, `SV_PUSH_URL` (default: the clone's push URL), `SV_VENV` (/workspace/sat-venv), `SV_SCOPE`
(only touch solvers whose state path starts with this; default `$SV_BASE/`).

## Manager's routine

- Retarget lane N: edit `assign/N.txt`, commit, push. Confirm on `lane-status-N` within ~2 min (new tag `STARTED`,
  old one gone from the list after its next cube boundary).
- Upgrade code: commit the code and the new `SHA256SUMS` in ONE commit (a lone SHA256SUMS mismatch for more than
  2 min stops every lane), then bump `VERSION` (same or later commit).
- Lane heartbeat stale (container restarted): send the REPAIR line. Nothing else.
- ORIGINAL_MODEL_FOUND: the lane halts by itself; examine the evidence before anything else.
- Watch for `ALERT` lines in lane-status-N (SHA failure in fill mode, halts, cake_lpr rejections, a second writer).
