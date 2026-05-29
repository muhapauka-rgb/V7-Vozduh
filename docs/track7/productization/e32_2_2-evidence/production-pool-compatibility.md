# E32.2.2 Production Pool Compatibility

production_pool_compatible=true

## Policy Engine

Compatible.

The policy engine can evaluate:

- authoritative batch fields;
- derived eligibility fields;
- risk score;
- capacity requirements;
- runtime drift status;
- packet freshness;
- audit lineage status.

Policy engine must not mutate authoritative scope after approval.

## Scheduler

Compatible.

Scheduler can consume:

- `batch_status`;
- `execution_window`;
- `expires_at`;
- `risk_score`;
- `execution_eligibility`;
- `target_available_capacity`;
- `capacity_gate_status`.

Scheduler cannot execute a batch unless execution-time recheck passes.

## Concurrency Controls

Compatible with future reservation ledger.

Required future fields:

```text
reservation_id
reserved_capacity
reservation_expires_at
concurrency_group
```

These should be introduced in later scheduler/reservation architecture, not guessed in this block.

## Observability

Compatible.

Operators can see:

- authoritative scope;
- derived eligibility;
- status/freshness;
- rollback completeness;
- capacity gate;
- runtime drift;
- audit lineage.

## Production Pool

Compatible.

Batch metadata can become the production-pool unit of scheduling and audit while preserving:

- exact scope;
- fail-closed validation;
- capacity gate integration;
- rollback containment;
- audit lineage.

## Compatibility Verdict

Batch Metadata Model is production-pool compatible.

