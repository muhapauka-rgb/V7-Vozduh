# E32.3.C Fail-Closed Review

fail_closed_behavior_valid=true

## Required Fail-Closed Rules

### Policy Failure Never Allows

```text
policy_failure_never_allows=true
```

Policy failure modes cannot produce `ALLOW`.

### Evaluation Error Denies

```text
evaluation_error_denies=true
```

Evaluator errors deny forward admission.

### Hard Or Unresolved Conflict Denies

```text
hard_or_unresolved_conflict_denies=true
```

Hard conflicts and unresolved conflicts deny forward admission.

### Soft Conflict Requires Review

```text
soft_conflict_requires_review=true
```

Soft conflicts block execution until review is completed.

### Missing Evidence Requires Additional Gates

```text
missing_evidence_requires_additional_gates=true
```

Missing evidence cannot be treated as allow.

### Deny Overrides Allow

```text
deny_overrides_allow=true
```

No allow policy can override a hard safety denial.

### Safety Overrides Optimization

```text
safety_overrides_optimization=true
```

Safety policy beats optimization, scheduling preference, route preference, and convenience policy.

### Rollback Containment Exact Scope

```text
rollback_containment_requires_exact_scope=true
```

Rollback containment may proceed only with known scope and no blast-radius expansion.

## Fail-Closed Verdict

Policy Engine fail-closed behavior is valid.
