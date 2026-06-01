# PROGRAM Z6.3 - Runtime Ownership Consolidation Audit Report

Project: V7 Vozduh
Branch target: `v7-next`
Audit mode: READ ONLY
Date: 2026-06-02

## Executive Verdict

Ownership consolidation can happen mostly through existing components.

The future authoritative runtime and execution owner should be:

`tools/v7-users-autoswitch`

The future authoritative scheduler should remain:

`systemd/v7-users-autoswitch.timer/service`

but scheduler-only.

The future authoritative audit sink should be:

`tools/runtime-support/v7-audit-log`

The future authoritative closure owner should be:

`admin/v7-admin-api` closure model plus `admin_core/operator_observability.py`, backed by `v7-audit-log` and runtime outcomes from `v7-users-autoswitch`.

This is not a Runtime Orchestrator design. It is an ownership suitability map based on existing reality.

## Evidence Directory

`z6_3-evidence`

- `00_gate0_inventory.md`
- `01_lifecycle_owner_matrix.md`
- `02_authority_and_bypass_analysis.md`
- `03_legacy_and_closure_analysis.md`
- `04_orchestrator_readiness_answers.md`
- `05_truth_source_audit.md`
- `06_final_verdicts.md`

## 1. Lifecycle Stage Inventory

| Stage | Current Owners | Current Writers | Current Readers | Current Authorities | Current Bypasses |
|---|---|---|---|---|---|
| Signals | service matrix refresh, Telegram sentinel, quality compact, health/speed/client tools | Signal tools | Autoswitch, Admin, observability | Distributed signal authority | Signal files influence planner without approval packets. |
| Health | health/state/speed tooling | health/state tools | Autoswitch, quality compact, Admin | Runtime state evidence | Unknown/ad hoc health writers. |
| Service Matrix | `v7-service-matrix-refresh-all`, `v7-service-matrix-test`, `v7-telegram-sentinel` | Matrix/sentinel tools | Autoswitch/Admin | Live service signal | Multiple writers. |
| Capacity | Autoswitch dynamic load, registries, Admin proposals | Autoswitch/load and registry owners | Autoswitch/Admin | Capacity admission signal | Manual registry changes. |
| Trust | Admin runtime/release trust surfaces | Admin/read model | Admin/operator views | Read-only trust evidence | Not connected to execution authority. |
| Policy | policy/org policy files | operator/Admin | Autoswitch/Admin | Hard/tenant policy authority | Manual file edits. |
| Eligibility | Autoswitch, Admin proposal gates | Autoswitch output/proposals | Admin/operator | Planner eligibility | Admin/manual switch can bypass. |
| Planner | Autoswitch | Autoswitch stdout JSON | Admin dry-run, systemd stdout/journal | Planner authority | Draft planner unit latent. |
| Proposal | Admin generated proposals, historical packets | Admin/report generators | Admin/operator | Governance input | Not authoritative for autonomous apply. |
| Selected Moves | Autoswitch in-process plan; file readers | Autoswitch stdout/evidence files | Autoswitch apply, Admin/operator gates | Autoswitch live selected-move authority | Persistent file readers can be mistaken for source. |
| Restore Barrier | Autoswitch enforcement; fragmented writer | Historical/manual/governance flows | Autoswitch/Admin | Barrier enforcement | No single creation/closure owner. |
| Runtime Recheck | Autoswitch, operator zero-move recheck, Admin gates | Path-local outputs | Admin/operator/autoswitch | Fragmented admission | Admin/CLI direct switch bypass. |
| Execution | Autoswitch apply, Admin apply/direct switch, CLI primitive | Route mutation tools | Admin/runtime state | Multiple execution authorities | Direct switch, CLI, latent sentinel path. |
| Verification | Autoswitch, Admin endpoint checks | Autoswitch/Admin | Admin/operator | Path-local verification | Manual verification reports. |
| Rollback | Autoswitch, Admin, generic rollback, proxy rollback | rollback tools/Admin | Admin/operator | Multiple rollback authorities | Generic rollback outside contract scope. |
| Audit | `v7-audit-log`, Admin audit, operator audit, JSONL events | Audit/event writers | Admin/operator | Fragmented audit authority | report-only closure. |
| Closure | Admin closure records, operator timeline, reports | Admin closure-set, reports | Admin/operator | No unified runtime-cycle closure | Autoswitch can complete without closure record. |

