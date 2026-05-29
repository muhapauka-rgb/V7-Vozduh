# E32.1.2 Required Capacity Fields

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

required_fields_defined=true

## Required Field Model

| Field | Purpose | Source | Authority | Update Trigger |
| --- | --- | --- | --- | --- |
| `capacity_class` | Active certified class label. | Certification lifecycle. | AUTHORITATIVE | Promotion, downgrade, expiration recovery. |
| `certified_capacity` | Numeric cap implied by certified class. | Capacity class taxonomy. | AUTHORITATIVE | Class promotion/demotion. |
| `current_capacity` | Currently usable batch cap after status and policy. | Derived from class, hard limit, policy, status. | DERIVED | Any status, policy, limit, or readiness change. |
| `soft_limit` | Advisory target occupancy/batch warning. | Egress registry. | AUTHORITATIVE | Capacity requalification or operator lowering. |
| `hard_limit` | Absolute target cap. | Egress registry. | AUTHORITATIVE | Capacity requalification or emergency lowering. |
| `active_policy_cap` | Policy engine cap for this target/context. | Policy engine. | AUTHORITATIVE | Policy update, production-pool scheduling policy. |
| `effective_batch_cap` | Max packet budget allowed now. | Derived formula. | DERIVED | Class, hard limit, policy, status, reservations. |
| `capacity_confidence` | Evidence quality level. | Certification evidence. | AUTHORITATIVE | Validation or evidence invalidation. |
| `capacity_status` | Operational status of capacity metadata. | Certification lifecycle. | AUTHORITATIVE | Validation, degradation, stale/expiry. |
| `capacity_validation_time` | Timestamp of latest accepted capacity validation. | Validation run. | AUTHORITATIVE | New accepted validation. |
| `capacity_validation_method` | Method used to validate capacity. | Validation run. | AUTHORITATIVE | New accepted validation. |
| `capacity_validation_evidence` | Pointers/hashes for evidence. | Evidence store. | AUTHORITATIVE | New accepted validation. |
| `capacity_validation_version` | Schema/tool version used for validation. | Validation tooling. | AUTHORITATIVE | Tool/schema update or validation run. |
| `capacity_expiration` | Hard expiration time for active eligibility. | TTL policy. | AUTHORITATIVE | New validation or manual downgrade. |
| `capacity_stale_after` | Time at which refresh is required before new execution. | TTL policy. | AUTHORITATIVE | New validation or policy update. |
| `last_readiness_status` | Most recent target readiness result. | Readiness helper. | DERIVED SNAPSHOT | Readiness check. |
| `last_restore_settle_status` | Most recent restore-settle result. | Restore-settle helper. | DERIVED SNAPSHOT | Restore-settle check. |
| `last_runtime_checkers_status` | Most recent runtime checker aggregate. | Runtime checkers. | DERIVED SNAPSHOT | Runtime checker run. |
| `target_users_count` | Current target occupancy. | Users registry. | DERIVED SNAPSHOT | Registry read. |
| `capacity_reserved` | Capacity reserved by active approval packets. | Packet/reservation subsystem. | DERIVED OR AUTHORITATIVE LEDGER | Packet creation, expiry, consumption, cancellation. |
| `available_capacity` | Effective cap minus current users and reservations. | Derived formula. | DERIVED | Occupancy/reservation/status change. |

## Field Details

### capacity_class

Purpose: names the active class, such as `CLASS_10`.

Authority: certification lifecycle, not readiness helper alone.

Update triggers:

- successful promotion block;
- downgrade block;
- expiration handling;
- manual safety lowering.

### certified_capacity

Purpose: numeric capacity associated with `capacity_class`.

Examples:

- `CLASS_1 -> 1`
- `CLASS_2 -> 2`
- `CLASS_4 -> 4`
- `CLASS_10 -> 10`

Authority: class taxonomy.

### current_capacity

Purpose: expresses how much movement may be approved now.

Rule:

```text
current_capacity = 0 unless capacity_status == CERTIFIED and freshness is valid
current_capacity = min(certified_capacity, hard_limit, active_policy_cap) when certified and fresh
```

### capacity_confidence

Values:

- `LOW`: static/model-only evidence.
- `MEDIUM`: capacity validation and long-window evidence exist.
- `HIGH`: class-sized governed execution, rollback, delayed monitoring, replay denial, and restore-settle exist.

Current target:

```text
capacity_confidence=HIGH
```

### capacity_status

Purpose: controls whether class metadata may be used for approval.

Allowed values:

```text
UNKNOWN
CANDIDATE
VALIDATING
CERTIFIED
STALE
DEGRADED
EXPIRED
```

### capacity_validation_method

Recommended values:

- `TARGET_LOCAL_PROBE`
- `LONG_WINDOW`
- `GOVERNED_MOVEMENT_PROOF`
- `ROLLBACK_REPLAY_RESTORE_PROOF`
- `PRODUCTION_POOL_POLICY_VALIDATION`

Multiple methods may be stored as a list.

### capacity_validation_evidence

Recommended contents:

- report paths;
- evidence directory paths;
- packet ids;
- audit record hashes;
- registry hashes;
- long-window summary hashes.

### capacity_reserved

Purpose: future concurrency protection.

A packet may reserve capacity before execution. Reserved capacity must expire with the packet and must be released after rollback, cancellation, expiry, or replay denial.

Initial non-concurrent implementation may set:

```text
capacity_reserved=0
max_concurrent_packets=1
```

