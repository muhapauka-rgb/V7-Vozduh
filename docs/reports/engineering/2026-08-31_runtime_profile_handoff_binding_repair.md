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

The safe-deploy gate accepted the deploy allowlist but correctly returned
`NO-GO` until the changed implementation is committed and GitHub truth can be
read.  Its current external blocker is `github_remote_unreadable`; no deploy
was attempted through that gate.

## Current status and next frontier

The repair is locally implemented and tested, but not deployed.  The next
action is to commit it, publish it when the existing GitHub truth check becomes
available, run the safe deploy, then wait for a new operator-created bad
placement and observe a fully automatic V7 recovery.  The new live sample
must retain every slow result and will be judged against the 7 s / 8 s law.
