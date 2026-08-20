# V5.3: трассировка времени T0–T11 и безопасный реестр ускорений

**Дата:** 2026-08-20 (MSK)  
**Статус:** завершённый read-only исследовательский блок; Matrix, Runtime, маршруты и пользователи не изменялись.  
**Связь с текущей Mission:** не заменяет `EXECUTE_V5_3_PHASE_G_BOUNDED_EGRESS_PARALLELISM_CONTROLLED_POLYGON` и не создаёт новую Mission/Program.

## Короткий вывод

Система не ограничивается тестами сервисов. Она уже объединяет быстрый сигнал по Telegram, периодическую полную Matrix, историю/устойчивость ошибки, выбор пригодного резерва, проверки маршрута после действия и восстановление. Самое раннее подозрение может появиться примерно через 4 секунды, но безопасное решение специально требует дополнительных подтверждений. Полный Matrix остаётся запасным и диагностическим контуром.

Нельзя честно назвать текущее production-время T0–T11: read-only Runtime-проверка обнаружила, что production работает на `0d8729a109…`, а локальная рабочая версия — `edbbedf6…`. Это не ошибка сервиса и не основание для deploy в данной задаче, но делает live-метрики неизвестными. Ни один результат полигона ниже не выдан за production-факт.

## Границы и доказательства

| Вид доказательства | Что подтверждено | Чего не подтверждает |
|---|---|---|
| Статический код и unit-файлы | владельцы, очередность, интервалы, пороги, fail-closed правила | фактическую задержку конкретного инцидента |
| Изолированный полигон | последовательность short → full, единый Matrix writer, отсутствие действия над пользователем, инварианты Phase G | нагрузку или время на production-серверах |
| Read-only Runtime | Matrix timer установлен и активен; autoswitch service в одобренном manual/inactive состоянии; authoritative deployment согласован сам с собой | live T0–T11: локальная версия не совпадает с установленной |
| Production | **не получено в этом блоке** | любые численные production-выводы |

## Карта процесса T0–T11

| Точка | Существующий владелец и действие | Известное ожидание | Статус |
|---|---|---:|---|
| T0 | канал/сервис фактически ухудшился | начало внешнего события | production: неизвестно |
| T1 | `v7-telegram-sentinel` или Matrix замечает сигнал | Telegram timer 4 s, accuracy 1 s; полный Matrix 15 min + jitter до 60 s | статически подтверждено |
| T2 | sentinel проверяет 5 Telegram TCP endpoint параллельно | до 2 s на endpoint | статически подтверждено |
| T3 | существующий Matrix writer фиксирует sample | lock wait до 90 s только при конкуренции | статически подтверждено; ожидание lock не измерено |
| T4 | история ошибки отделяет единичный сбой от устойчивого | 3 samples **или** 180 s для service failure; Telegram grace 14 s | статически подтверждено |
| T5 | существующий autoswitch consumer определяет scope источника | нет отдельного нового planner | статически подтверждено |
| T6 | существующий выбор резервов читает freshness, роль, capacity, quality и safety | freshness: fresh 900 s, stale 3600 s, expired 7200 s | статически подтверждено |
| T7 | короткая проверка обязательных сервисов выбранных резервов | bounded revalidation до 5 s, максимум 30 s; только нужный egress/service | статически подтверждено |
| T8 | advisory сравнивает short с full Matrix | при расхождении — full остаётся решающим | полигон подтверждён |
| T9 | решение допускается только после required-service, policy, cooldown и authority gates | cooldown обычно 180 s; один retry на incident | статически подтверждено |
| T10 | существующий route/traffic owner выполняет действие, если оно законно | в данном блоке не вызывался | production: неизвестно |
| T11 | post-switch verifier проверяет фактический маршрут/сервис/трафик; при необходимости rollback | отдельный обязательный контур | статически подтверждено; production: неизвестно |

### Что является «быстрым», а что «полным»

- Telegram sentinel — узкий ранний сигнал: 5 endpoint, 4-секундный запуск, 14-секундная grace. `DOWN` блокирует резерв, `DEGRADED` даёт предупреждение. Он не вправе в одиночку объявить источник неисправным или переключить пользователя.
- Full Matrix — 14 сервисов: `google`, `google_auth`, `youtube`, `apple`, `instagram`, `whatsapp`, `facebook`, `spotify`, `soundcloud`, `telegram`, `chatgpt`, `openai_auth`, `claude`, `anthropic`. Плановый запуск — каждые 15 минут с jitter до минуты. Это не единственный путь, но безопасный полный fallback и диагностический контур.
- Short Matrix — существующая проверка только основного и подходящих резервов и только релевантных обязательных сервисов. Она advisory; сравнение с full записывается тем же Matrix owner. Расхождение не даёт права на действие короткому пути.

