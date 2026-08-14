# BLOCK E32.2.2 Batch Metadata Model Report

e32_2_2_completed=true

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

batch_metadata_model_defined=true
authoritative_fields_defined=true
derived_fields_defined=true
status_freshness_model_defined=true
batch_metadata_validation_defined=true
metadata_audit_lineage_defined=true
capacity_runtime_integration_defined=true
production_pool_compatible=true

## Summary

E32.2.2 defines the formal Batch Metadata Model for V7 execution batches.

The model preserves the E32.2.1 rule:

```text
execution_batch = bounded_governance_scope
batch_is_authority=false
```

Batch metadata defines scope, status, timing, rollback, capacity requirements, and audit lineage. It does not authorize execution by itself.

## Authoritative Fields

Authoritative fields include:

- `batch_id`
- `batch_type`
- `batch_generation`
- `batch_status`
- `allowed_users`
- `source_targets`
- `destination_target`
- `rollback_targets`
- `rollback_manifest`
- `movement_budget`
- `blast_radius`
- `approval_packet_id`
- `execution_window`
- `capacity_requirements`
- `operator_context`
- `audit_lineage_id`
- `created_at`
- `expires_at`
- `parent_batch_id`
- `child_batch_ids`

These fields define identity, scope, rollback, capacity requirements, timing, and lineage.

## Derived Fields

Derived fields include:

- `effective_blast_radius`
- `target_capacity_required`
- `target_available_capacity`
- `risk_score`
- `execution_eligibility`
- `rollback_completeness`
- `runtime_drift_status`
- `packet_freshness_status`
- `capacity_gate_status`
- `audit_lineage_status`

Derived fields fail closed when inputs are missing, stale, or conflicting.

## Status And Freshness

Defined batch statuses:

```text
DRAFT
PRECHECKED
APPROVED
SCHEDULED
EXECUTING
OBSERVING
ROLLBACK_READY
ROLLING_BACK
COMPLETED
FAILED_CLOSED
REPLAY_DENIED
CANCELLED
EXPIRED
```

Required timestamps:

- `created_at`
- `expires_at`
- `approved_at`
- `execution_started_at`
- `completed_at`
- `stale_after`

## Validation Model

Batch metadata validation requires:

- exact user set;
- exact target set;
- `movement_budget == len(allowed_users)` for exact movement;
- `blast_radius == len(allowed_users)` for exact movement;
- complete rollback manifest;
- capacity requirements present;
- approval packet present before execution;
- audit lineage present;
- valid execution window.

Any failure denies forward execution.

## Audit Lineage

Metadata binds to:

- batch ledger;
- approval record;
- packet record;
- forward event;
- rollback event;
- replay denial;
- evidence paths.

Every event must reference:

```text
batch_id
audit_lineage_id
packet_id_or_denial_reason
```

## Capacity And Runtime Integration

Batch metadata references:

- `capacity_class`
- `capacity_status`
- `effective_batch_cap`
- `available_capacity`
- runtime checkers;
- restore-settle;
- selected moves;
- hidden movers.

Forward eligibility requires fresh capacity and runtime gates:

```text
capacity_status == CERTIFIED
movement_budget <= effective_batch_cap
movement_budget <= available_capacity
runtime_checkers_ok=true
restore_settle_gate_status=GO
selected_moves_count=0
hidden_movers_absent=true
```

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- batch_metadata_storage_format
- batch_status_transition_table_encoding
- risk_score_formula_owner
- parent_child_batch_lineage_rules
- reservation_fields_for_concurrent_batches
```

Recommended:

- versioned JSON for batch metadata;
- append-only batch ledger for status transitions;
- policy-owned risk score, with `BLOCKED` as hard-coded architecture result;
- child batches reference parent id and lineage id;
- reservation fields deferred to reservation ledger architecture.

## Remaining Open Questions

- exact JSON schema;
- exact status transition graph encoding;
- whether risk score is computed by policy engine or batch validator;
- whether rollback batches reuse original batch id or child batch id;
- how to model reservation fields before concurrency is certified.

recommended_next_block=E32_2_3_BATCH_LIFECYCLE

## Evidence Files

- `docs/track7/productization/e32_2_2-evidence/prior-model-intake.md`
- `docs/track7/productization/e32_2_2-evidence/authoritative-fields.md`
- `docs/track7/productization/e32_2_2-evidence/derived-fields.md`
- `docs/track7/productization/e32_2_2-evidence/status-freshness-model.md`
- `docs/track7/productization/e32_2_2-evidence/validation-model.md`
- `docs/track7/productization/e32_2_2-evidence/audit-lineage-model.md`
- `docs/track7/productization/e32_2_2-evidence/capacity-runtime-integration.md`
- `docs/track7/productization/e32_2_2-evidence/production-pool-compatibility.md`
- `docs/track7/productization/e32_2_2-evidence/final-model-decision.md`
- `docs/track7/productization/e32_2_2-evidence/tests.md`

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO

