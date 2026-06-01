# Block B Packet

Project: V7 Vozduh

Block: B - Small Batch Program

Packet source:

- `/tmp/block-b-small-batch-20260601T105928Z/packet.json`

## Packet Identity

- `packet_id=block-b-batch-20260601T105928Z`
- `approval_id=block-b-approval-20260601T105928Z`
- `operation_id=BLOCK_B_SMALL_BATCH_PROGRAM`

## Scope

- `movement_budget=2`
- `allowed_users=["10.7.0.11","10.7.0.12"]`
- `allowed_targets=["amneziawg-exec-20260528-10-8-1-14"]`
- Rollback targets: both users to `1`
- Route tables: `1009`, `1010`

## Replay Protection

- Packet ID unique
- Nonce required
- TTL required
- Used packet denied

## Observation Plan

- Before
- After
- Delayed
- Final

## Verdict

`packet_created=true`

