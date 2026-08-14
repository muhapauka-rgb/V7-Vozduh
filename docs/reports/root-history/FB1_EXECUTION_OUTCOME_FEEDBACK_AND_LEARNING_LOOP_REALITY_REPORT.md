# FB.1 Execution Outcome Feedback And Learning Loop Reality Report

Проект: V7 Vozduh

Дата: 2026-06-12

Режим: READ ONLY. Runtime, routing, users, deploy, apply не менялись.

## 1. Executive Summary

Итоговый вердикт: `PARTIAL_LEARNING`.

V7 уже не является системой "выполнил и забыл". В проекте есть существующий контур outcome feedback:

- canonical feedback builder: `admin_core/operator_execution_feedback.py`
- materialization endpoint: `/api/actions/execution-feedback-materialize`
- stores: `execution-events.jsonl`, `runtime-trust.jsonl`, `proposal-records.jsonl`, `closure-records.jsonl`
- snapshot consumer: `tools/v7-intelligence-snapshot-refresh`
- planner consumer: `tools/v7-users-autoswitch` через `trust-evolution-summaries`

Но свежие реальные исполнения `EXEC.2_4` и `EXEC.5_6` пока доказаны как выполненные, проверенные и rollback-ready, но не доказаны как материализованные в canonical feedback stores. Поэтому обучение существует, но текущий loop не закрыт полностью.

## 2. Outcome Reality Map

Найдены существующие outcome/feedback owners:

| Область | Owner | Статус |
|---|---|---|
| Feedback contract | `admin_core/operator_execution_feedback.py` | EXISTS |
| Feedback materialization | `admin/v7-admin-api` | EXISTS |
| Execution event store | `execution-events.jsonl` | EXISTS |
| Runtime trust store | `runtime-trust.jsonl` | EXISTS |
| Recommendation/proposal store | `proposal-records.jsonl` | EXISTS |
| Closure store | `closure-records.jsonl` | EXISTS |
| Snapshot refresh | `tools/v7-intelligence-snapshot-refresh` | EXISTS |
| Planner consumption | `tools/v7-users-autoswitch` | EXISTS |

Свежие execution outcomes:

| Stage | Result | Canonical feedback доказан |
|---|---|---|
| EXEC.2_4 one user | PASS | NO |
| EXEC.5_6 2 users | PASS | NO |
| EXEC.5_6 5 users | PASS | NO |
| EXEC.5_6 full remaining 8 users | PASS | NO |

## 3. Execution Trace

EXEC.2_4 trace:

`planner -> packet -> restore barrier -> governed apply -> verification -> rollback dry-run -> report/evidence`

Moved user:

- `10.7.0.5`: `awg3 -> vless`

EXEC.5_6 trace:

`planner -> packet -> restore barrier -> governed apply -> verification -> rollback dry-run -> report/evidence`

Moved users:

- Stage A: `10.0.0.2`, `10.0.0.3`
- Stage B: `10.0.0.6`, `10.7.0.3`, `10.7.0.2`, `10.7.0.4`, `10.7.0.6`
- Stage D: `10.7.0.8`, `10.7.0.9`, `10.7.0.10`, `10.7.0.11`, `10.7.0.12`, `10.7.0.13`, `10.7.0.14`, `10.7.0.15`

Break point:

`verification -> canonical feedback materialization`

## 4. Trust Evolution Audit

Trust evolution exists.

`admin_core/intelligence_workers.py` builds `trust-evolution-summaries` from:

- audit records
- switch history
- rollback history
- execution events
- runtime trust
- proposal/recommendation records
- closure records

`admin_core/intelligence_platform.py` defines trust evolution, prediction accuracy, service trust, suitability trust, rollback confidence and blast radius confidence.

`tools/v7-users-autoswitch` consumes `trust-evolution-summaries` in planner advisory and ranking evidence. It does not grant autonomous authority from this data.

Status: `PARTIAL`.

Reason: the machinery exists and is consumed, but fresh execution outcomes are not proven to be materialized into the canonical stores.

## 5. Feedback Loop Audit

