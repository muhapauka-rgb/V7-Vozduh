# V7 Autonomy Blueprint

Status: permanent autonomy engineering reference  
Program: `V7.AUTONOMY.BLUEPRINT.1_FULL_SYSTEM_MAP_AND_GAP_PLAN`  
Date: 2026-06-22  
Workspace: `/Users/ponch/Documents/New project`  
Branch: `Updatesystem`  
Blueprint base commit: `0d0de83c85ed51908933afe518b4012c319de11a`

This document is the complete autonomy blueprint for V7. It describes the current system architecture, dependency flows, maturity state, hidden or disconnected systems, and the safe roadmap from operator-driven control to production event-driven autonomy.

It is not an implementation plan for immediate apply. It does not authorize user movement, daemon enablement, autoswitch enablement, production writes, threshold changes, floor changes, planner changes, governance changes, or execution changes.

## 1. Current Architecture Verdict

V7 already has most of the structural pieces of a production autonomy system:

- observation and probes;
- service matrix;
- route/runtime/capacity/readiness models;
- planner and assignment decision;
- governed execution path;
- restore barrier;
- rollback model;
- feedback and learning stores;
- intelligence snapshots;
- trust evolution;
- prediction model;
- shadow/operator comparison path;
- operator UI and decision surfaces;
- truth/convergence gates.

The current gap is not "missing planner" or "missing execution". The current gap is evidence maturity and event binding:

```text
Regression event exists
  -> planner preview exists
  -> execution packet preview exists
  -> restore/rollback/feedback owners exist
  -> observed outcome, trust, and prediction evidence are not mature enough
  -> read-only event consumer is certified but not an apply authority
  -> production autonomy remains disabled
```

Current autonomy verdict:

`EVENT_DRIVEN_AUTONOMY_ARCHITECTURE_PARTIAL_NOT_READY_FOR_OPERATOR_FREE_PRODUCTION`

Current production alignment:

- AUTONOMY.FINAL.BRANCH_1B deployed the Branch 1A blast visibility fix through the existing safe deploy owner.
- Local/GitHub/runtime are aligned at `c4adc537b39e0335ad9cc0cf7ff9589d85860d60`.
- `tools/v7-truth-check --all --json` reports `PASS`; `tools/v7-convergence-status --json` reports `ALIGNED`.
- The approved snapshot-only blast recovery write completed with `blast_radius_evidence_count=11`, `blast_radius_confidence=100.0`, `trust_score=54.684`, `execution_allowed_now=false`, `apply_executed=false`, and `users_moved=0`.
- AUTONOMY.TRUST.BUILDOUT.1 later re-read the current consumed autonomous dry-run and found `blast_radius_confidence=0.0`, `trust=39.582`, `confidence=45.8`, and `prediction_confidence=39.6`. Branch 1B remains proven and closed.
- AUTONOMY.TRUST.DURABILITY.1 fixed the normal refresh code path so active JSONL files and numeric rotations are consumed as one evidence family. Local lifecycle proof and production refresh both show recovered blast evidence survives refresh/rebuild/reread with `blast_radius_confidence=100.0`.
- AUTONOMY.TRUST.ACCELERATION.1 added a deployed read-only evidence inventory owner. Final production inventory after refresh reports `21/21` prediction matches, `0` pending prediction rows, `0` operator comparisons, earned confidence `45.802`, trust `54.704`, and canary readiness blocked. Runtime deploy aligned to `43effb2a7a58a545fd90d48db53bbe1c0968a75b` before documentation-only updates.
- AUTONOMY.TRUST.SOURCE.REALITY.1 corrected the trust-source hierarchy: observed network outcome is primary; operator comparison is secondary supervised confirmation only when the operator has enough context. Blind operator training history is forbidden.
- EVENT.CONSUMER.READONLY.2 certified the read-only event consumer link from real production events to planner, packet, restore barrier, rollback, feedback, and learning previews. It did not enable apply, daemon, autoswitch, movement, new truth source, or synthetic evidence.
- AUTONOMY.CANARY.1_READINESS_RECHECK returned `AUTONOMY_CANARY_NO_GO`. Current production floors are confidence `39.606`, trust `54.705`, prediction confidence `36.859`, and secondary operator earned confidence `45.807`, all below the `70.0` canary floor. Event consumer remains certified read-only, blast and rollback confidence are `100.0`, but planner observe selected `0` moves and the snapshot gate stopped on `service-scores` / `channel-service-scores` source mismatch. No apply, daemon, autoswitch, movement, synthetic evidence, or new truth source occurred.
- AUTONOMY.CANARY.1A returned `CANDIDATE_VISIBILITY_BLOCKED`. It found real planner pressure (`candidate_moves_total=18`; `awg3=8`, `wireguard-1779454504-c43409=8`, `vless=10`) and proved that existing planner-owned `--pre-planner-refresh=write` clears snapshot gate inside observe without apply/user movement. However, normal observe still reverts to `dry_run_intelligence_snapshot_stop_required`, while the planner-owned refresh observe stops later at `dry_run_restore_barrier_clearance_generation_expired`. The next phase is an existing-owner planner/snapshot lifecycle durability fix, not a new planner or autonomy system.
- AUTONOMY.CANARY.1B deployed the existing-owner normal observe snapshot lifecycle fix in `tools/v7-users-autoswitch`. Production normal observe now clears snapshot gate (`stop_required=false`, `stop_families=[]`) and exposes real current candidates (`candidate_moves_total=8`) before stopping at `dry_run_restore_barrier_clearance_generation_expired`. A fresh one-user canary packet preview for `10.0.0.2 awg3 -> wireguard-1779454504-c43409` validates as `PACKET_VALID`, but the current restore-barrier clearance is expired and tied to an obsolete 10-user `vless` plan. Verdict: `CANARY_BLOCKED_BY_RESTORE`.
- AUTONOMY.CANARY.1C implemented read-only restore-barrier runtime action preview through the existing `admin_core/operator_execution.py` owner. Production now proves that the fresh one-user canary packet can obtain valid clearance preview (`ALLOW_RESTORE_BARRIER_CLEARANCE`, `RESTORE_BARRIER_CLEARANCE_PREVIEW_VALID`) and survive reread/explicit snapshot refresh without writing barrier state, applying autoswitch, or moving users. Canary is now blocked by confidence/trust/prediction floors: confidence `39.558`, trust `54.668`, prediction confidence `36.511`, and secondary operator earned confidence `45.837`. Verdict: `CANARY_BLOCKED_BY_CONFIDENCE`.
- AUTONOMY.CANARY.1D added deployed read-only floor forensics/materialization audit to `admin_core/autonomy_trust_acceleration.py`. Production after deploy `2915a4b8107d1fbd416661e562511a6ca2a864fe` proves current floor values remain low: confidence `37.402`, trust `53.051`, prediction confidence `33.753`, operator earned confidence `45.908`. Prediction is fully matched (`21/21`, `0` pending) but under-confident (`mean_forecast_confidence=0.3561`). Service rows are matched but low-confidence (`service_confidence=36.079`); candidate suitability has real but incomplete/low-confidence outcomes (`83/156`, suitability `26.126`). No safe immediate evidence/materialization fix can raise floors without new real evidence.

## 2. Full System Inventory

| Subsystem | Owner | Main files | Purpose | Status | Maturity | Certification State |
| --- | --- | --- | --- | --- | ---: | --- |
| Reference / ADR system | Documentation workflow | `docs/reference/V7_CANONICAL_REFERENCE.md`, `docs/reference/SYSTEM_MAP.md`, `docs/decisions/` | Preserve current truth and decisions | ACTIVE | 95% | Reference-first rule accepted |
| Truth / Convergence | Truth owner | `tools/v7-truth-check`, `tools/v7-convergence-status`, `tools/v7_sync_lib.py` | Local/GitHub/runtime/deploy alignment | ACTIVE | 100% | PASS / ALIGNED after Branch 1B deploy |
| Observation | Runtime tools and admin read models | `tools/v7-egress-quality-compact`, `tools/v7-service-matrix-refresh-all`, `tools/v7-telegram-sentinel`, `admin_core/*_views.py` | Observe service, quality, route, runtime, capacity, state | ACTIVE | 90% | Certified as read-only sources |
| Service Matrix | Service health owner | `tools/v7-service-matrix-refresh-all`, `tools/v7-service-matrix-test`, `admin_core/service_views.py` | Per-channel service availability/freshness | ACTIVE | 90% | Periodic refresh exists; manual targeted refresh exists |
| Telegram Sentinel | Event source | `tools/v7-telegram-sentinel`, `systemd/v7-telegram-sentinel.*` | Fast Telegram regression/source signal | ACTIVE as source | 75% | Service uses `--no-autoswitch`; not certified as apply trigger |
| Telemetry / Quality | Quality compact owner | `tools/v7-egress-quality-compact`, `tools/runtime-support/v7-egress-stability`, quality summary/ring | Avg/min Mbps, latency, fail rate, stability/history | ACTIVE | 85% | Periodic compaction exists |
| Capacity / Load | Planner/read model | `tools/v7-users-autoswitch`, `admin_core/diagnostic_views.py`, `admin/v7-admin-api` | Assignment pressure against limits | ACTIVE | 85% | Canonical semantics locked by ADR-009 |
| Observed Capacity Shadow | Future intelligence concept | Future owner should reuse `tools/v7-egress-quality-compact`, `admin_core/intelligence_workers.py`, `admin_core/shadow_autonomy.py` | Learn practical capacity from observed quality at user counts | APPROVED_CONCEPT_ONLY | 35% | ADR-011 accepted; not runtime behavior |
| Route Reality | Route read model | `admin_core/route_reality_views.py`, `admin_core/route_views.py` | Route readiness/topology/leak/mismatch evidence | ACTIVE | 80% | Supporting signal, not first-level traffic-quality truth |
| Runtime Readiness | Runtime read model | `admin_core/runtime_read_views.py`, `admin_core/operator_execution_pipeline.py` | Runtime state, snapshot readiness, operation wiring | ACTIVE | 85% | Truth known; current runtime mismatch blocks alignment |
| Channel Decision V7 | Planner/operator adapter | `tools/v7-users-autoswitch`, `admin_core/operator_decision_surface.py`, `admin/v7-admin-api` | Use/Evacuate/Keep/Emergency/Blocked operator answer | ACTIVE | 90% | Planner-first semantics locked |
| Channel Score / Technical Health | Diagnostics | `admin/v7-admin-api`, `admin_core/diagnostic_views.py` | Mixed diagnostic score and reality-first explanation | ACTIVE | 85% | Diagnostics-only ADR accepted |
| Planner / Autoswitch | Planner owner | `tools/v7-users-autoswitch` | Candidate ranking, blockers, selected moves, dry-run/apply path | ACTIVE | 95% | Governed execution certified up to 10 users; apply service inactive |
| Policy / Groups | Policy owner | `tools/v7-users-autoswitch`, `tools/runtime-support/v7-policy-*`, `admin/v7-admin-api` | Policy, group, route, and access constraints | ACTIVE | 80% | Existing policy tools; not fully mapped in autonomy evidence |
| Execution Packet | Packet owner | `tools/v7-operator-execution-packet`, `admin_core/operator_execution_pipeline.py` | Prepare bounded execution packet before apply | ACTIVE | 90% | Preview path works; live autonomy blocked |
| Restore Barrier | Safety owner | `tools/v7-restore-settle-gate`, `tools/v7-operator-execution-packet`, `admin_core/operator_execution.py` | Pre-apply restore boundary, approved plan lock, settle gate, and read-only clearance preview | ACTIVE | 95% lifecycle / 80% canary readiness | AUTONOMY.CANARY.1C proves fresh clearance preview is valid and durable across reread/refresh without writes; canary remains blocked by confidence/trust/prediction evidence floors |
| Governed Execution | Runtime execution owner | `admin_core/operator_execution.py`, `tools/v7-users-autoswitch --apply` | Apply selected moves under governance | ACTIVE_BUT_MANUAL | 90% | BA1/BA3/BA4 certified up to 10 users; production daemon disabled |
| Rollback | Rollback owner | `admin_core/operator_execution.py`, `tools/v7-users-autoswitch --rollback-packet --apply --verify` | Rollback packet/decision after failed or unsafe movement | PARTIAL_ACTIVE | 80% | Model exists; live rollback packet not certified for operator-free autonomy |
| Feedback | Feedback owner | `admin_core/operator_execution_feedback.py`, execution/closure JSONL stores | Post-action outcome evidence | ACTIVE | 85% | Governed evidence consumed; active stores can be empty/rotated |
| Learning | Intelligence/trust owners | `admin_core/intelligence_platform.py`, `admin_core/intelligence_workers.py`, `admin_core/intelligence_snapshots.py` | Convert outcomes into trust, prediction, suitability, blast confidence | ACTIVE_PARTIAL | 70% | Evidence consumed; quality insufficient |
| Prediction | Prediction owner | `admin_core/intelligence_workers.py`, `admin_core/intelligence_platform.py`, `admin_core/autonomy_trust_acceleration.py` | Forecast -> actual confidence | ACTIVE_PARTIAL | 50% evidence quality / 80% evidence durability / 95% inventory visibility | 21/21 matched and 0 pending rows; governed prediction feedback survives lifecycle; floor forensics proves low source confidence keeps production result near 34 |
| Trust Evolution | Trust owner | `admin_core/intelligence_platform.py`, `admin_core/intelligence_workers.py`, `tools/v7-intelligence-snapshot-refresh` | Outcome confidence/trust aggregation | ACTIVE_PARTIAL | 55% proven recovered trust / durable refresh deployed | Branch 1B proved trust `54.684`; TRUST.DURABILITY.1 fixed, deployed, and refreshed the lifecycle that had dropped rotated evidence from current consumed reads |
| Blast Radius | Blast evidence owner | `admin_core/intelligence_workers.py::build_blast_radius_evidence_rows`, `blast_radius_confidence_model`, `tools/v7-intelligence-snapshot-refresh` | Prove small governed operations are safe | OPERATIONALLY_CLOSED_DURABILITY_FIXED | 100% recovery proven / 100% durable production refresh | Branch 1B deployed and recovered 11 real blast rows; TRUST.DURABILITY.1 production refresh reads 11 rows and blast confidence `100.0` |
| Shadow Autonomy | Shadow owner | `admin_core/shadow_autonomy.py`, `admin_core/autonomy_trust_acceleration.py`, `/api/actions/shadow-autonomy-compare` | Compare recommendations with operator decisions when context is sufficient | ACTIVE_SECONDARY_PATH_READY_UNDERFED | 70% path / 25% evidence | Review packet, eligibility, growth projection, rotated shadow JSONL reads, UI visibility, and read-only review batches exist; comparison count is still 0, and comparison is secondary |
| Operator Comparison | Shadow comparison store | `admin_core/shadow_autonomy.py`, `admin_core/autonomy_trust_acceleration.py`, shadow JSONL family | Secondary supervised confirmation | ACTIVE_SECONDARY_PATH_READY_EMPTY | 70% path / 25% evidence | Current comparison evidence below floor; use only for contextual supervised confirmation, not blind bulk training |
| Trust Evidence Inventory | Read-only acceleration owner | `admin_core/autonomy_trust_acceleration.py`, `tools/v7-autonomy-trust-evidence-inventory` | Summarize current evidence, growth opportunities, review batches, canary proximity, floor forensics, and materialization audit | ACTIVE_READ_ONLY | 95% | AUTONOMY.CANARY.1D deployed and verified floor forensics; creates no evidence and performs no runtime mutation |
| Trust Source Hierarchy | Read-only trust model semantics | `admin_core/autonomy_trust_acceleration.py`, `docs/decisions/ADR-OBSERVED-OUTCOME-PRIMARY-TRUST.md` | Primary vs secondary vs diagnostic evidence classification | ACTIVE | 90% | Observed outcome is primary; operator comparison is secondary supervised confirmation |
| Event Detection | Event sources plus certified read-only binding | `tools/v7-telegram-sentinel`, service matrix, quality compact, route/runtime/capacity readers, `admin_core/events.py` | Detect and classify regression source facts | ACTIVE_READ_ONLY | 85% | Sources exist and classify into primary/secondary/diagnostic event classes |
| Event Consumption | Certified read-only consumer | `admin_core/events.py`, `admin_core/operator_execution_pipeline.py::event_consumer_readonly_certification_model` | Bind regression event to planner/packet/restore/rollback/feedback/learning previews | ACTIVE_READ_ONLY | 80% | EVENT.CONSUMER.READONLY.2 certified; AUTONOMY.CANARY.1_READINESS_RECHECK confirms live apply still blocked |
| Autonomous Runtime | Runtime service/timer | `systemd/v7-users-autoswitch.service`, `systemd/v7-users-autoswitch.timer` | Continuous apply service if enabled | DORMANT_BY_DESIGN | 35% | Inactive and approved manual mode; canary recheck still NO-GO |
| Admin UI / Operator Layer | Operator surface | `admin/v7-admin-api`, `admin_core/operator_decision_surface.py` | Decision-first operator visibility and actions | ACTIVE | 85% | Channel/User/Attention UX mostly mature |
| Governance | Execution pipeline | `admin_core/operator_execution_pipeline.py`, packet/restore/truth gates | Enforce floors, safety, action authority | ACTIVE | 85% | Floors block autonomy correctly |
| Identity / Users | Registry owner | `admin_core/admin_registry_views.py`, `admin/v7-admin-api`, user registry | User state, current channel, profile, policy context | ACTIVE | 85% | Operator surface mature; movement remains governed |
| Groups / Policies | Runtime support and planner | `tools/runtime-support/v7-policy-*`, planner policy gates | Multi-tenant/access/policy boundaries | ACTIVE_PARTIAL | 75% | Exists, but autonomy blueprint needs deeper future policy audit |

## 3. Dependency Graphs

### Observation Flow

```text
Runtime / channel state
  -> service matrix refresh
  -> quality compact / stability
  -> route reality
  -> runtime readiness
  -> capacity/load
  -> admin read models
  -> operator surfaces and planner context
```

### Decision Flow

```text
Users + channels + policies + service/quality/route/runtime/capacity evidence
  -> tools/v7-users-autoswitch
  -> candidate ranking
  -> blockers
  -> selected moves
  -> Channel Decision V7
  -> operator table/drawer/attention
```

### Execution Flow

```text
Planner selected moves
  -> operator/existing action approval boundary
  -> tools/v7-operator-execution-packet
  -> restore barrier / settle gate
  -> tools/v7-users-autoswitch --apply
  -> verification
  -> audit/closure
```

### Rollback Flow

```text
Applied movement / failed verification / unsafe result
  -> rollback model
  -> rollback packet
  -> restore barrier comparison
  -> rollback apply + verify
  -> closure evidence
  -> feedback / learning
```

### Learning Flow

```text
Execution events + runtime trust + proposal records + closure records
  -> intelligence snapshot refresh
  -> trust evolution summaries
  -> service/candidate/prediction/blast/rollback confidence
  -> autonomy gate inputs
```

### Trust Flow

```text
Governed outcomes
  -> decision confidence
  -> service confidence
  -> suitability confidence
  -> blast-radius confidence
  -> rollback confidence
  -> trust evolution overall confidence
  -> candidate trust floor
```

### Prediction Flow

```text
Service matrix + quality + risk + trust + blast summaries
  -> prediction forecasts
  -> later service/channel actuals
  -> matched forecast accuracy
  -> prediction confidence
  -> autonomy gate prediction floor
```

### Operator Flow

```text
Overview / Attention / Users / Channels
  -> decision-first table
  -> drawer
  -> inline problem/action explanation
  -> existing safe destination
  -> governed action path if execution is needed
```

### Autonomy Flow

```text
Regression event
  -> event consumer
  -> planner preview
  -> candidate gates
  -> execution packet
  -> restore barrier
  -> bounded apply
  -> verification
  -> rollback decision
  -> feedback
  -> learning
  -> trust growth
```

Current live-apply break after EVENT.CONSUMER.READONLY.2:

```text
Regression event
  -> read-only consumer certified
  -> snapshot/candidate visibility clear
  -> restore-barrier clearance preview valid
  -> gates fail confidence/trust/prediction/comparison
  -> no operator-free apply
```

### Event Flow

```text
Telegram sentinel / service matrix / quality compact / route/runtime/capacity regression
  -> read-model evidence
  -> operator surface and dry-run APIs
  -> not yet certified as live production apply trigger
```

### Blast Radius Flow

```text
Governed execution outcomes
  -> active or rotated feedback stores
  -> build_blast_radius_evidence_rows
  -> blast_radius_confidence_model
  -> trust_evolution_summary
  -> autonomy trust input
```

Branch 1A fixed the visibility break and Branch 1B deployed/recovered it in production:

```text
full decision_records
  -> blast_radius_records
  -> 11 rows
  -> blast_radius_confidence = 100.0
```

AUTONOMY.TRUST.BUILDOUT.1 durability caveat:

```text
Branch 1B recovered blast evidence
  -> later current consumed autonomous dry-run
  -> blast_radius_confidence = 0.0
  -> trust = 39.582
  -> trust durability phase required and completed by AUTONOMY.TRUST.DURABILITY.1
```

AUTONOMY.TRUST.DURABILITY.1 fixed lifecycle:

```text
active JSONL + numeric rotations
  -> normal snapshot refresh
  -> trust-evolution-summaries
  -> write snapshots
  -> reread snapshots
  -> blast_radius_confidence = 100.0 in local durability proof
  -> blast_radius_confidence = 100.0 in production refresh proof
```

### Confidence Flow

```text
candidate confidence
outcome confidence
operator comparison confidence
prediction confidence
trust confidence
rollback confidence
  -> autonomy_engine_trace_model
  -> autonomous_safety_gates
  -> apply allowed only if floors pass
```

## 4. Hidden, Dormant, Forgotten, And Disconnected Systems

| System | Classification | Evidence | Meaning |
| --- | --- | --- | --- |
| `systemd/v7-users-autoswitch.service` and timer | DORMANT_BY_DESIGN | Truth says autoswitch service/timer inactive and approved manual mode | Apply-capable timer exists but must not be enabled until event-driven certification passes |
| `systemd/drafts/v7-autoswitch-planner.*` | DORMANT_DRAFT | Draft systemd files | Planner-only periodic concept exists, not production apply |
| `systemd/drafts/v7-health.service` | PARTIAL_DRAFT | Draft loop every 30s | Health loop exists as draft/read model, not autonomy controller |
| Rotated `.jsonl.1` feedback stores | ACTIVE_EVIDENCE_DURABLE_IN_PRODUCTION_REFRESH | REMATERIALIZATION.3/4, Branch 1A, Branch 1B, and TRUST.DURABILITY.1 | Real governed blast evidence is consumed as part of the existing JSONL family; production refresh now reads 11 blast rows and blast confidence `100.0` |
| Shadow operator comparison store | ACTIVE_BUT_UNDERFED | `comparisons_total=0` in root confidence evidence | Mechanism exists, evidence volume missing |
| Prediction actual matching | ACTIVE_BUT_LOW_CONFIDENCE_DURABILITY_IMPROVED | 21/21 matched, 0 pending rows, confidence around 37; governed prediction feedback lifecycle proof passes | Mechanism works and direct feedback survives refresh/write/reread; current gap is source confidence/future real evidence, not missing actuals |
| Trust acceleration inventory | ACTIVE_READ_ONLY | `tools/v7-autonomy-trust-evidence-inventory` deployed in AUTONOMY.TRUST.ACCELERATION.1 | Exposes evidence inventory and review batches; intentionally does not create comparisons, actuals, trust, apply, or movements |
| Operator comparison as primary trust | DEMOTED_TO_SECONDARY | AUTONOMY.TRUST.SOURCE.REALITY.1 / ADR-OBSERVED-OUTCOME-PRIMARY-TRUST | Operator comparison remains useful only as contextual supervised confirmation; observed outcome is primary |
| Observed Capacity Shadow | APPROVED_BUT_NOT_IMPLEMENTED | ADR-011 | Concept accepted as shadow-only future model |
| Route first-level signal | DEMOTED_SUPPORTING | ADR-007 | Route exists but should not be treated as first-level table truth unless real blocker appears |
| Technical Health | ACTIVE_DIAGNOSTICS_ONLY | ADR-003/010 | Useful, but intentionally not a primary workflow |
| Sentinel event source | SOURCE_ONLY | `--no-autoswitch` | Good regression source, not a live apply trigger |
| Legacy/raw operator actions | DEMOTED | Operator actions reports | Many "check/run" buttons were moved behind details; background intelligence should carry first-line status |
| Old untracked POOL2 docs in worktree | UNKNOWN_UNTRACKED_DOCS | `git status --short` | Left untouched; not part of this blueprint commit unless separately reviewed |

