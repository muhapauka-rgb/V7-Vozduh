# V7 Hot-Path Legacy Scope Resolution Gate Report

**Mission:** `V7_HOT_PATH_LEGACY_SCOPE_RESOLUTION_GATE_V1`  
**Mode:** bounded read-only existing-owner analysis  
**Verdict:** `STOP_SAFE_MISSING_HISTORICAL_COHORT_DISPOSITION`

## Current facts

The existing L3 incident owner and `users.registry` owner were compared without
writing either artifact.

| Fact | Result |
| --- | ---: |
| Open passive incidents | 27 |
| Channel represented by all open records | `vless` |
| Current enabled users on that source | 11 |
| Current certification users on that source | 11 |
| Open scope status `INCIDENT_SCOPE_ACCOUNTING_BROKEN` | 27 / 27 |
| Records lacking a reconstructible baseline count | 20 |
| Records with baseline counts 15 / 24 / 34 | 1 / 3 / 3 |
| Records with a baseline event pointer and unresolved fingerprint | 27 / 27 |

## Why existing reconciliation correctly refuses closure

The existing `reconcile_service_failure_execution_outcomes()` owner already
has a narrow legacy rule: it can mark a legacy unpartitioned cohort as
`CERTIFICATION_ONLY` only when the present all-certification live cohort plus
already packet-protected members exactly equals the immutable baseline.

That equality is not present for baselines 15, 24 and 34 versus the current
cohort of 11. For 20 records the baseline denominator itself is unavailable.
The missing members may have been safely moved, recovered, explicitly
excluded, disabled, or may require a still-valid protection intent. Current
route state alone cannot distinguish these histories.

Consequently, loosening the equality rule, overwriting the legacy scope, or
treating missing baseline as zero would turn an evidence gap into an unsafe
closure. No such code change is admitted.

## Required owner-backed evidence

Each affected legacy record needs one existing-owner disposition:

```text
EXACT_PACKET_OR_RECOVERY_LINEAGE
| EXPLICIT_LEGACY_EXCLUSION_WITH_POINTER
| FRESH_MATRIX_GENERATION_THAT_SUPERSEDES_THE_LEGACY_INTENT
| STOP_SAFE_RETAINED_REENTRY
```

The first three may close or supersede an individual protection intent only
through the existing L3/Matrix/closure owners. The fourth preserves the current
consumer. None permits a global certification-only shortcut.

## Existing execution and closure lookup

A read-only lookup of existing `execution-events.jsonl` and
`closure-records.jsonl` was performed after this gate was opened. The live
open-record count had advanced naturally to 28; the result is unambiguous:

| Existing-evidence condition | Open incidents proven |
| --- | ---: |
| Any exact packet-bound execution feedback | 0 |
| Verified successful packet outcome | 0 |
| Recovery or expiry terminal | 0 |
| Existing closure evidence | 28 |

The closures are `STOP_SAFE_NO_ACTION`/non-executing evidence rather than an
outcome that disposes the historical cohort. Thus no existing execution or
recovery owner can close these records automatically. The only lawful current
disposition is `STOP_SAFE_RETAINED_REENTRY` until a fresh Matrix generation or
an explicit owner-backed historical cohort disposition exists.

## Hot-path consequence and next frontier

`V7_HOT_PATH_CERTIFICATION_SCOPE_ISOLATION_V1` is **not implementation-ready**.
The safe completed improvement remains bounded event reads plus L3 consumption
compaction. The next legal work is a read-only `LEGACY_COHORT_DISPOSITION`
lookup across existing packet, recovery and closure evidence, restricted to
the 27 current records and producing compact pointers only.

Runtime effects = `NONE`. Production routing effects = `NONE`. Authority
effects = `NONE`. CPS and all owner boundaries remain unchanged.
