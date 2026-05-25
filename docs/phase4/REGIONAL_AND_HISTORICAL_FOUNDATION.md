# V7 Phase 4 Regional And Historical Reliability Foundation

## Purpose

Autoswitch should learn from bounded historical summaries, not from opaque black-box routing.

## Historical Signals

Allowed historical signals:

- degradation frequency;
- quarantine history;
- switch success/failure history;
- maintenance frequency;
- reconnect instability;
- route-class survivability;
- service-specific failures;
- transport restart frequency.

## Regional And Operator Scope

Future regional awareness may track:

- country-specific service degradation;
- operator-specific failures;
- transport sensitivity;
- trusted RU availability;
- service survivability by region.

## Current Phase Boundary

Phase 4 prepares the model only. It must not introduce:

- distributed intelligence;
- AI routing;
- uncontrolled regional experiments;
- production-wide hidden behavior.

## Scoring Principle

Historical reliability is a modifier, not an override.

A historically stable egress still must pass current route verification and policy gates. A historically weak egress may be eligible only when current evidence and safety checks support it.

