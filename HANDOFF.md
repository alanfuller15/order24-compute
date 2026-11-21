# Handoff (read this first in a new session; keep it short)

Updated 2026-11-21 06:35Z. Owner: Alan. Goal: Erdős #128 order 24 (no triangle-free 24-vertex graph with >= 12 edges in
every 12-set). Status doc (Claude Docs): "Order 24 Closure Status". Live dashboard: branch `status`, STATUS.md.

## Runs by itself (no Claude needed)
- GitHub refill loop (self-chaining every ~8 min): continues the last layer formulas L82_0000, L81_0000, L80_0000/0001.
- A9 final claim: exp jobs a9v5_final_p0..31; collector -> branch a9-final-status (A9_FINAL.md); issues open on result.
- AUTOMATION.md lists everything; `control/HOLD` pauses it.

## Work is outsourced to ChatGPT/Codex (user's ChatGPT plan), tracked in issues #3-#9, branch closure-work
- Rules for them: closure_work/TASKS.md. Lanes: 7 writer, 3 Case B cert (done, ACCEPTED by lane 4), 4 reviewer,
  5 auditor + A9 final review, 6 A22 feasibility (NO-GO for full run), 8 A9 timeout fix (branch a9-final-fix).
- ChatGPT chat "Review mathematical note": max-cut >= m-21 for m=80..82 without A22/McKay-max; reduced to its Eq.(13),
  asked for a finite machine-checkable version.

## Open, in order
1. A9 final: parts 11-14 time out at any N (#9) -> lane 8 fix, re-dispatch, then lane 5 review (#3).
2. Apply REVIEW_T2 repairs to closure_work/out/ALPHA9_CLOSURE.DRAFT.md (#4).
3. L82_0001 audit re-dispatched 06:30Z (cake_heaps 8000,12000, swap 24); needs independent verification (#5).
4. #6 outside packages (T95, G11, seven-four) acceptance: materials not in repo.
5. #7 final statement + trust list (BCL 2(b), A22, McKay-max).

## How to work cheaply
- One-call status: skill order24-status-check. Audit: order24-audit-record (auditor on Sonnet). A9: order24-a9-final.
- Never claim the order-24 theorem; no agent approves its own work; git only `git fetch --no-tags origin main && git merge --ff-only FETCH_HEAD`.
- Long history lives in the old session's scratchpad STATE.md (not needed for routine checks).
