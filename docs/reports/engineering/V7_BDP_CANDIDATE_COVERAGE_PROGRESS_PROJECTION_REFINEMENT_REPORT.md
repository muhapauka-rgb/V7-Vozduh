# V7 BDP Candidate Coverage Progress Projection Refinement Report

Date: 2026-07-09

Status: `PASS`

Scope:

- Updated only `docs/programs/V7_BEHAVIOUR_DISCOVERY_PROGRAM.md`.
- Did not change AEP, OMP, Engineering Chain, Runtime, owners, architecture, or canonical maturity owners.
- Created no new program, architecture, model, owner, truth source, or separate Progress Matrix.

## 1. Summary

Candidate Coverage Matrix was refined to include a second canonical projection:

```text
Progress Projection
```

This projection is computed from the same Candidate Coverage Matrix cells.

It does not create a new matrix.

The existing Candidate Coverage Matrix remains the single coverage source for Implementation Candidate Classes.

## 2. Reuse Discovery Result

Existing mechanisms found and reused:

| Existing mechanism | Reuse |
| --- | --- |
| Candidate Coverage Matrix | Remains the single source for class/depth coverage. |
| Engineering Logic Coverage Model | Supplies coverage domains, coverage states, blockers, consumer, next action, and chain closure. |
| Automation Progress Matrix | Reused as supporting automation evidence, not replaced. |
| Implementation Progress Matrix | Reused as supporting implementation evidence, not replaced. |
| Production Enablement Matrix | Reused as supporting production evidence, not replaced. |
| Production Maturity Model | Remains canonical owner of Engineering Maturity and Production Maturity. |
| OMP | Remains the only consumer that can admit, route, reject, hold, or sequence implementation work. |
| Execution Certification Ladder | Supplies certification depth and legal certification evidence. |
| Verification / Rollback / Authority / Runtime / Consumer / Chain Closure / Intent Closure | Supply blockers and path requirements. |

No existing mechanism already computed per-cell progress from Candidate Coverage Matrix to `PRODUCTION_CERTIFIED`, so the existing matrix was extended with a computed projection.

## 3. What Was Added

Added to BDP:

- `Candidate Coverage Matrix Projections`;
- `Progress Projection`;
- per-cell progress fields;
- legal status progression;
- progress path calculation;
- Engineering Value computation;
- project maturity projection;
- progress query requirements;
- validation rules;
- output / closure / completion hooks;
- certification reviews for coverage projection, progress projection, engineering value, and project maturity.

## 4. Progress Calculation

Every Candidate Coverage Matrix cell now has:

- `Current Status`;
- `Next Status`;
- `Remaining Path`;
- exact blocker fields;
- `Estimated Existing Work`;
- `Terminal Alternative`.

Legal progression:

```text
NOT_STARTED
  -> DISCOVERED
  -> IMPLEMENTED
  -> CERTIFIED
  -> PRODUCTION_CERTIFIED
```

`NOT_APPLICABLE` remains terminal with reason.

No new Coverage States or Progress States were added.

## 5. Next Step Calculation

For every cell, BDP resolves the next step using only existing mechanisms:

```text
Current Status
  -> Existing Owner
  -> Existing Consumer
  -> Existing Verification
  -> Existing Rollback / STOP_SAFE
  -> Existing Authority
  -> Existing Runtime Boundary
  -> Existing Production Boundary
  -> Engineering Chain Closure
  -> Intent Closure
  -> Terminal Alternative
```

If no path exists, BDP must first classify the blocker as evidence, verification, authority, rollback, runtime, production, consumer, chain, or intent closure.

Only after existing mechanisms fail may BDP record `FUNDAMENTAL_ARCHITECTURE_GAP`.

## 6. Engineering Value Calculation

For each Implementation Candidate, BDP computes:

| Value | Meaning |
| --- | --- |
| `Coverage Gain` | Candidate Coverage Matrix status weight delta. |
| `Production Gain` | Delta toward `PRODUCTION_CERTIFIED`. |
| `Automation Gain` | Delta in automation evidence / Automation Progress. |
| `Chain Closure Gain` | Delta toward verified chain closure or legal terminal alternative. |
| `Verification Gain` | Delta toward accepted verification evidence. |
| `Engineering Value` | Sum of evidence-backed gains. |

Status weights:

```text
NOT_STARTED = 0.00
DISCOVERED = 0.25
IMPLEMENTED = 0.50
CERTIFIED = 0.75
PRODUCTION_CERTIFIED = 1.00
NOT_APPLICABLE = excluded with reason
```

Engineering Value is computed, not manually assigned.

## 7. Project Maturity Calculation

BDP now computes navigation indicators:

- `Overall Coverage`;
- `Overall Automation Coverage`;
- `Overall Implementation Coverage`;
- `Overall Verification Coverage`;
- `Overall Production Coverage`;
- `Overall Chain Closure`;
- `Overall Engineering Maturity`.

These values are BDP navigation metrics only.

They do not overwrite canonical Engineering Maturity or Production Maturity owned by the Production Maturity model.

## 8. Project Questions Now Answerable

BDP can now answer:

- which class has highest maturity;
- which class has lowest maturity;
- which blockers prevent Production Certification;
- which existing owners are bottlenecks;
- which existing consumers fail to close chains;
- which verification, rollback, authority, runtime, and production boundaries remain;
- which candidates create maximum computed maturity gain through existing OMP consumption.

## 9. No New Architecture Confirmation

The refinement does not:

- create a new architecture;
- create a new owner;
- create a new truth source;
- create a new model;
- create a new program;
- create a separate Progress Matrix;
- create new Coverage States;
- create new Progress States;
- change OMP;
- change AEP;
- change Engineering Chain;
- change Production Maturity ownership.

## 10. Reviews

| Review | Result |
| --- | --- |
| Reuse Review | `PASS` |
| Coverage Projection Review | `PASS` |
| Progress Projection Review | `PASS` |
| Duplication Review | `PASS` |
| No New Architecture Review | `PASS` |
| Coverage Completeness Review | `PASS` |
| Engineering Value Review | `PASS` |
| Project Maturity Review | `PASS_WITH_BOUNDARY` |
| Quality Review | `PASS` |
| Self Review | `PASS` |

`PASS_WITH_BOUNDARY` means BDP may compute navigation maturity indicators, but canonical Engineering Maturity and Production Maturity remain owned by the Production Maturity model.

## 11. Final Verdict

`PASS`

Candidate Coverage Matrix is now both:

- a coverage map;
- an engineering navigation surface.

It can show current status, next required step, remaining path to Production Certification, exact blockers, computed Engineering Value, and expected maturity gain without inventing architecture or creating a separate Progress Matrix.
