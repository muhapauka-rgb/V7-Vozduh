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

## Next executable step

After explicit approval of this narrowly bounded advisory-gate change, rerun
`tools/v7-safe-deploy`, verify local/GitHub/live hashes and health service,
then observe one automatic VLESS failover attempt. If it passes all existing
governed gates, continue the bounded ordinary cohort and N11 closure work; if
it stops, record the next exact owner-backed gate without manual movement.
