# Service Failure M5a/M5b: Action Class Contract и Shadow Boundary

Дата: `2026-07-26`
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`
Mission scope: `M5a/M5b`, read-only production verification.

## Итог

`PASS`. Текущий Service Failure цикл теперь различает Shadow demand и реально
допустимый action boundary. Shadow никогда не становится implicit execution
permission.

## Реализация

В существующем `tools/v7-users-autoswitch` расширен owner
`current_action_class_contract`.

Для Authority выше `CANARY` теперь обязательны:

- source и target egress scope;
- `max_users`, maximum Authority class и expiry;
- fresh-evidence, verification, rollback, anti-flap и cooldown gates;
- concrete stop conditions.

Новый read-only projection
`v7.service-failure-action-class-execution-boundary.v1` сопоставляет:

```text
Shadow candidate demand
-> current scoped action-class contract
-> all existing execution gates
-> NO_ACTION / STOP_SAFE / PACKET_MATERIALIZATION_ELIGIBLE
```

`PACKET_MATERIALIZATION_ELIGIBLE` не создаёт Candidate, Packet или lease и не
даёт право на execution. Это только следующий допустимый инженерный шаг.

## Production caller

Deploy: `deploy-z8-14-Updatesystem-7a15b1e-20260726T011105`.
Manifest изменил только `tools/v7-users-autoswitch`; service restart `false`.

Read-only production caller `/usr/local/bin/v7-users-autoswitch --pretty`:

```text
shadow_candidate_count = 76
allowed_selected_count = 0
status = STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED
contract blocker = current_action_class_contract_missing_or_schema_invalid
execution_authorized = false
Packet / lease = not created
apply = false (dry_run)
users moved = 0
```

## Проверка и terminal

- 181 focused unit tests: `PASS`.
- `tools/v7-truth-check --all --json`: `PASS / FULLY_ALIGNED`.
- `tools/v7-convergence-status --json`: `PASS / ALIGNED`.
- local, GitHub и production runtime snapshot:
  `7a15b1e330a33e40698e3ce7702b6a2b76a637ef`.

Forbidden effects: Runtime apply `0`, routing mutation `0`, user movement `0`,
Packet execution `0`, restore-barrier write `0`, rollback apply `0`, Authority
grant `0`, Production Maturity change `0`.

Current legal terminal remains `ENGINEERING_AUTHORITY`. Exact next frontier is
M5c boundary preparation only after the existing Authority owner provides a
fresh scoped contract; absent that contract V7 correctly remains `STOP_SAFE`.
