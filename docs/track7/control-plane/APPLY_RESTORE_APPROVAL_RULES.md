# Apply Restore Approval Rules

Mode: governance design only. This document does not authorize restoring apply authority.

## GO Conditions

Apply restore may be considered only when all are true:

- planner-only observation completed;
- pending moves are absent or fully understood;
- predicted movement count is within the accepted operator-approved range;
- no `v7-routing-sync` process is present or pending;
- `users.registry` did not drift unexpectedly;
- `v7-reconcile-check` is OK;
- `v7-user-route-check` is OK;
- `v7-killswitch-check` is OK;
- `v7-provisioning-reconcile-check` is OK;
- operator accepts autoswitch recovery as a separate stage from canary;
- containment plan exists for unexpected movement.

## NO-GO Conditions

Apply restore is blocked if any are true:

- planner predicts broad or unclear movement;
- movement reason is unclear;
- movement target/source is not understood;
- any runtime checker fails;
- `v7-routing-sync` appears;
- registry drift already occurred before apply restore;
- `v7-user-switch` appears unexpectedly;
- kill switch warning/failure appears;
- operator has not explicitly approved post-canary autoswitch recovery.

## Conditional Approval

Conditional approval may name exact accepted movements:

```text
accepted_user=<ip>
accepted_from=<egress>
accepted_to=<egress>
accepted_reason=<failover/reconnect/rebalance/planned>
max_apply_movements=<n>
```

Anything outside that approval is an abort condition.

## Operator Statement

Apply restore approval must include:

```text
I understand this is autoswitch recovery, not canary movement.
I approve restoring v7-users-autoswitch.timer under the stated movement limits.
```

## Current E9.3.2 Status

```text
apply_restore_requires_separate_approval=true
apply_restore_approved_now=false
execution_allowed_now=false
```

## E9.4.4 Delayed Restore Root-Cause Update

E9.4.4 classified the delayed post-restore movement found by E9.4.3:

```text
delayed_movement_root_cause=telegram_hard_block_recurred_after_clean_gate
root_cause_classification=MIXED_TELEGRAM_HARD_BLOCK_RECURRENCE_AND_CLEAN_GATE_WINDOW_TOO_SHORT
movement_count=3
moved_users=10.7.0.5,10.0.0.2,10.0.0.3
max_failover_behavior_expected=true
restore_governance_live_proven=false
```

Updated approval rule:

- a single clean final planner gate is not sufficient for apply restore proof;
- apply restore approval requires `N>=3` consecutive `selected_moves=0` planner-only samples;
- samples must span at least two full apply timer intervals;
- Telegram hard-block must remain absent for the full observation window;
- after apply timer restore, delayed-settle observation must also span at least two full apply timer intervals;
- any movement after apply restore must be classified as autoswitch recovery, not canary movement.

```text
apply_restore_model_safe=false
additional_policy_fix_required=true_for_restore_settle_guard
execution_allowed_now=false
```

## E9.3.3 Status

Planner-only restore was executed and apply authority remained held.

The planner exposed at least three pending failover recommendations:

```text
10.7.0.5: 1 -> awg3
10.0.0.2: 1 -> awg3
10.0.0.3: 1 -> awg3
```

Therefore apply restore is still NO-GO without separate approval.

Any apply restore approval must either:

- explicitly accept these movements and set `max_apply_movements>=3`; or
- wait for a new planner-only observation showing no selected moves.

Current status:

```text
planner_only_stage_safe=true
apply_restore_status=HELD_REQUIRES_SEPARATE_APPROVAL
apply_restore_approved_now=false
execution_allowed_now=false
```

## E9.3.4 Apply Restore Approval Packet

E9.3.4 refreshed planner-only evidence while keeping apply authority held.

Fresh planner-only samples no longer showed the E9.3.3 pending movements:

```text
candidate_moves=0
candidate_moves_total=0
selected_moves=0
apply_requested=false
apply_result.applied=false
```

