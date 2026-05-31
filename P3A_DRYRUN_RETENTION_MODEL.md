# P3.A Dry-Run Retention Model

Project: V7 Vozduh
Block: P3.A Runtime Dry-Run Foundation

## Rule

P3.A must follow the existing P2.5 retention architecture. It must not introduce infinite growth, unbounded per-tick streams or duplicate long-lived logs.

## Retention Strategy

| Data type | Retention approach |
| --- | --- |
| Dry-run reports | Prefer on-demand derived reports. Persist only if later blocks require auditability. |
| Dry-run contracts | TTL-bound preview records with source hashes and expiry. |
| Normalized events | Derived from canonical logs; avoid separate permanent copy. |
| Verification results | Keep compact result records linked to source contract ids. |
| Simulation details | Store summaries and source refs; avoid large duplicated payloads. |
| UI caches | Short-lived and rebuildable. |

## Required Controls For Any Later Persistent Store

- TTL or archive date.
- Maximum record count or compaction rule.
- Source refs instead of copied source payloads.
- Hashes for reproducibility.
- Cleanup path.
- Explicit retention class.
- No per-request unbounded append.
- No hook-local queue.

## Archive And Compaction

Dry-run records should compact by:

- Contract id.
- Candidate id.
- Source event id.
- Verification state.
- Retention class.

Expired records may be archived as summaries. Full source evidence remains in canonical stores governed by their own retention.

## Cleanup Responsibility

Cleanup should remain under the existing retention/closure architecture. P3.A should not introduce an independent cleanup daemon.

## Retention Verdict

`dryrun_retention_defined=true`

