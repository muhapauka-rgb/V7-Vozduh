# BLOCK E8.8 - One-User Canary Approval Packet

Mode: read-only / approval packet only.

Live mutation: forbidden.

Canary execution: forbidden.

## Executive Verdict

```text
candidate_user=10.7.0.15
current_egress=vless
target_egress=1
rollback_target=vless
canary_blast_radius=one_user
approval_status=CONDITIONAL
execution_allowed_now=false
runtime_mutation_performed=NO
user_movement_performed=NO
routing_mutation_performed=NO
canary_performed=NO
```

`CONDITIONAL` means the packet is complete enough for operator review, but it is not execution approval. The future live canary still needs a separate explicit approval naming this user, target, hold window, rollback command, abort authority, and observation owner.

## Current Runtime Facts

Read-only evidence was collected at `2026-05-25T13:57:37Z` and `2026-05-25T13:58:49Z`.

```text
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
users.registry_hash=4b8ac23f01f8a6f5857500115bac6b401b824502648272ccaae234f76bd37908
egress.registry_hash=67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
```

Authority state outside any approved hold window:

```text
v7-health.service=active/enabled
v7-autoswitch-planner.timer=active/enabled
v7-autoswitch-planner.service=inactive/static
v7-users-autoswitch.timer=active/enabled
v7-users-autoswitch.service=inactive/static
```

This means execution is still not allowed now. The future canary window must hold planner and apply authority again.

## Candidate Selection

Selected candidate:

```text
ip=10.7.0.15 current=vless table=1013 enabled=1
```

Reasons:

- enabled user;
- explicit current egress `vless`;
- explicit route table `1013`;
- current route reality is OK: table `1013` default route points to `tun0`;
- `v7-user-route-check` reports candidate route OK;
- candidate did not appear in the latest `13:29Z-13:45Z` autoswitch burst;
- last observed candidate movement was `2026-05-25T07:54:40Z`, from `1` to `vless`;
- current anti-flap evidence showed only an expired candidate reference near `2026-05-25T13:54:41Z`, before the targeted snapshot at `13:58:49Z`.

Rejected / avoided candidate patterns:

- `10.7.0.13 -> awg3` from older docs is stale and remains inappropriate for the first canary packet;
- `awg3` remains below quality floor and must not be used as the first target;
- users moved during the latest autoswitch burst are avoided as first-choice canary candidates.

## Target Egress Selection

Selected target:

```text
id=1
interface=v7e356a192b79
role=GLOBAL_FAST
enabled=1
manual_only=0
reserve_only=0
exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
```

Target readiness evidence:

```text
load_summary.users=10
load_summary.soft_limit=19
load_summary.hard_limit=24
load_summary.status=OK
stability.avg_mbps=59.4437
stability.min_mbps=43.24
stability.stability=0.727411
stability.samples=30
```

Why target `1` instead of `awg0`/`awg3`:

- `1` has the best current candidate target profile among the observed usable channels;
- `awg0` and `awg3` have materially worse quality/stability signals;
- target `1` explicitly excludes Trusted RU / Direct RU route classes, reducing Gosuslugi-sensitive coupling for this one-user mechanics canary.

## Canary Preview

Forward command that would run only after separate approval:

```bash
v7-user-switch 10.7.0.15 1
```

Forward preview artifact:

```text
docs/track7/control-plane/e8_8-evidence/user-switch-preview.json
docs/track7/control-plane/canary-previews/user-switch-preview.json
```

Important preview fields:

```text
mutation=false
runtime_commands_executed=false
errors=[]
warnings=[]
blast_radius=one_user
from_egress=vless
to_egress=1
table=1013
target_interface=v7e356a192b79
```

Expected registry change:

```diff
-ip=10.7.0.15 current=vless table=1013 enabled=1
+ip=10.7.0.15 current=1 table=1013 enabled=1
```

Expected route-table change:

```text
ip route replace default dev v7e356a192b79 table 1013
```

Expected ip-rule change:

```text
none from user-switch preview
```

Expected switch-history behavior:

```text
append one entry for user_ip=10.7.0.15, from=vless, to=1, table=1013
```

