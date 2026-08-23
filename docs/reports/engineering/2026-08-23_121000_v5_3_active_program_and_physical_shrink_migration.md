# V5.3 active Program and physical-shrink migration

**Date:** 2026-08-23  
**Scope:** program-contract migration and archival separation only. No Runtime,
Matrix, route, timer, client, state or application-code mutation occurred.

## Result

The active Program is now a single 421-line V5.3 execution contract.  It
contains only the current product/SLO contract, existing owners, layer roles,
N0–N11, safety/automation laws, replacement/physical-shrink law and terminal.
The 6,113 lines of superseded V5.3 evidence plans and V1–V5.2 material were
preserved byte-for-byte in:

`docs/archive/programs/V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_HISTORY.md`

The archive is explicitly `ARCHIVED_NON_EXECUTABLE_REFERENCE`: it cannot
dispatch work, set a cadence, grant Authority, override N0–N11 or establish
live state.  A direct comparison against the pre-migration Program range
passed.

## New binding cleanup contract

N0–N11 is now explicitly a replacement migration.  For every new mechanism,
the Program requires caller/consumer discovery, consumer migration,
equivalence/safety/SLO proof, a bounded fallback window, zero-caller and
zero-current-state proof, then physical deletion of obsolete code, imports,
configuration, timers/units, compatibility layers, state projections, tests,
fixtures and active Program references.

N11 cannot close while old primary paths, duplicate owners/decision paths,
unclassified timers or runtime branches, dead code/outputs, obsolete
compatibility/state/test fixtures or old executable Program contracts remain.
It requires before/after shrink receipts; C8 and Full Matrix survive only in
their explicitly current BACKSTOP and DEEP_BACKGROUND/FALLBACK roles.

## Validation and next step

`git diff --check` passed.  The archived body exactly matches the removed
pre-migration Program content.  No source code was removed prematurely;
physical Runtime cleanup is deliberately deferred to N11 after replacement and
consumer proof.

**Exact next step:** N0a remains the first implementation residual: bound the
existing downstream executor's memory.  N1–N7/N9 may independently proceed in
Polygon.  Each admitted implementation must now supply the replacement and
shrink evidence required by N11.

