# E32.2.2 Status And Freshness Model

status_freshness_model_defined=true

## Batch Status States

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

## State Semantics

| Status | Meaning | Forward Allowed | Rollback Allowed |
| --- | --- | --- | --- |
| `DRAFT` | Batch is being modeled. | No | No |
| `PRECHECKED` | Static/runtime read-only precheck passed. | No | No |
| `APPROVED` | Approval packet exists. | Not yet; recheck required | If rollback batch approved |
| `SCHEDULED` | Scheduler has planned execution window. | Only after recheck | If rollback scope exists |
| `EXECUTING` | Forward execution in progress. | Current operation only | Containment if failure |
| `OBSERVING` | Forward completed; observation active. | No new forward | Default rollback may be allowed |
| `ROLLBACK_READY` | Rollback manifest is ready. | No | Yes |
| `ROLLING_BACK` | Rollback executing. | No | Current rollback only |
| `COMPLETED` | Batch closed successfully. | No | No, unless new containment batch |
| `FAILED_CLOSED` | Batch denied or failed safely. | No | Containment only |
| `REPLAY_DENIED` | Replay attempt denied. | No | No |
| `CANCELLED` | Operator/system cancelled before execution. | No | No |
| `EXPIRED` | Execution window expired. | No | Containment only if needed |

## Required Timestamps

```text
created_at
expires_at
approved_at
execution_started_at
completed_at
stale_after
```

## Freshness Rules

### created_at

Immutable batch creation timestamp.

### expires_at

Hard execution deadline. Forward execution is denied after expiration.

### approved_at

Set when approval packet is created and accepted.

### execution_started_at

Set on first forward mutation command or transaction start.

### completed_at

Set only after forward, observation, rollback if required, replay validation, and closure checks.

### stale_after

Optional metadata warning threshold before hard expiration.

Recommended default:

```text
stale_after <= expires_at
```

## Expiration Behavior

If a batch expires before forward execution:

```text
forward_allowed=false
fresh_packet_required=true
```

If a batch expires during rollback/containment:

```text
rollback_containment_allowed=true_if_exact_scope_known
```

## Status Verdict

Status and freshness model is defined and fail-closed.

