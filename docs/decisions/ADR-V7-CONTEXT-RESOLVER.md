# ADR-V7 Context Resolver

Status: Accepted
Date: 2026-06-25
Program: `V7.CONTEXT.RESOLVER`

## Context

V7 has accumulated many canonical documents, ADRs, reports, runtime tools, packet previews, and handoff files.

Loading the whole project into an LLM context window is unsafe and unnecessary. It creates context-window overflow risk, mixes volatile packet state into research tasks, mixes research/history into runtime execution tasks, and can make future Codex sessions act on stale or unrelated information.

Existing mechanisms already define parts of the answer:

- Kernel defines source hierarchy and operating contract.
- OMP defines semantic reuse, no duplication, authority boundaries, and continuation rules.
- Canonical Reference defines Reference First.
- SYSTEM_MAP defines current owners.
- Current Program State isolates volatile state from stable rules.

These mechanisms are sufficient ownership. V7 does not need a new runtime owner, planner, governance layer, execution path, truth source, storage layer, or daemon.

## Decision

Context must be loaded by task-specific working set instead of loading the whole project.

Before every task, Codex must:

1. classify the task;
2. resolve the minimum working document set;
3. load only those documents;
4. execute the task;
5. unload unrelated context.

The canonical rule lives in `docs/reference/V7_CONTEXT_RESOLVER.md`.

## Consequences

- Future Codex sessions can start with only the documents selected by Context Resolver.
- Research tasks must not load packet state, current metrics, or current HLA.
- Execution tasks must not load research reports or historical reports unless directly required.
- Architecture tasks must load owner/truth documents and relevant ADRs, not volatile packet state.
- Documentation tasks must load the target document and minimal governing references.
- Historical reports remain evidence, not default context.
- Runtime truth/convergence remain verification surfaces, not always-loaded context.

## Semantic Reuse Result

| Field | Result |
| --- | --- |
| Existing semantic coverage | `70%` |
| Existing owners reused | Kernel, OMP, Canonical Reference, SYSTEM_MAP, ADRs |
| Missing behavior | Task classification, working-set matrix, maximum context rules |
| Need New Owner | `FALSE` |
| Decision | `EXTEND_DOCUMENTATION_ONLY` |

## Duplicate Detector

| Area | Verdict |
| --- | --- |
| Duplicate planner | `NONE` |
| Duplicate governance | `NONE` |
| Duplicate execution | `NONE` |
| Duplicate truth source | `NONE` |
| Duplicate evidence collector | `NONE` |
| Duplicate runtime owner | `NONE` |
| Duplicate context-loading rule | `NONE` |
| Final verdict | `NONE` |

## Safety

This ADR does not:

- create a planner;
- create governance;
- create execution;
- create a truth source;
- create synthetic evidence;
- change runtime behavior;
- lower floors;
- authorize restore-barrier writes;
- authorize apply;
- move users.
