# REVIEW_T2 — independent review for issue #4

## Dispositions and independence

Reviewer: **Codex lane-4 chat**, formerly a layer-SAT operator, now an independent reviewer. I did not write the alpha-9 mathematical sources, lane 7's closure draft, exp:B4, or lane 3's RA9X20 encoding/certification packet. I have not edited those submissions or produced a replacement encoding. The fresh proof runs below are bounded review replays of submitted CNFs, not new closure production.

Reviewed snapshot: `1af1550bcbe75659f5ffbeb95d7f0cc1f0bd2db0` on `closure-work`. Producers: **lane-7 chat** for T2a; **lane-3 chat / RA9X20** for the T2b packet (reviewing the earlier exp:B4 discovery lane). The exp:B4 materials do not identify a unique numbered discovery chat. Review receipts are in [REVIEW_T2_EVIDENCE/](REVIEW_T2_EVIDENCE/).

| Submission | Verdict | Exact scope |
|---|---|---|
| [ALPHA9_CLOSURE.DRAFT.md](ALPHA9_CLOSURE.DRAFT.md), lane 7 | **ACCEPT WITH REPAIR** | Accept the mathematical/source/label audit as a dated producer's summary; apply the two temporal integration repairs below before calling it the current combined status document. No new mathematical defect found. |
| [RA9X20/](RA9X20/), lane 3 | **ACCEPT**, for **each of B16, B17, B18, B19** | Reviewed graph-to-static-CNF implication plus the two recorded certificate checks per profile. B16 freshly replayed here in both encodings. B17–B19 are acceptance of the supplied checked-certificate records, not a claim of fresh proof replay here. |

**No order-24 theorem is claimed.** These verdicts do not accept issue #3, establish A0, turn finite searches into hand proofs, or promote missing artifacts / UNKNOWN / killed computations to UNSAT.

## T2a: claim and dependency trace

The draft is explicitly a producer's summary. Its section-4 zero-open ledger is a statement about a sequence of reviewed reductions/searches, retaining their dependencies; it is not a new profile list or a certificate for all original graphs.

| Draft claim | Checked source and finding |
|---|---|
| Target T; alpha >= 10 excluded; maximality bridge needs A0 | MATH.md §1 R1–R3 and the chain draft's “The class, the edge range, and the case this chain does not cover”. R1's three independent-set cases are valid; maximal extension can lower alpha, so the explicit A0 caveat is essential and correctly retained. |
| Production 430 profiles, 3,636 units; 299 A / 131 B; 84+215 / 16+115 | TASKS.md T2a supplies the unit inventory. MATH.md §4 supplies profile totals and strong/weak routing; §§4a,5–7 supply forward map, symmetry, lazy-clause justification, and binary-tree coverage obligations. Inventory is not coverage. P7/P8 truth is not needed for routing to weak extras. No Theorem-1 or 4f.1 shortcut is silently added to this production route. |
| Ledgers: A 84,81,77,65,36,32,15,14,8,8,0,0; B 16,10,7,7,4,4,4,4,4,2,2,0 | MATH.md §§4a–4l explicitly gives these counts. The last A removals are 17+1+6+8=32; B removals 2+2=4. Indices are v1 reporting indices, not indices into the 430-profile certified list. |
| 4g–4i claims and repairs | MATH.md 4g and RA9X9/REPORT.md, RA9X10/REPORT.md: M1 must be extended to pure Case A; n9=2 bipartiteness uses 4f.1; multiplicity <=2 is used only where justified (m<=2), <=3 otherwise. The draft preserves these scopes and the 4g s=6,k=5 repair. |
| 4j and 4l finite exclusions | RA9X13, RA9X15, RA9X16 REPORT.md and RA9X19/REPORT.md: finite-check labels are retained, not converted to hand-proof-only closure. B17's capacity statement is restricted to masks **meeting B**. B18/B19 capacity maxima and the corrected B19 root counts are not replaced by exploratory counters. All retain 4f.1 through 4g.2 on this route. |
| 4k's eight Case A profiles | MATH.md 4k; RA9X12/VERDICT.txt, orig/log.txt, mine/log.txt and controls_out.txt; RA9X18/REPORT.md. Exactly v1 84,85,87,90,94,98,101,104. Recorded static-CNF/LRAT acceptance is separate from the production run and does not use 4f.1 or 4h.2. No fresh replay of these sixteen historical proofs is claimed here. |
| Earlier finite evidence | MATH.md explicitly records the B23 signature enumeration, the enumerated C9 lemma 4f.1, and finite Zarankiewicz bounds in 4f.4. The draft does not claim independently to reproduce them. RA9X2–8 full reports are absent from this supplied bundle; their review attribution is inherited from MATH.md, as the draft says. |
| Full production gate | Independently fetched the **immutable** A9_FINAL.md at `9ba4f477384c3d415cc3c7ffb19d38a5e56d97bd`: precisely 27/32, missing 8,11,12,13,14, matching digests and literal “Not complete”. Issue #3 was open, both items unchecked, zero comments when inspected. Neither is an independent audit of all replay leaves. The draft correctly withholds the full-production final label. |

The dependency register is materially complete for the stated summary: target hypotheses and R3/F1–F5, MAX, S1–S9/Lemma J/L11, Theorem 1, both M1 scopes, N3, enumerated 4f.1, 4g.1/4g.2, 4h.2/4h.3, finite 4j/4l searches, and the separate 4k model. “Clause family C9” (MAX saturation) is explicitly distinguished from the enumerated “lemma C9” (4f.1). A0 and its BCL/A22/McKay-max/outside-package caveats are not discharged here. Dependencies shared by the two evidence routes are not counted as independent corroboration.

The historical 27/32 status is source-pinned, not a permanent assertion about a moving collector branch. Missing early reviewer reports remain an evidence-availability limit, not an excuse to upgrade a label. The draft contains no claim of unconditional emptiness of the target class or completion of alpha<=8.

### Required repairs: exact old -> new wording

These are **temporal integration repairs**, not rejection of the accurate pre-RA9X20 source snapshot. The lane-3 packet now exists in the reviewed branch. Leave the conditional provenance of the original MATH.md 4j/4l route intact. I propose wording only; I have not changed lane 7's draft.

**R1. Replace this complete paragraph:**

> For Case B, [exp_B4](../research/alpha9/v2/exp_B4/README.md) records unconditional-model solver UNSAT for b=0..3,
> but no separately reviewed LRAT closure in this snapshot. T2b/RA9X20 is a remaining task. Its +4g.2 runs are
> conditional on 4f.1/4g.2; they cannot remove those dependencies. The unconditional-model route is intended to
> avoid them but must first pass encoding review, independent re-encoding, and certificate checks. No such result
> is supplied by T2a. Prior timeouts and killed/incomplete controls remain non-results.

**With:**

> At T2a's source snapshot, [exp_B4](../research/alpha9/v2/exp_B4/README.md) supplied unconditional-model solver UNSAT for b=0..3, but T2a supplied no separate LRAT certification. The later lane-3 [RA9X20 packet](RA9X20/RESULTS.md) supplies two static CNFs and recorded pinned-cake checks for each of B16–B19; lane 4's [REVIEW_T2](REVIEW_T2.md) accepts that separate packet, including fresh replay of B16 in both encodings. This is SAT/LRAT certificate evidence plus a reviewed graph-to-CNF implication for these four profiles, without 4f.1/4g.2. It uses Theorem 1, Case-B M1, the b<=3 proof of N3, MAX and the target's degree/alpha/12-set hypotheses. It does not alter the historical conditional status of the +4g.2 runs or MATH.md 4j/4l, remove Case A's other finite dependencies, certify the 430-profile production run, or establish an order-24 theorem. Prior timeouts and killed/incomplete controls remain non-results.

