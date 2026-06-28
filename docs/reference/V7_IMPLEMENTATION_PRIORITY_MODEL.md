# V7 Implementation Priority Model

Status: canonical
Owner: OMP
Need New Owner: FALSE

## Purpose

This model defines how OMP chooses implementation work from `docs/programs/V7_IMPLEMENTATION_BACKLOG.md`.

It does not create a planner, governance layer, execution path, runtime owner, truth source, authority expansion, runtime apply, user movement, or synthetic evidence.

It is not a second queue.
It ranks the only live engineering queue.

## Selection Rule

OMP must choose the highest-priority unfinished backlog item unless that item crosses:

- `AUTHORITY_BOUNDARY`;
- `REAL_WORLD_LIMIT`;
- `UNSAFE_IMPLEMENTATION`;
- `FUNDAMENTAL_ARCHITECTURE_GAP`.

If the highest item is blocked, OMP may choose the next highest item only when the blocked item cannot progress without the stop condition being resolved.

OMP must not generate implementation tasks from reports, policies, architecture, ADRs, research documents, product documents, or chat history.

## Priority Inputs

Each item is scored from `0` to `5` for positive inputs and negative costs.

Positive inputs:

| Input | Meaning |
| --- | --- |
| Production value | Direct effect on user availability, invisible switching, operator workload, and production readiness. |
| Safety gain | Reduction in unsafe movement, stale decisions, false positives, rollback ambiguity, or broad blast radius. |
| Autonomy gain | Movement toward certified action-class, delegated autonomy, or production autonomy. |
| Reuse percentage | Amount of capability provided by existing owners without new systems. |
| Runtime impact | Ability to make Runtime thinner, safer, more deterministic, or more eligible for future automation. |
| Research confidence | Strength of industry consensus plus V7 reality audit evidence. |

Negative inputs:

| Input | Meaning |
| --- | --- |
| Complexity | Engineering effort and behavioral surface area. |
| Dependencies | Number and readiness of prerequisite owners/evidence. |
| Blast radius | Risk of affecting users, channels, services, policy, or authority boundaries during implementation. |
| Authority impact | Whether the work requires approval, policy expansion, or operator boundary changes. |
| Testing cost | Amount of focused, integration, truth, convergence, certification, and production verification required. |

## Score Formula

```text
positive_score =
  production_value * 5
  + safety_gain * 4
  + autonomy_gain * 4
  + runtime_impact * 3
  + reuse_percentage * 3
  + research_confidence * 2

negative_score =
  complexity * 3
  + dependencies * 2
  + blast_radius * 4
  + authority_impact * 4
  + testing_cost * 2

priority_score = positive_score - negative_score
```

The weights intentionally favor production safety, production value, autonomy gain, reuse, and low blast radius.

## Tier Mapping

| Tier | Score shape | Meaning |
| --- | --- | --- |
| `Tier A` | Highest score and direct blocker to certified production autonomy. | Highest production leverage. |
| `Tier B` | High score with useful production/autonomy value, often after Tier A prerequisites. | High value. |
| `Tier C` | Medium score, supporting clarity, observability, or bounded future readiness. | Medium. |
| `Tier D` | Low current score or future-scope item outside present product/runtime needs. | Optional. |

Tier assignment is not permanent.
OMP recalculates after every implementation, certified outcome, authority decision, runtime evidence change, or reality limit.

## Hard Gates

An item cannot be selected for implementation when:

1. it creates a new owner while `Need New Owner = FALSE`;
2. it bypasses policy lifecycle;
3. it enables runtime apply without certification and authority;
4. it moves users without explicit approved authority;
5. it expands authority silently;
6. it lowers safety, freshness, rollback, verification, trust, confidence, suitability, or anti-flap gates;
7. it duplicates planner, governance, execution, runtime, truth, packet, rollback, or learning owners;
8. it depends on synthetic evidence;
9. it redesigns completed architecture without `FUNDAMENTAL_ARCHITECTURE_GAP`.

## Recalculation Rule

OMP must recalculate priority after:

- backlog item completion;
- failed test or verification;
- truth/convergence result change;
- new certified outcome;
- authority approval or rejection;
- real-world state change;
- new evidence that changes complexity, dependencies, or confidence.

Recalculation must not create a new roadmap document.
The backlog remains the implementation queue.

## Current Priority Verdict

Current highest implementation priority:

```text
B2: Add hard-failure timer/risk class to policy windows.
```

Why current:

1. Tier A is complete.
2. B13 metric reliability is certified for blocking recommendations only.
3. B16 rollback authority certification is complete as read-only authority-review evidence.
4. RT2-S1 through RT2-S6 are complete as read-only/advisory owner-mapped surfaces.
5. RT2-S6 produced an OMP-owned advisory recommendation to return to existing backlog item `B1`.
6. `B1` is complete as read-only liveness evidence aggregation through existing owners.
7. `B2` is the first unfinished Tier B item and reuses existing OMP floors, safety policy, anti-flap overlay, and trust inventory owners.
8. It does not require authority expansion.
9. It does not enable runtime apply, automation, or user movement.
10. It improves hard-failure timing/risk policy readiness without creating a new owner.

Need New Owner: `FALSE`.
