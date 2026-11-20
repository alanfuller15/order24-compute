# What runs on its own (no Claude session needed)

- **refill** (`.github/workflows/refill.yml`, `ops/refill.py`): every live pass scans finished produce runs, folds prediction
  votes, dispatches the next waves (up to 40 jobs) and starts the next pass itself about 8 min later (the cron is a backup;
  GitHub throttles it). A run that takes over `per_run_minutes` (8) to plan is skipped and logged. Status page: branch `status`.
  Pause everything: commit a file `control/HOLD`. A manual start must pass `dry_run=false` (default is a dry run).
- **Codex lanes** (`lanes/supervise.sh`, `lanes/assign/N.txt`, `lanes/VERSION`): self-healing supervisors; bump `lanes/VERSION`
  to restart lane solvers on new code. Heartbeats: branches `lane-status-N`.
- **A9 final collection** (`.github/workflows/a9final_check.yml`, hourly): gathers the 8 parts `a9v3_final_p0..7` and writes
  `A9_FINAL.md` to branch `a9-final-status`.

# What still needs a person or a review agent (truth-bearing, by design)

- Stating the A9 final claim: only after ALL 8 PARTS AGREE on `a9-final-status` AND an independent reviewer checks it.
- Recording or auditing layer formulas (audit groups, `ops/recorded.txt`): independent audit per group.
- Any new mathematical claim (MATH.md sections): separate reviewer; no agent approves its own result.
- If `status` shows ATTENTION lines that persist for hours, a session should look.

Never run a plain `git pull`/`git fetch`; use `git fetch --no-tags origin main && git merge --ff-only FETCH_HEAD`.
