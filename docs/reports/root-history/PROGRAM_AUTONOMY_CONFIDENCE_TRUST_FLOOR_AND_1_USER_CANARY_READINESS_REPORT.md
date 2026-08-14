# PROGRAM_AUTONOMY_CONFIDENCE_TRUST_FLOOR_AND_1_USER_CANARY_READINESS_REPORT

Дата: 2026-06-08

Проект: V7 Vozduh

Ветка: Updatesystem

Коммит: ccfcfb1cdd05d321f6f0881296482b55c7fb6646

## Короткий итог

Блокер `confidence_too_low` был реальным, а не случайным.

Текущий production-кандидат:

- user: `10.0.0.3`
- route: `awg3 -> awg0`
- confidence: `0.458` = `45.8/100`
- trust: `3.15/100`
- prediction_confidence: `0.396` = `39.6/100`
- risk: `3.319`

Для автономного canary этого недостаточно. Система не должна двигать пользователя автоматически при таких доказательствах.

## Что было найдено

### Confidence

Confidence для автономного dry-run нормализуется в шкалу `0-100`.

Было:

- floor существовал неявно: `70.0`
- blocker: только `confidence_too_low`

Стало:

- floor вынесен явно: `AUTONOMY_CANARY_CONFIDENCE_FLOOR = 70.0`
- текущий кандидат имеет `45.8`, поэтому блокируется корректно

### Trust

Trust был проверен только на `<= 0`, то есть очень низкий положительный trust не получал отдельной причины блокировки.

Это было слабое место объяснимости, но не runtime-опасность: система всё равно блокировалась по confidence.

Стало:

- floor вынесен явно: `AUTONOMY_CANARY_TRUST_FLOOR = 70.0`
- текущий trust `3.15` теперь даёт отдельный blocker: `trust_too_low`

### Prediction confidence

Prediction confidence присутствует, но слабый:

- production: `0.396` = `39.6/100`

Стало:

- floor вынесен явно: `AUTONOMY_CANARY_PREDICTION_CONFIDENCE_FLOOR = 70.0`
- текущий кандидат получает blocker: `prediction_confidence_too_low`

## Калибровка

Пороги не снижались.

Безопасная калибровка применена только в сторону большей ясности:

- добавлена явная модель floors
- добавлена нормализация `0..1 -> 0..100`
- добавлена per-candidate оценка floors
- добавлены отдельные blockers для low trust и low prediction confidence

Это не включает автономию, не меняет planner, не меняет routing, не меняет governance и не двигает пользователей.

## Изменённые файлы

- `admin_core/operator_execution_pipeline.py`
- `tests/unit/test_operator_execution_pipeline.py`

Ключевые места:

- `admin_core/operator_execution_pipeline.py:115` - явные autonomy canary floors
- `admin_core/operator_execution_pipeline.py:167` - нормализация score в `0-100`
- `admin_core/operator_execution_pipeline.py:471` - модель canary floor
- `admin_core/operator_execution_pipeline.py:598` - safety gates и per-candidate floor evaluation
- `tests/unit/test_operator_execution_pipeline.py:314` - тест низких confidence/trust/prediction

## Тесты

Пройдено:

- `python3 -m py_compile admin/v7-admin-api admin_core/operator_execution_pipeline.py`
- `python3 -m unittest tests.unit.test_operator_execution_pipeline tests.unit.test_shadow_autonomy`
- `python3 -m unittest discover tests`

Результат полного набора:

- `399 tests`
- `OK`

## Deploy и truth

Коммит отправлен в GitHub:

- `ccfcfb1 Calibrate autonomy canary confidence gates`

Safe deploy выполнен через approved path:

- `tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --restart-admin-if-changed --json`

Проверки после deploy:

- `tools/v7-truth-check --all --json`: `PASS`
- convergence: `FULLY_ALIGNED`
- runtime action status: `READY_FOR_RUNTIME_ACTION`
- production commit: `ccfcfb1cdd05d321f6f0881296482b55c7fb6646`

## Production dry-run

Production autonomous dry-run выполнен read-only.

Результат:

- `candidate_count=1`
- `canary_autonomy_ready=false`
- `hard_stop_blockers=["confidence_too_low","trust_too_low","prediction_confidence_too_low"]`
- `users_moved=0`
- `apply_executed=false`
- `rollback_executed=false`
- `autonomy_enabled=false`
- `execution_allowed_now=false`

Floor evaluation:

- confidence: `45.8`, pass: `false`
- trust: `3.15`, pass: `false`
- prediction_confidence: `39.6`, pass: `false`

## Вывод

Canary autonomy пока не готова.

Причина не в баге deploy или snapshot gate. Причина в том, что текущий кандидат имеет слабую доказательную базу:

- confidence ниже floor
- trust почти отсутствует
- prediction confidence ниже floor

Система теперь объясняет это правильно и не создаёт ложного ощущения, что проблема только в одном числе.

## Final verdicts

confidence_model_understood=true

trust_model_understood=true

candidate_review_complete=true

autonomy_floor_defined=true

gap_analysis_complete=true

calibration_review_complete=true

safe_calibration_applied=true

tests_pass=true

deploy_pass=true

autonomy_dry_run_pass=true

canary_autonomy_ready=false

single_blocker=confidence_trust_prediction_evidence_below_floor

users_moved=0

apply_executed=false

rollback_executed=false

autonomy_enabled=false

SAFE_NEXT_STEP=COLLECT_OR_MATERIALIZE_CANARY_GRADE_EVIDENCE_FOR_10_0_0_3_AWG3_TO_AWG0_THEN_RETEST_AUTONOMY_DRY_RUN
