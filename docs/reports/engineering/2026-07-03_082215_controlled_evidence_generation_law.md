# Controlled Evidence Generation Law

Timestamp: 2026-07-03T08:22:15+0700

Mode: Documentation Only

Canonical document:

`docs/reference/capabilities/CONTROLLED_PRODUCTION_CERTIFICATION_PROGRAM.md`

## Summary

The Controlled Production Certification Program was updated to remove the remaining execution contradiction where certification could fall into waiting for random production incidents when controlled real production evidence could be legally generated.

No implementation, deployment, production modification, Runtime change, Planner change, Authority change, Restore Barrier change, or user movement was performed.

Final result:

`CONTROLLED_EVIDENCE_GENERATION_CANONICAL`

## Discover / Reuse / Extend Result

Existing concepts found and reused:

| Existing concept | Reuse / extension |
| --- | --- |
| Controlled Production Environment | Reused as the real production environment for scheduled evidence generation. |
| Controlled Incident | Reused as the legal incident object for certification evidence. |
| Reality Creation Law | Extended with explicit evidence decision semantics. |
| Reality Preservation Law | Preserved as the ban on fake evidence, synthetic success, and bypassed owners. |
| Certification Pool / Certification Group / Certification Users | Reused as the participant source for controlled evidence generation. |
| Authority | Reused as the budget and approval owner. |
| OMP | Reused as the phase progression and next-action owner. |
| Production Maturity | Reused as the certification evidence consumer. |
| Execution Mission Protocol | Reused for mission continuity and stop discipline. |

New owners created:

`NONE`

New architecture created:

`NONE`

## Sections Updated

Updated sections:

- Definitions.
- Reality Creation Law.
- New subsection: Controlled Evidence Generation Law.
- Certification Mission Contract.
- Certification Environment Lifecycle.
- Promotion Contract.
- Operational Procedure.
- Certification Recovery Contract.
- Certification State Machine.
- Integration With Existing V7 Canon.
- Canonical Owner Review.
- Program Roadmap.
- Owner Mapping.
- Certification Philosophy Summary.
- Final Engineering Review.

## Execution Flow Before

Before this update, the program already said controlled production certification should avoid waiting for random incidents, but phase progression could still practically terminate as HOLD when current production did not contain enough users for the next stage.

Old implicit flow:

```text
Required Evidence
  -> Real production does not currently provide enough evidence
  -> HOLD / wait for a suitable future incident
```

This left an inconsistency with Reality Creation Law and Controlled Production Environment.

## Execution Flow After

New canonical flow:

```text
Required Evidence
  -> Does real production already provide it?
  -> YES: Use real production
  -> NO: Can Controlled Production legally generate it?
  -> YES: Prepare Controlled Certification Environment
  -> Execute Certification Mission
  -> Restore Production
  -> Continue Certification Program
  -> NO: Enter HOLD with explicit reason, or CANONICAL_IMPOSSIBILITY
```

Waiting for a random production incident is now fallback only after the system proves why Controlled Production is not being used.

## New Canonical Law

`CONTROLLED_EVIDENCE_GENERATION_LAW`

Rule:

Certification must not depend on random production conditions.

Whenever required evidence is unavailable from current production, the system must determine whether Controlled Production can legally generate it. If it can, Controlled Production becomes the default execution path.

## HOLD Explanation Requirement

Every HOLD caused by missing certification evidence must answer:

`Why is Controlled Production not being used?`

Allowed terminal answers:

- `ALREADY_HAVE_REAL_EVIDENCE`
- `CONTROLLED_PRODUCTION_SELECTED`
- `BLOCKED_BY_SAFETY_OWNER`
- `CANONICAL_IMPOSSIBILITY`
- `MISSING_IMPLEMENTATION`

No HOLD may exist only because the system is waiting for an unknown future incident.

## Certification Evidence Sources

| Situation | Required action |
| --- | --- |
| Real production already provides sufficient evidence | Use it. |
| Real production is insufficient and Controlled Production is possible | Create a Controlled Certification Mission through existing owners. |
| Controlled Production is forbidden by safety owners | Enter `HOLD` with `BLOCKED_BY_SAFETY_OWNER`. |
| Controlled Production is impossible through current architecture | Enter `CANONICAL_IMPOSSIBILITY`. |
| Controlled Production requires missing implementation | Create an implementation task through existing owners and enter `HOLD` with `MISSING_IMPLEMENTATION`. |

## Owner Mapping Update

Added implementation bridge item:

| Item | Owner | Artifact | Consumer | Status |
| --- | --- | --- | --- | --- |
| Certification Evidence Decision | OMP, Authority, Production Maturity, Controlled Production Environment, Certification Mission Contract | Decision record selecting sufficient real production evidence, legal Controlled Production, safety-owner HOLD, missing implementation HOLD, or CANONICAL_IMPOSSIBILITY | Program Roadmap, Certification Reports, Current Program State, Passport view | `NEEDED_IMPLEMENTATION` |

This is an owner-mapped implementation bridge, not a new owner.

## Remaining Architectural Contradictions

`NONE`

The document now consistently says:

- random production incidents are valid opportunistic evidence;
- Controlled Production is valid scheduled evidence;
- Controlled Production is preferred when legal and safe;
- HOLD is allowed only after the Certification Evidence Decision explains why Controlled Production is not used.

## Remaining Implementation Bridge Work

Real remaining bridge work:

- implement or document the concrete owner invocation for Certification Evidence Decision;
- project the decision into Certification Reports, Current Program State, Passport view, OMP, and Production Maturity;
- define concrete controlled-source setup and legal degradation owner commands where still marked as `NEEDED_IMPLEMENTATION` or `NEEDED_OWNER_DECISION`.

These are implementation bridge tasks, not canonical document contradictions.

## Final Verdict

`CONTROLLED_EVIDENCE_GENERATION_CANONICAL`
