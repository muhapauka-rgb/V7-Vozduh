# V7 Stage 2 Knowledge Engineering Program

Status: `CLOSED_LOCKED_KNOWLEDGE`
Program: `V7.STAGE2.KNOWLEDGE_ENGINEERING`
Created: 2026-07-07
Owner: Canonical Reference / SYSTEM_MAP / OMP / Knowledge Plane
Input baseline: `STAGE_1_ACCEPTED`, `STAGE_1_LOCKED`
Target terminal state: `LOCKED_KNOWLEDGE`
Terminal state: `LOCKED_KNOWLEDGE`
Closed by: `docs/reports/research/V7_STAGE2_7_KNOWLEDGE_LOCK.md`

This document is the governing program for V7 Stage 2.

Stage 2 converts the locked Stage 1 Architecture into permanent engineering memory for the project.

It does not redesign architecture.
It does not re-run Stage 1.
It does not create new architecture domains.
It does not create a new OMP, Runtime, Planner, Authority, owner, roadmap, or truth source.

Stage 2 extracts engineering knowledge, not documents.

The final Stage 2 result is:

```text
LOCKED KNOWLEDGE
```

`LOCKED KNOWLEDGE` becomes the second foundation of V7 alongside:

```text
LOCKED ARCHITECTURE
```

## 1. Program Purpose

Stage 1 proved and locked the architecture baseline.
Stage 2 preserves the reusable engineering knowledge contained in that baseline so future engineers, Codex sessions, OMP executions, audits, and capability work can consume the knowledge without rediscovering it from reports.

The Stage 2 product is permanent engineering memory:

```text
Stage 1 Architecture Evidence
  -> Knowledge Inventory
  -> Knowledge Extraction
  -> Knowledge Deduplication
  -> Knowledge Graph
  -> Canonical Architecture Knowledge
  -> Knowledge Acceptance
  -> Knowledge Lock
```

Every accepted knowledge object must have:

| Required field | Meaning |
| --- | --- |
| Source | Where the knowledge came from. |
| Owner | Canonical owner or existing owner responsible for the knowledge. |
| Trust Level | Current trust state of the knowledge. |
| Terminal State | Current truth after superseded history is resolved. |
| Provenance | Evidence chain that explains how the knowledge reached terminal state. |
| Destination | Where the knowledge will be used after Stage 2. |

## 2. Stage 2 Boundaries

Stage 2 is a knowledge engineering program.

It must not change:

- Stage 1 locked architecture;
- the 26-domain architecture tree;
- domain names, order, or responsibilities;
- OMP behavior;
- Runtime behavior;
- Planner behavior;
- Authority permissions;
- production routing;
- user assignments;
- implementation owners;
- certification outcomes;
- trust, confidence, production maturity, or authority scores.

Stage 2 creates only these artifact classes:

- knowledge inventory reports;
- knowledge candidate registries;
- extraction queues;
- deduplication maps;
- knowledge graph artifacts;
- `docs/reference/V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md`;
- acceptance and lock reports.

Canonical reference updates follow Program Closure synchronization only after a Stage 2 acceptance gate proves the update preserves locked knowledge and does not change architecture.

## Program Invariants

These invariants are absolute program laws.
They remain true in every Stage 2 state and every Stage 2 stage.

- `LOCKED_ARCHITECTURE` is never changed.
- Existing Owner Law is always followed.
- Reality First is always followed.
- OMP remains the only execution program after Stage 2.
- History never becomes Current Truth.
- Every Knowledge Object has Source.
- Every Knowledge Object has Provenance.
- Every Knowledge Object has Canonical Owner.
- Every Knowledge Object has Consumer or a documented no-consumer reason.
- No Knowledge exists without Classification.
- No Source exists without Trust Level.
- No Knowledge exists without Terminal State.
- Stage 2 never changes architecture.

## 3. Program Input / Output Contract

Stage 2 begins from the locked Stage 1 baseline.

Program Inputs:

| Input | Role |
| --- | --- |
| `LOCKED_ARCHITECTURE` | Non-mutable architecture foundation. |
| Stage 1 Corpus | Complete certification corpus and terminal domain states. |
| Canonical Owners | Canonical Reference, SYSTEM_MAP, OMP, Current Program State, Runtime Model, Decision Model, policies, ADRs, and implementation owners. |
| OMP | Execution owner for program continuation and post-Stage-2 handoff. |
| `docs/reference/V7_MASTER_PROJECT_HANDOFF.md` | Canonical entry point and Stage 2 continuation pointer. |
| `docs/reports/research/V7_STAGE1_FINAL_ACCEPTANCE.md` | Stage 1 terminal acceptance and lock evidence. |
| `docs/reports/research/V7_STAGE1_CORPUS_AUDIT.md` | Stage 1 corpus-level integrity evidence. |
| `docs/reports/research/V7_PHASE1_DOMAIN_CERTIFICATION.md` | Domain certification corpus. |
| `docs/reports/research/V7_PHASE1_ARCHITECT_SUMMARY.md` | Architecture summary and domain structure. |
| `docs/reports/research/V7_AUTONOMOUS_MODEL_KNOWLEDGE_CONSOLIDATION.md` | Architecture tree and freeze evidence. |
| `docs/reference/SYSTEM_MAP.md` | Owner and topology lookup. |
| `docs/reference/V7_CANONICAL_REFERENCE.md` | Durable current project truth. |
| `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` | Permanent operating program and continuation rules. |
| `docs/programs/V7_CURRENT_PROGRAM_STATE.md` | Volatile current state and stop/next-action surface. |

Program Outputs:

| Output | Consumer |
| --- | --- |
| `LOCKED_KNOWLEDGE` | OMP, Canonical Reference, SYSTEM_MAP, Current Program State, future engineering work. |
| `docs/reference/V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md` | Discovery, Architecture Review, OMP, implementation, certification, engineering automation, future architecture evolution. |
| Stage 2 Knowledge Graph | Canonical Architecture Knowledge, Knowledge Acceptance, future knowledge evolution. |
| Knowledge Baseline | OMP and Current Program State. |
| Updated Current Program State | OMP and future Codex sessions. |
| OMP Continuation | Post-Stage-2 production and engineering execution. |

Stage 2.1 must expand beyond this initial set and discover all relevant project knowledge sources.

## 4. Official Stage 2 Roadmap

The official Stage 2 roadmap is:

```text
Stage 2.1 Knowledge Inventory
  -> Stage 2.2 Knowledge Extraction
  -> Stage 2.3 Knowledge Deduplication
  -> Stage 2.4 Knowledge Graph
  -> Stage 2.5 V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md
  -> Stage 2.6 Knowledge Acceptance
  -> Stage 2.7 Knowledge Lock
```

No Stage 2 step can skip the previous acceptance gate.

## Stage 2 Program State Machine

The official Stage 2 program lifecycle is:

```text
NOT_STARTED
  -> INVENTORY
  -> EXTRACTION
  -> DEDUPLICATION
  -> GRAPH
  -> CANONICALIZATION
  -> ACCEPTANCE
  -> LOCKED
```

State definitions:

| State | Meaning |
| --- | --- |
| `NOT_STARTED` | Stage 2 program exists, but Stage 2.1 has not begun. |
| `INVENTORY` | Stage 2.1 is discovering and classifying sources and knowledge candidates. |
| `EXTRACTION` | Stage 2.2 is extracting knowledge objects from the approved candidate queue. |
| `DEDUPLICATION` | Stage 2.3 is merging duplicate concepts while preserving provenance. |
| `GRAPH` | Stage 2.4 is materializing nodes and edges from accepted knowledge objects. |
| `CANONICALIZATION` | Stage 2.5 is producing `V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md`. |
| `ACCEPTANCE` | Stage 2.6 is independently verifying the knowledge baseline. |
| `LOCKED` | Stage 2.7 has locked the accepted knowledge baseline as `LOCKED_KNOWLEDGE`. |

Program Start Model:

```text
Program Approved
  -> Program Activated
  -> Current Program State records STAGE_2_ACTIVE
  -> OMP records Stage 2 as active knowledge program
  -> Stage 2.1 READY
  -> Stage 2.1 IN_PROGRESS
```

Program start rules:

- Program start is driven by Program State, Current Program State, and OMP.
- Subjective operator preference is not a program-start mechanism.
- Stage 2.1 enters `READY` only after Program Activation is recorded.
- Stage 2.1 enters `IN_PROGRESS` only after the Program Inputs table is available to the inventory executor.

Stage Transition Law:

Every official Stage 2 stage has this lifecycle:

```text
NOT_STARTED
  -> READY
  -> IN_PROGRESS
  -> READY_FOR_REVIEW
  -> READY_FOR_ACCEPTANCE
  -> PASS | PASS_WITH_MINOR_RISKS | HOLD | FAIL | BLOCKED
```

Stage state meanings:

| Stage state | Meaning |
| --- | --- |
| `NOT_STARTED` | Stage exists in the program but has no accepted input yet. |
| `READY` | Previous stage output is accepted and available as input. |
| `IN_PROGRESS` | Stage execution is active. |
| `READY_FOR_REVIEW` | Stage outputs exist and await Architecture Review, Quality Review, and Self Review. |
| `READY_FOR_ACCEPTANCE` | Stage execution, automatic reviews, and engineering report are complete; the stage is stopped and awaits independent Acceptance. |
| `PASS` | Stage completed and can feed the next stage. |
| `PASS_WITH_MINOR_RISKS` | Stage completed with accepted non-blocking risks and can feed the next stage. |
| `HOLD` | Stage cannot continue until bounded review or missing evidence is resolved. |
| `FAIL` | Stage output is rejected and requires recovery. |
| `BLOCKED` | Stage cannot start or continue because required input, authority, evidence, or owner resolution is missing. |

Stage transition rules:

- `PASS` from the previous stage automatically becomes eligible input to the next stage and may set the next stage to `READY`.
- `PASS_WITH_MINOR_RISKS` from the previous stage automatically becomes eligible input to the next stage with the accepted risk record attached and may set the next stage to `READY`.
- The next stage cannot begin without an accepted result from the previous stage and a separate operator command.
- `READY` means eligible to start, not authorized to enter `IN_PROGRESS`.
- Each stage uses only the approved output artifacts of the previous stage.
- Stage skipping is forbidden.
- Cross-stage execution is forbidden.
- A later stage cannot repair an earlier stage by reinterpretation; the earlier stage must be recovered and revalidated.

Stage Execution Closure Law:

After any Stage 2 stage finishes its internal execution, the executor must automatically complete this closure sequence:

```text
Stage Execution
  -> Architecture Review
  -> Quality Review
  -> Self Review
  -> Engineering Report
  -> Stage State = READY_FOR_ACCEPTANCE
  -> STOP
```

Stage execution closure rules:

- Automatic reviews are part of stage execution closure.
- The Engineering Report is part of stage execution closure.
- The stage is not final after automatic reviews; it is only `READY_FOR_ACCEPTANCE`.
- The executor must stop after the Engineering Report is created.
- The executor must not start independent Acceptance as part of automatic stage execution unless the operator separately commands Acceptance.
- The executor must not start the next stage after `READY_FOR_ACCEPTANCE`.
- `READY_FOR_ACCEPTANCE` does not authorize downstream consumption.

Next Stage Law:

- A next stage never starts automatically.
- `PASS`, `PASS_WITH_MINOR_RISKS`, or `READY` never authorizes automatic transition to `IN_PROGRESS`.
- The next stage may enter `READY` after the previous stage is accepted.
- The next stage enters `IN_PROGRESS` only after a separate operator command.
- Any automatic start of a next stage is a Stage Transition Law violation.

Acceptance Gate Law:

- Acceptance is not part of automatic Stage Execution.
- Acceptance is performed separately by the Program Acceptance Owner or an explicitly commanded independent acceptance action.
- A stage receives its final accepted state only after Acceptance completes.
- Automatic reviews and Engineering Report can make a stage `READY_FOR_ACCEPTANCE`; they cannot make it `PASS`, `PASS_WITH_MINOR_RISKS`, `HOLD`, or `FAIL` without Acceptance.
- Acceptance does not execute next-stage work.

Program Execution Model:

The official execution cycle for every Stage 2 stage is:

```text
Stage
  -> Execution
  -> Automatic Reviews
  -> Automatic Engineering Report
  -> READY_FOR_ACCEPTANCE
  -> STOP
  -> Independent Acceptance
  -> PASS | PASS_WITH_MINOR_RISKS | HOLD | FAIL | BLOCKED
  -> READY
  -> Operator Command
  -> Next Stage
```

This model clarifies execution timing only. It does not change Stage 2 architecture, route, stage boundaries, roles, or acceptance gates.

Allowed transitions:

| From | To | Required gate |
| --- | --- | --- |
| `NOT_STARTED` | `INVENTORY` | Current Program State records `STAGE_2_ACTIVE`; OMP activates Stage 2; Stage 2.1 enters `READY` then `IN_PROGRESS`. |
| `INVENTORY` | `EXTRACTION` | `STAGE_2_1_PASS` or `STAGE_2_1_PASS_WITH_MINOR_RISKS`. |
| `EXTRACTION` | `DEDUPLICATION` | `STAGE_2_2_EXTRACTION_PASS`. |
| `DEDUPLICATION` | `GRAPH` | `STAGE_2_3_DEDUPLICATION_PASS`. |
| `GRAPH` | `CANONICALIZATION` | `STAGE_2_4_GRAPH_PASS`. |
| `CANONICALIZATION` | `ACCEPTANCE` | `STAGE_2_5_CANONICAL_KNOWLEDGE_READY`. |
| `ACCEPTANCE` | `LOCKED` | `STAGE_2_KNOWLEDGE_ACCEPTED` or `STAGE_2_KNOWLEDGE_ACCEPTED_WITH_MINOR_RISKS`. |

Forbidden transitions:

- `NOT_STARTED` -> `EXTRACTION`;
- `INVENTORY` -> `DEDUPLICATION`;
- `INVENTORY` -> `GRAPH`;
- `EXTRACTION` -> `CANONICALIZATION`;
- `DEDUPLICATION` -> `ACCEPTANCE`;
- `GRAPH` -> `LOCKED`;
- `CANONICALIZATION` -> `LOCKED`;
- any transition that bypasses a required acceptance gate;
- any transition that re-runs Stage 1 or changes Stage 1 architecture;
- any transition that creates a new Runtime, Planner, Authority, OMP, architecture domain, owner, roadmap, or truth source.

Terminal program state:

```text
LOCKED
```

Terminal program result:

```text
LOCKED_KNOWLEDGE
```

## Stage Deliverables

| Stage | Primary deliverable |
| --- | --- |
| Stage 2.1 Knowledge Inventory | Knowledge Inventory Report. |
| Stage 2.2 Knowledge Extraction | Extracted Knowledge Registry. |
| Stage 2.3 Knowledge Deduplication | Deduplicated Knowledge Registry. |
| Stage 2.4 Knowledge Graph | Knowledge Graph. |
| Stage 2.5 Canonical Architecture Knowledge | `docs/reference/V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md`. |
| Stage 2.6 Knowledge Acceptance | Knowledge Acceptance Report. |
| Stage 2.7 Knowledge Lock | Knowledge Lock Report. |

## Stage Input / Output Contracts

| Stage | Inputs | Outputs | Acceptance Output |
| --- | --- | --- | --- |
| Stage 2.1 Knowledge Inventory | Locked Stage 1 baseline; canonical entry point; canonical owners; repository discovery surfaces. | Source Registry; Classification Matrix; Trust Matrix; Owner Matrix; Knowledge Candidate Registry; Terminal State Resolution; Knowledge Extraction Queue; Inventory Report. | `STAGE_2_1_PASS` or `STAGE_2_1_PASS_WITH_MINOR_RISKS`. |
| Stage 2.2 Knowledge Extraction | Knowledge Candidate Registry; Knowledge Extraction Queue; Stage 2.1 Validation PASS or PASS_WITH_MINOR_RISKS. | Extracted Knowledge Registry; `docs/reports/research/V7_STAGE2_2_KNOWLEDGE_EXTRACTION.md`. | `STAGE_2_2_EXTRACTION_PASS`. |
| Stage 2.3 Knowledge Deduplication | Extracted Knowledge Registry; Stage 2.2 Extraction PASS. | Deduplicated Knowledge Registry; Knowledge Merge Map; Superseded Knowledge Map; `docs/reports/research/V7_STAGE2_3_KNOWLEDGE_DEDUPLICATION.md`. | `STAGE_2_3_DEDUPLICATION_PASS`. |
| Stage 2.4 Knowledge Graph | Deduplicated Knowledge Registry; Knowledge Merge Map; Superseded Knowledge Map; Stage 2.3 Deduplication PASS. | Stage 2 Knowledge Graph; `docs/reports/research/V7_STAGE2_4_KNOWLEDGE_GRAPH.md`. | `STAGE_2_4_GRAPH_PASS`. |
| Stage 2.5 Canonical Architecture Knowledge | Stage 2 Knowledge Graph; Deduplicated Knowledge Registry; Knowledge Graph PASS. | `docs/reference/V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md`; Stage 2.5 Canonical Knowledge Report. | `STAGE_2_5_CANONICAL_KNOWLEDGE_READY`. |
| Stage 2.6 Knowledge Acceptance | `V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md`; Knowledge Graph; Stage 2.5 Canonical Knowledge Ready output. | `docs/reports/research/V7_STAGE2_6_KNOWLEDGE_ACCEPTANCE.md`. | `STAGE_2_KNOWLEDGE_ACCEPTED` or `STAGE_2_KNOWLEDGE_ACCEPTED_WITH_MINOR_RISKS`. |
| Stage 2.7 Knowledge Lock | Accepted Knowledge Baseline; Knowledge Acceptance Report; Stage 2 Knowledge Acceptance verdict. | `docs/reports/research/V7_STAGE2_7_KNOWLEDGE_LOCK.md`; canonical synchronization results; Current Program State update; OMP Knowledge Baseline handoff. | `STAGE_2_KNOWLEDGE_LOCKED`. |

## Program Governance

Program governance assigns exactly one responsibility set to each program role.

| Role | Responsibilities | Produces | Consumes | Authority | Outputs |
| --- | --- | --- | --- | --- | --- |
| Program Owner | Own the Stage 2 governing program and preserve Stage 2 boundaries. | Program acceptance state; program update decisions. | Locked Architecture; OMP; Current Program State; Canonical Reference; SYSTEM_MAP. | Engineering governance only; no Runtime, Planner, Authority, routing, or user-movement authority. | `STAGE_2_PROGRAM_ACCEPTED`; program governance decisions. |
| Program Executor | Execute Stage 2 stages through the official lifecycle. | Stage outputs, reports, registries, graph, canonical knowledge draft. | Program Inputs; previous-stage accepted outputs. | Stage execution authority inside this program only. | Stage deliverables and stage reports. |
| Program State Owner | Record active state, transitions, blockers, closure, and OMP handoff. | Program state records; Current Program State updates. | Stage verdicts; closure outputs; Knowledge Baseline. | Volatile state recording only; no canonical truth or Runtime authority. | `STAGE_2_ACTIVE`; `PROGRAM_STATE = CLOSED`; Current Program State update. |
| Program Acceptance Owner | Verify program acceptance and stage acceptance gates. | Acceptance verdicts. | Stage outputs; reviews; validation evidence. | Acceptance authority for Stage 2 artifacts only. | Stage acceptance outputs; `STAGE_2_PROGRAM_ACCEPTED`. |
| Knowledge Owner | Preserve locked knowledge and future knowledge evolution. | `LOCKED_KNOWLEDGE`; `LOCKED_KNOWLEDGE_VNEXT`. | Accepted canonical knowledge; evidence; provenance; Knowledge Evolution requests. | Knowledge memory authority only; no architecture redesign authority. | Knowledge Baseline; canonical knowledge updates. |
| Knowledge Consumer | Use locked knowledge after Stage 2. | Consumption evidence; reuse decisions; evolution requests. | `V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md`; Knowledge Graph; Knowledge Baseline. | Consumption authority only; no extraction authority when locked knowledge already contains the answer. | Discovery, Architecture Review, OMP, implementation, certification, engineering automation, and evolution inputs. |
| Program Closure Owner | Close Stage 2 and hand control to OMP. | Closure outputs. | `STAGE_2_KNOWLEDGE_LOCKED`; synchronization checks; Knowledge Baseline. | Closure authority only; no program redesign authority. | `CANONICAL_SYNCHRONIZATION_COMPLETE`; `ACTIVE_PROGRAM = OMP`; `PROGRAM_STATE = CLOSED`. |

No Stage 2 responsibility remains ownerless.
No program role creates a second Runtime, Planner, Authority, OMP, architecture domain, roadmap, or truth source.

Role Separation Law:

- Program Executor creates artifacts.
- Program Acceptance Owner accepts artifacts.
- Program Executor cannot accept its own output.
- Knowledge Owner preserves and updates locked knowledge only after acceptance.
- Knowledge Owner cannot independently confirm a `LOCKED_KNOWLEDGE` change.
- Program Closure Owner closes the program only after `STAGE_2_KNOWLEDGE_LOCKED`.
- No role can produce and accept the same artifact.

## Program Producer / Consumer Model

Every Stage 2 artifact has a producer, consumer, owner, acceptance result, terminal state, and storage location.

Storage Location Completeness:

- Storage Location must be a full repository path or a named canonical owner.
- Generic values such as `Stage 2 Report`, `Extraction Report`, or `Graph Report` are invalid.
- Invalid storage location creates `INCOMPLETE_ARTIFACT`.

