# E35.E Drift Detection Model

## Definition

Read Path Drift occurs when two layers show different authority reality for the same object and source version.

Example:

```text
Store says OPERATOR_PINNED
API says AUTO
Admin says AUTO
Evaluator says OPERATOR_PINNED
```

## Detection

Compare:

- source hash;
- authority state version;
- event high-watermark;
- user id;
- routing mode;
- owner;
- target;
- status.

## Severity

| Drift | Severity |
|---|---|
| Store vs Adapter mismatch | HIGH |
| Adapter vs API mismatch | HIGH |
| API vs Admin label mismatch | MEDIUM |
| API vs Evaluator mismatch | HIGH |
| Evaluator vs Conflict Resolver mismatch | HIGH |
| Event timeline stale only | MEDIUM |

## Reporting

Admin must show:

- drift detected;
- layer mismatch;
- affected user/channel;
- source hash;
- next safe action.

## Failure Behavior

Forward movement:

```text
DENY or REVIEW_REQUIRED
```

Never `ALLOW`.

## Verdict

```text
drift_detection_defined=true
```
