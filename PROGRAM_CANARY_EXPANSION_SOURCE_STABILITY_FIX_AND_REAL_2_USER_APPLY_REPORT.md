# PROGRAM CANARY EXPANSION SOURCE STABILITY FIX AND REAL 2 USER APPLY REPORT

Date: 2026-06-06

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Evidence folder: `canary_source_stability_evidence/`

## Executive Verdict

The `service_matrix` apply-window blocker was reproduced and closed in the existing governed apply path.

The fix is implemented in `tools/v7-users-autoswitch` and covered by regression tests. It does not create a new planner, new governance path, new execution path, new truth source, or validation bypass.

The real production 2-user apply was not executed in this run because the mandatory truth/deploy gate is currently NO-GO: the workspace contains mixed runtime-critical dirtiness from two packages:

- current CANARY source-stability fix:
  - `tools/v7-users-autoswitch`
  - `tests/unit/test_v7_users_autoswitch_policy.py`
  - `canary_source_stability_evidence/`
  - this report
- pre-existing admin UI/performance package:
  - `admin/v7-admin-api`
  - `USER_ADMIN_USER_PANEL_UI_PERFORMANCE_FIX_REPORT.md`

This is a real gate, not a cosmetic blocker. Safe deploy must not merge these silently into one live action without explicit separation or approval.

## SOURCE_STABILITY_ROOT_CAUSE

`service-matrix.json` is a live mutable source, not a static approval artifact.

Discovered writers/updaters:

| Component | Location | Role | Frequency / Trigger |
|---|---|---|---|
| Full service matrix refresh timer | `systemd/v7-service-matrix-refresh.timer` | Starts full refresh service | `OnUnitActiveSec=15min`, `RandomizedDelaySec=60s` |
| Full service matrix refresh service | `systemd/v7-service-matrix-refresh.service` | Runs refresh wrapper | `ExecStart=/usr/local/bin/v7-service-matrix-refresh-all` |
| Refresh wrapper | `tools/v7-service-matrix-refresh-all` | Runs `v7-service-matrix-test <egress> all` | Per enabled egress |
| Matrix writer | `tools/v7-service-matrix-test` | Writes `service-matrix.json` with atomic replace | Per refresh/test invocation |
| Fast Telegram sentinel timer | `systemd/v7-telegram-sentinel.timer` | Starts fast sentinel | `OnUnitActiveSec=4s`, `AccuracySec=1s` |
| Fast Telegram sentinel service | `systemd/v7-telegram-sentinel.service` | Runs Telegram sentinel | `ExecStart=/usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1 --no-autoswitch` |
| Telegram sentinel writer | `tools/v7-telegram-sentinel` | Updates Telegram row in `service-matrix.json` after grace threshold | Up to every sentinel cycle when state changes |

Root cause:

The governed apply plan correctly captured an atomic source bundle. Before `apply`, the validator reread live `service-matrix.json` from disk. A legitimate live writer changed only `service_matrix`, so the source bundle hash changed and the atomic gate failed closed with `atomic_execution_envelope_source_changed`.

This was safe behavior, but it made a bounded approved apply too fragile because `service_matrix` is an intentionally live signal.

## SOURCE_STABILITY_FIX_DECISION

Chosen fix:

Use an approved source-bundle stability lease inside the existing atomic envelope validation.

The lease is accepted only when all of these are true:

- the only mismatch is `source_bundle_hash`;
- the only changed source key is `service_matrix`;
- `runtime_snapshot_hash` is unchanged;
- selected move hash/count are unchanged;
- users registry and egress registry are unchanged;
- the restore barrier is expired, cleared, and has valid generation clearance;
- selected moves do not exceed `clearance_max_selected_moves`;
- selected users match `allowed_users` when present;
- selected targets match `allowed_targets` when present;
- snapshot gate has no stop condition;
- `source_mismatch_families=[]`;
- pre-planner refresh ran in write mode and returned `REFRESH_SUCCESS`;
- clearance TTL is not expired.

Everything else still fails closed.

## SOURCE_STABILITY_FIX_IMPLEMENTATION

Changed:

- `tools/v7-users-autoswitch`

Implementation details:

- Added `SOURCE_BUNDLE_LEASE_VALID` atomicity state.
- Added `_source_bundle_stability_lease_validation(...)`.
- Apply validation now attempts the lease only after normal envelope validation detects a mismatch.
- Restore barrier status now preserves approved envelope metadata at top level:
  - `approved_atomic_execution_envelope_id`
  - `approved_atomic_execution_envelope_hash`
  - `approved_source_bundle_hash`
  - `approved_snapshot_bundle_hash`

