# P6.A Movement Packet Design

Project: V7 Vozduh

Block: P6.A

## Packet Strategy

Reuse existing packet concepts from:

- `admin_core/operator_execution.py`
- `docs/track7/productization/e24-evidence/first-bounded-user-movement-approval-packet.json`
- `docs/track7/productization/e27_2-evidence/fresh-approval-packet.json`
- `docs/track7/productization/e28_2-evidence/fresh-approval-packet.json`

Do not create a parallel packet system.

## Proposed Packet Fields

Required fields for future P6.B certification:

- schema_version
- packet_id
- approval_id
- operation_id
- created_at
- expires_at
- runtime_action: `BOUNDED_SINGLE_USER_MOVEMENT`
- movement_budget: `1`
- blast_radius: `1`
- allowed_users: `["10.7.0.11"]`
- allowed_targets: `["amneziawg-exec-20260528-10-8-1-14"]`
- from_egress: `1`
- to_egress: `amneziawg-exec-20260528-10-8-1-14`
- rollback_target: `1`
- route_table: `1009`
- target_interface: `v7execwg0`
- users_registry_hash
- egress_registry_hash
- selected_moves_hash
- selected_moves_count
- runtime_snapshot_hash
- route_table_hash_before
- approval fields
- rollback_manifest
- observation_plan
- forbidden actions

## Movement Evidence

Packet must embed or reference:

- route movement preview result
- target readiness result
- checker baseline
- capacity/trust baseline
- selected moves proof

## Forbidden In Packet

Packet must explicitly forbid:

- users beyond `10.7.0.11`
- targets beyond `amneziawg-exec-20260528-10-8-1-14`
- autoswitch apply
- policy apply
- broad routing sync
- systemd changes
- deploy
- rollback unless separately triggered and verified

## Verdict

- movement_packet_defined=true
- parallel_packet_system_created=false
