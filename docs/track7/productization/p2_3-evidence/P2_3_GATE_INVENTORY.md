# P2.3 Gate Inventory

## Result

gate_inventory_complete=true

## Inventory

| Gate | Type | Hard/soft | Current behavior |
| --- | --- | --- | --- |
| authority | reference gate | hard | PASS when proposal reference exists, FAIL when missing |
| evaluator | evidence gate | hard | PASS when evidence reference exists, FAIL when missing |
| conflict_resolver | conflict gate | hard | PASS unless capacity conflict fails closed |
| runtime_trust | trust gate | hard | PASS on RUNTIME_OK, FAIL on RUNTIME_BLOCKING, otherwise REVIEW_REQUIRED |
| release_trust | trust gate | hard | PASS on release OK, FAIL on release drift, otherwise REVIEW_REQUIRED |
| required_services | service gate | soft | PASS when required services are healthy, FAIL when failing, REVIEW_REQUIRED when missing |
| capacity | capacity gate | hard | PASS when target has sufficient hard_limit, FAIL when exceeded/missing |
| policy | admission gate | hard | PASS when policy state is readable, REVIEW_REQUIRED for observation-only drafts |
| concurrency | lock gate | soft in preview | FAIL if active stored execution contracts conflict |
| restore_settle | runtime safety gate | hard | PASS when settled, FAIL on expired uncleared barrier, REVIEW_REQUIRED if active/missing |
| selected_moves | hidden mutation gate | hard | PASS when selected_moves=0, FAIL when selected moves exist |
| hidden_movers | hidden movement gate | hard | PASS when no selected moves and no recent switch events |
| target_readiness | target gate | hard | PASS when egress runtime readiness is enable-ready |
| routing_mode | route truth gate | hard | PASS when all affected users are known in users.registry |
| containment_state | rollback gate | hard | PASS when rollback manifest is complete |
| group_constraints | group gate | soft in preview | REVIEW_REQUIRED until dedicated group policy adapter exists |

## Current runtime preview result

remaining_unknown_gates_count=0

Current readiness is NOT_READY because concrete gates fail closed instead of remaining unknown:

- conflict_resolver
- capacity
- target_readiness

Current review-required gates:

- runtime_trust
- release_trust
- required_services
- policy
- hidden_movers
- routing_mode
- group_constraints
