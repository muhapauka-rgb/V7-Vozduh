# V7 Document Lifecycle

Status: canonical
Owner: OMP
Need New Owner: FALSE

## Purpose

This document defines the permanent role of every V7 document class.

It eliminates document-driven planning drift by making one rule explicit:

```text
Only docs/programs/V7_IMPLEMENTATION_BACKLOG.md drives engineering work.
Everything else is knowledge, execution state, evidence, or decisions.
```

This document does not redesign architecture, OMP, Runtime, Planner, Governance, execution, truth, policy, or implementation owners.

## Class 1: Reference

Purpose: permanent knowledge.

Examples:

- `docs/reference/V7_SYSTEM_ARCHITECTURE.md`;
- `docs/reference/V7_RUNTIME_MODEL.md`;
- `docs/reference/V7_DECISION_MODEL.md`;
- `docs/reference/V7_KERNEL.md`;
- `docs/reference/V7_CONTEXT_RESOLVER.md`;
- `docs/reference/V7_DOCUMENT_LIFECYCLE.md`;
- `docs/policies/`.

Rules:

1. Reference documents are frozen after certification.
2. The Canonical Policy Library is frozen after Stage 4 V7 Fit Analysis.
3. Changes are allowed only when:
   - industry consensus changes;
   - a real implementation proves `FUNDAMENTAL_ARCHITECTURE_GAP`;
   - the operator explicitly requests a reference update.
4. OMP must not edit reference documents during normal implementation.
5. Reference documents may explain, constrain, or verify work.
6. Reference documents must not act as implementation queue, roadmap, or current task list.

## Class 2: Programs

Purpose: drive execution.

Examples:

- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`;
- `docs/programs/V7_IMPLEMENTATION_PROGRAM.md`;
- `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

Rules:

1. Program documents are live.
2. They may be updated continuously when execution state, scheduler meaning, optimizer meaning, or volatile current state changes.
3. They must not accumulate historical design content.
4. OMP remains the permanent production operating program.
5. Current Program State carries volatile state.
6. V7 Implementation Program remains a supporting implementation reference under OMP, not an independent roadmap.

## Class 3: Implementation

Purpose: the only implementation queue.

Examples:

- `docs/programs/V7_IMPLEMENTATION_BACKLOG.md`;
- `docs/reference/V7_IMPLEMENTATION_PRIORITY_MODEL.md`.

Rules:

1. OMP always selects engineering work only from `docs/programs/V7_IMPLEMENTATION_BACKLOG.md`.
2. `docs/reference/V7_IMPLEMENTATION_PRIORITY_MODEL.md` defines how the backlog is ranked; it is not a second queue.
3. No implementation planning may live in reports, policies, ADRs, architecture, research documents, or product documents.
4. When a task finishes:

```text
DONE
  -> Recalculate backlog
  -> Update Current Program State
  -> Update OMP
  -> Continue
```

5. When the backlog becomes empty, OMP must answer:

```text
IMPLEMENTATION_COMPLETE
```

and stop.

## Class 4: Reports

Purpose: historical evidence only.

Rules:

1. Reports are read-only evidence.
2. Reports must never be used as planning queue.
3. Reports must never be used as roadmap.
4. Reports must never generate implementation tasks directly.
5. Reports may be loaded only when evidence is explicitly required.
6. If evidence in a report changes system truth, the truth must be promoted through Canonical Reference, SYSTEM_MAP, ADR, OMP, or backlog as appropriate.

## Class 5: ADR

Purpose: permanent decisions.

Rules:

1. ADRs are read-only after acceptance.
2. ADRs must never be used as implementation queue.
3. ADRs may explain why a decision exists.
4. ADRs may constrain future implementation.
5. ADRs do not replace OMP or the Implementation Backlog.

## OMP Selection Rule

OMP must never ask:

```text
What should I implement?
```

OMP must always read:

```text
Highest unfinished backlog item
```

Source order for implementation selection:

```text
OMP
  -> Current Program State
  -> V7_IMPLEMENTATION_BACKLOG
  -> V7_IMPLEMENTATION_PRIORITY_MODEL
  -> Implement or stop
```

Forbidden implementation sources:

- reports;
- policy documents;
- architecture documents;
- research documents;
- ADRs;
- product documents;
- chat history;
- old roadmaps.

## OMP Status Rule

OMP status must always display backlog progress:

```text
Tier A: complete / total
Tier B: complete / total
Tier C: complete / total
Tier D: optional complete / optional total
Overall: complete / actionable total
Implementation maturity: percent
Estimated remaining effort
Next item
```

The current initial status is:

```text
Tier A: 0 / 6 complete
Tier B: 0 / 20 complete
Tier C: 0 / 7 complete
Tier D: 0 / 6 optional complete
Overall: 0 / 33 actionable complete
Implementation maturity: 0%
Estimated remaining effort: Moderate
Next item: A1
```

## Lifecycle Verdict

There is one live engineering queue:

```text
docs/programs/V7_IMPLEMENTATION_BACKLOG.md
```

Need New Owner: `FALSE`.

Runtime mutation enabled: `NO`.

Runtime apply enabled: `NO`.

User movement enabled: `NO`.

Authority expansion enabled: `NO`.
