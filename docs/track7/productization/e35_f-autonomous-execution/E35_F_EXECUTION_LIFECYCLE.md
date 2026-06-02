# E35.F Execution Lifecycle

## Final Lifecycle

The final autonomous execution lifecycle is:

```text
Problem
-> Evidence Bundle
-> Proposal
-> Authority Evaluation
-> Conflict Resolution
-> Batch Candidate
-> Capacity / Policy / Concurrency Admission
-> Execution Candidate
-> Execution Contract
-> Operator Visibility Window
-> Runtime Validation
-> Execution-Time Recheck
-> Execution
-> Verification
-> Observation
-> Rollback Ready
-> Closure
```

Rollback is available from the moment an execution contract becomes executable until the closure state confirms rollback is no longer needed or the contract expires.

## Lifecycle States

| State | Meaning | Forward allowed |
|---|---|---|
| DISCOVERED | Problem detected; evidence may exist | No |
| EVIDENCED | Evidence bundle exists | No |
| PROPOSED | Proposal exists and links to evidence | No |
| EVALUATED | Authority evaluator has verdict | Only if ALLOW |
| CONFLICT_RESOLVED | Conflict resolver confirms no blocking conflict | Only if no blocking conflict |
| CANDIDATE | Candidate action is shaped but not executable | No |
| CONTRACTED | Execution contract exists | No |
| VALIDATED | Pre-execution validation passed | Not yet |
| RECHECKED | Execution-time recheck passed | Yes |
| EXECUTING | Runtime mutation in progress | Contract-limited only |
| VERIFYING | Post-action validation | No additional forward movement |
| OBSERVING | Monitoring for delayed side effects | No additional forward movement |
| ROLLBACK_READY | Rollback is possible and scoped | Rollback only unless closure permits next action |
| CLOSING | Closure/audit finalization | No |
| COMPLETED | Terminal success | No |
| FAILED_CLOSED | Terminal fail-closed | No |
| ROLLED_BACK | Terminal rollback success | No |
| CANCELLED | Terminal operator/system cancellation | No |
| EXPIRED | Terminal stale contract | No |

## Failure Paths

Any failure before execution enters `FAILED_CLOSED` or `REVIEW_REQUIRED` without runtime mutation.

Any failure after partial execution enters:

```text
ROLLBACK_READY -> ROLLING_BACK -> ROLLED_BACK
```

If rollback cannot be verified, state becomes:

```text
FAILED_CLOSED_CONTAINMENT_REQUIRED
```

and operator review is mandatory.

## Replay

An already consumed execution contract cannot return to `RECHECKED` or `EXECUTING`.

Replay attempts produce:

```text
REPLAY_DENIED
```

## Lifecycle Verdict

execution_lifecycle_defined=true
