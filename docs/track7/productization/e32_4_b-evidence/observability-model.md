# E32.4.B Observability Model

concurrency_observability_defined=true

## Operator View

Operators must be able to inspect concurrency state without mutating runtime.

The observability model must show:

- active locks;
- lock owner;
- reservation owner;
- lock age;
- reservation age;
- stale status;
- blocked batch;
- blocked user;
- blocked target;
- blocked packet;
- next safe action;
- audit lineage for lock/reservation decisions.

## Lock Visibility

Each lock should display:

```text
lock_id
lock_type
resource_id
owner_id
batch_id
purpose
acquired_at
expires_at
age
stale_status
fencing_token
blocking_effect
next_safe_action
```

## Reservation Visibility

Each reservation should display:

```text
reservation_id
reservation_type
owner_id
batch_id
target_id
reserved_capacity
allowed_users
created_at
expires_at
status
conflict_status
release_reason
next_safe_action
```

## Blocked Resource Views

Operators must be able to answer:

- which batch is blocked;
- which user is blocked;
- which target is blocked;
- which reservation conflicts;
- whether rollback remains allowed;
- whether human review is required;
- whether stale-lock recovery is safe.

## Status Semantics

| Status | Meaning | Operator Action |
| --- | --- | --- |
| ACTIVE | Lock or reservation is valid and owner heartbeat is current. | Inspect or wait. |
| BLOCKING | Resource blocks another batch or scheduler job. | Inspect owner and conflict. |
| STALE | TTL expired or heartbeat missing. | Run stale recovery review; no forward movement. |
| CONFLICTED | Two claims overlap unsafely. | Deny forward movement; resolve conflict. |
| RELEASED | Resource is no longer active. | Audit only. |
| EXPIRED | Reservation or lock expired. | Refresh packet/reservation or cancel batch. |

## Decision

concurrency_observability_defined=true
