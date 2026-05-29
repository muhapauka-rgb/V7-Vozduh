# E25.11 Pre-Integration Safety Snapshot

## Result

`candidate_user=10.7.0.11`

`candidate_still_on_1=true`

`selected_moves_zero=true`

`hidden_movers_absent=true`

`runtime_checkers_ok=true`

`v7execwg0_absent=true`

`nat_mss_for_v7execwg0_absent=true`

## Runtime Snapshot

- host: `v3119922.hosted-by-vdsina.ru`
- checked_at_utc: `2026-05-28T14:47:45Z`
- `users.registry` SHA256: `bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry` SHA256: `a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`
- candidate row: `ip=10.7.0.11 current=1 table=1009 enabled=1`
- candidate table `1009`: `default dev v7e356a192b79 scope link`
- candidate `route_get`: `dev v7e356a192b79 table 1009`
- default route: `default via 195.2.79.1 dev ens3 proto static onlink`
- DNS state: unchanged baseline, global `8.8.8.8 1.1.1.1`

## Integration Gap

- `v7execwg0` interface: absent
- NAT rule for `v7execwg0`: absent
- MSS clamp for `v7execwg0`: absent

## Helper Baseline

`v7-second-canary-target-readiness` default mode remained unchanged and selected the existing canary target:

- selected target: `wireguard-1779454504-c43409`
- approval status: `GO`
- execution allowed now: `false`

`v7-restore-settle-gate` against `/opt/v7/egress/state` remained `CONDITIONAL` because only the default single `path-samples.json` sample was present. This is expected for the live state dir and does not imply movement.

## Runtime Checkers

- `v7-reconcile-check`: `OK`
- `v7-user-route-check`: `OK`
- `v7-killswitch-check`: `OK`
- `v7-provisioning-reconcile-check`: `OK`

## Abort Conditions

- candidate not on `1`: `false`
- selected moves present: `false`
- hidden movers active: `false`
- runtime checker failure: `false`

Proceed to execution-only target activation and integration.
