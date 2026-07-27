# Активация standing policy и production re-entry

Дата: 2026-07-27

Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

## Результат Authority decision

Пользователь независимо одобрил точный production request:

- request: `sdpauth_r1_906f2d2515016198d4c47727`;
- hash:
  `906f2d2515016198d4c47727cc1c5fafcff391408b1627174645ea3c1d450b54`;
- решение: `APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY`.

Существующий owner `admin_core/operator_execution.py` один раз записал
standing contract:

- contract: `sdpc_f200a060c720a12669248105`;
- contract hash:
  `f200a060c720a1266924810589c25b01dc077c1385cd1260e79dab86bb6101fd`;
- status: `ACTIVE`;
- issued: `2026-07-26T17:21:00.971884+00:00`;
- expires: `2026-08-25T17:21:00.971884+00:00`;
- decision:
  `sdpdec_bace9b52fc8e391d2ed02f6c`;
- policy scope hash:
  `f610dbd87f9d8e5b63d69538138340ace04c9799ac42ebedd205206eee9f723e`.

Активация сама не создала Candidate, Packet или lease и не выполнила apply,
routing mutation или user movement.

## Fresh production re-entry

Реальный `tools/v7-service-matrix-refresh-all` owner-cycle выполнил семь
канальных проверок, passive consumer и advisory consumer. Fresh bounded
consumer сформировал рекомендацию для `10.0.0.2`, `vless ->
wireguard-1779454504-c43409`, но не получил готовый Packet и законно завершился:

- final verdict: `GOVERNED_TRANSACTION_STOPPED`;
- transaction status: `STOP_SAFE`;
- stop reason: `packet_not_ready`;
- apply: `false`;
- restore-barrier write: `false`;
- routing mutation: `false`;
- users moved: `0`;
- final safe mode: `OPEN`.

Это правильный продуктовый terminal: standing policy устранила ручное
подтверждение, но не обошла planner, Packet materialization или live gates.

## Найденный producer-consumer defect

Production re-entry обнаружил две ошибки классификации в существующем
`tools/v7-service-matrix-refresh-all`:

1. `GOVERNED_TRANSACTION_STOPPED` с `transaction_status=STOP_SAFE` ошибочно
   проецировался как wrapper `FAILED`.
2. Законный OMP terminal `NO_PENDING_OBLIGATION` ошибочно считался liveness
   failure.

Это существующий-owner engineering defect. Authority, Runtime, Planner,
Packet owner, registry, watcher или queue не добавлялись.

## Исправление и тесты

Wrapper теперь принимает `GOVERNED_TRANSACTION_STOPPED/STOP_SAFE` только при
`apply=false` и `users_moved=0`; настоящий неизвестный/опасный terminal
по-прежнему fail closed. OMP `NO_PENDING_OBLIGATION` признан успешным
идемпотентным no-op terminal.

- focused affected campaign: `137 tests PASS`;
- compile: `PASS`;
- diff check: `PASS`.

## Текущий terminal

Первый repair был задеплоен:
`deploy-z8-14-Updatesystem-c52618a-20260727T002636`. Affected production
replay подтвердил:

- OMP consumer: `PASS / NO_PENDING_OBLIGATION`;
- bounded consumer: `PASS / STOP_SAFE`;
- apply `false`, restore barrier `false`, users moved `0`, final `OPEN`.

Replay также доказал следующий точный predecessor gap:

```text
Service Matrix writes fresh observations
-> bounded executor builds decision surface from old snapshots
-> planner refreshes snapshots
-> executor keeps consuming the pre-refresh surface
-> snapshot_mismatch:risk-summaries
-> permanent packet_not_ready
```

Существующий `v7-intelligence-snapshot-refresh` owner уже реализован. Bounded
delegated path теперь вызывает его через существующий autoswitch
`--pre-planner-refresh write`, после чего заново читает decision surface и
Learning inventory перед Candidate/Packet gates. Никакие пороги, Authority,
failure classes или safety gates не ослаблены.

Повторная focused affected campaign: `138 tests PASS`.

`SNAPSHOT_PREDECESSOR_REPAIR_READY_FOR_SAFE_DEPLOY_AND_AFFECTED_PRODUCTION_REPLAY`

## Проверка длительного запуска и итоговая классификация

После deploy snapshot-predecessor repair реальный production owner-cycle был
завершён. Локальный получатель его большого JSON-ответа оставался ждать поток,
что выглядело как зависание, но runtime-процесс уже завершился; его безопасно
прервали только на локальной стороне. Это не restart, не timeout и не
незавершённая production-транзакция.

Durable production summary подтвердил, что snapshot defect устранён: Packet
preview стал `READY`, а bounded executor дошёл до законной event gate. Он
остановился без effects, потому что для активного standing contract отсутствует
**fresh matching service-failure event**:

- `final_verdict=GOVERNED_TRANSACTION_STOPPED`;
- `transaction_status=STOP_SAFE`;
- `stop_reason=delegated_policy_admission_denied`;
- blocker=`FRESH_MATCHING_SERVICE_FAILURE_EVENT_MISSING`;
- apply / restore barrier / routing mutation=`false`, users moved=`0`.

Это не повторный запрос Authority и не packet defect. Active standing contract
`sdpc_f200a060c720a12669248105` остаётся действующим в пределах исходного
scope. Следующий допустимый вход — только owner-backed новый matching service
failure; он запускает fresh Candidate → Packet → lease → live verification
через существующий bounded executor.

При проверке обнаружен один безопасный semantic producer-consumer gap:
advisory/OMP consumer продолжал смотреть на устаревший one-use contract и
неправильно публиковал `...AUTHORITY_RECONCILIATION`, хотя исполнитель уже
правильно видел active standing policy. Исправление переводит именно этот
случай в `STOP_SAFE_FRESH_EVENT_REVALIDATION_REQUIRED` и
`V7_SERVICE_FAILURE_AUTOMATION_FRESH_EVENT_REVALIDATION`; оно не создаёт
Candidate, Packet, lease или Authority request и не изменяет execution gates.

Focused affected verification после исправления: **139 tests PASS**, compile
и diff-check: **PASS**. Следующий шаг — обычный safe deploy этого
producer-consumer semantic repair и affected production replay; ожидаемый
terminal при отсутствии нового failure: `WAIT_FOR_FRESH_MATCHING_SERVICE_FAILURE_EVENT`.

## Закрытие repair

Repair задеплоен штатным `tools/v7-safe-deploy` как
`deploy-z8-14-Updatesystem-f53ad20-20260727T091319`. Manifest подтвердил
единственную runtime-замену: `tools/v7-users-autoswitch`; рестарт,
policy-write, restore barrier, apply, routing mutation и user movement не
выполнялись.

Production non-test caller существующего consumer вернул `PASS` и
`no_unmaterialized_passive_terminal`, сохранив все forbidden effects нулевыми.
Это корректный affected replay при отсутствии свежего matching failure: repair
установлен и доступен, но не создаёт событие для его искусственной проверки.

Итоговые truth и convergence: `PASS / FULLY_ALIGNED`, commit local/GitHub/
production runtime: `f53ad20bc79e791a0be1a5f823149a20bbf1118f`.
