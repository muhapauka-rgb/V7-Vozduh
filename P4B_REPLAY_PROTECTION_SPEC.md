# P4.B Replay Protection Specification

Project: V7 Vozduh
Block: P4.B First Controlled Runtime Action Specification

## Replay Detection

Replay is detected by searching existing audit records for the same `approval_id`.

If found:

`DENY_REPLAY`

## Duplicate Packet Detection

Duplicate packet id must be rejected if:

- same packet id appears in prior audit record
- same approval id appears in prior audit record
- same action id appears with a completed governance record

## Expired Packet Detection

If current time is greater than or equal to `expires_at`:

`APPROVAL_EXPIRED`

## Hash Mismatch Detection

Abort when any expected hash differs:

- users registry hash
- egress registry hash
- selected moves hash
- runtime snapshot hash

## Required Denial Record

In a later authorized block, replay/duplicate/expired/hash mismatch denials should append denial audit records without appending governance action records.

P4.B does not append records.

## Verdict

`replay_protection_complete=true`

