# V7 Phase 3 - Incident Timeline Model

## Purpose

V7 needs one incident timeline that compresses events into operator-relevant summaries.

The timeline is not a raw log viewer.

## Event Types

Track:

- degradation;
- recovery;
- autoswitch;
- quarantine;
- route mismatch;
- MTU issue;
- trusted RU issue;
- provisioning failure;
- transport restart;
- client instability.

## Unified Event Fields

Every event should have:

- timestamp;
- category;
- severity;
- affected object;
- reason;
- suggested action;
- correlation id;
- verification state.

Recommended optional fields:

- actor;
- before state;
- after state;
- rollback context;
- evidence links;
- dedupe key.

## Deduplication

Repeated events should collapse into one incident group:

- same category;
- same affected object;
- same reason;
- time window overlap.

## Timeline View

Default:

- active incidents;
- recent recoveries;
- actions required.

Drill-down:

- raw events;
- command output;
- audit rows;
- state snapshots.

## Alert Boundary

Timeline should feed calm alerts. It must not create alert spam.
