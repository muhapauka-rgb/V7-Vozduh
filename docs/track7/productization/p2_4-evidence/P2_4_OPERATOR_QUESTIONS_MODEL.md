# P2.4 Operator Questions Model

## Result

operator_questions_model_implemented=true

## Questions

The workflow answers:

- Why is execution not ready?
- What failed?
- Which gates require review?
- Who owns the issue?
- What evidence exists?
- What should happen next?
- Can the operator fix it?
- Must the operator wait?
- Is this runtime, governance, trust, policy, capacity, or channel readiness?

## Read Model

`GET /api/execution/readiness/explain` returns an `operator_questions` list with direct answers derived from readiness, gate results, and P2.4 workflow items.

## Boundary

The model explains preview readiness. It does not create authority and does not execute contracts.
