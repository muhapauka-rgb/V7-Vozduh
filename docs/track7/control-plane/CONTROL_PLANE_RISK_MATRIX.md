# Control Plane Risk Matrix

This matrix is governance only. It does not approve execution of mutation tools.

| Layer | Risk | Blast Radius | Rollback Clarity | Canary Allowed? |
|---|---|---|---|---|
| autoswitch apply timer | automated user movement through `v7-user-switch --apply` path | potentially many users over repeated timer runs | partial; depends on switch history and previous assignments | no, must be held first |
| health-loop autoswitch planner | `v7-health.service` invokes `v7-users-autoswitch` every 30 seconds without `--apply`; planner/load/reconnect state may still write | control-plane attribution and future autoswitch decisions; no direct user movement observed without `--apply` | restore is explicit but entangled with service ordering and possible `v7-routing-sync.service` relationship | no, must be held or split first |
| proposed planner split | draft `v7-autoswitch-planner.timer/service` separates non-apply planner from health | deployment-scoped until approved; after deploy, planner can be independently held | rollback documented in E8.3 migration plan but not live-proven | no canary until deploy and post-split mapping succeed |
| deployed autoswitch planner | E8.4 `v7-autoswitch-planner.timer/service` owns non-apply planner authority | planner/load/reconnect state only unless tool behavior changes | hold/restore via planner timer/service; E8.5 proved temporary hold/restored timers | conditional only inside approved quiet/canary window |
| admin/manual invocation | operator/API can invoke autoswitch dry-run/apply, user-switch, or routing-sync | one user to whole datapath depending on command | command-specific; requires manual evidence | no during rehearsal/canary window |
| sentinel-capable path | current unit uses `--no-autoswitch`, but alternate invocation can launch autoswitch | can become autoswitch apply authority if misinvoked | depends on invocation source | no unless verified no active autoswitch-capable sentinel |
| routing-sync | registry-wide route/rule mutation | all enabled users in `users.registry` | weak without full route/rule snapshot | no first mutation |
| user-switch | one user registry/assignment/route mutation | one user if autoswitch held and no routing-sync fallback | clear for switch-back to previous egress | conditional future canary only |
| Trusted RU | Gosuslugi-sensitive diagnostic/decision influence | route-class and downstream policy influence | unclear; state refresh/decision can be stale | no live refresh/decision in canary |
| policy apply | route/policy state and possible systemd/apply effects | route classes or broader runtime | partial, depends on policy backup/rollback | no |
| Direct/RU | route-class/domain mutation | route classes, possibly many users | partial; depends on domain/state backups | no |
| proxy runtime | proxy/public/runtime guard mutation | public ingress/proxy paths, possibly users | partial; rollback tools exist but are not fully proven | no |
| kill switch | leak guard rebuild/removal | whole datapath | high impact; rollback depends on prior ruleset | no during canary except emergency approval |
| rollback tools | restore configs/state from backups | target-dependent, can be broad | tool-specific; not universally proven | only as pre-approved rollback for named action |

## Current Canary Status

```text
CONDITIONAL
```

The only plausible future canary layer is `user-switch` for one named user. E8.5 proved the post-split quiet-window hold model. Canary remains blocked until reconcile `STABLE_FAIL` is classified or waived, target readiness is acceptable, and rollback readiness is explicit.

## E8.2 Quiet-Window Option Risk

| Option | Risk | Blast Radius | Restore Clarity | Recommendation |
|---|---|---|---|---|
| A: temporary hold `v7-health.service` plus autoswitch timer/service | pauses health/state summary loop and may interact with `v7-routing-sync.service` on restore | control-plane state freshness; datapath should continue if no route/rule mutation is triggered | conditional; explicit commands exist but restore-time routing-sync attribution must be accepted or ruled out | acceptable only with explicit operator approval for full-authority rehearsal |
| B: split health loop and autoswitch planner first | requires design/deploy and later verification | deployment-scoped, but improves future blast-radius boundaries | better after unit split rollback plan exists | preferred long-term path |

## E8.3 Split Design Status

```text
design_ready_for_deploy_approval=true
draft_units_created=true
deploy_performed=true
post_split_authority_mapping_done=true
current_canary_status=NO-GO
```

## E8.4 Runtime Split Status

```text
v7-health.service_health_only=true
planner_authority_separated=true
apply_authority_unchanged=true
rollback_performed=false
users_registry_changed=false
egress_registry_changed=false
user_movement_observed=false
routing_drift_observed=false
kill_switch_ok=true
user_route_check_ok=true
provisioning_reconcile_ok=true
reconcile_result_after_deploy=FAIL
quiet_window_verified=false
current_canary_status=NO-GO
```

## E8.5 Post-Split Quiet-Window Status

```text
v7-health_stayed_active=true
autoswitch_planner_held=true
autoswitch_apply_held=true
autoswitch_fully_quiet=true
users_registry_changed=false
egress_registry_changed=false
user_movement_observed=false
routing_drift_observed=false
reconcile_under_quiet=STABLE_FAIL
quiet_window_verified=true
restore_success=true
current_canary_status=CONDITIONAL
execution_allowed_now=False
```

Updated risk interpretation:

| Layer | E8.5 Status | Remaining Risk |
|---|---|---|
| autoswitch planner/apply hold | verified hold/restored | must be repeated inside any future canary window |
| health service | stayed active and health-only | must be rechecked before every quiet/canary window |
| reconcile | stable FAIL under quiet | must be classified before canary execution |
| user-switch | not executed | still requires separate one-user approval |
| routing-sync | not executed | remains forbidden as first live mutation |

## E8.6 Reconcile Classification Status

```text
reconcile_under_quiet_classification=CONFIRMED_FALSE_POSITIVE
failure_class=pipefail_grep_q_sigpipe
runtime_repair_needed_for_this_failure=false
checker_fix_recommended=true
bounded_canary_waiver_possible=true
current_canary_status=CONDITIONAL
execution_allowed_now=False
```

Updated matrix entry:

| Layer | E8.6 Status | Remaining Risk |
|---|---|---|
| `v7-reconcile-check` | confirmed false-positive for missing-rule checks | cannot be used as a hard canary gate until fixed or waived |
| route/rule runtime | actual rules and route reality OK in evidence | must be rechecked immediately before any one-user canary |
| canary approval | still not granted | requires separate approval and autoswitch hold window |

## E8.7 Checker Fix Status

```text
v7-reconcile-check_patched_repo=true
v7-reconcile-check_deployed_runtime=true
V7_RECONCILE_RESULT_after_fix=OK
runtime_repair_performed=false
runtime_mutation_scope=/usr/local/bin/v7-reconcile-check only
current_canary_status=CONDITIONAL
execution_allowed_now=False
```

Updated matrix entry:

| Layer | E8.7 Status | Remaining Risk |
|---|---|---|
| `v7-reconcile-check` | false-positive class fixed and deployed | must be rerun inside future quiet/canary window |
| canary readiness | reconcile blocker cleared | target readiness, autoswitch hold, rollback, and explicit approval still required |

## E8.8 One-User Canary Approval Packet

```text
candidate_user=10.7.0.15
current_egress=vless
target_egress=1
rollback_target=vless
approval_status=CONDITIONAL
execution_allowed_now=False
```

Updated matrix entry:

| Layer | E8.8 Status | Remaining Risk |
|---|---|---|
| user-switch canary | packet prepared for `10.7.0.15: vless -> 1` | live switch still forbidden until separate bounded approval |
| autoswitch planner/apply | must be held during canary window | active outside approved hold windows |
| target egress `1` | enabled, `GLOBAL_FAST`, current load summary OK | must be rechecked immediately before live canary |
| rollback | switch-back command prepared: `v7-user-switch 10.7.0.15 vless` | rollback itself is live mutation and needs observation authority |

## E9 First One-User Live Canary

```text
canary_executed=true
rollback_executed=true
candidate_user=10.7.0.15
forward_success=true
rollback_success=true
current_canary_status=SUCCESS_ROLLED_BACK
execution_allowed_now=False
```

Updated matrix entry:

| Layer | E9 Status | Remaining Risk |
|---|---|---|
| one-user `v7-user-switch` | live-proven for `10.7.0.15: vless -> 1 -> vless` | proof does not generalize automatically to other users or targets |
| quiet hold | worked during E9 canary window | must be repeated before any future canary |
| rollback | live-proven for `10.7.0.15 -> vless` | broader rollback remains unproven |
| routing-sync | not used | still forbidden as broad first mutation |
| autoswitch restore | timers restored and settle check OK | timers can resume movement after restore; future canaries need fresh hold |

## E9.1 Post-Canary Monitoring

```text
post_canary_monitoring_executed=true
delayed_side_effects_observed=false
current_canary_status=SUCCESS_ROLLED_BACK_MONITORED_STABLE
second_canary_readiness=CONDITIONAL
execution_allowed_now=False
```

Updated matrix entry:

| Layer | E9.1 Status | Remaining Risk |
|---|---|---|
| post-canary runtime | stable across baseline and 3 monitoring samples | observation window was short and does not prove long-term behavior |
| autoswitch post-restore | normal; no delayed movement observed | active timers can move users in future, so canary windows still need hold |
| second canary | conditionally discussable | requires new approval packet and fresh target/candidate evidence |
| target `1` | good candidate for second mechanics canary if still healthy | must be rechecked immediately before approval/execution |

## E9.2 Second Canary Approval Packet

```text
second_candidate_user=10.7.0.14
current_egress=vless
target_egress=1
approval_status=CONDITIONAL
execution_allowed_now=False
```

Updated matrix entry:

| Layer | E9.2 Status | Remaining Risk |
|---|---|---|
| second one-user canary | approval packet prepared for `10.7.0.14: vless -> 1` | execution still forbidden without separate E9.3 live approval |
| target `1` | interface up, diagnose OK, stability acceptable | load-state reports `1_users=1` and `SOFT_FULL`; needs explanation, clearance, or explicit one-user waiver |
| rollback | preview prepared for `10.7.0.14 -> vless` | not live-proven for this user yet |
| autoswitch planner/apply | hold model unchanged from E9 | must be held again during any future canary |
| routing-sync | not required | still forbidden |

## E9.2.1 Target 1 Load-State Truth

```text
target_1_load_state_classification=REAL_HIDDEN_LOAD
target_1_ready_for_E9_3=false
execution_allowed_now=False
```

## E9.4.2 Fresh Apply Restore Retry

```text
apply_restore_executed=true
apply_restore_aborted=false
final_planner_selected_moves=0
actual_movements_count=0
restore_verdict=CLEAN_RESTORE
autoswitch_recovery_bounded=true
execution_allowed_now=False
```

Updated matrix entry:

| Layer | E9.4.2 Status | Remaining Risk |
|---|---|---|
| autoswitch apply timer | restored cleanly after fresh zero-move gate | future restore still requires fresh final planner gate |
| autoswitch policy | runtime fix avoided broad Instagram-triggered failover; transient Telegram hard-block was absent at restore gate | Telegram can still transiently hard-block and must be sampled immediately before restore/canary |
| autoswitch recovery | timer-driven runs produced `selected_moves=[]` and no registry/routing mutation | recovery is proven for this state, not for arbitrary future planner state |

## E11.3 WireGuard Reservation Metadata Mutation

```text
reservation_mutation_executed=true
runtime_mutation_scope=/opt/v7/egress/state/egress.registry WireGuard row only
rollback_performed=false
wireguard_reserved_after=true
wireguard_users_after=0
users.registry_changed=false
unrelated_egress_rows_changed=false
target_readiness_after=NO-GO
second_canary_readiness_after=NO-GO
execution_allowed_now=false
```

## E11.16 Post-TTL Generation Governance Risk

| Risk | Status | Evidence | Mitigation | Disposition |
| --- | --- | --- | --- | --- |
| Barrier expiry re-enables delayed failover | `PROVEN_PRE_FIX` | Counterfactual expired-barrier dry-run selected 3 moves | Expired barrier now fails closed | `FIXED_BOUNDED` |
| TTL treated as authorization | `FIXED` | New restore barrier fields include `expired`, `cleared`, `post_ttl_blocking`, `failover_quarantine` | Require explicit clearance marker | `CONTROLLED` |
| Runtime user movement during fix | `NOT_OBSERVED` | users hash stable, switch-history count `2698` | No apply/user-switch used | `CLOSED` |
| Larger cohort promotion | `BLOCKED` | Full generation-token clearance rehearsal not yet run | Separate E11.17 block | `NO-GO` |

## E11.17 Generation Clearance Risk

| Risk | Status | Evidence | Mitigation | Disposition |
| --- | --- | --- | --- | --- |
| Plain clearance reopens fresh failover recompute | `FIXED_FOR_BOUNDED_CLEARANCE` | Full copied-state clearance produced `selected_moves=3` before budget guard | Require `clearance_max_selected_moves` for governed clearance | `UNBOUNDED_CLEARANCE_FORBIDDEN` |
| Expired uncleared barrier leaks movement | `NOT_OBSERVED` | Live apply-timer fail-closed rehearsal kept `selected_moves=0`, hash stable, switch-history `2698` | Keep fail-closed post-TTL barrier | `CLOSED_FOR_REHEARSAL` |
| Clearance budget ignored by apply | `NOT_OBSERVED` | Live sample E had `clearance_selected_moves_before_guard=3`, `clearance_budget_exceeded=true`, final `selected_moves=0` | Budget guard in `v7-users-autoswitch` | `CONTROLLED` |
| Larger cohort after generation rehearsal | `BLOCKED` | Live pressure still exists; unbounded clearance remains forbidden | Separate approval/design block required | `NO-GO` |

## E11.18 Promotion-Clean Decision Risk

| Risk | Status | Evidence | Mitigation | Disposition |
| --- | --- | --- | --- | --- |
| Two-user lifecycle still not bounded | `CLOSED` | E11.13 movement/rollback clean; E11.14-E11.17 closed delayed apply surface | Exact lifecycle gates documented | `TWO_USER_PROMOTION_CLEAN` |
| Selected-move budget insufficient | `CONTROLLED_FOR_ZERO_BUDGET` | Current copied-state pressure has `candidate_moves_total=9`, but `selected_moves=0` with budget guard | Keep zero budget for restore validation | `NONZERO_BUDGET_UNPROVEN` |
| Hidden delayed movement path | `NOT_OBSERVED` | Switch-history count stable at `2698`, hidden scan clean, runtime checkers OK | Continue delayed monitoring | `MONITOR` |
| Larger cohort pressure | `BLOCKING` | WireGuard hard limit `2`; no nonzero generation budget proof | E11.19 generation-token/nonzero-budget rehearsal | `NO-GO` |

## E11.11 Post-Closeout Governance Risk Update

| Risk | E11.11 status | Residual action |
| --- | --- | --- |
| Historical fixture mistaken for live truth | `HARDENED` | Readiness and restore-settle defaults now prefer E11.11/E11.10 evidence |
| Stale quality/interface state false NO-GO | `HARDENED` | Readiness parses `egress-quality-summary.json` and diagnose handshake detail |
| Reservation bypass through autoswitch | `CONTROLLED` | Planner/apply/failover/rebalance block `canary_reserved` destinations |
| Manual privileged movement bypass | `RESIDUAL_GOVERNED_RISK` | Require exact approved movement manifest |
| Delayed post-restore movement | `CONTROLLED_FOR_ONE_USER` | Keep delayed monitoring mandatory for cohort |
| Mini-cohort over target capacity | `BLOCKING_UNLESS_BOUNDED` | First cohort cap is two users while WireGuard `hard_limit=2` |
| Runtime/repo lineage partial | `RESIDUAL_OPERATIONAL_RISK` | Keep release lineage work separate from cohort execution |

```text
lifecycle_stable=true
mini_cohort_readiness=CONDITIONAL
execution_allowed_now=false
```

Updated matrix entry:

| Layer | E11.3 Status | Remaining Risk |
|---|---|---|
| WireGuard reservation metadata | applied to WireGuard row only with timestamped backup | autoswitch/readiness semantics must continue to honor reservation metadata |
| user movement | none by this block; `users.registry` hash unchanged during mutation transaction | surrounding timer-driven autoswitch movement is external runtime context and must be separated from metadata mutation attribution |
| target readiness | still `NO-GO` under strict checker | diagnose `SUSPECT` / stale-handshake semantics or waiver remains unresolved |
| canary readiness | still `NO-GO` | next step is diagnose semantics fix or stale-handshake waiver approval packet |
| canary execution | not performed and not authorized | new canary approval packet still required |

## E9.3.5 Apply Restore Gate

```text
apply_restore_executed=false
apply_restore_aborted=true
final_planner_selected_moves=3
final_planner_candidate_moves_total=15
actual_movements_count=0
execution_allowed_now=false
```

Updated matrix entry:

| Layer | E9.3.5 Status | Remaining Risk |
|---|---|---|
| autoswitch apply restore | aborted before timer start because final planner sample showed 3 selected moves and 15 candidate moves | apply authority remains held; production autoswitch recovery is not restored/proven |
| planner-only gate | worked as intended and prevented unapproved movement | planner decisions are volatile and must be sampled immediately before any apply restore |
| egress `1` eligibility | planner marked current egress `1` ineligible and recommended `vless` failover | root cause needs separate read-only analysis before approving apply restore |
| canary governance | no canary was executed in E9.3.5 | canary remains blocked until apply restore governance is resolved |

## E9.3.6 Autoswitch Root Cause

```text
root_cause=service_instagram_failed
classification=MIXED_TRANSIENT_SERVICE_SIGNAL_AND_EXPECTED_FAILOVER_BEHAVIOR
candidate_moves=15
selected_moves=3
apply_restore_safe_now=false
```

Updated matrix entry:

| Layer | E9.3.6 Status | Remaining Risk |
|---|---|---|
| service signal gating | `service_instagram_failed` can hard-block current egress `1` | transient service failures can create broad failover candidates |
| max failover limiter | capped selected moves to 3 | repeated timer runs could continue movement if signal persists |
| apply restore | remains held | requires zero selected moves or explicit accepted movement list |
| autoswitch policy | behavior is expected by current code | may be too aggressive for restore-after-canary attribution |

Updated matrix entry:

| Layer | E9.2.1 Status | Remaining Risk |
|---|---|---|
| target `1` | real user `10.7.0.5` assigned; table `1003` uses `v7e356a192b79` | not a clean second-canary target while occupied |
| load calculator | no bug detected; `v7-egress-load` counts `users.registry current=1` | static and dynamic load semantics differ (`SOFT_FULL` vs dynamic `OK`) |
| second candidate | `10.7.0.14` still `vless`, table `1012`, route OK | target must be changed or refreshed |
| E9.3 readiness | blocked for target `1` | requires target-selection refresh or explicit waiver |

## E9.2.2 Target Selection Refresh

```text
selected_target=NONE
approval_status=NO-GO
execution_allowed_now=False
```

Updated matrix entry:

| Layer | E9.2.2 Status | Remaining Risk |
|---|---|---|
| candidate `10.7.0.14` | still valid on `vless`, table `1012` | target unavailable |
| target `1` | occupied by `10.7.0.5` | not clean for second canary |
| `awg0` | zero-user, diagnose OK | below quality floor |
| `awg3` | zero-user, diagnose OK | below quality floor; previously avoided |
| OpenVPN target | zero-user, strong throughput | diagnose `SUSPECT`, stale handshake |
| WireGuard target | zero-user, strong throughput | diagnose `SUSPECT`, stale handshake |
| E9.3 | NO-GO | wait for clean target or create explicit waiver packet |

## E9.2.3 Second Canary Target Readiness Watcher

```text
manual_checker_created=true
current_second_canary_readiness=NO-GO
selected_target=NONE
clean_zero_user_target_exists=false
execution_allowed_now=false
```

| Layer | E9.2.3 Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| target watcher | read-only manual checker created | stale input if not rerun against fresh state | none; read-only | ready for manual evidence refresh |
| candidate `10.7.0.14` | still valid on `vless`, table `1012` | target unavailable | one-user if later approved | candidate can remain in future packet |
| target `1` | occupied by `10.7.0.5` | would mix mechanics canary with existing load | more than clean one-user attribution | NO-GO |
| zero-user targets | present but rejected | quality floor or `SUSPECT` diagnose | canary attribution unreliable | NO-GO |
| E9.3 | blocked | no selected target | none now | forbidden without new approval |

## E9.2.4 Zero-User Egress Diagnostics

```text
truly_no_clean_target=true
second_canary_readiness=CONDITIONAL
execution_allowed_now=false
```

| Layer | E9.2.4 Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| target `1` | best current operational target, occupied by `10.7.0.5` | mixes mechanics proof with existing target load | one user switch plus shared egress load | conditional waiver only |
| OpenVPN target | zero-user, high quality, interface up, diagnose `SUSPECT` | stale/idle handshake may hide real peer issue | one-user if later approved | conditional idle-SUSPECT waiver |
| WireGuard target | zero-user, high quality, interface up, diagnose `SUSPECT` | stale/idle handshake may hide real peer issue | one-user if later approved | conditional idle-SUSPECT waiver |
| `awg0` | zero-user, diagnose OK, below quality floor | bad target quality confounds canary | one-user if later approved | NO-GO |
| `awg3` | zero-user, diagnose OK, below quality floor | bad target quality confounds canary | one-user if later approved | NO-GO |
| watcher | strict clean-target mode | may be too strict for waiver mode, correct for clean mode | none | keep strict by default |

## E9.2.5 OpenVPN Waiver Approval Packet

```text
target_egress=openvpn-1779388847-d2ad7c
waiver_name=openvpn_idle_suspect_mechanics_canary
approval_status=CONDITIONAL
execution_allowed_now=false
```

