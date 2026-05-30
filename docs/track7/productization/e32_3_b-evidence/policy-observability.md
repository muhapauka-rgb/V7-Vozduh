# E32.3.B Policy Observability

policy_observability_defined=true

## Operator View

Operators must see:

- active policies;
- matched policies;
- denied policies;
- policy conflicts;
- review-required decisions;
- additional gates required;
- evidence used;
- final admission result;
- next safe action.

## Required Display Fields

```text
policy_id
policy_version
policy_type
policy_status
policy_scope
policy_priority
decision
conflict_status
blocked_reason
required_gates
evidence_used
next_safe_action
audit_lineage_id
```

## Active Policies

Display active policies that matched the action scope.

Expired, revoked, deprecated, and superseded policies must be visible for audit but not treated as allowing policies.

## Denied Policies

Operators must see every policy that denied the action, including:

- reason;
- scope;
- priority;
- blocking gate;
- override relationship.

## Policy Conflicts

Conflicts must show:

- conflict state;
- involved policies;
- winning decision;
- losing decision;
- human review requirement.

## Review-Required Decisions

Review-required output must show:

- review reason;
- responsible operator role;
- safe next action;
- whether forward execution is blocked.

## Evidence Used

Evidence display should include:

- capacity state;
- batch metadata;
- approval packet state;
- runtime gate state;
- execution-time recheck state;
- audit lineage.

## Observability Verdict

Policy observability is defined.
