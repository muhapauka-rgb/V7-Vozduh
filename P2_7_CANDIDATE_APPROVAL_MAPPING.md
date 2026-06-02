# P2.7 Candidate Approval Mapping

## Mapping

Candidate data is mapped into the existing Approval Center Preview through a derived read model:

- API: `GET /api/execution/candidate-approval`
- Implementation: `admin/v7-admin-api`
- Canonical approval source: `operator_approval_preview()`
- Candidate source: P2.6 derived candidate model

## Exposed Fields

The mapping exposes candidate readiness, risks, explanation, proposal references, evidence references, authority references, validation state, simulation state, and Approval Center contracts.

## Storage

No approval record is written. No approval queue is created. No approval store is introduced.

## Verdict

candidate_approval_mapping_implemented=true
existing_implementation_reused=true
parallel_systems_created=false
