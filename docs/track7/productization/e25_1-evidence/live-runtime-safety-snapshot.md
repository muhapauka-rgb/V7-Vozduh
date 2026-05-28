# E25.1 Live Runtime Safety Snapshot

Collected: 2026-05-28T10:33:07Z on `v3119922.hosted-by-vdsina.ru`.

## Local Repo Context

- branch: `Updatesystem`
- HEAD: `5de30074356771beef8d5b750415a38c78dbb28a`
- worktree: dirty with many prior governance/productization artifacts; no E25.1 runtime/user movement edits existed before this block.

## Runtime Identity

- `hostname=v3119922.hosted-by-vdsina.ru`
- `date_utc=Thu May 28 10:33:07 UTC 2026`

## Runtime Hashes

- `users.registry=bc7a6b1cbf6919267ce86314754898ef2f0d90b84b40d13db01f417cadfa215c`
- `egress.registry=a0ab01e831f8151acabfb5c895733b294248c1b7d242a0def657c5962c49dea8`

No registry drift from E24/E25 baseline.

## Candidate

- row: `ip=10.7.0.11 current=1 table=1009 enabled=1`
- route table `1009`: `default dev v7e356a192b79 scope link`
- route_get: `8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009`

Candidate moved since E25: NO.

## Users Per Egress

- `1=4`
- `awg0=3`
- `awg3=9`
- `wireguard-1779454504-c43409=0`

WireGuard users count:

- `0`

## WireGuard Target

Target:

- `id=wireguard-1779454504-c43409`
- `protocol=wireguard`
- `interface=v7e06a394c478`
- `enabled=1`
- `soft_limit=1`
- `hard_limit=2`
- `canary_reserved=true`
- `reservation_reason=second_canary_target`
- `reservation_owner=control_plane_governance`

Interface:

- `v7e06a394c478 UNKNOWN <POINTOPOINT,NOARP,UP,LOWER_UP>`
- address: `10.8.0.17/24`
- latest handshake observed: `1 minute, 41 seconds ago`

## Target Readiness

Command:

- `v7-second-canary-target-readiness --pretty`
- `v7-second-canary-target-readiness --json`

Result:

- `approval_status=GO`
- `second_canary_readiness=GO`
- `selected_target=wireguard-1779454504-c43409`
- `candidate_still_valid=true`
- `state_dir=/opt/v7/egress/state`
- `execution_allowed_now=false`

WireGuard score from helper:

- `avg_mbps=30.0077`
- `min_mbps=21.66`
- `stability=0.721815`
- `diagnose_status=OK`
- `load_status=OK`
- `zero_user=true`

## Raw Target Sources

Source mtimes:

- `stability.state`: `2026-05-28 13:32:36 +0300`
- `egress-load.state`: `2026-05-28 13:32:37 +0300`
- `egress-diagnose.state`: `2026-05-28 13:32:37 +0300`
- `egress-quality-summary.json`: `2026-05-28 13:31:42 +0300`

WireGuard values:

- `stability.state`:
  - `avg_mbps=30.0077`
  - `min_mbps=21.66`
  - `stability=0.721815`
  - `samples=30`
- `egress-load.state`:
  - `users=0`
  - `soft_limit=1`
  - `hard_limit=2`
  - `load_status=OK`
- `egress-diagnose.state`:
  - `diagnose_reason=OK`
  - `diagnose_severity=OK`
  - `diagnose_detail=handshake_age_seconds=71`
- `egress-quality-summary.json`:
  - `5m.stability=0.605`
  - `1h.stability=0.5919`
  - `24h.stability=0.697`
  - `7d.stability=0.8084`

## Selected Moves

- no `/opt/v7/egress/state/*selected*` files.
- selected_moves interpreted as `0`.

## Restore Barrier / Generation State

`autoswitch-restore-barrier.json`:

- `enabled=true`
- `block=E11.17`
- `allow_post_ttl_apply=true`
- `generation_clearance=true`
- `clearance_max_selected_moves=0`
- `expires_at=2000-01-01T00:00:00+00:00`

`autoswitch-safety.json`:

- keys observed: `egress`, `schema_version`, `updated`, `users`
- no explicit planner/apply/restore generation IDs exposed.

## Timers / Hidden Movers

The first composite command stopped after the generation-state section due a shell quoting error, so timers/checkers were validated in the restore-settle samples and follow-up checks instead of this file's composite output.

E25.1 restore-settle samples show:

- `planner_timer_state=inactive`
- `apply_timer_state=inactive`
- `hidden_movers_observed=false`
- runtime checkers OK

## Snapshot Verdict

- candidate still on `1`: YES
- WireGuard users count zero: YES
- target readiness GO: YES
- selected_moves zero: YES
- hidden movers absent in follow-up samples: YES
- runtime checkers OK in follow-up samples: YES
- registry hashes unchanged: YES

Abort condition met: NO.
