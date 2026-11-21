# Review RC22c: Lemma E, Lemma C22c, Corollary C22c-80 and the L80-82 coverage plan (research/a22_close/)

Independent reviewer, 2026-11-17. I did not produce the package. Read-only outside this folder (research/a22_review2/).
All runs at nice 19, each under 20 minutes. The package was copied to `pkgcopy/` before re-running its scripts, so
the package folder was never written. Nothing was committed, pushed or dispatched.

**VERDICT: ACCEPT WITH FIXES.** I found no mathematical or computational error. Every load-bearing claim was either
re-derived by hand or re-computed with my own code. The fixes concern how the trust dependency is stated, and one
place where union_lemma.py is weaker than close_group.py. None of them changes a verdict on a formula.

Fixes (I count none as a soundness bug, but they should be made before install):
- **F1 (ledger wording, must-fix for the route's "dependencies kept explicit" standard).** McKay-max does not stay
  inside L80-82. Theorem L_m for every m ≤ 79 assumes the closure of layer m + 1, and so inherits McKay-max through
  L80. The final order-24 statement inherits it too. TRUST_ENTRY "Scope of use" ("used only ... for the 7 formulas")
  and the ledger line "Theorem L_m for m ∈ {80, 81, 82} gains the hypothesis McKay-max" are true for direct use only.
  They should say that every layer m ≤ 82 and the final theorem depend on McKay-max transitively, until the 7 tags get
  certificates. The closure-document template for L51-L79 should list it in [1] inherited.
- **F2 (union_lemma.py should be no weaker than close_group.py).** close_group requires every line of a group to pass,
  and the CHECK_RESULTS tag set to equal the records tag set. union_lemma accepts a tag if any one line passes, and
  only reports failing lines. My control: I appended a failing duplicate line for a passing tag to a copy of L80 G1.
  union_lemma still printed `OK layer 80`, exit 0. Fix: require `nonpass == []`, and per group
  `{tags in CR} == {tags in records}` with one line each, or require close_group's OK for each group.
- **F3 (should-fix).** The lemma pins in union_lemma.py are compared only as strings in EXEMPT.json. Nothing checks
  that the pinned files (witness file, 3 CNFs) exist with those hashes, or re-runs mx_witness_check / cake_lpr. Better:
  pin excB_gen.py and mx_witness_check.py too, and have the closure step (or union_lemma) hash the on-disk a22c/ files.
- **F4 (cosmetic).** The recorded out/run.log predates code/union_lemma.py. A re-run adds one hash line, so the
  run.log hash in EXCEPTION_CHECK.md cannot be reproduced byte-for-byte. Every CNF, lazy list, proof and witness file
  is byte-identical. The page quote in TRUST_ENTRY reads "on N [vertices]", where the page has McKay's typo "on N
  graphs". Mark the bracket as an editorial insertion.

## 1. Mathematics: Lemma E, Lemma C22c, Corollary C22c-80. HOLDS

Checked from the definitions in LOW_LAYERS_ROUTE.md v2 (Theorem L_m: the class is triangle-free, α ≤ 8, every 12-set
≥ 12 edges, e = m) and cegar90c.py "Setting".

- **What the 7 formulas must exclude.** (S, T) is a maximum cut with |S| = s ≤ |T|, |S| largest; (s, a, b, c) =
  (|S|, e(S), e(T), e(S, T)); G[S] ≅ catalogue H_h. Saturation, δ ≥ 4, lex, twins, swap etc. are extra necessary
  conditions. They only shrink the set a formula must exclude. So the set to exclude is contained in {class graphs with
  m edges and mc(G) = c}, for every h_index and every family. All 7 tags have c = m − 22. I checked the pinned
  subsets: tag fields consistent, a + b + c = m for all 435, and 8 formulas (10,4,18,m−22), h = 0000..0007, per layer.
  The β distribution per layer is 23: 328, 22: 101, 21: 5, 20: 1, so 429 formulas have c ≤ m − 22, as stated.
- **Lemma E.**
  - Step 1 (a maximal supergraph M′ exists): holds.
  - Step 2: β(G + e) ≥ β(G), because mc rises by at most 1. So β(M′) ≥ 17, and A22 gives β(M′) = 17. M′ is maximal
    triangle-free on 22 vertices, so McKay-max applies.
  - Step 3: the floor is monotone under adding edges and invariant under isomorphism. So M_L has the floor, and
    Check W leaves only L ∈ {142, 195, 302}.
  - Step 4: φ(H) is a spanning subgraph of M_L with the floor, and φ(A) is independent in φ(H) (not necessarily in
    M_L; the CNF correctly uses y_e ∧ x_i ∧ x_j). The X11 condition is exactly e_H(U) + |A ∩ U| ≥ 12. A lazy subset
    of the conditions is a relaxation, so UNSAT is sound.
  - α and Δ of H are indeed not used.
- **Lemma C22c (a).**
  - H = G − v − u is induced, so it is triangle-free and has the floor.
  - A = N_G(v) − {u} is independent.
  - For an 11-set U ⊆ V(H): e_G(U + v) = e_H(U) + |A ∩ U|, since u ∉ U.
  - β(H) ≤ 17 by A22. β(H) = 17 contradicts Lemma E, so β(H) ≤ 16.
  - Lemma V (l91/A23_ROUTE.md, proof read: valid for every graph), applied at v and then at u in G − v, gives
    ⌊d(v)/2⌋ + ⌊d_{G−v}(u)/2⌋ ≥ 6.
- **(b) and (c).**
  - Δ ≤ 8 because N(v) is independent and α ≤ 8.
  - d ≤ 3 needs d_{G−v}(u) ≥ 10. d ∈ {4, 5} needs d_{G−v}(u) ≥ 8 for every u, which fails at a neighbour (d(u) − 1 ≤ 7).
  - (c): (x, y) gives d(y) ≥ 7. If d(y) = 7, (y, x) gives 3 + 2 = 5.
  - All correct. The equivalence with family a22 is RA22 §5 / R91B. I did not re-check the a22 clauses: they are not
    used by the exemption, which needs only (b) and (c) as mathematics.
- **Corollary C22c-80.**
  - Σ(d − 7) = 2m − 168 = n8 − n6.
  - No two degree-6 vertices are adjacent, so the 6·n6 edges at degree-6 vertices are distinct, each with an
    endpoint of degree 8. So 6n6 ≤ 8n8.
  - m = 80: n8 ≥ 24, n6 ≥ 32. m = 81: n8 ≥ 18, n6 ≥ 24. m = 82: n8 ≥ 12, n6 ≥ 16, n6 + n8 ≥ 28. Each is > 24.
  - m = 83: 6 ≤ n8 ≤ 11 is feasible.
  - Arithmetic re-done by hand: correct. (The same count also kills every m ≤ 82, including m < 72 through
    2m ≥ 144. This is not needed.)
- **Coverage by the corollary.** Each class graph is assigned to the formula of its own chosen maximum cut. So "no
  class graph at m ∈ {80, 81, 82} has mc ≤ m − 22" empties every formula with c ≤ m − 22, whatever h is and whatever
  its other families are.

## 2. Form B and Check W, re-derived independently. HOLDS

- **Check W, my own code** (`code/my_checkW.py`: networkx graph6 decoder, exhaustive numpy minimum over all 646,646
  12-sets for each of the 338 graphs; `out_checkW.txt`):
  - all 338 graphs are triangle-free and maximal triangle-free;
  - 335 have a 12-set with ≤ 11 edges;
  - exactly lines 142 (78 edges, min 12), 195 (74, 12) and 302 (81, 13) pass the floor.
  - This matches the package's OPEN set and RA22. (RA22's prose lists the edge counts as "74, 78 and 81" in a
    different order from the lines; this is cosmetic.)
