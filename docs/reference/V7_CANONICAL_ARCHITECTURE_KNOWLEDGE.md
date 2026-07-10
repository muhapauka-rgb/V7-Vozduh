# V7 Canonical Architecture Knowledge

Status: `LOCKED_KNOWLEDGE`
Program: `V7.STAGE2.KNOWLEDGE_ENGINEERING`
Stage: `Stage 2.7 - Knowledge Lock`
Created: 2026-07-07
Owner: Knowledge Owner / Canonical Reference / SYSTEM_MAP / OMP
Input baseline: `STAGE_1_LOCKED`
Current stage result: `STAGE_2_KNOWLEDGE_LOCKED`
Accepted by: `docs/reports/research/V7_STAGE2_6_KNOWLEDGE_ACCEPTANCE.md`
Locked by: `docs/reports/research/V7_STAGE2_7_KNOWLEDGE_LOCK.md`

This document is the canonical Stage 2 architecture knowledge baseline for V7.

It is permanent engineering memory. It is not a report, handoff, research note, execution log, or implementation summary.

It contains only accepted, deduplicated, owner-mapped, terminal-state-resolved engineering knowledge from:

- Deduplicated Knowledge Registry;
- Knowledge Merge Map;
- Superseded Knowledge Map;
- Stage 2 Knowledge Graph.

It does not contain unresolved research, manual review items, superseded current truth, historical evidence as active truth, or new architecture.

## 1. Knowledge Baseline

V7 has two foundations:

```text
LOCKED_ARCHITECTURE
LOCKED_KNOWLEDGE
```

`LOCKED_ARCHITECTURE` is the immutable Stage 1 architecture foundation.

`LOCKED_KNOWLEDGE` is the Stage 2 permanent engineering memory derived from that foundation.

Stage 2 knowledge exists to let engineers, Codex, OMP, audits, research, and implementation work use accepted engineering truth without rediscovering it from reports.

Baseline laws:

- Stage 1 architecture is locked.
- Stage 2 does not redesign architecture.
- Stage 2 does not create domains, owners, OMP, Runtime, Planner, Authority, roadmaps, or truth sources.
- Stage 2 knowledge must preserve Source, Owner, Trust Level, Terminal State, Provenance, Destination, Consumer, and Forbidden Misuse through direct fields or deterministic graph/source references.
- History is preserved as provenance only; history never becomes current truth.

## 2. Architecture Laws

### Locked Architecture Baseline

The Stage 1 architecture baseline is locked.

Engineering rule:

- Do not reopen Stage 1.
- Do not change the architecture tree.
- Do not grant production authority through Stage 2 knowledge work.

Graph pointer: `DK-2.3-001`
Provenance pointer: `KO-2.2R-001`

### Architecture Closed By Default

Architecture change is closed by default.

Engineering rule:

- No architecture change is authorized unless existing owners cannot express the required capability and an official change path proves that limitation.
- Stage 2 knowledge work cannot be used as evidence of architecture-change permission.

Graph pointer: `DK-2.3-029`
Provenance pointer: `KO-2.2R-029`

### Reality First

Reality First is active.

Engineering rule:

- Implementation evidence, reports, or derived observations cannot override locked architecture outside an official change path.
- Verification must confirm reality before promotion or consumption.

Graph pointer: `DK-2.3-030`
Provenance pointer: `KO-2.2R-030`

### Existing Owner Before New Owner

Existing owners must be used before any new owner is considered.

Engineering rule:

- Do not create duplicate, hidden, or ownerless responsibility.
- Responsibility must route through existing canonical owners.

Graph pointer: `DK-2.3-031`
Provenance pointer: `KO-2.2R-031`

## 3. Domain Knowledge

The architecture contains exactly 26 domain responsibilities.

Engineering rule:

- Do not add domains.
- Do not remove domains.
- Do not merge domains.
- Do not split domains.
- Do not reorder domains.
- Each domain responsibility remains independently graph-consumable.

Graph pointer: `DK-2.3-002`
Provenance pointer: `KO-2.2R-002`

| Domain | Canonical responsibility | Graph pointer | Provenance pointer |
|---|---|---|---|
| Domain 01 | Business Objective Responsibility | `DK-2.3-003` | `KO-2.2R-003` |
| Domain 02 | System Laws Responsibility | `DK-2.3-004` | `KO-2.2R-004` |
| Domain 03 | Product Principles Responsibility | `DK-2.3-005` | `KO-2.2R-005` |
| Domain 04 | Reality Model Responsibility | `DK-2.3-006` | `KO-2.2R-006` |
| Domain 05 | Observation Responsibility | `DK-2.3-007` | `KO-2.2R-007` |
| Domain 06 | Health Evidence Responsibility | `DK-2.3-008` | `KO-2.2R-008` |
| Domain 07 | Intelligence Responsibility | `DK-2.3-009` | `KO-2.2R-009` |
| Domain 08 | Routing Intelligence Responsibility | `DK-2.3-010` | `KO-2.2R-010` |
| Domain 09 | Wake Responsibility | `DK-2.3-011` | `KO-2.2R-011` |
| Domain 10 | Incident Responsibility | `DK-2.3-012` | `KO-2.2R-012` |
| Domain 11 | Diagnosis Responsibility | `DK-2.3-013` | `KO-2.2R-013` |
| Domain 12 | Decision Model Responsibility | `DK-2.3-014` | `KO-2.2R-014` |
| Domain 13 | Policy Responsibility | `DK-2.3-015` | `KO-2.2R-015` |
| Domain 14 | Planner Responsibility | `DK-2.3-016` | `KO-2.2R-016` |
| Domain 15 | Authority Responsibility | `DK-2.3-017` | `KO-2.2R-017` |
| Domain 16 | Identity Responsibility | `DK-2.3-018` | `KO-2.2R-018` |
| Domain 17 | Runtime Responsibility | `DK-2.3-019` | `KO-2.2R-019` |
| Domain 18 | Execution Responsibility | `DK-2.3-020` | `KO-2.2R-020` |
| Domain 19 | Verification Responsibility | `DK-2.3-021` | `KO-2.2R-021` |
| Domain 20 | Rollback / Closure Responsibility | `DK-2.3-022` | `KO-2.2R-022` |
| Domain 21 | Learning Responsibility | `DK-2.3-023` | `KO-2.2R-023` |
| Domain 22 | Production Maturity Responsibility | `DK-2.3-024` | `KO-2.2R-024` |
| Domain 23 | Current Program State Responsibility | `DK-2.3-025` | `KO-2.2R-025` |
| Domain 24 | OMP Responsibility | `DK-2.3-026` | `KO-2.2R-026` |
| Domain 25 | Engineering Automation Responsibility | `DK-2.3-027` | `KO-2.2R-027` |
| Domain 26 | Continuous Self Evolution Responsibility | `DK-2.3-028` | `KO-2.2R-028` |

Domain 11 current truth:

- Domain 11 Diagnosis is certified in the current terminal state.
- Historical `NOT CERTIFIED` text must remain historical and must not become current truth.
- Diagnosis must not mutate production.

Graph pointers: `DK-2.3-013`, `DK-2.3-038`
Provenance pointers: `KO-2.2R-013`, `KO-2.2R-038`

## 4. Producer / Consumer Knowledge

Stage 2 is a producer/consumer chain. Each stage consumes only accepted output from the previous stage.

| Producer stage | Consumer stage | Canonical rule | Graph pointer | Provenance pointer |
|---|---|---|---|---|
| Stage 2.1 Knowledge Inventory | Stage 2.2 Knowledge Extraction | Stage 2.2 consumes accepted inventory output only. | `DK-2.3-047` | `KO-2.2R-047` |
| Stage 2.2 Knowledge Extraction | Stage 2.3 Knowledge Deduplication | Stage 2.3 consumes accepted extraction output only. | `DK-2.3-048` | `KO-2.2R-048` |
| Stage 2.3 Knowledge Deduplication | Stage 2.4 Knowledge Graph | Stage 2.4 consumes accepted deduplicated output only. | `DK-2.3-049` | `KO-2.2R-049` |
| Stage 2.4 Knowledge Graph | Stage 2.5 Canonical Architecture Knowledge | Stage 2.5 consumes accepted graph output only. | `DK-2.3-050` | `KO-2.2R-050` |
| Stage 2.5 Canonical Architecture Knowledge | Stage 2.6 Knowledge Acceptance | Stage 2.6 consumes canonical knowledge output only after Stage 2.5 is ready. | `DK-2.3-051` | `KO-2.2R-051` |
| Stage 2.6 Knowledge Acceptance | Stage 2.7 Knowledge Lock | Stage 2.7 consumes accepted knowledge acceptance output only. | `DK-2.3-052` | `KO-2.2R-052` |
| Stage 2.7 Knowledge Lock | OMP Continuation | OMP continuation consumes the locked knowledge baseline. | `DK-2.3-053` | `KO-2.2R-053` |

Stage gate rule:

- Do not start a later stage before the previous acceptance gate.
- `READY` does not mean `IN_PROGRESS`.
- A separate operator command is required to start the next stage.

Graph pointers: `DK-2.3-045`, `DK-2.3-046`
Provenance pointers: `KO-2.2R-045`, `KO-2.2R-046`

## 5. Authority And Runtime Boundaries

### Authority

Authority owns permission and scope.

Engineering rule:

- Authority ownership is not execution ownership.
- Authority ownership is not verification ownership.
- Authority must not observe reality, select arbitrary candidates, mutate routing, or verify outcomes.

Graph pointers: `DK-2.3-032`, `DK-2.3-033`
Provenance pointers: `KO-2.2R-032`, `KO-2.2R-033`

### Runtime

Runtime applies authorized decisions inside its boundary.

Engineering rule:

- Runtime must not invent decisions.
- Runtime must not replace Planner.
- Runtime must not bypass Authority.
- Runtime must not bypass Verification.
- Runtime must not create truth.

Graph pointer: `DK-2.3-034`
Provenance pointer: `KO-2.2R-034`

## 6. Verification And Rollback Knowledge

### Verification Before Promotion

Action, autonomy, and capability state cannot be promoted without verification evidence.

Graph pointer: `DK-2.3-035`
Provenance pointer: `KO-2.2R-035`

### Evidence Before Consumption

Unverified evidence and generic reports are not durable knowledge.

Engineering rule:

- Evidence must be verified before consumption.
- Reports can be evidence, but reports are not durable truth owners.

Graph pointers: `DK-2.3-040`, `DK-2.3-044`
Provenance pointers: `KO-2.2R-040`, `KO-2.2R-044`

### Rollback

Rollback requires an authorized safe path.

Engineering rule:

- Do not perform rollback without authority and safety proof.

Graph pointer: `DK-2.3-036`
Provenance pointer: `KO-2.2R-036`

### Closure

Closure requires terminal outcome evidence.

Engineering rule:

- Do not treat an action as closed without observed outcome, verification, rollback, safe stop, or escalation evidence.

Graph pointer: `DK-2.3-037`
Provenance pointer: `KO-2.2R-037`

## 7. Governance And OMP Knowledge

OMP is the permanent operating program.

Engineering rule:

- Stage 2 must not become duplicate OMP.
- Stage 2 must not become Runtime.
- Stage 2 must not become Planner.
- Stage 2 must not become Authority.
- Stage 2 must not become a truth source outside accepted knowledge.

Graph pointer: `DK-2.3-039`
Provenance pointer: `KO-2.2R-039`

CPS volatile-state rule:

- Current Program State is a volatile current-state surface.
- Current Program State must not be treated as durable canonical truth.

