# RA9X20 — T2b independent Case B model review

## Scope and reviewer independence

Producer: the pre-existing **exp:B4 discovery lane** in the producer's scratchpad, mirrored as
`closure_work/research/alpha9/v2/exp_B4/` by commit
`b15336cf1907d32d6c7ea3afed9404d98da9bb66` (author metadata: alanfuller15,
`noreply@anthropic.com`). The materials identify it as exp:B4, adapted from
exp_A9_A_1nines; they do not identify a unique numbered producer chat. It is not
attributed to ChatGPT round 10 (the README explicitly excludes that source).
Reviewer: **this Codex lane-3 chat, RA9X20**, previously doing lane solver operations;
it did not produce exp:B4 or the MATH.md lemmas. Reviewer scripts import neither
`model_B4.py` nor any producer encoder, except for the explicitly identified static
capture adapter, whose purpose is to extract the producer's original formula.

Scope: version-1 profile numbers **B16 = 4^15, B17 = 4^14 5,
B18 = 4^13 5^2, B19 = 4^12 5^3** only. “Unconditional” means **without 4f.1,
its enumerated C9 lemma, 4g.2, or any bipartition assumption**. It does not remove
the hypotheses of Case B or the explicitly stated elementary lemma dependencies.
No order-24 theorem is claimed. No Case A result, coverage of all alpha=9
profiles, A0/external chain, or issue #3 final-production review is asserted here.

The six labels stay separate:

* **[hand-proof reviewed]**: the elementary implications and encoding argument below.
* **finite check reviewed (independent re-implementation)**: the graph controls and
  primitive sanity checks; not an exhaustive combinatorial classification.
* **SAT/LRAT certificate**: only each particular CNF whose binary LRAT passed the
  pinned cake checker, identified in `RESULTS.md`/`logs/*.json`.
* **reproduced**: the producer static UNSAT results in this run, not its historical timing.
* **producer's summary**: historical `main_b*_v3_out.txt`, control summaries and older runs.
* **conditional**: the producer's `--bip`/`--sides` results, which depend on 4f.1/4g.2;
  none is used for the present verdicts.

A log or a hash is not a proof. The proof objects were checked during this run;
per the requested retention rule they are deleted **only after** cake verification.
The CNFs and regeneration scripts are retained, but the deleted proof bytes must
be regenerated to repeat verification. Historical producer timeouts remain
UNKNOWN/incomplete, exactly as marked in the source materials; they are not UNSAT evidence.

## Mathematical dependency review [hand-proof reviewed]

Write I={0,...,8}, O={0,...,14}, s=15-b, with low masks of size 4 and high masks
of size 5. Case B is triangle-free, edge-maximal, alpha=9, maximum degree <=8,
and every 12-set spans >=12 edges. Nothing below uses a bipartition.

1. **Exact disjointness (4b.2, Theorem 1).** Adjacency of outside vertices implies
   disjoint masks by triangle-freeness. Conversely, if disjoint masks belonged to
   nonadjacent x,y, (MAX) gives a common neighbour z. It cannot lie in I. Its mask
   is disjoint from both others; in these four profiles the three masks have at
   least 4+4+4=12 elements in a 9-set, impossible. Thus x~y iff their masks are
   disjoint. High-high edges are impossible. Three outside vertices cannot form
   a triangle for the same counting reason. Triangles involving I are excluded
   by disjointness. (This specializes the general proof in 4b.2.)
2. **Degree caps DL/D2.** A low vertex has at most 4 outside neighbours. Each i in I
   has r_i<=8 neighbours in O. These follow from R3/F4/F5 for Case B.
3. **M1 (4c.2) uses only F1, alpha=9 and the 12-set rule.** Five low vertices
   through a pair {i,j}, together with I minus that pair, give a 12-set with 10
   edges. If exactly four low vertices Y contain the pair, they contribute eight
   edges in the 12-set (I minus the pair) union Y union {x}. Any other low mask
   meeting the pair contributes at most three edges and meets every Y-mask;
   likewise a high mask containing the pair contributes three. Therefore all
   other low masks avoid the pair, and every high mask contains at most one of
   the pair. The 11-b other low masks are 4-subsets of a 7-set, hence intersect
   pairwise. Each high mask has at least four elements there and intersects them;
   highs intersect each other too. This gives an independent 11-set: impossible.
   Hence q4_ij<=3; in particular low multiplicity <=3.
4. **N3 (4d.1), only its first b<=3 argument is needed.** If a low mask A occurs
   three times, M1 forces every other low mask to meet A in at most one element.
   Those other 12-b low masks have at least three elements of the 5-set I minus A,
   and hence meet pairwise. With all b highs they form a 12-set. A high's low
   neighbours all have its complementary 4-mask, of multiplicity <=3 by M1.
   This 12-set has <=3b<=9 edges, contradiction. Thus low multiplicity <=2.