| Layer | E9.2.5 Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| candidate `10.7.0.14` | valid baseline `vless`, table `1012` | must be rechecked before live switch | one-user | conditional |
| OpenVPN target | zero-user, high quality, interface up, diagnose `SUSPECT` | stale idle handshake may hide real peer failure | one-user if approved | conditional waiver |
| rollback | previewed to `vless` / `tun0` | not live-proven for this user/target | one-user | conditional |
| strict watcher | still NO-GO | clean target not available | none | correct for strict mode |
| E9.3 | not executable | requires explicit live approval and fresh checks | one-user only if approved | blocked now |

## E9.3 OpenVPN Waiver Canary Execution

```text
current_canary_status=SUCCESS_ROLLED_BACK_WITH_POST_RESTORE_AUTOSWITCH_MOVEMENT
execution_allowed_now=false
```

| Layer | E9.3 Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| OpenVPN waiver canary | forward/observation/rollback succeeded for `10.7.0.14` | target diagnose remains idle-SUSPECT | one user during held quiet window | mechanics proven with waiver |
| table `1012` | switched to `v7edb0c189291`, then restored to `tun0` | no drift observed during hold | one user | OK |
| kill switch | stayed OK | none observed | platform-wide dependency | OK |
| reconcile/provisioning | stayed OK | none observed | platform-wide consistency gate | OK |
| autoswitch restore | timer restore immediately triggered apply | moved `10.7.0.5` after rollback | additional user after restore | NOT READY for next canary |
| apply timer | restored and active | catch-up/immediate fire can move users outside canary attribution | potentially multiple users | requires staged restore model |

## E9.3.1 Restore Side-Effect Classification

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

Updated matrix entry:

| Layer | E9.3.1 Status | Remaining Risk |
|---|---|---|
| held canary window | one-user bounded for E9.3 candidate | still requires explicit approval per user/target |
| candidate rollback | live-proven for `10.7.0.14 -> vless` | does not bound post-restore autoswitch behavior |
| apply timer restore | immediately moved `10.7.0.5: 1 -> vless` | hidden blast radius unless apply restore is staged and separately approved |
| planner restore | should be restored before apply and observed | planner can reveal pending moves but may still write advisory state |
| future canary | blocked | restore governance must change before another live canary |

## E9.3.2 Staged Restore Governance

```text
staged_restore_model_created=true
recommended_restore_model=planner_first_apply_by_separate_approval
apply_restore_requires_separate_approval=true
future_canary_restore_sequence_safe=false
second_canary_readiness=CONDITIONAL_AFTER_STAGED_RESTORE_APPROVAL
execution_allowed_now=false
```

Updated matrix entry:

| Layer | E9.3.2 Status | Remaining Risk |
|---|---|---|
| staged restore model | documented | not live-proven yet |
| planner-only restore | required future stage | planner can reveal but not apply moves |
| apply restore approval | separate operator gate | can still move users once restored |
| future canary | conditionally discussable after staged restore approval | execution remains forbidden now |
# E9.3.3 Risk Matrix Addendum

| Layer | Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| planner-only restore | rehearsed successfully | exposes pending moves without applying them | none during planner-only stage | ready as observation stage |
| apply restore | held | immediate non-canary user movement possible | broader than canary | requires separate approval |
| autoswitch apply timer | inactive after E9.3.3 | restoring it can apply planner-selected moves | potentially multiple users | NO-GO without approval |
| future canary restore sequence | conditional | safe only if planner-first/apply-separate model is followed | one-user canary plus separately governed restore | conditional |

## E9.3.4 Apply Restore Approval Packet

```text
apply_restore_current_status=HELD
planner_only_active=true
apply_timer_held=true
pending_moves_visible=false
pending_moves_count=0_current
approval_status=CONDITIONAL
execution_allowed_now=false
```

| Layer | E9.3.4 Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| planner-only restore | active and producing zero selected moves in fresh samples | planner state can change with health/sentinel signals | none while apply held | safe to observe |
| apply restore | still held | restoring timer can immediately move users in a future sample | potentially multiple users | conditional separate approval only |
| awg3 eligibility | no current selected moves, but previous pending moves targeted awg3 | canary watcher and autoswitch planner have different eligibility semantics | non-canary users if apply restored during conflict | needs explicit acceptance or rule alignment |
| future canary | still blocked | canary attribution depends on separate apply restore handling | one-user only during canary; restore stage separate | blocked until apply restore governance is resolved |

## E9.3.7 Transient Service Signal Addendum

| Layer | Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| autoswitch service hard gates | design issue identified | one transient non-Telegram service failure can make current egress ineligible | all users on affected egress can become candidates over repeated runs | needs policy fix |
| service-signal persistence | proposed only | current code lacks N-sample confirmation before hard block | broad failover candidate set | not deployed |
| staged apply restore | held | current policy can produce non-zero moves in final planner sample | multiple users if approved blindly | NO-GO under current policy |
| canary attribution | blocked by restore policy | unrelated autoswitch movements can occur after canary window | broader than canary | requires policy refinement or explicit bounded apply waiver |

## E9.3.8 Repo Fix Addendum

| Layer | Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| autoswitch service policy | repo fix implemented | runtime still old until deploy | broad failover remains possible in runtime | deploy approval required |
| transient service failure | fixture-proven selected_moves=0 after repo fix | not yet proven on live runtime | none in fixture; runtime unchanged | needs post-deploy planner dry-run |
| apply restore | held | unsafe until runtime policy deploy and proof | potentially multiple users | NO-GO |
| future canary | blocked | restore/apply governance unresolved | one-user canary plus separate restore stage | NO-GO |

## E9.3.9 Runtime Policy Deploy Addendum

| Layer | Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| autoswitch runtime policy | deployed to `/usr/local/bin/v7-users-autoswitch` | single-file runtime change completed; rollback backup exists | policy planner only while apply held | deployed and verified |
| planner-only behavior | post-deploy `selected_moves=[]` | future health signals can change planner output | none while apply timer held | safe to observe |
| apply restore | still held | restoring timer can still move users if a future sample selects moves | potentially multiple users | requires separate approval |
| canary attribution | still blocked by restore governance | apply restore phase must be separated from canary | one-user during canary, broader if apply restored | NO-GO until apply restore is resolved |

## E9.4 Apply Restore Gate Addendum

| Layer | Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| final planner gate | non-zero selected moves | apply restore would move users immediately | three selected users in observed sample | abort required |
| apply timer | remained held | platform still lacks restored apply authority | none while held | NO-GO until movement is explained/approved |
| autoswitch recovery | not executed | selected moves still need post-policy root cause | potentially users on egress `1` | separate approval required |
| future canary | blocked | apply restore unresolved after policy fix | canary attribution not clean | NO-GO |

## E9.4.1 Post-Policy Root Cause Addendum

| Layer | Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| egress `1` eligibility | E9.4 abort sample hard-blocked by `telegram_required_telegram_down_14s` | transient Telegram sentinel hard-block can make current egress globally ineligible | all users on egress `1` can become failover candidates over repeated runs | classified; not safe to apply automatically |
| Instagram service signal | one failed sample downgraded to `DEGRADED_SERVICE` | penalty-only, not global ineligibility | none by itself | policy fix working for this class |
| final planner gate | later E9.4.1 snapshot recovered to `selected_moves=[]` | state is time-sensitive; stale approval is unsafe | none while apply timer held | must be repeated in next live block |
| apply timer | still held | restoring it without fresh gate could apply timer-driven movement | potentially multiple users | NO-GO without separate approval |
| future canary | blocked by apply restore governance | canary attribution depends on restored/understood autoswitch authority | canary one-user only after restore governance resolves | NO-GO |