- **Independent Form B** (`code/my_formB.py`: own CEGAR over **all** 12-sets and **all** 11-sets, PySAT totalizer
  instead of Sinz, own variable numbering; `out_formB.txt`):
  - all 3 UNSAT: 142 after 6 iterations, 195 after 6, 302 after 5;
  - the final CNFs, solved by the pinned cadical and checked by `/root/tools/cake_lpr/cake_lpr` (29e02af7…):
    `s VERIFIED UNSAT`, exit 0, for my_B142, my_B195 and my_B302 (`out_formB_cake.txt`).
  - This needs neither the package's lazy lists nor its generator.
- **Byte rebuild** (`code/my_rebuildB.py`: own decoder, Sinz LTseq written from the paper). From the package's lazy
  lists I get CNFs byte-identical to cnf/B142.cnf (9dcc7db7…), B195.cnf (7510e867…) and B302.cnf (b8a93280…). Every
  lazy set has size 12 (F12) or 11 (X11). I also read excB_gen.py line by line:
  - the decoder uses the standard column order and checks padding;
  - y_e and x_i are numbered as documented;
  - (I) is exactly independence in H;
  - at_least(12) = at_most(n − 12) of the negations, which is Sinz's clauses exactly;
  - the K = 0 and K ≥ n cases are handled.
  - test_card.py: 8,192 cases, 0 mismatches.
- **cake_lpr on the package's own proofs**, in the original folder with the pinned binary: B142, B195, B302, A605,
  A607, A767, A1047 and A1051 each give stdout exactly `s VERIFIED UNSAT`, exit 0 (`out_cake_pkg.txt`).
- **Re-run of run_check.sh and controls.sh** (in pkgcopy/):
  - witnesses, lazy lists, CNFs and proofs are byte-identical to the package's;
  - controls.log is identical;
  - C1 (5/5 UNSAT at T = 11; 4 SAT and 1051 UNSAT at T = 10; all SAT at T = 9) agrees with RA22;
  - C2 is SAT for all 3;
  - C3: every tampered input is refused.
- **mx_witness_check.py, read line by line:**
  - pinned hash, 338 graphs, one witness per graph in order;
  - each F12 witness is 12 distinct in-range vertices with ≤ 11 edges;
  - OPEN must equal {142, 195, 302}, and the exit code depends on it;
  - indexing (0-based non-empty lines) matches excB_gen.
  - The finders cannot cause a false pass: a wrong witness is rejected by the checker, and a wrong lazy list only
    weakens the CNF.

## 3. Trust entry. HOLDS (wording fix F1)

- **Hashes.**
  - data/minbip.tar and research/ext_dl/minbip_dl/minbip.tar: 0424c19d…7215;
  - tar member minbip22_17.g6: 67b6e19e…bfe4 (13,858 bytes, bdm/staff, 2025-10-11 22:30);
  - x member: 4458639b…39b7;
  - page snapshot: 0da08183…9d29fa;
  - all as stated.
- **The page** has the "this tar file" link `minbip.tar`, and the wording: "x.g6 contains all the triangle-free
  graphs on N graphs which achieve a(N)=A … (without the "x") has the subset of those which are maximal
  triangle-free". The OEIS snapshot (oeis/a389646.txt) links https://users.cecs.anu.edu.au/~bdm/data/graphs.html.
- **The statement is exactly what Lemma E step 2 uses:** completeness up to isomorphism, for maximal triangle-free,
  n = 22, β = 17. Nothing about the listed graphs is used, since Check W and Check B treat each line as an arbitrary
  graph.
- **Consistency evidence** (code/my_consist.py, out_consist.txt): see the addendum at the end. The x file's maximal
  members versus the maximal file, and whether the maximal completion of every x-file graph lies in the maximal file.
- **The "same computation" argument** is fairly labelled as an inference. McKay-max is strictly stronger than A22.
  It is also implied by x-file completeness together with a correct maximality filter.

## 4. Coverage plan. HOLDS (fix F2, should-fix F3)

