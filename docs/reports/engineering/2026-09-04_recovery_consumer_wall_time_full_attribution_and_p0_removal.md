# V7_RECOVERY_CONSUMER_WALL_TIME_FULL_ATTRIBUTION_AND_P0_REMOVAL

## Verdict

- `CONSUMER_WALL_FULLY_ATTRIBUTED = PASS` for dispatched recovery attempts.
- Reconstructed unaccounted wall for the latest valid automatic action receipt: `20.070 ms` (`0.062%`).
- Pre-dispatch terminal returns are now also closed by the same exclusive wall envelope.
- `CURRENT_115S_P0_REMOVED_OR_DEFERRED = IMPLEMENTED_NOT_LIVE_PROVEN`.
- `RECOVERY_LATENCY_SLO = NOT_CONSUMED`.
- Terminal boundary: no fresh ordinary automatic recovery transaction occurred after the final deployed fingerprint. No incident, user, target, route mutation, or state transition was manufactured.

## Current fingerprint and frontier

- Runtime implementation commit: `0248d8187090bb6351198e2cc04b2e59a9ee2430`.
- Runtime hashes:
  - `v7-health-loop`: `2d4e232fed5f765d879af84264f63be7bfbf2e2d4bb5baee496069d9840e762b`
  - `v7-users-autoswitch`: `71486a111d2f353621f141aacd75424642f54d93ab6f8e7e1b6cb4b4a0840215`
  - `v7-service-matrix-refresh-all`: `1f5d16de5b2521655e258eb70f7c5e6848d5f87bf4d10ae7746ab547923d73c5`
- `v7-health.service = active` after restart at `2026-09-04 01:41:37 MSK`.
- Current Program frontier remains `RECOVERY_LATENCY_SLO`.

## Consumer entrypoint and provenance

The measured production origin was the live existing chain:

`v7-health.service -> persistent Matrix consumer -> existing autoswitch/Planner owner -> governed executor -> route writer -> S11`.

Codex did not choose a user/source/target, create an incident, invoke the route writer, or manually advance Candidate/Packet/Lease/Barrier.

## Latest fully reconstructable automatic action receipt

The pre-repair receipt had:

- `T0 -> consumer start = 573 ms`;
- `consumer wall = 32,462.058 ms`;
- `consumer entry -> required-service S11 = 31,947.619 ms`;
- `S11 -> consumer return = 514.439 ms`;
- `T0 -> consumer completion = 33,035 ms`;
- one automatically moved ordinary user.

### Full mutually exclusive timeline

| Exclusive envelope | Duration |
|---|---:|
| consumer entry -> Matrix entry | included in reconstructed residual |
| Matrix entry -> governed dispatch | 16,290.556 ms |
| governed subprocess | 16,148.358 ms |
| governed result parse | 0.782 ms |
| post-child reconciliation/return | 2.292 ms |
| remaining scheduler/wrapper boundary | 20.070 ms |
| **consumer wall** | **32,462.058 ms** |

`UNACCOUNTED_WALL = 20.070 ms`, below both the `100 ms` and `1%` limits. The historical top-level receipt reported `16,293.302 ms` unaccounted because it predated propagation of `matrix_consumer_entry_ns`; its child Matrix receipt already measured the corresponding `16,290.556 ms` envelope. Current code projects that envelope directly.

For a lawful return before governed dispatch, the health owner now closes `Matrix entry -> consumer return` as the terminal pre-governed envelope. This is observability-only and changes no recovery semantics.

## P0/P1 attribution

### Removed pre-governed P0

The measured Matrix envelope was:

| Stage | Duration |
|---|---:|
| fresh profile-obligation advisory | 7,025.804 ms |
| passive consumer before handoff | 3,476.629 ms |
| post-passive current-scope lookup | 294.548 ms |
| duplicate service-failure advisory | 5,279.590 ms |
| **duplicate-chain total** | **16,076.571 ms** |

Root cause: one failed source could have several required-service incident IDs. The advisory required a singleton incident list even when the canonical Matrix current-scope owner had already selected one exact live source incident. The valid binding was rejected, so Runtime synchronously ran passive processing and rebuilt the advisory.

Owner: existing Matrix current-scope and existing autoswitch advisory owners.

Decision: `REUSE + COLLAPSE`.

- Reuse the exact Matrix-selected incident when it is present in fresh live service evidence.
- Narrow the transaction binding to that exact incident.
- Re-read and validate current Matrix scope after the first advisory.
- Do not run passive capture and a second advisory for the same unchanged current binding.
- Keep certification isolation and all current-data safety validation.

### Current next measured candidates

These are historical candidates, not a post-fix ranking:

- governed `apply_and_verification`: `8,769.298 ms` in the valid action receipt;
- governed subprocess wrapper beyond its known children: about `5.24 s`;
- advisory constructor/import/initialization envelope: previously about `4.36-5.09 s`, now explicitly instrumented as `advisory_planner_initialization`.

No further optimization was admitted without a fresh receipt on the current fingerprint.

## Structural before/after

Before:

`fresh advisory -> rejection caused by multi-service incident cardinality -> passive consumer -> scope reread -> second advisory -> governed dispatch`.

After:

`fresh advisory using exact Matrix source incident -> bounded current-scope revalidation -> governed dispatch`.

- Synchronous pre-governed subprocesses removed: `2` (`passive`, duplicate advisory).
- Advisory executions per unchanged generation: `2 -> 1`.
- Added: one bounded Matrix reread for safety.
- New owner/queue/timer/watcher/retry/state source: `0`.

## Code changes

- `e50575bc`: complete monotonic consumer/S11 attribution.
- `3df436d2`: exact Matrix source-incident binding and duplicate-chain collapse.
- `ba782836`: explicit advisory planner-initialization timing.
- `0248d818`: full terminal pre-governed wall attribution.

## Regression

- Focused health-loop tests: `39/39 PASS`.
- Targeted exact-incident/in-process advisory tests: `3/3 PASS` in `0.056 s` test time (`0.23 s` process wall).
- Combined affected suites: `328 PASS`, `5` pre-existing CPS-consistency failures, `1` local socket sandbox error. The failures are outside the touched owners and reproduce the already-known CPS/OMP fixture divergence; the socket error is `PermissionError` binding localhost in the restricted environment.
- Python compile and diff validation: `PASS`.

## Deploy and truth

- Safe-deploy allowlist: `PASS`.
- GitHub branch independently verified at `0248d8187090bb6351198e2cc04b2e59a9ee2430`.
- Safe-deploy final verdict: `PASS`, blockers `0`.
- Local/GitHub/deploy linkage aligned at deployment.
- Runtime hashes match the approved package; health service active.

## Post-repair evidence status

Existing isolated synthetic tests prove the exact multi-service source binding and in-process owner reuse without operational user movement. They are engineering evidence only and receive no production SLO credit.

No fresh ordinary automatic recovery receipt appeared after the final deployment. Therefore the required statement that the repaired owner no longer dominates production wall time is not yet evidence-backed, and neither the 7-second P95 nor 8-second maximum is claimed.

## Next CPS frontier

`RECOVERY_LATENCY_SLO` remains current. On the next naturally occurring owner-backed ordinary recovery, consume the already-deployed receipt and rank the largest current span. Continue with that exact owner only; expected historical candidates must not substitute for current measurement.
