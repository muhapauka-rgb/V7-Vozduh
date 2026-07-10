# V7 Behaviour Reality Validation

Status: `INDEPENDENT_REALITY_VALIDATION`
Input: `docs/reports/research/V7_BEHAVIOUR_DECOMPOSITION_REVIEW.md`
Reality Baseline: `docs/reports/research/V7_CURRENT_AUTONOMOUS_BEHAVIOUR_REALITY.md`
Date: `2026-07-08`

## 1. Scope

This report validates whether the Behaviours proposed in the Behaviour Decomposition Review actually exist in today's V7 engineering reality.

It does not:

- start Phase 3;
- perform Phase 2 Closure;
- create a Gap;
- modify Current Autonomous Behaviour Reality;
- modify AEP;
- modify AOS;
- modify Runtime;
- modify `LOCKED_ARCHITECTURE`;
- modify `LOCKED_KNOWLEDGE`.

No new source discovery was performed. The validation uses already collected Reality, Function Graph evidence, implementation evidence, Runtime evidence, tests, reports, and existing program/source evidence.

## 2. Foundational Law Applied

Behaviour Reality is evidence-driven and implementation-driven.

Architecture may explain Reality, but Reality never adapts itself to architecture.

No proposed Behaviour is accepted because it is logical, expected, common, architecturally implied, or useful. A Behaviour is accepted only when observable engineering evidence exists.

## 3. Validation Status Model

| Status | Meaning | May Enter Future Reality Refinement |
| --- | --- | --- |
| `OBSERVED_INDEPENDENT` | Real evidence exists and the item has its own situation, decision, execution/producer path, verification, and continuation/learning meaning. | `YES` |
| `OBSERVED_INTERNAL_STEP` | Real evidence exists, but the item is an internal step inside another Behaviour, not an independent Behaviour. | `NO` |
| `OBSERVED_COMPOSITE_NOT_ADMISSIBLE` | Real evidence exists, but the proposed item still combines multiple independent behaviours. | `NO_AS_WRITTEN` |
| `HYPOTHESIZED` | Evidence is insufficient for current independent Behaviour Reality. | `NO` |

## 4. Validation Summary

| Metric | Count |
| --- | ---: |
| Proposed Behaviours validated | `79` |
| Behaviours with observable evidence | `73` |
| `OBSERVED_INDEPENDENT` | `69` |
| `OBSERVED_INTERNAL_STEP` | `3` |
| `OBSERVED_COMPOSITE_NOT_ADMISSIBLE` | `1` |
| `HYPOTHESIZED` | `6` |
| Rejected from future Reality refinement as standalone Behaviours | `10` |

## 5. Observed Behaviour Catalogue

The following proposed Behaviours are observed and independent enough to participate in a future operator-approved Reality refinement.

| ID | Observed Behaviour | Evidence Type | Primary Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `OB-001` | Program Command Interpretation | Engineering/report evidence | AEP execution flow, operator command reports | `HIGH` |
| `OB-002` | Foundation / Source Consumption | Program/report evidence | AEP foundation rules, source disposition reports | `HIGH` |
| `OB-003` | Engineering Report Production | Engineering evidence | Stage 2 and AEP engineering reports | `HIGH` |
| `OB-004` | Review / Certification Recording | Engineering evidence | Review/certification sections in accepted reports | `HIGH` |
| `OB-005` | Source Enumeration | Repository evidence | `rg`, `find`, source inventory reports | `HIGH` |
| `OB-006` | Source Disposition | Engineering evidence | Source disposition matrices | `HIGH` |
| `OB-007` | Discovery Index Resolution | Function Graph evidence | Function Graph Appendix as discovery/evidence index | `HIGH` |
| `OB-008` | Behaviour Instance Capture | Engineering evidence | Current Behaviour Reality instance registry | `HIGH` |
| `OB-009` | Reality Aggregation | Engineering evidence | Behaviour Definition, Coverage, Graph sections | `HIGH` |
| `OB-010` | CPS State Recording | State evidence | `docs/programs/V7_CURRENT_PROGRAM_STATE.md` | `HIGH` |
| `OB-011` | OMP Continuation State Update | Program/state evidence | OMP, CPS, SYSTEM_MAP continuation rules | `MEDIUM_HIGH` |
| `OB-012` | Production Maturity Handoff | Program/state evidence | Production Maturity, SYSTEM_MAP, CPS | `MEDIUM_HIGH` |
| `OB-013` | Candidate Evaluation | Implementation/test evidence | `RoutingBrain`, decision surface tests | `HIGH` |
| `OB-014` | Policy Filtering | Implementation/policy evidence | `build_knowledge_decision_overlay`, policy models | `HIGH` |
| `OB-015` | Capacity / Service Validation | Implementation/test evidence | service fit, best-pool and service matrix models | `HIGH` |
| `OB-016` | Trust / Prediction Scoring | Implementation/test evidence | trust and prediction snapshots | `HIGH` |
| `OB-017` | Best Pool Recommendation | Implementation/test evidence | `RoutingBrain.best_available_pool_advice` | `HIGH` |
| `OB-018` | Decision Overlay / Proposal | Implementation/test evidence | operator decision surface and batch preview | `HIGH` |
| `OB-019` | Service Matrix Observation | Runtime/support evidence | service matrix refresh and evidence snapshots | `HIGH` |
| `OB-020` | Channel Trust Observation | Implementation/test evidence | trust recovery tests and snapshots | `HIGH` |
| `OB-021` | Degradation Signal Classification | Implementation/policy evidence | degradation signal policy mapping | `HIGH` |
| `OB-022` | Scoped Incident Observation | Engineering/runtime evidence | scoped/emergency verification evidence; live state unavailable | `MEDIUM` |
| `OB-023` | Authority Requirement Resolution | Program/test evidence | OMP, action-class authority tests | `HIGH` |
| `OB-024` | Action-Class Classification | Implementation/test evidence | action-class runtime enablement model | `HIGH` |
| `OB-025` | Blast-Radius Boundary Evaluation | Implementation/evidence evidence | blast radius evidence rows and policy model | `HIGH` |
| `OB-026` | Approval Decision | Program/runtime evidence | packet/authority approval paths | `MEDIUM_HIGH` |
| `OB-027` | Runtime Eligibility Governance | Implementation/test evidence | delegated autonomy runtime eligibility | `HIGH` |
| `OB-028` | Movement Candidate Admission | Implementation/test evidence | governed canary and autoswitch policy tests | `HIGH` |
| `OB-029` | Lease / Version Readiness | Implementation/test evidence | `build_execution_lease`, version/fingerprint checks | `HIGH` |
| `OB-030` | Restore Barrier Readiness | Implementation/test evidence | restore barrier clearance and tests | `HIGH` |
| `OB-031` | Governed Dry-Run / Apply Selection | Implementation/report evidence | governed canary dry-run cycle | `HIGH` |
| `OB-032` | Runtime Convergence Verification | Tool/report evidence | truth/convergence reports, `v7_sync_lib` | `HIGH` |
| `OB-033` | Action Terminal Classification | Implementation/test evidence | terminal classification policy/tests | `HIGH` |
| `OB-034` | Runtime Read Diagnostic Verification | Implementation/test evidence | runtime read views and diagnostic tests | `HIGH` |
| `OB-035` | Incident Scoped Verification | Engineering evidence | scoped verification reports and policies | `MEDIUM` |
| `OB-036` | Production / Certification Truth Closure | Report/state evidence | certification reports and Production Maturity consumption | `MEDIUM_HIGH` |
| `OB-037` | Rollback Readiness Check | Implementation/report evidence | rollback policy and readiness reports | `HIGH` |
| `OB-038` | Rollback Authority Certification | Implementation/test evidence | `build_rollback_authority_certification` | `HIGH` |
| `OB-039` | Restore Barrier Clearance | Implementation/test evidence | `build_restore_barrier_clearance` | `HIGH` |
| `OB-040` | Post-Rollback Verification / Learning | Implementation/test evidence | rollback-related feedback and trust tests | `MEDIUM_HIGH` |
| `OB-041` | Outcome Quality Evaluation | Implementation/test evidence | `outcome_quality_evaluation` | `HIGH` |
| `OB-042` | Decision Learning Record | Implementation/test evidence | `decision_learning_record` | `HIGH` |
| `OB-043` | Trust Evolution Update | Implementation/test evidence | `build_trust_evolution_snapshot` | `HIGH` |
| `OB-044` | Prediction Feedback | Implementation/test evidence | prediction actual/feedback rows | `HIGH` |
| `OB-045` | Recommendation Confidence Adjustment | Engineering/intelligence evidence | confidence/recommendation models | `MEDIUM_HIGH` |
| `OB-046` | Evidence Quality Feedback | Engineering/intelligence evidence | Engineering Intelligence and evidence-quality reports | `MEDIUM` |
| `OB-047` | Production Evidence Consumption | Report/evidence evidence | production evidence directories and reports | `HIGH` |
| `OB-048` | Production Certification Review | Report/state evidence | certification reports | `HIGH` |
| `OB-049` | Maturity Decision | Program/state evidence | Production Maturity Model and CPS | `HIGH` |
| `OB-050` | No-Change / Block Explanation | Program/report evidence | State Transition Law and engineering reports | `HIGH` |
| `OB-051` | CPS Maturity State Recording | State evidence | CPS maturity/current state fields | `HIGH` |
| `OB-052` | Operator Overview Projection | Implementation/test evidence | overview views and admin tests | `HIGH` |
| `OB-053` | Runtime Diagnostic View | Implementation/test evidence | runtime read and diagnostic views | `HIGH` |
| `OB-054` | Decision Preview | Implementation/test evidence | operator decision surface | `HIGH` |
| `OB-055` | Audit / Evidence Search | Implementation evidence | operator observability audit search | `HIGH` |
| `OB-056` | Governance / Execution Preview | Implementation evidence | operator governance/execution preview functions | `HIGH` |
| `OB-057` | Export Preview | Implementation evidence | operator audit export preview | `HIGH` |
| `OB-058` | Knowledge Change Detection | Stage 2/report evidence | Stage 2 knowledge inventory/extraction/lock reports | `MEDIUM_HIGH` |
| `OB-059` | Knowledge Owner Evaluation | Stage 2/report evidence | Stage 2 acceptance and canonical knowledge reports | `MEDIUM_HIGH` |
| `OB-060` | Canonical Sync | Stage 2/report evidence | Stage 2 knowledge lock report | `HIGH` |
| `OB-061` | Foundation Synchronization | AEP/report evidence | AEP foundation lifecycle and Phase 1 execution | `MEDIUM_HIGH` |
| `OB-062` | No-Change Recording | Program/report evidence | State Transition Law and reports | `HIGH` |
| `OB-063` | Diagnosis And Owner Resolution | Implementation/test evidence | Domain 11 record/projection source and tests | `HIGH` |
| `OB-064` | Deployment Manifest Production | Implementation/tool evidence | `build_deploy_manifest` | `HIGH` |
| `OB-065` | Safe Deploy Execution | Deployment evidence | safe deploy reports/evidence | `MEDIUM_HIGH` |
| `OB-066` | Runtime Linkage Recording | Implementation/tool evidence | `build_runtime_linkage` | `HIGH` |
| `OB-067` | Post-Deploy Convergence Check | Tool/report evidence | truth/convergence after deploy evidence | `HIGH` |
| `OB-068` | Deploy Rollback / Hold Decision | Deployment/report evidence | deploy safety reports; hold/rollback policy evidence | `MEDIUM_HIGH` |
| `OB-069` | Production Maturity Handoff | Report/state evidence | production certification/maturity handoff evidence | `MEDIUM_HIGH` |

## 6. Rejected Behaviour Catalogue

These proposed Behaviours must not enter Current Autonomous Behaviour Reality as standalone Behaviours in their current form.

| ID | Proposed Behaviour | Status | Reason |
| --- | --- | --- | --- |
| `RB-001` | Owner Consumption / Continuation | `HYPOTHESIZED` | Owner consumption is required by law, but confirmed concrete consumption is not proven for this proposed child as a general independent Behaviour. |
| `RB-002` | OMP Candidate Consumption | `HYPOTHESIZED` | AEP Phase 2 created no certified candidate for OMP consumption. |
| `RB-003` | OMP Mission Routing | `HYPOTHESIZED` | OMP mission routing exists as a program route, but not as a current Phase 2 output execution. |
| `RB-004` | Candidate Observation | `OBSERVED_INTERNAL_STEP` | Candidate inputs exist, but observation alone lacks independent decision, verification, and learning path. |
| `RB-005` | Freshness / Anti-Flap Evaluation | `OBSERVED_COMPOSITE_NOT_ADMISSIBLE` | Evidence exists for freshness and anti-flap, but the combined item has multiple policy decisions and should not enter Reality as one atomic Behaviour. |
| `RB-006` | Guarded Runtime Execution | `HYPOTHESIZED` | Guarded dry-run/apply selection is observed, but actual independent Runtime execution/mutation is not observed or admitted in Phase 2 reality. |
| `RB-007` | Verification Handoff | `OBSERVED_INTERNAL_STEP` | Evidence exists as a handoff from execution to verification, but it is not independent execution/learning behaviour. |
| `RB-008` | Rollback Handoff | `OBSERVED_INTERNAL_STEP` | Evidence exists as a handoff from guarded execution to rollback readiness, but not as standalone Behaviour. |
| `RB-009` | Rollback Execution Path | `HYPOTHESIZED` | Readiness/authority/restore paths are observed; independent rollback execution is not proven as current admitted reality. |
| `RB-010` | OMP / Owner Handoff | `HYPOTHESIZED` | Handoff is required by governance, but concrete current consumption is not sufficiently proven as an independent Behaviour. |

## 7. Evidence Matrix

