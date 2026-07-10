# V7 Stage 2.2 Knowledge Extraction Rerun

Date: 2026-07-07

Program: `V7_STAGE2_KNOWLEDGE_ENGINEERING_PROGRAM`

Stage: `Stage 2.2 - Knowledge Extraction`

Execution Type: `RERUN_WITH_ATOMICITY_REVIEW`

Program State:

```text
STAGE_1_LOCKED
STAGE_2_PROGRAM_ACCEPTED
STAGE_2_1_ACCEPTED_WITH_MINOR_RISKS
STAGE_2_2_READY
```

Stage result:

```text
STAGE_2_2_EXTRACTION_PASS
STAGE_2_3_READY
STAGE_2_3_IN_PROGRESS = FALSE
```

## 1. Stage Summary

This rerun re-executed Stage 2.2 under the updated Stage 2 program.

The previous Stage 2.2 report was used only as historical evidence for comparison. It was not copied, preserved, or treated as the expected object count.

Execution source:

```text
docs/reports/research/V7_STAGE2_1_KNOWLEDGE_INVENTORY.md
```

Approved queue verdict:

```text
QUEUE_READY_FOR_STAGE_2_2
QUEUE_IS_CANDIDATE_BASED_NOT_DOCUMENT_BASED
```

No new Knowledge Candidates were searched.
No Stage 2.1 inventory artifact was changed.
No Stage 2.3 work was performed.

## 2. Applied Lifecycle

Every queue candidate was processed through the official lifecycle:

```text
Knowledge Candidate
  -> Resolve Sources
  -> Resolve Terminal State
  -> Resolve Trust
  -> Resolve Owner
  -> Resolve Consumer
  -> Resolve Provenance
  -> Extract Knowledge
  -> Atomicity Review
  -> Create Knowledge Object(s)
  -> Knowledge Object Verification
  -> Save
  -> Extraction Complete
```

Atomicity Review results are mandatory and are recorded for every candidate.

## 3. Atomicity Review Results

| Queue ID | Candidate | Atomicity Review | Disposition | Objects | Atomicity basis |
|---|---|---|---|---:|---|
| Q-001 | KC-001 Locked Stage 1 Architecture Baseline | ATOMIC | ONE_OBJECT_CREATED | 1 | One baseline-lock law with one terminal state and one destination. |
| Q-002 | KC-002 26-Domain Responsibility Chain | SPLIT_REQUIRED | MULTIPLE_OBJECTS_CREATED | 27 | The chain assertion and each domain responsibility can exist independently and are graph-consumable separately. |
| Q-003 | KC-003 Architecture Closed By Default | ATOMIC | ONE_OBJECT_CREATED | 1 | One architecture-change boundary. |
| Q-004 | KC-004 Reality First Law | ATOMIC | ONE_OBJECT_CREATED | 1 | One verification law. |
| Q-005 | KC-005 Existing Owner Before New Owner | ATOMIC | ONE_OBJECT_CREATED | 1 | One owner-resolution law. |
| Q-006 | KC-006 Authority Boundary | SPLIT_REQUIRED | MULTIPLE_OBJECTS_CREATED | 2 | Positive authority ownership and forbidden authority misuse are independent assertions with different misuse surfaces. |
| Q-007 | KC-007 Runtime Apply Boundary | ATOMIC | ONE_OBJECT_CREATED | 1 | One Runtime boundary. |
| Q-008 | KC-009 Verification Before Promotion | ATOMIC | ONE_OBJECT_CREATED | 1 | One promotion/verification law. |
| Q-009 | KC-010 Rollback / Closure Terminal Safety | SPLIT_REQUIRED | MULTIPLE_OBJECTS_CREATED | 2 | Rollback authority and closure terminal-state safety are independent lifecycle responsibilities. |
| Q-010 | KC-011 Domain 11 Diagnosis Terminal State | ATOMIC | ONE_OBJECT_CREATED | 1 | One terminal certification state, with implementation details preserved as provenance. |
| Q-011 | KC-012 OMP Permanent Operating Program | ATOMIC | ONE_OBJECT_CREATED | 1 | One permanent operating-program law. |
| Q-012 | KC-014 Knowledge Preservation Rules | SPLIT_REQUIRED | MULTIPLE_OBJECTS_CREATED | 3 | Evidence role, canonical owner role, and durable-promotion rule can stand independently. |
| Q-013 | KC-015 No Orphan Artifact / Report Evidence Rule | SPLIT_REQUIRED | MULTIPLE_OBJECTS_CREATED | 2 | No-orphan artifact completeness and verified evidence consumption are separate rules. |
| Q-014 | KC-021 Program State Machine and Stage Gates | SPLIT_REQUIRED | MULTIPLE_OBJECTS_CREATED | 2 | State machine and stage-gate law are separate lifecycle/governance assertions. |
| Q-015 | KC-022 Producer / Consumer Model | SPLIT_REQUIRED | MULTIPLE_OBJECTS_CREATED | 7 | Each stage producer/consumer contract has distinct producer, consumer, output, and acceptance state. |
| Q-016 | KC-023 Forbidden Stage 2 Actions | SPLIT_REQUIRED | MULTIPLE_OBJECTS_CREATED | 5 | Forbidden architecture, owner/truth, runtime/authority, OMP, and stage-boundary actions are independent misuse boundaries. |
| Q-017 | KC-013 CPS Volatile Current State Boundary | ATOMIC | ONE_OBJECT_CREATED | 1 | One volatile-state boundary. |
| Q-018 | KC-018 Product Identity: Governed Routing Platform | ATOMIC | ONE_OBJECT_CREATED | 1 | One product identity principle. |
| Q-019 | KC-019 Canonical Policy Library Rules | SPLIT_REQUIRED | MULTIPLE_OBJECTS_CREATED | 2 | Policy non-invention and operationalization lifecycle are independent rules. |
| Q-020 | KC-020 ADR Supersession and Decision Rules | SPLIT_REQUIRED | MULTIPLE_OBJECTS_CREATED | 3 | ADR home, ADR update rule, and supersession handling are independent evidence/decision rules. |
| Q-021 | KC-016 Function Graph Implementation Reality | MANUAL_REVIEW | MANUAL_REVIEW | 0 | Derived Function Graph evidence has sync debt and cannot deterministically become current truth. |
| Q-022 | KC-017 Research-Derived System Laws | MANUAL_REVIEW | MANUAL_REVIEW | 0 | Research-derived object boundaries and canonical owner routing require bounded review. |
| Q-023 | KC-024 Historical Stage 1 Evidence | ATOMIC | NO_OBJECT_CREATED | 0 | Historical-only source family; no active reusable Knowledge Object created in Stage 2.2. |
| Q-024 | KC-025 Old Stage 2 Corpus Validation Label | MANUAL_REVIEW | MANUAL_REVIEW | 0 | Superseded label is historical and can confuse active route without review. |

