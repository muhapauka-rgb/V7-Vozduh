# V7 real ordinary failed-source recovery — engineering report

Date: 2026-08-28 (MSK)  
Mission: `V7_REAL_AUTOMATIC_FAILED_CHANNEL_USER_RECOVERY`  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

## Scope

This block consumed the two owner-approved corrections: keep a separate report
for the logical block, and prove callers/consumers before treating any old
branch as removable. The target was the existing ordinary production incident
for `10.7.0.125` (Liza), currently assigned to the failed `vless` channel.

## Fresh evidence before the change

- Matrix had a current `vless` failure scope classified
  `ORDINARY_PRODUCTION_ONLY`, affected scope 1, with a fresh source-scope
  fingerprint and 13/15 failed service observations.
- Planner selected one current move automatically: `10.7.0.125`,
  `vless -> awg0`; no target was supplied manually.
- The existing approved plan lock was expired and unrelated to the current
  user/source/target. Its clearance was also expired/cleared. This was the
  direct reason the governed consumer stopped before Packet creation.
- Intelligence snapshots were current after refresh; no ordinary user had
  moved before this block.

## Changes

Commits:

- `34519321` — Matrix quorum wake from identified failures.
- `86f3c338` — ordinary failure scope takes precedence over a stale
  certification tail.
- `18d73408` — reconcile an expired foreign lock for an ordinary incident;
  the historical lock remains diagnostic-only and is never reused.
- `b573faed` — pass explicit ordinary-service-failure context into the
  existing governed Planner.
- `140977ca` — route that context through the standing delegated apply path,
  not the emergency-incident gate.

No new owner, timer, registry, queue, state source, route writer, or authority
was created. Apply and verification semantics were not weakened.

## Verification

- Focused V7 suites: **247 tests passed** after the final code state.
- GitHub branch `Updatesystem`, local tree and remote are aligned at
  `140977ca36926d19abc4fc6dea5221df7fdd6d3c`.
- Safe deploy: PASS, deploy id
  `deploy-z8-14-Updatesystem-140977c-20260828T012402`.
- `v7-health.service`: active.
- Independent remote Planner read-only check after deploy: one fresh move
  selected, `expired_foreign_clearance_reconciled=true`, scope
  `ordinary_service_failure`, snapshot gate no longer stopping, and
  `PACKET_MATERIALIZATION_ELIGIBLE`.

## Caller/consumer proof

The active path is still the existing chain:

`v7-health.service` → `v7-health-loop` → existing Matrix T0 observation →
`v7-service-matrix-refresh-all` → `run_bounded_delegated_service_failure_action`
→ `v7-governed-canary-dry-run-cycle` → existing Planner/Candidate/Packet/Lease/
Barrier/Apply → `v7-user-switch`.

Static search alone was not used as closure evidence; the deployed health unit,
Matrix consumer, Planner output, and execution/closure records were checked.

## Runtime result and remaining blocker

The existing consumer was observed running after the earlier deploy, but its
current persisted incident had already been consumed by the process-local
exact-once T0 guard. The latest compact receipt still reports
`GOVERNED_TRANSACTION_STOPPED / packet_not_ready`, and the registry remains:

`10.7.0.125 current=vless table=1123 enabled=1`.

The final code is deployed; however, a new automatic production application
has not yet been credited. Obtaining that proof requires one fresh Matrix
event-only service cycle (or a new naturally generated failure event). The
available production service-cycle command can process all currently confirmed
incidents, so it is intentionally not run without an explicit narrow owner
approval for that broader side effect. No manual route or user change was made.

## Next step

After explicit approval for one event-only Matrix cycle, re-enter the existing
consumer and verify the complete automatic chain plus exact route/kernel and
required-service S11 for Liza. If the fresh cycle still stops, record the exact
post-Packet blocker; if it applies, record before/after assignment and close
the real-ordinary-recovery frontier.

