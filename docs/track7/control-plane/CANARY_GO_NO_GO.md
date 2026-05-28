# Canary GO / NO-GO Criteria

## Current Verdict

```text
NO-GO
```

## Block E8 Rehearsal Result

```text
quiet_window_rehearsal=aborted_restored
quiet_window_verified=false
reconcile_under_quiet=NOT_SAMPLED_ABORTED
canary_status=NO-GO
```

## Block E8.1 Authority Mapping Result

```text
unknown_loop_origin=v7-health.service
v7-health.service MainPID=2938206
v7-health.service Restart=always
v7-health.service ExecStart includes v7-users-autoswitch every 30 seconds
timer_service_only_hold_sufficient=false
canary_status=NO-GO
execution_allowed_now=False
```

## Block E8.2 Approval Packet Result

```text
full_authority_quiet_window_packet=prepared
quiet_window_executed=false
v7-health.service_hold_executed=false
recommended_path=Option B split/refactor first unless immediate quiet-window truth is required
canary_status=NO-GO
quiet_window_verified=false
execution_allowed_now=False
```

## Block E8.3 Split Design Result

```text
health_autoswitch_split_design=prepared
draft_units_created=true
split_deployed=false
post_split_authority_mapping_done=false
canary_status=NO-GO
quiet_window_verified=false
execution_allowed_now=False
```

## Block E8.4 Split Deploy Result

```text
health_autoswitch_split_deployed=true
v7-health.service_health_only=true
planner_authority_separated=true
apply_authority_unchanged=true
rollback_performed=false
quiet_window_verified=false
canary_status=NO-GO
execution_allowed_now=False
```

## Block E8.5 Post-Split Quiet-Window Result

```text
post_split_quiet_window_rehearsal_executed=true
rehearsal_aborted=false
restore_success=true
v7-health_stayed_active=true
autoswitch_planner_held=true
autoswitch_apply_held=true
autoswitch_fully_quiet=true
users.registry_changed=false
egress.registry_changed=false
user_movement_observed=false
routing_drift_observed=false
quiet_window_verified=true
reconcile_under_quiet=STABLE_FAIL
kill_switch_OK=true
user_route_check_OK=true
provisioning_reconcile_OK=true
canary_status=CONDITIONAL
execution_allowed_now=False
```

## Block E8.6 Reconcile Classification Result

```text
reconcile_under_quiet_classification=CONFIRMED_FALSE_POSITIVE
false_positive_class=pipefail_grep_q_sigpipe
affected_check=missing ip rule lookup table
real_runtime_mismatch_candidates=none for this failure class
canary_status=CONDITIONAL
execution_allowed_now=False
```

## Block E8.7 Reconcile Checker Fix Result

```text
v7-reconcile-check_repo_patched=true
v7-reconcile-check_runtime_deployed=true
backup_path=/root/v7-reconcile-check.backup.E87.20260525T134737Z
V7_RECONCILE_RESULT_after_fix=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
canary_status=CONDITIONAL
execution_allowed_now=False
```

## Block E8.8 One-User Canary Approval Packet

```text
candidate_user=10.7.0.15
current_egress=vless
target_egress=1
rollback_target=vless
route_table=1013
target_interface=v7e356a192b79
approval_status=CONDITIONAL
execution_allowed_now=False
runtime_mutation_performed=NO
user_movement_performed=NO
routing_mutation_performed=NO
canary_performed=NO
```

## Block E9 First One-User Live Canary Result

```text
canary_executed=true
rollback_executed=true
candidate_user=10.7.0.15
forward=vless -> 1
rollback=1 -> vless
forward_success=true
rollback_success=true
only_one_user_moved=true
routing_drift_observed=false
kill_switch_ok=true
reconcile_ok=true
provisioning_ok=true
quiet_window_preserved=true
blast_radius_respected=true
current_canary_status=SUCCESS_ROLLED_BACK
execution_allowed_now=False
```

## Block E9.1 Post-Canary Monitoring Result

```text
post_canary_monitoring_executed=true
delayed_side_effects_observed=false
unexpected_user_movement=false
candidate_10.7.0.15_still_vless=true
table_1013_back_to_tun0=true
users.registry_stable=true
egress.registry_stable=true
routing_drift_observed=false
hidden_routing_sync_observed=false
hidden_user_switch_observed=false
autoswitch_post_restore_behavior=normal
current_canary_status=SUCCESS_ROLLED_BACK_MONITORED_STABLE
second_canary_readiness=CONDITIONAL
execution_allowed_now=False
```

## Block E9.4.2 Fresh Bounded Apply Restore Retry Result

```text
apply_restore_executed=true
apply_restore_aborted=false
final_planner_selected_moves=0
final_telegram_hard_blocked=false
egress_1_eligible=true
actual_movements_count=0
broad_failover_observed=false
reconcile_ok=true
user_route_check_ok=true
kill_switch_ok=true
provisioning_ok=true
restore_verdict=CLEAN_RESTORE
autoswitch_recovery_bounded=true
current_canary_status=CONDITIONAL_APPLY_RESTORE_CLEAN_NEW_CANARY_APPROVAL_REQUIRED
execution_allowed_now=False
```

E9.4.2 removes the apply-restore-held blocker. It does not grant live canary execution. Any next canary requires a fresh approval packet and a new bounded quiet-window execution block.

## Block E9.4.3 Post-Apply-Restore Monitoring

E9.4.3 found delayed timer-driven autoswitch movement after the E9.4.2 clean restore observation:

```text
post_restore_monitoring_executed=true
delayed_side_effects_observed=true
unexpected_user_movement=true
actual_moved_users=10.7.0.5,10.0.0.2,10.0.0.3
movement=1 -> vless
routing_drift_observed=false
hidden_routing_sync_observed=false
hidden_user_switch_observed=false
autoswitch_timer_behavior=normal
selected_moves_status=delayed_timer_driven_failover_then_selected_moves_empty
reconcile_ok=true
user_route_check_ok=true
kill_switch_ok=true
provisioning_ok=true
restore_governance_live_proven=false
current_canary_status=NO-GO_POST_RESTORE_DELAYED_AUTOSWITCH_MOVEMENT_OBSERVED
execution_allowed_now=false
```

E9.4.2 proves the immediate clean-gate path, but E9.4.3 proves that immediate post-restore samples are not enough to clear delayed autoswitch side effects. Any next canary is blocked until the delayed movement is classified or the restore model adds a longer settle/guard window.

## Block E10.5 WireGuard Diagnostic / Reservation Feasibility

