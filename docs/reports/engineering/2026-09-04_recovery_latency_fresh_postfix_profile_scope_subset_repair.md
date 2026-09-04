# V7 Recovery Latency: Fresh Postfix Profile-Scope Subset Repair

## Scope

`V7_RECOVERY_LATENCY_SLO_FRESH_POSTFIX_MEASUREMENT_AND_DOMINANT_APPLY_SUBSPAN_REPAIR`.
This report concerns one automatic ordinary recovery observed after the
persistent-owner deployment. No user, source, target, Candidate, Packet,
Lease, Barrier, route, registry, Matrix or Authority state was manually
advanced for this investigation.

## Fresh Runtime Evidence

The existing `v7-health.service` caller completed automatic operation
`runtime_autoswitch_b5eb68ec00bc89b48f17e5e7` for three ordinary members from
`awg3` at 2026-09-04 09:18 MSK. The health receipt recorded:

| Span | Measured |
| --- | ---: |
| Matrix T0 to consumer start | 407 ms |
| Matrix T0 to required-service S11 | 24,971 ms |
| Matrix T0 to consumer completion | 25,321 ms |
| Matrix pre-governed | 16,078 ms |
| Governed execution to S11 | 24,563 ms from consumer entry; governed child wall 8,810 ms |
| Governed Apply and verification | 6,120 ms |

The receipt is valid automatic Runtime evidence, but fails the product
`<= 7 s` / `> 8 s` contract. It is not SLO credit.

The pre-governed envelope was attributable: initial source/handoff reads
136 ms, fresh profile advisory 7,264 ms, passive bridge 3,343 ms, and a second
advisory 5,224 ms. Apply itself remained an independent P1 at 6,120 ms.

## Proven Cause and Repair

The existing runtime-profile binding compared the full Matrix ordinary source
scope with the smaller set of profiles whose required service actually failed
using equality. For a mixed source, ordinary members with no failed required
service made that false despite the source, Matrix incident and scope
fingerprint being exact. The advisory then lost the exact binding and entered
the passive-first bridge followed by another advisory pass.

`tools/v7-users-autoswitch` now accepts only a non-empty affected profile set
contained in the exact Matrix ordinary scope (`0 < affected <= scope count`).
It preserves the same channel, Matrix incident id and scope fingerprint. The
existing Planner still derives members and targets; the governed executor still
revalidates current facts and owns Candidate, Packet, Lease, Barrier, Apply and
S11. No new owner, queue, cache, persistent state or route writer was added.

## Verification

- Focused runtime-profile binding and duplicate-advisory tests: 4 PASS.
- The affected broader suites were started. Their first failure is a pre-existing
  CPS/OMP consistency fixture (`cps_current_stop_divergence`, related durable
  program-state projections) in
  `test_accounted_scope_projects_active_incident_drain_into_source_cps`; it is
  unrelated to this source-scope predicate and was not changed here.
- `git diff --check`: PASS.

## Next Evidence

## Runtime Deployment and Postfix Observation

The approved safe deploy completed at 2026-09-04 09:57:56 MSK with the
required explicit restart of the persistent health owner. Runtime
`/usr/local/bin/v7-users-autoswitch` now has SHA-256
`e4d6eb5835fb51a77b17dffeb261c6bf61ed61412c80ea342584ba3ea19046b8`,
matching commit `96260e3f`; `v7-health.service` is active.

The normal `other_required` health producer is running on its existing 3.5 s
cadence. Its latest owner output is `CONTROLLED_OBSERVATION_ONLY`, with no new
Matrix profile T0, no active operation, and no lease. Older Matrix failures
are stale observations, not a fresh recovery event. Consequently this turn
creates no synthetic incident and earns no SLO credit.

The next valid evidence is one new ordinary Matrix T0 observed and consumed by
the normal `v7-health.service` caller. Its receipt will determine whether the
dominant residual remains preparation or has moved to governed
Apply/verification. No manual recovery is permitted.
