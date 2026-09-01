# Recovery Stability — temporal Matrix-evidence boundary

Date: 2026-09-02
Mission: `V7_RECOVERY_STABILITY_HARDENING_AND_STATE_SEQUENCE_SOAK`
Block: deterministic temporal boundary

## Purpose

Prove the exact freshness boundary already consumed by the existing
profile-impacting Matrix reader.  The objective is to prevent an old failed
row from starting a recovery while ensuring a genuinely current failed source
is never hidden by timing round-off.

## Work performed

Added deterministic time-controlled tests around the existing
`live_profile_failure_evidence` owner.  No Runtime behavior was changed.

- A newly observed required-service failure is admitted at 9.999 and exactly
  10.000 seconds, and rejected at 10.001 seconds when no exact health-owner
  handoff exists.
- A re-probed continuing required-service failure is admitted at 29.999 and
  exactly 30.000 seconds, and rejected at 30.001 seconds under the same
  condition.
- The existing exact-T0 handoff and fresh continuing-incident regressions ran
  alongside the boundary checks.

## Evidence

- 5 focused deterministic tests: PASS in 0.112 seconds.
- Includes the prior 100-transition current-scope/historical-residue soak:
  PASS.
- `git diff --check`: PASS.

The fixtures patch only their local wall clock.  They do not modify the
production Matrix, health loop, Authority, Planner, Candidate, Packet, Lease,
Barrier, routes, client assignments or timers.

## Result and boundary

The existing owner now has executable proof that its two admission windows are
inclusive at their intended boundary and fail closed immediately after it.
This is a narrow temporal primitive, not the whole
`RECOVERY_TEMPORAL_BOUNDARY_SOAK_CONSUMED` terminal: remaining coverage must
exercise expiry/re-entry boundaries for actual recovery obligations and the
seeded randomized state-sequence lane.  Ordinary live-path credit remains
separate and requires the normal V7 Runtime as origin.

## Simplification assessment

The work adds tests only.  It reuses the existing Matrix evidence reader and
does not add a Runtime branch, owner, state projection, retry loop or route
writer.  Runtime structural complexity is unchanged.
