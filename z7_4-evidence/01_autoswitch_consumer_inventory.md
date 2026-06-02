# Autoswitch Consumer Inventory

## Consumers

| Consumer | Location | Purpose | Schema Expectations | Classification | Risk |
|---|---|---|---|---|---|
| Autoswitch systemd service | `systemd/v7-users-autoswitch.service` | Invokes `/usr/local/bin/v7-users-autoswitch --apply` | Relies on executable path, stdout JSON tolerated by journald, exit code `0` | DO NOT TOUCH | HIGH if invocation/exit behavior changes |
| Autoswitch systemd timer | `systemd/v7-users-autoswitch.timer` | Starts runtime cycle every 20s after boot | No JSON parsing | DO NOT TOUCH | HIGH if cadence changed |
| Admin plan endpoint | `admin/v7-admin-api:15548` | Runs `v7-users-autoswitch --pretty` | Parses entire stdout as JSON and returns it under `plan` | REUSE / EXTEND | MEDIUM |
| Admin dry-run endpoint | `admin/v7-admin-api:15564` | Runs `v7-users-autoswitch --pretty`, audits wrapper action | Same root JSON under `plan`; no strict schema validation | REUSE / EXTEND | MEDIUM |
| Admin guarded apply endpoint | `admin/v7-admin-api:15574` | Runs `v7-users-autoswitch --mode guarded --apply --pretty` | Reads `plan.apply_result.applied`; returns root `plan` to UI | REUSE / EXTEND | MEDIUM/HIGH |
| Admin channel autoswitch UI | `admin/v7-admin-api:26654` | Target-scoped preview/apply display | Reads `plan.decisions`, `plan.selected_moves`, `plan.summary` | REUSE / EXTEND | MEDIUM |
| Admin settings autoswitch UI | `admin/v7-admin-api:31801` | Global autoswitch display/actions | Reads `plan.summary`, `plan.dynamic_load`, `plan.safety.anti_flap`, `plan.decisions` | REUSE / EXTEND | LOW/MEDIUM |
| Admin selected moves adapter | `admin/v7-admin-api:12916` | Execution gate selected-move blocker | Reads state files with `selected_moves` list or `summary.selected_moves` count | REUSE / EXTEND | MEDIUM if autoswitch starts writing selected-move state |
| Admin restore barrier adapter | `admin/v7-admin-api:12946` | Execution gate restore-settle blocker | Reads `autoswitch-restore-barrier.json`; expects active/expired/cleared | DO NOT TOUCH | LOW if output-only lineage |
| Operator execution recheck | `admin_core/operator_execution.py:138` | Zero-budget runtime recheck selected-move hash | Reads `selected-moves.json`, `selected_moves.json`, `current-selected-moves.json`; expects list or `selected_moves` list | REUSE / EXTEND | MEDIUM/HIGH if state writer changes |
| Operator observability selected-move summary | `admin_core/operator_observability.py:1147` | Operator view selected move count/freshness | Reads `selected-moves.json`, `autoswitch-selected-moves.json`, copied evidence files | REUSE / EXTEND | MEDIUM |
| Operator observability barrier summary | `admin_core/operator_observability.py:1183` | Restore-barrier UI/lineage | Reads barrier file fields; not autoswitch stdout | DO NOT TOUCH | LOW |
| Audit sink | `tools/runtime-support/v7-audit-log` | Appends audit JSONL | Accepts metadata key/value args; owns `request_id` when not supplied | REUSE / EXTEND | LOW/MEDIUM |
| Governance report generator | `tools/v7-control-plane-governance-check` | Historical control-plane status generation | Parses strings, fixture evidence, selected move snippets | DO NOT TOUCH | MEDIUM for regenerated reports |
| Autoswitch unit tests | `tests/unit/test_v7_users_autoswitch_policy.py` | Direct module tests for plan behavior | Calls `AutoswitchPlanner.plan()`; asserts nested keys and selected counts | EXTEND | MEDIUM |
| Autoswitch policy design tests | `tests/unit/test_v7_autoswitch_policy_design.py` | Abstract policy decision tests | Does not parse `tools/v7-users-autoswitch` JSON directly | DO NOT TOUCH | LOW |
| Restore settle tests | `tests/unit/test_v7_restore_settle_gate.py` | Restore gate sample parsing | Uses sample `summary.selected_moves` shape | DO NOT TOUCH / WATCH | LOW/MEDIUM |
| Historical reports/evidence | `BLOCK_*`, `PROGRAM_*`, `docs/track7/**` | Audit history, sample outputs, governance narratives | Some embed full autoswitch JSON or text markers | DO NOT TOUCH | LOW for implementation, MEDIUM for future report regeneration |

## Active Output Consumers

Active code consumers of current stdout JSON are concentrated in `admin/v7-admin-api`.

Active state-file consumers are split across Admin and operator modules:

- `selected_moves_read_adapter()`
- `selected_move_summary()`
- `selected_moves_state()`

This split is important: adding an operation envelope to stdout is safer than introducing or changing any selected-move state file writer.

## Parser Strictness

| Parser | Strictness | Tolerance |
|---|---|---|
| `run_json_command()` in Admin | Requires stdout to be parseable JSON object; extra fields tolerated | HIGH root parse sensitivity |
| Admin UI JS | Optional chaining/defaults; extra fields tolerated | HIGH tolerance |
| Admin guarded apply | Requires `apply_result` object and `applied` key | MEDIUM strict |
| Selected move adapters | Tolerate `selected_moves` list or numeric `summary.selected_moves` | MEDIUM tolerance |
| Operator execution recheck | Strict about selected move hash and zero count | HIGH semantic strictness |

## Inventory Verdict

Consumer inventory is complete for active code paths visible in the repository. Historical reports/evidence are inventoried as non-active consumers but can be affected by future regenerated samples.
