# E32.4.B Failure Modes

concurrency_failure_modes_defined=true

## Failure Mode Inventory

| Failure Mode | Detection | Runtime Impact | Operator Action | Fail-Closed Behavior |
| --- | --- | --- | --- | --- |
| USER_LOCK_CONFLICT | Same user locked by another active batch or rollback operation. | Deny forward movement for conflicting batch. | Inspect owner; wait, cancel, or select another user set. | No user movement. Rollback allowed only for known scope. |
| TARGET_LOCK_CONFLICT | Target locked for metadata mutation, maintenance, or another incompatible operation. | Deny target admission or execution. | Inspect target owner and operation purpose. | No target use until conflict clears. |
| CAPACITY_RESERVATION_CONFLICT | Active reservations exceed or would exceed effective_batch_cap. | Deny admission or approval packet generation. | Release expired reservations or reduce batch size. | No overcommit. |
| PACKET_REPLAY_RACE | Packet consumption ledger already contains packet or concurrent packet lock exists. | Deny replay and second execution. | Inspect packet lineage. | DENY_REPLAY; no movement. |
| BATCH_DOUBLE_EXECUTION | Batch state is EXECUTING, OBSERVING, ROLLING_BACK, COMPLETED, or terminal while another executor attempts execution. | Deny second execution. | Inspect batch state and audit lineage. | No duplicate execution. |
| STALE_LOCK | Lock TTL expired, owner heartbeat lost, or fencing token stale. | Deny forward movement. | Run stale-lock recovery review. | Forward denied until safe recovery. |
| STALE_RESERVATION | Reservation expired or evidence hash stale. | Deny forward movement and packet use. | Refresh reservation or regenerate packet. | No capacity claim without fresh evidence. |
| OWNER_HEARTBEAT_LOST | Owner heartbeat missing before operation completion. | Freeze conflicting forward actions. | Verify terminal state or recover owner. | No forward movement until ownership clarified. |
| AUDIT_LOCK_CONFLICT | Audit sequencing unavailable or locked by another writer. | Deny certification and possibly block terminal state finalization. | Inspect audit writer, retry append, or escalate. | No certification without ordered audit. |

## Common Detection Sources

- lock ledger;
- reservation ledger;
- batch status store;
- packet consumption ledger;
- owner heartbeat source;
- audit sequence store;
- execution-time recheck;
- runtime checker output.

## Operator Action Principles

- Prefer wait, cancel, refresh, recertify, or exact rollback.
- Never broaden user scope to resolve concurrency failure.
- Never bypass packet, capacity, policy, or runtime gates.
- Human review is required when ownership, scope, or audit order is unclear.

## Decision

concurrency_failure_modes_defined=true
