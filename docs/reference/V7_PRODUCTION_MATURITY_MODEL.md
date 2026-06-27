# V7 Production Maturity Model

Status: canonical
Owner: OMP
Need New Owner: FALSE

## Purpose

This document defines the canonical maturity model for V7.

The model has two independent dimensions:

1. `ENGINEERING MATURITY`
2. `PRODUCTION MATURITY`

Engineering Maturity measures completed engineering knowledge.

Production Maturity measures production readiness and distance to full production autonomy.

Scale:

```text
0% -> 100%
```

`100%` Engineering Maturity means:

```text
ENGINEERING_COMPLETE
```

`100%` Production Maturity means:

```text
PRODUCTION_AUTONOMY_CERTIFIED
```

This model does not redesign OMP, Runtime, architecture, Planner, Governance, execution, truth, policies, owners, authority, runtime apply, or user movement.

## Separation Rule

Engineering Maturity and Production Maturity must never be merged into one score.

Architecture, research, policy, and model completion prove that V7 understands the system it must build.

They do not prove that V7 is production-autonomous.

Production Maturity increases only through real implementation, deploy, testing, verification, certification, production outcomes, authority decisions, and certified autonomy.

Backlog completion increases only Production Maturity.

Reference documents must never change Engineering Maturity after certification unless one of these is true:

- industry consensus changes;
- implementation proves `FUNDAMENTAL_ARCHITECTURE_GAP`;
- the operator explicitly requests a reference update.

## Recalculation Rule

OMP must recalculate both maturity dimensions after every:

- implementation;
- deploy;
- truth;
- convergence;
- certification;
- production outcome;
- authority decision.

Values must be calculated from category status, backlog progress, certification state, and real outcomes.

They must not be hand-edited as opinion.

## Engineering Maturity Categories

Engineering Maturity is the weighted total of completed knowledge categories:

```text
overall =
  sum(category_current_percent * category_weight)
  / sum(category_weight)
```

Weights sum to `100`.

| Category | Current % | Target % | Weight | Current evidence basis |
| --- | ---: | ---: | ---: | --- |
| Architecture | `100` | `100` | `15` | Final system architecture is complete. |
| Decision Model | `100` | `100` | `15` | Decision Model is complete. |
| Runtime Model | `100` | `100` | `15` | Runtime Model is complete. |
| System Architecture | `100` | `100` | `15` | Integrated system architecture is complete. |
| Research | `100` | `100` | `15` | Research framework and required architecture research are complete. |
| Canonical Policy Library | `100` | `100` | `15` | Canonical Policy Library reached Stage 4 V7 Fit Analysis and produced the implementation backlog. |
| OMP | `100` | `100` | `10` | OMP is the permanent production operating program. |

Current Engineering Maturity:

```text
100.0%
```

Engineering status:

```text
ENGINEERING_COMPLETE
```

## Production Maturity Categories

Production Maturity is the weighted total of production readiness categories.

Weights sum to `100`.

| Category | Current % | Target % | Weight | Current evidence basis |
| --- | ---: | ---: | ---: | --- |
| Implementation | `11.8` | `100` | `20` | Implementation Backlog actionable progress is `4 / 34`. |
| Testing | `36` | `100` | `10` | A1/A2 focused unit tests, A4 closure read-model regression tests, and read-only CLI smoke checks pass; broader production certification remains open. |
| Production Deployments | `100` | `100` | `10` | Safe deploy owner exists and local/GitHub/production convergence is aligned. |
| Production Outcomes | `25` | `100` | `15` | A3 added a real governed no-rollback candidate outcome; A4 representative real outcomes are materialized and outcome closure is `COMPLETE`. |
| Certification | `32` | `100` | `15` | A1/A2 are implemented and tested; A3 has real no-rollback evidence; A4 representative evidence and closure read-model are complete. Architecture/model certification belongs to Engineering Maturity. |
| Authority Evolution | `15` | `100` | `10` | TIER_1 governed authority exists; delegated autonomy policy is not approved and authority expansion is not granted. |
| Production Autonomy | `0` | `100` | `10` | Runtime automation/apply remains disabled; no bounded production autonomy is certified. |
| Implementation Backlog Completion | `11.8` | `100` | `10` | Mandatory backlog completion is `4 / 34`. |

## Current Scores

Engineering calculation:

```text
(100*15 + 100*15 + 100*15 + 100*15 + 100*15 + 100*15 + 100*10) / 100 = 100.0
```

Production calculation:

```text
(11.8*20 + 36*10 + 100*10 + 25*15 + 32*15 + 15*10 + 0*10 + 11.8*10) / 100 = 27.2
```

Current Engineering Maturity:

```text
100.0%
```

Current Production Maturity:

```text
27.2%
```

Target:

```text
100%
```

Production remaining:

```text
72.8%
```

## Backlog Inputs

Current backlog progress:

| Scope | Complete | Total | Contribution |
| --- | ---: | ---: | --- |
| Tier A | `4` | `6` | A1/A2 read-only foundations are implemented and tested; A3 real no-rollback outcome evidence is closed; A4 representative outcome evidence is materialized and closure-complete. |
| Tier B | `0` | `21` | High-value implementation remains open. |
| Tier C | `0` | `7` | Medium implementation remains open. |
| Tier D optional | `0` | `6` | Optional future-scope work remains open. |
| Overall actionable | `4` | `34` | Implementation category is `11.8%`. |

Current highest implementation task:

```text
A5: Certify class-level blast-radius evidence beyond the one-user guard.
```

## Milestones

Milestones are status thresholds, not separate roadmaps.
OMP reports Engineering and Production milestones separately.

Engineering milestones finish at:

```text
ENGINEERING_COMPLETE
```

Production milestones finish at:

```text
PRODUCTION_AUTONOMY_CERTIFIED
```

### Engineering Milestones

| Milestone | Meaning | Required evidence |
| ---: | --- | --- |
| `20%` | Architecture Complete | Final architecture verdict is `ARCHITECTURE_COMPLETE`. |
| `40%` | Decision Model Complete | Decision Model is canonical. |
| `60%` | Runtime Model Complete | Runtime Model is canonical. |
| `80%` | Policy Library Complete | Canonical Policy Library reaches Stage 4 Fit Analysis. |
| `100%` | Engineering Complete | Architecture, research, policies, OMP, Decision Model, Runtime Model, and System Architecture are complete. |

Current Engineering milestone:

```text
ENGINEERING_COMPLETE
```

### Production Milestones

| Milestone | Meaning | Required evidence |
| ---: | --- | --- |
| `20%` | First Implementation Certified | At least one Tier A implementation item is `DONE`, tested, truth-checked, converged, and certified. |
| `35%` | Runtime Eligibility Implemented | Runtime eligibility gates are implemented through existing owners. |
| `50%` | Implementation Half Complete | At least half of actionable backlog items are `DONE` and verified. |
| `65%` | Certification Half Complete | Core action-class certification paths have repeated real outcomes and closure. |
| `80%` | Runtime Production Ready | Runtime eligibility, verification, rollback, freshness, anti-flap, and blast gates are implementation-certified. |
| `90%` | Bounded Production Autonomy | Bounded action classes have certified outcomes and approved authority/policy. |
| `100%` | Production Autonomy Certified | Runtime operates certified routine work inside approved policy; operator supervises exceptions. |

Current Production milestone:

```text
20%: First Implementation Certified
```

Next Production milestone:

```text
35%: Runtime Eligibility Implemented
```

## OMP Print Contract

OMP must always print:

```text
V7 PRODUCTION STATUS

ENGINEERING

Architecture
100%

Research
100%

Policies
100%

Engineering Maturity
100.0%

PRODUCTION

Implementation
11.8%

Certification
32%

Autonomy
0%

Production Maturity
27.2%

Overall Status
ENGINEERING_COMPLETE / PRODUCTION_IN_PROGRESS

Current Focus
CERTIFICATION

Backlog
Tier A
4 / 6
Tier B
0 / 21
Tier C
0 / 7
Tier D
0 / 6 optional
Overall
4 / 34 complete

Current Tier
TIER_1_GOVERNED

Highest Priority Task
A5: Certify class-level blast-radius evidence beyond the one-user guard.

Current Stop Condition
NONE: continue through existing A5 certification owner

Estimated Remaining Work
Moderate

Expected Next Milestone
35%: Runtime Eligibility Implemented
```

The numeric values must be recalculated after implementation, deploy, truth, convergence, certification, production outcome, or authority decision.

Current focus values:

- `IMPLEMENTATION`
- `CERTIFICATION`
- `AUTHORITY`
- `AUTONOMY`
- `PRODUCTION`

Focus transition:

```text
IMPLEMENTATION
  -> CERTIFICATION
  -> AUTHORITY EVOLUTION
  -> PRODUCTION AUTONOMY
  -> CONTINUOUS IMPROVEMENT
```

## Stop Rule

If the maturity score reaches `100%`, OMP must report:

```text
PRODUCTION_AUTONOMY_CERTIFIED
```

If the implementation backlog is empty before `100%`, OMP must report:

```text
IMPLEMENTATION_COMPLETE
```

and identify the non-backlog category preventing `PRODUCTION_AUTONOMY_CERTIFIED`.
