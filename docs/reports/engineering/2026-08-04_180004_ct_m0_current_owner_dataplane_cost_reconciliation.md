Mission ID: `V7_CONSTANT_TIME_COHORT_FAILOVER_M0_CURRENT_OWNER_DATAPLANE_AND_O_N_COST_RECONCILIATION_V1`
Run Nonce: `V7_CT_M0_20260804T110004Z`

# Engineering Report: CT-M0 current owner, data plane и O(N) cost reconciliation

Дата: 2026-08-04

## Итог

CT-M0 завершён как read-only `DISCOVERY_COMPLETION`. Текущий production hot
path доказан как последовательный `O(N)`: один per-user Planner result,
subprocess, table mutation, полный rewrite `users.registry`, visibility check,
service verification и audit/checkpoint на участника. Фактический успешный
forward+reset baseline равен `141.353447 s`.

Архитектурного запрета на constant-time model нет. Текущий Linux data plane
уже использует policy routing и имеет fwmark/nftables substrate, но class map,
class membership generation и atomic class-to-egress commit отсутствуют.
Вердикт: `KERNEL_CLASS_INDIRECTION_FEASIBILITY_PROVEN`, не
`CURRENT_IMPLEMENTATION_PRESENT`.

Machine-readable contract:
`docs/reports/engineering/evidence/2026-08-04_180004_ct_m0_current_owner_dataplane_cost_contract.json`.

## Discover -> Reuse -> Extend -> Implement

Новый route owner, Planner, Runtime, registry, queue, watcher, Time store,
Authority или Outcome store не создавались. По смыслу проверены существующие
owners, а не только совпадения названий.

Переиспользуются без повторной реализации:

- hard-failure/Matrix event production;
- exact fresh Matrix path receipt и invalidation rules;
- execution-control safety gates;
- bounded cohort checkpoint/circuit breaker;
- rollback/reset safety semantics;
- Outcome/Replay/Learning consumers;
- Permanent Polygon и Time foundation.

Текущий comprehensive Planner и `v7-user-switch` сохраняются только как
legacy exception path. Для массового совместимого incident их автоматический
выбор запрещён контрактом
`LEGACY_PER_USER_PATH_FOR_MASS_COMPATIBLE_INCIDENT_FORBIDDEN`.

## Production data-plane reality

Read-only production audit подтвердил: `125` registry rows, `125` уникальных
user tables, `130` source rules, `128` lookup tables, `7` enabled egress,
`0` netns, `0` nft maps и `1` fwmark rule. Это текущая модель
`one source rule + one table per user`, а не class indirection.

`tools/v7-users-autoswitch` выполняет `for move in selected_moves`, повторяя
fresh validation, `v7-user-switch`, route visibility и service verification.
`tools/runtime-support/v7-user-switch` берёт global flock, меняет одну routing
table, создаёт per-user assignment, затем полностью переписывает
`users.registry`. Поэтому cohort size непосредственно увеличивает hot-path
работу.

## Semantic class и prepared decision

Существующая `route_class` по required services полезна, но недостаточна для
kernel class identity. Каноническая совместимость должна включать source
channel profile, service-routing compatibility, policy set, eligible target
set, capacity bucket, path fingerprint, correlation domain и exception
boundary. Один общий source не делает пользователей одним routing class.

Prepared decision сейчас не производится как durable generation-bound объект
до аварии. CT-M0F должен связать существующие Matrix/topology/capacity/policy/
membership события с одной подготовленной проекцией. Hot validator проверяет
только объявленные generations/fingerprints; rebuild полного World Model после
failure запрещён.

## Hot path и durable closure

Целевой hot path:

`failure signal -> prepared decision -> bounded validation -> compact class
Packet/lease -> O(1)/O(K) generation commit -> kernel visibility -> aggregate
fast verification -> durable closure obligation`.

Outcome, Replay, Learning и полная exception reconciliation остаются за hot
path, но не являются необязательным «потом». Crash между kernel commit и
publication восстанавливает obligation из canonical generation и kernel
truth через существующих consumers.

Fresh compatible Matrix receipt запрещает полный service refresh до cutover.
Полный verifier допустим только при missing/stale receipt, path/service-set/
identity mismatch или unhealthy service evidence.

## Cost и performance ledger

Baseline owner: `admin_core.operator_execution_pipeline.execution_performance_foundation`.
Последний immutable receipt: `perfclose_6e6c4fa62f834a8d4b88da24`.

- Planner: `17.307274 s`;
- Packet+lease: `0.235222 s`;
- restore barrier: `0.259674 s`;
- apply+verification: `40.809895 s`;
- reset: `82.591859 s`;
- successful forward+reset: `141.353447 s`.

Точные `files_opened` и `fsync_count` существующий receipt не публикует; они
не выдумывались. CT-M0F расширяет тот же Time owner counters для scans, writes,
serialized bytes, subprocesses, locks, probes, unknown time и `10 vs 10,000`.

## Kernel, NAT и migration boundary

Positive feasibility основана на уже доступных policy-routing/fwmark/nftables
primitives и существующем route owner extension point. Выбор точного internal
primitive относится к CT-M0F/CT-M1, а не к этому read-only аудиту.

New-flow class cutover, atomic generation, crash reconciliation, rollback и
forward recovery должны быть доказаны в Polygon. Поведение уже существующих
NAT/conntrack flows не сертифицировано и зафиксировано как exact Polygon
kernel proof residual. Production claim не сделан.

## BDP/OMP consumption

Reality Gate disposition: `PASS_EXISTING_OWNER_EXTENSION_ONLY`. Live generic
capability-graph evaluation честно остаётся
`NOT_EVALUATED_PROGRAM_FRONTIER_PREEMPTS_CAPABILITY_GRAPH`: CT-M0 является уже
утверждённой Program dependency, поэтому существующий OMP program-frontier
consumer, а не параллельный generic capability Candidate, admitted CT-M0F.

CT-M0F admitted `READY`:
`V7_CONSTANT_TIME_COHORT_FAILOVER_REUSABLE_FAST_PRIMITIVES_CLOSURE_V1`.

CT-M1 formed `FORMED_DEPENDENCY_BLOCKED`:
`V7_CONSTANT_TIME_COHORT_FAILOVER_CLASS_BUCKET_KERNEL_PRIMITIVE_AND_CRASH_PROTOCOL_POLYGON_V1`.

Одновременно READY только CT-M0F. Incident frontier, Natural L8 lane и
Stage-48 readiness сохранены; Stage 48 не запускалась.

## Effects и terminal

Runtime apply, routing mutation, user movement, Candidate/Packet/lease,
restore-barrier write, rollback apply, Authority expansion и Production
Maturity change: `NONE`.

Focused CPS atomicity/live-pointer/Mission-identity suite: `PASS`. CPS atomic
reread, derived projections, dependency graph, Mission identity, completion
gate и OMP pointer consistency: `PASS`.

Terminal:
`CURRENT_DATAPLANE_CLASS_INDIRECTION_FEASIBILITY_AND_MINIMAL_IMPLEMENTATION_FRONTIER_CONSUMED`.

Exact next Product Evolution Frontier:
`V7_CONSTANT_TIME_COHORT_FAILOVER_REUSABLE_FAST_PRIMITIVES_CLOSURE_V1`.
