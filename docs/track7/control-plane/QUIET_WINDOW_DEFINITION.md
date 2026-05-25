# Quiet Window Definition

A quiet window is a bounded interval where the V7 control plane is stable enough that a one-user canary can be attributed to the operator's approved action, not to background automation.

## Required Truths

- No `v7-users-autoswitch --apply` can run.
- No active autoswitch process is running.
- No admin autoswitch apply is being executed.
- No admin manual user switch is being executed except the approved canary action.
- No `v7-routing-sync` is running.
- No policy apply, Direct/RU mutation, proxy apply, kill-switch rebuild, Trusted RU refresh, or rollback operation is running.
- Registry snapshots are stable before canary.
- Route and ip rule snapshots are stable before canary.
- Candidate user penalty state is known.
- Target egress readiness is known.
- Reconcile truth status is known or explicitly waived.

## Minimum Duration

Minimum quiet observation before canary:

```text
2 autoswitch timer periods plus 10 seconds
```

Given a 20s timer, the practical minimum is 50 seconds. A safer operator window is 60-90 seconds.

## Required Observations

Before opening the canary window:

- capture timer/service state;
- capture `users.registry` hash;
- capture `ip -4 rule show`;
- capture candidate route table;
- run read-only route/killswitch/provisioning checks;
- confirm no switch-history entry appears during the quiet interval;
- confirm autoswitch safety state is not changing.

## Acceptable Drift

Allowed:

- read-only check timestamps;
- passive health metric refreshes that do not write canary-critical state;
- operator UI reads.

Not allowed:

- registry assignment changes;
- candidate route table changes;
- ip rule changes;
- autoswitch safety penalty churn;
- reconnect/load summary writes from autoswitch planner;
- switch-history/audit movement events.

## Current Status

```text
quiet_window_status=unstable
```

Reason: autoswitch authority is active and the control plane has recently changed user assignments.
