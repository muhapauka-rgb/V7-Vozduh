# V7 Context Resolver

Status: canonical

## Purpose

Codex must load only the documents required for the current task.

Never load the whole project.

The Context Resolver is a documentation/control-plane rule. It is not a planner, governance layer, execution path, truth source, daemon, storage layer, or runtime authority.

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
