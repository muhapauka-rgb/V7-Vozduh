# RISK_FORECAST_MODEL

Output section: `prediction-summaries.items[0].risk_forecast`

Schema: `ri5.risk-forecast.v1`

## Inputs

- existing `risk-summaries` snapshot;
- channel forecast degradation probabilities;
- channel forecast recovery probabilities.

## Predictions

- current risk;
- future risk;
- risk growth;
- risk reduction;
- risk confidence.

## Authority

```text
runtime_decision_authority=none_prediction_only
```

