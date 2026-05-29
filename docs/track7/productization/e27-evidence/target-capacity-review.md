# E27 Target Capacity Review

`execution_target=amneziawg-exec-20260528-10-8-1-14`

## Current Target State

```text
target_users=0
role=EXECUTION_ONLY
soft_limit=1
hard_limit=1
manual_only=1
reserve_only=1
autoswitch_allowed=false
rebalance_allowed=false
production_assignment_allowed=false
```

Readiness helper explicit target mode:

```text
approval_status=GO
second_canary_readiness=GO
avg_mbps=27.12
min_mbps=10.67
stability=1.0
diagnose=OK
zero_user=true
```

## Capacity Analysis

The target is healthy and ready for a one-user movement, but its declared capacity is one user:

```text
soft_limit=1
hard_limit=1
```

A two-user governed movement would require capacity for two simultaneous assigned users during the forward observation window. Using this target for two users would exceed `hard_limit=1`, which would violate the execution target's own governance contract.

## Verdict

`capacity_safe_for_two_users=false`

Reason:

```text
execution_target_hard_limit=1<movement_budget=2
```

No user movement is allowed until either:

- this target is requalified with `hard_limit>=2` and sustained quality proof for two users; or
- a different execution-only target with capacity `>=2` is prepared.

