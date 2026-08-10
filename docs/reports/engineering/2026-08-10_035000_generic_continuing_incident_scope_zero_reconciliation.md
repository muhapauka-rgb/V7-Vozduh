# Generic continuing-incident scope-zero reconciliation

Дата: 2026-08-10

## Цель родительской Mission

Сохранить CT-M0F: измерить и сократить `CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_LATENCY`. Настоящий ремонт является только возвратом к этой цели и не создаёт отдельную Program, owner или Runtime path.

## Точная generic-причина

`tools/v7-service-matrix-test.update_matrix` уже умеет выпускать обычные `SERVICE_FAILURE_OBSERVED` и `SERVICE_FAILURE_REVALIDATED`; production JSONL содержит такие revalidation события для нескольких источников. Следовательно, отсутствие нового VLESS event на последнем cycle не являлось дефектом producer: новый VLESS episode имел только `failure_samples=1` при существующем пороге 3, а предыдущий episode получил owner-backed recovery.

Дефект находился в существующем `tools/v7-users-autoswitch.reconcile_service_failure_execution_outcomes`: когда `users.registry` уже подтверждал `current source scope = 0`, исторический passive protection intent мог остаться `OPEN` с прежним denominator. Он создавал zero-scope obligation и мог участвовать в выборе source, хотя не имел пользователей для защиты.

Это не VLESS-логика. Любой source с актуальным `unresolved_scope=0` теперь получает terminal protection intent:

```text
CURRENT_ROUTE_SOURCE_SCOPE_EMPTY
-> INTENT_CLOSED
-> channel_incident_state=OPEN_NO_ASSIGNED_USERS
-> no action / no Candidate / no Packet / no lease
-> next owner-backed source event with non-empty scope
```

Канал при этом не объявляется recovered: его наблюдение остаётся исторической диагностикой, а новый route-backed cohort сможет открыть новую current generation.

## Изменённые existing owners

- `tools/v7-users-autoswitch`: существующий scope-accounting и outcome-reconciliation owner;
- `tests/unit/test_service_failure_automation_evolution.py`: generic route-scope-zero contract.

Новых owner, state store, Planner, queue, scheduler, registry или raw user-list не создано. Compact projection хранит только count, fingerprint и route-truth pointer.

## Проверка

Пройдены `git diff --check` и affected suites:

```text
tests.unit.test_service_failure_automation_evolution
tests.unit.test_service_failure_episode
tests.unit.test_governed_canary_cli
tests.unit.test_v7_users_autoswitch_policy
```

Новый тест доказывает, что source с пустым live scope закрывает только protection intent, сохраняет `OPEN_NO_ASSIGNED_USERS`, не выполняет routing mutation и не перемещает пользователей. Существующие multi-source tests продолжают проверять, что live accounted incident предпочитается более новому historical zero-scope terminal.

## Production acceptance и следующий successor

До deploy production effect отсутствует: Candidate, Packet, lease, apply, routing mutation, rollback, Authority и Production Maturity равны `NONE`.

Следующий безопасный шаг: `tools/v7-safe-deploy` preflight для этого exact manifest, затем deploy и production non-test caller. Следующий обычный Matrix cycle должен consume existing reconciliation owner. При persistent failure с non-empty current scope он обязан продолжить тот же source-bound lifecycle; при empty scope терминал останется `CURRENT_SOURCE_SCOPE_EMPTY_NO_ACTION`; при recovery будет owner-backed recovery terminal. Во всех случаях CT-M0F возвращается к следующему lawful sample/residual без ручного Matrix запуска.
