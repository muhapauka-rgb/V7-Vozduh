# V7 Recovery Latency SLO — Live Measurement and Next P0/P1 Repair

**Mission:** `V7_RECOVERY_LATENCY_SLO_LIVE_MEASUREMENT_AND_NEXT_P0_P1_REPAIR`  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
**Date:** 2026-09-03

## Current frontier and provenance

CPS projects `RECOVERY_LATENCY_SLO=ACTIVE`,
`PROGRAM_GLOBAL_STOP=NONE`, and the existing normal-Runtime-only execution
law.  The formal closure audit records
`RECOVERY_CHAIN_SIMPLIFICATION=CONSUMED`; it is not reopened here.

GitHub and local `Updatesystem` are aligned at documentation commit
`de17cbad7c80ada1f0779460705d9f392c7d3ea8`.  The latest semantic Runtime
deployment is `f4322cbd362a02f79f9d505821a014fb5b58d11d` through
`deploy-z8-14-Updatesystem-f4322cb-20260903T121009`.  Runtime hashes confirm
the deployed health-loop, `v7-egress-diagnose`, Matrix writer and autoswitch
binaries; `v7-health.service` is active.

## Current measurement

The current healthy detector receipt is `1.705 s` total:

- contract build: `174 ms`;
- network probe wall: `1277 ms`;
- postprocess: `253 ms`;
- six current profile contracts on three sources;
- zero receiver/Matrix confirmation invocations.

The current healthy series is ordinarily about `2.1–3.0 s`, but the same
fingerprint has intermittent detector outliers of `7.826`, `8.285`, `9.234`
and `10.118 s`, producing `PREVIOUS_INVOCATION_RUNNING`.  At the exact live
sampling boundary a Telegram sentinel consumed material CPU on the two-vCPU
host, but the available receipts do not prove causal overlap for every
outlier.  This is a measured **unattributed detector-contention P1**, not yet
an admitted code cause.

## First fresh ordinary Runtime receipt

At `2026-09-03T11:21Z`, the normal V7 health caller detected fresh
profile-required failures and entered the existing governed chain without any
manual user, target, Candidate, Packet, Lease, Barrier or route operation.

| Source | Ordinary users moved | T0 -> consumer start | Consumer wall | Governed Apply/verify | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| `1` | 3 | 331 ms | 14.885 s | 6.221 s | automatic completed |
| `vless` | 1 | 368 ms | 12.141 s | 4.654 s | automatic completed |
| `1` (new binding) | 1 | 118 ms | 12.237 s | 4.101 s | automatic completed |

All three receipts carry `V7_HEALTH_RUNTIME` provenance and
`ACTION_COMPLETED`; the final one is ordinary-production-only.  The Runtime
therefore has a real caller-to-governed proof, but the SLO is **not met**:
`T0 -> consumer completion` is greater than 8 seconds for every sample.

The detector did not dominate these attempts: health handed Matrix the
current binding in 118--368 ms.  The measured dominant owned interval is
`apply_and_verification` (4.101--6.221 s), including route-writer subprocess,
route visibility and required-service verification.  A further roughly
7-second gap remains between the Matrix delegated-executor wall time and the
child's currently projected governed timeline.  That gap is not yet split by
an existing timing receipt, so it is an **unattributed executor-envelope P0**
rather than a safe optimisation target.

No code or policy has been changed from this observation alone.  The next
bounded action is to extend the existing Matrix-to-governed executor timing
receipt so the outer subprocess/envelope interval is measured on the next
normal V7-originated event; only then can a smallest existing-owner repair be
admitted.  The target remains P95 <= 7 s and max <= 8 s; no SLO credit is
claimed from this three-event evidence.