Every candidate has one terminal disposition.

## 4. Candidate Dispositions

| Disposition | Count | Candidates |
|---|---:|---|
| ONE_OBJECT_CREATED | 10 | KC-001, KC-003, KC-004, KC-005, KC-007, KC-009, KC-011, KC-012, KC-013, KC-018 |
| MULTIPLE_OBJECTS_CREATED | 10 | KC-002, KC-006, KC-010, KC-014, KC-015, KC-021, KC-022, KC-023, KC-019, KC-020 |
| MANUAL_REVIEW | 3 | KC-016, KC-017, KC-025 |
| NO_OBJECT_CREATED | 1 | KC-024 |
| REJECTED_WITH_REASON | 0 | None |

## 5. Candidates Split

| Candidate | Object count | Why split was required |
|---|---:|---|
| KC-002 | 27 | The chain-level assertion and each domain responsibility can exist independently and are consumed differently by Knowledge Graph and canonical knowledge work. |
| KC-006 | 2 | Authority ownership and Authority forbidden misuse are different atomic assertions. |
| KC-010 | 2 | Rollback authorization and closure terminal safety are different lifecycle responsibilities. |
| KC-014 | 3 | Evidence role, canonical owner role, and durable-promotion lifecycle are separate rules. |
| KC-015 | 2 | Artifact completeness and evidence verification are separate governance/evidence rules. |
| KC-021 | 2 | Program state machine and stage-gate law are separate lifecycle rules. |
| KC-022 | 7 | Producer/consumer contracts differ by stage, producer, consumer, output, and acceptance result. |
| KC-023 | 5 | Forbidden actions fall into distinct architecture, owner/truth, runtime/authority, OMP, and stage-boundary families. |
| KC-019 | 2 | Policy source discipline and policy operationalization lifecycle are separate rules. |
| KC-020 | 3 | ADR storage, ADR update, and supersession handling are separate decision/evidence rules. |

## 6. Extracted Knowledge Registry

All objects below passed Schema, Source, Trust Level, Terminal State, Owner, Consumer, Provenance, Destination, Forbidden Misuse, Review State, and Atomicity verification before registry admission.

| Knowledge ID | Candidate | Title | Category | Sources | Owner | Trust | Terminal State | Destination | Consumers | Provenance | Forbidden Misuse | Atomicity | Review State |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KO-2.2R-001 | KC-001 | Locked Stage 1 Architecture Baseline | Laws / Boundaries | SRC-002, SRC-003, SRC-004 | Stage 1 Acceptance / Canonical Reference | TERMINAL | TSR-001 | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; OMP | KC-001 -> Q-001 -> TSR-001 | Do not reopen Stage 1, alter architecture, or grant production authority. | ATOMIC | extracted |
| KO-2.2R-002 | KC-002 | 26-Domain Chain Completeness | Responsibilities / Producer-Consumer | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | CANONICAL KNOWLEDGE + KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4; Stage 2.5 | KC-002 -> Q-002 -> TSR-002 | Do not add, remove, merge, split, or reorder domains. | SPLIT_REQUIRED | extracted |
| KO-2.2R-003 | KC-002 | Domain 01 Business Objective Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 01 | Do not merge this responsibility into another domain. | SPLIT_REQUIRED | extracted |
| KO-2.2R-004 | KC-002 | Domain 02 System Laws Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 02 | Do not merge this responsibility into another domain. | SPLIT_REQUIRED | extracted |
| KO-2.2R-005 | KC-002 | Domain 03 Product Principles Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 03 | Do not merge this responsibility into another domain. | SPLIT_REQUIRED | extracted |
| KO-2.2R-006 | KC-002 | Domain 04 Reality Model Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 04 | Do not merge this responsibility into another domain. | SPLIT_REQUIRED | extracted |
| KO-2.2R-007 | KC-002 | Domain 05 Observation Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 05 | Do not merge this responsibility into another domain. | SPLIT_REQUIRED | extracted |
| KO-2.2R-008 | KC-002 | Domain 06 Health Evidence Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 06 | Do not merge this responsibility into another domain. | SPLIT_REQUIRED | extracted |
| KO-2.2R-009 | KC-002 | Domain 07 Intelligence Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 07 | Do not merge this responsibility into another domain. | SPLIT_REQUIRED | extracted |
| KO-2.2R-010 | KC-002 | Domain 08 Routing Intelligence Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 08 | Do not merge this responsibility into another domain. | SPLIT_REQUIRED | extracted |
| KO-2.2R-011 | KC-002 | Domain 09 Wake Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 09 | Do not merge this responsibility into another domain. | SPLIT_REQUIRED | extracted |
| KO-2.2R-012 | KC-002 | Domain 10 Incident Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 10 | Do not merge this responsibility into another domain. | SPLIT_REQUIRED | extracted |
| KO-2.2R-013 | KC-002 | Domain 11 Diagnosis Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002, TSR-003 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 11 | Do not treat historical NOT CERTIFIED text as current truth. | SPLIT_REQUIRED | extracted |
| KO-2.2R-014 | KC-002 | Domain 12 Decision Model Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 12 | Do not merge this responsibility into Runtime or Planner. | SPLIT_REQUIRED | extracted |
| KO-2.2R-015 | KC-002 | Domain 13 Policy Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 13 | Do not merge this responsibility into Authority or Runtime. | SPLIT_REQUIRED | extracted |
| KO-2.2R-016 | KC-002 | Domain 14 Planner Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 14 | Do not merge this responsibility into Runtime. | SPLIT_REQUIRED | extracted |
| KO-2.2R-017 | KC-002 | Domain 15 Authority Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 15 | Do not merge this responsibility into Runtime or Verification. | SPLIT_REQUIRED | extracted |
| KO-2.2R-018 | KC-002 | Domain 16 Identity Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 16 | Do not merge this responsibility into Runtime. | SPLIT_REQUIRED | extracted |
| KO-2.2R-019 | KC-002 | Domain 17 Runtime Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 17 | Do not merge this responsibility into Decision, Planner, or Authority. | SPLIT_REQUIRED | extracted |
| KO-2.2R-020 | KC-002 | Domain 18 Execution Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 18 | Do not merge this responsibility into Runtime authority. | SPLIT_REQUIRED | extracted |
| KO-2.2R-021 | KC-002 | Domain 19 Verification Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 19 | Do not merge this responsibility into Authority or Runtime. | SPLIT_REQUIRED | extracted |
| KO-2.2R-022 | KC-002 | Domain 20 Rollback / Closure Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 20 | Do not treat rollback or closure as verification bypass. | SPLIT_REQUIRED | extracted |
| KO-2.2R-023 | KC-002 | Domain 21 Learning Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 21 | Do not treat learning as authority. | SPLIT_REQUIRED | extracted |
| KO-2.2R-024 | KC-002 | Domain 22 Production Maturity Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 22 | Do not treat maturity as direct execution authority. | SPLIT_REQUIRED | extracted |
| KO-2.2R-025 | KC-002 | Domain 23 Current Program State Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 23 | Do not treat volatile state as canonical truth. | SPLIT_REQUIRED | extracted |
| KO-2.2R-026 | KC-002 | Domain 24 OMP Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 24 | Do not turn OMP into Runtime, Planner, or Authority. | SPLIT_REQUIRED | extracted |
| KO-2.2R-027 | KC-002 | Domain 25 Engineering Automation Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 25 | Do not let automation mutate without owner and authority gates. | SPLIT_REQUIRED | extracted |
| KO-2.2R-028 | KC-002 | Domain 26 Continuous Self Evolution Responsibility | Responsibilities | SRC-004, SRC-005, SRC-009 | Architecture Certification / SYSTEM_MAP | TERMINAL | TSR-002 | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-002 -> Q-002 -> Domain 26 | Do not treat self-evolution as self-authorized mutation. | SPLIT_REQUIRED | extracted |
| KO-2.2R-029 | KC-003 | Architecture Closed By Default | Forbidden Actions / Governance | SRC-003, SRC-010, SRC-011 | OMP / Canonical Reference | TERMINAL | TSR-004 | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; OMP | KC-003 -> Q-003 -> TSR-004 | Do not authorize architecture change without proof existing owners cannot express the capability. | ATOMIC | extracted |
| KO-2.2R-030 | KC-004 | Reality First Law | Laws / Verification | SRC-010, SRC-011, SRC-013 | Canonical Reference / OMP | AUTHORITATIVE | Current authoritative law | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; Verification owners | KC-004 -> Q-004 -> Trust/Owner matrices | Do not let implementation evidence override locked architecture outside official change path. | ATOMIC | extracted |
| KO-2.2R-031 | KC-005 | Existing Owner Before New Owner | Owner Rules / Governance | SRC-009, SRC-010, SRC-011 | SYSTEM_MAP / OMP | AUTHORITATIVE | Current authoritative owner law | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; OMP | KC-005 -> Q-005 -> Owner Matrix | Do not create duplicate, hidden, or ownerless responsibility. | ATOMIC | extracted |
| KO-2.2R-032 | KC-006 | Authority Owns Permission And Scope | Authority | SRC-011, SRC-013, SRC-025 | OMP / Authority / Policy | AUTHORITATIVE | Current authority boundary | CANONICAL KNOWLEDGE + KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4; Stage 2.5 | KC-006 -> Q-006 -> Owner Matrix | Do not treat authority ownership as execution or verification ownership. | SPLIT_REQUIRED | extracted |
| KO-2.2R-033 | KC-006 | Authority Must Not Mutate Or Verify Outcomes | Forbidden Actions | SRC-011, SRC-013, SRC-025 | OMP / Authority / Runtime Model | AUTHORITATIVE | Current authority boundary | CANONICAL KNOWLEDGE + KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4; Stage 2.5 | KC-006 -> Q-006 -> Owner Matrix | Do not let Authority observe reality, select arbitrary candidates, mutate routing, or verify outcomes. | SPLIT_REQUIRED | extracted |
| KO-2.2R-034 | KC-007 | Runtime Apply Boundary | Runtime / Boundaries | SRC-013, SRC-016, SRC-032 | Runtime Model | AUTHORITATIVE | Current runtime boundary | CANONICAL KNOWLEDGE + KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4; Stage 2.5 | KC-007 -> Q-007 -> Trust/Owner matrices | Do not let Runtime invent decisions, replace Planner, bypass Authority, bypass Verification, or create truth. | ATOMIC | extracted |
| KO-2.2R-035 | KC-009 | Verification Before Promotion | Verification / Lifecycle | SRC-003, SRC-011, SRC-013 | OMP / Verification owners | TERMINAL | Current verified law | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; OMP | KC-009 -> Q-008 -> Trust/Owner matrices | Do not promote action, autonomy, or capability state without verification evidence. | ATOMIC | extracted |
| KO-2.2R-036 | KC-010 | Rollback Requires Authorized Safe Path | Rollback | SRC-004, SRC-011, SRC-013, SRC-025 | Rollback / OMP / Policy | TERMINAL | Current rollback law | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; Runtime owners | KC-010 -> Q-009 -> Trust/Owner matrices | Do not perform rollback without authority and safety proof. | SPLIT_REQUIRED | extracted |
| KO-2.2R-037 | KC-010 | Closure Requires Terminal Outcome Evidence | Lifecycle | SRC-004, SRC-011, SRC-013, SRC-025 | OMP / Runtime Model | TERMINAL | Current closure law | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; OMP | KC-010 -> Q-009 -> Trust/Owner matrices | Do not treat an action as closed without observed outcome, verification, rollback, safe stop, or escalation evidence. | SPLIT_REQUIRED | extracted |
| KO-2.2R-038 | KC-011 | Domain 11 Diagnosis Certified Terminal State | Terminal State / Certification | SRC-019, SRC-020, SRC-021, SRC-022, SRC-023 | Diagnosis Contract / Recovery | TERMINAL | TSR-003 | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; Future Certification | KC-011 -> Q-010 -> TSR-003 | Do not treat historical Domain 11 NOT CERTIFIED text as current truth or let Diagnosis mutate production. | ATOMIC | extracted |
| KO-2.2R-039 | KC-012 | OMP Permanent Operating Program | Governance / Lifecycle | SRC-011, SRC-009, SRC-010 | OMP | AUTHORITATIVE | Current OMP law | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; OMP | KC-012 -> Q-011 -> Owner Matrix | Do not turn OMP into duplicate Runtime, Planner, Authority, or truth source. | ATOMIC | extracted |
| KO-2.2R-040 | KC-014 | Reports Are Evidence, Not Durable Truth Owners | Evidence Rules | SRC-010, SRC-009, SRC-011 | Canonical Reference / SYSTEM_MAP | AUTHORITATIVE | Current preservation law | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; Knowledge Owner | KC-014 -> Q-012 -> Owner Matrix | Do not make reports canonical owners. | SPLIT_REQUIRED | extracted |
| KO-2.2R-041 | KC-014 | Canonical Owners Preserve Durable Truth | Governance | SRC-010, SRC-009, SRC-011 | Canonical Reference / SYSTEM_MAP | AUTHORITATIVE | Current preservation law | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; Knowledge Owner | KC-014 -> Q-012 -> Owner Matrix | Do not preserve durable truth only in append-only reports. | SPLIT_REQUIRED | extracted |
| KO-2.2R-042 | KC-014 | Durable Findings Must Promote Through Existing Canonical Owners | Evidence Rules / Lifecycle | SRC-010, SRC-009, SRC-011 | Canonical Reference / OMP | AUTHORITATIVE | Current preservation law | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; OMP | KC-014 -> Q-012 -> Owner Matrix | Do not promote knowledge through new owners or bypass acceptance. | SPLIT_REQUIRED | extracted |
| KO-2.2R-043 | KC-015 | No Orphan Artifact Law | Governance | SRC-001, SRC-009, SRC-010, SRC-011 | Stage 2 Program / OMP | TERMINAL | Current Stage 2 law | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; Program Acceptance | KC-015 -> Q-013 -> Stage 2 Program | Do not consume artifacts missing Producer, Consumer, Owner, Acceptance, Terminal State, or Storage Location. | SPLIT_REQUIRED | extracted |
| KO-2.2R-044 | KC-015 | Evidence Requires Verification Before Consumption | Evidence Rules | SRC-001, SRC-009, SRC-010, SRC-011 | Stage 2 Program / OMP | TERMINAL | Current Stage 2 law | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; Program Acceptance | KC-015 -> Q-013 -> Stage 2 Program | Do not treat unverified evidence or generic reports as durable knowledge. | SPLIT_REQUIRED | extracted |
| KO-2.2R-045 | KC-021 | Stage 2 Program State Machine | Lifecycle | SRC-001 | Stage 2 Program | TERMINAL | TSR-005 | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; Program State Owner | KC-021 -> Q-014 -> SRC-001 | Do not create alternate Stage 2 state paths. | SPLIT_REQUIRED | extracted |
| KO-2.2R-046 | KC-021 | Stage Gates Block Stage Skipping | Governance / Lifecycle | SRC-001 | Stage 2 Program | TERMINAL | TSR-005 | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; Program Acceptance | KC-021 -> Q-014 -> SRC-001 | Do not start a later stage before the previous acceptance gate. | SPLIT_REQUIRED | extracted |
| KO-2.2R-047 | KC-022 | Stage 2.1 Outputs Feed Stage 2.2 | Producer-Consumer | SRC-001, SRC-004, SRC-009, SRC-011 | Stage 2 Program / SYSTEM_MAP / OMP | TERMINAL | Current producer/consumer law | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-022 -> Q-015 -> Stage 2 Program | Do not consume inventory outputs before acceptance. | SPLIT_REQUIRED | extracted |
| KO-2.2R-048 | KC-022 | Stage 2.2 Extracted Registry Feeds Stage 2.3 | Producer-Consumer | SRC-001, SRC-004, SRC-009, SRC-011 | Stage 2 Program / SYSTEM_MAP / OMP | TERMINAL | Current producer/consumer law | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-022 -> Q-015 -> Stage 2 Program | Do not deduplicate absent accepted extraction output. | SPLIT_REQUIRED | extracted |
| KO-2.2R-049 | KC-022 | Stage 2.3 Deduplicated Outputs Feed Stage 2.4 | Producer-Consumer | SRC-001, SRC-004, SRC-009, SRC-011 | Stage 2 Program / SYSTEM_MAP / OMP | TERMINAL | Current producer/consumer law | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-022 -> Q-015 -> Stage 2 Program | Do not build graph from non-deduplicated or unaccepted inputs. | SPLIT_REQUIRED | extracted |
| KO-2.2R-050 | KC-022 | Stage 2.4 Knowledge Graph Feeds Stage 2.5 | Producer-Consumer | SRC-001, SRC-004, SRC-009, SRC-011 | Stage 2 Program / SYSTEM_MAP / OMP | TERMINAL | Current producer/consumer law | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-022 -> Q-015 -> Stage 2 Program | Do not canonicalize before graph acceptance. | SPLIT_REQUIRED | extracted |
| KO-2.2R-051 | KC-022 | Stage 2.5 Canonical Knowledge Feeds Stage 2.6 | Producer-Consumer | SRC-001, SRC-004, SRC-009, SRC-011 | Stage 2 Program / SYSTEM_MAP / OMP | TERMINAL | Current producer/consumer law | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-022 -> Q-015 -> Stage 2 Program | Do not accept canonical knowledge before the canonical artifact exists. | SPLIT_REQUIRED | extracted |
| KO-2.2R-052 | KC-022 | Stage 2.6 Acceptance Feeds Stage 2.7 | Producer-Consumer | SRC-001, SRC-004, SRC-009, SRC-011 | Stage 2 Program / SYSTEM_MAP / OMP | TERMINAL | Current producer/consumer law | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-022 -> Q-015 -> Stage 2 Program | Do not lock knowledge without acceptance. | SPLIT_REQUIRED | extracted |
| KO-2.2R-053 | KC-022 | Stage 2.7 Lock Feeds OMP Continuation | Producer-Consumer | SRC-001, SRC-004, SRC-009, SRC-011 | Stage 2 Program / SYSTEM_MAP / OMP | TERMINAL | Current producer/consumer law | KNOWLEDGE GRAPH | Stage 2.3; Stage 2.4 | KC-022 -> Q-015 -> Stage 2 Program | Do not hand control to OMP without locked knowledge baseline. | SPLIT_REQUIRED | extracted |
| KO-2.2R-054 | KC-023 | Stage 2 Must Not Change Locked Architecture | Forbidden Actions / Boundaries | SRC-001, SRC-003 | Stage 2 Program | TERMINAL | Current Stage 2 boundary | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5 | KC-023 -> Q-016 -> Stage 2 Program | Do not change architecture, domains, names, order, or responsibilities. | SPLIT_REQUIRED | extracted |
| KO-2.2R-055 | KC-023 | Stage 2 Must Not Change Owners Or Truth Sources | Forbidden Actions / Boundaries | SRC-001, SRC-003 | Stage 2 Program | TERMINAL | Current Stage 2 boundary | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5 | KC-023 -> Q-016 -> Stage 2 Program | Do not create new owners, roadmaps, or truth sources. | SPLIT_REQUIRED | extracted |
| KO-2.2R-056 | KC-023 | Stage 2 Must Not Change Runtime Planner Authority Or Routing | Forbidden Actions / Boundaries | SRC-001, SRC-003 | Stage 2 Program | TERMINAL | Current Stage 2 boundary | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5 | KC-023 -> Q-016 -> Stage 2 Program | Do not alter Runtime, Planner, Authority, production routing, or user assignments. | SPLIT_REQUIRED | extracted |
| KO-2.2R-057 | KC-023 | Stage 2 Must Not Change OMP | Forbidden Actions / Governance | SRC-001, SRC-003 | Stage 2 Program | TERMINAL | Current Stage 2 boundary | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5 | KC-023 -> Q-016 -> Stage 2 Program | Do not make Stage 2 a replacement OMP or duplicate operating program. | SPLIT_REQUIRED | extracted |
| KO-2.2R-058 | KC-023 | Stage 2.2 Must Not Perform Later Stage Work | Forbidden Actions / Lifecycle | SRC-001, SRC-003 | Stage 2 Program | TERMINAL | Current Stage 2 boundary | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5 | KC-023 -> Q-016 -> Stage 2 Program | Do not deduplicate, graph, canonicalize, accept, or lock during Stage 2.2. | SPLIT_REQUIRED | extracted |
| KO-2.2R-059 | KC-013 | CPS Volatile Current State Boundary | Boundaries / Lifecycle | SRC-012, SRC-011, SRC-009 | Current Program State | AUTHORITATIVE | TSR-007 | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; CPS owner | KC-013 -> Q-017 -> TSR-007 | Do not treat CPS as durable canonical truth. | ATOMIC | extracted |
| KO-2.2R-060 | KC-018 | Product Identity: Governed Routing Platform | Principles / Product | SRC-002, SRC-026, SRC-010 | Product Specification | TERMINAL | Current product identity | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; Product owner | KC-018 -> Q-018 -> Trust/Owner matrices | Do not reduce V7 to VPN protocol mechanics or bypass safety for product goals. | ATOMIC | extracted |
| KO-2.2R-061 | KC-019 | Policy Behavior Must Not Be Invented Ad Hoc | Governance | SRC-025, SRC-011, SRC-024 | Policy Library / OMP | AUTHORITATIVE | TSR-010 | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; Policy owners | KC-019 -> Q-019 -> TSR-010 | Do not create operational policy from opinion or isolated reports. | SPLIT_REQUIRED | extracted |
| KO-2.2R-062 | KC-019 | Policy Becomes Operational Only Through Governed Lifecycle | Implementation Rules / Lifecycle | SRC-025, SRC-011, SRC-024 | Policy Library / OMP | AUTHORITATIVE | TSR-010 | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; OMP | KC-019 -> Q-019 -> TSR-010 | Do not implement policy before research, fit analysis, verification, certification, and OMP integration. | SPLIT_REQUIRED | extracted |
| KO-2.2R-063 | KC-020 | ADRs Preserve Durable Architecture Decisions | Governance / Evidence Rules | SRC-024, SRC-010, SRC-009 | ADR Owner / Canonical Reference | AUTHORITATIVE | TSR-009 | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; ADR Owner | KC-020 -> Q-020 -> TSR-009 | Do not leave durable architecture decisions only in chats or reports. | SPLIT_REQUIRED | extracted |
| KO-2.2R-064 | KC-020 | Changed Decisions Require ADR Update Or New ADR | Governance / Evidence Rules | SRC-024, SRC-010, SRC-009 | ADR Owner / Canonical Reference | AUTHORITATIVE | TSR-009 | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; ADR Owner | KC-020 -> Q-020 -> TSR-009 | Do not change decision meaning without updating the decision record. | SPLIT_REQUIRED | extracted |
| KO-2.2R-065 | KC-020 | Superseded ADR History Must Not Become Current Truth | Governance / Evidence Rules | SRC-024, SRC-010, SRC-009 | ADR Owner / Canonical Reference | AUTHORITATIVE | TSR-009 | CANONICAL KNOWLEDGE | Stage 2.3; Stage 2.5; Canonical Reference | KC-020 -> Q-020 -> TSR-009 | Do not promote superseded decision history as active truth. | SPLIT_REQUIRED | extracted |

## 7. Manual Review Candidates

| Candidate | Atomicity Review | Registry admission | Reason |
|---|---|---|---|
| KC-016 Function Graph Implementation Reality | MANUAL_REVIEW | NO | SRC-008 is derived evidence and TSR-006 records sync debt after final Domain 11 recovery. Current truth cannot be deterministically extracted without bounded review. |
| KC-017 Research-Derived System Laws | MANUAL_REVIEW | NO | Research-derived laws require owner and object-boundary review before extraction into active objects. |
| KC-025 Old Stage 2 Corpus Validation Label | MANUAL_REVIEW | NO | Historical Stage 2 label is superseded by the approved Knowledge Engineering route and needs bounded review to avoid active-route confusion. |

## 8. No Object Created

| Candidate | Atomicity Review | Disposition | Reason |
|---|---|---|---|
| KC-024 Historical Stage 1 Evidence | ATOMIC | NO_OBJECT_CREATED | Historical evidence is preserved as source/provenance. Stage 2.2 does not create an active reusable Knowledge Object from this historical family. |

## 9. Verification Results

All 65 created Knowledge Objects passed verification before entering the Extracted Knowledge Registry.

Verification checks:

- Schema;
- Source;
- Trust Level;
- Terminal State;
- Owner;
- Consumer;
- Provenance;
- Destination;
- Forbidden Misuse;
- Review State;
- Atomicity.

Verification summary:

| Verification item | Result |
|---|---|
| Schema | PASS |
| Source | PASS |
| Trust Level | PASS |
| Terminal State | PASS |
| Owner | PASS |
| Consumer | PASS |
| Provenance | PASS |
| Destination | PASS |
| Forbidden Misuse | PASS |
| Review State | PASS |
| Atomicity | PASS |
| Registry admission | PASS |

## 10. Comparison With Previous Stage 2.2 Execution

Previous report used for historical comparison only:

```text
docs/reports/research/V7_STAGE2_2_KNOWLEDGE_EXTRACTION.md
```

| Metric | Previous Stage 2.2 | Rerun Stage 2.2 | Change |
|---|---:|---:|---:|
| Queue candidates processed | 24 | 24 | 0 |
| Created Knowledge Objects | 20 | 65 | +45 |
| ONE_OBJECT_CREATED candidates | 20 | 10 | -10 |
| MULTIPLE_OBJECTS_CREATED candidates | 0 | 10 | +10 |
| MANUAL_REVIEW candidates | 3 | 3 | 0 |
| NO_OBJECT_CREATED candidates | 1 | 1 | 0 |
| Rejected candidates | 0 | 0 | 0 |
| Deduplication performed | 0 | 0 | 0 |
| Graph created | 0 | 0 | 0 |
| Canonical Knowledge created | 0 | 0 | 0 |

