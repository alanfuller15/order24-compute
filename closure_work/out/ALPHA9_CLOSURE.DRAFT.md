# Alpha = 9 closure: evidence and dependencies (DRAFT)

## Scope, provenance, and verdict

This is T2a for issue #4, written by the Codex lane-7 chat (the chat that previously ran fast-formula experiments),
from the supplied closure-work materials at commit `b15336cf1907d32d6c7ea3afed9404d98da9bb66`.
It is a **producer's summary**, not an independent review of this draft. A different chat must review it.
The mathematical sources were produced by the project's producer/orchestrator, incorporating the ChatGPT rounds
named in MATH.md; their reviewers are identified below. This chat did not produce those sources and does not
replace their reviews. No new solver run, certificate verification, or production-state change was performed.

Let F be the triangle-free graphs on 24 vertices for which every 12-vertex set spans at least 12 edges.
The alpha-9 target T is: **there is no edge-maximal triangle-free G in F with alpha(G) = 9**
([MATH.md](../research/alpha9/v2/MATH.md), section 1). The two evidence lines below address T with different
coverage mechanisms and trust requirements. Neither line is silently substituted for the other.

**Current verdict:** the section-4 reporting ledger has Case A 0 open and Case B 0 open, with the dependencies and
mixed evidence types stated below. The full production-run final claim is **pending**, not accepted here: the
inspected A9_FINAL.md says 27/32 parts, not ALL 32 PARTS AGREE, and issue #3 has no passing independent review.
This draft does not claim the order-24 theorem, emptiness of F, or completion of the alpha <= 8 chain.

## Status vocabulary (labels are not interchangeable)

| Label | Meaning and use here |
|---|---|
| [hand-proof reviewed] | A written mathematical argument reviewed by the named reviewer; not machine-checked. Used only at the scope recorded in MATH.md/reports. |
| finite check reviewed (independent re-implementation) | A finite search whose independent implementation/review is recorded; not an LRAT certificate. This applies to the specified 4j/4l searches, not automatically to all earlier enumerations. |
| SAT/LRAT certificate | Acceptance by the stated certificate checker for specified encoded instances; distinct from encoding soundness and case coverage. The full A9 production label is gated below. The separate eight-profile 4k evidence has its own recorded certificate review. |
| reproduced | A separately documented replay/re-implementation of the particular object, not a synonym for either of the preceding labels. No new replay is asserted by this draft. |
| producer's summary | This draft and unverified aggregate/status descriptions; hashes and logs identify evidence but are not proofs. |
| conditional | An implication retaining its hypotheses or outstanding finite/computational dependencies; not unconditional closure. |

## Alpha >= 10 and the maximality bridge

The chain status draft, ["The class, the edge range, and the case this chain does not cover"](../closure_drafts/ORDER24_CHAIN_STATUS.DRAFT.md),
records RCH's check of the elementary alpha >= 10 exclusion. MATH.md R1 gives the argument explicitly:

* An independent set of size at least 12 contains a zero-edge 12-set.
* An independent 11-set with any outside vertex spans at most 11 edges.
* For an independent 10-set I, an edge xy outside I would force disjoint I-neighbourhoods by triangle-freeness.
  The 12-set I + x + y would then span at most 10 + 1 = 11 edges. Thus the 14 outside vertices are independent,
  giving a zero-edge 12-set.

So G in F has alpha <= 9. This argument needs neither A0 nor any layer certificate. Its status is the hand
argument in R1 and the chain draft's reported RCH check; it is not a new certificate from this chat.

For a general G in F, adding edges until it is edge-maximal triangle-free preserves the 12-set floor, but can
lower alpha. Thus T alone does **not** exclude all original graphs of alpha = 9: a maximal extension might have
alpha <= 8. MATH.md R2 derives emptiness of F only **conditional** on both T and A0 (no member of F has alpha <= 8,
for every edge count). A0 is the separate layer chain, not proved by alpha-9 work. Its outstanding external and
review dependencies (BCL 2(b), A22, McKay-max as applicable, outside packages and other caveats) remain as recorded
in the chain status draft. No implication here discharges them.

## Evidence line I: the certified production route, final gate still open

The stated production inventory is **430 profiles, 3,636 units** (TASKS.md); the unit count is an inventory claim,
not the number of final replay leaves or a coverage proof. MATH.md sections 4, 4a, 5-7 describe its route:

1. R3 splits T into Case A (a degree-9 vertex v, I = N(v)) and Case B (Delta <= 8, any independent 9-set I).
2. The version-2 certified profile list has 299 Case A and 131 Case B profiles. It contains 84 + 16 strong
   (P1)-(P12) profiles and 215 + 115 weak extras. Every possible profile passes (P1)-(P5); failure of (P7)/(P8)
   routes it to the extras, otherwise (P9)-(P12) apply. **The truth of (P7)/(P8) is not required for this coverage
   routing.** The reporting-only levels 16-32 and later ledgers do not shrink this production list.
