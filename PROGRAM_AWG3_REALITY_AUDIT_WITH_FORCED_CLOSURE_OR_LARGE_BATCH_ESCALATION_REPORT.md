# PROGRAM AWG3 REALITY AUDIT WITH FORCED CLOSURE OR LARGE BATCH ESCALATION REPORT

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Evidence: `awg3_forced_closure_large_escalation_evidence/`

## Executive Verdict

AWG3 is recovered.

The previous `stability_below_floor` classification is no longer current after a
fresh production reality audit and planner recheck. No planner floor was lowered,
no eligibility was forced, no users were moved, and no apply was executed.

The system may proceed to LARGE_BATCH authority and packet preparation.

This does not authorize LARGE_BATCH execution yet.

## Production Truth

Evidence:

- `production_truth.json`
- `convergence_status.json`

Result:

- local/GitHub/production commit aligned at
  `8dda6fa35a7657f28c7a4164bdfd2a3ab6729989`
- `truth_check_final_verdict=PASS`
- `convergence_status=ALIGNED`
- `runtime_action_status=READY_FOR_RUNTIME_ACTION`
- no runtime mutation was performed by this program

## Phase 1 - AWG3 Reality Audit

Evidence:

- `awg3_reality_audit.json`
- `awg3_direct_reality_probe.txt`
- `planner_dry_run_before.json`

Fresh AWG3 state:

| Signal | Value |
| --- | --- |
| Planner eligible | true |
| Planner blocks | none |
| Current stability | 0.831 |
| 1h stability | 0.5598 |
| Required stability | 0.45 |
| Avg Mbps | 59.06 |
| Min Mbps | 49.09 |
| Service score | 100.0 |
| Telegram | OK |
| Capacity | OK, 0/14 hard |
| Best available pool | rank 1 |

Direct interface probe:

- `awg3` link is up
- route via `awg3` exists
- ping to `8.8.8.8`: 0 percent packet loss
- ping avg latency: 34.820 ms
- Google check: HTTP 204, rc 0
- YouTube check: HTTP 204, rc 0
- Instagram check: HTTP 200, rc 0
- Google Auth check: HTTP 200, rc 0

Conclusion:

AWG3 is not currently proven unsuitable for production routing.

## Phase 2 - Stability Calculation Audit

Evidence:

- `stability_policy_defaults.txt`
- `stability_gate_code.txt`
- `load_health_gate_code.txt`
- `awg3_stability_model.json`

Model:

- owner: `tools/v7-users-autoswitch`
- default `min_stability=0.45`
- quality gate checks:
  - current candidate stability
  - `egress-quality-summary.items[egress].windows.1h.stability`
  - current avg/min Mbps
  - 1h avg/min Mbps
  - service suitability
  - severity classification

Blocking rule:

If current stability exists and is below `min_stability`, the planner allows the
candidate only if an evidence-backed exception applies or 1h stability is above
the floor. Otherwise it blocks with `stability_below_floor`.

Fresh AWG3 values:

- current stability: 0.831
- 1h stability: 0.5598
- required floor: 0.45
- avg Mbps: 59.06
- min Mbps: 49.09
- 1h avg Mbps: 51.633
- 1h min Mbps: 30.191

Conclusion:

AWG3 now passes the actual stability model.

## Phase 3 - Root Cause Classification

Evidence:

- `awg3_root_cause.json`

Classification:

`STALE_HISTORY`

Meaning:

The previous blocker was caused by an older quality/stability view. Fresh
pre-planner refresh and planner dry-run now show:

- `awg3 eligible=true`
- `blocked=[]`
- current stability above floor
- 1h stability above floor
- services healthy
- Telegram healthy
- capacity healthy

Rejected classifications:

- `REAL_INSTABILITY`: rejected by current planner and direct probe
- `SERVICE_ISSUE`: rejected, service score is 100
- `CAPACITY_ISSUE`: rejected, load is 0/14 hard
- `POLICY_ISSUE`: rejected, AWG3 is not reserved/manual/canary
- `MEASUREMENT_ARTIFACT`: not proven as a code bug

