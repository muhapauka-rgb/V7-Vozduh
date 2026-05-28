# E14 Approval Contract Schemas

## Purpose

Approval contracts formalize what a human approves. They must be replay
resistant, generation-bound, rollback-aware, evidence-linked, and stale-safe.
These schemas are design contracts, not runtime implementation.

## Common Contract Envelope

All approval contracts include this envelope:

```json
{
  "type": "object",
  "required": [
    "schema_version",
    "contract_type",
    "contract_id",
    "operation_id",
    "created_at",
    "expires_at",
    "state_source",
    "status",
    "actor",
    "evidence_refs",
    "freshness"
  ],
  "properties": {
    "schema_version": { "type": "string" },
    "contract_type": { "type": "string" },
    "contract_id": { "type": "string" },
    "operation_id": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" },
    "expires_at": { "type": "string", "format": "date-time" },
    "state_source": { "enum": ["live", "copied_state", "simulation", "historical"] },
    "status": { "enum": ["draft", "approvable", "approved", "consumed", "expired", "revoked", "blocked", "stale"] },
    "actor": { "type": "object" },
    "evidence_refs": { "type": "array", "items": { "type": "string" } },
    "freshness": { "$ref": "#/$defs/Freshness" }
  }
}
```

## Shared Definitions

```json
{
  "$defs": {
    "StateHashes": {
      "type": "object",
      "required": ["users_registry_hash", "egress_registry_hash"],
      "properties": {
        "users_registry_hash": { "type": "string" },
        "egress_registry_hash": { "type": "string" },
        "switch_history_count": { "type": "integer" }
      }
    },
    "GenerationBinding": {
      "type": "object",
      "required": ["planner_generation_id", "selected_moves_fingerprint"],
      "properties": {
        "planner_generation_id": { "type": "string" },
        "apply_generation_id_expected": { "type": "string" },
        "restore_generation_id": { "type": "string" },
        "selected_moves_fingerprint": { "type": "string" },
        "replay_nonce": { "type": "string" }
      }
    },
    "Freshness": {
      "type": "object",
      "required": ["collected_at", "valid_until", "stale"],
      "properties": {
        "collected_at": { "type": "string", "format": "date-time" },
        "valid_until": { "type": "string", "format": "date-time" },
        "stale": { "type": "boolean" },
        "stale_reasons": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```

## 1. MovementApproval

```json
{
  "contract_type": "movement_approval",
  "required": [
    "approved_users",
    "from_targets",
    "to_targets",
    "state_hashes",
    "generation_binding",
    "selected_moves_count",
    "max_selected_moves",
    "blast_radius_contract_id",
    "rollback_manifest_id",
    "required_gates"
  ],
  "properties": {
    "approved_users": { "type": "array", "items": { "type": "string" } },
    "from_targets": { "type": "array", "items": { "type": "string" } },
    "to_targets": { "type": "array", "items": { "type": "string" } },
    "state_hashes": { "$ref": "#/$defs/StateHashes" },
    "generation_binding": { "$ref": "#/$defs/GenerationBinding" },
    "selected_moves_count": { "type": "integer" },
    "max_selected_moves": { "type": "integer" },
    "route_delta_summary": { "type": "array" },
    "target_capacity_delta": { "type": "array" },
    "blast_radius_contract_id": { "type": "string" },
    "rollback_manifest_id": { "type": "string" },
    "required_gates": { "type": "array", "items": { "type": "string" } }
  }
}
```

Validation:

- selected move count must be less than or equal to max selected moves;
- selected-move fingerprint must match the current SelectedMoveSet;
- rollback manifest must be valid before approval;
- approval expires on registry hash or generation drift.

## 2. RollbackApproval

```json
{
  "contract_type": "rollback_approval",
  "required": [
    "rollback_manifest_id",
    "source_operation_id",
    "users",
    "rollback_target_per_user",
    "expected_routes",
    "verification_checks",
    "partial_failure_policy"
  ],
  "properties": {
    "rollback_manifest_id": { "type": "string" },
    "source_operation_id": { "type": "string" },
    "users": { "type": "array", "items": { "type": "string" } },
    "rollback_target_per_user": { "type": "object" },
    "expected_routes": { "type": "array" },
    "verification_checks": { "type": "array", "items": { "type": "string" } },
    "partial_failure_policy": { "enum": ["stop_and_contain", "continue_only_approved", "manual_review_required"] }
  }
}
```

