# V5.3 Matrix comparison — controlled caller receipt

Date: 2026-08-20  
Scope: isolated end-to-end Polygon execution of the deployed existing-owner
comparison path. No production event, route, client or policy was used.

## What was exercised

The test uses the actual existing-owner chain with temporary loopback channels:

`existing Planner selection -> existing Matrix refresh -> existing Matrix
writer -> full selected-channel confirmation -> comparison receipt`.

The Planner selected one active source (`vless`), one eligible target (`awg0`)
and three required services. The short Matrix observation ran exactly 6 checks
(3 services × 2 selected channels). The following complete confirmation ran
28 checks (14 services × the same 2 channels).

The final canonical Matrix state contained both channels and all 14 service
rows per channel. The short/full required-service verdicts agreed. The
observation-only calls emitted no event and invoked no downstream consumer;
the test produced no Candidate, Packet, lease, route change or user move.

## Verification

| Check | Result |
| --- | --- |
| New end-to-end existing-owner Polygon chain | PASS |
| Existing selection and stale-denial checks | PASS |
| Existing observation-only and caller propagation checks | PASS |
| Existing controlled Matrix equivalence cases | PASS — healthy, required-service failure and methodology-limited response |
| Syntax and diff validation | PASS |

The controlled receipt proves the newly deployed caller contract works across
the real existing owner boundaries. It is not a production-latency sample: its
temporary local endpoints and test process do not represent real remote
network time, load or event frequency.

## Result and next action

Plan position: **the controlled caller receipt is complete.** The evidence now
covers selection, exact short probe, full confirmation, canonical final state,
agreement and no-mutation behavior without waiting for a natural incident.

Exact next action: perform the system-level Phase-E weighted decision using
this receipt, the separate scale revalidation and the mature-platform
comparison. The only eligible result is an existing-owner refinement that
retains full fallback; automatic FAST switching remains held until that
decision is durably consumed by the existing CPS/OMP owner.
