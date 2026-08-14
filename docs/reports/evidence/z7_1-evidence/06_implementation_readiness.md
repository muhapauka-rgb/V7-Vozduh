# Z7.1 Evidence 06 - Implementation Readiness

## No Work Required

| Area | Why |
|---|---|
| Runtime scheduler | Existing systemd autoswitch timer/service already starts runtime cycles. |
| Runtime owner | `tools/v7-users-autoswitch` already owns runtime planning/apply/verify/rollback mechanics. |
| Selected move calculation | Autoswitch already computes selected moves. |
| Selected move hash primitive | Autoswitch already has `_selected_moves_hash()`. |
| Planner generation primitive | Autoswitch already has `_generation_status()`. |
| Restore barrier enforcement | Autoswitch already reads and enforces restore-barrier/generation clearance. |
| Audit sink | `v7-audit-log` already exists and preserves metadata. |
| Closure store | Admin closure JSONL model already exists. |
| Operator observability | Historical operation/audit/closure preview surfaces already exist. |

## Configuration Only

No clearly configuration-only step was identified for full runtime-operation wiring. Current gaps are code-level wiring gaps, not only config gaps.

## Ownership Consolidation Only

| Area | Required Consolidation |
|---|---|
| Admin direct user switch | Must remain break-glass or controlled invocation; not normal runtime owner. |
| Admin rollback apply | Must remain break-glass/generic primitive; not normal rollback owner. |
| Execution contract/event store | Must remain read-only/non-authoritative unless later merged into runtime operation lineage. |
| Operator packet recheck | Must remain governance-only, not a second execution recheck owner. |
| Draft planner scheduler | Must remain dormant/DO NOT TOUCH unless explicitly merged. |

## Minimal Code Later

These are likely minimal future code changes, not performed in Z7.1:

- Add or accept `operation_id` in autoswitch runtime cycle context.
- Emit `operation_id` in autoswitch plan/apply output.
- Emit selected move hash as canonical operation lineage.
- Bind `planner_generation_id`, restore-barrier status, and selected move hash to operation lineage.
- Pass operation metadata into `v7-audit-log`.
- Use the existing Admin closure model to close runtime operation ids.
- Add operation lineage metadata to generic rollback/break-glass audit events.

## Significant Code Later

These would be significant and should be avoided unless a later program explicitly proves they are necessary:

- New orchestrator service.
- New operation store.
- New audit sink.
- New closure store.
- New scheduler.
- New execution engine.
- New rollback engine.
- Replacing Admin/operator historical operation model.

## Readiness Verdict

Implementation readiness is understood:

- The runtime mechanics are ready for wiring.
- The sinks/stores are ready for wiring.
- The missing work is the bridge, not the core owners.
- Future implementation should be small and owner-preserving if it only wires existing components.