5. **DH<=2**, despite the producer comment mentioning 4g.2(a), follows directly
   from disjointness and N3: every low neighbour of a high vertex is a copy of
   the unique complementary 4-mask, and there are at most two copies. No 4g.2.
6. **MX/C8 maximality.** For each missing I–O edge xi, a common neighbour must be
   in O and its mask contains i. Equivalently the union of masks of O-neighbours
   of x equals I minus M_x (the other inclusion is disjointness). For a pair in I,
   a common neighbour is some outside mask containing the pair. The remaining
   nonedges between outside vertices have intersecting masks, hence already
   have a common neighbour in I. These are exactly the missing maximality cases.
7. **Floors FL, derived without 4f.1.** Average the 455 twelve-subsets of O:
   an O-edge occurs in a fraction 22/35, so e(O)>=ceil(12*35/22)=20.
   Let E=e(H,L)<=2b (DH), Q=e(L), and k=12-b=s-3. Average the 12-sets H union Y,
   |Y|=k, to obtain

   `(k/s)*E + (k*(k-1)/(s*(s-1)))*Q >= 12`.

   Substituting E<=2b gives Q>=20,18,16,14 for b=0,1,2,3 respectively.
   The comment “4f.1 Consequence” in model_B4.py and README is an unnecessarily
   late citation for **this numerical bound**; it does not import the finite
   C9 enumeration or its bipartiteness conclusion. The derivation above repairs
   the dependency citation without changing any producer clauses.
8. **Symmetry (MATH.md section 5).** Allowed labelings are closed under all
   permutations of I and permutations within each fixed-size outside block.
   A lexicographically least 9x15 incidence matrix has nondecreasing rows and
   nondecreasing columns within blocks. Row order forces column 0 to be five
   zeros followed by four ones. This is existence of a representative, not a
   claim that every graph labeling satisfies double-lex. No BP class grouping.
   Column order places equal low masks consecutively, so low column x!=x+2
   is equivalent to multiplicity <=2. High multiplicity is not restricted.

The dependency chain is acyclic: R3/F1/F4/F5/(MAX)/alpha=9/12-set rule,
Theorem 1 -> M1 -> N3 -> DH -> floors. In particular it never traverses 4f.1,
4g.2, 4j or 4l; no external finite search is used as a premise.

## Producer code audit [hand-proof reviewed]

`model_B4.py` v3.1, default `--sym dlex --nocore`, b=0..3:

* X[k][A] chooses exactly one of 126 low 4-sets (complemented in high slots).
  X implies all nine E membership bits; the exactly-one makes this an exact mask.
* For each allowed pair, y -> no shared E bit. For every chosen type A, its clause
  forces y or a common mask element, giving the reverse implication too. Omitted
  high-high pairs are always nonedges, since 5+5>9.
* P[k,i,j] is equivalent to both membership bits. C8 is their disjunction over
  all slots; M1 is an at-most-three bound over low slots only.
* MX witness z implies y and E. It need not be equivalent: a genuine common
  neighbour can always set one witness true. Existential projection is exact.
* DL/DH/D2 counters, N3, and FL have the scopes reviewed above. Selectors are
  forced true as unit clauses under `--nocore`; none is left as a free relaxation.
* The one-direction prefix lex gates are sufficient: equality of an actual
  prefix forces its gate true, so a first greater bit is forbidden; a lex-valid
  pair has a satisfying intended-prefix extension. The independent implementation
  instead uses exact prefix-equality gates.
* Static TW covers all 455 twelve-subsets of O. The exact candidate checker
  considers every O-subset X: choosing the 12-|X| least frequent I-elements
  minimizes edges for fixed X, because I is independent. It checks 3<=|X|<=12,
  precisely the possible outside sizes of a 12-set. Alpha testing detects an
  independent X with enough uncovered I-elements to reach size 10. A lazy TW
  item is an actual 12-set inequality, and a lazy AL clause asserts that its
  independent-set witness is not independent. Both are valid necessary constraints.
* No `--bip`, `--sides`, BP selector, sigma variable, or 8+7 split is present in
  the captured formulas. The historical conditional/superseded runs are not used.

`dump_producer.py` executes the unmodified producer up to the Solver constructor
and captures `bootstrap_with`, before any call to solve, then stops by a private
exception. It does not run the producer's candidate checker, change clauses,
or seed the independent encoder. All eight main certificates are **static**:
no learned 12-set, alpha, or graph-blocking constraint was needed.

## Independent representation and exactness boundaries

`independent.py` was written in this reviewing chat from the definitions and
necessary conditions above. It does **not** reuse the producer's one-hot mask
encoding, selectors, type-index symmetry, totalizer circuits, ID numbering or
lazy checker. Its primitives are:

* Direct 135 incidence bits, exact 4/5 cardinalities.
* Exact AND gates for shared elements and y equivalent to the negated OR of
  those shared elements (all 105 O-pair variables are retained).
