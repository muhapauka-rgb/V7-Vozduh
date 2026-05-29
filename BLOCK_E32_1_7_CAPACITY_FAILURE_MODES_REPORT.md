# BLOCK E32.1.7 Capacity Failure Modes Report

e32_1_7_completed=true

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

capacity_failure_modes_defined=true
failure_mode_inventory_defined=true
detection_model_defined=true
runtime_impact_model_defined=true
operator_action_model_defined=true
alert_observability_model_defined=true
fail_closed_matrix_defined=true
production_pool_compatible=true

## Summary

E32.1.7 defines capacity failure modes and their fail-closed behavior. Every capacity failure mode blocks forward movement by default. Rollback remains available only as containment when exact rollback scope is known.

## Failure Modes

- `CAPACITY_STALE`
- `CAPACITY_DEGRADED`
- `CAPACITY_EXPIRED`
- `CAPACITY_REVOKED`
- `CAPACITY_UNKNOWN`
- `CAPACITY_CONFLICT`
- `CAPACITY_EVIDENCE_MISSING`
- `CAPACITY_CONFIDENCE_DROP`
- `CAPACITY_POLICY_CAP_EXCEEDED`
- `CAPACITY_RESERVATION_CONFLICT`

## Runtime Impact

Forward movement:

```text
allowed=false for all capacity failure modes
```

Rollback:

```text
allowed only as containment when exact rollback scope is known
```

Scheduler:

```text
admission_denied for all capacity failure modes except explicit rollback/containment workflow
```

## Operator Next Actions

- stale -> refresh validation
- degraded -> diagnose/remediate
- expired -> full recertification
- revoked -> incident review
- unknown -> inspect/discover
- conflict -> reconcile metadata/evidence
- evidence missing -> reconstruct evidence or recertify
- confidence drop -> recertify or downgrade
- policy cap exceeded -> lower batch or request policy review
- reservation conflict -> resolve ledger/packet state

## Alerts

Mapped alerts:

- `CAPACITY_STALE`
- `CAPACITY_DEGRADED`
- `CAPACITY_EXPIRED`
- `CAPACITY_REVOKED`
- `CAPACITY_UNKNOWN`
- `CAPACITY_CONFLICT`
- `CAPACITY_EVIDENCE_MISSING`
- `CONFIDENCE_DROP`
- `POLICY_CAP_EXCEEDED`
- `RESERVATION_CONFLICT`

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- automatic_reservation_conflict_resolution_scope
```

Recommended:

```text
automation may release clearly expired reservations;
ledger/audit disagreement requires human review
```

## Remaining Open Questions

- exact implementation of reservation expiry detection;
- whether `REVOKED` should be a separate capacity status or a status plus incident flag;
- whether confidence drop should automatically downgrade class or only block execution;
- how long failure alerts remain visible after resolution;
- whether policy cap exceeded should be warning-only during planning but hard-deny at execution.

recommended_next_block=E32_1_8_CAPACITY_CLASSES_CERTIFICATION

## Evidence Files

- `docs/track7/productization/e32_1_7-evidence/failure-mode-inventory.md`
- `docs/track7/productization/e32_1_7-evidence/detection-model.md`
- `docs/track7/productization/e32_1_7-evidence/runtime-impact-model.md`
- `docs/track7/productization/e32_1_7-evidence/operator-action-model.md`
- `docs/track7/productization/e32_1_7-evidence/alert-observability-model.md`
- `docs/track7/productization/e32_1_7-evidence/fail-closed-matrix.md`
- `docs/track7/productization/e32_1_7-evidence/production-pool-compatibility.md`
- `docs/track7/productization/e32_1_7-evidence/final-model-decision.md`
- `docs/track7/productization/e32_1_7-evidence/tests.md`

## Final Mutation Statement

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO

Autoswitch apply performed manually: NO

Canary performed: NO

Cohort performed: NO

