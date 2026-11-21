# Layers 87 down to 51: one uniform reduction (producer's note, version 7: version 6 plus one fact, the third encoder-v9 record (L83_s10a4b18c61_0000, audited 2026-11-18, group G8 of layer 83), gate review `closure_drafts/review_RCL/`; version 6: version 5 with the fixes of review RV5, research/route_v5_review/REVIEW.md (1 must-fix, 10 should-fix; no change to any formula, encoder, checker or pin); version 5: version 4 plus Corollary C22c-83 for layer 83, review research/c22c83/REVIEW.md; version 4: version 3 plus encoder version 9 for layers 83–85, review research/v9_review/REVIEW.md; version 3: version 2 plus Lemma C22c for layers 80–82, reviews research/review_a22/REVIEW_A22.md and research/a22_review2/REVIEW.md + FIX_CHECK.md)

Sun 2026-11-15, 19:15 AKST (date of version 2; versions 6 and 7: 2026-11-18). Model: `l88/L88_ROUTE.md` v2 (reviewed: R88A 0 must-fix; cross-vendor review 0 must-fix) and
`l89/L89_ROUTE.md` v3. This note states the reduction once for every m with 51 ≤ m ≤ 87; the per-layer numbers are in the
table below and are reproducible with the commands given. 51 is the least possible edge count: averaging the 12-set floor
over all 12-sets gives m ≥ 12·C(24,2)/C(12,2) = 50.18…

## Theorem L_m (51 ≤ m ≤ 87), conditional

Assume A22; the closure of layer m + 1 (for m = 87: `l88`, which assumes layers 89–96, BCL 2(b), A22); Theorem A
(saturation) and Theorem B (δ ≥ 4); the completeness of the H catalogue (uenum.py). Then no graph on 24 vertices is
triangle-free, has α ≤ 8, has ≥ 12 edges in every 12-set and has exactly m edges. The layers close in the order
87, 86, …, 51, each using the one above.
For m ∈ {80, 81, 82, 83} also assume McKay-max (section "Lemma C22c"); it is used directly only for the formulas listed in
`a22c/LEMMA_C22c_EXEMPT.json` (9 tags, all (10, 4, 18, m − 22)). Theorem L_m for every m ≤ 79, and any final
order-24 result, inherit McKay-max through L80 and L83 while the exemption is in use.
For m ∈ {84, 85} the certificate of one formula each rests on the version-9 symmetry argument (at m = 83 one more formula has a version-9 certificate, but Corollary C22c-83 closes it independently) (research/v9/SYM_V9.md §3; a reviewed argument,
not a checked one; "Dependencies" below); Theorem L_m for every m ≤ 83 inherits it through L84 and L85.

## Proof outline (for every m, 51 ≤ m ≤ 87)

1. Saturation (Theorem A at m needs layer m + 1 closed: adding a non-edge with no common neighbour keeps the class and
   gives m + 1 edges); Δ ≤ 8; δ ≥ 4 (Theorem B).
2. Cut: degree sum 2m ≤ 174 < 192 gives v with d(v) ≤ 7; G − v has degree sum ≤ 2m < 184 gives u with d_{G−v}(u) ≤ 7;
   A22 + Lemma V twice: β(G) ≤ 23, so mc(G) ≥ m − 23. (No lower bound on degrees is used.)
3. Profiles: `uprofiles.profiles(m, cut_lb=m − 23)`; no s = 12 profile (a 12/12 cut has c ≤ m − 24). From m = 87 down,
   profiles with s = 8 occur (S an 8-set; c ≤ 8·8 − 2a ≤ 64): 1 formula at m = 87, 2 at m = 86, 3 for m ≤ 85.
4. Formulas: `gformulas.py formulas<m>.json <m>` (generator unchanged), subset c ≥ m − 23 →
   `formulas<m>_c<m−23>.json` (table). Observed: for every m the s ≥ 9 profiles are the same (s, a, b) as at m = 88 with
   c = m − a − b, the same H catalogue; 432 formulas with s ≥ 9 per layer.
