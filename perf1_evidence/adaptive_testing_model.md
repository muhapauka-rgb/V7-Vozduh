# PERF.1 Adaptive Testing Model

## Probe Classes

| Class | Purpose | Examples | Default frequency |
|---|---|---|---|
| L0 file freshness | cheap state freshness | mtime/hash checks | every planner/admin request if bounded |
| L1 light health | cheap service status | systemctl is-active, latest summary read | 30-60s |
| L2 light network | cheap HTTP/TCP probe | one endpoint per service class | 1-5m adaptive |
| L3 service matrix | multi-service/channel probes | Google, Telegram, ChatGPT, YouTube | 5-15m healthy, faster if suspect |
| L4 heavy diagnostics | deep route/domain/proxy tests | direct domain, trusted RU, proxy loopback | explicit or suspect only |
| L5 emergency verification | execution/rollback verify | selected user route checks | only after apply/rollback |

## Adaptive Rules

- Healthy channel: test less frequently.
- Suspicious channel: test more frequently but within network budget.
- Failed channel: quarantine candidate selection and test on shorter cadence until recovered.
- Expensive probes: never automatic in runtime path.
- Heavy test escalation requires a lower-level warning, stale critical snapshot, or explicit operator action.

## Channel States

- HEALTHY
- SUSPECT
- DEGRADED
- FAILED
- QUARANTINED
- RECOVERING
- STALE
- UNKNOWN

## Scheduling Budget

For 50 channels:

- L2 total budget: 50 probes/min max
- L3 total budget: 10 channel-service batches/min max
- L4 total budget: 5 heavy probes/min max
- Per-channel heavy cooldown: at least 5 minutes unless emergency verification

## Runtime Consumption

Runtime consumes:

- last status
- freshness
- confidence
- quarantine flag
- route-class suitability score

Runtime does not schedule probes.
