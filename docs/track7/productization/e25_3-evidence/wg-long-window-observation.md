# E25.3 WireGuard Long Window Observation

## Scope

Target:

`wireguard-1779454504-c43409`

Observation window:

- start: `2026-05-28T11:15:00Z`
- end: `2026-05-28T11:30:08Z`
- samples: `16`
- interval: approximately `60s`
- raw log: `docs/track7/productization/e25_3-evidence/wg-long-window-raw.log`

No users were moved. No routing was mutated.

## Summary

| Metric | Result |
|---|---:|
| Samples | 16 |
| GO samples | 16 |
| NO-GO samples | 0 |
| min of `min_mbps` | 16.81 |
| max of `min_mbps` | 19.54 |
| min stability | 0.655310 |
| max stability | 0.771378 |

## Timeline

| Sample | Timestamp UTC | Verdict | Selected Target | Avg Mbps | Min Mbps | Stability | Handshake |
|---:|---|---|---|---:|---:|---:|---|
| 1 | 2026-05-28T11:15:00Z | GO | wireguard-1779454504-c43409 | 25.5610 | 16.81 | 0.657643 | 41 seconds |
| 2 | 2026-05-28T11:16:01Z | GO | wireguard-1779454504-c43409 | 25.6520 | 16.81 | 0.655310 | 1m41s |
| 3 | 2026-05-28T11:17:01Z | GO | wireguard-1779454504-c43409 | 25.8340 | 19.54 | 0.756368 | 38 seconds |
| 4 | 2026-05-28T11:18:02Z | GO | wireguard-1779454504-c43409 | 25.9250 | 19.54 | 0.753713 | 1m38s |
| 5 | 2026-05-28T11:19:02Z | GO | wireguard-1779454504-c43409 | 25.9660 | 19.54 | 0.752523 | 39 seconds |
| 6 | 2026-05-28T11:20:03Z | GO | wireguard-1779454504-c43409 | 25.9160 | 19.54 | 0.753974 | 1m39s |
| 7 | 2026-05-28T11:21:03Z | GO | wireguard-1779454504-c43409 | 25.8160 | 19.54 | 0.756895 | 36 seconds |
| 8 | 2026-05-28T11:22:04Z | GO | wireguard-1779454504-c43409 | 25.7660 | 19.54 | 0.758364 | 1m36s |
| 9 | 2026-05-28T11:23:04Z | GO | wireguard-1779454504-c43409 | 25.6660 | 19.54 | 0.761318 | 33 seconds |
| 10 | 2026-05-28T11:24:05Z | GO | wireguard-1779454504-c43409 | 25.9380 | 19.54 | 0.753335 | 1m33s |
| 11 | 2026-05-28T11:25:05Z | GO | wireguard-1779454504-c43409 | 26.0593 | 19.54 | 0.749828 | 30 seconds |
| 12 | 2026-05-28T11:26:06Z | GO | wireguard-1779454504-c43409 | 26.1200 | 19.54 | 0.748086 | 1m30s |
| 13 | 2026-05-28T11:27:06Z | GO | wireguard-1779454504-c43409 | 26.2413 | 19.54 | 0.744628 | 31 seconds |
| 14 | 2026-05-28T11:28:07Z | GO | wireguard-1779454504-c43409 | 26.3020 | 19.54 | 0.742909 | 1m31s |
| 15 | 2026-05-28T11:29:07Z | GO | wireguard-1779454504-c43409 | 26.3627 | 19.54 | 0.741199 | 28 seconds |
| 16 | 2026-05-28T11:30:08Z | GO | wireguard-1779454504-c43409 | 25.3313 | 19.54 | 0.771378 | 1m28s |

## Oscillation Analysis

E25.2 observed a fresh NO-GO immediately before the proposed movement:

- `min_mbps=4.61`
- `stability≈0.30`

E25.3 then observed 16 consecutive GO samples over about 15 minutes:

- `min_mbps>=16.81`
- `stability>=0.655310`

This proves the target is not permanently failed, but it also proves the execution target can oscillate across the readiness boundary within a short operational window.

## Interface / Runtime Observations

The target stayed zero-user during the window. `ip -s link` showed no RX/TX errors or drops in sampled output. `wg show` showed regular handshakes, with latest handshake ages below about two minutes in samples.

## Result

`target_generally_ok_but_spiky=true`

`single_execution_time_recheck_required=true`

`sustained_pre_execution_go_window_required=true`
