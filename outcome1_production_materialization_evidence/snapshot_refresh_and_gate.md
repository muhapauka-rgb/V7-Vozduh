# OUTCOME.1 Production Materialization - Snapshot Refresh And Runtime Gate Evidence

## Stable Snapshot Refresh

Production command:

```text
/usr/local/bin/v7-intelligence-snapshot-refresh --max-source-retries 12 --source-retry-sleep-sec 0.2
```

Result:

- dry_run: `false`
- source_stable: `true`
- source_consistency_attempts: `1`
- source_consistency_errors: `[]`
- snapshot_count: `11`
- warnings: `[]`
- total_snapshot_bytes: `546305`
- max_snapshot_bytes: `258490`
- runtime_behavior_changed: `false`
- governance_behavior_changed: `false`
- users_moved: `false`

Written snapshot families:

- `service-scores`
- `channel-service-scores`
- `user-service-scores`
- `risk-summaries`
- `trust-summaries`
- `blast-radius-summaries`
- `candidate-suitability-summary`
- `best-available-pool`
- `prediction-summaries`
- `trust-evolution-summaries`
- `overview-summary`

## Runtime Snapshot Gate

Production command:

```text
/usr/local/bin/v7-users-autoswitch --pretty
```

Result:

- operation terminal_state: `DRY_RUN`
- operation selected_move_count: `0`
- apply_result.applied: `false`
- apply_result.reason: `dry_run`
- snapshot_gate.active: `true`
- snapshot_gate.stop_required: `false`
- snapshot_gate.stop_families: `[]`
- snapshot_gate.source_mismatch_families: `[]`
- all checked snapshot families: `ALLOW`

Selected representative families:

- `service-scores`: validation_ok `true`, freshness `FRESH`, item_count `14`, confidence `0.8468`
- `channel-service-scores`: validation_ok `true`, freshness `FRESH`, item_count `7`, confidence `0.8468`
- `user-service-scores`: validation_ok `true`, freshness `FRESH`, item_count `18`, confidence `0.853`
- `candidate-suitability-summary`: validation_ok `true`, freshness `FRESH`, item_count `18`, confidence `0.8444`
- `prediction-summaries`: validation_ok `true`, freshness `FRESH`, item_count `1`, confidence `0.957`
- `trust-evolution-summaries`: validation_ok `true`, freshness `FRESH`, item_count `1`, confidence `0.9802`

## RI6 Live Outcome Counts

Production `trust-evolution-summaries.json`:

- generated_at: `2026-06-04T13:18:35.433908+00:00`
- prediction_actuals_count: `21`
- service_actuals_count: `21`
- candidate_outcomes_count: `67`
- prediction_validation_status: `VALIDATED`
- live_calibrated: `1`
- suitability_trust.candidates_seen: `90`
- suitability_trust.outcomes_seen: `67`
