# V5.3 T0–T11: timing breakdown и подтверждённое узкое место

Дата: 2026-08-21 02:05 MSK  
Track: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Блок: измерение времени, без изменения production

## Короткий вывод

Измерение завершено на трёх уровнях:

1. существующий synthetic governed T0–T11 на Polygon;
2. существующий short/full Matrix comparison на изолированном Polygon;
3. последний реальный полный Matrix cycle на `v7-vps`.

Подтверждено:

- synthetic Candidate → Packet → Lease → Barrier → Apply/Verification →
  Feedback занимает `23.675 ms` в тестовом fixture;
- short Matrix для 3 обязательных сервисов вместо полного набора из 14
  сокращает проверки `14 → 3` (`78.6%`) и измеренное время в Polygon примерно
  `49.868 ms → 21.868 ms` (`56.1%`);
- последний production full Matrix занял `85.675 s` по lifecycle payload и
  `87.192 s` wall clock;
- плановое ожидание между запусками Matrix (`15 min + до 60 s jitter`) намного
  больше времени самого probe.

Это не даёт права менять cadence или обходить full fallback. Short-result
остаётся advisory, full Matrix — финальным canonical observation, а при
отсутствии свежего exact certification context действие запрещено.

## 1. Synthetic T0–T11 timing

Прогон выполнен через существующий
`tools/v7-governed-canary-dry-run-cycle` в временном Polygon fixture. Apply был
stub только внутри fixture; production route и users не использовались.

| Этап | Время |
|---|---:|
| planner / selection | `10.928 ms` |
| packet and lease | `5.795 ms` |
| restore barrier | `3.802 ms` |
| apply and verification (stub) | `0.070 ms` |
| feedback and learning | `3.079 ms` |
| **итого** | **`23.675 ms`** |

Самый большой synthetic span — planner (`46.2%`), но эти значения не являются
production latency: сетевые вызовы и реальный apply заменены controlled fixture.
Выполненный результат: `GOVERNED_TRANSACTION_COMPLETED`, один synthetic user
внутри временной модели, terminal lease и cleanup подтверждены.

## 2. Polygon short/full Matrix

Пять пар запусков выполнены в отдельных процессах на локальном controlled
response surface. Полный вариант проверял 14 сервисов, короткий —
`telegram,google,google_auth` (3 сервиса). Writer оставался существующим,
cross-egress parallelism не включался.

| Вариант | Диапазон | Среднее | Проверки |
|---|---:|---:|---:|
| Full | `47.558–54.694 ms` | `49.868 ms` | `14` |
| Short | `20.639–23.054 ms` | `21.868 ms` | `3` |

Измеренное сокращение:

- количество проверок: `78.6%`;
- время controlled probe: `56.1%`.

Эквивалентность healthy-path и required-service failure подтверждена
существующим suite: `14/14 PASS`. Methodology-limit (`HTTP_LIMITED`) не
превращается в ложный failure. Full fallback выполняется всегда и остаётся
финальным наблюдением.

## 3. Последний production Matrix cycle

Read-only journal на `v7-vps`:

| Поле | Факт |
|---|---|
| Start | `2026-08-21 02:01:58 MSK` |
| Finish | `2026-08-21 02:03:25 MSK` |
| Wall clock | `87.192 s` |
| Lifecycle elapsed | `85.675 s` |
| Egress rows | `7`, по `14` сервисов |
| Result | `6` rows OK; `vless` WARN; egress `1` FAIL; общий lifecycle `OK` |
| Users/routes | `0` / `0` |
| Scope | `CERTIFICATION_ONLY`, execution forbidden |

Разбивка полного цикла по egress из payload:

| Egress | Время |
|---|---:|
| `vless` | `14.674 s` |
| `awg0` | `10.877 s` |
| `awg3` | `11.147 s` |
| `1` | `21.695 s` |
| `openvpn-1779388847-d2ad7c` | `10.693 s` |
| `wireguard-1779454504-c43409` | `7.423 s` |
| `amneziawg-exec-20260528-10-8-1-14` | `9.166 s` |

Сумма совпадает с lifecycle `85.675 s`, то есть production full Matrix сейчас
тратит время на последовательный полный обход egress, а не на Candidate/Packet
или lease.

## 4. Что является bottleneck

1. **До начала проверки:** плановый timer даёт до `15 min + 60 s jitter`.
   Это основной вклад в latency обнаружения для событий, которые не будят
   существующий ранний consumer.
2. **Внутри полного Matrix:** последовательные egress занимают около `86 s`.
   Самый длинный наблюдённый egress — `1` (`21.695 s`).
3. **Short path:** уже существует и даёт существенное сокращение probe на
   Polygon, но текущий production diagnostic не выдал свежий exact target и
   ordinary scope; последний цикл классифицирован как certification-only.
4. **Synthetic transaction:** его миллисекундные spans не объясняют production
   задержку и не оправдывают изменение Apply/Lease/Barrier.

## 5. Безопасность и изменения

- cadence, timeout, FAST и full Matrix не менялись;
- новый owner, Runtime, queue, watcher, registry или source of truth не
  создавались;
- production users moved: `0`;
- production route mutation: `0`;
- short/full comparison не получил права на действие;
- неизвестные, устаревшие и противоречивые данные продолжают блокировать
  продвижение.

## 6. Позиция в плане Mission

Выполнены пункты текущего логического блока:

1. timing synthetic T0–T11 извлечён;
2. synthetic сопоставлен с Polygon short/full и live Matrix;
3. bottleneck классифицирован доказательно;
4. отчёт сохранён, production change не потребовался.

Текущая Mission не закончена. Следующий executable шаг: на свежем Matrix
generation повторно получить exact current source/target/certification context
через существующий read-only/Polygon owner. Если context валиден, выполнить
следующий governed one-synthetic-client T10–T11 dry-run с записью decision,
candidate, packet, lease, barrier, verification и rollback/closure; обычных
клиентов не затрагивать.

## Источники и проверки

- live read-only `systemctl`/`journalctl` и state на `v7-vps`, последний цикл
  `02:01:58–02:03:25 MSK`;
- `tools/v7-governed-canary-dry-run-cycle` и custom Polygon timing extraction;
- `tests.unit.test_governed_canary_cli`: `127/127 PASS`;
- `tests.unit.test_v5_3_matrix_controlled_comparison` вместе с lifecycle
  binding: `14/14 PASS`;
- предыдущие отчёты:
  `2026-08-21_013722_v5_3_matrix_recovery_and_observability_restored.md`,
  `2026-08-21_015243_v5_3_polygon_synthetic_t0_t11_dry_run_execution.md`.
