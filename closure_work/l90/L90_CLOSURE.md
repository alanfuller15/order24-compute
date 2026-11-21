# Layer 90 closure (Erdős #128, order 24): producer's summary

Sun 2026-11-15, 16:35 AKST. Route: `L90_ROUTE.md` (version 3). Encoder notes: `BOUNDS90.md`. Cube-and-conquer: `CUBE90.md`.

## What is claimed

**Theorem L90 (conditional).** Assume A22 (a(22) = 17, McKay), the closure of layer 91 (with everything it assumes: layer 92,
BCL Theorem 2(b), layers 93–96), Theorems A and B, and the completeness of the catalogue of graphs H (uenum.py).
Then no graph on 24 vertices is triangle-free, has α ≤ 8, has at least 12 edges in every 12-vertex set, and has exactly
90 edges.

This is one edge layer. It is **not** the order-24 Erdős statement: that needs every other edge layer / degree family
excluded as well.

## Status, by the six labels

| Label | Layer 90 |
|---|---|
| [1] inherited | A22 (McKay's exact search); BCL Theorem 2(b); the closures of layers 91–96 as packaged before. Not re-proved here. |
| [2] reproduced | Not yet. A replica run that re-proves all 428 formulas from their records and keeps the proofs is running on 10 rented machines (`replica90.py`); its results are not in this package. |
| [3] structural | The reduction to 428 formulas (L90_ROUTE.md: cut argument by Corollary C22, profiles, the a22/b22 families, swap, iso8, tbip, twins). Reviewed by R90A, R90B, R90C, R90D (no must-fix open). The catalogue completeness (uenum.py) is a trusted computation, cross-checked by R90A with networkx, not a certificate. |
| [4] checked certificate | **PASS: all 428 formulas.** Each has an LRAT proof that the pinned CakeML-verified checker cake_lpr (29e02af7…) accepted against the CNF rebuilt by the pinned encoder from the record's lazy list, in five independent audits G1–G5 by auditor agents that did not produce the proofs. The five audits together cover the 428 formulas exactly once (audit/UNION_CHECK.txt). |
| [5] Lean | NOT RUN for layer 90 itself. (FloorLadderFixed.lean compiles with propext and Quot.sound only; it concerns the floor ladder lemma, not this layer.) |
| [6] family | Not applicable: no family statement is made here. |

## The five audits (formulas90_c67.json 6945c129…a643; G1 with gcert90.py 2cc11dea… (v4 records), G2–G5 with gcert90d.py 0435cbd0…)

| Group | Formulas | Encoders | Checker exit | CHECK_RESULTS SHA-256 | Report |
|---|---|---|---|---|---|
| G1 | 48 | v4 48 | 3 (partial, all pass; gcert90.py) | 3234fcd180a359f59b059276edeaebc6adfd0c7c9d16252a4d51013ee69d7c55 | reviews/A90_G1_AUDIT.md |
| G2 | 194 | v7 130, v6 52, v5 12 | 3 (partial, all pass) | 9a293c51e1ec5413700550942983d1f84f02403deadbedeab5301528b2b61a5c | reviews/A90_G2_AUDIT.md |
| G3 | 86 | v7 86 | 3 (partial, all pass) | 5fc9ff60a84b37958bb0943716feea11a9923fc953679af173c7d235c4fe13e9 | reviews/A90_G3_AUDIT.md |
| G4 | 54 | v7 54 (15 cube-and-conquer) | 3 (partial, all pass) | e211a1c33c940f51c672c9de2ed0c596bd758aefdc5570aed7c6d0a489d1e942 | reviews/A90_G4_AUDIT.md |
| G5 | 46 | v7 46 (21 cube-and-conquer) | 3 (partial, all pass) | 1aa6db62631626649d746ad86c97d6e93042e32047c5a56cbadc066dd5294d35 | reviews/A90_G5_AUDIT.md |

Each audit is a partial check (a tag filter selecting its group), so each exits 3 at best; there is no single exit-0 run
over all 428. The producer re-read every CHECK_RESULTS line (pass, cnf_match, proof_match, "s VERIFIED UNSAT", cake exit 0,
no override, pinned cake_lpr and formulas, hashes equal to the records) and checked that the groups' tag sets are disjoint
and their union is exactly the 428 formulas: `audit/UNION_CHECK.txt`.

## What the proof bytes are, and where

The audited proofs were deleted after each group's audit (disk limits); `audit/G*/proofs_index.txt` lists their SHA-256.
So the statement in [4] rests on the five audit reports and their CHECK_RESULTS, not on proof files that can be re-checked
today. The replica run is intended to restore a complete, re-checkable proof set; until it finishes and is itself audited,
no claim is made from it.

## Not claimed

- Route L90⁺ (A23 instead of A22): not done (L90_ROUTE.md).
- The full order-24 theorem: not claimed.
- Nothing UNKNOWN was upgraded: there were no UNKNOWN or satisfiable results; every formula has a passing certificate.