## 2. Primary Owner Analysis

| Stage | Strongest Existing Owner | Why | Runtime Authority | State Ownership | Duplication Risk | Could Another Existing Component Own Better? |
|---|---|---|---|---|---|---|
| Signals | Specialized signal tools | They already write specific evidence files | Advisory | Signal JSON/event JSONL | MEDIUM | No; centralizing all signals would create unnecessary coupling. |
| Health | Existing health/state tooling | Owns observed runtime state | Advisory | `v7-state.json` and speed state | MEDIUM | Autoswitch should consume, not own health production. |
| Service Matrix | Service matrix tooling | Purpose-built service checks | Advisory/hard signal | service matrix files | MEDIUM | Telegram sentinel should remain service-specific support. |
| Capacity | Autoswitch | It makes movement decisions using capacity | Runtime admission | load summary plus registry reads | MEDIUM | Admin proposals are visibility, not runtime owner. |
| Trust | Admin trust/read model | Already operator-facing and read-only | None | trust/read surfaces | LOW/MEDIUM | Runtime owner can consume later but should not own trust UI. |
| Policy | Policy files | They are hard truth sources | Hard input | policy files | MEDIUM | Autoswitch should enforce, not own policy authoring. |
| Eligibility | Autoswitch | It selects movement candidates | Runtime | plan JSON | MEDIUM | Admin proposals cannot execute. |
| Planner | Autoswitch | Existing planner authority | Runtime | plan JSON/stdout | LOW/MEDIUM | No; draft planner would duplicate. |
| Proposal | Admin proposal layer | Existing operator proposal surface | Governance/read | proposal store/generated proposals | MEDIUM | Autoswitch should not own human proposal UI. |
| Selected Moves | Autoswitch | Live moves are in-process planner output | Runtime | ephemeral plan JSON | HIGH | No; files are readers/evidence only. |
| Restore Barrier | Autoswitch | Existing enforcement and generation-token validation | Runtime suppression | barrier read/enforcement | HIGH | Admin can support closure but should not enforce runtime. |
| Runtime Recheck | Autoswitch | Closest live pre-execution owner | Runtime | plan/barrier/safety checks | HIGH | Operator execution is zero-move only. |
| Execution | Autoswitch | Already applies selected moves and verifies | Runtime mutation | apply result/safety state | HIGH | Admin should be surface, CLI primitive only. |
| Verification | Autoswitch | Existing post-switch route verification | Runtime | apply result | MEDIUM | Admin can display/support. |
| Rollback | Autoswitch for movement lifecycle | Existing local rollback after verify failure | Runtime rollback | apply result/safety | HIGH | Generic rollback is broad primitive, not lifecycle owner. |
| Audit | `v7-audit-log` | Existing sink used by Admin and runtime-support | Audit event sink | audit JSONL | HIGH | Admin should wrap/display, not replace sink. |
| Closure | Admin closure + operator observability | Existing closure records and operation timeline | Closure/read, not mutation | closure records/timeline | HIGH | Autoswitch should supply outcomes, not own operator closure UX. |

## 3. Secondary Owner Analysis

