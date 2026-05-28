# E24.2 E24 Packet Revalidation

## Original E24 Packet Shape

- `candidate_user=10.7.0.11`
- `selected_target=wireguard-1779454504-c43409`
- `rollback_target=1`
- `movement_budget=1`
- `execution_method=CLI_PACKET_ONLY`
- `ui_execution_allowed=false`

## Live Runtime Revalidation

Candidate:

- `10.7.0.11` remains on `1`.
- table remains `1009`.
- route/runtime checkers remain OK.

Target:

- `wireguard-1779454504-c43409` remains target readiness `GO`.
- WireGuard users count remains `0`.
- target reservation remains in egress registry:
  - `canary_reserved=true`
  - `reservation_owner=control_plane_governance`

Rollback target:

- rollback target `1` remains the candidate's current egress.
- users on `1`: `10.7.0.11`, `10.7.0.12`, `10.7.0.14`, `10.7.0.15`.

Selected moves:

- selected_moves remains `0`.
- no selected-move files observed.

Restore-settle:

- fresh E24.2 sample window collected.
- `v7-restore-settle-gate` returned `GO`.

Runtime hashes:

- `users.registry=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`

These match the E24 packet baseline, so packet hash refresh is not required solely due to registry drift.

## Packet Refresh Decision

- `packet_needs_refresh=false`

Reason:

- Runtime hashes are unchanged.
- Candidate/target/rollback semantics are unchanged.
- New restore-settle evidence should be referenced by the E25 execution packet/runbook, but the E24 movement preview itself remains valid.

## E25 Gate Decision

- `e24_packet_still_valid=true`
- `e25_execution_gate_ready=true`
- `execution_allowed_now=false`

E25 remains a separate execution block and must run fresh execution-time rechecks before any movement.
