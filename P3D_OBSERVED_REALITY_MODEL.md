# P3.D Observed Reality Model

Project: V7 Vozduh
Block: P3.D Dry-Run Verification

## Collection Rule

Observed reality is collected only by reading existing sources through P3.C adapters. P3.D does not run probes, write state or mutate runtime.

## Observed Fields

- `observed_at`
- `observed_outcome`
- `reason`
- `confidence`
- `evidence`
- `freshness`
- `input_refs`
- `input_hashes`
- `read_only`
- `derived_only`

## Sources

- Runtime state files.
- Service matrix.
- Capacity summary.
- Trusted RU decision state.
- Candidate workflow.
- Execution contracts/events.
- Audit and event logs.

## Result

Observed reality maps to the same allowed dry-run outcome vocabulary:

- `NO_ACTION`
- `WOULD_MOVE`
- `WOULD_BLOCK`
- `WOULD_REVIEW`
- `WOULD_ROLLBACK`

