# V7 Autonomous Recovery Engineering Agent Program

Status: `DESIGN_IN_PROGRESS`

## 1. Immutable objective

Build one persistent V7 engineering agent which, from a compact command and without the user relaying messages between GPT and Codex:

1. measures and reduces the interval from the physical failure of a channel to the verified transfer of every required affected client to a working channel;
2. keeps that complete interval within 7 seconds under an explicitly admitted load and evidence class;
3. removes artificial software limits on client count through capacity-bounded cohort execution rather than a fixed one-client path;
4. continuously improves lawful project automation;
5. runs controlled fault campaigns only in an isolated Polygon, repairs discovered defects through existing V7 owners, and automatically returns to the interrupted experiment;
6. uses GPT as semantic analyst/reviewer and Codex as a critical executor which may adapt instructions when repository evidence requires it.

The terminal is a working, behaviorally accepted agent. Documents, schemas, tests, reports, commits, deployments, or a finite scenario count alone are not completion.

## 2. Architecture decision

`EXTEND_EXISTING_EXECUTION_CONTRACT`. This Program is a supporting design and execution program under the existing CPS/OMP lifecycle. It is not a new product-control owner and does not create a parallel Agent System, coordinator, queue, registry, scheduler, Matrix, Authority, Planner, deploy owner, or truth source.

Reuse:

- `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM` for the N0-N11 recovery chain and active product frontier;
- existing Matrix health truth, scope derivation, Authority, Planner, Candidate/Packet/Lease/Barrier, governed Apply, `v7-user-switch`, required-service S11, rollback, and `v7-safe-deploy` owners;
- `V7_ROUTING_DIGITAL_TWIN_POLYGON_MASTER_PROGRAM` and Permanent Polygon OMP integration for deterministic scenarios, fault injection, replay, repair, and automatic return;
- existing warm cohort/class data plane and scale harness already exercised at 10,000 virtual users;
- bounded execution-profile identity, Analyst/Reviewer separation, critical Codex adaptation, re-entry, completion evidence gate, and no-microstep terminal rules.

No new runtime component is admitted unless a fresh responsibility audit proves that no existing owner can lawfully supply the required behavior.

## 3. User decisions

### Answer 1 — seven-second clock

The required interval begins when the channel physically fails, not when V7 finishes detecting or confirming the failure. It ends when the client has actually moved to another working channel. Pending clarification in Question 4, the safe default is the last required affected client's verified required-service S11.

Clock model:

- Polygon: `T_PHYSICAL_FAILURE` is the authoritative fault-injection timestamp.
- Production: V7 must not pretend to know the physical onset retrospectively. Exact onset requires an independent owner-backed external timestamp. Until that exists, report both `T_LAST_KNOWN_GOOD -> T_FIRST_VALID_FAILURE_OBSERVATION` as bounded blind time and the existing observation-to-last-S11 interval, without claiming an exact physical-onset SLO.

### Answer 2 — autonomous Polygon faults

Yes. The agent may autonomously break test channels, services, routes, dependencies, and other isolated Polygon components, generate combinations, restore them, replay them, and compare counterfactuals. Intentional Production failure remains prohibited.

### Answer 3 — autonomy

The agent may do everything necessary to reach the objective within existing V7 Authority and safety boundaries: discover, analyse, ask GPT, critically adapt the plan, edit code and contracts, test, run Polygon campaigns, review, commit, push, use the existing safe-deploy owner when admitted, verify behavior, roll back, repair, and continue automatically.

This permission does not authorize bypassing Authority, exposing secrets, spending money, creating external infrastructure, manufacturing Natural evidence, intentionally breaking Production, or moving real users outside existing admissibility and safety contracts.

### Answer 4 — recovery terminal

Recovery completes only when the last required affected client has switched and the necessary services have passed owner-backed verification. First-client success, route mutation, process exit, or partial-cohort success is not the terminal.

### Answer 5 — qualifying failure classes

