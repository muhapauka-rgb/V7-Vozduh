# P3.A Truth Source Audit

Project: V7 Vozduh
Block: P3.A Runtime Dry-Run Foundation

## Rule

Dry-run reports must be derived from existing canonical sources. P3.A must not create a new truth source for runtime, routing, user movement, approvals, execution or health.

## Truth Source Matrix

| Domain | Canonical truth source | Derived view | Presentation |
| --- | --- | --- | --- |
| Runtime state | Existing `STATE_DIR` files, registries, service matrix, policy state | `v7-state-json`, admin runtime fingerprint/convergence/drift | Admin runtime/checks views |
| Runtime events | `AUDIT_FILE`, `EVENT_DIR`, `switch-history.jsonl`, observer JSONL files | Normalized event timeline | Admin logs/timeline |
| Service health | `service-matrix.json`, sentinel state, egress summaries | Readiness and required-service gates | Admin checks and execution readiness |
| Trust and authority | Trusted RU diagnostic/decision state, runtime trust store, release trust store | Trust gates and authority verdicts | Governance preview |
| Candidates | Proposal/evidence stores and execution candidate read models | Candidate queue/detail/review previews | Admin execution/review views |
| Approval | P2.7 approval/review state and audit records | Approval summary/detail/evidence/lineage | Admin approval center |
| Execution contract preview | `EXECUTION_CONTRACTS_FILE` | Contract detail and summary preview | Admin execution contract views |
| Execution events preview | `EXECUTION_EVENTS_FILE` | Execution timeline, verification and rollback views | Admin execution timeline |
| Simulation | Derived from candidate, service matrix, blast radius, rollback and readiness adapters | Outcome preview and forecast | Admin execution preview views |
| Rollback preview | Contract rollback manifest plus rollback impact adapter | Rollback preview and verification | Admin rollback preview |
| Observability | Operator observability aggregation over existing state and evidence | Governance/rehearsal/operator view model | Admin operator views |

## Non-Canonical Areas

The following must not become canonical truth sources:

- UI labels or navigation state.
- Generated dry-run reports.
- Cached summaries without source hashes.
- Any hook-local queue.
- Any action-capable autoswitch output.
- Any ad hoc JSON file created only for P3.A.

## Ownership

| Truth family | Owner boundary |
| --- | --- |
| Runtime health and service evidence | Runtime support and observability tools. |
| Candidate/review/approval | Admin preview and P2.7 workflow surfaces. |
| Execution contract/event preview | Existing admin execution preview family. |
| Governance/rehearsal | Operator observability aggregation. |
| Retention | Existing P2.5 retention architecture and cleanup rules. |

## Truth Source Verdict

- Duplicate truth sources found: no blocking duplicate truth source.
- Dangerous parallel systems found for P3.A: none created.
- P3.A model status: derived-only.

`truth_source_audit_complete=true`

