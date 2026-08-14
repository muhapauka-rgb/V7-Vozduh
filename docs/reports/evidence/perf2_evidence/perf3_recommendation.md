# PERF.2 PERF.3 Recommendation

PERF.3 should create background Intelligence Workers that generate snapshots.

## Required Workers

| Worker | Output | Cadence |
|---|---|---:|
| service score worker | `service-scores.json` | 60s |
| channel service score worker | `channel-service-scores.json` | 60s |
| user service weight worker | `user-service-scores.json` | 300s |
| risk worker | `risk-summaries.json` | 60s |
| audit trust aggregation worker | `trust-summaries.json` | 300s |
| blast radius worker | `blast-radius-summaries.json` | 60s |
| capacity worker | `capacity-forecast-summaries.json` | 300s |
| predictive worker | `prediction-summaries.json` | 600s |
| admin performance worker | `overview-summary.json` | 30s |

## Constraints

Workers may:

- read raw service/history/traffic/audit inputs
- compute heavy intelligence
- write complete snapshot envelopes atomically

Workers must not:

- move users
- approve execution
- mutate governance
- mutate runtime route state
- restart services
- bypass planner

## Recommended PERF.3 First Step

Implement service score and trust summary producers first because they remove the largest future runtime pressure.
