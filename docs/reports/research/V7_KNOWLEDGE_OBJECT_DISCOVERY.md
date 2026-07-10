# V7 Knowledge Object Discovery

Status: `KNOWLEDGE_OBJECT_DISCOVERY_COMPLETE`
Date: `2026-07-08`
Scope: Discovery of existing V7 transformation objects only.

## 1. Purpose

This discovery answers one question:

```text
Does V7 already have one unified engineering object that moves through Observation -> Evidence -> Learning -> Knowledge -> Canonical Knowledge -> Future Autonomous Decision?
```

This document does not create a Knowledge Object, Experience Object, new memory, new owner, new architecture, new Runtime, new Planner, new truth source, new storage, new Knowledge system, or new Learning system.

## 2. Discovery Inputs

| Input | Evidence Used |
| --- | --- |
| Memory Architecture Discovery | Existing memory families and their owners, producers, consumers, lifetime, retention, and hierarchy. |
| Knowledge & Memory Transformation Discovery | Existing transformations and their owner/consumer/verification/canonicalization rules. |
| Stage 2 Knowledge Engineering Program | Existing Stage 2 Knowledge Object model, extraction unit, atomicity, and verification rules. |
| Behaviour Discovery Program | Behaviour Definition, Behaviour Instance, identity model, traceability chain, truth hierarchy, and evolution dispositions. |
| Current Autonomous Behaviour Reality | Concrete Behaviour Instances and Behaviour Definitions currently observed in V7. |
| AEP | Chain Closure Law, Consumer Confirmation Law, result lifecycle, canonical sync, Knowledge Evolution, and autonomous behaviour phases. |
| AOS / Execution Mission Protocol | Execution Context, same execution object, production execution identity, learning and CPS/OMP closure. |
| LOCKED_KNOWLEDGE / Canonical Knowledge | Permanent engineering memory, provenance, terminal-state boundaries, and Knowledge Evolution-only updates. |
| SYSTEM_MAP / Canonical Reference | Owner, producer, consumer, relationship, and source boundaries. |
| OMP / CPS / Production Maturity | Current-state, maturity, continuation, and consumer confirmation paths. |
| Function Graph | Discovery index for producers, consumers, functions, mutation paths, and implementation evidence. |

## 3. Current Transformation Objects

V7 already uses multiple explicit object families.

| Object Family | Existing Scope | Identity Boundary | Owner | What It Is Not |
| --- | --- | --- | --- | --- |
| Observation | Initial noticed fact, runtime/production signal, or behaviour candidate. | Situation/source/time/evidence envelope, often incomplete. | Observation/runtime evidence owners. | Not verified evidence, not learning, not canonical truth. |
| Evidence Record | Captured proof with source, owner, provenance, freshness, and identity. | Evidence source/provenance/freshness/owner. | Evidence/report/verification owners. | Not automatically verified, not automatically knowledge. |
| Verified Evidence | Evidence accepted for a specific consumer and scope. | Same evidence identity plus verification result and scope. | Verification owners. | Not the same object as a learning record or canonical knowledge. |
| Execution Context | Permanent production execution object until terminal state. | mission id, execution id, operation id, planner generation, selected move hash, user/source/target, stage, owner. | OMP / Runtime Model / Decision Model composition. | Not a knowledge object and not a canonical truth object. |
| Decision | Selected no-action/action/hold/escalation/rollback/manual-review result. | Decision identity, policy, evidence, authority, runtime context. | Decision Model / OMP / planner owners. | Not execution by itself and not learning by itself. |
| Outcome / Feedback Record | Terminal result consumed by learning and maturity paths. | Outcome identity tied to same execution/outcome evidence. | Outcome / feedback / learning owners. | Not the same object as the original observation. |
| Learning Record / Summary | Real outcome-backed learning, trust, prediction, confidence, or recommendation-quality memory. | Outcome/evidence lineage and learning family. | Learning / trust / prediction owners. | Advisory unless consumed through owner gates; not authority. |
| Engineering Report | Durable evidence and decision context artifact. | Report path, scope, evidence, review, owner/consumer, next action. | Engineering report lifecycle / OMP. | Not durable truth owner by itself. |
| Knowledge Candidate | Stage 2 / Knowledge Evolution candidate for extraction or review. | Candidate id, source, category, destination, priority/risk. | Stage 2 / Knowledge owner path. | Not yet a Knowledge Object. |
| Knowledge Object | Atomic reusable engineering knowledge unit in Stage 2. | knowledge id, category, owner, terminal state, consumer, provenance, forbidden misuse. | Knowledge Owner / Stage 2 program. | Not graph node, canonical concept, canonical prose, or universal V7 object. |
| Canonical Knowledge | Accepted terminal engineering truth in locked knowledge/canonical baseline. | Canonical owner, terminal state, provenance, lock/acceptance path. | Knowledge Owner / Canonical owners. | Not evidence, report, learning, or runtime state. |
| Behaviour Candidate | Candidate behaviour found by BDP. | Candidate evidence and provisional identity signature. | BDP. | Not automatically a Behaviour Definition or current Reality. |
| Behaviour Definition | Stable engineering identity of a behaviour type across time. | purpose, situation class, decision responsibility, execution responsibility, consumer, verification, learning, boundary, owner, provenance family. | BDP / AEP Reality owners. | Not Evidence or Knowledge Object. |
| Behaviour Instance | Concrete occurrence of a Behaviour Definition in current reality. | definition identity, concrete situation/context, evidence occurrence, producer/consumer, terminal/freshness state. | BDP / AEP Reality owners. | Does not create a new Behaviour Definition by default. |
| Chain Closure Element | Generic closure contract around a produced result. | element, producer, end state, consumer, consumption evidence, next action, terminal alternative. | AEP / OMP / responsible existing owner. | Not a domain object; it is a lifecycle wrapper for many object families. |
| Function Graph Node / Edge | Static implementation relationship index. | node/edge id and source path/function relationship. | Function Graph owner. | Discovery index only; not truth source or Knowledge Object. |

## 4. Transformation Object Matrix

| Transformation | Input Object | Output Object | Same Object? | Reason |
| --- | --- | --- | --- | --- |
| Production reality -> Observation | Production/runtime fact | Observation | No | A fact is captured as an observation envelope. |
| Observation -> Evidence | Observation | Evidence Record | No | Evidence adds source, owner, provenance, and freshness. |
| Evidence -> Verified Evidence | Evidence Record | Verified Evidence state/result | Same evidence identity, new verification state | Verification changes admissibility, not source identity. |
| Verified Evidence -> Runtime Decision Eligibility | Verified Evidence | Decision eligibility / packet / lease state | No | Operational eligibility is a distinct runtime/decision object. |
| Decision Eligibility -> Execution Context | Decision / packet / lease | Execution Context / same execution object | No, then same within execution | Execution Context freezes production execution identity. |
| Execution Context -> Runtime Apply / STOP_SAFE | Execution Context | Apply result or STOP_SAFE result | Same execution object with new stage | Production execution identity must be preserved until terminal state. |
| Apply / STOP_SAFE -> Verification | Apply result | Verification result | No | Verification result is a consumer output for the apply result. |
| Verification -> Rollback / Containment Closure | Verification result | Rollback/no-rollback/containment status | No | Rollback closure is a separate safety object. |
| Verification + Rollback -> Outcome | Verification and rollback state | Outcome / Feedback Record | No | Outcome summarizes terminal result for learning/maturity consumers. |
| Outcome -> Learning | Outcome / Feedback Record | Learning Record / trust/prediction update | No | Learning is derived from outcome evidence. |
| Learning -> Advisory Future Decision Input | Learning summary | Advisory decision input / confidence / trust signal | No | Advisory signals can influence future decision surfaces but do not become decisions. |
| Verified Evidence / Outcome / Learning -> Engineering Report | Evidence/outcome/learning objects | Engineering Report | No | Report preserves and routes evidence; it is a container/consumer artifact. |
| Engineering Report -> Production Maturity | Engineering Report | Maturity decision | No | Maturity owner consumes report and produces decision. |
| Production Maturity -> CPS | Maturity decision | Current Program State update/no-change | No | CPS stores volatile current operational state, not maturity object identity. |
| CPS / Report / Maturity -> OMP | CPS/report/maturity result | OMP continuation/mission/hold/impossibility | No | OMP consumes outputs and determines continuation. |
| Behaviour Evidence -> Behaviour Candidate / Instance | Evidence Records | Behaviour Candidate / Behaviour Instance | No | Behaviour object is identified from evidence; evidence remains separate. |
| Behaviour Candidate -> Behaviour Definition | Candidate / Instance | Existing/new/versioned Behaviour Definition | No or reuse existing Definition | Definition identity may be reused, versioned, or rejected. |
| Behaviour Definition / Instance -> Reality Proposal | Behaviour objects | Reality Refinement Proposal / Current Reality update if accepted | No | Reality proposal is an acceptance artifact. |
| Behaviour contradiction -> Knowledge Evolution trigger | Behaviour/evidence contradiction | Knowledge Evolution trigger | No | Contradiction routes to existing Knowledge Owner path. |
| Knowledge Candidate -> Knowledge Object | Candidate | Zero, one, or multiple Knowledge Objects | No | Stage 2 explicitly allows zero/one/multiple objects from one candidate. |
| Knowledge Object -> Canonical Knowledge | Extracted/deduplicated object/graph concept | Canonical Knowledge prose/baseline | No | Stage 2 says Knowledge Object is not canonical prose/concept. |
| Canonical Knowledge -> Future Decision | Canonical truth | Decision constraint/input | No | Canonical knowledge constrains future decisions; it is not the decision object. |
| Function Graph -> Discovery | Graph node/edge | Discovery lead / evidence index reference | No | Function Graph is an index; truth must be confirmed elsewhere. |

## 5. Object Identity

No single identity survives the whole chain from observation to future autonomous decision.

Existing identity scopes are deliberately local:

| Identity | Stable Within | Stops Being Same Object When |
| --- | --- | --- |
| Evidence identity | Evidence provenance, owner, source, freshness, and scope. | Evidence is consumed to create learning, report, maturity decision, or knowledge candidate. |
| Execution identity | Frozen production execution until terminal state. | Execution completes, becomes historical mission evidence, or a new execution is explicitly started. |
| Behaviour Definition identity | Stable behaviour type across time. | Defining identity factors change enough to require version update or new definition. |
| Behaviour Instance identity | Concrete occurrence of a Behaviour Definition. | A different concrete situation/context/evidence occurrence is processed. |
| Knowledge Object identity | Stage 2 extracted atomic knowledge object. | It is deduplicated, graphed, canonicalized, or superseded; canonical prose is not the same object. |
| Canonical Knowledge identity | Locked accepted truth state. | Knowledge Evolution accepts and locks a future state. |
| Report identity | Artifact path/scope/report lineage. | A consumer produces a maturity decision, CPS update, OMP continuation, or canonical sync decision. |
| Chain Closure identity | Produced result lifecycle. | The lifecycle closes or routes to next consumer; it wraps different object families rather than replacing them. |

The closest unifying mechanism is not an object. It is traceability:

```text
source/provenance
  -> owner
  -> identity
  -> consumer
  -> verification
  -> terminal state
  -> next action or terminal alternative
```

## 6. Object Lifecycle

V7 uses linked lifecycles, not one universal lifecycle.

Production execution lifecycle:

```text
Observation
  -> World Model
  -> Planner / Decision
  -> Authority
  -> Runtime
  -> Apply or STOP_SAFE
  -> Verification
  -> Rollback / Containment
  -> Outcome
  -> Learning
  -> Engineering Report
  -> CPS
  -> OMP / Production Maturity
```

Knowledge lifecycle:

```text
Source / Evidence / Report
  -> Knowledge Candidate
  -> Atomicity Review
  -> Zero / One / Multiple Knowledge Objects
  -> Verification
  -> Deduplication / Graph
  -> Canonical Knowledge
  -> Acceptance
  -> Lock
```

Behaviour lifecycle:

```text
Observed Behaviour Candidate
  -> Behaviour Identity Resolution
  -> Behaviour Instance Identity
  -> Behaviour Traceability Review
  -> Reality Refinement Proposal
  -> Current Autonomous Behaviour Reality if accepted
  -> AEP Phase 3 / OMP / Knowledge Evolution if applicable
```

Chain closure lifecycle:

```text
Producer
  -> Result Produced
  -> Consumer Assigned
  -> Consumer Consumed
  -> Consumption Confirmed
  -> Next Action
  -> Chain Closed
```

These lifecycles interoperate by consumer confirmation, not by preserving one universal object identity.

## 7. Object Transformation

Object transformation in V7 has three patterns:

| Pattern | Meaning | Examples |
| --- | --- | --- |
| State transition of same object | Same identity gains a new state within a bounded lifecycle. | Evidence -> verified evidence; Execution Context stage update; Behaviour Definition evidence refresh. |
| Derived object creation | A new object is produced from consumed evidence or result. | Outcome -> Learning Record; Report -> Production Maturity Decision; Candidate -> Knowledge Object. |
| Consumer routing / closure | A result is consumed and routed to next owner or terminal alternative. | Report -> OMP; Learning -> no-change/Knowledge Evolution/Production Maturity; Evidence -> terminal evidence-only. |

The universal rule is not "same object continues."

The universal rule is:

```text
No produced result is complete until an existing consumer confirms consumption or an existing owner records a terminal alternative.
```

## 8. Object Relationships

V7 relates objects through links, not inheritance into one master object.

| Relationship | Meaning |
| --- | --- |
| Observation -> Evidence | Observation becomes evidence only after capture with source/provenance/owner. |
| Evidence -> Verification | Evidence can receive a verification state for a specific consumer. |
| Evidence -> Behaviour Instance | Evidence can prove a concrete behaviour occurrence. |
| Behaviour Instance -> Behaviour Definition | Instance resolves to existing/new/versioned/ambiguous behaviour type. |
| Outcome -> Learning | Real outcome produces learning/trust/prediction update. |
| Evidence / Learning / Report -> Knowledge Evolution | Durable contradiction or durable knowledge-change evidence can trigger Knowledge Owner path. |
| Knowledge Object -> Canonical Knowledge | Knowledge Objects can feed canonical knowledge, but they are not canonical prose/concepts. |
| Canonical Knowledge -> Decision | Canonical truth constrains future decisions. |
| Function Graph -> Evidence Discovery | Graph relationships help find objects, but do not become object truth. |

## 9. Object State Changes

| Object | States Observed |
| --- | --- |
| Evidence | observed, recorded, verified, rejected, stale, historical, superseded, consumed. |
| Execution Context | init, executing, breakpoint, investigating, correcting, resuming, success, canonical impossibility, incomplete execution. |
| Behaviour Candidate | new, existing with new evidence, existing with new implementation, renamed, versioned, duplicate rejected, ambiguous. |
| Behaviour Trace | complete, complete with unknowns, partial hold, fail. |
| Knowledge Candidate | no object created, one object created, multiple objects created, manual review, rejected with reason. |
| Knowledge Object | extracted, verified, deduplicated, graph-consumed, canonicalization input, superseded/historical when applicable. |
| Canonical Knowledge | accepted, locked, unchanged, future locked state through Knowledge Evolution. |
| Learning | recorded, advisory, consumed, no-change, hold, routed to OMP/CPS/Production Maturity/Knowledge Evolution. |
| Chain Closure Element | not produced, produced, assigned, consumed, confirmed, closed, hold, continues, terminal accepted/rejected/hold/impossible. |

## 10. Object Producers

| Object | Producer |
| --- | --- |
| Observation | Runtime, diagnostics, production observation, repository/program discovery, operator/program command. |
| Evidence Record | Evidence owners, verification tools, reports, runtime/state tools, implementation/index producers. |
| Verified Evidence | Verification owners and certification owners. |
| Execution Context | OMP / Runtime Model / Decision Model composition. |
| Decision | Decision Model / OMP / planner/read-model owner path. |
| Outcome / Feedback Record | Runtime/apply, verification, rollback, and feedback owners. |
| Learning Record | Learning / trust / prediction owners from real outcomes. |
| Engineering Report | Codex/engineer/program executor. |
| Behaviour Candidate / Instance / Definition | BDP and AEP Reality path from evidence and identity resolution. |
| Knowledge Candidate / Knowledge Object | Stage 2 / Knowledge Evolution owner path. |
| Canonical Knowledge | Knowledge Owner after acceptance/lock. |
| Maturity Decision | Production Maturity owner. |
| CPS Update | Current Program State owner. |
| OMP Continuation | OMP. |

## 11. Object Consumers

