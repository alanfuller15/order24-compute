# T2b certification verdicts

The scope and dependency review are in [REPORT.md](REPORT.md). These verdicts
apply only to the four indicated unconditional models, without 4f.1 or 4g.2.
ACCEPT requires the reviewed graph-to-CNF implication plus both proof checks;
no larger order-24 theorem is asserted.

| Profile (v1) | Incidence profile | Verdict | Producer CNF | Independent CNF |
|---|---|---|---|---|
| B16 | 4^15 5^0 | ACCEPT | VERIFIED UNSAT | VERIFIED UNSAT |
| B17 | 4^14 5^1 | ACCEPT | VERIFIED UNSAT | VERIFIED UNSAT |
| B18 | 4^13 5^2 | ACCEPT | VERIFIED UNSAT | VERIFIED UNSAT |
| B19 | 4^12 5^3 | ACCEPT | VERIFIED UNSAT | VERIFIED UNSAT |

## Binary pins

- `bin/cadical`: `eae671d6fab57f7bf909e621adee2a2bd550a0ae0b561065c815f599c7696fe8` (3.0.1)
- `bin/cake_lpr`: `29e02af756c1f0fc4ccac78e9a908e0d8ef01201786f257f1b27b26603390798`

## Full uncompressed CNF / binary-LRAT hashes

### producer_B16

- CNF SHA256: `f0ed60cbc464367c94c32d60f2c54e2add25f5c86899d930558b375ac4248a1c`
- Binary LRAT SHA256: `a8e0689ff68fcbb395b1aa79f3360ec5605832a9e80d8d97a0db0fdeba18b634`
- LRAT bytes: 80345642; proof deleted only after pinned cake verification.

### independent_B16

- CNF SHA256: `46ed1d61c5ac6d784fd5c9d61563a66c92a20887a93c357af1ff35ba863e759d`
- Binary LRAT SHA256: `1f591daf940728d9e7373c858c553f9882c9170d86515c2aa0a77b8ecdcbd77c`
- LRAT bytes: 48979324; proof deleted only after pinned cake verification.

### producer_B17

- CNF SHA256: `e203177ef7f4d627daccd1ac37a331d90ab9b0ce11a9a4ebf8db3334b8950a09`
- Binary LRAT SHA256: `26614cbf1ea2a3ac80a39e6c591141545e6d4efa4b6fa25c6cff1bc8a142aa1b`
- LRAT bytes: 162313658; proof deleted only after pinned cake verification.

### independent_B17

- CNF SHA256: `b8a85348cdc90a2d8c71fe57d4b8ab33357454f30fda3032bbd2ef5f4e6daacc`
- Binary LRAT SHA256: `5f4fea409867ab25796115e9e37677a7c6a3fd50ba65038f3b5ebfc2ec8b6167`
- LRAT bytes: 94843275; proof deleted only after pinned cake verification.

### producer_B18

- CNF SHA256: `3e61cf593bc52a949eb4a1e9172b754b60e3648d65e8702d0a8416e48dfbc1fc`
- Binary LRAT SHA256: `79e3a55bd25959d93fdc3bdb134d278ed87a04593713696ee4d792a8e8ea2bea`
- LRAT bytes: 223123309; proof deleted only after pinned cake verification.

### independent_B18

- CNF SHA256: `859e614c2869f0fcefa42591f58a1605336b268067fcb909a9a44e10bb5f352e`
- Binary LRAT SHA256: `92e332e190a178a0a75b0f4138c1ca488fe1b0a761605d7bc399c5ea8f627e0d`
- LRAT bytes: 175945854; proof deleted only after pinned cake verification.

### producer_B19

- CNF SHA256: `2ce4bfd56143f1c6f37f917cb26afbba653473b34de89923bbf1d19bc9758d9e`
- Binary LRAT SHA256: `b58edb603e2f8ad689e983d144ff1d5a2477272ca5c1f087d0f41608af02a39b`
- LRAT bytes: 292338555; proof deleted only after pinned cake verification.

### independent_B19

- CNF SHA256: `6de75c3899a9aab26a160d0e363e253725aff5a6b4f9e29e86cc1cf9ed5a9e12`
- Binary LRAT SHA256: `8eedcf02976880c90a7a7406ddd5d4834fa8146465217211831dbdfe2cb631c8`
- LRAT bytes: 230821076; proof deleted only after pinned cake verification.

## Controls

All four known relaxed candidates give SAT in the independent encoding, with
every CNF clause checked against the returned assignment. The independent
24-vertex graph checker confirms triangle-free, degree <=8, alpha=9 and (MAX).
It enumerates all 2,704,156 twelve-sets per candidate. Minima B16/B17/B18/B19:
5/4/4/6 edges. B16–B18 use threshold 0 and drop M1; B19 uses threshold 6 and
retains M1. Floors are off. These are not threshold-12 counterexamples.

The primitive tests pass 2,260 assignments. The pinned cake checker verifies a
tiny genuine LRAT and rejects it against a changed SAT CNF, despite returning
exit 0 in the negative control. Acceptance therefore requires its exact stdout.

`INPUT_SHA256SUMS` pins reviewed inputs relative to the repository root;
`SHA256SUMS` pins all retained deliverables relative to this directory. The
per-certificate JSON and full solver/checker logs are under `logs/`; all eight
static CNFs are retained as `cnf/*.cnf.xz`. No LRAT is committed, as requested.
