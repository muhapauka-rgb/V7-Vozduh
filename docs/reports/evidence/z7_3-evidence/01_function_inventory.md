# Z7.3 Evidence 01 - Function Inventory

## `tools/v7-users-autoswitch`

| Function / Area | Current Purpose | Reuse Suitability | Extension Suitability | Risk | Planned Class |
|---|---|---|---|---|---|
| `now_iso()` | Timestamp helper | HIGH | Use for operation start/end timestamps | LOW | REUSE |
| `sha256_json(payload)` | Deterministic hash helper | HIGH | Use for operation id or runtime snapshot hash | LOW | REUSE |
| `AutoswitchPlanner.__init__` | Loads runtime state, restore barrier, generation, users, egress, policy | HIGH | Add operation context after generation load | MEDIUM | LINEAGE EXTENSION |
| `_generation_status()` | Computes `planner_generation_id` from runtime inputs | HIGH | Reuse as operation lineage input | LOW | REUSE |
| `_restore_barrier_status()` | Reads restore barrier and clearance metadata | HIGH | Reuse as operation lineage reference | LOW | REUSE |
| `plan()` | Builds decisions, selected moves, summary, safety and JSON plan | HIGH | Add `operation` envelope and expose selected move hash | MEDIUM | METADATA/LINEAGE EXTENSION |
| `_selected_moves_hash(selected)` | Computes selected move hash | HIGH | Promote to operation envelope field | LOW | REUSE |
| `_restore_clearance_generation_check(...)` | Checks generation/token/hash/count clearance | HIGH | Reference result in operation restore-barrier lineage | LOW | REUSE |
| `apply(plan)` | Handles dry-run/no-op/disabled/observe/apply execution result | HIGH | Add terminal state/reason and operation references in result rows | MEDIUM | LINEAGE EXTENSION |
| `_run_switch(ip, egress, reason)` | Calls movement primitive | HIGH | Pass operation id only as env/metadata if needed; avoid command signature change | MEDIUM | OPTIONAL EXTEND |
| `_verify_routes()` | Calls route verification | HIGH | Reference verification result under operation lineage | LOW | REUSE |
| `_update_safety_after_apply(results)` | Writes safety/anti-flap state after successful results | HIGH | No operation wiring needed | MEDIUM if touched | NO CHANGE |
| `main()` | Runs plan/apply and prints JSON | HIGH | Ensure final operation terminal/audit refs are present before print | MEDIUM | LINEAGE EXTENSION |

Potential new helper functions inside same file:

| Helper | Purpose | Risk | Note |
|---|---|---|---|
| `_operation_id(...)` or `_build_operation_context(...)` | Create deterministic/unique operation identity from existing facts | LOW/MEDIUM | New helper in existing owner, not a new truth source |
| `_runtime_snapshot_hash(...)` | Hash relevant runtime facts for operation lineage | LOW/MEDIUM | Reuse `sha256_json` |
| `_terminal_state(plan, apply_result)` | Normalize terminal state/reason | LOW | Avoid scattering state logic |
| `_audit_runtime_operation(operation, action)` | Invoke existing `v7-audit-log` with metadata | MEDIUM | Must not run in read-only dry-run unless explicitly chosen |

## `tools/runtime-support/v7-audit-log`

| Function / Area | Current Purpose | Planned Class | Reason |
|---|---|---|---|
| `parse_metadata(args)` | Accepts arbitrary metadata key=value args | NO CHANGE | Enough to carry operation lineage |
| `env_or_meta(...)` | Promotes known metadata/env to top-level audit fields | NO CHANGE | Already supports `request_id`, `object_type`, `object_id`, hashes |
| event JSON writer | Appends canonical audit event | NO CHANGE | No new audit sink needed |

## `admin/v7-admin-api`

| Function / Area | Current Purpose | Planned Class | Risk |
|---|---|---|---|
| `autoswitch_plan_state(...)` | Calls autoswitch dry-run and returns JSON plan | OPTIONAL METADATA EXTENSION | LOW |
| `autoswitch_dry_run_state(...)` | Calls autoswitch dry-run and Admin-audits wrapper action | OPTIONAL METADATA EXTENSION | LOW/MEDIUM |
| `autoswitch_apply_guarded(...)` | Calls autoswitch apply and Admin-audits wrapper action | OPTIONAL METADATA EXTENSION | MEDIUM |
| `closure_set_response(...)` | Existing closure writer for `runtime` object type | NO CHANGE for minimum | LOW |
| `closure_for(...)` / `attach_operational_metadata(...)` | Existing closure metadata attachment | NO CHANGE for minimum | LOW |
| `normalized_events(...)` | Reads audit and switch events | OPTIONAL EXTEND later | LOW |

## `admin_core/operator_observability.py`

| Function / Area | Current Purpose | Planned Class | Risk |
|---|---|---|---|
| `operation_summary_from_report(...)` | Historical operation summary | NO CHANGE for minimum | LOW |
| `audit_export_preview(...)` | Historical operation audit preview | OPTIONAL EXTEND later | LOW |
| `build_operator_view_model(...)` | Operator read model | OPTIONAL EXTEND later | LOW/MEDIUM |
| `selected_move_summary(...)` | Read selected move state files/copies | NO CHANGE for minimum | LOW |
| `barrier_summary(...)` | Read restore barrier state | NO CHANGE for minimum | LOW |

## `admin_core/operator_execution.py`

| Function / Area | Current Purpose | Planned Class | Reason |
|---|---|---|---|
| `runtime_recheck(...)` | Zero-move governance recheck | DO NOT TOUCH for minimum | Not the autoswitch runtime owner |
| `execute_packet(...)` | Append-only governance audit | DO NOT TOUCH for minimum | Already carries `operation_id` |
| `append_record(...)` | Governance record hash chain | DO NOT TOUCH | Separate governance truth |

