# TRUST_FORECAST_MODEL

Output section: `prediction-summaries.items[0].trust_forecast`

Schema: `ri5.trust-forecast.v1`

## Inputs

- existing `trust-summaries` snapshot;
- successful execution counters;
- successful rollback counters;
- failed execution counters;
- failed rollback counters;
- governance violation counters.

## Predictions

- trust trend;
- trust growth;
- trust decline;
- trust confidence.

## Authority

```text
runtime_decision_authority=none_prediction_only
```

