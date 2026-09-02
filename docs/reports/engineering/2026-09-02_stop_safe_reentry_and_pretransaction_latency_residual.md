# STOP_SAFE Re-entry and pre-transaction latency residual

Date: 2026-09-02  
Mission: `V7_RECOVERY_STOP_SAFE_REENTRY_VALIDATION_AND_PRETRANSACTION_LATENCY_RESIDUAL`

## Result

The existing Matrix recovery consumer now distinguishes an unchanged
`STOP_SAFE` incident from the same incident after a real owner-backed change.
The existing Matrix receipt also records the otherwise unattributed period
before the governed transaction starts. No new owner, queue, watcher, timer,
planner, registry, state projection, routing writer, or recovery path was
introduced.

## Re-entry semantics

The duplicate-suppression key remains bound to the existing Matrix source,
incident, affected scope, and required-service context. It now additionally
uses the existing prepared-projection invalidators:

- target health and path generation;
- target topology generation;
- target availability / rollback generation;
- capacity reservation generation;
- policy and organization-policy generations;
- active-operation generation.

The value is a deterministic digest of only those existing current-owner
facts and their freshness / invalidation status. It excludes timestamps and
advisory ranking. Therefore:

- an unchanged `STOP_SAFE` binding is suppressed exactly once;
- one real target, capacity, policy, conflict, lease/barrier, or freshness
  change permits one new normal Matrix attempt;
- a changed source remains isolated from another source;
- the code neither fabricates a Candidate nor invokes the recovery chain.

## Validation

- Focused Matrix-health suite: 35 passed.
- Direct consumer / receipt projection test: passed.
- Deterministic transition coverage: 100 invalidator changes.
- Seeded transition coverage: 1,000 generation changes.
- Static compile and whitespace validation: passed.
- Broader affected run: 173 passed; one pre-existing unrelated assertion
  remains in `test_source_bounded_planning_filters_before_decision_construction`.
  It expects an obsolete source string and was not changed or hidden by this
  Mission.

All validation is fixture-only. No Route writer, Candidate, Packet, Lease,
Barrier, registry, Core-primary state, user assignment, or customer route was
called or changed by the tests.

## Latency instrumentation

The existing Matrix lifecycle receipt now preserves the following monotonic
spans through the existing bounded action projection:

1. T0 to persistent Matrix consumer entry (when supplied by health);
2. current Matrix health read and passive capture;
3. failed-source scope read;
4. current source / L3 handoff lookup;
5. fresh-profile or ordinary advisory read where used;
6. standing-policy read;
7. current obligation and scope validation;
8. campaign-or-ordinary-scope resolution;
9. advisory snapshot freshness read;
10. governed-executor contract construction;
11. Matrix consumer entry to governed-executor dispatch.

The existing governed receipt continues to own all later Planner, Packet,
Lease, Barrier, Apply, route, and required-service/S11 timing. Thus the new
record fills the boundary before execution without duplicating execution
truth.

Known previous live evidence remains unchanged: VLESS `10.7.0.127 -> awg0`
was automatic, with T0-to-consumer 428 ms and required-service S11 at
16,453 ms. Its measured governed subtotal was about 7.0 seconds; the new
receipt is required to attribute the remaining pre-transaction interval on a
future live V7-originated recovery.

## Deployment and next action

Commit `83c155e06c7d344cc6b71cc50de99fafea38b019` was pushed to
`Updatesystem` and deployed by the existing safe gate as
`deploy-z8-14-Updatesystem-83c155e-20260902T093707`.

- GitHub, local commit and deployed Runtime linkage matched.
- The deployed Matrix file hash is
  `fa36b0aa37b10afa5c8ce62c8b1a59285cd41177c8cfcb02a93b26ac341eec3a`.
- `v7-health.service` is active; this deployment did not move users or alter
  routes.
- A read-only Runtime observation immediately after deployment found no
  active ordinary failed source and no new bounded action receipt.

The only valid next measurement is a new naturally generated V7 Runtime
recovery. Codex must observe its receipt only. It must not manually start,
advance, or complete the recovery transaction.