3. Section 5 proves that a suitably labelled graph extends to the base CNF: triangle restrictions, exact masks,
   degree/triple conditions, maximality families, and sound double-lex/fixed-column symmetry. Section 6 justifies
   each lazy independent-10-set or 12-set clause, including the complementary form. These are forward-map
   arguments; a checker accepting a CNF proof cannot replace them.
4. Section 7 requires a binary-tree leaf cover per profile. Checker v3 rebuilds each CNF, matches the record,
   obtains fresh CaDiCaL exit 20 and exactly `s VERIFIED UNSAT` from cake_lpr, and derives coverage only from
   replay-passing leaves, using one source per profile and one results file per unit; it does not splice sources.
5. A partitioned final claim requires exactly K = 0,...,31 for N = 32, common input digest, common code/binary
   digest, and COVERED AND VERIFIED in every part. Issue #3 must separately pass review by a non-producer.

**Inspected final-status snapshot:** [A9_FINAL.md on a9-final-status](https://github.com/alanfuller15/order24-compute/blob/9ba4f477384c3d415cc3c7ffb19d38a5e56d97bd/A9_FINAL.md),
commit `9ba4f477384c3d415cc3c7ffb19d38a5e56d97bd`, collector timestamp 2026-11-21T03:25Z.
It reports 27/32 COVERED AND VERIFIED, code digest `56875b1d91933390`, input digest `14bd4064b4b0e534`;
parts **8, 11, 12, 13, 14** say `no artifact yet`. The literal closing verdict is:

> **Not complete:** 27/32 parts COVERED AND VERIFIED; digests consistent: 1.

Issue [#3](https://github.com/alanfuller15/order24-compute/issues/3), inspected for this draft, is open with both
checklist items unchecked and no comments. Those missing parts are not inferred to be failures, successes, or
UNKNOWN solver answers; they are absent final evidence. Any actual UNKNOWN remains unresolved, never counted as
UNSAT. **Do not assign the full-production SAT/LRAT certificate label until A9_FINAL.md says ALL 32 PARTS AGREE
and issue #3's independent final-claim review passes.** Updating a collector alone is insufficient.

This route uses the base reductions, profile coverage, encoder/lazy-clause soundness and leaf coverage. It does
not use Theorem 1 of 4b.2, the enumerated 4f.1 lemma, 4g.2, or the later section-4 exclusions as shortcuts.
Its trusted base includes the encoding/checker implementation and its runtime, pinned cake_lpr, and hardware;
CaDiCaL's unsupported verdict alone is not evidence of UNSAT. No certificates were replayed in this writing task.

## Evidence line II: the section-4 mathematical/reporting route

All numbers below are **v1 profile indices** where indices are used. They are not indices in the 430-profile
certified list. The section-4 route is independent of that production list's later computation in the sense of
using separate reductions/searches; it shares mathematical premises and is not fully independent evidence for
those shared premises. MATH.md itself retains production section 7 as the basis of its final claim.

| Stage | Open Case A | Open Case B | Basis and status retained |
|---|---:|---:|---|
| Strong list (4a, level 12) | 84 | 16 | (P1)-(P12), with weak extras retained separately for production |
| 4b, level 16 | 81 | 10 | ChatGPT round 3, RA9X2 review as reported by MATH.md; hand arguments |
| 4c, level 20 | 77 | 7 | Round 4 / RA9X3; hand arguments plus B23 signature enumeration |
| 4d, level 24 | 65 | 7 | Round 5 / RA9X4; hand arguments, N3 adds structure |
| 4e, level 28 | 36 | 4 | Round 6 / RA9X5; repaired hand argument (false original odd-girth table is not used) |
| 4f, level 32 | 32 | 4 | Round 7 / RA9X6 as reported; hand arguments with finite C4-free/Zarankiewicz bounds in 4f.4; 4f.1 is enumerated, not a hand proof |
| 4g | 15 | 4 | 17 one-a=3 Case A profiles excluded [hand-proof reviewed], RA9X7; text check RA9X8, repairs applied |
| 4h | 14 | 4 | A86 excluded [hand-proof reviewed], RA9X9, conditional on 4f.1 via 4h.2; text check RA9X11 |
| 4i | 8 | 4 | A88,91,95,99,102,105 excluded [hand-proof reviewed], RA9X10, same 4f.1 dependence; text check RA9X14 |
| 4j | 8 | 2 | B16/B17 excluded by hand steps plus finite check reviewed (independent re-implementation), RA9X13/RA9X15, conditional on 4f.1 via 4g.2; text check RA9X17 |
| 4k | 0 | 2 | Eight n9=1 profiles: computer-checked exclusion of a reviewed finite model, separate SAT/LRAT evidence recorded by RA9X12; text/ledger check RA9X18 |
| 4l | 0 | 0 | B18/B19: hand steps plus finite check reviewed (independent re-implementation), RA9X16; conditional on 4f.1 via 4g.2; text check RA9X19 |

The level-32 list is 32 Case A + 4 Case B. The successive reporting ledgers remove 17 + 1 + 6 + 8 = 32 in A
and 2 + 2 = 4 in B. Zero open is the result of this ledger with all dependencies retained, not a fresh certificate
or a new `profile_ok` level. Earlier reductions are needed to get to that list.

### Dependency register (transitive dependencies count)

| Dependency | Source/status | Results that use it |
|---|---|---|
| Triangle-free, alpha = 9, 12-set floor, independence of I | Definition T; R1/R3 and F1-F5 | Every reduction and exclusion; these are hypotheses on the target, not imported axioms |
| (MAX) | R2: edge-maximal triangle-free implies a common neighbour for every non-edge | S4-S6; P10; 4b.1; Theorem 1; N3's saturation steps; forced complementary high/low types in 4c-4l; base C8-C10 |
| F1-F5, S1-S9, Lemma J, L11 | Sections 2-4a; hand proofs with review provenance as stated there | Profile coverage and 4b-4f; P11 isolates a=9 vertices and excludes n9>=4 using L11; degrees D=9/8 and row/body cap 8 persist in later searches |
| Theorem 1 (4b.2) | Adjacency iff masks disjoint; uses MAX, F1, S2, S3 | Mask-based arguments 4b-4l, exact graph reconstruction in 4k and exp_B4; not used by production CNF as an extra clause family |
| M1, Case B | 4c.2, all b in the mixed 4/5 family; uses F1, alpha=9 and 12-sets | N3, signature/type counts, 4f.1 applicability, 4g.2 through N3, all 4j/4l pair caps |
| M1, pure Case A | 4h.1, RA9X9 Repair A; extends the restricted 4d statement, uses isolation of Z | 4h-4i and 4k; do not use the older restricted statement without this extension |
| N3 | 4d.1, Case B b<=6; uses M1, Theorem 1, MAX/F4, degree and 12-set counts | 4e for b=4..6; 4f.1 consequence for b<=3; 4g.2 high d_O<=2; multiplicity/degree caps in 4j/4l |
| Enumerated finite lemma C9 (4f.1) | 1152 / 0 / 576 / 0 / 0 counts in RA9X6/c9lemma.py as reported in MATH.md; **not a written hand-proof-only result** | Bipartiteness for Case B b<=3; via 4g.2 all 4j/4l exclusions; via 4h.2 the A86 and other n9=2 exclusions in 4i |
| 4g.1 and 4g.2 | Rigidity and no 9+6 bipartition; reviewed hand arguments conditional on 4f.1 for existence of a bipartition; uses N3, Theorem 1, MAX/F1/F4 | The 8+7 setup throughout 4j and 4l; it excludes no profile by itself |
| 4g.3 | Hand-proof reviewed, including repaired s=6,k=5 branch | Removes A55-57,59-72, using F1/F2/S1/S6/S8, P4/P5/P11, Theorem 1, 12-sets; **no 4f.1** |
| 4h.2/4h.3 | Bipartite F and its 6+7 split/e(F)>=24 for n9=2 | 4h.6 and all 4i cases; retain 4f.1 dependence through 4h.2 |
| 4h.4/4h.5 | Degree-five saturation and no triple when s+t>=13 | A86; 4i uses multiplicity<=2 only for m<=2, and <=3 from M1 for m>=3; these lemmas themselves do not use 4f.1 |
| 4j.2/4j.3 | Windmill hand argument; B16 degree saturation and finite X/capacity search | B16; windmill also used for B17 Part 1a. Finite B16 search: 25,272/35,874 floor-passing X; max capacities 2/1 < 7 |
| 4j.4(b)/(c) | B17 degree-three finite check and final capacity search, RA9X15 | B17: 97/416 completed X in Part 1b, 0 Y survivors; Part 2 has 192,016 floor-passing X, residual capacity 0 over masks meeting anchor B; do not drop "meeting B" |
| 4l.1/4l.2/4l.3 | RA9X16 finite degree-four exclusion, hand consequence, seeded finite search | B18/B19: 0 Y leaves in Part 1, h_Y=0 and d_X=3 follow; Part 2 capacity maxima 0/0/1 (B18), 1/1/1/2 (B19), all below needed>=4; no unrecorded ChatGPT script is treated as evidence |
| 12-set rules R-a..R-d, floors/budgets, symmetry | Instances of the defining floor on independent I/X/Y; S9 stabilisers; 4j.1/4l.0 | 4j/4l searches and their sound capacity relaxations; 4l H not-superset-of-B and compulsory complements use MAX |
| 4k model | Theorem 1, isolated v (P11), R3/F4/F5, MAX saturation identity, pure-A M1 (4h.1), static 11-subsets of F | A84,85,87,90,94,98,101,104 only; **no 4f.1, 4h.2 or assumed bipartition** |
| A0 (all alpha<=8 layers) | Separate external-to-A9 chain, conditional status retained | Only R2's passage from T to emptiness of F; not the internal Case A/B exclusion |

**Do not confuse two C9s:** clause family (C9) in the section-4 review items/section 5 is the MAX saturation
identity. The enumerated finite lemma C9 is **4f.1**. The former is used by 4k and production; that does not make
them depend on the latter.

### The separate eight-profile certificate evidence (4k)

The original discovery folder [exp_A9_A_1nines](../research/alpha9/v2/exp_A9_A_1nines/README.md) says supporting
evidence only. Its solver UNSAT outputs alone are not certificates. The subsequent
[RA9X12 verdict](../research/alpha9/v2/review_RA9X12/VERDICT.txt) records review of that encoding, an independent
re-encoding from MATH.md, eight original + eight independently encoded static CNFs, binary LRAT, and cake_lpr
`s VERIFIED UNSAT` for all 16. The orig/mine logs record exits 20/0 and verification for every m=0..7.
[RA9X18](../research/alpha9/v2/review_RA9X18/REPORT.md) checked the section against those records and at that
review time recomputed the CNF/proof/output hashes. This branch supplies reports/checker outputs, not those raw
CNF/LRAT files; this chat has not independently replayed them. The label is MATH.md's **computer-checked exclusion
of a reviewed finite model (SAT/LRAT)**, separate from production, with the recorded checker trust retained.
No lazy clauses were needed (all eight instances UNSAT at first solve). Controls at thresholds 0 and 8 were SAT
in both encodings, decoded, checked and cross-fed; these are relaxed controls, not target-family examples.

For Case B, [exp_B4](../research/alpha9/v2/exp_B4/README.md) records unconditional-model solver UNSAT for b=0..3,
but no separately reviewed LRAT closure in this snapshot. T2b/RA9X20 is a remaining task. Its +4g.2 runs are
conditional on 4f.1/4g.2; they cannot remove those dependencies. The unconditional-model route is intended to
avoid them but must first pass encoding review, independent re-encoding, and certificate checks. No such result
is supplied by T2a. Prior timeouts and killed/incomplete controls remain non-results.

## Review trace and limits of this bundle

MATH.md attributes original rounds 3-12 to ChatGPT and the mathematical write-up to its producer/orchestrator.
Reviews RA9X2-RA9X8 are cited there but their REPORT.md files are not in this supplied bundle; in particular the
4f.1 enumeration and its RA9X6 review are not independently reproduced or newly labelled as reviewed finite
checks by this draft. This dependency remains explicit. The available RA9X9/10/13/15/16 reports record the later
mathematical/search reviews; RA9X12 records the separate model certification; RA9X18/19 review the later text.
RA9X11/14/17 check outputs/scripts are present, but their full hand-back reports are not. Several old ledger
paragraphs still say "awaits a separate check" after a later header records such a check; use the named later
record with its scope rather than reading the stale sentence as a new verdict.

## Not claimed / remaining gates

* No order-24 theorem; no unconditional emptiness of F; no replacement for A0 or for its trust/dependency list.
* No full-production SAT/LRAT final label at 27/32, no issue-#3 acceptance, and no independent text review of this
  newly written closure draft (the separate review checkbox in issue #4 remains open).
* No hand-proof-only closure: 4f.1 and other finite calculations remain finite dependencies, 4j/4l remain reviewed
  finite searches, and 4k remains certificate evidence for encoded models.
* No new proof replay, formalisation, or "reproduced" label for the full alpha-9 production run.
* No credit to exploratory results, relaxed controls, missing artifacts, timeouts, killed runs, or UNKNOWN as
  exclusions; no changes to the certified profile list, CNF, checker, production run, or record lists.
* No T2b/RA9X20 certification and no claim that all section-4 exclusions avoid 4f.1. Its removal from the complete
  alternate route remains outstanding even though the reporting ledger reads 0/0.
