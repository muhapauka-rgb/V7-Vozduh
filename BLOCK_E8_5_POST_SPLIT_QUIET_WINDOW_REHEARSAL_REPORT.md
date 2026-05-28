# Block E8.5 - Post-Split Quiet-Window Rehearsal Report

Date: 2026-05-25.

Mode: bounded live rehearsal.

Live mutation scope: temporary hold and restore of autoswitch planner/apply timer/service authority only.

## Executive Verdict

```text
rehearsal_executed=true
rehearsal_aborted=false
restore_success=true
v7-health_stayed_active=true
autoswitch_planner_held=true
autoswitch_apply_held=true
autoswitch_fully_quiet=true
quiet_window_verified=true
reconcile_under_quiet=STABLE_FAIL
current_canary_status=CONDITIONAL
execution_allowed_now=false
```

Block E8.5 proved that after the E8.4 health/autoswitch split, a quiet control-plane window can be created without stopping `v7-health.service`.

The quiet window was real enough for attribution:

- `v7-health.service` remained active.
- `v7-autoswitch-planner.timer/service` were held.
- `v7-users-autoswitch.timer/service` were held.
- no `v7-users-autoswitch`, `v7-user-switch`, or `v7-routing-sync` process was observed during corrected quiet samples.
- `users.registry` and `egress.registry` hashes remained stable.
- switch-history tail remained stable.
- ip rules and route tables remained stable.
- user route, kill switch, and provisioning checks remained OK.

The important negative result: `v7-reconcile-check` did not become OK under quiet conditions. It remained a stable FAIL in samples A, B, and C. This changes the interpretation from "race under active autoswitch is likely" to "stable checker semantic mismatch or stable reconcile disagreement must be classified before canary".

## Evidence Files

Evidence directory:

```text
docs/track7/control-plane/e8_5-evidence/
```

Primary evidence:

```text
pre-hold.txt
hold-confirmation-2.txt
quiet-sample-A.txt
quiet-sample-B.txt
quiet-sample-C.txt
post-restore.txt
post-restore-settled.txt
```

`hold-confirmation.txt` records an initial guard false-positive caused by process self-matching. The corrected rehearsal evidence is `hold-confirmation-2.txt` plus quiet samples A/B/C.

## Pre-Hold State

Pre-hold snapshot showed:

```text
v7-health.service=active
v7-autoswitch-planner.timer=active
v7-autoswitch-planner.service=inactive
v7-users-autoswitch.timer=active
v7-users-autoswitch.service=inactive
```

Pre-hold checks:

```text
V7_RECONCILE_RESULT=FAIL
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

Pre-hold registry hashes:

```text
users.registry=f3d22fbfbde9631345c6c07e3dc7fe7b25cad4f9e49ed4f174105bae4ae0515e
egress.registry=67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
```

The latest switch-history tail entry in pre-hold evidence was:

```text
2026-05-25T12:55:57.174223+00:00 user=10.7.0.5 from=vless to=1 reason=autoswitch_failover
```

That event predates the corrected E8.5 quiet samples and is not evidence of movement during the quiet window.

## Hold Execution

Executed hold commands:

```bash
systemctl stop v7-autoswitch-planner.timer
systemctl stop v7-autoswitch-planner.service
systemctl stop v7-users-autoswitch.timer
systemctl stop v7-users-autoswitch.service
```

No `v7-health.service` stop/restart was performed.

Corrected hold confirmation:

```text
v7-autoswitch-planner.timer=inactive
v7-autoswitch-planner.service=inactive
v7-users-autoswitch.timer=inactive
v7-users-autoswitch.service=inactive
v7-health.service=active
v7-health MainPID=2019739
```

The active health loop command remained health-only:

```text
v7-egress-history
v7-egress-stability
v7-egress-load
v7-egress-diagnose
v7-state-merge
v7-user-desired-state-save
v7-state-json-save
sleep 30
```

It did not include `v7-users-autoswitch`.

## Quiet-Window Samples

Three corrected samples were captured at quiet-window intervals:

```text
quiet-sample-A.txt
quiet-sample-B.txt
quiet-sample-C.txt
```

Across all three samples:

```text
no autoswitch/user-switch/routing-sync process observed=true
users.registry hash stable=true
egress.registry hash stable=true
switch-history stable=true
ip rules stable=true
route tables stable=true
V7_RECONCILE_RESULT=FAIL
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

Registry hashes across samples:

```text
users.registry=f3d22fbfbde9631345c6c07e3dc7fe7b25cad4f9e49ed4f174105bae4ae0515e
egress.registry=67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
```

Reconcile under quiet:

```text
sample_A=FAIL rc=1
sample_B=FAIL rc=1
sample_C=FAIL rc=1
verdict=STABLE_FAIL
```

This is not a canary GO signal. It is a better diagnostic signal: reconcile failure is stable under a verified quiet window.

## Restore

Executed restore commands:

```bash
systemctl start v7-autoswitch-planner.timer
systemctl start v7-users-autoswitch.timer
```

No manual `v7-users-autoswitch --apply` was executed.

Post-restore settled state:

```text
v7-health.service=active
v7-autoswitch-planner.timer=active
v7-autoswitch-planner.service=inactive
v7-users-autoswitch.timer=active
v7-users-autoswitch.service=inactive
```

The timers fired normally after restore and the oneshot services exited successfully. No registry hash change and no new switch-history movement were observed in the settled post-restore evidence.

Post-restore checks:

```text
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

Post-restore registry hashes:

```text
users.registry=f3d22fbfbde9631345c6c07e3dc7fe7b25cad4f9e49ed4f174105bae4ae0515e
egress.registry=67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
```

## Required Answers

```text
rehearsal_executed=true
rehearsal_aborted=false
restore_success=true
v7-health stayed active=true
autoswitch_planner_held=true
autoswitch_apply_held=true
autoswitch_fully_quiet=true
users.registry changed=false
egress.registry changed=false
user movement observed=false
routing drift observed=false
reconcile under quiet=STABLE_FAIL
kill switch OK=true
user route check OK=true
provisioning reconcile OK=true
quiet_window_verified=true
current_canary_status=CONDITIONAL
execution_allowed_now=false
```

## Current Interpretation

The E8.5 quiet window is verified. The control plane can now be made quiet post-split without stopping health.

Canary is still not directly executable because:

- autoswitch timers are restored and active outside a hold window;
- reconcile remains `STABLE_FAIL` under quiet;
- reconcile must be reclassified, fixed, or explicitly waived as a bounded false-positive before canary;
- candidate/target readiness still requires a fresh pre-canary review;
- operator approval for a one-user canary has not been granted.

## Next Recommended Step

Do not run canary yet.

Next exact step:

```text
Classify the quiet-window reconcile STABLE_FAIL as either:
1. a confirmed checker semantic false-positive with explicit one-user waiver criteria; or
2. a real stable runtime mismatch requiring non-canary repair planning.
```

After that, prepare a separate one-user canary approval packet using the verified post-split hold model.

## Mutation Statement

```text
Runtime mutation performed: YES - limited to temporary autoswitch planner/apply hold and restore only
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```
