# Order 24, Erdős #128: the chain of edge layers 96 down to 51 — status map (DRAFT, version 4)

**DRAFT, producer's map, 2026-11-18 (UTC). It claims nothing new.** It lists, in one place, what each layer document
states, what it assumes, and what would still be needed before anyone could state the order-24 result. It does **not**
state the order-24 theorem. Version 4 adds the independent replay P94M of the (6,7²,8²¹) replication and one more audited certificate (layer 81; 16,085 certified, 7 without a certificate, 97 audit groups, 26 hosted). Version 3 (2026-11-18, later): layers 87–51 now have closure documents, issued after the gate review RCL; one more formula is certified; rows and items updated accordingly. Version 2 is version 1 with the findings of review RCH
(`closure_drafts/review_RCH/REVIEW.md`: 5 must-fix, 10 should-fix; `FIX_CHECK.md`: 2 changes, then a delta check of version 3 with 3 changes, all made here). Paths are relative to the scratchpad root.

## The class, the edge range, and the case this chain does not cover

"The class": graphs G on 24 vertices that are triangle-free, have α(G) ≤ 8, and have at least 12 edges in every
12-vertex set.

- Upper end: triangle-free and α ≤ 8 give Δ ≤ 8 (a neighbourhood is independent), so m ≤ 96.
- Lower end: averaging the 12-set floor over all 12-sets gives m ≥ 12·C(24,2)/C(12,2) = 552/11 = 50.18…, so m ≥ 51
  (`layers/LOW_LAYERS_ROUTE.md`, now version 7; re-derived by reviews R-LOW and RCH).

So the class is empty if and only if every edge layer m = 51, …, 96 is empty. The chain is top-down: layers 96–94
use no other layer; layer 93 uses layer 94 (through Theorem A, for the 54,964 classes of its saturated run); each
layer m ≤ 92 uses layer m + 1 through Theorem A. No layer uses a layer below it (checked by RCH).

**The class statement is not the Erdős statement.** A counterexample to Erdős #128 at order 24 is a triangle-free graph
on 24 vertices with at least 12 edges in every 12-set; nothing in that definition bounds α. **Triangle-free 24-vertex
graphs with the 12-set floor and α ≥ 9 are a case that no document cited here covers.** The upper-layer documents call
the passage to α ≤ 8 "inherited" and do not re-examine it (`glayer/pkg/LAYER_CLOSURE_94_96.md`, "Not claimed": "it
needs the reduction to α ≤ 8, which is inherited [1] from the project's earlier work and is not re-examined here";
`l90/L90_ROUTE.md` says the reduction "is not used by Theorem L90 as stated. It is needed only to apply L90 to the
original problem"). Review RCH searched the scratchpad for it and found no document that states or proves it:

- `Order24_Frontier_Swarm_Closure/ACTIONABLE_PLAN.md` line 9: "Upstream reduction (counterexample ⇒ E1/G11 partition;
  T1/T2/E2/C7, cut-change, P8) | **inherited; documents never received** | none".
- `E1v3/README.md` line 14: "Those proofs are not in any package received, so please send them."
- `low/source/REPORT.md` names a "P8 independent-nine theorem"; no file defines "P8", "A/P7" or "P9".
- The G11 release (`EXECUTIVE_REPORT.md` §3) and the seven-four package treat it as upstream; the seven-four review
  still has the placeholder "[Authors: state the exact inherited result and its file.]".
- `lean_low/Order24/Statement.lean` defines `IsCounterexample` without α and `AlphaAtMostEight` separately; every
  Lean theorem takes α ≤ 8 as a hypothesis and none derives it.

