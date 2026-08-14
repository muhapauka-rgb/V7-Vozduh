# DRIFT_DETECTION_FRAMEWORK

Implemented in:

- `admin_core/intelligence_platform.py::drift_detection_framework`

## Detects

- prediction drift;
- service scoring drift;
- suitability drift;
- trust drift;
- risk drift.

## Runtime Boundary

Drift detection is not performed in runtime hot path.

## Verdict

```text
drift_detection_implemented=true
runtime_drift_analysis=false
```

