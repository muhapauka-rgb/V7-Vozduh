# V7 Canonical Reference

Status: canonical project reference
Last verified commit: `7b3f6bca`
Last verified date: 2026-06-23

This document describes the current meaning of V7 system concepts. It is not a history log and not an audit report. Reports remain evidence. ADRs explain why a decision was made. This reference is the current truth that future V7 work must read before re-auditing old concepts.

## Reference Update Rule

Any audit or implementation that changes system meaning must update this file. If the work makes or changes a decision, it must also add or update an ADR under `docs/decisions/`.

No important V7 knowledge may remain only in chat, temporary reports, Codex output, screenshots, or one-off validation notes.

Before commit and push after major logic work:

1. Update `docs/reference/V7_CANONICAL_REFERENCE.md`.
2. Update or create an ADR when a decision changed.
3. Run `tools/v7-truth-check --all --json`.
4. Run `tools/v7-convergence-status --json`.
5. Commit code and docs together.

## Knowledge Preservation Rules

1. No important knowledge may live only in chat.
2. No important knowledge may live only in reports.
3. Stable conclusions must move into `docs/reference/V7_CANONICAL_REFERENCE.md`.
4. Architectural decisions must move into ADRs under `docs/decisions/`.
5. Future audits must read this reference, relevant ADRs, and `docs/reference/SYSTEM_MAP.md` before auditing.
6. Full autonomy architecture, dependency, maturity, and roadmap questions must read `docs/reference/V7_AUTONOMY_BLUEPRINT.md` before launching a new autonomy-wide audit.

Before launching any new audit, use Reference First:

1. Read `docs/reference/V7_CANONICAL_REFERENCE.md`.
2. Read relevant ADRs.
3. Read `docs/reference/SYSTEM_MAP.md`.
4. Determine whether the answer already exists.

A new audit is allowed only when the reference has no answer, the reference explicitly marks the area `UNKNOWN`, system behavior changed after the last verified commit, or evidence contradicts this canonical reference. Otherwise, update the reference if needed and do not create a new audit.

## ARCHITECTURAL_DESIGN_METHODOLOGY

Status: `CANONICAL`

Purpose: preserve the complete V7 architectural design methodology so future capability work reuses existing laws instead of inventing new foundational principles.

Canonical verdict:

```text
ARCHITECTURAL_METHODOLOGY_COMPLETE
```

V7 does not need a new architectural law to design future capabilities.
The complete methodology is the composition of existing canonical owners:

| Methodology question | Canonical answer owner |
| --- | --- |
| What product outcome should the capability serve? | `docs/product/V7_PRODUCT_SPECIFICATION.md` through Business Objectives and Product Scale Objectives. |
| Does the capability already have an owner? | `docs/reference/SYSTEM_MAP.md`, this Canonical Reference, OMP, ADRs, policies, and the Implementation Backlog. |
| Where does the computation belong? | `docs/reference/V7_RUNTIME_MODEL.md` through Runtime Time Architecture and Work Placement Law. |
| What is the decision lifecycle and freshness contract? | `docs/reference/V7_RUNTIME_MODEL.md` through Decision Lifecycle And Runtime Foundation. |
| What is the desired-state chain? | `docs/reference/V7_RUNTIME_MODEL.md` and `docs/reference/V7_DECISION_MODEL.md`. |
| What is mandatory for certification? | Canonical certification owners: OMP, policies, Product Specification, Runtime Model, Decision Model, and existing certification sections. Implementation owners may not promote supporting metrics into mandatory gates unless the canonical owner says so. |
| What must remain live in Runtime? | Runtime Model safety gates, Thin Runtime Path Contract, STOP_SAFE, rollback, verification, freshness, authority, blast radius, anti-flap, movement protection, and restore barrier owners. |
| What can move earlier? | Work Placement Law: work may move earlier only when prepared knowledge stays fresh enough and live gates still revalidate material state before apply. |
| How does the change affect time? | Runtime Time Architecture, Reaction Latency Model, Runtime Cost Model, and Runtime Budget Allocation. |
| How does the change affect scale? | Product Scale Model/Objectives and OMP Production Scale First. |
| How does the change affect automation? | OMP, Action-Class Authority, Delegated Autonomy Policy, Safety-Bounded Authority, and Runtime Model authority rules. |
| How does work proceed? | OMP `Continue OMP` Engineering Control Loop, Implementation Backlog, Current Program State, Engineering Reports, and knowledge promotion rules. |

Permanent methodology:

```text
Discover
  -> Resolve canonical owner
  -> Reuse existing owner
  -> Extend existing owner only if required
  -> Apply Work Placement
  -> Apply Decision Lifecycle / Freshness
  -> Apply Certification Truth
  -> Apply Runtime Time / Cost / Latency review
  -> Apply Product Scale review
  -> Apply Safety / STOP_SAFE review
  -> Implement through backlog only
  -> Verify
  -> Report
  -> Promote durable knowledge
  -> Continue OMP
```

Stable conclusions:

1. V7 already contains canonical equivalents of Reality First, Truth Source, Certification Truth, Thin Runtime, Runtime Time Architecture, Reaction Latency, Work Placement, Decision Lifecycle, Decision Freshness, Desired State, World Model, Prepared Knowledge, Read Model Discipline, STOP_SAFE, Fail Closed, Authority Before Automation, Verification Before Promotion, Rollback First, Representative Evidence, Background Builds Knowledge, Runtime Consumes Prepared Knowledge, Discover -> Reuse -> Extend -> Implement, Product Scale First, Engineering Review, and Safety Review.
2. These principles are distributed intentionally by ownership, not missing: Product Specification owns product intent, Runtime Model owns runtime/time/placement/lifecycle semantics, OMP owns execution discipline, policies own operational certification semantics, SYSTEM_MAP owns ownership lookup, and this Canonical Reference preserves durable truth.
3. A future V7 capability can be designed without inventing a new architectural law if it answers the methodology questions above through existing owners.
4. New architecture remains the last resort under Architecture Closed by Default.
5. Need New Owner remains `FALSE`; Need New Backlog Item remains `FALSE`; Need New Architecture remains `FALSE`.

Re-audit rule:

Do not re-audit architectural methodology unless a future capability cannot be mapped to an existing canonical owner after complete discovery, production evidence contradicts the current methodology, a certified ADR changes the architectural law set, or the operator explicitly requests reopening.

## RUNTIME_TIME_ARCHITECTURE_MODEL

Status: `CANONICAL`

Purpose: preserve the durable RT Phase 1 conclusion so future work does not rediscover or bypass V7's architecture of time.

Canonical owner:

```text
docs/reference/V7_RUNTIME_MODEL.md
```

Stable conclusions:

1. V7's time architecture is `Observation Plane -> World Model Plane -> Planning Plane -> Execution Plane -> Verification Plane -> Feedback / Learning Plane -> OMP / Certification Plane`.
2. Runtime must remain the thin execution path: short, deterministic, lease-bound, and fail-closed.
3. Slow knowledge work should be prepared outside the execution path wherever safety permits.
4. Execution consumes prepared knowledge and then applies live safety gates.
5. Work Placement Law: every V7 computation must have one canonical execution plane and owner. Other planes may consume the result, but must not become competing owners.
6. A computation may move earlier only when prepared knowledge remains fresh enough and live safety gates still revalidate material state before apply.
7. Computation must stay live only when safety would be weaker if the work were precomputed.
8. Decision Lifecycle And Runtime Foundation defines the lifecycle of planner decisions, candidate universe, packets, leases, authority generation, world model, target readiness, rollback readiness, and verification readiness.
9. Decision Freshness states are `BORN`, `FRESH`, `STALE`, `INVALID`, and `DESTROYED`.
10. World Model Ownership is plane-based: Observation, World Model, Planning, Execution, Verification, Feedback/Learning, and OMP/Certification owners must not silently replace each other.
11. Desired State Contract follows `Current State -> Desired State -> Delta -> Execution Plan -> Verification -> Outcome -> Learning`.
12. Runtime Cost Model reviews CPU, memory, IO, blocking, lock contention, execution cost, rollback cost, and runtime cost.
13. Runtime Budget Allocation defines Observation, World Model, Planning, Execution, Verification, Learning, and OMP budget categories without numeric Phase 1 SLOs.
14. Product Evolution Review Gate requires Certification, Work Placement, Runtime Latency, Runtime Cost, Decision Freshness, and Safety review before future implementation is considered complete.
15. Reaction Latency means `Observation Latency + Decision Latency + Execution Latency + Verification Latency + Feedback / Learning Latency`.
16. User recovery latency is mainly Observation, Decision, Execution, and Verification latency. Feedback / Learning latency affects product maturity, future decisions, and certification.
17. Phase 1 creates no numeric latency SLOs, no latency gates, no runtime automation, no batch movement, no parallel movement, no execution queue, no user movement, no authority expansion, and no runtime behavior change.
18. Every future engineering activity must apply the Runtime Latency Engineering Review Checklist from `docs/reference/V7_RUNTIME_MODEL.md` and must preserve the Thin Runtime Path Contract.
19. Engineering Reports must include Product Evolution Review, Work Placement, and Latency Impact.
20. Phase 2 Automation-Time work is deferred, not optional. It may start only after bounded automation, runtime eligibility, verification, rollback, blast radius, metric reliability, reaction latency measurements, and explicit authority are certified or approved through existing owners.
21. Phase 2 forbids parallel movement, batch movement, continuous apply, execution queues, desired-state runtime, latency SLO gates, planner rewrite, and authority expansion before entry criteria are satisfied.
22. Need New Owner remains `FALSE`; Need New Backlog Item remains `FALSE`; Need New Architecture remains `FALSE`.

Re-audit rule:

Do not re-audit Runtime Time Architecture unless runtime architecture changes materially, bounded automation is certified and Phase 2 begins, production latency evidence contradicts the current model, or the operator explicitly requests reopening.

## PRE_PHASE_2_READINESS_PROGRAM

Status: `CANONICAL`

Purpose: preserve the durable conclusion that V7 already contains the foundations required to prepare for Runtime Phase 2, but Phase 2 itself remains closed until existing certification, measurement, and authority conditions are satisfied.

Canonical owner:

```text
docs/programs/OPERATIONAL_MATURITY_PROGRAM.md
```

Foundation owner:

```text
docs/reference/V7_RUNTIME_MODEL.md
```

Stable conclusions:

1. DL1 Decision Lifetime Model exists and is canonical.
2. DL2 Decision Freshness Contract exists and is canonical.
3. DL3 World Model Ownership exists and is canonical by plane ownership.
4. DL4 Desired Safe State exists partially: Desired State is canonical, but the Phase 2 Desired Safe State artifact must wait for A6/B13/B16 and authority.
5. DL5 Runtime Cost Model exists and is canonical.
6. DL6 Runtime Budget Allocation exists partially: budget categories are canonical, but numeric budgets are deferred until measurement and Phase 2 entry.
7. DL7 Product Evolution Review Gate exists and is canonical through Runtime Model and OMP.
8. Pre-Phase-2 Readiness is an OMP program, not a new architecture, owner, backlog item, runtime path, automation mode, or authority model.
9. Phase 2 may begin only after RT Phase 1, Work Placement, Decision Lifecycle, Pre-Phase-2 Readiness, A5, A6, B13, B16, Reaction Latency measurement, Runtime Cost measurement, canonical World Model, canonical Desired Safe State, active Engineering Review, and explicit authority are complete.
10. Until then, OMP continues through existing OMP/backlog owners. Current next item is `RT2-S3` Desired-State Delta Preparedness after RT2-S2 read-only world/readiness maturation.

Re-audit rule:

Do not re-audit Pre-Phase-2 Readiness unless a Phase 2 entry criterion changes, A5/A6/B13/B16 completion changes the readiness state, production evidence contradicts the readiness model, or the operator explicitly requests reopening.

## MASTER_SYSTEM_INTEGRATION_AUDIT_PART_1

Status: `SYSTEM_INVENTORY_COMPLETE`

Purpose: preserve the Part 1 master integration inventory so future work does not rediscover system ownership, capability ownership, dependency shape, or report-only knowledge boundaries.

Stable conclusions:

1. V7's major production system parts already exist: Product Specification, Business Objectives, Canonical Policy Library, OMP, Capability Framework, Implementation Backlog, Runtime Model, Runtime/read-only owners, Current Program State, Canonical Reference, SYSTEM_MAP, ADRs, and Engineering Reports.
2. The canonical dependency chain is `Product Specification -> Business Objectives -> Canonical Policies -> OMP -> Capability Framework -> Implementation Backlog -> Runtime Model -> Runtime -> Users`.
3. The current integration problem is not missing architecture. The current integration problem is incomplete connection and materialization between existing owners, especially where product language, capability progress, runtime eligibility, operator explanations, UI surfaces, and production evidence must converge.
4. Mandatory capabilities from the Part 1 audit all map to existing owners. Need New Owner remains `FALSE`.
5. No duplicate owner requiring replacement was found. Existing overlaps are layered defense-in-depth or lifecycle separation: authority vs runtime eligibility, freshness owners vs leases/snapshot gates, rollback manifest vs rollback execution, reports vs canonical truth, product intent vs policy translation, and OMP vs Current Program State.
6. Critical knowledge leak verdict: no audited durable rule must remain only in an Engineering Report. Recent durable findings for Business Objectives, Operator Responsibility, Business Intent, Decision Explainability, Execution Intent Authority, Approval Model Progress, Movement Protection, and World Equivalence are already promoted into Product Specification, OMP, Canonical Reference, Runtime Model, SYSTEM_MAP, or existing ADRs.
7. Engineering Reports remain historical evidence only. If a future report contains durable knowledge, it must immediately update Product Specification, Canonical Reference, OMP, Runtime Model, SYSTEM_MAP, ADR, or another existing canonical owner.
8. Capabilities currently `LOCKED` or complete at the canonical level: Knowledge System, Engineering Knowledge Preservation, Implementation Discipline.
9. Capabilities currently partially connected and still needing implementation/certification evidence through existing backlog items: Movement Protection, Decision Explainability, Authority Evolution, Action-Class Authority, Delegated Autonomy Policy, Runtime Eligibility, Rollback, Recovery Admission, Learning, Production Readiness, Production Autonomy, Observability, Business Operator Experience.
10. Business Objectives and Operator Responsibility are product-level concepts owned by Product Specification and consumed by OMP/policies/runtime only after translation into canonical policies, capability progress, runtime eligibility gates, and operator-facing explanations.
11. World Equivalence is canonical knowledge, not a recurring research task. Future world comparison is forbidden unless industry consensus materially changes, planner/runtime architecture materially changes, production evidence disproves current behavior, or the operator explicitly requests reopening.
12. Part 2 may proceed from this inventory without creating a new owner, new document, new roadmap, new planner, new governance, new execution path, or new truth source.

Knowledge leak rule:

If a future audit finds durable knowledge only in `docs/reports/`, old audits, temporary files, screenshots, or conversation history, that finding is `KNOWLEDGE_LEAK_CRITICAL` and must be assigned to an existing canonical owner before the task is considered complete.

## MASTER_SYSTEM_INTEGRATION_AUDIT_PART_2

Status: `SYSTEM_INTEGRATION_ANALYSIS_COMPLETE`

Purpose: preserve the Part 2 integration analysis, root-cause verdict, execution graph, and master integration atlas so future work integrates existing owners instead of redesigning V7.

Root cause verdict:

1. V7's current production gap is `INTEGRATION`, not missing architecture, missing product model, missing policy model, missing Runtime Model, missing OMP, or missing capability framework.
2. The dominant root-cause classes are missing runtime consumption, missing UI/operator consumption, missing observability/read-model materialization, missing certification, and missing production evidence.
3. No partially connected capability requires a new owner. Need New Owner remains `FALSE`.
4. No partially connected capability requires a replacement architecture, planner, governance layer, execution path, runtime owner, truth source, or roadmap.
5. Current execution stops at the governed production-operation boundary because A3 still needs real rollback/no-rollback outcome evidence and exact operational approval while the first action class remains `GOVERNED_ONLY`.
6. Product Owner and operator burden persists because routine execution has not yet been certified into Action-Class Authority, Delegated Autonomy Policy, runtime eligibility arbitration, Decision Explainability, and UI business-language surfaces.
7. Business language already exists in Product Specification as Business Objectives. It is consumed by OMP and policies conceptually, and Runtime consumes it only after policy translation. The remaining gap is consistent operator/UI exposure and evidence-linked decision explanations.
8. Runtime does not ignore the architecture; it stops where evidence, authority, certification, or runtime eligibility is not yet connected strongly enough for autonomous execution.
9. OMP does not ignore existing knowledge; it remains bound to the Implementation Backlog, Current Program State, production maturity, and capability framework. The gap is that not every canonical policy/capability has completed implementation and certification evidence.
10. No knowledge leak was found that requires a new canonical owner. Durable Part 2 findings are stored here and in SYSTEM_MAP; reports remain historical evidence.

Current execution graph:

```text
Product Owner
  -> Product Specification
  -> Business Objectives
  -> Canonical Policies
  -> OMP
  -> Capability
  -> Implementation Backlog
  -> Runtime Model
  -> Runtime / governed execution owners
  -> Users
```

Current stop points:

1. `Business Objectives -> UI`: business language is canonical but not yet consistently primary in operator surfaces.
2. `Policies -> Runtime`: policies are canonical and mapped to backlog, but centralized runtime arbitration and certification remain partial.
3. `Capability -> Runtime`: capability maturity exists in OMP, but runtime does not yet consume every capability state as executable eligibility.
4. `Runtime -> Users`: production movement remains governed because action classes are not yet certified for runtime autonomy.
5. `Outcome -> Learning -> OMP`: learning path exists, but more real representative outcomes and metric reliability are required for promotion.

Ideal execution graph:

```text
Product Owner
  -> Business Objectives
  -> Canonical Policies
  -> OMP capability state
  -> Backlog-completed certified gates
  -> Runtime eligibility arbitration
  -> Runtime executes or stops inside approved policy
  -> Verification
  -> Rollback / containment if needed
  -> Outcome closure
  -> Learning
  -> OMP maturity update
  -> Product Owner supervises policy and exceptions only
```

Permanent integration rule:

Future work must target the missing connections in the Master Integration Atlas. It must not start new semantic audits, new roadmaps, new documents, or new owners when an existing owner and backlog/capability path already exists.

## MASTER_SYSTEM_INTEGRATION_AUDIT_PART_3

Status: `MASTER_INTEGRATION_PROGRAM_COMPLETE`

Purpose: preserve the final master integration program so V7 can move from completed capabilities to one coherent production operating system through existing owners and backlog items only.

Stable conclusions:

1. The Master Integration Program lives in OMP, not in a new roadmap document.
2. The program uses the existing Master Integration Atlas in SYSTEM_MAP and maps every integration task to an existing owner, existing capability, and existing backlog item.
3. Need New Owner remains `FALSE`.
4. Need New Backlog Item remains `FALSE`.
5. No duplicate document, policy, capability, truth source, planner, governance layer, execution path, runtime owner, or roadmap is required.
6. Integration execution order begins with `A3` because class-level rollback/no-rollback evidence is the first dependency for action-class promotion, authority evolution, production evidence, learning, and production autonomy.
7. Runtime may consume only canonical policies, certified action classes, delegated autonomy policy, runtime eligibility, authority, freshness, rollback, verification, and learning. Runtime must not consume raw Product Owner text, raw Business Objectives, subjective operator wishes, or report-only knowledge.
8. Product Owner target interface is Business Objectives, Business Status, Business Risk, Business Profile, Business Results, and Business Exceptions only.
9. Operator UI target language is business language first; engineering details are secondary, read-only, expandable, and never primary.
10. OMP remains the permanent operating system and should normally require only `Status`, `Continue OMP`, `Approve authority expansion`, and `Production Action`.
11. Implementation may begin from the existing backlog and Master Integration Program without creating new audits or roadmaps.

Readiness verdict:

`READY_FOR_IMPLEMENTATION_PROMPT`

## MASTER_KNOWLEDGE_SYSTEM_AUDIT_PART_3

Status: `KNOWLEDGE_SYSTEM_OPERATIONAL`

Purpose: preserve the final operational Knowledge Plane contract so future OMP, Codex, AI agents, engineering, audit, implementation, and certification work starts from current knowledge instead of rediscovering old reports.

Stable conclusions:

1. The Knowledge Plane is operational and uses existing owners only. Need New Owner remains `FALSE`.
2. Audit Knowledge State is not a new truth source. It is the current durable knowledge state assembled from Canonical Reference, SYSTEM_MAP, OMP, Current Program State, Production Maturity, Knowledge Quality Model, Document Lifecycle, ADRs, canonical policies, and engineering reports as supporting evidence.
3. Knowledge State is current durable truth for engineering work; Engineering Reports are historical evidence; Current Program State is current runtime/program situation; Canonical Reference is durable project truth; OMP is the execution program; Implementation Backlog is the only engineering queue.
4. Future Codex and future AI agents must not start by reading historical reports. They must first consume Product Specification, Audit Knowledge State, Canonical Reference, Current Program State, OMP, and Implementation Backlog, then load Runtime Model, implementation files, reports, ADRs, policies, or tools only when the resolved task requires them.
5. Every future engineering action must determine: already known, still valid, re-open required, implementation required, existing owner, existing backlog mapping, confidence, freshness, and expected evidence.
6. Every future audit must reuse current knowledge first, audit only unknown or invalidated knowledge, update canonical owners when durable knowledge changes, update Audit Knowledge State, and create a historical Engineering Report.
7. Every future implementation must read the Knowledge Plane, implement the existing backlog item, verify, certify when required, create an Engineering Report, update canonical owners if durable knowledge changed, update Knowledge State, update Current Program State, and update OMP.
8. Every certification must update Knowledge State, Capability State, Production State, and Current Program State before producing historical evidence.
9. Knowledge promotion flow is `Temporary Investigation -> Engineering Report -> Verified -> Canonical Owner -> Audit Knowledge State -> OMP Consumption -> Future Codex`.
10. Knowledge invalidation triggers are Runtime Model changes, Product changes, Policy changes, contradictory production evidence, material implementation changes, operator decision changes, architecture changes, and Product Scale Model changes. Each trigger maps to existing owners; no new invalidation owner is required.
11. Knowledge System and Engineering Knowledge Preservation remain complete and locked at the canonical level while these rules hold.
12. Architecture maturity remains `ENGINEERING_COMPLETE`; Production Maturity remains implementation/certification-bound and must advance only through the Implementation Backlog, real verification, production outcomes, certification, and authority decisions.

Mandatory Knowledge Plane workflow:

```text
Product Specification
  -> Audit Knowledge State
  -> Canonical Reference
  -> Current Program State
  -> OMP
  -> Implementation Backlog
  -> Runtime Model when relevant
  -> Implementation when authorized
```

World-practice comparison:

The final V7 Knowledge Plane matches mature production knowledge-management practice:

| Practice family | Equivalent V7 behavior |
| --- | --- |
| Google SRE | Current operating state separated from postmortems and durable operational principles. |
| AWS control planes | Runtime consumes prepared knowledge and current state; durable policies and runbooks govern execution. |
| Cloudflare operations | Historical incidents/evidence feed durable rules, but live operation uses current control-plane state. |
| Kubernetes | Desired/current state, status, events, controllers, and API truth remain separated by owner and lifecycle. |
| ADR workflow | Decisions remain permanent records; they do not become runtime truth or implementation queues. |
| RFC workflow | Durable consensus moves into canonical references; drafts/reports remain supporting evidence. |

Re-open rule:

The operational Knowledge Plane must not be re-audited unless one of these is true:

1. an existing owner cannot map a finding after complete audit;
2. production evidence contradicts canonical knowledge;
3. Runtime Model, Product Specification, Canonical Policy Library, OMP, or Product Scale Model changes materially;
4. an implementation changes behavior materially;
5. the operator explicitly requests re-audit.

## Product Specification Rule

`docs/product/V7_PRODUCT_SPECIFICATION.md` is the highest-level product specification for V7.

It defines what V7 is as a product.

Architecture, OMP, Codex work, Runtime, implementation programs, research, reports, and ADRs derive product meaning from this specification.

Stable conclusions:

1. V7 is a production connectivity product that keeps users online by making routing invisible.
2. V7 is an autonomous routing control plane for user connectivity, not a VPN panel, manual routing tool, monitoring dashboard, static load balancer, hardcoded switch engine, or planner playground.
3. Product success means users stay online, important services remain reachable, routing changes are invisible or minimally disruptive, wrong moves are rare, rollback is available, learning improves decisions, and operator workload decreases.
4. V7 product principles are Reality First, User Connectivity First, Minimal Operator Work, Safety Before Movement, Learning From Reality, Event-Driven Operation, Reuse Before Rewrite, Simple Action-Class Authority, Explainability, Reversibility, Verification Before Trust, Background Knowledge / Thin Runtime, and No Duplicated Systems.
5. Current product maturity is `Operational`, moving through governed `Production` maturity.
6. Fundamental missing product questions: `NONE`.
7. Product certification verdict: `PRODUCT_SPECIFICATION_COMPLETE`.
8. Autonomy Promotion Engine is a product rule: V7 must move the operator from temporary governed packet approval to durable Action-Class Authority, authority expansion, product policy, new classes, and exceptional situations.
9. Automation grows by promoting certified action classes from real outcomes, verification, rollback quality, safety, blast radius, learning, trust, and authority policy; reports alone and synthetic evidence cannot promote a class.
10. Packet approval is not the primary product authority model. Packets are fresh runtime execution artifacts and may execute only when they match approved Action-Class Authority, policy, freshness, safety, rollback/no-rollback, verification, learning, and blast-radius bounds.
11. Packet-level approval remains only as a temporary `GOVERNED_ONLY` fallback until an action class is certified and explicitly approved for class authority or runtime capability.
12. Delegated Autonomy Policy is the target approval model: the operator approves bounded policy once, V7 may self-approve operational routing decisions only inside that policy, and Runtime stops outside it.
13. V7 may not self-approve policy expansion, new action classes, increased blast radius, lower safety gates, or authority expansion. V7 may only recommend those changes.
14. Execution Intent Authority is not a new owner or new authority model. Its semantics already map to Action-Class Authority plus Delegated Autonomy Policy plus Runtime fresh-packet eligibility: the operator approves constraints, Runtime selects or consumes the current valid packet inside those constraints, and re-approval is required only when constraints, class, policy, authority, safety, freshness, rollback/no-rollback, verification, learning, or blast-radius bounds are violated.
15. Approval Model Progress is not a new owner. OMP already owns the transition from temporary packet approval to Action-Class Authority, Delegated Autonomy Policy, and Runtime Capability through Autonomy Promotion Engine, Delegated Autonomy Policy Model, Authority Evolution capability, and Current Program State. If a single approval-progress percentage is needed, extend those existing OMP/Current State fields instead of creating a new document or owner.
16. The Canonical Policy Library at `docs/policies/` is the permanent source for operational behavior policy. Policies must be discovered from mature production systems, compared, validated, adapted, implemented, verified, certified, and integrated into OMP before becoming operational.
17. V7 may innovate in policy only after proving that no stable world consensus exists or that world consensus does not fit V7 architecture.
18. Business Objectives are the canonical top-level interface between the Product Owner and V7. The permanent chain is Product Owner -> Business Objectives -> Policy Translation -> Canonical Policies -> OMP -> Runtime -> Users. Product Owner communicates through Business Objectives, not packets, routing algorithms, action classes, blast-radius internals, rollback internals, runtime gates, planner logic, or protocol engineering.
19. Initial canonical Business Objectives are Maximum Stability, Fastest Recovery, Lowest User Disruption, Highest Service Availability, Lowest Business Risk, SLA Priorities, Business Risk Appetite, Minimal Operator Work, and Invisible VPN Experience.

## DECISION_OBJECT_MODEL

Status: `CANONICAL`

Purpose: preserve the complete V7 decision-object taxonomy so future work does not rediscover or confuse authority objects, decision objects, execution objects, packet artifacts, learning objects, and product intent.

Canonical hierarchy:

```text
Business Objective
  -> Business Intent
  -> Canonical Policy
  -> Operational Envelope
  -> Authority Object
  -> Action Class
  -> Decision Snapshot
  -> Eligibility Decision
  -> Execution Decision
  -> Fresh Packet
  -> Operation
  -> Verification
  -> Outcome
  -> Learning
  -> Knowledge
```

Object classes:

| Object | Owner | Class | Canonical rule |
| --- | --- | --- | --- |
| Business Objective | Product Specification | Product / canonical | Highest Product Owner interface; not runtime input until translated through policy. |
| Business Intent | Product Specification | Product / canonical | Product meaning derived from objectives, mission, principles, risk appetite, SLA priorities, and ideal user experience. |
| Canonical Policy | Canonical Policy Library | Canonical / policy | Translates product intent into operational rules; consumed by OMP and Runtime gates. |
| Operational Envelope | OMP, Runtime Model, Policy 004, Policy 005 | Canonical / authority | Defines approved class, policy, authority tier, blast radius, rollback, freshness, verification, anti-flap, learning, and risk bounds. |
| Authority Object | OMP / Policy 004 | Canonical / certification | Current fallback may be exact packet; target durable authority is Action Class / Delegated Policy / Business Objective constraints. |
| Authority Tier / Generation | OMP / Current Program State / Runtime Model | Runtime + canonical state | Permission scope and generation guard; does not prove runtime safety by itself. |
| Action Class | OMP / Policy 005 | Canonical / certification | Repeated operational capability promoted only by real outcomes, verification, rollback/no-rollback quality, blast radius, learning, and authority policy. |
| Delegated Autonomy Policy | OMP / Runtime Model | Canonical / authority | Bounded self-approval contract; current default is read-only and not approved. |
| Decision Model | V7 Decision Model | Canonical | Defines decision vocabulary, laws, input separation, and decision output shape. |
| Decision Snapshot | Decision Model + existing decision/read-model owners | Runtime-consumed | Prepared decision output; Runtime consumes it and must not invent it. |
| Planner Decision | Planner / autoswitch owners | Runtime input / implementation | Candidate/ranking output; not durable authority and not the complete decision model. |
| Eligibility Decision | Runtime Model + policy/read-model owners | Runtime | Pass/stop decision over policy, freshness, authority, rollback, verification, anti-flap, blast radius, and learning gates. |
| Execution Decision | Runtime Model + existing execution owner | Runtime | Execute or stop; only after eligibility and authority pass. |
| Packet / Preview | Execution Packet owner | Transient runtime artifact | Fresh bounded execution artifact; not canonical authority. |
| Operation | Execution owner / Current Program State | Transient runtime artifact that becomes historical after closure | One concrete production attempt with identifiers. |
| Selected Move | Planner/autoswitch + packet owner | Transient execution artifact | Concrete user/source/target move; must match authority envelope before execution. |
| Selected Move Hash | Packet / lease owner | Transient identity guard | Integrity guard for the selected move; not an authority object. |
| Execution Lease | Packet owner | Runtime guard | Binds approved governed packet while active; expires or closes after execution/rollback/cancel/material change. |
| Restore Barrier Clearance | Restore barrier owner | Runtime guard | One exact clearance before apply; not durable policy. |
| Rollback Manifest / Plan | Restore/Rollback owner | Runtime + certification evidence | Must exist or no-rollback path must be certified before trust grows. |
| Verification Plan | Verification owners / Runtime Model | Runtime + certification evidence | Required before mutation can be trusted. |
| Outcome | Feedback/outcome owner | Historical + learning | Real observed result of execution, no-op, rollback, or stop; can feed learning only after verification. |
| Learning Object | Learning/trust owners | Learning / knowledge | Updates future confidence only from observed outcomes, never synthetic evidence. |
| Knowledge Object | Knowledge Quality Model / Canonical owners | Canonical or historical depending on promotion | Durable knowledge must move to canonical owners; reports remain evidence only. |
| Engineering Report | OMP report lifecycle | Historical evidence | Never backlog, roadmap, owner, truth source, or runtime authority. |
| Current Program State | Current Program State | Volatile program state | Stores current bottleneck, authority class, packet when applicable, stop reason, progress, and next action. |

Authority rule:

Current `GOVERNED_ONLY` work may still require exact packet approval, but this is transitional. The durable target is:

```text
Business Objective
  -> Canonical Policy
  -> Delegated Autonomy Policy
  -> Action-Class Authority
  -> Runtime Eligibility
  -> Fresh Packet
```

Execution rule:

Runtime executes fresh packets or stops. It does not execute raw Business Objectives, raw Product Owner wishes, reports, historical evidence, or unverified planner guesses.

Learning rule:

