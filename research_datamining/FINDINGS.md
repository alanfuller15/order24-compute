# Order-24: bidirectional data mining — independent research note

**Snapshot:** GitHub `alanfuller15/order24-compute`, `main`, inspected Nov 20 Alaska / Nov 21 2026 UTC. **Scope:** execution and evidence reuse; no new theorem is claimed. Repo files were retrieved through GitHub. Three existing GitHub Actions **metadata ZIPs**, not full proof archives, were inspected locally. No LRAT has been independently replayed in this note.

## Findings with direct evidence

### 1. A two-dimensional formula grid, not isolated searches

All 37 JSON formula catalogues `data/formulas51_c28.json` through `data/formulas87_c64.json` were inspected directly. For layers 51–85, each catalogue has **435** entries, with the **same 435 `(s,a,b,h_index,h_edges)` templates in the same labeled graphs**, while `m`, `c`, and tags vary. L86 has 434 entries (a subset), L87 has 433 (a subset). Total: **16,092 formula obligations**. `ops/recorded.txt` shows **16,088** formula identifiers, leaving four absent: L80 h0 and h1, L81 h0, L82 h0, all `(s,a,b)=(10,4,18)`. `recorded` means recorded in the ledger; it is not an independent proof audit.

The hard H0 is four disjoint edges `(2,3),(4,5),(6,7),(8,9)` and two isolates. The H1 template comprises `(3,9),(4,9),(5,6),(7,8)` and three isolates. Thus L80, L81, L82 hard H0 formulas are adjacent parameter slices of the **same labeled graph**. Never infer UNSAT across layers merely from matching H: `c=m-a-b` and other clauses change.

At `status/STATUS.md` snapshot 2026-11-21 08:21Z: L82 h0 had 9 open cubes / 2.6 core-hours predicted, L81 h0 1,159 / 1.2 h, L80 h0 12 / 3.7 h, L80 h1 32,519 / 6.6 h. **Important correction:** L80 h1's independent producer metadata (run `44859551048`) already contains an UNSAT certificate report; the dashboard also flags it as **finished awaiting manager/audit**. Its previously recorded tree-open number is stale for determining what should be solved next. The report of a CakeML success in that metadata is not a new independent audit by us.

### 2. Universal lazy constraints: a concrete transfer route in both directions

The 16-KB metadata ZIP of run `44367413581` includes a completed `L83_s10a4b18c61_0000` record with **1,636** lazy constraints: **1,620** twelve-set floors and **16** nine-set non-independence constraints. All 1,636 are well-formed, unique, and compatible with the identical H0 in layers 80, 81 and 82 (16 nine-sets contain no fixed H0 edge; none of the twelve-sets has 12 fixed H0 edges). A validated source bank has been extracted into `L83_h0_seed_candidates.json` with full SHA-256 provenance.

**Soundness of transfer:** Every hypothetical counterexample has at least one edge in every nine-set (because `alpha<=8`) and at least 12 edges in every twelve-set (by the counterexample condition). Therefore each of these 1,636 set inequalities is valid *for every layer*, independent of the source certificate and of A22/McKay. To seed another formula, translate each `W` through that target's `lazy_clauses` and include its exact list in the target's final deterministic formula record. **This does not transfer UNSAT or waive any original-graph coverage obligation.**

Do not blindly preload all 1,636: additional clauses and sequential counters can increase memory or slow SAT. Benchmark `0, 16, 64, 256` cuts with a preserved negative control (equal-size random selection from the same bank), fixed cutoff, same solver, and full replay before deployment. All tests should be on an isolated branch and no live A9 check should be modified.

The L80 h1 run has 1,779 lazy sets (1,730 twelve-sets), and the L82 h2 run has 2,350 (2,303 twelve-sets). Pairwise **exact twelve-set intersections** among the three sources are only **24, 45, and 20** respectively, i.e. 0.5%–1.2% Jaccard. This cautions against blindly pooling cuts from different H-types. The source L83 H0 bank contains only 1,023 distinct H0-automorphism *patterns* among 1,620 twelve-sets; pattern equivalence is an **analytic feature**, not permission to omit universally required constraints from proof checking. In a comparison with H1/H2, H0-pattern intersections are 127/189/224 despite far smaller exact intersections. This suggests testing orbit-aware selection, not using orbit representatives as a proof shortcut.

### 3. Historical outcome votes need calibration before driving scheduling

