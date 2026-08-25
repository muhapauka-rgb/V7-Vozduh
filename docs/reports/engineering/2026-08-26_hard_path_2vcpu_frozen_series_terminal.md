# HARD_PATH 3-second SLO: frozen 2-vCPU evidence terminal

**Date:** 2026-08-26  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM`  
**Terminal:** `HARD_PATH_3S_2VCPU_ARCHITECTURE_EXHAUSTED`  
**Frozen runtime fingerprint:** `4b13e1475addd1a9a94a7edbf2736e45fb72c99c86ad91be7debd39c968a0eb1`

## Scope and invariants

This is one homogeneous, certification-only series. No code, configuration, cadence, priority, verifier, Planner, Matrix, Authority or route-writer semantics changed during the five samples. The existing Matrix/Planner chose targets; no target was substituted manually. Only `10.7.0.124` participated. After every sample it was returned to the isolated source `amneziawg-exec-20260528-10-8-1-14` with table `1122` and `default dev v7execwg0`.

The completed series has one cold and four warm samples across five owner-backed Matrix generations. It has no active reservation and zero ordinary-user effect.

## Complete authoritative distribution

| Sample | Kind | Onset to S11, ms | Failure to decision, ms | Decision to Apply, ms | Assignment, ms | Kernel visible, ms | Required service, ms | Result |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `ctm0fsample_d2e3…` | cold | 5,853.852 | 3,912.458 | 297.676 | 978.446 | 86.735 | 578.537 | performance fail |
| `ctm0fsample_1f1d…` | warm | 6,759.929 | 5,454.467 | 150.033 | 650.416 | 36.737 | 468.277 | performance fail |
| `ctm0fsample_b1db…` | warm | 3,098.637 | 1,749.580 | 163.269 | 592.120 | 25.422 | 568.245 | performance fail |
| `ctm0fsample_3596…` | warm | 1,895.404 | 1,041.507 | 132.292 | 391.044 | 17.219 | 313.342 | pass |
| `ctm0fsample_b06e…` | warm | 3,820.576 | 2,452.268 | 326.140 | 607.607 | 20.943 | 413.619 | performance fail |

Sorted totals: **1,895.404; 3,098.637; 3,820.576; 5,853.852; 6,759.929 ms**. With nearest-rank P95 for five samples, the fifth value is decisive: **P95 = 6,759.929 ms**.

## Acceptance result

| Requirement | Result |
|---|---|
| At least five functionally valid samples | Pass: 5 |
| At least one cold / two warm | Pass: 1 cold, 4 warm |
| At least two Matrix generations | Pass: 5 |
| P95 onset to S11 <= 3,000 ms | **Fail: 6,759.929 ms** |
| No valid sample > 5,000 ms | **Fail: 2 samples** |
| Required route identity and service S11 preserved | Pass in all 5 |
| Ordinary-user effect | Pass: 0 |

The system's own bounded gate records the same blockers: `authoritative_cutover_max_above_5000ms` and `authoritative_cutover_p95_above_3000ms`.

## What the evidence says

The route writer, kernel visibility and required-service confirmation are not the dominant residual. Their observed maxima were respectively `978.446 ms`, `86.735 ms`, and `578.537 ms`. The variable dominant span is failure-to-decision, with P95 `5,454.467 ms`.

One warm sample proved that the existing architecture can complete at `1,895.404 ms`; it did **not** prove the 3-second contract because the other valid samples remain part of the distribution. The cold sample at `5,853.852 ms` is only about `857 ms` lower than an earlier, non-homogeneous pre-frozen observation of `6,710.852 ms`; that comparison is diagnostic only, not a causal attribution to the persistent consumer because their implementation fingerprints differ.

The per-sample cutover receipts contain complete monotonic chain timing, but not a historical CPU/load snapshot. Therefore this block does not claim a numerical CPU-causation split; it establishes the product SLO failure on the actual 2-vCPU Runtime as measured.

## Safety closure

- All five samples have a valid forward evidence and a terminal cleanup record.
- No active CT-M0F reservation remains.
- The synthetic client is back on its isolated baseline route.
- `v7-health.service` is active.
- No ordinary client moved and no ordinary route assignment changed.
- No further HARD-path micro-optimization was made or is authorized by this terminal.

## Exact next decision

Do **not** begin Telegram-critical, N10 or N11 from this result: their entry condition was a successful HARD-path SLO series. The smallest remaining architectural owner decision is whether to admit `PERSISTENT_EXISTING_OWNER_PREPARED_VALIDATION_PROCESS` for a new bounded design/evidence cycle, or change/accept the product SLO on the existing 2-vCPU substrate. No implementation of that new architecture has been started here.
