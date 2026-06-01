# Block A Rollback Packet

Project: V7 Vozduh

Block: A - Single User Completion Program

Packet source:

- `/tmp/block-a-single-user-completion-20260601T104148Z/rollback_packet.json`

## Packet Identity

- `packet_id=block-a-rollback-20260601T104148Z`
- `approval_id=block-a-approval-20260601T104148Z`
- `operation_id=BLOCK_A_SINGLE_USER_COMPLETION`
- Mode: `single-user-rollback`

## Scope

- Movement budget: `1`
- Allowed users: `10.7.0.11`
- Allowed from egress: `amneziawg-exec-20260528-10-8-1-14`
- Allowed to egress: `1`
- Route table: `1009`
- Expected before interface: `v7execwg0`
- Expected after interface: `v7e356a192b79`

## Guards

- `scope_expansion_allowed=false`
- `autoswitch_apply_allowed=false`
- `bulk_movement_allowed=false`
- `deploy_allowed=false`
- `systemd_change_allowed=false`

## Preview Evidence

Preview source:

- `/tmp/block-a-single-user-completion-20260601T104148Z/rollback_preview.json`

Preview verdict:

- `mutation=false`
- `runtime_commands_executed=false`
- `blast_radius=one_user`
- `to_egress=1`
- `from_egress=amneziawg-exec-20260528-10-8-1-14`
- `target_interface=v7e356a192b79`
- `table=1009`
- `errors=[]`

## Packet Verdict

`rollback_packet_created=true`

