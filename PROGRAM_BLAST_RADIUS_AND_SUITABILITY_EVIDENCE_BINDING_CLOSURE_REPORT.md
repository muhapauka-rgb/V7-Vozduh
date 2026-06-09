# PROGRAM BLAST RADIUS AND SUITABILITY EVIDENCE BINDING CLOSURE REPORT

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

## Цель

Проверить не просто какие confidence-компоненты низкие, а почему успешная governed-история плохо превращается в:

- blast-radius confidence
- suitability confidence
- prediction confidence
- service confidence

Без автономии, без apply, без движения пользователей, без изменения planner/governance/authority.

## Короткий вывод

Проблема была реальной.

Успешная governed-история уже существовала в feedback-файлах, но `tools/v7-intelligence-snapshot-refresh` не читал эти файлы как вход для `trust-evolution-summaries`.

Из-за этого:

- authority promotion видел feedback и мог повышать authority;
- trust-evolution почти не видел этот же feedback;
- autonomy confidence оставался низким, хотя execution feedback уже был материализован.

Это был binding gap между existing governed feedback truth и advisory intelligence snapshots.

## Что найдено

### 1. Execution feedback существовал

В сохраненных production evidence были реальные успешные записи:

- `small_batch_stability_evidence/production_execution_events_tail.jsonl`
- `small_batch_stability_evidence/production_closure_records_tail.jsonl`

Примеры содержали:

- `outcome_status=success`
- `target_channel=vless`
- `verification_passed=true`
- `rollback_required=false`
- users: `10.0.0.2`, `10.0.0.3`, `10.0.0.6`

### 2. Snapshot refresh не читал feedback stores

До исправления refresh читал:

- audit logs
- switch history
- rollback history

Но не читал стандартные feedback stores, которые уже использует authority promotion:

- `execution-events.jsonl`
- `runtime-trust.jsonl`
- `proposal-records.jsonl`
- `proposals.jsonl`
- `closure-records.jsonl`

### 3. Blast-radius confidence был искажен

До исправления:

- `blast_radius_confidence=20.0`
- `records_seen=1000`
- `successful_small_operations=0`

Причина: модель получала общий audit tail, включая denial/clearance records, но не получала нормальные successful execution outcomes с явным масштабом.

### 4. Suitability confidence был искажен

До исправления:

- `suitability_confidence=16.277`
- outcomes формально были, но в rows реальные успешные `user:vless` не распознавались как `succeeded=true`.

Причина: нормализатор не понимал поля feedback records:

- `outcome_status`
- `target_channel`
- nested `execution_outcome`
- nested `verification_result`
- nested `rollback_result`

### 5. Prediction/service имеют другую природу

Prediction/service уже были `VALIDATED/MATCHED`.

Но confidence оставался низким из-за входной уверенности snapshot-источников:

- prediction rows имели accuracy около `94-97`, но row confidence около `0.33-0.39`;
- service rows имели correctness `100`, но confidence около `0.3375-0.35`.

Это не тот же binding gap. Это следующий отдельный вопрос: service/prediction source confidence calibration.

## Что исправлено

### `admin_core/intelligence_workers.py`

Расширена нормализация outcome evidence:

- `outcome_status`
- `target_channel`
- `source_channel`
- `recommended_egress`
- `execution_outcome`
- `verification_result`
- `rollback_result`

Добавлен builder:

- `build_blast_radius_evidence_rows(...)`

Он делает важную вещь:

- берет только records с известным outcome;
- группирует per-user execution feedback по operation/audit reference;
- считает blast radius по `users_moved`, `selected_move_count`, `movement_count`, `moved_users`, `selected_moves` или числу users в grouped feedback;
- не считает restore-barrier/clearance/denial шум как неудачное исполнение.

### `tools/v7-intelligence-snapshot-refresh`

Добавлено чтение existing feedback stores:

- `--feedback-log`
- `--execution-events-file`
- `--runtime-trust-file`
- `--proposal-records-file`
- `--closure-records-file`

Дефолтные пути:

- `<state-dir>/execution-events.jsonl`
- `<state-dir>/runtime-trust.jsonl`
- `<state-dir>/proposal-records.jsonl`
- `<state-dir>/proposals.jsonl`
- `<state-dir>/closure-records.jsonl`

Snapshot refresh по-прежнему не меняет runtime, governance, users или routes.

## Before / After

Evidence:

- `blast_radius_suitability_evidence_binding_evidence/before_after_trust_evolution_summary.json`
- `blast_radius_suitability_evidence_binding_evidence/local_rebuilt_snapshots/trust-evolution-summaries.json`

### Before

- `blast_radius_confidence=20.0`
- `successful_small_operations=0`
- `records_seen=1000`
- `suitability_confidence=16.277`
- `candidate_outcomes_count=67`

### After local rebuild with saved production evidence

- `blast_radius_confidence=100.0`
- `successful_small_operations=2`
- `records_seen=2`
- `suitability_confidence=29.023`
- `candidate_outcomes_count=3`
- `blast_radius_evidence_count=2`

Important:

Suitability не стал высоким полностью, потому что реальных bound outcomes пока мало относительно всего candidate pool. Но теперь успешные `10.0.0.2/3/6 -> vless` распознаются как `succeeded=true`.

## Tests

Passed:

- `py_compile`
- `python3 -m unittest tests.unit.test_intelligence_workers`
- `python3 -m unittest discover tests`

Evidence:

- `blast_radius_suitability_evidence_binding_evidence/py_compile.txt`
- `blast_radius_suitability_evidence_binding_evidence/targeted_tests.txt`
- `blast_radius_suitability_evidence_binding_evidence/full_unittest_discover.txt`

Full suite:

- `Ran 420 tests`
- `OK`

## Safety

Confirmed:

- users_moved=false
- apply_executed=false
- autonomy_enabled=false
- planner_changed=false
- governance_changed=false
- authority_changed=false
- runtime_behavior_changed=false in local snapshot refresh result
- governance_behavior_changed=false in local snapshot refresh result

Production SSH/safe deploy/truth-check were not executed in this run because escalated SSH was blocked by the environment usage limit.

## Final Verdicts

governed_history_binding_understood=true

root_cause_identified=true

safe_fix_applied=true

blast_radius_binding_closed=true

suitability_binding_improved=true

prediction_binding_gap_found=false

service_binding_gap_found=false

prediction_service_source_confidence_calibration_needed=true

autonomy_enabled=false

users_moved=0

apply_executed=false

production_deployed=false

production_truth_recheck_done=false

safe_to_deploy_binding_fix=true

safe_to_continue_autonomy_after_production_recheck=false

SAFE_NEXT_STEP=deploy_feedback_binding_fix_then_refresh_snapshots_and_rerun_autonomy_confidence_review

