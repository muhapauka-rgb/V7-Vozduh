# P2.7 Candidate Rehearsal Mapping

## Mapping

Candidate data is mapped into the existing Execution Rehearsal Preview through a derived read model:

- API: `GET /api/execution/candidate-rehearsal`
- Implementation: `admin/v7-admin-api`
- Canonical rehearsal source: `operator_execution_rehearsal_preview(operation_id)`
- Simulation source: P2.5 outcome, validation, verification, and rollback previews

## Exposed Fields

The mapping exposes dry-run preparation, execution assumptions, validation assumptions, verification assumptions, rollback assumptions, rehearsal matrix, rehearsal timeline, runtime recheck model, and immutable audit rehearsal preview.

## Storage

No dry-run packet store or second rehearsal system is created.

## Verdict

candidate_rehearsal_mapping_implemented=true
existing_implementation_reused=true
parallel_systems_created=false
