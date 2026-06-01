# P6 Replay Test

Project: V7 Vozduh

Block: P6

## Packet Replay

Packet:

- packet_id: `packet-p6-5b8223b9d803f429b8a67b78`
- approval_id: `approval-p6-af5e2daa75c37706b4a73559`

Replay check found the forward packet already consumed:

- used_forward_records: `1`
- replay verdict: `DENY_REPLAY`
- movement_executed_during_replay: false
- replay audit hash: `cbd5eae08adaed972fe4bbe02aa71ed1661e4c290c889fb7e45fce852d7a82a8`

No second movement command was executed during replay validation.

## Expired Packet

- expired packet verdict: `DENY_EXPIRED_PACKET`
- movement_executed: false
- expired audit hash: `43322f42894d5986ee4180ec2566e13eec4628ee1b7582f54b0447febc3406c6`

## Verdict

- replay_protection_verified=true
- duplicate_packet_denied=true
- replay_denied=true
- expired_packet_denied=true
