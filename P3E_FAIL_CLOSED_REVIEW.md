# P3.E Fail-Closed Review

Project: V7 Vozduh
Block: P3.E Dry-Run Certification

## Fail-Closed Controls

P3 dry-run fail-closed behavior includes:

- missing required runtime evidence -> `WOULD_BLOCK`
- failed execution preview consistency -> `WOULD_BLOCK`
- service failures -> `WOULD_BLOCK`
- blocked candidate -> `WOULD_BLOCK`
- stale key inputs -> `WOULD_REVIEW`
- invalid evaluator output -> `WOULD_BLOCK`
- invalid prediction output -> `INCONCLUSIVE`
- stale prediction -> `STALE`
- mismatch -> `VERIFIED_MISMATCH`

## Forbidden Outputs

Forbidden dry-run outputs:

- `MOVE`
- `EXECUTE`
- `APPLY`
- `ROUTE`
- `AUTOSWITCH_APPLY`

## Certification

The dry-run and verification model fails closed for planning purposes.

P4 must preserve the same posture: any unknown, stale, mismatched, missing, or inconclusive state must block execution and require operator review.

## Verdict

`fail_closed_certified=true`

