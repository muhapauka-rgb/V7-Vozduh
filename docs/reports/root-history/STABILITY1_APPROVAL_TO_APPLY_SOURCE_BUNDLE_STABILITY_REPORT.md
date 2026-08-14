# STABILITY.1 Approval-To-Apply Source Bundle Stability Closure

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Date: 2026-06-13

## 1. Source Inventory

STABILITY.1 mapped the approval-to-apply chain:

Planner
-> atomic execution envelope
-> approval packet
-> approved plan lock
-> restore barrier clearance
-> runtime recheck
-> apply validation

Existing owners were reused:

| Area | Owner |
|---|---|
| Planner decision | `tools/v7-users-autoswitch` |
| Atomic envelope | `tools/v7-users-autoswitch` |
| Approval packet | `admin_core/operator_execution.py` |
| Approved plan lock | `admin_core/operator_execution.py` |
| Restore barrier | `admin_core/operator_execution.py` |
| Apply validation | `tools/v7-users-autoswitch` |
| Snapshot refresh | `tools/v7-intelligence-snapshot-refresh` / `admin_core.intelligence_workers` |

No new planner, governance owner, execution engine, or truth source was created.

Detailed inventory evidence:

- `docs/reports/evidence/STABILITY1_EVIDENCE/source_inventory_and_policy.json`
- `docs/reports/evidence/STABILITY1_EVIDENCE/source_owner_code_refs.txt`

## 2. Stability Classification

Canonical source policy:

| Source | Class | Runtime policy |
|---|---|---|
| `users_registry` | STRICT | always stop if changed |
| `egress_registry` | STRICT | always stop if changed |
| `service_preferences` | STRICT | always stop if changed |
| `service_matrix` | VOLATILE | allow only with stable decision signature |
| `quality_summary` | VOLATILE | allow only with stable decision signature |
| `service-scores` | DERIVED | allow only when explained by leased volatile source drift |
| `channel-service-scores` | DERIVED | allow only when explained by leased volatile source drift |
| `trust/prediction/suitability/pool` snapshots | DERIVED | fail closed unless existing gate proves non-blocking |
| unknown source | UNKNOWN | fail closed |

This keeps the important distinction:

- changing selected users/targets/count/hash remains blocked;
- changing service evidence can be allowed only when the approved decision is semantically unchanged.

## 3. Drift Forensics

BA.2 replay:

- two-user autonomy certified;
- apply completed;
- feedback and trust loop completed.

Evidence:

- `docs/reports/evidence/STABILITY1_EVIDENCE/ba2_replay_forensics.json`

BA.3 replay:

- fresh planner selected 5 users;
- packet and restore barrier were valid;
- pre-execution dry-run passed;
- apply selected 0 users and did not move anyone;
- blocker repeated on first apply and retry.

Observed BA.3 blocker:

- `service-scores`
- `channel-service-scores`
- source mismatch key: `service_matrix`
- restore barrier source bundle lease: `ok=true`
- decision signature: stable
- selected move hash: stable
- selected users: stable
- selected targets: stable

The decisive anomaly was not unsafe decision drift. The anomaly was pre-planner apply-refresh scope classification:

- `pre_planner_refresh.state=SKIPPED_APPLY_FORBIDDEN`
- `stop_families` included `pre-planner-refresh`
- source bundle lease existed but could not clear the gate because `pre-planner-refresh` was treated as an unleased stop family.

Evidence:

- `docs/reports/evidence/STABILITY1_EVIDENCE/ba3_drift_forensics.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase7_five_user_apply.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase7_retry1_five_user_apply.json`

## 4. Decision Impact Audit

Decision-changing drift remains blocked:

- selected users change;
- selected targets change;
- selected move hash changes;
- selected move count changes;
- strict source hash changes;
- approved plan lock invalid;
- restore barrier expired;
- selected count exceeds clearance budget;
- runtime snapshot hash changes.

Non-decision-changing drift can be allowed only when:

- changed source keys are within the semantic drift set;
- strict source hashes are unchanged;
- approved selected move hash equals current selected move hash;
- selected count equals approved count;
- approved plan lock is valid;
- users and targets are within restore barrier constraints;
- pre-planner refresh succeeded or was not required.

