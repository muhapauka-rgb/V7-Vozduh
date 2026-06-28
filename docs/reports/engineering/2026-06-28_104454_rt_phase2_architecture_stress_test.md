# RT Phase 2 Discovery Part 2.5: Architecture Stress Test / Simplicity Challenge

Date: 2026-06-28
Program: V7 VOZDUH
Status: RT_PHASE_2_REQUIRES_SIMPLIFICATION

## Summary

RT Phase 2 is still required, but the 12-stage form from Part 2 is unnecessarily complex for OMP canonicalization.

If V7 were designed today from scratch using the current architecture, RT Phase 2 would not be canonicalized as 12 separate stages.
It would be smaller: a compact OMP capability-maturation phase with 6 workstreams.

This is not a rejection of RT Phase 2.
It is a simplification requirement before OMP canonicalization.

No Runtime, OMP, Runtime Model, Decision Model, Canonical Reference, SYSTEM_MAP, Backlog, Product Specification, Production Maturity Model, policy, ADR, authority, automation, or user movement was changed.

## Architecture Pressure Test

Primary question:

```text
If V7 were designed today from scratch, would RT Phase 2 still look like the current 12-stage proposal?
```

Answer:

```text
NO.
```

Reason:

The existing architecture already has:

- Runtime Time Architecture;
- Work Placement Law;
- Decision Lifecycle Foundation;
- Product Scale Objectives;
- Engineering Report Lifecycle;
- OMP capability framework;
- Implementation Backlog;
- Current Program State;
- action-class authority;
- delegated autonomy policy;
- runtime eligibility path;
- governed transaction path.

Therefore RT2 does not need 12 independent capability names.
Most RT2 stages are owner extensions or read-model maturation inside existing planes.

## Simpler Architecture

Recommended simplified RT Phase 2 shape:

| Simplified workstream | Absorbs original RT2 items | Primary classification | Existing owner |
| --- | --- | --- | --- |
| `RT2-S1 Measurement And Observability Foundation` | Runtime Cost Measurement, Runtime Intelligence, Runtime Dashboard | Read Model / Observability Surface | Runtime Model, OMP, admin/read-model owners |
| `RT2-S2 World And Readiness Maturation` | Continuous World Model, Continuous Readiness | Owner Extension / Read Model | World Model Plane, planner/readiness owners |
| `RT2-S3 Desired-State Delta Preparedness` | Desired State Operationalization, Planner Preparedness | Owner Extension / Certification Stage | Product/Policy/Decision Model + existing planner owners |
| `RT2-S4 Governed Execution Coordination` | Governed Orchestration, Execution Coordination / Queue Feasibility | Certification Stage / Owner Extension | governed transaction, packet/lease, restore, runtime owners |
| `RT2-S5 Certified Concurrency Ladder` | Bounded Parallelism | Certification Stage | OMP, action-class ladder, blast-radius, rollback, verification owners |
| `RT2-S6 Evidence-Based Continuous Improvement` | Runtime Evolution Governance, Continuous Operational Improvement | Engineering Rule / OMP Program Discipline | OMP, Backlog, Production Maturity, Engineering Reports |

This preserves every necessary function while removing redundant stage boundaries.

## Capability Classification

| Original RT2 capability | Does it need to exist? | Primary classification | Simplification decision |
| --- | --- | --- | --- |
| World Model Maturation | `YES` | Read Model | Merge into `RT2-S2`. |
| Readiness Maturation | `YES` | Read Model / Owner Extension | Merge into `RT2-S2`. |
| Desired State Operationalization | `YES` | Owner Extension | Merge into `RT2-S3`. |
| Planner Preparedness Maturation | `YES` | Owner Extension | Merge into `RT2-S3`. |
| Governed Orchestration Maturation | `YES` | Certification Stage | Merge into `RT2-S4`. |
| Execution Coordination / Queue Feasibility Gate | `YES_AS_GATE`, not standalone build | Certification Stage | Merge into `RT2-S4`; queue remains killable. |
| Certified Concurrency Ladder | `YES` | Certification Stage | Keep as `RT2-S5`. |
| Runtime Cost Measurement Maturation | `YES` | Read Model / Measurement | Merge into `RT2-S1`. |
| Runtime Intelligence Maturation | `YES` | Read Model / Measurement | Merge into `RT2-S1`. |
| Runtime Observability Surface Maturation | `YES` | Observability Surface | Merge into `RT2-S1`. |
| Evidence-Based Runtime Evolution Governance | `YES` | Engineering Rule | Merge into `RT2-S6`. |
| Continuous Operational Improvement Framework | `YES` | OMP Program Discipline | Merge into `RT2-S6`. |

