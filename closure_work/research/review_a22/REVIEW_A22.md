# Review RA22: the OUTWARD.md section 1.2 reduction (McKay extremal list -> refined A22 at beta = 22)

Reviewer: independent agent (did not produce the claim). Date 2026-11-17/18 (UTC). Read-only except this folder.
All computations at nice 19, each under 2 minutes. Scripts and outputs are in this folder.

**VERDICT: SOUND.** The finite exception search the claim leaves open is **empty**, by my own computation. Two things
are still needed: the route's own recording of that computation, and a trust addition (section 3). The reduction is
**stronger than claimed**:

- The exception case cannot occur at L80-L83 at all, by edge count alone.
- At L84-L85 it is also empty: none of the 5 exceptional graphs has even a **one-vertex** extension that satisfies the
  12-set floor.

So at every layer 80-85, every graph in a (10,4,18, m-22) formula (in fact every graph of the class with beta = 22)
has the a22 degree family. L80, L81 and L82 are impossible by degree counting.

## Definitions used (checked against the sources, not the claim)

- **Class** (cegar90c.py docstring; LOW_LAYERS_ROUTE.md Theorem L_m): G on 24 vertices with these properties:
  - triangle-free;
  - alpha(G) <= 8, hence Delta <= 8, since a neighbourhood is independent;
  - every 12-set spans >= 12 edges (the "floor");
  - e(G) = m (the "layer").
- **Formula (s,a,b,c,h)**: (S,T) is a **maximum cut** of G with |S| = s <= 12, chosen with |S| largest. Here
  a = e(S), b = e(T), c = e(S,T), and G[S] is isomorphic to catalogue graph number h (cegar90c.py lines 22-25).
  The other families (saturation from layer m+1, delta >= 4 from Theorem B, swap, twins, lex, ...) are further
  necessary conditions.
- **beta(G)** = m - maxcut(G).
- **Lemma V** (l91/A23_ROUTE.md): beta(G) <= beta(G - v) + floor(d(v)/2), for every graph G and vertex v.
- **A22**: a(22) = 17, i.e. every triangle-free graph on 22 vertices has beta <= 17 (OEIS A389646, McKay).
- **a22 family** (cegar90c.py lines 64-73, encoder v4 onward): delta >= 6, and for every edge xy with d(x) = 6,
  d(y) = 8. It is currently gated on m - c = 23 only.

## 1. beta(G) = 22 for every graph the (10,4,18,c) formulas at L80-L85 must exclude: HOLDS

- In formulas80_c57.json ... formulas85_c63.json, each layer has exactly 8 formulas with (s,a,b) = (10,4,18), one per
  h = 0000..0007. All have m - c = 22: c = 58, 59, 60, 61, 62, 63.
- Since (S,T) is a maximum cut, every graph a formula describes has beta(G) = a + b = 22, whatever h is. The argument
  uses only "G in the class, beta(G) >= 22". It ignores h, G[S] and every other family, so it covers every formula
  and every constraint.
- It proves more: no graph of the class at L80-L82 has beta = 22, whatever its profile. This is consistent with the
  already certified UNSAT results for the other c = m - 22 profiles there.
- Each class graph is assigned to the formula of its own maximum cut (route step 3). So excluding the beta = 22
  graphs at those layers excludes exactly what these 7 formulas (12 over L80-L85) stand for.

## 2. The deletion step: HOLDS

For distinct v, u, H = G - v - u is the induced subgraph on 22 vertices, and it keeps every property it needs:

- **Triangle-free**: H is a subgraph of G.
- **alpha(H) <= alpha(G) <= 8**: an independent set of H is independent in G.
- **Delta(H) <= 8**: degrees only drop. Also implied by alpha <= 8 and triangle-freeness.
- **Floor**: every 12-set of H is a 12-set of G, and spans the same edges in H as in G, since H is induced.

Nothing else is claimed for H, and nothing else is used.

## 3. The McKay facts: HOLD, re-derived with my own code. One trust addition.

I wrote rv_filter.py independently: my own graph6 decoder, an exact alpha by branch and bound, an exhaustive minimum
over all C(22,12) = 646,646 12-sets for **every** alpha <= 8 graph (no local search), and an exact beta over all
2^21 bipartitions.

**On `minbip22_17x.g6`** (tar SHA-256 0424c19d..., as stated): output in rv_filter.out.

- 1,076 graphs, all of order 22, all triangle-free.
- alpha: 7 for 421 graphs, 8 for 539, 9 for 116. 960 have alpha <= 8, and all 960 have Delta <= 8.
- Minimum 12-set edge count among the 960: 8 for 20 graphs, 9 for 205, 10 for 533, 11 for 197, 12 for 4, 13 for 1.
- So **exactly 5** satisfy the floor: 0-based lines 605, 607, 767, 1047, 1051.

