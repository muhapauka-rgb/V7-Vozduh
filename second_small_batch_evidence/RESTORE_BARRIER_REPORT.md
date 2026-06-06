# RESTORE_BARRIER_REPORT

## Requirement

Generate fresh restore barrier clearance:

- ALLOW_RESTORE_BARRIER_CLEARANCE
- clearance valid
- not expired

## Evidence

The production planner dry-run reported:

restore_barrier_status=restore_barrier_clearance_generation_expired

Because the snapshot gate also failed, restore clearance could not be treated as execution-ready.

## Verdict

restore_barrier_passed=false

allow_restore_barrier_clearance=false

clearance_valid=false

clearance_not_expired=false

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO
