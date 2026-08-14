# Production Snapshot Audit

## Command

Read-only SSH metadata scan of:

```text
/opt/v7/egress/state/intelligence/*.json
```

## Snapshot Files Observed

```text
blast-radius-summaries.json|1197|v7.intelligence.blast-radius-summaries.v1|2026-06-03T14:16:26.857257+00:00|FRESH|0.9934|1
channel-service-scores.json|2827|v7.intelligence.channel-service-scores.v1|2026-06-03T14:16:26.857257+00:00|FRESH|0.8953|7
overview-summary.json|2315|v7.intelligence.overview-summary.v1|2026-06-03T14:16:26.857257+00:00|FRESH|1.0|1
risk-summaries.json|1103|v7.intelligence.risk-summaries.v1|2026-06-03T14:16:26.857257+00:00|FRESH|0.9738|1
service-scores.json|4643|v7.intelligence.service-scores.v1|2026-06-03T14:16:26.857257+00:00|FRESH|0.8953|14
trust-summaries.json|1543|v7.intelligence.trust-summaries.v1|2026-06-03T14:16:26.857257+00:00|FRESH|1.0|1
```

## Missing Advisory Snapshot Families

Observed missing from production snapshot root:

```text
user-service-scores.json
candidate-suitability-summary.json
best-available-pool.json
prediction-summaries.json
trust-evolution-summaries.json
```

## Runtime Gate Observation

`/usr/local/bin/v7-users-autoswitch --pretty` reported:

```text
terminal_state=DRY_RUN
terminal_reason=dry_run_intelligence_snapshot_stop_required
snapshot_gate.stop_required=true
selected_move_count=0
apply_result.applied=false
```

The runtime gate treated required snapshot families as STOP due expired/source mismatch validation. This blocks approval readiness.

## Verdict

snapshot_root_exists=true

required_snapshot_files_present=true

advisory_snapshot_files_complete=false

snapshot_gate_stop_required=true

