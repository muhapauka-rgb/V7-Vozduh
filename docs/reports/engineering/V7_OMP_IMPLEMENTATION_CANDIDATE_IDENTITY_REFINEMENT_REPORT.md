# V7 OMP Implementation Candidate Identity Refinement Report

Date: 2026-07-09
Program: `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
Status: `PASS`

## 1. Summary

OMP was refined to prevent duplicate Mission creation after BDP integration while preserving genuinely different engineering situations.

The refinement integrates Implementation Candidate Identity into the existing OMP admission model. It does not create a new owner, queue, program, Runtime, Planner, truth source, or architecture.

## 2. Discovery Result

Existing OMP mechanisms found:

| Mechanism | Existing coverage | Reuse decision |
| --- | --- | --- |
| BDP Implementation Candidate Consumption Rule | Defines BDP output consumption, admission, Mission creation, and no-queue boundary. | Reused and extended. |
| Mission Formation | Converts accepted work into OMP Mission with owner, authority, verification, rollback, Runtime, production, and Codex handoff. | Reused and extended. |
| Re-open Evaluation | Determines whether verified knowledge/work should be reopened. | Reused and specialized for Candidate Instances. |
| Behavior Chain / Chain Closure | Requires producer, consumer, verified consumption, behavior change, and legal terminal consumer. | Reused as completion guard. |
| Backlog post-admission role | Records admitted Mission state and prevents BDP from becoming a queue. | Reused. |
| Duplicate owner / planner / queue rules | Prevent architectural duplication. | Reused. |

Gap found:

OMP had Candidate consumption and Mission admission, but did not formally define how to determine whether two accepted BDP candidates were the same concrete engineering situation or merely the same problem class.

## 3. Sections Extended

Updated OMP sections:

- `2.1.7.1. BDP Implementation Candidate Consumption Rule`
- `29.3 OMP Engineering Language`

Added inside the existing OMP admission model:

- Implementation Candidate Identity;
- Candidate Identity Components;
- Candidate Class and Instance Rules;
- Instance Duplicate Check;
- Candidate Merge Rule;
- Cohort Mission Safety Rule;
- Implementation Candidate Lifecycle;
- Mission Reopen Rules;
- Mission lifecycle binding;
- glossary entries for Class, Instance, Candidate Merge, Cohort Mission, and Mission Identity.

## 4. Identity Model

OMP now distinguishes:

| Level | Meaning |
| --- | --- |
| Implementation Candidate Class | Reusable engineering problem pattern. |
| Implementation Candidate Instance | Concrete engineering situation and the OMP admission unit. |
| OMP Mission Identity | Execution identity derived from one Instance or one safe Cohort Mission. |

Identity is not based on title, file, function, class name, document location, or wording similarity.

Instance identity is resolved through engineering context: Engineering Intent, Automation Break, affected Behaviour, affected capability, owner, consumer, current state, expected state, evidence window, runtime context, user/group/channel scope, verification, rollback, authority, and policy context.

## 5. Duplicate Prevention

Before Mission creation, OMP must now check whether a Candidate Instance:

- already exists;
- is already active;
- has already been implemented;
- is already verified and closed;
- is superseded;
- belongs to an existing Cohort Mission;
- has unresolved identity.

Duplicate evidence is merged only when deterministic identity proves the same Candidate Instance. Same Class or same title is not sufficient.

## 6. Real Repeat Support

Real recurring situations are preserved through Mission Reopen Rules.

OMP now distinguishes:

- `NEW_INSTANCE`;
- `REPEATED_INSTANCE`;
- `REGRESSION`;
- `SUPERSEDED_BY_CONTEXT`;
- `NOT_APPLICABLE_REPEAT`.

This prevents both harmful duplication and harmful over-merge.

## 7. Cohort Safety

Multiple Candidate Instances may become one Cohort Mission only when intent, automation break, owner, consumer, verification, rollback, authority, policy, runtime, and blast radius are compatible and per-Instance evidence remains traceable.

If any condition fails, Missions remain separate.

## 8. Reviews

| Review | Result |
| --- | --- |
| Identity Review | `PASS` |
| Mission Review | `PASS` |
| Duplicate Review | `PASS` |
| Instance Review | `PASS` |
| Cohort Review | `PASS` |
| Merge Review | `PASS` |
| Lifecycle Review | `PASS` |
| Reuse Review | `PASS` |
| No New Owner Review | `PASS` |
| No New Queue Review | `PASS` |
| Architecture Review | `PASS` |
| Quality Review | `PASS` |
| Self Review | `PASS` |

## 9. Architecture Impact

Architecture impact: `NONE`.

The refinement uses existing OMP ownership and existing Mission / Backlog / report / CPS evidence surfaces. It only clarifies admission identity and lifecycle semantics.

No new owner was created.
No new queue was created.
No new program was created.
No new architecture was created.

## 10. Final Verdict

```text
PASS
```

OMP now prevents repeated Missions for the same Implementation Candidate Instance while preserving separate Missions for genuinely different real engineering situations, even when they share one Implementation Candidate Class.
