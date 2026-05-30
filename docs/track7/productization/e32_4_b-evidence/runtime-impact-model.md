# E32.4.B Runtime Impact Model

concurrency_runtime_impact_defined=true

## Scope

Concurrency controls affect runtime eligibility and admission decisions. They do not execute runtime mutation, user movement, routing mutation, autoswitch apply, canary, or cohort execution.

## Execution Eligibility

Forward execution is eligible only when:

- required BATCH_LOCK is held by the executing owner;
- required PACKET_LOCK confirms packet is non-expired, non-replayed, and bound to the same batch;
- all candidate USER_LOCKS are held in canonical sorted order;
- target is eligible and any required TARGET_LOCK is compatible;
- capacity and target reservations are active, owner-matched, and non-conflicting;
- runtime gates, policy gates, capacity gates, and execution-time recheck remain GO.

If any required lock or reservation is missing, stale, conflicted, or owned by another actor, forward execution is denied.

## Scheduler Admission

Scheduler admission may reserve capacity and target eligibility but may not mutate users.

Scheduler admission is blocked by:

- active conflicting BATCH_LOCK;
- active conflicting USER_LOCK;
- capacity reservation overcommit;
- target reservation conflict;
- policy denial or review-required decision;
- stale reservation or stale packet lineage.

## Batch Execution

Batch execution requires:

- BATCH_LOCK owner matches executor;
- batch state transition compare-and-set succeeds;
- packet consumption is atomic;
- USER_LOCKS cover exactly the approved user set;
- reservation capacity covers batch size.

Concurrent batch execution attempts must fail closed.

## Rollback Execution

Rollback remains allowed for exact known rollback scope even when forward movement is denied by concurrency state.

Rollback requires:

- known moved user set;
- rollback manifest;
- USER_LOCKS for users being rolled back;
- BATCH_LOCK or rollback_operation_id;
- audit record for containment.

Rollback may not expand blast radius or touch unrelated users.

## Packet Consumption

PACKET_LOCK protects:

- packet refresh;
- packet expiry handling;
- packet execution consumption;
- replay validation;
- cancellation.

Packet consumption must be single-use. A concurrent replay or second execution attempt returns DENY_REPLAY and performs no movement.

## Reservation Ownership

Reservation ownership gates:

- capacity admission;
- target admission;
- batch approval;
- execution-time recheck.

A reservation may be consumed only by its owning batch. Unknown owner, expired reservation, or mismatched fencing token denies forward movement.

## Decision

concurrency_runtime_impact_defined=true
