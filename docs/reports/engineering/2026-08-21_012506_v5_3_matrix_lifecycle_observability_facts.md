# V5.3: Matrix lifecycle observability facts

Дата: 2026-08-21 01:25 MSK  
Track: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Mission class: bounded read-only diagnostic  

## SUMMARY

Текущий контур доказывает наличие и активацию расписания Matrix, но не доказывает
успешное завершение циклов. Фактическая cadence остаётся `UNKNOWN`.

Пятиминутный Codex heartbeat удалён отдельно и к production Matrix не относится.
В рамках этой диагностики timer, service, Runtime, Matrix state, клиенты и
маршруты не изменялись.

## RUNTIME_PROVENANCE

| Факт | Значение | Классификация |
|---|---|---|
| Local branch | `Updatesystem` | подтверждено |
| Local commit | `9c2a5e43fdebbb3147e8b4a0965042137ea2e153` | подтверждено |
| Runtime commit | `0d8729a109dcc5b9a9a6bea689ec053311c01869` | подтверждено snapshot |
| Runtime root | `/opt/v7` | подтверждено |
| State root | `/opt/v7/egress/state` | подтверждено |
| Runtime verdict | `NO-GO` | только из-за `runtime_local_commit_mismatch` |
| Local truth check | `PASS` | подтверждено |

Mismatch не исправлялся и не использовался как доказательство неисправности
Matrix. Классификация: `RUNTIME_PROVENANCE_ALIGNMENT = BLOCKED`.

## TIMER_CONFIGURATION

Источник: `systemd/v7-service-matrix-refresh.timer`.

```text
OnBootSec=2min
OnUnitActiveSec=15min
RandomizedDelaySec=60s
Unit=v7-service-matrix-refresh.service
```

Runtime read-only status:

```text
Loaded: loaded (.../v7-service-matrix-refresh.timer; enabled; preset: enabled)
Active: active (waiting)
Triggers: v7-service-matrix-refresh.service
```

Это подтверждает `CONFIGURED_MATRIX_CADENCE = 15min + до 60s jitter`, но не
`EFFECTIVE_MATRIX_CADENCE`.

## LAST_EXECUTION_FACTS

Запрошенные поля для `v7-service-matrix-refresh.service`:

| Поле | Значение | Статус |
|---|---|---|
| LAST_START | нет в разрешённом snapshot/read-only контракте | `UNKNOWN` |
| LAST_FINISH | нет | `UNKNOWN` |
| EXIT_CODE | нет | `UNKNOWN` |
| DURATION | нет | `UNKNOWN` |
| STATUS | статус oneshot не наблюдается; виден только timer | `UNKNOWN` |
| FAILURE_REASON | нет journal/log evidence | `UNKNOWN` |
| TIMEOUT_REASON | нет | `UNKNOWN` |

Нельзя утверждать ни успешный запуск, ни падение, ни зависание service.

## MATRIX_STATE_FRESHNESS

Ожидаемые файлы:

- `/opt/v7/egress/state/service-matrix.json`;
- `/opt/v7/egress/state/service-matrix-refresh-summary.json`.

Их текущие mtime, generation timestamp, age и schema validity через разрешённый
Runtime read-only путь не предоставлены. Поэтому:

`CURRENT_STATE_FRESHNESS = UNKNOWN`.

Последний доступный convergence snapshot собран `2026-08-20 22:07:15 MSK` и к
моменту этой проверки был старше трёх часов. Это возраст snapshot, а не доказанный
возраст самих Matrix-файлов.

В том же snapshot Autoswitch сообщил:

```text
terminal_state=DRY_RUN
selected_move_count=0
terminal_reason=dry_run_intelligence_snapshot_stop_required
```

Это не является доказательством свежей Matrix generation и не является реальным
перемещением клиента.

## EXECUTION_CHAIN

