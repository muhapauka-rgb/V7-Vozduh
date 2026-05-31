# BLOCK P3.A Runtime Dry-Run Foundation Report

Project: V7 Vozduh
Program: P3
Block: P3.A
Mode: Architecture / Discovery / Dry-Run Preparation

## Baseline

- Current branch: `v7-next`
- Local HEAD: `afcdd9cc61b7a1302c8785489991b0eac217b395`
- Prior P2.9 continuation signal: `safe_to_continue_to_runtime_dry_run=true`
- Runtime mutation performed: no
- Deployment performed: no
- Routing changed: no
- Users moved: no

## Reality Audit

Created: `P3A_REALITY_AUDIT.md`

The repository already contains runtime observation, candidate, readiness, approval, governance, rehearsal, simulation, verification and rollback preview surfaces. P3.A must reuse these surfaces instead of creating a parallel runtime system.

Key reuse points:

- Admin execution preview family.
- `admin_core/operator_observability.py`.
- `tools/runtime-support/v7-state-json`.
- `tools/v7-observability-summary`.
- Service matrix and sentinel evidence.
- Trusted RU read-only diagnostic/decision evidence.
- Proxy routing dry-run tools.
- Existing autoswitch evaluator semantics in non-apply mode only.

## Implementation Conflict Audit

Created: `P3A_IMPLEMENTATION_CONFLICT_AUDIT.md`

Adjacent implementations exist and are mandatory boundaries:

- Autoswitch evaluator has apply-capable paths and must be used only as non-apply semantics.
- Telegram sentinel can trigger autoswitch and must be consumed only as observer output.
- Trusted RU decision has optional write-state mode and must be consumed only in read-only form.
- `admin_core/operator_execution.py` has execution-named and append-capable paths and must not become the P3.A dry-run engine.

No parallel runtime system was created.

## Truth Source Audit

Created: `P3A_TRUTH_SOURCE_AUDIT.md`

Dry-run outputs are defined as derived reports over existing canonical sources:

- Runtime state and service evidence from existing state files and service matrix.
- Runtime events from audit/event stores.
- Candidate/review/approval from existing admin preview workflows.
- Contract and execution event previews from existing execution preview stores.
- Governance and rehearsal from operator observability.

Generated dry-run reports must not become canonical truth sources.

## Runtime Audit

Created: `P3A_RUNTIME_AUDIT.md`

Runtime inputs and observability surfaces were mapped. P3.A excludes autoswitch apply, sentinel action triggers, trusted RU write mode, operator execution append/execute paths, service/systemd control, deploy and routing apply.

## Domain Model

Created: `P3A_DRYRUN_DOMAIN_MODEL.md`

Runtime Dry-Run is defined as a derived, non-authoritative decision model. It observes existing runtime evidence and computes what would be recommended, blocked, reviewed or rolled back without executing anything.

## Event Model

Created: `P3A_RUNTIME_EVENT_MODEL.md`

The event model normalizes existing events only. It introduces no new event bus and no runtime hooks.

Core event types include:

- `HEALTH_CHANGE`
- `CHANNEL_DEGRADATION`
- `REQUIRED_SERVICE_FAILURE`
- `CAPACITY_PRESSURE`
- `TRUST_CHANGE`
- `POLICY_CHANGE`
- `SELECTED_MOVES_PRESENT`
- `RESTORE_BARRIER_CHANGE`
- `HIDDEN_MOVEMENT`
- `EXECUTION_CONTRACT_CHANGE`
- `AUDIT_ACTION`
- `ROUTING_TRUTH_CHANGE`

## Decision Model

Created: `P3A_DRYRUN_DECISION_MODEL.md`

Allowed dry-run decisions:

- `NO_ACTION`
- `WOULD_MOVE`
- `WOULD_BLOCK`
- `WOULD_REVIEW`
- `WOULD_ROLLBACK`

Forbidden action decisions:

- `MOVE`
- `APPLY`
- `EXECUTE`
- `ROUTE`
- `AUTOSWITCH_APPLY`

## Contract Model

Created: `P3A_DRYRUN_CONTRACT_MODEL.md`

Dry-run contracts are non-executable snapshots with source refs, hashes, decision reasons, simulations, verification plan, rollback preview, authority flags, expiry and retention class.

They do not replace existing execution contract truth sources and cannot be accepted by an executor.

## Verification Model

Created: `P3A_DRYRUN_VERIFICATION_MODEL.md`

Verification compares dry-run predictions with later observed reality. It verifies model quality and never triggers rollback, routing, movement or autoswitch.

Verification states:

- `NOT_VERIFIED`
- `VERIFIED_MATCH`
- `VERIFIED_MISMATCH`
- `INCONCLUSIVE`
- `STALE`

## Observability Model

Created: `P3A_DRYRUN_OBSERVABILITY_MODEL.md`

Dry-run observability should appear inside existing `/admin-v2` areas only:

- Execution
- Approval Center
- Governance Preview
- Rehearsal Preview
- Checks
- Logs

No new top-level admin section is required.

## Retention Model

Created: `P3A_DRYRUN_RETENTION_MODEL.md`

P3.A follows P2.5 retention architecture:

- Prefer on-demand derived reports.
- Persist only TTL-bound preview records if later blocks require it.
- Store source refs and hashes instead of copied payloads.
- Avoid hook-local queues and unbounded append streams.
- Keep cleanup under the existing retention architecture.

## Certification Readiness

Created: `P3A_CERTIFICATION_READINESS.md`

Status: `READY_WITH_BLOCKERS`

It is safe to continue to Runtime Hook Dry-Run design only if P3.B remains passive, non-authoritative, retention-bound and action-free.

## Risks

| Risk | Level | Mitigation |
| --- | --- | --- |
| Autoswitch apply accidentally reused | High | Use evaluator semantics only; forbid apply calls. |
| Sentinel becomes an action hook | High | Consume sentinel state only. |
| Trusted RU write-state leaks into dry-run | Medium | Use read-only preview only. |
| Dry-run reports become a new truth source | Medium | Keep reports derived and source-referenced. |
| Event normalization grows without bounds | Medium | Use derived views and retention-bound records only. |
| Operator execution boundary confused with dry-run | Medium | Do not use execution/append flows for P3.A. |

## Recommendation For P3.B

Proceed to Runtime Hook Dry-Run Design only as architecture/discovery first. P3.B should define passive hook contracts, input freshness, output retention and fail-closed behavior before any implementation. No hook may have authority to execute, route, apply, write runtime decision state or move users.

## Required Verdicts

`reality_audit_complete=true`

`implementation_conflict_audit_complete=true`

`truth_source_audit_complete=true`

`runtime_audit_complete=true`

`dryrun_domain_defined=true`

`dryrun_decision_model_defined=true`

`dryrun_contract_defined=true`

`dryrun_verification_defined=true`

`dryrun_observability_defined=true`

`dryrun_retention_defined=true`

`safe_to_continue_to_runtime_hook_dryrun=true`

## Safety

`runtime_mutation_performed=false`

`routing_changed=false`

`users_moved=false`

`autoswitch_apply_run=false`

`execution_engine_implemented=false`

`runtime_hooks_implemented=false`

`deploy_performed=false`

## Stop Condition

P3.A report complete. P3.B was not started.

