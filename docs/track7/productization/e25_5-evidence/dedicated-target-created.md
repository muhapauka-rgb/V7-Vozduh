# E25.5 Dedicated Target Created

## Result

`dedicated_execution_target_created=false`

No dedicated execution target was created or imported.

## Why

E25.5 did not find a spare working outbound profile suitable for immediate execution-only provisioning.

Unsafe candidates:

- Existing `wireguard-1779454504-c43409`: already active, not dedicated, known spiky.
- Draft `wg-1779455931-ba621c`: duplicate/update of existing WireGuard target, not a new target.
- `/etc/wireguard/wg-client-test.conf`: inbound/server test profile with route hooks.
- `/etc/amnezia/amneziawg/awg-client-test.conf`: inbound/server test profile with route/nft hooks.
- `/etc/wireguard/vps.conf`: raw client-like profile not normalized for V7 routing ownership; unsafe to start as-is.
- OpenVPN drafts: not cleanly runtime-ready for first movement; at least one recent draft had runtime `FAIL`.

## Runtime Mutation

No egress registry row was added. No interface was started. No config was copied or modified.

## Flags

- `dedicated_execution_target_created=false`
- `dedicated_execution_target_name=NONE`
- `dedicated_execution_target_zero_user=false`
- `governance_reserved=false`
- `autoswitch_excluded=false`
- `rebalance_excluded=false`
- `production_assignment_blocked=false`
