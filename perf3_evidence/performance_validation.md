# PERF.3 Performance Validation

## CLI Dry Run

Temporary fixture dry-run:

- command: `tools/v7-intelligence-snapshot-refresh --dry-run --pretty`
- rc: 0
- snapshots: 6
- elapsed_ms: 0.896
- total_snapshot_bytes: 7572
- max_snapshot_bytes: 1879
- runtime_behavior_changed: false
- governance_behavior_changed: false
- users_moved: false

## 50-Channel Synthetic Benchmark

Inputs:

- 50 channels
- 2000 users
- 10 required services
- 500 audit records

Result:

- elapsed_ms: 37.043
- worker_reported_elapsed_ms: 36.844
- snapshot_count: 6
- total_snapshot_bytes: 18465
- max_snapshot_bytes: 10009
- warnings: []

Snapshot sizes:

- blast-radius-summaries: 1012 bytes
- channel-service-scores: 10009 bytes
- overview-summary: 1872 bytes
- risk-summaries: 941 bytes
- service-scores: 3459 bytes
- trust-summaries: 1172 bytes

## Verdict

50-channel scale is feasible for PERF.3 producer scope.

Generated snapshots remain small and far below the PERF.2 1 MB read bound.
