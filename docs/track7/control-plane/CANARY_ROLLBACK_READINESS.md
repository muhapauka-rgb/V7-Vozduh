# Canary Rollback Readiness

## Candidate Rollback

E9 forward canary:

```text
v7-user-switch 10.7.0.15 1
```

Rollback command:

```text
v7-user-switch 10.7.0.15 vless
```

Rollback is also mutation and must not be executed without the same live approval boundary as the forward canary.

## Block E9 Rollback Result

```text
rollback_executed=true
rollback_success=true
candidate_user=10.7.0.15
from=1
to=vless
table=1013
route_after_rollback=default dev tun0 scope link
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
V7_RECONCILE_RESULT=OK
```

E9 live-proved rollback for this exact user after the forward canary. This does not prove rollback for other users, `routing-sync`, policy apply, Direct/RU, proxy runtime, or kill-switch mutation.

## Block E9.1 Post-Rollback Monitoring

```text
10.7.0.15_still_vless=true
table_1013_back_to_tun0=true
users.registry_stable=true
egress.registry_stable=true
delayed_side_effects_observed=false
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
V7_RECONCILE_RESULT=OK
```

The E9 rollback remained stable through baseline plus three 60-second monitoring samples.

## Rollback Evidence Prepared

- Previous egress after E8.8 selection: `vless`.
- Candidate target egress after E8.8 selection: `1`.
- Route table: `1013`.
- Rollback preview artifact: `docs/track7/control-plane/canary-previews/rollback-preview.json`.
- Expected rollback route: `ip route replace default dev tun0 table 1013`.

## Required Pre-Rollback Evidence During Future Canary

- Confirm current registry says `10.7.0.15 current=1`.
- Confirm table `1013` default route points to `v7e356a192b79`.
- Confirm no autoswitch movement is active.
- Confirm kill switch is still OK before rollback.
- Confirm rollback operator approval is present.

## Required Post-Rollback Checks

- `users.registry` returns `10.7.0.15 current=vless`.
- `user-10.7.0.15.assign` returns `vless`.
- Table `1013` default route uses `tun0`.
- `v7-user-route-check` remains OK.
- `v7-killswitch-check` remains OK.
- Switch log/audit evidence exists if the live tools emit it.

## Partial Failure Handling

If rollback partially fails:

- do not run `v7-routing-sync` as an automatic fallback;
- capture `users.registry`, assignment file, table `1013`, and kill switch status;
- keep autoswitch held;
- escalate to manual operator review with one-user scope still preserved.

## Verdict

Rollback shape is understandable and live-proven for `10.7.0.15` only. Broader rollback remains tool/action-specific and must not be assumed.

## Block E9.2 Proposed Second Rollback

```text
candidate_user=10.7.0.14
forward_would_run=v7-user-switch 10.7.0.14 1
rollback_would_run=v7-user-switch 10.7.0.14 vless
table=1012
expected_forward_route=default dev v7e356a192b79 table 1012
expected_rollback_route=default dev tun0 table 1012
rollback_feasible=true
rollback_live_proven_for_this_user=false
```

Rollback for `10.7.0.14` is previewed and mechanically analogous to E9, but it is not live-proven yet. If E9.3 is approved, the recommended strategy is immediate rollback after proof unless the operator explicitly approves a longer one-user observation period.

Required rollback evidence for E9.3:

- before forward: `10.7.0.14 current=vless table=1012`;
- after forward: `10.7.0.14 current=1` and table `1012` default route uses `v7e356a192b79`;
- rollback command: `v7-user-switch 10.7.0.14 vless`;
- after rollback: `10.7.0.14 current=vless` and table `1012` default route uses `tun0`;
- all four runtime checkers remain OK.

## Block E9.2.1 Rollback Impact

E9.2.1 did not invalidate the `10.7.0.14 -> vless` rollback command, but it changed target readiness:

```text
candidate_10.7.0.14_still_valid=true
target_1_current_user=10.7.0.5
target_1_ready_for_E9_3=false
```

If a future canary still targets `1`, rollback must account for two target-1 users during the canary window:

- existing real user: `10.7.0.5`;
- canary user if executed: `10.7.0.14`.

This increases interpretation risk. The recommended rollback model remains one-user rollback for the canary user only, but target `1` should not be used until it is zero-user again or explicitly waived.

## Block E9.2.2 Rollback Status

```text
candidate_user=10.7.0.14
selected_target=NONE
rollback_target=vless
rollback_preview_actionable=false
```

Because no clean target was selected, there is no actionable forward/rollback pair for E9.3. The baseline rollback command would still be:

```text
v7-user-switch 10.7.0.14 vless
```

but the candidate is already on `vless`, so this is not a live rollback plan until a future forward target is selected.

## Block E9.2.5 OpenVPN Waiver Rollback

E9.2.5 prepares a new conditional forward/rollback pair:

```text
forward_would_run=v7-user-switch 10.7.0.14 openvpn-1779388847-d2ad7c
rollback_would_run=v7-user-switch 10.7.0.14 vless
table=1012
expected_forward_route=default dev v7edb0c189291 table 1012
expected_rollback_route=default dev tun0 table 1012
rollback_feasible=true
rollback_live_proven_for_this_user=false
waiver_name=openvpn_idle_suspect_mechanics_canary
```

Rollback remains one-user scoped. If E9.3 is approved under this waiver, rollback must be ready before the forward switch and must not rely on `v7-routing-sync`.

## E9.3 Rollback Result

Rollback for the OpenVPN waiver canary succeeded:

```bash
v7-user-switch 10.7.0.14 vless
```

Verified rollback state:

```text
ip=10.7.0.14 current=vless table=1012 enabled=1
table 1012 default dev tun0
route_get from 10.7.0.14 -> dev tun0 table 1012
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

Rollback readiness remains good for candidate-level user switches. It does not prove autoswitch restore readiness: after rollback, restoring `v7-users-autoswitch.timer` caused timer-driven autoswitch movement for `10.7.0.5`.

## E9.3.1 Restore-Phase Rollback Boundary

E9.3.1 separates candidate rollback readiness from restore readiness:

```text
candidate_rollback=successful
candidate_table_restored=1012 -> tun0
restore_phase_additional_movement=10.7.0.5: 1 -> vless
restore_sequence_safe=false
```

Future rollback readiness must include a restore-stage plan:

- restore planner authority first;
- inspect planner-only pending movements;
- keep apply authority held until separate approval;
- record post-restore evidence separately from canary/rollback evidence;
- treat non-candidate pending movement as autoswitch recovery, not as part of the canary rollback.

## E9.3.2 Staged Restore Rollback Rule

Rollback readiness now includes a restore boundary:

```text
rollback_complete != operation_complete
planner_restore_first=true
apply_restore_requires_separate_approval=true
```

After rollback succeeds, the operator must not immediately restore apply authority. The correct future sequence is:

1. verify candidate rollback;
2. restore planner only;
3. observe pending moves;
4. approve or reject apply restore separately;
5. classify any apply movement as autoswitch recovery.
# E9.3.3 Restore Boundary Addendum

Rollback readiness is no longer sufficient by itself. E9.3.3 confirmed that canary rollback can be separated from autoswitch apply restore.

For future canaries, rollback readiness must include:

- candidate rollback command;
- candidate route table verification;
- planner-only restore observation;
- pending autoswitch movement summary;
- explicit decision to keep apply held or restore apply by separate approval.

Current status:

```text
candidate_rollback_model=proven_by_e9_and_e9_3
planner_only_restore_model=proven_by_e9_3_3
apply_restore_model=not_approved
```