Learning learns from verified outcomes, action-class evidence, policy/class performance, rollback/no-rollback results, and real user/service impact. It does not learn trust from packet existence, packet approval, synthetic evidence, or unverified expectations.

Need New Owner: `FALSE`.

Need New Backlog Item: `FALSE`.

Architecture gap: `NO`.

## Certified Root Cause Rule

When a phase has already certified all of the following:

1. root cause found;
2. solution proven;
3. dry-run successful;
4. no runtime-apply risk;

the next phase must move to:

```text
IMPLEMENT
  -> TEST
  -> VERIFY
  -> DOCUMENT
```

It must not create another discovery/audit report for the same root cause.

Allowed exception: a new audit may run only if new evidence contradicts the certified root cause, the proven dry-run no longer reproduces, the implementation would introduce runtime apply risk, or the reference explicitly marks the area `UNKNOWN`.

This rule applies after Reference First. Reference First determines whether the answer already exists; Certified Root Cause Rule determines that a proven answer must be implemented and verified rather than re-discovered.

## Autonomy Blueprint Rule

`docs/reference/V7_AUTONOMY_BLUEPRINT.md` is the permanent autonomy engineering blueprint. It maps current subsystems, dependency graphs, hidden/dormant systems, maturity percentages, industry comparison, and the 12-month roadmap from governed operator actions to event-driven autonomy.

Current blueprint verdict: `AUTONOMY_BLUEPRINT_CREATED_EVENT_DRIVEN_AUTONOMY_PARTIAL`.

Stable conclusions:

1. V7 already has the main owners for planner, governed execution, restore barrier, rollback, feedback, learning, trust, prediction, shadow comparison, and truth/convergence.
2. The safe path is to reuse and connect existing owners, not create a new planner, governance model, execution path, truth source, or confidence model.
3. Production event-driven autonomy remains blocked by insufficient observed outcome confidence, low prediction confidence, uncertified live event consumption, and autonomy floors still below `70.0`. Operator comparison is secondary supervised confirmation, not the primary trust source.
4. Timer-only movement remains rejected. Event-driven autonomy means regression event -> planner -> packet -> restore barrier -> bounded apply -> verification -> rollback decision -> feedback -> learning.
5. The next roadmap position is `OBSERVED_OUTCOME_EVIDENCE_AND_EVENT_CONSUMER_CLOSURE`.
6. The post-production scale phase `AUTONOMY.EVIDENCE.INDEX_AND_FRESHNESS_MODEL` is documented but deferred. It must not start until Production Autonomy is certified.

## Operational Maturity Program Rule

`docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` is the permanent production operating program and single execution program for V7. Version `4.0` replaces roadmap-driven, phase-first, free-form implementation ideas, and architecture-first continuation with continuous production maturity evolution.

The complete autonomy roadmap lives inside OMP. No additional roadmap document is required to drive V7 from current `TIER_1` governed autonomy toward full production autonomy.

Stable conclusions:

1. The current program is `V7.OMP.FINAL.PRODUCTION_PROGRAM`.
2. OMP is the permanent production operating program and single execution program.
3. OMP owns the complete autonomy roadmap and production maturity ladder.
4. Tier 0 is `COMPLETE`: Architecture, Research, Decision Model, Runtime Model, and System Architecture.
5. Tier 1 is `ACTIVE`: implementation, existing owner integration, testing, certification, production deployment, one-user governed canary, outcome closure, and learning.
6. Future tiers are evidence-gated: low-risk autonomous execution, small-batch autonomy, operational autonomy, production autonomy, authority evolution, continuous implementation, continuous optimization, continuous knowledge evolution, and production evolution.
7. OMP answers what implementation gives the highest production leverage right now.
8. OMP evaluates authority after every successful certified outcome: remain unchanged, shrink, or propose expansion.
9. OMP may recommend authority expansion, but must never silently expand authority.
10. Authority expansion requires explicit operator approval or certified policy approval.
11. Research changes implementation only through Research -> Decision Model -> OMP -> Implementation.
12. Research never creates architecture directly.
13. Architecture changes require real implementation evidence proving `FUNDAMENTAL_ARCHITECTURE_GAP`.
14. Otherwise V7 must reuse, extend, and implement inside existing owners.
15. Current packet, metrics, stop reason, bottleneck, HLA, and approval question live in `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.
16. New owners, knowledge models, planners, engines, pipelines, APIs, CLIs, storage, snapshots, or truth sources are forbidden unless `Need New Owner = TRUE`.
17. Every implementation must run semantic reuse audit before creating or extending system behavior.
18. After every implementation, OMP must run duplication detection across owners, planners, governance, execution, lifecycle, APIs, CLIs, knowledge models, routing logic, learning logic, truth sources, evidence collectors, packet builders, decision surfaces, and maturity models.
19. Future work may normally proceed through only: `Continue OMP`, `Status`, `Approve packet`, and `Approve authority expansion`, unless a real implementation proves `FUNDAMENTAL_ARCHITECTURE_GAP`.
20. OMP does not authorize restore-barrier writes, runtime apply, user movement, rollback apply, daemon/timer enablement, authority expansion, floor changes, synthetic evidence, new planner, new governance, new execution, storage, runtime owner, or truth source without the required authority.
21. OMP owns the Autonomy Promotion Engine for action classes. After every certified outcome, OMP must evaluate whether the action class can move to the next autonomy state.
22. Canonical action class states are `NOT_CERTIFIED`, `GOVERNED_ONLY`, `CERTIFIED_FOR_CLASS_APPROVAL`, `CERTIFIED_FOR_BOUNDED_AUTONOMY`, and `AUTONOMOUS_RUNTIME`.
23. Current first certifiable action class is `single-user governed candidate failover`; current promotion state is `GOVERNED_ONLY`; current promotion target is `CERTIFIED_FOR_CLASS_APPROVAL`; runtime automation enabled remains `NO`.
24. Action-Class Runtime Enablement path status is `PARTIAL`: existing OMP, trust inventory, governed dry-run, packet, lease, restore/rollback, feedback, learning, and Runtime Model owners now expose read-only action-class registry, packet-to-action-class mapping, authority-to-action-class mapping, runtime capability view, promotion recommendation, and readiness check. Need New Owner remains `FALSE`; Runtime cannot execute this class automatically yet.
25. OMP must evaluate after every certified action class whether packet-level approval can be permanently eliminated for that class. If yes, OMP prepares an Authority Promotion recommendation; if no, it records the exact missing evidence or policy that keeps the class in packet-level governed fallback.
26. The primary authority model is Action-Class Authority. Packet-level authority is a transitional fallback, not the long-term product abstraction.
27. MASTER 2 OMP completeness certification is `COMPLETE`: every future engineering capability, research result, architecture refinement, runtime improvement, implementation task, production evolution, operator workflow, UX/read-model/dashboard change, protocol/routing method, retirement, and deprecation must enter through existing OMP placement, existing owners, Engineering Report, Canonical Update, Current Program State, and the next OMP step.
28. No second roadmap, duplicate OMP, parallel master program, parallel capability program, new runtime, new planner, new truth source, new owner, automation path, or authority expansion is justified by MASTER 2.
29. MASTER 3 OMP resilience certification is complete; the current practical OMP step is `RT2-S3_DESIRED_STATE_DELTA_PREPAREDNESS` after RT2-S2 read-only world/readiness maturation.
30. MASTER 3 OMP resilience certification is `COMPLETE`: destructive tests failed to prove OMP wrong. OMP cannot be meaningfully split, duplicated, or simplified without losing owner, evidence, report, canonical update, CPS, or verification invariants. Future architecture pressure still enters through OMP and stops at Architecture Closed by Default if unmappable.
31. MASTER 4 architecture graduation is complete; Runtime implementation remains forbidden unless OMP, certification, and explicit authority allow it.
32. MASTER 3 final refinement confirms self-evolution and knowledge preservation: durable knowledge cannot remain only in reports, audits, research, implementation notes, or chat handoffs. OMP remains resilient only while Engineering Report -> Canonical Update -> Current Program State -> next OMP step stays intact.
27. OMP owns Delegated Autonomy Policy progression through existing owners. Current default policy is `dap_default_tier1_readonly`, state `NOT_APPROVED`, current mode `CLASS_APPROVAL`, target mode `DELEGATED_AUTONOMY`, max users per action `1`, runtime apply enabled `NO`.
28. Machine-readable Delegated Autonomy Policy preview and runtime eligibility are read-only surfaces exposed through `admin_core/autonomy_trust_acceleration.py` and `tools/v7-autonomy-trust-evidence-inventory`. They must not enable automation, move users, expand authority, write restore barriers, create evidence, or create duplicate planner/governance/execution/truth.
29. Execution Intent Authority must be treated as semantic reuse of existing authority owners, not as a new document, owner, planner, governance layer, execution path, or truth source. If future work needs this phrase, extend Action-Class Authority, Delegated Autonomy Policy, Runtime Eligibility, or OMP authority evaluation through existing owners.
30. Approval Model Progress must be calculated inside existing OMP/Current Program State ownership if needed. The current canonical inputs are current approval mode, target approval mode, current action-class state, packet-retirement status, delegated policy state, runtime capability state, blocking evidence, and Authority Evolution / Production Autonomy progress.
31. OMP must check `docs/policies/` before implementing or changing operational behavior. If a canonical policy exists, reuse it. If partial, extend it through methodology. If missing, run full world research before implementation.
32. OMP owns Decision Explainability as a permanent capability. Before any operator approval request, V7 must explain the decision in Russian using existing evidence owners; the explanation must show reason, evidence, expected value, risks, alternatives, safety gates, and capability impact before Approve / Reject. Explanation does not authorize runtime action, expand authority, write restore barriers, apply, roll back, move users, or create evidence.
33. The final human operator role is supervision, policy/authority boundary approval, exception handling, and explicit approval for authority expansion. Per-packet and per-routine-action approval are transitional maturity constraints, not the Production Autonomy target. Runtime must own routine certified execution inside approved policy; Product Owner must own business goals, durable product policy, risk appetite, SLA priorities, and approval of policy direction.
34. Business Intent is semantic reuse of Product Specification ownership, not a new owner or document. Product Specification owns product/business intent through Product Mission, Product Principles, Ideal User Experience, Product Success, Evolution Domains, Action-Class Authority, Delegated Autonomy Policy, SLA/service/user fit, and final product behavior. OMP consumes that intent as production leverage, maturity, backlog priority, and authority recommendations. Runtime consumes it only after translation into existing policies, action classes, eligibility gates, SLA/service/user fit, safety gates, and authority bounds.

## V7_CANONICAL_POLICY_LIBRARY

`docs/policies/` is the Canonical Policy Library for V7 operational behavior.

Stable conclusions:

1. The library is documentation-only and creates no planner, governance layer, execution path, runtime owner, truth source, synthetic evidence, apply authority, user movement authority, daemon, timer, or authority expansion.
2. Policy lifecycle is: DISCOVER -> FULL WORLD RESEARCH -> KNOWLEDGE NORMALIZATION -> INDUSTRY CONSENSUS DETECTION -> INDUSTRY DISAGREEMENT DETECTION -> CANONICAL POLICY INTERACTION AUDIT -> REALITY AUDIT -> V7 FIT ANALYSIS -> REUSE EXISTING V7 OWNERS -> CANONICAL POLICY -> IMPLEMENTATION -> VERIFICATION -> CERTIFICATION -> OMP INTEGRATION.
3. Operational implementation before certification is forbidden. The `IMPLEMENTATION` lifecycle step may prepare code or documentation only after a canonical policy exists; runtime enablement waits for `CERTIFICATION` and OMP integration.
4. World research must include all relevant successful systems, including mature network vendors, hyperscalers, cloud platforms, service mesh/proxy systems, routing protocols, RFCs, academic work, production postmortems, operator best practices, and community consensus where applicable.
5. Every policy must record industry consensus, consensus strength, supporting systems, industry disagreement, tradeoffs, V7 applicability, V7 fit analysis, owner reuse, implementation owner, certification state, and open questions.
6. OMP must consult the policy library before any operational behavior change.
7. Initial policy set is `POLICY_001_HARD_FAILURE`, `POLICY_002_SOFT_DEGRADATION`, `POLICY_003_RECOVERY_ADMISSION`, `POLICY_004_AUTHORITY`, `POLICY_005_ACTION_CLASS_PROMOTION`, `POLICY_006_BLAST_RADIUS`, `POLICY_007_ROLLBACK`, `POLICY_008_FRESHNESS`, and `POLICY_009_ANTI_FLAP`.
8. Current library state is `V7_FIT_ANALYSIS_COMPLETE_IMPLEMENTATION_BACKLOG_READY`.
9. Stage 1 `FULL WORLD RESEARCH`, Stage 1.5 `KNOWLEDGE NORMALIZATION`, Stage 2 `INDUSTRY CONSENSUS DETECTION`, Stage 2.5 `CANONICAL POLICY INTERACTION AUDIT`, Stage 3 `REALITY AUDIT`, and Stage 4 `V7 FIT ANALYSIS` are complete for the initial policy set.
10. Stage 4 policy-level classification is: `REUSE` for Authority, Action-Class Promotion, Rollback, Freshness, and Anti-Flap; `ADAPT` for Hard Failure, Soft Degradation, Recovery Admission, and Blast Radius; `REJECT` for no whole policy.
11. Specialized practice-level patterns rejected for current scope include MPLS/router-local repair, DNS recovery, provider replacement as runtime operation, distributed quorum authority, weighted traffic split, and BGP route-flap damping.
12. The implementation backlog derived from Stage 4 is `docs/programs/V7_IMPLEMENTATION_BACKLOG.md`.
13. The implementation priority model is `docs/reference/V7_IMPLEMENTATION_PRIORITY_MODEL.md`.
14. OMP must choose the highest-priority unfinished backlog item by production leverage, mark completed items `DONE`, recalculate backlog priority, and continue automatically unless a canonical stop condition is reached.
15. Current highest backlog item is `A3`: certify class-level rollback/no-rollback evidence for governed candidate movement.
16. Need New Owner remains `FALSE`; the library reuses Product Specification, Research Framework, OMP, Canonical Reference, SYSTEM_MAP, Runtime Model, ADRs, certified reports, and existing implementation owners.

Related ADR: `docs/decisions/ADR-V7-CANONICAL-POLICY-LIBRARY.md`.

## MOVEMENT_PROTECTION_MODEL

Status: `CANONICAL`

Purpose: preserve the production-proven movement protection mechanisms already implemented in V7 so future work extends this knowledge instead of rediscovering it.

Stable conclusions:

1. V7 already protects users from unnecessary movement through existing planner, safety, authority, freshness, recovery, rollback, and read-only anti-flap owners.
2. Primary implementation owners are `tools/v7-users-autoswitch`, `admin_core/autonomy_trust_acceleration.py`, `admin_core/operator_decision_surface.py`, OMP, Runtime Model, and the Canonical Policy Library.
3. Need New Owner remains `FALSE`.
4. Need New Document remains `FALSE`.
5. Movement protection is layered defense-in-depth, not a separate planner or governance model.

Current movement protection mechanisms:

| Mechanism | V7 implementation | Owner / module | Canonical behavior |
| --- | --- | --- | --- |
| Current channel stickiness / stay bias | Current channel score bonus and `sticky_keep_current` explanation | `tools/v7-users-autoswitch` | Keep the current channel unless a real candidate clearly beats it or current channel becomes ineligible. |
| Minimum movement improvement | `_beats_current` policy check | `tools/v7-users-autoswitch` | Planned movement requires both percentage and absolute score improvement over current. |
| Cooldown / hold-down | `_cooldown_ok` | `tools/v7-users-autoswitch` | Recent movement blocks planned, reconnect, or rebalance movement until cooldown expires. |
| User freeze | `_user_frozen` and `_update_safety_after_apply` | `tools/v7-users-autoswitch` | Repeated user movement freezes that user for a safety window. |
| Pair reversal block | `_pair_reversal_blocked_for_user` | `tools/v7-users-autoswitch` | Immediate reversal back to the prior source is blocked inside the stability window. |
| Target block after oscillation | `blocked_targets` safety state | `tools/v7-users-autoswitch` | Repeated target oscillation blocks the intermediate target for a safety window. |
| Egress quarantine | `egress_safety_quarantine` and failed verification quarantine | `tools/v7-users-autoswitch` | Targets with recent failed verification are blocked from new assignments. |
| Rebalance restraint | `_rebalance_needed`, `_best_alternative`, and score-without-sticky checks | `tools/v7-users-autoswitch` | Load balancing moves only when load gap and target quality are sufficient. |
| State change cost / movement economics | Sticky/current-channel bonus, minimum improvement threshold, cooldown, user freeze, pair reversal, target block, egress quarantine, rebalance restraint, authority caps, and blast-radius caps | `tools/v7-users-autoswitch`, `admin_core/autonomy_trust_acceleration.py`, OMP | Movement is treated as a state transition with cost; V7 moves only when benefit, safety, freshness, authority, and rollback conditions justify the transition. |
| Best available pool | `_mark_best_available_pool` | `tools/v7-users-autoswitch` | Candidate pool is constrained to top near-best candidates with service suitability floor. |
| Service persistence | `_service_failure_persistent` and `_gate_service_failures` | `tools/v7-users-autoswitch` | Transient service failures require repeated samples or persistence before hard blocking. |
| Freshness / runtime readiness | Freshness actionability, intelligence snapshot gate, runtime eligibility | `admin_core/autonomy_trust_acceleration.py`, `tools/v7-users-autoswitch`, Runtime Model | Stale or unknown evidence stops mutation-capable decisions. |
| Recovery admission | `build_recovery_admission` | `admin_core/autonomy_trust_acceleration.py` | Recovered channels require repeated success, freshness, cooldown clearance, and limited blast radius. |
| Anti-flap read model | `build_anti_flapping` | `admin_core/autonomy_trust_acceleration.py` | Existing decision/audit records block preview when recent oscillation is detected. |
| Blast-radius and authority caps | `_authority_budget_gate`, requested max selected moves, dynamic blast radius | `tools/v7-users-autoswitch`, OMP | Selected moves are capped by current authority, requested scope, and policy. |
| Rollback protection | Restore barrier, rollback manifest, selected-move identity, verification path | `admin_core/operator_execution.py`, `tools/v7-users-autoswitch` | Movement-capable execution must preserve rollback and selected-move identity. |

Canonical mapping:

| Industry principle | V7 implementation |
| --- | --- |
| Hold-down | Cooldown and recovery cooldown. |
| Dampening | User freeze, target block, pair reversal block, and anti-flap read model. |
| Health thresholds | Quality floors, service persistence, service suitability, and hard/soft service gates. |
| Rollback | Restore barrier, rollback manifest, rollback/no-rollback certification path. |
| Canary | Governed canary and action-class authority ladder. |
| Readiness | Freshness actionability, runtime eligibility, recovery admission, and intelligence snapshot gate. |
| Blast radius | Authority budgets, selected-move caps, dynamic blast-radius summary, and action-class ladder. |
| Consecutive failure threshold | Service failure persistence samples and failure window. |
| Consecutive success threshold | Recovery admission successful-check requirement. |
| Slow start / staged re-entry | Read-only progression is defined through recovery admission, post-admission observation windows, and blast-radius/action-class ladder; runtime consumption and authority remain blocked future work. |
| Max ejection / minimum health | Partially represented by capacity, authority budgets, and blast-radius bounds; pool max-ejection/minimum-health mapping remains a known gap. |
| Operator freeze / manual review | OMP authority boundary, runtime stop, planner freeze/quarantine behavior. |

Current implementation thresholds:

| Threshold | Current canonical value |
| --- | --- |
| Planner cooldown | `180` seconds. |
| Minimum planned movement improvement | `20%` and `50.0` absolute score delta. |
| Current channel sticky bonus | `50.0`. |
| Group preferred egress bonus | `60.0`. |
| Reconnect rotation cooldown | `180` seconds. |
| User freeze threshold, 1h | `2` switches. |
| User freeze duration, 1h | `3600` seconds. |
| User freeze threshold, 24h | `5` switches. |
| User freeze duration, 24h | `21600` seconds. |
| Target block duration | `1800` seconds. |
| Pair reversal window | `900` seconds. |
| Egress quarantine failed verifications | `2` failed verifications in 1h. |
| Egress quarantine duration | `3600` seconds. |
| Current egress grace window | `120` seconds. |
| Post-restore apply suppression window | `120` seconds. |
| Service failure persistence samples | `3` samples. |
| Service failure persistence window | `180` seconds. |
| Service failure minimum critical count | `2`. |
| Quality minimum average Mbps | `15.0`. |
| Quality minimum floor Mbps | `10.0`. |
| Quality minimum stability | `0.45`. |
| Best available pool top N | `3`. |
| Best available pool max score gap | `15%`. |
| Best available pool minimum service suitability | `50.0`. |
| Rebalance minimum user gap | `2`. |
| Rebalance minimum target score ratio | `0.75`. |
| Recovery admission minimum successful checks | `3`. |
| Recovery admission cooldown | `1800` seconds. |
| Limited recovery blast radius | `1` user. |
| Anti-flap cooldown | `1800` seconds. |
| Anti-flap minimum observation window | `3600` seconds. |
| Anti-flap rapid oscillation threshold | `2`. |
| Action authority budgets | CANARY `1`, SMALL_BATCH `2`, MEDIUM_BATCH `5`, LARGE_BATCH `10`, POOL `25`. |

Known remaining gaps:

1. Centralized hysteresis arbitration across hard failure, soft degradation, recovery, freshness, and anti-flap.
2. Explicit per-user `AUTO` / `PINNED` / `MANUAL` routing control mode.
3. Runtime consumption/authority for recovery slow-start.
4. Pool max-ejection / minimum-health mapping into V7-native capacity and blast-radius semantics.

Reaudit rule:

Movement Protection must not be audited again unless one of these is true:

1. planner behavior changes materially;
2. Runtime behavior changes materially;
3. production evidence disproves the current behavior;
4. the operator explicitly requests a re-audit.

Permanent rule:

Future implementation must extend this canonical movement-protection knowledge. It must not rediscover it, create a duplicate movement-protection owner, create a new planner, create new governance, create new execution, or create a new truth source.

## WORLD_EQUIVALENCE_MODEL

Status: `CANONICAL`

Purpose: record how V7 maps to proven engineering practices from mature production systems and prevent future re-research of already proven engineering equivalence.

Industry families compared:

- Cisco;
- Juniper;
- Cloudflare;
- Google SRE;
- Kubernetes;
- Envoy / Istio;
- HAProxy / NGINX;
- AWS / Azure / GCP.

Canonical engineering principles:

| Industry principle | Existing V7 owner | Implementation status | Equivalence | Canonical verdict |
| --- | --- | --- | --- | --- |
| Hold-down | `tools/v7-users-autoswitch`, recovery admission overlay | Implemented | Cooldown, recovery cooldown, restore/post-restore suppression windows | `EQUIVALENT` |
| Dampening | `tools/v7-users-autoswitch`, `admin_core/autonomy_trust_acceleration.py` | Implemented | User freeze, target block, pair reversal block, anti-flap read model | `EQUIVALENT` |
| Health Thresholds | `tools/v7-users-autoswitch`, service matrix, quality compact | Implemented | Quality floors, service persistence, service suitability, hard/soft service gates | `EQUIVALENT` |
| Readiness | Runtime Model, freshness actionability, intelligence snapshot gate | Implemented | Freshness, runtime eligibility, recovery admission, intelligence snapshot gate | `EQUIVALENT` |
| Recovery Admission | `admin_core/autonomy_trust_acceleration.py::build_recovery_admission`, `build_recovery_admission_certification`, `build_post_admission_observation_windows`, `build_recovery_slow_start_progression` | Partially implemented | Repeated success checks, cooldown, freshness, limited recovery blast radius, post-admission observation windows, read-only slow-start progression | `PARTIALLY_EQUIVALENT` |
| Rollback | `admin_core/operator_execution.py`, `tools/v7-users-autoswitch` | Implemented | Restore barrier, rollback manifest, selected-move identity, verification path | `EQUIVALENT` |
| Blast Radius | OMP, `tools/v7-users-autoswitch`, action-class ladder | Implemented | Authority budgets, selected-move caps, dynamic blast-radius summary | `EQUIVALENT` |
| Canary | OMP, governed canary dry-run cycle, action-class authority | Implemented | One-user governed canary, packet preview, restore/rollback preview, outcome closure path | `EQUIVALENT` |
| Progressive Promotion | OMP Autonomy Promotion Engine, Canonical Policy Library | Implemented as policy/readiness; certification still evidence-gated | Action-class states and authority ladder | `EQUIVALENT` |
| Freshness | `admin_core.autonomy_trust_acceleration`, Runtime Model, snapshot owners | Implemented | Freshness actionability, owner-issued freshness fields, runtime stop on stale/unknown evidence | `EQUIVALENT` |
| Runtime Eligibility | Runtime Model, delegated autonomy eligibility read model, OMP | Partially implemented | Existing read-only eligibility gates; runtime automation remains disabled | `PARTIALLY_EQUIVALENT` |
| Authority Separation | OMP, Runtime Model, ADRs, `admin_core/operator_execution.py` | Implemented | Engineering authority, operational authority, action-class authority, delegated policy boundaries | `EQUIVALENT` |
| Outcome Learning | `admin_core/operator_execution_feedback.py`, trust evolution, OMP | Implemented as read-only learning path; requires real outcomes | Outcome closure, learning records, knowledge growth, no synthetic evidence | `EQUIVALENT` |
| Anti-Flap | `tools/v7-users-autoswitch`, `admin_core/autonomy_trust_acceleration.py` | Implemented | Cooldown, freeze, pair reversal, target block, anti-flap overlay | `EQUIVALENT` |
| Stickiness | `tools/v7-users-autoswitch` | Implemented | Current-channel sticky score and `sticky_keep_current` behavior | `EQUIVALENT` |
| Minimum Improvement Threshold | `tools/v7-users-autoswitch::_beats_current` | Implemented | Planned movement requires percentage and absolute score delta over current | `EQUIVALENT` |
| State Change Cost / Movement Economics | `tools/v7-users-autoswitch`, Movement Protection Model, OMP | Implemented semantically | Sticky/current bias, benefit threshold, cooldown, freeze, reversal block, target block, quarantine, rebalance restraint, authority caps, and blast-radius caps | `EQUIVALENT` |
| BGP route-flap damping | None required for current product scope | Not implemented by design | V7 is not currently a routing-protocol owner | `NOT_APPLICABLE` |
| Weighted traffic split | None required for current product scope | Not implemented by design | V7 currently moves users/cohorts, not proxy traffic weights | `NOT_APPLICABLE` |
| Pool max-ejection / minimum-health | Planner capacity/load, blast-radius policy | Partial | Capacity and authority budgets exist; proxy-style max-ejection/minimum-health mapping remains open | `EXTENSION_REQUIRED` |
| Runtime-certified slow-start | Recovery admission, post-admission observation windows, blast-radius/action-class policy | Partial | Read-only staged progression exists; runtime consumption and authority remain open | `EXTENSION_REQUIRED_AFTER_B10` |
| Centralized policy arbitration | Canonical Policy Library, OMP, Runtime eligibility | Partial | Priority/conflict rules exist; implementation-level centralized arbitration remains open | `EXTENSION_REQUIRED` |
| Per-user AUTO / PINNED / MANUAL | Current user registry, group policy, planner | Partial | Current assignment, group preference, and channel flags exist; explicit per-user control mode remains open | `EXTENSION_REQUIRED` |

Canonical verdict:

1. V7 is already equivalent to mature production systems for hold-down, dampening, health thresholds, readiness, rollback, blast radius, canary, progressive promotion, freshness, authority separation, outcome learning, anti-flap, stickiness, and minimum improvement threshold.
2. V7 is partially equivalent for recovery admission and runtime eligibility because the read-only and governed paths exist, while runtime-certified autonomous behavior still requires real evidence and authority.
3. BGP route-flap damping and weighted traffic split are not applicable to current V7 product scope.
4. No fundamental architecture gap was found.
5. Need New Owner remains `FALSE`.
6. Need New Document remains `FALSE`.
7. Confirmed remaining gaps are represented exactly once in the Implementation Backlog or future gated runtime/authority work: centralized policy arbitration by `A6`, per-user `AUTO` / `PINNED` / `MANUAL` by `B21`, recovery slow-start progression completed by `B10` with runtime consumption still gated, and pool max-ejection / minimum-health semantics by `C7`.
8. State Change Cost already exists semantically and extends existing backlog item `B19`; it must not create a new owner, new document, or new backlog item.

Remaining real gaps:

1. Centralized policy arbitration.
2. Per-user `AUTO` / `PINNED` / `MANUAL` routing mode.
3. Runtime consumption/authority for recovery slow-start.
4. Pool max-ejection / minimum-health semantics.

Permanent rule:

Future engineering must first reuse these canonical mappings. It must not repeat world-comparison research, create duplicate owners, create a new planner, create new governance, create new execution, or create a new truth source.

Re-audit trigger:

World Equivalence must not be audited again unless one of these is true:

1. industry consensus materially changes;
2. planner architecture materially changes;
3. Runtime architecture materially changes;
4. the operator explicitly requests a new world comparison.

## V7_DOCUMENT_LIFECYCLE

`docs/reference/V7_DOCUMENT_LIFECYCLE.md` is the canonical rule for permanent document roles.

Stable conclusions:

1. Only `docs/programs/V7_IMPLEMENTATION_BACKLOG.md` drives engineering work.
2. Everything else is knowledge, execution state, historical evidence, or permanent decision record.
3. Reference documents are frozen after certification.
4. The Canonical Policy Library is frozen after Stage 4 V7 Fit Analysis.
5. Reference documents may change only when industry consensus changes, a real implementation proves `FUNDAMENTAL_ARCHITECTURE_GAP`, or the operator explicitly requests a reference update.
6. Program documents are live execution documents and may be updated continuously.
7. The Implementation Backlog is the only live implementation queue.
8. The Implementation Priority Model ranks the backlog; it is not a second queue.
9. Reports are historical evidence only and must never be used as planning queue, roadmap, or direct implementation source.
10. ADRs are permanent decisions and must never be used as implementation queue.
11. Policies, reports, architecture, research documents, ADRs, product documents, and chat history never generate implementation work directly.
12. OMP must always read the highest unfinished backlog item instead of asking what to implement.
13. When the backlog becomes empty, OMP must answer `IMPLEMENTATION_COMPLETE` and stop.

Need New Owner remains `FALSE`.

## V7_PRODUCTION_MATURITY_MODEL

`docs/reference/V7_PRODUCTION_MATURITY_MODEL.md` is the canonical model for calculating V7's Engineering Maturity and Production Maturity scores.

Stable conclusions:

1. Engineering Maturity and Production Maturity are independent dimensions and must never be merged into one score.
2. Engineering Maturity measures completed engineering knowledge: Architecture, Decision Model, Runtime Model, System Architecture, Research, Canonical Policy Library, and OMP.
3. Production Maturity measures production readiness: Implementation, Testing, Production Deployments, Production Outcomes, Certification, Authority Evolution, Production Autonomy, and Implementation Backlog Completion.
4. `100%` Engineering Maturity means `ENGINEERING_COMPLETE`.
5. `100%` Production Maturity means `PRODUCTION_AUTONOMY_CERTIFIED`.
6. Production Maturity must increase only through real implementation, deploy, testing, verification, certification, production outcomes, authority decisions, and certified autonomy.
7. Backlog completion increases only Production Maturity.
8. Reference documents must never change Engineering Maturity after certification unless industry consensus changes, implementation proves `FUNDAMENTAL_ARCHITECTURE_GAP`, or the operator explicitly requests a reference update.
9. OMP must recalculate both maturity dimensions after every implementation, deploy, truth, convergence, certification, production outcome, and authority decision.
10. Current Engineering Maturity is `100.0%`; current Engineering status is `ENGINEERING_COMPLETE`.
11. Current Production Maturity is `64.3%`; current remaining Production Maturity is `35.7%`.
12. Current Production milestone is `50%: Implementation Half Complete`; next Production milestone is `65%: Certification Half Complete`.
13. Current highest implementation task is `C5` Preserve Rollback As Operational Compensation Rather Than Transaction Rollback inside the existing Implementation Backlog.
14. OMP must print `V7 PRODUCTION STATUS` after every execution.
15. Current Production Status is: Engineering Maturity `100.0%`, Production Maturity `64.3%`, Current Autonomy Tier `TIER_1_GOVERNED`, Current Focus `IMPLEMENTATION`, Backlog `31 / 34` actionable complete, Highest Priority Task `C5`, Current Stop Condition `NONE_FOR_C5_ROLLBACK_OPERATIONAL_COMPENSATION_NOT_TRANSACTION_ROLLBACK`.
16. Future normal operator commands are `Continue OMP`, `Status`, `Approve packet`, and `Approve authority expansion`.
17. OMP must never request a new roadmap or new implementation plan.
18. Need New Owner remains `FALSE`.

## V7_KERNEL_AND_STATE_SPLIT

Stable conclusions:

1. `docs/reference/V7_KERNEL.md` is the permanent Codex operating contract for V7 work.
2. OMP is the scheduler/optimizer.
3. `docs/programs/V7_CURRENT_PROGRAM_STATE.md` is the volatile state file for current bottleneck, HLA, packet, authority boundary, metrics, stop reason, and next action.
4. Canonical Reference remains system truth.
5. SYSTEM_MAP remains owner/topology map.
6. ADRs remain accepted decisions.
7. Reports remain evidence and history.
8. Runtime remains reality and final verification.
9. `Continue OMP` means Codex executes the complete Engineering Control Loop through existing owners until an allowed stop condition. It is not only backlog continuation.
10. This split does not create a planner, governance, execution path, runtime truth source, daemon, timer, apply authority, or user movement authority.

## V7_CONTEXT_RESOLVER

`docs/reference/V7_CONTEXT_RESOLVER.md` is the canonical documentation-only rule for resolving the minimum working document set before each task.

Stable conclusions:

1. Codex must classify each task before loading documents.
2. Codex must load only the required working set for that task.
3. Context Resolver prevents unnecessary loading of packet state, current metrics, HLA, research, historical reports, or runtime evidence when they are unrelated to the task.
4. Research, execution, architecture, and documentation tasks have different working sets.
5. Historical reports remain evidence and must not be loaded by default.
6. Runtime truth/convergence remain verification surfaces and contradiction-resolution surfaces, not always-loaded context.
7. Context Resolver extends the existing Kernel source hierarchy, Reference First workflow, OMP semantic reuse rules, and Kernel/State split.
8. Need New Owner remains `FALSE`.
9. This resolver does not create a planner, governance, execution path, truth source, storage, daemon, runtime behavior, apply authority, synthetic evidence, floor change, or user movement authority.
10. Engineering Context Resolver is the operational form of the same owner. It classifies Architecture, Knowledge, Product, Policy, Implementation, Runtime, Production, Certification, Audit, Scale, Bug, Investigation, Operator Request, and Research tasks before loading context.
11. ECR must answer what is required, verified, current, historical, refresh-required, ignorable, reopened, implementation-bound, certification-bound, and runtime-investigation-bound.
12. ECR uses existing owners only: Product Specification, Audit Knowledge State, Canonical Reference, SYSTEM_MAP, Current Program State, OMP, Implementation Backlog, Runtime Model, Production Maturity Model, Knowledge Quality Model, policies, ADRs, and reports as evidence only.
13. For `Continue OMP`, the default ECR working set is Product Specification -> Audit Knowledge State -> Canonical Reference -> Current Program State -> OMP -> Current Backlog Item.
14. ECR prevents future Codex/AI agents from starting with full-project reads or report-first rediscovery.
15. `Continue OMP` is the single default engineering command and must run: Engineering Context Resolver -> Knowledge Consumption -> Re-open Evaluation -> OMP Execution -> Implementation/Audit/Certification/Verification -> Engineering Report -> Knowledge Promotion -> Current Program State Update -> OMP Update -> Continue OMP.
16. `Continue OMP` stops automatically when operator authority, runtime apply, production movement, architecture contradiction, missing canonical owner, re-open trigger, or product contradiction is encountered; it continues automatically when only implementation, documentation, integration, certification, verification, or knowledge promotion remains.

Related ADR: `docs/decisions/ADR-V7-CONTEXT-RESOLVER.md`.

## ENGINEERING_CONTEXT_RESOLVER_FINAL_AUDIT

Status: `ENGINEERING_CONTEXT_RESOLVER_OPERATIONAL`

Purpose: preserve the final architecture audit for the Engineering Context Resolver so future engineering work starts with minimal authoritative context and avoids repeated rediscovery.

Stable conclusions:

1. An implicit Engineering Context Resolver already existed through Context Resolver, Reference First, Knowledge Plane, OMP, Current Program State, SYSTEM_MAP, Canonical Reference, and Implementation Backlog.
2. The correct action is `EXTEND_EXISTING`, not `CREATE_NEW`.
3. ECR is not a new owner, truth source, audit registry, planner, governance layer, runtime path, roadmap, or backlog.
4. ECR must classify every task before context loading.
5. ECR task classes are Architecture, Knowledge, Product, Policy, Implementation, Runtime, Production, Certification, Audit, Scale, Bug, Investigation, Operator Request, and Research.
6. Each task class has mandatory context, optional context, forbidden-by-default context, and authoritative owners.
7. Historical reports are evidence only and must not be current truth or first-read context unless the resolver determines evidence is required.
8. ECR must determine whether knowledge is already verified, still current, historical only, refresh-required, ignorable, re-opened, implementation-bound, certification-bound, or runtime-investigation-bound.
9. `Continue OMP` is the default engineering command because ECR resolves its working set to Product Specification, Audit Knowledge State, Canonical Reference, Current Program State, OMP, and current Backlog item, then hands execution to the complete Engineering Control Loop.
10. Need New Owner remains `FALSE`; Need New Backlog Item remains `FALSE`; runtime impact is `NONE`.
11. Architecture phase remains complete. ECR strengthens execution discipline; it does not reopen architecture.
12. World-practice verdict: ECR matches mature engineering practice in Google SRE, AWS/Cloudflare control planes, Kubernetes controllers, ADR workflows, and large engineering organizations by separating current truth, durable knowledge, historical evidence, ownership, and execution state.

Re-open rule:

ECR must not be re-audited unless:

1. Context Resolver ownership changes materially;
2. Knowledge Plane ownership changes materially;
3. OMP workflow changes materially;
4. future work again starts from reports/full-project loading and creates rediscovery loops;
5. production evidence contradicts current knowledge-consumption order;
6. the operator explicitly requests re-audit.

## V7_RESEARCH_FRAMEWORK

`docs/programs/V7_RESEARCH_FRAMEWORK.md` is the permanent owner for architectural research methodology.

Stable conclusions:

1. Research Framework optimizes knowledge acquisition; OMP optimizes implementation.
2. Architectural research must follow the loop: Question → Resolve Context → Collect Sources → Validate Sources → Extract Patterns → Cross-System Comparison → Universal Principle → Compare With V7 → Reuse Analysis → Gap Classification → Recommendation → Canonical Update.
3. Research never invents architecture and never copies vendor architecture.
4. Research searches only for reusable engineering principles proven in mature production systems.
5. Every recommendation must prove mature production use, purpose, problem solved, V7 equivalent owner, reuse path, extension path, and why a new owner is or is not required.
6. Gap classifications are `ALREADY_EXISTS`, `EXISTS_BUT_UNDERUSED`, `READ_MODEL_MISSING`, `REAL_OUTCOME_REQUIRED`, `AUTHORITY_REQUIRED`, `FUTURE_SCALE_OPTIONAL`, and `FUNDAMENTAL_ARCHITECTURE_GAP`.
7. New architecture can be recommended only after extension of existing V7 owners is proven impossible.
8. Need New Owner remains `FALSE`.
9. Research Framework is documentation-only and does not create runtime behavior, execution behavior, a planner, governance layer, truth source, synthetic evidence, apply behavior, floor change, or user movement.

Research Standard:

Every architectural research must include:

- Universal Engineering Laws;
- Cross-System Comparison Matrix;
- V7 Mapping;
- Gap Classification;
- Reuse Analysis;
- Canonical Recommendations.

Research is complete only when universal principles are extracted, engineering laws are extracted, the comparison matrix is completed, V7 is mapped, gaps are classified, reuse path is defined, and canonical docs are updated.

Related process: `docs/reference/V7_RESEARCH_PROCESS.md`.
Related ADR: `docs/decisions/ADR-V7-RESEARCH-FRAMEWORK.md`.
Related ADR: `docs/decisions/ADR-V7-RESEARCH-STANDARD.md`.

## V7_DECISION_MODEL

`docs/reference/V7_DECISION_MODEL.md` is the canonical documentation-only read model for how V7 makes, exposes, escalates, verifies, and learns from decisions.

Stable conclusions:

1. V7 decisions must follow the loop: Event / Question -> Current State -> Desired State / Policy -> Evidence Quality -> Service / User / Channel Fit -> Risk / Blast Radius -> Decision Vocabulary -> Authority Gate -> Packet / Preview / Stop -> Verification -> Outcome -> Learning.
2. The canonical decision vocabulary remains `KEEP`, `MOVE`, `FAILOVER`, `DRAIN`, `QUARANTINE`, `RECOVER`, `PROBE_ONLY`, `ASK_OPERATOR`, and `NO_ACTION`.
3. Scores, diagnostics, raw health checks, and confidence fields explain decisions; they must not become a second decision model.
4. World-class decision principles map to existing V7 owners: desired/current reconciliation, policy/enforcement separation, symptom-first decisions, health/readiness gates, staged blast radius, human escalation, outcome learning, and thin runtime all already exist.
5. Two principles are underused and must be named in future decision work: make-before-break sequencing and live decision handoff state.
6. Overall gap classification is `READ_MODEL_MISSING`, now closed by `docs/reference/V7_DECISION_MODEL.md`.
7. Need New Owner remains `FALSE`; existing V7 decision owners are sufficient.
8. The model does not create a planner, governance layer, execution path, truth source, storage path, runtime behavior, apply behavior, floor change, synthetic evidence, or user movement authority.
9. The completed World-Class Decision Model research now contains the permanent research-standard shape: Universal Engineering Laws and Cross-System Comparison Matrix.

Related report: `docs/reports/V7_WORLD_CLASS_DECISION_MODELS_RESEARCH_REPORT.md`.
Related ADR: `docs/decisions/ADR-V7-WORLD-CLASS-DECISION-MODEL.md`.

## V7_RUNTIME_MODEL

`docs/reference/V7_RUNTIME_MODEL.md` is the canonical design contract for executable V7 Runtime.

Stable conclusions:

1. Runtime executes already-approved Decision Model snapshots; Runtime does not invent decisions.
2. Runtime follows the lifecycle: Event -> Runtime Wakeup -> Read Current Program State -> Read Decision Snapshot -> Policy -> Safety -> Authority -> Packet -> Execute OR Stop -> Verify -> Rollback if needed -> Outcome -> Learning -> Update Current Program State -> Notify OMP -> Sleep.
3. Runtime may wake only from approved existing sources: explicit operator/OMP invocation, certified regression event, existing governed canary lifecycle, or recorded-state resume.
4. Runtime composes existing owners: Event-Driven Autonomy Contract, Current Program State, Decision Model, Planner / Autoswitch, Safety-Bounded Authority, Execution Packet owner, Restore Barrier / Rollback, Runtime Readiness, truth/convergence, feedback, learning, and OMP.
5. Runtime must stop safely on missing/stale decision, policy block, safety block, authority boundary, invalid packet, duplicate work, loop guard, inconclusive verification, rollback authority boundary, unavailable outcome, or learning without real observed outcome.
6. Runtime restart and duplicate detection are idempotency-key based and must use durable existing identifiers: decision id, operation id, packet id, selected move hash, current state generation, restore barrier generation, rollback target, verification result id, and outcome closure id.
7. Runtime updates Current Program State only as a program continuation surface; Current Program State is not a runtime truth source.
8. Runtime feeds learning only from real observed outcomes.
9. Need New Owner remains `FALSE`; Runtime is an existing-owner composition contract.
10. Runtime must not ask for packet approval when an action class is already `AUTONOMOUS_RUNTIME` and policy, subject, target class, blast radius, freshness, safety, rollback/no-rollback, verification, learning, and authority generation remain inside certified bounds.
11. Runtime must generate or consume a fresh packet immediately before execution and verify that it belongs to the approved Action Class. Packet validity must not depend on a long-lived operator approval.
12. Runtime must stop or ask when the class is uncertified, governed-only, not class-approved, authority is exceeded, policy changed, risk exceeds certified blast radius, the packet does not match class authority, or required safety/freshness/rollback/verification/learning gates fail.
13. Runtime may execute automatically only inside an approved Delegated Autonomy Policy when action class, fresh packet, rollback, verification, anti-flap, blast radius, freshness, evidence, and known-failure-mode gates all pass.
14. This design does not implement runtime code, daemon/timer enablement, event consumer changes, autonomous execution, apply, user movement, planner changes, governance changes, execution changes, truth-source changes, floor changes, synthetic evidence, restore-barrier writes, or rollback apply.

Related report: `docs/reports/V7_RUNTIME_MODEL_DESIGN_REPORT.md`.
Related ADR: `docs/decisions/ADR-V7-RUNTIME-MODEL.md`.

## V7_SYSTEM_ARCHITECTURE

`docs/reference/V7_SYSTEM_ARCHITECTURE.md` is the canonical final architecture synthesis for V7 as one integrated production routing control plane.

Stable conclusions:

1. V7 is one event-driven routing control system: runtime reality -> evidence -> knowledge -> decision -> runtime -> verification -> feedback -> learning -> knowledge -> OMP -> sleep.
2. The final architecture verdict is `ARCHITECTURE_COMPLETE`.
3. Remaining architectural weaknesses: `0`.
4. Optional future scale/maturity improvements: `4`.
5. Need New Owner remains `FALSE`.
6. Runtime implementation may begin only as a separate implementation phase using existing owners and explicit approval boundaries.
7. Runtime implementation must not redesign Planner, Governance, Execution, Truth, Evidence, OMP, Decision Model, or Current Program State.
8. Missing real outcomes, missing evidence, stale packet state, and authority boundaries are current reality/operation limits, not architectural weaknesses.
9. New planner, governance, execution, truth source, evidence collector, runtime owner, lifecycle, or architecture owner is unnecessary unless a future ADR proves `FUNDAMENTAL_ARCHITECTURE_GAP`.
10. This synthesis does not implement code, runtime, daemon, timers, apply, user movement, truth-source creation, synthetic evidence, floor changes, restore-barrier writes, or rollback apply.

Related report: `docs/reports/V7_SYSTEM_ARCHITECTURE_SYNTHESIS_REPORT.md`.
Related ADR: `docs/decisions/ADR-V7-SYSTEM-ARCHITECTURE.md`.

## ARCHITECTURE_CLOSED_BY_DEFAULT

Status: `CANONICAL`.

Purpose: record the permanent V7 rule that architecture is complete by default and architecture evolution is the last resort.

Canonical rule:

Every newly discovered problem, idea, regression, optimization, or improvement must first be treated as one of:

- unfinished implementation;
- missing integration;
- missing certification;
- missing runtime consumption;
- missing read-model consumption;
- missing production evidence;
- missing authority maturity;
- missing capability progress;
- missing backlog completion;
- missing canonical-owner update.

Before proposing an architectural extension, OMP must prove that the existing OMP, Runtime Model, Product Specification, Canonical Policies, Implementation Backlog, canonical owners, SYSTEM_MAP, and Canonical Reference cannot own the finding through reuse, extension, integration, certification, read-model consumption, runtime consumption, authority maturity, or production evidence.

Default verdicts:

| Field | Default |
| --- | --- |
| Architecture complete | `TRUE` |
| Need New Owner | `FALSE` |
| Need New Backlog Item | `FALSE` |
| Architecture Extension | `LAST_RESORT` |

Architecture extension may be proposed only after a complete audit proves `FUNDAMENTAL_ARCHITECTURE_GAP`.

This rule does not change runtime behavior, planner behavior, governance, execution, truth sources, policies, backlog, authority, apply behavior, daemon/timer behavior, synthetic evidence rules, or user movement.

## V7_IMPLEMENTATION_PHASE

`docs/programs/V7_IMPLEMENTATION_PROGRAM.md` and `docs/reference/V7_IMPLEMENTATION_MODEL.md` define supporting implementation rules under OMP. OMP Version `4.0` is the single permanent production execution program; these files are not separate roadmap authorities.

Stable conclusions:

1. Architecture Phase is closed.
2. Research Phase is closed.
3. Decision Model is complete.
4. Runtime Model is complete.
5. System Architecture is complete.
6. Future work is implementation-first.
7. OMP optimizes `Production Leverage`, not architectural completeness.
8. Architecture changes require implementation evidence proving `FUNDAMENTAL_ARCHITECTURE_GAP`.
9. Implementation priority order is: existing owner implementation, existing owner integration, existing owner optimization, read-model improvements, testing, certification.
10. Every implementation task must be classified before work begins.
11. OMP now owns continuous production maturity evolution after Implementation Phase activation.
12. Current highest implementation leverage task lives in `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.
13. Need New Owner remains `FALSE`.
14. This phase does not authorize restore-barrier writes, runtime apply, user movement, rollback apply, daemon/timer enablement, event consumer mutation, authority expansion, floor changes, synthetic evidence, new planner, new governance, new execution, storage, runtime owner, or truth source.

Related ADR: `docs/decisions/ADR-V7-IMPLEMENTATION-PHASE.md`.

## V7_ENGINEERING_PRINCIPLES

`docs/reference/V7_ENGINEERING_PRINCIPLES.md` is the canonical engineering principles document for Safety-Bounded Authority.

Stable conclusions:

1. Trust decides autonomy tier.
2. Safety decides bounded action.
3. Knowledge Maturity and Execution Authority must not be collapsed into one concept.
4. `70/70/70` remains the floor for `TIER_2+` and autonomous progression.
5. A `TIER_1` governed one-user canary can be valid for explicit operator approval even while `TIER_2` remains blocked.
6. Background systems build knowledge: service intelligence, suitability, prediction, trust, recovery state, capacity intelligence, history, learning, and snapshots.
7. Runtime spends knowledge: event -> current state -> knowledge snapshot -> policy -> safety -> packet -> execute/stop.
8. Runtime must not perform broad audits, broad analytics, or long historical recomputation during the event path.
9. The principle does not create a new planner, governance, execution, truth source, evidence source, storage, daemon, timer, or authority model.
10. The principle does not authorize restore-barrier writes, runtime apply, user movement, rollback apply, daemon/timer enablement, floor changes, or synthetic evidence.
11. OMP remains the execution authority. If future work conflicts with OMP, OMP wins unless explicitly changed by the user.

Related ADR: `docs/decisions/ADR-V7-SAFETY-BOUNDED-AUTHORITY.md`.

## V7_IDEAL_AUTONOMOUS_ROUTING_MODEL

1. Ideal V7 is an event-driven autonomous routing control plane for `10,000+` users and `100+` channels.
2. The ideal control loop is: observe -> classify -> decide -> plan -> limit blast radius -> execute only if authorized -> verify -> rollback if needed -> learn -> update knowledge.
3. V7 must behave like desired-state reconciliation, not a blind timer. The desired state is user/service/channel assignments that satisfy policy, SLA, freshness, capacity, route safety, and recovery constraints.
4. The ideal action vocabulary is `KEEP`, `MOVE`, `FAILOVER`, `DRAIN`, `QUARANTINE`, `RECOVER`, `PROBE_ONLY`, `ASK_OPERATOR`, and `NO_ACTION`.
5. Channel Score remains diagnostics. Channel Decision remains planner/governance truth.
6. Evidence must mature from `RAW_OBSERVATION` to `STABLE_SIGNAL`, `CONFIRMED_KNOWLEDGE`, `ACTIONABLE_KNOWLEDGE`, and only then `AUTONOMY_GRADE_KNOWLEDGE`.
7. Data quality means freshness, coverage, correctness, consistency, diversity, source confidence, user impact relevance, service relevance, and actionability. Row count alone is not knowledge quality.
8. Current V7 already has most owners: observation, service matrix, planner, governed execution, restore barrier, rollback, feedback, learning, trust, prediction, event read-only consumer, operator surfaces, and truth/convergence.
9. Current gaps to ideal are service/user/SLA fit, passive real-user outcome closure, recovery admission, anti-flapping, autonomous rollback certification, explicit evidence maturity labels, active freshness/decay behavior, aggregated read models, and 10k-scale cohort/SLA operator views.
10. The exact next phase is `V7.KNOWLEDGE.QUALITY.MODEL`, using existing owners only.
11. No code, formula, floor, planner, governance, execution, truth source, runtime apply, daemon, autoswitch, synthetic evidence, or user movement changed in `V7.IDEAL.AUTONOMOUS.ROUTING.SYSTEM.MODEL`.
12. Related model / report / ADR: `docs/reference/V7_IDEAL_AUTONOMOUS_ROUTING_MODEL.md`, `docs/reports/V7_IDEAL_AUTONOMOUS_ROUTING_SYSTEM_MODEL_REPORT.md`, ADR-V7-IDEAL-AUTONOMOUS-ROUTING-MODEL.
13. Last verified commit: `61088d7a9fa48cc593a5cf2b681f520e8734b59d`.

## V7_KNOWLEDGE_QUALITY_MODEL

1. V7 must distinguish data, signal, knowledge, and action authority.
2. High-quality routing knowledge is fresh, covered, correct, consistent, diverse, source-confident, user-impact relevant, service-relevant, and actionable.
3. Knowledge maturity stages are `RAW_OBSERVATION`, `STABLE_SIGNAL`, `CONFIRMED_KNOWLEDGE`, `ACTIONABLE_KNOWLEDGE`, and `AUTONOMY_GRADE_KNOWLEDGE`.
4. Current V7 has broad routing knowledge, but only Safety Knowledge is currently classified as autonomy-grade. Channel, User Assignment, Policy, and Trust are actionable for governed review; Capacity, Failure, Decision Outcome, Prediction, and Event are confirmed; Service, Route, Quality, Recovery, Suitability, and Freshness remain stable signals; Operator Context remains raw/underfed.
5. Current autonomy blockers are knowledge-quality blockers, not missing planner/execution architecture: service/user/SLA fit, passive real-user outcome closure, recovery admission, suitability correctness, source confidence, freshness/decay, cohort/SLA knowledge, autonomous rollback certification, anti-flap knowledge, and contextual operator evidence.
6. Future reports must name the weak knowledge object and weak dimension instead of saying generic "more evidence needed".
7. `V7.KNOWLEDGE.QUALITY.READ_MODEL` is implemented through the existing read-only owner `admin_core/autonomy_trust_acceleration.py` and existing CLI surface `tools/v7-autonomy-trust-evidence-inventory`.
8. The read model exposes `knowledge_objects`, `maturity_distribution`, `tier_readiness_knowledge`, `10k_readiness`, and `p0_gaps`. It is deterministic, references `docs/reference/V7_KNOWLEDGE_QUALITY_MODEL.md`, and marks all scores as canonical rather than heuristic.
9. The read model is not an action authority. It does not change formulas, floors, planner, governance, execution, truth source, runtime apply, daemon state, autoswitch, storage, synthetic evidence, or user movement.
10. Related model / report / ADR: `docs/reference/V7_KNOWLEDGE_QUALITY_MODEL.md`, `docs/reports/V7_KNOWLEDGE_QUALITY_MODEL_REPORT.md`, `docs/reports/V7_KNOWLEDGE_QUALITY_READ_MODEL_REPORT.md`, ADR-V7-KNOWLEDGE-QUALITY-MODEL.
11. Last verified commit before read-model implementation: `64654b3a9a70f3aea06119104120e214a7d70571`.

## AUTONOMY_TRUST_SOURCE_HIERARCHY

1. Observed network outcome is the primary autonomy trust source for V7.
2. Primary sources are observed service outcome, observed channel quality, post-switch verification, rollback/no-rollback result, forecast-to-actual accuracy, and future client telemetry when implemented.
3. Operator comparison, operator override, and manual approval are secondary supervised evidence. They are useful only when the operator has enough operational context.
4. Manual operator actions are authoritative system actions, but they are not synthetic agreement with V7's autonomous recommendation.
5. After a manual action, V7 should respect the action and then observe service/channel outcome quality through existing evidence owners.
6. Operator comparison must not be used as blind bulk training data. Do not require an operator to manufacture comparison history for users whose real service quality they cannot directly observe.
7. Diagnostic sources such as raw technical health, route details, logs, and score components support explanation and troubleshooting; they are not primary autonomy trust sources by themselves.
8. Canary readiness must still block when primary observed-outcome confidence, trust, or prediction evidence is insufficient. Operator comparison may accelerate supervised confidence but does not replace observed outcome evidence.
9. Implementation owner for read-only classification: `admin_core/autonomy_trust_acceleration.py`; CLI surface: `tools/v7-autonomy-trust-evidence-inventory`.
10. Related ADR: `docs/decisions/ADR-OBSERVED-OUTCOME-PRIMARY-TRUST.md`.

## AUTONOMY_EXPERIENCE_CONFIDENCE_MODEL

V7 experience is the accumulated observed evidence that connects a real operational state or action to a later real outcome. It is not a single score and not operator opinion alone.

Canonical flow:

```text
Reality
  -> Observation
  -> Evidence
  -> Outcome
  -> Suitability
  -> Confidence
  -> Trust
  -> Planner
  -> Action
```

Current production forensic truth from `AUTONOMY.CANDIDATE_OUTCOME.REALITY.COLLECTION`:

1. Prediction experience is complete for the current window: `21/21` matched rows. It is undervalued as raw accuracy evidence, but intentionally limited by low forecast source confidence.
2. Service/channel experience exists (`21` rows) and is fresh, but source row confidence remains low at about `0.39`, so it cannot certify autonomy by itself.
3. Candidate/suitability experience is consumed but incomplete: `84` real selected-candidate outcomes against `156` candidates, with `72` missing candidate outcomes.
4. Suitability is genuinely low, not merely hidden: current mean correctness is `62.132`, mean candidate confidence is `0.407`, and suitability confidence is `27.569`.
5. Blast and rollback experience are sufficient and contribute `100`; they are not current canary blockers.
6. Operator comparison evidence is secondary supervised confirmation and remains underfed (`0` comparisons in this forensic pass).
7. Read-only visibility and aggregation gaps were fixed in existing owners: the inventory now exposes `candidate_outcome_reality_collection`, trust refresh uses the full decision family for candidate outcomes, and snapshot refresh reads the extended JSONL evidence window. Final production classification reports `captured_but_not_consumed=0`, `visibility_issue=0`, and `aggregation_issue=0`.
8. The final verdict is `OUTCOME_EVIDENCE_INCOMPLETE`: the experience pipeline exists and consumes available reality, but canary remains blocked because `72` candidate user/channel outcomes have not happened yet and `43` consumed outcomes are still weakly weighted.

Related reports: `docs/reports/AUTONOMY_SUITABILITY_KNOWLEDGE_AND_CONFIDENCE_FORENSICS_REPORT.md`, `docs/reports/AUTONOMY_CANDIDATE_OUTCOME_REALITY_COLLECTION_REPORT.md`.
Implementation owner: `admin_core/autonomy_trust_acceleration.py`.

## HIGHEST_LEVERAGE_OUTCOME_GROWTH

1. V7 must not assume that governed canary is automatically the highest-leverage next action.
2. The existing trust inventory owner now exposes a read-only `outcome_leverage_model` that ranks real outcome activities by expected floor gain per effort and risk.
3. Current production verdict is `MIXED_PATH`: prediction outcome cycles are highest leverage for prediction, service verification cycles are safest for service/trust source confidence, and governed/manual candidate outcomes are mandatory for suitability.
4. A governed one-user canary is valuable as real candidate/suitability reality, but one canary is too small to close TIER_2 by itself.
5. TIER_2 requires a mixed path: prediction forecast -> actual cycles, service verification outcome cycles, governed/manual candidate suitability outcomes, and feedback/outcome/learning closure after every real action.
6. The model is projection-only. It does not change formulas, floors, planner, governance, execution, truth source, storage, daemon state, runtime apply, synthetic evidence, or user movement.
7. Implementation owner: `admin_core/autonomy_trust_acceleration.py`.
8. CLI surface: `tools/v7-autonomy-trust-evidence-inventory`.
9. Related report: `docs/reports/V7_HIGHEST_LEVERAGE_OUTCOME_GROWTH_REPORT.md`.
10. Last verified runtime commit: `3cf500befeb33d368baef0998e5d6d36da46b8a3`.

## PRODUCTION_SCALE_FIRST

Status: `CANONICAL`.

Purpose: record the permanent V7 rule that every future change must remain efficient, safe, and maintainable at production-control-plane scale.

Product Scale Model:

- Canonical product owner: `docs/product/V7_PRODUCT_SPECIFICATION.md`.
- Canonical product section: `Product Scale Model`.
- Product vision subsection: `Product Scale Objectives`.
- Meaning: Product Scale Model is the product-level non-functional requirement, planning constraint, and long-term scale optimization target for target production scale.
- Execution consumer: OMP consumes Product Scale Model through `Production Scale First`.
- Runtime consumer: Runtime consumes Product Scale Model indirectly through OMP, Runtime Model work, Implementation Backlog, read models, and runtime eligibility implementation.
- This is not a new owner, not a new roadmap, not a new policy, and not a new runtime path.

Scale target:

- `10,000+` users;
- `100+` channels;
- millions of runtime decisions;
- long-lived evidence, telemetry, reports, and learning history.

Canonical rule:

Every future audit, implementation, test, report, policy change, runtime change, evidence model change, learning change, read model, UI/API data-loading change, storage change, background job, canonical update, and OMP decision must answer:

```text
Will this remain efficient, safe, and maintainable at 10,000+ users and 100+ channels?
```

Long-term Product Scale Objectives:

1. Runtime cost for one bounded runtime decision should remain approximately constant as the system grows.
2. Memory growth should remain controlled and should avoid large in-memory global state.
3. Storage growth should be predictable; raw evidence should be retained once while summaries, indexes, and read models are derived.
4. Heavy CPU work belongs to background processing, aggregation, and offline analysis.
5. Operator and API paths should read summarized views by default.
6. Learning should become incremental where equivalent incremental updates are possible.
7. Reports remain compact historical evidence; canonical owners store durable knowledge.
8. V7 should evolve toward bounded cost growth rather than cost proportional to users, channels, history size, or telemetry size.
9. Architecture should evolve toward scale-independent operation where practical, with representative evidence preferred over exhaustive enumeration when safety is preserved.
10. Increasing deployment size should have minimal impact on the cost, latency, and operational complexity of processing one bounded runtime decision.

Owner reuse:

| Concern | Existing owner |
| --- | --- |
| Product scale truth | `V7_PRODUCT_SPECIFICATION.md` -> `Product Scale Model` |
| Execution discipline | `OPERATIONAL_MATURITY_PROGRAM.md` |
| Thin runtime rule | `V7_RUNTIME_MODEL.md` |
| Production maturity impact | `V7_PRODUCTION_MATURITY_MODEL.md` |
| Durable canonical truth | `V7_CANONICAL_REFERENCE.md` |

No new owner, roadmap, policy, runtime path, planner, governance layer, execution path, truth source, or backlog item is created by this rule.

Mandatory scale checks:

| Check | Canonical requirement |
| --- | --- |
| Algorithmic complexity | Avoid `O(N^2)` behavior and full rescans where possible. Prefer `O(1)`, `O(log N)`, bounded scans, incremental updates, indexes, and summaries. |
| Runtime path safety | Runtime must remain thin and consume prepared/certified read models. Expensive work belongs to background jobs, pre-aggregation, or offline analysis. |
| Storage discipline | Store evidence once and derive summaries. Avoid duplicated durable data and unbounded growth without retention or compaction strategy. |
| Read-model discipline | UI, API, and operator views must use summaries, indexes, and drill-down. Normal views must not read massive raw histories. |
| Evidence and learning scale | Full enumeration of all user-to-channel combinations must not become a permanent autonomy blocker unless explicitly justified. Prefer representative action-class evidence, risk segmentation, blast radius, rollback/no-rollback proof, and learning quality. |
| Reporting discipline | Engineering reports are compact historical evidence. Durable knowledge belongs in canonical owners. Large raw outputs should be referenced or summarized. |
| Indexing and query discipline | Every new persistent data shape must declare lookup pattern and indexing/aggregation strategy when it grows with users, channels, or time. |
| Resource budget | Future implementation must consider CPU, memory, disk, IO, latency, and write amplification. |

Production scale validation questions:

1. Does runtime cost grow with user count?
2. Does storage grow without bounds?
3. Does CPU cost grow linearly?
4. Does memory growth remain controlled?
5. Can reports grow indefinitely?
6. Can telemetry be aggregated?
7. Can read models be precomputed?
8. Are indexes sufficient?
9. Can expensive work move out of Runtime?
10. Will this still be operationally efficient at production scale?

If the answer proves the proposal is not suitable for production scale, the proposal must be redesigned through existing owners before implementation. V7 must not lower production scale expectations.

Permanent re-audit trigger:

Production Scale First must be re-audited only when one of the following is true:

1. Product scale target changes materially.
2. Runtime architecture changes materially.
3. Evidence or learning model changes materially.
4. Production telemetry proves the current scale assumptions wrong.
5. Explicit operator request.

## POST_PRODUCTION_SCALE_PHASE

Phase name: `AUTONOMY.EVIDENCE.INDEX_AND_FRESHNESS_MODEL`.

Status: `DEFERRED_UNTIL_PRODUCTION_AUTONOMY_CERTIFIED`.

Purpose: prepare V7 for `100+` channels, `10,000+` users, and years of evidence without planner slowdown, trust distortion, or irrational use of stale data.

This is not a current blocker. It is documentation of a future scalability phase. It does not authorize runtime changes, code changes, planner changes, trust changes, execution changes, new owners, new schemas, new storage, or new truth sources.

Evidence classification for the future phase:

| Class | Name | Examples | Future meaning |
| --- | --- | --- | --- |
| A | Fast Reality | Telegram, YouTube, latency, packet loss, Service Matrix, Route Readiness | Fresh operational probes that age quickly and should influence current state only while fresh. |
| B | Channel Behavior | Stability, speed, failure rate, recovery rate, quality trend | Medium-horizon behavior evidence that describes how a channel behaves over time. |
| C | Outcome Evidence | Candidate outcomes, governed outcomes, manual outcomes, post-switch verification | Direct proof that decisions or movements produced good or bad real outcomes. |
| D | System Safety Evidence | Blast, rollback, restore, packet validity, feedback closure, learning closure | Safety evidence proving V7 can act, verify, recover, and learn inside bounded governance. |

Future evidence index concept:

| Field | Meaning |
| --- | --- |
| `evidence_id` | Stable id for the future catalog row. |
| `timestamp` | Time the evidence was observed or closed. |
| `evidence_type` | Class/type of evidence, for example service probe, candidate outcome, rollback proof. |
| `channel_id` | Channel scope when applicable. |
| `service_id` | Service scope when applicable. |
| `owner` | Existing owner that produced the evidence. |
| `quality_score` | Current quality/correctness meaning, calculated by existing owners only. |
| `freshness_score` | Future freshness/age weighting, shadow-only until certified. |
| `confidence_score` | Existing confidence meaning from current models, not a new trust engine. |
| `weight` | Future derived weighting after shadow validation. |

Freshness principles:

1. Old evidence is not deleted.
2. Old evidence loses weight.
3. Freshness depends on evidence type.
4. Telegram/service probe evidence and blast/rollback safety evidence must not age identically.
5. Freshness must not change planner, trust, or execution behavior until it has passed shadow validation.

Future aggregated read models:

| Read model | Intended future role |
| --- | --- |
| `channel_current_summary` | Compact current channel state for planner/operator reads. |
| `channel_service_summary` | Service availability and freshness summary. |
| `channel_behavior_summary` | Stability, speed, failures, recovery, and quality trend summary. |
| `candidate_outcome_summary` | Candidate and assignment outcome summary. |
| `system_safety_summary` | Blast, rollback, restore, packet, feedback, and learning safety summary. |
| `trust_evolution_summary` | Existing trust evolution summarized for scalable reads. |

Cardinality control rules:

1. Allowed dimensions should stay bounded: evidence type, channel, service, owner, time bucket, and outcome class.
2. High-cardinality risk comes from per-user, per-request, per-packet, per-log-line, and unbounded raw event dimensions.
3. Future mitigation should use existing-owner aggregation, bounded time windows, summaries, and retention-aware indexes before planner consumption.
4. Raw detail may remain in evidence/history stores, but planner-facing reads should use aggregated summaries.

Shadow validation rule:

Any future freshness/index model must first run in shadow mode with no direct planner impact, no direct trust impact, no direct execution impact, and no direct governance impact. It must compare old behavior versus freshness-weighted behavior before promotion.

Integration rule:

Any future implementation must reuse existing owners, existing truth sources, existing planner, existing governance, and existing execution path. It must not create a new trust engine.

Activation criteria:

1. Production Autonomy is certified.
2. Event-driven autonomy is operating through the existing chain: regression -> planner -> packet -> restore barrier -> bounded apply -> feedback -> learning.
3. Evidence volume or query cost demonstrates a real scale need, such as `100+` channels, `1000+` users, or multi-year evidence history.
4. A shadow freshness/index validation proves no trust distortion and no planner regression.
5. Truth and convergence pass before and after any future implementation.

Related ADR: `docs/decisions/ADR-FUTURE-EVIDENCE-INDEX-AND-FRESHNESS-MODEL.md`.

## Channels Final UX Rules

1. Channel Decision V7 is primary.
2. Channel table signals stay compact and are explained by the S/L/R/T header legend plus one V7-styled tooltip source.
3. Only one tooltip source is allowed for signal dots; native browser `title` tooltips must not duplicate custom tooltips.
4. Channel diagnostics use a balanced layout: summary first, then responsive reality-first diagnostic cards.
5. Diagnostics primary text is reality-first, not score-first; score math and point loss must not dominate the operator view.
6. Trust/recovery metadata must not compete with Channel Decision V7 in the first-level Channels table.
7. Every channel warning must be actionable. A visible warning must explain one of three outcomes: existing safe action and where it opens, automatic handling and what updates it, or why no safe action is available.
8. Channel drawer first screen must remain a compact operator inspection surface, not a form-like stack of nested cards. The first screen answers: channel, V7 decision, reason, next safe action, active problems, compact signals, and where engineer diagnostics live.
9. Ambiguous labels such as "check", "verify", "clarify", or "attention" are not enough on channel surfaces. If evidence is incomplete, the wording must say the reality and next step, for example "fresh data unavailable", "open service matrix", "open users", "open logs", "automatic refresh pending", or "safe action unavailable".
10. Operator Surface and Engineering Surface are separate. The Channel Drawer first screen must not show `score/100`, technical health/rating, confidence labels, raw status/state, evidence, history, logs, execution details, or service matrix details. Those belong behind the Engineer Diagnostics boundary.
11. The aggregate `Сигналы` table column is a compact visual container, not a sortable truth. Channel ordering may use individual first-level signals only: Services, Load, Runtime, or Stability.

## Channel Drawer Operator Rules

1. Channel identity is shown once, in the drawer header.
2. Decision is shown once.
3. Reason is shown once.
4. Operator view contains no score math, score badges, confidence labels, raw technical state, service matrix detail, evidence, execution, logs, settings, or debug content.
5. Every first-screen signal is actionable: clicking the signal opens an inline explanation and the existing safe destination when one exists.
6. Every first-screen problem is actionable: clicking the problem opens an inline explanation and the existing safe destination when one exists.
7. If no safe action exists, the UI explains why inside the same drawer.
8. Engineering diagnostics has one entry point and remains collapsed below the operator answer.
9. Settings and debug content must not appear in the operator view.
10. First-screen operator wording must avoid vague labels such as `Уточнить`, `Требует проверки`, and `Уверенность неполная`; use concrete reality-first wording such as `Нет свежих данных`, `Нет свежего подтверждения`, `Открыть матрицу сервисов`, `Открыть пользователей`, `Открыть логи`, or `Действие недоступно`.

## CHANNEL_OPERATOR_LANGUAGE_RULES

1. Decision first: Channel Decision V7 is the final operator answer.
2. Reason second: the first reason explains why V7 wants that decision.
3. Signals third: signals explain confidence and evidence behind the decision; they are not a second decision model.
4. Engineering hidden: scores, formulas, raw readiness, trust math, capacity math, planner internals, evidence, and logs stay behind Engineering Diagnostics.
5. Yellow never overrides decision: yellow signals mean attention or freshness limits, not "do not use" by themselves.
6. Red may influence decision: red signals can participate in `Evacuate`, `Blocked`, or other assignment restrictions and must explain the impact in operator language.
7. Signal details must answer `What happened`, `Why`, and `What to do`, without using a competing `Decision` field.
8. Problem details must answer `What happened`, `Why it matters`, and `What can be done now`.
9. Operator copy must avoid developer-only terms on the first screen, including raw `runtime`, `confidence`, `evidence`, `snapshot`, `eligibility`, `trust score`, and planner/gate internals.
10. If a warning does not change the decision, the UI must say that plainly, for example: "does not prohibit use" or "follow V7 decision".

## OPERATOR_ACTION_FLOW_RULES

1. Every operator-visible channel issue must explain itself.
2. Every issue detail must show a consistent structure: status, reason, decision impact, and action.
3. Every issue must explicitly explain whether it affects Channel Decision V7.
4. Every issue must explain whether operator action is required, optional, automatic, or unavailable.
5. Action categories are `Observe`, `Review`, and `Execute`; `Execute` may only prepare or open an existing governed flow.
6. Action rows must state where the action leads and what result the operator should expect.
7. A visible issue must not end at explanation only. If no safe action exists, the UI must say why in the same expanded item.
8. Problem details and signal details use the same action-flow structure.
9. Existing destinations are reused: Service Matrix, channel users, channel logs, engineering diagnostics, and governed user/action flows.
10. This rule does not create new planner logic, routing logic, signal calculations, governance, storage, or execution paths.

## CHANNEL_ATTENTION_RULES

1. Channels attention is a derived operator view, not a new truth source.
2. Channels attention must reuse existing Channel Decision V7, Overview Attention, first-level channel signals, service matrix, capacity/load, runtime readiness, stability, and channel status.
3. Attention priority is strict: Critical, Action Required, Review, Information, Healthy.
4. Critical means the operator should look first because users may need to leave or users are on a channel V7 should not use.
5. Action Required means an existing safe destination/action exists now.
6. Review means the channel needs fresh evidence or inspection but does not override Channel Decision V7 by itself.
7. Information means the role/state matters but can wait when no users or active problems are affected.
8. Healthy means Use or Keep with first-level operator signals OK; these channels can be ignored during triage.
9. Attention First sorting may reorder the Channels table by derived attention priority, assigned users, first-level signal severity, existing default operator order, and channel name.
10. Default table mode must preserve existing channel table behavior and manual sort settings.
11. The aggregate `Сигналы` column must not become a sortable truth. Attention ordering may use individual first-level signal severities only.
12. Attention visual styling must stay calm: urgent rows may have a narrow marker, while healthy rows remain visually quiet.
13. Attention entries must open existing destinations only: Channel Drawer, Service Matrix, channel users, logs/diagnostics, or existing governed user/action flows.
14. This rule does not change planner logic, assignment logic, execution, governance, signal calculations, decision logic, capacity formulas, routing formulas, storage, or database state.

## POOL_AUTONOMY_RUNTIME_RULES

1. V7 autonomy has been certified through governed execution up to 10 users, but that certification is not the same as a continuously enabled production daemon.
2. WireGuard `wireguard-1779454504-c43409` is promoted into the production pool and is a valid production channel, subject to the same planner/capacity/load gates as every other channel.
3. POOL.2 evidence on 2026-06-19 showed `POOL_NEEDS_RECOVERY`: active distribution `awg3=8`, `wireguard=8`, `vless=10`, with 8 failover candidates from `awg3` to `wireguard-1779454504-c43409`.
4. POOL.3 evidence on 2026-06-21 showed active distribution still `awg3=8`, `wireguard=8`, `vless=10`; `awg0` remained below stability floor; `awg3` was barely above stability floor but below min-speed floor and hard-full; WireGuard remained technically strong but hard-full. Fresh available API evidence did not reproduce the old 8-user awg3-to-WireGuard failover as an actionable current apply.
5. Current truth says `autoswitch_scheduler_active=false` and `autoswitch_service_active=false`, with inactive scheduler approved as manual mode.
6. Production autonomy direction is event-driven autonomy: channel/service regression -> planner -> packet -> restore barrier -> bounded apply -> verification -> rollback decision -> feedback -> learning.
7. Timer-only movement is rejected as a product model. Periodic probes and previews may run; periodic blind user movement must not run.
8. Any future production autonomy daemon must reuse existing planner, packet, restore barrier, execution, rollback, feedback, learning, truth, and convergence owners.

## EVENT_TRIGGER_READ_ONLY_CERTIFICATION

1. EVENT.1 evidence on 2026-06-21 certified the current event-driven autonomy trigger chain as read-only and blocked for live production apply.
2. Existing regression/evidence sources include `tools/v7-telegram-sentinel`, service matrix refresh, egress quality compaction, route/runtime/capacity read models, and planner blocker transitions.
3. The existing chain can preview planner output, execution packet draft, restore barrier ownership, rollback model, feedback model, and learning/confidence evidence without moving users.
4. EVENT.1 current truth: `preview_only=true`, `read_only=true`, `execution_allowed_now=false`, `apply_executed=false`, `users_moved=0`, `rollback_executed=false`, and `autonomy_enabled=false`.
5. EVENT.1 blockers were `confidence_too_low`, `trust_too_low`, `prediction_confidence_too_low`, operator comparison evidence below floor, restore barrier readiness blocked, and no certified live event consumer binding from regression evidence to governed planner trigger.
6. `v7-telegram-sentinel` is an event/regression source, but current service mode uses `--no-autoswitch`; it is not a certified production apply trigger.
7. EVENT.1 final verdict is `EVENT_TRIGGER_BLOCKED`.
8. EVENT.CONSUMER.READONLY.2 certified the missing read-only event consumer link without enabling apply. Existing production events now flow through `admin_core/events.py` into `admin_core/operator_execution_pipeline.py::event_consumer_readonly_certification_model`, which previews planner, packet, restore barrier, rollback, feedback, and learning surfaces without mutation.
9. EVENT.CONSUMER.READONLY.2 evidence used 10 real production event rows from Telegram Sentinel and Service Matrix. The read-only certification produced `event_count=10`, `primary_event_count=10`, `packet_preview_count=1`, `restore_preview_count=1`, `rollback_preview_count=1`, `feedback_preview_count=1`, `learning_preview_count=1`, `apply_executed=false`, `users_moved=0`, and `autonomy_enabled=false`.
10. The event consumer is now certified only as read-only. It is not a daemon, not an apply authority, not a new truth source, and not permission to move users. The next safe phase is readiness recheck plus evidence collection until confidence, trust, prediction, restore barrier, rollback, feedback, and learning gates pass together.

## AUTONOMY_CANARY_READINESS

1. AUTONOMY.CANARY.1_READINESS_RECHECK on 2026-06-23 returned `AUTONOMY_CANARY_NO_GO`.
2. The canary blocker is not missing architecture. Existing owners for event consumer, planner preview, packet preview, restore barrier preview, rollback preview, feedback preview, and learning preview are present and read-only certified.
3. Current production floors remain below the `70.0` canary requirement: confidence `39.606`, trust `54.705`, prediction confidence `36.859`, and secondary operator earned confidence `45.807`.
4. Current production comparison evidence remains underfed: comparison count `0`, agreement rate `0.0`, reviewable decisions `27`.
5. Current prediction lifecycle is durable but under-confident: `21/21` forecasts matched actuals, `0` pending rows, forecast accuracy `97.189`, and prediction confidence `36.859`.
6. Blast and rollback are not current blockers: blast radius confidence is `100.0` and rollback confidence is `100.0`.
7. The current planner observe run selected `0` moves and stopped with `dry_run_intelligence_snapshot_stop_required`; snapshot stop families were `service-scores` and `channel-service-scores`.
8. Snapshot refresh dry-run is stable and non-mutating: `source_stable=true`, `snapshot_count=11`, `runtime_behavior_changed=false`, `governance_behavior_changed=false`, and `users_moved=false`.
9. Production autonomy remains disabled. No apply, no user movement, no daemon enablement, no autoswitch enablement, no threshold/floor/formula change, no synthetic evidence, and no new truth source occurred.
10. Shortest safe path before another canary decision: snapshot gate / candidate recheck through existing owners, real observed service/channel outcome collection, prediction source-confidence collection, contextual supervised operator comparison if useful, then another canary readiness recheck.
11. AUTONOMY.CANARY.1A on 2026-06-23 returned `CANDIDATE_VISIBILITY_BLOCKED`.
12. Current production planner evidence shows `candidate_moves_total=18` with distribution `awg3=8`, `wireguard-1779454504-c43409=8`, and `vless=10`, but normal `v7-users-autoswitch --mode observe` still returns `selected_move_count=0` because snapshot gate stops on `service-scores` and `channel-service-scores` source mismatch against `service_matrix`.
13. Standalone `v7-intelligence-snapshot-refresh --pretty` is snapshot-only and safe (`source_stable=true`, `snapshot_count=11`, `runtime_behavior_changed=false`, `governance_behavior_changed=false`, `users_moved=false`), but by itself does not make the normal planner observe path persistently pass the snapshot gate.
14. Planner-owned refresh through existing `v7-users-autoswitch --mode observe --max-selected-moves 1 --pre-planner-refresh=write --pre-planner-refresh-command=/usr/local/bin/v7-intelligence-snapshot-refresh` clears snapshot gate inside that observe run (`stop_required=false`, `stop_families=[]`) without apply or user movement, but the run then stops at `dry_run_restore_barrier_clearance_generation_expired`.
15. AUTONOMY.CANARY.1B on 2026-06-23 implemented the smallest existing-owner durability fix in `tools/v7-users-autoswitch`: normal read-only `--mode observe` now auto-enables the existing pre-planner snapshot refresh owner when no explicit pre-refresh mode is supplied; explicit modes still win and `--apply` does not auto-enable refresh.
16. After deploy, production normal observe reports `snapshot_gate.stop_required=false`, `stop_families=[]`, `pre_planner_refresh.auto_enabled=true`, `pre_planner_refresh.state=REFRESH_SUCCESS`, and then stops at `dry_run_restore_barrier_clearance_generation_expired`.
17. Candidate visibility is now real on the normal observe path: production reports `candidate_moves_total=8`; canary-limited observe exposes the fresh candidate `10.0.0.2` from `awg3` to `wireguard-1779454504-c43409` before the restore guard.
18. A fresh execution packet preview for that one canary candidate validates as `PACKET_VALID` with `runtime_action=CREATE_RESTORE_BARRIER_CLEARANCE`, but no packet execution, restore-barrier write, apply, user movement, daemon, synthetic evidence, floor change, or new truth source occurred.
19. Canary is still blocked by restore: the current production restore barrier clearance expired on `2026-06-13T19:29:19.851623+00:00`, references planner generation `1fd508b2fc82598d134f3defb598dd6593f0decd3da8437d953e788c3d3c098b`, and contains an old approved plan lock for 10 `vless` moves. The fresh generation is `d4098562a46e2cb32db70bab1943d638637198b896423da9b633f79d8e250080`, so reusing the old lock is correctly rejected with `approved_plan_lock_expired` and `approved_plan_lock_user_source_mismatch`.
20. AUTONOMY.CANARY.1B final verdict is `CANARY_BLOCKED_BY_RESTORE`. The next safe phase is explicit governed restore-barrier clearance generation through the existing `tools/v7-operator-execution-packet` / `admin_core/operator_execution.py` owner, followed by another readiness recheck. This must not move users unless a later phase separately authorizes apply.
21. AUTONOMY.CANARY.1C on 2026-06-23 implemented the smallest existing-owner restore-barrier lifecycle fix: `admin_core/operator_execution.py` can now run a read-only `runtime_action_preview` for `CREATE_RESTORE_BARRIER_CLEARANCE` via `tools/v7-operator-execution-packet --preview-runtime-action`.
22. The new preview does not write the restore barrier, does not append audit/lifecycle state, does not apply autoswitch, and does not move users. It preserves duplicate active owner denial and returns explicit non-mutation flags.
23. Production 1C evidence shows `candidate_moves_total=8`; a fresh packet `pkt_09e0c1125bc0a6016abbb5a6` selects one canary move: `10.0.0.2 awg3 -> wireguard-1779454504-c43409`.
24. Restore-barrier preview now passes for that fresh packet with `ALLOW_RESTORE_BARRIER_CLEARANCE` and `RESTORE_BARRIER_CLEARANCE_PREVIEW_VALID`; the clearance preview uses generation `d4098562a46e2cb32db70bab1943d638637198b896423da9b633f79d8e250080` and selected move count `1`.
25. The valid clearance preview survives reread and an explicit snapshot refresh. Normal production observe still stops at `dry_run_restore_barrier_clearance_generation_expired` because 1C intentionally did not write clearance state.
26. After restore preview is clear, the next canary blocker is evidence confidence: confidence `39.558`, trust `54.668`, prediction confidence `36.511`, and secondary operator earned confidence `45.837`, all below the `70.0` floor.
27. AUTONOMY.CANARY.1C final verdict is `CANARY_BLOCKED_BY_CONFIDENCE`; the next safe phase is real existing-owner confidence/trust/prediction evidence closure, not runtime apply.
28. AUTONOMY.TIER1.GOVERNED_CANARY.READINESS on 2026-06-24 prepared and validated a fresh governed one-user canary packet without apply, movement, daemon enablement, runtime write, floor/formula change, synthetic evidence, or new truth source.
29. Fresh production reality changed from the older 1C candidate: `v7-users-autoswitch --mode observe --max-selected-moves 1` now exposes one planner-selected pre-guard canary candidate `10.7.0.5 vless -> awg0`. The older WireGuard target remains a strong candidate but is not the selected current target; target-constrained WireGuard observe produced no selected pre-guard move.
30. The fresh packet `pkt_7c64f53a8fd169a07445c438` validates as `PACKET_VALID` for operation `govexec_ebf49d9c3f11a0cdd04cd738`; its rollback manifest maps `10.7.0.5 awg0 -> vless`.
31. Production registry-backed restore preview for that packet passes with `ALLOW_RESTORE_BARRIER_CLEARANCE` and `RESTORE_BARRIER_CLEARANCE_PREVIEW_VALID`; it writes no record, performs no runtime mutation, performs no user movement, and does not apply autoswitch.
32. Current trust inventory reports `TIER_1 MARGINAL_OPERATOR_REVIEW`: confidence `38.82`, trust `54.115`, prediction confidence `35.514`, operator earned confidence `45.815`, rollback confidence `100.0`, and `72` missing candidate outcomes. Autonomous one-user canary remains `NO_GO`.
33. Final verdict for the phase is `TIER1_GOVERNED_CANARY_MARGINAL`: V7 can prepare a complete governed one-user canary packet, but execution still requires a separate explicit operator approval for the exact packet and target. Because the target is now `awg0`, operator review is mandatory before any apply.

## AUTONOMY_RISK_TIERED_FLOOR_MODEL

1. V7 uses tiered floor semantics for autonomy readiness as of AUTONOMY.FLOOR.SEMANTICS_AND_RISK_TIER_REVIEW.
2. The implementation is read-only semantics in `admin_core/operator_execution_pipeline.py::autonomy_risk_tier_floor_model`, `admin_core/operator_execution_pipeline.py::autonomy_risk_tier_review`, and `admin_core/autonomy_trust_acceleration.py::build_canary_proximity`.
3. Existing hard autonomous canary floors were not lowered: confidence `70.0`, trust `70.0`, and prediction confidence `70.0` still block bounded autonomous one-user canary readiness.
4. The accepted tiers are:
   - `TIER_0`: read-only preview, no apply, no movement.
   - `TIER_1`: first one-user governed canary review. If absolute safety gates are clean but confidence floors are low, status may be `MARGINAL_OPERATOR_REVIEW`; this is not `AUTONOMY_CANARY_GO`.
   - `TIER_2`: governed canary requiring hard `70/70/70`.
   - `TIER_3`: bounded autonomous one-user canary requiring hard `70/70/70` and a future explicit autonomy authority.
   - `TIER_4`: bounded autonomous small batch requiring `85/85/85`.
   - `TIER_5`: batch autonomy requiring `90/90/90`.
   - `TIER_6`: production autonomy requiring `95/95/95`; not granted by the current program.
5. Non-negotiable gates stay absolute for every movement tier: candidate exists, packet valid, rollback target known, restore barrier available before apply, snapshot gate clean, no hard service/capacity blocker, and existing runtime owner only.
6. Current certified values simulate as `TIER_1 MARGINAL_OPERATOR_REVIEW` and `TIER_3 NO_GO`: confidence `38.872`, trust `54.154`, prediction confidence `35.385`, rollback confidence `100`.
7. This model changes wording and readiness classification only. It does not change formulas, thresholds, runtime apply, planner, governance, execution, daemon status, autoswitch status, or truth source.
8. Related report / ADR: `docs/reports/AUTONOMY_FLOOR_SEMANTICS_AND_RISK_TIER_REVIEW_REPORT.md`, `docs/decisions/ADR-AUTONOMY-RISK-TIERED-FLOORS.md`.
9. AUTONOMY.TIER1.GOVERNED_CANARY.READINESS confirms the same tier semantics on fresh production evidence: `TIER_1 MARGINAL_OPERATOR_REVIEW`, `TIER_2+ NO_GO`, and no autonomous apply authority. Current planner-selected TIER_1 packet is `10.7.0.5 vless -> awg0`; the packet and restore preview are valid, but execution is still a separate governed apply decision.

## AUTONOMY_TRUST_SUFFICIENCY_MODEL

1. Trust sufficiency means "enough trust for this tier", not "enough trust for every autonomy tier".
2. Current stable verdict is `TRUST_MODEL_MIXED`.
3. The model is correct and safe for blocking autonomous canary and production autonomy: current production remains `TIER_2+ NO_GO` and autonomous one-user canary remains `NO_GO`.
4. The model is also correct for `TIER_1`: a first one-user governed canary may be `MARGINAL_OPERATOR_REVIEW` when non-negotiable gates are clean, but this is not an autonomous GO.
5. The mixed part is semantic/operational clarity: `70/70/70` must be described as the hard governed/autonomous progression boundary for TIER_2 and TIER_3+, not as a requirement to merely prepare a TIER_1 operator-reviewed packet.
6. Current production facts remain: prediction `21/21`, candidate outcomes `84/156`, missing outcomes `72`, blast `100`, rollback `100`, capture/visibility/aggregation loss `0`, confidence about `38.8`, trust about `54.1`, prediction confidence about `35.5`, operator earned confidence about `45.8`.
7. Full candidate coverage alone is not sufficient. Current projection for converting all `72` missing candidate outcomes reaches only about confidence `51.832`, trust `62.794`, suitability `52.769`, and still fails primary canary floors.
8. Prediction is undervalued as raw accuracy but fairly discounted as autonomy source confidence because the formula is `mean(matched_forecast_accuracy) * mean(forecast_confidence)`.
9. Blast and rollback confidence make a bounded governed canary safer, but they do not substitute for prediction, service, or suitability evidence.
10. No floor, formula, planner, governance, execution, truth source, daemon, autoswitch, runtime apply, synthetic evidence, or user movement changed in AUTONOMY.TRUST.SUFFICIENCY.MODEL.
11. The exact next phase is `AUTONOMY.TIER1.GOVERNED_CANARY.APPLY_DECISION`: approve or reject packet `pkt_7c64f53a8fd169a07445c438` (`10.7.0.5 vless -> awg0`) through existing owners only.
12. Related report / ADR: `docs/reports/AUTONOMY_TRUST_SUFFICIENCY_MODEL_REPORT.md`, ADR-AUTONOMY-TRUST-SUFFICIENCY-TIER-AWARE.
13. Last verified commit: `d4ee291be875b825fb883d835621c8530c8eda8c`.

## AUTONOMY_EVIDENCE_SATURATION_MODEL

1. Evidence saturation means "enough real evidence for this component and tier", not "no more evidence can ever be useful".
2. Current stable verdict is `SATURATION_MODEL_PARTIAL`.
3. V7 can theoretically reach trust, confidence, and autonomy readiness saturation: prediction, service, suitability, blast, rollback, and operator comparison confidence models are bounded on a `0..100` scale and can converge to `100` with high-quality real evidence.
4. V7 can also remain below floor forever if future evidence is low-confidence, wrong, non-representative, stale, or missing. More rows alone are not saturation.
5. Current blocker is quality and correctness, not hidden data: prediction has `21/21` matches but low source confidence; candidate suitability has `84/156` outcomes and `72` missing, and full current candidate coverage alone still projects below floor.
6. Blast and rollback are already saturated enough for the current safety role (`100`), but they do not saturate prediction, service, or suitability.
7. A component is saturated for a tier when non-negotiable gates are clean and either the component crosses the tier floor or additional same-source evidence would not change the tier decision.
8. Future autonomy phases must not ask for generic "more evidence"; they must name the unsaturated component, the target tier, current value, floor, and exact real evidence that can change the decision.
9. No code, formula, floor, planner, governance, execution, truth source, runtime apply, daemon, autoswitch, synthetic evidence, or user movement changed in AUTONOMY.EVIDENCE.SATURATION.MODEL.
10. Related report / ADR: `docs/reports/AUTONOMY_EVIDENCE_SATURATION_MODEL_REPORT.md`, ADR-AUTONOMY-EVIDENCE-SATURATION.
11. Last verified commit: `55ad5436f50ce0563b26a990d5c5ad175dcfdfa7`.

## AUTONOMY_ROOT_CONFIDENCE_TRUST_MODEL

1. V7 has two related but separate confidence layers: governed execution evidence and operator-free autonomy evidence.
2. Governed execution evidence comes from certified BA runs, execution outcomes, feedback, rollback readiness, and intelligence snapshots. It can raise inherited execution trust.
3. Operator-free autonomy evidence is stricter: it must prove safe autonomous trigger, self-stop, rollback decision, observed outcome quality, confidence floors, and operator-free apply boundary. Operator comparison is secondary supervised confirmation, not the primary proof.
4. BA1/BA3/BA4 evidence is consumed by `trust-evolution-summaries`; EVENT.1 reports `evidence_produced=true`, `evidence_stored=true`, `evidence_visible=true`, `evidence_consumed=true`, and `evidence_weighted=true`.
5. BA evidence does not automatically certify production autonomy. It currently raises inherited execution trust to `87.048`, while autonomy-specific trust remains `0.0` and autonomy-specific gap remains `100.0`.
6. Current candidate floor gates are owned by `admin_core/operator_execution_pipeline.py`. Floors are `confidence >= 70`, `trust >= 70`, and `prediction_confidence >= 70`.
7. Current EVENT.1 values are `confidence=45.8`, `trust=39.584`, and `prediction_confidence=39.6`; all are below floor, so apply must stop.
8. Outcome evidence is active and consumed from `trust-evolution-summaries`, but current component quality is insufficient: decision `50.0`, service `39.225`, suitability `29.528`, blast-radius `0.0`, prediction `37.355`, rollback `100.0`.
9. Shadow comparison evidence is owned by `admin_core/shadow_autonomy.py` and the existing `/api/actions/shadow-autonomy-compare` endpoint. Current production comparison count is `0`, so earned confidence remains about `45.802`, but this is a secondary supervised signal and must not force blind operator review.
10. Missing primary evidence must be collected through existing owners only: observed service/channel outcomes, matched prediction actuals, matched service/candidate outcomes, post-action verification, rollback/no-rollback evidence, and explicit blast-radius evidence. Read-only event consumer certification is complete, but evidence floors still block apply.
11. Lowering floors, adding a new planner, adding a new execution path, or enabling a timer/daemon to move users would violate the current autonomy model.
12. Last verified commit: `68b4153e95712b1ac432ccfac785561025ea4aed`.

## AUTONOMY_EVIDENCE_COLLECTION_RULES

1. Operator comparison evidence is collected only through the existing shadow autonomy comparison path: `/api/actions/shadow-autonomy-compare`.
2. A comparison record is valid only when a real operator judges a current shadow `decision_id` as `agree`, `disagree`, or `override`. Synthetic agreement records must not be generated to raise confidence.
3. The comparison endpoint writes `operator_comparison` records to the existing shadow autonomy JSONL store and admin audit, while reporting `runtime_mutation_performed=false`, `users_moved=0`, `apply_executed=false`, and `autonomy_enabled=false`.
4. Operator comparisons raise shadow `comparisons_total`, agreement rate, and earned confidence. They do not directly raise candidate trust or prediction confidence, and they are secondary supervised evidence rather than the primary autonomy trust path.
5. Prediction confidence improves only through existing matched prediction actuals from service/channel evidence, existing governed prediction feedback, and intelligence snapshot refresh. Current EVENT.1 evidence has `prediction_actuals_count=21`, `prediction_confidence=37.355` from outcome evidence, and final candidate prediction confidence `39.6`.
6. Service confidence improves through existing service matrix / channel-service score / quality evidence consumed by `service_intelligence_trust_model`. Current EVENT.1 service confidence is `39.225`.
7. Candidate confidence improves through existing candidate suitability and governed outcome evidence. Current EVENT.1 has `candidate_outcomes_count=83`, `suitability_confidence=29.528`, and final candidate confidence `45.8`.
8. Blast-radius confidence is owned by the existing `blast_radius_confidence_model` and `build_blast_radius_evidence_rows`; current EVENT.1 value is `0.0`, meaning consumed records did not classify into explicit usable blast-radius evidence.
9. Evidence collection may update evidence stores and snapshots only through existing owners. It must not create a new evidence store, planner, governance path, execution path, confidence model, trust model, prediction model, or truth source.
10. OPERATOR.COMPARISON.COLLECTION.1 implemented the durable existing-owner comparison collection path. `admin_core/shadow_autonomy.py` now exposes an operator review packet, per-decision comparison eligibility, and growth projection using the existing earned-confidence formula. `admin/v7-admin-api` reads active and rotated shadow-autonomy JSONL family records and preserves comparison rows separately from decision rows so old real comparisons are not displaced by newer shadow decisions.
11. Production inventory on 2026-06-23 found 27 users, 27 reviewable current shadow decisions, 0 comparison records, agreement rate `0.0`, earned confidence `45.802`, and user distribution `awg3=8`, `wireguard-1779454504-c43409=8`, `vless=11`.
12. Real operator comparison evidence must still be collected through the existing UI/API. The path is ready; the evidence volume is not.
13. Implementation commit: `f86148dc70a3a4d039dc41b555060ae0d2d4f13e`; deploy id `deploy-z8-14-Updatesystem-f86148d-20260623T094821`.
14. AUTONOMY.TRUST.ACCELERATION.1 added a read-only evidence inventory owner: `admin_core/autonomy_trust_acceleration.py` and `tools/v7-autonomy-trust-evidence-inventory`.
15. The trust acceleration inventory is a derived read model only. It may expose prediction collection plans, operator review batches, growth projections, and canary proximity, but it must not create synthetic comparisons, synthetic actuals, runtime apply, user movement, daemon enablement, new storage, new planner, new governance, new execution, new confidence model, or new truth source.
16. Production trust acceleration inventory after final deploy and snapshot refresh found 27 reviewable decisions, 0 reviewed decisions, 0 comparisons, agreement rate `0.0`, and earned confidence `45.802`.
17. The inventory exposes review batches for 5, 10, and 15 current decisions. A 5-comparison batch is insufficient for the `70.0` earned-confidence floor even at 100% agreement (`59.352`). A 10-comparison batch reaches the floor only at 100% agreement (`72.901`). A 15-comparison batch reaches the floor at 90% (`78.951`) or 80% (`71.451`) agreement, but not at 75% (`67.701`).
18. If operator comparison evidence is collected, it should use only recommendations where the operator has enough context. It must not be blind bulk training data. All comparison evidence must still pass through `/api/actions/shadow-autonomy-compare`.
19. AUTONOMY.TRUST.ACCELERATION.1 final verdict is `AUTONOMY_TRUST_ACCELERATION_PARTIAL`.
20. Implementation commits: `fd868640185461abb42f0e010e3beada9e6d9fc2`, `43effb2a7a58a545fd90d48db53bbe1c0968a75b`; final deploy id `deploy-z8-14-Updatesystem-43effb2-20260623T101511`.
21. AUTONOMY.TRUST.SOURCE.REALITY.1 reclassified operator comparison as secondary supervised confirmation and observed network outcome as the primary trust source. The read-only inventory now exposes `trust_source_classification`, `operator_authority_model`, `primary_real_evidence_path`, `secondary_supervised_confirmation_path`, and `blind_operator_training_required=false`.

## AUTONOMY_PREDICTION_EVIDENCE_RULES

1. Prediction confidence is calculated by `admin_core/intelligence_platform.py::prediction_accuracy_model`.
2. Forecasts are generated by `admin_core/intelligence_workers.py::build_prediction_snapshot` from existing service matrix, quality summary, risk, trust, and blast-radius evidence.
3. Forecast rows are extracted from existing `channel_forecasts` and `service_forecasts` by `admin_core/intelligence_workers.py::_prediction_forecast_rows`.
4. Prediction actuals are built by `admin_core/intelligence_workers.py::build_prediction_actual_rows` from existing service/channel score rows, bounded decision records, and existing governed prediction feedback fields (`prediction_expected`, `prediction_actual`) when present.
5. Forecasts match actuals by existing row keys: `id`, `channel`, `service`, `target`, `user`, or positional index.
6. The current formula is `prediction_confidence = mean(matched_forecast_accuracy) * mean(forecast_confidence)`, where matched accuracy is `100 - abs(predicted_quality - observed_quality)`.
7. The autonomy gate merges prediction values with `max(candidate_prediction_confidence, outcome_prediction_confidence)` and requires `prediction_confidence >= 70.0`.
8. AUTONOMY.PREDICTION.EVIDENCE.1 production forensics on 2026-06-22 found `forecasts_seen=21`, `prediction_actuals_built=21`, `matched_count=21`, `unmatched_forecasts=0`, `ignored_service_actuals=0`, mean accuracy `98.488`, mean forecast confidence `0.3792`, and outcome prediction confidence `37.351`.
9. The current prediction blocker is not missing matches. The blocker is low forecast/source confidence: accurate predictions are multiplied by low forecast confidence, keeping the result around `37.351` while the gate floor is `70.0`.
10. Current candidate prediction confidence remains `39.6`, so the final autonomy gate remains blocked by `prediction_confidence_too_low`.
11. Raising prediction confidence must use existing evidence owners only: repeated real forecast-to-later-actual comparisons, existing governed prediction feedback, fresher service/quality/trust/blast inputs, existing snapshot refresh, and existing shadow/operator comparison evidence.
12. Synthetic prediction actuals, changed confidence floors, changed prediction formula, new prediction owner, new planner, new governance path, new execution path, or new truth source are forbidden.
13. AUTONOMY.PREDICTION.EVIDENCE.2 implemented the existing-owner lifecycle fix in `admin_core/intelligence_workers.py`: direct governed prediction feedback now becomes prediction actual evidence through the existing `build_prediction_actual_rows` path.
14. Direct prediction feedback is consumed from the full existing decision stream so older feedback can survive refresh/rebuild/reread even when newer non-prediction records fill the bounded tail. Service/channel actuals remain bounded through the existing bounded decision set.
15. Local lifecycle proof in `docs/reports/AUTONOMY_PREDICTION_EVIDENCE_2_EVIDENCE/local_prediction_feedback_lifecycle.json` shows an old existing feedback record outside the 1000-row bounded tail still produces `prediction_actuals_count=1`, `matched_count=1`, `prediction_confidence=88.2`, and survives snapshot write/reread.
16. Production baseline before the fix was still `forecast_rows=21`, `matched_count=21`, `prediction_actuals_count=21`, and `prediction_confidence=36.992`; after safe deploy and snapshot refresh it remained `forecast_rows=21`, `matched_count=21`, `prediction_actuals_count=21`, and `prediction_confidence=36.651`. Current production confidence did not rise because no additional matching direct prediction feedback was present in the refreshed production evidence set.
17. The improvement is evidence durability/consumption, not a formula or floor change. Next safe phase: continue real outcome/source confidence and operator comparison evidence collection; do not enable operator-free autonomy until confidence/trust/prediction/comparison/event-consumer gates pass.
18. Implementation commit: `87ce1986a5b71751ed20fb82dd4b799f505f3928`.
19. AUTONOMY.TRUST.ACCELERATION.1 production inventory after final deploy and snapshot refresh found `forecasts_seen=21`, `forecast_actuals_seen=21`, `service_actuals_seen=21`, `matched_rows=21`, `pending_rows=0`, forecast accuracy `97.194`, and prediction confidence `36.861`.
20. Current prediction acceleration truth: there are no pending forecast rows to match, so adding "missing actuals" cannot raise the current snapshot. The blocker is source/forecast confidence and future real forecast cycles, not missing current matches.
21. The read-only acceleration inventory reports `best_possible_gain_if_5_pending_match=0.0` and `best_possible_gain_if_all_pending_match=0.0` because pending rows are currently zero.
22. Next prediction evidence phase must use existing owners only: fresh service/quality/trust inputs, future forecast-to-later-actual cycles, governed prediction feedback, and snapshot refresh. Formula/floor changes and synthetic actuals remain forbidden.

## AUTONOMY_BLAST_RADIUS_MATERIALIZATION_RULES

1. Blast-radius confidence is calculated by `admin_core/intelligence_platform.py::blast_radius_confidence_model`.
2. Blast-radius evidence rows are built by `admin_core/intelligence_workers.py::build_blast_radius_evidence_rows` and consumed by the `trust-evolution-summaries` snapshot family.
3. A usable blast-radius evidence row requires a known governed outcome and a movement radius derived from existing fields such as `blast_radius`, `affected_users`, `movement_count`, `users_moved`, `selected_move_count`, `target_users`, `users`, `moved_users`, `selected_moves`, or `moves`.
4. Historical governed feedback from BA/small-batch runs contains reusable movement-radius, success, verification, closure, and no-rollback evidence. A prior local rebuild using existing owners classified that evidence into `blast_radius_confidence=100.0` with `blast_radius_evidence_count=2`.
5. Current production autonomy evidence on 2026-06-21 still consumes `blast_radius_confidence=0.0`, so historical blast-radius evidence exists but is not currently materialized into the production consumed autonomy snapshot.
6. This is a materialization/refresh gap, not a reason to create a new blast-radius model, new confidence model, new trust model, new snapshot family, or new truth source.
7. The safe next action is to run the existing production snapshot refresh/materialization path against the correct production feedback stores, then re-read `trust-evolution-summaries` and `/api/operator/autonomous-dry-run`.
8. If production feedback stores lack the historical governed records, new governed evidence may be required; that must still be collected through existing execution, feedback, closure, and snapshot owners only.
9. `GET /api/operator/shadow-autonomy` currently records missing shadow decision rows through `record=true`; strict read-only audits should use `/api/operator/decision-surface` plus the pure `admin_core.shadow_autonomy` decision builder, or explicitly allow that product write.
10. AUTONOMY.REMATERIALIZATION.1 on 2026-06-21 re-ran the current existing builder against saved production governed feedback and again produced 2 usable blast-radius rows: radius `1` and radius `2`, both successful and rollback-free. The resulting existing model output was `blast_radius_confidence=100.0`, `successful_small_operations=2`, and `unsafe_large_operations=0`.
11. Fresh production API capture in AUTONOMY.REMATERIALIZATION.1 still reported `blast_radius_confidence=0.0`, `confidence=39.597`, `trust=39.597`, `prediction_confidence=39.6`, `apply_executed=false`, and `users_moved=0`.
12. If only blast-radius confidence becomes visible as `100.0`, estimated trust rises to about `54.698`, but the `70` trust floor still does not pass and autonomy remains `NOT_READY`.
13. Existing `tools/v7-intelligence-snapshot-refresh` supports the required feedback inputs and has a `--dry-run` mode; refresh writes intelligence snapshots only and must not move users or enable autonomy.
14. AUTONOMY.REMATERIALIZATION.2 on 2026-06-21 executed the existing production-supported path `/api/actions/planner-refresh-dry-run`, which runs `v7-users-autoswitch --pre-planner-refresh write --pre-planner-refresh-command v7-intelligence-snapshot-refresh`.
15. The refresh was safe: `apply_executed=false`, `user_movement_performed=false`, `routing_mutation_performed=false`, `users_moved=0`, and `runtime_mutation_scope=intelligence_snapshot_refresh_only`.
16. The refresh regenerated `trust-evolution-summaries` (`generated_at` changed from `2026-06-21T17:48:03.651484+00:00` to `2026-06-21T17:48:12.525206+00:00`) but had no metric effect: `blast_radius_confidence` stayed `0.0`, trust stayed `39.602`, confidence stayed `39.602`, and prediction stayed `39.6`.
17. The `blast_radius_records` source hash after refresh equals `sha256_json([])`, so the production consumed snapshot still contains no blast-radius rows. The standard production refresh path alone did not recover historical BA evidence.
18. AUTONOMY.REMATERIALIZATION.3 on 2026-06-22 certified the root cause as `BLAST_RECORDS_IN_DIFFERENT_STORE`.
19. The active production default refresh paths `/opt/v7/egress/state/execution-events.jsonl`, `/opt/v7/egress/state/runtime-trust.jsonl`, `/opt/v7/egress/state/proposal-records.jsonl`, `/opt/v7/egress/state/proposals.jsonl`, and `/opt/v7/egress/state/closure-records.jsonl` exist but currently contain 0 records, so standard refresh gives the builder no governed movement/outcome rows.
20. Historical governed blast-radius evidence still exists in production rotated stores such as `/opt/v7/egress/state/execution-events.jsonl.1`, `/opt/v7/egress/state/runtime-trust.jsonl.1`, `/opt/v7/egress/state/closure-records.jsonl.1`, and `/opt/v7/egress/state/proposal-records.jsonl.1`.
21. The current existing builder classifies those rotated production records without code changes: combined rotated `.jsonl.1` inputs produce 11 valid blast-radius rows. Therefore this is not a schema mismatch, not a builder/model failure, and not a reason to create a new model.
22. The safe recovery path is an approved use of existing archive restore/materialization or snapshot rebuild/refresh capability against real rotated feedback inputs. Manual trust snapshot editing, synthetic evidence, and runtime apply remain forbidden.
23. AUTONOMY.REMATERIALIZATION.4 on 2026-06-22 previewed recovery without writes. A strict refresh-equivalent run with rotated feedback inputs still produced `blast_radius_confidence=0.0` because the useful rotated rows did not become visible in the final bounded trust-evolution decision set.
24. The same phase previewed the existing trust model with the 11 builder-classified rotated blast rows supplied as visible `blast_radius_records`. That moved `blast_radius_confidence` from `0.0` to `100.0`, `overall_confidence` from `42.678` to `59.345`, and operator trust from `39.602` to `54.684`.
25. Blast recovery has moderate readiness impact but does not certify autonomy: confidence remains `45.8`, trust remains below the `70.0` floor at `54.684`, and prediction confidence remains `39.6`.
26. After visible blast recovery, the dominant remaining blocker is `prediction_confidence_too_low`; confidence remains a second blocker. The next evidence phase is `AUTONOMY.PREDICTION.EVIDENCE.1`.
27. AUTONOMY.FINAL.BRANCH_1 on 2026-06-22 closed the blast planning branch with immediate production recovery `NO-GO`.
28. Immediate recovery is blocked because the current as-is refresh/materialization paths can still leave `blast_radius_confidence=0.0`: `build_trust_evolution_snapshot` constructs `decision_records = audit_records + switch_records + rollback_records`, then uses `decision_records[-1000:]`. Current large `switch-history` can push restored feedback rows out of the consumed tail.
29. Existing refresh only is rejected as ineffective because active stores are empty. Existing execution-feedback materialization is rejected as an immediate path because active feedback rows can still be ordered before switch history and filtered out. Existing archive restore is useful as a real evidence source but is not sufficient alone.
30. Recommended recovery owner remains the existing snapshot rebuild/refresh owner, but it needs one visibility step: feed existing builder-classified blast rows into `trust_evolution_summary` as visible `blast_radius_records`, or equivalently fix existing-owner ordering/bounding so real feedback rows survive into the consumed trust-evolution snapshot.
31. This visibility step must not create a new planner, governance path, execution path, trust source, confidence model, or synthetic evidence. It is an existing-owner correction before any snapshot-only recovery write.
32. Exact next phase: `AUTONOMY.FINAL.BRANCH_1A_BLAST_VISIBILITY_OWNER_FIX_AND_DRY_RUN`.
33. Last verified commit: `5011d253e2bb0a11753d25a7487902ee528f84c1`.
34. AUTONOMY.FINAL.BRANCH_1A implemented the existing-owner visibility fix in `admin_core.intelligence_workers.build_trust_evolution_snapshot`.
35. The fix keeps general outcome mappers bounded by `bounded_decisions = decision_records[-MAX_HISTORY_RECORDS:]`, but builds `blast_radius_records` from the full existing `decision_records` stream before shared tail bounding can hide older governed feedback.
36. Production-data dry-run with the patched existing owner and real rotated `.jsonl.1` inputs produced `blast_radius_evidence_count=11`, `blast_radius_confidence=100.0`, `trust_evolution_overall_confidence=59.358`, `prediction_confidence=37.37`, `users_moved=0`, and `snapshot_written=false`.
37. Blast Branch acceptance passed: blast evidence count is nonzero, blast confidence is nonzero, evidence originates from real production governed records, no synthetic evidence was created, and existing owners only were used.
38. Blast Branch status is now `CLOSED`. Production autonomy is not enabled and still remains blocked by confidence, trust, prediction confidence, and operator comparison evidence.
39. AUTONOMY.FINAL.BRANCH_1B on 2026-06-22 deployed Branch 1A through the existing approved `tools/v7-safe-deploy` flow. Local, GitHub, and runtime are aligned at `c4adc537b39e0335ad9cc0cf7ff9589d85860d60`; final truth is `PASS` and final convergence is `ALIGNED`.
40. The approved production recovery write used the existing `/usr/local/bin/v7-intelligence-snapshot-refresh` owner with real rotated production stores: `execution-events.jsonl.1`, `runtime-trust.jsonl.1`, `proposal-records.jsonl.1`, `proposals.jsonl.1`, and `closure-records.jsonl.1`.
41. The recovery write was snapshot-only: `runtime_behavior_changed=false`, `governance_behavior_changed=false`, `users_moved=false`, `apply_executed=false`, and no daemon/autoswitch was enabled.
42. Production consumed autonomy metrics after recovery: `blast_radius_evidence_count=11`, `blast_radius_source_record_count=3372`, `blast_radius_confidence=100.0`, `trust_score=54.684`, `confidence_score=39.578`, `prediction_confidence=37.312`, `rollback_confidence=100.0`, `execution_allowed_now=false`, and `users_moved=0`.
43. Blast Branch status is now `OPERATIONALLY_CLOSED`. Blast recovery is no longer the dominant blocker.
44. Production autonomy remains blocked by `confidence_too_low`, `trust_too_low`, and `prediction_confidence_too_low`. The next safe phase is `AUTONOMY.PREDICTION.EVIDENCE.2_REAL_OUTCOME_CONFIDENCE_COLLECTION`; operator comparison evidence remains a parallel P1 track.
45. Last verified commit: `c4adc537b39e0335ad9cc0cf7ff9589d85860d60`.

## AUTONOMY_TRUST_BUILDOUT_RULES

1. AUTONOMY.TRUST.BUILDOUT.1 on 2026-06-22 re-read production using `/api/operator/autonomous-dry-run`, `/api/operator/decision-surface`, and a read-only local shadow model built from the decision surface.
2. No runtime apply, user movement, daemon enablement, autoswitch enablement, threshold change, floor change, synthetic evidence, manual snapshot edit, new planner, new governance path, new execution path, or new truth source occurred.
3. Fresh current consumed dry-run values were `candidate_count=1`, `execution_allowed_now=false`, `users_moved=0`, final confidence `45.8`, trust `39.582`, final prediction confidence `39.6`, outcome prediction confidence `37.343`, rollback confidence `100.0`, and blast-radius confidence `0.0`.
4. The fresh consumed values differ from the Branch 1B post-recovery evidence where production consumed blast-radius confidence was `100.0` and trust was `54.684`.
5. Canonical interpretation: Branch 1B blast recovery was proven and remains closed, but the currently consumed default autonomy dry-run does not durably preserve recovered blast evidence. This is a trust durability gap, not a reason to reopen blast model discovery.
6. The next trust phase must make existing recovered blast evidence durable under the normal existing snapshot/refresh owner before canary readiness can be considered.
7. Current operator comparison reality from read-only shadow build: 27 decisions, 0 comparisons, agreement rate `0.0`, average decision confidence `45.828`, and earned confidence `45.828`.
8. With the current shadow formula, the practical operator-comparison target is about 9 all-agree comparisons, 11 comparisons at 90% agreement, 15 at 80%, or 17 at 75% to reach earned confidence near or above `70.0`. The formal minimum comparison count remains 5, but that alone is unlikely to reach the earned-confidence floor.
9. Current prediction path remains healthy but under-confident: matching works, forecast accuracy was previously about `98.5`, and the blocker is low forecast/source confidence. Estimated future evidence need is about 23 perfect matched actuals or about 35 high-quality 90% matched actuals to approach the `70.0` floor.
10. Trust buildout order is: `AUTONOMY.TRUST.DURABILITY.1` -> `OPERATOR.COMPARISON.COLLECTION.1` -> `AUTONOMY.PREDICTION.EVIDENCE.2` -> `EVENT.CONSUMER.READONLY.2` -> `AUTONOMY.CANARY.1_READINESS_RECHECK`. EVENT.CONSUMER.READONLY.2 is complete as a read-only consumer certification.
11. AUTONOMY.TRUST.BUILDOUT.1 final verdict is `AUTONOMY_TRUST_PATH_PARTIAL`.
12. Last verified commit: `6b0c72f4157d5e4cb57db864d0bcd73b593f4fe0`.

## AUTONOMY_TRUST_DURABILITY_RULES

1. AUTONOMY.TRUST.DURABILITY.1 on 2026-06-22 implemented the certified root-cause fix for recovered blast evidence durability.
2. Root cause: normal `tools/v7-intelligence-snapshot-refresh` consumed active JSONL paths only, while real governed recovery evidence could live in rotated numeric store-family files such as `execution-events.jsonl.1`.
3. Current rule: normal snapshot refresh must consume the existing JSONL family, not only the active file. The family order is oldest numeric rotation to newest active file, for example `execution-events.jsonl.2` -> `execution-events.jsonl.1` -> `execution-events.jsonl`.
4. This is not a new truth source. Numeric rotations are part of the same existing evidence store family.
5. The implemented owner is `tools/v7-intelligence-snapshot-refresh`; it now expands JSONL family reads for audit inputs, feedback inputs, switch history, and rollback history.
6. Automated durability tests prove that recovered blast evidence survives refresh, rebuild, snapshot write, and reread while bounded decision processing remains at `MAX_HISTORY_RECORDS`.
7. Local verification evidence: `docs/reports/AUTONOMY_TRUST_DURABILITY_1_EVIDENCE/local_rotated_family_durability.json`.
8. Verified local lifecycle metrics: after refresh/rebuild/reread, `blast_radius_confidence=100.0`, `blast_radius_evidence_count=1`, `blast_radius_source_record_count=1001`, and `bounded_decision_count=1000`.
9. Production deploy and snapshot refresh also verified the fix: deploy id `deploy-z8-14-Updatesystem-29b980c-20260623T000551`, `blast_radius_confidence=100.0`, `blast_radius_evidence_count=11`, `blast_radius_source_record_count=4407`, `bounded_decision_count=1000`, `successful_small_operations=9`, and `unsafe_large_operations=0`.
10. No runtime apply, user movement, daemon enablement, planner change, governance change, execution change, threshold change, floor change, formula change, synthetic evidence, or new truth source occurred.
11. Branch 1B remains the production proof point for 11 real recovered rows and trust `54.684`; AUTONOMY.TRUST.DURABILITY.1 makes that class of recovered evidence durable under normal refresh code behavior.
12. Remaining autonomy blockers still stand: trust floor, prediction confidence, operator comparison evidence, readiness recheck, and disabled daemon/autoswitch runtime. Live event consumer certification is complete in read-only mode only.
13. AUTONOMY.TRUST.DURABILITY.1 final verdict is `TRUST_DURABILITY_FIXED`.
14. Last verified commit: `29b980c00a11097332eaad53a2c1fe2f77d2389d`.
15. AUTONOMY.TRUST.ACCELERATION.1 final production canary proximity after refresh: confidence `39.606`, trust `54.704`, prediction confidence `36.861`, operator earned confidence `45.802`; all remain below the `70.0` floor.
16. `AUTONOMY.CANARY.1` is not ready. Missing floor set is `confidence`, `trust`, `prediction_confidence`, and `operator_earned_confidence`.
17. AUTONOMY.CANARY.1D added read-only floor forensics and materialization audit to the existing `admin_core/autonomy_trust_acceleration.py` / `tools/v7-autonomy-trust-evidence-inventory` owner.
18. Production after deploy `2915a4b8107d1fbd416661e562511a6ca2a864fe` reports floor values: confidence `37.402`, trust `53.051`, prediction confidence `33.753`, and secondary operator earned confidence `45.908`; all remain below the `70.0` floor.
19. The confidence floor is low because it is currently derived from decision `50.0`, service `36.079`, and suitability `26.126`. Blast and rollback are both `100.0`, but they do not close the current confidence floor.
20. The trust floor is low because it is currently derived from decision `50.0`, service `36.079`, suitability `26.126`, and blast `100.0`; the result remains `53.051`, below floor.
21. The prediction floor is low even though actual matching is complete: production has `21` forecasts, `21` actuals, `21` matched rows, `0` pending rows, forecast accuracy `94.786`, and mean forecast confidence `0.3561`. Root cause is `low_forecast_source_confidence`, not missing current actuals.
22. The service floor is low because service rows are matched but low-confidence: `21` rows, mean correctness `100.0`, mean row confidence `0.361`, and service confidence `36.079`.
23. The suitability floor is low because candidate outcome evidence is present but incomplete and low-confidence: `156` candidates, `83` outcomes, sampled rows include `8` without outcome, mean candidate confidence `0.372`, mean correctness `64.395`, and suitability confidence `26.126`.
24. Current safe materialization audit says prediction actuals, service actuals, and candidate outcomes are consumed by existing owners; there is no safe immediate fix that can raise floors without new real evidence. Synthetic prediction actuals, synthetic candidate outcomes, synthetic operator comparisons, threshold/formula changes, runtime apply, and user movement remain forbidden.
25. Next safe evidence phase: collect real higher-confidence service/channel probe cycles and real governed/manual outcome closure through existing owners, then refresh snapshots and re-read the canary floors. `AUTONOMY.CANARY.1` remains blocked.

## 1. Channels

- What it means: A channel is an egress path that can carry users, be inspected by operators, and be considered by the planner.
- Source of truth: Channel registry/runtime channel state, operator decision surface, service matrix, route/runtime readiness, planner assignment truth.
- Where it is calculated: `admin_core/operator_decision_surface.py`, `tools/v7-users-autoswitch`, and channel helper functions in `admin/v7-admin-api`.
- Where it is displayed: Admin Channels table, Channel Drawer, Attention/Overview derived surfaces, technical diagnostics.
- What affects it: Registry flags, manual/reserve/canary role, service checks, stability, capacity/load, route readiness, runtime readiness, history, assigned users, planner gates.
- What does NOT affect it: Cosmetic UI labels, screenshots, operator-facing health score alone, or raw trust labels alone.
- Operator meaning: "Can this channel be used, should users stay, what is wrong, and what action is safe?" Operator wording must avoid vague "needs check" language. When evidence is incomplete, use reality-first wording that states the current reality and next step, such as "fresh data unavailable", "open service matrix", "open users", "open logs", "automatic refresh pending", or "safe action unavailable".
- Engineer meaning: Aggregated runtime/planner/read-model state for one egress object.
- Known caveats: Some roles such as Keep Only or Blocked may not appear in production screenshots if live data currently has no channel in that state.
- Related reports / ADRs: `UX_4_CHANNEL_DRAWER_REBUILD_SPECIFICATION_REPORT.md`, `CHANNEL_TRUTH_3_CHANNEL_ASSIGNMENT_ADAPTER_REPORT.md`, `CHANNEL_TRUTH_4_CHANNEL_ROLE_MODEL_REPORT.md`, `CHANNEL_SUITABILITY_2_PLANNER_FIRST_CHANNEL_MODEL_REPORT.md`, ADR-004.
- Last verified commit: `8ba2178f`.

## 2. Channel Decision V7

- What it means: The operator-facing decision for a channel: Use, Evacuate, Keep Current Users, Emergency Only, or Blocked.
- Source of truth: Existing planner/assignment truth and channel role flags, not a separate UI score.
- Where it is calculated: `tools/v7-users-autoswitch` candidate/blocker/selected-move logic and adapter code in `admin_core/operator_decision_surface.py` plus channel decision helpers in `admin/v7-admin-api`.
- Where it is displayed: Primary Channel table column and Channel Drawer first screen. The Channel Drawer first screen is Decision-first: drawer header channel identity → Decision → Reason → Signals → Problems → one collapsed Engineer Diagnostics entry, with no duplicate channel label and no score or technical health above the decision.
- What affects it: Selected moves, eligible candidates, blockers, current users, `manual_only`, `reserve_only`, canary reservation, disabled/quarantine/maintenance, service/route/speed/stability/load/policy gates.
- What does NOT affect it: Channel Score by itself, old TRUSTED/WATCH/QUARANTINED labels, or raw engineering health labels.
- Operator meaning: "What does V7 want me to do with this channel?" `Use` means V7 can use the channel under current planner/assignment evidence; it does not mean fastest, best, warning-free, or unlimited capacity. `Emergency Only` means the channel is role/policy restricted for manual, reserve, canary, or execution-only use; it does not mean technically broken.
- Engineer meaning: A read-only projection of planner assignment/retention/evacuation truth into operator language.
- Known caveats: If the planner cannot produce a role because data is absent, UI must show the safest truthful state rather than inventing eligibility. A channel can be `Use` while capacity/load is at warning or hard-full for new assignments; the decision must be read together with blocker/load details. Operator labels are locked as understandable terms: `Use`, `Keep Current Users`, `Evacuate`, `Emergency Only`, and `Blocked` / `Запрещён`; compact table labels may use Russian equivalents such as `Использовать`, `Оставить текущих`, `Перевести`, `Только аварийно`, `Запрещён`. `Загрузка решения` is an allowed transient loading state before assignment truth arrives; it is not a sixth planner decision and must not be counted as `Blocked`.
- Related reports / ADRs: `CHANNEL_TRUTH_1_FULL_DECISION_PIPELINE_AND_SCORE_ALIGNMENT_AUDIT_REPORT.md`, `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md`, `CHANNEL_TRUTH_3_CHANNEL_ASSIGNMENT_ADAPTER_REPORT.md`, `CHANNEL_SUITABILITY_2_PLANNER_FIRST_CHANNEL_MODEL_REPORT.md`, `CAPACITY_1_REALITY_AUDIT_REPORT.md`, ADR-009.
- Last verified commit: `2fb9d205`.

## 3. Channel Score

- What it means: A technical/mixed health score from 0 to 100 that explains channel condition; it is not assignment truth.
- Source of truth: Existing `channelSuitability(source)` model and its component breakdown.
- Where it is calculated: `admin/v7-admin-api` functions `channelSuitabilityServices`, `channelSuitabilityStability`, `channelSuitabilityCapacity`, `channelSuitabilityRoute`, `channelSuitabilityRuntime`, `channelSuitabilityHistory`, and `channelSuitability`.
- Where it is displayed: Diagnostics metadata and optional technical surfaces. Channel Drawer first screen must not display `score/100`; diagnostics must present reality-first explanations rather than score-first point math.
- What affects it: Services, stability, capacity, route/topology, runtime/readiness, and history components.
- What does NOT affect it: Planner assignment eligibility directly, emergency/manual role policy directly, or whether V7 should move current users.
- Operator meaning: "What real technical signals explain the channel condition?"
- Engineer meaning: A mixed diagnostic score useful for explanation and troubleshooting, separate from planner hard gates.
- Known caveats: A high score can coexist with Do Not Assign/Emergency Only/Evacuate if planner gates or role flags block assignment. A capacity reduction inside the score means user-assignment pressure against limits, not bandwidth saturation or speed failure. Operator diagnostics must not lead with point loss, component contribution, score penalty language, or vague "requires verification" wording.
- Related reports / ADRs: `CHANNEL_TRUTH_1_FULL_DECISION_PIPELINE_AND_SCORE_ALIGNMENT_AUDIT_REPORT.md`, `CHANNEL_SUITABILITY_1_PLANNER_DERIVED_SUITABILITY_MODEL_REPORT.md`, `CHANNEL_SUITABILITY_2_PLANNER_FIRST_CHANNEL_MODEL_REPORT.md`, `docs/operator_actions/CHANNEL_HEALTH_3_SCORE_EXPLANATION_MODEL_REPORT.md`, `CAPACITY_1_REALITY_AUDIT_REPORT.md`, `DIAGNOSTICS_1_REALITY_FIRST_REBUILD_REPORT.md`, ADR-002, ADR-009, ADR-010.
- Last verified commit: `2fb9d205`.

## 4. Technical Health

- What it means: A diagnostics-only reality explanation of what contributes to technical channel condition.
- Source of truth: Existing channel suitability breakdown and evidence/read models.
- Where it is calculated: `admin/v7-admin-api` channel suitability functions and reality-first diagnostics rendering.
- Where it is displayed: Nested technical diagnostics inside the Channel Drawer, not as a primary workflow.
- What affects it: Score components, fresh service/route/runtime evidence, stability/capacity/history inputs.
- What does NOT affect it: Operator action flow directly, assignment decision directly, or governance approval.
- Operator meaning: "What is really happening with services, stability, load, route readiness, runtime, and history?" Technical health can be good while assignment is Emergency Only, Keep Only, or load-limited. Diagnostics may use component status language such as `OK`, `Нет свежих данных`, and `Проблема`, then explain observed reality; first-screen operator wording must stay concrete and action-oriented.
- Engineer meaning: Component-level diagnostic view over the existing score inputs, rendered as observed reality instead of point math.
- Known caveats: Health must not reintroduce action/resolution language as first-line operator truth. Diagnostics may point to missing evidence but should not become a separate execution path. Diagnostics must not explain via lost points, penalties, score contribution, or generic "needs check" wording. Table-level "Healthy" is narrower than technical health: it requires a usable/keep assignment posture and no red first-level operator signal.
- Related reports / ADRs: `docs/operator_actions/CHANNEL_HEALTH_SCREEN_EXISTENCE_AUDIT.md`, `docs/operator_actions/CHANNEL_HEALTH_2_DIAGNOSTICS_ONLY_IMPLEMENTATION_REPORT.md`, `docs/operator_actions/CHANNEL_HEALTH_3_SCORE_EXPLANATION_MODEL_REPORT.md`, `CAPACITY_1_REALITY_AUDIT_REPORT.md`, `DIAGNOSTICS_1_REALITY_FIRST_REBUILD_REPORT.md`, ADR-003, ADR-009, ADR-010.
- Last verified commit: `2fb9d205`.

## 5. Route

- What it means: Route reality/readiness for user/channel traffic, including route status, direct/RU route checks, mismatch/leak risk, and topology signals.
- Source of truth: Runtime route read models and route reality helpers.
- Where it is calculated: `admin_core/route_reality_views.py`, `admin_core/route_views.py`, `admin/v7-admin-api` route status/readiness functions, and planner route gates in `tools/v7-users-autoswitch`.
- Where it is displayed: Routes surface, User Drawer, Channel Drawer diagnostics, Attention items when route risk exists.
- What affects it: Runtime route tables, policy routing, direct/RU route state, route evidence freshness, channel topology, planner route gates.
- What does NOT affect it: Channel Score alone, UI ordering, or manual labels.
- Operator meaning: "Is traffic going where it should, and is there a safety/leak problem?" In Channel diagnostics, route wording means readiness/topology confidence. It must not imply speed, bandwidth, latency, packet loss, or traffic quality unless route evidence explicitly shows a real route problem.
- Engineer meaning: Read-only runtime route evidence and planner gate input.
- Known caveats: Route validation is primarily diagnostic/status until a safe existing action exists; it must not imply unsafe execution. Channel UI should say "route readiness/confidence incomplete" rather than "route broken" unless runtime route evidence actually shows mismatch or leak risk.
- Related reports / ADRs: `UX_7_ATTENTION_LAYER_SPECIFICATION_REPORT.md`, `docs/operator_actions/OPERATOR_ACTIONS_AUTOMATION_REALITY_AUDIT.md`, `docs/operator_actions/CHANNEL_AUTOMATION_OPERATOR_REALITY_AUDIT_REPORT.md`.
- Last verified commit: `8ba2178f`.

## 6. Capacity

- What it means: Assignment/load posture for a channel or pool: current and projected users compared with configured soft, hard, and failover-hard limits. Capacity answers whether V7 may add users, should pause additions, or must treat a channel as full for planned/failover movement.
- Source of truth: Egress registry capacity fields (`capacity_users`, `soft_limit`, `hard_limit`), live assigned user counts, policy load settings, dynamic load summary, planner capacity/load gates, and capacity readiness tools.
- Where it is calculated: `tools/v7-users-autoswitch` `_load_policy`, `_healthy_for_load`, `_dynamic_load_summary`, `_load_limits_for_egress`, `_capacity_status`, `_capacity_decision`, `_gate_load`; `admin/v7-admin-api` `channelSuitabilityCapacity`, `channelLoad`, `loadPosture`, capacity read/preview helpers; runtime support tools `v7-capacity-check` and `v7-capacity-readiness`.
- Where it is displayed: Channel table Load/Capacity signal, Channel Drawer diagnostics, score explanation, execution preview/gates, overview Load card, global capacity/readiness summaries.
- What affects it: Current users assigned to an egress, projected users after movement, explicit per-egress limits, dynamic load policy, healthy working pool size, reserve ratio, soft/hard/failover multipliers, failover capacity multiplier, min/max limits, role flags that remove channels from normal working pool, and planner purpose (`current`, `planned`, `failover`).
- What does NOT affect it: CPU usage, bandwidth saturation, traffic volume, raw speed complaint alone, raw service success alone, cosmetic UI ordering, screenshots, or the mixed Channel Score by itself.
- Operator meaning: `Load OK` means the channel is within assignment limits. `Soft Full` / warning means the channel is near or at the soft limit and new additions require capacity/headroom evaluation. `Hard Full` / "on limit" means new planned assignments are restricted; current users are not automatically failing. `Overloaded` means failover-hard capacity was reached and is a stronger emergency load state. Operator copy should explain preferred assignment level, hard assignment limit, assignment restriction, and why current users may still work.
- Engineer meaning: Planner/gate input that bounds movement, affects ranking, can block planned/failover candidates, and prevents broad unsafe switching.
- Known caveats: Capacity/load is not speed quality and not traffic saturation. A channel can have good speed/stability and still be hard-full because too many users are assigned relative to policy. Production evidence on 2026-06-18 showed `vless` and `awg3` as technically usable/currently retained while load was hard-full for assignment. Global IP capacity readiness (`capacity_plan`) is a separate pool/readiness check and can fail independently from per-channel assignment load. Prefer "assignment limit reached" over "channel overloaded" when the operator might confuse load with internet quality.
- Related reports / ADRs: `CAPACITY_1_REALITY_AUDIT_REPORT.md`, `docs/capacity_2/CAPACITY_2_OBSERVED_CAPACITY_MODEL_REPORT.md`, `docs/track7/productization/e35_0_1-audit/capacity-policy-audit.md`, `CHANNEL_SCORE_REALITY_AUDIT.md`, `CHANNEL_ROUTE_COMPONENT_REALITY_AUDIT_REPORT.md`, `CHANNEL_SIGNALS_1_MODEL_AUDIT_REPORT.md`, `CHANNEL_SIGNALS_2A_SEMANTICS_REPORT.md`, `CHANNEL_TRUTH_1_FULL_DECISION_PIPELINE_AND_SCORE_ALIGNMENT_AUDIT_REPORT.md`, `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md`, `docs/operator_actions/CHANNEL_AUTOMATION_OPERATOR_REALITY_AUDIT_REPORT.md`, ADR-009, ADR-011.
- Last verified commit: `2fb9d205`.

## 6A. Observed Capacity Shadow

- What it means: A future shadow/advisory model that learns practical channel capacity from observed quality at different assigned-user levels. It asks: "At what user count does this channel begin to degrade in measured reality?"
- Source of truth: Derived evidence only from existing assigned-user counts, service matrix, quality summary windows, runtime readiness, route readiness, and history. It is not an active runtime truth source.
- Where it is calculated: Not implemented as runtime behavior in CAPACITY.2. Future implementation should reuse read-only patterns from `tools/v7-egress-quality-compact`, `admin_core/intelligence_workers.py`, and `admin_core/shadow_autonomy.py`.
- Where it is displayed: Not currently displayed as an active operator/planner decision. Future display should be advisory only until separately approved.
- What affects it: Assigned-user count, service failures, fail rate, p95 latency, avg/min Mbps, stability, runtime readiness, route readiness, historical trend, sample freshness, and confidence.
- What does NOT affect it: It must not directly affect planner eligibility, selected moves, autoswitch, governance, runtime execution, or existing `soft_limit`, `hard_limit`, and `capacity_users` values.
- Operator meaning: "V7 is learning whether this channel remains stable as users increase." It is not permission to move users and not proof of physical bandwidth.
- Engineer meaning: A snapshot-only learning/advisory layer for practical capacity under third-party or partially owned tunnel constraints.
- Known caveats: Current production evidence proves V7 can observe users and quality together, but does not yet prove causal capacity curves. Observed Capacity Shadow must remain observe/learn/recommend until a future governed program certifies planner integration.
- Related reports / ADRs: `docs/capacity_2/CAPACITY_2_OBSERVED_CAPACITY_MODEL_REPORT.md`, `docs/capacity_2/OBSERVED_CAPACITY_SHADOW_MODEL.md`, `docs/capacity_2/DATA_GAP_ANALYSIS.md`, ADR-011.
- Last verified commit: `67fbd850`.

## 7. Service Matrix

- What it means: Per-service reachability/health diagnostics for channels/services.
- Source of truth: Existing service matrix refresh/test outputs and admin service matrix read models.
- Where it is calculated: Runtime tools `v7-service-matrix-refresh-all` and `v7-service-matrix-test`; admin rendering helpers in `admin/v7-admin-api`.
- Where it is displayed: Checks, Channel Drawer service details, diagnostics, Attention item source when service failure affects users.
- What affects it: Service test results, freshness, channel availability, runtime check outputs.
- What does NOT affect it: It does not by itself execute user movement, bypass governance, or replace planner eligibility.
- Operator meaning: "Which services work on this channel and what needs re-checking?"
- Engineer meaning: Measurement/diagnostic input consumed by UI and planner gates.
- Known caveats: Service Matrix is diagnostic/background automation, not a standalone business action. Manual refresh is allowed only through existing safe actions. First-level channel Services should track primary user-facing services; hidden endpoint checks such as auth/API companion endpoints remain supporting diagnostics unless they become explicit planner blockers.
- Related reports / ADRs: `docs/operator_actions/OPERATOR_ACTIONS_AUTOMATION_REALITY_AUDIT.md`, `docs/operator_actions/CHANNEL_AUTOMATION_2_OPERATOR_SURFACE_SIMPLIFICATION_REPORT.md`, `UX_4_CHANNEL_DRAWER_REBUILD_SPECIFICATION_REPORT.md`.
- Last verified commit: `8ba2178f`.

## 8. Stability

- What it means: Whether channel behavior is steady enough for assignment/retention, including interface/runtime availability and speed stability floors.
- Source of truth: Planner gates, runtime/channel evidence, suitability stability component.
- Where it is calculated: `tools/v7-users-autoswitch` quality/stability gates and `admin/v7-admin-api` channel stability/suitability helpers.
- Where it is displayed: Channel diagnostics, assignment blocker language, score explanation, Attention/Channel Drawer when it becomes a problem.
- What affects it: Interface up/down, missing interface, stability floor, speed samples, quality history.
- What does NOT affect it: Human-readable labels alone or decorative UI state.
- Operator meaning: "Is this channel stable enough to trust for users?"
- Engineer meaning: Hard/soft quality gate and score component.
- Known caveats: Raw labels such as `interface_down_or_missing` must be translated into operator language.
- Related reports / ADRs: `docs/operator_actions/CHANNEL_HEALTH_3_SCORE_EXPLANATION_MODEL_REPORT.md`, `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md`, `CHANNEL_SUITABILITY_3_FINAL_CHANNEL_UI_POLISH_REPORT.md`.
- Last verified commit: `8ba2178f`.

## 9. Runtime Readiness

- What it means: Whether runtime state and evidence are present/readable enough for V7 to trust or act on a decision.
- Source of truth: Runtime read adapters, execution readiness/gates, runtime convergence checks, planner stop conditions.
- Where it is calculated: `admin_core/runtime_read_views.py`, `admin/v7-admin-api` `egress_runtime_readiness`, `admin_core/operator_execution_pipeline.py`, and `tools/v7-users-autoswitch`.
- Where it is displayed: Operator Center, Channel/User detail surfaces, execution preview, diagnostics, truth/convergence status.
- What affects it: Runtime file availability, registry readability, restore barrier, execution packet validity, governance gates, runtime/repo convergence.
- What does NOT affect it: Static documentation, UI score alone, or local code state without runtime verification.
- Operator meaning: "Is V7 ready and safe enough to trust this action/status?"
- Engineer meaning: Runtime safety/readability contract for planner and execution surfaces.
- Known caveats: Runtime readiness can block or downgrade action even when UI health looks good.
- Related reports / ADRs: `PROGRAM_CONV1_PERMANENT_TRUTH_AND_DEPLOYMENT_CONVERGENCE_SYSTEM_REPORT.md`, `CHANNEL_TRUTH_1_FULL_DECISION_PIPELINE_AND_SCORE_ALIGNMENT_AUDIT_REPORT.md`, `UX_7_ATTENTION_LAYER_SPECIFICATION_REPORT.md`.
- Last verified commit: `8ba2178f`.

## 10. History

- What it means: Past channel/user/runtime evidence used to explain trust, recovery, failures, and score/history components.
- Source of truth: Existing logs/evidence, intelligence snapshots, planner history/failure inputs.
- Where it is calculated: `admin_core/intelligence_platform.py`, `admin_core/intelligence_snapshots.py`, `tools/v7-users-autoswitch`, admin evidence/history views.
- Where it is displayed: Evidence/history/technical sections, not first-screen operator answers.
- What affects it: Failure history, recovery state, past measurements, audit events, intelligence snapshots.
- What does NOT affect it: It does not create a new truth source or new operator workflow by itself.
- Operator meaning: "What happened before, and does it explain this state?"
- Engineer meaning: Evidence trail and historical signal for diagnostics/planner decisions.
- Known caveats: History is useful after problem selection; it should not become top-level attention noise without another current problem source.
- Related reports / ADRs: `UX_7_ATTENTION_LAYER_SPECIFICATION_REPORT.md`, `docs/operator_actions/CHANNEL_UX_3_PROBLEM_CAUSE_SEPARATION_REPORT.md`, `PROGRAM_INTELLIGENCE_PLATFORM_CERTIFICATION_AND_HARDENING_REPORT.md`.
- Last verified commit: `8ba2178f`.

## 11. Planner

- What it means: The existing autoswitch/planning authority that evaluates candidates, blockers, selected moves, retention, evacuation, ranking, and execution readiness inputs.
- Source of truth: `tools/v7-users-autoswitch` and its read-only surfaces/adapters.
- Where it is calculated: Candidate/blocker/gate functions in `tools/v7-users-autoswitch`, with operator projections in `admin_core/operator_decision_surface.py`.
- Where it is displayed: Operator decision surface, Channel Decision V7, recommendations, execution previews, Attention items.
- What affects it: Channel registry, user state, service/route/speed/stability/capacity/policy gates, cooldown/freeze, restore barrier, governance, current users.
- What does NOT affect it: Channel Score alone, UI rearrangement, screenshots, or standalone labels.
- Operator meaning: "What does V7 recommend or block, and why?"
- Engineer meaning: Existing decision pipeline and safety gate authority.
- Known caveats: Planner read-only outputs are not the same as applying execution. Apply remains governed. Admin action wrappers may expose a successful dry-run `rc=0` while returning only a truncated stdout tail; when exact `candidate_moves_total` matters, prefer a full CLI JSON capture or a normalized endpoint that preserves the parsed plan.
- Related reports / ADRs: `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md`, `CHANNEL_TRUTH_3_CHANNEL_ASSIGNMENT_ADAPTER_REPORT.md`, `docs/operator_actions/CHANNEL_AUTOMATION_OPERATOR_REALITY_AUDIT_REPORT.md`, `docs/reports/POOL.3_RUNTIME_DISCOVER.md`, ADR-EVENT-DRIVEN-AUTONOMY.
- Last verified commit: `f875eeee`.

## 12. Assignment

- What it means: Whether V7 can assign new users to a channel, keep current users, evacuate users, or restrict the channel to emergency/manual use.
- Source of truth: Planner assignment eligibility, selected moves, blockers, channel role flags, and current user counts.
- Where it is calculated: `tools/v7-users-autoswitch` `_candidate`, `_block`, `_gate_*`, `_select_moves`, `_candidate_json`; adapter projection in `admin_core/operator_decision_surface.py` and channel decision helpers.
- Where it is displayed: Channel table decision column, Channel Drawer first screen/details, Attention Layer when action is needed.
- What affects it: Eligibility candidates, blockers, selected moves away, current users, manual/reserve/canary flags, disabled/quarantine states, policy and runtime gates.
- What does NOT affect it: Technical Health/Score alone or old trust labels.
- Operator meaning: "Can V7 use this channel, must users leave, or is it restricted?"
- Engineer meaning: Planner-derived role projection over existing channel/user truth.
- Known caveats: Quality and assignment can intentionally disagree. The UI must make the decision primary and health secondary. A channel can be technically READY and still hard-full for assignment; hard-full alone does not mean current users are broken or must move immediately.
- Related reports / ADRs: `CHANNEL_TRUTH_1_FULL_DECISION_PIPELINE_AND_SCORE_ALIGNMENT_AUDIT_REPORT.md`, `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md`, `CHANNEL_TRUTH_3_CHANNEL_ASSIGNMENT_ADAPTER_REPORT.md`, `docs/reports/POOL.3_RUNTIME_DISCOVER.md`, ADR-002, ADR-EVENT-DRIVEN-AUTONOMY.
- Last verified commit: `f875eeee`.

## 13. Users

- What it means: V7 customer/user objects with identity, profile, connection, route, channel, status, and operator actions.
- Source of truth: Existing user registry/identity data, runtime/user status, recommendations, why cards, route and profile state.
- Where it is calculated: Admin user surfaces in `admin/v7-admin-api`, user decision rows in `admin_core/operator_decision_surface.py`, explainability adapter, existing profile/identity handlers.
- Where it is displayed: Users table, User Drawer, Overview/Attention, Operator Center/recommendation details.
- What affects it: Profile issuance, connection status, assigned channel, route status, speed complaint/checks, phone confirmation, policy/group access, recommendations.
- What does NOT affect it: Channel score alone, unrelated channel diagnostics, or hidden technical evidence without a user-facing problem.
- Operator meaning: "Who is this, is there a problem, why, and what should I do?"
- Engineer meaning: User-centered projection of registry/runtime/profile/route/planner evidence.
- Known caveats: The current canonical reference focuses heavily on channel work because recent audits concentrated there. Deeper user lifecycle details may require a future dedicated audit.
- Related reports / ADRs: `UX_5B_USER_DRAWER_POLISH_AND_COMMERCIAL_CERTIFICATION_REPORT.md`, `UX_6_COMMERCIAL_OPERATOR_MODEL_DISCOVERY_REPORT.md`, `UX_7_ATTENTION_LAYER_SPECIFICATION_REPORT.md`.
- Last verified commit: `8ba2178f`.

## 14. Groups / Policies

- What it means: Organizational/group policy and access settings that constrain what users/channels/actions are allowed.
- Source of truth: Existing policy settings, identity/group data, org policy gates, execution policy adapters.
- Where it is calculated: Policy settings and group/organization UI in `admin/v7-admin-api`, policy gates in `tools/v7-users-autoswitch`, execution policy adapters in `admin_core/operator_execution_pipeline.py`.
- Where it is displayed: Users/Organizations, Settings/Policy, Execution drawer, policy/domain panels.
- What affects it: Organization, group, access policy, autoswitch mode, quality thresholds, load limits, cooldowns, route/service rules.
- What does NOT affect it: Operator UI preference, raw health score alone, or report text without live policy/config.
- Operator meaning: "Is this user/action allowed under current policy?"
- Engineer meaning: Constraint layer that planner and execution must honor.
- Known caveats: UNKNOWN - requires future audit for a full canonical group/policy contract beyond the current channel/operator work.
- Related reports / ADRs: `docs/phase5/POLICY_BASED_ACCESS.md`, `docs/phase5/MULTITENANT_MODEL.md`, `CHANNEL_TRUTH_2_ASSIGNMENT_ELIGIBILITY_TRUTH_DISCOVERY_REPORT.md`.
- Last verified commit: `8ba2178f`.

## 15. Autonomy

- What it means: Read-only intelligence/shadow/automation support plus governed execution certification that may recommend, simulate, monitor, or prepare bounded action, but must not create an independent execution path.
- Source of truth: Existing shadow autonomy, intelligence platform, operator execution pipeline, governed execution path.
- Where it is calculated: `admin_core/shadow_autonomy.py`, `admin_core/intelligence_platform.py`, `admin_core/operator_execution_pipeline.py`, `admin_core/operator_execution.py`, `admin_core/operator_execution_feedback.py`, planner tools.
- Where it is displayed: Operator Center, execution readiness, attention/overview summaries, evidence/details.
- What affects it: Planner signals, channel/service regression, safety gates, governance state, intelligence snapshots, execution readiness, restore barrier state, rollback readiness, feedback/learning evidence.
- What does NOT affect it: It does not bypass approval, restore barriers, governance, rollback, feedback, truth/convergence, or existing execution handlers. It must not move users merely because a timer fired.
- Operator meaning: "V7 can surface what needs attention, and can prepare governed action, but dangerous changes remain guarded until an event-driven chain is ready."
- Engineer meaning: Derived intelligence and governed automation layer over existing truth and execution owners.
- Known caveats: Continuous production autonomy daemon is not active as of POOL.3/EVENT.1/AUTONOMY.ROOT. Truth says `autoswitch_scheduler_active=false` and `autoswitch_service_active=false`. EVENT.1 proved the current read-only chain can preview planner/packet/restore/rollback/feedback/learning surfaces but must stop because confidence/trust/prediction floors fail, operator comparison evidence is below floor, restore barrier readiness is blocked, and no live event consumer is certified. AUTONOMY.ROOT clarified that BA evidence is consumed and raises governed inherited execution trust, but does not close operator-free autonomy trust. AUTONOMY.SOURCE_CONFIDENCE.REALITY.AUDIT deployed `confidence_reality_audit` in the existing read-only trust inventory. AUTONOMY.REAL_OUTCOME_COLLECTION_AND_CONFIDENCE_GROWTH then deployed read-only `real_outcome_source_inventory` and `real_outcome_growth_projection`. AUTONOMY.CANDIDATE_OUTCOME.REALITY.COLLECTION then deployed read-only candidate outcome collection and fixed existing-owner aggregation/window gaps. Current production verdict is `OUTCOME_EVIDENCE_INCOMPLETE`: available real candidate outcomes are consumed (`84/156`), there is no remaining visibility/capture/aggregation loss, but `72` real candidate outcomes have not happened yet and canary floors still fail. Current after-refresh floors are confidence `38.872`, trust `54.154`, prediction confidence `35.385`, operator earned confidence `45.815`. AUTONOMY.FLOOR.SEMANTICS_AND_RISK_TIER_REVIEW then clarified that this state is `TIER_1 MARGINAL_OPERATOR_REVIEW` for a first governed one-user review only, while autonomous one-user canary remains `NO_GO`.
- Related reports / ADRs: `PROGRAM_INTELLIGENCE_PLATFORM_CERTIFICATION_AND_HARDENING_REPORT.md`, `UX_7_ATTENTION_LAYER_SPECIFICATION_REPORT.md`, `docs/operator_actions/CHANNEL_AUTOMATION_OPERATOR_REALITY_AUDIT_REPORT.md`, `docs/reports/POOL.3_RUNTIME_DISCOVER.md`, `docs/reports/EVENT.1_REGRESSION_TRIGGER_CERTIFICATION.md`, `docs/reports/AUTONOMY_ROOT_CONFIDENCE_DISCOVERY.md`, `docs/reports/AUTONOMY_CANARY_1D_CONFIDENCE_TRUST_PREDICTION_FLOOR_CLOSURE_REPORT.md`, `docs/reports/AUTONOMY_EVIDENCE_REAL_SOURCE_CONFIDENCE_COLLECTION_REPORT.md`, `docs/reports/AUTONOMY_SOURCE_CONFIDENCE_REALITY_AUDIT_REPORT.md`, `docs/reports/AUTONOMY_REAL_OUTCOME_COLLECTION_AND_CONFIDENCE_GROWTH_REPORT.md`, `docs/reports/AUTONOMY_CANDIDATE_OUTCOME_REALITY_COLLECTION_REPORT.md`, `docs/reports/AUTONOMY_FLOOR_SEMANTICS_AND_RISK_TIER_REVIEW_REPORT.md`, ADR-EVENT-DRIVEN-AUTONOMY, ADR-AUTONOMY-RISK-TIERED-FLOORS.
- Last verified commit: `3753df1a`.

## 16. Truth / Convergence

- What it means: The project's guardrail that repo, runtime, approved files, deployment lineage, and system truth are aligned enough to proceed.
- Source of truth: `tools/v7-truth-check`, `tools/v7-convergence-status`, `tools/v7_sync_lib.py`, runtime fingerprints/linkage.
- Where it is calculated: Truth/convergence tools and their runtime/repo checks.
- Where it is displayed: CLI output, reports, admin status/convergence surfaces where present.
- What affects it: Repo commit, runtime deployed files, approved deploy file list, runtime hash/fingerprint, convergence status, lineage metadata.
- What does NOT affect it: Local documentation claims without tool verification, chat memory, or screenshots alone.
- Operator meaning: "Is this V7 instance aligned and safe to trust?"
- Engineer meaning: Mandatory pre/post gate for major audits, implementation, deploy, and canonical reference updates.
- Known caveats: Documentation-only commits may differ from runtime code commit while truth/convergence still pass; reports must state this honestly.
- Related reports / ADRs: `PROGRAM_CONV1_PERMANENT_TRUTH_AND_DEPLOYMENT_CONVERGENCE_SYSTEM_REPORT.md`, `PROGRAM_Z8_8_TRUTH_MANIFEST_AND_V7_TRUTH_CHECK_IMPLEMENTATION_REPORT.md`, ADR-001.
- Last verified commit: `8ba2178f`.

## 17. Admin UI Operator Model

- What it means: The admin UI should present daily work as a hybrid model: attention/problem-first when action is required, object-first when the system is healthy or the operator knows the object.
- Source of truth: Existing Users/Channels/Routes/Checks/Operator surfaces, Attention Layer derived projection, User and Channel drawers.
- Where it is calculated: UI rendering in `admin/v7-admin-api`, operator decision surface in `admin_core/operator_decision_surface.py`, existing alerts/checks/recommendations/why cards.
- Where it is displayed: Overview/Attention, Users, Channels, User Drawer, Channel Drawer, Operator Center.
- What affects it: Active problems, severity, operator decision surface, user/channel status, warnings, why cards, recommendations, execution readiness.
- What does NOT affect it: It must not create a new page, drawer, workflow, planner, governance model, truth source, storage, or execution path.
- Operator meaning: "Show me what needs attention first; otherwise let me browse users/channels calmly." In the Channel Drawer this means the first screen answers what V7 wants before any health score, technical rating, confidence label, route detail, evidence, history, logs, execution context, or service matrix details.
- Engineer meaning: Derived UX projection over existing objects and truth sources.
- Known caveats: The Attention Layer must stay deduplicated and calm; otherwise it becomes a noisy ticket system. Channel Drawer diagnostics must remain behind an explicit engineer boundary for normal operator work.
- Related reports / ADRs: `UX_6_COMMERCIAL_OPERATOR_MODEL_DISCOVERY_REPORT.md`, `UX_7_ATTENTION_LAYER_SPECIFICATION_REPORT.md`, `UX_5B_USER_DRAWER_POLISH_AND_COMMERCIAL_CERTIFICATION_REPORT.md`, `UX_4_CHANNEL_DRAWER_REBUILD_SPECIFICATION_REPORT.md`, `CHANNEL_DECISION_FIRST_1_OPERATOR_SURFACE_REPORT.md`, `CHANNEL_DECISION_FIRST_2_DRAWER_REPORT.md`, ADR-004.
- Last verified commit: `8ba2178f`.

## 18. Channel Operator Signal Model

- What it means: Channels must be presented through multiple operator signals, not through one mixed score that appears to explain everything.
- Source of truth: Existing Channel Decision V7 / assignment truth, channel suitability breakdown, service matrix, capacity/load state, route/topology readiness, runtime readiness, history, and current user counts.
- Where it is calculated: `admin/v7-admin-api` channel suitability, assignment, topology, and drawer helpers; planner assignment truth in `tools/v7-users-autoswitch`; operator projection in `admin_core/operator_decision_surface.py`.
- Where it is displayed: Channel table, Channel Drawer first-screen Signals block, technical diagnostics, and compact signal/tooltip presentation.
- What affects it: Planner decision/assignment role, selected moves, blockers, service availability, load/capacity posture, route readiness confidence, runtime readiness, stability, history, users on channel, and evidence freshness.
- What does NOT affect it: A single mixed score alone, raw trust/recovery labels alone, cosmetic table ordering, or UI-only labels without underlying existing truth.
- Operator meaning: "What did V7 decide, what compact signal explains it, how many users are affected, and what should I inspect next?" In the Channel Drawer, first-screen signals are compact support for the decision, not a score breakdown.
- Engineer meaning: A read-only classification layer over existing signals: operator signals, supporting signals, and diagnostics-only signals.
- Known caveats: First-level channel table signals are `Services`, `Load`, `Runtime`, and `Stability` in a stable S/L/R/T order so operators can understand dot position without widening the column. The operator-facing table renders them as compact dot indicators with meaning exposed through a minimal legend plus hover/focus/tap tooltips; the Channel Drawer renders the same signal set as compact clickable rows under the decision reason. The aggregate `Сигналы` table column must not be sorted as one mixed value; sorting is allowed only by an individual signal: Services, Load, Runtime, or Stability. No more than four first-level signals should be visible in one row. Route is supporting/diagnostics-only because the current route component is topology/readiness confidence and may be reduced by capacity or service state; it must not appear as a red first-level route failure unless planner/route evidence exposes a real route blocker. Services at first level track primary user-facing services; optional/hidden endpoint checks such as Anthropic API must not downgrade first-level Services by themselves. Technical Health remains diagnostics-only. Raw score components must not become an alternative planner or action owner, and diagnostics must explain observed reality instead of point deductions. First-level signal color is decision-aligned: red means the current planner/assignment decision requires removal, block, or immediate action. If the decision is `Use`, `Keep Current Users`, or `Emergency Only`, a raw diagnostic failure may remain visible as warning/diagnostic text, but it must not appear as a red first-level contradiction to the planner decision. Load/capacity warning means assignment pressure, not internet quality or channel speed failure. Operator Surface and Engineering Surface must stay separate: compact first-screen language tells the operator what to do; diagnostics may explain score inputs, confidence, evidence, and raw technical state. First-screen operator wording avoids generic "requires verification" phrasing and avoids `Уточнить`, `Требует проверки`, and `Уверенность неполная`; use `Нет свежих данных`, `Нет свежего подтверждения`, `Открыть матрицу сервисов`, `Открыть пользователей`, `Открыть логи`, or a concrete problem such as `Лимит назначений достигнут`.
- Related reports / ADRs: `CHANNEL_SIGNALS_1_MODEL_AUDIT_REPORT.md`, `CHANNEL_SIGNALS_2_TABLE_IMPLEMENTATION_REPORT.md`, `CHANNEL_SIGNALS_2A_SEMANTICS_REPORT.md`, `CHANNEL_SIGNALS_2B_ALIGNMENT_REPORT.md`, `CHANNEL_SIGNALS_2C_OPERATOR_SURFACE_REPORT.md`, `CHANNEL_SCORE_REALITY_AUDIT.md`, `CHANNEL_ROUTE_COMPONENT_REALITY_AUDIT_REPORT.md`, `CAPACITY_1_REALITY_AUDIT_REPORT.md`, `DIAGNOSTICS_1_REALITY_FIRST_REBUILD_REPORT.md`, `CHANNELS_OPERATOR_ENGINEER_SEPARATION_REPORT.md`, ADR-002, ADR-003, ADR-004, ADR-006, ADR-007, ADR-008, ADR-009, ADR-010.
- Last verified commit: `2fb9d205`.

## 19. UI Density Rules

