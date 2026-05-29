# BLOCK E32.1.5 Capacity Runtime Impact Report

e32_1_5_completed=true

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

capacity_runtime_impact_defined=true
execution_impact_defined=true
batch_limit_model_defined=true
status_impact_model_defined=true
target_eligibility_model_defined=true
execution_gate_model_defined=true
rollback_exception_model_defined=true
governance_integration_defined=true
future_scale_compatible=true

## Summary

E32.1.5 defines how capacity affects runtime behavior. Capacity is a forward-execution gate, not an execution authority by itself. A target needs fresh certified capacity, sufficient effective and available capacity, readiness GO, restore-settle GO, runtime checker health, valid packet semantics, and execution-time recheck before movement can proceed.

## Runtime Decisions Affected

- approval packet creation;
- execution-time recheck;
- target eligibility;
- batch size;
- scheduler eligibility;
- production-pool admission;
- rollback exception handling.

## Batch Limit

```text
effective_batch_cap = min(certified_capacity, hard_limit, active_policy_cap)
available_capacity = effective_batch_cap - target_users_count - capacity_reserved
```

Current target:

```text
target=amneziawg-exec-20260528-10-8-1-14
capacity_class=CLASS_10
capacity_status=CERTIFIED
capacity_confidence=HIGH
effective_batch_cap=10
max_concurrent_batches=1
```

## Status Impact

Only fresh `CERTIFIED` status permits forward movement eligibility.

Forward movement is denied for:

- `STALE`
- `DEGRADED`
- `EXPIRED`
- `REVOKED`
- `UNKNOWN`
- `CANDIDATE`
- `VALIDATING`

## Execution Gates

Capacity-related gates:

- `GATE_CAPACITY_CERTIFIED`
- `GATE_CAPACITY_FRESH`
- `GATE_CAPACITY_CONFIDENCE`
- `GATE_BATCH_WITHIN_EFFECTIVE_CAP`
- `GATE_AVAILABLE_CAPACITY`
- `GATE_TARGET_HARD_LIMIT`
- `GATE_POLICY_CAP`
- `GATE_TARGET_ELIGIBLE`

## Rollback Exception

Rollback remains allowed as containment when capacity is stale, degraded, or expired, provided:

- exact rollback user set is known;
- exact rollback target is known;
- route table mapping is known;
- rollback does not expand blast radius.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- max_concurrent_batches_for_production_pool
- production_pool_capacity_reservation_runtime_semantics
```

Recommended:

- keep `max_concurrent_batches=1` until reservation ledger certification;
- use a dedicated runtime-safe reservation ledger for production-pool capacity reservations.

## Remaining Open Questions

- exact reservation ledger storage and transaction model;
- whether target users count or reserved capacity should dominate scheduler admission when both are nonzero;
- whether production-pool policy cap should be global, per target, per class, or per route class;
- how to present capacity denials to operator workflows.

recommended_next_block=E32_1_6_CAPACITY_OBSERVABILITY

## Evidence Files

- `docs/track7/productization/e32_1_5-evidence/execution-impact-review.md`
- `docs/track7/productization/e32_1_5-evidence/batch-limit-model.md`
- `docs/track7/productization/e32_1_5-evidence/status-impact-model.md`
- `docs/track7/productization/e32_1_5-evidence/target-eligibility-model.md`
- `docs/track7/productization/e32_1_5-evidence/execution-gate-model.md`
- `docs/track7/productization/e32_1_5-evidence/rollback-exception-model.md`
- `docs/track7/productization/e32_1_5-evidence/governance-integration.md`
- `docs/track7/productization/e32_1_5-evidence/future-scale-review.md`
- `docs/track7/productization/e32_1_5-evidence/final-model-decision.md`
- `docs/track7/productization/e32_1_5-evidence/tests.md`

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO

