# V7 Context Resolver

Status: canonical

## Purpose

Codex must load only the documents required for the current task.

Never load the whole project.

The Context Resolver is a documentation/control-plane rule. It is not a planner, governance layer, execution path, truth source, daemon, storage layer, or runtime authority.

The Engineering Context Resolver (ECR) is the engineering-grade operating form of this same resolver. It is not a new subsystem, owner, truth source, audit system, roadmap, or backlog. It materializes the existing Context Resolver, Knowledge Plane, OMP, Canonical Reference, SYSTEM_MAP, Current Program State, and Implementation Backlog into one mandatory pre-workflow for engineering tasks.

ECR answers before work begins:

1. What knowledge is required?
2. What knowledge is already verified?
3. What knowledge is current?
4. What knowledge is historical evidence only?
5. What knowledge must be refreshed?
6. What knowledge can be ignored?
7. Which existing owner and backlog item apply?
8. Whether re-open, implementation, certification, or runtime investigation is required.

## Working Set Principle

```text
Task
  -> Context Resolver
  -> Required Documents
  -> Execute
  -> Unload
```

Working set means the smallest document set needed to answer or implement the current task safely.

Unload means do not continue relying on unrelated documents, packet state, reports, or historical context after the task-specific work is complete.

## Document Classes

| Class | Documents | Use |
| --- | --- | --- |
| Permanent | `docs/reference/V7_KERNEL.md`, `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` | Operating contract and scheduler/optimizer rules. |
| Volatile | `docs/programs/V7_CURRENT_PROGRAM_STATE.md` | Current bottleneck, HLA, packet, authority boundary, metrics, and stop reason. |
| Truth | `docs/reference/V7_CANONICAL_REFERENCE.md`, `docs/reference/SYSTEM_MAP.md` | Current system meaning and owner/topology map. |
| Decisions | `docs/decisions/*.md` | Accepted decisions relevant to the task. |
| Evidence | `docs/reports/*.md` | Historical evidence; load only when directly required. |
| Runtime | `tools/v7-truth-check --all --json`, `tools/v7-convergence-status --json` | Reality and final verification. |

## Automatic Rule

Before every task:

1. Classify the task.
2. Resolve the working set.
3. Load only required documents.
4. Execute.
5. Unload unrelated context.

If the task type is ambiguous, choose the smaller safe working set first and expand only when a required answer is missing.

## Engineering Context Resolver

Status: `OPERATIONAL`

Purpose: determine the minimum authoritative engineering context before any V7 engineering task starts.

Canonical ECR pipeline:

```text
Task
  -> Task Classification
  -> Context Resolution
  -> Knowledge Consumption
  -> Implementation or Audit
  -> Verification
  -> Certification when required
  -> Engineering Report
  -> Canonical Update when durable knowledge changes
  -> Knowledge State Update
  -> Current Program State Update
  -> OMP Continue
```

ECR consumes Knowledge Plane but does not replace it:

```text
Product Specification
  -> Audit Knowledge State
  -> Canonical Reference
  -> Current Program State
  -> OMP
  -> Implementation Backlog
  -> Task-specific owners only
```

Engineering context questions:

| Question | Existing owner used by ECR |
| --- | --- |
| What is the product meaning? | Product Specification. |
| Is this already known? | Canonical Reference + SYSTEM_MAP + Audit Knowledge State. |
| Is it still current? | Current Program State + Knowledge Quality/Freshness owners + truth/convergence when needed. |
| Is it historical only? | Engineering Reports lifecycle. |
| Does a re-open trigger apply? | OMP + Canonical Reference + relevant owner re-audit rules. |
| Is implementation required? | OMP + Implementation Backlog. |
| Is certification required? | OMP + Production Maturity Model + relevant policy/capability. |
| Is runtime investigation required? | Runtime Model + existing runtime owner + Current Program State. |
| Which context can be ignored? | Context Resolver maximum context rules + task-class matrix. |

## Task Classes

Every task must be classified before context is loaded.

| Task class | Mandatory context | Optional context | Must not read by default | Authoritative owners |
| --- | --- | --- | --- | --- |
| Architecture | Product Specification; Canonical Reference; SYSTEM_MAP; Architecture Closed by Default rule. | System Architecture / Runtime Model only if the question is not already answered. | Historical reports; packet state; current metrics unless contradiction requires them. | Product Specification; Canonical Reference; SYSTEM_MAP; System Architecture. |
| Knowledge | Product Specification; Canonical Reference; SYSTEM_MAP; Knowledge Plane / Audit Knowledge State; OMP report lifecycle. | Knowledge Quality Model; relevant reports as evidence only. | Runtime apply paths; packet previews; unrelated policy research. | Canonical Reference; SYSTEM_MAP; Knowledge Quality Model; OMP. |
| Product | Product Specification; Canonical Reference; SYSTEM_MAP. | OMP / policies only when product meaning affects execution. | Runtime internals; implementation files; historical reports unless evidence is needed. | Product Specification. |
| Policy | Product Specification; Canonical Policy Library; Canonical Reference; SYSTEM_MAP; OMP. | Relevant ADRs; relevant policy reports as evidence. | Runtime apply code; packet state unless operational policy requires it. | Canonical Policy Library; OMP. |
| Implementation | Product Specification; Audit Knowledge State; Canonical Reference; Current Program State; OMP; Implementation Backlog; current backlog item. | Relevant Runtime Model / owner files only for the selected backlog item. | Full project; unrelated reports; architecture research. | OMP; Implementation Backlog; specific code owner. |
| Runtime | Runtime Model; Current Program State; Canonical Reference; SYSTEM_MAP; relevant runtime owner. | Relevant runtime reports; truth/convergence; packet/lease state only if current task needs it. | Research reports; product rewrites; unrelated backlog. | Runtime Model; existing runtime owner; OMP. |
| Production | Current Program State; OMP; Production Maturity Model; truth/convergence; relevant safe deploy / production evidence owner. | Safe deploy reports; production outcome reports. | Architecture research; policy world research; implementation files unless production issue maps there. | OMP; Production Maturity Model; Current Program State. |
| Certification | OMP; Current Program State; Production Maturity Model; relevant capability/policy; evidence owner. | Certified reports; truth/convergence; tests. | Unrelated reports; runtime apply unless certification explicitly covers production action. | OMP; Production Maturity Model; relevant capability owner. |
| Audit | Audit Knowledge State; Canonical Reference; SYSTEM_MAP; OMP; relevant canonical owner. | Historical reports as evidence only. | Implementation files before architectural intent is established; unrelated reports. | Canonical Reference; SYSTEM_MAP; OMP. |
| Scale | Product Scale Model/Objectives; Production Scale First; OMP; Canonical Reference; SYSTEM_MAP. | Runtime Model / read-model owners if scale affects runtime or UI. | Packet state; production apply paths; unrelated reports. | Product Specification; OMP; Canonical Reference. |
| Bug | Current Program State; OMP Root Cause Engine; relevant owner map; relevant code owner; tests. | Runtime Model if runtime-relevant; reports for reproduction evidence. | Architecture redesign; new owners; unrelated backlog. | Existing code owner; OMP; Current Program State. |
| Investigation | Product Specification; Canonical Reference; SYSTEM_MAP; Current Program State if current behavior matters; relevant owner. | Reports as evidence only; implementation files after owner mapping. | Full project scan; unrelated historical research. | Existing mapped owner. |
| Operator Request | Product Specification; Current Program State; OMP; Canonical Reference. | Runtime Model / packet state only if the request concerns production action. | Research reports; full project; unrelated code. | OMP; Current Program State; Product Specification. |
| Research | Research Framework; Context Resolver; Engineering Principles; relevant canonical owner; relevant ADRs. | External sources only when explicitly research; prior reports as evidence. | Current packet/HLA/metrics; runtime apply paths; production state unless research requires it. | Research Framework; Canonical Reference; SYSTEM_MAP. |

## Task Examples

### Continue OMP

Meaning:

`Continue OMP` executes the complete Engineering Control Loop, not only backlog continuation.

Read:

- Product Specification;
- Audit Knowledge State;
- Canonical Reference;
- SYSTEM_MAP when ownership/topology mapping is needed;
- Current Program State;
- OMP;
- current Backlog item.

Then resolve:

- task class;
- existing owner;
- whether knowledge is already verified;
- whether knowledge is still current;
- whether a re-open trigger fired;
- current highest production-leverage action;
- stop or continue condition.

Nothing else unless OMP maps the current item to a specific owner, Runtime relevance is proven, or a re-open trigger fires.

### Runtime Bug

Read:

- Runtime Model;
- Current Program State;
- Canonical Reference;
- SYSTEM_MAP;
- relevant runtime owner;
- relevant runtime report only as evidence.

Do not read architecture research or unrelated reports.

### Architecture Question

First ask:

```text
Architecture already VERIFIED?
```

If yes, read:

- Product Specification;
- Canonical Reference;
- SYSTEM_MAP.

Do not perform a new architecture audit unless a re-open trigger fires.

## Re-open Logic

ECR must determine:

| Question | Output |
| --- | --- |
| Already verified? | `YES`, `NO`, or `UNKNOWN`. |
| Still current? | `CURRENT`, `STALE_RECHECK_REQUIRED`, `HISTORY_ONLY`, or `UNKNOWN`. |
| Re-open trigger fired? | `TRUE` / `FALSE`, with owner and reason. |
| Implementation required? | Existing backlog item or `NO`. |
| Certification required? | Existing capability/policy/certification path or `NO`. |
| Runtime investigation required? | Existing runtime owner or `NO`. |

Re-open triggers:

- product meaning changed;
- runtime model changed;
- canonical policy changed;
- implementation changed material behavior;
- production evidence contradicted canonical knowledge;
- Product Scale Model changed;
- operator explicitly requested re-open;
- durable knowledge was found only in reports/chat/temp output.

## Read Minimization

ECR optimizes:

- token usage;
- human reading;
- runtime;
- engineering time;
- correctness.

Rules:

1. Read the minimum authoritative owner set.
2. Read historical reports only as evidence.
3. Do not load the whole project.
4. Do not load implementation files until owner mapping requires them.
5. Do not load runtime/packet state unless the task is runtime, production, execution, authority, or current-state specific.
6. Do not load architecture/research material for normal implementation unless a re-open trigger proves it is needed.
7. Expand context only when the current owner cannot answer safely.

## Automatic Canonical Update

After every meaningful step:

```text
Engineering Report
  -> Knowledge Extraction
  -> Canonical Update if durable knowledge changed
  -> Audit Knowledge State Update
  -> Current Program State Update when current state changed
  -> OMP Continue
```

Durable knowledge must never remain only in the engineering report.

## Loading Rules

### Research Task

Load:

- `docs/reference/V7_KERNEL.md`
- `docs/reference/V7_ENGINEERING_PRINCIPLES.md`
- `docs/reference/V7_AUTONOMY_BLUEPRINT.md`
- `docs/reference/V7_DECISION_MODEL.md`, if it exists or is the active target
- relevant ADRs

Do NOT load:

- packet state
- current metrics
- current HLA
- execution packet previews

### Execution Task

Load:

- `docs/reference/V7_KERNEL.md`
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
- relevant execution ADRs

Do NOT load:

- research reports
- Cisco/control-plane research
- historical reports unless they are required to resolve a current contradiction

### Architecture Task

Load:

- `docs/reference/V7_KERNEL.md`
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- relevant ADRs

Do NOT load:

- packet state
- metrics
- research reports unless the architecture question explicitly depends on them

### Documentation Task

Load:

- `docs/reference/V7_KERNEL.md`
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/reference/V7_CANONICAL_REFERENCE.md`
- the relevant target document

Do NOT load anything else unless the target document points to a required source.

## Maximum Context Rule

Never intentionally load unrelated reports.

Never load historical reports unless explicitly required.

Never load packet state for research.

Never load research for runtime execution.

Never load volatile Current Program State unless the task requires current bottleneck, HLA, authority boundary, packet, metrics, or stop reason.

Never load runtime evidence unless verifying truth/convergence or resolving a contradiction between documentation and reality.

## Semantic Reuse Audit

| Field | Current Value |
| --- | --- |
| Desired capability | Prevent future LLM context-window overflow by resolving a minimum working document set before each task. |
| Existing owners found | `docs/reference/V7_KERNEL.md`, `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`, `docs/reference/V7_CANONICAL_REFERENCE.md`, `docs/reference/SYSTEM_MAP.md`, ADRs. |
| Semantically equivalent owners | Kernel source hierarchy, Reference First workflow, OMP semantic reuse/new-owner gate, Kernel/State split. |
| Existing semantic coverage | `70%`: existing sources define order, truth hierarchy, and reuse rules, but not task classification or maximum context rules. |
| Reuse strategy | Reuse Kernel as the operating contract, Canonical Reference as system truth, SYSTEM_MAP as owner map, and ADRs for decision preservation. |
| Extension strategy | Add a canonical documentation-only context resolver and reference it from Kernel, Canonical Reference, SYSTEM_MAP, and ADR. |
| Need New Runtime Owner | `FALSE` |
| Need New Planner | `FALSE` |
| Need New Governance | `FALSE` |
| Need New Execution | `FALSE` |
| Need New Truth Source | `FALSE` |
| Decision | `EXTEND_DOCUMENTATION_ONLY` |

## Duplication Detector

| Area | Verdict |
| --- | --- |
| Duplicate planner | `NONE` |
| Duplicate governance | `NONE` |
| Duplicate execution | `NONE` |
| Duplicate truth source | `NONE` |
| Duplicate evidence collector | `NONE` |
| Duplicate runtime owner | `NONE` |
| Duplicate context-loading rule | `NONE`; existing rules are source-order and reference-first rules, while this file defines task working sets. |
| Final verdict | `NONE` |

## Safety

This resolver does not authorize:

- restore-barrier writes;
- runtime apply;
- user movement;
- rollback apply;
- daemon or timer enablement;
- authority expansion;
- floor changes;
- synthetic evidence;
- new planner, governance, execution, storage, or truth source.
