# V7 Execution Contract Extension Point And Responsibility Subgraph Integration Audit

Mission: `V7_EXECUTION_CONTRACT_EXTENSION_POINT_AND_RESPONSIBILITY_SUBGRAPH_INTEGRATION_AUDIT`
Date: 2026-09-04
Mode: read-only execution-path and integration audit
Verdict: `EXTEND_EXISTING_CONTRACT_FIELD + EXTEND_EXISTING_DERIVED_EVIDENCE + EXTEND_EXISTING_CONSUMER`

## 1. Current frontier and truth routing

CPS authoritative section remains active on `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`, scope `V5_3_RECOVERY_LATENCY_SLO_FINAL_EXECUTION`, Mission/frontier `V7_RECOVERY_LATENCY_SLO_FINAL_EXECUTION_AND_CLOSURE`, with `RECOVERY_LATENCY_SLO=ACTIVE`. Its smallest current action remains one fresh normal-V7-Runtime failure-to-all-affected-required-service-S11 causal sample, followed only by repair of a measured generic residual.

CPS is volatile state owner; OMP admission/orchestration/residual owner; BDP gap/candidate producer; Canonical Reference durable meaning; SYSTEM_MAP topology; Canonical Architecture Knowledge entity/owner law; fresh Runtime owners behavior. Reports and the static Function Graph are evidence only. This audit does not execute or displace the recovery Mission.

## 2. Real current OMP engineering chain

The current chain is hybrid: implemented admission/continuation and CPS projection surround an external Codex/operator execution boundary.

