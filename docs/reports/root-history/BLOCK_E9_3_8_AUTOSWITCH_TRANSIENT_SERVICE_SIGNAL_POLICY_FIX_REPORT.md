# BLOCK E9.3.8 - Autoswitch Transient Service Signal Policy Fix Report

Mode: bounded repo-side policy fix.
Runtime deploy: no.
Live autoswitch apply: forbidden.
Apply timer restore: forbidden.
Canary: forbidden.

## Scope

E9.3.8 implemented the E9.3.7 policy design in repo source only:

```text
tools/v7-users-autoswitch
```

Runtime path was identified as:

```text
/usr/local/bin/v7-users-autoswitch
```

The runtime file was not modified.

## Repo Policy Fix

Implemented:

- `DEFAULT_SERVICE_SIGNAL_POLICY`
- `AutoswitchPlanner._service_signal_policy`
- single non-Telegram service failure becomes `service_signal_DEGRADED_SERVICE`
- persistent failure becomes conditional ineligibility
- multiple critical service failures become conditional ineligibility
- Telegram degraded without hard block remains non-hard
- Telegram hard block remains hard
- disabled/maintenance/quarantine egress remains hard
- restore-stage service-signal failover requires explicit `apply_restore_approved`
- restore-stage failover is bounded by `max_failover_per_restore_stage`

## Required Semantics After Fix

```text
Instagram one-sample fail => DEGRADED_SERVICE, selected_moves=0
Instagram persistent fail => selected_moves>0 allowed
Telegram degraded not hard-blocked => selected_moves=0
Telegram hard-blocked => failover allowed
Egress disabled => failover allowed
Multiple critical services failed => failover allowed
Restore stage without approval => selected_moves=0
Restore stage with approval => selected_moves bounded by max_failover_per_restore_stage
```

## Tests

Added repo-side tests:

```text
tests/unit/test_v7_users_autoswitch_policy.py
```

Existing design-contract tests remain:

```text
tests/unit/test_v7_autoswitch_policy_design.py
```

Targeted result:

```text
python3 -m unittest tests.unit.test_v7_users_autoswitch_policy tests.unit.test_v7_autoswitch_policy_design
Ran 15 tests
OK
```

Full result:

```text
tools/v7-run-tests: OK
```

## Dry-Run Result

Fixture planner tests prove:

```text
selected_moves_for_single_instagram_failure_after_fix=0
candidate_moves_total_for_single_instagram_failure_after_fix=0
```

Live current-state planner dry-run was not executed because `v7-users-autoswitch` planner mode can write load/reconnect state even without `--apply`. That should happen only after runtime deploy approval.

## Runtime Deploy Readiness

Runtime deploy is ready for a separate approval packet, but not performed:

```text
runtime_policy_deployed=false
code_fix_ready_for_runtime_deploy=true
apply_timer_should_remain_held=true
planner_dry_run_required_after_deploy=true
```

## Verification

```text
tools/v7-run-tests: OK, 64 tests
targeted autoswitch policy tests: OK, 15 tests
tools/v7-control-plane-governance-check --pretty: OK
tools/v7-second-canary-target-readiness --pretty: OK, second_canary_readiness=NO-GO
tools/v7-second-canary-target-readiness --json: OK, mutation=false
tools/v7-runtime-repo-diff --runtime-enumeration runtime-enumeration.json --pretty: OK, runtime_governance=partial
tools/v7-release-lineage-check --release-dir releases/v7-runtime-20260523T174503Z --pretty: OK, release_object ready, provenance incomplete
py_compile admin/tools/governance/autoswitch: OK
git diff --check: OK
```

Expected governance warnings remain:

```text
runtime_manifest_not_supplied
source_worktree_dirty
release_provenance=incomplete
known production-only lineage gaps remain outside E9.3.8 scope
```

## Governance Result

```text
repo_policy_fix_implemented=true
runtime_policy_deployed=false
code_fix_ready_for_runtime_deploy=true
selected_moves_for_single_instagram_failure_after_fix=0
apply_restore_safe_after_repo_fix=false_until_runtime_deploy_and_post_deploy_planner_proof
apply_timer_should_remain_held=true
execution_allowed_now=false
```

## Next Recommended Step

Prepare a separate bounded runtime deploy approval for `/usr/local/bin/v7-users-autoswitch` only. Keep `v7-users-autoswitch.timer` held. After deploy, run a planner-only dry-run and verify that the E9.3.5 failure class no longer produces broad selected moves.

## Final Mutation Statement

```text
Runtime mutation performed: NO
User movement performed: NO
Routing mutation performed: NO
Kill switch mutation performed: NO
Autoswitch apply performed manually: NO
Autoswitch apply timer restored: NO
Canary performed: NO
```
