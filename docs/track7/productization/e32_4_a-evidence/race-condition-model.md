# E32.4.A Race Condition Model

race_condition_model_defined=true

## Race Inventory

| Race | Detection | Prevention | Fail-Closed Behavior |
| --- | --- | --- | --- |
| USER_DOUBLE_MOVEMENT | Same user appears in two active batches, active packet sets, or concurrent switch intents. | USER_LOCK and candidate set uniqueness check during approval and execution-time recheck. | Deny later forward movement; allow exact rollback for already moved known scope. |
| TARGET_OVERCOMMIT | Sum of active capacity reservations exceeds effective_batch_cap. | Atomic CAPACITY_RESERVATION and target available-capacity calculation. | Deny new batch admission and mark reservation conflict. |
| PACKET_REPLAY_RACE | Packet consumed while another actor attempts replay, refresh, or execute. | PACKET_LOCK and append-only packet consumption ledger. | DENY_REPLAY; no movement. |
| BATCH_DOUBLE_EXECUTION | Batch enters EXECUTING twice from two operators or scheduler jobs. | BATCH_LOCK plus status compare-and-set from APPROVED/SCHEDULED to EXECUTING. | Deny second transition and preserve original lineage. |
| SCHEDULER_OPERATOR_CONFLICT | Operator executes or cancels while scheduler is admitting or executing same batch. | BATCH_LOCK, explicit owner transfer, scheduler_job_id binding. | Pause scheduler admission or deny operator action until owner is clear. |
| CAPACITY_DOUBLE_RESERVATION | Two admission flows reserve the same available capacity. | Atomic reservation ledger write with target capacity invariant. | Deny later reservation and require fresh capacity view. |

## Additional Races

| Race | Required Handling |
| --- | --- |
| ROLLBACK_FORWARD_OVERLAP | Rollback may not overlap forward execution for same user unless containment declares forward failed and rollback scope is exact. |
| AUDIT_ORDER_RACE | Audit backend must provide sequence or AUDIT_LOCK. Missing sequence blocks certification. |
| POLICY_DECISION_STALE_RACE | Policy decision must be revalidated at execution-time if policy version changed. |
| CAPACITY_STALE_RACE | Capacity status must be refreshed at execution-time if reservation or target validation became stale. |

## Prevention Strategy

The prevention strategy combines:

- deterministic lock ordering;
- owner-scoped reservations;
- short packet and reservation TTL;
- execution-time recheck;
- status compare-and-set;
- audit append-only sequencing;
- exact allowed user and target sets.

## Decision

Race prevention is mandatory for production-pool execution. If race state is uncertain, forward movement is denied.
