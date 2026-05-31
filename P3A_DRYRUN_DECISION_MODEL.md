# P3.A Dry-Run Decision Model

Project: V7 Vozduh
Block: P3.A Runtime Dry-Run Foundation

## Decision Principle

Dry-run decisions describe what would happen under current evidence. They never authorize or perform the action.

## Decision Values

| Decision | Meaning |
| --- | --- |
| `NO_ACTION` | Evidence does not justify movement, rollback, review or blocking. |
| `WOULD_MOVE` | If execution were allowed, the candidate would be eligible for movement. |
| `WOULD_BLOCK` | Safety, policy, trust, service or consistency gates would block action. |
| `WOULD_REVIEW` | Human review would be required before approval. |
| `WOULD_ROLLBACK` | If the candidate had already been applied, rollback would be recommended. |

Forbidden values:

- `MOVE`
- `APPLY`
- `EXECUTE`
- `ROUTE`
- `AUTOSWITCH_APPLY`

## Fail-Closed Evaluation Order

1. Source availability and freshness.
2. Truth-source consistency.
3. Runtime safety gates.
4. Policy and authority gates.
5. Trust gates.
6. Required-service gates.
7. Capacity and load gates.
8. Existing selected moves and hidden movement checks.
9. Candidate scoring.
10. Simulation result.
11. Rollback completeness.
12. Verification readiness.

The first blocking gate produces `WOULD_BLOCK` unless the correct outcome is `WOULD_REVIEW`.

## Decision Evidence

Each decision must include:

- Source references.
- Gate outcomes.
- Score explanation where scoring applies.
- Blocking reasons.
- Missing evidence.
- Simulation references.
- Verification plan reference.
- Rollback preview reference.

## Authority Flags

Every decision must carry:

- `preview_only=true`
- `non_authoritative=true`
- `execution_allowed_now=false`
- `runtime_mutation_performed=false`
- `routing_changed=false`
- `users_moved=false`

## Decision Verdict

`dryrun_decision_model_defined=true`

