# E32.2.3 Final Lifecycle Decision

batch_lifecycle_defined=true

## Final Lifecycle

Primary proof-style lifecycle:

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

Failure lifecycle:

```text
any_pre_execution_state -> FAILED_CLOSED
any_pre_execution_state -> EXPIRED
any_pre_execution_state -> CANCELLED
terminal_replay_attempt -> REPLAY_DENIED
```

Containment lifecycle:

```text
EXECUTING_or_OBSERVING_failure
  -> ROLLBACK_READY
  -> ROLLING_BACK
  -> COMPLETED_or_FAILED_CLOSED
```

## Lifecycle Principles

- Batch status does not authorize execution by itself.
- Approval does not allow mutation until execution-time recheck passes.
- Terminal states cannot resume execution.
- Expired batches require fresh generation or fresh packet.
- Partial forward failure defaults to rollback/containment.
- Replay attempts are denied and audited.

## Architecture Decisions Required

```text
ARCHITECTURE_DECISION_REQUIRED:
- retained_production_pool_completion_semantics
- exact_status_transition_table_schema
- reservation_release_timing_for_concurrent_batches
- partial_forward_failure_policy
```

Recommended:

- keep proof-style batches on default rollback until production-pool retention is certified;
- encode transitions as an explicit allowlist table;
- release reservations only at terminal state after audit closure;
- require immediate rollback/containment on partial forward failure until partial-completion semantics are certified.

## Remaining Open Questions

- whether `OBSERVING -> COMPLETED` without rollback is allowed for first production-pool retained movement;
- exact scheduler interaction with `SCHEDULED`;
- whether cancellation after `EXECUTING` should become containment rather than cancellation;
- exact representation of replay attempts as child audit events.

## Decision

Batch lifecycle is defined and compatible with E32.2.1, E32.2.2, and the certified Capacity Program.

recommended_next_block=E32_2_4_BATCH_VALIDATION_METHODOLOGY

