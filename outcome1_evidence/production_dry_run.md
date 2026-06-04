# Production Dry-Run

Command:

`ssh v7-vps '/usr/local/bin/v7-intelligence-snapshot-refresh --dry-run'`

Result:

```json
{
  "dry_run": true,
  "governance_behavior_changed": false,
  "metrics": {
    "elapsed_ms": 1218.194,
    "max_snapshot_bytes": 258254,
    "snapshot_count": 11,
    "snapshot_sizes": {
      "best-available-pool": 27893,
      "blast-radius-summaries": 1000,
      "candidate-suitability-summary": 91281,
      "channel-service-scores": 3528,
      "overview-summary": 2878,
      "prediction-summaries": 60285,
      "risk-summaries": 966,
      "service-scores": 17680,
      "trust-evolution-summaries": 258254,
      "trust-summaries": 1218,
      "user-service-scores": 79285
    },
    "total_snapshot_bytes": 544268
  },
  "runtime_behavior_changed": false,
  "snapshot_count": 11,
  "users_moved": false,
  "warnings": [],
  "written": {}
}
```

Boundary:

This was run against current production code. OUTCOME.1 code must be safe-deployed before mapper-enabled production dry-run can be certified.