**R2. Replace this complete final bullet:**

> * No T2b/RA9X20 certification and no claim that all section-4 exclusions avoid 4f.1. Its removal from the complete
>   alternate route remains outstanding even though the reporting ledger reads 0/0.

**With:**

> * T2a itself performed no T2b/RA9X20 certification. The separate RA9X20 packet, independently reviewed in REVIEW_T2, now supplies the four Case-B exclusions without 4f.1/4g.2. No claim is made that all section-4 exclusions avoid 4f.1: the cited Case-A and earlier finite dependencies remain, even though the reporting ledger reads 0/0.

## T2b: independent encoding and dependency audit

I read `model_B4.py`, the capture adapter, `independent.py`, certification/validation/control scripts, and the relevant MATH.md arguments. **No bipartition or 8+7 assumption enters either captured static formula.** `dump_producer.py` invokes only `[b, '--nocore']`, with default double-lex, and stops at Solver construction. BP/sigma/sides branches are inactive; selectors are fixed by units. No candidate-derived lazy clauses enter the submitted certificates.

The mathematical implications needed by the static constraints can be obtained before 4f.1/4g.2:

1. For these 4/5 masks, MAX plus triangle-freeness forces outside adjacency iff disjointness: a common outside neighbour of two disjoint masks would require three pairwise-disjoint masks of total size >=12 in a 9-set. High-high edges are impossible.
2. The Case-B degree caps are low outside-degree <=4 and I-degree <=8. M1 follows directly from the 12-set floor and alpha=9: five lows through a pair violate the floor; four force an independent 11-set among the remaining lows and highs.
3. If a low mask is tripled, M1 forces every other low mask to meet it in <=1 point; those 12-b lows pairwise intersect. Together with all b highs they make a 12-set with <=3b<=9 edges, contradiction for b<=3. Thus N3 needs no bipartiteness. A high's neighbours all have its unique complementary low mask, so its outside-degree is <=2.
4. Averaging outside twelve-sets gives e(O)>=20. With s=15-b, k=12-b and E=e(H,L)<=2b, the floor on H union a k-subset of L gives `(k/s) E + k(k-1)/(s(s-1)) Q >=12`, hence low-low floors 20/18/16/14. These use N3, not the enumeration or bipartiteness conclusion of 4f.1.
5. I-pair common-neighbour clauses and missing I–O-edge covers encode the remaining MAX cases. A lex-least incidence representative supplies double-lex and the fixed first column. Sorted low columns make “slot x differs from x+2” equivalent to multiplicity <=2. This is existence of a representative, not lossless acceptance of every labelling.

Clause audit: producer one-hot types imply all membership bits; disjointness is enforced in both directions; pair gates are exact; existential MX witnesses are sufficient; all 455 O-only twelve-subsets are included. The re-encoding instead uses direct membership bits with exact cardinalities, explicit shared-element AND/edge gates, exact prefix-equality gates and XOR multiplicity tests. It does not import the producer or its captured clauses. Both share PySAT cardinality machinery and pinned CaDiCaL/cake binaries; independence is of the graph encoding, not of all software or mathematical premises.

Both **static** encodings are necessary relaxations of the full graph family: mixed I/O twelve-sets and all alpha clauses are not materialized here. That direction is sufficient for a checked UNSAT proof. A static SAT assignment would not alone be an original-family graph. RA9X20 says this explicitly; its controls separately check the complete decoded graph.

The producer's DH/FL source comments cite late 4g.2/4f.1 passages. RA9X20's direct derivations above validly remove those dependency edges without changing clauses. Its suggested comment-only citation corrections are sensible, but not conditions for these ACCEPT verdicts. The reviewed source hashes must not be silently changed.

## Certificate evidence, controls, and replay limits

