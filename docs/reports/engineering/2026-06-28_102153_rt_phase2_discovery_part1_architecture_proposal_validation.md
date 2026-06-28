# RT Phase 2 Discovery Part 1: Architecture Proposal Validation

Date: 2026-06-28
Program: V7 VOZDUH
Status: RT_PHASE_2_DISCOVERY_PART1_COMPLETE

## Summary

RT Phase 2 is architecturally valid as a proposal.
It matches V7's existing architecture if it remains constrained by the current owners:
Product Specification, Runtime Model, Decision Model, OMP, Canonical Reference, SYSTEM_MAP, policies, ADRs, Backlog, and Current Program State.

RT Phase 2 is not ready for implementation.
It must remain non-canonical until later discovery stages validate exact owner mapping, implementation order, safety gates, measurements, and authority boundaries.

No OMP, Runtime Model, Decision Model, Canonical Reference, SYSTEM_MAP, Backlog, runtime behavior, authority, automation, or user movement was changed.

## Internal Discovery

| Proposed RT Phase 2 capability | Status | Existing owner / location | Finding |
| --- | --- | --- | --- |
| Continuous World Model | EXISTS_PARTIAL | Runtime Model, SYSTEM_MAP, Knowledge Plane, intelligence snapshots, Current Program State | Plane ownership and read models exist; continuous automation-grade hot state is not complete. |
| Continuous Observation | EXISTS_PARTIAL | service matrix, quality compact, sentinel, route/runtime truth owners | Observation tools exist; continuous automation consumption is not enabled. |
| Continuous Readiness | EXISTS_PARTIAL | planner/autoswitch, operator decision surface, runtime readiness owners | Readiness exists as read-only/gated surfaces; automation-grade readiness is future work. |
| Desired State | EXISTS | Product Specification, Business Objectives, Decision Model, Runtime Model | Desired State is canonical; it does not authorize execution by itself. |
| Delta Planning | EXISTS_PARTIAL | planner/autoswitch, Decision Model, Runtime Model | Candidate/delta-like planning exists; desired-state delta for Phase 2 is not implemented. |
| Execution Orchestration | EXISTS_PARTIAL | governed transaction, packet/lease, restore barrier, autoswitch apply owners | Governed orchestration exists; continuous/bounded autonomous orchestration is not enabled. |
| Execution Queue | MISSING | Future Phase 2 item in Runtime Model | Explicitly forbidden before Phase 2 entry; no current queue should exist. |
| Runtime Cost | EXISTS | Runtime Model, OMP Product Evolution Review | Cost dimensions are defined; measurement maturity remains future work. |
| Latency Intelligence | EXISTS_PARTIAL | Reaction Latency Model, Runtime Latency Engineering Review | Model/checklist exist; measured latency dashboard/certification are not complete. |
| Runtime Evolution | EXISTS_PARTIAL | OMP, Runtime Model, Backlog | Evolution discipline exists; runtime adaptation is not active. |
| Continuous Improvement | EXISTS | Product Specification, OMP, Canonical Reference | Continuous improvement is a core product/OMP principle. |
| Adaptive Runtime | EXISTS_PARTIAL | Delegated Autonomy Policy, Action-Class Authority, Runtime Model | Architecture supports bounded evolution; runtime automation is disabled. |
| Runtime Dashboard | EXISTS_PARTIAL | admin/read-model owners, future Phase 2 item | Operator/admin read models exist; runtime performance dashboard is not complete. |
| Reaction Latency Certification | EXISTS_PARTIAL | Runtime Model, OMP, Production Maturity Model | Concept exists; certification requires measurements and later authority. |

Counts:

- EXISTS: 3
- EXISTS_PARTIAL: 10
- EXISTS_FRAGMENTED: 0
- MISSING: 1

## External Validation

Mature production systems prepare automation with the same engineering pattern:

- Google SRE: automation is valuable when it is scoped, safe, and reduces operational toil without bypassing reliability discipline. Source: https://sre.google/sre-book/automation-at-google/
- Google Borg: large-scale control planes maintain desired state, observed state, scheduling/control loops, and operational constraints before autonomous changes. Source: https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/
- AWS Operational Excellence: production systems prepare, operate, evolve, learn, and improve through explicit operational mechanisms. Source: https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html
- Kubernetes: controllers reconcile desired state against current state using continuous observation and bounded control loops. Source: https://kubernetes.io/docs/concepts/architecture/controller/
- Netflix / Kayenta: promotion is evidence-driven through automated canary analysis before broader rollout. Sources: https://netflixtechblog.com/automated-canary-analysis-at-netflix-with-kayenta-3260bc7acc69 and https://spinnaker.io/docs/guides/user/canary/
- Cisco / Juniper / Cloudflare production control planes generally separate intent/policy, observed state, validation, orchestration, rollback/failover, and operator-visible control surfaces before autonomous changes.

## External System Matrix

| System | Core philosophy | Architecture | Strengths | Weaknesses | Applicability to V7 | Must copy | Must adapt | Must NOT copy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Google SRE | Automate toil only with safety and reliability discipline. | Humans define goals; automation executes bounded operations. | Strong reliability culture and post-incident learning. | Can be heavy if copied mechanically. | Strong fit. | Safety-first automation and learning loops. | Map SRE concepts to V7 OMP/capabilities. | Human-free automation before certification. |
| Google Borg | Desired/current state and continuous scheduling under constraints. | Cluster control plane with observed state and scheduling. | Proven at huge scale. | Too broad for V7 if copied directly. | Conceptual fit. | Desired/current state separation. | Scale down to routing/action classes. | Full scheduler rewrite. |
| AWS | Prepare, operate, evolve. | Well-Architected operational lifecycle. | Mature operational review model. | Generic, not routing-specific. | Strong fit for OMP gates. | Operational excellence loop. | Convert to V7 Product Evolution Review. | Generic checklist without owners. |
| Cloudflare | Global traffic control with health, steering, and failover. | Observation, policy, traffic steering, health checks. | Strong production failover pattern. | Public docs do not map 1:1 to V7 internals. | Useful for failover/health/steering. | Health-based steering discipline. | Apply through V7 policies and gates. | Direct traffic model assumptions. |
| Cisco | Intent/policy orchestration and safe network automation. | Service/intent model with validation/orchestration. | Strong network automation lineage. | Vendor platform assumptions. | Useful for authority/intent separation. | Intent before operation. | Map to Business Objectives -> policies. | Device/vendor-specific architecture. |
| Juniper | Intent-based networking with validation and closed-loop ideas. | Desired network state and assurance. | Strong desired-state model. | Vendor-specific. | Useful for Desired Safe State. | Assurance before automation. | Keep V7 owners. | Apstra-specific object model. |
| Kubernetes | Declarative desired state, controllers, reconciliation. | API objects, controllers, observed state. | Very clear control-loop model. | Cluster semantics can overfit. | Strong conceptual fit. | Reconcile current/desired state. | Use without creating a new V7 scheduler. | Blind controller loop that bypasses authority. |
| Netflix | Progressive delivery and evidence-based promotion. | Canary analysis and automated rollout judgement. | Strong promotion safety. | Service rollout differs from user routing. | Strong fit for certification/promotion. | Evidence before promotion. | Map metrics to V7 outcomes/trust. | Treating canary success as authority expansion. |
| Spinnaker / Kayenta | Automated canary analysis before promotion. | Metrics compare baseline/canary; promotion gates. | Clear bounded promotion model. | Depends on mature metrics. | Fit for B13/reaction latency certification. | Metric reliability before promotion. | V7-specific metrics and rollback semantics. | Metric-only certification without production outcomes. |

## Architecture Questions

| Question | Answer |
| --- | --- |
| Is RT Phase 2 conceptually correct? | YES. |
| Does it violate current Runtime philosophy? | NO, if Runtime remains thin and fail-closed. |
| Does it violate Thin Runtime? | NO, if heavy work remains in Observation, World Model, Planning, read models, or OMP. |
| Does it violate Work Placement? | NO, if every computation has one canonical plane and owner. |
| Does it violate Decision Lifecycle? | NO, if prepared objects remain governed by freshness/material invalidation. |
| Does it violate Certification Truth? | NO, if implementation metrics do not become mandatory gates without canonical owner approval. |
| Does it violate OMP philosophy? | NO, if it enters only through existing backlog and authority rules. |
| Does it introduce hidden new architecture? | NO at proposal level; future implementation must guard against queues/schedulers becoming hidden owners. |
| Does it require new owners? | NO. |
| Does it require new backlog? | NO. Existing owners map A5, A6, B13, B16, B18/C6, B19/B20, B8-B10, and later Phase 2 items. |
| Does it duplicate existing capabilities? | Not if treated as proposal and mapped to existing owners. |

## Gap Analysis

Real gaps before RT Phase 2 can become implementation:

1. A5 must certify class-level blast-radius evidence beyond one-user guard.
2. A6 must produce runtime eligibility arbitration.
3. B13 must certify metric reliability for promotion/runtime recommendation.
4. B16 must certify rollback/verification authority where required.
5. Reaction Latency must become measurable.
6. Runtime Cost must become measurable.
7. Desired Safe State must become explicit without becoming self-authorizing.
8. Execution Queue must remain absent until explicit Phase 2 entry.
9. Runtime Dashboard and Reaction Latency Certification are future Phase 2/late readiness surfaces, not current blockers for A5.

## Potential Duplicate Owners

No duplicate owner is required.

Potential future risks:

- Execution Queue becoming a second runtime owner.
- Desired Safe State becoming a second planner or authority owner.
- Latency budgets becoming unsafe SLO gates.
- Runtime Dashboard becoming a decision source instead of a read model.
- Continuous World Model replacing existing observation/planning owners.

All are preventable through Work Placement, Certification Truth, OMP, and Architecture Closed by Default.

## Recommendation

RT Phase 2 is architecturally valid as a proposal.
It should proceed to Part 2 discovery.

Do not implement.
Do not canonicalize Phase 2 implementation details yet.
Do not create a new owner, backlog item, runtime path, queue, scheduler, or authority model.

## Next Discovery Step

Part 2 should validate exact owner mapping and implementation boundaries for each RT Phase 2 capability before any OMP integration or implementation.

## Validation

Runtime changed: NO.
Automation enabled: NO.
Authority expanded: NO.
Users moved: NO.
New owner: NO.
New backlog: NO.
New architecture: NO.

FINAL VERDICT: RT_PHASE_2_DISCOVERY_PART1_COMPLETE
