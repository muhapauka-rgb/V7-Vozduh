# BA.3 Five User Autonomy Certification Report

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Date: 2026-06-13

## 1. Executive Summary

BA.3 did not certify five-user autonomy.

The system successfully reached the five-user execution gate:

- truth-check: PASS
- convergence: PASS
- runtime action safe: true
- policy limit raised from 2 to 5 through the admin API
- fresh planner produced 5 real planner-selected users
- fresh approval packet was created
- fresh restore barrier was written
- pre-execution dry-run showed 5 selected moves and a valid atomic envelope

Execution did not move users. The apply path failed closed because the atomic execution envelope detected source bundle drift in:

- `service-scores`
- `channel-service-scores`

This happened repeatedly between restore barrier clearance and apply. Therefore BA.3 is blocked by a source bundle stability issue, not by planner quality, governance authority, packet generation, restore barrier ownership, rollback readiness, or user availability.

For safety, after the blocker was proven, `autoswitch_max_planned_per_run` was returned from 5 to the previous certified value 2 through the canonical admin policy update path.

Final verdict: `FIVE_USER_AUTONOMY_BLOCKED`

## 2. Truth Gate

Initial truth gate passed.

Evidence:

- `docs/reports/evidence/BA3_EVIDENCE/phase1_truth_check.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase1_convergence_status.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase2_truth_after_policy_network.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase2_convergence_after_policy_network.json`

Final pre-execution truth after policy escalation:

- `final_verdict=PASS`
- `blockers=[]`
- `runtime_action_safe=true`
- `runtime_action_status=READY_FOR_RUNTIME_ACTION`

## 3. Policy Escalation

Canonical owner: admin API `/api/actions/policy-update`

Policy was raised:

- before: `autoswitch_max_planned_per_run=2`
- after: `autoswitch_max_planned_per_run=5`
- authority budget remained: `current_allowed_user_budget=25`
- mode remained: `guarded`

Evidence:

- `docs/reports/evidence/BA3_EVIDENCE/phase2_policy_before.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase2_policy_update_patch.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase2_policy_update_response.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase2_policy_update_summary.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase2_policy_after.json`

## 4. Fresh Planner

The fresh planner produced sufficient real candidates.

Planner result:

- active users: 26
- candidate moves total: 23
- authority selected before restore barrier: 5
- authority budget: 25
- snapshot source mismatch families: []
- snapshot stop required: false

The 5 planner-selected moves were:

| User | From | To |
|---|---|---|
| `10.7.0.3` | `vless` | `awg3` |
| `10.7.0.2` | `vless` | `awg3` |
| `10.7.0.4` | `vless` | `awg0` |
| `10.7.0.6` | `vless` | `awg3` |
| `10.7.0.8` | `vless` | `awg0` |

Evidence:

- `docs/reports/evidence/BA3_EVIDENCE/phase3_fresh_planner.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase3_fresh_planner_summary.json`

## 5. Packet

A fresh five-user packet was created through the canonical packet owner.

Packet properties:

- selected users: 5
- allowed targets: `awg0`, `awg3`
- rollback manifest: present
- user substitution: forbidden
- target substitution: forbidden
- executor reselect: forbidden

Evidence:

- `docs/reports/evidence/BA3_EVIDENCE/phase4_ba3_packet_generate.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase4_ba3_packet.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase4_ba3_packet_summary.json`

## 6. Restore Barrier

A fresh restore barrier clearance was written through the canonical runtime action owner.

Restore barrier result:

- verdict: `RESTORE_BARRIER_CLEARANCE_WRITTEN`
- recheck verdict: `ALLOW_RESTORE_BARRIER_CLEARANCE`
- selected move count: 5
- allowed users matched the packet
- allowed targets matched the packet
- rollback manifest was bound
- user movement: false

Evidence:

- `docs/reports/evidence/BA3_EVIDENCE/phase5_ba3_restore_barrier.json`

## 7. Pre-Execution Recheck

The post-clearance dry-run passed.

Result:

- selected moves: 5
- users matched packet
- targets matched packet
- atomic condition: `ENVELOPE_VALID`
- atomic mismatches: []
- snapshot stop required: false
- source mismatch families: []
- restore barrier generation valid: true

Evidence:

- `docs/reports/evidence/BA3_EVIDENCE/phase6_post_clearance_dry_run.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase6_post_clearance_dry_run_summary.json`

## 8. Autonomous Execution Attempt

The first apply attempt did not move users.

Result:

- terminal state: `NOOP`
- terminal reason: `no_selected_moves`
- applied: false
- selected moves at execution: 0
- atomic condition: `SOURCE_CHANGED`
- atomic mismatches:
  - `channel-service-scores`
  - `service-scores`

Evidence:

- `docs/reports/evidence/BA3_EVIDENCE/phase7_five_user_apply.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase7_drift_blocker_analysis.json`

## 9. Drift Retry

BA.3 performed bounded retries instead of forcing execution.

Retry 1:

- fresh planner kept the same five users and targets
- fresh packet was created
- fresh restore barrier was written
- post-clearance dry-run passed
- apply still failed closed with `SOURCE_CHANGED`

Retry 2:

- fresh planner and packet were created again
- fresh restore barrier was written again
- no-refresh dry-run still reported `SOURCE_CHANGED`

The repeated failure proves the blocker is not a stale packet only. The blocker is repeated source bundle instability or validation disagreement around `service-scores` and `channel-service-scores` between clearance and apply.

Evidence:

- `docs/reports/evidence/BA3_EVIDENCE/phase7_retry1_fresh_planner.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase7_retry1_packet.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase7_retry1_restore_barrier.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase7_retry1_post_clearance_dry_run.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase7_retry1_five_user_apply.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase7_retry2_fresh_planner.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase7_retry2_packet.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase7_retry2_restore_barrier.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase7_retry2_no_refresh_dry_run.json`

## 10. Post Attempt Safety Review

No user movement occurred.

The five BA.3 candidates remained on `vless`:

```text
ip=10.7.0.3 current=vless table=1001 enabled=1
ip=10.7.0.2 current=vless table=1000 enabled=1
ip=10.7.0.4 current=vless table=1002 enabled=1
ip=10.7.0.6 current=vless table=1004 enabled=1
ip=10.7.0.8 current=vless table=1006 enabled=1
```

Evidence:

- `docs/reports/evidence/BA3_EVIDENCE/phase9_exact_candidate_users_registry_after_block.txt`

## 11. Policy Revert

Because five-user autonomy was not certified, the planned autonomy limit was returned to the previous certified level.

Policy revert:

- `autoswitch_max_planned_per_run`: 5 -> 2
- `autoswitch_max_failover_per_run`: 25 unchanged
- canonical owner: admin API `/api/actions/policy-update`

Evidence:

- `docs/reports/evidence/BA3_EVIDENCE/phase9_policy_revert_patch.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase9_policy_revert_response.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase9_policy_revert_summary.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase9_policy_after_revert_overview.json`

## 12. Final Truth After Block

After the blocked execution and policy revert:

- truth-check: PASS
- convergence: PASS
- runtime action safe: true
- blockers: []

Evidence:

- `docs/reports/evidence/BA3_EVIDENCE/phase9_truth_after_block_and_policy_revert.json`
- `docs/reports/evidence/BA3_EVIDENCE/phase9_convergence_after_block_and_policy_revert.json`

## 13. Final Certification

Final verdict: `FIVE_USER_AUTONOMY_BLOCKED`

Single blocker:

`approval_to_apply_source_bundle_mismatch_service_scores_channel_service_scores`

Final verdicts:

- truth_gate_passed=true
- policy_escalated_to_5=true
- five_real_planner_candidates_available=true
- packet_created=true
- restore_barrier_created=true
- pre_execution_recheck_pass=true
- users_moved=0
- only_approved_users_moved=true
- verification_passed=false
- rollback_required=false
- feedback_materialized=false
- trust_updated=false
- prediction_updated=false
- recommendation_updated=false
- planner_reuse_verified=false
- policy_reverted_to_2=true
- five_user_autonomy_certified=false
- final_verdict=FIVE_USER_AUTONOMY_BLOCKED

Safe next step:

`PROGRAM BA3.BLOCKER_SOURCE_BUNDLE_STABILITY_CLOSURE`

The next program should not retry BA.3 execution directly. It should close the repeated `service-scores` / `channel-service-scores` source bundle mismatch between restore barrier clearance and apply, then rerun BA.3 from a fresh packet.
