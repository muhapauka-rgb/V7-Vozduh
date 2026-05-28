# E25.6 V7 Normalization Plan

## Result

- `normalization_possible=true`
- `unsafe_hooks_removed_or_blocked=true`
- `global_route_side_effects_prevented=true`
- `raw_activation_allowed=false`
- `activation_deferred=true`

## Proposed Normalized Target

- `target_name=wireguard-exec-20260528-10-89-0-2`
- `interface_name=v7execwg0`
- `protocol=wireguard`
- `source_profile=/root/v7-wg-client-test/v7-wg-client-test-direct-10.89.0.2.conf`
- `source_profile_hash=666cf51365f7e145726f7db7c503577ff2b5a872ae7351486cb41fd1316e0ff1`
- `route_table=1250`
- `role=EXECUTION_ONLY`

## Wrapper Rules

The activation block must create a normalized runtime profile with:

```ini
[Interface]
PrivateKey = <from source profile>
Address = 10.89.0.2/32
MTU = 1280
Table = off

[Peer]
PublicKey = <from source profile>
PresharedKey = <from source profile>
Endpoint = <from source profile>
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
```

Blocked from the runtime wrapper:

- raw DNS mutation
- PostUp/PostDown
- PreUp/PreDown
- nft/iptables hooks
- automatic default-route takeover
- production assignment

Routing must remain V7-owned:

- no global default route
- no broad routing-sync
- no autoswitch apply
- policy routing only after a governed user movement packet
- first movement may only target `10.7.0.11`

## Rollback / Removal Plan

If activation fails in the next block:

1. Bring down only `v7execwg0` if it was created.
2. Remove only the dedicated execution-only normalized config.
3. Remove only draft/disabled metadata for `wireguard-exec-20260528-10-89-0-2`.
4. Verify `users.registry` unchanged.
5. Verify no route table/rule exists for user `10.7.0.11`.
6. Run runtime checkers.

