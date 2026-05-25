# Control Plane Stability Signals

This model classifies whether the control plane is quiet enough for a future one-user canary.

## Stable

All are true:

- autoswitch apply authority held;
- no active autoswitch process;
- no registry assignment changes during observation;
- no route/rule snapshot changes during observation;
- no switch-history entries during observation;
- candidate user not in penalty/freeze;
- target egress health stable;
- reconcile truth clean or explicitly waived;
- kill switch/user-route/provisioning checks OK.

## Degraded

Any of these:

- target egress below quality floor but explicitly waived;
- reconcile checker reports false-positive under quiet evidence;
- stale Trusted RU state is unrelated to candidate;
- minor health metric drift without route/registry movement.

## Unstable

Any of these:

- autoswitch timer can still run `--apply`;
- autoswitch planner writes production observation state during window;
- candidate penalty state changes;
- reconnect/load summaries churn during observation;
- registry assignment changes without the approved canary action;
- route/rule snapshots change unexpectedly;
- reconcile oscillates without explanation.

## Unsafe For Canary

Any of these:

- kill switch check fails;
- user route check fails;
- provisioning reconcile fails;
- stable candidate ip rule/table missing;
- target egress disabled or missing interface;
- route leak evidence;
- autoswitch moves any user during the window;
- rollback unclear.

## Current Status

```text
control_plane_stability=unstable
quiet_window_status=unstable
```

Reason: autoswitch authority remains active and production planner paths can write observation state.
