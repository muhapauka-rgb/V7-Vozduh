# E32.1.7 Final Failure Mode Decision

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

capacity_failure_modes_defined=true

## Final Failure Mode Set

- CAPACITY_STALE
- CAPACITY_DEGRADED
- CAPACITY_EXPIRED
- CAPACITY_REVOKED
- CAPACITY_UNKNOWN
- CAPACITY_CONFLICT
- CAPACITY_EVIDENCE_MISSING
- CAPACITY_CONFIDENCE_DROP
- CAPACITY_POLICY_CAP_EXCEEDED
- CAPACITY_RESERVATION_CONFLICT

## Final Runtime Rule

All capacity failure modes deny forward movement by default.

Rollback remains available only when it is containment and exact rollback scope is known.

## Final Operator Rule

Every failure mode must provide:

- detection source;
- blocked action;
- allowed containment action;
- next safe action;
- whether human review is required.

## Final Production Pool Rule

Production pool must treat reservation conflict, policy cap exceeded, and capacity conflict as hard scheduler admission denials.

## Architecture Decision Required

```text
ARCHITECTURE_DECISION_REQUIRED=automatic_reservation_conflict_resolution_scope
recommended_option=automation_may_release_clearly_expired_reservations_only
```

recommended_next_block=E32_1_8_CAPACITY_CLASSES_CERTIFICATION

