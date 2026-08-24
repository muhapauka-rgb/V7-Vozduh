# Frozen HARD_PATH SLO series: convergence blocked

Date: 2026-08-24 21:05 MSK  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Mission: `V7_V5_3_N10_CONVERGENCE_AND_PROGRAM_COMPLETION_FROM_INTERRUPTED_STATE`  
Architecture: `V5.3 N0–N11 ROLE-BASED FAST RECOVERY ARCHITECTURE`  
Implementation fingerprint: `80d7d9c4b00bd520b3670ca76e66019978e8b7f5a76d68b775621148feabff98`

## TERMINAL

`HARD_PATH_SLO_CONVERGENCE_BLOCKED`

The implementation remained frozen. No code, configuration, cadence,
priority, verifier, Authority, Planner, Matrix or systemd change was made.

## SERIES ACCEPTANCE

- valid samples: **5**;
- invalid samples retained without SLO credit: **1**;
- cold valid: **1**;
- warm valid: **4**;
- distinct owner-backed Matrix generations: **5**;
- ordinary-user effect: **0**;
- health Runtime: active;
- Full Matrix, Telegram and autoswitch timers: inactive as intended;
- all valid samples completed the existing Candidate→Packet→Lease→Barrier→
  Apply→route/kernel→required-service S11 chain.

Nearest-rank P95 for five valid samples is the slowest valid sample:

`P95 = 4043.267 ms > 3000 ms`

Every valid sample remained below 5 seconds, but the P95 requirement failed.

## COMPLETE SAMPLE DISTRIBUTION

`onset→S11` is the owner’s `control_plane_and_kernel_path_cutover_latency_ms`;
the receipt confirms exact route/kernel visibility and required-service
verification. `T0` is the canonical `confirmed_hard_failure` event; its
separate detection interval is recorded as zero by the current owner.

| # | Kind | Valid | Matrix generation | onset→T0 | T0→decision | decision→Apply admission | Apply→assignment | assignment→kernel | kernel→route/service/S11 | onset→S11 |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | cold | yes | `ctm0fgen_1d934e94790e3d397c6ed4b6` | 0.000 | 1963.596 | 28.307 | 434.188 | 29.794 | 435.927 | **2891.812** |
| 2 | warm | no | `ctm0fgen_a36dad245badf29776d5aa69` | 0.000 | 7181.931 | 46.678 | 497.573 | 21.873 | 457.990 | **8206.045** |
| 3 | warm | yes | `ctm0fgen_52b54d4d9b2d4bcbc16611ca` | 0.000 | 1957.341 | 34.245 | 365.874 | 17.545 | 378.661 | **2753.666** |
| 4 | warm | yes | `ctm0fgen_e56393c3c055f42002036ebd` | 0.000 | 2058.220 | 36.863 | 357.088 | 20.079 | 415.262 | **2887.513** |
| 5 | warm | yes | `ctm0fgen_c3ea38eb244cbf5e7cf65152` | 0.000 | 3188.182 | 38.738 | 398.082 | 17.298 | 400.969 | **4043.267** |
| 6 | warm | yes | `ctm0fgen_58e76a7e848a60ecff664d87` | 0.000 | 2307.710 | 36.948 | 360.922 | 25.094 | 441.616 | **3172.290** |

The invalid sample’s reason was
`authoritative_cutover_sample_above_5000ms`; it remains visible and receives
no SLO credit.

## MONOTONIC EVENT RECEIPTS

For every sample, the existing receipt recorded these monotonic boundaries:

- `CONTROLLED_FAILURE_ONSET = FIRST_FAILED_OBSERVATION = T0_MATRIX_CONFIRMED`
  (`failure_detection_latency_ms = 0`);
- `TARGET_DECISION_BOUND`;
- `APPLY_ADMITTED`;
- `ASSIGNMENT_COMMITTED`;
- `KERNEL_PATH_VISIBLE`;
- `ROUTE_TARGET_IDENTITY_VERIFIED = REQUIRED_SERVICE_VERIFIED = S11` in the
  combined route-bound payload receipt.

Candidate creation, Packet creation and Lease acquisition have durable IDs for
every sample, but the current owner does not emit separate monotonic timestamps
for those three creation events. Their receipt IDs are retained in the audit;
no timestamps were fabricated. The same owner also does not emit a separate
monotonic boundary between route identity and required service: both are proven
by the single target-payload receipt.

