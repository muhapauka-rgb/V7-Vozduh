# E32.2.1 Production Pool Compatibility

production_pool_compatible=true

## Compatibility Scope

Execution Batch Model is reviewed against future:

- Policy Engine
- Scheduler
- Concurrency Controls
- Observability
- Production Pool

## Policy Engine

Compatible.

The policy engine can evaluate:

- batch type;
- allowed users;
- destination target;
- source targets;
- rollback manifest;
- capacity requirements;
- policy cap;
- execution window;
- operator context.

Policy engine must not authorize movement without approval packet and execution-time recheck.

## Scheduler

Compatible.

The scheduler can consume:

- batch status;
- execution window;
- destination target;
- required capacity;
- available capacity;
- reservation state;
- batch priority when later defined.

Scheduler must deny execution on stale packets, missing capacity, reservation conflict, target ineligibility, or runtime checker failure.

## Concurrency Controls

Compatible with a reservation ledger dependency.

Before concurrent batches:

```text
reservation_ledger_required=true
max_concurrent_batches=1_until_certified
```

This matches E32.1 capacity runtime impact and failure modes.

## Observability

Compatible.

Operators can see:

- batch id;
- batch type;
- status;
- allowed users;
- movement budget;
- blast radius;
- destination;
- rollback manifest;
- capacity gate state;
- current denial reason;
- audit lineage.

## Production Pool

Compatible.

Execution batches provide the unit of work for production-pool operation while preserving:

- exact scope;
- capacity gates;
- approval packet binding;
- rollback;
- replay protection;
- audit lineage.

## Compatibility Verdict

Execution Batch Model is compatible with production-pool architecture and ready for later E32 tracks.

