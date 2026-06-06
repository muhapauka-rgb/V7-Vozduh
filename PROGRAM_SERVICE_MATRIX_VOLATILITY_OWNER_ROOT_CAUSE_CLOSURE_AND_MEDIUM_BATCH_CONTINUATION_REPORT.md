# PROGRAM SERVICE MATRIX VOLATILITY OWNER ROOT CAUSE CLOSURE AND MEDIUM BATCH CONTINUATION REPORT

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Runtime code-fix commit: `203e209c29b6b808475d75348403de41b1f08b34`

Report/evidence commit: tracked separately after execution; production fingerprint may point to the report/evidence commit when safe deploy is used to keep local/GitHub/production truth aligned.

Evidence folder: `service_matrix_volatility_evidence/`

## Mission Result

The service-matrix volatility blocker was closed and MEDIUM_BATCH execution continued through the governed path.

Exactly 5 approved users were moved to `vless` through existing planner, packet, restore-barrier, apply, and verification ownership.

No autonomy was enabled. No LARGE_BATCH authority was enabled. No alternate planner, governance owner, execution path, truth source, or snapshot root was created.

## Root Cause

The original blocker was not a bad target selection and not a planner scoring bug.

The service truth source `service-matrix.json` had multiple live writers:

- `v7-service-matrix-refresh.timer` -> `v7-service-matrix-refresh.service` -> `/usr/local/bin/v7-service-matrix-refresh-all`
- `/usr/local/bin/v7-service-matrix-test`
- `v7-telegram-sentinel.timer` -> `v7-telegram-sentinel.service` -> `/usr/local/bin/v7-telegram-sentinel`

The first lock fix serialized `v7-service-matrix-refresh-all`, `v7-service-matrix-test`, and planner lifecycle reads, but `v7-telegram-sentinel` still wrote `service-matrix.json` every 4 seconds. That kept changing the source during planner snapshot lifecycle and caused fail-closed behavior.

Evidence:

- `production_writer_discovery.txt`
- `post_envelope_fix_process_check.txt`
- `service_matrix_idle_stability_probe.txt`
- `telegram_sentinel_writer_check.txt`

## Fixes Applied

### 1. Service Matrix Writer Lock

Commit: `945fdcd Serialize service matrix writer and planner lifecycle`

Added shared lock ownership for:

- `tools/v7-users-autoswitch`
- `tools/v7-service-matrix-refresh-all`
- `tools/v7-service-matrix-test`

### 2. Safe Deploy Truth Coverage

Commits:

- `7a4f676 Add service matrix tools to safe deploy truth`
- `b78edba Record service matrix executable truth in deploy snapshot`

Added service matrix runtime tools into safe deploy/truth check surface.

### 3. Nonzero Packet Atomic Envelope Binding

Commit: `06a6376 Fix nonzero packet atomic envelope binding`

Fixed a governance contract bug where the approval packet for pre-barrier selected moves reused the atomic envelope from `selected_moves=0`. The packet now binds the expected envelope to the approved nonzero move set.

### 4. Telegram Sentinel Serialization

Commit: `203e209 Serialize telegram sentinel service matrix writes`

Added the same `service-matrix.lock` to `v7-telegram-sentinel` and registered the sentinel binary in safe deploy runtime truth.

## Verification

Tests:

- `python3 -m unittest tests.unit.test_operator_execution_packet`: PASS
- `python3 -m unittest tests.unit.test_v7_users_autoswitch_policy`: PASS
- `python3 -m unittest tests.unit.test_v7_sync_tools tests.unit.test_v7_truth_check tests.unit.test_runtime_snapshot_fast_path`: PASS
- `python3 -m unittest discover tests`: PASS, 352 tests

Production convergence:

- `final_truth_check.json`: PASS / FULLY_ALIGNED
- `final_convergence_status.json`: PASS / ALIGNED / READY_FOR_RUNTIME_ACTION

Post-fix planner:

- `fresh_planner_after_sentinel_lock.json`: snapshot gate clean, no source mismatch
- `dry_run_recheck_after_sentinel_lock.json`: 5 selected moves available, restore barrier valid

## Real Governed Apply

Execution evidence:

- `real_governed_apply_after_sentinel_lock.json`

Approved users moved:

- `10.7.0.4`: `amneziawg-exec-20260528-10-8-1-14` -> `vless`
- `10.7.0.6`: `amneziawg-exec-20260528-10-8-1-14` -> `vless`
- `10.7.0.8`: `amneziawg-exec-20260528-10-8-1-14` -> `vless`
- `10.7.0.9`: `awg0` -> `vless`
- `10.7.0.10`: `awg0` -> `vless`

Verification:

- `users_moved=5`
- `only_approved_users_moved=true`
- `verification_passed=true`
- `rollback_required=false`
- `rollback_attempted=false`

## Feedback Closure

Feedback materialization evidence:

- `feedback_materialization_after_medium_apply.json`
- `final_runtime_feedback_state.txt`

Materialized for all 5 users:

- outcome feedback
- trust feedback
- prediction feedback
- recommendation feedback
- closure records

All feedback rows returned status `200`, outcome `success`, and closure `CLOSED`.

## Final Verdicts

service_matrix_writer_identified=true

service_matrix_change_expected=true

service_matrix_bug_fixed=true

telegram_sentinel_writer_serialized=true

packet_atomic_envelope_bug_fixed=true

lock_fix_deployed=true

convergence_aligned=true

snapshot_stop_required=false

source_mismatch_families=[]

fresh_packet_created=true

restore_barrier_fresh=true

dry_run_recheck_pass=true

medium_batch_continuation_executed=true

users_moved=5

apply_executed=true

only_approved_users_moved=true

verification_passed=true

rollback_required=false

outcomes_materialized=true

trust_feedback_updated=true

prediction_feedback_updated=true

recommendation_feedback_updated=true

medium_batch_execution_certified=true

SAFE_NEXT_STEP=MEDIUM_BATCH_STABILITY_WINDOW_OBSERVATION_AND_POST_EXECUTION_CERTIFICATION
