# P4.A Action Packet Design

Project: V7 Vozduh
Block: P4.A First Controlled Runtime Action Design

## Packet Name

`P4A_ZERO_MOVE_GOVERNANCE_ACTION_PACKET`

## Existing Concepts Reused

- `approval_id`
- `packet_id`
- `operation_id`
- `selected_first_action`
- `runtime_action`
- `approvals`
- `expires_at`
- `expected`
- `rollback_manifest`
- runtime recheck
- replay denial
- audit append record

## Required Packet Fields

| Field | Required value or rule |
| --- | --- |
| `schema_version` | Future P4.B schema mapped to existing operator execution model. |
| `selected_first_action` | Zero-movement governance clearance action. |
| `runtime_action` | `ZERO_MOVE_GOVERNANCE_STATE_TRANSITION`. |
| `constraints.selected_move_budget` | `0`. |
| `constraints.allowed_users` | `[]`. |
| `constraints.allowed_targets` | `[]`. |
| `constraints.user_movement_allowed` | `false`. |
| `constraints.routing_mutation_allowed` | `false`. |
| `approvals` | author and reviewer, different operators. |
| `expires_at` | short TTL, recommended 900 seconds. |
| `expected.users_registry_hash` | must match final recheck. |
| `expected.egress_registry_hash` | must match final recheck. |
| `expected.selected_move_hash` | empty selected-moves hash. |
| `expected.runtime_snapshot_hash` | must match final recheck. |
| `rollback_manifest` | compensating record plan. |
| `observation_window` | before/immediate/after/delayed checkpoints. |

## Non-Duplication Rule

This packet design must later map into the existing operator execution packet path. It must not introduce a second executor.

## Verdict

`action_packet_defined=true`

