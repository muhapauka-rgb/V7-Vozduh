# E32.1.5 Final Runtime Impact Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

capacity_runtime_impact_defined=true

## Final Rule

Capacity controls forward movement eligibility. It does not authorize movement by itself.

Forward execution requires:

```text
fresh CERTIFIED capacity
effective_batch_cap >= movement_budget
available_capacity >= movement_budget
capacity_confidence >= required_confidence
readiness GO
restore-settle GO
runtime checkers OK
packet valid
execution-time recheck pass
```

## Current Target Runtime Impact

```text
target=amneziawg-exec-20260528-10-8-1-14
capacity_class=CLASS_10
capacity_status=CERTIFIED
capacity_confidence=HIGH
effective_batch_cap=10
max_concurrent_batches=1
```

## Deny By Default

Forward execution is denied for:

- STALE;
- DEGRADED;
- EXPIRED;
- REVOKED;
- UNKNOWN;
- CANDIDATE;
- VALIDATING.

## Rollback Exception

Rollback remains allowed as containment during STALE, DEGRADED, or EXPIRED states when exact rollback scope is known.

## Production Pool Boundary

Production pool must not consume capacity until scheduler, reservation ledger, observability, rollback orchestration, and audit volume controls are certified.

recommended_next_block=E32_1_6_CAPACITY_OBSERVABILITY

