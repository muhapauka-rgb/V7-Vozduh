# V7 Permanent Polygon Target-Level Completion Plan

Document class: `EXECUTION_PLAN_CANDIDATE`

Approval and activation state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`

This document must not be used to determine whether the plan is approved, active, paused, waiting or terminal. It is a proposed bounded continuation plan under the existing OMP, BDP, CPS, FSSE/Engineering Polygon and component owners. It creates no new Runtime, Planner, scheduler, queue, daemon, truth source, Authority owner or Production Maturity owner.

## 1. Target Outcome

Довести Permanent Polygon до уровня, на котором он не ждёт появления большинства реальных инцидентов, чтобы начать инженерную проверку, а заранее проектирует owner-backed ситуации, исполняет их через реальные V7 owners в изоляции, потребляет результат, при необходимости формирует repair Mission и автоматически продолжает следующую obligation generation.

Целевой контур:

```text
current system/change/gap/requirement
-> owner-backed obligation
-> sufficient-fidelity decision
-> generated topology/workload/fault/time situation
-> real V7 owner execution in isolation
-> outcome/counterfactual/shadow Learning
-> OMP consumer and criterion coverage
-> mismatch -> BDP -> repair Mission -> automatic return
-> selective replay
-> next generation
-> event-driven reentry
```

Ожидание L7/L8 не должно останавливать L1-L6. При этом Polygon evidence никогда не подменяет controlled или natural production evidence, не предоставляет Authority и не повышает Production Maturity.

## 2. Honest Current Baseline

Перед исполнением baseline обязан заново читаться из CPS. Текущий planning snapshot:

- production-deployed и production-called engineering automation подтверждена;
- local/GitHub/production alignment был подтверждён отдельно от program completeness;
- потреблены engineering criteria CAP-U02, U03, U04, U05, U06, U10 и U11;
- current exact obligation: `POLYGON-CAP-U07-SHADOW_LEARNING_REPRESENTATION_MATRIX-G1`;
- Mission: `V7_POLYGON_CAP_U07_SHADOW_LEARNING_REPRESENTATION_MATRIX_V1`;
- Mission state: `ADMITTED_READY_FOR_DISPATCH`;
- external reentry: `PENDING`;
- CAP-U12, U13, U14, U16 и U20 не имеют прямых owner executor adapters;
- L7/L8 остаются отдельными production evidence remainders;
- `FULLY_ALIGNED` означает environment/version equality, а не полное достижение target-level Polygon.

## 3. Permanent Execution Laws

### 3.1 Discover -> Reuse -> Extend -> Implement

Перед каждым изменением:

1. прочитать CPS, OMP, durable criterion registry и текущий report;
2. найти существующего owner, producer, consumer и verification path;
3. доказать отсутствие уже работающей реализации;
4. переиспользовать или минимально расширить существующего owner;
5. создавать новый технический модуль только после necessity/duplication/architecture gates.

### 3.2 Living Dependency And Consumer Map

Missions ниже — capability stages, а не обязательные пустые контейнеры. После каждой consumed transition OMP обязан пересчитать остаток:

- полностью закрытая следующая Mission получает `MISSION_NOT_REQUIRED_ALREADY_CONSUMED`;
- частично закрытая сокращается до точных remaining criteria;
- связанные stages могут объединяться только при явных owner, identity, consumer, verification, isolation и terminal semantics;
- нельзя повторять experiment без invalidation reason;
- конец каждого действия обязан стать producer input следующего consumer.

### 3.3 No-Wait And Substrate Degradation

- L7/L8 wait является lane-local boundary, не global program stop.
- Отсутствие namespaces, tc/netem, Docker, root или external infrastructure не останавливает независимые L1/L2/model/identity/outcome/counterfactual/shadow Learning/logical-scale criteria.
- Используется максимальная честно доступная fidelity.
- Заблокированный higher-fidelity criterion сохраняется с точной причиной и reentry condition.
- Весь program может остановиться только если не осталось независимого owner-backed L1-L6 work и доказана точная infrastructure/Authority boundary.

### 3.4 Evidence And Safety Separation

На всём плане запрещены:

- production Runtime apply;
- production routing mutation;
- production packet execution;
- production user movement;
- restore-barrier write;
- rollback apply;
- daemon/timer enablement без отдельного owner authorization;
- Authority expansion;
- Production Maturity increase из Polygon evidence;
- выдача L1-L6 за L7/L8.

### 3.5 Report After Every Mission

Каждая Mission/исполнительный prompt завершает работу компактным report в `docs/reports/engineering/`, содержащим:

- exact objective и Mission identity;
- direct closure и lawful anticipatory closures;
- reused/extended owners;
- real producer/consumer/behavior change/next output;
- tests, experiments, evidence class и forbidden effects;
- reduced/merged/not-required later Missions;
- exact remaining frontier;
- deploy/truth/convergence/equality, если применимо.

## 4. Mission Sequence

## Mission 0 — CPS Semantic Integrity And Historical Lifecycle Reconciliation

Mission ID: `V7_PERMANENT_POLYGON_CPS_SEMANTIC_INTEGRITY_AND_PROJECTION_RECONCILIATION_V1`

Objective: устранить источник stale projections до следующего autonomous CAP-U07 run.

Must:

1. Исправить atomic CPS state projection, чтобы Section 0, Phase 6, protected WIP, deterministic sequence, dashboard capability rows и durable criterion registry строились из одной generation.
2. Синхронизировать:
   - `PHASE_6_CERTIFICATION_FRONTIER`;
   - `PHASE_6_EXACT_NEXT_ACTION`;
   - `PHASE_6_EXECUTABLE_FRONTIER`;
   - current Polygon obligation и next Mission.
3. Исправить lane semantics:
   - engineering stop = `NONE`, пока есть CAP-U07 или другое L1-L6 work;
   - controlled lane stop = `REAL_WORLD_LIMIT`, если нет qualifying controlled evidence;
   - natural lane stop = `REAL_WORLD_LIMIT`, если нет natural evidence;
   - global stop = `NONE`, пока engineering frontier executable.
4. Сделать frontier roles однозначными без создания нового planner:
   - production capability frontier;
   - Polygon obligation frontier;
   - Mission admission frontier;
   - active execution;
   - external reentry state.
5. Не трактовать `CURRENT_EXECUTION_FRONTIER=NONE` как отсутствие работы, если Mission admitted и wake pending.
6. Проецировать consumed engineering criterion из durable registry в capability summary rows CAP-U02/U03/U04/U05/U06/U10/U11, сохраняя whole capability `PARTIAL` и exact L7/L8 remainder.
7. Добавить в locked `V7_CERTIFIED_AUTONOMOUS_BEHAVIOUR_GAP_REGISTER.md` только additive lifecycle annotation:
   - historical terminal snapshot;
   - real non-test consumer gap later closed;
   - current live state owned by CPS/OMP;
   - historical identity и evidence не переписываются.
8. Разделить verdict semantics:
   - engineering program status: `PERMANENT_POLYGON_AUTONOMOUS_ENGINEERING_PROGRAM_PRODUCTION_DEPLOYED_AND_CALLER_CERTIFIED`;
   - environment equality: `FULLY_ALIGNED`;
   - explicitly not claimed: production routing autonomy, Authority promotion, Production Maturity increase.
9. Добавить fail-closed validators и regressions, которые отклоняют stale Phase 6 frontier, false global `REAL_WORLD_LIMIT`, ambiguous frontier roles, stale capability summaries и historical Gap Register без lifecycle annotation.

Completion contract: `INTEGRATION_COMPLETION`.

Terminal: `PERMANENT_POLYGON_CPS_SEMANTICS_AND_PROJECTIONS_ATOMICALLY_RECONCILED`.

Next output: тот же still-valid CAP-U07 obligation с новым deterministic wake; CAP-U07 не исполняется в Mission 0.

## Mission 1 — CAP-U07 Shadow Learning Representation

Mission ID: `V7_POLYGON_CAP_U07_SHADOW_LEARNING_REPRESENTATION_MATRIX_V1`

Objective: закрыть только engineering часть Learning через существующих feedback/Learning/OMP owners.

Required chain:

```text
baseline knowledge generation
-> isolated shadow fork
-> owner-backed synthetic engineering outcome
-> real existing Learning owner update in shadow state
-> held-out replay
-> baseline/recommendation comparison
-> improvement/no-change/regression/overfit classification
-> consumer consumption
-> reset and cleanup
-> next obligation
```

Must prove:

- fork, provenance, no-overlap, reset и cleanup;
- production confidence/trust/suitability/recommendations unchanged;
- at least one changed or owner-justified-unchanged future recommendation consumed by a held-out experiment;
- deterministic replay and duplicate suppression;
- CAP-U07 engineering criterion becomes consumed;
- whole CAP-U07 remains `PARTIAL`;
- representative real Learning remains exact L8 remainder;
- successor is admitted, not pre-started, and gets a distinct pending wake.

Completion contract: `AUTOMATION_COMPLETION`.

Terminal: `CAP_U07_SHADOW_LEARNING_ENGINEERING_CRITERION_CONSUMED_SUCCESSOR_ADMITTED`.

## Mission 2 — Missing Owner Executor Adapter Closure

Program stage ID: `V7_PERMANENT_POLYGON_MISSING_OWNER_EXECUTOR_ADAPTER_CLOSURE_V1`.

Это dynamic compressed stage, а не обязательные пять отдельных prompts. Перед каждым adapter выполняется discovery. Stages объединяются только при общем owner и явной независимой verification.

Required exact adapters:

| Criterion | Existing owners to discover/reuse | Minimum proof |
|---|---|---|
| CAP-U12 Runtime Maturation Measurement | `intelligence_platform`, `intelligence_workers`, RT2/OMP owners | read-only maturation measurements consumed; no maturity promotion |
| CAP-U13 Runtime Time Intelligence | `time`, `intelligence_platform`, RT2-S1/S6 | deterministic time/age/window/latency interpretation and consumer |
| CAP-U14 Engineering Observation | `operator_observability`, `runtime_read_views` | owner-backed observation completeness/staleness/absence matrix |
| CAP-U16 Engineering Time Validation | `time`, `operator_observability` | timing evidence validation, missing/stale/conflict terminals |
| CAP-U20 Adaptation Quality | `operator_execution_feedback`, `intelligence_platform`, RT2-S6/OMP | outcome-to-recommendation evolution in isolated engineering state |

Rules:

- никакого generic adapter, который только читает файл или возвращает `PASS`;
- каждый executor вызывает реального owner и передаёт результат реальному OMP consumer;
- отсутствие adapter сначала формирует существующий deterministic BDP Candidate;
- accepted repair Mission реализуется и проверяется автоматически в existing Engineering Authority, если не требуется новая Authority/architecture/infrastructure;
- repair terminal обязан вернуться к исходной obligation и выполнить same-fidelity replay;
- если adapter уже доказан, stage сокращается или получает `MISSION_NOT_REQUIRED_ALREADY_CONSUMED`.

Per-adapter terminal: `<CAP>_OWNER_EXECUTOR_ADAPTER_IMPLEMENTED_CONSUMED_AND_RETURNED`.

Stage terminal: `ALL_CURRENT_OWNER_BACKED_EXECUTOR_ADAPTER_GAPS_CLOSED`.

## Mission 3 — Current Seed L1-L6 Closure And Capability Projection

Mission ID: `V7_PERMANENT_POLYGON_CURRENT_SEED_L1_L6_CRITERION_CLOSURE_V1`.

Objective: потребить все remaining safe current-seed engineering criteria U02-U22 без заявления whole-capability completion.

Execution is dynamic:

1. прочитать durable registry и dependencies;
2. выбрать smallest executable owner-backed criterion;
3. выполнить minimum sufficient fidelity;
4. consume result;
5. atomically update registry, capability summary projection, Phase 6 lanes и next Mission;
6. continue event-driven;
7. skip already consumed/still-valid criteria;
8. preserve exact controlled/natural remainder.

Completion requires:

- no current-seed executable L1-L6 criterion remains uncovered;
- every consumed criterion has owner, experiment, fidelity, source/result fingerprints, consumer, behavior change, terminal and invalidation triggers;
- capability rows, dependency graph, dashboard projections and registry agree;
- `REAL_WORLD_LIMIT` exists only on exact L7/L8 lane-local criteria;
- unsupported adapters are zero or have an exact proven external boundary after all independent work is exhausted.

Terminal: `CURRENT_SEED_ALL_AVAILABLE_L1_L6_CRITERIA_CONSUMED_L7_L8_REMAINDERS_EXPLICIT`.

## Mission 4 — Proactive Situation Synthesis And Coverage Expansion

Mission ID: `V7_PERMANENT_POLYGON_PROACTIVE_SITUATION_SYNTHESIS_AND_COVERAGE_V1`.

Objective: превратить Polygon из текущего owner-backed scenario consumer в систематический проектировщик будущих инженерных ситуаций.

Situation generator must compose owner-declared equivalence classes and boundaries for:

- topology and route graph changes;
- workload, burst, skew and logical scale;
- channel/service degradation and correlated failures;
- latency, loss, jitter, reordering and asymmetric reachability;
- DNS/TCP/UDP/HTTP/service failures where substrate permits;
- stale, missing, conflicting and out-of-order telemetry;
- partial apply, verification timeout, rollback, containment and recovery slow-start;
- capacity/resource pressure and cleanup;
- policy/Authority boundaries without granting Authority;
- correct stay/no-action and delayed action;
- safety-first counterfactual branches;
- shadow Learning improvement/no-change/regression/overfit cases.

Generation rules:

- derive cases from owner contracts, invariants, dependency changes and uncovered boundary classes;
- prefer equivalence/boundary/pairwise coverage over meaningless Cartesian explosion;
- preserve deterministic seed and minimal reproduction identity;
- synthetic count growth alone is forbidden;
- every situation must name the real owner entrypoint, expected legal terminals, consumer and evidence class;
- newly discovered reproducible V7 mismatch routes to BDP repair and automatic return;
- Polygon/harness/oracle defects remain separated from V7 product defects.

Completion requires at least one newly generated, not pre-authored situation in each applicable family, real V7 owner consumption, deterministic replay, boundary coverage update and zero production effects.

Terminal: `PROACTIVE_OWNER_BACKED_SITUATION_SYNTHESIS_CONSUMED`.

## Mission 5 — Multi-Generation Source, Invalidation And Repair Campaign

Mission ID: `V7_PERMANENT_POLYGON_MULTI_GENERATION_SOURCE_INVALIDATION_REPAIR_CAMPAIGN_V1`.

Objective: доказать, что Polygon не заканчивается после seed U02-U22 и действительно реагирует на дальнейшее развитие системы.

Minimum campaign:

- at least 3 successive obligation generations;
- at least 6 distinct permanent source categories;
- at least 3 capability/owner families;
- one code/dependency fingerprint change;
- one policy/owner-contract change;
- one topology/workload/service/scale change;
- one regression/drift input;
- one new OMP Mission or BDP Intent Gap;
- one duplicate result suppression without re-execution;
- one selective invalidation proving unrelated criteria remain consumed;
- one mismatch -> BDP -> repair Mission -> automatic return -> replay PASS;
- one substrate-degradation case where lower fidelity continues;
- exact new next generation after every terminal.

Controlled/natural production outcomes may enter only as owner-backed source events. Synthetic outcomes cannot be labeled L7/L8.

Terminal: `PERMANENT_POLYGON_MULTI_GENERATION_EVOLUTION_AND_REPAIR_LOOP_CONSUMED`.

## Mission 6 — Cross-Process Autonomous Reentry And Stability Soak

Mission ID: `V7_PERMANENT_POLYGON_CROSS_PROCESS_REENTRY_AND_STABILITY_SOAK_V1`.

Objective: доказать независимость не внутри одного вызова, а через реальные отдельные turns/process boundaries.

Required evidence:

- at least 10 successful separate event-driven reentry turns across different obligations/generations;
- bounded isolated soak of at least 100 iterations;
- no active-execution overlap;
- compare-and-swap rejects stale generation without write;
- each consumed wake creates a distinct successor wake with monotonic chronology;
- watchdog only recovers a proven lost/failed dispatch and is no-op for a live dispatched event;
- duplicate wake/result/mission identities are suppressed;
- CPS/report/resource growth remains bounded;
- cleanup leaves no orphan topology, shadow Learning state, lease or temporary state;
- process restart/reload preserves durable frontier and resumes legally;
- no user prompt between safe Missions;
- any exact new Authority/infrastructure boundary is returned once with complete blocker evidence.

Terminal: `PERMANENT_POLYGON_CROSS_PROCESS_FULL_INDEPENDENCE_AND_STABILITY_CERTIFIED`.

## Mission 7 — Target-Level Final Certification And Permanent Operating Mode

Mission ID: `V7_PERMANENT_POLYGON_TARGET_LEVEL_FINAL_CERTIFICATION_V1`.

Must reuse valid evidence and must not ceremonially rerun closed work.

Final certification checks:

1. CPS has zero stale/ambiguous Phase 6, frontier, capability or historical-lifecycle projections.
2. CAP-U07 engineering criterion is consumed; its L8 remainder is explicit.
3. CAP-U12/U13/U14/U16/U20 have real owner executor adapters and real consumers.
4. All current safe L1-L6 criteria are consumed or have exact honest substrate boundaries.
5. Proactive situation synthesis creates owner-backed cases before real incidents.
6. Multi-generation source/invalidation/repair campaign passed.
7. Cross-process reentry and stability soak passed.
8. Producer -> consumer -> behavior change -> next output is closed for every certified link.
9. L7/L8 remain separate and cannot become a global engineering stop.
10. Runtime/routing/user/packet/restore/rollback/Authority/Production Maturity forbidden effects remain absent.
11. Full relevant tests, truth and convergence pass.
12. If deploy applies, safe-deploy manifest contains only intended files and local/GitHub/production commit plus runtime hashes are equal.
13. Final report uses narrow semantics and separates engineering automation certification from production routing autonomy.

Target terminal:

`PERMANENT_POLYGON_PROACTIVE_MULTI_GENERATION_AUTONOMOUS_ENGINEERING_VALIDATION_TARGET_LEVEL_CERTIFIED`

Exact status semantics:

```text
ENGINEERING_PROGRAM = TARGET_LEVEL_CERTIFIED
PRODUCTION_DEPLOY_AND_CALLER = CERTIFIED
ENVIRONMENT_ALIGNMENT = FULLY_ALIGNED
PRODUCTION_ROUTING_AUTONOMY = NOT_CLAIMED
AUTHORITY_PROMOTION = NONE
PRODUCTION_MATURITY_CHANGE = NONE
L7_L8 = SEPARATE_OWNER_BACKED_REMAINDERS
```

## 5. Stop Conditions

Legal whole-program stops:

- `POLYGON_SUBSTRATE_AUTHORITY_REQUIRED`, only after every independent lower-fidelity criterion is exhausted;
- `POLYGON_EXTERNAL_INFRASTRUCTURE_REQUIRED`, with exact unavailable substrate and remaining criterion;
- `FUNDAMENTAL_ARCHITECTURE_GAP`, only after reuse/composition/extension failure proof;
- exact operational/engineering Authority boundary outside existing policy.

Illegal stops while independent work remains:

- generic `REAL_WORLD_LIMIT`;
- bounded invocation budget;
- missing optional fidelity substrate;
- missing executor adapter already owned by an existing component;
- Mission terminal;
- tests/report/deploy completion without consumer behavior change and next output;
- waiting for a user prompt when an existing safe reentry path exists.

## 6. Approval Consequence

Approval of this plan authorizes only sequential OMP execution under existing safety and deploy laws. It does not itself activate a Mission, authorize production mutation, grant Authority, enable timers/daemons, change Production Maturity or waive exact safe-deploy manifest review.

After approval, the exact first executable Mission is Mission 0:

`V7_PERMANENT_POLYGON_CPS_SEMANTIC_INTEGRITY_AND_PROJECTION_RECONCILIATION_V1`

Mission 1 CAP-U07 may start only after Mission 0 proves one atomic non-stale CPS projection and materializes the still-valid CAP-U07 wake.
