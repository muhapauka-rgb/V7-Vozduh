# PROGRAM SERVICE TRUTH FRESHNESS, TRANSIENT FAILURE CLASSIFICATION AND MEDIUM BATCH FOUNDATION REPORT

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Date: 2026-06-06

## Executive Summary

The failure class is closed locally in the existing runtime owner: `tools/v7-users-autoswitch`.

No new planner, governance owner, execution path, truth source, snapshot root, or runtime authority was created.

The implementation extends the existing service suitability and service gate model so a service row is classified before it can influence candidate eligibility:

- `HEALTHY`
- `TRANSIENT_FAIL`
- `PERSISTENT_FAIL`
- `STALE_SERVICE_TRUTH`
- `PROBE_METHODOLOGY_ISSUE`
- `PROFILE_IRRELEVANT_FAIL`

The original fail-closed behavior is preserved for persistent failures, stale required truth, and legacy ambiguous multi-failure rows. The incident pattern is fixed by preventing explicit non-persistent service failures from collapsing candidate generation into an immediate hard block. Instead, those failures are degraded and marked for bounded targeted revalidation through the existing service-matrix checker.

## What Changed

### Existing Ownership Reused

Owner reused:

- Planner / runtime decision owner: `tools/v7-users-autoswitch`
- Existing service truth source: `service-matrix.json`
- Existing targeted revalidation writer: `tools/v7-service-matrix-test`
- Existing full refresh wrapper: `tools/v7-service-matrix-refresh-all`
- Existing convergence gates: `tools/v7-truth-check`, `tools/v7-convergence-status`

No parallel orchestrator or duplicate service truth model was introduced.

### Service Truth Classification

Added service truth policy defaults in `tools/v7-users-autoswitch`:

- freshness windows
- stale / expired thresholds
- bounded revalidation budget, default 5 seconds
- target-egress-only revalidation flag
- profile-relevant-only revalidation flag
- methodology HTTP codes: `401`, `403`, `404`, `405`, `429`

Added classifier methods:

- `_service_truth_freshness`
- `_service_probe_methodology_issue`
- `_service_truth_classification`
- `_attach_service_revalidation_command`

Each relevant service suitability row now includes:

- `truth_class`
- `planner_decision`
- `eligibility_behavior`
- `runtime_behavior`
- `blocked_action`
- `freshness`
- `revalidation`

### Bounded Revalidation Foundation

For transient/stale relevant service truth, the planner now emits the exact existing bounded revalidation command:

```text
tools/v7-service-matrix-test <egress> <service> --timeout 5 --state-dir <state_dir>
```

Guardrails:

- target egress only
- one service at a time
- no full matrix refresh in the planner loop
- no healthy service scan
- no history scan
- no user movement
- no autoswitch apply

The planner does not run network probes during normal planning. It exposes the bounded revalidation path so the existing service-matrix/refresh flow can perform the targeted check safely.

### Candidate Gate Behavior

Persistent failure:

- remains hard fail-closed
- blocks candidate eligibility
- can still trigger failover through the existing governed path

Transient failure:

- does not become `service_multiple_critical_failed` merely because there are two explicit one-sample failures
- remains degraded
- receives service score penalty
- emits `service_signal_TRANSIENT_REVALIDATION_REQUIRED`
- emits targeted revalidation command evidence

Stale required truth:

- remains fail-closed
- blocks with `service_<service>_truth_stale`

Probe methodology issue:

- becomes visible to operator
- does not masquerade as a transport failure
- does not hard-block candidate eligibility by itself

Profile-irrelevant failure:

- is classified as `PROFILE_IRRELEVANT_FAIL`
- is ignored for the current user/route profile
- remains visible in `ignored_failures`

Legacy ambiguous failures:

- multiple `ok=false` rows without status, timestamp, reason, or method evidence remain fail-closed
- this preserves old critical behavior and avoids weakening safety on low-evidence data

## Why This Solves The VLESS Symptom

The original symptom was not simply "VLESS is bad".

The deeper issue was that service rows could be treated as equally authoritative even when the evidence class was different:

- real persistent channel failure
- temporary service probe failure
- stale truth
- probe methodology limitation
- irrelevant service failure

That allowed a temporary or badly classified service FAIL to make a potentially healthy channel look globally unsafe.

The new classifier forces the planner to show why a service signal is blocking, degrading, ignored, or methodology-limited before it can influence routing.

## Performance Impact

Expected planner performance impact: low.

Reason:

- classification is pure in-memory evaluation of already-loaded `service-matrix.json`
- no new network calls are run in the planner loop
- no full matrix refresh is triggered by this patch
- no heavy history processing was added
- targeted revalidation is represented as a bounded existing command, not auto-executed during candidate scoring

The code adds decision metadata, not a new runtime scan loop.

## Safety Boundaries Preserved

Confirmed:

- no autonomy enabled
- no users moved
- no autoswitch apply
- no governance owner changed
- no planner owner changed
- no execution owner changed
- no rollback owner changed
- no new planner created
- no new truth source created
- no new snapshot root created
- no full service matrix refresh inside planner loop

## Tests Added

New regression tests in `tests/unit/test_v7_users_autoswitch_policy.py`:

- multiple explicit single-sample service failures are transient and do not hard-block
- transient failures emit bounded targeted revalidation command
- multiple persistent service failures still fail closed
- probe methodology issue is visible and not treated as transport block
- stale required service truth blocks
- profile-irrelevant service failure is classified and ignored

Existing tests for legacy multiple critical failures and restore-stage suppression still pass.

## Verification

Local verification:

```text
PYTHONPYCACHEPREFIX=/private/tmp/v7_pycache_service_truth python3 -m py_compile tools/v7-users-autoswitch
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy
python3 -m unittest discover tests
```

Results:

- targeted policy tests: PASS, 48 tests
- full test suite: PASS, 339 tests
- py_compile: PASS

Evidence:

- `docs/reports/evidence/service_truth_freshness_evidence/py_compile.txt`
- `docs/reports/evidence/service_truth_freshness_evidence/targeted_policy_tests.txt`
- `docs/reports/evidence/service_truth_freshness_evidence/full_unittest_discover.txt`
- `docs/reports/evidence/service_truth_freshness_evidence/local_diff_stat.txt`
- `docs/reports/evidence/service_truth_freshness_evidence/local_diff_name_only.txt`
- `docs/reports/evidence/service_truth_freshness_evidence/git_status_short.txt`
- `docs/reports/evidence/service_truth_freshness_evidence/service_matrix_test_help.txt`
- `docs/reports/evidence/service_truth_freshness_evidence/users_autoswitch_help.txt`
- `docs/reports/evidence/service_truth_freshness_evidence/truth_check_all.json`
- `docs/reports/evidence/service_truth_freshness_evidence/convergence_status.json`

## Production Read-Only Validation

Read-only convergence checks were executed and saved.

`tools/v7-truth-check --all --json`:

- GitHub: PASS
- local: NO-GO because this runtime-critical patch is still dirty
- production: NO-GO because production is at deployed commit `1bd7579add17c7a71f7cc7b3a1b65885e92a6ec2`
- local/GitHub current commit: `3c9e9e74fb5db6e7eaea9f1d621420f8ecabb1ba`

`tools/v7-convergence-status --json`:

- final verdict: NO-GO
- runtime action status: DEPLOY_REQUIRED
- mismatch: local `tools/v7-users-autoswitch` differs from production `/usr/local/bin/v7-users-autoswitch`

This is expected because this prompt did not authorize deploy, restart, autoswitch apply, or runtime mutation.

## Remaining Gap

The code is implemented and locally certified, but not production-converged.

The next safe step is not MEDIUM_BATCH. The next safe step is:

1. commit this program package separately
2. push `Updatesystem`
3. run approved safe deploy
4. run `tools/v7-truth-check --all --json`
5. run `tools/v7-convergence-status --json`
6. run a read-only planner dry-run for the affected SMALL_BATCH path
7. only then retry SMALL_BATCH certification / expansion evidence

## Final Verdicts

```text
service_truth_classifier_implemented=true
transient_failure_classified=true
persistent_failure_still_fail_closed=true
stale_truth_fail_closed=true
profile_irrelevant_fail_ignored=true
probe_methodology_issue_visible=true
bounded_revalidation_guard_defined=true
planner_candidate_collapse_fixed=true
tests_pass=true
production_validation_pass=false
safe_to_retry_SMALL_BATCH=false
safe_to_begin_MEDIUM_BATCH=false
```

## Exact Next Step

```text
COMMIT_SERVICE_TRUTH_FIX_THEN_PUSH_DEPLOY_TRUTH_CHECK
```

Do not attempt MEDIUM_BATCH yet.

Do not retry live SMALL_BATCH movement until this patch is committed, deployed, and production truth-check is PASS.