## E9.4.3 Post-Apply-Restore Monitoring Addendum

| Layer | Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| apply timer | restored and active | delayed timer-driven movement can occur after an immediate clean restore sample | three users observed in E9.4.3 | active but not yet governance-clean |
| autoswitch recovery | moved `10.7.0.5`, `10.0.0.2`, `10.0.0.3` from `1` to `vless` | movement happened after E9.4.2 had reported immediate `actual_movements_count=0` | broader than a one-user canary | requires delayed side-effect classification |
| route tables | consistent with changed registry | no drift against current registry, but runtime baseline changed | affected tables `100`, `101`, `1003` | operationally OK, attribution not OK |
| runtime checks | reconcile, user-route, kill-switch, provisioning all OK | checks do not prevent attributed autoswitch movement | platform-wide checks passed | healthy after movement |
| future canary | blocked | current candidate/target truth changed and restore governance is not fully proven | any future canary attribution would be ambiguous | NO-GO until root-cause/settle model update |

Updated status:

```text
current_canary_status=NO-GO_POST_RESTORE_DELAYED_AUTOSWITCH_MOVEMENT_OBSERVED
next_canary_readiness=NO-GO
execution_allowed_now=false
```

## E9.4.5 Restore Settle Gate Addendum

| Layer | Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| Restore settle gate | `defined_and_checker_created` | Without multi-sample settle, clean restore can miss delayed hard-block cycles | Up to autoswitch failover limit per apply cycle | Required before next apply restore/canary planning |
| Pre-restore gate | `NO-GO_on_E9.4.4_evidence` | Telegram hard-block and selected moves were present in the restore window | Three users moved in the observed delayed cycle | Not clean |
| Post-restore guard | `mandatory` | Immediate no-op is insufficient evidence | Broader than canary if timer later moves users | Must span at least two apply timer intervals |
| Next canary | `NO-GO` | Restore governance is not live-proven | Any future canary attribution can be polluted by delayed autoswitch recovery | Requires E9.4.5 gate to pass in future evidence |

Current status:

```text
restore_settle_checker_created=true
current_restore_settle_status=NO-GO
additional_policy_fix_required=true
next_canary_readiness=NO-GO
execution_allowed_now=false
```

## E9.4.4 Risk Matrix Update

| Layer | Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| Autoswitch apply restore | `delayed_movement_root_cause_classified` | A single clean gate can miss a later Telegram hard-block cycle | Up to `autoswitch_max_failover_per_run` per apply cycle | NO-GO for canary attribution until delayed-settle gate exists |
| Telegram hard-block signal | `transient_recurring` | `DOWN_GRACE` can become `TELEGRAM_DOWN_14S` after restore | All Telegram-required users on affected egress become candidates | Needs multi-sample restore gating |
| Canary restore governance | `not_live_proven` | Immediate no-op does not prove delayed stability | Broader than canary if apply timer moves users later | Requires restore settle design |
| Routing/datapath after movement | `stable` | No drift relative to changed registry | Moved users' tables only | Operationally OK, attribution unsafe |

Current status:

```text
restore_governance_live_proven=false
next_canary_readiness=NO-GO
execution_allowed_now=false
```

## E9.4.6 Fresh Restore Settle Observation Addendum

| Layer | Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| Fresh restore settle window | `GO` | A future signal can still change planner output, so approval must be fresh | none observed in E9.4.6 | ready for approval-packet planning |
| Autoswitch selected moves | `selected_moves=[]` across 3 samples | stale evidence is unsafe if reused later | none in fresh window | clean for current observation |
| Telegram hard-block | absent across fresh samples | Telegram remains a known transient risk | none while not hard-blocked | monitor in any future gate |
| Egress `1` eligibility | eligible across fresh samples | egress can become ineligible if Telegram hard-block recurs | users on egress `1` if hard-block recurs | currently stable |
| Next canary | `CONDITIONAL` | requires fresh candidate/target approval, not direct execution | one-user only after explicit approval | approval packet can resume |

Current status:

```text
current_restore_settle_status=GO
restore_governance_live_proven=true
next_canary_readiness=CONDITIONAL
execution_allowed_now=false
```

## E10 Fresh Second Canary Approval Matrix

| Layer | Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| Fresh restore-settle gate | `GO` | Future service-signal drift still requires fresh sampling before any live action | none in E10 | usable for approval-packet planning |
| Fresh canary candidate | `CONDITIONAL` (`10.7.0.11`) | Candidate is valid only if a target becomes approved | future one-user only | not executable without target |
| Fresh target selection | `NO-GO` | No clean target exists under strict route-class/diagnose rules | none in E10 | blocked |
| Route-class waiver paths | `not_accepted` | `awg0`/`awg3` lack Direct/RU and Trusted RU exclusions | future one-user only if separately approved | requires explicit waiver packet |
| Idle-SUSPECT waiver paths | `not_accepted` | OpenVPN/WireGuard require fresh diagnose waiver | future one-user only if separately approved | requires explicit waiver packet |
| Second canary | `NO-GO_E10_FRESH_SECOND_CANARY_PACKET_NO_CLEAN_TARGET` | stale approvals would be unsafe | none | approval packet complete, execution forbidden |

Current status:

```text
restore_settle_gate_status=GO
candidate_user=10.7.0.11
selected_target=NONE
second_canary_approval_status=NO-GO
execution_allowed_now=false
```

## E10.1 Target Remediation Matrix

| Layer | Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| `awg0` remediation candidate | `GO_for_future_metadata_packet` | Runtime metadata edit still needs backup and rollback | no current users; future one-user canary only | ready for bounded mutation approval packet |
| `awg3` fallback | `CONDITIONAL_fallback` | Lower current quality and prior restore discussion history | no current users | fallback only |
| Direct/RU exclusions | `metadata_only_planned` | Wrong metadata edit could alter policy-aware eligibility | route-class selection only; no domain/routing mutation in E10.1 | low risk with exact diff |
| Trusted RU exclusions | `metadata_only_planned` | Trusted RU state remains stale/sensitive | prevents target from sensitive route-class use | low risk with stale-state awareness |
| Kill switch | `no_mutation_expected` | Must be rechecked after any future runtime metadata mutation | none in E10.1 | read-only check required after mutation |
| Second canary | `blocked_until_metadata_mutation_and_new_packet` | Target not clean until metadata changes and fresh checks pass | none in E10.1 | conditional planning only |

Current status:

```text
remediation_candidate=awg0
remediation_approval_status=GO
mutation_required=true
policy_apply_required=false
execution_allowed_now=false
```

## E10.2 AWG0 Metadata Remediation Abort Matrix