The switching contract covers complete channel loss, route or tunnel loss, unavailability of a required service, critical quality degradation, and partial channel failure. Exact measurable thresholds and required corroboration belong to Matrix-owned health policy and must be frozen per service/profile.

### Answer 6 — confidence-sensitive action

Different signal classes require different lawful responses. Definitive owner-backed evidence may enter the fast path; ambiguous, weak, or potentially transient evidence requires bounded confirmation and must not trigger an unsafe move. Existing capability must be verified and extended only where coverage or consumption is incomplete.

### Answer 7 — load-independent software contract

There must be no fixed client-count limit in the software contract. The seven-second objective is accepted only inside a measured hardware/capacity envelope. Above it, the system uses automatically sized safe cohorts, admission and backpressure rather than silent overload or scope truncation.

### Answer 8 — first scale acceptance

Acceptance proceeds in two mandatory steps: first 1,000 affected clients, then 10,000. Passing 1,000 is an intermediate checkpoint, not completion.

### Answer 9 — adaptive cohorts

For a large failure, the system switches the largest currently safe amount in parallel and automatically reduces or increases cohort size from current capacity evidence. It must preserve complete affected scope and last-member verification.

### Answer 10 — fairness

All clients are equal. No commercial or manually assigned priority is introduced. Deterministic ordering and starvation freedom are still required where capacity forces multiple cohorts.

### Answer 11 — concurrent failures

Multiple failed channels are handled concurrently under one capacity view of surviving targets and shared resources. The system must prevent recovery activity from overloading the remaining working channels.

### Answer 12 — Polygon fault authority

All listed fault classes are authorized in a proven isolated Polygon: channel/tunnel/route/service loss; latency and packet loss; partial degradation; correlated multi-channel failure; process restart; stale state; wrong target; insufficient capacity; mid-switch failure; rollback; and repeated switching. The generator may compose them subject to isolation, cleanup and resource budgets.

### Answer 13 — Polygon fidelity

Use the existing Polygon and improve it only after capability discovery. It must provide progressive fidelity: fast deterministic virtual modelling; real V7 code paths in isolation; then a dedicated controlled environment as close to Production as lawfully possible. Missing resources or functions required by acceptance are extended under existing owners.

### Answer 14 — autonomous scenario generation

The agent generates new event combinations itself, in addition to regression and approved seed catalogs. Generation must be bounded, reproducible, coverage-directed and retain exact scenario/fault/time identities.

### Answer 15 — safe seeded defects

The agent may introduce deliberate safe test defects only in disposable or isolated Polygon surfaces. A seeded defect must never enter Production or be confused with a real product defect. Acceptance requires detection, causal diagnosis, repair, independent review, cleanup of the seed and automatic replay of the originating experiment.

### Answer 16 — invocation model

The agent runs after every qualifying material system change, operates continuous resource-bounded background Polygon campaigns, and exposes one compact command for a full campaign. The same command must be able to design/execute the complete admitted campaign initially and later perform incremental continuation when the system changes.

### Answer 17 — ideal automation

Inside authorized workflows, no manual relay or manual next-step execution remains. Every safe successor runs automatically. Human input is reserved for new Product Contract decisions, new costs, secrets, external infrastructure, or action outside existing Authority.

### Answer 18 — notification and non-blocking questions

Notify the user on full completion. If a genuine product decision is required, ask it once with evidence and bounded options, hold only the dependent branch, and continue every independent safe branch. A product question is not permission to terminate or pause the whole Mission.

## 4. Agent operating loop

`compact command -> fresh CPS/owner discovery -> frozen mission and acceptance contract -> Polygon campaign -> evidence gap or defect -> GPT semantic analysis -> Codex critical repository assessment -> bounded decision/re-entry -> existing-owner implementation -> independent review -> focused verification -> replay interrupted experiment -> broader selective regression -> evidence-backed next obligation or lawful terminal`

The user is not a transport layer. GPT/Codex packets, questions, reviews, corrections, checkpoints, and continuation are exchanged automatically. User input is requested only at a genuine Product Contract, Authority, safety, secret, cost, or external-resource boundary.

