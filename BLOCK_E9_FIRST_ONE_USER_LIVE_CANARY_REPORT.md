# BLOCK E9 - First One-User Live Canary Report

Mode: bounded live execution.

Approved mutation scope:

```text
one approved v7-user-switch: 10.7.0.15 vless -> 1
optional rollback: 10.7.0.15 1 -> vless
```

Forbidden actions remained forbidden:

```text
v7-routing-sync
manual autoswitch --apply
policy apply
Direct/RU mutation
Trusted RU refresh
proxy apply
kill switch mutation
registry edits outside approved v7-user-switch
deploy/systemd changes outside temporary timer/service hold/restore
```

## Executive Verdict

```text
canary_executed=true
rollback_executed=true
candidate_user=10.7.0.15
forward_success=true
rollback_success=true
users.registry_changed=true
only_one_user_moved=true
routing_drift_observed=false
kill_switch_ok=true
reconcile_ok=true
provisioning_ok=true
quiet_window_preserved=true
blast_radius_respected=true
current_canary_status=SUCCESS_ROLLED_BACK
execution_allowed_now=false
```

## Pre-Canary Snapshot

Pre-canary evidence is in:

```text
docs/track7/control-plane/e9-evidence/pre-canary.txt
```

Important pre-canary facts:

```text
candidate=ip=10.7.0.15 current=vless table=1013 enabled=1
target=1 interface=v7e356a192b79 enabled=1
target_5m_avg_mbps=62.64
target_5m_fail_rate=0.0144
target_5m_stability=0.8437
target_load_status=OK
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

Pre-canary note:
- outside quiet hold, autoswitch planner/apply authorities were active;
- no pre-existing `v7-user-switch` or `v7-routing-sync` process was active;
- all enabled users had already been moved to `vless` by prior autoswitch activity, but candidate assignment still matched the approved canary start state.

## Quiet Hold

Evidence:

```text
docs/track7/control-plane/e9-evidence/hold-confirmation.txt
```

Executed:

```text
systemctl stop v7-autoswitch-planner.timer
systemctl stop v7-autoswitch-planner.service
systemctl stop v7-users-autoswitch.timer
systemctl stop v7-users-autoswitch.service
```

Result:

```text
v7-health.service=active
v7-autoswitch-planner.timer=inactive
v7-autoswitch-planner.service=inactive
v7-users-autoswitch.timer=inactive
v7-users-autoswitch.service=inactive
```

Quiet hold was clean; no real autoswitch/user-switch/routing-sync process remained.

## Forward Canary

Evidence:

```text
docs/track7/control-plane/e9-evidence/post-switch.txt
```

Executed exactly:

```text
v7-user-switch 10.7.0.15 1
```

Result:

```text
switch_rc=0
10.7.0.15 current=1 table=1013 enabled=1
table_1013=default dev v7e356a192b79 scope link
route_get=8.8.8.8 from 10.7.0.15 dev v7e356a192b79 table 1013
```

Switch-history forward entry:

```json
{"from": "vless", "host": "v3119922.hosted-by-vdsina.ru", "reason": "manual", "table": "1013", "to": "1", "ts": "2026-05-25T14:28:16.465006+00:00", "user_ip": "10.7.0.15"}
```

Immediate checks:

```text
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
V7_RECONCILE_RESULT=OK
```

## Observation Window

Evidence:

```text
docs/track7/control-plane/e9-evidence/observation-A.txt
docs/track7/control-plane/e9-evidence/observation-B.txt
docs/track7/control-plane/e9-evidence/observation-C.txt
```

Samples:

| Sample | Time UTC | Candidate | Table 1013 | Checks | Process Guard |
|---|---:|---|---|---|---|
| A | 14:28:57 | `current=1` | `v7e356a192b79` | OK | quiet |
| B | 14:29:32 | `current=1` | `v7e356a192b79` | OK | quiet |
| C | 14:30:06 | `current=1` | `v7e356a192b79` | OK | quiet |

Observation verdict:

```text
users.registry hash stable after forward switch=true
egress.registry hash stable=true
route_table_1013 stable=true
switch-history extra movement=false
autoswitch/user-switch/routing-sync process=false
checks_ok=true
```

No abort condition triggered.

## Decision

Chose Option B: rollback immediately after mechanics proof.

Reason:
- this was the first live canary;
- mechanics were proven;
- keeping the user on target `1` was not necessary to prove the control-plane path;
- rollback restored baseline before autoswitch authorities were restored;
- shortest exposure is the safer operational path.

## Rollback

Evidence:

```text
docs/track7/control-plane/e9-evidence/rollback.txt
```

Executed exactly:

```text
v7-user-switch 10.7.0.15 vless
```

Result:

```text
rollback_rc=0
10.7.0.15 current=vless table=1013 enabled=1
table_1013=default dev tun0 scope link
route_get=8.8.8.8 from 10.7.0.15 dev tun0 table 1013
```

Switch-history rollback entry:

```json
{"from": "1", "host": "v3119922.hosted-by-vdsina.ru", "reason": "manual", "table": "1013", "to": "vless", "ts": "2026-05-25T14:30:34.658667+00:00", "user_ip": "10.7.0.15"}
```

Rollback checks:

```text
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
V7_RECONCILE_RESULT=OK
```

## Restore

Evidence:

```text
docs/track7/control-plane/e9-evidence/post-restore.txt
```

Executed:

```text
systemctl start v7-autoswitch-planner.timer
systemctl start v7-users-autoswitch.timer
```

Result after settle:

```text
v7-health.service=active
v7-autoswitch-planner.timer=active
v7-autoswitch-planner.service=inactive
v7-users-autoswitch.timer=active
v7-users-autoswitch.service=inactive
10.7.0.15 current=vless table=1013 enabled=1
table_1013=default dev tun0 scope link
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

Restore note:
- timers fired immediately after restore, so transient `v7-users-autoswitch` processes appeared;
- after settle, no `v7-user-switch` or `v7-routing-sync` was observed;
- no extra switch-history movement appeared after the manual rollback.

## Answers Required By Block E9

```text
canary_executed=true
rollback_executed=true
candidate_user=10.7.0.15
forward_success=true
rollback_success=true
users.registry_changed=true
only_one_user_moved=true
routing_drift_observed=false
kill_switch_ok=true
reconcile_ok=true
provisioning_ok=true
quiet_window_preserved=true
blast_radius_respected=true
current_canary_status=SUCCESS_ROLLED_BACK
execution_allowed_now=false
```

## Exact Next Recommended Step

Do not expand to multi-user movement yet.

Recommended next block:

```text
E9.1 - post-canary monitoring and second canary approval packet
```

Purpose:
- confirm autoswitch authority after restore remains stable;
- verify no delayed movement occurred after E9;
- decide whether a second one-user canary should be attempted, with a fresh candidate and target chosen from current runtime evidence;
- keep `routing-sync` forbidden as first broad mutation.

## Final Mutation Statement

```text
Runtime mutation performed: YES - limited to approved timer/service hold/restore plus one approved user-switch and rollback
User movement performed: YES - one approved user only, forward and rollback
Routing mutation performed: YES - table 1013 only
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: YES - bounded one-user canary only
```
