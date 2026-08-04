# Engineering Report: CT recovery SLO ladder program update

Дата: 2026-08-04T16:27:15Z

## Результат

Существующая `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1` обновлена до
V4.4 без нового Program, Mission, owner, store, daemon, Planner, Runtime или
Authority-системы.

Прежний CT-M0F gate p95 <= 10 секунд и max <= 15 секунд сохранён только как
переходный ceiling. Его прохождение больше не может закрыть CT-M0F или считаться
целевой скоростью продукта. Оно обязано автоматически вернуть измеренный
latency residual в существующий CT-M0F engineering consumer.

## Обязательная лестница

1. Transitional legacy ceiling: p95 <= 10 s, max <= 15 s.
2. Legacy operational gate: detection p95 <= 2 s, decision plus route commit
   p95 <= 500 ms, route-bound client recovery p95 <= 3 s, max <= 5 s.
3. Prepared class/bucket target: validation plus kernel commit p95 <= 250 ms,
   visibility p95 <= 100 ms, route-bound client recovery p95 < 1 s.
4. p99 <= 5 s разрешено утверждать только после не менее 100 owner-backed
   observations; production actions нельзя создавать ради заполнения
   percentile.

## Внешний benchmark-контекст

- IETF RSVP-TE Fast Reroute проектирует локальное переключение за десятки
  миллисекунд: https://www.rfc-editor.org/rfc/rfc4090
- Juniper приводит BFD detection около 200 ms для 50 ms interval и multiplier
  3: https://www.juniper.net/documentation/us/en/software/junos/high-availability/topics/topic-map/bfd.html
- FortiGate SD-WAN default health detection соответствует примерно 500 ms x 5
  failures: https://docs.fortinet.com/document/fortigate/7.4.2/cli-reference/77620/config-system-sdwan
- Google Cloud Router BFD default detection — 5 s:
  https://docs.cloud.google.com/network-connectivity/docs/router/concepts/bfd
- Cisco Catalyst SD-WAN default BFD failure detection — 7 s:
  https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/ha-scaling/ios-xe-17/high-availability-book-xe/m-high-availability-and-scaling.html

Эти значения в основном измеряют detection или route cutover. V7 сохраняет
более строгий end-to-end terminal: первый успешный exact route-bound client
traffic probe.

## Evidence и effect boundary

Это изменение обновляет только программу и live sequencing contract. Оно не
измеряет текущую скорость, не выполняет production transaction, не создаёт
Candidate/Packet/lease, не пишет restore barrier, не двигает пользователей, не
расширяет Authority и не меняет Production Maturity.

Текущий exact successor остаётся `CT-M0F-E_ENGINEERING`; CT-M0F-V и CT-M1
остаются dependency-blocked.

Terminal изменения:
`CT_RECOVERY_ORDERED_SLO_LADDER_CONTRACT_UPDATED`.
