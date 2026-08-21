# V5.3 T0–T11 — post-tournament architecture decision

Date: 2026-08-21 10:21 MSK  
Mission: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Stage: **E — architecture decision**  
Decision: `TARGET_ARCHITECTURE_MODEL_B_PLUS_C_POST_TOURNAMENT_REVALIDATED`

## Decision

Select the bounded FAST/DEEP architecture under the existing Matrix owner,
with passive escalation merged into the same Matrix path:

```text
existing passive signal or bounded fast trigger
→ exact source/hot-target service subset
→ existing Matrix writer/state/event
→ existing Planner source/target gates
→ existing Candidate → Packet → Lease → Barrier → Apply → Verification
→ full Matrix fallback and deep evidence
```

This is a post-tournament decision. It is not the old decision repeated by
name: it is selected because the new common failure and scale evidence
confirmed the measured bottleneck advantage and the fail-closed contracts.

## Candidate comparison

| Candidate | Result | Why accepted/rejected |
| --- | --- | --- |
| A — improved full Matrix | **Rejected** | Preserves the 14-service synchronous cost per egress (`14E`), including 14,000 modeled probes at 1,000 egresses, without a measured safety benefit over B/C. |
| B — exact FAST + DEEP under Matrix owner | **Selected core** | Reduced decision-path checks by 78.6% on the same service contract; kept full Matrix fallback, stale/conflict fail-closed behavior, Planner ownership and post-switch verification. |
| C — passive escalation through Matrix | **Merged into B** | Passive evidence safely accelerates suspicion in the same Matrix episode, but the tournament did not prove a separate architecture or independent health truth. |
| Role-aware/adaptive as a separate architecture | **Not admitted as separate candidate** | Current evidence supports it as a dimension of B/C; no measured gap proves a fourth architecture is needed. |

## Mature patterns reused, adapted and rejected

### Reused

- protocol-aware service checks and eligibility separation from Google Cloud;
- measurement → state → consumer separation from FRR/BFD and Cisco;
- compact current quality/stability projections from Fortinet-style SLA logic;
- explicit degraded/recovering and eligibility semantics from Envoy/HAProxy;
- multiple failure-domain evidence rather than one generic ping from MikroTik.

### Adapted

- HAProxy-like fall/rise and asymmetric failure/recovery thresholds, using the
  existing Matrix persistence and Planner cooldown owners;
- Envoy-like passive escalation, but only into the existing Matrix owner;
- role-aware hot/cold probe economy, with exact source/hot-target subsets and
  DEEP background/full fallback;
- target readiness as a separate Planner contract, never inferred from source
  health alone.

### Rejected

- direct BFD timing defaults as application/service truth;
- a second passive event or health owner;
- raw history scans on the synchronous path;
- single-host ping as Internet/service proof;
- unmeasured cross-egress parallelism as the first optimization;
- any short-result, stale-result or quality-only route action.

## Safety proof consumed by the decision

- Stage C candidate failure matrix: `5/5 PASS`.
- Stage D scale tournament: controlled 7/50/100 measurements plus explicit
  1,000-egress stress model.
- Short/full disagreement forced full canonical fallback and blocked action.
- Stale service state produced `MISSING_STATE_TRANSITION` and no apply.
- Certification-only identity was excluded from ordinary scope.
- Every candidate reached the same governed authority boundary with
  `users_moved=0` and `apply_executed=false`.
- Existing Matrix comparison + governed pipeline regression: `56/56 PASS`.

## Exact implementation residual

The selected architecture does not require a new owner or a new probe engine.
The exact residual is:

```text
promote the existing exact egress/service-subset comparative preflight
from shadow evidence to a governed decision consumer only after
fresh production caller/scope/provenance gates are satisfied
```

The existing implementation already runs short observation and unchanged full
observation for the same Planner-selected egresses, records agreement and
keeps full Matrix canonical. Automatic FAST consumer enablement remains held
until the exact production Runtime context and ordinary scope are coherent.
This decision therefore authorizes the implementation design and controlled
before/after work, but does not itself authorize a production route or client
move.

## Next stage

Stage F: compare the existing full path with the selected B+C path using one
before/after ledger for T0→T11, detection, decision, probe count,
short/full agreement, target readiness, resource pressure and recovery. The
result must distinguish controlled Polygon gain from any production gain.

## Verification boundary

No code, timer, route, Runtime, Authority or client state changed in issuing
this decision. Production evidence and automatic FAST admission remain later
gates in the same Mission.
