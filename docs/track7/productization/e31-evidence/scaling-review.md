# E31 Scaling Review

scaling_progression_valid=true

## Progression

| Scale | What scaled cleanly | What became harder | Stable controls |
| --- | --- | --- | --- |
| 1 | Approval packet, exact user match, rollback, replay denial | Initial target quality and dead profile acquisition | Fail-closed gates, restore-settle, runtime checkers |
| 2 | Blast radius and rollback manifest expanded deterministically | Capacity metadata needed requalification from 1 to 2 | Execution-only isolation, selected moves zero |
| 4 | Small cohort rollback and audit expanded cleanly | Capacity metadata needed requalification from 2 to 4 | Readiness, delayed monitoring, hidden mover scan |
| 10 | Candidate-pool normalization, capacity metadata, forward/rollback expanded to 10 | Candidate availability and operational evidence volume increased | Runtime checkers, restore-settle, replay denial, autoswitch exclusion |

## Scaling Findings

- Governance semantics scaled cleanly from 1 to 10 users.
- Capacity metadata changes were governance limits, not proven real throughput limits, through the 10-user target-local validation and long-window checks.
- Rollback remained deterministic because all certified cohorts used rollback target `1`.
- Evidence volume and operator procedure length increased materially at 10 users.
- Larger cohorts are now more likely to be limited by operations, batching, audit ergonomics, and concurrency controls than by the basic approval/recheck/rollback model.

## Conclusion

The scaling progression from 1 to 2 to 4 to 10 is valid. The certified capacity class is now `10_users`; execution scale above 10 remains unproven.
