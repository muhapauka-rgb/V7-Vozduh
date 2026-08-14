# Channel History Reality Map

## Existing Historical Channel Intelligence

| History Type | Owner | Windows / Retention | Storage | Status |
|---|---|---|---|---|
| Quality EMA windows | `tools/v7-egress-quality-compact` | `5m`, `1h`, `24h`, `7d` | `egress-quality-summary.json` | EXISTS |
| Bounded quality ring | `tools/v7-egress-quality-compact` | `DEFAULT_MAX_ITEMS=2000` | `egress-quality-ring.json` | EXISTS |
| RI service history windows | `ServiceHistoryStore` | `1h`, `24h`, `7d`, `30d` | derived from service matrix + quality summary | EXISTS as read model |
| Switch/audit execution history | autoswitch/runtime audit paths | bounded reads in workers, 1000 records / 512 KB tail | switch history/audit JSONL | EXISTS |
| Service matrix refresh events | `tools/v7-service-matrix-refresh-all` | daily JSONL events | `/opt/v7/events/service-matrix-refresh-*.jsonl` | EXISTS |

## Existing Aggregations

- EMA quality windows in `egress-quality-summary.json`.
- ServiceHistoryStore combines service matrix with quality windows.
- PredictiveFoundation provides disabled trend examples only.
- Trust worker reads bounded audit/switch history.
- Risk and blast workers consume service/trust summaries.

## Missing / Partial

- No production-confirmed `prediction-summaries.json` producer.
- No production-confirmed `capacity-forecast-summaries.json` producer.
- `user-service-scores.json` has a contract but is not in the six CONV.2 production-confirmed files.

## RI.4 Verdict

Historical quality already exists and must be reused.

RI.4 may extend history analysis through existing models/workers, but must not introduce a second history retention system.

