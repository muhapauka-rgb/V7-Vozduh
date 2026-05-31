# P3.B Truth Source Audit

Project: V7 Vozduh
Block: P3.B Runtime Hook Dry-Run Foundation

## Rule

Runtime Hook Dry-Run must be a derived observer/evaluator layer. It may not write decision state or become canonical for runtime, execution, candidates, readiness, simulation, verification or rollback.

## Truth Source Matrix

| Domain | Canonical source | Derived source | Presentation source |
| --- | --- | --- | --- |
| Runtime Events | Existing `AUDIT_FILE`, `EVENT_DIR`, `switch-history.jsonl`, observer JSONL files, `EXECUTION_EVENTS_FILE` | Normalized hook observation timeline | Admin logs, execution timeline, operator view |
| Runtime State | `STATE_DIR`, `users.registry`, `egress.registry`, service matrix, route-class state, trust state | `v7-state-json`, runtime fingerprint/drift/convergence | Admin runtime/checks/operator views |
| Execution Contracts | `EXECUTION_CONTRACTS_FILE` | Execution contract read models and dry-run hook contract references | `/api/execution/contracts` and contract drawers |
| Execution Events | `EXECUTION_EVENTS_FILE` | Execution timeline/verification/rollback summaries | `/api/execution/events`, `/api/execution/timeline` |
| Candidate | Existing proposal/evidence stores and execution candidate models | Candidate workflow/readiness/risk/explain views | `/api/execution/candidates`, candidate workflow UI |
| Readiness | Service matrix, trust, capacity, selected moves, restore barrier, target readiness adapters | Execution readiness, readiness forecast, gate catalog | `/api/execution/readiness*` |
| Simulation | Existing service impact, blast radius, rollback impact, outcome and route dry-run adapters | Hook simulation result | Rehearsal Preview and Execution preview |
| Verification | Execution verification preview plus later observed events | Hook verification result | `/api/execution/verification`, dry-run hook report |
| Rollback | Existing rollback manifest/impact/restore barrier evidence | Hook rollback simulation | `/api/execution/rollback`, rollback preview |

## Hook Truth Rules

Hook output is not canonical. It must always point back to canonical source refs and source hashes when available.

Hook-derived artifacts may include:

- Observation summary.
- Evaluation result.
- Dry-run decision.
- Verification plan.
- Report.

Hook-derived artifacts must not include:

- Authoritative routing state.
- User movement state.
- Decision state written back to runtime.
- Hook-owned execution contract.
- Hook-owned event stream.

## Conflict Review

No blocking truth-source conflict was found. Similar models exist, so P3.B must reuse them rather than introduce duplicate truth. If later implementation needs persistence, it must remain retention-bound, derived, and subordinate to existing canonical sources.

## Truth Source Verdict

`truth_source_audit_complete=true`

