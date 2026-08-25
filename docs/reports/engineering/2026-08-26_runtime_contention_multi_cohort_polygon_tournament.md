# V7 Runtime contention and multi-cohort failover — Polygon tournament

Дата: 2026-08-26 01:31 MSK  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Mission: `V7_RUNTIME_CONTENTION_AND_MULTI_COHORT_FAILOVER_EXPERIMENT`

## Терминальный статус этого Polygon-блока

`POLYGON_CONTENTION_AND_MULTI_COHORT_TOURNAMENT_CONSUMED`

Внешнего второго/третьего изолированного egress-источника сейчас нет. Вместо
ожидания выполнен полный безопасный Polygon tournament на **уже развёрнутых**
owners: V4 adaptive cohort contract, N9 prepared projection и hard-failure
owner. Это не выдаётся за production failover: Matrix, Candidate, Packet,
Lease, route/kernel и обычные клиенты не затрагивались.

## Неизменность и границы опыта

| Проверка | Результат |
|---|---|
| Product fingerprint `v7-users-autoswitch` | `9585b60fa882ae786754a46a37770b2d5ec4a7a2c6dcfd7dab42a368d709a3d9` |
| Локальный commit перед опытом | `740399021f16f5be0e4dd211afd70a0845549784` |
| `v7-health.service` | штатно продолжал работать; harness его не вызывал |
| Standalone Matrix/Telegram timers | остаются выключенными по текущему lifecycle |
| Изменение Authority | нет |
| Изменение Runtime, route или kernel | нет |
| Изменение assignment или обычных клиентов | нет / 0 |

Каждый вызов использовал отдельный временный state directory. Hard-owner
fixture запускал definitive Matrix command `/bin/false` только внутри этого
временного состояния; он не создавал реального incident и не писал canonical
Matrix.

## Phase A — contention при одной готовой группе из 10 synthetic members

Для каждого режима сделано пять независимых запусков. P95 для пяти точек —
самая медленная точка (nearest-rank).

| Режим | Параллельных вызовов | Интервал | Wall, ms (5 запусков) | Median, ms | P95, ms | Max hard-owner, ms | Все 10 допущены |
|---|---:|---:|---|---:|---:|---:|---|
| Quiet | 1 | 250 ms | 211.546, 158.832, 131.344, 188.360, 156.403 | 158.832 | 211.546 | 206.124 | да |
| Moderate | 2 | 50 ms | 248.416, 274.043, 276.013, 264.620, 255.221 | 264.620 | 276.013 | 269.616 | да |
| Back-to-back | 4 | 0 ms | 383.009, 403.364, 450.377, 431.789, 414.415 | 414.415 | 450.377 | 444.758 | да |

При четырёх одновременных вычислениях server-side wall P95 вырос с 211.546 до
450.377 ms (2.13×). Это измеренный bounded contention текущего process-based
Polygon fixture, а не задержка переключения клиента.

## Phase B — 1/2/3 source и cohort 1/10/100/300

Для каждого из 12 случаев измерены два режима.

- **Current policy exact** — настоящие текущие bounds. Для total больше 48
  owner fail-closed допускает только 48, не делая вид, что выполнены 100–900.
- **Mechanism shadow** — тот же существующий алгоритм без Authority/route/
  Runtime прав: только вычислительная оценка масштаба, не policy credit и не
  разрешение на реальный multi-cohort failover.

`projection / contract / hard` — миллисекунды соответственно для prepared
projection, adaptive cohort contract и hard-owner fixture.

