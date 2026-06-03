# PERF.2 Snapshot Envelope and Families

## Universal Envelope

Schema: `v7.intelligence-snapshot-envelope.v1`

Required fields:

- `schema`
- `generated_at`
- `expires_at`
- `ttl_seconds`
- `freshness_state`
- `confidence`
- `source_hashes`
- `generator`
- `item_count`
- `warnings`

Optional fields:

- `confidence_factors`
- `items`
- `summary`
- `metadata`

## Snapshot Families

| Family | File | Schema | Runtime role |
|---|---|---|---|
| service-scores | `service-scores.json` | `v7.intelligence.service-scores.v1` | service-aware advisory |
| channel-service-scores | `channel-service-scores.json` | `v7.intelligence.channel-service-scores.v1` | channel ranking |
| user-service-scores | `user-service-scores.json` | `v7.intelligence.user-service-scores.v1` | advisory-only |
| risk-summaries | `risk-summaries.json` | `v7.intelligence.risk-summaries.v1` | runtime risk guard |
| trust-summaries | `trust-summaries.json` | `v7.intelligence.trust-summaries.v1` | execution trust guard |
| blast-radius-summaries | `blast-radius-summaries.json` | `v7.intelligence.blast-radius-summaries.v1` | blast-radius guard |
| capacity-forecast-summaries | `capacity-forecast-summaries.json` | `v7.intelligence.capacity-forecast-summaries.v1` | capacity guard |
| prediction-summaries | `prediction-summaries.json` | `v7.intelligence.prediction-summaries.v1` | advisory-only |
| overview-summary | `overview-summary.json` | `v7.intelligence.overview-summary.v1` | admin-only |

## No Runtime Usage Yet

PERF.2 defines contracts and readers only.

Planner integration is explicitly deferred to PERF.4.
