# P2.9 Retention And Log Growth Risk Audit

Project: V7 Vozduh
Branch: `v7-next`
Mode: Read-only audit
Date: 2026-06-01

## Retention Boundary

Existing retention markers remain visible:

- `HARDENING_RETENTION_DAYS`
- freshness TTLs for evidence, proposals, runtime trust, release trust, and execution
- `CLOSURE_STORE_FILE`
- closure states: `OPEN`, `VERIFIED`, `CLOSED`, `EXPIRED`
- maintenance/log surfaces under security/log maintenance APIs

## Growth Findings

No new infinite-growth store was found for candidate/review/approval/governance/rehearsal/dry-run
workflow data.

Existing stores that still require normal retention discipline:

- `AUDIT_FILE`
- `EXECUTION_EVENTS_FILE`
- `EVIDENCE_STORE_FILE`
- `PROPOSAL_STORE_FILE`
- `RUNTIME_TRUST_STORE_FILE`
- `RELEASE_TRUST_STORE_FILE`
- `CLOSURE_STORE_FILE`
- repository evidence/report archive used by operator observability

## Recommendation

Runtime Dry-Run Architecture should continue using derived previews or existing stores. If it needs a
new store later, it must define TTL, archive, compaction, cleanup, and closure semantics before write
paths are introduced.

retention_log_growth_risk=LOW
event_log_growth_risk=LOW
infinite_growth_store_found=false