```text
wireguard_root_classification=STALE_HANDSHAKE_ONLY
wireguard_quality_ok=true
wireguard_zero_user=true
wireguard_reservation_feasible=true
reservation_requires_mutation=true
waiver_required=true
waiver_status=waiver_conditional
clean_target_possible=true
current_canary_status=NO-GO_E10_5_WIREGUARD_RESERVATION_OR_DIAGNOSE_FIX_REQUIRED
execution_allowed_now=false
```

WireGuard is the best current conditional path for a clean test target, but E10.5 does not authorize reservation or canary execution. Next step is a bounded approval packet for WireGuard reservation metadata and/or diagnose semantics refinement.

## Block E11.1 WireGuard Clean Target Diagnostic

```text
wireguard_root_classification=STALE_HANDSHAKE_ONLY
wireguard_quality_ok=true
wireguard_zero_user=true
wireguard_reservation_feasible=true
reservation_requires_mutation=true
waiver_required=true
waiver_status=waiver_conditional
expected_second_canary_readiness_after_reservation=CONDITIONAL_OR_GO_IF_DIAGNOSE_SEMANTICS_FIXED
dedicated_test_egress_needed=false_for_next_packet
current_canary_status=NO-GO_E11_1_WIREGUARD_RESERVATION_OR_DIAGNOSE_SEMANTICS_REQUIRED
execution_allowed_now=false
```

E11.1 authorizes no live action. It selects the next governance path: WireGuard reservation approval plus stale-handshake diagnose fix or explicit waiver.

## Block E11.3 WireGuard Reservation Metadata Mutation

```text
reservation_mutation_executed=true
rollback_performed=false
backup_path=/opt/v7/egress/state/egress.registry.e11_3_backup.20260526T184617Z
wireguard_reserved_after=true
wireguard_users_after=0
users.registry_changed=false
unrelated_egress_rows_changed=false
target_readiness_after=NO-GO
selected_target_after=NONE
waiver_required_after=true
restore_settle_gate_status=GO_BY_RUNTIME_PRE_GATE_NO_SELECTED_MOVES
reconcile_ok=true
user_route_check_ok=true
kill_switch_ok=true
provisioning_ok=true
second_canary_readiness_after=NO-GO
current_canary_status=NO-GO_E11_3_WIREGUARD_RESERVED_DIAGNOSE_SEMANTICS_OR_WAIVER_REQUIRED
execution_allowed_now=false
```

E11.3 reserved WireGuard metadata only. It did not fix diagnose semantics, did
not approve canary execution, and did not move users. The next safe step is a
fresh E11.4 diagnose semantics fix or stale-handshake waiver approval packet.

## GO Criteria

All must be true before any future one-user canary:

- `tools/v7-route-movement-preview` forward preview exists with `mutation=false`, `runtime_commands_executed=false`, and `errors=[]`.
- Rollback preview exists and exact rollback command is known.
- Candidate user is explicitly named.
- Target egress is healthy, enabled, not overloaded, and acceptable under policy thresholds.
- `v7-killswitch-check` is OK immediately before canary.
- `v7-user-route-check` is OK immediately before canary.
- Provisioning reconcile is OK immediately before canary.
- `v7-reconcile-check` is OK immediately before canary.
- Quiet-window rehearsal succeeded.
- Reconcile is clean under quiet-window, or an approved false-positive waiver exists.
- Autoswitch apply authority is held or otherwise proven unable to interfere.
- `v7-health.service` autoswitch planner authority is held, split out, or otherwise proven unable to write autoswitch/planner state during the window.
- If split path is chosen, post-split authority mapping proves `v7-health.service` no longer calls `v7-users-autoswitch`.
- If split path is chosen, `v7-autoswitch-planner.timer/service` can be held independently from health.
- After E8.4, post-split quiet-window rehearsal must hold `v7-autoswitch-planner.timer/service` and `v7-users-autoswitch.timer/service` while leaving `v7-health.service` active.
- The full authority model explicitly covers `v7-health.service`, admin/manual invocation, sentinel-capable invocation, and restore-time `v7-routing-sync` attribution.
- No anti-flap penalty/freeze applies to the candidate user.
- Trusted RU stale state is confirmed irrelevant to the candidate route class, or refreshed in a separately approved governance flow.
- Operator approval is explicit and bounded to one user.

## HARD BLOCKERS

Hard blockers cannot be ignored by the planner. They require resolution or a separately documented operator waiver where noted.

- autoswitch active authority can still run `v7-users-autoswitch --apply`;
- quiet-window rehearsal has not succeeded;
- `v7-reconcile-check` is not OK immediately before canary;
- target egress is below quality floor and no explicit one-user waiver exists;
- rollback command or rollback verification is unclear;
- kill switch is not OK;
- user route check is not OK;
- provisioning reconcile is not OK;
- Trusted RU/Gosuslugi-sensitive state is stale and relevant to the canary path;
- candidate user is in anti-flap/penalty state;
- any plan requires `v7-routing-sync` as the first live action.

## CONDITIONAL WAIVERS

Waivers must be explicit, time-bounded, and one-user scoped. A waiver does not turn the platform green.

- Target egress quality floor waiver: allowed only if the canary purpose is routing mechanics, not customer experience, and rollback is immediate.
- Reconcile false-positive waiver: allowed only after full read-only route/rule evidence proves candidate table consistency.
- Quiet-window rehearsal waiver: not allowed for canary; rehearsal success is mandatory.
- Trusted RU stale-state waiver: allowed only if the candidate path and target egress do not affect Trusted RU/Gosuslugi-sensitive route classes.
- Anti-flap waiver: allowed only when autoswitch is held and the operator accepts that the candidate was recently unstable.

## Block E9.3.5 Apply Restore Gate Result

```text
apply_restore_executed=false
apply_restore_aborted=true
final_planner_selected_moves=3
final_planner_candidate_moves_total=15
selected_moves=10.0.0.2:1->vless,10.0.0.3:1->vless,10.0.0.6:1->vless
apply_timer_restored=false
actual_movements_count=0
current_canary_status=NO-GO_APPLY_RESTORE_ABORTED_BY_FINAL_PLANNER_SAMPLE
execution_allowed_now=false
```

The apply restore block did not execute because final planner-only evidence showed nonzero pending movement. Further canary discussion remains blocked until autoswitch apply restore has either a fresh zero-move planner sample or a separate explicit approval for an exact movement list.

## Block E9.3.6 Root-Cause Result

```text
egress_1_ineligibility_root_cause=service_instagram_failed
root_cause_classification=MIXED_TRANSIENT_SERVICE_SIGNAL_AND_EXPECTED_FAILOVER_BEHAVIOR
confidence=high_for_abort_sample_medium_for_current_stability
apply_restore_safe_now=false
apply_should_remain_held=true
current_canary_status=NO-GO_APPLY_RESTORE_ROOT_CAUSE_UNDERSTOOD_APPLY_HELD
execution_allowed_now=false
```

