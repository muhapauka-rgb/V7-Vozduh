# Production Validation

Read-only production validation:

- `grep '^ip=10.0.0.2 ' /opt/v7/egress/state/users.registry`
- Result: `ip=10.0.0.2 current=vless table=100 enabled=1`

Read-only production baseline dry-run before deploying this gate:

- `selected_move_count=0`
- `authority_budget_gate=null`
- `apply_requested=false`

Read-only production dry-run after deploying this gate:

- `authority_budget_gate.enabled=true`
- `authority_budget_gate.truth_source=existing_policy_files`
- `authority_budget_gate.runtime_calculation_mode=prepared_state_only`
- `authority_budget_gate.authority_class=CANARY`
- `authority_budget_gate.current_allowed_user_budget=1`
- `authority_budget_gate.next_authority_class=SMALL_BATCH`
- `authority_budget_gate.next_allowed_user_budget=2`
- `authority_budget_gate.selected_moves_before_gate=14`
- `authority_budget_gate.selected_moves_after_gate=1`
- `authority_budget_gate.authority_cap_applied=true`
- `authority_budget_gate.decision=cap_selected_moves_to_authority_budget`
- `apply_requested=false`

Interpretation:

- the previously certified one-user movement remains present;
- this program did not move users;
- this program did not run autoswitch apply;
- the authority gate is deployed and active on production.
