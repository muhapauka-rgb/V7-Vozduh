# PROGRAM Z6.4 - Runtime Ownership Consolidation Design Report

Project: V7 Vozduh
Branch target: `v7-next`
Mode: READ ONLY ownership design
Date: 2026-06-02

## Executive Verdict

The final ownership model should consolidate around existing components:

- Runtime and execution owner: `tools/v7-users-autoswitch`
- Scheduler owner: `systemd/v7-users-autoswitch.timer/service`, scheduler-only
- Audit owner: `tools/runtime-support/v7-audit-log`
- Closure owner: `admin/v7-admin-api` closure model plus `admin_core/operator_observability.py`
- Low-level movement primitive: `v7-user-switch`
- Generic rollback primitive: `tools/runtime-support/v7-rollback-last-change`

No new orchestrator, planner, scheduler, execution engine, rollback engine, audit sink, closure source, restore-barrier source, or selected-move source is required.

## Evidence Directory

`z6_4-evidence`

- `00_gate0_revalidation.md`
- `01_target_lifecycle_model.md`
- `02_runtime_scheduler_admin_audit_models.md`
- `03_rollback_restore_barrier_closure_models.md`
- `04_authority_reduction_plan.md`
- `05_consolidated_ownership_map.md`
- `06_orchestrator_readiness_and_truth_audit.md`
- `07_final_verdicts.md`

## 1. Target Lifecycle Model

Signals -> Health -> Capacity -> Trust -> Policy -> Eligibility -> Planner -> Selected Moves -> Restore Barrier -> Runtime Recheck -> Execution -> Verification -> Rollback -> Audit -> Closure

| Stage | Primary Owner | Secondary Owner | Supporting Owners | Read-only Participants | Legacy Participants |
|---|---|---|---|---|---|
| Signals | Specialized signal writers | Admin/observability | service matrix, sentinel, quality, health/speed/client tooling | Autoswitch readers, Admin views | historical signal captures |
| Health | Existing health/state tooling | Autoswitch consumer | quality/speed/client tooling | Admin/operator views | unknown historical scripts |
| Capacity | `tools/v7-users-autoswitch` | Admin proposal/visibility | registries, load summary | Admin execution previews | historical packet checks |
| Trust | Admin trust/read model | Autoswitch future consumer | release/runtime evidence | operator views | historical trust reports |
| Policy | policy/org policy files | Admin policy surface | operator-controlled policy changes | Autoswitch/Admin readers | manual file edits |
| Eligibility | `tools/v7-users-autoswitch` | Admin proposal/gates | service matrix, policy, capacity, trust | Admin/operator views | historical proposals |
| Planner | `tools/v7-users-autoswitch` | Admin dry-run view | signal writers | systemd stdout/journal, Admin plan readers | draft planner timer |
| Selected Moves | `tools/v7-users-autoswitch` | Admin selected-move visibility/gates | restore-settle samples | operator observability | persistent selected-move files |
| Restore Barrier | `tools/v7-users-autoswitch` | Admin closure/visibility | restore-settle gate, operator observability | Admin restore-settle adapter | manual/historical barrier writes |
| Runtime Recheck | `tools/v7-users-autoswitch` | Admin/operator recheck evidence | `admin_core/operator_execution.py`, Admin gates | Admin execution previews | zero-move-only engine as movement owner |
| Execution | `tools/v7-users-autoswitch` | Admin controlled action surface | `v7-user-switch` primitive | Admin/operator views | direct CLI/manual authority |
| Verification | `tools/v7-users-autoswitch` | Admin/operator visibility | runtime checkers | operator timeline | manual verification reports |
| Rollback | `tools/v7-users-autoswitch` for movement lifecycle | `v7-rollback-last-change` primitive | Admin rollback surface, proxy guard rollback | rollback preview views | raw fallback rollback commands |
| Audit | `tools/runtime-support/v7-audit-log` | Admin audit wrapper/operator export | service event writers, autoswitch outcomes | Admin audit search | report-only audit |
| Closure | Admin closure model + `admin_core/operator_observability.py` | Autoswitch outcome + `v7-audit-log` | proposal/evidence closure controls | operator timeline/export | markdown closeouts |

