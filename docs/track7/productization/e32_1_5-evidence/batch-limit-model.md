# E32.1.5 Batch Limit Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

batch_limit_model_defined=true

## Effective Cap

```text
effective_batch_cap = min(certified_capacity, hard_limit, active_policy_cap)
```

If `capacity_status` is not fresh `CERTIFIED`, effective forward cap is treated as zero.

## Available Capacity

```text
available_capacity = effective_batch_cap - target_users_count - capacity_reserved
```

For execution-only targets today:

```text
target_users_count must be 0 before forward unless packet explicitly allows occupied target
capacity_reserved=0 unless one active packet exists
max_concurrent_batches=1
```

## Class Batch Caps

| Class | Certified Capacity | Max Batch Size | Max Concurrent Batch Size | Policy Cap Interaction |
| --- | ---: | ---: | ---: | --- |
| CLASS_1 | 1 | 1 | 1 | Policy may lower to 0 or 1. |
| CLASS_2 | 2 | 2 | 1 | Policy may lower to 0-2. |
| CLASS_4 | 4 | 4 | 1 | Policy may lower to 0-4. |
| CLASS_10 | 10 | 10 | 1 | Policy may lower to 0-10. |
| CLASS_20 | 20 only after certification | 20 after certification | 1 until scheduling model is certified | Policy may lower to 0-20. |
| CLASS_50 | 50 only after certification | 50 after certification | Requires production-pool scheduler decision | Policy-controlled. |
| CLASS_100 | 100 only after certification | 100 after certification | Requires production-pool scheduler decision | Policy-controlled. |

## Current Target

```text
target=amneziawg-exec-20260528-10-8-1-14
capacity_class=CLASS_10
certified_capacity=10
hard_limit=10
active_policy_cap=10
effective_batch_cap=10
max_concurrent_batches=1
```

## ARCHITECTURE_DECISION_REQUIRED

decision_needed=max_concurrent_batches_for_production_pool

Options:

1. Keep `max_concurrent_batches=1` for all classes.
2. Allow concurrent batches only after reservation ledger certification.
3. Allow policy engine to decide concurrency based on available capacity.

Recommended option:

```text
Option 2: allow concurrent batches only after reservation ledger certification.
```

Reason:

Concurrency without a reservation ledger can overbook target capacity and obscure rollback scope.

