# PROGRAM MEDIUM BATCH TARGET DRIFT CLOSURE AND REAL 5 USER EXECUTION REPORT

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Date: 2026-06-06

## Executive Verdict

The original target drift `vless -> awg3` was investigated and partially closed.

The first drift was an expected planner decision caused by current service/load truth changing the best target. The system correctly refused to apply an old `vless` approval packet after the planner selected `awg3`.

During bounded retry, a deeper blocker was proven: `service_matrix` continues to change between pre-planner snapshot refresh and snapshot gate validation, even after a new bounded post-reload refresh fix was implemented and deployed.

Because the snapshot gate remained unstable through retry #3, no governed apply was executed and no users were moved.

## Target Drift Root Cause

Classification: `SNAPSHOT_DRIFT`

Supporting classification details:

- initial visible symptom: `EXPECTED_BETTER_TARGET`
- deeper proven blocker: `SERVICE_TRUTH_VOLATILITY` / `SNAPSHOT_DRIFT`

Phase 2 selected:

- target: `vless`
- healthy egress total: `1`
- recommended score: `1974.91`

Phase 5 selected:

- target: `awg3`
- healthy egress total: `2`
- recommended score: `2080.71`

The target changed because service/load truth changed and the planner picked the better current target. This part is expected behavior.

However, subsequent retries showed that `service_matrix` changes after snapshot refresh, causing:

- `source_hash_mismatch:service-scores:service_matrix`
- `source_hash_mismatch:channel-service-scores:service_matrix`
- `dry_run_intelligence_snapshot_stop_required`

Evidence:

- `medium_batch_controlled_live_evidence/phase2_fresh_planner_remote.json`
- `medium_batch_controlled_live_evidence/phase5_dry_run_recheck.json`
- `medium_batch_target_drift_evidence/attempt1_snapshot_stop_diagnostics.json`
- `medium_batch_target_drift_evidence/attempt2_snapshot_stop_diagnostics.txt`

## Decision To Action

Decision:

- do not force the old `vless` packet;
- regenerate packet from current planner state only;
- if source volatility appears, close it before apply.

Action taken:

1. Ran bounded retry #1 from fresh planner.
2. Generated a fresh 5-user packet for current target.
3. Wrote fresh restore barrier through canonical owner.
4. Rechecked dry-run.
5. Found snapshot stop caused by `service_matrix` source mismatch.
6. Implemented a bounded post-source-reload snapshot refresh retry in `tools/v7-users-autoswitch`.
7. Added regression test.
8. Ran targeted and full tests.
9. Committed, pushed, and safe-deployed the fix.
10. Retried bounded planner twice.

Code commit:

- `e402a1d Fix pre-planner snapshot source drift retry`

Deploy:

- `medium_batch_target_drift_evidence/safe_deploy_snapshot_retry_fix.json`

## Fix Implemented

Changed existing pre-planner refresh behavior in `tools/v7-users-autoswitch`.

Before:

1. run snapshot refresh;
2. reload service matrix / quality summary / preferences;
3. validate snapshots.

If the source changed after refresh, snapshots could be fresh by timestamp but stale by source hash.

After:

1. run snapshot refresh;
2. reload source files;
3. if source changed, run one bounded post-reload refresh retry;
4. reload source files again;
5. if source changed again, fail closed with `SOURCE_VOLATILE_AFTER_POST_RELOAD_RETRY`.

This does not create a new planner, governance path, execution path, or truth source. It tightens the existing pre-planner refresh gate.

Tests:

- `tests.unit.test_runtime_snapshot_fast_path`: PASS
- `tests.unit.test_v7_users_autoswitch_policy`: PASS
- full `python3 -m unittest discover tests`: PASS, 351 tests

Evidence:

- `medium_batch_target_drift_evidence/full_unittest_after_snapshot_retry_fix.txt`

## Bounded Retry Results

### Attempt 1

Fresh planner:

- authority: `MEDIUM_BATCH`
- budget: `5`
- selected before authority gate: `5`
- selected after authority gate: `5`
- target: `vless`