| Object | Consumers |
| --- | --- |
| Observation | Evidence owners, BDP, runtime/read-model owners. |
| Evidence Record | Verification, BDP, OMP, Production Maturity, Learning, Engineering Reports. |
| Verified Evidence | Runtime decision eligibility, reports, Production Maturity, Learning, Knowledge Evolution where durable. |
| Execution Context | Runtime, verification, rollback, learning, CPS, OMP. |
| Outcome / Feedback Record | Learning, Production Maturity, Engineering Reports, OMP. |
| Learning Record | OMP, CPS, Production Maturity, Knowledge Evolution, decision advisory surfaces. |
| Engineering Report | Named owner, OMP, CPS, Production Maturity, canonical owner, Knowledge Evolution where durable. |
| Behaviour Definition / Instance | Behaviour Reality, AEP Phase 3, OMP, BDP future runs. |
| Knowledge Object | Stage 2.3 Deduplication, Stage 2.4 Graph, Stage 2.5 Canonical Knowledge. |
| Canonical Knowledge | OMP, AEP, BDP, engineers, Codex, future decision and discovery work. |
| Function Graph Node / Edge | BDP, AEP, engineers, relationship discovery; official sources must verify truth. |

## 12. Object Ownership

Object ownership is distributed:

- Stage 2 Knowledge Object belongs to Stage 2 / Knowledge Owner scope.
- Behaviour Definition and Behaviour Instance belong to BDP / AEP Reality scope.
- Execution Context belongs to OMP / Runtime Model / Decision Model composition.
- Evidence belongs to the producing evidence/verification/report owner.
- Learning belongs to Learning / trust / prediction owners.
- Production Maturity decisions belong to Production Maturity.
- CPS updates belong to CPS.
- Canonical Knowledge belongs to Knowledge Owner / canonical owner path.

No existing document establishes one owner for one universal object spanning all of these scopes.

## 13. Object Canonicalization

Only knowledge can become canonical truth, and only through the existing Knowledge Owner path.

Canonicalization rules observed:

- Stage 2 Knowledge Object is not canonical prose or canonical concept.
- Engineering Reports are evidence-only unless promoted by existing owner path.
- Behaviour evidence can trigger Knowledge Evolution but cannot rewrite locked knowledge.
- Learning can inform future decisions but does not become canonical by itself.
- Function Graph can support discovery but cannot become truth source by itself.
- `LOCKED_KNOWLEDGE` changes only through Knowledge Evolution and accepted lock.

Therefore canonicalization is a transformation between object families, not a state change of one universal object.

## 14. Need For Unified Knowledge Object

Discovery verdict:

```text
UNIFIED_KNOWLEDGE_OBJECT_NOT_FOUND
```

V7 does not currently use a single engineering object that remains identical across:

```text
Observation
  -> Evidence
  -> Learning
  -> Knowledge
  -> Canonical Knowledge
  -> Future Autonomous Decision
```

This is not a defect by itself.

The existing architecture intentionally uses:

- bounded object identities;
- explicit producer/consumer relationships;
- traceability paths;
- provenance;
- verification;
- terminal state;
- consumer confirmation;
- Knowledge Evolution for canonical truth;
- OMP/Authority/Production Maturity for autonomous action.

The need for a new unified object is not proven.

What is proven:

```text
V7_NEEDS_TRACEABILITY_ACROSS_OBJECTS
```

What is not proven:

```text
V7_NEEDS_ONE_UNIFIED_KNOWLEDGE_OBJECT
```

## 15. Evidence

| Evidence | Finding |
| --- | --- |
| Stage 2 Knowledge Object Model | Defines Knowledge Object only as minimum engineering knowledge unit in Stage 2; not graph node, canonical concept, or canonical prose. |
| Stage 2 Extraction Lifecycle | One Knowledge Candidate can produce zero, one, or multiple Knowledge Objects, proving candidate and object are not the same cross-system entity. |
| BDP Behaviour Identity Model | Defines Behaviour Definition and Behaviour Instance identity, but explicitly creates no owner, truth source, storage, Runtime identity, Planner identity, or architecture layer. |
| BDP Traceability Model | Preserves the full engineering life of a Behaviour through linked records; it does not create a new memory system. |
| AEP Chain Closure Law | Applies to many element types: phases, actions, artifacts, gaps, missions, implementations, verification, evidence, learning, canonical sync, reports, program state. It is a generic closure contract, not one object identity. |
| Execution Mission Protocol | Maintains same Execution Context only within production execution until terminal state. It does not become Knowledge Object or Canonical Knowledge. |
| Knowledge & Memory Transformation Discovery | Shows most transformations create derived objects or consume objects, not mutate one universal object. |
| Memory Architecture Discovery | Shows multiple memory families with separate owners, lifetimes, evidence levels, and canonical status. |
| Current Autonomous Behaviour Reality | Behaviour Instances aggregate into Behaviour Definitions, while learning, maturity, CPS, and knowledge evolution remain separate consumer paths. |

