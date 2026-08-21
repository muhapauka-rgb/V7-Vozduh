# V5.3 C8 three-phase deadline Polygon proof

Date: 2026-08-22 00:41 MSK  
Mission: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Block: `C8_1000_CONTRACT_THREE_PHASE_DEADLINE_ISOLATED_POLYGON`

## Result

The existing health owner completed three consecutive controlled FAST phases
against 1,000 active, distinct service contracts.  Each phase used the
existing C8 cap of eight read-only probes; no Matrix consequence, route,
client movement, production state or Runtime process was invoked.

| Measure | Phase 1 | Phase 2 | Phase 3 |
| --- | ---: | ---: | ---: |
| FAST pass time | 19.441 s | 22.324 s | 22.030 s |
| 30-second phase overrun | 0 | 0 | 0 |
| completed contracts | 1,000 | 1,000 | 1,000 |

Last-phase contract timings were: first `109 ms`, p50 `10.848 s`, p95
`20.524 s`, maximum `21.554 s`.  The actual start-to-start spacing was
`30.005 s` then `29.999 s`.  The host woke around five milliseconds after two
absolute deadlines, but neither phase overran its following 30-second
deadline.  `schedule_wake_late` therefore preserves that diagnostic fact,
while `deadline_miss` now correctly means a phase overrun rather than normal
host scheduling jitter.

## Minimal repair

The first isolated run exposed a real local cost: the parent re-launched an
external hash calculation for every already completed healthy contract.  The
existing temporary work-set builder now derives the exact same per-profile
state key once while it is already parsing the canonical input files.  Workers
remain read-only; the parent remains the sole state/consequence writer.  The
serial path retains its previous calculation as a compatibility fallback.

No owner, timer, queue, registry, planner, state authority, decision rule,
Matrix mode, persistence rule, recovery rule or production configuration was
added or changed.

## Evidence and verification

- Isolated temporary state: one ready `wgfast` source, 1,000 distinct exact
  contracts and a successful read-only probe response for each.
- Actual commands: the existing `v7-health-loop` called the existing
  `v7-egress-diagnose --fast-producer-only --fast-producer-concurrency 8`.
- Returned successfully (`rc=0`) after three phases.
- Telemetry proves `max_inflight=8`, `observation_count=1000`,
  `completed_contract_count=1000`, and `receiver_invocation_count=0`.
- A process inspection after completion found no retained test, health-loop or
  diagnose process.
- Focused regression suite after the repair: `56 passed in 22.848 s`.

The earlier 28.376/30.600/30.781-second run is retained as a before-repair
observation, not hidden or used as passing evidence.  The second, same-fixture
run above is the accepted result.

## Boundary and exact next step

This closes only the multi-phase C8 scheduler proof.  It does not prove a
canonical failure, T0, decision, packet, lease, apply or client recovery:
the FAST producer deliberately ends in Matrix observation-only mode.

Next, use the existing controlled Matrix and governed-executor fixture with
two fresh same-scope failed observations, then trace its existing
`Matrix -> T0 -> candidate -> packet -> lease -> barrier -> apply -> T11`
records on a synthetic client.  It must remain isolated, retain Full fallback
for stale/unknown/conflicting evidence, and perform no production route or
ordinary-client mutation.

## Production effect

None.  This is source and Polygon evidence only.  Automatic FAST, deployment,
production timer changes, Matrix-policy changes and client movement remain
held.
