# Ordinary recovery: execution-window identity repair

## Scope

Real V7 Runtime evidence showed that the automatic ordinary recovery path for
the two current users on the failed `vless` source reached Candidate, Packet,
Lease and the bounded cohort executor without any Codex route action.  It then
stopped before the first route mutation with
`core_primary_cohort_projection_contained`.

## Root cause

One automatic recovery transaction carries two legitimate identifiers:

- the durable L3 recovery/checkpoint identifier;
- the exact Packet-bound operation identifier used by the existing execution
  control and Core-primary owners.

The outer governed apply correctly opened and validated the second identifier.
The Core-primary cohort helper then re-read the first identifier for its member
control check and its atomic commit.  The existing fail-closed control owner
therefore rejected the mismatched operation before any user was moved.

## Change

`tools/v7-users-autoswitch` now passes the already accepted Packet-bound
execution operation identifier into the existing Core-primary cohort helper.
The helper continues to keep the L3 identifier for its checkpoint, but uses the
execution-window identity for its per-member control check, Core-primary commit
and matching rollback.  No owner, queue, registry, Matrix, target-selection
rule, authority scope, route writer or manual recovery path was added.

## Verification

- Focused regression for distinct durable and execution identifiers: PASS.
- `tests.unit.test_v7_health_fast_deadline_loop`: 25 PASS.
- Broader `tests.unit.test_service_failure_automation_evolution`: 128 ran;
  15 errors and 3 failures are pre-existing fixture/environment incompatibilities
  (fixture planners missing normal runtime attributes, local HTTP bind denied,
  and current CPS functional-footprint mismatch).  They do not exercise this
  changed identity handoff.  They remain visible and are not waived as evidence.

## Runtime result before this repair

The live Runtime itself, not Codex, selected `awg0` for `10.7.0.126` and
`10.7.0.127`, created bounded operations, and stopped safely with zero route
mutations.  This proves the defect is in the final common execution handoff,
not in health detection or target selection.

## Next step

Run the existing safe-deploy gate.  If it admits deployment, deploy this narrow
repair, restart only the existing health service so its in-process Matrix
consumer loads it, and observe the next normal V7 recovery cycle.  Credit a
result only if the Runtime independently performs the complete automatic chain
and exact service verification; do not manually move either user.
