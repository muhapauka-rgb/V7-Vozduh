# CT-M0F: привязка performance ledger к существующим owners

Время: `2026-08-04T17:22:50Z`

Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

Mission: `V7_CONSTANT_TIME_COHORT_FAILOVER_REUSABLE_FAST_PRIMITIVES_CLOSURE_V1`

Bounded delta: `CT_M0F_E_CONSTANT_TIME_PERFORMANCE_LEDGER_OWNER_BINDING_V1`

## Discover / Reuse

CT-M0 disposition и исходный код подтвердили:

- канонический Time owner уже существует:
  `admin_core.operator_execution_pipeline.execution_performance_foundation`;
- autoswitch уже публикует process-local `time.monotonic_ns` spans;
- governed transaction receipt уже является durable consumer;
- отдельный store, ledger owner, Runtime, watcher или Planner не требуется;
- residual был не в отсутствии измерений как таковых, а в отсутствии
  машинного consumer для nested spans и hidden-O(N) work counters.

## Extend / Implement

Расширены только существующие owners:

1. Autoswitch receipt публикует bounded `hot_path_work_counters`: число
   прочитанных planner rows, process/probe/lock counts, selected-move artifact
   lower bound и явные unknown counters.
2. Existing Time owner потребляет nested spans в compact projection
   `v7.constant-time-failover-performance-ledger.v1`.
3. Неизвестные `registry_rows_rewritten` и `serialized_member_bytes` не
   выдумываются и остаются `UNKNOWN`.
4. Existing governed transaction receipt потребляет projection и сохраняет
   его вместе с текущим timing evidence.

Новый durable store или truth source не создан.

## Verification

- Python compile с изолированным bytecode cache: `PASS`;
- `tests.unit.test_operator_execution_pipeline`: `PASS`;
- `tests.unit.test_governed_canary_cli`: `PASS`;
- `tests.unit.test_v7_users_autoswitch_policy`: `PASS`;
- всего: `331/331 PASS`;
- purity guard существующего Time owner: `PASS`;
- runtime apply, routing mutation, user movement, Candidate/Packet/lease,
  restore-barrier write, rollback apply, Authority expansion и Production
  Maturity change: `NONE`.

До commit безопасный truth показал CPS semantic consistency `PASS`; общий
convergence ожидаемо `NO-GO` только из-за ещё не committed runtime delta и
ранее существующих пользовательских report-файлов. Эти файлы не входят в
owned scope.

## Performance-ledger delta

До изменения existing Time owner видел только coarse execution durations и не
мог потребить nested CT spans/work counters.

После изменения он различает:

- detection;
- prepared validation;
- Packet/lease;
- canonical CAS;
- kernel commit;
- visibility;
- fast verification;
- new-flow recovery;
- closure activation;
- deferred verification;
- rollback/forward recovery;
- N/K dependency и bounded work counters.

Отсутствующие producer measurements остаются точным residual, а не нулём.

## Bounded terminal и successor

Этот delta закрывает только обязательную performance-ledger/hidden-O(N)
связь CT-M0F-E и не объявляет CT-M0F завершённой.

Terminal:
`CT_M0F_E_CONSTANT_TIME_PERFORMANCE_LEDGER_OWNER_BINDING_IMPLEMENTED`.

Exact successor внутри той же Mission:
`CT_M0F_E_CONTINUOUS_PREPARED_DECISION_AND_FRESHNESS_CONSUMER_BINDING_V1`.

CT-M0F-V остаётся dependency-blocked; CT-M1 остаётся
`FORMED_DEPENDENCY_BLOCKED`. Production validation в этом bounded invocation
не допускается.
