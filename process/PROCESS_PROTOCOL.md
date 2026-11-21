# Order-24 compute throughput: next iteration

Scope: **process engineering only**. Do not reactivate the abandoned 10+14 inequality route. Do not change the mathematical obligations or the active `a9v6` final claim.

## Source code evidence (main, 2026-11-21)

- `exp/a9check.py`: replays every assigned UNSAT occurrence, rebuilds exact CNF, calls `bin/cadical` to generate LRAT, optionally trims, then checks with CakeML. No durable per-leaf checkpoint. Success determined at end of part.
- `exp/a9final.sh`: downloads all source artifacts in each of 32 jobs; all jobs re-read all record files, although each checks only a slice. Uses a fail-closed `GATE_FAIL`/`GATE_PASS` gate.
- `exp/a9run.py`: `multiprocessing.Pool(maxtasksperchild=1)` and no independent replay checkpoint. A9 solver's cached twelve-set masks are recreated across worker lifetimes.
- `exp/a9solve.py`: uses 2,704,156 twelve-set masks and full stable `argsort` to select a small batch. An exact partial-sort candidate and an indexed coverage candidate are in the *separate* previous performance package.
- `.github/workflows/exp.yml`: `timeout ... | tee ... || true`, then upload, then Gate. This is fail-closed for A9 via its pre-created `GATE_FAIL`, but command exit statuses are masked for **other** scripts not using a gate.
- `.github/workflows/refill.yml`: deliberately holds a runner idle up to 480 s so self-chaining can compensate for throttled cron. Assess scheduling cost independently; never remove it without equivalent reliability.

## Delivery order (do not implement all simultaneously)

### 0. Do not interfere with live certificate jobs

Freeze the current code digest, input record order, proof acceptance predicate and `leaves-v1` partition mapping. Do not splice any new part into an `a9v6` set. Use a separate experimental branch and a new artifact generation name for any changed verifier.

### 1. Telemetry: isolate where the time goes

Emit machine-readable per-leaf stage timings: CNF rebuild, CaDiCaL, trim, wait for Cake lock, Cake verification, cleanup; plus proof bytes, temporary disk high-water, process peak RSS and output latency. Measure p50/p95/p99, aggregate CPU-seconds and critical-path wall-clock. Record operator time (artifact fetch, dependency installation, runner `sleep`). Stop changing heuristics if the bottleneck is an idle lock or I/O rather than solver CPU.

### 2. Freeze a **read-only** cost plan before changing scheduling

`a9_workload_plan.py` is included. It mirrors A9's ordered UNSAT occurrence IDs (including duplicates and extra profiles), existing composite input digest, and proposes an exhaustive, disjoint schedule. `--mode striped` gives the current `i mod N` baseline; `--mode weighted` uses longest-predicted-work-first bin packing. Both are accounting experiments only. Neither verifies proofs, and neither may be fed into the existing `leaves-v1` collector.

Its cost estimator uses existing `cadical_seconds`, `cake_seconds`, `proof_bytes` metadata; these estimates are imperfect because timings may come from different machines or producer workflows. Fit the weights to actual per-leaf replay timings before declaring an improvement. Longer-running leaves should be distributed, not grouped by old profile position. No claims based purely on synthetic data.

Usage:

```bash
python3 a9_workload_plan.py /path/to/first/results.jsonl /path/to/next/results.jsonl \
  --parts 32 --mode weighted --max-records 100 --target-cost 500 \
  --output /tmp/a9_next_plan.json --compare
python3 -m unittest -v test_a9_workload_plan.py
```

**Important:** supply results paths in the *exact same order* used by the frozen checker. If that is not available, no cross-run identity claim is justified. The manifest tracks source file ordinals, record line positions, SHA-256 of the exact line bytes, record index and expected CNF SHA-256. It does not inspect lazy payloads or prove any graph-theoretic claim.

### 3. Resumable proof cache (protocol v2; requires independent review)

Most of the wasted time comes from rerunning completed CaDiCaL work. Proposed cache entry:

