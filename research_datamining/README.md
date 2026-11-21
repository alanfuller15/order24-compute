# Bidirectional mining handoff

This is a read-only data-mining package, **not a certificate nor a code change to the live solver**.

`FINDINGS.md` contains the observed findings and proposed experiments.

`analyze_repo.py` reads an existing local checkout of the public `order24-compute` repository and any metadata ZIPs supplied to it; it never calls GitHub, modifies the checkout, invokes a SAT solver, or approves a proof. Example:

```bash
python3 analyze_repo.py --repo ~/order24-compute --meta 'source_meta/*.zip' --out metrics.json --bank lazy_sources.jsonl
```

`L83_h0_seed_candidates.json` contains 1,636 universal nine- and twelve-set inequalities extracted from an existing *producer* record, labeled as untrusted candidate optimization data. It is not an UNSAT certificate. The `origin_meta_zip_sha256` and original proof/CNF hashes provide provenance. Each item must be regenerated via the target encoder and included in its own proof CNF before a verifier can accept any refutation. Inspect `FINDINGS.md` first.

`source_meta/` bundles the three 16–18KB metadata artifacts only; no gigabyte-scale proof archives are included. All numerical counts are from inspections of actual repository files or these metadata artifacts, with source distinction recorded in the report.