| line | edges | alpha | Delta | min 12-set | beta |
|---|---|---|---|---|---|
| 605 | 77 | 8 | 8 | 12 | 17 |
| 607 | 74 | 7 | 7 | 12 | 17 |
| 767 | 80 | 8 | 8 | 12 | 17 |
| 1047 | 81 | 8 | 8 | 13 | 17 |
| 1051 | 78 | 8 | 8 | 12 | 17 |

- They are identical, as labelled graphs, to results_minbip22_survivors.g6. Every number in OUTWARD.md 1.2 is
  confirmed.
- beta was also checked on 3 other list graphs: 17 each.

**What is assumed.** McKay's page says the x file "contains all the triangle-free graphs on N [vertices] which achieve
a(N)=A", and the non-x file holds "the subset of those which are maximal triangle-free". The route today assumes only
the **value** a(22) = 17. The claim adds the **completeness of an extremal list**, a strictly stronger assumption.

**I reduced that addition to the maximal file** (rv_maximal.py, rv_maximal.out, rv_filter_maximal.out):

1. Take any H with beta(H) = 17, alpha <= 8 and the floor. It lies in a maximal triangle-free M on the same 22
   vertices.
2. M keeps all the relevant properties: beta(M) >= 17 (beta does not decrease when edges are added), so
   beta(M) = 17 by A22; alpha(M) <= 8; and the floor holds in M.
3. So M is in the maximal file and passes the filter. Of its 338 graphs, exactly 3 do: lines 142, 195 and 302, with
   74, 78 and 81 edges.
4. Spanning subgraphs that keep the floor are closed under edge deletion, so single-deletion search from those 3
   finds all of them: 92 up to isomorphism.
5. Exactly 5 of the 92 have beta = 17, and they are isomorphic to the 5 x-file survivors. The other 87 have beta 15 or
   16.

So the needed fact rests on the **completeness of McKay's maximal-triangle-free extremal list for n = 22** (plus A22).
The x file is consistent with it. This list is what an exact a(22) search over maximal triangle-free graphs produces,
but it is still an addition to the trust base and must be stated as one.

## 4. Lemma V and its double application: HOLDS

- The statement holds for every finite graph, with no hypotheses. The proof: take an optimal bipartition of G - v and
  put v on the side holding at most floor(d(v)/2) of its neighbours.
- Applied to G at v, then to G - v at u:

  beta(G) <= beta(G - v - u) + floor(d(v)/2) + floor(d_{G-v}(u)/2), with d_{G-v}(u) = d(u) - [uv in E].

  This is exactly C22b's use (l91/A23_ROUTE.md).
- Together with section 3: either H = G - v - u is isomorphic to one of the 5 survivors, or
  beta(H) <= 16, and then floor(d(v)/2) + floor(d_{G-v}(u)/2) >= 22 - 16 = 6.

## 5. Degree conclusions and counting: HOLD. The exception case is empty.

**The exception case.** Suppose some ordered pair has floor(d(v)/2) + floor(d_{G-v}(u)/2) <= 5.

- Then beta(H) >= 17, so H is a survivor and the floor sum is exactly 5.
- Floor sum 5 forces d(v) + d_{G-v}(u) to be 10, 11 or 12. That sum is exactly the number of edges of G not in H, so
  m = e(H) + 10..12, and m >= 84 because e(H) >= 74.
- **So at L80-L83 there is no exception.** At L84-L85 only line 607 (74 edges) could qualify.
- I then showed that none of the 5 survivors can occur as G - v - u in any class graph, at any m.
  - For each survivor H and **every** independent set A of H (2,047-2,112 per graph, all sizes), I computed the minimum
    of e_H(U) + |A ∩ U| over all 11-sets U. That is the edge count of the 12-sets through a new vertex x with
    N(x) = A.
  - The best value over all A is **10** for lines 605, 607, 767 and 1047, and **9** for line 1051 (rv_sanity_all.out).
  - That is below 12 even before Delta or alpha are imposed. So H + x already violates the floor, and so does any
    24-vertex G containing H + x.
- Cross-checks for line 607 at m = 84, 85 and 86:
  - a pysat CEGAR enumeration (rv_exception.py): 0 models;
  - a SAT-free enumeration (rv_exception2.py): 0 one-vertex extensions pass;
  - a control run without the floor finds models, so the encoding is not vacuous.
- **Consequence:** in every class graph, every ordered pair has floor sum >= 6.

