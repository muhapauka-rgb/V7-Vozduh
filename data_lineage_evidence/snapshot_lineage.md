# Snapshot Lineage Evidence

## Production Snapshot Root

Path: `/opt/v7/egress/state/intelligence`

Observed files:

| Snapshot | Exists | Bytes | Items | Generated At |
| --- | --- | ---: | ---: | --- |
| `service-scores.json` | true | 4643 | 14 | 2026-06-03T14:16:26.857257+00:00 |
| `channel-service-scores.json` | true | 2827 | 7 | 2026-06-03T14:16:26.857257+00:00 |
| `risk-summaries.json` | true | 1103 | 1 | 2026-06-03T14:16:26.857257+00:00 |
| `trust-summaries.json` | true | 1543 | 1 | 2026-06-03T14:16:26.857257+00:00 |
| `blast-radius-summaries.json` | true | 1197 | 1 | 2026-06-03T14:16:26.857257+00:00 |
| `overview-summary.json` | true | 2315 | n/a | 2026-06-03T14:16:26.857257+00:00 |

Expected but missing:

- `user-service-scores.json`
- `candidate-suitability-summary.json`
- `best-available-pool.json`
- `prediction-summaries.json`
- `trust-evolution-summaries.json`

## Refresh Dry-Run

Command:

`/usr/local/bin/v7-intelligence-snapshot-refresh --dry-run`

Result:

- `dry_run=true`
- `snapshot_count=11`
- `total_snapshot_bytes=546263`
- `max_snapshot_bytes=258235`
- `written={}`
- `warnings=[]`
- `runtime_behavior_changed=false`
- `governance_behavior_changed=false`
- `users_moved=false`

Dry-run snapshot sizes:

| Family | Bytes |
| --- | ---: |
| `best-available-pool` | 27875 |
| `blast-radius-summaries` | 1000 |
| `candidate-suitability-summary` | 91227 |
| `channel-service-scores` | 3530 |
| `overview-summary` | 2878 |
| `prediction-summaries` | 60293 |
| `risk-summaries` | 966 |
| `service-scores` | 17650 |
| `trust-evolution-summaries` | 258235 |
| `trust-summaries` | 1218 |
| `user-service-scores` | 81391 |

## Conclusion

The code path can build the full intelligence snapshot set. Production storage currently contains only the partial set. Full materialization must be done through the existing approved snapshot refresh path after outcome mappers are implemented and tested.
