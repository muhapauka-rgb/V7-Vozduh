# E32.2.B Production Pool Compatibility

production_pool_compatible=true

## Policy Engine

Compatible.

The policy engine can consume:

- validation gates;
- batch state;
- failure modes;
- fail-closed matrix;
- capacity status;
- risk score;
- next safe action.

Policy engine must deny forward execution for any batch failure mode.

## Scheduler

Compatible.

Scheduler can use:

- execution eligibility;
- execution window;
- blocked reasons;
- capacity reservations;
- status transitions;
- failure mode state.

Scheduler cannot bypass execution-time recheck.

## Concurrency Controls

Compatible with reservation ledger dependency.

Concurrency must respect:

- available capacity;
- reserved capacity;
- batch status;
- failure state;
- packet freshness;
- reservation expiry.

Until concurrency is certified:

```text
max_concurrent_batches=1
```

## Observability Scaling

Compatible.

Operators can see per-batch and aggregate:

- status;
- type;
- affected users;
- capacity state;
- blocked reasons;
- failure mode;
- next safe action;
- audit lineage.

## Production Pool

Compatible.

Batch operations define how production-pool batches are validated, observed, denied, contained, and audited.

They do not certify production-pool execution by themselves.

## Compatibility Verdict

Execution batch operations are production-pool compatible.
