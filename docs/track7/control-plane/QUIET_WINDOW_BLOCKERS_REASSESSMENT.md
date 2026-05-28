# Quiet Window Blockers Reassessment

Block: E8.1.

Mode: read-only reassessment.

## Current Status

```text
current_canary_status=NO-GO
current_quiet_window_status=unstable
quiet_window_verified=false
execution_allowed_now=False
```

Block E8 conclusion remains valid:

```text
quiet-window was not achieved
reconcile under quiet was not sampled
canary remains NO-GO
```

Block E8.1 adds the exact reason:

```text
v7-health.service contains an autoswitch planner loop
```

## Updated Blocker List

### Blocker 1 - `v7-health.service` autoswitch loop

Evidence:

```text
v7-health.service
Type=simple
Restart=always
MainPID=2938206
ExecStart=/bin/bash -c 'while true; do ... v7-users-autoswitch; sleep 30; done'
```

Impact:

```text
stopping v7-users-autoswitch.timer/service alone cannot quiet the control plane
```

Status:

```text
HARD BLOCKER
```

### Blocker 2 - `v7-users-autoswitch.timer` apply authority

Evidence:

```text
v7-users-autoswitch.timer active/enabled
OnUnitActiveSec=20s
v7-users-autoswitch.service ExecStart=/usr/local/bin/v7-users-autoswitch --apply
```

Impact:

```text
direct apply authority can move users every 20 seconds
```

Status:

```text
HARD BLOCKER until held in an approved rehearsal
```

### Blocker 3 - Planner writes without `--apply`

Repo-side source evidence:

```text
plan() calls _persist_dynamic_load_summary()
_observe_reconnect_events() can write reconnect state
```

Impact:

```text
even dry-run/planner invocation can churn state
```

Status:

```text
HARD BLOCKER for strict quiet-window attribution
```

### Blocker 4 - Admin/operator authority

Evidence:

```text
/api/actions/autoswitch-dry-run
/api/actions/autoswitch-apply-guarded
manual v7-users-autoswitch
manual v7-user-switch
manual v7-routing-sync
```

Impact:

```text
human/admin action can invalidate quiet-window/canary attribution
```

Status:

```text
requires operator freeze
```

### Blocker 5 - Restore ambiguity if `v7-health.service` is held

Evidence:

```text
v7-health.service Wants=v7-routing-sync.service
v7-health.service After=v7-routing-sync.service
```

Impact:

```text
future health-service stop/start must prove it does not unexpectedly perform routing mutation
```

Status:

```text
RESTORE MODEL BLOCKER
```

## Reconcile Under Quiet

Current status:

```text
reconcile_under_quiet=NOT_SAMPLED_ABORTED
```

Can reconcile-under-quiet be attempted now?

```text
NO
```

Reason:

```text
the authority map is now clearer, but a full hold has not been approved or executed
```

When can it be attempted?

```text
only after a second rehearsal approval explicitly covers v7-health.service autoswitch loop handling
```

## Quiet Window Feasibility

The quiet window is now more realistic because the unknown authority is identified.

However, it is not currently executable because the required hold is broader than Block E8 permissions.

Current feasibility:

```text
theoretically achievable=YES
operationally approved now=NO
governance status=CONDITIONAL
```

## Canary Status

Updated canary status:

```text
NO-GO
```

Reason:

```text
quiet-window has not succeeded
reconcile-under-quiet has not been sampled
autoswitch planner/apply authorities are not yet held
```

## Updated Execution Status

```text
execution_allowed_now=False
```

Allowed:

```text
read-only inspection
repo-side docs
static analysis
governance checker/tests
```

Forbidden:

```text
canary
user-switch
routing-sync
autoswitch apply
policy apply
Trusted RU refresh
Direct/RU mutation
proxy apply
kill switch mutation
systemctl stop/start/restart without separate approval
```

## Phase Tests And Verdicts

### Process Consistency Check

Evidence:

```text
PID 2938206 exists
cgroup=/system.slice/v7-health.service
MainPID=2938206
```

Verdict:

```text
PASS
```

### Authority Consistency Check

Evidence:

```text
v7-users-autoswitch.timer -> --apply
v7-health.service -> no-apply planner/state loop
admin API -> dry-run/apply/manual switch paths
```

Verdict:

```text
PASS
```

### Runtime Mutation Verification

Evidence:

```text
users.registry hash collected
v7-user-route-check OK
v7-killswitch-check OK
v7-provisioning-reconcile-check OK
v7-reconcile-check still inspected only
```

Verdict:

```text
PASS
read-only inspection only
```

## Final Reassessment

```text
quiet_window_verified=false
reconcile_under_quiet=NOT_SAMPLED
canary_status=NO-GO
execution_allowed_now=False
next_step=prepare separately approved E8.2 full-authority quiet-window rehearsal including v7-health.service authority
```
