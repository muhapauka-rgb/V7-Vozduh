# V7 Behaviour Decomposition Review

Status: `INDEPENDENT_GRANULARITY_AUDIT`
Program Context: `V7_AUTONOMOUS_EVOLUTION_PROGRAM`
Input Reality: `docs/reports/research/V7_CURRENT_AUTONOMOUS_BEHAVIOUR_REALITY.md`
Date: `2026-07-08`

## 1. Scope

This review audits the granularity of the Behaviour Definitions discovered in Current Autonomous Behaviour Reality.

It does not:

- start Phase 3;
- certify Autonomous Behaviour Gaps;
- execute Closure;
- modify Runtime;
- modify AEP;
- modify AOS;
- modify `LOCKED_ARCHITECTURE`;
- modify `LOCKED_KNOWLEDGE`;
- change the Current Autonomous Behaviour Reality artifact.

The review uses the already collected Reality, previously consumed source families, Function Graph evidence, implementation evidence, runtime model evidence, and the existing Behaviour Definition / Behaviour Instance model.

No new source discovery was performed.

## 2. Decomposition Rule

A Behaviour Definition is `ATOMIC` when it has one engineering purpose, one primary situation class, one decision family, one execution meaning, one verification meaning, and one learning/continuation meaning.

A Behaviour Definition is `COMPOSITE` when it contains multiple independent Behaviours, each with its own:

- Situation;
- Context;
- Interpretation;
- Decision;
- Execution;
- Verification;
- Learning or continuation.

The review does not split by file, function, class, or implementation count. It splits only when the internal behaviour can exist as an engineering behaviour on its own.

## 3. Review Summary

| Metric | Count |
| --- | ---: |
| Behaviour Definitions reviewed | `15` |
| Atomic Behaviour Definitions | `1` |
| Composite Behaviour Definitions | `14` |
| Recommended decompositions | `14` |
| No-change decisions | `1` |
| Runtime changes performed | `0` |
| Gap certifications performed | `0` |
| Phase 3 started | `NO` |

## 4. Behaviour Granularity Matrix

| Current Behaviour | Atomic / Composite | Reason | Internal Behaviours | Recommended Decomposition | Impact |
| --- | --- | --- | --- | --- | --- |
| `BD-001 Program Execution And Report Lifecycle` | `COMPOSITE` | It combines operator command interpretation, source/foundation consumption, report production, review, and owner consumption. These have separate decisions and verifications. | Program Command Interpretation; Foundation/Source Consumption; Report Production; Review/Certification Recording; Owner Consumption / Continuation. | Split into separate report-lifecycle behaviours before Phase 3 uses it as evidence. | Improves traceability of what was executed, what was consumed, and what was only reported. |
| `BD-002 Source Discovery And Reality Modeling` | `COMPOSITE` | Discovery, source disposition, Function Graph resolution, Behaviour Instance capture, and Reality aggregation are independent behaviours with different verification criteria. | Source Enumeration; Source Disposition; Discovery Index Resolution; Behaviour Instance Capture; Reality Aggregation. | Split into discovery and reality-modeling behaviours. | Prevents Phase 3 from treating "source discovery" and "current behaviour reality" as one gap surface. |
| `BD-003 OMP Mission Routing And Continuation` | `COMPOSITE` | It mixes CPS volatile state recording, OMP mission consumption/routing, production maturity consumption, and knowledge continuation. | CPS State Recording; OMP Candidate Consumption; OMP Mission Routing; OMP Continuation State Update; Production Maturity Consumption Handoff. | Split into OMP routing and CPS/consumer continuation behaviours. | Preserves OMP as execution owner and avoids hidden second state-machine interpretation. |
| `BD-004 Routing Advisory And Selection` | `COMPOSITE` | Routing advisory contains multiple autonomous behaviour decisions: candidate observation, evaluation, policy filtering, trust scoring, pool recommendation, and decision overlay. | Candidate Observation; Candidate Evaluation; Policy Filtering; Capacity/Service Validation; Trust/Prediction Scoring; Best Pool Recommendation; Decision Overlay / Proposal. | Split into advisory pipeline behaviours, with Runtime apply explicitly excluded. | Gives Phase 3 precise surfaces for advisory behaviour without implying authority. |
| `BD-005 Channel And Service Observation` | `COMPOSITE` | Service matrix, channel trust, degradation classification, freshness/anti-flap evaluation, and scoped incident observation each have separate context and verification. | Service Matrix Observation; Channel Trust Observation; Degradation Signal Classification; Freshness/Anti-Flap Evaluation; Scoped Incident Observation. | Split into observation families by decision/verifier, not by implementation file. | Reduces ambiguity between passive observation, degradation interpretation, and incident verification. |
| `BD-006 Authority And Action-Class Governance` | `COMPOSITE` | Authority resolution, action-class classification, blast-radius boundary, approval decision, and runtime eligibility are separable behaviours. | Authority Requirement Resolution; Action-Class Classification; Blast-Radius Boundary Evaluation; Approval Decision; Runtime Eligibility Governance. | Split into authority classification and approval/eligibility behaviours. | Prevents a single authority label from hiding multiple independent governance decisions. |
| `BD-007 Runtime Apply And Movement Guard` | `COMPOSITE` | It contains lease readiness, restore readiness, dry-run/apply decision, guarded execution, verification routing, and rollback handoff. | Movement Candidate Admission; Lease/Version Readiness; Restore Barrier Readiness; Governed Dry-Run / Apply Selection; Guarded Runtime Execution; Verification Handoff; Rollback Handoff. | Split into admission/readiness/execution/handoff behaviours. | Clarifies which part is current read-only/gated reality versus actual Runtime mutation. |
| `BD-008 Verification And Truth Closure` | `COMPOSITE` | Verification spans runtime convergence, action terminal classification, read-only diagnostics, incident verification, and production/certification truth closure. | Runtime Convergence Verification; Action Terminal Classification; Runtime Read Diagnostic Verification; Incident Scoped Verification; Production/Certification Truth Closure. | Split verification by independent verification target. | Avoids treating all verification failures or unknowns as one behavioural surface. |
| `BD-009 Rollback And Restore Barrier` | `COMPOSITE` | Rollback readiness, rollback authority, restore barrier clearance, rollback execution, and post-rollback classification can exist independently. | Rollback Readiness Check; Rollback Authority Certification; Restore Barrier Clearance; Rollback Execution Path; Post-Rollback Verification / Learning. | Split readiness, authority, barrier, execution, and post-verification. | Makes clear that rollback evidence exists without granting automatic rollback authority. |
| `BD-010 Learning And Outcome Feedback` | `COMPOSITE` | Outcome quality, trust evolution, prediction feedback, recommendation adjustment, and evidence-quality feedback are distinct learning behaviours. | Outcome Quality Evaluation; Decision Learning Record; Trust Evolution Update; Prediction Feedback; Recommendation Confidence Adjustment; Evidence Quality Feedback. | Split by learning target. | Prevents outcome learning from being over-generalized into one maturity or routing signal. |
| `BD-011 Production Certification And Maturity` | `COMPOSITE` | Production certification, maturity decision, evidence consumption, CPS update, and blocked/no-change explanation are separate owner decisions. | Production Evidence Consumption; Production Certification Review; Maturity Decision; No-Change / Block Explanation; CPS Maturity State Recording. | Split certification from maturity state mutation and CPS recording. | Keeps Production Maturity owner decision separate from evidence availability. |
| `BD-012 Operator/Admin Visibility` | `COMPOSITE` | Operator overview, runtime diagnostics, decision preview, audit/evidence search, and export/governance preview are different visibility behaviours. | Operator Overview Projection; Runtime Diagnostic View; Decision Preview; Audit/Evidence Search; Governance/Execution Preview; Export Preview. | Split by operator situation and consumer need. | Prevents read-only UI surfaces from being flattened into one visibility behaviour. |
| `BD-013 Knowledge Evolution And Canonical Sync` | `COMPOSITE` | Knowledge evolution, canonical sync, foundation synchronization, no-change decision, and owner handoff have different terminal states. | Knowledge Change Detection; Knowledge Owner Evaluation; Canonical Sync; Foundation Synchronization; No-Change Recording; OMP/Owner Handoff. | Split durable knowledge evolution from synchronization and continuation. | Avoids implying that every evidence finding updates canonical knowledge. |
| `BD-014 Diagnosis And Owner Resolution` | `ATOMIC` | It has one engineering purpose: produce a read-only diagnosis/owner-resolution record and projection from supplied evidence without mutation. Builder, validation, and projection are implementation/contract steps, not independent behaviours in the current Reality. | Diagnosis Evidence Intake; Diagnosis Record Production; Consumer Projection; Governance Exposure. | No decomposition recommended now. Keep as one Behaviour unless future evidence shows independent diagnosis and projection lifecycles. | Preserves Domain 11 as a single read-only owner-resolution behaviour. |
| `BD-015 Deployment And Convergence` | `COMPOSITE` | Manifest generation, safe deploy, runtime linkage, post-deploy convergence, rollback/no-op decision, and maturity consumption are separate behaviours. | Deployment Manifest Production; Safe Deploy Execution; Runtime Linkage Recording; Post-Deploy Convergence Check; Deploy Rollback / Hold Decision; Production Maturity Handoff. | Split deployment lifecycle behaviours before Phase 3 depends on them. | Separates deployment evidence from convergence proof and maturity consumption. |

## 5. Recommended Decomposition Catalogue

The following catalogue is a recommendation only. It is not applied to Current Autonomous Behaviour Reality in this review.

### BD-001 Recommended Children

| Recommended Behaviour | Implemented / Conceptual | Notes |
| --- | --- | --- |
| Program Command Interpretation | `IMPLEMENTED` | Evidenced by operator-driven program/report workflow. |
| Foundation / Source Consumption | `IMPLEMENTED` | Evidenced by AEP foundation and source-disposition rules. |
| Engineering Report Production | `IMPLEMENTED` | Evidenced by Stage 2 and AEP reports. |
| Review / Certification Recording | `IMPLEMENTED` | Evidenced by review sections and certification reports. |
| Owner Consumption / Continuation | `PARTIALLY_OBSERVED` | Evidence exists, but consumption confirmation varies by owner. |

### BD-002 Recommended Children

| Recommended Behaviour | Implemented / Conceptual | Notes |
| --- | --- | --- |
| Source Enumeration | `IMPLEMENTED` | Repository enumeration observed. |
| Source Disposition | `IMPLEMENTED` | Disposition matrix exists. |
| Discovery Index Resolution | `IMPLEMENTED` | Function Graph consumed as index. |
| Behaviour Instance Capture | `IMPLEMENTED` | Behaviour Instance Registry exists. |
| Reality Aggregation | `IMPLEMENTED` | Definitions, coverage, and graph exist. |

### BD-003 Recommended Children

| Recommended Behaviour | Implemented / Conceptual | Notes |
| --- | --- | --- |
| CPS State Recording | `IMPLEMENTED` | CPS is existing volatile owner. |
| OMP Candidate Consumption | `CONCEPTUAL_IN_PHASE_2` | Phase 2 creates no mission; later phases may feed OMP. |
| OMP Mission Routing | `CONCEPTUAL_IN_PHASE_2` | Not executed in Phase 2. |
| OMP Continuation State Update | `IMPLEMENTED_AS_MODEL` | Defined by OMP/CPS, not executed here. |
| Production Maturity Handoff | `IMPLEMENTED_AS_MODEL` | Existing owner path; not recalculated here. |

### BD-004 Recommended Children

| Recommended Behaviour | Implemented / Conceptual | Notes |
| --- | --- | --- |
| Candidate Observation | `IMPLEMENTED` | Evidence in routing/intelligence inputs. |
| Candidate Evaluation | `IMPLEMENTED` | RoutingBrain and advisory scoring. |
| Policy Filtering | `IMPLEMENTED` | Policy and decision overlays. |
| Capacity / Service Validation | `IMPLEMENTED` | Service fit and best-pool evidence. |
| Trust / Prediction Scoring | `IMPLEMENTED` | Trust and prediction models. |
| Best Pool Recommendation | `IMPLEMENTED` | Best available pool advice. |
| Decision Overlay / Proposal | `IMPLEMENTED` | Operator decision surface. |

### BD-005 Recommended Children

| Recommended Behaviour | Implemented / Conceptual | Notes |
| --- | --- | --- |
| Service Matrix Observation | `IMPLEMENTED` | Service matrix evidence and timers. |
| Channel Trust Observation | `IMPLEMENTED` | Trust/recovery model evidence. |
| Degradation Signal Classification | `IMPLEMENTED` | Degradation policy mapping evidence. |
| Freshness / Anti-Flap Evaluation | `IMPLEMENTED` | Freshness and anti-flap models. |
| Scoped Incident Observation | `PARTIALLY_OBSERVED` | Emergency/scoped evidence exists, live state unavailable. |

### BD-006 Recommended Children

| Recommended Behaviour | Implemented / Conceptual | Notes |
| --- | --- | --- |
| Authority Requirement Resolution | `IMPLEMENTED` | Authority rules and tests. |
| Action-Class Classification | `IMPLEMENTED` | Action-class ladder and runtime enablement evidence. |
| Blast-Radius Boundary Evaluation | `IMPLEMENTED` | Blast radius evidence and policies. |
| Approval Decision | `IMPLEMENTED_AS_GOVERNED_PATH` | Requires operator/authority decision. |
| Runtime Eligibility Governance | `IMPLEMENTED` | Runtime eligibility models. |

### BD-007 Recommended Children

| Recommended Behaviour | Implemented / Conceptual | Notes |
| --- | --- | --- |
| Movement Candidate Admission | `IMPLEMENTED` | Autoswitch/governed candidate evidence. |
| Lease / Version Readiness | `IMPLEMENTED` | Execution lease evidence. |
| Restore Barrier Readiness | `IMPLEMENTED` | Restore barrier tests/evidence. |
| Governed Dry-Run / Apply Selection | `IMPLEMENTED_AS_GATED_PATH` | Dry-run and guarded apply model exist. |
| Guarded Runtime Execution | `PARTIALLY_OBSERVED` | Runtime mutation not performed in Phase 2. |
| Verification Handoff | `IMPLEMENTED` | Verification policy/evidence. |
| Rollback Handoff | `IMPLEMENTED` | Rollback policy/readiness evidence. |

### BD-008 Recommended Children

| Recommended Behaviour | Implemented / Conceptual | Notes |
| --- | --- | --- |
| Runtime Convergence Verification | `IMPLEMENTED` | Truth/convergence evidence. |
| Action Terminal Classification | `IMPLEMENTED` | Terminal classification policy/tests. |
| Runtime Read Diagnostic Verification | `IMPLEMENTED` | Runtime read/diagnostic views. |
| Incident Scoped Verification | `PARTIALLY_OBSERVED` | Evidence exists; live incident state unavailable. |
| Production / Certification Truth Closure | `IMPLEMENTED_AS_OWNER_PATH` | Production maturity consumes verified evidence. |

### BD-009 Recommended Children

| Recommended Behaviour | Implemented / Conceptual | Notes |
| --- | --- | --- |
| Rollback Readiness Check | `IMPLEMENTED` | Rollback readiness evidence. |
| Rollback Authority Certification | `IMPLEMENTED_AS_REVIEW_ONLY` | Authority review only; no automatic authority. |
| Restore Barrier Clearance | `IMPLEMENTED` | Restore barrier model/tests. |
| Rollback Execution Path | `PARTIALLY_OBSERVED` | Path exists; automatic execution not granted here. |
| Post-Rollback Verification / Learning | `IMPLEMENTED_AS_MODEL` | Learning/feedback paths exist. |

### BD-010 Recommended Children

| Recommended Behaviour | Implemented / Conceptual | Notes |
| --- | --- | --- |
| Outcome Quality Evaluation | `IMPLEMENTED` | Feedback module evidence. |
| Decision Learning Record | `IMPLEMENTED` | Learning record model. |
| Trust Evolution Update | `IMPLEMENTED` | Trust evolution snapshots. |
| Prediction Feedback | `IMPLEMENTED` | Prediction feedback models. |
| Recommendation Confidence Adjustment | `IMPLEMENTED` | Confidence/recommendation evidence. |
| Evidence Quality Feedback | `IMPLEMENTED_AS_MODEL` | Engineering Intelligence and evidence quality signals. |

### BD-011 Recommended Children

| Recommended Behaviour | Implemented / Conceptual | Notes |
| --- | --- | --- |
| Production Evidence Consumption | `IMPLEMENTED` | Evidence directories and reports. |
| Production Certification Review | `IMPLEMENTED_AS_OWNER_PATH` | Certification reports exist. |
| Maturity Decision | `IMPLEMENTED_AS_OWNER_PATH` | Production Maturity owns decision. |
| No-Change / Block Explanation | `IMPLEMENTED_AS_LAW` | State Transition Law. |
| CPS Maturity State Recording | `IMPLEMENTED` | CPS consumes maturity state. |

### BD-012 Recommended Children

| Recommended Behaviour | Implemented / Conceptual | Notes |
| --- | --- | --- |
| Operator Overview Projection | `IMPLEMENTED` | Overview/admin read models. |
| Runtime Diagnostic View | `IMPLEMENTED` | Runtime read and diagnostic views. |
| Decision Preview | `IMPLEMENTED` | Operator decision surface. |
| Audit / Evidence Search | `IMPLEMENTED` | Operator observability model. |
| Governance / Execution Preview | `IMPLEMENTED` | Operator preview surfaces. |
| Export Preview | `IMPLEMENTED` | Audit/export preview behaviour. |

### BD-013 Recommended Children

| Recommended Behaviour | Implemented / Conceptual | Notes |
| --- | --- | --- |
| Knowledge Change Detection | `IMPLEMENTED_AS_GOVERNED_PATH` | Evidence can trigger owner review. |
| Knowledge Owner Evaluation | `IMPLEMENTED_AS_OWNER_PATH` | Existing knowledge owner path required. |
| Canonical Sync | `IMPLEMENTED_AS_OWNER_PATH` | Sync allowed only through existing owners. |
| Foundation Synchronization | `IMPLEMENTED_AS_AEP_MODEL` | AEP foundation sync model. |
| No-Change Recording | `IMPLEMENTED_AS_LAW` | State Transition Law. |
| OMP / Owner Handoff | `IMPLEMENTED_AS_MODEL` | Existing continuation model. |

### BD-014 No-Change Decision

| Recommended Behaviour | Implemented / Conceptual | Notes |
| --- | --- | --- |
| Diagnosis And Owner Resolution | `IMPLEMENTED` | Keep atomic for now. Internal record/projection/validation are contract steps under one read-only owner-resolution behaviour. |

### BD-015 Recommended Children

| Recommended Behaviour | Implemented / Conceptual | Notes |
| --- | --- | --- |
| Deployment Manifest Production | `IMPLEMENTED` | Sync/deploy tooling evidence. |
| Safe Deploy Execution | `IMPLEMENTED_AS_EVIDENCE_PATH` | Deploy reports and evidence. |
| Runtime Linkage Recording | `IMPLEMENTED` | Runtime linkage manifests. |
| Post-Deploy Convergence Check | `IMPLEMENTED` | Truth/convergence evidence. |
| Deploy Rollback / Hold Decision | `IMPLEMENTED_AS_GOVERNED_PATH` | Deploy safety evidence. |
| Production Maturity Handoff | `IMPLEMENTED_AS_OWNER_PATH` | Maturity consumes accepted evidence. |

## 6. Hidden Multiplicity Audit

| Multiplicity Type | Found In | Result |
| --- | --- | --- |
| Multiple Decisions | `BD-001`, `BD-002`, `BD-003`, `BD-004`, `BD-006`, `BD-007`, `BD-011`, `BD-015` | Composite decomposition recommended. |
| Multiple Verification Paths | `BD-001`, `BD-002`, `BD-007`, `BD-008`, `BD-009`, `BD-011`, `BD-015` | Composite decomposition recommended. |
| Multiple Learning Paths | `BD-010`, `BD-011`, `BD-013` | Composite decomposition recommended. |
| Multiple Runtime Paths | `BD-004`, `BD-007`, `BD-008`, `BD-012`, `BD-015` | Composite decomposition recommended where Runtime path changes behaviour meaning. |
| Multiple Policies | `BD-005`, `BD-006`, `BD-007`, `BD-009` | Composite decomposition recommended. |
| Multiple Rollback Paths | `BD-007`, `BD-009`, `BD-015` | Composite decomposition recommended. |
| Multiple OMP Interactions | `BD-001`, `BD-003`, `BD-011`, `BD-013` | Composite decomposition recommended. |

## 7. No-Change Decisions

| Behaviour | Decision | Reason |
| --- | --- | --- |
| `BD-014 Diagnosis And Owner Resolution` | `NO_DECOMPOSITION_RECOMMENDED` | The current evidence shows one read-only owner-resolution behaviour. Validation and consumer projection are necessary internal contract steps, not separate engineering behaviours in the current Reality. |

## 8. Impact Assessment

This review recommends updating the granularity of Current Autonomous Behaviour Reality before Phase 3 is used to certify any Autonomous Behaviour Gap.

The recommendation does not require:

- new architecture;
- new Runtime;
- new owner;
- new OMP route;
- new AEP phase;
- new source discovery;
- changing `LOCKED_ARCHITECTURE`;
- changing `LOCKED_KNOWLEDGE`.

Expected positive impact:

- Phase 3 can evaluate smaller Behaviour units;
- hidden decisions and verification paths become explicit;
- OMP mission routing remains safer because composite behaviours are not treated as single implementation units;
- Reality remains bottom-up because decomposition is derived from existing Behaviour Instances and evidence.

Risk if no decomposition is applied before Phase 3:

- Phase 3 may certify overly broad gaps;
- OMP could receive missions that mix several independent behaviours;
- verification, rollback, learning, and authority boundaries may be less visible.

## 9. Independent Certification

| Review | Result | Notes |
| --- | --- | --- |
| Behaviour Granularity Review | `PASS` | All `15` Behaviour Definitions were reviewed for granularity. |
| Behaviour Atomicity Review | `PASS_WITH_RECOMMENDATIONS` | `14` composite definitions identified; `1` atomic definition retained. |
| Behaviour Completeness Review | `PASS` | No source rediscovery required; review used existing Reality. |
| Architecture Review | `PASS` | No architecture or owner changes proposed. |
| Quality Review | `PASS` | Decomposition uses engineering behaviour criteria, not function/file count. |
| Reality Review | `PASS` | Current Reality is not modified; recommendations derive from existing instances. |
| Duplication Review | `PASS` | Recommended children are behaviour-level, not duplicate documents or owners. |
| Self Review | `PASS` | No Phase 3, Closure, Gap, Runtime, AEP, AOS, or locked-foundation changes performed. |

## 10. Final Verdict

Audit verdict:

```text
BEHAVIOUR_DECOMPOSITION_REVIEW_PASS
```

Granularity verdict:

```text
CURRENT_BEHAVIOUR_REALITY_IS_VALID_AS_TOP_LEVEL_MAP_BUT_TOO_COMPOSITE_FOR_SAFE_PHASE_3_INPUT
```

Next recommendation:

```text
Before Phase 3, run a separate operator-approved update of Current Autonomous Behaviour Reality to apply or reject the recommended decomposition.
```

This review does not apply the decomposition automatically.
