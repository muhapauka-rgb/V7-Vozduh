# V7 Phase 4 Service-Aware And Route-Class-Aware Switching

## Purpose

Not every service degradation is a full platform outage. Autoswitch must understand which route class and which service are affected before planning movement.

## Route Classes

Autoswitch must respect the authoritative route classes:

- GLOBAL_FAST;
- GLOBAL_STABLE;
- DIRECT_RU;
- TRUSTED_RU_SENSITIVE.

## Service Scope

Service-aware switching separates:

- Telegram-specific degradation;
- general HTTPS/DNS degradation;
- media/service-specific degradation;
- direct routing degradation;
- trusted RU degradation;
- egress-wide outage.

## Decision Rules

GLOBAL_FAST:

- optimize for usable performance but avoid latency chasing;
- movement requires clear stability or usability gain.

GLOBAL_STABLE:

- prioritize reliability over speed;
- movement requires verified stable target and persistence.

DIRECT_RU:

- direct routing is a controlled exception;
- direct issues must not cause unsafe global fallback.

TRUSTED_RU_SENSITIVE:

- trusted RU unavailable means degraded or blocked state;
- it must not silently fall back to unsafe routing.

## Candidate Eligibility

A target egress is eligible only when:

- route-class policy allows it;
- organization policy allows it;
- service-specific checks are acceptable;
- route verification is compatible;
- target is not quarantined, disabled, overloaded, or in maintenance;
- kill switch safety is preserved.

## Explainability

Autoswitch must explain whether a move is caused by:

- service-specific degradation;
- egress-wide degradation;
- route-class safety issue;
- client instability;
- maintenance/drain;
- operator policy.