| Stage | Secondary Owner | Support Function |
|---|---|---|
| Signals | Admin/observability | Display signal state and freshness. |
| Health | Autoswitch/Admin | Consume health for planning and visibility. |
| Service Matrix | Telegram sentinel | Fast service-specific signal contribution. |
| Capacity | Admin proposal layer | Capacity risk visibility and proposal generation. |
| Trust | Autoswitch | Future consumer of trust verdict, not producer. |
| Policy | Admin | Policy visibility and controlled operator changes. |
| Eligibility | Admin proposal/gates | Explain and preview eligibility. |
| Planner | Admin dry-run | Operator plan visibility. |
| Proposal | Operator observability | Timeline/evidence linkage. |
| Selected Moves | Admin selected-move gates | Read/evidence/validation only. |
| Restore Barrier | Admin restore-settle adapter, restore-settle gate | Visibility and evidence classification. |
| Runtime Recheck | `admin_core/operator_execution.py` | Zero-move recheck and governance record support. |
| Execution | Admin action surface | Operator-controlled invocation and audit wrapper. |
| Verification | Admin/operator observability | Post-action visibility. |
| Rollback | `v7-rollback-last-change`, Admin rollback preview | Low-level primitive and operator surface. |
| Audit | Admin audit wrapper, operator audit export | Event enrichment, search, export. |
| Closure | `v7-audit-log`, autoswitch outcome | Immutable event sink and runtime facts. |

## 4. Legacy Owner Analysis

| Owner | Type | Determination |
|---|---|---|
| Draft autoswitch planner systemd unit | Dormant/draft scheduler | DO NOT TOUCH |
| Persistent selected-move evidence files | Historical/read adapter | Retire Later as authority; keep as evidence. |
| Historical approval packets | Historical governance | Keep as evidence; not live owner. |
| Zero-move operator execution engine | Partial owner | Keep; not current movement executor. |
| Admin execution contract store | Preview/read-only owner | Keep; not current execution authority. |
| Direct CLI movement | Break-glass primitive | Retire Later as independent lifecycle path. |
| Generic latest-change rollback | Broad primitive | Keep primitive; not primary lifecycle owner alone. |
| Markdown closeout reports | Historical closure | Keep as evidence; not machine closure truth. |

## 5. Authority Analysis

Who currently has authority:

- Autoswitch has autonomous runtime and execution authority.
- Admin has manual mutation authority.
- CLI primitives have low-level mutation authority.
- Generic rollback has broad rollback authority when invoked.
- `v7-audit-log` has audit sink authority.
- Admin closure has closure-record authority but not runtime-cycle completion authority.

Who should have authority:

- Runtime/execution/verification/movement rollback: `tools/v7-users-autoswitch`.
- Scheduler: systemd timer/service only.
- Operator proposal/visibility/closure: Admin/operator surfaces.
- Audit sink: `v7-audit-log`.
- Broad primitive rollback: `v7-rollback-last-change` as helper, not lifecycle owner.

Who should lose independent authority later:

- Admin direct switch as independent lifecycle authority.
- CLI `v7-user-switch` as independent lifecycle authority.
- Sentinel-triggered autoswitch as execution authority.
- Persistent selected-move files as any live selected-move authority.
- Generic rollback as operation lifecycle owner.

Who should become advisory/read-only:

- Telegram sentinel execution path.
- Admin execution contracts until intentionally connected.
- Operator observability and selected-move adapters.
- Draft planner timer.

Who should remain execution-capable:

- Autoswitch as primary execution owner candidate.
- `v7-user-switch` as low-level primitive behind an owner.
- Admin as controlled operator surface for invoking existing owners.
- `v7-rollback-last-change` as low-level rollback primitive.

## 6. Bypass Analysis

| Bypass | Required | Duplicates Authority | Conflicts With Ownership | Production-Safe |
|---|---:|---:|---:|---|
| Autonomous autoswitch apply | Yes | Yes | Yes vs approval contracts | Partially; governed by policy/safety/barrier. |
| Admin autoswitch apply | Yes | Yes | Medium/high | Confirmed and audited, but bypasses contracts. |
| Admin direct user switch | Break-glass/operator need | Yes | High | Auth/CSRF/audit, but lifecycle conflict. |
| CLI `v7-user-switch` | Primitive need | Yes | High | Unsafe as independent path. |
| Sentinel autoswitch path | No active production need found | Yes | High latent | Production service uses `--no-autoswitch`. |
| `v7-rollback-last-change --apply` | Yes primitive | Yes | Medium/high | Guarded via Admin confirm, broad via CLI. |
| Persistent selected-move files | Evidence need | Potentially | High if authoritative | Safe only as read/evidence. |
| Draft planner timer | No active need found | Yes | High latent | DO NOT TOUCH. |

