# PROGRAM ATOMIC.1 - APPROVAL-TO-APPLY SOURCE BUNDLE STABILITY AND DECISION SIGNATURE CERTIFICATION

## Executive Summary

Final verdict: **SAFE_DRIFT_POLICY_CERTIFIED**

ATOMIC.1 closed the source-bundle-drift class at the existing atomic envelope owner.

The old behavior was:

```text
source bundle changed
-> stop execution
```

The new behavior is:

```text
source bundle changed
-> semantic decision signature check
-> same locked decision and only allowed volatile inputs changed
-> continue

source bundle changed
-> decision signature unstable or strict source changed
-> stop execution
```

This does not bypass planner, governance, restore barrier, approved plan lock, or runtime recheck. It extends the existing source-bundle lease with a decision signature.

No users were moved.

No apply was executed.

No production deployment was performed in this program.

## 1. Atomic Envelope Reality Map

Existing owners:

| Stage | Owner | Existing truth |
| --- | --- | --- |
| Planner selection | `tools/v7-users-autoswitch` | `selected_move_hash`, `selected_move_count` |
| Approval packet | `admin_core/operator_execution.py` | packet expected fields |
| Approved plan lock | `admin_core/operator_execution.py` | locked users, targets, selected hash, replacement flags |
| Restore barrier clearance | `admin_core/operator_execution.py` | clearance token, generation, budget, source hashes |
| Runtime recheck | `tools/v7-users-autoswitch` | restore barrier validation and atomic envelope validation |
| Source bundle | `tools/v7-users-autoswitch` | `service_matrix`, `quality_summary`, `service_preferences`, `users_registry`, `egress_registry` |

Key implementation points:

- `tools/v7-users-autoswitch`: `_atomic_execution_envelope`
- `tools/v7-users-autoswitch`: `_restore_clearance_generation_check`
- `tools/v7-users-autoswitch`: `_restore_barrier_source_bundle_lease`
- `tools/v7-users-autoswitch`: `_source_bundle_stability_lease_validation`
- `tools/v7-users-autoswitch`: `_apply_source_bundle_lease_to_intelligence_gate`
- `admin_core/operator_execution.py`: `approved_plan_lock_from_selected`
- `admin_core/operator_execution.py`: `recheck_nonzero_packet`

## 2. Source Bundle Audit

Source bundle members:

| Source | Classification | Reason |
| --- | --- | --- |
| `users_registry` | STRICT | A user source/current route change can alter blast radius and rollback meaning. |
| `egress_registry` | STRICT | A target/channel identity or enabled-state change can alter execution safety. |
| `service_preferences` | STRICT | Required-service policy can alter eligibility and governance meaning. |
| `service_matrix` | VOLATILE_ALLOWED_WITH_SIGNATURE | Probe/service data may refresh between approval and apply. Safe only if locked decision remains identical. |
| `quality_summary` | VOLATILE_ALLOWED_WITH_SIGNATURE | Quality data may refresh between approval and apply. Safe only if locked decision remains identical. |

Unknown sources remain fail-closed.

## 3. Drift Forensics

BA.2 blocker evidence:

```json
{
  "terminal_reason": "dry_run_restore_barrier_clearance_atomic_envelope_id_mismatch",
  "clearance_generation_reason": "restore_barrier_clearance_atomic_envelope_id_mismatch",
  "changed_source_keys": [
    "quality_summary",
    "service_matrix"
  ],
  "source_bundle_lease_reason": "restore_barrier_source_bundle_lease_hard_source_changed"
}
```

BA.2 was not blocked by:

- authority budget
- policy limit after escalation
- planner candidate availability
- packet generation
- restore barrier owner
- selected user replacement
- target replacement

The blocker was the old source-bundle lease policy. It accepted `service_matrix` drift only and rejected `quality_summary + service_matrix` even when the approved plan lock still represented the same decision.

## 4. Decision Signature Audit

Existing reusable decision concepts:

- `selected_move_hash`
- `selected_move_count`
- `approved_plan_lock`
- `allowed_users`
- `allowed_targets`
- `executor_may_reselect=false`
- `executor_may_replace_users=false`
- `executor_may_replace_targets=false`
- strict source hashes for `users_registry`, `egress_registry`, `service_preferences`

ATOMIC.1 reused these instead of creating a new truth source.

New evidence object:

```json
{
  "schema_version": "v7.source-bundle-decision-signature.v1",
  "selected_move_hash": "...",
  "approved_selected_move_hash": "...",
  "selected_move_count": 2,
  "approved_selected_move_count": 2,
  "selected_users": ["..."],
  "selected_targets": ["..."],
  "strict_source_hashes": {
    "egress_registry": "...",
    "service_preferences": "...",
    "users_registry": "..."
  },
  "approved_strict_source_hashes": {
    "egress_registry": "...",
    "service_preferences": "...",
    "users_registry": "..."
  }
}
```

This is not a new runtime authority. It is evidence written under the existing source-bundle lease owner.

