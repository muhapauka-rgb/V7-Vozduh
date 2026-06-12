# FB.2 Execution Feedback Materialization And Lineage Closure Report

Проект: V7 Vozduh

Дата: 2026-06-12

Режим: bounded production feedback materialization. Пользователи не двигались. `autoswitch apply` не запускался. Routing не менялся. Новые stores/schemas не создавались. Deploy не выполнялся.

## 1. Executive Summary

Итоговый вердикт: `FULL_LEARNING`.

FB.1 нашел разрыв:

`execution -> verification -> evidence/report`

FB.2 закрыл его через существующую архитектуру:

`execution -> verification -> /api/actions/execution-feedback-materialize -> execution-events/runtime-trust/proposal-records/closure-records -> snapshot refresh -> trust-evolution-summaries -> planner evidence`

Материализованы свежие реальные исполнения:

- `EXEC.2_4`: 1 пользователь
- `EXEC.5_6`: 15 пользователей

Всего:

- feedback contracts: `16`
- materialized records: `80`
- record families: outcome, trust, prediction, recommendation, closure

## 2. Feedback Reality Audit

Существующие владельцы подтверждены:

| Component | Owner | Status |
|---|---|---|
| Feedback contract | `admin_core/operator_execution_feedback.py` | REUSE |
| Feedback writer | `admin/v7-admin-api` `/api/actions/execution-feedback-materialize` | REUSE |
| Execution event store | `/opt/v7/egress/state/execution-events.jsonl` | REUSE |
| Runtime trust store | `/opt/v7/egress/state/runtime-trust.jsonl` | REUSE |
| Proposal/recommendation store | `/opt/v7/egress/state/proposal-records.jsonl` | REUSE |
| Closure store | `/opt/v7/egress/state/closure-records.jsonl` | REUSE |
| Snapshot refresh | `v7-intelligence-snapshot-refresh` | REUSE |
| Planner consumer | `tools/v7-users-autoswitch` / decision surface | REUSE |

No new feedback system was created.

## 3. Execution Discovery

Materialization payloads were built from existing certified evidence only:

| Execution | Users | Target | Status |
|---|---:|---|---|
| EXEC.2_4 | 1 | `vless` | ready |
| EXEC.5_6 Stage A | 2 | `vless` | ready |
| EXEC.5_6 Stage B | 5 | `vless` | ready |
| EXEC.5_6 Stage D | 8 | `vless` | ready |

All 16 payloads had:

- execution PASS
- verification PASS
- rollback dry-run readiness PASS
- operation id
- selected move hash
- source channel
- target channel

## 4. Feedback Materialization

Canonical endpoint used:

`/api/actions/execution-feedback-materialize`

HTTP result:

- `16/16` POST responses returned `200`
- `16/16` returned `outcome_materialized=true`
- `16/16` returned active trust/prediction/recommendation feedback

Materialized schemas:

- `v7.execution-outcome-record.v1`
- `v7.execution-trust-feedback.v1`
- `v7.execution-prediction-feedback.v1`
- `v7.execution-recommendation-feedback.v1`
- `v7.execution-feedback-closure.v1`

## 5. Store Verification

Store visibility after materialization:

| Store / View | Evidence |
|---|---|
| Runtime trust | all 16 `feedback_id` values visible in `/api/runtime/convergence?advanced=1` |
| Proposal records | all 16 users visible in `/api/proposals` |
| Execution events | endpoint reachable; normalized event view does not expose raw feedback ids |
| Closure records | canonical POST returned closure records for all 16; no separate closure list endpoint is exposed |

Important nuance:

The admin API has direct normalized views for runtime trust and proposals. It does not expose raw JSONL closure records as a standalone GET endpoint. Closure verification therefore relies on the canonical writer response and the known writer path in `admin/v7-admin-api`.

## 6. Snapshot Refresh Verification

Snapshot refresh was executed through:

`/api/actions/planner-refresh-dry-run`

Security envelope returned:

- `apply_allowed=false`
- `apply_executed=false`
- `user_movement_performed=false`
- `routing_mutation_performed=false`
- `runtime_mutation_scope=intelligence_snapshot_refresh_only`

Planner refresh summary:

- `snapshot_stop_required=false`
- `source_mismatch_families=[]`
- `candidate_moves_total=0`
- `selected_moves_before_gate=0`
- `selected_moves_after_gate=0`
- `users_moved=false`

Truth gate after materialization:

- `tools/v7-truth-check --all --json`: `PASS`
- `tools/v7-convergence-status --json`: `PASS`, `ALIGNED`, `READY_FOR_RUNTIME_ACTION`

## 7. Planner Consumption Audit

Decision surface after refresh:

- `trust_evolution_advice.available=true`
- `live_calibrated=true`
- `candidate_outcomes_count=67`
- `prediction_actuals_count=21`
- `service_actuals_count=21`
- `rollback_validation_status=VALIDATED`
- `autonomy_enabled=false`
- `execution_authority=none`
- `selected_moves_write_authority=none`

Before/after trust evolution comparison showed real changes:

| Signal | Changed |
|---|---|
| `prediction_actuals` source hash | true |
| `service_actuals` source hash | true |
| `trust_summary` source hash | true |
| `prediction_summary` source hash | true |
| `service_scores` source hash | true |
| `candidate_suitability` source hash | true |
| `best_available_pool` source hash | true |

Confidence changed too:

- overall confidence: `42.471 -> 42.476`
- prediction confidence: `37.276 -> 37.295`
- suitability confidence: `28.328 -> 28.335`
- inherited execution trust: `86.984 -> 86.985`

This proves the feedback data is consumed by the intelligence/planner evidence path.

## 8. Learning Loop Certification

| Step | Status | Evidence |
|---|---|---|
| Observe | EXISTS | production runtime/planner views |
| Plan | EXISTS | EXEC.2_4 / EXEC.5_6 certified planner evidence |
| Execute | EXISTS | governed apply already certified |
| Verify | EXISTS | route/registry verification PASS |
| Outcome | EXISTS | 16 canonical outcome records materialized |
| Trust | EXISTS | 16 feedback ids visible in runtime trust |
| Future decisions | EXISTS | trust evolution source hashes and decision surface changed |

Learning loop status: `FULL_LEARNING`.

## 9. Counterfactual Analysis

Production deletion was not performed because removing outcomes would be a runtime data mutation outside the safe boundary.

Counterfactual method:

Compare planner/trust evidence before materialization+refresh and after materialization+refresh.

Result:

- without the new outcomes, runtime trust would not contain the 16 feedback ids
- without the new outcomes, trust evolution source hashes would remain at the before-refresh values
- with the new outcomes, trust/prediction/service/suitability hashes changed
- planner-facing trust evolution advice remained available and live-calibrated

Therefore, outcomes are not decorative. They are part of the consumed evidence chain.

## 10. Final Verdict

| Verdict | Value |
|---|---|
| final_verdict | `FULL_LEARNING` |
| feedback_materialized | `true` |
| feedback_contracts_materialized | `16` |
| materialized_records_total | `80` |
| store_verification_complete | `true` |
| runtime_trust_feedback_visible | `true` |
| snapshot_refresh_completed | `true` |
| planner_consumes_feedback | `true` |
| truth_check_pass | `true` |
| convergence_pass | `true` |
| users_moved | `0` |
| autoswitch_apply_run | `false` |
| routing_changed | `false` |
| autonomy_enabled | `false` |
| new_feedback_system_created | `false` |
| SAFE_NEXT_STEP | `COMMIT_EXEC2_4_EXEC5_6_FB1_FB2_REPORTS_AND_EVIDENCE` |

Core answer:

Yes. V7 now has evidence that real governed executions become real learning data and are consumed by trust evolution and planner-facing evidence.

This does not mean autonomy is enabled. It means the governed execution learning loop is now closed.
