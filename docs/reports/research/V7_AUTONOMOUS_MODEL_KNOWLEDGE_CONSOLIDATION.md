# V7 Autonomous Model Knowledge Consolidation

Status: `KNOWLEDGE_CONSOLIDATION`
Mode: `ANALYSIS_ONLY`
Runtime impact: `NONE`
Authority impact: `NONE`
Production impact: `NONE`
Deployment: `NO`
Users moved: `NO`
Created: `2026-07-05`

## 1. Executive Summary

V7 already has the conceptual architecture of the ideal autonomous system. The model is not missing as design; it is distributed across canonical reference documents, OMP, Current Program State, Production Maturity, capability specifications, ADRs, engineering reports, and R1/R2/R3/R4 research.

The consolidated target is a governed autonomous production routing platform:

```text
Reality
  -> Observation
  -> Health Evidence
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
  -> OMP Mission / Continuation
  -> Engineering Automation
  -> Continuous Self Evolution
```

The main missing work is connection, inventory, and automation, not new architecture. The repeated weakness is that many concepts are defined correctly but live in multiple documents with different roles: canonical owner, volatile state, historical evidence, or research validation. The final ideal model can be drafted safely if it stays a map and does not replace OMP, Runtime, Planner, Authority, Controlled Production Certification, or Production Maturity.

Source:
- `docs/reference/V7_MASTER_PROJECT_HANDOFF.md` — Project Purpose, System Architecture, Major Owners.
- `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md` — Executive Summary, Final Autonomous Target, Fundamental Autonomy Laws.
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` — OMP as permanent production program.
- `docs/reference/SYSTEM_MAP.md` — Document Ownership Table and owner lookup.

## 2. Source Map

| Concept | Primary source file | Secondary source files | Status | Notes |
| --- | --- | --- | --- | --- |
| Full-system autonomy target | `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md` | `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`, R4 laws | `CANONICAL` | Already defines target map, autonomy levels, domains, gap model, and no-Codex dependency. |
| Execution program / navigator | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` | `docs/decisions/ADR-V7-OMP-PRODUCTION-PROGRAM.md`, `docs/reference/V7_MASTER_PROJECT_HANDOFF.md` | `CANONICAL` | OMP is the only long-term execution program. |
| Current volatile GPS | `docs/programs/V7_CURRENT_PROGRAM_STATE.md` | `docs/decisions/ADR-V7-KERNEL-AND-STATE-SPLIT.md`, `docs/reference/V7_MASTER_PROJECT_HANDOFF.md` | `CURRENT_STATE_ONLY` | Useful for active blocker/state; not durable truth. |
| Owner lookup | `docs/reference/SYSTEM_MAP.md` | `docs/reference/V7_CANONICAL_REFERENCE.md`, OMP | `CANONICAL` | Lookup only; not second truth source. |
| Runtime execution semantics | `docs/reference/V7_RUNTIME_MODEL.md` | `docs/reference/V7_AUTONOMOUS_RUNTIME_MODEL.md`, ADR-V7-RUNTIME-MODEL | `CANONICAL` | Runtime stays thin and consumes prepared/approved identity. |
| Autonomous runtime loop | `docs/reference/V7_AUTONOMOUS_RUNTIME_MODEL.md` | `docs/reference/V7_EXECUTION_MISSION_PROTOCOL.md`, L3 spec | `CANONICAL` | Orchestrates existing owners; does not grant authority. |
| Decision semantics | `docs/reference/V7_DECISION_MODEL.md` | ADR-V7-WORLD-CLASS-DECISION-MODEL, ADR-V7-ACTION-CLASS-AUTHORITY | `CANONICAL` | Decision is not execution; Runtime consumes decisions. |
| L3 emergency capability | `docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md` | Autonomous Runtime Model, Runtime Model, OMP | `CANONICAL` | Capability-specific contract for confirmed channel failure failover. |
| Controlled certification | `docs/reference/capabilities/CONTROLLED_PRODUCTION_CERTIFICATION_PROGRAM.md` | `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md`, OMP | `CANONICAL` | Proves batch ladder and controlled production evidence. |
| Production maturity | `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md` | Current Program State, OMP, certification reports | `CANONICAL_CONSUMER` | Consumes evidence and decides maturity impact; does not create capability. |
| Execution mission discipline | `docs/reference/V7_EXECUTION_MISSION_PROTOCOL.md` | `docs/reference/V7_EXECUTION_COMPLETION_PROTOCOL.md` | `CANONICAL` | Defines breakpoint continuation, object identity, success, impossibility. |
| Engineering automation | `docs/reference/V7_MASTER_PROJECT_HANDOFF.md` | Certification Program, engineering automation reports | `PARTIAL_CANONICAL` | Laws exist; current pipeline implementation remains incomplete. |
| Automation/workflow debt | `docs/reference/capabilities/CONTROLLED_PRODUCTION_CERTIFICATION_PROGRAM.md` | Master Handoff, R2/R3/R4 | `CANONICAL` | Manual actions/workflows must be classified. |
| Knowledge quality | `docs/decisions/ADR-V7-KNOWLEDGE-QUALITY-MODEL.md` | `docs/reference/V7_KNOWLEDGE_QUALITY_MODEL.md`, SYSTEM_MAP | `CANONICAL` | Autonomy-grade knowledge requires freshness, correctness, coverage, relevance, actionability. |
| External validation laws | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md` | R1/R2/R3 research KBs | `RESEARCH_ONLY` | Validates project model; should not directly mutate Runtime or Authority. |
| Architecture closure | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` | `docs/reports/engineering/2026-06-30_155940_canonical_integration.md` | `CANONICAL` | New architecture only after existing-owner failure proof. |

## 3. Consolidation Method

Sources were classified by owner role, not by recency alone.

Classification rules:

| Status | Meaning |
| --- | --- |
| `CANONICAL` | Durable rule owned by reference, OMP, policy, ADR, capability, or model document. |
| `RESEARCH_ONLY` | External or synthetic validation that may guide owner review but cannot authorize implementation. |
| `ENGINEERING_REPORT_EVIDENCE` | Historical proof of what happened, why, and with what test/deploy result. |
| `CURRENT_STATE_ONLY` | Volatile state for active continuation; useful but not durable design. |
| `PARTIAL` | Concept exists but lacks complete owner, implementation, inventory, or automation. |
| `CONFLICTING` | Sources disagree or use same term for different owner roles. |
| `SUPERSEDED` | Older report/doc value was replaced by later canonical owner or certification evidence. |

Contradictions were handled by owner hierarchy:

```text
Reality / production evidence
  -> canonical owner
  -> ADR / policy
  -> OMP / Current Program State for current state
  -> engineering report evidence
  -> research validation
```

Source:
- `docs/reference/SYSTEM_MAP.md` — Document Ownership Table.
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` — Kernel and State Split, Knowledge Preservation.
- `docs/reference/V7_MASTER_PROJECT_HANDOFF.md` — Canonical Knowledge, Engineering Reports.

## 4. Top-Level Autonomous System Model

### Consolidated Chain

| Transition | Why it exists | Owner/document | Status | What breaks if missing |
| --- | --- | --- | --- | --- |
| Reality -> Observation | Autonomy starts from real production state, not guesses. | Master Handoff; AOS; OMP Reality First. | `CANONICAL` | Synthetic/planner-only assumptions can move users incorrectly. |
| Observation -> Health Evidence | Raw state must become typed service/route/quality/source evidence. | SYSTEM_MAP Observation Plane; R1 health evidence. | `CANONICAL` | Failures become opaque and unverifiable. |
| Health Evidence -> Incident | A signal must be classified into a legal incident or no-action. | Autonomous Runtime Model incident lifecycle; L3 spec. | `CANONICAL` | Timers or noise can masquerade as execution permission. |
| Incident -> Diagnosis | The system must identify affected scope, owner, and exact condition. | Execution Mission Protocol; Engineering Operating System in Master Handoff. | `CANONICAL` | Investigations stop at blockers and never complete execution. |
| Diagnosis -> Decision Model | Diagnosed need must enter structured decision vocabulary before action selection. | Decision Model; L3 Planner Contract. | `CANONICAL` | Signals and diagnosis can become implicit action. |
| Decision Model -> Policy | Decision semantics must be constrained by product and operational boundaries. | POLICY_001/004/008; Decision Model. | `CANONICAL` | Technical possibility can masquerade as business permission. |
| Policy -> Planner | Policy boundaries must constrain what Planner may select. | Decision Model; Policy documents; L3 Planner Contract. | `CANONICAL` | Planner may emit impossible or unauthorized moves. |
| Planner -> Authority | Selected candidate must be admitted by approved class, scope, risk, and blast radius. | ADR-V7-ACTION-CLASS-AUTHORITY; Controlled Certification Program. | `CANONICAL` | Automation expands without earned scope. |
| Authority -> Identity | Approved selected move identity must be preserved before apply. | L3 Execution Contract; Master Handoff owners. | `CANONICAL` | Runtime can apply a different plan than Authority approved. |
| Identity -> Runtime | Runtime consumes committed identity and either allows live execution or stops. | Runtime Model; Autonomous Runtime Model. | `CANONICAL` | Runtime becomes a planner/truth source. |
| Runtime -> Execution | Execution is the actual mutation/no-mutation boundary. | Runtime Model; Decision Model Law 8. | `CANONICAL` | Apply success is mistaken for user restoration. |
| Execution -> Verification | Mutation is incomplete until proof exists. | Decision Model Law 8; Runtime Verification Contract. | `CANONICAL` | Apply success is mistaken for user restoration. |
| Verification -> Rollback / Closure | Failed verification must rollback, contain, or close no-rollback. | Policy 007; Runtime Model; Certification Program. | `CANONICAL` | Users remain in unverified state. |
| Rollback / Closure -> Learning | Terminal outcomes become durable feedback only after closure. | Autonomous Runtime Model Learning Loop; R4 Learning Laws. | `CANONICAL` | Trust grows from incomplete evidence. |
| Learning -> Production Maturity | Maturity consumes certified outcomes. | Production Maturity Model. | `CANONICAL_CONSUMER` | Maturity becomes opinion instead of evidence. |
| Production Maturity -> Current Program State | Current Program State exposes current bottleneck/next action. | Current Program State Behavior Contract. | `CANONICAL_CURRENT_STATE` | Operators lose current GPS position. |
| Current Program State -> OMP Mission / Continuation | OMP decides next work from current state and owners. | OMP Continue Loop. | `CANONICAL` | Work fragments into prompts/roadmaps. |
| OMP -> Engineering Automation | Repeated work becomes automation/workflow gap. | Master Handoff; Certification Program. | `CANONICAL_PARTIAL` | Human/Codex orchestration remains permanent. |
| Engineering Automation -> Continuous Self Evolution | Automation closes gaps and feeds next mission. | AOS Self-Improvement Model; R3. | `PARTIAL` | V7 can operate but not improve itself efficiently. |

Inference from:
- `docs/reference/V7_MASTER_PROJECT_HANDOFF.md` — Canonical production chain.
- `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md` — Universal lifecycle and autonomy domains.
- `docs/reference/V7_AUTONOMOUS_RUNTIME_MODEL.md` — control loop and state machine.
- `docs/reference/capabilities/CONTROLLED_PRODUCTION_CERTIFICATION_PROGRAM.md` — Capability Producers and Consumers.

## 5. Autonomous Routing Model

The routing model is incident-scoped, service-aware, authority-bounded, identity-preserving, and verification-closed.

Durable routing concepts:

| Concept | Consolidated meaning | Source status | Role in ideal model |
| --- | --- | --- | --- |
| Source/target health | Health is matrix evidence across route, service, quality, load, freshness, and policy. | `CANONICAL` + `RESEARCH_ONLY` support | Determines eligible current failure and safe target. |
| Required services | L3 is legal only when affected user's required service context is proven failed or current channel failed under policy. | `CANONICAL` | Prevents generic ineligible-current moves from becoming emergency failover. |
| Incident source | Failed source identity survives across bounded cycles until source recovers, no affected users remain, containment, or impossibility. | `CANONICAL` in Certification Program and Master Handoff | Keeps continuation from switching to unrelated users/sources. |
| Candidate selection | Planner selects eligible remaining users on incident source and excludes exhausted semantic attempts. | `ENGINEERING_REPORT_EVIDENCE` + canonical owner mapping | Prevents repeated failed user attempt from blocking evacuation. |
| Selected move identity | User/source/target/action/hash/generation must match through lock, barrier, runtime, verification, rollback. | `CANONICAL` | Prevents Authority-approved object mutation. |
| Authority budget | Current max users per governed cycle; ladder is 1/5/10/25/50/FULL_INCIDENT. | `CANONICAL` | Scales blast radius only after evidence. |
| Verification | Every moved user must be verified against route and required services. | `CANONICAL` | Proves restoration instead of merely assignment. |
| Rollback/no-rollback | Failed verification closes by rollback, containment, or certified no-rollback. | `CANONICAL` | Prevents dangling failed movement. |
| Learning | Terminal outcomes update trust, prediction, recommendation, and future evidence. | `CANONICAL_PARTIAL` | Enables evidence-based promotion/demotion. |

Source:
- `docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md` — Entry Conditions, Planner Contract, Execution Contract.
- `docs/reference/capabilities/CONTROLLED_PRODUCTION_CERTIFICATION_PROGRAM.md` — Incident Source, Authority Budget, Batch Ladder.
- `docs/reference/V7_DECISION_MODEL.md` — Decision Output Shape, Universal Laws.
- `docs/reports/research/2026-07-05_150942_v7_large_scale_autonomous_routing_reliability_research.md` — routing/reliability patterns.

## 6. Autonomous Operations Model

V7 operations are governed incident operations, not free-running background automation.

The operational model:

```text
real signal
  -> legal wake
  -> incident
  -> severity/scope/authority
  -> governed action or HOLD/STOP_SAFE
  -> verification and rollback/no-rollback
  -> learning and maturity consumption
```

Operational maturity is split from engineering maturity. Engineering can be complete while production autonomy remains unearned. Production freeze/HOLD is a valid safety state, but HOLD is not a terminal explanation until Owner Resolution classifies why the owner blocked.

SLO/error-budget thinking exists in research and maturity concepts, but V7 does not yet have a fully canonical product SLO set that can feed Authority directly. The current safe interpretation is: SLO/error budget may inform OMP, Authority, and Production Maturity, but cannot bypass Runtime gates.

Source:
- `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md` — Separation Rule and Production Maturity categories.
- `docs/reports/research/V7_AUTONOMOUS_OPERATIONS_RESEARCH.md` — SLO/Error Budget Governance, Operations Principles.
- `docs/reference/capabilities/CONTROLLED_PRODUCTION_CERTIFICATION_PROGRAM.md` — Recovery, HOLD, controlled production environment.
- `docs/reference/V7_AUTONOMOUS_RUNTIME_MODEL.md` — Incident Lifecycle, Circuit Breaker, Suspension.

## 7. Autonomous Engineering Model

V7 engineering autonomy is an owner-mapped self-improvement system.

Codex is currently a temporary assistant that performs discovery, implementation, test, report, safe deploy orchestration, and continuation under project rules. In the ideal model, routine Codex/manual orchestration becomes scripted, pipelined, or governed automation. Codex remains optional for exceptional engineering, policy, architecture, and impossibility reasoning.

Engineering model:

```text
Breakpoint / repeated workflow
  -> Owner Resolution
  -> existing-owner implementation if needed
  -> tests / regression
  -> safe deploy / convergence when applicable
  -> Engineering Report
  -> canonical sync when durable
  -> Current Program State update when volatile
  -> OMP continuation
  -> Automation / Workflow Audit
```

The strongest partial gap is not conceptual. It is pipeline materialization: certification preparation, Authority readiness polling, evidence collection, report/history/passport projection, and debt metric projection still appear as repeated manual workflows in reports.

Source:
- `docs/reference/V7_MASTER_PROJECT_HANDOFF.md` — Engineering Program, Automation Evolution, Workflow Evolution.
- `docs/reference/capabilities/CONTROLLED_PRODUCTION_CERTIFICATION_PROGRAM.md` — Automation Audit Loop, Workflow Audit Loop, Pipeline Candidate Contract.
- `docs/reports/engineering/2026-07-03_172908_engineering_automation_activation.md` — active engineering automation targets.
- `docs/reports/research/V7_AUTONOMOUS_ENGINEERING_SYSTEMS_RESEARCH.md` — autonomous engineering systems validation.

## 8. Knowledge And Truth Model

Knowledge in V7 is layered:

| Layer | Role | Must not do |
| --- | --- | --- |
| Reality / production runtime | Final observed state and verification evidence. | Become undocumented or synthetic. |
| Canonical reference / ADR / policies | Durable rules and decisions. | Hold volatile packet/current state. |
| SYSTEM_MAP | Owner/topology lookup. | Become a second truth source. |
| OMP | Execution program and continuation engine. | Become packet dump or parallel backlog. |
| Current Program State | Volatile current state/GPS. | Grant authority or durable truth. |
| Production Maturity | Evidence consumer and maturity decision owner. | Create capability or authority. |
| Engineering Reports | Historical evidence and proof. | Become roadmap, owner, or authority. |
| Research KBs | External validation and candidate laws. | Mutate implementation directly. |

Durable knowledge must have exactly one canonical owner. A report may prove a durable conclusion, but the conclusion remains historical until promoted. Current Program State may show current reality, but it is allowed to become stale and must not be used as the final design owner.

Source:
- `docs/reference/SYSTEM_MAP.md` — Document Ownership Table.
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` — Knowledge Preservation Contract.
- `docs/reference/V7_MASTER_PROJECT_HANDOFF.md` — Canonical Knowledge.
- `docs/decisions/ADR-V7-KNOWLEDGE-QUALITY-MODEL.md` — knowledge quality dimensions.

## 9. OMP As Execution Engine

OMP is the system navigator. It converts target/current gaps into missions and routes them through existing owners.

OMP owns:

- current work placement;
- continuation;
- owner mapping;
- no-duplicate discipline;
- capability admission;
- maturity/evidence consumption flow;
- authority evolution recommendation, not authority self-grant;
- architecture closed-by-default.

OMP should later consume the ideal autonomous model as a target map:

```text
Ideal model
  -> Current Program State autonomy inventory
  -> Autonomy Gap
  -> OMP mission
  -> existing owner
  -> evidence / certification / policy / impossibility
```

OMP must not become Runtime, Planner, Authority, or a new production daemon.

Source:
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` — Continue OMP Engineering Control Loop, Master OMP Completeness Certification.
- `docs/decisions/ADR-V7-OMP-PRODUCTION-PROGRAM.md` — OMP as permanent production program.
- `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md` — OMP Relationship and Autonomy Mission Model.

## 10. Current Program State As GPS

Current Program State is a volatile navigation surface. It records the current blocker, current phase, current authority class, current metrics, and next safe action. It is not a canonical source of durable design and not execution authority.

The consolidation found a useful ambiguity: Current Program State currently contains snapshots that may lag later Master Handoff/certification reports. This is allowed only if Current Program State is treated as GPS, not law. The future Phase 2 autonomy inventory should live in Current Program State, but each field must point to canonical owners and evidence.

Source:
- `docs/programs/V7_CURRENT_PROGRAM_STATE.md` — Behavior Contract and current state fields.
- `docs/decisions/ADR-V7-KERNEL-AND-STATE-SPLIT.md` — OMP/Current Program State split.
- `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md` — Current Program State Relationship.

## 11. Production Maturity As Consumer

Production Maturity consumes evidence after capability producers complete. It produces maturity decisions: `ACCEPT`, `PARTIAL_ACCEPT`, `BLOCK`, `NO_CHANGE`, or `INVALID_EVIDENCE`.

It should not approve Runtime Apply, expand Authority, enable automation, move users, change routing, or create evidence. Its role in the ideal model is to make production readiness visible and to block maturity claims that lack evidence.

Engineering Maturity is already complete. Production Maturity is not. That distinction is central: V7 understands the target architecture but still needs production evidence, automation pipelines, and authority/certification completion to become fully autonomous.

Source:
- `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md` — Purpose, Separation Rule, Product Evolution Behavior Contract.
- `docs/reference/capabilities/CONTROLLED_PRODUCTION_CERTIFICATION_PROGRAM.md` — Capability Consumers.

## 12. Human Boundary

Humans own policy, business risk, exceptional approval, architecture boundary decisions, and canonical impossibility acceptance. Humans should not own routine monitoring, routine incident diagnosis, normal certified failover, repeated evidence readback, routine report/state synchronization, or repeated engineering workflows.

Codex currently bridges many routine workflows. The final system must not depend on Codex for routine operation. Codex can remain a temporary engineering accelerator and exceptional reasoning assistant, not a production dependency.

Source:
- `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md` — Human Boundary and No Codex Dependency Law.
- `docs/reference/V7_MASTER_PROJECT_HANDOFF.md` — Automation Evolution, Workflow Evolution, Engineering Automation Vision.
- `docs/reports/research/V7_AUTONOMOUS_OPERATIONS_RESEARCH.md` — Human Boundary Models.
- `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md` — H1/H2 Human Boundary laws.

## 13. External Research Alignment

| V7 concept | Project source | R1/R2/R3/R4 supporting law | Alignment | Gap or caution |
| --- | --- | --- | --- | --- |
| Reality before authority | Master Handoff; AOS | R4 `Reality Precedes Authority` | Strong | Must stay true during controlled certification evidence generation. |
| Health matrix | L3 spec; SYSTEM_MAP service matrix | R1/R4 `Health Is A Matrix, Not A Boolean` | Strong | Need stable schema owner for cross-owner evidence matrix. |
| Decision not execution | Decision Model; Runtime Model | R4 `Decision Is Not Execution` | Strong | Runtime must never recompute committed selected move. |
| Progressive ladder | Certification Program | R1/R2 progressive rollout/canary patterns | Strong | Full incident still requires Authority proof. |
| Rollback closure | Runtime Model; Certification Program | R4 `Rollback Or Closure Is Mandatory` | Strong | Partial success semantics should remain explicit in batch stages. |
| Automation debt | Certification Program; Master Handoff | R2/R3/R4 automation/workflow laws | Strong | Debt projection pipeline remains partial. |
| SLO/error budget | Production Maturity; R2 | R2 operations research | Partial | V7-specific SLOs are not yet canonical enough for Authority input. |
| Analyzer/backtesting | OMP Engineering Intelligence; R3 | R3/R4 analyzer backtesting | Partial | Advisory first; blocking analyzers require certification. |
| Human boundary | AOS; Master Handoff | R2/R4 human boundary laws | Strong | Routine Codex dependency still exists in engineering workflows. |
| Knowledge owner discipline | SYSTEM_MAP; OMP | R4 `Durable Truth Has One Owner` | Strong | Some durable conclusions remain report-only until promoted. |

## 14. Duplicate / Overlap Review

Duplicate/overlap count: `9`.

| Duplication | Files involved | Harmless? | Canonical owner | Treatment |
| --- | --- | --- | --- | --- |
| Full autonomous target vs project handoff chain | AOS, Master Handoff | Mostly harmless | AOS for target, Master Handoff for entry/current context | Keep both; cross-reference. |
| OMP execution rules repeated in Master Handoff | OMP, Master Handoff | Harmless if handoff is entry point | OMP | Handoff should summarize, not redefine. |
| Runtime loop in Runtime Model, Autonomous Runtime, L3 | Runtime Model, Autonomous Runtime, L3 spec | Necessary specialization | Runtime Model / Autonomous Runtime / L3 by scope | Treat as layered, not duplicate. |
| Capability producers/consumers | Certification Program, Master Handoff, AOS | Harmless | Certification Program for certification; AOS for target | Keep owner-specific scope. |
| Automation/workflow debt | Certification Program, Master Handoff, R2/R3/R4 | Harmless but verbose | Certification Program / OMP | Research validates only. |
| Knowledge preservation | OMP, SYSTEM_MAP, Master Handoff | Harmless | OMP + Canonical Reference; SYSTEM_MAP lookup | Avoid treating SYSTEM_MAP as truth. |
| Production maturity and Current Program State state | Production Maturity Model, Current Program State, Master Handoff | Risky when stale | Production Maturity for maturity; Current Program State for current state | Current Program State must remain volatile. |
| Authority ladder and action-class authority | Certification Program, ADR Action-Class Authority, reports | Mostly harmless | ADR for authority model; Certification Program for ladder | Reports historical only. |
| Engineering automation program | Master Handoff, Certification Program, engineering reports | Partial duplicate | Master Handoff / Certification Program | Needs concrete pipeline ownership later. |

## 15. Conflicts / Ambiguities

Conflict count: `6`.

| Conflict / ambiguity | Files involved | Why it matters | Recommended resolution path |
| --- | --- | --- | --- |
| Current Program State snapshot can lag Master Handoff certification state. | Current Program State, Master Handoff | Future agent may follow stale phase/blocker. | Treat Current Program State as volatile; add timestamp freshness and source lineage in future inventory. |
| `Autonomous Operating System` is a target map but name sounds executable. | AOS, OMP | Could be mistaken for Runtime/OMP replacement. | Keep explicit "map, not engine" language in future ideal model. |
| Engineering reports contain durable laws before promotion. | Reports, OMP, SYSTEM_MAP | Durable knowledge can stay trapped in history. | OMP knowledge preservation must promote only durable conclusions. |
| SLO/error budget is researched but not fully canonical. | R2/R1, Production Maturity | Could be overused as Authority input. | Classify as `NEEDS_CANONICAL_SYNC` before runtime/authority use. |
| Certification Passport/Coverage Matrix are views, not owners. | Certification Program, Production Maturity, Current Program State | Risk of new truth source. | Preserve as consumer projection only. |
| Engineering automation is active but pipelines are partial. | Master Handoff, engineering automation reports | Repeated manual workflows continue despite canonical laws. | Phase 2 inventory should capture pipeline candidates and owner status. |

No conflict currently proves a need for a new Runtime, Planner, Authority, OMP, truth source, or architecture.

## 16. Missing Or Weakly Defined Concepts

| Missing / weak concept | Why required | Nearest owner | Classification |
| --- | --- | --- | --- |
| Autonomy Inventory schema in Current Program State | AOS expects Current Program State to expose domain/current level/target/blocker/owner/evidence/debt. | Current Program State / OMP | `NEEDS_PHASE_2_INVENTORY` |
| Source-to-owner health evidence matrix | Health matrix exists but cross-owner schema is spread across service matrix, route, quality, runtime. | Observation Plane / SYSTEM_MAP | `NEEDS_OWNER_MAPPING` |
| SLO/error-budget canonical V7 vocabulary | Research supports it; Production Maturity can consume it; Authority needs exact semantics before use. | Production Maturity / Authority / OMP | `NEEDS_CANONICAL_SYNC` |
| Automation Debt metric projection | Laws exist; projection pipeline remains partial. | OMP / Production Maturity / Current Program State | `NEEDS_IMPLEMENTATION_LATER` |
| Workflow/Pipeline Candidate registry projection | Workflow debt exists but single current view is weak. | OMP / Current Program State / Engineering Reports | `NEEDS_PHASE_2_INVENTORY` |
| Analyzer backtesting certification levels | R3/R4 support analyzer laws, but blocking/advisory thresholds remain unclear. | OMP / Engineering Intelligence | `NEEDS_CANONICAL_SYNC` |
| Controlled certification infrastructure inventory | Certification pool sufficiency exists; operational inventory view should be explicit. | Certification Program / Current Program State | `NEEDS_PHASE_2_INVENTORY` |
| Consumer synchronization debt status | Defined in Certification Program; current global view is weak. | OMP / Production Maturity / Current Program State | `NEEDS_PHASE_2_INVENTORY` |

This is a gap register seed, not a backlog.

## 17. Candidate Structure For Ideal Model

Future file candidate:

```text
docs/reference/V7_IDEAL_AUTONOMOUS_SYSTEM_MODEL.md
```

Recommended structure:

1. Purpose and non-goals.
2. Source hierarchy and owner hierarchy.
3. Top-level autonomous chain.
4. Capability producer/consumer model.
5. Routing autonomy model.
6. Operations autonomy model.
7. Runtime autonomy model.
8. Engineering autonomy model.
9. Knowledge/truth model.
10. OMP/Current Program State/Production Maturity relationship.
11. Authority and human boundary.
12. Automation/workflow/self-improvement model.
13. Autonomy inventory contract.
14. Evidence/certification/maturity contract.
15. Missing inventory fields for Phase 2.
16. Forbidden duplicates and non-goals.
17. Open questions requiring human owner review.

Do not include current phase details, active blockers, packet identities, deployment hashes, or certification history rows. Those belong to Current Program State, Engineering Reports, Certification History, or Master Handoff.

## 18. What Should Not Be Included In The Ideal Model

| Material | Should remain in | Reason |
| --- | --- | --- |
| Current production phase/blocker | Current Program State / Master Handoff | Volatile. |
| OMP mission sequencing | OMP | Execution program, not target model. |
| Production maturity score | Production Maturity Model / Current Program State | Consumer state. |
| Exact runtime gates and state machine details | Runtime Model / Autonomous Runtime Model | Runtime owner already exists. |
| L3 capability-specific entry/exit rules | L3 capability spec | Capability-specific. |
| Controlled certification ladder procedures | Certification Program | Specialized certification owner. |
| Historical proof and raw artifacts | Engineering Reports | Evidence history. |
| External organization research detail | R1/R2/R3/R4 KBs | Validation, not canonical implementation. |
| Owner lookup tables | SYSTEM_MAP | Lookup owner. |
| ADR decision rationale | ADRs | Decision history. |

## 19. Final Consolidated Interpretation

V7's ideal autonomous system is a governed, evidence-bounded production routing control plane plus a self-improving engineering control system.

It does not become autonomous by running a timer, making Planner more aggressive, or letting Runtime decide. It becomes autonomous when real production evidence enters legal wake/incident paths, Planner selects safe candidates, Authority admits only earned scope, Approved Plan Lock and Restore Barrier preserve identity, Runtime applies exactly the approved object, Verification proves the user/service outcome, Rollback/no-rollback closes failure or success, Learning records terminal reality, Production Maturity consumes evidence, Current Program State exposes current state, and OMP converts the next gap into the next owner-mapped mission.

The same shape governs engineering work. A repeated manual action becomes Automation Debt. A repeated manual workflow becomes Workflow Debt. Both must be classified and, where justified, converted into owner-bounded automation or governed pipelines. The final system reduces routine human/Codex work without replacing human policy authority, business judgement, exceptional approval, or architecture boundary ownership.

The ideal model is therefore already present. It needs consolidation, inventory, and pipeline materialization more than invention.

Source:
- `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md` — final target and autonomy laws.
- `docs/reference/V7_MASTER_PROJECT_HANDOFF.md` — current architecture and operating entry point.
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` — execution engine.
- `docs/reference/capabilities/CONTROLLED_PRODUCTION_CERTIFICATION_PROGRAM.md` — certification and automation/workflow evolution.
- `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md` — organization-independent laws.

## 20. Final Engineering Verdict

Does V7 already have the conceptual architecture?

```text
YES
```

The architecture exists as a distributed but coherent model.

Is the main missing work connection/automation/inventory?

```text
YES
```

Primary missing work:

- Autonomy Inventory in Current Program State.
- One consolidated ideal-system model doc.
- Pipeline materialization for repeated certification/engineering workflows.
- SLO/error-budget canonical vocabulary.
- Analyzer/backtesting certification thresholds.
- Consumer synchronization/debt projection views.

Are there genuinely missing design areas?

```text
NO FUNDAMENTAL ARCHITECTURE GAP FOUND
```

There are weak definitions and partial projections, but no evidence that V7 needs a new Runtime, Planner, Authority, OMP, truth source, execution path, or architecture.

Is it safe to proceed to drafting the ideal model?

```text
YES
```

Recommended next step:

```text
DRAFT_V7_IDEAL_AUTONOMOUS_SYSTEM_MODEL
```

Human owner review before drafting:

1. Confirm whether the ideal model should be a new canonical reference file or an extension of `V7_AUTONOMOUS_OPERATING_SYSTEM.md`.
2. Confirm that Current Program State is the future Autonomy Inventory owner.
3. Confirm whether SLO/error-budget vocabulary should be included now as `PARTIAL` or deferred.
4. Confirm that Engineering Automation and Workflow Evolution remain intrinsic to certification and not a separate program.
5. Confirm that no current production phase details should enter the ideal model.

Files inspected: `35`.

Inspected source set:

- `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`
- `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
- `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md`
- `docs/reference/V7_AUTONOMOUS_RUNTIME_MODEL.md`
- `docs/reference/V7_RUNTIME_MODEL.md`
- `docs/reference/V7_DECISION_MODEL.md`
- `docs/reference/V7_EXECUTION_MISSION_PROTOCOL.md`
- `docs/reference/V7_EXECUTION_COMPLETION_PROTOCOL.md`
- `docs/reference/capabilities/CONTROLLED_PRODUCTION_CERTIFICATION_PROGRAM.md`
- `docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md`
- `docs/reports/research/2026-07-05_150942_v7_large_scale_autonomous_routing_reliability_research.md`
- `docs/reports/research/V7_AUTONOMOUS_OPERATIONS_RESEARCH.md`
- `docs/reports/research/V7_AUTONOMOUS_ENGINEERING_SYSTEMS_RESEARCH.md`
- `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`
- `docs/decisions/ADR-V7-ACTION-CLASS-AUTHORITY.md`
- `docs/decisions/ADR-V7-KERNEL-AND-STATE-SPLIT.md`
- `docs/decisions/ADR-V7-RUNTIME-MODEL.md`
- `docs/decisions/ADR-EVENT-DRIVEN-AUTONOMY.md`
- `docs/decisions/ADR-V7-FRESHNESS-ACTIONABILITY.md`
- `docs/decisions/ADR-V7-IDEAL-AUTONOMOUS-ROUTING-MODEL.md`
- `docs/decisions/ADR-V7-SAFETY-BOUNDED-AUTHORITY.md`
- `docs/decisions/ADR-V7-WORLD-CLASS-DECISION-MODEL.md`
- `docs/decisions/ADR-V7-OMP-PRODUCTION-PROGRAM.md`
- `docs/decisions/ADR-V7-KNOWLEDGE-QUALITY-MODEL.md`
- `docs/reports/engineering/2026-07-02_083525_observation_l3_wake_bridge_implementation.md`
- `docs/reports/engineering/2026-07-02_233929_controlled_production_certification_program_execution.md`
- `docs/reports/engineering/2026-07-03_172908_engineering_automation_activation.md`
- `docs/reports/engineering/2026-07-03_084803_owner_resolution_law.md`
- `docs/reports/engineering/2026-07-03_124419_committed_l3_apply_emergency_scope_fix.md`
- `docs/reports/engineering/2026-07-01_232858_execution_mission_success_l3_one_user_restored.md`
- `docs/reports/engineering/2026-06-30_200442_l3_execution_closure_verification.md`
- `docs/reports/engineering/2026-06-30_155940_canonical_integration.md`

Files changed by this mission:

```text
docs/reports/research/V7_AUTONOMOUS_MODEL_KNOWLEDGE_CONSOLIDATION.md
```

Confirmed:

```text
NO runtime changes
NO Planner changes
NO Authority changes
NO Production changes
NO deployment
NO canonical docs changed
```

## Phase 1 Step 1 — Knowledge Collection

### 1. Step Purpose

Collect and index existing V7 knowledge needed for a future ideal autonomous system model.

This step is collection only. It does not synthesize the final model, create `V7_IDEAL_AUTONOMOUS_SYSTEM_MODEL.md`, create Phase 2 inventory, create OMP missions, or modify canonical owners.

### 2. Files Inspected

Files inspected or explicitly indexed in Step 1: `74`.

Relevant sources found: `63`.

Inspection scope:

- `docs/reference/`
- `docs/reference/capabilities/`
- `docs/programs/`
- `docs/decisions/`
- `docs/policies/`
- `docs/product/`
- `docs/reports/engineering/`
- `docs/reports/research/`
- selected historical `docs/reports/` autonomy evidence reports
- selected phase/capacity/operator-action docs where they expose source concepts

Search result warning: broad search returned many screenshots, raw evidence files, old phase reports, productization evidence files, and duplicated path hits. These were not all promoted to the source index because Step 1 needs durable knowledge sources, not every matching artifact.

### 3. Knowledge Source Index

| Path | Title | Classification | Why relevant | Concepts covered | Durable truth? | Evidence only? | Current state only? | Use in Step 2? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `docs/product/V7_PRODUCT_SPECIFICATION.md` | V7 Product Specification | `CANONICAL` | Product/business intent anchor. | Business Objective, User Access Guarantee, human/operator boundary. | YES | NO | NO | YES |
| `docs/reference/V7_MASTER_PROJECT_HANDOFF.md` | V7 Master Project Handoff | `CANONICAL` | Entry point and current operating summary. | Full chain, Capability Earned, automation/workflow, owner landscape. | PARTIAL | PARTIAL | PARTIAL | YES |
| `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md` | V7 Autonomous Operating System | `CANONICAL` | Current full-system target map. | Autonomy levels, gaps, domains, human boundary, Codex exit. | YES | NO | NO | YES |
| `docs/reference/V7_SYSTEM_ARCHITECTURE.md` | V7 System Architecture | `CANONICAL` | Final architecture and component relationships. | OMP, Current Program State, Runtime, Planner, Knowledge, Learning, Truth, Evidence. | YES | NO | NO | YES |
| `docs/reference/V7_CANONICAL_REFERENCE.md` | V7 Canonical Reference | `CANONICAL` | Durable project truth aggregator. | Canonical sync, architecture graduation, implementation state. | YES | PARTIAL | NO | YES |
| `docs/reference/SYSTEM_MAP.md` | V7 System Map | `REFERENCE_INDEX` | Owner/topology lookup. | Owners, document classes, planes, behavior propagation. | LOOKUP_ONLY | NO | NO | YES |
| `docs/reference/V7_RUNTIME_MODEL.md` | V7 Runtime Model | `CANONICAL` | Runtime execution semantics. | Runtime and Execution, identity, verification, rollback, thin runtime. | YES | NO | NO | YES |
| `docs/reference/V7_AUTONOMOUS_RUNTIME_MODEL.md` | V7 Autonomous Runtime Model | `CANONICAL` | Autonomous runtime loop over existing owners. | Wake, incident lifecycle, readiness, budgets, circuit breaker. | YES | NO | NO | YES |
| `docs/reference/V7_AUTONOMOUS_EXECUTION_PROGRAM.md` | V7 Autonomous Execution Program | `CANONICAL` | Permission model for autonomous execution. | L3-L7 ladder, autonomy execution boundary. | YES | NO | NO | YES |
| `docs/reference/V7_DECISION_MODEL.md` | V7 Decision Model | `CANONICAL` | Decision vocabulary and decision/execution separation. | Planner, authority gate, verification, rollback, learning. | YES | NO | NO | YES |
| `docs/reference/V7_IDEAL_AUTONOMOUS_ROUTING_MODEL.md` | V7 Ideal Autonomous Routing Model | `PARTIAL` / `SUPERSEDED` | Routing target knowledge with superseded execution path. | Routing autonomy, observation, evidence, operator asks, routing knowledge. | PARTIAL | NO | NO | YES_WITH_CAUTION |
| `docs/reference/V7_KNOWLEDGE_QUALITY_MODEL.md` | V7 Knowledge Quality Model | `CANONICAL` | Autonomy-grade knowledge criteria. | Knowledge Quality, freshness, correctness, actionability. | YES | NO | NO | YES |
| `docs/reference/V7_CONTEXT_RESOLVER.md` | V7 Context Resolver | `CANONICAL` | Context loading and ECR discipline. | Owner mapping, knowledge consumption, OMP continuation. | YES | NO | NO | YES |
| `docs/reference/V7_DOCUMENT_LIFECYCLE.md` | V7 Document Lifecycle | `CANONICAL` | Document roles and promotion rules. | Canonical Sync, report/canonical boundaries. | YES | NO | NO | YES |
| `docs/reference/V7_ENGINEERING_PRINCIPLES.md` | V7 Engineering Principles | `CANONICAL` | Engineering behavior rules. | Reality First, reuse, verification, no duplicate owners. | YES | NO | NO | YES |
| `docs/reference/V7_EXECUTION_MISSION_PROTOCOL.md` | V7 Execution Mission Protocol | `CANONICAL` | Completion-first execution investigation. | Completion First, breakpoints, identity, canonical impossibility. | YES | NO | NO | YES |
| `docs/reference/V7_EXECUTION_COMPLETION_PROTOCOL.md` | V7 Execution Completion Protocol | `CANONICAL` | Breakpoint/continuation law. | Execution continuity, stop conditions, mission completion. | YES | NO | NO | YES |
| `docs/reference/V7_KERNEL.md` | V7 Kernel | `CANONICAL` | Permanent Codex operating contract. | Reality First, no duplication, owner boundaries. | YES | NO | NO | YES |
| `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md` | V7 Production Maturity Model | `CANONICAL` | Maturity consumer model. | Production Maturity, evidence consumption, engineering vs production maturity. | YES | NO | NO | YES |
| `docs/reference/V7_RESEARCH_PROCESS.md` | V7 Research Process | `CANONICAL` | Research-to-owner flow. | External validation, research classification. | YES | NO | NO | YES |
| `docs/reference/V7_AUTONOMY_BLUEPRINT.md` | V7 Autonomy Blueprint | `SUPERSEDED` / `PARTIAL` | Historical autonomy inventory and gap map. | Autonomy inventory, dormant systems, gaps. | NO | PARTIAL | PARTIAL | YES_WITH_CAUTION |
| `docs/reference/capabilities/CONTROLLED_PRODUCTION_CERTIFICATION_PROGRAM.md` | Controlled Production Certification Program | `CAPABILITY_SPEC` | Governed capability certification. | Capability Earned, controlled production, debt, owner resolution, ladder. | YES | NO | NO | YES |
| `docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md` | L3 Emergency Autonomous Failover | `CAPABILITY_SPEC` | L3 routing autonomy contract. | Wake, incident, planner, authority, identity, verification, rollback. | YES | NO | NO | YES |
| `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` | Operational Maturity Program | `PROGRAM` | Permanent execution engine. | OMP Mission/Continuation, implementation routing, self-evolution. | YES | NO | NO | YES |
| `docs/programs/V7_CURRENT_PROGRAM_STATE.md` | V7 Current Program State | `CURRENT_STATE_ONLY` | Volatile GPS and future autonomy inventory owner. | Current blocker, metrics, authority class, next action. | NO | NO | YES | YES_WITH_FRESHNESS_CHECK |
| `docs/programs/V7_IMPLEMENTATION_PROGRAM.md` | V7 Implementation Program | `PROGRAM` | Supporting implementation flow under OMP. | Existing owner implementation, tests, deploy, certification. | PARTIAL | NO | NO | YES |
| `docs/programs/V7_IMPLEMENTATION_BACKLOG.md` | V7 Implementation Backlog | `PROGRAM` | Existing implementation queue. | Owner tasks, implemented capability set. | PARTIAL | NO | CURRENT-ish | YES_WITH_CAUTION |
| `docs/programs/V7_RESEARCH_FRAMEWORK.md` | V7 Research Framework | `PROGRAM` | Research intake discipline. | External research validation, owner mapping. | YES | NO | NO | YES |
| `docs/policies/POLICY_001_HARD_FAILURE.md` | Hard Failure Policy | `CANONICAL` | Failure policy vocabulary. | Health Evidence, failure classification, L3 entry. | YES | NO | NO | YES |
| `docs/policies/POLICY_002_SOFT_DEGRADATION.md` | Soft Degradation Policy | `CANONICAL` | Degradation vocabulary. | Routing autonomy, observation, degradation state. | YES | NO | NO | YES |
| `docs/policies/POLICY_003_RECOVERY_ADMISSION.md` | Recovery Admission Policy | `CANONICAL` | Recovery safety. | Recovery, anti-flap, post-failure admission. | YES | NO | NO | YES |
| `docs/policies/POLICY_004_AUTHORITY.md` | Authority Policy | `CANONICAL` | Authority boundary. | Authority, human boundary, approval. | YES | NO | NO | YES |
| `docs/policies/POLICY_005_ACTION_CLASS_PROMOTION.md` | Action Class Promotion Policy | `CANONICAL` | Promotion semantics. | Capability Earned, action class authority. | YES | NO | NO | YES |
| `docs/policies/POLICY_006_BLAST_RADIUS.md` | Blast Radius Policy | `CANONICAL` | User/scope limit. | Authority budget, safety, certification ladder. | YES | NO | NO | YES |
| `docs/policies/POLICY_007_ROLLBACK.md` | Rollback Policy | `CANONICAL` | Rollback/no-rollback boundary. | Rollback / Closure, containment. | YES | NO | NO | YES |
| `docs/policies/POLICY_008_FRESHNESS.md` | Freshness Policy | `CANONICAL` | Evidence freshness. | Health Evidence, Runtime eligibility, stale-read blocking. | YES | NO | NO | YES |
| `docs/policies/POLICY_009_ANTI_FLAP.md` | Anti-Flap Policy | `CANONICAL` | Oscillation protection. | Recovery, movement protection, stability. | YES | NO | NO | YES |
| `docs/decisions/ADR-V7-OMP-PRODUCTION-PROGRAM.md` | OMP Production Program ADR | `ADR` | Makes OMP the single execution program. | OMP, no duplicate roadmap. | YES | NO | NO | YES |
| `docs/decisions/ADR-V7-RUNTIME-MODEL.md` | Runtime Model ADR | `ADR` | Runtime thinness and owner composition. | Runtime and Execution, STOP_SAFE, no runtime planner. | YES | NO | NO | YES |
| `docs/decisions/ADR-V7-WORLD-CLASS-DECISION-MODEL.md` | Decision Model ADR | `ADR` | Decision model acceptance. | Decision loop, planning, action vocabulary. | YES | NO | NO | YES |
| `docs/decisions/ADR-V7-ACTION-CLASS-AUTHORITY.md` | Action-Class Authority ADR | `ADR` | Durable authority model. | Authority, packet fallback, class authority. | YES | NO | NO | YES |
| `docs/decisions/ADR-V7-SAFETY-BOUNDED-AUTHORITY.md` | Safety-Bounded Authority ADR | `ADR` | Separates knowledge maturity and bounded action. | Authority, safety, real evidence deadlock avoidance. | YES | NO | NO | YES |
| `docs/decisions/ADR-EVENT-DRIVEN-AUTONOMY.md` | Event-Driven Autonomy ADR | `ADR` | Rejects timer-only movement. | Wake, event-driven autonomy, blind polling rejection. | YES | NO | NO | YES |
| `docs/decisions/ADR-V7-KERNEL-AND-STATE-SPLIT.md` | Kernel and State Split ADR | `ADR` | Separates OMP rules from Current Program State volatile state. | Current Program State, OMP, current state boundary. | YES | NO | NO | YES |
| `docs/decisions/ADR-V7-KNOWLEDGE-QUALITY-MODEL.md` | Knowledge Quality ADR | `ADR` | Knowledge quality decision. | Knowledge Quality, actionability, autonomy-grade knowledge. | YES | NO | NO | YES |
| `docs/decisions/ADR-V7-FRESHNESS-ACTIONABILITY.md` | Freshness Actionability ADR | `ADR` | Fresh/stale/actionable classification. | Freshness, stale evidence, diagnostic-only evidence. | YES | NO | NO | YES |
| `docs/decisions/ADR-V7-IDEAL-AUTONOMOUS-ROUTING-MODEL.md` | Ideal Routing ADR | `ADR` | Routing target accepted. | Routing autonomy, evidence maturity. | YES | NO | NO | YES |
| `docs/decisions/ADR-V7-RECOVERY-ADMISSION-ANTI-FLAP.md` | Recovery/Anti-Flap ADR | `ADR` | Recovery safety decision. | Recovery, anti-flap, admission. | YES | NO | NO | YES |
| `docs/decisions/ADR-FUTURE-EVIDENCE-INDEX-AND-FRESHNESS-MODEL.md` | Future Evidence Index ADR | `ADR` | Future scale evidence model. | Evidence index, freshness, scale. | YES_FOR_FUTURE | NO | NO | YES_WITH_DEFER |
| `docs/decisions/ADR-OBSERVED-OUTCOME-PRIMARY-TRUST.md` | Observed Outcome Primary Trust ADR | `ADR` | Real outcomes outrank claims. | Learning, trust, production evidence. | YES | NO | NO | YES |
| `docs/decisions/ADR-AUTONOMY-EVIDENCE-SATURATION.md` | Evidence Saturation ADR | `ADR` | Evidence sufficiency model. | Evidence coverage, maturity, saturation. | YES | NO | NO | YES |
| `docs/decisions/ADR-AUTONOMY-RISK-TIERED-FLOORS.md` | Risk-Tiered Floors ADR | `ADR` | Autonomy floors by risk. | Authority, maturity floors, certification. | YES | NO | NO | YES |
| `docs/decisions/ADR-AUTONOMY-TRUST-SUFFICIENCY-TIER-AWARE.md` | Trust Sufficiency ADR | `ADR` | Trust by tier. | Trust, confidence, authority floors. | YES | NO | NO | YES |
| `docs/reports/research/2026-07-05_150942_v7_large_scale_autonomous_routing_reliability_research.md` | R1 Routing/Reliability Research | `RESEARCH_ONLY` | External routing reliability validation. | Health matrix, failover, rollback, routing scale. | NO | YES | NO | YES_AS_SUPPORT |
| `docs/reports/research/V7_AUTONOMOUS_OPERATIONS_RESEARCH.md` | R2 Autonomous Operations Research | `RESEARCH_ONLY` | Operations validation. | Incident, SLO/error budget, runbooks, human boundary. | NO | YES | NO | YES_AS_SUPPORT |
| `docs/reports/research/V7_AUTONOMOUS_ENGINEERING_SYSTEMS_RESEARCH.md` | R3 Autonomous Engineering Systems Research | `RESEARCH_ONLY` | Engineering automation validation. | Analyzer/backtesting, engineering automation, workflows. | NO | YES | NO | YES_AS_SUPPORT |
| `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md` | R4 Master Autonomous System Laws | `RESEARCH_ONLY` | Law extraction from R1-R3. | Universal laws, automation/workflow/knowledge laws. | NO | YES | NO | YES_AS_SUPPORT |
| `docs/reports/research/V7_AUTONOMOUS_MODEL_KNOWLEDGE_CONSOLIDATION.md` | This consolidation file | `RESEARCH_ONLY` | Step 1 working file. | Source index, coverage map, future Step 2 input. | NO | YES | NO | YES |
| `docs/reports/engineering/2026-06-30_155940_canonical_integration.md` | Canonical Integration | `ENGINEERING_REPORT_EVIDENCE` | Proves architecture integration closure. | Canonical integration, no duplicate owners. | NO | YES | NO | YES_AS_EVIDENCE |
| `docs/reports/engineering/2026-06-30_200442_l3_execution_closure_verification.md` | L3 Execution Closure Verification | `ENGINEERING_REPORT_EVIDENCE` | Proves L3 closure chain behavior. | Verification, rollback/success, learning, OMP. | NO | YES | NO | YES_AS_EVIDENCE |
| `docs/reports/engineering/2026-07-01_232858_execution_mission_success_l3_one_user_restored.md` | L3 One User Restored | `ENGINEERING_REPORT_EVIDENCE` | Real mission success evidence. | Execution mission, verification PASS, one-user restoration. | NO | YES | NO | YES_AS_EVIDENCE |
| `docs/reports/engineering/2026-07-02_083525_observation_l3_wake_bridge_implementation.md` | Observation L3 Wake Bridge | `ENGINEERING_REPORT_EVIDENCE` | Wake bridge implementation proof. | Observation, Wake, confirmed_current_channel_failure. | NO | YES | NO | YES_AS_EVIDENCE |
| `docs/reports/engineering/2026-07-02_233929_controlled_production_certification_program_execution.md` | Certification Program Execution | `ENGINEERING_REPORT_EVIDENCE` | Controlled certification execution evidence. | Certification phases, debt metrics, pipeline candidates. | NO | YES | NO | YES_AS_EVIDENCE |
| `docs/reports/engineering/2026-07-03_084803_owner_resolution_law.md` | Owner Resolution Law | `ENGINEERING_REPORT_EVIDENCE` | Documents owner-block resolution law integration. | Owner Resolution, terminal classifications. | NO | YES | NO | YES_AS_EVIDENCE |
| `docs/reports/engineering/2026-07-03_124419_committed_l3_apply_emergency_scope_fix.md` | Committed L3 Apply Scope Fix | `ENGINEERING_REPORT_EVIDENCE` | Runtime apply verification scope evidence. | Runtime Apply, verification identity, emergency scope. | NO | YES | NO | YES_AS_EVIDENCE |
| `docs/reports/engineering/2026-07-03_172908_engineering_automation_activation.md` | Engineering Automation Activation | `ENGINEERING_REPORT_EVIDENCE` | Engineering automation target evidence. | Automation Debt, Workflow Debt, pipeline candidates. | NO | YES | NO | YES_AS_EVIDENCE |
| `docs/reports/V7_IDEAL_AUTONOMOUS_ROUTING_SYSTEM_MODEL_REPORT.md` | Ideal Routing System Report | `ENGINEERING_REPORT_EVIDENCE` | Historical basis for ideal routing. | Routing target, knowledge, autonomy. | NO | YES | NO | YES_AS_EVIDENCE |
| `docs/reports/V7_KNOWLEDGE_QUALITY_MODEL_REPORT.md` | Knowledge Quality Model Report | `ENGINEERING_REPORT_EVIDENCE` | Evidence for knowledge quality model creation. | Knowledge Quality, autonomy readiness. | NO | YES | NO | YES_AS_EVIDENCE |
| `docs/reports/V7_DECISION_TO_OUTCOME_TO_LEARNING_INTEGRATION_REPORT.md` | Decision To Outcome To Learning | `ENGINEERING_REPORT_EVIDENCE` | Learning chain evidence. | Learning, observed outcomes, feedback. | NO | YES | NO | YES_AS_EVIDENCE |
| `docs/reports/EVENT.1_REGRESSION_TRIGGER_CERTIFICATION.md` | Event Regression Trigger Certification | `ENGINEERING_REPORT_EVIDENCE` | Event-driven autonomy proof/limits. | Event, wake, restore barrier, no mutation. | NO | YES | NO | YES_AS_EVIDENCE |
| `docs/capacity_2/OBSERVABLE_SIGNAL_INVENTORY.md` | Observable Signal Inventory | `PARTIAL` | Supplemental signal inventory. | Observation, health evidence, capacity. | NO | PARTIAL | NO | YES_WITH_CAUTION |
| `docs/capacity_2/DEGRADATION_MODEL.md` | Degradation Model | `PARTIAL` | Supplemental degradation semantics. | Soft degradation, quality, service impact. | NO | PARTIAL | NO | YES_WITH_CAUTION |
| `docs/operator_actions/OPERATOR_ACTIONS_AUTOMATION_REALITY_AUDIT.md` | Operator Actions Automation Reality Audit | `ENGINEERING_REPORT_EVIDENCE` | Operator/manual action evidence. | Human boundary, automation opportunity. | NO | YES | NO | YES_AS_EVIDENCE |

### 4. Source Classification

| Classification | Count | Role in later Step 2 |
| --- | ---: | --- |
| `CANONICAL` | 23 | Primary durable model source. |
| `ADR` | 16 | Durable decision rationale and boundary source. |
| `PROGRAM` | 5 | Execution, current state, and research workflow source. |
| `CAPABILITY_SPEC` | 2 | Capability-specific execution/certification source. |
| `CURRENT_STATE_ONLY` | 1 | Use only for volatile owner/inventory placement. |
| `REFERENCE_INDEX` | 1 | Owner lookup only. |
| `ENGINEERING_REPORT_EVIDENCE` | 12 | Historical proof and implementation evidence. |
| `RESEARCH_ONLY` | 5 | External validation and law support only. |
| `PARTIAL` | 4 | Supplemental or weakly canonical source. |
| `SUPERSEDED` | 2 | Use only for historical context with caution. |
| `UNKNOWN_RELEVANCE` | 0 | No source promoted with unknown relevance. |

Strongest source categories: `CANONICAL`, `PROGRAM`, `CAPABILITY_SPEC`, and `ADR`.

Weakest source categories: `PARTIAL`, `SUPERSEDED`, and `RESEARCH_ONLY` for SLO/error budget, analyzer/backtesting thresholds, and older autonomy roadmap material.

### 5. Concept Coverage Map

| Concept | Primary source | Secondary sources | Coverage status | Notes |
| --- | --- | --- | --- | --- |
| Business Objective | `docs/product/V7_PRODUCT_SPECIFICATION.md` | Master Handoff, System Architecture | `FOUND_CANONICAL` | Product intent exists; Step 2 should keep it concise. |
| User Access Guarantee | Product Specification | Master Handoff, L3 spec | `FOUND_CANONICAL` | Expressed as keeping users online/restoring connectivity. |
| Reality First | Master Handoff | OMP, AOS, Execution Mission Protocol, ADRs | `FOUND_CANONICAL` | Strongest cross-document law. |
| Observation | SYSTEM_MAP | AOS, Autonomous Runtime Model, policies, R1 | `FOUND_CANONICAL` | Observation plane mapped; health schema spread across owners. |
| Health Evidence | Knowledge Quality Model | R1, service matrix references, policies | `FOUND_PARTIAL` | Concept strong; one unified matrix owner still weak. |
| Incident | Autonomous Runtime Model | L3 spec, Certification Program | `FOUND_CANONICAL` | Incident lifecycle and incident_source exist. |
| Diagnosis | Execution Mission Protocol | Master Handoff, Owner Resolution Law report | `FOUND_CANONICAL` | Breakpoint/producer/consumer/owner method exists. |
| OMP owner routing | SYSTEM_MAP | OMP, Context Resolver, Certification Program | `FOUND_CANONICAL` | SYSTEM_MAP is lookup, not truth. |
| Authority | ADR Action-Class Authority | POLICY_004, Certification Program, L3 spec | `FOUND_CANONICAL` | Authority is durable and blast-radius bounded. |
| Planner | Decision Model | L3 spec, System Architecture, Planner reports | `FOUND_CANONICAL` | Planner selects; Runtime consumes. |
| Identity | L3 spec | Runtime Model, Master Handoff, apply-scope reports | `FOUND_CANONICAL` | Approved Plan Lock/Restore Barrier identity chain is explicit. |
| Runtime and Execution | Runtime Model | Autonomous Runtime Model, ADR Runtime Model | `FOUND_CANONICAL` | Runtime thinness is clear. |
| Verification | Runtime Model | L3 spec, Decision Model, reports | `FOUND_CANONICAL` | Mutation incomplete until verified. |
| Rollback / Closure | POLICY_007 | Runtime Model, Certification Program, reports | `FOUND_CANONICAL` | Rollback/no-rollback closure exists. |
| Learning | Autonomous Runtime Model | Decision-to-outcome report, R4 laws | `FOUND_CANONICAL` | Terminal outcomes only; implementation evidence partial. |
| Production Maturity | Production Maturity Model | Certification Program, Current Program State | `FOUND_CANONICAL` | Consumer only. |
| Current Program State | Current Program State | Kernel/State ADR, AOS | `FOUND_CANONICAL` | Current-state owner; not durable truth. |
| OMP Mission / Continuation | OMP | Context Resolver, OMP ADR | `FOUND_CANONICAL` | Single execution program. |
| Engineering Automation | Master Handoff | Certification Program, activation report, R3 | `FOUND_PARTIAL` | Laws exist; pipeline materialization partial. |
| Automation Debt | Certification Program | Master Handoff, R2/R4 | `FOUND_CANONICAL` | Classification model exists. |
| Workflow Debt | Certification Program | Master Handoff, R3/R4 | `FOUND_CANONICAL` | Pipeline Candidate contract exists. |
| Pipeline Candidate | Certification Program | Engineering automation activation report | `FOUND_PARTIAL` | Registry/projection weak. |
| Analyzer / Backtesting | R3/R4 | OMP Engineering Intelligence, B13 references | `FOUND_PARTIAL` | Advisory/blocking thresholds need review. |
| Knowledge / Truth Model | SYSTEM_MAP | Canonical Reference, Knowledge Quality Model, OMP | `FOUND_CANONICAL` | Layering is strong. |
| Human Boundary | AOS | Master Handoff, R2/R4, Authority policy | `FOUND_CANONICAL` | Humans own policy/exception/architecture. |
| Codex Exit Strategy | AOS | Master Handoff, R3 | `FOUND_PARTIAL` | Principle exists; concrete exit metrics weak. |
| Continuous Self Evolution | AOS | OMP, Master Handoff, R3/R4 | `FOUND_CANONICAL` | Owner-bounded self-improvement exists conceptually. |
| Autonomy Gap | AOS | OMP, Current Program State future inventory | `FOUND_CANONICAL` | Gap model exists; inventory not materialized. |
| Autonomy Inventory | AOS | Current Program State, Autonomy Blueprint | `FOUND_PARTIAL` | Future Current Program State view; not built as current inventory. |
| SLO / Error Budget | R2 | Production Maturity, R1 | `FOUND_RESEARCH_ONLY` | Needs canonical V7 vocabulary before Authority use. |
| External Research Validation | R1/R2/R3/R4 | Research Framework, Research Process | `FOUND_CANONICAL` | Research process is canonical; research content is support. |

### 6. Missing Source Warnings

| Warning | Status | Why it matters | Step 2 handling |
| --- | --- | --- | --- |
| No single `V7_IDEAL_AUTONOMOUS_SYSTEM_MODEL.md` exists yet. | EXPECTED | Future model is not created in Step 1. | Step 2 may consolidate; this step only indexes. |
| Autonomy Inventory is not a concrete Current Program State section/view yet. | `FOUND_PARTIAL` | Future comparison needs current autonomy level per domain. | Mark as Phase 2 inventory input, not current blocker. |
| SLO/error-budget semantics are research-supported but not canonical enough. | `FOUND_RESEARCH_ONLY` | Could accidentally become Authority input. | Treat as `NEEDS_REVIEW`. |
| Analyzer/backtesting thresholds are not fully canonical. | `FOUND_PARTIAL` | Analyzer may be advisory vs blocking. | Keep as Step 2 caution. |
| Pipeline Candidate registry/projection is weak. | `FOUND_PARTIAL` | Workflow debt may not be visible as one inventory. | Map to OMP/Current Program State/Engineering Reports later. |
| `V7_AUTONOMY_BLUEPRINT.md` contains useful inventory but has superseded roadmap content. | `SUPERSEDED` | Step 2 must not revive old roadmap. | Use only as historical source index. |
| Engineering reports contain durable findings but are not durable truth. | NORMAL | Reports can mislead if treated as current canon. | Use as evidence only. |
| Current Program State may lag latest handoff/certification reports. | NORMAL_FOR_Current Program State | Current Program State is volatile. | Always pair Current Program State with timestamp/source. |

### 7. Candidate Source Priority

| Priority | Source family | Use |
| --- | --- | --- |
| P0 | Product Specification, AOS, Master Handoff, OMP, SYSTEM_MAP, Runtime Model, Decision Model, Production Maturity, Certification Program, L3 spec | Primary Step 2 model material. |
| P1 | ADRs, policies, Context Resolver, Execution Mission/Completion, Knowledge Quality, Canonical Reference | Boundary and owner validation. |
| P2 | R1/R2/R3/R4 research KBs | External validation and candidate cautions. |
| P3 | Engineering reports from L3/certification/automation/owner resolution | Evidence of what was proven and what remains partial. |
| P4 | Autonomy Blueprint, older phase/capacity/operator-action docs | Historical/contextual support only; do not treat as current execution authority. |

### 8. Step 1 Findings

1. The knowledge base is sufficient to draft the future ideal autonomous model without inventing architecture.
2. Durable truth is strongest around Reality First, OMP, Runtime thinness, Decision != Execution, Authority, Verification, Rollback, and no duplicate owners.
3. Routing autonomy knowledge is strong, but a unified source-to-owner Health Evidence matrix remains weak.
4. Engineering automation knowledge is strong as law, weaker as materialized pipeline/inventory.
5. SLO/error-budget appears mostly in research and maturity context, not as a fully canonical V7 authority input.
6. Autonomy Inventory is expected to live in Current Program State, but Step 1 found no complete current inventory table.
7. Several useful historical files are explicitly superseded or evidence-only and must not become Step 2 architecture authority.

### 9. Step 1 Verdict

```text
PHASE_1_STEP_1_KNOWLEDGE_COLLECTION_COMPLETE
```

Step 1 is complete.

Step 2 consolidation is recommended.

Step 2 should use this section as the source index and avoid re-running broad unfocused repository discovery unless a source gap is challenged.

### 10. Next Step

Recommended next step:

```text
PHASE_1_STEP_2_CONSOLIDATE_EXISTING_MODEL
```

Step 2 should produce a human-readable consolidation from the indexed sources only.

Step 2 must not:

- create new architecture;
- create new owners;
- create OMP missions;
- create Phase 2 inventory;
- modify Runtime, Planner, Authority, OMP, Current Program State, Production Maturity, or canonical docs;
- create `V7_IDEAL_AUTONOMOUS_SYSTEM_MODEL.md` unless explicitly authorized by the next task.

## Phase 1 Step 1B — Code Reality Collection

### 1. Step Purpose

Collect the code-level reality behind the documented autonomous V7 chain.

This step checks concrete source files, functions, scripts, timers, tests, and admin/API surfaces. It does not synthesize the ideal autonomous model, implement behavior, refactor code, deploy, move users, or change Runtime, Planner, Authority, OMP, Current Program State, Production Maturity, or canonical documents.

### 2. Code Search Scope

Code files inspected or explicitly indexed in Step 1B: `31`.

Functions, classes, scripts, services, timers, or API surfaces indexed: `54`.

Search scope included:

- `tools/`
- `tools/runtime-support/`
- `admin/`
- `admin_core/`
- `systemd/`
- `tests/unit/`
- `tests/contracts/`

Representative search terms:

```text
observe observation health service_matrix wake incident planner candidate selected_move authority
approved_plan lock restore_barrier runtime_apply apply verification verify rollback learning
production_maturity current_program_state omp mission owner_resolution automation_debt workflow_debt
pipeline_candidate engineering_report canonical_sync safe_deploy truth_check convergence admin dashboard operator
```

Search warning: broad grep across the repository returns many documentation and evidence hits. Step 1B promotes only concrete code artifacts, tests, CLIs, systemd units, or API surfaces.

### 3. Code Artifact Index

| Path | Function / class / script / API | What it does | Input | Output | Caller / trigger | Consumer | Owner / domain | Tests found | Model match | Connected? | Runtime status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `systemd/v7-users-autoswitch.timer` | `v7-users-autoswitch.timer` | Movement heartbeat. | systemd timer schedule | starts service | systemd | `v7-users-autoswitch.service` | Movement heartbeat | `tests/unit/test_v7_sync_tools.py` | YES | YES | Real production path |
| `systemd/v7-users-autoswitch.service` | `ExecStart=/usr/local/bin/v7-governed-canary-dry-run-cycle --execute-l3-production-validation ... --max-users 1` | Starts governed L3 validation owner. | timer trigger | governed owner CLI | movement timer | governed owner | Governed L3 owner | `tests/unit/test_v7_sync_tools.py` | YES | YES | Real production path |
| `systemd/drafts/v7-autoswitch-planner.timer` | `v7-autoswitch-planner.timer` | Planner refresh heartbeat. | systemd timer schedule | starts planner refresh service | systemd | planner refresh service | Planner refresh | forensic reports, endpoint tests | YES_WITH_LIMIT | YES | Refresh-only path |
| `systemd/drafts/v7-autoswitch-planner.service` | `ExecStart=/usr/local/bin/v7-users-autoswitch --pre-planner-refresh=write ...` | Refreshes planner/intelligence state without apply. | timer trigger | planner state refresh | planner timer | state snapshots | Planner refresh | forensic reports | YES_WITH_LIMIT | YES | No Runtime Apply |
| `systemd/v7-service-matrix-refresh.service` | `ExecStart=/usr/local/bin/v7-service-matrix-refresh-all` | Refreshes service matrix. | enabled egress registry | `service-matrix.json` | service-matrix timer | Planner / snapshots / verification | Health Evidence | `tests/unit/test_telegram_sentinel_lock_scope.py`, autoswitch tests | YES | YES | Real observation writer |
| `systemd/v7-telegram-sentinel.service` | `ExecStart=/usr/local/bin/v7-telegram-sentinel --no-autoswitch` | Fast Telegram sentinel, no direct autoswitch. | egress registry, network probe | matrix/event updates | telegram timer | service matrix, events | Health Evidence / Observation | `tests/unit/test_telegram_sentinel_lock_scope.py` | YES | YES | Real observation writer |
| `tools/v7-telegram-sentinel` | `check_egress`, `check_telegram`, `update_matrix_items`, `run_autoswitch` | Probes Telegram and writes matrix/events; autoswitch hook exists but service uses `--no-autoswitch`. | egress row, prior matrix, socket probe | service matrix item / event | systemd sentinel service | Planner / intelligence snapshots | Observation / Health Evidence | `tests/unit/test_telegram_sentinel_lock_scope.py` | PARTIAL | PARTIAL | Real writer, autoswitch hook dormant in service |
| `tools/v7-service-matrix-refresh-all` | `run_one`, `service_matrix_writer_lock`, `main` | Refreshes service matrix for enabled egress channels. | egress registry, checker command | service matrix JSON/events | systemd service | Planner, snapshots, verification | Health Evidence | lock-scope and autoswitch tests | YES | YES | Real writer |
| `tools/v7-service-matrix-test` | CLI script | Tests required service reachability for one egress/user path. | target/user/egress service args | rc/stdout result | Runtime verification / matrix refresh | `tools/v7-users-autoswitch._verify_emergency_required_services` | Verification / Health Evidence | `tests/unit/test_v7_users_autoswitch_policy.py` | YES | YES | Real verification path |
| `tools/v7-intelligence-snapshot-refresh` | `build_stable_snapshot_run`, `load_inputs`, `read_jsonl_family` | Builds Heavy Brain intelligence snapshots from existing evidence. | service matrix, quality, registries, audit/history | snapshot families under state/intelligence | planner refresh, L3 plan pre-refresh | Planner advisory inputs / Admin UI | Intelligence snapshots | `tests/unit/test_intelligence_workers.py` | YES_WITH_LIMIT | YES | Connected advisory path |
| `admin_core/intelligence_workers.py` | `build_all_snapshots` | Coordinates all snapshot families. | service matrix, quality, feedback, registries | WorkerRunResult snapshots | `tools/v7-intelligence-snapshot-refresh` | Planner/advisory/admin read models | Intelligence / Learning read model | `tests/unit/test_intelligence_workers.py` | YES_WITH_LIMIT | YES | Advisory, no runtime authority |
| `admin_core/intelligence_workers.py` | `build_service_score_snapshots` | Converts service matrix and quality into service/channel scores. | service matrix, quality, preferences | service-score snapshots | snapshot refresh | Planner advisory / Admin UI | Health Evidence read model | `tests/unit/test_intelligence_workers.py` | YES | YES | Advisory |
| `admin_core/intelligence_workers.py` | `build_candidate_suitability_snapshot` | Builds per-user candidate suitability. | services, users, egress, trust/risk/blast snapshots | candidate suitability snapshot | snapshot refresh | Planner advisory / Admin UI | Planner intelligence | `tests/unit/test_intelligence_workers.py` | YES_WITH_LIMIT | YES | Advisory |
| `admin_core/intelligence_workers.py` | `build_best_available_pool_snapshot` | Builds best available pool advice. | candidate suitability, runtime state, egress registry | best-available-pool snapshot | snapshot refresh | Planner advisory | Planner intelligence | `tests/unit/test_intelligence_workers.py`, autoswitch policy tests | YES_WITH_LIMIT | YES | Advisory |
| `admin_core/intelligence_workers.py` | `build_trust_evolution_snapshot` | Aggregates outcome/rollback/feedback evidence. | audit/switch/rollback records and snapshots | trust-evolution snapshot | snapshot refresh | Learning read model / Admin UI | Learning | `tests/unit/test_intelligence_workers.py` | YES_WITH_LIMIT | YES | Advisory / evidence consumer |
| `admin_core/operator_execution_feedback.py` | `decision_outcome_learning_model` | Aggregates closed outcome records into learning model. | decision feedback closure records | learning/effectiveness summary | intelligence workers | trust evolution / admin read model | Learning | `tests/unit/test_operator_execution_feedback.py`, `tests/unit/test_intelligence_workers.py` | YES | YES | Read-only learning model |
| `tools/v7-users-autoswitch` | `Planner._l3_incident_context` | Materializes L3 incident context from gate evidence and selected moves. | emergency gate, selected moves, operation | `safety.l3_incident` | Planner plan generation | Runtime apply, learning closure | Incident | `tests/unit/test_v7_users_autoswitch_policy.py` | YES | YES | Real L3 path |
| `tools/v7-users-autoswitch` | `Planner._decision_for_user` | Computes per-user keep/switch/failover decision. | user, candidate set, current candidate | decision row | planner plan | `_select_moves`, plan output | Planner | `tests/unit/test_v7_users_autoswitch_policy.py` | YES | YES | Real planner path |
| `tools/v7-users-autoswitch` | `Planner._candidate` | Builds candidate and runs basic/reservation/org/quality/service/load/safety gates. | user, egress, services, route class | Candidate object | `_decision_for_user` | candidate JSON / decisions | Planner / Eligibility | `tests/unit/test_v7_users_autoswitch_policy.py` | YES | YES | Real planner path |
| `tools/v7-users-autoswitch` | `_gate_basic`, `_gate_reservation`, `_gate_org`, `_gate_quality`, `_gate_service`, `_gate_load`, `_gate_safety` | Eligibility gates. | Candidate and policy/evidence state | `eligible`, blockers, reasons | `_candidate` | Planner decision / failover selection | Planner eligibility | `tests/unit/test_v7_users_autoswitch_policy.py` | YES | YES | Real planner path |
| `tools/v7-users-autoswitch` | `_service_truth_classification`, `_service_truth_freshness` | Classifies service evidence freshness and truth. | service matrix row, required/relevant flags | truth class and blocked action | service suitability/gate service | candidate eligibility / reasons | Health Evidence / Freshness | `tests/unit/test_v7_users_autoswitch_policy.py` | YES | YES | Real planner path |
| `tools/v7-users-autoswitch` | `_select_moves`, `_pick_projected_moves` | Selects bounded moves and filters exhausted semantic retries. | decisions, incident source context, projected load | selected moves | planner plan | Restore Barrier / packet / apply | Planner | `tests/unit/test_v7_users_autoswitch_policy.py` | YES | YES | Real planner path |
| `tools/v7-users-autoswitch` | `_l3_retry_budget_exhausted_for_move` | Excludes exhausted semantic attempts in active incident continuation. | move, incident context, retry budget | retry state / exhausted flag | `_pick_projected_moves` | selected move filtering | Planner / Retry Budget | `tests/unit/test_v7_users_autoswitch_policy.py` | YES | YES | Real planner path |
| `tools/v7-users-autoswitch` | authority budget functions and promotion gates | Computes governed batch ladder and promotion readiness. | policy, evidence, truth check | authority budget / blockers | Planner / authority readiness commands | selected move cap / promotion | Authority | `tests/unit/test_v7_users_autoswitch_policy.py` | YES | YES | Real authority code |
| `tools/v7-users-autoswitch` | `_authority_promotion_truth_check` | Runs `v7-truth-check` before authority promotion. | truth check command | pass/fail/blockers | authority promotion path | authority readiness | Authority / Truth | `tests/unit/test_v7_users_autoswitch_policy.py`, `tests/unit/test_v7_truth_check.py` | YES | YES | Real gate |
| `tools/v7-users-autoswitch` | `Planner.apply` | Applies selected moves only when committed envelope/gates pass. | plan, restore barrier, approved identity | apply result | `--apply --verify` CLI | operation finalization / audit / learning | Runtime Apply | `tests/unit/test_v7_users_autoswitch_policy.py` | YES | YES | Real Runtime path |
| `tools/v7-users-autoswitch` | `_verify_routes_for_apply`, `_verify_emergency_required_services` | Route and required-service verification after apply. | moved user / target / selected move | rc/stdout | `Planner.apply` | rollback decision / terminal classification | Verification | `tests/unit/test_v7_users_autoswitch_policy.py` | YES | YES | Real Runtime path |
| `tools/v7-users-autoswitch` | `_run_switch` | Calls existing user switch command for apply/rollback. | user ip, target, reason | subprocess result | `Planner.apply` | verification/rollback result | Runtime Apply / Rollback | `tests/unit/test_v7_users_autoswitch_policy.py` | YES | YES | Real mutation boundary |
| `tools/v7-users-autoswitch` | `finalize_operation`, `_l3_materialize_learning_closure` | Emits terminal audit and L3 learning closure after apply. | plan/apply result/incident | operation terminal, audit, feedback rows | planner CLI completion | governed owner proof / learning files | Learning / Closure | `tests/unit/test_v7_users_autoswitch_policy.py` | YES | YES | Real terminal path |
| `tools/v7-governed-canary-dry-run-cycle` | `run_l3_production_validation_plan` | Runs Planner in governed L3 planning mode with pre-refresh. | state/event/snapshot/restore barrier/max users/source | plan payload | `execute_l3_production_validation` | packet materialization | Governed owner | `tests/unit/test_governed_canary_cli.py` | YES | YES | Real production validation path |
| `tools/v7-governed-canary-dry-run-cycle` | `execute_l3_production_validation` | Full governed L3 owner: plan, authority budget check, packet, lease, restore barrier, apply, proof. | explicit confirmation, max users, state/event paths | execution result | systemd movement service or CLI | audit/report/certification | Governed L3 owner | `tests/unit/test_governed_canary_cli.py` | YES | YES | Real governed path |
| `tools/v7-governed-canary-dry-run-cycle` | `run_autoswitch_apply` | Calls `v7-users-autoswitch --apply --verify` with approved identity. | packet identity, max users, source/target | apply payload | `execute_l3_production_validation` | proof quality / lease terminalization | Runtime bridge | `tests/unit/test_governed_canary_cli.py` | YES | YES | Real bridge |
| `tools/v7-governed-canary-dry-run-cycle` | `materialize_governed_transaction_feedback` | Converts execution result into feedback records. | packet/apply/operation result | feedback materialization | governed transaction path | learning/intelligence | Learning | `tests/unit/test_governed_canary_cli.py` | YES | YES | Connected |
| `admin_core/operator_execution.py` | `packet_from_plan` | Materializes governance packet from Planner plan. | plan, dual approval ids, TTL | packet with approved plan lock/rollback manifest | governed L3 owner | `execute_packet`, Runtime apply identity | Approved Plan Lock / Packet | `tests/unit/test_operator_execution_packet.py`, governed CLI tests | YES | YES | Real governed path |
| `admin_core/operator_execution.py` | `approved_plan_lock_from_selected` | Builds immutable selected-move identity lock. | selected moves, packet, packet hash | approved plan lock | `packet_from_plan`, `packet_from_preview` | restore barrier / runtime apply identity | Approved Plan Lock | `tests/unit/test_operator_execution_packet.py` | YES | YES | Real governed path |
| `admin_core/operator_execution.py` | `runtime_recheck` | Rechecks packet/runtime source hashes and governance constraints. | packet, state dir, planner snapshot | allow/deny verdict | `execute_packet` | restore barrier clearance | Authority / Runtime Recheck | `tests/unit/test_operator_execution_packet.py` | YES | YES | Real governed path |
| `admin_core/operator_execution.py` | `build_restore_barrier_clearance` | Builds generation-bound restore barrier clearance. | packet | clearance object | `append_restore_barrier_clearance` | `tools/v7-users-autoswitch` restore barrier gate | Restore Barrier | `tests/unit/test_operator_execution_packet.py` | YES | YES | Real governed path |
| `admin_core/operator_execution.py` | `append_restore_barrier_clearance` | Writes restore barrier clearance, with duplicate owner guard. | restore barrier file, packet, recheck | clearance file/result | `execute_packet` | Runtime apply | Restore Barrier | `tests/unit/test_operator_execution_packet.py` | YES | YES | Real governed path |
| `admin_core/operator_execution.py` | `execute_packet` | Validates/consumes governance packet and writes clearance/audit records. | packet, audit store, state dir | approval/denial/clearance result | governed L3 owner / packet CLI | Runtime apply gate | Authority / Restore Barrier | `tests/unit/test_operator_execution_packet.py` | YES | YES | Real governed path |
| `admin_core/operator_execution.py` | `create_execution_lease_from_packet`, `write_execution_lease`, `finish_execution_lease` | Preserves operation identity and blocks overlaps. | packet/operation | execution lease state | governed L3 owner | apply bridge / duplicate guard | Identity | `tests/unit/test_operator_execution_packet.py`, governed CLI tests | YES | YES | Real governed path |
| `admin_core/operator_execution_pipeline.py` | `EXECUTION_LOOP_STAGES` | Static canonical stage contract. | none | stage metadata | admin/readiness/tests | admin UI / tests | Pipeline model | `tests/unit/test_operator_execution_pipeline.py` | YES | PARTIAL | Read model / contract |
| `admin_core/operator_execution_pipeline.py` | `governed_canary_knowledge_gated_dry_run_cycle` | Builds operator preview cycle for governed canary path. | events, decision surface, lease, max users | packet preview / stop reason | governed transaction path / admin UI | packet materialization | Operator execution pipeline | `tests/unit/test_operator_execution_pipeline.py`, governed CLI tests | YES | YES | Connected preview path |
| `admin_core/operator_execution_pipeline.py` | `l3_production_validation_runtime_action_transition` | Validates L3 production plan can transition to runtime action. | plan, max users | transition verdict | governed L3 owner | packet constraints / apply path | Authority transition | `tests/unit/test_governed_canary_cli.py` | YES | YES | Real governed path |
| `admin_core/operator_execution_pipeline.py` | `pipeline_certification` and dashboard helpers | Certifies/read-models pipeline shape. | existing records / static contracts | dashboard/certification payload | admin API/tests | Admin UI | Engineering Automation / Operator visibility | `tests/unit/test_operator_execution_pipeline.py` | YES_WITH_LIMIT | PARTIAL | Read-only |
| `admin/v7-admin-api` | `GET /api/operator/*` | Operator visibility endpoints. | HTTP GET | read-only JSON views | browser/admin UI | operator | Admin UI / visibility | `tests/unit/test_operator_observability.py`, contract tests | YES | YES | Read-only visibility |
| `admin/v7-admin-api` | `GET /api/execution/*` | Execution dashboard/readiness/candidate views. | HTTP GET | read-only JSON views | browser/admin UI | operator/engineering | Admin UI / visibility | endpoint contract tests | YES_WITH_LIMIT | YES | Read-only visibility |
| `admin/v7-admin-api` | `GET /api/omp/dashboard` | OMP dashboard projection. | HTTP GET | OMP dashboard JSON | admin UI | operator/engineering | OMP visibility | endpoint contract tests | YES_WITH_LIMIT | PARTIAL | Read-only projection |
| `admin/v7-admin-api` | `GET /api/runtime/convergence` | Runtime convergence projection. | HTTP GET | convergence JSON | admin UI | operator/engineering | Convergence visibility | endpoint contract tests | YES | YES | Read-only projection |
| `admin_core/operator_views.py` | facade functions | Thin read-only facade over operator observability. | repo/state/event paths | operator view payloads | admin API | admin UI | Operator visibility | `tests/unit/test_operator_observability.py` | YES | YES | Read-only |
| `admin_core/operator_observability.py` | `build_operator_view_model`, `build_operator_operation_detail`, `audit_search`, `execution_governance_preview` | Builds operator evidence/lineage/governance previews. | repo/audit/evidence files | read-only view payloads | admin API | admin UI | Operator visibility | `tests/unit/test_operator_observability.py` | YES | YES | Read-only |
| `tools/v7-truth-check` | `combine_results`, CLI `main` | Fail-closed local/GitHub/runtime truth gate. | manifest, git/runtime commands | truth verdict | safe deploy / authority promotion / operator | convergence / authority | Truth / Safe deploy | `tests/unit/test_v7_truth_check.py` | YES | YES | Real gate, read-only |
| `tools/v7-safe-deploy` | `main`, `v7_sync_lib.safe_deploy_plan` | Approved deploy/provenance helper. | apply/confirm flags | deploy plan/result | operator/automation | production runtime | Safe Deploy | `tests/unit/test_v7_sync_tools.py` | YES | YES | Real deploy owner when invoked |
| `tools/v7-convergence-owner` | `sync.convergence_owner_status` | Single operator-facing convergence next action. | local/github/runtime truth | next action / safe command | operator/admin | human / automation | Convergence | `tests/unit/test_v7_sync_tools.py` | YES | YES | Read-only owner |
| `tools/v7_sync_lib.py` | `truth_check`, `convergence_status`, `convergence_owner_status` | Shared implementation for truth/convergence/safe deploy tooling. | git/runtime/deploy manifest | status / safe next command | CLIs | operator/admin | Truth / Convergence | `tests/unit/test_v7_sync_tools.py` | YES | YES | Real tooling core |
| `admin_core/intelligence_platform.py` | platform models and certification helpers | Models SLO, replay, drift, shadow execution, readiness. | synthetic/current records | read-only model payloads | tests/admin future surfaces | research/admin | Analyzer / Backtesting | `tests/unit/test_intelligence_platform.py` | PARTIAL | PARTIAL | Mostly framework/read-only |
| `admin_core/shadow_autonomy.py` | `build_shadow_autonomy_model` | Builds shadow/autonomy comparison model. | decision surface/history | shadow autonomy payload | admin API/tests | operator UI | Continuous Self Evolution / Shadow autonomy | `tests/unit/test_shadow_autonomy.py` | PARTIAL | PARTIAL | Read-only |
| `tools/v7-autonomy-trust-evidence-inventory` | CLI `main` | Read-only autonomy trust evidence inventory. | state/audit/event dirs | inventory JSON | operator/research | reports/admin | Autonomy inventory | tests via acceleration suite | PARTIAL | UNKNOWN | Read-only, not runtime chain |

### 4. Function-Level Autonomous Chain Map

| Ideal chain step | Documented owner | Code path / function | Input | Output | Downstream consumer | Connected? | Tested? | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Reality | Reality First / runtime state | state files under `/opt/v7/egress/state`, registries read by `tools/v7-users-autoswitch`, `tools/v7-intelligence-snapshot-refresh`, admin views | production registries, service matrix, quality, audit/events | real state inputs | Observation, Planner, Admin UI | YES | YES | `CODE_CONFIRMED` | Code reads existing state; Step 1B did not inspect production state. |
| Observation | Observation / Health Evidence | `tools/v7-telegram-sentinel`, `tools/v7-service-matrix-refresh-all`, `tools/v7-path-benchmark` | network probes, egress registry | matrix/events/quality samples | Planner and snapshots | YES | YES | `CODE_CONFIRMED` | Telegram autoswitch hook is dormant under systemd `--no-autoswitch`; writer path is real. |
| Health Evidence | Service Matrix / Quality | `service_matrix_writer_lock`, `build_service_score_snapshots`, `_service_truth_classification` | service matrix, quality summary | truth classes, service scores | Candidate gates / snapshots | YES | YES | `CODE_CONFIRMED` | Unified health model is spread across writer, snapshot, and planner functions. |
| Incident | L3 Emergency Failover | `Planner._l3_incident_context`, runtime incident record helpers | emergency gate evidence and selected moves | `safety.l3_incident`, incident key/source | Runtime eligibility / learning | YES | YES | `CODE_CONFIRMED` | Incident source exists in code and is used by L3 continuation tests. |
| Diagnosis | Execution Mission / Owner Resolution | reports and admin read models; no single runtime diagnosis owner found | evidence/reports | diagnosis text/views | human/Codex | PARTIAL | PARTIAL | `CODE_PARTIAL` | Breakpoint investigation is mostly documented/report-driven, not one executable owner. |
| OMP owner routing | SYSTEM_MAP / OMP | `admin_core/operator_execution_pipeline.EXECUTION_LOOP_STAGES`, admin endpoint inventories | static owner map | owner/stage metadata | admin UI/tests | PARTIAL | YES | `CODE_PARTIAL` | Code maps execution stages; full canonical owner mapping remains documentation-led. |
| Authority | POLICY_004 / Action-class authority | authority budget/promotion functions in `tools/v7-users-autoswitch`, `operator_execution.validate_nonzero_packet`, `runtime_recheck` | policy/evidence/truth/packet | allow/deny, authorized budget | packet/restore barrier/apply | YES | YES | `CODE_CONFIRMED` | Real L3 governed path uses this gate. |
| Planner | Planner | `Planner._decision_for_user`, `_candidate`, gates, `_select_moves` | users, egress, policy, evidence | decisions and selected moves | packet owner / Runtime apply | YES | YES | `CODE_CONFIRMED` | Real planner path is heavily tested. |
| Identity | Approved Plan Lock / Execution Lease | `approved_plan_lock_from_selected`, `packet_from_plan`, `create_execution_lease_from_packet` | selected moves and packet | lock, rollback manifest, lease | restore barrier / apply bridge | YES | YES | `CODE_CONFIRMED` | Strong identity continuity code and tests exist. |
| Runtime and Execution | Runtime | `Planner.apply`, `run_autoswitch_apply`, `_run_switch` | approved plan, restore barrier, CLI args | user movement result | verification/finalization | YES | YES | `CODE_CONFIRMED` | Real mutation boundary is `v7-users-autoswitch --apply --verify`. |
| Verification | Runtime / Verification | `_verify_routes_for_apply`, `_verify_emergency_required_services`, `tools/v7-service-matrix-test` | moved user/target/services | verification rc/output | rollback decision | YES | YES | `CODE_CONFIRMED` | Real post-apply verification exists. |
| Rollback / Closure | Runtime / Rollback | `_run_switch(..., "rollback")`, rollback packet manifest, `finish_execution_lease`, `finalize_operation` | failed verification and rollback target | rollback result, terminal operation | learning/audit | YES | YES | `CODE_CONFIRMED` | Rollback is part of Runtime apply path. |
| Learning | Learning / Feedback | `_l3_materialize_learning_closure`, `decision_outcome_learning_model`, trust evolution snapshot | terminal operation/apply results | feedback and closure records | intelligence snapshots / certification | YES | YES | `CODE_CONFIRMED` | Learning exists as feedback/read model; not an independent planner writer. |
| Production Maturity | Production Maturity | No dedicated code writer found; mostly docs/reports/admin projections | certification evidence | maturity status in docs/reports | humans/OMP | NO | PARTIAL | `DOC_ONLY` | Code has maturity-like models, but canonical Production Maturity update appears document/report-led. |
| Current Program State | Current Program State | No dedicated code writer found in inspected files | reports / human state | current state document | OMP/humans | NO | UNKNOWN | `DOC_ONLY` | Current Program State is documented as volatile owner; Step 1B found no connected code updater. |
| OMP Mission / Continuation | OMP | `/api/omp/dashboard`, docs/reports, no mission executor found | docs/reports/evidence | dashboard projection | admin UI/humans | PARTIAL | PARTIAL | `CODE_PARTIAL` | OMP visibility exists; executable mission continuation remains documentation/Codex-led. |
| Engineering Automation | Engineering Automation | `admin_core/intelligence_platform`, `operator_execution_pipeline.pipeline_certification`, reports | evidence/models | automation/readiness views | admin/research | PARTIAL | YES | `CODE_PARTIAL` | Mostly read-only model and certification helpers, not closed-loop automation. |
| Continuous Self Evolution | Learning / OMP | trust evolution, decision outcome learning, shadow autonomy | outcomes/history | advisory model updates | planner advisory/admin | PARTIAL | YES | `CODE_PARTIAL` | Evidence feeds models, but automatic model-to-capability loop is not fully connected. |

### 5. Documented Model vs Code Reality

| Documented concept | Code reality | Status | Evidence |
| --- | --- | --- | --- |
| Governed L3 execution chain | Exists and is connected through timer/service, governed owner, Planner, packet, approved lock, restore barrier, Runtime apply, verification, rollback, learning closure. | `CODE_CONFIRMED` | `systemd/v7-users-autoswitch.service`, `tools/v7-governed-canary-dry-run-cycle`, `tools/v7-users-autoswitch`, `admin_core/operator_execution.py` |
| Planner refresh loop | Exists as separate refresh-only path. | `CODE_CONFIRMED` | `systemd/drafts/v7-autoswitch-planner.service` |
| Observation -> confirmed channel failure | Code exists in Planner/L3 wake path and tests. | `CODE_CONFIRMED` | `tools/v7-users-autoswitch`, tests around `confirmed_current_channel_failure` |
| Incident source continuity | Code and regression tests exist. | `CODE_CONFIRMED` | `tools/v7-users-autoswitch`, `test_active_failed_source_incident_constrains_next_l3_selection`, `test_l3_success_keeps_failed_source_incident_open_when_users_remain` |
| Retry-aware continuation | Code and tests exist. | `CODE_CONFIRMED` | `_l3_retry_budget_exhausted_for_move`, `test_active_incident_skips_exhausted_semantic_attempt_and_selects_next_user` |
| Adaptive governed batch ladder | Code constants/promotion gates and tests exist; production enablement remains authority/certification-bound. | `CODE_CONFIRMED` | `AUTHORITY_CLASS_BUDGETS`, promotion rules, governed CLI tests |
| Production Maturity consumer | Canonical docs exist; no connected code writer found. | `DOC_ONLY` | No concrete code owner found in Step 1B. |
| Current Program State writer | Canonical docs exist; no connected code writer found. | `DOC_ONLY` | No concrete code owner found in Step 1B. |
| Automation Debt / Workflow Debt / Pipeline Candidate | Documented strongly; code is mostly read-only modeling/report support. | `CODE_PARTIAL` | `admin_core/intelligence_platform.py`, `operator_execution_pipeline.py`, reports |
| Analyzer / Backtesting | Framework code exists, but mostly read-only and not connected as a blocking production owner. | `CODE_PARTIAL` | `admin_core/intelligence_platform.py`, tests |
| Admin UI / operator visibility | Broad read-only API surface exists; it should not be treated as execution authority. | `CODE_CONFIRMED` | `admin/v7-admin-api`, `admin_core/operator_views.py`, endpoint tests |

### 6. Connected Paths

| Path | Chain | Status | Notes |
| --- | --- | --- | --- |
| Governed movement heartbeat | `v7-users-autoswitch.timer` -> `v7-users-autoswitch.service` -> `tools/v7-governed-canary-dry-run-cycle --execute-l3-production-validation` -> Planner -> packet -> restore barrier -> Runtime apply/verify -> rollback/no-rollback -> learning closure | `CODE_CONFIRMED` | Strongest confirmed end-to-end code path. |
| Planner refresh heartbeat | `v7-autoswitch-planner.timer` -> `v7-autoswitch-planner.service` -> `tools/v7-users-autoswitch --pre-planner-refresh=write` -> intelligence snapshot refresh | `CODE_CONFIRMED_REFRESH_ONLY` | Does not invoke Runtime Apply or Verification. |
| Health evidence writer path | `v7-service-matrix-refresh.timer/service` and `v7-telegram-sentinel.timer/service` -> service matrix/events -> Planner/snapshots | `CODE_CONFIRMED` | Sentinel service explicitly uses `--no-autoswitch`. |
| Governed packet path | Planner plan -> `operator_execution.packet_from_plan` -> approved plan lock -> `execute_packet` -> restore barrier clearance -> Runtime apply identity args | `CODE_CONFIRMED` | Strong identity preservation and tests. |
| Learning evidence path | Runtime terminal apply result -> `_l3_materialize_learning_closure` / governed feedback materialization -> intelligence snapshots -> admin/read models | `CODE_CONFIRMED_WITH_READ_MODEL_LIMIT` | Connected as evidence/read model; not a standalone autonomous decision writer. |
| Admin visibility path | state/audit/evidence -> `admin_core/operator_observability` / admin API -> operator dashboard | `CODE_CONFIRMED_READ_ONLY` | Visibility only. |
| Safe deploy / convergence path | `tools/v7-truth-check` -> `v7_sync_lib.convergence_status` -> `v7-convergence-owner` / `v7-safe-deploy` | `CODE_CONFIRMED` | Real tooling owner; production access not exercised in Step 1B. |

### 7. Dormant / Partial / Unused Code

| Artifact | Classification | Reason |
| --- | --- | --- |
| `tools/v7-telegram-sentinel.run_autoswitch` | `DORMANT` | Code hook exists, but systemd service invokes sentinel with `--no-autoswitch`; movement is owned by governed L3 owner. |
| `admin_core/intelligence_platform.py` production shadow / SLO / replay / drift helpers | `CODE_PARTIAL` | Extensive tested framework, mostly read-only and not connected as production blocking owner. |
| `admin_core/shadow_autonomy.py` | `CODE_PARTIAL` | Shadow/autonomy model exists, but does not execute runtime actions. |
| `admin_core/operator_execution_pipeline.pipeline_certification` and dashboard helpers | `CODE_PARTIAL` | Useful read-only certification/visibility model, not a Runtime executor. |
| `tools/v7-autonomy-trust-evidence-inventory` | `UNKNOWN` / `PARTIAL` | Read-only inventory CLI exists; Step 1B did not find a connected production invocation. |
| `/api/execution/*` candidate/workflow endpoints | `CODE_PARTIAL` | Operator/readiness display, not execution authority. |
| Production Maturity / Current Program State automatic synchronization | `DOC_ONLY` | No connected code writer found in inspected artifacts. |

Dormant, unconnected, partial, or doc-only artifacts counted in this section: `7`.

### 8. Missing Code For Documented Concepts

| Concept | Missing / weak code reality | Status |
| --- | --- | --- |
| Current Program State automatic writer | No connected code owner found that updates `docs/programs/V7_CURRENT_PROGRAM_STATE.md` from runtime/certification evidence. | `DOC_ONLY` |
| Production Maturity automatic writer | No connected code owner found that updates canonical Production Maturity state from capability evidence. | `DOC_ONLY` |
| OMP executable mission continuation | OMP dashboard/read models exist; no single code executor found that converts reports/blockers into next OMP mission. | `CODE_PARTIAL` |
| Automation Debt registry | Debt laws/docs exist; no single code registry/updater found. | `DOC_ONLY` / `CODE_PARTIAL` |
| Workflow Debt registry | Workflow laws/docs exist; no single code registry/updater found. | `DOC_ONLY` / `CODE_PARTIAL` |
| Pipeline Candidate registry | Candidate concept exists in docs/read models; no durable connected registry owner found. | `CODE_PARTIAL` |
| Owner Resolution executor | Owner Resolution law exists in docs/reports; no executable owner-resolution loop found. | `DOC_ONLY` |
| Analyzer/backtesting as blocking authority | Framework/test code exists; no connected production blocking path found. | `CODE_PARTIAL` |
| Engineering Report generation owner | Reports exist, but no single code artifact found that automatically creates required engineering reports after every breakpoint. | `DOC_ONLY` |

### 9. Tests / Regression Coverage Map

| Area | Test files found | Coverage status | Notes |
| --- | --- | --- | --- |
| Planner gates, L3 wake, incident source, retry, apply/verify/rollback | `tests/unit/test_v7_users_autoswitch_policy.py` | STRONG | Covers many historical defects and L3 continuation behavior. |
| Governed owner / L3 production validation / batch budget | `tests/unit/test_governed_canary_cli.py` | STRONG | Covers explicit confirmation, packet path, apply bridge, batch budgets, proof quality. |
| Packet / approved plan lock / restore barrier / execution lease | `tests/unit/test_operator_execution_packet.py` | STRONG | Covers lock, packet, clearance, lease, identity. |
| Operator execution pipeline | `tests/unit/test_operator_execution_pipeline.py` | STRONG_READ_ONLY | Covers pipeline contracts, dry run, dashboard, no direct runtime execution. |
| Intelligence snapshots / learning read model | `tests/unit/test_intelligence_workers.py`, `tests/unit/test_operator_execution_feedback.py` | STRONG_READ_ONLY | Covers snapshot families and outcome learning. |
| Safe deploy / truth / convergence | `tests/unit/test_v7_truth_check.py`, `tests/unit/test_v7_sync_tools.py` | STRONG | Covers dirty classification, truth gate, deploy manifest, convergence owner. |
| Admin operator visibility | `tests/unit/test_operator_observability.py`, `tests/contracts/endpoint_inventory_test.py` | STRONG_READ_ONLY | Ensures operator namespace is read-only and endpoints remain stable. |
| Analyzer/backtesting/intelligence platform | `tests/unit/test_intelligence_platform.py` | PARTIAL_FRAMEWORK | Tests framework models; not proof of connected production blocking. |
| Current Program State / Production Maturity / debt registries | No direct code-owner tests found | WEAK | Likely documentation/report-led today. |

Cheap test policy: Step 1B did not run heavy suites because the mission is read-only collection. Relevant test files were listed and indexed.

### 10. Runtime / Authority / Production Safety Confirmation

Confirmed for Step 1B:

```text
NO code changes
NO runtime behavior changes
NO Planner changes
NO Authority changes
NO production changes
NO deployment
NO users moved
NO timers started/stopped/enabled/disabled
```

The only file intended for modification by this step is:

```text
docs/reports/research/V7_AUTONOMOUS_MODEL_KNOWLEDGE_CONSOLIDATION.md
```

### 11. Step 1B Findings

1. The strongest confirmed code path is the governed L3 movement chain from `v7-users-autoswitch.timer` through `tools/v7-governed-canary-dry-run-cycle` into `tools/v7-users-autoswitch --apply --verify`.
2. The repository clearly separates movement heartbeat from planner refresh heartbeat. Planner refresh alone does not move users.
3. Observation and health evidence are real code paths, but health truth is distributed across service matrix writers, intelligence snapshots, and Planner service truth classification.
4. L3 incident source continuity, retry-aware continuation, approved plan lock identity, restore barrier clearance, Runtime apply, Verification, Rollback, and Learning closure all have concrete code and tests.
5. Intelligence, shadow autonomy, analyzer/backtesting, and many admin execution views are mostly read-only/advisory; they should not be counted as production execution authority.
6. Production Maturity, Current Program State, Automation Debt, Workflow Debt, Pipeline Candidate registry, Owner Resolution execution, and automatic Engineering Report generation are weaker in code than in documentation.
7. Admin UI provides broad visibility and some action endpoints, but operator/execution visibility endpoints are explicitly read-only in tests and should not be treated as execution owners.

### 12. Step 1B Verdict

```text
PHASE_1_STEP_1B_CODE_REALITY_COLLECTION_COMPLETE
```

Step 1B is complete.

Step 2 consolidation is recommended.

Step 2 should treat the governed L3 chain as `CODE_CONFIRMED`, intelligence/admin/readiness models as mostly `CODE_PARTIAL` or read-only, and Current Program State/Production Maturity/debt registries as documented concepts with weak or missing code owners unless later evidence proves otherwise.

### 13. Next Step

Recommended next step:

```text
PHASE_1_STEP_2_CONSOLIDATE_DOCUMENTED_AND_CODE_REALITY_MODEL
```

Step 2 should consolidate Step 1 documentation knowledge with Step 1B code reality.

Step 2 must not:

- create `V7_IDEAL_AUTONOMOUS_SYSTEM_MODEL.md` unless explicitly authorized;
- create new architecture;
- create new owners;
- create OMP missions;
- modify Runtime, Planner, Authority, OMP, Current Program State, Production Maturity, or canonical docs;
- treat read-only admin/intelligence surfaces as execution authority;
- treat reports as runtime behavior.

## Phase 1 Step 1C — Full Function Graph Audit

### 1. Step Purpose

Create a structural function graph of the autonomous V7 code reality that is precise enough to draw visual diagrams later.

This step is read-only. It does not implement, refactor, fix bugs, deploy, move users, change timers, or modify Runtime, Planner, Authority, OMP, Current Program State, Production Maturity, or canonical documents.

### 2. Audit Method

The audit used the Step 1 and Step 1B source index, then inspected code under `tools/`, `tools/runtime-support/`, `admin/`, `admin_core/`, `systemd/`, `tests/unit/`, and `tests/contracts/`.

Commands used were read-only discovery commands:

```text
git status --short
find tools admin admin_core systemd tests -type f | sort
rg "def |class |ExecStart=|/api/operator|/api/execution|/api/omp|/api/runtime/convergence" tools admin admin_core systemd tests
rg targeted function names for Planner, Authority, Restore Barrier, Runtime Apply, Verification, Rollback, Learning, Safe Deploy, Truth, Convergence, Admin UI
sed selected function bodies and systemd units
```

Code files discovered in scope: `226`.

Raw function/class/API/systemd hits from discovery: `3831`.

Relevant autonomous functions, classes, scripts, services, timers, APIs, and test surfaces indexed in this Step 1C graph: `87`.

Tests were not run. Step 1C is a read-only structural audit; it only indexed existing test coverage.

### 3. Function Graph Scope

Included domains:

- Observation and Health Evidence
- Wake and Incident
- Diagnosis and OMP owner routing
- Authority and Packet Admission
- Planner, Candidate Selection, and Selected Move
- Approved Plan Lock and Restore Barrier
- Runtime Apply, Verification, Rollback, and Closure
- Learning, Feedback, and Intelligence Snapshots
- OMP, Current Program State, and Production Maturity projections
- Engineering Automation, Reports, Debt, Pipeline Candidates, and Owner Resolution
- Safe Deploy, Truth Check, and Convergence
- Admin UI and Operator Visibility

Excluded from durable graph conclusions:

- evidence-only shell scripts under historical report/evidence directories;
- tests as production behavior;
- reports as runtime state;
- admin UI displays as execution authority;
- documentation-only concepts without concrete code ownership.

### 4. Function Inventory

| ID | Path | Function / class / script / API | Domain | Type | Called by | Calls | Reads | Writes | Subprocesses | Input object | Output object | Downstream consumer | Mutation level | Authority role | Closure status | Test coverage | Autonomous role | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F001 | `systemd/v7-users-autoswitch.timer` | `v7-users-autoswitch.timer` | Runtime heartbeat | `SYSTEMD_TIMER` | systemd | triggers service | timer unit | none | systemd | time schedule | service trigger | F002 | `READ_ONLY` | none | `CLOSED_CHAIN` | `test_v7_sync_tools.py` | movement heartbeat entry | `OnUnitActiveSec=20s`. |
| F002 | `systemd/v7-users-autoswitch.service` | `ExecStart=/usr/local/bin/v7-governed-canary-dry-run-cycle ... --max-users 1` | Governed movement | `SYSTEMD_SERVICE` | F001 | F003 | unit env | none | F003 CLI | systemd activation | governed owner run | F003 | `READ_ONLY` until CLI mutates | invokes existing owner | `CLOSED_CHAIN` | `test_v7_sync_tools.py` | production movement entry | Real movement heartbeat. |
| F003 | `tools/v7-governed-canary-dry-run-cycle` | `main` | Governed owner | `CLI_SCRIPT` | F002 / operator CLI | F004, F006 | CLI args, state paths | result stdout | planner/apply subprocess via helpers | CLI args | transaction result | certification/operator | `UNKNOWN` wrapper | explicit confirmation gate | `CLOSED_CHAIN` | `test_governed_canary_cli.py` | governed L3 owner | Wrapper dispatch. |
| F004 | `tools/v7-governed-canary-dry-run-cycle` | `execute_l3_production_validation` | Governed owner | `FUNCTION` | F003 | F005, F006, F022, F024, F026, F027, F028, F042 | state dir, event dir, audit dir, lease, restore barrier | execution lease, audit, restore barrier via callees | indirect planner/apply | args, state/event/snapshot paths | `v7.l3-production-validation-execution.v1` | operator/certification | `AUTHORITY_GATE` | explicit confirmation + budget | `CLOSED_CHAIN` | `test_governed_canary_cli.py` | full governed L3 transaction | Central production validation function. |
| F005 | `tools/v7-governed-canary-dry-run-cycle` | `run_l3_production_validation_plan` | Planner bridge | `FUNCTION` | F004 | F029 CLI | state, events, snapshots, restore barrier | none directly | `v7-users-autoswitch --pre-planner-refresh ...` | max users/source | plan payload | F004/F024 | `READ_ONLY` | planning precondition | `CLOSED_CHAIN` | `test_governed_canary_cli.py` | gets Planner plan | Runs Planner, no apply. |
| F006 | `tools/v7-governed-canary-dry-run-cycle` | `run_autoswitch_apply` | Runtime bridge | `FUNCTION` | F004 | F029 CLI | args, packet identity | none directly | `v7-users-autoswitch --apply --verify` | approved identity, max users | apply payload | F004/F007 | `RUNTIME_MUTATION` through subprocess | approved identity required | `CLOSED_CHAIN` | `test_governed_canary_cli.py` | enters Runtime Apply | Passes packet id, operation id, selected hash, authority generation. |
| F007 | `tools/v7-governed-canary-dry-run-cycle` | `materialize_governed_transaction_feedback` | Feedback | `FUNCTION` | governed transaction path | feedback helpers | apply result, packet, operation | feedback records via caller path | none | transaction result | feedback rows | intelligence snapshots | `STATE_WRITER` when persisted by caller | none | `PARTIAL_CHAIN` | `test_governed_canary_cli.py` | learning materialization support | L3 direct path also uses F041. |
| F008 | `systemd/drafts/v7-autoswitch-planner.timer` | `v7-autoswitch-planner.timer` | Planner refresh | `SYSTEMD_TIMER` | systemd | F009 | timer unit | none | systemd | schedule | service trigger | F009 | `READ_ONLY` | none | `CLOSED_CHAIN` | forensic/test references | refresh heartbeat | Draft path in repo. |
| F009 | `systemd/drafts/v7-autoswitch-planner.service` | `ExecStart=/usr/local/bin/v7-users-autoswitch --pre-planner-refresh=write ...` | Planner refresh | `SYSTEMD_SERVICE` | F008 | F029/F055 | unit env | snapshot/state through subprocess | `v7-users-autoswitch`, `v7-intelligence-snapshot-refresh` | timer trigger | refreshed planner/intelligence state | Planner/admin | `STATE_WRITER` | no movement authority | `PARTIAL_CHAIN` | forensic/test references | refresh only | Does not invoke Runtime Apply. |
| F010 | `systemd/v7-service-matrix-refresh.service` | `ExecStart=/usr/local/bin/v7-service-matrix-refresh-all` | Health Evidence | `SYSTEMD_SERVICE` | service-matrix timer | F011 | unit env | none directly | F011 CLI | timer trigger | matrix refresh run | Planner/snapshots | `STATE_WRITER` via CLI | none | `CLOSED_CHAIN` | lock/sentinel tests | service matrix writer entry | Real health writer. |
| F011 | `tools/v7-service-matrix-refresh-all` | `main` | Health Evidence | `CLI_SCRIPT` | F010 / operator | F012, F013 | egress registry, state dir | service matrix/events | checker command | CLI args | refresh result | Planner/snapshots | `STATE_WRITER` | none | `CLOSED_CHAIN` | lock tests | service matrix refresh | Uses writer lock. |
| F012 | `tools/v7-service-matrix-refresh-all` | `service_matrix_writer_lock` | Health Evidence | `FUNCTION` | F011 | fcntl lock | `service-matrix.lock` | lock file metadata | none | state dir/timeout | lock acquisition | F013 | `STATE_WRITER` | serialization gate | `CLOSED_CHAIN` | lock tests | writer serialization | Prevents concurrent matrix writes. |
| F013 | `tools/v7-service-matrix-refresh-all` | `run_one` | Health Evidence | `FUNCTION` | F011 | checker command | egress id, checker, state dir | returns row | service checker | egress id | service test result | F011 | `READ_ONLY` itself | none | `CLOSED_CHAIN` | lock tests | per-egress probe | Writes happen in caller. |
| F014 | `systemd/v7-telegram-sentinel.service` | `ExecStart=/usr/local/bin/v7-telegram-sentinel --threshold-seconds 14 --timeout 1 --no-autoswitch` | Observation | `SYSTEMD_SERVICE` | telegram timer | F015 | unit env | none directly | F015 CLI | timer trigger | sentinel run | matrix/events | `STATE_WRITER` via CLI | no movement authority | `CLOSED_CHAIN` | `test_telegram_sentinel_lock_scope.py` | Telegram observation entry | Explicitly no autoswitch. |
| F015 | `tools/v7-telegram-sentinel` | `main` | Observation | `CLI_SCRIPT` | F014 / operator | F016, F017, F018, F019 | egress registry, matrix | sentinel JSON/events/matrix | optional autoswitch if flag not disabled | CLI args | sentinel payload | Planner/snapshots | `STATE_WRITER` | no authority under systemd | `CLOSED_CHAIN` | sentinel lock tests | Telegram sentinel | Movement hook dormant in service. |
| F016 | `tools/v7-telegram-sentinel` | `check_egress` | Observation | `FUNCTION` | F015 | `check_telegram`, `route_class_fitness` | egress row, prior matrix | returns item | socket probes | egress row/prior | egress Telegram item | F017/F018 | `READ_ONLY` | none | `CLOSED_CHAIN` | sentinel tests | probe producer | Per-egress probe. |
| F017 | `tools/v7-telegram-sentinel` | `update_matrix_items` | Health Evidence | `FUNCTION` | F015 | writer lock/write JSON | matrix file | matrix file | none | items | lifecycle result | Planner/snapshots | `STATE_WRITER` | none | `CLOSED_CHAIN` | sentinel tests | matrix writer | Lock scope optimized. |
| F018 | `tools/v7-telegram-sentinel` | `update_matrix` | Health Evidence | `FUNCTION` | F015/F017 | `update_matrix_items` | matrix file | matrix file | none | egress item | updated matrix | Planner/snapshots | `STATE_WRITER` | none | `CLOSED_CHAIN` | sentinel tests | single item writer | Wrapper. |
| F019 | `tools/v7-telegram-sentinel` | `run_autoswitch` | Dormant movement hook | `FUNCTION` | F015 only when not `--no-autoswitch` | autoswitch command | blocked items | none directly | autoswitch subprocess | blocked items | autoswitch result | none in systemd path | `UNKNOWN` | not authorized in service | `DORMANT` | sentinel tests around no-autoswitch | dormant hook | DORMANT_BY_SYSTEMD. |
| F020 | `tools/v7-service-matrix-test` | `main` | Verification | `CLI_SCRIPT` | F037 / matrix refresh | F021 | CLI args, state | optional matrix update | curl/probe subprocesses | user/egress/service args | rc/stdout/matrix row | Runtime verification | `STATE_WRITER` when update enabled | verification gate | `CLOSED_CHAIN` | autoswitch verification tests | service verification CLI | Real post-apply service check. |
| F021 | `tools/v7-service-matrix-test` | `update_matrix` | Health Evidence | `FUNCTION` | F020 | writer lock/write JSON | matrix file | matrix file | none | results | matrix update | Planner/snapshots | `STATE_WRITER` | none | `CLOSED_CHAIN` | service verify tests | matrix update from test | Shared evidence object. |
| F022 | `admin_core/operator_execution.py` | `packet_from_plan` | Packet / Identity | `FUNCTION` | F004 | F023, validation | plan | none | none | Planner plan | governance packet | F027 | `AUTHORITY_GATE` | dual approval packet | `CLOSED_CHAIN` | `test_operator_execution_packet.py`, `test_governed_canary_cli.py` | packet materializer | Includes rollback manifest and approved lock. |
| F023 | `admin_core/operator_execution.py` | `approved_plan_lock_from_selected` | Approved Plan Lock | `FUNCTION` | F022 | hash helpers | selected moves/packet | none | none | selected moves, packet hash | approved plan lock | F026/F028/F036 | `AUTHORITY_GATE` | identity lock | `CLOSED_CHAIN` | packet tests | immutable identity | `executor_may_reselect=False`. |
| F024 | `admin_core/operator_execution.py` | `create_execution_lease_from_packet` | Identity | `FUNCTION` | F004 | lease builder | packet, source preview | none | none | packet | lease object | F025/F004/F006 | `AUTHORITY_GATE` | overlap/identity guard | `CLOSED_CHAIN` | packet/governed tests | execution identity lease | Prevents overlap. |
| F025 | `admin_core/operator_execution.py` | `write_execution_lease` | Identity | `FUNCTION` | F004 | write JSON | lease file | lease file | none | lease | write result | F006/F028 | `STATE_WRITER` | lease gate | `CLOSED_CHAIN` | packet tests | lease writer | State mutation, not user movement. |
| F026 | `admin_core/operator_execution.py` | `runtime_recheck` | Authority / Recheck | `FUNCTION` | F027 | validators/hash checks | state dir, planner snapshot | none | none | packet/state | allow/deny recheck | F027 | `AUTHORITY_GATE` | fail-closed recheck | `CLOSED_CHAIN` | packet tests | packet admission | Ensures current sources match approved packet. |
| F027 | `admin_core/operator_execution.py` | `execute_packet` | Authority / Restore Barrier | `FUNCTION` | F004 / packet CLI | F026, F028 | audit store, state dir, packet | audit, restore barrier, lifecycle | none | packet | clearance result | F006/F036 | `AUTHORITY_GATE` + `STATE_WRITER` | packet consume and clearance | `CLOSED_CHAIN` | packet tests | admission + clearance | No user movement. |
| F028 | `admin_core/operator_execution.py` | `append_restore_barrier_clearance` | Restore Barrier | `FUNCTION` | F027 | F029 | restore barrier file | restore barrier file + backup | none | packet/recheck | clearance result | F036 | `STATE_WRITER` | restore barrier gate | `CLOSED_CHAIN` | packet tests | clearance writer | Duplicate owner guard. |
| F029 | `admin_core/operator_execution.py` | `build_restore_barrier_clearance` | Restore Barrier | `FUNCTION` | F028 | hash/stable id | packet | none | none | packet | clearance object | F028/F036 | `AUTHORITY_GATE` | identity + budget clearance | `CLOSED_CHAIN` | packet tests | clearance object builder | Embeds approved plan lock. |
| F030 | `admin_core/operator_execution.py` | `finish_execution_lease` | Closure | `FUNCTION` | F004 | write lease terminal | lease file | lease file | none | terminal operation | terminalized lease | operator/audit | `STATE_WRITER` | closure of active lease | `CLOSED_CHAIN` | packet/governed tests | execution closure | Releases duplicate guard. |
| F031 | `tools/v7-users-autoswitch` | `main` | Planner / Runtime | `CLI_SCRIPT` | F005/F006/F009/operator | Planner object methods | state files, policy, args | plan/audit/safety via methods | switch/verify/service test via methods | CLI args | plan JSON | governed owner/admin/operator | `UNKNOWN` dispatch | mode-dependent | `CLOSED_CHAIN` | autoswitch policy tests | Planner/Runtime CLI | One binary owns observe and apply modes. |
| F032 | `tools/v7-users-autoswitch` | `Planner._decision_for_user` | Planner | `FUNCTION` | plan generation | F033/F034/F039 | users, egress, policy/evidence | none | none | User | decision row | F039 | `READ_ONLY` | none | `CLOSED_CHAIN` | autoswitch policy tests | decision producer | Emits keep/switch/failover. |
| F033 | `tools/v7-users-autoswitch` | `Planner._candidate` | Candidate Selection | `FUNCTION` | F032 | F034-F038 | egress/evidence/policy | none | none | user+egress+services | Candidate | F032 | `READ_ONLY` | none | `CLOSED_CHAIN` | autoswitch tests | candidate builder | Runs all gates. |
| F034 | `tools/v7-users-autoswitch` | `_gate_basic`, `_gate_reservation`, `_gate_org`, `_gate_quality`, `_gate_service`, `_gate_load`, `_gate_safety` | Candidate gates | `FUNCTION` | F033 | `_block`, evidence helpers | candidate/evidence/policy | candidate object mutation only | none | Candidate | eligible/blockers/reasons | F033/F032 | `READ_ONLY` externally | planning gate | `CLOSED_CHAIN` | autoswitch tests | eligibility gates | In-memory mutation only. |
| F035 | `tools/v7-users-autoswitch` | `_service_truth_classification`, `_service_truth_freshness` | Health Evidence | `FUNCTION` | `_service_suitability`/F034 | freshness helpers | service matrix rows | none | none | service row | truth class | F034 | `READ_ONLY` | freshness gate | `CLOSED_CHAIN` | autoswitch tests | service truth gate | Determines stale/persistent/transient. |
| F036 | `tools/v7-users-autoswitch` | `_l3_incident_context` | Wake / Incident | `FUNCTION` | plan generation | incident key helpers | gate evidence, selected moves, generation | incident safety object in plan | none | gate+selected | incident context | F037/F041 | `READ_ONLY` | incident gate | `CLOSED_CHAIN` | autoswitch tests | incident materializer | Incident source and key producer. |
| F037 | `tools/v7-users-autoswitch` | `_select_moves` | Selected Move | `FUNCTION` | Planner plan generation | F038 | decisions, authority budget, incident context | selected moves in plan | none | decisions | selected moves | F022/F036/F040 | `READ_ONLY` | blast-radius budget | `CLOSED_CHAIN` | autoswitch tests | move selector | Raises failover cap only through governed authority. |
| F038 | `tools/v7-users-autoswitch` | `_pick_projected_moves` | Selected Move | `FUNCTION` | F037 | retry budget helpers, target projection | decisions/projected load/incident | selected list | none | candidate decisions | picked moves | F037 | `READ_ONLY` | retry/budget filter | `CLOSED_CHAIN` | autoswitch tests | retry-aware picker | Excludes exhausted semantic attempts. |
| F039 | `tools/v7-users-autoswitch` | authority budget and promotion functions | Authority | `FUNCTION` | plan/promotion commands | F050 | policy, evidence, truth | policy/report state depending command | `v7-truth-check` | authority policy/evidence | budget/readiness/promotion verdict | F037/F004 | `AUTHORITY_GATE` | authority budget | `CLOSED_CHAIN` | autoswitch tests | authority budget owner | Includes canonical ladder. |
| F040 | `tools/v7-users-autoswitch` | `Planner.apply` | Runtime Apply | `FUNCTION` | F031 in `--apply` mode | F041, F042, F043, `_run_switch` | plan, restore barrier, approved lock, state | safety/audit via finalization | `v7-user-switch`, route/service checks | approved plan | apply result | F041/F004 | `RUNTIME_MUTATION` | restore barrier + eligibility required | `CLOSED_CHAIN` | autoswitch tests | runtime mutation boundary | User movement happens here. |
| F041 | `tools/v7-users-autoswitch` | `finalize_operation` | Closure | `FUNCTION` | F031 after plan/apply | F044 | plan/apply result | audit if apply | none | plan | terminal operation/audit/closure | F004/admin/learning | `REPORT_WRITER` / audit writer | terminal classification | `CLOSED_CHAIN` | autoswitch tests | operation closure | Adds `l3_learning_closure`. |
| F042 | `tools/v7-users-autoswitch` | `_verify_routes_for_apply` | Verification | `FUNCTION` | F040 | route-check command | user/target scope | none | `v7-user-route-check` | selected user/target | rc/stdout | F040 | `READ_ONLY` | verification gate | `CLOSED_CHAIN` | autoswitch tests | route verification | Scoped in emergency mode. |
| F043 | `tools/v7-users-autoswitch` | `_verify_emergency_required_services` | Verification | `FUNCTION` | F040 | F020 CLI | selected move/services | none | `v7-service-matrix-test` | selected move | rc/stdout | F040 | `READ_ONLY` | service verification gate | `CLOSED_CHAIN` | autoswitch tests | service verification | Failure triggers rollback. |
| F044 | `tools/v7-users-autoswitch` | `_l3_materialize_learning_closure` | Learning | `FUNCTION` | F041 | feedback/audit append helpers | plan, incident, operation, apply results | feedback/closure records when apply | none | terminal plan | learning closure | snapshots/admin/certification | `STATE_WRITER` | none | `CLOSED_CHAIN` | autoswitch tests | terminal learning writer | Writes outcome/trust/prediction/recommendation/closure evidence. |
| F045 | `tools/v7-intelligence-snapshot-refresh` | `main` | Intelligence | `CLI_SCRIPT` | F009/F005 pre-refresh/operator | F046, F047 | state/audit/event files | intelligence snapshots | none | CLI args | snapshot refresh result | Planner/admin | `STATE_WRITER` | no runtime authority | `CLOSED_CHAIN` | intelligence worker tests | snapshot refresh entry | Writes only snapshots. |
| F046 | `tools/v7-intelligence-snapshot-refresh` | `load_inputs` | Intelligence | `FUNCTION` | F047/F045 | read registries/json/jsonl | service matrix, quality, prefs, audit, history | none | none | paths | input bundle | F047 | `READ_ONLY` | none | `CLOSED_CHAIN` | intelligence tests | snapshot input loader | Consumes rotated JSONL. |
| F047 | `tools/v7-intelligence-snapshot-refresh` | `build_stable_snapshot_run` | Intelligence | `FUNCTION` | F045 | F048 | input files | none directly | none | state/audit paths | WorkerRunResult | F045/write snapshots | `READ_ONLY` until caller writes | source consistency gate | `CLOSED_CHAIN` | intelligence tests | stable snapshot builder | Retries source changes. |
| F048 | `admin_core/intelligence_workers.py` | `build_all_snapshots` | Intelligence | `FUNCTION` | F047 | F049-F054 | input bundle | none | none | evidence bundle | snapshot families | F045/Planner/Admin | `ADVISORY_ONLY` | no runtime authority | `CLOSED_CHAIN` | `test_intelligence_workers.py` | snapshot orchestrator | Builds 11 families. |
| F049 | `admin_core/intelligence_workers.py` | `build_service_score_snapshots` | Intelligence / Health | `FUNCTION` | F048 | service intelligence helpers | service matrix/quality/preferences | none | none | health evidence | service/channel scores | Planner/advisory/admin | `ADVISORY_ONLY` | no runtime authority | `CLOSED_CHAIN` | intelligence tests | health read model | Snapshot only. |
| F050 | `admin_core/intelligence_workers.py` | `build_trust_snapshot` | Trust | `FUNCTION` | F048 | trust model | audit/switch/rollback records | none | none | history records | trust summary | blast/risk/advisory | `ADVISORY_ONLY` | no runtime authority | `CLOSED_CHAIN` | intelligence tests | trust read model | Bounded history. |
| F051 | `admin_core/intelligence_workers.py` | `build_candidate_suitability_snapshot` | Planner intelligence | `FUNCTION` | F048 | `RoutingBrain` | users/egress/service/trust/risk/blast | none | none | snapshots/registries | candidate suitability | best pool/admin/planner advisory | `ADVISORY_ONLY` | no runtime authority | `CLOSED_CHAIN` | intelligence tests | suitability read model | Advisory only. |
| F052 | `admin_core/intelligence_workers.py` | `build_best_available_pool_snapshot` | Planner intelligence | `FUNCTION` | F048 | `RoutingBrain.best_available_pool_advice` | candidate suitability/runtime/egress | none | none | snapshot | pool advice | Planner/advisory/admin | `ADVISORY_ONLY` | no runtime authority | `CLOSED_CHAIN` | intelligence tests | pool read model | No single-best authority. |
| F053 | `admin_core/intelligence_workers.py` | `build_trust_evolution_snapshot` | Learning | `FUNCTION` | F048 | F054 | feedback/audit/snapshots | none | none | decision records | trust evolution | Admin/learning read model | `ADVISORY_ONLY` | no runtime authority | `CLOSED_CHAIN` | intelligence tests | learning consumer | Consumes feedback evidence. |
| F054 | `admin_core/operator_execution_feedback.py` | `decision_outcome_learning_model` | Learning | `FUNCTION` | F053 / admin | quality helpers | closed feedback records | none | none | decision records | learning model | trust evolution/admin | `ADVISORY_ONLY` | none | `CLOSED_CHAIN` | feedback/intelligence tests | learning read model | Aggregates closed outcomes. |
| F055 | `admin_core/routing_brain.py` | `RoutingBrain` | Planner intelligence | `CLASS` | F051/admin/routing tests | score/advice methods | service matrix/quality/preferences | none | none | evidence inputs | advice rows | snapshots/admin | `ADVISORY_ONLY` | no runtime authority | `CLOSED_CHAIN` | routing tests | advisory brain | Does not write selected moves. |
| F056 | `admin_core/operator_execution_pipeline.py` | `EXECUTION_LOOP_STAGES` | OMP owner routing | `DATA_SCHEMA` | tests/admin | none | static module | none | none | none | stage map | admin/readiness | `READ_ONLY` | none | `READ_ONLY_TERMINAL` | pipeline tests | diagram source | Static contract. |
| F057 | `admin_core/operator_execution_pipeline.py` | `governed_canary_knowledge_gated_dry_run_cycle` | Operator Pipeline | `FUNCTION` | governed transaction path/admin | packet preview helpers | events, decision surface, lease | none | none | event/surface/lease | packet preview/stop reason | packet materialization/admin | `ADVISORY_ONLY` | authority boundary preview | `PARTIAL_CHAIN` | pipeline/governed tests | preview pipeline | Read-only preview in generic canary path. |
| F058 | `admin_core/operator_execution_pipeline.py` | `l3_production_validation_runtime_action_transition` | Authority transition | `FUNCTION` | F004 | validation helpers | plan/max users | none | none | plan | transition verdict | F022 | `AUTHORITY_GATE` | transition gate | `CLOSED_CHAIN` | governed tests | runtime action admission | Ensures L3 move scope. |
| F059 | `admin_core/operator_execution_pipeline.py` | `pipeline_certification` | Engineering automation | `FUNCTION` | admin/tests | static checks | static contracts | none | none | none | certification payload | admin/tests | `READ_ONLY` | none | `READ_ONLY_TERMINAL` | pipeline tests | pipeline read model | Not execution. |
| F060 | `admin/v7-admin-api` | `GET /api/operator/*` | Operator Visibility | `API_ENDPOINT` | browser/operator | F061/F062 | state/evidence/audit via views | none | none | HTTP query | JSON view | admin UI | `READ_ONLY` | none | `READ_ONLY_TERMINAL` | endpoint/operator tests | operator visibility | GET-only namespace per tests. |
| F061 | `admin_core/operator_views.py` | facade functions | Operator Visibility | `FUNCTION` | F060 | F062 | repo/state/event paths | none | none | paths/query | view payload | F060 | `READ_ONLY` | none | `READ_ONLY_TERMINAL` | operator tests | thin facade | No execution. |
| F062 | `admin_core/operator_observability.py` | `build_operator_view_model`, `build_operator_operation_detail`, `audit_search`, `execution_governance_preview` | Operator Visibility | `FUNCTION` | F061/F060 | evidence readers/redaction | reports/audit/evidence | none | none | repo/operation query | read-only payload | F060/admin UI | `READ_ONLY` | none | `READ_ONLY_TERMINAL` | operator tests | visibility/evidence graph | Displays, does not execute. |
| F063 | `admin/v7-admin-api` | `GET /api/execution/*` | Admin UI | `API_ENDPOINT` | browser/operator | execution view builders | state/evidence/contracts | none | none | HTTP query | JSON view | admin UI | `READ_ONLY` | none | `READ_ONLY_TERMINAL` | endpoint tests | execution dashboard | Display/readiness only. |
| F064 | `admin/v7-admin-api` | `GET /api/omp/dashboard` | OMP Visibility | `API_ENDPOINT` | browser/operator | OMP dashboard builder | docs/state/evidence | none | none | HTTP query | dashboard JSON | admin UI/human | `READ_ONLY` | none | `READ_ONLY_TERMINAL` | endpoint tests | OMP projection | Not an OMP executor. |
| F065 | `admin/v7-admin-api` | `GET /api/runtime/convergence` | Convergence Visibility | `API_ENDPOINT` | browser/operator | convergence helpers | runtime/local truth | none | none | HTTP query | convergence JSON | admin UI/human | `READ_ONLY` | none | `READ_ONLY_TERMINAL` | endpoint tests | convergence display | Read-only. |
| F066 | `tools/v7-truth-check` | `main` / `combine_results` | Truth Check | `CLI_SCRIPT` | operator/F039/F068 | local/github/runtime truth functions | manifest, git, runtime snapshot/read-only cmds | none | read-only git/runtime commands | mode args | truth result | F067/F068/F039 | `READ_ONLY` | truth gate | `CLOSED_CHAIN` | `test_v7_truth_check.py` | fail-closed truth owner | No mutating commands allowed by tests. |
| F067 | `tools/v7_sync_lib.py` | `truth_check` | Truth Check | `FUNCTION` | F068/F069 | F066 module | manifest | none | read-only command runner | mode | truth dict | convergence/deploy | `READ_ONLY` | truth gate | `CLOSED_CHAIN` | sync/truth tests | library truth adapter | Loads truth module. |
| F068 | `tools/v7_sync_lib.py` | `convergence_status` | Convergence | `FUNCTION` | F070/F065 | F067, git/deploy delta helpers | git/runtime manifest | none | read-only git/runtime via runner | runner | convergence dict | F069/F070/admin | `READ_ONLY` | convergence guard | `CLOSED_CHAIN` | sync tests | convergence owner core | Computes safe next command. |
| F069 | `tools/v7_sync_lib.py` | `convergence_owner_status` | Convergence | `FUNCTION` | F070 | F068 | convergence result | none | none | runner | owner next action | operator/admin | `READ_ONLY` | next action owner | `CLOSED_CHAIN` | sync tests | single next action | Operator-facing. |
| F070 | `tools/v7-convergence-owner` | `main` | Convergence | `CLI_SCRIPT` | operator/admin | F069 | none | stdout only | none | CLI args | JSON/status | operator/human | `READ_ONLY` | convergence owner | `READ_ONLY_TERMINAL` | sync tests | convergence CLI | No mutation. |
| F071 | `tools/v7-safe-deploy` | `main` | Safe Deploy | `CLI_SCRIPT` | operator/Codex approved path | F072 | deploy manifest/truth | production files if apply | ssh/scp/system commands through sync lib | apply/confirm flags | deploy result | production/runtime truth | `DEPLOYMENT_MUTATION` when apply | deploy confirmation required | `CLOSED_CHAIN` | sync tests | safe deploy owner | Not invoked in Step 1C. |
| F072 | `tools/v7_sync_lib.py` | `safe_deploy_plan` | Safe Deploy | `FUNCTION` | F071 | F067, deploy helpers | local files, manifest, github truth | remote/runtime files if apply | ssh/cp/system actions via runner | apply/confirm | deploy plan/result | truth/convergence | `DEPLOYMENT_MUTATION` when apply | deploy gate | `CLOSED_CHAIN` | sync tests | deploy implementation | Requires confirmation. |
| F073 | `admin_core/intelligence_platform.py` | `production_convergence_audit`, `deploy_readiness_audit`, `production_shadow_execution_pipeline` | Analyzer / Backtesting | `FUNCTION` | tests/admin future | model helpers | provided model inputs | none | none | model args | advisory payload | tests/admin | `ADVISORY_ONLY` | no runtime authority | `PARTIAL_CHAIN` | intelligence platform tests | future framework | Not a blocking production owner. |
| F074 | `admin_core/shadow_autonomy.py` | `build_shadow_autonomy_model` | Continuous Self Evolution | `FUNCTION` | admin/tests | shadow helpers | decision surface/history | none | none | decision/history | shadow model | admin/operator | `ADVISORY_ONLY` | none | `PARTIAL_CHAIN` | shadow tests | comparison model | Needs operator comparisons. |
| F075 | `tools/v7-autonomy-trust-evidence-inventory` | `main` | Autonomy inventory | `CLI_SCRIPT` | operator/research | inventory readers | state/audit/events | stdout only | none | CLI args | inventory JSON | human/reports | `READ_ONLY` | none | `UNKNOWN` | acceleration tests indirect | evidence inventory | No production invocation found. |
| F076 | `tools/v7-safe-commit` | `main` | Engineering workflow | `CLI_SCRIPT` | operator/Codex | sync lib | git status | git commit if apply | git | CLI args | commit result | GitHub/deploy | `REPORT_WRITER` / git mutation | local workflow gate | `CLOSED_CHAIN` | sync tests | safe commit helper | Outside runtime. |
| F077 | `tools/v7-safe-push` | `main` | Engineering workflow | `CLI_SCRIPT` | operator/Codex | sync lib | git/remote | git push if apply | git | CLI args | push result | GitHub/truth | `REPORT_WRITER` / git mutation | local workflow gate | `CLOSED_CHAIN` | sync tests | safe push helper | Outside runtime. |
| F078 | `tools/v7-egress-quality-compact` | `main` | Health Evidence | `CLI_SCRIPT` | `v7-egress-quality-compact.service` | compaction helpers | quality/service matrix/restore barrier | quality summary | none | state dir | compacted quality | Planner/snapshots | `STATE_WRITER` | pauses on active restore barrier | `CLOSED_CHAIN` | `test_egress_quality_compact_lifecycle.py` | quality compactor | Protects restore barrier window. |
| F079 | `tools/v7-autoswitch-safety-review` | `main` | Safety review | `CLI_SCRIPT` | operator | review helpers | policy/state/matrix | report stdout | none | paths | safety review | human/Codex | `READ_ONLY` | advisory only | `READ_ONLY_TERMINAL` | safety/design tests | safety audit | Not Runtime gate unless consumed manually. |
| F080 | `tools/v7-infrastructure-readiness-review` | `main` | Infrastructure review | `CLI_SCRIPT` | operator | parser helpers | systemd/registry | report stdout | none | paths | readiness review | human/Codex | `READ_ONLY` | advisory only | `READ_ONLY_TERMINAL` | infra tests | readiness audit | Not automatic certification owner. |
| F081 | `tools/v7-operator-execution-packet` | CLI wrapper | Packet | `CLI_SCRIPT` | operator | `admin_core.operator_execution.main` | packet/plan/preview | packet/audit/clearance depending mode | none | CLI args | packet/validation/clearance result | governed/operator | `AUTHORITY_GATE` | packet owner CLI | `CLOSED_CHAIN` | packet tests | packet CLI | Wrapper around F022/F027. |
| F082 | `tests/unit/test_v7_users_autoswitch_policy.py` | L3 policy tests | Tests | `TEST` | unittest | Planner functions | fixtures/tmp state | tmp files | mocked subprocess | test fixture | assertions | developers | `READ_ONLY` | no production authority | `TEST_ONLY` | self | regression proof | Tests are not production behavior. |
| F083 | `tests/unit/test_governed_canary_cli.py` | governed owner tests | Tests | `TEST` | unittest | F003-F007 | fixtures/tmp state | tmp files | mocked subprocess | test fixture | assertions | developers | `READ_ONLY` | no production authority | `TEST_ONLY` | self | governed regression | Strong proof of linkage. |
| F084 | `tests/unit/test_operator_execution_packet.py` | packet/lease/restore tests | Tests | `TEST` | unittest | F022-F030 | fixtures/tmp state | tmp files | none/mocked | test fixture | assertions | developers | `READ_ONLY` | no production authority | `TEST_ONLY` | self | identity regression | Strong lock coverage. |
| F085 | `tests/unit/test_intelligence_workers.py` | intelligence snapshot tests | Tests | `TEST` | unittest | F048-F054 | fixtures/tmp | tmp snapshots | subprocess in CLI tests | test fixture | assertions | developers | `READ_ONLY` | no production authority | `TEST_ONLY` | self | snapshot regression | Advisory/read-model coverage. |
| F086 | `tests/unit/test_v7_sync_tools.py` / `test_v7_truth_check.py` | sync/truth tests | Tests | `TEST` | unittest | F066-F072 | fixtures/fake runner | tmp files | fake runner | test fixture | assertions | developers | `READ_ONLY` | no production authority | `TEST_ONLY` | self | deploy/truth regression | Confirms fail-closed and safe commands. |
| F087 | `tests/contracts/endpoint_inventory_test.py` | endpoint inventory contract | Tests | `TEST` | unittest | admin API source | admin API file | none | py_compile | admin source | assertions | developers | `READ_ONLY` | no production authority | `TEST_ONLY` | self | admin endpoint contract | Freezes visibility surface. |

### 5. Function Call Graph By Chain

| Chain name | Entry point | Function sequence | State objects passed | State objects written | Terminal output | Downstream consumer | Chain status | Main missing edge |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A. Observation / Health Evidence | F010/F014 | F010 -> F011 -> F012/F013 and F014 -> F015 -> F016 -> F017/F018 | egress registry, service matrix, quality summary, event records | service matrix, Telegram sentinel state, service events, quality summary via F078 | health evidence | Planner F031/F035, snapshots F045/F048, admin views | `FULLY_CLOSED` | Unified health owner is distributed across multiple scripts. |
| B. Wake / Incident | F031 plan generation | F035 -> F032/F033/F034 -> F037 -> F036 | service truth, decisions, selected moves, emergency gate | incident context in plan; incident record through Runtime path | L3 incident context/key/source | Runtime apply F040, learning F044 | `FULLY_CLOSED` | Diagnosis of incident producer remains report-led. |
| C. Planner / Candidate / Decision | F031 observe/guarded | F032 -> F033 -> F034/F035 -> F037/F038 | users, egress, policies, matrix, snapshots, authority budget | planner plan selected moves | decisions and selected moves | packet F022 or apply F040 | `FULLY_CLOSED` | None for L3 governed chain. |
| D. Authority / Packet / Identity | F004 | F004 -> F058 -> F022 -> F023 -> F024/F025 -> F027/F026 -> F028/F029 | plan, selected moves, authority budget, source hashes | governance packet, approved plan lock, execution lease, audit, restore barrier clearance | clearance + locked identity | Runtime apply F006/F040 | `FULLY_CLOSED` | Generic canary preview path remains read-only unless transaction path explicitly runs. |
| E. Runtime Apply / Verification / Rollback | F006/F031 apply | F006 -> F031 -> F040 -> `_run_switch` -> F042/F043 -> rollback `_run_switch` if needed -> F041 | approved identity, restore barrier, selected moves, rollback manifest | production route/user mutation, safety/audit, terminal operation | apply/verification/rollback result | F004/F041/F044 | `FULLY_CLOSED` | None for governed L3 path; real service failures still terminate through rollback. |
| F. Learning / Feedback / Intelligence | F041/F044/F045 | F041 -> F044 -> feedback records -> F045 -> F047 -> F048 -> F049-F054 | terminal operation, apply rows, feedback records, audit/history | feedback/closure records, intelligence snapshots | trust evolution / decision learning | admin read models, future Planner advisory | `PARTIALLY_CLOSED` | Learning influences snapshots/advisory; automatic capability/Current Program State sync not closed. |
| G. OMP / Current Program State / Production Maturity | F064/admin docs | reports/docs -> F064 dashboard projection | docs/reports/current state | none found in code | OMP dashboard view | human/Codex | `PARTIALLY_CLOSED` | No executable OMP mission continuation, Current Program State writer, or Production Maturity writer found. |
| H. Engineering Automation / Reports / Debt | F059/F073/F075 plus reports | analyzer/read-model helpers -> reports/manual updates | evidence and models | reports by Codex/human | automation/readiness evidence | human/Codex | `PARTIALLY_CLOSED` | No automatic Engineering Report, Automation Debt, Workflow Debt, Pipeline Candidate registry writer found. |
| I. Admin UI / Operator Visibility | F060/F063/F064/F065 | admin API -> F061/F062/read-model helpers | state, audit, evidence, docs | none for GET views | JSON dashboard | operator/human | `CLOSED_TO_READ_ONLY` | Visibility is not execution authority. |
| J. Safe Deploy / Truth / Convergence | F066/F070/F071 | F066 -> F067 -> F068 -> F069/F070 and F071 -> F072 -> F067 | manifest, git, runtime fingerprint/snapshot, deploy allowlist | deploy files only when approved apply | truth/convergence/deploy result | operator/Authority promotion/safe deploy | `FULLY_CLOSED` | Production runtime access depends on environment/approval. |

### 6. Producer / Consumer Graph

| Producer function | Output produced | Storage path or return object | Consumer function | Consumer domain | Automatic consumption? | Human/Codex consumption? | Status | Gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F017/F018 | service matrix items | `/opt/v7/egress/state/service-matrix.json` | F035, F045/F049, F020 | Health/Planner/Verification | YES | YES | `CONSUMED_AUTOMATICALLY` | Distributed health semantics. |
| F011/F013 | service-matrix refresh result | service matrix/events | F035/F045 | Health/Planner | YES | YES | `CONSUMED_AUTOMATICALLY` | None for Planner. |
| F078 | compacted quality summary | `/opt/v7/egress/state/egress-quality-summary.json` | F035/F045 | Health/Planner/Intelligence | YES | YES | `CONSUMED_AUTOMATICALLY` | Compaction is separate owner. |
| F045/F048 | intelligence snapshots | `/opt/v7/egress/state/intelligence/*` | F031, admin UI/read models | Intelligence/Planner | YES | YES | `CONSUMED_AUTOMATICALLY` | Advisory authority only. |
| F032/F037 | planner decisions/selected moves | plan return object/stdout | F022/F040/F036 | Planner/Packet/Runtime | YES | YES | `CONSUMED_AUTOMATICALLY` | None in governed path. |
| F036 | L3 incident context | plan `safety.l3_incident` | F040/F044 | Incident/Runtime/Learning | YES | YES | `CONSUMED_AUTOMATICALLY` | Incident diagnosis reports are manual. |
| F022 | governance packet | packet object / optional file via CLI | F027/F024/F006 | Packet/Authority/Runtime | YES | YES | `CONSUMED_AUTOMATICALLY` | Requires approved execution path. |
| F023 | approved plan lock | packet.approved_plan_lock | F028/F040 | Identity/Restore/Runtime | YES | YES | `CONSUMED_AUTOMATICALLY` | None. |
| F025 | execution lease | `/opt/v7/egress/state/operator-execution-lease.json` | F004/F006/F030 | Identity/overlap | YES | YES | `CONSUMED_AUTOMATICALLY` | None. |
| F028 | restore barrier clearance | `/opt/v7/egress/state/autoswitch-restore-barrier.json` | F040 | Restore/Runtime | YES | YES | `CONSUMED_AUTOMATICALLY` | None. |
| F040 | runtime apply result | plan `apply_result` stdout/audit | F041/F044/F004 | Runtime/Closure/Learning | YES | YES | `CONSUMED_AUTOMATICALLY` | None. |
| F042/F043 | verification result | apply row rc/stdout | F040 | Verification/Rollback | YES | YES | `CONSUMED_AUTOMATICALLY` | Service probe detail can be timeout/failure. |
| F040 rollback branch | rollback result | apply row rollback fields | F041/F044 | Rollback/Learning | YES | YES | `CONSUMED_AUTOMATICALLY` | None. |
| F044 | feedback/learning closure | execution feedback JSONL / closure records | F045/F053/F054 | Learning/Intelligence | YES | YES | `CONSUMED_AUTOMATICALLY` | Current Program State/Production Maturity sync missing. |
| F053/F054 | trust evolution/decision learning | intelligence snapshots/read model | admin UI / Planner advisory | Learning/Advisory | YES | YES | `CONSUMED_AUTOMATICALLY` | Not a direct authority grant. |
| F062 | operator views | HTTP JSON | browser/operator | Visibility | YES via UI | YES | `READ_ONLY_DISPLAY` | Not execution. |
| F064 | OMP dashboard | HTTP JSON | browser/operator | OMP visibility | YES via UI | YES | `READ_ONLY_DISPLAY` | No mission executor. |
| F066/F068/F069 | truth/convergence status | CLI/JSON result | Authority promotion, operator, safe deploy | Truth/Deploy | YES where invoked | YES | `CONSUMED_AUTOMATICALLY` | Runtime access can be unavailable. |
| Codex/human reports | engineering report | `docs/reports/engineering/*` | human/Codex, sometimes admin evidence index | Reports | NO | YES | `CONSUMED_BY_CODEX` | No automatic report writer found. |
| Codex/human Current Program State update | Current Program State | `docs/programs/V7_CURRENT_PROGRAM_STATE.md` | human/Codex/OMP | Current Program State | NO | YES | `CONSUMED_BY_HUMAN` | No code writer found. |
| Codex/human maturity update | Production Maturity state/docs | docs/reference/program files | human/Codex/OMP | Production Maturity | NO | YES | `CONSUMED_BY_HUMAN` | No code writer found. |
| Codex/human debt records | automation/workflow debt | reports/docs | human/Codex | Automation/Workflow | NO | YES | `CONSUMED_BY_CODEX` | No registry writer found. |

### 7. State File Graph

| State / evidence object | Storage path | Producer | Consumer | Freshness rule | Authority relevance | Mutation relevance | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| service matrix | `/opt/v7/egress/state/service-matrix.json` | F011/F017/F020 | F035/F045/F049/F043 | service truth fresh/stale/expired policy in F035 | Required for L3 evidence and verification | state file | `CODE_CONFIRMED` |
| quality summary | `/opt/v7/egress/state/egress-quality-summary.json` | F078 / quality tools | F035/F045/F049 | quality policy metrics freshness | candidate quality gate | state file | `CODE_CONFIRMED` |
| event records | `/opt/v7/events/*.jsonl` | F015/F011/other runtime tools | F003/F045/admin | bounded JSONL tail; event collapse in L3 | wake/incident evidence | event file | `CODE_CONFIRMED` |
| intelligence snapshots | `/opt/v7/egress/state/intelligence/*` | F045/F048 | F031/admin/F051-F053 | snapshot freshness state in envelopes | advisory and authority evidence | state file | `CODE_CONFIRMED` |
| planner plan | CLI return object/stdout | F031/F005 | F004/F022/F040 | generation/source hashes | basis for authority and apply | return object | `CODE_CONFIRMED` |
| selected moves | plan `selected_moves` | F037/F038 | F022/F023/F040 | selected move hash/generation | core identity object | return object | `CODE_CONFIRMED` |
| governance packet | packet object / optional packet file | F022/F081 | F027/F024 | packet TTL/dual approval | Authority admission | packet object/file | `CODE_CONFIRMED` |
| approved plan lock | packet `approved_plan_lock` | F023 | F028/F040 | packet expiry/generation/hash | Identity lock | embedded object | `CODE_CONFIRMED` |
| execution lease | `/opt/v7/egress/state/operator-execution-lease.json` | F025 | F004/F006/F030 | lease TTL/status | overlap/identity guard | state file | `CODE_CONFIRMED` |
| restore barrier clearance | `/opt/v7/egress/state/autoswitch-restore-barrier.json` | F028 | F040/F078 | clearance expiry/generation token | mandatory Runtime apply gate | state file | `CODE_CONFIRMED` |
| rollback manifest | packet `rollback_manifest` | F022 | F040 rollback/F041/F044 | operation-scoped | rollback readiness | embedded object | `CODE_CONFIRMED` |
| runtime apply result | plan `apply_result` | F040 | F041/F044/F004 | terminal operation | Capability proof | return/audit object | `CODE_CONFIRMED` |
| verification result | apply row `verify_rc`/`service_verify_rc` | F042/F043 | F040/F041/F044 | immediate post-apply | success/rollback gate | return object | `CODE_CONFIRMED` |
| rollback result | apply row rollback fields | F040 | F041/F044 | immediate on failed verification | closure/safety | runtime mutation result | `CODE_CONFIRMED` |
| operation audit | audit JSONL / plan audit | F041/F027 | admin/evidence/intelligence | append-only | proof/evidence | audit file | `CODE_CONFIRMED` |
| learning closure | feedback/closure records | F044/F007 | F045/F053/F054 | closed terminal only | certification evidence | learning file | `CODE_CONFIRMED` |
| decision feedback | feedback JSONL | F044/F007 | F054/F053 | bounded history | trust/readiness | learning file | `CODE_CONFIRMED` |
| trust evolution | intelligence snapshot | F053 | admin/Planner advisory | snapshot freshness | advisory only | state file | `CODE_CONFIRMED` |
| OMP dashboard | admin JSON projection | F064 | browser/human | request-time/read model | no direct authority | read-only | `CODE_PARTIAL` |
| Current Program State | `docs/programs/V7_CURRENT_PROGRAM_STATE.md` | human/Codex | human/Codex/OMP | document timestamp | current state only | doc file | `DOC_ONLY` |
| Production Maturity state | docs/reference/program reports | human/Codex | human/Codex | report/doc freshness | maturity consumer | doc/report | `DOC_ONLY` |
| engineering report | `docs/reports/engineering/*` | human/Codex | human/Codex/admin evidence index | timestamped report | evidence only | report file | `DOC_ONLY` as writer |
| automation debt record | reports/docs | human/Codex | human/Codex | none found in code | no direct authority | report/doc | `DOC_ONLY` |
| workflow debt record | reports/docs | human/Codex | human/Codex | none found in code | no direct authority | report/doc | `DOC_ONLY` |
| pipeline candidate record | reports/docs/read models | human/Codex/admin views | human/Codex | none found in code | no direct authority | report/doc | `CODE_PARTIAL` |
| safe deploy manifest | deploy manifest/runtime fingerprint | F072/sync tooling | F066/F068/F071 | truth check | deployment gate | deploy file | `CODE_CONFIRMED` |
| truth check result | CLI JSON | F066/F067 | F039/F068/F071 | immediate command run | authority/deploy gate | read-only result | `CODE_CONFIRMED` |
| convergence status | CLI/admin JSON | F068/F069/F070/F065 | operator/human/deploy workflow | request-time | safe next action | read-only result | `CODE_CONFIRMED` |

### 8. Mutation Boundary Map

| Function | Mutation target | Guard before mutation | Authority required? | Rollback available? | Verification available? | Evidence written? | Tests found? | Safety status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F017/F018 `update_matrix*` | state file | writer lock | NO | N/A | probe result | event/matrix | YES | Safe state writer. |
| F011 `v7-service-matrix-refresh-all` | state file | writer lock and per-egress checker | NO | N/A | service probe | matrix/event | YES | Safe observation writer. |
| F015 `v7-telegram-sentinel` | state file | `--no-autoswitch` in systemd, writer lock | NO for state | N/A | Telegram probe | matrix/event | YES | Movement disabled by service flag. |
| F019 `run_autoswitch` | unknown/autoswitch subprocess | flag-dependent; systemd disables | UNKNOWN | UNKNOWN | UNKNOWN | command result | PARTIAL | Dormant by systemd; not production movement owner. |
| F020/F021 `v7-service-matrix-test` | state file when update enabled | writer lock | NO | N/A | service probe itself | matrix row | YES | Verification writer; safe when scoped. |
| F025 `write_execution_lease` | state file | packet identity + active lease check in caller | YES via governed owner | N/A | N/A | lease | YES | Identity mutation only. |
| F027 `execute_packet` | audit file / restore barrier via F028 | packet validation + runtime recheck + replay guard | YES | rollback manifest bound | N/A | audit/lifecycle | YES | No user movement. |
| F028 `append_restore_barrier_clearance` | state file | duplicate clearance guard + packet recheck | YES | rollback manifest bound | N/A | clearance/lifecycle | YES | Restore barrier mutation only. |
| F030 `finish_execution_lease` | state file | terminal operation | YES | yes if rollback result exists | yes if result exists | lease terminal | YES | Closure mutation only. |
| F040 `Planner.apply` | production user routing | `--apply`, non-observe mode, selected moves, atomic envelope, L3 eligibility, restore barrier, approved identity | YES | YES | YES | safety/audit/operation | YES | Main Runtime mutation boundary. |
| F040 rollback branch | production user routing | verification failure + rollback-on-verify-fail | YES | this is rollback | post-rollback rc | apply row | YES | Rollback mutation boundary. |
| F041 `finalize_operation` | audit/report-like state | terminal verdict and apply flag | YES indirectly | already encoded | already encoded | audit/closure | YES | Terminal evidence writer. |
| F044 `_l3_materialize_learning_closure` | learning/feedback files | L3 incident + operation id + terminal result | NO new authority | N/A | consumes verification | feedback/closure | YES | Learning writer after terminal outcome. |
| F045 `v7-intelligence-snapshot-refresh` | intelligence snapshot files | source consistency retries | NO | N/A | source hash consistency | snapshots | YES | Advisory state writer only. |
| F071/F072 `v7-safe-deploy` / `safe_deploy_plan` | deployment/runtime files | explicit apply+confirm, truth checks, allowlist, rollback manifest | YES operator/deploy confirmation | backup/rollback manifest | truth check after deploy | manifest/fingerprint | YES | Deployment mutation boundary; not run. |
| F076/F077 safe commit/push | git state/remote | safe sync guards | YES local workflow | git history | truth/convergence later | git output | YES | Engineering workflow mutation, not runtime. |

### 9. Read-Only / Advisory Surface Map

| Surface | Functions | Input | Output | Consumer | Why not execution |
| --- | --- | --- | --- | --- | --- |
| Operator dashboard | F060-F062 | state/audit/evidence/reports | JSON views | browser/operator | GET/read-only; tests assert no POST under operator namespace. |
| Execution dashboard | F063 | contracts/readiness/evidence | JSON views | browser/operator | Displays readiness and candidates, does not apply. |
| OMP dashboard | F064 | docs/reports/read model | JSON projection | browser/human | Projection only; no mission executor found. |
| Runtime convergence display | F065/F068 | truth/convergence state | JSON status | browser/operator | Read-only status; deploy separate. |
| Intelligence snapshots | F048-F054 | existing evidence | advisory snapshots | Planner/admin | Snapshot fields explicitly say no runtime decision authority. |
| Shadow autonomy | F074 | decision surface/history | comparison model | admin/operator | Requires comparisons; no runtime mutation. |
| Analyzer/backtesting | F073 | model inputs | advisory/certification payloads | tests/admin/research | Framework code only; no blocking production owner found. |
| Safety/readiness review CLIs | F079/F080 | state/config/docs | report stdout | human/Codex | Advisory; not auto-consumed by Runtime. |

### 10. Orphan / Stub / Dormant Function Map

| Function | Why it is orphan/stub/dormant | What calls it | What it calls | What output it produces | Why output is not consumed | Could it be useful later? | Nearest owner | Classification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F019 `tools/v7-telegram-sentinel.run_autoswitch` | systemd sentinel uses `--no-autoswitch`; governed owner owns movement | F015 only when flag permits | autoswitch subprocess | autoswitch result | production service path disables it | Maybe as explicit operator diagnostic, not movement owner | Observation / governed movement | `DORMANT_BY_SYSTEMD` |
| F073 `admin_core.intelligence_platform` production/shadow/backtesting helpers | framework/read-only models; no production blocker invocation found | tests/admin future surfaces | model helpers | advisory payloads | not wired into Authority/Runtime | yes for future analyzer owner | Engineering Intelligence | `FUTURE_FRAMEWORK` |
| F074 `shadow_autonomy.build_shadow_autonomy_model` | read-only comparison model requiring operator comparisons | admin/tests | shadow helpers | shadow readiness | not a Runtime/Authority consumer | yes for trust calibration | Shadow autonomy | `FUTURE_FRAMEWORK` |
| F075 `v7-autonomy-trust-evidence-inventory` | no production invocation found | operator/research | readers | inventory JSON | consumed manually/reports | yes for automation inventory | Autonomy inventory | `ORPHAN_NO_CONSUMER` |
| F079 `v7-autoswitch-safety-review` | advisory CLI, not chained into Runtime | operator | review helpers | safety report | consumed manually | yes as certification evidence | Safety review | `READ_ONLY_HELPER` |
| F080 `v7-infrastructure-readiness-review` | advisory CLI, not certification executor | operator | parsers | readiness report | consumed manually | yes as readiness evidence | Infrastructure review | `READ_ONLY_HELPER` |
| Engineering report creation | no function found | human/Codex | N/A | report files | no code producer | yes | Engineering Reports | `DOC_ONLY` |
| Automation/Workflow Debt registry | no durable writer found | human/Codex | N/A | report/doc entries | no registry consumer | yes | Certification Program / OMP | `DOC_ONLY` |
| Current Program State/Production Maturity writers | no code writer found | human/Codex | N/A | docs | manual sync | yes | Current Program State / Production Maturity | `DOC_ONLY` |

Orphan, stub, dormant, future-framework, read-only-helper, or doc-only functions/concepts counted: `9`.

### 11. Chain Closure Matrix

| Ideal autonomous chain step | Code entry | Code exit | Closed into next step? | Next step | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Reality | state files / registries | F011/F015/F045/F031 read inputs | YES | Observation/Planner | `FULLY_CLOSED` | Code reads real runtime state paths. |
| Observation | F010/F014 | service matrix/events | YES | Health Evidence | `FULLY_CLOSED` | systemd + writer code. |
| Health Evidence | F011/F017/F049/F035 | truth classes/service scores | YES | Planner gates | `FULLY_CLOSED` | Planner service truth functions and tests. |
| Wake | F035/F036 / emergency gate | incident context | YES | Incident | `FULLY_CLOSED` | L3 wake tests. |
| Incident | F036 | `safety.l3_incident` | YES | Runtime eligibility/Learning | `FULLY_CLOSED` | incident source and retry tests. |
| Diagnosis | reports/admin evidence | human/Codex finding | PARTIAL | Owner Resolution | `PARTIALLY_CLOSED` | No executable diagnosis owner found. |
| OMP owner routing | F056/static maps + docs | owner/stage metadata | PARTIAL | Authority/engineering | `PARTIALLY_CLOSED` | Code stage map exists; canonical mapping mostly docs. |
| Authority | F039/F058/F026/F027 | allow/deny/clearance | YES | Identity/Runtime | `FULLY_CLOSED` | governed L3 tests. |
| Planner | F032-F038 | selected moves | YES | Packet/Runtime | `FULLY_CLOSED` | selected move tests. |
| Identity | F022-F025/F028 | lock/lease/clearance | YES | Runtime apply | `FULLY_CLOSED` | packet/lease tests. |
| Runtime and Execution | F040 | apply result | YES | Verification | `FULLY_CLOSED` | apply tests. |
| Verification | F042/F043 | verify rc/service rc | YES | Rollback/Closure | `FULLY_CLOSED` | verification/rollback tests. |
| Rollback / Closure | F040/F041/F030 | terminal operation/lease | YES | Learning | `FULLY_CLOSED` | rollback tests. |
| Learning | F044/F053/F054 | feedback/trust evolution | PARTIAL | Maturity/Current Program State/OMP | `PARTIALLY_CLOSED` | read models exist; Current Program State/maturity sync missing. |
| Production Maturity | docs/reports | maturity doc state | NO | next authority/certification | `DOC_ONLY` | no code writer found. |
| Current Program State | docs/programs file | Current Program State doc state | NO | OMP/handoff | `DOC_ONLY` | no code writer found. |
| OMP Mission / Continuation | F064/docs | dashboard/manual next work | PARTIAL | engineering mission | `PARTIALLY_CLOSED` | no executable mission continuation owner found. |
| Engineering Automation | F059/F073/F075/docs | advisory/registry-like evidence | PARTIAL | implementation/certification | `PARTIALLY_CLOSED` | no debt registry writer found. |
| Continuous Self Evolution | F053/F054/F074 | advisory learning/shadow model | PARTIAL | Planner/Authority future | `PARTIALLY_CLOSED` | no automatic promotion from learning to authority found. |
| Safe Deploy / Truth / Convergence | F066-F072 | truth/deploy/convergence result | YES | production sync | `FULLY_CLOSED` | sync/truth tests. |

Fully closed chains: `9`.

Partial chains: `7`.

Doc-only chain steps: `2`.

### 12. Test Coverage By Function

| Function group | Primary tests | Coverage |
| --- | --- | --- |
| F001-F006 governed movement entry and production validation | `tests/unit/test_governed_canary_cli.py`, `tests/unit/test_v7_sync_tools.py` | STRONG |
| F010-F021 health evidence / sentinel / service matrix | `tests/unit/test_telegram_sentinel_lock_scope.py`, `tests/unit/test_egress_quality_compact_lifecycle.py`, `tests/unit/test_v7_users_autoswitch_policy.py` | STRONG |
| F022-F030 packet, approved lock, restore barrier, lease | `tests/unit/test_operator_execution_packet.py`, `tests/unit/test_governed_canary_cli.py` | STRONG |
| F031-F044 Planner, incident, selected moves, apply, verify, rollback, learning | `tests/unit/test_v7_users_autoswitch_policy.py` | STRONG |
| F045-F055 intelligence / learning read models | `tests/unit/test_intelligence_workers.py`, `tests/unit/test_operator_execution_feedback.py`, `tests/unit/test_routing_brain.py` | STRONG_READ_ONLY |
| F056-F059 operator pipeline/readiness | `tests/unit/test_operator_execution_pipeline.py`, `tests/unit/test_ctr_i1_no_bypass.py` | STRONG_READ_ONLY |
| F060-F065 admin/operator/OMP/convergence visibility | `tests/unit/test_operator_observability.py`, `tests/contracts/endpoint_inventory_test.py` | STRONG_READ_ONLY |
| F066-F072 truth/deploy/convergence | `tests/unit/test_v7_truth_check.py`, `tests/unit/test_v7_sync_tools.py` | STRONG |
| F073-F075 analyzer/shadow/autonomy inventory | `tests/unit/test_intelligence_platform.py`, `tests/unit/test_shadow_autonomy.py`, `tests/unit/test_autonomy_trust_acceleration.py` | PARTIAL_FRAMEWORK |
| Current Program State / Production Maturity / debt registry / report writer | no direct code-owner tests found | WEAK |

### 13. Diagram-Ready Edge List

| from_id | to_id | edge_type | object_passed | status | notes |
| --- | --- | --- | --- | --- | --- |
| F001 | F002 | `TRIGGERS` | systemd activation | CLOSED | movement heartbeat |
| F002 | F003 | `CALLS` | CLI args | CLOSED | governed L3 service |
| F003 | F004 | `CALLS` | parsed args | CLOSED | dispatch |
| F004 | F005 | `CALLS` | state/event/snapshot/max_users/source | CLOSED | plan generation |
| F005 | F031 | `CALLS` | Planner CLI args | CLOSED | observe/guarded plan |
| F008 | F009 | `TRIGGERS` | systemd activation | CLOSED | refresh heartbeat |
| F009 | F031 | `CALLS` | pre-planner refresh args | CLOSED_REFRESH_ONLY | no apply |
| F009 | F045 | `CALLS` | pre-refresh command | CLOSED | snapshot refresh |
| F010 | F011 | `TRIGGERS` | systemd activation | CLOSED | matrix refresh |
| F011 | F012 | `CALLS` | state dir/timeout | CLOSED | writer lock |
| F011 | F013 | `CALLS` | egress id/checker | CLOSED | per-egress probe |
| F013 | service_matrix | `WRITES` | service result | CLOSED | via caller |
| F014 | F015 | `TRIGGERS` | systemd activation | CLOSED | sentinel |
| F015 | F016 | `CALLS` | egress row/prior | CLOSED | Telegram probe |
| F015 | F017 | `CALLS` | probe items | CLOSED | matrix write |
| F017 | service_matrix | `WRITES` | sentinel item | CLOSED | writer lock |
| service_matrix | F035 | `READS` | service row | CLOSED | Planner truth |
| service_matrix | F045 | `READS` | source input | CLOSED | snapshots |
| F045 | F047 | `CALLS` | input paths | CLOSED | stable run |
| F047 | F048 | `CALLS` | evidence bundle | CLOSED | build snapshots |
| F048 | F049 | `CALLS` | service evidence | CLOSED | service scores |
| F048 | F051 | `CALLS` | users/egress/evidence | CLOSED | candidate suitability |
| F048 | F053 | `CALLS` | decisions/snapshots | CLOSED | trust evolution |
| F053 | F054 | `CALLS` | decision records | CLOSED | decision learning |
| F048 | intelligence_snapshots | `WRITES` | snapshot families | CLOSED | via refresh writer |
| intelligence_snapshots | F031 | `READS` | advisory snapshots | CLOSED | Planner/advisory |
| F031 | F032 | `CALLS` | user | CLOSED | decision |
| F032 | F033 | `CALLS` | user/egress/services | CLOSED | candidate |
| F033 | F034 | `CALLS` | candidate | CLOSED | gates |
| F034 | F035 | `CALLS` | service row | CLOSED | truth classification |
| F032 | F037 | `CONSUMES` | decisions | CLOSED | selected move selection |
| F037 | F038 | `CALLS` | decisions/projected load | CLOSED | retry-aware pick |
| F037 | selected_moves | `WRITES` | plan selected moves | CLOSED | in return object |
| F037 | F036 | `CALLS` | gate evidence/selected moves | CLOSED | incident context |
| F036 | l3_incident | `WRITES` | incident context | CLOSED | plan safety object |
| selected_moves | F022 | `CONSUMES` | selected move set | CLOSED | packet materialization |
| F004 | F058 | `CALLS` | plan/max users | CLOSED | transition gate |
| F004 | F022 | `CALLS` | plan/approval ids | CLOSED | packet |
| F022 | F023 | `CALLS` | selected moves/packet hash | CLOSED | approved lock |
| F022 | rollback_manifest | `WRITES` | rollback items | CLOSED | packet embedded |
| F004 | F024 | `CALLS` | packet/plan | CLOSED | lease object |
| F004 | F025 | `CALLS` | lease | CLOSED | write lease |
| F004 | F027 | `CALLS` | packet/state/audit | CLOSED | consume packet |
| F027 | F026 | `CALLS` | packet/state | CLOSED | runtime recheck |
| F027 | F028 | `CALLS` | packet/recheck | CLOSED | clearance writer |
| F028 | F029 | `CALLS` | packet | CLOSED | clearance object |
| F028 | restore_barrier | `WRITES` | clearance | CLOSED | Runtime gate |
| restore_barrier | F040 | `READS` | clearance | CLOSED | apply eligibility |
| F004 | F006 | `CALLS` | approved identity | CLOSED | apply bridge |
| F006 | F031 | `CALLS` | `--apply --verify` args | CLOSED | Runtime CLI |
| F031 | F040 | `CALLS` | approved plan | CLOSED | apply |
| F040 | production_routing | `MUTATES` | user->target | CLOSED | guarded route/user switch |
| F040 | F042 | `VERIFIES` | user/target | CLOSED | route verification |
| F040 | F043 | `VERIFIES` | selected move/services | CLOSED | service verification |
| F043 | F020 | `CALLS` | service verification CLI args | CLOSED | required services |
| F040 | production_routing | `ROLLS_BACK` | user->source | CLOSED_IF_VERIFY_FAILS | rollback branch |
| F040 | F041 | `CONSUMES` | apply result | CLOSED | finalize |
| F041 | F044 | `LEARNS_FROM` | terminal plan | CLOSED | L3 learning closure |
| F044 | decision_feedback | `WRITES` | outcome/trust/prediction/recommendation/closure | CLOSED | later snapshot input |
| decision_feedback | F045 | `READS` | feedback records | CLOSED | snapshot refresh |
| F044 | F004 | `CONSUMES` | capability state | CLOSED | production proof |
| F030 | execution_lease | `WRITES` | terminal status | CLOSED | lease closure |
| F060 | F061 | `CALLS` | API request | CLOSED_READ_ONLY | operator facade |
| F061 | F062 | `CALLS` | repo/state/event query | CLOSED_READ_ONLY | observability |
| F062 | browser | `DISPLAYS` | JSON view | CLOSED_READ_ONLY | no execution |
| F064 | browser | `DISPLAYS` | OMP dashboard | PARTIAL | no mission executor |
| F066 | F067 | `CONSUMES` | truth module result | CLOSED | library adapter |
| F068 | F067 | `CALLS` | all truth | CLOSED | convergence |
| F069 | F068 | `CALLS` | convergence result | CLOSED | next action |
| F071 | F072 | `CALLS` | deploy args | CLOSED_IF_CONFIRMED | safe deploy |
| F072 | production_runtime | `MUTATES` | approved deploy files | CLOSED_IF_CONFIRMED | not run in Step 1C |

Edges indexed: `67`.

### 14. Code Reality Findings

1. The governed L3 execution chain is functionally closed from systemd heartbeat to Runtime Apply, Verification, Rollback/No-Rollback, and Learning closure.
2. Planner refresh is a separate refresh-only chain and does not move users.
3. Health evidence is connected, but the health model is distributed across service-matrix writers, Telegram sentinel, quality compaction, intelligence snapshots, and Planner truth classification.
4. Authority/Identity/Restore Barrier is the most strongly closed non-runtime contract: packet, approved plan lock, execution lease, runtime recheck, restore barrier clearance, and apply identity are all connected and tested.
5. Runtime mutation is narrow and visible: `Planner.apply` plus `_run_switch`, guarded by apply mode, selected moves, atomic envelope, L3 eligibility, restore barrier, approved packet identity, verification, and rollback.
6. Learning is code-confirmed through terminal feedback and trust evolution snapshots, but its downstream synchronization into Current Program State, Production Maturity, OMP continuation, debt registries, and engineering reports is incomplete or document/manual-led.
7. Admin UI and operator surfaces are strong read-only visibility systems, not execution systems.
8. Analyzer/backtesting/shadow autonomy code exists and is tested as a framework, but Step 1C did not find it connected as a production blocking owner.
9. The biggest broken edge is after `Learning / Capability Evidence`: code writes/derives learning evidence, but automatic Current Program State, Production Maturity, OMP mission continuation, Engineering Report generation, Automation Debt, Workflow Debt, and Pipeline Candidate synchronization are not closed as executable code chains.
10. The biggest read-only-only area is Admin UI / OMP / execution dashboard / intelligence platform projection.
11. The biggest missing automation area is the documentation and program synchronization layer after real capability evidence is produced.

### 15. Step 1C Verdict

```text
PHASE_1_STEP_1C_FULL_FUNCTION_GRAPH_AUDIT_COMPLETE
```

Step 1C is complete.

Step 2 can proceed.

Step 2 should use:

- Step 1 for documented knowledge source classification;
- Step 1B for code reality by artifact;
- Step 1C for function graph, state graph, mutation boundaries, closed chains, partial chains, and broken edges.

Step 2 must preserve the distinction between:

- closed execution code;
- advisory/read-only code;
- document-only program responsibilities;
- reports as evidence;
- tests as proof, not production behavior.

### 16. Next Step

Recommended next step:

```text
PHASE_1_STEP_2_CONSOLIDATE_DOCUMENTED_AND_CODE_FUNCTION_GRAPH_REALITY
```

Step 2 should consolidate the autonomous system model from existing documented and code reality only.

Step 2 must not:

- create `V7_IDEAL_AUTONOMOUS_SYSTEM_MODEL.md` unless explicitly authorized;
- create new architecture;
- create new owners;
- create OMP missions;
- modify Runtime, Planner, Authority, OMP, Current Program State, Production Maturity, or canonical docs;
- treat read-only admin/intelligence/analyzer surfaces as execution authority;
- treat reports as runtime state;
- treat tests as production behavior.

### 17. Step 1C Exhaustive Function Graph Appendix Completion

The original Step 1C section above was a high-level autonomous-chain index. It indexed `87` relevant autonomous nodes and was useful for chain-level reasoning, but it was not sufficient for a full function-by-function structural audit.

The exhaustive continuation is stored in the companion appendix files:

```text
docs/reports/research/V7_AUTONOMOUS_MODEL_FUNCTION_GRAPH_APPENDIX.md
docs/reports/research/V7_AUTONOMOUS_MODEL_FUNCTION_GRAPH_APPENDIX.json
```

The markdown appendix is the durable Step 1C function graph evidence. The JSON appendix is the machine-readable graph payload for later visualization. Together they index every discovered Python function, class, method, CLI entrypoint, API handler surface, test function/class, and systemd unit in the audited code scope.

Exhaustive appendix totals:

| Metric | Value |
| --- | ---: |
| Code files discovered in original Step 1C scope | `225` |
| Function/class nodes indexed | `3438` |
| Systemd units indexed | `13` |
| Static call/systemd edges indexed | `24819` |
| Mutation-capable nodes detected | `820` |
| Read-only/advisory nodes detected | `1202` |
| Orphan/stub/dormant/read-only-orphan nodes detected | `114` |

Closure counts:

| Closure | Count |
| --- | ---: |
| `CLI_ENTRYPOINT` | `76` |
| `ENTRY_LOGIC_PARTIAL` | `32` |
| `LEAF_CLOSED` | `290` |
| `LOGIC_CLOSED` | `654` |
| `MUTATION_CLOSED` | `323` |
| `MUTATION_ENTRYPOINT` | `1` |
| `ORPHAN_UNLINKED` | `3` |
| `READ_ONLY_CLOSED` | `985` |
| `READ_ONLY_ORPHAN` | `9` |
| `STUB_OR_DORMANT` | `102` |
| `TEST_ONLY` | `963` |

Domain counts:

| Domain | Count |
| --- | ---: |
| `admin_api` | `717` |
| `admin_core` | `807` |
| `runtime_support` | `57` |
| `test` | `963` |
| `tool` | `894` |

Each appendix inventory row records:

- node ID;
- source path and line;
- function/class/method name;
- domain;
- node type;
- what it does;
- static callers;
- static calls;
- reads;
- writes;
- subprocesses;
- input/output behavior;
- downstream nodes;
- mutation classification;
- authority relevance;
- closure status;
- static test references;
- autonomous role;
- notes.

The appendix also includes:

- systemd entrypoint graph;
- diagram-ready edge list;
- orphan/stub/dormant/read-only-orphan map;
- mutation boundary map;
- read-only/advisory surface map;
- machine-readable JSON for later visualization.

Updated Step 1C verdict:

```text
PHASE_1_STEP_1C_EXHAUSTIVE_FUNCTION_GRAPH_AUDIT_COMPLETE
```

Step 2 can proceed using the companion appendix as the authoritative exhaustive function graph evidence.

# Phase 1

## Domain 01 — Business Objective

Status:

DRAFT

### 1. Business Objective

V7 существует для того, чтобы пользователь оставался онлайн даже тогда, когда отдельные каналы, сервисы, маршруты, страны, провайдеры или операционные условия меняются и деградируют. Его бизнесовая цель не в том, чтобы быть еще одной VPN-панелью, набором протоколов или ручным переключателем маршрутов. V7 должен превращать подключение пользователя в управляемый производственный результат: система должна понимать реальную производственную ситуацию, выбирать безопасный рабочий путь, избегать лишних перемещений, восстанавливать доступ при сбоях, проверять фактический результат и учиться на том, что реально произошло.

Главный смысл V7 - невидимая надежная маршрутизация. Пользователь не должен разбираться, работает ли его доступ через OpenVPN, WireGuard, VLESS или другой канал. Для пользователя продукт должен ощущаться как стабильный интернет-доступ к важным сервисам с минимальными перебоями, минимальной ручной эскалацией и минимальным риском ухудшить состояние неверным переключением. Для владельца продукта и оператора V7 должен переводить техническую сложность маршрутизации в язык бизнес-целей: максимальная стабильность, быстрое восстановление, минимальное нарушение пользовательского опыта, высокая доступность сервисов, низкий бизнес-риск, понятные SLA-приоритеты, низкая операторская нагрузка и невидимый VPN-опыт.

Долгосрочно V7 должен стать управляемой самоулучшающейся production-routing платформой. Это означает не безусловную автоматику и не самовольные массовые действия, а рост сертифицированной автономии на основе реальных производственных исходов. Каждая новая степень самостоятельности должна быть заработана доказанными результатами, безопасной проверкой, обратимостью или корректным закрытием результата и признанием через существующие правила зрелости и допуска.

### 2. Why V7 Exists

V7 существует потому, что обычная эксплуатация VPN слишком ручная для надежного production-уровня. Отдельная панель может показывать серверы, мониторинг может показывать здоровье, скрипт может перемещать пользователей, а оператор может реагировать на проблемы. Но в реальной системе одновременно меняются пользователи, сервисы, каналы, страны, провайдеры, политики и риски. Без V7 пользователи могут оставаться на деградировавшем канале, оператор вынужден вручную искать затронутых людей, решения могут быть поздними или слишком широкими, доказательства могут устаревать, откат может быть неочевидным, а каждый инцидент превращается в ручное расследование.

Ценность V7 в том, что он превращает повторяющееся ручное спасение подключений в управляемый продуктовый процесс. Система должна сохранять доступность, снижать время реакции на подтвержденные проблемы, не двигать пользователей без достаточной пользы, уменьшать операторскую нагрузку и накапливать знание из реальных исходов, чтобы следующие решения становились безопаснее и точнее.

### 3. Primary Product

Основной продукт V7 - не VPN-протокол, не маршрутизатор как технический объект, не админка и не скрипт переключения. Основной продукт - надежная production-connectivity как результат: пользователь получает рабочий доступ к нужным интернет-сервисам, а маршрутизация остается для него невидимой.

В продуктовых терминах V7 является автономным routing control plane для пользовательской связности. Он должен защищать пользовательский доступ, делать маршруты безопасными и объяснимыми для оператора, поддерживать рост от ручного управления к сертифицированной автономии и сохранять бизнес-контроль над риском.

### 4. Primary User Value

Пользователь получает не "другой VPN", а ощущение, что интернет продолжает работать. В нормальном состоянии ценность выражается в стабильности: пользователь остается на рабочем маршруте без хаотичных переключений и лишней смены состояния. При сбое ценность выражается в быстром восстановлении: подтвержденные жесткие проблемы не требуют долгого ручного расследования, а доступ возвращается через безопасное действие. При частичной деградации ценность выражается в доступности важных сервисов: Telegram, YouTube, ChatGPT, обычный browsing и другие важные для пользователя сервисы должны быть достижимы по смыслу пользовательского/SLA-профиля, а не только по факту технически поднятого канала.

Для оператора и владельца продукта ценность состоит в снижении ручной нагрузки и риска. V7 должен показывать бизнесовую причину, ожидаемую пользу, риск, результат и исключения, а не заставлять владельца продукта мыслить пакетами, hash-ами выбранных moves, внутренностями rollback или деталями протоколов.

### 5. System Success Criteria

V7 выполняет свое назначение, когда реальные пользователи остаются онлайн или восстанавливаются после деградации без ненужной ручной охоты за причиной. Бизнесовый успех означает, что важные сервисы остаются доступными, подтвержденные сбои приводят к безопасному восстановлению, неверные или рискованные действия редки, результат проверяется фактическим production-исходом, а откат или корректное закрытие всегда доводятся до конца.

Система успешна, если маршрутизация для пользователя становится невидимой и надежной, операторская работа постепенно сокращается до целей, политик, исключений и осознанных решений о риске, а автономия растет только после сертифицированных реальных результатов. На зрелом уровне успех выражается в `PRODUCTION_AUTONOMY_CERTIFIED`: production-зрелость достигает состояния, где сертифицированная автономия доказана реальными внедрениями, проверками, сертификациями, production outcomes и решениями о допустимой автономии.

Также успех включает масштабируемость продуктового смысла: V7 должен быть способен поддерживать большую production-систему с множеством пользователей, каналов, сервисов, runtime-решений и долговременной историей доказательств, не превращая каждую проблему в ручную операцию.

### 6. System Failure Criteria

V7 следует считать неуспешным, если пользователь остается на плохом или нерабочем канале, хотя система видит производственную проблему и в рамках сертифицированной области могла бы безопасно восстановить доступ. Неуспехом также является ситуация, когда система технически "что-то сделала", но пользовательский сервис не восстановлен, результат не проверен, rollback/no-rollback не закрыт или вывод основан только на отчете, dry-run, синтетике или устаревшем знании.

V7 также проваливает бизнесовую цель, если для обычных подтвержденных инцидентов по-прежнему требуется постоянное ручное вмешательство Codex, администратора или оператора; если маршрутизация остается понятной только через инженерные артефакты; если система двигает пользователей слишком широко, слишком поздно, без доказанной пользы или в более плохое состояние; если рост автоматизации происходит без реальных production-исходов; или если техническая архитектура начинает заслонять главный продуктовый результат - надежный пользовательский доступ.

### 7. Non Goals

- V7 не пытается быть просто VPN-панелью, витриной серверов или ручным инструментом переключения.
- V7 не пытается быть blind automation, где таймер, cron или скрипт сами по себе являются достаточной причиной для production-действия.
- V7 не пытается автоматически двигать всех пользователей без сертифицированной области, риска, проверки и корректного завершения результата.
- V7 не пытается сертифицировать продукт по отчетам, dry-run или синтетическим примерам вместо реальных production outcomes.
- V7 не пытается сделать Product Owner ответственным за пакеты, routing algorithms, action classes, blast-radius internals, rollback internals, runtime gates, planner logic или protocol engineering.
- V7 не пытается заменить бизнесовую цель архитектурной сложностью, документацией или бесконечным аудитом.
- V7 не должен становиться permanently Codex-driven системой: Codex может помогать инженерно, но не должен быть постоянной production-зависимостью.
- V7 не должен снижать безопасность ради видимости автономии: если действие не доказано, не разрешено или не проверяемо, бизнесово правильное поведение - не притворяться зрелым.

### 8. Supporting Evidence

| Statement | Source |
| --- | --- |
| V7 keeps users online by automatically finding, proving, and learning the safest working route for internet access. | `docs/product/V7_PRODUCT_SPECIFICATION.md`, `Layer 1: Product`, `One Sentence`. |
| V7 exists because ordinary VPN operation is too manual for real production reliability; the product problem is to keep users connected, choose safe routes, avoid unnecessary movement, recover from failure, and learn from what actually happened. | `docs/product/V7_PRODUCT_SPECIFICATION.md`, `Product Mission`. |
| Business Objectives are the canonical top-level interface between the Product Owner and V7; the Product Owner should communicate through Business Objectives, not technical internals. | `docs/product/V7_PRODUCT_SPECIFICATION.md`, `Business Objectives`; `docs/reference/V7_CANONICAL_REFERENCE.md`, `Product Specification Rule`. |
| Initial Business Objectives include Maximum Stability, Fastest Recovery, Lowest User Disruption, Highest Service Availability, Lowest Business Risk, SLA Priorities, Business Risk Appetite, Minimal Operator Work, and Invisible VPN Experience. | `docs/product/V7_PRODUCT_SPECIFICATION.md`, `Initial Business Objectives`; `docs/reference/V7_CANONICAL_REFERENCE.md`, `Product Specification Rule`. |
| V7 is no longer merely a VPN; it is a governed production routing platform whose product purpose is to keep users online through safe, verified, evidence-based recovery and certified automation growth. | `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`, `Project Purpose`. |
| The core product is invisible reliable routing; users should not need to know whether traffic uses OpenVPN, WireGuard, VLESS, or another channel. | `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`, `Project Purpose`. |
| V7 is an event-driven autonomous routing control plane that protects user connectivity by observing production reality, selecting safe routes through existing owners, acting only under certified authority, verifying outcomes, and learning from real evidence. | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`, `Project Vision`. |
| V7 is a production connectivity product that keeps users online by making routing invisible and targets large-scale operation with many users, channels, runtime decisions, and evidence history. | `docs/reference/SYSTEM_MAP.md`, `Product Specification` row. |
| Product success means users stay online, important services remain reachable, routing changes are invisible or minimally disruptive, wrong moves are rare, rollback is available, learning improves decisions, and operator workload decreases. | `docs/reference/V7_CANONICAL_REFERENCE.md`, `Product Specification Rule`. |
| `100%` Production Maturity means `PRODUCTION_AUTONOMY_CERTIFIED`, and production maturity increases only through real implementation, deploy, testing, verification, certification, production outcomes, authority decisions, and certified autonomy. | `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md`, `Purpose`, `Separation Rule`. |
| The final autonomous target is a governed self-improving production routing platform; human involvement should shrink to business goals, policy decisions, exceptional approvals, canonical impossibility decisions, and deliberate architecture change approval. | `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`, `Final Autonomous Target`. |
| Mature autonomous routing should not be a single "move traffic" function; it must be governed by real evidence, bounded execution, verification, rollback/closure, and learning. | `docs/reports/research/2026-07-05_150942_v7_large_scale_autonomous_routing_reliability_research.md`, `Summary`, `Large-System Principles`. |
| Large-scale operations discipline turns repeated human work into bounded automation only when it remains scoped, tested, observable, reversible, and connected to user impact. | `docs/reports/research/V7_AUTONOMOUS_OPERATIONS_RESEARCH.md`, `Summary`, `Large-Scale Operations Principles`. |
| Engineering automation should reduce repeated valuable manual work through owner-backed governed pipelines, while humans remain responsible for business, policy, risk, and architecture decisions. | `docs/reports/research/V7_AUTONOMOUS_ENGINEERING_SYSTEMS_RESEARCH.md`, `Summary`, `Engineering Automation Principles`. |
| Universal autonomy law: reality precedes authority; verification completes mutation; rollback or closure is mandatory. | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `Executive Summary`, `LAW U1`, `LAW U4`, `LAW U5`. |
| Authority expansion is never automatic and may be recommended only after certified outcomes; reports alone do not grant production autonomy. | `docs/decisions/ADR-V7-OMP-PRODUCTION-PROGRAM.md`, `Decision`; `docs/reference/V7_CANONICAL_REFERENCE.md`, `Product Specification Rule`. |
| Current program state shows the project still distinguishes understanding the system from proving production autonomy; production autonomy must be earned rather than asserted. | `docs/programs/V7_CURRENT_PROGRAM_STATE.md`, `Current State Summary`; `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md`, `Separation Rule`. |

Domain:

Business Objective

Status:

DRAFT

Approved:

NO

Ready for Owner Review:

YES

### Architecture Review

Architecture

PASS

Domain 01 correctly owns the product-level reason V7 exists: reliable user connectivity as a managed production outcome. It does not confuse product objective with VPN protocols, Runtime behavior, Planner behavior, Authority mechanics, reports, or implementation artifacts.

Completeness

PASS

The domain covers why V7 exists, what problem it solves, who benefits, what success means, what failure means, long-term purpose, and non-goals. It also includes the Product Owner-facing interpretation: V7 must be understood through user connectivity, service availability, business risk, operator effort, and invisible routing rather than technical internals.

Boundaries

PASS

The domain stays at product-objective level. It does not own policy translation, decision semantics, planning, authority admission, runtime execution, verification, rollback, learning, OMP, Production Maturity, or Current Program State. Those remain downstream consumers.

Project Consistency

PASS

No canonical V7 document contradicts this domain. Product Specification, Canonical Reference, AOS, OMP, SYSTEM_MAP, Production Maturity, and Master Handoff all support the same top-level meaning: V7 is a governed production connectivity/routing product whose autonomy is earned from real outcomes.

Research Consistency

PASS

R1, R2, R3, and R4 reinforce the same principle: world-class autonomous production systems separate product outcome, evidence, decision, authority, execution, verification, rollback, learning, and evolution. The Business Objective domain correctly defines the product outcome without importing implementation.

Function Graph Consistency

PASS

Function Graph evidence does not require Business Objective to become a code owner. Real code begins downstream in observation, evidence, planner, authority, runtime, verification, rollback, learning, and visibility surfaces. The graph confirms that Business Objective is a product/canonical source consumed through policies, OMP, decision language, and operator explanations.

Future Scale

PASS

The domain remains valid at 100, 1 000, 10 000, 100 000, and 1 000 000 users because it defines the invariant product outcome, not a fixed mechanism. Scale pressure belongs to downstream domains: evidence volume, policy, authority, blast radius, runtime safety, verification, rollback, learning, OMP, and production maturity.

### Objective Improvements

NO OBJECTIVE IMPROVEMENT FOUND

Review iterations tested possible improvements around measurable SLOs, Product Owner interface, operator language, policy translation, scale objectives, and implementation consumption. None passed the improvement rule as a Domain 01 change: each is already present in the domain, already owned by another domain, or belongs to downstream implementation/certification rather than the Business Objective architecture.

### Self Criticism

Would you design it differently today?

NO

The domain is correctly shaped as the top product source. If designed from zero today, it would still define V7 as reliable production connectivity and invisible routing, while explicitly refusing to become Runtime, Planner, Authority, protocol design, UI design, or maturity scoring. The only known partial gaps are downstream consumption gaps already owned by Policy, OMP, operator/UI explanation, Production Maturity, and Current Program State.

### Cross Domain Review

Changing this domain would affect:

- Product Principles;
- Decision Model;
- Policy;
- Planner;
- Authority;
- Runtime;
- Verification;
- Rollback / Closure;
- Learning;
- Production Maturity;
- Current Program State;
- OMP;
- Engineering Automation;
- Continuous Self Evolution.

No change is required, so cross-domain impact is `NONE`.

### Owner Verdict

READY FOR APPROVAL

## Domain 02 — System Laws

Status:

DRAFT

### 1. Introduction

System Law - это фундаментальное правило, которое управляет поведением всей V7-системы независимо от конкретной подсистемы, инструмента, отчета или текущей реализации. Закон отвечает не на вопрос "как именно это сделать", а на вопрос "что V7 никогда не должна нарушать, если хочет оставаться безопасной, управляемой и действительно автономной production-системой".

Эти законы существуют, потому что V7 работает с реальными пользователями, реальными каналами, реальными сбоями и реальными business-risk последствиями. Любая часть системы может ошибиться, устареть, увидеть неполную картину или захотеть ускорить действие. Законы задают общий каркас: что считается доказательством, когда действие разрешено, когда результат считается завершенным, где проходит граница человека, как растет автономия и почему нельзя подменять production-реальность отчетами, dry-run, догадками или конфигурацией.

Каждая подсистема V7 обязана подчиняться этим законам. Если отдельный компонент работает правильно локально, но нарушает общий закон, вся система становится ненадежной: пользователи могут остаться без доступа, автоматика может начать двигать не тот объект, maturity может быть завышена, а оператор может получить ложную уверенность. Поэтому System Laws стоят выше доменных моделей и должны применяться ко всем будущим доменам Phase 1.

### 2. Fundamental Laws

#### Law 01. Reality First

Описание: реальная production-реальность всегда сильнее предположений, синтетических примеров, dry-run, stale-отчетов, planner-only выводов и мнения ассистента. V7 может объяснять и готовить действия на симуляциях, но production-способность доказывается только реальными исходами.

Зачем существует: V7 должна защищать пользователей в изменяющемся мире, где сигналы могут быть шумными, устаревшими или неполными. Если система начинает считать подготовительную информацию равной реальности, она получает ложную зрелость.

Что ломается при нарушении: автоматика может сработать по несуществующей проблеме, пропустить настоящую проблему, сертифицировать несуществующую capability или заявить успех без пользовательского восстановления.

Пример: dry-run может показать, что действие выглядит допустимым, но это не доказывает, что реальный пользователь был безопасно восстановлен в production.

#### Law 02. Evidence Before Capability

Описание: capability существует только тогда, когда есть доказательство ее реального поведения. Константа, конфигурация, документ, отчет или локальный тест могут описывать намерение, но не создают production-способность сами по себе.

Зачем существует: автономные системы опасны, когда объявленная зрелость опережает фактическую способность. V7 должна расти только от проверенного результата к следующему уровню.

Что ломается при нарушении: система может включить автоматизацию, которая существует только на бумаге; maturity станет мнением, а не состоянием продукта; оператор потеряет доверие к сертификации.

#### Law 03. Authority Before Production Mutation

Описание: никакое production-действие не может выполняться только потому, что обнаружен сигнал, найден кандидат, построен план или пришел таймер. Должно быть явное разрешение в допустимой области риска, масштаба и класса действия.

Зачем существует: факт о мире и право изменить мир - разные вещи. Даже правильное действие становится опасным, если применено слишком широко, слишком рано или вне разрешенной области.

Что ломается при нарушении: появляется неуправляемая автоматика, broad movement, скрытое расширение blast radius и production-изменения без бизнесового контроля.

#### Law 04. Decision Is Not Execution

Описание: рекомендация, план, candidate, score, selected action или approval preview не являются production-выполнением. Между намерением и изменением реальности должна сохраняться проверяемая граница.

Зачем существует: решение может устареть, потерять identity, оказаться небезопасным или выйти за пределы разрешения до момента фактического действия.

Что ломается при нарушении: система начинает считать "выбрали" равным "сделали"; отчеты объясняют не тот execution; пользователь может быть перемещен по устаревшему или неподтвержденному намерению.

#### Law 05. Object Continuity

Описание: одно execution-расследование или production-действие должно сохранять одну и ту же identity: subject, source, target, action, generation, selected object и incident context. Смена объекта допустима только как явный restart с доказанным основанием.

Зачем существует: автономная цепочка проходит через несколько владельцев и стадий. Без непрерывной identity невозможно доказать, что все оценивали один и тот же объект.

Что ломается при нарушении: расследование начинает объяснять другой candidate, production-действие применяет не тот план, а выводы о root cause становятся недостоверными.

#### Law 06. Detection Is Not Diagnosis

Описание: обнаруженный симптом доказывает только то, что что-то наблюдалось. Он не доказывает причину, владельца, масштаб или правильное действие без дополнительной классификации.

Зачем существует: один и тот же симптом может быть вызван каналом, сервисом, свежестью данных, нагрузкой, политикой, проверкой или внешней средой.

Что ломается при нарушении: V7 неправильно классифицирует сбой, выбирает неверный recovery path, обвиняет не того owner и повторяет одинаковые ошибки.

#### Law 07. Safety Before Confidence

Описание: высокая уверенность, хороший score или зрелый анализ не могут заменить safety constraints. Перед действием должны быть удовлетворены безопасность, допустимый риск, проверяемость, обратимость или корректное закрытие результата.

Зачем существует: модель может быть уверенной и все равно опасной. Production-система должна быть безопасной до того, как она будет быстрой или уверенной.

Что ломается при нарушении: V7 начнет делать уверенные, но небезопасные действия; recovery может ухудшить состояние пользователя или расширить инцидент.

#### Law 08. Blast Radius Before Scale

Описание: широкое действие должно быть заработано через малый масштаб, staged rollout, canary, batch ladder или другой ограничитель воздействия. Масштаб не должен увеличиваться раньше доказанной устойчивости предыдущего уровня.

Зачем существует: даже правильная логика может сломаться на масштабе из-за скрытых зависимостей, нагрузки, частичных отказов или неверных предположений.

Что ломается при нарушении: один дефект может затронуть всех пользователей, все каналы или весь incident scope до того, как система успеет обнаружить проблему.

#### Law 09. Verification Completes Mutation

Описание: production-изменение не завершено, пока независимая проверка не докажет фактический результат. Успешный запуск действия не равен восстановленному пользовательскому сервису.

Зачем существует: команда может выполниться, маршрут может измениться, но пользовательский доступ может остаться сломанным. V7 должна доверять результату, а не факту выполнения команды.

Что ломается при нарушении: система сообщает успех, пока пользователи остаются без доступа; learning получает ложное положительное evidence; maturity растет на неподтвержденных изменениях.

#### Law 10. Rollback Or Closure Is Mandatory

Описание: каждое production-изменение должно завершиться rollback, containment или явно сертифицированным no-rollback closure. Нельзя оставлять затронутый объект в незакрытом состоянии.

Зачем существует: не каждое изменение можно полностью откатить, но каждый измененный объект должен получить безопасное terminal состояние.

Что ломается при нарушении: пользователи застревают в неизвестном состоянии, retry-loop повторяет плохие попытки, а дальнейшая автоматизация строится на незакрытом риске.

#### Law 11. Unknown Is Not Pass And Not Fail

Описание: timeout, missing data, stale data, lock wait или неперсистированный объект должны называться unknown, пока нет доказательства pass или fail. Policy может выбрать fail-closed поведение, но причина все равно остается unknown.

Зачем существует: отсутствие результата не равно отрицательному результату. В распределенной системе проверка может не ответить по причинам, не связанным со здоровьем цели.

Что ломается при нарушении: здоровый путь может быть ошибочно признан плохим, плохой путь может быть принят как рабочий, а root cause уйдет в неправильного владельца.

#### Law 12. Freshness Matches Action Risk

Описание: доказательство должно быть достаточно свежим для конкретного класса действия. Данные, пригодные для анализа или объяснения, могут быть непригодны для production mutation.

Зачем существует: риск и обратимость действий различаются. Чем сильнее воздействие, тем строже требования к свежести и проверяемости evidence.

Что ломается при нарушении: V7 принимает production-решение по устаревшей картине мира и может восстановить уже неактуальный инцидент или ухудшить текущую ситуацию.

#### Law 13. Learn From Terminal Outcomes

Описание: каждый terminal outcome - success, rollback, hold, stop, unknown, block или impossibility - должен становиться learning evidence для будущих решений, maturity и automation evolution.

Зачем существует: production-реальность является главным учителем V7. Система, которая не учится на закрытых исходах, повторяет одни и те же инциденты.

Что ломается при нарушении: retry-budget не улучшается, плохие попытки повторяются, maturity не отражает реальную способность, а отчеты превращаются в архив вместо механизма улучшения.

#### Law 14. Negative Evidence Is Evidence

Описание: STOP, rollback, blocker, unknown и HOLD не являются "провалом исследования". Это доказательства границ текущей capability, которые должны быть классифицированы и использованы.

Зачем существует: безопасный отказ является частью production-способности. Знать, чего система не может делать безопасно, так же важно, как знать, что она может.

Что ломается при нарушении: команда будет обходить safety stops, терять root cause, повторять один и тот же blocker и продвигать автономию без знания ее границ.

#### Law 15. Existing Owner Before New Owner

Описание: каждое изменение сначала ищет существующего владельца. Новый owner, truth source, execution path или архитектурный слой допустим только после доказательства, что существующая система не может выразить нужное поведение.

Зачем существует: дублирование владельцев создает противоречивые истины и неуправляемую архитектуру. V7 должна расти через reuse и extension, а не через параллельные системы.

Что ломается при нарушении: появляются конкурирующие Runtime, Planner, Authority, roadmaps, truth sources или workflows; разные части V7 начинают жить по разным правилам.

#### Law 16. Durable Truth Has One Canonical Owner

Описание: долговечное правило, семантика или product fact должны иметь одного canonical owner. Другие документы и представления могут потреблять или проецировать это знание, но не становиться второй истиной.

Зачем существует: несколько источников правды неизбежно расходятся при изменениях. Система должна знать, куда идти за правилом и где его менять.

Что ломается при нарушении: отчеты начинают спорить с reference-документами, текущие состояния начинают выдавать разрешения, а future sessions получают несовместимые инструкции.

#### Law 17. Reports Preserve Evidence, Not Authority

Описание: engineering reports сохраняют историю и доказательства. Они могут питать canonical owners, maturity и будущие расследования, но сами не становятся roadmap, authority, truth source или live state.

Зачем существует: отчет является историческим артефактом и устаревает сразу после изменения reality. Использовать отчет как живое разрешение опасно.

Что ломается при нарушении: V7 действует по старой истории, создает report-only capability и смешивает доказательство прошлого с текущим правом действовать.

#### Law 18. Automation Must Be Suspendable

Описание: любой автономный или полуавтономный класс действия должен иметь понятный stop, hold, demotion или suspension path.

Зачем существует: automation усиливает не только правильность, но и дефекты. Если автоматический контур вредит, он должен быстро и безопасно останавливаться.

Что ломается при нарушении: ошибочная автоматизация продолжает повторять rollback, расширяет incident или создает cascading failure.

#### Law 19. Repeated Manual Work Is Debt Until Classified

Описание: повторяющееся ручное действие или workflow является debt, пока оно не автоматизировано, не признано intentionally manual, не заблокировано будущей capability, не признано not cost-effective или canonically impossible.

Зачем существует: человеческое внимание не масштабируется линейно с пользователями, каналами, инцидентами и сертификациями.

Что ломается при нарушении: V7 остается permanent Codex/admin dependent, routine work не превращается в системную способность, а production growth требует все больше ручного труда.

#### Law 20. Humans Own Policy, Exceptions, And Architecture Boundaries

Описание: зрелая автономия убирает routine toil, но не забирает у людей ответственность за бизнесовые цели, policy boundaries, exceptional risk acceptance, authority expansion и deliberate architecture change.

Зачем существует: некоторые решения требуют ценностного суждения, ответственности и бизнесового риска, которые нельзя вывести только из telemetry.

Что ломается при нарушении: система начнет сама расширять собственную власть, менять policy, принимать неразрешенный business risk или оформлять архитектурный drift как автоматическое улучшение.

#### Law 21. Evolution Is Incremental And Reversible Where Possible

Описание: V7 должна развиваться малыми наблюдаемыми шагами, с возможностью rollback, containment или safe closure там, где это возможно. Big-bang transformation не является нормальным способом роста автономии.

Зачем существует: крупные production-системы имеют скрытые зависимости. Малые шаги обнаруживают риск до широкого воздействия.

Что ломается при нарушении: одна ошибка превращается в системный сбой, а команда теряет возможность понять первый divergence и безопасно вернуться.

### 3. Relationships Between Laws

Эти законы образуют не независимый список, а систему взаимного усиления. Reality First задает главный источник истины: V7 должна смотреть на реальный мир. Evidence Before Capability превращает эту реальность в критерий зрелости. Authority Before Production Mutation ограничивает право действовать, а Decision Is Not Execution не дает путать намерение с изменением production.

Object Continuity, Freshness и Unknown Classification защищают качество доказательства: система должна знать, какой объект она рассматривает, насколько свежи данные и что именно доказано. Detection Is Not Diagnosis не дает перейти от симптома к причине без проверки. Safety Before Confidence и Blast Radius Before Scale удерживают систему от опасного ускорения.

Verification, Rollback/Closure и Learning превращают действие в завершенный production-цикл. Verification доказывает результат, rollback или closure закрывает риск, а learning переносит terminal outcome в будущее поведение. Negative Evidence делает STOP и rollback не тупиком, а полезной границей capability.

Existing Owner, Single Canonical Owner и Reports Preserve Evidence удерживают архитектуру целостной. Они запрещают параллельные правды, owner drift и report-driven execution. Automation Suspendability, Manual Work Debt и Human Boundary Laws описывают, как V7 становится автономнее без потери контроля: рутинное должно автоматизироваться, но политика, исключения и архитектурные решения остаются человеческой границей.

Incremental Evolution связывает все вместе: V7 растет только через проверенные, ограниченные, обратимые или закрываемые шаги. Поэтому ни один закон не заменяет остальные: каждый закрывает отдельный класс системного риска.

### 4. Non-Negotiable Laws

Следующие законы являются non-negotiable для любой production-impacting работы:

- Reality First.
- Evidence Before Capability.
- Authority Before Production Mutation.
- Decision Is Not Execution.
- Object Continuity.
- Safety Before Confidence.
- Verification Completes Mutation.
- Rollback Or Closure Is Mandatory.
- Unknown Is Not Pass And Not Fail.
- Existing Owner Before New Owner.
- Durable Truth Has One Canonical Owner.
- Reports Preserve Evidence, Not Authority.
- Humans Own Policy, Exceptions, And Architecture Boundaries.

Эти законы нельзя нарушать ради скорости, удобства, красивого отчета, ускорения сертификации, уменьшения ручной работы или видимости автономии. Если выполнение задачи требует нарушить один из них, это не обычный blocker, а архитектурное противоречие или граница policy, которую нужно явно классифицировать.

### 5. Supporting Evidence

| Law | Source |
| --- | --- |
| Reality First | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW U1: Reality Precedes Authority`; `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`, `Fundamental Autonomy Laws`; `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`, `Reality First`. |
| Evidence Before Capability | `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`, `Executive Summary`; `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md`, `Separation Rule`; `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`, `Capability Earned`; `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW EV1`. |
| Authority Before Production Mutation | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW U1`, `LAW A1`, `LAW A2`; `docs/decisions/ADR-V7-ACTION-CLASS-AUTHORITY.md`, `Decision`; `docs/decisions/ADR-V7-OMP-PRODUCTION-PROGRAM.md`, `Decision`. |
| Decision Is Not Execution | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW U3`; `docs/reference/V7_DECISION_MODEL.md`, `Universal Engineering Laws`, `Law 1`; `docs/reference/V7_RUNTIME_MODEL.md`, `Runtime Laws`. |
| Object Continuity | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW R2`; `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`, `Final Autonomous Target`; historical execution identity findings in `docs/reports/engineering/`. |
| Detection Is Not Diagnosis | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW U2`; `docs/reports/research/V7_AUTONOMOUS_OPERATIONS_RESEARCH.md`, `Summary`; `docs/reference/V7_DECISION_MODEL.md`, `Universal Principles`. |
| Safety Before Confidence | `docs/reference/V7_DECISION_MODEL.md`, `Universal Engineering Laws`, `Law 6`; `docs/reference/V7_CANONICAL_REFERENCE.md`, `Product Specification Rule`; `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW S1`, `LAW A1`. |
| Blast Radius Before Scale | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW A1`; `docs/reference/V7_DECISION_MODEL.md`, `Universal Engineering Laws`, `Law 7`; `docs/reports/research/2026-07-05_150942_v7_large_scale_autonomous_routing_reliability_research.md`, `Summary`. |
| Verification Completes Mutation | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW U4`; `docs/reference/V7_DECISION_MODEL.md`, `Universal Engineering Laws`, `Law 8`; `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`, `Fundamental Autonomy Laws`. |
| Rollback Or Closure Is Mandatory | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW U5`, `LAW RB1`; `docs/reference/V7_DECISION_MODEL.md`, `Universal Engineering Laws`, `Law 9`; `docs/reports/research/V7_AUTONOMOUS_OPERATIONS_RESEARCH.md`, `Summary`. |
| Unknown Is Not Pass And Not Fail | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW V2`; production verification and lock-owner investigations in `docs/reports/engineering/`. |
| Freshness Matches Action Risk | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW K2`; `docs/reference/V7_DECISION_MODEL.md`, `Decision Inputs`; `docs/reference/V7_RUNTIME_MODEL.md`, `Runtime Laws`. |
| Learn From Terminal Outcomes | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW L1`; `docs/reference/V7_DECISION_MODEL.md`, `Universal Engineering Laws`, `Law 10`; `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`, `Fundamental Autonomy Laws`. |
| Negative Evidence Is Evidence | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW L2`; `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`, `Owner Resolution`; `docs/reports/research/V7_AUTONOMOUS_OPERATIONS_RESEARCH.md`, `Summary`. |
| Existing Owner Before New Owner | `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`, `Discover -> Reuse -> Extend -> Create Only If Necessary`; `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`, `Existing Owner Law`; `docs/decisions/ADR-V7-OMP-PRODUCTION-PROGRAM.md`, `Consequences`. |
| Durable Truth Has One Canonical Owner | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW K1`; `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`, `Canonical Knowledge`; `docs/reference/SYSTEM_MAP.md`, ownership lookup rules. |
| Reports Preserve Evidence, Not Authority | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW E2`; `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`, `Engineering Reports`; `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md`, `Product Evolution Behavior Contract`. |
| Automation Must Be Suspendable | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW AU1`; `docs/reports/research/V7_AUTONOMOUS_OPERATIONS_RESEARCH.md`, `Summary`; `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`, `Fundamental Autonomy Laws`. |
| Repeated Manual Work Is Debt Until Classified | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW E1`, `LAW H2`; `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`, `Automation Evolution`, `Workflow Evolution`; `docs/reports/research/V7_AUTONOMOUS_ENGINEERING_SYSTEMS_RESEARCH.md`, `Summary`. |
| Humans Own Policy, Exceptions, And Architecture Boundaries | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW H1`; `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`, `Human Boundary`; `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`, `Controlled Production`, `Owner Resolution`. |
| Evolution Is Incremental And Reversible Where Possible | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW EV2`; `docs/reports/research/2026-07-05_150942_v7_large_scale_autonomous_routing_reliability_research.md`, `Summary`; `docs/reports/research/V7_AUTONOMOUS_OPERATIONS_RESEARCH.md`, `Summary`. |

Domain:

System Laws

Status:

DRAFT

Approved:

NO

Ready for Owner Review:

YES

## Domain 03 — Product Principles

Status

DRAFT

### 1. Definition

Product Principles - это постоянные продуктовые правила, которые переводят Business Objective в ожидаемое поведение V7. Они объясняют, каким должен быть продукт с точки зрения пользователя, владельца продукта и оператора: реальность важнее предположений, пользовательская связность важнее технической красоты, безопасность важнее движения, доверие появляется только после проверки, а автоматизация растет только из реальных исходов.

### 2. What V7 Is

V7 - это governed production routing platform, которая обеспечивает пользователям рабочую связность через управляемый выбор, проверку и развитие маршрутизации в реальной production-среде. Это не "еще один VPN", потому что продуктовая ценность V7 находится не в отдельном туннеле или протоколе, а в способности поддерживать доступ пользователя к важным сервисам, понимать реальное состояние каналов, безопасно менять маршрут, проверять результат и учиться на закрытых исходах.

V7 также является engineering platform, потому что сама система должна постоянно уменьшать ручную инженерную работу: повторяемые расследования, проверки, сертификации, операторские действия и workflow должны превращаться в существующие owner-governed процессы. Автономность в V7 не является отдельной декоративной функцией. Она является частью продукта, потому что пользовательская связность, controlled production safety, evidence-based scaling и снижение операторской нагрузки невозможны как разовые ручные действия; они должны развиваться как постоянное свойство системы.

### 3. Purpose

Product Principles существуют, чтобы V7 не превращался в набор технических механизмов без продуктового центра. Они удерживают систему вокруг главной цели: пользователь должен оставаться онлайн, важные сервисы должны быть доступны, маршрутизация должна быть невидимой, а оператор не должен управлять внутренностями системы как основным языком продукта.

### 4. Responsibilities

Этот домен отвечает за продуктовые ограничения, которым должны подчиняться все последующие домены. Он определяет, что V7 должна быть reality-first, user-connectivity-first, safe-before-movement, explainable, reversible, evidence-driven, owner-reusing и non-duplicating системой. Он не отвечает за выбор конкретного действия, production mutation, техническую диагностику, authority admission или runtime execution.

### 5. Relationships

Product Principles опираются на Business Objective и System Laws. Они становятся продуктовой рамкой для Reality Model, потому что реальность должна измеряться не ради наблюдения как такового, а ради пользовательского результата. Следующие домены должны использовать эти принципы как язык ограничений, не переопределяя их.

### 6. System Laws

Домен ограничен законами Reality First, Evidence Before Capability, Safety Before Confidence, Existing Owner Before New Owner, Reports Preserve Evidence Not Authority, Human Boundary и Incremental Evolution.

### 7. Success Criteria

Домен выполняет роль, если все будущие решения V7 можно объяснить через продуктовую ценность, пользовательскую связность, безопасность, доказанность, минимальную операторскую нагрузку и отсутствие дублирующих систем.

### 8. Failure Criteria

Домен провален, если V7 начинает объяснять себя техническими артефактами вместо пользовательского результата, если автоматизация оправдывается удобством вместо evidence, или если новые подсистемы создаются без доказанной необходимости.

### 9. Supporting Evidence

| Statement | Source |
| --- | --- |
| Product principles include Reality First, User Connectivity First, Minimal Operator Work, Safety Before Movement, Learning From Reality, Event-Driven Operation, Reuse Before Rewrite, Simple Authority, Explainability, Reversibility, Verification Before Trust, Background Knowledge / Thin Runtime, and No Duplicated Systems. | `docs/product/V7_PRODUCT_SPECIFICATION.md`, `Product Principles`; `docs/reference/V7_CANONICAL_REFERENCE.md`, `Product Specification Rule`. |
| V7 is a governed production routing platform centered on real production evidence, safety-bounded authority, controlled certification, no duplicate owners, and continuous automation/workflow evolution. | `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`, `Project Purpose`, `Project Philosophy`. |
| V7 must not create duplicate Runtime, Planner, Authority, OMP, truth source, roadmap, or execution path. | `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`, `Non-Goals`; `docs/decisions/ADR-V7-OMP-PRODUCTION-PROGRAM.md`, `Forbidden`. |

Domain:

Product Principles

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 04 — Reality Model

Status

DRAFT

### 1. Definition

Reality Model - это представление того, что в production действительно существует и происходит сейчас: пользователи, каналы, сервисы, деградации, риски, свежесть данных, подтвержденные исходы и текущие границы возможностей. Это не мнение, не отчет и не намерение, а основа, от которой V7 должна начинать любое рассуждение.

### 2. Purpose

Reality Model нужен, чтобы V7 не действовала по догадкам. Он связывает продуктовую цель с наблюдаемым миром: если пользовательский доступ должен быть сохранен, система сначала должна понимать, что реально сломано, что реально работает, какие пользователи затронуты и какие доказательства достаточно свежие.

### 3. Responsibilities

Этот домен отвечает за различение реального состояния, предположения, синтетического примера, historical evidence и текущего production fact. Он не отвечает за сбор конкретного сигнала, диагностику причины, выбор действия, authority admission или выполнение действия.

### 4. Relationships

Reality Model следует за Product Principles и задает основу для Observation. Observation читает и пополняет картину реальности, но не должна подменять всю реальность одним сигналом. Health Evidence, Wake и Incident позже используют Reality Model как контекст, а не как разрешение на действие.

### 5. System Laws

Домен ограничен законами Reality First, Unknown Is Not Pass And Not Fail, Freshness Matches Action Risk, Evidence Before Capability и Reports Preserve Evidence Not Authority.

### 6. Success Criteria

Домен успешен, если V7 ясно различает текущую production-реальность, устаревшее знание, synthetic evidence, unknown-состояние и доказанный terminal outcome.

### 7. Failure Criteria

Домен провален, если stale report, dry-run, isolated metric или planner-only assumption начинает считаться реальностью, либо если unknown ошибочно превращается в pass или fail.

### 8. Supporting Evidence

| Statement | Source |
| --- | --- |
| Real production reality overrides synthetic examples, guesses, report-only claims, stale artifacts, and planner-only assumptions. | `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`, `Reality First`; `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW U1`. |
| Autonomy is earned by evidence, verification, safety gates, authority, production validation, maturity consumption, and certification where required. | `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`, `Executive Summary`. |
| Production Maturity increases only through real implementation, deploy, testing, verification, certification, production outcomes, authority decisions, and certified autonomy. | `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md`, `Separation Rule`. |

Domain:

Reality Model

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 05 — Observation

Status

DRAFT

### 1. Definition

Observation - это домен, который замечает production-факты. Он отвечает на вопрос: "что реально наблюдается?" Observation фиксирует признаки состояния пользователей, каналов, сервисов и среды, но сам по себе не объясняет причину, не выбирает действие и не дает права менять production.

### 2. Purpose

Observation существует, чтобы V7 не ждала ручного обнаружения очевидных проблем и не работала вслепую. Без наблюдения система не знает, какие пользователи затронуты, какие сервисы деградировали, какой канал выглядит проблемным и какие факты требуют дальнейшего анализа.

### 3. Responsibilities

Домен отвечает за поступление наблюдаемых фактов, сохранение их связи с реальностью, указание свежести и передачу наблюдения дальше. Он не отвечает за diagnosis, wake admission, incident scope, planning, authority или execution.

### 4. Relationships

Observation использует Reality Model и создает вход для Health Evidence. Он должен поддерживать Product Principles: наблюдение нужно для пользовательской связности, а не для технической витрины. Следующий домен превращает отдельные наблюдения в структурированное health evidence.

### 5. System Laws

Домен ограничен законами Reality First, Detection Is Not Diagnosis, Freshness Matches Action Risk, Unknown Is Not Pass And Not Fail и Evidence Before Capability.

### 6. Success Criteria

Observation успешен, если важные production-факты становятся видимыми, свежесть понятна, affected scope не теряется, а наблюдение не выдается за diagnosis или permission.

### 7. Failure Criteria

Observation провален, если реальный сбой остается невидимым, если сигнал теряет привязку к пользователю, каналу или сервису, если freshness неизвестна, или если один симптом сразу трактуется как готовое действие.

### 8. Supporting Evidence

| Statement | Source |
| --- | --- |
| V7 observes users, channels, services, route quality, failure signals, service reachability, and user impact. | `docs/product/V7_PRODUCT_SPECIFICATION.md`, `What V7 Actually Does`, `Observes`. |
| V7 final target includes continuous observation of production reality and detection of incidents and degradation from real evidence. | `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`, `Final Autonomous Target`. |
| Mature systems separate observation from health classification, incident materialization, authority, execution, verification, rollback, and learning. | `docs/reports/research/2026-07-05_150942_v7_large_scale_autonomous_routing_reliability_research.md`, `Summary`. |

Domain:

Observation

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 06 — Health Evidence

Status

DRAFT

### 1. Definition

Health Evidence - это структурированное доказательство о пригодности или непригодности пользователей, каналов, сервисов, источников, целей и условий для дальнейшего решения. Это не один boolean и не общий score, а набор проверяемых причин, свежести, контекста и ограничений.

### 2. Purpose

Health Evidence существует, чтобы V7 могла отличать технически поднятый канал от реально полезного пользовательского пути. Пользовательская связность зависит от сервисов, свежести данных, нагрузки, безопасности, SLA-контекста и причин деградации, а не только от факта, что интерфейс или маршрут выглядит живым.

### 3. Responsibilities

Домен отвечает за то, чтобы здоровье было объяснимым, разложенным по измерениям и пригодным для downstream-доменов. Он не отвечает за wake, incident creation, planning, authority admission, execution или verification outcome.

### 4. Relationships

Health Evidence получает факты от Observation и подготавливает основание для Wake. Оно должно сохранять связь с Reality Model и не превращаться в самостоятельное решение. Если evidence неполное или stale, следующие домены должны видеть это явно.

### 5. System Laws

Домен ограничен законами Reality First, Unknown Is Not Pass And Not Fail, Freshness Matches Action Risk, Detection Is Not Diagnosis и Safety Before Confidence.

### 6. Success Criteria

Домен успешен, если V7 может объяснить, какой именно аспект health подтвержден, какой неизвестен, какой устарел, какой сервис или контекст затронут, и почему это evidence достаточно или недостаточно для следующего шага.

### 7. Failure Criteria

Домен провален, если health сворачивается в непрозрачный score, если missing evidence трактуется как pass, если timeout трактуется как service failure без доказательства, или если важные причины теряются между доменами.

### 8. Supporting Evidence

| Statement | Source |
| --- | --- |
| Routing health must preserve source, target, service, freshness, load, safety, and reason evidence separately. | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW R1`. |
| Technical Health is diagnostics-only and explains why the score is what it is; it must not become a separate primary action owner. | `docs/decisions/ADR-003-health-screen-diagnostics-only.md`, `Decision`. |
| Decision inputs include health/readiness, evidence quality/freshness, user/service relevance, risk, authority, rollback, verification readiness, and outcome history. | `docs/reference/V7_DECISION_MODEL.md`, `Decision Inputs`. |

Domain:

Health Evidence

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 07 — Intelligence

Status

DRAFT

Definition

Intelligence - это подготовленное знание, которое помогает V7 понимать production-реальность до момента действия. Оно объединяет наблюдения, исторические исходы, пригодность сервисов, доверие к направлениям, прогнозные признаки и объяснимые рекомендации, но само по себе не является решением, authority или runtime-действием.

Purpose

Intelligence существует, чтобы live-контур V7 не выполнял тяжелое расследование под давлением. Система должна заранее готовить знания, которые улучшают качество решений, объяснений и будущих проверок, но не превращаются в самостоятельное право менять production.

Responsibilities

Домен отвечает за подготовку, обновление, объяснение и ограниченное предоставление знаний для следующих доменов. Вне его ответственности находятся product policy, authority admission, execution, verification result и production-изменение.

Relationships

Intelligence получает вход от Reality Model, Observation, Health Evidence, Learning и исторических outcomes. Его выход потребляют Diagnosis, Decision Model, Planner, Routing Intelligence и Engineering Automation. Он является домен фонового знания и должен оставаться отделенным от execution.

System Laws

Домен ограничен законами Reality First, Evidence Before Capability, Freshness Matches Action Risk, Learn From Terminal Outcomes, Reports Preserve Evidence Not Authority и Safety Before Confidence.

Success Criteria

Intelligence считается успешным, если подготовленное знание улучшает объяснимость, пригодность решений и качество диагностики, не выдавая себя за authority или verified production capability.

Failure Criteria

Домен считается проваленным, если advice начинает действовать как разрешение, если stale knowledge используется как live reality, если synthetic evidence повышает maturity, или если background intelligence становится скрытым planner/runtime.

Supporting Evidence

| Statement | Source |
| --- | --- |
| Background systems build knowledge and Runtime spends подготовленное знание. | `docs/reference/V7_RUNTIME_MODEL.md`, `Runtime Laws`, `Runtime Time Architecture`. |
| Decision inputs include evidence quality, свежийness, user/service fit, risk, rollback, verification readiness, and outcome history. | `docs/reference/V7_DECISION_MODEL.md`, `Decision Inputs`. |
| Function Graph validation shows intelligence and routing-intelligence surfaces exist primarily as read-only/advisory projections and test-covered knowledge surfaces. | `docs/reports/research/V7_AUTONOMOUS_MODEL_FUNCTION_GRAPH_APPENDIX.md`, `Read-Only / Advisory Nodes`, intelligence and routing intelligence entries. |

Domain:

Intelligence

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 08 — Routing Intelligence

Status

DRAFT

Definition

Routing Intelligence - это специализированный intelligence-domain, который оценивает пригодность route, service, user и target как advisory knowledge. Он помогает V7 понимать candidate pools и service fit, но не разрешает movement и не заменяет Planner, Policy или Authority.

Purpose

Routing Intelligence существует, чтобы routing choices были опирались на service quality, user needs, historical outcomes, trust, suitability и pool health, а не только на простую technical availability.

Responsibilities

Домен отвечает за advisory route suitability, service fit, candidate/pool comparison, trust context и explainability для routing decisions. Он не отвечает за final action selection, production authority, identity lock, runtime execution or verification.

Relationships

Routing Intelligence получает вход от Intelligence, Health Evidence, Learning и Reality Model. Его output потребляют Decision Model и Planner как advice. Authority and Runtime must treat it as подготовленное знание, not as permission.

System Laws

Домен ограничен законами Health Is A Matrix, Safety Before Confidence, Evidence Before Capability, Freshness Matches Action Risk, Decision Is Not Execution and Learn From Terminal Outcomes.

Success Criteria

Routing Intelligence успешен, если он улучшает объяснение candidate и suitability, не становясь hidden authority или hidden planner.

Failure Criteria

Домен провален, если advisory score becomes action, if stale suitability overrides live safety, if service fit is collapsed into a single opaque score, or if it moves users by itself.

Supporting Evidence

| Statement | Source |
| --- | --- |
| V7 product principles include background knowledge and thin runtime. | `docs/product/V7_PRODUCT_SPECIFICATION.md`, `Product Principles`. |
| Decision inputs include service/user/channel fit, evidence quality, readiness and risk before action. | `docs/reference/V7_DECISION_MODEL.md`, `Decision Inputs`. |
| Function Graph validation shows routing intelligence components are largely read-only/advisory and connected to tests for advisory scoring, suitability and prediction without authority. | `docs/reports/research/V7_AUTONOMOUS_MODEL_FUNCTION_GRAPH_APPENDIX.md`, routing intelligence entries and tests. |

Domain:

Routing Intelligence

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 09 — Wake

Status

DRAFT

### 1. Definition

Wake - это домен, который решает, достаточно ли подтвержденного production-события, чтобы начать следующий governed цикл реакции. Wake не является таймером, cron, blind polling или правом на действие. Он отвечает на вопрос: "есть ли легальная причина продолжить обработку этого production-состояния?"

### 2. Purpose

Wake нужен, чтобы V7 не начинала recovery или escalation от произвольного шума. Он отделяет простое наличие наблюдений от подтвержденного события, которое можно передать в Incident. Это защищает систему от blind automation и одновременно позволяет не игнорировать реальные деградации.

### 3. Responsibilities

Домен отвечает за признание или отклонение wake reason, сохранение связи с evidence и передачу только допустимого события дальше. Он не отвечает за diagnosis, scope ownership, action selection, authority admission или runtime execution.

### 4. Relationships

Wake получает Health Evidence и передает признанное событие в Incident. Он опирается на Reality Model и Product Principles: событие должно служить пользовательской связности и не должно быть искусственным разрешением на движение.

### 5. System Laws

Домен ограничен законами Reality First, Authority Before Production Mutation, Detection Is Not Diagnosis, Unknown Is Not Pass And Not Fail и Automation Must Be Suspendable.

### 6. Success Criteria

Wake успешен, если реальные подтвержденные production-проблемы могут начать governed обработку, а таймеры, polling, synthetic examples и неподтвержденные сигналы не становятся самостоятельной authority.

### 7. Failure Criteria

Wake провален, если очевидная production-деградация не материализуется как допустимое событие, либо если обычный таймер или технический шум запускает цепочку как будто он является authority.

### 8. Supporting Evidence

| Statement | Source |
| --- | --- |
| Real evidence must precede authority; a signal, alert, probe, metric, report, AI output, timer, or document is not itself permission to mutate production. | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `Executive Summary`, `LAW U1`. |
| V7 final target detects incidents and degradation from real evidence. | `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`, `Final Autonomous Target`. |
| V7 operations research maps Reality to Observation / Wake / Incident before decision and authority. | `docs/reports/research/V7_AUTONOMOUS_OPERATIONS_RESEARCH.md`, `Summary`. |

Domain:

Wake

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 10 — Incident

Status

DRAFT

### 1. Definition

Incident - это оформленная production-ситуация, в которой подтвержденная проблема имеет scope, affected reality и причину для продолжения governed обработки. Incident не равен одному сигналу и не равен выбранному действию; он удерживает контекст проблемы до восстановления, containment, canonical impossibility или другого законного завершения.

### 2. Purpose

Incident существует, чтобы V7 работала не с разрозненными сигналами, а с сохраняемой ситуацией. Для failed-source или degraded-service проблемы важно не потерять исходный scope после первого действия и не переключиться на unrelated optimization.

### 3. Responsibilities

Домен отвечает за сохранение incident identity, affected scope, incident source или другого релевантного контекста, а также за понятные условия продолжения или закрытия. Он не отвечает за diagnosis details, planning, authority, execution, verification или learning outcome.

### 4. Relationships

Incident принимает допустимое событие от Wake и дает контекст Diagnosis и Planner. Он должен сохранять связь с Reality Model и Product Principles: цель incident - восстановление затронутой пользовательской реальности, а не произвольное улучшение системы.

### 5. System Laws

Домен ограничен законами Object Continuity, Detection Is Not Diagnosis, Negative Evidence Is Evidence, Rollback Or Closure Is Mandatory и Incremental Evolution.

### 6. Success Criteria

Incident успешен, если scope проблемы сохраняется через governed цикл, затронутые пользователи не теряются, unrelated action не подменяет recovery, а закрытие происходит только по доказанному terminal условию.

### 7. Failure Criteria

Incident провален, если после одного действия система забывает, что affected users еще остаются, если incident scope меняется молча, или если последующие домены объясняют уже другой execution object.

### 8. Supporting Evidence

| Statement | Source |
| --- | --- |
| Failover incident remains scoped to its failed source until recovery, containment, impossibility, or no affected users remain. | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW R3`. |
| V7 final target can detect incidents and degradation, diagnose affected owner/scope/root condition, and close rollback/no-rollback correctly. | `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`, `Final Autonomous Target`. |
| Operations discipline separates detection, incident command, bounded automation, verification, rollback/containment, postmortem, and maturity improvement. | `docs/reports/research/V7_AUTONOMOUS_OPERATIONS_RESEARCH.md`, `Summary`. |

Domain:

Incident

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 11 — Diagnosis

Status

DRAFT

### 1. Definition

Diagnosis - это домен, который объясняет, почему observed или incident state возник, какой owner или condition является причиной, и что доказано на данный момент. Diagnosis не является решением к действию и не является authority; это переход от симптома к проверенной причине или к признанному unknown.

### 2. Purpose

Diagnosis нужен, чтобы V7 не лечила симптомы вслепую. Без него система может принять service symptom за source failure, stale evidence за target failure или owner block за terminal explanation.

### 3. Responsibilities

Домен отвечает за root-cause classification, owner resolution, различение symptoms и causes, фиксацию unknown и объяснение, почему дальнейшее расследование больше не нужно или почему нужно продолжить. Он не отвечает за action ranking, authority admission, runtime execution или verification result.

### 4. Relationships

Diagnosis получает context от Incident и объясняет его для Planner и Authority. Он должен использовать Health Evidence, не теряя Reality Model, и обязан уважать System Laws: detection is not diagnosis and unknown is not fail/pass.

### 5. System Laws

Домен ограничен законами Detection Is Not Diagnosis, Unknown Is Not Pass And Not Fail, Negative Evidence Is Evidence, Existing Owner Before New Owner и Reports Preserve Evidence Not Authority.

### 6. Success Criteria

Diagnosis успешен, если причина, owner, unknown-state или policy boundary названы доказательно, а система не останавливается на label без terminal owner resolution.

### 7. Failure Criteria

Diagnosis провален, если первый blocker принимается за root cause, если симптомы классифицируются без доказательства, если unknown маскируется под fail, или если investigation drift объясняет другой объект.

### 8. Supporting Evidence

| Statement | Source |
| --- | --- |
| A failed probe or alert proves only that something was observed, not why it happened. | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW U2`. |
| A blocking owner is never the final explanation; owner blocks must be classified into policy, missing implementation, missing invocation, defect, or impossibility. | `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`, `Owner Resolution`. |
| Human escalation is valid when authority, ambiguity, policy, missing evidence, or risk blocks automation. | `docs/reference/V7_DECISION_MODEL.md`, `Universal Engineering Laws`, `Law 11`. |

Domain:

Diagnosis

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 12 — Decision Model

Status

DRAFT

Definition

Decision Model - это домен, который определяет язык и форму решений V7. Он объясняет, какие decision outcomes допустимы, какие входы должны быть разделены перед выбором действия, и почему decision не является execution.

Purpose

Decision Model существует, чтобы V7 принимал решения структурированно, объяснимо и в границах product intent, policy, evidence, risk and authority. Он предотвращает ситуацию, где raw signal, score или operator wish становятся неявным действием.

Responsibilities

Домен отвечает за decision vocabulary, decision inputs, escalation semantics, stop outcomes, reconciliation между desired/current state и explainability. Он не отвечает за реализацию planning, authority approval, identity lock, runtime apply, verification or хранение learning.

Relationships

Decision Model получает вход от Business Objective, Product Principles, Reality Model, Health Evidence, Diagnosis и Intelligence. Его output потребляют Policy, Planner, Authority и operator-facing explanation domains. Он задает семантику решения, но не выполняет его.

System Laws

Домен ограничен законами Decision Is Not Execution, Safety Before Confidence, Detection Is Not Diagnosis, Evidence Before Capability, Authority Before Production Mutation and Humans Own Policy Boundaries.

Success Criteria

Decision Model успешен, если каждое решение можно объяснить через current state, desired state, policy basis, evidence basis, risk, authority need, verification expectation и learning path.

Failure Criteria

Домен провален, если decision vocabulary распадается на competing models, если score becomes action, если escalation считается ошибкой, или если decision output нельзя проверить дальше.

Supporting Evidence

| Statement | Source |
| --- | --- |
| V7 Decision Model defines how V7 should make, expose, escalate, and learn from decisions. | `docs/reference/V7_DECISION_MODEL.md`, `Purpose`. |
| Decision output vocabulary includes KEEP, MOVE, FAILOVER, DRAIN, QUARANTINE, RECOVER, PROBE_ONLY, ASK_OPERATOR, and NO_ACTION. | `docs/reference/V7_DECISION_MODEL.md`, `Decision Vocabulary`. |
| A system must separate choosing an action from executing that action. | `docs/reference/V7_DECISION_MODEL.md`, `Universal Engineering Laws`, `Law 1`; `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW U3`. |

Domain:

Decision Model

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 13 — Policy

Status

DRAFT

Definition

Policy - это домен, который переводит product intent и business objectives в operational boundaries. Policy определяет, какие действия допустимы, какие условия должны блокировать действие, какие риски приемлемы и какие исключения требуют человеческого решения.

Purpose

Policy существует, чтобы V7 не действовал только потому, что действие технически возможно. Он связывает пользовательскую ценность, бизнесовый риск, safety, свежийness, reversibility, authority and scale limits.

Responsibilities

Домен отвечает за constraints, guardrails, fail-open/fail-closed semantics, SLA/service/user fit, risk appetite и explicit exception boundaries. Он не отвечает за producing observations, selecting candidate, approving authority expansion, runtime execution or verifying outcomes.

Relationships

Policy получает вход от Business Objective, Product Principles, System Laws и Decision Model. Его потребляют Planner, Authority, Runtime и Certification domains. Policy не должен быть raw product text внутри runtime; он должен быть переведен в operational rules до action.

System Laws

Домен ограничен законами Humans Own Policy Boundaries, Authority Before Production Mutation, Safety Before Confidence, Unknown Is Not Pass And Not Fail, Durable Truth Has One Canonical Owner and Existing Owner Before New Owner.

Success Criteria

Policy успешен, если technically possible actions are constrained by approved business risk, safety, service priority, свежийness, blast radius and exception rules before they can proceed.

Failure Criteria

Домен провален, если raw product wishes become direct execution input, если exceptions скрыты, policy дублируется между owners или safety behavior неоднозначен.

Supporting Evidence

| Statement | Source |
| --- | --- |
| Business Objectives are translated through Canonical Policies into operational rules. | `docs/product/V7_PRODUCT_SPECIFICATION.md`, `Business Objectives`, `Policy Translation`. |
| Policy constraints must be evaluated before an action is exposed as safe. | `docs/reference/V7_DECISION_MODEL.md`, `Universal Engineering Laws`, `Law 2`. |
| The Canonical Policy Library is the permanent source for operational behavior policy. | `docs/reference/V7_CANONICAL_REFERENCE.md`, `Product Specification Rule`. |

Domain:

Policy

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 14 — Planner

Status

DRAFT

### 1. Definition

Planner - это домен, который превращает доказанную ситуацию и ограничения в candidate action или stop outcome. Он выбирает допустимое направление с учетом текущей реальности, desired product state, policy constraints, health evidence, risk, blast radius и readiness. Planner не выполняет production action.

### 2. Purpose

Planner нужен, чтобы V7 не действовала реактивно и не смешивала диагноз с исполнением. Он формирует структурированное намерение: что можно сделать, для кого, зачем, с каким expected benefit и почему это не должно нарушить Product Principles.

### 3. Responsibilities

Домен отвечает за выбор или отказ от выбора action candidate внутри доступной evidence и policy. Он не отвечает за authority admission, committed identity lock, runtime execution, verification или rollback closure.

### 4. Relationships

Planner получает Diagnosis и Incident context, использует Health Evidence и передает выбранное намерение в Authority. Он должен сохранять связь с предыдущими доменами и не превращать план в действие.

### 5. System Laws

Домен ограничен законами Decision Is Not Execution, Safety Before Confidence, Blast Radius Before Scale, Freshness Matches Action Risk, Object Continuity и Retry/Evidence constraints как часть broader system laws.

### 6. Success Criteria

Planner успешен, если candidate action объясним, ограничен incident/product context, не выходит за evidence, не выбирает exhausted или unrelated action и явно сообщает stop, когда безопасного candidate нет.

### 7. Failure Criteria

Planner провален, если выбирает действие без достаточной evidence, повторяет known-bad semantic attempt, меняет incident scope, выдает plan как execution или скрывает blockers.

### 8. Supporting Evidence

| Statement | Source |
| --- | --- |
| Decision Model defines how V7 should make, expose, escalate, and learn from decisions; it is documentation-only and does not create execution authority. | `docs/reference/V7_DECISION_MODEL.md`, `Purpose`. |
| Decision systems separate current state, desired state, policy constraints, health, evidence quality, user/service relevance, risk, authority, rollback, verification readiness, and outcome history. | `docs/reference/V7_DECISION_MODEL.md`, `Decision Inputs`. |
| A plan, recommendation, candidate, score, or selected move is not production execution. | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW U3`. |

Domain:

Planner

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 15 — Authority

Status

DRAFT

Definition

Authority - это домен, который определяет, имеет ли V7 право продолжить выбранное намерение внутри утвержденного класса, масштаба, риска, policy boundary, blast-radius boundary и certification boundary. Authority не доказывает, что действие полезно или успешно; оно доказывает, что системе позволено продолжить в данном классе и масштабе.

Purpose

Authority существует, чтобы product autonomy росла безопасно и управляемо. Даже если evidence strong, decision good and technical action possible, production-изменение должно оставаться внутри approved scope, action class, risk appetite, staged maturity and delegated policy limits.

Responsibilities

Домен отвечает за admission, refusal, approval boundary, action-class authority, delegated autonomy boundaries, blast-radius budget, staged scale, exception handling, authority expansion recommendations и refusal outside scope. Он не отвечает за observation, planning quality, identity continuity, runtime execution, verification, rollback или learning. Он также не расширяет собственные полномочия автоматически.

Relationships

Authority получает candidate и policy context от Decision Model, Planner and Policy. Он либо допускает candidate дальше к Identity, либо останавливает с объяснимой boundary. Его output потребляют Identity, Runtime and Execution. Authority expansion может быть рекомендована только после certified outcomes and human/policy approval там, где он требуется.

System Laws

Домен ограничен законами Authority Before Production Mutation, Blast Radius Before Scale, Evidence Before Capability, Humans Own Policy Boundaries, Safety Before Confidence, Exceptions And Architecture Boundaries and Incremental Evolution.

Success Criteria

Authority успешен, если каждое разрешенное действие has explicit scope, class, risk boundary and scale limit, and каждое refused action имеет понятную boundary reason. Broad action не должен проходить как small scope, а exception должен быть явно назван.

Failure Criteria

Домен провален, если V7 self-approves policy expansion, if packet approval is mistaken for durable product authority, if broad actions bypass staged certification, if technical possibility becomes production permission, or if authority becomes hidden inside another domain.

Supporting Evidence

| Statement | Source |
| --- | --- |
| Action-Class Authority becomes the primary V7 approval model; packets are fresh, bounded, validated, ephemeral execution artifacts. | `docs/decisions/ADR-V7-ACTION-CLASS-AUTHORITY.md`, `Decision`. |
| Authority expansion is never automatic and may be recommended only after certified outcomes. | `docs/decisions/ADR-V7-OMP-PRODUCTION-PROGRAM.md`, `Decision`. |
| The number, scope and class of production objects affected by automation must be explicitly bounded. | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW A1`. |

Domain:

Authority

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 16 — Identity

Status

DRAFT

Definition

Identity - это домен, который сохраняет, какой именно production-объект, incident, пользователь, source, target, action, generation and selected move рассматриваются на каждом этапе. Identity отвечает за committed continuity выбранного и разрешенного действия до исполнения, verification, rollback and learning, чтобы downstream-домены не начали молча говорить о разных объектах.

Purpose

Identity существует, чтобы V7 могла доказать непрерывность от evidence до decision, authority, runtime, execution, verification and learning. Без identity система может честно пройти несколько правильных стадий, но в конце применить, проверить или записать outcome для другого объекта.

Responsibilities

Домен отвечает за subject continuity, incident continuity, selected object continuity, generation continuity, immutability of committed execution identity, mismatch detection and explicit restart when identity changes. Он не отвечает за selecting action, approving authority, applying mutation, verifying service outcome or learning maturity.

Relationships

Identity получает context from Incident, Decision Model, Planner and Authority. Его потребляют Runtime, Execution, Verification, Rollback / Closure and Learning. Он является shared contract across domains, not an action owner.

System Laws

Домен ограничен законами Object Continuity, Decision Is Not Execution, Unknown Is Not Pass And Not Fail, Reports Preserve Evidence Not Authority and Durable Truth Has One Canonical Owner.

Success Criteria

Identity успешен, если every domain can prove it handled the same object or explicitly stopped on mismatch.

Failure Criteria

Домен провален, если investigation switches candidate silently, if execution applies different object than approved, if verification checks different contract, if incident scope is lost, or if learning records outcome under wrong identity.

Supporting Evidence

| Statement | Source |
| --- | --- |
| The same execution object must preserve user, source, target, action, generation, selected move hash, and incident identity through all owners. | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW R2`. |
| V7 final target includes preserving committed identity through the approval and restore boundary before apply. | `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`, `Final Autonomous Target`. |
| Function Graph validation shows identity-related tests and owner surfaces around packet, approval binding, selected hash, source/target scope and execution lease. | `docs/reports/research/V7_AUTONOMOUS_MODEL_FUNCTION_GRAPH_APPENDIX.md`, identity/approval/packet test references. |

Domain:

Identity

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 17 — Runtime

Status

DRAFT

Definition

Runtime - это thin live boundary of V7 that consumes prepared, approved, locked and fresh decision artifacts and either allows execution safely or stops. Runtime не является местом для broad research, изобретения product policy, authority expansion, historical recomputation or final verification proof.

Purpose

Runtime существует, чтобы production action under pressure stayed bounded, fast, explainable and safe. В момент действия система должна потреблять подготовленное знание, но заново проверять live safety boundaries, current eligibility, authority, identity, verification readiness and rollback readiness.

Responsibilities

Домен отвечает за execute-or-stop semantics, live gate enforcement, respect for locked identity, thin consumption of prepared knowledge, bounded mutation admission and handoff to execution/verification/rollback outcomes. Он не отвечает за creating decision, broad diagnosis, policy expansion, authority expansion, actual success proof or long-term learning.

Relationships

Runtime получает input от Identity, Authority, Policy and prepared Intelligence. Execution потребляет разрешенный Runtime path. Verification and Rollback / Closure потребляют результат. Learning and Current Program State потребляют terminal outcomes.

System Laws

Домен ограничен законами Decision Is Not Execution, Runtime Safety, Authority Before Production Mutation, Verification Completes Mutation, Rollback Or Closure Is Mandatory and Freshness Matches Action Risk.

Success Criteria

Runtime успешен, если он allows only committed approved identity inside current safety boundaries or safely stops with clear reason.

Failure Criteria

Runtime провален, если it invents decisions, recomputes broad planning, bypasses authority, applies stale identity, treats apply as verified success or continues without rollback/verification readiness.

Supporting Evidence

| Statement | Source |
| --- | --- |
| Runtime executes already-approved decisions and does not invent decisions. | `docs/reference/V7_RUNTIME_MODEL.md`, `Purpose`. |
| Runtime must stay thin and spend prepared knowledge. | `docs/reference/V7_RUNTIME_MODEL.md`, `Runtime Laws`; `docs/reference/V7_DECISION_MODEL.md`, `Universal Engineering Laws`, `Law 4`. |
| Runtime applies only committed approved identity or stops safely. | `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`, `Fundamental Autonomy Laws`. |

Domain:

Runtime

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 18 — Execution

Status

DRAFT

Definition

Execution - это фактический production-impacting step, который меняет reality или намеренно останавливается до изменения. Он уже, чем Runtime: Runtime управляет execute-or-stop semantics, а Execution является моментом, где committed allowed action применяется или отклоняется.

Purpose

Execution нужен, чтобы у V7 была ясная граница между approved intent and changed production reality. Этот домен не дает путать reports, previews, recommendations, authority objects and runtime admission with actual mutation.

Responsibilities

Домен отвечает за применение committed action only when allowed, bounded mutation, touched-object scope, execution result disclosure and prohibition against hiding no-op/stop as success. Он не отвечает за choosing action, authorization, verification user-visible outcome or learning maturity.

Relationships

Execution получает input от Runtime and Identity. Verification потребляет execution result. Rollback / Closure потребляет failed or unsafe execution outcomes. Learning consumes terminal closure, not raw apply by itself.

System Laws

Домен ограничен законами Decision Is Not Execution, Authority Before Production Mutation, Object Continuity, Verification Completes Mutation and Rollback Or Closure Is Mandatory.

Success Criteria

Execution успешен, если actual mutation happens only for locked approved object or safely does not happen, and downstream domains can verify exactly what was touched.

Failure Criteria

Execution провален, если он меняет production без authority, затрагивает wrong object, скрывает no-op как success, пропускает verification или оставляет touched objects untracked.

Supporting Evidence

| Statement | Source |
| --- | --- |
| A production change is incomplete until independent verification proves outcome. | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW U4`. |
| A plan, recommendation, candidate, score, or selected move is not production execution. | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW U3`. |
| Runtime executes, stops, verifies, rolls back, records outcomes and feeds learning only through existing owners. | `docs/reference/V7_RUNTIME_MODEL.md`, `Purpose`. |

Domain:

Execution

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 19 — Verification

Status

DRAFT

### 1. Definition

Verification - это домен, который доказывает фактический outcome после production action. Он отвечает не за то, была ли команда запущена, а за то, достигнут ли пользовательский и contract-level результат, который оправдывает доверие к изменению.

### 2. Purpose

Verification нужен, чтобы V7 не путала action completed с service restored. Без независимой проверки система может объявить успех, когда пользователь по-прежнему не получил working connectivity.

### 3. Responsibilities

Домен отвечает за проверку того же contract, который был selected, admitted, locked and executed; сохранение raw outcome class; различение pass, fail and unknown. Он не отвечает за planning, authority, execution or rollback decision beyond its verified result.

### 4. Relationships

Verification получает execution outcome от Runtime and Execution и передает доказанный result в Rollback / Closure. Он должен сохранять Object Continuity и не менять критерий успеха задним числом.

### 5. System Laws

Домен ограничен законами Verification Completes Mutation, Unknown Is Not Pass And Not Fail, Object Continuity, Freshness Matches Action Risk and Learn From Terminal Outcomes.

### 6. Success Criteria

Домен успешен, если outcome проверен по тому же object and contract, unknown явно отделен от fail/pass, а result достаточно доказателен для closure, rollback или learning.

### 7. Failure Criteria

Домен провален, если проверяет другой сервис, другой user, другой target, трактует timeout как service fail без доказательства, или позволяет считать непроверенный apply успешным.

### 8. Supporting Evidence

| Statement | Source |
| --- | --- |
| A production change is incomplete until independent verification proves its outcome. | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW U4`. |
| Verification must evaluate the same required services, user, source, target, and action class that planning and runtime used. | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW V1`. |
| Timeout, missing data, stale data, lock wait, or unpersisted object must be classified as unknown unless evidence proves pass or fail. | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW V2`. |

Domain:

Verification

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 20 — Rollback / Closure

Status

DRAFT

### 1. Definition

Rollback / Closure - это домен, который доводит production mutation до безопасного terminal состояния. Если verification показывает failure, unsafe outcome or unacceptable unknown, система должна компенсировать, contain or stop safely. Если действие успешно или rollback невозможен по сертифицированной причине, домен должен закрыть результат как safe closure or certified no-rollback closure. Rollback не является time travel; он operationally закрывает риск.

### 2. Purpose

Rollback / Closure нужен, чтобы V7 не оставляла пользователей, каналы, incidents or touched production objects в unsafe, unknown or незакрытом состоянии. Production-система должна знать, что произошло с каждым touched object после действия, and future decisions must consume only closed evidence.

### 3. Responsibilities

Домен отвечает за safe compensation, containment, touched-object tracking, rollback result, no-rollback closure, partial outcome preservation, terminal safety state and evidence for closure. Он не отвечает за initial decision, authority approval, execution admission, verification probe design or long-term maturity.

### 4. Relationships

Rollback / Closure получает verified result and execution outcome when result requires compensation or closure. Learning consumes terminal outcome. Production Maturity consumes only closed evidence. Он завершает action cycle before maturity or autonomy can grow.

### 5. System Laws

Домен ограничен законами Rollback Or Closure Is Mandatory, Verification Completes Mutation, Unknown Is Not Pass And Not Fail, Partial Success as Outcome, Negative Evidence Is Evidence and Learn From Terminal Outcomes.

### 6. Success Criteria

Домен успешен, если каждый failed, unsafe or touched object reaches safe terminal state: restored, contained, rolled back, safely closed or explicitly impossible. Partial success must remain per-object, not hidden under one batch label, and evidence remains available for Learning and Production Maturity.

### 7. Failure Criteria

Домен провален, если failed action remains open, residual risk is ignored, successful and failed batch objects collapse into ambiguous state, failed objects are not contained, or rollback/no-rollback success is assumed without evidence.

### 8. Supporting Evidence

| Statement | Source |
| --- | --- |
| Every mutation must have rollback, containment, or certified no-rollback closure. | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW U5`. |
| Rollback restores a safe operational state; it does not erase all side effects. | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW RB1`. |
| Partial success is a first-class outcome and must preserve per-object outcome. | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW RB2`. |

Domain:

Rollback / Closure

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 21 — Learning

Status

DRAFT

### 1. Definition

Learning - это домен, который превращает terminal outcomes в future evidence. Он не учится на ожиданиях, намерениях или непроверенных отчетах; он учится на закрытых реальных исходах: success, rollback, stop, unknown, hold, block, partial success and canonical impossibility.

### 2. Purpose

Learning нужен, чтобы V7 становился лучше после каждого production или certification результата. Без learning система будет повторять known-bad attempts, завышать maturity or ignore evidence boundaries.

### 3. Responsibilities

Домен отвечает за сохранение outcome meaning, feeding future decisions, maturity impact, authority recommendations, automation candidates and regression knowledge. Он не отвечает за executing action, verifying outcome or approving authority expansion.

### 4. Relationships

Learning получает terminal state от Rollback / Closure и передает evidence в Production Maturity, Current Program State and future planning. Он замыкает product loop from reality back to improved future behavior.

### 5. System Laws

Домен ограничен законами Learn From Terminal Outcomes, Negative Evidence Is Evidence, Evidence Before Capability, Reports Preserve Evidence Not Authority and Humans Own Policy Boundaries.

### 6. Success Criteria

Домен успешен, если every terminal outcome changes future knowledge appropriately, known bad paths are not repeated blindly, and maturity/authority never improve from unverified opinions.

### 7. Failure Criteria

Домен провален, если система забывает rollback, повторяет exhausted attempt, treats report as capability, or learns maturity from synthetic or unverified evidence.

### 8. Supporting Evidence

| Statement | Source |
| --- | --- |
| Every terminal outcome must become learning evidence for future planning, authority, maturity, or automation decisions. | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW L1`. |
| Stops, rollbacks, unknowns, and blocks are evidence about capability boundaries. | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW L2`. |
| Decision confidence may improve only from observed outcomes, not synthetic evidence or operator wishes. | `docs/reference/V7_DECISION_MODEL.md`, `Universal Engineering Laws`, `Law 10`. |

Domain:

Learning

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 22 — Production Maturity

Status

DRAFT

### 1. Definition

Production Maturity - это домен, который отражает доказанную production-способность V7. Он не создает capability and does not approve action; it consumes real evidence, certification results, verified outcomes and authority decisions to state how mature the system actually is.

### 2. Purpose

Production Maturity нужен, чтобы V7 отличала "мы понимаем систему" от "система действительно автономна в production". Engineering completeness, documentation and research do not equal production autonomy.

### 3. Responsibilities

Домен отвечает за maturity scoring, production readiness interpretation, certified autonomy state and evidence consumption. Он не отвечает за producing evidence, approving action, moving users, creating runtime behavior or creating backlog by itself.

### 4. Relationships

Production Maturity получает evidence from Learning and certification outcomes, then informs Current Program State and OMP. It must not replace the producer domains.

### 5. System Laws

Домен ограничен законами Evidence Before Capability, Learn From Terminal Outcomes, Reports Preserve Evidence Not Authority, Durable Truth Has One Canonical Owner and Incremental Evolution.

### 6. Success Criteria

Домен успешен, если maturity reflects real outcomes, separates engineering maturity from production autonomy, and refuses synthetic-only or report-only evidence.

### 7. Failure Criteria

Домен провален, если maturity hand-edited as opinion, if documentation completion is treated as production autonomy, or if maturity grants execution permission.

### 8. Supporting Evidence

| Statement | Source |
| --- | --- |
| `100%` Production Maturity means `PRODUCTION_AUTONOMY_CERTIFIED`. | `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md`, `Purpose`. |
| Engineering Maturity and Production Maturity must never be merged; architecture/research/policy/model completion does not prove production autonomy. | `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md`, `Separation Rule`. |
| Production Maturity consumes evidence and maturity impact; it does not replace producers. | `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`, `Fundamental Autonomy Laws`; `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md`, `Product Evolution Behavior Contract`. |

Domain:

Production Maturity

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 23 — Current Program State

Status

DRAFT

### 1. Definition

Current Program State - это volatile snapshot текущего положения V7: current bottleneck, capability state, blocker, next action, current maturity signal and active execution context. It is not a truth source, not authority and not a roadmap.

### 2. Purpose

Current Program State нужен, чтобы будущая работа могла продолжиться без потери контекста. Он отвечает на вопрос: "где V7 находится сейчас и что должно произойти дальше?"

### 3. Responsibilities

Домен отвечает за видимость текущего состояния, раскрытие blockers, ясность следующего шага и синхронизацию с earned reality. Он не отвечает за утверждение действия, расширение authority, производство evidence, создание product meaning или замену OMP.

### 4. Relationships

Current Program State получает состояние от Production Maturity, Learning и текущих missions, затем информирует OMP и human handoff. Он должен отражать reality после завершения producers, а не блокировать capability только из-за незавершенной синхронизации документации, если этого не требует safety.

### 5. System Laws

Домен ограничен законами Reality First, Reports Preserve Evidence Not Authority, Durable Truth Has One Canonical Owner, Evidence Before Capability and Negative Evidence Is Evidence.

### 6. Success Criteria

Домен успешен, если любой future session can see current phase, blocker, owner resolution, current capability and next step without treating Current Program State as permission.

### 7. Failure Criteria

Домен провален, если stale state вводит работу в заблуждение, выдает authority, скрывает blockers или становится вторым roadmap/truth source.

### 8. Supporting Evidence

| Statement | Source |
| --- | --- |
| Current Program State stores current operational reality only and must not approve Runtime apply, expand authority, enable automation, move users, or create owners. | `docs/programs/V7_CURRENT_PROGRAM_STATE.md`, `Purpose`, `Prohibited Behavior`. |
| Current Program State records current evidence and blocker, but cannot approve action. | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW U1`, current state impact. |
| Current Program State is the current GPS position and autonomy inventory, while OMP is the navigator and execution engine. | `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`, `Executive Summary`. |

Domain:

Current Program State

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 24 — OMP

Status

DRAFT

### 1. Definition

OMP - это постоянная operating program система V7: она выбирает next mission, направляет работу существующим владельцам, потребляет evidence и maturity, предотвращает duplicate roadmaps и поддерживает продолжение. В этой Phase 1 книге OMP является координационным доменом, а не новой архитектурой.

### 2. Purpose

OMP нужен, чтобы V7 не останавливалась после отчета, blocker или partial implementation. Он превращает evidence, blockers, maturity gaps и authority boundaries в следующую governed mission.

### 3. Responsibilities

Домен отвечает за continuation, routing missions, production maturity ladder, authority evaluation как program process, implementation prioritization и предотвращение ownerless work. Он не отвечает за создание production evidence, выполнение runtime action, verification outcome или замену canonical owners.

### 4. Relationships

OMP потребляет Current Program State и Production Maturity, затем определяет, какая работа продолжается дальше. Он поддерживает Continuous Self Evolution, но не должен становиться duplicate owner предыдущих доменов.

### 5. System Laws

Домен ограничен законами Existing Owner Before New Owner, Durable Truth Has One Canonical Owner, Negative Evidence Is Evidence, Evidence Before Capability, Human Boundary and Incremental Evolution.

### 6. Success Criteria

Домен успешен, если каждый blocker становится классифицированной работой, каждый capability gap направляется существующему владельцу, а программа продолжается до pass, hold, block with resolution или canonical impossibility.

### 7. Failure Criteria

Домен провален, если он создает parallel roadmaps, останавливается на reports, принимает owner block как terminal без resolution или считает documentation capability.

### 8. Supporting Evidence

| Statement | Source |
| --- | --- |
| OMP becomes the permanent production operating program and single execution program for V7. | `docs/decisions/ADR-V7-OMP-PRODUCTION-PROGRAM.md`, `Decision`. |
| OMP preserves what V7 does next and follows Reality First, Discover-Reuse-Extend-Implement, tests before certification, certification before next phase, documentation after implementation, and automatic continuation where possible. | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`, `Project Vision`, `Program Principles`. |
| OMP converts gaps into missions and routes them to existing owners. | `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`, `Fundamental Autonomy Laws`, `OMP Relationship`. |

Domain:

OMP

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 25 — Engineering Automation

Status

DRAFT

### 1. Definition

Engineering Automation - это домен, который превращает повторяющуюся ручную инженерную работу into управляемые пайплайны, закрепленные за владельцами or классификации намеренно ручной работы. Он улучшает то, как V7 строится, сертифицируется, разворачивается, расследуется и синхронизируется, но не обходит production-безопасность.

### 2. Purpose

Engineering Automation нужен, чтобы V7 не оставалась зависимой от ручной оркестрации Codex или администратора. По мере роста production-capability инженерная система должна сокращать повторяющиеся цепочки команд, ручную синхронизацию отчетов, regression toil и investigation toil.

### 3. Responsibilities

Домен отвечает за Automation Audit, Workflow Audit, automation debt, workflow debt, pipeline candidates, backtesting анализаторов и минимизацию команд. Он не отвечает за production mutation, runtime authority, product policy или обход safety owners.

### 4. Relationships

Engineering Automation потребляет OMP-миссии и доказательства повторяющихся workflows, затем питает Continuous Self Evolution. Он обязан соблюдать Product Principles и System Laws: допустима только безопасная automation в границах существующих владельцев.

### 5. System Laws

Домен ограничен законами Repeated Manual Work Is Debt Until Classified, Automation Must Be Suspendable, Existing Owner Before New Owner, Reports Preserve Evidence Not Authority and Humans Own Policy Boundaries.

### 6. Success Criteria

Домен успешен, если повторяющиеся ценные workflows становятся безопаснее, проще, закреплены за владельцами и проверены, а низкоценная или требующая человеческого суждения работа явно классифицирована как намеренно ручная или экономически нецелесообразная.

### 7. Failure Criteria

Домен провален, если повторяющаяся работа остается необъясненной, automation превращается в личный скрипт или Codex-only workflow, либо обходит владельцев ради видимой скорости.

### 8. Supporting Evidence

| Statement | Source |
| --- | --- |
| V7 should evolve from Codex-orchestrated engineering into owner-backed governed engineering pipelines. | `docs/reports/research/V7_AUTONOMOUS_ENGINEERING_SYSTEMS_RESEARCH.md`, `Summary`. |
| Every manual action triggers an Automation Audit; unexplained manual work is Automation Debt. | `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`, `Automation Evolution`. |
| Repeated manual action or workflow is automation/workflow debt until classified. | `docs/reports/research/V7_MASTER_AUTONOMOUS_SYSTEM_LAWS.md`, `LAW E1`, `LAW H2`. |

Domain:

Engineering Automation

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Domain 26 — Continuous Self Evolution

Status

DRAFT

### 1. Definition

Continuous Self Evolution - это домен, который описывает, как V7 становится лучше после каждого реального цикла. Он объединяет capability evolution, automation evolution и workflow evolution в один непрерывный контур улучшения.

### 2. Purpose

Continuous Self Evolution нужен, чтобы V7 не завершалась документом, отчетом или single certification result. Каждый реальный процесс должен создавать evidence, каждое evidence должно улучшать capability или классифицировать границу, а каждый повторяющийся ручной workflow должен становиться кандидатом на более безопасное системное улучшение.

### 3. Responsibilities

Домен отвечает за замкнутое улучшение: reality создает evidence, evidence создает capability, capability меняет authority или maturity, outcomes создают learning, learning создает следующие missions, а повторяющаяся ручная работа создает automation или workflow decisions. Он не отвечает за утверждение policy, создание новых владельцев или выдачу autonomy без evidence.

### 4. Relationships

Continuous Self Evolution следует после Engineering Automation и возвращается к Business Objective через улучшенную пользовательскую связность, снижение операторской работы и более безопасную сертифицированную автономию. Он не переопределяет предыдущие домены, а гарантирует, что их terminal outcomes становятся входом следующего цикла.

### 5. System Laws

Домен ограничен законами Learn From Terminal Outcomes, Evidence Before Capability, Incremental Evolution, Existing Owner Before New Owner, Automation Must Be Suspendable and Humans Own Policy Boundaries.

### 6. Success Criteria

Домен успешен, если ни один terminal outcome не исчезает молча, capability улучшается на реальных outcomes, automation debt классифицирован, workflow debt классифицирован, а future missions становятся проще, безопаснее и лучше закреплены за владельцами.

### 7. Failure Criteria

Домен провален, если отчеты завершают процесс, blockers не превращаются в missions или классифицированные границы, manual workflows остаются необъясненными, либо V7 постоянно нуждается в routine Codex orchestration.

### 8. Supporting Evidence

| Statement | Source |
| --- | --- |
| V7 final target includes learning from every terminal outcome, updating current state/maturity, creating missions from gaps, certification workflows, documentation sync after capability earned, classifying repeated manual actions/workflows, and improving the engineering system. | `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md`, `Final Autonomous Target`. |
| Every process ends by becoming input to another process: Reality -> Evidence -> Capability -> Authority -> Production -> Certification -> Automation Audit -> Workflow Audit -> Next Mission. | `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`, `Continuous Process`. |
| V7 gets better forever through reality, evidence, decisions, verification, learning, policy, maturity, and more reality. | `docs/product/V7_PRODUCT_SPECIFICATION.md`, `Why V7 Gets Better Forever`, `Autonomy Promotion Engine`. |

Domain:

Continuous Self Evolution

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

## Phase 1 Consistency Report

Status

DRAFT

### Terminology Consistency

Терминология согласована для owner review: Business Objective остается продуктовым источником смысла, System Laws остаются универсальными ограничениями, Reality Model удерживает evidence, а последующие домены потребляют предыдущие определения вместо повторного переопределения.

### Duplicate Definitions

Architecture Tree Audit материализован. Дублирующие draft-домены больше не существуют как самостоятельные домены:

- Authority Admission merged into Authority;
- Identity Lock merged into Identity;
- Runtime Execution split into Runtime and Execution;
- Rollback merged into Rollback / Closure.

### Unique Responsibility

Каждый финальный домен имеет отдельную review responsibility:

- Intelligence готовит background knowledge.
- Routing Intelligence предоставляет advisory routing knowledge.
- Decision Model определяет язык решений.
- Policy переводит product intent в operational boundaries.
- Authority допускает или отклоняет action scope.
- Identity сохраняет object continuity.
- Runtime обеспечивает execute-or-stop semantics.
- Execution является actual mutation/no-mutation boundary.
- Verification доказывает фактический outcome.
- Rollback / Closure закрывает touched objects в terminal safe state.

### Architecture Contradictions

Новая architecture не вводилась. Structural overlap, возникший из-за последовательного добавления broad и narrow draft-доменов, устранен через материализацию Architecture Tree Audit.

### Supporting Evidence

Каждый финальный домен содержит supporting evidence. Function Graph и Function Graph Appendix использовались только как validation того, что intelligence, routing intelligence, identity, runtime, execution, verification, rollback/closure и authority существуют как связанные project surfaces; implementation details не копировались в основной текст.

### Upstream And Downstream Relationships

Каждый финальный домен называет upstream и downstream consumers на architecture level. В основном тексте не описывались code, APIs, functions или classes.

Domain:

Phase 1 Consistency Report

Status:

DRAFT

Approved:

NO

Ready For Owner Review:

YES

# Phase 1

## Architecture Tree Audit

Status:

DRAFT

### 1. Audit Scope

This audit certifies only the domain structure of the future V7 Ideal Autonomous System Model.

It does not review wording, does not rewrite domains, does not improve prose, does not synchronize canonical documents, and does not create implementation work.

Domain nodes found before materialization: `30`.

### 2. Domain Independence Matrix

| Domain | Truly independent? | Duplicates another domain? | Recommendation | Canonical domain if merged | Position change? | New domain required? |
| --- | --- | --- | --- | --- | --- | --- |
| 01 Business Objective | YES | NO | remain | n/a | keep `01` | NO |
| 02 System Laws | YES | NO | remain | n/a | keep `02` | NO |
| 03 Product Principles | YES | NO | remain | n/a | keep `03` | NO |
| 04 Reality Model | YES | NO | remain | n/a | keep `04` | NO |
| 05 Observation | YES | NO | remain | n/a | keep `05` | NO |
| 06 Health Evidence | YES | NO | remain | n/a | keep `06` | NO |
| 07 Wake | YES | NO | remain | n/a | move after Intelligence and Routing Intelligence in final tree only if the owner prefers knowledge-before-event ordering; otherwise keep after Health Evidence | NO |
| 08 Incident | YES | NO | remain | n/a | after Wake | NO |
| 09 Diagnosis | YES | NO | remain | n/a | after Incident | NO |
| 10 Planner | YES | partial overlap with Decision Model only in decision language | remain | n/a | after Decision Model and Policy | NO |
| 11 Authority Admission | NO | Authority | merge | Authority | remove as independent node | NO |
| 12 Identity Lock | NO | Identity | merge | Identity | remove as independent node | NO |
| 13 Runtime Execution | NO | Runtime and Execution | split/merge | Runtime and Execution | remove as independent node | NO |
| 14 Verification | YES | NO | remain | n/a | after Execution | NO |
| 15 Rollback / Closure | YES | Rollback partially duplicates it | remain as canonical | Rollback / Closure | after Verification | NO |
| 16 Learning | YES | NO | remain | n/a | after Rollback / Closure | NO |
| 17 Production Maturity | YES | NO | remain | n/a | after Learning | NO |
| 18 Current Program State | YES | NO | remain | n/a | after Production Maturity | NO |
| 19 OMP | YES | NO | remain | n/a | after Current Program State | NO |
| 20 Engineering Automation | YES | NO | remain | n/a | after OMP | NO |
| 21 Continuous Self Evolution | YES | NO | remain | n/a | final domain | NO |
| 22 Intelligence | YES | partial overlap with Routing Intelligence | remain | n/a | move after Health Evidence | NO |
| 23 Decision Model | YES | partial overlap with Planner only in vocabulary | remain | n/a | before Policy and Planner | NO |
| 24 Policy | YES | NO | remain | n/a | after Decision Model and before Planner | NO |
| 25 Authority | YES | Authority Admission | remain as canonical | Authority | after Planner | NO |
| 26 Identity | YES | Identity Lock | remain as canonical | Identity | after Authority | NO |
| 27 Routing Intelligence | YES | partial overlap with Intelligence | remain | n/a | after Intelligence and before Wake/Planner consumers | NO |
| 28 Runtime | YES | Runtime Execution partially duplicates it | remain as canonical | Runtime | after Identity | NO |
| 29 Execution | YES | Runtime Execution partially duplicates it | remain as canonical | Execution | after Runtime | NO |
| 30 Rollback | NO | Rollback / Closure | merge | Rollback / Closure | remove as independent node | NO |

### 3. Merge Decisions

#### 3.1 Authority Admission -> Authority

Why they overlap:

Both domains answer the same architectural question: whether a proposed production-impacting action is allowed inside the current approved scope, class, risk boundary, policy boundary, and blast-radius boundary.

Duplicated responsibility:

Admission, refusal, scope boundary, authority ceiling, and policy-risk admission are duplicated.

Canonical survivor:

Authority.

Why:

Authority is the broader and more durable domain name. It can include admission, refusal, authority class, delegated policy, blast radius, expansion recommendation, and exceptional boundary handling. Keeping a separate Authority Admission domain would make admission look like a second authority owner.

#### 3.2 Identity Lock -> Identity

Why they overlap:

Both domains preserve object continuity across planning, approval, runtime, verification, rollback, and learning.

Duplicated responsibility:

Subject identity, source/target identity, action identity, incident identity, generation identity, and mismatch detection.

Canonical survivor:

Identity.

Why:

Identity is the more general architecture domain. Identity Lock is a mechanism-level expression of the same responsibility. The future ideal model should name the invariant, not one particular locking concept.

#### 3.3 Runtime Execution -> Runtime + Execution

Why split:

Runtime Execution contains two separate responsibilities.

Runtime owns the execute-or-stop live safety boundary.

Execution owns the actual mutation/no-mutation boundary where approved intent either changes production reality or safely does not.

Why separation improves architecture:

Runtime can remain a thin enforcement domain, while Execution remains the concrete production transition. This preserves the system law Decision Is Not Execution and avoids treating Runtime as both gate and mutation outcome.

Resulting domains:

- Runtime.
- Execution.

Canonical survivors:

Runtime and Execution.

#### 3.4 Rollback -> Rollback / Closure

Why they overlap:

Rollback is one terminal safety path. Closure is the broader terminal responsibility that also includes containment and certified no-rollback closure.

Duplicated responsibility:

Compensation after failed or unsafe execution, terminal safety state, touched-object closure, and evidence for Learning and Production Maturity.

Canonical survivor:

Rollback / Closure.

Why:

The system law is not merely "rollback"; it is "rollback, containment, or certified closure." The canonical domain must preserve the broader responsibility so no touched production object remains open.

### 4. Non-Merge Decisions

#### 4.1 Planner and Decision Model remain separate

Planner and Decision Model overlap only in language, not responsibility.

Decision Model defines vocabulary, input separation, escalation semantics, and decision shape.

Planner uses those semantics to propose or refuse a candidate action.

They should not merge because merging them would confuse decision language with action selection.

#### 4.2 Intelligence and Routing Intelligence remain separate

Intelligence is general prepared knowledge.

Routing Intelligence is specialized advisory knowledge about route, service, user, target, suitability, trust, and pool context.

They should not merge because Function Graph validation shows routing intelligence is a distinct connected advisory surface, while Intelligence is broader background knowledge.

#### 4.3 Runtime and Execution remain separate

Runtime enforces execute-or-stop eligibility.

Execution is the actual production transition.

They should not merge because the architecture needs a clear line between live admission/enforcement and mutation/no-mutation reality.

#### 4.4 Policy and Authority remain separate

Policy defines operational boundaries derived from product intent.

Authority decides whether an action is allowed inside those boundaries at the current certification and risk level.

They should not merge because policy is a rule source and Authority is an admission boundary.

### 5. Removal Decisions

Removed as independent domains in the final tree:

- Authority Admission.
- Identity Lock.
- Runtime Execution.
- Rollback.

These are not deleted from historical draft text in this step. They are only removed from the recommended final architecture tree.

### 6. New Domain Decision

No new domain is required.

Reason:

All responsibilities discovered in project knowledge, Function Graph, CPS, OMP, Production Maturity, research, and reports map into the existing domain set after the recommended merges and split.

Adding another domain would duplicate one of these already-covered responsibilities:

- product intent;
- universal law;
- reality/evidence;
- prepared intelligence;
- event/incident/diagnosis;
- decision/planning/policy/authority;
- identity/runtime/execution;
- verification/closure/learning;
- maturity/current state/OMP;
- engineering automation/self evolution.

### 7. Final Proposed Tree

01 Business Objective

02 System Laws

03 Product Principles

04 Reality Model

05 Observation

06 Health Evidence

07 Intelligence

08 Routing Intelligence

09 Wake

10 Incident

11 Diagnosis

12 Decision Model

13 Policy

14 Planner

15 Authority

16 Identity

17 Runtime

18 Execution

19 Verification

20 Rollback / Closure

21 Learning

22 Production Maturity

23 Current Program State

24 OMP

25 Engineering Automation

26 Continuous Self Evolution

### 8. Final Validation

Every responsibility appears exactly once:

PASS after applying the recommended merges.

No duplicated responsibility exists:

PASS in the final proposed tree.

Every domain has a single responsibility:

PASS in the final proposed tree.

Domains follow logical architecture order:

PASS. The tree starts from product meaning and universal constraints, moves through reality/evidence/knowledge, then event/incident/diagnosis, then decision/policy/planning/authority, then identity/runtime/execution, then verification/closure/learning, then maturity/state/program/automation/evolution.

Function Graph can map into this tree:

PASS. Function Graph nodes map into intelligence, routing intelligence, decision, planner, authority, identity, runtime, execution, verification, rollback, learning, state, OMP, and engineering automation surfaces. No implementation-only domain is required.

OMP can execute against this tree:

PASS. OMP consumes maturity, current state, blockers, owner routing, automation debt, workflow debt, and capability gaps without becoming a duplicate owner of earlier domains.

CPS can inventory this tree:

PASS. Current Program State can expose current position, capability state, blocker, owner resolution, maturity state, and next mission against these domain names.

Gap Register can compare against this tree:

PASS. The final proposed tree gives stable domain names for gap detection without requiring implementation details.

### 9. Final Verdict

Domains before materialization:

30

Merged:

3

Removed:

1

Added:

0

Final domains:

26

Architecture duplication:

PASS

Architecture completeness:

PASS

Recommended final architecture:

READY

Materialization status:

APPLIED

Live domain headings now match the Final Proposed Tree.

# Phase 1 Architecture Freeze

Status:

APPROVED

Architecture Tree:

FROZEN

Further domain additions:

FORBIDDEN

Further domain removals:

FORBIDDEN

Further domain renaming:

FORBIDDEN

Further domain reordering:

FORBIDDEN

Future work:

Owner Review only.
