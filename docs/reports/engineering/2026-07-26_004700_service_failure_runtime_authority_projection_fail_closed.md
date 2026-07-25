# Service Failure: закрытие устаревшей runtime Authority-проекции

Дата: `2026-07-26`
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`
Класс: `IMPLEMENTATION_OWNER_EXTENSION` / `POLICY_AUTHORITY_BOUNDARY`

## Итог

`PASS`. Устранён latent production-риск: историческая policy-проекция
`XLARGE_BATCH/50` больше не может интерпретироваться как текущая Authority.
Реальный production planner теперь fail-closed ещё до restore-barrier/apply.

## Наблюдение и last responsible link

Read-only production preflight обнаружил в существующем owner
`/etc/v7/policy.json`:

```text
authority_class = XLARGE_BATCH
certified_authority_class = XLARGE_BATCH
current_allowed_user_budget = 50
promoted_at = 2026-07-03
```

При этом CPS Section 0 фиксирует текущий frontier
`V7_SERVICE_FAILURE_AUTOMATION_AUTHORITY_RECONCILIATION`, stop
`ENGINEERING_AUTHORITY` и запрет на user movement без exact one-use contract.

Последняя ответственная связь:

```text
historical policy promotion
-> tools/v7-users-autoswitch authority_budget_policy
-> selected-move budget
-> restore-barrier/apply path
```

До исправления historical evidence могло дать planner-у budget `50`; это не
было текущим CPS-bound action Authority.

## Исправление

В существующем owner `tools/v7-users-autoswitch` добавлен
`v7.current-action-class-contract.v1` gate.

Для Authority выше `CANARY` policy обязана иметь свежий scoped contract с:

- `contract_id` и `active_program`;
- legal action class `GOVERNED_ONLY` либо `EMERGENCY_FAILOVER`;
- неистёкшим `expires_at`;
- maximum Authority class и `max_users`.

Контракт ограничивает effective budget. Его отсутствие, неправильная схема,
scope, action class, срок, Authority ceiling или zero budget дают
`FROZEN/0` с причиной
`block_all_selected_moves_current_action_class_contract_required`.
Новый owner, queue, registry, planner, runtime или Authority не созданы.

## Проверка

- Локально: `180` unit tests PASS, включая новый regression:
  historical `XLARGE_BATCH` без contract -> `selected_moves=0`.
- Production deploy: `deploy-z8-14-Updatesystem-613f7a6-20260726T004805`;
  manifest изменил только `/usr/local/bin/v7-users-autoswitch`.
- Production caller: read-only `/usr/local/bin/v7-users-autoswitch --pretty`.
  Результат: `candidate_moves_total=76`, `selected_moves=0`,
  `authority_lifecycle_state=FROZEN`, `current_allowed_user_budget=0`,
  `apply=false/dry_run`.
- Provenance refresh: `deploy-z8-14-Updatesystem-b7f3937-20260726T005012`,
  changed runtime files `[]`, service restart `false`.
- `tools/v7-truth-check --all --json`: `PASS / FULLY_ALIGNED`.
- `tools/v7-convergence-status --json`: `PASS / ALIGNED`.
- local, GitHub и production runtime snapshot: commit
  `b7f3937b815fe21e51e1de10a6b1041a3e36c06f`.

## Эффекты и terminal

```text
runtime apply = 0
routing mutation = 0
user movement = 0
packet execution = 0
restore-barrier write = 0
rollback apply = 0
authority grant = 0
Production Maturity change = 0
```

Текущий legal terminal не изменён: `ENGINEERING_AUTHORITY`.

Exact next OMP frontier:

`V7_SERVICE_FAILURE_AUTOMATION_AUTHORITY_RECONCILIATION` — существующий
Authority owner может выдать только свежий, exact, scoped, expiring contract;
без него система корректно остаётся `STOP_SAFE/FROZEN`. Этот отчёт не выдаёт
Authority и не разрешает apply.
