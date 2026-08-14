# FB.1 Lineage Break Summary

Дата: 2026-06-12

Режим: read-only audit.

## Что доказано

- Существующий владелец canonical feedback: `admin_core/operator_execution_feedback.py`.
- Существующий writer canonical feedback: `admin/v7-admin-api` endpoint `/api/actions/execution-feedback-materialize`.
- Существующие canonical stores:
  - `/opt/v7/egress/state/execution-events.jsonl`
  - `/opt/v7/egress/state/runtime-trust.jsonl`
  - `/opt/v7/egress/state/proposal-records.jsonl`
  - `/opt/v7/egress/state/closure-records.jsonl`
- Snapshot refresh читает execution/trust/recommendation/closure feedback inputs.
- Planner читает `trust-evolution-summaries` и использует их как advisory/ranking evidence.

## Свежие executions

EXEC.2_4:
- `10.7.0.5`: `awg3 -> vless`
- apply PASS
- verification PASS
- rollback dry-run PASS
- canonical feedback materialization evidence: не найдено в свежей evidence-папке

EXEC.5_6:
- Stage A: 2 users moved
- Stage B: 5 users moved
- Stage D: 8 users moved
- total moved: 15
- verification PASS for executed stages
- rollback dry-run PASS for executed stages with explicit production state dir
- canonical feedback materialization evidence: не найдено в свежей evidence-папке

## Lineage verdict

Intended lineage exists:

`governed execution -> verification -> /api/actions/execution-feedback-materialize -> execution/trust/proposal/closure stores -> snapshot refresh -> trust-evolution-summaries -> planner advisory`

Observed latest lineage is incomplete:

`governed execution -> verification -> report/evidence`

Разрыв:

`verification -> canonical feedback materialization`

## FB.1 classification

`PARTIAL_LEARNING`

Причина:

V7 имеет существующую learning architecture и частично использует historical outcomes, но свежие EXEC.2_4/EXEC.5_6 outcomes не доказаны как превращенные в canonical feedback records.
