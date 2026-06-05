# PROGRAM SMALL BATCH 2 USER COHORT CERTIFICATION AND AUTHORITY PROMOTION EVIDENCE REPORT

Project: V7 Vozduh
Workspace: /Users/ponch/Documents/New project
Branch: Updatesystem
Date: 2026-06-05

## Executive Verdict

SMALL_BATCH authority promotion was applied after explicit operator confirmation, but the first real 2-user cohort was not certified.

The governed execution path correctly refused to move users when production runtime snapshot truth became inconsistent with live source truth. The result is a safe NOOP, not an unsafe partial execution.

No users were moved. Rollback is not required.

## Scope

Requested cohort:

- 10.0.0.3: awg3 -> vless
- 10.0.0.6: awg3 -> vless
- max selected moves: 2
- live governed apply requested with --apply --verify

Allowed path:

Recommendation -> Approval Packet -> Execution Recheck -> Restore Barrier -> Governed Apply -> Verification -> Outcome -> Feedback -> Closure

No new planner, governance owner, execution path, rollback authority, truth source, or snapshot root was created.

## Evidence Folder

Evidence directory:

- small_batch_cohort_evidence/

Key files:

- phase1_truth_before_policy.json
- phase2_policy_promotion_result.json
- phase2_policy_after.json
- phase3_small_batch_plan_before_clearance.json
- phase4_small_batch_approval_packet.json
- phase5_approval_packet_recheck.json
- phase5_restore_barrier_clearance_execute.json
- phase5_execution_recheck_plan_after_clearance.json
- phase6_small_batch_execution_bundle.txt
- phase6_retry_fresh_plan.json
- phase6_retry_approval_packet.json
- phase6_retry_clearance_and_apply_bundle.txt
- phase7_truth_after_noop.json
- phase7_production_after_noop_readonly.txt

## Phase Results

### Phase 1 - Truth Baseline

Production truth before authority promotion was aligned.

Post-run truth check:

- final_verdict: PASS
- convergence_status: FULLY_ALIGNED
- runtime_truth_status: KNOWN
- state_truth_status: KNOWN
- current_commit: a50dac8a911f0dc98a496705729e48d4de2a9a0b
- remote_branch_commit: a50dac8a911f0dc98a496705729e48d4de2a9a0b

Evidence:

- phase7_truth_after_noop.json

### Phase 2 - Authority Promotion

After explicit operator confirmation, production authority policy was promoted:

- authority_class: SMALL_BATCH
- current_allowed_user_budget: 2
- next_allowed_user_budget: 5
- evidence_floor: one_successful_governed_execution_plus_operator_approved_small_batch

Evidence:

- phase2_policy_promotion_result.json
- phase2_policy_after.json
- phase7_production_after_noop_readonly.txt

### Phase 3 - Recommendation / Planner

The planner selected exactly two cohort moves after pre-planner snapshot refresh and runtime recheck:

- selected_move_count: 2
- selected_move_hash: fcbbb6b0bb355003c3cf794875a78d68ce4a52d05c0c1ecfa94c761b7ef35438
- selected users:
  - 10.0.0.3 awg3 -> vless
  - 10.0.0.6 awg3 -> vless
- terminal_state: DRY_RUN
- terminal_reason: dry_run_selected_moves_available

Snapshot gate was clean at this stage:

- stop_required: false
- source_mismatch_families: []

Evidence:

- phase3_small_batch_plan_before_clearance.json
- phase5_execution_recheck_plan_after_clearance.json

### Phase 4 - Approval Packet

Approval packet was generated for the selected cohort:

- packet_id: pkt_ecd7382c305c4f8a1130774f
- approval_id: appr_2b9ce0c240ad8028f305bb53
- allowed_users:
  - 10.0.0.3
  - 10.0.0.6
- allowed_targets:
  - vless
- selected_move_budget: 2
- selected_move_hash: fcbbb6b0bb355003c3cf794875a78d68ce4a52d05c0c1ecfa94c761b7ef35438
- rollback target for both users: awg3

Evidence:

- phase4_small_batch_approval_packet.json
- phase6_retry_approval_packet.json

### Phase 5 - Restore Barrier Clearance

Restore barrier clearance was written and matched the selected generation/hash:

- clearance_max_selected_moves: 2
- clearance_expected_selected_moves: 2
- clearance_generation_ok: true
- clearance_generation_reason: restore_barrier_clearance_generation_match
- clearance_guard_reason: restore_barrier_clearance_budget_and_generation_ok

Evidence:

- phase5_approval_packet_recheck.json
- phase5_restore_barrier_clearance_execute.json
- phase6_retry_clearance_and_apply_bundle.txt

### Phase 6 - Governed Apply

Two governed apply attempts occurred after explicit operator confirmation.

Attempt 1:

- result: NOOP
- terminal_state: NOOP
- terminal_reason: no_selected_moves
- cause: restore barrier clearance expired before apply
- users moved: 0

Attempt 2:

- fresh approval packet generated
- fresh restore barrier clearance written
- authority gate allowed selected_moves <= 2
- restore barrier generation/hash matched
- result: NOOP
- terminal_state: NOOP
- terminal_reason: no_selected_moves
- users moved: 0

Blocking condition in attempt 2:

- intelligence_snapshots.stop_required: true
- source_mismatch_families:
  - service-scores
  - channel-service-scores
- selected_moves_before_gate: 2
- selected_moves_suppressed: true
- selected_moves_after_gate: 0

Specific mismatch evidence:

- source_hash_mismatch:service-scores:service_matrix
- source_hash_mismatch:channel-service-scores:service_matrix

Later read-only dry-run also showed mismatch against quality_summary:

- source_hash_mismatch:service-scores:quality_summary
- source_hash_mismatch:channel-service-scores:quality_summary

Evidence:

- phase6_small_batch_execution_bundle.txt
- phase6_retry_clearance_and_apply_bundle.txt
- phase7_production_after_noop_readonly.txt

### Phase 7 - Post-Run Runtime State

Production read-only check confirmed no user movement:

- 10.0.0.3 current=awg3
- 10.0.0.6 current=awg3

No rollback is required because no forward movement occurred.

Evidence:

- phase7_production_after_noop_readonly.txt

## Safety Audit

No prohibited action was taken:

- no direct user movement outside governed apply
- no autoswitch bypass
- no manual route mutation
- no new planner
- no new governance authority
- no new execution authority
- no new rollback authority
- no new truth source
- no new snapshot root
- no snapshot gate bypass
- no rollback path bypass

The production safety gates behaved correctly:

- stale/expired restore barrier blocked attempt 1
- snapshot/source mismatch blocked attempt 2
- both blocks produced NOOP instead of unsafe movement

## Root Cause

The current architecture can produce a valid 2-user plan and a valid restore barrier clearance, but the live production source inputs can change between snapshot refresh and apply.

For one-user CANARY execution, apply-time pre-planner refresh is supported in bounded scope. For SMALL_BATCH=2, the existing implementation does not allow apply-time internal pre-planner refresh, so the runtime must rely on externally refreshed snapshots. In production, that was not stable enough for the 2-user cohort apply window.

This is not a governance failure. It is a convergence/atomicity gap between:

- snapshot refresh
- source reload
- restore barrier clearance
- apply-time snapshot validation

## Authority Score

authority_score_defined: true

Score outcome:

- cohort_success_credit: 0
- reason: no production user movement occurred
- authority_should_not_advance: true
- promotion_to_medium_batch_allowed: false

The SMALL_BATCH policy is currently present on production, but SMALL_BATCH execution is not certified by this run.

## Final Verdicts

small_batch_completed=false

production_authority_promoted=true

current_authority_class=SMALL_BATCH

current_allowed_user_budget=2

next_allowed_user_budget=5

selected_users_identified=true

approval_packet_created=true

execution_recheck_passed=true

restore_barrier_clearance_created=true

governed_apply_attempted=true

users_moved=0

verification_passed=false

rollback_required=false

rollback_executed=false

outcomes_materialized=false

trust_feedback_updated=false

prediction_feedback_updated=false

recommendation_feedback_updated=false

authority_score_defined=true

snapshot_source_consistency_blocker=true

safe_for_next_cohort=false

safe_for_bounded_autonomy=false

safe_for_production_autonomy=false

new_truth_sources_created=false

duplicate_systems_created=false

tests_pass=true

truth_check_pass=true

## Required Next Step

SAFE_NEXT_STEP=PROGRAM_SMALL_BATCH_SNAPSHOT_ATOMICITY_FIX_OR_AUTHORITY_DEMOTION

Required decision before any further cohort:

1. Either demote/freeze production authority back to CANARY until the SMALL_BATCH snapshot/apply atomicity blocker is fixed.
2. Or implement a scoped fix that makes multi-user governed apply use a single consistent runtime truth envelope across snapshot refresh, source reload, restore barrier clearance, and apply-time validation.

Do not retry SMALL_BATCH live movement until this blocker is closed.

