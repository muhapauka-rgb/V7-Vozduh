# P2.3 Adapter Discovery

## Result

adapter_discovery_completed=true

P2.3 found usable read-only sources for the main execution validation gates.

## Adapter sources

| Gate | Read-only source | Adapter status |
| --- | --- | --- |
| authority | proposal reference in generated draft | implemented |
| evaluator | evidence reference in generated draft | implemented |
| conflict_resolver | capacity adapter | implemented |
| runtime_trust | runtime convergence model | implemented |
| release_trust | release current model | implemented |
| required_services | service matrix | implemented |
| capacity | egress registry metadata and assigned user count | implemented |
| policy | policy state reader | implemented |
| concurrency | execution contract store | implemented |
| restore_settle | autoswitch restore barrier state file | implemented |
| selected_moves | selected moves state files | implemented |
| hidden_movers | selected moves plus switch-history tail | implemented |
| target_readiness | egress runtime readiness helper | implemented |
| routing_mode | users.registry | implemented |
| containment_state | rollback manifest | implemented |
| group_constraints | users.registry, partial review adapter | implemented as review-required |

## Notes

The group constraints adapter is intentionally conservative. It removes UNKNOWN by using known registry/draft data, but it remains REVIEW_REQUIRED until a dedicated group policy reader exists.
