# V7 Master Project Handoff

Status: `CANONICAL ENTRY POINT`

Owner: OMP / Canonical Reference / Current Program State

Handoff version: `V7_MASTER_PROJECT_HANDOFF_BACKGROUND_AUTOMATION_CERTIFIED_V1`

Last updated: 2026-07-16

Stage 1 architecture status: `STAGE_1_ACCEPTED`, `STAGE_1_LOCKED`

Stage 2 knowledge status: `LOCKED_KNOWLEDGE`

This document is the single entry point for any new ChatGPT conversation or engineer working on V7.

Assume all previous conversations are lost. Read this document first. It explains what V7 is, what is already proven, what is locked, what remains active, and which documents are canonical evidence.

Do not create another handoff. Do not create a parallel roadmap. Do not re-run Stage 1 by default.

## 0. Canonical Strategy Update

Status: `ACTIVE_CANONICAL_STRATEGY`

This section synchronizes the handoff with the current post-Stage-2 strategy. It does not rewrite Stage 1 history, Stage 2 history, OMP, AOS, `LOCKED_ARCHITECTURE`, or `LOCKED_KNOWLEDGE`.

Older sections that describe Stage 2 as the next active architecture-program step are preserved as historical handoff context from the Stage 1 to Stage 2 transition. The current strategic interpretation is:

```text
LOCKED_ARCHITECTURE
  -> LOCKED_KNOWLEDGE
  -> OMP execution
  -> Current Program State
  -> Engineering Context Resolver
  -> Research / Discovery only when required
  -> Existing-owner implementation when admitted
```

### Canonical Project Strategy

The main project goal is no longer best described as creating new capabilities.

The current canonical goal is:

```text
V7 must gradually automate the application and execution of the knowledge,
laws, policies, runtime rules, routing rules, channel rules, OMP rules,
decision logic, verification rules, rollback rules, learning rules, and
canonical synchronization rules it already has.
```

The strategic measure of progress is the reduction of places where existing system laws still require human or Codex participation to understand, decide, execute, verify, learn, or synchronize.

### Strategic Program Roles

Autonomous Evolution Program is the strategic program.

It:

- understands the system;
- builds current reality;
- certifies Autonomous Behaviour Gaps;
- hands certified work to OMP.

OMP remains the only execution operating system.

Autonomous Evolution Program must not become a second OMP, second Runtime, second Planner, second Authority, second roadmap, or second truth source.

The current active execution program is OMP. CPS is the only live volatile state owner. Canonical Reference is the durable truth owner. SYSTEM_MAP owns owner topology. Engineering Reports are historical evidence only.

### Primary Analysis Unit

The main analysis unit is:

```text
Autonomous Behaviour
```

Autonomous Behaviour means:

```text
Situation
  -> Interpretation
  -> Applicable Knowledge
  -> Applicable Laws
  -> Reasoning
  -> Decision
  -> Execution
  -> Verification
  -> Learning
  -> Improvement
```

Law Execution is only one part of Autonomous Behaviour. V7 must first understand the situation, select applicable knowledge and laws, reason about constraints, decide what is allowed, and only then execute.

### Phase 2 Strategic Meaning

Phase 2 must build:

```text
Current Autonomous Reality Model
```

not merely an inventory.

It must discover:

- situations V7 currently observes or handles;
- interpretation paths;
- applicable knowledge and law selection;
- reasoning paths;
- decision paths;
- execution paths;
- automation state;
- manual dependency;
- structural friction.

Phase 2 must not create gaps or OMP missions.

### Phase 3 Strategic Meaning

Phase 3 must certify:

```text
Autonomous Behaviour Gap
```

Autonomous Behaviour Gap means a proven place where V7 cannot yet independently understand a situation, select applicable existing knowledge and laws, reason about constraints, decide an allowed action or no-action, execute through existing owners, verify the result, learn from the outcome, or synchronize durable consequences.

Law Execution Gap is a subtype of Autonomous Behaviour Gap.

### Strategic Change Rule

The project may create, simplify, combine, automate, or remove unnecessary elements only when evidence proves that doing so improves autonomy while preserving architecture, owners, OMP, Runtime, Authority, verification, rollback, learning, production safety, and canonical truth boundaries.

The standing method remains:

```text
Discover
  -> Reuse
  -> Extend
  -> Implement
```

### Current Strategic Direction

This section is strategic reference context, not volatile task state. Before execution, resolve current scope and safe next action from `docs/programs/V7_CURRENT_PROGRAM_STATE.md` section `0. Authoritative Live Current State`.

The active program is `FUTURE_SCALE_SCENARIO_ENGINEERING`. FSSE makes the existing Engineering Polygon and OMP exercise real V7 code against bounded deterministic future-scale states instead of waiting for rare production situations that cannot occur at the current approximately 50-user / 5-channel scale.

The exact current frontier is:

```text
FSSE-01 foundation COMPLETE_CONSUMED
  -> FSSE-02 execution harness COMPLETE_CONSUMED
  -> FSSE-03 high-fidelity validation COMPLETE_CONSUMED
  -> FSSE-04 autonomous Polygon integration and certification COMPLETE_CONSUMED
  -> two natural external reentries COMPLETE_CONSUMED
  -> FULL_INDEPENDENT_BACKGROUND_AUTOMATION_PRODUCTION_CERTIFIED
```

FSSE-04 connects the standard `Continue OMP` trigger to the existing bounded OMP/Polygon consumer. The existing Codex Automation Platform heartbeat owns independent external reentry: two distinct natural 30-minute scheduled events arrived after prior target-thread turns exited, invoked the standard consumer, released their leases without overlap and produced zero Runtime/production/Authority effects. Commit `a8e6454f62699d0a2bea5eeccfb0b959cb6abf3e` is production-deployed, truth is `FULLY_ALIGNED`, convergence is `ALIGNED`, deploy delta is zero and snapshot equality is certified. CAP-U07 remains protected capability-local `WAITING_EXTERNAL_DEPENDENCY` WIP.