## 7. Lifecycle Closure Analysis

Z6.2 found no unified lifecycle closure owner. Z6.3 identifies the closest existing closure owner candidate:

`admin/v7-admin-api` closure model + `admin_core/operator_observability.py`

with `v7-audit-log` as audit sink and `v7-users-autoswitch` as runtime outcome provider.

Rationale:

- Admin already writes closure records with state/reason/actor/timestamp.
- Admin calls `v7-audit-log` for closure actions.
- Operator observability already exposes timeline, runtime verdicts, operation detail, audit export preview, governance preview, and rehearsal preview.
- It is non-runtime-mutating and operator-facing.

Closure should not be owned by systemd, signal writers, selected-move files, or historical markdown reports.

## 8. Ownership Consolidation Map

| Lifecycle Stage | Current Owners | Primary Owner Candidate | Secondary Owner Candidate | Supporting Owners | Legacy Owners | Conflict Level | Reuse Recommendation |
|---|---|---|---|---|---|---:|---|
| Signals | Signal tools | Specialized signal writers | Autoswitch consumer | Admin/observability | None material | MEDIUM | REUSE |
| Health | Health/state tools | Existing health tooling | Autoswitch/Admin | quality compact | Unknown scripts | MEDIUM | REUSE |
| Service Matrix | service matrix tools, sentinel | service matrix tooling | sentinel advisory | Admin/autoswitch readers | ad hoc writers | MEDIUM | REUSE |
| Capacity | Autoswitch, registry, Admin | Autoswitch | Admin proposals | registries | historical packets | MEDIUM | REUSE/EXTEND |
| Trust | Admin read surfaces | Admin trust/read model | Autoswitch consumer | operator views | historical docs | LOW/MEDIUM | REUSE |
| Policy | Policy files/Admin | policy files | Autoswitch enforcer | Admin visibility | manual edits | MEDIUM | REUSE |
| Eligibility | Autoswitch/Admin gates | Autoswitch | Admin gates | signals | historical packets | MEDIUM | REUSE |
| Planner | Autoswitch | Autoswitch | Admin dry-run | signals | draft planner | LOW/MEDIUM | REUSE |
| Proposal | Admin/historical packets | Admin proposal layer | operator observability | evidence bundles | markdown packets | MEDIUM | REUSE |
| Selected Moves | Autoswitch/files | Autoswitch | Admin gates | restore-settle samples | selected-move files | HIGH | REUSE/REFACTOR LATER |
| Restore Barrier | Autoswitch/fragmented writers | Autoswitch | Admin closure/visibility | restore-settle gate | manual writes | HIGH | REUSE/REFACTOR LATER |
| Runtime Recheck | Autoswitch/operator/Admin | Autoswitch | operator execution/Admin gates | observability | zero-move-only engine as executor | HIGH | REUSE/EXTEND |
| Execution | Autoswitch/Admin/CLI | Autoswitch | Admin surface | `v7-user-switch` primitive | direct CLI authority | HIGH | REUSE/EXTEND |
| Verification | Autoswitch/Admin | Autoswitch | Admin observability | runtime checkers | manual reports | MEDIUM | REUSE |
| Rollback | Autoswitch/Admin/generic | Autoswitch for movement lifecycle | `v7-rollback-last-change` primitive | Admin rollback/audit | raw fallback commands | HIGH | REUSE/REFACTOR LATER |
| Audit | audit log/Admin/operator/events | `v7-audit-log` | Admin/operator audit views | signal event writers | markdown reports | HIGH | REUSE/EXTEND |
| Closure | Admin/operator/reports | Admin closure + operator observability | autoswitch outcome + audit log | evidence/proposal closure controls | report closeouts | HIGH | REUSE/EXTEND |