## 3. RestoreApproval

```json
{
  "contract_type": "restore_approval",
  "required": [
    "restore_id",
    "restore_phase",
    "restore_settle_state_id",
    "restore_barrier_id",
    "generation_binding",
    "delayed_monitoring_contract_id",
    "timer_action"
  ],
  "properties": {
    "restore_id": { "type": "string" },
    "restore_phase": { "enum": ["planner_restore", "apply_restore", "delayed_monitoring_closeout"] },
    "restore_settle_state_id": { "type": "string" },
    "restore_barrier_id": { "type": "string" },
    "generation_binding": { "$ref": "#/$defs/GenerationBinding" },
    "delayed_monitoring_contract_id": { "type": "string" },
    "timer_action": { "enum": ["none", "restore_apply_timer", "hold_apply_timer", "restore_planner_timer"] }
  }
}
```

## 4. GenerationClearance

```json
{
  "contract_type": "generation_clearance",
  "required": [
    "barrier_id",
    "cleared",
    "allow_post_ttl_apply",
    "generation_clearance",
    "generation_binding",
    "clearance_max_selected_moves",
    "allowed_users",
    "allowed_targets"
  ],
  "properties": {
    "barrier_id": { "type": "string" },
    "cleared": { "type": "boolean" },
    "allow_post_ttl_apply": { "type": "boolean" },
    "generation_clearance": { "type": "boolean" },
    "generation_binding": { "$ref": "#/$defs/GenerationBinding" },
    "clearance_max_selected_moves": { "type": "integer" },
    "allowed_users": { "type": "array", "items": { "type": "string" } },
    "allowed_targets": { "type": "array", "items": { "type": "string" } },
    "consumption_policy": { "enum": ["consume_once", "fail_closed_on_mismatch"] }
  }
}
```

## 5. CohortApproval

```json
{
  "contract_type": "cohort_approval",
  "required": [
    "cohort_id",
    "approved_users",
    "selected_target",
    "rollback_targets",
    "max_cohort_size",
    "target_hard_limit",
    "movement_approval_id",
    "delayed_monitoring_contract_id"
  ],
  "properties": {
    "cohort_id": { "type": "string" },
    "approved_users": { "type": "array", "items": { "type": "string" } },
    "selected_target": { "type": "string" },
    "rollback_targets": { "type": "object" },
    "max_cohort_size": { "type": "integer" },
    "target_hard_limit": { "type": "integer" },
    "movement_approval_id": { "type": "string" },
    "delayed_monitoring_contract_id": { "type": "string" }
  }
}
```

## 6. EmergencyContainment

```json
{
  "contract_type": "emergency_containment",
  "required": [
    "containment_reason",
    "trigger_event_id",
    "allowed_actions",
    "forbidden_actions",
    "evidence_required",
    "post_containment_review_required"
  ],
  "properties": {
    "containment_reason": { "type": "string" },
    "trigger_event_id": { "type": "string" },
    "allowed_actions": { "type": "array", "items": { "type": "string" } },
    "forbidden_actions": { "type": "array", "items": { "type": "string" } },
    "evidence_required": { "type": "array", "items": { "type": "string" } },
    "post_containment_review_required": { "type": "boolean" }
  }
}
```

## 7. ReplayProtection

```json
{
  "contract_type": "replay_protection",
  "required": [
    "generation_binding",
    "state_hashes",
    "token_status",
    "consumed_at",
    "replay_rejection_reasons"
  ],
  "properties": {
    "generation_binding": { "$ref": "#/$defs/GenerationBinding" },
    "state_hashes": { "$ref": "#/$defs/StateHashes" },
    "token_status": { "enum": ["active", "consumed", "expired", "revoked", "mismatch"] },
    "consumed_at": { "type": ["string", "null"], "format": "date-time" },
    "replay_rejection_reasons": { "type": "array", "items": { "type": "string" } }
  }
}
```