**Degrees.** Use 4 <= d <= 8; the bound d <= 8 comes from alpha <= 8.

- If d(v) <= 3, a pair would need d_{G-v}(u) >= 10, which is impossible.
- If d(v) is 4 or 5, every u != v needs d_{G-v}(u) >= 8. A neighbour u has d(u) - 1 <= 7, and v has a neighbour since
  d(v) >= 4. Contradiction, so **delta >= 6**.
- If d(v) is 6 or 7, every neighbour u of v needs d(u) - 1 >= 6, so d(u) >= 7.
- Take an edge xy with d(x) = 6. Then d(y) >= 7. If d(y) = 7, the pair (y, x) gives 3 + floor(5/2) = 5 < 6. So
  **d(y) = 8**.
- Conversely, I enumerated the degree cases (6, 7 or 8, adjacent or not): the only pairs with floor sum < 6 are a
  degree-6 vertex next to a degree-6 or degree-7 vertex.
- So the conclusion is exactly the a22 family, nothing more and nothing less. R91B already verified the encoded
  clauses' equivalence to this family.

**Counting.**

- With degrees in {6, 7, 8}: n6 + n7 + n8 = 24 and 6 n6 + 7 n7 + 8 n8 = 2m, so n8 - n6 = 2m - 168.
- Degree-6 vertices have only degree-8 neighbours, and each degree-8 vertex has at most 8 of them, so 6 n6 <= 8 n8.

| m | n6 | 6 n6 <= 8 n8 gives | result |
|---|---|---|---|
| 80 | n8 + 8 | n8 >= 24 | impossible |
| 81 | n8 + 6 | n8 >= 18, n6 >= 24 | impossible |
| 82 | n8 + 4 | n8 >= 12, n6 >= 16, total > 24 | impossible |
| 83 | n8 + 2 | 6 <= n8 <= 11 | feasible |
| 84 | n8 | no new bound | feasible |
| 85 | n8 - 2 | no new bound | feasible |

The arithmetic is confirmed. L80-L82 are excluded. L83-L85 get the a22 family at c = m - 22 unconditionally, with no
exception branch.

## 6. What remains

**The finite search** is not needed in the form OUTWARD proposes. What is needed instead is one tiny statement, run
once per survivor H:

> No independent set A of H gives min_U e_H(U) + |A ∩ U| >= 12.

- My scripts (untrusted) do this in seconds.
- To meet the route's standard it should be a pinned script, or a cake_lpr-checked CNF per H (22 variables plus
  floor clauses), reviewed like uenum.py. The alternative is to list it as a trusted computation.

**Also needed for L80-L82 to count as closed:**

- **A written lemma** (say "C22c") in the route, replacing the (10,4,18,m-22) formulas at L80-L82. It needs its own
  review and a mention in Theorem L_m's hypotheses (the McKay maximal list).
- **The gcert80, gcert81 and gcert82 pins.**
  - Today these checkers pin 435 formulas each.
  - Either a new subset file excluding the 8 (10,4,18) formulas, with checker coverage at 427 plus a pin and review
    for that subset, or a documented exception in close_group.py.
  - The 1 or 2 already certified (10,4,18) formulas per layer stay valid but become unnecessary.
- **Encoder route not recommended for L80-L82.** Gating a22 on c = m - 22 (a v10 encoder) is sound, but the
  contradiction there is a pigeonhole-style degree count that CDCL may find hard. The lemma route is cleaner.

**For L83-L85:**

- Gate the a22 family on m - c = 22 as well. It is sound by the lemma above.
- That needs a new encoder version, the R91B-style identity and semantic tests, a review, and gcert pins of the new
  encoder version for those 5 formulas.
- Old (10,4,18) records stay valid under their own encoder version.
- Optional extra: the counting bound 6 n6 <= 8 n8 with n8 - n6 = 2m - 168 (n8 >= 6 at m = 83) could be added as
  redundant cardinality clauses.

**Trust ledger:** add "McKay's list of maximal triangle-free 22-vertex graphs with beta = 17 is complete" next to A22.
Nothing from A23 or A23+ is used.

## Could not check

- That McKay's maximal list (or the x list) is complete. It cannot be checked here: about 143 CPU-h of independent
  search.
- Whether McKay's method produced the extremal list as an exhaustive classification, rather than only the value.
  His page says "all"; I did not see his code.
- I did not re-run the claim's own scripts (minbip_*.py). I re-derived their facts independently instead.
- I made no route or checker edits, and did not inspect gcert80-82 or close_group.py in detail. Section 6 describes
  what they would need, from LOW_LAYERS_ROUTE.md.
