# E22.1 Replay / Denial Matrix

All denial cases wrote append-only denial records and performed no runtime action.

| Case | Verdict | Record Written | Expected Evidence |
|---|---:|---:|---|
| Replay same packet | `DENY_REPLAY` | true | `approval_id_already_recorded` |
| Expired packet | `DENY_PACKET_INVALID` | true | `approval_expired` |
| Modified registry hash | `DENY_HASH_MISMATCH` | true | `users_registry_hash` mismatch |
| Modified selected-move hash | `DENY_PACKET_INVALID` | true | `selected_move_hash_invalid_for_zero_budget` |
| Missing second confirmation | `DENY_PACKET_INVALID` | true | `dual_confirmation_missing` |
| Nonzero movement budget | `DENY_PACKET_INVALID` | true | `selected_move_budget_not_zero` |
| Runtime action attempt | `DENY_PACKET_INVALID` | true | `runtime_action_not_allowed` |
| Allowed users not empty | `DENY_PACKET_INVALID` | true | `allowed_users_not_empty` |

Audit chain after matrix:

```text
pre_audit_record_count=0
post_audit_record_count=9
approval_record_persisted=1
denial_record=8
```

All records reported:

```text
runtime_mutation=false
user_movement=false
routing_mutation=false
runtime_action_performed=false
```
