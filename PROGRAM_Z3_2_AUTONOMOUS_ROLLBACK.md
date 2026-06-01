# PROGRAM Z3.2 Autonomous Rollback

## Rollback Scope

Rollback the single Z3.2 movement:

- user: `10.7.0.16`
- from: `awg3`
- to: `vless`
- table: `1014`

## Rollback Authority

Existing live authority:

- `v7-user-switch 10.7.0.16 vless`

No new rollback engine was created.

## Rollback Evidence

Before rollback:

- `ip=10.7.0.16 current=awg3 table=1014 enabled=1`

Rollback output confirmed:

- user switched to `vless`
- route device: `tun0`
- state egress: `vless`
- fail_count: `0`
- rc: `0`

After rollback:

- collected_at: `2026-06-01T17:59:05.202268+00:00`
- `ip=10.7.0.16 current=vless table=1014 enabled=1`
- users_registry_hash: `ee71cdd73a5a9b03ff009b8c29fae194fbf97c4f956677028c3c1166c2e4dae4`
- egress_registry_hash: `f884a1269e1077a31a8e1dbbf55160e61822a8af5c2dc9abb28a243cadc4acd5`
- route_check: `OK`

Final observation:

- route_check_rc: `0`
- reconcile_rc: `0`
- killswitch_rc: `0`
- users hash still restored to pre-move value

## Verdict

- autonomous_rollback_certified=true
- rollback_scope_one_user=true
- final_state_restored=true
- egress_registry_unchanged=true

