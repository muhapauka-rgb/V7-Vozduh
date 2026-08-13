# Engineering Report — Service Failure automatic successor re-entry

Date: `2026-07-26`

Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

## Objective

Remove the manual `continue` gap after service-failure transaction terminals
without creating a scheduler, queue, Runtime, Planner, owner or Authority path.

## Fresh discovery

The standard `continue_omp_engineering_control_loop` already prioritised the
existing durable service-failure obligation and produced an exact successor.
However, it returned immediately after one consumption, while
`consume_service_failure_automation_frontier` called the atomic CPS owner with
`request_external_wake=false`. The successor therefore existed in data but was
not behaviorally reachable without another operator prompt.

The same consumer selected an obligation and appended its receipt without an
interprocess lock around the full select -> CPS projection -> receipt sequence.
Sequential replay was suppressed, but concurrent exact-once consumption was
not proven.

## Existing-owner repair

- The existing closure-records owner now holds a sidecar `flock` across the
  complete consumption transition. Competing Continue OMP processes cannot
  consume the same obligation or publish two successors.
- Receipt append now flushes and `fsync`s before releasing that owner lock.
- A safe non-terminal successor requests the already certified event-driven
  OMP wake as part of the atomic CPS projection.
- Exact Authority and real-world terminals continue to suppress the wake and
  preserve external input requirements.
- The Program contract now explicitly requires result -> OMP consumer -> CPS
  -> residual -> successor -> event-driven re-entry, including the evidence-
  gated `1 -> 2 -> 5 -> 10 -> bounded cohort` ladder.

No new durable registry, scheduler, queue, daemon, Runtime, Planner or Authority
owner was added.

## Verification

- Four concurrent independent processes: exactly one `PASS`, three
  `NO_PENDING_OBLIGATION`.
- Safe successor: `request_external_wake=true` and deterministic dispatch
  required.
- Existing service-failure focused suite: `12` tests, `PASS`.
- Full affected service-failure, policy, Authority projection, truth,
  self-continuation and event-driven re-entry suite: `336` tests, `PASS`.
- `git diff --check`: `PASS`.

## Effects and current terminal

Runtime apply, routing mutation, user movement, Packet/lease creation,
restore-barrier write, rollback apply, Authority expansion and Production
Maturity change: `NONE`.

The live service-failure action remains at the independent existing-owner
boundary `RESTORE_BARRIER_REQUIRED_FOR_EMERGENCY_FAILOVER`. This repair does not
issue that barrier or an Action Class contract. After the owner decision, the
same event-driven loop must resume automatically through fresh reconciliation.

## Production verification

The change was deployed only through the canonical safe-deploy owner. The only
runtime delta was the existing sync/OMP consumer library; no service restart
was required.

The production binary-only service-failure consumer opened the existing
closure-records owner under the new interprocess lock and returned no pending
obligation. Runtime, routing, users, Authority and Production Maturity were
unchanged.

The full Continue OMP consumer remains source-CPS-owned. The binary-only
production layout intentionally has no duplicate canonical CPS, so external
event-driven re-entry continues through the already certified Codex Automation
Platform source-workspace owner. No second production CPS was created.

The source non-test Continue OMP caller invoked the real consumer, consumed the
next independent product engineering frontier and produced its exact next
output with zero forbidden effects.

Post-deploy truth returned PASS/FULLY_ALIGNED and convergence returned
PASS/ALIGNED. CPS was intentionally not rewritten: the current owner-backed
program terminal remains the independent restore-barrier/Action-Class Authority
boundary.
