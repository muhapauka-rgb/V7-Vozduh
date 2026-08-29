# V7 automated ordinary failed-source recovery activation

Date: 2026-08-29  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Mission: `V7_AUTOMATED_ORDINARY_FAILED_SOURCE_RECOVERY_ACTIVATION`

## Result of this execution block

The existing health/Matrix consumer reached the ordinary failed-source action
for `vless` automatically. Matrix identified two ordinary users on the source
and the existing Planner selected `awg3` as the governed target. No manual
source, target, user, route, Candidate, Packet, Lease, or Apply was created by
the operator.

The governed transaction stopped before Apply because the packet gate observed
stale advisory intelligence projections (`risk-summaries`,
`blast-radius-summaries`, `overview-summary`) and the associated confidence,
trust, and prediction-floor warnings. This is a real consumer-path blocker:
the action was attempted, but `users_moved=0` and there was no ordinary-user
route change.

## Fresh live evidence

- `vless`: current Matrix service failures; 2 ordinary users (`10.7.0.126`,
  `10.7.0.127`).
- `awg3`: current Matrix row has no failed services and was selected by the
  existing Planner; target capacity reported as 39.
- active standing delegated policy: `sdpc_59029615229bc0f931a80be6`, max one
  user, one concurrent transaction, no self-expansion.
- `v7-health.service`: active.
- no standalone Matrix/Telegram timer was added or enabled.
- failed transaction: `packet_not_ready`, primary detail
  `snapshot_mismatch:risk-summaries`; no Apply and no route mutation.

## Change prepared

Commit `ee4ae185` (published to `Updatesystem`) adds a narrowly scoped
`ORDINARY_SERVICE_FAILURE` gate profile. It lets an emergency ordinary
failed-source transaction rely on current Matrix incident evidence plus the
existing governed target, capacity, lease, barrier, route, and required-
service gates, while treating lagging intelligence snapshots as advisory.
Normal planning and controlled/certification transactions retain strict
snapshot, confidence, trust, and prediction gates.

Focused verification: `423 PASS` across operator-execution, governed-cycle,
and autoswitch policy suites.

## Deployment status

The safe-deploy reviewer rejected applying `ee4ae185` because this is a
production safety-gate relaxation and requires explicit confirmation for that
specific change. The commit is published but not deployed; the live Runtime
continues running the previous aligned implementation. No workaround was
attempted.

## Subsequent live outcome and timing reconciliation

A later read-only reconciliation of the live Runtime records shows that the
existing automatic consumer subsequently completed both VLESS failovers. This
supersedes the earlier point-in-time snapshot above (`users_moved=0`); it does
not imply that `ee4ae185` was deployed.

All timestamps below are UTC (Moscow time is UTC+03:00). The first failure
observation for the incident was `2026-08-29T00:25:12.008579Z`.

| User | Target | Latest actionable failure event | Apply/operation terminal | Exact route/service verification | First observation -> S11 | Event -> S11 |
|---|---|---|---|---:|---:|---:|
| `10.7.0.126` | `awg0` | `00:48:47.654446Z` | `00:50:31.661559Z` / `APPLIED` | `00:50:36.502954Z` (`V7_USER_ROUTE_CHECK=OK`, service connected) | 1524.494 s (25m 24.494s) | 108.849 s |
| `10.7.0.127` | `awg3` | `02:05:05.050933Z` | `02:06:48.514706Z` / `APPLIED` | `02:06:54.275959Z` (`V7_USER_ROUTE_CHECK=OK`, service connected) | 6102.267 s (1h 41m 42.267s) | 109.225 s |

The current `users.registry` then contained no enabled VLESS users: user
`10.7.0.126` was on `awg0`, user `10.7.0.127` on `awg3`, and the disabled
synthetic entry `10.7.0.7` remained disabled. The operation records include the
existing decision trace, packet id, source incident/event ids, `APPLIED`
terminal state, and exact route verification; no manual target substitution
was recorded.

The complete route-writer critical path was 4266.334 ms for `10.7.0.126` and
5065.986 ms for `10.7.0.127`. The low-level kernel route mutation itself was
only 100 ms and 70 ms respectively; most of the writer interval was audit
work (3330 ms and 3870 ms). Exact individual timestamps for Candidate,
Packet, Lease, and Barrier are not persisted in these outcome records, so they
are not fabricated here. The evidence shows that the dominant delay was
before the final governed operation became actionable (about 103--104 s after
the latest bound event), with the second user additionally waiting for the
one-user-at-a-time transaction scope.

## Next executable step

After explicit approval of this narrowly bounded advisory-gate change, rerun
`tools/v7-safe-deploy`, verify local/GitHub/live hashes and health service,
then observe one automatic VLESS failover attempt. If it passes all existing
governed gates, continue the bounded ordinary cohort and N11 closure work; if
it stops, record the next exact owner-backed gate without manual movement.