## Phase 4 - Safe Fix Review

Evidence:

- `awg3_fix_review.json`

Fix verdict:

- `awg3_fix_available=false`
- `awg3_fix_applied=false`

Reason:

No fix was required. The safe existing recheck path cleared the stale stability
classification without forcing eligibility, lowering planner floors, changing
governance, or mutating routes.

## Phase 5 - Retest

Evidence:

- `planner_retest_summary.json`
- `awg3_retest.json`
- `large_batch_candidate_foundation.json`

Planner retest:

- `snapshot_stop_required=false`
- `source_mismatch_families=[]`
- `pre_planner_refresh_state=REFRESH_SUCCESS`
- `healthy_egress_total=3`
- `candidate_moves_total=17`
- `selected_moves=0`
- `terminal_state=DRY_RUN`
- `terminal_reason=dry_run_restore_barrier_clearance_generation_expired`

Interpretation:

Planner and snapshot gate are healthy. The dry-run correctly selected zero moves
because no fresh approval packet or restore-barrier clearance exists for this new
generation.

## Phase 6 - AWG3 Decision

Evidence:

- `awg3_decision.json`

Decision:

`AWG3_RECOVERED`

Result:

- `awg3_recovered=true`
- `awg3_eligible=true`
- no second AWG3 investigation is needed

## Phase 7 - Pool Review

Evidence:

- `pool_review.json`

Eligible pool after review:

- `vless`
- `awg0`
- `awg3`

Pool counts:

- `eligible_pool_after_review=3`
- `healthy_pool_after_review=5`
- `eligible_soft_spare_users=21`
- `eligible_hard_spare_users=28`

Note:

`vless` is currently soft-full, but `awg0` and `awg3` have sufficient empty
capacity for LARGE_BATCH packet preparation.

## Phase 8 - LARGE_BATCH Decision

Evidence:

- `large_batch_decision.json`
- `large_batch_preparation_foundation.json`

Decision:

`large_batch_preparation_ready=true`

Current LARGE_BATCH preparation pool:

- `vless`
- `awg0`
- `awg3`

Candidate foundation:

The planner currently recommends `awg3` as the primary target for a 10-user
preparation foundation. This is not an approval packet and not an execution
authorization.

First 10 candidate users in the foundation:

| User | Current | Recommended | Confidence |
| --- | --- | --- | --- |
| `10.0.0.2` | `vless` | `awg3` | medium |
| `10.0.0.3` | `vless` | `awg3` | medium |
| `10.0.0.6` | `vless` | `awg3` | medium |
| `10.7.0.3` | `vless` | `awg3` | medium |
| `10.7.0.2` | `vless` | `awg3` | medium |
| `10.7.0.4` | `vless` | `awg3` | medium |
| `10.7.0.5` | `vless` | `awg3` | medium |
| `10.7.0.6` | `vless` | `awg3` | medium |
| `10.7.0.8` | `vless` | `awg3` | medium |
| `10.7.0.9` | `vless` | `awg3` | medium |

Execution status:

- `large_batch_execution_ready=false`
- authority review still required
- approval packet still required
- rollback manifest still required
- restore barrier review still required
- operator approval still required

## Phase 9 - Escalation Rule

Evidence:

- `escalation_report.json`

AWG3 audit is closed.

Because AWG3 recovered, the correct escalation is:

`LARGE_BATCH_AUTHORITY_AND_PACKET_PREPARATION`

No second AWG3 investigation should be opened unless AWG3 fails again during the
actual LARGE_BATCH packet/recheck gate.

## Final Verdicts

```text
awg3_root_cause_identified=true
awg3_fix_available=false
awg3_fix_applied=false
awg3_recovered=true
awg3_eligible=true
eligible_pool_after_review=3
healthy_pool_after_review=5
large_batch_pool_ready=true
large_batch_preparation_ready=true
single_blocker=NONE
users_moved=0
apply_executed=false
authority_promoted=false
SAFE_NEXT_STEP=LARGE_BATCH_AUTHORITY_AND_PACKET_PREPARATION
```
