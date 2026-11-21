# exp:B4 (discovery lane; supporting evidence only)

Scope: the 4 open Case B profiles 4^(15-b) 5^b, b = 0..3 (v1 B16 4^15, B17 4^14 5, B18 4^13 5^2, B19 4^12 5^3).
Not a SAT certificate, not a profile_ok level, no coverage credit (until separately reviewed and LRAT-checked).
Nothing outside this folder was written. ChatGPT round 10 is not used.

## Model (`model_B4.py`; constraints and MATH.md sections in its docstring)
G is determined by the 15 masks (Theorem 1, 4b.2). Families (selector names):
DL low d_O <= 4 (R3, D = 8); DH high d_O <= 2 (4e.1 / 4g.2(a), via N3); D2 r_i <= 8 (F5); MX saturation identity
((MAX)+(F4), clause family C9); C8 every pair of I in some mask ((MAX), C8); M1 q4 <= 3 (4c.2); N3 low multiplicity
<= 2 (4d.1); FL e(O) >= 20 (4d.1(ii)) and e(L) >= 20/18/16/14 (4f.1 Consequence, averaged 4e.1 inequality);
TW the 12-set rule (455 12-subsets of O static, every other 12-set exact and lazy); LAZY alpha <= 9 and lazy 12-sets
(exact checker over all 2^15 subsets X of O with the 12-|X| least frequent elements of I).
Symmetry: MATH.md section 5 (SYM)(a),(b) and (C13) (double-lex on the 9 x 15 incidence matrix, column 0 = {5,6,7,8}).
A candidate passing every check would be an actual order-24 graph of (T), Case B; the script stops on one.

Run "+4g.2" (`--sides h`, labelled; conditional on the accepted 4f.1 (enumerated lemma C9) and 4g.2): G[O] has a
bipartition into independent classes X (8) and Y (7); case split on h = number of a = 5 vertices in X (h = 0..b);
same-class pairs non-adjacent (masks meet); static instances of TW for X u U (U 4-subset of Y), Y u W (W 5-subset of
X), X u J (|J| = 4), Y u J (|J| = 5) (family BP). Symmetry: (SYM) with the four groups (block, class).

## Results (2026-11-19)
Unconditional model (no 4f.1 / 4g.2), model_B4.py v3 (= v2 encoding: double-lex, Q floor), files main_b{0..3}_v3_out.txt:

| profile | result | CPU (user s) | wall s | lazy items |
|---|---|---|---|---|
| 4^15 (B16) | 0 survivors (UNSAT, 1st solve) | 62.6 | 216 | 0 |
| 4^14 5 (B17) | 0 survivors (UNSAT, 1st solve) | 232.3 | 673 | 0 |
| 4^13 5^2 (B18) | 0 survivors (UNSAT, 1st solve) | 373.3 | 1021 | 0 |
| 4^12 5^3 (B19) | 0 survivors (UNSAT, 1st solve) | 400.0 | 940 | 0 |

Earlier timeouts on the then heavily contended host (load ~9 on 2 cores): main_b3_v1_timeout_out.txt (v1 symmetry,
476 CPU-s / 1800 s wall), main_b3_v2_out.txt (v2, 389 CPU-s / 1800 s wall). Not results.

+4g.2 model (`--sides h`, labelled, conditional on 4f.1/C9 and 4g.2), files sides_b{b}_h{h}_out.txt: all 10 cases
(b,h) = (0,0),(1,0),(1,1),(2,0..2),(3,0..3) 0 survivors on the first solve, 10.6-34.5 CPU-s each (186 CPU-s total).
Core runs (assumption selectors, not minimised) in core_sides_*_out.txt.

Which constraints did the work: thr 0 (12-set rule switched off except through its proved consequences M1, N3; FL
off; alpha <= 9 still lazy) is already UNSAT for b = 0, 1, 2 unconditionally (ctl_main_b{0,1,2}_thr0_out.txt) and for
the +4g.2 cases tried at thr 0, (b,h) = (0,0), (1,0), (1,1), (3,0), (3,2), (3,3) (b = 2 not run at thr 0), but SAT for (3,1); dropping M1 at thr 0 makes b = 0, 1, 2 satisfiable (ablate_main_*). So for
b <= 2 the pair-incidence bound M1 (q4 <= 3) together with N3, Theorem 1 structure, MX, C8, degree caps and alpha <= 9
is decisive; for b = 3 the 12-set rule itself is needed (thr 0 SAT; +4g.2 case h = 1: thr 6 SAT, thr 8 UNSAT).

Controls (non-vacuity; every model found was brute-force verified as a graph by verify_graph_B.py: triangle-free,
Delta <= 8, alpha = 9, (MAX), exact min over all C(24,12) 12-sets):
* unconditional b=3: thr 0 SAT (v1 and v3), thr 6 SAT (v1, v2); verify_control_thr0/thr6/thr6_v2_out.txt,
  verify_ctl_candidate_main_b3_thr0_out.txt (min 12-set edges 6).
* unconditional thr 0 with M1 dropped, b = 0, 1, 2: SAT, verified (verify_ablate_main_b*_out.txt).
* +4g.2 b=3 h=1: thr 0, 2, 4, 6 SAT (ctl_candidate_b3_h1_thr*.json, verified; check_sides_out.txt confirms the slot
  classes are independent of sizes 8 + 7), thr 8 UNSAT (353 s). b=0 h=0 thr 0 with M1 dropped (or M1+N3 dropped): SAT,
  verified.
No candidate at threshold 12 appeared in any run.

Versions: model_B4_v1.py (v1 symmetry, no Q floor), model_B4_v2.py (double-lex, Q floor), model_B4.py (v3.1: +
--sides, with the same-class low-high fix; superseded_v3_0/ holds the pre-fix runs, not used).