Canary remains blocked because apply restore governance is unresolved, even though the first two one-user canary mechanics were proven.

## NO-GO Criteria

Any one of these blocks canary:

- autoswitch timer can still run `v7-users-autoswitch --apply` during the proposed canary window;
- `v7-autoswitch-planner.timer/service` can still run planner writes during the proposed canary window;
- `v7-health.service` is not health-only or begins running the 30-second autoswitch planner/state loop again;
- candidate user is in anti-flap penalty/freeze;
- target egress is below policy quality floor or overloaded;
- kill switch warning/failure;
- user route check warning/failure;
- provisioning reconcile warning/failure;
- unexplained route consistency errors;
- rollback command or post-checks unclear;
- plan requires `v7-routing-sync` as first live action;
- Trusted RU/Gosuslugi-sensitive state is relevant and stale;
- operator approval is missing.

## Current Blockers

- Autoswitch apply timer is active outside approved hold windows.
- Autoswitch planner timer is active outside approved hold windows.
- Block E8.4 deployed the split and completed post-deploy authority mapping.
- Block E8.5 verified a post-split quiet window while leaving `v7-health.service` active.
- E8.7 fixed and deployed `v7-reconcile-check`; post-fix result is OK.
- E8.8 prepared a fresh one-user approval packet for `10.7.0.15: vless -> 1`.
- E9 executed the first approved one-user canary and rollback successfully.
- E9.1 observed no delayed side effects after autoswitch timers were restored.
- Execution is still blocked for any additional canary until a separate live approval holds planner/apply authority and reruns immediate pre-checks.
- Old candidate `10.7.0.13 -> awg3` is superseded by E8.8 and must not be used as the first canary target.
- Target `awg3` remains avoided because quality/stability is weak.
- Trusted RU decision evidence remains sensitive; E8.8 target `1` excludes `TRUSTED_RU_SENSITIVE,DIRECT_RU`, but this must be rechecked before execution.

## Recommendation

Continue governance. The first one-user canary succeeded, was rolled back, and remained stable in post-canary monitoring. Do not expand scope without a new approval packet.

Preferred next step:

```text
E9.2 second one-user canary approval packet, if current runtime evidence supports it.
```

## Block E9.2 Second Canary Approval Packet

```text
second_candidate_user=10.7.0.14
current_egress=vless
target_egress=1
rollback_target=vless
target_1_ready=false
approval_status=CONDITIONAL
execution_allowed_now=False
```

E9.2 prepared a second one-user approval packet only. It did not execute canary, user-switch, routing-sync, autoswitch apply, route mutation, registry mutation, or deploy.

The second canary remains conditional, not executable, because target `1` is interface/health-ready but load-state is not clean:

```text
1_users=1
1_soft_limit=1
1_hard_limit=2
1_load_status=SOFT_FULL
```

Fresh registry/reconcile evidence still shows all enabled users on `vless`, so this appears stale or planner-derived. It must be cleared, explained, or explicitly waived for a one-user mechanics canary before E9.3 execution can be considered.

Updated GO requirements for E9.3:

- separate live approval names `10.7.0.14 -> 1`;
- candidate still `current=vless table=1012 enabled=1`;
- target `1` interface still `UP,LOWER_UP`;
- target `1` load-state is clean or explicitly waived for one-user mechanics;
- planner/apply timers and services are held cleanly;
- `v7-health.service` remains active;
- `v7-reconcile-check`, `v7-user-route-check`, `v7-killswitch-check`, and `v7-provisioning-reconcile-check` are all OK immediately before switch;
- rollback command `v7-user-switch 10.7.0.14 vless` is prepared.

## Block E9.2.1 Target 1 Load-State Truth

```text
target_1_load_state_classification=REAL_HIDDEN_LOAD
target_1_ready_for_E9_3=false
waiver_required=true
waiver_acceptable=false
real_hidden_load_detected=true
candidate_10.7.0.14_still_valid=true
execution_allowed_now=False
```

E9.2.1 showed that target `1` load-state is real current runtime state:

```text
10.7.0.5 current=1 table=1003 enabled=1
table 1003 default dev v7e356a192b79
```

This supersedes the E9.2 assumption that `1_users=1` might be stale or planner-derived. The second canary may not proceed to target `1` while target `1` is already occupied and static load marks it `SOFT_FULL`, unless a new explicit approval accepts that the test is no longer pure one-user mechanics.

Updated NO-GO for E9.3 target `1`:

- target `1` has real current user `10.7.0.5`;
- static load status is `SOFT_FULL`;
- adding `10.7.0.14` would mix route mechanics with capacity/load behavior;
- current recommended next step is read-only target selection refresh, not live execution.

## Block E9.2.2 Target Selection Refresh

```text
candidate_user=10.7.0.14
candidate_still_valid=true
selected_target=NONE
approval_status=NO-GO
execution_allowed_now=False
```

E9.2.2 found no clean zero-user target for the second canary:

- `1` is occupied by real user `10.7.0.5`;
- `awg0` is zero-user but below quality floor;
- `awg3` is zero-user but below quality floor;
- `openvpn-1779388847-d2ad7c` is zero-user but diagnose `SUSPECT`;
- `wireguard-1779454504-c43409` is zero-user but diagnose `SUSPECT`.

Updated GO/NO-GO:

```text
E9.3=NO-GO
```

The next safe step is another read-only target selection refresh after target state changes, or a new explicit waiver packet if the operator wants to accept a non-clean target.

## Block E9.2.3 Target Readiness Watcher

E9.2.3 added a manual read-only checker:

```text
tool=tools/v7-second-canary-target-readiness
candidate_user=10.7.0.14
candidate_still_valid=true
selected_target=NONE
approval_status=NO-GO
second_canary_readiness=NO-GO
execution_allowed_now=false
```

The checker formalizes the E9.2.2 target-selection rules and can be rerun later without mutating runtime. It does not authorize E9.3.

Current GO/NO-GO update:

| Gate | Status | Reason |
|---|---|---|
| candidate `10.7.0.14` | GO | still `current=vless`, enabled, rollback target clear |
| target `1` | NO-GO | occupied by real user `10.7.0.5`, load-state users=1 |
| `awg0` | NO-GO | zero-user but below quality floor and lacks sensitive-class exclusions |
| `awg3` | NO-GO | zero-user but below quality floor and lacks sensitive-class exclusions |
| OpenVPN target | NO-GO | zero-user and fast, but diagnose `SUSPECT` |
| WireGuard target | NO-GO | zero-user and fast, but diagnose `SUSPECT` |

E9.3 remains forbidden until the manual checker returns a clean `GO` and a separate live approval names the exact user, target, rollback, and quiet-window hold.

