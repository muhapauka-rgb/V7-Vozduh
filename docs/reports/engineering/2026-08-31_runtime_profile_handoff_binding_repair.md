# V7: repair of the live profile recovery handoff

Date: 2026-08-31

## Scope

This is a bounded repair of the existing Matrix -> autoswitch recovery path.
It does not create a new owner, planner, queue, state source or route writer.

## Live evidence that opened the repair

The operator placed three ordinary users on `vless`.  The normal V7 Runtime,
not Codex, detected the profile-required service failure and moved all three
to `awg0` through Candidate, Packet, Lease, Barrier, Apply and service
verification.

The event is not valid seven-second evidence:

| Interval | Observed |
| --- | ---: |
| Matrix T0 | 2026-08-31 09:25:17 MSK |
| governed action starts | 09:26:06 MSK |
| first route assignment | 09:26:16 MSK |
| all three assignments | 09:26:18 MSK |
| required-service verification receipt | 09:26:32 MSK |

The automatic caller was confirmed by the `v7-health.service` journal
(`PROFILE_MATRIX_T0_CONSUMED`) and the generated operation record.  No
operator command, Codex route-writer call, manually selected target, Candidate,
Packet, Lease or Barrier was used.

## Measured cause

The source was current and unambiguous, but the profile fast-path did not keep
that binding.  The existing runtime therefore fell through to the historical
advisory path:

- pre-obligation source reconciliation: 11,596.780 ms;
- final source reconciliation: 12,430.161 ms;
- advisory total: 25,168.937 ms.

These retrospective reads are not a safety prerequisite once current Matrix
evidence has uniquely identified a failed source with affected profiles.  The
existing Planner, Authority, Candidate/Packet/Lease/Barrier owners and exact
route/service verification remain mandatory.

## Repair

`runtime_profile_handoff_source_constraint` now consumes the existing health
binding when present.  If that label is unavailable, it reuses the existing
`automatically_prioritized_failed_source` reader only when its current
Matrix + assignment + required-service join yields one unambiguous source.

The fallback only restores the *source* binding.  It does not choose a target
or a user and cannot create a governed execution object.  A missing or tied
result remains fail-closed and uses the established non-fast path.

## Verification

Passed focused tests:

- exact Matrix source fallback when the environment label is unavailable;
- fast-path passive-history deferral law;
- obligation-before-passive-history ordering.

Focused tests passed: three tests, 0.497 s, no failures.  The committed change
is `46f57e9a Preserve runtime profile failure binding`; the independent GitHub
branch check returned the same commit.  After GitHub truth became available,
the existing safe-deploy gate returned `PASS` and deployed the approved
implementation.

Post-deploy Runtime evidence:

- local and deployed Matrix implementation SHA-256 both equal
  `2a24d21a63ff7cf38f35159b19ceeec526d1336e34163da5f51ca1c0e063a899`;
- `v7-health.service` is active;
- `v7-admin-api.service` is active;
- standalone Matrix and Telegram timers remain inactive.

## Current status and next frontier

The repair is deployed and the previous three-user event is complete: all three
identities are now on `awg0`.  It was completed before this repair and remains
functional evidence only, not 7-second acceptance evidence.

The next action is one new operator-created bad placement.  V7's normal health
caller, not Codex, must then discover and recover it.  The new live sample must
retain every slow result and will be judged against the 7 s / 8 s law.
