# P2.7 Candidate Governance Mapping

## Mapping

Candidate data is mapped into the existing Execution Governance Preview through a derived read model:

- API: `GET /api/execution/candidate-governance`
- Implementation: `admin/v7-admin-api`
- Canonical governance source: `operator_execution_governance_preview(operation_id)`
- Operation id: derived from candidate id

## Exposed Fields

The mapping exposes governance readiness, authority readiness, boundary readiness, review requirements, blocking conditions, dual confirmation, replay protection, execution denial, and disabled actions.

## Storage

No governance store or second workflow is created.

## Verdict

candidate_governance_mapping_implemented=true
existing_implementation_reused=true
parallel_systems_created=false