However, apply restore is still not automatically approved. The previous E9.3 restore side effect proved that `v7-users-autoswitch.timer` can immediately move non-canary users when restored, and E9.3.3 proved that planner-only state can expose pending movements before apply.

Updated decision:

```text
apply_restore_current_status=HELD
planner_only_active=true
apply_timer_held=true
pending_moves_visible=false
pending_moves_count=0_current
pending_moves_stable=false
pending_moves_safe_to_apply=false_without_separate_operator_approval
awg3_eligibility_conflict=true
approval_status=CONDITIONAL
apply_restore_approved_now=false
execution_allowed_now=false
```

Conditional means apply restore may be discussed in a separate bounded live block only after a final immediate planner-only sample confirms either zero selected moves or an exact operator-approved movement list.

## E9.3.5 Apply Restore Execution Gate Result

E9.3.5 collected the required final immediate planner-only sample before restoring apply authority. The sample no longer matched the zero-move E9.3.4 approval packet:

```text
selected_moves=3
candidate_moves_total=15
apply_requested=false
selected_target=vless
reason=current_egress_not_eligible
```

Selected moves were:

```text
10.0.0.2: 1 -> vless
10.0.0.3: 1 -> vless
10.0.0.6: 1 -> vless
```

Because this was not a zero-move restore and no operator approval existed for the exact movement list, apply restore was aborted before `v7-users-autoswitch.timer` was started.

Updated decision:

```text
apply_restore_executed=false
apply_restore_aborted=true
apply_restore_current_status=HELD
pending_moves_visible=true
pending_moves_count=3_selected_15_candidates
pending_moves_safe_to_apply=false_without_exact_operator_approval
approval_status=NO-GO
execution_allowed_now=false
```

## E9.3.6 Root-Cause Update

E9.3.6 classified the E9.3.5 abort cause:

```text
egress_1_ineligibility_root_cause=service_instagram_failed hard service gate
root_cause_classification=MIXED_TRANSIENT_SERVICE_SIGNAL_AND_EXPECTED_FAILOVER_BEHAVIOR
candidate_moves_count=15
selected_moves_count=3
vless_target_reason=best eligible failover target
max_failover_behavior_expected=true
apply_restore_safe_now=false
apply_should_remain_held=true
execution_allowed_now=false
```

## E9.4.5 Restore Settle Gate Rule

E9.4.5 replaces the single-sample final gate with a restore settle gate.

Pre-restore apply approval is not even reviewable unless:

```text
required_samples>=3
required_apply_timer_intervals>=2
selected_moves=0 in every sample
telegram_hard_blocked=false in every sample
egress_1_eligible=true in every sample
users.registry stable
egress.registry stable
runtime_checkers=OK
hidden_movers_observed=false
```

Post-restore clean status is not granted by an immediate no-op. It requires a delayed settle window:

```text
observe at least 2 full apply timer intervals
movement_count=0 for clean restore
selected_moves remains empty or no-op
any movement is classified as autoswitch recovery, not canary movement
```

Current E9.4.5 read-only checker status:

```text
tool=tools/v7-restore-settle-gate
current_restore_settle_status=NO-GO
reason=telegram_hard_block_and_selected_moves_seen_in_E9.4.4_restore_window
apply_restore_model_safe=false
execution_allowed_now=false
```

Apply restore remains NO-GO unless a fresh final planner-only sample returns `selected_moves=0` or the operator explicitly approves the exact movement list and maximum movement count.

## E9.3.7 Policy Design Update

E9.3.7 does not approve apply restore. It formalizes the policy issue behind the E9.3.5 abort:

```text
current_policy_problem=single transient non-Telegram service failure can hard-block current egress and generate broad failover candidates
proposed_policy_model=service-signal confidence and persistence layer before global ineligibility
code_fix_required_before_apply_restore=true
apply_restore_safe_under_current_policy=false
apply_should_remain_held=true
execution_allowed_now=false
```

Updated apply restore approval rule:

- a single service failure such as `service_instagram_failed` must not be enough to approve broad failover;
- if current policy still treats the service failure as hard ineligible, apply restore remains NO-GO unless selected moves are zero in the immediate final planner sample;
- broad service-signal movement requires a separate exact-move approval packet;
- durable restoration should wait for a code-level autoswitch policy refinement or an explicit bounded operator waiver.

## E9.3.8 Repo Fix Update

The code-level policy refinement now exists repo-side:

```text
repo_policy_fix_implemented=true
runtime_policy_deployed=false
selected_moves_for_single_instagram_failure_after_fix=0
```

Apply restore is still not approved because the runtime executable has not been updated and no post-deploy planner proof exists.

Current rule:

```text
apply_restore_safe_after_repo_fix=false_until_runtime_deploy_and_post_deploy_planner_proof
apply_timer_should_remain_held=true
execution_allowed_now=false
```

## E9.3.9 Runtime Policy Deploy Update

The autoswitch policy fix was deployed to the runtime checker/planner path only. Apply authority remained held.

```text
runtime_policy_deployed=true
apply_timer_remained_held=true
planner_only_behavior_changed_without_apply_authority=true
selected_moves=0_after_deploy
```

This did not approve apply restore by itself. A separate fresh final planner-only gate remained mandatory.

## E9.4 Apply Restore Gate Abort

E9.4 attempted a bounded apply restore after policy deploy, but aborted at the final planner gate:

```text
selected_moves=3
candidate_moves_total=16
reason=current_egress_not_eligible
root_cause_later_classified=telegram_required_telegram_down_14s
apply_restore_executed=false
```

The abort was correct because the exact movement list was not approved.

## E9.4.1 Root-Cause Classification

E9.4.1 classified the E9.4 abort as a transient Telegram hard-block, not an incomplete Instagram policy fix:

```text
root_cause_classification=TELEGRAM_HARD_BLOCK
policy_fix_incomplete=false
apply_should_remain_held=true_until_fresh_clean_gate
```

## E9.4.2 Fresh Restore Retry

E9.4.2 repeated the required final planner-only gate. The latest gate was clean:

```text
selected_moves=0
egress_1_eligible=true
telegram_hard_blocked=false
runtime_checkers=OK
```

Apply timer restore was executed:

```text
systemctl start v7-users-autoswitch.timer
start_rc=0
```

Post-restore observation showed:

```text
actual_movements_count=0
actual_moved_users=[]
broad_failover_observed=false
emergency_containment_performed=false
apply_restore_clean=true
autoswitch_recovery_bounded=true
```

Updated rule: apply restore is acceptable only when the immediate final planner-only gate is clean or the operator explicitly approves the exact movement list. E9.4.2 proves the clean-gate path.

## E9.4.3 Delayed Movement After Clean Restore

E9.4.3 found that a clean immediate restore is not enough to clear apply-restore risk:

```text
E9.4.2 immediate_actual_movements_count=0
E9.4.3 delayed_side_effects_observed=true
delayed_moved_users=10.7.0.5,10.0.0.2,10.0.0.3
movement=1 -> vless
```

Updated apply restore approval rule:

- a clean final planner-only gate remains required before restoring apply;
- immediate post-restore `actual_movements_count=0` is not sufficient as final proof;
- post-restore monitoring must cover at least one full apply timer period and should cover multiple periods;
- any delayed movement after restore must be classified as autoswitch recovery or unexpected movement before future canary approval;
- if delayed movement occurs without exact prior approval, canary readiness returns to NO-GO.

Current status:

```text
apply_restore_current_status=RESTORED
delayed_side_effects_observed=true
restore_governance_live_proven=false
approval_status=NO-GO_FOR_NEW_CANARY_UNTIL_DELAYED_MOVEMENT_CLASSIFIED
execution_allowed_now=false
```

## E9.3.9 Runtime Policy Deploy Update

The policy fix is now deployed to runtime:

```text
runtime_policy_deployed=true
runtime_policy_hash=d07a045bd9ad8470e872d4774ac776733a2051b36ec60507a6baf6ca9bab454b
backup_path=/usr/local/bin/v7-users-autoswitch.backup.e9_3_9.20260525T213519Z
apply_timer_remained_held=true
```

