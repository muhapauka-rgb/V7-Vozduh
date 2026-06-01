# PROGRAM Z3.2 Trust Test

## Objective

Test trust degradation, trust changes, policy restrictions, and autonomy response.

## Live Evidence

The live move was constrained to:

- route_class: `GLOBAL_STABLE`
- user: `10.7.0.16`
- target: `awg3`
- budget: `1`

The planner was also invoked with explicit user and target filters, preventing trust-class expansion.

## Existing Coverage

`admin_core/hybrid_approval.py` classifies target trust and policy:

- `RU_SENSITIVE_EXCLUDED`
- `EXECUTION_ONLY`
- `MANUAL_OR_RESERVED`
- `AUTOSWITCH_FORBIDDEN`
- `AUTOSWITCH_ALLOWED`

`tests/unit/test_v7_hybrid_approval.py` verifies that execution-only targets require exact target approval.

`tests/unit/test_v7_users_autoswitch_policy.py` verifies that canary-reserved targets are not used as production failover targets.

## Non-Executed Stress

No live trust degradation or live policy downgrade was injected into production runtime.

## Verdict

- baseline_trust_scope_enforced=true
- exact_user_filter_enforced=true
- exact_target_filter_enforced=true
- live_trust_degradation_injected=false
- trust_handling_certified=false