Graph pointer: `DK-2.3-059`
Provenance pointer: `KO-2.2R-059`

Product identity:

- V7 is a governed routing platform.
- V7 must not be reduced to VPN protocol mechanics.
- Product goals must not bypass safety.

Graph pointer: `DK-2.3-060`
Provenance pointer: `KO-2.2R-060`

## 8. Owner And Evidence Rules

Canonical owners preserve durable truth.

Engineering rule:

- Reports are evidence, not durable truth owners.
- Durable truth must be preserved by canonical owners.
- Durable findings promote through existing canonical owners.
- Durable findings must not promote through new owners or bypass acceptance.

Graph pointers: `DK-2.3-040`, `DK-2.3-041`, `DK-2.3-042`
Provenance pointers: `KO-2.2R-040`, `KO-2.2R-041`, `KO-2.2R-042`

No Orphan Artifact Law:

- Do not consume artifacts missing Producer, Consumer, Owner, Acceptance, Terminal State, or Storage Location.

Graph pointer: `DK-2.3-043`
Provenance pointer: `KO-2.2R-043`

ADR rules:

- ADRs preserve durable architecture decisions.
- Changed decisions require an ADR update or a new ADR.
- Superseded ADR history must not become current truth.

Graph pointers: `DK-2.3-063`, `DK-2.3-064`, `DK-2.3-065`
Provenance pointers: `KO-2.2R-063`, `KO-2.2R-064`, `KO-2.2R-065`

## 9. Evolution Rules

Policy behavior must not be invented ad hoc.

Engineering rule:

- Do not create operational policy from opinion or isolated reports.
- Policy becomes operational only through governed lifecycle.
- Policy implementation requires research, fit analysis, verification, certification, and OMP integration.

Graph pointers: `DK-2.3-061`, `DK-2.3-062`
Provenance pointers: `KO-2.2R-061`, `KO-2.2R-062`

Knowledge evolution rule:

- Accepted knowledge may evolve only through existing owners, verification, acceptance, and the future Knowledge Evolution path.
- Stage 2 canonical knowledge does not authorize self-approved mutation.

Graph pointers: `DK-2.3-027`, `DK-2.3-028`, `DK-2.3-042`
Provenance pointers: `KO-2.2R-027`, `KO-2.2R-028`, `KO-2.2R-042`

## 10. Forbidden Actions

Stage 2 must not:

- change locked architecture;
- change domain names, order, or responsibilities;
- change owners;
- change truth sources;
- change Runtime;
- change Planner;
- change Authority;
- change production routing;
- change OMP;
- perform later-stage work inside an earlier stage;
- promote superseded history as current truth;
- turn reports into durable truth owners;
- create operational policy from opinion or isolated reports;
- treat self-evolution as self-authorized mutation.

Graph pointers: `DK-2.3-054`, `DK-2.3-055`, `DK-2.3-056`, `DK-2.3-057`, `DK-2.3-058`, `DK-2.3-065`
Provenance pointers: `KO-2.2R-054`, `KO-2.2R-055`, `KO-2.2R-056`, `KO-2.2R-057`, `KO-2.2R-058`, `KO-2.2R-065`

## 11. Terminal State Rules

Terminal-state rules:

- Current truth is the terminal state.
- Superseded text remains provenance only.
- Historical evidence can explain how current truth was reached, but cannot become active truth.
- Domain 11 current truth is certified.
- Superseded ADR history is not current truth.
- Old Stage 2 labels do not override the approved Knowledge Engineering route.

Graph pointers: `DK-2.3-038`, `DK-2.3-045`, `DK-2.3-065`
Provenance pointers: `KO-2.2R-038`, `KO-2.2R-045`, `KO-2.2R-065`

## 12. Knowledge Graph Pointers

Canonical knowledge is backed by the Stage 2 Knowledge Graph.

Graph artifact:

```text
docs/reports/research/V7_STAGE2_4_KNOWLEDGE_GRAPH.md
```

Graph metrics:

| Metric | Value |
|---|---:|
| Primary DK nodes | 65 |
| Total graph nodes | 191 |
| Total graph edges | 223 |
| Deduplicated input concepts | 65 |

Required graph families are represented:

- domains;
- laws;
- principles;
- owners;
- responsibilities;
- producer / consumer relationships;
- boundaries;
- forbidden actions;
- evidence;
- terminal states;
- decisions;
- implementation owners;
- destination owners;
- risks;
- manual review items.

## 13. Provenance Index

Every canonical knowledge entry in this document resolves provenance through:

```text
Canonical Section
  -> DK-2.3-* graph pointer
  -> KO-2.2R-* source object pointer
  -> accepted Stage 2.3 / Stage 2.4 artifacts
```

The canonical document does not repeat raw report summaries. It stores stable graph and source-object pointers.

| Range | Knowledge family | Graph pointers | Provenance pointers |
|---|---|---|---|
| Baseline and architecture laws | Lock, closed architecture, Reality First, Existing Owner | `DK-2.3-001`, `DK-2.3-029`, `DK-2.3-030`, `DK-2.3-031` | `KO-2.2R-001`, `KO-2.2R-029`, `KO-2.2R-030`, `KO-2.2R-031` |
| Domain responsibilities | 26-domain chain and Domain 01 through Domain 26 | `DK-2.3-002` through `DK-2.3-028` | `KO-2.2R-002` through `KO-2.2R-028` |
| Authority / Runtime / Rollback / Closure | Authority, Runtime, rollback, closure | `DK-2.3-032` through `DK-2.3-037` | `KO-2.2R-032` through `KO-2.2R-037` |
| Domain 11 terminal state | Diagnosis certified terminal state | `DK-2.3-038` | `KO-2.2R-038` |
| Governance / OMP / evidence | OMP, reports, owners, promotion, no-orphan, evidence | `DK-2.3-039` through `DK-2.3-044` | `KO-2.2R-039` through `KO-2.2R-044` |
| State machine / producer-consumer | Stage state and Stage 2 chain | `DK-2.3-045` through `DK-2.3-053` | `KO-2.2R-045` through `KO-2.2R-053` |
| Forbidden Stage 2 actions | Architecture, owner/truth, runtime/routing, OMP, later-stage prohibitions | `DK-2.3-054` through `DK-2.3-058` | `KO-2.2R-054` through `KO-2.2R-058` |
| CPS / product / policy / ADR | CPS, product identity, policy lifecycle, ADR rules | `DK-2.3-059` through `DK-2.3-065` | `KO-2.2R-059` through `KO-2.2R-065` |

