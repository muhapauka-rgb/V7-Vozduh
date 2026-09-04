# Ordinary failed-source target-pin isolation and live recovery — 2026-09-01

## Result

`10.7.0.126` and `10.7.0.127` were left on failed source `1` while the current
Matrix had an exact ordinary affected scope of two.  The existing Planner,
run read-only with the same current source contract, selected `awg0` for both
users.  The live governed consumer nevertheless stopped at
`ordinary_service_failure_selection_binding_invalid` with zero candidates.

The repair is deployed and the live V7 Runtime subsequently moved both users
from `1` to `awg0` itself.  Codex did not invoke the route writer, choose the
target, create an incident, Candidate, Packet, Lease or Barrier, or edit the
user registry.

## Cause and repair

The governed transaction unconditionally passed the target of a separate
certification/availability action class into ordinary failed-source planning
and Apply.  That target is lawful only for its certification action.  It must
not constrain an ordinary service-failure Planner decision.

`governed_planner_target_for_action()` now returns a target constraint only
for the availability-first or CT-M0F certification action that owns it.
Ordinary service failure receives no injected target and continues to consume
the existing Planner's current selection.

* Commit/deploy: `12b53f5d9aa69bf419a8d6c9c991750a6632a1c7` —
  `Keep certification target pins out of ordinary recovery`.
* Deployment: `tools/v7-safe-deploy --apply` passed allowlist, GitHub
  alignment and truth checks; the updated governed executor was installed and
  `v7-health.service` restarted.
* Focused tests: target-pin separation, ordinary selection binding, and
  exact Matrix-source handoff passed.  Python syntax compilation passed.
* The broad legacy unit bundle still has unrelated pre-existing fixture
  expectation failures; none were hidden or changed by this patch.

## Live Runtime evidence

At `2026-09-01T14:22:13Z` Matrix recorded source `1` as currently failed,
with two ordinary affected users and incident
`sfinc_d1f8e0179264449d1b9078e6e6df5916`.  The existing Planner's read-only
current decision selected both `10.7.0.126` and `10.7.0.127` for `awg0`.

The health Runtime receipt at `2026-09-01 17:27:59 +03:00` proves the normal
automatic path completed: `source=1`, `affected_scope_count=2`,
`action_attempted=true`, `action_completed=true`, `users_moved=2`,
`action_status=ACTION_COMPLETED`.  Current canonical assignments are:

* `10.7.0.126 -> awg0`
* `10.7.0.127 -> awg0`

The current Matrix ordinary failed-source scope is empty and
`v7-health.service` is active.

## Timing and remaining boundary

This receipt is functional automatic-recovery proof, but it is **not** a
seven-second pass:

| Interval | Measured |
| --- | ---: |
| Matrix T0 to consumer start | 9.957 s |
| Consumer execution | 14.410 s |
| Matrix T0 to consumer complete | 24.368 s |

The repaired target binding removed an invalid stop; the remaining latency is
in existing execution/verification work, not target discovery.  The next
frontier is to reduce the measured `T0 -> consumer start` and governed
execution path while keeping the live V7 caller as the sole recovery actor.
