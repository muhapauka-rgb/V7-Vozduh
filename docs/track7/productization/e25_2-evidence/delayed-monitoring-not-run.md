# E25.2 Delayed Monitoring

## Result

`not_applicable_no_forward_movement`

Delayed monitoring after forward/rollback was not run because E25.2 aborted before any movement.

Final no-mutation safety check at `2026-05-28T11:02:43Z`:

- `users.registry=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`
- `10.7.0.11` remained on `1`
- no users on `wireguard-1779454504-c43409`
- no hidden mover process observed

`delayed_movement_observed=false` for this block because no movement occurred and registry hashes remained unchanged.
