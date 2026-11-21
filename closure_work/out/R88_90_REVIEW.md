# T4b — closing text/evidence review of the layer 88–90 summaries

## Reviewer, sources, and verdict

Reviewer: **Codex lane-7 chat**, the chat that ran the earlier fast-formula experiments and wrote T2a on this
branch. It did not produce L88_CLOSURE.md, L89_CLOSURE.md, L90_CLOSURE.md, their routes, or their original audits.
The reviewed documents identify their producer only as the project's **producer**; the imported materials were
assembled in closure-work by the producer/orchestrator. A precise original producer-chat identifier is not supplied.
Original reviewers/auditors are R88A, R89A, R90A–D, the cited cross-vendor ChatGPT reviews, and A88/A89/A90 group
auditors, as reported by the summaries. Their independence is reported, not established anew by this review.

Source snapshot: `05ee6515c0e00361d6969ad70ab8204a33ed351a` on closure-work; the three reviewed files themselves
are unchanged from `b15336cf1907d32d6c7ea3afed9404d98da9bb66`.
Read in full: [L88](../l88/L88_CLOSURE.md), [L89](../l89/L89_CLOSURE.md), [L90](../l90/L90_CLOSURE.md),
[LOW_LAYERS_ROUTE.md v7](../layers/LOW_LAYERS_ROUTE.md), and the
[chain status map v4](../closure_drafts/ORDER24_CHAIN_STATUS.DRAFT.md).
Line references below are to the source files in that snapshot.

**Verdict: internally consistent conditional producer's summaries, with required scope wording and a blocking
source-evidence limitation. Closing acceptance of the underlying layer closures is NOT established by this bundle.**
No arithmetic contradiction was found. I checked the stated audit accounting against itself and against the
available route/status map, and checked the two available formula subsets. I could not independently check the
stated audit results against their primary CHECK_RESULTS/records/union files, or check the three specific routes:
those files are not included. This is a completed review with explicit unresolved findings, not an approval of
missing evidence and not a claim that the reported certificates failed.

No new SAT/LRAT run, proof replay, production mutation, or theorem claim was made. All UNKNOWN/no-verdict results
retain their status. The order-24 theorem is not claimed.

## 1. What is available and what is not

The only tracked files under `closure_work/l88/`, `l89/`, `l90/` are the three closure summaries. Missing here:

* L88_ROUTE.md v2, L89_ROUTE.md v3, L90_ROUTE.md v3; BOUNDS90.md and CUBE90.md;
* reviews/A88_G1..G5_AUDIT.md, A89_G1..G4_AUDIT.md, A90_G1..G5_AUDIT.md;
* each layer's `audit/UNION_CHECK.txt`, group CHECK_RESULTS, records and proof indices;
* the named route-review reports, XGPT_REVIEW_L88.md, XGPT_REVIEW_L89.md and XGPT_CERT6.md;
* `gcert88.py`, `gcert89.py`, and the exact historical checker/encoder bundles for all L90 versions;
* formulas90_c67.json, and a completed, audited replica90 result.

The repository does contain data/formulas88_c65.json and data/formulas89_c66.json, the current v7 encoder and
cake_lpr binary. Read-only identity/count checks gave:

| File | Observed SHA-256 / count | Comparison |
|---|---|---|
| data/formulas88_c65.json | 9835d16272c1cad0b81f822febd2305758217ad9ea4a24ff77031596dddb3538; 432 formulas, 19 distinct (s,a,b,c) | Matches L88's quoted pin ends/count and the route's 432 s>=9 base count |
| data/formulas89_c66.json | 792aef890e8c17d38b6726a820e25e9a95997f9986a2277012ef45acf47e3031; 432 formulas, 19 profiles | Matches L89's quoted pin ends/count |
| code/cegar90c.py | 7699f39b78d7703cfb65691f5d7e8cd5f149f6a587400596bbbfb6122ffa86b9 | Matches the summaries' v7 pin prefix |
| bin/cake_lpr | 29e02af756c1f0fc4ccac78e9a908e0d8ef01201786f257f1b27b26603390798 | Matches their checker pin prefix |

Every formula in the two subsets has a+b+c=m, and the minimum c is 65 for L88 and 66 for L89, respectively m-23.
These checks establish identity and accounting only. They do not prove catalogue completeness, profile coverage,
encoder soundness, group disjointness, or acceptance of a certificate.

The low-layer route covers **51–87**, not 88–90. It cites L88 v2 and L89 v3 as its model and uses L88 as the upper
boundary; it is not a replacement for the three omitted layer routes. The chain map is another producer's
summary of these audits, so agreement with it is corroborating text, not an independent audit replay.

