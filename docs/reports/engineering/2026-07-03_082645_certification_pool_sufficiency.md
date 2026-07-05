# Certification Pool Sufficiency

Timestamp: 2026-07-03T08:26:45+0700

Mode: Documentation Only

Canonical document:

`docs/reference/capabilities/CONTROLLED_PRODUCTION_CERTIFICATION_PROGRAM.md`

## Summary

The Controlled Production Certification Program was updated so certification cannot become blocked merely because the certification infrastructure is too small.

The program now requires a Certification Pool Decision before any HOLD caused by insufficient Certification Users. If the Certification Pool can legally be expanded through existing owners, expansion becomes the required path. HOLD is permitted only when expansion is blocked by policy, blocked by missing implementation, or canonically impossible.

No implementation, deployment, production modification, Runtime change, Planner change, Authority change, Restore Barrier change, or user movement was performed.

Final result:

`CERTIFICATION_INFRASTRUCTURE_SELF_SUFFICIENT`

## New Canonical Law

`CERTIFICATION_INFRASTRUCTURE_SUFFICIENCY_LAW`

Rule:

The certification program must maintain sufficient certification infrastructure to execute every certification stage.

Certification capability must never depend on accidental availability of Certification Users.

Certification infrastructure is part of the production platform.

## Discover / Reuse / Extend Result

Existing concepts found and reused:

| Existing concept | Reuse / extension |
| --- | --- |
| Certification Users | Reused as real production identities designated for certification. |
| Certification Groups | Reused as the stage/cohort grouping mechanism. |
| Certification Pool Design | Extended with sufficiency and expansion requirements. |
| Controlled Production Environment | Reused as the real production environment for certification users. |
| Controlled Incident | Reused as the legal production incident shape. |
| Reality First / Reality Preservation | Preserved: fake users, mock users, synthetic identities, and fabricated production evidence remain forbidden. |
| Owner Mapping | Extended with pool decision and expansion bridge items. |
| OMP | Reused as the phase and next-action owner. |
| Production Maturity | Reused as the certification evidence consumer. |

New owners created:

`NONE`

New architecture created:

`NONE`

## Updated Sections

Updated sections:

- Definitions.
- Certification Infrastructure Sufficiency Law.
- Certification Environment Lifecycle.
- Certification Pool Design.
- Certification Readiness Checklist.
- Operational Procedure.
- Certification State Machine.
- Integration With Existing V7 Canon.
- Canonical Owner Review.
- Program Roadmap.
- Owner Mapping.
- Certification Philosophy Summary.
- Final Engineering Review.

## Certification Pool Sufficiency Rule

Before beginning a certification stage, the system must determine:

```text
Does a sufficiently large Certification Group already exist?
  -> YES: Use it.
  -> NO: Can additional Certification Users be legally created?
  -> YES: Create additional Certification Users through existing owners.
  -> Register them through existing owners.
  -> Assign them to the Certification Pool.
  -> Continue the certification program.
  -> NO: Enter HOLD with explicit reason, or CANONICAL_IMPOSSIBILITY.
```

## Certification Pool Decision

| Situation | Required action |
| --- | --- |
| Pool already sufficient | Execute certification. |
| Pool insufficient and expansion allowed | Expand Certification Pool through existing owners. |
| Pool insufficient but expansion forbidden | Enter `HOLD` with `POOL_EXPANSION_BLOCKED_BY_POLICY`. |
| Pool expansion requires missing implementation | Enter `HOLD` with `POOL_EXPANSION_BLOCKED_BY_IMPLEMENTATION`. |
| Pool expansion impossible through current architecture | Enter `CANONICAL_IMPOSSIBILITY`. |

## Required HOLD Explanation

Before entering HOLD because of insufficient Certification Users, the system must answer:

`Why does the Certification Pool not already contain enough users?`

Allowed terminal answers:

- `POOL_ALREADY_SUFFICIENT`
- `POOL_EXPANDED`
- `POOL_EXPANSION_BLOCKED_BY_POLICY`
- `POOL_EXPANSION_BLOCKED_BY_IMPLEMENTATION`
- `CANONICAL_IMPOSSIBILITY`

No insufficient-pool HOLD may remain unexplained.

## Reality First Preservation

The update explicitly preserves Reality First:

- Certification Users are real production identities.
- Certification Users are not fake users.
- Certification Users are not mock users.
- Certification Users are not synthetic identities.
- Certification Users are not temporary fabricated objects.
- They participate in real Runtime, Planner, Authority, Verification, Rollback, Learning, OMP, and Production Maturity.

## Execution Flow Before

Old implicit flow:

```text
Stage requires more Certification Users
  -> Certification Group insufficient
  -> NOT_READY / HOLD
```

This allowed the program to depend on accidental certification user availability.

## Execution Flow After

New canonical flow:

```text
Stage requires more Certification Users
  -> Certification Pool Decision
  -> Pool already sufficient: execute certification
  -> Expansion allowed: expand pool through existing owners, then execute certification
  -> Expansion blocked: HOLD with exact reason
  -> Expansion impossible: CANONICAL_IMPOSSIBILITY
```

## Owner Mapping Update

Added bridge items:

| Item | Owner | Status |
| --- | --- | --- |
| Certification Pool Decision | Existing user registry, group/org policy owner, assignment owner, OMP, Production Maturity | `NEEDED_IMPLEMENTATION` |
| Certification Pool expansion procedure | Existing user registry, account provisioning, group/org policy, assignment, routing, OMP, Production Maturity | `NEEDED_IMPLEMENTATION` |

These are implementation bridges through existing owners, not new owners.

## Remaining Architectural Contradictions

`NONE`

The document now consistently states:

- certification does not wait for accidental production scale;
- insufficient pool size triggers legal expansion when possible;
- HOLD requires explicit policy, implementation, or impossibility reason;
- fake users and synthetic identities remain forbidden.

## Remaining Infrastructure Gaps

Real remaining bridge work:

- define concrete owner invocation for Certification Pool Decision;
- define concrete owner invocation for legal Certification User creation/registration/designation;
- project pool sufficiency state into Certification Reports, Current Program State, Passport view, OMP, and Production Maturity.

These are implementation bridge tasks, not canonical document contradictions.

## Final Verdict

`CERTIFICATION_INFRASTRUCTURE_SELF_SUFFICIENT`
