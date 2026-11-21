# The case α = 9 of Erdős #128 at order 24: mathematics behind the computation

Status of this note: every numbered statement is labelled PROVED (proof written here) or ASSUMED (taken from outside).
Nothing here is an approval. The computation (section 7) is a separate object; this note only shows that, IF every
cube formula is unsatisfiable, THEN the graphs described in section 1 do not exist.

## 1. Statement and reductions

𝔽 = the set of triangle-free graphs G on 24 vertices in which every 12-vertex set spans at least 12 edges.

**Target (T).** There is no G ∈ 𝔽 that is edge-maximal triangle-free and has α(G) = 9.

**(A0) ASSUMED (external, the project's chain).** No G ∈ 𝔽 has α(G) ≤ 8. (It must cover every edge count; it is
applied below to an edge-maximal graph.)

**(R1) PROVED. α(G) ≤ 9 for G ∈ 𝔽.** Let I be independent. |I| ≥ 12: a 12-subset of I spans 0 edges. |I| = 11: for
x ∉ I the 12-set I + x spans d_I(x) ≤ 11 edges. |I| = 10: if x, y ∉ I were adjacent, N_I(x) ∩ N_I(y) = ∅ (no
triangle), so I + x + y spans d_I(x) + d_I(y) + 1 ≤ 11 edges; hence the 14 vertices outside I are pairwise
non-adjacent and 12 of them span 0 edges. ∎

**(R2) PROVED given (A0). (T) implies 𝔽 = ∅.** Let G ∈ 𝔽. Add edges one at a time as long as no triangle appears;
the process stops at an edge-maximal triangle-free G* ⊇ G on the same vertices. Adding edges cannot lower the number
of edges in a 12-set, so G* ∈ 𝔽, and α(G*) ≤ 9 by (R1) applied to G*. By (A0), α(G*) = 9, contradicting (T). ∎
In an edge-maximal triangle-free graph every two non-adjacent vertices have a common neighbour (otherwise the edge
could be added). This is used as **(MAX)**.

**(R3) PROVED. Two cases.** Let G be as in (T). Every neighbourhood is independent, so Δ(G) ≤ 9.
* Case A: some vertex v has degree 9. Put I = N(v): an independent 9-set; v is adjacent to all of I.
* Case B: Δ(G) ≤ 8. Let I be any independent 9-set.
The cases are exhaustive (they need not be made disjoint in the formulas; they are, by definition).

## 2. Notation and basic facts (G as in (T), I as in (R3))

O = V ∖ I (15 vertices). For x ∈ O: N_I(x) = N(x) ∩ I (its "mask"), a_x = |N_I(x)|, d_O(x) = |N(x) ∩ O|.
D = 8 in Case B and D = 9 in Case A; every vertex has degree ≤ D (PROVED: (R3)).
"body" = O in Case B, O ∖ {v} in Case A.

* **(F1) PROVED.** If x, y ∈ O are adjacent then N_I(x) ∩ N_I(y) = ∅ (no triangle); so a_x + a_y ≤ 9.
* **(F2) PROVED.** For every triple X ⊆ O: e(X) + Σ_{x∈X} a_x ≥ 12 (the 12-set I ∪ X; I is independent), and
  e(X) ≤ 2 (no triangle).
* **(F3) PROVED.** a_x ≥ 1 for x ∈ O (else I + x is an independent 10-set).
* **(F4) PROVED.** N(i) ⊆ O for i ∈ I.
* **(F5) PROVED.** Each i ∈ I has at most 8 neighbours in the body (Case B: Δ ≤ 8; Case A: deg(i) ≤ 9 and v is a
  neighbour). Hence C := Σ_{x ∈ body} a_x ≤ 72.

## 3. Structural lemmas (all PROVED here; H = {x ∈ O : a_x ≥ 5}, L = O ∖ H, ℓ = |L|)

**(S1)** H is independent and |H| ≤ 9, so ℓ ≥ 6.
Proof. Two adjacent vertices of H would have a_x + a_y ≥ 10, against (F1). α = 9. ∎

**(S2)** a_x ≥ 2 for all x ∈ O.
Proof. Suppose a_x ≤ 1; then a_x = 1 by (F3) and x ∈ L. Pick y, z ∈ L ∖ {x} (ℓ ≥ 6). (F2): e({x,y,z}) ≥ 12 − 1 − 4 − 4
= 3, a triangle. ∎

**(S3)** At most two vertices have a ≤ 3; at most one has a = 2; if some a_y = 2 then every other vertex of L has
a = 4.
Proof. Three vertices with a ≤ 3: (F2) gives e ≥ 3, a triangle. If a_y = 2 and a_z ≤ 3 (z ≠ y), pick w ∈ L ∖ {y,z}:
e({y,z,w}) ≥ 12 − 2 − 3 − 4 = 3, a triangle. ∎

**(S4)** a_x ≠ 8.
Proof. Let N_I(x) = I ∖ {i}. x and i are non-adjacent, so by (MAX) they have a common neighbour y; y ∈ O by (F4);
y ~ x gives N_I(y) ⊆ {i} by (F1), so a_y ≤ 1, against (S2). ∎
Consequently a_x ∈ {2,…,7} in Case B (a_x ≤ 8 = Δ) and a_x ∈ {2,…,7, 9} in Case A.

**(S5)** If a_x = 7, with I ∖ N_I(x) = {i, j}: x has exactly one neighbour y in O, and N_I(y) = {i, j} (so a_y = 2).
Proof. Every neighbour y ∈ O of x has N_I(y) ⊆ {i,j} (F1), hence a_y = 2 and N_I(y) = {i,j} by (S2). A neighbour
exists by (MAX) for the pair x, i and (F4). There is at most one vertex with a = 2 (S3). ∎

**(S6)** If a_x = 6, with T = I ∖ N_I(x): x has a neighbour y ∈ O with N_I(y) = T (so a_y = 3).
Proof. Every neighbour of x in O has its mask inside T (F1), of size 2 or 3 (S2). For each i ∈ T, (MAX) and (F4) give
a neighbour y_i of x in O with i ∈ N_I(y_i). If none of the y_i has mask T, all of them have a = 2; by (S3) they are
one and the same vertex, whose 2-element mask would contain the three elements of T. ∎

**(S7)** If a_y = 2: at most one vertex of L ∖ {y} is non-adjacent to y; so y has at least ℓ − 2 neighbours in L.
Proof. For z ≠ z' in L ∖ {y}, a_z = a_z' = 4 (S3), so e({y,z,z'}) ≥ 2 (F2). If both were non-adjacent to y, e ≤ 1. ∎

**(S8)** If a_z = 3: at most two vertices of L ∖ {z} are non-adjacent to z; so z has at least ℓ − 3 neighbours in L.
Proof. For y ≠ y' in L ∖ {z}: e({z,y,y'}) ≥ 12 − 3 − 4 − 4 = 1. If y1, y2, y3 ∈ L ∖ {z} were all non-adjacent to z,
each pair of them would have to be adjacent: a triangle. ∎

**(S9)** If a_z = a_z' = 3 (z ≠ z'): z ≁ z', and every vertex of L ∖ {z,z'} is adjacent to both.
Proof. For y ∈ L ∖ {z,z'} (a_y = 4 by (S3)... precisely a_y ≤ 4 and not ≤ 3, by (S3)): e({z,z',y}) ≥ 12 − 3 − 3 − 4 = 2.
Suppose z ~ z'. Then each such y is adjacent to exactly one of z, z' (at least one by the count, not both: triangle).
There are ℓ − 2 ≥ 4 such y, so two of them, y1, y2, are adjacent to the same one, say z. Then y1 ≁ y2 (common
neighbour z), and y1, y2 ≁ z', so e({z',y1,y2}) = 0 < 12 − 3 − 4 − 4 = 1, against (F2). Hence z ≁ z', and e ≥ 2 forces
y ~ z and y ~ z'. ∎

## 4. Admissible profiles

The profile of (G, I) is the sorted tuple (a_x)_{x∈O} (15 numbers; in Case A the last one is a_v = 9). Notation:
n_k = number of entries equal to k; ℓ = n_2 + n_3 + n_4.

Filters (each PROVED; `a9core.profile_ok`):
* (P1) entries in {2,…,7} (Case B); in {2,…,7,9} with the last entry 9 (Case A). [(S2), (S4), Δ ≤ D]
* (P2) #{entries ≥ 5} ≤ 9 (v counted). [(S1)]
* (P3) sum over the body ≤ 72. [(F5)]
* (P4) n_2 ≤ 1; n_2 + n_3 ≤ 2; n_2 = 1 ⇒ n_3 = 0. [(S3)]
* (P5) n_7 > 0 ⇒ n_2 = 1; n_6 > 0 ⇒ n_3 ≥ 1. [(S5), (S6), with (S3)]
* (P7) degree of a low vertex:
  - n_2 = 1: ℓ − 2 + n_7 ≤ D − 2. Proof: let a_y = 2. y has ≥ ℓ − 2 neighbours in L (S7); every vertex with a = 7 is
    adjacent to its unique neighbour with a = 2, which is y (S5, S3); these are in H, disjoint from L.
    deg(y) = 2 + d_O(y) ≤ D. ∎
  - n_3 = 1 (then n_2 = 0 by (P4)): ℓ − 3 + n_6 ≤ D − 3. Proof: let a_z = 3. d_L(z) ≥ ℓ − 3 (S8); every vertex with
    a = 6 has a neighbour with a = 3 (S6), which is z. deg(z) = 3 + d_O(z) ≤ D. ∎
  - n_3 = 2: ℓ − 2 + ⌈n_6/2⌉ ≤ D − 3. Proof: z, z' are each adjacent to the ℓ − 2 other vertices of L (S9); every
    vertex with a = 6 is adjacent to z or z' (S6), so one of them has ≥ ⌈n_6/2⌉ such neighbours. ∎
* (P8) n_7 > 0 ⇒ 7 n_7 + Σ_{x ∈ body, a_x ≠ 7} (a_x − 2) ≤ 56. Proof: let a_y = 2 and M = I ∖ N_I(y) (7 vertices).
  Every vertex with a = 7 has mask M (S5). The vertices of M have together at most 7·8 = 56 neighbours in the body
  (F5), counted with multiplicity. A vertex with a = 7 contributes 7; any other body vertex x contributes
  |N_I(x) ∩ M| ≥ a_x − 2 (y contributes 0 = a_y − 2). ∎

**Counts (`python3 enum_profiles.py`, list version 2).**
* (P1)–(P5) ("weak"): 141 in Case B, 325 in Case A.
* (P1)–(P8): 26 in Case B, 110 in Case A (list version 1; the second ChatGPT review recounted the same 26 / 110 and
  reports that (P8) removes nothing after (P7)).
* (P1)–(P12) ("strong", section 4a): **16 in Case B, 84 in Case A**; identical in content and order to RA9X's
  surviving lists (`index_map.py` checks this against review_RA9X/profiles_out.txt).

**Certified list (version 2) = strong (P1)–(P12) profiles, then the "weak extras" = profiles passing (P1)–(P5) but
failing (P7) or (P8): 16 + 115 = 131 in Case B, 84 + 215 = 299 in Case A, 430 in all.**
sha256(json.dumps(list)) — strong B ab4d10d06bfdd37a5a53f609697349deb18f0dcb672928d71f2718ded3935757,
strong A 3dabdaf62ac5b0402850ef8794a2fb8ea9ea11b1ad732b5a24abb653d18e793f, certified B
56259beb2e5cb494b958f40a0531c663b116c22e6c366a6c649053c07ad5fa31, certified A
bfc030dfe85703f995dfee908b1e61ef502a90c8737068686fbe61c0db690c68 (python's json.dumps of a list of tuples).
Version-1 lists (26+115, 110+215) are in archive_v1/; index_map_v1_v2.json maps version-1 to version-2 indices.

**Why this list covers every case (PROVED).** Let p be the profile of G. By (P1)–(P5) p passes the weak filters. If p
fails (P7) or (P8), p is a weak extra. Otherwise p passes (P1)–(P8); then by section 4a p passes (P9)–(P12), so p is
strong. Note that this argument never uses that (P7) or (P8) are TRUE: they only route p to one of the two parts.
Every weak extra is refuted by the base formula alone (no lazy item; all 330 in under 5 s in total).
**Dependencies of the certified result in sections 3–4a:** (F1)–(F5), (S1)–(S6) (for (P1)–(P5)); and for (P9)–(P12):
Lemma J (S1–S3 relative to any independent 9-set), (S5), (S7), (S8), (S9) (relative to I), (MAX) (in (P10)), and
the 11-vertex lemma (L11) (in (P11)). Not used for coverage: the truth of (P7), (P8).

**Comparison with the review's 89 / 364.** I did not tune anything towards these numbers. Re-implementing the Case B
filters as the review summary states them (60 ≤ C ≤ 72, |H| ≤ 9, (B5)–(B8), a = 7 ⇒ some a = 2, a = 6 ⇒ some a ≤ 3,
132 a_x + 25 C ≥ 1872; `review_filters.py`) gives **116**, not 89: so the review used something its summary does not
state, or I read a filter differently; I cannot resolve this without its enumerator (not downloaded). Adding my (S6)
(a = 6 ⇒ some a = 3 exactly) gives 79; adding (P7) gives exactly my 26. In every variant my strong list of 26 is a subset of the
review-filter list. The certified weak list (141) contains all 116 − (those violating (P4)/(P5) as I state them);
whether it contains the review's 89 cannot be checked without its list. Case A was not compared (the review's Case A filters are not stated in enough detail).

**Review items.** Re-proved and used: a ∈ {2..7}/{2..7,9}; C ≤ 72; the saturation identity
∪_{y∈N_O(x)} N_I(y) = I ∖ N_I(x) (⊆ is (F1), ⊇ is (MAX)+(F4); it is clause family (C9)); a = 7 ⇒ unique outside
neighbour, a = 2, complementary mask (S5); the low-incidence structure (S3, S7–S9); the triple rule (sum 10 ⇒ exactly
two edges, sum 11 ⇒ at least one: immediate from (F2) and e(X) ≤ 2; clause family (C7)). Not used and not re-proved
here: h ≥ 20, C ≥ 56/60 as separate statements, (A5), (A7), (A8), (B2), (B3), (B15)/(B16)/(A11), the literature
statements. **I found no error in the review items I re-proved.** One of them is weaker than what is true ((S6)).

## 4a. Profile exclusions from a second independent 9-set (P9)–(P12)

Source: the second ChatGPT review of this note (closure_drafts/reviews/XGPT_A9_MATH.md, sections 3.3, 3.4, 4),
accepted by the independent reviewer RA9X (review_RA9X/REPORT.md: proofs checked, the 11-vertex lemma checked
exhaustively on all 30,395 triangle-free graphs with α ≤ 5 on 11 vertices and by SAT; two wording fixes, applied
below). Proofs written out here in my words; each is applied only to profiles that pass (P1)–(P8).

**Lemma J (PROVED).** Let J be any independent 9-set of G (G as in (T); only triangle-freeness, α(G) = 9 and the
12-set condition are used — no (MAX), no degree bound). For x ∉ J write b_x = |N_J(x)|, H_J = {x ∉ J : b_x ≥ 5},
L_J = the other 15 − |H_J| vertices outside J. Then:
(F1_J) adjacent x, y ∉ J have disjoint J-neighbourhoods, so b_x + b_y ≤ 9; (F2_J) every triple X outside J has
e(X) + Σ b_x ≥ 12; (S1_J) H_J is independent, so |H_J| ≤ 9 and |L_J| ≥ 6; (S2_J) b_x ≥ 2 for all x ∉ J;
(S3_J) at most two vertices outside J have b ≤ 3, at most one has b = 2, and if some b_y = 2 then every other
vertex of L_J has b = 4.
Proof. Word for word the proofs of (F1), (F2), (S1), (S2), (S3) with I replaced by J; (F3)_J (b_x ≥ 1) holds since
J + x would be an independent 10-set. Those proofs use only these facts and |L_J| ≥ 3. ∎

Notation below: H, L, n_k as in section 4 (relative to I), D = 8 (Case B) or 9 (Case A). If |H| = 9 then H is an
independent 9-set (S1), and Lemma J applies to J = H; then b_x = d_H(x).

**(P9) Case B: |H| = 9 ⇒ n_2 = 0 and n_3 = 0 (PROVED; review 3.4).** Let |H| = 9, so |L| = 6.
* n_2 = 1, a_y = 2: the other 5 vertices of L have a = 4 (S3), and y is adjacent to at least 4 of them (S7). Such a
  z has deg(z) ≤ 8, 4 neighbours in I and the neighbour y ∉ H, so d_H(z) ≤ 3. Four vertices outside H with ≤ 3
  neighbours in H contradict (S3_H).
* n_3 = 1 (then n_2 = 0 by (P4)), a_z = 3: the other 5 vertices of L have a = 4; z is adjacent to at least 3 of them
  (S8); each has d_H ≤ 8 − 4 − 1 = 3: three such vertices contradict (S3_H).
* n_3 = 2, a_z = a_z' = 3: the other 4 vertices of L have a = 4 and are adjacent to both z and z' (S9); each has
  d_H ≤ 8 − 4 − 2 = 2: four such vertices contradict (S3_H). ∎

**(P10) Case B: the profile 4^6 5^9 is impossible (PROVED; review 3.3).** Here H = the nine a = 5 vertices, L = the
six a = 4 vertices, |H| = 9.
(a) For x ∈ L, h ∈ H: x ~ h iff N_I(x) and N_I(h) are complementary. "⇒" is (F1) (4 + 5 = 9). "⇐": if they are
complementary and x ≁ h, (MAX) gives a common neighbour w; w ∉ I (the masks are disjoint), so w ∈ O and its mask is
disjoint from both, i.e. empty, against (S2).
(b) Types. For a 5-subset A of I let c_A = #{h ∈ H : N_I(h) = A} and l_A = #{x ∈ L : N_I(x) = I ∖ A}. So Σ c_A = 9,
Σ l_A = 6, and by (a) an L-vertex of type A has exactly c_A neighbours in H and an H-vertex of type A has exactly
l_A neighbours in L, hence in O (H is independent).
H side (MAX + F4): if c_A ≥ 1, take h of type A and i ∈ I ∖ A; h ≁ i, so they have a common neighbour w, which lies in
O (F4); w ~ h forces N_I(w) ⊆ I ∖ A (F1), so a_w ≤ 4, w ∈ L, a_w = 4 and N_I(w) = I ∖ A: l_A ≥ 1.
L side (S2_H): an L-vertex of type A has d_H = c_A ≥ 2. So the types that occur in H and in L are the same, and on
them c_A ≥ 2 and l_A ≥ 1.
Degree caps (D = 8): an H-vertex of type A has degree 5 + l_A ≤ 8, so l_A ≤ 3; an L-vertex of type A has degree
≥ 4 + c_A, so c_A ≤ 4.
(S3_H): the L-vertices with d_H ≤ 3 are those of types with c_A ≤ 3: Σ_{c_A ≤ 3} l_A ≤ 2.
The partitions of 9 into parts in {2, 3, 4} are (4,3,2), (3,3,3), (3,2,2,2). For the last two every part is ≤ 3,
so Σ l_A = 6 ≤ 2: impossible. For (4,3,2): the 3- and 2-types have l ≥ 1 each and together ≤ 2, so both are 1 and the
4-type has l = 6 − 2 = 4 > 3: impossible. ∎

**Lemma L11 (PROVED; review A1).** Every triangle-free graph F on 11 vertices with α(F) ≤ 5 has 8 vertices spanning
at most 11 edges.
Proof. Δ(F) ≤ 5 (neighbourhoods are independent). F is not bipartite (a side would have ≥ 6 vertices). Let C be a
shortest odd cycle, of length r ∈ {5, 7, 9, 11}; C has no chord (a chord would close a shorter odd cycle). A vertex
outside C has an independent set of C as its C-neighbourhood, so at most ⌊r/2⌋ neighbours on C; the 11 − r outside
vertices span at most ⌊(11 − r)²/4⌋ edges (Mantel). So e(F) ≤ r + (11 − r)⌊r/2⌋ + ⌊(11 − r)²/4⌋ = 26, 23, 18, 11 for
r = 5, 7, 9, 11; e(F) ≤ 26.
A fixed edge lies in a fraction C(9,6)/C(11,8) = 84/165 = 28/55 of the 8-subsets. If e(F) ≤ 23 the average 8-set
has ≤ 23·28/55 < 12 edges: done. Let e ∈ {24, 25, 26} and t = number of degree-5 vertices. The deficits 5 − d(x) sum
to 55 − 2e and are ≥ 1 off the degree-5 vertices, so t ≥ 11 − (55 − 2e): t ≥ 8, 6, 4 for e = 26, 25, 24.
If the degree-5 vertices contain an independent triple T (always if t ≥ 6, since R(3,3) = 6 and F is
triangle-free), F − T has 8 vertices and e − 15 ≤ 11 edges. Remaining case: e = 24, t ∈ {4, 5}, and the degree-5
vertices contain no independent triple, hence an edge uv. Deficits sum to 7: for t = 4 the 7 other vertices all
have degree 4; for t = 5 the 6 others have degrees 4,4,4,4,4,3. N(u) is an independent 5-set containing v; among
N(u) ∖ {v} at most one vertex has degree < 4, so it has two vertices w1, w2 of degree ≥ 4. {v, w1, w2} is
independent, so deleting it removes 5 + d(w1) + d(w2) ≥ 13 edges: 8 vertices with ≤ 11 edges. ∎

**(P11) Case A: n_9 ≤ 3 (PROVED; review A1).** A vertex z with a_z = 9 has no neighbour in O (its O-neighbours would
have empty masks by (F1), against (S2)). Suppose Z is a set of 4 vertices with a = 9 and let F = G[O ∖ Z]
(11 vertices, triangle-free). α(F) ≤ 5: an independent 6-set of F together with Z is independent in G (Z has no
neighbours in O), of size 10. By L11 some 8-set Y ⊆ O ∖ Z has e(Y) ≤ 11; then the 12-set Y ∪ Z spans
e(Y) + e(Y, Z) + e(Z) = e(Y) ≤ 11 edges, against the 12-set condition. ∎

