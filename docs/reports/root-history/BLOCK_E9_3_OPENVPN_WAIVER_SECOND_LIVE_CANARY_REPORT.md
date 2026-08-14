# Block E9.3 OpenVPN Waiver Second Live Canary Report

## Summary

Block E9.3 executed the approved waiver-based one-user canary for:

```text
waiver_name=openvpn_idle_suspect_mechanics_canary
candidate_user=10.7.0.14
forward=vless -> openvpn-1779388847-d2ad7c
rollback=openvpn-1779388847-d2ad7c -> vless
candidate_table=1012
target_interface=v7edb0c189291
```

The canary mechanics succeeded during the quiet window:

- autoswitch planner/apply authorities were held;
- `v7-health.service` stayed active;
- `10.7.0.14` moved from `vless` to `openvpn-1779388847-d2ad7c`;
- table `1012` changed from `tun0` to `v7edb0c189291`;
- route_get for `10.7.0.14` used `v7edb0c189291`;
- user-route, kill switch, provisioning reconcile, and reconcile checks stayed OK;
- rollback restored `10.7.0.14` to `vless`;
- table `1012` returned to `tun0`.

Important caveat:

After restoring autoswitch timers, the restored `v7-users-autoswitch.timer` immediately ran its apply service under timer authority and moved another user:

```text
10.7.0.5: 1 -> vless
table 1003: v7e356a192b79 -> tun0
```

No manual autoswitch apply was executed. No manual switch was executed for `10.7.0.5`. This was a post-restore autoswitch side effect and must be treated as a control-plane governance finding.

## Evidence

Evidence folder:

```text
docs/track7/control-plane/e9_3-evidence/
```

Primary evidence files:

| File | Purpose |
|---|---|
| `pre-canary.txt` | pre-canary systemd/process/registry/routing/checker snapshot |
| `hold-confirmation.txt` | planner/apply authority hold confirmation |
| `post-switch.txt` | forward switch evidence |
| `observation-A.txt` | quiet-window observation sample A |
| `observation-B.txt` | quiet-window observation sample B |
| `observation-C.txt` | quiet-window observation sample C |
| `rollback.txt` | rollback evidence |
| `post-restore.txt` | immediate authority restore evidence |
| `post-restore-settle.txt` | post-restore settle evidence |
| `post-restore-drift-analysis.txt` | read-only analysis of post-restore autoswitch movement |

## Pre-Canary Gates

| Gate | Result |
|---|---|
| candidate row | `ip=10.7.0.14 current=vless table=1012 enabled=1` |
| target zero-user | `openvpn target user count from registry: 0` |
| target interface | `v7edb0c189291 UP LOWER_UP` |
| target diagnose | `SUSPECT`, reason `curl_ok_but_handshake_stale` |
| target load | `openvpn-1779388847-d2ad7c_users=0`, `load_status=OK` |
| candidate route table | table `1012` default `tun0` |
| candidate route_get | `dev tun0 table 1012` |
| reconcile | OK |
| user-route-check | OK |
| kill switch | OK |
| provisioning reconcile | OK |

The waiver assumption held: OpenVPN was still idle/stale-handshake `SUSPECT`, not a newly detected hard failure.

## Hold Result

Approved hold commands were executed only for:

```text
v7-autoswitch-planner.timer
v7-autoswitch-planner.service
v7-users-autoswitch.timer
v7-users-autoswitch.service
```

Hold confirmation:

```text
planner.timer=inactive
planner.service=inactive
users.timer=inactive
users.service=inactive
v7-health.service=active
```

## Forward Canary Result

Executed exact approved command:

```bash
v7-user-switch 10.7.0.14 openvpn-1779388847-d2ad7c
```

Result:

```text
v7-user-switch forward rc=0
ip=10.7.0.14 current=openvpn-1779388847-d2ad7c table=1012 enabled=1
table 1012 default dev v7edb0c189291
route_get 8.8.8.8 from 10.7.0.14 iif wg0 -> dev v7edb0c189291 table 1012
```

Checks after forward:

```text
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
V7_RECONCILE_RESULT=OK
```

## Observation Window

Observation samples A/B/C were taken during the held quiet window.

Stable facts across samples:

```text
10.7.0.14 current=openvpn-1779388847-d2ad7c
openvpn target user count from registry=1
table 1012 default dev v7edb0c189291
target diagnose reason=curl_ok_but_handshake_stale
target diagnose severity=SUSPECT
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
V7_RECONCILE_RESULT=OK
```

No autoswitch, user-switch, or routing-sync process was observed during the quiet samples.

## Rollback Result

Safest operational path chosen:

```text
rollback after mechanics proof
```

Reason:

- this was a waiver target, not a clean target;
- the objective was mechanics plus target-diversity proof;
- keeping a user on an idle-SUSPECT target would add unnecessary exposure.

Executed exact approved rollback:

```bash
v7-user-switch 10.7.0.14 vless
```

Result:

```text
v7-user-switch rollback rc=0
ip=10.7.0.14 current=vless table=1012 enabled=1
openvpn target user count from registry=0
table 1012 default dev tun0
route_get 8.8.8.8 from 10.7.0.14 iif wg0 -> dev tun0 table 1012
```

Checks after rollback:

```text
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
V7_RECONCILE_RESULT=OK
```

## Restore Result

Restored approved timer authorities:

```bash
systemctl start v7-autoswitch-planner.timer
systemctl start v7-users-autoswitch.timer
```

No manual autoswitch apply command was executed.

Immediate restore state:

```text
v7-health.service=active
v7-autoswitch-planner.timer=active/enabled
v7-users-autoswitch.timer=active/enabled
```

The timers fired immediately after restore:

```text
python3 /usr/local/bin/v7-users-autoswitch
python3 /usr/local/bin/v7-users-autoswitch --apply
```

This was timer-driven restored authority, not manual execution.

## Post-Restore Side Effect

Post-restore settle evidence showed:

```text
ip=10.7.0.5 current=vless table=1003 enabled=1
table 1003 default dev tun0
```

Before E9.3, `10.7.0.5` was:

```text
current=1
table=1003
default dev v7e356a192b79
```

Classification:

```text
post_restore_autoswitch_movement=true
manual_autoswitch_apply=false
manual_user_switch_for_10.7.0.5=false
canary_quiet_window_blast_radius=one_user
total_block_user_movement=more_than_one_user_due_to_post_restore_timer_apply
```

This is not a failure of the approved OpenVPN canary mechanics, but it is a failure of the stronger post-restore expectation that no extra movement would occur after authority restore.

## Final Answers

| Question | Answer |
|---|---|
| canary_executed | true |
| waiver_used | true |
| waiver_name | `openvpn_idle_suspect_mechanics_canary` |
| rollback_executed | true |
| candidate_user | `10.7.0.14` |
| forward_success | true |
| rollback_success | true |
| users.registry_changed | true during forward/rollback; final registry changed again after autoswitch restore |
| only_one_user_moved | false for full block; true during held canary window |
| routing_drift_observed | false during held canary; post-restore timer moved `10.7.0.5` routing to `tun0` |
| kill_switch_ok | true |
| reconcile_ok | true |
| provisioning_ok | true |
| quiet_window_preserved | true during hold |
| blast_radius_respected | true during canary window; false as full-block invariant after timer restore |
| OpenVPN_target_behavior | route mechanics worked; diagnose remained idle/stale `SUSPECT` |
| diagnose_semantics_confirmed_idle_only | true for observed E9.3 evidence |
| current_canary_status | `SUCCESS_ROLLED_BACK_WITH_POST_RESTORE_AUTOSWITCH_MOVEMENT` |
| execution_allowed_now | false |

## Next Recommended Step

Do not run another canary yet.

Run a read-only E9.3.1 post-restore autoswitch side-effect analysis:

1. Determine why restored `v7-users-autoswitch.timer` immediately moved `10.7.0.5` from `1` to `vless`.
2. Decide whether future canary windows must restore planner first, then observe, then restore apply separately.
3. Define a safer restore sequence that prevents immediate unbounded apply movement after a canary rollback.
4. Reassess whether `v7-users-autoswitch.timer` should be restored in paused/manual-approved mode after canary windows.

## Mutation Statement

```text
Runtime mutation performed: YES — limited to approved hold/restore plus one approved user-switch and rollback
User movement performed: YES — approved candidate 10.7.0.14 during quiet window; additional post-restore timer-driven autoswitch moved 10.7.0.5
Routing mutation performed: YES — table 1012 during canary/rollback; table 1003 later changed by restored autoswitch timer
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: YES — waiver-based bounded one-user canary only
```

