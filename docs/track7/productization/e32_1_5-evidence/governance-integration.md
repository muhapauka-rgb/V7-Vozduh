# E32.1.5 Governance Integration

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

governance_integration_defined=true

## Approval Packets

Approval packets must bind:

- capacity class;
- capacity status;
- certified capacity;
- hard limit;
- active policy cap;
- effective batch cap;
- available capacity;
- target users count;
- validation evidence;
- freshness thresholds.

Packets are non-executable unless capacity gates pass at creation and at execution-time recheck.

## Execution-Time Recheck

Execution-time recheck is authoritative for runtime decision.

It must recompute:

- capacity status;
- freshness;
- effective cap;
- available capacity;
- target occupancy;
- policy cap;
- readiness;
- restore-settle;
- runtime checker health.

## Policy Engine

Policy engine may lower active policy cap. It may not raise capacity above certified capacity.

Policy engine future responsibilities:

- TTL enforcement;
- capacity reservation ledger;
- scheduler admission;
- production-pool caps;
- automatic demotion signals.

## Scheduler

Scheduler eligibility requires:

- fresh CERTIFIED capacity;
- available capacity;
- no conflicting packet reservation;
- policy cap sufficient;
- exact target and rollback plan.

Until reservation ledger is certified, scheduler must use:

```text
max_concurrent_batches=1
```

## Production Pool

Production pool may use capacity metadata as input only after:

- production-pool policy model is certified;
- scheduler model is certified;
- observability model is certified;
- rollback orchestration is certified;
- audit volume handling is certified.

