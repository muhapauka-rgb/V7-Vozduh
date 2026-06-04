# PROGRAM OPERATOR DECISION SURFACE AND ACTION WORKFLOW IMPLEMENTATION REPORT

Project: V7 Vozduh  
Branch: Updatesystem  
Workspace: `/Users/ponch/Documents/New project`  

## Mission Result

Implemented the first production Operator Decision Surface inside the existing V7 admin UI.

The implementation is intentionally bounded:

- read-only recommendation surface;
- no new planner;
- no new governance;
- no new execution path;
- no new rollback owner;
- no direct user movement from the new recommendation UI;
- no duplicate recommendation engine;
- no duplicate truth source.

## DISCOVER -> REUSE -> EXTEND -> MERGE -> IMPLEMENT

### Discovered Existing Ownership

- Existing admin UI: `admin/v7-admin-api`
- Existing operator read model: `admin_core/operator_views.py`
- Existing operator observability and previews: `admin_core/operator_observability.py`
- Existing approval preview: `/api/operator/approval-preview`
- Existing governance preview: `/api/operator/execution-governance-preview`
- Existing rollback preview: `/api/operator/rollback-preview`
- Existing intelligence snapshots: `admin_core/intelligence_snapshots.py`
- Existing safe deploy allowlist: `tools/v7_sync_lib.py`
- Existing audit writer: `audit_admin` -> `v7-audit-log`
- Existing evidence and closure stores: `EVIDENCE_STORE_FILE`, `CLOSURE_STORE_FILE`

### Reused

- `best-available-pool`
- `candidate-suitability-summary`
- `prediction-summaries`
- `trust-summaries`
- `trust-evolution-summaries`
- `channel-service-scores`
- existing operator approval/governance/rollback previews
- existing admin table/drawer UI patterns
- existing configurable table columns
- existing safe deploy allowlist validation

### Extended

- Added read-only helper: `admin_core/operator_decision_surface.py`
- Added GET endpoint: `/api/operator/decision-surface`
- Added action endpoint: `/api/actions/recommendation-ignore`
- Added user table columns:
  - Current channel remains the existing channel column.
  - Recommended channel.
  - Operator decision state.
- Added channel table column:
  - Channel state.
- Added user recommendation drawer.
- Added channel state drawer.
- Added batch recommendation preview drawer.
- Added ignore fingerprint behavior.
- Added tests for snapshot-derived recommendation, missing snapshot fail-closed behavior, fingerprint changes, and no execution/write imports.

## User Surface

The user table now exposes:

- current channel;
- recommended channel;
- operator state: OK / Recommendation / Warning;
- calm highlight when current channel differs from the recommendation;
- click-through drawer explaining why.

The user recommendation drawer shows:

- user;
- current channel;
- recommended channel;
- confidence;
- expected improvement;
- risk;
- trust;
- prediction;
- reasons;
- Decision -> Action chain.

## User Actions

### Ignore Recommendation

Implemented as `/api/actions/recommendation-ignore`.

It:

- stores ignored recommendation fingerprint;
- writes audit;
- writes evidence;
- writes closure;
- hides only the current fingerprint in the browser UI;
- does not suppress future recommendations;
- lets highlight return when the recommendation hash changes.

Runtime mutation: false.  
Users moved: 0.

### Move User

The new recommendation drawer does not call `/api/actions/user-switch`.

Instead it opens a preview-only workflow:

Recommendation -> Approval Packet -> Snapshot Gate -> Restore Barrier -> Rollback Packet -> Governance -> Execution -> Audit -> Closure

Execution remains owned by existing governed execution path.

### Apply Best Recommendations

The toolbar button opens a batch preview only.

It shows:

- users to move;
- source -> target groups;
- blast radius;
- rollback readiness;
- confidence;
- risk;
- required workflow.

It does not move users.

## Channel Surface

The channel table now exposes a Channel State column:

- Excellent
- Good
- Warning
- Degraded

The channel state drawer shows:

- channel;
- state;
- users;
- capacity;
- stability;
- risk;
- trust;
- prediction;
- Telegram / YouTube / Instagram / ChatGPT service state when snapshot data exists;
- reason for the state.

## Decision To Action Matrix

| Decision | Action | Runtime Mutation |
| --- | --- | --- |
| Ignore recommendation | Audit/evidence/closure fingerprint; hide current fingerprint | false |
| Move user | Open approval/governance/rollback preview | false |
| Apply best recommendations | Open batch preview | false |
| Recommendation changed | New hash restores highlight | false |
| Recommendation expired | Show conservative warning | false |
| Recommendation rejected | Audit/evidence outcome only | false |
| Recommendation approved | Must use existing governed chain | governed path only |

## Audit Integration

Implemented:

- audit event via `audit_admin`;
- evidence bundle in existing evidence store;
- closure record in existing closure store;
- no silent ignore action.

## Performance Certification

The decision helper uses a request snapshot foundation: registries, runtime state, and intelligence snapshots are loaded once per admin request and then transformed into UI rows.

Evidence:

- `operator_surface_evidence/performance_summary.md`

## Duplication Audit

No duplicate planner, governance, execution, rollback, recommendation engine, runtime truth, or snapshot root was created.

Evidence:

- `operator_surface_evidence/safety_duplication_audit.md`

## Regression

PASS:

- py_compile: admin and new helper
- focused unit tests
- full unit suite: 300 tests
- endpoint inventory generated
- deploy allowlist validation PASS after adding the new module to approved deploy files

Evidence:

- `operator_surface_evidence/test_summary.md`
- `operator_surface_evidence/endpoint_inventory.json`

## Files Changed

- `admin/v7-admin-api`
- `admin_core/operator_decision_surface.py`
- `tests/unit/test_operator_decision_surface.py`
- `tests/unit/test_operator_observability.py`
- `tools/v7_sync_lib.py`

## Final Verdicts

user_recommendation_surface_implemented=true  
channel_state_surface_implemented=true  
operator_action_workflow_implemented=true  
batch_preview_implemented=true  
audit_integration_complete=true  
decision_action_matrix_complete=true  
ui_matches_existing_design=true  
new_truth_sources_created=false  
duplicate_systems_created=false  
planner_authority_changed=false  
governance_changed=false  
execution_path_changed=false  
rollback_path_changed=false  
tests_pass=true  
SAFE_NEXT_STEP=commit_push_safe_deploy_truth_check_and_browser_verify_admin_surface

