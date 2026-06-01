# P4.B Observation Specification

Project: V7 Vozduh
Block: P4.B First Controlled Runtime Action Specification

## Before Checkpoint

Capture:

- packet id
- approval id
- action id
- approval author/reviewer
- users registry hash
- egress registry hash
- selected moves hash/count
- runtime snapshot hash
- dry-run summary id
- dry-run verification id/state
- rollback preview state
- audit tail hash/ref
- governance store tail hash/ref

## During Checkpoint

For a later authorized execution block:

- action start timestamp
- recheck verdict
- append result
- action record hash
- audit record hash
- no user movement flag
- no routing mutation flag
- no autoswitch apply flag
- no rollback execution flag

## After Checkpoint

Verify:

- exactly one governance action record for approval id
- exactly one audit action record
- replay attempt is denied
- users registry unchanged
- egress registry unchanged
- selected moves unchanged and empty
- operator timeline renders the action
- audit search renders the action and denial evidence

## Verification Checkpoint

Post-action verification state:

`VERIFIED_ZERO_MOVE_GOVERNANCE_RECORD_ONLY`

## Retention

Use existing audit and governance retention. P4.B creates no new stream.

## Verdict

`observation_spec_complete=true`

