# V7 Code Responsibility Deep Audit Report

Status: `RT2_PR2A_CODE_RESPONSIBILITY_DEEP_AUDIT_PASS_READ_ONLY`

Scope: OMP §28.9 `RT2-PR2A CODE RESPONSIBILITY DEEP AUDIT`, added as the mandatory substep of the existing `RT2-PR2 LEGACY_SURFACE_REDUCTION`. The requested `V7_POST_RESET_RUNTIME_MATURITY_AND_OPTIMIZATION_PROGRAM_V1` is represented canonically by that existing RT2 profile inside OMP; no parallel Program was created.

Inputs: PR1 baseline, PR2 engine/package audit, M10 responsibility/benchmark evidence, current committed source, existing unit tests and saved knowledge graph. This is `DISCOVER -> CLASSIFY -> PLAN` only. No code, files, deployment, timer, service, Runtime, routing, CPS or Authority state was changed.

## 1. Coverage and method

The analysis follows `FILE -> MODULE -> CLASS -> FUNCTION -> CALLER -> CONSUMER -> STATE -> SIDE EFFECT -> PRODUCT EFFECT`. It uses the PR2 reproducible graph (1,076 file-level nodes, 3,585 total nodes, 3,979 confirmed structural edges), AST function inventories, source call sites, deploy/unit contracts and existing tests. Function-level depth is applied to mutation-capable, safety, fallback and high-fan-out paths; low-impact helpers are classified without pretending that every helper needs Runtime-level analysis.

| Surface | Observed size | Function/class inventory | Required depth |
| --- | ---: | ---: | --- |
| `tools/v7-users-autoswitch` | 23,639 LOC | 313 functions | full responsibility groups and critical path functions |
| `tools/v7_sync_lib.py` | 25,379 LOC | 306 functions | full responsibility groups and critical persistence functions |
| `admin/v7-admin-api` | 41,024 LOC | 717 functions | API/UI/action boundaries and mutation-capable handlers |
| `admin_core/operator_execution.py` | 9,044 LOC | 165 functions | Packet/lease/barrier/approval/rollback boundary |
| active mutation-capable production dependencies | unit and executable contracts | 5 primary runtime chains | caller/consumer/effect chain |

## 2. Component responsibility maps

### 2.1 `tools/v7-users-autoswitch`

Component: legacy planner, governed execution adapter and compatibility/engineering surface.

Architectural layer: predominantly Control Plane and fallback; several Engineering Plane diagnostics remain co-located. It is not the primary Core dataplane writer.

Owner: existing Planner/autoswitch, policy/Authority, Matrix, execution and rollback owners.

Real consumers: explicit manual/governed invocation, the Matrix event-only consumer path, `v7-user-switch`, service-Matrix verification, existing diagnostics and unit tests. The inactive `v7-users-autoswitch.timer` is not proof of no consumer; the active planner-named timer instead calls the Matrix event-only consumer.

| Responsibility | Critical functions / entrypoints | Caller -> consumer | State / side effect | Product effect | Classification / decision |
| --- | --- | --- | --- | --- | --- |
| passive event consumption | `consume_passive_events_only`, `AutoswitchPlanner._consume_passive_production_events`, `materialize_service_failure_automation_advisory` | `v7-service-matrix-refresh-all --consume-existing-service-failure-events-only` -> planner consumer -> governed standing-policy path | reads Matrix/event receipts; may materialize bounded engineering/incident projections | retains a lawful incident successor without primary packet forwarding | `KEEP_CONTROL_PLANE`; split logically from generic planning before any physical shrink |
| governed planning and selection | `AutoswitchPlanner.plan`, `_decision_for_user`, `_select_moves`, `_authority_budget_gate`, `_approved_plan_lock_validation`, `_emergency_failover_authority_gate` | main/guided CLI -> plan -> packet/clearance consumer | reads users, egress, policy, Matrix, restore barrier and snapshot facts; persists selected-plan/load summary | produces bounded, fail-closed candidate moves | `KEEP_FALLBACK`; `RESPONSIBILITY_MIXING` because health, decision, snapshot and lifecycle logic coexist |
| user movement / verify / rollback | `AutoswitchPlanner.apply`, `_run_switch`, `_verify_routes_for_apply`, `_reuse_or_verify_emergency_required_services`, rollback packet functions | approved plan -> `v7-user-switch` -> existing low-level writer; failed verify -> rollback owner | subprocesses, routing verification, audit/rollback records | bounded recovery only; never Core primary forwarding | `LEGACY_EXCEPTION`; removal requires equivalent governed Authority, rollback and crash/recovery proof |
| certification, Polygon and topology diagnostics | `controlled_source_topology_diagnostic`, `controlled_campaign_target_selection_diagnostic`, `ct_m0f_standing_source_selection_only`, authority-request helpers | explicit diagnostic CLI/tests -> Engineering/OMP consumers | reads CPS/owner evidence; diagnostic outputs only unless separately admitted | engineering evidence and certification readiness | `WRONG_ARCHITECTURAL_LAYER` inside planner file; `MOVE_TO_ENGINEERING_PLANE` is a future function-level extraction candidate |
| legacy compatibility | legacy per-user route checks, compatibility adapters and old plan/packet schemas | governed fallback/manual operators and tests | can read legacy per-user route state; legacy writer only under explicit path | preserves recovery compatibility | `HISTORICAL_RESIDUE` only where no live fallback consumer remains; no whole-file removal proof |

Critical function checks:

| Function | Purpose / caller / consumer | State and effect | Required? / disposition |
| --- | --- | --- | --- |
| `AutoswitchPlanner.plan` | CLI main -> `apply`/receipt consumer | reads registries, policy, Matrix, restore barrier and authority limits; persists dynamic-load summary | required only for governed/fallback planning; `SHRINK` by separating non-planner diagnostics |
| `AutoswitchPlanner.apply` | CLI main after `plan` -> `v7-user-switch` and verifier | attempts bounded movement only behind selection and gates; records outcomes | safety-critical fallback; `KEEP` |
| `_consume_passive_production_events` | Matrix event producer and `consume_passive_events_only` -> service-failure consumer | consumes durable event/Matrix state, returns bounded successor | active Control/Engineering consumer; `KEEP`, isolate from movement code |
| `_verify_routes_for_apply` | `apply` -> route/service verification | invokes `ip route/rule` checks before movement terminal | safety critical; `KEEP_FALLBACK` |
| `controlled_source_topology_diagnostic` | explicit CLI/tests -> OMP/certification evidence | read-only evidence projection | not planner hot path; `MOVE_TO_ENGINEERING_PLANE` candidate |

Final disposition: `SHRINK_BY_RESPONSIBILITY`, with `KEEP` for bounded planner/fallback and `MOVE_TO_ENGINEERING_PLANE` candidates. `REMOVE_CANDIDATE = NONE` until per-function consumer and recovery evidence is complete.

### 2.2 `tools/v7_sync_lib.py`

Component: shared engineering truth, OMP continuation, Polygon, deploy and reconciliation library.

Architectural layer: Engineering Plane. It is explicitly outside the Core primary forwarding graph.

Owner: existing OMP, CPS, deploy/truth, Polygon and canonical-document owners.

Real consumers: `v7-truth-check`, `v7-safe-deploy`, release/sync tools, Matrix continuation consumers, Polygon/test tooling and unit tests.

| Responsibility | Critical functions / entrypoints | Caller -> consumer | State / side effect | Product effect | Classification / decision |
| --- | --- | --- | --- | --- | --- |
| CPS normalization / consistency | `build_normalized_cps_document`, `atomic_reconcile_cps`, `cps_live_state_consistency`, `program_execution_reconciliation` | truth-check/reconciliation callers -> CPS + OMP pointer owner | atomically writes/reconciles current-state projection only when explicitly requested | prevents contradictory engineering execution state | `KEEP_ENGINEERING`; high-risk persistence boundary, not Runtime |
| OMP continuation | `continue_omp_engineering_control_loop`, `heartbeat_program_reentry`, `consume_service_failure_automation_frontier` | `v7-truth-check --continue-omp` or Matrix receipt consumer -> exact next owner | reads CPS/capability corpus; rejects recursion/external/incident boundaries | preserves legal successor or STOP_SAFE, not route apply | `KEEP_ENGINEERING`; `RESPONSIBILITY_MIXING` with CPS updates and orchestration in one module |
| Polygon / scale / certification | `execute_future_scale_scenario`, `execute_permanent_polygon_*`, `finalize_polygon_*` | CI/tests/OMP -> evidence and next criteria consumer | generated evidence and optional CPS projection under owner gates | engineering validation only | `MOVE_TO_ENGINEERING_SUBMODULE` candidate; no Runtime dependency |
| deploy / runtime identity | `safe_deploy_plan`, runtime fingerprint/manifest helpers | `v7-safe-deploy` -> existing deploy owner | deploy plan, identity, manifest and safe apply boundary | safe delivery, not routing decision | `KEEP_SEPARATE_INTERFACE`; do not co-locate with CPS mutation long term |
| delegated-policy reconciliation | `reconcile_active_standing_delegated_policy_to_cps`, `_service_failure_action_class_reuse_projection` | existing policy/Matrix owner -> CPS projection | writes only lawful engineering projection; preserves fail-closed fields | keeps bounded action-class evidence aligned | `KEEP_ENGINEERING`, target extraction with CPS helpers |

Critical function checks:

| Function | Purpose / caller / consumer | State and effect | Required? / disposition |
| --- | --- | --- | --- |
| `atomic_reconcile_cps` | reconciliation callers -> CPS/OMP pointer owner | atomic document update and rollback on failure | required canonical persistence boundary; `KEEP` |
| `continue_omp_engineering_control_loop` | truth-check/Matrix lifecycle -> existing OMP or exact external owner | reads frontier; explicitly rejects recursive, binary-only, active-incident and external-boundary misuse | required Engineering control; `KEEP`, isolate selector/projection helpers |
| `cps_live_state_consistency` | truth-check -> operator/OMP consumer | read-only consistency result | `KEEP` as verifier |
| `safe_deploy_plan` | `v7-safe-deploy` -> deploy owner | plan/identity/deploy evidence, no routing authority by itself | `KEEP` behind deploy interface |

Final disposition: `SHRINK_BY_EXISTING_ENGINEERING_INTERFACES`. The proven issue is co-location of CPS mutation, continuation, Polygon and deployment—not a Runtime layer violation. No function is an `REMOVE_CANDIDATE` until every CLI and test consumer is migrated or retired.

### 2.3 `admin/v7-admin-api`

Component: active administrative HTTP API and embedded UI surface.

Architectural layer: API/read-model/UI boundary, with guarded operator-action adapters. It must not become a parallel routing or Authority owner.

Owner: existing admin/API, operator-execution, component and deploy owners.

Real consumers: `v7-admin-api.service`, browser/admin clients, existing read models and guarded action endpoints.

| Responsibility | Critical functions / entrypoints | Caller -> consumer | State / side effect | Product effect | Classification / decision |
| --- | --- | --- | --- | --- | --- |
| HTTP dispatch | `Handler.do_GET`, `Handler.do_POST` | HTTP server -> named handler/read/action consumer | parses request/auth/CSRF context and dispatches | admin visibility and bounded operator interaction | `KEEP_API`; dispatch is too broad and requires route-group extraction |
| UI rendering | `html_page_v2`, `connect_page`, `overview` | GET route -> browser | emits 16,528-line embedded HTML/CSS/JS; no routing state write | human operator surface | `RESPONSIBILITY_MIXING`; `SHRINK_MOVE_TO_UI_ASSET` candidate under existing admin owner |
| egress provisioning / configuration | `egress_draft_runtime_run`, `egress_channel_add_pipeline`, `egress_draft_*`, proxy/OpenVPN helpers | guarded POST -> existing runtime/deploy component owner | may prepare/apply component configuration through existing guards | controlled egress lifecycle | `KEEP_ACTION_ADAPTER`; direct business/runtime logic within API is an extraction candidate |
| operator decision/action | recommendation, service-aware preview/guarded handlers, execution-contract helpers | guarded POST -> `operator_execution`/existing tools | action request, audit and explicit safety gates | operator can inspect or request bounded action | `KEEP_ADAPTER`; prevent duplicate policy/Authority decision |
| read models / diagnostics | `user_readiness`, `egress_detail`, status/overview helpers | GET -> existing registry/health readers | reads state and shapes response | observability | `KEEP_READ_MODEL`; extract from mutation handlers where entangled |

Critical function checks:

| Function | Purpose / caller / consumer | State and effect | Required? / disposition |
| --- | --- | --- | --- |
| `html_page_v2` | GET route -> browser | presentation only, but 16,528 LOC embedded in API executable | required UI, not required in API module; `MOVE_TO_UI_ASSET` candidate |
| `Handler.do_POST` | HTTP caller -> named existing action owner | dispatches many component, egress and operator actions | required boundary; `SHRINK_BY_ROUTE_GROUP`, never direct replacement |
| `egress_draft_runtime_run` | guarded POST -> deploy/runtime component owner | invokes existing draft/runtime path | mutation-capable adapter; `KEEP_GUARDED`, extract lifecycle service only with owner proof |
| `service_aware_apply_guarded` | guarded POST -> existing service-aware action path | enforces explicit guard before action | safety-relevant adapter; `KEEP` |

Final disposition: `SHRINK_BY_ROUTE_AND_PRESENTATION_SEPARATION`; no direct route or whole API deletion is supported. `html_page_v2` is the clearest low-risk structural extraction candidate but needs compatibility/UI tests and a separately admitted change.

### 2.4 `admin_core/operator_execution.py`

Component: canonical governed execution safety boundary.

Architectural layer: Control Plane safety/Authority boundary; excluded from continuous Data Plane forwarding.

Owner: existing operator-execution, Packet, lease, barrier, rollback and Authority owners.

Real consumers: governed canary cycle, packet CLI, admin action adapters, truth/governance checks and execution unit tests.

| Responsibility | Critical functions / entrypoints | Caller -> consumer | State / side effect | Product effect | Classification / decision |
| --- | --- | --- | --- | --- | --- |
| packet schema and approval validation | `validate_approvals`, `validate_zero_packet`, `validate_nonzero_packet`, expiry/binding validators | packet builders/`execute_packet` -> legal execution gate | reads approvals, expiry, action class and binding | blocks unsafe or replayed action | `KEEP_SAFETY_BOUNDARY` |
| runtime recheck and bounded clearance | `runtime_recheck`, `preview_restore_barrier_clearance`, `append_restore_barrier_clearance` | governed cycle -> execution consumer | reads current state; may write a bounded restore-barrier clearance only in runtime-action mode | prevents stale/overbroad movement | `KEEP_SAFETY_BOUNDARY` |
| execution receipt / audit | `execute_packet`, `append_record` helpers | governed cycle/CLI -> audit and successor consumers | append-only audit; records denial/approval/runtime-action result | replay prevention and accountable terminal | `KEEP` |
| rollback semantics | `rollback_operational_compensation_contract` and rollback validation helpers | packet/test/rollback consumer | produces compensation contract, not global rewind | bounded recovery model | `KEEP`; not historical residue |
| authority request/policy scaffolding | controlled-certification/standing-policy request and validation helpers | existing policy owner -> packet/Matrix consumer | contracts and validation, no self-granted scope | exact action-class enforcement | `KEEP`, but candidate for submodule separation from packet primitives |

Critical function checks:

| Function | Purpose / caller / consumer | State and effect | Required? / disposition |
| --- | --- | --- | --- |
| `validate_approvals` | packet validators -> `execute_packet` | rejects missing/expired/invalid dual or delegated approval | mandatory safety boundary; `KEEP` |
| `execute_packet` | governed cycle/CLI -> audit, clearance and exact next consumer | replay check; may append governed record or bounded clearance; explicitly reports no user/routing movement itself | mandatory boundary; `KEEP` |
| `rollback_operational_compensation_contract` | packet/tests -> rollback consumer | read-only compensation contract | mandatory recovery semantics; `KEEP` |
| `validate_nonzero_packet` | packet builder/executor -> clearance path | validates blast radius, users, targets, envelopes and source bindings | mandatory safety boundary; `KEEP` |

Final disposition: `KEEP_SAFETY_BOUNDARY`, with future `SHRINK_BY_SUBMODULE` only after preserving packet/lease/barrier/replay/rollback tests. There is no proof that this layer is obsolete.

### 2.5 Runtime mutation-capable dependency map

| Runtime chain | Caller -> consumer | State / side effect | Correct class | Finding / disposition |
| --- | --- | --- | --- | --- |
| `v7-path-guard-repair.timer` -> `v7-path-guard-repair --apply` | 2-minute timer -> sanity check -> repair commands | may set `ip_forward`, MSS clamp, invoke `v7-routing-sync`, enable killswitch, invoke Direct autosync, write state/audit | `LEGACY_EXCEPTION` / recovery Control Plane | `HIDDEN_RUNTIME_DEPENDENCY` relative to M10 compact projection; `KEEP` pending exact failure-matrix and Authority/recovery reconciliation |
| `v7-direct-autosync.timer` -> `v7-direct-auto-sync` | 10-minute timer -> Direct DNS/config owner | may update domains, render/restart dnsmasq, write Direct state | `CONTROL_PLANE` for Direct product behavior | `KEEP_RUNTIME`; exclude explicitly from Core minimality claim, not a routing-Core consumer |
| `v7-autoswitch-planner.timer` -> `v7-service-matrix-refresh-all --consume-existing-service-failure-events-only` | 30-second timer -> Matrix/event consumer -> governed standing-policy consumer only | reads existing event/Matrix state; no unconditional legacy planner loop | `CONTROL_PLANE` plus Engineering continuation | `KEEP_RUNTIME`; unit name is `HISTORICAL_RESIDUE`/operator-confusing, rename only through unit/deploy admission |
| `v7-service-matrix-refresh.timer` and Telegram sentinel | 15-minute refresh / 4-second sentinel (`--no-autoswitch`) -> Matrix state/events | health observation, durable Matrix update, exact existing consumer wake | `CONTROL_PLANE` | `KEEP_RUNTIME`; no duplicate primary routing writer proven |
| `v7-health.service` | 30-second health loop -> history/stability/load/diagnose/state projection consumers | multiple health/state reads and writes | `CONTROL_PLANE` | `RESPONSIBILITY_MIXING_CANDIDATE`; first map each output writer/reader, then consider splitting loop commands |

## 3. Cross-component classifications

| Classification | Evidence | Required disposition |
| --- | --- | --- |
| `DUPLICATE_RESPONSIBILITY` | No duplicate primary routing writer: Core `v7-routing-sync` is unique. Multiple health producers (Matrix refresh, sentinel, health loop) are deliberate but need per-state writer fencing; no automatic consolidation proof yet. | retain owners; audit state writer contracts before any merge |
| `RESPONSIBILITY_MIXING` | autoswitch combines planning, movement, Matrix, certification and diagnostics; sync library combines CPS, OMP, Polygon and deploy; admin API combines UI, dispatch and component lifecycle; health loop groups multiple outputs. | function/interface extraction plan, never a line-count split |
| `WRONG_ARCHITECTURAL_LAYER` | planner-hosted topology/Polygon diagnostics are Engineering responsibility; embedded UI is presentation responsibility. No Engineering -> Core synchronous forwarding edge was found. | move only these isolated responsibilities under existing Engineering/UI owners |
| `HISTORICAL_RESIDUE` | planner-named unit now runs Matrix event consumption; inactive autoswitch unit remains a fallback declaration; legacy per-user adapter remains recovery-capable. | keep until consumer, fallback and deployment references close; rename/unit cleanup after admission |
| `HIDDEN_RUNTIME_DEPENDENCY` | path guard and Direct autosync are active mutation-capable unit chains outside the compact M10 core description. | canonical package/topology reconciliation before `RUNTIME_PACKAGE_MINIMAL_PASS` |