- What it means: V7 admin screens use one compact visual rhythm so operators can scan more useful information per viewport without losing hierarchy.
- Source of truth: Existing admin CSS/layout primitives in `admin/v7-admin-api`: `.metric`, `.stat-card`, `.cards-grid`, `.check-card`, `.filterbar`, `.filter-chip`, channel table, and Channel Drawer section classes.
- Where it is calculated: UI rendering and CSS only. Density rules do not calculate planner truth, channel score, assignment, capacity, route, service, runtime, or history semantics.
- Where it is displayed: Overview, Users, Channels, Routes, Operator, Checks, Channel table, Channel Drawer, and shared dashboard cards.
- What affects it: Card padding/height, section spacing, table row padding, filter chrome, drawer section spacing, and placement of explanatory legends.
- What does NOT affect it: Planner decisions, assignment eligibility, score formulas, signal severity, execution readiness, storage, snapshots, APIs, or runtime state.
- Operator meaning: "The screen should show the answer and next action without wasting vertical space." Cards are compact status summaries, filters behave like lightweight navigation, tables prefer useful density, and drawers keep readable but tight sections.
- Engineer meaning: A shared UI standard over existing components. Channels, Users, Routes, Operator, and Checks should reuse the same dashboard card sizing instead of each tab inventing its own visual scale.
- Known caveats: Density must not hide required operator answers. Mobile 390px views must keep filters horizontally usable without clipping. Channel signal explanation must not consume a standalone row; the S/L/R/T legend belongs inside the Signals column header, with detailed meaning in the existing tooltip source.
- Related reports / ADRs: `CHANNELS_FINAL_DENSITY_AND_CONSISTENCY_REPORT.md`, `CHANNELS_OPERATOR_ENGINEER_SEPARATION_REPORT.md`, `CHANNELS_DRAWER_NO_DUPLICATES_ACTIONABLE_PROBLEMS_REPORT.md`, ADR-006, ADR-007, ADR-010.
- Last verified commit: `CHANNELS.TABLE_AND_LAYOUT_FINAL_POLISH implementation commit`.

## 20. Autonomous Routing Fit / Outcome / Recovery Foundation

- What it means: Read-only routing foundation that explains whether a user/channel recommendation is service/user/SLA fit, whether real outcome closure exists, whether a recovered channel may be re-admitted, whether anti-flap blocks rapid oscillation, and whether evidence is actionable now or stale.
- Source of truth: Existing operator decision surface, intelligence snapshots, service/user/channel score families, trust-evolution summaries, candidate suitability, best-available-pool, audit/feedback/closure records, and knowledge quality read model.
- Where it is calculated: `admin_core/autonomy_trust_acceleration.py` through `build_service_user_sla_fit`, `build_decision_outcome_closure`, `build_recovery_admission`, `build_anti_flapping`, `build_freshness_actionability`, and `build_routing_recommendation_readiness`.
- Where it is displayed: `tools/v7-autonomy-trust-evidence-inventory` full JSON and `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only`.
- What affects it: Required services, service freshness, channel candidate quality, capacity/headroom hints, policy eligibility, route/runtime safety hints, current assignment, real decision/packet/apply/verification/outcome/learning records, recovery successful checks, cooldowns, quarantine/degraded lifecycle, and rapid reverse movement evidence.
- What does NOT affect it: It does not change planner formulas, floors, assignment selection, service score formulas, recovery trust formulas, governance, execution, storage, snapshots, daemon state, or runtime apply authority.
- Operator meaning: "Do we actually know this user should stay or move, and what blocks that answer right now?"
- Engineer meaning: Existing-owner read model that turns known routing gaps into explicit JSON contracts before any planner or autonomy authority changes.
- Known caveats: This is not a new planner and not autonomy authority. `routing_recommendation_readiness` may say `NOT_READY_FOR_AUTONOMOUS_ROUTING` even while planner previews exist. Recovery admission is staged and read-only; one successful check must not jump a channel to fully trusted. Decision outcome closure requires real fields and must not synthesize outcomes. Freshness actionability classifies stale/missing evidence as recheck/unknown instead of pretending it is usable. Anti-flap currently detects oscillation from existing decision/audit records only.
- Related reports / ADRs: `docs/reports/V7_AUTONOMOUS_ROUTING_FIT_OUTCOME_RECOVERY_FOUNDATION_REPORT.md`, ADR-V7-SERVICE-USER-SLA-FIT-MODEL, ADR-V7-RECOVERY-ADMISSION-ANTI-FLAP, ADR-V7-FRESHNESS-ACTIONABILITY, `docs/reports/V7_KNOWLEDGE_QUALITY_READ_MODEL_REPORT.md`.
- Last verified commit: `V7.AUTONOMOUS.ROUTING.FIT_OUTCOME_RECOVERY_FOUNDATION implementation commit`.

## 21. Knowledge To Decision Integration

- What it means: Existing routing knowledge now influences the existing read-only operator decision surface before packet/governed execution preview. It can suppress unsafe recommendations, redirect a recommendation to a safer SLA-fit candidate, and expose readiness blockers without granting runtime apply authority.
- Source of truth: Existing `operator_decision_surface`, `autonomy_trust_acceleration` routing foundation models, intelligence snapshot statuses, candidate/best-pool snapshots, trust-evolution recovery state, and existing decision/audit records.
- Where it is calculated: `admin_core/operator_decision_surface.py::build_knowledge_decision_overlay`, `_apply_knowledge_to_user_row`, and `build_batch_preview`; reused foundation logic lives in `admin_core/autonomy_trust_acceleration.py`.
- Where it is displayed: Operator decision surface JSON, batch preview `knowledge_decision_readiness`, admin/operator consumers that read user recommendation rows and review/blocker fields.
- What affects it: Explicit stale suitability evidence, hard service/user/SLA fit blockers, degraded/quarantined recovery targets, anti-flap oscillation records, and decision outcome closure/readiness state.
- What does NOT affect it: It does not change planner formulas, trust floors, confidence floors, assignment formulas, runtime apply authority, governance, restore barrier behavior, storage, snapshots, daemons, or timers.
- Operator meaning: "The recommendation is now filtered through current knowledge gates before it becomes a visible movement candidate."
- Engineer meaning: Safe integration layer over the existing decision projection. It is not a planner fork; it only annotates, blocks, or retargets preview recommendations using existing read models.
- Known caveats: Missing optional snapshots should not become hard blockers by themselves. Free-form candidate `reasons` are not missing service requirements. NEW channels may still require CTR review without being hard-blocked by recovery admission; degraded/quarantined/cooldown/service-specific recovery blockers remain hard blockers. `runtime_apply_allowed` remains `false`.
- Related reports / ADRs: `docs/reports/V7_KNOWLEDGE_TO_DECISION_INTEGRATION_REPORT.md`, `docs/reports/V7_AUTONOMOUS_ROUTING_FIT_OUTCOME_RECOVERY_FOUNDATION_REPORT.md`, `docs/reports/V7_KNOWLEDGE_QUALITY_READ_MODEL_REPORT.md`, ADR-V7-SERVICE-USER-SLA-FIT-MODEL, ADR-V7-RECOVERY-ADMISSION-ANTI-FLAP, ADR-V7-FRESHNESS-ACTIONABILITY.
- Last verified commit: `V7.KNOWLEDGE_TO_DECISION.INTEGRATION implementation commit`.

## 22. Decision To Outcome To Learning Integration

- What it means: Existing governed/manual decisions can now close into outcome quality, learning records, knowledge growth, and read-only decision effectiveness. This completes the read-only chain `decision -> outcome -> learning -> better future decisions` without granting runtime apply authority.
- Source of truth: Existing execution feedback contracts, materialized feedback/closure records, trust-evolution summaries, intelligence snapshot refresh, autonomy trust/evidence inventory, and operator decision surface.
- Where it is calculated: `admin_core/operator_execution_feedback.py` builds outcome quality, knowledge growth, learning records, and effectiveness; `admin_core/intelligence_workers.py` embeds this model into existing `trust-evolution-summaries`; `admin_core/autonomy_trust_acceleration.py` exposes it through the existing trust inventory; `admin_core/operator_decision_surface.py` shows it in knowledge decision readiness.
- Where it is displayed: `trust-evolution-summaries.decision_outcome_learning`, `tools/v7-autonomy-trust-evidence-inventory` standard payload as `decision_outcome_learning`, `decision_effectiveness`, and `knowledge_growth`, plus operator batch preview `knowledge_decision_readiness`.
- What affects it: Real execution/verification/rollback outcomes, prediction expected/actual values, service/user outcome evidence, recommendation id, decision id, packet id when present, and materialized learning records.
- What does NOT affect it: It does not create synthetic evidence, new storage, a new snapshot family, a new feedback system, a new learning engine, a planner fork, governance changes, execution changes, daemon/timer changes, runtime apply, or user movement.
- Operator meaning: "After a decision closes, did it work, what did V7 learn, and did confidence/suitability/recovery knowledge improve or degrade?"
- Engineer meaning: Existing feedback and intelligence owners now expose outcome quality (`SUCCESS`, `PARTIAL_SUCCESS`, `FAILED`, `UNKNOWN`), knowledge growth, and effectiveness metrics that survive refresh/rebuild/reread through existing snapshots.
- Known caveats: Effectiveness is only as strong as real outcome records. Missing packet ids or service/user outcomes remain closure gaps; they must be produced by real governed/manual outcomes, not fabricated. The model is read-only and cannot certify autonomy by itself while confidence/trust/prediction/suitability floors remain weak.
- Related reports / ADRs: `docs/reports/V7_DECISION_TO_OUTCOME_TO_LEARNING_INTEGRATION_REPORT.md`, `docs/reports/V7_KNOWLEDGE_TO_DECISION_INTEGRATION_REPORT.md`, `docs/reports/V7_AUTONOMOUS_ROUTING_FIT_OUTCOME_RECOVERY_FOUNDATION_REPORT.md`, `docs/reports/V7_KNOWLEDGE_QUALITY_READ_MODEL_REPORT.md`, ADR-EVENT-DRIVEN-AUTONOMY, ADR-OBSERVED-OUTCOME-PRIMARY-TRUST.
- Last verified commit: `V7.DECISION_TO_OUTCOME_TO_LEARNING.INTEGRATION implementation commit`.

## 23. Governed Canary Knowledge-Gated Dry-Run Cycle

- What it means: V7 now has a single read-only entrypoint that automatically runs the governed canary preparation cycle from event/current state through knowledge-gated decision, candidate selection, packet preview, restore/rollback preview, verification plan, outcome closure plan, learning path, and next-step decision. It is allowed to stop only at a classified stop reason, with `AUTHORITY_BOUNDARY` being the intended legitimate boundary before operator approval / restore-barrier write / apply.
- Source of truth: Existing event sources, existing `operator_decision_surface`, existing knowledge quality and routing foundation overlays, existing autonomous dry-run safety gates, existing packet/restore/rollback owners, and existing feedback/learning owners.
- Where it is calculated: `admin_core/operator_execution_pipeline.py::governed_canary_knowledge_gated_dry_run_cycle`; CLI surface `tools/v7-governed-canary-dry-run-cycle`.
- Where it is displayed: CLI JSON payload and future admin/operator consumers that read `cycle_id`, `candidate`, `target`, `decision`, `knowledge_gates`, `packet_preview`, `restore_status`, `rollback_status`, `verification_plan`, `outcome_closure_plan`, `learning_path`, `stop_reason`, and `next_action`.
- What affects it: Current event rows, current planner/decision-surface candidate state, service/user/SLA fit, freshness actionability, recovery admission, anti-flapping, decision effectiveness, knowledge quality, routing recommendation readiness, packet preview readiness, restore/rollback preview readiness, and closure/learning connectivity.
- What does NOT affect it: It does not create a planner, governance model, execution path, truth source, storage, snapshot family, daemon, timer, runtime apply authority, synthetic evidence, or user movement. It does not lower confidence/trust/prediction floors.
- Operator meaning: "V7 can prepare the next governed one-user canary packet by itself and tell me exactly where it must stop for my approval."
- Engineer meaning: Existing-owner orchestration contract that makes non-authority gaps test-failing and visible: `MISSING_OWNER`, `DISCONNECTED_OWNER`, `MISSING_FIELD`, `MISSING_TRIGGER`, `MISSING_STATE_TRANSITION`, `MISSING_CLI_OR_API_SURFACE`, `MISSING_VERIFICATION_STEP`, `MISSING_DOCUMENTED_POLICY`, `MISSING_TEST_COVERAGE`, or `AUTHORITY_BOUNDARY`.
- Known caveats: The local workspace without `/opt/v7` production state correctly returns `MISSING_TRIGGER`; that is not a runtime failure and not an apply attempt. Production deployment at `71c216cf0c51bbb22430045dd962bc62dbfb1f81` proved the CLI can read real runtime state and stop at `AUTHORITY_BOUNDARY` with `10.7.0.5 vless -> awg3`, packet preview ready, restore/rollback preview ready, verification/outcome/learning connected, `apply=false`, and `users_moved=0`. If the cycle stops before `AUTHORITY_BOUNDARY`, the next phase must fix the existing owner gap and rerun rather than writing another discovery-only report.
- Related reports / ADRs: `docs/reports/V7_GOVERNED_CANARY_KNOWLEDGE_GATED_AUTONOMOUS_DRY_RUN_CYCLE_REPORT.md`, `docs/reports/V7_DECISION_TO_OUTCOME_TO_LEARNING_INTEGRATION_REPORT.md`, `docs/reports/AUTONOMY_TIER1_GOVERNED_CANARY_READINESS_REPORT.md`, ADR-EVENT-DRIVEN-AUTONOMY.
- Last verified commit: `71c216cf0c51bbb22430045dd962bc62dbfb1f81`.

## 24. Autonomy-Grade Suitability Program

- What it means: Suitability is now evaluated as a read-only knowledge program, not just as a trust component. V7 can explain current suitability maturity, what it measures, why it increased/decreased, what knowledge is missing, and which real outcome activities grow suitability fastest.
- Source of truth: Existing candidate suitability snapshots, candidate outcome matcher, trust-evolution suitability rows, decision outcome learning, freshness actionability, service/user/SLA fit, and outcome leverage model.
- Where it is calculated: `admin_core/autonomy_trust_acceleration.py` through `build_suitability_quality_model`, `build_suitability_knowledge_growth_model`, `build_suitability_effectiveness_expansion`, and `build_autonomy_grade_suitability_program`.
- Where it is displayed: `tools/v7-autonomy-trust-evidence-inventory` standard payload as `suitability_quality_model`, `suitability_knowledge_growth`, `suitability_effectiveness_expansion`, and `autonomy_grade_suitability_program`; the knowledge quality read model also overlays Suitability with autonomy-grade stage and blockers.
- What affects it: Real candidate outcomes, consumed candidate coverage, mean correctness, mean candidate confidence, suitability confidence, freshness/actionability, decision correctness, fit correctness, service/user outcome learning, rollback rate, and evidence pipeline loss.
- What does NOT affect it: It does not change planner formulas, candidate ranking, trust formulas, confidence floors, governance, execution, storage, snapshot families, daemon/timer state, runtime apply authority, or user movement. It does not create synthetic candidate outcomes.
- Operator meaning: "V7 can now say whether it truly knows that a candidate channel fits a user, what is still missing, and what real action would improve that knowledge."
- Engineer meaning: Existing-owner read model for graduating suitability from `STABLE_SIGNAL` toward `CONFIRMED_KNOWLEDGE`, `ACTIONABLE_KNOWLEDGE`, and `AUTONOMY_GRADE_KNOWLEDGE`.
- Known caveats: Current production suitability remains `STABLE_SIGNAL`, next stage `CONFIRMED_KNOWLEDGE`, and not autonomy-grade. Production inventory at deployed code commit `b16cea5f0d77585f9f0c16bf41a9106641f36e07` reports `156` candidates, `84` consumed candidate outcomes, `72` missing candidate outcomes, coverage ratio `0.5385`, mean correctness `68.107`, mean candidate confidence `0.411`, suitability confidence `29.358`, and freshness `ACTIONABLE_NOW`. Prediction/service cycles alone cannot make suitability autonomy-grade. `user_improvement_rate` is visible as unknown until the feedback owner emits it explicitly. Real governed/manual candidate outcomes are still required before higher autonomy.
- A4 representative evidence scope: `candidate_key` is currently a concrete `user -> candidate_channel` pair, and `candidate_count` is an enumeration of those pairs from the current suitability snapshot. This is useful as a suitability knowledge signal, but it must not be treated as a permanent requirement to exhaustively observe every user/channel combination before action-class promotion. Action-class promotion remains owned by `POLICY_005_ACTION_CLASS_PROMOTION`, OMP, and backlog item `A4`; production-grade certification should use representative class evidence, risk segmentation, rollback/no-rollback proof, blast-radius history, freshness, anti-flap, verification, and learning. Candidate enumeration may inform that decision but must not replace action-class evidence. Need New Owner remains `FALSE`; Need New Backlog Item remains `FALSE`.
- Action Class Certification Model: the first Action Class is `single-user governed candidate failover`. A4 owns only representative real outcome evidence for this class; A4 does not by itself certify runtime autonomy, class authority, delegated policy, or packet approval retirement. Full first-class certification requires the existing chain `A4 representative outcomes -> A5 blast-radius proof -> A6 runtime eligibility arbitration -> B13 metric reliability -> B12/class authority evaluation`. Mandatory proof classes are real outcomes, terminal classification, verification, rollback/no-rollback semantics, blast radius, freshness/safety/anti-flap, learning materialization, runtime eligibility consumption, metric reliability, and authority policy approval. `missing_candidate_outcomes` and `candidate_count` are inventory and coverage signals only; they may inform certification but must not be the canonical hard gate. Need New Owner remains `FALSE`; Need New Backlog Item remains `FALSE`; Need New Architecture remains `FALSE`.
- OMP Certification Signal Classification Model: across the entire OMP certification chain, every metric must be classified before it is used as a blocker. Canonical classes are `CERTIFICATION_REQUIREMENT`, `SUPPORTING_EVIDENCE`, `COVERAGE_SIGNAL`, `INVENTORY_SIGNAL`, `LEARNING_SIGNAL`, `RELIABILITY_SIGNAL`, `OPTIMIZATION_SIGNAL`, and `IMPLEMENTATION_ARTIFACT`. Inventory and coverage metrics may support certification, learning, and reliability analysis, but they must not become hard certification blockers unless the canonical owner explicitly defines them as mandatory for that stage. The current first divergence is the A4/B13 evidence owner treating `missing_candidate_outcomes` as missing evidence rather than an inventory/coverage signal. Existing owners remain sufficient: OMP, `A4`, `B13`, `admin_core.autonomy_trust_acceleration`, feedback/learning owners, and the runtime enablement read model. Need New Owner remains `FALSE`; Need New Backlog Item remains `FALSE`; Need New Architecture remains `FALSE`.
- Related reports / ADRs: `docs/reports/V7_AUTONOMY_GRADE_SUITABILITY_PROGRAM_REPORT.md`, `docs/reports/V7_HIGHEST_LEVERAGE_OUTCOME_GROWTH_REPORT.md`, `docs/reports/V7_DECISION_TO_OUTCOME_TO_LEARNING_INTEGRATION_REPORT.md`, `docs/reports/AUTONOMY_CANDIDATE_OUTCOME_REALITY_COLLECTION_REPORT.md`, ADR-EVENT-DRIVEN-AUTONOMY, ADR-OBSERVED-OUTCOME-PRIMARY-TRUST.
- Last verified commit: `b16cea5f0d77585f9f0c16bf41a9106641f36e07`.

## 25. Autonomous Knowledge Growth Program

- What it means: V7 now exposes a read-only maturity model for existing autonomy cycles, so the system can show which cycles are manual, partially automated, autonomous until authority boundary, or fully autonomous. The program does not create a new autonomy engine; it measures and continues existing knowledge/decision/outcome/learning cycles until a legitimate boundary or unsafe condition.
- Source of truth: Existing trust/evidence inventory, knowledge quality read model, suitability quality and growth models, prediction plan, real outcome source inventory, freshness actionability, recovery admission, decision outcome closure, decision outcome learning, routing recommendation readiness, outcome leverage model, and governed canary dry-run proximity.
- Where it is calculated: `admin_core/autonomy_trust_acceleration.py::build_autonomous_knowledge_growth_program`, exposed through `build_acceleration_inventory` and `tools/v7-autonomy-trust-evidence-inventory`.
- Where it is displayed: Standard trust/evidence inventory JSON as `autonomous_knowledge_growth_program`.
- What affects it: Existing cycle triggers, state transitions, real outcome availability, candidate outcome coverage, forecast/actual rows, service/channel evidence, freshness, recovery state, closure completeness, learning records, dry-run cycle readiness, and explicit authority boundaries.
- What does NOT affect it: It does not move users, execute apply, enable daemons, write restore barriers, create evidence, create storage, create snapshots, create a planner, change governance, change execution, lower floors, or change suitability/trust/prediction formulas.
- Operator meaning: "How much of V7's learning and preparation can run by itself before it correctly asks for authority?"
- Engineer meaning: Existing-owner maturity inventory and guardrail contract for autonomy cycles. Each cycle reports owner, trigger, state transitions, output, authority boundary, automation level, gap classes, blockers, and safe next step. Runtime safety flags remain explicit: `runtime_apply_allowed=false`, `runtime_mutation_performed=false`, `users_moved=0`, `apply_executed=false`, `autonomy_enabled=false`.
- Known caveats: The current implementation is a maturity/readiness layer, not production apply. It can classify and expose autonomy progress, but cycles that require real governed/manual outcomes still stop at `AUTHORITY_BOUNDARY` or outcome-required blockers. Local workspace dry-run may stop at `MISSING_TRIGGER` when `/opt/v7` production state is unavailable. Production deployment of implementation commit `d86a38c13c2b78626e68e622583ce08a72f37763` verified `autonomous_knowledge_growth_program` with `12` cycles, maturity score `84.167`, and safety flags `apply_executed=false`, `users_moved=0`, `runtime_mutation=false`. Final production deployment of owner-path fix commit `33619fd7c31c8cc92d4964d00d01400b251a9616` verified that runtime `v7-governed-canary-dry-run-cycle` resolves the existing planner owner correctly and reaches `AUTHORITY_BOUNDARY` for `10.7.0.5 vless -> awg3` with no apply and no movement.
- Related reports / ADRs: `docs/reports/V7_AUTONOMOUS_KNOWLEDGE_GROWTH_PROGRAM_REPORT.md`, `docs/reports/V7_AUTONOMY_GRADE_SUITABILITY_PROGRAM_REPORT.md`, `docs/reports/V7_GOVERNED_CANARY_KNOWLEDGE_GATED_AUTONOMOUS_DRY_RUN_CYCLE_REPORT.md`, `docs/reports/V7_DECISION_TO_OUTCOME_TO_LEARNING_INTEGRATION_REPORT.md`, `docs/reports/V7_HIGHEST_LEVERAGE_OUTCOME_GROWTH_REPORT.md`, ADR-EVENT-DRIVEN-AUTONOMY, ADR-OBSERVED-OUTCOME-PRIMARY-TRUST.
- Last verified commit: `33619fd7c31c8cc92d4964d00d01400b251a9616`.

## 26. Autonomous Routing Evolution Program

- What it means: V7 now has a read-only evolution view that ties the existing knowledge growth, suitability, outcome leverage, decision/outcome/learning, event preparation, and TIER_2 readiness models into one payload. It answers: which phases advanced, what remains blocked, how far TIER_2 is, and where the system must stop.
- Source of truth: Existing `autonomous_knowledge_growth_program`, `autonomy_grade_suitability_program`, `suitability_quality_model`, `suitability_knowledge_growth`, `suitability_effectiveness_expansion`, `outcome_leverage_model`, `knowledge_quality_read_model`, `routing_recommendation_readiness`, `decision_outcome_learning`, `canary_proximity`, `real_outcome_growth_projection`, candidate outcome collection, prediction plan, and real outcome source inventory.
- Where it is calculated: `admin_core/autonomy_trust_acceleration.py::build_autonomous_routing_evolution_program`, exposed through `build_acceleration_inventory`.
- Where it is displayed: `tools/v7-autonomy-trust-evidence-inventory` standard payload as `autonomous_routing_evolution_program`.
- What affects it: Current autonomy cycle maturity, suitability stage, candidate outcome gap, decision correctness, fit correctness, outcome quality, learning growth, routing readiness, canary floor gaps, prediction/source evidence, and highest-leverage real outcome activities.
- What does NOT affect it: It does not change planner formulas, trust formulas, floors, governance, execution, storage, snapshot families, daemon/timer state, event authority, restore-barrier behavior, runtime apply authority, or user assignments.
- Operator meaning: "How close is V7 to governed TIER_2, and what exact real-world evidence or authority is still missing?"
- Engineer meaning: Existing-owner integration read model for phases A-F of autonomous routing evolution: knowledge growth, suitability outcomes, confirmed knowledge, actionable knowledge, event-to-decision-to-outcome, and TIER_2 readiness.
- Known caveats: This is an evolution/readiness surface, not a controller. It can show `AUTHORITY_BOUNDARY`, `REAL_GAP`, or `READY_FOR_TIER_2_GOVERNED_REVIEW`, but it cannot approve apply. Local workspace without production runtime state can show zero floor values; production inventory is required for runtime-grade numbers. Production deployment at `702f7f91e53a42d55aa47f29c5d598960de46130` exposes the evolution program, verifies `AUTHORITY_BOUNDARY`, reports phases A=`ADVANCED`, B=`REAL_OUTCOMES_REQUIRED`, C/D/F=`BLOCKED`, E=`AUTONOMOUS_UNTIL_AUTHORITY_BOUNDARY`, keeps `apply_executed=false`, `users_moved=0`, `runtime_mutation_performed=false`, and leaves TIER_2 blocked by confidence `39.543`, trust `54.657`, prediction `36.73`, and suitability `29.405`.
- Related reports / ADRs: `docs/reports/V7_AUTONOMOUS_ROUTING_EVOLUTION_PROGRAM_REPORT.md`, `docs/reports/V7_AUTONOMOUS_KNOWLEDGE_GROWTH_PROGRAM_REPORT.md`, `docs/reports/V7_AUTONOMY_GRADE_SUITABILITY_PROGRAM_REPORT.md`, `docs/reports/V7_HIGHEST_LEVERAGE_OUTCOME_GROWTH_REPORT.md`, `docs/reports/V7_GOVERNED_CANARY_KNOWLEDGE_GATED_AUTONOMOUS_DRY_RUN_CYCLE_REPORT.md`, ADR-EVENT-DRIVEN-AUTONOMY, ADR-OBSERVED-OUTCOME-PRIMARY-TRUST.
- Last verified commit: `702f7f91e53a42d55aa47f29c5d598960de46130`.

## 27. Maximum Reality Knowledge Extraction

- What it means: V7 exposes a read-only maximum-reality extraction model that classifies every missing routing-knowledge item by what can be obtained from the current production system: `OBTAINABLE_NOW`, `OBTAINABLE_AFTER_EXISTING_EVENT`, `OBTAINABLE_AFTER_GOVERNED_ACTION`, `REQUIRES_MORE_USERS`, `REQUIRES_MORE_CHANNELS`, `REQUIRES_NEW_SERVICES`, or `REQUIRES_NEW_ARCHITECTURE`. It is designed to stop repeated speculation about whether more testing can raise autonomy when the missing evidence has not physically happened yet.
- Source of truth: Existing acceleration inventory inputs: autonomous knowledge growth, autonomous routing evolution, candidate outcome reality collection, real outcome source inventory, real outcome growth projection, suitability quality/growth, prediction collection plan, decision outcome closure/learning, freshness actionability, and outcome leverage.
- Where it is calculated: `admin_core/autonomy_trust_acceleration.py::build_maximum_reality_knowledge_extraction`, exposed through `build_acceleration_inventory`.
- Where it is displayed: `tools/v7-autonomy-trust-evidence-inventory` standard payload as `maximum_reality_knowledge_extraction`.
- What affects it: Current candidate outcome coverage, never-happened candidate outcomes, hidden/captured-but-not-consumed outcomes, prediction pending rows, service/channel outcome source utilization, closure completeness, learning records, freshness domains, and existing cycle maturity.
- What does NOT affect it: It does not run probes by itself, move users, apply autoswitch, write restore barriers, create evidence, create storage, change formulas, change floors, create a planner, create governance, create an execution path, create a truth source, or enable daemons.
- Operator meaning: "What real routing knowledge can V7 still obtain today, and where does it honestly have to wait for a real event or operator-approved action?"
- Engineer meaning: Deterministic read-only maximum-extraction inventory and physical-limit classifier over existing owners. It also projects maximum current suitability from current candidate rows without adding users, channels, services, formulas, or floor changes.
- Known caveats: Local workspace without production runtime state can show zero candidate/suitability values. Runtime inventory is required for production-grade maximum suitability and physical-limit values. Missing candidate outcomes marked `never_happened` are not hidden evidence; they require real governed/manual action and post-action outcome closure before they can become knowledge. Production deployment at `215757eb21e8c8c6c4222bd3810bd9e9a7b3edb7` reports `72` missing candidate outcomes, `0` obtainable now, `72` obtainable after governed action, maximum projected current suitability `54.312`, and remaining unreachable gap to the `70` suitability floor `15.688`; no more users, channels, or services are required for those 72 current candidate outcomes, but real governed/manual action is required.
- Related reports / ADRs: `docs/reports/V7_MAXIMUM_REALITY_KNOWLEDGE_EXTRACTION_REPORT.md`, `docs/reports/V7_AUTONOMOUS_ROUTING_EVOLUTION_PROGRAM_REPORT.md`, `docs/reports/AUTONOMY_CANDIDATE_OUTCOME_REALITY_COLLECTION_REPORT.md`, `docs/reports/V7_AUTONOMY_GRADE_SUITABILITY_PROGRAM_REPORT.md`, ADR-EVENT-DRIVEN-AUTONOMY, ADR-OBSERVED-OUTCOME-PRIMARY-TRUST.
- Last verified commit: `215757eb21e8c8c6c4222bd3810bd9e9a7b3edb7`.

## 28. Final Autonomous Routing Architecture Certification

- What it means: V7 now exposes a final read-only architecture certification that answers whether the system has every fundamental knowledge source, decision capability, lifecycle stage, routing capability, and autonomy cycle required for an autonomy-grade routing control plane. This is an architecture certification, not runtime permission and not a trust/floor certification.
- Source of truth: Existing canonical reference, SYSTEM_MAP, autonomy blueprint, ideal autonomous routing model, knowledge quality model, certified reports through `V7_MAXIMUM_REALITY_KNOWLEDGE_EXTRACTION_REPORT.md`, and the existing trust/evidence inventory owners.
- Where it is calculated: `admin_core/autonomy_trust_acceleration.py::build_final_autonomous_routing_architecture_certification`, exposed through `build_acceleration_inventory`.
- Where it is displayed: `tools/v7-autonomy-trust-evidence-inventory` standard payload as `final_autonomous_routing_architecture_certification`.
- What affects it: Existing knowledge quality objects, autonomous knowledge growth cycles, autonomous routing evolution, maximum reality extraction, service/user/SLA fit, outcome closure, learning, recovery admission, anti-flapping, freshness/actionability, suitability quality, candidate outcome reality, real outcome source inventory, prediction plan, and canary proximity.
- What does NOT affect it: It does not move users, execute apply, enable autonomy, create a daemon, create a new planner, create governance, create execution, create storage, create a truth source, create synthetic evidence, change formulas, change floors, or change runtime assignments.
- Operator meaning: "V7 has the architectural parts it needs; remaining work is to earn real experience and authority before it may move users autonomously."
- Engineer meaning: The certification machine-checks `EXISTS` / `PARTIAL` / `MISSING` across knowledge sources, decisions, lifecycle stages, autonomy cycles, routing capabilities, and duplication/owner reuse. Fundamental missing classes are empty; partial classes are future/authority/reality extensions rather than new architecture owners.
- Known caveats: The final architecture synthesis supersedes the older wording `ARCHITECTURE_COMPLETE_WITH_FUTURE_OPTIONAL_EXTENSIONS` with `ARCHITECTURE_COMPLETE`: remaining architectural weaknesses are `0`, while direct client telemetry, 10k-scale cohort/SLA aggregate views, long-horizon evidence aging/retirement, and operator-free quarantine/recovery apply certification remain optional future improvements. Runtime autonomy remains limited by real-world experience and authority: confidence, trust, prediction, suitability, candidate outcomes, and explicit apply authority still must pass through existing owners. Production deployment at `39c46ed379ff4a2ccadb84a49a0dd9dcd2de579b` reports `17` existing knowledge-source classes, `4` partial classes, `0` fundamental missing classes, `9` existing decisions, `2` partial decisions, `7` existing lifecycle stages, `2` partial lifecycle stages, `10` existing routing capabilities, `72` missing candidate outcomes, canary blockers `confidence`, `trust`, and `prediction_confidence`, with `apply_executed=false`, `users_moved=0`, and `autonomy_enabled=false`.
- Related reports / ADRs: `docs/reports/V7_FINAL_AUTONOMOUS_ROUTING_ARCHITECTURE_CERTIFICATION_REPORT.md`, `docs/reports/V7_MAXIMUM_REALITY_KNOWLEDGE_EXTRACTION_REPORT.md`, `docs/reports/V7_AUTONOMOUS_ROUTING_EVOLUTION_PROGRAM_REPORT.md`, `docs/reports/V7_AUTONOMOUS_KNOWLEDGE_GROWTH_PROGRAM_REPORT.md`, `docs/reports/V7_GOVERNED_CANARY_KNOWLEDGE_GATED_AUTONOMOUS_DRY_RUN_CYCLE_REPORT.md`, ADR-EVENT-DRIVEN-AUTONOMY, ADR-OBSERVED-OUTCOME-PRIMARY-TRUST.
- Last verified commit: `39c46ed379ff4a2ccadb84a49a0dd9dcd2de579b`.