All submitted `INPUT_SHA256SUMS` entries passed at the reviewed snapshot; every retained artifact in RA9X20/SHA256SUMS passed. All eight compressed CNFs have valid headers/clause counts and decompress to their per-certificate input hashes. I regenerated all eight static CNFs from the submitted scripts: all eight hashes matched. All eight raw cake logs are exactly `s VERIFIED UNSAT\n`; all eight solver logs report UNSAT; the structured records consistently give solver exit 20, checker exit 0 and the pinned binaries. The records' proof hashes are identifiers of deleted proofs, **not substitutes for those proofs**.

Fresh independent reviewer replay: **both B16 encodings**. Each freshly regenerated binary LRAT passed the pinned checker with exit 0 and exact stdout `s VERIFIED UNSAT\n`. Each regenerated proof hash also matched the submitted proof hash byte-for-byte. `replay.json` and raw logs retain the result; my verified scratch proofs were then deleted. B17–B19 LRAT bytes are not retained in the submission and were **not freshly regenerated here**. Their ACCEPT is at the recorded certificate-review level, supported by the supplied logs, source/CNF audit and successful B16 replay; it is not a claim of an all-eight independent proof replay.

Binary pins:

- CaDiCaL: `eae671d6fab57f7bf909e621adee2a2bd550a0ae0b561065c815f599c7696fe8`.
- cake_lpr: `29e02af756c1f0fc4ccac78e9a908e0d8ef01201786f257f1b27b26603390798`.

The controls are **adequate sanity/acceptance-path controls at their disclosed scope**, not a proof of global encoding soundness. I reran all four planted SAT controls, checked every returned CNF clause, and reran the full 24-vertex C++ graph checker. All have alpha=9, triangle-free, degree<=8 and zero nonmaximal pairs; all 2,704,156 twelve-sets per candidate were inspected. B16/B17/B18 lower the threshold to 0 **and drop M1**, retaining N3; B19 lowers it to 6 with M1/N3 retained; floors are off. Minima reproduce as 5/4/4/6. These are not threshold-12 counterexamples and are not independent discovery of witnesses. They do not test every active threshold-12 family in isolation; the written implication argument remains necessary.

The 2,260 submitted primitive checks passed on rerun. A fresh tiny checker positive control passed; applying its proof to a different SAT CNF gave **exit 0 but no VERIFIED stdout**, reproducing the recorded negative control. `certify.py` requires the exact positive verdict as well as exit 0. Thus exit status alone is not being miscounted as acceptance. No supplied timeout/killed/UNKNOWN exploratory run is used for a certificate verdict.

### Per-profile input and proof identifiers

