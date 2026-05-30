# E32.5.B Failure Modes

scheduler_failure_modes_defined=true

## Failure Mode Matrix

| Failure Mode | Detection | Impact | Fail-Closed Behavior | Operator Action |
| --- | --- | --- | --- | --- |
| SCHEDULE_EXPIRED | now > not_after, packet expired, or execution window closed. | Schedule cannot dispatch. | Mark EXPIRED; no runtime mutation. | Regenerate schedule or packet if still desired. |
| QUEUE_CONFLICT | Two schedules claim incompatible queue position, owner, or dispatch slot. | Dispatch blocked. | Hold or FAILED_CLOSED if ambiguous. | Inspect queue owner and reorder safely. |
| DEPENDENCY_FAILED | Parent batch failed, cancelled, expired, or unknown. | Child cannot dispatch. | FAILED_CLOSED or CANCELLED according to operator intent. | Regenerate child with fresh dependency model. |
| WINDOW_CLOSED | execution_window is AFTER_WINDOW. | Dispatch blocked. | EXPIRED; no runtime mutation. | Create new windowed schedule if valid. |
| LOCK_UNAVAILABLE | Required lock is held, stale, or conflicted. | Dispatch blocked. | WAITING_LOCKS or FAILED_CLOSED if unsafe. | Inspect lock owner; run stale recovery if needed. |
| RESERVATION_UNAVAILABLE | Capacity/target/batch reservation missing, stale, expired, or conflicted. | Dispatch blocked. | WAITING_LOCKS, EXPIRED, or FAILED_CLOSED. | Refresh or regenerate reservation. |
| SCHEDULER_DRIFT | Schedule metadata, queue view, or derived state differs from authoritative batch/runtime truth. | Dispatch blocked. | FAILED_CLOSED until rebuilt from authoritative sources. | Recompute schedule and audit drift. |
| DOUBLE_DISPATCH_ATTEMPT | Schedule already DISPATCHED or terminal while another actor dispatches. | Second dispatch denied. | Deny duplicate dispatch; no runtime mutation. | Inspect audit lineage and active owner. |

## Common Detection Sources

- schedule metadata store;
- batch ledger;
- policy decision record;
- capacity state;
- lock/reservation ledger;
- packet state;
- audit lineage;
- current time and window source.

## Decision

scheduler_failure_modes_defined=true
