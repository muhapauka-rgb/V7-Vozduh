# E25.4 Execution Egress Strategy

## Decision

`strategy=CREATE_DEDICATED_WIREGUARD_EXECUTION_TARGET`

## Existing Runtime Inventory

Current VPS egresses:

| Egress | Protocol | Users | Readiness | Notes |
|---|---|---:|---|---|
| `1` | amneziawg | 4 | baseline, not target | rollback/current target for candidate |
| `wireguard-1779454504-c43409` | wireguard | 0 | GO at inventory time | governance reserved, but spiky in E25.2/E25.3 |
| `openvpn-1779388847-d2ad7c` | openvpn | 0 | NO-GO | diagnose SUSPECT / interface unknown |
| `awg0` | amneziawg | 3 | NO-GO | occupied, HARD_FULL, missing exclusions |
| `awg3` | amneziawg | 9 | NO-GO | occupied, HARD_FULL, missing exclusions |
| `vless` | vless | 0 registry / 1 load | NO-GO | load user, diagnose SUSPECT, missing exclusions |

The only existing target that can pass all readiness gates is still `wireguard-1779454504-c43409`, and E25.3 classified it as spiky.

## Protocol Choice

Dedicated WireGuard is the cleanest execution-only target because:

- readiness helper already handles WireGuard diagnose through handshake evidence;
- interface state is observable;
- load-state and zero-user checks already work;
- route behavior is predictable;
- rollback from/to baseline egress remains simple;
- existing governance reservation path has already been proven for WireGuard.

OpenVPN is not selected because the current OpenVPN target has diagnose `SUSPECT` and interface unknown. VLESS is not selected because it lacks the required route-class exclusions and has diagnose/load blockers. Existing AWG targets are production-occupied and hard-full.

## Required Target Shape

The dedicated execution target should be a new egress id, for example:

`execution-wg-<timestamp-or-id>`

Required metadata:

- `protocol=wireguard`
- `type=interface`
- `enabled=1`
- `role=EXECUTION_ONLY`
- `soft_limit=1`
- `hard_limit=1`
- `manual_only=1`
- `reserve_only=1`
- `canary_reserved=true`
- `execution_reserved=true`
- `reservation_owner=operator_execution_governance`
- `service_tags=governance,execution`
- `exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU`

Required protection:

- zero users;
- excluded from autoswitch assignment;
- excluded from rebalance;
- not selected by planner as production failover;
- movement only via explicit operator-governed packet.

## Why E25.4 Did Not Create It

Creating a real dedicated execution egress requires a real profile/interface and egress registry mutation. No unused dedicated profile was present in the runtime inventory, and this block's final mutation statement requires no runtime mutation. Creating a fake egress registry row without a real working interface would weaken readiness, not improve it.

Therefore E25.4 prepares the strategy and confirms the gap, but does not create a runtime target.
