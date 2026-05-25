# V7 Phase 4 - Historical Reliability Scoring

## Purpose

Autoswitch must prefer reliable paths, not momentarily fast paths.

## Reliability Inputs

Use:

- long-term stability;
- degradation frequency;
- reconnect instability;
- quarantine history;
- maintenance frequency;
- service matrix history;
- quality fail rate;
- route verification failures.

## Current Inputs

Existing sources:

- `egress-quality-summary.json`;
- `egress-quality-ring.json`;
- `autoswitch-safety.json`;
- `client-reconnect-state.json`;
- `service-matrix.json`;
- `telegram-sentinel.json`;
- `switch-history.jsonl`.

## Scoring Rule

Fast current speed can improve score, but it must not override:

- hard service failures;
- route class mismatch;
- safety quarantine;
- repeated verification failures;
- user freeze/cooldown.

## Future Readiness

Historical reliability can later support prediction, but Phase 4 must remain deterministic and explainable.
