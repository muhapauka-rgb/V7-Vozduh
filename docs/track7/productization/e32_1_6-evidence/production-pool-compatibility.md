# E32.1.6 Production Pool Compatibility

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

production_pool_compatible=true

## Execution Batches

Compatible.

Observability exposes:

- movement budget;
- effective cap;
- available cap;
- reservation state;
- target eligibility;
- denial reasons.

## Scheduler

Compatible.

Scheduler needs visibility into:

- target available capacity;
- capacity reservations;
- max concurrent batches;
- stale/expiration status;
- next refresh deadline.

## Policy Engine

Compatible.

Policy engine needs visibility into:

- active policy cap;
- policy cap blockers;
- route-class restrictions;
- confidence thresholds;
- status transitions.

## Production Pool

Compatible but not sufficient alone.

Production pool observability must add:

- aggregate pool capacity;
- per-target capacity;
- reserved capacity;
- scheduled batches;
- failed admission reasons;
- rollback orchestration state;
- audit volume health.

## ARCHITECTURE_DECISION_REQUIRED

decision_needed=capacity_dashboard_authoritative_source

Options:

1. Dashboard reads registry, state files, audit, and helpers directly.
2. Dashboard reads a generated capacity view model.
3. Dashboard reads a policy-engine API.

Recommended option:

```text
Option 2 now, Option 3 after policy engine exists.
```

Reason:

Direct reads can produce inconsistent operator views. A generated view model can be tested and versioned before a policy-engine API is available.

