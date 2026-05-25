# V7 Phase 1 - Operator Visibility Foundation

## Purpose

Operator visibility must reduce chaos. It must not become a giant dashboard or raw telemetry wall.

Phase 1 visibility should explain routing safety, mismatch, and impact in calm, grouped language.

## Information Order

Operator surfaces should follow this order:

1. overall platform routing state;
2. safety blockers;
3. impacted users or egresses;
4. grouped cause;
5. suggested bounded action;
6. drill-down diagnostics.

Raw metrics come last, not first.

## Summary Cards

Good summary examples:

- `Routing safe: verified`
- `1 kill switch blocker`
- `2 users assigned to degraded egress`
- `Trusted RU degraded: no safe fallback`
- `Autoswitch paused by safety bound`

Bad summary examples:

- 300 raw latency values;
- full nftables dump on homepage;
- every route table row without grouping;
- blinking critical counters without explanation.

## Diagnostic Groups

Use groups:

- kill switch;
- route assignment;
- direct/RU;
- egress health;
- service matrix;
- autoswitch safety;
- contract validation;
- audit/recent repair.

Each group should have:

- status;
- impact;
- reason;
- recommended action;
- timestamp.

## Progressive Disclosure

Default view:

- compressed status;
- only active blockers/warnings;
- clear next step.

Drill-down:

- exact mismatch category;
- affected file/interface/rule;
- command output excerpt;
- before/after when repair has occurred.

## Operator Trust Rules

The UI must distinguish:

- desired state;
- observed state;
- runtime state;
- verified effective state;
- stale state;
- unknown state.

Unknown must not be presented as healthy.

## Phase 1 Boundary

This is an information architecture foundation. It does not require frontend redesign in Phase 1.
