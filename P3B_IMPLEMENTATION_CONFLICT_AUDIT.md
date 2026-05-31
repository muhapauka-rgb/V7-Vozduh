# P3.B Implementation Conflict Audit

Project: V7 Vozduh
Block: P3.B Runtime Hook Dry-Run Foundation

## Purpose

This audit identifies existing hook-like, observer-like and evaluator-like behavior so P3.B does not duplicate systems or accidentally introduce execution authority.

## Conflict Findings

| Area inspected | Existing behavior | Conflict level | P3.B decision |
| --- | --- | --- | --- |
| Autoswitch evaluator | `tools/v7-users-autoswitch` plans by default and can apply with `--apply`. | High | Reuse evaluator semantics; forbid apply path. |
| Sentinel | `tools/v7-telegram-sentinel` observes Telegram/service health and can invoke guarded autoswitch. | High | Consume sentinel state/events only; no sentinel-as-hook action. |
| Trusted RU | Diagnostic is evidence; decision is preview by default but has `--write-state`. | Medium | Use read-only output only; no state writes. |
| Operator execution | `admin_core/operator_execution.py` validates/rechecks packets and can append approval/governance records through execution-named modes. | High | Do not use as runtime hook foundation. |
| Operator observability | `admin_core/operator_observability.py` aggregates previews and disables actions. | Low | Reuse presentation and governance model. |
| Runtime support dry-runs | Proxy/public/route dry-runs already define non-mutating route simulation. | Medium | Reuse as dry-run semantics. |
| Execution preview | Admin API already exposes read-only execution/candidate previews. | Medium | Reuse; no new parallel preview family. |
| Candidate workflow | P2.7/P3.A candidate workflow already exists. | Medium | Reuse candidate status and lineage. |

## Critical Boundaries

### Autoswitch Boundary

Runtime hooks must never call:

- `v7-users-autoswitch --apply`
- Any wrapper that converts a hook decision into selected moves.
- Any route verification path that only makes sense after an apply.

Allowed use is limited to reading existing planner output or reusing gate vocabulary in a non-authoritative model.

### Sentinel Boundary

The sentinel can be a source of observed service evidence, but not a hook executor. P3.B hooks may consume sentinel state, freshness and event facts. They must not invoke sentinel runtime behavior that can start autoswitch.

### Trusted RU Boundary

Trusted RU decision output is a read-only preview unless `--write-state` is used. P3.B forbids write-state mode and treats existing trusted RU state as an external truth input, not hook-owned state.

### Operator Execution Boundary

`admin_core/operator_execution.py` is explicitly not a movement engine, but its execution naming and audit append paths make it unsafe as the foundation for P3.B hooks. P3.B hook contracts should not call it, wrap it, or depend on it for hook lifecycle.

## No-Duplicate Rule

P3.B must not create:

- A new autoswitch planner.
- A new execution queue.
- A new runtime event bus.
- A new hook-local state store.
- A new admin top-level section.
- A new truth source for candidate, readiness, simulation, verification or rollback.

## Conflict Verdict

`implementation_conflict_audit_complete=true`

