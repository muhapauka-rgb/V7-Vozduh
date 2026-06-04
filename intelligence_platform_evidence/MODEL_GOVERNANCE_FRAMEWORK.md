# MODEL_GOVERNANCE_FRAMEWORK

Implemented in:

- `admin_core/intelligence_platform.py::model_governance_framework`

## Versions

```text
model_version=v7.intelligence-platform.model.v1
weights_version=v7.intelligence-platform.weights.v1
calibration_version=v7.intelligence-platform.calibration.v1
schema_version=v7.intelligence.model-governance.v1
```

## Compatibility Rules

- runtime-required snapshots must preserve schema/freshness/confidence/source hashes and item shape;
- advisory snapshots may be ignored when stale or low confidence;
- planner authority remains `tools/v7-users-autoswitch`.

## Migration Rules

- schema change: additive first;
- weight change: requires replay, forecast validation, drift review, and operator-visible certification;
- calibration change: requires before/after distribution comparison.

## Integration

Model governance metadata is now included in worker-produced service and prediction snapshot metadata.

## Verdict

```text
model_governance_implemented=true
```

