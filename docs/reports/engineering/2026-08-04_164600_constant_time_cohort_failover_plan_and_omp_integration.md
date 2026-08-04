# Engineering Report: план constant-time cohort failover и интеграция с OMP

Дата: 2026-08-04

## Результат

В существующий
`V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1` добавлена V4.0 capability
plan для перехода от user-linear route mutation к class/bucket generation
cutover с вычислительной сложностью, независимой от количества пользователей и
ограниченной сертифицированным числом buckets/targets.

Новая Program не создавалась. Текущий CPS frontier, Stage-48 admission,
Authority, Runtime, routing, users и Production Maturity не изменялись.

## Основные дополнения

- обязательный read-only M0 data-plane/O(N) feasibility audit;
- доказательство реального Linux primitive до реализации;
- semantic routing-class identity и exception overlay;
- canonical membership/class generation без массового registry rewrite;
- bounded O(K) multi-target partitioning;
- PREPARED -> CAS -> kernel commit -> observed -> COMMITTED crash protocol;
- one-time bounded migration, shadow parity и legacy fallback;
- one class/bucket Packet and lease;
- fast/deferred verification separation;
- new-flow, existing-flow/conntrack и application SLO separation;
- generation rollback и forward recovery;
- logical + kernel Polygon certification at 10,000 members;
- residual-based controlled production and independent Authority decision.

## OMP closure integration

OMP обновлена до V4.63. Добавлена Section 46 с exact producer/output/consumer/
completion/successor map для CT-M0..CT-M9.

Каждая Mission обязана закрыть:

```text
trigger -> producer -> output -> consumer -> behavior -> verification
-> next output -> CPS -> residual -> successor/legal terminal
```

Открытая стадия без `next_required_consumer`, `reentry_condition` или durable
successor классифицируется `BROKEN_CAUSAL_LINEAGE`. Tests, commit, deploy,
dashboard, report или preview не являются terminal consumer.

Incident Frontier и Product Evolution Frontier остаются параллельными. Legacy
per-user execution сохраняется как fallback, пока exact migrated class/bucket
scope не пройдёт Polygon, controlled-production и owner-backed admission.

## Activation boundary

Документ является `APPROVED_EXECUTION_PLAN`, а не live Mission admission.
CPS остаётся единственным activation and sequencing owner.

Первый допустимый future frontier:

`V7_CONSTANT_TIME_COHORT_FAILOVER_M0_CURRENT_OWNER_DATAPLANE_AND_O_N_COST_RECONCILIATION_V1`

M0 завершается только после потребления результата BDP Reality Gate и OMP
Candidate Admission с точным CT-M1 successor либо legal terminal/re-entry.

## Forbidden effects

В ходе plan integration отсутствуют:

- production apply;
- routing mutation;
- user movement;
- Packet/lease creation;
- restore-barrier write;
- rollback/forward-recovery apply;
- Authority or policy mutation;
- Production Maturity change;
- новая Runtime/Planner/registry/watcher/queue/owner/truth source.