### Research First Rule

Before creating any new fundamental mechanism, owner, planner, runtime, engine, program, architecture, or truth source, V7 must:

1. perform world research;
2. read official documentation where available;
3. build a cross-system matrix;
4. compare external practice with V7 reality;
5. prove a real V7 gap;
6. only then change architecture through existing governance.

Fundamental mechanisms must not be built from intuition, naming preference, or local conceptual pressure.

### Immediate Next Task

The exact continuing action is:

```text
COMMAND = AUTHORIZE CANONICAL SAFE DEPLOY FOR CURRENT_CANONICAL_HEAD
STOP = ENGINEERING_AUTHORITY
REENTRY = EXISTING ACTIVE 30-MINUTE CODEX AUTOMATION PLATFORM HEARTBEAT REMAINS ENABLED BUT DOES NOT GRANT DEPLOY AUTHORITY
```

The next thread must close only the existing safe-deploy boundary:

```text
explicit safe-deploy Engineering Authority
  -> tools/v7-safe-deploy for the exact canonical commit
  -> truth --all
  -> convergence
  -> runtime snapshot equality
  -> production-closure terminal reconciliation
```

Do not repeat FSSE-01 through FSSE-04, create another heartbeat/Polygon/owner, bypass the standard `Continue OMP` command, or infer Runtime/production Authority from engineering automation certification.

## 1. What V7 Is

V7 is a governed production routing platform.

It is not "just a VPN". VPN protocols are transport mechanisms. The actual product is reliable, evidence-driven routing continuity for users.

V7 exists to keep users online when connectivity sources fail, degrade, recover, or become unsafe. It observes real production state, creates evidence, diagnoses the situation, selects legal routing actions, asks Authority for a bounded permission, applies only the approved action through Runtime, verifies the result, rolls back or closes safely, learns from the outcome, and gradually earns more autonomy.

The product value is invisible reliability. The user should not care whether the current path is OpenVPN, WireGuard, VLESS, or another channel. V7's job is to preserve service continuity while preventing unsafe automatic movement.

V7 is also an engineering platform. Its architecture deliberately improves the way the system is built: every manual action, repeated workflow, blocker, recovery, test, certification, and report becomes evidence for future automation and workflow simplification.

## 2. Current Project State

Stage 1 of the V7 Autonomous Engineering roadmap is complete.

The complete Stage 1 architecture baseline has been accepted and locked:

- Stage 1.1 Domain Certification processed all 26 architecture domains.
- Stage 1.2 Recovery closed the only remaining NOT CERTIFIED domain, Domain 11 Diagnosis.
- Stage 1.3 Corpus Audit proved the 26 domains form one complete and internally consistent architecture.
- Final Stage 1 Architecture Acceptance passed.
- Stage 1 is now the official canonical architectural foundation of V7.

Stage 2 Knowledge Engineering is also complete and locked:

```text
Stage 2.1 Knowledge Inventory
  -> Stage 2.2 Knowledge Extraction
  -> Stage 2.3 Knowledge Deduplication
  -> Stage 2.4 Knowledge Graph
  -> Stage 2.5 V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md
  -> Stage 2.6 Knowledge Acceptance
  -> Stage 2.7 Knowledge Lock
  -> LOCKED_KNOWLEDGE
```

The locked knowledge baseline is:

```text
docs/reference/V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md
```

The current active execution program is:

```text
docs/programs/OPERATIONAL_MATURITY_PROGRAM.md
```

The only authoritative volatile current-state owner is:

```text
docs/programs/V7_CURRENT_PROGRAM_STATE.md
```

Architecture is complete by default. New architecture is allowed only after a proven `FUNDAMENTAL_ARCHITECTURE_GAP`.

Do not treat old Stage 1 recovery tasks as active work. They are historical evidence.

### Current FSSE Handoff Snapshot

This is a handoff projection only. CPS Section 0 remains authoritative if volatile state changes after this update.

