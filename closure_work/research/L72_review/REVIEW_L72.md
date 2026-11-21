# RL72 review of upload_L72/CLAIM_L72.md: "L(24) >= 72" [hand-proof reviewed]

Reviewer: RL72 (independent; did not write the claim). Date 2026-11-18.
Setting: G triangle-free on n vertices, every 12-vertex induced subgraph spans >= 12 edges ("12-set condition");
L(n) = a proven lower bound on e(G). (In the source, many inline symbols were lost when it was exported; they were reconstructed from context. Every
reconstruction is forced by the arithmetic.)

## Per-step verdicts

| Step | Verdict | Notes |
|---|---|---|
| 1a Inheritance of the 12-set condition by induced subgraphs on >= 12 vertices | ACCEPT | 12-subsets of G[U] are 12-subsets of G with the same induced graph. |
| 1b L(12) = 12; averaging L(n) >= ceil(n L(n-1)/(n-2)) for n >= 13 | ACCEPT | Sum_v e(G-v) = (n-2) e(G). Values 15, 18, 21, 24, 28 recomputed. Line 34 writes "=": these are lower bounds (the CP-SAT witnesses below show they are in fact attained at n = 13..16). |
| 2 Deletion identity e(H-I) = e(H) - Sum_{v in I} d(v), I independent | ACCEPT | Each removed edge has exactly one end in I. |
| 3 Ramsey values R(3,3)=6, R(3,4)=9, R(3,7)=23 | ACCEPT | Standard (R(3,7)=23: Kalbfleisch 1966, Graver-Yackel 1968). R(3,5)=14 and R(3,6)=18 are **not used** by the claim. Every use is applied to an induced subgraph of a triangle-free graph with >= R(3,k) vertices; every "two nonadjacent among >= 3 vertices" is the trivial R(3,2)=3. |
| 4a n=17, 28 edges | ACCEPT | d <= 28-24 = 4. Degree sum 56 <= 51 + x gives x >= 5 degree-4 vertices; 6 would give an independent triple (R(3,3)), leaving 16 edges < 18 = L(14). With exactly five, the other 12 vertices have sum 36 and each is <= 3, so all are exactly 3. This is derived, not assumed: no vertices of degree <= 2 can occur. u,v are nonadjacent degree-4 vertices (5 vertices, triangle-free). At least 15-8 = 7 common non-neighbours give an independent triple (R(3,3)); {u,v,triple} is independent with sum >= 17, leaving 11 < 12. |
| 4b n=17, 29 edges | ACCEPT | d <= 5; pair rule d(u)+d(v)-1_{uv} <= 29-21 = 8 is correct (e(G-u-v) = m - d(u) - d(v) + 1_{uv} >= L(15)). At most one degree-5 vertex. If there is none: x >= 7, independent triple, leaving 17 < 18. If there is one, w: x >= 5, and every degree-4 vertex is adjacent to w (9 - 1_{uv} <= 8). Then N(w) = five independent degree-4 vertices, leaving 29-20 = 9 < 12. Degree-sum bounds use only upper bounds, so low-degree vertices only strengthen them. |
| 4c n=17, 30 edges | ACCEPT | d <= 6; pair bound 9. Degree-6 case: unique, no degree-5 (6+5-1 = 10 > 9), every degree-4 vertex adjacent to it, x >= 6 (60 <= 54+x), five of the independent neighbours leave 10 < 12. Max degree 5 case: degree-5 vertices are pairwise adjacent, so b <= 2; 60 <= 51+2b+c. b=0: c >= 9, R(3,4) gives an independent 4-set, leaving 14 < 15 = L(13). b=1: c >= 7. If w had >= 3 degree-4 non-neighbours, two of them are nonadjacent, and {w,a,b} (sum 13) leaves 17 < 18. So w has >= c-2 >= 5 degree-4 neighbours, i.e. all 5 neighbours have degree 4 and form an independent set, leaving 10 < 12. b=2: w1 ~ w2, each has >= c-2 degree-4 neighbours (same argument), and triangle-freeness makes the neighbourhoods disjoint. So 2(c-2) <= c, i.e. c <= 4, contradicting c >= 5. All cases are covered (the max-degree-6 and max-degree-<=5 split is exhaustive; b in {0,1,2}). |
| 4 => L(17) >= 31 | ACCEPT | Below 28 is excluded by the recurrence. |
| 5a n=18: 35, n=20: 46, n=21: 51 | ACCEPT | Recurrence only. |
| 5b n=19: 40 impossible | ACCEPT | d <= 40-35 = 5, x >= 80-4*19 = 4, two nonadjacent, leaving 30 < 31. |
| 5c n=22: 57 impossible | ACCEPT | d <= 6, x >= 114-110 = 4, two nonadjacent, leaving 45 < 46. |
| 5d n=23: 64 impossible | ACCEPT | d <= 6, x >= 128-115 = 13 >= 9 = R(3,4), independent 4-set, leaving 40 < 41. |
| 5e n=24: 71 impossible | ACCEPT | Recurrence gives 71. d <= 71-65 = 6, so all deficits 6-d are >= 0, with total 144-142 = 2. Exclude one vertex of positive deficit; the other 23 have total deficit <= 1. R(3,7) = 23 on them gives an independent 7-set with sum >= 42-1 = 41, leaving 30 edges on 17 vertices < 31. The arithmetic checks. Excluding a vertex is necessary (deficit 2 would only give 40, i.e. 31 edges). |
| => L(24) >= 72 | ACCEPT | So every edge layer m <= 71 has no candidate. |
| 6 Layer-72 restrictions | ACCEPT WITH REPAIR | Correct: Delta <= 72-65 = 7; not 6-regular (R(3,7), 30 < 31), so Delta = 7; every independent 7-set has sum <= 41; at most 8 degree-7 vertices (9 would give an independent 4-set by R(3,4), leaving 44 < 46 = L(20)); the degree-7 induced subgraph has alpha <= 3; N(v) for deg v = 7 is an independent 7-set, so sum <= 41 and it contains a vertex of degree <= 5. **Missing justification** (true; repair supplied): "at least 2 vertices of degree <= 5". If at most one exists, exclude it; the remaining 23 vertices all have degree >= 6 and contain an independent 7-set of sum >= 42 > 41. Then "at least 2 degree-7 vertices" follows: the degree-<=5 vertices give total deficit >= 2, and each degree-7 vertex gives excess exactly 1, with excess = deficit. (A single degree-4 vertex also has deficit 2, so the second bullet does not follow from the deficit count alone; the argument above is needed.) |
| 7 General sieve | ACCEPT WITH REPAIR | As exported it reads "then [G] cannot contain an independent k-set", which is false as stated. Correct statement: if n-k >= 12 and k*d > m - L(n-k), then **H_d** contains no independent k-set; since G[H_d] is triangle-free, |H_d| <= R(3,k)-1. The n-k >= 12 condition must be stated. The weighted 24-vertex version is as checked in 5e. |
| Claim header "previously stated 67-edge threshold" | n/a | No bearing on the proof. |

