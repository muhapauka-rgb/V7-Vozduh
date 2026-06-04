# Snapshot Architecture Map

Canonical root:

```text
/opt/v7/egress/state/intelligence
```

## Snapshot Families

| Snapshot | Producer | Consumer | TTL | Runtime requirement | Stale behavior | Production-confirmed in CONV.2 |
|---|---|---|---:|---|---|---|
| `service-scores.json` | PERF.3 service score worker | runtime planner advisory reader | 120s | required_for_service_aware_apply | WARN | yes |
| `channel-service-scores.json` | PERF.3 service score worker | runtime planner channel ranking reader | 120s | required_for_service_aware_apply | WARN | yes |
| `user-service-scores.json` | PERF.3 user service weight worker | runtime planner advisory reader | 600s | advisory_only | IGNORE | no |
| `risk-summaries.json` | PERF.3 risk worker | runtime planner risk guard | 120s | required_for_intelligence_apply | STOP | yes |
| `trust-summaries.json` | PERF.3 audit trust aggregation worker | runtime planner trust guard | 600s | required_for_intelligence_apply | STOP | yes |
| `blast-radius-summaries.json` | PERF.3 risk/trust worker | runtime planner blast radius guard | 120s | required_for_intelligence_apply | STOP | yes |
| `capacity-forecast-summaries.json` | PERF.3 capacity worker contract | runtime planner capacity guard | 600s | required_for_capacity_apply | WARN | no |
| `prediction-summaries.json` | PERF.3 predictive worker contract | runtime planner advisory reader | 900s | advisory_only | IGNORE | no |
| `overview-summary.json` | PERF.3 admin performance worker | admin API overview reader | 60s | admin_only | IGNORE | yes |

## Canonical Flow

```text
Raw runtime data
  -> Heavy Brain workers
  -> Snapshot envelope files
  -> Runtime bounded readers
  -> Planner advisory/risk/trust/blast gate
```

## Production-CONV.2 Snapshot Set

CONV.2 verified exactly six files:

- `service-scores.json`
- `channel-service-scores.json`
- `risk-summaries.json`
- `trust-summaries.json`
- `blast-radius-summaries.json`
- `overview-summary.json`

## Stop Model

Runtime-required STOP families:

- `risk-summaries`
- `trust-summaries`
- `blast-radius-summaries`

Service-aware WARN families:

- `service-scores`
- `channel-service-scores`

Advisory-only IGNORE families:

- `user-service-scores`
- `prediction-summaries`

Admin-only:

- `overview-summary`

## RI.4 Verdict

Snapshot architecture exists and is production-confirmed for the six current files.

RI.4 may extend workers/snapshots inside this contract.

RI.4 must not create a second snapshot root or a second envelope model.

