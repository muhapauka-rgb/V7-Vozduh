# Block E Implementation Conflict Audit

Date: 2026-06-01

## Inspected Areas

- autoswitch planner
- proposal cap
- operator execution
- movement packets
- approval packets
- rollback previews
- verification tools

## Existing Implementations

| Area | Location | Behavior | Decision |
| --- | --- | --- | --- |
| Autoswitch planner | `tools/v7-users-autoswitch` | Produces shadow plan and optional apply. | Reuse. |
| Proposal cap | `tools/v7-autoswitch-proposal-cap` | Read-only post-processes shadow JSON into bounded proposal. | Reuse. |
| Safety review | `tools/v7-autoswitch-safety-review` | Read-only safety review with D2 KV parser fix. | Reuse. |
| Movement preview | `tools/v7-route-movement-preview` | Non-mutating switch/rollback preview. | Reuse. |
| Runtime checks | `v7-killswitch-check`, `v7-user-route-check`, `v7-runtime-contract-validate` | Runtime verification. | Reuse. |
| Operator execution packet module | `admin_core/operator_execution.py` | Existing packet logic is zero-movement record/governance only. | Do not misuse for movement. |

## Conflict Findings

No new planner was created.

No new apply engine was created.

No movement packet executor was created in Block E Stage 1.

Existing `admin_core/operator_execution.py` cannot be used as a one-user movement executor because it explicitly validates zero-movement packets. Treating it as a live movement approval engine would be a semantic conflict.

## Decision

Use existing shadow planner plus proposal cap for Stage 1 only.

Stop before Stage 2 until explicit operator approval names:

- candidate user
- current egress
- target egress
- budget
- rollback command
- pre/post checks