## 29. Runtime Capability Maturation Program / RT Phase 2

- What it means: The old 12-stage RT Phase 2 plan is superseded by one six-workstream `Runtime Capability Maturation Program`. RT2 is not a Runtime replacement, Planner replacement, World Model replacement, Truth Source, Owner, Backlog, or parallel roadmap.
- Source of truth: OMP owns sequence, dependencies, entry/exit criteria, stop rules, graduation, and continuation. Runtime Model owns the runtime consumption contract. Decision Model owns decision/state/delta semantics. SYSTEM_MAP owns ownership lookup. Research Framework/Process owns external model collection and fit analysis workflow.
- Current execution order: `A5 -> A6 -> B13 -> B16 -> Runtime Capability Maturation Program -> B1 -> B2 -> B3 -> B4 -> B5 -> B6 -> B7 -> B8 -> B9 -> B10 -> B11 -> B12 -> B14 -> B15 -> B17 -> B18 -> B19 -> B20 -> B21 -> C1 -> C2 -> C3 -> C4 -> C5`.
- OMP Capability Transition Contract: OMP must explain why each next step becomes available, which capability produced evidence, which owners may consume it, which capability unlocks, which capability remains blocked, why the next step is safe, and why later steps remain forbidden. Transition logic belongs permanently in `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`, with owner lookup in `docs/reference/SYSTEM_MAP.md` and current transition state in `docs/programs/V7_CURRENT_PROGRAM_STATE.md` when state changes. Engineering reports may record evidence but must not be the only place that preserves transition logic.
- OMP Capability Production Contract: OMP must explain what capability each major stage produces, which evidence proves it, who owns it, who consumes it, which future capability/stage it unlocks, which capability/stage remains blocked, and why. The Capability Production Graph and producer/consumer matrix belong permanently in `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`, with owner lookup in `docs/reference/SYSTEM_MAP.md` and current produced capability state in `docs/programs/V7_CURRENT_PROGRAM_STATE.md` when state changes. Engineering reports may record evidence but must not be the only place that preserves production graph, producer/consumer relationships, or unlocked/blocked capability rules.
- OMP Progress Dashboard Model: OMP owns the permanent read-only dashboard model; Current Program State owns the volatile current dashboard snapshot; SYSTEM_MAP owns dashboard ownership lookup; Canonical Reference preserves only durable dashboard rules. The dashboard displays overall progress, current OMP state, capability progress, production graph, RT2 progress, Production Maturity, Engineering Intelligence, stop gates, transition explanation, and future capability-quality placeholders. It consumes canonical owners only and cannot decide, approve, rank implementation, mutate Runtime, certify evidence, expand authority, create a queue, replace Planner, create a roadmap, or become a truth source.
- OMP Dual-View Visualization: OMP Dashboard supports `OPERATOR_VIEW` and `ENGINEERING_VIEW` as two synchronized presentations of identical canonical data. Operator View is minimal, fast, card/progress/graph based, and hides engineering noise by default. Engineering View is complete, traceable, evidence-based, and exposes capability graph, production graph, producer/consumer matrix, transition contracts, owner mapping, evidence, blockers, RT2, and Engineering Intelligence. Both views consume OMP, SYSTEM_MAP, Current Program State, Production Maturity Model, and Canonical Reference only. Presentation may differ; state and truth must not.
- OMP Dashboard UI Foundation: OMP Dashboard is the canonical V7 OMP section inside the existing admin panel, exposed as the top-level `OMP` tab at `/admin/omp`. It must not replace the existing admin home / overview page and must not create a second app shell. Executive View is the first layer inside the OMP tab, with synchronized Operator View and Engineering View from the same canonical data. Existing Overview, Operator, Execution, Health/Read Model, Routing, Users, Channels, Checks, Logs, Settings, and Security surfaces keep their existing navigation meaning and may be drill-downs, not separate dashboard truth. Design HTML files are visual references only. The dashboard remains read-only, cannot implement Runtime behavior, cannot apply changes, cannot expand authority, cannot create a planner/queue/roadmap, cannot duplicate state/read models/truth, and cannot introduce chart requirements before a later implementation task.
- OMP Dashboard Design System: OMP Dashboard visual language is minimal, elegant, calm, fast, low-noise, progressively disclosed, traceable, and modern in both dark and light modes. Operator View prioritizes one-minute understanding through progress bars, current-stage cards, maturity indicators, stop-gate cards, risk/recommendation cards, and a simple capability graph. Engineering View prioritizes traceability through capability/production/dependency graphs, producer-consumer matrix, transition contracts, owner mapping, evidence, blockers, RT2, and Engineering Intelligence. Future implementation must follow this design system, but this rule does not create UI code, charts, Runtime behavior, OMP data-model changes, new read models, authority, or architecture.
- Current transition: C4 produced `all_at_once_promotion_unavailable_verification = DONE_READ_ONLY_ALL_AT_ONCE_PROMOTION_UNAVAILABLE`, so OMP continues to existing backlog item `C5` Preserve Rollback As Operational Compensation Rather Than Transaction Rollback. Runtime self-optimization, automatic recommendations, direct implementation without OMP, authority lowering, safety-gate weakening, Runtime apply, automation, registry write, concurrency enablement, authority expansion, blast-radius expansion, all-at-once promotion, direct class promotion, queue daemon, planner replacement, synthetic evidence, threshold/formula mutation, rollback/apply execution, and user movement remain forbidden.
- Continue OMP B1: `build_liveness_evidence_aggregation` exists in `admin_core.autonomy_trust_acceleration` as a read-only B1 implementation. It aggregates existing liveness evidence by source family, confidence, owner, freshness/status, and policy relevance from service matrix, Telegram sentinel, quality compact, route reality, hard-failure classification, and intelligence snapshot owners. B1 is `DONE_READ_ONLY`; it creates no synthetic evidence, changes no formulas, grants no authority, mutates no Runtime, applies no changes, and moves no users. B1 unlocks existing backlog item `B2` hard-failure timer/risk class policy windows.
- Continue OMP B2: `build_hard_failure_policy_windows` exists in `admin_core.autonomy_trust_acceleration` as a read-only B2 implementation. It maps hard-failure risk classes to existing action-class freshness windows and anti-flap policy impact without changing timers, creating evidence, changing formulas, granting authority, mutating Runtime, applying changes, or moving users. B2 unlocks existing backlog item `B3` soft-degradation trend threshold vocabulary alignment.
- Continue OMP B3: `build_soft_degradation_threshold_vocabulary_alignment` exists in `admin_core.autonomy_trust_acceleration` as a read-only B3 implementation. It maps existing quality compact, service matrix, planner/autoswitch, freshness, anti-flap, and hard-failure override evidence to canonical `POLICY_002_SOFT_DEGRADATION` results and decision vocabulary without changing thresholds, formulas, creating evidence, granting authority, mutating Runtime, applying changes, or moving users. B3 unlocks existing backlog item `B4` signal-to-policy degradation evidence mapping.
- Continue OMP B4: `build_degradation_signal_policy_mapping` exists in `admin_core.autonomy_trust_acceleration` as a read-only B4 implementation. It maps existing latency, error, timeout, loss, jitter, saturation, service-response, and route-readiness signal families to `POLICY_002_SOFT_DEGRADATION` meanings without making attribution claims, changing thresholds, changing formulas, creating evidence, granting authority, mutating Runtime, applying changes, or moving users. B4 unlocks existing backlog item `B5` observed degradation attribution.
- Continue OMP B5: `build_observed_degradation_attribution` exists in `admin_core.autonomy_trust_acceleration` as a read-only B5 implementation. It joins existing active service/quality observations and passive feedback/outcome/trust evidence by object, attributes only evidence sources, and makes no root-cause claims, threshold changes, formula changes, synthetic evidence, authority changes, Runtime mutation, apply behavior, or user movement. B5 unlocks existing backlog item `B6` V7-native degradation response mapping.
- Continue OMP B6: `build_v7_native_degradation_response_mapping` exists in `admin_core.autonomy_trust_acceleration` as a read-only B6 implementation. It maps circuit-breaker and outlier-ejection practice to existing V7-native actions without creating Runtime behavior, mutating thresholds/formulas, creating synthetic evidence, granting authority, applying changes, or moving users. B6 unlocks existing backlog item `B7` service-objective policy-threshold binding.
- Continue OMP B7: `build_service_objective_policy_threshold_binding` exists in `admin_core.autonomy_trust_acceleration` as a read-only B7 implementation. It binds required services, service freshness, fit score, capacity/headroom, route/runtime safety, soft-degradation policy, and degradation response objectives to existing threshold sources without changing thresholds/formulas, creating synthetic evidence, granting authority, mutating Runtime, applying changes, or moving users. B7 unlocks existing backlog item `B8` recovery admission certification.
- Continue OMP B8: `build_recovery_admission_certification` exists in `admin_core.autonomy_trust_acceleration` as a read-only B8 implementation. It certifies existing recovery admission evidence only when repeated successful checks, service readiness evidence, quality readiness evidence, freshness, and objective binding context are present, without admitting traffic, changing Runtime, changing thresholds/formulas, creating synthetic evidence, granting authority, applying changes, or moving users. B8 unlocks existing backlog item `B9` post-admission observation windows.
- Continue OMP B9: `build_post_admission_observation_windows` exists in `admin_core.autonomy_trust_acceleration` as a read-only B9 implementation. It verifies existing post-admission service observation and quality compact `5m`/`1h` windows after B8 recovery admission certification, without admitting traffic, changing Runtime, changing thresholds/formulas, creating synthetic evidence, granting authority, applying changes, or moving users. B9 unlocks existing backlog item `B10` recovery slow-start progression.
- Continue OMP B10: `build_recovery_slow_start_progression` exists in `admin_core.autonomy_trust_acceleration` as a read-only B10 implementation. It defines recovery slow-start as `OBSERVATION_CERTIFIED_READ_ONLY` -> `ONE_USER_GOVERNED_RECOVERY_REVIEW` -> `BEYOND_ONE_USER_ACTION_CLASS_REVIEW`, reusing B8/B9 and class-level blast-radius evidence without admitting traffic, changing Runtime, changing thresholds/formulas, creating synthetic evidence, granting authority, applying changes, or moving users. B10 unlocks existing backlog item `B11` org/cohort isolation and identity policy integration.
- Continue OMP B11: `build_org_cohort_identity_policy_integration` exists in `admin_core.autonomy_trust_acceleration` as a read-only B11 implementation. It integrates existing identity -> group/cohort -> allowed/preferred/excluded egress -> exclusive_group/egress ACL/default isolation gates through existing planner, identity, org-policy, channel-policy, OMP, Backlog, and Production Maturity owners without changing Runtime, changing thresholds/formulas, creating synthetic evidence, granting authority, applying changes, directly promoting classes, or moving users. B11 unlocks existing backlog item `B12` next action-class stage certification.
- Continue OMP B12: `build_next_action_class_stage_certification` exists in `admin_core.autonomy_trust_acceleration` as a read-only B12 implementation. It consumes A5 blast-radius evidence, A6 runtime eligibility arbitration, B13 blocking metric reliability, and B11 identity/policy boundaries into a next action-class stage certification gate without changing Runtime, changing thresholds/formulas, creating synthetic evidence, granting authority, applying changes, directly promoting classes, expanding blast radius, or moving users. B12 unlocks existing backlog item `B14` service/pool/cohort blast-radius scope.
- Continue OMP B14: `build_service_pool_cohort_blast_radius_scope` exists in `admin_core.autonomy_trust_acceleration` as a read-only B14 implementation. It maps service, pool, cohort, capacity, action-class, and blast-radius scope from existing service/user/SLA fit, B11 identity/cohort, A5 blast-radius, B12 stage-certification, and autoswitch capacity/load owners without changing Runtime, changing thresholds/formulas, creating synthetic evidence, granting authority, applying changes, directly promoting classes, expanding blast radius, or moving users. B14 unlocks existing backlog item `B15` containment/forward-fix classification.
- Continue OMP B15: `containment_forward_fix_classification` exists in `admin_core.operator_execution` and is surfaced through `admin_core.operator_execution_pipeline` as a read-only B15 implementation. It classifies no-execution-contained, forward-fix-verified, rollback-contained, containment-failed, partial-forward-fix, and unverified-forward-fix states from existing packet, verification, rollback, and partial-failure policy evidence without changing Runtime, changing thresholds/formulas, creating synthetic evidence, granting authority, applying changes, executing rollback, or moving users. B15 unlocks existing backlog item `B17` stale-read reporting with mutation blocking.
- Continue OMP B17: `build_stale_read_mutation_blocking` exists in `admin_core.autonomy_trust_acceleration` as a read-only B17 implementation. It preserves stale/unknown freshness visibility as reportable read-only evidence while blocking mutation through existing freshness actionability, runtime eligibility, routing readiness, truth/convergence, read-only inventory, OMP, Backlog, and Production Maturity owners without changing Runtime, changing thresholds/formulas, creating synthetic evidence, granting authority, applying changes, mutating from stale reads, or moving users. B17 unlocks existing backlog item `B18` owner-issued version/lease pattern.
- Continue OMP B18: `build_owner_issued_version_lease_pattern` exists in `admin_core.autonomy_trust_acceleration` as a read-only B18 implementation. It exposes owner-issued version/lease/generation/TTL/source-hash coverage by reusing existing execution lease, Runtime Model freshness gates, `SNAPSHOT_FAMILIES`, freshness actionability, action-class freshness windows, B17 stale-read mutation blocking, OMP, Backlog, and Production Maturity owners without changing lease behavior, changing Runtime, changing thresholds/formulas, creating synthetic evidence, granting authority, applying changes, creating a new owner, or moving users. B18 unlocks existing backlog item `B19` hysteresis and state-change-cost mapping.
- Continue OMP B19: `build_hysteresis_state_change_cost_mapping` exists in `admin_core.autonomy_trust_acceleration` as a read-only B19 implementation. It centralizes existing sticky/current bias, minimum improvement, cooldown, observation window, oscillation detection, user freeze, pair reversal, target block/quarantine, recovery thresholds, and freshness identity cost vocabulary without changing thresholds, formulas, Runtime, authority, planner ownership, synthetic evidence, or users. B19 unlocks existing backlog item `B20` hard-failure override anti-flap arbitration.
- Continue OMP B20: `build_hard_failure_override_anti_flap_arbitration` exists in `admin_core.autonomy_trust_acceleration` as a read-only B20 implementation. It encodes confirmed hard failure as anti-flap override candidate for authority review only, while suspected/no hard failure cannot override anti-flap. It does not execute override, change thresholds/formulas, mutate Runtime, expand authority, synthesize evidence, create a new owner, or move users. B20 unlocks existing backlog item `B21` per-user routing control mode.
- Continue OMP B21: `build_per_user_routing_control_mode` exists in `admin_core.autonomy_trust_acceleration` as a read-only B21 implementation. It exposes explicit or inferred per-user `AUTO` / `PINNED` / `MANUAL` routing control mode through existing user registry, group/org policy, planner gate, admin operator surface, B11 identity/cohort policy, B20 hard-failure/anti-flap, OMP, Backlog, and Production Maturity owners. It does not write the registry, mutate Runtime, expand authority, replace Planner, synthesize evidence, create a new owner, or move users. B21 unlocks existing backlog item `C1` fail-open/fail-closed action-class behavior.
- Continue OMP C1: `build_fail_open_fail_closed_action_class_behavior` exists in `admin_core.autonomy_trust_acceleration` as a read-only C1 implementation. It records fail-closed Runtime mutation/apply behavior per action class and allows only read-only fail-open diagnosis, evidence collection, operator explanation, Engineering Report, and Canonical Update. It does not change Runtime behavior, grant fail-open mutation, expand authority, replace Planner, synthesize evidence, create a new owner, or move users. C1 unlocks existing backlog item `C2` probabilistic suspicion advisory evidence.
- Continue OMP C2: `build_probabilistic_suspicion_advisory_evidence` exists in `admin_core.autonomy_trust_acceleration` as a read-only C2 implementation. It keeps shadow autonomy, source-confidence, and soft-degradation suspicion as advisory-only evidence with direct blocking power `NONE` and direct execution power `NONE`. It does not grant Runtime apply, expand authority, mutate thresholds/formulas, replace Planner, synthesize evidence, create a new owner, or move users. C2 unlocks existing backlog item `C3` break-glass authority audited exceptional operator policy.
- Continue OMP C3: `break_glass_authority_policy_contract` exists in `admin_core.operator_execution_pipeline` as a read-only C3 implementation. It defines break-glass as disabled-by-default, audited, exceptional operator policy only, requiring explicit operator policy, incident context, audit, verification/closure, truth/convergence, OMP, and Current Program State updates. It does not grant break-glass invocation, Runtime apply, automation, authority expansion, rollback/apply execution, synthesize evidence, replace Planner, create a new owner, or move users. C3 unlocks existing backlog item `C4` all-at-once promotion unavailable verification.
- Continue OMP C4: `build_all_at_once_promotion_unavailable_verification` exists in `admin_core.autonomy_trust_acceleration` as a read-only C4 implementation. It consumes action-class runtime enablement, A5 blast-radius certification, B12 next-stage certification, B14 service/pool/cohort scope, and C3 break-glass policy evidence to verify all-at-once/direct action-class promotion remains unavailable. It does not grant Runtime apply, automation, authority expansion, blast-radius expansion, direct class promotion, synthetic evidence, replace Planner, create a new owner, or move users. C4 unlocks existing backlog item `C5` rollback operational-compensation preservation.
- Current produced capability: C4 produced All-at-Once Promotion Unavailable Verification as a read-only owner-mapped implementation. The owner is existing OMP, blast-radius/action-class gates, Backlog, Production Maturity, and `admin_core.autonomy_trust_acceleration`. Consumers are OMP, `C5`, Current Program State, Production Maturity, Canonical Reference, Authority Evolution, Blast Radius, Rollback, Decision Explainability, Observability, and Production Autonomy. Runtime apply, automation, silent authority expansion, blast-radius expansion, all-at-once promotion, direct class promotion, rollback/apply execution, planner replacement, new owner, synthetic evidence, and user movement remain blocked.
- Workstreams: `RT2-S1` Measurement & Observability Foundation; `RT2-S2` World & Readiness Maturation; `RT2-S3` Desired-State Delta Preparedness; `RT2-S4` Governed Execution Coordination; `RT2-S5` Certified Concurrency Ladder; `RT2-S6` Evidence-Based Continuous Improvement.
- What does NOT change: No runtime behavior, automation, authority, deployment, apply path, user movement, synthetic evidence, new owner, new backlog, new planner, new runtime, new truth source, or new roadmap is created by RT2 canonicalization.
- Safety rule: Optimization is safety-certified only. Runtime remains thin and may only consume prepared knowledge, perform live validation, execute bounded certified mutation when authorized, verify, rollback/STOP_SAFE, close outcome, and feed learning from observed outcomes.
- Runtime Time Intelligence: Fits existing architecture. Runtime Model owns time semantics, time domains, topology, Work Placement, and thin-runtime constraints; `RT2-S1` owns read-only measurement/observability of time, latency, cost, waits, and dependency topology; `RT2-S6` owns evidence-based recommendations through OMP/backlog/canonical-owner flow. No new owner, Runtime, Planner, Truth Source, roadmap, automation, authority, or runtime behavior is created.
- Runtime Time Intelligence Capability Maturation: Complete as a canonical RT2-internal maturity ladder. Levels are Time Measurement, Time Domains, Time Topology, Critical Path, Time Budget, Dependency Weight, Impact Prediction, Engineering Recommendation, Certification, and Continuous Runtime Optimization Recommendation Loop. Levels 1-5 mature measurement/structure through Runtime Model and `RT2-S1`; levels 6-10 mature recommendation/certification/learning through `RT2-S6`, OMP, Production Maturity, Backlog, Learning owners, and existing canonical owners. Runtime self-optimization remains forbidden.
- External models: External/world-practice models enter through Research Framework/Process, V7 Fit Analysis, Work Placement Review, Safety/Authority/Verification/Rollback/Freshness Review, and then canonical owner/backlog mapping only if applicable. They never override V7 directly.
- Current status: `ACTIVE_IMPLEMENTATION`; RT2-S1 through RT2-S6 are complete as read-only/advisory owner-mapped surfaces; `C5` is the current OMP step.
- MASTER 1 closure: `COMPLETE`; RT2 canonicalization is closed inside existing owners, OMP can self-drive RT2 after prerequisites, MASTER 2 is not started, and the next implementation milestone remains A5.
- Related reports: `docs/reports/engineering/2026-06-28_130037_rt2_integration_discovery_audit.md`, `docs/reports/engineering/2026-06-28_112236_rt_phase2_final_program_refinement.md`, `docs/reports/engineering/2026-06-28_104454_rt_phase2_architecture_stress_test.md`.

## 30. Architecture Graduation & Product Transition / Master 4

- Verdict: `MASTER_4_COMPLETE`.
- What it means: Architecture Mode is complete. V7 is now in Product Execution Mode. Architecture is closed by default and future work must enter through OMP.
- Architecture Constitution: Architecture preserves Reality, Safety, Authority, Certification, Verification, Knowledge, and Evolution. Architecture does not own backlog execution, runtime mutations, deployments, user movement, engineering tasks, production operations, or engineering history.
- Change protocol: Idea -> Existing Owner Check -> Reuse / Extend Existing Owner -> OMP -> Implementation if approved -> Verification -> Engineering Report -> Canonical Update -> Current Program State -> Continue OMP. Architecture proposal is allowed only after existing architecture cannot express the capability.
- Capability admission rule: every future capability must answer why an existing owner cannot express it. Without a proven answer, new owner, new roadmap, new Runtime, new Planner, new Truth Source, new Master Program, and new Capability Program are forbidden.
- Knowledge preservation: durable conclusions cannot remain only in reports, audits, research, chats, implementation notes, or handoff notes. Every durable conclusion must have exactly one canonical owner.
- Product Execution Contract: OMP -> Implementation Backlog or existing owner -> Verification -> Engineering Report -> Canonical Update -> Current Program State -> Continue OMP. No parallel workflow is allowed.
- Program navigation: no `ARCHITECTURAL_INVARIANTS.md` or `PROGRAM_MAP.md` file is created because OMP, SYSTEM_MAP, Canonical Reference, Current Program State, Kernel, Runtime Model, Decision Model, and Document Lifecycle already express those roles.
- Next implementation milestone remains `A5_CERTIFY_CLASS_LEVEL_BLAST_RADIUS_EVIDENCE_BEYOND_ONE_USER_GUARD`. MASTER 4 does not begin A5.
- MASTER 4 Engineering Review: `ARCHITECTURE_GRADUATION_CONFIRMED`. Capability injection, future engineer navigation, Product Execution Mode, Constitution, Capability Admission, and Knowledge Preservation are confirmed through existing owners. No MASTER 5, new architecture phase, new roadmap, new owner, Runtime implementation, automation, authority expansion, or A5 start is created.
- Capability Lifecycle Certification: `CAPABILITY_LIFECYCLE_CERTIFIED`. Runtime Time Intelligence proves that a post-graduation capability can move through Idea -> OMP -> Implementation Backlog or existing owner -> Implementation if approved -> Verification/Certification -> Engineering Report -> Canonical Update -> Current Program State -> Continue OMP without new architecture, owner, roadmap, capability program, Runtime implementation, or A5 start.
- Engineering Intelligence Materialization Phase 1: `ENGINEERING_INTELLIGENCE_PHASE1_COMPLETE`. Engineering Intelligence is materially represented through existing owners: Runtime Model owns the contract and process/time semantics, OMP owns lifecycle and recommendation progression, Production Maturity owns maturity view, SYSTEM_MAP owns owner lookup, CPS owns volatile visibility, and Engineering Reports preserve evidence. No new Runtime, Planner, Owner, Truth Source, roadmap, master program, capability program, Runtime implementation, automation, authority expansion, or A5 change is created.
- Engineering Intelligence Materialization Phase 2: `ENGINEERING_INTELLIGENCE_PHASE2_COMPLETE`. The Engineering Validation Loop is permanently materialized through existing owners: Runtime Model owns Prediction, Validation, and Confidence contracts; OMP owns Engineering Validation and Recommendation Validation lifecycles; Production Maturity owns validation maturity; SYSTEM_MAP owns validation ownership; CPS owns current validation maturity. Recommendation -> Outcome -> Prediction vs Reality -> Difference -> Confidence Update -> Recommendation Evolution is canonical, advisory, and non-authorizing until separate OMP implementation/certification. No Runtime implementation, A5 change, new owner, new roadmap, new truth source, or new capability program is created.
- Engineering Intelligence Materialization Phase 3: `ENGINEERING_INTELLIGENCE_PHASE3_COMPLETE`. Adaptive Engineering is permanently materialized through existing owners: Runtime Model owns Adaptive Engineering, Recommendation Evolution, and Engineering Learning contracts; OMP owns Adaptive Engineering and Recommendation Evolution lifecycles; Production Maturity owns Adaptive Engineering Maturity; SYSTEM_MAP owns Adaptive Engineering ownership; CPS owns current adaptive maturity. Recommendation -> Implementation -> Outcome -> Prediction vs Reality -> Confidence Update -> Recommendation Improvement -> Future Recommendation -> Engineering Learning -> Future Engineering is canonical, OMP-governed, and non-authorizing. Runtime never self-improves; only Engineering Intelligence evolves. No Runtime implementation, Runtime adaptation, A5 change, new owner, new roadmap, new truth source, or new capability family is created.
- Continue OMP A5: `class_level_blast_radius_certification` exists in `admin_core.autonomy_trust_acceleration` as a read-only A5 verifier. It consumes existing E29 historical governed execution proofs for one-user, two-user, and four-user movement. A5 blast-radius evidence is `DONE_READ_ONLY`; this does not expand blast radius, authority, Runtime behavior, automation, planner behavior, or user movement. The next implementation item is A6 runtime eligibility arbitration.
- Continue OMP A6: `runtime_eligibility_arbitration` exists in `admin_core.autonomy_trust_acceleration` as a read-only execute-or-stop model. It consumes freshness, authority, blast radius, rollback/no-rollback, anti-flap, verification, learning, routing readiness, and runtime_apply gates. A6 is `DONE_READ_ONLY`; current result is `STOP_SAFE` at authority/runtime_apply. This does not enable Runtime apply, expand authority, move users, create a new Runtime, create a new owner, or create a new truth source. The next implementation item is B13 metric reliability verification.
- Continue OMP B13: `metric_reliability_certification` exists in `admin_core.autonomy_trust_acceleration` as a read-only verifier for automated promotion recommendation metrics. B13 is `DONE_READ_ONLY`; current result is `CERTIFIED_FOR_BLOCKING_RECOMMENDATIONS_ONLY` with recommendation `DO_NOT_PROMOTE_COLLECT_REAL_EVIDENCE`. Positive promotion remains blocked by partial service outcome, candidate outcome, confidence/trust/prediction floor, freshness, runtime_apply, and authority evidence. This does not enable Runtime apply, expand authority, move users, change formulas, lower floors, create evidence, create a new Runtime, create a new owner, or create a new truth source. The next implementation item is B16 rollback authority certification.
- Continue OMP B16: `rollback_authority_certification` exists in `admin_core.autonomy_trust_acceleration` as a read-only verifier for automatic rollback authority readiness. B16 is `DONE_READ_ONLY`; current result is `CERTIFIED_FOR_AUTHORITY_REVIEW_ONLY` with recommendation `DO_NOT_ENABLE_AUTOMATIC_ROLLBACK_AUTHORITY_WITHOUT_OPERATOR_APPROVAL`. Rollback/verification/metric/runtime evidence is ready for authority review only; automatic rollback authority is not granted, runtime apply remains disabled, rollback execution is not performed, authority/runtime_apply remain STOP gates, and no users move. The next OMP step is `RT2-S1` Measurement & Observability Foundation inside the existing Runtime Capability Maturation Program.
- Continue OMP RT2-S1: `rt2_s1_measurement_observability_foundation` exists in `admin_core.operator_execution_pipeline` as a read-only measurement foundation. RT2-S1 is `DONE_READ_ONLY`; runtime cost, runtime time, reaction latency, stop reasons, lifecycle, wait states, dependency topology, Time-To-Safe-Recovery, and bottlenecks are visible or owner-mapped as missing. Dashboard/read-model output cannot decide, approve, certify, mutate, create synthetic metrics, expand authority, or become a truth source. The next OMP step is `RT2-S2` World & Readiness Maturation.
- Continue OMP RT2-S2: `rt2_s2_world_readiness_maturation` exists in `admin_core.operator_decision_surface` as a read-only prepared world/readiness surface. RT2-S2 is `DONE_READ_ONLY`; compact user/channel state, snapshot statuses, freshness/readiness, candidate readiness, live policy gate ownership, knowledge readiness, and trust/learning are prepared from existing owners and can be consumed as READY/STOP context. Prepared state cannot approve, move users, create Desired State authority, replace planner, mutate Runtime, create synthetic evidence, or become a truth source. The next OMP step is `RT2-S3` Desired-State Delta Preparedness.
- Continue OMP RT2-S3: `rt2_s3_desired_state_delta_preparedness` exists in `admin_core.operator_decision_surface` as a read-only advisory desired-state delta/prepared-plan surface. RT2-S3 is `DONE_READ_ONLY`; deltas consume existing S2 readiness, decision surface, batch preview, planner/autoswitch recommendations, policy/review evidence, and live-gate semantics. Desired State remains advisory and non-authorizing; the prepared plan cannot approve movement, replace planner owners, mutate Runtime, create synthetic evidence, create authority, or move users.
- Continue OMP RT2-S4: `rt2_s4_governed_execution_coordination` exists in `admin_core.operator_execution_pipeline` as a read-only governed execution coordination surface. RT2-S4 is `DONE_READ_ONLY`; one bounded decision-to-terminal-outcome path is owner-mapped through packet, runtime recheck, restore barrier, apply, verification, rollback readiness, feedback, and closure owners. It does not execute apply, write restore barrier, move users, enable concurrency, create a queue, expand authority, create a new execution path, or change Runtime behavior. The next OMP step is `RT2-S5` Certified Concurrency Ladder.
- Continue OMP RT2-S5: `build_rt2_s5_certified_concurrency_ladder` exists in `admin_core.autonomy_trust_acceleration` as a read-only certified concurrency ladder. RT2-S5 is `DONE_READ_ONLY`; current certified level is `SERIAL_ONLY_READ_ONLY`, wider levels are explicit `STOP_SAFE`, and RT2-S6 is unlocked. This does not enable parallelism, runtime apply, automation, authority expansion, queue daemon, planner replacement, new owner, new truth source, or user movement.
- Continue OMP RT2-S6: `build_rt2_s6_evidence_based_continuous_improvement` exists in `admin_core.autonomy_trust_acceleration` as a read-only/advisory evidence-based improvement surface. RT2-S6 is `DONE_READ_ONLY`; it produced an owner-mapped recommendation to return OMP to existing backlog item `B1`. This does not enable Runtime self-optimization, automatic recommendations, direct implementation without OMP, runtime apply, automation, authority expansion, planner replacement, new owner, new truth source, or user movement.