No execution bypass was introduced. The apply path remains `planner -> packet/barrier -> atomic validation -> existing apply`.

## SOURCE_STABILITY_TEST_REPORT

Changed:

- `tests/unit/test_v7_users_autoswitch_policy.py`

Added coverage:

- service_matrix changes during apply window are accepted only with valid governed source-bundle lease;
- stable bundle still passes through normal `ENVELOPE_VALID`;
- real runtime source change still blocks apply;
- expired lease blocks apply;
- unapproved users block apply;
- two-user blast radius cap remains enforced.

Verification:

| Command | Result |
|---|---|
| `python3 -m unittest tests.unit.test_v7_users_autoswitch_policy` | PASS, 42 tests |
| `python3 -m unittest discover tests` | PASS, 333 tests |
| `PYTHONPYCACHEPREFIX=/private/tmp/v7-pycache python3 -m py_compile tools/v7-users-autoswitch tests/unit/test_v7_users_autoswitch_policy.py` | PASS |

Evidence:

- `canary_source_stability_evidence/unit_autoswitch_policy.txt`
- `canary_source_stability_evidence/unit_discover_tests.txt`
- `canary_source_stability_evidence/py_compile.txt`

## DEPLOY_AND_TRUTH_REPORT

Deploy was not executed.

Read-only gates:

| Gate | Result | Evidence |
|---|---|---|
| `tools/v7-truth-check --local --json` | NO-GO | `canary_source_stability_evidence/truth_check_local_dirty.json` |
| `tools/v7-safe-deploy --json` | NO-GO | `canary_source_stability_evidence/safe_deploy_plan_dirty.json` |

Truth-check blockers:

- `dirty_workspace`
- `runtime_critical_dirty`

Runtime-critical dirty paths:

- `admin/v7-admin-api`
- `tools/v7-users-autoswitch`

Safe-deploy blocker:

- `github_truth_check_failed`

Production deploy delta observed by safe deploy:

- `tools/v7-users-autoswitch` differs from production;
- `admin/v7-admin-api` differs from production;
- other checked runtime files were aligned in the safe-deploy plan sample.

## PHASES NOT EXECUTED

The following phases were intentionally not executed because the truth/deploy gate is NO-GO:

- fresh production readiness;
- fresh approval packet;
- fresh restore barrier;
- final pre-apply lock;
- real governed apply;
- post-apply verification;
- outcome materialization;
- trust/prediction/recommendation feedback;
- SMALL_BATCH certification.

No users were moved in this run.

## Required Next Step

One proven blocker must be closed before retrying the real 2-user apply:

`mixed_runtime_critical_dirty_workspace`

Safe closure options:

1. Commit the pre-existing admin UI/performance package separately, then commit this source-stability package separately.
2. Push `Updatesystem`.
3. Run approved safe deploy with the required admin restart flag if admin is included:
   - `tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --restart-admin-if-changed --json`
4. Run:
   - `tools/v7-truth-check --all --json`
   - `tools/v7-convergence-status --json`
5. Only after FULLY_ALIGNED, regenerate fresh packet/barrier and execute the real governed apply for exactly:
   - `10.0.0.3 awg3 -> vless`
   - `10.0.0.6 awg3 -> vless`

## Final Verdicts

| Verdict | Value |
|---|---|
| source_stability_root_cause_identified | true |
| source_stability_fix_implemented | true |
| source_bundle_stable_across_refresh_packet_barrier_apply | local_tests_true_production_not_executed |
| truth_check_pass | false |
| fresh_packet_created | false |
| restore_barrier_fresh | false |
| users_moved | 0 |
| only_approved_users_moved | true |
| verification_passed | false |
| rollback_required | false |
| outcomes_materialized | false |
| trust_feedback_updated | false |
| prediction_feedback_updated | false |
| recommendation_feedback_updated | false |
| small_batch_certified | false |
| current_certified_authority | CANARY |
| current_runtime_authority | CANARY |
| current_allowed_user_budget | 2 |
| safe_for_medium_batch_review | false |
| safe_for_bounded_autonomy | false |
| safe_for_production_autonomy | false |
| SAFE_NEXT_STEP | commit/separate mixed runtime-critical workspace, push, safe deploy, truth-check, then retry fresh packet/barrier/apply |
