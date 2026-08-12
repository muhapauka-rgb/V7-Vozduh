# Быстрый сигнал отказа: канонический Matrix bridge

Дата: `2026-08-12`

## Причина

`v7-telegram-sentinel` уже выполнялся каждые четыре секунды, но только
обновлял компактный Telegram-статус в `service-matrix.json`. Канонический
source-bound `SERVICE_FAILURE_OBSERVED` / `SERVICE_FAILURE_REVALIDATED` event
создавал только полный `v7-service-matrix-refresh-all`, работающий раз в 15
минут. В результате существующий governed failover consumer мог не получить
свежий legal event до следующего полного прохода.

Это общий producer-to-consumer gap, а не VLESS-специфичная проблема и не
условие восстановления исходного канала.

## Исправление

Расширен существующий `tools/v7-telegram-sentinel`:

```text
confirmed Telegram hard failure (existing 4 s sentinel)
-> existing tools/v7-service-matrix-test.update_matrix
-> canonical failure episode / source scope / event identity
-> existing Matrix + autoswitch + governed L3 consumer
```

Sentinel не создаёт Candidate, Packet, lease, новый Planner, очередь, Runtime
или собственный event store. Он удерживает существующий matrix writer lock и
передаёт threshold-crossing (`bad_since`, `bad_for_seconds`) каноническому
Matrix owner. Таким образом persistence, recovery, incident identity и
следующий consumer остаются у прежних владельцев.

## Границы

- Нет policy write, Authority change, Production Maturity change.
- Нет route mutation и user movement внутри sentinel.
- Реальное действие возможно только позже через существующие active standing
  policy, target/capacity/freshness/cooldown/anti-flap, Candidate, Packet,
  lease, verification и rollback gates.
- CT-M0F controlled source не участвует в этом production producer bridge.

## Проверка

`tests.unit.test_telegram_sentinel_lock_scope`: `11/11 PASS`.

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
подтвердить: `CONFIRMED_FAILURE_PUBLISHED_TO_EXISTING_MATRIX_OWNER` при
реальном безопасном signal, затем обычный governed consumer должен принять
созданный Matrix event. Никакой production failure не создаётся ради этой
проверки; при отсутствии такого сигнала bridge остаётся готовым, а CT-M0F
продолжается отдельно.
