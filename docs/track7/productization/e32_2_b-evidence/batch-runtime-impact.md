# E32.2.B Batch Runtime Impact

batch_runtime_impact_defined=true

## Principle

Batch architecture defines potential runtime impact, but this block performs no runtime mutation.

Actual runtime mutation may occur only in a future explicitly authorized execution block.

## users.registry Impact

Forward movement batches may change:

```text
allowed_user.current: source_target -> destination_target
```

Constraints:

- only `allowed_users`;
- only approved destination target;
- no unrelated users;
- no implicit cohort expansion.

Rollback batches may change:

```text
affected_user.current: current_target -> rollback_target
```

Constraints:

- only rollback manifest users;
- only known rollback targets.

## Route Table Impact

Forward movement may update only route tables mapped to approved users.

Rollback may restore only route tables mapped to rollback users.

Forbidden:

- broad routing-sync;
- route mutation for unrelated users;
- route class mutation outside batch scope.

## Capacity Reservation Impact

Future production-pool batches may reserve capacity:

```text
reserved_capacity += movement_budget
```

Reservation must be released on terminal states:

- `COMPLETED`;
- `FAILED_CLOSED`;
- `CANCELLED`;
- `EXPIRED`;
- `REPLAY_DENIED`.

Until reservation ledger certification:

```text
max_concurrent_batches=1
```

## Audit Impact

Every batch operation writes or references:

- batch ledger record;
- approval record;
- packet record;
- forward events;
- rollback events;
- denial events;
- replay events;
- evidence paths.

## Packet Impact

Execution consumes the approval packet.

After successful forward:

```text
packet_consumed=true
replay_must_deny=true
```

## Rollback Impact

Rollback is runtime mutation, but only as:

- planned proof-style rollback;
- failure containment;
- exact manifest rollback.

Rollback must not expand blast radius.

## Runtime Impact Verdict

Batch runtime impact is defined and bounded to approved users, route tables, packet state, audit lineage, capacity reservation, and rollback manifest.
