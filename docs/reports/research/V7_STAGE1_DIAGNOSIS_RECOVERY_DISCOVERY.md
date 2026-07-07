# V7 Stage 1.2 — Diagnosis Recovery Discovery

Дата: 2026-07-07

Режим: Recovery Discovery, без реализации.

## 1. Executive Summary

Domain 11 — Diagnosis не сертифицирован не из-за ошибки архитектуры. Архитектурно домен определен правильно: он должен превращать incident/evidence state в доказанное объяснение причины, owner, unknown state, policy boundary или required resolution, не смешивая симптом, blocker и root cause.

Причина `NOT CERTIFIED` точная: в реализации нет одного замкнутого executable/read-only Diagnosis / Owner Resolution projection, который берет существующие evidence, blockers, incident/execution identity и owner map, выпускает machine-readable diagnosis record, присваивает terminal owner-resolution classification и делает этот результат потребляемым для OMP, Current Program State и Production Maturity.

В проекте уже есть много частей Diagnosis:

- `tools/v7-egress-diagnose` диагностирует состояние egress health.
- `tools/v7-users-autoswitch` производит current-channel failure evidence, blockers, wake evidence и selected move diagnostics.
- `tools/v7-control-plane-governance-check` читает root-cause/status artifacts и формирует локальные governance projections.
- `admin_core/diagnostic_views.py` дает read-only diagnostic/admin projections.
- `admin_core/autonomy_trust_acceleration.py` уже содержит read-only engineering automation models, root-cause-adjacent attribution models и запрет на root-cause claims без доказательств.
- Engineering Reports уже выполняют Owner Resolution вручную и документально.

Но эти части не замкнуты в один канонический Diagnosis output. Поэтому Stage 1 правильно классифицировал Domain 11 как `NOT CERTIFIED`.

Минимальная implementation mission: расширить существующий Engineering Automation / OMP read-only путь, прежде всего `admin_core/autonomy_trust_acceleration.py` и его тесты, чтобы он выпускал `v7.diagnosis-owner-resolution.v1` record. При необходимости добавить CLI/report projection через существующий `tools/v7-control-plane-governance-check`. Новый Runtime, Planner, Authority, Wake, Restore Barrier или отдельный owner не нужны.

## 2. Current Diagnosis Architecture

Diagnosis в V7 расположен между Incident и Decision Model / Planner / Authority. Он не должен выполнять действие, выбирать target, выдавать authority, запускать Runtime, подтверждать Verification или закрывать Rollback. Его работа — объяснить, что доказано, что неизвестно, кто является owner, где первый divergence, и какая terminal owner-resolution classification применима.

Канонический pipeline для Diagnosis:

| Stage | Current status | Evidence | Notes |
| --- | --- | --- | --- |
| Observation | Implemented | `tools/v7-users-autoswitch._current_channel_failure_evidence`, Observation domains in certification corpus | Produces observed facts and confirmed failure evidence. |
| Health Evidence | Implemented | `tools/v7-egress-diagnose`, service/quality/readiness state, `test_v7_egress_diagnose.py` | Produces health facts such as `diagnose_severity`, `diagnose_reason`. |
| Incident | Implemented | Domain 10 certification, `tools/v7-users-autoswitch` incident source/context logic | Preserves incident identity and scope. |
| Diagnosis | Partial | Domain 11 certification, Function Graph, diagnostic helpers | Architecture exists; no single diagnosis record / owner-resolution projection. |
| Owner Resolution | Partial | `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`, `docs/reports/engineering/2026-07-03_084803_owner_resolution_law.md`, Current Program State | Law and report practice exist; executable projection/storage remains missing. |
| Decision Model | Implemented | Domain 12 certification | Consumes diagnosis semantics but should not produce diagnosis truth. |
| Planner | Implemented | Domain 14 certification, `tools/v7-users-autoswitch` | Consumes evidence and blockers; not root-cause owner. |
| Authority | Implemented | Domain 15 certification | Consumes policy/risk/diagnosis; not diagnosis owner. |
| Runtime | Implemented | Domain 17 certification | Executes or stops; not diagnosis owner. |
| Verification | Implemented | Domain 18 certification | Produces verification result; diagnosis may interpret blockers later. |
| Rollback | Implemented | Domain 19/20 certification | Consumes terminal conditions; not diagnosis producer. |
| Learning | Implemented | Domain 21 certification | Consumes outcomes and evidence. |
| Current Program State | Partial | `docs/programs/V7_CURRENT_PROGRAM_STATE.md` exposes Blocking Owner, Owner Resolution State, Terminal Root Cause | It can consume owner-resolution output but currently receives report/manual synchronized values. |
| Production Maturity | Partial | Certification reports and program docs | It can consume diagnosis evidence but no executable diagnosis projection is present. |

Current architecture is correct: Diagnosis must stay separate. The gap is implementation closure.

## 3. Existing Implementation Map

| Responsibility | Current owner | Implementation location | Evidence | Consumers | Status |
| --- | --- | --- | --- | --- | --- |
| Egress health evidence collection | `tools/v7-egress-diagnose` | `tools/v7-egress-diagnose`; `tests/unit/test_v7_egress_diagnose.py` | Produces `egress-diagnose.state` with severity/reason such as `interface_down_or_missing`. | `v7-state`, autoswitch, readiness tools, admin views | Implemented |
| Current channel failure evidence | `tools/v7-users-autoswitch` | `_controlled_certification_failure_context`, `_current_channel_failure_evidence` | Emits `schema_version`, `wake_source`, `channel`, `affected_users_on_channel`, `diagnose_reason`, `source_object`, `owner`. | Wake, Incident, Planner, Authority path | Implemented |
| Candidate/blocker generation | `tools/v7-users-autoswitch` | gate methods such as `_gate_egress_health`, `_gate_load`, `_gate_safety`; selected moves diagnostics | Emits blockers/reasons and selected move diagnostics. | Planner/Authority/Runtime chain | Implemented |
| Local root-cause status projection | `tools/v7-control-plane-governance-check` | `e936_egress_1_root_cause_status`, `e941_post_policy_egress_1_root_cause_status`, `e944_delayed_restore_root_cause_status`, `e11_4_wireguard_diagnose_decision_status` | Reads specific report artifacts and emits local root-cause classifications/confidence. | Governance check output, engineering/operator review | Partial |
| Admin diagnostic read model | `admin_core/diagnostic_views.py` | `DiagnosticSnapshot`, `traffic_zero_summary`, `client_speed_summary`, `killswitch_summary`, `capacity_state`, `diagnostic_schema_contracts` | Read-only schema contracts; tests verify no mutation surface. | Admin API, UI, operator visibility | Implemented for admin diagnostics; Partial for Domain 11 |
| Confidence/root-cause-adjacent analysis | `admin_core/operator_execution_pipeline.py` | `autonomy_confidence_component_review_model`, `_confidence_component_root_causes` | Identifies limiting confidence components. | Operator execution pipeline/read models | Partial |
| Read-only attribution without root cause claim | `admin_core/autonomy_trust_acceleration.py` | `build_observed_degradation_attribution` and related B/C models | Explicitly sets `root_cause_claimed: False`, blocks Runtime/Authority, preserves read-only diagnosis. | Engineering Automation, tests, inventory | Partial |
| Owner Resolution law | Canonical docs / Engineering Reports | `docs/reference/V7_MASTER_PROJECT_HANDOFF.md`; `docs/reports/engineering/2026-07-03_084803_owner_resolution_law.md` | Defines terminal classifications: `POLICY_PROHIBITION`, `IMPLEMENTATION_MISSING`, `OWNER_INVOCATION_MISSING`, `IMPLEMENTATION_DEFECT`, `CANONICAL_IMPOSSIBILITY`. | OMP, CPS, Engineering Automation, certification program | Implemented as law; Missing as executable projection |
| Owner Resolution records | Engineering Reports / Current Program State | `docs/reports/engineering/*owner_resolution*`; `docs/programs/V7_CURRENT_PROGRAM_STATE.md` | Reports manually record owner, terminal classification, root cause, required resolution. | Human/Codex, CPS, Production Maturity | Partial |
| Machine-readable Diagnosis Record | None found as closed owner | No `diagnosis_record`, `owner_resolution_state` schema owner found in code | Domain 11 certification explicitly reports no single executable diagnosis owner. | OMP, CPS, Production Maturity, Engineering Automation | Missing |
| Diagnosis persistence | Engineering Reports and CPS text | Reports preserve evidence; CPS exposes latest state manually | No durable indexed diagnosis object found. | CPS, PM, OMP | Partial |
| Diagnosis tests | Scattered tests | `test_v7_egress_diagnose.py`, `test_api5_runtime_route_diagnostic_views.py`, `test_autonomy_trust_acceleration.py` | Tests health diagnosis, admin read-only diagnostics, root-cause-adjacent attribution; no end-to-end Owner Resolution record tests. | CI/unit test suite | Partial |

## 4. Missing Responsibilities

| Responsibility | Existing evidence | Missing part | Required status to certify |
| --- | --- | --- | --- |
| Diagnosis object | Domain 11 defines outputs; reports contain narrative diagnosis. | No stable schema such as `v7.diagnosis-owner-resolution.v1`. | Implement machine-readable read-only record. |
| Diagnosis projection | Governance check/admin views expose local diagnostic/status summaries. | No unified projection from incident/evidence/blocker to diagnosis result. | Add one read-only projection through existing Engineering Automation / OMP path. |
| Owner Resolution executable loop | Owner Resolution Law and report examples exist. | No function/model that classifies a blocker into the terminal Owner Resolution states. | Add deterministic classifier/projection for owner blocks. |
| Blocking owner classification | Current Program State can display it; governed tools can emit `blocking_owner`. | No reusable classification object with owner, root cause, required resolution, evidence refs. | Emit terminal classification and required resolution fields. |
| First divergence | Forensic reports repeatedly compute it manually. | No generic field/projection in Domain 11 implementation. | Add optional `first_divergence` field and preserve `UNKNOWN` when not proven. |
| Unknown preservation | Laws define it; stale-read models preserve read-only diagnosis. | Diagnosis record does not exist to carry `UNKNOWN` forward. | Add explicit unknown/missing-evidence states. |
| Evidence quality/confidence | Local helpers emit confidence; research requires backtesting. | No shared confidence/evidence-quality field for diagnosis record. | Add confidence/evidence_quality with evidence refs. |
| Diagnosis consumers | OMP, CPS, Production Maturity are known consumers. | They consume report/manual values, not canonical diagnosis output. | Project diagnosis output into existing consumers. |
| Diagnosis tests | Adjacent tests exist. | No tests for owner-resolution terminal classification and no-mutation diagnosis record. | Add focused unit tests and fixture tests. |
| Analyzer backtesting | R3 defines analyzer backtesting model. | Diagnosis analyzer is not yet backtested as a generic Owner Resolution analyzer. | Backtesting can be future work; first certification only needs deterministic read-only projection for known evidence/blocker cases. |

## 5. Root Cause of NOT CERTIFIED

Stage 1 classified Domain 11 as `NOT CERTIFIED` because the implementation is not closed.

Exact missing implementation:

`No executable, read-only Diagnosis / Owner Resolution projection exists that consumes the current incident/evidence/blocker artifacts and emits a stable machine-readable Diagnosis Record with owner, terminal classification, evidence refs, confidence, unknown handling, first divergence when proven, required resolution, and downstream consumer projection.`

This is not:

- an Incident architecture defect;
- a Planner defect;
- an Authority defect;
- a Runtime defect;
- a Verification defect;
- a Rollback defect;
- a need for new owners.

The missing part is the bridge from already-existing evidence/report/status fragments into one canonical Diagnosis / Owner Resolution output.

