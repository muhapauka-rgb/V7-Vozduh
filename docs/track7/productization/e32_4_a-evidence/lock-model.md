# E32.4.A Lock Model

lock_model_defined=true

## Lock Principles

Locks protect short critical sections. Reservations protect planned capacity over a longer lifecycle. A lock alone is not a capacity claim.

All lock acquisition must be fail-closed:

- if a required lock cannot be acquired, forward movement is denied;
- if lock ownership is unknown, forward movement is denied;
- if a lock is stale and cannot be safely recovered, human review is required;
- rollback remains allowed only for exact known rollback scope.

## Lock Types

| Lock | Scope | Owner | Acquisition Rules | Release Rules | Fail-Closed Behavior |
| --- | --- | --- | --- | --- | --- |
| USER_LOCK | One user identity and its route table. | batch_id or rollback_operation_id. | Acquire before approving execution or mutating that user. For multi-user batch, acquire in deterministic user sort order. | Release after forward verification, rollback verification, cancellation, or failed-closed terminal state. | Deny any competing forward movement or rollback with unknown scope. |
| TARGET_LOCK | One target egress and its mutable target metadata. | batch_id, scheduler_job_id, or maintenance_operation_id. | Acquire before target metadata mutation, capacity requalification, or target isolation change. | Release after metadata commit or failed validation rollback. | Deny target admission if lock holder is unknown or conflicting. |
| BATCH_LOCK | One execution batch. | operator_session_id or scheduler_job_id. | Acquire before status transition, packet creation, execution, observation close, rollback, or cancellation. | Release after state transition is durably recorded. | Deny double execution and require state reload. |
| PACKET_LOCK | One approval packet. | batch_id. | Acquire before packet refresh, consumption, replay validation, cancellation, or expiry handling. | Release after packet state is durably recorded. | Deny execution if packet state cannot be proven unique and non-replayed. |
| AUDIT_LOCK | One audit lineage stream, if the audit backend lacks atomic append. | audit_writer_id. | Acquire before writing ordered lineage events. Not required if append-only store provides atomic sequence numbers. | Release after event hash and sequence are persisted. | Deny certification if audit order cannot be proven. |

## Acquisition Ordering

The base lock order is:

```text
BATCH_LOCK
PACKET_LOCK
USER_LOCKS(sorted by user IP/table)
TARGET_LOCK
AUDIT_LOCK
```

Capacity reservations are acquired after precheck and before packet approval; execution-time locks must verify reservation freshness.

## Lock Timeout

Every lock must include:

- lock_id;
- owner_id;
- resource_id;
- acquired_at;
- expires_at;
- fencing_token;
- purpose;
- batch_id where applicable.

Expired locks are not automatically ignored for forward movement. The recovery path must prove the prior owner cannot still commit a conflicting state transition.

## Decision

The lock model is owner-scoped, ordered, fenced, TTL-bound, and fail-closed.
