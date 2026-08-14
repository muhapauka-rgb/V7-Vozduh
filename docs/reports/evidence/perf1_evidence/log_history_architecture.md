# PERF.1 Log and History Architecture

## Rule

Runtime must not scan large history directly.

## Raw Logs

Raw append stores remain authoritative evidence:

- audit logs
- switch history JSONL
- operation lifecycle records
- service probe samples
- route reality probe outputs
- traffic raw or SQLite stores

Raw logs are not runtime decision inputs directly.

## Aggregation Layers

| Aggregation | Input | Output |
|---|---|---|
| Audit aggregation | audit/event JSONL | `trust-summaries.json` |
| Execution history aggregation | switch history | `execution-history-summary.json` |
| Service history aggregation | service matrix + quality ring | `service-scores.json` |
| Route reality aggregation | route probes | `route-reality-summary.json` |
| Traffic aggregation | SQLite/raw counters | `traffic-summary.json` |
| Capacity aggregation | registries + usage | `capacity-forecast-summaries.json` |

## Compaction

- Raw JSONL remains append-only for audit value.
- Runtime-facing summaries are compact JSON snapshots.
- Ring buffers stay bounded by item count and age.
- Large history windows are represented by EMA/percentiles/counts, not full samples.

## Retention

- Runtime summaries: keep latest plus short prior history.
- Raw audit: retain per compliance/ops policy.
- Probe rings: bounded by size and age.
- Admin export: explicit, paginated, never runtime-triggered.
