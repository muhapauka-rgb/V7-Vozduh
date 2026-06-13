# STABILITY1.CLOSE Deploy And BA3 Recertification Report

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Date: 2026-06-13

## 1. Executive Summary

STABILITY.1 was deployed successfully.

The old BA.3 blocker was closed in production:

- local commit: `989b5c700591aaf332cc17a981d11c07cb1de5c5`
- GitHub commit: `989b5c700591aaf332cc17a981d11c07cb1de5c5`
- production commit: `989b5c700591aaf332cc17a981d11c07cb1de5c5`
- truth-check after deploy: PASS
- convergence after deploy: PASS
- runtime action safe: true

BA.3 was rerun from a fresh planner, but five-user autonomy was not executed.

Reason:

Fresh production planner found only 3 real candidate moves, not 5.

Per BA.3 safety rules, V7 may not invent users, substitute users, substitute targets, or execute a smaller cohort and call it five-user certification. Therefore execution stopped before packet generation, restore barrier, and apply.

Final verdict: `FIVE_USER_AUTONOMY_BLOCKED`

Single blocker: `insufficient_real_planner_candidates_3_of_5`

## 2. Pre-Deploy Audit

Workspace was clean before STABILITY1.CLOSE evidence was created.

STABILITY.1 commit was already present and pushed:

- `989b5c7 PROGRAM STABILITY.1 source bundle stability closure`

Pre-deploy truth showed deployment was required.

Deploy delta:

- `tools/v7-users-autoswitch`

Evidence:

- `STABILITY1_CLOSE_EVIDENCE/phase1_truth_before_deploy.json`
- `STABILITY1_CLOSE_EVIDENCE/phase1_convergence_before_deploy.json`

## 3. Safe Deploy

Approved deploy command was used:

```bash
tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --restart-admin-if-changed --json
```

Result:

- final verdict: PASS
- no user movement
- no autoswitch apply
- no routing mutation

Evidence:

- `STABILITY1_CLOSE_EVIDENCE/phase4_safe_deploy.json`

## 4. Post-Deploy Truth Gate

Post-deploy truth:

- truth-check: PASS
- convergence: PASS
- deploy delta: []
- production commit: `989b5c700591aaf332cc17a981d11c07cb1de5c5`
- runtime action safe: true

Evidence:

- `STABILITY1_CLOSE_EVIDENCE/phase5_truth_after_deploy.json`
- `STABILITY1_CLOSE_EVIDENCE/phase5_convergence_after_deploy.json`

## 5. BA.3 Policy Preparation

Canonical owner:

- admin API `/api/actions/policy-update`

Policy was raised for the BA.3 attempt:

- `autoswitch_max_planned_per_run`: 2 -> 5
- `autoswitch_max_failover_per_run`: 25 unchanged

Evidence:

- `STABILITY1_CLOSE_EVIDENCE/phase6_admin_session_after_form_login.json`
- `STABILITY1_CLOSE_EVIDENCE/phase6_policy_update_patch.json`
- `STABILITY1_CLOSE_EVIDENCE/phase6_policy_update_response_retry.json`
- `STABILITY1_CLOSE_EVIDENCE/phase6_policy_update_summary_retry.json`

## 6. Fresh Planner

Fresh planner command used production runtime and pre-planner refresh:

```bash
/usr/local/bin/v7-users-autoswitch --pre-planner-refresh write --pre-planner-refresh-command v7-intelligence-snapshot-refresh --max-selected-moves 5 --pretty
```

Planner result:

- users total: 26
- egress total: 7
- healthy egress total: 1
- candidate moves total: 3
- authority selected before restore barrier: 3
- planned limit: 5
- authority budget: 25
- snapshot stop required: false
- source mismatch families: []

Planner-selected real moves:

| User | From | To | Type |
|---|---|---|---|
| `10.0.0.2` | `awg3` | `vless` | failover |
| `10.0.0.3` | `awg0` | `vless` | failover |
| `10.0.0.6` | `awg0` | `vless` | failover |

Evidence:

- `STABILITY1_CLOSE_EVIDENCE/phase6_fresh_planner.json`

## 7. BA.3 Stop Decision

BA.3 requires exactly 5 real planner-selected users.

Fresh planner produced only 3.

Therefore the program stopped before:

- packet generation
- restore barrier generation
- apply
- feedback materialization
- trust update

This is a correct stop. Executing 3 users would not certify five-user autonomy, and adding two synthetic users would violate BA.3 safety rules.

## 8. Safety Cleanup

Because BA.3 was not certified, policy was returned to the previous certified level:

- `autoswitch_max_planned_per_run`: 5 -> 2

Evidence:

- `STABILITY1_CLOSE_EVIDENCE/phase6_policy_revert_patch.json`
- `STABILITY1_CLOSE_EVIDENCE/phase6_policy_revert_response.json`
- `STABILITY1_CLOSE_EVIDENCE/phase6_policy_revert_summary.json`

Candidate users remained in their original state because no apply was executed:

```text
ip=10.0.0.2 current=awg3 table=100 enabled=1
ip=10.0.0.3 current=awg0 table=101 enabled=1
ip=10.0.0.6 current=awg0 table=104 enabled=1
```

Evidence:

- `STABILITY1_CLOSE_EVIDENCE/phase9_three_candidate_users_registry.txt`

## 9. Final Truth

After BA.3 stop and policy revert:

- truth-check: PASS
- convergence: PASS
- runtime action safe: true
- production remains aligned to `989b5c700591aaf332cc17a981d11c07cb1de5c5`

Evidence:

- `STABILITY1_CLOSE_EVIDENCE/phase9_truth_after_ba3_block_policy_revert.json`
- `STABILITY1_CLOSE_EVIDENCE/phase9_convergence_after_ba3_block_policy_revert.json`

## 10. Final Certification

Final verdict: `FIVE_USER_AUTONOMY_BLOCKED`

Final verdicts:

- stability1_deployed=true
- production_verified=true
- truth_pass=true
- convergence_pass=true
- runtime_action_safe=true
- ba3_planned_limit_raised=true
- fresh_planner_generated=true
- five_real_candidates_available=false
- planner_candidate_moves_total=3
- packet_created=false
- restore_barrier_created=false
- apply_executed=false
- users_moved=0
- feedback_materialized=false
- trust_updated=false
- prediction_updated=false
- recommendation_updated=false
- policy_reverted_to_2=true

Single blocker:

`insufficient_real_planner_candidates_3_of_5`

Safe next step:

`wait_or_restore_candidate_pool_until_fresh_planner_has_at_least_5_real_moves_then_rerun_BA3`

Do not retry BA.3 execution until a fresh planner produces at least 5 real planner-selected users.
