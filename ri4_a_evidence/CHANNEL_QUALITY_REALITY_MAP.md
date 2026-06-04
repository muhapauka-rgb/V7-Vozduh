# Channel Quality Reality Map

## Existing Measurements

| Measurement | Owner / Producer | Storage | Consumer |
|---|---|---|---|
| service HTTP/TCP reachability | `tools/v7-service-matrix-test` | `service-matrix.json` | service-aware routing, RI, admin service views |
| Telegram TCP/DC health | `tools/v7-service-matrix-test`, `tools/v7-telegram-sentinel` | `service-matrix.json`, sentinel state | autoswitch, admin, service summaries |
| speed/throughput | runtime state tools and `v7-egress-quality-compact` | `v7-state.json`, `egress-speed.json`, `egress-quality-summary.json` | autoswitch, RI, admin diagnostics |
| latency | service matrix rows and quality compact | service rows, `p95_latency_ms` windows | RI service scoring, service views |
| fail rate | `v7-egress-quality-compact` | `egress-quality-summary.json` | RI history/scoring |
| stability | runtime state / quality compact | `egress-quality-summary.json`, egress state | autoswitch quality guard, RI service score |
| reconnect/disconnect | autoswitch safety/reconnect state | `client-reconnect-state.json`, switch history | autoswitch planner |

## Quality Scores Already Calculated

- `tools/v7-egress-quality-compact::score_for()` computes quality score from avg Mbps, min Mbps, latency, stability and fail rate.
- `ServiceIntelligenceEngine.score_service()` computes per-service score using availability, latency, throughput, error rate, stability, confidence and freshness.
- `tools/v7-users-autoswitch` computes native service suitability and candidate `score_parts`.
- `RoutingBrain.candidate_advisory_scores()` computes bounded RI `score_part`.
- Snapshot workers produce compact channel/service scores.

## Storage

Canonical quality stores:

- `/opt/v7/egress/state/egress-quality-summary.json`
- `/opt/v7/egress/state/egress-quality-ring.json`
- `/opt/v7/egress/state/service-matrix.json`
- `/opt/v7/egress/state/v7-state.json`
- `/opt/v7/egress/state/egress-speed.json`

Derived intelligence stores:

- `/opt/v7/egress/state/intelligence/channel-service-scores.json`
- `/opt/v7/egress/state/intelligence/service-scores.json`

## RI.4 Classification

Quality collection: REUSE.

Quality summarization: REUSE.

Quality scoring: EXTEND only in `ServiceIntelligenceEngine` or worker outputs.

New channel quality store: DO_NOT_CREATE.

