# V5.3: интеграция трека оптимизации времени обнаружения и восстановления

**Дата:** 2026-08-20 (MSK)
**Тип:** изменение порядка инженерной работы в существующей V5.3 Program.
**Статус:** `PROGRAM_ORDER_UPDATED`; без изменения CPS, Runtime, Matrix, autoswitch, маршрутов, клиентов или production.

## Итог

В действующую V5.3 добавлен bounded track
`V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`. Это не новая
Program, Mission, owner или архитектура. Его задача — не ускорять отдельный
тест, а последовательно доказать, где теряется время на полной цепочке от
возникновения сбоя до восстановления клиентского трафика.

Прежнее решение
`TARGET_ARCHITECTURE_REFINED_EXISTING_OWNER_VARIANT` сохранено как действующее
ограничение безопасности: Full Matrix остаётся live baseline, subset остаётся
shadow comparison, automatic FAST остаётся HOLD. Интеграция не отменяет и не
перескакивает текущий CPS-фронтир
`EXECUTE_V5_3_PHASE_G_BOUNDED_EGRESS_PARALLELISM_CONTROLLED_POLYGON`.

## Почему потребовалось изменение

Ранее программа уже требовала Atlas, семантику сбоев, сравнение практик,
кандидаты и архитектурное решение. Но краткая формула порядка могла быть
прочитана как «benchmark → выбрать FAST → implementation». Это риск: скорость
Matrix не равна времени восстановления клиента, а часть задержки может быть
в persistence, свежести данных, readiness резерва, допуске решения или
проверке после действия.

Новый порядок фиксирует причинную зависимость: сначала измерить путь и
сценарии, потом назвать реальные bottleneck, после — сопоставить именно эти
проблемы с внешними паттернами и лишь затем принимать или уточнять
архитектуру.

## Внесённые изменения в Program

Изменён файл:

- [V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM.md](../../programs/V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM.md)

Добавлено:

1. Встроенный трек T0–T11 без нового владельца или источника истины.
2. Двенадцать упорядоченных evidence gates L1–L12:

   `Current reality → scenario matrix → responsibility → test roles → root
   contributors → safe options → problem-to-pattern benchmark → architecture
   → controlled validation → scale → implementation → before/after proof`.

3. Явное различение двух часов:
   - наблюдаемое внешнее возникновение сбоя → восстановление клиента — только
     когда происхождение сбоя доказуемо;
   - существующий product KPI `T0 FAILURE CONFIRMED → T11 CLIENT TRAFFIC
     RECOVERED` — обязательный измеряемый результат.

4. Обязательное правило для внешнего опыта:

   `доказанная проблема V7 → подходящий зрелый механизм → существующий owner
   → REUSE / ADAPT / REJECT`.

5. Обновлённое Definition of Done: нужны карта T0–T11, матрица сценариев,
   роли сигналов и тестов, root contributors, register безопасных вариантов,
   mapping проблем к паттернам и честное разделение Runtime/Polygon/static
   evidence.

## Что уже можно переиспользовать, но не выдавать за production

Отчёт
[2026-08-20_235500_v5_3_t0_t11_latency_trace_and_safe_optimization_register.md](2026-08-20_235500_v5_3_t0_t11_latency_trace_and_safe_optimization_register.md)
уже даёт исходный L1–L6 материал:

- статическую карту T0–T11;
- семь failure-сценариев;
- разделение detection/confirmation/decision/action;
- роли проверок;
- начальный реестр задержек и безопасных возможностей;
- 9/9 полигонных проверок существующей short→full цепочки.

Однако этот материал не закрывает production-измерение: Runtime наблюдение
показало отличающиеся local и deployed commit (`edbbedf6…` и `0d8729a109…`).
Поэтому численные live T0–T11 и реальный эффект для клиентов пока отмечены
`UNKNOWN`, а не повышены до факта.

## Что остаётся действительным

- Existing Matrix writer, state, lock и full Matrix fallback.
- Existing Planner, target/readiness, policy, Authority, route/apply и
  post-switch verification owners.
- Source/target/recovery/post-switch separation и fail-closed для stale,
  unknown и conflicting data.
- Предыдущие Atlas и mature-platform comparison — как переиспользуемые
  источники, без повторного исследования до нового invalidator.
- Phase G controlled Polygon и его границы: не превращать cross-egress
  parallelism в автоматически признанное ускорение.

## Что сознательно отложено

- Новый или изменённый FAST Runtime consumer.
- Изменение cadence, threshold, persistence, Matrix или autoswitch.
- Новая архитектура, owner, Planner, queue, watcher, registry либо state.
- Маршруты, переключение пользователей и production deploy.
- Повторный benchmark ради количества компаний, а не ради конкретной
  доказанной проблемы.

## Проверка качества изменения

- Прочитаны актуальные CPS/OMP и V5.3 Program; CPS остаётся владельцем
  текущего фронтира.
- Изменение ограничено Program и этим отчётом.
- `git diff --check` — без ошибок.
- Runtime и production не вызывались для изменений.

## Текущая позиция и следующий шаг

**Позиция:** программа получила правильные «рельсы» для дальнейшей работы;
система и её текущий план исполнения не изменены.

**Точный следующий шаг по текущему CPS, а не по этому документу:** existing
OMP/CPS consumer должен потребить уже полученный результат Phase G «не
допускать cross-egress parallelism», атомарно пересчитать frontier и явно
зафиксировать отсутствие Runtime-admission из этой гипотезы. После этого
первым новым latency-residual остаётся согласованное Runtime-наблюдение
существующих T0–T11 spans, если его можно получить без производства события
и без изменения безопасных границ.

## Эффект

| Область | Эффект |
| --- | --- |
| Program order | изменён: выбор архитектуры поставлен после доказанных причин задержки |
| CPS/OMP current frontier | не изменён |
| Код / Matrix / autoswitch | не изменены |
| Runtime / production | без эффекта |
| Маршруты / клиенты | без эффекта |