```text
LATEST_TERMINAL_MISSION = V7_OMP_FULL_INDEPENDENT_BACKGROUND_AUTOMATION_AND_FSSE04_PRODUCTION_CLOSURE_V1
LATEST_TERMINAL_RUN_NONCE = V7_OMP_EXTERNAL_REENTRY_PAIR_6E013631_92871890
LATEST_TERMINAL_VERDICT = FULL_INDEPENDENT_BACKGROUND_AUTOMATION_PRODUCTION_CERTIFIED
LATEST_TERMINAL_REPORT = docs/reports/engineering/2026-07-16_001627_full_independent_background_automation_and_fsse04_production_closure.md
TRUTH_CONVERGENCE = FULLY_ALIGNED

ACTIVE_PROGRAM = FUTURE_SCALE_SCENARIO_ENGINEERING
CURRENT_PROGRAM_STAGE = FSSE_04_COMPLETE_BACKGROUND_AUTOMATION_PRODUCTION_CERTIFIED
CURRENT_ACTIVE_SCOPE = FULL_INDEPENDENT_BACKGROUND_AUTOMATION_PRODUCTION_CERTIFIED
CURRENT_PROGRAM_EXECUTION_FRONTIER = NONE
CURRENT_NEXT_ACTION_ID = WAIT_FOR_REPRESENTATIVE_REAL_LEARNING_OUTCOMES
NEXT_MISSION_ID = NONE
NEXT_SCENARIO_ID = NONE
CURRENT_STOP_CONDITION = REAL_WORLD_LIMIT
OMP_CONTINUATION_REQUIRED = FALSE
EXTERNAL_INPUT_REQUIRED = TRUE
AUTHORITY_REQUIRED_NOW = NO_INSIDE_APPROVED_POLICY
FSSE_STATUS = FSSE_04_AUTONOMOUS_ENGINEERING_LOOP_CERTIFIED
FSSE_00_EXTERNAL_REENTRY_STATUS = FULL_INDEPENDENT_BACKGROUND_AUTOMATION_PRODUCTION_CERTIFIED
FSSE_00_BLOCKS_FSSE_01 = FALSE
OMP_AUTOMATION_LEVEL = FULL_INDEPENDENT_BACKGROUND_AUTOMATION_PRODUCTION_CERTIFIED
MANUAL_CONTINUE_OMP_FALLBACK = ACTIVE
CURRENT_STATE_GENERATION = cpsgen_V7_BACKGROUND_AUTOMATION_PRODUCTION_CERTIFIED_928718904BCD
CURRENT_TRANSITION_ID = EXTERNAL_REENTRY_PRODUCTION_CERTIFIED_V1
SCENARIO_COVERAGE_GENERATION = fssef_dcd80bd4189d95ec7c58d661
SCENARIO_COVERAGE_FINGERPRINT = dcd80bd4189d95ec7c58d661af3ac313c1f7760f925c9937f9f15dfe40f873df
SCENARIO_CORPUS_COUNT = 40
SCENARIO_ELIGIBLE_COUNT = 0
SCENARIO_COVERED_COUNT = 40
SCENARIO_STALE_COUNT = 0
SCENARIO_BLOCKED_COUNT = 0
SCENARIO_MISMATCH_COUNT = 0
SCENARIO_BUDGET = 40
SCENARIO_STOP_REASON = FSSE_04_CERTIFIED_CONTINUE_OMP
```

FSSE-04 evidence is `docs/reports/engineering/2026-07-15_214500_future_scale_autonomous_polygon_integration_and_certification.md`. Independent reentry closure evidence is `docs/reports/engineering/2026-07-16_001627_full_independent_background_automation_and_fsse04_production_closure.md` plus the append-only owner evidence registry.

## 3. Current Maturity Snapshot

| Area | Current maturity |
|---|---|
| Production maturity | Production execution and governed certification capabilities exist, but routine full production autonomy remains governed by OMP and Authority. Stage 1 architecture lock does not automatically grant new production authority. |
| Autonomy maturity | Architecture for autonomous routing is complete and locked. Autonomy still expands only through evidence, certification, Authority, Runtime, Verification, Rollback / Closure, Learning, and OMP. |
| Architecture maturity | Complete, accepted, and locked. Future architecture change is exceptional and must pass formal evolution procedures. |
| Certification maturity | Stage 1 architecture certification corpus is complete: 26 certified domains, corpus audit PASS, final acceptance PASS. |
| Implementation maturity | Core governed owners exist. Domain 11 Diagnosis recovery implementation is complete. Implementation work after Stage 1 must follow OMP and existing-owner discipline. |
| Engineering maturity | Engineering work is governed by evidence, owner resolution, completion-first execution, automation audit, workflow audit, and canonical knowledge preservation. |
| Governance maturity | OMP is the permanent operating program. Authority boundaries, Runtime boundaries, Current Program State, Production Maturity, SYSTEM_MAP, and Canonical Reference are the active governance surfaces. |
| Project status | Stage 1 locked. Stage 2 locked knowledge complete. Product execution and continuation run through OMP, with volatile state owned by CPS. |

## 4. Canonical Inputs

Read these first when resuming V7:

1. `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`
2. `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
3. `docs/reference/V7_CANONICAL_REFERENCE.md`
4. `docs/reference/SYSTEM_MAP.md`
5. `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
6. `docs/reference/V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md`
7. `docs/reference/V7_CONTEXT_RESOLVER.md`
8. `docs/reports/research/V7_STAGE2_PROGRAM_FINAL_CERTIFICATION.md`
9. `docs/reports/research/V7_STAGE2_7_KNOWLEDGE_LOCK.md`
10. `docs/reports/research/V7_STAGE2_6_KNOWLEDGE_ACCEPTANCE.md`
11. `docs/reports/research/V7_STAGE1_FINAL_ACCEPTANCE.md`
12. `docs/reports/research/V7_STAGE1_CORPUS_AUDIT.md`
13. `docs/reports/research/V7_PHASE1_DOMAIN_CERTIFICATION.md`
14. `docs/reports/research/V7_PHASE1_ARCHITECT_SUMMARY.md`
15. `docs/programs/V7_AUTONOMOUS_EVOLUTION_PROGRAM.md`
16. `docs/reports/research/V7_AUTONOMOUS_EVOLUTION_PROGRAM_REFACTORING_PLAN.md`

Stage 1 recovery evidence:

- `docs/reports/research/V7_STAGE1_DIAGNOSIS_RECOVERY_DISCOVERY.md`
- `docs/reference/V7_DIAGNOSIS_RECORD_CONTRACT.md`
- `docs/process/V7_DIAGNOSIS_IMPLEMENTATION_ACCEPTANCE.md`
- `docs/reports/research/V7_STAGE1_DIAGNOSIS_IMPLEMENTATION_MISSION.md`
- `docs/reports/engineering/V7_STAGE1_DIAGNOSIS_IMPLEMENTATION_REPORT.md`

Important supporting references:

- `docs/prompts/V7_DOMAIN_ARCHITECTURE_CERTIFICATION_PROMPT.md`
- `docs/process/STAGE1_ACCEPTANCE_PROMPT.md`
- `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`
- `docs/reference/V7_SYSTEM_ARCHITECTURE.md`
- `docs/reference/V7_RUNTIME_MODEL.md`
- `docs/reference/V7_DECISION_MODEL.md`
- relevant ADRs under `docs/decisions/`
- Function Graph Appendix and JSON under `docs/reports/research/`
- Research R1-R4 under `docs/reports/research/`

Reports are evidence. Canonical owners preserve durable truth. Do not turn every report into a new owner.

## 5. Locked Architecture

The locked architecture contains exactly 26 domains:

1. Business Objective
2. System Laws
3. Product Principles
4. Reality Model
5. Observation
6. Health Evidence
7. Intelligence
8. Routing Intelligence
9. Wake
10. Incident
11. Diagnosis
12. Decision Model
13. Policy
14. Planner
15. Authority
16. Identity
17. Runtime
18. Execution
19. Verification
20. Rollback / Closure
21. Learning
22. Production Maturity
23. Current Program State
24. OMP
25. Engineering Automation
26. Continuous Self Evolution

The architecture chain is:

```text
Business Objective
  -> System Laws
  -> Product Principles
  -> Reality Model
  -> Observation
  -> Health Evidence
  -> Intelligence
  -> Routing Intelligence
  -> Wake
  -> Incident
  -> Diagnosis
  -> Decision Model
  -> Policy
  -> Planner
  -> Authority
  -> Identity
  -> Runtime
  -> Execution
  -> Verification
  -> Rollback / Closure
  -> Learning
  -> Production Maturity
  -> Current Program State
  -> OMP
  -> Engineering Automation
  -> Continuous Self Evolution
```

This structure is locked because:

- every domain has a unique mission;
- no current architectural responsibility appears twice;
- no required responsibility is missing;
- every domain has consumers;
- producer / consumer chains are continuous;
- Reality continuity is preserved;
- Authority continuity is preserved;
- implementation continuity is sufficient at architecture-audit level;
- Domain 11 recovery closed the only Stage 1 blocker;
- Stage 1.3 Corpus Audit passed;
- Final Acceptance passed.

Architecture Locked means:

- do not add domains by default;
- do not remove domains by default;
- do not rename domains by default;
- do not reorder domains by default;
- do not re-certify Stage 1 by default;
- do not create a duplicate architecture program;
- future architecture evolution must pass formal evolution procedures.

## 6. Stage 1 Result

Stage 1 is complete.

### Stage 1.1 Domain Certification

The Architecture Certification Engine certified the full 26-domain corpus. The first terminal pass found one incomplete domain: Domain 11 Diagnosis.

The finding was correct: the Diagnosis architecture was good, but implementation reality lacked one executable read-only Diagnosis / Owner Resolution projection.

### Stage 1.2 Recovery

Stage 1.2 did not redesign architecture.

It completed:

- recovery discovery;
- Diagnosis Record Contract;
- Diagnosis Implementation Acceptance;
- minimal implementation mission;
- implementation through existing owners;
- tests;
- implementation report;
- targeted Domain 11 recertification.

Domain 11 now has executable read-only evidence:

- schema `v7.diagnosis-owner-resolution.v1`;
- Diagnosis Record producer;
- validator;
- consumer projection;
- governance projection;
- tests for schema, unknown state, terminal classifications, first divergence, mutation boundary, consumers, and compatibility.

Domain 11 final result: `CERTIFIED`.

### Stage 1.3 Corpus Audit

Stage 1.3 audited the corpus as one architecture.

Result: `STAGE_1_3_PASS`.

It found:

- 0 critical blockers;
- 0 major blockers;
- 0 duplicate responsibilities;
- 0 missing responsibilities;
- 0 broken producer / consumer chains;
- 0 authority-boundary breaks;
- 0 reality-continuity breaks.

It accepted two minor non-blocking risks:

- historical superseded Domain 11 NOT CERTIFIED text remains in the append-only corpus;
- static Function Graph evidence may need refresh after Domain 11 recovery.

### Final Acceptance

Final Stage 1 Acceptance result:

```text
STAGE_1_ACCEPTED
STAGE_1_LOCKED
READY_FOR_STAGE_2
```

The Stage 1 Architecture Certification Corpus is now the official canonical architectural foundation of V7.

## 7. Current Roadmap

The active execution roadmap is OMP.

The active volatile state and next allowed action must be read from CPS:

```text
docs/programs/V7_CURRENT_PROGRAM_STATE.md
```

Future-Scale Scenario Engineering FSSE-01 through FSSE-04 is complete and consumed. OMP V4.28 and CPS Section 0 resolve recurring continuation through the existing Codex Automation Platform heartbeat and standard `Continue OMP` consumer.

Compressed completion-first plan:

| Position | Mission | Status |
|---|---|---|
| FSSE-01 | `V7_FUTURE_SCALE_POLYGON_FOUNDATION_V1` | `COMPLETE_CONSUMED` |
| FSSE-02 | `V7_FUTURE_SCALE_POLYGON_EXECUTION_HARNESS_V1` | `COMPLETE_CONSUMED` |
| FSSE-03 | `V7_FUTURE_SCALE_HIGH_FIDELITY_VALIDATION_V1` | `COMPLETE_CONSUMED` |
| FSSE-04 | `V7_OMP_FUTURE_SCALE_AUTONOMOUS_POLYGON_INTEGRATION_AND_CERTIFICATION_V1` | `COMPLETE_CONSUMED` |
| External reentry | existing Codex Automation Platform heartbeat | `PRODUCTION_CERTIFIED_TWO_NATURAL_REENTRIES` |

FSSE-01 established the foundation; FSSE-02 connected the real-code harness; FSSE-03 consumed the 40-scenario high-fidelity corpus; FSSE-04 certified bounded multi-transition `Continue OMP`; two natural external reentries then certified independent background engineering continuation. No FSSE phase should be replayed without a formal re-open trigger.

