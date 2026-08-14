# V7 Hot-Path Event Ledger Bounding — Execution Report

**Mission:** `V7_HOT_PATH_EVENT_LEDGER_BOUNDING_V1`  
**Status:** `IMPLEMENTED_AND_DEPLOYED; ROOT_BOTTLENECK_NOT_CLOSED`  
**Commit:** `497b4e06` · **Deploy:** `deploy-z8-14-Updatesystem-497b4e0-20260814T185337`

## Goal and scope

Remove one proven history-amplification defect from the existing event-only
Matrix consumer: `current_failed_source_scope()` previously read the entire
append-only failure ledger and only then selected its final 2,000 rows.

Only `tools/v7-service-matrix-refresh-all` and its exact unit assertion changed.
No service, timer, owner, queue, state schema, Packet, lease, restore barrier,
routing, CPS or Authority contract changed.

## Change

`current_failed_source_scope()` now reuses the already deployed bounded JSONL
reader from `admin_core.intelligence_workers`:

| Property | Before | After |
| --- | --- | --- |
| Logical event window | last 2,000 rows | last 2,000 rows |
| Physical read | whole ledger | at most 16 MiB tail |
| Current production ledger | 92 MiB / 38,462 rows | bounded input |
| New owner/store/component | none | none |

The static scope semantics are unchanged: latest `SERVICE_FAILURE_OBSERVED` or
`SERVICE_FAILURE_REVALIDATED` rows determine ordinary active scope and
certification-only scope.  The test expectation was aligned with two scope
fields (`scope_classification`, `controlled_certification_scope_count`) that
were already emitted before this Mission.

## Validation

- Source compilation: PASS (bytecode-cache writes deliberately disabled).
- `tests.unit.test_operator_induced_passive_capture`: 4/4 PASS.
- Existing `tests.unit.test_v7_sync_tools` checks reached the relevant planner,
  deployment and hot-path assertions without a regression; unrelated test-run
  execution exceeded the interactive observation window and was not treated as
  a passing full-suite claim.
- Safe deploy allowlist: PASS.
- Production deployed hash equals local hash:
  `c85117f80889656d6b1d74a931395861792fa7b7588953107dddd0d11aaf67e1`.
- Safe-deploy truth gate: PASS; GitHub alignment: PASS.

## Before / after production evidence

Before deployment, `v7-autoswitch-planner.service` repeatedly consumed
70.398–91.417 seconds wall time and 48.212–54.244 seconds CPU, with
approximately 546–552 MiB peak memory.  The same unit was occupied by
certification-only reconciliation while `active=false` for ordinary users.

After deployment, the new source was confirmed installed.  A subsequent
existing planner invocation remained active beyond the available observation
window.  This does **not** invalidate the bounded ledger read; it proves that
the dominant remaining cost is elsewhere and must not be hidden by claiming a
full end-to-end speedup.

## Residue and safety

| Check | Result |
| --- | --- |
| Old full `read_text(...).splitlines()[-2000:]` in this scope path | removed |
| Canonical Matrix event owner | retained |
| Ordinary active scope | retained and still blocks any unsafe shortcut |
| Certification-only open incident | retained; no bypass introduced |
| Packet / lease / barrier / apply / verification | unchanged |
| Runtime / Production / Authority effect | bounded reader deployed / no route action / NONE |

## Root-cause frontier

The next bottleneck is not an Admin wrapper and not the fast sentinel.  The
production current state has grown to approximately:

| Existing artifact | Size | Records / entries |
| --- | ---: | ---: |
| `service-failure-events.jsonl` | 92 MiB | 38,462 |
| `execution-events.jsonl` | 41 MiB | 24,354 |
| `closure-records.jsonl` | 29 MiB | 13,153 |
| `l3-runtime-state.json` | 26 MiB | 1,169 incidents; 37,565 consumption entries |

The currently open certification-only incident has zero ordinary affected users
but an owner-backed unresolved certification scope.  It prevents deleting or
blindly skipping reconciliation.  The next bounded Mission must therefore
build a compact current-state projection through the existing L3/closure owner,
prove exact re-entry for changed incident semantics, and move only completed
history out of the synchronous consumer.  It must not alter the governed
forward path.

## Programmatic delta

| Metric | Delta |
| --- | ---: |
| Runtime source files changed | 1 |
| Test files changed | 1 |
| Source LOC added / removed | 14 / 11 |
| Files deleted | 0 |
| Services/timers changed | 0 |
| Routing/Authority/CPS edges changed | 0 |

## Next frontier

`V7_HOT_PATH_CURRENT_STATE_COMPACTION_ADMISSION_V1` — read-only admission for
an existing-owner compact L3/closure projection.  Required proof: every open
incident retains owner, successor and re-entry before any completed history is
excluded from the synchronous event consumer.