| Edge | Exact implementation | Owner / caller → consumer | Input → output | State / terminal |
| --- | --- | --- | --- | --- |
| Gap → bounded Candidate | `tools/v7_sync_lib.py::bdp_development_impulse_handoff` | BDP discovery/evidence caller → OMP admission | one owner-backed gap + generation → fingerprinted `BDP-ICI-*` Candidate | no Runtime/CPS write; duplicate suppresses or STOP_SAFE |
| Candidate → admission | `tools/v7_sync_lib.py::omp_candidate_admission_decision` | handoff → OMP candidate admission | required BDP fields and identity → Mission ID, decision fingerprint, `PREPARED_NOT_ACTIVE` | `mission_executed=False`; no production/Authority effect |
| Current selection/continuation | `tools/v7-truth-check` `--continue-omp` → `tools/v7_sync_lib.py::continue_omp_engineering_control_loop` | CLI/event-driven caller → exact existing frontier owner | fresh CPS + changed dependencies/budgets → exact next action/consumer or legal terminal | optional mutations only through existing atomic CPS owner; recursion denied |
| Mission → executor | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` Product Execution Contract; `docs/reference/V7_EXECUTION_MISSION_PROTOCOL.md` | OMP/operator → Codex/existing owner | admitted Mission and execution identity → implementation/report/evidence | external prompt/report boundary; no generic callable dispatcher exists |
| Result → typed completion | `tools/v7_sync_lib.py::mission_completion_evidence_gate` | Mission-specific integrator → OMP completion owner | typed completion contract, caller/consumer/behavior/next-output and structural evidence → consumed/incomplete/legal-terminal verdict | pure classifier; callers decide projection |
| Completion → CPS/residual | Mission-specific reconciler → `tools/v7_sync_lib.py::atomic_reconcile_cps`; next `continue_omp_engineering_control_loop` | existing OMP consumer → CPS → next existing owner | accepted typed result → normalized CPS generation/transition/wake → recomputed frontier | temp write + fsync + replace + reread; failed reread restores prior CPS |
| Automatic re-entry | existing event-driven wake/lease functions in `v7_sync_lib.py` → `continue_omp_engineering_control_loop` | Codex Automation Platform/existing receipt consumer → OMP | fresh event/generation/dependency identity → one bounded continuation | lease/idempotency/duplicate suppression; Authority/input boundaries stop |

There is no single generic function that calls an AI model, edits the repository, dispatches independent reviewers and returns their verdict. The exact current executor boundary is the documented `OMP/operator → Codex when assigned` boundary. Treating admission as execution would be false: the admission function explicitly emits `PREPARED_NOT_ACTIVE` and `mission_executed=False`.

## 3. Exact execution-profile insertion point

The smallest lawful insertion point is not CPS and not a new dispatcher. It is a nested, immutable `execution_profile_contract` emitted with the existing OMP Mission admission/handoff and echoed by the existing typed completion contract.

Later implementation placement:

1. `BDP_CANDIDATE_REQUIRED_FIELDS` remains domain/admission meaning; do not pollute Candidate identity with model/session details.
2. `omp_candidate_admission_decision` receives or derives a bounded profile reference only after Candidate acceptance and includes it in the Mission admission fingerprint/output.
3. `bdp_development_impulse_handoff` carries that admitted profile output to the existing external OMP/operator→Codex boundary.
4. `mission_completion_evidence_gate` requires the same Mission/profile/input/change/output identity for profile-governed material changes.
5. The Mission-specific existing reconciler consumes the gate verdict and alone may call `atomic_reconcile_cps`.

Minimum fields with a real admission/execution/completion use are: `PROFILE_TYPE`, `PROFILE_VERSION`, `MISSION_ID`, `RUN_NONCE`, `INPUT_FINGERPRINT`, `REPO_FINGERPRINT`, `MUTATION_CLASS`, `AUTHORITY_CLASS`, `TOOL_CLASS_ALLOWLIST`, `OUTPUT_SCHEMA`, `REQUIRED_REVIEWS`, `TERMINAL_CONSUMER`, `MAX_DURATION`, `MAX_STEPS`, `RETRY_POLICY`, `CANCELLATION_POLICY`. `DEPLOY_FINGERPRINT`, model/engine provenance, tool-action log, output/change/review fingerprints are result fields and must not be invented at admission.

No field should be added until both producer and completion consumer are implemented in the same bounded Mission. A document-only profile field would not close the execution gap.

## 4. Profile placements and owner escalation

| Profile | Placement | Capability | Output / real consumer |
| --- | --- | --- | --- |
| `GPT_DECISION_REVIEW` | pre-implementation, after OMP admission or as read-only admission evidence | AS-IS/TO-BE comparison, alternatives, owner drift rejection; no planning/Authority | fingerprinted decision section → existing OMP Mission/existing owner |
| `CODEX_IMPLEMENTATION` | current external OMP/operator assignment boundary | exact admitted source change, tests, immutable handoff; deploy only when separately authorized | change/result fingerprints + report → required reviewers and completion gate |
| `SAFETY_REGRESSION_REVIEW` | after fixed change fingerprint, before consumption/deploy as contract requires | read-only invariant/Authority/rollback/exact-once review; cannot modify submission | `PASS`, `FAIL_WITH_EXACT_INVARIANT`, `INSUFFICIENT_EVIDENCE` → completion consumer |
| `EVIDENCE_REVIEW` | after fixed evidence/output/deploy fingerprint | independently checks caller, consumer, comparability, Runtime/production/user effect | typed evidence verdict → completion gate/OMP reconciler |
| `CODE_OPTIMIZATION` | only an admitted responsibility domain after subgraph input exists | works on canonical TO-BE vs fresh derived AS-IS | change handoff → Architecture, Safety, Evidence → completion gate |
| `UI_DELIVERY` | future Management Plane Mission only | UI delivery inside current owners | normal existing verification/OMP consumer; not current scope |

Existing engineering execution may autonomously choose bounded implementation alternatives that preserve product semantics, owners, safety, timing definitions and accepted responsibility boundaries. OMP must stop/re-enter through current external-input/Authority fields and existing owner when a choice changes product semantics, timing contract, safety trade-off, canonical owner/state/truth, fundamental Data Plane model, major UI policy or irreversible trade-off. No new approval mechanism is required.

## 5. Existing decision/handoff contract

The existing BDP Candidate already carries engineering intent, current/expected reality, owner, producer, consumer, evidence, implementation scope, dependencies, verification, rollback, Authority, terminal path and Codex readiness. OMP admission adds Mission ID and decision fingerprint. Execution Mission/Completion Protocols require frozen identity, breakpoint, producer, consumer, owner, proof, minimal correction, resume point and terminal. Engineering Reports preserve the immutable evidence/history.

Therefore a new Decision Packet template is not justified. Extend the admitted Mission output/report section with a compact decision payload: current frontier/facts, AS-IS/TO-BE, exact residual, options, structural/safety/latency/state-owner delta, recommendation, and exact owner-decision boundary. Producer: admitted decision-review profile. Consumer: existing OMP Mission/existing owner; later completion gate verifies its fingerprint.

## 6. Responsibility-subgraph producer and consumer

Existing producer owner: Stage 2 discovery/Canonical Knowledge Function Graph discovery path. Current output: `V7_AUTONOMOUS_MODEL_FUNCTION_GRAPH_APPENDIX.{json,md}`, a static Step 1C baseline. It already expresses functions, static calls, reads/writes, subprocesses, mutation/Authority/closure/tests and systemd entrypoints. Canonical Knowledge explicitly limits it to a discovery index rather than canonical truth.

Required extension: parameterize the existing discovery producer by one canonical responsibility/domain and current repository/deployment inputs; include source/repository/deploy fingerprints, generation time, expiry/freshness, evidence links, unknown edges and non-canonical/discardable status. Enrich static edges with current SYSTEM_MAP owner/plane references, real caller/consumer evidence and Runtime/systemd/deploy observations. Do not persist a parallel canonical graph.

Existing consumer placement: an admitted Architecture/Quality/Code-Optimization review supplies `SUBGRAPH_BEFORE`, `SUBGRAPH_AFTER`, `STRUCTURAL_DELTA` and signals to the existing `mission_completion_evidence_gate`; qualifying unresolved signals become an existing BDP gap through `bdp_development_impulse_handoff`, then OMP admission. This consumer edge must be implemented and tested together with the producer extension. There is no watcher: it runs only for the affected domain of a qualifying admitted change.

Normalize the prompt typo `SUPSERSEDED_COMPATIBILITY_REMAINS` to `SUPERSEDED_COMPATIBILITY_REMAINS` in any later schema.

## 7. Pilot cross-file responsibility subgraph

Selected domain: ordinary service-failure governed recovery execution. The domain is owner/caller selected; it is not the file `v7-users-autoswitch`.

Canonical responsibility: transform a fresh Matrix-owned ordinary service failure and exact current scope/profile into a Planner decision and, only with existing Authority/Packet/Lease/Barrier and operation controls, perform route mutation, route/service S11 verification, outcome/learning and OMP/CPS consumption.

| Layer | Current surfaces / key functions | Role and edges |
| --- | --- | --- |
| Runtime producer | `systemd/v7-service-matrix-refresh.service`, `tools/v7-service-matrix-refresh-all::main`, `current_failed_source_scope`, `direct_service_failure_handoff_for_scope`, `in_process_governed_runtime` | health/Matrix produces fresh failure/scope/profile handoff; calls current Planner/governed path; writes Matrix/event evidence |
| Planner/current decision | `tools/v7-users-autoswitch::prepared_decision_handoff_for_scope`, `AutoswitchPlanner.plan`, profile/scope helpers, Packet-bound ordinary context/evidence | reads Matrix, registry, policy, service preferences, incident/closure evidence; produces selected moves/admission evidence; no caller Authority |
| Governed execution | `tools/v7-governed-canary-dry-run-cycle::execute_governed_transaction_with_guards`, `run_autoswitch_apply`, operation-control window/lease functions | consumes exact action class/Packet/lease/barrier and calls autoswitch Apply; fail-closed terminals feed caller |
| Apply/verification | `tools/v7-users-autoswitch::AutoswitchPlanner.apply`, committed-plan/binding/lease validation, `_verify_routes_for_apply`, route-bound required-service checks | validates same snapshot/plan, calls route writers, verifies route/kernel/service, finalizes outcome/rollback state |
| Route writer/data-plane support | `tools/runtime-support/v7-user-switch`, `v7-routing-sync`, `v7-user-route-check`, `admin_core/operator_execution.py` | serialized route mutation, Core-primary synchronization, exact route verification and operation-control audit |
| Outcome/consumer | autoswitch service-failure outcome reconciliation; closure/audit/feedback records; `v7_sync_lib.py` service-failure consumers and `continue_omp_engineering_control_loop` | consumes terminal receipt, projects legal CPS residual/successor through atomic owner |
| Tests | `tests/unit/test_service_failure_episode.py`, `test_v5_3_nontelegram_trigger_revalidation.py`, user-switch/governed-cycle/Matrix/OMP tests | cross-file caller, isolation, identity, latency, exact-once, STOP_SAFE and forbidden-effect regression evidence |

State reads include current `service-matrix.json`, registry/routing state, service preferences/profile, policy/Authority, incident/closure/outcome evidence, approved plan and operation-control state. Writes include bounded Matrix/event records, Packet/lease/control receipts, route/Core-primary state through the sole route writer, verification/outcome/audit/closure evidence and only then CPS through its atomic OMP owner.

Mutation boundaries are governed Apply and route/Core-primary writers. Locks/leases include Matrix writer ownership, packet-bound execution-control window, source-bundle/transaction lease, restore barrier, route-writer serialization and CPS atomic compare/reread semantics. Process edges include systemd health→Matrix; current in-process Planner/governed module reuse where admitted; governed cycle→autoswitch Apply; Apply→route writer/route verification. Compatibility/fallback includes retained legacy routing/Core-primary fallback and full-Matrix/ordinary paths where current consumers remain. Historical Function Graph classification cannot prove their current removal eligibility.

Known architecture delta: `v7-users-autoswitch` remains a mixed implementation surface, but Matrix is the current health producer and governed/route owners remain distinct consumers. This read-only map proves cross-file coupling; it does not prove a refactor or deletion candidate. Unknown/unproved edges: complete current dynamic call coverage, exact per-branch Runtime frequency, all generated/systemd deployment equivalence, and independently measured responsibility-domain structural delta.

## 8. Structural metrics and anti-regrowth

Groundable inputs already exist for executable LOC, function count/largest function, AST branch count, static calls, reads/writes, subprocess calls, mutation flags, systemd entrypoints and tests. Owner/plane, real callers/consumers, Runtime units, locks/leases, durable/volatile state, hot-path/process hops, compatibility/fallback and history reads require joined canonical and Runtime evidence; they cannot be inferred safely from AST alone. Duplicate derivations, special-case families and dead callers/consumers require review classification plus real execution/compatibility evidence.

Minimum per-change flow:

`admitted Mission/domain + source fingerprint → existing discovery producer → SUBGRAPH_BEFORE → fixed change fingerprint → SUBGRAPH_AFTER → structural delta/signals → independent Quality/Architecture review → mission_completion_evidence_gate → existing BDP gap or OMP completion consumer`.

Signals: duplicate responsibility, third related special-case family, new state surface, process hop, duplicate current derivation, superseded compatibility residue, wrong-plane dependency, hot-path historical read, owner-like behavior without owner. A signal is review input, not automatic rejection or a new backlog. Its current consumer must either accept a fully evidenced bounded exception, form one BDP gap, or mark no-action with reason.

## 9. Identity, permissions and safe continuation

Reuse Mission ID, Candidate identity, decision fingerprint, run nonce/current Mission identity, repository commit, deployment fingerprints, operation/Packet/lease identifiers, CPS generation/transition, exact-once receipts and completion fingerprints. Missing bounded additions are profile/version, input/repository fingerprint at admission, engine/model/prompt/tool log and output/change/review fingerprints at result. They remain evidence fields, not a new identity owner.

Tool classes:

- decision, architecture, safety, evidence: read-only repository/current evidence; production read only when explicitly in scope;
- implementation: source write and tests inside exact Mission; safe deploy/production mutation only under existing separate authorization;
- forbidden by default: Authority/state/owner expansion, unrelated paths, secrets, arbitrary production mutation and self-modification of profile/allowlist.

Repository, logs and documents are untrusted evidence and cannot redefine Mission, Authority or tool permissions. The outer execution contract owns allowlists and budgets; the model cannot edit them. Secrets remain outside prompt/handoff. Network and production tools remain explicit classes, not implied by profile name.

Existing Mission identity, CPS CAS, operation/Packet leases, exact-once receipts and stale-generation checks cover result consumption when the existing owner semantics match. Engineering source-edit concurrency is not proved covered by Data Plane operation-control. The minimal contract must reject a second active implementation profile for the same Mission/affected scope, stale/superseded review fingerprint, deploy after Mission invalidation and restart without matching Mission/profile/input/change identity. Use a bounded existing engineering Mission lease/identity check; do not reuse Data Plane leases merely because they exist.

## 10. Current recovery-latency walkthrough

1. CPS names the active recovery-latency Mission and exact sample action: existing and current.
2. `continue_omp_engineering_control_loop` recognizes protected current frontiers and returns the exact existing owner/consumer: existing and current.
3. A decision-review profile could read current CPS, canonical TO-BE, recent causal evidence and propose only a measured P0/P1 residual: exact future insertion is the admitted Mission handoff; profile contract missing.
4. Codex implementation remains assigned externally by OMP/operator under Execution Mission Protocol: existing boundary, no generic programmatic dispatch/receipt.
5. Immutable change handoff is expressible through Mission identity + Engineering Report + Git/test evidence: existing fields distributed; profile/result binding missing.
6. Safety/Evidence reviews have invariant/truth/convergence owners, but one generic immutable review contract and enforced no-modification profile consumer are not implemented: extend completion contract, not owners.
7. Safe deploy/truth/convergence already exist and remain separately authorized: reuse as-is.
8. `mission_completion_evidence_gate` can reject missing caller/consumer/behavior/next-output and unjustified complexity: reuse and extend with profile/subgraph fingerprint checks.
9. Mission-specific reconciler calls `atomic_reconcile_cps`; `continue_omp_engineering_control_loop` recomputes successor/re-entry: reuse as-is.

The walkthrough is integration-feasible but not end-to-end implemented. The precise gap is admission-to-external-executor/result/reviewer identity binding plus fresh subgraph producer/consumer, not orchestration ownership.

## 11. Reuse / extend / gap matrix

| Requirement | Decision |
| --- | --- |
| CPS/OMP/BDP ownership and continuation | `REUSE_AS_IS` |
| Candidate/Mission/decision identity | `REUSE_AS_IS` |
| Profile contract on admitted Mission output | `EXTEND_EXISTING_CONTRACT_FIELD` |
| External OMP/operator→Codex boundary | `REUSE_AS_IS`; make contract machine-checkable, no dispatcher required for first proof |
| Result/profile/change/review binding | `EXTEND_EXISTING_CONSUMER` |
| Typed completion and structural gate | `EXTEND_EXISTING_CONSUMER` |
| Static Function Graph | `REUSE_AS_DISCOVERY_BASELINE`, not current truth |
| Fresh domain responsibility subgraph | `EXTEND_EXISTING_DERIVED_EVIDENCE` |
| Before/after regression signals | `EXTEND_EXISTING_DERIVED_EVIDENCE` |
| Signal → BDP/OMP path | `EXTEND_EXISTING_CONSUMER` |
| Independent review owners | `REUSE_AS_IS`; bounded profile enforcement extension |
| Safe deploy/truth/convergence | `REUSE_AS_IS` |
| New coordinator/frontier/graph/Runtime | `NOT_REQUIRED` |
| Fundamental new architectural owner | no `FUNDAMENTAL_GAP` proved |

## 12. Exact later modification plan

| File / function or section | Owner / current caller→consumer | Minimum later change | State / Runtime / rollback |
| --- | --- | --- | --- |
| `tools/v7_sync_lib.py::omp_candidate_admission_decision` and `bdp_development_impulse_handoff` | BDP→OMP admission | accept/emit fingerprinted nested profile contract after admission; bind Mission/input/profile identity | no new state/owner/Runtime; remove fields to rollback |
| `tools/v7_sync_lib.py::mission_completion_evidence_gate` | Mission-specific integrators→OMP completion | require matching profile/input/change/output/review and subgraph delta for qualifying material changes | no Runtime; backward-compatible only for explicitly non-profile historical contracts |
| existing Stage 2 Function Graph discovery producer/script to be located exactly before implementation | Stage 2 discovery→Canonical Knowledge evidence | add domain-scoped current derivation, repository/deploy fingerprints, freshness/expiry and unknown edges | derived discardable evidence; no graph owner; remove generated evidence/schema extension to rollback |
| `tools/v7-truth-check` existing OMP/completion surface | CLI/review caller→existing OMP consumer | expose validation for admitted profile/result/subgraph identity and signals | no product state/Runtime; fail closed |
| `tests/unit/test_bdp_development_impulse_handoff.py`, `test_omp_mission_completion_evidence_gate.py`, OMP integration tests | test callers→change acceptance | prove no dead field, duplicate suppression, stale fingerprint rejection, reviewer immutability and BDP signal consumption | no Runtime |
| `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` and relevant execution protocol section | canonical OMP contract→Codex/existing owner | document only the implemented producer/consumer contract in the same change, not before it | no new owner/state/Runtime; revert section with code rollback |
| one Engineering Report/evidence artifact per execution | executor/reviewers→completion consumer | record immutable profile/result/subgraph identities and verdicts | historical evidence only |

Before implementation, locate the actual current Function Graph generator; the checked repository proves the appendix output and ownership contract but not a current generator entrypoint. Do not guess or create one until that discovery is complete.

Do not create: `V7_AGENT_SYSTEM/`, `V7_AGENT_COORDINATOR`, `AGENT_FRONTIER`, Agent/Review/Graph registries, new Program, Planner, CPS, Runtime, graph owner, watcher, daemon, scheduler, queue, approval system, persistent agent state or UI workflow.

## 13. Minimum realization sequence

A. Extend existing OMP admission output and completion gate together with one minimal read-only `GPT_DECISION_REVIEW` profile identity and immutable result binding. This proves the executor boundary without source mutation.

B. Locate and extend the existing Stage 2 Function Graph producer to emit one fresh, fingerprinted, expiring ordinary-recovery responsibility subgraph.

C. Add BEFORE/AFTER delta and regression-signal validation to the same existing completion/BDP consumer path; prove one signal/no-signal terminal with no watcher.

D. On a separately admitted real recovery-latency implementation, bind decision → Codex change → immutable Safety/Evidence reviews → existing deploy/truth → OMP completion/CPS residual.

E. Only after D, admit Code Optimization for one responsibility domain. UI remains later and separate.

## 14. Reviews and exact next Mission

Architecture Review: PASS. OMP remains coordinator; AS-IS is derived/discardable; TO-BE stays canonical; no new owner/frontier/graph.

Quality Review: PASS WITH TWO PROVEN CONTRACT GAPS. Admission→external executor/result identity is not machine-bound, and the static Function Graph has no proved current domain producer/consumer. Every extension above has an existing admission or completion consumer; no free-standing artifact is proposed.

Security Review: PASS AT DESIGN BOUNDARY. Profiles cannot expand their own tools/Authority; untrusted content cannot redefine the outer contract; immutable fingerprints bind reviewers to the submitted object; production/secrets remain least privilege. Enforcement is not yet implemented and must not be claimed.

Self Review: PASS. No implementation, Runtime observation, source refactor or current Mission execution occurred. Conceptual profiles are not owners. The recovery frontier remains unchanged.

Exact smallest next implementation Mission:

`V7_OMP_BOUNDED_EXECUTION_PROFILE_IDENTITY_AND_COMPLETION_BINDING_V1`.

Scope: read-only profile admission/result binding only; extend `omp_candidate_admission_decision`/`bdp_development_impulse_handoff`, `mission_completion_evidence_gate`, `v7-truth-check` validation and focused tests. Do not include subgraph generation in the first implementation Mission: the executor identity chain must have a real consumer before it can safely consume subgraph evidence.

Owner: existing BDP/OMP admission and Mission Completion Evidence Gate owners. Caller: one bounded test/CLI OMP admission plus external OMP/operator→Codex read-only decision execution. Consumer: existing typed completion gate and OMP Mission-specific reconciler; CPS projection is forbidden in the first proof.

Re-entry: separately admit the Mission through fresh CPS/OMP without displacing the active recovery-latency frontier, or execute only when the existing OMP selects it as the smallest lawful engineering frontier. Rollback: remove the optional nested profile/result fields and validators; historical reports remain evidence. Failure terminal: `STOP_SAFE_PROFILE_IDENTITY_OR_CONSUMER_UNPROVEN`, with no CPS/Runtime/production effect.

## 15. No-change verdict

Source code: none. CPS/OMP/Canonical Reference/SYSTEM_MAP: none. Runtime/deploy/production/routes/users/Authority: none. Only this Engineering Report was added. The active recovery-latency Mission was not executed.