## 14. Consumer Index

This canonical knowledge is intended for:

- OMP;
- Canonical Reference;
- SYSTEM_MAP;
- Current Program State;
- Codex sessions;
- engineering implementation;
- architecture review;
- certification;
- research;
- future knowledge evolution.

Consumer rules:

- Consumers may use this document as current Stage 2 canonical knowledge only after Stage 2.6 acceptance.
- Consumers must not use this document to change architecture, owners, Runtime, Planner, Authority, routing, OMP, or terminal states.
- Consumers must follow graph and provenance pointers when deeper evidence is required.
- Manual review and risk nodes in the graph are not active canonical knowledge.

## 15. Engineering Entity Model

Status: `CANONICAL_KNOWLEDGE_EVOLUTION`

The Engineering Entity Model is the single canonical definition of V7 engineering entities.

It canonicalizes entities already present in LOCKED_ARCHITECTURE, LOCKED_KNOWLEDGE, AEP, BDP, OMP, CPS, SYSTEM_MAP, Canonical Reference, Runtime Model, Decision Model, Function Graph, Engineering Reports, and production evidence.

It does not create:

- new architecture;
- new owner;
- new program;
- new Runtime;
- new Planner;
- new truth source;
- new storage system;
- new execution queue.

Future AEP, BDP, OMP, CPS, Engineering Report, Canonical Reference, SYSTEM_MAP, and Codex work must use this section as the canonical vocabulary for engineering entities. Program-specific definitions may specialize lifecycle or fields, but must not redefine the entity identity.

### 15.1 Entity Governance Rules

Entity rules:

1. An engineering entity is real only if it has an engineering purpose, boundary, owner or existing owner path, producer, consumer, lifecycle, terminal state, and relationship to other entities.
2. A named concept without owner, producer, consumer, lifecycle, and terminal state is a field, attribute, view, evidence, or analytical lens, not an independent entity.
3. Reports, dashboards, discovery indexes, function names, file names, and narrative headings do not create entity identity.
4. AEP, BDP, and OMP must not define the same entity differently. If a term appears in multiple programs, this chapter owns the canonical entity definition.
5. Entity lifecycle completion requires producer output, consumer assignment, verified consumption, behaviour or state change where applicable, and legal terminal state.
6. Entity evolution must follow Discover -> Reuse -> Extend -> Implement through existing owners.
7. Entity canonicalization never grants authority, mutates Runtime, changes production, creates missions, or updates CPS by itself.

### 15.2 Canonical Entity Registry