## 16. Independent Certification

| Review | Verdict | Notes |
| --- | --- | --- |
| Knowledge Object Review | `PASS` | Existing Stage 2 Knowledge Object model is correctly scoped to knowledge extraction, not the whole V7 architecture. |
| Transformation Review | `PASS` | Transformation matrix shows when same identity is preserved and when a new object is produced. |
| Memory Review | `PASS` | Multiple memory families remain distinct and owner-mapped. |
| Knowledge Review | `PASS` | Canonical knowledge path remains Knowledge Evolution / accepted lock only. |
| Reality Review | `PASS` | Behaviour and production reality are evidence-backed, not inferred from a unified object assumption. |
| Reuse Review | `PASS` | Existing object models and traceability mechanisms were reused. |
| Owner Review | `PASS` | No universal owner exists or was created; existing object owners remain intact. |
| Duplication Review | `PASS` | No new Knowledge Object, Experience Object, memory, storage, truth source, or architecture was created. |
| Quality Review | `PASS_WITH_MINOR_RISKS` | Cross-object traceability exists, but there is no single object registry; this is an auditability risk, not proof of architecture gap. |
| Self Review | `PASS` | Discovery did not design or introduce a new object. |

## 17. Engineering Report

### Summary

Knowledge Object Discovery was completed as a single self-contained report.

The discovery found that V7 uses distinct object families linked by traceability, provenance, owner/consumer contracts, verification, and terminal states. It did not find one unified object that remains the same from Observation through Evidence, Learning, Knowledge, Canonical Knowledge, and Future Autonomous Decision.

### Objects Discovered

- Observation;
- Evidence Record;
- Verified Evidence;
- Execution Context;
- Decision;
- Outcome / Feedback Record;
- Learning Record / Summary;
- Engineering Report;
- Behaviour Candidate;
- Behaviour Definition;
- Behaviour Instance;
- Knowledge Candidate;
- Knowledge Object;
- Canonical Knowledge;
- Chain Closure Element;
- Function Graph Node / Edge.

### Reuse

The discovery reused:

- Memory Architecture Discovery;
- Knowledge & Memory Transformation Discovery;
- Stage 2 Knowledge Object Model;
- BDP Behaviour Identity and Traceability Models;
- AEP Chain Closure and Consumer Confirmation;
- Execution Context / same execution object discipline;
- Canonical Knowledge and Knowledge Evolution boundaries;
- OMP, CPS, Production Maturity, Verification, Learning, Function Graph, SYSTEM_MAP, and Canonical Reference.

### Existing Object Model

The existing V7 object model is not one universal object model.

It is a linked-object model:

```text
bounded object identities
  -> deterministic transformations
  -> producer / consumer contracts
  -> verification
  -> traceability
  -> terminal state or next action
```

### Need For Unified Object

No need for a unified object is proven.

The stronger existing need is:

```text
cross-object traceability discipline
```

not:

```text
new unified Knowledge Object
```

### PASS / HOLD

```text
KNOWLEDGE_OBJECT_DISCOVERY_PASS_WITH_MINOR_RISKS
```

Minor risk:

- V7 has no single cross-system object registry. This can make audits harder, but existing traceability, chain closure, and owner/consumer contracts already provide the required architectural continuity.

## 18. Final Answer

V7 does not currently use one unified engineering entity that passes unchanged through:

```text
Observation
  -> Evidence
  -> Learning
  -> Knowledge
  -> Canonical Knowledge
  -> Future Autonomous Decision
```

The architecture consciously uses different objects without a single universal entity.

Final verdict:

```text
KNOWLEDGE_OBJECT_DISCOVERY_PASS_WITH_MINOR_RISKS
UNIFIED_KNOWLEDGE_OBJECT_NOT_FOUND
ARCHITECTURE_USES_LINKED_OBJECT_FAMILIES
NO_NEW_KNOWLEDGE_OBJECT_REQUIRED
NO_NEW_EXPERIENCE_OBJECT_REQUIRED
NO_NEW_OWNER_REQUIRED
NO_NEW_ARCHITECTURE_REQUIRED
```

The correct existing abstraction is not a unified object. It is the traceable chain between object families.