| Artifact | Producer | Consumer | Owner | Acceptance | Terminal state | Storage location |
| --- | --- | --- | --- | --- | --- | --- |
| Program Inputs | Program Owner / Program State Owner | Stage 2.1 Knowledge Inventory | OMP / Current Program State | `STAGE_2_PROGRAM_ACCEPTED` | `READY_FOR_STAGE_2_1` | `docs/programs/V7_STAGE2_KNOWLEDGE_ENGINEERING_PROGRAM.md` |
| Source Registry | Stage 2.1 Knowledge Inventory | Stage 2.2 Knowledge Extraction | Program Executor | `STAGE_2_1_PASS` or `STAGE_2_1_PASS_WITH_MINOR_RISKS` | `INVENTORY_ACCEPTED` | `docs/reports/research/V7_STAGE2_1_KNOWLEDGE_INVENTORY.md` |
| Classification Matrix | Stage 2.1 Knowledge Inventory | Stage 2.2 Knowledge Extraction | Program Executor | `STAGE_2_1_PASS` or `STAGE_2_1_PASS_WITH_MINOR_RISKS` | `INVENTORY_ACCEPTED` | `docs/reports/research/V7_STAGE2_1_KNOWLEDGE_INVENTORY.md` |
| Knowledge Candidate Registry | Stage 2.1 Knowledge Inventory | Stage 2.2 Knowledge Extraction | Program Executor | `STAGE_2_1_PASS` or `STAGE_2_1_PASS_WITH_MINOR_RISKS` | `INVENTORY_ACCEPTED` | `docs/reports/research/V7_STAGE2_1_KNOWLEDGE_INVENTORY.md` |
| Knowledge Extraction Queue | Stage 2.1 Knowledge Inventory | Stage 2.2 Knowledge Extraction | Program Executor | `STAGE_2_1_PASS` or `STAGE_2_1_PASS_WITH_MINOR_RISKS` | `READY_FOR_EXTRACTION` | `docs/reports/research/V7_STAGE2_1_KNOWLEDGE_INVENTORY.md` |
| Extracted Knowledge Registry | Stage 2.2 Knowledge Extraction | Stage 2.3 Knowledge Deduplication | Program Executor | `STAGE_2_2_EXTRACTION_PASS` | `EXTRACTION_ACCEPTED` | `docs/reports/research/V7_STAGE2_2_KNOWLEDGE_EXTRACTION.md` |
| Deduplicated Knowledge Registry | Stage 2.3 Knowledge Deduplication | Stage 2.4 Knowledge Graph | Program Executor | `STAGE_2_3_DEDUPLICATION_PASS` | `DEDUPLICATION_ACCEPTED` | `docs/reports/research/V7_STAGE2_3_KNOWLEDGE_DEDUPLICATION.md` |
| Knowledge Merge Map | Stage 2.3 Knowledge Deduplication | Stage 2.4 Knowledge Graph | Program Executor | `STAGE_2_3_DEDUPLICATION_PASS` | `DEDUPLICATION_ACCEPTED` | `docs/reports/research/V7_STAGE2_3_KNOWLEDGE_DEDUPLICATION.md` |
| Stage 2 Knowledge Graph | Stage 2.4 Knowledge Graph | Stage 2.5 Canonical Architecture Knowledge | Program Executor / Knowledge Owner | `STAGE_2_4_GRAPH_PASS` | `GRAPH_ACCEPTED` | `docs/reports/research/V7_STAGE2_4_KNOWLEDGE_GRAPH.md` |
| `V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md` | Stage 2.5 Canonical Architecture Knowledge | Stage 2.6 Knowledge Acceptance; post-lock Knowledge Consumers | Knowledge Owner | `STAGE_2_KNOWLEDGE_ACCEPTED_WITH_MINOR_RISKS` | `LOCKED_KNOWLEDGE` | `docs/reference/V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md` |
| Knowledge Acceptance Report | Stage 2.6 Knowledge Acceptance | Stage 2.7 Knowledge Lock | Program Acceptance Owner | `STAGE_2_KNOWLEDGE_ACCEPTED` or `STAGE_2_KNOWLEDGE_ACCEPTED_WITH_MINOR_RISKS` | `KNOWLEDGE_ACCEPTED` | `docs/reports/research/V7_STAGE2_6_KNOWLEDGE_ACCEPTANCE.md` |
| Knowledge Lock Report | Stage 2.7 Knowledge Lock | Program Closure | Program Closure Owner | `STAGE_2_KNOWLEDGE_LOCKED` | `LOCKED_KNOWLEDGE` | `docs/reports/research/V7_STAGE2_7_KNOWLEDGE_LOCK.md` |
| Knowledge Baseline | Stage 2.7 Knowledge Lock | OMP; Current Program State; Knowledge Consumers | Knowledge Owner | `STAGE_2_KNOWLEDGE_LOCKED` | `LOCKED_KNOWLEDGE` | `docs/reference/V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md`; `docs/reports/research/V7_STAGE2_4_KNOWLEDGE_GRAPH.md`; `docs/reports/research/V7_STAGE2_7_KNOWLEDGE_LOCK.md` |
| OMP Continuation | Program Closure | OMP | OMP | `PROGRAM_STATE = CLOSED` | `ACTIVE_PROGRAM = OMP` | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`; `docs/programs/V7_CURRENT_PROGRAM_STATE.md` |

Producer / Consumer chain:

```text
Program
  -> produces Program Inputs
  -> consumed by Knowledge Inventory
  -> produces Source Registry / Candidate Registry / Extraction Queue
  -> consumed by Knowledge Extraction
  -> produces Extracted Knowledge Registry
  -> consumed by Knowledge Deduplication
  -> produces Deduplicated Knowledge Registry / Knowledge Merge Map
  -> consumed by Knowledge Graph
  -> produces Stage 2 Knowledge Graph
  -> consumed by Canonical Architecture Knowledge
  -> produces V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md
  -> consumed by Knowledge Acceptance
  -> produces Knowledge Acceptance Report
  -> consumed by Knowledge Lock
  -> produces LOCKED_KNOWLEDGE / Knowledge Baseline
  -> consumed by Program Closure
  -> produces OMP Continuation
```

## Program Execution Law

All Stage 2 execution occurs only through the official lifecycle and state machine.

Execution rules:

- Stage 2.2 execution without Stage 2.1 accepted output is forbidden.
- Stage 2.3 execution without Stage 2.2 accepted output is forbidden.
- Stage 2.4 execution without Stage 2.3 accepted output is forbidden.
- Stage 2.5 execution without Stage 2 Knowledge Graph is forbidden.
- Stage 2.6 execution without canonical knowledge output is forbidden.
- Stage 2.7 execution without Knowledge Acceptance output is forbidden.
- `LOCKED_KNOWLEDGE` changes outside Stage 2 Program Closure or Knowledge Evolution Law are forbidden.
- Alternative execution routes are forbidden.
- Parallel Stage 2 programs are forbidden.
- Program State Machine bypass is forbidden.
- Acceptance Gate bypass is forbidden.
- Stage execution must stop at `READY_FOR_ACCEPTANCE` after automatic reviews and the Engineering Report.
- Independent Acceptance starts only after a separate operator command.
- Next-stage execution starts only after an accepted previous-stage result and a separate operator command.
- Automatic stage-to-stage execution is forbidden.

## Failure Recovery Model

Stage 2 recovery sequence:

```text
FAIL
  -> Root Cause Analysis
  -> Correction
  -> Revalidation
  -> Re-execution
  -> PASS
```

Recovery rules:

- `FAIL` never automatically rolls back a previously accepted stage.
- Re-execution starts only after the root cause is corrected.
- Revalidation uses the same acceptance gate as the failed stage.
- `HOLD` pauses the current stage and records the missing evidence, unresolved owner, or bounded review item.
- `HOLD` exits only through `PASS`, `PASS_WITH_MINOR_RISKS`, `FAIL`, or `BLOCKED`.
- `MANUAL_REVIEW` is bounded and must end in `PASS`, `FAIL`, or `EXPLICIT_EXCEPTION_ACCEPTED`.
- `EXPLICIT_EXCEPTION_ACCEPTED` must name the owner, risk, scope, destination, and consumer impact.
- Manual review cannot change architecture, create a new owner, or promote history to Current Truth.

## Output Verification Law

Every Stage 2 deliverable follows the same verification sequence:

```text
Artifact
  -> Schema Validation
  -> Completeness Validation
  -> Producer Validation
  -> Consumer Validation
  -> Verification Result
  -> READY_FOR_ACCEPTANCE
  -> STOP
  -> Independent Acceptance
  -> Next Stage READY
```

Verification rules:

- Schema Validation proves the artifact has the required logical structure.
- Completeness Validation proves the artifact satisfies stage completion criteria through direct fields or deterministic resolution through official Stage 2 artifacts.
- Producer Validation proves the declared producer created the artifact.
- Consumer Validation proves the next stage or post-lock consumer is defined.
- Verification Result is stored in the Engineering Report and can make the stage `READY_FOR_ACCEPTANCE`.
- Acceptance records the official acceptance output only when performed as an independent acceptance action.
- Next Stage becomes `READY` only after accepted artifacts exist.
- Next Stage enters `IN_PROGRESS` only after a separate operator command.
- A `FAIL` result at any verification step blocks downstream consumption.

Knowledge Object Verification:

- Every Knowledge Object created by Stage 2.2 must pass verification before entering the Extracted Knowledge Registry.
- Verification must confirm Schema, Source, Trust Level, Terminal State, Owner, Consumer, Provenance, Destination, Forbidden Misuse, Review State, and Atomicity.
- A Knowledge Object with any missing mandatory element is `KNOWLEDGE_OBJECT_VERIFICATION_FAIL`.
- `KNOWLEDGE_OBJECT_VERIFICATION_FAIL` objects cannot be saved into the Extracted Knowledge Registry.
- Verification may use direct fields or deterministic resolution through official Stage 2 artifacts.
- Verification must record every Resolution Path used to satisfy logical completeness.
- Verification must prove that the object does not authorize architecture change, owner change, Runtime change, Planner change, Authority change, OMP change, production routing change, or superseded-state promotion.

Verification Evidence Law:

- Every verification step produces a Verification Result.
- Verification Result is stored in the engineering report for the current stage.
- Verification is complete only when the Verification Result exists.
- Missing Verification Result means Verification is `FAIL`.
- Downstream stages cannot consume artifacts with missing Verification Result.

## Logical Schema Law

Stage 2 uses logical schema completeness.

A required program attribute must exist, but the program does not require every required field to be physically stored in the same record.

Allowed schema forms:

| Schema form | Meaning |
| --- | --- |
| Logical Schema | The complete required field set exists across official Stage 2 artifacts and can be resolved deterministically. |
| Physical Schema | The complete required field set is stored directly in one record. |

Physical Schema is allowed.
Logical Schema is allowed.
Physical denormalization is not required when Logical Schema is complete.

Example:

```text
Knowledge Candidate Registry
  -> Source
  -> Trust Matrix
  -> Trust Level
```

This is a valid implementation when the resolution path is official, unique, and deterministic.

Logical Schema rules:

- every required attribute must be stored directly or deterministically resolved;
- a normalized artifact is complete when all required attributes can be resolved through official Stage 2 artifacts;
- Acceptance must verify logical completeness, not physical field co-location;
- Acceptance must not require duplicate storage of a value that is deterministically resolvable through official Stage 2 artifacts;
- if a required value is neither stored directly nor deterministically resolved, Schema Validation is `FAIL`;
- if a required value has multiple competing official resolution paths that produce different or ambiguous values, Schema Validation is `FAIL`;
- if a required value has exactly one official resolution path and no ambiguity, Schema Validation is `PASS`.

Logical Schema does not weaken the Knowledge Object Model, Source Classification Model, Terminal State Law, Traceability Law, or No Orphan Artifact Law.
It defines how required fields may be represented without forcing unnecessary duplication.

## Deterministic Resolution Law

Every required field in a Stage 2 artifact must satisfy exactly one of these conditions:

1. `STORED_DIRECTLY`.
2. `DETERMINISTICALLY_RESOLVED`.

`STORED_DIRECTLY` means the field value is present in the artifact record itself.

`DETERMINISTICALLY_RESOLVED` means the field value is obtained from exactly one official Stage 2 artifact through a declared Resolution Path.

Valid deterministic resolution requires:

- the source artifact is official for the current stage;
- the join key or lookup key is explicit;
- the resolution path has exactly one result;
- the resolved value does not conflict with any direct value;
- the resolved value has a canonical owner or source owner;
- the resolution path is recorded in the current stage report or acceptance report.

Resolution outcomes:

| Resolution outcome | Meaning |
| --- | --- |
| `PASS` | Exactly one official path resolves the value. |
| `FAIL` | No official path resolves the value. |
| `FAIL` | More than one competing path resolves the value ambiguously. |
| `FAIL` | A direct value conflicts with a resolved value. |
| `HOLD` | A bounded manual review is required to choose the official path without changing architecture. |

Examples:

```text
Candidate
  -> Source
  -> Trust Matrix
  -> Trust Level
```

```text
Candidate
  -> Terminal State Resolution
  -> Terminal State
```

```text
Queue Item
  -> Candidate
  -> Owner Matrix
  -> Owner
