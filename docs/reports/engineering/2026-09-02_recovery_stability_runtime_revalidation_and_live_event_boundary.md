# Recovery stability: Runtime revalidation and live-event boundary

Date: 2026-09-02 (MSK)  
Scope: current `RECOVERY_STABILITY_FOUNDATION`; read-only Runtime reconciliation.

## Purpose

Confirm that the deployed automatic ordinary-service recovery path is alive
after the stability corrections, and determine whether a current ordinary
failure exists that V7 itself may lawfully recover.

## Evidence

| Check | Result |
| --- | --- |
| GitHub / local branch | `479c3ea04e4b438421038198332e517a5e00c627`, aligned |
| Deployed behavioural commit | `75fe43e321d7b48c66f604ddd74e16045fd19f06` |
| `v7-health.service` | active; persistent Matrix owner proven |
| Truth check | `PASS`, no blockers; local mismatch is documentation/tests only |
| Ordinary detector | active every 3.5 s; recent complete cycles took approximately 2.2--2.5 s |
| Matrix state file | atomically refreshed at 02:03:50 MSK |
| Ordinary producer state | refreshed at 02:03:52 MSK; 3 active sources, 12 bounded probes, 0 receiver invocations, 0 consumer wakes |

The health journal's `ORDINARY_REQUIRED_SERVICE_DETECTION_PRIORITY` lines are
not a recovery operation and not a stuck queue.  They show the normal bounded
ordinary detector temporarily yielding CPU from advisory probes.  Its latest
producer receipt is `PASS` with `profile_failure_count=0` for every evaluated
current profile contract.

The existing Matrix still retains historical failed-service episodes for some
sources, but the current producer did not create a fresh eligible failure
binding and the read-only plan contained no selected ordinary move.  Historical
episodes therefore received no recovery credit and did not cause a route
mutation.

## Safety result

No user, route, candidate, packet, lease, barrier, registry entry, timer or
policy was changed by this reconciliation.  The deployed Runtime remains the
only actor permitted to originate a recovery transaction.

## Exact remaining boundary

The Program requires five to ten same-fingerprint **live ordinary Runtime**
cycles before recovery stability can be consumed.  There is currently no fresh
ordinary service failure with an affected eligible assignment, so there is no
lawful transaction to observe.  Creating or advancing one manually would
invalidate the required automatic provenance.

The next executable evidence is a genuine current ordinary profile-service
failure followed by the normal chain:

`v7-health -> Matrix -> affected scope -> Authority -> Planner -> Candidate -> Packet -> Lease -> Barrier -> Apply -> required-service S11`.

When it occurs, V7 must perform it itself; this report is not a request to
manually move a client or invoke an internal recovery command.
