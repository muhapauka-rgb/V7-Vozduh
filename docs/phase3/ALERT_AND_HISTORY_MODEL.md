# V7 Phase 3 - Alert And Historical Quality Model

## Purpose

V7 must avoid alert spam and unbounded telemetry.

History should support decisions while staying compact.

## Alert Philosophy

Alerts must be:

- grouped;
- deduplicated;
- severity-aware;
- actionable;
- tied to affected object;
- safe-action oriented.

Alerts must not be:

- raw metric spam;
- repeated every timer tick;
- unrelated to operator decisions;
- shown without suggested action.

## Historical Quality

Use bounded summaries:

- EMA windows;
- degradation frequency;
- instability score;
- reconnect trends;
- service failure counts;
- MTU/path stability flags.

Existing related files:

- `egress-quality-summary.json`;
- `egress-quality-ring.json`;
- `path-samples.json`;
- `path-benchmark.json`;
- `autoswitch-safety.json`;
- `client-reconnect-state.json`.

## Retention

Default rule:

- keep compact summaries long enough to explain trends;
- keep bounded recent samples;
- do not store infinite raw telemetry.

## Future Foundation

This model prepares for:

- predictive degradation;
- adaptive routing;
- AI-assisted diagnostics;
- transport intelligence.

It does not implement AI in Phase 3.