| Evidence Type | Behaviours Supported | Notes |
| --- | --- | --- |
| Source code | Routing, decision surface, runtime read views, execution pipeline, feedback, intelligence, sync/deploy tooling, diagnosis records. | Strongest proof for implementation existence. |
| Tests | Routing boundary, no-authority, decision overlay, trust, prediction, runtime diagnostics, rollback, operator execution. | Strong proof of expected behaviour and forbidden actions. |
| Function Graph | Producers, consumers, mutation flags, read-only/advisory paths, Domain 11 addendum. | Evidence index only, not truth source. |
| Engineering reports | Program/report lifecycle, certification, Stage 2 knowledge, deploy, production evidence. | Real engineering evidence; may be historical if superseded. |
| Runtime/deployment evidence snapshots | Deploy, runtime fingerprint/linkage, production evidence, truth/convergence. | Supports observed deployment/convergence behaviour, but not live current state. |
| Program/state docs | OMP, CPS, Production Maturity, AEP, Canonical Reference, SYSTEM_MAP. | Defines owners/laws and some state evidence; not sufficient alone for behaviour acceptance. |

## 8. Behaviour Validation Matrix

| Parent | Proposed Behaviour | Status | Producer | Consumer | Implementation / Runtime Path | Decision / Verification / Learning Path | Confidence | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `BD-001` | Program Command Interpretation | `OBSERVED_INDEPENDENT` | Operator/Codex | Program report workflow | AEP/report execution pattern | Command -> execute/hold -> report | `HIGH` | Real operator-command engineering workflow exists. |
| `BD-001` | Foundation / Source Consumption | `OBSERVED_INDEPENDENT` | AEP/Foundation process | Phase execution | AEP source/foundation sections | consume/disposition -> foundation verdict | `HIGH` | Foundation source consumption is explicitly performed and reported. |
| `BD-001` | Engineering Report Production | `OBSERVED_INDEPENDENT` | Codex/report owner | Operator/OMP/future phase | Engineering reports | produce report -> review -> possible consumption | `HIGH` | Repeated engineering reports exist. |
| `BD-001` | Review / Certification Recording | `OBSERVED_INDEPENDENT` | Review/certification process | Operator/future phase | report review sections | PASS/HOLD/reject recording | `HIGH` | Reviews are explicit report artifacts. |
| `BD-001` | Owner Consumption / Continuation | `HYPOTHESIZED` | varies | owner/OMP | not uniformly proven | consumption confirmation not deterministic | `MEDIUM_LOW` | Required by law, but not sufficiently observed as independent current Behaviour. |
| `BD-002` | Source Enumeration | `OBSERVED_INDEPENDENT` | Codex/repository scan | Reality report | `rg`, `find` evidence | enumerate -> count -> inventory | `HIGH` | Directly observed during Phase 2. |
| `BD-002` | Source Disposition | `OBSERVED_INDEPENDENT` | Reality report | Behaviour validation | disposition matrix | source -> disposition -> use/reject | `HIGH` | Disposition matrix exists. |
| `BD-002` | Discovery Index Resolution | `OBSERVED_INDEPENDENT` | Function Graph index | Reality report | Function Graph `.md/.json` | index -> official-source resolution | `HIGH` | Function Graph consumed as evidence index. |
| `BD-002` | Behaviour Instance Capture | `OBSERVED_INDEPENDENT` | Reality report | Behaviour aggregation | Behaviour Instance Registry | instance -> chain matrix | `HIGH` | Concrete registry exists. |
| `BD-002` | Reality Aggregation | `OBSERVED_INDEPENDENT` | Reality report | Behaviour Catalogue/Coverage/Graph | aggregation tables | instances -> definitions -> coverage | `HIGH` | Aggregation is explicit and verified. |
| `BD-003` | CPS State Recording | `OBSERVED_INDEPENDENT` | CPS owner | OMP/operator/dashboard | CPS document | state -> next action / readiness | `HIGH` | CPS exists as volatile state owner. |
| `BD-003` | OMP Candidate Consumption | `HYPOTHESIZED` | future Phase 3/AEP | OMP | no Phase 2 candidate produced | no current candidate consumption | `LOW` | Future route, not current observed behaviour. |
| `BD-003` | OMP Mission Routing | `HYPOTHESIZED` | OMP | execution owner | OMP model | no AEP Phase 2 mission routed | `LOW` | Valid OMP capability, but not observed from current Reality output. |
| `BD-003` | OMP Continuation State Update | `OBSERVED_INDEPENDENT` | OMP/CPS | operator/next action | OMP/CPS docs | continue/hold/state-update | `MEDIUM_HIGH` | Existing continuation model and state evidence exist. |
| `BD-003` | Production Maturity Handoff | `OBSERVED_INDEPENDENT` | reports/evidence | Production Maturity/CPS | Production Maturity and CPS | maturity decision -> CPS state | `MEDIUM_HIGH` | Owner path exists and is evidenced. |
| `BD-004` | Candidate Observation | `OBSERVED_INTERNAL_STEP` | routing inputs | candidate evaluation | routing/intelligence inputs | lacks standalone decision/learning | `MEDIUM_HIGH` | Real input acquisition, but not independent Behaviour. |
| `BD-004` | Candidate Evaluation | `OBSERVED_INDEPENDENT` | RoutingBrain | decision overlay/operator | `RoutingBrain.candidate_*` | evaluate -> score -> tests | `HIGH` | Has producer, output, tests, and consumer. |
| `BD-004` | Policy Filtering | `OBSERVED_INDEPENDENT` | decision overlay | operator decision surface | `build_knowledge_decision_overlay` | allow/block/reason -> tests | `HIGH` | Independent filtering behaviour exists. |
| `BD-004` | Capacity / Service Validation | `OBSERVED_INDEPENDENT` | service fit models | routing advisory | service fit/best-pool code | fit/pass/fail -> tests | `HIGH` | Separate validation behaviour exists. |
| `BD-004` | Trust / Prediction Scoring | `OBSERVED_INDEPENDENT` | intelligence workers | routing/decision surfaces | trust/prediction snapshots | score -> confidence -> feedback | `HIGH` | Has source, tests, and learning consumers. |
| `BD-004` | Best Pool Recommendation | `OBSERVED_INDEPENDENT` | RoutingBrain | operator decision surface | `best_available_pool_advice` | rank -> recommend -> tests | `HIGH` | Produces independent recommendation output. |
| `BD-004` | Decision Overlay / Proposal | `OBSERVED_INDEPENDENT` | operator decision surface | operator/admin | decision overlay/batch preview | proposal -> preview -> tests | `HIGH` | Real operator-facing proposal behaviour exists. |
| `BD-005` | Service Matrix Observation | `OBSERVED_INDEPENDENT` | service matrix refresh | routing/health models | service matrix tools/evidence | observe -> matrix -> freshness | `HIGH` | Observable evidence and consumer paths exist. |
| `BD-005` | Channel Trust Observation | `OBSERVED_INDEPENDENT` | intelligence workers | routing/trust models | trust/recovery snapshots | trust state -> tests -> learning | `HIGH` | Trust observation is implemented and tested. |
| `BD-005` | Degradation Signal Classification | `OBSERVED_INDEPENDENT` | autonomy trust model | policy/decision consumers | degradation policy mapping | classify -> policy mapping | `HIGH` | Separate classification behaviour exists. |
| `BD-005` | Freshness / Anti-Flap Evaluation | `OBSERVED_COMPOSITE_NOT_ADMISSIBLE` | freshness and anti-flap models | routing/authority gates | `build_freshness_actionability`, `build_anti_flapping` | two policy decisions | `HIGH` | Evidence exists, but this proposed item combines two policies. |
| `BD-005` | Scoped Incident Observation | `OBSERVED_INDEPENDENT` | runtime/evidence reports | verification/OMP | scoped reports/policies | observe -> verify/hold | `MEDIUM` | Engineering evidence exists; live incident state unavailable. |
| `BD-006` | Authority Requirement Resolution | `OBSERVED_INDEPENDENT` | OMP/authority model | execution owner/operator | authority docs/tests | required/not required -> approval path | `HIGH` | Authority boundary is current system behaviour. |
| `BD-006` | Action-Class Classification | `OBSERVED_INDEPENDENT` | action-class model | runtime eligibility/OMP | action-class runtime enablement | classify -> eligibility | `HIGH` | Implemented and tested. |
| `BD-006` | Blast-Radius Boundary Evaluation | `OBSERVED_INDEPENDENT` | blast-radius evidence model | authority/runtime gate | blast-radius evidence rows | scope -> allow/hold | `HIGH` | Separate evidence and policy path exists. |
| `BD-006` | Approval Decision | `OBSERVED_INDEPENDENT` | operator/authority path | execution owner | approval packet/governance paths | approve/deny/hold | `MEDIUM_HIGH` | Governed approval behaviour exists. |
| `BD-006` | Runtime Eligibility Governance | `OBSERVED_INDEPENDENT` | runtime eligibility model | OMP/operator | delegated runtime eligibility | eligible/not eligible -> tests | `HIGH` | Implemented as read-only eligibility governance. |
| `BD-007` | Movement Candidate Admission | `OBSERVED_INDEPENDENT` | autoswitch/governed canary | execution pipeline | governed canary code/tests | admit/reject candidate | `HIGH` | Candidate admission is implemented. |
| `BD-007` | Lease / Version Readiness | `OBSERVED_INDEPENDENT` | operator execution | runtime guard | `build_execution_lease` | lease ready/not ready | `HIGH` | Real lease readiness path exists. |
| `BD-007` | Restore Barrier Readiness | `OBSERVED_INDEPENDENT` | operator execution | execution/rollback gates | restore barrier clearance | clear/hold -> tests | `HIGH` | Implemented and tested. |
| `BD-007` | Governed Dry-Run / Apply Selection | `OBSERVED_INDEPENDENT` | execution pipeline | operator/runtime owner | governed canary cycle | dry-run/apply/hold | `HIGH` | Governed selection path exists. |
| `BD-007` | Guarded Runtime Execution | `HYPOTHESIZED` | not proven as admitted current runtime mutation | runtime | no observed current mutation path | execution not observed/admitted | `LOW` | Guarded dry-run exists; independent Runtime execution is not current evidence. |
| `BD-007` | Verification Handoff | `OBSERVED_INTERNAL_STEP` | execution pipeline | verification owner | verification policy links | handoff only | `MEDIUM_HIGH` | Real handoff, not independent Behaviour. |
| `BD-007` | Rollback Handoff | `OBSERVED_INTERNAL_STEP` | execution pipeline | rollback owner | rollback policy links | handoff only | `MEDIUM_HIGH` | Real handoff, not independent Behaviour. |
| `BD-008` | Runtime Convergence Verification | `OBSERVED_INDEPENDENT` | sync/truth tools | deployment/production owners | `v7_sync_lib`, truth reports | pass/fail/unknown | `HIGH` | Independent verification target exists. |
| `BD-008` | Action Terminal Classification | `OBSERVED_INDEPENDENT` | execution/verification policy | learning/rollback/maturity | terminal classification tests | terminal -> outcome | `HIGH` | Terminal classification is tested. |
| `BD-008` | Runtime Read Diagnostic Verification | `OBSERVED_INDEPENDENT` | runtime read views | operator/OMP | runtime read/diagnostic views | read -> validate/unknown | `HIGH` | Real read-only verification path exists. |
| `BD-008` | Incident Scoped Verification | `OBSERVED_INDEPENDENT` | scoped reports/policies | OMP/operator | incident/scoped evidence | verify/hold/stop-safe | `MEDIUM` | Evidence exists; live state unavailable. |
| `BD-008` | Production / Certification Truth Closure | `OBSERVED_INDEPENDENT` | certification reports | Production Maturity/CPS | reports and maturity owner | certify -> maturity/state | `MEDIUM_HIGH` | Owner path and reports exist. |
| `BD-009` | Rollback Readiness Check | `OBSERVED_INDEPENDENT` | rollback policy/readiness | execution/authority | rollback readiness evidence | ready/not ready | `HIGH` | Readiness behaviour exists. |
| `BD-009` | Rollback Authority Certification | `OBSERVED_INDEPENDENT` | autonomy trust model | authority/operator | rollback authority certification | certify for review / do not enable | `HIGH` | Explicit implementation exists. |
| `BD-009` | Restore Barrier Clearance | `OBSERVED_INDEPENDENT` | operator execution | runtime apply/rollback | restore barrier clearance | clear/hold | `HIGH` | Implemented and tested. |
| `BD-009` | Rollback Execution Path | `HYPOTHESIZED` | not proven as admitted current runtime action | runtime/rollback owner | readiness paths only | no independent current execution proof | `LOW` | Rollback readiness exists; execution path is not current admitted Reality. |
| `BD-009` | Post-Rollback Verification / Learning | `OBSERVED_INDEPENDENT` | feedback/trust tests | learning/routing | rollback-related feedback tests | rollback outcome -> learning | `MEDIUM_HIGH` | Evidence exists for post-rollback learning interpretation. |
| `BD-010` | Outcome Quality Evaluation | `OBSERVED_INDEPENDENT` | feedback owner | learning/maturity | `outcome_quality_evaluation` | evaluate -> quality | `HIGH` | Implemented and tested. |
| `BD-010` | Decision Learning Record | `OBSERVED_INDEPENDENT` | feedback owner | trust/prediction | `decision_learning_record` | record -> learning model | `HIGH` | Implemented and tested. |
| `BD-010` | Trust Evolution Update | `OBSERVED_INDEPENDENT` | intelligence workers | routing/decision models | trust evolution snapshot | update trust -> tests | `HIGH` | Implemented and tested. |
| `BD-010` | Prediction Feedback | `OBSERVED_INDEPENDENT` | intelligence workers | prediction confidence | prediction feedback rows | actual vs forecast | `HIGH` | Implemented and tested. |
| `BD-010` | Recommendation Confidence Adjustment | `OBSERVED_INDEPENDENT` | intelligence platform | OMP/operator | confidence/recommendation reports | adjust confidence | `MEDIUM_HIGH` | Engineering evidence exists. |
| `BD-010` | Evidence Quality Feedback | `OBSERVED_INDEPENDENT` | Engineering Intelligence | OMP/dashboard/framework | reports and SYSTEM_MAP | evidence quality -> recommendation | `MEDIUM` | Evidence exists mostly through reports/model. |
| `BD-011` | Production Evidence Consumption | `OBSERVED_INDEPENDENT` | reports/evidence dirs | certification/maturity | production evidence snapshots | consume/invalid/accept | `HIGH` | Evidence consumption is visible. |
| `BD-011` | Production Certification Review | `OBSERVED_INDEPENDENT` | certification process | Production Maturity/CPS | certification reports | pass/hold/reject | `HIGH` | Multiple certification reports exist. |
| `BD-011` | Maturity Decision | `OBSERVED_INDEPENDENT` | Production Maturity | CPS/OMP | maturity model/CPS | accept/block/no-change | `HIGH` | Existing owner path. |
| `BD-011` | No-Change / Block Explanation | `OBSERVED_INDEPENDENT` | OMP/report process | CPS/next action | State Transition Law | explained no-change/block | `HIGH` | Required and evidenced in reports. |
| `BD-011` | CPS Maturity State Recording | `OBSERVED_INDEPENDENT` | CPS | OMP/dashboard | CPS fields | record maturity state | `HIGH` | CPS records current maturity. |
| `BD-012` | Operator Overview Projection | `OBSERVED_INDEPENDENT` | overview views | operator/admin | `overview_views.py` | project -> display | `HIGH` | Implemented projection. |
| `BD-012` | Runtime Diagnostic View | `OBSERVED_INDEPENDENT` | runtime/diagnostic views | operator/OMP | `runtime_read_views.py`, `diagnostic_views.py` | read -> diagnostic output | `HIGH` | Implemented and tested. |
| `BD-012` | Decision Preview | `OBSERVED_INDEPENDENT` | decision surface | operator | operator decision surface | preview/propose | `HIGH` | Implemented and tested. |
| `BD-012` | Audit / Evidence Search | `OBSERVED_INDEPENDENT` | operator observability | operator/engineering | audit search functions | search -> result/export | `HIGH` | Implemented. |
| `BD-012` | Governance / Execution Preview | `OBSERVED_INDEPENDENT` | operator observability | operator/authority | governance/execution preview | preview -> review | `HIGH` | Implemented. |
| `BD-012` | Export Preview | `OBSERVED_INDEPENDENT` | operator observability | operator/engineering | audit export preview | export preview | `HIGH` | Implemented. |
| `BD-013` | Knowledge Change Detection | `OBSERVED_INDEPENDENT` | Stage 2 reports | knowledge owner | knowledge inventory/extraction evidence | detect -> queue/review | `MEDIUM_HIGH` | Stage 2 proves real knowledge detection behaviour. |
| `BD-013` | Knowledge Owner Evaluation | `OBSERVED_INDEPENDENT` | Stage 2 acceptance | canonical knowledge owner | acceptance reports | accept/hold/reject | `MEDIUM_HIGH` | Engineering evidence exists. |
| `BD-013` | Canonical Sync | `OBSERVED_INDEPENDENT` | Stage 2 lock | canonical docs/owners | knowledge lock report | sync/verify | `HIGH` | Canonical sync was performed in Stage 2. |
| `BD-013` | Foundation Synchronization | `OBSERVED_INDEPENDENT` | AEP foundation model/report | phase execution | AEP Phase 1/foundation evidence | synchronize/verify | `MEDIUM_HIGH` | AEP foundation lifecycle is evidenced. |
| `BD-013` | No-Change Recording | `OBSERVED_INDEPENDENT` | reports/laws | OMP/CPS | State Transition Law | explain no-change | `HIGH` | Real report pattern exists. |
| `BD-013` | OMP / Owner Handoff | `HYPOTHESIZED` | not uniformly proven | OMP/owner | handoff model | consumption not confirmed | `MEDIUM_LOW` | Required route, but insufficient current evidence as standalone Behaviour. |
| `BD-014` | Diagnosis And Owner Resolution | `OBSERVED_INDEPENDENT` | Domain 11 implementation/tests | OMP/CPS/PM/reports | diagnosis record/projection | produce/validate/project | `HIGH` | Real read-only Behaviour exists. |
| `BD-015` | Deployment Manifest Production | `OBSERVED_INDEPENDENT` | sync tooling | deploy/release process | `build_deploy_manifest` | manifest -> validation | `HIGH` | Implemented. |
| `BD-015` | Safe Deploy Execution | `OBSERVED_INDEPENDENT` | deploy reports/evidence | runtime/deployment owner | safe deploy evidence | deploy/hold/report | `MEDIUM_HIGH` | Deployment evidence exists. |
| `BD-015` | Runtime Linkage Recording | `OBSERVED_INDEPENDENT` | sync tooling | runtime/deploy verification | `build_runtime_linkage` | linkage -> verify | `HIGH` | Implemented. |
| `BD-015` | Post-Deploy Convergence Check | `OBSERVED_INDEPENDENT` | truth/convergence tools | deployment/maturity | truth/convergence reports | pass/fail/unknown | `HIGH` | Evidence exists. |
| `BD-015` | Deploy Rollback / Hold Decision | `OBSERVED_INDEPENDENT` | deploy safety reports | deploy/rollback owner | deploy reports and rollback policy | hold/rollback/no-op | `MEDIUM_HIGH` | Hold/rollback decision behaviour evidenced. |
| `BD-015` | Production Maturity Handoff | `OBSERVED_INDEPENDENT` | certification/maturity reports | Production Maturity/CPS | reports/state docs | handoff -> maturity decision | `MEDIUM_HIGH` | Existing owner handoff path evidenced. |

