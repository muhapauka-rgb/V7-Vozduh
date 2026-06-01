# P5.1 Truth Source Audit

## Classification

| Domain | Canonical Runtime Truth | Derived Source | Presentation Source |
| --- | --- | --- | --- |
| Users | `/opt/v7/egress/state/users.registry` | `v7-state.json.users` when present | `/api/users`, admin UI |
| Egress | `/opt/v7/egress/state/egress.registry` | egress summaries and runtime readiness views | `/api/egress`, admin UI |
| Selected Moves | live selected-move files under `STATE_DIR` if present; otherwise zero only when explicitly missing in recheck logic | autoswitch plan summaries | operator/admin previews |
| Runtime Hashes | hashes of current runtime files | runtime fingerprint response | `/api/runtime/fingerprint` |
| Health | `summary.state`, `egress-status.state`, `v7-state.json`, service matrix files | runtime convergence/drift model | `/api/runtime/convergence`, `/api/runtime/drift` |
| Capacity | `egress-load.state`, `egress-load-summary.json`, egress registry limits | readiness summaries | admin capacity/readiness views |
| Trust | runtime trust JSONL and trusted RU state files | convergence trust model | runtime trust UI |
| Candidate State | proposal/execution stores under `STATE_DIR` | execution candidate APIs | admin execution pages |
| Execution State | execution contracts/events under `STATE_DIR` | dry-run and verification APIs | admin execution pages |
| Audit State | `/opt/v7/audit/audit.jsonl` and event JSONL | audit search/export previews | admin audit views |
| Observation State | event directory and generated runtime state | observability summaries | operator/admin views |

## Current Certification

The canonical architecture is clear, but fresh live runtime truth is not certified in this environment.

Reasons:

- local `/opt/v7/egress/state` is absent
- unauthenticated runtime APIs return 401
- authenticated API access was not used to avoid session/audit side effects
- old evidence and fixtures were explicitly excluded

## Verdicts

- truth_source_audit_complete=true
- canonical_runtime_truth_model_identified=true
- runtime_truth_source_certified=false
- truth_conflict_found=false
- stale_sources_rejected=true
