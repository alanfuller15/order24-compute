# Independent review: L82_s10a4b18c60_0001 audit

Reviewed 2026-11-21. Issue: https://github.com/alanfuller15/order24-compute/issues/5

**Verdict: UNKNOWN / NOT ACCEPTED as a completed independent audit.** The hosted
runner failed before uploading audit outputs. This is not a proof rejection and
must not be treated as a successful audit. No audit-success note was added to main
or to `ops/recorded.txt`.

## Provenance and independence

Producer evidence: `recake-L82_s10a4b18c60_0001`, artifact 14508417499, from
[producer run 44476347300](https://github.com/alanfuller15/order24-compute/actions/runs/44476347300),
commit `e997a517cb13cc5eeacc0210d5257c79ad71c1b3`, workflow actor `alanfuller15`.
The user attributes this evidence to a separate producer chat; that chat's name is
not recorded in the retrieved artifact metadata. Reviewer: this independent
Codex lane-5 auditor conversation. This conversation did not produce the reviewed
proof or recake record. Earlier unfinished lane searches are not this certificate.
The reviewer-produced extraction below is transport evidence only, not a new proof.

## Audit job and observed failure

Audit: [run 44863702714](https://github.com/alanfuller15/order24-compute/actions/runs/44863702714),
at commit `2fa84dcf86b3bcc55a2e88f07984f0f859938fbb`, job/check run `136722566933`.
The requested inputs were layer 82, producer run 44476347300, artifact
`recake-L82_s10a4b18c60_0001`, heaps `8000,12000`, swap 24 GB. The completed
workflow's individual dispatch values could not be recovered from job logs;
these values identify the user-requested run, not independently verified inputs.

The run began at 03:57:39 UTC and concluded **failure** at 04:50:44 UTC.
The job API reports successful pins/tools, swap, and artifact-download steps;
`Check` began at 04:03:30 UTC and has no completed timestamp in the retained step
record. `Upload` never started. Its artifact list is empty (`total_count=0`).
The job-log endpoint returned `404 BlobNotFound`.

The check-run failure annotation states verbatim:

> The hosted runner lost communication with the server. Anything in your workflow that terminates the runner process, starves it for CPU/Memory, or blocks its network access can cause this error.

That annotation does not establish a specific memory, CPU, or network cause.

| Required acceptance evidence | Observation |
|---|---|
| `main.exit = 3`, selected formula passing | Unavailable |
| `CHECK_RESULTS`: `pass`, `cnf_match`, `proof_match` all true | Unavailable |
| `cake_exit = 0`, exact `cake_lpr = s VERIFIED UNSAT` | Unavailable from independent audit |
| Both negative controls exit 1 | Unavailable |
| Runner input hashes match downloaded producer record | Cannot compare: no `inputs.sha256` artifact |
| Pinned `run_audit.sh` source | Verified at the exact audit commit |
| Heap/swap changes preserve checker and controls | Source reviewed; actual executed diff/output unavailable |

## Producer record independently retrieved

The full producer ZIP exceeds the connector's 512 MiB limit and its storage host
is inaccessible directly from this runtime. A read-only extraction job downloaded
the original ZIP on a GitHub runner, checked its complete digest against GitHub's
artifact metadata, and copied the root `results.jsonl` without modification.
It did not run a SAT solver, rewrite a record, or generate/check a proof.

Extraction: [run 44867969701](https://github.com/alanfuller15/order24-compute/actions/runs/44867969701),
script commit `a447acce6a09137a63c49aa152455ecc51628f94`,
`exp/audit_extract_record.py`. Artifact `independent-l82-0001-record-extraction-v2`
(ID 14691779507) was downloaded locally and its ZIP digest checked:
`a1258edfb792ebd85c91795f09b1612725e131e79718c62f6de7d32ac24751a0`.
A previous extraction attempt (44867872465) failed on cross-host authentication
and supplied no producer record; it is not used as evidence.

- Original producer ZIP SHA-256: `2df991281337fe8662460ae53b760c497b84b5b956cd87a9c147662faeba0a6e`.
- Original `results.jsonl`: 167162 bytes; SHA-256 `db050c40edb553d992458b426f7060a98b68c6c83adcfba8f95c12c0ffdebca8`.
- Exactly one record, tag `L82_s10a4b18c60_0001`, encoder `v7`, status `UNSAT`.
- Record CNF SHA-256: `cfa61509c693ba3cc3f186cfeb48182e683b3b07fd608f6ba722ccaa02b06ad6`.
- Record compressed proof SHA-256: `9d1e20d9255da6d1a686d93cfb38d20f4a2ca4140282fd3ca968b5ee9f577faa`.
- The producer record reports `cake_exit=0`, heap 12000 MB, and `s VERIFIED UNSAT`.
  These remain **producer's summary**, not the missing independent audit verdict.

## Source review at the audit commit

`audit_kit/run_audit.sh` SHA-256:
`69e79abe66e68205153f78b97e132d13d7bf31515b9f7b365c12be16760868f5`.

`audit_kit/with_heaps.sh` SHA-256:
`9b261298765eee0f8a2be9ac88f9ed6fc5c4512fff2dde7b35283d81e77b146e`.

The wrapper verifies the unmodified harness pin, validates the heap list, writes
a temporary harness copy, and checks that its diff changes exactly one line:
adding `CAKE_HEAPS=8000,12000` to the isolated checker's environment. It logs the
diff and both script hashes. Swap is created separately by `audit.yml`; it is not
added by `with_heaps.sh`. Neither mechanism changes the pinned checker, formulas,
proof, or negative-control definitions. The checker retries a larger heap only
when no `s ` verdict line was printed; acceptance requires stdout to split into
exactly `['s VERIFIED UNSAT']` and exit 0.

This source review and the producer hashes do not substitute for the unavailable
proof-check and negative-control results. The gate for a main audit-success
commit is not met. A completed independent rerun with output artifacts is needed.
No claim about the order-24 theorem is made.
