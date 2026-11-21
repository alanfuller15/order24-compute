# T6 — A22 independent re-check feasibility

Date: 2026-11-21 UTC. Author/producer: Codex lane 6, this closure-work chat.
Inputs: `closure_work/TASKS.md`, `research/review_a22/REVIEW_A22.md`,
`research/a22_review2/REVIEW.md`, and `layers/LOW_LAYERS_ROUTE.md` within `closure_work/`.
Baseline branch commit: `a51eba4196e04742b22130fc40535a04dafea73c`.

**Decision: NO-GO for launching a full independent n=22 recomputation on free runners now.**
GO only for bounded development pilots of a direct maximal-triangle-free generator, coverage checker,
and threshold-cut pruning. The supplied material does not document McKay's search implementation or
justify a whole-search runtime. Generic `geng -t 22` plus exact max-cut is infeasible. No large search
was started. There is a concrete sharding/certificate design below, but its n=22 costs remain UNKNOWN.

## 1. What must actually be established

For a graph H, beta(H) = e(H) - maxcut(H), the minimum number of edges to delete to make it bipartite.
The route's A22 dependency is the **upper bound**

> Every triangle-free graph H on 22 vertices satisfies beta(H) <= 17.

The equality a(22)=17 additionally needs one triangle-free witness with beta=17; an upper-bound
recheck alone does not establish equality. No alpha, degree, floor, connectivity or edge-count
restriction may be silently added to the universal search.

The second, strictly stronger dependency is **McKay-max**:

> Every maximal triangle-free graph on 22 vertices with beta=17 is isomorphic to one of the
> 338 graphs of `minbip22_17.g6`.

Completeness, rather than the validity of individual file members, is the missing assertion.
A sufficient independent computation classifies all maximal triangle-free graphs with beta>=17:
prove no beta>=18, and prove that every beta=17 output is in the pinned list up to isomorphism.
This implies the required completeness, even if a listed graph were redundant.
Adding an edge cannot decrease beta, so every graph has a maximal triangle-free supergraph with
at least its beta. This justifies maximal-only generation for the universal upper bound. It does
not justify replacing universal coverage with a scan of McKay's 338 supplied graphs.

The route uses A22 with Lemma V,
`beta(G) <= beta(G-v-u) + floor(d(v)/2) + floor((d(u)-[uv in E])/2)`,
to constrain maximum cuts of the 24-vertex class. It uses McKay-max directly in Lemma E/C22c,
with recorded checks W and B, to exclude floor-keeping extensions of an extremal 22-vertex graph.
The current route ledger names direct use at layers 80–83 and transitive inheritance below them;
these remain conditional dependencies. The review's older discussion of applications at 84–85
is not a reason to silently broaden the current ledger.

## 2. Evidence and provenance labels

This report is a **producer's summary** and feasibility recommendation. This chat wrote the pilot
checker independently of McKay's search and of the supplied reviewers' scripts, but it is also the
producer of these new pilot results, **not their independent reviewer**. The supplied review was
produced by the separate RA22 reviewer chat; its 143 CPU-hour estimate is quoted evidence, not a
benchmark reproduced here. The supplied RA22 review scripts/outputs are not present alongside its
Markdown in this checkout.

Keep the six labels separate:

- **[hand-proof reviewed]**: do not assign it here; the monotonicity and reduction arguments above
  are explanations, not a newly independent hand-proof review.
- **finite check reviewed (independent re-implementation)**: not assigned to this report's own
  pilots; independent review of their generator/checker/coverage is still required.
- **SAT/LRAT certificate**: none produced by this task; the route records separate W/B work.
- **reproduced**: only the specific bounded counts, timings and existing-list scan below.
- **producer's summary**: all new measurements, projections and engineering recommendations here.
- **conditional**: the route retains A22 and McKay-max; neither is discharged by these pilots.

No order-24 theorem is claimed. Hashes identify inputs and code; they are not proofs.

## 3. Methods and their limitations

**McKay's published data.** The official page
<https://users.cecs.anu.edu.au/~bdm/data/graphs.html>, section “Extremal graphs for bipartization
of triangle-free graphs”, says it gives all extremal graphs up to 23 vertices; the `x.g6` file
contains all extremal graphs and the non-x file the maximal subset. This is a statement of output
coverage, not a documented generation/pruning algorithm or independent proof of completeness.
No source, hardware, split manifest or runtime explaining the review's “about 143 CPU-h” was found
in the supplied materials or this page. Do not treat 143 CPU-h as a reliable project estimate.

