# Program Z1 Implementation Conflict Audit

Date: 2026-06-01

## Reused Implementations

| Area | Existing Implementation | Decision |
| --- | --- | --- |
| Autoswitch planner | `tools/v7-users-autoswitch` | Reused as canonical fresh planner. |
| Proposal cap | `tools/v7-autoswitch-proposal-cap` | Reused for budget `1` and hold filters. |
| Safety review | `tools/v7-autoswitch-safety-review` | Reused for read-only safety preflight. |
| Movement preview | `tools/v7-route-movement-preview` | Reused for target and rollback preview. |
| Runtime movement | `v7-user-switch` | Not invoked because packet was stale. |

## Conflict Finding

No duplicate planner, executor, packet engine, rollback engine, or systemd/deploy path was introduced.

Executing the prompt-approved `10.7.0.16 -> awg0` movement after fresh planner changed the canonical proposal would have created an approval bypass. The existing planner truth overrides the stale packet.

## Decision

Stop before movement and report fresh approval requirement.

