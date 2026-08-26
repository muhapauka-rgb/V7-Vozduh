# V5.3 Telegram-critical S11 scope reconciliation

**Date:** 2026-08-26  
**Program:** `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
**Scope:** one measured correction to the existing Matrix verifier used after a
governed Telegram-critical switch. This report is historical evidence; live
state remains in `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

## Why this block exists

The deployed prepared-target handoff was proven in a second certification-only
transaction. It reused the fresh Matrix decision, did not rebuild the Planner
world model, and selected the target through the normal owner. The transaction
was functionally valid but slow: 18,782.195 ms from onset to S11.

The receipt isolates the remaining post-switch cost. The required Telegram
endpoints passed in roughly 45--201 ms. But the command used for S11 also ran
Telegram's optional diagnostic endpoints; an optional TCP/5222 endpoint waited
4,004.3 ms. That is neither an unrelated service failure nor a required
Telegram profile condition. Waiting for it makes S11 slower while providing no
additional required-service evidence.

| Observed span | Measured |
| --- | ---: |
| onset -> decision | 10,589.498 ms |
| decision -> Apply admission | 190.721 ms |
| assignment commit | 425.350 ms |
| kernel path visible | 17.248 ms |
| required-service verification reported by receipt | 6,931.644 ms |
| onset -> S11 | **18,782.195 ms** |

This sample is a functional performance failure, not rollout credit. It was
closed through the existing recovery/reset owners; the certification identity
returned to its isolated source and ordinary-user effect remained zero.

## Change made

The existing `tools/v7-service-matrix-test` now accepts a narrowly constrained
`--required-endpoints-only` mode. It is accepted only together with
`--services telegram --probe-observation-only`:

- it probes every endpoint marked required for Telegram;
- it keeps route/kernel verification unchanged in the governed apply path;
- it does not run optional Telegram diagnostics or unrelated services;
- it cannot write a partial result into the canonical full Matrix, so normal
  Matrix health and target-selection semantics remain unchanged;
- an invalid invocation stops safely.

`tools/v7-users-autoswitch` uses that mode only when the affected profile's
sole required service is Telegram. Profiles with other service requirements,
and ordinary full Matrix checks, keep their existing behavior.

This reuses the current Matrix verifier and the sole route writer. It adds no
owner, timer, runtime, planner, queue, registry, alternate truth source or
routing command.

## Verification before publication

| Check | Result |
| --- | --- |
| required-only Telegram unit proof | required endpoints only; optional endpoints excluded |
| governed verifier command contract | exact Telegram subset plus observation-only boundary |
| focused Matrix/Planner regression | 324 tests passed |
| broader affected V5.3 regression | 565 tests passed |
| routing/client effect during tests | none |

The local test showed the sandbox cannot bind a loopback port; the unchanged
isolated Polygon test suite was then rerun in the permitted test environment
and passed. This is an environment limitation, not a product failure.

## Runtime proof after deployment

The change was published as `2c755001ef2045a9f45ca8489e07aa453fe0af9d` and
deployed by the existing safe-deploy owner as
`deploy-z8-14-Updatesystem-2c75500-20260826T153152`. Local, GitHub and Runtime
hashes matched; `v7-health.service` stayed active and the retired standalone
Matrix/Telegram timers stayed inactive.

One new cold certification-only transaction was then run through the normal
owner chain. Matrix selected `awg3`; no target was selected manually. The
prepared decision was reused, no world model was rebuilt and there was no full
Planner fallback. The result was functionally valid but does not earn latency
credit:

| Span | Before scope correction | After scope correction |
| --- | ---: | ---: |
| required Telegram service verification | 6,931.644 ms | **1,183.018 ms** |
| onset -> S11 | 18,782.195 ms | **17,759.208 ms** |

The necessary Telegram proof itself became 5,748.626 ms faster (about 83%).
The remaining dominant time is now before the decision: first failed
observation/confirmation was 13,566.293 ms and failure -> decision was
14,755.000 ms. The downstream prepared decision, Apply, route and mandatory
service verification are no longer the leading cause.

The test identity, temporary profile and controlled failure condition were
removed through the existing reset/recovery owners. It returned to its isolated
source; no ordinary route or user assignment changed.

## Next action

Do not repeat this same certification sample merely to fill a series. First
measure and remove, if safe, the proven producer contention before T0: the
Telegram role is scheduled every second but its healthy observations were
repeatedly delayed by shared Matrix writes while parallel Matrix work held the
same writer lock. Preserve the Matrix owner, confirmation and recovery
semantics; do not relax required service proof or begin N10/N11, which retain
their separate owner-backed contracts.