**nauty/geng.** `geng -t n` generates triangle-free graphs up to isomorphism, including disconnected
graphs; no `-c`, degree restriction or alpha restriction was used. Its residue/modulus facility can
partition generation (all residues must be covered). A maximality filter after enumeration does
not remove the expensive generation of nonmaximal graphs. A genuinely direct maximal generator
via canonical augmentation is the preferred development route; it needs its own completeness
argument and independently reviewed pruning. Neither `geng` coverage nor direct maximal generation
comes with an LRAT certificate merely by saving output hashes.

**SAT.** Use 231 edge variables, forbid all 1,540 triangles, and seek beta>=18 by requiring at least
18 uncut edges for **every** bipartition. There are 2^21 cuts modulo complementation; fix one vertex's
side. All cuts give an exact but large finite CNF after cardinality encoding. Lazy generation is
sound for an UNSAT proof: each added cut inequality is necessary for every counterexample, so an
UNSAT subset suffices. A SAT intermediate master is UNKNOWN until an independent exact max-cut
oracle finds no violating cut. Timeout is UNKNOWN, never UNSAT. Maximality is expressible by saying
each nonedge has a common neighbour, with explicit witness variables. Symmetry restrictions need a
coverage proof. For McKay-max, search beta>=17 outside the known isomorphism classes; excluding only
338 labelled edge vectors is insufficient (all relabellings must be covered).

**ILP.** For a fixed graph, maximize the sum of crossing-edge variables with binary side variables
and standard XOR linearizations. A feasible cut witnesses beta<=17 (or <=16). Proving exact max-cut
requires a checkable optimality certificate; ordinary solver “optimal” logs do not meet the route's
certificate standard. A graph-selection master with universal cut inequalities is a separation/
bilevel problem, not one routine small max-cut ILP. It still has the classification/coverage problem.

## 4. Actual bounded pilots

Machine: Intel Xeon Platinum 8573C, 3 available cores, about 9,968 MB RAM, no swap. Each pipeline used
one generator and one checker process (at most two cores), sequentially by n. Compiler: `g++ -O3`.
nauty 2.8.9 fetched from <https://pallini.di.uniroma1.it/nauty2_8_9.tar.gz>, configured locally and
`make -j2 geng`. No system packages or environment-maintenance scripts changed.
Each full-enumeration pipeline had a 45-second timeout; each maximal-filter pilot a 30-second timeout.
All completed; no timed-out result was converted into a conclusion. No enumeration above n=12 ran.

The independently written checker decodes graph6, verifies triangle-freeness, and visits every
2^(n-1) cut by Gray-code updates. It records max beta over the supplied stream. The maximal filter
accepts exactly graphs in which every nonedge has a common neighbour. This was an after-filter,
**not a direct maximal-generator benchmark**.

| n | All triangle-free graphs | Maximum beta | Pipeline wall seconds | Maximal graphs | Filtered pipeline seconds |
|---:|---:|---:|---:|---:|---:|
| 7 | 107 | 1 | 0.003911 | 6 | 0.003073 |
| 8 | 410 | 2 | 0.004002 | 10 | 0.003039 |
| 9 | 1,897 | 2 | 0.013190 | 16 | 0.005247 |
| 10 | 12,172 | 4 | 0.062153 | 31 | 0.025790 |
| 11 | 105,071 | 4 | 0.846288 | 61 | 0.129104 |
| 12 | 1,262,180 | 5 | 18.774666 | 147 | 1.414877 |

Controls: NetworkX's independent graph atlas contains exactly 107 triangle-free order-7 graphs;
a separate Python exhaustive-mask calculation gave maximum beta=1. Twenty-one path/cycle/complete-
bipartite controls at n=3..9 matched exhaustive Python max-cut, with the triangle rejected explicitly.
These controls test the implementation; they do not prove nauty's completeness or n=22 feasibility.

A second bounded pilot scanned only McKay's existing 338 maximal-file graphs, not the n=22 universe:
708,837,376 cut evaluations in 4.8966 seconds, maximum beta=17. This supplies beta<=17 for those inputs
and at least one equality witness by exhaustive computation. It **does not** establish A22 or
McKay-max. A producer's output scan remains different from an independently reviewed computation.

