# TG1 Docs-Only Runtime Truth Gate Closure and BA1 Recertification Report

## 1. Truth Gate Root Cause

Root cause: `tools/v7-truth-check` treated every `runtime_commit != local_commit` as `runtime_local_commit_mismatch`.

`tools/v7-convergence-status` already had the correct classification model:

- deployable/runtime changes require deploy
- unknown changes block
- docs/evidence/report-only changes are `DOCS_ONLY_MISMATCH`

The bug was that `truth-check` did not reuse that classification before adding the runtime blocker.

Impact before TG.1:

- local/GitHub had only docs/evidence/report commits ahead of production runtime
- `deploy_delta_mismatches=[]`
- `deployment_required=false`
- `runtime_action_safe=true`
- but `truth-check --all` still returned `NO-GO`

## 2. Classification Audit

Existing classification owner reused:

- `tools/v7_sync_lib.py`
- `classify_deployable_changes`
- `changed_files_between_commits`

Classification behavior after TG.1:

- docs/reports/evidence: do not block runtime truth
- deployable runtime files: still block
- unknown paths: still block
- runtime dirty workspace: still blocks
- binary hash mismatch: still blocks
- runtime provenance unknown: still blocks

No new truth source was created.

## 3. Counterfactual Analysis

If docs-only commits are ignored for runtime blocking:

- runtime safety decreases: `false`
- routing safety decreases: `false`
- execution safety decreases: `false`
- autonomy safety decreases: `false`

Reason:

Docs/evidence/report commits do not change deployed binaries, runtime services, routing state, planner behavior, restore barrier behavior, rollback behavior, or execution behavior.

The fix remains fail-closed because only `DOCS_ONLY_MISMATCH` is ignored. Deployable or unknown changes continue to produce `NO-GO`.

## 4. Fix Applied

Commit:

`396c3d1 Treat docs-only runtime truth mismatches as non-blocking`

Changed files:

- `tools/v7-truth-check`
- `tests/unit/test_v7_truth_check.py`

Implementation:

- `tools/v7-truth-check` now uses the existing `v7_sync_lib` classification model.
- When runtime commit differs from local commit, it checks changed paths between the runtime commit and local commit.
- If the delta is docs/evidence/report-only, it emits warning `runtime_local_commit_docs_only_mismatch_ignored` instead of blocker `runtime_local_commit_mismatch`.
- If the delta is deployable or unknown, the blocker remains.

Tests added:

- docs-only runtime mismatch does not block truth
- deployable runtime mismatch still blocks truth

Validation:

- `py_compile`: PASS
- targeted tests: PASS, 47 tests
- full suite: PASS, 444 tests
- `git diff --check`: PASS

Safe deploy:

- deploy id: `deploy-z8-14-Updatesystem-396c3d1-20260612T222208`
- user movement: `false`
- autoswitch apply: `false`
- routing mutation: `false`
- restore barrier mutation: `false`
- planner modified: `false`

## 5. Retest Results

Post-fix truth gate:

- `truth-check --all`: `PASS`
- convergence: `FULLY_ALIGNED`
- blockers: `[]`
- local commit: `396c3d160f81a7064735a46c52f1d3ffb36d71fd`
- GitHub commit: `396c3d160f81a7064735a46c52f1d3ffb36d71fd`
- production commit: `396c3d160f81a7064735a46c52f1d3ffb36d71fd`

Post-fix convergence:

- `final_verdict=PASS`
- `status=ALIGNED`
- `runtime_action_status=READY_FOR_RUNTIME_ACTION`
- `runtime_action_safe=true`

Docs-only runtime truth blocker is closed.

## 6. BA.1 Recertification

BA.1 truth gate after TG.1:

- truth: `PASS`
- convergence: `PASS`
- runtime action: `READY_FOR_RUNTIME_ACTION`

Production planner dry-run:

- users total: `26`
- egress total: `7`
- healthy egress total: `3`
- candidate moves total: `26`
- selected moves: `0`
- apply requested: `false`

New blocker:

`snapshot_source_mismatch_service_scores_channel_service_scores`

The production planner stopped before selected moves because the atomic execution envelope reported:

- `stop_required=true`
- `source_mismatch_families=["channel-service-scores","service-scores"]`
- action: `refresh_replan_and_reapprove_before_apply`
- blocked actions: `user_movement`, `autoswitch_apply`, `authority_promotion`

No autonomous movement was executed.

## 7. Final Verdict

Final verdict: `TRUTH_GATE_CLOSED_NEW_BLOCKER`

Closed:

- `runtime_truth_gate_no_go_docs_only_mismatch`

New single blocker:

`snapshot_source_mismatch_service_scores_channel_service_scores`

Safety:

- users moved: `0`
- apply executed: `false`
- routing changed: `false`
- autonomy enabled: `false`

Safe next step:

`REFRESH_PRODUCTION_INTELLIGENCE_SNAPSHOTS_THEN_RERUN_BA1`
