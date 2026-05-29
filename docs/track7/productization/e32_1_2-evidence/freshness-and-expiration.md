# E32.1.2 Freshness And Expiration Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

freshness_model_defined=true

## Design Choice

Capacity metadata has two clocks:

1. Certification history: the audit record that a class was proven.
2. Operational freshness: whether that class may be used for a new approval packet right now.

Historical certification does not expire as a fact. Operational eligibility does expire.

## Recommended Initial TTLs

For bounded operator-driven execution:

```text
capacity_stale_after=24h after latest accepted long-window or class proof
capacity_expiration=7d after latest accepted long-window or class proof
approval_packet_ttl=30m
execution_time_recheck_freshness=immediate / same block
```

For production pool:

```text
capacity_stale_after=6h
capacity_expiration=24h
approval_packet_ttl=15m or scheduler-controlled reservation TTL
execution_time_recheck_freshness=immediate / same scheduler transaction
```

Reasoning:

- E25-E31 proved governance over bounded operator windows, not unattended long-lived pool scheduling.
- Production pool has higher operational risk and should refresh more often.
- Expired or stale capacity should block forward movement, while rollback remains allowed.

## Stale Threshold

When `now >= capacity_stale_after`:

- set `capacity_status=STALE` or compute `is_fresh=false`;
- block new executable approval packets;
- allow refresh validation;
- allow rollback/remediation;
- keep historical certification visible.

## Expiration Threshold

When `now >= capacity_expiration`:

- set `capacity_status=EXPIRED`;
- require full validation refresh before new movement;
- do not use old evidence to calculate `current_capacity`;
- retain the historical audit chain.

## Immediate Invalidation Triggers

Regardless of time, mark stale/degraded/expired on:

- target readiness NO-GO;
- runtime checker failure;
- restore-settle failure;
- hidden movers detected;
- selected_moves nonzero outside approved windows;
- target profile/interface changes;
- NAT/MSS/provisioning integration changes;
- hard_limit lower than class size;
- audit chain inconsistency;
- replay protection failure;
- rollback failure;
- autoswitch/rebalance exclusion violation.

## Refresh Requirements

To refresh STALE capacity without changing class:

- readiness GO;
- restore-settle GO;
- runtime checkers OK;
- target users count expected;
- selected_moves=0;
- hidden movers absent;
- class-appropriate long-window or policy-defined refresh proof.

To recover EXPIRED or DEGRADED capacity:

- rerun class-appropriate validation;
- rebind evidence hashes;
- re-evaluate class status;
- require final safety review before packet generation.

## Fail-Closed Behavior

If freshness cannot be computed:

```text
capacity_status=UNKNOWN
current_capacity=0
execution_allowed=false
```