| Entity | Status | Purpose | Boundary | Owner | Producer | Consumer | Input | Output | Lifecycle | Terminal State | Relationships |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Engineering Intent | `REAL_ENTITY` | Preserve the engineering purpose that a behaviour, rule, gate, mission, or implementation is meant to close. | Intent is purpose and closure expectation only; it is not execution, authority, or implementation. | Originating owner; BDP for Intent Closure analysis; OMP for admitted Mission intent. | Architecture law, programme rule, owner contract, report, operator command, or existing behaviour evidence. | BDP, OMP, Codex Mission input, Engineering Report, Verification, Learning. | Existing purpose, expected state, current state, evidence. | Intent Closure status, Expected Intent Closure, Mission intent. | Declared -> traced -> closure-assessed -> consumed by implementation or terminal alternative -> verified. | `INTENT_CLOSED`, `INTENT_CLOSED_WITH_LIMITS`, `AUTOMATION_BREAK`, `INTENT_NOT_APPLICABLE`, `INTENT_UNKNOWN`. | Drives Behaviour analysis, Automation Break detection, Implementation Candidate generation, Mission closure, Learning. |
| Behaviour Definition | `REAL_ENTITY` | Define a canonical type of autonomous behaviour. | Type-level behaviour only; it does not execute. | AEP / BDP using existing canonical owners and Reality evidence. | AEP ideal model, BDP discovery, Canonical Knowledge, Function Graph, Runtime / Decision evidence. | Behaviour Catalogue, Behaviour Coverage, Behaviour Graph, BDP, AEP Phase 2 / Phase 3, OMP when candidate is admitted. | Evidence of behaviour type, owner, sources, relationships. | Accepted Behaviour Definition record. | Discovered -> identity resolved -> evidence linked -> coverage assessed -> graph/catalogued -> evolved if new evidence requires. | `ACTIVE`, `PARTIAL`, `SUPERSEDED`, `NOT_APPLICABLE`, `MANUAL_REVIEW`. | Aggregates Behaviour Instances; may lead to Implementation Candidate only through BDP readiness and OMP admission. |
| Behaviour Instance | `REAL_ENTITY` | Represent a concrete occurrence or execution of a Behaviour Definition in current reality. | Instance-level situation only; not a new owner, Runtime, Planner, or truth source. | BDP / AEP Reality model; actual operational owner remains the existing domain owner. | Runtime evidence, production evidence, Engineering Reports, CPS, Function Graph, implementation, tests, operator evidence. | Behaviour Reality, Behaviour Coverage, Automation Readiness, Intent Closure, OMP if implementation candidate is admitted. | Situation, context, evidence, current state, decision/execution/verification/learning traces. | Behaviour Instance record and traceability path. | Observed -> identity resolved -> trace linked -> validated -> consumed by Reality / BDP -> aggregated or terminal. | `OBSERVED`, `VALIDATED`, `PARTIAL`, `SUPERSEDED`, `REJECTED`, `UNKNOWN`. | Instantiates Behaviour Definition; may expose Automation Break, Outcome, Learning, Production Evidence. |
| Automation Break | `CHAIN_STATE_RECORD` | Record the Engineering Chain state where existing logic stops before achieving its original intent. | Chain state and evidence record only; not a certified Gap, OMP Mission, authority grant, production state, backlog item, or independent entity. | BDP. | Intent Closure analysis over Behaviour, rule, gate, policy, verification, rollback, Runtime path, decision path, execution path, or engineering condition. | BDP reports, AEP Phase 3, OMP after acceptance as implementation/blocker evidence. | Intent trace, last successful step, stopping point, reason for stop, owner, producer, consumer. | Automation Break Catalogue / Matrix evidence record. | Detected -> classified -> owner/consumer resolved -> implementation readiness evaluated -> consumed, terminal alternative, or not applicable. | `MANUAL_STEP`, `MANUAL_APPROVAL`, `MISSING_TRIGGER`, `MISSING_EXECUTION`, `MISSING_VERIFICATION`, `MISSING_ROLLBACK`, `MISSING_RUNTIME`, `MISSING_CONSUMER`, `MISSING_OWNER_EXTENSION`, `MISSING_IMPLEMENTATION`, `NOT_REPRODUCIBLE`, `NOT_AUTOMATABLE`. | May generate Implementation Candidate only when missing implementation is bounded and owner-mapped. |
| Implementation Candidate Class | `REAL_ENTITY` | Represent a reusable engineering problem pattern that may appear in multiple real situations. | Class-level pattern only; cannot become a Mission by itself. | OMP admission model consuming BDP output. | BDP Implementation Candidate Catalogue, Engineering Intent Closure, Automation Readiness, accepted owner evidence. | OMP, Mission admission, duplicate prevention, Cohort safety review. | Class signature: intent, break type, affected behaviour/capability/owner/consumer, policy/verification/rollback/authority pattern. | Candidate Class identity. | Discovered -> normalized -> matched against existing classes -> reused or extended -> consumed by Instance admission. | `ACTIVE`, `MERGED`, `SUPERSEDED`, `NOT_APPLICABLE`. | Groups Implementation Candidate Instances; prevents class-only Mission creation. |
| Implementation Candidate Instance | `REAL_ENTITY` | Represent one concrete engineering situation that may require implementation. | Instance-level implementation input only; not a queue, backlog, owner, roadmap, mission, or execution permission. | OMP admission model; BDP produces candidate input. | BDP Implementation Candidate Catalogue or accepted existing-owner input. | OMP admission, existing owner, Codex after Mission assignment, Verification, Engineering Report. | Engineering Intent, Automation Break, affected Behaviour/capability/owner/consumer, current/expected state, evidence window, runtime/user/group/channel scope, verification, rollback, authority, policy. | `MISSION_ACCEPTED`, `MISSION_HOLD`, `MISSION_REJECTED`, `MISSION_NOT_APPLICABLE`, merged evidence, or Cohort Mission membership. | Discovered -> normalized -> duplicate checked -> merge/cohort reviewed -> admitted/held/rejected/not applicable -> implemented/verified/closed or reopened. | `DISCOVERED`, `NORMALIZED`, `MERGED`, `MISSION_CREATED`, `IN_PROGRESS`, `IMPLEMENTED`, `VERIFIED`, `CLOSED`, `SUPERSEDED`, `REOPENED`. | Consumed by OMP; may produce Mission; may attach to Cohort Mission; may reopen after closure. |
| Mission | `REAL_ENTITY` | OMP-admitted implementation unit with owner, intent, dependencies, authority, verification, rollback, Runtime, production, Codex handoff, and terminal state. | Mission is execution-management identity only; it is not a Runtime actor, authority source, owner, queue, or truth source. | OMP; Codex may assist when assigned. | OMP admission from Backlog, existing owner, or accepted Implementation Candidate Instance / safe Cohort. | Codex, implementation owner, Verification, Engineering Report, CPS, Reality / BDP refresh when required. | Admitted work item, Engineering Intent, owner, dependencies, authority, verification, rollback, runtime/production boundaries. | Implemented change, verified no-change, hold/rejection, terminal evidence. | Created -> assigned -> implemented or held -> verified -> reported -> CPS/canonical update when needed -> closed/reopened/superseded. | `MISSION_CREATED`, `IN_PROGRESS`, `IMPLEMENTED`, `VERIFIED`, `CLOSED`, `SUPERSEDED`, `REOPENED`, `TERMINAL_HOLD`, `TERMINAL_REJECTED`, `TERMINAL_IMPOSSIBLE`. | Consumes Implementation Candidate Instance; produces Implementation, Verification, Engineering Report, Outcome/Learning evidence. |
| Capability | `REAL_ENTITY` | Represent a durable system ability or maturity workstream owned by existing architecture. | Capability is not a queue and not a Mission; Mission may implement or certify part of a Capability. | Existing capability owner via SYSTEM_MAP / OMP / Production Maturity Model. | Architecture baseline, OMP maturity model, production evidence, implementation evidence. | OMP, Production Maturity, CPS, Canonical Reference, engineering work. | Capability definition, owner, maturity, blockers, dependencies, evidence. | Capability state, maturity change, certification, retirement/deprecation. | Defined -> owner-mapped -> matured/implemented/certified -> consumed by production maturity -> locked/retired/deprecated. | `NOT_STARTED`, `IN_PROGRESS`, `COMPLETED`, `CERTIFIED`, `CONSUMED`, `BLOCKED`, `WAITING`, `RETIRED`, `DEPRECATED`. | Aggregates Missions, evidence, Production Maturity, CPS and Canonical updates. |
| Verification | `REAL_ENTITY` | Prove behaviour, truth, convergence, safety, no unintended mutation, and implementation effect. | Verification is proof path and evidence; it does not authorize action or replace Runtime / Planner. | Verification owners, truth/convergence owners, OMP when task-class requires. | Implementation owner, Runtime, tests, production observation, reports. | OMP, Certification, Engineering Report, Learning, Production Maturity, Canonical Knowledge. | Expected result, actual result, tests, runtime/prod evidence, safety/rollback checks. | Verification result and evidence. | Planned -> executed -> result classified -> consumed by Mission / Capability / Certification / Learning. | `PASS`, `PASS_WITH_LIMITS`, `FAIL`, `INCONCLUSIVE`, `NOT_APPLICABLE_WITH_REASON`, `BLOCKED`. | Gates promotion, Mission closure, Outcome, Learning, Production Evidence, Canonical updates. |
| Reality | `REAL_ENTITY` | Represent current observed system state and real production/implementation/behaviour conditions. | Reality is observed state, not desired state, roadmap, authority, or design. | Reality Model / CPS / Runtime / production owners depending on scope. | Runtime, production, tests, reports, CPS, operator observation, implementation evidence. | AEP, BDP, OMP, Verification, Production Maturity, Canonical Reference when durable. | Current state, runtime state, production state, behaviour evidence, blockers. | Reality snapshot, Reality evidence, Reality refinement proposal, CPS update when volatile. | Observed -> verified/classified -> consumed by program/owner -> updated or terminal no-change recorded. | `CURRENT`, `STALE`, `UNKNOWN`, `VERIFIED`, `CONTRADICTED`, `SUPERSEDED`, `NOT_APPLICABLE`. | Produces Behaviour Instances, Production Evidence, Outcomes, OMP inputs, Learning triggers. |
| Engineering Report | `REAL_ENTITY` | Preserve historical evidence, action context, verification, decisions, risks, and learning triggers after meaningful engineering work. | Evidence and history only; not roadmap, backlog, authority, owner, or truth source. | Report lifecycle owner / OMP report lifecycle. | Codex, engineer, OMP Mission, certification, audit, research, implementation work. | OMP, Canonical owner, CPS, SYSTEM_MAP, future engineering, audits, Knowledge Evolution. | Work performed, sources, evidence, review results, decisions, verification, next action. | Engineering Report artifact. | Created -> reviewed -> consumed by owner/canonical path -> durable conclusions promoted or left historical. | `HISTORICAL_EVIDENCE`, `CONSUMED`, `PARTIAL`, `SUPERSEDED`, `NOT_CANONICAL`. | Supports Verification, Outcome, Learning, Canonical Update, CPS update, Mission closure. |
| Canonical Knowledge | `REAL_ENTITY` | Preserve accepted durable engineering truth for future engineering consumption. | Durable knowledge only; not raw report, manual review, unresolved research, or production authority. | Knowledge Owner / Canonical Reference / SYSTEM_MAP / OMP according to knowledge type. | Stage 2 knowledge lock, Knowledge Evolution, accepted canonical updates. | AEP, BDP, OMP, CPS, Engineering Reports, Codex, audits, implementation. | Accepted knowledge, provenance, owner, trust, terminal state, consumer, forbidden misuse. | LOCKED_KNOWLEDGE / canonical update. | Proposed -> verified -> accepted -> locked/promoted -> consumed -> evolved through official Knowledge Evolution when required. | `LOCKED`, `LOCKED_KNOWLEDGE_VNEXT`, `SUPERSEDED`, `HISTORICAL`, `MANUAL_REVIEW`, `REJECTED`. | Defines entity vocabulary, laws, owner rules, boundaries, producer/consumer relationships. |
| Production Evidence | `REAL_ENTITY` | Prove real deployed/runtime/production effect or limitation. | Real evidence only; synthetic, advisory, or report-only evidence is insufficient. | Runtime / production / verification / feedback owners. | Production runtime, governed execution, canary, convergence, operator outcome, monitoring. | Verification, OMP, Production Maturity, Learning, Certification, Canonical Knowledge when durable. | Runtime result, service/user/channel state, convergence, trust/confidence, outcome records. | Production evidence record. | Observed -> attributed -> verified -> consumed by outcome/learning/maturity/certification -> preserved. | `VALID`, `VALID_WITH_LIMITS`, `STALE`, `CONTRADICTED`, `INSUFFICIENT`, `NOT_APPLICABLE`. | Supports Outcome, Learning, Verification, Mission closure, Capability certification. |
| Outcome | `REAL_ENTITY` | Record the observed result of a decision, action, implementation, rollback/no-rollback, or verification path. | Result record only; it does not decide future action without Learning/OMP consumption. | Feedback / outcome owners. | Runtime execution, verification, production evidence, operator action, report. | Learning, OMP, Production Maturity, trust/confidence, future decisions. | Action/decision identity, expected result, actual result, verification, production evidence. | Outcome closure record. | Produced -> verified -> classified -> consumed by Learning / OMP / maturity -> preserved. | `SUCCESS`, `FAILURE`, `PARTIAL`, `NO_CHANGE`, `INCONCLUSIVE`, `NOT_APPLICABLE`. | Feeds Learning, Production Evidence, Verification, Engineering Report, future Behaviour evidence. |
| Learning | `REAL_ENTITY` | Convert verified outcomes into future decision, confidence, recommendation, knowledge, or no-change evidence. | Learning is evidence-derived improvement; it does not mutate Runtime or authority by itself. | Feedback / learning owners, OMP for engineering learning, canonical owner when durable. | Outcome, production evidence, verification, reports, prediction vs reality comparison. | OMP, Planner/trust owners, Production Maturity, Canonical Knowledge, future missions. | Outcome closure, prediction delta, confidence delta, recommendation quality, affected owner. | Learning record, recommendation update, confidence/evidence update, canonical update need, or no-change decision. | Triggered -> evidence resolved -> update/no-change classified -> consumed by owner/OMP/canonical path -> future decision affected. | `LEARNED`, `NO_CHANGE`, `INSUFFICIENT_EVIDENCE`, `BLOCKED`, `SUPERSEDED`, `NOT_APPLICABLE`. | Closes Outcome loop and supports continuous self-evolution. |

