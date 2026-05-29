# E32.1.5 Future Scale Review

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

future_scale_compatible=true

## CLASS_20

Compatible.

Runtime model can gate CLASS_20 with:

- certified capacity 20;
- hard limit at least 20;
- policy cap at least requested batch;
- available capacity at least requested batch;
- max concurrent batches 1 until reservation ledger exists.

## CLASS_50

Compatible with architecture decision.

Needs:

- production-pool quality floors;
- reservation ledger;
- audit volume controls;
- rollback orchestration;
- scheduler policy.

## CLASS_100

Compatible with architecture decision.

Needs:

- same controls as CLASS_50;
- stronger scheduler and rollback orchestration;
- large-scale observability.

## PRODUCTION_POOL

Compatible, not authorized by this block.

Production pool must define:

- policy cap behavior;
- reservation ledger;
- concurrent batch rules;
- target occupancy handling;
- rollback and incident containment paths.

## ARCHITECTURE_DECISION_REQUIRED

decision_needed=production_pool_capacity_reservation_runtime_semantics

Options:

1. Store reservations in approval packet audit only.
2. Store reservations in a dedicated runtime-safe reservation ledger.
3. Derive reservations dynamically from active packets.

Recommended option:

```text
Option 2: dedicated runtime-safe reservation ledger.
```

Reason:

Audit-only state is hard to query safely at scheduler speed. Pure derivation from packets risks stale parsing and race conditions. A dedicated ledger can be append-only or transactional and can be checked by execution-time recheck.

