# V7 runtime profile handoff binding trace — 2026-08-30

## Purpose

The latest live evidence contains several simultaneously failed sources.  An
existing health child confirms profile failures and starts a source-bound
Matrix consumer, but its compact summary can be overwritten by a parallel
background Matrix receipt before inspection.

## Added diagnostic

The existing Matrix summary now records only the current binding decision for
a runtime profile handoff:

- whether the health-owned source binding was exact;
- source and current incident identity;
- affected-scope count; and
- whether the historical passive consumer was deferred.

This is diagnostic output from the existing Matrix owner.  It is not a new
registry, planner, queue, source of truth, or route action.

## Verification

- Python compilation: PASS.
- Focused fresh-profile passive-deferral test: PASS.
- Diff whitespace validation: PASS.

## Next evidence

On the next normal V7 profile-failure call, inspect this binding together with
the live operation receipt.  It will distinguish an exact source binding from
an upstream event/incident-materialisation gap before any further repair.
