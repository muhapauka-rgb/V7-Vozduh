# Z7.2 Evidence 05 - Lineage Map and Readiness

## Complete Lineage Map

```text
operation_id
  -> operation_owner=tools/v7-users-autoswitch
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

## Required Lineage

| Lineage | Required |
|---|---|
| `operation_id` | yes |
| `operation_owner` | yes |
| `planner_generation_id` | yes |
| `selected_move_hash` | yes |
| `selected_move_count` | yes |
| `runtime_snapshot_hash` | yes |
| terminal runtime state | yes |
| terminal reason | yes |
| audit `request_id` | yes |
| audit object id = `operation_id` | yes |
| closure object id = `operation_id` | yes after closure |

## Optional Lineage

| Lineage | Optional Condition |
|---|---|
| selected move entries | empty for no-op |
| verification output refs | only if execution attempted |
| rollback output refs | only if rollback attempted |
| approval id | only if operator approval packet involved |
| packet id | only if packet involved |
| proposal id | only if Admin proposal initiated the operation |
| contract id | only if execution contract preview is linked |
| event id | only if Admin execution event model is linked |

## Historical Lineage

Historical report lineage remains useful but must not be canonical runtime truth:

- `BLOCK_*.md` operation summaries,
- evidence directories,
- audit export previews,
- execution rehearsal previews,
- execution contract/event read-only stores.

## Wiring Readiness

No work required:

- autoswitch owner selection,
- scheduler,
- planner generation primitive,
- selected move hash primitive,
- restore barrier logic,
- runtime apply/verify/rollback mechanics,
- audit sink,
- closure store,
- operator observability reader.

Ownership wiring only:

- keep Admin direct switch as break-glass,
- keep generic rollback as break-glass primitive,
- keep operator packet recheck governance-only,
- keep execution contracts read-only/non-authoritative unless linked.

Metadata extension only:

- add operation id references to autoswitch output,
- add operation id references to selected move/apply/rollback rows,
- add operation metadata into audit events,
- use closure object id as operation id.

Minimal code later:

- generate/bind operation id inside autoswitch,
- expose operation envelope in autoswitch JSON,
- emit audit events through existing `v7-audit-log`,
- pass operation metadata through Admin guarded apply wrapper,
- allow generic rollback/break-glass wrappers to require/reference operation id.

Significant code:

- not required for Z7.2 design.
- new operation store is not justified.
- new orchestrator is forbidden by design.

## Truth Source Audit

| Truth | Owner | Z7.2 Design |
|---|---|---|
| Operation truth | Autoswitch runtime output + audit/closure references | Reuse `operation_id`, no new store |
| Runtime truth | `tools/v7-users-autoswitch` | Unchanged |
| Audit truth | `v7-audit-log` | Unchanged |
| Closure truth | Admin closure model | Unchanged |
| Rollback truth | Autoswitch branch; generic primitive only as break-glass | Unchanged |
| Lineage truth | Operation envelope references existing facts | No duplicate lineage store |

## Final Readiness Verdict

The design can continue to Z7.3 because it defines wiring around existing owners and existing metadata surfaces without creating a new truth source.

