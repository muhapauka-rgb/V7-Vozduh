# V5.3 Matrix health — system-level weighted architecture decision

Date: 2026-08-20  
Scope: Phase-E system-level revalidation using the Atlas, mature-platform
comparison, deployed shadow comparison, controlled caller receipt and
controlled scale evidence.

## Decision

`TARGET_ARCHITECTURE_REFINED_EXISTING_OWNER_VARIANT`

The refinement is intentionally conservative:

- the existing full Matrix remains the live detection and switching baseline;
- the existing Planner-to-Matrix exact subset is retained as a deployed
  shadow comparison and safety/measurement path;
- a passive signal may still raise suspicion only through the existing Matrix;
- no automatic FAST switch, new cadence, threshold, target registry, queue,
  owner or state store is admitted.

This is the engineering decision input for the system-level resolution of the
earlier provisional B+C result. It does not reject the useful subset
mechanism. It rejects treating it as a faster first Runtime decision before an
official pre-full selector exists. It has no Runtime effect until the existing
OMP/CPS owner consumes this exact result atomically.

## Why the full Matrix remains live

| Gate | Full Matrix baseline | Exact subset shadow | Result |
| --- | --- | --- | --- |
| Source failure safety | PASS | PASS only after existing Planner selection | full remains first confirmation |
| Target readiness | PASS | PASS; exact selected target is rechecked | retained as comparison/future primitive |
| Stale, unknown or conflict | PASS, broad recheck | STOP_SAFE or full comparison | no shortcut permitted |
| Recovery and flap | PASS | same existing Planner/Matrix rules | no threshold change |
| Probe work | 14 checks per channel | controlled 3-service profile | subset is materially cheaper when legally callable |
| First detection time | existing caller is before selection | selection arrives after full lifecycle | subset cannot currently reduce first detection |
| Scale and mutation safety | 3k/60, 5k/100 and 10k/100 Polygon PASS | controlled caller receipt PASS | no route/client action in either path |

The critical distinction is causal ordering, not code quality: the existing
Planner can select a source and target only from current canonical Matrix and
suitability facts. Running its subset before that fact exists would use stale
or invented selection and violate the fail-closed contract. The deployed
shadow path therefore improves evidence and safety without falsely claiming a
current switching-time improvement.

## Rejected interpretations

- **Do not enable automatic FAST now.** The evidence proves a controlled
  comparison, not a lawful pre-full selection source.
- **Do not add a pre-selector, watcher, registry or schedule.** That would be
  a new health/control owner and contradict the Mission.
- **Do not remove the full Matrix.** It is the final canonical result in the
  comparison and the safe live fallback.
- **Do not count Polygon timing as production time.** It bounds behaviour and
  probe work only.

## Exact next action

Extend the existing OMP/CPS atomic-consumption owner — not a new owner — to
accept this bounded Phase-E result, verify its report/evidence identity and
project the exact `TARGET_ARCHITECTURE_REFINED_EXISTING_OWNER_VARIANT` with
automatic FAST still held. Only after that durable terminal is consumed may
Phase G evaluate serial cross-channel traversal at caps 1, 2 and 4 on a
controlled Polygon. No automatic FAST consumer is part of either step.
