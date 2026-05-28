# E25.1 Target Readiness Root Cause

## E25 Failure

During E25, `v7-second-canary-target-readiness` returned `NO-GO` because WireGuard stability from `stability.state` was below the `0.45` floor:

- `0.422735`
- `0.431723`
- `0.438413`

At the same time:

- WireGuard users count was zero.
- load status was OK.
- diagnose was OK.
- interface was inferred UP/LOWER_UP from diagnose.

## E25.1 Recheck

At 2026-05-28T10:33:07Z, the same helper returned `GO` using the same authoritative state directory:

- `state_dir=/opt/v7/egress/state`
- `approval_status=GO`
- `selected_target=wireguard-1779454504-c43409`
- WireGuard stability from `stability.state`: `0.721815`
- floor: `0.45`

No helper threshold was changed.
No runtime source was refreshed manually.
No readiness semantics were weakened.

## Source Files Read By Helper

Helper source:

- `tools/v7-second-canary-target-readiness`
- VPS runtime path: `/usr/local/bin/v7-second-canary-target-readiness`

Decision path:

1. Resolve state dir.
   - `/opt/v7/egress/state`
2. Parse:
   - `users.registry`
   - `egress.registry`
   - `egress-load.state`
   - `egress-stability.state` or `stability.state`
   - fallback `egress-quality-summary.json` only if flat stability state is absent
   - `egress-diagnose.state`
   - `interface-state.state`
3. Reject target if:
   - occupied,
   - load users nonzero,
   - diagnose not OK,
   - avg/min/stability below floors,
   - Direct/RU exclusions missing,
   - disabled/manual/reserve-only.

Because `stability.state` exists, helper intentionally uses it as the movement-critical stability source before the quality summary fallback.

## E25.1 Raw Sources

`stability.state` at E25.1:

- mtime: `2026-05-28 13:32:36 +0300`
- `wireguard-1779454504-c43409_avg_mbps=30.0077`
- `wireguard-1779454504-c43409_min_mbps=21.66`
- `wireguard-1779454504-c43409_stability=0.721815`
- `wireguard-1779454504-c43409_samples=30`

`egress-quality-summary.json`:

- mtime: `2026-05-28 13:31:42 +0300`
- `5m.stability=0.605`
- `1h.stability=0.5919`
- `24h.stability=0.697`
- `7d.stability=0.8084`

`egress-load.state`:

- `users=0`
- `soft_limit=1`
- `hard_limit=2`
- `load_status=OK`

`egress-diagnose.state`:

- `diagnose_reason=OK`
- `diagnose_severity=OK`
- `diagnose_detail=handshake_age_seconds=71`

Target metadata:

- `canary_reserved=true`
- `reservation_owner=control_plane_governance`
- `exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU`

## Classification

`REAL_TARGET_DEGRADATION_TRANSIENT_RECOVERED`

Supporting evidence:

- E25 blocking source was not stale; `stability.state` was fresh and below floor.
- E25.1 uses the same source and now returns above floor.
- No helper code or threshold changed.
- No manual diagnostic refresh was performed.
- No target metadata drift was observed.
- Load/diagnose stayed OK, so the only E25 blocker was a transient quality/stability window.

## Safety Conclusion

Moving `10.7.0.11` to WireGuard is not automatically allowed by this block, but the target readiness blocker is recovered for packet preparation:

- `target_readiness_recovered=true`
- `target_readiness_final_status=GO`
- `helper_fix_applied=false`
