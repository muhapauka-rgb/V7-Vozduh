# EXISTING IMPLEMENTATION REPORT

Project: V7 Vozduh
Block: P2.7
Title: Candidate Review, Approval And Dry-Run Workflow

## Conflict Decision

existing_implementation_found=true

The mandatory implementation conflict rule is triggered. The repository already contains operator approval, governance, approval-packet, and rehearsal/dry-run-preview implementations. P2.7 implementation must stop here to avoid creating a parallel review/approval/dry-run system.

No P2.7 runtime code, API, UI, execution engine, routing, autoswitch, user movement, or runtime hooks were added.

## Existing Implementations

### Approval Center Preview

- Location: `admin_core/operator_observability.py:1330`
- Entry point: `build_approval_preview(model, repo_root)`
- Owner: Operator Observability / Approval Center
- Truth source: read-only operator view model, generation guard evidence, rollback manifest preview, blast-radius preview, evidence freshness preview, selected movement intent, and repository evidence files
- Behavior: builds schema `e16.approval-preview.v1`; marks approval status as `PREVIEW_ONLY`; exposes disabled execution actions and contract previews for movement approval, generation clearance, rollback manifest, blast radius, and evidence freshness
- API: `admin/v7-admin-api:32551` exposes `/api/operator/approval-preview`
- UI: `admin/v7-admin-api:20476` renders the existing `Approval Center`; `admin/v7-admin-api:20477` renders `operatorApprovalContracts`

### Execution Governance Preview

- Location: `admin_core/operator_observability.py:729`
- Entry point: `execution_governance_preview(repo_root, approval_preview=None, operation_id="")`
- Owner: Execution Governance Preview
- Truth source: approval preview, operation lineage, approval contracts, denial contracts, dual-confirmation requirements, expiry rules, replay rejection rules, rollback-bound execution rules, and audit-contract metadata
- Behavior: builds schema `e19.execution-governance-preview.v1`; keeps `preview_only=true` and `execution_allowed_now=false`; exposes governance contracts and disabled execution actions
- API: `admin/v7-admin-api:32616` exposes `/api/operator/execution-governance-preview`
- UI: `admin/v7-admin-api:20478` renders `operatorExecutionGovernance`; `admin/v7-admin-api:26759` renders governance preview cards

### Execution Rehearsal / Dry-Run Preview

- Location: `admin_core/operator_observability.py:945`
- Entry point: `execution_rehearsal_preview(repo_root, execution_preview=None, operation_id="")`
- Owner: Execution Rehearsal Preview
- Truth source: execution governance preview, operation lineage, approval contracts, runtime-truth snapshots, generation and fingerprint checks, rollback state, containment state, and replay audit expectations
- Behavior: builds schema `e20.execution-rehearsal.v1`; keeps `preview_only=true`, `rehearsal_only=true`, and `execution_allowed_now=false`; produces denial/rehearsal scenarios such as stale approval, stale runtime truth, generation mismatch, changed blast radius, rollback invalidation, replay after rollback, and execution after containment
- API: `admin/v7-admin-api:32621` exposes `/api/operator/execution-rehearsal-preview`
- UI: `admin/v7-admin-api:20479` renders `operatorExecutionRehearsal`; `admin/v7-admin-api:26778` renders rehearsal preview cards

### Operator Approval Preview Facades

- Location: `admin_core/operator_observability.py:1547`
- Entry points:
  - `build_operator_approval_preview(repo_root=None, state_dir=None, event_dir=None, now=None)`
  - `build_operator_execution_governance_preview(operation_id="", repo_root=None)` at `admin_core/operator_observability.py:1576`
  - `build_operator_execution_rehearsal_preview(operation_id="", repo_root=None)` at `admin_core/operator_observability.py:1580`
- Owner: Operator Observability API facade
- Truth source: derived operator view model plus the Approval Center, governance, and rehearsal preview builders
- Behavior: exposes existing preview implementations to the admin API without executing runtime actions
- API: wired into `admin/v7-admin-api` operator routes
- UI: consumed by the existing Operator tab Approval Center

### Approval Packet Validation And Audit

- Location: `admin_core/operator_execution.py`
- Entry points:
  - approval packet schema validation at `admin_core/operator_execution.py:92`
  - dual approval-role validation at `admin_core/operator_execution.py:120`
  - append-only governance/audit helpers at `admin_core/operator_execution.py:239` and `admin_core/operator_execution.py:260`
  - CLI flag `--execute-approval-record` at `admin_core/operator_execution.py:368`
