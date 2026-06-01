# P6 Packet

Project: V7 Vozduh

Block: P6

## Packet Identity

- packet path: `/tmp/p6-first-user-movement-20260601T102011Z/packet.json`
- packet_id: `packet-p6-5b8223b9d803f429b8a67b78`
- approval_id: `approval-p6-af5e2daa75c37706b4a73559`
- operation_id: `P6_FIRST_USER_MOVEMENT_PROGRAM`
- packet hash: `4652e77f81e1acf172e0a026b9e4b0ce45afbc8b032accc149be4d962f30cbe3`

## Scope

- movement_budget: `1`
- blast_radius: `1`
- allowed_users: `["10.7.0.11"]`
- allowed_targets: `["amneziawg-exec-20260528-10-8-1-14"]`
- from_egress: `1`
- to_egress: `amneziawg-exec-20260528-10-8-1-14`
- rollback_target: `1`
- route_table: `1009`
- target_interface: `v7execwg0`

## Runtime Hashes

- users registry hash: `07362c9aa6f959be2ab06f26928692c6844f37a3bd266be8de4e56193f6d9a9f`
- egress registry hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- selected moves count: `0`
- selected moves hash: `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
- runtime snapshot hash: `ec11fffc70bf63d04dd76b723e415692b4be371ec007ec0df638fc5ecb216c84`

## Approval

- approval author: `prompt-authorized-operator`
- approval reviewer: `codex-runtime-reviewer`
- dual confirmation required: true
- dual confirmation captured: true
- approval TTL: 30 minutes

## Rollback Preview

- rollback command preview: `v7-user-switch 10.7.0.11 1`
- execute rollback now: false

## Replay Protection

- packet_id_unique=true
- approval_id_unique=true
- duplicate_packet_denied=true

## Verdict

- packet_created=true
- packet_scope_valid=true