Why reports are insufficient: Engineering Reports preserve evidence but are not a reusable executable owner. Domain 11 certification explicitly rejected “reports alone satisfy Diagnosis” because reports do not provide a stable, machine-readable object that OMP, Current Program State, Production Maturity and Engineering Automation can consume.

## 6. Minimal Implementation Mission

Mission name:

`IMPLEMENT_EXECUTABLE_READ_ONLY_DIAGNOSIS_OWNER_RESOLUTION_PROJECTION`

Mission scope:

Implement only the smallest read-only Diagnosis / Owner Resolution projection required to make Domain 11 certifiable.

Do not create:

- new Runtime;
- new Planner;
- new Authority;
- new Wake owner;
- new Restore Barrier owner;
- new mutation path;
- new production automation;
- new root-cause authority.

### Item 1 — Diagnosis / Owner Resolution Record Builder

| Field | Value |
| --- | --- |
| Owner | Existing Engineering Automation read-model owner |
| Files | `admin_core/autonomy_trust_acceleration.py`; `tests/unit/test_autonomy_trust_acceleration.py` |
| Reason | This file already owns read-only automation/trust models, preserves no-mutation guarantees, models stale-read diagnosis, and has tests proving read-only behavior. |
| Expected output | New read-only model, e.g. `schema_version: v7.diagnosis-owner-resolution.v1`, with `diagnosis_status`, `subject`, `source_object`, `evidence_refs`, `symptom`, `root_cause`, `root_cause_proven`, `unknown_state`, `blocking_owner`, `owner_resolution_state`, `terminal_classification`, `first_divergence`, `confidence`, `evidence_quality`, `required_resolution`, `consumers`, `read_only: true`, `runtime_mutation_performed: false`, `authority_expanded: false`. |
| Consumers | OMP, Current Program State, Production Maturity, Engineering Automation, Engineering Reports, future Domain 11 recertification. |
| Tests required | Unit tests for every terminal classification; unknown preservation; no root-cause claim without evidence; no mutation; consumer fields present. |

### Item 2 — Existing Evidence Adapter

| Field | Value |
| --- | --- |
| Owner | Existing evidence/report read-model owners |
| Files | `admin_core/autonomy_trust_acceleration.py`; optionally `admin_core/operator_observability.py` if operation/report evidence lookup is needed |
| Reason | Diagnosis needs to consume existing artifacts without becoming a new truth source. |
| Expected output | Adapter that accepts existing report/blocker/evidence dictionaries and maps them into the diagnosis record without recomputing Planner/Runtime decisions. |
| Consumers | Diagnosis record builder. |
| Tests required | Fixture tests for known examples: policy prohibition, implementation missing, owner invocation missing, implementation defect, canonical impossibility candidate, unknown/missing evidence. |

### Item 3 — Governance / Report Projection

| Field | Value |
| --- | --- |
| Owner | Existing governance check / report projection owner |
| Files | `tools/v7-control-plane-governance-check`; optional tests if this tool has test coverage or fixture-based checks |
| Reason | This tool already reads root-cause artifacts and emits governance projections; it can expose the new diagnosis record without owning Runtime/Planner/Authority. |
| Expected output | A read-only CLI/status projection that prints or embeds the diagnosis owner-resolution record for engineering reports and certification recovery. |
| Consumers | Engineering Reports, OMP status synchronization, Current Program State / Production Maturity synchronization. |
| Tests required | Ensure projection does not mutate state and preserves diagnosis record fields. |

### Item 4 — Consumer Projection Contract

| Field | Value |
| --- | --- |
| Owner | Existing OMP / CPS / Production Maturity consumers |
| Files | Minimal existing read-model/projection files only if required by current implementation; no canonical document rewrite in the implementation task unless explicitly requested. |
| Reason | Domain 11 needs proof that the diagnosis record is consumable by downstream owners. |
| Expected output | Consumers can read `blocking_owner`, `owner_resolution_state`, `terminal_classification`, `terminal_root_cause`, `required_resolution`, and `evidence_refs` from the same diagnosis object. |
| Consumers | OMP, CPS, Production Maturity. |
| Tests required | Consumer fixture test or contract test proving field availability and no duplicate/manual-only state source. |

