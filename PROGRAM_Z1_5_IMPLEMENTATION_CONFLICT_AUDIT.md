# Program Z1.5 Implementation Conflict Audit

Date: 2026-06-01

## Existing Implementations

| Area | Existing Implementation | Behavior | Decision |
| --- | --- | --- | --- |
| Planner | `tools/v7-users-autoswitch` | Builds shadow plan, generation ID, selected move hash, optional apply. | Reuse. |
| Proposal cap | `tools/v7-autoswitch-proposal-cap` | Read-only budget/hold post-processor for shadow JSON. | Extend if needed. |
| Safety review | `tools/v7-autoswitch-safety-review` | Pure read-only safety preflight. | Reuse. |
| Movement preview | `tools/v7-route-movement-preview` | Non-mutating one-user movement and rollback preview. | Reuse. |
| Operator execution packet | `admin_core/operator_execution.py` | Zero-movement governance packet validation and audit records only. | Do not reuse for live movement without explicit new contract. |
| Approval preview UI | `admin_core/operator_observability.py` | Read-only operator preview and replay semantics. | Reuse/extend. |

## Conflict Findings

No equivalent policy-based movement approval contract exists.

Existing packet support is zero-movement and must not be stretched into movement authority. A policy-based approval model should be added as a governance contract around existing planner/proposal/recheck tools, not as a parallel planner or executor.

## Reuse Path

1. Keep `v7-users-autoswitch` as canonical proposal source.
2. Keep proposal cap as the bounded budget/hold layer.
3. Add policy approval validation as a recheck layer.
4. Keep movement execution in existing `v7-user-switch` or a future explicitly approved bounded wrapper.
5. Use existing audit/replay patterns, but with a new movement packet schema.

