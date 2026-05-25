# V7 Phase 4 Confidence And Bounded Migration

## Purpose

Autoswitch must avoid large or uncertain movement. Confidence decides whether a plan is advisory, staged, or eligible for guarded apply.

## Confidence Levels

Low confidence:

- weak evidence;
- stale data;
- single-signal degradation;
- unclear client-vs-egress scope;
- unverified target.

Allowed result: recommend observation or diagnostics only.

Medium confidence:

- persistent degradation;
- compatible target exists;
- no hard safety blockers;
- limited affected scope.

Allowed result: small bounded plan or operator-confirmed action.

High confidence:

- multi-signal persistent degradation;
- service impact is clear;
- target route is verified;
- cooldown and freeze gates pass;
- migration scope is bounded and reversible.

Allowed result: guarded migration within configured limits.

## Bounded Migration Rules

Autoswitch must respect:

- maximum planned moves per run;
- maximum failover moves per run;
- maximum reconnect-driven moves per run;
- target load reserve;
- hard and soft load limits;
- organization policy limits;
- user cooldown;
- egress quarantine state.

## Capacity Safety

Even during degradation, alternate egress must not be overloaded. If all targets are unsafe or overloaded, autoswitch should report degraded state instead of forcing movement.

## Rollback Context

Every applied movement must preserve:

- previous assignment;
- target assignment;
- reason;
- confidence;
- verification result;
- rollback availability.