## 5. Gap Analysis Against Ideal V7 Vision

Ideal vision:

```text
User
  -> Observation
  -> Understanding
  -> Decision
  -> Execution
  -> Verification
  -> Learning
  -> Trust Growth
  -> Autonomous Execution
```

| Stage | Current V7 | Gap |
| --- | --- | --- |
| User | Strong registry/admin identity and channel state | Policy/group implications need a dedicated autonomy-policy pass |
| Observation | Strong service/quality/route/runtime/capacity sources | Event sources are not yet bound into a certified live consumer |
| Understanding | Strong operator decision surfaces and diagnostics | Some intelligence outputs remain underfed or disconnected |
| Decision | Planner and Channel Decision V7 are mature | Autonomy gate cannot rely on planner alone; confidence/trust/prediction still fail |
| Execution | Governed execution certified up to 10 users | Operator-free apply not certified and service/timer inactive |
| Verification | Restore/rollback/feedback models exist | Live rollback packet for autonomous apply is not certified |
| Learning | Feedback/trust/prediction/blast owners exist | Observed outcome evidence quality and prediction source confidence are weak |
| Trust Growth | Trust-evolution pipeline exists | Blast durability fixed, deployed, and refreshed; trust source hierarchy now prioritizes observed outcomes over blind operator comparisons |
| Autonomous Execution | Desired event-driven model is documented | Floors, comparison evidence, prediction confidence, readiness recheck, and disabled daemon remain blockers |

## 6. Industry Comparison

This comparison uses industry philosophy only. It does not import new architecture into V7.

| Industry Pattern | Relevant Principle | V7 Classification | V7 Meaning |
| --- | --- | --- | --- |
| Google SRE automation | Automate repeated operational work, but use reliable signals, guardrails, and risk-aware rollout | PARTIALLY_EXISTS_IN_V7 | V7 has probes, gates, restore/rollback, BA evidence, and a read-only event consumer; floors are not ready |
| Google SRE monitoring / golden signals | Use symptom-oriented metrics and actionable alerts | PARTIALLY_EXISTS_IN_V7 | Service/quality/capacity signals exist; operator surfaces now decision-first |
| Kubernetes controllers | Observe current state, compare to desired state, reconcile continuously | PARTIALLY_EXISTS_IN_V7 | Planner/dry-run resembles reconciliation; live controller is intentionally inactive |
| Progressive delivery / Argo Rollouts | Incremental rollout with metric analysis before promotion | PARTIALLY_EXISTS_IN_V7 | BA1/BA3/BA4 and restore barriers exist; production event-driven progressive rollout not enabled |
| Kayenta / Spinnaker canary analysis | Compare baseline/canary metrics before promotion | PARTIALLY_EXISTS_IN_V7 | Prediction and service actual comparisons exist; confidence is too low |
| Netflix automation philosophy | Automation must earn confidence through production evidence and blast containment | PARTIALLY_EXISTS_IN_V7 | Blast-radius path now proven in dry-run; autonomy still gated |
| LinkedIn recommendation systems | Use logged outcomes, offline/online evaluation, and feedback loops before ranking changes | PARTIALLY_EXISTS_IN_V7 | Shadow comparison endpoint exists but lacks current comparison volume |
| OpenAI eval systems | Treat evaluation runs as explicit evidence before deployment changes | PARTIALLY_EXISTS_IN_V7 | V7 has tests/truth/evidence reports; needs recurring eval-like outcome collection |
| Control plane systems | Separate desired state, observed state, and actuation authority | ALREADY_EXISTS_IN_V7 | V7 has read models, planner, execution packet, restore barrier, and truth gates |
| Autonomous remediation systems | Trigger from validated symptoms, act in bounded scope, verify, rollback, learn | PARTIALLY_EXISTS_IN_V7 | Architecture matches, but live event trigger and evidence floors fail |

Sources used:

- Google SRE, Automation at Google: `https://sre.google/sre-book/automation-at-google/`
- Google SRE, Monitoring Distributed Systems: `https://sre.google/sre-book/monitoring-distributed-systems/`
- Google SRE Workbook, Canarying Releases: `https://sre.google/workbook/canarying-releases/`
- Kubernetes Controllers: `https://kubernetes.io/docs/concepts/architecture/controller/`
- Argo Rollouts documentation: `https://argo-rollouts.readthedocs.io/`
- Spinnaker Canary documentation: `https://spinnaker.io/docs/guides/user/canary/`
- OpenAI Evals guide: `https://platform.openai.com/docs/guides/evals`
- LinkedIn recommender systems evidence literature: `https://arxiv.org/abs/1809.06473`

