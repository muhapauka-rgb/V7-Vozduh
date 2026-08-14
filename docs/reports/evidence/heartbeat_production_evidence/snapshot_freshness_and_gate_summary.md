# Snapshot Freshness And Gate Summary

Program: PROGRAM_HEARTBEAT_PRODUCTION_MATERIALIZATION_AND_OPERATOR_VISIBLE_CERTIFICATION
Date: 2026-06-04
Root: /opt/v7/egress/state/intelligence

## Snapshot Files

All required and extended snapshot families were present and freshly written.

Observed generated_at:

```text
2026-06-04T15:06:59.808784+00:00
```

Observed mtime window:

```text
2026-06-04T15:07:01Z
```

Families:

- service-scores.json: FRESH, confidence=0.8469, item_count=14
- channel-service-scores.json: FRESH, confidence=0.8469, item_count=7
- risk-summaries.json: FRESH, confidence=0.9617, item_count=1
- trust-summaries.json: FRESH, confidence=1.0, item_count=1
- blast-radius-summaries.json: FRESH, confidence=0.9904, item_count=1
- overview-summary.json: FRESH, confidence=1.0, item_count=1
- user-service-scores.json: FRESH, confidence=0.8532, item_count=18
- candidate-suitability-summary.json: FRESH, confidence=0.8466, item_count=18
- best-available-pool.json: FRESH, confidence=0.9617, item_count=18
- prediction-summaries.json: FRESH, confidence=0.957, item_count=1
- trust-evolution-summaries.json: FRESH, confidence=0.9804, item_count=1

## Runtime Gate

Production dry-run showed the pre-planner refresh path itself is healthy:

```json
{
  "pre_state": "REFRESH_DRY_RUN_SUCCESS",
  "pre_decision": "refresh_path_validated",
  "pre_stop_required": false,
  "pre_snapshot_count": 11,
  "pre_source_stable": true,
  "pre_source_errors": []
}
```

However, the runtime snapshot gate still failed source-hash consistency after loading snapshots:

```json
{
  "gate_stop_required": true,
  "gate_stop_families": ["channel-service-scores", "service-scores"],
  "gate_source_mismatch_families": ["channel-service-scores", "service-scores"],
  "service_errors": [
    "source_hash_mismatch:service-scores:service_matrix",
    "source_hash_mismatch:service-scores:quality_summary"
  ],
  "channel_errors": [
    "source_hash_mismatch:channel-service-scores:service_matrix",
    "source_hash_mismatch:channel-service-scores:quality_summary"
  ]
}
```

## Interpretation

The snapshot writer can produce fresh snapshots, but the planner's post-refresh source hash validation can observe different service_matrix and quality_summary hashes. The system correctly fails closed:

- intelligence_present=false
- planner_influence_active=false
- selected_move_count=0
- apply_result.applied=false

## Verdict

snapshot_files_fresh=true
snapshot_source_consistency_certified=false
snapshot_freshness_certified=false

