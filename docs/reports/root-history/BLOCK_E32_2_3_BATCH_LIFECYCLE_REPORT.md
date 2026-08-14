# BLOCK E32.2.3 Batch Lifecycle Report

e32_2_3_completed=true

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

batch_lifecycle_defined=true
state_inventory_defined=true
state_transition_model_defined=true
approval_flow_defined=true
execution_flow_defined=true
observation_flow_defined=true
rollback_flow_defined=true
failure_flow_defined=true
production_pool_compatible=true

## Summary

E32.2.3 defines the full execution batch lifecycle. The lifecycle preserves the E32.2.1/E32.2.2 principle that a batch is scope and metadata, not execution authority.

Execution requires approval packet, execution-time recheck, capacity gates, runtime gates, restore-settle, target eligibility, and audit lineage.

## State Inventory

Transient states:

```text
DRAFT
PRECHECKED
APPROVED
SCHEDULED
EXECUTING
OBSERVING
ROLLBACK_READY
ROLLING_BACK
```

Terminal states:

```text
COMPLETED
FAILED_CLOSED
REPLAY_DENIED
CANCELLED
EXPIRED
```

## Primary Lifecycle

Proof-style lifecycle:

```text
DRAFT
  -> PRECHECKED
  -> APPROVED
  -> SCHEDULED
  -> EXECUTING
  -> OBSERVING
  -> ROLLBACK_READY
  -> ROLLING_BACK
  -> COMPLETED
```

## Approval Flow

Approval requires:

- complete batch metadata;
- complete rollback manifest;
- valid movement budget and blast radius;
- capacity requirements;
- approval packet;
- audit lineage;
- operator confirmation where required.

Approval does not authorize mutation until execution-time recheck.

## Execution Flow

Execution requires:

- non-expired packet and batch;
- packet not replayed;
- exact user and target match;
- complete rollback manifest;
- capacity status `CERTIFIED`;
- movement budget within effective and available capacity;
- runtime checkers OK;
- restore-settle GO;
- selected moves zero;
- hidden movers absent.

## Observation Flow

Observation requires runtime samples, delayed movement checks, replay readiness, and audit completion. Proof-style batches proceed to rollback readiness after observation.

## Rollback Flow

Rollback states:

```text
ROLLBACK_READY
ROLLING_BACK
```

Rollback requires exact affected user set, exact rollback targets, known route tables when applicable, audit events, and no blast-radius expansion.

## Failure Flow

Failure states:

```text
FAILED_CLOSED
EXPIRED
CANCELLED
REPLAY_DENIED
```

Terminal states cannot resume execution directly. Recovery requires a new batch generation, fresh approval packet, or a separate rollback/containment batch.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- retained_production_pool_completion_semantics
- exact_status_transition_table_schema
- reservation_release_timing_for_concurrent_batches
- partial_forward_failure_policy
```

Recommended:

- keep proof-style batches on default rollback until production-pool retention is certified;
- encode transitions as an explicit allowlist table;
- release reservations only after terminal audit closure;
- require immediate rollback/containment on partial forward failure until partial-completion semantics are certified.

## Remaining Open Questions

- whether `OBSERVING -> COMPLETED` without rollback is allowed for first production-pool retained movement;
- exact scheduler interaction with `SCHEDULED`;
- whether cancellation after `EXECUTING` should become containment rather than cancellation;
- exact representation of replay attempts as child audit events.

recommended_next_block=E32_2_4_BATCH_VALIDATION_METHODOLOGY

## Evidence Files

- `docs/track7/productization/e32_2_3-evidence/state-inventory.md`
- `docs/track7/productization/e32_2_3-evidence/state-transition-model.md`
- `docs/track7/productization/e32_2_3-evidence/approval-flow.md`
- `docs/track7/productization/e32_2_3-evidence/execution-flow.md`
- `docs/track7/productization/e32_2_3-evidence/observation-flow.md`
- `docs/track7/productization/e32_2_3-evidence/rollback-flow.md`
- `docs/track7/productization/e32_2_3-evidence/failure-flow.md`
- `docs/track7/productization/e32_2_3-evidence/production-pool-compatibility.md`
- `docs/track7/productization/e32_2_3-evidence/final-lifecycle-decision.md`
- `docs/track7/productization/e32_2_3-evidence/tests.md`

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO

