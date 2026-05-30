# E32.2.C Fail-Closed Review

fail_closed_behavior_valid=true

## Review Scope

This review verifies:

- all failure modes;
- all denial paths;
- rollback exceptions;
- containment rules.

## Batch Failure Modes

Defined failure modes:

- `BATCH_STALE`
- `BATCH_EXPIRED`
- `BATCH_REPLAY_ATTEMPT`
- `BATCH_RUNTIME_DRIFT`
- `BATCH_CAPACITY_CONFLICT`
- `BATCH_PARTIAL_FORWARD`
- `BATCH_PARTIAL_ROLLBACK`
- `BATCH_AUDIT_INCONSISTENCY`
- `BATCH_ROLLBACK_SCOPE_UNKNOWN`

## Forward Denial

Every batch failure mode denies forward movement:

```text
forward_allowed=false_for_all_batch_failure_modes
```

## Denial Paths

Forward execution is denied on:

- invalid metadata;
- incomplete rollback manifest;
- missing approval packet;
- expired packet;
- failed execution-time recheck;
- capacity conflict;
- runtime drift;
- selected moves nonzero;
- hidden movers present;
- audit lineage conflict;
- replay attempt.

## Rollback Exceptions

Rollback may proceed only when:

```text
exact_scope_known=true
rollback_target_known=true
blast_radius_expansion=false
```

Rollback is denied when rollback scope is unknown.

## Containment Rules

Containment is allowed only when:

- it reduces or does not expand risk;
- exact affected user set is known or human-approved reconstruction exists;
- audit lineage is preserved;
- no unrelated user is touched.

## Human Review

Human review is required when:

- audit lineage conflicts;
- rollback scope is unknown;
- partial rollback remains unresolved;
- replay movement is suspected;
- runtime drift is unexplained.

## Fail-Closed Verdict

Fail-closed behavior is valid.
