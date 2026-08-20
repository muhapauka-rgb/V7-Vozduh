# V5.3 T0–T11: Polygon и read-only Runtime — модель задержки

Дата: 2026-08-21 00:14 MSK  
Mission: `V7_COMPLETE_HEALTH_TEST_STABILITY_SYSTEM_ATLAS`  
Track: `V5_3_T0_T11_LATENCY_OPTIMIZATION`  
Статус блока: evidence-only, без изменения Runtime, Matrix, маршрутов и клиентов.

## SUMMARY

Выполнен текущий шаг T0–T11: повторно использована накопленная карта L1–L6, проведён существующий Polygon-набор и выполнена read-only Runtime-проверка. Новая архитектура не выбиралась и не внедрялась.

Главный результат: в Polygon короткая проверка сохраняет решение полной проверки на проверенных сценариях и сокращает число запросов в цепочке выбора кандидатов, но доказанного production-ускорения пока нет. Runtime виден частично: таймер Matrix активен, состояние и бинарные хэши доступны, однако развёрнутый код (`0d8729a109...`) не совпадает с локальным кодом (`972c4f86c1...`). Поэтому live-распределения T0–T11, включая реальные T3/T6–T11, классифицированы как `UNKNOWN`, а не как измеренные.

Безопасный вывод: основная подтверждённая задержка для отказов, которые не попадают в Telegram-сигнал, — ожидание следующего полного Matrix-цикла (15 минут плюс до 60 секунд случайной задержки). Это статическая верхняя граница, не production percentile. Persistence 3 samples или 180 секунд, freshness/role/capacity/quality gates и полная проверка при расхождении сохраняются как защитные условия.

## CURRENT_T0_T11_LATENCY_MODEL

| Этап | Существующий владелец/потребитель | Что известно | Класс |
|---|---|---|---|
| T0 | внешний сигнал отказа | Источник отказа в этом блоке не создавался | `UNKNOWN` для production |
| T1 | Telegram sentinel / Matrix timer | Telegram: 4 s, accuracy 1 s; полный Matrix: 15 min + jitter до 60 s | static |
| T2 | Matrix probe owner | Telegram: 5 endpoint-проверок параллельно, TCP timeout по умолчанию 2 s; общий Matrix timeout 8 s (границы 3–30 s) | static + Polygon |
| T3 | существующий Matrix writer | Lock wait до 90 s при конкуренции; в текущем Runtime span не получен | static, live `UNKNOWN` |
| T4 | service-failure persistence owner | 3 samples или 180 s; Telegram grace 14 s | static |
| T5 | существующий autoswitch consumer | Решение только через существующий owner; прямого переключения из теста нет | static + Polygon caller |
| T6 | target-readiness/freshness owner | Fresh 900 s, stale 3600 s, expired 7200 s; учитываются role/capacity/quality/safety | static, live `UNKNOWN` |
| T7 | bounded targeted revalidation | Budget 5 s, clamp максимум 30 s, exact egress/service | static |
| T8 | short/full comparator | При расхождении выигрывает full Matrix | Polygon подтверждён |
| T9 | policy/required-service/cooldown gates | Cooldown 180 s, одна попытка на инцидент, Authority gates | static |
| T10 | route/traffic owner | В этот блок не вызывался; фактическая latency не измерялась | `UNKNOWN` |
| T11 | post-switch verification/rollback | Только статическая карта; переключение намеренно не выполнялось | `UNKNOWN` |

## POLYGON_SCENARIO_RESULTS

Запущены существующие тесты `test_v5_3_matrix_controlled_comparison`, caller-chain тесты service-failure и lifecycle binding: **17/17 PASS**.

* Full Matrix: 14 сервисов; точный subset: 3 сервиса (`telegram, google, google_auth`). На здоровом пути оба результата `OK`; на отказе `google` оба результата `WARN`, строка `FAIL` сохранена в обоих вариантах.
* Методологически ограниченный ответ `HTTP_LIMITED` признан допустимым (`ok=true`) и не превращён в ложный отказ.
* Planner выбрал существующие цели `[1, 2, vless]`; короткая фаза выполнила 6 проверок, затем полная — 42. Сравнение observation-only, `routing_mutation_performed=false`, `users_moved=0`.
* Cross-egress Polygon с существующим durable writer: cap 1/2/4 сохранил single-writer; последний прогон дал примерно 0.862 s / 0.636 s / 1.045 s. Это controlled result, не разрешение на production parallelism.
* Предыдущий Phase-G полный probe surface (8 egress × 14 services, injected 25 ms) дал cap1 0.839–0.856 s, cap2 0.640–0.649 s в стабильных прогонах, но cap4 был нестабилен; преимущество cap2 не воспроизводилось во всех сериях.
* В transient failure/recovery сценарии одна временная проба не создала инцидент и не нарушила recovery semantics.

