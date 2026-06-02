# E35.F Admin Integration Plan

## Constraint

Use existing `/admin-v2`.

Do not create a new top-level section.

## Главная

Add compact execution surfaces:

- Execution Summary;
- Pending Executions;
- Execution Failures;
- Rollback Activity;
- Current Autonomy Level.

## Пользователи

Per-user drawer additions:

- Execution History;
- Authority History;
- Rollback History;
- Verification Status;
- linked Evidence;
- linked Proposal;
- routing mode owner.

## Каналы

Per-channel drawer additions:

- Execution Impact;
- Target Readiness;
- Current capacity class;
- rollback exposure;
- affected users in active/past contracts.

## Проверки

Add check cards:

- Execution Health;
- Validation Health;
- Verification Health;
- Rollback Health;
- Authority Read Path Health.

## Логи

Add filters for:

- Execution Events;
- Validation Events;
- Verification Events;
- Rollback Events;
- Replay Denials;
- Contract Expiry.

## Безопасность

Surface:

- denied executions;
- review-required executions;
- emergency-only outcomes;
- authority conflicts;
- unreadable stores;
- stale trust blocks.

## UX Rules

- Operator copy first, raw details second.
- Drawer-first details.
- No noisy always-open panels.
- Every execution item links to Evidence, Proposal, Authority, Contract, Verification and Rollback state.

admin_integration_defined=true
