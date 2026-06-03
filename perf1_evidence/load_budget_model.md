# PERF.1 Load Budget Model

Target scale:

- 2000+ users
- 50+ channels
- 50+ service checks/classes over time

## Runtime Budgets

| Path | Target | Hard ceiling | Notes |
|---|---:|---:|---|
| planner decision dry-run | <= 250 ms | 500 ms | compact summaries only |
| single-user execution overhead | <= 2 s | 5 s | excludes unavoidable external tool wait |
| governance validation | <= 150 ms | 300 ms | packet and snapshot hashes only |
| rollback preparation | <= 250 ms | 500 ms | no history scan |
| audit append | <= 100 ms | 250 ms | no aggregation |
| closure state update/read | <= 100 ms | 250 ms | no large search |
| runtime snapshot read | <= 50 ms | 150 ms | bounded files |

## Admin API Budgets

| View | Target | Hard ceiling | Notes |
|---|---:|---:|---|
| overview from snapshot | <= 200 ms | 500 ms | no live probes |
| service summary read | <= 150 ms | 400 ms | from service snapshot |
| diagnostics page shell | <= 250 ms | 750 ms | no implicit heavy checks |
| explicit diagnostics action | async/explicit | bounded by command timeout | user-triggered only |
| traffic summary | <= 250 ms | 750 ms | compact SQLite summary or snapshot |

## Heavy Brain Budgets

| Work | Budget | Frequency |
|---|---:|---:|
| light service probes | <= 50 probes/min total | adaptive |
| heavy service probes | <= 5 probes/min total | only suspicious/failing |
| service history aggregation | <= 2 CPU seconds/run | 30-60s |
| trust aggregation | <= 1 CPU second/run | 1-5m |
| prediction summary | <= 5 CPU seconds/run | 5-15m |
| capacity forecast | <= 1 CPU second/run | 5m |
| log compaction | <= 2 CPU seconds/run | 1-5m |

## Disk and Log Budgets

- Keep runtime snapshots compact: target under 5 MB total for runtime-required intelligence summaries.
- Keep per-snapshot file under 1 MB where possible.
- Keep raw rings bounded; no runtime dependency on unbounded JSONL.
- Keep audit/event aggregation summaries separate from raw append logs.

## Network Probe Budgets

For 50 channels:

- light HTTP/TCP health: adaptive, default 10-20% of channels per minute
- suspicious channels: 1-3 minute cadence
- healthy channels: 5-15 minute cadence
- heavy multi-endpoint tests: only after warning or explicit operator request

## Memory Budgets

- Runtime planner: target under 128 MB RSS incremental cost.
- Heavy Brain worker: target under 512 MB RSS for 2000 users / 50 channels.
- Admin API request: target no large history materialization; use pagination and snapshots.
