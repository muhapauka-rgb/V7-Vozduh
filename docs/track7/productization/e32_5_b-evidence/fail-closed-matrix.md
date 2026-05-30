# E32.5.B Fail-Closed Matrix

scheduler_fail_closed_matrix_defined=true

| Failure Mode | Dispatch Allowed | Rollback Allowed | Containment Allowed | Human Review Required |
| --- | --- | --- | --- | --- |
| SCHEDULE_EXPIRED | NO | YES, exact known moved scope only | YES | NO unless state conflicts |
| QUEUE_CONFLICT | NO | YES, exact known moved scope only | YES | YES |
| DEPENDENCY_FAILED | NO | YES, exact known moved scope only | YES | YES if dependency state unclear |
| WINDOW_CLOSED | NO | YES, exact known moved scope only | YES | NO unless emergency override requested |
| LOCK_UNAVAILABLE | NO | YES, exact known moved scope only | YES | YES if owner/stale state unclear |
| RESERVATION_UNAVAILABLE | NO | YES, exact known moved scope only | YES | YES if conflict exists |
| SCHEDULER_DRIFT | NO | YES, exact known moved scope only | YES | YES |
| DOUBLE_DISPATCH_ATTEMPT | NO for second dispatch | YES, exact known moved scope only | YES | YES |

## Matrix Rules

- Dispatch is denied for every scheduler failure mode.
- Rollback remains allowed only for exact known moved scope.
- Containment may inspect, cancel, expire, recompute, or exact-rollback.
- Human review is required when owner, dependency, queue, audit, or movement state is unclear.

## Decision

scheduler_fail_closed_matrix_defined=true
