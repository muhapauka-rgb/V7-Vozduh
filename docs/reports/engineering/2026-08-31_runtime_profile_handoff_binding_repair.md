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

## Follow-up: repeated placement on the same continuing failed source

At 13:20 MSK the normal `v7-health.service` caller emitted
`PROFILE_MATRIX_T0_CONSUMED` for three ordinary identities newly assigned to
the still-failed `vless` source. Matrix had a fresh three-member failed-source
scope and healthy eligible alternatives. No governed recovery was admitted.

Cause: the existing compact L3 incident for the *same* continuing source
incident remained closed after its earlier successful recovery. The runtime
hot path correctly avoids a slow historical scan, but consequently treated the
old zero-unresolved scope as current and passed no affected identities to the
existing governed executor.

Bounded repair prepared locally:

- Matrix passes its exact current source scope to the existing autoswitch
  advisory process only for the in-process profile handoff;
- autoswitch independently proves the source, incident, current Matrix scope
  count and registry-derived affected count agree;
- only the matching existing compact incident is reopened, with no stored raw
  user list, no target selection and no execution authority;
- Candidate, Packet, Lease, Barrier, Apply and every route mutation remain
  exclusively with the normal existing V7 governed caller.

Focused verification passed: five tests, including scope re-entry isolation,
the process-local handoff boundary, source-fallback behavior, exact ordering
and fresh-obligation materialization. The full two-module historical suite
also exposed pre-existing fixture errors unrelated to these changed paths;
they access partially constructed planners without their required Matrix or
policy inputs. They do not fail in the focused repaired paths.

Deployment and live proof remain pending safe publication of the repair. The
required next action after deployment is to leave the three already placed
identities untouched and observe the normal V7 caller recover them; Codex must
not advance that recovery manually.

At 13:39:45 MSK the production registry still showed the three test identities
`10.7.0.125`, `10.7.0.126` and `10.7.0.127` on `vless`; `v7-health.service`
was active. They were deliberately left in place so that the next valid proof
can originate entirely from the deployed V7 caller. The safe-deploy gate was
locally aligned but returned `NO-GO` solely because GitHub truth was unreadable;
no deployment was attempted or bypassed.

Fresh Matrix reading at 13:40 MSK continued to show current VLESS failures for
Google, Google Auth, Instagram and YouTube under the same active source
incident. It also retained older failures for several other services. Thus the
three identities are correctly left as a live acceptance condition: the source
is not suitable for profiles requiring any of the currently failed services.

## Follow-up: stale fast-producer reuse boundary

After the first deployed scope repair, the ordinary required-service detector
continued to run every 3.5 seconds, but it reused a Matrix service row for up
to 120 seconds. The health handoff correctly admits a row for only 10 seconds.
That mismatch meant a newly placed profile could receive a stale reuse receipt
instead of a new canonical Matrix confirmation, so no valid current T0 reached
the normal recovery caller.

The bounded repair makes the fast-producer reuse interval exactly 10 seconds,
the same as the health consumer's existing live-evidence law. A result older
than that is never used to start recovery; it causes the existing exact Matrix
writer to reconfirm the affected source/service contract. The health service
also emits one startup line stating whether its existing in-process Matrix
consumer loaded successfully. No cadence, policy, target selection, Authority,
route writer or client assignment logic changed.

Focused tests prove both sides: a fresh Matrix result is reused, while an
11-second continuing result must invoke the canonical confirmation before it
can progress. A historical test expecting a shadow call after fresh reuse fails
unchanged against the pre-repair version and was not treated as evidence for
this repair.
