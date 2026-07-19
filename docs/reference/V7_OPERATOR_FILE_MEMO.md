# V7 Operator File Memo

Purpose: give the operator one readable place to see which project files matter and what each file is responsible for.

This document is a navigation memo only. It does not replace OMP, SYSTEM_MAP, Canonical Reference, Runtime Model, Decision Model, policies, capability specs, or engineering reports.

## Update Rule

When a durable project document is created or promoted to canonical/project-level use, add it to this memo.

Engineering reports do not need one row per report. Their directory is represented as a report archive entry.

## File Index

| Category | File | What It Is Responsible For | Owner | Update When |
|---|---|---|---|---|
| Program | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` | Main OMP execution program: stages, gates, capability closure, verified consumption, and product execution order. | OMP | OMP rules, stage order, closure law, or capability progression changes. |
| Program | `docs/programs/V7_CURRENT_PROGRAM_STATE.md` | Current volatile program snapshot: current step, blockers, produced capability, next safe action, progress, and operator-facing state. | Current Program State | Current OMP state or production/program status changes. |
| Program | `docs/programs/V7_IMPLEMENTATION_BACKLOG.md` | Existing implementation backlog and actionable capability list. | Implementation Backlog | Backlog item status or capability ownership changes. |
| Program | `docs/programs/V7_IMPLEMENTATION_PROGRAM.md` | Implementation program rules and handoff from architecture to code. | Implementation Program | Implementation lifecycle rules change. |
| Program | `docs/programs/V7_ROUTING_DIGITAL_TWIN_POLYGON_MASTER_PROGRAM.md` | Supporting Master Program plan for autonomous L1-L6 Routing Digital Twin evolution through seven automatically linked OMP Missions; OMP remains execution owner and CPS remains live state. | Existing OMP / FSSE Polygon owners | Polygon fidelity, identity, isolation, autonomous handoff, repair-return, evidence, or certification plan changes. |
| Program | `docs/programs/V7_L7_L8_PRODUCTION_EVIDENCE_AND_AUTHORITY_EVOLUTION_PROGRAM.md` | Proposed bounded program for record-level L7/L8 production evidence, temporal and intent verification, representative Learning, and an owner-consumed action-class Authority recommendation; CPS remains activation owner. | Existing OMP / Production Maturity / Authority owners | L7/L8 evidence acceptance, outcome-passport projection, representativeness, or Authority-recommendation plan changes. |
| Canonical | `docs/reference/V7_CANONICAL_REFERENCE.md` | Highest-level canonical reference and durable truth hierarchy. | Canonical Reference | Durable canonical rules or cross-document truth hierarchy changes. |
| Canonical | `docs/reference/SYSTEM_MAP.md` | Owner map: where responsibilities live and which component owns each concept. | SYSTEM_MAP | Owner mapping, responsibility routing, or canonical location changes. |
| Runtime | `docs/reference/V7_RUNTIME_MODEL.md` | Runtime contracts: fail-closed behavior, live gates, execution safety, freshness, rollback, verification, and runtime limits. | Runtime Model | Runtime contract, gate, or safety invariant changes. |
| Decision | `docs/reference/V7_DECISION_MODEL.md` | Decision lifecycle, decision ownership, identity, commit semantics, and decision-to-runtime boundaries. | Decision Model | Decision identity, planner/decision contract, or commit behavior changes. |
| Autonomy | `docs/reference/V7_AUTONOMOUS_EXECUTION_PROGRAM.md` | Program for autonomous execution maturity and progressive autonomy. | Autonomous Execution Program | Autonomy capability ladder or certification expectations change. |
| Autonomy | `docs/reference/V7_AUTONOMOUS_RUNTIME_MODEL.md` | Autonomous runtime operating model, stability law, control-loop responsibilities, and architecture closure. | Autonomous Runtime Model | Autonomous runtime operating contracts change. |
| Autonomy | `docs/reference/V7_AUTONOMOUS_OPERATING_SYSTEM.md` | Consolidated autonomous operating-system description and operator-facing autonomy framing. | Autonomous Operating System | Durable autonomy operating model changes. |
| Product | `docs/reference/V7_MASTER_PROJECT_HANDOFF.md` | Human handoff: what the project is, philosophy, current state, and how another developer should continue. | Project Handoff | Major project context changes or handoff needs refreshing. |
| Product | `docs/reference/V7_PROJECT_MAP.md` | Project map and module-level orientation. | Project Map | Major module/layout relationships change. |
| Product | `docs/reference/V7_SYSTEM_ARCHITECTURE.md` | System architecture overview. | Architecture Reference | Architecture-level relationships change. |
| Production | `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md` | Production maturity scoring, certification interpretation, and maturity consumers. | Production Maturity Model | Production maturity rules or certification interpretation changes. |
| Implementation | `docs/reference/V7_IMPLEMENTATION_MODEL.md` | Implementation model and code execution expectations. | Implementation Model | Implementation methodology changes. |
| Implementation | `docs/reference/V7_IMPLEMENTATION_PRIORITY_MODEL.md` | Priority model for implementation sequencing. | Implementation Priority Model | Priority logic changes. |
| Knowledge | `docs/reference/V7_CONTEXT_RESOLVER.md` | Context resolver and engineering-context lookup rules. | Engineering Context Resolver | Context lookup or knowledge-plane rules change. |
| Knowledge | `docs/reference/V7_KNOWLEDGE_QUALITY_MODEL.md` | Knowledge quality and durability model. | Knowledge Quality Model | Durable knowledge quality rules change. |
| Knowledge | `docs/reference/V7_DOCUMENT_LIFECYCLE.md` | Document lifecycle and canonical/document status semantics. | Document Lifecycle | Document state or lifecycle semantics change. |
| Knowledge | `docs/reference/V7_RESEARCH_PROCESS.md` | Research process rules. | Research Process | Research workflow changes. |
| Knowledge | `docs/programs/V7_RESEARCH_FRAMEWORK.md` | Research framework and boundaries. | Research Framework | Research ownership or admissibility rules change. |
| Execution | `docs/reference/V7_EXECUTION_MISSION_PROTOCOL.md` | Execution mission protocol and operational execution structure. | Execution Mission Protocol | Execution mission rules change. |
| Execution | `docs/reference/V7_EXECUTION_COMPLETION_PROTOCOL.md` | Completion protocol: how execution proves closure. | Execution Completion Protocol | Execution completion criteria change. |
| Capability | `docs/reference/capabilities/L3_EMERGENCY_AUTONOMOUS_FAILOVER.md` | L3 emergency autonomous failover capability contract. | L3 Capability Owner | L3 capability behavior or certification changes. |
| Reports | `docs/reports/engineering/` | Engineering reports archive: audits, implementation reports, validation reports, and final evidence. | Engineering Reports | Reports are created for completed engineering tasks. |
| Research | `docs/research/` | Research outputs and discovery evidence that support but do not replace canonical documents. | Research Evidence | Research artifacts are created or superseded. |
| Policies | `docs/policies/` | Policy documents, authority/freshness/safety rules, and policy constraints. | Policy Library | Policy rules change. |
| Decisions | `docs/decisions/` | ADRs and decision records. | ADR Owners | Durable architectural/engineering decisions are accepted or superseded. |

## Operating Notes

- This memo is intentionally short compared with canonical files.
- It should point to owners, not duplicate their full contents.
- If a new file becomes important enough that the operator must remember it, add one row here.
- If a file is superseded, keep the row and say what replaced it.
