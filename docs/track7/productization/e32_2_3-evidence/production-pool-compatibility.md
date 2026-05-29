# E32.2.3 Production Pool Compatibility

production_pool_compatible=true

## Policy Engine

Compatible.

The policy engine can evaluate:

- allowed state transitions;
- approval preconditions;
- execution-time gates;
- failure transitions;
- terminal state behavior;
- recovery path requirements.

Policy may deny or cancel a batch, but cannot mutate approved scope without a new generation.

## Scheduler

Compatible.

The scheduler can operate on:

- `PRECHECKED`;
- `APPROVED`;
- `SCHEDULED`;
- `EXPIRED`;
- `CANCELLED`;
- `FAILED_CLOSED`.

Scheduler cannot skip execution-time recheck before `EXECUTING`.

## Concurrency Controls

Compatible with future reservation ledger.

Concurrency-sensitive transitions:

- `APPROVED -> SCHEDULED`;
- `SCHEDULED -> EXECUTING`;
- `EXECUTING -> OBSERVING`;
- terminal release of reservations.

Before reservation ledger certification:

```text
max_concurrent_batches=1
```

## Production Pool

Compatible.

The lifecycle supports:

- operator movement batches;
- rollback batches;
- evacuation batches;
- capacity rebalance batches;
- staged migration batches;
- containment batches.

Production-pool retained movement requires a later block to define `OBSERVING -> COMPLETED` without default rollback.

## Compatibility Verdict

Batch lifecycle is production-pool compatible without granting production-pool execution authority.

