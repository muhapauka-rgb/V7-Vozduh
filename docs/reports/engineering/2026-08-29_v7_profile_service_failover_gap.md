# V7 Profile-Service Failover Gap

**Date:** 2026-08-29  
**Scope:** Read-only reconciliation of an ordinary user's required-service
failure against the current Matrix, Planner and governed recovery path.

## Current fact

The affected ordinary profile requires `instagram` and `telegram` and is
assigned to `awg3`. The latest Matrix record confirms a persistent Instagram
failure on that source. The Telegram observation and all candidate observations
needed for an exact target decision are stale, so a route action must not use
them.

## Root cause

There are two independent gaps.

1. The current ordinary service-failure apply gate requires a *whole-channel*
   confirmed failure even when an exact profile-required service has a fresh,
   persistent Matrix failure. This contradicts the product rule: a user whose
   required service is unavailable must be recoverable even if unrelated
   services on the same channel still work.
2. The Matrix state is stale. `v7-health.service` is active, but its
   background required-service and target-readiness child work is repeatedly
   still running at the next due time. Therefore the Planner has no fresh,
   owner-admitted target and correctly stops rather than moving a user using
   hours-old evidence.

The existing consumer recorded the current incident as
`STOP_SAFE_CURRENT_INCIDENT_NOT_ACTIONABLE`: no owner-backed actionable target
was available. No client was moved during this reconciliation.

## Required correction

Retain Matrix as the health owner and `v7-user-switch` as the sole route
writer. Admit an ordinary recovery when all conditions hold:

- an exact profile-required service has a fresh, persistent Matrix failure;
- the source assignment is still current;
- the Planner finds a distinct target with fresh proof for every required
  service;
- the existing Candidate, Packet, Lease, Barrier and S11 verification pass.

Do not require unrelated services on the source to fail. Restore bounded
Matrix target-readiness completion so stale evidence cannot suppress this
ordinary recovery path.
