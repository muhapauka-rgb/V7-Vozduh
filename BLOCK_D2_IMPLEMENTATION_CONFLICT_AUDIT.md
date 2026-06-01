# Block D2 Implementation Conflict Audit

Date: 2026-06-01

## Search Scope

Searched repository for autoswitch safety, approval, proposal, hold, registry parser, review queue, approval workflow, dry-run packet, operator approval, governance approval, candidate approval, and enabled egress handling.

## Existing Implementations Found

| Area | Location | Behavior | Decision |
| --- | --- | --- | --- |
| Shadow planner | `tools/v7-users-autoswitch` | Produces full shadow plan and can optionally apply with `--apply`. | Reuse, do not duplicate. |
| Safety review | `tools/v7-autoswitch-safety-review` | Read-only preflight, but registry parser assumed legacy two-column rows. | Extend in place. |
| Restore barrier | `v7-users-autoswitch` / `autoswitch-restore-barrier.json` | Blocks selected moves under zero-budget restore clearance. | Reuse. |
| Operator surfaces | `admin_core/operator_observability.py` | Read-only approval/observability surfaces and manual apply forbiddance. | Do not modify in D2. |
| Approval docs | `docs/track7/control-plane/*` and block reports | Existing operator approval model. | Reuse as governance context. |

## Conflict Result

No existing bounded post-shadow proposal cap implementation was found.

The added `tools/v7-autoswitch-proposal-cap` is not a parallel planner. It consumes existing `v7-users-autoswitch` shadow JSON, applies operator hold filters and a fixed budget, and emits a non-executable proposal.

## Differences From Target

- The runtime-installed safety-review remains unmodified because deploy is forbidden in D2.
- Repository safety-review is fixed and was executed against live state through stdin over SSH for certification.

## Migration Path

1. Keep `v7-users-autoswitch` as the only planner.
2. Keep `v7-autoswitch-safety-review` as the safety preflight after KV parser remediation.
3. Use `v7-autoswitch-proposal-cap` as a read-only bridge from shadow plan to operator approval packet.
4. In the next deployment-authorized block, install or package the parser fix before any live operator apply.

