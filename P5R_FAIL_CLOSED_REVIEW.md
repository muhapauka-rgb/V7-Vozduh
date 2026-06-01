# P5R Fail-Closed Review

Project: V7 Vozduh

Block: P5 RETRY

## Denial Matrix

| Case | Verdict | Error class | Governance appended |
| --- | --- | --- | --- |
| duplicate/replay packet | `DENY_REPLAY` | `approval_id_already_recorded` | false |
| expired packet | `DENY_PACKET_INVALID` | `approval_expired` | false |
| stale/mismatched registry hash | `DENY_HASH_MISMATCH` | `users_registry_hash` | false |
| invalid movement scope | `DENY_PACKET_INVALID` | `selected_move_budget_not_zero`, `allowed_users_not_empty`, `user_movement_not_forbidden` | false |
| unknown runtime action | `DENY_RUNTIME_ACTION_UNSUPPORTED` | `runtime_action_not_zero_move_governance_transition` | false |
| missing approval | `DENY_PACKET_INVALID` | `dual_confirmation_missing` | false |
| blocked record-only runtime action request | `DENY_RUNTIME_ACTION_UNSUPPORTED` | `runtime_action_not_zero_move_governance_transition` | false |

## Store Impact

Denied cases appended audit denial records only.

- governance records before denial tests: `1`
- governance records after denial tests: `1`
- audit records after all tests: `8`

## Verdict

- fail_closed_review_complete=true
- unknown_denied=true
- missing_denied=true
- stale_denied=true
- expired_denied=true
- invalid_denied=true
- mismatched_denied=true
- replayed_denied=true
- blocked_denied=true