**(P12a) Case A: |H| = 9 ⇒ n_3 ≠ 2 (PROVED; review A2).** If n_3 = 2 (a_z = a_z' = 3), the other 4 vertices of L
have a = 4 (S3) and are adjacent to z and z' (S9); each has degree ≤ 9, so d_H ≤ 9 − 4 − 2 = 3. Four vertices outside
H with ≤ 3 neighbours in H contradict (S3_H). ∎

**(P12b) Case A: |H| = 9 and n_2 = 1 ⇒ n_9 = 1 and n_7 ≤ 2 (PROVED; review A3).** Let a_y = 2 and W = L ∖ {y};
|W| = 5 and every w ∈ W has a = 4 (S3).
(i) y is adjacent to all of W. Otherwise y ≁ w for some w ∈ W; by (S7) y is adjacent to the other 4 vertices z of W.
For each such z the triple {y, z, w} has incidence sum 10, so it spans ≥ 2 edges (F2): yz and zw. Then z has the
two outside neighbours y, w ∉ H, so d_H(z) ≤ 9 − 4 − 2 = 3: four such z contradict (S3_H).
(ii) W is independent (all in N(y)). d_H(y) ≥ 2 by (S2_H), and deg(y) = 2 + 5 + d_H(y) ≤ 9, so A := N_H(y) has
exactly 2 vertices; A is independent (A ⊆ H).
(iii) Let Z = the k = n_9 ≥ 1 vertices with a = 9 (v among them); they have no neighbour in O (see (P11)), so
Z ∩ A = ∅ and there are no edges between Z and W ∪ A; no edges between W and A (all in N(y), triangle-free). So
W ∪ A ∪ Z is independent, of size 7 + k ≤ 9: k ≤ 2.
(iv) k = 2: J = W ∪ A ∪ Z is an independent 9-set. Let N_I(y) = {i, j}. i and j are adjacent to y, hence not to
any vertex of W ∪ A (triangles), and adjacent to both vertices of Z (masks = I). So |N_J(i)| = |N_J(j)| = 2: two
vertices outside J with b = 2, against (S3_J). Hence k = 1.
(v) Every vertex with a = 7 is adjacent to the unique vertex with a = 2, i.e. y (S5), and lies in H; so n_7 ≤ |A| = 2. ∎

Predicates as implemented (`a9core.profile_ok`, level 12, applied after (P1)–(P8)): Case B: exclude if
|H| = 9 and (n_2 = 1 or n_3 ≥ 1) [(P9); n_2 = 1 and n_3 ≥ 1 cannot both hold by (P4)], or p = 4^6 5^9 [(P10)].
Case A: exclude if n_9 ≥ 4 [(P11)]; if |H| = 9 and n_3 = 2 [(P12a)]; if |H| = 9, n_2 = 1 and (n_9 ≥ 2 or n_7 ≥ 3)
[(P12b)]. Here |H| = #entries ≥ 5 (v counted). Excluded version-1 indices: B 3,4,5,7,8,9,13,14,15,25; A 3,10,32,58,93,97
(P11), 42–54 (P12a), 21,23–28 (P12b). Finished UNSAT certificates of these profiles are kept as extra evidence
(a9check reports and checks them; they are not needed for coverage).

## 4b. Further exclusions (ChatGPT round 3, accepted by RA9X2)

Source: ChatGPT round 3 (gpt/round3_raw.txt), accepted with changes by RA9X2 (review_RA9X2/REPORT.md: no mathematical
errors; four write-up requirements, all applied here: Lemma S4_J with proof, Theorem 1 stated for every G with its
dependencies and cited where used, the hypothesis k ≥ 12 − h in 4b.9, the wording of 4b.7). Proofs in my own words.
**Status: reporting only.** These results define the "level 16" list (Case B 10, Case A 81; `profile_ok(level=16)`,
`level16.py`). The certified list (section 4, version 2: 131 + 299), the CNF and the production run are unchanged; a
certificate for a superset of profiles stays valid. Profile numbers "B k" / "A k" below are version-1 indices
(archive_v1/), and every profile is also written as a tuple.

**4b.1 Lemma S4_J (PROVED).** Let J be any independent 9-set of G (G as in (T)) and x ∉ J. Then |N_J(x)| ≠ 8.
Proof. Suppose N_J(x) = J ∖ {j}. Then x ≁ j, so by (MAX) x and j have a common neighbour w. w ∉ J (J is independent
and w ~ j). Since w ~ x, (F1_J) gives N_J(w) ∩ N_J(x) = ∅, so N_J(w) ⊆ {j} and |N_J(w)| ≤ 1, against (S2_J). ∎
Use in Case B: a vertex i ∈ I with |N_J(i)| ≥ 8 for some independent 9-set J ⊆ O has |N_J(i)| = 8 (deg(i) ≤ 8),
contradicting S4_J.

**4b.2 Theorem 1, exact disjointness (PROVED; every G as in (T), Cases A and B).** For x, y ∈ O:
x ~ y ⇔ N_I(x) ∩ N_I(y) = ∅. Dependencies: (MAX), (F1), (S2), (S3). (F4) is not needed: the common neighbour z cannot lie in I
because it would belong to both masks.
Proof. "⇒" is (F1). "⇐": let the masks be disjoint and suppose x ≁ y. By (MAX) they have a common neighbour z; z ∉ I
(it would lie in both masks), so z ∈ O, and by (F1) N_I(z) is disjoint from both masks. Hence
a_x + a_y + a_z ≤ 9 with all three ≥ 2 (S2). Sort the three values s1 ≤ s2 ≤ s3. If s1 = 2, then by (S3) every
other vertex with a ≤ 4 has a = 4, so s2, s3 ≥ 4 and the sum is ≥ 10. If s1 ≥ 3, the sum ≤ 9 forces s1 = s2 = s3 = 3:
three vertices with a ≤ 3, against (S3). ∎
(Consequence noted by the review: the 105 outside-edge variables are determined by the masks. Not used in the CNF.)

**4b.3 Case B, profiles B0 = (2,4^7,5^7) and B2 = (2,4^6,5^7,7) are impossible (PROVED; review 2.1).** Let y be the
a = 2 vertex; all other vertices of L have a = 4 (S3). deg(y) ≤ 8, so d_O(y) ≤ 6.
* B0: h = 7, ℓ = 8. By (S7) y is adjacent to at least 6 of the seven a = 4 vertices, so to exactly 6 of them and to
  nothing else in O. Let w be the a = 4 vertex with y ≁ w and Z the six others. For z ∈ Z the triple {y, z, w} has
  incidence sum 10, so it spans ≥ 2 edges (F2); as y ≁ w, both yz and zw are edges. So z has two neighbours in L and
  d_H(z) ≤ 8 − 4 − 2 = 2. Z is independent (common neighbour y), H is independent (S1). Five vertices of Z together
  with H form a 12-set with at most 5·2 = 10 edges: contradiction.
* B2: h = 8 (the a = 7 vertex is in H), ℓ = 7. The a = 7 vertex is adjacent to y (S5), so y has at most 5 neighbours in
  L, and at least 5 by (S7): exactly 5, with one non-neighbour w among the a = 4 vertices. As before each of the five
  neighbours z ∈ Z is adjacent to w and has d_H(z) ≤ 2; four of them with H form a 12-set with ≤ 8 edges. ∎

**4b.4 Case B, profile B1 = (2,4^6,5^8) is impossible (PROVED; review 2.2; uses Theorem 1 and S4_J).** h = 8, ℓ = 7;
y the a = 2 vertex, W the six a = 4 vertices, T = N_I(y), |T| = 2. By (S7) y has ≥ 5 neighbours in W. If exactly 5,
the argument of 4b.3 (B2) gives a 12-set with ≤ 8 edges. So y ~ every vertex of W, and d_O(y) ≤ 6 leaves no
neighbour in H. Then J = H ∪ {y} is an independent 9-set. W is independent, and every w ∈ W has a mask disjoint
from T (F1). Any four vertices of W with H form a 12-set whose edges are the H–W edges among them; each w has
d_H(w) ≤ 8 − 4 − 1 = 3, so each has exactly 3 (every w lies in such a four-set).
By Theorem 1 an a = 5 vertex and an a = 4 vertex are adjacent iff their masks are complementary. Group W by mask:
a type B occurring l_B times needs 3 vertices of H with mask I ∖ B, each adjacent to all l_B vertices of the type;
d_O(h) ≤ 3 gives l_B ≤ 3, so W uses at least 2 types, and these need at least 6 distinct vertices of H, all with
masks I ∖ B ⊇ T. The other (at most two) vertices of H are not adjacent to y, so by Theorem 1 their masks meet T.
Counting incidences between T and H: at least 6·2 + 2·1 = 14, so some i ∈ T has ≥ 7 neighbours in H, and i ~ y:
|N_J(i)| ≥ 8, against 4b.1. ∎

**4b.5 Case B, two vertices with a = 3 and h ≥ 7 is impossible; in particular B6 = (3,3,4^5,5^8) (PROVED; review
2.3).** Let z, z' have a = 3; by (S3) the other ℓ − 2 = 13 − h vertices of L have a = 4, and by (S9) each is adjacent to
z and z', so it has d_H ≤ 8 − 4 − 2 = 2, and these vertices form an independent set W (common neighbour z). Since
|W| = 13 − h ≥ 12 − h, take 12 − h of them together with H: a 12-set with at most 2(12 − h) ≤ 10 edges for h ≥ 7.
(Profiles with n_3 = 2 passing (P1)–(P8) have h ≥ 8.) ∎

**4b.6 Alternative proofs for B3–B5 and B13–B15 (PROVED; review 2.4; already excluded by (P9)).** These have h = 9,
ℓ = 6. If a_y = 2: y has ≥ 4 neighbours of a = 4 (S7); three of them are independent, each with d_H ≤ 8 − 4 − 1 = 3;
with H they form a 12-set with ≤ 9 edges. If a_z = 3 (only one): z has ≥ 3 neighbours of a = 4 (S8); the same
12-set argument. ∎

**4b.7 Case B, profiles B11 = (3,4^6,5^8) and B12 = (3,4^6,5^7,6) are impossible (PROVED; review 2.5 with RA9X2's
wording; uses Theorem 1 and S4_J).** h = 8, ℓ = 7: z with a_z = 3, T = N_I(z) (|T| = 3), and six a = 4 vertices.
deg(z) ≤ 8 gives d_O(z) ≤ 5. By (S8) z has ≥ 4 neighbours among the a = 4 vertices; call them Z (independent). In B12
the a = 6 vertex is adjacent to z (S6; z is the only a = 3 vertex), so |Z| = 4 there; in B11, |Z| ∈ {4, 5}.
(i) Every Z-vertex has exactly 3 neighbours in H: any four of Z with H form a 12-set whose edges are H–Z edges, and
d_H ≤ 8 − 4 − 1 = 3. Its H-neighbours have a = 5 (an a = 6 vertex cannot meet an a = 4 vertex, 6 + 4 > 9) and the
complementary mask (Theorem 1), which contains T (the Z-masks avoid T by (F1)). An H-vertex has d_O ≤ 3, so a
Z-type occurs at most 3 times; |Z| ≥ 4 needs at least two types; three types would need 9 vertices with a = 5, more
than exist. So **exactly two types occur in Z, and exactly six high vertices (H6) are their complements; they all
contain T.**
(ii) If z has no neighbour in H, then J = H ∪ {z} is an independent 9-set; every H-mask meets T (Theorem 1, z ≁ h),
and six contain T, so the T–H incidences are ≥ 6·3 + 2·1 = 20 > 3·6, and some i ∈ T has ≥ 7 neighbours in H plus z:
|N_J(i)| ≥ 8, against 4b.1. This applies in B11 when |Z| = 5 (then d_O(z) = 5 is used up by Z) and when z has no
high neighbour. Hence in both profiles |Z| = 4 and z has exactly one neighbour h0 ∈ H (in B12 the a = 6 vertex);
h0's mask is disjoint from T, so h0 ∉ H6, and exactly one further vertex h1 of H remains.
(iii) Let w1, w2 be the two a = 4 vertices not adjacent to z. By (S8) (triple {z, w1, w2}, sum 11) w1 ~ w2, so their
masks are disjoint (F1); by Theorem 1 each meets T. Neither is adjacent to a vertex of H6 (that would make its mask
the complement of an H6-mask, which avoids T), nor to h0 (B12: 6 + 4 > 9; B11: its mask would be I ∖ N_I(h0) ⊇ T,
and the other w would then avoid T). h1 has a = 5 and is adjacent to at most one of them (adjacency means mask
= I ∖ N_I(h1), and the two masks differ). Choose w ∈ {w1, w2} with w ≁ h1; w has no neighbour in H.
(iv) J = (H ∖ {h0}) ∪ {z, w} is an independent 9-set (z's only H-neighbour is h0; w has none; z ≁ w). Pick
i ∈ N_I(w) ∩ T. Then i is adjacent to the six vertices of H6 ⊆ J, to z and to w: |N_J(i)| ≥ 8, against 4b.1. ∎

**4b.8 Alternative proof that B25 = (4^6,5^9) is impossible (PROVED; review 2.6; uses Theorem 1; already excluded by
(P10)).** H = the nine a = 5 vertices, L the six a = 4 vertices. For Y ⊆ L, |Y| = 3:
12 ≤ e(H ∪ Y) = e(Y) + Σ_{y∈Y} d_H(y) and d_H(y) ≤ 4 − d_L(y) (degree 8), so
e(H ∪ Y) ≤ 12 + e(Y) − Σ_Y d_L(y) = 12 − e(Y) − e(Y, L ∖ Y). Equality is forced; every vertex of L lies in such a Y,
so L is independent and every L-vertex has exactly 4 neighbours in H, all of the complementary type (Theorem 1). An
occupied L-type therefore needs exactly 4 H-vertices of the complementary mask; every H-vertex has an L-neighbour of
complementary type ((MAX) + (F4), as in (P10)(b)); d_O(h) ≤ 3 bounds a type's multiplicity by 3. So L uses at least
2 types (needing 8 H-vertices) and not 3 (12 > 9): exactly two types and exactly eight H-vertices of the two
complementary masks. The ninth H-vertex has an L-neighbour, hence one of these two masks, and that L-neighbour gets
a fifth H-neighbour: contradiction. ∎

**4b.9 Case A capacity inequality for n_2 = 1 (PROVED; review 4.2 with the hypothesis k ≥ r).** Let n_2 = 1, y the
a = 2 vertex, h = |H| (v counted), ℓ = 15 − h, r = 12 − h, Z = N_L(y) (all a = 4 by (S3)), k = |Z|. Then
ℓ − 2 ≤ k ≤ ℓ − 1 (S7) and k + n_7 ≤ D − 2 (every a = 7 vertex is adjacent to y by (S5); deg(y) ≤ D). Z is
independent (common neighbour y), H is independent. **If k ≥ r**: every r-subset U ⊆ Z gives the 12-set H ∪ U with
e(H ∪ U) = e(H, U) ≥ 12; summing over all r-subsets, Σ_{z∈Z} d_H(z) ≥ ⌈12k/r⌉. Only a = 5 vertices of H can meet Z
(a = 6: 6 + 4 > 9; a = 7: their only outside neighbour is y (S5); a = 9: no outside neighbours, see (P11)); each has
d_O ≤ D − 5. So ⌈12k/r⌉ ≤ (D − 5) n_5.
**(P16a)**: exclude a Case A profile with n_2 = 1 if for every k ∈ {ℓ − 2, ℓ − 1} with k + n_7 ≤ 7, k ≥ r and
⌈12k/r⌉ > 4 n_5. On the level-12 list (P7) guarantees that k = ℓ − 2 is admissible (ℓ − 2 + n_7 ≤ D − 2), so the
condition is never satisfied vacuously there. On the level-12 list it removes exactly
A2 = (2,4^8,5^3,9^3): h = 6, ℓ = 9, r = 6; k ≤ 7 forces k = 7; ⌈84/6⌉ = 14 > 12;
A9 = (2,4^7,5^3,7,9^3): h = 7, ℓ = 8, r = 5; k ≤ 6 forces k = 6; ⌈72/5⌉ = 15 > 12. ∎

**4b.10 Case A capacity inequality for n_3 = 2 (PROVED; review 4.5).** Let a_z = a_z' = 3; W = the other ℓ − 2 vertices
of L (a = 4 by (S3)), each adjacent to z and z' (S9), so W is independent; k = |W| = ℓ − 2, r = 12 − h. If k ≥ r, as in
4b.9 Σ_{w∈W} d_H(w) ≥ ⌈12k/r⌉, and only a = 5 vertices can meet W (a = 6: sum 10; n_7 = 0 by (P5) since n_2 = 0;
a = 9 isolated in O), each with d_O ≤ 4: ⌈12k/r⌉ ≤ 4 n_5. **(P16b)** excludes the profile otherwise. On the level-12
list it removes exactly A41 = (3^2,4^5,5^3,6^2,9^3): h = 8, ℓ = 7, k = 5, r = 4, ⌈60/4⌉ = 15 > 12. ∎

**Level-16 predicates (`profile_ok(level=16)`, applied after (P1)–(P12); reporting only).**
Case B: exclude n_2 = 1 (P13: on the level-12 list exactly B0, B1, B2, by 4b.3, 4b.4); n_3 = 2 (P14: exactly B6, by
4b.5); n_3 = 1 and h ≥ 8 (P15: exactly B11, B12, by 4b.7; h = 9 is already (P9)). Case A: (P16a), (P16b) as above
(exactly A2, A9, A41). Note that (P13) and (P15) as predicates are justified only for the profiles they remove from
the level-12 list, which is the only place they are applied.
Counts: **Case B 10** (B10 = (3,4^7,5^7) and B16–B24 = 4^(15−b) 5^b, b = 0..8), **Case A 81**; identical in content and
order to review_RA9X2/survivors.py (`level16.py` checks this).
sha256(json.dumps(level-16 list)): B fd21e67063627800757849199339e28ddbaadb80948ed5bfc1d27f50c5c757e7,
A dc02f45ba1641ae2378c6bad700b33fd8b694ee55851c15dbf6998a2bdf69803 (separate from the certified list, whose sha256
values in section 4 are unchanged).

**4b.11 The all-4 profile B16 = 4^15: structure (PROVED; review section 3; excludes nothing by itself).** Let M be the
multiset of the 15 masks (4-subsets of I); by Theorem 1, x ~ y iff their masks are disjoint. Write r_i = #{masks ∋ i},
q_ij = #{masks ⊇ {i, j}}.
* r_i ∈ [3, 8] and Σ r_i = 60. Upper: deg(i) ≤ 8. Lower: by (MAX) every j ≠ i shares a neighbour with i, i.e. some
  mask contains {i, j}; a mask containing i covers 3 other elements, so r_i ≥ ⌈8/3⌉ = 3.
* q_ij ∈ [1, 3]. Lower: (MAX). If q_ij ≥ 5, five such vertices Y with I ∖ {i, j} form a 12-set with 5·2 = 10 edges
  (Y is independent: the masks meet). If q_ij = 4: a fifth vertex whose mask contains exactly one of i, j gives, with
  the four and I ∖ {i, j}, a 12-set with 4·2 + 3 = 11 edges (the five masks pairwise meet); so the other 11 masks avoid
  i and j, are 4-subsets of a 7-set, pairwise meet, and form an independent 11-set: against α = 9.
* Multiplicity ≤ 2: if a mask A occurs 3 times, every pair inside A has q = 3, so every other mask B has |A ∩ B| ≤ 1
  and at least 3 elements in the 5-set I ∖ A; the remaining 12 masks pairwise meet: an independent 12-set.
* At most 4 doubled types: two doubled types meeting in ≥ 2 elements would give q ≥ 4; so they pairwise meet in ≤ 1
  element; the doubled types through a fixed i have disjoint 3-sets in I ∖ {i}, so at most 2; 4d ≤ 9·2 gives d ≤ 4.
  Hence at least 11 of the 15 masks are distinct.
* Every occupied mask A has neighbours of at least two distinct types: by (MAX)/(F4) each of the 5 elements of I ∖ A is
  in the mask of some neighbour, and a neighbour's mask is a 4-subset of the 5-set I ∖ A, missing one element.
* Odd girth ≥ 9: if A ∩ B = B ∩ C = ∅ then A, C ⊆ I ∖ B (5 elements), so |A ∖ C| ≤ 1; along a closed walk of length
  2s + 1 the mask after 2s steps differs from the start in ≤ s elements but must be disjoint from it (4 elements), so
  s ≥ 4. Hence G[O] has no odd cycle of length < 9; every induced subgraph of G[O] on ≤ 8 vertices is bipartite.
  (RA9X2 confirmed by brute force: the shortest odd closed walk in the disjointness graph of 4-subsets of 9 is 9.)

## 4c. Further exclusions (ChatGPT round 4, accepted by RA9X3)

Source: ChatGPT round 4 (gpt/round4_transcript.md), accepted by RA9X3 (review_RA9X3/REPORT.md; its scripts
b10_table.py, mixed_enum.py, q4only.py, survivors.py are in the same folder). Proofs in my own words. **Status:
reporting only**, like 4b: they define the "level 20" list (Case B 7, Case A 77; `profile_ok(level=20)`,
`level20.py`); the certified list, the CNF and the production run are unchanged. "B k" / "A k" are version-1 indices.

**4c.1 Case B, B10 = (3,4^7,5^7) is impossible (PROVED; uses Theorem 1).** Let z be the a = 3 vertex, T = N_I(z),
H the seven a = 5 vertices (independent), W the seven a = 4 vertices. deg(z) ≤ 8 gives d_O(z) ≤ 5, and (S8) gives
d_W(z) ≥ ℓ − 3 = 5; so z has exactly five neighbours Z ⊆ W and none in H. Let p, q be the other two vertices of W:
z ≁ p, q, and the triple {z, p, q} (sum 11) spans an edge (F2), so p ~ q. By (F1) the Z-masks avoid T and
M_p ∩ M_q = ∅; by Theorem 1 M_p and M_q both meet T. Z is independent (common neighbour z).
*Step 1 (counting).* Every high vertex h has a neighbour in O ((MAX) with some i ∉ N_I(h), and (F4)); it is not in
H (independent) and not z, so it lies in W and has the complementary mask (F1). Let H_Z be the high vertices whose
complementary mask is a Z-type, h := |H_Z|; the others are complementary to M_p or M_q (these are not Z-types: they
meet T). H ∪ Z is a 12-set whose edges are the H–Z edges: E_Z := e(H, Z) ≥ 12. Group Z into mask types t with
multiplicities d_t and let c_t be the number of high vertices with mask I ∖ t; by Theorem 1 each of them is adjacent to
all d_t vertices of type t, so E_Z = Σ c_t d_t and Σ c_t = h. Bounds: c_t ≤ 3 (a Z-vertex has degree ≥ 4 + 1 + c_t ≤ 8);
d_t ≤ 3 when c_t ≥ 1 (a high vertex has d_O ≤ 3); a type with c_t = 0 contributes nothing, and the partitions (4,1),
(5) give E_Z ≤ 3, so only partitions of 5 into parts ≤ 3 matter. (A lower bound c_t ≥ 1 is not needed.) The finite
table (review_RA9X3/b10_table.py, 8 values of h) gives: max E_Z = 0, 3, 6, 9, 11 for h = 0..4, all < 12; for h = 5 only
d = (3,2) with c = (2,3) (E_Z = 12) or c = (3,2) (E_Z = 13); h = 6, 7 are not excluded by counting.
*Step 2 (h = 7).* Every high mask is I ∖ t ⊇ T. Take i ∈ M_p ∩ T: i is adjacent to z, to all 7 high vertices and to p:
degree 9 > 8.
*Step 3 (h = 6).* One high vertex h* is complementary to M_p or M_q, say M_p. Take i ∈ M_q ∩ T; i ∉ M_p, so
i ∈ I ∖ M_p = N_I(h*). i is adjacent to z, the 6 vertices of H_Z, q and h*: degree 9.
*Step 4 (h = 5).* Two high vertices lie outside H_Z. If both are complementary to M_p, the vertex i of Step 3 has
degree ≥ 1 + 5 + 1 + 2 = 9; likewise for M_q. So one, h_p, is complementary to M_p and one, h_q, to M_q. As M_p, M_q are
disjoint and both meet the 3-set T, one of them, say M_p, meets T in exactly one element; then M_p has 3 elements in
the 6-set I ∖ T, and no 4-subset of I ∖ T (every Z-mask) avoids them: p has no neighbour in Z, and its only high
neighbour is h_p (a high neighbour of p has mask I ∖ M_p; the H_Z-masks are complements of Z-types, which differ
from M_p, and h_q has mask I ∖ M_q ≠ I ∖ M_p), so d_H(p) = 1. In both h = 5 configurations some type has c_t = 3; take w ∈ Z of that type (d_H(w) = 3). The 12-set
H ∪ (Z ∖ {w}) ∪ {p} spans E_Z − 3 + 1 ≤ 13 − 3 + 1 = 11 edges (Z ∪ {p} is independent): contradiction. ∎

**Mixed family 4^(15−b) 5^b (Case B).** H = the b vertices with a = 5, L = the s = 15 − b vertices with a = 4. By
Theorem 1: H is independent, h ∈ H and x ∈ L are adjacent iff N_I(x) = I ∖ N_I(h), two vertices of L are adjacent iff
their masks are disjoint. q4_ij := #{x ∈ L : {i, j} ⊆ N_I(x)}.

**4c.2 Lemma M1: q4_ij ≤ 3; in particular every 4-mask occurs at most 3 times in L (PROVED; F1, α = 9, 12-sets).**
If five vertices of L contain {i, j}, they and I ∖ {i, j} form a 12-set with 5·2 = 10 edges (their masks meet, so they
are pairwise non-adjacent by (F1)). Suppose exactly four, Y. For any fifth outside vertex x, the 12-set
(I ∖ {i, j}) ∪ Y ∪ {x} has 4·2 = 8 edges from Y; if x ∈ L and N_I(x) meets {i, j}, or x ∈ H and N_I(x) ⊇ {i, j},
then x is adjacent to no vertex of Y (F1) and contributes ≤ 3 more: ≤ 11. So every other vertex of L avoids i and j, and every high mask contains at most one of
them. The other 11 − b low masks are 4-subsets of the 7-set I ∖ {i, j}, hence pairwise intersecting; each high mask has
≥ 4 elements in that 7-set, hence meets each of them. By (F1) the b high vertices and those 11 − b low vertices form an
independent set of size 11: against α = 9. ∎

**4c.3 Lemma M2: a tripled low mask (PROVED).** If a 4-mask A occurs 3 times in L, every pair inside A has q4 = 3, so
every other low mask B has |A ∩ B| ≤ 1 and hence ≥ 3 elements in the 5-set I ∖ A; two such masks meet, so the other
12 − b low vertices W form an independent set. With c = #{h : N_I(h) = I ∖ A} and k = #{w ∈ W : N_I(w) ∩ A = ∅},
each copy of A has degree 4 + c + k ≤ 8 (Theorem 1; the copies are pairwise non-adjacent): c + k ≤ 4. ∎

**4c.4 Moments and the forced tripled mask (PROVED).** Σ_i r_i = 60 + b and Σ_{i<j} q_ij = 90 + 4b (r_i = deg(i),
q_ij counts all outside masks containing {i, j}), 2 ≤ r_i ≤ 8 ((MAX): the masks through i cover the 8 other elements,
each covers ≤ 4; degree cap), q_ij ≥ 1 ((MAX)), Σ_i (8 − r_i) = 12 − b.
Let E = e(H, L), Q = e(L). For Y ⊆ L with |Y| = 12 − b, H ∪ Y is a 12-set: e(Y) + Σ_Y d_H(y) ≥ 12. Averaging over all Y:
((12 − b)/s) E + ((12 − b)(11 − b)/(s(s − 1))) Q ≥ 12, and E + 2Q ≤ 4s (each low vertex has d_H + d_L ≤ 4).
b = 8 (s = 7): 4E + 2Q ≥ 84 and Q ≤ (28 − E)/2 give 3E ≥ 56, **E ≥ 19**. b = 7 (s = 8): 35E + 20Q ≥ 672 and
Q ≤ (32 − E)/2 give 25E ≥ 352, **E ≥ 15**.
**No tripled mask ⇒ E ≤ 2b (needs only (F1)):** the low neighbours of a high vertex h all have the mask I ∖ N_I(h)
(F1), which then occurs ≤ 2 times, so d_L(h) ≤ 2. Hence for b = 8 (16 < 19) and b = 7 (14 < 15) some low mask is
tripled. ∎

**4c.5 Case B, B24 = 4^7 5^8 is impossible (PROVED; Theorem 1, M1, M2, S2_J).** Let A be tripled (4c.4), W the other
4 low vertices (independent, |N_I(w) ∩ A| ≤ 1), c as in M2, so c ≤ 4.
Step 1: c ≥ 3. For w ∈ W the 12-set H ∪ {A-copies} ∪ {w} spans 3c + d_H(w) + 3f_w edges (f_w = 1 iff N_I(w) ∩ A = ∅,
then w is adjacent to the three copies). If f_w = 0: d_H(w) ≤ 4, so 3c ≥ 8; if f_w = 1: d_H(w) ≤ 4 − 3 = 1, so 3c ≥ 8.
Step 2: every high vertex has a low neighbour ((MAX) + (F4)), of the complementary mask; a high vertex of mask I ∖ A is
adjacent only to the A-copies. Group W into types B with multiplicity d_B (≤ 3 by M1) and c_B high vertices of mask
I ∖ B: Σ c_B = 8 − c, and a W-vertex of type B has degree 4 + c_B + 3f_B ≤ 8. H ∪ W is a 12-set: Σ d_B c_B ≥ 12.
c = 3: Σ c_B = 5 with c_B ≤ 4 and Σ d_B = 4 reaches 12 only with d = (3, 1), c_B = (4, 1) (13); all other choices give
≤ 11. So W = three copies of B (c_B = 4, hence f_B = 0 and |A ∩ B| = 1) and one vertex C with one high neighbour; the
12-set H ∪ {A-copies} ∪ {C} spans 9 + 1 + 3f_C ≥ 12 only if f_C = 1, i.e. C ∩ A = ∅. Then B ∖ A (3 elements) and C
(4 elements) lie in the 5-set I ∖ A, so |B ∩ C| ≥ 2, and a pair in B ∩ C has q4 ≥ 4: against M1.
c = 4: Σ c_B = 4; Σ d_B c_B ≥ 12 forces d = (3, 1), c = (4, 0). So four high vertices have mask I ∖ A and four have
I ∖ B, |A ∩ B| = 1 (f_B = 0 as before) with A ∩ B = {i}, and the fourth W-vertex w has no high neighbour. J = H ∪ {w}
is an independent 9-set; i lies in no high mask, so |N_J(i)| ≤ 1: against (S2_J). ∎

**4c.6 Case B, B23 = 4^8 5^7 is impossible (PROVED; signature enumeration, script a9_b23_enum.py).** Let A be tripled
(4c.4, b = 7), W the other 5 low vertices (independent), c as in M2. Signature: c; the W-types B_1, …, B_m with
multiplicities d_1 ≥ … ≥ d_m (a partition of 5, parts ≤ 3 by M1); c_i = number of high vertices of mask I ∖ B_i;
f_i = 1 iff B_i ∩ A = ∅. Constraints, each proved:
 (S) c + Σ c_i = 7: every high vertex has a low neighbour ((MAX) + (F4)), whose mask is its complement (F1), i.e. A or
     some B_i.
 (a) c + Σ d_i f_i ≤ 4: degree of a copy of A (4c.3; Theorem 1).
 (b) c_i + 3 f_i ≤ 4: degree of a W-vertex of type i (its high neighbours are the c_i complementary ones, its low
     neighbours the three A-copies iff f_i = 1, W being independent; Theorem 1).
 (c) every Y ⊆ L with |Y| = 5, made of y_A ≤ 3 copies of A and y_i ≤ d_i vertices of type i, gives the 12-set H ∪ Y
     with y_A c + Σ y_i c_i + y_A Σ y_i f_i ≥ 12 edges (H independent; Theorem 1 for every adjacency).
The script enumerates all signatures (c from 0 to 7, all partitions, all flags, all compositions; 22,718 tested;
types of equal multiplicity are not identified, a harmless superset) and finds exactly 5 survivors, the same as
review_RA9X3/mixed_enum.py: (c; d; c_i; f) = (2; 3,2; 4,1; 0,1), (2; 3,1,1; 4,0,1; 0,1,1), (2; 3,1,1; 4,1,0; 0,1,1),
(3; 3,1,1; 4,0,0; 0,0,1), (3; 3,1,1; 4,0,0; 0,1,0). Each contains a type B with d = 3 and c_B = 4 — so f_B = 0 by (b) and
|A ∩ B| = 1 — and another type C with f_C = 1. As in 4c.5, B ∖ A and C lie in the 5-set I ∖ A, |B ∩ C| ≥ 2, and the
three copies of B with C give q4 ≥ 4: against M1. The script checks this pattern for every survivor (exit 0). ∎
(Cross-check: for b = 8 the script finds the 2 signatures of 4c.5, (3; 3,1; 4,1; 0,1) and (4; 3,1; 4,0; 0,0).)

**4c.7 Case A filter (P20): |H| = 9 and n_3 = 1 ⇒ n_5 ≥ 6 (PROVED; review "A4").** Let z be the a = 3 vertex; L = {z}
∪ five a = 4 vertices (S3). By (S8) z has a set Z of ≥ 3 neighbours among them; Z is independent. Each w ∈ Z has
d_H(w) ≤ 9 − 4 − 1 = 4; any three vertices of Z with H form a 12-set whose edges are H–Z edges, so every w ∈ Z has
exactly 4 high neighbours. These have a = 5 (a = 6: 6 + 4 > 9; n_7 = 0 by (P5); a = 9: no outside neighbours) and the
complementary mask, and by Theorem 1 every a = 5 vertex of that mask is adjacent to w: exactly 4 vertices have mask
I ∖ N_I(w). Suppose n_5 ≤ 5. Then Z has a single type A (two would need 8 vertices with a = 5), with 4 complementary
high vertices, each of outside degree ≤ 9 − 5 = 4. Not all five a = 4 vertices have mask A (else those high vertices
would have 5 outside neighbours), so some a = 4 vertex u has mask ≠ A; u ∉ Z, and its high neighbours are a = 5
vertices with mask I ∖ N_I(u), at most n_5 − 4 ≤ 1 of them. For w1, w2 ∈ Z the 12-set H ∪ {w1, w2, u} spans
≤ 4 + 4 + 1 + 2 = 11 edges: contradiction. ∎ On the level-16 list it removes exactly A80 = (3,4^5,5^5,6^3,9),
A81 = (3,4^5,5^5,6^2,9^2), A82 = (3,4^5,5^5,6,9^3), A83 = (3,4^5,5^4,6^3,9^2).

**Level-20 predicates (`profile_ok(level=20)`, applied after (P1)–(P16); reporting only).** Case B: exclude the three
tuples B10 = (3,4^7,5^7) (P17, 4c.1), B23 = 4^8 5^7 (P18, 4c.6), B24 = 4^7 5^8 (P19, 4c.5). Case A: exclude |H| = 9,
n_3 = 1, n_5 ≤ 5 (P20, 4c.7).
Counts: **Case B 7** (4^(15−b) 5^b, b = 0..6, i.e. B16–B22), **Case A 77**; identical in content and order to
review_RA9X3/survivors_out.txt (`level20.py` checks this).
sha256(json.dumps(level-20 list)): B 75bfc1c5923b629e8ff0a0cefc9f66145008e2d243d0db2c534388deff0be72f,
A 7643f96a708624bfe2c5a46476f77b543969951fe6fb9db191afefaa056d51ff (separate from the certified list, unchanged).

## 4d. ChatGPT round 5, accepted by RA9X4

Source: ChatGPT round 5 (gpt/round5_transcript.md), accepted by RA9X4 (review_RA9X4/REPORT.md, with write-up fixes:
the maximality step in N3, the k ≠ 0 step, "M_w ≠ A" in A6, no König in A7, M1 in Case A). Proofs in my own words.
**Status: reporting only** ("level 24" list: Case B 7, Case A 65; `profile_ok(level=24)`, `level24.py`). The certified
list, the CNF and the production run are unchanged. Notation of 4c (mixed family 4^(15−b) 5^b, H, L, q4, M1, M2).

**4d.1 Lemma N3: for b = 0, …, 6 no 4-mask occurs three times in L (Case B, profile 4^(15−b) 5^b) (PROVED; excludes
no profile).** Suppose A occurs three times (copies A1, A2, A3). By M2 the other 12 − b low vertices W are pairwise
non-adjacent, each W-mask meets A in at most one element, and c + k ≤ 4 (c = # high vertices with mask I ∖ A,
k = # W-vertices with mask disjoint from A). Every high vertex has a low neighbour ((MAX) + (F4); H is independent),
whose mask is its complement (F1).
* b ≤ 3: H ∪ W is a 12-set whose edges are H–W edges; a high vertex has at most 3 low neighbours (its complementary
  mask occurs ≤ 3 times by M1), so e(H ∪ W) ≤ 3b ≤ 9 < 12.
* **(i) Maximality: every W-type B has a high vertex with mask I ∖ B (c_B ≥ 1).** Let w ∈ W have mask B. The outside
  neighbours of w are the high vertices with mask I ∖ B (Theorem 1) and, if B ∩ A = ∅, the three copies of A (W is
  independent). If |B ∩ A| = 1, w has no low neighbour at all; by (MAX) and (F4), w and any i ∉ B have a common
  neighbour in O, so a high vertex of mask I ∖ B exists. If B ∩ A = ∅, B is a 4-subset of the 5-set I ∖ A; let e be the
  missing element. The common neighbour of w and e must contain e in its mask; the copies of A do not; so it is a high
  vertex of mask I ∖ B.
* **(ii) k ≥ 1.** If k = 0, the only outside edges are high–low edges (the copies of A are pairwise non-adjacent, no
  W-vertex is adjacent to a copy, W is independent), so e(O) ≤ 3b ≤ 18. But every 12-subset of O spans ≥ 12 edges, and
  an edge of O lies in a fraction C(13,10)/C(15,12) = 22/35 of them, so e(O) ≥ 12·35/22 > 19, e(O) ≥ 20.
* **(iii) The disjoint types.** Let t be the number of distinct W-types disjoint from A (t ≥ 1 by (ii)); their
  vertices number k. A vertex w of such a type C is adjacent to the three copies of A, so 4 + 3 + c_C ≤ 8 and c_C ≤ 1;
  with (i), c_C = 1. Hence the high vertices complementary to disjoint types are exactly t and contribute exactly k
  edges to e(H, W).
* **(iv) The meeting types.** If B meets A and C is a disjoint type, then B ∖ A (3 elements) and C (4 elements) lie in
  the 5-set I ∖ A, so |B ∩ C| ≥ 2 and a pair in B ∩ C gives q4 ≥ d_B + d_C; by M1 d_B ≤ 2. So every high vertex with a
  meeting-type complement has ≤ 2 neighbours in W; high vertices of mask I ∖ A have none.
* **(v) Bounds on k.** t = 1: k ≤ 3 (M1). t = 2: two distinct 4-subsets of a 5-set share 3 elements, so a common pair
  gives k = d_1 + d_2 ≤ 3. Any t: k ≤ 4 − c (M2). If c = 0: by (MAX) a copy of A needs, for each of the 5 elements of
  I ∖ A, a neighbour whose mask contains it; its neighbours are then only W-vertices of disjoint types, each missing one
  element of I ∖ A; so t ≥ 2.
* **(vi) Count.** H ∪ W is a 12-set (W independent): 12 ≤ e(H, W) ≤ k + 2(b − c − t).
  b = 4: t = 1: ≤ 3 + 2(3 − c) ≤ 9; t = 2: ≤ 3 + 2(2 − c) ≤ 7; t ≥ 3: ≤ (4 − c) + 2(1 − c) ≤ 6.
  b = 5: t = 1: ≤ 11; t = 2: ≤ 9; t ≥ 3: ≤ (4 − c) + 2(2 − c) ≤ 8.
  b = 6: t = 1 forces c ≥ 1 by (v): ≤ 3 + 2(5 − c) ≤ 11; t = 2: ≤ 3 + 2(4 − c) ≤ 11; t ≥ 3: ≤ (4 − c) + 2(3 − c) ≤ 10.
  All < 12. ∎
Independent check: review_RA9X4/caseB_notriple.py enumerates all signatures for b = 0..8 from Theorem 1, the degree
caps, M1 and the 12-set rule, and tests every survivor for a geometric realisation (q4 ≤ 3, r_i ≤ 8, q_ij ≥ 1): 0
realisations for every b ≤ 6 (review_RA9X4/caseB_notriple_out.txt).

**4d.2 Necessary conditions for 4^(15−b) 5^b, b ≤ 6 (PROVED).** For a 4-set A let u_A = multiplicity of A in L and
v_A = number of high vertices with mask I ∖ A. Then u_A ∈ {0, 1, 2} (N3); Σ u_A = 15 − b; Σ v_A = b; v_A > 0 ⇒ u_A > 0
(every high vertex has a low neighbour of complementary mask); for occupied A: Σ_{B ∩ A = ∅} u_B + v_A ≤ 4 (degree of a
low vertex of mask A, Theorem 1); every high vertex has u ≤ 2 low neighbours.
Design identities: with r4_i = #{x ∈ L : i ∈ N_I(x)} and q4_ij as before, Σ_i r4_i = 4(15 − b), Σ_{i<j} q4_ij =
6(15 − b); w_ij := 3 − q4_ij ∈ {0, 1, 2, 3} (M1); Σ w_ij = 108 − 6(15 − b) = 18 + 6b; Σ_{j ≠ i} w_ij = 24 − 3 r4_i
= 3(8 − r4_i). For b = 0, q4_ij = q_ij ≥ 1 ((MAX)), so w_ij ∈ {0, 1, 2} with total 18.

**Case A with |H| = 9.** Then ℓ = 6, H is an independent 9-set (Lemma J applies to J = H), D = 9, a = 9 vertices have
no outside neighbours (see (P11)), and an a = 4 vertex can only be adjacent to high vertices with a = 5 and the
complementary mask (a = 6: 6 + 4 > 9; a = 7: its only outside neighbour has a = 2 (S5); a = 9: none), all of which it is
adjacent to by Theorem 1.
**M1 in Case A.** In the setting of 4d.6 (L = 4^6, H = a = 5 and a = 9 vertices) the proof of 4c.2 goes through: the
fifth-vertex step for x ∈ H uses only a = 5 vertices (an a = 5 mask containing {i, j} gives 8 + 3 = 11 edges), and in
the final independent set the a = 9 vertices can be added because they are isolated in G[O]: size 15 − 4 = 11 > 9.

**4d.3 A5: Case A, |H| = 9, n_2 = 1 is impossible (PROVED).** (On the level-20 list: (2,4^5,5^8,9), (2,4^5,5^7,7,9),
(2,4^5,5^6,7^2,9).) Let y have a = 2; the other five vertices of L have a = 4 (S3), and n_6 = 0 ((P5)). By (S7) y has a
set Z of ≥ 4 neighbours among them; Z is independent. Each z ∈ Z has outside degree ≤ 9 − 4 = 5, one used by y, so
d_H(z) ≤ 4; any three vertices of Z with H form a 12-set whose edges are H–Z edges, so d_H(z) = 4 for all z ∈ Z and
the outside neighbours of z are exactly y and four a = 5 vertices of mask I ∖ N_I(z); so exactly four a = 5 vertices
have that mask. The Z-masks avoid N_I(y) (F1), so all these complementary masks contain N_I(y).
Two Z-types would need 8 vertices with a = 5, all with masks ⊇ N_I(y): then n_5 = 8, the profile is (2,4^5,5^8,9), and
y has no neighbour in H (the a = 5 vertices meet N_I(y); the a = 9 vertex has none): H ∪ {y} is an independent 10-set.
So Z has one type A, and since the four a = 5 vertices of mask I ∖ A have outside degree ≤ 4 and are adjacent to all of
Z, |Z| = 4. Let w be the fifth a = 4 vertex: w ≁ y, and w ≁ Z (their degrees are used up). If N_I(w) = A, then
N_I(w) ∩ N_I(y) = ∅ and Theorem 1 gives w ~ y: so N_I(w) = B ≠ A. The 12-set H ∪ {z1, z2, w} spans 8 + d_H(w) edges,
so d_H(w) ≥ 4: four further a = 5 vertices of mask I ∖ B, n_5 = 8, profile (2,4^5,5^8,9), H = 4 × (I ∖ A) + 4 × (I ∖ B)
+ v. y is not adjacent to the I ∖ A vertices; it is adjacent to the I ∖ B vertices iff N_I(y) ⊆ B. If so, y has
4 + 4 = 8 > 7 outside neighbours; if not, H ∪ {y} is an independent 10-set. ∎

**4d.4 A6: Case A, |H| = 9, n_3 = 1 is impossible (PROVED).** (On the level-20 list the six profiles
(3,4^5,5^8,9), (3,4^5,5^7,6,9), (3,4^5,5^7,9^2), (3,4^5,5^6,6^2,9), (3,4^5,5^6,6,9^2), (3,4^5,5^6,9^3).) Let z have
a = 3, T = N_I(z); the other five vertices of L have a = 4; n_7 = 0 ((P5)). By (S8) z has a set Z of ≥ 3 neighbours
among them (independent). As in 4d.3: d_H(w) = 4 for all w ∈ Z (d_H ≤ 9 − 4 − 1, triples of Z with H), the outside
neighbours of w are z and four a = 5 vertices of mask I ∖ N_I(w), and exactly four a = 5 vertices have that mask;
these masks contain T.
Two Z-types: 8 vertices with a = 5, so the profile is (3,4^5,5^8,9) and every a = 5 mask contains T: z has no
neighbour in H, and H ∪ {z} is an independent 10-set. So Z has one type A and, as in 4d.3, |Z| ≤ 4.
If N_I(w) = A for an a = 4 vertex w ∉ Z, then N_I(w) ∩ T = ∅ and Theorem 1 gives w ~ z: impossible. So the a = 4
vertices outside Z have masks ≠ A, and they are not adjacent to Z (degrees used up).
|Z| = 3: the two others w, w' are non-adjacent to z, and the triple {z, w, w'} (sum 11) gives w ~ w', so their masks are
disjoint, different from each other and from A. The 12-sets H ∪ {z1, z2, w} and H ∪ {z1, z2, w'} give d_H(w),
d_H(w') ≥ 4: four a = 5 vertices of each of the masks I ∖ A, I ∖ N_I(w), I ∖ N_I(w'): 12 > 9.
|Z| = 4: the fifth w has d_H(w) ≥ 4 in the same way, so n_5 = 8, the profile is (3,4^5,5^8,9) and
H = 4 × (I ∖ A) + 4 × (I ∖ B) + v with B = N_I(w). z is not adjacent to the I ∖ A vertices and is adjacent to the I ∖ B
vertices iff T ⊆ B: then z has 4 + 4 = 8 > 6 outside neighbours; otherwise H ∪ {z} is an independent 10-set. ∎

**4d.5 A7: Case A, |H| = 9, n_2 = n_3 = 0 is impossible (PROVED).** Then L consists of six a = 4 vertices and
H of m vertices with a = 5 and t = 9 − m ≥ 1 with a = 9 (on the level-20 list: (4^6,5^8,9), (4^6,5^7,9^2), (4^6,5^6,9^3),
so m ≤ 8). E := e(H, L).
* No 4-mask occurs three times in L: each a = 5 vertex has ≤ 2 low neighbours, E ≤ 2m ≤ 16. By 4b.11 (odd girth ≥ 9 of
  the disjointness graph of 4-sets) and Theorem 1, G[L] is bipartite; let X, Y be a bipartition with |X| ≥ 3. If
  |X| = |Y| = 3, the 12-sets H ∪ X and H ∪ Y give E ≥ 24. If |X| ≥ 4, take an independent 4-set U ⊆ X: its four
  triples with H are 12-sets, so 3 e(H, U) ≥ 48, e(H, U) ≥ 16; each of the two other low vertices has a high neighbour
  (else it extends H to an independent 10-set), so E ≥ 18. Both contradict E ≤ 16. (König's theorem is not needed.)
* Some mask A occurs three times (≤ 3 by M1 in Case A). As in M2 the other three low vertices W are independent and
  their masks meet A in ≤ 1 element. The 12-set H ∪ {A-copies} spans 3c edges (c = # a = 5 vertices of mask I ∖ A), so
  c ≥ 4. The 12-set H ∪ W spans e(H, W) = Σ_B d_B c_B ≥ 12 over the W-types B (d_B ≤ 3, Σ c_B ≤ m − c ≤ 4), which forces
  m = 8, c = 4 and W = three copies of one mask B with c_B = 4: H = 4 × (I ∖ A) + 4 × (I ∖ B) + v. |A ∩ B| ≤ 1 by M1.
  If A ∩ B = ∅, a copy of A is adjacent to 4 high vertices and the 3 copies of B: outside degree 7 > 9 − 4. If
  A ∩ B = {i}, i lies in no a = 5 mask, so its only neighbour in H is v: against (S2_H). ∎

**Level-24 predicate (`profile_ok(level=24)`, reporting only).** Case A: exclude |H| = 9 (P21; 4d.3–4d.5 cover the
three cases n_2 = 1, n_3 = 1, and n_2 = n_3 = 0 with L = 4^6). On the level-20 list it removes exactly the 12 profiles
named above. Case B: unchanged (N3 excludes no profile).
Counts: **Case B 7** (4^(15−b) 5^b, b = 0..6), **Case A 65** (n_9 = 1: 24, n_9 = 2: 23, n_9 = 3: 18); identical in
content and order to review_RA9X4/survivors_r5_out.txt (`level24.py` checks this).
sha256(json.dumps(level-24 list)): B 75bfc1c5923b629e8ff0a0cefc9f66145008e2d243d0db2c534388deff0be72f (as level 20),
A 28e08d6fb357e6f3cbb01bf6161bdb27416f2878a02f24abada0dfae33984ba3.

## 4e. ChatGPT round 6, accepted by RA9X5 with a repair

Source: ChatGPT round 6 (gpt/round6_condensed.txt), accepted by RA9X5 with one repair (review_RA9X5/REPORT.md;
scripts in the same folder). ChatGPT's step 1.1 used a table of maximum edge numbers of non-bipartite graphs of odd
girth ≥ 9 on 9, 10, 11 vertices (9, 10, 12) that is **false** (the true values are 9, 11, 14: a vertex may duplicate a
cycle vertex); 4e.2 below is RA9X5's repaired argument. Proofs in my own words. **Status: reporting only** ("level 28"
list: Case B 4, Case A 36; `profile_ok(level=28)`, `level28.py`); the certified list, the CNF and the production run
are unchanged.

### Case B, profiles 4^(15−b) 5^b with b = 4, 5, 6 (v1 B20, B21, B22)

**4e.1 Setting (PROVED).** s = 15 − b ∈ {11, 10, 9} low vertices (a = 4), b high vertices (a = 5); Theorem 1 gives
all adjacencies (high–low iff complementary, low–low iff disjoint, high–high never). By N3 (4d.1) every low mask
occurs at most twice, so a high vertex has 1 or 2 low neighbours (≥ 1 by (MAX) + (F4)). Let E = e(H, L), Q = e(L),
T = e(O) = E + Q, h2 = number of high vertices whose complementary mask occurs twice; then E = b + h2 ≤ 2b, and
E + 2Q ≤ 4s (a low vertex has outside degree ≤ 4). Averaging the 12-sets H ∪ Y (Y ⊆ L, |Y| = s − 3) gives
((s − 3)/s) E + ((s − 3)(s − 4)/(s(s − 1))) Q ≥ 12, i.e. 8E + 5Q ≥ 144 (b = 6), 21E + 14Q ≥ 360 (b = 5),
40E + 28Q ≥ 660 (b = 4); with E ≤ 2b: Q ≥ 10, 11, 13 respectively.

**4e.2 G[L] and G[O] are bipartite (PROVED; RA9X5's repair).** Suppose G[L] is not bipartite and let C be a shortest
odd cycle. Its length is 9 or 11 (odd girth ≥ 9 by 4b.11; s ≤ 11), it has no chord, and its vertices have pairwise
distinct masks (a repeated mask would split the closed walk of types into two shorter closed walks, one of them odd
and shorter than 9, against 4b.11).
* Length 11 (only b = 4, C = L): Q = 11 < 13.
* Length 9, C = c_0 … c_8. **A vertex x ∈ L ∖ C has at most 2 neighbours on C, and if it has 2, they are c_{j−1},
  c_{j+1} and N_I(x) = N_I(c_j)** ("x duplicates the middle vertex"). Indeed, two neighbours c_i, c_k of x split C
  into arcs of lengths d and 9 − d, one odd; with x they close an odd cycle of length (odd arc) + 2 ≥ 9, so the even
  arc has length 2; three neighbours cannot be pairwise at distance 2 on C9. If the neighbours are c_{j−1}, c_{j+1},
  then N_I(x) and N_I(c_j) are both disjoint from the two distinct masks of c_{j−1}, c_{j+1}, whose union has ≥ 5
  elements; at most one 4-set avoids it, so N_I(x) = N_I(c_j).
  - b = 6 (s = 9, L = C): Q = 9 < 10.
  - b = 5 (one extra vertex x): Q ≤ 9 + 2 = 11 and Q ≥ 11, so x duplicates some c_j and Q = 11; then 21E ≥ 360 − 154
    gives E ≥ 10 = 2b, so every high vertex has a doubled complementary mask, i.e. mask I ∖ N_I(c_j): the copies of c_j
    have degree 4 + 2 + 5 = 11 > 8.
  - b = 4 (two extra vertices x, y): Q = 9 + e_x + e_y + [x ~ y] with e_x, e_y ≤ 2 the numbers of cycle neighbours,
    and Q ≥ 13. If neither is a duplicate of a cycle vertex, Q ≤ 9 + 1 + 1 + 1 = 12. x, y cannot have the same mask
    and Q ≥ 13 (then e_x = e_y ≤ 1 and x ≁ y). So, say, x duplicates c_j.
    (B) e_y ≤ 1: then Q ≥ 13 forces e_y = 1 and y ~ x; y ~ x means N_I(y) ∩ N_I(c_j) = ∅, so y ~ c_j, and that is
        y's only cycle neighbour; y is a singleton type. Q = 13, so 40E ≥ 660 − 364 gives E = 8 = 2b: all 4 high
        vertices have mask I ∖ N_I(c_j), and a copy of c_j has degree 4 + 3 + 4 = 11 > 8.
    (A) y duplicates c_k, k ≠ j (k = j would triple a mask, against N3); x ~ y iff c_j ~ c_k iff |j − k| = 1.
        (A1) c_j ≁ c_k: Q = 13, so E = 8 and all high vertices have mask I ∖ N_I(c_j) or I ∖ N_I(c_k), h_j + h_k = 4;
        a copy of c_j has degree 4 + 2 + h_j ≤ 8, so h_j = h_k = 2. The 12-set H ∪ (L ∖ {c_j, x, y}) spans
        (13 + 8) − 4 − 4 − 4 = 9 edges (each removed vertex carries 2 low and 2 high edges, none shared): contradiction.
        (A2) c_j ~ c_k: Q = 14, so 40E ≥ 660 − 392 gives E ≥ 7, i.e. h2 ≥ 3. But a copy of c_j is adjacent to c_{j−1}
        and to both copies of c_k, so it has ≤ 1 high neighbour; likewise for c_k: h2 ≤ 2.
  Independent check: review_RA9X5/caseB_nonbip.py enumerates all 576 chordless 9-cycles of distinct 4-masks through a
  fixed arc of the Kneser graph K(9,4), every choice of the extra masks (multiplicity ≤ 2), every distribution of the
  high vertices and every 12-set H ∪ Y: 0 survivors for b = 4, 5, 6 (4,603,392 configurations for b = 4).
So G[L] is bipartite. Copies of one mask have the same neighbourhood, so a bipartition can be chosen with all copies
of a type on one side; a high vertex is adjacent only to the copies of its complementary type, so putting it on the
other side gives a bipartition of G[O]. ∎

**4e.3 T ≥ 24 (PROVED).** Let P, R be the classes of a bipartition of G[O]; each is independent in G, so |P|, |R| ≤ 9:
the sizes are {6, 9} or {7, 8}. Outside degrees: ≤ 4 for low, ≤ 2 for high vertices. For a set S ⊆ P, the 12-set
R ∪ S (|S| = 12 − |R|) spans exactly Σ_{v∈S} d(v) edges.
* {6, 9}: any three vertices of the 6-class have degree sum ≥ 12, so none is high (2 + 4 + 4 < 12) and all have degree
  4: T = Σ over the 6-class = 24.
* {7, 8}: any 4 vertices of the 7-class sum to ≥ 12 and any 5 of the 8-class sum to ≥ 12; with h7, h8 high vertices in
  the classes this gives h7 ≤ 2 (16 − 2 min(h7, 4) ≥ 12) and h8 ≤ 4 (20 − 2 min(h8, 5) ≥ 12). If h7 = 2, the two high
  vertices and any two low vertices of the 7-class reach the cap 2 + 2 + 4 + 4 = 12, so all are saturated and
  T = 2·2 + 5·4 = 24. If h8 = 4, the four high vertices and any low vertex of the 8-class reach 2·4 + 4 = 12, so
  T = 4·2 + 4·4 = 24. The remaining case is b = 4 with (h7, h8) = (1, 3): with deficiencies δ = cap − degree, every
  choice of the high vertex and three low vertices of the 7-class gives δ_high + δ_1 + δ_2 + δ_3 ≤ 2; so at most two low
  vertices have positive deficiency, and all deficiencies in the class sum to ≤ 2: T ≥ 2 + 24 − 2 = 24.
(b = 6 forces (h7, h8) = (2, 4); b = 5 gives (1, 4) or (2, 3); b = 4 gives (0, 4), (1, 3), (2, 2); RA9X5's tbound.py
checks all of them.) ∎

**4e.4 Type-graph lemmas (PROVED).** The type graph has the distinct low masks as vertices and disjointness as edges.
* It has girth ≥ 6: no odd cycles shorter than 9 (4b.11), and no 4-cycles, since two distinct 4-masks have at most
  one common disjoint 4-mask (their union has ≥ 5 elements).
* Maximum edge numbers ex(m) of girth-≥6 graphs: for m ≤ 5 the graph is a forest, ex(m) = m − 1; ex(6) = 6, attained
  only by C6 (a cycle must be Hamiltonian, a chord would make a shorter cycle); ex(7) = 7, and a 7-vertex, 7-edge
  girth-≥6 graph is C7 or C6 plus a pendant edge (if it contains a C6, the seventh vertex has at most one neighbour on
  it; otherwise every cycle is Hamiltonian and chordless): **it has at most one vertex of degree 3**. A girth-≥6 graph
  with minimum degree ≥ 3 has ≥ 2 + 4 + 8 = 14 vertices, so for m ≤ 13 deleting a vertex of degree ≤ 2 gives
  ex(m) ≤ ex(m − 1) + 2: ex(8) ≤ 9, ex(9) ≤ 11, ex(10) ≤ 13, ex(11) ≤ 15. (The exact values 9, 10, 12, 14 for m = 8..11
  are checked by RA9X5's girth6.py; only the bounds above are used.)
* Doubled types (multiplicity 2) pairwise meet in ≤ 1 element (a pair in both would have q4 = 4, against M1).
  **At most 3 doubled types:** four would have 16 incidences on 9 elements, so Σ_i C(n_i, 2) ≥ 7 pairwise
  intersections (n_i = number of doubled types containing i; minimum at seven 2's and two 1's), but ≤ C(4,2) = 6 are
  allowed. **Three doubled types meet pairwise in exactly one element:** if A ∩ B = ∅, then |A ∪ B| = 8 and the third
  type C has ≤ 1 element in A, ≤ 1 in B and ≤ 1 outside: |C| ≤ 3. So there are no edges between doubled vertices then.
* **A singleton type is disjoint from at most one doubled type:** if S is disjoint from A and B, then A, B ⊆ I ∖ S
  (5 elements) and |A ∩ B| ≥ 3.
* **Matching lemma.** Two distinct masks have at most one common disjoint mask (above). Let A, B be doubled types
  with |A ∩ B| = 1, X the singletons disjoint from A, Y those disjoint from B, U the others. X and Y are independent
  (two masks inside a 5-set meet). A vertex S ∈ X has ≤ 1 neighbour in Y: its Y-neighbours are disjoint from S and from
  B, and S ≠ B (S ∩ A = ∅ ≠ B ∩ A). Symmetrically for Y. A vertex of U has ≤ 1 neighbour in X and ≤ 1 in Y, since it
  differs from A and B. ∎

**4e.5 The three profiles are impossible (PROVED).** d := number of doubled types (d ≤ 3), x, y, z := numbers of low
edges among doubled vertices, between doubled and singleton vertices, among singleton vertices.
*b = 6 (4^9 5^6).* T ≥ 24, E + 2Q ≤ 36, E ≤ 12 give E = 12, Q = 12, and every low vertex has outside degree exactly 4;
every high vertex has a doubled complementary type, so d ≥ 1.
 d = 1: all six high vertices have the same mask and a copy of the doubled type has 6 high neighbours.
 d = 2 (A, B): if A ∩ B = ∅ each copy has 2 low neighbours of the other type, so ≤ 2 high neighbours, and
 h_A + h_B ≤ 4 < 6. If |A ∩ B| = 1: x = 0; the four doubled vertices have degree sum 16, of which 2(h_A + h_B) = 12 are
 high edges, so y = 4; the 5 singletons have z ≤ ex(5) = 4: Q ≤ 8.
 d = 3: x = 0 (4e.4), y ≤ 3·2 = 6 (each singleton meets one doubled type at most), z ≤ ex(3) = 2: Q ≤ 8 < 12.
*b = 5 (4^10 5^5).* E ≤ 10, T ≥ 24 and E + 2Q ≤ 40 give E ≥ 8, Q ≥ 24 − E = 19 − h2 ≥ 14, h2 ≥ 3.
 d = 0: E = 5. d = 1 (A): h_A = h2 ≥ 3, so a copy of A has ≤ 1 low neighbour; in the type graph on A and the 8
 singletons (9 vertices), Q = z + 2a with a ≤ 1 the type-degree of A and z + a ≤ ex(9) ≤ 11: Q ≤ 12 < 14.
 d = 2 (A, B; 6 singletons): if A ∩ B = ∅: x = 4, a copy of A has ≤ 2 − h_A singleton neighbours, so
 y ≤ 8 − 2h2, z ≤ ex(6) = 6: Q ≤ 18 − 2h2 < 19 − h2. If |A ∩ B| = 1: x = 0, y ≤ 2(4 − h_A) + 2(4 − h_B) = 16 − 2h2,
 Q ≤ 22 − 2h2; with Q ≥ 19 − h2 this forces h2 = 3, Q = 16, y = 10, z = 6: the singleton graph has 6 edges on 6
 vertices, so it is a C6; y = 10 means exactly five singletons are adjacent to (both copies of) one doubled type each.
 By the matching lemma these five induce a matching; but five vertices of a C6 induce a path with 4 edges.
 d = 3 (4 singletons): x = 0, y ≤ 8, z ≤ 3: Q ≤ 11 < 14.
*b = 4 (4^11 5^4).* E = 4 + h2 ≤ 8, Q ≥ 20 − h2.
 d = 0: 11 distinct types, Q ≤ ex(11) ≤ 15 < 20. d = 1 (A; 9 singletons): a copy of A has ≤ 4 − h2 low neighbours;
 type graph on 10 vertices: Q = z + 2a ≤ ex(10) + a ≤ 13 + 4 − h2 < 20 − h2. d = 3 (5 singletons): Q ≤ 0 + 10 + 4 = 14
 < 16 ≤ 20 − h2.
 d = 2, A ∩ B = ∅ (7 singletons): x = 4, y ≤ 8 − 2h2, z ≤ ex(7) = 7: Q ≤ 19 − 2h2 < 20 − h2.
 d = 2, A ∩ B = {i}: x = 0. Let X, Y, U be the singletons disjoint from A, from B, from neither (no singleton is
 disjoint from both), a = |X|, b' = |Y|, u = |U|, g = a + b' = 7 − u. Degrees of the copies: h_A + a ≤ 4,
 h_B + b' ≤ 4, so g ≤ 8 − h2. y = 2g and, by the matching lemma, z ≤ min(a, b') + 2u + C(u, 2), also z ≤ 7. From
 20 − h2 ≤ Q ≤ 2g + 7: g ≥ (13 − h2)/2, hence h2 ≤ 3 and:
  h2 = 0: g = 7, u = 0, z ≤ 3: Q ≤ 17 < 20. h2 = 1: g = 7 (Q ≤ 17) or g = 6, u = 1 (z ≤ 3 + 2, Q ≤ 17) < 19.
  h2 = 2: g = 6, u = 1: Q ≤ 17 < 18. h2 = 3: g = 5, u = 2: z ≤ 2 + 4 + 1 = 7, Q ≤ 17 = 20 − h2, so equality holds
  everywhere: z = 7 on 7 vertices, and both U-vertices have a neighbour in X, one in Y and each other, i.e. degree 3.
  A 7-vertex, 7-edge girth-≥6 graph has at most one vertex of degree 3 (4e.4): contradiction. ∎

### Case A (29 profiles)

**4e.6 Common facts.** D = 9; the a = 9 vertices have no outside neighbours; an a = 4 vertex is adjacent only to the
a = 5 vertices of complementary mask (all of them, Theorem 1), to low vertices of disjoint mask, and to a = 2 / a = 3
vertices as determined by (F1) and Theorem 1 (a = 6: 6 + 4 > 9; a = 7: only the a = 2 vertex, (S5)). Since v ∈ H has
a = 9, n_5 ≤ |H| − 1.

**4e.7 n_2 = 1 and |H| ∈ {6, 7, 8} (15 profiles, v1 A0, A1, A4–A8, A11–A18) are impossible (PROVED).** Let y have
a = 2, W the other low vertices (a = 4), m = |W| = 14 − |H|. By (S7) y is adjacent to ≥ m − 1 of W; its outside degree
is ≤ 7.
*One non-neighbour lemma.* If y ≁ w for exactly one w ∈ W and Z = W ∖ {w} has ≥ 6 vertices: for z ∈ Z the triple
{y, z, w} (sum 10) spans 2 edges, so z ~ w; hence the Z-masks avoid N_I(y) ∪ N_I(w), which has ≤ 5 elements
(N_I(y) ∩ N_I(w) ≠ ∅ by Theorem 1 since y ≁ w); so they are 4-subsets of a set G0 of ≥ 4 and ≤ 5 elements. Z is
independent. Six Z-masks have 24 incidences in G0, so some 3 elements J carry ≥ 15 of them; the 12-set
(I ∖ J) ∪ (those six) spans ≤ 24 − 15 = 9 edges.
* |H| = 6 (m = 8): y has ≥ 7 low neighbours and outside degree ≤ 7: exactly one non-neighbour: the lemma applies.
* |H| = 7 (m = 7): by the lemma y ~ all of W, which uses up its outside degree, so n_7 = 0. The W-masks lie in the
  7-set N = I ∖ N_I(y) and W is independent; the 12-sets (I ∖ J) ∪ W for 4-sets J ⊆ N give Σ_{i∈J} r_i ≤ 16 (r_i =
  frequency of i in W), and Σ_{i∈N} r_i = 28 forces r_i = 4 for all i ∈ N. A mask cannot occur 4 times (its elements
  would be saturated, leaving 3 elements for the other masks). If A occurs 3 times, the other four masks each contain
  N ∖ A and one element of A, so they are distinct; the a = 5 vertices of mask I ∖ A number ≤ 4 (degree of a copy:
  4 + 1 + c ≤ 9), so e(H, W) ≤ 3·4 + (n_5 − 4) ≤ 14; otherwise every mask occurs ≤ 2 times and e(H, W) ≤ 2 n_5 ≤ 12.
  But the 12-sets H ∪ Y (Y ⊆ W, |Y| = 5) average to e(H, W) ≥ ⌈84/5⌉ = 17.
* |H| = 8 (m = 6). If y has exactly 5 low neighbours Z (one non-neighbour w): as in the lemma the Z-masks are 4-subsets
  of G0 (≤ 5 elements) and Z is independent; each z ∈ Z is adjacent to y and w, so d_H(z) ≤ 3, and the 12-sets H ∪ Z'
  (|Z'| = 4) force d_H(z) = 3; so every Z-type has exactly 3 complementary a = 5 vertices; n_5 ≤ 7 allows ≤ 2 types;
  one type (5 copies) would give its high vertices 5 outside neighbours; two types share ≥ 3 elements of G0, so all five
  Z-masks contain a common pair {i, j} and (I ∖ {i, j}) ∪ Z spans 10 edges. Hence y ~ all of W; W is independent, its
  masks lie in N = I ∖ N_I(y), and averaging the 12-sets H ∪ Y (|Y| = 4) gives e(H, W) ≥ 18. Every a = 5 vertex meets
  only copies of one mask and has ≤ 4 outside neighbours; a W-vertex has ≤ 4 high neighbours (4 + 1 + c ≤ 9). By the
  multiplicity pattern of W:
  - all ≤ 2: e(H, W) ≤ 2 n_5 ≤ 14;
  - a mask with ≥ 5 copies has no high neighbour (its high vertices would have ≥ 5 outside neighbours), and four
    copies with H give a 12-set with 0 edges;
  - (3,1,1,1): ≤ 3·4 + 3 = 15; (4,1,1): two copies and the two singletons have high degrees summing to
    ≤ c_A + (c_A + c_S1 + c_S2) ≤ 4 + 7 = 11 < 12;
  - (3,2,1): 3c_A + 2c_B + c_C ≥ 18 with c's ≤ 4 and sum ≤ 7 forces (4, 3, 0); then {C, B, B, A} has high degrees
    0 + 3 + 3 + 4 = 10 < 12;
  - (4,2): A, B ⊆ N (7 elements) meet; J = three elements of A including one of A ∩ B carries 4·3 + 2 = 14 incidences,
    and (I ∖ J) ∪ W spans 24 − 14 = 10 edges;
  - (3,3): |A ∩ B| ≥ 2 would put a pair in five independent vertices (10 edges), and A ∩ B ≠ ∅ (inside N), so
    |A ∩ B| = 1. The 12-sets H ∪ {A, A, A, B} and H ∪ {A, B, B, B} give c_A, c_B ≥ 3. Take three B-copies, three a = 5
    vertices of mask I ∖ A (pairwise non-adjacent, and not adjacent to the B-copies since B ≠ A) and J = B ∖ A
    (3 elements): the 12-set (I ∖ J) ∪ (these six) spans 3·1 + 3·2 = 9 edges. ∎

**4e.8 n_3 = 2 and |H| ∈ {7, 8} (11 profiles, v1 A29–A31, A33–A40) are impossible (PROVED).** Let z, z' have a = 3,
masks T, T'. By (S9) z ≁ z' and every a = 4 vertex is adjacent to both; so the a = 4 vertices W form an independent set
with masks in U = I ∖ (T ∪ T'), |U| ≤ 6; two distinct W-masks meet in ≥ 2 elements. No pair lies in five W-masks
((I ∖ {i, j}) ∪ five of them would span 10 edges), so a mask occurs ≤ 4 times and two distinct masks have total
multiplicity ≤ 4. A W-vertex has ≤ 9 − 4 − 2 = 3 high neighbours, all with a = 5 and complementary mask (n_7 = 0 by (P5)).
* |H| = 8 (|W| = 5): the 12-sets H ∪ W' (|W'| = 4) force every w to have exactly 3 high neighbours, so each W-type has
  exactly 3 complementary a = 5 vertices; n_5 ≤ 7 allows ≤ 2 types; one type would give its high vertices 5 outside
  neighbours, two types have total multiplicity 5 > 4.
* |H| = 7 (|W| = 6): averaging the 12-sets H ∪ Y (|Y| = 5) gives e(H, W) ≥ ⌈72/5⌉ = 15. The multiplicity pattern is
  (3,1,1,1) or has all multiplicities ≤ 2. In the first case ≤ 3 high vertices match the tripled mask (3 neighbours
  each) and every other high vertex meets ≤ 1 W-vertex: e(H, W) ≤ 9 + 3 = 12 (n_5 ≤ 6); in the second e(H, W) ≤ 2 n_5
  ≤ 12. ∎

**4e.9 Pure profiles 4^(12−m) 5^m 9^3 with m ≥ 3 are impossible; on the level-24 list v1 A100 (4^9,5^3,9^3), A103
(4^8,5^4,9^3), A106 (4^7,5^5,9^3) (PROVED).** Let Z be the three a = 9 vertices (isolated in G[O]) and U = O ∖ Z,
|U| = 12. α(G[U]) ≤ 6 (with Z an independent set of G), and every 9-set S ⊆ U spans ≥ 12 edges (S ∪ Z is a 12-set).
*G[U] is bipartite.* For m ≥ 4 the low graph has ≤ 8 vertices and odd girth ≥ 9. For m = 3 a non-bipartite low graph
on 9 vertices is a chordless C9 (9 edges), so e(U) ≤ 9 + 3·4 = 21, while averaging 9-sets gives
e(U) ≥ ⌈12·C(12,9)/C(10,7)⌉ = ⌈12·220/120⌉ = 22. The high vertices attach to copies of one type, as in 4e.2.
The two classes are independent in G, so both have exactly 6 vertices, and taking a whole class plus three vertices
of the other shows: **any three vertices of a class have degree sum ≥ 12** (outside degrees: a = 4 ≤ 5, a = 5 ≤ 4).
*No class contains ≥ 3 high vertices.* If X does, any three of them force all its high vertices to have degree 4;
their neighbours are the copies of their complementary masks in the other class Y (6 vertices), so they all have the
same complementary mask P with exactly 4 copies in Y. The other two vertices of Y (k high, 2 − k low, k ≤ 2) are not
adjacent to the high vertices of X, so they have degree ≤ 6 − h ≤ 3 (h ≥ 3 high vertices in X); these two and one
P-copy (degree ≤ 5) sum to ≤ 11. Hence each class has ≤ 2 high vertices, m ≤ 4: m = 5 (A106) is impossible.
*m = 4:* two high vertices per class. In X, the two high vertices and a low vertex sum to ≥ 12, so one high vertex has
degree 4 and the four low vertices of Y are copies of one mask P; symmetrically the low vertices of X are copies of
one mask Q. Every high vertex has a low neighbour ((MAX) + (F4)), so both high vertices of X have mask I ∖ P and both of
Y have I ∖ Q. A P-copy then has degree 2 + (4 if P ∩ Q = ∅ else 0) = 6 > 5 or 2, and three P-copies would sum to 6.
*m = 3:* the classes have 2 and 1 high vertices; X = {h1, h2} + 4 low, Y = {h3} + 5 low. As before h1 has degree 4,
its mask's complement P has 4 copies in Y, and the fifth low vertex q of Y has another mask. h2 has degree
≥ 12 − 4 − 5 = 3, so its complementary mask has ≥ 3 copies in Y: it is P, and q has no high neighbour: d(q) ≤ 4 (its
neighbours are low vertices of X). Let g = d(h3): the triple {h3, q, P-copy} gives g ≥ 12 − 4 − 5 = 3, so ≥ 3 low
vertices of X have mask C (complement of h3's mask).
 g = 4: all four low vertices of X are C-copies, and a P-copy has degree 2 + (0 or 4): 2 (three of them sum to 6) or 6.
 g = 3: three C-copies and a fourth low vertex r with another mask; the triple gives d(q) = 4 and d(P-copy) = 5 for
 every P-copy; q is adjacent to all four low vertices of X; a P-copy has 2 high and 3 low neighbours in X, which forces
 P ∩ C = ∅ (all-or-nothing on the C-copies) and P-copy ≁ r; then a C-copy is adjacent to the 4 P-copies, q and h3:
 degree 6 > 5. ∎
(For m = 6 the same argument gives a second proof of A109 = (4^6,5^6,9^3), already excluded by 4d.5.)

**Level-28 predicates (`profile_ok(level=28)`, applied after (P1)–(P21); reporting only).** Case B: exclude 4^11 5^4,
4^10 5^5, 4^9 5^6 (P22, 4e.5). Case A: exclude n_2 = 1 with |H| ∈ {6, 7, 8} (P23, 4e.7); n_3 = 2 with |H| ∈ {7, 8}
(P24, 4e.8); entries in {4, 5, 9} with n_9 = 3 and n_5 ≥ 3 (P25, 4e.9).
Counts: **Case B 4** (4^15, 4^14 5, 4^13 5^2, 4^12 5^3 = v1 B16–B19), **Case A 36** (n_3 = 1: 18; pure 4/5/9: 18);
identical in content and order to RA9X5's survivors (review_RA9X5/idx_out.txt, REPORT.md; `level28.py`).
sha256(json.dumps(level-28 list)): B 1f5e234b36b722085a2100866ee3a398ef6cbc291997a843880f0a4a893860e0,
A 8297d5c80689ed834e7bc4c05b690201755ce20e8726a2ae6fb44972c3b7000f (separate from the certified list, unchanged).

## 4f. ChatGPT round 7, accepted by RA9X6

Source: ChatGPT round 7 (gpt/round7_part1_condensed.txt and the following parts), accepted by RA9X6
(review_RA9X6/REPORT.md; scripts c9lemma.py, caseA_iso9.py, misc_checks.py in the same folder). Proofs in my own words.
**Status: reporting only** ("level 32" list: Case B 4, Case A 32; `profile_ok(level=32)`, `level32.py`); the certified
list, the CNF and the production run are unchanged.

**4f.1 Finite lemma C9 (PROVED by exhaustive enumeration; review_RA9X6/c9lemma.py).** Consider the disjointness graph
K(9,4) on the 126 four-subsets of a 9-set, and call a family of masks *admissible* if no pair of elements lies in more
than 3 of its masks (q4 ≤ 3). By symmetry (S_9 acts transitively on ordered pairs of disjoint 4-sets) fix the first two
masks A = {0,1,2,3}, B = {4,5,6,7}. Then:
(a) there is no admissible path of 10 distinct masks (the admissible simple paths starting with (A, B) number
1, 4, 16, 64, 256, 384, 576, 1152 for 2, …, 9 vertices and 0 for 10);
(b) the admissible 9-cycles through the oriented edge (A, B) number 576 (all chordless);
(c) no further mask adjacent to such a cycle keeps the family admissible (0 of 15,552 candidates), and
(d) no second copy of a cycle mask keeps it admissible (0).
Counts 1152 / 0 / 576 / 0 / 0. Control: without the condition q4 ≤ 3 there are 60,960 ten-mask paths, so the
condition is essential.
**Consequence (PROVED, given (a)–(d)).** Let L be the low vertices of a profile 4^(15−b) 5^b (Case B). The family of
low masks is admissible by M1 (4c.2, valid for every b), and so is every subfamily. Let K be a non-bipartite component
of G[L] and C a shortest odd cycle in K. Its masks are distinct (two vertices with equal masks are twins; on a shortest
odd cycle of length ≥ 5 a vertex whose two cycle-neighbours are twins would close a shorter odd cycle), its length is
≥ 9 (4b.11), and it is not ≥ 11, since 10 consecutive vertices would form an admissible 10-mask path (a). So C is a
9-cycle, and by (c), (d) no other low vertex (new mask or copy) is adjacent to it: K = C, a C9. As s ≤ 15 < 18 there is
at most one such component, and the other s − 9 low vertices span a triangle-free graph, so
Q ≤ 9 + ⌊(s − 9)²/4⌋ (Mantel), i.e. Q ≤ 18, 15, 13, 11 for b = 0, 1, 2, 3. The averaged 12-set inequality of 4e.1
with E ≤ 2b (N3) requires Q ≥ 20, 18, 16, 14 (recomputed in review_RA9X6/misc_checks.py). Hence **G[L] is bipartite for
b = 0, …, 3**, and, as in 4e.2 (high vertices attach to the copies of one type), **G[O] is bipartite**. ∎
This does not exclude the four Case B profiles 4^15, 4^14 5, 4^13 5^2, 4^12 5^3, which stay **OPEN**. (ChatGPT also
gave a bipartite 15-vertex graph with 21 edges, every 12-set spanning ≥ 12 edges and α = 8, verified by RA9X6: the
step T ≥ 24 of 4e.3 does not carry over to b ≤ 3 without the mask structure.)

**4f.2 Case A preliminaries.** As in 4e.6; three a = 9 vertices Z are isolated in G[O], and F := G[O ∖ Z] has 12
vertices, α(F) ≤ 6 (an independent 7-set of F with Z would be an independent 10-set), and every 9-subset of F spans
≥ 12 edges (with Z it is a 12-set). Outside degrees: a = 4 ≤ 5, a = 5 ≤ 4, a = 6 ≤ 3.

**4f.3 v1 A73 = (3,4^6,5^3,6^2,9^3) is impossible (PROVED).** |H| = 8 (three a = 5, two a = 6, three a = 9), L = {z}
∪ six a = 4 vertices, z with a = 3. Each a = 6 vertex is adjacent to z (S6) and to no other outside vertex (any other
mask has size ≥ 4, and 6 + 4 > 9). z has outside degree ≤ 6, two used by the a = 6 vertices, and ≥ 4 neighbours among
the a = 4 vertices (S8): exactly four, Z, and no a = 5 neighbour; Z is independent. The 12-set H ∪ Z spans only edges
between the three a = 5 vertices and Z, at most 3·4 = 12, so all 12 are present: every Z-vertex has the complementary
mask of every a = 5 vertex, so all of Z has one mask P (and the a = 5 vertices have mask I ∖ P). Z together with the
two a = 6 vertices is an independent 6-set of F; each of the other two a = 4 vertices p, q is not adjacent to the a = 6
vertices, so by α(F) ≤ 6 it has a neighbour in Z, hence (Theorem 1, equal masks) is adjacent to all of Z. Then a
Z-vertex is adjacent to z, three a = 5 vertices, p and q: outside degree 6 > 5. ∎

**4f.4 v1 A89 = (4^12,9^3), A92 = (4^11,5,9^3), A96 = (4^10,5^2,9^3) are impossible (PROVED; numerical bounds checked
by review_RA9X6/caseA_iso9.py).** Here F consists of m ∈ {0, 1, 2} a = 5 vertices and 12 − m a = 4 vertices.
* M1 holds (4d, "M1 in Case A"); a mask occurring three times would make the other 9 − m low vertices pairwise
  intersecting, hence independent, and with Z an independent set of 12 − m ≥ 10: so every mask occurs ≤ 2 times, at
  most 3 masks are doubled (4e.4), and E := e(H_5, L) ≤ 2m.
* F is bipartite: averaging 9-sets, e(F) ≥ ⌈12·C(12,9)/C(10,7)⌉ = 22. A shortest odd cycle of F consists of low
  vertices (a high vertex's neighbours are twins, see 4f.1), so it has length 9 or 11. For 11, the twelfth vertex adds
  ≤ 5 edges: e(F) ≤ 16. For 9 (chordless), each of the 3 other vertices has ≤ 2 neighbours on it (4e.2) and they span
  ≤ 2 edges (triangle-free): e(F) ≤ 9 + 6 + 2 = 17. Both < 22.
* Every vertex of F has degree ≥ 2 and both classes have exactly 6 vertices (α(F) ≤ 6); a class plus three vertices of
  the other is a 9-set spanning the degree sum of the three, so any three vertices of a class have degree sum ≥ 12, and
  e(F) ≥ 24. Hence Q := e(L) ≥ 24 − 2m. Copies of a mask are twins of positive degree, so they lie in the same class.
* Upper bound. Let the low vertices split p + q over the classes (6 + 6 for m = 0; 5 + 6 for m = 1; 4 + 6 or 5 + 5 for
  m = 2) and let d_l, d_r be the numbers of doubled masks in the two classes (d = d_l + d_r ≤ 3). The distinct masks
  form a bipartite C4-free graph (two distinct masks have ≤ 1 common disjoint mask), so their edges number at most the
  Zarankiewicz number z(p − d_l, q − d_r; 2, 2); each second copy adds ≤ 5 edges (its outside degree). If d_l ≥ 2, a
  vertex of the other class meets at most one doubled mask of the first (two doubled masks meet in ≤ 1 element, so their
  union has ≥ 7 elements and no 4-set avoids it), so the low edges at the doubled vertices of that class are ≤ 2q and
  Q ≤ 2q + 5(p − 2d_l); symmetrically for d_r ≥ 2; and always Q ≤ 5 min(p, q). With the exact values z(a, b; 2, 2) for
  a, b ≤ 6 (16 for 6 × 6, 14 for 5 × 6, 12 for 5 × 5 and 4 × 6, …; computed in caseA_iso9.py), the maximum of these bounds
  over all cases is 22, 20, 19 for m = 0, 1, 2, below the required 24, 22, 20. ∎
Together with 4e.9 (m ≥ 3) and 4d.5 (m = 6), every pure profile 4^(12−m) 5^m 9^3 is impossible.

**Level-32 predicates (`profile_ok(level=32)`, applied after (P1)–(P25); reporting only).** Case A: exclude
(3,4^6,5^3,6^2,9^3) (P26, 4f.3) and entries in {4, 5, 9} with n_9 = 3 and n_5 ≤ 2 (P27, 4f.4). Case B unchanged.
Counts: **Case B 4** (4^15, 4^14 5, 4^13 5^2, 4^12 5^3), **Case A 32** (v1 55–57, 59–72, 84–88, 90, 91, 94, 95, 98, 99,
101, 102, 104, 105); identical in content and order to RA9X6's survivors (`level32.py`).
sha256(json.dumps(level-32 list)): B 1f5e234b36b722085a2100866ee3a398ef6cbc291997a843880f0a4a893860e0 (as level 28),
A 498f5473dfc64cc164a1cc9f830f1b1a7928ddf6fd64a27ad75f50ea64970b2b (separate from the certified list, unchanged).

## 4g. ChatGPT round 8 (part 1), reviewed by RA9X7 with a repair

Source: ChatGPT round 8, part 1 (closure_drafts/reviews/gpt/round8_part1_condensed.md), reviewed by RA9X7
(review_RA9X7/REPORT.md: 1.1, 1.2, 2.1–2.5 accepted, 2.6 accepted with a repair for s = 6, k = 5; status
[hand-proof reviewed]). Proofs in my own words; this write-up was checked by RA9X8 (ACCEPT WITH REPAIR; the 4g.3.3 repair is applied;
scripts in review_RA9X8/). **Status: reporting
only.** No `profile_ok` level and no predicate are added; the certified list (section 4, version 2: 131 + 299; its
sha256 values unchanged), `a9core.py`, the CNF and the production run are unchanged. Nothing here is a SAT certificate,
and no order-24 theorem is claimed. Profile numbers are version-1 indices (archive_v1/).
Supporting evidence (not part of the proofs): RA9X7's standard-library scripts in review_RA9X7/ — caseB_checks.py
(caseB_checks_out.txt: 4g.1 frequency vectors, 4g.2 degree vectors, trace multisets and set algebra), small_checks.py
(small_checks_out.txt: 4g.3.3 incidence count, the intersection facts, the averaging numbers, the k = 5 patterns),
caseA_onea3.py (caseA_onea3_out.txt: end-to-end model check of all 17 profiles of 4g.3, 0 survivors), idx.py
(idx_out.txt: index ↔ tuple table).

### Case B, profiles 4^(15−b) 5^b with b = 0, …, 3 (v1 B16–B19)

**4g.1 Rigidity lemma (PROVED).** Let X ⊆ O be an independent set of G with |X| = 9 in which every mask has size 4
or 5, and let h ≤ 3 be the number of vertices of X with a = 5. For i ∈ I put r_i = #{x ∈ X : i ∈ N_I(x)}. Then
r_i ≥ 4 for every i ∈ I; more precisely r_i = 4 + e_i with e_i ≥ 0 and Σ e_i = h, so the sorted frequency vector is
one of 4^9 (h = 0); 4^8 5 (h = 1); 4^8 6, 4^7 5^2 (h = 2); 4^8 7, 4^7 5 6, 4^6 5^3 (h = 3).
Proof. Σ_i r_i = Σ_{x∈X} a_x = 36 + h. For J ⊆ I with |J| = 6, S = (I ∖ J) ∪ X is a 12-set; I and X are independent,
so the edges of S are the I–X edges inside S: e(S) = Σ_{x∈X} |N_I(x) ∖ J| = (36 + h) − Σ_{i∈J} r_i ≥ 12, i.e.
Σ_{i∈J} r_i ≤ 24 + h for every 6-set J. Taking J = the six largest frequencies, the three smallest r_1 ≤ r_2 ≤ r_3
sum to ≥ (36 + h) − (24 + h) = 12. If r_1 ≤ 3, then r_2 + r_3 ≥ 9, so r_3 ≥ 5, and the six largest frequencies (each
≥ r_3) sum to ≥ 30 > 27 ≥ 24 + h: contradiction. Hence every r_i ≥ 4; writing r_i = 4 + e_i gives Σ e_i = h, and the
vectors listed are the partitions of h = 0, …, 3 (conversely every such vector satisfies the 6-set inequality, as
Σ_{i∈J} e_i ≤ h). ∎ (RA9X7 enumerated all sorted 9-vectors with these constraints: exactly the list above.)

**4g.2 No 9 + 6 bipartition for b = 0, …, 3 (PROVED, conditional on 4f.1; excludes no profile).** Let the profile be
4^(15−b) 5^b with b ≤ 3. By 4f.1, G[O] is bipartite. **Every partition O = X ⊔ Y into two independent sets has
{|X|, |Y|} = {8, 7}.**
Proof. Both classes are independent in G, so |X|, |Y| ≤ 9 (α = 9), and the sizes are {9, 6} or {8, 7}. Suppose
|X| = 9, |Y| = 6.
(a) Outside degrees. A low vertex (a = 4) has d_O ≤ 8 − 4 = 4. A high vertex (a = 5) with mask C has as O-neighbours
only vertices whose masks are disjoint from C (F1), i.e. 4-sets inside the 4-set I ∖ C: copies of the low mask I ∖ C,
which occurs at most twice by N3 (4d.1, b ≤ 6); so d_O ≤ 2.
(b) Every y ∈ Y is low with d_O(y) = 4. For U ⊆ Y with |U| = 3, X ∪ U is a 12-set; since X and Y are independent, all
O-neighbours of a vertex of Y lie in X and e(X ∪ U) = Σ_{y∈U} d_O(y) ≥ 12. If some y had d_O(y) ≤ 3 (in particular if
y were high), y and any two other vertices of Y would give ≤ 3 + 4 + 4 = 11.
(c) Fix y ∈ Y, B = N_I(y), and let N ⊆ X be its 4 neighbours; their masks are disjoint from B (F1). Let X' = X ∖ N,
|X'| = 5. X satisfies the hypotheses of 4g.1 (h ≤ b ≤ 3), so each i ∈ B lies in ≥ 4 masks of X, none of them in N:
each i ∈ B is missing from at most one mask of X'. The at most 4 vertices of X' missing an element of B leave some
x ∈ X' with N_I(x) ⊇ B.
(d) If a_x = 4, then N_I(x) = B, and every vertex of N has a mask disjoint from N_I(x), so it is adjacent to x by
Theorem 1 (4b.2): an edge inside X, against its independence.
(e) If a_x = 5, A := N_I(x) ⊋ B. x has an O-neighbour w ((MAX) for x and some i ∈ I ∖ A, with (F4)); its mask is a
subset of size ≥ 4 of the 4-set I ∖ A, so N_I(w) = I ∖ A, and w ∈ Y because X is independent. N_I(w) = I ∖ A is
disjoint from B ⊆ A, so w ≠ y and, by Theorem 1, w ~ y: an edge inside Y, against its independence. ∎
(This is RA9X7's shorter ending; ChatGPT's longer second step via a second high vertex x' is also correct but not
needed. Dependencies: 4f.1 (hence the enumerated lemma C9), N3, M1 via N3, Theorem 1, (MAX), (F1), (F4), 4g.1.)
Consequence: 4^15, 4^14 5, 4^13 5^2, 4^12 5^3 remain **OPEN**; any graph of these profiles would have G[O] bipartite
with classes of sizes 8 and 7 only.

### Case A, the 17 profiles with exactly one entry a = 3

The profiles (v1 index: tuple), with s = n_4 and h = |H| = 14 − s (v counted):
s = 8 (h = 6): 55 (3,4^8,5^5,9), 56 (3,4^8,5^4,9^2), 57 (3,4^8,5^3,9^3);
s = 7 (h = 7): 59 (3,4^7,5^6,9), 60 (3,4^7,5^5,6,9), 61 (3,4^7,5^5,9^2), 62 (3,4^7,5^4,6,9^2), 63 (3,4^7,5^4,9^3),
64 (3,4^7,5^3,6,9^3);
s = 6 (h = 8): 65 (3,4^6,5^7,9), 66 (3,4^6,5^6,6,9), 67 (3,4^6,5^6,9^2), 68 (3,4^6,5^5,6^2,9), 69 (3,4^6,5^5,6,9^2),
70 (3,4^6,5^5,9^3), 71 (3,4^6,5^4,6^2,9^2), 72 (3,4^6,5^4,6,9^3).
These are exactly the 17 profiles with n_3 = 1 on the level-32 list (review_RA9X7/idx_out.txt).

**4g.3.1 Setting (PROVED).** D = 9. Let z be the a = 3 vertex, T = N_I(z), W the s vertices with a = 4 (so
L = {z} ∪ W), m = n_5, Z = N(z) ∩ W, k = |Z|. In these profiles n_2 = 0, n_7 = 0 ((P4), (P5)) and n_9 ≥ 1; since v ∈ H
has a = 9, **m ≤ h − 1**.
* **s − 2 ≤ k ≤ 6 − n_6.** Lower bound: (S8), z has at most two non-neighbours in L ∖ {z} = W. Upper bound: deg(z) ≤ 9
  gives d_O(z) ≤ 6, and every a = 6 vertex is adjacent to z by (S6) (z is the only vertex with a = 3) and lies outside
  W. For 68 and 71 (s = 6, n_6 = 2) this forces k = 4.
* **Z is independent.** Its masks are disjoint from T (F1), i.e. 4-subsets of the 6-set N := I ∖ T; two 4-subsets of
  a 6-set meet in ≥ 2 elements, so no two Z-vertices are adjacent (F1).
* **H-neighbours of Z.** For w ∈ Z, an H-neighbour of w has a = 5 and mask I ∖ N_I(w): a = 6 is excluded by 6 + 4 > 9
  (F1), n_7 = 0, and a = 9 vertices have no O-neighbours (see (P11)); a 5-mask disjoint from a 4-mask is its
  complement. Conversely every a = 5 vertex of mask I ∖ N_I(w) is adjacent to w (Theorem 1). For a 4-set A let
  c_A = #{a = 5 vertices with mask I ∖ A}; each a = 5 vertex is counted for one A only, so Σ_A c_A ≤ m, and for
  Y ⊆ Z with y_A vertices of type A, e(H, Y) = Σ_A y_A c_A.
* **c_A ≤ 4 for every Z-type A:** a copy w of A has d_O(w) ≤ 9 − 4 = 5, one O-edge goes to z, and w is adjacent to all
  c_A vertices counted by c_A.
* **The 12-set rule.** H is independent (S1) and Z is independent, so for Y ⊆ Z with |Y| = 12 − h = s − 2 (possible
  since k ≥ s − 2) H ∪ Y is a 12-set with e(H ∪ Y) = e(H, Y): **e(H, Y) ≥ 12 for every (s − 2)-subset Y of Z.**

**4g.3.2 Common-pair obstruction (PROVED; hypothesis k = s − 2).** If k = s − 2, then no four vertices of Z have masks
containing a common pair J = {i, j} ⊆ I. In particular (since any two Z-masks share a pair, see 4g.3.1) Z has no type
of multiplicity ≥ 4, no tripled type together with a further vertex, and no two doubled types.
Proof. Let p, q be the two vertices of W ∖ Z. z ≁ p, q, and the triple {z, p, q} has incidence sum 11, so it spans an
edge (F2): p ~ q, and N_I(p) ∩ N_I(q) = ∅ (F1). Suppose U ⊆ Z, |U| = 4, all masks ⊇ J. Consider the 12-set
S = (I ∖ J) ∪ U ∪ {p}. Its edges: 4·2 = 8 between I ∖ J and U, 4 − |N_I(p) ∩ J| between I ∖ J and p, none inside U
(Z independent), and between p and U only if a mask of U is disjoint from N_I(p). If N_I(p) meets J, it meets every
mask of U, so p has no neighbour in U (F1) and e(S) = 8 + 4 − |N_I(p) ∩ J| ≤ 11 < 12. Hence N_I(p) ∩ J = ∅, and by the
same argument N_I(q) ∩ J = ∅. Then N_I(p) and N_I(q) are disjoint 4-subsets of the 7-set I ∖ J: impossible. ∎

**4g.3.3 Balanced incidence for k = 6 (PROVED).** If k = 6, every element of N lies in exactly 4 of the six Z-masks,
no Z-type occurs three times, and e(H, Z) ≤ 2m.
Proof. Let f_i = #{w ∈ Z : i ∈ N_I(w)}; f_i = 0 for i ∈ T and Σ_{i∈N} f_i = 24. For J ⊆ I with |J| = 3 the 12-set
(I ∖ J) ∪ Z (Z independent) spans Σ_{w∈Z} |N_I(w) ∖ J| = 24 − Σ_{i∈J} f_i edges, so Σ_{i∈J} f_i ≤ 12. Sort the six
values on N: f_1 ≤ … ≤ f_6. Then f_4 + f_5 + f_6 ≤ 12 and f_1 + f_2 + f_3 ≤ f_4 + f_5 + f_6, with total 24, so both
triples sum to exactly 12. f_4 is the least of three values summing to 12, so f_4 ≤ 4; f_3 is the largest of three
values summing to 12, so f_3 ≥ 4; with f_3 ≤ f_4 this gives f_3 = f_4 = 4. Then three values ≥ f_4 = 4 summing to 12
are all 4, and three values ≤ f_3 = 4 summing to 12 are all 4 (repair by RA9X8). So every i ∈ N is omitted by exactly two Z-masks. A type A occurring three times
would omit the two elements of N ∖ A three times each. Hence all multiplicities y_A ≤ 2 and
e(H, Z) = Σ_A y_A c_A ≤ 2 Σ_A c_A ≤ 2m. ∎ (RA9X7: of the 38,760 multisets of six 4-subsets of a 6-set, 130 satisfy the
3-set rule; all have all frequencies 4 and multiplicities ≤ 2.)

**4g.3.4 s = 8: 55, 56, 57 are impossible (PROVED).** h = 6, n_6 = 0, m ≤ 5, and 6 = s − 2 ≤ k ≤ 6: k = 6. The 12-set
H ∪ Z spans e(H, Z) ≤ 2m ≤ 10 < 12 edges (4g.3.3). ∎

**4g.3.5 s = 7: 59–64 are impossible (PROVED).** h = 7, m ≤ 6, k ∈ {5, 6}; the 12-sets are H ∪ Y with |Y| = 5.
* k = 6: each of the six 5-subsets Y of Z gives e(H, Y) ≥ 12, and each Z-vertex lies in five of them, so
  5 e(H, Z) ≥ 72 and e(H, Z) ≥ 15. But e(H, Z) ≤ 2m ≤ 12 (4g.3.3).
* k = 5 = s − 2: 4g.3.2 applies, and H ∪ Z is a 12-set, so e(H, Z) ≥ 12. The multiplicity patterns of five masks are
  (5), (4,1), (3,2), (3,1,1), (2,2,1), (2,1,1,1), (1^5). The first five are excluded by 4g.3.2 (a type ≥ 4 times; a
  tripled type with another vertex; two doubled types). (1^5): e(H, Z) = Σ c_A ≤ m ≤ 6. (2,1,1,1) with doubled type A:
  e(H, Z) = c_A + Σ_{types} c ≤ 4 + m ≤ 10. Both < 12. ∎

**4g.3.6 s = 6: 65–72 are impossible (PROVED; k = 5 by RA9X7's repair).** h = 8, m ≤ 7, k ∈ {4, 5, 6}; the 12-sets are
H ∪ Y with |Y| = 4.
* k = 6 (only if n_6 = 0): each Z-vertex lies in C(5,3) = 10 of the C(6,4) = 15 four-subsets, so 10 e(H, Z) ≥ 180 and
  e(H, Z) ≥ 18; but e(H, Z) ≤ 2m ≤ 14 (4g.3.3).
* k = 5 (n_6 ≤ 1). Here k = s − 1: only one a = 4 vertex lies outside Z, so 4g.3.2 is **not** available (ChatGPT's
  draft used it here; this is the gap RA9X7 found). Instead:
  (i) No pair J = {i, j} lies in all five Z-masks: otherwise the 12-set (I ∖ J) ∪ Z (Z independent) spans 5·2 = 10
  edges. If Z has at most two distinct types, its masks do have a common pair (two distinct 4-subsets of N share ≥ 2
  elements, and one type contains pairs trivially); so the patterns (5), (4,1), (3,2) are impossible.
  (ii) In each remaining pattern (1^5), (2,1,1,1), (2,2,1), (3,1,1) there is a 4-subset Y ⊆ Z with at most one type
  doubled and none tripled (drop any vertex; drop a singleton; drop one copy of a doubled type; drop one copy of the
  tripled type, respectively). For it e(H, Y) = Σ_A y_A c_A ≤ Σ_A c_A + max_A c_A ≤ m + 4 ≤ 11 < 12.
  (RA9X7's repair phrases (i) for "a type four times" with a case distinction on the fifth mask B; since all Z-masks
  lie in the 6-set N, B always contains a pair of A, so only the 10-edge branch occurs. RA9X7's model check finds 0
  survivors for s = 6, k = 5 even without any vertex outside Z.)
* k = 4 = s − 2 (the only possibility for 68, 71): 4g.3.2 applies and Y = Z, so e(H, Z) ≥ 12. Patterns (4), (3,1),
  (2,2) have at most two types, hence a pair common to all four masks (as in (i)): excluded by 4g.3.2. (1^4):
  e(H, Z) ≤ m ≤ 7; (2,1,1) with doubled A: e(H, Z) ≤ c_A + m ≤ 11. Both < 12. ∎

**Dependencies of 4g.3:** (F1), (F2), (S1), (S6), (S8), (P4)/(P5) (for n_2 = n_7 = 0), the isolation of a = 9 vertices
in G[O] ((P11)), Theorem 1 (4b.2), the 12-set condition. Not used: 4f.1, the enumerated lemma C9, any SAT result.
RA9X7's end-to-end model check (caseA_onea3_out.txt: all Z multisets up to S_9, all masks of p, q, every 12-set
(I ∖ J) ∪ S, all capacity vectors) has 0 survivors for every s, k; without p, q its only survivors are the patterns
4g.3.2 handles (s = 7, k = 5: (3,1,1), (2,2,1); s = 6, k = 4: (4), (3,1), (2,2)).

**Status ledger after 4g (reporting only; level-32 list minus 4g.3; not SAT certificates; not a `profile_ok` level;
superseded by the ledger after 4h).**

| Case | open profiles (v1 indices) | count | basis |
|---|---|---|---|
| A | 84 (4^14,9), 85 (4^13,5,9), 86 (4^13,9^2), 87 (4^12,5^2,9), 88 (4^12,5,9^2), 90 (4^11,5^3,9), 91 (4^11,5^2,9^2), 94 (4^10,5^4,9), 95 (4^10,5^3,9^2), 98 (4^9,5^5,9), 99 (4^9,5^4,9^2), 101 (4^8,5^6,9), 102 (4^8,5^5,9^2), 104 (4^7,5^7,9), 105 (4^7,5^6,9^2) — the 15 pure 4/5/9 profiles | 15 | level 32 (4f) minus 55–57, 59–72 (4g.3) [hand-proof reviewed] |
| B | B16 4^15, B17 4^14 5, B18 4^13 5^2, B19 4^12 5^3 — G[O] bipartite (4f.1), 8 + 7 split only (4g.2) | 4 | level 32 (4f) + 4g.2 [hand-proof reviewed] |

Excluded by 4g: Case A v1 55, 56, 57, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72 (17 profiles, 4g.3);
Case B none. "[hand-proof reviewed]" means the hand proofs were checked by RA9X7 (with the repair above); these
exclusions are not SAT certificates and change nothing in the certified list, the CNF, the checker or the
production run, which remain the only basis of the final claim (section 7). No order-24 theorem is claimed.

## 4h. ChatGPT round 9 (part 1), reviewed by RA9X9 with two repairs

Source: ChatGPT round 9, part 1 (closure_drafts/reviews/gpt/round9_part1_condensed.md), reviewed by RA9X9
(review_RA9X9/REPORT.md: claim (2) accepted; claims (1), (3) accepted with Repair A (M1 for every pure Case A
profile); claim (4) accepted with Repair B (a tripled low mask is impossible); status [hand-proof reviewed]). Proofs
in my own words. **This write-up was checked by RA9X11: all subsections ACCEPT; the 4h.5 scope-sentence repair and the 4h.2 clarification are applied (review_RA9X11/).** **Status: reporting only.** No `profile_ok`
level and no predicate are added; the certified list (section 4, version 2: 131 + 299; its sha256 values unchanged),
`a9core.py`, the CNF and the production run are unchanged. Nothing here is a SAT certificate, and no order-24 theorem
is claimed. Profile numbers are version-1 indices (archive_v1/).
Supporting evidence (not part of the proofs): RA9X9's standard-library scripts in review_RA9X9/ — small_checks.py
(small_checks_out.txt, "ALL OK": the multisets of five and of four 4-subsets of a 5-set allowed by q4 ≤ 3, the 21 masks
addable to the five 4-subsets of a 5-set, the "disjoint from ≤ 1 of y1..y4" check, the bound table of 4h.2, the
averaging numbers of 4h.2 and 4h.3, the 45 masks addable to a tripled mask), model_4_13_9_2.py
(model_4_13_9_2_out.txt: end-to-end model check of 4^13 9^2, see 4h.6) and diag.py (diag_out.txt: negative control).

**Setting and notation (all of 4h).** Case A, D = 9, pure profile 4^s 5^m 9^t with s + m + t = 15. On the level-32
list (4f) these are the 15 profiles with t ∈ {1, 2}:
t = 1 (s = 14 − m, m = 0, …, 7): 84 (4^14,9), 85 (4^13,5,9), 87 (4^12,5^2,9), 90 (4^11,5^3,9), 94 (4^10,5^4,9),
98 (4^9,5^5,9), 101 (4^8,5^6,9), 104 (4^7,5^7,9);
t = 2 (s = 13 − m, m = 0, …, 6): 86 (4^13,9^2), 88 (4^12,5,9^2), 91 (4^11,5^2,9^2), 95 (4^10,5^3,9^2),
99 (4^9,5^4,9^2), 102 (4^8,5^5,9^2), 105 (4^7,5^6,9^2).
(|H| = m + t ≤ 8 because |H| = 9 is excluded by 4d; t = 3 is excluded by 4e.9, 4f.4, 4d.5; t ≤ 3 by (P11).) So s ≥ 7.
L = the s low vertices (a = 4), H5 = the m vertices with a = 5, Z = the t vertices with a = 9 (v among them), and
q4_ij = #{x ∈ L : {i, j} ⊆ N_I(x)}. Facts used throughout: the vertices of Z have no neighbour in O (see (P11)); H is
independent (S1), so H5 ∪ Z is independent; by Theorem 1 (4b.2) two low vertices are adjacent iff their masks are
disjoint, and an a = 5 vertex of mask P is adjacent exactly to the low vertices of mask I ∖ P (a 4-set disjoint from a
5-set is its complement). In particular copies of one low mask are pairwise non-adjacent twins (same neighbourhood),
and **all neighbours of an a = 5 vertex are copies of one low mask**. A low vertex has outside degree ≤ 9 − 4 = 5.

**4h.1 Lemma M1 in pure Case A: q4_ij ≤ 3 for all i ≠ j; in particular every 4-mask occurs at most 3 times in L
(PROVED; Repair A of RA9X9; uses (F1), (S1), the isolation of Z, α = 9, the 12-set condition).**
Proof. Fix i ≠ j and put R = I ∖ {i, j} (7 elements). Low vertices whose masks contain {i, j} have meeting masks, so
they are pairwise non-adjacent (F1), and each mask has exactly 2 elements in R. If there are five of them, they and R
form a 12-set with 5·2 = 10 edges (I is independent): impossible. Suppose there are exactly four, Y. Let x ∈ O ∖ Y
and consider the 12-set S = R ∪ Y ∪ {x}: Y contributes 8 edges (to R), x contributes |N_I(x) ∩ R| edges to R and
e(x, Y) edges to Y.
* If x ∈ L and N_I(x) meets {i, j}: N_I(x) meets every Y-mask, so e(x, Y) = 0 (F1), and |N_I(x) ∩ R| ≤ 3: e(S) ≤ 11.
* If a_x = 5 and N_I(x) ⊇ {i, j}: again e(x, Y) = 0 and |N_I(x) ∩ R| = 3: e(S) = 11.
Both contradict the 12-set condition. Hence the s − 4 low vertices outside Y have masks inside the 7-set R, and every
a = 5 mask contains at most one of i, j, so it has ≥ 4 elements in R. Two 4-subsets of a 7-set meet, and a set with ≥ 4
elements of R meets every 4-subset of R; so by (F1) these s − 4 low vertices and the m vertices of H5 are pairwise
non-adjacent (H5 is independent by (S1)). Adding Z (no neighbours in O, and independent) gives an independent set of
size (s − 4) + m + t = 11 > 9: against α = 9. So q4_ij ≤ 3, and a mask occurring 4 times would give q4_ij ≥ 4. ∎
(This extends "M1 in Case A" of 4d, which was stated for |H| = 9, to every pure Case A profile; the a = 9 vertices are
needed only in the final independent set. Every subfamily of the low masks is then admissible in the sense of 4f.1.)

**4h.2 F is bipartite for all 15 pure profiles (PROVED, conditional on the enumerated lemma 4f.1).** Let
F = G[O ∖ Z] = G[L ∪ H5], n := |F| = 15 − t. Then:
(i) α(F) ≤ 9 − t (an independent set of F together with Z is independent in G);
(ii) every (12 − t)-subset S of F spans ≥ 12 edges (S ∪ Z is a 12-set, and its edges are those of S, since Z has no
neighbour in O and is independent);
(iii) averaging (ii) over all (12 − t)-subsets (each edge lies in a fraction (12 − t)(11 − t)/(n(n − 1)) of them):
e(F) ≥ 12·14·13/(11·10) = 1092/55 ≈ 19.85 for t = 1 and e(F) ≥ 12·13·12/(10·9) = 104/5 = 20.8 for t = 2, i.e.
**e(F) ≥ 20 (t = 1) and e(F) ≥ 21 (t = 2)**.
Proof of bipartiteness. Suppose F has an odd cycle, and let C be a shortest one; F is triangle-free, so |C| ≥ 5, and C
has no chord.
* *C contains no a = 5 vertex.* If h ∈ C has a = 5, its two cycle-neighbours u, w are copies of one low mask, hence
  twins. Let w' be the other cycle-neighbour of w; then u ~ w', and replacing the path u, h, w, w' of C by the edge uw'
  gives a closed walk of odd length |C| − 2, which contains an odd cycle shorter than C.
* *The masks on C are distinct.* If u ≠ w on C have equal masks, they are non-adjacent twins at cycle distance d ≥ 2,
  splitting C into arcs of lengths d and |C| − d, one of them odd. Following the arc of length d from u to the
  cycle-neighbour w− of w on that arc, and closing with the edge w−u (w− ~ w, hence w− ~ u), gives a cycle of length d;
  likewise the other arc gives a cycle of length |C| − d. One of them is odd and shorter than C. (The odd one has length ≥ 3, so it is a genuine cycle.)
* *|C| = 9.* By Theorem 1, consecutive masks along C are disjoint, so C is a closed walk of odd length in the
  disjointness graph of 4-subsets of I, which has odd girth ≥ 9 (4b.11): |C| ≥ 9. If |C| ≥ 11, ten consecutive
  vertices of C form a path of 10 distinct masks with consecutive masks disjoint; the family is admissible (q4 ≤ 3) by
  4h.1, against 4f.1(a) (by symmetry its first edge may be taken to be (A, B) = ({0,1,2,3}, {4,5,6,7})).
* *C is an isolated component of G[L].* C is an admissible 9-cycle of distinct masks. A low vertex x ∉ C with the mask
  of a cycle vertex would give an admissible family consisting of the cycle and a second copy of one of its masks,
  against 4f.1(d); a low vertex x ∉ C with a new mask adjacent to a vertex of C would give an admissible family
  consisting of the cycle and a further adjacent mask, against 4f.1(c) (in both cases the family is a subfamily of the
  low masks, admissible by 4h.1). So no other low vertex is adjacent to C and none repeats a cycle mask.
Hence s ≥ 9, and with r := s − 9: e(L) = 9 + e(L ∖ C) ≤ 9 + ⌊r²/4⌋ (Mantel; L ∖ C is triangle-free). There are no edges
inside H5 (S1) and none at Z. An a = 5 vertex h of mask P has as neighbours exactly the copies of I ∖ P: if I ∖ P is a
cycle mask, it occurs only once in L (by 4f.1(d), as above), so d(h) ≤ 1; otherwise all copies lie in L ∖ C, so
d(h) ≤ r. Therefore
  **e(F) ≤ 9 + ⌊r²/4⌋ + m·max(1, r).**
Bound table (s = 15 − t − m, r = s − 9; recomputed here and in RA9X9's small_checks_out.txt, item (5)):

| t | need e(F) ≥ | m = 0 | m = 1 | m = 2 | m = 3 | m = 4 | m = 5 |
|---|---|---|---|---|---|---|---|
| 2 | 21 | r = 4: 9 + 4 + 0 = 13 | r = 3: 9 + 2 + 3 = 14 | r = 2: 9 + 1 + 4 = 14 | r = 1: 9 + 0 + 3 = 12 | r = 0: 9 + 0 + 4 = 13 | s = 8 < 9 |
| 1 | 20 | r = 5: 9 + 6 + 0 = 15 | r = 4: 9 + 4 + 4 = 17 | r = 3: 9 + 2 + 6 = 17 | r = 2: 9 + 1 + 6 = 16 | r = 1: 9 + 0 + 4 = 13 | r = 0: 9 + 0 + 5 = 14 |

Every bound is below the requirement of (iii) (largest: 14 < 21 for t = 2, 17 < 20 for t = 1). For t = 2, m ≥ 5 and
t = 1, m ≥ 6 we have s ≤ 8 < 9, so no odd cycle exists at all. Hence **F has no odd cycle: F is bipartite** for all 15
profiles. ∎
(As ChatGPT notes, this uses the pair-incidence condition q4 ≤ 3 through 4f.1, not odd girth alone. RA9X9's note on
the bound: the complementary low type of an a = 5 vertex can lie on the cycle only as a single copy, by 4f.1(d), which
is the "1" in max(1, r).) Since both classes of a bipartition of F are independent in G together with Z, they have at
most 9 − t vertices: for t = 1 the classes have sizes {7, 7} or {6, 8}; for t = 2 see 4h.3.

**4h.3 t = 2: class sizes 6 + 7 and e(F) ≥ 24 (PROVED, given 4h.2).** Let t = 2 (|F| = 13) and let X ⊔ Y be a
bipartition of F. Both classes are independent, so |X|, |Y| ≤ 7 by 4h.2(i), and |X| + |Y| = 13: the sizes are 6 and 7;
let |X| = 6, |Y| = 7. For U ⊆ X with |U| = 3, Y ∪ U is a 10-subset of F; X and Y are independent, so every F-neighbour
of a vertex of U lies in Y and e(Y ∪ U) = Σ_{u∈U} d_F(u). By 4h.2(ii), **Σ_{u∈U} d_F(u) ≥ 12 for every 3-set U ⊆ X.**
Summing over the C(6, 3) = 20 triples, each vertex of X lies in C(5, 2) = 10 of them: 10·Σ_{x∈X} d_F(x) ≥ 240, so
**e(F) = Σ_{x∈X} d_F(x) ≥ 24.** ∎

**4h.4 Degree-five saturation (PROVED; uses 4h.1, Theorem 1, (F1)).** In a pure profile, let x ∈ L have mask A and
five low neighbours, and put C = I ∖ A (5 elements). Then the five neighbour masks are exactly the five 4-subsets of C,
and all low vertices other than these five are pairwise non-adjacent.
Proof. A neighbour mask is disjoint from A, i.e. a 4-subset of C; it omits exactly one element of C. For e ∈ C let
n_e = number of the five neighbours whose mask omits e; Σ_{e∈C} n_e = 5. For a pair {i, j} ⊆ C, the neighbour masks
containing both i and j are those omitting neither: 5 − n_i − n_j of them, so 5 − n_i − n_j ≤ q4_ij ≤ 3 (4h.1), i.e.
n_i + n_j ≥ 2 for all i ≠ j in C. If some n_e = 0, the four other values are ≥ 2 and Σ n_e ≥ 8 > 5. So every n_e ≥ 1,
and Σ n_e = 5 forces n_e = 1 for all e: the five masks are distinct and are the five 4-subsets of C. Each pair in C then
lies in exactly 3 of them, so q4_ij = 3 by 4h.1 and no further low mask contains a pair of C: every low vertex w other
than the five neighbours has |N_I(w) ∩ C| ≤ 1, hence |N_I(w) ∩ A| ≥ 3. Two such masks have ≥ 3 elements each in the
4-set A, so they meet, and the vertices are non-adjacent (F1). ∎
(RA9X9: of the 126 multisets of five 4-subsets of a 5-set only the five distinct subsets satisfy q4 ≤ 3; 21 masks can be
added to them keeping q4 ≤ 3, each meets C in ≤ 1 element, and they pairwise meet.)
**Consequence for 4^13 9^2 (v1 86).** Here F = G[L] (m = 0), so every F-neighbour of a low vertex is low, and its
outside degree is ≤ 5: **degree 5 is the only case above 4**. If x had degree 5, the s − 5 = 8 low vertices other than
its five neighbours (x among them) would be pairwise non-adjacent, and with the two a = 9 vertices they would form an
independent 10-set. Hence **every vertex of F has degree ≤ 4** in 4^13 9^2.
(Observation, not used, not part of RA9X9's review: the same count gives s − 5 + t = 10 for 4^14 9 (v1 84), so there
too every vertex of F has degree ≤ 4. For m ≥ 1 the lemma alone gives no contradiction, since s − 5 + t ≤ 9.)

**4h.5 No tripled low mask when s + t ≥ 13; in particular multiplicity ≤ 2 in 4^13 9^2 (PROVED; Repair B of RA9X9,
an M2-style argument; uses 4h.1, (F1), the isolation of Z).** Let A occur three times in L. Every pair inside A lies in
the three copies, so q4 = 3 on these pairs (4h.1) and no other low mask contains a pair of A: every other low vertex w
has |N_I(w) ∩ A| ≤ 1, hence ≥ 3 elements of its mask in the 5-set I ∖ A. Two such masks meet (3 + 3 > 5), so the other
s − 3 low vertices are pairwise non-adjacent (F1), and with Z they form an independent set of size s − 3 + t. This is
≥ 10 > 9 as soon as s + t ≥ 13. ∎
Scope. s + t ≥ 13 holds for t = 2 exactly when m ≤ 2 (v1 86, 88, 91) and for t = 1 exactly when m ≤ 2 (v1 84, 85, 87).
RA9X9 reviewed the instance 4^13 9^2 (the other 10 low vertices and the two a = 9 vertices: an independent 12-set;
its script finds 45 masks addable to a tripled mask under q4 ≤ 3, all meeting A in ≤ 1 element and pairwise meeting).
**For m ≥ 3 (t = 1: v1 90, 94, 98, 101, 104; t = 2: v1 95, 99, 102, 105) multiplicity ≤ 2 is not proved here** (the count gives only s − 3 + t = 12 − m ≤ 9, and the a = 5 vertices cannot simply be added, since they may be adjacent to low vertices of the complementary mask; repair by RA9X11);
it is not needed in this section, whose only application is 4h.6.

**4h.6 v1 86 = (4^13, 9^2) is impossible (PROVED; given 4h.2 (hence 4f.1), 4h.3, 4h.4, 4h.5).** Here F = G[L], 13 low
vertices. By 4h.2 F is bipartite, by 4h.3 its classes X, Y have sizes 6, 7 and Σ_{x∈X} d(x) = e(F) ≥ 24, and by 4h.4
every degree is ≤ 4. So Σ_{x∈X} d(x) ≤ 24, hence = 24, and **every x ∈ X has degree exactly 4**.
(a) Fix x ∈ X with mask A and neighbours y1, …, y4 ∈ Y; put C = I ∖ A. Their masks are 4-subsets of C and are
distinct: with n_e as in 4h.4 (now Σ_{e∈C} n_e = 4), a pair {i, j} ⊆ C lies in 4 − n_i − n_j of them, and q4_ij ≤ 3
gives n_i + n_j ≥ 1, so at most one n_e is 0; five values with sum 4 and at most one zero are 1, 1, 1, 1, 0, so the
four masks omit four different elements of C. (RA9X9: of the 70 multisets of four 4-subsets of a 5-set, the 5 that
satisfy q4 ≤ 3 all consist of distinct subsets.)
(b) Let x' ∈ X have mask B ≠ A. Then B is disjoint from at most one of the masks of y1, …, y4: two distinct 4-subsets
of the 5-set C have union C, so a 4-set disjoint from both lies in I ∖ C = A and equals A. By Theorem 1, x' has at most
one neighbour among y1, …, y4; since d(x') = 4 and |Y ∖ {y1, …, y4}| = 3, x' is adjacent to all three vertices
w1, w2, w3 of Y ∖ {y1, …, y4}. (Vertices of X with mask A are copies of x.)
(c) Suppose X contains x', x'' with distinct masks B, B'', both ≠ A. By (b) each of w1, w2, w3 has a mask disjoint from
B and from B''. |B ∪ B''| ≥ 5, so at most one 4-set avoids B ∪ B'': w1, w2, w3 have the same mask, which then occurs
three times in L, against 4h.5 (s + t = 15 ≥ 13). Hence X carries at most two masks, A and possibly one other, each
occurring at most twice (4h.5): |X| ≤ 4 < 6. Contradiction. ∎
(Compared with ChatGPT's step 4: distinctness in (a) is proved by the omission count instead of the pair-incidence
estimate; the "each 4-mask at most twice" bound that ChatGPT called "previously proved" is 4h.5, which was not
previously available in this profile — this is Repair B.)
RA9X9's end-to-end model check of 4^13 9^2 (model_4_13_9_2_out.txt), assuming only Theorem 1, isolated a = 9
vertices, a bipartite F with classes 6 + 7, degrees ≤ 5, q4 ≤ 3 and multiplicity ≤ 3 (so neither 4h.4 nor 4h.5), finds
0 survivors (9,044 Y-sets, 69,412 X-sets); the negative control without the q4/multiplicity filters (diag_out.txt)
leaves 1,212 configurations passing all F-level checks, so the search is not vacuous and M1 is essential. These are
supporting evidence only, not part of the proof.

**Dependencies of 4h.** (F1), (S1), (R3) (degree ≤ 9), α = 9, the 12-set condition, the isolation of the a = 9 vertices
in G[O] ((P11)), Theorem 1 (4b.2), the odd-girth statement of 4b.11, the exclusions 4d (|H| = 9) and 4d.5, 4e.9, 4f.4
(t = 3) only for the list of profiles, and — for 4h.2, hence 4h.3 and 4h.6 — the enumerated finite lemma 4f.1 (a), (c),
(d) (review_RA9X6/c9lemma.py). 4h.1, 4h.4 and 4h.5 do not use 4f.1. Not used: any SAT result, the certified list, (P7),
(P8).

**Status ledger after 4h (reporting only; supersedes the ledger after 4g; superseded by the ledger after 4i; not SAT
certificates; not a `profile_ok` level).**

| Case | open profiles (v1 indices) | count | basis |
|---|---|---|---|
| A | 84 (4^14,9), 85 (4^13,5,9), 87 (4^12,5^2,9), 88 (4^12,5,9^2), 90 (4^11,5^3,9), 91 (4^11,5^2,9^2), 94 (4^10,5^4,9), 95 (4^10,5^3,9^2), 98 (4^9,5^5,9), 99 (4^9,5^4,9^2), 101 (4^8,5^6,9), 102 (4^8,5^5,9^2), 104 (4^7,5^7,9), 105 (4^7,5^6,9^2) — pure 4/5/9 profiles; F bipartite (4h.2, conditional on 4f.1); for t = 2 classes 6 + 7 and e(F) ≥ 24 (4h.3) | 14 | ledger after 4g minus 86 (4h.6) [hand-proof reviewed] |
| B | B16 4^15, B17 4^14 5, B18 4^13 5^2, B19 4^12 5^3 — G[O] bipartite (4f.1), 8 + 7 split only (4g.2) | 4 | unchanged from the ledger after 4g [hand-proof reviewed] |

Excluded by 4h: Case A v1 86 (4^13, 9^2); Case B none. "[hand-proof reviewed]" means the hand proofs were checked by
RA9X9 (with Repairs A and B); this write-up of them awaits a separate check. These exclusions are not SAT certificates
and change nothing in the certified list, `a9core.py`, the CNF, the checker or the production run, which remain the
only basis of the final claim (section 7). No order-24 theorem is claimed.

## 4i. ChatGPT round 9 (part 2), reviewed by RA9X10 with repairs

Source: ChatGPT round 9, part 2 (closure_drafts/reviews/gpt/round9_part2_condensed.md, its sections 5–11), reviewed by
RA9X10 (review_RA9X10/REPORT.md: the lemmas of section 5 accepted; m = 1 (section 6) accepted with a wording repair;
m = 2 (section 7) accepted; m = 3 (section 8) accepted with three repairs (steps (a) and (b) rewritten; in (c) the choice of A, B specified); m = 4 (section 9) accepted; m = 5
(section 10) accepted under the reading given there; m = 6 (section 11) accepted, with a shorter proof; status
[hand-proof reviewed]). Proofs in my own words; where RA9X10 repaired or re-read a step, the repaired version is the
one written here. **This write-up was checked by RA9X14: all subsections ACCEPT; header wording repair applied (review_RA9X14/).** **Status: reporting only.**
No `profile_ok` level and no predicate are added; the certified list (section 4, version 2: 131 + 299; its sha256
values unchanged), `a9core.py`, the CNF and the production run are unchanged. Nothing here is a SAT certificate, and
no order-24 theorem is claimed. Profile numbers are version-1 indices (archive_v1/).

**4i.1 Setting (PROVED, given 4h).** The profiles are 4^(13−m) 5^m 9^2 for m = 1, …, 6: v1 88 (m = 1), 91 (m = 2),
95 (m = 3), 99 (m = 4), 102 (m = 5), 105 (m = 6); m = 0 is v1 86, excluded in 4h.6. Notation of 4h with t = 2:
s = 13 − m low vertices (L, a = 4), the m vertices H5 with a = 5 ("highs" in this section), the two a = 9 vertices Z,
F = G[L ∪ H5] with |F| = 13, d = d_F. A vertex of Z has no neighbour in O, so d_F(x) = d_O(x) for x ∈ F.
(a) *Classes.* F is bipartite (4h.2, conditional on the enumerated lemma 4f.1), and every bipartition has classes of
sizes 6 and 7 (4h.3). Fix one, X ⊔ Y with |X| = 6, |Y| = 7. Both classes are independent, so every edge of F joins X
to Y and **e(F) = Σ_{x∈X} d(x) = Σ_{y∈Y} d(y)**.
(b) *3-sum rule* (4h.3): **Σ_{u∈U} d(u) ≥ 12 for every 3-set U ⊆ X**, and **e(F) ≥ 24**.
(c) *Types and adjacency.* The type of a low vertex is its mask. By Theorem 1 (4b.2) two low vertices are adjacent iff
their types are disjoint. A high h with mask P is adjacent exactly to the low vertices of type I ∖ P (a 4-set disjoint
from the 5-set P is its complement; conversely Theorem 1), and to nothing else in O (H is independent (S1); Z has no
O-neighbour). We say h *matches* the type I ∖ P; every high matches exactly one type (which need not occur). For a
4-set A let μ(A) = number of low vertices of type A (its multiplicity) and c_A = number of highs matching A, so
Σ_A c_A = m. Then for a low vertex x of type A, **d(x) = d_L(x) + c_A**, where d_L(x) is its number of low neighbours;
and for a high h matching A, **d(h) = μ(A)** (all copies of A are its neighbours, and nothing else is).
(d) *Twins.* By (c), copies of one type have the same neighbourhood in F, and every vertex of X has degree ≥ 2 (by
(f1) below), so its copies share a neighbour (in Y) and lie in X as well: **for a type occurring in X, all its copies
lie in X, and all its matching highs lie in Y** (a matching high is adjacent to the copies). In particular, for a low
x ∈ X of type A, c_A counts highs in Y only. Every count below counts vertices, with copies counted separately; RA9X10
re-derived each capacity count in this form ("twin checks").
(e) *Multiplicity bounds.* μ(A) ≤ 3 for every 4-set A (M1, 4h.1). For m ≤ 2 we have s + t = 15 − m ≥ 13, so 4h.5
gives **μ(A) ≤ 2 for m ≤ 2**. For m ≥ 3 only **μ(A) ≤ 3** is available (4h.5, scope), and the arguments of 4i.5–4i.8
use only that bound, treating tripled types explicitly. Consequently **d(h) ≤ 3 for every high (≤ 2 when m ≤ 2)**, and
**d(x) ≤ 5 for every low x** (outside degree ≤ 9 − 4).
(f) *Degree consequences of (b).* All degrees are ≤ 5.
(f1) d(x) ≥ 2 for x ∈ X (otherwise x and any two others sum ≤ 1 + 5 + 5 = 11).
(f2) At most one vertex of X has degree ≤ 3 (3 + 3 + 5 = 11).
(f3) If x0 ∈ X has d(x0) ≤ 3, any two of the other five vertices of X have degree sum ≥ 9, so at most one of them has
degree ≤ 4: **at least four of them have degree 5**. If d(x0) ≤ 2, any two of the others sum ≥ 10: **all five have
degree 5**.
(f4) *Degree concentration:* **|X ∩ H5| ≤ 1**, since a high has degree ≤ 3 by (e) and two of them would contradict (f2)
(3 + 3 + 5 = 11).
(g) *Two compositions.* By (f4) either **(I)** X consists of six low vertices and Y of the m highs and 7 − m low
vertices, or **(II)** X consists of one high h0 and five low vertices and Y of m − 1 highs and 8 − m low vertices; in
(II), d(h0) ≤ 3 (≤ 2 for m ≤ 2), so (f3) applies to x0 = h0. Write ℓ_Y = |Y ∩ L| (7 − m in (I), 8 − m in (II)); all
low neighbours of a vertex of X lie in Y ∩ L.
(h) *Capacity of Y:* by (c), (e), **Σ_{y∈Y} d(y) ≤ 5 ℓ_Y + 3 |Y ∩ H5|**.

**4i.2 Lemmas (PROVED; use 4h.1, 4h.4, Theorem 1, (F1)).**
* **(L1) Distinct star masks.** If a low vertex x of type A has k ≥ 4 low neighbours, their types are k distinct 4-subsets
  of C = I ∖ A. Proof. Their types are disjoint from A, i.e. 4-subsets of the 5-set C; k ≤ 5 by (e). For k = 5 this is
  4h.4. For k = 4, let n_e (e ∈ C) be the number of the four types omitting e, so Σ_e n_e = 4; a pair {i, j} ⊆ C lies
  in 4 − n_i − n_j of them, and q4_ij ≤ 3 (4h.1) gives n_i + n_j ≥ 1, so at most one n_e is 0; five non-negative
  integers with sum 4 and at most one zero are 1, 1, 1, 1, 0, so the four types omit different elements (as in
  4h.6(a)). ∎
* **(L2) Two distinct 4-sets.** If M ≠ M' are 4-sets, |M ∪ M'| ≥ 5, so at most one 4-set is disjoint from both. ∎
* **(L3) Dense stars.** Let x, x' be low vertices, x with ≥ 4 low neighbours, and suppose x and x' have at least two
  low neighbours in common. Then x and x' have the same type. Proof. The two common neighbours have distinct types
  (L1, applied to x); type(x) and type(x') are both disjoint from both, so they coincide by (L2). ∎
  Used with pigeonhole: if x, x' ∈ X have d_L(x) ≥ 4 and d_L(x) + d_L(x') ≥ ℓ_Y + 2, they share ≥ 2 low neighbours
  (inside Y ∩ L) and have the same type.
* **(L4) Related types.** Let A ≠ B be types occurring in X with μ(A) + μ(B) ≥ 4. Then |A ∩ B| = 1, no 4-set is
  disjoint from both, and **no vertex of F is adjacent both to the copies of A and to the copies of B**. Writing d_L(A)
  for the common number of low neighbours of the copies of A, **d_L(A) + d_L(B) ≤ ℓ_Y**. Proof. If |A ∩ B| ≥ 2, a pair
  inside A ∩ B lies in ≥ 4 low masks, against 4h.1. If A ∩ B = ∅, the copies of A and of B are adjacent (Theorem 1),
  inside the independent class X. So |A ∩ B| = 1, |A ∪ B| = 7, and a 4-set disjoint from both would lie in a 2-set. A
  low vertex adjacent to copies of both would have such a mask; a high matches one type only. The low neighbours of the
  copies of A and of B are therefore disjoint subsets of Y ∩ L. ∎
* **(L5)** If two distinct types A, B are both disjoint from one 4-set M, then A, B ⊆ I ∖ M (5 elements), so
  |A ∩ B| ≥ 3. ∎
RA9X10 checked (L1) (the q4-admissible multisets of four and five 4-subsets of a 5-set consist of distinct sets),
(L2), (L4) and (L5) by enumeration (review_RA9X10/small_checks_out.txt, items (1)–(5), "ALL OK"). The degree
concentration (f4) is ChatGPT's "3 + 3 + 5 = 11".

**4i.3 m = 1: v1 88 = (4^12, 5, 9^2) is impossible (PROVED; repaired wording of ChatGPT section 6).** μ ≤ 2, so the
high h has d(h) ≤ 2 (4i.1(e)).
* (II), h ∈ X. By (f3) the five low vertices of X have degree 5. Y = 7 low vertices; h is in X, so these five have no
  high neighbour and d_L = 5, all inside the 7 vertices of Y. Any two of them share ≥ 5 + 5 − 7 = 3 low neighbours, so
  by (L3) all five have one type: μ ≥ 5 > 2. (ChatGPT wrote "≤ 6 low vertices" for the opposite class; it has 7, and
  the count still works: RA9X10's repair.)
* (I), h ∈ Y. Y ∩ L has 6 vertices. By (f2) at least five vertices of X have degree ≥ 4; h is adjacent to at most two
  vertices of X, so at least three vertices of X have degree ≥ 4 and no high neighbour, hence d_L ≥ 4 inside the six
  low vertices of Y. Any two share ≥ 4 + 4 − 6 = 2, so by (L3) these three have one type: μ ≥ 3 > 2. ∎

**4i.4 m = 2: v1 91 = (4^11, 5^2, 9^2) is impossible (PROVED; ChatGPT section 7).** μ ≤ 2 and d(h) ≤ 2 for both highs.
* (II), h0 ∈ X, the other high h1 ∈ Y, ℓ_Y = 6. By (f3) the five low vertices of X have degree 5; h1 is adjacent to at
  most two of them, so at least three have d_L = 5 inside the 6 low vertices of Y; two of them share ≥ 4, so by (L3)
  the three have one type: μ ≥ 3 > 2.
* (I), both highs h1, h2 ∈ Y, X = six low vertices, ℓ_Y = 5. Let W be the set of vertices of X of degree ≥ 4; |W| ≥ 5
  by (f2). A vertex of W without high neighbour has d_L ≥ 4 inside the five low vertices of Y; two such share ≥ 3, so
  they have one type (L3), and there are at most μ ≤ 2 of them. Hence at least three vertices of X have a high
  neighbour. Let r be the number of vertices of X with a high neighbour: 3 ≤ r ≤ d(h1) + d(h2) ≤ 4. If h1, h2 matched
  the same type A, then r = μ(A) ≤ 2; so they match distinct types A (of h1) and B (of h2), and the vertices of X with
  a high neighbour are exactly the copies of A and of B: r = μ(A) + μ(B).
  - r = 3, say μ(A) = 2, μ(B) = 1. The other three vertices of X have types outside {A, B} and no high neighbour; by
    (f2) at least two of them lie in W, and by the above they have one type C with μ(C) = 2. The sixth vertex has a
    type D ∉ {A, B, C} (each of A, B, C has all its copies already placed). A ≠ C and μ(A) + μ(C) = 4, so by (L4) each
    low y ∈ Y is adjacent to copies of at most one of A, C (≤ 2 edges), and to ≤ 1 copy of B and ≤ 1 copy of D:
    d(y) ≤ 4. Then e(F) = Σ_Y d ≤ 5·4 + d(h1) + d(h2) = 20 + 3 = 23 < 24.
  - r = 4: μ(A) = μ(B) = 2, and the other two vertices x_C, x_D of X have types C, D ∉ {A, B}. By (L4) each low y ∈ Y
    has ≤ 2 edges to the copies of A and B, and ≤ 2 more to x_C, x_D: d(y) ≤ 4, and e(F) ≤ 20 + 4 = 24. So e(F) = 24
    and every low y ∈ Y is adjacent to x_C and to x_D. If C ≠ D, every low vertex of Y has a type disjoint from C and
    D, which by (L2) is one and the same 4-set: μ ≥ 5. If C = D, then A, B, C are three doubled types in X, pairwise
    related by (L4), so each low y ∈ Y is adjacent to copies of at most one of them: d(y) ≤ 2 < 4. ∎

**4i.5 m = 3: v1 95 = (4^10, 5^3, 9^2) is impossible (PROVED; ChatGPT section 8 with RA9X10's rewritten steps).** Only
μ ≤ 3 is used; d(h) ≤ 3 for all highs.
* (II), h0 ∈ X, highs h1, h2 ∈ Y, ℓ_Y = 5. By (f3) the set D5 of degree-5 low vertices of X has |D5| ≥ 4.
  (a) h1, h2 match different types. Then every low vertex of X has at most one high neighbour (c_A ≤ 1 for every type
  A occurring in X; h0 ∈ X is not a neighbour), so every vertex of D5 has d_L ≥ 4 inside the five low vertices of Y.
  Two of them share ≥ 3, so by (L3) all of D5 has one type: μ ≥ 4, against M1. (ChatGPT's "exactly one high
  neighbour" was not justified; this replacement uses only "at most one". RA9X10 repair (a).)
  (b) h1, h2 match the same type A; then c_A = 2 and c_B = 0 for every other type B. If no vertex of D5 has type A,
  every vertex of D5 has d_L = 5, i.e. is adjacent to all five low vertices of Y; by (L3) all of D5 has one type,
  μ ≥ 4. Otherwise let x_A ∈ D5 have type A: d_L(x_A) = 5 − 2 = 3. Since μ(A) ≤ 3 < |D5|, some x' ∈ D5 has a type
  ≠ A; it has d_L(x') = 5, so it is adjacent to all low vertices of Y, including the three low neighbours of x_A. By
  (L3) (applied to x', which has 5 low neighbours) x_A and x' have the same type: contradiction. (RA9X10 repair (b).)
* (I), all three highs in Y, X = six low vertices, ℓ_Y = 4.
  (i) Suppose some x ∈ X, of type A, is adjacent to all four low vertices of Y. Their types are distinct (L1), so by
  (L3) a vertex of X of another type has at most one low neighbour. With a = μ(A) ≤ 3 (all copies in X, each with 4
  low neighbours): low–low edges ≤ 4a + (6 − a) = 6 + 3a ≤ 15, and high–low edges ≤ 3·3 = 9 (4i.1(e)). As e(F) ≥ 24,
  equality holds: a = 3, there are exactly 15 low–low edges, and every high has degree 3, i.e. matches a type with
  three copies, all in X. If all three highs match A, each of the three non-A vertices of X has no high neighbour and
  ≤ 1 low neighbour, so degree ≤ 1, against (f1). Otherwise some high matches a type B ≠ A with μ(B) = 3, so
  X = 3 copies of A + 3 copies of B; by (L4) no low vertex of Y is adjacent to copies of both, and since every low
  vertex of Y is adjacent to the copies of A, the copies of B have no low neighbour: low–low edges = 12 < 15.
  (ii) Hence every vertex of X has d_L ≤ 3. By (f2) at least five vertices of X have degree ≥ 4, and each of them has
  a high neighbour. Consider the types whose copies have degree ≥ 4 (copies are twins, so this is a property of the
  type); together they have ≥ 5 copies, each type has ≤ 3, so there are ≥ 2 such types; each has c ≥ 1, and
  Σ c ≤ 3, so there are ≤ 3 of them. Choose A, B among them with the two largest multiplicities: μ(A) + μ(B) ≥ 4 (with
  two types the sum is ≥ 5; with three types summing to ≥ 5, two largest summing to ≤ 3 would leave ≤ 1 for the third,
  total ≤ 4). By (L4), d_L(A) + d_L(B) ≤ 4. With d(A) = d_L(A) + c_A ≥ 4 and d(B) = d_L(B) + c_B ≥ 4:
  c_A + c_B ≥ 8 − 4 = 4 > 3 = m. Contradiction. (RA9X10 repair (c): ChatGPT's choice of A, B was not specified.) ∎

**4i.6 m = 4: v1 99 = (4^9, 5^4, 9^2) is impossible (PROVED; ChatGPT section 9).** μ ≤ 3; d(h) ≤ 3.
* (I), all four highs in Y, X = six low vertices, ℓ_Y = 3. The low vertices of Y contribute ≤ 15 to Σ_Y d ≥ 24, so the
  highs contribute ≥ 9; if no high had degree 3 they would contribute ≤ 4·2 = 8. So some high has degree 3: it matches
  a type A with μ(A) = 3, all three copies in X. They are twins, so by (f2) they do not have degree ≤ 3: they have
  degree ≥ 4. Among the other three vertices of X (types ≠ A) at most one has degree ≤ 3; let x_B, of type B ≠ A, have
  degree ≥ 4. μ(A) + μ(B) ≥ 4, so by (L4) d_L(A) + d_L(B) ≤ 3, and c_A + c_B ≥ (4 + 4) − 3 = 5 > 4 = m. Contradiction.
* (II), h0 ∈ X, three highs in Y, ℓ_Y = 4; |D5| ≥ 4 for the degree-5 low vertices of X (f3). A vertex of D5 has
  d_L ≤ 4, so its type has c ≥ 1.
  - If every vertex of D5 has exactly one high neighbour, each has d_L = 4, i.e. is adjacent to all four low vertices
    of Y; by (L3) all of D5 has one type, μ ≥ 4.
  - Otherwise some x_A ∈ D5 of type A has c_A ≥ 2. If c_A = 3, all three highs match A, the vertices of X with a high
    neighbour are the ≤ 3 copies of A, and D5 (≥ 4 vertices, all needing a high neighbour) cannot be covered. If
    c_A = 2, the third high matches one type B ≠ A, the vertices of D5 are copies of A or of B, and since μ(A) ≤ 3 some
    x_B ∈ D5 has type B, c_B = 1, d_L(x_B) = 4: x_B is adjacent to all four low vertices of Y, which contain the
    d_L(x_A) = 3 low neighbours of x_A. By (L3) (applied to x_B), A = B: contradiction. ∎
  (This is ChatGPT's case list "all three highs one type / three distinct types / multiplicities 2 + 1", organised by
  the largest c so that highs matching types absent from X are covered too.)

**4i.7 m = 5: v1 102 = (4^8, 5^5, 9^2) is impossible (PROVED; ChatGPT section 10 under RA9X10's reading).** μ ≤ 3;
d(h) ≤ 3.
* (I), all five highs in Y, X = six low vertices, ℓ_Y = 2. By (h), Σ_Y d ≤ 5·3 + 2·5 = 25, and Σ_Y d ≥ 24, so the
  highs contribute ≥ 14. If at most three highs had degree 3, they would contribute ≤ 3·3 + 2·2 = 13; so **at least four
  highs have degree 3**, each matching a type with three copies, all in X. X has room for at most two tripled types.
  - Two tripled types A ≠ B: X = 3 copies of each; by (L4) each low vertex of Y is adjacent to the copies of at most
    one of them, so has degree ≤ 3: Σ_Y d ≤ 5·3 + 2·3 = 21 < 24.
  - One tripled type A: the ≥ 4 highs of degree 3 all match A, so c_A ≥ 4 and at most one high matches another type.
    Each of the three non-A vertices of X has ≤ 1 high neighbour and ≤ ℓ_Y = 2 low neighbours, so degree ≤ 3: three
    vertices of X of degree ≤ 3, against (f2).
* (II), h0 ∈ X, four highs in Y, ℓ_Y = 3; |D5| ≥ 4 (f3). A vertex of D5 has d_L ≤ 3, so its type has c ≥ 2. Since
  μ ≤ 3 < |D5|, D5 contains ≥ 2 distinct types, each with c ≥ 2, and the c-values of types in X sum to ≤ 4. Hence D5
  carries exactly two types A, B, with c_A = c_B = 2, and every vertex of D5 has d_L = 3: it is adjacent to all three
  low vertices of Y. Take one of them, y: A and B are both disjoint from type(y), so |A ∩ B| ≥ 3 (L5). But the copies
  of A and B in D5 number ≥ 4, so a pair inside A ∩ B lies in ≥ 4 low masks, against M1 (q4 ≤ 3). ∎
  (ChatGPT's "two complementary types of multiplicities 2 + 2" is read, as RA9X10 does, as "two types, each matched by
  two highs"; and its "both disjoint from all three opposite low masks" needs only one of them, by (L5).)

**4i.8 m = 6: v1 105 = (4^7, 5^6, 9^2) is impossible (PROVED; RA9X10's shorter proof of ChatGPT section 11).**
* (I), all six highs in Y, ℓ_Y = 1: Σ_Y d ≤ 6·3 + 1·5 = 23 < 24.
* (II), h0 ∈ X, five highs in Y, ℓ_Y = 2. The neighbours of h0 are low vertices of Y, so d(h0) ≤ 2; by (f1) d(h0) = 2,
  and by (f3) all five low vertices of X have degree 5. So Σ_X d ≥ 2 + 25 = 27, while Σ_Y d ≤ 2·5 + 5·3 = 25 (h). As
  both sums equal e(F): contradiction. ∎
(ChatGPT's longer argument via ≥ 4 highs of degree 3 matching one tripled type is also correct but not needed.)

**4i.9 Supporting evidence (not part of the proofs).** RA9X10's independent model check (review_RA9X10/model_n9_2.c,
with the Python reference model_n9_2.py) assumes only Theorem 1, the isolation of Z ((P11)), F bipartite with classes
6 + 7, the degree caps, r_i ≤ 7, every 10-subset of F spanning ≥ 12 edges, and M1 (q4 ≤ 3) — neither 4h.5 nor the
lemmas of 4i.2; symmetry: a maximum-degree vertex of X is taken low with mask {0, 1, 2, 3} (it is low by (f4)) and its
neighbourhood is reduced under S_5 on {4, …, 8}. It finds **0 F-level survivors for every m = 0, …, 6**
(c_out_m0.txt … c_out_m6.txt, each under a second of CPU; the Python reference gives identical counters for m = 0, 1, 2,
6). Controls: with the q4 cap removed (c_ctl99_m*.txt) the survivors number 109,792 / 48,404 / 9,128 / 88 for
m = 0, 1, 2, 3, so the search is not vacuous there and M1 is essential. **For m = 4, 5, 6 no relaxation tried produced
survivors** (q4 cap 4, c_ctl4; cap removed, c_ctl99; 10-set threshold 11, c_ctlTH11; cap removed and threshold 11 for
m = 6, c_ctlcap99TH11_m6.txt; RA9X10: up to 10^8 placements evaluated, implementations agree); **non-vacuity for m ≥ 4 is therefore only
indirect** (the search reaches its deep levels and the two implementations agree), not demonstrated by a surviving
control. These checks are supporting evidence, not SAT certificates and not part of the proofs above.

**Dependencies of 4i.** 4h.2 (hence the enumerated finite lemma 4f.1 (a), (c), (d)) and 4h.3 for the classes 6 + 7,
the 3-sum rule and e(F) ≥ 24; 4h.1 (M1) everywhere; 4h.5 for m ≤ 2 only; 4h.4 (in (L1)); Theorem 1 (4b.2); (F1);
(S1); the isolation of the a = 9 vertices in G[O] ((P11)); (R3) (degree ≤ 9). Not used: multiplicity ≤ 2 for m ≥ 3
(not proved, 4h.5); any SAT result; the certified list; (P7), (P8).

**Status ledger after 4i (reporting only; supersedes the ledger after 4h; superseded by the ledger after 4j; not SAT certificates; not a `profile_ok`
level).**

| Case | open profiles (v1 indices) | count | basis |
|---|---|---|---|
| A | 84 (4^14,9), 85 (4^13,5,9), 87 (4^12,5^2,9), 90 (4^11,5^3,9), 94 (4^10,5^4,9), 98 (4^9,5^5,9), 101 (4^8,5^6,9), 104 (4^7,5^7,9) — the n_9 = 1 pure 4/5/9 profiles; F bipartite (4h.2, conditional on 4f.1), classes {7, 7} or {6, 8} | 8 | ledger after 4h minus 88, 91, 95, 99, 102, 105 (4i) [hand-proof reviewed] |
| B | B16 4^15, B17 4^14 5, B18 4^13 5^2, B19 4^12 5^3 — G[O] bipartite (4f.1), 8 + 7 split only (4g.2) | 4 | unchanged from the ledger after 4h [hand-proof reviewed] |

Excluded by 4i: Case A v1 88, 91, 95, 99, 102, 105 (with 86 from 4h.6, every n_9 = 2 pure profile 4^(13−m) 5^m 9^2,
m = 0, …, 6, is excluded, conditional on 4f.1 via 4h.2); Case B none. An exact model check of the eight n_9 = 1
profiles is under certification by RA9X12; it is **not** counted here, and those eight stay open in this ledger.
"[hand-proof reviewed]" means the hand proofs were checked by RA9X10 (with the repairs above); this write-up of them
awaits a separate check. These exclusions are not SAT certificates and change nothing in the certified list,
`a9core.py`, the CNF, the checker or the production run, which remain the only basis of the final claim (section 7).
No order-24 theorem is claimed.

## 4j. ChatGPT rounds 10 (part 1) and 11, reviewed by RA9X13 and RA9X15: Case B 4^15 and (4^14, 5)

Sources: ChatGPT round 10, part 1 (closure_drafts/reviews/gpt/round10_part1_condensed.md: 4^15, v1 B16), reviewed by
RA9X13 (review_RA9X13/REPORT.md and its hand-back: 1.1, 1.2 ACCEPT [hand-proof reviewed]; 1.3 ACCEPT, finite check
reviewed (independent re-implementation, two code paths); write-up notes W1–W4, non-blocking, all applied here); and
ChatGPT round 11, parts 1–2 (closure_drafts/reviews/gpt/round11_condensed.md: (4^14, 5), v1 B17), reviewed by RA9X15
(review_RA9X15/REPORT.md: ACCEPT WITH REPAIR; Part 1a [hand-proof reviewed]; Part 1b finite check reviewed, with
RA9X15's own case split (IIa)/(IIb) replacing ChatGPT's "117-case check", whose details were never captured; Part 2
finite check reviewed (independent re-implementation reproducing every count), with the wording repair R2). Proofs in
my own words. **This write-up was checked by RA9X17: ACCEPT WITH REPAIR; repairs R17-1..R17-3 applied (review_RA9X17/).** **Status: reporting only.** No
`profile_ok` level and no predicate are added; the certified list (section 4, version 2: 131 + 299; its sha256 values
unchanged), `a9core.py`, the CNF and the production run are unchanged. **The two searches below are finite checks
reviewed by independent re-implementation; they are NOT SAT certificates, carry no LRAT/DRAT proof, and are not part
of the certified computation.** No order-24 theorem is claimed. Profile numbers are version-1 indices (archive_v1/).
Labels: written steps carry **[hand-proof reviewed]**; exhaustive searches carry **[finite check reviewed
(independent re-implementation)]**.

**4j.1 Setting (PROVED, conditional on 4f.1 through 4g.2).** Case B (Δ ≤ 8, D = 8), profile 4^(15−b) 5^b with
b ∈ {0, 1}. "Low" = a = 4 (4-mask), "high" = a = 5 (5-mask). Facts used, with sources:
* *Adjacency (Theorem 1, 4b.2).* For x, y ∈ O: x ~ y ⇔ N_I(x) ∩ N_I(y) = ∅. Hence **the masks of an independent
  subset of O pairwise intersect**, and a set of outside vertices is independent iff its masks pairwise intersect.
* *Bipartition.* G[O] is bipartite (4f.1, b ≤ 3), and every partition of O into two independent sets has sizes 8 and 7
  (4g.2). Fix one: **X** (8 vertices) and **Y** (7 vertices), both independent. Every O-neighbour of a vertex of Y lies
  in X, so d_O(y) = d_X(y) for y ∈ Y, and likewise d_O(x) = d_Y(x) for x ∈ X.
* *M1 (4c.2, every b).* q4_ij := #{low x ∈ O : {i, j} ⊆ N_I(x)} ≤ 3.
* *N3 (4d.1, b ≤ 6).* No 4-mask occurs three times among the low vertices: **multiplicity ≤ 2**.
* *Row cap.* r_i := #{x ∈ O : i ∈ N_I(x)} = deg(i) (N(i) ⊆ O by (F4)), so **r_i ≤ 8** (Δ ≤ 8).
* *Degree caps.* A low vertex has d_O ≤ 8 − 4 = 4. A high vertex h has d_O(h) ≤ 2 (4g.2(a): its O-neighbours have
  masks disjoint from the 5-set N_I(h), i.e. they are copies of the 4-set I ∖ N_I(h), at most 2 by N3).
* *12-set rules* (the defining 12-set condition of 𝔽: every 12-vertex set spans ≥ 12 edges; I, X, Y are independent, so every edge of the 12-sets below runs between two of these sets):
  (R-a) for U ⊆ Y, |U| = 4: X ∪ U spans Σ_{u∈U} d_X(u) edges, so **Σ_{u∈U} d_X(u) ≥ 12**;
  (R-b) *8-set floor*: for K ⊆ I, |K| = 4: X ∪ K spans Σ_{i∈K} r_i(X) edges, so **the four smallest r_i(X) sum to
  ≥ 12**; equivalently, for every 5-set C' ⊆ I, Σ_{i∈C'} r_i(X) ≤ (Σ_{x∈X} a_x) − 12;
  (R-c) *9-set floor*: for y ∈ Y and K ⊆ I, |K| = 3: X ∪ {y} ∪ K spans d_X(y) + Σ_{i∈K} r_i(X ∪ {y}) edges, so
  **d_X(y) + (three smallest r_i(X ∪ {y})) ≥ 12**;
  (R-d) *Y-floor*: for K ⊆ I, |K| = 5: Y ∪ K spans Σ_{i∈K} r_i(Y) edges, so **the five smallest r_i(Y) sum to ≥ 12**.
  Here r_i(S) := #{x ∈ S : i ∈ N_I(x)}; all r_i(S), q4-counts and multiplicities over a subset S ⊆ O are ≤ the
  corresponding counts over O, so the caps of M1, N3 and r_i ≤ 8 hold for every partial count.
* *Symmetry.* Every statement above is invariant under S_9 acting on I; once a mask is fixed, under its stabiliser.

**4j.2 Windmill lemma: the degree-four obstruction (PROVED; [hand-proof reviewed], RA9X13 1.1 and RA9X15 Part 1a;
uses Theorem 1, M1, N3, r_i ≤ 8, the degree caps, (R-a)).** *Assume X consists of 8 low vertices* (Y may contain at
most one high vertex). Then **no low w ∈ Y has d_X(w) = 4**; hence every low vertex of Y has d_X ≤ 3.
Proof. Suppose w ∈ Y is low with d_X(w) = 4; put B = N_I(w), C = I ∖ B (|C| = 5).
(a) *The four neighbour masks are distinct.* They are disjoint from B (Theorem 1), i.e. 4-subsets of C; each omits one
element of C. If two coincide, the multiset has one of the patterns AAA·, AAPP, AAPQ (A, P, Q distinct). AAA· is
excluded by N3. In AAPP, |A ∩ P| = 3 (two distinct 4-subsets of a 5-set), and a pair inside A ∩ P lies in all four
masks. In AAPQ, A ∩ P ∩ Q is C minus three elements, a pair, and it lies in all four masks. Both give q4 ≥ 4, against
M1. So the four masks are C ∖ {p} for four distinct p, and the fifth element c of C lies in all four.
(b) *The other four masks of X.* The 12-set X ∪ B ((R-b) with K = B) gives 32 − Σ_{i∈C} r_i(X) ≥ 12, i.e.
Σ_{i∈C} r_i(X) ≤ 20; the four neighbours already contribute 16. Each of the other four vertices x ∈ X is non-adjacent
to the four neighbours (X independent), so its mask meets each C ∖ {p}; in particular it meets C (a 4-mask inside B
equals B and is disjoint from them). The remaining budget 4 forces |N_I(x) ∩ C| = 1, and the single element must lie
in every C ∖ {p}, so it is c: N_I(x) = {c} ∪ T_x with T_x a 3-subset of B.
(c) *The windmill.* For b ∈ B, the low masks containing {c, b} include exactly the masks {c} ∪ T_x with b ∈ T_x (the
masks C ∖ {p} avoid B). Σ_{b∈B} #{x : b ∈ T_x} = 4·3 = 12 over four elements b, and each count is ≤ 3 by M1, so each
equals 3: every b ∈ B is omitted by exactly one T_x, i.e. the T_x are the four sets B ∖ {j}, j ∈ B. Hence
**X = {C ∖ {p} : p ∈ C ∖ {c}} ∪ {{c} ∪ (B ∖ {j}) : j ∈ B}**, unique, and r_c(X) = 8. By r_c ≤ 8 no vertex of Y has c
in its mask.
(d) *Degrees into X.* Let C° = C ∖ {c}. A low mask M ⊆ I ∖ {c} = B ∪ C° with β = |M ∩ B|, γ = |M ∩ C°| (β + γ = 4) is
disjoint from C ∖ {p} iff M ∩ C° ⊆ {p}, and from {c} ∪ (B ∖ {j}) iff M ∩ B ⊆ {j}. So d_X(M) = 4 if M = B or M = C°;
d_X(M) = 1 if β = 3 or γ = 3; d_X(M) = 0 if β = γ = 2. (RA9X13's checks11.py: of the 70 masks avoiding c, 2 have degree
4, 32 have degree 1, 36 have degree 0; ChatGPT's "≤ 2" is the weaker statement.)
(e) *Multiplicities of B and C° in Y.* A pair inside B lies in exactly two of the sets B ∖ {j}, so q4 on it is 2 from X
plus 1 from w: a second copy of B would give 4. A pair inside C° lies in exactly two of the masks C ∖ {p}, so C°
occurs at most once in Y. (checks11.py: 0 extra copies of B, at most 1 of C°.)
(f) *Count.* Y has 7 vertices. Apart from w and at most one copy of C°, every low vertex of Y has d_X ≤ 1 by (d), (e),
and a high vertex has d_O ≤ 2. So at least 5 vertices of Y have d_X ≤ 2, and four of them U give, by (R-a),
12 ≤ Σ_U d_X ≤ 8. Contradiction. Since a low vertex has d_O ≤ 4, every low vertex of Y has d_X ≤ 3. ∎
(Write-up note W1 of RA9X13 applied: the non-distinct patterns are written out. The lemma is stated so that it serves
both 4j.3 (Y all low) and 4j.4 Part 1a (one high vertex in Y).)

**4j.3 v1 B16 = 4^15 is impossible (PROVED, given 4f.1 via 4g.2, and given the finite check in (c)).**
**(a) Degree saturation (PROVED; [hand-proof reviewed], RA9X13 1.2).** All 15 outside vertices are low, so 4j.2
applies: every y ∈ Y has d_X(y) ≤ 3. If some y had d_X(y) ≤ 2, then y and any three other vertices of Y would give
Σ_U d_X ≤ 2 + 9 = 11 < 12, against (R-a). Hence **every vertex of Y has exactly three neighbours, all in X**, and
e(G[O]) = 7·3 = 21. ∎
**(b) The reduction to a finite problem (PROVED; [hand-proof reviewed]).** Fix y ∈ Y; by S_9 take N_I(y) = B =
{0, 1, 2, 3}, C = {4, …, 8}. By (a), y has exactly three X-neighbours; their masks are disjoint from B, i.e. 4-subsets
of C; by N3 no 4-subset of C is taken three times. Of the C(7, 3) = 35 multisets of three 4-subsets of C, 30 are
admissible (the 5 tripled ones are excluded), and under S_5 acting on C (which fixes B) they form exactly two orbits:
* **D** (three distinct, orbit size 10): representative C ∖ {4}, C ∖ {5}, C ∖ {6};
* **R** (one doubled plus one other, orbit size 20): representative C ∖ {4}, C ∖ {4}, C ∖ {5}.
(review_RA9X13/orbits.py, orbits_out.txt.) All constraints below are invariant under the stabiliser S_4 × S_5 of B, so
fixing these representatives loses no case; RA9X13 re-ran the full search from second representatives D2, R2 with
identical counts (symspot_out.txt). The other five vertices of X are not neighbours of y (it has exactly three), so
**their masks meet B** (W2); they meet each seed mask and each other (X independent). Every vertex of Y has a mask
with **exactly three** disjoint X-masks, by (a) and Theorem 1.
**(c) The search [finite check reviewed (independent re-implementation)].** Enumerate every multiset of five further
4-masks completing the seed to X, subject to the following necessary conditions (each with its source):
1. each new mask meets B (y has exactly 3 X-neighbours; 4j.3(a), Theorem 1);
2. the 8 masks of X pairwise intersect (X independent; Theorem 1);
3. multiplicity ≤ 2 within X (N3);
4. q_ij(X) ≤ 3 for every pair (M1; all masks are low);
5. r_i(X) ≤ 8 (deg(i) ≤ 8, (F4));
6. at a completed X: the 8-set floor (R-b), the four smallest r_i(X) sum to ≥ 12 (with Σ a_x = 32; RA9X13 note (iii)).
For each completed X passing the floor, consider every 4-mask m with **exactly three** disjoint masks in X (the only
masks a vertex of Y can carry), and its **capacity**
cap(m) := min( 2 − μ_X(m), min_{i∈m} (8 − r_i(X)), min_{{i,j}⊆m} (3 − q_ij(X)) ),
where μ_X, r_i(X), q_ij(X) are counts over X only. *Soundness of the relaxation:* in a real graph, a mask m occurring
μ_Y(m) times in Y has μ_X(m) + μ_Y(m) ≤ 2 (N3), r_i(X) + μ_Y(m) ≤ r_i(O) ≤ 8 for i ∈ m, and q_ij(X) + μ_Y(m) ≤ q_ij(O)
≤ 3 for {i, j} ⊆ m; so μ_Y(m) ≤ cap(m), and the 7 vertices of Y (y included; B itself is one of the degree-3 masks)
force **Σ_m cap(m) ≥ 7**. The relaxation ignores all constraints among Y vertices (pairwise intersection, the Y-floor,
the caps d_Y(x) ≤ 4), so it can only accept too much, never wrongly reject. The capacity uses μ_X, q_X, r_X only, which
is sound because the true counts over O are at least these (W2).
**Results** (review_RA9X13/search415.py → search_main_out.txt; second, bit-mask implementation search415b.py →
searchb_main_out.txt; the two agree exactly, and agree with every comparable number printed by ChatGPT):

| seed | candidate X masks | completed X passing the floor | Σ cap distribution | max Σ cap | survivors (Σ cap ≥ 7) |
|---|---|---|---|---|---|
| D | 108 | 25,272 | {0: 6264, 1: 18504, 2: 504} | 2 | 0 |
| R | 112 | 35,874 | {0: 12306, 1: 23568} | 1 | 0 |

("candidate X masks" = 4-masks meeting B and all three seed masks, available for the five remaining X slots; this is
what ChatGPT's output calls "candidate_types" (W2), and I recomputed 108 / 112 here. Node and leaf counts depend on
where pruning happens and are not comparable: RA9X13 applies the floor at the leaves, 8,123,553 / 4,050,758 nodes;
ChatGPT's 931,380 / 1,099,132. Only 9 (D) and 22 (R) masks ever have exactly three X-neighbours in a floor-passing X.)
Since Σ cap ≤ 2 < 7 in every case, **no 4^15 graph exists**. ∎
**Controls and robustness (supporting evidence, not part of the proof; review_RA9X13/controls_out.txt,
controls2_out.txt, control_yrelax_out.txt, search415c.py, search415d.py).** With q ≤ 4 and multiplicity ≤ 3 (seed D):
max Σ cap 4, 0 survivors; floor threshold lowered to 10 (seed D): 2,821,632 floor-passing X, max Σ cap 2, 0 survivors;
q removed (seed D; the exact Y completion was enabled but never invoked, since max Σ cap 4 < 7): 0 survivors. **Negative control** (search415d.py
--yrelax: the real X enumeration, but the capacity of a Y mask limited only by the row caps, i.e. the multiplicity and
pair caps on Y dropped): **2,028 survivors**, Σ cap up to 10. So the search is not vacuous by construction; the
multiplicity and pair caps are what remove every case. Two optional controls were stopped early by RA9X13 for budget
(q ≤ 4 / mult ≤ 3 / floor 10; seed R with q removed); they are not claimed.
**Dependencies of 4j.3** (W3): Theorem 1 (4b.2), N3 (4d.1), M1 (4c.2), deg(i) ≤ 8 with (F4), d_O ≤ 4, 4f.1 (G[O]
bipartite; an enumerated finite lemma) and 4g.1/4g.2 (the 8 + 7 split), 4j.2, and 4j.3(a) for "exactly three".

**4j.4 v1 B17 = (4^14, 5) is impossible (PROVED, given 4f.1 via 4g.2, and given the finite checks in (b) and (c)).**
Let h be the unique high vertex (a_h = 5); all other outside vertices are low.
**(a) Part 1a: h ∈ X, and the 4-sum rule on Y (PROVED; [hand-proof reviewed], RA9X15 Part 1a).** Suppose h ∈ Y. Then X
consists of 8 low vertices and 4j.2 applies: every low vertex of Y has d_X ≤ 3. A 4-set U ⊆ Y containing h has
Σ_U d_X ≤ d_O(h) + 3·3 ≤ 2 + 9 = 11 < 12, against (R-a). Hence **h ∈ X and all seven vertices of Y are low**, and
(R-a) holds for every 4-set U ⊆ Y. Moreover, **some vertex of Y has mask I ∖ N_I(h)**: for i ∉ N_I(h), (MAX) gives a
common neighbour of h and i, which lies in O (F4); its mask is disjoint from the 5-set N_I(h) (F1), hence is the
4-set I ∖ N_I(h); it is low and adjacent to h ∈ X, so it lies in Y. ∎
**(b) Part 1b: the degree-three theorem — every vertex of Y has d_X = 3 exactly, and e(G[O]) = 21.** Written part
[hand-proof reviewed]: since every Y vertex is low, d_X ≤ 4; if no Y vertex has d_X = 4, then every d_X ≤ 3, and as in
4j.3(a), (R-a) forces every d_X = 3 and e(G[O]) = 21. It remains to exclude a vertex w ∈ Y with d_X(w) = 4. This is a
finite check [finite check reviewed (independent re-implementation); RA9X15's case split, replacing the uncaptured
"117 cases"]. The split is exhaustive: w is adjacent to h or not.
* **(IIa) w ~ h.** By S_9 take N_I(h) = C = {4, …, 8}; then N_I(w) is disjoint from C (F1), so N_I(w) = B =
  {0, 1, 2, 3}. The other three X-neighbours of w are low (h is the only high vertex) with masks disjoint from B, i.e.
  three 4-subsets of C with no triple (N3): up to S_5 on C (the stabiliser of B and C) two seeds, **T3** (three
  distinct: C ∖ {6}, C ∖ {7}, C ∖ {8}) and **T21** (one doubled plus one: C ∖ {8}, C ∖ {8}, C ∖ {7})
  (review_RA9X15/seeds_orbits.py: 30 admissible multisets, 2 orbits). The other four low X masks are not neighbours of
  w (d_X(w) = 4 exactly), so they meet B, and they meet C (non-adjacent to h) and every other X mask. C-budget:
  Σ_{x∈X} a_x = 5 + 7·4 = 33, so (R-b) with K = B gives Σ_{i∈C} r_i(X) ≤ 21; h and the seeds contribute
  5 + 12 = 17, and each of the four other masks at least 1.
* **(IIb) w ≁ h.** All four X-neighbours of w are low. By S_9 take N_I(w) = B' = {0, 1, 2, 3}, C' = {4, …, 8}. As in
  4j.2(a) the four neighbour masks are distinct, C' ∖ {p} for p ∈ C' ∖ {c}; by S_5 on C' take c = 8. The other three
  low X masks and the 5-mask of h meet B' (they are not neighbours of w) and meet every X mask (X independent). The
  same budget Σ_{i∈C'} r_i(X) ≤ 21 holds (each further mask meets C', since it meets every C' ∖ {p}).
In both cases, b17g.py enumerates every completed X (the 5-mask of h ranges over all 5-sets in (IIb)) subject to:
pairwise intersection in X (Theorem 1); low multiplicity ≤ 2 (N3); q4 ≤ 3 over low masks (M1); r_i ≤ 8 over all
placed masks, h included (deg(i) ≤ 8); the C-budget (a consequence of (R-b), so it loses nothing); the 8-set floor (R-b)
and the 9-set floor (R-c) with anchor w (d_X(w) = 4). For every X passing the floors it runs an **exact** backtracking
search for the other six Y masks (anchor w fixed) under necessary conditions only: Y masks pairwise intersect and
meet N_I(w) (Y independent; Theorem 1); multiplicity ≤ 2, q4 ≤ 3, r_i ≤ 8 over all 15 masks; d_X ≤ 4 for every Y
vertex and d_Y(x) ≤ 4 for every low x ∈ X (degree caps; the cap d_O(h) ≤ 2 is not imposed, which only relaxes); the
4-sum rule (R-a) on Y; the Y-floor (R-d); and (MAX) for h, i.e. some Y mask equals I ∖ N_I(h) (Part 1a). Masks are
chosen in non-increasing d_X order, and a branch is cut only when even the most optimistic completion (all later picks
of the current degree) fails (R-a); this is sound because every later pick has degree ≤ the current one.
**Results** (IIa_out.txt, IIb_out.txt):

| case | completed X | pass floors | Y survivors |
|---|---|---|---|
| IIa | 97 (T3 16, T21 81) | 16 (all T3) | 0 |
| IIb | 416 | 80 | 0 |

In every floor-passing X the only candidate Y mask with d_X ≥ 3 is the anchor's own mask (counter
"Ycand_n_deg>=3_1" equal to the number of floor-passing X). (Reading of this output, not an additional claim: the
anchor mask occurs at most twice in Y (N3), so at least five Y vertices would have d_X ≤ 2 and four of them violate
(R-a); the search confirms this directly.) Hence no Y vertex has d_X = 4, every Y vertex has d_X = 3, and
e(G[O]) = 21. ∎ Controls (IIa_controls_out.txt, IIb_controls_out.txt; supporting evidence): with the Y-conditions
(R-a), (R-d) and (MAX)-for-h dropped and r_i ≤ 9, q4 ≤ 4, multiplicity ≤ 3: **9 survivors** (IIa) and **63 survivors**
(IIb); additionally with both X-floors lowered to 10: **816 survivors** (IIa). Smaller relaxations (one or two
conditions dropped) still give 0, so several constraints act together. No comparison with ChatGPT's "117 cases" is
possible (not captured).
**(c) Part 2: the finite exclusion.**
*Written part [hand-proof reviewed] (RA9X15 2.1–2.3).* By S_9 take N_I(h) = C = {4, …, 8}, B = I ∖ C = {0, 1, 2, 3}. By
Part 1a some y ∈ Y has mask B; it is adjacent to h. By (b), d_X(y) = 3, so y has exactly two further X-neighbours; they
are low with masks disjoint from B, i.e. **exactly two low X masks are 4-subsets of C**. Up to S_5 on C two seeds:
**D** (two distinct 4-subsets of C; representative C ∖ {7}, C ∖ {8}) and **R** (one 4-subset of C taken twice,
allowed by N3; representative C ∖ {8}, C ∖ {8}); of the 15 multisets of two 4-subsets of C, 10 form the orbit of D
and 5 that of R (seeds_orbits.py). The other five low X masks
meet B (else they would be further neighbours of y), meet C (non-adjacent to h ∈ X) and meet every other X mask.
*The budget.* Σ_{x∈X} a_x = 33; the 12-set X ∪ B gives Σ_{i∈B} r_i(X) = 33 − Σ_{i∈C} r_i(X) ≥ 12, i.e. Σ_{i∈C} r_i(X) ≤
21. h and the seeds contribute 5 + 4 + 4 = 13, so **the other five low masks contribute ≤ 8 incidences to C**, each at
least 1. This budget is the case K = B of the 8-set floor, so pruning with it removes only X that the floor rejects
anyway (checked: without budget pruning seed D gives 31,381,068 completed X and the same 91,056 floor-passing ones;
gpt_nobudget_out.txt).
*The constraints of the search, with sources:* (1) the five masks meet B and C and pairwise intersect X (above;
Theorem 1); (2) low multiplicity ≤ 2, counting y (N3); (3) every pair in ≤ 3 low masks, counting y (M1; y is low);
(4) r_i ≤ 8 over X ∪ {y}, h included (deg(i) ≤ 8); (5) the C-budget; (6) at a completed X, the 8-set floor (R-b) (four
smallest r_i(X) ≥ 12, h included) and the 9-set floor (R-c) with y (3 + three smallest r_i(X ∪ {y}) ≥ 12). All
counting conditions only tighten as masks are added, and the floors are tested on completed X only.
*The capacity test (with Repair R2).* Every Y vertex other than y has d_X = 3 by (b), and its mask meets B (Y
independent). For a 4-mask m meeting B with exactly three disjoint X masks, let
cap(m) := min( 2 − μ(m), min_{i∈m} (8 − r_i), min_{{i,j}⊆m} (3 − q4_ij) ), with counts over X ∪ {y} (so for m = B, cap
is the number of copies of B beyond y). As in 4j.3(c), the number of further Y vertices with mask m is ≤ cap(m), so a
real graph needs **Σ cap ≥ 6** over these masks. **Corrected statement (R2):** in every floor-passing X, *the only
degree-3 mask meeting B is B itself, and its residual capacity is 0*. (ChatGPT's wording "the only 4-mask with degree
3 into a completed X is B itself" is false as written: 3,408 floor-passing X have a second degree-3 mask, 3,336 of
them with positive capacity, but all such masks are disjoint from B and so cannot occur in Y.)
**Results [finite check reviewed (independent re-implementation)]** (review_RA9X15/b17.py --mode gpt, written from the
statement; gpt_budget_out.txt; every count equals ChatGPT's):

| seed | nodes | completed X | pass both floors | degree-3 masks ≠ B meeting B with cap > 0 | cap(B) > 0 |
|---|---|---|---|---|---|
| D | 1,168,207 | 675,096 | 91,056 | 0 | never |
| R | 1,813,959 | 1,151,344 | 100,960 | 0 | never |
| total | 2,982,166 | 1,826,440 | 192,016 | 0 | never |

(The 9-set floor removes nothing beyond the 8-set floor here: pass_f8 = pass_both.) (The script's `capsum` histogram sums over all degree-3 masks, including those disjoint from B, and so shows 3,336 X with sum 1; Σ cap over masks meeting B is read from the counters `extra_deg3_positive_cap_meeting_B` = 0 and `B_positive_cap` = 0, both absent from the output, i.e. 0. RA9X17 re-ran with an added counter: none of the 3,408 extra degree-3 masks, of any capacity, meets B.) So Σ cap = 0 < 6 in every case,
and **no (4^14, 5) graph exists**. ∎
*Controls (supporting evidence).* q4 ≤ 4 and multiplicity ≤ 3 (seed D; gpt_ctl_q4m3_D_out.txt): 612 (X, mask) instances
of a degree-3 mask meeting B with positive capacity, cap(B) > 0 in 91,824 X, Σ cap up to 3; floors lowered to 11 (seed
R; gpt_ctl_f11_R_out.txt): 575,968 X pass, 5,616 such instances. So the capacity test is not vacuous; **no control
strong enough to produce full survivors (Σ cap ≥ 6) was run for Part 2** within budget; the Part 1b controls exercise
the same kind of Y logic and do produce survivors.
**Dependencies of 4j.4:** Theorem 1 (4b.2), M1 (4c.2), N3 (4d.1), deg(i) ≤ 8 with (F4), the degree caps (low d_O ≤ 4,
high d_O ≤ 2 by 4g.2(a)), (MAX), (F1), 4f.1 (enumerated) and 4g.2 (the 8 + 7 split), 4j.2 (in Part 1a), and the finite
checks (b) (for "d_X = 3 exactly") and (c).

**Dependencies of 4j.** As listed in 4j.3 and 4j.4; in particular every result of 4j is conditional on the enumerated
finite lemma 4f.1 (through 4g.2), and 4j.3, 4j.4 rest on the finite checks reviewed by independent re-implementation
(RA9X13: search415.py / search415b.py; RA9X15: b17.py, b17g.py). Not used: any SAT result, the certified list, (P7),
(P8), the exp_B4 SAT model (RA9X13: it has no b = 0 result to compare; RA9X15 did not consult it).

**Status ledger after 4j (reporting only; supersedes the ledger after 4i; not SAT certificates; not a `profile_ok`
level).**

| Case | open profiles (v1 indices) | count | basis |
|---|---|---|---|
| A | 84 (4^14,9), 85 (4^13,5,9), 87 (4^12,5^2,9), 90 (4^11,5^3,9), 94 (4^10,5^4,9), 98 (4^9,5^5,9), 101 (4^8,5^6,9), 104 (4^7,5^7,9) — the n_9 = 1 pure 4/5/9 profiles; F bipartite (4h.2, conditional on 4f.1), classes {7, 7} or {6, 8} | 8 | unchanged from the ledger after 4i [hand-proof reviewed] |
| B | B18 4^13 5^2, B19 4^12 5^3 — G[O] bipartite (4f.1), 8 + 7 split only (4g.2) | 2 | ledger after 4i minus B16, B17 (4j) |

Excluded by 4j: Case B v1 B16 (4^15, 4j.3) and B17 ((4^14, 5), 4j.4) — written steps [hand-proof reviewed], searches
[finite check reviewed (independent re-implementation)], conditional on 4f.1 via 4g.2; Case A none. The exact model
check of the eight n_9 = 1 Case A profiles is under certification (RA9X12) and is **not** counted here; those eight
stay open in this ledger. These exclusions are not SAT certificates and change nothing in the certified list,
`a9core.py`, the CNF, the checker or the production run, which remain the only basis of the final claim (section 7).
This write-up awaits a separate check. No order-24 theorem is claimed.

### 4k. The eight n_9 = 1 Case A profiles: exact model check (RA9X12)

Statement. v1 84 (4^14,9), 85 (4^13,5,9), 87 (4^12,5^2,9), 90 (4^11,5^3,9), 94 (4^10,5^4,9), 98 (4^9,5^5,9),
101 (4^8,5^6,9), 104 (4^7,5^7,9) admit no graph. Label: **computer-checked exclusion of a reviewed finite model**
(SAT/LRAT, cake_lpr "s VERIFIED UNSAT" for both the original encoding exp_A9_A_1nines/model_1nines.py, sha256
c5f29088…, and an independent re-encoding from this file, scripts/gen_mine.py); not a hand proof, separate from
the certified production run. Model uses only Theorem 1 (4b.2), (P11) isolation of v, (R3), (F4), (F5), (MAX) via
the saturation identity (clause family (C9) of the section 4 review items; not the enumerated lemma 4f.1), 4h.1 (M1), and the 12-set rule for 12-sets containing v and no I-vertex; symmetry breaking
reviewed sound; every instance UNSAT at the first solve, so no lazy clauses enter. Controls: thresholds 0 and 8 SAT
in both encodings, models decoded and re-checked, cross-fed. Records: review_RA9X12/ (VERDICT.txt, orig/log.txt,
mine/log.txt with CNF/proof/checker sha256).

**Status ledger after 4k (reporting only; checked by RA9X18 with repairs R1, R2; supersedes the ledger after 4j; not a `profile_ok` level).**

| Case | open profiles (v1 indices) | count | basis |
|---|---|---|---|
| A | none | 0 | ledger after 4j minus 84, 85, 87, 90, 94, 98, 101, 104 (4k, computer-checked model) |
| B | B18 4^13 5^2, B19 4^12 5^3 | 2 | unchanged from the ledger after 4j |

Every Case A profile of the level-32 list (4f) is now excluded: by the reviewed hand proofs of 4g–4i (partly
conditional on 4f.1, as cited there) or by the 4k model check (which uses neither 4f.1 nor 4h.2). This changes nothing in the certified list or production run, which remain
the only basis of the final claim (section 7). No order-24 theorem is claimed.

### 4l. Case B (4^13, 5^2) and (4^12, 5^3): ChatGPT round 12, reviewed by RA9X16

Sources: ChatGPT "round 11 continuation" = round 12 (closure_drafts/reviews/gpt/round12_B18_B19_condensed.md: v1 B18
(4^13, 5^2) and B19 (4^12, 5^3); the 301-line source script shown by ChatGPT was not captured), reviewed by RA9X16
(review_RA9X16/REPORT.md: **ACCEPT WITH REPAIR**, repairs R1–R4 wording/provenance only, all applied here). Part 1
(no degree-4 Y vertex): finite check reviewed, RA9X16's own exact search rv16c.c / rv16.py replacing the uncaptured
ChatGPT code (R4). The consequence h_Y = 0, d_X = 3, e(O) = 21: [hand-proof reviewed]. Part 2 (seeded degree-3 search):
finite check reviewed (independent re-implementation), every completed-X leaf count and capacity maximum identical to
ChatGPT's. Proofs in my own words. **Status: reporting only.** No `profile_ok` level and no predicate are added; the
certified list (section 4, version 2: 131 + 299; its sha256 values unchanged), `a9core.py`, the CNF and the production
run are unchanged. **The searches below are finite checks reviewed by independent re-implementation; they are NOT SAT
certificates, carry no LRAT/DRAT proof, and are not part of the certified computation.** No order-24 theorem is
claimed. Profile numbers are version-1 indices (archive_v1/). Labels as in 4j.

**4l.0 Setting (PROVED, conditional on 4f.1 through 4g.2).** Case B (Δ ≤ 8, D = 8), profile 4^(15−b) 5^b with
b ∈ {2, 3}; "low" = a = 4, "high" = a = 5. Everything listed in 4j.1 holds here with the same sources (4j.1 is stated for b ∈ {0, 1}, but each
fact used there holds for b ≤ 3: 4f.1 and 4g.2 for b ≤ 3, N3 for b ≤ 6, the rest for every b): Theorem 1 (x ~ y ⇔ masks disjoint, so the masks of an independent set
pairwise intersect); G[O] bipartite (4f.1) with every bipartition 8 + 7 (4g.2), **X** (8) and **Y** (7) both
independent, d_O = d_X on Y and d_O = d_Y on X; M1 (q4_ij ≤ 3 over low masks); N3 (low multiplicity ≤ 2); r_i ≤ 8;
the degree caps **low d_O ≤ 4, high d_O ≤ 2** (4g.2(a)); the 12-set rules (R-a)–(R-d); S_9 symmetry. Write h_X, h_Y for
the numbers of high vertices in X, Y (h_X + h_Y = b), and r_i(S), σ_k(v) := sum of the k smallest entries of v.
In addition:
* *(MAX) for a high vertex.* If h is high with mask H, then **some vertex of the other class has mask I ∖ H**: for
  i ∉ H, (MAX) gives a common neighbour of h and i, which lies in O (F4); its mask is disjoint from H (F1), hence is the
  4-set I ∖ H; it is low and adjacent to h, so it lies in the class not containing h (as in 4j.4(a)).
* *C-budget (2).* If a low y ∈ Y has mask B and C = I ∖ B, the 12-set B ∪ X spans Σ_{i∈B} r_i(X) =
  Σ_{x∈X} |N_I(x) ∩ B| = (32 + h_X) − Σ_{x∈X} |N_I(x) ∩ C| edges (Σ_{x∈X} a_x = 4·8 + h_X), so
  **Σ_{x∈X} |N_I(x) ∩ C| ≤ 20 + h_X** (2). This is the case K = B of (R-b), so pruning with it loses nothing.
* *Floors.* (4) **σ_4(r(X)) ≥ 12** ((R-b), the 12-set X ∪ K, |K| = 4). (5) If Z ⊆ Y is a set of j ≤ 3 vertices each with
  d_X = 3, the 12-set X ∪ Z ∪ K, |K| = 4 − j, spans 3j + Σ_{i∈K} r_i(X ∪ Z) edges (X, Z, K independent), so
  **3j + σ_{4−j}(r(X) + r(Z)) ≥ 12** (5). (4) is the case j = 0.

**4l.1 No low vertex of Y has d_X = 4 [finite check reviewed (independent re-implementation); RA9X16 rv16c / rv16.py,
part 1].** Suppose a low y ∈ Y has d_X(y) = 4. By S_9 take N_I(y) = B = {0, 1, 2, 3}, C = {4, …, 8}. y's
X-neighbours have masks disjoint from B (Theorem 1): a high one has mask C (the only 5-set avoiding B), a low one a
4-subset of C. Let c := #{high x ∈ X with mask C} (c ≤ h_X ≤ 3); the other 4 − c neighbours are low 4-subsets of C.
*Seeds* (up to S_5 on C, which fixes B and C; multiplicity ≤ 2 and q4 ≤ 3 applied): c = 0: four distinct (1+1+1+1;
a repeated mask would give q4 ≥ 4 as in 4j.2(a)); c = 1: 1+1+1 or 2+1; c = 2: 1+1 or 2; c = 3: 1. (review_RA9X16/
seeds16.py → seeds16_out.txt: the orbit counts of k = 0, …, 4 low 4-subsets of C are 1, 1, 2, 2, 1.) The other X masks
are not neighbours of y, so they meet B; they meet every X mask (X independent). The search covers **every allocation
(h_X, h_Y) with h_X + h_Y = b and every c ≤ h_X** (it does not assume a high vertex in X), and places the h_X − c further
high X masks H without any symmetry reduction, subject to **H ≠ C and H ⊉ B** (R1): by (MAX) some Y vertex has mask
I ∖ H, and if H ⊇ B then I ∖ H ⊆ C is disjoint from B, so that Y vertex would be adjacent to y inside the independent
set Y. The X completion imposes pairwise intersection, low multiplicity ≤ 2, q4 ≤ 3, r_i ≤ 8 (all counted with y),
and the C-budget (2). At a completed X: the forced Y masks I ∖ H (H a high X mask ≠ C) must meet B and each other, have
d_X ≤ 4 and fit the caps; the floors (5) with Z = ∅ and Z = {y} (d_X(y) = 4 there, i.e. 4 + σ_3(r(X ∪ {y})) ≥ 12).
For every surviving X, an **exact** search for the remaining Y vertices: low candidates = 4-masks meeting every placed
Y mask with d_X ≤ 4; high candidates = complements of low X masks (a high Y vertex needs I ∖ H in X by (MAX)); exactly
h_Y high in Y; Y pairwise intersecting; multiplicity, q4, r_i over all 15 masks; d_Y(x) ≤ 4 (low x), ≤ 2 (high x);
the 4-sum rule (R-a) (masks taken in non-increasing d_X order, cut only when the most optimistic completion fails);
at a Y leaf the Y-floor (R-d) and then a **full check** of the 24-vertex graph built by Theorem 1 (every 12-set spans
≥ 12 edges, α ≤ 9, Δ ≤ 8, triangle-free, edge-maximality).
**Results** (review_RA9X16/main_1_2_out.txt, main_1_3_out.txt; C program rv16c.c, cross-checked by the Python rv16.py
on b = 2, h_X ≤ 1: py_p1_b2_hX0_out.txt, py_p1_b2_hX1_out.txt, identical counts):

| profile | X nodes | completed X | X passing the floors | Y leaves | survivors |
|---|---|---|---|---|---|
| B18 (b = 2), all (h_X, h_Y), all c | 385,854 | 14,395 | 1,934 | 0 | 0 |
| B19 (b = 3), all (h_X, h_Y), all c | 3,311,247 | 168,611 | 34,932 | 0 | 0 |

(Per-allocation counts are in the output files. ChatGPT's per-allocation node counts, e.g. 76,278 and 854,845, count a
different pruning order and are not comparable; its claim "0 optimistic survivors" in every allocation agrees.) Hence
**no low vertex of Y has d_X = 4**. ∎

**4l.2 Consequence: h_Y = 0, every Y vertex is low with d_X = 3, e(G[O]) = 21 (PROVED; [hand-proof reviewed], given
4l.1).** By 4l.1 and the cap low d_O ≤ 4, every low y ∈ Y has d_X(y) ≤ 3. If h_Y ≥ 1, take a high y ∈ Y (d_X ≤ 2) and
three further Y vertices (|Y| = 7 and b ≤ 3, so three low ones exist, each d_X ≤ 3): Σ d_X ≤ 2 + 9 = 11 < 12,
against (R-a). So **h_Y = 0, h_X = b**, and all seven Y vertices are low with d_X ≤ 3. If some y had d_X(y) ≤ 2, then y
and any three others give Σ ≤ 2 + 9 = 11 < 12, against (R-a). Hence **every y ∈ Y has d_X(y) = 3**, and since X, Y are
independent, **e(G[O]) = 7·3 = 21** (3). ∎

**4l.3 The seeded degree-three search [finite check reviewed (independent re-implementation); RA9X16 rv16c / rv16.py,
part 2].** By 4l.2, X contains all b ≥ 2 high vertices. Fix one, and by S_9 take its mask C = {4, …, 8}, B = I ∖ C =
{0, 1, 2, 3}. By (MAX) some y ∈ Y has mask B; d_X(y) = 3. y's X-neighbours are the c ≥ 1 high X vertices with mask C
and 3 − c low X vertices whose masks are 4-subsets of C. *Seeds* (up to S_5 on C; seeds16_out.txt): **c = 1 distinct**
(C ∖ {7}, C ∖ {8}), **c = 1 doubled** (C ∖ {8} twice; allowed by N3), **c = 2** (C ∖ {8}), **c = 3** (none); c ≤ b.
*Extra high masks.* The b − c further high X masks H satisfy H ≠ C and **H ⊉ B** (R1; reason as in 4l.1: I ∖ H lies in
Y by (MAX), and H ⊇ B would make I ∖ H ⊆ C disjoint from B, i.e. adjacent to y in Y). Each such H forces a
**compulsory Y vertex** with mask I ∖ H (MAX); it is charged to the multiplicity, q4 and r_i caps before X is completed,
and the compulsory masks (B included) must pairwise intersect and have d_X ≤ 3 at the root ("root checks"). The extras
are taken as orbit representatives under the stabiliser of the seed in S_4(B) × S_5(C) (--sym), and the whole search
was **also run without symmetry**, over all 120 single extra masks and all 7,260 multisets of two
(main_2_2_out.txt, main_2_3_out.txt): the same conclusion, 0 survivors.
*Completion of X.* The 8 − b low X masks other than the seeds meet B (they are not neighbours of y, which has exactly
three) and every X mask; low multiplicity ≤ 2, q4 ≤ 3, r_i ≤ 8 (counting y and the compulsory Y vertices); every
compulsory Y vertex keeps d_X ≤ 3 and every low x keeps d_Y ≤ 4; the C-budget (2) with h_X = b. A *completed X leaf*
is a completed X in which **every compulsory Y vertex has d_X exactly 3** (4l.2). On it: floor (4), then floor (5) for
every set Z of j ≤ 3 compulsory Y vertices.
*The c = 3 branch* (B19 only; no extras). Budget (2): Σ_{x∈X} |N_I(x) ∩ C| ≤ 23; the three copies of C give 15, so the
five low X masks give ≤ 8, and each gives ≥ 1 (it meets C, being non-adjacent to the high vertices). Hence at least
two of them have |M ∩ C| = 1, i.e. M = (B minus one element) ∪ {one element of C}; all such masks form one orbit of
the stabiliser S_4 × S_5 (|stab| = 2880), so one may be fixed to {0, 1, 2, 4}, as ChatGPT does. RA9X16 ran this branch
**without** the fixing (2,283,720 completed X leaves, every one with a mask meeting C once; counter
c3_has_one_in_C) and counted the 252,602 that contain {0, 1, 2, 4} (c3_0124_out.txt), which is ChatGPT's number.
*Capacity and the exact Y search.* Every further Y vertex is low with d_X = 3 (4l.2) and its mask meets every
compulsory mask (Y independent). For a 4-mask m meeting every compulsory mask with exactly three disjoint X masks let
cap(m) := min( 2 − μ(m), min_{i∈m} (8 − r_i), min_{{i,j}⊆m} (3 − q4_ij), min_{x∈X, x∩m=∅} (cap_d(x) − d_Y(x)) ),
counts over X ∪ {compulsory Y vertices}, cap_d = 4 (low x), 2 (high x). As in 4j.3(c), a real graph has at most cap(m)
further Y vertices with mask m, and needs **Σ cap ≥ 7 − #compulsory ≥ 4** (at most 1 + (b − c) ≤ 3 compulsory masks).
The relaxation ignores interactions among the further Y vertices, so it can only accept too much. In addition, for
every floor-passing X an **exact** Y search (as in 4l.1, all Y low of degree exactly 3, then the full check) was run.
**Results** (main_2_2_sym_out.txt, main_2_3_sym_out.txt; the C program rv16c.c; rv16.py reproduces B18 c = 1 exactly,
py_p2_b2_c1_sym_out.txt; columns = counters Xdeg3, Xfloor4 (= Xfloor5), largest cap_k; counters absent from an output
line are 0, also for Yleaves / Ysurvivors in 4l.1):

| profile | seed | orbit roots (RA9X16; ChatGPT) | completed X leaves | pass floors (4), (5) | max Σ cap | needed | exact Y survivors |
|---|---|---|---|---|---|---|---|
| B18 | c = 1 distinct | 8; 8 | 17,493 | 240 | 0 | 5 | 0 |
| B18 | c = 1 doubled | 6; 6 | 12,957 | 243 | 0 | 5 | 0 |
| B18 | c = 2 | 1; 1 | 1,381,456 | 352,480 | 1 | 6 | 0 |
| B19 | c = 1 distinct | 131 (109 after root checks); 111 | 26,288 | 780 | 1 | ≥ 4 | 0 |
| B19 | c = 1 doubled | 85 (65 after root checks); 70 | 17,976 | 720 | 1 | ≥ 4 | 0 |
| B19 | c = 2 | 6; 6 | 23,664 | 1,677 | 1 | 5 | 0 |
| B19 | c = 3 | 1; 1 | 252,602 with {0,1,2,4} fixed (2,283,720 unfixed) | 1,192,680 (unfixed) | 2 | 6 | 0 |

(R3: the B18 c = 2 cell is 1 root, 1,381,456 leaves, max capacity 1; ChatGPT's line "2 c 2 1 1,381,456 1" is read this
way.) (R2: for B19 c = 1, RA9X16's orbit counts 131 and 85 differ from ChatGPT's 111 and 70; this has no effect, since
the completed-X leaf counts and capacity maxima agree and the no-symmetry runs cover all roots.) Floor (5) never prunes
beyond (4) (Xfloor4 = Xfloor5 in every branch). In every branch max Σ cap ≤ 2 < 4 ≤ needed, and the exact Y search has
0 survivors. Hence **no (4^13, 5^2) and no (4^12, 5^3) graph exists** (given 4f.1 via 4g.2 and the finite checks
4l.1, 4l.3). ∎

**Controls and robustness (supporting evidence, not part of the proof; review_RA9X16/controls_out.txt,
controls2_out.txt, controls3_out.txt).** Python and C agree on every compared run (B18 part 2 c = 1 with symmetry; part 1
b = 2, h_X ≤ 1; and the relaxed part-1 run below restricted to b = 2, h_X = 1: 88,943 X nodes, 2,495 completed,
1,823 passing the floors, 1,872 Y leaves, all rejected by the full check as non-maximal, in both programs). Relaxed part 1 with q4 ≤ 5, multiplicity ≤ 4, r_i ≤ 10 and 12-set threshold 10 in the floors and Y
conditions (full check unchanged): **14,508 (b = 2) and 74,064 (b = 3) Y leaves**; with q4 ≤ 6, multiplicity ≤ 7,
r_i ≤ 12, threshold 8: 22,751,844 Y leaves (b = 2); every one rejected by the full check (Δ > 8 or not edge-maximal). Relaxed part 2 (q4 ≤ 4, multiplicity ≤ 3): the capacity test
passes in 7,380 X, with no Y leaf. Threshold 11 alone (parts 1 and 2, b = 2, 3) or 10 alone (part 1, b = 2, 3; part 2, b = 3): 0 Y leaves. So the Y search and the full check are exercised
and the main result is not vacuous by construction; several constraints act together. The read-only exp_B4 SAT model is
UNSAT at b = 2, 3, consistent (not used).
**Dependencies of 4l:** Theorem 1 (4b.2), M1 (4c.2), N3 (4d.1), deg(i) ≤ 8 with (F4), the degree caps (low d_O ≤ 4,
high d_O ≤ 2 by 4g.2(a)), (MAX) with (F1), (F4), the 12-set rules (R-a)–(R-d) and the floors (2), (4), (5) (all instances of the defining
12-set condition, which the full check also tests), 4f.1 (enumerated) and 4g.2 (the 8 + 7 split), and the finite checks 4l.1 (for 4l.2) and 4l.3 (RA9X16:
rv16c.c, rv16.py, seeds16.py; rootfilt.py is exploratory only (rootfilt_out.txt: 121 / 77, reproducing neither
count) and is not used). Not used: any SAT result, the certified list, (P7), (P8), the exp_B4 model.

**Status ledger after 4l (reporting only; supersedes the ledger after 4k; not SAT certificates; not a `profile_ok`
level).**

| Case | open profiles (v1 indices) | count | basis |
|---|---|---|---|
| A | none | 0 | unchanged from the ledger after 4k |
| B | none | 0 | ledger after 4k minus B18 (4^13, 5^2), B19 (4^12, 5^3) (4l) |

Excluded by 4l: Case B v1 B18 and B19 — written steps [hand-proof reviewed], searches [finite check reviewed
(independent re-implementation)], conditional on 4f.1 via 4g.2. With 4g–4k, every Case A and Case B profile of the
level-32 list (4f) is now excluded in this reporting ledger: by reviewed hand proofs and reviewed finite checks (partly
conditional on the enumerated lemma 4f.1, as cited in each section) and by the 4k model check. These exclusions are not
SAT certificates and are not a `profile_ok` level; they change nothing in the certified list, `a9core.py`, the CNF, the
checker or the production run, which remain the only basis of the final claim (section 7). This write-up was checked by RA9X19 (repairs R1–R4 applied). No order-24 theorem is claimed.

## 5. The cube formula (`a9core.build(case, profile, cube)`)

Labelling. I = {0,…,8}; the outside vertices are numbered x = 0,…,14 (graph vertex 9 + x) with a_x non-decreasing
(= the profile). In Case A the vertex v is among the last block (a = 9); the formula treats all a = 9 columns alike.
Among all labellings of this kind choose the one whose 9 × 15 incidence matrix M (M[i][x] = 1 iff i ~ x), read row
by row (row 0 first, each row from x = 0 to x = 14), is lexicographically least. **(SYM) PROVED:** for this labelling
(a) row i ≤lex row i+1 for i = 0..7, and (b) for x, x+1 in the same block of equal a: column x ≤lex column x+1
(columns read from i = 0 to 8). Proof. The admissible labellings are closed under permuting I and under permuting
outside vertices with equal a. (a) If row i >lex row i+1, swapping the two rows gives an admissible labelling whose
matrix is smaller (rows before i unchanged, row i smaller). (b) If column x >lex column x', x < x' in one block, let r
be the first row where they differ: M[r][x] = 1, M[r][x'] = 0. Swapping the columns leaves rows < r unchanged and
changes row r first at position x, from 1 to 0: a smaller matrix. Both contradict minimality. ∎ (Checked by brute
force on small matrices: tests.py T2.)

Variables: m(x,i) (135) and e(x,y), x < y (105); auxiliaries are introduced only with implications "aux ⇒ meaning",
or by counters all of whose clauses are satisfied when the auxiliaries are set to their intended values, so every
labelled graph of the cube extends to a satisfying assignment (encoders checked exhaustively: tests.py T1).

Clause families (all PROVED necessary for the labelled graph):
* cube literals (section 7: a leaf of a binary tree over edge variables; the root cube is empty).
* (C1) ¬e(x,y) when a_x + a_y ≥ 10 (F1). These pairs ("NE") are then omitted from all other families: sound,
  because their literals are false.
* (C2), (C3) no triangle i-x-y, x-y-z.
* (C4) exactly a_x of the m(x,·) are true (the profile).
* (C5) each i has at most D outside neighbours; (C6) d_O(x) ≤ D − a_x. (Degree ≤ D.)
* (C7) e(X) ≥ 12 − Σ_{x∈X} a_x for every triple X of O (F2).
* (C8) every pair of I has a common neighbour (in O); (C9) for x ∈ O, i ∈ I: x ~ i or a common neighbour y ∈ O;
  (C10) for x, y ∈ O: x ~ y or a common neighbour in I or in O. ((MAX), (F4).)
* (C11), (C12) = (SYM)(a), (b).
* (C13) column 0 is fixed: m(0,i) = 1 exactly for i ≥ 9 − a_0. PROVED: by (SYM)(a) the first entries of the rows are
  non-decreasing in i (row i ≤lex row i+1 implies M[i][0] ≤ M[i+1][0]), and column 0 has exactly a_0 ones. ∎

## 6. Lazy constraints (`a9core.add_lazy`)

* ['I', T], T a 10-set: T is not independent (α = 9): one clause over the free pairs of T.
* ['F', S], S a 12-set with K = S ∩ I, Y = S ∩ O, J = I ∖ K: e(S) = e(Y) + Σ_{y∈Y} |N_I(y) ∩ K| ≥ 12.
  If |J| ≥ 5 this is encoded directly. If |J| ≤ 4 the **complementary form** is encoded:
  e(Y) + #{(y,j) : y ∈ Y, j ∈ J, y ≁ j} ≥ 12 − Σ_{y∈Y} a_y + |Y||J|.
  PROVED equivalent under (C4): |N_I(y) ∩ K| = a_y − |N_I(y) ∩ J| = a_y − |J| + #{j ∈ J : y ≁ j}. ∎
Both kinds are true in every graph of the cube, whatever the list contains; the list only has to make the formula
unsatisfiable. (Checked on planted graphs: tests.py T3.)

## 7. Case split and completeness (PROVED)

Let G be as in (T). By (R3) it is in Case A or Case B, with I as given there. Its profile satisfies (P1)–(P5), so it
is one of the 131 (B) or 299 (A) profiles of the certified list (version 2; section 4, "Why this list covers
every case"). Label G as in section 5. Then the labelled graph satisfies every clause of
`build(case, profile, [])` (section 5) and every lazy item (section 6).

Cubes. A cube is a list of literals over the 240 edge variables, added as unit clauses. For a profile, the leaves
used are the leaves of a binary tree whose inner nodes branch on one edge variable (children: cube + [v] and
cube + [−v]). The labelled graph is a total assignment of the edge variables, so it satisfies the cube of exactly
one leaf of any such tree. How the tree is grown is irrelevant for soundness: `a9cubes.gen` branches on incidence
bits m(x,i) of chosen columns in order, skipping bits that unit propagation fixes (the propagating solver is not
trusted: skipping a bit merely means not branching on it), and stops a branch either when all bits of the columns
are decided or when propagation fails; `a9run` starts the 33 strong profiles without an entry ≤ 3 from the leaves of this
tree for columns 1, 2 and the other 397 profiles from the root, and replaces a cube that exceeds its time budget
by the leaves of the same construction for the next column below it. `a9check.complete` re-checks from the records
alone that the UNSAT leaves of each profile are exactly the leaves of a binary tree of this form (recursively: all
cubes start with ±v for one variable v, both signs occur, and both sub-families are complete; a single cube must be
empty), and that every one of the 131 + 299 profiles of the certified list occurs. Records are matched to the
list by their profile tuple (not by index: indices changed between list versions 1 and 2).

Hence: if every leaf formula (base + cube + lazy list) is unsatisfiable, no G as in (T) exists.

**The final claim (checker version 3).** Only leaves that were replayed and passed in one `a9check --final` run
count: the CNF is rebuilt from (profile, cube, lazy list), its SHA-256 must equal the record, CaDiCaL must exit 20 on
it and cake_lpr must print exactly "s VERIFIED UNSAT"; coverage is computed from exactly this set (per profile one
source, inside it one results file per unit; leaves of different sources are never united). With `--part K/N` the
claim requires exactly the parts K = 0, …, N − 1 for one N, all over the same input (same input digest), all run with
the same code (same sha256 of exp/*.py, exp/*.sh, bin/cadical, bin/cake_lpr, logged by a9final.sh), and all printing
"COVERED AND VERIFIED". (`--part` is rejected unless N ≥ 1 and 0 ≤ K < N.) Local records (out/*) are
not part of the claim.

What a reviewer has to trust besides this note: `a9core.py` implements sections 4, 4a, 5, 6 as written (about 190 lines);
the CNF checked by cake_lpr is the one `a9core` builds (a9check.py rebuilds it and compares SHA-256, then re-runs
CaDiCaL and cake_lpr); cake_lpr; and (A0) for the final corollary.

## 8. Tests (`tests.py`; sanity checks, not proofs)

T1 encoders vs brute force; T2 (SYM) on all 0/1 matrices of sizes 3×4, 3×5, 4×4 with blocks; T3 random edge-maximal
triangle-free graphs with α = 9 on 24 vertices and an independent 9-set: they satisfy the generic families
(C1)–(C6), (C8)–(C10) with D = 9, and each lazy item is satisfiable together with the graph exactly when the set has
≥ 12 edges / is not independent; T4 lemma-level SAT checks: from the axioms (triangle-free, I independent, (MAX),
a ≥ 1, degree ≤ 9, (F2) for all 455 triples, α ≤ 9 lazily) the negation of each of (S2), (S4), (S5), (S6), (S3),
(S7), (S8), (S9), (S1) is refuted by the solver. Results: out/tests.log (list version 1), out/tests_v2.log (version 2: ALL PASS).
