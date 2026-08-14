# SERVICE_FORECAST_MODEL

Output section: `prediction-summaries.items[0].service_forecasts`

Schema: `ri5.service-forecast.v1`

## Services

- Telegram
- YouTube
- Instagram
- ChatGPT
- generic/default services when present in history

## Predictions

- future quality;
- future degradation probability;
- future recovery probability;
- future stability;
- future confidence.

## Authority

```text
runtime_decision_authority=none_prediction_only
```

