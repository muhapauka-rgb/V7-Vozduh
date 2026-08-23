# V5.3 N7 causal Polygon tournament

Date: 2026-08-23 MSK  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Block: `N7 CAUSAL_POLYGON_TOURNAMENT`  
Verdict: `COMPLETE_FOR_N7; N8_RUNTIME_CUTOVER_REQUIRED`

## Scope and safety

The existing Matrix remained the only canonical health/T0 writer. The existing
Planner supplied the prepared target set; no target was selected manually. All
production observations were Matrix/Telegram owner invocations with routing
mutation disabled. No ordinary client was moved, no route was changed and no
T11 was claimed. The terminal measured by the causal harness is S11.

## Implementation and deployment lineage

| Commit | Change | Production deploy |
|---|---|---|
| `9e03c207` | causal failure tournament and Planner-prepared Matrix consumer | `deploy-z8-14-Updatesystem-9e03c20-20260823T145029` |
| `a100be5a` | split prepared target checks into path, Telegram and other roles | `deploy-z8-14-Updatesystem-a100be5-20260823T145743` |
| `0e1a6a5c` | bounded timeout for exact role-scoped services | `deploy-z8-14-Updatesystem-0e1a6a5-20260823T145912` |
| `95d91e3c` | reuse the Matrix path owner in-process | `deploy-z8-14-Updatesystem-95d91e3-20260823T150243` |
| `1055f90f` | one atomic Matrix commit for a prepared path batch | `deploy-z8-14-Updatesystem-1055f90-20260823T150441` |

One earlier deploy attempt produced only a local/sandbox-side record because
GitHub access was unavailable. It was not counted. Every deploy listed above
was independently reconciled; the final truth check is `FULLY_ALIGNED` at
`1055f90f9d6a64d1d468b64d53665f5f7ea533cd`.

## Causal tournament result

The same controlled onset-to-S11 model covered interface, process, tunnel,
path, Telegram, DNS, other-required, multi-service and partial failures across
cadence offsets.

| Class / mode | P95 | Maximum | Disposition |
|---|---:|---:|---|
| interface, Mode B | 0.902 s | 0.952 s | `MODE_B_DIRECT_T0_ADMITTED` only for fresh `INTERFACE_DOWN_OR_MISSING` |
| interface, Mode A | 1.901 s | 1.951 s | retained fallback/comparator |
| tunnel/path/route, Mode A | 0.901 s | 0.951 s | `MODE_A_RETAINED` |
| Telegram, Mode A | 1.901 s | 1.951 s | `MODE_A_RETAINED`, two distinct failed endpoints |
| DNS/other/multi, Mode A | 9.501 s | 9.751 s | `MODE_A_RETAINED`, below 15 s contract |

Measured internal spans: direct Matrix T0 owner P95 1.521 ms; targeted Matrix
confirmation 0.883 ms; prepared-generation validation 0.0068 ms; S11 contract
validation 0.022 ms. Process death, tunnel/path/route absence, Telegram, DNS,
other-service and multi-service evidence remain ambiguous until their declared
Matrix/rotating-endpoint confirmation. Partial degradation remains Full/
`STOP_SAFE`, not direct T0.

## Falsification and contention

- stale or wrong generation produced no Matrix write;
- replay and restart produced exactly one event;
- correlated Telegram failure was suppressed;
- HARD and prepared-target roles remained independently schedulable when DEEP
  or other roles missed a deadline;
- no direct-T0 class bypassed source identity, freshness or generation checks.

## Production-context prepared-target evidence

The official prepared projection contained six semantic classes, four
contracts and two deduplicated targets: `awg0`, `awg3`.

The initial all-service check took 8.305 s. Splitting responsibility exposed
and removed process-per-target overhead. The path probe itself is now parallel
and cheap (69.7--71.1 ms for both targets), with one Matrix writer acquisition
and one atomic write. While the predecessor Telegram timer was still active,
the path batch spent 6.0--6.8 s waiting for the shared Matrix lock. This is not
network latency: the contemporaneous Telegram role measured 3.081 s total,
including 3.003 s lock wait and only 0.012 s lock hold. It is the exact caller
contention N8 must remove by migrating from separate predecessor timers to the
single role loop.

The other-service prepared-target role checked four required non-Telegram
services on both targets in 1.492 s. Both targets passed all 14 current Matrix
services; exact role probes were 0.78--0.83 s and their durable Matrix spans
were 0.087--0.303 s. Telegram checked the active required source plus both
prepared targets; all three were healthy. It created no event or candidate and
performed no autoswitch.

## Tests and limitations

The focused role/Matrix/health suites passed (37 tests including loopback
Matrix comparison). The causal tournament suite covers timing distribution,
phase offsets, stale/wrong-generation, replay/restart, correlation and role
isolation. Two historical lifecycle-binding failures and older CT-M0F/CPS
fixture failures predate N7 and are not represented as N7 regressions.

N7 does not prove unattended Runtime activation, predecessor timer retirement,
an applied client recovery or independent T11 telemetry. Those are N8/N10
responsibilities.

## Runtime and production effect

- source/runtime binaries: deployed and provenance-aligned;
- active production caller: still predecessor, deliberately unchanged in N7;
- Matrix writes: canonical owner only;
- route changes: 0;
- users moved: 0;
- terminal credit: S11 only, T11 false.

## Exact next step

`N8 UNATTENDED_RUNTIME_CALLER_AND_CONSUMER_CUTOVER`: seed the current Planner
prepared projection through the existing Matrix state, run a finite role-loop
canary, activate `v7-health.service --role-based-fast`, retire the two
overlapping predecessor timers only after rollback-ready proof, and execute one
controlled synthetic failure through the existing Candidate/Packet/Lease/
Barrier/Apply/verification chain. If independent client telemetry is absent,
record S11 and keep T11 false.
