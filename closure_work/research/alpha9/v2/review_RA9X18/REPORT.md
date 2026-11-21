# RA9X18: review of MATH.md section "### 4k" against review_RA9X12/

Verdict: **ACCEPT WITH REPAIR** (two wording fixes; R3 is optional). No numbers, profiles or certificate claims are wrong.

MATH.md was not edited. No git activity.

## Checks done

1. **Profiles.** 4k lists v1 84, 85, 87, 90, 94, 98, 101, 104 = 4^(14-m) 5^m 9, m = 0..7. This matches
   VERDICT.txt ("v1 84, 85, 87, 90, 94, 98, 101, 104 (m = 0..7)"), the gen_mine.py and dump_orig.py profile
   convention (s + m = 14, m = n_5), the exp_A9_A_1nines README and the 4h setting list. OK.
2. **Certificates.** For all 16 instances (orig_m0..7 and mine_m0..7) I recomputed sha256 on disk for the CNF, the LRAT
   and the cake output. All of them match the cnf_sha256, proof_sha256 and cake_out_sha256 values in orig/log.txt and
   mine/log.txt. Every *.cake.txt has exactly one "s VERIFIED UNSAT" line. Every *.cadical.txt has "s UNSATISFIABLE"
   and "exited with non-zero status 20". Both logs record cadical_exit=20, cake_exit=0 and VERIFIED on every line.
   OK.
3. **Input hashes.** inputs_sha256.txt gives model_1nines.py c5f29088…6a43, which matches the file now on disk and
   the "c5f29088…" in 4k. The MATH.md that RA9X12 reviewed (c336b97b…) is byte-identical to MATH.md.pre_4i. Diffing it
   against the current MATH.md, nothing changed before line 1233 except the 4h ledger header. All the lemmas 4k
   cites are therefore byte-identical to the version RA9X12 reviewed. OK.
4. **Cited lemmas exist and are the ones the model uses.** These all exist: Theorem 1 = 4b.2 (l.263), (P11)
   (l.215, first sentence: a = 9 vertices have no O-neighbour), (R3) (l.27), (F4) (l.42), (F5) (l.43), (MAX) (l.25),
   the saturation identity "clause family (C9)" (section 4 review items, l.144), 4h.1 Lemma M1 in pure Case A
   (l.1100), and the 12-set rule (section 1). They correspond one-to-one to the constraints in gen_mine.py
   (E, T1, DG, RI, MX, Q4, TW, SB) and in model_1nines.py (G1–G4, D1, D2, MX, M1, static TW). The phrase "12-sets
   containing v and no I-vertex" is exactly the static TW family, the 11-subsets X of F, using e(X ∪ {v}) = e(X).
   [AL] and the remaining 12-sets are lazy only. All eight model_m*_out.txt show "iterations": 1, "learned_tw": 0
   and "learned_alpha": 0, so "UNSAT at the first solve, no lazy clauses enter" is true. dump_orig.py states the
   same. OK, apart from R1 and R3.
5. **Controls.** controls_out.txt shows thr 0 and thr 8 SAT (exit 10) in both encodings, every decoded model
   check ALL_OK, and the cross-feeds consistent (thr8 to thr8 SAT, thr8 to thr12 UNSAT, both directions). OK.
6. **Label and overclaim.** The section says "computer-checked exclusion of a reviewed finite model", "not a hand
   proof", "separate from the certified production run" and "No order-24 theorem is claimed". The ledger is
   "reporting only … not a `profile_ok` level". OK.
7. **Ledger arithmetic.** After 4j, Case A has exactly these 8 open and Case B has B18 and B19 (2). After 4k, Case A
   is 8 − 8 = 0 and Case B stays at 2. Both are consistent. OK.

## Required repairs (exact wording)

**R1 (ambiguous citation).** The phrase "C9" can be confused with the enumerated **Finite lemma C9, 4f.1**. The
original model's README says explicitly that it does not use 4f.1.
Replace
  `(MAX) with the C9 saturation family,`
with
  `(MAX) via the saturation identity (clause family (C9) of the section 4 review items; not the enumerated lemma 4f.1),`

**R2 (closing paragraph: wrong base list and wrong dependency).** Two problems. First, the ledgers since 4g count
open profiles of the **level-32 list (4f)**, not of the whole v1 list. Second, "this rests on 4f.1" makes the 4k
exclusions look conditional on 4f.1, but the model uses neither 4f.1 nor 4h.2.
Replace
  `All Case A profiles of the v1 list are now excluded by reviewed hand proofs (4g–4i) plus the 4k model check; this
rests on 4f.1 and the other lemmas cited, and changes nothing`
with
  `Every Case A profile of the level-32 list (4f) is now excluded: by the reviewed hand proofs of 4g–4i (partly
conditional on 4f.1, as cited there) or by the 4k model check (which uses neither 4f.1 nor 4h.2). This changes nothing`

## Optional (recommended)

**R3 (M1 provenance).** model_1nines.py itself cites 4c.2/4d "M1 in Case A", which 4d states for |H| = 9. Its
docstring argues the extension, and 4h.1 is the reviewed statement covering these profiles. gen_mine.py cites 4h.1.
Replace
  `4h.1 (M1),`
with
  `4h.1 (M1; the original encoding cites 4c.2/4d "M1 in Case A", extended to these profiles by 4h.1),`
