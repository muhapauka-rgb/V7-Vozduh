# Candidate Suitability Model

## Purpose

Candidate Suitability measures how suitable a channel is for a specific user at a specific moment.

It is not a planner, not governance, not execution authority, and not a selected move writer.

## Inputs

| Input | Source |
|---|---|
| Channel quality | `egress-quality-summary.json`, service matrix rows |
| Channel history | `ServiceHistoryStore`, quality windows |
| Service quality | `service-matrix.json` |
| Service history | `ServiceHistoryStore` windows |
| User service weights | `UserServiceWeights` from `service-preferences.json` |
| Risk | `risk-summaries.json` |
| Trust | `trust-summaries.json` / `ExecutionTrustModel` |
| Blast radius context | `blast-radius-summaries.json` / `DynamicBlastRadiusModel` |
| Planner advisory inputs | existing RoutingBrain candidate advisory scores |

## Scoring Logic

Implemented as an extension of `RoutingBrain.candidate_advisory_scores`.

Suitability score is normalized to `0..100`.

Breakdown:

| Factor | Weight |
|---|---:|
| weighted service score | 35% |
| service history score | 25% |
| execution trust score | 15% |
| service confidence score | 15% |
| inverse degradation risk | 10% |

The snapshot worker may apply additional bounded penalties, for example high-risk channel penalty.

## Explainability

Each candidate carries:

- `reason_breakdown`;
- service/history/trust/risk explanations;
- source snapshot references;
- authority guards.

Example breakdown:

```json
{
  "service_weight": 14.2,
  "service_history": 9.1,
  "execution_trust": 4.5,
  "service_confidence": 5.8,
  "risk": -7.0
}
```

## Confidence

Candidate confidence is derived from service confidence and snapshot confidence factors.

Snapshot confidence factors:

- source completeness;
- history completeness;
- probe completeness;
- service completeness.

## Authority

Candidate Suitability may influence planner advisory score part only after existing planner hard gates mark a candidate eligible.

It cannot:

- create candidates;
- bypass hard gates;
- bypass governance;
- move users;
- write selected moves;
- execute runtime actions.

