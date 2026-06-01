# Program Z2 Fail Closed

Date: 2026-06-01

## Verdict

replay_protection_verified=true
fail_closed_verified=true

## Verified Denials

Unit tests verify denial for:

- expired approval
- stale proposal fingerprint
- budget greater than `1`
- replayed approval id
- execution-only target without exact target approval

Manual CLI replay check:

- first execution record: `ALLOW_HYBRID_BOUNDED_AUTONOMY`
- second validation: `DENY_HYBRID_APPROVAL`
- replay error: `approval_replay`

## Hash Mismatch

The validator fails closed when expected fingerprints or registry hashes do not match runtime-derived values.

## Stale Runtime

The validator denies if runtime registry files are missing or selected moves are not empty.

## Safety

- fail_open_paths_found=false
- runtime_mutation_performed=false
- users_moved=false
- routing_changed=false

