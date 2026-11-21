# T4c — fix-check of the remaining RC22c route must-fix

## Scope, provenance, verdict

**Verdict: PASS / FIXED for F1 in LOW_LAYERS_ROUTE.md version 7. No replacement of its McKay-max scope wording is
required to discharge this particular must-fix.** This is a text/dependency fix-check, not acceptance of the
whole route, the external McKay computation, a certificate replay, or the order-24 theorem.

Reviewer: **Codex lane-7 chat** (prior compute experiments, then T2a writer and T4b reviewer). This chat did not
produce the reviewed route or RC22c/FIX_CHECK. The route is the project's producer/orchestrator's note; the older
review identifies its author as the independent reviewer RC22c, without a unique chat identifier. Those original
chat identifiers are not supplied; no stronger identity verification is asserted. This reviewer is distinct
from both of those source producers. T2a, written by this chat, is not an object accepted by this fix-check.

Read in full:

* [research/a22_review2/FIX_CHECK.md](../research/a22_review2/FIX_CHECK.md), especially Remaining fixes item 1;
* [research/a22_review2/REVIEW.md](../research/a22_review2/REVIEW.md), F1 and sections 3–5;
* [layers/LOW_LAYERS_ROUTE.md](../layers/LOW_LAYERS_ROUTE.md), **version 7**;
* [ORDER24_CHAIN_STATUS.DRAFT.md](../closure_drafts/ORDER24_CHAIN_STATUS.DRAFT.md), v4, the recorded review gap.

Source tree: `f3f7643b767af0b992adabf5b9375782ddf22fb1` on closure-work. The source files below are unchanged
from materials commit `b15336cf1907d32d6c7ea3afed9404d98da9bb66`. Hashes identify the exact text checked;
they are not mathematical proofs:

| Source | SHA-256 |
|---|---|
| LOW_LAYERS_ROUTE.md | 0accac93f7850648ba8a05284fc1d4519cb0b36672916ac4034e5a4d8b6f9347 |
| FIX_CHECK.md | 911a172a2665abb5101b492d16af07afc9052136ac81f378bb89a96fb28462ae |
| REVIEW.md | 58569a6b78bb2fba277d63b695ce999f958b65d3f29cbbda94443a1b8293bb4c |

Line references below are to these exact source copies.

## What the old must-fix required

FIX_CHECK's Remaining fixes item 1 (lines 48–59) found that COVERAGE_PLAN.md's proposed route diff still said:

1. `it is used only for the formulas listed in a22c/LEMMA_C22c_EXEMPT.json`;
2. `McKay-max (layers 80–82 only)`;
3. `Used only by Lemma E, so only by the exempt tags.`

The required repair was to distinguish **direct** use from **inherited** use: the exempt tags use McKay-max
directly, but Theorem L_m for every m<=79 and any final order-24 result using that chain inherit it through L80.
A note outside the actual route text was insufficient. The earlier REVIEW's F1 explains the top-down induction.

The old package had seven exemptions in layers 80–82. Version 7 additionally includes the layer-83 corollary
and two tags at that layer. A correct fix-check must accommodate that extension, not paste the old "seven tags"
scope unchanged.

## The three locations in the actual version-7 route

| Old defect | Actual replacement in the installed route | Result |
|---|---|---|
| Unqualified "used only" by listed formulas | Theorem L_m, lines 14–16: `For m ∈ {80, 81, 82, 83} also assume McKay-max ... it is used directly only for the formulas listed in a22c/LEMMA_C22c_EXEMPT.json ... Theorem L_m for every m ≤ 79, and any final order-24 result, inherit McKay-max through L80 and L83 while the exemption is in use.` | PASS: directly-only restriction plus explicit lower-layer/final-result inheritance appears in the theorem's own text. |
| "layers 80–82 only" | Dependencies kept explicit, lines 89–90: `McKay-max (used directly in layers 80–83; layers 80–82 also inherit it through layer 83; inherited by L_m for every m ≤ 79 and any final order-24 result)` | PASS: all direct layers and transitive paths are named; it does not confine trust to 80–82. |
| "Used only by Lemma E ..." | Same dependency item, lines 91–92: `Used directly only by Lemma E, so directly only by the exempt tags; inherited through L80 and L83 by every lower layer and the final result.` | PASS: both uses of "only" are qualified and followed by the inheritance clause. |

The ellipses in the table elide identifiers/parentheses, not hypotheses; the cited line spans supply the full
sentences. These are the route's operative theorem and dependency list, not merely a historical COVERAGE_PLAN
note or a closure-template footer. F1 is therefore repaired at the point where FIX_CHECK required it.