Post-deploy planner-only observation showed:

```text
selected_moves=[]
apply_result=no_selected_moves
users.registry_changed=false
egress.registry_changed=false
checkers=OK
```

Updated rule:

```text
apply_restore_safe_after_runtime_deploy=false_until_separate_apply_restore_approval
apply_timer_should_remain_held=true
execution_allowed_now=false
```

Apply restore can be considered only in a later block with a fresh final planner-only sample and explicit approval for whatever movement list is visible at that time.

## E9.4 Apply Restore Gate Result

E9.4 attempted the bounded post-policy apply restore sequence, but stopped at the final planner-only gate.

```text
apply_restore_executed=false
apply_restore_aborted=true
abort_stage=final_planner_only_gate
final_planner_selected_moves=3
selected_moves=10.7.0.5:1->vless,10.0.0.2:1->vless,10.0.0.3:1->vless
apply_timer_remained_held=true
execution_allowed_now=false
```

Updated rule:

- `selected_moves=0` remains mandatory for automatic apply restore;
- non-zero selected moves require a new exact-move approval packet;
- policy deploy alone is not sufficient to restore apply authority;
- apply restore remains NO-GO until the post-policy `current_egress_not_eligible` cause is classified.

## E9.4.1 Post-Policy Root-Cause Classification

E9.4.1 classified the E9.4 final gate:

```text
post_policy_egress_1_root_cause=telegram_required_telegram_down_14s
root_cause_classification=TELEGRAM_HARD_BLOCK
confidence=high_for_E9_4_abort_sample_medium_for_current_recovered_state
candidate_moves_count=16
selected_moves_count=3
selected_moves=10.7.0.5:1->vless,10.0.0.2:1->vless,10.0.0.3:1->vless
policy_fix_incomplete=false
```

Updated apply restore rule:

- automatic apply restore still requires a fresh final planner-only sample with `selected_moves=0`;
- if selected moves are non-zero because of Telegram hard-block, apply restore requires exact operator approval of the movement list;
- a single non-Telegram service degradation is not sufficient to block apply restore under the deployed policy;
- apply timer remains held until a new bounded restore block is approved.

```text
apply_restore_safe_now=false
apply_should_remain_held=true
execution_allowed_now=false
```

## E9.4.6 Fresh Restore-Settle Observation

E9.4.6 observed the already-restored apply timer state without live mutation.

```text
fresh_restore_settle_status=GO
samples_count=3
samples_span_seconds=68
apply_timer_intervals_covered=3.4
selected_moves_by_sample=[0,0,0]
telegram_hard_blocked_by_sample=[false,false,false]
egress_1_eligible_by_sample=[true,true,true]
registry_stable=true
runtime_checks_ok=true
new_delayed_movements_observed=false
```

Updated approval implication:

- the current runtime settle window is clean;
- restore governance is live-proven for this fresh window;
- this does not grant canary execution;
- the next allowed step is a new approval packet or target refresh using current registry truth.

## E10 Approval Packet Boundary

E10 confirms that apply-restore governance and canary-target approval are separate gates.

```text
restore_settle_gate_status=GO
second_canary_approval_status=NO-GO
selected_target=NONE
execution_allowed_now=false
```

Apply restore can be considered governed only when the restore-settle gate is fresh and GO. A canary still requires a separate target decision. E10 found no acceptable target, so no canary execution is allowed even though restore-settle status is GO.

## E10.1 Apply Restore Boundary

E10.1 is target remediation planning only. It does not change apply-restore approval rules.

```text
restore_settle_gate_status=GO
remediation_candidate=awg0
policy_apply_required=false
apply_restore_required_for_remediation=false
execution_allowed_now=false
```

Future `awg0` metadata remediation must not start/stop autoswitch timers and must not run autoswitch apply. After any separate approved metadata mutation, restore-settle and runtime checks must be rerun before canary approval is reconsidered.
