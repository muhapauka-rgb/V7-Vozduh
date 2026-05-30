# E32.3.B Policy Evaluation Model

policy_evaluation_defined=true

## Evaluation Outcomes

Policy evaluation may return:

```text
ALLOW
DENY
REVIEW_REQUIRED
ADDITIONAL_GATES_REQUIRED
```

Internal evaluation may also produce:

```text
NOT_APPLICABLE
CONFLICT
ERROR
```

These internal outcomes must be resolved into a final admission-compatible result.

## Evaluation Inputs

Required inputs:

- proposed action;
- batch metadata;
- capacity state;
- runtime gate state;
- approval packet state;
- execution-time recheck state;
- operator identity and role;
- route class;
- production-pool state when applicable;
- active policies;
- policy versions;
- policy scopes;
- policy priorities.

## Evaluation Outputs

Each evaluation must produce:

- decision;
- applied policy ids;
- policy versions;
- matched scopes;
- denied policies;
- required gates;
- conflict status;
- blocked reasons;
- next safe action;
- audit lineage id.

## Evaluation Order

Safe evaluation order:

```text
1. load_active_policies
2. filter_by_scope
3. validate_policy_metadata
4. evaluate_hard_denies
5. evaluate_safety_policies
6. evaluate_capacity_and_batch_policies
7. evaluate_operator_and_route_class_policies
8. evaluate_scheduling_and_production_pool_policies
9. resolve_conflicts
10. produce_admission_decision
```

## Deny Precedence

```text
deny_precedence=true
```

Any hard `DENY` overrides `ALLOW`.

## Safety Precedence

```text
safety_precedence=true
```

Safety policies override optimization, scheduling preference, balancing preference, and convenience policies.

## Review And Gates

`REVIEW_REQUIRED` does not allow execution.

`ADDITIONAL_GATES_REQUIRED` does not allow execution until all named gates pass.

## Evaluation Verdict

Policy evaluation is defined and fail-closed.
