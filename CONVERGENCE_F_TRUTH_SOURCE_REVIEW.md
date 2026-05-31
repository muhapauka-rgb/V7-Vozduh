# Convergence F Truth Source Review

Project: V7 Vozduh
Block: Convergence F

## Simulation Truth Sources

| Domain | Canonical truth source | Derived sources | Presentation sources |
|---|---|---|---|
| Outcome | `execution_candidate_outcome_for_draft` | validation preview, service impact, blast radius, rollback impact, readiness forecast | `/api/execution/outcome-preview`, Execution drawer |
| Blast Radius | `execution_blast_radius_for_draft` | draft affected users, users registry, target capacity, service impact | `/api/execution/blast-radius`, Execution drawer |
| Service Impact | `execution_service_impact_for_draft` | service matrix, required services from draft metadata | `/api/execution/service-impact`, Execution drawer |
| Simulation | candidate outcome model | all preview-only impact/readiness models | Outcome preview API and candidate rehearsal mapping |
| Forecast | `execution_readiness_forecast_for_draft` | validation preview checks | `/api/execution/readiness-forecast`, Execution drawer |

## Conflict Review

No competing persistent truth source was introduced. The public routes are wrappers around existing
derived read models and keep `read_only`, `non_authoritative`, `preview_only`, and
`execution_allowed_now=false` semantics.

truth_source_review_complete=true
