# Block D2 Reality Audit

Date: 2026-06-01
Branch: `v7-next`

## Repository State

- Current branch: `v7-next`
- Local HEAD: `d139c47d470055d8e61c3f40e7c4a2343d2538f4`
- `origin/v7-next`: `d139c47d470055d8e61c3f40e7c4a2343d2538f4`
- `origin/main`: `593619d494e215d11fd826086593527a4a555690`
- `origin/Updatesystem`: `b848fbf82f76f916b2fc6e5d04b24a1068e6048f`

## Existing Runtime Reality

- Runtime truth source: `/opt/v7/egress/state/users.registry`
- Egress truth source: `/opt/v7/egress/state/egress.registry`
- Enabled user rows: `18`
- Registry rows total: `19`
- Current enabled user distribution:
  - `amneziawg-exec-20260528-10-8-1-14`: `10`
  - `awg0`: `3`
  - `awg3`: `3`
  - `vless`: `2`

## Existing Tools

- `tools/v7-users-autoswitch`: authoritative shadow planner and optional apply engine.
- `tools/v7-autoswitch-safety-review`: read-only safety preflight.
- `admin_core/operator_observability.py`: operator observability and read-only approval surfaces.
- `admin_core/operator_execution.py`: operator execution packet support with `autoswitch_apply=false`.

## Runtime Constraints Observed

- `v7-users-autoswitch.timer`: `inactive`
- No observed `v7-user-switch`, `v7-users-autoswitch --apply`, `v7-routing-sync`, policy apply, or rebalance process.
- Admin API health check: unavailable on `127.0.0.1:8017`.

## Classification

- Reuse: `v7-users-autoswitch` shadow planner, registry truth sources, existing safety state.
- Extend: `v7-autoswitch-safety-review` registry parser.
- Add bounded helper: `v7-autoswitch-proposal-cap`, a read-only post-processor for existing shadow output.
- Do not touch: runtime config, routing, systemd, users, main, Updatesystem.