## 9. Orchestrator Readiness Analysis

A. Can ownership consolidation happen mostly through existing components?

Yes.

B. Can `tools/v7-users-autoswitch` become the runtime owner without creating a new orchestrator?

Yes. It already owns the live autonomous runtime path.

C. Can systemd remain scheduler-only?

Yes. It should launch the cycle and not own lifecycle truth.

D. Can Admin become operator surface only?

Yes. Admin is strongest as visibility/proposal/closure/audit/action surface, not primary runtime owner.

E. Can execution paths be unified without replacing components?

Yes, by ownership consolidation around existing autoswitch and existing primitives. This report does not implement that.

F. Can rollback ownership be centralized around existing logic?

Mostly yes. Movement rollback suitability belongs with autoswitch; broad rollback primitive remains `v7-rollback-last-change`.

G. Can lifecycle closure be added without introducing duplicate truth?

Yes, if closure reuses Admin closure records and `v7-audit-log`, with runtime outcome supplied by autoswitch.

H. What are the largest ownership conflicts?

- Autoswitch apply vs Admin execution contracts.
- Admin direct switch vs autoswitch selected moves.
- CLI `v7-user-switch` vs governed lifecycle.
- Restore-barrier enforcement vs fragmented barrier creation/closure.
- Generic rollback vs contract-scoped rollback.
- Multiple audit and closure writers.
- Persistent selected-move readers vs ephemeral selected-move truth.
- Draft planner timer as latent duplicate scheduler/planner.

I. What are the smallest changes required for consolidation?

No implementation is proposed here. The smallest ownership changes implied by the evidence are:

- keep autoswitch as runtime/execution owner candidate;
- keep systemd scheduler-only;
- keep Admin operator/closure/audit surface;
- keep `v7-audit-log` as audit sink;
- keep `v7-user-switch` and `v7-rollback-last-change` as primitives, not lifecycle owners;
- demote sentinel execution capability to advisory/signal-only ownership;
- prevent persistent selected-move files from becoming canonical live selected-move truth;
- make restore-barrier lifecycle suitability align with the runtime owner and Admin closure support.

## 10. Truth Source Audit

ownership conflicts=HIGH

authority conflicts=HIGH

duplicate execution authority=HIGH

duplicate rollback authority=HIGH

duplicate audit authority=HIGH

duplicate closure authority=HIGH

duplicate truth sources=HIGH

orphan lifecycle stages=restore_barrier_generation_closure, unified_runtime_closure, autonomous_audit_completion, contract_scoped_rollback_execution, global_runtime_recheck

## 11. Final Verdicts

ownership_model_understood=true

primary_runtime_owner=tools/v7-users-autoswitch

primary_execution_owner=tools/v7-users-autoswitch

primary_rollback_owner=tools/v7-users-autoswitch_for_movement_lifecycle_with_tools/runtime-support/v7-rollback-last-change_as_low_level_generic_rollback_primitive

primary_audit_owner=tools/runtime-support/v7-audit-log

primary_closure_owner=admin/v7-admin-api_closure_model_plus_admin_core/operator_observability.py

ownership_conflicts_understood=true

authority_conflicts_understood=true

safe_to_continue_to_Z6_4=true

## 12. Boundary for Z6.4

Z6.4 must not create a new orchestrator, scheduler, planner, execution path, rollback path, audit truth source, closure truth source, restore-barrier truth source, or selected-move truth source.

Any next-stage design must start from:

- `tools/v7-users-autoswitch` as primary runtime/execution owner candidate;
- `systemd/v7-users-autoswitch.timer/service` as scheduler-only;
- Admin/operator surfaces as proposal, visibility, closure, and audit surfaces;
- `v7-audit-log` as canonical audit sink candidate;
- existing rollback and movement primitives retained behind ownership boundaries.

