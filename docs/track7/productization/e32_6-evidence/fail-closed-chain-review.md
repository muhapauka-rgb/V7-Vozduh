# E32.6 Fail-Closed Chain Review

fail_closed_chain_valid=true

## End-to-End Fail-Closed Chain

| Layer | Failure Behavior | Result |
| --- | --- | --- |
| Capacity | stale, degraded, expired, revoked, insufficient, or impossible capacity denies forward movement. | VALID |
| Batch | invalid metadata, scope mismatch, rollback gap, stale packet, replay, or audit inconsistency denies execution. | VALID |
| Policy | DENY blocks; REVIEW_REQUIRED blocks; ADDITIONAL_GATES_REQUIRED blocks until satisfied. | VALID |
| Concurrency | lock conflict, reservation conflict, stale lock, replay race, owner heartbeat loss, or double execution denies forward movement. | VALID |
| Scheduling | queue conflict, dependency failure, closed window, unavailable locks/reservations, drift, or double dispatch denies dispatch. | VALID |
| Execution-Time Recheck | stale runtime truth, packet mismatch, target not GO, hidden movers, selected moves, or checker failure denies execution. | VALID |

## Rollback Exception

Rollback remains allowed only for exact known moved scope.

No layer may broaden rollback scope to resolve failure.

## Decision

fail_closed_chain_valid=true