Scenario evidence is engineering evidence. It may reveal defects, justify source repair and certify invariant behavior. It may not claim production outcome, grant Authority, mutate Runtime, move users, or increase Production Maturity.

Stage 2 is not active execution work. It is the completed knowledge engineering route that produced `LOCKED_KNOWLEDGE`.

### Stage 2.1 Knowledge Inventory

Inventory all Stage 1 trusted knowledge, deltas, laws, boundaries, owner mappings, producer / consumer relationships, evidence references, and candidate canonical knowledge.

### Stage 2.2 Knowledge Extraction

Extract actual reusable architectural knowledge from the certification corpus. Do not recertify domains.

### Stage 2.3 Knowledge Deduplication

Collapse duplicated wording and repeated evidence into single canonical concepts while preserving meaning and provenance.

### Stage 2.4 Knowledge Graph

Build the graph of domains, laws, owners, producers, consumers, boundaries, evidence, gaps, decisions, and downstream canonical destinations.

### Stage 2.5 V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md

Create the canonical architecture knowledge document from the validated and deduplicated graph.

### Stage 2.6 Knowledge Acceptance

Independently verify that the extracted architecture knowledge is complete, consistent, traceable, and safe to use as canonical knowledge.

### Stage 2.7 Knowledge Lock

Lock the accepted knowledge baseline. After this, future work proceeds through OMP and formal evolution procedures.

Current continuation:

```text
Read handoff
  -> Resolve current context through ECR
  -> Read CPS for volatile current state
  -> Use OMP for execution decisions
  -> Use Canonical Reference for durable truth
  -> Use SYSTEM_MAP for owners
  -> Use Engineering Reports only as evidence
  -> Continue OMP or run approved Discovery
```

## 8. What Has Been Completed

Completed:

- V7 product identity clarified: governed production routing platform, not merely VPN protocols.
- Stage 1 Architecture Certification Engine created, evolved, locked, and executed.
- 26-domain architecture tree materialized and frozen.
- Domain Certification Corpus completed.
- Architect Summary completed.
- Domain 11 Diagnosis recovery completed.
- Diagnosis Record Contract completed.
- Diagnosis Implementation Acceptance completed.
- Diagnosis implementation mission completed.
- Diagnosis implementation completed through existing owners.
- Domain 11 recertified as `CERTIFIED`.
- Stage 1 Corpus Audit passed.
- Stage 1 Final Acceptance passed.
- Stage 1 locked as canonical architectural foundation.
- Stage 2 Knowledge Engineering completed.
- `docs/reference/V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md` accepted.
- Stage 2 Knowledge Graph accepted.
- Stage 2 Knowledge Lock completed.
- `LOCKED_KNOWLEDGE` recorded.
- Stage 2 program final certification completed.
- Architecture Closed by Default remains active.
- OMP remains the permanent operating program.
- Current Program State is the only live volatile state owner.
- Canonical Reference is the durable truth owner.
- SYSTEM_MAP is the owner/topology map.
- Existing Owner Law remains active.
- Reality First remains active.
- Authority and Runtime boundaries remain active.
- Continuous Self Evolution remains part of the locked architecture.
- Mission Completion Evidence Gate is active. Tests, deployment, reports and CPS edits alone do not prove functional completion.
- FSSE-01 Future-Scale Polygon Foundation is implemented, deployed and consumed.
- FSSE-02 Future-Scale Polygon Execution Harness is implemented and consumed for `CAPACITY_BOUNDARY`.
- FSSE-03 high-fidelity validation and FSSE-04 autonomous Polygon integration are complete and consumed.
- Two distinct natural external reentries certify independent background engineering continuation.
- FSSE current-state and derived-registry consistency correction is implemented and committed; the current source delta still requires canonical safe deploy.
- All 40 current high-fidelity scenarios are covered; the current next action is `AUTHORIZE_SAFE_DEPLOY_CURRENT_CANONICAL_HEAD`.

Completed historical work must not be reopened unless objective evidence proves corruption, contradiction, or a formally accepted evolution need.

## 9. What Remains

Active engineering execution work:

- obtain explicit Engineering Authority for the canonical safe deploy of `CURRENT_CANONICAL_HEAD`;
- deploy only through `tools/v7-safe-deploy` and the existing allowlist;
- verify truth `--all`, convergence and runtime snapshot equality;
- then reconcile the existing production-closure Mission without replaying FSSE or the natural heartbeat evidence;
- preserve no routing mutation, no user movement and no Authority expansion.

Known non-blocking follow-up:

- two natural external reentries are certified automation evidence; current source convergence remains pending safe deploy and this is not Runtime or routing autonomy;
- CAP-U07 remains protected capability-local WIP at its real-world dependency boundary;
- append-only historical Domain 11 NOT CERTIFIED text remains superseded by Stage 1.2 terminal evidence;
- old Function Graph evidence should be used as discovery/index evidence unless current implementation evidence proves a contradiction.

## 10. System Laws And Invariants

### Reality First

Real production evidence wins over guesses, synthetic examples, stale reports, planner-only assumptions, and desired outcomes.

### Existing Owner Law

Before creating anything new:

```text
DISCOVER
  -> REUSE
  -> EXTEND
  -> CREATE ONLY IF NECESSARY
```

New owners are allowed only when no existing canonical owner can legally own the responsibility.

### Authority Boundary

Authority owns permission, blast radius, capability budget, promotion, demotion, and policy prohibition. Authority does not observe reality, select arbitrary candidates, mutate routing, or verify outcomes.

### Runtime Boundary

