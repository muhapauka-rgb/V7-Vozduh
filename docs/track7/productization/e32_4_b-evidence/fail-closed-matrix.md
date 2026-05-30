# E32.4.B Fail-Closed Matrix

concurrency_fail_closed_matrix_defined=true

| Failure Mode | Forward Allowed | Rollback Allowed | Containment Allowed | Human Review Required |
| --- | --- | --- | --- | --- |
| USER_LOCK_CONFLICT | NO | YES, exact known scope only | YES | YES if owner unclear |
| TARGET_LOCK_CONFLICT | NO | YES, exact known scope only | YES | YES if target state unclear |
| CAPACITY_RESERVATION_CONFLICT | NO | YES, exact known scope only | YES | YES if overcommit cannot be attributed |
| PACKET_REPLAY_RACE | NO | NO unless prior forward movement is proven | YES | YES |
| BATCH_DOUBLE_EXECUTION | NO | YES, exact known scope only | YES | YES |
| STALE_LOCK | NO | YES, exact known scope only | YES | YES |
| STALE_RESERVATION | NO | YES, exact known scope only | YES | NO if refresh is clean, YES if conflict exists |
| OWNER_HEARTBEAT_LOST | NO | YES, exact known scope only | YES | YES |
| AUDIT_LOCK_CONFLICT | NO for certification; execution depends on prior phase | YES, exact known scope only | YES | YES |

## Matrix Rules

- Forward movement is denied for every concurrency failure mode.
- Rollback is allowed only for exact known scope and never for unknown or expanded scope.
- Containment may inspect, freeze, cancel, release expired reservations, or perform exact rollback.
- Human review is mandatory whenever owner, scope, audit order, or movement state is unclear.

## Decision

concurrency_fail_closed_matrix_defined=true
