# P5R Packet

Project: V7 Vozduh

Block: P5 RETRY

## Packet Identity

- packet_id: `pkt_p5r_zero_move_governance_state_20260601T095456Z_primary`
- approval_id: `appr_p5r_zero_move_governance_state_20260601T095456Z_primary`
- operation_id: `P5R_FIRST_RUNTIME_ACTION_RETRY`
- schema_version: `e22.operator-execution-packet.v1`

## Action

- selected_first_action: `ZERO_MOVEMENT_GENERATION_CLEARANCE_RECHECK`
- runtime_action: `ZERO_MOVE_GOVERNANCE_STATE_TRANSITION`

The prompt-selected action maps to the existing runtime action field.

## Approval

- approval author: `prompt-authorized-operator`
- approval reviewer: `codex-runtime-reviewer`
- created_at: `2026-06-01T09:54:56.461679+00:00`
- expires_at: `2026-06-01T10:24:56.461679+00:00`

## Constraints

- selected_move_budget: `0`
- allowed_users: `[]`
- allowed_targets: `[]`
- user_movement_allowed: false
- routing_mutation_allowed: false

## Expected Runtime Hashes

- users registry hash: `07362c9aa6f959be2ab06f26928692c6844f37a3bd266be8de4e56193f6d9a9f`
- egress registry hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- selected move hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- runtime snapshot hash: `ec11fffc70bf63d04dd76b723e415692b4be371ec007ec0df638fc5ecb216c84`
- generation_id: `p5r-live-runtime-20260601T095456Z`

## Rollback Preview

- rollback_manifest: `NONE_NOT_REQUIRED_APPEND_ONLY_GOVERNANCE_AUDIT`

Rollback is preview-only. No rollback execution is allowed or needed for append-only governance/audit records.

## Observation Plan

- before sample
- after action sample
- after denial tests sample

Each sample verifies users registry hash, egress registry hash, selected moves, routing hash, and autoswitch timer state.

## Replay Protection

- approval_id_unique=true
- packet_id_unique=true
- duplicate_packet_must_deny=true

## Verdict

- packet_created=true
- packet_scope_zero_move=true
- packet_runtime_action=ZERO_MOVE_GOVERNANCE_STATE_TRANSITION