## 9. Reality Validation Matrix

| Category | Count | Reality Admission |
| --- | ---: | --- |
| Observed and independent | `69` | May be used in a future Reality Refinement. |
| Observed but internal step | `3` | Must not become standalone Behaviour. |
| Observed but still composite | `1` | Must be refined before admission. |
| Hypothesized | `6` | Must not enter Current Autonomous Behaviour Reality. |

## 10. Hypothesized Behaviours

The following proposed Behaviours are not sufficiently proven as current independent V7 Behaviour:

- Owner Consumption / Continuation;
- OMP Candidate Consumption;
- OMP Mission Routing;
- Guarded Runtime Execution;
- Rollback Execution Path;
- OMP / Owner Handoff.

These may become observed later only if real engineering evidence proves producer, consumer, execution, verification, and state/learning continuation.

## 11. Confidence Assessment

| Confidence Band | Behaviour Count | Notes |
| --- | ---: | --- |
| `HIGH` | `55` | Source code, tests, Function Graph, or direct report evidence clearly supports the behaviour. |
| `MEDIUM_HIGH` | `15` | Evidence exists, but owner consumption/live state/freshness is less direct. |
| `MEDIUM` | `3` | Evidence exists mainly through reports or unavailable live state limits confidence. |
| `MEDIUM_LOW` | `2` | Governance route exists but consumption confirmation is weak. |
| `LOW` | `4` | Hypothesized due to absent current execution/admission proof. |