## 2. Runtime Owner Model

`tools/v7-users-autoswitch` owns, and only it should own, live runtime movement truth:

- eligibility evaluation for movement;
- planner execution;
- canonical live selected moves;
- selected-move generation/hash/generation validation;
- restore-barrier consumption and runtime validation;
- runtime recheck for movement execution;
- apply admission;
- execution through the movement primitive;
- verification;
- movement rollback decision for the operation it executed;
- runtime outcome emission;
- autoswitch-owned safety/reconnect/load writes.

Out of scope for autoswitch:

- systemd scheduling;
- policy authorship;
- signal production;
- operator approval UX;
- closure record authorship;
- audit sink ownership;
- broad file/config rollback;
- historical report ownership.

## 3. Scheduler Model

`systemd/v7-users-autoswitch.timer/service` should own only:

- timer cadence;
- process launch;
- scheduled actor identity;
- OS-level service result.

It should never own:

- selected moves;
- planner authority;
- restore-barrier truth;
- execution outcome truth;
- rollback decisions;
- audit completion;
- closure state;
- policy/trust/capacity decisions.

## 4. Admin Model

Admin should own:

- operator visibility;
- proposals and approval surface;
- dry-run display;
- execution contract preview/read model;
- closure records;
- audit search/export surface;
- controlled operator invocation surface;
- runtime verdict display;
- evidence lineage and operation timeline.

Admin should approve:

- operator intent;
- closure transitions;
- governed manual actions;
- future runtime-owner-bound actions.

Admin should close:

- evidence objects;
- proposals;
- runtime/current objects;
- release/trust/drift objects;
- operation lifecycle records after runtime outcome and audit evidence exist.

Admin should never execute directly as lifecycle owner:

- direct user movement outside runtime ownership;
- independent selected-move execution;
- independent planner truth;
- independent rollback truth;
- sentinel-triggered runtime actions;
- closure without runtime/audit backing.

## 5. Audit Model

Canonical audit truth:

`tools/runtime-support/v7-audit-log`

Supplemental evidence:

- Admin action responses;
- operator observability timeline;
- service matrix event JSONL;
- Telegram sentinel event JSONL;
- autoswitch stdout/systemd journal;
- execution preview stores.

Historical evidence:

- markdown reports;
- historical approval packets;
- evidence bundles from prior blocks;
- raw fallback records.

Closure evidence:

- Admin closure records;
- final runtime outcome from autoswitch;
- audit event proving terminal state;
- operator export preview.

Audit relationship:

- Runtime owner produces execution facts.
- Audit owner records canonical events.
- Closure owner records lifecycle closure.
- No separate audit truth source is introduced.

## 6. Rollback Model

| Rollback Type | Owner | Authority | Scope | Limitation |
|---|---|---|---|---|
| Primary movement rollback | `tools/v7-users-autoswitch` | runtime movement lifecycle | users moved by runtime owner in current operation | not broad file/config rollback |
| Generic rollback primitive | `tools/runtime-support/v7-rollback-last-change` | primitive rollback | latest backup under configured roots | too broad to own lifecycle |
| Admin rollback surface | `admin/v7-admin-api` | operator wrapper | preview/apply wrapper | not rollback truth |
| Proxy guard rollback | Admin + proxy guard tool | emergency/domain rollback | proxy runtime guard domain | supporting only |
| Historical rollback | packets/reports | evidence | previous governed operations | not live authority |
| Emergency rollback | CLI primitives | break-glass | manual recovery | exceptional and audited only |

## 7. Restore Barrier Model

| Restore Barrier Stage | Future Owner | Reason |
|---|---|---|
| creation | Admin/operator closure/governance surface initiates; autoswitch owns runtime-valid shape | Creation is operator/governance intent, but runtime owner must define consumable shape. |
| validation | `tools/v7-users-autoswitch` | Autoswitch already validates active/expired/cleared/generation/hash/count/budget semantics. |
| consumption | `tools/v7-users-autoswitch` | Barrier exists to suppress or allow runtime selected moves. |
| expiration | Autoswitch interprets expiry; Admin displays expiry | Runtime meaning of expiry belongs to runtime owner. |
| clearance | Admin records intent; autoswitch validates generation/hash/count/budget | Clearance is operator intent plus runtime validation. |
| closure | Admin closure model + operator observability | Closure is lifecycle/evidence state, not execution. |
| audit | `v7-audit-log` | Canonical event sink. |

Restore-barrier rule:

- Autoswitch owns whether a barrier allows or blocks execution.
- Admin owns operator-visible lifecycle and closure.
- `v7-audit-log` owns canonical audit events.
- The barrier file is state/transport, not an owner.

## 8. Lifecycle Closure Model

An operation is COMPLETE when:

1. Runtime owner emitted terminal outcome: no-op, executed-and-verified, failed-closed, rolled back, cancelled, expired, or denied.
2. Rollback is not applicable, completed, or failed-closed.
3. Canonical audit event exists or absence is marked as closure blocker.
4. Admin/operator closure record is set with actor, reason, timestamp, and terminal state.
5. Operator observability can display final runtime verdict and evidence refs.

Completion declarations:

- Runtime completion: `tools/v7-users-autoswitch`.
- Operation closure: Admin closure model + operator observability.
- Audit completion: `v7-audit-log` event plus Admin/operator closure evidence.

Failure declarations:

- Runtime failure: `tools/v7-users-autoswitch`.
- Closure failure/blocker: Admin/operator closure model.
- Audit failure/blocker: Admin/operator closure model based on audit evidence.

Rollback completion:

- Movement rollback: `tools/v7-users-autoswitch`.
- Generic rollback: `v7-rollback-last-change` result, recorded through Admin/audit.
- Operation rollback closure: Admin/operator closure model.

Final lifecycle verdict:

- Runtime verdict: `tools/v7-users-autoswitch`.
- Operation closure verdict: Admin closure model + operator observability.
- Audit truth: `v7-audit-log`.

## 9. Authority Reduction Plan

| Path / Component | Future Role |
|---|---|
| `tools/v7-users-autoswitch` | Remain primary runtime/execution authority. |
| systemd autoswitch timer/service | Remain scheduler-only authority. |
| Admin autoswitch apply | Become controlled operator surface invoking runtime owner, not lifecycle owner. |
| Admin direct user switch | Become break-glass/exceptional operator path, not normal lifecycle owner. |
| CLI `v7-user-switch` | Become low-level primitive/break-glass only. |
| Sentinel execution path | Become advisory/signal-only. |
| Draft planner | Become legacy/do-not-touch. |
| Persistent selected-move files | Become read/evidence adapters, not live truth. |
| Generic rollback | Become primitive/emergency rollback, not lifecycle owner. |
| Admin execution contracts | Remain preview/governance/read model until connected through owner boundaries. |
| Operator execution zero-move engine | Remain governance/recheck support, not movement owner. |
| Historical reports/packets | Remain evidence, not authority. |

## 10. Consolidated Ownership Map

| Lifecycle Stage | Primary Owner | Secondary Owner | Truth Source | Authority Source | Closure Source | Conflict Level | Migration Difficulty |
|---|---|---|---|---|---|---:|---:|
| Signals | specialized signal writers | Admin/observability | signal JSON/event JSONL | signal tool ownership | Admin/operator evidence closure | MEDIUM | LOW |
| Health | health/state tooling | Autoswitch consumer | `v7-state.json` and speed state | health tool ownership | Admin/operator evidence closure | MEDIUM | MEDIUM |
| Capacity | autoswitch | Admin proposal surface | runtime plan/load summary | runtime owner | Admin/operator closure | MEDIUM | MEDIUM |
| Trust | Admin trust/read model | Autoswitch consumer | Admin trust surfaces | operator/governance read model | Admin closure | LOW/MEDIUM | MEDIUM |
| Policy | policy files | Admin policy surface | policy files | policy authority | Admin closure/evidence | MEDIUM | LOW/MEDIUM |
| Eligibility | autoswitch | Admin gates | autoswitch plan | runtime owner | Admin closure | MEDIUM | MEDIUM |
| Planner | autoswitch | Admin dry-run | autoswitch plan JSON | runtime owner | Admin/operator timeline | LOW/MEDIUM | LOW |
| Selected Moves | autoswitch | Admin visibility/gates | in-process autoswitch plan | runtime owner | Admin/operator timeline | HIGH | MEDIUM/HIGH |
| Restore Barrier | autoswitch | Admin closure/visibility | barrier file interpreted by runtime owner | runtime owner | Admin closure + audit | HIGH | HIGH |
| Runtime Recheck | autoswitch | Admin/operator evidence | runtime owner result | runtime owner | Admin closure | HIGH | HIGH |
| Execution | autoswitch | Admin controlled surface | runtime owner outcome | runtime owner | Admin closure + audit | HIGH | HIGH |
| Verification | autoswitch | Admin/operator views | runtime verify result | runtime owner | Admin closure + audit | MEDIUM | MEDIUM |
| Rollback | autoswitch movement lifecycle | generic rollback primitive | runtime/generic rollback result | runtime owner / primitive | Admin closure + audit | HIGH | HIGH |
| Audit | `v7-audit-log` | Admin/operator audit views | audit JSONL | audit sink owner | Admin closure references audit | HIGH | MEDIUM |
| Closure | Admin closure + operator observability | autoswitch outcome + audit | closure records | closure owner | Admin closure records | HIGH | HIGH |

