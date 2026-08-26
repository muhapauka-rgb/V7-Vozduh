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

## Next action

Publish and safely deploy this already-tested bounded verifier-scope correction.
Then run **one** certification-only cold Telegram-critical transaction on the
new immutable fingerprint, verify the exact required Telegram endpoints and
complete cleanup. The result will decide whether any further latency work is
actually justified. Do not manufacture a five-sample series or begin N10/N11:
those require their own owner-backed contracts.
