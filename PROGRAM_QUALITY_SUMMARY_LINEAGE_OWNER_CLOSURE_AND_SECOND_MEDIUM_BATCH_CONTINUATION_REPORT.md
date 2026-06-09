# PROGRAM QUALITY SUMMARY LINEAGE OWNER CLOSURE AND SECOND MEDIUM BATCH CONTINUATION REPORT

Project: V7 Vozduh

Branch: Updatesystem

Date: 2026-06-07

Evidence folder: `quality_summary_lineage_evidence/`

## Executive Verdict

The `quality_summary` blocker was real and was closed at the owner/lifecycle level.

`quality_summary` is not a passive snapshot artifact. It is an independent mutable runtime source written by `tools/v7-egress-quality-compact` into `/opt/v7/egress/state/egress-quality-summary.json`.

The original failure was not safely fixable by widening source-bundle exceptions. The safe fix was to bind the existing writer to the existing runtime lifecycle:

1. Serialize `v7-egress-quality-compact` with the existing `service-matrix.lock`.
2. Add `v7-egress-quality-compact` to the approved deploy/truth coverage.
3. Bind `v7-egress-quality-compact` to active restore-barrier clearance windows so it skips writes while a nonzero approved plan is live.

Second MEDIUM execution was not performed.

Reason: after `quality_summary` was closed, final dry-run still stopped on `dry_run_intelligence_snapshot_stop_required` caused by service-matrix-only drift. Restore barrier accepted the existing `service_matrix` source-bundle lease, but dry-run did not materialize selected moves because the intelligence snapshot gate remains stop-required in dry-run mode. Applying anyway would have violated the program requirement that dry-run recheck must pass before real apply.

## Owner And Lineage

Owner:

- Writer: `tools/v7-egress-quality-compact`
- State file: `/opt/v7/egress/state/egress-quality-summary.json`
- Reader: `tools/v7-users-autoswitch`
- Snapshot reader: `tools/v7-intelligence-snapshot-refresh`
- Runtime systemd owner: `v7-egress-quality-compact.service` / `v7-egress-quality-compact.timer`

Lineage:

`v7-state.json` + `egress-speed.json` + `service-matrix.json`
→ `v7-egress-quality-compact`
→ `egress-quality-summary.json`
→ planner scoring / intelligence snapshots / snapshot source hashes

Classification:

`quality_summary_lineage=INDEPENDENT_MUTABLE_RUNTIME_SOURCE`

Root cause:

`RACE_CONDITION`

Detailed cause:

- `service_matrix` already had lifecycle locking.
- `quality_summary` was a hard source in atomic execution envelopes but its writer could run independently during packet/barrier/apply windows.
- Approved deploy/truth coverage initially omitted `v7-egress-quality-compact`, so the first code fix could not be fully production-converged.
- After deploy coverage was fixed, the remaining lifecycle gap was timer writes during active restore-barrier TTL.

## Fixes Implemented

Commits:

- `5b8c267` Serialize quality summary lifecycle writes
- `c541146` Add quality compactor to deploy truth coverage
- `538b5eb` Align quality compactor truth snapshot commands
- `9e4d637` Bind quality compactor to restore barrier lifecycle

Files changed:

- `tools/v7-egress-quality-compact`
- `tests/unit/test_egress_quality_compact_lifecycle.py`
- `tools/v7_sync_lib.py`
- `tools/v7-truth-check`

Behavior added:

- `v7-egress-quality-compact` acquires `service-matrix.lock`.
- If lock is unavailable, it exits with `LOCK_TIMEOUT` and writes no summary/ring.
- If `V7_SERVICE_MATRIX_LOCK_HELD=1`, it safely inherits the lifecycle lock.
- During an active restore-barrier clearance window with approved nonzero selected moves, compactor exits OK with `SKIPPED_RESTORE_BARRIER_ACTIVE` and writes no summary/ring.
- Safe deploy and truth coverage now include `/usr/local/bin/v7-egress-quality-compact`.

## Verification

Local tests:

- `python3 -m unittest discover tests`
- Result after final fix: `Ran 362 tests in 28.512s OK`

Production deploy:

- Final deployed commit: `9e4d637f97a9870b9a5fa4f6e2480f22e43c2e37`
- Safe deploy: PASS
- Final truth-check: PASS / FULLY_ALIGNED
- Final convergence-status: PASS / READY_FOR_RUNTIME_ACTION

Production smoke:

- `v7-egress-quality-compact --pretty`
- Result: `SKIPPED_RESTORE_BARRIER_ACTIVE`
- `service_matrix_lock.released=true`
- `restore_barrier_pause.reason=active_restore_barrier_clearance_window`
- `users_moved=false`

## Second MEDIUM Retry

Fresh retry was executed through the canonical flow:

1. Fresh planner with pre-planner refresh write.
2. Fresh 5-user packet.
3. Packet recheck.
4. Restore barrier clearance.
5. Final dry-run recheck.

Fresh packet contained 5 users:

- `10.7.0.11`
- `10.7.0.12`
- `10.7.0.14`
- `10.7.0.15`
- `10.0.0.2`

Targets:

- `awg0`
- `awg3`

Final dry-run result:

- `terminal_reason=dry_run_intelligence_snapshot_stop_required`
- `selected_move_count=0`
- `restore_barrier.clearance_generation_ok=true`
- `restore_barrier.clearance_generation_reason=restore_barrier_clearance_generation_match_source_bundle_lease`
- `source_bundle_lease.ok=true`
- `source_bundle_lease.changed_source_keys=["service_matrix"]`
- `quality_summary` was not the changed source.

Decision:

No apply was executed.

Reason:

The program requires dry-run recheck PASS before real governed apply. The existing service-matrix-only lease is accepted by restore barrier, but dry-run still keeps the intelligence snapshot gate stop-required. Applying at this point would rely on apply-only lease behavior without a passing dry-run recheck.

## Final Verdicts

`quality_summary_owner_identified=true`

`quality_summary_lineage=INDEPENDENT_MUTABLE_RUNTIME_SOURCE`

`quality_summary_classification=HARD_RUNTIME_SOURCE`

`quality_summary_race_closed=true`

`quality_summary_derived_source_bound_correctly=true`

`quality_summary_drift_after_fix=false`

`deploy_pass=true`

`truth_check_pass=true`

`convergence_ready=true`

`tests_pass=true`

`second_medium_completed=false`

`users_moved=0`

`apply_executed=false`

`verification_passed=false`

`rollback_required=false`

`outcomes_materialized=false`

`trust_feedback_updated=false`

`prediction_feedback_updated=false`

`recommendation_feedback_updated=false`

`stability_window_completed=false`

`large_batch_ready=false`

`SAFE_NEXT_STEP=SERVICE_MATRIX_SOURCE_BUNDLE_LEASE_DRY_RUN_READINESS_CLOSURE`

## Next Required Block

The next block should not re-open `quality_summary`.

The blocker is now:

`service_matrix_only_source_bundle_lease_is_accepted_by_restore_barrier_but_not_materialized_as_dry_run_readiness`

Required next action:

Define or reuse an existing read-only readiness mode that proves the exact apply-time source-bundle lease outcome without moving users, so dry-run can certify:

- approved users unchanged
- approved targets unchanged
- selected move hash accepted
- restore barrier valid
- only `service_matrix` drift present
- intelligence snapshot gate would be leased under governed apply

Only after that read-only readiness PASS should real MEDIUM apply be attempted.