## 7. Autonomy Maturity Model

| Area | Readiness | Evidence |
| --- | ---: | --- |
| Observation | 90% | Service matrix, quality compact, sentinel, route/runtime/capacity read models exist |
| Operator understanding | 85% | Decision-first channels/users/attention surfaces implemented and documented |
| Planner | 95% | `tools/v7-users-autoswitch` is canonical planner/assignment truth |
| Policy/governance | 85% | Execution pipeline, floors, restore barrier, explicit apply boundaries |
| Governed execution | 90% | BA certifications up to 10 users; apply path exists but manual |
| Verification / restore | 85% | Restore barrier known; autonomous dry-run currently blocked |
| Rollback | 80% | Rollback model exists; live autonomous rollback not certified |
| Feedback | 85% | Feedback/closure stores and intelligence consumption exist |
| Learning | 70% | Trust/prediction/blast/suitability models exist; evidence quality uneven |
| Blast-radius evidence | 100% | Branch 1B production recovery: 11 rows, 100 confidence |
| Prediction evidence | 50% | 21/21 matched; direct governed prediction feedback is now consumed durably, but low source confidence keeps production output around 37 |
| Operator comparison | 25% | Existing endpoint/store; secondary supervised evidence only, not primary trust |
| Trust source hierarchy | 90% | Observed outcome primary, operator comparison secondary, diagnostics separate |
| Trust | 55% | Production dry-run after recovery reports trust `54.684`, below the `70.0` floor |
| Event detection | 85% | Event sources exist and the read-only consumer is certified; live apply remains blocked |
| Autonomous runtime | 45% | Architecture exists; daemon inactive; blast blocker closed; confidence/trust/prediction floors fail |
| Truth/deploy alignment | 100% | Local/GitHub/runtime aligned at `c4adc537`; truth/convergence pass |
| Overall production autonomy | 45% | Correctly blocked; no operator-free apply should run now |

## 8. What Exists, What Is Partial, What Is Missing

### Already Exists

- Canonical planner.
- Governed execution.
- Restore barrier.
- Rollback model.
- Service matrix.
- Quality/stability compaction.
- Route/runtime/capacity read models.
- Operator decision surface.
- User and Channel drawers.
- Attention layer.
- Intelligence snapshots.
- Trust evolution.
- Prediction model.
- Blast-radius evidence builder.
- Shadow comparison endpoint.
- Truth/convergence system.

### Partially Exists

- Event-driven autonomy chain.
- Contextual operator comparison evidence as secondary supervised confirmation.
- Prediction confidence evidence volume and source confidence.
- Observed Capacity Shadow.
- Progressive rollout/canary autonomy.
- Durable planner candidate visibility after service-matrix-derived snapshot refresh.
- Autonomous rollback certification.
- Policy/group autonomy mapping.

### Missing

- Live apply-capable event consumer remains disabled; read-only consumer certification is complete.
- Repeated forecast -> later actual collection loop with higher confidence.
- Higher-confidence observed service/channel outcome cycles.
- Contextual operator comparison records only where the operator has enough context.
- Formal autonomous canary ladder after all floors pass.
- Automatic but bounded production event loop that is not a blind timer.

## 8A. Current Evidence Status: 2026-06-23

`AUTONOMY.EVIDENCE.REAL_SOURCE_CONFIDENCE_COLLECTION` deployed read-only source-confidence attribution in the existing trust inventory owner (`admin_core/autonomy_trust_acceleration.py`) at runtime commit `e932356dfa714a2455f5eb404db3bea8dc78a935`.

Current production evidence verdict is `EVIDENCE_MIXED`:

- Prediction matches are complete and consumed: `21/21`, `0` pending, but prediction remains low because mean forecast confidence is `0.378`.
- Blast-radius evidence is sufficient and contributes `100.0`.
- Rollback evidence is sufficient and contributes `100.0`.
- Service outcomes exist (`21`) but are low-confidence (`0.39` mean row confidence).
- Candidate outcomes exist (`83`) but are incomplete against `156` candidates.
- Operator comparisons remain `0` and are secondary evidence only.

Current floors remain below canary target:

| Floor | Current | Target |
| --- | ---: | ---: |
| Confidence | 39.042 | 70.000 |
| Trust | 54.282 | 70.000 |
| Prediction confidence | 35.486 | 70.000 |
| Operator earned confidence | 45.862 | 70.000 |

Fastest next evidence path is real service/channel probe cycles through existing service matrix and quality snapshot owners, followed by intelligence snapshot refresh and trust inventory reread. No synthetic evidence, formula change, floor change, runtime apply, user movement, or daemon enablement is allowed for this step.

## 9. Biggest Risks