## 5. Semantic Recheck Model

Allowed only when all conditions are true:

- changed sources are a subset of `quality_summary`, `service_matrix`
- `approved_plan_lock` is valid
- selected hash matches approved selected hash
- selected count matches approved count
- users are not replaced
- targets are not replaced
- registry and service preference hashes remain stable
- restore barrier generation is valid
- clearance budget is not exceeded

Still blocked when:

- `users_registry` changes
- `egress_registry` changes
- `service_preferences` changes
- selected hash changes
- selected count changes
- approved plan lock is invalid
- restore barrier clearance expired
- snapshot gate has unaccepted mismatch families
- pre-planner refresh/apply validation requirements are not met

## 6. Counterfactual Tests

Added tests:

- `test_readiness_dry_run_allows_semantic_quality_and_service_matrix_drift`
- `test_readiness_dry_run_blocks_semantic_drift_without_stable_signature`

Preserved existing tests:

- `test_readiness_dry_run_keeps_snapshot_gate_closed_for_unleased_quality_drift`
- `test_readiness_dry_run_uses_source_bundle_lease_for_service_matrix_snapshot_drift`
- existing governed apply source-bundle lease tests
- existing approved plan lock rejection tests

Result:

```text
safe drift allowed
unsafe drift blocked
old service_matrix lease preserved
unleased quality drift still blocked
```

## 7. Fix Applied

Changed:

- `tools/v7-users-autoswitch`
- `tests/unit/test_v7_users_autoswitch_policy.py`

Implementation:

- Added `_source_bundle_lease_scope`.
- Reused `_restore_barrier_source_bundle_lease`.
- Reused `_source_bundle_stability_lease_validation`.
- Extended lease reason from service-matrix-only to semantic decision stable drift.
- Added `decision_signature` evidence to both allow and deny paths.

No new planner was created.

No new governance owner was created.

No new execution path was created.

No new truth source was created.

## 8. BA.2 Retest

BA.2 production execution was **not** rerun in this program because the fix is local and not deployed yet.

Local counterfactual replay is covered by the new unit test:

```text
quality_summary + service_matrix drift
+ valid approved plan lock
+ same selected users
+ same selected targets
+ same selected hash/count
-> dry_run_selected_moves_available
```

Unsafe counterfactual is also covered:

```text
quality_summary + service_matrix drift
+ unstable approved plan lock
-> gate remains closed
-> selected_moves=0
```

Required next BA.2 step:

```text
commit ATOMIC.1
push
safe deploy
truth-check
convergence-status
rerun BA2.GATE two-user autonomy
```

## 9. Autonomy Impact Review

Impact on BA.2:

- Removes the old blanket blocker for `quality_summary + service_matrix` drift.
- Keeps two-user autonomy fail-closed unless the exact locked decision remains stable.

Impact on BA.3/future autonomy:

- Reduces false stops caused by harmless probe refreshes.
- Does not permit user replacement.
- Does not permit target replacement.
- Does not permit registry drift.
- Does not permit service preference drift.

Impact on batch execution:

- Same semantic rule applies to larger batches.
- Batch safety still depends on selected hash/count, approved plan lock, restore barrier, and budget.

Impact on governance:

- Governance remains owner of approval/restore barrier.
- CTR/planner/execution ownership unchanged.

## 10. Validation

Validation evidence:

- `docs/reports/evidence/ATOMIC1_EVIDENCE/py_compile.txt`
- `docs/reports/evidence/ATOMIC1_EVIDENCE/unit_test_v7_users_autoswitch_policy.txt`
- `docs/reports/evidence/ATOMIC1_EVIDENCE/unit_test_operator_execution_packet.txt`
- `docs/reports/evidence/ATOMIC1_EVIDENCE/full_unittest_discover.txt`
- `docs/reports/evidence/ATOMIC1_EVIDENCE/git_diff_check.txt`
- `docs/reports/evidence/ATOMIC1_EVIDENCE/ba2_drift_forensics_summary.json`

Results:

```text
py_compile: PASS
test_v7_users_autoswitch_policy: 74 tests PASS
test_operator_execution_packet: 15 tests PASS
full unittest discover: 446 tests PASS
git diff --check: PASS
```

## 11. Final Verdict

Final verdict: **SAFE_DRIFT_POLICY_CERTIFIED**

```json
{
  "atomic_envelope_mapped": true,
  "source_bundle_audited": true,
  "ba2_drift_root_cause_known": true,
  "decision_signature_reused_or_defined": true,
  "semantic_recheck_model_defined": true,
  "bounded_fix_applied": true,
  "safe_drift_allowed": true,
  "unsafe_drift_blocked": true,
  "fail_closed_preserved": true,
  "users_moved": 0,
  "apply_executed": false,
  "production_deployed": false,
  "safe_to_retry_ba2_after_deploy": true,
  "SAFE_NEXT_STEP": "COMMIT_PUSH_SAFE_DEPLOY_ATOMIC1_THEN_RERUN_BA2_GATE"
}
```
