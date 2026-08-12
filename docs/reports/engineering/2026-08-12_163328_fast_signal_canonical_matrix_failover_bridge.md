# Быстрый сигнал отказа: канонический Matrix bridge

Дата: `2026-08-12`

## Причина

`v7-telegram-sentinel` уже выполнялся каждые четыре секунды, но только
обновлял компактный Telegram-статус в `service-matrix.json`. Канонический
source-bound `SERVICE_FAILURE_OBSERVED` / `SERVICE_FAILURE_REVALIDATED` event
создавал только полный `v7-service-matrix-refresh-all`, работающий раз в 15
минут. В результате existing governed consumer мог не получить свежий legal
event до следующего полного прохода.

Это общий producer-to-consumer gap, а не VLESS-специфичная проблема и не
условие восстановления исходного канала.

## Исправление

Расширен существующий `tools/v7-telegram-sentinel`:

```text
confirmed Telegram hard failure (existing 4 s sentinel)
-> existing tools/v7-service-matrix-test.update_matrix
-> canonical failure episode / source scope / event identity
-> existing v7-users-autoswitch.timer -> v7-governed-canary-dry-run-cycle
```

Sentinel не создаёт Candidate, Packet, lease, новый Planner, очередь, Runtime
или собственный event store. Он удерживает существующий matrix writer lock и
передаёт threshold-crossing (`bad_since`, `bad_for_seconds`) каноническому
Matrix owner. Следующий consumer остаётся существующим 20-секундным
`v7-users-autoswitch.timer` / governed executor: sentinel не запускает
длинный lifecycle синхронно и не создаёт новую периодику. Таким образом
persistence, recovery, incident identity и execution gates остаются у прежних
владельцев.

## Границы

- Нет policy write, Authority change, Production Maturity change.
- Нет route mutation и user movement внутри sentinel.
- Реальное действие возможно только позже через существующие active standing
  policy, target/capacity/freshness/cooldown/anti-flap, Candidate, Packet,
  lease, verification и rollback gates.
- CT-M0F controlled source не участвует в этом production producer bridge.

## Проверка

Фокусный набор: `11/11 PASS`.

Покрыто:

- проба выполняется вне matrix writer lock;
- confirmed fast failure публикуется только через существующий canonical
  Matrix event owner;
- healthy/degraded наблюдение не создаёт event bridge;
- threshold crossing не теряет время начала failure;
- bridge не выполняет Runtime effects.
- integration-проверка доказывает: подтверждённый fast signal создаёт один
  настоящий canonical `SERVICE_FAILURE_OBSERVED` с source-scope через
  существующий Matrix writer; это не synthetic event и не отдельный store.

## Следующий шаг

После commit/push/deploy production caller `v7-telegram-sentinel` должен
подтвердить: `CONFIRMED_FAILURE_PUBLISHED_TO_EXISTING_MATRIX_OWNER` для
нового реального signal; затем следующий existing 20-second governed consumer
должен принять созданный Matrix event. Никакой production failure не создаётся
ради этой проверки; все routing/user effects возможны только через уже
действующий standing policy, fresh Candidate/Packet/lease и live gates.

## Production verification

Deploy `80904026f4f62fbbf969ddf16fbe23b5598cbcdb` прошёл исключительно через
`tools/v7-safe-deploy`. Manifest и apply подтвердили единственный runtime-файл:
`/usr/local/bin/v7-telegram-sentinel`. Forbidden effects равны `false`:
policy/Authority/restore barrier, routing mutation и user movement не менялись.

Обычный production caller sentinel подтвердил реальный current signal для
канала `1` и создал один новый owner-backed canonical event:

```text
sfe_dd85b7f1edbd364f3f8106da4cf25530
-> SERVICE_FAILURE_OBSERVED
-> source_incident sfinc_b847db10feb643ecfdc8a475d539c5ef
-> READY_FOR_EXISTING_AUTOSWITCH_TIMER
```

Это не Natural L8 credit, не Candidate/Packet/lease и не user move. Local,
GitHub и production runtime согласованы на `80904026`; `truth` и
`convergence` вернули `PASS`, `GITHUB_ALIGNED`, `RUNTIME_ALIGNED`.

### Точный remaining blocker

Production `v7-users-autoswitch.timer` имеет состояние `enabled`, но
`inactive (dead)` с `2026-07-02`. Именно он является существующим ordinary
consumer, который должен передать новый canonical event в governed executor.
Поэтому fast producer и canonical event уже production-consumed, но следующий
action-capable consumer не будет запущен автоматически, пока timer не будет
операционно активирован.

Это не дефект Telegram/VLESS и не повод запускать новый timer, Planner или
direct apply. Active standing policy остаётся owner-backed и действует до
`2026-08-29`; её ordinary production runtime limit равен `4`, однако любой
реальный action по-прежнему требует fresh target/capacity/anti-flap/Candidate/
Packet/lease/verification/rollback gates.

**Legal terminal:**
`OPERATIONAL_TIMER_ACTIVATION_REQUIRED_FOR_EXISTING_GOVERNED_CONSUMER`.

**Exact re-entry:** existing operational/systemd owner activates only
`v7-users-autoswitch.timer`; then the next timer run consumes the already
published canonical event through the existing governed path. No new Authority,
policy write, manual Matrix run or synthetic event is required.
