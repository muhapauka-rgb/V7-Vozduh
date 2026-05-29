# E30.2 Denial Semantic Tests

- unauthorized_user: DENY_EXPECTED=true
- unauthorized_target: DENY_EXPECTED=true
- movement_budget_gt_10: DENY_EXPECTED=true
- stale_users_hash: DENY_EXPECTED=true
- stale_egress_hash: DENY_EXPECTED=true
- stale_selected_moves_hash: DENY_EXPECTED=true
- target_not_go: DENY_EXPECTED=true
- target_hard_limit_lt_10: DENY_EXPECTED=true
- missing_confirmation: DENY_EXPECTED=true
- wrong_generation: DENY_EXPECTED=true
- replay_attempt_simulation: DENY_EXPECTED=true

denial_semantics_valid=true
runtime_mutation_performed=false
