# Layer 89 closure (Erdős #128, order 24): producer's summary

Sun 2026-11-15, 18:20 AKST. Route: `L89_ROUTE.md` (version 3). Model: layer 90 (`l90/L90_CLOSURE.md`).

## What is claimed

**Theorem L89 (conditional).** Assume A22 (a(22) = 17, McKay); the closure of layer 90 (with everything it assumes: the
closures of layers 91–96, BCL Theorem 2(b), A22); Theorem A (saturation, which at m = 89 uses layer 90) and Theorem B
(δ ≥ 4); and the completeness of the H catalogue (uenum.py). Then no graph on 24 vertices is triangle-free, has α ≤ 8, has
at least 12 edges in every 12-vertex set, and has exactly 89 edges.

This is one edge layer. It is **not** the order-24 Erdős statement, which needs every other edge layer / degree family
excluded as well.

## Status, by the six labels

| Label | Layer 89 |
|---|---|
| [1] inherited | A22; BCL 2(b); closures of layers 90–96. Not re-proved here. |
| [2] reproduced | NOT RUN (no second independent production of the 432 certificates; proofs deleted after audit). |
| [3] structural | Reduction to 432 formulas (L89_ROUTE.md v3). Reviewed by R89A (0 must-fix, 4 should-fix, all made) and by an independent cross-vendor review (ChatGPT, reviews/XGPT_REVIEW_L89.md: its one must-fix was "certificates not yet complete", now addressed below; its should-fix 1–2 made, 3 recorded as an explicit dependency). Both re-derived the 19 profiles and 432 formulas independently with zero discrepancies. Catalogue completeness stays a trusted computation. |
| [4] checked certificate | **PASS: all 432 formulas.** Each has an LRAT proof that the pinned CakeML-verified checker cake_lpr (29e02af7…) accepted against the CNF rebuilt by the pinned encoder v7 (cegar90c.py 7699f39b…) from the record's lazy list, in four independent audits G1–G4 (checker gcert89.py d1b89923…, generated from gcert90d.py with only the formulas pin, run label, v7-only and resume-rule changes, confirmed by each auditor's diff). The four groups are disjoint and cover the 432 formulas exactly once (audit/UNION_CHECK.txt; also checked by auditor G4). A cross-vendor spot-check re-verified 6 certificates in a separate sandbox (reviews/XGPT_CERT6.md). |
| [5] Lean | NOT RUN for layer 89. |
| [6] family | Not applicable. |

## The four audits (formulas89_c66.json 792aef89…3031; gcert89.py d1b89923…)

| Group | Formulas | Checker exit | CHECK_RESULTS SHA-256 | Report |
|---|---|---|---|---|
| G1 | 163 | 3 (partial, all pass) | b893e6a33e55ddcfefa3f43e29beccdc8c372a1f423da9aea21cf0e94a69ed33 | reviews/A89_G1_AUDIT.md |
| G2 | 130 (4 cube-and-conquer) | 3 (partial, all pass) | 6fa249c251aec85e73d9afa316d370416ab9cb68f58f04b061652bcdcb0923f9 | reviews/A89_G2_AUDIT.md |
| G3 | 104 | 3 (partial, all pass) | c659a21aab7a5c481230c2e1708fcead4cb545d5392f36993363021f66ad362f | reviews/A89_G3_AUDIT.md |
| G4 | 35 | 3 (partial, all pass) | 4b7c6883fe8b7131653a3e60eba01515c27bf4b21d63df62766dab987ea83148 | reviews/A89_G4_AUDIT.md |

Each audit is a partial run (tag filter), exit 3 at best; there is no single exit-0 run over all 432. Each auditor ran
two negative controls (tampered lazy list; tampered proof), both rejected (exit 1). The producer re-read every
CHECK_RESULTS line and checked disjointness and exact coverage.

## Production (untrusted; plays no part in correctness)

Proofs were produced on GitHub Actions (public repo alanfuller15/order24-compute; up to 40 concurrent 4-core jobs; producer
grun90.py and ccc90.py with encoder v7) and by a local cube-and-conquer run, between 16:53 and 18:05 AKST. Every record was
rebuilt and its proof checked by the audits above; where a record came from does not matter.

## Proof bytes

Audited proofs were deleted after each group's audit (index files audit/G*/proofs_index.txt). [4] therefore rests on the
four audit reports and their CHECK_RESULTS. Duplicate, unrecorded proof copies were deleted too (dup_proofs_deleted_index.txt).

## Not claimed

- The full order-24 theorem. Layers below 89 are not addressed.
- Nothing UNKNOWN was upgraded: every one of the 432 formulas has a passing certificate; no satisfiable result occurred.
