# Closure tasks for ChatGPT / Codex (issues #3-#7)

Everything needed is in this branch (`closure-work`) under `closure_work/`, mirroring the producer's scratchpad paths.
Rules (non-negotiable):
- Never claim the order-24 theorem. Keep the six status labels separate: [hand-proof reviewed], "finite check reviewed
  (independent re-implementation)", SAT/LRAT certificate, reproduced, producer's summary, conditional.
- A reviewer must not be the agent/chat that produced the thing it reviews. Say which chat produced and which reviewed.
- No sorry/admit/unsupported axioms; hashes and logs are not proofs; preserve UNKNOWN results.
- Git: never a plain `git pull`; use `git fetch --no-tags origin main && git merge --ff-only FETCH_HEAD`. Work on branch
  `closure-work` (rebase onto it the same way); never force-push main.
- Write each deliverable as a file in `closure_work/out/` and comment its path on the issue.

## T2a (issue #4) - write the alpha = 9 closure document  -> closure_work/out/ALPHA9_CLOSURE.DRAFT.md
Inputs: research/alpha9/v2/MATH.md (sections 4b-4l; ledgers after 4j, 4k, 4l: Case A 0 open, Case B 0 open),
review_RA9X*/REPORT.md, exp_A9_A_1nines/, and the certified A9 production run (430 profiles, 3,636 units; final claim
on branch a9-final-status, A9_FINAL.md). State precisely: (1) alpha >= 10 excluded (chain status draft, section
"The class..."); (2) for alpha = 9 the two independent lines of evidence - the certified run (label: SAT/LRAT certificate,
only once A9_FINAL.md says ALL 32 PARTS AGREE and issue #3's review passes) and the MATH.md section 4 write-up (labels
per section); (3) every dependency (4f.1, 4g.2, M1, N3, (MAX), Theorem 1 ...) and which result uses which; (4) what is
NOT claimed. Do not upgrade any label.

## T2b (issue #4) - Case B exact-model certification avoiding 4f.1  -> closure_work/out/RA9X20/
Inputs: research/alpha9/v2/exp_B4/ (model_B4.py v3.1, README, outputs). Review the UNCONDITIONAL encoding against MATH.md
(must not use 4f.1/4g.2); dump the static CNF per profile B16-B19; write an independent re-encoding from MATH.md; run
CaDiCaL with binary LRAT and the pinned cake_lpr (repo bin/cake_lpr; or run on GitHub via .github/workflows/exp.yml);
controls (lowered thresholds SAT, models re-checked). Report per profile ACCEPT/REJECT with hashes.

## T4b (issue #6) - closing review of l88/L88_CLOSURE.md, l89/L89_CLOSURE.md, l90/L90_CLOSURE.md
Check each against its stated audit results and the route; list must-fix / should-fix with exact wording.
-> closure_work/out/R88_90_REVIEW.md

## T4c (issue #6) - route must-fix
research/a22_review2/FIX_CHECK.md left 1 must-fix on the route text; check whether layers/LOW_LAYERS_ROUTE.md (v7) fixes
it; if not, propose exact wording. -> closure_work/out/ROUTE_FIXCHECK.md

## Later: T1 review of the A9 final claim (#3, when A9_FINAL.md says ALL 32 PARTS AGREE); T4a outside packages (#6,
materials not in this branch); T5 final statement (#7, after #3-#6).

## T6 (new issue) - A22 re-check feasibility  -> closure_work/out/A22_FEASIBILITY.md
A22: a(22) = 17, i.e. every triangle-free graph on 22 vertices has beta <= 17 (OEIS A389646, McKay; uncertified).
Read closure_work/research/review_a22/ (REVIEW_A22.md says exactly what is used, including the stronger 'McKay-max'
extremal-list assumption). Deliver: (1) the precise statement(s) the route uses; (2) known methods (McKay's, if
documented; nauty/geng triangle-free generation, maximal triangle-free graphs, SAT/ILP formulations) and an estimate of
the size of a full independent re-computation for n = 22, with a small-n pilot (n <= 16 or 18) timed on your machine,
extrapolated; (3) a plan that splits it into independent jobs of < 5 h each on GitHub's free 4-core runners, with a
certificate story (how a checker other than the producer would trust each piece); (4) a go/no-go recommendation.
Do not start a big computation; pilots only.