## 2. Audit accounting and individual findings

| Layer | Stated groups and verdicts | Checked accounting | Review result |
|---|---|---|---|
| 88 | G1 112 pass; G2 124; G3 114; G4 82 attempted, 81 pass and one no verdict, exit 1; G5 one pass, exit 3 | Original allocation 112+124+114+82=432; passing lines 112+124+114+81+1=432; 433 attempted rows including the re-check | Internally consistent only if G5 is the independent passing re-check of exactly G4's L88_s10a4b18c66_0001. Exact tag-set coverage cannot be checked without primary files. |
| 89 | G1 163, G2 130, G3 104, G4 35; each exit 3 | 163+130+104+35=432 | Consistent with the 432-formula subset. Four cube-and-conquer records in G2 remain certificates of rebuilt formulas as reported, not four extra formulas. Six spot-checks are additional checks, not extra coverage or a full replay. |
| 90 | G1 48, G2 194, G3 86, G4 54, G5 46; each exit 3 | 48+194+86+54+46=428 | Consistent. Encoder split: v4 48, v5 12, v6 52, v7 316 = 428; G2's 130+52+12=194. The 15+21 cube-and-conquer records are 36 of the v7 records, not extra formula coverage. |

### L88 (lines 22, 30–46, 56–62)

The retained G4 cake_exit=-9/NOT VERIFIED line is a **no verdict**, not UNSAT, and not a checker rejection of the
proof. Hash agreement did not establish UNSAT. Only G5's reported accepted proof supplies coverage for that tag;
the G4 auditor's diagnostic success is explicitly not counted. The summary correctly retains the failed attempt
and the exception to the tampered-proof control for G5. It must remain possible to see that G4's original target
set and G5's re-check target overlap once while the **passing** tag sets cover exactly once. A label such as
"all G1–G5 groups disjoint" would be false; the document does not currently say that.

No single exit-0 run is claimed; the positive group exits are 3 (partial). G4 remains exit 1. Deleted proofs mean
this review cannot re-check its 862 MB proof or diagnose memory pressure. The memory/download explanation is the
producer's report, not a proof of correctness. Nothing requires replacing that no-verdict line with a success.

### L89 (lines 21–37, 47–53)

The text distinguishes partial group checks, the separate six-certificate spot-check, and reproduction NOT RUN.
These distinctions are correct. The cross-vendor review's former "certificates not yet complete" objection is
**reported** addressed by the four audits; it cannot be marked independently discharged here without their outputs
and exact union. The subset pin/count agrees with the actual repository file. No arithmetic issue found.

### L90 (lines 20–26, 30–46)

The five groups total 428. The mixed historical encoders must stay visible: a replay using only current v7 does
not reproduce the reported v4/v5/v6 checks. The theorem uses the A22/Corollary C22 route, not the uncompleted A23
alternative L90+. The [5] row correctly limits the Lean floor-ladder statement to that lemma; it does not assert
Lean verification of the whole layer. A run described as "running on 10 rented machines" has no result in this
bundle and earns no reproduced label or coverage credit. See S1 for dated wording.

## 3. Route and dependency check

The stated induction is **91 -> 90 -> 89 -> 88 -> 87 -> ... -> 51**. At each layer m, Theorem A uses the closure of
m+1 to force saturation; Theorem B gives minimum degree 4; alpha<=8 gives maximum degree 8. No cited statement
here uses a lower layer to establish a higher one. All three theorems concern exactly their edge count in the
class (triangle-free, alpha<=8, 12-set floor). The low route's initial hypothesis L88 matches that scope.

A22 and BCL 2(b), the upper-layer closures with **all their assumptions/caveats**, and completeness of uenum's
catalogue remain dependencies. The route/status map additionally identifies reviewed hand reductions (maximum
cut, profiles, 14-F/11-set floors and necessary encoder/symmetry families) and the trusted implementation/base.
Those do not become SAT/LRAT facts when a CNF is certified. Their specific route checks are not reproducible from
the summaries alone. The three outside layer-94/95 packages and layer-91 caveats are inherited, not approved by
T4b. McKay-max is used below at layers 80–83 and inherited downwards; it should **not** be imported backwards as a
new assumption of L88–L90. Similarly v8/v9 provisions for lower layers do not establish their historical encoders.

The summaries' old numeric label tables must be read at their own scope: [3] structural = reported reviewed hand
arguments, not automatic formal proof; [4] = reported checked certificate, not reproduction; [2] remains NOT RUN
(or uncompleted for L90); [5] not run for these layers. This review is a text/evidence review, not a new certificate,
finite-check re-implementation or independent production replay. Conditional status and producer's-summary status
both remain; neither is erased by a successful wording review.

