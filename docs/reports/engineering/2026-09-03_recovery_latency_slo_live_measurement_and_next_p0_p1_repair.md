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
`d9b3fb6c`.  The latest semantic Runtime
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

No code or policy has been changed from this observation alone.  The target
remains P95 <= 7 s and max <= 8 s; no SLO credit is claimed from this
evidence.

## Second fresh ordinary Runtime receipt

At `2026-09-03T11:35Z`, while this Mission was waiting for a fresh incident,
the normal health owner itself consumed two simultaneous current source
failures.  This was not triggered, advanced, or completed by Codex.

| Source | Ordinary users moved | T0 -> consumer start | T0 -> S11/consumer completion | Dominant measured interval | Result |
| --- | ---: | ---: | ---: | --- | --- |
| `vless` | 1 | 341 ms | 21.374 s | Apply/verify 5.103 s | automatic completed |
| `1` | 3 | 110 ms | 26.820 s | Apply/verify 12.556 s | automatic completed |

The second receipt resolves the earlier uncertainty: detector entry is not
the active bottleneck.  The three-member `1` transaction performed three
serial route-writer mutations (`1.946 + 1.898 + 1.805 s`), each followed by
its own route/required-service S11 observation (`~1.1--1.2 s`).  Its full
governed Apply/verify span was `12.556 s`; the one-member `vless` Apply/verify
span was `5.103 s`.  The source/Matrix-to-consumer handoff remained fast
(`110--341 ms`).

This is valid production provenance (`V7_HEALTH_RUNTIME`,
`ACTION_COMPLETED`, `runtime_mutation_performed=true`) and proves that V7 did
automatically recover four ordinary users.  It also proves that a bounded
multi-member recovery cannot meet the product 7/8-second clock while the
current Program-mandated serial Apply/route-writer boundary remains.  That
boundary is explicitly outside this Mission's admitted scope (no new
concurrency or routing-core modernization).  It is therefore recorded as a
measured **governed-Apply/data-plane P0**, not silently treated as a detector
or advisory defect and not manually bypassed.
