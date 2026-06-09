# PROGRAM MEDIUM BATCH CONTROLLED LIVE COMPLETION AND EXECUTION CERTIFICATION REPORT

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Date: 2026-06-06

## Executive Verdict

MEDIUM_BATCH authority remains valid and production truth is aligned.

The controlled live execution did not proceed to apply. The program stopped at the mandatory dry-run recheck gate because the fresh restore-barrier clearance no longer matched the planner-selected move hash.

No users were moved.

This is a safe NO-GO caused by planner target volatility between approval packet generation and post-clearance dry-run recheck.

## Phase 1 - Truth Check

Result: PASS.

- `tools/v7-truth-check --all --json`: `PASS`, `FULLY_ALIGNED`
- `tools/v7-convergence-status --json`: `PASS`, `ALIGNED`
- runtime action status: `READY_FOR_RUNTIME_ACTION`

Evidence:

- `medium_batch_controlled_live_evidence/phase1_truth_check.json`
- `medium_batch_controlled_live_evidence/phase1_convergence_status.json`

## Phase 2 - Fresh 5 User Planner

Fresh production planner was run with:

- `--pre-planner-refresh write`
- `--max-selected-moves 5`

Result before restore-barrier gate:

- authority: `MEDIUM_BATCH`
- allowed budget: `5`
- selected moves before authority gate: `5`
- selected moves after authority gate: `5`
- authority cap applied: false

Initial approved candidate set:

| User | From | To | Move Type |
| --- | --- | --- | --- |
| `10.7.0.4` | `amneziawg-exec-20260528-10-8-1-14` | `vless` | `failover` |
| `10.7.0.6` | `amneziawg-exec-20260528-10-8-1-14` | `vless` | `failover` |
| `10.7.0.8` | `amneziawg-exec-20260528-10-8-1-14` | `vless` | `failover` |
| `10.7.0.9` | `awg0` | `vless` | `failover` |
| `10.7.0.10` | `awg0` | `vless` | `failover` |

Final `selected_moves` was still `0` at this point because no fresh restore-barrier clearance had been written yet.

Evidence:

- `medium_batch_controlled_live_evidence/phase2_fresh_planner.json`
- `medium_batch_controlled_live_evidence/phase2_fresh_planner_remote.json`

## Phase 3 - 5 User Approval Packet

Production approval packet was generated through the canonical packet owner.

Result:

- packet id: `pkt_73461d6948a11fd8930df1a9`
- approval id: `appr_f95443b36ca2771ae5cb2abd`
- selected move count: `5`
- selected move budget: `5`
- approved target: `vless`
- rollback manifest items: `5`
- approved plan lock present: true
- atomic envelope present: true

Evidence:

- `medium_batch_controlled_live_evidence/phase3_packet_generation.json`
- `medium_batch_controlled_live_evidence/phase3_five_user_approval_packet.json`

## Phase 4 - Restore Barrier Clearance

Packet recheck and restore-barrier clearance were run through:

- `/usr/local/bin/v7-operator-execution-packet`
- owner: `admin_core/operator_execution.py`

Result:

- recheck verdict: `ALLOW_RESTORE_BARRIER_CLEARANCE`
- clearance verdict: `RESTORE_BARRIER_CLEARANCE_WRITTEN`
- selected move count: `5`
- users matched packet: true
- runtime action scope: restore-barrier clearance only
- user movement: false
- autoswitch apply: false

Evidence:

- `medium_batch_controlled_live_evidence/phase4_restore_barrier_clearance.json`

## Phase 5 - Dry-Run Recheck

Mandatory post-clearance dry-run failed the exact-match gate.

Expected:

- `selected_moves=5`
- users match approval packet
- target matches approval packet
- selected move hash matches restore barrier

Observed:

- `selected_moves=0`
- selected users: none
- approved users: `10.7.0.4`, `10.7.0.6`, `10.7.0.8`, `10.7.0.9`, `10.7.0.10`
- approved target: `vless`
- current planner target after recheck: `awg3`
- guard reason: `restore_barrier_clearance_selected_moves_hash_mismatch`
- approved selected move hash: `b47437e7614ca203bc6b06498bfb1ab4d97c101a8910310c9448a7c3dc647141`
- current selected move hash: `3112289879fa9640295a6e4fd30783d28fa64245dfa258b745d7c0f2212dd10d`

