# Program F2 Autonomy Reliability

Date: 2026-06-01
Status: NOT_CERTIFIED

Autonomy reliability was not tested through live movement because autonomous execution did not start.

Fresh planner behavior was consistent in one important way:

- it preserved budget `1`
- it preserved one-user scope
- it preserved rollback target
- it rejected stale target by changing the fresh recommendation

autonomy_reliable=false