Packet:

- packet id: `pkt_aa9b856a058a3fbe96d0ce97`
- users: `10.7.0.4`, `10.7.0.6`, `10.7.0.8`, `10.7.0.9`, `10.7.0.10`
- target: `vless`
- rollback items: `5`

Restore barrier:

- `ALLOW_RESTORE_BARRIER_CLEARANCE`
- `RESTORE_BARRIER_CLEARANCE_WRITTEN`

Dry-run recheck:

- selected move hash matched;
- restore barrier guard: `restore_barrier_clearance_budget_and_generation_ok`;
- blocked by snapshot gate:
  - `dry_run_intelligence_snapshot_stop_required`
  - `source_hash_mismatch:service-scores:service_matrix`
  - `source_hash_mismatch:channel-service-scores:service_matrix`

Apply executed: false.

Evidence:

- `medium_batch_target_drift_evidence/attempt1_fresh_planner.json`
- `medium_batch_target_drift_evidence/attempt1_approval_packet.json`
- `medium_batch_target_drift_evidence/attempt1_restore_barrier_clearance.json`
- `medium_batch_target_drift_evidence/attempt1_dry_run_recheck.json`

### Attempt 2

After fix deploy, fresh planner still failed closed:

- pre-refresh state: `SOURCE_VOLATILE_AFTER_POST_RELOAD_RETRY`
- source reload changed keys: `service_matrix`
- post-retry reload changed keys: `service_matrix`
- snapshot stop families: `service-scores`, `channel-service-scores`

Apply executed: false.

Evidence:

- `medium_batch_target_drift_evidence/attempt2_fresh_planner.json`
- `medium_batch_target_drift_evidence/attempt2_snapshot_stop_diagnostics.txt`

### Attempt 3

Final bounded retry still failed closed:

- pre-refresh state: `SOURCE_VOLATILE_AFTER_POST_RELOAD_RETRY`
- source reload changed keys: `service_matrix`
- post-retry reload changed keys: `service_matrix`
- snapshot stop families: `service-scores`, `channel-service-scores`
- restore barrier guard: `restore_barrier_clearance_selected_moves_hash_mismatch`

Apply executed: false.

Evidence:

- `medium_batch_target_drift_evidence/attempt3_fresh_planner.json`

## Production Truth After Stop

Final read-only checks:

- truth check: `PASS`, `FULLY_ALIGNED`
- convergence: `PASS`, `ALIGNED`
- runtime action status: `READY_FOR_RUNTIME_ACTION`

Evidence:

- `medium_batch_target_drift_evidence/final_stop_truth_check.json`
- `medium_batch_target_drift_evidence/final_stop_convergence_status.json`

## Final Verdicts

target_drift_root_cause=SNAPSHOT_DRIFT

target_drift_closed=false

fresh_packet_created=true

restore_barrier_fresh=true

dry_run_recheck_pass=false

users_moved=0

only_approved_users_moved=true

verification_passed=false

rollback_required=false

outcomes_materialized=false

trust_feedback_updated=false

prediction_feedback_updated=false

recommendation_feedback_updated=false

medium_batch_execution_certified=false

SAFE_NEXT_STEP=CLOSE_CONTINUOUS_SERVICE_MATRIX_VOLATILITY_OWNER_BEFORE_RETRYING_MEDIUM_BATCH_APPLY

## Required Next Step

Do not retry apply directly.

The next program should identify the writer that changes `/opt/v7/egress/state/service-matrix.json` during the pre-planner refresh window and make that source stable for one planner packet lifecycle.

Required closure options:

1. pause or serialize the service-matrix writer during packet generation and recheck;
2. make `v7-intelligence-snapshot-refresh` own a stable service-matrix input lease for the planner lifecycle;
3. move service-matrix refresh into a single canonical pre-planner transaction;
4. prove two consecutive fresh planners have no `service_matrix` source drift before generating a new packet.

Only after that should MEDIUM_BATCH live apply be retried.
