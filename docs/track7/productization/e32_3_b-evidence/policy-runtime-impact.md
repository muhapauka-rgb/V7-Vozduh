# E32.3.B Policy Runtime Impact

policy_runtime_impact_defined=true

## Principle

Policy may affect runtime eligibility, but policy must not directly mutate runtime.

```text
policy_is_runtime_mutation=false
```

## What Policy May Affect

### Execution Eligibility

Policy may set:

```text
execution_eligibility=ALLOW_OR_DENY_OR_REVIEW_OR_GATED
```

It cannot execute movement.

### Scheduler Admission

Policy may allow or deny scheduler admission.

It cannot enqueue or execute the batch by itself.

### Batch Eligibility

Policy may determine whether a batch type, budget, scope, or lifecycle state is eligible.

It cannot mutate batch metadata after approval.

### Target Eligibility

Policy may deny use of a target based on:

- capacity class;
- capacity status;
- route class;
- target role;
- production-pool state.

It cannot change target metadata.

### Rollback Eligibility

Policy may allow exact-scope rollback or require containment review.

It cannot expand rollback scope.

### Operator Actions

Policy may require:

- operator role;
- dual confirmation;
- human review;
- emergency confirmation.

It cannot impersonate operator approval.

## What Policy Must Not Affect Directly

Policy must not:

- edit `users.registry`;
- edit route tables;
- run movement commands;
- apply autoswitch;
- mutate kill-switch controls;
- consume approval packets;
- bypass runtime gates.

## Runtime Impact Verdict

Policy runtime impact is defined as eligibility and admission impact only.