Native role transport is separately fail-closed. Before a full campaign after a
native-adapter change, one compact `AUTONOMOUS_RECOVERY NATIVE_SMOKE` must
start a fresh read-only Analyst, return strict JSON tied to an immutable packet,
and retain an attempt envelope with command-policy identity, exit/timeout,
thread-start/final-message observation and redacted bounded output evidence.
Its Codex runtime state is transport-only and non-canonical; it never becomes a
V7 owner, registry or truth source. A smoke failure is an exact `STOP_SAFE` and
does not enter Docker, Polygon, CPS, Runtime, Production or Authority.

## 5. Required reasoning roles

- GPT Analyst: causal and semantic analysis, hypotheses, alternatives, product/safety meaning, and decision recommendation.
- Codex Executor: verifies actual repository/runtime facts, challenges or narrowly adapts the recommendation, implements only the admitted change, and reports evidence honestly.
- Independent Reviewer: attempts to falsify the proposed decision and completion claim.
  Its immutable engineering-Polygon packet must contain the current producer,
  caller, consumer and existing-owner execution path, and it must echo that
  evidence fingerprint with `ISOLATED_POLYGON_ENGINEERING_ONLY`. A documented
  mechanism without a current execution consumer is insufficient. This scope
  requires rejection of missing/tampered owner evidence, but does not permit
  demanding or inferring Runtime, Production, user-effect or final Section 8
  evidence from an isolated engineering packet.
- Deterministic V7 owners: retain all product truth, admissibility, mutation, verification, rollback, deployment, and terminal authority.

## 6. Scale meaning

“Unlimited clients” means no fixed software ceiling and no single-client assumption. It does not mean literal infinity or unsafe simultaneous mutation. Work is expressed as complete affected scope, prepared asynchronously where possible, and applied through capacity-aware cohorts/classes with admission, backpressure, rollback, fairness, and last-member verification. Acceptance must state the tested load and capacity envelope.

## 7. Safety invariants

- Controlled destructive experiments occur only in a proven isolated Polygon.
- Production faults are observed, never fabricated.
- No weakening of required-service S11 or narrowing of affected scope to meet seven seconds.
- Stale generation, wrong target, uncertain scope, Authority denial, insufficient capacity, unverified isolation, or missing rollback causes `STOP_SAFE`.
- Every repair retains origin experiment identity and automatically returns to replay it.
- Agent activity cannot silently replace the active CPS product frontier.

## 8. Completion definition

The Program completes only when one compact command in a fresh task demonstrably:

1. loads the persistent agent contract without a large prompt;
2. observes CPS and selects the exact lawful obligation;
3. runs multi-fault isolated Polygon campaigns across admitted topology, service, timing, concurrency, stale/current, restart, rollback, and partial-failure classes;
4. uses real independent GPT-style Analyst and Reviewer contexts plus critical Codex adaptation;
5. finds and repairs a seeded or naturally exposed non-trivial defect through existing owners;
6. automatically returns to and passes the originating experiment;
7. proves the complete physical-onset-to-last-required-client S11 clock within the accepted seven-second load envelope in Polygon;
8. proves no fixed one-client ceiling and records the tested scale/capacity law;
9. leaves zero unexplained manual relay in the admitted workflow;
10. produces owner-consumed evidence, updates CPS/OMP atomically, and names the next automatic obligation or a lawful terminal.

## 9. Design-question register

There are 18 design questions in total. All 18 have been answered. Their reconciliation against current CPS, existing owners and executable capabilities is the final design-freeze gate.

## 10. Fresh existing-capability reconciliation

### Signal confidence — `REUSE`, narrowly `EXTEND`

The user's expectation is confirmed. The current N0-N11 implementation already distinguishes signal classes:

- definitive fresh local hard evidence with exact source and generation may take the Matrix-governed fast path;
- ambiguous or remote timeout, loss, generic path, service-quality, DNS, Telegram or partial evidence remains `SUSPECT` until bounded targeted confirmation;
- stale, wrong-generation, conflicting or uncertain evidence cannot move users and must degrade or `STOP_SAFE`.

