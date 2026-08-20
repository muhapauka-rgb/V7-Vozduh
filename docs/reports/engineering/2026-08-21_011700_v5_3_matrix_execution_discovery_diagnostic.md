# V5.3: диагностика работы и обнаружения Matrix

Дата: 2026-08-21 01:17 MSK  
Класс: read-only operational diagnostic  
Mission: `V7_COMPLETE_HEALTH_TEST_STABILITY_SYSTEM_ATLAS`  

## Краткий вывод

Проблема разделена на две части:

1. Пятиминутная автоматическая проверка была внешним heartbeat Codex. Она
   поставлена на паузу и не является production Matrix.
2. Production Matrix настроен на 15 минут, но текущие read-only данные не
   доказывают успешное завершение ни одного свежего цикла. Поэтому сейчас
   нельзя считать Matrix «работающим по расписанию» только на основании
   `active (waiting)`.

Production-клиенты, маршруты, Matrix, Runtime и systemd timer не изменялись.

## Что подтверждено

| Область | Наблюдение | Статус |
|---|---|---|
| Timer | `OnUnitActiveSec=15min`, `RandomizedDelaySec=60s`, `OnBootSec=2min` | подтверждено статикой |
| Caller | `v7-service-matrix-refresh.timer` → `v7-service-matrix-refresh.service` → `v7-service-matrix-refresh-all --runtime-hot-path-only --matrix-comparative-preflight` | подтверждено статикой и Runtime snapshot |
| Runtime | timer `active (waiting)` | подтверждено, но это только состояние планировщика |
| Последняя доступная наблюдаемость | convergence snapshot собран `2026-08-20 22:07:15 MSK` | устарело относительно текущей проверки |
| Autoswitch | `DRY_RUN`, `selected_move_count=0`, `dry_run_intelligence_snapshot_stop_required` | подтверждено snapshot |
| Свежая генерация | новый `service-matrix.json`, last start/finish/exit и next trigger не входят в разрешённый read-only набор | не подтверждено |

## Техническая причина, которую можно утверждать уже сейчас

Существующий caller выполняет полную проверку egress-каналов последовательно:

- для каждого egress вызывается существующий `v7-service-matrix-test`;
- один вызов имеет внешний hard timeout `timeout * 14`;
- при штатном значении timeout `8 s` это до `112 s` на один egress;
- после probes тот же production вызов может ждать bounded delegated action ещё
  до `passive_consumer_timeout_sec + 180 s`, то есть обычно до `210 s`;
- итоговый compact summary записывается только после соответствующей части
  lifecycle.

При ранее зафиксированных 7 egress и 14 сервисах теоретический верхний бюджет
для полностью последовательного неблагоприятного прохода равен:

| Компонент | Верхняя оценка |
|---|---:|
| 7 egress × 112 s | 784 s (13:04) |
| bounded action | 210 s (03:30) |
| всего до summary | 994 s (16:34) |

Это кандидат на наложение полного прохода на 15-минутный интервал. Это не
доказательство фактического timeout: точный exit code, длительность текущего
цикла и systemd failure reason сейчас не видны через разрешённый read-only путь.

## Почему Matrix «не обнаруживается»

Текущий read-only контракт наблюдает наличие и состояние timer, но не
предоставляет одновременно:

- последний start/finish service;
- exit code последнего запуска;
- следующий trigger;
- mtime/freshness канонического `service-matrix.json`;
- журнал или причину прерванного запуска.

Из-за этого одинаково выглядят как минимум три сценария: успешный цикл с
устаревшим snapshot, зависший/долгий цикл и упавший oneshot. Нельзя безопасно
выбрать один сценарий без расширения наблюдаемости существующего владельца.

## Что не делалось

- не запускался ручной Matrix refresh;
- не менялись timer/service, cadence, Runtime, Matrix state, клиенты или
  маршруты;
- не создавался новый owner, watcher, registry или источник истины;
- не выполнялся controlled dry-run, поскольку свежая ordinary Matrix generation
  и exact certification context не подтверждены.

## Безопасный следующий шаг

Существующий Runtime/Matrix owner должен добавить в действующий read-only
контур одну проверку одного цикла, без запуска и изменения systemd:

1. `last_start`, `last_finish`, `exit_code` для
   `v7-service-matrix-refresh.service`;
2. `next_trigger` для `v7-service-matrix-refresh.timer`;
3. mtime и возраст `service-matrix.json` и
   `service-matrix-refresh-summary.json`;
4. bounded tail журнала с причиной failure/timeout, если цикл просрочен.

После появления свежей канонической генерации повторяется T0–T11 re-entry:
сначала exact certification context, затем только разрешённый synthetic
one-client dry-run. До этого сохраняется `STOP_SAFE`.

## Проверки этого блока

- AST parse: `tools/v7-service-matrix-refresh-all`,
  `tools/v7-service-matrix-test`, `tools/v7-truth-check` — PASS.
- `tools/v7-truth-check --local --json` — PASS.
- `tools/v7-truth-check --runtime-readonly --json` — NO-GO только из-за
  `runtime_local_commit_mismatch`; Matrix timer в runtime snapshot —
  `active (waiting)`.

