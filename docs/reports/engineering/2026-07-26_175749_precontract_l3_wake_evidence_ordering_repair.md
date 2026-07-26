# Отчёт: устранение deadlock между L3 wake и Action Class contract

Дата: 2026-07-26
Статус: IMPLEMENTED_AND_TESTED_PENDING_PRODUCTION_DEPLOY

## Причина

В существующем `tools/v7-users-autoswitch` одноразовый Action Class contract
проверялся до L3 evidence gate. При отсутствующем или истёкшем contract
`_authority_budget_gate` корректно удалял выбранное перемещение. Затем
`_emergency_failover_authority_gate` строил L3 wake только из оставшегося
`selected`; в результате не возникало ни evidence, ни допустимого fresh request.
После fail-closed запрета на выпуск contract без L3 wake образовывался цикл:

`contract missing -> selected empty -> no L3 wake -> contract request denied`.

Это дефект порядка producer -> consumer, а не основание для ослабления
Authority или создания искусственного production event.

## Исправление существующего owner

`AutoswitchPlanner.plan()` сохраняет ограниченный request-cap pre-contract
shadow selection и передаёт его исключительно в L3 evidence gate.

- `tools/v7-users-autoswitch` помечает источник как
  `pre_contract_shadow_selection_read_only`, только когда contract gate уже
  обнулил execution selection;
- evidence-only rows никогда не попадают в `eligible`: для этого требуется,
  чтобы та же строка пережила Action Class contract gate;
- следовательно, L3 wake может открыть только выпуск fresh owner-issued
  contract, но не Candidate, Packet, lease, routing mutation или user movement;
- после contract issuance обычный planner обязан заново пройти freshness,
  policy, authority, target, rollback и execution gates.

## Проверка

Добавлен регрессионный тест отсутствующего Action Class contract при свежем
service failure. Он подтверждает одновременно:

1. `selected_moves == []`;
2. `ACCEPT_WAKE` с `confirmed_service_failure` сохраняется;
3. execution boundary остаётся
   `STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED`;
4. Candidate, Packet и lease не созданы.

Выполнено:

```text
PYTHONPYCACHEPREFIX=/tmp/v7-pycache python3 -m unittest \
  tests.unit.test_v7_users_autoswitch_policy \
  tests.unit.test_service_failure_automation_evolution \
  tests.unit.test_operator_execution_packet

Ran 225 tests ... OK
```

## Legal terminal до deploy

`PRODUCTION_DEPLOY_AND_NON_TEST_OWNER_CALL_REQUIRED`.

Следующий допустимый шаг: safe deploy только `tools/v7-users-autoswitch`, затем
production read-only reconciliation. Если живое fresh L3 evidence действительно
подтверждено, существующий Authority owner сможет сформировать новый scope-bound
request; если нет, terminal остаётся `WAIT_FOR_FRESH_OWNER_BACKED_L3_WAKE`.
Ни L8, ни Production Maturity, ни routing/user scope этим исправлением не
изменяются.
