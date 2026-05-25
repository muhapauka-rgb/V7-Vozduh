# V7 Phase 3 - Trusted RU Observability

## Purpose

Trusted RU is safety-sensitive. Degradation must be visible and must not silently fallback to unsafe routing.

## Required States

Show:

- available;
- unavailable;
- degraded;
- policy blocked;
- unsafe fallback prevented;
- route mismatch;
- service denial risk;
- unknown.

## Required Evidence

Evidence should include:

- policy/domain class;
- selected path;
- direct/RU diagnostics;
- DNS path;
- route table;
- service matrix where applicable;
- last verification timestamp.

## Operator Summary

Default:

- trusted RU status;
- blocker/warning;
- affected route classes/domains;
- safe suggested action.

Drill-down:

- domain samples;
- direct table/mark state;
- DNS capture state;
- route-class candidates.

## Safety Rule

If trusted RU is unavailable and no policy-safe fallback exists, the correct state is blocked/degraded, not healthy.
