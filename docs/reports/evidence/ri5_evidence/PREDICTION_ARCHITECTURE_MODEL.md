# PREDICTION_ARCHITECTURE_MODEL

Schema: `ri5.prediction-architecture.v1`

Owner: `PredictiveFoundation`

## Prediction Domains

- Channel Quality
- Service Quality
- Risk
- Trust
- Recovery
- Degradation
- Capacity
- Blast Radius

## Architecture

```text
ServiceHistoryStore
-> PredictiveFoundation
-> intelligence_workers
-> prediction-summaries.json
-> runtime planner optional advisory read
```

## Authority

```text
prediction=advice_only
planner_decision_owner=tools/v7-users-autoswitch
governance_authority=unchanged
execution_authority=none
selected_moves_write_authority=none
runtime_mutation_authority=none
```

## Runtime Rule

Runtime may read `prediction-summaries.json`.

Runtime may not compute forecasts.

