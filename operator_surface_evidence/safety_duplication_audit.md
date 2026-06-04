# Safety And Duplication Audit

## Reused Existing Ownership

- Recommendations: `candidate-suitability-summary.json`, `best-available-pool.json`
- Prediction: `prediction-summaries.json`
- Trust: `trust-summaries.json`, `trust-evolution-summaries.json`
- Channel/service state: `channel-service-scores.json`, runtime overview data
- Governance preview: existing `/api/operator/execution-governance-preview`
- Approval preview: existing `/api/operator/approval-preview`
- Rollback preview: existing `/api/operator/rollback-preview`
- Audit write: existing `v7-audit-log` through `audit_admin`
- Evidence/closure write: existing `EVIDENCE_STORE_FILE` and `CLOSURE_STORE_FILE`

## No Duplicate Authority

- No new planner.
- No new governance.
- No new execution path.
- No new rollback owner.
- No new recommendation engine.
- No new runtime truth source.
- No direct user movement in the new recommendation action path.

## Decision To Action Rule

- Ignore Recommendation: writes audit/evidence/closure fingerprint only; hides current fingerprint in UI.
- Move User: opens approval/governance/rollback preview; does not call `v7-user-switch`.
- Apply Best Recommendations: opens batch preview only; no batch movement.
- Recommendation changed: recommendation hash changes; highlight can return.
- Recommendation expired/missing: UI stays conservative and snapshot blockers are visible.

