# P4.A Rollback Preview Design

Project: V7 Vozduh
Block: P4.A First Controlled Runtime Action Design

## Rollback Type

The selected first action has no user, route, service or systemd rollback because it does not change those domains.

Rollback is a compensating append-only governance record:

- original action record remains immutable
- compensating record marks action superseded or invalidated
- audit lineage links compensation to original action id

## Rollback Verification

Rollback verification checks:

- original action record exists
- compensating record references original action id
- no user movement occurred
- no routing change occurred
- selected moves remained empty
- audit chain remains hash-linked

## Rollback Observation

Observation checks:

- operator timeline shows both records
- audit search can find original and compensating record
- dry-run and execution preview still report no user/routing mutation

## Confidence

Rollback confidence is high for governance-record compensation and not applicable for runtime traffic restoration.

## Verdict

`rollback_preview_defined=true`

