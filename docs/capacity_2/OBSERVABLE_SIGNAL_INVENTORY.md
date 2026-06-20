# OBSERVABLE SIGNAL INVENTORY

Project: V7 VOZDUH
Program: CAPACITY.2_OBSERVED_CAPACITY_MODEL_AUDIT
Mode: audit only
Last verified commit: `67fbd8506321802222c6f8ed3d34cfe406a45d8a`

## Inventory

| Signal | Exists | Source | Useful for observed capacity? | Notes |
| --- | --- | --- | --- | --- |
| Assigned users | Yes | runtime user/channel state, planner egress model | Strong | Required independent variable. |
| Service matrix | Yes | `v7-service-matrix-refresh-all`, `v7-service-matrix-test`, `service-matrix.json` | Strong | Detects service failures and partial degradation. |
| Avg Mbps | Yes | `v7-state.json`, `egress-speed.json`, quality compact summary | Strong | Direct throughput symptom. |
| Min Mbps | Yes | same as speed inputs | Strong | Good collapse detector; less forgiving than avg. |
| P95 latency | Yes | service matrix latencies compacted by `v7-egress-quality-compact` | Strong | SRE-style latency degradation signal. |
| Fail rate | Yes | service failures / health severity compacted by `v7-egress-quality-compact` | Strong | SRE-style error signal. |
| Stability | Yes | runtime state, speed summary, quality summary, planner gates | Strong | Detects flapping/unstable transport. |
| Runtime readiness | Yes | `egress_runtime_readiness`, runtime read models | Medium | Detects missing/down interfaces and stale runtime state. |
| Route readiness | Yes | route reality/readiness helpers and topology state | Medium | Useful only when route evidence is real; not throughput by itself. |
| History windows | Yes | quality summary windows `5m`, `1h`, `24h`, `7d` | Strong | Required for trend and capacity-learning confidence. |
| Planner candidate reasons | Yes | `tools/v7-users-autoswitch` candidate JSON | Medium | Explains blockers; not a measurement itself. |
| Intelligence snapshots | Yes | `admin_core/intelligence_workers.py`, `v7-intelligence-snapshot-refresh` | Medium | Read-only derived evidence and forecasting foundation. |
| Shadow autonomy records | Yes | `admin_core/shadow_autonomy.py` | Medium | Useful pattern for observe/learn/recommend safety. |
| CPU/RAM | No | not owned/observed for third-party tunnels | Not available | Do not infer. |
| Provider bandwidth limit | No | third-party infrastructure | Not available | Do not invent. |
| Packet loss | Partial / not canonical | service failures and latency are proxies | Future gap | Add only as telemetry, not assumed now. |
| Real per-user traffic demand | Partial | assigned users and total traffic views exist, but not enough for causal capacity | Future gap | Needed for robust observed-capacity learning. |

## Existing Quality Compaction

`tools/v7-egress-quality-compact` already builds rolling quality windows with:

- `avg_mbps`
- `min_mbps`
- `p95_latency_ms`
- `fail_rate`
- `stability`
- `users`
- health code / severity

This is the closest existing source for an observed-capacity model.

## Audit Verdict

V7 already observes enough symptoms to build a shadow observed-capacity model. V7 does not yet have enough causal evidence to let that model influence planner assignment automatically.
