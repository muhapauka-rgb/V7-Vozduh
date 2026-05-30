# E32.3.A Policy Scope Model

policy_scope_model_defined=true

## Scope Types

Supported scopes:

```text
global
target
capacity_class
batch_type
route_class
operator_role
user_group
production_pool
emergency_only
```

## Scope Matching

Policy applicability is evaluated by matching the proposed action context against policy scope.

Action context may include:

- target id;
- target capacity class;
- batch type;
- route class;
- operator role;
- user group;
- production pool id;
- emergency flag.

## Multiple Scope Combination

Policies may combine scopes using:

```text
AND
OR
NOT
```

Safe default:

```text
combined_scope_requires_all_positive_constraints=true
negative_scope_exclusion_overrides_positive_match=true
```

## Scope Specificity

Specificity order:

```text
emergency_only
operator_role
user_group
route_class
batch_type
target
capacity_class
production_pool
global
```

More specific policy may refine broader policy but cannot override a hard safety denial.

## Ambiguous Scope

If scope is ambiguous:

```text
policy_applicability=UNRESOLVED
admission=DENY_or_REQUIRE_REVIEW
```

For forward movement, unresolved scope denies admission.

Rollback containment may proceed only with exact rollback scope and rollback policy allowance.

## Scope Verdict

Policy scope model is defined and fail-closed.
