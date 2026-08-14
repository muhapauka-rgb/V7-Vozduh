# Change Impact Matrix

## Planned Change Impact

| Planned Change | Risk | Why | Safe Boundary |
|---|---|---|---|
| Add root `operation` envelope | LOW/MEDIUM | Active JSON consumers are tolerant of extra root fields | Additive only; do not wrap current root |
| Add root `operation_id` alias | MEDIUM | Existing Admin/operator workflows already use `operation_id` | Prefer canonical `operation.operation_id`; if root alias exists, type-scope clearly |
| Add `selected_move_hash` | LOW | Existing helper already computes it; barrier already uses related hashes | Derive from existing `_selected_moves_hash()` only |
| Add `runtime_snapshot_hash` | MEDIUM | Existing operator recheck computes a runtime snapshot hash separately | Match existing semantics or name autoswitch-specific hash explicitly |
| Add `terminal_state` | MEDIUM | May duplicate `apply_result.applied/reason` | Derive only; do not alter `apply_result` |
| Add `terminal_reason` | LOW/MEDIUM | Existing no-op reasons already used in reports | Preserve existing reason strings |
| Add audit metadata | MEDIUM | `v7-audit-log` writes to audit JSONL and owns `request_id` | Reuse audit schema; do not create new sink |
| Add closure metadata | LOW/MEDIUM | Admin closure owns closure state | Output target/ref only; no new closure store |
| Add operation id to selected move rows | LOW/MEDIUM | UI ignores extra row fields; tests may need updates | Keep existing row fields unchanged |
| Add operation id to apply result rows | LOW/MEDIUM | Existing row consumers mostly inspect rc/verify/rollback/output | Keep existing row fields unchanged |
| Change stdout shape | HIGH | Admin `json.loads(output)` and UI expect root plan object | Forbidden |
| Change exit behavior | HIGH | systemd/Admin rely on normal `0` for dry-run/no-op planning | Forbidden |
| Write selected-move state file | HIGH | Multiple adapters read selected-move files with subtly different candidates | Defer unless separately audited |

## Safe Implementation Boundary

May be added safely:

- additive root `operation` envelope,
- derived selected move hash,
- operation id references on move/result rows,
- derived terminal fields,
- audit metadata passed to existing `v7-audit-log` in apply/runtime mode only,
- tests asserting additive shape.

Must remain untouched:

- scheduler/timer/service,
- move selection algorithm,
- restore barrier admission logic,
- safety state update logic except additive metadata if proven safe,
- `v7-audit-log` schema,
- Admin closure schema,
- Admin autoswitch endpoint response wrappers,
- `selected_moves` root list,
- `summary.selected_moves` count,
- `apply_result` shape.

Must not be introduced:

- new orchestrator,
- new scheduler,
- new operation store,
- new audit sink,
- new closure store,
- duplicate selected-move state writer,
- duplicate runtime recheck owner.

## Highest Risk

The highest-risk change is any write or schema change involving selected-move state files, because Admin and operator modules already read multiple possible selected-move filenames and do not all use the same candidate list.

The second-highest risk is redefining `runtime_snapshot_hash` differently from `admin_core/operator_execution.py`.
