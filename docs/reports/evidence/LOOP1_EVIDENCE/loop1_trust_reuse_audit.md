# LOOP.1 Trust Reuse Audit

## Question

Do real governed executions influence trust, and does updated trust influence planner evidence?

## Evidence

FB.2 materialized 16 real execution feedback contracts into existing stores.

Runtime trust visibility:

- all 16 feedback IDs were visible in `/api/runtime/convergence?advanced=1`
- all 16 moved users were visible in runtime/trust evidence

Planner consumption:

- `trust_evolution_advice.available=true`
- `live_calibrated=true`
- `planner_decision_owner=tools/v7-users-autoswitch`
- `execution_authority=none`
- `selected_moves_write_authority=none`

Before/after source hashes changed after materialization and refresh:

- `prediction_actuals`
- `service_actuals`
- `trust_summary`
- `prediction_summary`
- `service_scores`
- `candidate_suitability`
- `best_available_pool`

Confidence values changed:

- overall confidence: `42.471 -> 42.476`
- prediction confidence: `37.276 -> 37.295`
- suitability confidence: `28.328 -> 28.335`
- inherited execution trust: `86.984 -> 86.985`

## Conclusion

Real executions influence trust and planner-facing evidence.

The influence is advisory/planner-evidence influence, not autonomous execution authority.