The exact timestamp/reason field is runtime-tool-owned and must be verified after the future canary if it is approved.

## Rollback Preview

Rollback command prepared for the same future approval boundary:

```bash
v7-user-switch 10.7.0.15 vless
```

Rollback preview artifact:

```text
docs/track7/control-plane/e8_8-evidence/rollback-preview.json
docs/track7/control-plane/canary-previews/rollback-preview.json
```

Expected rollback registry change:

```diff
-ip=10.7.0.15 current=1 table=1013 enabled=1
+ip=10.7.0.15 current=vless table=1013 enabled=1
```

Expected rollback route-table change:

```text
ip route replace default dev tun0 table 1013
```

Rollback remains a live mutation and must not be executed without the same bounded approval and observation discipline as the forward canary.

## Canary Hold Model

Future canary window must hold autoswitch planner and apply authority:

```bash
systemctl stop v7-autoswitch-planner.timer
systemctl stop v7-autoswitch-planner.service
systemctl stop v7-users-autoswitch.timer
systemctl stop v7-users-autoswitch.service
```

Future canary window must leave health active:

```text
v7-health.service must remain active
```

Restore sequence after evidence:

```bash
systemctl start v7-autoswitch-planner.timer
systemctl start v7-users-autoswitch.timer
```

Forbidden during the future canary window unless separately approved:

```text
v7-routing-sync
v7-users-autoswitch --apply manual
policy apply
Direct/RU mutation
Trusted RU refresh/diagnostic
proxy apply
kill switch mutation
registry edits outside v7-user-switch
```

## Pre-Canary Gates

All must be true immediately before any future execution:

- `v7-reconcile-check` returns `V7_RECONCILE_RESULT=OK`;
- `v7-user-route-check` returns `V7_USER_ROUTE_CHECK=OK`;
- `v7-killswitch-check` returns `V7_KILLSWITCH_CHECK=OK`;
- `v7-provisioning-reconcile-check` returns `V7_PROVISIONING_RECONCILE_CHECK=OK`;
- `users.registry` hash captured;
- `egress.registry` hash captured;
- no active `v7-users-autoswitch`, `v7-user-switch`, or `v7-routing-sync` process;
- `v7-health.service` active;
- planner/apply timers and services confirmed held;
- target `1` still enabled and load summary still acceptable;
- candidate assignment still exactly `10.7.0.15 current=vless table=1013 enabled=1`;
- forward and rollback previews still match current registry;
- rollback command is copied into the live runbook before execution;
- operator approval explicitly names `10.7.0.15 -> 1`.

## Abort Conditions

Abort before forward switch if:

- any pre-canary checker fails;
- target `1` is degraded, overloaded, disabled, or interface-missing;
- candidate user changed assignment since this packet;
- autoswitch planner/apply cannot be fully held;
- unexpected `v7-user-switch` or `v7-routing-sync` appears;
- registry hash changes unexpectedly before canary;
- route/rule snapshot drifts unexpectedly;
- rollback command cannot be confirmed;
- operator cannot keep observation and restore authority in one window.

Abort after forward switch and rollback immediately if:

- table `1013` does not point to `v7e356a192b79`;
- `v7-user-route-check` fails or reports candidate mismatch;
- `v7-killswitch-check` fails or warns;
- `users.registry` does not show exactly `10.7.0.15 current=1`;
- switch-history does not show expected one-user movement;
- any user other than `10.7.0.15` moves;
- autoswitch process reappears during the window;
- target health falls below accepted threshold.

## Approval Status

```text
approval_status=CONDITIONAL
execution_allowed_now=false
```

The packet identifies a plausible first one-user canary candidate and rollback path. It does not make canary execution GO because the live hold, immediate pre-checks, and operator approval have not been performed in this block.

## Exact Next Step

Prepare a separate bounded live canary approval message for:

```text
10.7.0.15: vless -> 1
rollback: 10.7.0.15 -> vless
```

That next block must be explicitly limited to:

- hold planner/apply authority;
- run pre-checks;
- execute one `v7-user-switch 10.7.0.15 1` only if all gates pass;
- collect evidence;
- rollback if any abort condition triggers;
- restore planner/apply timers.

## Final Mutation Statement

```text
Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
```
