# PROGRAM Z7.2 - Operation Wiring Design Report

Project: V7 Vozduh  
Branch target: v7-next  
Date: 2026-06-02  
Mode: READ ONLY design  
Evidence directory: `z7_2-evidence`

## Executive Verdict

`operation_id` should be wired by extending existing runtime outputs and metadata, not by creating any new truth source.

Canonical design:

```text
tools/v7-users-autoswitch creates operation_id
  -> operation envelope in autoswitch JSON output
  -> selected moves / selected_move_hash / planner_generation_id / runtime_snapshot_hash
  -> execution / verification / rollback results
  -> terminal runtime verdict
  -> v7-audit-log metadata and object_id
  -> Admin closure object_id
  -> operator observability reads the linked lineage
```

No new runtime owner, scheduler, audit sink, closure store, rollback owner, operation store, or orchestrator is introduced.

## Discovery Gate Summary

Existing fields were inventoried before design.

Reusable fields:

- `operation_id`
- `proposal_id`
- `approval_id`
- `packet_id`
- `contract_id`
- `event_id`
- `request_id`
- `record_hash`
- `planner_generation_id`
- `selected_move_hash`
- `runtime_snapshot_hash`
- `before_hash`
- `after_hash`
- closure `object_type`
- closure `object_id`

Primary finding:

- `operation_id` exists in operator/governance/historical code.
- `operation_id` is missing in `tools/v7-users-autoswitch`.
- Wiring should add propagation, not duplicate lineage.

## Operation Creation Wiring

Creator:

- `tools/v7-users-autoswitch`

Creation time:

- once per runtime cycle,
- after runtime context is loaded,
- before selected moves are treated as executable,
- before no-op/denied/dry-run result is returned.

First copy:

```text
autoswitch JSON root -> operation.operation_id
```

Minimum operation envelope:

```json
{
  "operation": {
    "operation_id": "<id>",
    "operation_owner": "tools/v7-users-autoswitch",
    "operation_kind": "autoswitch_runtime_cycle",
    "operation_started_at": "<iso>",
    "operation_mode": "observe|guarded|active|disabled",
    "apply_requested": true,
    "target_egress": "",
    "planner_generation_id": "",
    "selected_move_hash": "",
    "selected_move_count": 0,
    "runtime_snapshot_hash": "",
    "terminal_state": "",
    "terminal_reason": ""
  }
}
```

No-op, denied, dry-run, observe, restore-barrier-denied, and replay-denied outcomes must receive operation identity. No mutation does not mean no operation.

## Autoswitch Wiring

Autoswitch remains owner of:

- planner,
- selected moves,
- selected move hash,
- planner generation,
- restore barrier checks,
- runtime recheck,
- execution,
- verification,
- normal movement rollback,
- terminal runtime verdict.

Required propagation:

| Autoswitch Area | Required `operation_id` Link |
|---|---|
| plan root | `operation.operation_id` |
| planner generation | `operation.planner_generation_id` |
| selected moves | each selected move references `operation_id` |
| selected move hash | `operation.selected_move_hash` |
| restore barrier | `operation.restore_barrier_ref` |
| runtime recheck | `operation.runtime_recheck` |
| apply result | each result row references `operation_id` |
| verification | verification result references `operation_id` |
| rollback | rollback result references same `operation_id` |
| terminal verdict | `operation.terminal_state` and `operation.terminal_reason` |

## Rollback Wiring

Rollback remains part of the same operation.

Normal rollback lineage:

```text
operation_id
  -> selected_move_hash
  -> selected_move_index
  -> execution result
  -> verification failure
  -> rollback attempt
  -> rollback verdict
  -> terminal runtime verdict
```

Generic rollback remains break-glass. It must reference an existing operation id, or a break-glass wrapper must create/require an operation id before audit and closure. The generic rollback primitive must not become rollback truth by itself.

## Audit Wiring

Audit owner remains:

- `tools/runtime-support/v7-audit-log`

Minimum audit references:

```text
action=runtime_operation_terminal
component=autoswitch
object_type=runtime_operation
object_id=<operation_id>
result=<terminal_state>
request_id=<operation request/correlation id>
metadata.operation_id=<operation_id>
metadata.planner_generation_id=<planner_generation_id>
metadata.selected_move_hash=<selected_move_hash>
metadata.selected_move_count=<selected_move_count>
metadata.runtime_snapshot_hash=<runtime_snapshot_hash>
metadata.restore_barrier_status=<status>
metadata.rollback_verdict=<rollback verdict when present>
```

