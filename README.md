# order24-compute

Compute workers for the Erdős problem #128 order-24 project: each edge layer is reduced to a set of SAT formulas, and each
formula needs an LRAT unsatisfiability certificate. GitHub Actions jobs run the (untrusted) producer — CEGAR search with
PySAT, proofs by CaDiCaL, trimmed by lrat-trim, self-checked by cake_lpr — and upload records and proofs as artifacts.

Nothing produced here is trusted: every record is rebuilt from the formula and its lazy list by the pinned encoder and its
proof is checked by the CakeML-verified checker cake_lpr (`code/gcert90d.py`), by an independent auditor, elsewhere.

- `code/`: encoders (cegar91/90/90b/90c), producer `grun90.py`, cube-and-conquer `ccc90.py`, checker `gcert90d.py`
- `data/formulas89_c66.json`: layer 89, 432 formulas (c >= 66)
- `bin/`: CaDiCaL 3.0.1, lrat-trim, cake_lpr (x86-64 Linux); `SHA256SUMS` pins everything
- `chunks/<wave>/*.txt`: the tag lists of each job; `ckpt/`: lazy lists carried between waves
