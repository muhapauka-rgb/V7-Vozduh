# AWG0 / AWG3 Stability Root Cause Report

Project: V7 Vozduh

Program: STABILITY.ROOT

Mode: READ ONLY

Date: 2026-06-13

## Executive Summary

BA.3 is blocked because the planner currently sees only one eligible channel: `vless`.

`awg0` and `awg3` are not failing because Telegram, Google, YouTube, Instagram, or Google Auth are down. Their service scores are excellent.

They are failing because their speed stability is poor: the low-end speed floor is too far below the average speed.

Final classification:

`REAL_CHANNEL_INSTABILITY`

Root cause:

`throughput_consistency_collapse_speed_p10_too_low_relative_to_average`

Plainly: the channels can open services, but speed dips too deeply and too often. The planner correctly treats them as risky for moving users.

## 1. Stability Formula Breakdown

The current stability chain is:

`egress-history.jsonl`

to

`tools/runtime-support/v7-egress-stability`

to

`/opt/v7/egress/state/stability.state`

to

`tools/runtime-support/v7-state-json`

to

`v7-state.json`

to

`tools/v7-egress-quality-compact`

to

`egress-quality-summary.json`

to

`tools/v7-users-autoswitch`

Stability is not a service reachability score.

The live formula is effectively:

```text
stability = low_speed_floor / average_speed
```

Where the low speed floor is derived from the recent speed history. In current evidence it is represented as `min_mbps` / p10-style floor.

The planner gate uses:

```text
min_stability = 0.45
```

The quality summary then keeps EMA windows:

```text
5m  alpha = 0.35
1h  alpha = 0.18
24h alpha = 0.06
7d  alpha = 0.02
```

So a channel can have good service checks and still fail stability if its low-speed floor collapses.

Evidence:

- `AWG0_AWG3_STABILITY_EVIDENCE/stability_formula_breakdown.json`
- `AWG0_AWG3_STABILITY_EVIDENCE/source_quality_compact_sample_and_ema_formula.txt`
- `AWG0_AWG3_STABILITY_EVIDENCE/source_stability_model_discovery.json`

## 2. Raw Signal Audit

Current production-derived planner evidence shows:

| Channel | Service score | Telegram | Avg Mbps | Low Mbps | Live stability | 1h stability | Floor | Blocker |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `awg0` | `100.0` | OK | `21.90` | `6.91` | `0.315` | `0.2162` | `0.45` | `stability_below_floor` |
| `awg3` | `99.767` | OK | `31.98` | `5.86` | `0.183` | `0.1836` | `0.45` | `stability_below_floor` |

The formula recomputes cleanly:

```text
awg0: 6.91 / 21.90 = 0.3155
awg3: 5.86 / 31.98 = 0.1832
```

That matches the observed live stability.

Service matrix state:

| Channel | YouTube | Instagram | Telegram | Google | Google Auth |
| --- | --- | --- | --- | --- | --- |
| `awg0` | OK / 100 | OK / 100 | OK / 100 | OK / 100 | OK / 100 |
| `awg3` | OK / 100 | OK / 100 | OK / 100 | OK / 100 | OK / 98.836 |

No safety events were present in this evidence:

- no incoming rollback signal
- no failed verification signal
- no quarantine signal

Evidence:

- `AWG0_AWG3_STABILITY_EVIDENCE/raw_signal_audit.json`
- `AWG0_AWG3_STABILITY_EVIDENCE/source_stability1_close_phase6_fresh_planner.json`

## 3. Time Window Analysis

The issue is recent and current, not permanent historical failure.

Observed stability trend:

| Channel | 2026-06-06 22:39 | 2026-06-06 22:54 | 2026-06-07 12:16 | 2026-06-13 07:46 |
| --- | ---: | ---: | ---: | ---: |
| `awg0` 1h | `0.5081` | `0.5991` | `0.5714` | `0.2162` |
| `awg3` 1h | `0.3104` | `0.5598` | `0.5260` | `0.1836` |

Both channels were able to cross the `0.45` floor earlier.

By 2026-06-13, both had fallen sharply below the floor:

- `awg0`: from healthy 1h stability to `0.2162`
- `awg3`: from healthy 1h stability to `0.1836`

This points to current/recent throughput instability, not a channel class that is inherently unusable.

Evidence:

- `AWG0_AWG3_STABILITY_EVIDENCE/time_window_analysis.json`
- `AWG0_AWG3_STABILITY_EVIDENCE/source_historical_stability_trend.json`

## 4. Service vs Stability Explanation

The apparent contradiction is real but not pathological:

```text
service score ~= 100
stability ~= 0.2
```

They measure different things.

Service score answers:

Can this channel reach required services right now?

Examples:

- Telegram
- Google
- YouTube
- Instagram
- Google Auth

Stability answers:

Is the channel's throughput consistent enough that users are unlikely to hit deep speed drops after movement?

So the current state means:

```text
Services are reachable.
Speed floor is unreliable.
```

This is why BA.3 should not blindly use `awg0` / `awg3` for 5-user autonomy yet.

Evidence:

- `AWG0_AWG3_STABILITY_EVIDENCE/service_vs_stability_explanation.json`

## 5. Event Forensics

The available evidence does not prove a Telegram outage, service outage, governance block, capacity block, or quarantine.

The event pattern that reduced stability is:

```text
speed oscillation / throughput floor collapse
```

Additional observed signals:

| Channel | 5m p95 latency | 1h p95 latency | 5m fail rate | 1h fail rate |
| --- | ---: | ---: | ---: | ---: |
| `awg0` | `3564.1 ms` | `4045.8 ms` | `0.0715` | `0.0716` |
| `awg3` | `2857.4 ms` | `2709.6 ms` | `0.1091` | `0.1335` |

These values support the stability finding: the channels are reachable, but the recent quality envelope is noisy.

Limitation:

The local evidence set does not include the raw last-30 speed samples from production `egress-history.jsonl`. Therefore this report proves the reducer at the stability-input level, but does not name each individual raw sample that caused the p10/min floor.

Evidence:

- `AWG0_AWG3_STABILITY_EVIDENCE/event_forensics.json`

## 6. AWG0 Root Cause

`awg0` chain:

1. Service probes pass.
2. Aggregate service score remains `100.0`.
3. Runtime speed history reports:
   - average speed: `21.90 Mbps`
   - low speed floor: `6.91 Mbps`
4. Live stability becomes:

```text
6.91 / 21.90 = 0.3155
```

5. 1h EMA stability remains lower:

```text
0.2162
```

6. Autoswitch quality gate requires:

```text
0.45
```

7. Candidate is blocked by:

```text
stability_below_floor
```

AWG0 is not blocked by:

- Telegram failure
- service matrix failure
- capacity
- governance reservation
- policy floor bug

AWG0 root cause:

`throughput_consistency_collapse_speed_p10_too_low_relative_to_average`

## 7. AWG3 Root Cause

`awg3` chain:

1. Service probes pass.
2. Aggregate service score remains about `99.767`.
3. Runtime speed history reports:
   - average speed: `31.98 Mbps`
   - low speed floor: `5.86 Mbps`
4. Live stability becomes:

```text
5.86 / 31.98 = 0.1832
```

5. 1h EMA stability remains:

```text
0.1836
```

6. Autoswitch quality gate requires:

```text
0.45
```

7. Candidate is blocked by:

```text
stability_below_floor
```

AWG3 is not blocked by:

- Telegram failure
- service matrix failure
- capacity
- governance reservation
- policy floor bug

AWG3 root cause:

`throughput_consistency_collapse_speed_p10_too_low_relative_to_average`

## 8. Recovery Forecast

If channels stay at current stability, they do not naturally recover above `0.45`.

If future samples become stable, recovery is possible.

Samples needed to cross `0.45`:

| Channel | Future sample stability | 5m | 1h | 24h | 7d |
| --- | ---: | ---: | ---: | ---: | ---: |
| `awg0` | current `0.315` | never | never | never | never |
| `awg0` | `0.50` | 4 | 9 | 21 | 6 |
| `awg0` | `0.70` | 2 | 4 | 7 | 2 |
| `awg0` | `0.90` | 1 | 3 | 5 | 1 |
| `awg3` | current `0.183` | never | never | never | never |
| `awg3` | `0.50` | 5 | 10 | 14 | already above |
| `awg3` | `0.70` | 2 | 4 | 4 | already above |
| `awg3` | `0.90` | 2 | 3 | 3 | already above |

This means the channels are recoverable if the speed floor improves. They are not proven permanently broken.

Evidence:

- `AWG0_AWG3_STABILITY_EVIDENCE/recovery_forecast.json`

## 9. Mismeasurement Audit

No evidence proves that stability is being underestimated.

Checks:

- The live stability values recompute from `min_mbps / avg_mbps`.
- Both 5m and 1h windows are below the floor.
- Service matrix does not contradict stability because it measures reachability, not throughput consistency.
- No stale-data mismatch was proven in the evidence set.
- EMA behavior is expected: it keeps recent instability visible until enough healthy samples arrive.

Possible limitation:

The raw production speed ring was not available in local evidence. A future read-only production capture could inspect the exact last-30 speed samples for `awg0` and `awg3`.

This limitation does not change the conclusion, because the current planner-facing values already prove why eligibility failed.

Evidence:

- `AWG0_AWG3_STABILITY_EVIDENCE/mismeasurement_audit.json`

## 10. Final Verdict

Final classification:

`REAL_CHANNEL_INSTABILITY`

Direct answer:

`awg0` and `awg3` have excellent service scores but poor stability because service checks are passing while the speed floor is collapsing relative to average speed.

The planner is not confusing Telegram health with channel stability. It is seeing:

```text
services reachable = true
throughput consistency = false
```

Therefore `stability_below_floor` is justified by the current evidence.

Final verdicts:

```text
awg0_root_cause_identified=true
awg3_root_cause_identified=true
service_quality_good=true
stability_low=true
measurement_artifact_proven=false
quality_model_issue_proven=false
root_cause=throughput_consistency_collapse_speed_p10_too_low_relative_to_average
classification=REAL_CHANNEL_INSTABILITY
floor_change_recommended=false
policy_change_recommended=false
runtime_changed=false
routing_changed=false
autonomy_changed=false
safe_next_step=AWG0_AWG3_SPEED_VARIANCE_OBSERVATION_AND_RAW_HISTORY_CAPTURE
```

Recommended next step:

Run a read-only production observation window that captures the raw speed samples behind `awg0` and `awg3`:

- `egress-history.jsonl`
- `stability.state`
- `egress-speed.json`
- `egress-quality-summary.json`
- service matrix at the same timestamp

Purpose:

identify the exact speed dips and decide whether the instability is caused by channel transport, measurement cadence, host load, remote endpoint behavior, or local probing noise.

Do not lower the stability floor yet.

Do not force `awg0` or `awg3` into BA.3 yet.
