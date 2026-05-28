# Full Autoswitch Hold Model

Block: E8.3.

Mode: approval packet only.

No hold was executed.

## Purpose

Block E8 proved that stopping only `v7-users-autoswitch.timer` and
`v7-users-autoswitch.service` does not create a quiet control-plane. Block E8.1
identified the remaining authority as `v7-health.service`.

This document defines the full authority model required before another
quiet-window rehearsal can be approved.

## Current Autoswitch Authorities

### Apply authority

```text
v7-users-autoswitch.timer
  -> v7-users-autoswitch.service
    -> /usr/local/bin/v7-users-autoswitch --apply
```

Effect:

```text
can move users through v7-user-switch
can alter users.registry and per-user routing state through switch path
can invalidate any one-user canary attribution
```

### Planner/state authority

```text
v7-health.service
  -> /bin/bash -c 'while true; do ... v7-users-autoswitch; sleep 30; done'
```

Observed facts from E8.1:

```text
UnitFileState=enabled
Restart=always
MainPID=2938206
ControlGroup=/system.slice/v7-health.service
ExecStart includes v7-users-autoswitch every 30 seconds
```

Effect:

```text
does not call --apply
does not directly move users through apply mode
can still write planner/load/reconnect state
can make reconcile/routing observations race-prone
prevents strict quiet-window attribution
```

### Admin/operator authority

Static repo evidence shows admin/manual paths can invoke:

```text
v7-users-autoswitch --pretty
v7-users-autoswitch --mode guarded --apply --pretty
v7-user-switch
v7-routing-sync
```

Effect:

```text
manual or admin action can invalidate rehearsal evidence
```

### Sentinel-capable authority

Current systemd unit uses `--no-autoswitch`, so the active unit is not a current
autoswitch launcher. The code path remains capable if invoked without
`--no-autoswitch`.

Effect:

```text
must be verified not running without --no-autoswitch before any quiet window
```

## Full Hold Definition

A full autoswitch hold means all autoswitch/user-movement authorities are unable
to run for the approved observation window:

```text
v7-users-autoswitch.timer inactive
v7-users-autoswitch.service inactive
v7-health.service held or its autoswitch planner isolated
no v7-users-autoswitch process
no v7-user-switch process
no v7-routing-sync process
no admin autoswitch/user-switch action
no manual shell invocation
no sentinel invocation without --no-autoswitch
no policy/proxy/Direct/RU/Trusted RU apply
```

This does not approve canary, user-switch, routing-sync, policy apply, proxy
apply, Direct/RU mutation, Trusted RU refresh, or kill-switch mutation.

## Option A - Bounded Temporary Hold

Option A is a short, explicitly approved operational rehearsal that temporarily
holds both the apply authority and `v7-health.service`.

Future approved hold sequence:

```bash
systemctl stop v7-users-autoswitch.timer
systemctl stop v7-users-autoswitch.service
systemctl stop v7-health.service
```

Future approved restore sequence:

```bash
systemctl start v7-health.service
systemctl start v7-users-autoswitch.timer
```

Required immediate verification after hold:

```bash
systemctl is-active v7-users-autoswitch.timer || true
systemctl is-active v7-users-autoswitch.service || true
systemctl is-active v7-health.service || true
pgrep -a -f 'v7-users-autoswitch|v7-user-switch|v7-routing-sync|v7-health' || true
sha256sum /opt/v7/egress/state/users.registry 2>/dev/null || true
ip -4 rule show
ip -4 route show table all
```

Expected duration:

```text
2 to 5 minutes maximum
```

What pauses during the hold:

```text
v7-egress-history
v7-egress-stability
v7-egress-load
v7-egress-diagnose
v7-state-merge
v7-user-desired-state-save
v7-state-json-save
v7-users-autoswitch planner invocation
```

Short-hold safety assumption:

```text
datapath should continue using already-applied routes/rules/interfaces
users should not be moved
health summaries may become stale for the hold duration
autoswitch decisions should be suspended rather than applied
```

Risks:

```text
health summaries stale for 2 to 5 minutes
load/reconnect planner state paused
restore may interact with v7-routing-sync.service because v7-health.service has Wants/After relationship
operator must prove no routing-sync starts during restore
manual/admin paths remain a human-process risk
```

Option A GO conditions:

```text
operator explicitly approves holding v7-health.service
pre-hold evidence is captured
active process list contains no v7-user-switch or v7-routing-sync
admin/operator freeze is active
restore plan is accepted including v7-health.service
abort conditions are understood
```

Option A NO-GO conditions:

```text
v7-routing-sync active before hold
v7-user-switch active before hold
operator cannot approve v7-health.service hold
restore of v7-health.service could trigger unapproved routing-sync
kill switch/user-route/provisioning checks fail before hold
manual/admin freeze cannot be guaranteed
```

## Option B - Split Health And Autoswitch Planner First

Option B is a design/deploy path before any new quiet-window rehearsal. It
separates health observation from autoswitch planning.

Target model:

```text
v7-health.service
  -> health/history/stability/load/state merge only

v7-autoswitch-planner.service/timer
  -> v7-users-autoswitch without --apply, if still needed

v7-users-autoswitch.timer/service
  -> v7-users-autoswitch --apply
```

Required design constraints:

```text
health-only service must not call v7-users-autoswitch
planner service must be independently holdable
apply timer must remain independently holdable
admin/manual authority must remain governed by approval
restore must not start routing-sync unless explicitly approved
```

Advantages:

```text
clean authority boundary
quiet-window can hold planner/apply without stopping unrelated health updates
future rehearsal evidence becomes easier to attribute
restore is less entangled with health state
```

Risks:

```text
requires runtime design, deploy, and verification
not read-only
must be separately approved
can introduce unit ordering mistakes if rushed
```

Option B GO conditions:

```text
repo design reviewed
unit split reviewed
rollback for unit split documented
deployment approval granted separately
post-deploy authority map revalidated
```

Option B NO-GO conditions:

```text
need immediate reconcile-under-quiet evidence
no deploy/change approval exists
unit split cannot be tested safely
operator cannot tolerate deployment risk
```

## Recommendation

Preferred governance path:

```text
Option B for durable platform design
Option A only if the operator needs immediate quiet-window truth before refactor
```

## E8.3 Option B Draft Status

Block E8.3 prepares the durable split design:

```text
systemd/drafts/v7-health.service
systemd/drafts/v7-autoswitch-planner.service
systemd/drafts/v7-autoswitch-planner.timer
```

If deployed in a separately approved future block, the full hold model changes:

```text
v7-health.service remains active
v7-autoswitch-planner.timer/service held for quiet-window
v7-users-autoswitch.timer/service held for quiet-window
admin/manual/sentinel-capable paths frozen
```

This means the future quiet-window no longer needs to stop broad health summary
work. It still must hold both autoswitch planner and autoswitch apply authority.

Post-split full hold requirement:

```text
v7-autoswitch-planner.timer inactive
v7-autoswitch-planner.service inactive
v7-users-autoswitch.timer inactive
v7-users-autoswitch.service inactive
v7-health.service active and health-only
no v7-users-autoswitch process
no v7-user-switch process
no v7-routing-sync process
no admin/manual autoswitch or user movement
```

E8.3 execution status:

```text
current_canary_status=NO-GO
quiet_window_verified=false
execution_allowed_now=False
runtime_mutation_performed=NO
split_design_ready_for_deploy_approval=true
split_deployed=false
```

## E8.4 Deployed Split Status

Block E8.4 deployed the split.

Current authority model:

```text
v7-health.service
  -> health/history/load/state/json save only
  -> no v7-users-autoswitch

v7-autoswitch-planner.timer/service
  -> v7-users-autoswitch without --apply

v7-users-autoswitch.timer/service
  -> v7-users-autoswitch --apply
```

Post-split quiet-window hold should hold:

```text
v7-autoswitch-planner.timer
v7-autoswitch-planner.service
v7-users-autoswitch.timer
v7-users-autoswitch.service
```

It should not need to stop:

```text
v7-health.service
```

Current status:

```text
split_deployed=true
post_split_authority_mapping_done=true
quiet_window_verified=false
current_canary_status=NO-GO
execution_allowed_now=False
```

## E8.5 Post-Split Rehearsal Result

Block E8.5 executed the post-split hold model.

Held authorities:

```text
v7-autoswitch-planner.timer
v7-autoswitch-planner.service
v7-users-autoswitch.timer
v7-users-autoswitch.service
```

