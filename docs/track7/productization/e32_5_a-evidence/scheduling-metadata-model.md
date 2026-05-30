# E32.5.A Scheduling Metadata Model

scheduling_metadata_model_defined=true

## Authoritative Fields

| Field | Meaning | Authority |
| --- | --- | --- |
| schedule_id | Unique schedule object id. | Scheduler metadata store. |
| batch_id | Batch being scheduled. | Batch ledger. |
| schedule_type | IMMEDIATE, DEFERRED, WINDOWED, DEPENDENT, MAINTENANCE, or EMERGENCY. | Scheduler metadata. |
| schedule_status | Lifecycle state of schedule. | Scheduler metadata. |
| priority | Queue ordering weight. | Scheduler policy/config, not Routing Intelligence. |
| requested_start | Requested dispatch time. | Operator or scheduler request. |
| not_before | Earliest dispatch time. | Schedule metadata. |
| not_after | Latest dispatch time. | Schedule metadata. |
| execution_window | Valid dispatch window. | Schedule metadata or maintenance calendar. |
| dependency_batch_ids | Parent batch dependencies. | Schedule metadata. |
| maintenance_window_id | Maintenance window binding. | Maintenance calendar. |
| emergency_flag | Emergency schedule indicator. | Explicit operator/emergency approval. |
| scheduler_owner | Current scheduler owner. | Scheduler/owner transfer ledger. |
| created_at | Creation timestamp. | Scheduler metadata store. |
| updated_at | Last update timestamp. | Scheduler metadata store. |
| expires_at | Schedule expiration timestamp. | Derived at creation, authoritative after persisted. |
| audit_lineage_id | Audit lineage for schedule events. | Audit store. |

## Derived Fields

| Field | Meaning |
| --- | --- |
| schedule_effective_status | Effective state after window, dependency, expiration, and lock checks. |
| queue_position | Relative order among dispatchable or waiting schedules. |
| ready_to_dispatch | True only when schedule, batch, policy, capacity, concurrency, packet, and runtime preconditions are satisfied. |
| blocked_reason | Current reason preventing dispatch. |
| dependency_status | Summary of parent batch states. |
| window_status | BEFORE_WINDOW, IN_WINDOW, AFTER_WINDOW, or NONE. |
| expiration_status | ACTIVE, EXPIRING_SOON, EXPIRED. |
| admission_status | Current policy/capacity/batch admission summary. |
| lock_reservation_status | Current concurrency and reservation status. |

## Field Rules

- Authoritative fields must be persisted and auditable.
- Derived fields must be recomputed at dispatch-time.
- Stale derived fields cannot authorize execution.
- Missing authoritative metadata fails closed.

## Decision

scheduling_metadata_model_defined=true
