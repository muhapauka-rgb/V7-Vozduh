# V7 Behaviour Discovery Program

Status: `CANONICAL_PROGRAM_READY_FOR_IMPLEMENTATION`
Document status: `CANONICAL_PROGRAM_READY_FOR_IMPLEMENTATION`
Execution status: `EXECUTED_FOR_LIMITED_SCENARIO_SCOPE; CURRENT_PROJECT_SCOPE_ACCEPTED_BY_AEP_PHASE_2`
Current consumer: `AEP Phase 3 consumes the accepted Phase 2 Reality; no project-wide BDP terminal claim`
Project-scope terminal status: `NOT_TERMINAL; formal P01-P19 run evidence is incomplete`
Purpose: Permanent reproducible engineering mechanism for discovering V7 Engineering Chains, Autonomous Behaviour inside those chains, Automation-Ready Engineering Logic, Implementation-Ready engineering work, Engineering Intent Closure, and Engineering Logic Automation Coverage.
Date: `2026-07-08`

## 1. Purpose

The V7 Behaviour Discovery Program is the permanent engineering program for discovering, validating, and certifying observed V7 Engineering Chains and the Behaviour Instances inside those chains after project changes.

The primary discovery object is now:

```text
Engineering Chain
```

Behaviour remains mandatory inside every Engineering Chain. BDP does not replace Behaviour Discovery; it places Behaviour Discovery inside the canonical chain:

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

Its purpose is also to discover existing V7 engineering logic that is ready, limited-ready, or blocked from automatic execution through existing owners, OMP, Runtime, Verification, Rollback, Production Maturity, and CPS.

Its purpose is also to identify which existing Behaviour, Automation Candidate, rule, gate, condition, policy, verification, rollback, or authority rule is sufficiently defined to become a real implementation task through existing OMP and Codex execution discipline.

Its purpose is also to measure what portion of existing V7 engineering logic is already discovered, understood, formalized, automation-ready, implementation-ready, implemented, verified, and production-enabled.

Its purpose is also to detect where existing V7 engineering logic stops before its original engineering intent is achieved.

It makes this process reproducible:

```text
Project Change
  -> Engineering Chain Discovery
  -> Behaviour Discovery inside Chain
  -> Evidence Validation
  -> Behaviour Validation
  -> Chain Walk
  -> Automation Readiness Assessment
  -> Implementation Readiness Assessment
  -> Implementation Candidate Instance Packaging
  -> Engineering Intent Closure Assessment
  -> Engineering Logic Automation Coverage Assessment
  -> Reality Refinement Proposal
  -> Reality Certification
  -> Current Autonomous Behaviour Reality candidate
```

The program does not discover desired behaviour. It discovers current observed engineering behaviour.

Core law:

```text
Evidence Before Abstraction
```

Official order:

```text
Engineering Chain
  -> Engineering Intent
  -> Trigger / Condition
  -> Observed Behaviour Instance
  -> Evidence
  -> Validation
  -> Behaviour Definition
  -> Decision / Execution / Verification / Outcome / Learning Trace
  -> Automation Readiness
  -> Implementation Readiness
  -> Implementation Candidate Instance
  -> Engineering Intent Closure
  -> Engineering Logic Coverage
  -> Behaviour Reality
```

Never:

```text
Architecture
  -> Expected Behaviour
  -> Assumed Reality
```

## 2. Non Goals

This program must not:

- create Runtime;
- create Planner;
- create OMP;
- create a new architecture;
- create a new truth source;
- create a new Knowledge Owner;
- create a new identity owner;
- create a new intent owner;
- create a new memory system;
- create a new storage system;
- modify AEP;
- modify AOS;
- modify `LOCKED_ARCHITECTURE`;
- modify `LOCKED_KNOWLEDGE`;
- modify Current Autonomous Behaviour Reality automatically;
- create Autonomous Behaviour Gaps;
- create Automation Gaps automatically;
- create OMP automation missions;
- create a second automation queue;
- create a new coverage owner;
- create a new progress truth source;
- create OMP missions from Implementation Candidates;
- update the official OMP Implementation Backlog;
- prioritize or schedule OMP implementation work;
- assign Codex implementation work automatically;
- execute Implementation Candidates;
- execute Phase 3;
- execute Runtime actions;
- move users;
- expand authority;
- automatically execute Automation-Ready Engineering Logic;
- treat automation readiness as authority;
- replace Function Graph;
- replace Knowledge Graph;
- replace OMP;
- replace CPS.

## 3. Relationship With AEP

AEP remains the strategic post-Stage-2 program route.

The Behaviour Discovery Program is a reusable discovery mechanism that AEP may invoke when Phase 2 or a future operator-approved Reality Refinement requires a current Behaviour Reality build.

Relationship:

```text
AEP
  -> requests Behaviour Discovery
  -> consumes certified Behaviour Reality output
  -> decides whether Phase 2 / Reality Refinement / later phases may proceed
```

BDP does not define AEP phases and does not change AEP state.

BDP may support AEP by identifying Automation-Ready Engineering Logic and Automation Gaps inside observed Behaviour. AEP remains responsible for deciding whether later phases may consume these findings.

## 4. Relationship With Phase 2

Phase 2 is the AEP phase that builds Current Autonomous Behaviour Reality.

BDP is the repeatable mechanism that can produce Phase 2-compatible evidence and candidate Reality artifacts.

BDP may be used:

- for initial Phase 2 execution;
- after a project change;
- before a Reality Refinement;
- before Phase 3 if the current Reality requires updated evidence;
- after implementation evidence changes.

BDP does not itself approve Phase 2 completion. Phase 2 acceptance remains outside this program unless the operator explicitly runs acceptance.

Phase 2-compatible evidence may include Automation Readiness evidence where it is derived from existing conditions, gates, policies, checks, verification paths, rollback paths, authority boundaries, maturity rules, or continuation rules.

## 5. Relationship With OMP

OMP remains the only execution operating system.

BDP may produce certified Reality evidence and OMP-ready automation input that OMP can later consume through existing AEP/OMP routes.

BDP may also produce OMP-ready Implementation Candidate Instances and Codex Implementation Input when existing engineering logic is sufficiently defined as a real engineering situation through existing owners.

BDP cannot:

- create OMP missions;
- create OMP automation missions;
- create OMP implementation missions;
- prioritize OMP work;
- update the official OMP Implementation Backlog;
- assign Codex tasks;
- bypass OMP;
- update OMP state;
- execute OMP;
- create a second OMP queue.

OMP may consume BDP output only when the output has a certified consumer path.

BDP outputs may become OMP implementation input only after certification and chain closure. BDP does not select, schedule, authorize, assign Codex, or execute implementation.

The final BDP output consumed by OMP must be an `Implementation Candidate Instance`, not an abstract improvement, document, rule, validation, model, owner, or report.

OMP compatibility requires that BDP package a concrete engineering situation that can be admitted, rejected, held, converted into a Mission, implemented, verified, learned from, and closed by OMP.

## 6. Relationship With Current Autonomous Behaviour Reality

Current Autonomous Behaviour Reality is the target artifact that represents observed Behaviour Reality.

BDP can produce:

- a candidate Reality build;
- a Reality Refinement Proposal;
- evidence needed to update Reality;
- certification evidence for a Reality update.

BDP cannot update Current Autonomous Behaviour Reality automatically.

Allowed path:

```text
Behaviour Discovery Program
  -> Reality Refinement Proposal
  -> Reality Certification
  -> Operator / Program Acceptance
  -> Current Autonomous Behaviour Reality update
```

## 7. Relationship With Canonical Knowledge

`LOCKED_KNOWLEDGE` and Canonical Knowledge are inputs and reference boundaries.

BDP may use Canonical Knowledge to interpret evidence, laws, owners, and forbidden actions.

BDP must use the Engineering Entity Model and Engineering Chain Model in `docs/reference/V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md` as the single canonical source for:

- Engineering Entity definitions;
- Engineering Chain semantics;
- Chain states;
- Chain Closure;
- Chain Walk;
- Automation Break as chain state record;
- Producer -> Consumer relationship rules.

BDP may specialize these canonical rules into discovery fields, matrices, reports, and validation gates, but it must not redefine Engineering Chain independently.

BDP must not:

- change locked knowledge;
- canonicalize new knowledge;
- create a knowledge object;
- run Stage 2 again;
- replace Knowledge Evolution.

If BDP discovers that Behaviour evidence contradicts locked knowledge, it records a contradiction and routes it to the existing Knowledge Evolution owner path. It does not rewrite knowledge.

## 8. Relationship With Existing Discovery Systems

BDP reuses existing discovery systems. It does not create a parallel discovery architecture.

| Existing System | Reused As | Rule |
| --- | --- | --- |
| Stage 1 Architecture Certification / Corpus Validation | Architecture boundary and terminal architecture evidence | Cannot be reopened by BDP. |
| Stage 2 Knowledge Inventory | Source family discovery, source classification, trust/owner/terminal-state patterns | Reuse inventory/exhaustion laws, not knowledge extraction. |
| Stage 2 Knowledge Extraction | Atomicity, verification, provenance, deterministic resolution patterns | Reuse object discipline as behaviour discipline. |
| Stage 2 Deduplication / Graph / Canonicalization | Merge, supersession, graph and canonical-consumption patterns | Reuse validation logic; do not create canonical knowledge. |
| LOCKED_KNOWLEDGE Engineering Entity Model | Canonical Engineering Entity vocabulary | Reuse as entity vocabulary; do not redefine entities inside BDP. |
| LOCKED_KNOWLEDGE Engineering Chain Model | Canonical relationship model from Engineering Intent through Intent Closure | Reuse as primary discovery object and chain semantics; do not create a new chain architecture. |
| Function Graph Discovery | Discovery/evidence index for producers, consumers, runtime paths, mutation paths, tests | Use as index only, not truth source. |
| AEP Phase 2 Reality | Behaviour Definition / Behaviour Instance model | Reuse as target reality model and primary identity split. |
| AEP Behaviour Coverage / Behaviour Graph | Behaviour space coverage, progress measurement, and relationship mapping | Reuse as completeness, coverage, and traceability discipline; do not create Behaviour Graph truth source. |
| AEP Behaviour Discovery Rule | Discover / Reuse / Extend / Create-only-if-necessary order | Reuse to prevent duplicate Behaviour Definitions. |
| AOS / Runtime identity discipline | Committed identity, material identity, packet/lease/freshness identity, owner-issued version/lease discipline | Reuse as stability discipline for behaviour evidence; do not create Runtime identity. |
| Canonical Knowledge / Reality First / Evidence Before Consumption | Truth hierarchy, verification boundary, historical/superseded handling | Reuse as behaviour evidence weighting and conflict resolution law. |
| SYSTEM_MAP / Owner Maps | Owner, consumer, producer, implementation and source relationships | Reuse as traceability map; not a Behaviour source by itself. |
| Behaviour Decomposition Review | Granularity review pattern | Reuse atomic/composite validation. |
| Behaviour Reality Validation | Observed/hypothesized/internal-step validation model | Reuse admission statuses. |
| Behaviour Surface Discovery | Observed analytical engineering surface pattern | Reuse as optional discovery and coverage lens only; never as architecture, owner, truth source, storage, entity, Runtime concept, or Planner concept. |
| Certification Pipeline | PASS/HOLD/review gates and evidence recording | Reuse certification structure. |
| OMP / CPS | Consumer chain, state recording, continuation | Reuse existing owner/consumer paths only. |
| Engineering Reports | Evidence and review artifacts | Reuse as output and traceability vehicle. |
| Memory Architecture Discovery | Existing memory families, lifetimes, retention, evidence levels, and owner mappings | Reuse memory ownership and evidence lifecycle; do not create new memory. |
| Knowledge & Memory Transformation Discovery | Existing transformations from observation to evidence, learning, reports, canonical sync, and future decision input | Reuse transformation owner/consumer discipline; do not create a transformation system. |
| Engineering Proof Architecture Discovery | Proof-gated owner/consumer chain discipline | Reuse evidence, verification, traceability, consumer confirmation, terminal state, and chain closure as automation-readiness gates. |
| Production Maturity | Evidence-consuming maturity decisions | Reuse maturity owner path; do not recalculate maturity inside BDP. |
| Current Autonomous Behaviour Reality / Production Evidence | Reality acceptance, implementation, verification, and production enablement signals | Reuse as coverage inputs; do not mutate Reality or production state. |
| Runtime / Decision Model | Runtime identity, packet/lease/freshness, decision lifecycle, execution/STOP_SAFE boundaries | Reuse existing execution constraints; do not create Runtime or Planner authority. |
| Verification / Rollback / Authority / Policies | Existing gates, checks, rollback, containment, STOP_SAFE, authority and policy boundaries | Reuse as automation-readiness criteria; do not expand authority. |
| OMP / Chain Closure / Terminal State | Existing completion and consumer confirmation discipline | Reuse as intent-closure evidence; do not create a new intent owner or completion authority. |
| OMP Implementation / Backlog Discipline | OMP selects implementation work through existing owners and backlog rules | Reuse as consumer path for Implementation Candidates; do not update or fork the official backlog. |
| AOS Codex Role | Codex is temporary engineering assistant, not permanent production dependency | Reuse as Codex readiness boundary; BDP may prepare Codex input but must not make Codex a Runtime or production dependency. |

## 9. Program Invariants

- Reality First.
- Evidence Before Abstraction.
- No Hypothetical Behaviour.
- Implementation evidence outranks architecture expectation.
- Function Graph is an index, not truth.
- Architecture explains Reality; Reality does not adapt to architecture.
- Behaviour is not a function, class, file, or document.
- Behaviour identity is not a name, file path, function, class, document, report title, or repository location.
- Behaviour must be observed as engineering behaviour.
- Behaviour identity must be resolved before Reality admission or merge.
- Behaviour completeness is Behaviour Space coverage, not merely Discovery Pass completion.
- Behaviour traceability must connect identity, evidence, implementation, verification, Reality, and consumer path.
- Discovery must be economical: reuse sufficient existing evidence before running new discovery.
- Behaviour truth follows evidence hierarchy; architecture alone cannot prove observed Behaviour.
- Behaviour evolution must preserve identity, evidence lineage, and Reality lineage.
- Behaviour Surface is an analytical discovery lens only.
- Engineering Chain is the primary BDP discovery object.
- Behaviour is not replaced by Engineering Chain; Behaviour Instance is a mandatory stage inside each Engineering Chain.
- BDP must discover Engineering Chain by Producer -> Consumer relationships, not by file proximity, function adjacency, name similarity, or report wording.
- Engineering Chain semantics are consumed from LOCKED_KNOWLEDGE and must not be redefined by BDP.
- Every discovered Engineering Chain must have Chain State, Chain Walk evidence, Intent Closure status, and terminal state or explicit unknown/blocked reason.
- Behaviour Surface is not an architecture level, owner, truth source, storage system, entity, Runtime concept, Planner concept, or mandatory program layer.
- Automation-Ready Engineering Logic is an analytical BDP result, not a new architecture level, owner, truth source, Runtime, Planner, OMP queue, storage system, or authority grant.
- Automation readiness may classify existing logic only; it must not invent new rules, policies, gates, triggers, execution paths, verification paths, rollback paths, or authority.
- Automation readiness must preserve existing owner, producer, consumer, authority boundary, terminal state, and chain closure.
- Machine-checkable does not mean executable; execution still requires existing owner path, OMP consumption, authority boundary, verification, rollback/containment/STOP_SAFE where applicable, and production safety.
- Implementation Readiness is an analytical BDP result, not a mission, official backlog item, Runtime change, OMP state change, owner grant, Codex assignment, or implementation execution.
- Implementation Candidate may be produced only for existing engineering logic that requires no new architecture, no new Behaviour, no new rule, and no new owner.
- Engineering Automation Backlog is a BDP output catalogue only; the official implementation queue remains OMP / Implementation Backlog.
- Codex Implementation Input is implementation preparation only; Codex must not become a production dependency or permanent Runtime actor.
- Engineering Intent Closure is a BDP analysis result, not a new owner, truth source, goal system, Runtime state, OMP state, production state, or authority grant.
- Intent Closure compares original engineering intent with final state through existing evidence; it must not invent desired behaviour or new goals.
- Automation Break is a discovered stopping point in existing logic, not a certified Autonomous Behaviour Gap and not an OMP mission.
- Intent-derived Implementation Candidates must enter the same Implementation Candidate Catalogue as readiness-derived candidates.
- Engineering Logic Automation Coverage is a BDP measurement result, not a new architecture layer, owner, truth source, backlog, priority system, Runtime state, OMP state, or production state.
- Coverage measures progress of existing engineering logic toward automation and production enablement; it must not measure success by document count, Behaviour count, or report count alone.
- Coverage statuses must preserve existing owner, producer, consumer, verification, rollback, authority, production maturity, and chain closure boundaries.
- No new owner.
- No new truth source.
- No Runtime mutation.
- No OMP bypass.
- No authority expansion.
- No automatic Reality update.

## 10. Discovery Lifecycle

Official lifecycle:

```text
Trigger
  -> Scope Freeze
  -> Existing Discovery Reuse Resolution
  -> Discovery Economy Decision
  -> Discovery Pass Plan
  -> Discovery Pass Execution
  -> Evidence Corpus Assembly
  -> Engineering Chain Discovery
  -> Engineering Chain Walk
  -> Observed Behaviour Candidate Capture
  -> Evidence Validation
  -> Behaviour Truth Hierarchy Resolution
  -> Behaviour Identity Resolution
  -> Behaviour Independence Validation
  -> Optional Behaviour Surface Lens Assignment
  -> Behaviour Merge / Deduplication
  -> Behaviour Completeness Review
  -> Behaviour Traceability Review
  -> Behaviour Evolution Review
  -> Engineering Chain Coverage Review
  -> Automation Readiness Assessment
  -> Implementation Readiness Assessment
  -> Candidate Reality Gate
  -> Implementation Candidate Instance Packaging
  -> Engineering Chain Closure Assessment
  -> Reality Refinement Proposal
  -> Reality Certification
  -> Consumer Assignment
  -> Chain Closure
  -> STOP
```

The lifecycle stops after certification and chain closure. It never automatically updates Current Autonomous Behaviour Reality and never starts Phase 3.

For any scope that produces OMP-facing implementation input, BDP must not stop at Behaviour, Automation Break, Implementation Readiness, or abstract Implementation Candidate.

The terminal OMP-facing BDP package must be:

```text
Implementation Candidate Instance
```

or a legal non-candidate result:

```text
IMPLEMENTATION_BLOCKED_WITH_REASON
IMPLEMENTATION_NOT_APPLICABLE_WITH_REASON
REALITY_INSTANCE_INSUFFICIENT
ENGINEERING_CHAIN_NOT_OBSERVED_WITH_REASON
```

This prevents OMP from receiving abstract improvements, documents, rules, reports, or model references as if they were real engineering situations.

## 11. Discovery Pass Architecture

Each Discovery Pass must prove necessity before execution.

Required fields:

| Field | Meaning |
| --- | --- |
| `Pass ID` | Stable pass identifier. |
| `Purpose` | What behaviour evidence the pass discovers. |
| `Necessity Proof` | Why the pass is required. |
| `Inputs` | Existing sources or evidence surfaces. |
| `Output` | Evidence records or candidate behaviours. |
| `Owner / Source Owner` | Existing owner of the source or evidence. |
| `Forbidden Use` | What the pass cannot conclude. |
| `Consumer` | Later pass or report that consumes it. |
| `Completion Criteria` | Required proof that the pass is complete. |

No pass may exist without necessity proof.

### Behaviour Surface Lens

Behaviour Surface may be used by BDP only as an analytical Discovery Lens.

Surface Lens purpose:

- group Discovery Passes when evidence shows a stable shared engineering surface;
- organize coverage checks across related Behaviour candidates;
- reveal missing Situation / Interpretation / Decision / Verification / Learning evidence inside a known surface;
- help readers navigate BDP outputs.

Surface Lens must not:

- create a new architecture layer;
- create a new Behaviour entity;
- create a new owner;
- create a new truth source;
- create storage;
- create Runtime authority;
- create Planner authority;
- replace Behaviour, Behaviour Instance, Function Graph, Knowledge Graph, OMP, CPS, AEP, AOS, or Current Autonomous Behaviour Reality.

Engineering Chain is the primary discovery object of BDP. Behaviour Instance remains the mandatory behaviour stage inside each Engineering Chain and the minimum behaviour unit validated by BDP. Surface Lens is only a grouping label applied after evidence proves that a group of Behaviours or Engineering Chains shares a common purpose, source family, boundary, Runtime/decision/verification/learning pattern, consumer, or owner.

Surface Lens admission statuses:

| Status | Meaning | Program Rule |
| --- | --- | --- |
| `OBSERVED_ENGINEERING_SURFACE` | Evidence proves a stable shared Behaviour surface. | May be used as optional grouping and coverage lens. |
| `CONCEPTUAL_ONLY` | The grouping is useful conceptually but lacks proven implementation/owner/consumer/verification boundary. | Must not be used as architecture or required discovery structure. |
| `REJECTED` | The candidate is a source, index, architecture document, broad abstraction, or duplicate of an existing system. | Must not be used as Surface Lens. |
| `NOT_APPLICABLE` | The candidate Behaviour does not require a surface grouping. | Valid result; Surface Lens is optional. |

Observed Surface Lens labels currently admitted for BDP navigation and coverage:

- Routing / Decision;
- Runtime / Execution Guard;
- Verification / Truth Closure;
- Rollback / Restore;
- Learning / Outcome;
- Authority / Policy;
- Deployment / Convergence;
- Operator / Admin Visibility;
- Production Certification / Maturity;
- Knowledge / Canonical Sync;
- Engineering / Report.

Conceptual or rejected Surface candidates must not be promoted by BDP. `Experience` may remain conceptual unless future evidence proves a stable independent owner, consumer, verification boundary, and Behaviour set. Broad labels such as General Autonomy, Whole Runtime, Whole Production, or Whole Engineering must not hide independent Behaviours.

Discovery Passes may be grouped by Surface Lens when useful, but pass IDs remain the official execution structure. Surface labels never replace Discovery Pass IDs, evidence records, Behaviour candidates, validation statuses, or consumer chains.

### Engineering Chain Discovery Model

Engineering Chain Discovery is mandatory for every BDP run.

BDP must discover the Engineering Chain first, then validate Behaviour inside that chain.

Canonical chain consumed from LOCKED_KNOWLEDGE:

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

BDP must not replace Behaviour Discovery. It must prove where Behaviour Instance sits inside the Engineering Chain.

For each Engineering Chain, BDP must determine:

- Engineering Intent;
- Trigger;
- Condition;
- Behaviour Instance;
- Decision;
- Execution;
- Verification;
- Outcome;
- Learning;
- Intent Closure.

For each Engineering Chain, BDP must perform:

- Forward Walk;
- Backward Walk;
- Middle-Out Walk;
- Producer -> Consumer Walk.

For each Engineering Chain, BDP must classify:

- Intent;
- Current State;
- Expected Outcome;
- Actual Outcome;
- Chain State;
- Terminal State;
- Intent Closure;
- Automation Break.

If the Engineering Chain is not closed, BDP must evaluate:

- Automation Break;
- Implementation Readiness;
- Implementation Candidate.

Engineering Chain Discovery must not:

- create new Engineering Entity;
- create new owner;
- create new architecture;
- create new Runtime;
- create new Planner;
- create new OMP Mission;
- mutate OMP;
- mutate CPS;
- mutate Current Autonomous Behaviour Reality;
- mutate LOCKED_KNOWLEDGE;
- assign Codex work;
- execute implementation.

Engineering Chain Discovery only discovers, traces, validates, classifies, and packages outputs for existing consumers.

### Required Discovery Passes

| Pass ID | Discovery Pass | Necessity Proof | Primary Outputs |
| --- | --- | --- | --- |
| `BDP-P01` | Repository Surface Discovery | Behaviour evidence may exist in docs, source, tests, tools, reports, evidence directories, and state files. | Source family inventory and change surface. |
| `BDP-P02` | Implementation Discovery | Behaviour Reality is implementation-driven; real producers/consumers often live in code. | Implementation evidence records. |
| `BDP-P03` | Function Graph Discovery | Existing Function Graph indexes producers, consumers, mutation paths, tests, systemd, closures. | Relationship evidence and candidate paths. |
| `BDP-P04` | Runtime / State Discovery | Behaviour may depend on Runtime, read-only views, state snapshots, CPS, deployment state, or live state availability. | Runtime/state evidence or `UNAVAILABLE` records. |
| `BDP-P05` | Decision Discovery | Autonomous Behaviour requires situation interpretation and decision selection. | Decision path evidence. |
| `BDP-P06` | Verification Discovery | Behaviour cannot enter Reality without verification evidence or explicit unknown. | Verification path evidence. |
| `BDP-P07` | Rollback / Restore Discovery | Runtime-affecting or safety behaviour requires rollback/readiness/protection evidence. | Rollback and restore evidence. |
| `BDP-P08` | Learning / Outcome Discovery | Autonomous Behaviour includes learning or continuation where present. | Outcome, feedback, trust, prediction, confidence evidence. |
| `BDP-P09` | Policy / Law Discovery | Behaviour decisions are constrained by existing policies, laws, authority, forbidden actions. | Applicable policy/law evidence. |
| `BDP-P10` | OMP / CPS Discovery | Behaviour chain closure depends on OMP/CPS consumer/state paths. | Owner, consumer, state, continuation evidence. |
| `BDP-P11` | Production / Deployment Discovery | Real behaviour may exist in deployment/convergence/production evidence. | Production and deploy evidence records. |
| `BDP-P12` | Engineering Report Discovery | Engineering reports contain observed execution, certification, no-change, and historical evidence. | Report evidence records. |
| `BDP-P13` | Canonical / Knowledge Boundary Discovery | Canonical knowledge and locked foundations define constraints and contradiction checks. | Boundary and contradiction evidence. |
| `BDP-P14` | Experience / Outcome Discovery | If user/service/channel outcomes exist, they prove behaviour impact and learning. | Outcome and experience evidence. |
| `BDP-P15` | Automation Readiness Discovery | Existing Behaviour may contain machine-checkable logic, gates, rules, checks, policies, verification, rollback, authority, maturity, or continuation rules that are ready or blocked for automatic execution through existing owners. | Automation readiness candidates, blockers, predicates, trigger/execution/verification/rollback coverage. |
| `BDP-P16` | Implementation Readiness Discovery | Existing Behaviour or Automation Candidate may be sufficiently defined to become implementation work through existing OMP and Codex without new architecture, owner, rule, or Behaviour. | Implementation Candidates, implementation blockers, OMP Implementation Input, Codex Implementation Input, Engineering Automation Backlog catalogue. |
| `BDP-P17` | Engineering Intent Closure Discovery | Existing engineering logic may stop before its original intent is achieved. | Intent Closure Matrix, Intent Coverage Matrix, Automation Break Catalogue, Automation Break Matrix, Intent Trace, Forward Trace, Backward Trace. |
| `BDP-P18` | Engineering Logic Coverage Discovery | BDP must measure how much existing engineering logic is discovered, automation-ready, implementation-ready, implemented, verified, production-enabled, blocked, or unknown. | Engineering Logic Coverage Matrix, Automation Progress Matrix, Implementation Progress Matrix, Production Enablement Matrix. |
| `BDP-P19` | Engineering Chain Discovery | LOCKED_KNOWLEDGE requires Engineering Chain as the canonical relationship model between Engineering Entities. BDP must discover the chain containing each Behaviour Instance and implementation candidate. | Engineering Chain Catalogue, Engineering Chain Coverage, Engineering Chain Walk, Engineering Chain Traceability, Engineering Chain Closure Matrix, Engineering Chain Automation Break Matrix, Engineering Chain Implementation Candidates. |

`BDP-P14` is conditional. It runs only when experience/outcome evidence exists or a change claims user/service/channel outcome impact.

`BDP-P15` is required when the BDP scope includes readiness for automation, OMP implementation input, Phase 3 preparation, manual dependency analysis, law execution analysis, trigger coverage, verification automation, rollback automation, or any claim that existing V7 logic may be machine-checkable. If none of those conditions apply, the pass must be marked `NOT_APPLICABLE` with evidence.

`BDP-P16` is required when the BDP scope includes implementation readiness, OMP-ready implementation input, Codex implementation input, engineering automation backlog formation, owner-extension planning, automation implementation, or any claim that existing V7 logic is ready to become implementation work. If none of those conditions apply, the pass must be marked `NOT_APPLICABLE` with evidence.

`BDP-P17` is required when the BDP scope includes intent closure, goal completion, outcome completion, execution completion, chain completion, automation break discovery, or any claim that existing engineering logic reaches or fails to reach its own engineering goal. If none of those conditions apply, the pass must be marked `NOT_APPLICABLE` with evidence.

`BDP-P18` is required when the BDP scope includes automation progress, implementation progress, production enablement, engineering automation coverage, capability coverage, progress coverage, or any claim about how much existing engineering logic has moved from discovery to production. If none of those conditions apply, the pass must be marked `NOT_APPLICABLE` with evidence.

`BDP-P19` is required for every BDP run. If the run scope has no observable Engineering Chain, the pass must produce `ENGINEERING_CHAIN_NOT_OBSERVED_WITH_REASON`, preserve the Behaviour evidence decision, and stop before claiming Chain Closure.

## 12. Evidence Model

Evidence Record schema:

| Field | Required | Meaning |
| --- | --- | --- |
| `Evidence ID` | Yes | Stable ID. |
| `Evidence Type` | Yes | Source code, test, report, runtime observation, production evidence, policy, state, Function Graph, etc. |
| `Source` | Yes | File, path, report, command, or external observation. |
| `Observed Fact` | Yes | What was observed. |
| `Engineering Chain ID` | Required when applicable | Stable chain identifier or `ENGINEERING_CHAIN_NOT_OBSERVED_WITH_REASON`. |
| `Engineering Chain Segment` | Required when applicable | Intent, Trigger, Condition, Behaviour Instance, Decision, Execution, Verification, Outcome, Learning, Intent Closure, or `NOT_APPLICABLE`. |
| `Observed Behaviour Candidate` | Yes | Candidate behaviour supported. |
| `Producer` | Required if known | Existing producer. |
| `Consumer` | Required if known | Existing consumer. |
| `Chain Walk Evidence` | Required when applicable | Forward, Backward, Middle-Out, and Producer -> Consumer walk evidence or explicit blocker. |
| `Chain State` | Required when applicable | `OPEN`, `PARTIALLY_CLOSED`, `CLOSED`, `AUTOMATION_BREAK`, `BLOCKED`, `STOP_SAFE`, `NOT_APPLICABLE`, or `UNKNOWN`. |
| `Terminal State` | Required when applicable | Terminal state or explicit unknown/blocked reason. |
| `Runtime Path` | Required when applicable | Runtime/read-only/execution path or `NOT_APPLICABLE`. |
| `Decision Path` | Required when applicable | Decision path or `NOT_OBSERVED`. |
| `Verification Path` | Required | Verification path or explicit `UNKNOWN` / `NOT_OBSERVED`. |
| `Learning Path` | Required | Learning path or explicit `UNKNOWN` / `NOT_OBSERVED`. |
| `Automation Readiness Evidence` | Required when applicable | Existing condition/gate/rule/policy/check evidence or `NOT_APPLICABLE`. |
| `Machine-checkable Predicate` | Required when applicable | Predicate and input data, or `NOT_OBSERVED` / `NOT_APPLICABLE`. |
| `Trigger Evidence` | Required when applicable | Existing trigger, possible existing-owner trigger, missing trigger, or `NOT_APPLICABLE`. |
| `Execution / No-Execution Path` | Required when applicable | Existing execution path, explicit no-execution path, or blocker. |
| `Rollback / Containment / STOP_SAFE Path` | Required when applicable | Safety path or `NOT_APPLICABLE` with reason. |
| `Automation Blocking Reason` | Required when blocked | Blocking reason from Automation Readiness Classification. |
| `Implementation Readiness Evidence` | Required when applicable | Evidence that the logic can or cannot become implementation work. |
| `Implementation Scope` | Required when applicable | Existing owner/file/module/document scope or blocker. |
| `Implementation Dependencies` | Required when applicable | Existing dependencies, missing dependencies, or `NOT_APPLICABLE`. |
| `Codex Readiness` | Required when applicable | Whether Codex can implement through existing owners without architecture/runtime/authority change. |
| `Implementation Blocking Reason` | Required when blocked | Exact implementation blocker. |
| `Coverage State` | Required when applicable | Current coverage state for the supported logic or Behaviour. |
| `Coverage Domain` | Required when applicable | Behaviour, Automation, Implementation, Production, or cross-domain coverage area. |
| `Coverage Blocking Reason` | Required when blocked | Exact blocker preventing next coverage state. |
| `Initial Intent` | Required when applicable | Original engineering goal of the Behaviour, rule, gate, policy, path, or condition. |
| `Final State` | Required when applicable | Observed or resolved terminal state reached by the logic. |
| `Intent Closure Status` | Required when applicable | `INTENT_CLOSED`, `AUTOMATION_BREAK`, or explicit `INTENT_NOT_APPLICABLE`. |
| `Automation Break Reason` | Required when break exists | Exact reason why the original intent is not achieved. |
| `Surface Lens` | Optional | Analytical grouping label: `OBSERVED_ENGINEERING_SURFACE` or `NOT_APPLICABLE`; never a source of truth. |
| `Truth Level` | Yes | Behaviour truth hierarchy level for this evidence. |
| `Traceability Path` | Yes | Deterministic path from evidence to candidate, owner/source, and consumer, or explicit `INCOMPLETE`. |
| `Confidence` | Yes | `HIGH`, `MEDIUM_HIGH`, `MEDIUM`, `MEDIUM_LOW`, `LOW`. |
| `Freshness` | Yes | Current, stale, historical, unavailable, ambiguous. |
| `Forbidden Use` | Yes | What cannot be inferred from this evidence. |

Evidence cannot be promoted to Behaviour Reality unless validation passes.

## 13. Observed Behaviour Candidate Model

Observed Behaviour Candidate schema:

| Field | Required |
| --- | --- |
| `Candidate ID` | Yes |
| `Engineering Chain ID` | Yes or `ENGINEERING_CHAIN_NOT_OBSERVED_WITH_REASON` |
| `Engineering Chain State` | Yes or `UNKNOWN` |
| `Forward Walk` | Yes or `INCOMPLETE` |
| `Backward Walk` | Yes or `INCOMPLETE` |
| `Middle-Out Walk` | Yes or `INCOMPLETE` |
| `Producer -> Consumer Walk` | Yes or `INCOMPLETE` |
| `Situation` | Yes |
| `Context` | Yes |
| `Interpretation` | Yes |
| `Applicable Knowledge` | Yes or `UNKNOWN` |
| `Applicable Laws` | Yes or `UNKNOWN` |
| `Possible Decisions` | Yes or `UNKNOWN` |
| `Decision Selection` | Yes or `UNKNOWN` |
| `Execution / Producer Path` | Yes or `NOT_OBSERVED` |
| `Verification` | Yes or `NOT_OBSERVED` |
| `Learning / Continuation` | Yes or `NOT_OBSERVED` |
| `Automation-Ready Engineering Logic` | Yes or `NOT_APPLICABLE` |
| `Automation Readiness Status` | Yes or `NOT_APPLICABLE` |
| `Machine-checkable Predicate` | Yes or `NOT_APPLICABLE` |
| `Trigger` | Yes, `MISSING`, or `NOT_APPLICABLE` |
| `Execution Path` | Yes, `NO_EXECUTION_PATH`, or `NOT_APPLICABLE` |
| `Authority Boundary` | Yes or `UNKNOWN` |
| `Rollback / Containment / STOP_SAFE` | Yes or `NOT_APPLICABLE` |
| `OMP Consumer Path` | Yes or `NOT_APPLICABLE` |
| `Implementation Readiness` | Yes or `IMPLEMENTATION_NOT_APPLICABLE` |
| `Implementation Candidate` | Yes or `IMPLEMENTATION_NOT_APPLICABLE` |
| `Implementation Scope` | Yes or `NOT_APPLICABLE` |
| `Codex Readiness` | Yes or `NOT_APPLICABLE` |
| `Coverage State` | Yes or `NOT_APPLICABLE` |
| `Coverage Domain` | Yes or `NOT_APPLICABLE` |
| `Coverage Blocking Reason` | Required when blocked |
| `Initial Intent` | Yes or `NOT_APPLICABLE` |
| `Final State` | Yes or `NOT_APPLICABLE` |
| `Intent Closure Status` | Yes or `INTENT_NOT_APPLICABLE` |
| `Automation Break Reason` | Required when break exists |
| `Evidence Records` | Yes |
| `Producer` | Yes or `UNKNOWN` |
| `Consumer` | Yes or `UNKNOWN` |
| `Behaviour Definition Identity` | Yes or `PENDING_IDENTITY_RESOLUTION` |
| `Behaviour Instance Identity` | Yes or `PENDING_IDENTITY_RESOLUTION` |
| `Identity Disposition` | Yes or `PENDING_IDENTITY_RESOLUTION` |
| `Completeness Role` | Yes or `UNKNOWN` |
| `Traceability Path` | Yes or `INCOMPLETE` |
| `Truth Level` | Yes |
| `Evolution Disposition` | Yes or `NOT_APPLICABLE` |
| `Surface Lens` | Optional |
| `Confidence` | Yes |
| `Admission Status` | Yes |

Admission statuses:

| Status | Meaning |
| --- | --- |
| `OBSERVED_INDEPENDENT` | May be considered for Reality Refinement. |
| `OBSERVED_INTERNAL_STEP` | Real but not standalone Behaviour. |
| `OBSERVED_COMPOSITE_NOT_ADMISSIBLE` | Real but must be split before Reality admission. |
| `HYPOTHESIZED` | Must not enter Reality. |
| `REJECTED_NO_EVIDENCE` | No engineering evidence. |
| `REJECTED_ARCHITECTURE_ONLY` | Only architecture or expectation supports it. |

## 14. Behaviour Identity Model

Behaviour Identity Model defines how BDP determines whether an observed Behaviour Candidate is:

- a new Behaviour Definition;
- an existing Behaviour Definition with new evidence;
- an existing Behaviour Definition with new implementation;
- an existing Behaviour Definition with a new name;
- a new version of an existing Behaviour Definition;
- a different Behaviour that shares a name;
- ambiguous and requiring manual review.

Behaviour Identity Model creates no owner, no truth source, no storage, no Runtime identity, no Planner identity, and no architecture layer. It is a deterministic resolution model inside BDP.

The model reuses:

- AEP `Behaviour Definition -> Behaviour Instance`;
- AEP Behaviour Discovery Rule;
- Current Autonomous Behaviour Reality Behaviour Definition Catalogue;
- Function Graph as discovery index only;
- Canonical Knowledge, SYSTEM_MAP, Decision Model, Runtime Model, OMP, and CPS as official owner/source/context references;
- AOS / Runtime committed identity discipline as evidence-stability discipline, not as a new Runtime identity.

Behaviour identity is resolved at two levels.

### Behaviour Definition Identity

Behaviour Definition Identity is the stable engineering identity of the behaviour type across time.

It is defined by the deterministic identity signature:

| Identity Factor | Required | Identity Role |
| --- | --- | --- |
| `Engineering Purpose` | Yes | The durable outcome the behaviour exists to produce. |
| `Situation Class` | Yes | The class of situation the behaviour interprets. |
| `Decision Responsibility` | Yes | The decision or decision-bound responsibility the behaviour owns or supports. |
| `Execution Responsibility` | Yes or `NOT_EXECUTING` | The producer/execution responsibility, not a file/function path. |
| `Primary Consumer` | Yes | The owner/system/report/reality path that consumes the behaviour output. |
| `Verification Obligation` | Yes | The proof required before the behaviour output may be consumed. |
| `Learning / Continuation Obligation` | Yes or `NOT_APPLICABLE` | The required feedback, learning, OMP, CPS, report, or no-change continuation. |
| `Authority / Boundary / Forbidden Use` | Yes | What the behaviour is forbidden to do or infer. |
| `Canonical Owner / Owner Role` | Yes or `UNKNOWN_WITH_EVIDENCE` | Existing owner or owner role that confirms the behaviour boundary. |
| `Evidence Provenance Family` | Yes | Source family proving the identity signature. |

Names, titles, file paths, function names, class names, report names, and repository locations are supporting labels only. They are not identity factors.

### Behaviour Instance Identity

Behaviour Instance Identity is the identity of a concrete occurrence of a Behaviour Definition in a specific current reality.

It is defined by:

- Behaviour Definition Identity;
- concrete situation;
- concrete context;
- evidence occurrence or report/run/source envelope;
- concrete producer/consumer path when known;
- terminal state, freshness, or explicit unknown;
- verification and learning/continuation evidence for that occurrence.

A new Behaviour Instance does not create a new Behaviour Definition by default.

### Identity Resolution Lifecycle

Official identity resolution lifecycle:

```text
Observed Behaviour Candidate
  -> Resolve Existing Behaviour Definitions
  -> Build Candidate Identity Signature
  -> Compare With Existing Identity Signatures
  -> Resolve Definition Identity
  -> Resolve Instance Identity
  -> Assign Identity Disposition
  -> Identity Validation
  -> Continue To Behaviour Independence Validation
```

Resolution must follow:

```text
Discover
  -> Reuse
  -> Extend
  -> Implement
```

In BDP, `Implement` means materialize the identity resolution in BDP outputs such as the candidate registry, identity resolution matrix, validation matrix, and refinement proposal. It does not mean code implementation, Runtime mutation, owner creation, or architecture change.

BDP may not create a new Behaviour Definition until it proves that no existing Behaviour Definition, Behaviour Instance, owner, source, evidence path, Function Graph relationship, Knowledge Graph relationship, OMP mission pattern, Runtime rule, Decision Model rule, or canonical knowledge entry covers the candidate identity signature.

### Identity Dispositions

| Disposition | Meaning | Rule |
| --- | --- | --- |
| `EXISTING_BEHAVIOUR_NEW_EVIDENCE` | Identity signature matches an existing Behaviour Definition; evidence is new or fresher. | Reuse existing Definition; attach evidence. |
| `EXISTING_BEHAVIOUR_NEW_IMPLEMENTATION` | Identity signature matches; implementation/producer path changed without changing purpose, situation class, decision responsibility, consumer, verification, learning, or forbidden boundary. | Reuse existing Definition; record implementation change as evidence. |
| `EXISTING_BEHAVIOUR_RENAMED` | Identity signature matches; only label/name changed. | Reuse existing Definition; record alias/name lineage. |
| `BEHAVIOUR_VERSION_UPDATE` | Identity signature keeps lineage but materially changes a defining factor such as situation class, decision responsibility, consumer, verification obligation, learning obligation, authority boundary, or forbidden use. | Extend existing Definition through version lineage; do not create unrelated duplicate. |
| `NEW_BEHAVIOUR_DEFINITION` | No existing Definition or official source path covers the identity signature. | May enter Reality Refinement only after validation and consumer assignment. |
| `DIFFERENT_BEHAVIOUR_NAME_COLLISION` | Name matches but identity signature differs. | Must not merge by name. |
| `DUPLICATE_BEHAVIOUR_REJECTED` | Candidate duplicates an existing identity without new evidence, implementation, name, or version value. | Reject as duplicate. |
| `MANUAL_REVIEW_IDENTITY_AMBIGUOUS` | Identity cannot be resolved deterministically from official sources. | Hold from Reality admission and merge. |

### Identity Stability Rules

- Same name is neither sufficient nor required for same Behaviour.
- Same file/function/class/document is neither sufficient nor required for same Behaviour.
- Different name does not create a new Behaviour when the identity signature is stable.
- Different implementation does not create a new Behaviour when the identity signature is stable.
- Different evidence does not create a new Behaviour when it only proves or refreshes the same identity signature.
- Different consumer, decision responsibility, verification obligation, learning obligation, authority boundary, forbidden use, or situation class may require a version update or a new Behaviour Definition.
- Identity comparison must be deterministic and reproducible from recorded fields.
- If more than one identity resolution is possible, disposition must be `MANUAL_REVIEW_IDENTITY_AMBIGUOUS`.

## 15. Behaviour Completeness Model

Behaviour Completeness Model determines whether the Behaviour Space for the current BDP scope has been covered enough to produce a certified Reality Refinement Proposal.

Completeness is not Discovery Saturation.

- Discovery Saturation answers: did the approved Discovery Passes finish?
- Behaviour Completeness answers: does the discovered Behaviour Space have enough coverage to support the program decision?

BDP reuses AEP Behaviour Catalogue, Behaviour Coverage, Behaviour Graph, Current Autonomous Behaviour Reality, Surface Lens grouping, Function Graph index, SYSTEM_MAP, Canonical Knowledge, and BDP identity resolution as completeness inputs.

Completeness dimensions:

| Dimension | Required Question |
| --- | --- |
| `Scope Coverage` | Are all behaviours inside the run scope accounted for as observed, rejected, unavailable, unknown, or not applicable? |
| `Behaviour Definition Coverage` | Does every candidate resolve to an existing/new/versioned/ambiguous Behaviour Definition disposition? |
| `Behaviour Instance Coverage` | Are concrete instances linked to Definitions or explicitly marked unavailable/unknown/not applicable? |
| `Surface / Domain Coverage` | If Surface Lens or source/domain families are used, are all relevant surfaces/families covered or dispositioned? |
| `Situation Coverage` | Are known situation classes represented or explicitly not applicable? |
| `Decision / Execution Coverage` | Are decision, execution, producer, and non-execution paths resolved or marked unknown/not observed? |
| `Verification / Learning Coverage` | Are verification and learning/continuation paths resolved or explicitly unknown/not applicable? |
| `Owner / Consumer Coverage` | Are owners and consumers resolved or marked unknown with evidence? |
| `Truth Coverage` | Does each accepted Behaviour rely on the strongest available truth level for the run scope? |
| `Traceability Coverage` | Can every accepted Behaviour be traced from identity to evidence, implementation/source, verification, Reality output, and consumer? |
| `Unknown Coverage` | Are unknown, unavailable, stale, historical, and not-applicable areas explicit rather than hidden? |

Completeness statuses:

| Status | Meaning | Program Rule |
| --- | --- | --- |
| `COMPLETE_FOR_SCOPE` | Behaviour Space is sufficiently covered for the declared scope. | May proceed to Reality Refinement Proposal. |
| `COMPLETE_WITH_EXPLICIT_UNKNOWNS` | Coverage is sufficient, and all gaps are explicit `UNKNOWN`, `UNAVAILABLE`, `HISTORICAL`, or `NOT_APPLICABLE`. | May proceed with recorded risks. |
| `PARTIAL_HOLD` | A required Behaviour Space area lacks coverage or disposition. | Must not certify Reality Refinement. |
| `INCOMPLETE_FAIL` | Completeness claims hide missing Behaviour Space, unknowns, or contradictions. | Fail BDP run. |

Completeness never means all possible future behaviours are known. It means the declared scope has no hidden Behaviour Space.

## 16. Behaviour Traceability Model

Behaviour Traceability Model preserves the full engineering life of a Behaviour without creating a new memory system.

Required traceability chain:

```text
Behaviour Definition Identity
  -> Behaviour Identity Signature
  -> Behaviour Instance Identity
  -> Evidence Records
  -> Source / Owner / Producer
  -> Implementation / Function Graph Index / SYSTEM_MAP Reference
  -> Tests / Verification Evidence
  -> Runtime / State / Report Evidence where applicable
  -> Current Autonomous Behaviour Reality candidate
  -> Reality Refinement Proposal
  -> Consumer / OMP / CPS path
  -> Experience / Outcome where applicable
  -> Canonical Knowledge / Knowledge Evolution path where applicable
```

Traceability statuses:

| Status | Meaning |
| --- | --- |
| `TRACE_COMPLETE` | Required chain segments are present or explicitly not applicable. |
| `TRACE_COMPLETE_WITH_UNKNOWNS` | Chain is usable, but some segments are explicit `UNKNOWN` or `UNAVAILABLE`. |
| `TRACE_PARTIAL_HOLD` | Required chain segment is missing and not dispositioned. |
| `TRACE_FAIL` | Chain contains contradiction, orphan output, unsupported source, or hidden inference. |

Traceability rules:

- Every accepted Behaviour Candidate must have a traceability path.
- Missing implementation, Runtime, test, experience, or canonical-knowledge segment must be explicit `NOT_APPLICABLE`, `NOT_OBSERVED`, `UNKNOWN`, `UNAVAILABLE`, `HISTORICAL`, or `SUPERSEDED`.
- Function Graph and SYSTEM_MAP may help trace relationships, but they do not prove Behaviour truth by themselves.
- Reports may preserve traceability, but report narrative alone cannot replace source/evidence identity.
- No orphan Behaviour, evidence record, Reality proposal item, or engineering report output is allowed.

## 17. Behaviour Discovery Economy Model

Behaviour Discovery Economy Model determines whether new Discovery is necessary.

BDP must reuse sufficient existing evidence before running new Discovery.

Discovery economy outcomes:

| Outcome | Meaning | Rule |
| --- | --- | --- |
| `DISCOVERY_NOT_REQUIRED_REUSE_EVIDENCE` | Existing evidence is current, traceable, sufficiently strong, identity-stable, and scope-compatible. | Use existing evidence and record reuse proof. |
| `TARGETED_DISCOVERY_REQUIRED` | Only specific missing, stale, ambiguous, or changed areas require discovery. | Run only necessary Discovery Passes. |
| `FULL_DISCOVERY_REQUIRED` | Scope, evidence, implementation, Reality, or identity changed enough that targeted discovery cannot prove completeness. | Run full BDP Discovery Pass plan for scope. |
| `DISCOVERY_HOLD` | Discovery need cannot be determined because inputs or authority are missing. | Stop until operator/owner clarifies. |

Existing evidence is sufficient only when all conditions hold:

- scope is unchanged or narrower than the evidence scope;
- evidence truth level is strong enough for the decision;
- evidence is current enough for its declared use;
- identity signature is stable;
- traceability path is complete or complete with explicit unknowns;
- no contradiction exists between implementation, Runtime/state, reports, canonical knowledge, or owner maps;
- consumer does not require fresher proof;
- no project change claims Behaviour change.

New Discovery is required when any condition holds:

- project change may alter Behaviour identity, situation, decision, execution, verification, learning, owner, consumer, or forbidden use;
- evidence is stale, historical, superseded, unavailable, or ambiguous for the intended decision;
- existing evidence lacks traceability or owner/source provenance;
- identity disposition is `PENDING_IDENTITY_RESOLUTION` or `MANUAL_REVIEW_IDENTITY_AMBIGUOUS`;
- implementation, Function Graph relationship, Runtime/state evidence, Decision Model rule, or canonical boundary changed;
- Reality Refinement or Phase 3 readiness requires fresher Behaviour proof;
- consumer rejects existing evidence as insufficient.

Discovery economy must reduce unnecessary scanning, not weaken Reality First.

## 18. Behaviour Truth Hierarchy

Behaviour Truth Hierarchy defines the official weight of Behaviour evidence.

Truth levels:

| Level | Evidence Type | Rule |
| --- | --- | --- |
| `T1_OBSERVED_PRODUCTION_VERIFIED` | Current observed production outcome or production certification with owner provenance and verification. | Strongest Behaviour truth. |
| `T2_OBSERVED_RUNTIME_VERIFIED` | Current Runtime/state/read-only diagnostic evidence with freshness, owner provenance, and verification. | Strong current Behaviour truth when production observation is not required. |
| `T3_OBSERVED_BEHAVIOUR_VERIFIED` | Reproducible observed Behaviour from tools/tests/execution reports with verification evidence. | Strong for repository/current engineering reality. |
| `T4_IMPLEMENTATION_CURRENT` | Current implementation/source plus owner/source mapping and supporting Function Graph/SYSTEM_MAP relationships. | Proves implementation existence, not Behaviour truth alone unless supported by validation. |
| `T5_TESTS_CURRENT` | Current tests demonstrating expected behaviour. | Supports Behaviour proof but cannot outrank contradictory observed Runtime/production evidence. |
| `T6_ACCEPTED_ENGINEERING_REPORT` | Current accepted engineering/certification report with traceable evidence. | Supports Behaviour proof when evidence pointers are valid. |
| `T7_CANONICAL_BOUNDARY` | Canonical Knowledge, AEP, AOS, Decision Model, Runtime Model, SYSTEM_MAP, OMP, CPS. | Defines laws, owners, boundaries, consumers, and forbidden actions; does not by itself prove observed Behaviour execution. |
| `T8_HISTORICAL_OR_SUPERSEDED` | Historical reports, superseded plans, stale evidence, old snapshots. | Historical only unless explicitly accepted for context. |
| `T9_HYPOTHESIS_OR_ARCHITECTURE_ONLY` | Desired behaviour, architecture-only expectation, synthetic example, unsupported narrative. | Cannot prove Behaviour and must not enter Reality. |

Conflict rules:

- Reality First wins: verified observed production/runtime evidence outranks implementation, tests, reports, and architecture expectation.
- Current implementation outranks stale reports when the question is implementation existence.
- Verified evidence outranks unverified report narrative.
- Canonical boundaries can forbid a Behaviour claim even when lower-level evidence appears to support it.
- Historical or superseded evidence must not be promoted as current truth.
- If highest available truth is insufficient for the consumer decision, Discovery Economy must require targeted or full discovery.

## 19. Behaviour Evolution Support

Behaviour Evolution Support defines how BDP accompanies Behaviour changes over time without creating a separate Behaviour Change Model.

It reuses:

- Behaviour Identity Model;
- Identity Dispositions;
- Behaviour Traceability Model;
- Behaviour Completeness Model;
- Reality Refinement Proposal;
- Chain Closure;
- OMP / CPS consumer paths;
- Knowledge Evolution path when canonical knowledge is affected.

Evolution dispositions:

| Disposition | Meaning | Rule |
| --- | --- | --- |
| `EVOLUTION_NONE` | Candidate confirms existing Behaviour without material change. | Attach evidence and preserve identity. |
| `EVOLUTION_EVIDENCE_REFRESH` | Same Behaviour, fresher/stronger evidence. | Update evidence lineage in proposal. |
| `EVOLUTION_IMPLEMENTATION_CHANGED` | Same Behaviour identity, implementation/source path changed. | Preserve Definition identity; record implementation lineage. |
| `EVOLUTION_RENAMED` | Same Behaviour identity, label changed. | Preserve identity; record alias/name lineage. |
| `EVOLUTION_VERSIONED` | Same lineage but material identity factor changed. | Create version lineage through Reality Refinement Proposal; do not duplicate. |
| `EVOLUTION_SUPERSEDED` | Older Behaviour evidence or definition is no longer current truth. | Preserve as historical/superseded; do not treat as active Reality. |
| `EVOLUTION_CONTRADICTION` | Evidence conflicts with current Reality or locked/canonical boundary. | Route to existing owner, Knowledge Evolution, OMP, or manual review path. |
| `EVOLUTION_MANUAL_REVIEW` | Evolution cannot be determined deterministically. | Hold from automatic Reality admission. |

Evolution rules:

- Behaviour evolution must preserve identity lineage, evidence lineage, owner/consumer lineage, and Reality lineage.
- BDP may propose Reality refinement but must not update Current Autonomous Behaviour Reality automatically.
- BDP must not create a new owner, Runtime, OMP, Planner, truth source, memory system, or storage system to support evolution.
- Superseded Behaviour remains historical evidence, not active Reality.
- Behaviour evolution that affects canonical knowledge routes to existing Knowledge Evolution; BDP does not rewrite locked knowledge.

## 20. Automation Readiness Model

Automation-Ready Engineering Logic is an analytical BDP result.

It is not:

- a new architecture;
- a new owner;
- a new Runtime;
- a new Planner;
- a new truth source;
- a new storage layer;
- a new OMP queue;
- an authority grant;
- an automatic execution permission.

Automation-Ready Engineering Logic is an existing V7 engineering condition, law, gate, policy, check, verification, rollback, authority rule, maturity rule, or continuation rule that can be evaluated for automatic execution readiness.

Automation-Ready Engineering Logic must satisfy all of the following before it can be classified as `AUTOMATION_READY`:

1. it already exists in V7;
2. it has an existing owner;
3. it has an existing producer;
4. it has an existing consumer;
5. it is machine-checkable;
6. it has input data;
7. it has a trigger or can receive an existing-owner trigger;
8. it has a deterministic decision rule;
9. it has an execution path or explicit no-execution path;
10. it has a verification path;
11. it has rollback, containment, or `STOP_SAFE` path where applicable;
12. it has terminal state;
13. it has chain closure;
14. it does not require manual operator decision for each occurrence;
15. it does not expand authority outside an existing owner path.

Automation readiness classification:

| Status | Meaning |
| --- | --- |
| `AUTOMATION_READY` | All required readiness criteria are satisfied and existing owner paths support automatic execution under existing authority. |
| `AUTOMATION_READY_WITH_LIMITS` | Machine-checkable and executable only within bounded existing limits such as read-only, canary, explicit authority envelope, limited trigger, or restricted scope. |
| `MACHINE_CHECKABLE_ONLY` | Predicate can be evaluated automatically, but execution path, authority, trigger, verification, rollback, or consumer closure is not complete. |
| `OBSERVATION_ONLY` | Existing logic can observe or classify but cannot decide or execute. |
| `MANUAL_GATE_ONLY` | Existing logic requires operator/manual decision for each occurrence. |
| `BLOCKED_BY_AUTHORITY` | Existing authority boundary does not permit automatic execution. |
| `BLOCKED_BY_MISSING_TRIGGER` | Predicate or logic exists, but no existing trigger is available or defined. |
| `BLOCKED_BY_MISSING_EXECUTION_PATH` | Logic exists, but no legal execution or explicit no-execution path exists. |
| `BLOCKED_BY_MISSING_VERIFICATION` | Logic exists, but verification path is absent or insufficient. |
| `BLOCKED_BY_MISSING_ROLLBACK` | Runtime-affecting or safety logic lacks rollback, containment, or `STOP_SAFE` path. |
| `BLOCKED_BY_MISSING_CONSUMER` | Output has no certified consumer or OMP/CPS/owner path. |
| `BLOCKED_BY_INSUFFICIENT_EVIDENCE` | Evidence is stale, incomplete, ambiguous, synthetic, or below required truth level. |
| `NOT_AUTOMATABLE` | The logic is intentionally manual, conceptual, non-deterministic, authority-bound, unsafe, or lacks existing-owner path. |

Automation Readiness Record schema:

| Field | Required | Meaning |
| --- | ---: | --- |
| `Existing Condition` | Yes | Existing condition, law, gate, policy, check, verification, rollback, authority, maturity, or continuation rule. |
| `Source` | Yes | Source file, report, canonical reference, runtime evidence, policy, test, Function Graph index, or owner artifact. |
| `Owner` | Yes | Existing owner of the condition or rule. |
| `Producer` | Yes | Existing producer of the input or result. |
| `Consumer` | Yes | Existing consumer or terminal alternative. |
| `Trigger` | Yes | Existing trigger, possible existing-owner trigger, missing trigger, or `NOT_APPLICABLE`. |
| `Input Data` | Yes | Required input data and freshness requirement. |
| `Machine-checkable Predicate` | Yes | Deterministic predicate or reason it is not machine-checkable. |
| `Decision Rule` | Yes | Deterministic rule, no-action rule, hold rule, or manual gate. |
| `Execution Path` | Yes | Existing execution path, explicit no-execution path, or blocker. |
| `Authority Boundary` | Yes | Existing authority envelope and forbidden authority expansion. |
| `Verification Path` | Yes | Existing verification path or blocker. |
| `Rollback / Containment / STOP_SAFE` | Yes | Existing safety path, not applicable reason, or blocker. |
| `Terminal State` | Yes | Terminal result or allowed terminal alternative. |
| `Chain Closure` | Yes | Producer/consumer closure status and evidence. |
| `Runtime Impact` | Yes | `NONE`, `READ_ONLY`, `GUARDED`, `RUNTIME_AFFECTING`, or `UNKNOWN`. |
| `Production Impact` | Yes | `NONE`, `OBSERVATION`, `ADVISORY`, `PRODUCTION_AFFECTING`, or `UNKNOWN`. |
| `User Impact` | Yes | `NONE`, `INDIRECT`, `DIRECT`, or `UNKNOWN`. |
| `Automation Readiness Status` | Yes | One official status from the classification table. |
| `Blocking Reason` | Required when blocked | Exact missing/unsafe element. |
| `Required Existing Owner Extension` | Required when not ready | Existing owner extension needed, or `NOT_APPLICABLE`. |
| `OMP Consumer Path` | Yes | OMP path, terminal no-OMP reason, or `NOT_APPLICABLE`. |

Relationship with Behaviour:

- BDP continues to discover Behaviour first.
- For every accepted or held Behaviour Candidate, BDP must determine whether it contains Automation-Ready Engineering Logic or record `NOT_APPLICABLE`.
- BDP must classify which part of the Behaviour is automated, observed-only, machine-checkable-only, manual-gated, authority-blocked, trigger-blocked, execution-blocked, verification-blocked, rollback-blocked, consumer-blocked, evidence-blocked, or not automatable.
- BDP must not split a Behaviour solely because it contains multiple automation conditions unless those conditions represent independent Behaviours under the Behaviour Independence and Identity rules.

Relationship with OMP:

- BDP may produce `Automation Readiness Candidate`, `Automation Readiness Matrix`, `Automation Refinement Proposal`, and `OMP-ready implementation input`.
- BDP does not create OMP missions automatically.
- OMP remains the only execution operating system and the only route for implementation consumption.

Relationship with Phase 3:

Phase 3 should consume certified BDP automation findings as evidence for Automation Gaps.

Automation Gap types:

| Gap Type | Meaning |
| --- | --- |
| `Automation Gap` | Existing engineering logic is sufficiently defined but not automatically executed through existing owner path. |
| `Law Execution Gap` | Existing law or condition is machine-checkable but not automatically executed. |
| `Manual Dependency Gap` | Existing logic requires manual action for each occurrence. |
| `Trigger Gap` | Existing logic lacks a trigger. |
| `Execution Path Gap` | Existing logic lacks legal execution or no-execution path. |
| `Verification Automation Gap` | Existing logic lacks automatic verification path. |
| `Rollback Automation Gap` | Existing logic lacks rollback, containment, or `STOP_SAFE` path. |
| `Authority Automation Gap` | Existing logic is blocked by authority boundary or approval model. |
| `Consumer Automation Gap` | Existing logic lacks certified consumer or chain closure. |

BDP may identify these gaps as candidates only. BDP must not execute Phase 3 or create certified Autonomous Behaviour Gaps.

## 21. Implementation Readiness Model

Implementation Readiness is an analytical BDP result.

It answers:

```text
What is sufficiently defined to become real implementation work through existing OMP and Codex?
```

It is not:

- a new architecture;
- a new Behaviour;
- a new owner;
- a new OMP mission;
- a new OMP queue;
- an update to the official Implementation Backlog;
- a Runtime change;
- a Planner change;
- an authority grant;
- a Codex assignment;
- implementation execution.

Implementation Readiness applies to:

- Behaviour;
- Automation Candidate;
- rule;
- gate;
- condition;
- policy;
- verification;
- rollback;
- authority rule;
- maturity rule;
- continuation rule;
- existing-owner extension candidate.

Implementation readiness statuses:

| Status | Meaning |
| --- | --- |
| `IMPLEMENTATION_READY` | Existing engineering logic is fully defined, requires no new architecture, no new owner, no new Behaviour, no new rule, and only needs implementation through existing OMP/Codex owner path. |
| `IMPLEMENTATION_BLOCKED` | Existing logic is not ready for implementation because one or more required implementation inputs are missing or unsafe. |
| `IMPLEMENTATION_NOT_APPLICABLE` | The Behaviour or evidence item is already complete, intentionally non-implementable, historical, evidence-only, read-only with no implementation need, or outside the declared scope. |

Implementation blockers:

| Blocker | Meaning |
| --- | --- |
| `MISSING_TRIGGER` | No trigger or existing-owner trigger is defined. |
| `MISSING_EXECUTION_PATH` | No legal implementation or execution path is defined. |
| `MISSING_VERIFICATION` | Verification path is absent or insufficient. |
| `MISSING_ROLLBACK` | Rollback, containment, or `STOP_SAFE` path is absent where required. |
| `MISSING_RUNTIME_SUPPORT` | Required Runtime support does not exist through existing Runtime owners. |
| `MISSING_AUTHORITY` | Existing authority does not permit the implementation or action class. |
| `MISSING_CONSUMER` | No OMP, owner, CPS, Production Maturity, or terminal consumer path exists. |
| `MISSING_EXISTING_OWNER_EXTENSION` | Existing owner can express the work, but the required owner extension is not yet defined. |
| `MISSING_EVIDENCE` | Evidence is stale, unavailable, ambiguous, synthetic, or below required truth level. |
| `MISSING_SCOPE` | Implementation scope cannot be bounded to existing owner/file/module/document surfaces. |
| `MISSING_DEPENDENCY` | Required existing dependency is absent, unknown, or unresolved. |
| `ARCHITECTURE_REQUIRED` | The candidate would require new architecture and therefore cannot be emitted as implementation-ready by BDP. |
| `NEW_OWNER_REQUIRED` | The candidate cannot be expressed by existing owners and therefore cannot be emitted as implementation-ready by BDP. |