## Redundancy Test

| Capability removed | What breaks? | Existing owner with similar work | Can owner absorb it? | Independent? |
| --- | --- | --- | --- | --- |
| World Model | Runtime lacks compact current state for future automation. | World Model Plane, intelligence snapshots, CPS | `YES` | `NO`, paired with readiness. |
| Readiness | Runtime cannot cheaply know candidate/target safety. | Planner/readiness/service owners | `YES` | `NO`, consumes world model. |
| Desired State | Delta planning lacks product/policy target. | Product Spec, Business Objectives, Decision Model | `YES` | `NO`, paired with planner. |
| Planner Preparedness | Desired state cannot become actionable deltas. | Planner/autoswitch | `YES` | `NO`, paired with desired state. |
| Governed Orchestration | Future bounded execution lacks lifecycle discipline. | Governed transaction, packet/lease/restore owners | `YES` | `PARTIAL`, but queue depends on it. |
| Execution Queue | Nothing breaks now; future batching/concurrency may lack coordination. | Governed transaction/runtime owners | `YES_AFTER_ENTRY` | `NO`, should stay feasibility gate. |
| Parallelism | Future larger blast-radius execution remains serial. | OMP/action-class/blast owners | `YES` | `YES`, but only as certification ladder. |
| Runtime Cost | Phase 2 cannot prove Product Scale impact. | Runtime Model + OMP | `YES` | `NO`, pairs with latency/observability. |
| Runtime Intelligence | Latency/cost signals remain invisible. | Runtime Model + read models | `YES` | `NO`, pairs with measurement. |
| Dashboard | Operators lack surface for runtime performance. | Admin/read-model owners | `YES` | `NO`, consumer only. |
| Runtime Evolution Governance | Improvements may become ad hoc. | OMP + Backlog | `YES` | `NO`, pairs with continuous improvement. |
| Continuous Improvement | RT2 lacks long-term loop. | Product Spec + OMP | `YES` | `NO`, existing OMP discipline. |

## Merge Opportunities

| Merge | Decision | Reason |
| --- | --- | --- |
| World Model + Readiness | `MERGE` | Readiness is a consumer of current world state; separate stages create artificial boundaries. |
| Runtime Cost + Runtime Intelligence + Dashboard | `MERGE` | All are measurement/observability surfaces; none should be a decision owner. |
| Runtime Evolution + Continuous Improvement | `MERGE` | Both are OMP-governed improvement recommendation loops. |
| Desired State + Planner Preparedness | `MERGE` | Desired state becomes useful only through prepared deltas in the existing planner owner. |
| Governed Orchestration + Queue Feasibility | `MERGE_WITH_QUEUE_DEFERRED` | Queue is not a runtime owner; it is possible future coordination after orchestration maturity. |
| Queue + Parallelism | `DO_NOT_FULLY_MERGE` | Queue is coordination; parallelism is authority/blast/rollback certification. |

## Removal Opportunities

No capability should disappear completely today.

However, these should not be standalone canonical RT2 stages:

- Execution Queue;
- Runtime Dashboard;
- Runtime Cost Intelligence;
- Runtime Evolution Engine;
- Continuous Runtime Evolution Framework;
- Continuous Readiness;
- Continuous Planning.

They should be merged into the 6 simplified workstreams.

## Kill Criteria