| Layer | Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| `awg0` metadata mutation | `ABORTED_BEFORE_MUTATION` | E10.1 zero-user assumption became stale | none, because no edit occurred | blocked |
| `awg0` target readiness | `NO-GO` | Occupied by real users and `HARD_FULL` load state | active users on `awg0` if metadata were changed | not eligible for clean target remediation |
| `awg3` fallback | `NO-GO` | Also occupied by real users | active users on `awg3` | not a clean fallback |
| Restore-settle gate | `GO` | Future service-signal drift remains possible | none in E10.2 | usable but insufficient without target |
| Runtime checks | `OK` | none observed | none | stable |
| Second canary target pool | `NO-GO` | No clean target under strict current rules | none | requires fresh target-pool truth refresh |
| E10.2 runtime mutation | `NO` | no runtime write performed | none | correctly aborted |

Current status:

```text
metadata_mutation_executed=false
abort_reason=awg0_no_longer_zero_user
target_readiness_after=NO-GO
selected_target_after=NONE
restore_settle_gate_status=GO
second_canary_readiness_after=NO-GO
current_canary_status=NO-GO_E10_2_AWG0_METADATA_REMEDIATION_ABORTED_TARGET_OCCUPIED
execution_allowed_now=false
```

## E10.3 Fresh Target Pool Truth Matrix

| Layer | Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| Restore-settle gate | `GO` | Future service-signal drift still requires fresh sampling before live action | none in E10.3 | usable for approval-packet planning only |
| `target 1` | `NO-GO_OCCUPIED` | Six production users currently on target | active users on `1` | not a canary target |
| `awg0` | `NO-GO_ZERO_USER_LOW_QUALITY_MISSING_EXCLUSIONS` | Metadata-only remediation would not fix quality floor | none if read-only; active production pool if later mutated | blocked |
| `awg3` | `NO-GO_ZERO_USER_LOW_QUALITY_MISSING_EXCLUSIONS` | Same as `awg0`, with lower current stability | none if read-only | blocked |
| OpenVPN | `NO-GO_SUSPECT_LOW_QUALITY` | SUSPECT diagnose plus current min/stability below floor | one-user only if separately waived later | not recommended |
| WireGuard | `CONDITIONAL_SUSPECT_QUALITY_OK` | stale-handshake diagnose blocks clean target | one-user only if separate waiver approved | best conditional waiver candidate |
| Second canary | `NO-GO` | No clean zero-user target exists | none in E10.3 | blocked |

Current status:

```text
restore_settle_gate_status=GO
clean_zero_user_target_exists=false
best_current_target_path=E_PAUSE_CANARY_AND_FOCUS_ON_TARGET_POOL_GOVERNANCE_OR_CAPACITY
second_canary_readiness=NO-GO
execution_allowed_now=false
```

## E10.4 Target Reservation Strategy Matrix

| Layer | Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| Target reservation policy | `CREATED_DESIGN_ONLY` | Not deployed; autoswitch does not yet enforce reservation | none in E10.4 | ready for future approval packet |
| WireGuard path | `BEST_SHORT_TERM_CONDITIONAL` | `SUSPECT` stale handshake must be classified | none until future approval | next read-only diagnostic recommended |
| Dedicated canary egress | `BEST_DURABLE_STRATEGY` | Requires provisioning/metadata/policy approval | none in E10.4 | planning required |
| AWG remediation | `NOT_IMMEDIATE` | Quality floor fails; metadata alone insufficient | none in E10.4 | blocked until quality improves |
| Occupied target canary | `NOT_PREFERRED` | Weak attribution and no clean isolation | possible one-user command but shared target state | avoid except explicit mechanics waiver |
| Second canary | `NO-GO` | No clean reserved zero-user target | none | blocked |

Current status:

```text
target_pool_blocker=no_clean_reserved_zero_user_target
best_strategy=WIREGUARD_DIAGNOSE_THEN_RESERVE_OR_WAIVE
recommended_next_block=E10.5_WIREGUARD_STALE_HANDSHAKE_DIAGNOSTIC_AND_RESERVATION_FEASIBILITY_PACKET
second_canary_readiness=NO-GO
execution_allowed_now=false
```

## E10.5 WireGuard Diagnostic / Reservation Feasibility Matrix

| Layer | Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| WireGuard target | `CONDITIONAL_STALE_HANDSHAKE_ONLY` | Persisted diagnose says SUSPECT even though live handshake is fresh | none in E10.5 | best conditional reservation candidate |
| Quality floor | `OK` | Historical fail-rate advisory remains noisy, but current avg/min/stability pass | none | acceptable for waiver packet |
| Route-class exclusions | `PRESENT` | Direct/RU and Trusted RU exclusions already present | none | clean for route-class scope |
| Reservation | `FEASIBLE_NOT_APPLIED` | `canary_reserved=true` must be enforced by tooling before relying on it | none until mutation | needs bounded approval packet |
| Waiver | `CONDITIONAL` | Diagnose `SUSPECT` still blocks strict clean target readiness | future one-user only if approved | requires fresh gate |
| Second canary | `NO-GO` | no reservation or waiver has been approved | none | blocked |

Current status:

```text
wireguard_root_classification=STALE_HANDSHAKE_ONLY
wireguard_reservation_feasible=true
waiver_required=true
second_canary_readiness=NO-GO_E10_5_WIREGUARD_RESERVATION_OR_DIAGNOSE_FIX_REQUIRED
execution_allowed_now=false
```

## E11.1 WireGuard Clean Target Matrix

| Layer | Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| WireGuard datapath | `STALE_HANDSHAKE_ONLY` | persisted diagnose is stale/too strict | none in E11.1 | suitable conditional target |
| WireGuard quality | `OK` | historical fail-rate advisory still noisy but avg/min/stability pass | none | acceptable |
| WireGuard reservation | `FEASIBLE_NOT_APPLIED` | reservation must be enforced by tooling | none until mutation | needs E11.2 approval |
| Waiver | `CONDITIONAL` | diagnose remains `SUSPECT` under strict rules | future one-user only | acceptable only with fresh gate |
| Dedicated test egress | `NOT_REQUIRED_FOR_NEXT_PACKET` | without it, WireGuard waiver carries residual diagnose semantics risk | none | recommended long-term |
| Second canary | `NO-GO` | no reservation, no waiver/fix yet | none | blocked |

Current status:

```text
best_strategy=WIREGUARD_RESERVE_THEN_DIAGNOSE_FIX_OR_STALE_HANDSHAKE_WAIVER
recommended_next_block=E11.2_WIREGUARD_RESERVATION_AND_DIAGNOSE_SEMANTICS_APPROVAL_PACKET
execution_allowed_now=false
```

## E11.2 WireGuard Reservation And Stale-Handshake Semantics

| Layer | Status | Risk | Blast Radius | Operational Readiness |
|---|---|---|---|---|
| WireGuard datapath | `LIVE_HEALTHY` | persisted diagnose stale relative to live handshake | none in E11.2 | usable for conditional approval |
| Diagnose semantics | `TOO_STRICT` | strict target readiness still rejects `SUSPECT` | none | needs fix or waiver |
| Reservation | `APPROVED_FOR_SEPARATE_PACKET` | metadata must be applied and honored before reliance | none until mutation | next bounded block |
| Waiver | `CONDITIONAL` | accepts stale diagnose only for one canary window | future one-user only | requires fresh approval |
| Second canary | `NO-GO` | reservation not applied and no fresh candidate packet | none | blocked |

Current status:

```text
wireguard_semantics_classification=DIAGNOSE_SEMANTICS_TOO_STRICT
reservation_feasible=true
reservation_requires_mutation=true
waiver_status=waiver_conditional
expected_second_canary_readiness=CONDITIONAL_AFTER_RESERVATION_WITH_WAIVER_OR_GO_AFTER_DIAGNOSE_FIX
current_status=NO-GO_E11_2_WIREGUARD_RESERVATION_APPROVAL_READY
```

## E11.4 Risk Entry - WireGuard Diagnose Semantics

| Risk | Classification | Evidence | Mitigation | Current Status |
| --- | --- | --- | --- | --- |
| WireGuard diagnose marks reserved zero-user target `SUSPECT` despite good route/quality evidence | `DIAGNOSE_REFRESH_BUG` | Runtime `v7-egress-diagnose` uses an AWG-specific handshake command path; strict readiness and autoswitch block `severity_SUSPECT` | Prepare bounded protocol-aware diagnose fix; keep strict canary `NO-GO` until fixed or explicitly waived | `OPEN` |
| Stale-handshake waiver hides a real target fault | Low datapath risk, medium attribution risk | WireGuard is zero-user/reserved/quality OK, but persisted diagnose remains `SUSPECT` | Waiver only for one user with fresh live `wg show`, route, restore-settle, and rollback evidence | `CONDITIONAL_FALLBACK_ONLY` |

Current risk posture:

```text
diagnose_affects_real_runtime=false
diagnose_affects_target_readiness_only=false
stale_handshake_operational_risk=LOW_DATAPATH_MEDIUM_GOVERNANCE_ATTRIBUTION
fix_required=true
execution_allowed_now=false
```

## E11.5 Risk Entry - Repo Fix Ready, Runtime Unchanged

| Risk | Classification | Evidence | Mitigation | Current Status |
| --- | --- | --- | --- | --- |
| Repo-side fix not yet deployed to runtime | `RUNTIME_DEPLOY_REQUIRED` | `tools/v7-egress-diagnose` tests pass and fixed fixture selects WireGuard, but `/usr/local/bin/v7-egress-diagnose` remains unchanged | Prepare bounded runtime deploy with backup, hash verification, diagnose refresh, target readiness, and rollback command | `OPEN` |
| AWG regression from protocol split | `LOW_TESTED` | Fixture tests prove AWG path still uses `awg show` | Recheck AWG0/AWG3 diagnose after runtime deploy | `MONITOR_AFTER_DEPLOY` |

Current status:

```text
repo_diagnose_fix_implemented=true
runtime_deploy_executed=false
awg_regression_observed=false
execution_allowed_now=false
```

## E11.6 Risk Entry - Runtime Diagnose Fix Deployed

| Risk | Classification | Evidence | Mitigation | Current Status |
| --- | --- | --- | --- | --- |
| WireGuard false stale-handshake blocker persists after deploy | `RESOLVED` | Runtime diagnose now reports `wireguard-1779454504-c43409_diagnose_reason=OK`; target readiness selects reserved WireGuard when current candidate truth is supplied | Keep protocol-aware diagnose tests and re-run fresh readiness before canary approval | `CLOSED` |
| AWG regression from protocol-aware command split | `NOT_OBSERVED` | `awg0`, `awg3`, and target `1` all report `OK`; target `1` confirmed `protocol=amneziawg` and `awg show` path works | Continue AWG regression matrix in future diagnose deploys | `MONITOR` |
| Stale canary packet reused after runtime truth changed | `GOVERNANCE_RISK` | `10.7.0.14` is currently on `1`, not `vless` | Require fresh candidate/current-egress/rollback packet before any canary | `OPEN` |

Current status:

```text
diagnose_fix_deployed=true
target_readiness_after=GO
selected_target_after=wireguard-1779454504-c43409
waiver_required_after=false
execution_allowed_now=false
```

## E11.7 Risk Entry - Reserved Target Occupied

| Risk | Classification | Evidence | Mitigation | Current Status |
| --- | --- | --- | --- | --- |
| Reserved WireGuard target carries production users | `RESERVATION_ENFORCEMENT_GAP` | `canary_reserved=true` but registry/load-state show 12 users on `wireguard-1779454504-c43409` | Investigate autoswitch reservation enforcement; do not use target for canary until zero-user | `OPEN` |
| Fresh packet reuses stale target assumptions | `PREVENTED` | E11.7 aborted with `selected_target=NONE` and no executable preview | Keep Phase 1 target readiness gate mandatory | `CLOSED_FOR_E11.7` |

Current status:

```text
target_readiness_status=NO-GO
wireguard_diagnose=OK
wireguard_occupancy=12
approval_status=NO-GO
execution_allowed_now=false
```

## E11.8 Risk Entry - Reservation Enforcement Fixed, Drain Still Required

| Risk | Status | Evidence | Mitigation | Disposition |
| --- | --- | --- | --- | --- |
| Production autoswitch assigns new users to `canary_reserved` target | `FIXED` | Runtime `v7-users-autoswitch` now blocks `canary_reserved_production_assignment_blocked`; post-deploy observation showed no new WireGuard assignments | Keep targeted reservation enforcement tests and runtime hash check | `CLOSED_FOR_NEW_ASSIGNMENT` |
| Existing users remain on reserved WireGuard target | `OPEN` | `wireguard_users_after=10` | Prepare separate bounded drain approval packet; no canary while occupied | `NO-GO_FOR_CANARY` |
| Automatic drain from reserved target causes broad movement | `PREVENTED` | E11.8 deliberately holds current reserved users with a separate drain approval reason | Drain only by explicit future block | `CONTROLLED` |

## E11.10 Risk Entry - Second Canary Closeout

| Risk | Status | Evidence | Mitigation | Disposition |
| --- | --- | --- | --- | --- |
| E11.10 canary left open after observation C | `CLOSED` | Closeout proved `10.7.0.3` was still on WireGuard and then rolled it back to `awg0` | Bounded rollback of only `10.7.0.3`, then staged restore and delayed monitoring | `CLOSED_ROLLED_BACK_AND_SETTLED` |
| Keep decision while planner predicted movement | `PREVENTED` | Pre-rollback closeout samples B/C showed `selected_moves=1` | Reject keep, execute default rollback | `CLOSED` |
| Non-candidate user movement during closeout | `NOT_OBSERVED` | Rollback diff changed only `10.7.0.3`; final switch-history count stayed stable | Keep closeout movement budget to one candidate user | `CLOSED_FOR_E11.10` |
| Delayed autoswitch movement after apply restore | `NOT_OBSERVED` | Final samples A/B/C: registry hash stable, switch-history count stable, `selected_moves=0`, checkers OK | Continue restore-settle gate requirement for future live blocks | `MONITOR` |

Current E11.10 closeout posture:

```text
rollback_executed=true
rollback_target=awg0
restore_settle_gate_status=GO
delayed_movements_observed=false
runtime_checks_ok=true
execution_allowed_now=false
```

## E11.12 Risk Entry - Two-User Mini-Cohort Approval Packet