Objects changed:

```text
OBJECT_COUNT_DELTA = +45
NEW_MULTIPLE_OBJECTS_CREATED = 10
SPLIT_CANDIDATES = 10
```

Reason for difference:

The rerun applies the new Atomicity Test and Object Splitting Rule. Candidates that previously produced broad objects now produce separate atomic Knowledge Objects when their internal assertions have different responsibility, category, owner, consumer, terminal state, destination, forbidden misuse, or provenance chain.

## 11. Extraction Statistics

| Metric | Value |
|---|---:|
| Total queue candidates processed | 24 |
| Created Knowledge Objects | 65 |
| P0 queue candidates processed | 17 |
| P0 Knowledge Objects created | 59 |
| P1 queue candidates processed | 6 |
| P1 Knowledge Objects created | 6 |
| P1 Manual Review dispositions | 3 |
| P2 queue candidates processed | 1 |
| Manual Review Count | 3 |
| Rejected Candidate Count | 0 |
| No Object Created Count | 1 |
| MULTIPLE_OBJECTS_CREATED Count | 10 |
| Extraction Coverage | 100% of approved Knowledge Extraction Queue |
| Deduplication Performed | 0 |
| Graph Nodes Created | 0 |
| Graph Edges Created | 0 |
| Canonical Knowledge Created | 0 |

