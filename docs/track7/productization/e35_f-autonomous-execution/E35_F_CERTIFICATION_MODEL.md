# E35.F Certification Model

## Certification Layers

Before live autonomous execution:

| Layer | Required verdict |
|---|---|
| Read Path | CERTIFIED |
| Authority | CERTIFIED |
| Boundary Evaluator | CERTIFIED |
| Conflict Resolver | CERTIFIED |
| Evidence Linkage | CERTIFIED |
| Proposal Linkage | CERTIFIED |
| Execution Contract | CERTIFIED |
| Validation Engine | CERTIFIED |
| Verification Engine | CERTIFIED |
| Rollback | CERTIFIED |
| Observability | CERTIFIED |
| Audit | CERTIFIED |
| Replay Protection | CERTIFIED |
| Runtime Hook | CERTIFIED in dry-run before enforce |

## Conditions That Must Be GO

- Authority store readable.
- Evaluator and conflict resolver agree on source hash.
- Contract generator emits exact users/targets/rollback.
- Validation denies stale/missing inputs.
- Verification detects out-of-scope movement.
- Rollback remains exact-scope.
- Admin shows reason, authority, rollback, verification and next safe action.
- Audit chain is append-only.
- Replay is denied.

## NO-GO Conditions

- Any runtime hook can execute without contract.
- Contract can omit rollback.
- REVIEW_REQUIRED can become ALLOW without review closure.
- OPERATOR_PINNED can be bypassed by autonomous action.
- MANUAL mode can be overridden without explicit operator authority.
- Hidden movers or selected moves can be ignored.
- Store unreadable fails open.

## Certification Verdict

certification_model_defined=true
runtime_mutation_performed=false