```

## Normalized Artifact Law

Stage 2 artifacts may be normalized.

Normalization is valid when:

- logical schema is complete;
- all required dependencies are deterministic;
- no ambiguous lookup exists;
- no cyclic dependency is required to resolve a field;
- every resolved field has a recorded Resolution Path;
- every normalized artifact still has producer, consumer, owner, acceptance, terminal state, and storage location;
- downstream consumers can resolve required fields without inventing a new source, owner, or rule.

It is forbidden to require denormalization when:

- logical schema is complete;
- all dependencies are deterministic;
- there is no ambiguity;
- there is no cyclic dependency;
- traceability is preserved.

Normalization must not create:

- a new truth source;
- a new owner;
- a new acceptance gate;
- a hidden extraction step;
- a bypass around Terminal State Law;
- a bypass around Stage Transition Law.

## Traceability Law

Every Stage 2 artifact must preserve this traceability chain:

```text
Stage
  -> Inputs
  -> Outputs
  -> Producer
  -> Consumer
  -> Evidence
  -> Acceptance
  -> Terminal State
```

Traceability rules:

- The origin of every Stage 2 result must be provable.
- Every artifact must point to its producing stage.
- Every artifact must point to its consuming stage or post-lock consumer.
- Every artifact must point to evidence and acceptance output.
- Every terminal state must trace back to accepted evidence.
- Every logically resolved field must record a `Resolution Path`.
- A `Resolution Path` must be unique.
- A `Resolution Path` must use only official Stage 2 artifacts or canonical owners declared by the current stage.
- A logically resolved field without a unique `Resolution Path` is incomplete.

Resolution Path examples:

```text
Candidate
  -> Source
  -> Trust Matrix
  -> Trust Level
```

```text
Candidate
  -> Terminal State Resolution
  -> Terminal State
```

```text
Queue Item
  -> Candidate
  -> Knowledge Candidate Registry
  -> Category / Owner / Destination
```

## No Orphan Artifact Law

Every Stage 2 artifact must have all required ownership fields:

- Producer;
- Consumer;
- Owner;
- Acceptance;
- Terminal State;
- Storage Location.

An artifact missing any required ownership field is `INCOMPLETE_ARTIFACT`.
`INCOMPLETE_ARTIFACT` cannot be consumed by any Stage 2 stage or post-lock process.

## Not Applicable Law

`NOT_APPLICABLE` is allowed only with proof.

Required chain:

```text
NOT_APPLICABLE
  -> Reason
  -> Evidence
  -> Acceptance
```

Any `NOT_APPLICABLE` without Reason, Evidence, and Acceptance is `UNJUSTIFIED_NOT_APPLICABLE`.
`UNJUSTIFIED_NOT_APPLICABLE` blocks the artifact, stage, or review that contains it.

## Stage 2 Metrics

Stage 2 execution must report engineering metrics so the quality of the knowledge baseline is measurable.

Required metrics:

| Metric | Meaning |
| --- | --- |
| `Total Sources` | Count of all discovered sources in the Source Registry. |
| `Canonical Sources` | Count of sources classified as `CANONICAL`. |
| `Knowledge Objects` | Count of extracted knowledge objects. |
| `P0 Objects` | Count of P0 knowledge candidates or objects. |
| `P1 Objects` | Count of P1 knowledge candidates or objects. |
| `Duplicate Ratio` | Share of extracted objects later merged or superseded during deduplication. |
| `Extraction Coverage` | Share of extraction-eligible candidates processed by Stage 2.2. |
| `Deduplication Coverage` | Share of extracted objects reviewed by Stage 2.3. |
| `Knowledge Graph Nodes` | Count of accepted graph nodes. |
| `Knowledge Graph Edges` | Count of accepted graph edges. |
| `Manual Review Count` | Count of objects or candidates requiring bounded manual review. |
| `Historical Objects` | Count of objects preserved as history-only. |
| `Terminal Objects` | Count of objects with terminal current truth. |
| `Canonical Concepts` | Count of deduplicated canonical concepts accepted for canonical knowledge. |

These metrics are quality indicators. They do not create authority, change architecture, change OMP, change Runtime, or certify production autonomy.

## 5. Knowledge Object Model

Stage 2 works with knowledge objects, not files.

A knowledge object is a durable engineering conclusion, rule, boundary, responsibility, relationship, lifecycle, owner mapping, or discovery that can be consumed by future V7 work.

A Knowledge Object is the minimum engineering knowledge unit in Stage 2.
It is not a new architecture entity, not a graph node, not a canonical concept, and not canonical prose.
It is the atomic extracted unit consumed by Stage 2.3.

Knowledge Object atomicity is determined by the Stage 2.2 Atomicity Test.

Minimum knowledge object schema:

| Field | Required | Description |
| --- | ---: | --- |
| `knowledge_id` | Yes | Stable Stage 2 identifier. |
| `title` | Yes | Human-readable knowledge name. |
| `category` | Yes | Knowledge category. |
| `source_refs` | Yes | Source documents, sections, reports, code owners, or evidence. |
| `canonical_owner` | Yes | Existing owner responsible for durable truth. |
| `source_type` | Yes | Source classification. |
| `trust_level` | Yes | Trust classification. |
| `terminal_state` | Yes | Current truth after superseded states are resolved. |
| `provenance` | Yes | Evidence chain and state transitions. |
| `destination` | Yes | Future use location. |
| `consumers` | Yes | Existing consumers that should use the knowledge. |
| `forbidden_misuse` | Yes | What this knowledge must not be used to authorize. |
| `review_state` | Yes | Inventory, extracted, deduplicated, accepted, locked, or rejected. |

Knowledge categories:

- Laws;
- Principles;
- Responsibilities;
- Producer / Consumer;
- Runtime;
- Authority;
- Verification;
- Rollback;
- Lifecycle;
- Governance;
- Boundaries;
- Forbidden Actions;
- Engineering Discoveries;
- Certification Discoveries;
- Evolution Rules;
- Owner Rules;
- Evidence Rules;
- Implementation Rules.

## 6. Source Classification Model

Every discovered source must be classified.

Source Type:

| Source Type | Meaning |
| --- | --- |
| `CANONICAL` | Durable current truth owner. |
| `GOVERNANCE` | Program, policy, OMP, Authority, lifecycle, or operating control source. |
| `IMPLEMENTATION` | Source code, tools, tests, function graph, or implementation owner evidence. |
| `CERTIFICATION` | Domain, capability, acceptance, audit, or certification result. |
| `EVIDENCE` | Report, runtime proof, test output, audit output, screenshot, or append-only proof. |
| `RESEARCH` | Research, discovery, comparison, or analysis source. |
| `HISTORICAL` | Superseded or chronology-preserving source. |
| `SUPPORTING` | Contextual source that supports but does not own terminal truth. |

Trust Level:

| Trust Level | Meaning |
| --- | --- |
| `TERMINAL` | Accepted final state for the relevant knowledge. |
| `AUTHORITATIVE` | Current canonical owner or governing owner. |
| `DERIVED` | Derived from authoritative or terminal sources. |
| `HISTORICAL` | Preserved as history, not current truth by itself. |
| `SUPERSEDED` | Explicitly replaced by later terminal evidence. |

## 7. Terminal State Law

Stage 2 must preserve history while consuming only current terminal truth.

Append-only evidence can contain older states. Those states must not be promoted as active knowledge after a later terminal state supersedes them.

Canonical example:

```text
Domain 11 Diagnosis

NOT CERTIFIED
  -> Recovery Discovery
  -> Diagnosis Record Contract
  -> Implementation Acceptance
  -> Implementation Mission
  -> Implementation Report
  -> Recertification
  -> Corpus Audit
  -> Final Acceptance
  -> CURRENT TRUTH = CERTIFIED
```

Stage 2 must record the whole provenance chain, but the current knowledge object must use:

```text
terminal_state = CERTIFIED
trust_level = TERMINAL
```

It is forbidden to promote superseded `NOT CERTIFIED` text as active project truth.

## 8. Stage 2.1 Knowledge Inventory

Status: `COMPLETE`

Purpose:

Fully inventory Stage 1 engineering knowledge.

Stage 2.1 must not extract, merge, deduplicate, rewrite, or canonicalize knowledge.
It only identifies where knowledge exists and prepares extraction.

### 8.1 Inventory Sources

Codex must discover the fullest available source set.

It must not limit inventory to the handoff.

Discovery is performed through two distinct families:

1. `Knowledge Sources`.
2. `Discovery Indexes`.

`Knowledge Sources` are documents, records, code owners, reports, contracts, ADRs, policies, and other artifacts that may contain candidate engineering knowledge after classification, trust assignment, owner resolution, and terminal-state resolution.

`Discovery Indexes` are navigation artifacts that help Stage 2.1 find knowledge. They do not create knowledge and do not establish canonical truth by themselves.

Mandatory discovery surfaces:

- Canonical Reference;
- SYSTEM_MAP;
- OMP;
- Current Program State;
- Runtime Model;
- Decision Model;
- Autonomous Operating System;
- Autonomous Runtime Model;
- Autonomous Execution Program;
- Architecture Certification Corpus;
- Architect Summary;
- Corpus Audit;
- Final Acceptance;
- Domain Recovery;
- Diagnosis Record Contract;
- Diagnosis Implementation Acceptance;
- ADRs;
- Research;
- Function Graph;
- Function Appendix;
- Engineering Reports;
- Reference Documents;
- Product Specification;
- Policies;
- capabilities under `docs/reference/capabilities/`;
- process documents;
- prompt documents;
- tests and code owners when they are necessary to prove implementation reality;
- any other canonical, governance, implementation, certification, evidence, research, historical, or supporting source found through repository search.

### Discovery Index Model

Discovery Index:

- helps find Sources;
- helps find Owners;
- helps find Producers;
- helps find Consumers;
- helps find Runtime Boundaries;
- helps find Authority Boundaries;
- helps find Relationships;
- helps find Implementation Evidence.

Discovery Index is a navigation layer only.

Discovery Index is not:

- a Canonical Source;
- a Historical Source;
- Evidence;
- a Knowledge Object;
- a Canonical Owner;
- a Terminal State;
- engineering truth.

Discovery Index never changes engineering truth.
Any source, owner, relationship, boundary, or implementation fact found through a Discovery Index must be confirmed through an official Source classified by Stage 2.1.

Discovery Indexes may participate in discovery and traceability.
They must not be promoted into `CANONICAL_KNOWLEDGE` unless an official Source independently contains the same knowledge and owns it.

### Discovery Index Family

Stage 2.1 must classify the following as Discovery Indexes when they exist:

| Discovery Index | Required use | Truth rule |
| --- | --- | --- |
| Repository Search | Required | Navigation only; found artifacts must be classified separately. |
| SYSTEM_MAP | Required | Owner/topology lookup; canonical owner status remains defined by SYSTEM_MAP itself and relevant canonical owners. |
| Function Graph | Required when present | Navigation only for implementation relationships and boundaries. |
| Function Graph Appendix | Required when present | Navigation only for implementation relationships and boundaries. |
| ADR index/search | Required when present | Navigation only; individual ADRs are classified separately. |
| Report index/search | Required when present | Navigation only; individual reports or report families are classified separately. |
| Reference index/search | Required when present | Navigation only; individual reference documents are classified separately. |
| Code search / owner search | Required when implementation reality matters | Navigation only; implementation evidence must be classified separately. |
| Other project indexes discovered by repository search | Required when present | Navigation only until classified by Stage 2.1. |

Function Graph pinning:

If these files exist in the repository, they are mandatory Discovery Index artifacts for Stage 2.1:

```text
docs/reports/research/V7_AUTONOMOUS_MODEL_FUNCTION_GRAPH_APPENDIX.md
docs/reports/research/V7_AUTONOMOUS_MODEL_FUNCTION_GRAPH_APPENDIX.json
```

If they exist, Stage 2.1 must use them during Knowledge Inventory to discover implementation owners, producers, consumers, runtime boundaries, authority boundaries, relationships, read-only surfaces, mutation-capable surfaces, and implementation evidence candidates.

If they do not exist, Stage 2.1 continues using the remaining Discovery Surfaces and records the missing Function Graph Appendix artifacts as `NOT_AVAILABLE_DISCOVERY_INDEX`.

Function Graph Appendix rule:

- Function Graph Appendix helps find implementation evidence.
- Function Graph Appendix does not make implementation evidence canonical.
- Function Graph Appendix does not override Canonical Reference, SYSTEM_MAP, OMP, ADRs, Runtime Model, Decision Model, terminal acceptance reports, or current source code.
- Any knowledge candidate found through Function Graph Appendix must resolve to an official Source, owner, trust level, terminal state, and destination before Stage 2.2 extraction.

Required discovery methods:

- internal Codex repository search;
- project reference files;
- SYSTEM_MAP owner mapping;
- function graph and appendix review;
- ADR index review;
- report index review;
- canonical owner lookup;
- existing owner verification when implementation reality matters.

Discovery Exhaustion Criteria:

- all Canonical Sources are checked;
- all Mandatory Discovery Surfaces are checked;
- all Discovery Indexes are checked;
- all Reference Index entries are checked;
- all SYSTEM_MAP references are expanded;
- all ADR references are expanded;
- all discovered links are processed;
- all discovered sources are classified;
- all found Discovery Indexes are processed;
- all sources found through Discovery Indexes are either classified or explicitly marked `UNKNOWN_REQUIRES_DISCOVERY`;
- no unprocessed Discovery Surface remains;
- every unknown source has terminal state `UNKNOWN_REQUIRES_DISCOVERY` or `CLASSIFIED`.

Discovery is exhausted only after all criteria are true.
Stage 2.1 cannot complete because searching stopped; it completes only because Discovery Exhaustion Criteria passed.

Output:

```text
Source Registry
```

### 8.2 Source Classification

For each discovered source, Stage 2.1 must record:

- path or identifier;
- source title;
- source type;
- trust level;
- owner;
- canonical consumer;
- whether it is terminal, current, derived, historical, or superseded;
- whether it participates in Stage 2.2 extraction.

Output:

```text
Classification Matrix
Trust Matrix
Owner Matrix
```

### 8.3 Knowledge Candidate Discovery

For every source, Stage 2.1 must register whether it contains candidate knowledge in these categories:

- Laws;
- Principles;
- Responsibilities;
- Producer / Consumer;
- Runtime;
- Authority;
- Verification;
- Rollback;
- Lifecycle;
- Governance;
- Boundaries;
- Forbidden Actions;
- Engineering Discoveries;
- Certification Discoveries;
- Evolution Rules;
- Owner Rules;
- Evidence Rules;
- Implementation Rules.

Stage 2.1 must not extract the knowledge text.
It only registers that a candidate exists.

Output:

```text
Knowledge Candidate Registry
```

Knowledge Candidate Registry schema:

| Field | Required |
| --- | ---: |
| `candidate_id` | Yes |
| `source` | Yes |
| `category` | Yes |
| `owner` | Yes |
| `trust_level` | Yes |
| `terminal_state` | Yes |
| `priority` | Yes |
| `risk` | Yes |
| `destination` | Yes |
| `consumer` | Yes |
| `extraction_reason` | Yes |
| `blocking_concern` | Yes |

Every candidate must satisfy this schema.
A candidate that fails the schema is `INCOMPLETE_CANDIDATE` and cannot enter the Knowledge Extraction Queue.

### 8.4 Terminal State Resolution

For each candidate, Stage 2.1 must identify the current terminal state or mark it for manual review.

Allowed terminal-state classifications:

- `CURRENT_TERMINAL`;
- `CURRENT_AUTHORITATIVE`;
- `DERIVED_FROM_TERMINAL`;
- `HISTORICAL_ONLY`;
- `SUPERSEDED_BY_TERMINAL_EVIDENCE`;
- `CONFLICT_REQUIRES_MANUAL_REVIEW`;
- `UNKNOWN_REQUIRES_DISCOVERY`.

Resolution rule:

```text
Latest accepted terminal evidence wins over earlier append-only history.
```

Output:

```text
Terminal State Resolution
```

### 8.5 Knowledge Extraction Queue

Stage 2.1 must build an extraction queue by Knowledge Candidate, not by document.

Each queue item must include:

- source;
- knowledge category;
- priority;
- risk;
- destination;
- owner;
- terminal state;
- extraction reason;
- blocking concern, if any.

Allowed destinations:

| Destination | Meaning |
| --- | --- |
| `CANONICAL_KNOWLEDGE` | Candidate should be extracted into the canonical architecture knowledge document. |
| `KNOWLEDGE_GRAPH` | Candidate should become a graph node or edge. |
| `HISTORICAL` | Candidate remains provenance/history only. |
| `IGNORE` | Candidate is not relevant to Stage 2 knowledge memory. |
| `MANUAL_REVIEW` | Candidate cannot be safely classified without human or deeper evidence review. |

Priority model:

| Priority | Meaning |
| --- | --- |
| `P0` | Required for locked architecture memory, safety boundaries, terminal truth, owner mapping, or forbidden-action preservation. |
| `P1` | Required for producer/consumer continuity, governance, lifecycle, or implementation continuity. |
| `P2` | Useful supporting knowledge or evidence provenance. |
| `P3` | Historical or low-risk supporting context. |

Risk model:

| Risk | Meaning |
| --- | --- |
| `HIGH` | Wrong extraction could create unsafe active truth, authority confusion, Runtime confusion, owner duplication, or superseded-state promotion. |
| `MEDIUM` | Wrong extraction could mislead future engineering or duplicate knowledge. |
| `LOW` | Wrong extraction is mostly documentation hygiene risk. |

Output:

```text
Knowledge Extraction Queue
```

### 8.6 Inventory Validation

Before Stage 2.2 begins, Stage 2.1 must verify:

- Discovery Exhaustion Criteria passed;
- all canonical owners are discovered;
- all required source families were searched;
- no unknown high-priority source family remains;
- source classifications are complete;
- trust levels are assigned;
- owners are assigned or explicitly marked manual review;
- terminal state is resolved or explicitly marked manual review;
- candidate registry is complete enough for extraction;
- extraction queue is ordered by candidate priority and risk;
- Stage 2 boundaries were preserved.

Validation verdicts:

- `STAGE_2_1_PASS`;
- `STAGE_2_1_PASS_WITH_MINOR_RISKS`;
- `STAGE_2_1_HOLD`;
- `STAGE_2_1_FAIL`.

Stage 2.2 starts only after `STAGE_2_1_PASS` or `STAGE_2_1_PASS_WITH_MINOR_RISKS`.

### 8.7 Inventory Report

Stage 2.1 must create:

```text
docs/reports/research/V7_STAGE2_1_KNOWLEDGE_INVENTORY.md
```

Required report sections:

- Inventory Summary;
- Source Registry;
- Classification Matrix;
- Trust Matrix;
- Terminal State Resolution;
- Knowledge Candidate Registry;
- Extraction Queue;
- Validation Verdict;
- Risks;
- Next Stage.

### Stage Completion Criteria

Stage 2.1 is complete only when:

- all required Source Families are discovered or explicitly marked `UNKNOWN_REQUIRES_DISCOVERY`;
- Discovery Exhaustion Criteria passed;
- Source Registry is complete;
- Classification Matrix is complete;
- Trust Matrix is complete;
- Owner Matrix is complete;
- Knowledge Candidate Registry is complete;
- every Knowledge Candidate Registry entry satisfies the required candidate schema;
- Terminal State Resolution is complete or bounded by manual review;
- Knowledge Extraction Queue is formed by Knowledge Candidate, not by document;
- Inventory Report exists at `docs/reports/research/V7_STAGE2_1_KNOWLEDGE_INVENTORY.md`;
- Architecture Review is PASS;
- Quality Review is PASS;
- Self Review is PASS;
- Validation Verdict is `STAGE_2_1_PASS` or `STAGE_2_1_PASS_WITH_MINOR_RISKS`.

## 9. Stage 2.2 Knowledge Extraction

Status: `COMPLETE`

Purpose:

Extract reusable engineering knowledge from the approved candidate queue.

Stage 2.2 extracts knowledge objects, not document summaries.

Rules:

- extract from candidates, not from whole files;
- preserve source references and provenance;
- preserve owner and consumer mapping;
- preserve forbidden actions;
- preserve terminal state;
- mark ambiguity for manual review;
- do not deduplicate during extraction except for exact duplicate source references;
- do not change architecture.

### Extraction Unit

The minimum Stage 2.2 input unit is one approved Knowledge Candidate from the Stage 2.1 Knowledge Extraction Queue.

The Stage 2.2 output unit is zero, one, or multiple Knowledge Objects plus an extraction disposition for the processed candidate.

Allowed candidate outcomes:

| Candidate outcome | Allowed when |
| --- | --- |
| `NO_OBJECT_CREATED` | The candidate destination is `IGNORE`, the candidate is not extraction-eligible, the candidate is history-only with no reusable knowledge object, or the candidate is rejected with an evidence-backed reason. |
| `ONE_OBJECT_CREATED` | The candidate expresses exactly one atomic engineering law, principle, responsibility, boundary, owner rule, evidence rule, implementation rule, lifecycle rule, verification rule, authority rule, runtime rule, governance rule, or discovery. |
| `MULTIPLE_OBJECTS_CREATED` | The candidate contains multiple separable atomic knowledge units with distinct category, owner, consumer, destination, terminal state, or forbidden misuse. |
| `MANUAL_REVIEW` | Source, terminal state, trust level, owner, consumer, provenance, destination, forbidden misuse, or object boundary cannot be deterministically resolved through official Stage 2 artifacts. |
| `REJECTED_WITH_REASON` | The candidate cannot produce a valid Knowledge Object because required evidence is absent, the candidate violates Stage 2 boundaries, or extraction would promote superseded or unsupported truth. |

Stage 2.2 processes every queue item by Knowledge Candidate.
It does not process arbitrary documents as extraction units.

### Extraction Lifecycle

Every Stage 2.2 extraction follows this deterministic lifecycle:

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

Lifecycle rules:

- `Resolve Sources` uses the candidate Source field and the Stage 2.1 Source Registry.
- `Resolve Terminal State` uses the Terminal State Resolution artifact and never promotes superseded history to current truth.
- `Resolve Trust` uses the Trust Matrix or the unique recorded Resolution Path from Source to Trust Level.
- `Resolve Owner` uses the Owner Matrix, canonical owner mapping, or a unique recorded Resolution Path.
- `Resolve Consumer` uses the candidate destination, Program Producer / Consumer Model, and downstream Stage 2 consumer contract.
- `Resolve Provenance` records the source chain, terminal-state chain, and acceptance evidence that support the object.
- `Extract Knowledge` extracts only reusable engineering knowledge and must not summarize a document.
- `Atomicity Review` applies the Atomicity Test before any Knowledge Object is created.
- `Create Knowledge Object(s)` applies the Knowledge Object Creation Rules below.
- `Knowledge Object Verification` applies Output Verification Law before registry admission.
- `Save` writes only verified Knowledge Objects into the Extracted Knowledge Registry.
- `Extraction Complete` records the candidate disposition in `docs/reports/research/V7_STAGE2_2_KNOWLEDGE_EXTRACTION.md`.

If any lifecycle step cannot be resolved deterministically, the candidate disposition is `MANUAL_REVIEW` or `REJECTED_WITH_REASON`.
The lifecycle does not create an alternate stage, acceptance gate, owner, truth source, or extraction authority.

### Knowledge Object Creation Rules

Knowledge Object creation is governed by program rules, not by session preference.

Atomicity Test:

A Knowledge Object is atomic only when all of these criteria are true at the same time:

- it has one primary engineering meaning;
- it has one engineering responsibility;
- it has one category;
- it has one Terminal State;
- it has one primary Canonical Owner;
- it has one primary Consumer;
- it has one Provenance Chain;
- it has one Forbidden Misuse;
- it contains no independent engineering assertion that can exist as a standalone Knowledge Object.

Atomicity Review:

Every Knowledge Candidate must pass Atomicity Review before Knowledge Object creation.

Allowed Atomicity Review results:

| Result | Meaning | Required candidate disposition |
| --- | --- | --- |
| `ATOMIC` | The candidate contains exactly one atomic engineering knowledge unit under the Atomicity Test. | `ONE_OBJECT_CREATED` when all required fields verify; otherwise `MANUAL_REVIEW` or `REJECTED_WITH_REASON`. |
| `SPLIT_REQUIRED` | The candidate contains multiple independent engineering knowledge units under the Object Splitting Rule. | `MULTIPLE_OBJECTS_CREATED` when all split objects verify; otherwise `MANUAL_REVIEW`. |
| `MANUAL_REVIEW` | The Atomicity Test cannot be resolved deterministically from official Stage 2 artifacts. | `MANUAL_REVIEW`. |

Atomicity Review must be recorded in the Stage 2.2 report.

Creation rules:

- Create no object when the candidate is not extraction-eligible, is explicitly `IGNORE`, lacks an official source, lacks a terminal state, or is rejected with evidence.
- Create one object only when Atomicity Review returns `ATOMIC` and all required fields are directly stored or deterministically resolved.
- Create multiple objects only when Atomicity Review returns `SPLIT_REQUIRED` and each resulting Knowledge Object passes Knowledge Object Verification.
- Route to `MANUAL_REVIEW` when object boundaries, source, terminal state, trust level, owner, consumer, provenance, destination, forbidden misuse, or review state are ambiguous.
- Preserve exact duplicate source references only as shared provenance; do not merge duplicate knowledge concepts during Stage 2.2.
- Preserve superseded knowledge only as history or provenance unless Terminal State Resolution marks it as current truth.
- Do not create an object whose source is only a Discovery Index without confirmation by an official Source.
- Do not create an object that changes architecture, creates a new owner, or changes OMP, Runtime, Planner, Authority, production routing, or domain boundaries.

Every created Knowledge Object must satisfy the Knowledge Object Model.

Object Splitting Rule:

If a candidate contains independent engineering assertions with different Category, Owner, Consumer, Terminal State, Destination, Forbidden Misuse, or Provenance Chain, Stage 2.2 must create `MULTIPLE_OBJECTS_CREATED`.

If all engineering assertions inside a candidate protect the same responsibility, Boundary, Law, Lifecycle, or primary engineering meaning, Stage 2.2 must create `ONE_OBJECT_CREATED`.

Atomicity Decision Rule:

The decision between `ONE_OBJECT_CREATED` and `MULTIPLE_OBJECTS_CREATED` is not made by Codex preference.
It is made only by the Atomicity Test, Object Splitting Rule, Deterministic Resolution Law, Traceability Law, and Knowledge Object Verification.
If these rules do not produce a single deterministic outcome, the candidate must be routed to `MANUAL_REVIEW`.

### Knowledge Object Verification

Before a Knowledge Object can enter the Extracted Knowledge Registry, Stage 2.2 must verify:

| Verification item | Required result |
| --- | --- |
| Schema | All Knowledge Object Model fields exist directly or through deterministic resolution. |
| Source | Source references resolve to official Stage 2 sources. |
| Trust Level | Trust Level resolves through one official path. |
| Terminal State | Terminal State resolves through Terminal State Resolution and separates current truth from history. |
| Owner | Canonical owner or existing owner resolves through one official path. |
| Consumer | Consumer resolves through destination and Program Producer / Consumer Model. |
| Provenance | Provenance chain is complete and evidence-backed. |
| Destination | Destination is one of the official Stage 2 destinations or a bounded manual review disposition. |
| Forbidden Misuse | The object states what it cannot authorize and preserves Stage 2 boundaries. |
| Review State | Review state is valid for Stage 2.2 and is not accepted, locked, or canonicalized prematurely. |
| Atomicity | Atomicity Review result supports the object boundary: `ATOMIC` for one object or `SPLIT_REQUIRED` for multiple objects. |

If any required verification item is missing, conflicting, ambiguous, or unresolved, the object is not admitted to the Extracted Knowledge Registry.
The candidate must instead be recorded as `MANUAL_REVIEW`, `REJECTED_WITH_REASON`, or `NO_OBJECT_CREATED` in the Stage 2.2 report.

### Extraction Determinism

Given the same Stage 2 program revision, the same accepted Stage 2.1 outputs, and the same Knowledge Extraction Queue, Stage 2.2 must produce the same Knowledge Objects and the same candidate dispositions.

Determinism rules:

- All object creation decisions must follow this program, the Knowledge Object Model, Terminal State Law, Logical Schema Law, Deterministic Resolution Law, Traceability Law, and Output Verification Law.
- Codex interpretation cannot override missing, conflicting, or ambiguous evidence.
- Subjective judgment is not a valid source of Source, Trust Level, Terminal State, Owner, Consumer, Provenance, Destination, Forbidden Misuse, or Review State.
- If the program rules do not determine exactly one valid extraction result, the candidate must be routed to `MANUAL_REVIEW`.
- Manual review is a deterministic disposition when extraction cannot be safely resolved by the official artifacts.
- Stage 2.2 cannot create alternate extraction lifecycles, alternate acceptance gates, alternate schemas, or alternate registry formats.

Output:

```text
Extracted Knowledge Registry
docs/reports/research/V7_STAGE2_2_KNOWLEDGE_EXTRACTION.md
```

Acceptance gate:

```text
STAGE_2_2_EXTRACTION_PASS
```

### Stage Completion Criteria

Stage 2.2 is complete only when:

- extraction consumed the approved Stage 2.1 Knowledge Extraction Queue;
- every P0 extraction candidate is extracted or rejected with an explicit evidence-backed reason;
- every P1 extraction candidate is extracted, deferred, or marked `MANUAL_REVIEW`;
- every processed candidate has a deterministic disposition: `NO_OBJECT_CREATED`, `ONE_OBJECT_CREATED`, `MULTIPLE_OBJECTS_CREATED`, `MANUAL_REVIEW`, or `REJECTED_WITH_REASON`;
- every processed candidate has Atomicity Review result: `ATOMIC`, `SPLIT_REQUIRED`, or `MANUAL_REVIEW`;
- every created Knowledge Object passed Knowledge Object Verification before entering the Extracted Knowledge Registry;
- every extracted knowledge object has source, owner, trust level, terminal state, provenance, destination, consumers, and forbidden misuse;
- every extracted Knowledge Object satisfies the Atomicity Test;
- every logical field used by extraction has a unique Resolution Path or direct stored value;
- extracted objects preserve terminal truth and superseded history separation;
- extraction did not deduplicate concepts beyond exact duplicate source references;
- Stage 2.2 used the official Extraction Lifecycle and did not create an alternate extraction mechanism;
- Extracted Knowledge Registry exists;
- `docs/reports/research/V7_STAGE2_2_KNOWLEDGE_EXTRACTION.md` exists;
- Architecture Review is PASS;
- Quality Review is PASS;
- Self Review is PASS;
- acceptance gate is `STAGE_2_2_EXTRACTION_PASS`.

## 10. Stage 2.3 Knowledge Deduplication

Status: `COMPLETE`

Purpose:

Collapse repeated knowledge into single canonical concepts while preserving all provenance.

Deduplication must not erase meaningful differences between:

- law and implementation rule;
- architecture boundary and runtime boundary;
- current truth and history;
- owner and consumer;
- certification evidence and canonical owner;
- prohibition and recommendation;
- terminal state and superseded state.

Output:

```text
Deduplicated Knowledge Registry
Knowledge Merge Map
Superseded Knowledge Map
docs/reports/research/V7_STAGE2_3_KNOWLEDGE_DEDUPLICATION.md
```

Acceptance gate:

```text
STAGE_2_3_DEDUPLICATION_PASS
```

### Stage Completion Criteria

Stage 2.3 is complete only when:

- every extracted knowledge object is reviewed for duplication;
- duplicate concepts are merged into canonical concepts without losing provenance;
- meaningful differences between law, rule, boundary, owner, consumer, evidence, and history are preserved;
- superseded knowledge is mapped without becoming current truth;
- Deduplicated Knowledge Registry exists;
- Knowledge Merge Map exists;
- Superseded Knowledge Map exists;
- `docs/reports/research/V7_STAGE2_3_KNOWLEDGE_DEDUPLICATION.md` exists;
- Duplicate Ratio and Deduplication Coverage are reported;
- Architecture Review is PASS;
- Quality Review is PASS;
- Self Review is PASS;
- acceptance gate is `STAGE_2_3_DEDUPLICATION_PASS`.

## 11. Stage 2.4 Knowledge Graph

Status: `COMPLETE`

Purpose:

Build the graph of Stage 2 knowledge objects and relationships.

Required node families:

- domains;
- laws;
- principles;
- owners;
- responsibilities;
- producer / consumer relationships;
- boundaries;
- forbidden actions;
- evidence;
- terminal states;
- decisions;
- implementation owners;
- destination owners;
- risks;
- manual review items.

Required edge families:

- owns;
- produces;
- consumes;
- forbids;
- verifies;
- supersedes;
- derives_from;
- certified_by;
- implemented_by;
- governs;
- depends_on;
- terminalizes;
- should_promote_to;
- should_remain_historical.

Output:

```text
Stage 2 Knowledge Graph
docs/reports/research/V7_STAGE2_4_KNOWLEDGE_GRAPH.md
```

Acceptance gate:

```text
STAGE_2_4_GRAPH_PASS
```

### Stage Completion Criteria

Stage 2.4 is complete only when:

- required node families are represented or explicitly marked `NOT_APPLICABLE` through Not Applicable Law;
- required edge families are represented or explicitly marked `NOT_APPLICABLE` through Not Applicable Law;
- every P0 canonical concept has graph representation unless manually reviewed;
- owners, sources, terminal states, consumers, boundaries, forbidden actions, and provenance are connected;
- graph output preserves current truth versus historical evidence;
- Knowledge Graph exists;
- `docs/reports/research/V7_STAGE2_4_KNOWLEDGE_GRAPH.md` exists;
- Knowledge Graph Nodes and Knowledge Graph Edges are reported;
- Architecture Review is PASS;
- Quality Review is PASS;
- Self Review is PASS;
- acceptance gate is `STAGE_2_4_GRAPH_PASS`.

## 12. Stage 2.5 Canonical Architecture Knowledge

Status: `COMPLETE_READY_ACCEPTED_AND_LOCKED`

Purpose:

Create the canonical architecture knowledge document:

```text
docs/reference/V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md
```

This document must contain accepted, deduplicated, owner-mapped, terminal-state-resolved knowledge.

It must not contain:

- raw report summaries;
- unresolved contradictions;
- superseded current truth;
- new architecture;
- new owners;
- new authority;
- Runtime behavior changes;
- Planner behavior changes;
- OMP changes.

Required sections:

- Knowledge Baseline;
- Architecture Laws;
- Domain Knowledge;
- Producer / Consumer Knowledge;
- Authority and Runtime Boundaries;
- Verification and Rollback Knowledge;
- Governance and OMP Knowledge;
- Owner and Evidence Rules;
- Evolution Rules;
- Forbidden Actions;
- Terminal State Rules;
- Knowledge Graph Pointers;
- Provenance Index;
- Consumer Index.

Output:

```text
V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md
Stage 2.5 Canonical Knowledge Report
```

Acceptance gate:

```text
STAGE_2_5_CANONICAL_KNOWLEDGE_READY
```

### Stage Completion Criteria

Stage 2.5 is complete only when:

- `docs/reference/V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md` exists;
- the document contains accepted, deduplicated, owner-mapped, terminal-state-resolved knowledge;
- required sections are present;
- every included knowledge object has source, owner, trust level, terminal state, provenance, and destination;
- raw report summaries are excluded;
- unresolved contradictions are excluded or marked for bounded manual review;
- superseded states are not promoted as current truth;
- no new architecture, owner, Authority, Runtime behavior, Planner behavior, or OMP change is introduced;
- Stage 2.5 Canonical Knowledge Report exists;
- Architecture Review is PASS;
- Quality Review is PASS;
- Self Review is PASS;
- acceptance gate is `STAGE_2_5_CANONICAL_KNOWLEDGE_READY`.

## 13. Stage 2.6 Knowledge Acceptance

Status: `COMPLETE_ACCEPTED_WITH_MINOR_RISKS`

Purpose:

Independently verify that Stage 2 knowledge is complete, consistent, traceable, safe, and usable.

Acceptance checks:

- all P0 candidates are extracted or explicitly rejected with reason;
- all P1 candidates are extracted, deferred, or manual-review classified;
- every knowledge object has source, owner, trust level, terminal state, provenance, and destination;
- no superseded state is promoted as current truth;
- no architecture change is introduced;
- no duplicate owner, Runtime, Planner, Authority, OMP, roadmap, or truth source is created;
- producer / consumer relationships are preserved;
- Authority, Runtime, Diagnosis, Verification, Rollback / Closure, Learning, OMP, and Current Program State boundaries are preserved;
- Function Graph synchronization risk is resolved or explicitly accepted as non-blocking;
- manual-review items are bounded and do not block locked knowledge;
- canonical knowledge has consumers.

Output:

```text
docs/reports/research/V7_STAGE2_6_KNOWLEDGE_ACCEPTANCE.md
```

Acceptance verdicts:

- `STAGE_2_KNOWLEDGE_ACCEPTED`;
- `STAGE_2_KNOWLEDGE_ACCEPTED_WITH_MINOR_RISKS`;
- `STAGE_2_KNOWLEDGE_HOLD`;
- `STAGE_2_KNOWLEDGE_REJECTED`.

Stage 2.7 starts only after `STAGE_2_KNOWLEDGE_ACCEPTED` or `STAGE_2_KNOWLEDGE_ACCEPTED_WITH_MINOR_RISKS`.

### Stage Completion Criteria

Stage 2.6 is complete only when:

- all acceptance checks are performed;
- all P0 candidates are extracted, accepted, or explicitly rejected with reason;
- all P1 candidates are extracted, deferred, or manual-review classified;
- every accepted knowledge object has required metadata;
- no superseded state is promoted as current truth;
- no architecture change is detected;
- no duplicate owner, Runtime, Planner, Authority, OMP, roadmap, or truth source is created;
- producer / consumer relationships are preserved;
- manual-review items are bounded and non-blocking or the stage returns HOLD;
- Knowledge Acceptance Report exists;
- Architecture Review is PASS;
- Quality Review is PASS;
- Self Review is PASS;
- acceptance verdict is `STAGE_2_KNOWLEDGE_ACCEPTED` or `STAGE_2_KNOWLEDGE_ACCEPTED_WITH_MINOR_RISKS`.

## 14. Stage 2.7 Knowledge Lock

Status: `COMPLETE_LOCKED_KNOWLEDGE`

Purpose:

Lock the accepted Stage 2 knowledge baseline.

Lock result:

```text
LOCKED_KNOWLEDGE
```

After lock:

- Stage 2 knowledge becomes the second foundation of V7 alongside locked architecture;
- future engineering must consume `V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md` when architecture knowledge matters;
- reports remain evidence, not new truth owners;
- history remains preserved but terminal truth wins;
- architecture remains closed by default;
- future knowledge evolution must pass formal owner and evidence procedures.

Output:

```text
docs/reports/research/V7_STAGE2_7_KNOWLEDGE_LOCK.md
Canonical Reference synchronization result
SYSTEM_MAP synchronization result
Current Program State update
OMP Knowledge Baseline handoff
```

Final verdict:

```text
STAGE_2_ACCEPTED
STAGE_2_KNOWLEDGE_LOCKED
READY_FOR_POST_STAGE_2_OMP_CONTINUATION
```

### Stage Completion Criteria

Stage 2.7 is complete only when:

- accepted knowledge baseline is locked as `LOCKED_KNOWLEDGE`;
- Knowledge Lock Report exists;
- `STAGE_2_ACCEPTED` is recorded;
- `STAGE_2_KNOWLEDGE_LOCKED` is recorded;
- `READY_FOR_POST_STAGE_2_OMP_CONTINUATION` is recorded;
- Canonical Reference synchronization result is recorded as `CANONICAL_REFERENCE_VERIFIED_UP_TO_DATE` or `CANONICAL_REFERENCE_UPDATED`;
- SYSTEM_MAP synchronization result is recorded as `SYSTEM_MAP_VERIFIED_UP_TO_DATE` or `SYSTEM_MAP_UPDATED`;
- Current Program State is updated;
- OMP receives the new Knowledge Baseline;
- Architecture Review is PASS;
- Quality Review is PASS;
- Self Review is PASS;
- Stage 2 terminal program state is `LOCKED`.

## Program Closure

After `STAGE_2_KNOWLEDGE_LOCKED`, Stage 2 must close in this exact order:

1. Canonical Synchronization.
2. Check whether Canonical Reference changed.
3. If Canonical Reference has no changes, record `CANONICAL_REFERENCE_VERIFIED_UP_TO_DATE`.
4. If Canonical Reference has changes, update Canonical Reference and record `CANONICAL_REFERENCE_UPDATED`.
5. Check whether SYSTEM_MAP changed.
6. If SYSTEM_MAP has no changes, record `SYSTEM_MAP_VERIFIED_UP_TO_DATE`.
7. If SYSTEM_MAP has changes, update SYSTEM_MAP and record `SYSTEM_MAP_UPDATED`.
8. Update Current Program State.
9. Record the new Knowledge Baseline.
10. Transfer control to OMP.
11. Record `ACTIVE_PROGRAM = OMP`.
12. Record `PROGRAM_STATE = CLOSED`.

Closure outputs:

```text
CANONICAL_SYNCHRONIZATION_COMPLETE
CANONICAL_REFERENCE_VERIFIED_UP_TO_DATE | CANONICAL_REFERENCE_UPDATED
SYSTEM_MAP_VERIFIED_UP_TO_DATE | SYSTEM_MAP_UPDATED
CURRENT_PROGRAM_STATE_UPDATED
KNOWLEDGE_BASELINE_RECORDED
ACTIVE_PROGRAM = OMP
PROGRAM_STATE = CLOSED
```

Program Closure cannot change Stage 2 architecture, reopen Stage 1, add domains, create owners, create Runtime, create Planner, create Authority, create OMP, change production routing, or move users.

## Knowledge Consumption Law

After `LOCKED_KNOWLEDGE`, all future engineering processes must use:

```text
docs/reference/V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md
```

as the primary source of engineering knowledge.

Mandatory consumers:

- Discovery;
- Architecture Review;
- OMP;
- Implementation;
- Certification;
- Engineering Automation;
- Future Architecture Evolution.

Consumption rules:

- When locked knowledge contains the required knowledge, repeated extraction from Stage 1 reports is forbidden.
- Existing locked knowledge is consumed directly from `V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md`.
- Reports remain provenance and evidence, not the primary engineering memory after lock.
- New or changed knowledge enters only through the Knowledge Evolution Law.

## Knowledge Evolution Law

After `LOCKED_KNOWLEDGE`, manual editing of engineering memory is forbidden.

Every knowledge change follows this lifecycle:

```text
Knowledge Change Request
  -> Evidence
  -> Review
  -> Acceptance
  -> Knowledge Update
  -> Knowledge Lock
  -> LOCKED_KNOWLEDGE vNext
