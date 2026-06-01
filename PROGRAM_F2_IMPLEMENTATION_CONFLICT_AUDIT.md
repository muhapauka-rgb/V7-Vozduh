# Program F2 Implementation Conflict Audit

Date: 2026-06-01

## Inspected Implementations

| Area | Existing Implementation | Decision |
| --- | --- | --- |
| Planner | `tools/v7-users-autoswitch` | Reuse; canonical fresh proposal source. |
| Proposal cap | `tools/v7-autoswitch-proposal-cap` | Reuse; budget and hold enforcement. |
| Safety review | `tools/v7-autoswitch-safety-review` | Reuse; D2 KV parser fix. |
| Movement preview | `tools/v7-route-movement-preview` | Reuse; no mutation. |
| Movement execution | `v7-user-switch` | Only after fresh exact packet passes recheck. |
| Operator execution module | `admin_core/operator_execution.py` | Not suitable for one-user movement; zero-movement governance only. |

## Conflict Finding

No duplicate system was created.

The existing canonical proposal source changed target from the prompt-approved `awg3` to fresh `awg0`. Overriding that with the stale target would bypass planner truth and packet freshness.

## Decision

Fail closed. Do not execute movement.

