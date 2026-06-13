# TRANSPORT.1 AWG0 / AWG3 Raw Stability Forensics Report

Project: V7 Vozduh

Mode: READ ONLY

Date: 2026-06-13

## Executive Summary

TRANSPORT.1 answered the remaining question:

Why do `awg0` and `awg3` lose stability while service scores stay excellent?

Final answer:

`awg0` and `awg3` are reachable, but their shared AmneziaWG transport path has bursty throughput collapse.

The key evidence is simple:

- `awg0` and `awg3` both use the same remote endpoint: `194.124.210.244:34403`
- both return HTTP code `200`
- both pass Telegram/service checks
- both have deep speed drops
- `vless` survives the same measurement window
- reserved WireGuard also survives the same measurement window

Final classification:

`REMOTE_ENDPOINT_INSTABILITY`

More precise wording:

`shared_amneziawg_endpoint_or_path_instability`

This is not a planner bug.

This is not an autonomy bug.

This is not a stability floor bug.

This is not a Telegram outage.

## 1. Raw Sample Analysis

Production capture was collected read-only from:

`/opt/v7/egress/state/`

Captured files:

- `egress-history.jsonl`
- `stability.state`
- `egress-speed.json`
- `egress-quality-summary.json`
- `service-matrix.json`
- `v7-state.json`
- `egress.registry`

Evidence folder:

`TRANSPORT1_EVIDENCE/`

The raw history has `120` rows. The last-30 window covers:

`2026-06-13T14:54:05+03:00`

to

`2026-06-13T15:15:56+03:00`

### Last 30 Real Samples

#### vless

`vless` stays stable. It never falls below `26.7038 Mbps` in the last-30 window.

```text
53.8649, 53.8649, 53.8649, 53.8649, 53.8649,
26.7038, 26.7038, 26.7038, 26.7038, 26.7038, 26.7038, 26.7038, 26.7038,
51.5326, 51.5326, 51.5326, 51.5326, 51.5326, 51.5326, 51.5326,
51.8062, 51.8062, 51.8062, 51.8062, 51.8062, 51.8062, 51.8062, 51.8062,
44.3389, 44.3389, 44.3389
```

All samples returned code `200`.

#### awg0

`awg0` is bursty. It jumps from `3.3481 Mbps` to `50.0315 Mbps`, then collapses again to `6-7 Mbps`.

```text
3.3481, 3.3481, 3.3481, 3.3481, 3.3481,
50.0315, 50.0315, 50.0315, 50.0315, 50.0315, 50.0315, 50.0315, 50.0315,
6.6710, 6.6710, 6.6710, 6.6710, 6.6710, 6.6710, 6.6710,
7.4650, 7.4650, 7.4650, 7.4650, 7.4650, 7.4650, 7.4650, 7.4650,
6.9547, 6.9547, 6.9547
```

All samples returned code `200`.

#### awg3

`awg3` also has bursts and a fresh hard drop at the end.

```text
15.0912, 15.0912, 15.0912, 15.0912, 15.0912,
54.9401, 54.9401, 54.9401, 54.9401, 54.9401, 54.9401, 54.9401, 54.9401,
19.4123, 19.4123, 19.4123, 19.4123, 19.4123, 19.4123, 19.4123,
17.7313, 17.7313, 17.7313, 17.7313, 17.7313, 17.7313, 17.7313, 17.7313,
4.6354, 4.6354, 4.6354
```

All samples returned code `200`.

Full last-30, last-50, and last-100 samples are stored in:

- `TRANSPORT1_EVIDENCE/analysis/raw_samples_last_30_50_100.json`
- `TRANSPORT1_EVIDENCE/analysis/awg0_last100_samples.csv`
- `TRANSPORT1_EVIDENCE/analysis/awg3_last100_samples.csv`
- `TRANSPORT1_EVIDENCE/analysis/vless_last100_samples.csv`

## 2. Variance Analysis

The production stability script uses the 30 most recent nonzero samples.

It sorts the values and uses:

```text
p10_index = ceil(count / 10)
floor = sorted[p10_index]
stability = floor / average
```

### Last 30

| Channel | Avg Mbps | Median Mbps | Production floor Mbps | Min Mbps | Max Mbps | Stability | Code 000 | Code 200 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `vless` | `44.5761` | `51.5326` | `26.7038` | `26.7038` | `53.8649` | `0.5991` | `0` | `30` |
| `awg0` | `18.0308` | `7.4650` | `3.3481` | `3.3481` | `50.0315` | `0.1857` | `0` | `30` |
| `awg3` | `26.3843` | `18.5718` | `4.6354` | `4.6354` | `54.9401` | `0.1757` | `0` | `30` |

Important:

`awg0` has a high maximum, but the median is only `7.465 Mbps`.

That means the channel is not merely slower than `vless`; it is unstable.

`awg3` has a high maximum too, but the fresh final drop to `4.6354 Mbps` pulls the production floor down.

### Low-Speed Counts

| Channel | Below 1 Mbps | Below 5 Mbps | Below 10 Mbps |
| --- | ---: | ---: | ---: |
| `vless` | `0` | `0` | `0` |
| `awg0` | `0` | `4` | `22` |
| `awg3` | `0` | `3` | `3` |

This is the core difference:

`vless` has no low-speed floor collapse.

`awg0` and `awg3` do.

Evidence:

- `TRANSPORT1_EVIDENCE/analysis/variance_analysis.json`
- `TRANSPORT1_EVIDENCE/raw_capture/production_state/stability.state`

## 3. Drop Detection

Drop detection used the last-100 samples.

Drop threshold:

```text
max(5 Mbps, 45% of channel last-100 average)
```

### awg0 Drops

`awg0` last-100 average:

`24.1972 Mbps`

Drop threshold:

`10.8888 Mbps`

Detected:

- `46` drop samples
- `5` drop runs

Major runs:

| Start | End | Samples | Min Mbps |
| --- | --- | ---: | ---: |
| `14:07:20` | `14:11:46` | `7` | `5.4837` |
| `14:24:16` | `14:28:39` | `7` | `0.9600` |
| `14:40:43` | `14:45:15` | `7` | `1.5393` |
| `14:51:54` | `14:56:18` | `7` | `3.3481` |
| `15:03:04` | `15:15:56` | `18` | `6.6710` |

This is not one bad measurement.

It is repeated multi-minute degradation.

### awg3 Drops

`awg3` last-100 average:

`35.5251 Mbps`

Drop threshold:

`15.9863 Mbps`

Detected:

- `25` drop samples
- `4` drop runs

Major runs:

| Start | End | Samples | Min Mbps |
| --- | --- | ---: | ---: |
| `14:12:31` | `14:17:41` | `8` | `14.7042` |
| `14:24:16` | `14:28:39` | `7` | `3.3781` |
| `14:51:54` | `14:56:18` | `7` | `15.0912` |
| `15:14:28` | `15:15:56` | `3` | `4.6354` |

### Pattern

The drops are burst-like.

They are not random isolated single samples.

They are also not total failures, because every listed sample still returned code `200`.

Evidence:

- `TRANSPORT1_EVIDENCE/analysis/drop_detection.json`

## 4. Correlation Analysis

### Service Correlation

Telegram and service probes stay healthy for `awg0` and `awg3`.

Recent Telegram sentinel evidence:

- `awg0`: OK, score `100`, critical OK
- `awg3`: OK, score `100`, critical OK

Current service matrix also keeps both channels service-reachable.

This proves the failure is not:

- Telegram down
- Google down
- HTTP code `000`
- service matrix hard failure

### Interface Counters

Read-only `ip -s link` showed:

| Interface | RX errors | RX dropped | TX errors | TX dropped |
| --- | ---: | ---: | ---: | ---: |
| `awg0` | `0` | `0` | `0` | `28867` |
| `awg3` | `0` | `0` | `0` | `109919` |
| `tun0` | `0` | `0` | `0` | `357828` |

These are cumulative counters, so they do not alone prove the exact minute of collapse.

But they support that the AWG interfaces have seen transmit-side pressure/drops.

### Server Load

Read-only server snapshot:

```text
load average: 2.05, 2.37, 2.32
vmstat showed short high CPU samples
memory available: ~2355 MB
```

Local CPU pressure may contribute to measurement noise, but it does not explain the full pattern by itself:

- `vless` remains stable in the same window
- reserved WireGuard remains stable in the same window
- `awg0` and `awg3` share the same AWG endpoint

### Shared Endpoint

Read-only config fields:

```text
awg0 Endpoint = 194.124.210.244:34403
awg3 Endpoint = 194.124.210.244:34403
```

This is the strongest transport-level correlation.

Both unstable channels share the same remote AWG endpoint.

Evidence:

- `TRANSPORT1_EVIDENCE/raw_capture/transport_runtime_readonly.txt`
- `TRANSPORT1_EVIDENCE/raw_capture/server_load_readonly.txt`
- `TRANSPORT1_EVIDENCE/raw_capture/awg_public_config_fields.txt`
- `TRANSPORT1_EVIDENCE/raw_capture/production_state/service-matrix.json`

## 5. Channel Comparison

### Why vless Survives

`vless` has a stable speed floor:

```text
avg = 44.5761 Mbps
floor = 26.7038 Mbps
stability = 0.5991
```

Its last-30 window has:

- no sample below `10 Mbps`
- no code `000`
- no deep floor collapse

### Why awg0 Fails

`awg0` has:

```text
avg = 18.0308 Mbps
floor = 3.3481 Mbps
stability = 0.1857
```

It has:

- `22 / 30` samples below `10 Mbps`
- repeated multi-minute drop runs
- code `200`, meaning the channel answers but too slowly

### Why awg3 Fails

`awg3` has:

```text
avg = 26.3843 Mbps
floor = 4.6354 Mbps
stability = 0.1757
```

It has:

- a good high end near `54.9401 Mbps`
- a fresh low-end collapse to `4.6354 Mbps`
- code `200`, so it is reachable but unstable

### Reserved WireGuard Comparison

Reserved WireGuard in the same stability state:

```text
avg = 55.3763 Mbps
floor = 47.32 Mbps
stability = 0.8545
```

This strongly argues against a general V7 server-wide measurement failure.

## 6. Root Cause

Root cause classification:

`REMOTE_ENDPOINT_INSTABILITY`

Precise cause proven by available evidence:

`shared_amneziawg_endpoint_or_path_instability`

Full chain:

1. `awg0` and `awg3` are enabled AmneziaWG channels.
2. Both use the same endpoint: `194.124.210.244:34403`.
3. Both return code `200` in speed samples.
4. Both pass Telegram/service reachability.
5. Both show repeated burst-like speed collapses.
6. `vless` and reserved WireGuard survive the same window.
7. The planner rejects `awg0` and `awg3` because the speed floor is too low relative to average.

What is not proven:

- planner bug
- policy bug
- stability floor bug
- Telegram outage
- full local server outage
- pure measurement artifact

What remains not separable from this read-only evidence:

- exact remote endpoint CPU/load
- provider throttling on the remote endpoint
- path-level congestion between V7 and `194.124.210.244`
- AmneziaWG implementation-specific behavior under this endpoint

So the honest conclusion is:

The physical failure is proven to the shared AWG endpoint/path level.

Endpoint-side access would be needed to split remote host load from network path throttling.

Evidence:

- `TRANSPORT1_EVIDENCE/analysis/final_root_cause_classification.json`

## 7. Recovery Forecast

If nothing changes and future samples stay at the current low-stability regime:

`awg0` and `awg3` should not be expected to recover safely.

Recovery requires new healthy samples with a higher speed floor.

### awg0

Current quality summary:

| Window | Current stability |
| --- | ---: |
| `5m` | `0.1223` |
| `1h` | `0.1324` |
| `24h` | `0.2210` |
| `7d` | `0.3107` |

Samples needed for `1h` to cross `0.45`:

| Future sample stability | Samples needed |
| ---: | ---: |
| `0.50` | `11` |
| `0.70` | `5` |
| `0.90` | `3` |

### awg3

Current quality summary:

| Window | Current stability |
| --- | ---: |
| `5m` | `0.4753` |
| `1h` | `0.3930` |
| `24h` | `0.2927` |
| `7d` | `0.3451` |

Samples needed for `1h` to cross `0.45`:

| Future sample stability | Samples needed |
| ---: | ---: |
| `0.50` | `4` |
| `0.70` | `2` |
| `0.90` | `1` |

Interpretation:

`awg3` can recover faster if the fresh final drop stops.

`awg0` needs a longer clean window because its 1h/24h/7d state is worse.

Evidence:

- `TRANSPORT1_EVIDENCE/analysis/recovery_forecast.json`

## 8. Recovery Options

Do not change the stability floor yet.

Do not force `awg0` or `awg3` into BA.3 yet.

Ranked options:

1. Check the shared remote AWG endpoint `194.124.210.244:34403`.
   - endpoint CPU/load
   - provider throttling
   - network path congestion
   - AmneziaWG daemon health

2. Add or test a second AWG endpoint that does not share `194.124.210.244:34403`.
   - If the second endpoint is stable, root cause is confirmed at endpoint/path level.

3. Run a read-only 30-60 minute observation window.
   - collect raw speed samples
   - collect interface counters before/after
   - collect server load before/after
   - compare `vless`, `awg0`, `awg3`, reserved WireGuard

4. Keep BA.3 blocked until at least two eligible production channels have stable throughput floors.

5. If endpoint cannot recover, replace the AWG endpoint instead of lowering the floor.

## 9. Final Verdict

Final verdict:

```text
raw_history_captured=true
last_30_samples_shown=true
last_50_samples_captured=true
last_100_samples_captured=true
variance_analysis_complete=true
drop_detection_complete=true
latency_failure_correlation_complete=true
channel_comparison_complete=true
root_cause_classification=REMOTE_ENDPOINT_INSTABILITY
root_cause_precise=shared_amneziawg_endpoint_or_path_instability
measurement_artifact_proven=false
local_server_load_primary_cause=false
service_failure_primary_cause=false
planner_bug=false
policy_bug=false
safe_for_ba3_now=false
runtime_changed=false
routing_changed=false
policy_changed=false
autonomy_changed=false
deploy_run=false
```

Direct answer:

`awg0` and `awg3` lose stability because their shared AWG endpoint/path produces bursty speed collapses while still returning successful service responses.

The channels are not dead.

They are not service-blocked.

They are currently not stable enough for BA.3.

Safe next step:

```text
AWG_ENDPOINT_RECOVERY_OR_REPLACEMENT_REVIEW
```

Goal of next step:

Either recover `194.124.210.244:34403` or introduce a second independent stable AWG endpoint, then rerun BA.3 candidate pool.