This means V7 can distinguish harmless operational drift from decision-changing drift, but only through the existing atomic envelope and approved plan lock.

## 5. Atomic Envelope Policy

The policy remains fail-closed.

`STRICT` sources:

- any change stops execution.

`VOLATILE` sources:

- allowed only if the decision signature remains identical.

`DERIVED` sources:

- allowed only if their mismatch is caused by leased volatile source drift.

`UNKNOWN` sources:

- always stop.

The fix does not weaken source bundle validation. It only corrects the apply-refresh scope model for governed multi-target packets.

## 6. Semantic Stability Model

Existing ATOMIC.1 decision signature was reused.

Signature fields:

- selected move hash
- approved selected move hash
- selected count
- approved count
- selected users
- selected targets
- strict source hashes
- approved strict source hashes

BA.3 had a stable signature and a valid source bundle lease, but the apply-refresh gate required a single `--target-egress`. BA.3 packet had two approved targets:

- `awg0`
- `awg3`

That was valid governance, not target substitution.

## 7. Fix Applied

Changed file:

- `tools/v7-users-autoswitch`

Fix:

The governed envelope apply-refresh scope now accepts approved multi-target packets when:

- `--allow-pre-planner-refresh-with-apply` is present;
- restore barrier has generation clearance;
- requested moves are within `clearance_max_selected_moves`;
- approved atomic envelope metadata exists;
- approved targets are present in the restore barrier;
- no manual target replacement is attempted.

For single-target applies, the existing `--target-egress` check remains.

New evidence fields:

- `apply_refresh_scope.allowed_targets`
- `apply_refresh_scope.target_scope`

`target_scope` is:

- `single_target_arg` for explicit single-target apply;
- `approved_plan_lock_targets` for governed multi-target packet apply.

No routing mutation was performed by this program.

## 8. Replay Results

Added regression test:

- `test_governed_apply_pre_refresh_accepts_approved_multi_target_lock`

The test reproduces the BA.3 shape:

- apply mode;
- pre-planner refresh write;
- `--allow-pre-planner-refresh-with-apply`;
- `--max-selected-moves=5`;
- restore barrier with multiple approved targets;
- no `--target-egress`.

Expected and verified result:

- refresh state: `REFRESH_SUCCESS`
- target scope: `approved_plan_lock_targets`
- no `SKIPPED_APPLY_FORBIDDEN`

Validation:

- `python3 -m py_compile tools/v7-users-autoswitch`: PASS
- targeted autoswitch policy tests: 75 tests PASS
- full test suite: 447 tests PASS
- `git diff --check`: PASS

Evidence:

- `docs/reports/evidence/STABILITY1_EVIDENCE/py_compile.txt`
- `docs/reports/evidence/STABILITY1_EVIDENCE/unit_test_v7_users_autoswitch_policy.txt`
- `docs/reports/evidence/STABILITY1_EVIDENCE/full_unittest_discover.txt`
- `docs/reports/evidence/STABILITY1_EVIDENCE/code_diff.patch`

## 9. Future Autonomy Review

Impact:

- BA.3 can be retried after this fix is deployed.
- BA.4 and future batch autonomy can use multi-target approved packets without being misclassified as unbounded apply refresh.
- Operator-approved autonomy and governed execution retain the same packet, barrier, and runtime recheck boundaries.
- The fix does not enable autonomy by itself.
- The fix does not move users.
- The fix does not bypass planner, governance, restore barrier, runtime recheck, or apply validation.

## 10. Final Verdict

Final verdict: `SOURCE_BUNDLE_STABILITY_CERTIFIED`

Final findings:

- source inventory complete: true
- stability classification complete: true
- BA.3 root cause identified: true
- decision-changing drift blocked: true
- harmless governed multi-target drift path fixed: true
- fail-closed behavior preserved: true
- tests passed: true

Single blocker: `NONE`

Safe next step:

`PROGRAM STABILITY1.CLOSE DEPLOY AND BA3 RECERTIFICATION`

Deploy this bounded fix through the approved safe deploy path, verify truth/convergence, then rerun BA.3 from a fresh planner, packet, and restore barrier.