Runtime is thin. It consumes committed approved identity and either applies safely or stops. Runtime does not invent decisions, replace Planner, bypass Authority, bypass Restore Barrier, bypass Verification, or create truth.

### Decision != Execution

Decision Model, Policy, and Planner prepare action. Runtime and Execution apply only after Authority and identity gates.

### Verification Law

A production action is not successful until Verification proves the outcome.

### Mission Completion Evidence Gate

Mission completion evidence must match the declared Mission type. Source changes, passing tests, deployment, a report, a manual Codex call, or a CPS status edit cannot alone prove stronger functional completion.

Integration completion requires a real non-test caller, a real consumer, verified consumption, behavior change and a next output. Automation additionally requires an independent real trigger, idempotency, duplicate suppression and a bounded legal terminal. Runtime and Production completion require their corresponding real effects, verification and owner acceptance.

The gate is active in OMP and consumed by existing truth/convergence owners. Future threads must not repeat report/test-only OMP cycles.

### Rollback / Closure Law

Every touched action must end in rollback, containment, no-rollback closure, success closure, or canonical terminal classification.

### Diagnosis Law

Diagnosis is read-only. It explains root cause and owner resolution from evidence. It does not mutate Runtime, Planner, Authority, Restore Barrier, users, or production state.

### OMP Law

OMP is the operating program. It maps work to owners, consumes maturity, prevents duplicate roadmaps, and continues execution.

OMP is the only execution program. It must consume CPS for volatile current state, Canonical Reference for durable truth, SYSTEM_MAP for owner topology, and Engineering Reports as evidence.

### Architecture Closed By Default

Future architecture change is exceptional. It requires proof that existing OMP capabilities, canonical owners, SYSTEM_MAP, Canonical Reference, Runtime Model, Decision Model, policies, and backlog cannot express the required capability.

### Current State Consistency

OMP owns operating rules and may preserve historical snapshots, but CPS is the only authoritative live volatile state. Any apparent current/next/highest/focus/status value outside CPS is live only when confirmed by CPS.

Location:

```text
docs/programs/OPERATIONAL_MATURITY_PROGRAM.md
docs/programs/V7_CURRENT_PROGRAM_STATE.md
docs/reference/V7_CANONICAL_REFERENCE.md
```

### Engineering Truth Lifecycle

Any engineering truth reused by OMP, Codex, BDP, Mission, dashboards, Engineering Intelligence, or future automation must have an owner, truth source, validity basis, invalidation triggers, revalidation route, and reuse rule. Existing owners must classify reused truth before it can be consumed as current.

Location:

```text
docs/programs/OPERATIONAL_MATURITY_PROGRAM.md
docs/reference/V7_CANONICAL_REFERENCE.md
```

### Automation Gap Closure

Every STOP or unfinished Engineering Intent must be classified as a real boundary or routed through the existing BDP -> OMP path as a possible automation-removal Implementation Candidate Instance. This creates no new Automation Engine, owner, planner, runtime, or roadmap.

Location:

```text
docs/programs/OPERATIONAL_MATURITY_PROGRAM.md
```

### Engineering Intent Closure Validation

An automation-gap closure is not complete just because work happened. It is complete only when the original Engineering Intent is achieved, the original STOP or Intent Gap disappears, Current State matches Expected State, and the Engineering Chain reaches a Legal Terminal Consumer.

Location:

```text
docs/programs/OPERATIONAL_MATURITY_PROGRAM.md
```

### Intent Gap Detection

OMP must detect unfinished Engineering Intent even when execution or verification appears to pass. A formal PASS does not close work if the intended state was not achieved.

Location:

```text
docs/programs/OPERATIONAL_MATURITY_PROGRAM.md
```

### Intent Responsibility Resolution

Every `INTENT_GAP_DETECTED` must identify the last responsible Engineering Chain link and owner-mapped responsibility class, or record `UNKNOWN_WITH_REASON` and the smallest existing next action. Generic routing without owner-mapped responsibility is forbidden.

Location:

```text
docs/programs/OPERATIONAL_MATURITY_PROGRAM.md
docs/reference/V7_CANONICAL_REFERENCE.md
```

### Necessity Framework

Every permanent owner, capability, function, module, service, CLI, API, read model, dashboard, engineering process, or document must be auditable for why it deserves to exist. OMP consumes the existing Necessity Framework; it does not create a Necessity Engine or new owner.

Location:

```text
docs/reference/V7_NECESSITY_FRAMEWORK.md
docs/programs/OPERATIONAL_MATURITY_PROGRAM.md
docs/reference/SYSTEM_MAP.md
```

### Capability Maturity Protection

Necessity, merge, removal, value conservation, collapse, owner elimination, function elimination, and architectural minimization must not alter an element that belongs to an unfinished capability. Such elements are protected until the capability reaches an accepted terminal state.

Location:

```text
docs/programs/OPERATIONAL_MATURITY_PROGRAM.md
docs/reference/V7_CANONICAL_REFERENCE.md
```

### Engineering Work In Progress Protection

Architectural minimization must not alter any engineering object participating in unfinished work: Mission, Candidate, Engineering Chain, Behavior Chain, State Transition, Verification, Certification, dependency, root cause, producer/consumer handoff, integration, BDP Discovery, or another active lifecycle.

Location:

```text
docs/programs/OPERATIONAL_MATURITY_PROGRAM.md
docs/reference/V7_CANONICAL_REFERENCE.md
```

### Approved Future Dependency Protection

Architectural minimization must not alter an object already required by an approved future Mission, Candidate, Engineering Chain, Capability plan, State Transition, Verification, Certification, Integration, Producer, Consumer, Behavior Chain, Runtime Transition, `Depends On`, `Unblocks`, or other accepted execution dependency.

Location:

```text
docs/programs/OPERATIONAL_MATURITY_PROGRAM.md
docs/reference/V7_CANONICAL_REFERENCE.md
```

### Research First Rule

Before creating any new fundamental mechanism, V7 must perform world research, read official documents, build a cross-system matrix, compare with V7, and prove a real gap. Fundamental mechanisms must not be created from intuition.

### Prompt Evolution Law

The Architecture Certification Engine is locked. Future prompt changes are allowed only when repeated execution evidence justifies them. The canonical standard requires real weakness evidence, not theoretical discussion.

### Continuous Self Evolution

Every meaningful project action should improve at least one of:

- product capability;
- automation capability;
- workflow orchestration;
- knowledge quality;
- owner clarity;
- future engineering leverage.

### Future-Scale Scenario Evidence Boundary

When ordinary safe engineering work is exhausted, OMP may continue through the existing Future-Scale Scenario Engineering frontier. Deterministic scenario evidence is engineering evidence only. It can reveal a reproducible defect and drive an existing-owner repair, but cannot become production truth, Runtime authority, action-class authority, user movement or Production Maturity credit.

## 11. Governance Model

V7 governance is distributed but not ambiguous.

| Surface | Role |
|---|---|
| Canonical Reference | Durable project meaning and canonical conclusions. |
| SYSTEM_MAP | Owner and topology lookup. |
| OMP | Permanent operating program and continuation owner. |
| Current Program State | Volatile current state and next-action surface. |
| Production Maturity | Evidence-consuming production maturity state. |
| ADRs | Durable architectural decisions and rejected alternatives. |
| Engineering Reports | Historical evidence and proof. |
| Function Graph | Implementation reality and dependency evidence. |
| Domain Certification Corpus | Stage 1 architecture evidence. |
| Locked Knowledge | Permanent architecture knowledge baseline in `docs/reference/V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md`. |

No single report becomes a new truth source by itself.

No dashboard or summary may reinterpret canonical truth.

## 12. Production And Runtime Model

The canonical production execution chain remains:

```text
Observation
  -> Wake
  -> Incident
  -> Diagnosis
  -> Decision Model
  -> Policy
  -> Planner
  -> Authority
  -> Identity
  -> Runtime
  -> Execution
  -> Verification
  -> Rollback / Closure
  -> Learning
  -> Production Maturity
  -> Current Program State
  -> OMP
```

Important boundaries:

- Observation does not decide.
- Wake does not grant authority.
- Incident does not execute.
- Diagnosis does not mutate.
- Planner does not apply.
- Authority does not verify success.
- Runtime does not plan.
- Execution does not claim success.
- Verification does not create authority.
- Rollback / Closure is terminal safety.
- Learning consumes outcomes; it does not rewrite history.
- OMP routes continuation; it does not bypass production gates.

## 13. PROJECT MEMORY

This section preserves what Stage 1, Stage 2, and later OMP refinements taught as knowledge, not as a chronological diary.

### Product Knowledge

V7's product is reliable governed routing, not VPN protocol management.

Users receive continuity. Operators receive controlled autonomy. Engineers receive a system whose future work can be routed through known owners instead of improvised from scratch.

### Architecture Knowledge

The 26-domain model is complete because each domain owns one responsibility and the full chain closes from Business Objective to Continuous Self Evolution.

The architecture is intentionally explicit. It separates reality, evidence, diagnosis, decision, policy, planning, authority, identity, runtime, execution, verification, closure, learning, maturity, state, OMP, automation, and self-evolution because mixing these responsibilities creates unsafe production behavior.

### Locked Knowledge

Stage 2 converted the locked Stage 1 architecture into permanent engineering memory.

The canonical baseline is:

```text
docs/reference/V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md
```

Future engineering must consume this baseline before re-extracting Stage 1 reports. Reports remain provenance and evidence, not durable truth owners.

### Certification Knowledge

Certification is not documentation approval. Certification is evidence-backed proof that architecture and implementation reality align well enough for the stated domain.

Append-only certification history can contain superseded states. Consumers must read the latest terminal state, not the first historical state.

### Domain 11 Knowledge

Domain 11 was the only Stage 1 blocker. The problem was not architecture. The problem was missing executable implementation: V7 had reports and owner-resolution concepts, but lacked one canonical read-only Diagnosis / Owner Resolution Record.

The fix proved an important rule: when architecture is correct and implementation is incomplete, do not redesign architecture. Extend the existing owner minimally and recertify.

### World Convergence Knowledge

V7 converges with mature engineering practice through:

- observability before action;
- evidence before confidence;
- diagnosis before decision;
- policy before execution;
- authority before mutation;
- bounded blast radius;
- thin runtime;
- post-action verification;
- rollback / closure;
- feedback and learning;
- operational maturity;
- controlled autonomy expansion.

V7 does not copy another company. It independently expresses universal production engineering laws in a form suitable for autonomous routing.

### Implementation Knowledge

Implementation reality matters. Architecture is not accepted if Function Graph, tests, current code, or runtime owners contradict it.

Read-only advisory surfaces are allowed. They must not mutate Runtime, expand Authority, rank execution directly, synthesize evidence, or become truth sources.

### Governance Knowledge

No duplicate owners. No duplicate Runtime. No duplicate Planner. No duplicate Authority. No duplicate OMP. No duplicate truth source.

If a future task seems to need a new owner, first prove why existing owners cannot own it.

### Evolution Knowledge

Future work should simplify execution, not multiply documents. The correct path is usually:

```text
Reality
  -> Evidence
  -> Owner Resolution
  -> Existing Owner
  -> Implementation if needed
  -> Verification
  -> Engineering Report
  -> Canonical Update if durable
  -> Current Program State if volatile
  -> Continue OMP
```

