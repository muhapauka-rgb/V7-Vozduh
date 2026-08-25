# V7 Runtime contention and multi-cohort failover experiment — Polygon baseline

Дата: 2026-08-26 01:07 MSK  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Mission: `V7_RUNTIME_CONTENTION_AND_MULTI_COHORT_FAILOVER_EXPERIMENT`

## Терминальный статус этого блока

`POLYGON_BASELINE_CONSUMED_PRODUCTION_LANE_EXTERNAL_RESOURCE_BLOCKED`

Полный production эксперимент с controlled source failure не закрыт: в текущем
пуле нет второго здорового изолированного источника с необходимой ёмкостью, а
общие источники нельзя ломать даже для теста, поскольку на них находятся обычные
клиенты. Поэтому результаты ниже — честное server-side Polygon измерение
существующего owner, а не production failover credit.

## Что проверено

- штатный `controlled_source_topology_diagnostic` (read-only);
- действующие reservation/Authority owners;
- существующий V4 bounded-cohort contract;
- существующий N9 scale harness;
- deployed `tools/v7-users-autoswitch` без изменения Runtime.

Добавлена только append-only запись one-user substrate request через существующий
Authority owner (`cpsauth_r1_f6e77c6...`); это не расширяет Authority и не
разрешает multi-cohort эксперимент.

## Production preflight

| Проверка | Результат |
|---|---|
| Изолированный `amneziawg-exec-20260528-10-8-1-14` | здоров, но уже занят одним CT-M0F identity и имеет reservation `n10-20260823-1508`; campaign group не совпадает |
| Пустой `1` | ordinary=0, reservation dry-run проходит, но Matrix/quality состояние FAIL, поэтому controlled failure baseline невалиден |
| `awg0`, `awg3` | здоровы, но shared с обычными клиентами; fault injection запрещён |
| `wireguard-1779454504-c43409`, `openvpn-1779388847-d2ad7c`, `vless` | shared/failed/expired либо не имеют безопасной изоляции |
| Готовые dedicated drafts | hard capacity 2; не дают cohort 10/100/300 |
| `v7-health.service` | `active` |
| standalone Matrix/Telegram timers | `inactive` |
| deployed product hashes | совпадают с локальными: autoswitch `9585b60f…`, operator_execution `28d6164c…` |
| users/egress/Matrix fingerprints | до и после harness не изменились |

## Server-side Polygon measurements

Harness вызывал только существующий чистый
`build_service_failure_adaptive_cohort_contract`; не создавал Candidate, Packet,
Lease, reservation, route, assignment или Matrix generation.

| Запрошенный cohort | Фактически допущен | Статус | Время, ms | Peak allocation |
|---:|---:|---|---:|---:|
| 1 | 1 | MOVE_READY | 1.200 | 10,058 B |
| 10 | 10 | MOVE_READY | 1.285 | 15,427 B |
| 100 | 48 | MOVE_READY, bounds ограничивают | 7.624 | 72,891 B |
| 300 | 48 | MOVE_READY, верхний bound 48; остальные остаются вне текущего execution scope | 11.960 | 151,291 B |

Для 100/300 лимит 48 определяется одновременно текущими generic/adapter,
Authority, Runtime, verification, rollback и request bounds. Это подтверждает
fail-closed поведение: система не считает 100/300 исполненными, когда текущий
контракт допускает только 48.

### Contention series

Один и тот же deployed owner, cohort=300, только Polygon projection:

| Одновременных вызовов | Wall, ms | Сумма вызовов, ms | Max вызов, ms | Все effective=48 |
|---:|---:|---:|---:|---|
| 1 | 11.597 | 9.983 | 9.983 | да |
| 2 | 23.940 | 34.997 | 21.931 | да |
| 4 | 44.168 | 68.643 | 28.935 | да |
| 8 | 92.677 | 216.214 | 34.798 | да |

Это измеряет contention внутри чистой projection-функции на текущем сервере;
оно не является T0→S11 и не доказывает route/client recovery.

## Existing N9 Polygon scale gate

`python3 -m unittest tests.unit.test_v5_3_n9_full_scale_tournament` — **5/5 PASS**.
Проверены сетки 7/50/100/1000 egress и 250/500/10,000 synthetic users,
профили one/few/many, bounded probes, compact prepared projection и hard-owner
one-second gate. Это подтверждает готовность Polygon data-plane projection,
но не заменяет production multi-cohort failover.

## Invariants

- ordinary user movement: `0`;
- route/kernel changes: `0`;
- Candidate/Packet/Lease: `0`;
- Matrix/Planner/Authority semantics: unchanged;
- Runtime product code: unchanged;
- temporary harness: удалён локально и на сервере;
- no fabricated production timing or SLO credit.

## Exact remaining blocker

Для Phase A/Phase B требуется owner-backed healthy isolated source topology:
минимум два независимых certification-only source (для variance/independent
failure), а для заявленных cohort 100/300 — capacity contract не меньше этих
размеров либо отдельное явно admitted narrowing mission. Ни один текущий
источник не удовлетворяет всем условиям одновременно. Создание нового
внешнего peer/config/egress не является локальной операцией и не может быть
выведено из существующих draft metadata.

## Следующий шаг в общей программе

`V7_RUNTIME_CONTENTION_AND_MULTI_COHORT_FAILOVER_EXPERIMENT` остаётся на
production preflight. Следующий допустимый successor — принять через
существующий admin/v7-admin-api egress-draft lifecycle owner минимум два
здоровых изолированных certification sources, проверить их capacity/fresh
Matrix/rollback, затем автоматически вернуться к Phase A (quiet/moderate/
back-to-back) и Phase B (1/10/100/300). До появления такого ресурса дальнейший
source-failure запуск был бы либо опасным для обычных клиентов, либо невалидным
доказательством.
