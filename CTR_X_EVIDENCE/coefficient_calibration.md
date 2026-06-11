# CTR.X Coefficient Calibration Evidence

CTR.X required three coefficient models.

The passive observation-window collector now emits all three:

## MODEL_A_CURRENT

- TRUSTED: +20
- WATCH: 0
- NEW: -8
- RECOVERING: -12
- DEGRADED: -18
- QUARANTINED: -24

## MODEL_B_CONSERVATIVE

- TRUSTED: +10
- WATCH: 0
- NEW: -4
- RECOVERING: -6
- DEGRADED: -9
- QUARANTINED: -12

## MODEL_C_AGGRESSIVE

- TRUSTED: +40
- WATCH: 0
- NEW: -16
- RECOVERING: -24
- DEGRADED: -36
- QUARANTINED: -48

## Current production calibration result

No model can be certified on production data yet.

Reason:

- usable CTR shadow cycles: 0
- no winner changes available
- no quality outcomes available
- no service outcomes available

Therefore:

- MODEL_A_CURRENT=NEUTRAL_INSUFFICIENT_DATA
- MODEL_B_CONSERVATIVE=NEUTRAL_INSUFFICIENT_DATA
- MODEL_C_AGGRESSIVE=NEUTRAL_INSUFFICIENT_DATA

Coefficient tuning must wait for a production dry-run observation window with `ctr_shadow_comparison` payloads.

