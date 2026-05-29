# E32.1.2 Governance Integration

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

governance_integration_defined=true

## Approval Packets

Approval packets must bind capacity metadata at creation time:

- `capacity_class`
- `certified_capacity`
- `hard_limit`
- `active_policy_cap`
- `effective_batch_cap`
- `capacity_status`
- `capacity_validation_time`
- `capacity_expiration`
- `capacity_validation_evidence`
- `movement_budget`
- `blast_radius`

Packet generation is denied unless:

```text
capacity_status == CERTIFIED
movement_budget <= effective_batch_cap
blast_radius <= effective_batch_cap
readiness_status == GO
restore_settle_status == GO
runtime_checkers_ok == true
```

## Execution-Time Recheck

Execution-time recheck must recompute:

- current capacity status;
- freshness;
- effective batch cap;
- target users count;
- selected moves count;
- hidden movers status;
- runtime checker status;
- restore-settle status;
- readiness status.

Execution is denied if any packet-bound capacity field conflicts with live authoritative metadata.

## Batch Size Limits

Batch size is constrained by:

```text
movement_budget <= min(certified_capacity, hard_limit, active_policy_cap)
movement_budget <= available_capacity
```

For execution-only targets, autoswitch and rebalance do not consume capacity.

## Rollback Approval

Rollback is not blocked by stale or degraded capacity. Rollback must remain available as containment.

Rollback still requires:

- exact rollback manifest;
- exact approved user set;
- no unrelated movement;
- audit record append;
- post-rollback restore-settle.

## Target Eligibility

A target is eligible for forward movement only when:

- `capacity_status=CERTIFIED`;
- freshness valid;
- readiness GO;
- restore-settle GO;
- runtime checkers OK;
- target role compatible with movement type;
- target is not exposed to unauthorized autoswitch/rebalance usage.

## Production Pool

Production pool must add policy controls:

- policy cap;
- scheduling window;
- concurrent packet limit;
- capacity reservation ledger;
- automatic stale refresh handling;
- operator override controls;
- audit volume controls.

Production pool may use capacity class as an input, but capacity class alone is not production-pool authorization.

## Concurrency And Reservations

Initial safe rule:

```text
max_concurrent_packets=1
capacity_reserved=0 unless one active packet exists
```

Future production-pool rule:

```text
available_capacity = effective_batch_cap - target_users_count - capacity_reserved
```

Each packet reserves `movement_budget` until one of:

- packet expires;
- packet is cancelled;
- forward movement completes and occupancy is reflected;
- rollback completes;
- replay is denied and no reservation remains.