## Роли проверок Matrix

| Проверка | Источник: подтверждение неисправности | Резерв: готовность | Качество/ранжирование | Глубокая диагностика |
|---|---|---|---|---|
| google | да, channel health | да, если требуется профилем | да | да |
| google_auth | по профилю | да, если требуется | да | да |
| youtube | нет, сам по себе | для VIDEO_OPTIMIZED | да | да |
| apple | по профилю | для GLOBAL_STABLE | да | да |
| instagram | нет, сам по себе | для VIDEO_OPTIMIZED | да | да |
| whatsapp | по профилю | для GLOBAL_STABLE | да | да |
| facebook | по профилю | для GLOBAL_FAST | да | да |
| spotify | нет, сам по себе | для VIDEO_OPTIMIZED | да | да |
| soundcloud | нет, сам по себе | для VIDEO_OPTIMIZED | да | да |
| telegram | быстрый input после grace/persistence, не единолично | required hard gate для нужных классов | да | да |
| chatgpt | по профилю | для GLOBAL классов | да | да |
| openai_auth | по профилю | для GLOBAL классов | да | да |
| claude | по профилю | для GLOBAL классов | да | да |
| anthropic | по профилю | для GLOBAL классов | да | да |

«По профилю» означает: требование задаёт существующий route-class/explicit-service contract; произвольно превращать частичный сервисный сбой в общий source failure нельзя.

## Семь сценариев и минимально достаточное доказательство

| Сценарий | Что нужно до решения | Что не допускается |
|---|---|---|
| жёсткий отказ канала | устойчивый source/path факт + свежий пригодный резерв + обязательные сервисы + policy gates | действие по одному probe |
| tunnel up, но Internet нет | path/Internet evidence + persistence + target readiness | считать tunnel up признаком здоровья |
| Telegram недоступен | sentinel ratio/critical endpoint + grace + Matrix/history; для target — hard block, где Telegram required | переключение только по первому fast sample |
| Google/критичный сервис частично деградировал | route-class relevance + persistent evidence или bounded revalidation | трактовать нерелевантный профиль как общий отказ |
| ухудшение качества | quality history и допустимый профиль; это ranking, не source-rescue | срочное переключение без hard evidence |
| recovery нестабилен | текущая generation/route verification и устойчивое новое evidence | считать один успех восстановлением |
| ложный сбой probe | methodology classification и повторная bounded проверка | permanent block по ошибке методики |

## Где действительно ждёт система

| Участок | Конфигурационный максимум/интервал | Назначение | Измерение в production |
|---|---:|---|---|
| ожидание планового полного Matrix | до 16 min от границы цикла (15 min + 60 s jitter) | широкий baseline/диагностика | неизвестно |
| Telegram ранний сигнал | примерно 4–5 s до старта следующего запуска | быстрое подозрение Telegram-only | неизвестно |
| Telegram grace | 14 s | защита от короткого флапа | неизвестно |
| persistence service failure | 3 sample или 180 s | защита от ложного действия | неизвестно |
| отдельный probe Matrix | timeout 3–30 s, default 8 s | ограничение сетевого ожидания | неизвестно |
| targeted revalidation | budget 5 s, clamp до 30 s | проверить выбранный резерв, не весь мир | полигонная семантика подтверждена |
| stale/expired source truth | 900 / 3600 / 7200 s | fail-closed при старых данных | неизвестно |
| cooldown/retry | 180 s / 1 попытка на incident | защита от колебаний | неизвестно |
| Matrix writer lock | до 90 s при конкуренции | единственный устойчивый writer | неизвестно |

## Реестр возможностей ускорения (без изменения реализации)

