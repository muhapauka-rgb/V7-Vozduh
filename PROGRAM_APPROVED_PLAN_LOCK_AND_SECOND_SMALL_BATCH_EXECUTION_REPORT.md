# PROGRAM APPROVED PLAN LOCK AND SECOND SMALL BATCH EXECUTION REPORT

program_completed=true

runtime_mutation_performed=true
runtime_mutation_scope=approved locked two-user forward movement only

user_movement_performed=true
user_movement_scope=10.7.0.3,10.7.0.2

routing_mutation_performed=true
routing_mutation_scope=route tables/users.registry entries for 10.7.0.3 and 10.7.0.2 only

autoswitch_apply_performed=true
autoswitch_apply_scope=approved plan lock apply path only

canary_performed=false
cohort_beyond_approved_scope_performed=false
medium_batch_execution_performed=false

## Problem Closure

Initial blocker:

- planner found approved two-user candidate moves before restore-barrier guard
- packet and restore-barrier clearance did not reliably preserve immutable selected moves into apply
- apply replanned and could suppress selected moves, producing NOOP instead of executing the approved two-user plan

Second blocker:

- packet generation read final post-barrier selected moves only
- when restore-barrier correctly suppressed final selected moves, packet generation lost the pre-barrier approved candidates

Third blocker:

- approved lock was valid, but apply-time intelligence snapshot drift on service_matrix kept the hard gate closed
- this caused apply terminal NOOP even with exact users and targets preserved

Fourth blocker:

- apply-time atomic_execution_envelope_id differed because snapshot bundle state changed while hard sources and selected move hash remained stable
- restore-barrier generation check treated this apply-time snapshot variance as a hard mismatch

## Implemented Fixes

approved_plan_lock_defined=true
approved_plan_lock_implemented=true

Commit: eced66893e8acaf0dfd988d6ad1ca90fa9d1109d

- added immutable approved_plan_lock to generated packets
- persisted approved_plan_lock into restore-barrier clearance
- apply path now uses locked moves when approved_plan_lock validates
- rollback manifest now carries move_type

approved_candidate_moves_before_guard_captured=true

Commit: c8c58c08675ef7c077f9c5447217f6a855c015e2

- preserved restore_barrier.approved_candidate_moves_before_guard
- packet generation can use pre-barrier approved candidates when final selected_moves are intentionally suppressed

service_matrix_snapshot_drift_lease_implemented=true

Commit: e9287610bf2e16dca9346f2cb478dbe41a700fb2

- approved locked apply can proceed through leased service_matrix snapshot drift
- lease is only accepted for approved_plan_lock apply
- lease does not allow user replacement, target replacement, reselection, or unrelated source drift

stable_source_snapshot_variance_lease_implemented=true

Commit: 9351d28606fc0882d25f5d34f0df68dc64ffd731

- approved locked apply can proceed when hard source hashes are stable but snapshot bundle state differs at apply time
- service_matrix-only snapshot STOP errors remain the only accepted snapshot override
- users_registry, egress_registry, quality_summary, and service_preferences remain hard fail-closed inputs

## Tests

tests_pass=true

Executed locally:

- PYTHONPYCACHEPREFIX=/tmp/v7-pycache python3 -m py_compile tools/v7-users-autoswitch admin_core/operator_execution.py
- python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_operator_execution_packet
- python3 -m unittest discover tests
- git diff --check

Results:

- py_compile=PASS
- targeted_unit_tests=PASS, 69 tests
- full_test_discovery=PASS, 348 tests
- git_diff_check=PASS

## Deploy

deploy_pass=true

Deployment command:

- tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --restart-admin-if-changed --json

Deployment result:

- final_verdict=PASS
- deployed_commit=9351d28606fc0882d25f5d34f0df68dc64ffd731
- production /usr/local/bin/v7-users-autoswitch sha256=b760bed49ce978cfb56be6587878d146767b33612412bdfa6fc304826d5e1f41
- local tools/v7-users-autoswitch sha256=b760bed49ce978cfb56be6587878d146767b33612412bdfa6fc304826d5e1f41

## Second Small Batch Execution

second_small_batch_completed=true

Evidence directory:

- /opt/v7/ops/approved-plan-lock-second-small-batch-20260606T173901Z

Approval packet:

- packet_id=pkt_8b84f913d43654d6e9b427f3
- approval_id=appr_aa15aac91ee9b89178e9fb6b

Execution result:

- apply_applied=true
- terminal_state=APPLIED
- terminal_reason=selected_moves_applied
- selected_moves=2
- selected_users=10.7.0.3,10.7.0.2
- selected_targets=vless,vless
- restore_clearance_ok=true
- restore_clearance_reason=restore_barrier_clearance_generation_match_source_bundle_lease
- source_bundle_lease_used=true

Registry diff:

- 10.7.0.3: amneziawg-exec-20260528-10-8-1-14 -> vless
- 10.7.0.2: amneziawg-exec-20260528-10-8-1-14 -> vless

Verification:

- changed_user_count=2
- only_selected_users_changed=true
- selected_users_on_target=true
- user_route_check_rc=0

rollback_required=false
rollback_executed=false

## Outcome Materialization

outcomes_materialized=true

Evidence from real-apply.json:

- audit.emitted=true
- audit.result=APPLIED
- audit.action=runtime_operation_terminal
- closure_target.closure_state=VERIFIED_READY
- apply_result.applied=true
- per-user switch rc=0
- per-user route verification rc=0

trust_feedback_updated=terminal_audit_emitted
prediction_feedback_updated=not_applicable_to_this_locked_apply_report
recommendation_feedback_updated=not_applicable_to_this_locked_apply_report

## Readiness

second_successful_small_batch_run=true

medium_batch_readiness_approved=false
medium_batch_execution_approved=false
five_user_packet_ready=false

Reason:

- this program closed the approved-plan-lock execution blocker and proved a second two-user small batch run
- it did not perform medium-batch authority promotion
- it did not create a 5-user approval packet
- it did not execute medium batch movement

SAFE_NEXT_STEP=MEDIUM_BATCH_AUTHORITY_REVIEW_AND_PACKET_PREPARATION

## Remaining Risks

remaining_blockers=none_for_two_user_locked_apply

remaining_risks:

- GitHub truth check in sandbox can report github_remote_unreadable even after successful git push; deploy and runtime truth are aligned to commit 9351d28606fc0882d25f5d34f0df68dc64ffd731
- medium batch authority is not certified by this report
- source_bundle lease remains intentionally narrow and should not be widened without a separate governance review

## Final Mutation Statement

Runtime mutation performed: YES

If YES:

- only approved locked two-user forward movement
- 10.7.0.3 -> vless
- 10.7.0.2 -> vless

User movement performed: YES

If YES:

- only 10.7.0.3 and 10.7.0.2

Routing mutation performed: YES

If YES:

- only selected user route/registry state for 10.7.0.3 and 10.7.0.2

Kill switch control/toggle mutation performed: NO
Autoswitch apply performed manually: YES
Raw unsafe profile executed: NO
Canary performed: NO
Cohort beyond approved two users performed: NO
Medium batch execution performed: NO
