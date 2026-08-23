# Controlled unattended failure-to-T11 automation — bounded execution report

**Date:** 2026-08-23  
**Programs:** `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`; existing Automation / Mission Completion Evidence direction  
**Block:** `CONTROLLED_UNATTENDED_FAST_FAILURE_TO_T11_AUTOMATION`  
**Outcome:** `STOP_SAFE_RUNTIME_MEMORY_LIMIT`; no route or client change.

## Purpose and boundary

This block traced the live controlled VLESS failure from the existing Matrix
episode to its existing governed CT-M0F consumer.  It did not create a Program,
Mission, owner, Matrix, Runtime, queue, registry, state store, or route writer.
Only the existing Matrix, `users.registry`, controlled selector, governed
executor, Packet/Lease chain, and systemd consumers were inspected or reused.

The controlled source remained certification-only and the ordinary-user count
remained zero throughout.  No ordinary user was selected, moved, or otherwise
affected.

## Proven caller/consumer chain

| Output | Existing producer | Automatic caller | Existing consumer | Observed result |
| --- | --- | --- | --- | --- |
| VLESS failed Matrix episode | Matrix timer / Matrix writer | `v7-service-matrix-refresh.timer` | Matrix refresh | fresh `WARN`/failed source observed |
| current controlled scope | Matrix + `users.registry` | Matrix refresh | CT-M0F selector | exactly one certification identity and `awg3` selected |
| ready selection | selector | Matrix controlled branch | governed CT-M0F executor | consumer was reached automatically |
| Candidate → Packet → Lease → Apply → T11 | governed executor | same consumer | existing Planner/Packet/Lease/verification owners | not reached: kernel OOM killed consumer before Candidate |

The first automatic attempt demonstrated that the earlier functional gap was
real: a `READY` selection had no automatic consumer.  The connection was added
through the existing consumer, then independently exercised by the normal
Matrix timer (no manual Matrix, selector, Packet, Lease, Apply, verification,
or closure command was run after the failure condition).

## Changes made

1. The existing CT-M0F consumer now supplies the existing compact target
   diagnostic to the bounded-memory selector as an ephemeral one-shot file;
   no cache or durable state was created.
2. The existing governed executor gained the narrow
   `CERTIFICATION_ONLY_MATRIX_FAILURE` pre-apply binding.  It rechecks the
   fresh Matrix episode, current `users.registry` scope, exact incident,
   service correlation, and zero ordinary-user condition before any Packet can
   be made.  It deliberately does not pretend that a certification-only
   incident has an ordinary positive-scope OMP obligation.
3. A real-failure regression locks the one-way rule: after a verified move,
   the client remains on the reserve while VLESS is failed.  Returning to VLESS
   remains exclusively the existing recovery/re-admission lifecycle.
4. The attempted automatic consumer exposed a production memory ceiling.  A
   30-second existing planner timer caused repeated OOM retries; it was
   disabled and the service stopped.  Matrix timer/cadence, routes, and clients
   were not changed.
5. Production Matrix now returns a bounded `STOP_SAFE` for this controlled
   branch while the executor memory correction is not proven.  This prevents
   further automatic OOM retries and leaves the full Matrix fallback intact.

## Production observations

- Existing Matrix timer was enabled and continued its ordinary 15-minute
  lifecycle.
- A Matrix run completed successfully and reached the automatic controlled
  consumer; no manual intermediary command was used.
- The consumer's peak memory reached approximately **1.6–1.8 GiB** and was
  killed by the kernel before Candidate materialization.
- The automatic record confirms `users_moved=0`,
  `runtime_mutation_performed=false`, no Candidate, Packet, Lease, Barrier,
  Apply, route change, traffic verification, T11, or closure.
- The recurring 30-second `v7-autoswitch-planner.timer` is now disabled on the
  host as a containment action.  This is not a Matrix timer and does not
  change Matrix cadence.

## Verification

- Focused automation, one-way recovery, and Matrix-binding tests: **all
  passed**.
- Existing Polygon Matrix/candidate suite: **11/11 passed**.
- The broader two-module local run completed **226 passing tests** and exposed
  three pre-existing fixture-contract failures unrelated to this block; none
  are in changed code paths.
- Safe deployment and independent GitHub convergence passed for commits:
  `0f9cc12f`, `6c9a0109`, `daf763c3`, and final containment `0a0add6c`.

## Timing and residual

The ordinary Matrix observation took about **58–69 seconds**.  The intended
automatic consumer began from that Matrix output but consumed about
**87 seconds** before OOM termination, so there is no valid Failure→T11 timing
or speedup claim.  `T0→T11` remains unproven and must not be inferred from
synthetic or partial execution.

## Exact next step

Run a **bounded Polygon memory-profile and reduction** of the existing
governed CT-M0F executor, identifying the owner-held large allocation during
the exact ready-selection → Candidate path.  Reuse/stream or release that
existing-owner input without changing the Decision, Packet, Lease, Matrix,
or route owners.  Then prove one isolated consumer run below the production
memory envelope before re-enabling any automatic consumer trigger.  Only after
that proof may the full unattended VLESS failure → reserve → traffic T11 test
be retried.
