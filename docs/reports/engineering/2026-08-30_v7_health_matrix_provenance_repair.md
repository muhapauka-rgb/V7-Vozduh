# V7 health-origin Matrix evidence: bounded repair prepared

Date: 2026-08-30 (MSK)  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Scope: ordinary VLESS failed-source recovery; no manual operational transition.

## Current live finding

The two ordinary identities on `vless` remain assigned there and their stored
profiles require services which current VLESS probes fail.  The resident
`v7-health.service` is active and its normal `other_required` role is
performing profile checks.  Its current receipt shows four failed VLESS
services and a successful wake of the Matrix consumer.

The failure was not absence of a detector.  Matrix events created by that
resident health process were labelled `EXTERNAL_UNATTRIBUTED`, exactly like an
operator/external capture.  The existing passive/ordinary consumer therefore
preserved them as observation-only material instead of recognising the known
V7 Runtime caller and continuing its normal governed reconciliation.

The Matrix event itself remains capture-only in either case; it never creates
a Candidate, Packet, Lease, Barrier, Authority or route change.

## Repair

The existing health owner now supplies its bounded role identity to its own
Matrix writer child.  The Matrix writer labels only that combination as
`V7_HEALTH_RUNTIME`; direct CLI/other callers remain
`EXTERNAL_UNATTRIBUTED`.

The existing autoswitch provenance contract accepts the known health-origin
observation for ordinary current-profile reconciliation.  It still denies it
natural-production credit and leaves every existing Authority, target,
Packet/Lease/Barrier, mutable validation, route-writer and S11 gate intact.
No owner, timer, queue, registry, state file, planner or route writer was
added.

## Verification before deploy

* Matrix writer provenance test: health-owned emission is labelled
  `V7_HEALTH_RUNTIME` while remaining capture-only and execution-forbidden.
* Profile-required event admission test: both historic external and the
  known V7 health provenance require the same current Matrix/source/profile
  match.
* `tests.unit.test_v7_health_fast_deadline_loop`: 25 checks passed.
* Focused writer/profile checks: 27 checks passed.
* `tests.unit.test_v7_users_autoswitch_policy` and
  `tests.unit.test_operator_execution_packet`: 341 checks passed.
* Python compilation of all changed Runtime files passed.

## Next action

Publish and deploy this bounded repair through `tools/v7-safe-deploy`, verify
local/GitHub/Runtime alignment, then observe only the ordinary V7 health
caller.  A valid result requires V7 itself—not Codex—to recreate the governed
transaction and either complete required-service S11 for the two affected
members or surface the next exact generic safety blocker.