* Sequential cardinality counters for both upper bounds and negated lower bounds.
* Exact prefix-equality gates for double-lex; low-mask XOR comparisons for N3.
* Explicit maximality cover ANDs; low pair incidence counters; the two derived
  floors; the 455 O-only 12-set inequalities.

This static CNF is a **necessary relaxation of the full exact graph model**:
it does not explicitly materialize every mixed I/O 12-set inequality or every
10-set alpha clause. Every graph under review has a double-lex representative
that extends to a satisfying assignment of this static CNF. Therefore its
verified UNSAT suffices to exclude that full graph model. We do not call a SAT
solution of the static relaxation a graph of the original family. The producer
has exact lazy completion, but the certificates here close its static part too.
For controls we separately check the *whole* graph, including all mixed 12-sets
and exact alpha, rather than assume static SAT is enough.

The proof checker certifies the generated clauses, not their mathematical
interpretation; the interpretation/coverage argument is the text review above.
This remains an elementary text review plus finite certificates, not a formal
proof-assistant derivation of the reductions.

## Controls and reproducibility

`controls.py` plants the producer's stored relaxed candidate for each profile into
an independently generated CNF, invokes the pinned CaDiCaL, and checks **every
CNF clause** against its returned SAT assignment. This is a cross-check of an
existing candidate, not an independent search for a new example. The copied
`control_B*.candidate.json` files preserve those models. These are **not** examples
of the target family at threshold 12.

For B16–B18, threshold=0 with M1 dropped (N3 retained, floors off); merely lowering
the threshold while retaining M1 is already UNSAT in the producer experiments.
For B19, threshold=6 with M1/N3 retained (floors off). `check_graph.cpp` independently
builds all 24 vertices and their adjacency from the masks; it exhaustively checks
all 2,704,156 12-sets, computes maximum independent-set size, triangle-freeness,
maximum degree, and every nonedge's common neighbour. Its graph checks do not
use M1/N3/BP as shortcuts. See `controls.json` for exact results and all candidate,
CNF and checker-binary hashes. The exact minima are 5,4,4,6 respectively; all have
alpha=9, maximum degree <=8, triangle-free and maximal.

`unit_checks.py` tests 2,260 primitive assignments (sequential counters, exact
lex gates, signed ANDs). `checker_controls.py` first verifies a tiny genuine
binary LRAT, then offers it against a different, SAT CNF; the pinned checker
rejects it. This binary can return exit 0 even on rejection, so `certify.py`
requires **both** exit 0 **and** stdout exactly `s VERIFIED UNSAT`.

Run from the repository with Python 3.12, python-sat==1.9.dev21 and g++ available:

```sh
TASK=closure_work/out/RA9X20
SCRATCH=/workspace/work/RA9X20-reproduction
mkdir -p "$SCRATCH"
sha256sum -c "$TASK/INPUT_SHA256SUMS"
python3 "$TASK/unit_checks.py"
python3 "$TASK/checker_controls.py" "$SCRATCH"
python3 "$TASK/controls.py" "$SCRATCH"
python3 "$TASK/certify.py" "$SCRATCH" --rerun
```

`--rerun` repeats all certificates; without it `certify.py` skips already verified
completion records.
`cnf/*.cnf.xz` decompress to the exact static DIMACS inputs. `logs/*.json` records
full uncompressed CNF and binary-LRAT SHA256, bytes, binary pins, invocation,
exit status, and elapsed times. The uncompressed input and the LRAT hashes are
not the compressed-file hashes; `SHA256SUMS` covers the retained artifacts.
`runtime.json` pins the reviewed source commit. If later branch changes make
`INPUT_SHA256SUMS` fail, reproduce against those input versions rather than
silently certifying new source text.

An 1800-second or 750-MiB proof limit is a guard, not an UNSAT result: any such
failure is explicitly UNKNOWN and aborts further certification, with its proof
left in scratch. No UNKNOWN is promoted to ACCEPT.

## Review dispositions

**Must-fix defects in the audited unconditional clauses: none found.**
**Should-fix documentation:** replace the FL citation “4f.1 Consequence” with
“averaging the 12-sets H union Y, using E<=2b from N3; see derivation in RA9X20”.
Replace DH's leading “4g.2(a)” citation with “Theorem 1 plus N3 (4d.1)”.
These are citation clarifications, not extra assumptions or code changes.
The audited producer file is left unmodified.

The full exact model is not closed merely by reproducing the old solver's
UNSAT return or by observing a hash match. Final **per-profile ACCEPT/REJECT**
is stated in `RESULTS.md` after checking the newly generated proofs. There is
no verdict on the optional conditional model or any superseded output.

The two encodings share the installed PySAT cardinality library and the same
pinned solver/checker binaries. “Independent” refers to re-deriving and writing
the graph constraint encoding, with different primary variables and gates; it
does not claim independently implemented arithmetic-counter libraries or a
second proof checker. Their precise versions and pins are in `runtime.json`,
`INPUT_SHA256SUMS` and the per-certificate records. This common dependency is
explicit rather than being hidden by the label.