## 12. Independent Certification

| Review | Result | Notes |
| --- | --- | --- |
| Reality Validation Review | `PASS` | Every proposed Behaviour was validated against evidence. |
| Observed Behaviour Review | `PASS` | Observed catalogue contains only evidence-backed Behaviours. |
| Evidence Review | `PASS_WITH_MINOR_RISKS` | Live runtime/admin state remains unavailable; no live state was assumed. |
| Behaviour Independence Review | `PASS` | Internal steps and still-composite proposals were rejected as standalone Behaviours. |
| Implementation Reality Review | `PASS` | Source/test/Function Graph/report evidence was used where available. |
| Reality First Review | `PASS` | Architecture/model-only items were not accepted without evidence. |
| No Hypothetical Behaviour Review | `PASS` | Hypothesized items are explicitly barred from Reality. |
| Architecture Review | `PASS` | No architecture changes or new owners created. |
| Quality Review | `PASS` | Validation distinguishes evidence, independence, and confidence. |
| Self Review | `PASS` | No Phase 3, Closure, Gap, Runtime, AEP, AOS, or locked-foundation changes performed. |

## 13. Final Verdict

Reality Validation verdict:

```text
BEHAVIOUR_REALITY_VALIDATION_PASS
```

PASS/HOLD:

```text
PASS
```

Final rule for future Reality Refinement:

```text
Only OBSERVED_INDEPENDENT Behaviours may be considered for admission into a refined Current Autonomous Behaviour Reality.
HYPOTHESIZED, OBSERVED_INTERNAL_STEP, and OBSERVED_COMPOSITE_NOT_ADMISSIBLE entries must not be admitted as standalone Behaviours.
```

Current Autonomous Behaviour Reality remains unchanged.
