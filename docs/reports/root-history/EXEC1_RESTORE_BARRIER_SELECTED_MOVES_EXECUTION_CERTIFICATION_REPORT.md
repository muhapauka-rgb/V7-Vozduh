# EXEC.1 Restore Barrier Selected Moves Execution Certification Report

## 1. Executive Summary

Final certification: `EXECUTION_BLOCKED`.

The selected moves are fully explained.

Current production planner facts:

| Item | Value |
|---|---|
| planner owner | `tools/v7-users-autoswitch` |
| approval packet owner | `admin_core/operator_execution.py` |
| restore barrier owner | `admin_core/operator_execution.py` |
| users_total | `26` |
| healthy_egress_total | `1` |
| candidate_moves_total | `16` |
| candidate target | `vless` |
| authority budget | `25` |
| selected_moves_before_restore_barrier | `16` |
| restore barrier clearance budget | `10` |
| selected_moves_after_gate | `0` |
| terminal_reason | `dry_run_restore_barrier_clearance_selected_moves_exceed_budget` |
| snapshot_stop_required | `false` |
| source_mismatch_families | `[]` |

Root cause:

```text
STALE_RESTORE_BARRIER_CLEARANCE + STALE_APPROVED_PLAN_LOCK
```

The current restore barrier is an old nonzero clearance for 10 moves from `2026-06-07`. Current planner reality now has 16 candidate moves to `vless`. The old approved plan lock is invalid because it is expired and user source routes changed. The planner correctly refuses to reuse it.

No production remediation was applied in EXEC.1. A local fresh packet preview was generated as proof of the correct remediation path, but writing the fresh restore barrier clearance to production requires explicit operator approval because it is a governance/runtime mutation.

## 2. Restore Barrier Reality Map

Ownership:

| Function | Owner |
|---|---|
| planner decision | `tools/v7-users-autoswitch` |
| selected move calculation | `tools/v7-users-autoswitch` |
| authority budget gate | `tools/v7-users-autoswitch` |
| restore barrier read | `tools/v7-users-autoswitch` |
| approval packet generation | `admin_core/operator_execution.py` via `tools/v7-operator-execution-packet` |
| restore barrier clearance write | `admin_core/operator_execution.py` |
| apply validation | `tools/v7-users-autoswitch` |
| user movement | existing governed apply path only |

Runtime restore barrier file:

```text
/opt/v7/egress/state/autoswitch-restore-barrier.json
```

Current restore barrier facts:

| Field | Value |
|---|---|
| enabled | `true` |
| generation_clearance | `true` |
| allow_post_ttl_apply | `true` |
| clearance_max_selected_moves | `10` |
| clearance_expected_selected_moves | `10` |
| clearance_expires_at | `2026-06-07T12:10:45.714602+00:00` |
| allowed_targets | `awg0`, `awg3` in old clearance |
| current fresh planner target | `vless` |
| approved_plan_lock_ok | `false` |
| approved_plan_lock_invalid_reasons | `approved_plan_lock_expired`, `approved_plan_lock_user_source_mismatch` |

Evidence:

- `docs/reports/evidence/EXEC1_EVIDENCE/autoswitch_plan_summary.json`
- `docs/reports/evidence/EXEC1_EVIDENCE/operator_overview_summary.json`
- `docs/reports/evidence/EXEC1_EVIDENCE/planner_restore_barrier_code_refs.txt`
- `docs/reports/evidence/EXEC1_EVIDENCE/operator_execution_code_refs.txt`

## 3. Selected Move Forensics

Pipeline:

```text
active users
  -> planner decisions
  -> switch candidates
  -> authority budget gate
  -> restore barrier gate
  -> selected_moves
  -> apply gate
```

Observed current pipeline:

| Stage | Result |
|---|---|
| active planner users | `26` |
| switch decisions | `16` |
| keep decisions | `10` |
| recommended target for all switches | `vless` |
| authority budget gate | allows `16 <= 25` |
| restore barrier gate | blocks `16 > 10` |
| selected_moves | `[]` |

The exact point where moves disappear is the restore barrier gate, after authority budget and before final `selected_moves`.

Current switch decision reason:

```text
current_egress_not_eligible
```

Current affected users:

```text
10.7.0.5
10.0.0.2
10.0.0.3
10.0.0.6
10.7.0.3
10.7.0.2
10.7.0.4
10.7.0.6
10.7.0.8
10.7.0.9
10.7.0.10
10.7.0.11
10.7.0.12
10.7.0.13
10.7.0.14
10.7.0.15
```

Evidence:

- `docs/reports/evidence/EXEC1_EVIDENCE/current_switch_decisions.json`
- `docs/reports/evidence/EXEC1_EVIDENCE/approved_candidate_moves_before_guard.json`
- `docs/reports/evidence/EXEC1_EVIDENCE/autoswitch_plan_summary.json`

## 4. Budget Clearance Root Cause

The terminal reason is correct:

```text
restore_barrier_clearance_selected_moves_exceed_budget
```

Why:

| Field | Value |
|---|---|
| current selected before restore barrier | `16` |
| old clearance max selected moves | `10` |
| comparison | `16 > 10` |
| result | selected moves suppressed |

Who produced it:

`tools/v7-users-autoswitch` computes the fresh plan and checks the existing restore barrier. The code path records:

```text
clearance_selected_moves_before_guard = len(selected)
clearance_budget_exceeded = len(selected) > clearance_max_selected_moves
clearance_guard_reason = restore_barrier_clearance_selected_moves_exceed_budget
selected = []
```

Deeper cause:

The old restore barrier is not only too small. It is also stale:

| Field | Old approved clearance | Current planner reality |
|---|---|---|
| selected move count | `10` | `16` |
| selected move hash | `2ce019...` | `25c2fe...` |
| planner generation | `6b3a40...` | `8cb2eb...` |
| targets | `awg0`, `awg3` | `vless` |
| lock expiry | `2026-06-07T12:10:45Z` | current run: `2026-06-11` |

So the blocker is not a false positive. The planner is refusing to execute a changed plan under an old clearance.

## 5. Counterfactual Analysis

If restore barrier budget passed without a fresh packet:

| Question | Answer |
|---|---|
| Would selected moves appear if only budget changed from 10 to 16? | Not safely |
| Would execution proceed using the old clearance? | No |
| Why? | generation/hash/count/expiry still mismatch |
| Would planner produce valid candidates? | Yes, 16 candidates to `vless` |
| Would governance permit execution? | Not with the old clearance |
| Actual blast radius now | 16 users |

Predicted next blockers if only the budget number were changed:

```text
restore_barrier_clearance_generation_expired
restore_barrier_clearance_generation_mismatch
restore_barrier_clearance_selected_moves_hash_mismatch
restore_barrier_clearance_selected_moves_count_mismatch
```

Evidence:

- `docs/reports/evidence/EXEC1_EVIDENCE/counterfactual_summary.json`

## 6. Governance Readiness

Governance is behaving correctly.

Positive:

| Gate | Status |
|---|---|
| authority | `PASS` |
| evaluator | `PASS` |
| concurrency | `PASS` |
| restore_settle | `PASS` |
| selected_moves | `PASS` |
| hidden_movers | `PASS` |
| containment_state | `PASS` |

Not ready:

| Gate | Status |
|---|---|
| conflict_resolver | `FAIL` |
| capacity | `FAIL` |
| target_readiness | `FAIL` |
| runtime_trust | `REVIEW_REQUIRED` |
| release_trust | `REVIEW_REQUIRED` |
| required_services | `REVIEW_REQUIRED` |
| policy | `REVIEW_REQUIRED` |
| routing_mode | `REVIEW_REQUIRED` |
| group_constraints | `REVIEW_REQUIRED` |

Execution dashboard says:

```text
status = NOT_READY
execution_allowed_now = false
execution_engine_present = false
readiness_reason = One or more validation gates failed closed.
```

Important: the execution readiness surface is preview-only/read-only. It does not currently expose a production execution engine as ready.

Evidence:

- `docs/reports/evidence/EXEC1_EVIDENCE/execution_readiness_summary.json`
- `docs/reports/evidence/EXEC1_EVIDENCE/execution_readiness_raw.json`

## 7. One User Execution Readiness

Current verdict:

```text
ONE_USER_READY=false
```

Reason:

There is no current one-user approval packet and no current one-user restore barrier clearance matching the fresh planner generation.

Can one-user execution be prepared safely?

```text
yes, with a fresh scoped one-user packet and restore barrier clearance
```

Required next evidence:

1. Fresh planner dry-run scoped to one approved user.
2. `max_selected_moves=1`.
3. Fresh packet generated from that exact plan.
4. Runtime recheck against the same generation/hash.
5. Restore barrier clearance written by `admin_core/operator_execution.py`.
6. Post-clearance dry-run confirms exactly one selected move.
7. Only then, explicit apply approval.

No one-user movement was performed.

## 8. Small Batch Readiness

Current verdict:

```text
SMALL_BATCH_READY=false
```

