# E32.1.3 Production Pool Compatibility

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

production_pool_compatible=true

## Compatibility With Capacity Classes

Compatible.

Lifecycle states apply to every capacity class and preserve E32.1.1 boundaries:

- CLASS_10 is current certified maximum;
- CLASS_20/50/100 require additional lifecycle promotion;
- PRODUCTION_POOL remains an architecture target until policy is certified.

## Compatibility With Metadata Model

Compatible.

Lifecycle states map directly to E32.1.2 `capacity_status`:

- UNCERTIFIED maps to UNKNOWN;
- CANDIDATE maps to CANDIDATE;
- VALIDATING maps to VALIDATING;
- CERTIFIED maps to CERTIFIED;
- STALE maps to STALE;
- DEGRADED maps to DEGRADED;
- EXPIRED maps to EXPIRED;
- REVOKED maps to EXPIRED plus revoked flag or separate terminal state.

## Compatibility With Execution Batches

Compatible.

Execution batches can query:

- class;
- status;
- effective cap;
- available capacity;
- freshness;
- evidence pointers;
- reservation state.

## Compatibility With Policy Engine

Compatible.

The policy engine can enforce:

- TTL;
- demotion;
- reservations;
- packet count limits;
- production-pool caps;
- denial on missing evidence.

## Compatibility With Scheduling

Compatible.

Scheduling can use RECERTIFYING, STALE, and capacity reservations to prevent stale or overbooked target use.

## Compatibility With Production Pool

Compatible, with one boundary:

Production pool cannot inherit CLASS_10 as open-ended production authority. It must certify policy controls, concurrency, audit volume, rollback orchestration, and scheduling behavior before production-pool movement is allowed.

