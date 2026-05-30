# E32.3.B Admission Decision Model

admission_decision_model_defined=true

## Admission Inputs

Final admission combines:

- policy evaluation;
- Capacity Program;
- Execution Batch scope;
- approval packet;
- runtime gates;
- execution-time recheck.

## Decision Flow

```text
proposed_action
  -> batch_scope_validation
  -> capacity_gate_validation
  -> policy_evaluation
  -> approval_packet_validation
  -> runtime_gate_validation
  -> execution_time_recheck
  -> final_admission_decision
```

## Required Positive Conditions

Final forward admission requires:

```text
policy_decision=ALLOW
capacity_status=CERTIFIED
batch_scope_valid=true
approval_packet_valid=true
runtime_checkers_ok=true
restore_settle_gate_status=GO
execution_time_recheck_passed=true
selected_moves_count=0
hidden_movers_absent=true
```

## Denial Conditions

Admission denies if:

- any hard policy deny applies;
- any policy conflict is hard or unresolved;
- capacity gate fails;
- batch scope invalid;
- rollback manifest incomplete;
- approval packet expired or mismatched;
- runtime gate fails;
- execution-time recheck fails;
- replay attempt detected.

## Review Conditions

Admission returns `REVIEW_REQUIRED` if:

- soft conflict exists;
- operator role requires confirmation;
- emergency policy is involved;
- risk score exceeds review threshold;
- audit reconstruction is required.

## Additional Gates

Admission returns `ADDITIONAL_GATES_REQUIRED` if:

- capacity recertification required;
- restore-settle refresh required;
- approval packet refresh required;
- dual confirmation required;
- reservation ledger check required.

## Final Admission Verdict

Only a fully resolved positive result can produce forward execution eligibility.

Policy alone cannot authorize movement.