### 15.3 Non-Independent Entity Rules

These concepts may appear in AEP, BDP, OMP, reports, Runtime, or implementation, but they are not independent engineering entities unless they satisfy the Entity Governance Rules:

| Concept | Canonical classification | Rule |
| --- | --- | --- |
| Behaviour | Umbrella term. | Use `Behaviour Definition` or `Behaviour Instance` when identity matters. |
| Autonomous Behaviour Unit | Analytical record. | Represents a Behaviour Instance in AEP/BDP analysis; it is not a separate executable entity. |
| Law Execution Unit | Nested analytical segment. | Part of Behaviour Instance reasoning/execution; not a standalone entity. |
| Behaviour Surface | Analytical Discovery lens. | Helps group Behaviour discovery passes; not an architecture level, owner, storage, Runtime, Planner, or truth source. |
| Function Graph | Discovery index. | Helps locate implementation relationships; it is not canonical truth by itself. |
| Knowledge Graph | Traceability graph. | Supports knowledge relationships; canonical truth lives in accepted Canonical Knowledge. |
| Dashboard / read model / diagnostic surface | View or evidence surface. | Not a terminal consumer and not authority. |
| Backlog | Post-admission implementation registry. | Records admitted OMP Mission state; does not discover candidates or authorize implementation by itself. |
| Codex Implementation Input | Handoff payload. | Assigns scoped implementation work only after OMP/operator assignment; not an owner or production dependency. |

