# Core-primary stable classes and live-history budget

Date: 2026-08-30  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Mission: `V7_CORE_PRIMARY_STABLE_ROUTE_CLASS_REPAIR_AND_LIVE_7S_RECOVERY`

## Scope and operating law

This work repaired generic Runtime behaviour only. No user assignment, source,
target, Candidate, Packet, Lease, Barrier, route-writer action, incident or
automatic consumer was invoked manually. The live V7 caller remains the only
permitted origin of a recovery transaction.

## Findings and completed repairs

1. Core-primary used the position of occupied egresses as its route class.
   When the last user left one egress, that egress could disappear and the
   remaining classes could be renumbered. This prevented later affected-cohort
   admission. Commit `c35c1e39` extends the existing canonical
   `egress.registry` with stable Core-primary mark/table identities. The
   existing migration owner consumed seven stable classes; Runtime verified all
   128 user classes and all 7 egress classes against the Core-primary map.
   Empty egresses keep their identity but remain ineligible when unhealthy.

2. A completed ordinary operation could remain blocked because the cleanup
   mistook the passive `v7-users-autoswitch` observer for an active route
   writer. Commit `98c0a3df` now distinguishes observers from the two actual
   route-writing entrypoints, allowing the existing Matrix owner to release an
   exact completed-but-unapplied lease safely.

3. During real Runtime observation, `v7-health.service` was killed by the
   kernel for memory use. The cause was an unbounded parse of the append-only
   `closure-records.jsonl` during background closure reconciliation. Commit
   `f426f6aa` restricts that live operation to the existing bounded current
   owner window. It can only republish a no-forward-apply closure successor;
   lack of older history never authorizes routing.

4. A second live background path still parsed the entire execution-outcome
   ledger. Commit `a2524f7b` limits this live reconciliation to the same
   current owner window. The compact L3 state retains already-consumed
   lineage; the immutable full ledger remains available to the existing
   offline/history reader.

## Evidence

- Focused Core-primary, lease-cleanup and bounded-history suite: **17/17
  passed** after the final change.
- Both commits were published to `Updatesystem` and deployed only through
  `tools/v7-safe-deploy`:
  - `deploy-z8-14-Updatesystem-f426f6a-20260830T190959`
  - final deployed fingerprint: `a2524f7b2808ce10510637ee379d077ff5559400`
- Deploy validation reported local/GitHub alignment and no deploy blockers.
- Before the repair, the passive observer reached about **471 MB RSS** and the
  health service had an OOM termination with a **1.1 GB** peak. After the final
  deployment, the same observer was about **70 MB RSS** while active; the
  health service was `active/running`, with zero new restarts in the observed
  post-deploy window.
- Matrix still classified VLESS as degraded (one healthy service of fourteen
  in the last observed complete Matrix record). This does not make VLESS an
  automatic target; it only preserves its stable route class.

## What is not yet claimed

There is no valid new automatic end-to-end seven-second recovery measurement
from this change. The Runtime was previously interrupted by memory exhaustion,
and the current health cycle still shows long service-role runs. Therefore this
report does not credit an S11 result, a client recovery, or the 7-second SLO.

## Exact next step

Leave control with the normal V7 Runtime and observe one fresh profile-required
failure through:

`Matrix -> automatic affected scope -> automatic Authority -> Planner ->
Candidate -> Packet -> Lease -> Barrier -> Apply -> Core-primary -> S11`.

Record first valid failure observation through all-affected S11. If it exceeds
7 seconds or stops, use that Runtime receipt to repair the next generic cause;
do not move a user manually.