The following hashes agree between RESULTS.md, logs/*.json and the retained CNFs (proof hashes checked freshly only for B16). P = producer; I = independent.

| Profile | Encoding | CNF SHA256 | Recorded binary-LRAT SHA256 | Verdict |
|---|---|---|---|---|
| B16 | producer | `f0ed60cbc464367c94c32d60f2c54e2add25f5c86899d930558b375ac4248a1c` | `a8e0689ff68fcbb395b1aa79f3360ec5605832a9e80d8d97a0db0fdeba18b634` | ACCEPT |
| B16 | independent | `46ed1d61c5ac6d784fd5c9d61563a66c92a20887a93c357af1ff35ba863e759d` | `1f591daf940728d9e7373c858c553f9882c9170d86515c2aa0a77b8ecdcbd77c` | ACCEPT |
| B17 | producer | `e203177ef7f4d627daccd1ac37a331d90ab9b0ce11a9a4ebf8db3334b8950a09` | `26614cbf1ea2a3ac80a39e6c591141545e6d4efa4b6fa25c6cff1bc8a142aa1b` | ACCEPT |
| B17 | independent | `b8a85348cdc90a2d8c71fe57d4b8ab33357454f30fda3032bbd2ef5f4e6daacc` | `5f4fea409867ab25796115e9e37677a7c6a3fd50ba65038f3b5ebfc2ec8b6167` | ACCEPT |
| B18 | producer | `3e61cf593bc52a949eb4a1e9172b754b60e3648d65e8702d0a8416e48dfbc1fc` | `79e3a55bd25959d93fdc3bdb134d278ed87a04593713696ee4d792a8e8ea2bea` | ACCEPT |
| B18 | independent | `859e614c2869f0fcefa42591f58a1605336b268067fcb909a9a44e10bb5f352e` | `92e332e190a178a0a75b0f4138c1ca488fe1b0a761605d7bc399c5ea8f627e0d` | ACCEPT |
| B19 | producer | `2ce4bfd56143f1c6f37f917cb26afbba653473b34de89923bbf1d19bc9758d9e` | `b58edb603e2f8ad689e983d144ff1d5a2477272ca5c1f087d0f41608af02a39b` | ACCEPT |
| B19 | independent | `6de75c3899a9aab26a160d0e363e253725aff5a6b4f9e29e86cc1cf9ed5a9e12` | `8eedcf02976880c90a7a7406ddd5d4834fa8146465217211831dbdfe2cb631c8` | ACCEPT |

## Source pins and retained review receipts

| Reviewed file | SHA256 |
|---|---|
| `out/ALPHA9_CLOSURE.DRAFT.md` | `8703eb35decefa53c54c8ac1a9d88a7972a52766f58c3a535773240b08ef2c12` |
| `out/RA9X20/REPORT.md` | `c7d410ffbf2e8e074dc87e3b014dc1a6ae00207392b3a4d3c6b271afeceeb94e` |
| `out/RA9X20/RESULTS.md` | `6a2d4d57ad8144d0b0a85379457db0bc6585708e5ed2b1cb3b7cfdda02f50372` |
| `out/RA9X20/independent.py` | `c08a0f861d7f1df308df62cdd3747e8f20ee9dc6dd7fb227336276bb9becd839` |
| `out/RA9X20/SHA256SUMS` | `e561a0a9cfe94d56f1d6e67165790b7035e88104fa599f0d3173f375deea4820` |
| `research/alpha9/v2/MATH.md` | `6526feb0ae96a4698cd751bfd6d2fc681d4989a21c9579c2389a49667846782f` |

Review receipts: `REVIEW_T2_EVIDENCE/SHA256SUMS` pins my small records, raw B16 solver/checker logs and replay drivers. The larger submitted CNFs stay in RA9X20/cnf; no submission was overwritten. `replay.py` regenerates the two B16 proofs from retained CNFs; `checks.py` regenerates all eight inputs and reruns planted controls and the checker negative control. They use `/workspace/r` and scratch `/workspace/work/review-t2`; invoke with `/workspace/sat-venv/bin/python`. The existing RA9X20 `validate.py` and `unit_checks.py` were run read-only, with their output retained in my evidence directory. The input manifest and retained-artifact checks preceded review replays. These verification scripts and receipts are not a new independent graph encoder.

Before publishing, `closure-work` advanced to `a51eba4` (TASKS.md appended unrelated T6, plus unrelated A22/tool material). I fast-forwarded without altering the reviewed T2 submissions; their hashes above remain fixed. Consequently the old RA9X20 INPUT_SHA256SUMS entry for TASKS.md is a pin to the earlier reviewed version and will now fail on that one later append; the initial PASS receipt is not a claim that a moving task file still has its old hash. Replay the reviewed input versions at `1af1550bcbe75659f5ffbeb95d7f0cc1f0bd2db0`, or compare the unrelated task-only delta explicitly. No mathematical source or encoder was silently refreshed.

Residual gates: lane 7's two integration edits are proposed, not applied; the 430-profile final-production review remains a distinct pending issue #3; missing earlier review artifacts and finite-check dependencies remain stated; the alpha<=8 external chain and its trust list remain outside this review. ACCEPT here is not an order-24 theorem or formal proof-assistant verification.
