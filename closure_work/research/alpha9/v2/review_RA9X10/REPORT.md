# RA9X10 — review of ChatGPT round 9 part 2 (closure_drafts/reviews/gpt/round9_part2_condensed.md)
Written by the orchestrator from the reviewer's hand-back, 2026-11-19 ~06:30Z. Status [hand-proof reviewed]; exhaustive model checks are supporting evidence, not SAT certificates; no order-24 claim.

| Profile | v1 | Verdict | Multiplicity bound used |
|---|---|---|---|
| 4^12 5 9^2 | 88 | ACCEPT WITH REPAIR (wording) | <= 2 (proved, s+t >= 13) |
| 4^11 5^2 9^2 | 91 | ACCEPT | <= 2 (proved) |
| 4^10 5^3 9^2 | 95 | ACCEPT WITH REPAIR (two steps rewritten) | <= 3 only (M1) |
| 4^9 5^4 9^2 | 99 | ACCEPT | <= 3 only |
| 4^8 5^5 9^2 | 102 | ACCEPT | <= 3 only |
| 4^7 5^6 9^2 | 105 | ACCEPT (shorter proof exists) | <= 3 only |

Multiplicity: a tripled mask A gives the other 10−m low vertices + 2 a=9 an independent set of 12−m > 9 iff m <= 2; for m >= 3 only M1 (<= 3) is available; the m >= 3 arguments use only <= 3 and treat tripled types explicitly. a=5 degree = multiplicity of its complementary mask (<= 3).
Twins: every capacity count holds with twins (copies have identical neighbourhoods; a=5 adjacent exactly to the copies of its complement). Re-derived: s7 r=3 <= 23, r=4 <= 24 with forced structure; s8 low–low <= 6+3a <= 15 (+ <= 9), two tripled <= 12; s9 <= 23, c_A+c_B >= 5 > 4; s10 <= 25 forcing >= 4 a=5 of degree 3, two tripled <= 21; s11 <= 23.
Section 5 lemmas correct (degree concentration 3+3+5 = 11; distinct dense stars when neighbourhoods share >= 2; "related": two distinct types with >= 4 occurrences meet in exactly 1, no 4-mask disjoint from both — all checked).
Repairs:
- s6 (m=1), a=5 in X: the opposite class has 7 low vertices (not <= 6); still works: five degree-5 X lows with 5 low neighbours each share >= 5+5−7 = 3 => same type, multiplicity 5, contradiction.
- s8 (m=3) (a) "exactly one high neighbour" unjustified; replacement: each degree-5 X low has <= 1 a=5 neighbour, hence >= 4 low neighbours among the 5 Y lows; by dense stars all share one type => multiplicity >= 4, against M1 (free a=5 vertices included). (b) if no degree-5 copy of A exists, the >= 4 degree-5 lows are all non-A with 5 low neighbours => same type, multiplicity >= 4; else ChatGPT's geometry applies. (c) choose A, B among types whose copies have degree >= 4 (>= 2 and <= 3 such types; the two largest sum >= 4); then c_A + c_B >= 4 > 3.
- s10: read "complementary types" as "two types, each matched by two a=5 vertices"; all three Y masks disjoint from A and B => |A∩B| >= 3, with combined multiplicity >= 4 violating q4 <= 3.
- s11 shorter: one a=5 in X: X degree sum >= 2 + 25 = 27 > Y capacity 2·5 + 5·3 = 25.
Independent model check (assumes only Theorem 1, P11, F bipartite 6+7, degree caps, r_i <= 7, every 10-subset of F >= 12 edges, M1; NOT Repair B, NOT ChatGPT's lemmas; symmetry: x = max-degree X vertex is a=4 with mask {0,1,2,3}, neighbourhoods reduced under S5 on {4..8}): 0 survivors for m = 0..6 (C, <= 0.5 s CPU each; Python reference gives identical counters for m = 0, 1, 2, 6).
Controls: without M1, survivors 109,792 / 48,404 / 9,128 / 88 for m = 0..3 (non-vacuous; M1 is essential). For m = 4..6 no relaxation produced survivors (up to 10^8 placements evaluated; implementations agree) — non-vacuity there is indirect.
Ledger effect: v1 88, 91, 95, 99, 102, 105 excluded [hand-proof reviewed], conditional on 4f.1 / F bipartite and M1 (pure Case A). With 86, the whole n9 = 2 pure family is closed.
Files: model_n9_2.py/.c, c_out_m*.txt, controls c_ctl*.txt, small_checks.py/_out.txt (ALL OK).
