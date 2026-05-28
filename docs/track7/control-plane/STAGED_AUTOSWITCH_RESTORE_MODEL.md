# Staged Autoswitch Restore Model

Mode: governance design only. This document does not authorize live execution.

## Purpose

E9.3 proved that a held one-user canary can be bounded, but E9.3.1 proved that restoring autoswitch apply authority can immediately move non-candidate users. The restore phase must therefore be staged and governed separately.

## Core Rule

```text
planner restore first;
apply restore only by separate explicit approval.
```

## Stage A — Canary Quiet Hold

Future canary blocks must hold autoswitch mutation authority before any user switch:

```text
v7-autoswitch-planner.timer held
v7-autoswitch-planner.service held
v7-users-autoswitch.timer held
v7-users-autoswitch.service held
v7-health.service active
```

Required status:

```text
canary_window_status=quiet
planner_authority=held
apply_authority=held
health_authority=active
```

## Stage B — Canary Forward / Rollback

Only the approved user may be switched. `v7-routing-sync` and manual autoswitch apply remain forbidden.

Required status:

```text
approved_user_only=true
candidate_route_table_only=true
rollback_command_prepared=true
```

## Stage C — Restore Planner Only

After rollback or canary decision, restore only the non-apply planner authority:

```text
restore v7-autoswitch-planner.timer only
keep v7-users-autoswitch.timer held
```

This stage is intended to reveal planned/pending autoswitch decisions without granting mutation authority.

Required status:

```text
restore_planner_status=planner_only
apply_restore_status=held
runtime_apply_allowed=false
```

## Stage D — Observe Planner-Only

Observe at least two planner periods, or longer if state is changing.

Collect:

- planner service activity;
- selected/pending moves if visible;
- users.registry hash;
- switch-history tail;
- route/rule snapshots;
- four runtime checkers;
- process guard for `v7-user-switch` and `v7-routing-sync`.

Required status:

```text
planner_only_observation_done=true
apply_movement_count=0
pending_moves_classified=true
```

## Stage E — Apply Restore Approval

Restoring `v7-users-autoswitch.timer` is no longer an automatic cleanup step. It is a separate approval gate.

Approval must name:

- expected pending movement count;
- accepted movement reason classes;
- maximum allowed movement count;
- abort conditions;
- post-apply settle duration;
- containment plan if unexpected movement occurs.

Required status:

```text
apply_restore_requires_separate_approval=true
operator_approval_required=true
```

## Stage F — Post-Apply Settle

If apply authority is restored, any movement is classified as autoswitch recovery, not canary movement.

Required status:

```text
post_apply_settle_observed=true
post_restore_movement_classification=autoswitch_recovery_or_unexpected
canary_blast_radius_reported_separately=true
```

## Model Verdict

```text
recommended_restore_model=planner_first_apply_by_separate_approval
future_canary_restore_sequence_safe=false
```

The sequence is safe enough to design and approve in a future live block, but not safe by default until the staged restore process is executed and validated.

## E9.3.3 Planner-Only Rehearsal Result

E9.3.3 executed the planner-first part of this model without a canary.

Result:

```text
planner_restored=true
apply_restored=false
v7_health_active=true
apply_timer_held=true
user_movement_observed=false
routing_drift_observed=false
users.registry_changed=false
planner_only_stage_safe=true
```

The rehearsal proved that restoring planner authority alone can expose pending autoswitch decisions while apply authority remains held.

The final planner-only evidence showed at least three pending failover recommendations:

```text
10.7.0.5: 1 -> awg3
10.0.0.2: 1 -> awg3
10.0.0.3: 1 -> awg3
```

These moves were not applied. `v7-users-autoswitch.timer` remained inactive.

Updated verdict:

```text
future_canary_restore_sequence_safe=conditional_planner_only_stage_proven_apply_not_restored
apply_restore_status=HELD_REQUIRES_SEPARATE_APPROVAL
```

## E9.3.4 Apply Restore Approval Packet Result

E9.3.4 did not restore apply authority. It repeated planner-only observation and found no fresh selected moves:

```text
selected_moves=0
pending_moves_visible=false
apply_timer_held=true
```

This improves the immediate outlook but does not change the staged model. The apply timer remains a separate live authority. Restoring it can still trigger autoswitch recovery outside canary attribution.

Current staged restore state:

```text
planner_only_stage=active
apply_restore_status=HELD
approval_status=CONDITIONAL
execution_allowed_now=false
```

The next live step must be an apply-restore block with its own fresh evidence and explicit operator approval.

## E9.3.5 Apply Restore Execution Gate

E9.3.5 attempted the next bounded apply-restore stage, but only up to the final planner-only gate. The final sample changed from E9.3.4 `selected_moves=0` to:

```text
selected_moves=3
candidate_moves_total=15
selected_moves=10.0.0.2:1->vless,10.0.0.3:1->vless,10.0.0.6:1->vless
reason=current_egress_not_eligible
```

The model therefore required abort before restoring apply authority. `v7-users-autoswitch.timer` remained held.

Updated staged restore state:

```text
planner_only_stage=active
apply_restore_status=HELD_ABORTED_BY_FINAL_PLANNER_SAMPLE
apply_restore_executed=false
actual_movements_count=0
restore_governance_proven=false_apply_restore_not_executed
execution_allowed_now=false
```

This result strengthens the rule that apply restore must be based on an immediate final planner sample, not earlier approval evidence.

## E9.3.6 Egress 1 Ineligibility Root Cause

E9.3.6 explains the E9.3.5 abort:

```text
root_cause=service_instagram_failed on current egress 1
root_cause_classification=MIXED_TRANSIENT_SERVICE_SIGNAL_AND_EXPECTED_FAILOVER_BEHAVIOR
selected_moves=3
candidate_moves_total=15
target=vless
apply_should_remain_held=true
apply_restore_status=HELD
```

The source behavior is expected: when current egress is not eligible, failover decisions are selected up to `autoswitch_max_failover_per_run`. The governance risk is that a transient service signal can create a broad candidate set across all users on one egress.

## E9.4.2 Clean Apply Restore Result

After the E9.3.8 policy fix and E9.3.9 runtime deploy, E9.4.2 retried apply restore with a fresh final planner-only gate.

The gate was clean:

```text
selected_moves=0
egress_1_eligible=true
telegram_hard_blocked=false
```

The apply timer restore was executed as a separate stage:

```text
systemctl start v7-users-autoswitch.timer
```

Observation result:

```text
actual_movements_count=0
apply_restore_clean=true
autoswitch_recovery_bounded=true
```

Updated staged restore state:

```text
planner_only_gate=clean
apply_restore_status=RESTORED_CLEAN
restore_governance_proven=true_for_zero_move_clean_gate
execution_allowed_now=false
```

Future canary blocks must still keep canary execution and restore execution separate. E9.4.2 proves the restore stage can be clean, not that canary execution is generally approved.

## E9.3.7 Transient Service Signal Policy Model

Staged restore now has an additional policy-design dependency:

```text
single service failure -> DEGRADED_SERVICE, not HARD_INELIGIBLE
persistent service failure -> CONDITIONAL_INELIGIBLE
interface/transport/sentinel hard failure -> HARD_INELIGIBLE
```

The restore model should treat service-signal failover as separate from transport failover:

- transport hard failure can justify immediate failover within existing caps;
- single-service failure should only penalize the egress and surface warnings;
- persistent or multi-service failure can propose movement, but apply restore still requires explicit approval;
- during restore, `post_restore_apply_suppression_window_seconds` should suppress broad service-signal failover unless a hard transport signal exists.

Until that policy exists in code, apply restore remains held or sample-bound.

## E9.3.8 Repo Fix Status

The transient service-signal policy now exists in repo code, but not in runtime.

Staged restore sequence remains:

1. deploy patched `/usr/local/bin/v7-users-autoswitch` only after separate approval;
2. keep apply timer held;
3. run planner-only dry-run;
4. confirm single-service transient failure does not produce broad selected moves;
5. only then reassess apply restore.

No staged restore command is authorized by E9.3.8.

## E9.3.9 Runtime Policy Deploy Status

The autoswitch policy refinement is now deployed to `/usr/local/bin/v7-users-autoswitch`.

Staged restore state after deploy:

```text
planner_timer=active
apply_timer=held_inactive
runtime_policy_deployed=true
planner_only_selected_moves=[]
apply_result=no_selected_moves
users.registry_changed=false
egress.registry_changed=false
```

The staged restore sequence remains unchanged:

1. keep apply timer held;
2. collect a fresh final planner-only sample;
3. request separate operator approval for apply restore;
4. restore apply only in a separate bounded block.

E9.3.9 does not authorize apply restore.

## E9.4 Post-Policy Apply Restore Gate

E9.4 used the staged model correctly and aborted before restoring apply authority:

```text
planner_timer=active
apply_timer=held_inactive
runtime_policy_deployed=true
final_planner_selected_moves=3
apply_restore_executed=false
apply_restore_aborted=true
```

The staged model remains valid: it prevented unapproved user movement by exposing selected moves before apply authority returned.

Next model requirement:

```text
post_policy_selected_move_root_cause_required=true
exact_movement_approval_required=true
```

## E9.4.1 Root Cause Closure

E9.4.1 closed the post-policy root-cause question for the E9.4 abort sample.

The staged model worked correctly:

1. planner-only gate observed selected moves;
2. apply authority stayed held;
3. no user movement or routing mutation occurred;
4. root cause was classified before any apply restore.

Root cause:

```text
egress_1_blocker=telegram_required_telegram_down_14s
telegram.hard_blocked=true
instagram_single_sample=DEGRADED_SERVICE only
selected_moves=3
candidate_moves_total=16
```

Current staged restore implication:

```text
apply_restore_status=HELD
fresh_final_planner_gate_required=true
exact_movement_approval_required_if_selected_moves_nonzero=true
execution_allowed_now=false
```

The later E9.4.1 snapshot showed `selected_moves=[]`, so the E9.4 hard block was transient. That recovery does not itself authorize apply restore; the final gate must be repeated in the next live restore block.

## E9.4.3 Delayed Post-Restore Monitoring Result

E9.4.2 restored apply authority after a clean final gate and immediate observation showed no movement. E9.4.3 extended observation and found a delayed timer-driven autoswitch movement after that clean restore:

```text
10.7.0.5: 1 -> vless
10.0.0.2: 1 -> vless
10.0.0.3: 1 -> vless
movement_ts=2026-05-26T07:29:08Z
```

Later samples stabilized:

```text
selected_moves=[]
apply_result.applied=false
checks=OK
routing_drift_observed=false
```

Updated staged restore implication:

```text
restore_governance_live_proven=false
reason=delayed_timer_driven_apply_movement_after_clean_restore
future_canary_restore_sequence_safe=false_until_delayed_restore_window_is_governed
```

The staged model must now include a post-apply delayed-settle stage, not only an immediate post-apply sample. A future clean restore should require at least one full apply timer period, preferably multiple periods, with no new switch-history entries and `selected_moves=[]` before canary planning resumes.

## E9.4.4 Delayed-Settle Stage Requirement

E9.4.4 showed that the model must include more than immediate post-restore observation.

Observed sequence:

```text
clean_gate_selected_moves=0
immediate_post_restore_movements=0
delayed_timer_cycle_selected_moves=3
movement_ts=2026-05-26T07:29:08Z
```

Root cause:

```text
telegram.status=TELEGRAM_DOWN_14S
egress_1_blocker=telegram_required_telegram_down_14s
candidate_moves_total=16
selected_moves=3
```

New mandatory stage:

```text
STAGE G — Delayed post-apply settle
  observe at least two full apply timer intervals
  require no new switch-history/safety incoming entries
  require selected_moves=[] in repeated planner/apply output
  classify any movement as autoswitch recovery outside canary boundary
```

Future restore cannot be marked live-proven until STAGE G passes.

## E9.4.5 Restore Settle Gate

The staged restore model now requires a formal gate before and after apply timer restore.

```text
STAGE C1 — Pre-restore settle gate
  collect at least 3 consecutive planner/apply state samples
  span at least 2 full apply timer intervals
  require selected_moves=0 throughout
  require telegram.hard_blocked=false throughout
  require egress_1_eligible=true throughout
  require registry hashes stable
  require runtime checkers OK

STAGE G — Post-restore settle gate
  observe at least 2 full apply timer intervals after timer restore
  require movement_count=0 for clean restore
  classify any movement as autoswitch recovery
  keep next canary NO-GO if broad/delayed movement appears
```

`tools/v7-restore-settle-gate` is the repo-side read-only checker for saved samples and fixtures. It does not start or stop timers and does not invoke autoswitch apply.

Current E9.4.5 status:

```text
restore_settle_gate_rules_created=true
restore_settle_checker_created=true
current_restore_settle_status=NO-GO
restore_governance_live_proven=false
execution_allowed_now=false
```

## E9.4.6 Fresh Settle Observation

E9.4.6 collected a new read-only settle window after the E9.4.4 hard-block recurrence.

```text
current_restore_settle_status=GO
pre_restore_gate=GO
post_restore_settle_view=GO
samples_span_seconds=68
apply_timer_intervals_covered=3.4
selected_moves_all_zero=true
telegram_hard_blocked_seen=false
egress_1_eligible_all_samples=true
registry_stable=true
checks_ok=true
new_delayed_movements_observed=false
```

The staged model remains mandatory. The clean E9.4.6 window means future canary planning can return to approval-packet mode, not execution mode.

## E10 Fresh Second Canary Packet Implication

E10 used the staged restore model as an approval-packet prerequisite, not as execution approval.

```text
restore_settle_gate_status=GO
restore_governance_live_proven=true
candidate_user=10.7.0.11
selected_target=NONE
second_canary_approval_status=NO-GO
execution_allowed_now=false
```

The staged lifecycle remains mandatory for any future canary:

1. hold planner and apply;
2. execute one explicitly approved user switch only;
3. observe quiet window;
4. rollback or keep by separate approval;
5. restore planner only;
6. run restore-settle gate across at least two apply intervals;
7. restore apply only by separate approval when the settle gate is GO;
8. run post-restore settle monitoring.

E10 does not approve Stage A execution because no clean target was selected.
