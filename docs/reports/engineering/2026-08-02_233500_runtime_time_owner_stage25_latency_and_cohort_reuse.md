# Engineering Report: Runtime Time owner, Stage-25 latency и cohort reuse

Дата: 2026-08-02  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Mission: `STAGE_25_FASTEST_SAFE_RUNTIME_PATH_PROVEN_V1` continuation  
Runtime commit: `0d29365b50ed4fe4752470118a9457917e0c0dbc`

## Итог

Discovery не выявил отсутствующую «систему времени». Каноническая семантика уже принадлежит `docs/reference/V7_RUNTIME_MODEL.md`; production analysis owner уже существует в `admin_core.operator_execution_pipeline.execution_performance_foundation`, а bounded observability consumer — в `admin_core.operator_observability`. Исходная классификация: `TIME_OPTIMIZATION_LOOP_PARTIAL` и `EXISTING_TIME_OWNER_CONSUMER_BINDING_GAP`.

Stage-25 producer уже использовал `time.monotonic_ns()` и сохранил compact `performance_timeline`. Он доказал:

- forward child: `3,276,881,978 us`;
- два recovery/reset окна: `1,696,614,625 us` и `2,378,035,487 us`;
- aggregate verification: около `18.715 s`;
- governed member window: около `92.882–147.411 s`;
- Outcome/Replay/Learning lookup и route truth не были доминирующими затратами.

Точный residual находился не в Matrix timer и не в ожидании Authority. Один immutable allocation subset исполнялся как полный Planner -> Candidate -> Packet -> lease -> clearance -> apply -> verification цикл для каждого пользователя. Действующая owner-issued standing policy уже разрешает до `48` пользователей в одной транзакции при `max_concurrent_transactions=1`, а существующий L3 executor уже поддерживает cohort Packet, operation-scoped binding, per-user apply result, verification и rollback items.

## Реализованное исправление

Новый owner, ledger, watcher, очередь, Runtime или Authority не создавались.

1. L3 governed transaction теперь формирует compact monotonic breakdown:
   `planner`, `packet_and_lease`, `restore_barrier`, `apply_and_verification`, `feedback_and_learning`.
2. Elapsed вычисляется только через process-local `time.monotonic_ns`; UTC остаётся только audit/order metadata.
3. Projection немедленно потребляется существующим `execution_performance_foundation`, включая slow-path classification.
4. Timing хранится один раз на cohort transaction, а не дублируется в каждой per-user evidence row: пять span rows на Packet, raw identity list отсутствует.
5. Availability-first forward path использует один свежий cohort Packet/lease на точный immutable allocation subset вместо полного lifecycle на каждого участника. Конкурентность остаётся `1`; policy ceiling, fresh target/capacity, Candidate, Packet, lease, verification, rollback/containment и circuit breaker сохранены.

Это устраняет до `N-1` повторных полных Planner/Packet lifecycle на target subset. Для Stage 48 с одной allocation целью число forward governed invocations уменьшается с `48` до `1`. Network/service verification остаётся реальным safety lower bound и не объявляется устранённым.

## Storage и overhead

Production owner inventory показывает bounded readers/rotated owners; крупнейшие текущие stores имеют размер порядка 2.3–6.3 MB (`execution-events.jsonl`, `closure-records.jsonl`, `operator-execution-audit.jsonl`, `l3-runtime-state.json`). Новая projection не создаёт отдельное хранилище и добавляет ровно пять compact spans на transaction. Фактический no-effect microbenchmark: `10,000` projections за `258.202 ms`, `25.82 us` на transaction, `1,189 bytes` serialized; cohort timing не размножается на число пользователей.

## Проверка

- `tests.unit.test_governed_canary_cli`: PASS, 108 tests;
- `tests.unit.test_service_failure_episode` + `tests.unit.test_operator_execution_pipeline`: PASS, 88 tests;
- итоговый affected set: PASS, 196 tests;
- safe-deploy manifest: PASS; единственный runtime delta — `tools/v7-governed-canary-dry-run-cycle`;
- production deploy: PASS, release `deploy-z8-14-Updatesystem-0d29365-20260802T233237`;
- Authority expansion: `false`;
- Production Maturity change: `false`;
- ручной Matrix запуск: не выполнялся;
- Stage-25 credit: не повторялся.

## Current production boundary

До deploy обычный Matrix Stage-48 preflight завершался `STOP_SAFE` без mutation: `availability_first_source_cohort_too_small`. Текущая aggregate route truth: `41` certification identities на `vless`, ещё `11` находятся на других каналах. Поэтому Stage 48 не может законно выбрать exact cohort 48 и не должен запускаться ради benchmark.

Первый ordinary Matrix tick после финального deploy стартовал `2026-08-02T16:38:10Z`, завершился rc=0 в `16:40:49Z` и реально потребил production entrypoint. Stage-48 consumer остановился до Candidate/Packet/lease/mutation с blockers `availability_first_controlled_source_missing` и `availability_first_source_cohort_too_small`; `runtime_mutation_performed=false`, `users_moved=0`. Его bounded critical-path preflight составил `30.433350 s`: restored reconciliation `6.982397 s`, partial reconciliation `0.284692 s`, planner/allocation `23.149463 s`.

Законный terminal — owner-backed `STOP_SAFE` с automatic re-entry; это не опровержение cohort optimization и не разрешение искусственно перемещать identities. Полный post-repair production latency для cohort Packet может быть заявлен только после реальной admitted owner-driven transaction.

## Terminals

- `V7_EXISTING_TIME_CAPABILITY_DISCOVERED`
- `V7_TIME_CANONICAL_OWNER_IDENTIFIED`
- `V7_TIME_STORAGE_AND_RETENTION_IDENTIFIED`
- `V7_STAGE_25_EXISTING_TIMING_DATA_RECONSTRUCTED`
- `V7_TIME_PRODUCER_CONSUMER_CHAIN_AUDITED`
- `V7_TIME_CAPABILITY_REUSED_OR_EXACT_GAP_PROVEN`
- `GOVERNED_MEMBER_WINDOW_MONOTONIC_BREAKDOWN_IMPLEMENTED`
- `STAGE_25_AVOIDABLE_FORWARD_LIFECYCLE_MULTIPLICATION_REPAIRED`
- `STAGE_48_OPTIMIZED_RUNTIME_READY_PENDING_LIVE_SOURCE_COHORT`

`STAGE_48_OPTIMIZED_RUNTIME_READY` и production p50/p95 не заявляются до реального owner-driven cohort execution. Точный re-entry: ordinary Matrix observation, в котором controlled source содержит не менее 48 current certification identities и все существующие health/capacity/policy gates проходят.