5. Encoder: version 7 (cegar90c.py, 7699f39b…) for s ≥ 9; **version 8** (`v8/cegar90d.py`, 3c91eb94…) for s = 8:
   version 7 with one change, `check_formula` accepting s = 8 (version 7 refuses s < 9). For s ≥ 9 the two give the same
   CNF. Reviewed by R-LOW (0 must-fix): every family's derivation (BOUNDS90.md) holds at s = 8 and for general m; the
   diff of cegar90d against cegar90c is exactly a docstring and `8 <= s`; v7 and v8 give byte-identical CNFs on all 19
   s ≥ 9 profiles at m = 87 and m = 51; v7 refuses every s = 8 formula. Data in "Facts" below.
   **Version 9** (`code/cegar90e.py`, 7c416f1c…; added in version 4 of this note; permitted by the checkers at layers 83–85 only, and used by exactly three records, named below; review R-V9,
   research/v9_review/REVIEW.md: ACCEPT-WITH-FIXES, no soundness defect, encoder unchanged by the fixes): version 7 plus
   the family `auts`, appended at the end of the base formula after `twins`. For automorphisms σ of H outside the twin
   subgroup (generators of Aut(H)/W, `residual_generators`) it adds the lex inequality key(λ) ≥ key(σλ) on the key of
   `twins` (T-degrees of S, then the S × T matrix row by row). Sound by the maximum argument of `twins`: the labelling of
   largest key over Aut(H) × Sym(T) satisfies lex, twins and every such inequality at once (research/v9/SYM_V9.md). With
   `auts` left out the CNF is byte-identical to version 7's; formulas without such automorphisms (H 0004, 0006 of
   (10,4,18), and 160 of the 432 s ≥ 9 formulas per layer) get exactly the version-7 CNF. Like version 7 it refuses
   s = 8. Used by exactly three records: L85_s10a4b18c63_0000, L84_s10a4b18c62_0000 and (version 7) L83_s10a4b18c61_0000 (all H 0000 of (10,4,18), residual symmetry 24). The layer-83 record is a certificate for a formula that Corollary C22c-83 also closes (step 7); the H-0001 formulas at m = 84, 85 have version-7 records (RV5 must-fix 1), and L83_s10a4b18c61_0001 has no certificate. Data in
   "Version 9" below.
