# E25.10 Target-Local Activation

## Result

`handshake_successful=true`

`rx_packets_present=true`

`target_connectivity_usable=true`

`global_route_side_effects_prevented=true`

`dns_side_effect_blocked=true`

`routing_mutation_for_users=false`

`raw_profile_executed=false`

## Activation Attempt 1

The first normalized activation failed closed:

- command path: `awg-quick up /etc/amnezia/v7execwg0.conf`
- result: `up_rc=1`
- failure: `Line unrecognized: I1=`
- interface cleanup: `awg-quick` deleted `v7execwg0`
- default route changed: `false`
- DNS changed: `false`
- table `1009` changed: `false`
- `users.registry` changed: `false`
- `egress.registry` changed: `false`
- runtime checkers after failure: `OK`

Root cause: the operator-provided AmneziaWG profile contained empty optional `I1`-`I5` fields. These were removed from the normalized wrapper; other AmneziaWG parameters were preserved.

## Activation Attempt 2

Normalized wrapper:

- config: `/etc/amnezia/v7execwg0.conf`
- SHA256 after remediation: `1016222374577511ac3292f8d30b899ca1d6c95d6b3ede7299e69cf8e504f41d`
- `Table=off`: `true`
- DNS removed: `true`
- hooks absent: `true`
- empty `I1`-`I5` removed: `true`

Activation succeeded:

- command path: `awg-quick up /etc/amnezia/v7execwg0.conf`
- result: `up_rc=0`
- interface: `v7execwg0`
- address: `10.8.1.14/32`
- MTU: `1280`

## Side-Effect Check

Before and after activation:

- default route: `default via 195.2.79.1 dev ens3 proto static onlink`
- user table `1009`: `default dev v7e356a192b79 scope link`
- DNS global state: unchanged
- `users.registry` SHA256: `bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry` SHA256 before metadata attempt: `a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`
- candidate row: `ip=10.7.0.11 current=1 table=1009 enabled=1`

No user route table changed and no user moved.

## Connectivity

`awg show v7execwg0` after activation:

- latest handshake: `Now`
- transfer before probe: `92 B received, 344 B sent`

Target-local ping:

- command: `ping -c 3 -W 3 -I v7execwg0 1.1.1.1`
- result: `3 packets transmitted, 3 received, 0% packet loss`
- RTT: `min/avg/max/mdev = 27.439/30.652/34.225/2.781 ms`

`awg show v7execwg0` after probe:

- latest handshake: `2 seconds ago`
- transfer after probe: `476 B received, 728 B sent`

## Runtime Safety After Probe

- `v7-reconcile-check`: `OK`
- `v7-user-route-check`: `OK`
- `v7-killswitch-check`: `OK`
- `v7-provisioning-reconcile-check`: `OK`

The profile is usable as a target-local external outbound profile through the V7-normalized wrapper.