| Capability | Kill criteria |
| --- | --- |
| Execution Queue | Never implement if serial bounded execution plus operator-visible transaction state is enough; if queue adds latency, hidden authority, retry storms, or duplicate runtime ownership. |
| Bounded Parallelism | Never implement if production evidence shows parallel actions increase rollback, verification, capacity, or anti-flap risk more than they reduce recovery latency. |
| Runtime Dashboard | Never implement as standalone if existing admin/read-model surfaces can expose required latency/cost/status summaries without a new surface. |
| Runtime Cost Measurement | Never implement live-path measurement that adds meaningful runtime latency, blocking IO, or heavy telemetry cost. |
| Desired State Operationalization | Never implement if it becomes self-authorizing, duplicates planner/authority, or creates desired-state drift without live gate revalidation. |
| World Model Maturation | Never implement a global mutable world object if existing indexed read models remain more scale-safe. |
| Planner Preparedness | Never implement if it becomes a planner rewrite or bypasses A6/B13 certification. |
| Governed Orchestration | Never implement if it weakens fail-closed, rollback, verification, restore barrier, or terminal outcome learning. |
| Runtime Intelligence | Never implement if it turns metrics into unsafe certification gates or authority signals. |
| Continuous Improvement | Never implement if it mutates Runtime automatically or bypasses OMP/backlog/authority. |

## Complexity Analysis

Scale:

- `LOW`: small extension or owner-local maturity.
- `MEDIUM`: cross-owner coordination.
- `HIGH`: risk of new hidden architecture.

| Simplified workstream | Runtime complexity | Architecture complexity | Operator complexity | Testing complexity | Certification complexity | Maintenance complexity | Benefit exceeds cost? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Measurement And Observability Foundation | `LOW` if read-model based | `LOW` | `LOW` | `MEDIUM` | `MEDIUM` | `MEDIUM` | `YES` |
| World And Readiness Maturation | `LOW` | `MEDIUM` | `LOW` | `MEDIUM` | `HIGH` | `MEDIUM` | `YES` |
| Desired-State Delta Preparedness | `LOW` | `MEDIUM` | `MEDIUM` | `HIGH` | `HIGH` | `MEDIUM` | `YES_WITH_BOUNDARIES` |
| Governed Execution Coordination | `MEDIUM` | `MEDIUM` | `LOW` | `HIGH` | `HIGH` | `MEDIUM` | `YES_WITH_QUEUE_DEFERRED` |
| Certified Concurrency Ladder | `MEDIUM` | `MEDIUM` | `MEDIUM` | `HIGH` | `HIGH` | `HIGH` | `YES_ONLY_AFTER_EVIDENCE` |
| Evidence-Based Continuous Improvement | `NO_RUNTIME_CHANGE` | `LOW` | `LOW` | `LOW` | `MEDIUM` | `LOW` | `YES` |

The 12-stage model increases documentation and certification complexity without increasing safety.
The 6-workstream model preserves safety and reduces program overhead.

## Industry Comparison

Mature production systems solve these problems with roughly equal or less explicit architecture than the 12-stage RT2 form:

- Google SRE emphasizes scoped automation, reliability, toil reduction, and learning loops rather than many named runtime subprograms.
- AWS Operational Excellence uses prepare/operate/evolve and continuous improvement loops; it does not require every measurement surface to become a separate architecture stage.
- Kubernetes separates desired/current state and reconciliation, but the core concept is compact: desired state, observed state, controller loop, status.
- Netflix/Kayenta emphasizes evidence-based promotion and canary analysis; it does not make dashboard/cost/evolution separate authority owners.
- Cisco/Juniper/Cloudflare-style control planes separate intent, observed state, validation, orchestration, and assurance, but avoid giving observability or queues independent decision authority.

Conclusion:

RT2 should use equal-or-less architecture than mature systems:

```text
measure -> prepare state -> decide delta -> coordinate execution -> certify concurrency -> improve
```

## Program Validation

