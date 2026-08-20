# V5.3 Matrix probe economy — controlled scale revalidation

Date: 2026-08-20  
Scope: Phase-F controlled scale evidence for the deployed Matrix comparison;
no production probe, route, client or policy mutation.

## Result

Three existing high-fidelity Polygon scenarios passed through the existing
Planner, safety and OMP consumers:

| Controlled case | Scale | Planner plus independent replay | Result |
| --- | ---: | ---: | --- |
| service-specific degradation despite healthy channel aggregate | 3,000 users / 60 channels | 7.403 s | PASS |
| recovery oscillation under capacity pressure | 5,000 users / 100 channels | 21.231 s | PASS |
| bounded decision trace volume | 10,000 users / 100 channels | 22.282 s | PASS |

All three retained deterministic replay, capacity/safety boundaries and the
existing consumer chain. Every forbidden effect was false: no Runtime or
production mutation, route change, client move, packet, rollback or Authority
expansion occurred. These scenarios prove that decision work is bounded by
channel classes rather than by a direct per-user Matrix probe loop; they do
not measure live endpoint latency.

## Probe budget model

The existing broad Matrix catalogue has 14 services per enabled channel.
Thus its unchanged broad-sweep probe volume is:

| Channels | Full Matrix checks per sweep |
| ---: | ---: |
| 7 current | 98 |
| 50 | 700 |
| 100 | 1,400 |
| 1,000 | 14,000 |

The controlled exact profile used three required services. The deployed
comparison may run it only for the exact Planner-selected active source and
eligible target set. Its immediate probe volume is therefore `3 × K`, where
`K` is the Planner-selected source plus target-channel count: 6 checks for one
source and one target, or 9 for one source and two targets. The full 14-service
check for that same selected set then remains the final comparison/fallback.

The 14-to-3 controlled Matrix measurement remains `41.284 ms` versus
`9.793 ms` (76.3% shorter, 78.6% fewer selected checks). It is a controlled
local measurement only. No production endpoint-time, CPU, memory or natural
event rate is inferred from it.

## Decision and remaining boundary

The evidence supports the existing provisional B+C direction only as a
fail-closed existing-owner refinement: exact source/target/service selection,
short Matrix observation and unchanged full confirmation. It does not admit
an automatic FAST switching path, a new health owner, cross-egress
parallelism, cadence change or a claim of production time reduction.

Plan position: **Phase-F controlled scale evidence is complete; the final
controlled caller receipt remains.**

Exact next action: exercise the deployed Planner-to-Matrix comparison as one
isolated Polygon chain — Planner selection -> short Matrix observation ->
full selected-channel Matrix confirmation -> compact agreement/fallback
receipt — with no real incident, route or client. Then recalculate whether the
system-level Phase-E terminal can be emitted or whether the full baseline must
remain the only admitted Runtime path.