## Block E9.2.4 Zero-User Egress Diagnostics

E9.2.4 classified why the watcher has no clean target:

```text
truly_no_clean_target=true
best_current_target=1
occupied_target_acceptable_with_waiver=true
openvpn_target_real_status=IDLE_BUT_HEALTHY_DIAGNOSE_TOO_STRICT
wireguard_target_real_status=IDLE_BUT_HEALTHY_DIAGNOSE_TOO_STRICT
awg0_real_status=QUALITY_TOO_LOW
awg3_real_status=QUALITY_TOO_LOW
second_canary_readiness=CONDITIONAL
execution_allowed_now=false
```

Updated GO/NO-GO:

| Path | Status | Requirement |
|---|---|---|
| clean zero-user target | NO-GO | wait for watcher `selected_target != NONE` |
| OpenVPN waiver path | CONDITIONAL | explicit idle-SUSPECT waiver plus fresh read-only evidence |
| WireGuard waiver path | CONDITIONAL | explicit idle-SUSPECT waiver plus fresh read-only evidence |
| occupied target `1` path | CONDITIONAL | explicit mechanics-with-production-load waiver |
| AWG0/AWG3 | NO-GO | quality must improve before use |

No live E9.3 execution is allowed from E9.2.4. The next packet must explicitly choose clean isolation, target diversity with waiver, or production-load realism with waiver.

## Block E9.2.5 OpenVPN Waiver Approval Packet

E9.2.5 chooses the target-diversity waiver path and prepares an approval packet only:

```text
candidate_user=10.7.0.14
target_egress=openvpn-1779388847-d2ad7c
rollback_target=vless
waiver_name=openvpn_idle_suspect_mechanics_canary
waiver_required=true
waiver_acceptable=true
approval_status=CONDITIONAL
execution_allowed_now=false
```

Updated gate state:

| Gate | Status | Notes |
|---|---|---|
| clean target | NO-GO | OpenVPN remains diagnose `SUSPECT` |
| waiver packet | CONDITIONAL | explicit idle/stale handshake waiver prepared |
| candidate | GO | `10.7.0.14 current=vless table=1012 enabled=1` |
| target zero-user | GO | OpenVPN target has zero registry/load users in evidence |
| target quality | GO | avg/min/stability above floor |
| target diagnose | CONDITIONAL | only stale-idle `SUSPECT` is waived |
| live execution | FORBIDDEN | requires separate E9.3 bounded live approval |

No E9.3 execution is allowed from this document. A future E9.3 must repeat fresh checks and explicitly accept the waiver.

## Block E9.3 OpenVPN Waiver Canary Execution

E9.3 executed the approved OpenVPN idle-SUSPECT waiver canary:

```text
candidate_user=10.7.0.14
forward=vless -> openvpn-1779388847-d2ad7c
rollback=openvpn-1779388847-d2ad7c -> vless
waiver_name=openvpn_idle_suspect_mechanics_canary
```

The held canary window passed: forward switch, observation, rollback, reconcile, user-route, kill switch, and provisioning checks all stayed OK.

Post-restore caveat:

```text
v7-users-autoswitch.timer fired immediately after restore
10.7.0.5 moved from 1 to vless under restored timer authority
```

Updated state:

```text
current_canary_status=SUCCESS_ROLLED_BACK_WITH_POST_RESTORE_AUTOSWITCH_MOVEMENT
execution_allowed_now=false
```

No further canary should run until the autoswitch restore side effect is analyzed and the restore sequence is made staged or explicitly bounded.

## Block E9.3.1 Restore Side-Effect Analysis

```text
restore_side_effect_classification=EXPECTED_BUT_UNSAFE_RESTORE_SEQUENCE
autoswitch_root_cause=timer_restore_immediate_apply_failover
blast_radius_during_canary=one_user
blast_radius_after_restore=broader_than_canary
restore_sequence_safe=false
restore_sequence_governance_gap=true
future_restore_model_recommended=planner_first_apply_by_separate_approval
second_canary_readiness=NO-GO
execution_allowed_now=false
```

Updated hard gate:

- restore `v7-autoswitch-planner.timer` first and observe planner-only state before restoring apply authority;
- keep `v7-users-autoswitch.timer` held until a separate explicit approval restores apply authority;
- if planner evidence shows pending non-candidate movement, apply restore becomes a separate autoswitch recovery operation, not a canary cleanup step;
- no future canary is allowed under the old "restore planner/apply timers together" model.

## Block E9.3.2 Staged Restore Governance Packet

```text
staged_restore_model_created=true
recommended_restore_model=planner_first_apply_by_separate_approval
apply_restore_requires_separate_approval=true
future_canary_restore_sequence_safe=false
second_canary_readiness=CONDITIONAL_AFTER_STAGED_RESTORE_APPROVAL
execution_allowed_now=false
```

Updated gate:

- canary execution is still forbidden now;
- a future canary may be discussed only with staged restore included in the approval packet;
- apply authority restore must not be bundled with canary cleanup;
- the next live step should be a staged-restore rehearsal/approval flow, not another canary.
# E9.3.3 Staged Restore Gate

E9.3.3 proved planner-only restore can be performed without user movement, routing drift, or registry drift.

However, planner-only observation also exposed pending non-canary autoswitch moves while apply was held. Therefore future canary execution is still not a clean GO until apply restore governance is explicitly approved.

Updated gate:

```text
planner_only_restore_rehearsal=PASS
apply_restore_approval=REQUIRED
canary_execution_allowed_now=false
current_canary_status=CONDITIONAL_STAGED_RESTORE_PROVEN_APPLY_APPROVAL_REQUIRED
```

Hard blocker remains:

```text
v7-users-autoswitch.timer_restore_without_separate_approval
```

## Block E9.3.4 Autoswitch Apply Restore Approval Packet

E9.3.4 was read-only. It did not restore apply authority.

Current evidence:

```text
v7-autoswitch-planner.timer=active
v7-users-autoswitch.timer=inactive
pending_moves_visible=false
selected_moves=0
V7_RECONCILE_RESULT=OK
V7_USER_ROUTE_CHECK=OK
V7_KILLSWITCH_CHECK=OK
V7_PROVISIONING_RECONCILE_CHECK=OK
```

Updated gate:

```text
apply_restore_approval_status=CONDITIONAL
canary_execution_allowed_now=false
execution_allowed_now=false
```

No new canary is allowed until apply restore is handled as a separate stage. The current recommended next step is a bounded E9.3.5 apply-restore approval/execution block with a final planner-only sample and explicit operator approval.

## Block E9.3.7 Autoswitch Service-Signal Policy Design

Current status after E9.3.7:

```text
current_canary_status=NO-GO_APPLY_RESTORE_POLICY_REFINEMENT_REQUIRED
apply_restore_safe_under_current_policy=false
apply_should_remain_held=true
execution_allowed_now=false
```

Hard blockers:

- autoswitch apply timer is still held;
- current autoswitch policy can make egress globally ineligible from a single non-Telegram service failure;
- broad failover candidates can be generated from transient service state;
- no code-level policy refinement has been deployed.

Conditional path:

- a future apply restore can be considered only with a fresh final planner-only sample showing `selected_moves=0`; or
- with exact operator approval for a known bounded movement list; or
- after a policy fix adds persistence/confidence thresholds before global ineligibility.

No canary execution is allowed in this state.

## Block E9.3.8 Repo Policy Fix

E9.3.8 implemented the transient service signal policy repo-side only.

Current status:

```text
repo_policy_fix_implemented=true
runtime_policy_deployed=false
current_canary_status=NO-GO_REPO_POLICY_FIX_READY_RUNTIME_DEPLOY_REQUIRED
execution_allowed_now=false
```

Canary remains blocked until:

- runtime `v7-users-autoswitch` is updated under separate approval;
- post-deploy planner dry-run proves the E9.3.5 broad failover class is suppressed;
- apply restore governance is resolved or explicitly kept out of the canary boundary.

## Block E9.3.9 Runtime Policy Deploy

E9.3.9 deployed the repo-fixed autoswitch policy to runtime as a single approved file update.

Current status:

```text
runtime_policy_deployed=true
runtime_policy_hash=d07a045bd9ad8470e872d4774ac776733a2051b36ec60507a6baf6ca9bab454b
apply_timer_remained_held=true
planner_only_selected_moves=[]
planner_only_apply_result=no_selected_moves
users.registry_changed=false
egress.registry_changed=false
current_canary_status=NO-GO_RUNTIME_POLICY_DEPLOYED_APPLY_RESTORE_PROOF_REQUIRED
execution_allowed_now=false
```

This removes the `runtime_policy_deploy_required` blocker, but it does not approve canary or apply restore.

Remaining blockers:

- `v7-users-autoswitch.timer` is still held and must not be restored without separate approval;
- apply restore needs a fresh final planner-only sample under the deployed policy;
- future canary attribution remains blocked until autoswitch apply restore is separately governed or explicitly out of scope.

## Block E9.4 Apply Restore After Policy Fix

E9.4 did not restore apply authority because the final planner-only gate returned non-zero selected moves.

```text
apply_restore_executed=false
apply_restore_aborted=true
final_planner_selected_moves=3
selected_moves=10.7.0.5:1->vless,10.0.0.2:1->vless,10.0.0.3:1->vless
actual_movements_count=0
current_canary_status=NO-GO_APPLY_RESTORE_ABORTED_AFTER_POLICY_FIX
execution_allowed_now=false
```

Canary remains NO-GO. The next blocker is no longer runtime policy deployment; it is post-policy planner selection. The selected moves must be explained or explicitly approved as a separate autoswitch recovery stage before any future canary can be attributed cleanly.

## Block E9.4.1 Post-Policy Root-Cause Classification

E9.4.1 classified the E9.4 post-policy planner selection:

```text
post_policy_egress_1_root_cause=telegram_required_telegram_down_14s
root_cause_classification=TELEGRAM_HARD_BLOCK
selected_moves_count=3
candidate_moves_count=16
policy_fix_incomplete=false
current_canary_status=NO-GO_POST_POLICY_TELEGRAM_HARD_BLOCK_CLASSIFIED_APPLY_HELD
execution_allowed_now=false
```

Current GO/NO-GO:

- canary remains NO-GO;
- apply restore remains NO-GO without a fresh final planner-only gate;
- if the next gate returns `selected_moves=0`, a bounded apply restore retry can be considered;
- if the next gate returns non-zero moves, those moves require a separate exact approval packet;
- Telegram hard-block grace/confirmation is a future policy-design question, not an implicit approval.

## Block E9.4.4 Delayed Restore Root Cause

E9.4.4 classified delayed movement after the clean E9.4.2 apply restore:

```text
delayed_movement_root_cause=telegram_hard_block_recurred_after_clean_gate
root_cause_classification=MIXED_TELEGRAM_HARD_BLOCK_RECURRENCE_AND_CLEAN_GATE_WINDOW_TOO_SHORT
moved_users=10.7.0.5,10.0.0.2,10.0.0.3
movement_count=3
restore_governance_live_proven=false
apply_restore_model_safe=false
```

Current canary status:

```text
current_canary_status=NO-GO_DELAYED_RESTORE_ROOT_CAUSE_CLASSIFIED_RESTORE_GATE_INSUFFICIENT
next_canary_readiness=NO-GO
execution_allowed_now=false
```

New canary blocker:

- restore governance must include a delayed-settle gate across multiple apply timer periods;
- immediate post-restore no-op is no longer sufficient evidence;
- canary blast radius must distinguish canary-window movement from post-restore autoswitch recovery movement.

## Block E9.4.5 Restore Settle Gate Design

E9.4.5 creates the formal restore settle gate and repo-side read-only checker.

```text
restore_settle_gate_rules_created=true
restore_settle_checker_created=true
tool=tools/v7-restore-settle-gate
pre_restore_required_samples=3
required_apply_timer_intervals=2
post_restore_settle_required=true
current_restore_settle_status=NO-GO
next_canary_readiness=NO-GO
execution_allowed_now=false
```

Updated GO requirement:

- pre-restore gate must show `selected_moves=0` across at least three consecutive samples;
- those samples must span at least two full apply timer intervals;
- Telegram hard-block must remain false throughout;
- egress `1` must remain eligible throughout if users are on it;
- registry hashes and runtime checkers must remain stable;
- after apply restore, delayed settle must pass before canary planning resumes.

Current evidence remains NO-GO because E9.4.4 evidence contains `TELEGRAM_DOWN_14S`, `telegram_required_telegram_down_14s`, and `selected_moves=3`.

## Block E9.4.6 Fresh Restore Settle Observation

E9.4.6 collected fresh live read-only evidence and normalized it through `tools/v7-restore-settle-gate`.

```text
fresh_restore_settle_observation_executed=true
current_restore_settle_status=GO
samples_count=3
samples_span_seconds=68
apply_timer_intervals_covered=3.4
selected_moves_all_zero=true
telegram_hard_blocked_seen=false
egress_1_eligible_all_samples=true
users.registry_stable=true
egress.registry_stable=true
runtime_checks_ok=true
new_delayed_movements_observed=false
restore_governance_live_proven=true
next_canary_readiness=CONDITIONAL
execution_allowed_now=false
```

