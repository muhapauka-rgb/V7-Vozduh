# E25.7 Pre-Activation Safety Snapshot

## Result

- `pre_activation_snapshot_collected=true`
- `candidate_user=10.7.0.11`
- `candidate_still_on_1=true`
- `selected_moves_zero=true`
- `hidden_movers_absent=true`
- `runtime_checkers_ok=true`
- `target_interface_conflict=false`
- `route_table_1250_conflict=false`

## Baseline

- `users.registry=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`
- `10.7.0.11 current=1 table=1009 enabled=1`
- `route table 1009=default dev v7e356a192b79 scope link`
- `route_get=8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009`
- `default_route=default via 195.2.79.1 dev ens3`
- `resolver_hash=e911046add776eefa83ecc3826ee13f03921013f50678a104ead1fe1146b55a7`

No `v7execwg0` interface or route table `1250` conflict existed before activation.