- Owner: Operator Execution Packet / Runtime Governance Audit
- Truth source: `e22.operator-execution-packet.v1` approval packet, recheck inputs, runtime-truth hashes, selected movement hash, dual confirmations, and audit stores
- Behavior: validates approval packets, rejects runtime actions unless explicitly allowed by the packet constraints, checks dual-confirmation roles, rejects replay/staleness, and can append audit/governance records
- API: not a P2.7 read API; this is an execution-packet/audit component
- UI: no new UI should be created over this without an explicit architecture decision
- Safety note: P2.7 must not call the append paths because the block forbids runtime mutation

### Existing Admin Integration

- Location: `admin/v7-admin-api`
- Owner: Admin v2 / Operator tab
- Truth source: operator observability facades
- Behavior: existing `/admin-v2` operator UI already contains Approval Center surfaces and read-only operator preview endpoints
- UI evidence:
  - `admin/v7-admin-api:20469` states the section has no POST actions, no shell commands, and no user movement
  - `admin/v7-admin-api:20476` renders `Approval Center`
  - `admin/v7-admin-api:20477` renders approval contracts
  - `admin/v7-admin-api:20478` renders execution governance
  - `admin/v7-admin-api:20479` renders execution rehearsal

## Differences From P2.7 Target Architecture

- Existing approval and governance are operation-preview centric, not candidate-review centric.
- Existing review workflow does not expose the exact P2.7 state set: `NEW`, `UNDER_REVIEW`, `BLOCKED`, `READY_FOR_APPROVAL`, `APPROVED`, `REJECTED`, `ARCHIVED`.
- Existing dry-run preparation is represented as execution rehearsal/governance preview, not as a P2.7 `Dry-Run Candidate` packet.
- Existing approval audit exists in the execution-packet/audit layer, but parts of that layer can append audit records and are therefore outside P2.7 read-only implementation scope.
- Existing UI lives in the Operator tab Approval Center, while P2.7 asks for candidate-driven review, approval, and dry-run preparation inside existing `/admin-v2` without new top-level sections.
- P2.6 introduced derived execution candidates, but the existing E16/E19/E20 Approval Center has not yet been formally bridged to the P2.6 candidate model.

## Migration Path

Do not create a parallel P2.7 review/approval/dry-run subsystem. Reuse the existing Approval Center and operator observability implementations as the canonical foundation.

Recommended migration path:

1. Define candidate-to-operator-preview adapters over the existing P2.6 candidate model.
2. Derive candidate review state from candidate readiness, blockers, risks, and explanation data instead of introducing a new write store.
3. Map candidate approval summary/detail/reason/evidence/lineage/audit to the existing approval preview and execution governance preview contracts.
4. Map candidate dry-run preparation to existing execution rehearsal preview plus P2.5 outcome/simulation previews.
5. Add read-only candidate-specific API endpoints only as composition/proxy endpoints over the canonical operator observability models.
6. Render candidate review/approval/dry-run surfaces inside the existing `/admin-v2` operator/candidate workflow, without adding a new top-level section.
7. Keep retention aligned with P2.5 by deriving compact preview records from existing stores and avoiding unbounded candidate approval queues.
8. Keep `admin_core/operator_execution.py` audit append paths out of P2.7 until a later block explicitly allows controlled mutation.

## Classification

Reuse:

- `build_approval_preview`
- `execution_governance_preview`
- `execution_rehearsal_preview`
- `build_operator_approval_preview`
- `build_operator_execution_governance_preview`
- `build_operator_execution_rehearsal_preview`
- existing `/api/operator/approval-preview`
- existing `/api/operator/execution-governance-preview`
- existing `/api/operator/execution-rehearsal-preview`
- existing `/admin-v2` Operator tab Approval Center UI

Extend:

- Candidate-specific adapters over P2.6 candidate data and existing operator preview contracts
- Admin UI panels that compose existing Approval Center data with candidate detail, without adding a top-level section
- Read-only API composition endpoints that proxy canonical preview models

Refactor:

- Align naming between candidate lifecycle, approval preview, governance preview, and rehearsal preview
- Normalize review-state vocabulary if the architecture decides P2.7 state names are canonical

Replace:

- None. The existing implementation is broad enough to serve as the foundation.

Do Not Touch:

- runtime execution hooks
- autoswitch apply
- routing apply
- user movement paths
- execution engine
- `admin_core/operator_execution.py` append-only audit/governance mutation paths

## Stop Statement

P2.7 implementation is stopped after the mandatory reality audit because existing implementations are present.

No parallel systems were created.

runtime_mutation_performed=false
routing_changed=false
users_moved=false
autoswitch_apply_run=false
execution_engine_implemented=false
runtime_hooks_implemented=false
