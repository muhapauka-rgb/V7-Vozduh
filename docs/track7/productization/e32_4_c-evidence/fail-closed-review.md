# E32.4.C Fail-Closed Review

fail_closed_behavior_valid=true

## Reviewed Fail-Closed Requirements

| Requirement | Evidence | Result |
| --- | --- | --- |
| missing lock denies | E32.4.A fail-closed rules and E32.4.B runtime impact. | VALID |
| stale lock denies | E32.4.A stale lock handling and E32.4.B failure modes. | VALID |
| replay race denies | PACKET_REPLAY_RACE returns DENY_REPLAY. | VALID |
| reservation conflict denies | CAPACITY_RESERVATION_CONFLICT denies admission and forward movement. | VALID |
| ownership conflict denies | Unknown owner, mismatched fencing token, or heartbeat loss denies forward movement. | VALID |
| rollback containment exception remains valid | Rollback is allowed only for exact known rollback scope. | VALID |

## Fail-Closed Matrix Verdict

Every defined concurrency failure mode denies forward movement.

Rollback is never allowed for unknown or expanded scope.

Containment may inspect, freeze, cancel, release expired reservations, or perform exact rollback.

Human review is required when owner, scope, audit order, or movement state is unclear.

## Decision

fail_closed_behavior_valid=true
