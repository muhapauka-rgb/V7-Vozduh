# HARD_PATH 3-second SLO: post-projection frozen 2-vCPU terminal

**Date:** 2026-08-26  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM`  
**Terminal:** `HARD_PATH_3S_2VCPU_ARCHITECTURE_EXHAUSTED`  
**Frozen Runtime fingerprint:** `ba7161f5f0eeb959fb193b7ec94370185f686e6ba0fe7d80b695c6727a926cd3`  
**Deployed code:** `e4106fd647978adf481d78201ed10a183a130fcb`; `deploy-z8-14-Updatesystem-e4106fd-20260826T023921`

## Scope and controls

This is the homogeneous controlled proof after the bounded prepared-projection
freshness correction.  The Runtime code, configuration, cadence, priorities,
verifier, Planner, Matrix, Authority, route writer and S11 semantics did not
change during the series.  The existing Matrix/Planner selected each target;
no target was substituted manually.

Only certification identity `10.7.0.124` was used.  Every transaction went
through the existing health -> Matrix -> Candidate -> Packet -> Lease ->
Barrier -> Apply -> route/kernel -> required-service chain and terminal
cleanup.  The evidence contains five functionally valid samples: one cold,
four warm, and five distinct owner-backed Matrix generations.

## Authoritative distribution

| Sample | Kind | Matrix generation | T0 -> decision, ms | Decision -> Apply, ms | Assignment, ms | Kernel visible, ms | Required-service, ms | Onset -> S11, ms | Result |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `ctm0fsample_fb4f…` | cold | `ctm0fgen_d1bd…` | 1746.435 | 148.679 | 406.110 | 15.956 | 379.813 | 2696.992 | pass |
| `ctm0fsample_e86f…` | warm | `ctm0fgen_ebcd…` | 2208.310 | 269.044 | 1021.842 | 37.367 | 578.376 | 4114.938 | fail |
| `ctm0fsample_5bdf…` | warm | `ctm0fgen_7e98…` | 2923.247 | 348.186 | 978.415 | 53.187 | 590.109 | 4893.144 | fail |
| `ctm0fsample_8013…` | warm | `ctm0fgen_0482…` | 2454.329 | 345.159 | 1042.913 | 40.115 | 567.008 | 4449.524 | fail |
| `ctm0fsample_495f…` | warm | `ctm0fgen_dd63…` | 2776.836 | 412.055 | 1130.911 | 31.802 | 663.281 | 5014.885 | fail |

Sorted totals: **2696.992; 4114.938; 4449.524; 4893.144; 5014.885 ms**.
For five samples nearest-rank P95 is the fifth value, therefore
**P95 = 5014.885 ms**.

## Gate result

| Requirement | Result |
|---|---|
| At least five functionally valid samples | Pass: 5 |
| Cold and at least two warm | Pass: 1 cold, 4 warm |
| At least two owner-backed Matrix generations | Pass: 5 |
| P95 onset -> S11 <= 3000 ms | **Fail: 5014.885 ms** |
| No valid sample > 5000 ms | **Fail: 5014.885 ms** |
| Route identity, kernel visibility and required-service S11 | Pass in all 5 |
| Ordinary-user effect | Pass: none; certification-only identity only |

## Interpretation

The bounded correction worked: the cold sample reached 2696.992 ms and its
prepared projection was consumed in 41.150 ms.  It did not make the result
stable enough for the product contract.  The largest repeatable residual is
still the failure-to-decision interval (1746.435–2923.247 ms); the last
sample also crossed the individual 5-second ceiling.  The audit records
monotonic chain timing but not a historical CPU/load snapshot, so this report
does not claim a numerical CPU-causation split.

Every slow but functionally valid sample remains in the calculation.  No
additional micro-optimization was made after the frozen series began.

## Runtime and safety closure

- `v7-health.service` is active after the series.
- Legacy standalone Matrix and Telegram timers are inactive as intended.
- All five sample terminals have forward evidence and cleanup records; no
  certification reservation remains active.
- No ordinary client was moved or had a route/assignment changed.
- The isolated certification source was restored by the governed cleanup path.

## Exact next frontier

This terminal blocks Telegram-critical, N10 and N11: they cannot borrow SLO
credit from a failed shared HARD path.  The Program forbids another automatic
micro-optimization on this two-vCPU configuration.  The required external
owner decision is one of:

1. explicitly accept/change the current product SLO; or
2. admit a materially different control-plane architecture for a new bounded
   design and evidence cycle.

The previously accepted no-resize constraint remains in force.  No new
architecture is implemented by this report.