```

Allowed terminal states:

| Terminal state | Meaning |
| --- | --- |
| `LOCKED_KNOWLEDGE_VNEXT` | Change accepted, updated, and locked. |
| `REJECTED_NO_EVIDENCE` | Change rejected because evidence is missing. |
| `REJECTED_CONFLICTS_WITH_LOCKED_ARCHITECTURE` | Change rejected because it would alter locked architecture. |
| `REJECTED_DUPLICATE_KNOWLEDGE` | Change rejected because locked knowledge already contains it. |
| `SUPERSEDED_BY_NEW_TERMINAL_EVIDENCE` | Existing knowledge remains provenance and the new terminal state becomes current truth. |
| `MANUAL_REVIEW_REQUIRED` | Change is blocked until bounded review reaches an allowed terminal state. |

Knowledge Evolution cannot create a new Runtime, Planner, Authority, OMP, architecture domain, owner, roadmap, or truth source.

## End-To-End Lifecycle Closure Review

Stage 2 is a closed finite program only when all checks pass:

| Check | Required result |
| --- | --- |
| Every stage has input | PASS |
| Every stage has output | PASS |
| Every stage output is consumed by the next stage | PASS |
| No dangling artifacts exist | PASS |
| No unused terminal results exist | PASS |
| No stage lacks a consumer | PASS |
| No stage lacks a producer | PASS |
| No dead ends exist before `LOCKED` | PASS |
| No cycles exist in the official Stage 2 route | PASS |
| No ambiguous transitions exist | PASS |
| Program Closure hands control to OMP | PASS |

Closure chain:

```text
Program Inputs
  -> Stage 2.1 Source Registry / Candidate Registry / Extraction Queue
  -> Stage 2.2 Extracted Knowledge Registry
  -> Stage 2.3 Deduplicated Knowledge Registry
  -> Stage 2.4 Knowledge Graph
  -> Stage 2.5 V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md
  -> docs/reports/research/V7_STAGE2_6_KNOWLEDGE_ACCEPTANCE.md
  -> docs/reports/research/V7_STAGE2_7_KNOWLEDGE_LOCK.md
  -> LOCKED_KNOWLEDGE
  -> Program Closure
  -> OMP Continuation
