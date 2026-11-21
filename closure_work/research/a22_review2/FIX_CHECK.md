# Fix check: review RC22c fixes F1-F4 in research/a22_close/ (against a22_close.pre_fix/)

Reviewer of RC22c (REVIEW.md), 2026-11-17. Read-only on the package; all runs at nice 19; my files are in fix/ and t80/.

**VERDICT: ACCEPT WITH FIXES (documentation only).**
- The code fixes F2 and F3 are correct, and every control behaves as it should.
- F4 is done.
- F1 is done in TRUST_ENTRY.md and LEMMA_A22.md. It is **not** done in the text that will actually be pasted into the
  route (COVERAGE_PLAN.md's route diff).
- The install instructions are stale.
- Nothing affects soundness.

## What I checked

**The diff is limited to what was described.**
- `diff -r a22_close.pre_fix a22_close` touches only these: COVERAGE_PLAN.md, EXCEPTION_CHECK.md, LEMMA_A22.md,
  LEMMA_C22c_EXEMPT.json, TRUST_ENTRY.md, code/union_lemma.py, SHA256SUMS, plus the new SHA256SUMS.pre_fix.
- cnf/, data/ and out/mx_witnesses.txt are unchanged.
- `sha256sum -c SHA256SUMS` passes, and it lists every file except the two SUMS files.

**F2 and F3 code.** I read union_lemma.py again in full.
- It sets `nonpass == []`.
- Per group, it requires the CR tag set to equal the records tag set.
- It re-hashes 7 files under A22C_DIR when the layer uses exemptions.
- A missing argument or a missing file fails.
- LEMMA_PINS equals EXEMPT.json lemma_pins, and both new pins equal the real hashes of excB_gen.py and
  mx_witness_check.py.

| Control | Result |
|---|---|
| L80, L81, L82 real, A22C = a22_close | OK, exit 0 (all three) |
| no 4th argument | NOT OK ("a22c folder not given"), exit 1 |
| A22C nonexistent | NOT OK (all 7 files listed), exit 1 |
| each of the 7 pinned files corrupted in a copy (one at a time) | NOT OK naming exactly that file, exit 1 (7/7) |
| B302.cnf removed | NOT OK, exit 1 |
| intact copy | OK, exit 0 |
| pre-fix EXEMPT.json (old pins) | AssertionError, exit 1 |
| exemption list short / wrong layer / c = m − 21 / tag not in F / empty for 80 | NOT OK, exit 1 (each) |
| exempt tag also certified | OK (sound) |
| **F2 control: failing duplicate line for a passing tag** | **NOT OK, exit 1 (was OK before the fix)** |
| proof-hash mismatch; CR line without record; record without CR line; extra G1 record for a tag that passes in G2; formulas hash matching only in its 8-char prefix; a group's CR file missing | NOT OK, exit 1 (each) |
| restored copy | OK, exit 0 |

**F4.** The EXCEPTION_CHECK.md note and the TRUST_ENTRY line 17 marker are correct.

## Remaining fixes

1. **F1 in the route diff (must-fix: this is the text that goes into LOW_LAYERS_ROUTE.md).** COVERAGE_PLAN.md still
   proposes three lines with the old scope:
   - line 65: "it is used only for the formulas listed in a22c/LEMMA_C22c_EXEMPT.json";
   - line 74: "McKay-max (layers 80–82 only)";
   - line 76: "Used only by Lemma E, so only by the exempt tags."

   Each needs the same qualifier as TRUST_ENTRY: *directly* only by those tags, and Theorem L_m for every m ≤ 79 and
   any final order-24 result inherit it through L80. The note after the closure template (line 106) is right, but it
   is not part of the route text.

   LEMMA_A22.md line 121 ("used only by Lemma E, so only by the 7 tags") should also read "directly". Line 124 now
   qualifies it, so this is minor.
2. **Install instructions (should-fix).**
   - COVERAGE_PLAN.md line 34 still gives the old union_lemma.py hash (2a4004d5…). It is now 4b06f5e3….
   - Line 35 still gives the old EXEMPT.json hash (6b72f21d…). It is now e40b1737….
   - Line 44's command lacks the new 4th argument (`a22c`). Run as written, it would print NOT OK. That failure is
     safe, but the instruction is wrong.
   - The dry-run files out/UNION_DRYRUN_L8x.txt are from the pre-fix script. Regenerate them with the 4th argument.
   - REVIEW_BRIEF.md line 120 has the same old usage. This is cosmetic.
3. **Optional.** A *passing* duplicate CR line is still accepted. close_group rejects it, through
   `len(L) == len(recs)`. This is sound, since both lines are passing checks of the same pinned certificate. Adding
   "one CR line per tag" would make union_lemma no weaker than close_group in every respect.

Once fixes 1 and 2 are made (text only, no code change), I would accept without further re-runs, provided that
union_lemma.py and EXEMPT.json are unchanged from 4b06f5e3… and e40b1737….