## 8. BlastRadiusContract

```json
{
  "contract_type": "blast_radius_contract",
  "required": [
    "affected_users",
    "max_users_moved",
    "targets_touched",
    "reserved_targets_touched",
    "route_classes_touched",
    "rollback_scope",
    "out_of_scope"
  ],
  "properties": {
    "affected_users": { "type": "array", "items": { "type": "string" } },
    "max_users_moved": { "type": "integer" },
    "targets_touched": { "type": "array", "items": { "type": "string" } },
    "reserved_targets_touched": { "type": "array", "items": { "type": "string" } },
    "route_classes_touched": { "type": "array", "items": { "type": "string" } },
    "rollback_scope": { "type": "object" },
    "out_of_scope": { "type": "array", "items": { "type": "string" } }
  }
}
```

## 9. TargetReservation

```json
{
  "contract_type": "target_reservation",
  "required": [
    "target_id",
    "reserved",
    "reservation_reason",
    "allowed_use",
    "enforcement_scope",
    "current_users",
    "mutation_allowed"
  ],
  "properties": {
    "target_id": { "type": "string" },
    "reserved": { "type": "boolean" },
    "reservation_reason": { "type": "string" },
    "allowed_use": { "type": "array", "items": { "type": "string" } },
    "enforcement_scope": { "type": "array", "items": { "type": "string" } },
    "current_users": { "type": "integer" },
    "mutation_allowed": { "type": "boolean" }
  }
}
```

## 10. DelayedMonitoringContract

```json
{
  "contract_type": "delayed_monitoring_contract",
  "required": [
    "monitor_id",
    "operation_id",
    "required_samples",
    "sample_interval_seconds",
    "monitored_fields",
    "closeout_conditions",
    "unexpected_movement_policy"
  ],
  "properties": {
    "monitor_id": { "type": "string" },
    "operation_id": { "type": "string" },
    "required_samples": { "type": "integer" },
    "sample_interval_seconds": { "type": "integer" },
    "monitored_fields": { "type": "array", "items": { "type": "string" } },
    "closeout_conditions": { "type": "array", "items": { "type": "string" } },
    "unexpected_movement_policy": { "enum": ["hold_apply_and_classify", "manual_review_required"] }
  }
}
```

## Schema Verdict

These schemas make approvals exact, expiring, generation-owned, rollback-aware,
and evidence-linked. They intentionally do not create any mutating API.

## E19 Execution Contract Extension

E19 extends approval previews into disabled execution-governance contracts:

- ExecutionIntent
- ExecutionApproval
- ExecutionConfirmation
- DualConfirmation
- ExecutionBarrier
- RollbackBoundExecution
- ReplayRejection
- ExecutionExpiry
- BlastRadiusEnforcement
- ExecutionDenial
- ExecutionAuditRecord

These objects are exposed through `GET /api/operator/execution-governance-preview`.
They are preview-only, redacted, replay-aware, and do not enable runtime execution.

## E21 First Real Approval Packet Boundary

E21 selects the first future real action as an approval-record and runtime-recheck
transition only:

- no user movement;
- no routing mutation;
- no autoswitch apply;
- no browser-triggered execution;
- CLI packet execution recommended;
- production approval persistence required;
- dual operator auth required;
- live runtime recheck required.

The selected first action is:

```text
F_READONLY_TO_EXECUTION_TRANSITION_PACKET_WITH_ZERO_MOVE_GENERATION_CLEARANCE_AS_NEXT_BOUNDARY
```

This means the first real step proves approval/audit persistence before any
runtime-affecting action is considered.

## E22 Packet Consumer Result

E22 implements the CLI packet consumer and append-only audit store. In the local
workspace the first zero-movement packet failed closed with `DENY_STALE_RUNTIME`
because live runtime registry files were unavailable. A denial audit record was
persisted and replay rejection was verified.

Approval success remains blocked until the same packet consumer can run against
fresh VPS runtime state.
