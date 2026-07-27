# Active Incident: автоматический drain и reconciliation Missions

Дата: `2026-07-27/28`  
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Статус: `ACTIVE_DRAIN_RUNTIME_CONSUMED; incident remains open`

## Новое owner-backed доказательство

Production `v7-service-matrix-refresh.timer` самостоятельно выполнил три
последовательных Tier-1 транзакции одного continuing VLESS incident. Между
ними не было команды оператора или Codex, запускающей Matrix:

| Цикл | Production feedback | Результат |
| --- | --- | --- |
| N | `execfb_141f921bc6f2a593eab6312a` | один fresh governed user outcome, затем passive + OMP consumer |
| N+1 | `execfb_b7731405789f6127df1cdddf` | следующий Matrix cycle сам прошёл Observation → OMP → fresh Packet/lease → verification → Outcome/Learning → successor |
| N+2 | `execfb_280dd6712e37aceccbcc5bfb` | следующий штатный cycle `19:56:23–19:59:17 MSK` завершил ещё одну одиночную governed transaction |

Каждая транзакция остаётся ограниченной существующей standing policy:
`max_users=1`, `max_concurrent_transactions=1`, fresh Situation/Candidate/
Packet/lease и live gates. Ни batch, ни Authority expansion, ни promotion
tier не появились.

Source-CPS bridge read-only потребил N+1 и N+2 после их production terminal.
Current owner-backed scope:

```text
affected=31
protected=1
unresolved=30
excluded_or_recovered=0
next consumer=tools/v7-service-matrix-refresh-all
re-entry=enabled v7-service-matrix-refresh.timer
```

Инвариант scope соблюдён: `31 = 1 + 30 + 0`. `PENDING_WAKE_ID=NONE` и
`REENTRY_ACTIVE_LEASE=NONE`: Codex не удерживает operational execution.

## Статус исполнимой карты

| Mission | Текущее честное состояние |
| --- | --- |
| M0–M2 | ранее production-consumed: compact dual lifecycle, exact-once receipt и successor linkage работают |
| M3 | `BOUNDED_AUTOMATIC_INCIDENT_DRAIN_RUNTIME_CONSUMED`: доказаны N → N+1 → N+2 без ручного запуска Matrix |
| M4 | dynamic residual: нет нового `STOP_SAFE` с engineering responsible link; корректные terminals не создают BDP churn |
| M5 | `MISSION_NOT_REQUIRED_FOR_CURRENT_PASS`: отсутствует unresolved engineering cell; Polygon не дублирует работающий production path |
| M6 | current path production-proven тремя fresh bounded outcomes |
| M7 | новые Outcome feedback потреблены существующими outcome/feedback owners; tier остаётся `HOLD_CURRENT_TIER=1`, без неявного promotion |
| M8 | CPS/runtime/OMP pointers owner-backed и aligned |
| M9 | existing exact-once/duplicate/stale-lease/policy tests прошли; production сохраняет serial-only boundary, без concurrency expansion |
| M10 | `PARTIAL_ACTIVE_DRAIN`: implementation path принят, но общий terminal ещё недопустим, пока `unresolved_scope=30` |

## Проверка M9

Запущены существующие focused suites: service-failure evolution/episode,
external and event-driven reentry, real-consumer heartbeat, production
certification и policy design. Все прошли. Они покрывают duplicate suppression,
atomic wake lifecycle, stale lease recovery, single-flight и strict serial
policy. Никакой runtime mutation этим тестом не выполнялась.

## Exact next frontier

`CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN`.

Это не ожидание новой аварии: тот же unrecovered incident сам revalidates через
existing Matrix timer. Program не объявляется завершённой искусственно —
remaining 30 source-scope пользователей будут обрабатываться только по одному,
только при fresh current gates, до `CURRENT_SOURCE_SCOPE_EMPTY`, verified
source recovery или exact live blocker.
