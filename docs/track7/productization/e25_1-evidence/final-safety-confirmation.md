# E25.1 Final Safety Confirmation

Collected from VPS at `2026-05-28T10:40:41Z`.

## Runtime Hashes

- `users.registry=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`

## Candidate

`ip=10.7.0.11 current=1 table=1009 enabled=1`

## Selected Moves

No selected-move files were present under `/opt/v7/egress/state`; interpreted by the governance tooling as `selected_moves=0`.

## Target Readiness

`v7-second-canary-target-readiness --json` returned:

- `approval_status=GO`
- `second_canary_readiness=GO`
- `selected_target=wireguard-1779454504-c43409`
- `candidate_still_valid=true`
- WireGuard target `safe_for_second_canary=true`
- WireGuard target `zero_user=true`
- WireGuard target `diagnose_status=OK`
- WireGuard target `load_status=OK`
- WireGuard target `stability=0.830617`
- `execution_allowed_now=false`

## Runtime Checkers

- `V7_RECONCILE_RESULT=OK`
- `V7_USER_ROUTE_CHECK=OK`
- `V7_KILLSWITCH_CHECK=OK`
- `V7_PROVISIONING_RECONCILE_CHECK=OK`

## Hidden Movers

No active process matched:

- `v7-user-switch`
- `v7-routing-sync`
- `v7-users-autoswitch --apply`

## Mutation Statement

- Runtime mutation performed: NO
- User movement performed: NO
- Routing mutation performed: NO
- Kill switch mutation performed: NO
- Autoswitch apply performed manually: NO
- Canary/cohort performed: NO
