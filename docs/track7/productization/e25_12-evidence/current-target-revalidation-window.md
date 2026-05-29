# E25.12 Current Target Revalidation Window

## Result

`current_target_revalidation_window_collected=true`

`current_target_recovered=true`

`target_readiness_final_status=GO`

`sustained_go=true`

`no_sample_below_floor=true`

`quality_spikes_detected=false`

`first_movement_ready=true`

## Window

- target: `amneziawg-exec-20260528-10-8-1-14`
- interface: `v7execwg0`
- selected recovery: `MTU=1200`
- sample count: `20`
- window start UTC: `2026-05-28T17:38:51Z`
- window end UTC: `2026-05-28T18:00:40Z`
- span: `1309 seconds`
- user movement performed: `false`
- routing mutation for users performed: `false`

## Quality Summary

- avg Mbps final: `27.12`
- min Mbps final: `10.67`
- stability final: `1.000`
- samples below `10.0 Mbps`: `0`
- samples below `15.0 Mbps`: `5`
- readiness avg floor: `15.0 Mbps`
- readiness min floor: `10.0 Mbps`

The target remained above the hard per-window min floor on every sample. Samples `1`, `2`, `17`, `19`, and `20` were below `15 Mbps`, but the readiness model requires the window average to be at or above `15 Mbps`, and the final average was `27.12 Mbps`.

## Sample Summary

| Sample | UTC | Mbps | Ping Loss % | RTT Avg ms | Checkers | Selected Moves | Hidden Movers | Candidate Current | Target Users |
| ---: | --- | ---: | ---: | ---: | --- | ---: | ---: | --- | ---: |
| 1 | 2026-05-28T17:38:51Z | 12.60 | 0 | 26.710 | OK | 0 | 0 | 1 | 0 |
| 2 | 2026-05-28T17:40:00Z | 14.34 | 0 | 27.181 | OK | 0 | 0 | 1 | 0 |
| 3 | 2026-05-28T17:41:11Z | 17.09 | 0 | 131.057 | OK | 0 | 0 | 1 | 0 |
| 4 | 2026-05-28T17:42:21Z | 43.04 | 0 | 42.776 | OK | 0 | 0 | 1 | 0 |
| 5 | 2026-05-28T17:43:29Z | 18.75 | 0 | 45.806 | OK | 0 | 0 | 1 | 0 |
| 6 | 2026-05-28T17:44:38Z | 41.16 | 0 | 22.707 | OK | 0 | 0 | 1 | 0 |
| 7 | 2026-05-28T17:45:46Z | 40.59 | 0 | 35.622 | OK | 0 | 0 | 1 | 0 |
| 8 | 2026-05-28T17:46:55Z | 30.03 | 0 | 29.025 | OK | 0 | 0 | 1 | 0 |
| 9 | 2026-05-28T17:48:03Z | 45.48 | 0 | 37.273 | OK | 0 | 0 | 1 | 0 |
| 10 | 2026-05-28T17:49:12Z | 21.16 | 0 | 34.491 | OK | 0 | 0 | 1 | 0 |
| 11 | 2026-05-28T17:50:21Z | 31.72 | 0 | 22.750 | OK | 0 | 0 | 1 | 0 |
| 12 | 2026-05-28T17:51:29Z | 19.05 | 0 | 38.767 | OK | 0 | 0 | 1 | 0 |
| 13 | 2026-05-28T17:52:39Z | 29.33 | 0 | 35.046 | OK | 0 | 0 | 1 | 0 |
| 14 | 2026-05-28T17:53:47Z | 26.65 | 0 | 50.605 | OK | 0 | 0 | 1 | 0 |
| 15 | 2026-05-28T17:54:56Z | 32.37 | 0 | 24.199 | OK | 0 | 0 | 1 | 0 |
| 16 | 2026-05-28T17:56:05Z | 31.36 | 0 | 26.298 | OK | 0 | 0 | 1 | 0 |
| 17 | 2026-05-28T17:57:13Z | 10.67 | 0 | 39.198 | OK | 0 | 0 | 1 | 0 |
| 18 | 2026-05-28T17:58:22Z | 47.72 | 0 | 27.054 | OK | 0 | 0 | 1 | 0 |
| 19 | 2026-05-28T17:59:31Z | 14.74 | 0 | 62.875 | OK | 0 | 0 | 1 | 0 |
| 20 | 2026-05-28T18:00:40Z | 14.64 | 0 | 38.493 | OK | 0 | 0 | 1 | 0 |

Raw data:

- `docs/track7/productization/e25_12-evidence/quality-samples.tsv`
- `docs/track7/productization/e25_12-evidence/restore-settle-samples/`

## Runtime Quality State Update

The live quality state was updated conservatively from the 20-sample window:

```text
amneziawg-exec-20260528-10-8-1-14_avg_mbps=27.12
amneziawg-exec-20260528-10-8-1-14_min_mbps=10.67
amneziawg-exec-20260528-10-8-1-14_stability=1.000
```

This is the only post-recovery runtime state update beyond the target-local MTU change.

## Readiness Result

Command:

`v7-second-canary-target-readiness --execution-target-id amneziawg-exec-20260528-10-8-1-14 --pretty`

Result:

- selected target: `amneziawg-exec-20260528-10-8-1-14`
- approval status: `GO`
- diagnose: `OK`
- load: `OK`
- users count: `0`
- avg Mbps: `27.12`
- min Mbps: `10.67`
- stability: `1.0`
- execution allowed now: `false`

Full outputs:

- `docs/track7/productization/e25_12-evidence/final-readiness.pretty`
- `docs/track7/productization/e25_12-evidence/final-readiness.json`

## Restore-Settle Result

Command:

`v7-restore-settle-gate --pre-restore --state-dir /tmp/e25_12_restore_settle_samples`

Result:

- gate status: `GO`
- sample count: `20`
- samples span seconds: `1309`
- apply timer intervals covered: `65.45`
- selected moves by sample: all `0`
- registry stable: `true`
- egress registry stable: `true`
- checkers OK: `true`
- hidden movers observed: `false`
- moved users: none

Full outputs:

- `docs/track7/productization/e25_12-evidence/restore-settle-gate.pretty`
- `docs/track7/productization/e25_12-evidence/restore-settle-gate.json`

## Verdict

`quality_recovery_successful=true`

The current execution target recovered after target-local MTU tuning. Replacement profile search/import is not required for the next movement-preparation block.
