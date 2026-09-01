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

## Live causal finding and repair

The new parent/child split, together with read-only process observation, showed
that the material local contention was not a required Matrix confirmation.
The Admin overview could start duplicate full rebuilds while its cache was
empty.  Each rebuild reconstructs route reality for every enabled user and
runs read-only diagnostics, so two such requests competed directly with the
ordinary detector on the two-vCPU Runtime.

The Admin now coalesces an initial full rebuild to one worker. Concurrent
requests receive the already-existing lightweight canonical registry/Matrix
view until that worker completes.  The full passive overview cache is also
held longer, while the existing two-second live-status path continues to show
current assignments and channel health.  This changes neither an operator
action's immediate response nor any Matrix, Planner, Authority, routing, or
client behaviour.

## Verification

- Shell and Python syntax validation passed.
- Focused batch-producer, health-receipt and Admin cache-coalescing regressions
  passed.
- A broader historical health-loop test group has pre-existing expectation
  failures around its simulated scheduling order. Those assertions are outside
  this reporting-only detector change and are retained as non-credit
  diagnostics; no expectation was weakened.

## Production deployment and residual observation

The Admin coalescing repair was published and safely deployed in commit
`6762bc4`.  Local, GitHub and copied Runtime files were subsequently verified
as aligned; `v7-health.service` and `v7-admin-api.service` are active.  The
deployment touched neither Matrix ownership nor any user assignment.

The first post-deploy ordinary-detector observations were mostly in the
expected low-second zone: 2.606 s and 3.064 s for the complete detector
script.  A separate 8.300 s observation remains valid regression evidence.
Its receipt attributes 0.225 s to contract construction, 7.719 s before the
child receipt, and 0.046 s to atomic output.  The parent added about 0.208 s.
Therefore the residual is inside the existing batch observation owner, not an
Admin rebuild, Matrix write, or post-processing tail.

The complete per-attempt and process-CPU split was not present for that first
residual.  It has now been added as diagnostic-only output of the existing
batch owner for the next live cycle: batch owner elapsed time, user CPU,
system CPU, slowest individual attempt and timeout-like attempt count.  It
does not change the probe set, timeout, cadence, Matrix state, target
selection, Authority, routing or user movement.

## Next step

Safely deploy the bounded residual instrumentation.  Then classify any next
ordinary-detector outlier from the complete parent/child/process split before
making another performance change.  The product seven-second recovery result
remains open until a current owner-admitted live ordinary failure occurs; no
operator placement or recovery was manufactured for this report.
