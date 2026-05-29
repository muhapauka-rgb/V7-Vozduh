# E25.11 Long-Window Validation

## Result

`long_window_validation_performed=true`

`sample_count=19`

`window_start_utc=2026-05-28T14:56:23Z`

`window_end_utc=2026-05-28T15:16:32Z`

`sustained_go=false`

`no_sample_below_floor=false`

`quality_spikes_detected=true`

`target_users_zero=true`

`selected_moves_zero=true`

`hidden_movers_absent=true`

`runtime_checkers_ok=true`

## Why Not 20 Samples

The planned 20-sample SSH collection window was interrupted by a remote connection reset after sample 19:

```text
Read from remote host 195.2.79.116: Connection reset by peer
client_loop: send disconnect: Broken pipe
```

The collected 19 samples still span approximately 20 minutes. This report does not claim a 20/20 sample window.

## Sample Summary

| Sample | UTC | Status | Mbps | Ping Loss | RTT Avg ms | Readiness | Checkers | Selected Moves | Hidden Movers |
| --- | --- | --- | ---: | --- | ---: | --- | --- | ---: | ---: |
| 1 | 14:56:23 | OK | 11.36 | 0 | 63.422 | GO | OK | 0 | 0 |
| 2 | 14:57:30 | OK | 7.49 | 0 | 35.332 | GO | OK | 0 | 0 |
| 3 | 14:58:37 | OK | 12.43 | 0 | 28.097 | GO | OK | 0 | 0 |
| 4 | 14:59:43 | OK | 15.74 | 0 | 22.546 | GO | OK | 0 | 0 |
| 5 | 15:00:51 | OK | 13.29 | 0 | 27.187 | GO | OK | 0 | 0 |
| 6 | 15:01:58 | OK | 13.68 | 0 | 38.277 | GO | OK | 0 | 0 |
| 7 | 15:03:08 | OK | 9.45 | 0 | 34.579 | GO | OK | 0 | 0 |
| 8 | 15:04:15 | OK | 8.50 | 0 | 32.221 | GO | OK | 0 | 0 |
| 9 | 15:05:23 | OK | 12.09 | 0 | 25.364 | GO | OK | 0 | 0 |
| 10 | 15:06:31 | OK | 9.53 | 0 | 30.286 | GO | OK | 0 | 0 |
| 11 | 15:07:38 | OK | 13.69 | 0 | 25.986 | GO | OK | 0 | 0 |
| 12 | 15:08:45 | OK | 13.16 | 0 | 26.529 | GO | OK | 0 | 0 |
| 13 | 15:09:51 | OK | 5.08 | 0 | 77.442 | GO | OK | 0 | 0 |
| 14 | 15:11:00 | OK | 14.27 | 0 | 27.968 | GO | OK | 0 | 0 |
| 15 | 15:12:06 | OK | 15.78 | 0 | 23.937 | GO | OK | 0 | 0 |
| 16 | 15:13:13 | OK | 14.56 | 0 | 27.776 | GO | OK | 0 | 0 |
| 17 | 15:14:20 | OK | 10.89 | 0 | 38.809 | GO | OK | 0 | 0 |
| 18 | 15:15:26 | OK | 11.81 | 0 | 23.162 | GO | OK | 0 | 0 |
| 19 | 15:16:32 | OK | 15.69 | 0 | 27.093 | GO | OK | 0 | 0 |

## Quality Verdict

- observed min Mbps: `5.08`
- observed avg Mbps: `12.03`
- samples below `10 Mbps`: `5`
- stability ratio used for state: `0.737`

After the window, the execution target runtime state was updated conservatively:

```text
amneziawg-exec-20260528-10-8-1-14_avg_mbps=12.03
amneziawg-exec-20260528-10-8-1-14_min_mbps=5.08
amneziawg-exec-20260528-10-8-1-14_stability=0.737
```

`v7-second-canary-target-readiness --execution-target-id amneziawg-exec-20260528-10-8-1-14` then returned:

- selected target: `NONE`
- approval status: `NO-GO`
- target reason: `avg_mbps below floor (12.03); min_mbps below floor (5.08)`

## Governance Verdict

The target is platform-integrated and governed correctly:

- runtime checkers remained OK in every collected sample;
- selected moves remained zero;
- hidden movers remained absent;
- candidate user remained on `1`;
- no user movement occurred.

The remaining blocker is target quality stability, not platform integration.
