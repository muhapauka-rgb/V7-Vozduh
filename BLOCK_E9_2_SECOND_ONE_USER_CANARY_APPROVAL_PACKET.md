# BLOCK E9.2 - Second One-User Canary Approval Packet

Mode: read-only approval packet only.

Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO

## Executive Verdict

```text
second_candidate_user=10.7.0.14
current_egress=vless
target_egress=1
rollback_target=vless
target_1_ready=false
blast_radius=one_user
rollback_feasible=true
approval_status=CONDITIONAL
second_canary_strategy=different_user_same_target_1_immediate_rollback_proof
execution_allowed_now=false
```

E9.2 prepared a second one-user canary packet. It did not execute canary, user-switch, routing-sync, autoswitch apply, policy apply, Direct/RU mutation, Trusted RU refresh, proxy apply, kill-switch mutation, registry mutation, deploy, or systemd changes.

The proposed second canary should use a different user and the same target:

```text
forward would run:  v7-user-switch 10.7.0.14 1
rollback would run: v7-user-switch 10.7.0.14 vless
```

This is not an execution approval. The packet is conditional because target `1` is interface/health-ready but current load-state still reports `1_users=1` / `SOFT_FULL` after E9 rollback, while registry/reconcile evidence shows all enabled users on `vless`. That stale or planner-derived load signal must be cleared, explained, or explicitly waived for a mechanics-only one-user canary.

## Runtime Snapshot

Fresh read-only runtime snapshot:

```text
captured_utc=2026-05-25T15:07:16Z
v7-health.service=active/enabled
v7-autoswitch-planner.timer=active/enabled
v7-users-autoswitch.timer=active/enabled
users.registry_sha256=90afd3fb2a626726baee6d2106807f33de62240a674d0bb7a866e62e8c0a8334
egress.registry_sha256=67ac7afbac42b452f6d5be0ff1e3fc3cf3b3fae63ed72a7c18c6363a8e354d2f
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
hidden_user_switch_observed=false
hidden_routing_sync_observed=false
```

Evidence:

- `docs/track7/control-plane/e9_2-evidence/runtime-snapshot.txt`
- `docs/track7/control-plane/e9_2-evidence/candidate-selection.md`
- `docs/track7/control-plane/e9_2-evidence/target-readiness.md`
- `docs/track7/control-plane/e9_2-evidence/hold-model.md`

## Candidate Selection

Selected candidate:

```text
user=10.7.0.14
enabled=1
current=vless
table=1012
current_table_default=default dev tun0 scope link
current_route_get=8.8.8.8 from 10.7.0.14 dev tun0 table 1012
current_ip_rule=1012: from 10.7.0.14 lookup 1012
```

Why this candidate:

- changes the user variable from E9;
- keeps the target variable stable on target `1`;
- remains in the same `10.7.0.0/22` cohort as the first canary;
- uses table `1012`, adjacent to but distinct from the live-proven table `1013`;
- read-only route evidence is coherent;
- no recent switch-history entry for `10.7.0.14` appeared in the inspected tail;
- rollback target is explicit.

Rejected/not selected:

- `10.7.0.15`: already used in E9;
- `10.7.0.7`: disabled;
- `10.0.0.2`, `10.0.0.3`, `10.0.0.6`: older `10.0.0.0/24` cohort, less comparable to E9;
- `10.7.0.8`, `10.7.0.11`, `10.7.0.13`: eligible fallback candidates, not selected because only one bounded candidate is needed.

## Target `1` Readiness

Target `1` positive evidence:

```text
id=1
enabled=1
interface=v7e356a192b79
role=GLOBAL_FAST
manual_only=0
reserve_only=0
exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
interface_state=UP,LOWER_UP
diagnose_reason=OK
diagnose_severity=OK
handshake_age_seconds=96
avg_mbps=60.067
min_mbps=46.59
stability=0.775634
samples=30
```

Target `1` readiness concern:

```text
egress-load.state: 1_users=1
egress-load.state: 1_soft_limit=1
egress-load.state: 1_hard_limit=2
egress-load.state: 1_load_status=SOFT_FULL
egress-load-summary.json: per_egress.1.users=1
```

Because fresh registry evidence shows all enabled users on `vless`, this appears stale or planner-derived rather than a live route assignment. It still matters for approval: the second canary must not execute unless the operator accepts this as a one-user mechanics waiver or a fresh pre-execution check shows the load-state has cleared.

## Preview Outputs

Forward preview:

```text
artifact=docs/track7/control-plane/e9_2-evidence/forward-preview.json
mutation=false
runtime_commands_executed=false
user=10.7.0.14
from_egress=vless
to_egress=1
table=1012
target_interface=v7e356a192b79
route_would_change=ip route replace default dev v7e356a192b79 table 1012
rollback_command=v7-user-switch 10.7.0.14 vless
```

Rollback preview:

```text
artifact=docs/track7/control-plane/e9_2-evidence/rollback-preview.json
mutation=false
runtime_commands_executed=false
user=10.7.0.14
from_egress=1
to_egress=vless
table=1012
target_interface=tun0
route_would_change=ip route replace default dev tun0 table 1012
```

Expected live changes if a future E9.3 is separately approved:

