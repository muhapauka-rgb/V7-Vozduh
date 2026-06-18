# ADR-005 Reference First Rule

Status: Accepted
Date: 2026-06-18
Commit: `a723ccb7`

## Context

V7 now has a canonical knowledge base:

- `docs/reference/V7_CANONICAL_REFERENCE.md`
- `docs/reference/SYSTEM_MAP.md`
- `docs/decisions/`

Before these documents existed, repeated audits rediscovered already-resolved concepts such as Route, Capacity, Channel Score, Health, Planner, Assignment, Service Matrix, Trust, Recovery, and Autonomy.

## Decision

A concept may not be re-audited until Canonical Reference, relevant ADRs, and System Map have been checked.

Required path before launching any audit:

1. Read `docs/reference/V7_CANONICAL_REFERENCE.md`.
2. Read relevant ADRs under `docs/decisions/`.
3. Read `docs/reference/SYSTEM_MAP.md`.
4. Determine whether the answer already exists.

A new audit is allowed only if:

- Reference has no answer.
- Reference explicitly marks the area `UNKNOWN`.
- System behavior changed after the last verified commit.
- Evidence contradicts Canonical Reference.

Otherwise, update the reference if needed and do not create a new audit.

## Alternatives considered

- Continue audit-per-question: rejected because it wastes time and fragments truth.
- Keep reports as the first source: rejected because reports are evidence/history, not current truth.
- Rely on chat memory: rejected because chat memory is not durable project infrastructure.

## Consequences

- Future questions such as "What is Route?", "What is Capacity?", "What is Channel Score?", and "Why is channel overloaded?" must be answered from reference first.
- New audits become exception paths, not the default response.
- Stable audit conclusions must be moved into the canonical reference.
- Architectural decisions must be moved into ADRs.

## Affected modules

- Project workflow
- Documentation workflow
- Audit workflow
- Canonical reference
- ADR system

## Reference updates

- Added Knowledge Preservation Rules to `docs/reference/V7_CANONICAL_REFERENCE.md`.
- Added Reference First Workflow to `docs/reference/SYSTEM_MAP.md`.

## Related reports

- `V7_REFERENCE_1_CANONICAL_KNOWLEDGE_BASE_REPORT.md`
- `REFERENCE_2_REFERENCE_FIRST_RULE_REPORT.md`
