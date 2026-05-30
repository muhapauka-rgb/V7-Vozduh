# E32.4.A Reservation Model

reservation_model_defined=true

## Reservation Principles

Reservations represent planned use of constrained resources. They do not execute movement and do not mutate user routing.

Reservations are required when a batch depends on capacity remaining available between approval packet generation and execution-time recheck.

## Reservation Types

| Reservation | Purpose | Owner | Lifecycle | Expiration | Release Behavior |
| --- | --- | --- | --- | --- | --- |
| CAPACITY_RESERVATION | Claim part of a target effective batch cap for one future batch. | batch_id. | Created after precheck and policy admission, refreshed at execution-time recheck, consumed or released after execution/rollback/cancel/expiry. | Short bounded TTL, no longer than packet validity. | Released on completion, rollback completion, cancellation, expiry, failed-closed denial, or explicit operator cancellation. |
| TARGET_RESERVATION | Mark a target as intended for a specific batch, maintenance, or certification action. | batch_id or operation_id. | Created before approval packet generation when target is selected. | Same or shorter than capacity reservation TTL. | Released when target is no longer needed or batch reaches terminal state. |
| BATCH_RESERVATION | Bind allowed users, target, rollback manifest, capacity claim, and packet lineage. | batch_id. | Created while batch moves from PRECHECKED to APPROVED. | Expires with packet or earlier if runtime drift invalidates it. | Released only after terminal batch state is recorded. |

## Reservation Fields

Each reservation must contain:

```text
reservation_id
reservation_type
owner_id
batch_id
target_id
allowed_users
reserved_capacity
created_at
expires_at
status
fencing_token
evidence_hash
release_reason
```

## Reservation Statuses

```text
REQUESTED
ACTIVE
CONSUMING
RELEASED
EXPIRED
FAILED_CLOSED
CONFLICTED
```

## Fail-Closed Behavior

- Missing reservation denies forward execution for scheduled or production-pool batches.
- Overlapping active reservations that exceed available capacity deny later admission.
- Unknown owner denies release by non-owner.
- Expired reservation denies forward movement and requires packet refresh or batch regeneration.

## Decision

Capacity and target reservations are mandatory for concurrent production-pool execution and optional but recommended for manually executed single-batch architecture paths.
