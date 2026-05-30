# E32.5.A Prior Architecture Intake

prior_architecture_loaded=true

## Reviewed Architecture Layers

Scheduling Foundation reviewed the certified E32 architecture layers:

- E32.1 Capacity Program;
- E32.2 Execution Batches;
- E32.3 Policy Engine;
- E32.4 Concurrency Controls.

## Extracted Batch Lifecycle Inputs

Execution Batches define the action object and lifecycle.

Relevant states:

```text
DRAFT
PRECHECKED
APPROVED
SCHEDULED
EXECUTING
OBSERVING
ROLLBACK_READY
ROLLING_BACK
COMPLETED
FAILED_CLOSED
REPLAY_DENIED
CANCELLED
EXPIRED
```

Scheduler may affect queue and scheduling state, but it cannot bypass batch lifecycle gates or execute runtime mutation by itself.

## Extracted Capacity Inputs

Capacity Program provides:

- target capacity class;
- certified capacity;
- hard_limit;
- active_policy_cap;
- effective_batch_cap;
- capacity status;
- capacity freshness;
- capacity failure modes.

Scheduler must not dispatch a batch if capacity is stale, degraded, expired, revoked, insufficient, or reservation-conflicted.

## Extracted Policy Inputs

Policy Engine provides admission logic.

Certified policy boundary:

```text
policy_is_authority=false
policy_is_runtime_mutation=false
policy_is_admission_logic=true
```

Scheduler must not convert policy REVIEW_REQUIRED or DENY into executable state.

## Extracted Concurrency Inputs

Concurrency Controls provide:

- USER_LOCK;
- TARGET_LOCK;
- BATCH_LOCK;
- PACKET_LOCK;
- AUDIT_LOCK;
- CAPACITY_RESERVATION;
- TARGET_RESERVATION;
- BATCH_RESERVATION;
- owner transfer;
- stale lock recovery;
- race and deadlock prevention.

Scheduler must obey lock ordering and reservation ownership.

## Extracted Failure Modes

Scheduling must fail closed when it sees:

- missing or stale capacity;
- policy denial;
- packet expiry;
- dependency failure;
- lock conflict;
- reservation conflict;
- stale owner heartbeat;
- audit lineage ambiguity;
- schedule expiry.

## Intake Decision

prior_architecture_loaded=true
