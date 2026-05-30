# E32.4.A Integration Review

capacity_compatible=true
batches_compatible=true
policy_compatible=true

## Capacity Program Compatibility

Concurrency controls preserve the capacity model:

- capacity remains a forward-execution gate, not an authority;
- effective_batch_cap remains derived from certified capacity, hard_limit, and active_policy_cap;
- CAPACITY_RESERVATION prevents double-spending available capacity;
- target overcommit fails closed;
- stale, degraded, expired, or revoked capacity denies forward movement;
- rollback remains allowed for exact known scope.

capacity_compatible=true

## Execution Batches Compatibility

Concurrency controls fit the batch lifecycle:

- BATCH_LOCK serializes lifecycle transitions;
- PACKET_LOCK prevents replay or concurrent packet refresh;
- USER_LOCKS protect approved users and rollback scope;
- reservations bind batch, target, capacity, packet, and rollback manifest;
- partial-forward and partial-rollback paths remain containment flows, not broad automation.

batches_compatible=true

## Policy Engine Compatibility

Concurrency controls preserve policy authority boundaries:

- policy_is_authority=false;
- policy_is_runtime_mutation=false;
- policy_is_admission_logic=true;
- policy can deny, allow, require review, or require additional gates;
- policy cannot acquire runtime mutation authority;
- policy version changes require fresh admission or execution-time recheck.

policy_compatible=true

## Cross-Layer Admission Order

The safest cross-layer order is:

```text
draft batch
candidate set validation
capacity eligibility
policy admission
reservation acquisition
approval packet generation
execution-time recheck
lock acquisition
forward execution
observation
rollback or completion
reservation release
audit finalization
```

## Decision

The concurrency foundation is compatible with Capacity Program, Execution Batches, and Policy Engine architecture without granting any layer new runtime mutation authority.