| Risk | Status | Evidence | Mitigation | Disposition |
| --- | --- | --- | --- | --- |
| Two-user cohort exceeds reserved target capacity | `CONTROLLED` | WireGuard `users=0`, `soft_limit=1`, `hard_limit=2`; selected cohort size is exactly two | Hard cap first cohort at two users; third user forbidden | `CONDITIONAL_GO_FOR_PACKET_ONLY` |
| Runtime drift invalidates stale candidate truth | `OBSERVED_AND_REBOUND` | Initial E11.12 state drifted before final settle samples; final samples then proved stable hash `27e42d79...` | Future execution must re-run fresh candidate/current-egress pre-checks | `CONDITIONAL` |
| Delayed autoswitch movement before cohort | `NOT_OBSERVED_FINAL_STATE` | Restore-settle samples `[0,0,0]`, registry stable, hidden movers false, checkers OK | Keep restore-settle gate mandatory before and after execution | `CLOSED_FOR_E11.12` |
| Shared rollback target `1` is overloaded by static load state | `MEDIUM` | Both selected users currently live on `1`; rollback restores original state, but target carries 13 users | Sequential rollback and per-user verification | `ACCEPTABLE_WITH_GATES` |
| WireGuard under two-user live load remains unproven | `RESIDUAL` | E11.12 is read-only; no cohort load was executed | First execution must be an E11.13 bounded live block with immediate rollback criteria | `OPEN_FOR_EXECUTION_BLOCK` |

Current E11.12 posture:

```text
mini_cohort_readiness=CONDITIONAL
selected_candidates=10.7.0.11,10.7.0.12
selected_target=wireguard-1779454504-c43409
target_capacity_safe=true
restore_settle_gate_status=GO
approval_status=CONDITIONAL
execution_allowed_now=false
```

## E11.13 Risk Entry - Mini-Cohort Executed, Delayed Apply Movement

| Risk | Status | Evidence | Mitigation | Disposition |
| --- | --- | --- | --- | --- |
| Two-user WireGuard overload | `NOT_OBSERVED` | WireGuard users reached exactly 2, hard limit 2, checkers OK | Keep two-user cap | `CLOSED_FOR_E11.13` |
| Approved user rollback failure | `NOT_OBSERVED` | Both users rolled back to `1`; only approved users changed during rollback | Keep sequential rollback | `CLOSED_FOR_E11.13` |
| Reserved target leakage after rollback | `NOT_OBSERVED` | Final WireGuard users `0`; target readiness after `GO` | Keep reservation enforcement | `CLOSED_FOR_E11.13` |
| Delayed non-cohort movement after apply restore | `OBSERVED` | `10.7.0.9`, `10.7.0.10`, `10.7.0.13` moved `1 -> awg0` after apply timer restore | Apply timer re-held; root-cause required | `OPEN_BLOCKER` |
| Larger cohort promotion | `BLOCKED` | Full lifecycle status includes delayed apply movement | No larger cohort until E11.14 hardening | `NO-GO` |

Current E11.13 posture:

```text
mini_cohort_lifecycle_status=EXECUTED_ROLLED_BACK_DELAYED_APPLY_MOVEMENT_OBSERVED_CONTAINED
wireguard_users_after=0
runtime_checks_ok=true
apply_timer_reheld_for_containment=true
next_stage_readiness=NO_GO_FOR_LARGER_COHORT_APPLY_RESTORE_ROOT_CAUSE_REQUIRED
execution_allowed_now=false
```
## E11.14 Delayed Apply-Restore Risk

Risk: post-restore apply timer can perform fresh non-cohort failover after a clean restore-settle window.

Observed impact:

- 10.7.0.9, 10.7.0.10, 10.7.0.13 moved from `1` to `awg0` by timer-driven autoswitch.
- Trigger: target `1` transient Telegram hard signal (`telegram_required_telegram_down_14s`).
- Not stale selected_moves; not manual apply; not hidden routing-sync.

Mitigation:

- Apply timer remains held after E11.13 containment.
- E11.14 deployed restore-barrier service-signal suppression in `v7-users-autoswitch`.
- Restore barrier now quarantines failover selection during post-restore containment; `telegram_required_*` is also classified as service-signal-only for restore-stage semantics.
- Larger cohort readiness remains NO-GO until apply-restore barrier/generation rehearsal is complete.

Residual risk: medium while apply timer is held and barrier active; high if apply timer is restored without a fresh E11.15 approval/rehearsal.

## E11.15 Apply-Restore Barrier Rehearsal Risk

| Risk | Status | Evidence | Mitigation | Disposition |
| --- | --- | --- | --- | --- |
| Apply timer ignores restore barrier | `NOT_OBSERVED` | Timer-triggered apply run had active barrier, `selected_moves=0`, and `apply_result.reason=no_selected_moves` | Keep barrier parser/runtime tests | `CLOSED_FOR_BOUNDED_REHEARSAL` |
| Delayed non-cohort movement during barrier window | `NOT_OBSERVED` | Five samples kept registry hash `bc7a6b1c...`, switch-history count `2698`, WireGuard users `0` | Keep multi-interval observation mandatory | `CLOSED_FOR_E11.15_WINDOW` |
| Rebalance bypasses failover barrier | `NOT_OBSERVED` | All samples had `rebalance_candidates=0` and selected moves `0` | Keep targeted autoswitch policy tests | `CLOSED_FOR_E11.15_WINDOW` |
| Barrier TTL expiry causes fresh movement | `UNTESTED` | TTL expires at 2026-05-28T10:52:27Z, outside bounded window | Require post-TTL validation or generation-token model | `OPEN_BLOCKER_FOR_UNATTENDED_APPLY` |
| Barrier over-suppresses production recovery | `CONDITIONAL` | Active barrier intentionally suppresses failover selection | Apply timer returned to hold after rehearsal | `CONTROLLED_BY_HOLD` |
| Larger cohort promotion | `BLOCKED` | Post-TTL/generation behavior not proven | Separate E11.16 governance block | `NO-GO` |

Current E11.15 posture:

```text
barrier_rehearsal_executed=true
apply_timer_final_state=held
user_movement_observed=false
delayed_non_cohort_movement_prevented=true
mini_cohort_readiness_after=CONDITIONAL
larger_cohort_readiness_after=NO-GO
execution_allowed_now=false
```

## E12 Generation-Token And Nonzero Budget Risk

| Risk | Status | Evidence | Control | Residual status |
| --- | --- | --- | --- | --- |
| Nonzero clearance without ownership | `FIXED` | Budget 3 without token produced `selected_moves=0` | Require `generation_token` for `clearance_max_selected_moves>0` | `CLOSED` |
| Stale generation replay | `FIXED` | Stale generation selected 0 | Match `clearance_generation_id` to current planner generation | `CLOSED` |
| Stale selected-move replay | `FIXED` | Stale hash selected 0 | Match `approved_selected_moves_hash` | `CLOSED` |
| Count drift | `FIXED` | Expected-count mismatch selected 0 | Match `clearance_expected_selected_moves` | `CLOSED` |
| Budget too small | `FIXED` | Budget 2 against 3 selected candidates selected 0 | Enforce max selected moves before apply | `CLOSED` |
| Live timer nonzero rehearsal | `CLOSED` | Timer run with budget 3/no token returned no selected moves; switch-history stayed 2698 | Fail-closed generation guard | `CLOSED` |
| Larger cohort execution | `BLOCKED` | WireGuard hard limit 2; live matching-token movement not approved | Separate larger-cohort packet and target capacity | `CONDITIONAL_NO_GO` |
| Restart replay | `OPEN` | Generation is persisted-state derived, but restart rehearsal not executed | Future restart replay rehearsal | `MONITOR` |