## 11. Orchestrator Readiness

A. Can ownership consolidation alone solve most current conflicts?

Yes. Most current conflicts are ownership ambiguity and bypass authority, not missing primitives.

B. How much of Runtime Orchestrator already exists?

A partial orchestrator exists in `tools/v7-users-autoswitch`.

C. What percentage of orchestrator functionality already exists?

Estimated 65%.

D. What ownership gaps remain?

- restore-barrier creation/closure ownership;
- lifecycle closure truth;
- audit completion for autonomous cycles;
- direct Admin/CLI movement boundaries;
- generic rollback boundary;
- execution contract connection boundary.

E. What lifecycle gaps remain?

- no single operation terminal state;
- no guaranteed final audit event for every runtime cycle;
- no universal runtime recheck for manual paths;
- no unified rollback completion declaration;
- no canonical selected-move archive tied to closure.

F. What truth-source gaps remain?

- selected moves: in-process truth versus persistent readers;
- closure: Admin closure records versus reports;
- rollback: runtime rollback versus generic rollback outputs;
- audit: event sink versus report-only closeout;
- barrier: file state versus lifecycle owner.

G. What closure gaps remain?

- no formal COMPLETE/FAILED/ROLLED_BACK/CANCELLED/EXPIRED rule across all paths;
- no required link between runtime outcome, audit event, and closure record;
- autonomous cycles can finish without closure record;
- rollback completion and audit completion are not unified lifecycle state.

H. What is the smallest implementation required after this design?

Ownership wiring around existing components:

- preserve autoswitch as runtime owner;
- route execution outcomes to existing audit/closure surfaces;
- constrain manual/direct paths into operator surface or break-glass roles;
- define restore-barrier lifecycle records using existing Admin closure/audit surfaces and autoswitch validation;
- keep systemd scheduler-only;
- avoid any new orchestrator, scheduler, planner, execution engine, rollback engine, audit sink, or closure truth source.

## 12. Truth Source Audit

The proposed model creates:

- no duplicate truth sources;
- no duplicate planners;
- no duplicate execution paths;
- no duplicate rollback paths;
- no duplicate closure paths;
- no duplicate audit sinks.

Truth anchors:

- Runtime truth: `tools/v7-users-autoswitch`
- Scheduler truth: systemd timer/service
- Policy truth: policy files
- Signal truth: specialized signal files
- Audit truth: `v7-audit-log`
- Closure truth: Admin closure records/operator observability

## 13. Final Verdicts

ownership_model_designed=true

runtime_owner_model_defined=true

scheduler_model_defined=true

admin_model_defined=true

audit_model_defined=true

rollback_model_defined=true

restore_barrier_model_defined=true

closure_model_defined=true

implementation_scope_understood=true

safe_to_continue_to_Z6_5=true

## 14. Z6.5 Boundary

Z6.5 may proceed only if it preserves the ownership anchors from this report and does not introduce parallel systems.

This report authorizes design continuity only. It does not authorize implementation, deployment, runtime mutation, service restart, route mutation, user movement, merge, or force push.

