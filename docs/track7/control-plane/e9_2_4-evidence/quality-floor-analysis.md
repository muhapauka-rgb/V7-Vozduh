# E9.2.4 AWG0 / AWG3 Quality Floor Analysis

Mode: read-only diagnostics only.

Targets:

- `awg0`
- `awg3`

## Observed State

| Target | Interface State | Registry Users | Load Users | Diagnose | Avg Mbps | Min Mbps | Stability | Route-Class Exclusions | Readiness Blocker |
|---|---|---:|---:|---|---:|---:|---:|---|---|
| `awg0` | `UP,LOWER_UP` | 0 | 0 | `OK` | 11.909 | 4.17 | 0.350155 | none declared | below avg/min/stability floor; policy-sensitive exclusions absent |
| `awg3` | `UP,LOWER_UP` | 0 | 0 | `OK` | 5.62633 | 4.39 | 0.78026 | none declared | below avg/min floor; policy-sensitive exclusions absent |

## Quality Floor

The current watcher and autoswitch policy use:

```text
min_avg_mbps=15.0
min_floor_mbps=10.0
min_stability=0.45
```

`tools/v7-users-autoswitch` blocks targets below these thresholds:

```text
avg_mbps_below_floor
min_mbps_below_floor
stability_below_floor
```

`tools/runtime-support/v7-egress-stability` calculates stability from the last 30 non-zero history samples:

```text
avg = average of last non-zero samples
floor = p10 floor sample
stability = floor / avg
```

## Interpretation

`awg0` and `awg3` are not rejected due to load or interface state. They are rejected because observed quality is below the canary floor.

`awg0`:

- avg is below 15 Mbps;
- min is below 10 Mbps;
- stability is below 0.45;
- no Direct/RU or Trusted RU exclusions are declared in the egress row.

`awg3`:

- avg is far below 15 Mbps;
- min is below 10 Mbps;
- stability is above 0.45 but the speed floor still fails;
- no Direct/RU or Trusted RU exclusions are declared in the egress row;
- prior E-governance already avoided `awg3` as a target.

## Classification

| Target | Classification | Reason |
|---|---|---|
| `awg0` | `QUALITY_TOO_LOW` | Real observed quality floor failure; not a clean second canary target. |
| `awg3` | `QUALITY_TOO_LOW` | Real observed avg/min floor failure; not a clean second canary target. |

## Canary Implication

Neither AWG target should be used for E9.3 unless the test definition changes and the operator explicitly accepts a low-quality target. That is not recommended for a mechanics reproducibility canary.
