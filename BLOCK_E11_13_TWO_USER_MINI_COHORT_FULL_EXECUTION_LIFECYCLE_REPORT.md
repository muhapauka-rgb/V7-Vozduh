# BLOCK E11.13 - Two-User Mini-Cohort Full Execution Lifecycle

block=E11.13
mode=LARGE_BOUNDED_LIVE_MINI_COHORT_EXECUTION
execution_allowed_now=false

## Executive Verdict

mini_cohort_executed=true
mini_cohort_aborted=false
moved_users=10.7.0.11,10.7.0.12
rollback_executed=true
rollback_targets=1,1
only_approved_users_moved=false
wireguard_users_after=0
reservation_enforced_after=true
delayed_movements_observed=true
restore_settle_gate_status=GO
runtime_checks_ok=true
target_readiness_after=GO
mini_cohort_lifecycle_status=EXECUTED_ROLLED_BACK_DELAYED_APPLY_MOVEMENT_OBSERVED_CONTAINED
next_stage_readiness=NO_GO_FOR_LARGER_COHORT_APPLY_RESTORE_ROOT_CAUSE_REQUIRED
recommended_next_block=E11.14_DELAYED_APPLY_RESTORE_MOVEMENT_ROOT_CAUSE_AND_APPLY_TIMER_GOVERNANCE_FIX

E11.13 successfully executed the approved two-user cohort and cleanly rolled
both approved users back. The cohort itself stayed within the WireGuard hard
limit and showed no WireGuard route/checker regression.

The lifecycle is not promotion-clean: after the restore-settle gate passed and
the apply timer was restored, autoswitch moved three non-cohort users:

```text
10.7.0.9   1 -> awg0  2026-05-27T10:18:25Z
10.7.0.10  1 -> awg0  2026-05-27T10:18:27Z
10.7.0.13  1 -> awg0  2026-05-27T10:18:29Z
```

No manual autoswitch apply was run. Because this was unapproved non-cohort
movement after apply restore, apply was held again as emergency containment.

## Phase Summary

### Phase 0 - Fresh Prechecks

Evidence:

- `docs/track7/control-plane/e11_13-evidence/prechecks.txt`
- `docs/track7/control-plane/e11_13-evidence/precheck-samples/`
- `docs/track7/control-plane/e11_13-evidence/precheck-target-readiness-user1.json`
- `docs/track7/control-plane/e11_13-evidence/precheck-target-readiness-user2.json`
- `docs/track7/control-plane/e11_13-evidence/precheck-restore-settle.json`

```text
wireguard_users=0
target_readiness_user1=GO
target_readiness_user2=GO
restore_settle_gate_status=GO
selected_moves_by_sample=[0,0,0]
runtime_checks_ok=true
hidden_movers_observed=false
candidates_current=1,1
```

Prechecks passed.

### Phase 1 - Hold Governance Window

Evidence: `docs/track7/control-plane/e11_13-evidence/hold-verification.txt`

```text
v7-health.service=active
v7-autoswitch-planner.timer=inactive
v7-autoswitch-planner.service=inactive
v7-users-autoswitch.timer=inactive
v7-users-autoswitch.service=inactive
selected_moves=0
hidden_movers_observed=false
runtime_checks_ok=true
```

The governance hold succeeded.

### Phase 2 - Move User 1

Evidence: `docs/track7/control-plane/e11_13-evidence/user1-verification.txt`

```text
command=v7-user-switch 10.7.0.11 wireguard-1779454504-c43409
only_user1_changed=true
10.7.0.11_current=wireguard-1779454504-c43409
wireguard_users=1
selected_moves=0
hidden_movers_observed=false
runtime_checks_ok=true
```

### Phase 3 - Move User 2

Evidence: `docs/track7/control-plane/e11_13-evidence/user2-verification.txt`

```text
command=v7-user-switch 10.7.0.12 wireguard-1779454504-c43409
only_user2_changed=true
10.7.0.11_current=wireguard-1779454504-c43409
10.7.0.12_current=wireguard-1779454504-c43409
registry_wireguard_users=2
hard_limit_exceeded=false
selected_moves=0
runtime_checks_ok=true
```

### Phase 4 - Observation Window

Evidence:

- `docs/track7/control-plane/e11_13-evidence/observation-A.txt`
- `docs/track7/control-plane/e11_13-evidence/observation-B.txt`
- `docs/track7/control-plane/e11_13-evidence/observation-C.txt`

```text
wireguard_users_by_sample=2,2,2
selected_moves_by_sample=0,0,0
users_registry_stable=true
hidden_movers_observed=false
runtime_checks_ok=true
candidate_routes_wireguard=true
```

The two-user WireGuard observation window was clean.

### Phase 5 - Rollback

Evidence: `docs/track7/control-plane/e11_13-evidence/rollback-verification.txt`

