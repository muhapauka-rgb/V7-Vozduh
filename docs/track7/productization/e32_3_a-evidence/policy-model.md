# E32.3.A Policy Model

policy_model_defined=true

## Definition

A policy is versioned governance decision logic that evaluates whether a proposed action is allowed, denied, requires review, or requires additional gates.

Policy is not runtime mutation.

## Authority Position

```text
policy_is_authority=false
policy_is_runtime_mutation=false
policy_is_admission_logic=true
```

Policy contributes to admission decisions but cannot execute movement by itself.

## Admission Formula

Admission requires:

```text
policy_decision
  + capacity_gates
  + batch_scope
  + runtime_gates
  + approval_packet
  + execution_time_recheck
  + operator_confirmation_if_required
  -> admission_decision
```

## Admission Decisions

Policy may produce:

```text
ALLOW
DENY
REQUIRE_REVIEW
REQUIRE_ADDITIONAL_GATE
NOT_APPLICABLE
CONFLICT
```

Only `ALLOW` from applicable policies can contribute to admission.

Any hard `DENY` overrides allow.

## Policy Boundary

Policy can decide:

- whether a batch type is allowed;
- whether a target class is sufficient;
- whether risk is acceptable;
- whether operator role is sufficient;
- whether scheduling window is allowed;
- whether rollback/containment is allowed;
- whether route classes are eligible.

Policy cannot:

- mutate registries;
- move users;
- alter route tables;
- bypass capacity gates;
- bypass execution-time recheck;
- override rollback exact-scope requirements;
- consume approval packets.

## Model Verdict

Policy model is defined as fail-closed admission logic, not execution authority.