## 4. Must-fix / required evidence before closing acceptance

### M1 — expose primary evidence or explicitly restrict the acceptance claim (all three)

This is an evidence-delivery blocker to a fully checked closing review, not a discovered false audit result.
The TASKS materials do not supply the named routes/audits/records. Short hash citations cannot substitute for them.
The actual mathematical or certificate correctness cannot be accepted on that basis. To keep these files as
self-contained summaries now, add the following paragraph immediately before each status table (exact wording):

> Evidence scope of this copy: this is the producer's summary of the named audits. The cited layer route, audit
> reports, records, CHECK_RESULTS and UNION_CHECK are not included in closure_work. The present text review checks
> internal consistency and the stated dependencies; it does not independently verify the reported certificate
> acceptance or exact tag coverage. Closing acceptance of that evidence remains pending its delivery and review.

For full acceptance, supply stable accessible references/copies of the omitted items listed in section 1, with
full digests and original producer/reviewer identifiers, and re-check their exact tag unions and checker outcomes.
This requirement need not resurrect the deleted proof set to review the **historical audit reports**; it does
require raw proofs or a separately audited fresh replay for a **new certificate replay** claim. These are different
objectives. The original reports' status labels should not be revoked or promoted in the meantime.

### M2 — state the alpha restriction when describing the distance to the original problem

L88 lines 12–13, L89 lines 12–13, and L90 lines 12–13 say the original order-24 statement needs the other edge
layers/degree families excluded. That is necessary but leaves out the alpha>=9 branch explicitly identified as
outside the class by the chain status map. Replace each two-line paragraph with (substitute m=88,89,90):

> This is a conditional statement about the alpha <= 8 class at exactly m edges. Applying the layer chain to the
> original order-24 problem would also require every other possible edge layer of that class and a separately
> justified treatment of alpha >= 9 (including the maximal-extension bridge). Neither is supplied by this layer
> summary, and the order-24 theorem is not claimed.

This is a scope repair, not a claim that the original summaries already stated the theorem. The new T2a draft
also retains its final-review gates; citing it alone would not discharge the alpha branch.

## 5. Should-fix (exact proposed wording)

**S1 — date the L90 replica statement.** Replace L90's [2] row (line 20) with:

> NOT ESTABLISHED by this summary. At the summary's original date the producer reported replica90.py running on
> 10 rented machines; no completed, independently audited result or retained complete replica proof set is supplied
> here. That reported run contributes no coverage or reproduced status to this document.

This neither assumes it is still running nor invents its eventual outcome.

**S2 — make L88's replacement accounting immediate.** After its audit table (line 34), insert:

> G1–G4 allocate 432 distinct target formulas. G5 repeats one target of G4; there are 433 attempted main-run rows,
> of which 432 pass. Exact coverage means the passing rows of G1–G3, the 81 passing rows of G4, and G5's one passing
> row contain every target tag exactly once. G4's no-verdict row is retained and is not counted as a pass.

This wording reports the asserted union; section M1 still limits what was verified here.

**S3 — identify the union acceptance rule.** After the union assertion in L89 and L90, add:

> The reported exact union is over the full expected formula-tag set and the passing main-run rows, matched to
> their records and the appropriate pinned checker/encoder version. A count total or a CHECK_RESULTS digest alone
> is not a coverage check. Controls and diagnostic runs are not counted as additional coverage.

For L88 use S2's explicit exception accounting rather than demanding every historical attempted row pass.

**S4 — preserve the trusted-base distinction.** Add under the status table in each summary:

> Reviewed mathematical reductions and encoder/symmetry arguments remain hand-proof dependencies. The encoded
> UNSAT claims rely on the pinned cake_lpr checker and on the rebuild/coverage scripts, their runtimes and the
> operating system/hardware. No unsupported solver verdict or hash comparison alone establishes UNSAT, and no
> layer-wide Lean verification or independent second production is claimed.

## Disposition

T4b supplies a separate closing review of the **write-ups**, with findings and exact suggested text. No source
summary was silently edited. M1 blocks independent acceptance of the unavailable audit/route evidence; M2 is a
required scope clarification; S1–S4 improve traceability and dated reporting. The displayed counts, induction
order, G4/G5 distinction, partial exits and deleted-proof caveats are internally consistent. No order-24 theorem,
new SAT/LRAT certificate, full replay, or resolution of the outside packages is asserted.
