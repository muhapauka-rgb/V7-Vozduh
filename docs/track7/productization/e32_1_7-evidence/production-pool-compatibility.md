# E32.1.7 Production Pool Compatibility

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

production_pool_compatible=true

## Execution Batches

Compatible.

Failure modes map to batch admission denials. Batch execution can report exact denial reason instead of a generic NO-GO.

## Policy Engine

Compatible.

Policy engine can consume failure modes as:

- hard deny;
- warning;
- refresh required;
- incident review required;
- policy review required.

## Scheduler

Compatible.

Scheduler must deny admission on:

- stale;
- degraded;
- expired;
- revoked;
- unknown;
- conflict;
- reservation conflict;
- policy cap exceeded.

## Reservation Ledger

Compatible.

Reservation conflicts are first-class failures and must be visible before production-pool scheduling is enabled.

## Operator UI

Compatible.

Operator UI can show:

- failure mode;
- source;
- blocked action;
- allowed containment;
- next safe action.

## ARCHITECTURE_DECISION_REQUIRED

decision_needed=automatic_reservation_conflict_resolution_scope

Options:

1. Only human review may resolve reservation conflicts.
2. Automation may release clearly expired reservations.
3. Automation may reconcile ledger/audit differences.

Recommended option:

```text
Option 2: automation may release clearly expired reservations; ledger/audit disagreement requires human review.
```

Reason:

Expired reservations are mechanical cleanup. Ledger/audit disagreement is a governance integrity issue.

