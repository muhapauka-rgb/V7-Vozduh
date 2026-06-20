# DATA GAP ANALYSIS

Project: V7 VOZDUH
Program: CAPACITY.2_OBSERVED_CAPACITY_MODEL_AUDIT
Mode: audit only
Last verified commit: `67fbd8506321802222c6f8ed3d34cfe406a45d8a`

## Existing Data

| Data | Exists | Adequacy |
| --- | --- | --- |
| Assigned users per egress | Yes | Good |
| Service matrix | Yes | Good |
| Runtime readiness | Yes | Good |
| Route readiness | Yes | Medium |
| Avg/min Mbps | Yes | Good |
| P95 latency | Yes | Good as service latency proxy |
| Fail rate | Yes | Good |
| Stability | Yes | Good |
| Rolling windows | Yes | Good (`5m`, `1h`, `24h`, `7d`) |
| Quality ring samples | Yes | Good for history, bounded |
| Planner blockers/reasons | Yes | Good for explanation |
| Intelligence snapshots | Yes | Good foundation |

## Missing or Weak Data

| Gap | Impact |
| --- | --- |
| Causal load-step history | Cannot confidently say user count caused degradation. |
| Per-channel user demand / traffic volume | User count alone may not represent load. |
| Packet loss | Current model uses service failure and latency proxies. |
| Provider-side CPU/RAM/bandwidth | V7 often does not own the tunnel; unavailable by design. |
| Controlled promotion/demotion samples | Needed to certify practical capacity safely. |
| Explicit tunnel ownership metadata | Needed to distinguish owned vs third-party confidence. |
| Confidence per observation | Needed before advisory output is trusted. |

## Future Telemetry Candidates

All future telemetry must remain read-only unless a separate implementation program approves it.

| Candidate | Purpose |
| --- | --- |
| `observed_capacity_samples.jsonl` | Append-only shadow evidence of users + quality. |
| `observed_capacity_summary.json` | Derived advisory snapshot. |
| Per-user traffic buckets | Better approximation of actual demand. |
| Packet loss / reconnect trend | Stronger degradation detection. |
| Ownership field | Mark `owned`, `third_party`, `unknown`. |
| Confidence score | Prevent premature planner use. |

## Audit Verdict

V7 has enough data to observe and learn. V7 does not yet have enough data to automate capacity changes.
