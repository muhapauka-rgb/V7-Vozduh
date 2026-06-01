# Program Z1 Fail Closed

Date: 2026-06-01

## Verified

- stale packet denied
- no movement after stale approval drift
- no autoswitch apply outside packet
- no deploy
- no systemd change
- no scope expansion

## Not Live-Exercised

- replay
- expired packet
- invalid packet
- blocked packet after successful execution

replay_protection_verified=false
fail_closed_verified=true

