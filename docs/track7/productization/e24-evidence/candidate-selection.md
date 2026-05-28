# E24 Candidate Selection

## Candidate Pool

All enabled users were reviewed from `users.registry`, current route table state, and checker output.

| User | Current | Table | Route Sanity | Rollback Target | Risk |
|---|---|---:|---|---|---|
| 10.0.0.2 | awg3 | 100 | OK | awg3 | legacy subnet, not first choice |
| 10.0.0.3 | awg3 | 101 | OK | awg3 | legacy subnet, not first choice |
| 10.0.0.6 | awg3 | 104 | OK | awg3 | legacy subnet, not first choice |
| 10.7.0.2 | awg3 | 1000 | OK | awg3 | stable but not prior cohort candidate |
| 10.7.0.3 | awg3 | 1001 | OK | awg3 | prior canary user; avoid reusing for first operator path |
| 10.7.0.4 | awg3 | 1002 | OK | awg3 | stable but not prior cohort candidate |
| 10.7.0.5 | awg3 | 1003 | OK | awg3 | stable but not prior cohort candidate |
| 10.7.0.6 | awg3 | 1004 | OK | awg3 | stable but not prior cohort candidate |
| 10.7.0.8 | awg3 | 1006 | OK | awg3 | stable but not prior cohort candidate |
| 10.7.0.9 | awg0 | 1007 | OK | awg0 | was delayed-moved in E11.13; avoid |
| 10.7.0.10 | awg0 | 1008 | OK | awg0 | was delayed-moved in E11.13; avoid |
| 10.7.0.11 | 1 | 1009 | OK | 1 | selected; prior two-user cohort path, clean rollback |
| 10.7.0.12 | 1 | 1010 | OK | 1 | acceptable alternate; reserve as backup |
| 10.7.0.13 | awg0 | 1011 | OK | awg0 | was delayed-moved in E11.13; avoid |
| 10.7.0.14 | 1 | 1012 | OK | 1 | acceptable but less proven |
| 10.7.0.15 | 1 | 1013 | OK | 1 | acceptable but less proven |

## Selected Candidate

```text
candidate_user=10.7.0.11
current_egress=1
rollback_target=1
table=1009
candidate_selection_reason=prior two-user cohort candidate, currently on rollback target 1, route table sane, rollback independent, minimal first operator-driven blast radius
```

Current route evidence:

```text
table_route=default dev v7e356a192b79 scope link
route_get=8.8.8.8 from 10.7.0.11 dev v7e356a192b79 table 1009
```

## Selection Verdict

candidate_user_stable=true for approval-packet design.

candidate_user_stable_for_execution=false until E25 rechecks target-readiness, restore-settle, selected_moves, hidden movers, and route sanity again.
