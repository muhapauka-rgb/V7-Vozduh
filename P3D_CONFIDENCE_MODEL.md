# P3.D Confidence Model

Project: V7 Vozduh
Block: P3.D Dry-Run Verification

## Confidence Values

- `HIGH`
- `MEDIUM`
- `LOW`
- `UNKNOWN`

## Rules

- `NOT_VERIFIED`, `INCONCLUSIVE`, `STALE` produce low confidence.
- `VERIFIED_MISMATCH` produces medium confidence and requires review.
- `VERIFIED_MATCH` with weak freshness produces medium confidence.
- `VERIFIED_MATCH` with strong prediction and observation confidence produces high confidence.
- Otherwise confidence degrades to medium or low.

## Verdict

`confidence_model_defined=true`

