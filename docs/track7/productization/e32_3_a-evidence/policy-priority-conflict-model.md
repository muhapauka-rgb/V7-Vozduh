# E32.3.A Policy Priority And Conflict Model

policy_priority_model_defined=true
policy_conflict_model_defined=true

## Priority Rules

### Deny Overrides Allow

```text
hard_deny_overrides_allow=true
```

No allow decision can override a hard safety denial.

### Safety Overrides Optimization

Safety policies override:

- optimization policies;
- scheduling preferences;
- balancing preferences;
- convenience rules.

### Rollback Containment Exception

Rollback containment may override a forward block only when:

```text
exact_scope_known=true
blast_radius_expansion=false
rollback_target_valid=true
```

This does not allow new forward movement.

### Emergency Policy Rules

Emergency policies may allow containment under stricter audit and human-review rules.

Emergency policies cannot:

- bypass exact scope;
- bypass audit;
- expand blast radius;
- bypass replay denial.

## Conflict States

```text
NO_CONFLICT
SOFT_CONFLICT
HARD_CONFLICT
UNRESOLVED_CONFLICT
```

### NO_CONFLICT

Policies agree or only non-overlapping policies apply.

### SOFT_CONFLICT

Policies disagree on optimization, scheduling, or preference but no safety rule is violated.

Default:

```text
require_review=true
```

### HARD_CONFLICT

At least one safety, capacity, rollback, scope, or audit policy denies an action that another policy allows.

Default:

```text
admission=DENY
```

### UNRESOLVED_CONFLICT

Policy applicability, priority, or source of authority cannot be determined.

Default:

```text
admission=DENY_FOR_FORWARD
human_review_required=true
```

## Conflict Representation

Conflict record must include:

- policies involved;
- action context;
- winning decision;
- losing decision;
- priority reason;
- required operator action;
- audit lineage.

## Priority And Conflict Verdict

Policy priority and conflict model is defined and fail-closed.
