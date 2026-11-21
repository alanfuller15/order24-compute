# exp:A9-A-1nines (A2-approved, discovery lane; supporting evidence only)

Scope: the 8 pure Case A profiles with n_9 = 1 (MATH.md 4g ledger): v1 84 (4^14,9), 85 (4^13,5,9), 87 (4^12,5^2,9),
90 (4^11,5^3,9), 94 (4^10,5^4,9), 98 (4^9,5^5,9), 101 (4^8,5^6,9), 104 (4^7,5^7,9); m = n_5 = 0..7.

Not a SAT certificate, not a profile_ok level, no coverage credit. Nothing outside this folder was written.

Files
* `r9_arith.py`, `r9_arith_out.txt` - task (a): exact arithmetic of ChatGPT round 9 part 1 section 1, t = 1 and t = 2.
* `model_1nines.py` - task (b): mask model per profile (pysat 1.9.dev21, CaDiCaL 1.5.3), constraints and their
  MATH.md sections in the docstring; lazy (CEGAR) 12-set / alpha constraints, exact checker over all 2^14 subsets.
* `run_all.sh` - sequential runner (nice 19, ulimit -v 1500000, timeout 1800 s, waits for >= 2000 MB available).
* `model_m{0..7}_out.txt` - per-profile logs (last lines: JSON result and /usr/bin/time CPU line).
* `runner_log.txt` - start/exit per profile.
* `verify_graph.py` - independent brute-force check (all C(24,12) 12-sets, exact alpha, (MAX)) of a candidate JSON;
  used only on the non-vacuity control candidate.
* `candidate_m7_thr8.json`, `verify_control_out.txt` - non-vacuity control (12-set threshold lowered to 8; NOT a graph
  of the family).

Model: G is determined by the 14 masks (Theorem 1 4b.2, (P11), (R3), (F4)); constraints are the defining properties
(12-set rule, alpha <= 9, Delta <= 9 / r_i <= 8 (F5), saturation identity from (MAX)+(F4)), plus the redundant helper
M1 (4c.2 / 4d "M1 in Case A"). No round-9 claim, no 4f.1 C9 lemma, no bipartiteness is used. Symmetry: masks sorted
within the low and within the high slots; WLOG the smallest low mask is {0,1,2,3} (S_9 transitive on 4-sets).
Because the model is exact, a passing candidate would be an actual order-24 graph; the script stops on one.

## Results (2026-11-19)
All 8 profiles: **0 survivors** (UNSAT on the first solve, from the static constraints alone: all 11-subsets of F
span >= 12 edges, degree caps, r_i <= 8, saturation identity, M1, symmetry). No lazy constraint was needed. Summary in
`model_1nines_out.txt`. Total CPU about 0.35 core-hours (all runs incl. controls). Task (c) (round-9 claims) not run:
no survivor needs a claim. Controls: lowering the threshold to 0 or 8 gives models (brute-force verified for 8,
min 12-set edges = 8, triangle-free, alpha 9, (MAX) holds), threshold 11 is still UNSAT for 4^7 5^7 9.
