# CHANNEL_FORECAST_MODEL

Output section: `prediction-summaries.items[0].channel_forecasts`

Schema: `ri5.channel-forecast.v1`

## Inputs

- `ServiceHistoryStore`
- service quality scores by window
- service stability by window
- service confidence by window

## Predictions

- quality trend;
- failure probability;
- degradation probability;
- recovery probability;
- stability forecast;
- confidence.

## Windows Used

- `1h`
- `24h`
- `7d`
- `30d`

## Authority

```text
runtime_decision_authority=none_prediction_only
```