### 15.4 Engineering Chain Model

Status: `CANONICAL`

Engineering Chain is the canonical relationship model between existing Engineering Entity records.

Engineering Chain is not:

- a new Engineering Entity;
- a new owner;
- a new Runtime;
- a new Planner;
- a new program;
- a new architecture;
- a new truth source;
- a new storage system;
- a new execution queue.

Engineering Chain describes how existing entities relate by Producer -> Consumer links, how Engineering Intent moves through work, and how closure is proven.

Any V7 engineering work must be treated as an Engineering Chain, not as a set of unrelated functions, files, reports, or implementation steps.

#### 15.4.1 Canonical Engineering Chain

Canonical Engineering Chain:

```text
Engineering Intent
  -> Trigger
  -> Condition
  -> Behaviour Instance
  -> Decision
  -> Execution
  -> Verification
  -> Outcome
  -> Learning
  -> Intent Closure
```

Canonical chain mapped to the Engineering Entity Registry:

| Chain segment | Canonical entity / classification | Rule |
| --- | --- | --- |
| Engineering Intent | `Engineering Intent` | Every chain starts with purpose or explicit `INTENT_NOT_APPLICABLE`. |
| Trigger | Input / producer signal | Trigger is a field or event, not a standalone entity unless it satisfies Entity Governance Rules. |
| Condition | Reality / policy / rule condition | Condition is the observed or required state that activates the chain. |
| Behaviour Instance | `Behaviour Instance` | Concrete occurrence where the intent is evaluated or executed. |
| Decision | Decision Model / existing decision owner output | Decision is a chain segment; it does not replace Planner, Runtime, or Authority. |
| Execution | Mission / implementation / Runtime execution owner output | Execution may be real action, no-action, hold, or legal terminal alternative. |
| Verification | `Verification` | Verification proves whether execution or no-action matched expected result. |
| Outcome | `Outcome` | Outcome records actual result. |
| Learning | `Learning` | Learning consumes verified outcome and affects future evidence, confidence, recommendation, or canonical update. |
| Intent Closure | Closure state of `Engineering Intent` | Closure compares original intent with verified outcome. |

Extended chain when implementation work is required:

```text
Engineering Intent
  -> Trigger / Condition
  -> Behaviour Instance
  -> Intent Closure analysis
  -> Automation Break when intent is not closed
  -> Implementation Candidate Class / Instance when implementation is bounded and owner-mapped
  -> OMP Mission when admitted
  -> Implementation
  -> Verification
  -> Production Evidence / Outcome
  -> Learning
  -> Engineering Report
  -> Canonical Knowledge / CPS / SYSTEM_MAP / OMP update when required
  -> Reality
```

`Automation Break` is a chain state and closure disposition. The Automation Break Catalogue / Matrix may store evidence records for that state, but the state itself does not create a new owner, Runtime, Planner, Mission, architecture, authority grant, or execution permission.

#### 15.4.2 Chain Closure

Engineering Chain is closed only when:

```text
Engineering Intent == Verified Outcome
```

or when an explicit terminal alternative proves why the intent is not applicable, cannot be completed, or must stop safely.

Closure requires:

1. Engineering Intent is present or explicitly `INTENT_NOT_APPLICABLE`.
2. Producer is identified for every produced output.
3. Consumer is identified for every consumed output.
4. Consumption is verified through owner state, tests, runtime behaviour, certification evidence, CPS, canonical owner, or explicit `NOT_APPLICABLE_WITH_REASON`.
5. Outcome is verified.
6. Outcome is compared against Engineering Intent.
7. Learning / no-change / terminal alternative is recorded.
8. Terminal State exists.

If the chain ends but Engineering Intent does not match Outcome, the chain is not closed. It must be classified as `AUTOMATION_BREAK`, `BLOCKED`, `STOP_SAFE`, `NOT_APPLICABLE`, or `UNKNOWN` with reason.

#### 15.4.3 Chain Walk

