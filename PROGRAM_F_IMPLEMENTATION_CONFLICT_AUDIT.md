# Program F Implementation Conflict Audit

Date: 2026-06-01

## Inspected Implementations

| Area | Existing Implementation | Decision |
| --- | --- | --- |
| Autoswitch planner | `tools/v7-users-autoswitch` | Reuse only. |
| Proposal cap | `tools/v7-autoswitch-proposal-cap` | Reuse only. |
| Safety review | `tools/v7-autoswitch-safety-review` | Reuse D2 parser fix. |
| Movement preview | `tools/v7-route-movement-preview` | Reuse for proposal/rollback preview. |
| Operator execution | `admin_core/operator_execution.py` | Do not misuse; existing module is zero-movement record/governance only. |
| Runtime movement | `v7-user-switch` | Only allowed after exact approved packet and recheck. |
| Runtime checks | `v7-killswitch-check`, `v7-user-route-check`, `v7-runtime-contract-validate` | Reuse. |

## Conflict Finding

No new planner, movement executor, approval queue, rollback engine, deploy path, or systemd mutation was created.

The requested Program F Stage 1 says "Use approved packet", but no approved packet exists in the prompt or repo artifacts. Executing anyway would create an approval-bypass path, which is forbidden.

## Decision

Stop before runtime movement.

