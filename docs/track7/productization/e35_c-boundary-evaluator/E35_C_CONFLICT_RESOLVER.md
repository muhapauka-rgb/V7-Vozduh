# E35.C Conflict Resolver

## Purpose

Multiple authorities may disagree.

The resolver produces one deterministic outcome.

## Inputs

- proposed action;
- boundary evaluator intermediate results;
- conflict category;
- authority domains involved;
- policy rules;
- review policy;
- emergency context.

## Output

```json
{
  "conflict_detected": true,
  "conflict_type": "OPERATOR_PIN_VS_GROUP_EXCLUDE",
  "outcome": "REVIEW_REQUIRED",
  "winning_domain": "GROUP",
  "losing_domain": "OPERATOR",
  "reason": "target_not_allowed_by_group",
  "next_safe_action": "operator_review"
}
```

## Required Conflict Outcomes

| Conflict | Outcome |
|---|---|
| Operator pin vs Group exclude | `DENY` or `REVIEW_REQUIRED` according to group override policy. |
| Operator pin vs Required Services hard fail | `EMERGENCY_ONLY` if current pinned target unsafe; otherwise `DENY`. |
| Operator pin vs Safety | `DENY` forward; containment may be `EMERGENCY_ONLY`. |
| Operator pin vs Containment | `EMERGENCY_ONLY` if trigger valid. |
| Autoswitch vs Governance | `DENY` if governance missing/stale/out-of-scope. |
| Group vs User Intent | Group wins; user intent becomes proposal/review input. |
| Scheduler vs Operator | Operator wins unless governance override exists. |
| Proposal vs Authority | Authority wins. |
| Speed/score vs Boundary | Boundary wins. |

## No Ambiguity Rule

If conflict type is unknown:

```text
REVIEW_REQUIRED
```

Never ALLOW unknown conflict.

## Admin Surface

Show:

- conflict type;
- domains involved;
- winning domain;
- reason;
- next safe action.

## Tests

- every known conflict has deterministic outcome;
- unknown conflict returns `REVIEW_REQUIRED`;
- conflict resolver never mutates runtime;
- conflict event is generated.

## Verdict

```text
conflict_resolver_defined=true
```
