# PERF.3 Service Score Worker

## Inputs

- `service-matrix.json`
- `egress-quality-summary.json`
- `service-preferences.json`

## Outputs

- `service-scores.json`
- `channel-service-scores.json`

## Reused Logic

- `ServiceHistoryStore.from_runtime_inputs`
- `UserServiceWeights.from_service_preferences`
- `ServiceIntelligenceEngine.score_service`
- `ServiceIntelligenceEngine.score_all_targets`

## Output Shape

`service-scores.json` contains compact per-service aggregates:

- service
- target_count
- average_score
- confidence
- low_targets
- runtime_decision_authority=`none_snapshot_only`

`channel-service-scores.json` contains compact per-channel aggregates:

- channel
- aggregate_score
- verdict
- confidence
- required_missing
- required_low
- runtime_decision_authority=`none_snapshot_only`

## Failure Behavior

Missing service matrix or quality summary yields valid snapshots with warnings:

- `service_matrix_missing_or_empty`
- `quality_summary_missing_or_empty`

Confidence drops instead of failing runtime.
