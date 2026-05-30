# E32.5.C Dispatch Boundary Review

scheduler_authority_boundary_valid=true

## Boundary Assertions

Scheduler cannot:

- choose users;
- choose targets;
- override policy DENY;
- bypass capacity;
- bypass concurrency;
- bypass execution-time recheck;
- bypass approval packet;
- mutate runtime.

## Certified Scheduler Identity

```text
scheduler_is_authority=false
scheduler_is_runtime_mutation=false
scheduler_is_time_ordering_layer=true
```

## Dispatch Boundary

DISPATCHED means:

- schedule is handed to execution path;
- owner transfer may occur;
- execution-time recheck must still run;
- packet validity must still be verified;
- locks and reservations must still be valid;
- batch scope remains unchanged.

DISPATCHED does not mean:

- users moved;
- routes changed;
- packet consumed as execution;
- capacity/policy/concurrency bypassed;
- runtime mutation occurred.

## Decision

scheduler_authority_boundary_valid=true
