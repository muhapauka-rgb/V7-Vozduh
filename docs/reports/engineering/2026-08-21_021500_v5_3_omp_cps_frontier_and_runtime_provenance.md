# V5.3: OMP/CPS frontier и Runtime provenance

Дата: 2026-08-21 02:15 MSK  
Track: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Блок: read-only reconciliation после Polygon T10–T11

## OMP/CPS consumer

`tools/v7-truth-check --continue-omp --json` завершился `PASS`:

- текущая Mission сохранена;
- `exact_next_automatic_action` остаётся
  `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`;
- terminal не выставлен;
- authority/routing/runtime/user movement отсутствуют;
- real caller: `continue_omp_engineering_control_loop`;
- real consumer: existing V5.3 Health/Test/Stability owners.

Это подтверждает, что Polygon evidence не потеряла Mission и не создала новую
Program.

## Runtime provenance

`tools/v7-truth-check --runtime-readonly --json` дал `NO-GO` только по
`runtime_local_commit_mismatch`:

| Источник | Commit |
|---|---|
| Local `Updatesystem` | `3b02120363951027609bf9df6aba507425e65834` |
| Runtime `/opt/v7` | `0d8729a109dcc5b9a9a6bea689ec053311c01869` |

При этом live state Matrix известен, timer proven active, authoritative Matrix
binaries совпадают, а локальное рабочее дерево чистое. Расхождение содержит не
только текущие отчёты, но и изменения `tools/v7-truth-check`,
`tools/v7_sync_lib.py`, тестов и исторических Program/engineering документов
(38 paths, около 4144 added/changed lines). Это не безопасная документационная
разница и не основание автоматически накатывать весь local HEAD в production.

## Решение

- deploy текущего local HEAD не выполнялся;
- production Matrix/Runtime/routes/users не изменялись;
- текущий `NO-GO` классифицирован как provenance/deploy boundary, а не Matrix
  failure;
- Polygon lane остаётся допустимым для дальнейшего измерения без ожидания
  natural failure.

## Проверка минимального diff

Сравнение `0d8729a109dcc5b9a9a6bea689ec053311c01869..HEAD` не содержит
изменений в `tools/v7-service-matrix-*`, `tools/v7-users-autoswitch`,
`admin_core`, `systemd` или runtime-конфигурации. Расхождение затрагивает
`tools/v7-truth-check` (`22` добавленных строк) и `tools/v7_sync_lib.py`
(`516/5` строк), а также Program/reports/tests. Поэтому для текущего Matrix
latency блока нет доказанного минимального production deploy diff: live Matrix
бинарии уже согласованы, а остальной local HEAD нельзя накатывать целиком
только ради снятия формального commit mismatch.

Это закрывает проверку deploy scope без deploy. Следующее измерительное
продолжение может идти через существующий Polygon и direct read-only Matrix
owners; production apply остаётся запрещённым до отдельной provenance-сверки.

## Re-entry gate checks

На Polygon прошли `3/3` focused tests:

- exact standing semantic binding для availability-first scope;
- baseline reset через существующий scope owner без L3 incident;
- fail-closed при identity mismatch.

Следовательно, текущий STOP_SAFE — это не пропущенная локальная проверка
selection logic. Он воспроизводится именно отсутствием production exact
admission/context и Runtime provenance.

Дополнительный bounded Polygon scope check: `4/4 PASS` — authority/runtime
bounds ограничивают cohort, zero-authority остаётся shadow без stage credit,
soft quality miss отделяется от hard failure, а hard/insufficient truth
закрывается fail-closed.

## Реальный caller short/full пути

Production unit действительно запускает существующий caller:

```text
v7-service-matrix-refresh.timer
  → v7-service-matrix-refresh.service
  → v7-service-matrix-refresh-all --runtime-hot-path-only --matrix-comparative-preflight
  → v7-users-autoswitch --consume-service-failure-automation-only
  → existing short Matrix → unchanged full Matrix comparison
```

Но для текущего `CERTIFICATION_ONLY` source branch refresh owner намеренно
завершает обработку до advisory comparison (`DEFERRED_TO_EXISTING_CONTROLLED_OWNER`),
потому что там нет ordinary user scope. Поэтому текущий live vless цикл
подтверждает Matrix и STOP_SAFE, но не является доказательством short/full
latency именно для ordinary failover. Это проверено synthetic caller chain и
не требует менять production ветку.

### Bounded ordinary-scope caller timing

В отдельном Polygon fixture существующий caller был запущен с одним source,
одним target и тремя обязательными сервисами:

| Вариант | Время | Проверки |
|---|---:|---:|
| Short | `67.306 ms` | `6` |
| Full | `265.157 ms` | `28` |

Результат: `MATRIX_FAST_FULL_AGREEMENT`, расхождений нет, full остаётся
финальным canonical observation. Short уменьшил controlled время на `74.6%`
и количество проверок на `78.6%`. `users_moved=0`, routing mutation отсутствует.

Дополнительные caller/lifecycle guards: `4/4 PASS` — exact subset использует
существующий probe owner, observation-only останавливается до downstream
consumer, runtime caller передаёт comparison без apply, а ordinary STOP_SAFE
не запускает certification tail раньше времени.

## Текущая позиция Mission

T0–T11 timing, fresh Matrix revalidation и one-client synthetic T10–T11 уже
доказаны в engineering lane. Production branch остаётся `STOP_SAFE`, пока не
появится exact action-class target context и согласованная Runtime provenance.

Следующий executable шаг: выделить минимальный deployable diff для текущего
V5.3 consumer (без исторических reports и без несвязанных Program/tool
изменений), прогнать его независимую проверку и только затем повторить
read-only Runtime convergence. До такой сверки production apply запрещён.

## Источники

- `tools/v7-truth-check --continue-omp --json`;
- `tools/v7-truth-check --runtime-readonly --json`;
- `git diff --stat 0d8729a109dcc5b9a9a6bea689ec053311c01869..HEAD`;
- предыдущие отчёты текущего V5.3 блока.