| Этап | Existing owner / input → output | Timestamp available | Evidence |
|---|---|---|---|
| Timer | systemd timer → service activation | только timer status | `active (waiting)` |
| Service | `v7-service-matrix-refresh.service` → `v7-service-matrix-refresh-all --runtime-hot-path-only --matrix-comparative-preflight` | нет | unit file |
| Full caller | `v7-service-matrix-refresh-all` → последовательный `run_one` по enabled egress | нет | source code |
| Probe | `v7-service-matrix-test egress all --timeout 8` | нет | source code |
| Matrix writer | existing per-egress writer → `service-matrix.json` | нет | source code |
| Summary | compact projection → `service-matrix-refresh-summary.json` | нет | source code |
| Consumer | existing passive/governed consumers after probe lifecycle | нет | source code; no runtime receipt |

## EFFECTIVE_CADENCE

Доступна только configured cadence: `15min + до 60s jitter`.

Последовательность циклов, gaps, starts, finishes и failures отсутствует в
разрешённом evidence. Поэтому:

`EFFECTIVE_MATRIX_CADENCE = UNKNOWN`  
`CONFIGURED_EQUALS_EFFECTIVE = UNKNOWN`

## POSSIBLE_FAILURE_MODES

| Сценарий | Статус | Основание |
|---|---|---|
| A. Timer работает, service успешно завершён, state обновляется | `UNKNOWN` | нет finish/exit/mtime |
| B. Timer работает, service запускается, цикл долгий | `UNKNOWN` | нет duration/timeout |
| C. Timer работает, service падает | `UNKNOWN` | нет exit/log |
| D. Service успешен, state не обновляется | `UNKNOWN` | нет state freshness |
| E. State обновляется, consumer не видит свежесть | `UNKNOWN` | нет consumer receipt |

Статический кандидат на overlap уже известен из caller: 7 egress × внешний
`8s * 14` hard timeout = 784s, плюс bounded action до 210s, то есть до 994s
(16:34) до compact summary в неблагоприятном сценарии. Это риск конструкции,
но не доказанная причина текущего отсутствия свежего evidence.

## CONFIRMED_FACTS

- Timer настроен на 15 минут с jitter до 60 секунд и активен.
- Timer вызывает существующий Matrix service; новый owner не создавался.
- Runtime snapshot и local source имеют mismatch; mismatch не исправлялся.
- Полный Matrix остаётся baseline; FAST не включался.
- Свежая успешная генерация, effective cadence и реальное перемещение клиентов не
  доказаны.

## UNKNOWN_FACTS

- фактический start/finish последнего запуска;
- exit code и причина возможного failure/timeout;
- mtime/age обоих Matrix state-файлов;
- количество и длительность последних N циклов;
- visibility свежего state у consumer;
- реальная причина задержки или пропуска generation.

## T0-T11_IMPACT

Переход к реальному T0–T11 перемещению сейчас запрещён безопасной границей:
нет свежего ordinary Matrix state и exact certification context. Наличие timer не
заменяет fresh Matrix/current state.

Следовательно, текущий frontier остаётся:

```text
fresh ordinary Matrix generation
  → exact certification context
  → governed synthetic one-client dry-run
  → только затем real client movement observation
```

Архитектура, cadence, timeout и Runtime не менялись.

## NEXT_SAFE_STEP

Существующий Runtime/Matrix owner должен расширить только read-only наблюдаемость
одного цикла, без запуска service:

1. last start/finish и exit code `v7-service-matrix-refresh.service`;
2. next trigger timer;
3. mtime/age/schema обоих Matrix state-файлов;
4. bounded journal tail с failure/timeout reason.

После этого effective cadence классифицируется как `FRESH`, `STALE`, `EXPIRED`
или `UNKNOWN`, и только при fresh state продолжается T0–T11.

## CHECKS

- `tools/v7-truth-check --local --json`: `PASS`.
- `tools/v7-truth-check --runtime-readonly --json`: `NO-GO` по
  `runtime_local_commit_mismatch`; timer status наблюдаем.
- AST parse Matrix caller, Matrix probe и truth-check: `PASS`.
- Production mutation: `NONE`.

## DEFINITION_OF_DONE

Диагностический блок выполнен по доступному read-only контуру, но Mission-level
DoD ещё не достигнут: last execution evidence, state freshness и effective
cadence остаются `UNKNOWN`. Это честный observation blocker, а не завершение
Matrix lifecycle.