| Sources × cohort | Total | Exact effective | Exact projection / contract / hard, ms | Shadow effective | Shadow projection / contract / hard, ms |
|---|---:|---:|---|---:|---|
| 1 × 1 | 1 | 1 | 0.244 / 0.205 / 104.436 | 1 | 0.248 / 0.227 / 151.937 |
| 1 × 10 | 10 | 10 | 0.411 / 0.262 / 102.982 | 10 | 0.468 / 0.214 / 126.626 |
| 1 × 100 | 100 | 48 | 3.189 / 1.068 / 99.086 | 100 | 3.093 / 1.896 / 132.741 |
| 1 × 300 | 300 | 48 | 16.951 / 1.870 / 126.882 | 300 | 9.038 / 2.254 / 129.870 |
| 2 × 1 | 2 | 2 | 0.216 / 0.156 / 99.225 | 2 | 0.215 / 0.170 / 172.602 |
| 2 × 10 | 20 | 20 | 0.847 / 0.423 / 168.308 | 20 | 0.747 / 0.351 / 194.442 |
| 2 × 100 | 200 | 48 | 29.142 / 1.960 / 141.459 | 200 | 19.741 / 4.499 / 108.238 |
| 2 × 300 | 600 | 48 | 17.767 / 3.014 / 134.234 | 600 | 23.263 / 8.344 / 151.167 |
| 3 × 1 | 3 | 3 | 0.252 / 0.156 / 112.773 | 3 | 0.253 / 0.249 / 138.397 |
| 3 × 10 | 30 | 30 | 0.977 / 0.416 / 187.135 | 30 | 2.142 / 0.390 / 101.445 |
| 3 × 100 | 300 | 48 | 13.151 / 3.840 / 149.455 | 300 | 15.056 / 4.029 / 112.848 |
| 3 × 300 | 900 | 48 | 40.088 / 6.617 / 185.526 | 900 | 44.763 / 8.572 / 134.806 |

### Нагрузка процесса

На наибольшем shadow случае (3 × 300 = 900) процесс занял 39.710 ms user CPU,
0.791 ms system CPU и 31,132 KiB peak RSS. Наибольшие значения по всей серии:
39.710 ms user CPU, 1.068 ms system CPU и 31,132 KiB RSS. Наблюдаемая очередь
планировщика во время серии составляла 3–7 runnable задач; это контекст
измерения, а не доказательство причинности.

## Что это доказывает

1. Текущий owner сохраняет safety: фактический policy scope не расширяется
   выше 48, даже когда Polygon предъявляет 100–900 synthetic identities.
2. Его подготовленная projection и cohort contract сами по себе не имеют
   многосекундной стоимости: максимум shadow — 44.763 ms и 8.572 ms.
3. Даже с fixture hard-owner максимум здесь 194.442 ms. Следовательно,
   ранее измеренный секундный residual реального HARD_PATH нельзя объяснить
   одной лишь разбивкой клиентов по группам или линейным ростом cohort logic.
4. В четырёх параллельных Polygon вызовах есть измеримый contention, но его
   server-side уровень остаётся ниже полусекунды в данном безопасном опыте.

## Что опыт намеренно не доказывает

Он не доказывает один, два или три **реальных** source failures, не подтверждает
T0→S11, readiness внешней capacity, Candidate/Packet/Lease/Apply, фактическое
восстановление трафика или production SLO. Для этого нужен независимый healthy
certification egress topology; его локально и безопасно создать из отсутствующих
внешних VPN endpoint/credentials нельзя.

## Проверки

`python3 -m unittest tests.unit.test_v5_3_n9_full_scale_tournament` — **5/5 PASS**
(6.372 s). Она покрывает Polygon scale grid 7/50/100/1000 egress и
250/500/10,000 synthetic users и подтверждает, что использованный N9 scale
контракт не регрессировал.

## Следующий шаг программы

Этот много-групповой Polygon-блок закрыт без ожидания внешних событий.
Следующий точный frontier: использовать зафиксированный результат при
диагностике оставшегося HARD_PATH residual — измерять существующими Polygon
owners Matrix/prepared-decision process/lock spans, а не запускать новый
cohort/scale design или менять Runtime. Реальный multi-source failover остаётся
отдельным production-evidence lane до появления owner-backed изолированных
здоровых sources; это не даёт права подменять его shared каналами или
ручным выбором target.

