# A9 final replay partition fix

## Diagnosis from the downloaded a9v5 artifacts

The production unit is `(case, profile index, initial cube)` (`a9run.units`).
The final checker does **not** partition these units: it concatenates 131 B and
299 A profiles and assigns entire profiles by `profile_position % N`.
Thus B011/B012/B013/B014 share parts with A072/A073/A074/A075 at N=32.
At N=16 the same pairs remain in 11–14; at N=8 they remain in 3–6.
Increasing N cannot divide the work of any one of those profiles.

| Part | Run | Completed replay records | Dominant completed profiles | CNFs still present at interruption |
| --- | --- | ---: | --- | --- |
| 11 | 44836391638 | 3865 | B011: 2097, A072: 1756 | A072: jobs 3798, 3864, 3867 |
| 12 | 44836394883 | 2882 | B012: 2323, A073: 547 | B012: jobs 2881, 2882, 2884, 2885 |
| 13 | 44836398694 | 3060 | B013: 2992, A074: 56 | B013: jobs 3039, 3052, 3055 |
| 14 | 44836402388 | 2663 | B014: 1773, A075: 879 | A075: jobs 2660, 2662, 2664, 2666 |

All four `final_full.log` files end in `KeyboardInterrupt` waiting on the replay
pool, without a verdict. The oldest leftover CNF in each artifact was written
at 05:05:46, 05:06:54, 05:03:56, and 05:06:14 UTC respectively; the corresponding
LRAT files were still being written around 05:08:22–28. This is a queue of
thousands of replays, not evidence of one CaDiCaL invocation running 5.5 hours.
The old logs have no start/per-leaf timing, so they cannot establish a rigorous
upper bound on each entire replay (including rebuild). This patch adds elapsed
seconds per replay. No replay checkpoint/resume exists: restarting repeats all
completed work. Producer resume in a9run is irrelevant to this checker.

A separate failure-reporting bug explains the green workflow runs: `exp.yml`
uses `timeout ... | tee ... || true`; interruption kills a9final before it can
write GATE_FAIL. The workflow Gate then sees no failure marker.

## Change and soundness

`a9final.sh` now invokes `a9check --final --partition leaves`. All parts parse
the same ordered results files as before. From the list of **all UNSAT record
occurrences**, part K/N replays entries K, K+N, K+2N, ... . This includes
unselected, duplicate, and extra-profile records, just as the old final check
did across all parts. Within each source/profile the costly leaves are spread
among all parts instead of staying together. Cardinalities differ by at most
one, rather than thousands versus 13.

Every part checks structural coverage of the whole certified list, preserving
the existing first-source/first-complete-file-per-unit selection and binary
cube-tree completeness rules. Foreign leaves are explicitly **provisional**;
a part's verdict alone establishes no claim. A final claim requires ALL K=0..N-1
with identical N, ordered input digest, code digest, and `partition leaves-v1`.
The slices are disjoint and exhaustive, so if all parts pass, EVERY UNSAT
record has independently passed rebuild/SHA-256, CaDiCaL exit 20 and exact
cake_lpr verification. At that point all provisional flags are backed by their
owning part's replay, and the global coverage check is exactly the old
unpartitioned replay-passed coverage check. Any failed replay rejects its owner;
missing coverage, malformed tags and MODEL records still reject the claim.
No source union, proof acceptance rule, CNF clause or lazy constraint changes.
The legacy `--partition profiles` behavior remains available and is the default
for direct a9check calls.

The wrapper creates GATE_FAIL **before** downloads and removes it only after
both the final verdict and a9gate succeed. Timeout/interruption therefore fails
closed. Full logs are retained, including new replay durations.

## Validation and rerun

Run `python3 -m unittest discover -s exp -p test_a9final.py -v` (six tests) and
`bash -n exp/a9final.sh`. Tests exercise disjoint/exhaustive allocation including
extra/duplicate records and empty parts, whole-check versus all-parts agreement,
failed replay ownership, missing trees, bad flags/tags, MODEL records, no mixing
sources/files, hash/CaDiCaL/exact-cake checks, and early failure markers.
SAT calls in the partition tests are mocked; this is not a full certificate replay.

Rerun **all 32** parts from one commit of this branch, not only 11–14, with
`script=a9final.sh`, `args="K/32 4"`, `name=a9v6_final_pK`. The collector is updated
to that new artifact generation to avoid mixing old and new layouts. Retain the
same explicit producer RUN_ID set, or verify identical input digests. Old v5
verdicts cannot fill any v6 slot. The full rerun was not dispatched by this fix.

The evidence supports the <5-hour target by spreading the four congested
profile pairs across 32 workers groups, instead of assigning thousands of
leaves to one group. It is **not** a measured wall-time guarantee: this patch
has not run all 32 full jobs, and leaf costs/runner speed can vary. The retained
per-leaf timings make any residual straggler identifiable; increasing N now
actually divides each expensive profile rather than leaving it indivisible.
