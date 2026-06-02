# PROGRAM Z7.4 - Implementation Conflict Audit Report

Project: V7 Vozduh  
Branch target: v7-next  
Date: 2026-06-02  
Mode: READ ONLY implementation conflict audit  
Evidence directory: `z7_4-evidence`

## Executive Verdict

Operation lineage wiring can be added to `tools/v7-users-autoswitch` without creating a duplicate orchestrator, scheduler, operation store, audit sink, or closure store, but only if the change is strictly additive.

The current autoswitch JSON contract has active Admin/UI consumers. The safest implementation boundary is:

1. keep current root JSON shape,
2. add a lineage-only `operation` envelope,
3. preserve `selected_moves`, `summary.selected_moves`, `decisions`, and `apply_result`,
4. reuse existing `planner_generation_id`, selected-move hash, `v7-audit-log`, and Admin closure semantics,
5. extend only `tests/unit/test_v7_users_autoswitch_policy.py` for the first bounded implementation block.

## Primary Answer

What can break if operation wiring is added to `tools/v7-users-autoswitch`?

- Admin endpoints can break if stdout stops being one parseable JSON object.
- Admin guarded apply can break if `apply_result.applied` changes type or location.
- Admin channel/settings UI can break if `summary`, `dynamic_load`, `safety`, `decisions`, or `selected_moves` change shape.
- Operator gates can break if selected-move state file shape or selected-move hash semantics change.
- Runtime recheck can break if `runtime_snapshot_hash` is redefined inconsistently with `admin_core/operator_execution.py`.
- Tests can break if existing selected move, restore-barrier, and service-signal assertions are not preserved.
- Historical report generation can drift if regenerated evidence no longer contains expected markers such as `selected_moves=0`, `selected_moves=[]`, or `apply_result.reason=no_selected_moves`.

## Discovery Gate Result

Every active consumer class visible in the repository was inventoried:

- systemd service/timer,
- Admin autoswitch endpoints,
- Admin UI renderers,
- selected-move adapters,
- operator execution/runtime recheck,
- operator observability,
- audit sink,
- runtime-support tools,
- tests,
- fixtures/evidence,
- report generator patterns.

Classification:

| Component | Classification |
|---|---|
| `tools/v7-users-autoswitch` | REUSE / EXTEND |
| `tests/unit/test_v7_users_autoswitch_policy.py` | EXTEND |
| `admin/v7-admin-api` autoswitch endpoints | REUSE / EXTEND later only if pass-through needed |
| Admin autoswitch UI | REUSE / DO NOT TOUCH for minimal change |
| `admin_core/operator_execution.py` | REUSE / DO NOT TOUCH for minimal change |
| `admin_core/operator_observability.py` | REUSE / DO NOT TOUCH for minimal change |
| `tools/runtime-support/v7-audit-log` | REUSE / DO NOT TOUCH |
| `systemd/v7-users-autoswitch.*` | DO NOT TOUCH |
| `tools/v7-control-plane-governance-check` | DO NOT TOUCH |
| Historical reports/evidence | DO NOT TOUCH |

## Autoswitch Consumer Inventory

| Consumer | Location | Contract | Risk |
|---|---|---|---|
| systemd apply cycle | `systemd/v7-users-autoswitch.service`, `.timer` | path, args, exit behavior | HIGH if touched |
| Admin plan | `admin/v7-admin-api:15548` | stdout JSON object under `plan` | MEDIUM |
| Admin dry-run | `admin/v7-admin-api:15564` | stdout JSON object under `plan` | MEDIUM |
| Admin guarded apply | `admin/v7-admin-api:15574` | `plan.apply_result.applied` | MEDIUM/HIGH |
| Channel UI | `admin/v7-admin-api:26654` | `decisions`, `selected_moves`, `summary` | MEDIUM |
| Settings UI | `admin/v7-admin-api:31801` | `summary`, `dynamic_load`, `safety.anti_flap`, `decisions` | LOW/MEDIUM |
| Selected move adapter | `admin/v7-admin-api:12916` | state file `selected_moves` list or `summary.selected_moves` count | MEDIUM |
| Operator selected move summary | `admin_core/operator_observability.py:1147` | state/evidence selected move files | MEDIUM |
| Runtime recheck | `admin_core/operator_execution.py:156` | selected move hash/count, runtime snapshot hash | HIGH semantic risk |
| Audit writer | `tools/runtime-support/v7-audit-log` | JSONL audit schema, metadata key/value args | LOW/MEDIUM |
| Main tests | `tests/unit/test_v7_users_autoswitch_policy.py` | direct `plan()` assertions | MEDIUM |

## Current JSON Contract

Current root autoswitch output:

```text
schema_version
updated
enabled
mode
apply_requested
target_egress
safety
summary
dynamic_load
reconnect_events
quality_history
org_isolation
decisions
selected_moves
apply_result
```

Fields that must remain stable:

- `selected_moves` as list,
- `summary.selected_moves` as count,
- `decisions` as list,
- `apply_result.applied` as boolean,
- `apply_result.reason` as no-op/deny string,
- `apply_result.results` as apply result list,
- root stdout as one JSON object,
- normal no-op/dry-run exit code behavior.

Consumers are generally tolerant of additional fields, but not of moved or retyped existing fields.

## Duplication Audit

Existing identifiers and metadata already present:

- `planner_generation_id` from autoswitch input hashes,
- selected move hash helper and restore barrier selected-move hashes,
- `runtime_snapshot_hash` in operator execution recheck,
- audit `request_id` in `v7-audit-log`,
- Admin/operator candidate `operation_id`,
- execution `event_id`,
- hash-chain `record_hash`.

Operation wiring is safe only if it references these existing truths instead of replacing them.

Conflict findings:

