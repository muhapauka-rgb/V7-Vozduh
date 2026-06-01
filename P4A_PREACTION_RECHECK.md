# P4.A Pre-Action Recheck

Project: V7 Vozduh
Block: P4.A First Controlled Runtime Action Design

## Immediate Recheck

The future action must run an immediate recheck after approval and before any action record is written.

## Required Checks

- users registry exists and hash matches
- egress registry exists and hash matches
- runtime snapshot hash matches
- selected moves hash is empty and count is zero
- service health did not degrade
- capacity did not change into a blocking state
- trust did not degrade
- required services did not become blocked
- candidate/action packet state is still valid
- readiness is still acceptable
- dry-run verification is current and not mismatched
- rollback preview is available
- audit/event observation is available

## Any Change

Any changed, stale, missing, invalid, expired, mismatched or unknown state aborts the future action.

## Verdict

`preaction_recheck_defined=true`

