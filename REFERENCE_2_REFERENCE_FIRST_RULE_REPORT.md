# REFERENCE.2 Reference First Rule Report

Date: 2026-06-18
Base commit: `a723ccb7`
Runtime changes: none
Logic changes: none
UI changes: none
Planner/governance/execution changes: none

## 1. Created Files

| File | Purpose |
| --- | --- |
| `docs/decisions/ADR-005-reference-first-rule.md` | Makes Reference First an accepted project decision. |
| `REFERENCE_2_REFERENCE_FIRST_RULE_REPORT.md` | Documents this documentation-only change. |

## 2. Updated Files

| File | Update |
| --- | --- |
| `docs/reference/V7_CANONICAL_REFERENCE.md` | Added Knowledge Preservation Rules and re-audit conditions. |
| `docs/reference/SYSTEM_MAP.md` | Added Reference First Workflow: Question -> Reference -> ADR -> System Map -> Audit only if still needed. |

## 3. Reference First Rule

Before launching any new audit:

1. Read `docs/reference/V7_CANONICAL_REFERENCE.md`.
2. Read relevant ADRs.
3. Read `docs/reference/SYSTEM_MAP.md`.
4. Determine whether the answer already exists.

## 4. Re-Audit Conditions

A new audit is allowed only if:

| Condition | Meaning |
| --- | --- |
| A | Reference has no answer. |
| B | Reference explicitly marks the area `UNKNOWN`. |
| C | System behavior changed after the last verified commit. |
| D | Evidence contradicts Canonical Reference. |

Otherwise, update the reference if needed and do not create a new audit.

## 5. Knowledge Preservation Rules Added

1. No important knowledge may live only in chat.
2. No important knowledge may live only in reports.
3. Stable conclusions must move into Canonical Reference.
4. Architectural decisions must move into ADR.
5. Future audits must read Reference before auditing.

## 6. Success Criteria

Future questions such as:

- What is Route?
- What is Capacity?
- What is Channel Score?
- Why is channel overloaded?

must be answerable without launching a new audit when the canonical reference already contains the answer.

## 7. Tests Run

Initial gate before edits:

| Check | Result |
| --- | --- |
| `tools/v7-truth-check --all --json` | PASS / `FULLY_ALIGNED` after unsandboxed GitHub remote read |
| `tools/v7-convergence-status --json` | PASS / `ALIGNED` after unsandboxed GitHub remote read |
| `git diff --check` | PASS |

Final verification is required after commit/push.

## 8. Remaining Gaps

| Gap | Status |
| --- | --- |
| Groups / Policies full canonical contract | Still `UNKNOWN` in canonical reference; future audit allowed if needed. |
| Autonomy full canonical contract | Still `UNKNOWN` in canonical reference; future audit allowed if needed. |

## 9. Final Verdict

REFERENCE_FIRST_RULE_ACTIVE
