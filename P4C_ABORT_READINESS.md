# P4.C Abort Readiness

Project: V7 Vozduh
Block: P4.C First Controlled Runtime Action Program

## Abort States

The program aborts on:

- unknown
- missing
- stale
- expired
- invalid
- mismatched
- replay
- blocked

## Verified Fail-Closed Paths

Verified by existing tests:

- expired packet -> denied
- missing second approval -> denied
- movement packet -> denied
- selected moves hash mismatch -> denied
- missing generation id -> denied
- invalid runtime action -> denied
- missing runtime -> denied
- replay -> denied
- path traversal -> denied

## Verdict

`abort_ready=true`

