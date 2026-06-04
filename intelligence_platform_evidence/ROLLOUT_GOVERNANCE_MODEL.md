# ROLLOUT_GOVERNANCE_MODEL

Implemented in:

- `admin_core/intelligence_platform.py::rollout_governance_model`

## Levels

- `shadow_only`
- `operator_visible`
- `advisory_only`
- `advisory_weighted`
- `bounded_influence`
- `future_production_influence`

## Requirements

Each level requires:

- tests pass;
- fresh snapshots;
- confidence above floor;
- no authority conflict;
- governance unchanged;
- planner owner unchanged;
- runtime mutation false.

## Rollback Rules

- disable/ignore snapshot family;
- revert weight version;
- operator review.

## Verdict

```text
rollout_governance_implemented=true
```