Not held:

```text
v7-health.service
```

Observed result:

```text
v7-health.service stayed active=true
autoswitch_planner_held=true
autoswitch_apply_held=true
autoswitch_fully_quiet=true
users.registry_changed=false
egress.registry_changed=false
user_movement_observed=false
routing_drift_observed=false
quiet_window_verified=true
reconcile_under_quiet=STABLE_FAIL
restore_success=true
```

Updated hold model:

```text
After the E8.4 split, full autoswitch hold no longer requires stopping v7-health.service.
Full hold requires holding both planner and apply authority while health remains active.
```

The verified post-split hold is sufficient for future quiet-window attribution. It is not a canary approval and does not by itself allow `v7-user-switch`.

### Option C - Policy-level autoswitch disable

Potentially set:

```text
autoswitch_enabled=false
```

This was not executed in E8.1.

Advantages:

- may avoid stopping services.

Risks:

- writes runtime config/policy;
- health loop may continue planner writes;
- not sufficient for full quiet-window if state churn must stop;
- restore requires exact previous policy value.

Verdict:

```text
not enough for quiet-window by itself
```

### Option D - Process kill

Forbidden in E8.1 and not recommended as governance-safe hold.

Reason:

```text
v7-health.service Restart=always can resurrect the process
kill does not express intended service state
restore semantics are weaker than systemd hold
```

Verdict:

```text
forbidden and not a clean hold model
```

## Restore Requirements

A future restore model must restore exactly the authorities held.

If only autoswitch timer/service are held:

```text
restore v7-users-autoswitch.timer
verify active/enabled/waiting
verify no unexpected service failure
```

If `v7-health.service` is also held:

```text
restore v7-health.service
verify ActiveState=active
verify MainPID exists
verify command line matches expected health loop
verify no immediate crash/restart loop
verify v7-users-autoswitch.timer restored if it was active before
verify no unexpected v7-routing-sync execution
```

Important:

```text
restore is not safe if it silently starts routing-sync or broad apply tooling
```

## Race Conditions

Known races:

- `v7-users-autoswitch.timer` can fire every 20 seconds.
- `v7-health.service` loop can run every 30 seconds.
- Admin API can invoke autoswitch/user-switch manually.
- Telegram sentinel code can invoke autoswitch if run without `--no-autoswitch`.
- `v7-health.service` restart policy can recreate the health loop.
- Starting/stopping services can change process state between snapshots.
- Planner writes can occur without user movement and still invalidate quiet-window attribution.

## Quiet-Window Feasibility

Quiet-window is theoretically achievable only if all autoswitch authorities are held:

```text
systemd apply timer/service
health-loop planner authority
admin/operator launch paths
sentinel alternate invocation paths
manual shell launch paths
```

Current execution permission:

```text
execution_allowed_now=False
```

Current canary status:

```text
CONDITIONAL
```

`CONDITIONAL` means the quiet-window blocker is resolved, but canary execution
remains blocked until reconcile `STABLE_FAIL` is classified or waived and a fresh
one-user approval packet exists.

## Future Minimal Rehearsal Preconditions

Before a second quiet-window rehearsal:

1. Explicit approval must include `v7-health.service` hold or an equivalent no-write autoswitch planner isolation.
2. Pre-hold evidence must capture `v7-health.service` state, `MainPID`, command line, and cgroup.
3. Restore packet must define whether `v7-health.service` is restarted and how to detect unintended `v7-routing-sync`.
4. Admin/operator freeze must be active.
5. Sentinel must be verified with `--no-autoswitch`.
6. Mutation verification must include registry hash, switch-history tail, pgrep, route/rule snapshots, kill switch, user-route-check, provisioning reconcile, and reconcile-check.

## Test + Verdict

Test:

```text
Full hold model checked against E8.1 authority evidence.
```

Verdict:

```text
CONDITIONAL
full hold is realistic only with explicit v7-health.service authority handling
canary remains NO-GO
```

## Runtime Mutation Statement

```text
Runtime mutation performed: NO
Hold executed: NO
Restore executed: NO
Autoswitch apply performed: NO
User movement performed: NO
Routing mutation performed: NO
```

E8.5 runtime mutation statement:

```text
Runtime mutation performed: YES - limited to temporary autoswitch planner/apply hold and restore only
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```
