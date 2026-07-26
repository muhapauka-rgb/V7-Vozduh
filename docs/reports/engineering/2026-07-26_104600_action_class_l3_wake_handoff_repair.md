# Отчёт: устранение разрыва Action Class → L3 wake

Дата: 2026-07-26  
Статус: `IMPLEMENTED_PENDING_SAFE_DEPLOY`

## Что обнаружено

Штатная read-only сверка `tools/v7-users-autoswitch --action-class-contract-reconciliation-only`
создавала готовый к выдаче one-use Action Class request при наличии свежего shadow Candidate.
После выдачи policy contract тот же существующий autoswitch consumer мог отказать до
создания Candidate/Packet/lease с `confirmed_l3_wake_required`.

Это не разрешало небезопасный apply: перемещений, Packet, lease, rollback и изменения
Production Maturity не было. Но это был реальный producer → consumer handoff defect:
короткоживущий contract мог быть выдан и истечь, хотя необходимый event-driven L3 wake
уже отсутствовал.

## Исправление

В существующем owner `tools/v7-users-autoswitch` Action Class reconciliation теперь
включает `safety.l3_wake` в issue preflight:

- если L3 контекст присутствует и `accepted != true`, request получает точный blocker
  (в production: `confirmed_l3_wake_required`);
- статус становится
  `ACTION_CLASS_CONTRACT_REQUEST_TEMPLATE_WAITING_FRESH_PRECONDITIONS`;
- policy owner не получает request, который consumer заранее не сможет применить;
- для не-L3 Action Class путей поведение не меняется.

Добавлен regression test на rejected L3 wake.

## Проверка

Выполнено локально:

```text
PYTHONPYCACHEPREFIX=/tmp/v7-pycache python3 -m unittest \
  tests.unit.test_service_failure_automation_evolution \
  tests.unit.test_v7_users_autoswitch_policy \
  tests.unit.test_operator_execution_packet

Ran 224 tests — OK
```

До исправления production evidence показал:

- coherent snapshot refresh: `PASS`, общий service-matrix lock удержан;
- один конкретный shadow move `10.0.0.2: vless → wireguard-1779454504-c43409`;
- issued contract `acc_2587f87703d8f2bb68c82dbc`;
- execution boundary: `STOP_SAFE_OTHER_EXECUTION_GATE_REQUIRED`;
- exact blocker: `confirmed_l3_wake_required`;
- `users_moved=0`, Packet/lease отсутствуют, contract не consumed.

## Законный terminal

До deploy: `IMPLEMENTED_PENDING_SAFE_DEPLOY`.

После deploy требуется повторить read-only reconciliation и подтвердить, что при
отсутствующем/просроченном L3 wake policy issue request не формируется. Следующий
runtime frontier остаётся existing owner-backed `confirmed current L3 wake` или
Automation Gap Closure; старый contract, Packet и restore-barrier identity не могут
быть переиспользованы.
