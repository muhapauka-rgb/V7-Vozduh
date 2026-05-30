# E32.3.B Policy Failure Modes

policy_failure_modes_defined=true

## POLICY_STALE

Detection:

- policy staleness threshold exceeded;
- stale policy source cache.

Impact:

```text
allow=false
```

Operator action:

Refresh policy state or review policy version.

Fail-closed:

Forward admission denied until freshness is restored.

## POLICY_EXPIRED

Detection:

- `now > expires_at`.

Impact:

```text
allow=false
```

Operator action:

Activate a new policy version or remove dependency.

Fail-closed:

Expired policy cannot allow action.

## POLICY_CONFLICT

Detection:

- two or more applicable policies produce conflicting decisions.

Impact:

```text
allow=false_for_hard_or_unresolved_conflict
review_required=true_for_soft_conflict
```

Operator action:

Resolve conflict or choose a higher-priority policy through governance.

Fail-closed:

Forward admission denied on hard/unresolved conflict.

## POLICY_SCOPE_UNKNOWN

Detection:

- action context cannot be matched to policy scope;
- scope expression ambiguous.

Impact:

```text
allow=false
review_required=true
```

Operator action:

Clarify scope or create explicit policy.

Fail-closed:

Forward admission denied.

## POLICY_METADATA_INVALID

Detection:

- missing id/version/status/scope/owner;
- invalid decision mode;
- invalid lifecycle transition.

Impact:

```text
allow=false
```

Operator action:

Repair metadata and re-review policy.

Fail-closed:

Policy excluded from allow path; if required policy invalid, admission denied.

## POLICY_EVIDENCE_MISSING

Detection:

- required capacity, batch, packet, runtime, or audit evidence absent.

Impact:

```text
allow=false
additional_gates_required=true
```

Operator action:

Collect missing evidence or regenerate packet/recheck.

Fail-closed:

No forward admission until evidence exists.

## POLICY_PRIORITY_CONFLICT

Detection:

- two applicable policies share incompatible priority;
- priority source unclear.

Impact:

```text
allow=false
review_required=true
```

Operator action:

Fix priority model or resolve conflict through governance.

Fail-closed:

Forward admission denied.

## POLICY_EVALUATION_ERROR

Detection:

- evaluator error;
- parse failure;
- unsupported policy expression;
- dependency unavailable.

Impact:

```text
allow=false
review_required=true
```

Operator action:

Inspect evaluator error and rerun after repair.

Fail-closed:

Forward admission denied.

## Failure Modes Verdict

Policy failure modes are defined and fail closed.
