# Block B User Selection

Project: V7 Vozduh

Block: B - Small Batch Program

Date: 2026-06-01

## Selected Users

- `10.7.0.11`
- `10.7.0.12`

## Why Selected

`10.7.0.11` was selected because it completed Block A full lifecycle successfully:

- Move observed
- Rollback observed
- Route table `1009`
- Rollback target `1`
- Good checker visibility

`10.7.0.12` was selected because it was adjacent in the same source egress and had equivalent observability:

- Current egress `1`
- Route table `1010`
- Enabled
- Existing rollback target `1`
- Route table default via `v7e356a192b79`

## Why Others Were Rejected

Other users were not selected to keep the batch exactly at the approved size of `2`.

Disabled user `10.7.0.7` was rejected because it is not healthy for movement.

Users on `awg0`, `awg3`, and `vless` were rejected to avoid mixed-source blast radius in the first small batch.

## Verdict

`users_selected=true`

