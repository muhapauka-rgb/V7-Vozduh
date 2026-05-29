# E32.1.5 Target Eligibility Model

runtime_mutation_performed=false
user_movement_performed=false
routing_mutation_performed=false

target_eligibility_model_defined=true

## Eligibility Inputs

Target forward eligibility requires all of:

- `capacity_status=CERTIFIED`;
- capacity freshness valid;
- `capacity_confidence` at or above required threshold;
- readiness GO;
- restore-settle GO;
- runtime checkers OK;
- selected moves zero;
- hidden movers absent;
- target role compatible with execution type;
- hard limit greater than or equal to movement budget;
- active policy cap greater than or equal to movement budget;
- available capacity greater than or equal to movement budget;
- autoswitch/rebalance/production assignment flags compatible with target role.

## Execution-Only Target Rule

For `role=EXECUTION_ONLY`:

- explicit operator/governance movement may use the target;
- autoswitch may not use the target;
- rebalance may not use the target;
- production failover may not use the target;
- target must remain governance-reserved.

## Confidence Requirements

Suggested minimums:

- movement execution: HIGH for certified classes;
- target-local validation only: MEDIUM, not executable;
- production pool: VERY_HIGH or policy-specific equivalent.

## Target Ineligibility

Target becomes ineligible when:

- capacity status is not fresh CERTIFIED;
- readiness is NO-GO;
- restore-settle is not GO;
- runtime checkers fail;
- target is occupied unexpectedly;
- policy cap is below requested movement;
- hard limit is below requested movement;
- isolation flags are broken.

