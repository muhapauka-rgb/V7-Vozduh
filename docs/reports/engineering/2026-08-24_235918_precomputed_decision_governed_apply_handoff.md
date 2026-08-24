# Передача подготовленного решения в governed Apply: итог миссии

Дата: 24 августа 2026, MSK  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Mission: `V7_PRECOMPUTED_DECISION_TO_GOVERNED_APPLY_HANDOFF`  
Архитектура: `V5.3 N0–N11 ROLE-BASED FAST RECOVERY ARCHITECTURE`

## SUMMARY

Минимальная передача существующего Matrix/Planner prepared decision в governed
caller реализована, проверена тестами, опубликована и развернута. Она не создаёт
новый Planner, cache, очередь, owner или источник истины. При stale, missing или
ambiguous projection используется существующий полный Planner и fail-closed.

Миссия остановлена на терминале:

`PRECOMPUTED_DECISION_HANDOFF_FUNCTIONAL_BLOCKED`

Причина терминала — не доказанный дефект handoff. Controlled cold evidence не
может быть воспроизведена в текущем Polygon runtime: после подготовки
synthetic failure активный health/condition lifecycle переводит тот же
synthetic профиль на `awg3` до source-binding governed caller. Planner видит
несовпадение identity и законно делает `STOP_SAFE`. Обычные пользователи не
затронуты.

## CURRENT FROZEN FAILURE DISTRIBUTION

Последняя frozen-серия до этой миссии имела один immutable fingerprint
`80d7d9c4b00bd520b3670ca76e66019978e8b7f5a76d68b775621148feabff98` и пять
functionally valid samples:

| sample | kind | onset→S11, ms | T0→decision, ms | classification |
|---:|---|---:|---:|---|
| 1 | cold | 2891.812 | 1963.596 | functionally valid, performance fail |
| 2 | warm | 2753.666 | 1957.341 | functionally valid, performance pass |
| 3 | warm | 2887.513 | 2058.220 | functionally valid, performance pass |
| 4 | warm | 4043.267 | 3188.182 | functionally valid, performance fail |
| 5 | warm | 3172.290 | 2307.710 | functionally valid, performance fail |

Nearest-rank P95 для пяти samples: `4043.267 ms`, поэтому HARD_PATH SLO не
пройден. Отдельная функционально завершённая проба `8206.045 ms` ранее была
ошибочно исключена только из-за длительности; новая семантика теперь сохраняет
её как performance failure.

## PERFORMANCE-EVIDENCE SEMANTICS CORRECTION

`admin_core/operator_execution_pipeline.py` теперь разделяет:

- `FUNCTIONALLY_VALID` — вся цепочка и доказательство S11 корректны;
- `PERFORMANCE_PASS` — latency удовлетворяет SLO;
- `PERFORMANCE_FAIL` — цепочка корректна, но latency выше SLO/ceiling;
- `MEASUREMENT_INVALID` — отсутствует обязательная временная, lineage-,
  generation- или safety-доказательная часть.

Совместимое поле `ok` теперь означает функциональную валидность, а не
быстродействие. Исторические raw receipts не изменялись.

## T0_TO_DECISION DECOMPOSITION

На пяти read-only Polygon-shaped runs нового owner instrumentation:

| span / owner | p50, ms | p95, ms | max, ms | CPU / load / RSS | классификация |
|---|---:|---:|---:|---|---|
| prepared decision lookup | 0.112 | 0.124 | 0.124 | CPU около 0.1 ms; RSS owner context | `REQUIRED_HOT_VALIDATION` |
| prepared generation validation | 0.007 | 0.009 | 0.010 | negligible | `REQUIRED_HOT_VALIDATION` |
| current scope validation | <0.01 | <0.02 | <0.02 | negligible | `REQUIRED_HOT_VALIDATION` |
| candidate eligibility / target freshness | 0.001 | 0.002 | 0.003 | negligible в empty local fixture | `REQUIRED_HOT_VALIDATION` |
| pre-planner refresh | 2.13 | 2.48 | 2.48 | part of current Planner path | `STALE_FALLBACK_ONLY` |
| registry read | 0.033 | 0.041 | 0.041 | no byte counter exposed | `REQUIRED_HOT_VALIDATION` |
| policy / capacity validation | 8.155 | 11.243 | 11.243 | CPU close to wall; load sampled | `REQUIRED_HOT_VALIDATION` |
| Planner initialization | 10.735 | 14.161 | 14.161 | CPU 11–13 ms; process count unavailable on macOS | `STALE_FALLBACK_ONLY` |

Runtime diagnostics now expose wall time, process CPU, load start/end, peak RSS,
process count where available, and explicit `UNKNOWN` for lock wait, bytes,
files and subprocess count when the existing owner has no counter. No material
measurement overhead was observed.

Production-shaped read-only Matrix projection after deploy was fresh:
`PREPARED_CLASS_DECISION_AVAILABLE`, `PREPARED_CLASS_DECISION_FRESH`,
six deduplicated target/service contracts, `world_model_rebuilt=false`.

## EXACT DOMINANT SUBSPAN

The frozen evidence still attributes the largest residual to synchronous
`T0→decision` work. Post-decision Apply, assignment, kernel and service
verification remain the smaller and more stable part. The new handoff removes
the broad rebuild only when the existing projection and all invalidators are
fresh; it does not claim that the current 2-vCPU runtime has already met the
3-second SLO.

## WHY CURRENT N5 PREPARED DECISION WAS NOT SUFFICIENTLY CONSUMED

