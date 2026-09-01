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

## Verification

- Shell syntax validation passed.
- The focused batch producer regression passed and asserts every new field.
- A broader historical health-loop test group has pre-existing expectation
  failures around its simulated scheduling order. Those assertions are outside
  this reporting-only detector change and are retained as non-credit
  diagnostics; no expectation was weakened.

## Next step

Deploy this bounded instrumentation through the existing safe-deploy owner.
Then classify the next ordinary detector outlier from its complete time split
before making any further performance change.