Current post-clearance candidate set before guard changed to:

| User | From | New Planner Target | Move Type |
| --- | --- | --- | --- |
| `10.7.0.4` | `amneziawg-exec-20260528-10-8-1-14` | `awg3` | `failover` |
| `10.7.0.6` | `amneziawg-exec-20260528-10-8-1-14` | `awg3` | `failover` |
| `10.7.0.8` | `amneziawg-exec-20260528-10-8-1-14` | `awg3` | `failover` |
| `10.7.0.9` | `awg0` | `awg3` | `failover` |
| `10.7.0.10` | `awg0` | `awg3` | `failover` |

The approved packet was for `vless`, but the current planner recheck selected `awg3`. The restore-barrier hash mismatch correctly blocked apply.

Evidence:

- `medium_batch_controlled_live_evidence/phase5_dry_run_recheck.json`
- `medium_batch_controlled_live_evidence/phase5_hash_mismatch_diagnostics.txt`

## Stop Decision

The prompt required STOP if dry-run recheck did not show exactly 5 approved selected moves.

STOP was executed.

No `v7-users-autoswitch --apply --verify` was run.

No users were moved.

Current registry rows for the approved users after stop:

```text
ip=10.7.0.4 current=amneziawg-exec-20260528-10-8-1-14 table=1002 enabled=1
ip=10.7.0.6 current=amneziawg-exec-20260528-10-8-1-14 table=1004 enabled=1
ip=10.7.0.8 current=amneziawg-exec-20260528-10-8-1-14 table=1006 enabled=1
ip=10.7.0.9 current=awg0 table=1007 enabled=1
ip=10.7.0.10 current=awg0 table=1008 enabled=1
```

Evidence:

- `medium_batch_controlled_live_evidence/phase5_approved_users_current_registry_rows.txt`

## Post-Stop Truth

Post-stop read-only checks:

- truth check: `PASS`, `FULLY_ALIGNED`
- first convergence attempt: transient GitHub read NO-GO
- convergence retry: `PASS`, `ALIGNED`, `READY_FOR_RUNTIME_ACTION`

Evidence:

- `medium_batch_controlled_live_evidence/phase5_stop_truth_check.json`
- `medium_batch_controlled_live_evidence/phase5_stop_convergence_status.json`
- `medium_batch_controlled_live_evidence/phase5_stop_convergence_status_retry.json`

## Root Cause

The approved target changed between packet generation and dry-run recheck:

- packet target: `vless`
- recheck target: `awg3`

The most likely immediate cause is volatile service/eligibility/load-balancing input after the pre-planner refresh. The planner saw two healthy egresses during recheck and selected `awg3` as the current best target. Because the approved packet was bound to `vless`, the restore-barrier selected-move hash changed and the approved plan lock failed closed.

This proves the gate is working: no execution can proceed after target drift.

## Final Verdicts

truth_check_pass=true

fresh_planner_pass=true

five_user_packet_ready=true

restore_barrier_fresh=true

dry_run_recheck_pass=false

users_selected=0

users_moved=0

only_approved_users_moved=true

verification_passed=false

rollback_required=false

rollback_executed=false

outcomes_materialized=false

trust_feedback_updated=false

prediction_feedback_updated=false

recommendation_feedback_updated=false

medium_batch_execution_completed=false

medium_batch_execution_certified=false

current_runtime_authority=MEDIUM_BATCH

current_allowed_user_budget=5

safe_for_large_batch_review=false

safe_for_autonomy_review=false

SAFE_NEXT_STEP=CLOSE_PLANNER_TARGET_VOLATILITY_BETWEEN_PACKET_AND_RECHECK_THEN_RETRY_MEDIUM_BATCH_LIVE_COMPLETION_FROM_FRESH_PLANNER

## Required Next Step

Do not retry apply directly.

Next work should close the packet-to-recheck target drift:

1. compare service truth and planner inputs between `phase2_fresh_planner_remote.json` and `phase5_dry_run_recheck.json`;
2. identify why target changed from `vless` to `awg3`;
3. decide whether this is expected load-balancing behavior or unstable service truth;
4. if expected, regenerate a fresh packet for the current target and rerun the gate from Phase 2;
5. if unstable, fix the volatility source before any new packet;
6. only apply when post-clearance dry-run shows exactly 5 selected moves matching the packet.
