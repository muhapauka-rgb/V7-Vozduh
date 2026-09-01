# Ordinary detector outer-latency attribution

Date: 2026-09-01

## Observation

Normal `other_required` detector cycles are not uniformly bounded: the health
owner observed occasional multi-second outer runs even though the existing
batch state showed a much shorter probe and post-processing interval. This is
not sufficient evidence to change probe cadence, safety confirmation, Matrix
ownership, or recovery execution.

## Bounded measurement change

The existing `v7-egress-diagnose` state output now distinguishes:

- profile-contract construction;
- batch setup before network probes;
- network probe wall time;
- canonical post-probe processing;
- total detector wall time.

The observation timestamp used by existing consumers remains in its prior
wall-clock domain. The added monotonic readings are reporting-only and cannot
alter Matrix state, target selection, Authority, packets, leases, routes, or
user assignments.

The first live readings isolated a further gap: the detector's internal
network work completes in about two seconds while the health owner can observe
an outer child lifetime well above that.  The existing child now returns one
ephemeral timing receipt to its parent only after atomically publishing its
normal state.  The receipt splits contract construction, detector-to-commit,
atomic output commit, and full script lifetime.  It creates no state, caller,
Matrix write, or recovery action; its sole purpose is to separate local
startup/scheduling delay from the detector's already-measured work.

## Verification

- Shell and Python syntax validation passed.
- Focused batch-producer and health-receipt regressions passed.
- A broader historical health-loop test group has pre-existing expectation
  failures around its simulated scheduling order. Those assertions are outside
  this reporting-only detector change and are retained as non-credit
  diagnostics; no expectation was weakened.

## Next step

Deploy this bounded instrumentation through the existing safe-deploy owner.
Then classify the next ordinary-detector outlier from the parent/child split
before making any further performance change.
