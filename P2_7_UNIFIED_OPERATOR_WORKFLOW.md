# P2.7 Unified Operator Workflow

## Flow

P2.7 connects the existing systems into one derived operator flow:

Proposal -> Candidate -> Approval Center -> Governance Preview -> Rehearsal Preview

## API

`GET /api/execution/candidate-workflow`

## UI

The existing `/admin-v2` Operator tab Approval Center now includes a Candidate bridge panel. It does not add a new top-level navigation section.

## Consistency

The workflow checks:

- Proposal to Candidate
- Candidate to Approval Center
- Candidate to Governance Preview
- Governance Preview to Rehearsal Preview
- Single source of truth

Missing proposal lineage fails closed.

## Verdict

unified_operator_workflow_implemented=true
parallel_systems_created=false