### Final OMP Output Contract

Status: `CANONICAL`

BDP final OMP-facing output is:

```text
Implementation Candidate Instance
```

This is not a new entity. It reuses the existing Engineering Entity Model and OMP Implementation Candidate Instance semantics.

BDP may use the phrase `Engineering Reality Instance` only as an explanatory description of the same output shape:

```text
Implementation Candidate Instance
  = a concrete engineering situation in current Reality
  = anchored in Engineering Chain + Behaviour Instance + Intent Closure
  = admissible by OMP
```

The final BDP output must not be:

- idea;
- improvement;
- document;
- rule;
- validation;
- refactoring;
- owner;
- model;
- report;
- source;
- Discovery Index;
- context artifact;
- abstract Behaviour Definition;
- Automation Break by itself.

Context artifacts may support evidence, owner lookup, or provenance. They must not become the counted Candidate Instance.

### Implementation Candidate Instance Schema

Implementation Candidate Instance schema:

| Field | Required | Meaning |
| --- | ---: | --- |
| `Candidate Instance ID` | Yes | Stable identity for one concrete engineering situation. |
| `Primary Class` | Yes | One official Implementation Candidate Class from the BDP classification model. |
| `Secondary Classes` | Yes | Zero or more supporting classes, or `NONE`. Secondary classes never replace the Primary Class. |
| `Execution Depth` | Yes | Execution Certification depth target or achieved level: `L1`, `L2`, `L3`, `L4`, `L5`, `L6`, or `NOT_APPLICABLE_WITH_REASON`. |
| `Candidate Coverage Matrix Position` | Yes | Matrix coordinate: `Primary Class x Execution Depth`. |
| `Class Coverage Status` | Yes | Coverage status for this class/depth: `NOT_STARTED`, `DISCOVERED`, `IMPLEMENTED`, `CERTIFIED`, `PRODUCTION_CERTIFIED`, or `NOT_APPLICABLE`. |
| `Engineering Intent` | Yes | The original engineering purpose that the situation must close or explicitly fail to close. |
| `Current Reality` | Yes | Current observed state of the concrete situation, not desired state or document wording. |
| `Expected Reality` | Yes | Expected state after implementation, no-change, hold, rejection, or legal terminal alternative. |
| `Engineering Chain` | Yes | Chain ID / Chain Walk from Intent through Closure, or blocker with reason. |
| `Engineering Chain Segment` | Yes | Segment affected by the candidate: Intent, Trigger, Condition, Behaviour Instance, Decision, Execution, Verification, Outcome, Learning, Intent Closure, or explicit `NOT_APPLICABLE_WITH_REASON`. |
| `Behaviour Instance` | Yes | Concrete Behaviour Instance in current Reality, or explicit `NOT_APPLICABLE_WITH_REASON` for non-behaviour engineering situation. |
| `Behaviour` | Yes | Behaviour Definition / Instance or `NOT_APPLICABLE_WITH_REASON` for non-behaviour rule evidence. |
| `Automation Logic` | Yes | Automation-Ready Engineering Logic, blocker, or `NOT_APPLICABLE`. |
| `Automation Break` | Required when exists | Discovered stopping point in existing logic, or explicit no-break terminal reason. |
| `Existing Rule` | Yes | Existing rule, gate, condition, policy, verification, rollback, authority, maturity, or continuation rule. |
| `Current Outcome` | Yes | Actual outcome currently observed, including `NO_OUTCOME_YET`, `UNKNOWN_WITH_REASON`, or evidence-backed outcome. |
| `Expected Outcome` | Yes | Outcome expected after OMP Mission or legal terminal alternative. |
| `Intent Closure State` | Yes | `INTENT_CLOSED`, `AUTOMATION_BREAK`, `INTENT_NOT_APPLICABLE`, `UNKNOWN_WITH_REASON`, or legal blocker. |
| `Affected Owner` | Yes | Existing owner that can receive implementation, hold, rejection, no-change, or terminal classification. |
| `Owner` | Yes | Alias of Affected Owner for OMP compatibility. |
| `Producer` | Yes | Existing producer of the candidate input or evidence. |
| `Affected Consumer` | Yes | Existing consumer expected to use the result, or explicit consumer gap. |
| `Consumer` | Yes | OMP, existing owner, CPS, Production Maturity, Codex input, or terminal alternative. |
| `Evidence` | Yes | Evidence proving the situation exists in Reality; documents/models may appear here only as evidence, never as the candidate itself. |
| `Implementation Scope` | Yes | Existing file/module/tool/document/owner scope or blocker. |
| `Runtime Impact` | Yes | `NONE`, `READ_ONLY`, `GUARDED`, `RUNTIME_AFFECTING`, or `UNKNOWN`. |
| `Production Impact` | Yes | `NONE`, `OBSERVATION`, `ADVISORY`, `PRODUCTION_AFFECTING`, or `UNKNOWN`. |
| `Dependencies` | Yes | Existing dependencies, missing dependencies, or `NOT_APPLICABLE`. |
| `Verification` | Yes | Existing verification path or blocker. |
| `Verification Context` | Yes | What will prove the candidate outcome, including method, owner, source, and expected evidence. |
| `Rollback` | Yes | Existing rollback/containment/`STOP_SAFE`, not applicable reason, or blocker. |
| `Authority` | Yes | Existing authority boundary or blocker. |
| `Authority Context` | Yes | Whether implementation/no-change is allowed automatically or must stop at `ENGINEERING_AUTHORITY`, `OPERATIONAL_AUTHORITY`, `STOP_SAFE`, or another existing boundary. |
| `Terminal Path` | Yes | Mission, hold, reject, not applicable, no-change, STOP_SAFE, authority stop, or other legal terminal path available to OMP. |
| `Implementation Readiness` | Yes | `IMPLEMENTATION_READY`, `IMPLEMENTATION_BLOCKED`, or `IMPLEMENTATION_NOT_APPLICABLE`. |
| `Implementation Blocking Reason` | Required when blocked | Exact blocker from the official blocker table. |
| `OMP Consumer` | Yes | OMP consumer path or terminal no-OMP reason. |
| `Codex Readiness` | Yes | `CODEX_READY`, `CODEX_READY_WITH_LIMITS`, `CODEX_BLOCKED`, or `CODEX_NOT_APPLICABLE`. |

### Candidate Reality Gate

BDP may emit an Implementation Candidate Instance only if it represents a real engineering situation.

A real engineering situation exists only when BDP can prove all of the following:

1. It exists in current Reality through evidence.
2. It belongs to an Engineering Chain or has a recorded chain-observation blocker.
3. It contains a Behaviour Instance or a justified non-behaviour engineering chain segment.
4. It has Engineering Intent.
5. It has Current Reality and Expected Reality.
6. It has Current Outcome and Expected Outcome.
7. It has Intent Closure State.
8. It has affected Owner and affected Consumer or explicit consumer gap.
9. It has Verification Context.
10. It has Authority Context.
11. It has Terminal Path.
12. OMP can admit, hold, reject, or mark it not applicable.
13. It has exactly one Primary Class.
14. It has Candidate Coverage Matrix position.
15. It has Execution Depth.
16. It has Class Coverage Status.

If any condition fails, BDP must not emit `IMPLEMENTATION_READY`.

It must emit one of:

```text
IMPLEMENTATION_BLOCKED
IMPLEMENTATION_NOT_APPLICABLE
REALITY_INSTANCE_INSUFFICIENT
ENGINEERING_CHAIN_NOT_OBSERVED_WITH_REASON
CONSUMER_GAP_RECORDED
OWNER_GAP_RECORDED
VERIFICATION_CONTEXT_MISSING
AUTHORITY_CONTEXT_MISSING
TERMINAL_PATH_MISSING
CANDIDATE_CLASS_MISSING
CANDIDATE_COVERAGE_POSITION_MISSING
EXECUTION_DEPTH_MISSING
COVERAGE_STATUS_MISSING
```

### Implementation Candidate Classification Model

Status: `CANONICAL_BDP_REFINEMENT`

Implementation Candidate Classification is part of the existing BDP Implementation Candidate Instance contract.

It is not:

- a new architecture;
- a new owner;
- a new pipeline;
- a new OMP mission mechanism;
- a replacement for OMP Candidate Identity;
- a replacement for Action Class authority;
- a replacement for Capability Classification;
- a replacement for Engineering Logic Coverage.

BDP owns classification before handoff.
OMP owns admission after handoff.

Every Implementation Candidate Instance must have:

- exactly one `Primary Class`;
- zero or more `Secondary Classes`;
- one `Execution Depth`;
- one `Candidate Coverage Matrix Position`;
- one `Class Coverage Status`.

Primary Class is selected by the dominant engineering responsibility being changed or proven.

Secondary Classes may be attached when the same Candidate also touches supporting responsibilities. Secondary Classes must not make the Candidate ambiguous and must not allow one Candidate Instance to be counted as multiple Primary Class instances.

#### Reused Classification Sources

This model reuses existing V7 mechanisms:

| Existing mechanism | Reuse |
| --- | --- |
| Engineering Entity Model | `Implementation Candidate Class` and `Implementation Candidate Instance` are existing entities. |
| Engineering Chain Model | Class selection follows the affected Chain segment and Engineering Intent. |
| Automation Readiness Model | Supplies automation status, blockers, trigger/execution/verification/rollback/authority coverage. |
| Implementation Readiness Model | Supplies implementation readiness, blocker, owner, consumer, scope, verification, rollback, authority, and OMP consumer context. |
| Engineering Logic Coverage Model | Supplies coverage states and progress measurement. |
| OMP Candidate Identity | OMP consumes Class / Instance identity but does not receive class-only work. |
| Action Class / Authority Model | Runtime authority remains separate from Candidate Class. |
| Execution Certification Ladder | Supplies Execution Depth and certification evidence. |

#### World Research Normalization

World research is used only to normalize class coverage, not to import foreign architectures.

Representative mature-system patterns:

| Source family | Normalized engineering pattern for V7 |
| --- | --- |
| Kubernetes controllers | Reconcile current state toward desired state; classify observation, desired/current delta, execution, status update, and external-state boundaries. |
| Google SRE | Separate monitoring, automation, release/change, incident response, rollback, learning, and simplicity/decoupling. |
| AWS Well-Architected / cloud operations | Treat operations as code, make reversible changes, learn from operational events, and verify operational readiness. |
| Cisco / Juniper / Arista routing systems | Separate config intent, policy, route selection, convergence, maintenance, and rollback/commit-confirm boundaries. |
| BGP / OSPF / IS-IS / MPLS / SD-WAN / IETF RFCs | Separate signaling, policy, convergence, graceful drain, reachability, and failure containment. |
| Envoy / HAProxy / NGINX | Separate health checking, runtime guards, load-balancing decisions, drain/slow-start, and upstream availability. |
| Cloudflare / Meta / Netflix / Google Traffic Engineering | Separate traffic steering, capacity, degradation, staged rollout, blast-radius, and feedback loops. |
| AWS / Azure / GCP | Separate managed control-plane intent, authority/IAM, deployment, health, rollback, audit, and evidence. |

V7 canonical classes below are universal normalized classes, not copied vendor classes.

#### Official Implementation Candidate Classes

| Class | Purpose | Typical Engineering Intent | Typical Engineering Chain | Typical Automation Break | Typical Behaviour | Typical Verification | Typical Terminal State | Typical OMP Consumption | Typical Execution Certification | Production Impact | Runtime Impact | Authority Boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `OBSERVATION_EVIDENCE_REFRESH` | Produce or refresh current evidence without mutating Runtime. | Make current state observable and fresh enough for downstream decisions. | Trigger -> Observation -> Evidence -> Verification -> Consumer. | `MISSING_EVIDENCE`, `MISSING_TRIGGER`, stale evidence. | Read-model, service matrix, quality snapshot, diagnostic view, evidence refresh. | Freshness check, schema check, source owner check, read-only test. | `VERIFIED_EVIDENCE_AVAILABLE` or `EVIDENCE_BLOCKED`. | OMP consumes as evidence or no-change terminal alternative. | L1-L6 for no-mutation lane; production certification only when evidence is production-owned. | `NONE` or `OBSERVATION`. | `NONE` or `READ_ONLY`. | Observation authority only; no Runtime apply. |
| `INTERPRETATION_DECISION_ADVISORY` | Interpret evidence and produce advisory or decision-support output. | Convert current facts into ranking, explanation, suitability, or recommendation without granting execution. | Evidence -> Interpretation -> Advisory Decision -> Consumer. | `MISSING_DECISION_RULE`, `MISSING_CONSUMER`, insufficient evidence. | Routing advisory, scoring, diagnosis, explanation, candidate suitability. | Deterministic predicate tests, no-movement proof, owner consumer proof. | `ADVISORY_PRODUCED`, `NO_ACTION`, or `INTERPRETATION_BLOCKED`. | OMP consumes as decision evidence, not as execution permission. | L1-L6 if advisory remains no-mutation and Behavior Chain completes. | `ADVISORY`. | `READ_ONLY`. | Advisory cannot approve governance or Runtime mutation. |
| `POLICY_AUTHORITY_BOUNDARY` | Resolve whether existing policy/authority permits action. | Prevent unauthorized execution and classify required stop or allowed path. | Intent -> Policy -> Authority Review -> Stop / Allow / Hold. | `MISSING_AUTHORITY`, `BLOCKED_BY_POLICY`, unknown authority. | Action-class check, authority gate, policy enforcement, STOP classification. | Policy owner check, authority matrix, action-class evidence. | `AUTHORIZED`, `AUTHORITY_STOP`, `POLICY_BLOCKED`, or `HOLD`. | OMP consumes as admission boundary. | Certifiable through legal terminal stop or authorized no-change; Runtime mutation requires separate authority evidence. | `NONE` to `PRODUCTION_AFFECTING`. | `NONE`, `GUARDED`, or `RUNTIME_AFFECTING`. | Existing OMP / policy / operator authority only. |
| `EXECUTION_PACKET_LEASE_GATE` | Bind execution identity before any guarded action. | Ensure the exact approved action is the only executable action. | Decision -> Packet -> Lease -> Gate -> Execute / Reject. | `MISSING_IDENTITY`, `MISSING_PACKET`, stale lease, hash mismatch. | Packet generation, lease validation, duplicate-owner guard, replay denial. | Packet tests, identity hash tests, lease expiry tests, replay denial tests. | `VALID_LEASE`, `PACKET_REJECTED`, `STOP_SAFE`, or `NO_EXECUTION`. | OMP consumes as Mission admission/execution gate. | L1-L6 in no-mutation preview/reject lane; mutation requires authority and rollback proof. | `NONE` to `PRODUCTION_AFFECTING`. | `GUARDED` or `RUNTIME_AFFECTING`. | Exact packet, lease, rollback, and action-class authority required. |
| `RUNTIME_APPLY_OR_SERVICE_MUTATION` | Perform a bounded Runtime or service state mutation. | Change live routing/service/deployment state under certified authority. | Intent -> Authority -> Execute -> Verify -> Outcome -> Rollback/Contain. | `MISSING_RUNTIME_SUPPORT`, `MISSING_AUTHORITY`, `MISSING_ROLLBACK`, `MISSING_VERIFICATION`. | User movement, service failover, deploy apply, proxy/runtime change. | Runtime verification, truth/convergence, production evidence, rollback/no-rollback evidence. | `IMPLEMENTED_VERIFIED`, `ROLLBACK_VERIFIED`, `STOP_SAFE`, or `AUTHORITY_STOP`. | OMP consumes as Mission only after authority and rollback gates. | Not L6-continuous unless production/authority class is certified; may stop at authority. | `PRODUCTION_AFFECTING`. | `RUNTIME_AFFECTING`. | Operational/production authority required. |
| `VERIFICATION_TRUTH_CONVERGENCE` | Prove implementation, source truth, runtime truth, or convergence. | Determine whether current state matches expected state. | Expected State -> Verification -> Result -> Consumer. | `MISSING_VERIFICATION`, inconclusive truth, convergence mismatch. | Test execution, truth-check, convergence status, schema verification. | Test result, truth/convergence evidence, report consumption. | `VERIFIED`, `FAILED`, `INCONCLUSIVE`, `BLOCKED`, or `NOT_APPLICABLE`. | OMP consumes as pass/fail/hold evidence. | L1-L6 if verification has consumer and Behavior Chain completes. | `NONE` or `OBSERVATION`. | `NONE` or `READ_ONLY`. | Verification owner only; no apply authority. |
| `ROLLBACK_CONTAINMENT_RECOVERY` | Restore or contain failed/unsafe state. | Make failure recoverable or explicitly contained. | Failure / Risk -> Rollback / Containment -> Verification -> Outcome. | `MISSING_ROLLBACK`, `CONTAINMENT_UNCERTAIN`, unsafe action. | Restore barrier, rollback packet, containment classification, recovery check. | Rollback dry-run, rollback verification, containment evidence. | `ROLLBACK_READY`, `ROLLBACK_VERIFIED`, `CONTAINED`, `STOP_SAFE`, or `HOLD`. | OMP consumes as safety precondition or recovery Mission. | Certifiable as no-mutation proof or governed rollback; mutation requires authority. | `NONE` to `PRODUCTION_AFFECTING`. | `GUARDED` or `RUNTIME_AFFECTING`. | Rollback/containment authority required when applying changes. |
| `CONSUMER_CONFIRMATION_CHAIN_CLOSURE` | Prove producer output was consumed and changed downstream behavior. | Close output lifecycle and prevent orphan artifacts. | Producer -> Output -> Consumer -> Consumption -> Behavior Change -> Next Output. | `MISSING_CONSUMER`, `CONSUMPTION_NOT_VERIFIED`, `ORPHAN_OUTPUT`. | Report consumption, CPS update/no-change, owner confirmation, terminal consumer proof. | Behavior Chain Status, consumption evidence, terminal consumer verification. | `CHAIN_CLOSED`, `TERMINAL_ACCEPTED`, `TERMINAL_HOLD`, or `BROKEN`. | OMP consumes as closure evidence and blocker input. | L1-L6 when `Behavior Chain Status = COMPLETE` or legal terminal verified. | `NONE`. | `NONE`. | Existing owner consumption only. |
| `LEARNING_FEEDBACK_MATURITY` | Convert verified outcome into learning, confidence, or maturity signal. | Preserve operational learning and update maturity only through owner. | Outcome -> Learning -> Maturity / Future Decision -> Consumer. | `MISSING_OUTCOME`, `MISSING_CONSUMER`, `MISSING_EVIDENCE`. | Feedback materialization, prediction delta, maturity decision, confidence update. | Feedback tests, maturity decision evidence, owner consumption. | `LEARNING_RECORDED`, `NO_CHANGE`, `MATURITY_UPDATED`, or `HOLD`. | OMP / Production Maturity consumes as evidence, not automatic authority. | L1-L6 for no-mutation learning lane; production certification requires maturity owner. | `NONE` or `OBSERVATION`. | `NONE` or `READ_ONLY`. | Production Maturity owner for maturity changes. |
| `KNOWLEDGE_CANONICAL_SYNC` | Synchronize durable knowledge only through canonical owners. | Promote accepted durable truth or record no-change. | Evidence -> Knowledge Owner -> Canonical Sync -> Consumer. | `MISSING_OWNER_ACCEPTANCE`, `MISSING_TRACEABILITY`, superseded truth. | Canonical Reference/SYSTEM_MAP/Locked Knowledge sync, no-change, provenance preservation. | Owner acceptance, traceability check, no-orphan evidence. | `CANONICAL_UPDATED`, `NO_CHANGE`, `HISTORICAL_ONLY`, or `HOLD`. | OMP consumes as durable truth update/no-change evidence. | L1-L6 when legal terminal consumer is verified; no automatic locked knowledge mutation. | `NONE`. | `NONE`. | Canonical owner acceptance required. |
| `DISCOVERY_INDEX_TRACEABILITY` | Use indexes to find sources, relationships, and traceability without creating truth. | Improve discovery coverage and avoid missing owner/consumer paths. | Discovery Index -> Source Resolution -> Traceability -> Candidate / Not Applicable. | `MISSING_SOURCE`, `UNKNOWN_OWNER`, unresolved relationship. | Function Graph, repository search, SYSTEM_MAP index use, source trace. | Source resolution, official-source confirmation, trace path uniqueness. | `TRACE_RESOLVED`, `SOURCE_RESOLVED`, `NOT_APPLICABLE`, or `UNKNOWN`. | OMP consumes only through certified Candidate evidence, never raw index. | L1-L6 only when trace supports a real Candidate; index alone is not countable. | `NONE`. | `NONE`. | Discovery only; no truth or execution authority. |
| `IMPLEMENTATION_OWNER_EXTENSION` | Modify an existing owner in a bounded, verified way. | Add, correct, or harden behavior within an existing owner without new architecture. | Intent -> Scope -> Implementation -> Verification -> Consumer. | `MISSING_EXISTING_OWNER_EXTENSION`, bounded missing implementation. | Code/doc owner extension, guard, parser, schema, report lifecycle improvement. | Tests, diff review, owner verification, Behavior Chain completion. | `IMPLEMENTED_VERIFIED`, `NO_CHANGE`, `HOLD`, or `REJECTED`. | OMP consumes as Mission candidate after admission. | L1-L6 when each instance has verified terminal consumer; production certification if runtime/production affected. | `NONE` to `PRODUCTION_AFFECTING`. | `NONE`, `READ_ONLY`, `GUARDED`, or `RUNTIME_AFFECTING`. | Existing owner and OMP mission authority only. |
| `ARCHITECTURE_BOUNDARY_OR_GAP_PROOF` | Classify work that cannot be expressed by existing architecture. | Prove whether a real engineering situation is blocked by architecture boundary. | Candidate -> Existing Owner Search -> Reuse Failure Proof -> Stop / Gap Report. | `ARCHITECTURE_REQUIRED`, `NEW_OWNER_REQUIRED`, unexpressible responsibility. | Fundamental architecture gap proof, forbidden action, explicit hold. | Existing owner exhaustion, contradiction proof, architecture review. | `FUNDAMENTAL_ARCHITECTURE_GAP`, `REJECTED_EXISTING_OWNER_AVAILABLE`, or `HOLD`. | OMP consumes only as stop/gap evidence; no automatic architecture change. | Not certifiable as implementation completion; certifiable as legal terminal stop only. | `NONE`. | `NONE`. | Engineering authority; architecture change requires separate controlled action. |