Canary remains blocked from execution. The next safe step is a fresh approval packet or target selection refresh, because runtime registry truth changed during earlier timer-driven autoswitch recovery.
## Block E10 Fresh Second Canary Approval Packet

E10 rebuilt second-canary approval from current runtime truth after restore-settle governance was proven live.

```text
restore_settle_gate_status=GO
candidate_user=10.7.0.11
selected_target=NONE
target_status=NO-GO
waiver_required=true
waiver_acceptable=false
rollback_feasible=true
second_canary_approval_status=NO-GO
current_canary_status=NO-GO_E10_FRESH_SECOND_CANARY_PACKET_NO_CLEAN_TARGET
execution_allowed_now=false
```

Facts:

- restore governance is currently clean enough for approval-packet planning only;
- stale E9.2/E9.3 second-canary packets are invalid because `10.7.0.14` is now on egress `1`;
- target `1` is occupied by `10.7.0.14` and `10.7.0.15`;
- `awg0` and `awg3` are zero-user and diagnose OK, but lack Direct/RU and Trusted RU route-class exclusions required by strict E10 target rules;
- OpenVPN and WireGuard are zero-user but diagnose `SUSPECT`;
- E10 accepts no waiver.

Canary execution remains forbidden until a new explicit approval packet selects one concrete target with `GO` or an explicitly accepted waiver.

## Block E10.1 Zero-User Target Remediation Approval Packet

E10.1 did not approve canary execution. It approved only the planning path for a future bounded metadata remediation block.

```text
remediation_candidate=awg0
remediation_approval_status=GO
expected_target_after_remediation=awg0
expected_second_canary_readiness_after_remediation=GO_if_fresh_checks_remain_OK
mutation_required=true
mutation_scope=/opt/v7/egress/state/egress.registry awg0 metadata only
policy_apply_required=false
direct_ru_risk=LOW_METADATA_EXCLUSION_ONLY
trusted_ru_risk=LOW_METADATA_EXCLUSION_ONLY_WITH_STALE_STATE_AWARENESS
kill_switch_risk=LOW_RECHECK_REQUIRED_AFTER_MUTATION
current_canary_status=CONDITIONAL_E10_1_TARGET_REMEDIATION_APPROVED_METADATA_BLOCK_REQUIRED
execution_allowed_now=false
```

Hard boundary:

- no egress metadata was changed in E10.1;
- no Direct/RU state was changed;
- no Trusted RU diagnostic or decision state was refreshed;
- no policy apply was run;
- no route, ip rule, nft, user registry, or datapath mutation was performed.

The next valid step is a separate bounded mutation packet for `awg0` egress metadata only.

## Block E10.2 Bounded AWG0 Target Metadata Remediation

E10.2 was authorized to mutate only `awg0` metadata in `/opt/v7/egress/state/egress.registry`, but the block aborted before backup and mutation because fresh runtime truth invalidated the E10.1 zero-user assumption.

```text
metadata_mutation_executed=false
metadata_mutation_aborted=true
abort_reason=awg0_no_longer_zero_user
backup_path=NOT_CREATED_ABORTED_BEFORE_MUTATION
target_readiness_after=NO-GO
selected_target_after=NONE
restore_settle_gate_status=GO
second_canary_readiness_after=NO-GO
current_canary_status=NO-GO_E10_2_AWG0_METADATA_REMEDIATION_ABORTED_TARGET_OCCUPIED
execution_allowed_now=false
```

Fresh E10.2 facts:

- `awg0` is occupied by `10.0.0.2`, `10.0.0.6`, `10.7.0.3`, and `10.7.0.4`;
- `awg0` load-state agrees with registry occupancy: `awg0_users=4`, `load_status=HARD_FULL`;
- `awg3` is also occupied by `10.0.0.3` and `10.7.0.2`;
- target `1` is occupied by `10.7.0.14` and `10.7.0.15`;
- OpenVPN/WireGuard remain zero-user but diagnose `SUSPECT`;
- restore-settle gate remains `GO`, but no clean second-canary target exists.

No metadata was changed. No backup was created because the abort happened in Phase 1 before any runtime write was permitted.

The next valid step is a fresh target-pool truth refresh and a new remediation/approval packet based on current occupancy.

## Block E10.3 Fresh Target Pool Truth Refresh

E10.3 performed a read-only refresh after the E10.2 abort. It did not repeat metadata mutation and did not move users.

Fresh E10.3 status:

```text
restore_settle_gate_status=GO
clean_zero_user_target_exists=false
best_current_target_path=E_PAUSE_CANARY_AND_FOCUS_ON_TARGET_POOL_GOVERNANCE_OR_CAPACITY
second_canary_readiness=NO-GO
current_canary_status=NO-GO_E10_3_NO_CLEAN_ZERO_USER_TARGET
execution_allowed_now=false
```

Current target truth:

- `target 1` is occupied by six users and is not a clean canary target.
- `awg0` and `awg3` are zero-user again, but both fail target quality floor and still lack Direct/RU + Trusted RU exclusions.
- OpenVPN is zero-user but `SUSPECT` and below quality floor.
- WireGuard is zero-user and quality OK, but `SUSPECT`; it needs a separate stale-handshake waiver packet before any use.

Canary execution remains forbidden.

## Block E10.4 Target Pool Governance Strategy

E10.4 is strategy/design only. It created a target reservation policy and selected the safest next planning path.

```text
clean_zero_user_target_exists=false
target_pool_blocker=no_clean_reserved_zero_user_target
best_strategy=WIREGUARD_DIAGNOSE_THEN_RESERVE_OR_WAIVE
recommended_next_block=E10.5_WIREGUARD_STALE_HANDSHAKE_DIAGNOSTIC_AND_RESERVATION_FEASIBILITY_PACKET
dedicated_canary_target_needed=true
wireguard_waiver_path_recommended=true
awg_quality_remediation_needed=true
target_reservation_policy_created=true
second_canary_readiness=NO-GO
current_canary_status=NO-GO_E10_4_TARGET_POOL_GOVERNANCE_REQUIRED
execution_allowed_now=false
```

No canary may execute from E10.4. The next valid step is a read-only WireGuard stale-handshake diagnosis and reservation feasibility packet, or a separate dedicated canary/test egress planning block.

## Block E11.2 WireGuard Reservation Approval Packet

E11.2 confirms WireGuard as the next reservation candidate, but keeps canary
execution blocked:

```text
wireguard_semantics_classification=DIAGNOSE_SEMANTICS_TOO_STRICT
wireguard_quality_ok=true
wireguard_zero_user=true
reservation_feasible=true
reservation_requires_mutation=true
waiver_required=true
waiver_status=waiver_conditional
expected_second_canary_readiness=CONDITIONAL_AFTER_RESERVATION_WITH_WAIVER_OR_GO_AFTER_DIAGNOSE_FIX
current_canary_status=NO-GO_E11_2_WIREGUARD_RESERVATION_APPROVAL_READY
execution_allowed_now=false
```

