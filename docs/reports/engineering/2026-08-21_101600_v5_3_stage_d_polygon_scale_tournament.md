# V5.3 T0–T11 — Stage D Polygon and scale tournament

Date: 2026-08-21 10:16 MSK  
Mission: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Stage: **D — Polygon + scale tournament**  
Status: `CONTROLLED_SCALE_RESULT_CONSUMED; PRODUCTION_SCALE_NOT_CLAIMED`

## Tournament rule

The same existing Matrix owner and the same Stage C failure contract were used
for the candidates:

- A — full 14-service Matrix;
- B — exact 3-service subset under the existing owner;
- C — the same subset with passive escalation through the same Matrix event
  path.

The 7/50/100 runs used an ephemeral local response surface. The 1,000-egress
row is an explicit stress model, not a live network measurement.

## Probe budget and controlled measurements

| Egresses | Variant | Probes | Harness wall | Owner CPU sum | Evidence |
| ---: | --- | ---: | ---: | ---: | --- |
| 7 | Full | 98 | 0.336 s | 307.884 ms | controlled local |
| 7 | Short | 21 | 0.133 s | 92.113 ms | controlled local |
| 50 | Full | 700 | 2.522 s | 2,142.091 ms | controlled local |
| 50 | Short | 150 | 0.921 s | 635.781 ms | controlled local |
| 100 | Full | 1,400 | 4.729 s | 4,322.248 ms | controlled local |
| 100 | Short | 300 | 1.860 s | 1,296.978 ms | controlled local |
| 1,000 | Full | 14,000 | — | — | explicit stress model |
| 1,000 | Short, hot cohort capped at 4 | 12 | — | — | explicit stress model |

Controlled probe-count reduction is `78.6%` whenever every egress is checked
short (`3/14` services). With a bounded hot cohort of four, the decision path
is capped at 12 probes even as the deep full Matrix grows with egress count.
The local wall and CPU values are engineering measurements only; process start
and local response-surface variance make them unsuitable as production latency.

## Scale invariants

The common failure contract remained unchanged at every modeled scale:

- short/full disagreement requires the full result as canonical fallback;
- stale/unknown target readiness remains fail-closed;
- probe cost scales by egress role/cohort, never by client count;
- full Matrix remains available for deep/background evidence;
- cross-egress concurrency is not used to hide probe volume or lock pressure.

## Tournament interpretation

Candidate A preserves safety but retains `14E` decision-path probe volume.
Candidate B reduces the decision path to `3H`, where `H ≤ 4`, while retaining
full fallback. Candidate C has the same probe budget as B; its only additional
dimension is passive escalation through the existing Matrix event path. The
current Polygon data proves the budget/safety advantage of the B/C family, but
does not prove a separate C advantage in detection latency yet.

This is sufficient to proceed to the architecture decision gate, but not to
claim production improvement or automatic FAST enablement.

## Exact next step

Stage E must issue one post-tournament architecture decision. It must record:

1. why the selected candidate won on T0→T11, probe budget and safety;
2. why A and the unselected dimensions were rejected;
3. which mature patterns are reused, adapted or rejected;
4. the precise implementation residual and its production/provenance gate.

## Verification and limits

- Stage C/D harness: `5/5 PASS`.
- Existing Matrix comparison + governed pipeline regression: `56/56 PASS`.
- No production users, routes, timers, Matrix state or Runtime were changed.
- No RSS or external-network production scale evidence was claimed.
