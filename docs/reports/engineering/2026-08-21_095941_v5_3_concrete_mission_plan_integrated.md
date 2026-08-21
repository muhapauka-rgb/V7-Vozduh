# V5.3 T0–T11 — concrete Mission plan integrated into the Program

Date: 2026-08-21 09:59 MSK  
Mission: `V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION`  
Change class: Program/state documentation; no production mutation.

## Request handled

The supplied A–G working plan was incorporated into the existing
`V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM.md`. It is now the durable
execution plan for the switching-time objective, so later work cannot drift
into isolated Matrix tests or unconnected microsteps.

The supplied plan was retained where it adds concrete gates, but reconciled
with the already accepted anti-confirmation-bias rule:

```text
baseline → bottleneck/pattern synthesis → candidates
→ common Polygon/scale tournament → architecture decision
→ implementation → before/after → production proof
```

Therefore the former architecture result is historical candidate evidence. It
is not silently restored as a winner before the tournament.

## Durable stages now recorded in the Program

### A — unified baseline and provenance

One table covers CPS/OMP, Runtime snapshot, production version, Matrix
timer/service/caller, last full cycle, T0–T11 order, deployed selectors and
evidence class. Engineering/Polygon work may continue while deploy-grade
provenance is open; implementation and production claims may not.

### B — mature-system synthesis and candidate formation

Existing Envoy, HAProxy, Google Cloud, FRR/BFD, Cisco, Fortinet and MikroTik
research is reused. Each proven bottleneck receives a mechanism, existing V7
owner, `REUSE/ADAPT/REJECT` disposition and falsifiable Polygon measurement.
Distinct A/B/C candidates are formed without a preselected winner.

### C — ordinary-failure path

The full governed path is tested for every candidate, from T0 through Matrix,
Planner source/target selection, service subset, full fallback, decision,
Candidate, Packet, Lease, Barrier, Apply, verification and T11 recovery. It
starts with one synthetic client and bounded ordinary-like scope. Stale,
unknown, conflict, recovery/re-admission, scope separation and short/full
disagreement are explicit safety cases.

### D — Polygon and scale tournament

The same failure matrix and result schema are used at 7, 50, 100 and 1,000
egresses. Required outputs include latency, probe count, agreement,
false-positive/negative, recovery, stale/conflict, target readiness,
CPU/RAM/network, lock pressure, timeout budget, complexity and safety. Cross-
egress concurrency is measured, not assumed to be the solution.

### E — decision and implementation

Only after B–D are consumed does Phase E select one architecture. The
implementation residual remains the existing exact service-subset and exact
egress-selection connection to the refresh-all fast source/target path. The
sequence is shadow → controlled synthetic → bounded scope → production-safe
observation → limited production application, with full fallback and rollback.

### F — before/after proof

The old and new paths are compared using one method across T0–T11, detection,
decision, execution, probe count, agreement, target readiness, FP/FN,
resource/lock pressure, recovery, client traffic and rollback. Polygon-only
gain is not called production gain.

### G — production evidence and closure

Only natural ordinary failure or read-only production observation plus
controlled evidence is used. No production failure is manufactured. Closure
requires T0–T11, before/after, equivalence, target readiness, client recovery,
fallback preservation, residual classification, CPS/OMP consumption and an
exact successor or lawful terminal.

## Current position

Stage A is bounded: the measured baseline is sufficient for Engineering, while
deploy-grade provenance remains a separate gate. Stage B is the active block:
produce the bottleneck-to-mature-system synthesis matrix and candidate inputs.
Stage C begins only after those inputs and the common tournament harness are
ready. No code, timer, Matrix owner, Runtime, route or client changed in this
turn.

## Verification

- Existing Program updated in place; no new Program, Mission, owner, queue,
  watcher, registry or truth source.
- `git diff --check` passed.
- `python3 tools/v7-truth-check --continue-omp --json` passed: Mission and
  exact next action retained; authority, Runtime, routing and user movement
  effects are all zero.
- Production, routing, Runtime and Authority effects: none.
