# E35.E Failure Model

## Failure Behavior

| Failure | Behavior |
|---|---|
| Store unreadable | fail closed; authority health DEGRADED; no ALLOW |
| Events unreadable | timeline degraded; state can still read; audit warning |
| Adapter failure | read model unavailable; REVIEW_REQUIRED |
| API failure | admin shows unavailable; evaluator must not use stale API payload |
| Admin failure | runtime unaffected; operator sees error |
| Evaluator input missing | DENY or REVIEW_REQUIRED depending input category |
| Conflict input missing | REVIEW_REQUIRED |
| Source hash mismatch | read-path drift; REVIEW_REQUIRED |

## Fail Open?

No authority read-path failure may fail open for forward movement.

## Emergency?

Emergency requires valid emergency/containment input. Store/read failure alone does not create `EMERGENCY_ONLY`.

## Verdict

```text
failure_model_defined=true
```
