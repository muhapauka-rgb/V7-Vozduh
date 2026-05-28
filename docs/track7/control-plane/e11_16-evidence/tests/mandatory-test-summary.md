# E11.16 Mandatory Test Summary

## Full Suite

`tools/v7-run-tests`

Result: PASS

```text
Ran 90 tests in 7.196s
OK
py_compile ok
```

## Targeted Tests

```text
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_v7_egress_diagnose tests.unit.test_v7_restore_settle_gate tests.unit.test_v7_second_canary_target_readiness
```

Result: PASS

```text
Ran 41 tests in 3.561s
OK
```

Coverage:

- reservation enforcement tests: PASS
- diagnose tests: PASS
- autoswitch policy tests: PASS
- restore barrier tests: PASS
- restore-settle tests: PASS
- target-readiness tests: PASS
- planner/apply generation tests: PASS via post-TTL fail-closed tests
- delayed movement regression tests: PASS via expired-barrier fail-closed simulation
- governance checker tests: PASS

## Governance Tools

`tools/v7-control-plane-governance-check --pretty`

Result: PASS

Key output:

```text
e11_16_post_ttl_generation_governance_complete=True
e11_16_post_ttl_behavior_safe=True
e11_16_barrier_expiry_safe=True
e11_16_delayed_movement_after_ttl_observed=False
e11_16_generation_governance_required=True
e11_16_generation_fix_executed=True
e11_16_apply_timer_final_state=held
e11_16_runtime_checks_ok=True
e11_16_regressions_observed=False
e11_16_mini_cohort_readiness_after=CONDITIONAL
e11_16_larger_cohort_readiness_after=NO-GO
e11_16_unattended_apply_lifecycle_status=CONDITIONAL_WITH_GENERATION_GOVERNANCE
e11_16_pre_fix_selected_moves=3
e11_16_post_fix_selected_moves=0
execution_allowed_now=False
```

## Readiness / Settle

- `tools/v7-second-canary-target-readiness --pretty`: PASS, target readiness `GO`.
- `tools/v7-second-canary-target-readiness --json`: PASS, target readiness `GO`.
- `tools/v7-restore-settle-gate --pre-restore --pretty`: PASS, gate `GO`.
- `tools/v7-restore-settle-gate --pre-restore --json`: PASS, gate `GO`.

## Runtime / Lineage

- `tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty`: PASS with known partial-governance warnings.
- `tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty`: PASS with known lineage/dirty-worktree warnings.

## Static Checks

- Python `py_compile`: PASS.
- `bash -n tools/v7-run-tests tools/v7-egress-diagnose`: PASS.
- `git diff --check`: PASS.
