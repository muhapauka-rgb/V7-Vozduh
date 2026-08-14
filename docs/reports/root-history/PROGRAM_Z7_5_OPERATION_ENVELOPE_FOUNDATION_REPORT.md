# PROGRAM Z7.5 - Operation Envelope Foundation Report

Project: V7 Vozduh  
Branch target: v7-next  
Date: 2026-06-02  
Mode: first bounded implementation block  

## Executive Verdict

Z7.5 added the operation envelope foundation to `tools/v7-users-autoswitch` as a strictly additive output-only lineage extension.

No scheduler, systemd, routing, user movement, planner selection, restore barrier, runtime state writer, audit writer, closure, rollback, or execution behavior was changed.

## Gate 0 Result

Re-inventory confirmed:

| Area | Existing Owner | Z7.5 Classification |
|---|---|---|
| autoswitch root output | `tools/v7-users-autoswitch` | EXTEND |
| planner generation id | existing `self.generation["planner_generation_id"]` | REUSE |
| selected move hash | existing `_selected_moves_hash()` | REUSE |
| selected move count | existing final selected move list / `summary.selected_moves` | REUSE |
| selected move calculation | `plan()` existing selection logic | DO NOT TOUCH |
| restore barrier logic | `plan()` restore barrier section | DO NOT TOUCH |
| apply behavior | `apply(plan)` | DO NOT TOUCH |
| audit sink | `tools/runtime-support/v7-audit-log` | DO NOT TOUCH |
| closure store | Admin closure model | DO NOT TOUCH |
| scheduler | `systemd/v7-users-autoswitch.*` | DO NOT TOUCH |
| tests | `tests/unit/test_v7_users_autoswitch_policy.py` | EXTEND |

No hidden consumer or schema risk was found that required stopping implementation. Z7.4 boundaries remained valid.

## Changed Files

1. `tools/v7-users-autoswitch`
2. `tests/unit/test_v7_users_autoswitch_policy.py`
3. `PROGRAM_Z7_5_OPERATION_ENVELOPE_FOUNDATION_REPORT.md`

## Implementation Summary

`tools/v7-users-autoswitch` now adds an additive root `operation` object to plan output:

```json
{
  "operation": {
    "operation_owner": "tools/v7-users-autoswitch",
    "operation_type": "runtime_autoswitch",
    "operation_started_at": "...",
    "planner_generation_id": "...",
    "selected_move_hash": "...",
    "selected_move_count": 0,
    "operation_id": "runtime_autoswitch_..."
  }
}
```

Implementation details:

- `operation_started_at` is captured when `AutoswitchPlanner` is created.
- `planner_generation_id` reuses the existing planner generation hash.
- `selected_move_hash` reuses `_selected_moves_hash()` and is computed from the final selected move list after restore-barrier guards.
- `selected_move_count` is derived from the final selected move list.
- `operation_id` is derived from the operation context payload using existing `sha256_json()`.
- Existing root fields remain in place.
- Existing `selected_moves`, `summary`, `safety`, `decisions`, and `apply_result` contracts are unchanged.

## Test Updates

`tests/unit/test_v7_users_autoswitch_policy.py` now verifies:

- no-op output contains operation envelope,
- selected-move output contains operation envelope,
- operation id exists,
- planner generation reference matches `plan["safety"]["generation"]["planner_generation_id"]`,
- selected move hash matches the existing selected-move hash algorithm,
- selected move count matches both `len(plan["selected_moves"])` and `plan["summary"]["selected_moves"]`,
- existing root fields remain present.

## Validation

Command:

```text
python3 -m unittest tests/unit/test_v7_users_autoswitch_policy.py
```

Result:

```text
Ran 21 tests in 0.170s
OK
```

## Risk Assessment

| Risk | Status |
|---|---|
| output schema break | LOW; root contract is additive |
| selected move behavior change | LOW; selection logic untouched |
| restore barrier behavior change | LOW; guard logic untouched |
| runtime state mutation risk | LOW; no new state file writer |
| audit duplication risk | LOW; audit sink untouched |
| closure duplication risk | LOW; closure untouched |
| operation identity duplication risk | LOW/MEDIUM; scoped with `operation_type=runtime_autoswitch` and owner |
| consumer compatibility risk | LOW; existing fields remain unchanged |

## Truth Source Audit

```text
duplicate_operation_truth=false
duplicate_runtime_truth=false
duplicate_lineage_truth=false
duplicate_audit_truth=false
duplicate_closure_truth=false
```

## Success Criteria

```text
operation_envelope_exists=true
operation_id_exists=true
planner_generation_reference_exists=true
selected_move_hash_reference_exists=true
selected_move_count_reference_exists=true
existing_output_schema_preserved=true
existing_selected_move_logic_unchanged=true
existing_restore_barrier_behavior_unchanged=true
targeted_tests_pass=true
new_truth_source_created=false
safe_to_continue_to_Z7_6=true
```

## Safety Statement

Z7.5 performed no deploy, no autoswitch apply, no user movement, no routing mutation, no runtime mutation, no service restart, no systemd modification, no timer modification, no cleanup, no deletion, no merge, and no force push.
