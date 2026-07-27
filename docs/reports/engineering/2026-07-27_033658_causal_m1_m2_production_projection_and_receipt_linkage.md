# CAUSAL M1/M2: production compact projection и receipt linkage

Дата: 2026-07-27 03:36 UTC
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`
Миссии: `CAUSAL_M1_DUAL_LIFECYCLE_COMPACT_PROJECTION`, `CAUSAL_M2_ATOMIC_TRANSITION_AND_RECEIPT_LINKAGE`
Статус: `PRODUCTION_DEPLOYED_AND_CONSUMED`

## Результат

Закрыты два последовательных causal gaps без создания нового хранилища,
очереди, watcher, planner, Runtime или Authority owner.

1. Passive terminal теперь materializes в existing
   `l3-runtime-state.json:incidents` как compact record. Он разделяет
   channel incident, cohort protection intent и user protection intent,
   хранит только count/fingerprint scope, lineage и точный next consumer.
2. Existing OMP receipt теперь под existing `closure-records.lock` materializes
   обратно в тот же compact record. Receipt — durable linearization point;
   interrupted receipt-to-read-model handoff восстанавливается на следующем
   существующем consumer invocation без второго receipt.

## Production verification

| Проверка | Результат |
| --- | --- |
| M1 deploy | `f1ee0bcb`, затем idempotency repair `5fa996f8` |
| M1 production caller | 43 current passive incident projections; `invalid_open_incidents=0` |
| M1 repeat | `changed_records=0` |
| M2 deploy | `c444630b`, затем generation-safe repair `7e44f958` |
| M2 production OMP consumer | `NO_PENDING_OBLIGATION`; receipt reconciliation `PASS`; `missing_incident_projections=0`; `invalid_open_incidents=0` |
| M2 repeat | `changed_records=0`; second receipt не создан |
| Truth / convergence | `PASS`, `FULLY_ALIGNED`, `ALIGNED` |

Первая production M1 replay выявила churn: исторические closures одного
incident последовательно переписывали current projection. Исправление
перевело reconciliation на latest terminal per source incident. Повторный
caller подтвердил exact idempotency.

Первая M2 implementation могла сравнить legacy receipt по одному source.
Исправление допускает legacy binding только при точном
`source_incident_id + Situation + Decision Trace`; новый M1 receipt обязан
иметь exact `incident_key`. Поэтому старый receipt не может пометить новую
generation как consumed.

## Forbidden effects

На всех deploy/caller runs: Candidate `false`, Packet `false`, lease `false`,
Runtime apply `false`, routing mutation `false`, users moved `0`, rollback
apply `false`, Authority change `false`, Production Maturity `false`.

## Exact next frontier

`V7_INCIDENT_CAUSAL_CLOSURE_M3_ACTIVE_INCIDENT_REVALIDATION_AND_TERMINAL_REOPENING_V1`
(`CAUSAL_M3_ACTIVE_INCIDENT_REVALIDATION`).

M3 использует уже materialized compact record, чтобы active incident не
оставался вечным passive terminal: он должен получать fresh owner-backed
revalidation, exact reopen/close/continue semantics и successor без
переиспользования старых Candidate, Packet, lease или Authority.