## 12. P0 Status

| P0 status item | Result |
|---|---|
| All P0 queue candidates processed | PASS |
| All P0 queue candidates have Atomicity Review | PASS |
| All P0 queue candidates have terminal disposition | PASS |
| All created P0 Knowledge Objects verified | PASS |
| P0 rejected candidates | 0 |
| P0 manual review candidates in approved queue | 0 |

Inherited input note:

`KC-008 Decision Before Execution` remains present in the Stage 2.1 Candidate Registry but absent from the approved Knowledge Extraction Queue. This rerun did not add it because Stage 2.2 is constrained to the approved queue.

## 13. P1 Status

| Candidate | Result |
|---|---|
| KC-013 | ONE_OBJECT_CREATED |
| KC-019 | MULTIPLE_OBJECTS_CREATED |
| KC-020 | MULTIPLE_OBJECTS_CREATED |
| KC-016 | MANUAL_REVIEW |
| KC-017 | MANUAL_REVIEW |
| KC-025 | MANUAL_REVIEW |

P1 completion rule result:

```text
PASS
```

## 14. Risks

| Risk | Severity | Blocking | Resolution |
|---|---|---:|---|
| KC-008 exists in Candidate Registry but not in approved Extraction Queue | Minor | No | Rerun processed only the approved queue. Future acceptance may decide whether inherited queue omission needs bounded correction. |
| Function Graph Appendix sync debt | Minor | No | KC-016 remains `MANUAL_REVIEW`; no object admitted from derived sync-debt evidence. |
| Research-derived laws need owner/object-boundary review | Minor | No | KC-017 remains `MANUAL_REVIEW`. |
| Old Stage 2 label can confuse active route | Minor | No | KC-025 remains `MANUAL_REVIEW`; active route remains approved Knowledge Engineering route. |
| More atomic objects increase Stage 2.3 workload | Minor | No | This is expected; Stage 2.3 owns deduplication and canonical concept formation. |

## 15. Stage Completion Criteria

| Completion Criterion | Result |
|---|---|
| Extraction consumed the approved Stage 2.1 Knowledge Extraction Queue | PASS |
| Every P0 extraction candidate is extracted or rejected with evidence-backed reason | PASS |
| Every P1 extraction candidate is extracted, deferred, or marked `MANUAL_REVIEW` | PASS |
| Every processed candidate has deterministic disposition | PASS |
| Every processed candidate has Atomicity Review result | PASS |
| Every created Knowledge Object passed Knowledge Object Verification before registry admission | PASS |
| Every extracted Knowledge Object has source, owner, trust level, terminal state, provenance, destination, consumers, and forbidden misuse | PASS |
| Every extracted Knowledge Object satisfies the Atomicity Test | PASS |
| Every logical field used by extraction has a unique Resolution Path or direct stored value | PASS |
| Extracted objects preserve terminal truth and superseded history separation | PASS |
| Extraction did not deduplicate concepts beyond exact duplicate source references | PASS |
| Stage 2.2 used the official Extraction Lifecycle and did not create an alternate extraction mechanism | PASS |
| Extracted Knowledge Registry exists in this report | PASS |
| `docs/reports/research/V7_STAGE2_2_KNOWLEDGE_EXTRACTION_RERUN.md` exists | PASS |
| Architecture Review is PASS | PASS |
| Quality Review is PASS | PASS |
| Self Review is PASS | PASS |
| Acceptance gate is `STAGE_2_2_EXTRACTION_PASS` | PASS |

## 16. Review Results

Architecture Review:

```text
PASS
```

The rerun did not change architecture, owners, Runtime, Planner, Authority, OMP, production routing, Stage 2 route, or Stage boundaries.

Quality Review:

```text
PASS
```

All queue candidates were reprocessed from fixed Stage 2.1 inputs, and every candidate has Atomicity Review, terminal disposition, and verification result.

Self Review:

```text
PASS
```

The rerun did only Stage 2.2 Knowledge Extraction. It did not perform Stage 2.3 Deduplication, Stage 2.4 Graph, Stage 2.5 Canonical Knowledge, Stage 2.6 Acceptance, or Stage 2.7 Lock.

Extraction Review:

```text
PASS
```

The official lifecycle was applied, including Atomicity Review before Knowledge Object creation.

Knowledge Object Review:

```text
PASS
```

All 65 created objects satisfy the Knowledge Object Model and are atomic extracted units, not canonical concepts or graph nodes.

Atomicity Review:

```text
PASS
```

Ten candidates were deterministically split into multiple objects. No candidate was artificially kept as one object when Object Splitting Rule applied.

Consistency Review:

```text
PASS
```

No duplicate lifecycle, alternate schema, alternate acceptance gate, Deduplication, Graph construction, Canonical Knowledge creation, or new entity was introduced.

## 17. Stage Verdict

```text
STAGE_2_2_EXTRACTION_PASS
STAGE_2_2_RERUN_COMPLETED
STAGE_2_3_READY
STAGE_2_3_IN_PROGRESS = FALSE
```