## Why the repair matches the dependency graph

The route's theorem (lines 10–13) assumes closure of layer m+1, and step 1 uses that for saturation. Thus:

* A use of McKay-max to close an exempt formula at L83 is inherited by L82, L81, L80 and every lower layer.
* Direct uses in L82/L81/L80 add their own dependencies; L79 inherits L80, hence L78 and so on inherit it too.
* Layers L84–L87 do not acquire this hypothesis backwards from lower layers. Nor does this repair add it to
  L88–L90 or other upstream layers.
* Any final result relying on these conditional closures must retain McKay-max while that route is used.

The dependency list explicitly covers 80–82's inheritance through L83 as well as <=79 through L80/L83. No layer
in the relevant downward chain is omitted. This does **not** claim that such a final result is otherwise ready.
The class remains triangle-free order 24, alpha<=8, every 12-set spanning at least 12 edges; its identification
with the original problem is a separate matter.

The route defines McKay-max precisely as completeness up to isomorphism of the maximal triangle-free graphs on
22 vertices with beta=17 in the named list; it is stronger than the A22 upper bound beta<=17. Lemma E uses this
completeness to move from a maximal extension to a listed graph. Neither it nor its completeness is newly
proved by this wording check. The route retains Check W and Check B as recorded checks with distinct roles.

## Current exemptions do not erase inherited trust

Version 7 keeps the nine-tag exemption file unchanged: 2+2+3 tags at layers 80/81/82 and two at layer 83.
Its step 7 records that L83_s10a4b18c61_0000 is now **exempt and also certified**, while _0001 is still closed by
the corollary alone (433+1 certified, one corollary-only at that layer). A redundant certificate does not justify
removing McKay-max from the chain while another formula still needs it. Likewise, certifying a lower-layer
exemption would not automatically remove that layer's inherited L83 dependency. These are stated record counts,
not a fresh coverage/certificate audit by this reviewer.

The distinction is exactly why the current "directly only" plus "also inherit" language matters. F1's fix
survives the extension from the older seven-tag plan to the version-7 nine-tag list.

## What this verdict does not discharge

1. FIX_CHECK's **item 2 (install-instruction should-fix)** concerns old script/EXEMPT hashes, the fourth `a22c`
   argument, and dry-run files in COVERAGE_PLAN.md/REVIEW_BRIEF.md. Those files and the installed union script/
   EXEMPT data are not supplied in closure_work. Their current state is **not checked** here. The old report's
   "accept without further re-runs" also required specified code/data hashes to remain unchanged; version 7
   quotes a later union_lemma pin. This fix-check cannot infer that entire conditional acceptance from F1 alone.
2. The optional passing-duplicate-line improvement is not F1 and is not re-checked. The older review's code
   controls are reported evidence; this task did not rerun them or upgrade their labels.
3. The chain map also mentions **two cross-vendor should-fixes** and R-LOW's lack of a second route review. Their
   original cross-vendor report is not in this bundle and the two items cannot be identified/verified from that
   sentence alone. This report neither implements them nor marks them complete. The RC22c install-instruction
   item must not silently be equated with those two independent items.
4. No broad gate review of route v7, review of outside packages, or new verification of encoder v9/symmetry,
   raw proofs, LRAT acceptance, union logic, or catalogue completeness is supplied by T4c. T4b separately records
   the evidence limits for the layer-88–90 summaries. It is not an acceptance of this route's entire chain.
5. Existing [hand-proof reviewed], finite check reviewed (independent re-implementation), SAT/LRAT certificate,
   reproduced, producer's summary, and conditional labels keep their original scopes. A text repair is not a
   certificate, no new computation is called reproduced, and missing/UNKNOWN results remain unresolved.

## Exact hand-back

No McKay-max replacement text is needed for the specific route must-fix. For a status register, the following
wording accurately records this narrow result (it is a proposal; no status-map source was edited):

> RC22c F1 route wording: FIXED in LOW_LAYERS_ROUTE.md v7, independently checked by the Codex lane-7 chat in
> closure_work/out/ROUTE_FIXCHECK.md. The theorem and dependency list distinguish direct use for the exempt tags
> in layers 80–83 from inheritance by layers 80–82 through L83, all layers <=79 through L80/L83, and any final
> result using the chain. This closes only F1; install instructions, the separate cross-vendor should-fixes,
> broader route acceptance, and all mathematical/computational trust assumptions retain their prior status.

No order-24 theorem is claimed.