Strongly recommended events:

- `runtime_operation_started`
- `runtime_operation_terminal`

Conditional events:

- `runtime_operation_rollback`
- `runtime_operation_denied`
- `runtime_operation_noop`

No new audit sink is required.

## Closure Wiring

Closure owner remains:

- `admin/v7-admin-api`
- `admin_core/operator_observability.py`

Closure key:

```text
object_type=runtime
object_id=<operation_id>
```

Minimum closure references:

- `operation_id`,
- terminal state,
- audit `request_id` or audit event reference,
- rollback verdict if present,
- selected move count,
- selected move hash,
- planner generation id.

Closure must be after audit:

```text
runtime terminal verdict -> audit exists -> closure may become VERIFIED/CLOSED
```

If audit is missing, closure remains `OPEN` or becomes `EXPIRED` with `audit_missing` reason.

## No-Op Wiring

No-op and denial states are real operation terminal states:

| Case | Terminal State |
|---|---|
| selected moves zero | `NO_OP_EMPTY_SELECTION` |
| policy disabled | `DENIED_POLICY` |
| trust denied | `DENIED_TRUST` |
| capacity denied | `DENIED_CAPACITY` |
| restore barrier denied | `DENIED_RESTORE_BARRIER` |
| replay denied | `DENIED_REPLAY` |
| dry-run | `NO_OP_DRY_RUN` |
| observe mode | `NO_OP_OBSERVE` |

Each must carry:

- `operation_id`,
- `planner_generation_id`,
- `selected_move_hash`,
- `selected_move_count`,
- terminal reason,
- audit reference.

## Complete Lineage

```text
operation_id
  -> planner_generation_id
  -> runtime_snapshot_hash
  -> selected_move_hash
  -> selected_move_count
  -> restore_barrier_ref
  -> runtime_recheck_verdict
  -> selected_moves[]
  -> execution_results[]
  -> verification_results[]
  -> rollback_verdict
  -> terminal_runtime_verdict
  -> audit_refs[]
  -> closure_ref
```

Required lineage:

- `operation_id`
- `planner_generation_id`
- `runtime_snapshot_hash`
- `selected_move_hash`
- `selected_move_count`
- terminal runtime state
- audit reference
- closure reference after closure

Optional lineage:

- proposal id,
- approval id,
- packet id,
- contract id,
- event id,
- rollback output refs,
- verification output refs.

Historical lineage:

- report-derived operations,
- evidence directories,
- audit export previews,
- execution rehearsal previews.

Historical lineage remains useful but not canonical runtime truth.

## Wiring Readiness

No work required:

- runtime owner selection,
- scheduler,
- planner generation primitive,
- selected move hash primitive,
- restore barrier logic,
- apply/verify/rollback mechanics,
- audit sink,
- closure store,
- operator observability reader.

Metadata extension only:

- operation envelope in autoswitch output,
- operation references in selected moves/apply/rollback rows,
- operation metadata in audit events,
- operation id as closure object id.

Minimal code later:

- generate/bind `operation_id` in autoswitch,
- emit terminal audit events through existing `v7-audit-log`,
- pass operation metadata through Admin guarded apply wrapper,
- require/reference operation id for break-glass rollback/manual paths.

Significant code not required:

- new orchestrator,
- new scheduler,
- new operation store,
- new audit sink,
- new closure store,
- new rollback engine.

## Truth Source Audit

| Truth | Design Verdict |
|---|---|
| Operation truth | `operation_id` reused; no new operation truth source |
| Runtime truth | `tools/v7-users-autoswitch` remains owner |
| Lineage truth | Operation envelope references existing facts; no new lineage store |
| Audit truth | `v7-audit-log` remains owner |
| Closure truth | Admin closure remains owner |
| Rollback truth | Autoswitch normal rollback; generic rollback break-glass only |

## Final Verdicts

```text
operation_creation_model_defined=true
runtime_wiring_defined=true
rollback_wiring_defined=true
audit_wiring_defined=true
closure_wiring_defined=true
lineage_model_defined=true
implementation_scope_understood=true
safe_to_continue_to_Z7_3=true
```

## Safety Statement

Z7.2 performed no implementation, no refactor, no API creation, no storage creation, no runtime mutation, no routing mutation, no user movement, no autoswitch apply, no deployment, no service restart, no systemd modification, no timer modification, no cleanup, no deletion, no merge, and no force push.

