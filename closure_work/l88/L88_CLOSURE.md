# Layer 88 closure (Erdős #128, order 24): producer's summary

Mon 2026-11-16, 07:25 UTC (Sun 22:25 AKST). Route: `L88_ROUTE.md` (version 2). Model: layer 89 (`l89/L89_CLOSURE.md`).

## What is claimed

**Theorem L88 (conditional).** Assume A22 (a(22) = 17, McKay); the closure of layer 89 (`l89/L89_CLOSURE.md`, with
everything it assumes: layer 90, the closures of layers 91–96, BCL Theorem 2(b), A22); Theorem A (saturation, which at
m = 88 uses layer 89) and Theorem B (δ ≥ 4); and the completeness of the H catalogue (uenum.py). Then no graph on 24
vertices is triangle-free, has α ≤ 8, has at least 12 edges in every 12-vertex set, and has exactly 88 edges.

This is one edge layer. It is **not** the order-24 Erdős statement, which needs every other edge layer / degree family
excluded as well.

## Status, by the six labels

| Label | Layer 88 |
|---|---|
| [1] inherited | A22; BCL 2(b); closures of layers 89–96. Not re-proved here. |
| [2] reproduced | NOT RUN (no second independent production of the 432 certificates; proofs deleted after audit). |
| [3] structural | Reduction to 432 formulas (L88_ROUTE.md v2). Reviewed by R88A (0 must-fix, 2 should-fix: 1 made in route v2; 2 was a mislabelled header in close_group.py, fixed) and by an independent cross-vendor review (ChatGPT, reviews/XGPT_REVIEW_L88.md: 0 must-fix; should-fix 1 = the 14-F dependency, made in route v2; should-fix 2 = subset provenance not replayable from its attachments, answered by R88A's byte-for-byte regeneration of formulas88.json and the subset). Catalogue completeness stays a trusted computation. |
| [4] checked certificate | **PASS: all 432 formulas.** Each has an LRAT proof that the pinned CakeML-verified checker cake_lpr (29e02af7…) accepted against the CNF rebuilt by the pinned encoder v7 (cegar90c.py 7699f39b…) from the record's lazy list, in independent audits with checker gcert88.py (23efd4b7…; gcert89.py with the formulas pin, own name, run label and two messages changed). Groups G1–G4 partition the 432 formulas; one formula of G4 got no verdict (see below) and passed in a one-formula formal re-check G5. Every formula has exactly one passing group main-run line (audit/UNION_CHECK.txt). |
| [5] Lean | NOT RUN for layer 88. |
| [6] family | Not applicable. |

## The audits (formulas88_c65.json 9835d162…3538; gcert88.py 23efd4b7…)

| Group | Formulas | Checker exit | Passing lines | CHECK_RESULTS SHA-256 | Report |
|---|---|---|---|---|---|
| G1 | 112 | 3 (partial, all pass) | 112 | 7efc50eddf41b8ef3dab502cb8d310e8a0be85ab9eb7be5f37ba8469efdb0b3e | reviews/A88_G1_AUDIT.md |
| G2 | 124 | 3 (partial, all pass) | 124 | 76086ce92f7b055af241d5f9b73b0ad00f090de249697be0e5081aaae6103468 | reviews/A88_G2_AUDIT.md |
| G3 | 114 (2 built on a macOS runner) | 3 (partial, all pass) | 114 | 55d4bad5fc936b7b29b1c273085b4b882ccdb7b5406cf5ba86f6030bb7b732a0 | reviews/A88_G3_AUDIT.md |
| G4 | 82 | **1** | 81 | 0c7c45de80c0757fc5bf57abe711421cbb0819b248a17d4a575d8d83b23e81e8 | reviews/A88_G4_AUDIT.md |
| G5 | 1 (re-check of G4's L88_s10a4b18c66_0001) | 3 (partial, all pass) | 1 | a207fed4293ecca2c080df8a074bd34a8cef72674f47c4953eb8365e8a0d1947 | reviews/A88_G5_AUDIT.md |

Each audit is a partial run (tag filter), exit 3 at best; there is no single exit-0 run over all 432. Each auditor ran
negative controls (tampered lazy list; tampered proof copy, except G5 whose only proof was too large to copy), all
rejected (exit 1). The producer re-read every CHECK_RESULTS line (close_group.py) and checked the union.

**The G4 failure.** For L88_s10a4b18c66_0001 (862 MB trimmed proof) the CNF and proof hashes matched, but cake_lpr was
killed twice by the memory-cgroup OOM killer (cgroup limit about 5.8 GiB) and printed no verdict: cake_exit -9, "NOT
VERIFIED", empty tail. The pressure came from a producer download process holding a 2.5 GB artifact in memory. This is a
no-verdict line, not a rejected proof, and it stays in G4's results as it is. The download scripts were changed to stream
to disk (measured: 42 MB instead of 2.5 GB), downloads were stopped, and G5, a separate independent auditor, re-checked
that one formula alone (no other checker or download running; oom_kill counter unchanged; no new kernel OOM lines): pass,
"s VERIFIED UNSAT", heap 2000. The G4 auditor's own diagnostic re-run also passed but is not counted as a group result.

## Production (untrusted; plays no part in correctness)

Proofs were produced on GitHub Actions (public repo alanfuller15/order24-compute; producer grun90.py with encoder v7, waves
m88a/m88b of 4 formulas per job; 2 formulas on a macOS runner built from source as a lane test) between 03:45 and 06:33
UTC. Every record was rebuilt and its proof checked by the audits above; where a record came from does not matter.

## Proof bytes

Audited proofs were deleted after each group's audit (index files audit/G*/proofs_index.txt). [4] therefore rests on the
audit reports and their CHECK_RESULTS.

## Not claimed

- The full order-24 theorem. Layers below 88 are not addressed here.
- Nothing UNKNOWN was upgraded: every one of the 432 formulas has a passing certificate line; no satisfiable result occurred.
