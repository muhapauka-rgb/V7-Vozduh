# P4 Action Domain Model

Project: V7 Vozduh
Block: P4 Controlled Runtime Action Planning

## Core Concepts

| Concept | Definition |
| --- | --- |
| Action | A proposed bounded runtime change that may later become executable only after separate approval and recheck. |
| Action Packet | Non-executable planning contract describing scope, target, evidence, approval, recheck, rollback and observation. |
| Action Scope | Exact boundary of allowed effect: users, target, route class, service, time window and mutation class. |
| Action Target | Specific runtime object affected by the future action. |
| Action Evidence | Source refs, hashes, dry-run output, verification, readiness and candidate lineage. |
| Action Verification | Planned checks before, during and after future action. |
| Action Rollback | Preview-only rollback plan bound to the same scope. |
| Action Observation | Time-boxed monitoring contract for before/during/after checkpoints. |

## Allowed Planning Actions

P4 may define plans for future action classes:

- zero-movement governance state transition
- one-user movement candidate
- rollback candidate
- containment candidate
- route policy candidate

P4 does not implement any action class.

## Authority States

- `PLANNING_ONLY`
- `READY_FOR_REVIEW`
- `APPROVED_FOR_DESIGN`
- `RECHECK_REQUIRED`
- `ABORTED`
- `EXPIRED`
- `NOT_EXECUTABLE_IN_P4`

## Design Rule

No Action becomes executable from P4. Execution authority requires a later explicitly authorized block.

## Verdict

`action_domain_defined=true`