## 4. Mature architecture fit

PR2/M10 benchmark is reused, not rerun. Its applicable pattern is stable: prepare/control state separately, apply forwarding through a narrow adapter, isolate observations/engineering work from packet forwarding, and retain recovery only behind bounded authority. V7 matches this at the Core boundary. The gaps are file/module responsibility boundaries above the Core—not a reason to add daemons, a Core v2, FRR/Junos emulation, a new owner or a new health system.

## 5. Required cleanup sequence (planning only)

```text
CONSISTENT EXISTING OMP/CPS ADMISSION
  -> canonical runtime-package/topology reconciliation
  -> per-function caller/consumer and state-writer matrix for one selected component
  -> smallest existing-owner extraction or removal proposal
  -> affected tests
  -> existing promotion ladder, safe deploy and observation
  -> residue check: imports, CLI, units, deploy, state, rollback and docs
  -> finalize exact physical delta
```

Priority order after legal admission:

1. Reconcile the active path-guard, Direct autosync, Matrix and health chains into the existing runtime package truth.
2. Isolate `v7-users-autoswitch` read-only diagnostics/Engineering helpers from governed movement semantics.
3. Separate `v7_sync_lib.py` public interfaces by existing CPS, continuation, Polygon and deploy consumers.
4. Extract `html_page_v2`/route groups from `admin/v7-admin-api` while retaining one API boundary.
5. Only then evaluate unused legacy helpers; no candidate is physically removable today.

## 6. Verification residual

The independent Core, autoswitch-policy, packet/Authority, routing-sync and Telegram-sentinel suites passed: `284 tests, OK`. The broader selected run executed `352` tests and has three pre-existing service-failure failures. This audit changes only the OMP contract and this report, so it cannot be their cause; they remain an exact evidence gap for the existing service-failure owner:

- `test_ct_m0f_standing_source_selection_reuses_controlled_pool_owner`: expected `ct_m0f_standing_source_selection_only(...).ok == true`, received false;
- `test_ct_m0f_active_service_failure_binding_requires_accounted_live_owner`: expected accounted live-owner binding, received false;
- `test_passive_idempotent_reentry_consumes_new_packet_bound_outcome`: a third passive reentry still reports `changed_records = 1` where the contract expects `0`.

Disposition: `EXISTING_SERVICE_FAILURE_OWNER_RECHECK_REQUIRED`. It is not fixed, suppressed or used to grant a mutation admission in PR2A.

## 7. Completion and residual

- Large components were analysed by responsibility and critical function, not only file size: `PASS`.
- Every mapped block names purpose, layer, owner, consumer/effect and disposition: `PASS`.
- Duplicate, mixing, wrong-layer, historical-residue and hidden-runtime classifications were assessed: `PASS`.
- A physical-cleanup sequence exists but authorizes no cleanup: `PASS`.
- `CODE_RESPONSIBILITY_DEEP_AUDIT_PASS = PASS`.

Residual: `RT2-PR3` remains blocked by the existing OMP/CPS admission transaction, natural real-traffic observation and runtime-package truth reconciliation recorded by PR1/PR2. This report does not advance CPS or assert `LEGACY_SURFACE_REDUCTION_PASS`.

## PROGRAMMATIC_CHANGE_DELTA

Program source LOC: `0 -> 0 -> 0`.

Documentation/report LOC: `0 -> 227 -> +227` for this report; OMP contract delta is reported separately from program source.

Test LOC: `0 -> 0 -> 0`; existing tests and source were read only.

Files added / modified / deleted / moved / runtime-excluded: program files `0 / 0 / 0 / 0 / 0`.

Functions/classes/entrypoints added / removed / moved / merged / changed: `0 / 0 / 0 / 0 / 0`.

Dependency, state, runtime package and routing-object edges changed: `0`; existing edges were classified only.

Legacy physical removal vs logical/runtime exclusion: `0` physical removal; no classification was converted into a Runtime change.

`PROGRAMMATIC_CODE_EFFECT = NONE`.

Runtime effects = `NONE`

Production effects = `NONE`

Authority effects = `NONE`
