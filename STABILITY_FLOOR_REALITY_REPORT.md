# STABILITY_FLOOR.1 - Channel Stability Floor Validation And Eligibility Reality Audit

Дата: 2026-06-13  
Workspace: `/Users/ponch/Documents/New project`  
Branch: `Updatesystem`  
Mode: READ ONLY. No policy changes, no floor changes, no eligibility changes, no routing changes, no autonomy changes.

## Executive Summary

Финальный вывод: `0.45` выглядит оправданным как production safety floor. `awg0` и `awg3` сейчас исключены корректно.

Это не похоже на “здоровые каналы, задавленные слишком консервативным floor”. Оба канала имеют хорошие service scores и Telegram OK, но свежая stability действительно просела:

- `awg0`: live `0.315`, 1h `0.2162`
- `awg3`: live `0.183`, 1h `0.1836`
- текущий floor: `0.45`

Контрфактическая проверка floors из промпта:

| Floor | Planner pool | BA.3 readiness |
|---:|---:|---|
| 0.45 | `vless` only | false |
| 0.40 | `vless` only | false |
| 0.35 | `vless` only | false |
| 0.30 | `vless` only | false |

Чтобы оба `awg0/awg3` прошли только по stability, floor пришлось бы опустить примерно до `0.15`, что уже выглядит как опасное ослабление, а не настройка.

## Phase 1 - Stability Model Discovery

Evidence:

- `STABILITY_FLOOR_EVIDENCE/stability_model_discovery.json`
- `STABILITY_FLOOR_EVIDENCE/autoswitch_default_quality_policy.txt`
- `STABILITY_FLOOR_EVIDENCE/autoswitch_candidate_quality_gate.txt`
- `STABILITY_FLOOR_EVIDENCE/quality_compact_header_and_windows.txt`
- `STABILITY_FLOOR_EVIDENCE/quality_compact_sample_and_ema_formula.txt`

Owners:

- stability writer: `tools/v7-egress-quality-compact`
- eligibility consumer: `tools/v7-users-autoswitch`
- source file: `egress-quality-summary.json`

What stability measures:

`stability` is a rolling quality signal based on runtime state/speed quality, then smoothed into EMA windows:

- `5m` alpha `0.35`
- `1h` alpha `0.18`
- `24h` alpha `0.06`
- `7d` alpha `0.02`

`v7-egress-quality-compact` builds samples from:

- `v7-state.json`
- `egress-speed.json`
- `service-matrix.json`

It takes `live.stability` first, falls back to speed stability, and falls back to `1.0 if ok else 0.0`.

Eligibility logic in `v7-users-autoswitch`:

- read live `egress.stability`;
- read 1h historical stability from `egress-quality-summary.json`;
- if live stability is below floor and 1h stability is also below floor, block with `stability_below_floor`;
- exception exists only for protocol diagnostic limited suspect channels with strong service evidence and minimum stability `0.15`.

## Phase 2 - Floor Origin Audit

Evidence:

- `tools/v7-users-autoswitch:80`
- `tools/v7-second-canary-target-readiness:34`
- `tools/v7-observability-summary:252`

`0.45` is not learned dynamically. It is configured/hardcoded as a default safety threshold:

- `DEFAULT_QUALITY_POLICY["min_stability"] = 0.45`
- current planner evidence reports `min_stability=0.45`
- canary target readiness also uses stability floor `0.45`
- observability marks degraded when stability `<0.45`

Owner: current runtime planner owner, `tools/v7-users-autoswitch`, with policy override possible through quality policy.

Verdict: floor is a deliberate safety threshold, not a temporary BA.3-specific rule.

## Phase 3 - AWG0 Forensics

Evidence:

- `STABILITY_FLOOR_EVIDENCE/awg0_awg3_forensics.json`
- `STABILITY_FLOOR_EVIDENCE/current_channel_stability_table.json`

`awg0` values:

| Metric | Value |
|---|---:|
| service score | 100.0 |
| Telegram | OK |
| live stability | 0.315 |
| 5m stability | 0.2268 |
| 1h stability | 0.2162 |
| 24h stability | 0.3186 |
| 7d stability | 0.4436 |
| floor | 0.45 |
| blocker | `stability_below_floor` |

Why `awg0` got blocked:

- live stability is below floor by `-0.135`;
- 1h stability is below floor by `-0.2338`;
- 24h is below floor by `-0.1314`;
- 7d is just under floor by `-0.0064`;
- health severity is `OK`, so protocol diagnostic exception does not apply;
- service score is good, but service score is not allowed to override normal-channel stability floor.

Classification: `TEMPORARILY_UNSTABLE`, not misclassified.

## Phase 4 - AWG3 Forensics

Evidence:

- `STABILITY_FLOOR_EVIDENCE/awg0_awg3_forensics.json`
- `STABILITY_FLOOR_EVIDENCE/current_channel_stability_table.json`

`awg3` values:

| Metric | Value |
|---|---:|
| service score | 99.767 |
| Telegram | OK |
| live stability | 0.183 |
| 5m stability | 0.1098 |
| 1h stability | 0.1836 |
| 24h stability | 0.387 |
| 7d stability | 0.4964 |
| floor | 0.45 |
| blocker | `stability_below_floor` |

Why `awg3` got blocked:

- live stability is below floor by `-0.267`;
- 1h stability is below floor by `-0.2664`;
- 24h is below floor by `-0.063`;
- 7d is above floor, but planner uses fresh/live + 1h for current eligibility;
- no protocol diagnostic exception applies.

Classification: `TEMPORARILY_UNSTABLE`, not misclassified.

## Phase 5 - Channel-By-Channel Analysis

Evidence:

- `STABILITY_FLOOR_EVIDENCE/current_channel_stability_table.json`
- `STABILITY_FLOOR_EVIDENCE/current_channel_stability_table.csv`

| Channel | Stability 1h | Service score | Health | Eligible | Reason |
|---|---:|---:|---|---|---|
| `vless` | 0.4814 | 100.0 | SUSPECT, non-hard | true | passes via service-backed exception |
| `awg0` | 0.2162 | 100.0 | OK | false | `stability_below_floor` |
| `awg3` | 0.1836 | 99.767 | OK | false | `stability_below_floor` |
| `wireguard-1779454504-c43409` | 0.8216 | 100.0 | OK | false | `canary_reserved_production_assignment_blocked` |
| `amneziawg-exec-20260528-10-8-1-14` | 0.1567 | 100.0 | OK | false | manual/reserve/canary + stability |
| `1` | 0.0002 | 2.834 | FAIL | false | hard fail + Telegram down + speed floors |
| `openvpn-1779388847-d2ad7c` | 0.0002 | 2.838 | FAIL | false | hard fail + Telegram down + speed floors |

Channels that fail only because of stability:

- `awg0`
- `awg3`

## Phase 6 - Counterfactual Analysis

Evidence:

- `STABILITY_FLOOR_EVIDENCE/floor_counterfactual.json`

Diagnostic only. Runtime was not modified.

| Floor | Healthy channels under current evidence | Pool size | BA.3 readiness |
|---:|---|---:|---|
| 0.45 | `vless` | 1 | false |
| 0.40 | `vless` | 1 | false |
| 0.35 | `vless` | 1 | false |
| 0.30 | `vless` | 1 | false |

Additional diagnostic:

| Floor | Effect |
|---:|---|
| 0.20 | `awg0` could enter, `awg3` still blocked |
| 0.15 | `awg0` and `awg3` could enter |

Interpretation:

Lowering from `0.45` to `0.30` would not solve BA.3. To recover both `awg0` and `awg3` by threshold alone requires a very large reduction to about `0.15`, which would admit channels with very weak short-window stability.

## Phase 7 - Historical Validation

Evidence:

- `STABILITY_FLOOR_EVIDENCE/historical_stability_trend.json`
- `STABILITY_FLOOR_EVIDENCE/historical_stability_trend.csv`

Historical samples:

| Snapshot | awg0 1h | awg3 1h | Meaning |
|---|---:|---:|---|
| 2026-06-06 22:39 | 0.5081 | 0.3104 | awg0 passed, awg3 did not |
| 2026-06-06 22:54 | 0.5991 | 0.5598 | both passed |
| 2026-06-07 12:16 | 0.5714 | 0.5260 | both passed |
| 2026-06-13 07:46 | 0.2162 | 0.1836 | both fail |

This matters: the same `0.45` floor allowed `awg0/awg3` when they were actually stable enough. The current exclusion is caused by a real deterioration in current/1h stability, not by a floor that always suppresses them.

## Phase 8 - Misclassification Audit

`awg0`: `TEMPORARILY_UNSTABLE`

Evidence:

- service score 100;
- Telegram OK;
- no hard health fail;
- live and 1h stability far below floor;
- historical 7d almost at floor, meaning channel is not permanently bad.

`awg3`: `TEMPORARILY_UNSTABLE`

Evidence:

- service score 99.767;
- Telegram OK;
- no hard health fail;
- live and 1h stability far below floor;
- 7d stability above floor, meaning recent instability is sharper than long-term history.

No `MISCLASSIFIED` result is proven.

## Phase 9 - Final Verdict

Answer: `awg0` and `awg3` are not proven too broken forever, but they are truly too unstable for current production planner use.

Is `0.45` justified?

Yes, based on current evidence:

- it is a repeated safety threshold, not a BA.3-only hack;
- it previously allowed `awg0/awg3` when their 1h stability was above floor;
- it currently blocks them because live and 1h stability are well below floor;
- lowering to `0.30` would not restore BA.3 anyway;
- lowering to `0.15` would likely increase risk by admitting very unstable recent channels.

Should `awg0` be excluded?

Yes, for now. It is service-healthy but current/1h unstable.

Should `awg3` be excluded?

Yes, for now. It is service-healthy but even more unstable in live/1h windows.

Would changing the floor likely improve V7?

Not at the tested floors `0.40/0.35/0.30`. It would not restore BA.3. A large drop to around `0.15` might increase candidate count, but would materially increase routing risk.

Recommended next step:

`AWG0_AWG3_STABILITY_RECOVERY_WINDOW_AND_SERVICE_RETEST`

Do not lower the floor yet. Instead:

1. Observe/retest `awg0` and `awg3` over a fresh stability window.
2. Confirm whether live + 1h stability recover above `0.45`.
3. If they recover, rerun BA.3 fresh planner.
4. If they do not recover, investigate why their service score is high while stability is low.

## Final Verdicts

| Verdict | Value |
|---|---|
| stability_model_understood | true |
| floor_origin_known | true |
| floor_origin | `DEFAULT_QUALITY_POLICY.min_stability=0.45`, policy-owned by `tools/v7-users-autoswitch` |
| awg0_root_cause_known | true |
| awg3_root_cause_known | true |
| awg0_classification | `TEMPORARILY_UNSTABLE` |
| awg3_classification | `TEMPORARILY_UNSTABLE` |
| awg0_misclassified | false |
| awg3_misclassified | false |
| floor_0_45_justified | true |
| lowering_to_0_30_solves_ba3 | false |
| lowering_floor_likely_increases_risk | true |
| runtime_changed | false |
| policy_changed | false |
| routing_changed | false |
| apply_executed | false |
| SAFE_NEXT_STEP | `AWG0_AWG3_STABILITY_RECOVERY_WINDOW_AND_SERVICE_RETEST` |