Next GO condition is not canary. It is a separate bounded metadata mutation
packet for WireGuard reservation, followed by diagnose semantics fix or an
explicit stale-handshake waiver in a fresh second-canary approval packet.

## E11.4 WireGuard Diagnose Semantics Decision

Current canary status after E11.4:

```text
current_canary_status=NO-GO_E11_4_DIAGNOSE_FIX_REQUIRED_WAIVER_ACCEPTABLE
wireguard_root_cause_classification=DIAGNOSE_REFRESH_BUG
fix_required=true
waiver_acceptable=true
best_strategy=FIX_FIRST_WITH_WAIVER_AS_FALLBACK
recommended_next_block=E11.5_BOUNDED_WIREGUARD_DIAGNOSE_SEMANTICS_FIX_PACKET
execution_allowed_now=false
```

The next canary is not executable now. The cleanest path is a bounded diagnose
semantics fix packet for WireGuard handshake freshness. A stale-handshake waiver
can be prepared only as a conditional fallback and must not be treated as clean
target `GO`.

## E11.5 WireGuard Diagnose Fix Packet Result

```text
repo_diagnose_fix_implemented=true
diagnose_fix_executed=false
runtime_deploy_executed=false
wireguard_diagnose_after=SUSPECT_UNCHANGED_RUNTIME
target_readiness_after=NO-GO_RUNTIME_UNCHANGED_GO_IN_REPO_FIXED_FIXTURE
second_canary_readiness_after=NO-GO_RUNTIME_UNCHANGED_GO_IN_REPO_FIXED_FIXTURE
current_canary_status=NO-GO_E11_5_REPO_FIX_READY_RUNTIME_DEPLOY_REQUIRED
recommended_next_block=E11.6_BOUNDED_RUNTIME_DEPLOY_OF_WIREGUARD_DIAGNOSE_FIX
execution_allowed_now=false
```

No canary is allowed after E11.5. The next step is a bounded runtime deploy of
the diagnose tooling only, followed by fresh target readiness and runtime
checker verification.

## E11.6 Runtime Diagnose Fix Deploy Result

```text
diagnose_fix_deployed=true
wireguard_diagnose_after=OK
wireguard_blocker_after=NONE
awg_regression_observed=false
target_readiness_after=GO
selected_target_after=wireguard-1779454504-c43409
waiver_required_after=false
second_canary_readiness_after=GO
current_canary_status=CONDITIONAL_E11_6_WIREGUARD_DIAGNOSE_FIXED_FRESH_CANARY_PACKET_REQUIRED
execution_allowed_now=false
```

Canary execution remains forbidden until a fresh approval packet is generated
against current runtime truth. The stale `vless -> target` packets must not be
reused.

## E11.7 Fresh Packet After Diagnose Fix

Fresh runtime truth blocked the second-canary packet:

```text
target_readiness_status=NO-GO
restore_settle_gate_status=GO
candidate_user=NONE
selected_target=NONE
wireguard_diagnose=OK
wireguard_zero_user=false
wireguard_users=12
approval_status=NO-GO
recommended_next_block=E11.8_TARGET_POOL_RECONCILIATION_OR_WIREGUARD_RESERVATION_ENFORCEMENT_PACKET
execution_allowed_now=false
```

The blocker is no longer stale-handshake diagnose. The blocker is that the
reserved WireGuard target is currently occupied by production users.

## E11.8 Reservation Enforcement Fix

```text
reservation_enforcement_root_cause=canary_reserved_metadata_present_but_not_consumed_by_v7_users_autoswitch
root_cause_classification=MIXED_RESERVATION_METADATA_NOT_CONSUMED_PLANNER_IGNORES_RESERVATION_APPLY_TRUSTS_PLANNER_EXISTING_USERS_NOT_DRAINED
runtime_fix_executed=true
wireguard_users_after=10
reservation_enforced=true
target_readiness_after=NO-GO
selected_target_after=NONE
second_canary_readiness_after=NO-GO_RESERVED_WIREGUARD_USERS_REQUIRE_DRAIN_PACKET
execution_allowed_now=false
```

E11.8 closed the new-assignment gap: production autoswitch now blocks
`canary_reserved` targets as destinations. It did not drain existing WireGuard
users. No canary may execute until a separate bounded drain approval packet
returns WireGuard to zero-user state and target readiness is refreshed.

## E11.10 Closeout - Second Canary Lifecycle Closed

E11.10 was closed by a bounded live closeout block. The canary had already
executed:

```text
candidate_user=10.7.0.3
forward_from=awg0
forward_to=wireguard-1779454504-c43409
```

The closeout found `10.7.0.3` still on WireGuard. Because pre-rollback settle
samples B/C showed `selected_moves=1`, the keep decision was rejected and the
default rollback was executed:

```text
rollback_executed=true
rollback_target=awg0
only_one_user_moved=true
restore_settle_gate_status=GO
delayed_movements_observed=false
runtime_checks_ok=true
second_canary_lifecycle_status=CLOSED_ROLLED_BACK_AND_SETTLED
execution_allowed_now=false
```

No new canary was performed by the closeout. Future work must start from a
post-E11.10 governance review, not by reusing the E11.10 live window.

## E11.11 Post-Closeout Governance Review

E11.11 performed a full post-E11.10 governance and hardening review. It did not
execute a canary, user movement, routing mutation, kill-switch mutation, proxy
apply, Direct/RU mutation, or manual autoswitch apply.

```text
governance_review_completed=true
lifecycle_stable=true
reservation_enforcement_complete=true
delayed_movement_protection_complete=true
mini_cohort_readiness=CONDITIONAL
execution_allowed_now=false
```

The current safe next stage is an approval packet for a two-user mini-cohort.
Execution remains forbidden until that packet names exact users, forward target,
rollback targets, hold windows, route checks, delayed monitoring, and rollback
criteria. A three-user cohort is not justified while the reserved WireGuard
target has `hard_limit=2`.

## E11.12 Two-User Mini-Cohort Approval Packet

E11.12 created the first mini-cohort approval packet. It did not execute a
cohort, canary, user movement, routing mutation, kill-switch mutation, or manual
autoswitch apply.

```text
mini_cohort_readiness=CONDITIONAL
selected_candidates=10.7.0.11,10.7.0.12
selected_target=wireguard-1779454504-c43409
target_capacity_safe=true
restore_settle_gate_status=GO
rollback_feasible=true
blast_radius=2_users_max
approval_status=CONDITIONAL
execution_allowed_now=false
recommended_next_block=E11.13_TWO_USER_MINI_COHORT_EXECUTION_PACKET_WITH_FRESH_PRECHECKS
```

