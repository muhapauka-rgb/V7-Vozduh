# REAL_APPLY_REPORT

## Requirement

Execute exactly two approved users through the existing governed path only.

## Evidence

Execution was not authorized:

- no valid planner-selected two-user cohort;
- no approval packet;
- no valid restore barrier;
- selected_moves=0;
- snapshot_stop_required=true.

The available admin apply path was not used because it is too broad for this program's boundary and cannot enforce the exact required fresh planner state and selected user count.

## Verdict

real_governed_apply_executed=false

users_moved=0

only_approved_users_moved=true

Runtime mutation performed: NO

User movement performed: NO

Routing mutation performed: NO
