# BLOCK E11.12 - Two-User Mini-Cohort Approval Packet

block=E11.12
mode=LARGE_READ_ONLY_MINI_COHORT_GOVERNANCE_PACKET
live_mutation=forbidden
mini_cohort_execution=forbidden
user_movement=forbidden
routing_mutation=forbidden
execution_allowed_now=false

## Executive Verdict

mini_cohort_readiness=CONDITIONAL
approval_status=CONDITIONAL
recommended_next_block=E11.13_TWO_USER_MINI_COHORT_EXECUTION_PACKET_WITH_FRESH_PRECHECKS

E11.12 approves a future first mini-cohort packet shape, not execution. The
approval is conditional because the selected WireGuard target can hold exactly
two users by hard limit, and fresh runtime drift occurred during evidence
collection before the final settle samples stabilized. Any future execution
must re-run the full pre-check set against fresh live state.

## Fresh Runtime Truth

Evidence:

- `docs/track7/control-plane/e11_12-evidence/current-runtime-snapshot.txt`
- `docs/track7/control-plane/e11_12-evidence/current-state/`
- `docs/track7/control-plane/e11_12-evidence/current-target-readiness.json`
- `docs/track7/control-plane/e11_12-evidence/current-target-readiness-candidate-2.json`
- `docs/track7/control-plane/e11_12-evidence/current-restore-settle-gate.json`

```text
users.registry_sha256=27e42d79bd073b7ad4934814958ab9301d46f4b730074fe9cc3f9b3d70410be7
egress.registry_sha256=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8
wireguard_reserved=true
wireguard_users=0
target_readiness=GO
restore_settle_gate_status=GO
selected_moves=0
runtime_checks_ok=true
hidden_movers_observed=false
```

The initial E11.12 snapshot saw runtime state before a fresh autoswitch drift.
Corrected restore-settle samples then proved the final state stable across
three samples and more than two apply timer intervals:

```text
selected_moves_by_sample=[0, 0, 0]
registry_stable=true
egress_registry_stable=true
checkers_ok=true
hidden_movers_observed=false
wireguard_users_by_sample=0,0,0
```

## Selected Cohort

selected_candidates=10.7.0.11,10.7.0.12
selected_target=wireguard-1779454504-c43409
rollback_targets=1,1
blast_radius=2_users_max

| User | Current egress | Table | Rollback target | Current route |
| --- | --- | --- | --- | --- |
| `10.7.0.11` | `1` | `1009` | `1` | `default dev v7e356a192b79` |
| `10.7.0.12` | `1` | `1010` | `1` | `default dev v7e356a192b79` |

Both candidates are enabled, have `switches_1h=0`, and do not have WireGuard in
their recent `last_targets`. Candidates `10.7.0.13`, `10.7.0.14`, and
`10.7.0.15` were rejected despite `switches_1h=0` because their recent history
includes the reserved WireGuard target.

## Target Capacity

target_capacity_safe=true
capacity_safe_scope=exactly_two_users
three_user_cohort_allowed=false

```text
wireguard_users_before=0
wireguard_soft_limit=1
wireguard_hard_limit=2
wireguard_users_after_expected=2
hard_limit_exceeded=false
```

The second user reaches the hard limit. Any third user is prohibited.

## Preview Only

Forward preview:

```text
v7-user-switch 10.7.0.11 wireguard-1779454504-c43409
v7-user-switch 10.7.0.12 wireguard-1779454504-c43409
```

Rollback preview:

```text
v7-user-switch 10.7.0.11 1
v7-user-switch 10.7.0.12 1
```

No command above was executed by E11.12.

## Required Future Gates

Before any E11.13 execution:

1. Verify WireGuard users remain `0`.
2. Verify both selected users still have `current=1` and tables `1009`/`1010`.
3. Verify target readiness remains `GO`.
4. Verify restore-settle gate remains `GO`.
5. Verify selected moves remain `0`.
6. Verify all runtime checkers OK.
7. Verify hidden movers absent.
8. Hold planner/apply before movement.
9. Move users sequentially, with verification after each move.
10. Default final decision remains rollback unless keep is separately proven safer.

## Verification Matrix

```text
tools/v7-run-tests=PASS
targeted_reservation_enforcement_tests=PASS
targeted_diagnose_tests=PASS
targeted_autoswitch_policy_tests=PASS
restore_settle_gate_tests=PASS
target_readiness_tests=PASS
mini_cohort_planning_tests=PASS
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

Known warnings are not E11.12 blockers: `runtime_manifest_not_supplied`,
`source_worktree_dirty`, known production-only lineage gaps, and missing local
archive manifest.

## Required Answers

```text
mini_cohort_readiness=CONDITIONAL
selected_candidates=10.7.0.11,10.7.0.12
selected_target=wireguard-1779454504-c43409
target_capacity_safe=true
restore_settle_gate_status=GO
rollback_feasible=true
blast_radius=2_users_max
approval_status=CONDITIONAL
execution_allowed_now=false
recommended_next_block=E11.13_TWO_USER_MINI_COHORT_EXECUTION_PACKET_WITH_FRESH_PRECHECKS
```

## Final Mutation Statement

Runtime mutation performed: NO
User movement performed by this block: NO
Routing mutation performed by this block: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Canary performed: NO
