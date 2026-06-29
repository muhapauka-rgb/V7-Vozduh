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
| Implementation | `91.2` | `100` | `20` | Implementation Backlog actionable progress is `31 / 34`. |
| Testing | `74` | `100` | `10` | A1/A2 focused unit tests, A4 closure read-model regression tests, A6/B13/B16 read-only verification tests, B1 liveness evidence aggregation tests, B2 hard-failure policy-window tests, B3 soft-degradation threshold vocabulary tests, B4 degradation signal policy mapping tests, B5 observed degradation attribution tests, B6 V7-native degradation response mapping tests, B7 service-objective threshold binding tests, B8 recovery admission certification tests, B9 post-admission observation window tests, B10 recovery slow-start progression tests, B11 org/cohort identity policy integration tests, B12 next action-class stage certification tests, B14 service/pool/cohort blast-radius scope tests, B15 containment/forward-fix classification tests, B17 stale-read mutation blocking tests, B18 owner-issued version/lease pattern tests, B19 hysteresis/state-change-cost mapping tests, B20 hard-failure override anti-flap arbitration tests, B21 per-user routing control mode tests, C1 fail-open/fail-closed action-class behavior tests, C2 probabilistic suspicion advisory evidence tests, C3 break-glass authority policy tests, C4 all-at-once promotion unavailable verification tests, RT2-S1 measurement/observability tests, RT2-S2 world/readiness tests, RT2-S3 desired-state delta tests, RT2-S4 governed coordination tests, RT2-S5 certified concurrency ladder tests, RT2-S6 evidence-based continuous improvement tests, and read-only CLI/import smoke checks pass; broader production certification remains open. |
| Production Deployments | `100` | `100` | `10` | Safe deploy owner exists and local/GitHub/production convergence is aligned. |
| Production Outcomes | `25` | `100` | `15` | A3 added a real governed no-rollback candidate outcome; A4 representative real outcomes are materialized and outcome closure is `COMPLETE`. |
| Certification | `95` | `100` | `15` | A1/A2 are implemented and tested; A3 has real no-rollback evidence; A4 representative evidence and closure read-model are complete; A5 blast-radius evidence is certified read-only from E29 one/two/four-user proofs; A6 runtime eligibility arbitration is read-only complete and stops at authority/runtime_apply; B1 liveness evidence aggregation is implemented/tested read-only; B2 hard-failure policy windows are implemented/tested read-only; B3 soft-degradation threshold vocabulary is implemented/tested read-only; B4 degradation signal policy mapping is implemented/tested read-only; B5 observed degradation attribution is implemented/tested read-only; B6 V7-native degradation response mapping is implemented/tested read-only; B7 service-objective threshold binding is implemented/tested read-only; B8 recovery admission certification is implemented/tested read-only; B9 post-admission observation windows are implemented/tested read-only; B10 recovery slow-start progression is implemented/tested read-only; B11 org/cohort identity policy integration is implemented/tested read-only; B12 next action-class stage certification is implemented/tested read-only and stops at authority/runtime_apply; B13 metric reliability is certified for blocking recommendations only; B14 service/pool/cohort blast-radius scope is implemented/tested read-only and does not expand blast radius; B15 containment/forward-fix classification is implemented/tested read-only and does not execute apply or rollback; B16 rollback authority evidence is certified for authority review only; B17 stale-read mutation blocking is implemented/tested read-only and preserves stale reporting without mutation; B18 owner-issued version/lease pattern is implemented/tested read-only and changes no lease behavior; B19 hysteresis/state-change-cost mapping is implemented/tested read-only and changes no thresholds or formulas; B20 hard-failure override anti-flap arbitration is implemented/tested read-only and does not execute override, expand authority, mutate thresholds/formulas, or move users; B21 per-user routing control mode is implemented/tested read-only and does not write registry, replace planner, expand authority, or move users; C1 fail-open/fail-closed action-class behavior is implemented/tested read-only and does not change Runtime behavior, grant fail-open mutation, expand authority, replace Planner, synthesize evidence, or move users; C2 probabilistic suspicion advisory evidence is implemented/tested read-only and does not grant direct blocking power, direct execution power, Runtime apply, authority expansion, threshold/formula mutation, synthetic evidence, planner replacement, or user movement; C3 break-glass authority policy is implemented/tested read-only and does not grant break-glass invocation, Runtime apply, automation, authority expansion, rollback/apply execution, synthetic evidence, planner replacement, or user movement; C4 all-at-once promotion unavailable verification is implemented/tested read-only and does not allow all-at-once/direct promotion, Runtime apply, automation, authority expansion, blast-radius expansion, synthetic evidence, or user movement; RT2-S1 measurement/observability is complete as owner-mapped read-only evidence; RT2-S2 world/readiness is complete as owner-mapped read-only prepared state; RT2-S3 desired-state delta preparedness is complete as owner-mapped read-only advisory delta/prepared plan; RT2-S4 governed execution coordination is complete as owner-mapped read-only bounded coordination; RT2-S5 certified concurrency ladder is complete as serial-only read-only boundary plus explicit STOP_SAFE for wider levels; RT2-S6 evidence-based continuous improvement is complete as owner-mapped advisory recommendation to existing backlog item B1. Architecture/model certification belongs to Engineering Maturity. |
| Authority Evolution | `15` | `100` | `10` | TIER_1 governed authority exists; delegated autonomy policy is not approved and authority expansion is not granted. |
| Production Autonomy | `0` | `100` | `10` | Runtime automation/apply remains disabled; no bounded production autonomy is certified. |
| Implementation Backlog Completion | `91.2` | `100` | `10` | Mandatory backlog completion is `31 / 34`. |

