# P2.9 Terminology And Status Audit

Project: V7 Vozduh
Branch: `v7-next`
Mode: Read-only audit
Date: 2026-06-01

## Status Vocabularies

Observed canonical status groups:

- Execution contract statuses: `DRAFT`, `PRECHECKED`, `APPROVED`, `SCHEDULED`, `VALIDATED`,
  `RECHECKED`, `EXECUTING`, `VERIFYING`, `OBSERVING`, `ROLLBACK_READY`, `ROLLING_BACK`,
  `COMPLETED`, `FAILED_CLOSED`, `ROLLED_BACK`, `REPLAY_DENIED`, `CANCELLED`, `EXPIRED`
- Candidate lifecycle: `DISCOVERED`, `CANDIDATE`, `VALIDATING`, `READY_FOR_REVIEW`, `BLOCKED`,
  `READY_FOR_CONTRACT`, `ARCHIVED`, `EXPIRED`
- P2.7 review bridge states: `BLOCKED`, `READY_FOR_APPROVAL`, `UNDER_REVIEW`, `ARCHIVED`
- Freshness/closure: `FRESH`, `STALE`, `EXPIRED`, `UNKNOWN`; `OPEN`, `VERIFIED`, `CLOSED`, `EXPIRED`
- Preview-only markers: `PREVIEW_ONLY`, `PREPARED_PREVIEW_ONLY`, `NOT_REQUESTED_PREVIEW_ONLY`

## Findings

Some domain terms overlap semantically, especially `APPROVED` in execution contracts versus
preview-only approval center state. This is not a dangerous duplicate system because the preview
responses carry explicit `preview_only` and `execution_allowed_now=false` flags.

Recommendation for Runtime Dry-Run Architecture: keep dry-run statuses prefixed or scoped as
`DRY_RUN_*` or `PREVIEW_*` until an execution block explicitly authorizes runtime behavior.

terminology_status_duplication_risk=LOW
truth_sources_clean=true
execution_allowed_now=false
