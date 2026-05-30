# E32.5.A Scheduling Model

scheduling_model_defined=true

## Scheduler Definition

Scheduler is the time-ordering and dispatch-preparation layer for already prepared/admissible batches.

It answers:

- when a batch may run;
- in what order queued batches should run;
- whether the execution window is open;
- whether dependencies are satisfied;
- whether a scheduled execution has expired;
- whether scheduler ownership can transfer to execution.

## Authority Boundary

```text
scheduler_is_authority=false
scheduler_is_runtime_mutation=false
scheduler_is_time_ordering_layer=true
```

Scheduler is not Routing Intelligence.

Scheduler does not decide:

- why a user should switch;
- which user should switch;
- which target should be selected;
- whether policy should allow a batch;
- whether capacity is certified;
- whether locks may be bypassed.

## Non-Bypass Rules

Scheduler must not bypass:

- policy admission;
- approval packet requirements;
- execution-time recheck;
- capacity gates;
- concurrency locks;
- reservations;
- rollback manifest;
- audit lineage;
- fail-closed denial.

## Scheduler Outputs

Scheduler may produce:

- schedule status;
- queue position;
- dispatch readiness;
- blocked reason;
- dependency status;
- window status;
- expiration status;
- owner transfer request.

Scheduler may not produce runtime mutation.

## Decision

scheduling_model_defined=true
