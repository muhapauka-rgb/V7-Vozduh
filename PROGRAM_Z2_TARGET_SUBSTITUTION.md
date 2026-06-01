# Program Z2 Target Substitution

Date: 2026-06-01

## Verdict

target_substitution_working=true

## Rules Implemented

Policy-approved target substitution is allowed only when all checks pass:

- budget is exactly `1`
- exactly one move is proposed
- user is explicitly allowed by policy
- target route class equals approved route class
- target trust class equals approved trust class
- target policy class equals approved policy class
- target capacity is not `HARD_FULL`
- rollback target equals the user's current egress

Target approval is required when:

- target is execution-only
- target is manual-only or reserved
- autoswitch is forbidden for the target
- route class changes
- trust class changes
- budget is above `1`

## Z2 Validation

Proposal target:

- `awg3`

Target descriptor:

- route class: `GLOBAL_STABLE`
- trust class: `RU_SENSITIVE_EXCLUDED`
- policy class: `AUTOSWITCH_ALLOWED`
- capacity class: `EMPTY`

Result:

- target approval required: `false`
- substitution ok: `true`

## Fail-Closed Coverage

Unit tests verify that an `EXECUTION_ONLY` target is denied under policy approval unless exact target approval is present.

## Safety

- scope_expanded=false
- target_substitution_unbounded=false
- runtime_mutation_performed=false

