# Program Z2 Runtime Recheck

Date: 2026-06-01

## Verdict

runtime_recheck_working=true

## Checks Implemented

`admin_core/hybrid_approval.py` rechecks:

- schema version
- approval mode
- expiry
- selected move count
- runtime registry availability
- safety status
- proposal fingerprint
- policy fingerprint
- runtime fingerprint
- users registry hash
- egress registry hash
- selected move hash
- budget equals `1`
- exactly one proposal move
- target substitution
- approval replay

## Z2 Recheck Result

Initial validation:

- verdict: `ALLOW_HYBRID_BOUNDED_AUTONOMY`
- errors: `[]`

Replay validation after audit record:

- verdict: `DENY_HYBRID_APPROVAL`
- errors: `approval_replay`

## Safety

- runtime_mutation_performed=false
- users_moved=false
- routing_changed=false
- autoswitch_apply_run=false

