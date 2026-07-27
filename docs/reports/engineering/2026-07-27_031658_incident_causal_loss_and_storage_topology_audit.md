# M0: аудит причинной потери и топологии хранения инцидентов

Дата: 2026-07-27 03:16 UTC
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`
Миссия: `CAUSAL_M0_CAUSAL_LOSS_AND_STORAGE_AUDIT`
Статус: `CAUSAL_LOSS_AND_SCALE_RESIDUAL_EXACTLY_PROVEN`

## Вердикт

Дефект подтверждён. Это не отсутствие логов, OMP consumer или защиты от
дубликатов. Production уже хранит append-only события, closures, Outcomes,
Learning, shadow decisions и compact L3 state. Но passive service-failure
линия не материализуется в тот же компактный incident state, которым владеет
L3 execution path. Поэтому `STOP_SAFE` имеет исторический terminal и OMP
receipt, но не получает durable current incident / protection-intent /
successor state.

Точный residual:

`PASSIVE_INCIDENT_PROJECTION_MISSING_CAUSAL_LINEAGE_AND_SUCCESSOR_INVARIANTS`.

## Проверенные существующие owners

| Назначение | Существующий owner | Результат аудита |
| --- | --- | --- |
| Неизменяемая история | `/opt/v7/egress/state/*jsonl`, date-partitioned `/opt/v7/events/*jsonl` | уже существует; новый log/store не нужен |
| Passive capture | `tools/v7-users-autoswitch._consume_passive_production_events` | Situation, Decision Trace, Outcome, Learning и closure создаются идемпотентно |
| OMP consumption | `tools/v7_sync_lib.py:consume_service_failure_automation_frontier` | один obligation потребляется ровно один раз под существующим `closure-records.lock` |
| Текущая incident-проекция | `/opt/v7/egress/state/l3-runtime-state.json`, `AutoswitchPlanner` | существует, атомарно записывается, но passive line в неё не входит |
| Bounded read model | `admin_core.summary_builders.bounded_jsonl_records`, snapshot architecture | существует; Runtime обязан читать compact state, не raw history |

Исторический V1.4 defect «нет durable OMP consumer» не найден: 85
`service_failure_automation_obligation` имеют 85 exact-once OMP receipts.
Повторно чинить этот закрытый link запрещено.

## Production evidence (обезличенные агрегаты)

| Проверка | Результат |
| --- | --- |
| `closure-records.jsonl` | 3 698 строк, около 4.0 MB |
| passive terminals / obligations / OMP receipts | 85 / 85 / 85 |
| distinct passive source incidents | 43 |
| L3 incident records | 173; 135 `OPEN`, 4 `SUSPENDED`, остальные terminal/no-evidence |
| passive source IDs, совпавшие с L3 incident key | 0 из 43 |
| незакрытые L3 records без `next_required_consumer` | 148 |
| незакрытые L3 records без `reentry_condition` | 148 |
| наличие required causal/intent fields в L3 records | 0 для всех: generation, Situation, Decision Trace, obligation, Candidate/Packet/lease, Outcome/Learning, parent transition, intent scope/closure |
| bounded fields, уже существующие в L3 | `attempts[-50:]`, `processed_event_ids[-500:]` |
| storage sizes | L3 state ~1.4 MB; execution events ~7.0 MB; trust ~3.1 MB; shadow ~0.27 MB |

Следовательно, current state растёт не из-за полного списка пользователей, а
из-за отсутствия compact lifecycle/intent projection и ограниченного lookup
path для passive records. `read_jsonl` в passive advisory и
`_read_jsonl_records` в OMP selector сейчас читают полный closure file;
retention/rollup порогов в этой Mission не вводилось. Исторические значения
growth-rate и actual lock-hold telemetry существующие owners не публикуют,
поэтому никаких выдуманных числовых retention limits не зафиксировано.

## Отдельное CPS/runtime расхождение

CPS ещё указывает `ENGINEERING_AUTHORITY` и ожидание решения по standing
policy. Production policy owner подтверждает активный contract с id/hash,
expiry `2026-08-25T17:21:00.971884+00:00` и scope класса one-user. Это
`RUNTIME_CPS_PROJECTION_MISMATCH`, а не основание вручную редактировать CPS.
Его reconciliation остаётся за существующими CPS/Authority owners в
`CAUSAL_M8_RUNTIME_CPS_POINTER_RECONCILIATION`.

## Безопасность M0

Только read-only audit. Не выполнялись: policy write, Candidate, Packet,
lease, restore barrier, Runtime apply, routing mutation, user movement,
rollback apply, Authority expansion и изменение Production Maturity.

## Точный successor

`V7_INCIDENT_CAUSAL_CLOSURE_M1_DUAL_LIFECYCLE_COMPACT_PROJECTION_V1`
(`CAUSAL_M1_DUAL_LIFECYCLE_COMPACT_PROJECTION`).

M1 расширяет только существующий `l3-runtime-state.json` и existing closure
transition: для каждой passive line создаёт bounded incident / cohort / user
intent projection, полный lineage и mandatory next consumer/re-entry fields.
Новый registry, database, queue, watcher, planner, Runtime или Authority
owner создавать запрещено.