| Step | Status | Notes |
|---|---|---|
| Observe | EXISTS | service/snapshot/planner inputs exist |
| Plan | EXISTS | planner creates selected moves |
| Execute | EXISTS | governed apply works |
| Verify | EXISTS | route/registry verification works |
| Outcome | PARTIAL | reports/evidence exist; canonical feedback not proven for latest executions |
| Trust | PARTIAL | trust consumes stores when populated |
| Future decisions | PARTIAL | planner reads trust snapshots, but latest executions may be absent |

## 6. Data Lineage Audit

Intended lineage:

`execution result -> feedback contract -> execution/trust/prediction/recommendation/closure records -> snapshot refresh -> trust-evolution-summaries -> planner/governance evidence`

Observed latest lineage:

`execution result -> verification -> evidence/report`

Lineage break:

`feedback materialization is available, but not proven automatic for EXEC.2_4/EXEC.5_6`.

## 7. Counterfactual

If outcome records disappear:

- governed execution still works
- verification still works
- rollback readiness still works
- planner can still use service/capacity/current snapshots
- trust evolution becomes underfed
- prediction accuracy cannot honestly improve
- recommendation quality cannot be certified from recent real outcomes
- autonomy confidence remains limited
- governance loses historical proof quality

This means outcomes are not optional for the intelligence layer.

## 8. Learning Loop Certification

Final classification: `PARTIAL_LEARNING`.

Not `NO_LEARNING`, because:

- feedback architecture exists
- canonical stores exist
- trust evolution consumes historical outcomes
- planner consumes trust evolution snapshots

Not `FULL_LEARNING`, because:

- latest certified executions are not proven materialized into canonical feedback stores
- execution evidence and learning state are still split
- no evidence found that governed apply automatically closes outcome/trust/prediction/recommendation feedback

## 9. Gap Analysis

Primary gap:

`governed apply result is not proven to automatically become canonical feedback`.

Secondary gaps:

- fresh EXEC.2_4/EXEC.5_6 outcomes need materialization
- feedback closure should reference operation ids and moved users
- rollback readiness should be linked to the same feedback records
- snapshot refresh should be rerun after materialization
- planner should be rechecked after refreshed trust-evolution data

## 10. Next Program Design

Recommended next program:

`PROGRAM FB.2 EXECUTION FEEDBACK MATERIALIZATION AND LINEAGE CLOSURE`

Purpose:

Close the exact break without creating a new feedback system.

Required scope:

1. Reuse `/api/actions/execution-feedback-materialize`.
2. Materialize EXEC.2_4 and EXEC.5_6 outcomes into existing stores.
3. Verify records in:
   - `execution-events.jsonl`
   - `runtime-trust.jsonl`
   - `proposal-records.jsonl`
   - `closure-records.jsonl`
4. Refresh intelligence snapshots through existing approved refresh path.
5. Verify `trust-evolution-summaries` includes the new evidence.
6. Run planner dry-run only.
7. No routing change.
8. No user movement.
9. No new storage.

## 11. Evidence

Evidence folder:

- `docs/reports/evidence/FB1_EVIDENCE/fb1_feedback_owner_code_map.txt`
- `docs/reports/evidence/FB1_EVIDENCE/fb1_trust_recovery_code_map.txt`
- `docs/reports/evidence/FB1_EVIDENCE/fb1_learning_model_code_map.txt`
- `docs/reports/evidence/FB1_EVIDENCE/fb1_prior_report_evidence_map.txt`
- `docs/reports/evidence/FB1_EVIDENCE/fb1_execution_evidence_summary.json`
- `docs/reports/evidence/FB1_EVIDENCE/fb1_lineage_break_summary.md`

## 12. Final Verdict

| Verdict | Value |
|---|---|
| final_verdict | `PARTIAL_LEARNING` |
| outcome_reality_mapped | `true` |
| execution_trace_mapped | `true` |
| trust_evolution_exists | `true` |
| feedback_loop_exists | `partial` |
| data_lineage_complete | `false` |
| canonical_feedback_owner_exists | `true` |
| latest_exec_feedback_materialized | `false` |
| new_feedback_system_needed | `false` |
| safe_next_step | `PROGRAM FB.2 EXECUTION FEEDBACK MATERIALIZATION AND LINEAGE CLOSURE` |

Answer to the core question:

V7 learns from its own actions partially. The architecture and consumers exist, but the latest real executions are not yet proven to be converted into canonical feedback records. The next step is not new architecture; it is closing the existing materialization lineage.