RT Phase 2 should exist as one OMP program after Phase 2 entry, but not as 12 independent subprograms.

Correct form:

```text
One OMP Phase 2 program
  -> 6 capability-maturation workstreams
  -> all mapped to existing backlog/owners
  -> no new queue/runtime/planner/authority owner
```

It should not exist as:

- several OMP programs;
- a new runtime architecture;
- a new roadmap outside backlog;
- a queue-first automation project;
- a dashboard-first observability project.

## Alternative Architecture

Smaller RT2:

```text
RT2-S1 Measurement And Observability Foundation
  -> RT2-S2 World And Readiness Maturation
  -> RT2-S3 Desired-State Delta Preparedness
  -> RT2-S4 Governed Execution Coordination
  -> RT2-S5 Certified Concurrency Ladder
  -> RT2-S6 Evidence-Based Continuous Improvement
```

Mandatory entry prerequisites remain unchanged:

- A5 complete;
- A6 complete;
- B13 complete;
- B16 complete;
- bounded automation certified;
- runtime eligibility certified;
- rollback/verification certified;
- blast radius certified;
- metric reliability certified;
- RT Phase 1 complete;
- Work Placement complete;
- Decision Lifecycle complete;
- Pre-Phase-2 Readiness complete;
- Reaction Latency measurable;
- Runtime Cost measurable;
- explicit authority.

## Readiness For OMP Canonicalization

Verdict:

```text
NO, not in the 12-stage form.
YES, after simplification to the 6-workstream form.
```

Remaining issues before canonicalization:

1. Replace the 12-stage RT2 list with the smaller 6-workstream shape.
2. Preserve original capabilities as absorbed responsibilities, not standalone stages.
3. Mark Execution Queue as a killable feasibility gate, not mandatory implementation.
4. Mark Dashboard as observability consumer, not a capability owner.
5. Keep parallelism as certification ladder only.
6. Keep continuous improvement as OMP-governed recommendations only.

## Recommendation

Do not canonicalize RT2 Part 2 as-is.

Proceed to Part 3 OMP Canonicalization only if Part 3 uses the simplified 6-workstream structure and preserves all current safety/authority/owner boundaries.

Current OMP execution should still continue with `A5`.

## Validation

| Check | Result |
| --- | --- |
| Runtime changed | `NO` |
| OMP changed | `NO` |
| Runtime Model changed | `NO` |
| Decision Model changed | `NO` |
| Canonical Reference changed | `NO` |
| SYSTEM_MAP changed | `NO` |
| Backlog changed | `NO` |
| Runtime automation enabled | `NO` |
| Authority expanded | `NO` |
| Users moved | `NO` |
| New owner | `NO` |
| New backlog | `NO` |
| New architecture | `NO` |

## Final Answers

1. Is RT Phase 2 still required? `YES`.
2. Can RT2 be smaller? `YES`.
3. Stages to remove: none as functions; remove standalone stage status for Queue, Dashboard, Runtime Cost Intelligence, Runtime Evolution Engine, Continuous Runtime Evolution Framework, Continuous Readiness, and Continuous Planning.
4. Stages to merge: World+Readiness; Cost+Intelligence+Dashboard; Evolution+Continuous Improvement; Desired State+Planner Preparedness; Orchestration+Queue Feasibility.
5. Stages to keep unchanged: Certified Concurrency Ladder as a distinct certification ladder; Governed Execution Coordination as a workstream, but queue remains deferred.
6. Kill criteria: documented above.
7. Simpler architecture exists? `YES`: 6-workstream RT2.
8. Complexity acceptable? `YES_AFTER_SIMPLIFICATION`; `NO` for 12 independent stages.
9. Ready for OMP Canonicalization? `NO_AS_12_STAGE_MODEL`; `YES_AFTER_SIMPLIFICATION`.
10. Engineering report path: `docs/reports/engineering/2026-06-28_104454_rt_phase2_architecture_stress_test.md`.

FINAL VERDICT: RT_PHASE_2_REQUIRES_SIMPLIFICATION
