# L3 Pre-Restore Selected Move Continuity Fix

## Summary

After the persisted failed-source cooldown continuation fix, Phase 4 MEDIUM_BATCH certification progressed to the next breakpoint:

- Wake: `ACCEPT_WAKE`
- Planner candidate/proposal moves: `25`
- Authority-bounded selected moves before emergency gate: `10`
- transition status: `BLOCKED`
- transition error: `l3_validation_selected_move_count_above_max_users`
- transition selected_move_count: `25`

The certification target was `--max-users 10`, so the transition should have consumed the bounded 10-move selection, not all 25 affected user decisions.

## Root Cause

Owners:

- producer: `tools/v7-users-autoswitch`
- consumer: `admin_core/operator_execution.selected_moves_from_plan`
- transition owner: `admin_core/operator_execution_pipeline.py`

The Planner preserved only the count:

- `safety.selected_moves_diagnostics.selected_moves_before_restore_barrier = 10`

It did not persist the actual bounded pre-restore selected move rows. When final `plan.selected_moves` was empty because Restore Barrier approval had not yet been materialized, `operator_execution.selected_moves_from_plan()` fell back to all switch `decisions`, which contained 25 affected users. The transition then correctly blocked because 25 exceeded `--max-users 10`.

## Correction

Planner now persists:

- `safety.selected_moves_diagnostics.selected_moves_before_restore_barrier_rows`

Operator execution now consumes selected moves in this order:

1. final `plan.selected_moves`;
2. `restore_barrier.approved_candidate_moves_before_guard`;
3. `safety.selected_moves_diagnostics.selected_moves_before_restore_barrier_rows`;
4. broad `decisions` fallback only when no bounded selected object exists.

This preserves the exact bounded move object across:

Planner selection
-> governed transition
-> packet materialization
-> approved plan lock
-> restore barrier
-> Runtime Apply

## Changed Files

- `tools/v7-users-autoswitch`
- `admin_core/operator_execution.py`
- `tests/unit/test_operator_execution_packet.py`

## Tests

Targeted:

```text
python3 -m unittest \
  tests.unit.test_operator_execution_packet.OperatorExecutionPacketTest.test_packet_from_plan_uses_diagnostic_pre_restore_rows_before_decision_fallback \
  tests.unit.test_operator_execution_packet.OperatorExecutionPacketTest.test_packet_from_plan_uses_pre_barrier_selected_moves_when_final_selected_suppressed \
  tests.unit.test_operator_execution_packet.OperatorExecutionPacketTest.test_packet_from_plan_prefers_final_selected_moves_over_decisions \
  tests.unit.test_v7_users_autoswitch_policy.V7UsersAutoswitchPolicyTest.test_active_l3_failed_source_incident_cooldown_does_not_trap_affected_user

OK
```

Affected suites:

```text
python3 -m unittest \
  tests.unit.test_v7_users_autoswitch_policy \
  tests.unit.test_operator_execution_packet \
  tests.unit.test_governed_canary_cli \
  tests.unit.test_operator_execution_pipeline

Ran 240 tests in 10.681s
OK
```

Compile:

```text
PYTHONPYCACHEPREFIX=/tmp/v7_pycache python3 -m py_compile \
  tools/v7-users-autoswitch \
  admin_core/operator_execution.py \
  tests/unit/test_v7_users_autoswitch_policy.py \
  tests/unit/test_operator_execution_packet.py

OK
```

## Current Phase Position

Current Phase: Phase 4 MEDIUM_BATCH certification

Interrupted breakpoint resolved: governed transition consumed broad decisions instead of bounded pre-restore selected moves.

Next step: deploy through the standard safe deployment path and resume the same Phase 4 certification run with `--max-users 10`.

## Automation Debt

No new automation debt created. The existing manual certification workflow remains an execution-program workflow candidate for future consolidation.

## Workflow Debt

The repeated cycle of production breakpoint -> owner resolution -> patch -> tests -> deploy -> resume remains Workflow Debt until the certification program earns a governed pipeline for this process.
