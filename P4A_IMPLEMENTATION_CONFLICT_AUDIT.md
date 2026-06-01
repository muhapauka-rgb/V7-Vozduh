# P4.A Implementation Conflict Audit

Project: V7 Vozduh
Block: P4.A First Controlled Runtime Action Design

## Inspected Areas

- operator execution
- execution contracts
- approval packets
- candidate workflow
- governance preview
- rehearsal preview
- rollback preview
- verification reports

## Equivalent Functionality

The repository already contains the concepts P4.A needs:

- packet validation and replay denial in `admin_core/operator_execution.py`
- zero-movement governance state transition in `admin_core/operator_execution.py`
- approval/governance/rehearsal previews in `admin_core/operator_observability.py`
- execution preview and candidate workflow APIs in `admin/v7-admin-api`
- dry-run and verification APIs in `admin/v7-admin-api`

## Conflict Decision

P4.A must not create a parallel packet system, execution engine, approval queue, rollback executor or verification store.

The P4.A action design maps to existing packet/governance concepts and remains design-only.

## Reuse / Extend / Do Not Touch

| Component | Decision | Reason |
| --- | --- | --- |
| `admin_core/operator_execution.py` | Reuse later | Existing validation/recheck/replay pattern is the right boundary. |
| `admin_core/operator_observability.py` | Reuse | Existing approval/governance/rehearsal previews already explain the path. |
| `/api/execution/*` read APIs | Reuse | Existing execution evidence and rollback/readiness previews. |
| `/api/runtime/dry-run/*` read APIs | Reuse | Certified planning trust. |
| action-capable admin routes | Do Not Touch | P4.A must not implement action execution. |
| systemd/deploy/routing/autoswitch tools | Do Not Touch | Forbidden by prompt. |

## Verdict

`implementation_conflict_audit_complete=true`

`parallel_action_design_created=false`

