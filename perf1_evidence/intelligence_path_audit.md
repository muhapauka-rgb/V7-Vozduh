# PERF.1 Intelligence Path Audit

## Service History

Current owner: `admin_core.routing_intelligence.ServiceHistoryStore`

Current cost:

- Builds from `service-matrix.json` and `egress-quality-summary.json`
- Cost grows by channels x services x windows

Future cost risk:

- 50 channels x 50 services x 4 windows is fine in background
- Rebuilding per runtime decision is not acceptable

Required architecture:

- precompute service history summaries
- runtime reads compact score per route class/channel

## Service Intelligence

Current owner: `ServiceIntelligenceEngine`

Current cost:

- Scores target/service windows in memory

Future cost risk:

- acceptable for background batch
- risky if repeated per user or per API request

Required architecture:

- heavy brain produces `service-scores`
- runtime consumes route-class suitability summaries

## User Weights

Current owner: `UserServiceWeights`

Current cost:

- Built from service preferences and required services

Future cost risk:

- 2000 users x service weights can be cheap if compact
- repeated normalization per candidate is avoidable

Required architecture:

- precompute user/service group weights
- group users with identical service requirements

## Execution Trust

Current owner: `ExecutionTrustModel`

Current cost:

- Reads bounded audit records today

Future cost risk:

- unbounded audit scan would become expensive

Required architecture:

- audit aggregation creates compact trust summary
- runtime never scans full audit history

## Dynamic Blast Radius

Current owner: `DynamicBlastRadiusModel`

Current cost:

- Cheap formula over compact inputs

Future cost risk:

- low if inputs stay compact
- high if it pulls live service history or audit scans

Required architecture:

- consume `risk-summaries`, `trust-summaries`, platform health summary

## Predictive Foundation

Current owner: `PredictiveFoundation`

Current cost:

- Model foundation exists in RI layer

Future cost risk:

- prediction can become CPU-heavy if it scans long windows or per-user histories

Required architecture:

- run prediction in Heavy Brain background workers
- publish compact `prediction-summaries`

## Admin API Read Views

Current owner: `admin/v7-admin-api` and `admin_core/*views.py`

Current cost:

- pure builders are cheap
- monolith still has many `run_readonly`, SQLite, JSONL, and command read paths

Future cost risk:

- overview and diagnostics can become slow if they trigger live probes or broad SQLite scans

Required architecture:

- admin overview reads snapshot bundles
- heavy diagnostics are explicit or background refreshed
