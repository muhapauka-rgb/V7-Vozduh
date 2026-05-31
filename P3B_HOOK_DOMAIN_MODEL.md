# P3.B Hook Domain Model

Project: V7 Vozduh
Block: P3.B Runtime Hook Dry-Run Foundation

## Definition

A Runtime Hook Dry-Run is a passive observation and evaluation boundary. It sees runtime evidence, produces non-authoritative dry-run decisions, and reports what would happen. It never executes the decision.

## Domain Roles

| Role | Responsibility | Boundary |
| --- | --- | --- |
| Runtime Hook | Passive boundary that receives or reads evidence and starts dry-run evaluation. | No action authority, no writes to runtime decision state. |
| Observer | Reads existing runtime, service, trust, audit, candidate and execution evidence. | Read-only and freshness-aware. |
| Evaluator | Applies gate, policy, trust, capacity, readiness and autoswitch-like scoring semantics. | Produces only `WOULD_*` decisions. |
| Decision Producer | Emits non-authoritative decision and reasons. | Cannot emit executable decisions. |
| Verification Producer | Defines how the prediction should be checked later. | Does not trigger checkers or rollback. |
| Report Producer | Formats operator-facing explanation, evidence and confidence. | Presentation only. |

## Hook Responsibilities

Runtime Hook Dry-Run may:

- Observe existing runtime activity.
- Normalize evidence references.
- Evaluate gates and candidate state.
- Simulate likely impact.
- Produce a dry-run decision.
- Produce a verification plan.
- Produce an operator report.

Runtime Hook Dry-Run may not:

- Execute.
- Route.
- Apply.
- Autoswitch.
- Move users.
- Change runtime.
- Write decision state.
- Register action-capable hooks.

## Hook Lifecycle

1. Receive passive trigger or read request.
2. Load existing canonical inputs.
3. Check freshness and ownership.
4. Normalize observations.
5. Evaluate gates fail-closed.
6. Produce non-executable decision.
7. Attach evidence and confidence.
8. Attach verification and rollback simulation.
9. Render report.
10. Expire or compact derived output.

## Hook Boundary Invariant

Every hook output must include:

- `read_only=true`
- `derived_only=true`
- `preview_only=true`
- `non_authoritative=true`
- `execution_allowed_now=false`
- `runtime_hooks_with_authority=false`

## Domain Verdict

`hook_domain_defined=true`

