# E27 Audit And Replay Model

## Required Records

For two-user movement, the audit model must record:

- one approval packet with `movement_budget=2`;
- two forward user movement entries or one structured forward batch entry containing both users;
- two rollback entries or one structured rollback batch entry containing both users;
- one replay denial entry if the packet is replayed after use.

## Required Packet Uniqueness

Packet uniqueness must bind:

```text
packet_id
approval_id
operation_id
allowed_users=["10.7.0.11","10.7.0.12"]
allowed_targets=["amneziawg-exec-20260528-10-8-1-14"]
movement_budget=2
users_registry_hash
egress_registry_hash
selected_moves_hash
execution_target_capacity_state
```

## Replay Denial

Replay must deny if any forward record exists for the packet lineage. It must not require both users to have moved before marking the packet consumed, otherwise partial replay could become possible.

## Verdict

`audit_scales_to_two_users=true`

`replay_model_scales_to_two_users=true`

Condition: the two-user packet must treat the forward execution as one atomic governed operation for replay purposes, even if audit details include per-user records.