The existing sparse dataset `data/pred_votes.json` contains **69 formula tags**, **13,295 cube keys** and **27,211 raw `(tag-index,outcome)` entries** (outcome 0 = closed, 1 = timeout split). We independently detected **3,833 duplicate identical triples**, **411 `(tag,cube)` pairs containing both a closed and a split observation**, and **1,995 cube keys with duplicates**. Contradictory labels can arise legitimately under different time budgets or versions: treat them as uncertainty, not evidence of an invalid proof.

The present `ops/pool.py` uses *all* historical entries except the target's own tag to compute `vote` and `n_vote` features; duplicates alter those features. Relative to exact deduplication of identical `(tag,outcome)` observations, **1,907 of 13,295** cube keys have different features for target L80 h0; **1,946** for L81 h0; **1,914** for L82 h0. On some keys the mean split score moves visibly, e.g. `0.408 -> 0.333`, but whether this improves scheduling must be tested with out-of-time, held-out-run data. Do not overwrite the raw dataset: build parallel cleaned features and evaluate both versions.

`ops/cost_model.json` is a 200-tree regressor on only five features: `parent_to`, `grand_to`, `depth`, `vote`, `n_vote`. The older extended model `data/pred_model4.json` has 25 features, including layer, crossing-edge count and H index. A new *cost-to-go* model should test layer/H features, handle censored timeouts, and validate with holdout by whole formula and by time (not random cube-only splitting). Prioritize reducing the *worst completion tail*, not prediction accuracy alone.

### 4. Metadata plane before proof plane

The three fetched metadata ZIPs are about 15–18 KB each, yet the corresponding complete proof ZIPs are roughly **1.12 GB**, **3.67 GB** and **3.18 GB**. Metadata already contains `results.jsonl` with full lazy item lists, formula/proof hashes, tree state and per-stage timings. Do discovery, matching, failure classification and seed mining with metadata only; fetch full proof artifacts solely for independent replays or needed proof slices. The full artifacts were not fetched or replayed here.

The three completed records report sum-of-cube CaDiCaL times **21,352.3 s**, **77,635.9 s**, **63,632.7 s** respectively, versus final reported CakeML times **85.9 s**, **1,148.7 s**, **477.4 s**. These are different accounting categories (cumulative search time versus final check); they show why proof-generation/search improvements are likely higher leverage for layer jobs than minimizing the final check alone. The A9 final replay is a different workload with its own bottleneck.

### 5. Machine-readable dependency DAG and typed progress

`exp/cegar90f.py` documents two critical assumptions: saturation at layer `m` requires exclusion at `m+1`; its `b22` and `a22c` families rely on A22. Do not treat an `UNSAT` CNF result and an original-graph exclusion as interchangeable. Establish nodes and explicit edges for `producer complete -> proof replay -> coverage/forward-map checked -> assumption dependencies discharged -> accepted formula`. This is essential if the objective is to eliminate McKay-max without circularity. In the layer chain, independently accepted L83 unlocks the saturation premise for L82; accepted L82 then unlocks L81; accepted L81 unlocks L80. The actual active encoder variant and assumptions for each proof must be read from its metadata and reviewed before declaring the dependency discharged.

## Priority pathways

1. **Near-term, low-risk:** use metadata and the existing 16,088 recorded slots to maintain typed progress and identify genuine pending audits; never re-solve a producer-completed formula solely because `recorded.txt` awaits an auditor.
2. **Experimental, high-leverage:** pilot L83 H0's 1,636 universal constraints on L82/L81/L80 H0 with controlled 16/64/256 initial seeds. Then repeat with cuts from any lower-layer matching H0 source, if its metadata is available. This is bidirectional transfer of true inequalities, **not** a transfer of verdicts.
3. **Engineering:** build a versioned outcome ledger: `(formula fingerprint, cube, encoder, budget, solver, timestamp, outcome, elapsed)` and compare cost-model predictions with observed outcomes. Preserve raw observations and flag conflicting or repeated labels.
4. **Acceptance pipeline:** automate a typed dependency and provenance DAG, with explicit conditional results; audit L80 h1's completed certificate rather than repeating its core search.

## Direct evidence links

- `data/formulas80_c57.json`, `data/formulas81_c58.json`, `data/formulas82_c59.json`, `data/formulas83_c60.json`, `ops/recorded.txt` in `main`.
- `data/pred_votes.json`, `ops/pool.py` lines 145–154, `ops/refill.py` lines 175–205.
- `exp/cegar90f.py` lines 30–34, 81–101, 535–550 and 564–625.
- GitHub Actions run artifacts `44367413581` (`m83f9s4m-h01-meta`), `44859551048` (`m80d6s4m-h02a-meta`), `44841258724` (`m82d6s4m-h01-meta`). These three small source ZIPs are bundled for independent regeneration of metadata findings.