N5 already produced prepared semantic classes and bounded hot targets, but the
governed L3 caller did not carry that object into the exact Apply path. The
caller therefore paid the full Planner path again. The new adapter connects the
existing summary to the existing Planner call only for one unique official
target; otherwise it records the reason and falls back.

## PREPARED DECISION INVALIDATION MODEL

The handoff checks existing owner-backed facts for source identity/failure
generation, membership, target topology and path freshness, profile/service
contract, capacity/reservation, policy/Authority, organization policy, service
routing, anti-flap and conflicting operation state. Any stale, missing,
ambiguous or contradictory input returns `EXISTING_FULL_PLANNER` or
`STOP_SAFE`. A prepared proposal never grants Apply permission.

## ONE ARCHITECTURAL CHANGE

Only one architectural change was admitted:

`PRECOMPUTED_DECISION_TO_GOVERNED_APPLY_HANDOFF`

It carries the prepared proposal and generation/fingerprint bundle into the
existing governed path, bounded-validates it, and preserves Candidate → Packet
→ Lease → Barrier → Apply → exact route/service/S11 gates.

## FILES / OWNERS CHANGED

- `tools/v7-users-autoswitch` — existing Planner diagnostics and read-only
  prepared-decision handoff adapter;
- `tools/v7-governed-canary-dry-run-cycle` — existing caller passes the handoff
  and preserves sample classification;
- `admin_core/operator_execution_pipeline.py` — evidence semantics;
- `admin_core/operator_execution.py` — compatible evidence record projection;
- focused unit tests for slow-valid samples, missing timing and stale/ambiguous
  prepared targets.

No new owner, Planner, Runtime, state store, queue, timer, registry or truth
source was created. Matrix writer count and Planner owner count remain one.

## NO SECOND PLANNER / NO SECOND TRUTH PROOF

The handoff reads the existing Matrix-owned summary and returns a bounded
proposal. It does not rank servers independently, write state, create
execution objects or authorize a move. A stale or ambiguous proposal is
consumed only as a fallback reason.

## FOCUSED SAFETY TESTS

The focused V5.3 suite passed: **434 tests**, including:

- valid slow sample remains in the performance distribution;
- missing timing is measurement-invalid;
- one unique prepared target is reusable;
- ambiguous targets fail closed;
- stale/missing projection uses the existing full Planner;
- existing Candidate/Packet/Lease and Matrix safety tests remain green.

## DEPLOY / TRUTH ALIGNMENT

| surface | result |
|---|---|
| local branch | `Updatesystem`, clean |
| local commit | `6506d0496435271f2b8ce9620c26bca69c49595f` |
| GitHub `Updatesystem` | aligned to `6506d049` |
| safe deploy | `deploy-z8-14-Updatesystem-6506d04-20260824T232959`, PASS |
| runtime commit | `6506d049` |
| runtime critical hashes | known and match authoritative |
| `v7-health.service` | active |
| Matrix cadence timer | disabled, unchanged |
| autoswitch service/timer | disabled, unchanged |
| ordinary-user movement | 0 |
| Authority expansion | false |

## POST-DEPLOY COLD SAMPLE

Одна новая controlled попытка прошла через governed Apply и route verification
для synthetic `10.7.0.92`, но была сохранена как
`MEASUREMENT_INVALID`: запуск не включил отдельный CT-M0F evidence-consumer
flag, поэтому route owner не эмитировал обязательный cutover receipt. Это не
изменение S11 и не скрытый slow sample. Reset-owner безопасно закрыл остаток.

После исправленного запуска система дважды остановилась **до Apply**:

`availability_first_planner_identity_missing:10.7.0.92`

Read-only race boundary показала: сразу после setup identity находится на
dedicated execution source; между setup/condition и governed binding текущий
health/condition lifecycle возвращает её на `awg3`. Поэтому Planner не создаёт
устаревший Candidate и делает `STOP_SAFE`. Source registry остался enabled,
обычные identity/маршруты не изменялись.

## NEW HOMOGENEOUS SERIES

Не начиналась. Условие серии — одна валидная post-deploy cold sample — не
выполнено. Запуск серии при неподтверждённом source binding был бы
статистически недействителен.

## ALL FUNCTIONALLY VALID SAMPLE TABLE

Новых functionally valid samples после handoff: `0`. Предыдущие пять frozen
samples приведены выше и остаются единственной SLO-доказательной серией.

## P50 / P95 / MAX

Для frozen серии: `P50=2887.513 ms`, `P95=4043.267 ms`,
`MAX=4043.267 ms`. Новая серия не имеет распределения.

## HARD_PATH TERMINAL

`PRECOMPUTED_DECISION_HANDOFF_FUNCTIONAL_BLOCKED`

Терминал означает, что текущий runtime не дал безопасно получить новую
functional cold receipt из-за source-binding race. Он не означает, что S11
ослаблен или что handoff признан причиной race. Автоматические performance
micro-patches не продолжались.

## EXACT NEXT FRONTIER

Сначала устранить или отдельно согласовать owner-level race между synthetic
controlled-condition setup и Matrix/health lifecycle, сохранив один Matrix
writer и без ручного pin target. После доказанного устойчивого source binding
повторить ровно одну cold functional sample на fingerprint `6506d049`, затем
заморозить реализацию и только после этого решать вопрос о новой homogeneous
HARD_PATH series. Telegram/N10/N11 в эту миссию не входят.
