# PERF.3 RI.4 Recommendation

## Verdict

safe_to_begin_RI4=true

## Reason

Service Intelligence Expansion can now build on snapshot producers instead of running heavy calculations in runtime.

Available foundations:

- canonical snapshot envelope
- read-only snapshot readers
- service score producer
- channel service score producer
- trust summary producer
- risk summary producer
- blast radius producer
- overview summary producer

## RI.4 Recommended Boundary

RI.4 may extend Service Intelligence using snapshots as inputs/outputs.

RI.4 must not:

- integrate snapshots into live runtime decisions without PERF.4
- move users
- write selected moves
- bypass governance
- run service probes inside planner
- scan raw history inside planner

## Next Safe RI.4 Scope

- expand service catalog scoring
- add route-class service score summaries
- add user/group service score producer if needed
- keep planner behavior unchanged until PERF.4