```

## Final Program Consistency Review

Final consistency requires all checks to pass:

| Check | Required result |
| --- | --- |
| No duplicate rules | PASS |
| No duplicate responsibilities | PASS |
| No duplicate owners | PASS |
| No artifacts without Producer | PASS |
| No artifacts without Consumer | PASS |
| No artifacts without Owner | PASS |
| No artifacts without Acceptance | PASS |
| No artifacts without Terminal State | PASS |
| No dead ends | PASS |
| No cycles | PASS |
| No ambiguous transitions | PASS |
| No ambiguous owners | PASS |
| No ambiguous laws | PASS |
| No ambiguous schema interpretation | PASS |
| Logical Schema and Physical Schema are both defined | PASS |
| Deterministic Resolution has exactly one official path per resolved field | PASS |
| Normalized artifacts do not require denormalization when logical schema is complete | PASS |
| Discovery Index Model is defined as navigation-only | PASS |
| Discovery Indexes do not become Canonical Source, Evidence, Historical Source, or Knowledge Object | PASS |
| Function Graph Appendix pinning is defined when artifacts exist | PASS |
| Stage 2.2 has one official Extraction Lifecycle | PASS |
| Stage 2.2 object creation is deterministic | PASS |
| Knowledge Object remains the minimum engineering knowledge unit | PASS |
| Atomicity Test defines one-object versus multiple-object creation | PASS |
| Knowledge Object Verification gates Extracted Knowledge Registry admission | PASS |
| No competing lifecycles | PASS |

Consistency failure state:

```text
PROGRAM_CONSISTENCY_HOLD
```

`PROGRAM_CONSISTENCY_HOLD` blocks Stage 2 continuation until the failing rule, owner, artifact, transition, or lifecycle is corrected and revalidated.

## 15. Stage 2 Reviews

Every Stage 2 stage must complete three reviews before acceptance.

### Architecture Review

Questions:

- Did the stage preserve locked Stage 1 architecture?
- Did it avoid new domains?
- Did it avoid owner duplication?
- Did it preserve Authority, Runtime, Planner, Diagnosis, Verification, Rollback / Closure, Learning, OMP, and Current Program State boundaries?
- Did it avoid promoting evidence reports into canonical owners?

### Quality Review

Questions:

- Are sources traceable?
- Are owners resolved?
- Are trust levels explicit?
- Are terminal states explicit?
- Are provenance chains clear?
- Are destinations and consumers defined?
- Are risks classified?

### Self Review

Questions:

- Did the stage do only its declared work?
- Did it avoid extraction during inventory?
- Did it avoid deduplication during extraction?
- Did it avoid canonicalization before acceptance?
- Did it preserve history without treating history as current truth?
- Is the next stage unblocked only by a valid acceptance gate?

## 16. Stage 2 Program Acceptance

Program Acceptance is the verifiable acceptance of the Stage 2 governing program.

This program is accepted as the governing Stage 2 program only when all acceptance criteria are true:

- it starts from `STAGE_1_LOCKED`;
- it defines `LOCKED_KNOWLEDGE` as the Stage 2 terminal result;
- it preserves `LOCKED_ARCHITECTURE`;
- it defines Stage 2.1 through Stage 2.7;
- it gives Stage 2.1 a complete inventory lifecycle;
- it requires source classification, trust levels, owners, terminal states, candidate discovery, extraction queue, validation, and inventory report;
- it defines acceptance gates for later stages;
- it requires Architecture Review, Quality Review, and Self Review;
- it creates no new architecture, owner, Runtime, Planner, Authority, OMP, roadmap, or truth source;
- it defines Program Inputs and Program Outputs;
- it defines Program Start Model through Program State, Current Program State, and OMP;
- it defines Stage Input / Output Contracts;
- it defines Failure Recovery Model;
- it defines Program Closure;
- it defines Knowledge Consumption Law;
- it defines Knowledge Evolution Law;
- it passes End-To-End Lifecycle Closure Review;
- it defines Program Governance;
- it defines Program Producer / Consumer Model;
- it defines Program Execution Law;
- it defines Output Verification Law;
- it defines Traceability Law;
- it defines No Orphan Artifact Law;
- it passes Final Program Consistency Review;
- it defines Discovery Exhaustion Criteria;
- it defines Discovery Index Model;
- it defines Discovery Index Family;
- it pins Function Graph Appendix `.md` and `.json` as mandatory Discovery Indexes when present;
- it defines Storage Location Completeness;
- it defines Role Separation Law;
- it defines Verification Evidence Law;
- it defines Knowledge Candidate Registry schema;
- it defines Logical Schema Law;
- it defines Deterministic Resolution Law;
- it defines Normalized Artifact Law;
- it defines Stage 2.2 Extraction Unit;
- it defines Stage 2.2 Extraction Lifecycle;
- it defines Knowledge Object Creation Rules;
- it defines Knowledge Object Atomicity Test;
- it defines Stage 2.2 Atomicity Review;
- it defines Object Splitting Rule;
- it requires Knowledge Object Verification before Extracted Knowledge Registry admission;
- it defines Extraction Determinism;
- it requires Acceptance to verify Logical Completeness rather than Physical Completeness;
- it defines Not Applicable Law;
- Stage 2 Definition Of Done requires `STAGE_2_PROGRAM_ACCEPTED`.

Acceptance Rule:

Stage 2 acceptance gates must verify logical completeness.

Acceptance must not require all required fields to be physically duplicated in one record when:

- the required field is stored directly in the record; or
- the required field is deterministically resolved through exactly one official Stage 2 artifact; and
- the Resolution Path is recorded; and
- no ambiguity, conflict, or cyclic dependency exists.

Acceptance must return `FAIL` when:

- a required field is missing and cannot be resolved;
- more than one official path resolves the value ambiguously;
- a direct value conflicts with a resolved value;
- a Resolution Path relies on a non-official artifact;
- normalization hides a new owner, truth source, extraction step, or acceptance gate.

Acceptance may return `HOLD` when a bounded manual review is required to choose or record the official Resolution Path without changing architecture.

Program Acceptance output:

```text
STAGE_2_PROGRAM_ACCEPTED
```

Program Acceptance is not the final Stage 2 verdict.
It accepts the governing program so Stage 2.1 can execute under this program.

## 17. Program Self Review

Architecture Review:

PASS.

This program does not redesign architecture, add domains, change owners, change Runtime, change Planner, change Authority, change OMP, or alter production behavior.

Quality Review:

PASS.

The program defines source classification, trust classification, terminal-state resolution, knowledge object schema, candidate registry, extraction queue, deterministic extraction lifecycle, knowledge object verification, validation gates, required reports, and acceptance reviews.

Self Review:

PASS.

The program separates inventory, extraction, deduplication, graphing, canonicalization, acceptance, and lock. It explicitly prevents Stage 2.1 from extracting or merging knowledge, prevents Stage 2.2 from deduplicating or canonicalizing knowledge, and prevents superseded states from becoming active truth.

Update Review:

PASS.

The added completion criteria, state machine, deliverables, Definition of Done, and metrics improve execution control and measurability without changing Stage 2 architecture, route, stages, acceptance gates, Knowledge Object Model, Source Classification Model, Terminal State Law, boundaries, or review definitions.

Final Update Review:

PASS.

The added Program Invariants, Stage Transition Law, Stage Input / Output Contracts, Failure Recovery Model, and Program Closure strengthen execution discipline without changing Stage 2 architecture, route, stages, boundaries, Knowledge Object Model, Source Classification Model, Terminal State Law, Reviews, or Acceptance Gates.

Architecture Refinement Review:

PASS.

Program Start Model, Program Input / Output Contract, Program Acceptance, Knowledge Consumption Law, Knowledge Evolution Law, and End-To-End Lifecycle Closure Review close remaining lifecycle gaps without changing Stage 2 architecture or acceptance gates.

Program Closure Review:

PASS.

Program Closure produces deterministic synchronization results, updates Current Program State, records the Knowledge Baseline, transfers control to OMP, and terminates with `PROGRAM_STATE = CLOSED`.

State Machine Review:

PASS.

The program has one official route, one stage lifecycle, explicit allowed transitions, explicit forbidden transitions, and no stage-skipping path.

End-to-End Lifecycle Review:

PASS.

Every stage has input, output, producer, consumer, accepted transition, and downstream use. The final consumer is OMP continuation after `LOCKED_KNOWLEDGE`.

Governance Review:

PASS.

Every program role has responsibilities, produces, consumes, authority, and outputs. No responsibility remains ownerless.

Producer / Consumer Review:

PASS.

Every program artifact has producer, consumer, owner, acceptance, terminal state, and storage location.

Traceability Review:

PASS.

Every Stage 2 artifact traces Stage -> Inputs -> Outputs -> Producer -> Consumer -> Evidence -> Acceptance -> Terminal State.

Lifecycle Review:

PASS.

The official lifecycle remains linear from Program Inputs through OMP Continuation, with no alternate route.

Consistency Review:

PASS.

No duplicate rule, duplicate responsibility, duplicate owner, orphan artifact, dead end, cycle, ambiguous transition, ambiguous owner, ambiguous law, or competing lifecycle remains.

Verification Review:

PASS.

Every verification requires a stored Verification Result in the engineering report for the current stage. Missing Verification Result means `FAIL`.

Discovery Review:

PASS.

Stage 2.1 completes discovery only after Discovery Exhaustion Criteria pass.
Discovery Indexes are checked as navigation layers, not as canonical truth.
Function Graph Appendix `.md` and `.json` are mandatory Discovery Index artifacts when present.

Source Classification Review:

PASS.

Discovery Index is a separate discovery-source family and does not replace Source Classification Model.
Discovery Indexes do not become Canonical Sources, Historical Sources, Evidence, or Knowledge Objects.
Any knowledge candidate found through a Discovery Index must still resolve to an official Source, owner, trust level, terminal state, and destination.

Schema Review:

PASS.

Knowledge Candidate Registry has a required logical schema and incomplete candidates cannot enter the extraction queue.
Required fields may be stored directly or deterministically resolved through official Stage 2 artifacts.
Acceptance verifies logical completeness rather than physical field co-location.

Logical Schema Review:

PASS.

Logical Schema Law, Deterministic Resolution Law, Normalized Artifact Law, and Traceability Law now define a single interpretation of schema completeness.
Physical schema is permitted but not required.
Normalized Stage 2 artifacts are valid when every required field has a unique direct value or unique Resolution Path.
Ambiguous, missing, conflicting, or cyclic resolution remains `FAIL`.

Extraction Review:

PASS.

Stage 2.2 now defines one extraction unit, one extraction lifecycle, deterministic candidate dispositions, Knowledge Object Creation Rules, and the required verification sequence before Extracted Knowledge Registry admission.
The refinement explains how extraction is performed without changing the Stage 2 route, creating a second extraction program, or moving deduplication, graph, canonicalization, acceptance, or lock responsibilities into Stage 2.2.

Knowledge Object Review:

PASS.

The Knowledge Object Model remains unchanged.
Every created object must satisfy the existing schema and must pass verification for Schema, Source, Trust Level, Terminal State, Owner, Consumer, Provenance, Destination, Forbidden Misuse, Review State, and Atomicity before registry admission.
Objects with missing, conflicting, or ambiguous mandatory elements cannot enter the Extracted Knowledge Registry.

Atomicity Review:

PASS.

Knowledge Object remains the minimum engineering knowledge unit in Stage 2.
No Knowledge Atom, new entity, new stage, alternate schema, alternate lifecycle, or alternate model was introduced.
Stage 2.2 now deterministically decides `ONE_OBJECT_CREATED` versus `MULTIPLE_OBJECTS_CREATED` through Atomicity Test, Atomicity Review, Object Splitting Rule, Deterministic Resolution Law, Traceability Law, and Knowledge Object Verification.

Program Consistency Review:

PASS.

The logical schema refinement, Discovery Index integration, extraction refinement, and atomicity refinement strengthen existing discovery, verification, traceability, schema, extraction, object creation, and acceptance mechanisms without changing the Stage 2 route, stages, acceptance gates, Knowledge Object Model, Source Classification Model, Terminal State Law, boundaries, reviews, or architecture.
Stage 2.2 has one official deterministic extraction lifecycle and no competing extraction lifecycle.

Program Refinement Audit:

PASS.

The final engineering refinements strengthen existing mechanisms without changing architecture, route, stages, boundaries, models, reviews, or acceptance gates.

## Stage 2 Definition Of Done

Stage 2 is fully complete only when all of these conditions are true at the same time:

- `STAGE_2_PROGRAM_ACCEPTED` is recorded;
- `LOCKED_KNOWLEDGE` is created;
- `docs/reference/V7_CANONICAL_ARCHITECTURE_KNOWLEDGE.md` is accepted;
- Knowledge Graph is accepted;
- all P0 Knowledge Objects are processed;
- all P1 Knowledge Objects are processed or have acceptable bounded `MANUAL_REVIEW`;
- Knowledge Acceptance verdict is PASS;
- Knowledge Lock verdict is PASS;
- Canonical Reference synchronization result is recorded as `CANONICAL_REFERENCE_VERIFIED_UP_TO_DATE` or `CANONICAL_REFERENCE_UPDATED`;
- SYSTEM_MAP synchronization result is recorded as `SYSTEM_MAP_VERIFIED_UP_TO_DATE` or `SYSTEM_MAP_UPDATED`;
- Current Program State is updated;
- OMP receives the new Knowledge Baseline;
- Stage 2 metrics are reported;
- no Stage 2 boundary was violated;
- no architecture change was introduced;
- no new Runtime, Planner, Authority, OMP, architecture domain, owner, roadmap, or truth source was created.

## 18. Final Program Verdict

```text
V7_STAGE2_KNOWLEDGE_ENGINEERING_PROGRAM_CREATED
STAGE_2_PROGRAM_READY
NEXT_STAGE = STAGE_2_1_KNOWLEDGE_INVENTORY
```
