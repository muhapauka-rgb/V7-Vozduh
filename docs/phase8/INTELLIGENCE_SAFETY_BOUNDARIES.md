# V7 Phase 8 Intelligence Safety Boundaries

## Purpose

Phase 8 intelligence improves reliability and operator clarity. It does not replace the deterministic routing core.

## Intelligence May

- recommend;
- score;
- forecast;
- explain;
- prioritize diagnostics;
- suggest quarantine;
- suggest maintenance;
- suggest stealth escalation;
- suggest route-class-aware investigation.

## Intelligence Must Never

- silently reroute users;
- bypass policy;
- override route classes;
- disable kill switch;
- ignore kill switch state;
- enable unverified egress;
- remove quarantine;
- mass-migrate users;
- change stealth mode without bounded policy;
- hide reasons from the operator.

## Deterministic Core Rule

Policy remains authoritative.

Route classes remain authoritative.

Kill switch remains mandatory.

Autoswitch remains bounded, audited, explainable, and reversible.

## Confidence Rule

No recommendation is valid without:

- confidence;
- explanation;
- evidence;
- safety bounds;
- next safe action.