### Recent Completion-Truth Knowledge

The Phase 2-to-current retrospective proved that reports, tests and deployment can establish useful evidence without establishing real functional closure. A named consumer is insufficient unless it invokes and consumes the output. A manual Codex call is not independent automation. A state update without behavior change is not implementation completion.

FSSE-02 satisfies integration completion because `tools/v7-truth-check --omp-scenario-execution` is a real non-test caller, real V7 Planner and execution-preview owners are invoked, `OMP_PROGRAM_EXECUTION_RECONCILIATION` consumes the normalized PASS, coverage changes from 0 to 1, and the exact next Mission is `V7_FUTURE_SCALE_HIGH_FIDELITY_VALIDATION_V1`.

Independent background automation satisfies automation completion because two distinct natural Codex Automation Platform events invoked the standard `Continue OMP` consumer after prior turns exited, used unique event/invocation identities, released leases without overlap, preserved idempotency/duplicate suppression and produced bounded next outputs with zero Runtime, production or Authority effects.

### Common Misunderstandings To Avoid

- Do not confuse Stage 1 architecture lock with full production autonomy.
- Do not confuse Stage 2 `LOCKED_KNOWLEDGE` with a new execution program.
- Do not treat reports as active roadmaps.
- Do not treat Engineering Reports as current truth owners.
- Do not treat OMP historical snapshots as current volatile state; CPS wins.
- Do not treat historical `NOT CERTIFIED` text as current if later terminal evidence supersedes it.
- Do not re-run Stage 1 or Stage 2 by default.
- Do not create `V7_MASTER_PROJECT_HANDOFF_V2`.
- Do not use Function Graph staleness as an architecture failure unless current implementation evidence also contradicts the architecture.
- Do not use documentation sync as a blocker for capability producers unless a safety owner requires it.
- Do not let Runtime decide.
- Do not let Planner execute.
- Do not let Diagnosis mutate.
- Do not let OMP become a duplicate Runtime.
- Do not add Engineering Confidence, a new owner, a new engine, a new architecture, or OMP changes for Engineering Truth Usage before the required world research proves a real gap.
- Do not treat passing FSSE schema/tests or a scenario report as an executed scenario consumer.
- Do not recreate or manually duplicate the active certified heartbeat; it is the existing external reentry owner.
- Do not wait for rare production events when the existing FSSE frontier can produce bounded engineering evidence.

## 14. STARTING A NEW CHAT

### Current Entrypoint For A New Thread

Read in this order:

1. `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`;
2. `docs/programs/V7_CURRENT_PROGRAM_STATE.md`, Section 0 only for live volatile state;
3. `docs/reports/engineering/2026-07-16_001627_full_independent_background_automation_and_fsse04_production_closure.md`;
4. `docs/reports/engineering/2026-07-15_214500_future_scale_autonomous_polygon_integration_and_certification.md`;
5. OMP V4.28 external reentry and Future-Scale sections;
6. `tools/v7_sync_lib.py` and `tools/v7-truth-check`;
7. `docs/reports/engineering/evidence/V7_OMP_EXTERNAL_REENTRY_RUNS.jsonl` only when external reentry evidence is required.

Use ECR before widening context. Use Canonical Reference for durable meaning, SYSTEM_MAP for owner topology, OMP for continuation, and Engineering Reports only as evidence. CPS Section 0 overrides all current-looking historical snapshots.

Then execute:

```text
Discover -> Reuse -> Extend -> Implement
Continue OMP

ACTION:
Continue OMP
```

Required boundary:

- do not repeat FSSE-01 through FSSE-04;
- do not recreate, pause or replace the certified heartbeat without a separate owner-authorized Mission;
- do not start unrelated capability work;
- do not create a new simulator, owner, Planner, Runtime, scheduler, queue or truth source;
- do not use toy decision logic as proof;
- preserve CAP-U07 protected capability-local WIP;
- preserve no Runtime mutation, no production mutation, no user movement, no Authority expansion and no Production Maturity credit.

Already proven and reusable:

- Stage 1 architecture is accepted and locked;
- Stage 2 knowledge is locked;
- OMP is the only execution operating system;
- CPS is the only volatile current-state owner;
- Mission Completion Evidence Gate is active;
- FSSE-01 is complete, deployed and consumed;
- FSSE-02 is complete and consumed for `CAPACITY_BOUNDARY`;
- FSSE-03 and FSSE-04 are complete and consumed;
- two distinct natural external reentries are certified owner-backed automation evidence;
- AEP Phase 5 is `COMPLETE_CONSUMED_TWO_NATURAL_REENTRIES`;
- current-state consistency and local/GitHub truth are aligned; production convergence and snapshot equality are pending safe deploy;
- `SAFE_DEPLOY_CURRENT_CANONICAL_HEAD` is the current program frontier;
- `EXTERNAL_INPUT_REQUIRED = TRUE` and `OMP_CONTINUATION_REQUIRED = FALSE` until deploy authority is granted;
- scenario frontier generation is `fssef_dcd80bd4189d95ec7c58d661`;
- current coverage fingerprint is `dcd80bd4189d95ec7c58d661af3ac313c1f7760f925c9937f9f15dfe40f873df`.

Do not recreate this handoff under another filename. Do not run a broad architecture audit unless a formal Re-open Trigger exists.

## 15. Final Self Review

Obsolete active roadmap removed:

YES.

Completed work still presented as future work:

NO.

Duplicated explanations collapsed:

YES.

Can a new engineer continue from this document alone:

YES.

Important Stage 1 knowledge missing:

NO.

Current active roadmap:

OMP execution through CPS and ECR; certified independent background reentry invokes the bounded standard `Continue OMP` frontier.

Ready for seamless continuation:

YES
