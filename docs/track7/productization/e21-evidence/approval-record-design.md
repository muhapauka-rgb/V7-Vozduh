# E21 Approval Record And Audit Design

## First Real Approval Packet Schema

```json
{
  "schema_version": "e21.first-real-approval-packet.v1",
  "approval_id": "appr_<hash>",
  "operation_id": "E21_FIRST_REAL_OPERATOR_DRIVEN_BOUNDED_EXECUTION",
  "selected_first_action": "F_READONLY_TO_EXECUTION_TRANSITION_PACKET_WITH_ZERO_MOVE_GENERATION_CLEARANCE_AS_NEXT_BOUNDARY",
  "actor": {
    "operator_id": "required",
    "role": "approval_author",
    "session_id": "required",
    "signed_at": "required"
  },
  "second_confirmer": {
    "operator_id": "required",
    "role": "approval_reviewer",
    "session_id": "required",
    "signed_at": "required",
    "same_actor_allowed": false
  },
  "created_at": "required",
  "expires_at": "required",
  "runtime_snapshot_hash": "required",
  "selected_move_hash": "required",
  "generation_id": "required",
  "blast_radius": {
    "max_users": 0,
    "allowed_users": [],
    "allowed_targets": [],
    "runtime_mutation": "approval_record_only"
  },
  "rollback_manifest": {
    "rollback_type": "approval_revocation",
    "user_rollback_required": false,
    "routing_rollback_required": false,
    "revoke_to_state": "NOT_APPROVED_FAIL_CLOSED"
  },
  "stale_invalidation": [
    "runtime_snapshot_hash_changed",
    "selected_move_hash_changed",
    "generation_id_changed",
    "target_readiness_changed",
    "restore_settle_changed",
    "approval_expired",
    "operator_identity_changed"
  ],
  "replay_prevention": {
    "single_use": true,
    "append_only_audit_required": true,
    "used_at": null,
    "replay_denial_id": "required_on_replay"
  },
  "emergency_containment": {
    "user_movement_allowed": false,
    "routing_mutation_allowed": false,
    "safe_state": "APPROVAL_REVOKED_NO_RUNTIME_ACTION"
  },
  "evidence_refs": [
    "execution-governance-preview",
    "execution-rehearsal-preview",
    "runtime-recheck-gates",
    "denial-replay-matrix"
  ]
}
```

## Immutable Audit Record Shape

```json
{
  "audit_record_id": "audit_<hash>",
  "record_type": "approval_created|approval_confirmed|recheck_passed|denial|revoked",
  "approval_id": "appr_<hash>",
  "previous_record_hash": "hash",
  "record_hash": "hash",
  "created_at": "required",
  "actor": "required",
  "payload_hash": "required",
  "runtime_mutation": false
}
```

## Design Verdict

approval_record_design_complete=true
immutable_audit_shape_complete=true
production_approval_persistence_required=true
dual_operator_auth_required=true
execution_allowed_now=false
