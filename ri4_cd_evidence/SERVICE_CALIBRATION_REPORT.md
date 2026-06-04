# SERVICE_CALIBRATION_REPORT

## Implemented Calibration Guards

Implemented in `admin_core/intelligence_workers.py`:

- per-service score distribution;
- per-channel aggregate score distribution;
- spread;
- standard deviation;
- rounded distinct score count;
- compression states:
  - `OK`
  - `LOW_SPREAD`
  - `COLLAPSED_IDENTICAL`
  - `HIGH_SCORE_COMPRESSION`
  - `LOW_SCORE_COMPRESSION`

## Probe Score Preservation

RI4.CD blends the richer service-specific criteria with existing `service_matrix.score`.

Reason:

Existing probe truth already carries calibrated runtime knowledge. Ignoring it flattened scores and reduced user-weight differentiation during tests. Blending preserves old truth while adding new detail.

## Test Result

Focused test suite initially detected score compression in routing-brain ranking. Calibration was adjusted and the focused suite then passed.

```text
focused_tests=52 OK
full_tests=256 OK
```

## Verdict

```text
score_spread_guard_implemented=true
confidence_spread_guard_implemented=true
degradation_sensitivity_implemented=true
service_differentiation_preserved=true
```