Input identities, independently downloaded from the official page:

- `minbip.tar`: `0424c19d8a4b00eb449b4c148d27ff38e53a9f1348850451d925b9312f6f7215`.
- `minbip22_17.g6`: `67b6e19e60bf556c9e6103c301ccba5f4a723c5426bacd8f787c86c106a3bfe4`, 338 lines.
- `minbip22_17x.g6`: `4458639bd01e936bab95e64bd085c98482c5b850012abd9fc08474aa854a39b7`, 1,076 lines.
- nauty archive: `c97ab42bf48796a86a598bce3e9269047ca2b32c14fc23e07208a244fe52c4ee`.

## 5. Extrapolation: what can and cannot be budgeted

The full pipeline grew by 22.1847 from n=11 to n=12. Extending that ratio for ten further orders
would give about **17.2 million single-pipeline years** at n=22. This is a deliberately crude
warning, **not a calibrated prediction or a runtime bound**; neither pruning nor growth is constant.
Even a simpler structural check rules out the unpruned approach: choosing arbitrary edges across
one fixed 11+11 split gives 2^121 labelled triangle-free graphs. An isomorphism class has at most
22! labellings, hence there are at least 2^121/22! = 2.365e15 unlabelled triangle-free graphs.
At the n=12 checker's approximately 7.26 ns per cut, scanning all 2^21 cuts for even that lower-bound
number would cost about **1.14 million CPU-years**. This is conditional throughput extrapolation,
not a lower bound on every possible algorithm. Bipartite detection, early cut witnesses, direct
maximal generation and certified pruning can avoid most of that work.

The existing-list scan gives 6.91 ns/cut, or about 0.0145 seconds/22-vertex graph, and thus roughly
4.0 CPU-hours per million graphs for full cut enumeration alone (excluding generation). The small-n
rate would give 4.23 CPU-hours/million. A direct maximal search with N leaves would therefore cost
roughly 4.0–4.23 * N/1e6 CPU-hours **if** each leaf needed a complete cut sweep. Its actual N, partial-
node count and early-witness/pruning rate at n=22 are **UNKNOWN here**. For sensitivity only: 1e8
leaves imply 400–423 CPU-h; 1e10 imply 40,000–42,300 CPU-h. These N values are scenarios, not claimed
graph counts. The filtered n=12 count of 147 cannot justify a precise n=22 maximal-count forecast.

If 143 CPU-h eventually proved reproducible for the *complete* desired search, the ideal compute
floor would be 35.75 hours on four perfectly utilized cores, before independent checking, generation,
artifacts and reruns. This conditional arithmetic does not validate that estimate. Free-runner
availability, concurrency and quota are not guaranteed by a 4-core specification.

## 6. Concrete independent-job and certificate design (not launched)

1. **Define two obligations and pin inputs.** P18 excludes beta>=18 universally. P17 classifies
   maximal beta>=17 and matches every extremal class to the pinned 338 list, with explicit
   permutations checked by a separate small program. Use no floor/alpha assumptions in P18/P17.
2. **Development gates first.** Implement direct maximal canonical augmentation and threshold-cut
   pruning independently of the producer; cross-check complete counts/histograms against `geng -t`
   at n<=12. Next run n=14/16 bounded pilots (at most five minutes per shard) including restart,
   negative controls and checker cost. Sample multiple prefix types; extrapolate tail costs and
   measure a representative 4-core runner. None of those larger pilots was run in this task.
3. **Partition the canonical search tree into an exhaustive prefix frontier.** The manifest contains
   every root, child relation, canonical decision, assignment/prune witness and stable shard ID.
   Split expensive prefixes recursively. An independent checker verifies coverage, not merely that
   worker outputs have different hashes. Canonical/isomorphism pruning must carry a checkable
   permutation plus a reviewed canonical-parent argument. Without that, use a labelled exhaustive
   prefix tree; it is easy to cover but may be computationally hopeless.
4. **Hard wall budget <5 hours.** Run four independent single-thread subshards per job. Give each
   process 3 CPU-hours and the whole job a 4-hour wall watchdog, leaving a separate margin below
   5 hours for setup/artifacts. Checkpoint by immutable prefix boundaries. An unfinished subtree
   returns UNKNOWN and child prefixes; it is not marked closed. Checker jobs get the same watchdog
   and recursively split work. This enforces per-job duration even if total job count is unknown.