So the existence, statement and status of the reduction are **unverified**, and until it is found or proved, any
statement built on this chain is about the class only. What is easy (producer's remark; checked by reviewer RCH for α ≥ 10 only): an independent
set of size ≥ 12 contains a 12-set with 0 edges; size 11 plus one more vertex spans at most 11 edges; for size 10,
two outside vertices x, y need d_I(x) + d_I(y) + [xy] ≥ 12, and an edge xy forces disjoint
neighbourhoods in I (sum at most 10 + 1 = 11), so the 14 outside vertices are independent, and 12 of them span 0 edges. So α ≥ 10 is excluded by a few
lines, and the open case is **α = 9**. An exploratory computation on it is running (`research/alpha9/`; nothing
claimed).

## Layer by layer

| Layers | Document | Kind | Degree families | Formulas / classes | Certificates, replays and reviews, as the documents state them |
|---|---|---|---|---|---|
| 96, 95, 94 | `glayer/pkg/LAYER_CLOSURE_94_96.md` (package `Order24_Layers94_96_Closure_v2.zip`, 3a83d8de…) | delivered package | all eight families of m ≥ 94 (RCH re-enumerated: 1 + 2 + 5). Five in this package; the other three in outside packages, next rows | 2,051 classes (five families) | 2,051 of 2,051 by cake_lpr; full independent replay by auditor P4 (those five families only); review RG |
| 95: (7²,8²²) | `Order24_95Edge_TwoSeven_Closure.zip` (541a815e…), `CLOSURE_95_TWOSEVEN.md` | delivered package | one family | 1,848 classes | full replay by auditor P3 (1,848 pass, proofs byte-identical). The document itself says: "As a family result this is [6], awaiting formal acceptance by someone other than the producer"; no record of that acceptance was found |
| 94: (6,7²,8²¹) | G11 release `release/Order24_G11_Original_Scope_Certified_Closure.zip` (a9d82678…) | delivered release | one family | 890 + 3,425 classes by cake_lpr, 13 by an independent-9 witness | (production certificate pass by the integrator; 20 proofs re-checked by an agent; the release itself has **no independent full replay**. Separately, a replication of all 6,911 classes in the 94–96 package's format (same encoder file as the package, byte-identical) was produced on 2026-11-18 and **replayed in full by independent auditor P94M**: 6,911 of 6,911 pass the package's unmodified checker on GitHub-hosted runners (CNF rebuilt and equal to the record, fresh CaDiCaL proof, cake_lpr "s VERIFIED UNSAT", proofs byte-identical; 12 shards, each exit 0 as a partial run; negative controls failed on every shard, none of them reaching cake_lpr; `f94m/audit_P94M/REPORT.md`, assembled results f3b73e7d…). The replay does not establish the forward map, the encoder's soundness or the catalogue's completeness (reviewed by R94M). The 94–96 document still names the G11 release as the evidence of record and still says "52 of 6,911"; it has not been reissued). The release says: "This report does **not** claim the mixed degree family closed"; its result is Theorem U (maxcut ≤ 70), "computer-assisted, not formally verified end to end", which "uses no external input"; the emptiness of the family is its corollary, conditional on M1 (a cut of at least 71 edges), which this chain supplies from BCL 2(b) through the Lean transfer; assembly review "ACCEPT WITH CAVEAT". The 94–96 document's "That family was closed in the G11 release" is stronger than the release's own words |
| 94: (7⁴,8²⁰) | `Order24_SevenFour_Partner_Closure.zip` (71968ec6…) | delivered package | one family | 4,566 classes | **3,144 classes have no cake_lpr certificate** and rest on structural arguments (label [3]); 1,414 structural and certified; 8 certified only; 1,422 distinct verified formulas; two certificate attempts (S10_D1_E4_0009, S11_D1_E8_0593) are listed as not verified for a resource reason (cake_lpr out of memory); both classes are excluded structurally (`CLASS_LEDGER.json`: checker VALID, "classes_remaining": 0); no full replay (8 residue classes regenerated, 112-class cross-validation sample). Status in the package: "[6] conditional on [1] (BCL), within the R7 frame"; not claimed: "an unconditional family exclusion" |
| 93 | `g93/pkg/Order24_Layer93_Closure/LAYER_CLOSURE_93.md` (zip 8cf0dfeb…) | delivered package | all eleven families (partitions of deficit 6; RCH re-enumerated) | 64,447 classes (9,483 + 54,964); 134 frames, 8 excluded by arithmetic | 64,447 of 64,447 by cake_lpr; full independent replay by auditor P5; reviews R93, R93-S. Uses the closure of layer 94 — all five 94-edge families, so also the G11 and seven-four rows above — for the saturated run |
| 92 | `l92/pkg92c/Order24_Layer92_Closure/LAYER_CLOSURE_92.md` (zip 1f694970…) | delivered package | not split by family | 15 profiles, 423 formulas | auditor A1: one run of gcert92.py, exit 0, 423 of 423, on stored trimmed proofs; reviews R92, R2, R3, R4, C1. **Proofs since deleted** (`cleanup_2026-11-15.log`: 570 audited proof files under l92/ and l91/ deleted); the package README still says the proofs stay on the producer's machine |
| 91 | `l91/pkg91b/Order24_Layer91_Closure/LAYER_CLOSURE_91.md` (zip 36e75b40…) | delivered package | not split by family | 17 profiles, 426 formulas | auditor A91: six partial runs (each exit 3) and a resumed final run, "exit 5 (resumed), not 0", 426 of 426; **no exit-0 run** on the route the chain uses; reviews R91A, R91B. **Proofs deleted**; README stale |
| 90 | `l90/L90_CLOSURE.md` | producer's summary | not split by family | 428 formulas | 428 of 428 in five audit groups (each exit 3); proofs deleted. [2]: "Not yet. A replica run … is running" — no result of it was found |
| 89 | `l89/L89_CLOSURE.md` | producer's summary | not split by family | 432 formulas | 432 of 432 in four audit groups (each exit 3); proofs deleted |
| 88 | `l88/L88_CLOSURE.md` | producer's summary | not split by family | 432 formulas | 432 of 432: group G4 exited 1 (one no-verdict line), repaired by the one-formula group G5; proofs deleted |
| 87 … 51 | `layers/l<m>/L<m>_CLOSURE.md` (37 documents; copies in `closure_drafts/issued/`; index `closure_drafts/INDEX.md`) | producer's summaries, **issued 2026-11-18** after text review RCD and gate review RCL (`closure_drafts/review_RCL/GATE.md`, `GATE2.md`): each records a conditional theorem about the class, with its open items; the project owner gave one general instruction on 2026-11-18 ('stop placing review items on my plate, continue. make a review agent. use chat gpt as a reviewer. i need work to progress'); that it covers the closure decision is the producer's reading, which RCL called reasonable | not split by family | 16,092 formulas | 16,084 with a passing certificate line in 96 audit groups (layers 87–76 partial runs; 75–51 one exit-0 run each; 25 groups ran on GitHub-hosted runners in the producer repository's workflow); 8 (layers 83–80) with **no certificate**, covered by Corollaries C22c-83 / C22c-80; proofs deleted (two stray copies kept, layers 87 and 86) |

"Not split by family": from layer 92 down the reduction takes a maximum cut and its profile (s, a, b, c) and does not
fix the degree sequence ("the degrees are not fixed: there is one formula per (profile, H)", encoder docstring). The
degree facts used are d ≤ 8; d ≥ 4, which holds because the graph is saturated (Theorem A, needing layer m + 1) and
then by Theorem B; cut-local inequalities; and the β-gated families from A22 and Lemma V. RCH re-computed the profile
lists (3, 9, 11, 14 for m = 96..93; 15, 17, 18, 19, 19 for 92..88; 20, 21 for 87, 86; 22 for m ≤ 85) and found no
profile with s = 12 or s ≤ 7. Inside the class RCH found no degree family, edge count or cut case that no document
addresses.

"Delivered package" means delivered to the user. Whether the user accepted any of the upper packages is not recorded
in the files read for this map.

## Everything the chain assumes, collected

External or inherited results (label [1]; none re-proved in this project):

| Item | Used by | What the documents say about it |
|---|---|---|
| The reduction to α ≤ 8 | the passage from Erdős #128 to the class | **not found on disk**; statement and status unverified (section above) |
| BCL Theorem 2(b) (Balogh–Clemen–Lidický, arXiv:2103.14179v1) | layers 96–92 directly (cut bound), every lower layer by inheritance | asymptotic statement in an extended abstract; proof of Theorem 2 is a sketch on a flag-algebra computation; its certificate has not been checked |
| A22: a(22) = 17 (McKay, OEIS A389646) | layers 91–51 directly (cut bound via Lemma V) | computer result, not refereed, no certificate, not reproduced |
| McKay-max | layers 83–80 directly (8 formulas: one at layer 83, L83_s10a4b18c61_0001); layers 82–80 also inherit it through layer 83; layers 79–51 by inheritance | assumption about an external computation; the trust entry is itself a draft pending review of its wording |

Project arguments that are reviewed but not machine-checked (label [3]):

| Item | Used by |
|---|---|
| The reductions (cut, profiles, frames, forward maps) of each layer document; P1–P6 (their proof report, ULAYER_REPORT.md, is not on disk) | every layer |
| Theorem 14-F (proved in the T95 package) and the 11-set floor; F(16) = 22 and F(t ≥ 17) ≥ 25 for m ≤ 87 | every profile list |
| Lemma V, Corollaries C22 and C22b | layers 91–51 |
| W92 (degree-weighted blow-up, V10); R92-11 | layer 92; inherited below |
| strict_T, lex_blocks, the arithmetic exclusions | layer 93; inherited below |
| The structural exclusions of the seven-four package (3,144 classes) | layer 94; inherited below |
| The encoder clause families (BOUNDS90.md, `twins`, and the corresponding arguments of layers 96–91) | every layer |
| The version-9 symmetry family `auts` | one record each at layers 85, 84 and 83 (the layer-83 formula is also closed by Corollary C22c-83); inherited below |
| Lemma C22c and Corollaries C22c-80, C22c-83 (with recorded checks W and B) | layers 83–80; inherited below |
| The union and coverage checks | every layer |

Hypotheses proved in Lean, each as an implication: Theorem A (`saturated_of_next_layer_closed`, general in m; takes the
closure of layer m + 1 as a hypothesis) and Theorem B (`four_le_degree`), used by every layer 92–51 (Theorem A also by layer 93); the BCL transfer
for m ≥ 93 (BCL "enters only as a hypothesis"); the profile lists for m = 93–96 (taking P1–P5 and the cut bound as
hypotheses); bridge lemmas of layer 92. The documents report standard axioms only. No layer's formula set has a Lean
result; a Lean second checker was tried on two formulas, is reviewed (RLC), and stays not counted.

Trusted computations and trusted base: the completeness of the H catalogue (`uenum.py`) for layers 92–51; the
catalogues and frames of layers 96–93 (re-enumerated by their reviewers, per their documents); and, for every
certificate, the pinned cake_lpr binary (29e02af7…), the checker scripts, Python with PySAT/numpy/networkx, the
operating system and hardware. CaDiCaL and lrat-trim are not trusted. The auditors' independence from the producer is
the producer's arrangement, not something a reviewer verified.

Label [4] (checked certificate): cake_lpr accepted an LRAT proof for every counted formula or class of the 94–96
package, layer 93, layers 92–88 and the 16,084 certified formulas of layers 87–51. It does **not** hold for every
class of the outside packages (rows above), nor for the 8 exempt formulas.

Label [2] (reproduced): full independent replays exist for the five families of the 94–96 package (P4), for
(7²,8²²) (P3) and for layer 93 (P5). For (6,7²,8²¹) the G11 release has none, but the 2026-11-18 replication of that family was replayed in full by P94M (6,911 of 6,911). There is none for the seven-four family. For layers 92–51 no second
production exists, and the audited proofs are deleted from layer 92 down, so [4] there rests on audit reports and
CHECK_RESULTS files. No single exit-0 run over all formulas exists for layers 91–76.

## What stands between this chain and a statement about order 24

1. **The α ≥ 9 case** (in fact α = 9): find the inherited reduction with its proof, or prove it. Until then any
   statement is about the class only.
2. **The three outside packages**: T95 awaits acceptance by someone other than its producer; the G11 release does
   not itself claim its family closed and has no independent replay (the family's 6,911 classes now have an independently replayed replication, not yet written into the 94–96 document); the seven-four package rests on 3,144
   structurally excluded classes (two further certificate attempts failed for lack of memory; those classes are also
   covered structurally) and has no full replay. Layers 93 and below inherit
   all of this through layer 94.
3. **Layers 87–51 are closed only in the sense of their documents**: conditional theorems about the class, issued by
   reviewers' decision, with [2] and [5] NOT RUN and their proofs deleted. Open items inside them:
   `research/a22_review2/FIX_CHECK.md` left 1 must-fix on route text that no later reviewer file confirms; the
   cross-vendor review's two should-fixes were not implemented; R-LOW did not re-check version 2 of the route.
4. **Layers 90, 89, 88 are producer's summaries** with no closing review of the documents themselves; the layer-90
   replica run has no recorded result.
5. **Layers 92 and 91**: proofs deleted, READMEs stale, and layer 91 has no exit-0 run.
6. **Acceptance**: whether the user accepted any of the upper packages is not recorded.
7. **The trust list above would have to be stated in full** in any order-24 statement, which would be conditional on
   BCL 2(b), A22 and McKay-max at least.
8. **Eight formulas have no certificate** (layers 83–80; a ninth, L83_s10a4b18c61_0000, was certified and audited on
   2026-11-18). Production on seven of them is running; certificates for all eight would remove the direct use of
   McKay-max.

## Not claimed

- The order-24 theorem, or that the class is empty.
- More for layers 87–51 than their closure documents state.
- Anything about graphs with α = 9.
- That this map is complete: the outside packages were read only in their top-level reports and RESULTS.json.