Any program or owner using Engineering Chain may walk the chain:

- forward from Engineering Intent to Outcome and Learning;
- backward from Outcome to Engineering Intent;
- from any entity to its producer;
- from any entity to its consumer;
- from a blocker to the last successful step;
- from a terminal state to the evidence that proves it.

Chain Walk must use Producer -> Consumer relationships only. It must not infer hidden relationships from name similarity, file proximity, narrative wording, or function adjacency.

Forward walk answers:

```text
What should this intent produce next?
```

Backward walk answers:

```text
What intent, source, owner, and evidence produced this outcome?
```

Middle-out walk answers:

```text
What producer created this entity, who consumes it, and what terminal state can close it?
```

#### 15.4.4 Chain States

Canonical Engineering Chain states:

| State | Meaning |
| --- | --- |
| `OPEN` | Chain has a valid intent or trigger and has not reached a terminal state. |
| `PARTIALLY_CLOSED` | Some expected outputs were produced or consumed, but intent/outcome equivalence or terminal consumer proof is incomplete. |
| `CLOSED` | Verified Outcome satisfies Engineering Intent, or an accepted terminal alternative legally closes the chain. |
| `AUTOMATION_BREAK` | Chain stopped before Engineering Intent was achieved. |
| `BLOCKED` | Existing owner, evidence, authority, verification, rollback, Runtime, consumer, or dependency prevents continuation. |
| `STOP_SAFE` | Safe legal stop was produced instead of unsafe continuation. It prevents unsafe mutation but does not equal successful intent closure unless the intent was safe stop itself. |
| `NOT_APPLICABLE` | Chain does not apply to the current entity, scope, owner, or evidence context, with reason. |
| `UNKNOWN` | Evidence is insufficient to classify closure. |

Forbidden chain terminal states:

- report created with no consumer;
- dashboard/read-model visible with no owner consumption;
- recommendation emitted with no OMP or owner routing;
- implementation exists with no verification;
- verification exists with no outcome classification;
- outcome exists with no learning/no-change/terminal alternative;
- consumer named but consumption unverified.

#### 15.4.5 Chain Invariants

Engineering Chain invariants:

1. Every chain starts with Engineering Intent or explicit `INTENT_NOT_APPLICABLE`.
2. Every chain ends with Intent Closure, Automation Break, legal terminal alternative, or explicit unknown/blocked state.
3. Every produced entity or output must have Producer and Consumer.
4. A named Consumer is not proof of consumption.
5. A created report, dashboard view, recommendation, diagnostic output, or read-only status is not terminal closure.
6. The chain must not lose Engineering Intent.
7. The chain must not end without Terminal State.
8. Chain Closure requires Intent/Outcome comparison.
9. Automation Break must name last successful step, stopping point, reason for stop, owner, producer, consumer, and terminal alternative when one exists.
10. Chain Walk must be deterministic and traceable to existing owners or evidence.
11. Chain Model must not create or rename Engineering Entities.
12. Program-specific chains in AEP, BDP, OMP, CPS, reports, Codex, SYSTEM_MAP, and Canonical Reference must reuse this model rather than define independent chain semantics.

#### 15.4.6 Program Consumers

| Consumer | Engineering Chain usage |
| --- | --- |
| AEP | Uses Engineering Chain to trace Reality -> Behaviour Instance -> Gap / implementation need -> OMP continuation without creating execution authority. |
| BDP | Uses Engineering Chain for Intent Closure, Forward Trace, Backward Trace, Automation Break, Implementation Candidate readiness, traceability, and coverage. |
| OMP | Uses Engineering Chain to admit Candidate Instances, form Missions, verify producer/consumer consumption, classify completion, and prevent report-only closure. |
| CPS | Stores volatile current chain state, blocker, current task, stop reason, and next action only when volatile state changes. It does not redefine the chain. |
| Engineering Reports | Preserve chain evidence, reviews, actions, blockers, verification, outcome, learning trigger, and next action. Reports are evidence, not terminal closure. |
| Canonical Reference | Stores current system truth produced by closed chains when durable and accepted. It does not define separate chain semantics. |
| SYSTEM_MAP | Resolves owners, producers, consumers, and topology for Chain Walk. It does not prove truth by itself. |
| Codex | Executes or analyzes only the chain segment assigned by OMP/operator and must preserve intent, owner, producer, consumer, verification, outcome, report, and terminal state. |

Engineering Chain is therefore the canonical model of relationships between Engineering Entities. Future AEP, BDP, OMP, CPS, Engineering Report, Canonical Reference, SYSTEM_MAP, and Codex work must use it as the single source of truth for chain semantics.

### 15.5 Entity Certification

Entity Review: `PASS`.
Lifecycle Review: `PASS`.
Producer Review: `PASS`.
Consumer Review: `PASS`.
Relationship Review: `PASS`.
Chain Review: `PASS`.
Chain Closure Review: `PASS`.
Intent Review: `PASS`.
Automation Break Review: `PASS`.
Duplication Review: `PASS`.
Reuse Review: `PASS`.
No New Entity Review: `PASS`.
No New Architecture Review: `PASS`.
Quality Review: `PASS`.
Self Review: `PASS`.

Certification verdict:

```text
ENGINEERING_ENTITY_MODEL_CANONICALIZED
```

The canonical entity model is complete enough for future AEP, BDP, OMP, CPS, Engineering Report, Canonical Reference, SYSTEM_MAP, and Codex work to use as the single source of engineering entity definitions.

## 16. Acceptance State

This document passed Stage 2.6 Knowledge Acceptance and Stage 2.7 Knowledge Lock.

Current state:

```text
LOCKED_KNOWLEDGE
```

Acceptance and lock evidence:

```text
STAGE_2_KNOWLEDGE_ACCEPTED_WITH_MINOR_RISKS
STAGE_2_KNOWLEDGE_LOCKED
```
