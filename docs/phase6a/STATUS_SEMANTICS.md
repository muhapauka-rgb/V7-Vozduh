# V7 Phase 6A Status Semantics

## Purpose

Statuses must be consistent across overview, channels, routing, diagnostics, and identity.

## Canonical Statuses

healthy:

- system or object is operating as expected;
- no operator action required.

degraded:

- service is usable but quality or policy confidence is reduced;
- operator should inspect grouped details.

unstable:

- repeated degradation or oscillation risk exists;
- autoswitch and maintenance decisions should be cautious.

blocked:

- traffic, service, route class, or lifecycle path cannot continue safely;
- operator action or explicit policy is required.

quarantined:

- object is intentionally isolated from production impact;
- no user routing eligibility.

maintenance:

- operator-controlled temporary state;
- drain/rollback context should be visible.

recovering:

- object improved but still inside verification window;
- avoid immediate reverse switching.

unknown:

- evidence is missing, stale, or corrupt;
- run safe diagnostics before action.

## Visual Rule

Use restrained semantic tones. The same status must look and read the same across all pages.