Minimality decision:

The smallest certifying change is not a new service or new owner. It is a read-only record/projection added to existing Engineering Automation / governance read-model owners. That closes the implementation/ownership gap while preserving the current architecture.

## 7. Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Diagnosis accidentally becomes Authority | Unsafe production mutation from diagnostic output. | Keep record `read_only: true`; assert no Runtime/Authority expansion; tests must reject mutation fields. |
| Root cause claimed without proof | Violates Detection Is Not Diagnosis. | Use `root_cause_proven: false` and `unknown_state` unless evidence refs satisfy rule. |
| Reports remain the only source | Domain 11 stays NOT CERTIFIED. | Builder must emit machine-readable object, not only narrative markdown. |
| Overbuilding a new owner | Violates Existing Owner Before New Owner. | Reuse `admin_core/autonomy_trust_acceleration.py` and governance/read-model paths. |
| Misclassification of owner block | Wrong engineering mission produced. | Terminal classification tests for all Owner Resolution states. |
| Consumer drift | CPS/PM/OMP read different diagnosis facts. | Single diagnosis record must be the source projection for consumers. |

## 8. Required Tests

Minimum required tests:

1. `POLICY_PROHIBITION` classification from a known policy block.
2. `IMPLEMENTATION_MISSING` classification from a missing capability/owner implementation blocker.
3. `OWNER_INVOCATION_MISSING` classification from a missing invocation/propagation blocker.
4. `IMPLEMENTATION_DEFECT` classification from a violated existing-owner contract.
5. `CANONICAL_IMPOSSIBILITY` remains possible only when explicitly proven; ordinary blockers must not become impossibility.
6. Unknown/missing evidence remains `UNKNOWN` and does not become pass/fail/root cause.
7. First divergence is present when evidence proves it and omitted/unknown when not proven.
8. Diagnosis record preserves source object / operation identity.
9. Diagnosis record contains downstream consumer fields for OMP, CPS and Production Maturity.
10. Diagnosis record is read-only: no subprocess mutation, no Runtime apply, no Authority expansion, no synthetic evidence, no user movement.
11. Governance/report projection exposes the same record without recomputing or rewriting diagnosis truth.
12. Regression test proves existing health diagnosis, autoswitch, Authority, Runtime, Verification and Rollback behavior are unchanged.

Candidate test files:

- `tests/unit/test_autonomy_trust_acceleration.py`
- `tests/unit/test_api5_runtime_route_diagnostic_views.py` if admin diagnostic contracts are extended
- a new focused unit test file only if existing test files cannot reasonably own the new model tests

## 9. Expected Certification Result

After the minimal implementation mission:

- Domain 11 architecture should remain unchanged.
- Function Graph should show a closed read-only Diagnosis / Owner Resolution projection.
- Stage 1 recertification should no longer find `IMPLEMENTATION_GAP` for the core diagnosis object.
- Stage 1 recertification should no longer find `OWNERSHIP_GAP` for owner-resolution projection.
- Domain 11 should move from `NOT CERTIFIED` to `CERTIFIED`, assuming tests pass and no new evidence contradicts the architecture.

Expected result after implementation:

`CERTIFIED`

## 10. Stage 1.2 Readiness

Stage 1.2 is ready to proceed to implementation planning, but not implementation in this discovery task.

Readiness:

| Item | Status |
| --- | --- |
| Root cause understood | READY |
| Minimal implementation mission defined | READY |
| New owner required | NO |
| Architecture redesign required | NO |
| Code patch performed now | NO |
| OMP / Knowledge Consolidation modified now | NO |
| Production changes performed now | NO |
| Next step | Execute the minimal implementation mission through existing Engineering Automation / OMP / governance read-model owners, then rerun Domain 11 certification. |

Final discovery verdict:

`DIAGNOSIS_RECOVERY_DISCOVERY_COMPLETE`