5. **Certificate options.** An exhaustive-search certificate records every covered branch. A leaf
   beta<=17 (P18) or beta<=16 (nonlisted P17) has a 22-bit cut whose uncut count a simple independent
   checker verifies. Known-class leaves carry an isomorphism permutation. Pruned subtrees need a
   bound valid for every completion (e.g. an explicit cut with at most k possible uncut edges even
   if every remaining unknown edge is added). A closed proof of full branch coverage is essential.
   Alternatively encode each labelled prefix's P18 counterexample CNF with lazy necessary cut
   inequalities, and produce LRAT checked by pinned `cake_lpr`; independently review the encoder,
   master-prefix coverage and any symmetry argument. For P17, isomorphism exclusions need their
   own completeness proof. LRAT proves the CNF, not an undocumented graph-to-CNF reduction.
6. **Aggregate with a reviewer other than this chat and the search producer.** The aggregator checks
   every manifest leaf closed, no UNKNOWN, all checker acceptances, consistent pinned versions,
   exact list matching and a separately verified equality witness. Keep generated certificates
   outside Git history when large; immutable manifests/hashes aid transport, never replace proofs.
   A second independently implemented generator provides strong coverage cross-checking if formal
   canonical-augmentation coverage is unavailable; it must finish, not merely match small pilots.

## 7. Recommendation and acceptance gate

**NO-GO now for full n=22 re-computation on free 4-core runners.** Existing-list validity is cheap;
independent coverage is the unresolved cost and trust problem. **GO for bounded engineering only**,
subject to a separately reviewed maximal-generation/coverage scheme and measured representative
pruned shard tails. A future production GO requires (a) demonstrated restartable complete small-order
search, (b) a justified n=22 workload estimate with total quota/storage budget, (c) an independent
checker covering both P18 and P17, and (d) a separate reviewer. Until all jobs and reviews finish,
A22/McKay-max stay external, conditional trust entries. No UNKNOWN is upgraded.

## Appendix — minimal pilot reproduction

Working files were kept under `/workspace/work/a22/`; only this report is published. Rebuild `geng`
from the pinned archive, compile the following C++ with `g++ -O3`, then pipe `geng -t -q N` into it
for N=7..12 with a 45-second timeout. For the maximal-filter variant, insert the nonedge-common-
neighbour predicate described above before enumerating cuts. Do not run this unpruned pipeline at 22.
The timing starts before spawning both programs and ends only after both exit successfully.

```cpp
#include <iostream>
#include <string>
#include <vector>
#include <chrono>
using namespace std;
int main(){string s; unsigned long long count=0, cuts=0;int maxbeta=-1,n=0; auto start=chrono::steady_clock::now();while(cin>>s){n=s[0]-63;vector<unsigned>adj(n);int k=0,m=0;for(int j=1;j<n;j++)for(int i=0;i<j;i++,k++)if(((s[1+k/6]-63)>>(5-k%6))&1){adj[i]|=1u<<j;adj[j]|=1u<<i;m++;}for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)if((adj[i]>>j&1)&&(adj[i]&adj[j]))return 2;unsigned mask=0;int cut=0,best=0;for(unsigned t=1;t<(1u<<(n-1));t++){int v=__builtin_ctz(t),d=__builtin_popcount(adj[v]),other=__builtin_popcount(adj[v]&mask);cut+=(mask>>v&1)?2*other-d:d-2*other;mask^=1u<<v;best=max(best,cut);}maxbeta=max(maxbeta,m-best);cuts+=(1u<<(n-1));count++;}cerr<<"n="<<n<<" graphs="<<count<<" cut_evaluations="<<cuts<<" max_beta="<<maxbeta<<" checker_seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"\n";}
```

Checker source SHA-256: `bdb5f3fe126b5e9102cb184ad7af415fbcc0fe79417a5d28aecc84b9d6a3ac17`.
Maximal-filter source SHA-256: `9fed852b350baafb5929584de92adfda48598b42bcd608d27bda2a56808aee0d`.
The code is pilot evidence; its hashes do not confer independent review or a completeness proof.
