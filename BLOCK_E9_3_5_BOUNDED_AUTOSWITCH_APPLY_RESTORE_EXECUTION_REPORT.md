# Block E9.3.5 — Bounded Autoswitch Apply Restore Execution Report

Mode: bounded live autoswitch recovery rehearsal.

## Executive Verdict

E9.3.5 did not restore `v7-users-autoswitch.timer`. The final required planner-only sample was no longer zero-move: it selected 3 failover moves and exposed 15 total candidate movement decisions. Per the block abort rule, apply restore was aborted before any live apply authority was returned.

## Required Answers

```text
apply_restore_executed=false
apply_restore_aborted=true
apply_restore_emergency_containment=false
planner_only_prediction=selected_moves=3 candidate_moves_total=15 target=vless reason=current_egress_not_eligible
actual_movements_count=0
actual_moved_users=none
movement_reasons=not_executed; predicted reasons were current_egress_not_eligible/failover from 1 to vless
predicted_vs_actual_match=n/a_not_executed
awg3_movements_observed=false
routing_drift_observed=false
hidden_routing_sync_observed=false
reconcile_ok=true_before_restore
user_route_check_ok=true_before_restore
kill_switch_ok=true_before_restore
provisioning_ok=true_before_restore
autoswitch_recovery_bounded=false_not_executed_due_final_planner_gate
restore_governance_proven=false_apply_restore_not_executed
current_canary_status=NO-GO_APPLY_RESTORE_ABORTED_BY_FINAL_PLANNER_SAMPLE
execution_allowed_now=false
```

## Evidence Collected

- Pre-apply restore snapshot: `docs/track7/control-plane/e9_3_5-evidence/pre-apply-restore.txt`
- Current target readiness, pretty: `docs/track7/control-plane/e9_3_5-evidence/pre-apply-restore-readiness.txt`
- Current target readiness, JSON: `docs/track7/control-plane/e9_3_5-evidence/pre-apply-restore-readiness.json`
- Final planner-only sample: `docs/track7/control-plane/e9_3_5-evidence/final-planner-only-sample.txt`
- Final planner-only classification: `docs/track7/control-plane/e9_3_5-evidence/final-planner-only-classification.txt`
- Abort classification: `docs/track7/control-plane/e9_3_5-evidence/apply-restore-abort-classification.md`

## Final Planner-Only Sample

```text
selected_moves=3
candidate_moves_total=15
different_or_non_keep_decisions=15
apply_requested=false
```

Selected movements that would have been eligible for apply:

| User | From | To | Reason |
|---|---|---|---|
| 10.0.0.2 | 1 | vless | current_egress_not_eligible |
| 10.0.0.3 | 1 | vless | current_egress_not_eligible |
| 10.0.0.6 | 1 | vless | current_egress_not_eligible |

The broader planner context listed 15 candidate decisions from `1` to `vless`. The planner rejected current egress `1` because it was not eligible, including `service_instagram_failed` and degraded Telegram/service context.

## Movement Classification

No movement occurred in E9.3.5. The apply timer was not restored, so there was no timer-driven apply run and no route table mutation.

```text
actual_movements_count=0
actual_moved_users=none
user_movement_observed=false
routing_mutation_observed=false
kill_switch_mutation_observed=false
autoswitch_apply_manual=false
```

## Governance Interpretation

E9.3.4 showed `selected_moves=0`, but the final E9.3.5 sample showed nonzero selected moves. That proves the planner-only state can change quickly and that apply restore cannot rely on stale approval evidence.

The staged restore model behaved correctly because it prevented restoring apply authority when final evidence no longer matched the zero-move approval assumption.

## Recommended Next Step

Keep `v7-users-autoswitch.timer` held. Run a new read-only block to explain why egress `1` became ineligible and why 15 users are candidate failovers to `vless`. After that, choose one of:

- wait until planner-only selected moves return to zero and repeat E9.3.5;
- approve a bounded apply restore with an explicit accepted movement list and max movement count;
- adjust autoswitch eligibility/quality policy in a separate design/fix block before restore.

## Verification

```text
tools/v7-run-tests=PASS
tools/v7-control-plane-governance-check --pretty=PASS
tools/v7-second-canary-target-readiness --pretty=PASS_NO-GO
tools/v7-second-canary-target-readiness --json=PASS_NO-GO
tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty=PASS_WITH_WARNINGS
tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty=PASS_WITH_WARNINGS
py_compile_admin_tools_governance=PASS
git_diff_check=PASS
```

Runtime/repo diff warning:

```text
runtime_manifest_not_supplied
```

Release lineage warning status:

```text
source_worktree_dirty
runtime_manifest_missing_locally_or_not_supplied
known_43_production_only_tools_require_lineage
archive_manifest_missing_locally_or_not_supplied
release_provenance=incomplete
runtime_lineage=partial
```

## Final Mutation Statement

```text
Runtime mutation performed: NO — apply restore aborted before timer start
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Autoswitch apply timer restored: NO
Canary performed: NO
```
