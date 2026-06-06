# PROGRAM MEDIUM BATCH READINESS TEST SYSTEM AND BLOCKER CLOSURE REPORT

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Evidence folder: `medium_batch_readiness_evidence/`

Scope: test-and-action system for MEDIUM_BATCH readiness. No user movement, no autoswitch apply, no authority promotion, no MEDIUM_BATCH execution, no autonomy.

## 1. Baseline Report

Baseline evidence:

- `medium_batch_readiness_evidence/baseline_truth_check_network.json`
- `medium_batch_readiness_evidence/baseline_convergence_status_network.json`
- `medium_batch_readiness_evidence/baseline_production_planner_dry_run.json`

Production truth:

| Check | Result |
| --- | --- |
| truth-check final verdict | PASS |
| convergence status | FULLY_ALIGNED |
| GitHub/local/production commit | `766ef7af8c21a9fec54b65a6610952ba992f5e17` |
| convergence-status final verdict | PASS |
| runtime action status | READY_FOR_RUNTIME_ACTION |

Baseline planner:

| Field | Value |
| --- | --- |
| terminal_state | DRY_RUN |
| terminal_reason | `dry_run_intelligence_snapshot_stop_required` |
| snapshot_stop_required | true |
| source_mismatch_families | `channel-service-scores`, `service-scores` |
| candidate_moves_total | 15 |
| selected_moves | 0 |
| healthy_egress_total | 2 |

Baseline verdict: production truth was aligned, but the planner correctly failed closed on intelligence snapshot source mismatch.

## 2. Snapshot Mismatch Root Cause

Root-cause evidence:

- `medium_batch_readiness_evidence/snapshot_root_cause_hashes.json`
- `medium_batch_readiness_evidence/snapshot_root_cause_runtime_listing.txt`

Affected families:

| Family | Error |
| --- | --- |
| `service-scores` | `source_hash_mismatch:service-scores:service_matrix` |
| `channel-service-scores` | `source_hash_mismatch:channel-service-scores:service_matrix` |

Hash/timestamp trace:

| Source | Timestamp | Hash |
| --- | --- | --- |
| snapshot `service-scores` generated_at | `2026-06-06T13:48:22.140620+00:00` | source service_matrix `c578d994...` |
| snapshot `channel-service-scores` generated_at | `2026-06-06T13:48:22.140620+00:00` | source service_matrix `c578d994...` |
| current `service-matrix.json` mtime | `2026-06-06T13:48:45.679033+00:00` | current service_matrix `7d797e52...` |

Cause classification:

| Possible cause | Verdict |
| --- | --- |
| stale snapshot | true |
| volatile source changed after refresh | true |
| writer/validator mismatch | false |
| missing pre-planner refresh write | true |
| stale deployed code | false |
| schema/hash contract mismatch | false |

Exact cause:

`service-matrix.json` changed after the snapshot was generated. The snapshot was still fresh by TTL, but its embedded `service_matrix` source hash no longer matched the current source hash. The planner correctly treated this as a STOP condition for runtime-required intelligence snapshots.

## 3. Snapshot Action Matrix

| Condition | Decision | Action | Executor | Evidence | Next State |
| --- | --- | --- | --- | --- | --- |
| `service_matrix` hash changed after snapshot refresh | close with existing pre-planner refresh write | run planner with `--pre-planner-refresh write` | `/usr/local/bin/v7-users-autoswitch` | `fix_pre_planner_refresh_write_planner_dry_run.json` | load refreshed snapshots before planner |
| source is volatile but stable during refresh build | reuse existing stable source retry logic | no code change | `/usr/local/bin/v7-intelligence-snapshot-refresh` | refresh result `source_stable=true` | snapshot source mismatch closed |
| deploy mismatch | no action | not present | `tools/v7-truth-check` | truth PASS | no deploy |
| schema/hash bug | no action | not present | snapshot validator | validation errors only source mismatch | no code fix |

No new planner, truth source, or snapshot root was created.

## 4. Safe Fix And Retest

Safe fix applied:

```text
/usr/local/bin/v7-users-autoswitch \
  --pre-planner-refresh write \
  --pre-planner-refresh-command /usr/local/bin/v7-intelligence-snapshot-refresh \
  --pretty
```

This was a dry-run planner invocation. It did not include `--apply`.

Evidence:

- `medium_batch_readiness_evidence/fix_pre_planner_refresh_write_planner_dry_run.json`
- `medium_batch_readiness_evidence/post_fix_truth_check.json`
- `medium_batch_readiness_evidence/post_fix_convergence_status.json`

Fix result:

| Field | Value |
| --- | --- |
| pre_planner_refresh_state | REFRESH_SUCCESS |
| pre_planner_refresh_source_stable | true |
| snapshot_count | 11 |
| snapshot_stop_required | false |
| source_mismatch_families | `[]` |
| stop_families | `[]` |
| apply_requested | false |
| users_moved | false |

Post-fix truth:

| Check | Result |
| --- | --- |
| truth-check | PASS / FULLY_ALIGNED |
| convergence-status | PASS |
| runtime action status | READY_FOR_RUNTIME_ACTION |

Snapshot blocker verdict: closed.

## 5. MEDIUM_BATCH Readiness Tests

MEDIUM_BATCH scope was tested as dry-run only:

```text
/usr/local/bin/v7-users-autoswitch \
  --pre-planner-refresh write \
  --pre-planner-refresh-command /usr/local/bin/v7-intelligence-snapshot-refresh \
  --max-selected-moves 5 \
  --pretty
```

Evidence:

- `medium_batch_readiness_evidence/medium_batch_scope_dry_run.json`
- `medium_batch_readiness_evidence/medium_batch_scope_summary.json`
- `medium_batch_readiness_evidence/medium_batch_selected_moves.json`
- `medium_batch_readiness_evidence/post_dry_run_target_users_registry.txt`

Readiness fields:

| Field | Value |
| --- | --- |
| apply_requested | false |
| snapshot_stop_required | false |
| source_mismatch_families | `[]` |
| candidate_moves_total | 15 |
| healthy_egress_total | 2 |
| selected_moves_before_gate | 5 |
| selected_moves_after_gate | 2 |
| final selected_moves | 0 |
| terminal_reason | `dry_run_restore_barrier_clearance_generation_expired` |

Authority state:

| Field | Value |
| --- | --- |
| authority_class | SMALL_BATCH |
| prepared_authority_class | SMALL_BATCH |
| certified_authority_class | SMALL_BATCH |
| runtime_authority_class | SMALL_BATCH |
| current_allowed_user_budget | 2 |
| next_authority_class | MEDIUM_BATCH |
| next_allowed_user_budget | 5 |
| authority_cap_applied | true |

Planner behavior:

The planner found a MEDIUM-sized candidate surface, but the authority gate correctly capped requested budget 5 down to the current certified SMALL_BATCH budget 2. It then produced no final selected moves because the existing restore-barrier clearance was generation-expired and scoped to the previous 2-user `vless` operation.

Target users after dry-run:

| User | Current egress |
| --- | --- |
| `10.0.0.3` | `vless` |
| `10.0.0.6` | `vless` |

No user movement occurred.

## 6. Readiness Decision

Technical snapshot blocker: closed.

MEDIUM_BATCH candidate review: available.

MEDIUM_BATCH execution: not ready and not safe.

Reason:

The system is currently certified at SMALL_BATCH with runtime budget 2. A budget 5 dry-run is visible to the planner but is intentionally capped by the authority gate. The previous restore barrier is also expired and scoped to the old 2-user operation, so it cannot authorize a 5-user operation.

This is the correct safe behavior. It means the next stage is not execution. The next stage is MEDIUM_BATCH preparation: authority/governance review, fresh 5-user approval packet review, and fresh restore-barrier generation for a proposed budget 5 cohort.

## Final Verdicts

| Verdict | Value |
| --- | --- |
| baseline_collected | true |
| snapshot_root_cause_identified | true |
| safe_fix_applied | true |
| snapshot_stop_required | false |
| source_mismatch_families | `[]` |
| planner_dry_run_clean | false |
| medium_batch_candidates_available | true |
| ready_for_medium_batch_preparation | true |
| ready_for_medium_batch_execution | false |
| users_moved | 0 |
| autoswitch_apply_run | false |
| authority_promoted | false |
| SAFE_NEXT_STEP | `PREPARE_MEDIUM_BATCH_5_USER_APPROVAL_PACKET_REVIEW_WITH_FRESH_RESTORE_BARRIER` |

## Remaining Blocker

One proven blocker remains for execution:

`MEDIUM_BATCH_EXECUTION_AUTHORITY_NOT_PREPARED_OR_CERTIFIED`

Evidence:

- current certified authority is SMALL_BATCH
- current runtime budget is 2
- requested budget 5 was capped to 2
- previous restore barrier clearance is expired and scoped to 2 users

Safe fix path:

1. Start a dedicated MEDIUM_BATCH preparation program.
2. Reuse the existing authority lifecycle and approval packet system.
3. Generate a fresh 5-user candidate review without apply.
4. Generate/review a fresh restore barrier and rollback manifest for budget 5.
5. Require explicit operator approval before any live governed apply.

Do not execute MEDIUM_BATCH until the preparation packet and authority review are complete.
