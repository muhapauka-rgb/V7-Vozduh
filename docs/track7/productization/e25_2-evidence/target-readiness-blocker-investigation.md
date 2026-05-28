# E25.2 Target Readiness Blocker Investigation

## Classification

`REAL_TARGET_DEGRADATION_RECURRED`

WireGuard target readiness recovered during E25.1, but degraded again during E25.2 fresh execution-time recheck. This is not stale packet state and not a helper threshold relaxation problem. The movement-critical helper saw fresh low performance values and correctly returned NO-GO.

## Samples

### Sample 1

- timestamp: `2026-05-28T11:02:02Z`
- `approval_status=NO-GO`
- `selected_target=NONE`
- WireGuard `avg_mbps=15.3983`
- WireGuard `min_mbps=4.61`
- WireGuard `stability=0.299384`
- WireGuard diagnose: `OK`
- WireGuard load: `OK`
- WireGuard users: `0`
- rejection reasons:
  - `min_mbps below floor (4.61)`
  - `stability below floor (0.299384)`

### Sample 2

- timestamp: `2026-05-28T11:02:43Z`
- `approval_status=NO-GO`
- `selected_target=NONE`
- WireGuard `avg_mbps=15.3227`
- WireGuard `min_mbps=4.61`
- WireGuard `stability=0.300861`
- WireGuard diagnose: `OK`
- WireGuard load: `OK`
- WireGuard users: `0`
- rejection reasons:
  - `min_mbps below floor (4.61)`
  - `stability below floor (0.300861)`

## Raw Source State

Files were fresh at the VPS local time around `2026-05-28 14:01 +0300`:

- `/opt/v7/egress/state/stability.state`
- `/opt/v7/egress/state/egress-quality-summary.json`
- `/opt/v7/egress/state/egress-load.state`
- `/opt/v7/egress/state/egress-diagnose.state`

Raw stability rows for WireGuard:

```text
wireguard-1779454504-c43409_avg_mbps=15.3983
wireguard-1779454504-c43409_min_mbps=4.61
wireguard-1779454504-c43409_stability=0.299384
wireguard-1779454504-c43409_samples=30
```

Raw load rows:

```text
wireguard-1779454504-c43409_users=0
wireguard-1779454504-c43409_soft_limit=1
wireguard-1779454504-c43409_hard_limit=2
wireguard-1779454504-c43409_load_status=OK
```

Raw diagnose rows:

```text
wireguard-1779454504-c43409_diagnose_reason=OK
wireguard-1779454504-c43409_diagnose_severity=OK
wireguard-1779454504-c43409_diagnose_detail=handshake_age_seconds=93
```

Quality summary for WireGuard also showed a degraded short window:

- 5m `avg_mbps=19.541`
- 5m `min_mbps=8.895`
- 5m `stability=0.4104`
- trend: `degrading`

## Theory Review

- candidate drift: NO, `10.7.0.11` remains on `1`.
- target drift: YES, target readiness regressed to NO-GO.
- selected_moves appeared: NO.
- hidden mover active: NO.
- runtime checker failure: NO.
- helper false NO-GO: NO evidence. Raw stability and quality summary both show short-window degradation.
- stale source data: NO evidence. Source files were fresh.
- diagnose/load conflict: PARTIAL but expected. Diagnose/load can be OK while quality floor fails; readiness requires all gates.
- packet expiry: NO, packet still fresh at E25.2 recheck.
- registry drift: NO, registry hashes unchanged.

## Decision

Do not execute movement. A zero-user target with diagnose/load OK is still unsafe for this movement when `min_mbps` and `stability` are below the movement-critical floor.

Recommended next block: recover or replace the target before retrying user movement.