| Proposed Field | Conflict Risk | Verdict |
|---|---|---|
| `operation_id` | MEDIUM because Admin/operator already use candidate operation ids | Safe if scoped as runtime autoswitch operation |
| `runtime_snapshot_hash` | MEDIUM/HIGH if semantics differ from operator execution | Reuse or explicitly scope |
| `terminal_state` | MEDIUM because `apply_result` already encodes terminal status | Derive only |
| `audit metadata` | LOW/MEDIUM | Use `v7-audit-log`, no new sink |
| `closure metadata` | LOW/MEDIUM | Output reference only, no new closure store |
| operation envelope | LOW/MEDIUM | Additive lineage object only |

## Test Coverage Audit

Covered now:

- service-signal failover/non-failover,
- Telegram hard/soft behavior,
- restore barrier active/expired/cleared behavior,
- selected move budget,
- generation token/hash/count mismatch,
- canary reserved target behavior,
- selected move count assertions.

Not covered yet:

- operation envelope in dry-run/no-op output,
- operation id generation,
- selected move hash as output lineage,
- runtime snapshot hash as output lineage,
- terminal state/reason derivation,
- operation id on selected move rows,
- operation id on apply result rows,
- audit metadata construction for terminal runtime audit.

Minimum test extension target remains `tests/unit/test_v7_users_autoswitch_policy.py`.

## Fixture Audit

Current autoswitch tests build fixtures in temporary directories and do not rely on golden snapshots. Historical docs/evidence contain sample autoswitch JSON and text markers, but they are not active unit-test fixtures.

Potentially sensitive fixture/sample paths:

- `docs/track7/control-plane/e11_18-evidence/current-selected-moves-local-state-copy.json`
- `docs/track7/control-plane/e12-evidence/current-selected-moves-local-state-copy.json`
- older `current-autoswitch-plan.pretty.json` evidence files
- journal dumps containing embedded autoswitch JSON

No fixture update is required before a bounded additive implementation, unless tests are added with new expected operation lineage fields.

## Runtime Contract Audit

Runtime state writers in current autoswitch:

- `egress-load-summary.json` through `_persist_dynamic_load_summary()` during planning,
- `autoswitch-safety.json` through `_update_safety_after_apply()` after successful apply rows,
- `client-reconnect-state.json` through `_update_safety_after_apply()` when reconnect state changes.

Runtime readers:

- users/egress registries,
- `v7-state.json`,
- speed/client speed/service matrix,
- quality summary,
- safety state,
- Telegram sentinel,
- restore barrier,
- reconnect/vless activity,
- policy and org policy.

Adding output-only operation lineage does not change runtime truth. Changing state writer behavior would be a separate HIGH-risk implementation and is outside Z7.4 readiness.

## Phase Impact Matrix

| Change | Risk | Allowed In First Bounded Block |
|---|---|---|
| Add `operation` envelope | LOW/MEDIUM | yes |
| Add selected move hash output | LOW | yes |
| Add operation id to selected move rows | LOW/MEDIUM | yes |
| Add derived terminal state/reason | MEDIUM | yes, derived only |
| Add operation id to apply result rows | LOW/MEDIUM | yes |
| Emit terminal audit through `v7-audit-log` | MEDIUM | later in bounded block after output tests |
| Add closure target metadata | LOW/MEDIUM | yes as output reference only |
| Write selected-move state file | HIGH | no |
| Modify Admin endpoints | MEDIUM | no for first block |
| Modify systemd/timer | HIGH | no |

## Safe Implementation Boundary

Safe to add:

- `operation` envelope,
- `operation.operation_id`,
- `operation.operation_owner="tools/v7-users-autoswitch"`,
- `operation.operation_type="runtime_autoswitch"`,
- lineage references to `planner_generation_id`, selected move hash, runtime snapshot hash,
- derived `terminal_state` and `terminal_reason`,
- operation refs on selected moves/apply result rows,
- tests for no-op, selected-move, barrier-denied, and mocked apply paths.

Must not change:

- scheduler,
- systemd units,
- move selection,
- restore barrier rules,
- selected-move root list,
- summary counts,
- apply result contract,
- audit schema,
- closure schema,
- runtime state writer set.

## Implementation Readiness

Implementation can proceed to Z7.5 under a bounded additive plan.

Safest first change:

1. Add internal operation context in `tools/v7-users-autoswitch`.
2. Emit additive `operation` envelope in dry-run/no-op output.
3. Add tests proving existing keys remain unchanged.

Highest-risk change:

- writing selected-move state files or redefining `runtime_snapshot_hash`.

Rollback strategy:

- revert the bounded autoswitch/test change. Because the safe path introduces no new store and no migration, rollback is a code revert only.

## Truth Source Audit

```text
duplicate_operation_truth=false_if_lineage_only
duplicate_runtime_truth=false_if_autoswitch_remains_owner
duplicate_lineage_truth=false_if_existing_ids_are_referenced
duplicate_audit_truth=false_if_v7_audit_log_is_reused
duplicate_closure_truth=false_if_admin_closure_is_referenced_only
duplicate_rollback_truth=false_if_apply_result_remains_owner
```

## Final Verdicts

```text
consumer_inventory_complete=true
json_contracts_understood=true
test_coverage_understood=true
runtime_contracts_understood=true
operation_id_conflicts_understood=true
change_impact_understood=true
implementation_conflicts_understood=true
safe_to_begin_bounded_implementation=true
```

## Safety Statement

Z7.4 performed no implementation, no code patching in autoswitch/Admin/runtime files, no API creation, no runtime mutation, no routing mutation, no user movement, no autoswitch apply, no deploy, no service restart, no systemd modification, no timer modification, no cleanup, no deletion, no merge, and no force push.
