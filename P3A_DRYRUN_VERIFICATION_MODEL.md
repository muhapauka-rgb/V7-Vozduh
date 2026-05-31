# P3.A Dry-Run Verification Model

Project: V7 Vozduh
Block: P3.A Runtime Dry-Run Foundation

## Purpose

Dry-run verification compares earlier dry-run predictions with later observed reality. It verifies the model, not a runtime action.

## Verification States

| State | Meaning |
| --- | --- |
| `NOT_VERIFIED` | No later evidence is available yet. |
| `VERIFIED_MATCH` | Later evidence matches the prediction. |
| `VERIFIED_MISMATCH` | Later evidence contradicts the prediction. |
| `INCONCLUSIVE` | Evidence is insufficient or conflicting. |
| `STALE` | Contract expired before verification. |

## Verification Targets

| Target | Verification question |
| --- | --- |
| Decision | Was `WOULD_BLOCK`, `WOULD_REVIEW`, `WOULD_MOVE`, `NO_ACTION` or `WOULD_ROLLBACK` consistent with later evidence? |
| Gate result | Did each gate predict the later observed constraint accurately? |
| Service impact | Did predicted service impact match observed health trend? |
| Trust impact | Did trust evidence remain consistent with the prediction? |
| Rollback readiness | Did rollback prerequisites remain available? |
| Candidate stability | Did the candidate remain equivalent or become stale? |

## Verification Inputs

- Later runtime event observations.
- Later service matrix and sentinel evidence.
- Later trust and route truth evidence.
- Later execution preview events.
- Later audit records.
- Original contract input hashes.

## Fail-Closed Verification Rules

- Missing source references produce `INCONCLUSIVE`.
- Expired contracts produce `STALE`.
- Source hash mismatch produces `INCONCLUSIVE` unless the mismatch itself is the finding.
- Any evidence of hidden movement invalidates `WOULD_MOVE` predictions.
- Verification must not trigger rollback or autoswitch.

## Verification Verdict

`dryrun_verification_defined=true`