## RUNTIME_OBSERVATION_RESULTS

Read-only `tools/v7-truth-check --runtime-readonly --json`:

* `final_verdict=NO-GO` только по `runtime_local_commit_mismatch`.
* Runtime root: `/opt/v7`; state root: `/opt/v7/egress/state`; deploy branch `Updatesystem`; deploy commit `0d8729a109...`.
* Локальный commit: `972c4f86c1...`; binary hashes известны и совпадают с authoritative manifest.
* Matrix timer: `LIVE_MATRIX_TIMER_PROVEN`; scheduler truth известен. Autoswitch scheduler/service неактивны в разрешённом manual mode.
* Доступны operation wiring, execution store, audit path, snapshot root и restore barrier.
* T0–T11 span distributions и текущие production receipts для этой версии не извлечены. Из-за mismatch нельзя переносить локальную разметку spans на production.

Классификация: Runtime topology/activation — `measured/read-only`; T0–T11 timing distributions — `UNKNOWN`; это ограничение доказательности, не разрешение на deploy.

## FAILURE_SCENARIO_TIMELINES

| Сценарий | Что проверено | Безопасная интерпретация |
|---|---|---|
| A. Hard channel failure | Частичный Polygon FAIL по сервису; реальный канал не ломался | Нужен отдельный source/channel signal; один probe не инцидент |
| B. Tunnel up, Internet down | Не инжектировался | Tunnel/process up не означает target readiness; нужен внешний service evidence |
| C. Telegram-only | Telegram входит в subset; sentinel cadence известна | Telegram — быстрый сигнал и вход в решение, не единственная истина |
| D. Critical service failure | Full/subset одинаково сохранили `google=FAIL`, общий `WARN` | Persistence owner должен увидеть тот же decisive row |
| E. Quality degradation | Quality fields и gates найдены статически | Нужен runtime sample p95/fail-rate/stability; сейчас `UNKNOWN` |
| F. Recovery | Одна временная проба не создала событие | Recovery не ускоряется ценой снятия persistence |
| G. False failure / methodology | `HTTP_LIMITED` остался `ok=true` | Ограничение метода не является отказом сервиса |
| H. Stale/unknown/conflicting | Freshness и full-on-divergence правила статически подтверждены | При stale/unknown/conflict — no switch; full wins |
| I. Capacity/flapping | cap 1/2/4 и single-writer проверены в Polygon | Не делать cross-egress parallelism production policy без повторного evidence |

## TELEGRAM_ROLE_RESULT

Telegram sentinel — ранний индикатор доступности канала/критичного сервиса, источник grace/fast wake и один из входов в persistence. Он не является Authority, не выбирает сервер сам и не выполняет переключение.

## MATRIX_ROLE_RESULT

Matrix — подтверждение доступности конкретных сервисов через конкретный egress, источник service rows для full/subset comparison, диагностика quality/capacity и вход в target readiness. Matrix не доказывает сам по себе route/client effect.

## TEST_ROLE_RESULT

Polygon отделяет проверку методики и причинности от production: он измеряет число probe attempts, длительность probe surface, writer serialization, equivalence full/subset и отсутствие side effects. Unit/lifecycle тесты подтверждают caller и owner binding. Ни один тест не доказывает production T10/T11.

## MINIMUM_SAFE_EVIDENCE_MODEL