## Computational evidence (all under research/L72_review/; uncertified CP-SAT unless noted)

- arith_check.py / arith_check.out: mechanical replay of every numeric step (recurrence values, degree caps, counts, deletions).
- cpsat_floor.py (pure model: triangle-free + all 12-sets >= 12 + total edges):
  - cpsat_small.jsonl: n=13, <= 14 edges INFEASIBLE; witnesses for n=13 (15), n=14 (18), n=15 (21), re-checked in Python.
  - cpsat_chain.jsonl: n=14 <= 17 (with floor 13:15), n=15 <= 20 (floors 13,14), n=16 <= 23 (floors 13..15) all INFEASIBLE.
    Witness at n=16 with 24 edges. So L(13..16) = 15, 18, 21, 24 exactly.
  - cpsat_17.jsonl: control n=17, 31 edges FEASIBLE (witness re-checked). So L(17) = 31 exactly and the lemma is sharp.
    The unsplit n=17 <= 30 run (floors 13..16) hit its 2400 s limit (UNKNOWN).
- cpsat_degsplit.py (n=17, split by nonincreasing degree sequence; floors 12..16 imposed on all k-sets; no min-degree
  assumption, so degree-0/1/2 vertices are included):
  - degsplit_28.jsonl: 34/34 sequences INFEASIBLE.
  - degsplit_29.jsonl: 50/50 sequences INFEASIBLE.
  - m=30 (362 sequences): PARTIAL, budget-capped. degsplit_30_partial.jsonl: 116 INFEASIBLE (all degree-6
    sequences plus the high-b ones, in descending order down to [5^8,3^5,2,2,1,0]). degsplit_30_b012.jsonl (run30_b012.py):
    38 of the 56 remaining b<=2 sequences INFEASIBLE before the cap. In total 154/362 checked, 0 feasible; 208 unchecked.
  These checks are conditional on the floors L(13..16), which are checked by the chain above.
- cegar_floor.py (pysat/CaDiCaL lazy 12-set CEGAR, for LRAT): n=13 <= 14 edges UNSAT in 674 s (CNF cnf/n13_le14.cnf).
  The n=17 run with floors timed out at 2700 s. CDCL cannot do the averaging (counting) steps efficiently, so **no LRAT /
  cake_lpr certificate** was produced for the n=17 lemma. The SAT label for the lemma remains open.

## Overall

L(24) >= 72: **ACCEPT** [hand-proof reviewed]. Steps 1-5 are correct as written (after reconstructing the missing symbols). Section 3
needs one supplied justification; section 4 needs a precise restatement. Neither affects the main result.
This gives an elementary, SAT-free second proof that edge layers <= 71 contain no candidate. Context: layers 51-71 are already
recorded by SAT; m <= 50 is covered by Razborov 2022; STATE.md cites BCL low density for m <= 71. It is not an order-24 claim, and layer 72 stays open.