Current direct admission is deliberately narrow: interface down/missing is proven; other classes remain confirmation-bound. The agent must reuse this split. It may propose promotion of another signal class only after a Matrix/Authority-owned tournament proves freshness, false-positive safety, restart/replay behavior and independent corroboration requirements.

### Polygon — `REUSE_EXISTING_POLYGON`, targeted extensions only

Already reusable:

- L1-L6 progressive fidelity from deterministic model through real isolated V7 paths, namespaces/network impairment, containers/services, sanitized snapshots and hybrid logical scale;
- durable obligations, generations, bounded continuation and no-overlap behavior;
- mismatch -> existing BDP Candidate -> OMP repair -> automatic same-obligation replay;
- 1,000-user scheduling evidence and 10,000-user logical-scale harness;
- 10,000-member warm cohort/class mapping and constant-time atomic class-switch primitive;
- an existing adaptive-cohort contract bounded by incident scope, capacity, Authority, Runtime, verification, rollback and breaker constraints.

Required extensions:

1. bounded coverage-directed combination generation: pairwise, boundary, state-transition, risk-weighted, seeded and regression replay;
2. explicit 1,000 then 10,000 acceptance under the new physical-onset-to-last-S11 objective and recorded resource envelope;
3. simultaneous independent and correlated multi-source campaigns covering target competition, shared capacity, fairness, starvation, overlapping cohorts, rollback collision and last-member S11;
4. one non-trivial isolated seeded V7 defect with genuine diagnosis, repair, independent review, seed removal and automatic replay;
5. progressive certification beyond the current live action-class cohort envelope rather than treating logical 10,000-user modelling as Production Authority.

### Current constraints that the agent must solve rather than hide

- Existing binding Production SLO begins at first valid observation, while the new objective begins at physical failure. Polygon injection supplies exact onset; Production requires independent onset telemetry before the exact claim is lawful.
- Current code demonstrates logical 10,000-user scale, but current Runtime/Authority cohort admission is narrower and action-class dependent. The goal is `SCALE_WITHOUT_ARCHITECTURAL_FIXED_CEILING`, achieved by progressively certified capacity-aware cohorts until the complete scope reaches S11.
- Current simultaneous-source handling preserves separate incident identities but product mutation is still a bounded transaction path, not generally admitted parallel Production mutation.
- “Actual switch” means assignment truth, kernel/route truth and required-service S11. A claim about what the client device itself experienced additionally requires independent client-side telemetry.

### Frozen responsibility boundary

GPT and Codex may analyse, challenge, implement, test and review, but never become Matrix, Planner, Authority, route writer, deploy owner or S11 truth owner. Prefer parallel preparation and verification with safe atomic class/cohort commits; actual mutation concurrency remains capacity- and Authority-governed.

## 11. Implementation phases (frozen after Q&A)

1. Freeze product clocks, terminal, evidence classes, autonomy, and safety boundaries from the full Q&A.
2. Bind the agent profile/skill into existing OMP and Polygon repair-return lifecycle; add no new owner without gap proof.
3. Close physical-onset observability and full affected-scope/last-member measurement.
4. Generalize switching from single-client assumptions to capacity-bounded cohort execution.
5. Add systematic coverage generation, hidden scenarios, fault combinations, and automation-maturity backlog consumption.
6. Prove autonomous GPT/Codex decision, implementation, independent review, repair, replay, deploy/rollback, and continuation without user relay.
7. Run fresh-context behavioral acceptance, controlled scale/SLO acceptance, then separately prepare lawful Production evidence.

## 12. Current exact next action

Freeze the executable Mission plan from this reconciled Program, then implement it continuously through existing OMP/Polygon owners. The first implementation block must bind the persistent compact-command agent profile and prove automatic GPT/Codex question-review-repair-replay continuation without user relay. Later blocks must not be declared terminal before the complete Definition of Done in Section 8 is behaviorally accepted.
