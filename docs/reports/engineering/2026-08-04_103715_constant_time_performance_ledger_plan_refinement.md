# Engineering Report: performance-ledger усиление constant-time плана

Дата UTC: `2026-08-04T10:37:15Z`

## Результат

Существующий `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM` обновлён до
V4.2, его OMP-интеграция — до V4.65. Новая программа, Mission container,
Time owner, store, registry, log owner, daemon, watcher, Planner, Runtime или
Authority system не создавались.

## Добавленные обязательные контракты

1. `CONSTANT_TIME_FAILOVER_PERFORMANCE_LEDGER` — projection существующего
   `execution_performance_foundation` и Time owner после каждой CT Mission.
2. `LEGACY_EXCEPTION_PATH_BASELINE_AND_REQUIRED_SLO_PROVEN` — разложение
   текущего длительного fallback и evidence-derived bounded SLO.
3. `PREPARED_DECISION_CONTINUOUS_PRODUCER_AND_FRESHNESS_CONSUMER_PROVEN` —
   prepared decision существует до аварии и обновляется существующими owners.
4. `FRESH_MATRIX_RECEIPT_HOT_PATH_REUSE_GUARD_PROVEN` — совместимый fresh
   Matrix receipt не допускает возврат полного service verification в hot path.
5. `CUTOVER_HIDDEN_O_N_GUARD_PROVEN` — incident cutover не сканирует/хеширует
   полный cohort, не переписывает registry и не создаёт per-user lifecycle.

## Performance closure

Каждая исполненная или динамически сжатая Mission теперь обязана показать:

```text
old critical path
-> removed blocking work
-> new critical path
-> measured latency and operation counters
-> remaining blocking work
-> exact next latency residual
-> existing Time/OMP consumer acknowledgement
```

Unknown time не может быть записано как ноль. Улучшение одного интервала не
скрывает регрессию другого. 10 и 10 000 участников сравниваются одновременно
по времени и по числу scans, rewrites, audits, probes, locks, processes и
per-member execution objects.

## Effect boundary

Изменение является plan/governance-only. CPS frontier, Runtime, routing,
пользователи, Packet execution, restore barrier, Authority и Production
Maturity не изменялись.

Текущий legal terminal:
`APPROVED_CAPABILITY_PLAN_NOT_LIVE_FRONTIER`.