```json
{
  "protocol":"a9-proof-cache-v2",
  "input_digest":"FULL_SHA256",
  "code_digest":"FULL_SHA256",
  "unsat_occurrence":12345,
  "source_file_ordinal":2,
  "record_line":981,
  "record_line_sha256":"FULL_SHA256",
  "cnf_sha256":"FULL_SHA256",
  "proof_sha256":"FULL_SHA256",
  "proof_object":"12345.lrat.gz"
}
```

The proof is **untrusted binary evidence**, not a trusted `pass` boolean. To use it: verify input occurrence identity; decompress proof into a unique temp path; verify proof object SHA; independently rebuild exact CNF from (profile, cube, original lazy items); compare its full SHA to the record; **run CakeML on reconstructed CNF and cached proof**; require the exact verification line, valid status, no exception, and log the check. If absent, corrupt, or not Cake-verified, regenerate proof with CaDiCaL, trim optionally, and check CakeML. A cached proof must never skip CakeML. Cache is namespaced by complete input and code digests, occurrence ID and CNF SHA. Avoid shared mutable CNF paths and shell-tool injection. Use `fsync` followed by same-filesystem atomic rename when writing each entry. Do not accept an incomplete temp file.

Persist a subset of *expensive* proofs (e.g., high CaDiCaL time but bounded compressed size) if artifact storage is limiting. The entry's existence cannot count as a verified leaf. It can, however, avoid rerunning CaDiCaL after interruption. A job may end with `GATE_FAIL` and still upload **untrusted cache objects** via the existing `if: always()` artifact path; a fresh job must recheck each cached proof with the pinned CakeML checker before counting anything. Preserve 10+ minutes of job deadline margin for artifact upload.

**Critical protocol distinction:** Current A9 final explicitly reruns CaDiCaL for every occurrence. Reusing a proof object changes this process obligation, even though a valid, independently checked LRAT proof is mathematically sufficient. Version the protocol (`proof-reuse-v2`), get an independent review, and launch an all-new complete claim generation. Do not retrofit cached results into an active `leaves-v1` campaign.

### 4. Resumable **chunks** and an independent whole-cover gate

For a future generation, split the *ordered occurrence set* into bounded independent chunks, each with a manifest of exact occurrence IDs, input hash and code hash. Each chunk verifies every assigned proof with CakeML. An interrupted chunk is incomplete; its partial cache can be retained as untrusted data for the next attempt. The collector must prove that successful chunk assignments form a **disjoint exact cover** of all UNSAT occurrence indices; that all runs used matching input, code and protocol digests; that there is no MODEL; and that the unchanged first-source/per-unit complete-tree checker covers the entire certified profile list. Never infer full coverage from a subset of successes.

Chunk outputs should be independently audited, with simulated missing chunk, duplicate chunk, wrong manifest, stale inputs, corrupt proof, nonzero checker exit, and interrupted upload negative controls. Schedule cost should influence only *which* leaf is assigned to a part, never mathematical acceptance.

### 5. Optimize I/O only after the proof ledger works

Avoid downloading all producer artifacts independently in 32 jobs: build an immutable manifest with the ordered complete record list, copy to each part, deliver only the assigned lazy payloads, and check record and lazy SHA-256. Keep `record.file` + source label and original per-unit selection semantics stable. This is the last stage because careless input-order or source regrouping breaks certificate coverage.

## Acceptance metrics

1. **Safety**: exact index-once coverage, no MODEL, no missing or corrupted proof accepted, no false `GATE_PASS`, no mixed code/input digests; all negative controls reject.
2. **Performance**: per-phase CPU/wall utilization, time in Cake-lock queue, proof bytes retained vs avoided CaDiCaL time, p95/p99 leaf service time, most-loaded job vs median, total GitHub runner minutes. Measure on isolated or comparably loaded runners.
3. **Reproducibility**: full input/manifest hashes, pinned tool hashes, deterministic plan on identical files, exact producer record line provenance, transparent untrusted-cache handling.
4. **Economics**: only retain a cache object when expected avoided regeneration time exceeds its upload/download/storage and re-verification overhead. No proof artifact is automatically worth preserving.

This document is an engineering proposal. The live 32-part campaign and four remaining formulas are not rerun or modified by the supplied files.