- `users.registry` row for `10.7.0.14` would change `current=vless` to `current=1`;
- assignment file for `10.7.0.14` would be written by `v7-user-switch`;
- switch-history/audit would append one forward entry;
- table `1012` default route would change from `tun0` to `v7e356a192b79`;
- rollback would restore `current=vless` and table `1012` default route to `tun0`;
- no other user should move.

## Future Hold Model

Future canary must repeat the E9 quiet-window pattern:

```text
systemctl stop v7-autoswitch-planner.timer
systemctl stop v7-autoswitch-planner.service
systemctl stop v7-users-autoswitch.timer
systemctl stop v7-users-autoswitch.service
```

`v7-health.service` must remain active.

Restore after evidence:

```text
systemctl start v7-autoswitch-planner.timer
systemctl start v7-users-autoswitch.timer
```

E9.2 did not execute these commands.

## Risk Review

What changes from E9:

- user changes from `10.7.0.15` to `10.7.0.14`;
- route table changes from `1013` to `1012`;
- rollback is not yet live-proven for `10.7.0.14`;
- target remains `1`, so target variable is intentionally stable.

What stays bounded:

- exactly one user;
- exactly one route table;
- same target interface already live-proven;
- no routing-sync dependency;
- rollback target is known.

Risk increases:

- target `1` load-state currently reports `SOFT_FULL` despite registry baseline;
- broader rollback remains unproven beyond the first user;
- no second live proof exists yet.

Recommendation for future execution strategy:

```text
A) rollback again after proof
```

Operational reason: E9.2 is a reproducibility/mechanics test, not a capacity migration. Keeping the second user on target `1` would mix mechanics validation with load/capacity behavior while target load-state is already semantically noisy.

## Approval Status

```text
approval_status=CONDITIONAL
execution_allowed_now=false
```

Conditional requirements before any E9.3 live execution:

- separate bounded live approval naming `10.7.0.14 -> 1`;
- fresh `v7-reconcile-check=OK`;
- fresh `v7-user-route-check=OK`;
- fresh `v7-killswitch-check=OK`;
- fresh `v7-provisioning-reconcile-check=OK`;
- candidate still `current=vless table=1012 enabled=1`;
- target interface still `UP,LOWER_UP`;
- target `1` load-state either clears, is explained, or receives explicit one-user mechanics waiver;
- autoswitch planner/apply authority held cleanly;
- rollback command prepared and still matches baseline.

## Exact Next Recommended Step

Do not execute canary now. The next step should be:

```text
E9.3 bounded live second canary request, only if the operator explicitly accepts the target-1 load-state condition or a fresh snapshot shows target_1_load_state_clean=true.
```

If the operator does not want a load-state waiver, run another read-only target readiness refresh first.

## Final Answers

```text
second_candidate_user=10.7.0.14
current_egress=vless
target_egress=1
rollback_target=vless
target_1_ready=false
blast_radius=one_user
rollback_feasible=true
approval_status=CONDITIONAL
second_canary_strategy=different_user_same_target_1_immediate_rollback_proof
execution_allowed_now=false
runtime_mutation_performed=NO
user_movement_performed=NO
routing_mutation_performed=NO
canary_performed=NO
```

## E9.2.1 Superseding Load-State Finding

E9.2.1 supersedes the target-readiness uncertainty in this packet:

```text
target_1_load_state_classification=REAL_HIDDEN_LOAD
target_1_current_user=10.7.0.5
target_1_ready_for_E9_3=false
candidate_10.7.0.14_still_valid=true
```

The E9.2 packet remains useful for candidate and rollback shape, but target `1` is not currently clean for E9.3. A future approval must either select a different zero-user target, wait for target `1` to return to zero users and refresh evidence, or explicitly waive the fact that target `1` is already occupied.

## E9.2.2 Superseding Target Selection Finding

E9.2.2 attempted to select a replacement target and found no clean target:

```text
candidate_user=10.7.0.14
candidate_still_valid=true
selected_target=NONE
approval_status=NO-GO
```

This supersedes E9.2 target selection. The candidate remains usable for a future packet, but there is no approved target and no executable E9.3 command.

## E9.2.3 Target Readiness Watcher Update

E9.2.3 added a manual read-only checker so target selection can be repeated without mutating runtime:

```text
tool=tools/v7-second-canary-target-readiness
candidate_user=10.7.0.14
candidate_still_valid=true
selected_target=NONE
approval_status=NO-GO
second_canary_readiness=NO-GO
should_E9_3_execute_now=false
```

This packet remains superseded for execution. A future E9.3 approval must use a fresh checker result and must not reuse target `1` while it is occupied by `10.7.0.5`.

## E9.2.5 OpenVPN Waiver Packet Update

E9.2.5 creates a new conditional target-diversity packet:

```text
candidate_user=10.7.0.14
target_egress=openvpn-1779388847-d2ad7c
rollback_target=vless
waiver_name=openvpn_idle_suspect_mechanics_canary
approval_status=CONDITIONAL
execution_allowed_now=false
```

This supersedes the old target `1` packet for the next discussion. E9.3 is still forbidden until a separate bounded live approval explicitly accepts the idle-SUSPECT waiver.