Reason:

The current fresh plan naturally contains 16 candidate moves. The system can generate a fresh 16-user packet preview, but there is no current fresh small-batch packet or restore barrier clearance for 2, 5, or 10 users.

Observed current safe batch size:

```text
0
```

Current unsafe batch sizes:

```text
1, 2, 5, 10, 16
```

They are unsafe now only because no matching fresh governance packet and restore barrier clearance exists. This is governance readiness, not planner inability.

## 9. Root Cause Classification

Final classification:

```text
RESTORE_BARRIER
```

Secondary symptom:

```text
BUDGET_POLICY
```

Not root cause:

| Candidate | Verdict |
|---|---|
| planner | not root cause |
| execution pipeline | not primary root cause |
| snapshot gate | not root cause |
| authority budget | not root cause |

Exact blocker:

```text
stale_restore_barrier_clearance_for_old_10_move_plan_current_plan_has_16_moves
```

## 10. Safe Remediation

Safe remediation path:

```text
fresh planner
  -> fresh scoped packet
  -> fresh restore barrier clearance through admin_core/operator_execution.py
  -> post-clearance dry-run
  -> explicit governed apply approval if selected moves match
```

What was done in EXEC.1:

| Action | Result |
|---|---|
| production selected move forensics | complete |
| restore barrier root cause | complete |
| counterfactual | complete |
| local fresh packet preview from current plan | complete |
| production restore barrier write | not executed |
| autoswitch apply | not executed |
| user movement | not executed |

Local fresh packet preview:

| Field | Value |
|---|---|
| packet schema | `c1.governance-lifecycle-packet.v1` |
| runtime action | `CREATE_RESTORE_BARRIER_CLEARANCE` |
| selected move budget | `16` |
| allowed target | `vless` |
| rollback items | `16` |
| user movement allowed | `false` |
| routing mutation allowed | `false` |
| autoswitch apply allowed | `false` |

Evidence:

- `docs/reports/evidence/EXEC1_EVIDENCE/fresh_packet_preview_generation_result.json`
- `docs/reports/evidence/EXEC1_EVIDENCE/fresh_packet_preview_from_current_plan.json`

Why production remediation was not applied:

Writing restore barrier clearance is a governance/runtime mutation. It does not move users, but it changes production execution readiness. EXEC.1 did not include explicit approval to write a new production restore barrier clearance.

## 11. Retest Results

No production fix was applied, so no post-fix production retest was run.

Read-only retest status:

| Check | Value |
|---|---|
| autoswitch plan rc | `0` |
| snapshot stop | `false` |
| source mismatch families | `[]` |
| planner candidates | `16` |
| selected moves | `0` |
| terminal reason | `dry_run_restore_barrier_clearance_selected_moves_exceed_budget` |

Attempted unsafe/not-approved action:

`planner-refresh-dry-run` POST was not used for EXEC.1 after review rejected it as a production snapshot write. No workaround was attempted.

## 12. Execution Certification

Final answer:

```text
EXECUTION_BLOCKED
```

Detailed verdicts:

| Verdict | Value |
|---|---|
| selected_moves_fully_explained | `true` |
| restore_barrier_fully_explained | `true` |
| budget_clearance_fully_explained | `true` |
| planner_can_find_candidates | `true` |
| snapshot_gate_clean | `true` |
| authority_budget_allows_current_plan | `true` |
| current_restore_barrier_allows_current_plan | `false` |
| one_user_ready_now | `false` |
| one_user_preparable | `true` |
| small_batch_ready_now | `false` |
| small_batch_preparable | `true` |
| execution_ready_now | `false` |
| autoswitch_apply_executed | `false` |
| users_moved | `0` |

## 13. Final Verdict

Final verdict:

```text
EXECUTION_BLOCKED
```

Single final blocker:

```text
fresh_restore_barrier_clearance_missing_for_current_planner_generation
```

Safe next step:

```text
EXEC2_FRESH_SCOPED_PACKET_AND_RESTORE_BARRIER_CLEARANCE_PREP
```

Recommended EXEC2 scope:

1. Choose execution size: `1`, `2`, `5`, `10`, or current full `16`.
2. Run fresh scoped planner dry-run.
3. Generate packet from that exact plan.
4. Request explicit approval for restore barrier clearance write.
5. Write restore barrier clearance only through `admin_core/operator_execution.py`.
6. Run post-clearance dry-run.
7. Stop before apply unless the user explicitly approves governed apply.

No further restore-barrier discovery program is required. The blocker is known and operationally closed to one next action.