## Current Scores

Engineering calculation:

```text
(100*15 + 100*15 + 100*15 + 100*15 + 100*15 + 100*15 + 100*10) / 100 = 100.0
```

Production calculation:

```text
(91.2*20 + 74*10 + 100*10 + 25*15 + 95*15 + 15*10 + 0*10 + 91.2*10) / 100 = 64.3
```

Current Engineering Maturity:

```text
100.0%
```

Current Production Maturity:

```text
64.3%
```

Target:

```text
100%
```

Production remaining:

```text
35.7%
```

## Backlog Inputs

Current backlog progress:

| Scope | Complete | Total | Contribution |
| --- | ---: | ---: | --- |
| Tier A | `6` | `6` | A1/A2 read-only foundations are implemented and tested; A3 real no-rollback outcome evidence is closed; A4 representative outcome evidence is materialized and closure-complete; A5 blast-radius evidence is certified read-only from E29 historical proofs; A6 runtime eligibility arbitration is read-only complete. |
| Tier B | `21` | `21` | B1 liveness evidence aggregation is implemented/tested read-only; B2 hard-failure policy windows are implemented/tested read-only; B3 soft-degradation threshold vocabulary is implemented/tested read-only; B4 degradation signal policy mapping is implemented/tested read-only; B5 observed degradation attribution is implemented/tested read-only; B6 V7-native degradation response mapping is implemented/tested read-only; B7 service-objective threshold binding is implemented/tested read-only; B8 recovery admission certification is implemented/tested read-only; B9 post-admission observation windows are implemented/tested read-only; B10 recovery slow-start progression is implemented/tested read-only; B11 org/cohort identity policy integration is implemented/tested read-only; B12 next action-class stage certification is implemented/tested read-only; B13 metric reliability certification is read-only complete for blocking recommendations; B14 service/pool/cohort blast-radius scope is implemented/tested read-only; B15 containment/forward-fix classification is implemented/tested read-only; B16 rollback authority certification is read-only complete for authority review; B17 stale-read mutation blocking is implemented/tested read-only; B18 owner-issued version/lease pattern is implemented/tested read-only; B19 hysteresis/state-change-cost mapping is implemented/tested read-only; B20 hard-failure override anti-flap arbitration is implemented/tested read-only; B21 per-user routing control mode is implemented/tested read-only. |
| Tier C | `4` | `7` | C1 fail-open/fail-closed action-class behavior, C2 probabilistic suspicion advisory evidence, C3 break-glass authority audited exceptional operator policy, and C4 all-at-once promotion unavailable verification are implemented/tested read-only; remaining medium implementation continues at C5. |
| Tier D optional | `0` | `6` | Optional future-scope work remains open. |
| Overall actionable | `31` | `34` | Implementation category is `91.2%`. |

Current highest implementation task:

```text
C5: Preserve rollback as operational compensation rather than transaction rollback.
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
35%: Runtime Eligibility Implemented
```

Next Production milestone:

```text
50%: Implementation Half Complete
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
91.2%

Certification
95%

Autonomy
0%

Production Maturity
64.3%

Overall Status
ENGINEERING_COMPLETE / PRODUCTION_IN_PROGRESS

Current Focus
IMPLEMENTATION

Backlog
Tier A
6 / 6
Tier B
21 / 21
Tier C
4 / 7
Tier D
0 / 6 optional
Overall
31 / 34 complete

Current Tier
TIER_1_GOVERNED

Highest Priority Task
C5: Preserve rollback as operational compensation rather than transaction rollback.

Current Stop Condition
NONE_FOR_C5_ROLLBACK_OPERATIONAL_COMPENSATION_NOT_TRANSACTION_ROLLBACK: continue through existing Runtime Model and rollback policy owners

Estimated Remaining Work
Moderate

Current Production Milestone
50%: Implementation Half Complete
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

## Engineering Intelligence Maturity

Status: `PHASE_1_MATERIALIZED`.

Engineering Intelligence maturity is a Production Maturity view, not a new program.
It measures whether existing engineering intelligence owners can turn evidence into recommendations and later learn from implemented outcomes.

| Level | Meaning | Existing owners | Current Phase 1 status | Certification basis |
| --- | --- | --- | --- | --- |
| Measured | Observation, time, process, outcome, prediction, and confidence evidence exists or is owner-mapped as missing. | `RT2-S1`, Runtime Model, read-model owners, feedback/learning owners. | `PARTIAL` | Measurement reliability and owner mapping. |
| Understood | Evidence can explain process, time, blocker, dependency, and owner. | Runtime Model, Work Placement, Decision Lifecycle, Runtime Time Topology. | `COMPLETE` | Product Evolution Review and Work Placement Review. |
| Recommended | Evidence can produce owner-mapped recommendation/no-change/missing-evidence verdict. | `RT2-S6`, OMP, Backlog, Engineering Reports. | `PARTIAL` | Engineering Review and safety review. |
| Validated | Implemented recommendations have before/after outcome evidence. | OMP, affected owner, verification, feedback/outcome owners. | `FUTURE_IMPLEMENTATION` | Tests, truth/convergence, real outcome or not-applicable proof. |
| Predictive | Recommendation impact can be compared against prediction. | Prediction Evidence / Confidence owners, Production Maturity, OMP. | `PARTIAL` | Prediction-vs-reality evidence and B13-style reliability. |
| Adaptive | Certified outcomes update future recommendation quality without self-modifying Runtime. | Decision To Outcome To Learning, `RT2-S6`, OMP. | `PARTIAL` | Real outcomes, confidence update, canonical owner update. |

Engineering Intelligence cannot certify Runtime automation, authority expansion, or user movement by itself.

### Engineering Intelligence Validation Maturity

Status: `PHASE_2_MATERIALIZED`.

Validation maturity measures whether recommendations are checked against observed reality.
It is a Production Maturity view, not a new roadmap or capability program.

| Level | Validation meaning | Existing owners | Current Phase 2 status |
| --- | --- | --- | --- |
| Measured | Recommendation, prediction, outcome, and confidence evidence are visible or owner-mapped as missing. | `RT2-S1`, `RT2-S6`, prediction/confidence/outcome owners. | `PARTIAL` |
| Understood | Expected result, observed result, difference, owner, and evidence source can be explained. | Runtime Model + OMP + Engineering Reports. | `COMPLETE` |
| Recommended | Recommendation carries expected result and validation plan. | `RT2-S6` + OMP. | `PARTIAL` |
| Validated | Implemented recommendation has outcome and prediction-vs-reality classification. | OMP + verification/outcome/learning owners. | `FUTURE_IMPLEMENTATION` |
| Predictive | Prediction confidence is updated from validation history. | Prediction Evidence / Confidence owners. | `PARTIAL` |
| Adaptive | Future recommendations improve from validated outcomes without runtime self-modification. | Decision To Outcome To Learning + `RT2-S6` + OMP. | `PARTIAL` |

Validation maturity cannot be used as authority, automation approval, or runtime apply eligibility without separate OMP certification.

### Adaptive Engineering Maturity

Status: `PHASE_3_MATERIALIZED`.

Adaptive Engineering maturity completes the Engineering Intelligence materialization ladder.
It is a Production Maturity view only.
Runtime never self-improves.

| Level | Adaptive meaning | Existing owners | Current Phase 3 status |
| --- | --- | --- | --- |
| Measured | Engineering observations, recommendations, outcomes, predictions, confidence, and learning evidence are visible or owner-mapped as missing. | `RT2-S1`, `RT2-S6`, Runtime Model, feedback/learning owners. | `PARTIAL` |
| Understood | Process, time, recommendation, validation, and confidence meaning are explainable through existing owners. | Runtime Model, OMP, SYSTEM_MAP. | `COMPLETE` |
| Recommended | Future recommendations can be owner-mapped with confidence and expected measurement. | `RT2-S6` + OMP. | `PARTIAL` |
| Validated | Recommendation effects are checked against real outcomes. | OMP + verification/outcome owners. | `FUTURE_IMPLEMENTATION` |
| Predictive | Prediction accuracy and confidence trends inform future recommendations. | Prediction Evidence / Confidence owners. | `PARTIAL` |
| Adaptive | Future recommendations evolve from validated outcomes and confidence changes. | Decision To Outcome To Learning + `RT2-S6` + OMP. | `PARTIAL` |
| Self-Improving Engineering | Engineering recommendations improve without Runtime self-modification. | OMP + `RT2-S6` + Production Maturity + canonical owners. | `CANONICAL_READY_IMPLEMENTATION_FUTURE` |

Self-Improving Engineering is not Runtime self-improvement, automation, authority, or direct implementation.
It is the OMP-governed ability to improve future engineering recommendations from real validated outcomes.
