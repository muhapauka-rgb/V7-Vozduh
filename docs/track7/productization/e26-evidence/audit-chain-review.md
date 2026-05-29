# E26 Audit Chain Review

`audit_chain_valid=true`

## Source

Raw audit evidence was collected from:

- `/opt/v7/audit/operator-execution-audit.jsonl`
- local copy: `docs/track7/productization/e26-evidence/audit-chain-review-raw.md`

## E25.15 Records

| Order | Event | Timestamp UTC | Record Hash | Verdict |
|---:|---|---|---|---|
| 1 | `forward_movement` | `2026-05-28T20:54:13Z` | `f4fd62bec6fff288d951876f6dfd62be3ff19a209e486998c0df022900bc4537` | OK |
| 2 | `rollback_movement` | `2026-05-28T20:57:19Z` | `792c6d82b6d8ced4b96b68b1562fd2bde601cb0e6af91c37a07f54295e9865c1` | OK |
| 3 | `replay_validation` | `2026-05-28T21:02:19Z` | `c105e00b2eed112271f87b337b5375185672a53fd3687dc351eb687e70b20e55` | DENY_REPLAY |

## Packet Lineage

```text
packet_id=packet-0671c44ea5024978724e11e9
approval_id=approval-4bbbbf5f5d145367d490d523
operation_id=e25-15-first-movement-retry-20260528T205228Z
candidate_user=10.7.0.11
target=amneziawg-exec-20260528-10-8-1-14
```

## Review

The event order is correct: forward movement, rollback movement, then replay denial. The replay denial refers to the same packet lineage and was recorded after successful rollback. No audit evidence indicates a second forward movement for the replay.

The audit chain is valid for E25.15 certification.

