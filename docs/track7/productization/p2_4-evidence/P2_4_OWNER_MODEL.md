# P2.4 Owner Model

## Result

owner_model_implemented=true

## Owners

| Gate | Owner |
| --- | --- |
| authority | Authority Layer |
| evaluator | Evidence / Proposal |
| conflict_resolver | Authority Layer |
| runtime_trust | Runtime Governance |
| release_trust | Release Governance |
| required_services | Routing Policy |
| capacity | Capacity Program |
| policy | Routing Policy |
| concurrency | Execution Control Plane |
| restore_settle | Autoswitch Safety |
| selected_moves | Autoswitch Safety |
| hidden_movers | Autoswitch Safety |
| target_readiness | Channel Owner |
| routing_mode | Operator / User Routing |
| containment_state | Rollback / Containment |
| group_constraints | Operator / Group Policy |

## API

`GET /api/execution/readiness/owners` returns grouped owner counts for blockers, review-required gates, unknown gates, and passing gates.
