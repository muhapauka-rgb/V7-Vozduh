# ADR-001 Canonical Reference System

Status: Accepted
Date: 2026-06-18
Commit: `8ba2178f`

## Context

V7 knowledge was scattered across chats, audit reports, screenshots, implementation reports, and code. Repeated work re-audited the same concepts: route, capacity, channel score, health, planner decisions, service matrix, assignment, runtime truth, and convergence.

## Decision

Create `docs/reference/V7_CANONICAL_REFERENCE.md` as the current conceptual truth of the system, `docs/reference/SYSTEM_MAP.md` as the compact module map, and `docs/decisions/` as the decision record home.

Future work that changes system meaning must update the reference. If it changes a decision, it must create or update an ADR.

## Alternatives considered

- Keep knowledge only in reports: rejected because reports are evidence/history, not current truth.
- Keep knowledge only in code: rejected because operators and future audits need concept-level meaning.
- Keep knowledge in chat/Codex memory: rejected because it is not durable project infrastructure.

## Consequences

- Future audits should read the canonical reference before re-auditing old concepts.
- Important decisions become reviewable and linkable.
- Documentation must be updated with meaningful logic/UX/governance changes.

## Affected modules

- Documentation workflow
- Audit workflow
- Truth/convergence workflow

## Reference updates

- Created `docs/reference/V7_CANONICAL_REFERENCE.md`
- Created `docs/reference/SYSTEM_MAP.md`

## Related reports

- `V7_REFERENCE_1_CANONICAL_KNOWLEDGE_BASE_REPORT.md`
- `PROGRAM_CONV1_PERMANENT_TRUTH_AND_DEPLOYMENT_CONVERGENCE_SYSTEM_REPORT.md`
- `PROGRAM_Z8_8_TRUTH_MANIFEST_AND_V7_TRUTH_CHECK_IMPLEMENTATION_REPORT.md`