#### Primary Class Decision Rule

BDP selects Primary Class deterministically:

1. If the Candidate would require new architecture or new owner, use `ARCHITECTURE_BOUNDARY_OR_GAP_PROOF`.
2. Else if the Candidate's dominant purpose is live mutation, use `RUNTIME_APPLY_OR_SERVICE_MUTATION`.
3. Else if the dominant purpose is admission/authority/policy decision, use `POLICY_AUTHORITY_BOUNDARY`.
4. Else if the dominant purpose is packet/lease/identity execution gating, use `EXECUTION_PACKET_LEASE_GATE`.
5. Else if the dominant purpose is rollback, containment, or recovery, use `ROLLBACK_CONTAINMENT_RECOVERY`.
6. Else if the dominant purpose is verification/truth/convergence, use `VERIFICATION_TRUTH_CONVERGENCE`.
7. Else if the dominant purpose is consumer confirmation or chain closure, use `CONSUMER_CONFIRMATION_CHAIN_CLOSURE`.
8. Else if the dominant purpose is learning, feedback, maturity, or outcome materialization, use `LEARNING_FEEDBACK_MATURITY`.
9. Else if the dominant purpose is canonical knowledge synchronization, use `KNOWLEDGE_CANONICAL_SYNC`.
10. Else if the dominant purpose is discovery index / traceability use, use `DISCOVERY_INDEX_TRACEABILITY`.
11. Else if the dominant purpose is observation/evidence refresh, use `OBSERVATION_EVIDENCE_REFRESH`.
12. Else if the dominant purpose is interpretation/advisory decision support, use `INTERPRETATION_DECISION_ADVISORY`.
13. Else if the dominant purpose is bounded existing-owner implementation, use `IMPLEMENTATION_OWNER_EXTENSION`.
14. Else return `CANDIDATE_CLASS_UNKNOWN_WITH_REASON` and do not emit `IMPLEMENTATION_READY`.

No Candidate may have more than one Primary Class.

#### Candidate Class Coverage

For each official class BDP must record:

| Coverage Field | Meaning |
| --- | --- |
| `Covered` | Existing implementation / evidence / owner paths prove this class can be represented. |
| `Not Covered` | A real engineering situation exists that cannot be represented by the class. |
| `Unknown` | Evidence is insufficient to determine coverage. |
| `Discovery Required` | Additional bounded BDP Discovery is required to classify coverage. |

Class coverage does not imply implementation completion.

Class coverage means BDP can represent, classify, trace, and hand off the Candidate without inventing a new architecture.

#### Candidate Coverage Matrix

BDP must maintain a Candidate Coverage Matrix.

Matrix X-axis:

```text
Execution Depth: L1, L2, L3, L4, L5, L6
```

Matrix Y-axis:

```text
Implementation Candidate Class
```

Allowed cell statuses:

```text
NOT_STARTED
DISCOVERED
IMPLEMENTED
CERTIFIED
PRODUCTION_CERTIFIED
NOT_APPLICABLE
```

Cell meanings:

| Status | Meaning |
| --- | --- |
| `NOT_STARTED` | No real Candidate Instance has been discovered for this class/depth. |
| `DISCOVERED` | A real Candidate Instance exists and passes Candidate Reality Gate, but is not implemented/certified at this depth. |
| `IMPLEMENTED` | Existing implementation or no-change/legal terminal implementation evidence exists. |
| `CERTIFIED` | Execution Certification or equivalent owner certification proves this class/depth in a non-production or bounded mode. |
| `PRODUCTION_CERTIFIED` | Production Maturity or production certification owner proves this class/depth in production. |
| `NOT_APPLICABLE` | The class cannot legally apply to the depth, with reason. |

Coverage Matrix rules:

1. Matrix status must be based on evidence, not aspiration.
2. A document, report, owner, model, rule, section, Function Graph node, or context artifact cannot fill a matrix cell by itself.
3. Matrix coverage must preserve Primary Class.
4. Secondary Classes may be noted but must not double-count coverage.
5. A class/depth may be `CERTIFIED` only if Behavior Chain completion or legal terminal consumer verification exists.
6. A class/depth may be `PRODUCTION_CERTIFIED` only if production certification or Production Maturity owner evidence exists.
7. `UNKNOWN` is not an allowed cell status; unknowns must appear as `NOT_STARTED` or `DISCOVERED` with explicit blocker in the supporting coverage record.
8. Candidate Coverage Matrix is a BDP progress view and not a new truth source.

#### Candidate Coverage Matrix Projections

Candidate Coverage Matrix has two official projections over the same cells:

| Projection | Question Answered |
| --- | --- |
| `Current View` | Where each Implementation Candidate Class currently stands at each Execution Depth. |
| `Progress Projection` | What is required for each cell to reach the next Coverage State and ultimately `PRODUCTION_CERTIFIED`. |

Progress Projection is not:

- a new matrix;
- a new model;
- a new architecture;
- a new owner;
- a new truth source;
- a new progress state;
- a replacement for Engineering Logic Coverage;
- a replacement for Automation Progress, Implementation Progress, or Production Enablement outputs.

Progress Projection is a computed view of Candidate Coverage Matrix cells using existing BDP, OMP, Execution Certification, Production Maturity, Verification, Rollback, Authority, Consumer, Chain Closure, and Intent Closure evidence.

For every Candidate Coverage Matrix cell, BDP must compute:

| Field | Required | Meaning |
| --- | ---: | --- |
| `Current Status` | Yes | Existing cell status from the allowed Candidate Coverage Matrix statuses. |
| `Next Status` | Yes | Next legal status on the path to `PRODUCTION_CERTIFIED`, or `TERMINAL_ALTERNATIVE`. |
| `Remaining Path` | Yes | Ordered remaining legal statuses and owner gates needed to reach `PRODUCTION_CERTIFIED`, or terminal alternative. |
| `Blocking Conditions` | Yes | Exact blockers preventing the next status, or `NONE`. |
| `Blocking Owner` | Yes | Existing owner responsible for the blocker, or `NOT_APPLICABLE`. |
| `Blocking Evidence` | Yes | Missing or insufficient evidence, or `NONE`. |
| `Blocking Verification` | Yes | Missing verification path/evidence, or `NONE`. |
| `Blocking Authority` | Yes | Authority boundary or stop condition, or `NONE`. |
| `Blocking Rollback` | Yes | Missing rollback/containment/`STOP_SAFE`, or `NONE`. |
| `Blocking Runtime` | Yes | Runtime owner/path limitation, or `NONE`. |
| `Blocking Production` | Yes | Production Maturity / production certification blocker, or `NONE`. |
| `Blocking Consumer` | Yes | Missing consumer or consumption confirmation blocker, or `NONE`. |
| `Blocking Chain` | Yes | Missing Engineering Chain segment or closure blocker, or `NONE`. |
| `Blocking Intent Closure` | Yes | Missing or failed Intent Closure blocker, or `NONE`. |
| `Estimated Existing Work` | Yes | Computed count and names of existing-owner work items required to advance, not a new backlog. |
| `Terminal Alternative` | Yes | Legal terminal alternative when progress is not applicable or unsafe. |
| `Depends On` | Yes | Existing Implementation Candidate Instances or chain conditions that must be completed before this cell can advance, computed only from Engineering Chain Walk. |
| `Unblocks` | Yes | Existing Implementation Candidate Instances or chain conditions that can advance if this cell advances, computed only from Engineering Chain Walk. |
| `Critical Path` | Yes | Whether this cell sits on the longest or most blocking existing Engineering Chain path to `PRODUCTION_CERTIFIED`. |
| `Dependency Depth` | Yes | Number of unresolved upstream Engineering Chain dependencies between this cell and the nearest currently advanceable candidate or terminal alternative. |
| `Root Cause` | Yes | Single evidence-backed root cause for blocked progress, or `ROOT_CAUSE_NOT_DETERMINED_WITH_REASON`. |
| `Final Consumer` | Yes | Terminal consumer of the chain path affected by this cell. |

Legal status progression:

```text
NOT_STARTED
  -> DISCOVERED
  -> IMPLEMENTED
  -> CERTIFIED
  -> PRODUCTION_CERTIFIED
```

`NOT_APPLICABLE` is terminal and must have a reason.

Progress Projection must not create new Coverage States or Progress States.

Progress Projection must not create:

- Dependency Graph;
- Progress Graph;
- Navigation Graph;
- Relationship Graph;
- Dependency Model.

All dependency, unblock, critical-path, root-cause, and final-consumer fields must be computed from the existing Engineering Chain, Chain Walk, Producer, Consumer, Intent Closure, Verification, Authority, Rollback, Production, Runtime, Execution Certification, and Candidate Coverage Matrix.

#### Progress Path Calculation

For each cell, BDP must calculate the path to `PRODUCTION_CERTIFIED` using only existing mechanisms:

```text
Current Status
  -> Resolve Next Legal Status
  -> Resolve Engineering Chain Walk
  -> Resolve Producer -> Consumer Path
  -> Resolve Existing Owner
  -> Resolve Existing Consumer
  -> Resolve Existing Verification
  -> Resolve Existing Rollback / STOP_SAFE
  -> Resolve Existing Authority
  -> Resolve Existing Runtime Boundary
  -> Resolve Existing Production Boundary
  -> Resolve Engineering Chain Closure
  -> Resolve Intent Closure
  -> Resolve Terminal Alternative
  -> Compute Remaining Path
```

If the path cannot be expressed through existing owners, rules, gates, certification, chains, or checks, BDP must:

1. verify whether an existing owner can express the path;
2. verify whether the blocker is evidence, verification, authority, rollback, runtime, production, consumer, chain, or intent closure;
3. verify whether the class/depth is legally `NOT_APPLICABLE`;
4. only after those checks record `FUNDAMENTAL_ARCHITECTURE_GAP`.

BDP must not invent architecture to create a path.

#### Engineering Chain Dependency Projection

Progress Projection uses Engineering Chain as the only relationship source for candidate dependencies.

It must not build a separate dependency graph.

For every Implementation Candidate Instance, BDP must compute:

| Field | Computation Rule |
| --- | --- |
| `Depends On` | Upstream Implementation Candidate Instances or chain conditions whose terminal state is required before the candidate can reach its Next Status. Derived from Backward Walk and Producer -> Consumer Walk only. |
| `Unblocks` | Downstream Implementation Candidate Instances or chain conditions whose blocker is removed if the candidate reaches its Next Status. Derived from Forward Walk and Producer -> Consumer Walk only. |
| `Critical Path` | `YES` when the candidate is on the longest unresolved chain path to Production Certification, blocks the greatest downstream progress, or is the only path to a required Final Consumer; otherwise `NO` with reason. |
| `Dependency Depth` | Count of unresolved upstream dependency steps in the Engineering Chain. `0` means the candidate is currently advanceable if all non-chain blockers are clear. |
| `Root Cause` | The earliest unresolved evidence-backed chain blocker that prevents progress, selected from existing blocker categories. If none can be proven, record `ROOT_CAUSE_NOT_DETERMINED_WITH_REASON`. |
| `Final Consumer` | The terminal chain consumer affected by completion, legal terminal alternative, or stop. |

Dependency derivation rules:

1. `Depends On` may include only existing Implementation Candidate Instances, existing chain conditions, or legal terminal alternatives.
2. `Unblocks` may include only existing Implementation Candidate Instances, existing chain conditions, or legal terminal alternatives.
3. BDP must not infer dependency from name similarity, file proximity, class similarity, document order, report wording, or Function Graph adjacency alone.
4. Function Graph may provide trace evidence only when the relationship is confirmed by Engineering Chain Producer -> Consumer evidence.
5. A document, owner, model, report, rule, section, canonical source, or Function Graph node cannot be a dependency target by itself.
6. If multiple upstream blockers exist, `Root Cause` must be the earliest unresolved blocker in the Backward Walk that prevents all downstream progress.
7. If the earliest blocker cannot be determined from evidence, BDP must record `ROOT_CAUSE_NOT_DETERMINED_WITH_REASON` and must not invent a root cause.
8. If no existing Engineering Chain can express dependency, BDP must classify the condition as missing chain evidence before recording any architecture gap.

#### System Engineering Value Projection

Engineering Value must include system effect, not only local cell gain.

For every Implementation Candidate Instance, BDP must compute:

| System Value Field | Computation Rule |
| --- | --- |
| `Unblocked Candidate Count` | Count of downstream Candidate Instances that can advance if this candidate reaches its Next Status. |
| `Critical Path Impact` | `1.00` when candidate is on the critical path, `0.50` when it affects a critical path indirectly, `0.00` otherwise. |
| `Root Cause Impact` | Count or ratio of blocked candidates sharing this candidate's Root Cause. |
| `System Engineering Value` | Engineering Value plus normalized Unblocked Candidate Count, Critical Path Impact, and Root Cause Impact. |

Default system value formula:

```text
System Engineering Value =
  Engineering Value
  + normalized(Unblocked Candidate Count)
  + Critical Path Impact
  + normalized(Root Cause Impact)
```

System Engineering Value must preserve blockers and must not become subjective priority.

OMP remains the owner of admission, sequencing, mission creation, and implementation selection.

#### Engineering Value Projection

For every Implementation Candidate Instance, BDP must compute Engineering Value from existing evidence:

| Value Field | Computation Rule |
| --- | --- |
| `Coverage Gain` | Delta in Candidate Coverage Matrix status weight for the affected Primary Class / Execution Depth. |
| `Production Gain` | Delta toward `PRODUCTION_CERTIFIED`, using Production Maturity or production certification evidence. |
| `Automation Gain` | Delta in existing Automation Coverage / Automation Progress for the affected class or chain. |
| `Chain Closure Gain` | Delta from unresolved consumer/chain/intent closure to verified closure or legal terminal alternative. |
| `Verification Gain` | Delta from missing/inconclusive verification to accepted verification evidence. |
| `Engineering Value` | Weighted sum of the above deltas, with blockers preserved and no manual override. |

Default status weights for computed gain:

| Status | Weight |
| --- | ---: |
| `NOT_STARTED` | `0.00` |
| `DISCOVERED` | `0.25` |
| `IMPLEMENTED` | `0.50` |
| `CERTIFIED` | `0.75` |
| `PRODUCTION_CERTIFIED` | `1.00` |
| `NOT_APPLICABLE` | Excluded from denominator with reason. |

Default Engineering Value formula:

```text
Engineering Value =
  Coverage Gain
  + Production Gain
  + Automation Gain
  + Chain Closure Gain
  + Verification Gain
```

BDP may report component values separately, but must not replace them with subjective priority.

#### Project Maturity Projection

BDP must compute project-level maturity indicators from Candidate Coverage Matrix and existing coverage evidence:

| Indicator | Computation Rule |
| --- | --- |
| `Overall Coverage` | Eligible cells with status above `NOT_STARTED` divided by all eligible cells. |
| `Overall Automation Coverage` | Eligible cells with automation-ready or automated evidence divided by all eligible cells. |
| `Overall Implementation Coverage` | Eligible cells at `IMPLEMENTED`, `CERTIFIED`, or `PRODUCTION_CERTIFIED` divided by all eligible cells. |
| `Overall Verification Coverage` | Eligible cells at `CERTIFIED` or `PRODUCTION_CERTIFIED` divided by all eligible cells. |
| `Overall Production Coverage` | Eligible cells at `PRODUCTION_CERTIFIED` divided by all eligible cells. |
| `Overall Chain Closure` | Eligible cells with verified Engineering Chain Closure or legal terminal consumer divided by all eligible cells. |
| `Overall Engineering Maturity` | Computed average of eligible cell status weights, adjusted only by existing chain closure and verification evidence. |

These indicators are BDP navigation metrics.

They must not overwrite canonical Engineering Maturity or Production Maturity owned by the Production Maturity model.

#### Progress Query Requirements

Using Progress Projection, BDP must be able to answer:

- which class has the highest maturity;
- which class has the lowest maturity;
- which blockers prevent Production Certification;
- which candidate unblocks the largest number of other candidates;
- which candidates lie on the critical path;
- which root cause blocks the largest part of the project;
- which existing owners are bottlenecks;
- which existing consumers do not close chains;
- which verification paths are missing;
- which rollback paths are missing;
- which authority boundaries stop progress;
- which runtime boundaries limit progress;
- which production boundaries remain;
- which candidates produce maximum computed maturity gain through existing OMP consumption.

#### Default V7 Candidate Coverage Matrix Baseline

Initial baseline after classification integration:

| Implementation Candidate Class | L1 | L2 | L3 | L4 | L5 | L6 |
| --- | --- | --- | --- | --- | --- | --- |
| `OBSERVATION_EVIDENCE_REFRESH` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` |
| `INTERPRETATION_DECISION_ADVISORY` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` |
| `POLICY_AUTHORITY_BOUNDARY` | `DISCOVERED` | `DISCOVERED` | `DISCOVERED` | `DISCOVERED` | `DISCOVERED` | `DISCOVERED` |
| `EXECUTION_PACKET_LEASE_GATE` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` |
| `RUNTIME_APPLY_OR_SERVICE_MUTATION` | `DISCOVERED` | `DISCOVERED` | `DISCOVERED` | `DISCOVERED` | `DISCOVERED` | `DISCOVERED` |
| `VERIFICATION_TRUTH_CONVERGENCE` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` |
| `ROLLBACK_CONTAINMENT_RECOVERY` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `DISCOVERED` |
| `CONSUMER_CONFIRMATION_CHAIN_CLOSURE` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` |
| `LEARNING_FEEDBACK_MATURITY` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` |
| `KNOWLEDGE_CANONICAL_SYNC` | `DISCOVERED` | `DISCOVERED` | `DISCOVERED` | `DISCOVERED` | `DISCOVERED` | `DISCOVERED` |
| `DISCOVERY_INDEX_TRACEABILITY` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` |
| `IMPLEMENTATION_OWNER_EXTENSION` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` | `CERTIFIED` |
| `ARCHITECTURE_BOUNDARY_OR_GAP_PROOF` | `NOT_APPLICABLE` | `NOT_APPLICABLE` | `NOT_APPLICABLE` | `NOT_APPLICABLE` | `NOT_APPLICABLE` | `NOT_APPLICABLE` |

Baseline interpretation:

- `CERTIFIED` means the class has already been proven in the no-mutation / read-only / legal-terminal Execution Certification lane or equivalent existing evidence.
- `DISCOVERED` means real situations exist, but full certification or production certification still depends on existing authority, production, canonical-owner, or runtime boundaries.
- `NOT_APPLICABLE` for `ARCHITECTURE_BOUNDARY_OR_GAP_PROOF` means it is a legal stop/gap-proof class, not an implementation completion class.

#### No-Gap Rule

Every real engineering situation discovered by BDP must map to exactly one official Primary Class.

If no class fits, BDP must:

1. record the situation as `CANDIDATE_CLASS_UNKNOWN_WITH_REASON`;
2. prove why every existing class fails;
3. check whether the situation is actually a document, owner, report, model, source, rule, or context artifact rather than a Candidate Instance;
4. check whether an existing owner can express the situation as one of the existing classes;
5. only after proof of non-coverage may propose extension of the class list.

Class extension is a BDP refinement action and does not create architecture by itself.

#### No-Duplication Rule

Classes must not overlap by name or by vague similarity.

Primary Class separation is by dominant engineering responsibility:

| If the dominant responsibility is... | Use class |
| --- | --- |
| observe or refresh evidence | `OBSERVATION_EVIDENCE_REFRESH` |
| interpret or advise without authority | `INTERPRETATION_DECISION_ADVISORY` |
| decide authority or policy boundary | `POLICY_AUTHORITY_BOUNDARY` |
| bind packet / lease / execution identity | `EXECUTION_PACKET_LEASE_GATE` |
| mutate Runtime / service / production | `RUNTIME_APPLY_OR_SERVICE_MUTATION` |
| verify truth, test, or convergence | `VERIFICATION_TRUTH_CONVERGENCE` |
| rollback, contain, or recover | `ROLLBACK_CONTAINMENT_RECOVERY` |
| prove consumer confirmation or chain closure | `CONSUMER_CONFIRMATION_CHAIN_CLOSURE` |
| record learning, feedback, or maturity | `LEARNING_FEEDBACK_MATURITY` |
| synchronize canonical knowledge | `KNOWLEDGE_CANONICAL_SYNC` |
| use a discovery index or traceability surface | `DISCOVERY_INDEX_TRACEABILITY` |
| implement bounded existing-owner extension | `IMPLEMENTATION_OWNER_EXTENSION` |
| prove existing architecture cannot express situation | `ARCHITECTURE_BOUNDARY_OR_GAP_PROOF` |

If two classes appear applicable, BDP must select the class corresponding to the first unclosed dominant Engineering Chain responsibility and record the other class as Secondary Class.

#### Execution Certification Compatibility

For every class BDP must determine whether the Execution Certification Ladder can certify it:

| Class | Execution Certification compatibility |
| --- | --- |
| `OBSERVATION_EVIDENCE_REFRESH` | `YES` in no-mutation/read-only lanes; production certification when production evidence owner accepts. |
| `INTERPRETATION_DECISION_ADVISORY` | `YES` when advisory has no execution authority and Behavior Chain completes. |
| `POLICY_AUTHORITY_BOUNDARY` | `YES_AS_LEGAL_TERMINAL_OR_AUTHORITY_PROOF`; mutation requires separate authority. |
| `EXECUTION_PACKET_LEASE_GATE` | `YES` for preview/reject/no-mutation gates; runtime apply requires authority. |
| `RUNTIME_APPLY_OR_SERVICE_MUTATION` | `LIMITED`; stops at authority/rollback/production boundary unless certified. |
| `VERIFICATION_TRUTH_CONVERGENCE` | `YES` when verification evidence has consumer. |
| `ROLLBACK_CONTAINMENT_RECOVERY` | `YES_WITH_LIMITS`; rollback apply requires authority and scope. |
| `CONSUMER_CONFIRMATION_CHAIN_CLOSURE` | `YES`; this is core ladder evidence. |
| `LEARNING_FEEDBACK_MATURITY` | `YES_WITH_LIMITS`; maturity promotion requires Production Maturity owner. |
| `KNOWLEDGE_CANONICAL_SYNC` | `YES_WITH_LIMITS`; canonical mutation requires owner acceptance. |
| `DISCOVERY_INDEX_TRACEABILITY` | `YES_ONLY_AS_SUPPORTING_REAL_CANDIDATE`; index alone cannot be counted. |
| `IMPLEMENTATION_OWNER_EXTENSION` | `YES` when OMP admits Mission or legal terminal alternative and verification passes. |
| `ARCHITECTURE_BOUNDARY_OR_GAP_PROOF` | `NO_AS_IMPLEMENTATION`; `YES_AS_CANONICAL_STOP` if a real fundamental gap is proven. |

### Negative Candidate Semantics

BDP must not emit as Implementation Candidate Instance:

- document synchronization by itself;
- rule creation by itself;
- validation by itself;
- report creation by itself;
- owner existence by itself;
- model consumption by itself;
- STOP condition by itself;
- canonical source by itself;
- Function Graph node by itself;
- Behaviour Definition by itself;
- Automation Break by itself;
- abstract improvement with no current Reality and expected Reality;
- refactoring with no affected Behaviour / Engineering Chain segment and no current/expected outcome.

These may be evidence, source, owner, consumer, verification context, or terminal path for a real Candidate Instance.

They must not be the Candidate Instance.

Implementation Ready rules:

1. The candidate must reuse existing architecture.
2. The candidate must reuse existing Behaviour or `NOT_APPLICABLE` non-behaviour rule evidence.
3. The candidate must reuse existing owners.
4. The candidate must not create new rules, policies, gates, or authority.
5. The implementation scope must be bounded.
6. Runtime and production impact must be explicit.
7. Dependencies must be known or explicitly not applicable.
8. Verification must exist.
9. Rollback, containment, or `STOP_SAFE` must exist where required.
10. Authority must be sufficient or the candidate is blocked.
11. OMP consumer path must exist.
12. Codex readiness must be assessed.
13. Chain closure must be possible.

Relationship with Automation Readiness:

- Automation Readiness asks whether existing logic can be automatically evaluated or executed.
- Implementation Readiness asks whether existing logic is sufficiently defined to become implementation work.
- `AUTOMATION_READY`, `AUTOMATION_READY_WITH_LIMITS`, `MACHINE_CHECKABLE_ONLY`, and blocked automation states may all produce Implementation Candidates if the missing work is bounded and owner-mapped.
- `NOT_AUTOMATABLE` may produce an Implementation Candidate only when the implementation is to preserve or expose the non-automatable boundary through existing owners.
- Intent Closure may produce Implementation Candidates when an Automation Break is caused by missing implementation and the missing work is bounded, owner-mapped, and does not require new architecture, owner, rule, Behaviour, Runtime, Planner, or authority.

Relationship with OMP:

- BDP may produce `OMP Implementation Input`.
- BDP may produce `Implementation Candidate Catalogue`.
- BDP may produce `Engineering Automation Backlog` as a discovery catalogue.
- BDP must not create OMP missions.
- BDP must not update the official OMP Implementation Backlog.
- OMP remains the only owner that can select, prioritize, sequence, accept, reject, or route implementation work.

Relationship with Codex:

- BDP may produce `Codex Implementation Input`.
- Codex readiness means the work is sufficiently scoped for Codex to implement later under OMP/operator command.
- Codex readiness does not assign work to Codex.
- Codex readiness does not create a production dependency on Codex.
- Codex must not bypass OMP, owners, Runtime, Authority, Verification, Rollback, Production Maturity, or CPS.

Implementation Candidate generation lifecycle:

```text
Behaviour / Automation Candidate / Existing Rule
  -> Resolve Owner
  -> Resolve Producer
  -> Resolve Consumer
  -> Resolve Implementation Scope
  -> Resolve Dependencies
  -> Resolve Runtime Impact
  -> Resolve Production Impact
  -> Resolve Verification
  -> Resolve Rollback / STOP_SAFE
  -> Resolve Authority
  -> Resolve OMP Consumer
  -> Resolve Codex Readiness
  -> Implementation Readiness Decision
  -> Implementation Candidate Instance or Blocker
```

Implementation Candidate source paths:

| Source Path | Route | Catalogue Rule |
| --- | --- | --- |
| Readiness-derived | `Behaviour Instance -> Automation Readiness -> Implementation Readiness -> Implementation Candidate Instance` | Enter the unified Implementation Candidate Catalogue after Candidate Reality Gate and Implementation Readiness validation. |
| Intent-derived | `Engineering Intent -> Intent Trace -> Automation Break -> Candidate Reality Gate -> Implementation Candidate Instance` | Enter the same unified Implementation Candidate Catalogue after Intent Closure, Candidate Reality Gate, and Implementation Readiness validation. |

BDP must not create separate implementation catalogues for intent-derived candidates.

## 22. Engineering Logic Automation Coverage Model

Engineering Logic Automation Coverage is the final BDP progress metric.

It answers:

```text
What part of existing V7 engineering logic has moved from observed logic to production-enabled automation?
```

It is not:

- a new architecture;
- a new owner;
- a new truth source;
- a new Runtime state;
- a new Planner state;
- a new OMP state;
- a new implementation queue;
- a new production maturity owner;
- a replacement for Behaviour Reality, OMP, Production Maturity, or Engineering Reports.

Coverage must be computed from existing BDP outputs and reused owner evidence:

- Behaviour Candidate Registry;
- Behaviour Identity Resolution Matrix;
- Behaviour Completeness Matrix;
- Automation Readiness Matrix;
- Implementation Readiness Matrix;
- Implementation Candidate Catalogue;
- Implementation Blocker Matrix;
- Engineering Automation Backlog catalogue;
- Current Autonomous Behaviour Reality where accepted by its owner;
- OMP / CPS consumer state where available;
- Production Maturity and production evidence where available;
- Verification, rollback, authority, and chain closure evidence.

BDP must measure these coverage domains for every declared engineering area:

| Coverage Domain | Question |
| --- | --- |
| `Engineering Chain Coverage` | How much existing engineering logic is represented as a traceable Engineering Chain from Intent to Closure? |
| `Behaviour Coverage` | How much existing engineering logic is discovered, understood, and represented as Behaviour or explicit non-Behaviour evidence? |
| `Automation Coverage` | How much existing engineering logic is machine-checkable, automation-ready, limited-ready, blocked, manual-gated, or not automatable? |
| `Implementation Coverage` | How much existing engineering logic is implementation-ready, implementation-blocked, already implemented, or not applicable? |
| `Production Coverage` | How much existing engineering logic is verified, production-enabled, production-blocked, or explicitly not production-applicable? |

For every Behaviour, Automation Candidate, Implementation Candidate, and applicable non-behaviour engineering rule, BDP must assign one current coverage state:

| Coverage State | Meaning |
| --- | --- |
| `DISCOVERED` | Existing logic has evidence but has not yet been accepted into Reality. |
| `REALITY_ACCEPTED` | Behaviour or logic is accepted by the appropriate Reality/owner path. |
| `AUTOMATION_READY` | Logic satisfies Automation Readiness rules. |
| `IMPLEMENTATION_READY` | Logic satisfies Implementation Readiness rules. |
| `IMPLEMENTED` | Existing implementation evidence proves implementation exists. |
| `AUTOMATED` | Existing evidence proves the logic is automatically evaluated or executed through an existing owner path. |
| `VERIFIED` | Verification evidence exists for the implemented or accepted logic. |
| `PRODUCTION_ENABLED` | Production or Production Maturity evidence proves the logic is active or consumable in production path. |
| `DEPRECATED` | Logic is superseded, historical, or no longer active. |
| `NOT_APPLICABLE` | Coverage state does not apply to this logic, with reason. |
| `BLOCKED` | Logic cannot advance to the next coverage state; blocker must be recorded. |
| `UNKNOWN` | Evidence is insufficient to classify coverage state. |

For each engineering area, BDP must calculate the following Engineering Logic Coverage fields:

| Field | Required | Meaning |
| --- | ---: | --- |
| `Engineering Area` | Yes | Behaviour Surface Lens, owner area, source family, or declared scope area. |
| `Total Engineering Logic` | Yes | Total count or explicit bounded set of logic units in scope. |
| `Discovered` | Yes | Count or set of logic with evidence. |
| `Automation Ready` | Yes | Count or set with `AUTOMATION_READY` or `AUTOMATION_READY_WITH_LIMITS`. |
| `Implementation Ready` | Yes | Count or set with `IMPLEMENTATION_READY`. |
| `Implemented` | Yes | Count or set with implementation evidence. |
| `Automated` | Yes | Count or set with automatic evaluation or execution evidence. |
| `Verified` | Yes | Count or set with verification evidence. |
| `Production Enabled` | Yes | Count or set with production enablement evidence. |
| `Blocked` | Yes | Count or set blocked from next coverage state. |
| `Unknown` | Yes | Count or set that lacks enough evidence. |
| `Primary Blocker Categories` | Yes | Trigger, execution, verification, rollback, authority, consumer, Runtime, evidence, policy, owner extension, production enablement, or other official blocker. |
| `Consumer` | Yes | AEP, OMP, Reality Refinement, Production Maturity, owner, operator, or terminal alternative. |
| `Next Action` | Yes | Existing-owner next action, OMP input, terminal alternative, or `NOT_APPLICABLE`. |

For every Engineering Chain, BDP must calculate Engineering Chain Coverage:

| Field | Required | Meaning |
| --- | ---: | --- |
| `Discovered` | Yes | Chain candidate exists or explicit `NOT_OBSERVED_WITH_REASON`. |
| `Observed` | Yes | Evidence proves at least one real chain segment. |
| `Intent Traced` | Yes | Engineering Intent is traced or explicitly not applicable/unknown. |
| `Behaviour Traced` | Yes | Behaviour Instance is traced or explicit blocker is recorded. |
| `Decision Traced` | Yes | Decision segment is traced or explicit blocker is recorded. |
| `Execution Traced` | Yes | Execution/no-execution path is traced or explicit blocker is recorded. |
| `Verification Traced` | Yes | Verification path is traced or explicit blocker is recorded. |
| `Outcome Traced` | Yes | Actual Outcome is traced or explicit blocker is recorded. |
| `Learning Traced` | Yes | Learning/no-change/terminal alternative is traced or explicit blocker is recorded. |
| `Closure Verified` | Yes | Intent/Outcome comparison is verified or explicit blocker is recorded. |
| `Automation Break` | Yes | `YES`, `NO`, or explicit unknown/not applicable reason. |
| `Implementation Candidate` | Yes | Candidate link, blocker, or `IMPLEMENTATION_NOT_APPLICABLE`. |

Automation Progress must answer:

- how much existing engineering logic is already automated;
- how much requires implementation;
- how much requires existing owner extension;
- how much requires Runtime support;
- how much requires Verification;
- how much requires Rollback / containment / `STOP_SAFE`;
- how much requires Authority resolution;
- how much requires Production Enablement;
- how much is blocked by evidence, consumer, policy, or chain closure.

Coverage classification rules:

1. Coverage cannot promote a Behaviour into Reality.
2. Coverage cannot mark logic production-enabled without production or Production Maturity evidence.
3. Coverage cannot mark logic implemented without implementation evidence.
4. Coverage cannot mark logic verified without verification evidence.
5. Coverage cannot mark logic automation-ready unless Automation Readiness rules pass.
6. Coverage cannot mark logic implementation-ready unless Implementation Readiness rules pass.
7. Coverage must preserve blockers rather than hide them inside aggregate percentages.
8. Coverage must not create OMP missions, mutate backlogs, assign Codex work, or execute implementation.
9. Coverage must report progress of engineering logic, not document count, report count, or raw Behaviour count.

Coverage lifecycle:

```text
Engineering Chain / Behaviour / Automation Candidate / Implementation Candidate / Existing Rule
  -> Resolve Coverage Domain
  -> Resolve Chain Segments
  -> Resolve Current Coverage State
  -> Resolve Evidence
  -> Resolve Blocker or Next State
  -> Resolve Consumer
  -> Resolve Next Action or Terminal Alternative
  -> Record Coverage
  -> Chain Closure
```

Coverage outputs may guide AEP, OMP, owner review, and future implementation planning only after certification and consumer acceptance.

## 23. Engineering Intent Closure Model

Engineering Intent Closure is a BDP analysis result.

It answers:

```text
Does existing engineering logic achieve its own original engineering intent?
```

It is not:

- a new architecture;
- a new owner;
- a new truth source;
- a new goal system;
- a new Runtime state;
- a new Planner state;
- a new OMP state;
- a new production state;
- an authority grant;
- an OMP mission;
- a certified Autonomous Behaviour Gap.

Engineering Intent Closure applies to:

- Behaviour;
- rule;
- gate;
- policy;
- verification;
- rollback;
- Runtime path;
- decision path;
- execution path;
- automation candidate;
- implementation candidate;
- existing engineering condition.

For every applicable item, BDP must resolve:

| Field | Required | Meaning |
| --- | ---: | --- |
| `Initial Intent` | Yes | Original engineering purpose of the logic. |
| `Current State` | Yes | Current observed state or explicit `UNKNOWN`. |
| `Expected State` | Yes | State required for the original intent to be satisfied. |
| `Final State` | Yes | Terminal state reached by the existing logic. |
| `Last Successful Step` | Yes | Last step with evidence before stop or completion. |
| `Stopping Point` | Required when not closed | Exact point where logic stops. |
| `Existing Owner` | Yes | Existing owner of the logic or terminal alternative. |
| `Producer` | Yes | Producer of input, action, or evidence. |
| `Consumer` | Yes | Consumer of output or terminal alternative. |
| `Machine-checkable` | Yes | Predicate or reason it is not machine-checkable. |
| `Verification` | Yes | Verification evidence, blocker, or `NOT_APPLICABLE`. |
| `Rollback` | Yes | Rollback/containment/`STOP_SAFE`, blocker, or `NOT_APPLICABLE`. |
| `Authority` | Yes | Existing authority boundary or blocker. |
| `Reason For Stop` | Required when not closed | Exact stop reason. |

Forward Analysis:

```text
Condition
  -> Behaviour
  -> Decision
  -> Execution
  -> Verification
  -> Rollback
  -> Outcome
  -> Terminal State
```

Backward Analysis:

```text
Expected Goal
  -> Expected Outcome
  -> Required Execution
  -> Required Decision
  -> Required Inputs
  -> Original Condition
```

Intent Closure statuses:

| Status | Meaning |
| --- | --- |
| `INTENT_CLOSED` | Final State fully satisfies Initial Intent with evidence. |
| `INTENT_CLOSED_WITH_LIMITS` | Final State satisfies Initial Intent only inside an explicit existing boundary. |
| `AUTOMATION_BREAK` | Existing engineering logic stops before Initial Intent is achieved. |
| `INTENT_NOT_APPLICABLE` | No independent intent applies or the item is evidence-only, historical, or outside scope. |
| `INTENT_UNKNOWN` | Intent or final state cannot be resolved from available evidence. |

Automation Break means:

```text
Existing engineering logic ends, but its original engineering intent is not achieved.
```

Automation Break classification:

| Break Type | Meaning |
| --- | --- |
| `MANUAL_STEP` | Intent stops at a manual action. |
| `MANUAL_APPROVAL` | Intent stops at manual approval. |
| `MISSING_TRIGGER` | No trigger exists to continue the logic. |
| `MISSING_EXECUTION` | Required execution path is absent. |
| `MISSING_VERIFICATION` | Required verification path is absent. |
| `MISSING_ROLLBACK` | Required rollback/containment/`STOP_SAFE` is absent. |
| `MISSING_RUNTIME` | Runtime support is absent or unavailable through existing owners. |
| `MISSING_CONSUMER` | No consumer or chain closure exists. |
| `MISSING_OWNER_EXTENSION` | Existing owner needs a bounded extension. |
| `MISSING_IMPLEMENTATION` | Required implementation is absent. |
| `NOT_REPRODUCIBLE` | Logic cannot be reproduced deterministically from evidence. |
| `NOT_AUTOMATABLE` | The intent is intentionally or structurally non-automatable. |

Implementation Candidate rule:

- If an Automation Break is caused by `MISSING_IMPLEMENTATION`, BDP must evaluate whether the missing implementation can become an Implementation Candidate through existing owners.
- If the missing implementation requires new architecture, new owner, new rule, new Behaviour, Runtime redesign, Planner redesign, OMP modification, authority expansion, production mutation, or unsupported dependency, it must not become an Implementation Candidate.
- Accepted intent-derived candidates must enter the unified Implementation Candidate Catalogue.
- Rejected intent-derived candidates must be recorded in Automation Break Catalogue with exact reason.

Intent Closure lifecycle:

```text
Behaviour / Rule / Gate / Policy / Verification / Rollback / Runtime Path / Decision Path / Execution Path
  -> Resolve Initial Intent
  -> Build Forward Trace
  -> Build Backward Trace
  -> Resolve Current State
  -> Resolve Expected State
  -> Resolve Final State
  -> Compare Initial Intent With Final State
  -> Intent Closure Decision
  -> Automation Break or Intent Closed
  -> Implementation Candidate Evaluation when applicable
  -> Chain Closure
```

Intent Closure rules:

1. Intent must be derived from existing evidence, canonical knowledge, owner artifacts, implementation, runtime, decision, policy, verification, rollback, reports, Function Graph, or SYSTEM_MAP.
2. Intent must not be invented from desired behaviour.
3. Forward Trace and Backward Trace must be deterministic or explicitly `INTENT_UNKNOWN`.
4. Final State must be evidence-backed or explicitly `UNKNOWN`.
5. `INTENT_CLOSED` requires Initial Intent and Final State alignment.
6. `AUTOMATION_BREAK` requires a specific Stopping Point and Reason For Stop.
7. Automation Break must not be treated as a certified Autonomous Behaviour Gap.
8. Automation Break must not create OMP missions, mutate backlog, assign Codex work, execute implementation, mutate Runtime, expand authority, mutate production, or update Reality automatically.

Intent Closure engineering report requirements:

- total Intent records reviewed;
- count of `INTENT_CLOSED`;
- count of `INTENT_CLOSED_WITH_LIMITS`;
- count of `AUTOMATION_BREAK`;
- count of `INTENT_UNKNOWN`;
- count of `INTENT_NOT_APPLICABLE`;
- primary stop reasons;
- Automation Break classification totals;
- new intent-derived Implementation Candidates;
- rejected intent-derived candidate reasons;
- final `PASS` / `HOLD` verdict.

## 24. Validation Model

Validation sequence:

```text
Evidence Validation
  -> Behaviour Truth Hierarchy Validation
  -> Behaviour Identity Validation
  -> Behaviour Traceability Validation
  -> Reality Validation
  -> Behaviour Independence Validation
  -> Optional Surface Lens Validation
  -> Behaviour Completeness Validation
  -> Behaviour Evolution Validation
  -> Automation Readiness Validation
  -> Implementation Readiness Validation
  -> Engineering Intent Closure Validation
  -> Engineering Logic Coverage Validation
  -> No Hypothetical Behaviour Review
  -> Producer / Consumer Validation
  -> Verification Path Validation
  -> Learning / Continuation Validation
  -> Forbidden Use Validation
```

Validation outcomes:

| Outcome | Meaning |
| --- | --- |
| `PASS` | Behaviour may proceed to merge/deduplication. |
| `PASS_WITH_MINOR_RISKS` | Behaviour may proceed with explicit risk. |
| `HOLD` | Missing required proof; no Reality admission. |
| `FAIL` | Contradiction, no evidence, duplicate owner, Runtime/OMP/authority violation, or hypothetical behaviour. |

Surface Lens Validation rules:

- Surface Lens validation cannot admit a Behaviour by itself.
- A Behaviour with a valid Surface Lens must still pass evidence, independence, producer/consumer, verification, learning, and forbidden-use validation.
- A Behaviour without Surface Lens may still pass when surface grouping is `NOT_APPLICABLE`.
- A conceptual or rejected Surface Lens must not be used to justify a Behaviour, Discovery Pass, Reality update, or architecture claim.
- Surface Lens may only improve navigation, coverage checking, and explanation of related Behaviours.

Behaviour Identity Validation rules:

- Every candidate must have Behaviour Definition Identity, Behaviour Instance Identity, and Identity Disposition before Reality admission.
- Identity may be resolved directly from the candidate or deterministically through official BDP/AEP/Reality/Function Graph/Canonical Knowledge/owner artifacts.
- Name, file, function, class, or document match must not be used as sufficient identity proof.
- Name, file, function, class, or document difference must not be used as sufficient proof of a new Behaviour.
- Merge/deduplication may use identity signature only after evidence and identity validation pass.
- `MANUAL_REVIEW_IDENTITY_AMBIGUOUS` and `DUPLICATE_BEHAVIOUR_REJECTED` cannot enter Reality as independent Behaviours.

Behaviour Truth Hierarchy Validation rules:

- Every evidence record must have a truth level.
- The strongest available truth level for the run scope must be used or explicitly marked unavailable.
- Lower-level evidence must not override higher-level contradictory observed production/runtime evidence.
- Architecture-only, hypothesis-only, synthetic, historical, or superseded evidence must not prove current Behaviour.

Behaviour Traceability Validation rules:

- Every accepted Behaviour Candidate must have `TRACE_COMPLETE` or `TRACE_COMPLETE_WITH_UNKNOWNS`.
- `TRACE_PARTIAL_HOLD` blocks Reality admission.
- `TRACE_FAIL` fails the candidate.
- Traceability must include explicit consumer path and terminal alternative.

Behaviour Completeness Validation rules:

- Every BDP run must produce a Behaviour Completeness status.
- `COMPLETE_FOR_SCOPE` may proceed.
- `COMPLETE_WITH_EXPLICIT_UNKNOWNS` may proceed with recorded risks.
- `PARTIAL_HOLD` blocks certification.
- `INCOMPLETE_FAIL` fails the BDP run.

Behaviour Evolution Validation rules:

- Every candidate must have an Evolution Disposition or `NOT_APPLICABLE`.
- Evolution must preserve identity lineage, evidence lineage, owner/consumer lineage, and Reality lineage.
- Versioned or superseded Behaviour must be represented as lineage, not duplicate Behaviour.
- Evolution affecting canonical knowledge must route to existing Knowledge Evolution.

Discovery Economy Validation rules:

- Every BDP run or proposed BDP run must record a Discovery Economy outcome.
- `DISCOVERY_NOT_REQUIRED_REUSE_EVIDENCE` is valid only when sufficiency conditions are documented.
- `TARGETED_DISCOVERY_REQUIRED` must name the minimal Discovery Passes required.
- `FULL_DISCOVERY_REQUIRED` must name why targeted discovery is insufficient.
- `DISCOVERY_HOLD` stops execution until the missing input or authority is resolved.

Engineering Chain Validation rules:

- Every BDP run must produce Engineering Chain Catalogue or explicit `NOT_APPLICABLE`.
- Every discovered Engineering Chain must include Engineering Intent, Trigger, Condition, Behaviour Instance, Decision, Execution, Verification, Outcome, Learning, and Intent Closure segments or explicit blocker/unknown/not-applicable reason.
- Every Engineering Chain must include Forward Walk, Backward Walk, Middle-Out Walk, and Producer -> Consumer Walk evidence or explicit blocker.
- Every Engineering Chain must include Chain State and Terminal State.
- Chain Closure requires evidence that Verified Outcome satisfies Engineering Intent, or an accepted terminal alternative.
- `AUTOMATION_BREAK` requires evidence that the chain stopped before Engineering Intent was achieved.
- Engineering Chain must not replace Behaviour identity; Behaviour Instance must remain traceable inside the chain.
- Engineering Chain validation must use LOCKED_KNOWLEDGE Engineering Chain Model and must not redefine chain states or chain semantics.
- Engineering Chain validation must not create new Engineering Entity, Architecture, owner, Runtime, Planner, OMP Mission, backlog mutation, Codex assignment, Reality update, locked knowledge mutation, authority expansion, production mutation, or implementation execution.

Automation Readiness Validation rules:

- Every accepted or held Behaviour Candidate must have Automation Readiness status or explicit `NOT_APPLICABLE`.
- `AUTOMATION_READY` requires owner, producer, consumer, input data, trigger, machine-checkable predicate, deterministic decision rule, execution or explicit no-execution path, authority boundary, verification path, rollback/containment/`STOP_SAFE` where applicable, terminal state, and chain closure.
- `AUTOMATION_READY_WITH_LIMITS` must record the exact existing limit.
- `MACHINE_CHECKABLE_ONLY` must not be treated as executable.
- `OBSERVATION_ONLY` must not be treated as decision or execution.
- `MANUAL_GATE_ONLY` must not be treated as automated.
- Blocked statuses must name the missing or unsafe element.
- No automation readiness result may expand authority, create Runtime, create Planner, create OMP mission, mutate production, move users, or bypass verification/rollback/consumer closure.

Implementation Readiness Validation rules:

- Every accepted or held Behaviour Candidate must have Implementation Readiness status or explicit `IMPLEMENTATION_NOT_APPLICABLE`.
- `IMPLEMENTATION_READY` requires existing owner, producer, consumer, implementation scope, dependencies, verification, rollback/containment/`STOP_SAFE` where applicable, authority boundary, OMP consumer path, Codex readiness, and chain closure.
- `IMPLEMENTATION_BLOCKED` must name the exact blocker.
- `IMPLEMENTATION_NOT_APPLICABLE` must explain why implementation is not required or outside scope.
- Implementation Candidate must not require new architecture, new Behaviour, new rule, new owner, Runtime redesign, Planner redesign, OMP modification, authority expansion, production mutation, user movement, or automatic execution.
- Codex readiness must not be treated as Codex assignment, permanent Codex dependency, OMP approval, or execution permission.

Implementation Candidate Classification Validation rules:

- Every Implementation Candidate Instance must have exactly one Primary Class from the official Implementation Candidate Classification Model.
- Every Implementation Candidate Instance must have Secondary Classes recorded as zero or more official classes, or explicit `NONE`.
- Every Implementation Candidate Instance must have Execution Depth, Candidate Coverage Matrix Position, and Class Coverage Status.
- Primary Class must be selected by the deterministic Primary Class Decision Rule.
- Secondary Classes must not cause double-counting in Execution Certification or Candidate Coverage Matrix.
- A document, report, owner, model, rule, section, Function Graph node, canonical source, or context artifact must not be treated as an Implementation Candidate Class instance.
- If no official class fits, BDP must emit `CANDIDATE_CLASS_UNKNOWN_WITH_REASON` and must not emit `IMPLEMENTATION_READY`.
- Candidate Coverage Matrix cells must be evidence-backed and must not be filled by context artifacts alone.
- Candidate Classification must not duplicate OMP admission, OMP Candidate Identity, Action Class authority, Mission Classification, or Capability Classification.

Candidate Coverage Progress Projection Validation rules:

- Every Candidate Coverage Matrix cell must have a computed Progress Projection or explicit `NOT_APPLICABLE`.
- Progress Projection must reuse the same Candidate Coverage Matrix cell and must not create a separate Progress Matrix.
- Progress Projection must use only existing Candidate Coverage Matrix statuses.
- Every projection record must include Current Status, Next Status, Remaining Path, blockers, Estimated Existing Work, and Terminal Alternative.
- `Next Status` must follow the legal status progression unless the cell is `NOT_APPLICABLE` or a legal terminal alternative applies.
- `Remaining Path` must be derived from existing owners, consumers, verification, rollback, authority, runtime, production, Engineering Chain Closure, and Intent Closure evidence.
- A missing path must first be classified by existing blocker type before `FUNDAMENTAL_ARCHITECTURE_GAP` may be recorded.
- Engineering Value, Coverage Gain, Production Gain, Automation Gain, Chain Closure Gain, and Verification Gain must be computed from evidence-backed deltas, not manual priority.
- Depends On, Unblocks, Critical Path, Dependency Depth, Root Cause, and Final Consumer must be computed from Engineering Chain Walk and Producer -> Consumer evidence only.
- BDP must not create Dependency Graph, Progress Graph, Navigation Graph, Relationship Graph, Dependency Model, or new relationship entity.
- Root Cause must be the earliest evidence-backed unresolved blocker in the Backward Walk; if not determinable, BDP must record `ROOT_CAUSE_NOT_DETERMINED_WITH_REASON`.
- Critical Path must be derived from unresolved Engineering Chain paths to Production Certification, downstream unblock count, or sole Final Consumer path.
- System Engineering Value must include Engineering Value, Unblocked Candidate Count, Critical Path Impact, and Root Cause Impact.
- System Engineering Value must not become OMP admission, sequencing, mission creation, implementation priority, or backlog mutation.
- Overall Coverage, Overall Automation Coverage, Overall Implementation Coverage, Overall Verification Coverage, Overall Production Coverage, Overall Chain Closure, and Overall Engineering Maturity must be computed from Candidate Coverage Matrix cells and supporting coverage evidence.
- BDP project-level maturity indicators must not overwrite canonical Engineering Maturity or Production Maturity.
- Progress Projection must not create OMP missions, mutate OMP state, mutate backlogs, assign Codex work, mutate Runtime, expand authority, mutate production, or update canonical maturity.

Engineering Intent Closure Validation rules:

- Every applicable Behaviour, rule, gate, policy, verification, rollback, Runtime path, decision path, execution path, Automation Candidate, Implementation Candidate, and existing engineering condition must have Intent Closure Status or explicit `INTENT_NOT_APPLICABLE`.
- Every Intent Closure record must include Initial Intent, Current State, Expected State, Final State, Existing Owner, Producer, Consumer, and evidence.
- Every non-closed Intent must include Last Successful Step, Stopping Point, Reason For Stop, and Automation Break classification.
- Forward Trace and Backward Trace must be present or explicitly `INTENT_UNKNOWN`.
- `INTENT_CLOSED` requires evidence that Final State satisfies Initial Intent.
- `AUTOMATION_BREAK` requires evidence that existing logic ends before Initial Intent is achieved.
- Intent-derived Implementation Candidates must pass Implementation Readiness validation before entering the unified Implementation Candidate Catalogue.
- Intent Closure must not invent desired behaviour, create new goals, create OMP missions, mutate backlog, assign Codex work, execute implementation, mutate Runtime, expand authority, mutate production, update Reality, or certify Autonomous Behaviour Gaps.

Engineering Logic Coverage Validation rules:

- Every applicable Behaviour Candidate, Automation Candidate, Implementation Candidate, and non-behaviour engineering rule must have a Coverage State or explicit `NOT_APPLICABLE`.
- Every coverage record must identify Coverage Domain, evidence, blocker or next state, consumer, and next action or terminal alternative.
- `PRODUCTION_ENABLED` requires production or Production Maturity evidence.
- `IMPLEMENTED` requires implementation evidence.
- `AUTOMATED` requires evidence that the logic is automatically evaluated or executed through an existing owner path.
- `VERIFIED` requires verification evidence.
- `AUTOMATION_READY` and `IMPLEMENTATION_READY` must be derived from their official readiness models.
- `AUTOMATED` must not be inferred from automation readiness alone.
- `BLOCKED` must name the exact blocker category.
- `UNKNOWN` must remain explicit and must not be counted as ready, implemented, automated, verified, or production-enabled.
- Coverage must not create OMP missions, mutate OMP state, update the official Implementation Backlog, assign Codex work, mutate Runtime, expand authority, mutate production, or update Reality automatically.

## 25. Reality Refinement Model

BDP may produce a Reality Refinement Proposal only after validation.

The proposal must classify every candidate:

- add to Reality;
- update existing Behaviour;
- merge with existing Behaviour;
- reject as hypothetical;
- reject as internal step;
- reject as still composite;
- mark unavailable / unknown;
- route contradiction to existing owner.

The proposal is not an update. It is an input for a later operator-approved Reality refinement.

The proposal must also classify Automation Readiness findings:

- add automation readiness evidence to the Behaviour;
- mark existing automation-ready logic as `AUTOMATION_READY`;
- mark bounded automation-ready logic as `AUTOMATION_READY_WITH_LIMITS`;
- mark logic as machine-checkable only;
- mark observation-only logic;
- mark manual-gated logic;
- record automation blocker and required existing-owner extension;
- produce OMP-ready automation input proposal where certified;
- mark automation finding `NOT_APPLICABLE`.

Automation Readiness findings do not update Current Autonomous Behaviour Reality automatically and do not create OMP missions.

The proposal must also classify Engineering Chain findings:

- record Engineering Chain State;
- record Forward Walk, Backward Walk, Middle-Out Walk, and Producer -> Consumer Walk status;
- record Intent Closure;
- record Automation Break when the chain is not closed;
- record Implementation Readiness and Implementation Candidate when the break is caused by bounded missing implementation;
- record Terminal State or terminal alternative.

Engineering Chain findings do not update Current Autonomous Behaviour Reality automatically, do not create new Engineering Entity, do not create OMP missions, do not assign Codex work, do not mutate Runtime, do not expand authority, do not mutate production, do not mutate locked knowledge, and do not execute implementation.

The proposal must also classify Implementation Readiness findings:

- mark existing logic as `IMPLEMENTATION_READY`;
- mark blocked logic as `IMPLEMENTATION_BLOCKED`;
- mark non-applicable logic as `IMPLEMENTATION_NOT_APPLICABLE`;
- record implementation blocker and required existing-owner extension where applicable;
- produce OMP Implementation Input where certified;
- produce Codex Implementation Input where scoped;
- produce Engineering Automation Backlog catalogue where useful.

Implementation Readiness findings do not update OMP, do not update the official Implementation Backlog, do not create OMP missions, do not assign Codex work, and do not execute implementation.

The proposal must also classify Engineering Intent Closure findings:

- mark intent as `INTENT_CLOSED`;
- mark bounded closure as `INTENT_CLOSED_WITH_LIMITS`;
- record `AUTOMATION_BREAK`;
- record `INTENT_UNKNOWN`;
- record `INTENT_NOT_APPLICABLE`;
- produce intent-derived Implementation Candidate only after Implementation Readiness validation;
- record rejected intent-derived candidate with exact reason.

Engineering Intent Closure findings do not update Current Autonomous Behaviour Reality automatically, do not create certified Autonomous Behaviour Gaps, do not update OMP, do not update the official Implementation Backlog, do not create OMP missions, do not assign Codex work, and do not execute implementation.

The proposal must also classify Engineering Logic Coverage findings:

- record current coverage state;
- record coverage domain;
- record blocker category or next state;
- record consumer and next action;
- record Engineering Logic Automation Coverage for the declared scope.

Engineering Logic Coverage findings do not update Current Autonomous Behaviour Reality automatically, do not update OMP, do not update Production Maturity, do not update production state, do not create OMP missions, do not assign Codex work, and do not execute implementation.

## 26. Merge / Deduplication Model

Merge is behaviour-level, not text-level.

Merge is allowed only when candidates represent the same engineering behaviour with compatible:

- Situation;
- Decision;
- Producer;
- Consumer;
- Verification;
- Learning / continuation;
- Runtime path;
- Policy / law;
- Evidence provenance.

Merge must preserve all evidence records.

Merge is forbidden when identity signatures differ, even if names or implementation locations match.

Merge is required to reuse an existing Behaviour Definition when identity signatures match, even if names, file paths, implementation locations, or reports differ.

## 27. Certification Model

Every BDP run must perform:

- Architecture Review;
- World Research Review;
- Reuse Review;
- Duplication Review;
- Discovery Review;
- Discovery Economy Review;
- Evidence Review;
- Behaviour Truth Hierarchy Review;
- Reality Review;
- Behaviour Completeness Review;
- Behaviour Traceability Review;
- Behaviour Identity Review;
- Behaviour Evolution Review;
- Behaviour Independence Review;
- Engineering Chain Review;
- Engineering Chain Reuse Review;
- Chain Walk Review;
- Chain Coverage Review;
- Chain Traceability Review;
- Automation Readiness Review;
- Implementation Readiness Review;
- Candidate Classification Review;
- Candidate Coverage Review;
- Coverage Projection Review;
- Progress Projection Review;
- Critical Path Review;
- Root Cause Review;
- Engineering Value Review;
- System Value Review;
- Project Maturity Review;
- No Gap Review;
- Execution Certification Compatibility Review;
- Implementation Scope Review;
- Implementation Dependency Review;
- Intent Review;
- Intent Closure Review;
- Forward Trace Review;
- Backward Trace Review;
- Automation Break Review;
- Engineering Coverage Review;
- Automation Coverage Review;
- Implementation Coverage Review;
- Production Coverage Review;
- Progress Review;
- Machine Checkability Review;
- Trigger Review;
- Execution Path Review;
- No Hypothetical Behaviour Review;
- Producer / Consumer Review;
- Verification Review;
- Rollback / STOP_SAFE Review;
- Authority Boundary Review;
- Manual Dependency Review;
- OMP Consumer Review;
- Codex Readiness Review;
- Engineering Automation Review;
- No New Graph Review;
- No New Architecture Review;
- No New Entity Review;
- No New Runtime Review;
- No Authority Expansion Review;
- Chain Closure Review;
- Quality Review;
- Self Review.

Certification verdicts:

| Verdict | Meaning |
| --- | --- |
| `BEHAVIOUR_DISCOVERY_PASS` | Discovery output is ready for consumer acceptance. |
| `BEHAVIOUR_DISCOVERY_PASS_WITH_MINOR_RISKS` | Output is usable with recorded risks. |
| `BEHAVIOUR_DISCOVERY_HOLD` | Output cannot be consumed until blockers are resolved. |
| `BEHAVIOUR_DISCOVERY_FAIL` | Output violates program law. |

## 28. Outputs

Every proposed BDP run must produce a Discovery Economy Decision.

If the decision is `DISCOVERY_NOT_REQUIRED_REUSE_EVIDENCE`, required outputs are:

- Discovery Economy Decision;
- reuse evidence summary;
- Engineering Report;
- Chain Closure status.

If the decision allows Discovery execution, required outputs are:

| Output | Consumer |
| --- | --- |
| Behaviour Discovery Report | Operator, AEP, Reality Refinement. |
| Discovery Economy Decision | Discovery Pass Plan and Engineering Report. |
| Discovery Pass Registry | Engineering report and future repeatability. |
| Evidence Corpus | Validation and certification. |
| Engineering Chain Catalogue | Certification, AEP, BDP repeatability, OMP consumer review after acceptance. |
| Engineering Chain Coverage | Certification, AEP/OMP/operator progress review, and future Reality/implementation planning. |
| Engineering Chain Walk | Chain Walk Review, Intent Closure Review, Automation Break Review, and consumer acceptance. |
| Engineering Chain Traceability | Certification, producer/consumer validation, and future repeatability. |
| Engineering Chain Closure Matrix | Closure Review, OMP consumer review, and implementation readiness review. |
| Engineering Chain Automation Break Matrix | Automation Break Review, Implementation Readiness Review, and OMP blocker input after acceptance. |
| Engineering Chain Implementation Candidates | OMP, Codex preparation, and future implementation owner review after acceptance. |
| Observed Behaviour Candidate Registry | Reality Refinement Proposal. |
| Behaviour Identity Resolution Matrix | Validation, merge/deduplication, and Reality Refinement Proposal. |
| Behaviour Truth Hierarchy Matrix | Validation and Reality Refinement Proposal. |
| Behaviour Completeness Matrix | Certification and Reality Refinement Proposal. |
| Behaviour Traceability Matrix | Certification and consumer acceptance. |
| Behaviour Evolution Disposition Matrix | Reality Refinement Proposal and future Reality lineage. |
| Behaviour Validation Matrix | Certification and refinement. |
| Reality Validation Matrix | Certification and refinement. |
| Merge / Deduplication Map | Reality Refinement Proposal. |
| Hypothesized / Rejected Behaviour Catalogue | Prevents false Reality admission. |
| Automation Readiness Matrix | Certification, Reality Refinement Proposal, and OMP-ready automation input. |
| Automation Candidate Catalogue | OMP, future Phase 3, and implementation owner review after acceptance. |
| Automation Blocker Matrix | OMP, Phase 3 preparation, and existing owner extension planning. |
| Manual Dependency Matrix | OMP and Phase 3 preparation. |
| Machine-Checkable Predicate Inventory | Validation, certification, and future implementation owner review. |
| Trigger / Execution / Verification / Rollback Coverage Matrix | Automation Readiness Review, OMP Consumer Review, and Phase 3 preparation. |
| OMP Automation Input Proposal | OMP-only consumer path after certification and acceptance. |
| Implementation Candidate Catalogue | OMP, Codex preparation, future implementation owner review after acceptance. |
| Implementation Candidate Classification Matrix | Candidate Classification Review, OMP consumer review, Execution Certification, and future candidate repeatability. |
| Candidate Coverage Matrix | Candidate Coverage Review, Execution Certification, AEP/OMP/operator progress review, and future automation planning. Includes Current View and computed Progress Projection. |
| Candidate Coverage Progress Projection | Computed projection of Candidate Coverage Matrix cells; not a separate Progress Matrix and not a new truth source. |
| Implementation Blocker Matrix | OMP, owner-extension planning, and future implementation readiness review. |
| Implementation Readiness Matrix | Certification, OMP consumer review, Codex readiness review. |
| OMP Implementation Input | OMP-only consumer path after certification and acceptance. |
| Codex Implementation Input | Codex-ready scoped input for later OMP/operator-approved implementation. |
| Engineering Automation Backlog | BDP catalogue of implementation-ready or implementation-blocked engineering automation candidates; not the official OMP Implementation Backlog. |
| Intent Closure Matrix | Certification, implementation readiness review, and engineering progress analysis. |
| Intent Coverage Matrix | Certification, AEP/OMP/operator progress review, and future Reality/implementation planning. |
| Automation Break Catalogue | OMP, owner-extension planning, and future Phase 3 preparation after acceptance. |
| Automation Break Matrix | Automation Break Review, Implementation Readiness Review, and Engineering Logic Coverage. |
| Intent Trace | Traceability, certification, and consumer acceptance. |
| Forward Trace | Intent Closure Review and Automation Break Review. |
| Backward Trace | Intent Closure Review and Automation Break Review. |
| Engineering Logic Coverage Matrix | Certification, AEP/OMP/operator progress review, and future Reality/implementation planning. |
| Automation Progress Matrix | Automation Coverage Review, OMP consumer review, and Phase 3 preparation. |
| Implementation Progress Matrix | Implementation Coverage Review, OMP consumer review, and owner-extension planning. |
| Production Enablement Matrix | Production Coverage Review, Production Maturity consumer review, and AEP/OMP progress review. |
| Engineering Automation Coverage Report | Operator, AEP, OMP, and Engineering Reports as the certified progress view. |
| Reality Refinement Proposal | Operator-approved future Reality update. |
| Certification Report | Consumer acceptance. |
| Engineering Report | OMP/CPS/operator traceability if accepted. |

When Surface Lens grouping is used, the Behaviour Discovery Report may contain a Surface Lens coverage section. This is not a separate artifact, owner, entity, or storage layer.

## 29. Consumers

Valid consumers:

- operator;
- AEP Phase 2;
- future Reality Refinement task;
- Current Autonomous Behaviour Reality owner after acceptance;
- AEP Phase 3 only after operator command and accepted Reality;
- OMP only after certified/accepted consumer path;
- OMP for Engineering Chain findings only as certified relationship/closure/input evidence after acceptance, never as automatically created mission or backlog update;
- OMP for Automation Readiness findings only as certified implementation input proposal, never as automatically created mission;
- OMP for Implementation Candidates only as certified implementation input, never as automatically created mission or official backlog update;
- OMP for Automation Break findings only as certified blocker and implementation input after acceptance, never as automatically created mission or certified Gap;
- OMP for Engineering Logic Coverage only as certified progress and blocker input, never as automatically created mission or backlog update;
- Production Maturity for Production Enablement findings only as evidence input, never as automatic maturity update;
- Codex only as later OMP/operator-approved implementation assistant, never as autonomous production dependency;
- CPS only for volatile state if accepted by the appropriate owner;
- Engineering Reports as evidence.

Invalid consumers:

- Runtime;
- Planner;
- direct production execution;
- authority expansion;
- automatic OMP mission creation;
- automatic automation execution;
- automation authority expansion;
- automatic implementation execution;
- automatic Codex assignment;
- official OMP Implementation Backlog mutation by BDP;
- locked knowledge mutation;
- architecture mutation.

## 30. Chain Closure

Every BDP output must have:

- Producer;
- Consumer;
- Consumption Status;
- Consumption Evidence;
- Next Action;
- Terminal Alternative.

Consumption statuses:

- `NOT_PRODUCED`;
- `PRODUCED`;
- `ASSIGNED`;
- `CONSUMED`;
- `CONFIRMED`;
- `CHAIN_CLOSED`;
- `TERMINAL_ACCEPTED`;
- `TERMINAL_REJECTED`;
- `TERMINAL_HOLD`;
- `TERMINAL_IMPOSSIBLE`.

A BDP run is not chain-closed merely because an output exists.

Official closure:

```text
Output Produced
  -> Consumer Assigned
  -> Consumer Consumed
  -> Consumption Confirmed
  -> Next Action Recorded
  -> Chain Closed
```

If a consumer does not confirm consumption, the output remains `CHAIN_HOLD`.

Engineering Chain outputs are chain-closed only when:

- Engineering Chain Catalogue is produced or explicitly `NOT_APPLICABLE`;
- Engineering Chain Coverage is produced or explicitly `NOT_APPLICABLE`;
- Engineering Chain Walk is produced or explicitly `NOT_APPLICABLE`;
- Engineering Chain Traceability is produced or explicitly `NOT_APPLICABLE`;
- Engineering Chain Closure Matrix is produced or explicitly `NOT_APPLICABLE`;
- Engineering Chain Automation Break Matrix is produced or explicitly `NOT_APPLICABLE`;
- Engineering Chain Implementation Candidates are produced or explicitly `NOT_APPLICABLE`;
- every chain has Engineering Intent or explicit `INTENT_NOT_APPLICABLE`;
- every chain has Trigger, Condition, Behaviour Instance, Decision, Execution, Verification, Outcome, Learning, and Intent Closure segments traced or explicitly blocked/unknown/not applicable;
- every chain has Forward Walk, Backward Walk, Middle-Out Walk, and Producer -> Consumer Walk evidence or explicit blocker;
- every chain has Chain State and Terminal State or explicit unknown/blocked reason;
- no Engineering Chain output creates new Engineering Entity, Architecture, owner, Runtime, Planner, OMP Mission, official backlog mutation, Codex assignment, Reality update, locked knowledge mutation, authority expansion, production mutation, or implementation execution.

Automation Readiness outputs are chain-closed only when:

- each automation candidate has existing owner, producer, consumer, and source;
- each readiness status has evidence;
- each blocker has a blocking reason and existing owner extension or terminal alternative;
- OMP Automation Input Proposal has OMP as consumer or explicit `NOT_APPLICABLE`;
- no Runtime, OMP, authority, production, user, locked knowledge, or architecture mutation occurred.

Implementation Readiness outputs are chain-closed only when:

- each Implementation Candidate has existing owner, producer, consumer, implementation scope, dependencies, verification, rollback/containment/`STOP_SAFE` where applicable, authority boundary, OMP consumer, and Codex readiness;
- each Implementation Candidate has exactly one Primary Class, Secondary Classes or `NONE`, Execution Depth, Candidate Coverage Matrix Position, and Class Coverage Status;
- Implementation Candidate Classification Matrix and Candidate Coverage Matrix are produced or explicitly `NOT_APPLICABLE`;
- Candidate Coverage Progress Projection is computed from the same Candidate Coverage Matrix cells or explicitly `NOT_APPLICABLE`;
- each projected cell has Current Status, Next Status, Remaining Path, blockers, Estimated Existing Work, and Terminal Alternative;
- each projected cell has Depends On, Unblocks, Critical Path, Dependency Depth, Root Cause, and Final Consumer computed from Engineering Chain Walk or explicit `NOT_APPLICABLE`;
- each Engineering Value component is computed from evidence-backed delta or explicitly `NOT_APPLICABLE`;
- each System Engineering Value component is computed from Engineering Chain dependency projection or explicitly `NOT_APPLICABLE`;
- each Candidate Coverage Matrix cell is evidence-backed and does not count documents, owners, reports, models, rules, sections, Function Graph nodes, canonical sources, or context artifacts as Candidate Instances;
- each implementation blocker has exact blocking reason and existing-owner extension or terminal alternative;
- OMP Implementation Input has OMP as consumer or explicit `NOT_APPLICABLE`;
- Codex Implementation Input is scoped and marked as later OMP/operator-approved implementation input only;
- Engineering Automation Backlog is explicitly marked as BDP catalogue, not official OMP backlog;
- no OMP mission, OMP state update, official backlog mutation, Codex assignment, Runtime mutation, authority expansion, production mutation, user movement, locked knowledge mutation, or architecture mutation occurred.

Engineering Intent Closure outputs are chain-closed only when:

- each Intent Closure record has Initial Intent, Current State, Expected State, Final State, owner, producer, consumer, evidence, and closure status;
- each non-closed Intent has Last Successful Step, Stopping Point, Reason For Stop, and Automation Break classification;
- Intent Closure Matrix, Intent Coverage Matrix, Automation Break Catalogue, Automation Break Matrix, Intent Trace, Forward Trace, and Backward Trace are produced or explicitly `NOT_APPLICABLE`;
- intent-derived Implementation Candidates enter the unified Implementation Candidate Catalogue only after Implementation Readiness validation;
- rejected intent-derived candidates are recorded with exact reason;
- no Automation Break is treated as certified Autonomous Behaviour Gap;
- no Intent Closure output creates OMP missions, mutates OMP state, updates the official Implementation Backlog, assigns Codex work, mutates Runtime, expands authority, mutates production, updates Reality, locked knowledge, or architecture.

Engineering Logic Coverage outputs are chain-closed only when:

- each coverage record has Coverage Domain, Coverage State, evidence, consumer, next action or terminal alternative, and chain closure status;
- each blocked coverage item has an exact blocker category;
- each `UNKNOWN` item remains explicit and is not counted as ready, implemented, automated, verified, or production-enabled;
- Engineering Logic Coverage Matrix, Automation Progress Matrix, Implementation Progress Matrix, Production Enablement Matrix, and Engineering Automation Coverage Report are produced or explicitly `NOT_APPLICABLE`;
- Overall Coverage, Overall Automation Coverage, Overall Implementation Coverage, Overall Verification Coverage, Overall Production Coverage, Overall Chain Closure, and Overall Engineering Maturity are computed or explicitly `NOT_APPLICABLE`;
- BDP project-level maturity indicators remain navigation metrics and do not mutate canonical Engineering Maturity or Production Maturity;
- no coverage output creates OMP missions, mutates OMP state, updates the official Implementation Backlog, assigns Codex work, mutates Runtime, expands authority, mutates production, updates Production Maturity, updates Reality, locked knowledge, or architecture.

## 31. Completion Criteria

A proposed BDP run stopped by `DISCOVERY_NOT_REQUIRED_REUSE_EVIDENCE` is complete only when:

- Discovery Economy Decision is recorded;
- reuse evidence is recorded;
- consumer/next action is recorded;
- chain closure status is recorded;
- no Discovery Pass was executed unnecessarily.

A BDP run that proceeds beyond the Discovery Economy Decision is complete only when:

- Discovery Economy Decision is recorded;
- all required Discovery Passes have a pass result or justified `NOT_APPLICABLE`;
- no pass exists without necessity proof;
- Evidence Corpus is complete for the run scope;
- Engineering Chain Catalogue is produced or explicitly `NOT_APPLICABLE`;
- Engineering Chain Coverage is produced or explicitly `NOT_APPLICABLE`;
- Engineering Chain Walk is produced or explicitly `NOT_APPLICABLE`;
- Engineering Chain Traceability is produced or explicitly `NOT_APPLICABLE`;
- Engineering Chain Closure Matrix is produced or explicitly `NOT_APPLICABLE`;
- Engineering Chain Automation Break Matrix is produced or explicitly `NOT_APPLICABLE`;
- Engineering Chain Implementation Candidates are produced or explicitly `NOT_APPLICABLE`;
- every discovered Engineering Chain has Engineering Intent, Trigger, Condition, Behaviour Instance, Decision, Execution, Verification, Outcome, Learning, and Intent Closure traced or explicitly blocked/unknown/not applicable;
- every discovered Engineering Chain has Forward Walk, Backward Walk, Middle-Out Walk, Producer -> Consumer Walk, Chain State, Terminal State, and Intent Closure status;
- Behaviour is preserved as mandatory Chain stage and is not replaced by Chain labels;
- every evidence record has source, observed fact, producer/consumer if known, truth level, traceability path, confidence, and forbidden use;
- every Observed Behaviour Candidate has validation status;
- every Observed Behaviour Candidate has Behaviour Definition Identity, Behaviour Instance Identity, and Identity Disposition or an explicit `MANUAL_REVIEW_IDENTITY_AMBIGUOUS`;
- every Observed Behaviour Candidate has Truth Level, Traceability Path, Completeness Role, and Evolution Disposition or explicit `NOT_APPLICABLE`;
- every Observed Behaviour Candidate has Automation Readiness status or explicit `NOT_APPLICABLE`;
- every Observed Behaviour Candidate has Implementation Readiness status or explicit `IMPLEMENTATION_NOT_APPLICABLE`;
- every applicable Behaviour, rule, gate, policy, verification, rollback, Runtime path, decision path, execution path, Automation Candidate, Implementation Candidate, and existing engineering condition has Intent Closure Status or explicit `INTENT_NOT_APPLICABLE`;
- every applicable Observed Behaviour Candidate, Automation Candidate, Implementation Candidate, and existing engineering rule has Coverage State or explicit `NOT_APPLICABLE`;
- strongest available truth level for each accepted Behaviour is used or explicitly unavailable;
- every accepted Behaviour has `TRACE_COMPLETE` or `TRACE_COMPLETE_WITH_UNKNOWNS`;
- Behaviour Completeness status is `COMPLETE_FOR_SCOPE` or `COMPLETE_WITH_EXPLICIT_UNKNOWNS`;
- no hidden Behaviour Space remains undispositioned inside the declared scope;
- no Behaviour is created solely from name, file, function, class, document, or repository location;
- no Behaviour is merged solely from name, file, function, class, document, or repository location;
- existing Behaviour Definitions are reused when identity signatures match;
- Behaviour evolution preserves identity, evidence, owner/consumer, and Reality lineage;
- automation readiness preserves existing owner, producer, consumer, authority boundary, terminal state, and chain closure;
- `AUTOMATION_READY` and `AUTOMATION_READY_WITH_LIMITS` findings have machine-checkable predicate, input data, trigger, deterministic decision rule, execution or explicit no-execution path, verification path, rollback/containment/`STOP_SAFE` where applicable, terminal state, and OMP consumer path or terminal alternative;
- blocked automation findings have a blocking reason and required existing owner extension or terminal alternative;
- `MACHINE_CHECKABLE_ONLY`, `OBSERVATION_ONLY`, and `MANUAL_GATE_ONLY` findings are not treated as executable automation;
- OMP Automation Input Proposal is produced or explicitly `NOT_APPLICABLE`;
- `IMPLEMENTATION_READY` findings have existing owner, producer, consumer, implementation scope, dependencies, verification, rollback/containment/`STOP_SAFE` where applicable, authority boundary, OMP consumer, Codex readiness, and chain closure;
- every Implementation Candidate Instance has exactly one Primary Class, Secondary Classes or `NONE`, Execution Depth, Candidate Coverage Matrix Position, and Class Coverage Status;
- Implementation Candidate Classification Matrix is produced or explicitly `NOT_APPLICABLE`;
- Candidate Coverage Matrix is produced or explicitly `NOT_APPLICABLE`;
- Candidate Coverage Progress Projection is computed from Candidate Coverage Matrix cells or explicitly `NOT_APPLICABLE`;
- every Progress Projection cell has Current Status, Next Status, Remaining Path, blockers, Estimated Existing Work, and Terminal Alternative;
- every Progress Projection cell has Depends On, Unblocks, Critical Path, Dependency Depth, Root Cause, and Final Consumer computed from Engineering Chain Walk or explicit `NOT_APPLICABLE`;
- Engineering Value is computed for every applicable Implementation Candidate or explicitly `NOT_APPLICABLE`;
- System Engineering Value is computed for every applicable Implementation Candidate or explicitly `NOT_APPLICABLE`;
- Overall Coverage, Overall Automation Coverage, Overall Implementation Coverage, Overall Verification Coverage, Overall Production Coverage, Overall Chain Closure, and Overall Engineering Maturity are computed or explicitly `NOT_APPLICABLE`;
- no real engineering situation in the declared scope remains unclassified or unmapped without `CANDIDATE_CLASS_UNKNOWN_WITH_REASON`;
- no Candidate Coverage Matrix cell is filled by a document, owner, report, model, rule, section, Function Graph node, canonical source, or context artifact alone;
- `IMPLEMENTATION_BLOCKED` findings have exact blocker and required existing-owner extension or terminal alternative;
- Implementation Candidate Catalogue is produced or explicitly `NOT_APPLICABLE`;
- Implementation Blocker Matrix is produced or explicitly `NOT_APPLICABLE`;
- Implementation Readiness Matrix is produced or explicitly `NOT_APPLICABLE`;
- OMP Implementation Input is produced or explicitly `NOT_APPLICABLE`;
- Codex Implementation Input is produced or explicitly `NOT_APPLICABLE`;
- Engineering Automation Backlog is produced as BDP catalogue or explicitly `NOT_APPLICABLE`;
- Engineering Automation Backlog is not treated as official OMP Implementation Backlog;
- Intent Closure Matrix is produced or explicitly `NOT_APPLICABLE`;
- Intent Coverage Matrix is produced or explicitly `NOT_APPLICABLE`;
- Automation Break Catalogue is produced or explicitly `NOT_APPLICABLE`;
- Automation Break Matrix is produced or explicitly `NOT_APPLICABLE`;
- Intent Trace is produced or explicitly `NOT_APPLICABLE`;
- Forward Trace is produced or explicitly `NOT_APPLICABLE`;
- Backward Trace is produced or explicitly `NOT_APPLICABLE`;
- every Automation Break has Last Successful Step, Stopping Point, Reason For Stop, owner, producer, consumer, and terminal alternative;
- intent-derived Implementation Candidates are merged into the unified Implementation Candidate Catalogue after validation;
- Automation Break is not treated as certified Autonomous Behaviour Gap or OMP mission;
- Engineering Logic Coverage Matrix is produced or explicitly `NOT_APPLICABLE`;
- Automation Progress Matrix is produced or explicitly `NOT_APPLICABLE`;
- Implementation Progress Matrix is produced or explicitly `NOT_APPLICABLE`;
- Production Enablement Matrix is produced or explicitly `NOT_APPLICABLE`;
- Engineering Automation Coverage Report is produced or explicitly `NOT_APPLICABLE`;
- coverage records preserve evidence, blocker, consumer, next action, and terminal alternative;
- coverage does not treat document count, report count, or raw Behaviour count as final progress;
- Engineering Chain Coverage does not treat raw chain count as final progress without Closure Verified and consumer path evidence;
- all `HYPOTHESIZED` behaviours are barred from Reality admission;
- all internal steps are barred from standalone Reality admission;
- all composite candidates are split or rejected as not admissible;
- if Surface Lens is used, every label is `OBSERVED_ENGINEERING_SURFACE` or `NOT_APPLICABLE`;
- no conceptual or rejected Surface Lens is treated as architecture, owner, truth source, storage, Runtime concept, Planner concept, entity, or mandatory layer;
- merge/deduplication preserves evidence;
- Reality Refinement Proposal is produced or explicitly `NOT_APPLICABLE`;
- certification verdict is `BEHAVIOUR_DISCOVERY_PASS` or `BEHAVIOUR_DISCOVERY_PASS_WITH_MINOR_RISKS`;
- output consumers are assigned;
- chain closure status is recorded;
- no Runtime, AEP, AOS, OMP, locked knowledge, or architecture mutation occurred;
- no authority expansion, production mutation, user movement, automatic OMP mission creation, automatic automation execution, automatic implementation execution, official backlog mutation, or automatic Codex assignment occurred.

## 32. Program Trigger Model

BDP may be triggered by:

- operator command;
- accepted AEP Phase 2 need;
- significant implementation change;
- significant Runtime evidence change;
- production evidence update;
- new report that claims behaviour change;
- contradiction between Reality and implementation evidence;
- pre-Phase-3 Reality freshness check;
- operator or AEP request to assess Automation Readiness;
- report or implementation evidence that claims existing logic is machine-checkable;
- manual dependency reduction review;
- trigger/execution/verification/rollback automation readiness review;
- OMP request for certified automation input candidates;
- operator, AEP, or OMP request to discover Engineering Chains;
- report, implementation evidence, runtime evidence, decision evidence, verification evidence, rollback evidence, production evidence, or owner evidence that claims an Engineering Chain exists, changed, closed, broke, or requires implementation;
- operator or AEP request to assess Implementation Readiness;
- OMP request for certified implementation input candidates;
- Codex readiness review request;
- engineering automation backlog catalogue request;
- report or implementation evidence that claims existing logic is ready for implementation;
- operator or AEP request to assess Engineering Intent Closure;
- operator or AEP request to find Automation Breaks;
- report, implementation evidence, runtime evidence, decision evidence, verification evidence, rollback evidence, production evidence, or owner evidence that claims existing logic reaches or fails to reach its original intent;
- operator or AEP request to measure Engineering Logic Automation Coverage;
- OMP request for automation, implementation, or production enablement progress;
- Production Maturity request for production enablement evidence.

Every trigger must first produce a Discovery Economy Decision. If the decision is `DISCOVERY_NOT_REQUIRED_REUSE_EVIDENCE`, BDP records reuse evidence and stops without unnecessary Discovery Pass execution.

BDP must not run automatically unless an existing owner explicitly authorizes the run.

Automation-related triggers still begin with Discovery Economy Decision and do not create automatic OMP missions.

Implementation-related triggers still begin with Discovery Economy Decision and do not create OMP missions, mutate the official OMP Implementation Backlog, assign Codex work, or execute implementation.

Coverage-related triggers still begin with Discovery Economy Decision and do not create OMP missions, mutate the official OMP Implementation Backlog, assign Codex work, mutate Production Maturity, mutate production state, update Reality, or execute implementation.

Intent-related triggers still begin with Discovery Economy Decision and do not create certified Autonomous Behaviour Gaps, OMP missions, official backlog mutations, Codex assignments, Runtime mutations, authority expansion, production mutations, Reality updates, or implementation execution.

Engineering Chain-related triggers still begin with Discovery Economy Decision and do not create new Engineering Entity, architecture, OMP missions, official backlog mutations, Codex assignments, Runtime mutations, authority expansion, production mutations, Reality updates, locked knowledge mutations, or implementation execution.

## 33. Final Program Verdict

This document defines a permanent Behaviour Discovery Program ready for later implementation.

It discovers:

- Engineering Chains;
- observed Behaviour;
- Automation-Ready Engineering Logic;
- Implementation-Ready engineering work;
- Automation Gaps as candidates;
- OMP-ready automation input proposals;
- OMP-ready Implementation Candidates;
- intent-derived Implementation Candidates through Automation Break analysis;
- Codex Implementation Input;
- Engineering Automation Backlog catalogue;
- Engineering Intent Closure;
- Engineering Chain Coverage;
- Engineering Chain Walk;
- Engineering Chain Traceability;
- Engineering Chain Closure;
- Automation Break Catalogue;
- Engineering Logic Automation Coverage;
- Automation Progress;
- Implementation Progress;
- Production Enablement progress.

Verdict:

```text
BEHAVIOUR_DISCOVERY_PROGRAM_DESIGNED
```

Implementation status:

```text
NOT_STARTED
```

Discovery execution status:

```text
NOT_EXECUTED
```