6. Certificates: grun90 (v7) / grun90v8 (v8) records, produced on GitHub Actions (untrusted). Checker
   `l<m>/code/gcert<m>.py`, made by `code/make_gcert.py` from gcert88.py: formulas pin, own name, run label, messages, and
   encoder version 8 added (pinned) with records required to name v7 or v8. Audited in groups by independent auditors;
   coverage of all formulas checked per layer. For m = 83, 84, 85 (version 4 of this note) the checker is regenerated by
   `code/make_gcert_v9.py` from the installed gcert<m>.py: encoder version 9 added (pinned, label v9), records may name
   v7, v8 or v9; nothing else changes. Earlier audits of those layers stay valid (the new checker treats v7/v8 records
   exactly as before; its code hash differs, so its CHECK_RESULTS cannot resume the old checker's).
7. Layers 80–83 only: Corollary C22c-80 (section "Lemma C22c") shows that no class graph with m ∈ {80, 81, 82} edges
   has mc ≤ m − 22, so a formula with c ≤ m − 22 describes no graph: a formula's (S, T) is a maximum cut of the graph it describes, so its c equals mc(G) (profile definition, `uprofiles.py` docstring; RV5 should-fix 3). The formulas of `a22c/LEMMA_C22c_EXEMPT.json`
   (no checked certificate) are closed by it; every other formula of these layers keeps its certificate.
   Coverage: `code/union_lemma.py` (pinned, 7617024f365efc1a82a850026103abc6bcfa575f1722a84f5130e4c3b8d182d6) re-reads every group's CHECK_RESULTS as close_group.py does and requires
   certified ∪ exempt = the 435 formulas, each exempt tag with c ≤ m − 22; output `l<m>/audit/UNION_CHECK.txt`.
   Layer 83 (version 5): Corollary C22c-83 shows the same for m = 83 (no class graph with 83 edges has mc ≤ 61); the two
   formulas listed under "83" in `a22c/LEMMA_C22c_EXEMPT.json` are closed by it, the other 433 keep their certificates;
   the same union check gives `l83/audit/UNION_CHECK.txt`. A v9 certificate for these two tags is redundant for coverage; since version 7 one exists for L83_s10a4b18c61_0000 (audit group G8), the exemption file is unchanged, and `union_lemma.py` reports that tag as "exempt and also certified" (433 + 1 certified, 1 by the corollary alone).

## Facts for 51 ≤ m ≤ 87 (R-LOW should-fix 3; data from reviews/RLOW_REPORT.md, review_RLOW/t/)

- Profiles: 20 at m = 87, 21 at m = 86, 22 for m ≤ 85. The s = 8 profiles are (8,0,23,c) from m = 87, (8,0,22,c) from
  m = 86, (8,1,22,c) from m = 85; the least s is 8. The s ≥ 9 (s, a, b) are the same 19 at every layer, with the same H
  lists as layer 88 for each (s, a, b, h_index): 432 formulas with s ≥ 9 per layer.
- Gates: a22 fires exactly at c = m − 23 (327 formulas at m = 87, 327 at m = 86, 328 for m ≤ 85); b22 exactly at
  c = m − 22 (100 at m = 87, 101 for m ≤ 86). tbip, isolates and symmetry fire on 0 formulas (tbip's gate c ≥ 67,
  b + c ≥ 83 is never met; isolates needs (11,8,15,69); symmetry needs s = 12).
- s = 8 encodings (v8): about 3.45–3.51 million clauses, of which floors about 3.33–3.39 million; a22 18,232 (or
  18,132 for (8,1,22,·)), b22 18,980; swap 1,024; twins 812 (7 pairs; 696 and 6 pairs for H = {6,7}); iso8 gives no
  clauses at s = 8 (b ≤ 23 < 24 = 3(t − 8)); triangles, sdeg, tdeg, totals, lex, saturation and arith fire everywhere.
- Every rebuild with an empty lazy list equals the build (all 9 s = 8 formulas of m = 87, 86, 85, 51 checked).
- uprofiles does not prune with the δ ≥ 4 degree sums (2a + c ≥ 4s, 2b + c ≥ 4t); at m = 51, 21 of 22 profiles violate
  them, so those formulas are trivially UNSAT. This costs time only.

## Dependencies kept explicit (R-LOW should-fix 2)

- Why no profile has s ≤ 7 for m ≤ 87. For m ≥ 80 the degree bound c ≤ 8s − 2a ≤ 56 < m − 23 excludes s ≤ 7. For
  m ≤ 79 it does not (m − 23 ≤ 56); what excludes s ≤ 7 there is P4's averaging floor on the large side: with t = 24 − s,
  b = m − a − c ≤ 23 (because c ≥ m − 23), while F(17) = 25 and F(t) ≥ 28 for t ≥ 18, where F(t) = ⌈12·t(t−1)/132⌉ is the
  least number of edges a t-set can span given the 12-set floor (averaging). So t ≥ 17 is impossible and s ≥ 8.
- F(16) = ⌈240/11⌉ = 22 is load-bearing: it keeps s = 8 to b ∈ {22, 23}; without it (8,0,21,64) would enter at m = 85.
- The 14-F lemma, P5 (s = 11 ⇒ a ≥ 7), F(16) = 22 and F(t ≥ 17) ≥ 25 do not depend on m (R-LOW re-derived 14-F, P5 and
  t(t − 1)/11 by hand).
- The cut bound uses only A22, Lemma V, triangle-freeness and α ≤ 8; saturation clauses use layer m + 1 closed; δ ≥ 4
  uses Theorem B (Lean `four_le_degree`, no edge-count hypothesis).
- Catalogue completeness (uenum.py) stays a trusted computation.
- McKay-max (used directly in layers 80–83; layers 80–82 also inherit it through layer 83; inherited by L_m for every m ≤ 79 and any final order-24 result): every maximal triangle-free graph on 22 vertices with β = 17 is isomorphic to a graph
  of `minbip22_17.g6` (67b6e19e…, in minbip.tar 0424c19d…; a22c/TRUST_ENTRY.md). A trust entry next to A22, from the
  same McKay computation. Used directly only by Lemma E, so directly only by the exempt tags; inherited
  through L80 and L83 by every lower layer and the final result.
- Check W (witness file 06311d4e…, verified by mx_witness_check.py f53aab3e…) and Check B (3 CNFs, generator
  excB_gen.py 308d3d4e…, LRAT proofs accepted by cake_lpr 29e02af7…) are recorded checks, not trusted computations
  (a22c/EXCEPTION_CHECK.md). Lemma C22c and its two corollaries use neither Theorem A, Theorem B, the catalogue nor any
  other layer.
- Definitions used without restating them here (L88_ROUTE.md, `uprofiles.py`, `gformulas.py`): a profile (s, a, b, c) is a maximum cut (S, T) of G
  with |S| = s, a edges inside S, b inside T and c = mc(G) across; a formula is a profile with one graph H = G[S] of the catalogue. The labels
  P1–P6 are defined in the docstring of `l88/code/uprofiles.py`, which says they are proved in ULAYER_REPORT.md (this note gives no path for
  that report); 14-F and the 11-set floor are named in L88_ROUTE.md. "BCL 2(b)" is the theorem inherited through layer 88
  (l88/L88_CLOSURE.md). Theorem A is the saturation statement of step 1 (hypothesis 3 of l90/L90_ROUTE.md); this note gives no location for
  its proof.
- The trusted checker of every layer certificate is cake_lpr (29e02af7…, CakeML-verified); gcert<m>.py rebuilds the CNF with the pinned
  encoder, compares the CNF and proof hashes with the record, and calls it. The soundness of the encoder's clause families (BOUNDS90.md; `twins`; `auts`) is a set of reviewed arguments, not
  checked ones.
- Paths (RV5 should-fix 7): `l<m>/`, `a22c/`, `v8/`, `code/`, `pre_v9/` are relative to `layers/`; `research/`, `l88/`, `l89/`, `l91/` to the
  scratchpad root; `audit_kit/`, produce.yml, ops/pool.py, ccc90.py to the repository clone `gh/order24-compute/`. `cegar90e.py` is at
  `l83/code/`, `l84/code/`, `l85/code/` and the repository's `code/` (not in `layers/code/`); cegar90c.py is in every `l<m>/code/`; uprofiles.py, gformulas.py and
  uenum.py are in `l88/code/` (scratchpad root), where `code/gen_all.sh` runs them; BOUNDS90.md has copies at `l90/BOUNDS90.md` and in
  `l90/review_R90B/in/` and `l90/review_R90D/in/` (the copies given to those reviews); the first two differ, and this note does not say which
  version each family's review read.
- Pins not stated elsewhere: make_gcert.py b502f405…, make_gcert_v9.py 4cd688cb…, close_group.py 18e57227…, a22c/SHA256SUMS 60105cff…; in `l88/code/`: uprofiles.py 9261343a…, gformulas.py 700f0423…, uenum.py 960df182…, gcert88.py 23efd4b7….
- `code/union_lemma.py` (7617024f…) still calls itself a draft for layers 80–82 in its docstring and labels every exemption "exempt by
  Corollary C22c-80" in its output, also for the two layer-83 tags, which are exempt by Corollary C22c-83 (RV5 should-fix 8). Its logic is
  as reviewed; the text is left unchanged so that the pinned hash stays valid.
- The subset maker (a heredoc in code/gen_all.sh) is not pinned to the full file's hash; R-LOW reproduced its bytes for
  all 37 layers.
- `code/close_group.py` accepts v8 (required for s = 8) and v7 or v8 for s ≥ 9, as the checker does (R-LOW s-f 1);
  since version 4 of this note also v9 for s ≥ 9, and only when M ∈ {83, 84, 85} (R-V9 should-fix 6).
- Version 9 adds one trusted argument (research/v9/SYM_V9.md §3), of the same kind as the reviewed `twins` argument, and
  rests on the same reviewed fact: every family other than lex and twins holds under every relabelling in Λ(G). Its
  counters are exact because Δ(G) ≤ 8 for every class graph (SYM_V9.md §5).

## Lemma C22c (β = 22 at order 24, from A22 and McKay's maximal list)


**Definitions.** For a graph G: β(G) = e(G) − mc(G), with mc(G) the largest cut. The *floor* of a graph on n ≥ 12
vertices: every 12-set of vertices spans ≥ 12 edges. The *class*: graphs on 24 vertices that are triangle-free, have
α ≤ 8 and the floor (Theorem L_m, without the edge count).

**Facts used, and nothing else.**

- **A22** (in the trust ledger already): every triangle-free graph on 22 vertices has β ≤ 17 (OEIS A389646, McKay).
- **McKay-max** (new trust entry, TRUST_ENTRY.md): every maximal triangle-free graph on 22 vertices with β = 17 is
  isomorphic to one of the 338 graphs of `minbip22_17.g6` (SHA-256 67b6e19e…bfe4, member of McKay's `minbip.tar`,
  SHA-256 0424c19d…7215). Only completeness is assumed: nothing about the listed graphs themselves (that they are
  maximal, or have β = 17) is used.
- **Lemma V** (l91/A23_ROUTE.md, reviewed R91A, RA22): β(G) ≤ β(G − v) + ⌊d(v)/2⌋ for every graph G and vertex v.
- **Check W** (recorded, EXCEPTION_CHECK.md §1): for each of the 338 lines of `minbip22_17.g6` except 142, 195 and 302 (0-based line indices, here and below),
  the witness file (SHA-256 06311d4e…e110) names a 12-set spanning ≤ 11 edges; `mx_witness_check.py` (SHA-256
  f53aab3e…70ec) re-verifies every witness (exit 0).
- **Check B** (recorded, EXCEPTION_CHECK.md §2): for L ∈ {142, 195, 302}, the CNF B_L made by `excB_gen.py` (SHA-256
  308d3d4e…96d5) from line L and its lazy list is UNSAT; cake_lpr (29e02af7…) accepted CaDiCaL's LRAT proof for each.
  B_L is satisfiable whenever there are a spanning subgraph H of M_L (the graph of line L) with the floor and an
  independent set A of H with e_H(U) + |A ∩ U| ≥ 12 for every 11-set U (each clause family of B_L states one of these
  conditions, for the listed sets only; the cardinality encoding is Sinz's sequential counter, exhaustively tested for
  n ≤ 8 by `test_card.py`).

**Lemma E (no floor-keeping one-vertex extension).** Let H be a triangle-free graph on 22 vertices with β(H) = 17 and
the floor. Then for every independent set A of H there is an 11-set U ⊆ V(H) with e_H(U) + |A ∩ U| ≤ 11.

*Proof.*
1. Add non-edges to H one at a time while no triangle forms. This ends in a maximal triangle-free graph M′ on V(H)
   with E(H) ⊆ E(M′).
2. β(M′) ≥ β(H) = 17, since every bipartition leaves at least as many edges of M′ uncut as of H. By A22, β(M′) = 17.
   So by McKay-max there is a bijection φ: V(H) → {0, …, 21} that maps M′ onto M_L for some line L of the file.
3. M′ has the floor, because H has it and E(H) ⊆ E(M′). Isomorphism keeps the floor, so M_L has it. By Check W, every
   line other than 142, 195 and 302 has a 12-set with ≤ 11 edges. So L ∈ {142, 195, 302}.
4. Suppose A is independent in H and e_H(U) + |A ∩ U| ≥ 12 for every 11-set U. Then φ(H) is a spanning subgraph of
   M_L with the floor, φ(A) is independent in φ(H), and φ(A) meets every 11-set U as required. So B_L is
   satisfiable: put y_e true iff e ∈ φ(H), x_i true iff i ∈ φ(A), and the counter variables as the counts they name.
   This contradicts Check B. ∎

α(H) and Δ(H) are not used. The 11 graphs of the maximal file with α = 9 are excluded by the floor witnesses too.

**Lemma C22c.** Let G be in the class with β(G) ≥ 22. Then:
- (a) for all distinct vertices v, u: ⌊d(v)/2⌋ + ⌊d_{G−v}(u)/2⌋ ≥ 6;
- (b) δ(G) ≥ 6;
- (c) if xy is an edge and d(x) = 6, then d(y) = 8.

*Proof.*
1. **(a)** Let H = G − v − u, the induced subgraph on 22 vertices.
   - H is triangle-free.
   - Every 12-set of H is a 12-set of G and spans the same edges, so H has the floor.
   - By A22, β(H) ≤ 17. Suppose β(H) = 17. Let A = N_G(v) ∩ V(H). A is independent, because N_G(v) is independent in
     the triangle-free G. For every 11-set U ⊆ V(H), U ∪ {v} is a 12-set of G, so 12 ≤ e_G(U ∪ {v}) =
     e_H(U) + |A ∩ U|. This contradicts Lemma E. So β(H) ≤ 16.
   - Lemma V applied to G at v, then to G − v at u: 22 ≤ β(G) ≤ β(H) + ⌊d(v)/2⌋ + ⌊d_{G−v}(u)/2⌋ ≤
     16 + ⌊d(v)/2⌋ + ⌊d_{G−v}(u)/2⌋.
2. **Δ(G) ≤ 8**, since N(v) is independent and α ≤ 8.
3. **(b)** Let d(v) ≤ 5.
   - If d(v) ≤ 3, (a) needs ⌊d_{G−v}(u)/2⌋ ≥ 5, so d_{G−v}(u) ≥ 10 > 8, for any u ≠ v. Impossible.
   - If d(v) ∈ {4, 5}, (a) needs d_{G−v}(u) ≥ 8 for every u ≠ v. v has a neighbour u, and d_{G−v}(u) = d(u) − 1 ≤ 7.
     Impossible.
4. **(c)** Apply (a) to (v, u) = (x, y): 3 + ⌊(d(y) − 1)/2⌋ ≥ 6, so d(y) ≥ 7. If d(y) = 7, (a) for (v, u) = (y, x)
   gives 3 + ⌊(6 − 1)/2⌋ = 5 < 6. So d(y) = 8. ∎

(b) and (c) are exactly encoder family `a22` (cegar91.py onward; R91B showed the clauses state exactly δ ≥ 6 and (c)).
Here they are proved for β ≥ 22, not only for β = 23 as in Corollary C22b. Conversely, (b) and (c) imply (a) (RA22 §5
enumerated the cases), so nothing weaker is lost.

**Corollary C22c-80.** For m ∈ {80, 81, 82}, no graph of the class with m edges has β ≥ 22. So such a graph has
mc ≥ m − 21.

*Proof.* Suppose G is one.
1. By (b) and Δ ≤ 8, every degree is 6, 7 or 8. Let n_k be the number of vertices of degree k. Then
   n6 + n7 + n8 = 24 and 6n6 + 7n7 + 8n8 = 2m, so n8 − n6 = 2m − 168.
2. By (c), each of the 6n6 edge ends at degree-6 vertices goes to a degree-8 vertex. In particular no edge joins two
   degree-6 vertices, so these are 6n6 distinct edges. A degree-8 vertex takes at most 8 of them, so 6n6 ≤ 8n8.
3. The three layers:
   - m = 80: n6 = n8 + 8, so 6n8 + 48 ≤ 8n8, so n8 ≥ 24 and n6 ≥ 32 > 24.
   - m = 81: n6 = n8 + 6, so n8 ≥ 18 and n6 ≥ 24, total ≥ 42 > 24.
   - m = 82: n6 = n8 + 4, so n8 ≥ 12 and n6 ≥ 16, total ≥ 28 > 24.

   Each is a contradiction. ∎

The corollary uses neither saturation (Theorem A), nor Theorem B, nor the closure of any other layer, nor the H
catalogue. At m = 83 this count alone allows n8 ∈ [6, 11], so Corollary C22c-80 stops at 82; Corollary C22c-83 below
adds the step n6 ≤ α and closes m = 83.

**Corollary C22c-83.** No class graph with m = 83 edges has mc(G) ≤ 61. Hence every layer-83 formula with c ≤ 61 describes no graph; in
particular L83_s10a4b18c61_0000 and L83_s10a4b18c61_0001 (both (10, 4, 18, 61)).

*Proof.* Suppose G is a class graph with 83 edges and mc(G) ≤ 61, so β(G) ≥ 22 and Lemma C22c applies. Let n_k be the number of vertices of degree k and D_k the set of them. By (b) and Δ ≤ 8: n6 + n7 + n8 = 24 and
6 n6 + 7 n7 + 8 n8 = 2m = 166. Subtracting 7 · 24 = 168:  n8 - n6 = -2, so n6 = n8 + 2.
1. By (c) every neighbour of a vertex of D6 lies in D8. So D6 is an independent set, hence n6 ≤ α(G) ≤ 8, hence n8 ≤ 6.
   (This step, n6 ≤ α, is the one not used in Corollary C22c-80.)
2. The 6 n6 edges leaving D6 all end in D8, and D8 has 8 n8 edge ends: 6 n6 ≤ 8 n8, i.e. 6 n8 + 12 ≤ 8 n8, so n8 ≥ 6.
3. So n8 = 6, n6 = 8, n7 = 10, and 6 n6 = 48 = 8 n8: every edge end at D8 is used by an edge to D6. So every neighbour
   of a vertex of D8 lies in D6.
4. A vertex of D7 has no neighbour in D6 (step 1: neighbours of D6 are in D8) and none in D8 (step 3). So all 7
   neighbours of each vertex of D7 lie in D7: G[D7] is a 7-regular graph on 10 vertices, with 35 edges.
5. G[D7] is triangle-free, and a triangle-free graph on 10 vertices has at most floor(10^2 / 4) = 25 edges (Mantel).
   (Equivalently: the 7 neighbours of a vertex form an independent set, each with 7 neighbours outside it, needing
   ≥ 14 vertices.) Contradiction. ∎

Corollary C22c-83 uses neither saturation, nor Theorem B, nor the closure of any other layer, nor the H catalogue
(review research/c22c83/REVIEW.md). At m = 84 and m = 85 the same count leaves solutions (n6 = n8 ≤ 8; n8 = n6 + 2, n6 ≤ 8).


## Version 9 (layers 83–85; added in version 4 of this note)

- Encoder `code/cegar90e.py` 7c416f1c6e33c6b95ebea72210ecfc0afa8f3b9ec7e29fa844145c118828de8e; diff against cegar90c.py:
  research/v9/diffs/cegar90e_vs_cegar90c.diff (docstring, `FAMILIES` + 'auts', `automorphisms`,
  `residual_generators`, `auts()` called last in `build()`). Soundness note research/v9/SYM_V9.md; review R-V9
  research/v9_review/REVIEW.md (ACCEPT-WITH-FIXES; the fixes concern installation, documentation and producer code).
- (10,4,18) generators and new clauses (independent of c): H 0000 (2-3, 4-5, 6-7, 8-9): (2 4)(3 5), (4 6)(5 7),
  (6 8)(7 9), 690 clauses, 87 variables; 0001: (5 7)(6 8), 230; 0002: (4 5)(8 9), 230; 0003: (4 5)(6 7)(8 9), 348;
  0005: (5 6)(8 9), 230; 0007: (6 7)(8 9), 230; 0004, 0006: none.
- Identity: on formulas83_c60, formulas84_c61 and formulas85_c62 (432 s ≥ 9 formulas each) v9 with `auts` off = v7 byte
  for byte, v9's base extends v7's base (prefix), formulas without generators are byte-identical; recorded v7 CNFs
  (lazy lists from records) are reproduced by v9 with `auts` off (research/v9/tests; R-V9 §4 on its own sample).
- Records: "encoder": "v9"; produced by ccc90.py with ENCODER=cegar90e (produce.yml input `encoder`; ops/pool.py
  carries the encoder of the wave it continues). v9 cube trees start from scratch (a v7 state folder is refused under
  v9); the v7 states are kept.
- Checkers: gcert83 (03b8b298…), gcert84 (c94cb7a0…), gcert85 (7b98319e…), made by make_gcert_v9.py; audit_kit/l83–l85
  PINS.sha256 add cegar90e.py.

## Per-layer data (reproduce: `code/gen_all.sh`, `code/make_gcert.py <m>`; for m = 83, 84, 85 then `code/make_gcert_v9.py`)

| m | cut ≥ | formulas | s = 8 | profiles | subset SHA-256 | full file SHA-256 (prefix) | gcert SHA-256 (prefix) |
|---|---|---|---|---|---|---|---|
| 87 | 64 | 433 | 1 | 20 | 1cac80d148df1b57eca58f832c020d32ba851e1e18aa61ed5058842d388a4365 | 7519437e1a9b8aec | c43956c02efa8854 |
| 86 | 63 | 434 | 2 | 21 | fb6534d28a8f8ffea92be3d8b1662a744d5b7195c1298c07c1e30a2abf866c35 | 8be2c86a505800a2 | c79723d12d966406 |
| 85 | 62 | 435 | 3 | 22 | bbc8d1c67e1fb0ffbd486caf436cdefb530dc9ac2198dbdb88ece256f7f1cd64 | 87e27ab6f139f3d5 | 7b98319ef479dfe3 |
| 84 | 61 | 435 | 3 | 22 | d0cd20441c75c958ee123144395b6af9af93022b2f064c41017aad0b97a3c557 | 48fa24c5e3589b1e | c94cb7a0e5b0f262 |
| 83 | 60 | 435 | 3 | 22 | f15403b2edb588166563d2d7aed95c0ccc173379719fd7fc1d3e51bb9d77af73 | 9f194816d9ce5964 | 03b8b2985cba8509 |
| 82 | 59 | 435 | 3 | 22 | 75d77a7fbf033db5b9b4bdb08dbcd6327723243c39bd517996fec5e16d8fc521 | 6e1f54b2f6ff5620 | 0b3b7b57bacc86a0 |
| 81 | 58 | 435 | 3 | 22 | 3a8af3389222566dffdd81a1cba143af7bc0e5101de0a5bf2300c6cd97a035ec | dd9a17fa91697fe5 | 21cdd2ef6026b6d2 |
| 80 | 57 | 435 | 3 | 22 | d334f1fc3195bdc7a464234ba4daa3df6f8c1c468f3e346f261c85f6a8520690 | aa81ee7f8b7e1891 | a558a04e3c013ac9 |
| 79 | 56 | 435 | 3 | 22 | 20b50b5da7c9658168e11c9c810cacad5a95d800659db02b5c1264e6739c6124 | ed2b89010e2ed237 | 0160636717b49e9c |
| 78 | 55 | 435 | 3 | 22 | bb7f41e956b8bc34a27df5f922928589e5b63e45707d87100bd40ffe6b1f5e33 | 9dd96e7c73d3206e | f0a977e9a7b054fb |
| 77 | 54 | 435 | 3 | 22 | 3444441d8ef44434aa59c4183284359d5fcce735e27ea7dbc38b1fb2ae0fa576 | 5d60885c08526237 | cd18fff10c4b4c01 |
| 76 | 53 | 435 | 3 | 22 | b3c41e6d9a0f6af017489df376547fc56bd24b8c72ccf726785218a40eac1cc4 | 3836965858b3c5bf | 571cbe0cecbc9636 |
| 75 | 52 | 435 | 3 | 22 | 87ccefc254dec809f144aaf5877410134d10d3517ee447fca4dcf14cd05a3f2f | 80eef7bf6692a123 | 8bc617261437d41c |
| 74 | 51 | 435 | 3 | 22 | 1a5f53340c8f4beab1915602bba9cb2b65244a0b470ddaadb5e153476abc74a6 | ac3034982a14cf86 | 67b0c991a50203fa |
| 73 | 50 | 435 | 3 | 22 | 48a49f60f4442e83187714316c8b5bb822ac5c04fb895a05d52b3e5ec732ff1a | 4c21acf96ba14feb | 97af794ba183ac8a |
| 72 | 49 | 435 | 3 | 22 | 3788e2b1623323daa705766ef95ebcc05208a63bbdffeb9c582479333ae5de9f | 76cea8d8626ec48f | f5308a058f0272ad |
| 71 | 48 | 435 | 3 | 22 | 7a43aca405bb8a8f662f355e604d70ce451d322170fec9ec2b7e6bfeb15eda94 | a6311ca164e3f15d | db8e91fcef68d105 |
| 70 | 47 | 435 | 3 | 22 | 4148d61b2339142b0fb77ba6e0befefb319438b061fd3031b200147d7a5f1127 | 3202e17349badd45 | ff0fcdb84d17b50a |
| 69 | 46 | 435 | 3 | 22 | 8e5363e7be36a9a1b2102509cdda75a6839fde0a5e224682a87f66dd92a29ad4 | 93bbfb6d3f9bce18 | 77a89d6b5e109c23 |
| 68 | 45 | 435 | 3 | 22 | 16e8e4394987f0771960bc58f007f03eeca976913533baf3a8c7ebeb0d1d3f99 | 2559fe0745e6899f | 490df6112540c773 |
| 67 | 44 | 435 | 3 | 22 | 6bf4c206850fe0c179ed6757a96e84cd26cf31dc85c1496118d9d12fbee67a65 | 6656789fd217b287 | a2540dc15575f9ae |
| 66 | 43 | 435 | 3 | 22 | 1dede7fa43c953209be6c31b89b6475c2f11e8440c01ab4d208d347e9b6a3029 | d0c9615c6f50383e | 8ce2cd3507b3776a |
| 65 | 42 | 435 | 3 | 22 | 8e9b565647b120c4cd1f0e1cb8c7a89e64bab139173aa1c4cf836112a72b35e5 | 6b7d468512e214f9 | 1fc7f081c25ad75a |
| 64 | 41 | 435 | 3 | 22 | 171050da397279eee8e43e706bc6ec15d9a8167b1aa5da8c88704d5a56fcd2f9 | cc3d486e0a175a8d | b27ef3a571823475 |
| 63 | 40 | 435 | 3 | 22 | f7d635d8940bb27e032c8f2090709403c4627a26b859f00969410e5f4c670a83 | b4339043742e6c2f | d2389048736dad3e |
| 62 | 39 | 435 | 3 | 22 | 74272e9098ec4d344bd6c5849aae9ae4a7cbad3b09539d35e9c13383caf85009 | 9040089bdecdacfa | a311a8aa3d512250 |
| 61 | 38 | 435 | 3 | 22 | c614c709092380e71ca6ffd805c99c691ef3111588d8452ef84fe69a200bc87c | 0c146df6d10c036e | aed3e3fd8c4d7b4f |
| 60 | 37 | 435 | 3 | 22 | 8e90301bcc4fed4eaf537beb54151bf9dc6bca36c86e63c375cd4d0a9c353152 | 4f1fe9692bab016b | aa42b59fdfe66dfe |
| 59 | 36 | 435 | 3 | 22 | c4902fc412fee362e11bee596c25b5a348e96acefeaffa795c8b870f94eab7d8 | b2a0dce31f214ba3 | 0f41becccb7d57dc |
| 58 | 35 | 435 | 3 | 22 | bc45f562736329510d0df7e6e4cc542dd1e4a27f8dba86784d2bd4481c0440ac | 2afa8f625b3147e7 | 0150344a74549ded |
| 57 | 34 | 435 | 3 | 22 | f1bf230bcbe78f17ba5720008d0ea550104c9b6558a21c996ccd08232d180923 | 54c17488416209b8 | 659cdb7741354472 |
| 56 | 33 | 435 | 3 | 22 | a0b8f3e80881e28ad3ca0a8cba117a009a565a72a54e165629606413b346ebce | 21ed83fb4b8d30aa | fc911852d9f4c1db |
| 55 | 32 | 435 | 3 | 22 | 5e07d2233241fbfe48edad14f982e6d8a56de67c7c3fda4a1a7a253bdbb08abe | 0ea2ecea9e3796e9 | 2e3b0393c91866ce |
| 54 | 31 | 435 | 3 | 22 | 2c97fd80625692ebcbc1655f24e199cd2eedbd46edd7166944bf5a8709210e10 | 0ea404116c65c0f3 | e2beafc1fb0b24da |
| 53 | 30 | 435 | 3 | 22 | b316a6c826d5eb9a752a3db75e47a483edcbb71556609009142c56f691455513 | 48ec00a271653929 | 025d9d61bee79d66 |
| 52 | 29 | 435 | 3 | 22 | 2f0914fc78abc0ee22636531622c46c4cbb49493e8fc6686a5a1196d70468577 | 9563cebab2e34d31 | cb3eccb9a38f64fc |
| 51 | 28 | 435 | 3 | 22 | 1fa8a5e4dbc587ac52dec821f3bd095c5d05f7770f9325d2e73a39afb6234831 | 90a45ea9c417e4e3 | 409c8a6e2763066d |

Note (version 6; RV5 should-fix 1, 2): rows 85, 84 and 83 give the installed, v9-aware checker (PIN.json `gcert_sha256`). The checker before encoder version 9 (PIN.json `previous_gcert_sha256`: gcert85 4c7202f8ade07d56…, gcert84 00e11661e5472266…, gcert83 384a2e7c32a86281…; copies in `pre_v9/l<m>/code/`) is the one the earlier audit groups ran: by the `code_sha256` field of the CHECK_RESULTS lines, groups G1–G7 of layers 85 and 84 share one value and G8 (the v9 record) has another; groups G1–G7 of layer 83 share one value, and (version 7) its group G8, the v9 record, has the v9-aware checker's value 00a00b3c…. The old and new checkers differ only by the v9 pin and acceptance (12 changed lines each; RV5 diffed all three against `pre_v9/`).

Layers 80, 81, 82: 435 formulas each, of which 2, 2, 3 are closed by Corollary C22c-80 (a22c/LEMMA_C22c_EXEMPT.json)
and the rest by audited certificates; union files l80/audit/UNION_CHECK.txt, l81/…, l82/….
Layer 83 (version 5): 435 formulas, of which 2 are closed by Corollary C22c-83 (a22c/LEMMA_C22c_EXEMPT.json) and 433 by
audited certificates; union file l83/audit/UNION_CHECK.txt. Closure order unchanged: L83's certified formulas use
saturation and δ ≥ 4, so L83 closes only after L84–L87.
