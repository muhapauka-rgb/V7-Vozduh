# P4 Fail-Closed Review

Project: V7 Vozduh
Block: P4 Controlled Runtime Action Planning

## Fail-Closed States

The following states all abort:

- `UNKNOWN`
- `MISSING`
- `STALE`
- `INVALID`
- `EXPIRED`
- `MISMATCHED`
- `INCONCLUSIVE`
- `BLOCKED`
- `FAILED_CLOSED`

## Required Denials

Future action planning must deny:

- stale packet
- stale runtime evidence
- changed runtime hash
- changed selected moves hash
- changed candidate state
- failed service health
- degraded trust
- rollback unavailable
- observation unavailable
- approval replay
- scope expansion
- single-operator approval

## Certification

P4 fail-closed design is certified for planning.

Execution fail-closed behavior must still be implemented and tested in a later explicitly authorized block.

## Verdict

`fail_closed_certified=true`

