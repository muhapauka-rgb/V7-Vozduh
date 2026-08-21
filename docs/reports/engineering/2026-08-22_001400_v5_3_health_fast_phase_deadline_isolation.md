# V5.3 FAST phase deadline isolation

Date: 2026-08-22 00:14 MSK  
Mission: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Input terminal: `PREDEPLOY_FAST_OPTIMIZATION_REQUIRED_WITH_EXACT_RESIDUAL`  
Block: `EXISTING_V7_HEALTH_FAST_PHASE_PUBLICATION_AND_NEXT_PHASE_DEADLINE_ISOLATION`

## Summary

The existing health owner now has one foreground, monotonic-deadline loop.
FAST starts first and subsequent starts are scheduled from the prior intended
deadline, not from completion of the legacy tail plus `sleep 30`.  Old work is
still performed by the same owner, but only inside the remaining phase budget.
It is deferred synchronously when that budget expires; no worker, queue,
timer, state file, Matrix writer, route change, or client movement was added.

This is source and Polygon validation only.  Nothing was deployed, FAST was
not enabled automatically, and production persistence/recovery are unchanged.

## Current and old loop

| Item | Old | New |
| --- | --- | --- |
| Health owner | `v7-health.service` | unchanged |
| FAST start | after history/stability/load | first operation |
| Next start | all work + `sleep 30` | prior monotonic deadline + 30 s |
| Long old work | can delay next FAST indefinitely | bounded to remaining budget or deferred |
| FAST overlap | not explicitly governed | impossible: one foreground phase at a time |
| Persistent scheduler state | none | none |

Exact old command order was `history -> stability -> load -> diagnose ->
state merge -> desired-state save -> JSON save -> sleep 30`.  The old tail can
therefore delay the second producer observation.  The new owner order is
`FAST -> bounded legacy round -> wait until absolute next FAST deadline`.

## Code changes

- `systemd/v7-health.service` now starts only the existing health owner's
  installed loop, `/usr/local/bin/v7-health-loop`.
- `tools/runtime-support/v7-health-loop` is the implementation of that owner.
  It uses one process-local `time.monotonic_ns()` clock; the planned deadline
  is ephemeral execution memory, not canonical state.
- The loop starts child commands in a separate process group, waits for every
  one, and terminates the entire group if its budget expires.  Thus an old
  command cannot remain in the background or collide with a later FAST phase.
- Legacy commands rotate fairly between phases.  Each existing command still
  writes through its old atomic temporary-file path; interruption never
  publishes a partial new canonical file.
- `tools/v7_sync_lib.py` includes the loop in the existing deployment manifest.
  It was not published or deployed.

## Deadline and overrun semantics

For planned starts `D0, D0+30s, D0+60s`, a completed FAST phase waits only to
the next absolute deadline.  A phase that overruns begins the currently due
next phase immediately after it finishes.  It does not create a backlog and
never overlaps the prior phase.  Logs include planned/actual starts,
start-to-start time, jitter, pass duration, overrun and deadline-miss marker.
These are journal telemetry only, not a new state surface.

## Polygon evidence

The new focused test exercises three phases with a deliberately slow legacy
command.  Its result shows that the legacy command is terminated within the
remaining budget and does not turn a 0.5 s test cadence into a multi-second
cadence.  A separate overrun test proves serial immediate continuation:
phase N+1 starts after N finishes, not at `finish(N)+interval` and not in
parallel.  It also proves that controlled commands require a finite test run.

Focused regression suite:

```text
56 tests passed in 24.704 s
```

It covers the health loop, FAST producer C8 safety, service-Matrix
observation-only writer boundary, controlled persistence guard, non-Telegram
trigger path, stale/unknown protections and the prior latency model.

An exploratory 1,000-contract shell fixture was deliberately not treated as
evidence: its per-probe shell startup model differs from the accepted C8
fixture and therefore cannot invalidate or replace the measured C8 one-pass
result (`29.436 s`).  It left no process after completion.  The earlier first
Bash prototype also exposed per-process monotonic clocks on this development
host; it was discarded and its two test processes were stopped.  The committed
implementation keeps all scheduling time inside one Python process and has no
such clock split.

## Safety invariants retained

- C8 remains an explicit controlled `v7-egress-diagnose` option only; normal
  service invocation does not pass `--fast-producer-only` or a parallel cap.
- At most eight read-only probes and serialized Matrix consequences remain
  unchanged.
- The full Matrix remains the fallback for stale, unknown, conflicting or
  ambiguous evidence and for target-readiness denial.
- Candidate B remains two fresh same-scope producer observations plus one
  targeted Matrix corroboration in controlled/shadow mode only.
- Recovery rise, cooldown and re-admission policy were not changed.

## T0–T11 and remaining evidence

The scheduling defect is removed in code and its process/lifecycle safety is
tested.  A new real controlled C8 multi-phase measurement must still be run
through this loop using the already accepted 1,000-contract Polygon fixture,
then be connected to the existing governed T0–T11 fixture.  The present FAST
trigger intentionally requests Matrix observation-only mode, so it cannot
honestly be described as canonical T0 or client recovery.  No automatic or
ordinary-client action was enabled to bridge that boundary.

| Scenario | Failure to sample 1 | sample 1 to sample 2 | T0 / T11 |
| --- | ---: | ---: | --- |
| exact persistent service/DNS/tunnel/multi-service | bounded scheduler code | bounded scheduler code | not yet measured under controlled C8 caller |
| transient / source-change / stale / conflict | fail closed | repeat reset or Full fallback | STOP_SAFE |
| target stale, unknown or capacity/policy denied | n/a | n/a | STOP_SAFE / Full revalidation |

## Final terminal and next action

```text
FAST_HEALTH_LIFECYCLE_OPTIMIZATION_REQUIRED_WITH_EXACT_RESIDUAL
```

Exact residual: execute the accepted 1,000-contract C8 Polygon fixture for
three consecutive deadline-isolated phases and feed its two fresh,
same-scope failures through the existing controlled Matrix/T0–T11 fixture.
This is the smallest next action; it must retain the existing observation vs
canonical-action boundary and must not deploy or enable automatic FAST.

## Production effect

None: no deploy, timer change on a runtime host, Matrix change, canonical
production persistence change, route change, ordinary-client movement or
recovery-policy change.