| Приоритет | Возможность | Доказательство | Безопасное направление |
|---:|---|---|---|
| 1 | Сократить время до *подозрения* для не-Telegram hard channel случаев | статический: full Matrix cadence | измерить существующие trigger-to-T4 spans в Runtime; не менять cadence без результата |
| 2 | Измерить, какая доля T0–T11 — persistence, а не probe | статический: 3 samples/180 s | разделять «обнаружено» и «достаточно для решения» в метриках |
| 3 | Измерить T6–T9 для выбора уже известных резервов | статический + полигон | использовать существующие performance spans, не новый tracker |
| 4 | Сократить лишние probe после уже выбранного резерва | полигон: short/full equivalence | только current subset → full comparison; full fallback сохраняется |
| 5 | Проверить ожидание единого Matrix writer | статический lock 90 s | сначала собрать contention distribution, не добавлять writer |
| 6 | Отделить queue/worker задержку от сетевой | пока неизвестно | наблюдение существующего caller, без новой очереди |
| 7 | Проверить post-action verification как часть T11 | static only | замерить отдельные spans после легального controlled exercise |
| 8 | Не возвращаться к cross-egress parallelism | Phase G полигон: cap 2 нестабилен, cap 4 хуже/нагруженнее | оставить serial cross-egress; это не источник безопасного ускорения |

Главный практический вывод: наиболее перспективно не «ускорять Matrix целиком», а измерить, где в реальной цепочке теряется время, и применять существующую короткую проверку только после выбора подходящих резервов. Сокращать persistence, freshness или post-switch verification без доказательства нельзя: это защитные барьеры, а не пустая задержка.

## Выполненная проверка на полигоне

Команда:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  tests.unit.test_v5_3_matrix_controlled_comparison \
  tests.unit.test_service_failure_episode.ServiceFailureEpisodeTest.test_matrix_runtime_caller_passes_comparison_only_to_existing_advisory_owner \
  tests.unit.test_service_failure_automation_evolution.ServiceFailureAutomationEvolutionTest.test_existing_planner_selection_drives_subset_then_full_matrix_comparison \
  tests.unit.test_service_failure_automation_evolution.ServiceFailureAutomationEvolutionTest.test_polygon_caller_chain_writes_short_then_full_canonical_matrix_without_action
```

Результат: **9/9 OK**, 6.788 s. Подтверждены equivalence healthy/required-failure/methodology-limit, сохранение transient-failure/recovery semantics, serial Matrix writer, short→full comparison, передача comparison только existing advisory owner и отсутствие действия над пользователями в caller chain.

Внутри теста Phase G (не production): cap 1 = 0.912374 s / peak 8 запросов; cap 2 = 0.795557 s / peak 12; cap 4 = 1.031917 s / peak 20. Это подтверждает ранее принятый вывод: не объявлять cross-egress parallelism ускорением.

## Неизменённые защитные свойства

- Full Matrix не отключён и не заменён.
- Нет нового owner, Runtime, Planner, watcher, registry или source of truth.
- Не изменялись Matrix, FAST, autoswitch, route policy, production Runtime и маршруты.
- Не было переключения клиентов и не создано production-событие ради измерения.
- Unknown/stale/conflicting evidence продолжает блокировать продвижение там, где это требуется существующим контрактом.

## Текущая позиция и точный следующий шаг

Этот блок — **read-only анализ текущей Mission**, а не новая ветка плана. По актуальному `tools/v7-truth-check --continue-omp --json` действующий фронтир остаётся `EXECUTE_V5_3_PHASE_G_BOUNDED_EGRESS_PARALLELISM_CONTROLLED_POLYGON`; truth-check проходит, новых blocker от этого исследования нет.

**Следующий шаг по существующему плану:** существующий OMP/CPS owner должен атомарно потребить уже полученный Phase-G результат «cross-egress parallelism не admitted», пересчитать фронтир и зафиксировать, что Phase H не получает Runtime-admission из этой гипотезы. Только после этого допустимо планировать отдельное измерение реального T0–T11 на согласованной Runtime-версии. Этот отчёт не выполняет consumption и не меняет CPS.

## Источники

- `tools/v7-truth-check --continue-omp --json` и `--runtime-readonly --json`, выполнены 2026-08-20.
- `tools/v7-service-matrix-test`, `tools/v7-service-matrix-refresh-all`, `tools/v7-telegram-sentinel`, `tools/v7-users-autoswitch`.
- `systemd/v7-service-matrix-refresh.timer`, `systemd/v7-service-matrix-refresh.service`, `systemd/v7-telegram-sentinel.timer`, `systemd/v7-users-autoswitch.timer`.
- [Предыдущая архитектурная трассировка Matrix](2026-08-20_162200_v5_3_complete_health_test_stability_system_atlas.md) и [строгая revalidation](2026-08-20_170000_v5_3_system_revalidation_strict_reconciliation.md).
