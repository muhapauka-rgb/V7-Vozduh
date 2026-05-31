# Convergence F Simulation Consolidation

Project: V7 Vozduh
Block: Convergence F

## Canonical API Family

Simulation and impact now live inside the existing `/api/execution/*` read/preview family:

- `/api/execution/outcome-preview`
- `/api/execution/blast-radius`
- `/api/execution/service-impact`
- `/api/execution/readiness-forecast`
- `/api/execution/rollback-impact`
- `/api/execution/candidate-rehearsal`

## Canonical Read Models

- Outcome: `execution_candidate_outcome_for_draft`
- Blast radius: `execution_blast_radius_for_draft`
- Service impact: `execution_service_impact_for_draft`
- Forecast: `execution_readiness_forecast_for_draft`
- Rollback impact: `execution_rollback_impact_for_draft`
- Rehearsal: `operator_execution_rehearsal_preview`

## Canonical UI Surface

The existing Execution drawer is the canonical presentation surface. No new top-level navigation,
Simulation drawer, Impact drawer, or Candidate drawer family was introduced.

simulation_consolidation_complete=true
