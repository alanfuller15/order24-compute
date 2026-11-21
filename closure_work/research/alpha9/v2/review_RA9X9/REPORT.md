# RA9X9 — review of ChatGPT round 9 part 1 (closure_drafts/reviews/gpt/round9_part1_condensed.md)
Written by the orchestrator from the reviewer's hand-back, 2026-11-19 ~04:25Z. Status [hand-proof reviewed]; finite steps exhaustively checked; not SAT certificates; no order-24 claim.

| Claim | Verdict |
|---|---|
| (1) F bipartite for all 15 pure 4/5/9 Case A profiles, t = 1, 2 | ACCEPT WITH REPAIR (citation: M1 extended to pure Case A) |
| (2) 6+7 classes, e(F) >= 24 for t = 2 | ACCEPT |
| (3) degree-five saturation lemma (4^13 9^2) | ACCEPT (same M1 note) |
| (4) exclusion of (4^13, 9^2), v1 86 | ACCEPT WITH REPAIR (multiplicity <= 2 proved here) |

Repair A — M1 for every pure Case A profile 4^s 5^m 9^t: five low masks containing {i,j} plus I\{i,j} = 12-set with 10 edges. Exactly four (Y): any fifth vertex x — low meeting {i,j}: (I\{i,j}) ∪ Y ∪ {x} has 8 + <=3 = 11; a=5 with mask ⊇ {i,j}: 8+3 = 11 (a=9 gives 15, not needed). So the other s−4 low masks lie in the 7-set I\{i,j} and meet pairwise; each a=5 mask has >= 4 elements in that 7-set and meets them all; a=5 pairwise non-adjacent (S1), a=9 isolated (P11): independent set (s−4)+m+t = 11 > 9.
Claim 1 details: 4f.1 (C9) parts (a)–(d) apply to any q4 <= 3 family; no high–high edges (F1); a=5 adjacent exactly to copies of I\C; shortest odd cycle all low, = C9, isolated by 4f.1(c),(d). Bound e(F) <= 9 + floor(r^2/4) + m·max(1,r) (complementary type on the cycle occurs once by 4f.1(d)). Recomputed: t=2 m=0..4 bounds 13,14,14,12,13 < 21; t=1 m=0..5 bounds 15,17,17,16,13,14 < 20; larger m: s <= 8, bipartite by odd girth. Profiles: t=1 v1 84,85,87,90,94,98,101,104; t=2 86,88,91,95,99,102,105. Deps: 4f.1, 4b.11, Theorem 1, P11, S1, M1 (extended).
Claim 3: simpler proof via n_e = #masks missing e (Σ n_e = 5, pair count 5 − n_i − n_j <= 3 forces all n_e = 1); exhaustive: of 126 multisets of five 4-subsets of a 5-set only the five distinct satisfy q4 <= 3; 21 masks can be added, each meets C in <= 1, has >= 3 in A, all pairwise meeting; 8 independent low + 2 a=9 = 10.
Repair B — multiplicity <= 2 for t = 2 (M2-style): a mask A' three times => every pair in A' at q4 = 3 => every other low mask meets A' in <= 1 => >= 3 elements in the 5-set I\A' => pairwise meeting => the other 10 low vertices + 2 a=9 form an independent 12-set. (Checked: 45 addable masks, all pairwise meeting.)
Claim 4 chain: Σ_X d >= 24 with degrees <= 4 => all degree 4; neighbour masks distinct 4-subsets of I\A; a mask != A is disjoint from <= 1 of them; so x' (mask != A) adjacent to all three of Y\{y1..y4}; two distinct masks have <= 1 common disjoint 4-mask => a tripled mask, contradiction (Repair B); so X has types A and one other, each <= 2: |X| <= 4 < 6.
End-to-end model check of 4^13 9^2 (assuming only Theorem 1, isolated a=9, bipartite 6+7, degree <= 5, q4 <= 3, multiplicity <= 3; NOT claim 3 or multiplicity <= 2): 0 survivors (9,044 Y-sets, 69,412 X-sets, 7.9 s). Negative control without q4/multiplicity filters: 1,212 configurations pass all F-level checks — search is not vacuous; M1 is essential.
Ledger after write-up: Case A open = 14 (v1 84,85,87,88,90,91,94,95,98,99,101,102,104,105); F bipartite [hand-proof reviewed] for all 15 (conditional on 4f.1); 86 excluded [hand-proof reviewed].
Files: small_checks.py/_out.txt (ALL OK), model_4_13_9_2.py/_out.txt, diag.py/_out.txt.