| Risk | Severity | Why |
| --- | --- | --- |
| Enabling `v7-users-autoswitch.timer` before gates pass | Critical | It would turn an apply-capable timer into mutation authority without event-driven certification |
| Treating planner readiness as autonomy readiness | High | Planner can propose; autonomy also needs observed outcome confidence, trust, prediction, restore, and rollback evidence |
| Reintroduced deploy drift after Branch 1B | Medium | Truth/convergence are currently aligned; future logic changes must keep runtime aligned |
| Synthetic evidence temptation | High | Would inflate confidence without real operator/outcome proof |
| Prediction confidence misunderstanding | Medium | AUTONOMY.CANARY.1D proves matches exist (`21/21`, `0` pending); low source confidence is the blocker |
| Forcing blind operator comparisons | High | The operator cannot truthfully judge distributed user outcomes without enough context; this would manufacture weak evidence |
| Operator comparison starvation | Low | The mechanism exists, but it is now secondary rather than the primary trust path |
| Overbuilding new owners | Medium | V7 already has owners; new planner/governance/execution would fragment truth |
| Treating timer probes as autonomous movement | Medium | Periodic probes are valid; blind movement is rejected |

## 10. Next 12 Month Roadmap

### Immediate: 0-2 Weeks

1. Keep autoswitch daemon/timer inactive.
2. Start observed service/channel outcome evidence collection through existing service/quality/prediction owners.
3. Start prediction evidence collection with real forecast -> later actual pairs.
4. Fix durable candidate visibility through the existing planner/snapshot refresh lifecycle owner, then re-run canary readiness.
5. Re-run truth/convergence after each evidence or logic change.

### Near Term: 2-8 Weeks

1. Improve prediction confidence through repeated real outcomes, not formula changes.
2. Use operator comparison only as contextual supervised confirmation through real agree/disagree/override records.
3. Recheck restore barrier and rollback preview readiness for event-triggered packets.
4. Add observability for autonomy readiness in admin without adding a new truth source.
5. Prepare an autonomous canary review only after floors pass.
6. Implement Observed Capacity Shadow as snapshot/advisory only if needed and separately approved.

### Medium Term: 2-6 Months

1. Run a bounded event-driven autonomy canary only after floors pass.
2. Start with one user / one event / one channel, explicit rollback readiness, and feedback closure.
3. Extend to small batches only after repeated successful evidence.
4. Add progressive autonomy stages: shadow -> operator-approved -> one-user auto -> bounded batch auto -> production auto.
5. Retire or archive obsolete duplicate reports once stable conclusions are in reference/ADR.

### Long Term: 6-12 Months

1. Mature event-driven controller behavior without becoming a blind timer.
2. Let observed capacity influence recommendations only after shadow evidence is certified.
3. Build a recurring eval discipline for planner/prediction/trust decisions.
4. Formalize an autonomy release train with rollback, blast radius, and operator override metrics.
5. Move from operator-first recovery to operator-supervised autonomy, then limited operator-free autonomy.

## 11. What To Delete Or Ignore

Do not delete immediately. Classify first.

| Candidate | Recommendation |
| --- | --- |
| Draft autoswitch planner timer | Keep as draft evidence; do not enable as movement owner |
| `v7-users-autoswitch.timer` apply cadence | Keep disabled until event-driven certification passes |
| Legacy raw UI check actions | Continue demotion to details/status |
| Repeated broad audits of route/capacity/score | Stop; answer from reference first |
| Synthetic evidence scripts | Do not create |
| New planner/governance/execution proposals | Ignore unless existing owner cannot be extended |

## 12. Top 10 Next Actions

1. Collect observed service/channel outcome evidence through existing service, quality, prediction, feedback, and closure owners.
2. Collect time-separated prediction forecast -> later actual evidence.
3. Run `AUTONOMY.CANARY.1C_RESTORE_BARRIER_CLEARANCE_RECHECK` through existing packet/restore owners only.
4. Recheck restore barrier creation for a single event-triggered packet in preview mode after normal observe no longer stops at snapshot mismatch.
5. Recheck rollback packet readiness for the same single event-triggered packet.
6. Build an autonomy readiness dashboard row from existing gate values only.
7. Keep `v7-users-autoswitch.service/timer` inactive until confidence/trust/prediction floors pass.
8. Use operator comparisons only when the operator has enough context; do not create blind training history.
9. Preserve Branch 1B evidence and never replace it with synthetic records.
10. Keep refresh durability protected by tests whenever evidence-store lifecycle changes.

## 13. Final Blueprint Verdict

`AUTONOMY_BLUEPRINT_CREATED_EVENT_DRIVEN_AUTONOMY_PARTIAL`

V7 has the right architecture shape and most owners already exist. Branch 1B closed the blast recovery loop as a proven production recovery, AUTONOMY.TRUST.DURABILITY.1 fixed the normal durability gap, and AUTONOMY.TRUST.SOURCE.REALITY.1 corrected trust semantics: observed network outcomes are primary, while operator comparison is secondary supervised confirmation. The safe path is not to build another autonomy system or force blind operator reviews. The safe path is to collect real observed outcome and prediction evidence, certify event consumption read-only, and only then authorize a bounded canary apply.
