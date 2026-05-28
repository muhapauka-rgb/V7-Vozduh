# Block E8.4 - Health / Autoswitch Planner Split Deploy Report

Mode: bounded live deploy.

Live mutation scope: approved systemd split only.

## 1. Deploy Result

```text
deploy_success=true
rollback_performed=false
```

E8.4 applied the E8.3 split design to runtime systemd units.

Runtime files changed:

```text
/etc/systemd/system/v7-health.service
/etc/systemd/system/v7-autoswitch-planner.service
/etc/systemd/system/v7-autoswitch-planner.timer
/etc/systemd/system/v7-health.service.d/10-routing-order.conf
```

Runtime files only backed up, not changed:

```text
/etc/systemd/system/v7-users-autoswitch.service
/etc/systemd/system/v7-users-autoswitch.timer
```

Backup location:

```text
/root/v7-e84-systemd-split-20260525T123450Z/backups/
```

## 2. Authority Result

```text
v7-health.service_health_only=true
planner_authority_separated=true
apply_authority_unchanged=true
```

Post-deploy authority model:

```text
v7-health.service
  -> health/history/load/state/json save only
  -> no v7-users-autoswitch

v7-autoswitch-planner.timer/service
  -> v7-users-autoswitch without --apply

v7-users-autoswitch.timer/service
  -> v7-users-autoswitch --apply
```

Evidence:

```text
docs/track7/control-plane/e8_4-evidence/post-deploy-authority.txt
docs/track7/control-plane/e8_4-evidence/post-deploy-process-guard-clean.txt
```

Clean process guard showed:

```text
no self-safe pgrep match for /usr/local/bin/v7-users-autoswitch
no self-safe pgrep match for /usr/local/bin/v7-user-switch
no self-safe pgrep match for /usr/local/bin/v7-routing-sync
old health loop with v7-users-autoswitch absent
v7-health.service MainPID runs health-only loop
```

## 3. Runtime Safety Result

```text
users.registry_changed=false
egress.registry_changed=false
user_movement_observed=false
routing_drift_observed=false
kill_switch_ok=true
user_route_check_ok=true
provisioning_reconcile_ok=true
reconcile_result_after_deploy=FAIL
```

Registry hashes:

```text
users.registry before=90afd3fb2a626726baee6d2106807f33de62240a674d0bb7a866e62e8c0a8334
users.registry after=90afd3fb2a626726baee6d2106807f33de62240a674d0bb7a866e62e8c0a8334
egress.registry before=67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
egress.registry after=67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
```

Checks:

```text
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
V7_RECONCILE_RESULT=FAIL
```

Reconcile was not fixed or forced. It remains a known blocker for canary until
sampled under a post-split quiet-window.

## 4. Rollback

```text
rollback_performed=false
```

Rollback was not triggered because:

```text
v7-health.service started successfully
v7-health.service no longer contains the autoswitch planner call
v7-autoswitch-planner.timer active/enabled
users.registry unchanged
egress.registry unchanged
kill switch OK
user route check OK
provisioning reconcile OK
no unexpected user-switch/routing-sync process observed
```

Rollback remains possible from:

```text
/root/v7-e84-systemd-split-20260525T123450Z/backups/
```

## 5. Current Governance Status

```text
current_canary_status=NO-GO
quiet_window_verified=false
execution_allowed_now=False
```

Why canary remains NO-GO:

```text
post-split quiet-window rehearsal has not run
reconcile-under-quiet has not been sampled
autoswitch planner and apply timers are active by design
one-user canary approval has not been granted
```

## 6. Exact Next Recommended Step

Next block:

```text
E8.5 post-split quiet-window rehearsal approval and execution
```

Scope should be:

```text
hold v7-autoswitch-planner.timer/service
hold v7-users-autoswitch.timer/service
leave v7-health.service active
do not run canary
do not run user-switch
do not run routing-sync
sample reconcile under quiet
verify registry/rules/routes/switch-history stability
restore planner/apply timers
```

## 7. Mutation Statement

```text
Runtime mutation performed: YES - limited to approved systemd split only
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```
