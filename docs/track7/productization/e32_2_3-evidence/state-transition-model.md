# E32.2.3 State Transition Model

state_transition_model_defined=true

## Happy Path

Primary forward execution lifecycle:

```text
DRAFT
  -> PRECHECKED
  -> APPROVED
  -> SCHEDULED
  -> EXECUTING
  -> OBSERVING
  -> ROLLBACK_READY
  -> ROLLING_BACK
  -> COMPLETED
```

For forward batches that intentionally remain deployed instead of rolling back, the future production-pool lifecycle may allow:

```text
OBSERVING -> COMPLETED
```

This branch is not certified for the current proof-style movement blocks unless a later block defines production-pool retention semantics.

## Failure Paths

### Pre-Approval Failure

```text
DRAFT -> FAILED_CLOSED
PRECHECKED -> FAILED_CLOSED
```

Triggers:

- invalid metadata;
- incomplete rollback manifest;
- missing capacity requirements;
- invalid user or target scope.

### Approval Failure

```text
PRECHECKED -> FAILED_CLOSED
APPROVED -> FAILED_CLOSED
```

Triggers:

- approval packet missing;
- approval packet invalid;
- stale registry or capacity hashes;
- operator confirmation missing.

### Expiration

```text
DRAFT -> EXPIRED
PRECHECKED -> EXPIRED
APPROVED -> EXPIRED
SCHEDULED -> EXPIRED
```

Forward execution is denied after expiration.

### Execution Failure

```text
SCHEDULED -> FAILED_CLOSED
EXECUTING -> ROLLBACK_READY
EXECUTING -> FAILED_CLOSED
```

If forward mutation started and exact rollback scope is known, transition to `ROLLBACK_READY`.

If no mutation occurred and authorization failed, transition to `FAILED_CLOSED`.

### Observation Failure

```text
OBSERVING -> ROLLBACK_READY
OBSERVING -> FAILED_CLOSED
```

Observation failure with users on target requires rollback readiness if rollback scope is exact.

### Rollback Failure

```text
ROLLING_BACK -> FAILED_CLOSED
```

Rollback failure must preserve evidence and trigger containment/escalation.

### Replay

Replay attempt after a consumed packet:

```text
COMPLETED -> REPLAY_DENIED
FAILED_CLOSED -> REPLAY_DENIED
EXPIRED -> REPLAY_DENIED
```

Replay denial is a terminal audit event for the replay attempt, not a resumption of the original batch.

### Cancellation

Before forward execution:

```text
DRAFT -> CANCELLED
PRECHECKED -> CANCELLED
APPROVED -> CANCELLED
SCHEDULED -> CANCELLED
```

Cancellation after forward execution is not allowed; rollback or containment is required.

## Disallowed Transitions

The lifecycle forbids:

- `COMPLETED -> EXECUTING`
- `EXPIRED -> EXECUTING`
- `FAILED_CLOSED -> EXECUTING`
- `CANCELLED -> EXECUTING`
- `REPLAY_DENIED -> EXECUTING`
- any transition that changes approved user set without a new batch generation.

## Transition Verdict

State transition model is defined and fail-closed.