The first valid sample IDs were:

`reservation=ctm0fsample_374d6dcad862eb54978b71b9`,
`operation=govexec_2000d6cee4c1adc29f303731`,
`packet=pkt_6f534cf6eca6f178fbe487dc`,
`lease=execlease_7428a22e6fab0faf05aaacb6`.

The last valid sample IDs were:

`reservation=ctm0fsample_2eb3190695c73d8608195990`,
`operation=govexec_f07e7f29a6c8287095cff0b1`,
`packet=pkt_56e07c777fa843602f4153a2`,
`lease=execlease_538f0d2a4eb859027d3042a4`.

Raw monotonic nanosecond boundaries emitted by the owner (the route/service
and S11 columns intentionally share one combined target-payload receipt):

| Sample | onset = first failed = T0 | decision | Apply | assignment | kernel visible | route = service = S11 |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 9520095506332536 | 9520097469928622 | 9520097498235908 | 9520097932423516 | 9520097962217764 | 9520098398144864 |
| 2 | 9521498277555508 | 9521505459486100 | 9521505506164396 | 9521506003737292 | 9521506025610760 | 9521506483600674 |
| 3 | 9521694039222360 | 9521695996563288 | 9521696030808058 | 9521696396682350 | 9521696414227576 | 9521696792888406 |
| 4 | 9521862840973396 | 9521864899192980 | 9521864936056420 | 9521865293144314 | 9521865313223548 | 9521865728485910 |
| 5 | 9521999693513104 | 9522002881694650 | 9522002920432372 | 9522003318513914 | 9522003335811636 | 9522003736780264 |
| 6 | 9522138143146078 | 9522140450856246 | 9522140487804324 | 9522140848726436 | 9522140873819992 | 9522141315435868 |

The current audit schema has no monotonic fields for Candidate-created,
Packet-created or Lease-acquired; only their durable IDs and wall-clock
creation receipts are available. This is recorded as an instrumentation
limitation rather than silently replaced with wall time.

## CPU / LOAD CONTEXT

The current execution owner does not persist per-sample CPU, RSS or load
snapshots. Therefore per-sample load attribution is **unknown**, not inferred.
The final read-only substrate snapshot was load average `6.60 / 6.96 / 6.20`
and `v7-health` was about 2.5% CPU at that instant; this is contextual only and
is not retroactively assigned to any sample. The owner’s own ledger also marks
network-probe count, lock count, process count and serialized bytes as
`UNKNOWN`.

## DOMINANT RESIDUAL

The residual is not route visibility or required-service verification:

- post-decision assignment→service path stayed approximately `0.74–0.92 s`;
- `T0→decision` ranged from `1.957 s` to `3.188 s` for valid samples and
  reached `7.182 s` in the invalid sample;
- the slow valid sample (4.043 s) is dominated by that decision interval.

This is a measured decision/Planner admission variance, not evidence that S11
semantics are unsafe. The current receipts cannot separate deterministic
Planner work from substrate contention because CPU/load context was not
captured per sample. The deterministic post-decision path is bounded; the
remaining variance is concentrated before Apply.

## SAFETY / PRODUCTION EFFECT

- `v7-health.service` remained active throughout.
- No timer was enabled, no cadence or priority changed.
- Source/target were selected by the existing Planner; no manual target
  substitution was used.
- Only certification identity `10.7.0.92` was used; it ended on the baseline
  `awg0` after controlled cleanup.
- No ordinary user or ordinary route changed.
- No Authority expansion, duplicate Candidate, stale Apply or altered S11
  verifier semantics occurred.

## SMALLEST REMAINING ARCHITECTURAL CHOICE

Do not apply another micro-optimization automatically. The smallest remaining
choice is whether to introduce, through existing owners and with the same
freshness/invalidation laws, a precomputed decision/target-admission handoff so
the synchronous `T0→decision` work is no longer paid after failure, or to accept
the current 2-vCPU/substrate decision-path limit and revise the SLO/architecture
by owner decision. Any future change must be a separately admitted bounded
architecture decision; this terminal does not authorize a patch.

## EXACT NEXT FRONTIER

`TELEGRAM_CRITICAL` governed S11 proof, followed by the separate N10 contract
(`controlled → ordinary-like → small cohort → bounded production`). N10 is not
complete from this blocked HARD_PATH series.
