# P4.B Rollback Preview Specification

Project: V7 Vozduh
Block: P4.B First Controlled Runtime Action Specification

## Rollback Preview

Because the selected first action changes no users, routes, services, deploy state or systemd state, rollback is not traffic restoration.

Rollback preview is:

`COMPENSATING_GOVERNANCE_RECORD_ONLY`

## Rollback Evidence

Required evidence:

- original action id
- original governance record hash
- original audit record hash
- compensating record id
- compensating record hash
- unchanged users registry hash
- unchanged egress registry hash
- unchanged selected moves hash

## Rollback Verification

Verify:

- original record remains immutable
- compensating record references original record
- audit chain remains hash-linked
- no user movement occurred
- no routing mutation occurred
- no autoswitch apply occurred
- no rollback execution occurred

## Rollback Observation

Operator timeline and audit search must show both records and the relationship between them.

## Rollback Confidence

`HIGH` for governance compensation.

`NOT_APPLICABLE` for traffic restoration.

## Verdict

`rollback_preview_complete=true`

