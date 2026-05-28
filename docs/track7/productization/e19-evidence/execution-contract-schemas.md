# E19 Execution Contract Schemas

## ExecutionIntent

```json
{
  "object_type": "ExecutionIntent",
  "operation_id": "string",
  "intent": "bounded_movement_or_restore_action",
  "scope": "ExecutionBoundary",
  "execution_allowed_now": false,
  "preview_only": true
}
```

## ExecutionApproval

```json
{
  "object_type": "ExecutionApproval",
  "approval_id_preview": "string",
  "approval_actor_required": true,
  "generation_id_required": true,
  "selected_move_fingerprint_required": true,
  "rollback_manifest_required": true,
  "runtime_snapshot_hash_required": true,
  "status": "NOT_REQUESTED_PREVIEW_ONLY"
}
```

## DualConfirmation

```json
{
  "object_type": "DualConfirmation",
  "sequence": [
    "primary_approval",
    "independent_second_confirmation",
    "freshness_recheck",
    "execution_boundary_recheck"
  ],
  "both_operators_required": true,
  "same_actor_allowed": false
}
```

## ReplayRejection

```json
{
  "object_type": "ReplayRejection",
  "reject_on_generation_mismatch": true,
  "reject_on_selected_move_fingerprint_mismatch": true,
  "reject_on_runtime_snapshot_hash_mismatch": true,
  "reject_on_expired_approval": true,
  "reject_on_stale_evidence": true
}
```

## RollbackBoundExecution

```json
{
  "object_type": "RollbackBoundExecution",
  "rollback_manifest": "RollbackManifestPreview",
  "rollback_required_before_execution": true,
  "partial_rollback_policy": "abort_and_contain_until_operator_review"
}
```

## ExecutionAuditRecord

```json
{
  "object_type": "ExecutionAuditRecord",
  "immutable_execution_id_required": true,
  "lineage_required": [
    "approval_lineage",
    "execution_lineage",
    "rollback_lineage",
    "delayed_movement_lineage",
    "replay_denial_lineage",
    "containment_lineage"
  ],
  "runtime_write_in_stage": false
}
```

## Verdict

execution_contracts_complete=true
mutating_execution_still_disabled=true
execution_allowed_now=false
