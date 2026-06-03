# PERF.1 Snapshot Architecture

## Snapshot Store

Proposed root:

- `/opt/v7/egress/state/intelligence/`

Repository contract location:

- future `admin_core/intelligence_snapshots.py`
- future schema evidence under `perf2_evidence/`

## Snapshot Envelope

Every snapshot should include:

- schema
- generated_at
- expires_at
- ttl_seconds
- freshness_state
- confidence
- source_hashes
- generator
- input_window
- item_count
- compact items
- warnings

## Required Snapshot Families

| Snapshot | Owner | TTL | Update frequency | Runtime use |
|---|---|---:|---:|---|
| `service-scores.json` | Heavy Brain service worker | 60s | 30-60s | route-class suitability |
| `channel-service-scores.json` | Heavy Brain service worker | 60s | 30-60s | channel ranking |
| `user-service-scores.json` | Heavy Brain user-weight worker | 300s | on preference change or 5m | user/group preference match |
| `risk-summaries.json` | Heavy Brain risk worker | 60s | 30-60s | runtime risk guard |
| `trust-summaries.json` | Audit aggregation worker | 300s | on audit growth or 5m | execution trust guard |
| `blast-radius-summaries.json` | Risk/trust worker | 60s | 30-60s | selected move cap advice |
| `capacity-forecast-summaries.json` | Capacity worker | 300s | 5m | scaling/capacity guard |
| `prediction-summaries.json` | Predictive worker | 300s | 5-15m | advisory only |
| `overview-summary.json` | Admin performance worker | 10-30s | mtime/hash changed | admin response speed |

## Freshness Rules

- Runtime-required snapshot stale: stop or degrade to planner-only hard gates, depending policy.
- Advisory-only snapshot stale: ignore advisory, do not block hard-gate planner.
- UNKNOWN freshness: STOP for live apply.
- Admin overview stale: show stale badge, do not trigger heavy recompute implicitly.

## Confidence Rules

- confidence >= 0.8: normal advisory
- 0.5 <= confidence < 0.8: reduced advisory weight
- confidence < 0.5: advisory ignored for runtime
- confidence UNKNOWN: advisory ignored