* Hard channel: свежий source/channel signal + service evidence + persistence; tunnel-up без внешнего подтверждения недостаточен.
* Tunnel up / Internet down: process/tunnel liveness отдельно от target service readiness; unknown блокирует переход.
* Telegram-only: sentinel может разбудить проверку, но решение требует required-service и freshness gates.
* Critical service: decisive row должна совпасть в subset и full; при расхождении автоматически запускается full.
* Quality degradation: p95/fail-rate/stability с freshness и failure-domain; один slow sample не равен down.
* Recovery: минимум существующий recovery evidence и снятие persistence только по действующему owner.
* Stale/unknown/conflicting: no switch, full fallback, причина записывается в существующий receipt.
* Capacity/flapping: bounded budget, single writer, cooldown и retry budget; не расширять параллелизм по Polygon-only скорости.

## TOP_LATENCY_CONTRIBUTORS

1. Полный Matrix cadence 15 min + jitter до 60 s для отказов вне Telegram fast path — подтверждено статически, не live percentile.
2. Probe timeout/сервисный ответ (до 8 s по default Matrix probe) — статический бюджет; текущая production distribution неизвестна.
3. Persistence 3 samples или 180 s — намеренная safety latency, её нельзя убирать ради скорости.
4. Writer lock wait до 90 s при конкуренции — статический ceiling, факт конкуренции в текущем Runtime неизвестен.
5. T6–T11 (freshness, decision, route effect, post-switch verification) — не измерены live и не должны оптимизироваться вслепую.

## UNKNOWN_MEASUREMENTS

Неизвестны: реальный T0 trigger-to-evidence, production p50/p95 для T2/T3/T6/T7, частота short/full divergence, доля stale/unknown/conflict, T10 route visibility, T11 post-switch verification/rollback, реальная flapping/capacity distribution и client-visible recovery. Причина — commit mismatch и отсутствие законного controlled production event в этом блоке.

## SAFE_NEXT_OPTIMIZATION_OPTIONS

Это варианты для следующего evidence-блока, не выбранная архитектура:

1. Read-only reconciliation существующих Matrix/autoswitch performance spans на совпадающей с Runtime версии.
2. Разделить измерение source detection, target readiness и decision latency, не создавая новый collector или store.
3. В Polygon расширить только существующий observation-only сценарий stale/unknown/conflict и bounded recovery, сохраняя full fallback.
4. После доказанных spans сравнить cadence/persistence/targeted subset как варианты; до этого не менять timer, thresholds, writer или routing.

## WHAT_NOT_TO_CHANGE

Не менять Matrix owner, Autoswitch owner, Runtime, timer cadence, persistence, freshness thresholds, route/client state, single-writer contract, full fallback, cooldown или Authority gates. Не создавать новый tracker, queue, registry, watcher, database или parallel truth source. Не выполнять deploy только ради измерения.

## NEXT_EXECUTABLE ACTION

Текущая позиция плана: **Phase G consumed → T0–T11 evidence model active → Runtime span reconciliation pending → root-cause classification → safe options → mature-platform mapping → architecture decision**.

Точный следующий шаг: существующий владелец Matrix/autoswitch должен выполнить read-only reconciliation performance spans на Runtime, совпадающем с локальной версией, и вернуть распределения T0–T9 плюс законные receipts T10–T11. Если mismatch сохраняется, оставить эти поля `UNKNOWN` и продолжить только Polygon/static lane; не менять production.

Owner: существующий Matrix/autoswitch owner.  
Consumer: `continue_omp_engineering_control_loop` → existing V5.3 health-test stability owners.  
Re-entry: совпадение Runtime/local provenance или отдельное разрешённое evidence-окно.  
Safe terminal for this block: evidence recorded, no route/client movement, full fallback preserved.

## SOURCES AND REPRODUCIBILITY

* `docs/reports/engineering/2026-08-20_235500_v5_3_t0_t11_latency_trace_and_safe_optimization_register.md` — L1–L6 static map.
* `docs/reports/engineering/2026-08-20_241500_v5_3_phase_g_consumption_and_t0_t11_track_start.md` — Phase-G consumption and track start.
* `tests/unit/test_v5_3_matrix_controlled_comparison.py` — controlled Matrix Polygon.
* `tests/unit/test_service_failure_automation_evolution.py` — existing planner selection and short/full caller chain.
* `tests/unit/test_service_failure_episode.py` — advisory owner binding.
* `tests/unit/test_v5_3_matrix_decision_lifecycle_binding.py` — lifecycle/OMP binding.
* `tools/v7-truth-check --runtime-readonly --json` — read-only Runtime observation.

No production mutation, route change, client movement, deploy or push was performed.
