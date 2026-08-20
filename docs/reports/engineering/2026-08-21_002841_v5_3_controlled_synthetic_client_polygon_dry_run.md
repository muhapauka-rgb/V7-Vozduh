# V5.3: controlled synthetic-клиент на свободном VLESS-канале — Polygon/dry-run

Дата: 2026-08-21 00:28 MSK  
Mission: `V7_COMPLETE_HEALTH_TEST_STABILITY_SYSTEM_ATLAS`  
Track: `V5_3_T0_T11_LATENCY_OPTIMIZATION`  
Класс результата: Engineering Polygon / read-only dry-run; production не изменялся.

## SUMMARY

Проверена идея использовать свободный VLESS-канал со специально созданными клиентами как отдельную тестовую группу. В системе уже есть официальный controlled-topology механизм; новый owner, новый клиентский реестр или новый источник истины не понадобились.

Механизм допускает только явно помеченную `certification_user` identity, проверяет уникальность и принадлежность к controlled-пулу, не смешивает её с обычными клиентами и не выдаёт ей обычное доверие. При отсутствии корректной controlled identity или при наличии обычных клиентов на источнике он останавливается безопасно.

## EXECUTED_EVIDENCE

Запущены существующие тесты governed dry-run/controlled topology: **11/11 PASS**.

Проверено:

* повторное использование registry-marked certification identity;
* отказ для обычной, неподтверждённой identity;
* требование пустого controlled source;
* запрет фабрикации trust/learning для synthetic-клиента;
* обновление существующего snapshot owner после reservation;
* повторная проверка exact active manifest и продолжение той же кампании;
* восстановление потерянного terminal из истины существующего owner;
* сохранение action-class при cleanup/reset;
* bounded execution timing через существующий owner;
* read-only preflight provisioned substrate.

Дополнительно подтверждено ранее в T0–T11 Polygon: 17/17 тестов Matrix/service-failure caller chain PASS.

## WHAT_THIS_PROVES

Synthetic-клиенты пригодны для controlled проверки:

1. T5 — существующий planner/controlled-topology owner выбирает identity;
2. T6 — target readiness и reservation проверяются до действия;
3. T7–T9 — bounded decision, safety gates и stop-safe при противоречии;
4. T10 — governed dry-run имеет существующую timing-разбивку, включая `apply_route_visibility_and_verification`;
5. T11 — verification/cleanup lineage восстанавливается через existing owner.

Это инженерное доказательство механизма, а не production-результат и не естественное поведение обычных клиентов.

## WHAT_WAS_NOT_DONE

Фактический перенос клиента с VLESS на другой production-канал не выполнялся. Не выполнялись route mutation, autoswitch apply, deploy, push и изменение реального Runtime.

Причина: текущий развёрнутый Runtime (`0d8729a109...`) не совпадает с локальным кодом (`972c4f86c1...`), а текущий T0–T11 блок разрешает только Polygon/read-only evidence. Наличие именно указанной пользователем свободной VLESS-группы в live registry этим запуском не подтверждалось.

## SAFETY_RESULT

* `users_moved=0` в выполненных dry-run/Polygon проверках;
* ordinary users не использовались;
* synthetic evidence не повышает production trust и не закрывает natural-production criteria;
* full Matrix fallback, persistence, freshness и Authority gates не изменены.

## PLAN_POSITION_AND_NEXT_ACTION

Позиция плана: **T0–T11 evidence model → controlled synthetic topology proven in Polygon → Runtime span reconciliation pending → safe optimization options**.

Точный следующий шаг: существующему Matrix/Autoswitch owner выполнить read-only проверку live registry на наличие отдельной `certification_user` группы на VLESS и совпадение Runtime/local provenance. Если группа подтверждена и есть разрешённое controlled-окно, следующий блок может запустить только existing governed dry-run с измерением T10–T11; обычные клиенты и маршруты не затрагивать.

Owner: existing controlled-topology / Matrix / Autoswitch owners.  
Consumer: `continue_omp_engineering_control_loop`.  
Re-entry: подтверждённая live certification identity + совпадающий Runtime или отдельное разрешённое controlled evidence-окно.

## SOURCES

* `tools/v7-governed-canary-dry-run-cycle`
* `tools/v7-users-autoswitch`
* `tests/unit/test_governed_canary_cli.py`
* `docs/programs/V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM.md`
* `docs/reports/engineering/2026-08-21_001432_v5_3_t0_t11_polygon_runtime_latency_model.md`

