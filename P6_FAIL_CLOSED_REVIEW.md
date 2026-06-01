# P6 Fail-Closed Review

Project: V7 Vozduh

Block: P6

## Fail-Closed Matrix

The P6 fail-closed matrix was recorded in audit:

- audit hash: `8c04c325ede7036604459ba4619bca2d84188d4054edc9b77b89b8b6c90d02c8`

Abort states:

- unknown: abort
- missing: abort
- stale: abort
- expired: abort
- invalid: abort
- mismatched: abort
- blocked: abort

## Movement Protection

No movement was executed for replay, expired, or fail-closed validation cases.

Only the original approved packet-scope movement executed.

## Verdict

- fail_closed_verified=true
- unknown_aborts=true
- missing_aborts=true
- stale_aborts=true
- expired_aborts=true
- invalid_aborts=true
- mismatched_aborts=true
- blocked_aborts=true
