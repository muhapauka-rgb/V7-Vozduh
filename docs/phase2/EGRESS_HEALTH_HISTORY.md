# V7 Phase 2 - Egress Health History

## Purpose

Each egress needs history for reliability decisions, but UI must stay summary-first.

## History Types

Track:

- degradation history;
- switch history;
- quarantine history;
- runtime incidents;
- restart frequency;
- packet loss trends;
- reconnect instability;
- service matrix history;
- MTU/MSS warnings;
- rollback events.

## Storage Principles

History should be:

- append-only or ring-buffered;
- corruption-safe;
- compacted for UI;
- tied to egress id;
- timestamped;
- attributable when action-based.

Existing related files:

- `egress-quality-summary.json`;
- `egress-quality-ring.json`;
- `service-matrix.json`;
- `autoswitch-safety.json`;
- draft quarantine result files;
- audit logs.

## Health Summary

Default operator summary:

- health state;
- last incident;
- stability confidence;
- quarantine/maintenance status;
- suggested action.

Drill-down:

- raw samples;
- per-service results;
- restart timeline;
- switch events.

## Phase 2 Boundary

This document defines the target history model. It does not change compaction logic.
