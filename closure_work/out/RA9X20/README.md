# RA9X20 (T2b / issue #4)

Start with [RESULTS.md](RESULTS.md) for per-profile verdicts and full CNF/LRAT hashes,
then [REPORT.md](REPORT.md) for the independent review, mathematical dependencies,
encoding details, limitations and reproduction commands.

- `cnf/`: exact static DIMACS inputs compressed with xz (both encodings, B16–B19).
- `logs/`: full solver/checker logs and structured certificate records.
- `independent.py`: independent direct-bit re-encoding (no producer imports).
- `dump_producer.py`: capture adapter for the unmodified producer's static CNF.
- `certify.py`: binary LRAT generation and pinned cake verification.
- `controls.py`, `check_graph.cpp`: planted SAT controls and independent full-graph checks.
- `unit_checks.py`, `checker_controls.py`: primitive tests and checker positive/negative controls.
- `validate.py`: retained-CNF and acceptance-record integrity checks.
- `summarize.py`: rebuild the verdict table from certificate records.
- `INPUT_SHA256SUMS`: reviewed input hashes, relative to the repository root.
- `SHA256SUMS`: retained artifact hashes, relative to this directory.

The LRATs are intentionally not retained after successful cake verification.
Their recorded hashes are identifiers, not replacements for proof objects.
No optional bipartition model or order-24 theorem is certified here.
