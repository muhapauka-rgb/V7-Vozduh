# E32.4.B Owner Transfer Model

owner_transfer_model_defined=true

## Purpose

Owner transfer allows a batch to move safely between operator, scheduler, executor, and rollback controller without allowing implicit takeover.

## Allowed Transfers

| Transfer | When Allowed | Required Proof |
| --- | --- | --- |
| operator -> scheduler | Batch is scheduled after approval and reservation acquisition. | batch_id, packet_id, reservation_id, policy decision, capacity evidence, audit event. |
| scheduler -> execution | Execution-time recheck passes and scheduler starts execution. | fresh runtime snapshot, non-expired packet, valid locks, valid reservations. |
| execution -> rollback | Forward verification fails or containment requires rollback. | moved user set, rollback manifest, forward audit record, containment reason. |
| operator -> rollback | Operator starts explicit rollback for exact known scope. | rollback manifest, current user state, USER_LOCKS, audit record. |
| scheduler -> operator | Scheduled execution is cancelled or requires manual review. | cancellation reason, released reservations, packet state update. |

## Forbidden Transfers

Ownership may not transfer to:

- Policy Engine;
- autoswitch;
- rebalance;
- unknown actor;
- actor without fresh fencing token;
- actor without audit event.

## Transfer Requirements

Each transfer must record:

```text
object_id
object_type
previous_owner
next_owner
previous_fencing_token
next_fencing_token
transfer_reason
runtime_snapshot_hash
packet_state
reservation_state
created_at
audit_event_hash
```

## Safe Transfer Rules

- Transfer must be atomic relative to BATCH_LOCK.
- Transfer must not change allowed users, allowed target, rollback target, or blast radius.
- Transfer must not bypass execution-time recheck.
- Transfer must release no lock unless the next owner already has a valid fencing token or the batch is terminal.
- Failed transfer leaves batch in fail-closed state for forward movement.

## Decision

owner_transfer_model_defined=true
