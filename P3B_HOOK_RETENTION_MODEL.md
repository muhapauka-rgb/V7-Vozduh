# P3.B Hook Retention Model

Project: V7 Vozduh
Block: P3.B Runtime Hook Dry-Run Foundation

## Rule

P3.B follows P2.5 retention architecture and P3.A retention rules. Hooks must not create infinite streams or hook-local queues.

## Retention Approach

| Artifact | Retention model |
| --- | --- |
| Hook observation | Derived view over canonical sources; avoid persistence unless needed. |
| Hook contract | TTL-bound preview/report record if persisted later. |
| Hook decision | Stored only inside contract/report; non-authoritative. |
| Hook verification result | Compact result linked to hook contract and source events. |
| Hook report | Derived/on-demand by default; archive only summary if needed. |
| UI cache | Short-lived rebuildable cache. |

## Required Controls For Later Persistence

- TTL.
- Expiry.
- Maximum cardinality or compaction rule.
- Source refs and hashes.
- Retention class.
- Cleanup path.
- No per-tick append-only hook stream.
- No hook-owned canonical queue.

## Compaction Keys

- `hook_contract_id`
- `candidate_id`
- `execution_contract_id`
- `source_event_id`
- `decision`
- `verification_state`
- `retention_class`

## Retention Verdict

`hook_retention_defined=true`

