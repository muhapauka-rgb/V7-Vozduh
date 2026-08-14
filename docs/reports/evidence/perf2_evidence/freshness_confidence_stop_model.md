# PERF.2 Freshness, Confidence, and Stop Model

## Freshness States

- `FRESH`: inside stale window and not expired
- `STALE`: older than stale window but not expired
- `EXPIRED`: past `expires_at`
- `UNKNOWN`: missing, corrupt, invalid, future-dated, or unknown timestamps

## Runtime Behavior

| State | Default runtime behavior |
|---|---|
| FRESH | ALLOW |
| STALE | family-specific WARN, IGNORE, or STOP |
| EXPIRED | STOP |
| UNKNOWN | STOP |

## Stop Conditions

Runtime must stop for:

- missing snapshot when snapshot is requested
- corrupt snapshot
- schema mismatch
- invalid envelope
- UNKNOWN freshness
- EXPIRED freshness
- low confidence on runtime-required snapshots
- snapshot too large

## Confidence Model

Range: `0.0` to `1.0`

Factors:

- source_completeness
- history_completeness
- probe_completeness
- service_completeness

Rules:

- below family floor and runtime-required: STOP
- below family floor and advisory-only: IGNORE
- confidence UNKNOWN/invalid: STOP

## Family-Specific Stale Behavior

- service-scores: WARN
- channel-service-scores: WARN
- user-service-scores: IGNORE
- risk-summaries: STOP
- trust-summaries: STOP
- blast-radius-summaries: STOP
- capacity-forecast-summaries: WARN
- prediction-summaries: IGNORE
- overview-summary: IGNORE
