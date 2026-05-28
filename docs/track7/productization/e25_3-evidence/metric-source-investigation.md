# E25.3 Metric Source Investigation

## Helper

Tool:

`tools/v7-second-canary-target-readiness`

The helper is read-only. Its module docstring says it never calls `v7-user-switch`, `v7-routing-sync`, autoswitch, `ip`, `nft`, `systemctl`, SSH, or live mutation commands.

## State Files Read

The helper resolves a state directory, preferring `/opt/v7/egress/state` when live runtime files exist.

It reads:

- `users.registry`
- `egress.registry`
- `egress-load.state`
- `egress-stability.state` if present
- `stability.state` if `egress-stability.state` is absent
- `egress-quality-summary.json` only if no flat stability state exists
- `egress-diagnose.state`
- `interface-state.state` when present

## Authoritative Source

For live movement readiness, `stability.state` was authoritative in E25.2/E25.3 because it existed and contained WireGuard rows.

`egress-quality-summary.json` is a fallback for the helper, not the primary source when `stability.state` is present.

## Thresholds

The helper uses:

```text
avg_mbps >= 15.0
min_mbps >= 10.0
stability >= 0.45
```

The helper also requires:

- candidate still on expected current egress
- target not current baseline egress
- target enabled
- interface confirmed or inferred UP/LOWER_UP
- zero registry users
- zero load users
- diagnose OK
- not manual-only
- not reserve-only
- Direct/RU and Trusted/RU sensitive exclusions present

## Source Freshness

During E25.2 blocker investigation, source files were fresh at the VPS local time around `2026-05-28 14:01 +0300`:

- `stability.state`
- `egress-quality-summary.json`
- `egress-load.state`
- `egress-diagnose.state`

During E25.3 final safety check, target readiness again read live runtime state and returned GO.

## Source Divergence

E25.2:

- `stability.state`: WireGuard `min_mbps=4.61`, `stability≈0.30`
- quality summary 5m: `min_mbps=8.895`, `stability=0.4104`, trend `degrading`

Both sources showed short-window degradation, though `stability.state` was stricter and more movement-critical.

E25.3:

- 16/16 `stability.state` samples returned GO.
- quality summary later showed WireGuard 5m `min_mbps=15.533`, `stability=0.6146`, trend `improving`.

## Semantics Review

The helper semantics are strict but correct for first governed movement. It did not produce a false NO-GO in E25.2: the primary live movement-readiness source and the smoothed quality summary both supported a degraded short window.

No threshold change is justified.

## Result

- `metrics_stale=false`
- `helper_false_no_go=false`
- `readiness_gate_correct=true`
- `scoring_noise_detected=false`
- `metric_volatility_detected=true`
