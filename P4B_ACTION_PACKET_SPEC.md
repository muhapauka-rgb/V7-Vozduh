# P4.B Action Packet Specification

Project: V7 Vozduh
Block: P4.B First Controlled Runtime Action Specification

## Packet Type

`P4B_ZERO_MOVE_GOVERNANCE_ACTION_PACKET`

## Current Compatibility Target

The packet must be compatible with the existing operator execution validator unless a later block explicitly versions a wrapper.

## Exact Schema

```json
{
  "schema_version": "e22.operator-execution-packet.v1",
  "packet_id": "pkt_<hash>",
  "approval_id": "appr_<hash>",
  "action_id": "act_zero_move_governance_<hash>",
  "operation_id": "p4b_zero_move_governance_<timestamp>",
  "action_type": "ZERO_MOVE_GOVERNANCE_STATE_TRANSITION",
  "selected_first_action": "ZERO_MOVEMENT_GENERATION_CLEARANCE_RECHECK",
  "runtime_action": "ZERO_MOVE_GOVERNANCE_STATE_TRANSITION",
  "scope": {
    "kind": "runtime_governance.zero_move_state_transition",
    "user_movement_allowed": false,
    "routing_mutation_allowed": false,
    "autoswitch_apply_allowed": false,
    "rollback_execution_allowed": false,
    "deploy_allowed": false,
    "systemd_change_allowed": false
  },
  "target": {
    "kind": "append_only_runtime_governance_record",
    "store": "operator_runtime_governance_actions",
    "record_type": "zero_move_governance_state_transition"
  },
  "created_at": "<iso8601>",
  "expires_at": "<created_at + 900 seconds>",
  "approval_state": "APPROVED_FOR_RECHECK_ONLY",
  "approval_author": {
    "operator_id": "<operator-a>",
    "role": "approval_author",
    "approved_at": "<iso8601>",
    "approval_text": "I approve P4B zero-move governance action design for final runtime recheck only."
  },
  "approval_reviewer": {
    "operator_id": "<operator-b>",
    "role": "approval_reviewer",
    "approved_at": "<iso8601>",
    "approval_text": "I independently approve P4B zero-move governance action design for final runtime recheck only."
  },
  "approvals": [
    {"operator_id": "<operator-a>", "role": "approval_author", "approved_at": "<iso8601>"},
    {"operator_id": "<operator-b>", "role": "approval_reviewer", "approved_at": "<iso8601>"}
  ],
  "constraints": {
    "selected_move_budget": 0,
    "allowed_users": [],
    "allowed_targets": [],
    "user_movement_allowed": false,
    "routing_mutation_allowed": false
  },
  "runtime_hashes": {
    "users_registry_hash": "<sha256>",
    "egress_registry_hash": "<sha256>",
    "selected_move_hash": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e3570d6d6b1b25c0aefc1b5",
    "selected_move_count": 0,
    "runtime_snapshot_hash": "<sha256>"
  },
  "candidate_hashes": {
    "action_design_hash": "<sha256>",
    "dry_run_summary_id": "<id>",
    "dry_run_verification_id": "<id>"
  },
  "expected": {
    "generation_id": "<stable-generation-id>",
    "users_registry_hash": "<sha256>",
    "egress_registry_hash": "<sha256>",
    "selected_move_hash": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e3570d6d6b1b25c0aefc1b5",
    "runtime_snapshot_hash": "<sha256>"
  },
  "evidence_refs": [],
  "verification_plan": {},
  "rollback_preview": {},
  "rollback_manifest": "COMPENSATING_GOVERNANCE_RECORD_ONLY",
  "observation_window": {},
  "replay_protection": {
    "approval_id_unique": true,
    "packet_id_unique": true,
    "expires_at_required": true,
    "hash_match_required": true
  },
  "authority_state": "NOT_AUTHORIZED_FOR_EXECUTION_IN_P4B"
}
```

## Empty Selected Moves Hash

The selected moves hash must be the existing empty list hash used by `admin_core/operator_execution.py`:

`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e3570d6d6b1b25c0aefc1b5`

## Verdict

`action_packet_spec_complete=true`

