# E23 Replay / Denial Verification

Replay and invalid packet cases were executed after the successful runtime action.

## Counts

```text
pre_audit_count=10
post_audit_count=19
pre_governance_count=1
post_governance_count=1
```

Only denial audit records were appended during denial verification. No additional runtime governance action record was written.

## Matrix

| Case | Verdict | Evidence |
|---|---|---|
| replay same packet | `DENY_REPLAY` | `approval_id_already_recorded` |
| expired packet | `DENY_PACKET_INVALID` | `approval_expired` |
| stale generation | `DENY_PACKET_INVALID` | `generation_id_missing` |
| stale selected_move_hash | `DENY_PACKET_INVALID` | `selected_move_hash_invalid_for_zero_budget` |
| modified runtime action | `DENY_PACKET_INVALID` | `runtime_action_not_allowed` |
| modified blast radius | `DENY_PACKET_INVALID` | `allowed_targets_not_empty` |
| unauthorized movement budget | `DENY_PACKET_INVALID` | `selected_move_budget_not_zero` |
| packet attempting user movement | `DENY_PACKET_INVALID` | `allowed_users_not_empty`, `user_movement_not_forbidden` |
| packet attempting routing mutation | `DENY_PACKET_INVALID` | `routing_mutation_not_forbidden` |

## Post-Denial Runtime State

```text
users_registry_hash=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c
egress_registry_hash=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8
restore_barrier_hash=f5f37e9595f87233939ed067ef25e58c500adae687de4090a8c1832140571079
selected_move_count=0
hidden_movers=absent
runtime_checkers=OK
```

replay_rejection_verified=true
immutable_audit_chain_verified=true
