# E32.2.B Batch Failure Modes

batch_failure_modes_defined=true

## Failure Mode Inventory

### BATCH_STALE

Detection:

- stale batch metadata;
- stale runtime snapshot;
- stale capacity evidence.

Runtime impact:

```text
forward_allowed=false
```

Operator action:

Refresh precheck and packet.

Fail-closed behavior:

Do not execute stale batch.

### BATCH_EXPIRED

Detection:

- `now > expires_at`;
- approval packet expired.

Runtime impact:

```text
forward_allowed=false
```

Operator action:

Create fresh batch or packet.

Fail-closed behavior:

Terminal `EXPIRED`.

### BATCH_REPLAY_ATTEMPT

Detection:

- packet already has consumed forward record;
- batch generation reused after terminal event.

Runtime impact:

```text
forward_allowed=false
routing_mutation_allowed=false
```

Operator action:

Verify no movement and preserve denial audit.

Fail-closed behavior:

Terminal `REPLAY_DENIED`.

### BATCH_RUNTIME_DRIFT

Detection:

- users registry hash mismatch;
- egress registry hash mismatch;
- selected moves appeared;
- hidden movers present;
- user no longer on expected source target.

Runtime impact:

```text
forward_allowed=false
```

Operator action:

Classify drift and create fresh packet if safe.

Fail-closed behavior:

No mutation until drift is explained.

### BATCH_CAPACITY_CONFLICT

Detection:

- movement budget exceeds effective cap;
- movement budget exceeds available capacity;
- target no longer `CERTIFIED`;
- reservation conflict.

Runtime impact:

```text
forward_allowed=false
scheduler_admission=false
```

Operator action:

Reduce batch, recertify capacity, or resolve reservation conflict.

Fail-closed behavior:

No forward movement.

### BATCH_PARTIAL_FORWARD

Detection:

- some but not all approved users moved;
- command sequence stopped mid-batch;
- forward verification mismatch.

Runtime impact:

```text
new_forward_allowed=false
rollback_or_containment_required=true
```

Operator action:

Run exact rollback/containment for affected users.

Fail-closed behavior:

Transition to `ROLLBACK_READY` if scope known, otherwise `FAILED_CLOSED` plus human review.

### BATCH_PARTIAL_ROLLBACK

Detection:

- some but not all affected users returned;
- route tables not fully restored;
- target users count not restored.

Runtime impact:

```text
forward_allowed=false
containment_allowed=true_if_scope_known
```

Operator action:

Contain remaining affected users and escalate.

Fail-closed behavior:

`FAILED_CLOSED` until resolved.

### BATCH_AUDIT_INCONSISTENCY

Detection:

- missing forward event;
- missing rollback event;
- packet/audit mismatch;
- lineage conflict.

Runtime impact:

```text
forward_allowed=false
replay_allowed=false
```

Operator action:

Human review and audit reconstruction.

Fail-closed behavior:

No new execution using conflicting lineage.

### BATCH_ROLLBACK_SCOPE_UNKNOWN

Detection:

- affected user set unknown;
- rollback targets missing;
- route tables unknown after partial mutation.

Runtime impact:

```text
forward_allowed=false
rollback_allowed=false_until_scope_known
containment_requires_human_review=true
```

Operator action:

Stop, reconstruct state, and create containment plan.

Fail-closed behavior:

No automated rollback.

## Failure Modes Verdict

Batch failure modes are defined and fail closed.
