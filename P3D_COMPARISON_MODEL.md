# P3.D Comparison Model

Project: V7 Vozduh
Block: P3.D Dry-Run Verification

## Implemented Comparison States

- `VERIFIED_MATCH`
- `VERIFIED_MISMATCH`
- `INCONCLUSIVE`
- `STALE`
- `NOT_VERIFIED`

## Rules

- Missing prediction: `NOT_VERIFIED`
- Invalid/forbidden prediction output: `INCONCLUSIVE`
- Missing observed outcome: `NOT_VERIFIED`
- Prediction older than TTL: `STALE`
- Prediction equals observed outcome: `VERIFIED_MATCH`
- Prediction differs from observed outcome: `VERIFIED_MISMATCH`

## Verdict

`comparison_model_defined=true`

