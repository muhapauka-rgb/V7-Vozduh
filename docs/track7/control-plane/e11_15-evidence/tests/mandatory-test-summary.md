# E11.15 Mandatory Test Summary

## Full Suite

`tools/v7-run-tests`

Result: PASS

```text
Ran 89 tests in 6.827s
OK
py_compile ok
```

## Targeted Unit Tests

Command:

```text
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_v7_egress_diagnose tests.unit.test_v7_restore_settle_gate tests.unit.test_v7_second_canary_target_readiness
```

Result: PASS

```text
Ran 40 tests in 3.461s
OK
```

Coverage mapping:

- targeted reservation enforcement tests: PASS
- targeted diagnose tests: PASS
- targeted autoswitch policy tests: PASS
- restore barrier tests: PASS
- restore settle gate tests: PASS
- target readiness tests: PASS
- delayed movement regression tests: PASS via restore-barrier failover suppression tests and E11.15 live rehearsal evidence
- planner/apply timing tests: PASS via restore-settle tests and E11.15 apply-timer rehearsal evidence
- governance checker tests: PASS via `tools/v7-control-plane-governance-check --pretty`

## Governance Tools

`tools/v7-control-plane-governance-check --pretty`

Result: PASS

Key output:

```text
current_canary_status=E11_15_APPLY_RESTORE_BARRIER_CONDITIONAL_FINAL_HELD
e11_15_apply_restore_barrier_rehearsal_complete=True
e11_15_barrier_rehearsal_executed=True
e11_15_apply_timer_restored=True
e11_15_apply_timer_final_state=held
e11_15_user_movement_observed=False
e11_15_delayed_non_cohort_movement_prevented=True
e11_15_barrier_consumed_by_apply=True
e11_15_selected_moves_during_rehearsal=0
e11_15_barrier_ttl_status=ACTIVE_NOT_EXPIRED_NOT_OBSERVED_POST_TTL
e11_15_runtime_checks_ok=True
e11_15_regressions_observed=False
e11_15_mini_cohort_readiness_after=CONDITIONAL
e11_15_larger_cohort_readiness_after=NO-GO
execution_allowed_now=False
```

## Target Readiness

`tools/v7-second-canary-target-readiness --pretty`

Result: PASS

```text
selected_target=wireguard-1779454504-c43409
approval_status=GO
second_canary_readiness=GO
execution_allowed_now=False
```

`tools/v7-second-canary-target-readiness --json`

Result: PASS

```text
selected_target=wireguard-1779454504-c43409
approval_status=GO
second_canary_readiness=GO
```

## Restore-Settle Gate

`tools/v7-restore-settle-gate --pre-restore --pretty`

Result: PASS

```text
gate_status=GO
selected_moves_by_sample=[0, 0, 0]
registry_stable=True
checkers_ok=True
hidden_movers_observed=False
execution_allowed_now=False
```

`tools/v7-restore-settle-gate --pre-restore --json`

Result: PASS

```text
"gate_status": "GO"
"selected_moves_by_sample": [0, 0, 0]
"registry_stable": true
"checkers_ok": true
```

## Runtime / Lineage

`tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty`

Result: PASS with known governance warnings:

```text
Runtime governance: partial
Named lineage gaps: 55
Critical lineage gaps (known): 32
Unlisted lineage gaps: 0
warnings:
  - runtime_manifest_not_supplied
```

`tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty`

Result: PASS with known lineage/dirty-worktree warnings:

```text
runtime_lineage=partial
release_provenance=incomplete
release_object=releases/v7-runtime-20260523T174503Z ready=True missing=0
warnings:
  - runtime_manifest_missing_locally_or_not_supplied
  - source_worktree_dirty
  - known_43_production_only_tools_require_lineage
  - archive_manifest_missing_locally_or_not_supplied
```

## Static Checks

Python compile:

```text
PYTHONPYCACHEPREFIX=/private/tmp/v7-pycache-e11-15 python3 -m py_compile tools/v7-control-plane-governance-check tools/v7-users-autoswitch tools/v7-restore-settle-gate tools/v7-second-canary-target-readiness
```

Result: PASS

Shell syntax:

```text
bash -n tools/v7-run-tests
bash -n tools/v7-egress-diagnose
```

Result: PASS

Note: `tools/v7-egress-diagnose` is a shell script, so it is intentionally validated with `bash -n`, not `py_compile`.

`git diff --check`

Result: PASS
