# E25.7 Interface Activation

## Result

- `profile_activated=true`
- `activated_interface=v7execwg0`
- `raw_profile_executed=false`
- `default_route_changed=false`
- `dns_changed=false`
- `users_registry_changed=false`
- `egress_registry_changed=false`
- `candidate_user_route_table_changed=false`
- `hidden_movers_absent=true`
- `rollback_required=true`

## Activation Command Result

`wg-quick up v7execwg0` returned `0` and executed only:

- `ip link add dev v7execwg0 type wireguard`
- `wg setconf v7execwg0 ...`
- `ip -4 address add 10.89.0.2/32 dev v7execwg0`
- `ip link set mtu 1280 up dev v7execwg0`

No route installation occurred because `Table=off` was present.

## Side-Effect Comparison

| Surface | Before | After |
| --- | --- | --- |
| `users.registry` hash | `bc7a6b1...fa215c` | unchanged |
| `egress.registry` hash | `a0ab01e...9dea8` | unchanged |
| default route | `default via 195.2.79.1 dev ens3` | unchanged |
| `/etc/resolv.conf` hash | `e911046...b55a7` | unchanged |
| candidate table 1009 | `default dev v7e356a192b79` | unchanged |
| candidate `route_get` | `dev v7e356a192b79 table 1009` | unchanged |

Activation was side-effect clean. Validation later failed on target-local connectivity, so removal was executed.