- **My own re-read** (`code/my_union.py`), every group's run_G*/CHECK_RESULTS against audit/G*/records.jsonl with
  close_group's conditions plus the full formulas hash:
  - L80: 433 pass, missing exactly L80_s10a4b18c58_0000/_0001;
  - L81: 433 pass, missing L81_…c59_0000/_0001;
  - L82: 432 pass, missing L82_…c60_0000/_0001/_0002.
  - No failing lines, no tag in two groups, no record without a passing line.
  - The 7 missing tags have no record at all.
- **union_lemma.py dry runs** with my own output paths: OK for all three layers, exit 0, output identical to the
  package's out/UNION_DRYRUN_L8x.txt.
- **What union_lemma.py checks.**
  - The exempt check reads c from the pinned formulas file (hash checked against PIN.json) and requires
    m ∈ {80, 81, 82} and c ≤ m − 22.
  - The lemma pins are hard-coded.
  - The per-line conditions equal close_group's, with the formulas hash compared in full rather than by prefix.
- **Controls.**
  - Package controls: short list NOT OK (exit 1); c = m − 21 exemption NOT OK; wrong pins AssertionError.
  - Mine: layer-81 tags listed under "80" NOT OK. An extra c = m − 21 tag NOT OK. An L83 exemption is reported invalid
    (m ∉ {80, 81, 82}). A proof-hash mismatch, an encoder v6 (in both the line and the record), a CR line without a
    record, and a missing CR line are each NOT OK.
  - Duplicates in the exemption list, and an exempt tag that is also certified, are accepted. Both are sound.
  - **Gap:** an extra failing line for a passing tag is accepted (F2).
  - The glob `run_G*` ignores the neg/ and gha/ CHECK_RESULTS, which is correct.

## 5. Uncertain points and things not addressed

- **Order of closure.** It is correctly kept. The corollary needs no other layer, but the 433/433/432 certified
  formulas carry saturation (layer m + 1 closed) and δ ≥ 4 (Theorem B). So L82 still waits for L83, and so on.
- **Transitive trust (F1).** This is the one real omission. Layers 51-79 and the final result inherit McKay-max.
- **Exemption scope.** Naming only the 7 tags (rather than all 429) is the right choice. It keeps McKay-max out of
  every formula that already has a certificate, and it can shrink later.
- **Options.** Option C, leaving gcert80-82, close_group.py, PIN.json and the subsets unchanged, is sound and
  sufficient, given F2. The 6 formulas with c ≥ m − 21 per layer keep their certificates, as they must.
- **L83-85 encoder gating.** It is correctly left as a separate change.
- **Trusted computing base.** Python, the libc and cake_lpr remain trusted as for gcert. Both my generator and the
  package's are Python, which is independent code but not an independent interpreter.

## Could not check

- McKay-max itself (completeness, about 143 CPU-h).
- The live URL. I used the saved snapshots and made no network fetch.
- The R91B equivalence of family a22 with (b) and (c). The exemption does not rely on it.

## Addendum: McKay file consistency (code/my_consist.py, out_consist.txt; networkx vf2pp isomorphism)

- The x file has exactly 338 maximal triangle-free members. They match the 338 maximal-file graphs one-to-one up to
  isomorphism, and the maximal file has no isomorphic duplicates.
- For every one of the 1,076 x-file graphs, a greedy maximal triangle-free completion is isomorphic to a graph of the
  maximal file. A22 together with x-file completeness requires this.
- So the two files are mutually consistent, and McKay-max is equivalent to "the x file is complete, and its
  maximality filter is correct". This is consistency only; it does not prove completeness.

## Files here

- code/: my_checkW.py, my_formB.py, my_rebuildB.py, my_union.py, my_consist.py
- outputs: out_checkW.txt, out_formB.txt, out_formB_cake.txt, out_rebuild.txt, out_cake_pkg.txt, out_consist.txt,
  union/L8x.txt
- re-run copy: pkgcopy/
- the original logs, kept for diffing: orig_out/
- my union controls: t80/, ex_*.json
