# E32.4.A Deadlock Prevention Model

deadlock_prevention_defined=true

## Deadlock Scenarios

| Scenario | Cause | Prevention |
| --- | --- | --- |
| Two batches share users in opposite lock order | Batch A locks user X then waits for Y; Batch B locks Y then waits for X. | Sort USER_LOCK acquisition by canonical user key. |
| Target and batch lock inversion | One actor locks target then waits for batch while another locks batch then waits for target. | Enforce global lock order. |
| Packet refresh vs execution | Refresh holds packet while execution holds batch, each waits for the other. | Acquire BATCH_LOCK before PACKET_LOCK. |
| Audit writer contention | Long audit lock blocks state transition cleanup. | Prefer append-only atomic audit sequencing; keep AUDIT_LOCK last and short. |
| Stale scheduler job | Scheduler retains lock after crash or network interruption. | TTL plus fencing token plus owner heartbeat verification. |

## Global Lock Order

```text
1. BATCH_LOCK
2. PACKET_LOCK
3. USER_LOCKS(sorted by canonical user key)
4. TARGET_LOCK
5. AUDIT_LOCK
```

No actor may acquire an earlier lock after holding a later lock.

## Timeout Strategy

Locks must have short TTLs and bounded renewal.

Recommended defaults:

```text
interactive_operator_lock_ttl=5m
scheduler_precheck_lock_ttl=5m
execution_lock_ttl=10m
rollback_lock_ttl=10m
audit_lock_ttl=30s
```

Exact TTL values are architecture decisions for implementation, but all must be shorter than packet validity unless an explicit rollback containment window is active.

## Stale Lock Handling

Stale lock handling requires:

- verify owner heartbeat or terminal state;
- verify no pending audit commit from old owner;
- record stale-lock recovery event;
- issue new fencing token;
- rerun runtime and packet recheck before forward movement.

## Deadlock Recovery

If deadlock is suspected:

1. Deny new forward movement.
2. Freeze affected batch status transitions.
3. Identify lock graph and owners.
4. Release only stale locks whose owner is proven inactive.
5. Preserve rollback for exact known moved scope.
6. Require human review if lock graph cannot be proven safe.

## Decision

Deadlock prevention uses strict global lock order, sorted user locks, short TTLs, fencing tokens, and fail-closed stale lock recovery.