```text
rollback_decision=default
command=v7-user-switch 10.7.0.11 1
command=v7-user-switch 10.7.0.12 1
only_approved_users_changed=true
10.7.0.11_current=1
10.7.0.12_current=1
registry_wireguard_users=0
selected_moves=0
runtime_checks_ok=true
```

Rollback was clean.

### Phase 6 - Staged Restore

Evidence:

- `docs/track7/control-plane/e11_13-evidence/planner-restore.txt`
- `docs/track7/control-plane/e11_13-evidence/restore-settle.txt`
- `docs/track7/control-plane/e11_13-evidence/restore-settle.json`
- `docs/track7/control-plane/e11_13-evidence/apply-restore.txt`

```text
planner_restore_only=true
restore_settle_gate_status=GO
selected_moves_by_sample=[0,0,0]
registry_stable=true
checkers_ok=true
hidden_movers_observed=false
apply_timer_restored_after_gate_GO=true
manual_autoswitch_apply=false
```

### Phase 7 - Delayed Monitoring

Evidence:

- `docs/track7/control-plane/e11_13-evidence/delayed-monitoring-A.txt`
- `docs/track7/control-plane/e11_13-evidence/delayed-monitoring-B.txt`
- `docs/track7/control-plane/e11_13-evidence/delayed-monitoring-C.txt`
- `docs/track7/control-plane/e11_13-evidence/delayed-movement-classification.txt`
- `docs/track7/control-plane/e11_13-evidence/emergency-containment-apply-held.txt`
- `docs/track7/control-plane/e11_13-evidence/final-state-after-containment.txt`

Delayed monitoring found a non-clean post-apply lifecycle:

```text
wireguard_users_after=0
cohort_users_after=1,1
selected_moves_after=0
runtime_checks_ok=true
hidden_movers_observed=false
delayed_non_cohort_movements=10.7.0.9,10.7.0.10,10.7.0.13
delayed_movement_route=1->awg0
apply_timer_reheld_for_containment=true
```

The reserved WireGuard target remained clean, but the apply restore lifecycle
still produced delayed non-cohort movement. This blocks promotion.

## Final Answers

## Verification Matrix

```text
tools/v7-run-tests=PASS
targeted_reservation_enforcement_tests=PASS
targeted_diagnose_tests=PASS
targeted_autoswitch_policy_tests=PASS
restore_settle_gate_tests=PASS
target_readiness_tests=PASS
mini_cohort_lifecycle_tests=PASS
planner_apply_timing_tests=PASS
governance_checker_tests=PASS
tools/v7-control-plane-governance-check --pretty=PASS
tools/v7-second-canary-target-readiness --pretty=PASS
tools/v7-second-canary-target-readiness --json=PASS
tools/v7-restore-settle-gate --pre-restore --pretty=PASS
tools/v7-restore-settle-gate --pre-restore --json=PASS
tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty=PASS_WITH_EXISTING_WARNINGS
tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty=PASS_WITH_EXISTING_WARNINGS
py_compile=PASS
bash -n relevant shell scripts=PASS
git diff --check=PASS
```

Known warnings are existing repo/runtime lineage warnings, not E11.13 execution
blockers: `runtime_manifest_not_supplied`, dirty source worktree, production-only
lineage gaps, and missing local archive manifest.

```text
mini_cohort_executed=true
mini_cohort_aborted=false
moved_users=10.7.0.11,10.7.0.12
rollback_executed=true
rollback_targets=1,1
only_approved_users_moved=false
wireguard_users_after=0
reservation_enforced_after=true
delayed_movements_observed=true
restore_settle_gate_status=GO
runtime_checks_ok=true
target_readiness_after=GO
mini_cohort_lifecycle_status=EXECUTED_ROLLED_BACK_DELAYED_APPLY_MOVEMENT_OBSERVED_CONTAINED
next_stage_readiness=NO_GO_FOR_LARGER_COHORT_APPLY_RESTORE_ROOT_CAUSE_REQUIRED
recommended_next_block=E11.14_DELAYED_APPLY_RESTORE_MOVEMENT_ROOT_CAUSE_AND_APPLY_TIMER_GOVERNANCE_FIX
execution_allowed_now=false
```

## Final Mutation Statement

Runtime mutation performed: YES
Runtime mutation scope: planner/apply hold, approved two-user movement, approved rollback, planner restore, apply timer restore, emergency apply hold containment
User movement performed by this block: YES
User movement scope: manual movement only for approved users `10.7.0.11`, `10.7.0.12`; delayed autoswitch moved non-cohort users `10.7.0.9`, `10.7.0.10`, `10.7.0.13` after apply restore
Routing mutation performed by this block: YES
Routing mutation scope: approved users during manual movement and rollback; delayed autoswitch route changes observed for non-cohort users after apply restore
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
