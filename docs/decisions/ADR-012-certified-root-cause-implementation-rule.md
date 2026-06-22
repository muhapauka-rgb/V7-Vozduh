# ADR-012 Certified Root Cause Implementation Rule

Status: Accepted
Date: 2026-06-22
Commit: `ece796d`

## Context

V7 now has a reference-first workflow and many phases have already certified specific root causes through evidence, dry-runs, and safety checks.

Repeated discovery after a certified root cause creates project drag and fragments attention. Once the cause and fix path are proven, the safest next step is usually controlled implementation through the existing owner, followed by tests, verification, and documentation.

## Decision

If all of the following are true:

1. root cause found;
2. solution proven;
3. dry-run successful;
4. no runtime-apply risk;

then the next phase must follow:

```text
IMPLEMENT
  -> TEST
  -> VERIFY
  -> DOCUMENT
```

It must not create another discovery/audit report for the same root cause.

## Exceptions

A new audit is allowed only when:

- new evidence contradicts the certified root cause;
- the proven dry-run no longer reproduces;
- implementation would introduce runtime apply risk;
- the canonical reference marks the area `UNKNOWN`;
- the implementation owner cannot be identified from existing reference, ADRs, system map, or code.

## Alternatives considered

- Continue discovery after each phase: rejected because it repeats known findings and delays fixes.
- Implement without verification: rejected because V7 requires truth/convergence and evidence-backed runtime safety.
- Create a new owner for certified fixes: rejected because V7 must reuse existing owners unless the reference proves no owner exists.

## Consequences

- Certified findings become action triggers, not prompts for another audit.
- Follow-up phases must be scoped to existing owner implementation, tests, verification, and reference/report updates.
- Runtime apply remains forbidden unless the phase explicitly authorizes it and gates pass.
- This rule strengthens Reference First by adding the post-certification action path.

## Affected modules

- Project workflow
- Audit workflow
- Implementation workflow
- Canonical reference
- System map

## Reference updates

- Added Certified Root Cause Rule to `docs/reference/V7_CANONICAL_REFERENCE.md`.
- Added Certified Root Cause Workflow to `docs/reference/SYSTEM_MAP.md`.

## Related reports

- `docs/reports/AUTONOMY_TRUST_BUILDOUT_1_REPORT.md`
- `docs/reports/AUTONOMY_FINAL_BRANCH_1B_DEPLOY_AND_RECOVERY_REPORT.md`
- `docs/reports/AUTONOMY_FINAL_BRANCH_1A_REPORT.md`
- `REFERENCE_2_REFERENCE_FIRST_RULE_REPORT.md`