The conditional status is intentional: WireGuard has `soft_limit=1` and
`hard_limit=2`, so exactly two users are allowed for the first mini-cohort and a
third user is forbidden. Future execution must re-run fresh pre-checks because
runtime drift was observed during E11.12 before the final settle samples proved
the latest state stable.

## E11.13 Two-User Mini-Cohort Execution

E11.13 executed the approved two-user mini-cohort and rolled both users back.
The WireGuard cohort window itself was clean, but the full restore lifecycle was
not clean because restoring the apply timer caused delayed non-cohort movement.

```text
mini_cohort_executed=true
moved_users=10.7.0.11,10.7.0.12
rollback_executed=true
rollback_targets=1,1
wireguard_users_after=0
restore_settle_gate_status=GO
delayed_movements_observed=true
delayed_non_cohort_users=10.7.0.9,10.7.0.10,10.7.0.13
apply_timer_reheld_for_containment=true
mini_cohort_lifecycle_status=EXECUTED_ROLLED_BACK_DELAYED_APPLY_MOVEMENT_OBSERVED_CONTAINED
next_stage_readiness=NO_GO_FOR_LARGER_COHORT_APPLY_RESTORE_ROOT_CAUSE_REQUIRED
recommended_next_block=E11.14_DELAYED_APPLY_RESTORE_MOVEMENT_ROOT_CAUSE_AND_APPLY_TIMER_GOVERNANCE_FIX
execution_allowed_now=false
```

No larger cohort is allowed until the delayed apply-restore movement is root
caused and the restore lifecycle is hardened.
## E11.14 Status

current_status=NO-GO_FOR_LARGER_COHORT
reason=E11.13 apply timer restore caused delayed non-cohort movement; E11.14 deployed bounded restore-barrier mitigation but promotion requires separate apply-restore rehearsal.

Facts:

- Second canary and two-user mini-cohort movement/rollback were clean.
- Delayed movement after apply restore was real and timer-driven.
- E11.14 root cause: governance gap plus delayed service-signal recompute.
- Runtime fix: restore-barrier failover quarantine; final v2 dry-run shows `selected_moves=0` while the barrier is active.
- Apply timer remains held.

Next allowed block:

recommended_next_block=E11.15_APPLY_RESTORE_BARRIER_REHEARSAL_AND_GENERATION_GOVERNANCE
execution_allowed_now=false

## E11.15 Apply-Restore Barrier Rehearsal

E11.15 restored the apply timer only inside a bounded restore-barrier rehearsal,
then returned it to hold. No canary, cohort execution, user movement, routing
mutation, kill-switch mutation, or manual autoswitch apply was performed.

```text
barrier_rehearsal_executed=true
apply_timer_restored=true
apply_timer_final_state=held
user_movement_observed=false
delayed_non_cohort_movement_prevented=true
barrier_consumed_by_apply=true
selected_moves_during_rehearsal=0
barrier_ttl_status=ACTIVE_NOT_EXPIRED_NOT_OBSERVED_POST_TTL
runtime_checks_ok=true
mini_cohort_readiness_after=CONDITIONAL
larger_cohort_readiness_after=NO-GO
recommended_next_block=E11.16_POST_TTL_BARRIER_EXPIRY_AND_GENERATION_TOKEN_GOVERNANCE
execution_allowed_now=false
```

The barrier passed the bounded apply-timer rehearsal, but post-TTL behavior was
not observed. Mini-cohort promotion is conditional only; unattended apply timer
operation and any larger cohort remain blocked.

## E11.16 Post-TTL Generation Governance

E11.16 proved that barrier expiry alone was not safe: a counterfactual
expired-barrier dry-run on copied live state selected 3 failover moves before
the fix. A bounded generation-clearance fix was deployed so expired barriers
fail closed until explicit governance clearance.

```text
post_ttl_behavior_safe=true
barrier_expiry_safe=true
generation_governance_required=true
generation_fix_executed=true
apply_timer_final_state=held
runtime_checks_ok=true
mini_cohort_readiness_after=CONDITIONAL
larger_cohort_readiness_after=NO-GO
unattended_apply_lifecycle_status=CONDITIONAL_WITH_GENERATION_GOVERNANCE
execution_allowed_now=false
```

## E11.17 Generation Clearance Rehearsal

E11.17 proved that expired uncleared restore barrier behavior is fail-closed
under the live apply timer, and that explicit clearance must be bounded by a
movement budget. A full copied-state rehearsal showed plain clearance would
produce `selected_moves=3`; the deployed E11.17 guard then allowed a live
clearance rehearsal with `clearance_max_selected_moves=0`.

```text
fail_closed_rehearsal_clean=true
generation_clearance_consumed=true
selected_moves_after_clearance=0
clearance_selected_moves_before_guard=3
delayed_movement_after_clearance_observed=false
apply_timer_final_state=held
runtime_checks_ok=true
mini_cohort_readiness_after=GO
larger_cohort_readiness_after=NO-GO
execution_allowed_now=false
```

Mini-cohort GO applies only to a separately approved bounded two-user lifecycle.
Unbounded apply clearance remains forbidden.

## E11.18 Two-User Promotion-Clean Approval

E11.18 performed a read-only promotion-clean review of the already executed
two-user mini-cohort lifecycle. The lifecycle is now promotion-clean only under
the exact bounded governance shape proven by E11.13-E11.17.

```text
two_user_promotion_clean=true
generation_governance_complete=true
delayed_movement_protection_complete=true
larger_cohort_blocked=true
operational_maturity_status=TWO_USER_PROMOTION_CLEAN_LARGER_COHORT_BLOCKED
recommended_next_block=E11.19_GENERATION_TOKEN_OR_NONZERO_BUDGET_REHEARSAL
execution_allowed_now=false
```

This is not execution approval. A larger cohort remains NO-GO.

## E12 Generation-Token Hardening And Nonzero Budget Rehearsal

E12 closed the nonzero-budget governance gap with immutable generation-token
ownership.

```text
immutable_generation_governance_required=true
immutable_generation_governance_implemented=true
nonzero_budget_rehearsal_safe=true
delayed_movement_observed=false
replay_resistance_complete=true
larger_cohort_readiness_after=CONDITIONAL_NO_GO
operational_maturity_status=BOUNDED_ORCHESTRATION_PRODUCTION_GRADE
execution_allowed_now=false
```

Nonzero clearance now requires `generation_token`,
`clearance_generation_id`, `approved_selected_moves_hash`, and bounded selected
move count. E12 authorizes the governance primitive only; it does not authorize
larger cohort execution.
