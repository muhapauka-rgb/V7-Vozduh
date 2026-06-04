# PREDICTION_ACCURACY_MODEL

Status: PASS

Implementation:

- `prediction_accuracy_model`
- worker extraction of RI5 channel and service forecasts from `prediction-summaries`

Forecast domains:

- channel_quality
- service_quality
- risk
- trust
- recovery
- degradation

Important behavior:

- Forecasts without actual outcomes are marked `PENDING_OUTCOME`.
- Missing live actuals produce `LIVE_OUTCOME_REQUIRED`.
- RI6 does not treat pending forecasts as validated accuracy.

