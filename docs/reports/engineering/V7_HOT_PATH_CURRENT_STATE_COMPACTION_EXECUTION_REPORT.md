# V7 Hot-Path Current-State Compaction — Execution Report

**Mission:** `V7_HOT_PATH_CURRENT_STATE_COMPACTION_V1`  
**Program / CPS frontier:** `V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1` / unchanged — `RS6_RUNTIME_PACKAGE_MINIMIZATION` → `EXECUTE_RS6_RUNTIME_PACKAGE_MINIMIZATION`  
**Status:** `IMPLEMENTED_AND_DEPLOYED; HOT_CONSUMER_STORAGE_SHRUNK; END_TO_END_FAILOVER_LATENCY_NOT_YET_PROVEN`

## Scope and root cause

The existing passive service-failure consumer retained its exact-once
`passive_event_consumptions` history in `l3-runtime-state.json`, then loaded
the whole 92 MiB `service-failure-events.jsonl` before selecting the last
2,000 events.  It also wrote a stale in-memory L3 snapshot *after* outcome
reconciliation, allowing the old consumption index to overwrite a freshly
reconciled state.

This Mission changed only the existing `tools/v7-users-autoswitch` owner and
its unit tests.  It introduced no state schema, owner, service, timer, queue,
truth source or routing decision path.

## Change performed

| Commit | Change | Preserved contract |
| --- | --- | --- |
| `1cad98b5` | Persist existing bounded consumption compaction before outcome reconciliation. | Reconciliation receives and persists the current L3 state; exact re-entry remains owner-backed. |
| `959e1368` | Extend the existing JSONL reader with an optional bounded tail and apply it only to the passive event source (2,000 rows / 16 MiB). | Logical event window remains the newest 2,000 records; no event producer or decision owner changed. |

The VPS binary hash equals the local hash:
`006ee91995bae001bc99780128871c26ff5d4a9f1084d863e4c1db320d6a4f2a`.
The deployed source contains the bounded passive-source call.

## Validation

| Check | Result |
| --- | --- |
| Source compile without bytecode writes | PASS |
| Exact JSONL-tail window test | PASS |
| Existing passive-consumer compaction/reconciliation regression test | PASS |
| Certification-only scope remains non-actionable | PASS |
| Safe-deploy allowlist and GitHub alignment | PASS (`deploy-z8-14-Updatesystem-959e136-20260814T191943`) |
| Existing non-target broad service-failure suite | Not a completion claim: it has pre-existing CPS/frontier expectation failures, including one reproduced without this patch. |

## Before / after production evidence

The normal systemd cycle (not a manually triggered failover) consumed the
deployed code and compacted the existing L3 projection.

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| `l3-runtime-state.json` | 27,272,117 bytes | 10,427,884 bytes | -16,844,233 bytes (-61.8%) |
| `passive_event_consumptions` | 37,783 | 1,997 | -35,786 (-94.7%) |
| Passive consumer completion in observed normal cycle | 15–30 sec / occasional timeout | 15.9 sec in the first compacted cycle | bounded source and compact state now observed |
| Users moved / routing mutations | 0 | 0 | unchanged |

The subsequent planner advisory still consumes roughly one minute in normal
certification-only cycles.  That work constructs prepared decisions but emits
`execution_allowed=false`, creates no Candidate/Packet/lease, and performs no
routing mutation.  Therefore this Mission proves a real reduction of the
synchronous consumer's retained history; it does **not** prove that
`FAILURE → CLIENT MOVED` is now fast.

## Physical delta

| Metric | Delta |
| --- | ---: |
| Runtime source files changed | 1 |
| Test files changed | 1 |
| Source LOC added / removed | 39 / 4 |
| Test LOC added / removed | 58 / 0 |
| Functions added | 0 |
| Files deleted / added | 0 / 0 |
| New runtime dependency, owner, state writer or authority edge | 0 |

## Safety and effects

- **Runtime effect:** existing L3 retained-history projection is compacted.
- **Production routing effect:** `NONE` — no user move, route apply, Packet,
  lease, barrier or verification execution occurred.
- **Authority effect:** `NONE`.
- **CPS frontier:** unchanged.

## Remaining frontier

`CERTIFICATION_ONLY` currently enters the expensive advisory planner despite
there being no executable ordinary scope.  A generic fast-return is still not
admitted: open passive incidents include historical ordinary scopes and require
owner-backed re-entry classification first.

The exact next bounded read-only action is
`V7_HOT_PATH_PASSIVE_INCIDENT_REENTRY_CLASSIFICATION_V1`: classify each open
passive incident as current ordinary re-entry, current certification
reconciliation, terminal owner-backed, or stop-safe incomplete evidence.  Only
that proof can safely admit certification-scope isolation.  Packet, lease,
barrier, route apply and verification remain outside this Mission and must not
be bypassed.
