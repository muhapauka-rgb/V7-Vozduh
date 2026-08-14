# V7 Hot-Path Fresh Obligation OMP Decoupling — Execution Report

**Mission:** `V7_HOT_PATH_FRESH_OBLIGATION_OMP_DECOUPLING_V1`  
**Commit:** `28c9e84543453ea66c1e33d29ea0afa7c7635757`  
**Verdict:** `IMPLEMENTED_AND_DEPLOYED`; fresh-path production observation remains pending a natural fresh obligation.

## Goal and bounded scope

Remove OMP receipt consumption as a synchronous predecessor of the existing
fresh service-failure executor. OMP remains an Engineering Plane receipt
consumer after execution; it is not removed from V7 and it remains a required
predecessor for the pre-existing receipt-bound, no-fresh-obligation branch.

Only `tools/v7-service-matrix-refresh-all` and its focused source-order test
were changed. No owner, state store, queue, worker, Planner, Packet, lease,
restore barrier, routing call, CPS field, or Authority rule was changed.

## Before → after

| Branch | Before | After |
| --- | --- | --- |
| Fresh advisory obligation | advisory → OMP receipt → bounded executor | advisory → bounded executor → OMP receipt |
| No fresh obligation / receipt handoff | OMP receipt → handoff → executor | unchanged |
| Packet / lease / barrier / apply / verify | executor-owned | unchanged |

The fresh executor continues to validate the exact obligation, source incident,
scope and policy. The deferred receipt is still invoked exactly once when it was
eligible, and its result is retained in the payload with an explicit
`receipt_deferred_until_after_fresh_execution` marker.

## Physical delta

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| Runtime source files | 1 | 1 | 0 |
| Test files | 1 | 1 | 0 |
| Added runtime lines | 0 | 27 | +27 |
| Added test lines | 0 | 19 | +19 |
| New runtime owners / stores / workers | 0 | 0 | 0 |
| Removed synchronous fresh-path dependency | OMP receipt before executor | OMP receipt after executor | 1 edge |

This is a latency-oriented dependency removal, not an LOC-reduction claim.

## Validation

- Python compile of the changed runtime tool passed.
- Targeted unit tests passed (3/3), including the fresh-order contract,
  legal no-op lifecycle, and executor delegation contract.
- Remote deployed binary SHA-256 matched the local approved binary.
- Existing safe deploy refreshed the canonical runtime fingerprint:
  `deploy-z8-14-Updatesystem-28c9e84-20260814T201200`.
- `tools/v7-truth-check --all --json` passed: CPS, GitHub and runtime commits
  all resolve to `28c9e84543453ea66c1e33d29ea0afa7c7635757`.

## Production observation boundary

No synthetic failure was created. The naturally observed planner cycles were
certification/advisory cycles with `execution_allowed=false`; therefore they
did not produce a fresh obligation or a user move. The new fresh ordering is
deployed and source-proven, but end-to-end fresh-failover latency improvement
is **not yet claimed**. Existing receipt-bound and legacy re-entry paths remain
unchanged.

## Effects and rollback

- **Runtime effect:** on a fresh obligation only, the existing executor can
  start before OMP receipt processing.
- **Production effect:** no routing mutation or user movement observed from
  this deployment alone.
- **Authority effect:** `NONE`.
- **Rollback:** `git revert 28c9e845`, followed by the existing safe deploy.

## Next step for the failover goal

Proceed with the bounded, read-only
`V7_HOT_PATH_POST_DECISION_MATERIALIZATION_PROFILE_V1`: map the approximately
38-second interval after `prepared_decision` and before completion into exact
functions, reads, writes and required safety effects. It must not revisit OMP
or change routing; its output is the smallest safe admission candidate for the
remaining hot-path latency.
