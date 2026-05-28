# E24.1 Helper Cross-Check

## Runtime Registry Hashes

After helper execution:

- `users.registry`
  - sha256=`bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry`
  - sha256=`a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`

These match the E24 snapshot hashes. No registry mutation was observed.

## Candidate User

Live users registry:

- `ip=10.7.0.11 current=1 table=1009 enabled=1`

Route checker:

- `10.7.0.11` registry matches assignment.
- table `1009` default route uses `v7e356a192b79`.
- `route_get` uses `v7e356a192b79`.

Candidate validity:

- candidate still on expected rollback/source egress `1`: YES.

## Selected Target

Live egress registry row:

- `id=wireguard-1779454504-c43409`
- `protocol=wireguard`
- `interface=v7e06a394c478`
- `enabled=1`
- `role=GLOBAL_FAST`
- `soft_limit=1`
- `hard_limit=2`
- `exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU`
- `canary_reserved=true`
- `reservation_reason=second_canary_target`
- `reservation_owner=control_plane_governance`

Direct interface evidence:

- `v7e06a394c478 UNKNOWN <POINTOPOINT,NOARP,UP,LOWER_UP>`
- `v7e06a394c478 UNKNOWN 10.8.0.17/24`

WireGuard read-only diagnose:

- interface `v7e06a394c478`
- latest handshake: `1 minute, 13 seconds ago`
- transfer counters present

Target readiness helper result:

- `selected_target=wireguard-1779454504-c43409`
- `status=GO`
- `zero_user=True`
- `diagnose_status=OK`
- `approval_status=GO`

Target cross-check verdict:

- WireGuard target clean: YES.
- WireGuard target reserved: YES.
- WireGuard target capacity within hard limit: YES.
- Target readiness helper agrees with manual runtime truth: YES.

## Runtime Checkers

Executed after helper deploy:

- `v7-reconcile-check`: `V7_RECONCILE_RESULT=OK`
- `v7-user-route-check`: `V7_USER_ROUTE_CHECK=OK`
- `v7-killswitch-check`: `V7_KILLSWITCH_CHECK=OK`
- `v7-provisioning-reconcile-check`: `V7_PROVISIONING_RECONCILE_CHECK=OK`

## Hidden Movement Scan

No active processes found for:

- `v7-user-switch`
- `v7-routing-sync`
- `v7-users-autoswitch --apply`

## Switch History

- `/opt/v7/egress/state/switch-history.log`: MISSING

No switch-history mutation was observed by the deploy/run actions.

## Cross-Check Verdict

- Target readiness helper output is live-runtime based and cross-checked.
- Runtime state remained unchanged after helper deployment/execution.
- Restore-settle helper is installed and safe but lacks fresh restore-settle sample evidence for an E25 GO.
