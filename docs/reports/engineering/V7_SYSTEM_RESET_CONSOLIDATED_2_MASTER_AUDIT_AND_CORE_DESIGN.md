# V7 System Reset — Volume 2: Master Audit and Core Design

> Consolidated source set. This volume preserves the included reports verbatim;
> the volume heading and separators are navigational only. It is the compact
> sendable representation of the original report set, not a new authority.

## Reading map

1. Master Audit and RESET-M1B through RESET-M5 evidence.
2. RESET-M10 contract and final architecture.
3. RT2 operating/deep-simplification contracts.
4. Responsibility realignment plan, Program contract and execution hardening.

The appended source blocks in this volume are: `340000`, `350000`, `370000`,
`380000`, `430000`, `440000` and `450000`.

---

# V7 System Reset Master Audit Report

Status: `RESET_MASTER_AUDIT_REPORT_FINAL_SELF_REVIEW_PASS`

Program: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1`

Scope generation: source commit `7ffa4c06bab741f266070e6506987e320e828922`, branch `Updatesystem`, production identity and current CPS captured 2026-08-13. This report is historical evidence and a decision instrument; CPS remains volatile truth.

## Executive verdict

The primary V7 routing Product Contract is `PARTIALLY_REALIZED`. Observation, selection, governed apply, kernel visibility, payload verification, rollback, feedback and evidence mechanisms exist and have real callers. They are not assembled into a bounded routine recovery path. Current production begins from a 15-minute Matrix cycle, executes broad probes and repeated planning/reconciliation, crosses at least nine pre-apply producer-consumer hops and 17 state surfaces, writes at least six durable objects before apply, and uses an O(N) assignment writer. The measured successful forward lifecycle is 58.761588 s while kernel mutation plus visibility is approximately 0.878 s.

The first proven systemic root cause is `LOCAL_CONTRACT_COMPLETION_WITHOUT_PARENT_PRODUCT_EFFECT`. Programs and capabilities generated valid local outputs, reports, tests, deployments and certification states, but the real consumer/product-effect chain was not the controlling completion unit. The CPS unfinished registry itself records for U02-U22 that consumption, behavior change, next output, Runtime consumption or production consumption remains `NO_OR_PARTIAL` after their engineering criteria were consumed.

The second proven root cause is `ENGINEERING_PLANE_PLACED_IN_SYNCHRONOUS_ROUTING_LIFECYCLE`: Matrix expansion, passive reconciliation, advisory/Planner construction, OMP consumption, evidence/closure and broad verification surround the sub-second apply/visibility effect.

The third proven root cause is `DOCUMENTED_ACTIVE_PROGRAM_NOT_CONSUMED_BY_ALL_REAL_OWNERS`. CPS declares Reset as active, while `tools/v7_sync_lib.py`, `tools/v7-users-autoswitch`, `admin_core/operator_execution.py` and governed execution surfaces retain hard-coded Service Failure/Polygon active-program identities and normalized CPS defaults. This creates current `ACTIVE_PROGRAM`, continuation and mission-pointer divergences. Reset registration is therefore `IMPLEMENTED_NOT_CONSUMED` by those legacy consumers.

These are M0 conclusions, not permission to patch Runtime or accept M1 dispositions.

## Scope and evidence classes

- `OBSERVED_PRODUCTION`: consumed 2026-08-13 routing reality audit and read-only Runtime truth.
- `STATIC_PROVEN`: current source, callers, imports, constants, entrypoints and file/function inventory.
- `CONFIGURED`: systemd/tool installation contracts and canonical ownership maps.
- `HISTORICAL`: prior reports and Program labels, never used as live state without current consumer evidence.
- `UNKNOWN_REQUIRES_OWNER_EVIDENCE`: dynamic/external consumers not yet demonstrated in current scope.

Current Program surface: 16 files / 46,171 lines under `docs/programs`. Largest documents are OMP 11,112; Service Failure Automation 4,793; BDP 2,923; CPS 2,870; AEP 2,265; Stage 2 2,242. Document size is context, not disposition.

## Program Intent Reality matrix

| Object | Intended contribution | Real producer/caller/consumer evidence | Product/terminal effect | Intent Reality verdict | Exact residual |
| --- | --- | --- | --- | --- | --- |
| Reset Program V1 | Audit failure causes, specify/migrate minimal Core, shrink legacy | CPS/OMP register M0; no Runtime owner consumes Reset identity consistently | M0 started; no Runtime effect intended yet | `PARTIALLY_REALIZED` | finish M0-M1B evidence before Core contract/implementation |
| OMP | development orchestration, intent/consumer/completion discipline | real source consumers in `v7_sync_lib.py`, `v7-truth-check`, CPS reconciliation | local engineering continuation proven; product hot path also calls OMP/reconciliation | `WRONG_ARCHITECTURAL_PLACEMENT` | M1B separate keepable development laws from synchronous routing functions |
| CPS | sole volatile Program/capability state | read/written by `v7_sync_lib.py` and truth/continuation entrypoints | active Reset fields exist, but section 0 contains contradictory legacy generations/frontiers | `PARTIALLY_REALIZED` | M0 classify contradictions; M2 collapse to compact current Program state |
| Implementation Program | govern implementation lifecycle | referenced by OMP/canonical docs; no direct Runtime caller required | lifecycle rules influence engineering; current active queue role displaced by Reset | `PARTIALLY_REALIZED` | M1 component-level disposition |
| Implementation Backlog | single implementation queue | referenced by OMP/canonical owners; marked 34/34 complete | historical implementation selection, not current routing effect | `PARTIALLY_REALIZED` | classify historical/acceptance value versus active queue necessity |
| Autonomous Evolution Program | strategic knowledge-to-gap-to-OMP evolution | `v7_sync_lib.py` canonical source mapping; reports/OMP consumers | engineering inputs and accepted candidates; no direct routing effect expected | `PARTIALLY_REALIZED` | M1 retain useful intent/contracts without parallel roadmap |
| Behaviour Discovery Program | discover/certify behavior gaps and candidates | OMP and `v7_sync_lib.py` consumers; extensive engineering results | gap/candidate production exists; failed to constrain aggregate product complexity | `CONSUMED_NO_PRODUCT_EFFECT` for primary contract | M1B scope down to asynchronous development input |
| Stage 2 Knowledge Program | extract, accept and lock canonical engineering knowledge | canonical reference/CPS/OMP consume locked state | lawful separate knowledge terminal exists | `INTENT_REALIZED` | M1 preserve knowledge/evidence; close active Program machinery |
| Research Framework | bounded research owner/process | canonical/manual consumers; no required Runtime caller | lawful engineering support only | `INTENT_REALIZED` as separate support contract | M1 determine permanent lightweight reference scope |
| Routing Digital Twin Polygon Master | effect-free scenario/decision validation | substantial `v7_sync_lib.py` implementation and OMP entrypoints | engineering validation/caller evidence; no production routing effect by design | `INTENT_REALIZED` for engineering terminal, `WRONG_ARCHITECTURAL_PLACEMENT` if synchronous | M1 retain as acceptance corpus/asynchronous tool only |
| Permanent Polygon OMP Integration | integrate Polygon results into OMP | `v7_sync_lib.py` permanent Polygon consumers and CPS projections | engineering continuation exists | `PARTIALLY_REALIZED` | M1 merge overlapping Polygon Program machinery |
| Permanent Polygon Design-Time Completion | design-time product validation loop | `v7_sync_lib.py` design-time missions/consumers | separate engineering effect; product behavior indirect | `PARTIALLY_REALIZED` | M1 acceptance-only/merge candidate; prove current live consumer |
| Permanent Polygon Target-Level Plan | target-level Polygon completion | no non-report external filename references found | current live consumer unproven | `IMPLEMENTED_NOT_CONSUMED` | exact owner evidence or merge/close disposition |
| L7/L8 Evidence and Authority Evolution | preserve controlled/natural evidence lanes and Authority recommendation | `v7_sync_lib.py` consumers; CPS capability rows | controlled evidence consumed; natural evidence legally absent; no implicit Authority | `PARTIALLY_REALIZED` with lawful lane terminal | M1 preserve acceptance/Authority semantics asynchronously |
| Service Failure Automation Evolution | detect incidents and drive governed continuation | hard-coded in autoswitch, operator execution, Matrix, sync library and governed cycle | real product/engineering effects exist; recovery remains slow/coupled and its identity now conflicts with active Reset | `PARTIALLY_REALIZED` | classify reusable failure/health semantics versus legacy execution machinery |
| Service Failure Lifecycle/Multi-Lane | durable incident/product frontier | program ID and consumers implemented in `v7_sync_lib.py`; filename has no external reference | incident/closure projections exist; independent current Program necessity unclear | `PARTIALLY_REALIZED` | M1 merge with Service Failure semantics or legacy-only evidence |

## Capability Intent Reality

| Group | Current CPS evidence | Product Contract verdict | Residual |
| --- | --- | --- | --- |
| CAP-C01-C12 | labels `LOCKED`/`COMPLETE`, with local owners and reopen triggers | local framework/knowledge/safety terminals exist; labels do not establish fast routing recovery | M1B test whether each rule prevented the observed failure; keep real safety, redesign documentary protections |
| CAP-U01 | one governed controlled run and route repair consumed | `INTENT_REALIZED` for bounded historical run, not scalable routine recovery | retain acceptance corpus, do not infer Core architecture |
| CAP-U02-U06 | movement/eligibility/Authority/rollback/recovery matrices consumed; whole capabilities partial/waiting | `PARTIALLY_REALIZED`; production consumer/effect incomplete | map exact pre-apply safety semantics versus async evidence work |
| CAP-U07-U09 | Learning/readiness/autonomy matrices consumed; real representative outcomes/Authority incomplete | `CONSUMED_NO_PRODUCT_EFFECT` for routine recovery | move engineering consumption after compact Runtime receipt |
| CAP-U10-U13 | observability/explainability/Runtime maturation/time matrices consumed | `PARTIALLY_REALIZED`; observability exists but adds surfaces and does not close recovery | keep necessary operational visibility; remove from synchronous apply path |
| CAP-U14-U22 | engineering-intelligence criteria consumed; next outputs and real outcomes incomplete | `CONSUMED_NO_PRODUCT_EFFECT` for primary contract | asynchronous development-plane disposition; no Core admission by default |

## Product relationship reality

Verified current chain:

`Matrix timer -> 7 checker children/98 probes -> Matrix/events -> passive consumer -> Service Failure/OMP reconciliation -> governed Planner -> Candidate/Packet/lease/barrier -> repeated Planner/live reads -> per-user switch/global registry rewrite -> kernel visibility/payload verify -> Outcome/Replay/Learning/closure/CPS`.

The broken parent link is not absence of routing code. It is the inability to transform a fresh failure generation into bounded apply/verify without synchronously traversing broad engineering, historical and certification machinery. Local consumers change local state, but the aggregate behavior violates the latency and complexity intent.

## Complexity baseline

| Surface | LOC | Functions/classes | Initial semantic signal |
| --- | ---: | ---: | --- |
| `tools/v7_sync_lib.py` | 25,279 | 306 / 0 | mixed CPS, OMP, Polygon, service-failure, deploy/truth owners; split/merge disposition pending M0B |
| `tools/v7-users-autoswitch` | 23,167 | 309 / 4 | Planner, consumers, validation, apply, verification and closure responsibilities |
| `admin_core/autonomy_trust_acceleration.py` | 13,892 | 200 / 0 | broad engineering/read-model/certification responsibility |
| `tools/v7-governed-canary-dry-run-cycle` | 12,694 | 103 / 0 | governed orchestration and evidence expansion |
| `admin_core/operator_execution.py` | 8,853 | 161 / 1 | Authority/Packet/lease/barrier/execution contracts |
| `tools/v7-control-plane-governance-check` | 7,331 | 74 / 0 | broad historical governance verification |
| `admin_core/operator_execution_pipeline.py` | 5,020 | 95 / 0 | execution pipeline/read-only maturity extensions |
| `tools/v7-service-matrix-refresh-all` | 4,350 | 46 / 0 | observation, event production and consumer invocation |

No large-file disposition is accepted from size alone. M0B must prove callers, responsibilities, state/effects, dynamic edges and change reasons.

## Production entrypoint and module coverage ledger

The immutable source scope contains 48 executable top-level tools, 29 `admin_core` Python modules, 12 concrete systemd unit files plus three draft units, and 69 explicit subprocess/command-discovery launch sites across the principal Matrix/governed/autoswitch/sync/execution owners. This is a lower bound because shell dispatch and remote install scripts add edges outside Python AST calls.

### Executable tools

| Initial class | Stable identities | Evidence / residual |
| --- | --- | --- |
| `CURRENT_PRODUCT_REQUIRED` | `v7-users-autoswitch`, `v7-service-matrix-refresh-all`, `v7-service-matrix-test`, `v7-egress-quality-compact`, `v7-telegram-sentinel`, `v7-egress-set-state`, `v7-operator-execution-packet`, `v7-client-speed-api` | systemd, deploy allowlist or direct live owner calls; M0B must split pre/post-apply responsibilities |
| `ASYNC_ENGINEERING_REQUIRED` | `v7-truth-check`, `v7-convergence-status`, `v7-convergence-owner`, `v7-intelligence-snapshot-refresh`, `v7-autonomy-trust-evidence-inventory`, `v7-observability-summary`, `v7-routing-intelligence-shadow`, `v7-path-sample-ingest`, `v7-path-benchmark`, `v7-path-optimizer-advice` | real engineering/truth/read-model consumers; not Core pre-apply by default |
| `LEGACY_EXCEPTION_REQUIRED` pending proof | `v7-governed-canary-dry-run-cycle`, `v7-restore-settle-gate`, `v7-second-canary-target-readiness`, `v7-route-movement-preview`, `v7-autoswitch-safety-review`, `v7-identity-consistency-review` | governed/certification/safety corpus; necessary semantics must be separated from legacy orchestration |
| `DEPLOY_RELEASE_REQUIRED` | `v7-safe-deploy`, `v7-safe-commit`, `v7-safe-push`, `v7-release-sync`, `v7-release-lineage-check`, `v7-sync-status`, `v7-runtime-repo-diff`, `v7-runtime-contract-validate`, `v7-runtime-tool-enumerate` | engineering delivery owners, never routine routing hot path |
| `MANUAL_OR_AUDIT_ONLY` pending current consumer proof | `v7-admin-endpoint-inventory`, `v7-admin-platform-review`, `v7-admin-ux-review`, `v7-control-plane-governance-check`, `v7-ctr-observation-window`, `v7-egress-import-regression`, `v7-egress-lifecycle-validate`, `v7-infrastructure-readiness-review`, `v7-intelligence-readiness-review`, `v7-public-gateway`, `v7-sensitive-state-check` | no systemd Runtime start; static references are review/test/engineering owners |
| `INSTALL_TEST_SUPPORT` | `v7-autoswitch-install-systemd`, `v7-run-tests` | explicit install/test entrypoints; no product decision ownership |
| `UNRESOLVED_STATIC_NO_CALLER` | none accepted for deletion | tools with no internal textual caller may be operator, packaging or external entrypoints; M0C requires deploy/config/shell evidence before `UNREACHABLE` |

### `admin_core` modules

| Initial class | Stable identities | Evidence / residual |
| --- | --- | --- |
| `CURRENT_PRODUCT_REQUIRED` | `registry_readers`, `routing_brain`, `routing_intelligence`, `operator_execution`, `operation_scoped_binding`, `operator_execution_pipeline`, `operator_execution_feedback`, `events`, `sanitize` | imported by Runtime/governed/autoswitch owners; exact responsibility and state/effect edges pending M0B |
| `ASYNC_ENGINEERING_REQUIRED` | `autonomy_trust_acceleration`, `intelligence_platform`, `intelligence_workers`, `intelligence_snapshots`, `shadow_autonomy`, `operator_decision_surface`, `explainability_adapter`, `runtime_read_views`, `time` | engineering/read-model/Polygon/truth consumers; no Core pre-apply admission by default |
| `READ_MODEL_UI_REQUIRED` | `admin_registry_views`, `diagnostic_views`, `operator_observability`, `operator_views`, `overview_views`, `performance_summaries`, `route_reality_views`, `route_views`, `service_views`, `summary_builders` | admin/read presentation chain; async/manual consumer classification, not routing truth |
| `PACKAGE_SUPPORT` | `__init__` | import/package boundary only |

`operation_scoped_binding` has no direct textual `admin_core.operation_scoped_binding` import because it is imported through `from admin_core import ...`; it remains reachable. `performance_summaries` similarly acts as a top-level aggregation consumer. These examples prove why text-only no-caller results cannot establish dead code.

### systemd/process truth

| Unit family | Configured behavior | Initial disposition evidence |
| --- | --- | --- |
| service Matrix | 15-minute timer plus up to 60-second jitter -> `v7-service-matrix-refresh-all` | current observer and execution wake; too slow/broad for future primary path |
| Telegram sentinel | 4-second timer -> sentinel with `--no-autoswitch` | current fast observer, no execution consumer |
| quality compactor | 5-minute timer -> quality compaction | async prepared evidence candidate |
| users autoswitch | 20-second timer definition -> governed validation service | source unit exists; live truth reports scheduler inactive in approved manual mode, so configuration is not current activation proof |
| OpenVPN template | managed external process per egress | legacy protocol owner; preserve until migration/exception evidence |
| draft planner/health | draft 30-second Planner and shell health loop | `HISTORICAL_OR_NOT_DEPLOYED` unless production identity proves installation; must not enter Core |

The principal owners contain 69 explicit subprocess launch/discovery sites. This confirms process topology is a first-class complexity surface, not an incidental implementation detail. M0B must classify each launch as product-required, async engineering, legacy exception, manual/test, or removal candidate.

## Root-cause hypotheses requiring M1B proof

1. `Reuse Existing Owner` removed owner proliferation but permitted unlimited semantic expansion of a few files.
2. `Architecture Closed by Default` and WIP/future-dependency protections made systemic replacement harder than adding another adapter/stage.
3. Completion gates were introduced after much of the architecture existed and validate typed local Missions, not continuous end-to-end Product Contract SLO/complexity.
4. Engineering evidence and audit lineage became synchronous prerequisites, converting development correctness into Runtime latency.
5. CPS accumulated hundreds of live-looking fields and historical projections; atomic writers normalize against hard-coded older Program identities.

These remain hypotheses until caller/consumer history and owner behavior are reconciled in M1B.

## RESET-M0 closure

RESET-M0 is complete against the immutable source generation named above. All 16 Program surfaces, all CPS capability groups, all 48 executable top-level tools, all 29 `admin_core` modules, and every configured systemd/process family are represented by an evidence-backed Intent Reality verdict or an exact residual routed to RESET-M0B/RESET-M0C/RESET-M1. The report also preserves the verified production relationship chain, the three systemic root causes, the active-Program consumer mismatch and the Product Contract verdict.

This terminal does not claim function-level code classification. That work is the explicit RESET-M0B successor and is not a coverage gap in RESET-M0. Static absence of a caller remains insufficient for deletion, no existing Program disposition is activated, and no historical label is treated as current production proof.

Self-review found no contradiction between the M0 conclusions and the preserved exhaustive-audit, deep-relationship, root-cause or evidence-driven-decision contracts. Failed or unproven criteria are carried forward as targeted residuals; already proven M0 areas are not re-audited without an exact invalidation trigger.

## Current residual and successor

RESET-M0 terminal: `RESET_M0_SYSTEM_REALITY_INTENT_AND_PRODUCT_CONTRACT_AUDIT_COMPLETE`.

Exact successor: `EXECUTE_RESET_M0B_CODE_REALITY_AND_COMPLEXITY_AUDIT`.

RESET-M0B must classify production-relevant functions and dynamic edges against the frozen scope without deletion or mutation. No Core design, implementation, disposition activation, Runtime mutation, production effect or Authority effect is admitted by this report.

## RESET-M0B code reality and responsibility manifest

Static AST coverage of the immutable scope accounts for 73 Python/executable code files, 129,532 LOC, 2,290 functions and 34 classes: 44 parseable `tools` Python entrypoints/libraries and all 29 `admin_core` modules. The four remaining executable tools are non-Python/install-test wrappers already accounted for in the executable ledger. Function containment is the logical coverage projection; high-impact routing, recovery and Authority owners receive the deeper edge analysis below, while UI/read-model/test/support functions retain sufficient owner and disposition classification without pretending equal Runtime risk.

| High-impact owner | Functions / classes | Proven responsibility domains | State/effect/process evidence | Semantic disposition | Residual / next action |
| --- | ---: | --- | --- | --- | --- |
| `tools/v7_sync_lib.py` | 306 / 0 | CPS/OMP normalization; capability and Mission reconciliation; Service Failure and Polygon lifecycles; truth/deploy/runtime evidence; external re-entry | 15 subprocess sites, five lock references, 91 atomic-write references, nine JSONL references and at least 64 Runtime/deploy state-path references; can launch or discover broad V7/systemd/ssh tooling | `SPLIT_BY_RESPONSIBILITY` | M1B separates development-state reconciliation from deploy/truth support; no Core admission |
| `tools/v7-users-autoswitch` | 309 / 4 | observe/parse; Planner/selection; Authority and policy gates; assignment mutation; route/payload verification; rollback/recovery; Service Failure closure | 17 subprocess sites, 55 atomic-write references, 47 JSONL references and at least 141 state-path references; calls `v7-user-switch`, route check, Matrix, snapshot, truth and state owners | `EXTRACT_LEGACY_BOUNDARY` | preserve current production owner until M6; map minimal plan/apply/verify semantics into M3 contract |
| `tools/v7-governed-canary-dry-run-cycle` | 103 / 0 | Candidate/Packet/lease orchestration; controlled campaigns; apply/verify/recovery; feedback and certification | 15 subprocess sites, 13 atomic-write references, 90 JSONL references and at least 290 state/audit references; option-driven dispatch is mainly `argparse.Namespace` field selection, not hidden function loading | `EXTRACT_LEGACY_BOUNDARY` | keep as acceptance/legacy exception until migration; exclude broad campaign machinery from Core |
| `tools/v7-service-matrix-refresh-all` | 46 / 0 | checker fan-out; Matrix/event writing; passive and OMP consumers; governed campaign wake | 13 subprocess sites, two lock references, five atomic-write references, 12 JSONL references and at least 70 state/audit references | `EXTRACT_LEGACY_BOUNDARY` | retain observation compatibility; separate broad engineering/transaction dispatch from future observe receipt |
| `admin_core/operator_execution.py` | 161 / 1 | Authority requests/decisions; Packet/lease/barrier; action-class policy; replay/idempotency; durable execution audit | two lock references, 43 atomic-write references, 16 JSONL references and policy/audit/restore-barrier state; no subprocess apply owner | `KEEP_COHESIVE` | preserve Authority semantics; M3 consumes only minimal generation/policy/lease interface |
| `admin_core/operator_execution_pipeline.py` | 95 / 0 | governance/readiness models; simulation; performance and recovery contracts; knowledge-gated dry-run projections | predominantly pure/read-model transformations; three atomic helper references, no production subprocess owner | `REVIEW_AFTER_MIGRATION` | reuse acceptance contracts; do not place projection pipeline in Core |
| `admin_core/autonomy_trust_acceleration.py` | 200 / 0 | confidence/evidence/suitability/promotion and autonomy maturity projections | predominantly pure engineering models; no subprocess, network or durable Runtime writer proven | `REVIEW_AFTER_MIGRATION` | async engineering only; necessity/duplication disposition in M0C/M1 |
| `tools/v7-control-plane-governance-check` | 74 / 0 | broad governance/history consistency checks | manual/audit entrypoint, not configured routing apply owner | `REVIEW_AFTER_MIGRATION` | retain only owner-backed acceptance value after Core proof |

The function-name/domain projection is not used as caller proof. It is an accounting layer over exact file ownership. Direct calls, imports, subprocesses, systemd and file/JSON/JSONL exchanges determine reachability; `getattr(args, ...)` in autoswitch/governed owners is option/state dispatch and does not establish an independently loaded function. Static no-caller findings remain unresolved rather than deleted when packaging, operator or external callers are possible.

### Producer-consumer and state/effect graph

| Producer -> transport -> consumer | State/effect | Placement verdict | Owner-backed residual |
| --- | --- | --- | --- |
| systemd Matrix timer -> subprocess -> `v7-service-matrix-refresh-all` -> seven checker children | reads policy/registry/health; writes Matrix/events | observer is required; 15-minute cadence and full fan-out cannot satisfy primary recovery contract | retain legacy observation, define compact fresh receipt in M3 |
| Matrix/events -> file/JSONL -> passive/autoswitch consumers | failure generation and affected scope | necessary signal is mixed with historical/reconciliation surfaces | M2 names one authoritative generation/health receipt |
| Matrix -> subprocess -> OMP/Service Failure reconciliation in `v7_sync_lib.py` | writes CPS/receipts/wakes before routing effect | `WRONG_ARCHITECTURAL_PLACEMENT` for synchronous recovery | development continuation remains async; exclude from Core |
| advisory/Planner -> in-process/file state -> governed cycle | produces moves, Candidate/Packet/lease inputs | selection and certification responsibilities are duplicated across autoswitch/governed/execution owners | M0C exact duplication disposition; M3 one pure PLAN contract |
| governed cycle -> subprocess -> `v7-users-autoswitch --apply` | assignment/kernel mutation through existing `v7-user-switch` and state owners | current required legacy apply, but preceded by broad orchestration | preserve until fenced cutover; M3 one APPLY owner |
| apply -> route/payload checks -> outcome/audit/rollback | kernel visibility, payload proof, recovery | `REAL_SAFETY_PROTECTION`; maximum evidence depth required | preserve compact verify/recovery semantics |
| outcome -> JSONL/CPS/Replay/Learning/closure | durable engineering and historical evidence | valuable after effect, not a pre-apply dependency | move to recoverable asynchronous closure contract |

### Code-reality findings

1. `OVERSIZED_OWNER_REUSE`: owner reuse prevented owner proliferation but concentrated unrelated lifecycles in `v7_sync_lib.py` and autoswitch. Their separate callers, state surfaces and change reasons prove semantic split/extraction is warranted; file size alone did not decide it.
2. `DUPLICATED_TRANSACTION_ORCHESTRATION`: Matrix, autoswitch, governed cycle and operator execution each contain admission/selection/stage/closure concepts. M0C must decide which semantics survive; M0B grants no removal.
3. `STATE_AND_EFFECT_COLOCATION`: autoswitch reads broad engineering state, plans, mutates assignments, verifies and closes evidence in one owner. The actual mutation remains necessary, but its synchronous dependencies violate the product contract.
4. `DYNAMIC_EDGE_BOUND`: principal dynamic behavior is command/path/argument selection plus subprocess and state exchange. No plugin-style production function loader was found in the high-impact owners. External/operator/package entrypoints remain explicitly unresolved where source cannot prove the caller.
5. `REAL_SAFETY_SEMANTICS_PRESENT`: Authority, Packet, lease, replay/idempotency, restore barrier, rollback and route/payload verification have concrete owners and effects; audit shrink cannot remove them.

### RESET-M0B residual

The production call/state/effect graph and semantic large-file dispositions are proven for the high-impact mutation, recovery and Authority owners. Every scoped function is accounted through its owning file/module and risk-proportional responsibility class; non-static and external caller uncertainty remains explicit rather than converted into deletion proof. RESET-M0B terminal: `RESET_M0B_CODE_REALITY_COMPLEXITY_AND_RELATIONSHIP_MANIFEST_COMPLETE`.

The remaining bounded criterion is reconciliation of duplicated/no-live-consumer/manual/test/historical classifications across the already-accounted tool/module ledger. Exact successor: `EXECUTE_RESET_M0C_DUPLICATION_DEAD_CODE_AND_LEGACY_SURFACE_AUDIT`. No mutation is required to proceed.

## RESET-M0C duplication, dead-code and legacy disposition

The question `WHO_CALLS THIS IN REAL NON-TEST OPERATION?` was applied through configured systemd callers, direct imports/calls, subprocess discovery, deploy/package manifests and explicit operator entrypoint status. The complete tool/module identities remain in the earlier ledger; this matrix changes decision context by grouping duplicated responsibilities rather than repeating every identity.

| Responsibility surface | Existing implementations/consumers | Disposition | Necessary semantics / exact residual |
| --- | --- | --- | --- |
| observation and health | Matrix refresh/test, Telegram sentinel, quality compactor, autoswitch observations, `routing_intelligence` | `CURRENT_PRODUCT_REQUIRED` plus `DUPLICATED` aggregation | keep fresh health/capacity/failure facts; M2/M3 select one receipt contract, legacy observers remain until cutover |
| planning and selection | `AutoswitchPlanner`, `routing_brain`, `routing_intelligence`, governed Candidate selection, pipeline advice/ranking | `DUPLICATED` | preserve policy/capacity/eligibility semantics; future Core gets one pure deterministic PLAN owner |
| Authority/admission | `operator_execution`, autoswitch gates, governed Packet/lease guards | `CURRENT_PRODUCT_REQUIRED`; orchestration duplicated, Authority owner not duplicated | preserve `operator_execution` Authority; callers consume a compact owner-issued contract |
| assignment/kernel apply | autoswitch plus `v7-user-switch` and `v7-egress-set-state` | `CURRENT_PRODUCT_REQUIRED` / `LEGACY_EXCEPTION_REQUIRED` | preserve current writer until fenced migration; one future APPLY writer only |
| route/payload verification | autoswitch, governed cycle, user-route checker, Matrix checker | `CURRENT_PRODUCT_REQUIRED` plus `DUPLICATED` | preserve exact route visibility and payload proof; remove repeated broad verification only after M5 evidence |
| rollback/recovery/barrier | autoswitch, governed cycle, `operator_execution` restore barrier | `CURRENT_PRODUCT_REQUIRED` / `REAL_SAFETY_PROTECTION` | maximum evidence depth; no removal candidate |
| CPS/OMP/Program reconciliation | `v7_sync_lib.py`, autoswitch, Matrix/OMP consumers | `ASYNC_ENGINEERING_REQUIRED` and `WRONG_ARCHITECTURAL_PLACEMENT` | keep development continuation outside future routing hot path; repair hard-coded identity in its owner phase |
| snapshot/inventory/read models | snapshot refresh, intelligence modules, registry/admin views | `ASYNC_ENGINEERING_REQUIRED` or `READ_MODEL_UI_REQUIRED` | derive asynchronously; cannot block apply and cannot become routing truth |
| evidence/Replay/Learning/campaigns | governed cycle, sync library, autonomy/pipeline models, JSONL closures | `ASYNC_ENGINEERING_REQUIRED` / `LEGACY_EXCEPTION_REQUIRED` | consume compact outcome after effect; campaign machinery is acceptance corpus, not Core machinery |
| deploy/release/truth tooling | safe deploy/commit/push, release/convergence/runtime checks | `DEPLOY_RELEASE_REQUIRED` | separate engineering lifecycle; never routine routing hot path |
| admin/review/diagnostic CLIs | inventory/platform/UX/governance/infrastructure/intelligence reviews | `MANUAL_ONLY` or `ASYNC_ENGINEERING_REQUIRED` | retain where operator/acceptance consumer exists; package separately after migration review |
| tests/install wrappers | systemd installer and test runner | `TEST_SUPPORT_ONLY` / `INSTALL_TEST_SUPPORT` | no product decision ownership |
| draft planner/health units | draft unit files without production installation evidence | `HISTORICAL_ONLY` | exclude from deployment and Core; physical deletion requires later packaging/history proof |

No function, module, service or CLI receives `UNREACHABLE` or `REMOVE_CANDIDATE` from static evidence alone. All executable tools have a repository packaging/deploy/operator reference, and external/manual invocation cannot be disproved from source. This is a conservative evidence result, not a claim that every surface should survive migration. M7/M9 removal requires replacement semantics, production reachability proof, rollback and measured shrink.

### Unknown and external residual register

| Residual | Evidence class | Owner | Disposition / successor |
| --- | --- | --- | --- |
| operator-invoked review/diagnostic frequency | `REQUIRES_EXTERNAL_OWNER` | existing operator/tool owners | retain as `MANUAL_ONLY`; packaging review after migration |
| consumers outside repository/deploy manifest | `UNKNOWN` bounded by packaging evidence | existing deploy/release owner | do not delete; recheck at M7/M9 only if removal proposed |
| draft unit historical retention need | `HISTORICAL` | existing systemd/repository owner | exclude from Runtime; decide physical retention in M9 |
| exact duplicate helper-level serialization/hash/read functions | `STATIC_PROVEN` duplicate form, effect equivalence unproven | owning modules | no mechanical merge; consolidate only with behavior/replay proof |
| hard-coded Service Failure/Polygon Program normalization | `STATIC_PROVEN` and truth-check `NO-GO` | CPS/OMP consumers in sync/autoswitch/operator execution | M1B law/root-cause disposition, M2 compact truth correction; no audit-phase patch |

### RESET-M0C terminal

The duplication/dead/legacy matrix covers every previously inventoried code/service/CLI identity through an owner-backed class or exact external residual. Necessary product, safety, recovery and Authority semantics are separated from legacy development/campaign machinery. Terminal: `RESET_M0C_DUPLICATION_DEAD_CODE_AND_LEGACY_DISPOSITION_COMPLETE`.

Exact successor: `EXECUTE_RESET_M1_PROGRAM_PORTFOLIO_DISPOSITION`.

## RESET-M1 Program portfolio disposition

Disposition separates intent/policy/acceptance value from legacy execution machinery and historical evidence. It does not physically remove or rewrite any Program in this phase.

| Existing Program/state surface | Disposition | Preserved value | Excluded or later action |
| --- | --- | --- | --- |
| System Reset and Routing Core Migration | `COMPLETE_AND_CLOSE` after M9 | this bounded M0-M9 contract and completion evidence | must not become permanent Reset machinery |
| OMP | `REDESIGN` | development-plane admission, evidence and exact-successor discipline | synchronous routing lifecycle and Runtime selection excluded; laws reviewed in M1B |
| Current Program State | `KEEP_PERMANENT` | sole compact volatile Program/capability frontier owner | routing Runtime truth and historical projection bulk excluded through M2 |
| Implementation Program | `COMPLETE_AND_CLOSE` | lifecycle/history and reusable acceptance discipline | no active parallel implementation Program/queue after Reset |
| Implementation Backlog | `COMPLETE_AND_CLOSE` | completed 34/34 historical evidence | no permanent active backlog projection without owner-backed new work |
| Autonomous Evolution Program | `REDESIGN` | bounded development input and knowledge-to-gap intent | autonomous roadmap/planning expansion and hot-path participation excluded |
| Behaviour Discovery Program | `KEEP_AS_ACCEPTANCE_CONTRACT` | failure taxonomy, behavior scenarios and discovery criteria | no automatic Runtime/Program expansion; execution remains async/on demand |
| Stage 2 Knowledge Engineering | `COMPLETE_AND_CLOSE` | locked canonical knowledge and evidence | completed Program machinery not retained as active lifecycle |
| Research Framework | `KEEP_PERMANENT` | lightweight bounded research method under existing owners | no Runtime dependency, roadmap or routing Authority |
| Routing Digital Twin Polygon Master | `KEEP_AS_ACCEPTANCE_CONTRACT` | scenarios, replay/decision equivalence and isolation criteria | Polygon execution excluded from Core and synchronous routing |
| Permanent Polygon OMP Integration | `MERGE` | useful OMP acceptance inputs and evidence | separate Program machinery merges into OMP/Polygon acceptance contract |
| Permanent Polygon Design-Time Completion | `MERGE` | design-time validation criteria and corpus | separate lifecycle/mission progression closes into acceptance corpus |
| Permanent Polygon Target-Level Completion Plan | `COMPLETE_AND_CLOSE` | historical target-level evidence | no current independent consumer or parallel plan owner |
| L7/L8 Evidence and Authority Evolution | `KEEP_AS_ACCEPTANCE_CONTRACT` | controlled/natural evidence separation and no implicit Authority | campaign progression excluded from Core; natural evidence remains unmanufactured |
| Service Failure Automation Evolution | `REDESIGN` | failure generation, health, causal integrity, rollback/recovery and incident semantics | legacy multi-stage orchestration, OMP/CPS progression and campaign work excluded from future hot path |
| Service Failure Lifecycle and Multi-Lane Product Evolution | `MERGE` | incident/multi-lane evidence and closure semantics | separate Program identity merges with redesigned Service Failure acceptance/async closure |

No owner boundary changes here. `MERGE`, `REDESIGN` and `COMPLETE_AND_CLOSE` are owner-backed target dispositions consumed by later phases; source documents and historical evidence remain intact until M9 proves safe physical cleanup. CT-M0F recovery clock, meaningful valid-sample laws, initial `<3 s` production gate and prepared warm-path `<1 s` target are preserved as acceptance contracts; legacy topology/orchestration is `LEGACY_ONLY` pending migration.

RESET-M1 terminal: `RESET_M1_ALL_EXISTING_PROGRAM_DISPOSITIONS_OWNER_BACKED`.

Exact successor: `EXECUTE_RESET_M1B_OMP_AND_DEVELOPMENT_SYSTEM_FAILURE_ANALYSIS`.

## RESET-M1B OMP and development-system failure analysis

The OMP laws are internally coherent as local engineering controls, but their composition optimized for owner reuse, lifecycle continuity and evidence production rather than bounded end-to-end product behavior. Several important gates were added after the oversized architecture existed. Their machine-checkable completion class is selected per Mission, so an analysis, acceptance, documentation or implementation terminal can be lawful while the parent Product Contract remains unrealized. CPS explicitly retained `NO_OR_PARTIAL` U02-U22 consumer/effect residuals, yet independent capability work and protection laws permitted further local Missions.

| OMP law/control | Evidence-backed disposition | Failure mechanism | Preserved/replacement rule |
| --- | --- | --- | --- |
| Architecture Closed by Default | `REDESIGN` | defaulted systemic defects to unfinished integration/certification inside existing architecture; made architectural correction the last resort | reuse first remains, but a measured Product Contract/complexity failure is a valid architecture-gap trigger |
| Architecture Phase Complete / redesign prohibitions | `SUPERSEDE_FOR_RESET` | historical completion claims could prevent correcting the now-proven architecture defect | Reset owner evidence and M3 contract may redesign within unchanged safety/Authority boundaries |
| Semantic Reuse / Need New Owner Gate | `KEEP` plus complexity budget | correctly prevented parallel owners but allowed indefinite semantic extension of two oversized owners | reuse existing owners only while responsibility, hot-path and total-system budgets remain satisfied |
| Capability Maturity Protection | `REDESIGN` | protected implementation topology whenever attached to unfinished capability, including topology causing the failure | protect required capability behavior/evidence, not every legacy implementation object |
| Engineering WIP Protection | `REDESIGN` | almost any object connected to an unfinished chain became non-minimizable; open work could indefinitely preserve obsolete construction | protect active effects/safety and bounded work scope; allow owner-backed replacement with preserved terminal path |
| Approved Future Dependency Protection | `SCOPE_DOWN` | future plans could make existing objects permanently necessary without renewed necessity/product proof | require named approved consumer, expiry/invalidation and replacement compatibility |
| Mission Completion Evidence Gate | `REDESIGN` | correctly distinguishes completion classes, but validates the declared local contract and does not force parent Product Contract closure | every local terminal must propagate an explicit parent-product effect/residual before more architecture growth |
| Behavior Enforcement | `SIMPLIFY` | producer/consumer/next-output proof exists, but chains were evaluated locally and expanded documentation/evidence surfaces | retain compact end-to-end behavior proof tied to the fundamental Product Contract |
| Intent Gap Detection/Closure | `REDESIGN` | gaps recursively produced BDP/OMP work, encouraging more candidates and lifecycle machinery instead of systemic simplification | first classify architecture/complexity root cause; prefer merge/simplify/remove before extend |
| Necessity Framework | `KEEP` with execution gate | necessity existed mainly as documentary verdict and could not overcome protection laws | execute at M7/M9 with reachability, replacement and measured shrink proof |
| Decision Trace/Reproducibility | `SCOPE_DOWN` | useful evidence became broad synchronous decision/campaign material | compact Runtime decision receipt; full trace asynchronous |
| Safety-Bounded Authority, Packet/lease, rollback, verification | `KEEP` | no evidence these protections caused the primary failure; they prevented unsafe mutation | preserve as `REAL_SAFETY_PROTECTION`, evaluate compact placement only |
| CPS sole volatile owner / Engineering Truth Lifecycle | `KEEP` and `SIMPLIFY` | correct ownership, but normalized writers retained hard-coded old Program identities and excessive projections | M2 compact CPS; consumers must not invent/normalize a competing active Program |

### Exact root-cause chain

`local typed terminal -> report/test/certification evidence -> capability/Program continuation -> protection of unfinished topology -> extension of existing oversized owners -> more state/process/evidence edges -> locally valid consumers -> parent routing Product Contract still partial`.

The last responsible development-system link is the absence of a mandatory `local terminal -> parent Product Contract effect or exact bounded residual` propagation gate before admitting further capability/architecture growth. The next responsible link is protection of implementation topology rather than necessary behavior. The Runtime manifestation is synchronous use of engineering reconciliation/campaign machinery around a sub-second mutation.

### RESET_OMP_CONTRACT_CONFLICT

`RESET_OMP_CONTRACT_CONFLICT` is materialized for Architecture Closed by Default, historical Architecture Phase Complete/redesign prohibitions, and the three protection laws. The Reset Program's owner-backed Product Contract and production/complexity evidence supersede those legacy-development protections only for M2-M9 correction. Real safety, Authority, production mutation, rollback, verification, active writer fencing and evidence preservation are not superseded.

### Master Audit self-review

- Goal coverage: all M0-M1B phase criteria and six logical outputs have a conclusion, evidence basis, owner, disposition, residual and successor.
- Contradictions: CPS/OMP documented frontier is internally aligned; truth-check still exposes hard-coded legacy normalization, carried to M2 rather than hidden.
- Root-cause depth: causal chain reaches product intent, development admission, code/process/state topology and observed production latency.
- Product trace: the fundamental recovery contract is linked to measured 58.761588 s lifecycle, approximately 0.878 s mutation/visibility, synchronous pre-apply machinery and exact preserve/exclude decisions.
- Targeted recheck: only previously failed/unproven criteria were revisited; no valid scope area was fully re-audited.

Terminals: `RESET_MASTER_AUDIT_REPORT_GOAL_COVERAGE_RECONCILED`, `DEEP_PROGRAM_COMPONENT_FUNCTION_RELATIONSHIP_GRAPH_PROVEN`, and `RESET_MASTER_AUDIT_REPORT_FINAL_SELF_REVIEW_PASS`.

RESET-M1B terminal: `RESET_M1B_OMP_AND_DEVELOPMENT_SYSTEM_FAILURE_ROOT_CAUSE_PROVEN`.

Exact successor: `EXECUTE_RESET_M2_TRUTH_OWNER_AND_STATE_SURFACE_COLLAPSE`.

---

# RESET-M1B Master Audit Closure and RESET-M2 Activation Engineering Report

Status: `RESET_MASTER_AUDIT_REPORT_FINAL_SELF_REVIEW_PASS`

The Master Audit now proves the development-system root cause and assigns dispositions to the relevant OMP laws. Local typed terminals, topology-protection laws and unbudgeted owner reuse explain how locally valid progress accumulated without the parent routing Product Contract. `RESET_OMP_CONTRACT_CONFLICT` supersedes only legacy development protections needed for Reset correction; real safety, Authority, rollback and verification remain mandatory.

Risk closed: Reset can correct the proven architecture defect without treating historical Architecture Complete/protection claims as an absolute veto, and without weakening production safety.

Owners affected: no boundary changes. CPS remains volatile state owner; OMP remains development-plane orchestrator.

- Evidence: `docs/reports/engineering/V7_SYSTEM_RESET_MASTER_AUDIT_REPORT.md`.
- Exact successor: `EXECUTE_RESET_M2_TRUTH_OWNER_AND_STATE_SURFACE_COLLAPSE`.
- Runtime effects = `NONE`.
- Production effects = `NONE`.
- Authority effects = `NONE`.

---

# RESET-M2 Truth Owner and State Surface Collapse Engineering Report

Status: `RESET_M2_ONE_OWNER_PER_NECESSARY_RUNTIME_FACT_AND_COLLAPSE_DISPOSITIONS_COMPLETE`

Intent closed: every necessary routing Runtime fact now has one named existing authoritative owner and every surrounding projection has a collapse disposition. This phase changes no live Runtime state or routing behavior.

| Runtime fact | Authoritative existing owner/source | Necessary reader/decision | Freshness/invalidation | Disposition |
| --- | --- | --- | --- | --- |
| user assignment | existing users/assignment registry written by `v7-user-switch`/autoswitch owner | PLAN delta, APPLY CAS, route verify | assignment generation; any writer commit invalidates | `KEEP_AUTHORITATIVE` |
| egress health | current Service Matrix/quality owner receipt | OBSERVE/PLAN target eligibility | generation and bounded age; new probe/failure invalidates | `KEEP_AUTHORITATIVE` |
| capacity | existing egress registry plus generation-bound Matrix capacity receipt | PLAN admission and blast reserve | registry/policy/assignment change invalidates | `MERGE` into one prepared target receipt |
| active policy | `/etc/v7/policy.json` existing policy owner | PLAN and pre-apply safety validation | policy generation/hash; any owner write invalidates | `KEEP_AUTHORITATIVE` |
| Authority generation | `admin_core/operator_execution.py` owner-issued policy/Authority audit lineage | pre-apply admission | expiry, policy/decision supersession invalidates | `KEEP_AUTHORITATIVE` |
| incident/failure generation | existing Service Failure/Matrix incident owner | OBSERVE trigger and affected scope | fresh Matrix generation/recovery invalidates | `MERGE` into compact failure receipt; legacy incident history read-only |
| target health receipt | existing Matrix exact-path receipt | PLAN target and bounded revalidation | path fingerprint, generation, age or topology change invalidates | `KEEP_AUTHORITATIVE` |
| active operation/lease | existing `operator_execution` Packet/lease/barrier owner | single-writer fencing and idempotency | terminal/expiry/generation mismatch invalidates | `KEEP_AUTHORITATIVE` |
| kernel route state | Linux kernel route/rule/mark tables through existing route-check owner | APPLY reconciliation and VERIFY | every apply/netlink/process change invalidates | `KEEP_AUTHORITATIVE` |
| verification result | existing exact user-route/payload verifier receipt | success, rollback or forward recovery | operation/generation/route/payload context bound | `KEEP_AUTHORITATIVE` |
| outcome | existing execution feedback/closure append-only owner | async evidence, Replay, Learning, CPS/OMP residual | immutable operation identity; correction is append-only | `KEEP_AUTHORITATIVE` |

Collapse dispositions for surrounding surfaces:

- CPS remains sole compact Program/capability frontier; it is `DERIVED_ASYNC_ONLY` for routing facts and cannot be a Core input.
- OMP, Reports, Production Maturity, Replay, Learning, Polygon and campaign state are `DERIVED_ASYNC_ONLY`.
- broad snapshots, dashboards and inventories are `DERIVE_ON_DEMAND` or `DERIVED_ASYNC_ONLY`.
- historical Packet, Mission, incident and campaign projections are `LEGACY_READ_ONLY`.
- duplicate capacity/health/incident summaries `MERGE` into generation-bound prepared receipts; physical retirement waits for M7/M9 evidence.

The current detailed CPS compatibility projection remains source history during migration, but only its Section 0 Program frontier is authoritative. It does not gain routing-truth status. Hard-coded legacy Program normalization remains a source defect to be corrected with compact CPS consumer work; it grants no production/runtime effect in this report.

Owner: existing Runtime fact owners, CPS volatile owner and OMP development-plane owner. No new owner/store/registry was created.

Evidence: Master Audit code/state graph, CPS Section 0, SYSTEM_MAP routing truth chain, existing policy/Matrix/assignment/operator-execution/verifier/feedback owners.

Residual: specify the exact vNext positive/negative contracts, recovery clock, freshness decisions, fencing and crash recovery before code.

Exact successor: `EXECUTE_RESET_M3_VNEXT_ARCHITECTURE_AND_MINIMAL_CORE_CONTRACTS`.

- Runtime effects = `NONE`.
- Production effects = `NONE`.
- Authority effects = `NONE`.

---

# RESET-M3 vNext Architecture and Minimal Core Contracts Engineering Report

Status: `RESET_M3_VNEXT_POSITIVE_NEGATIVE_RECOVERY_AND_COMPLEXITY_CONTRACTS_ACCEPTED`

Intent closed: the future Core is specified before code as one compact five-stage contract under existing Runtime/policy/Authority/assignment/verifier owners. The new module is justified only as the isolated replacement boundary required to remove engineering-plane work from the synchronous routing lifecycle; it is not a new Program, Planner, scheduler, truth source or Authority owner.

## Positive contract

Input envelope `v7.routing-core-input.v1` contains immutable `generation`, `observed_at`, bounded freshness deadline, current assignments, health/capacity receipts, policy generation, Authority generation, operation/lease identity and exact scope. All identities are strings; cohorts are bounded and deterministically ordered.

1. `OBSERVE` validates schema, generation, identity and freshness and returns a normalized immutable receipt.
2. `STATE` validates one authoritative value per M2 fact and derives no historical/engineering state.
3. `PLAN` is pure and deterministic: eligible healthy targets with reserve are ranked by declared policy; output is only the minimal desired-assignment delta.
4. `APPLY` contract accepts current generation, operation id, idempotency key and fencing token; M4 shadow implementation emits no effect. Later effectful adapters must use the existing assignment/kernel writer.
5. `VERIFY` contract binds assignment, kernel visibility, exact user routing context, expected egress and payload result to the same operation/generation.

Mandatory gates: exact source/target identity, lawful target, capacity reserve, current policy/Authority generations, bounded scope, one active operation, CAS/fencing, idempotency, cooldown/anti-flap, circuit breaker/blast radius, rollback or forward-recovery readiness, route visibility and exact payload proof.

## Negative contract

Core must not read or execute OMP, CPS progression, Reports, Production Maturity, Learning, Replay, Polygon, historical incident reconciliation, campaign/certification history, full Matrix when a compatible fresh receipt exists, broad inventory refresh, Planner subprocess chains, expanded Outcome/closure objects or engineering scheduling. It cannot grant Authority, write policy, create users/targets, invent health/capacity, infer fresh truth from history or mutate during shadow mode.

## Recovery clock

Canonical end-to-end clock: `FIRST_QUALIFYING_FAILURE_EVIDENCE -> EXACT_CLIENT_NETWORK_CONTEXT_TARGET_PAYLOAD_RECOVERY`.

| Span | Initial hard budget |
| --- | ---: |
| failure receipt publication | 500 ms |
| input/state validation | 100 ms |
| deterministic plan | 100 ms |
| Authority/fencing/pre-apply validation | 200 ms |
| assignment/kernel apply | 1,000 ms |
| kernel visibility | 300 ms |
| exact-context payload verification | 800 ms |
| total initial production gate | `<3,000 ms` |

Prepared compatible warm-path target is `p95 <1,000 ms` end to end with a 1,500 ms hard ceiling. Lifecycle closure is separately measured and never substitutes for traffic recovery.

## Freshness decisions

Every health/capacity/policy/Authority/identity/membership/target receipt has owner, generation, `observed_at`, maximum age and invalidators. Exactly one result is legal: `USE_FRESH_PREPARED_RECEIPT`, `BOUNDED_SYNCHRONOUS_REVALIDATION`, `FALLBACK_TO_LEGACY`, or `STOP_SAFE`. Missing identity/policy/Authority/fencing is always `STOP_SAFE`; stale compatible health may use bounded existing-owner revalidation; unavailable Core or unsupported scope is `FALLBACK_TO_LEGACY`; no stale input triggers broad Core-side reconciliation.

## Single writer and crash recovery

Legacy remains sole production writer through M5. Shadow Core has `effects=ZERO`. Later ownership is scope-specific and atomic: a current generation plus operation id plus fencing token admits exactly one writer; stale Legacy/Core tokens reject before mutation. A compact apply receipt records intended delta, committed assignment/kernel identity and verification obligation. Restart reconciles receipt with assignment/kernel truth, then resumes verify, rollback or forward recovery and emits exactly one asynchronous closure obligation. `APPLY_SUCCEEDED_CLOSURE_LOST` is forbidden.

## Preserve/exclude and complexity budget

Preserve policy/Authority, assignment truth, health/capacity/freshness, cooldown/anti-flap, circuit breaker/blast radius, idempotency/fencing, rollback/forward recovery, route/payload verification and append-only outcome lineage. Exclude all engineering-plane surfaces named by the negative contract.

M3 baseline remains: 129,532 production Python/tool LOC in the audited scope; 17+ state surfaces; at least nine pre-apply hops; at least six pre-apply durable writes; 69 explicit subprocess/discovery sites; 58.761588 s observed lifecycle versus approximately 0.878 s mutation/visibility. M4 Core budget: one module, no process/timer/store/owner, zero effectful subprocesses, zero durable writes/locks/network calls in shadow planning, and a focused pure-contract test surface. Every later delta must reduce total active hot-path surface before completion.

Owner: existing `admin_core` Runtime model namespace, existing policy/Authority/assignment/verifier owners. Core earns effect Authority only through M4-M6 evidence.

Evidence: RESET Master Audit, RESET-M2 state-owner report and existing Reset Program contracts.

Residual: implement the effect-free pure Core, tests and shadow comparator within the accepted budget.

Exact successor: `EXECUTE_RESET_M4_EFFECT_FREE_SHADOW_CORE_IMPLEMENTATION_AND_GATES`.

- Runtime effects = `NONE`.
- Production effects = `NONE`.
- Authority effects = `NONE`.

---

# RESET-M4 Effect-Free Shadow Core Engineering Report

Status: `RESET_M4_EFFECT_FREE_SHADOW_CORE_FUNCTIONAL_AND_COMPLEXITY_GATES_PASS`

What changed: one new 220-LOC pure module, `admin_core/routing_core.py`, implements the accepted OBSERVE -> STATE -> PLAN -> shadow APPLY -> VERIFY contract. One 100-LOC focused test module covers determinism, immutability, stale input, fencing, Authority scope/blast, target eligibility, capacity and engineering-plane exclusion.

Intent closed: Core can produce a deterministic minimal desired-assignment delta from one generation-bound envelope while proving `effects=ZERO`. Legacy remains sole writer and the module has no file/network/process/lock/durable-state behavior.

Evidence:

- `python3 -m unittest tests.unit.test_routing_core`: 8/8 PASS.
- 1,000 in-process shadow runs: p50 0.0661 ms, p95 0.0688 ms, max 0.1128 ms; effects ZERO; stable two-move plan.
- static source check: no I/O, subprocess, lock, network or OS mutation imports/calls.
- deterministic fingerprint binds generation, policy generation, Authority generation, operation and desired delta.

Complexity BEFORE: no Core; audited 129,532 LOC; 17+ state surfaces; >=9 pre-apply hops; >=6 durable writes; 69 subprocess/discovery sites. AFTER M4 source: Core 220 LOC, one module, zero new process/timer/store/owner/state surface/subprocess/lock/durable write/network call. Runtime hot path delta = 0 because Shadow Core is not deployed or wired.

Risk closed: a future decision comparator can test Core logic without creating a second writer or allowing CPS/OMP/history/campaign inputs into routing decisions.

Owner: existing `admin_core` namespace; existing policy, Authority, assignment and verification owners remain authoritative.

Residual: compare Core and legacy decisions across replay/Polygon cases, classify every divergence, and consume the result without reproducing legacy defects.

Exact successor: `EXECUTE_RESET_M5_DECISION_EQUIVALENCE_AND_POLYGON_VALIDATION`.

- Runtime effects = `NONE`.
- Production effects = `NONE`.
- Authority effects = `NONE`.

---

# RESET-M5 Decision Equivalence and Polygon Validation Engineering Report

Status: `RESET_M5_CLASSIFIED_DECISION_EQUIVALENCE_AND_POLYGON_VALIDATION_PASS`

What changed: no Runtime code or wiring changed. Existing autoswitch/Polygon-derived policy fixtures and the new Core shadow tests were consumed as one decision-equivalence gate.

Evidence: 12/12 focused tests PASS, covering transient versus persistent service failure, source-scoped selection, multiple transient failures, deterministic Core planning, freshness, Authority/fencing/blast, target health/allowlist/capacity, zero effects and engineering-plane exclusion.

| Comparison | Verdict | Classification |
| --- | --- | --- |
| transient single-sample or nonpersistent failure | Legacy selects no move; Core receives no qualifying failure scope | `EQUIVALENT_AT_CONTRACT_BOUNDARY` |
| persistent qualifying source failure with healthy lawful target | Legacy selects failover; Core returns `PLAN_READY` for same source/user/target class | `EQUIVALENT_REQUIRED_BEHAVIOR` |
| source-scope mismatch | Legacy selects zero moves; Core validates exact declared scope/assignments | `EQUIVALENT_REQUIRED_BEHAVIOR` |
| unhealthy/disallowed/no-capacity target | both refuse a move | `EQUIVALENT_SAFETY` |
| missing/stale Authority, generation or fence | Core STOP_SAFE is stricter than legacy dry-run planning | `INTENTIONAL_CORE_SAFETY_DIVERGENCE` |
| target ranking | Legacy uses broad advice/history; Core uses fresh allowed/healthy capacity and deterministic tie-break | `INTENTIONAL_SIMPLIFICATION`; any policy-required ordering must be prepared by the policy owner before Core |
| evidence/closure expansion | Legacy produces broad operation/campaign artifacts; Core emits only compact shadow decision/apply/verify contracts | `INTENTIONAL_ASYNC_DIVERGENCE` |

No unexplained divergence remains in the admitted Core contract. Polygon/replay evidence is consumed as acceptance corpus, not copied into Core or executed synchronously. Proven legacy defects—broad pre-apply reconciliation, historical state dependence, campaign bookkeeping and multi-process planning—were not reproduced.

Risk closed: superficial same-output equivalence cannot force known legacy defects into Core, while required failure classification, target legality, capacity and safety behavior remain covered.

Owner: existing autoswitch/Polygon test owners and the existing `admin_core` namespace. Legacy remains sole production writer.

Complexity delta: code delta 0 in M5; process/timer/store/state/writer delta 0; Runtime hot-path delta 0.

Residual: prepare a controlled scope-specific migration adapter with atomic writer fencing, deploy through the existing safe owner, and prove zero double-write before any Core effect.

Exact successor: `EXECUTE_RESET_M6_CONTROLLED_MIGRATION_SINGLE_WRITER_FENCED_CUTOVER`.

- Runtime effects = `NONE`.
- Production effects = `NONE`.
- Authority effects = `NONE`.


---

<!-- Source report: docs/reports/engineering/2026-08-13_340000_reset_m10_contract_amendment.md -->

# RESET-M10 Contract Amendment Engineering Report

Status: `RESET_PROGRAM_CONTRACT_RECONCILED_FOR_M10_EXECUTION; RESET_M10_NOT_EXECUTED`

## What changed

The existing `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1` now contains an explicit dependency order: M10.1 responsibility audit; M10.2 industry benchmark; M10.3 `CHANNEL_HEALTH_MODEL`; M10.4 `FINAL_PRIMARY_RUNTIME_BOUNDARY` and routing-decision minimality; M10.5 Engineering Plane extraction; M10.6 fast/slow path separation; M10.7 evidence-gated dataplane-adapter simplification; M10.8 final complexity audit; and M10.9 `FINAL_ARCHITECTURE_MAP`. Each stage now declares purpose, inputs, output, owner, completion criteria, exact successor and exact residual through the existing report lifecycle.

The Program header now distinguishes live state from historical entry: M0-M9 are complete; CPS still owns `PROGRAM_COMPLETE / NONE_RESET_PROGRAM_TERMINAL`; M10 is contract-ready but not active or executed until a separate owner-backed CPS transition. The former M0 entry point and successor remain explicitly historical. Production Authority wording now consumes the CPS-backed `CORE_PRIMARY_FOR_124_COMPATIBLE_PRODUCTION_USERS_WITH_EXACT_LEGACY_FALLBACK` state without changing it.

The final completion contract now requires `FINAL_RUNTIME_SIMPLIFICATION_PASS` and interprets `PRIMARY_SYSTEM_SURFACE_REDUCED` across the complete production software/control-plane surface rather than only the kernel/dataplane surface.

The Program-level `EXISTING_CAPABILITY_DISCOVERY_BEFORE_IMPLEMENTATION` law now requires every Reset and future implementation Mission to prove existing capability, owner, producer, consumer, state, Authority, reuse, merge, simplification and removal possibilities before new implementation. It reuses existing OMP Architecture Closed by Default, New Owner Gate, necessity and duplication controls; the required evidence is a compact logical Mission/report record, not a new artifact or framework.

The global `ARCHITECTURAL_RESPONSIBILITY_BOUNDARY_MODEL` and bounded `RESET-M10.1 — Architecture Responsibility Audit` now require every retained Program, owner, module, file, service, timer, state surface and Runtime component to prove its purpose, owner, lifecycle, inputs, outputs, real consumer, product effect, allowed/forbidden dependencies and removal condition. Exclusive Data/Control/Engineering/Legacy/Remove placement, `DELETE_TEST`, OMP-as-Engineering-only, Program lifecycle reconciliation and state-surface dispositions feed final gate `ARCHITECTURAL_RESPONSIBILITY_BOUNDARY_PASS`.

The single `SINGLE_SOURCE_OF_ARCHITECTURAL_TRUTH` law separates Runtime truth, current architecture truth and historical evidence. Runtime/Control Plane owners and CPS retain live state; the existing Canonical Reference/`SYSTEM_MAP` owners retain current architecture; Engineering Reports remain historical evidence. `FINAL_ARCHITECTURE_MAP` is the reconciled current projection and onboarding reference, not a new owner or truth source. M10.9 now performs `ARCHITECTURAL_TRUTH_RECONCILIATION` and requires `SINGLE_SOURCE_OF_ARCHITECTURAL_TRUTH_PASS`.

The single global `END_TO_END_CHANGE_COMPLETION_GATE` now prevents a working new path from being mistaken for a completed change. Material implementation and migration work must prove starting state, final state, transition, real-consumer migration, validation, old-surface disposition, safe cleanup or owner-backed exception, next-consumer consumption and final owner confirmation. `NO_UNDISPOSITIONED_ORPHANED_SURFACE_AFTER_CHANGE` covers abandoned code, imports, owners, services, timers, state, configuration and old/new duplicate paths while preserving explicit historical, recovery, fallback, external-owner and migration exceptions.

M10.9 closes the remaining architectural-comprehension gap: the existing M10 report must project the proven Runtime, Control Plane, Engineering Plane and legacy-exception boundaries into one readable final map, including runtime dependencies, final data flow, canonical ownership and `KEEP / LEGACY_EXCEPTION / REMOVED / FUTURE_REVIEW` dispositions. `FINAL_ARCHITECTURE_MAP_COMPLETE = PASS` is now mandatory. The map reuses existing evidence and owners; it is not a new Runtime artifact, truth source, audit framework or separate document class.

## Why

M0-M9 validly proved root cause, Core architecture, production authority and physical kernel routing shrink. The completion evidence nevertheless measured the strongest physical reduction primarily at kernel/dataplane level and did not yet prove the final simple product architecture `failure -> affected clients -> healthy set -> policy -> fast switch -> verify`. M10 closes that gap through explicit Data/Control/Engineering plane placement, formal channel admission, a minimal synchronous decision chain and whole-production `BEFORE / AFTER / DELTA` evidence. M10.9 additionally ensures that the final architecture, owners, dependencies, Runtime flow and exceptions are understandable without reconstructing them from historical reports. Architectural truth reconciliation closes the risk that historical Programs, Reports or competing diagrams continue to present different current architectures after Reset. The completion gate closes the separate risk that new behavior succeeds while obsolete producers, consumers, services, timers, state surfaces, configuration or ownership remain as hidden migration tails. The global discovery law closes the historical growth pattern in which a new idea produced another file, owner, state surface, process and report before existing capability reuse was proven.

## Boundaries

- M10 is part of the existing Reset Program; no Program, roadmap or parallel contract was created.
- M0-M9 order and evidence remain unchanged.
- Core architecture and routing capabilities were not expanded.
- Junos, IOS XR, FRRouting and Linux are bounded principle benchmarks only; no external implementation is copied.
- Existing owner, CPS, Runtime, Planner, Authority and truth-source boundaries remain unchanged.
- CPS/current successor was not changed; no M10 successor existed to reuse, so none was invented and M10 was not represented as active or executed.
- The architecture map is produced only during M10 execution as a section of the existing phase report; this amendment creates no additional report file for it.
- Audit/disposition RESET-M0 through RESET-M1B remain decision-only; physical cleanup is required only after implementation/migration validation and never before fallback, rollback, recovery, Authority or consumer-migration gates.
- Architecture truth remains with existing Canonical Reference/`SYSTEM_MAP` owners; document-status reconciliation is logical evidence in existing artifacts, not a registry, framework or new document ecosystem.
- Owners affected contractually: existing Routing Core/dataplane writer and verifier, channel-health/Matrix, policy, capacity, Authority, assignment-state, OMP/Polygon/Learning/Replay, deploy/truth and CPS owners. Their boundaries are classified and constrained; none receives new Runtime or Authority.

## Effects

- Runtime effects = `NONE`.
- Production effects = `NONE`.
- Routing effects = `NONE`.
- Authority effects = `NONE`.

Residual: separate owner-backed CPS reconciliation and explicit M10 execution remain required before the expanded final completion contract can pass.

Terminal: `RESET_PROGRAM_CONTRACT_RECONCILED_FOR_M10_EXECUTION`.


---

<!-- Source report: docs/reports/engineering/2026-08-13_350000_reset_m10_runtime_simplification_and_final_architecture.md -->

# RESET-M10 Runtime Simplification and Final Architecture Engineering Report

Status: `RESET_M10_COMPLETE`

This is the single decision-oriented M10 report. It reuses the M0-M9 coverage ledger, Master Audit, production promotion/retirement evidence and canonical owners; it does not restart the repository audit or create an inventory, Runtime, owner, state surface or truth source.

## RESET-M10.1 — Architecture responsibility audit

| Scoped surface | Placement | Existing owner | Real consumer / product effect | Lifecycle and final disposition |
| --- | --- | --- | --- | --- |
| nft `user_class` / `class_egress`, six fwmark rules and six route tables | `DATA_PLANE_REQUIRED` | `tools/runtime-support/v7-routing-sync` plus Linux nft/ip owners | production client packets; applies forwarding state | continuously active `KEEP`; remove only after a proven replacement |
| `v7-routing-sync` Core-primary apply, verify and fallback | `DATA_PLANE_REQUIRED` | existing routing writer | kernel forwarding and restart/recovery | primary `KEEP`; legacy builder retained only as explicit fallback |
| users/egress registries and assignments | `CONTROL_PLANE_REQUIRED` | existing Assignment owners | Core class membership and current-egress resolution | `KEEP`; volatile facts are not copied into reports |
| service Matrix, route-class fitness, quality and tunnel/runtime probes | `CONTROL_PLANE_REQUIRED` | existing Matrix/quality/runtime-health owners | target admission and Planner safety gates | `KEEP`; asynchronous observation, never forwarding authority |
| policy, capacity and delegated action-class contract | `CONTROL_PLANE_REQUIRED` | existing policy/capacity/Authority owners | bounds legal target selection and user movement | `KEEP`; fail closed when stale or absent |
| `admin_core/routing_core.py` | `CONTROL_PLANE_REQUIRED` | existing Routing Core decision owner | effect-free decision comparison and bounded Core semantics | `KEEP`; no dataplane effect by itself |
| governed Packet/lease/barrier, `v7-user-switch`, verification and rollback | `LEGACY_EXCEPTION` | existing execution/Authority/verification owners | bounded user movement and recovery when explicitly admitted | `fallback_only`; not a primary forwarding dependency; removal requires equivalent Authority, rollback and crash-recovery proof |
| `tools/v7-users-autoswitch` | `LEGACY_EXCEPTION` | existing Planner/autoswitch owner | manual/governed fallback, certification and exact action-class execution | installed but timer inactive; `NOT PRIMARY`, `NOT CORE DEPENDENCY`, retained for safety/compatibility |
| Matrix refresh, Telegram sentinel and quality collection | `CONTROL_PLANE_REQUIRED` | existing observation owners | fresh health facts and failure events | asynchronous `KEEP`; no synchronous Core apply dependency |
| OMP, CPS reconciliation, Reports, Polygon, Learning, Replay and campaigns | `ENGINEERING_PLANE_REQUIRED` | existing OMP/evidence/learning owners | engineering continuation, audit, certification and improvement | `engineering_only`; forbidden in live forwarding decisions |
| historical Programs and M0-M9 reports | `ENGINEERING_PLANE_REQUIRED` | existing document/evidence owners | explanation and prior decision evidence | `HISTORICAL_EVIDENCE`; never live Runtime or architecture truth |
| 124 per-user source rules and 124 per-user route tables | `REMOVE` | former legacy routing writer | no remaining primary consumer | already physically removed by M9; fallback can reconstruct them only during explicit recovery |
| active `v7-users-autoswitch.timer` as primary movement loop | `REMOVE` | former automation surface | no admitted primary consumer | already inactive/manual; must not be re-enabled as a parallel primary path |

`DELETE_TEST` result: deleting the Core dataplane breaks production forwarding; deleting current Assignment/Policy/Authority/Health inputs breaks lawful decisions; deleting governed fallback loses required rollback/recovery semantics. OMP/history/report surfaces can be absent from the production routing process without changing forwarding and are therefore physically excluded from the primary dependency graph. No scoped component remains unclassified and no duplicate primary routing owner remains.

## RESET-M10.2 — Industry benchmark

The benchmark is principle-only:

- Junos separates the Routing Engine from the Packet Forwarding Engine and updates forwarding without interrupting packet flow. V7 conforms through Control Plane owners preparing state and the nft/ip Data Plane applying it.
- IOS XR separates protocol/RIB functions from a hardware-abstraction layer that programs the dataplane, and favors a leaner architecture with optional components packaged by role. V7 conforms by keeping the minimal Core adapter primary and classifying engineering/governed surfaces outside it.
- FRRouting separates protocol daemons from zebra/dataplane coordination. V7 uses the same responsibility boundary, not FRR code or protocol topology.
- Linux rtnetlink/FIB contracts distinguish control messages from kernel forwarding state. V7's nft/ip writer and post-apply verification are the bounded adapter to that state.

No benchmark requires a new daemon, protocol suite, owner or abstraction. Material boundary comparison is complete: V7 has explicit decision, apply and engineering responsibilities; the retained governed executor is an owner-backed safety exception outside primary forwarding.

## RESET-M10.3 — CHANNEL_HEALTH_MODEL

`EGRESS_ADMISSION_STATE` is a logical projection of existing facts, not stored state. Its owner is the existing Matrix/quality/runtime-health composition consumed by existing policy/capacity/Planner gates.

| State | Required existing evidence | New-client admission | Existing-client use | Legal successor |
| --- | --- | --- | --- | --- |
| `UNKNOWN` | missing, stale or generation-unbound transport/service/quality/capacity evidence | forbidden | retain only under current fail-closed policy; probe required | `PROBING` |
| `PROBING` | current observation owner is collecting a generation | forbidden | no new movement; current traffic is not proof of eligibility | `HEALTHY`, `DEGRADED`, `UNUSABLE` |
| `HEALTHY` | interface/transport usable; required service fitness acceptable; quality within policy; lawful spare capacity; facts fresh | allowed inside Policy and Authority | allowed | `DEGRADED`, `UNUSABLE`, `PROBING` after invalidation |
| `DEGRADED` | transport exists but one or more service/quality/capacity criteria are marginal | forbidden unless exact policy explicitly admits degraded use | may continue only within existing safety policy while a healthy alternative is evaluated | `HEALTHY`, `UNUSABLE`, `PROBING` |
| `UNUSABLE` | hard transport failure or required service/quality/capacity gate fails | forbidden | evacuation candidate; mutation still requires Policy, Authority, rollback and verification | `RECOVERING`, `PROBING` |
| `RECOVERING` | fresh positive samples after unusable state, but hold-down/persistence not yet satisfied | forbidden | not a target; existing use only under recovery policy | `HEALTHY`, `DEGRADED`, `UNUSABLE` |

Freshness and invalidation remain defined by the producing Matrix/quality/runtime/policy owners. A source-generation change, stale timestamp, interface/route change, service regression, capacity breach, policy change or Authority expiry returns admission to `UNKNOWN`/`PROBING`. Ping or TCP alone cannot yield `HEALTHY`. This composes `TRANSPORT_HEALTH + SERVICE_HEALTH + TRAFFIC_QUALITY + CAPACITY_HEALTH`; it neither replaces nor duplicates their owners.

## RESET-M10.4 — FINAL_PRIMARY_RUNTIME_BOUNDARY

The deployed primary graph is:

```text
users/egress assignments + exact Core-promotion policy
                         |
                         v
             v7-routing-sync (210 LOC)
                         |
                         v
            nft class maps + ip rules/tables
                         |
                         v
              production client traffic
                         |
                         v
                 kernel verification
```

Admitted decision dependencies are the existing Health Receipt, Policy, Authority, Assignment, Dataplane and Verification contracts. OMP, Reports, Learning, Replay, History, campaigns and certification are absent from the continuous forwarding graph. The current Core-primary apply consumes assignments and the exact promotion contract; movement to a different assignment remains separately gated by the existing governed executor. This preserves Authority instead of inventing an unapproved class-wide switch authority.

## RESET-M10.5 — Engineering Plane extraction

Packaging classes are now explicit:

- `runtime_required`: `v7-routing-sync`, registry readers, exact Core-promotion policy, nft/ip and verify.
- `control_plane_async`: Matrix/quality/runtime observation and existing policy/capacity/Authority facts.
- `fallback_only`: `v7-users-autoswitch`, `v7-user-switch`, Packet/lease/barrier, rollback/recovery and expanded verification. They remain installed because their safety semantics have real consumers, but their services do not own primary forwarding and the autoswitch timer remains inactive/manual.
- `engineering_only`: OMP/CPS reconciliation functions in `v7_sync_lib.py`, Polygon, reports, Learning, Replay, campaign/certification and historical closure machinery.

The large files were not mechanically split: size alone does not justify a new package owner. Their production admission is narrowed by caller and service state, which physically excludes Engineering Plane code from the running primary process without duplicating it.

## RESET-M10.6 — Fast and reconciliation paths

```text
FAST FORWARDING PATH
prepared assignments/policy -> v7-routing-sync -> nft/ip -> verify

GOVERNED FAILURE ACTION
failure event -> prepared Matrix health -> Planner/policy/Authority gates
-> bounded user switch -> verify/rollback -> Core membership reconciliation

ASYNC RECONCILIATION
periodic probes -> Matrix/quality -> audit/outcome -> OMP/reports/learning
```

The first path continuously forwards without the second or third. The governed failure action remains necessary because current Authority is per bounded action, not an implicit class-wide grant. Reports, Learning, Replay, maturity, full inventory and historical reconciliation occur only after/outside apply. Thus the slow Engineering path is not a forwarding prerequisite and no Authority bypass was introduced.

## RESET-M10.7 — Dataplane adapter

Disposition: `KEEP_SIMPLIFIED_EXISTING_ADAPTER`.

The former primary chain built per-user route objects. The current chain is `Core owner -> v7-routing-sync -> nft/ip -> kernel`: one Python process, one lock domain, one atomic nft transaction, six class rules/tables and explicit verification/fallback. Replacing the 210-line adapter would add ownership and migration risk without lowering the synchronous level count. Fencing (single routing lock), idempotent replacement, atomic nft apply, exact Authority, fallback restoration and verify remain intact.

## RESET-M10.8 — Final complexity and cleanup audit

Two baselines are stated to avoid claiming that classification deletes installed fallback code:

| Metric | Pre-Core legacy primary | M10 entry | Final | Final vs legacy |
| --- | ---: | ---: | ---: | ---: |
| primary individualized kernel routing objects | 248 | 12 | 12 | -236 (-95.2%) |
| primary routing processes per reconciliation | legacy Planner/writer chain | 1 | 1 | reduced to one adapter process |
| primary routing adapter LOC | large legacy execution path (23,639-line autoswitch surface admitted) | 210 | 210 | legacy surface excluded from primary |
| active primary autoswitch timers | 1 legacy concept | 0 | 0 | -1 |
| primary pre-apply Engineering Plane hops | multiple audit/reconciliation gates | 0 | 0 | removed |
| primary pre-apply durable writes | Packet/history/closure chain | 0 | 0 | removed |
| primary lock domains | multiple governed domains | 1 routing lock | 1 | bounded |
| primary critical-path subprocess layers | Planner -> writer -> scripts -> kernel | adapter -> nft/ip | adapter -> nft/ip | reduced |
| Reset-added Runtime owners/processes/timers/state surfaces | 0 | 0 | 0 | 0 |

M10 entry-to-final LOC is deliberately `0`: the already deployed minimal adapter was correct, and rewriting it for a numerical delta would violate reuse-first and safety. Whole-production reduction is the combination of M9 physical deletion and M10 proof that 23,639-line autoswitch, 25,380-line synchronization/engineering library, OMP/report/history/campaign surfaces and inactive timers are `LEGACY_SURFACE_NOT_ADMITTED_TO_FINAL_RUNTIME`. They remain installed only where an exact manual/governed safety, deploy/truth or engineering consumer exists.

Cleanup dispositions:

- `STILL_REQUIRED`: compact Core dataplane, assignments, health observation, policy/capacity/Authority, verify.
- `LEGACY_EXCEPTION_REQUIRED`: governed per-user execution, rollback, fallback and recovery; owner-backed removal condition is equivalent bounded Authority plus production rollback/crash proof.
- `ARCHIVE`: historical Programs/reports remain evidence and are not loaded by Runtime.
- `DELETE`: legacy primary kernel objects and any active parallel autoswitch timer; both are absent from final primary state.

`NEW_ARCHITECTURE_COMPLETE = PASS`; `OLD_ARCHITECTURE_CLOSED = PASS`. No superseded import, service, timer, state writer, config entry or old/new primary pair remains undispositioned. The fallback is explicit, not an orphan.

## RESET-M10.9 — FINAL_ARCHITECTURE_MAP

### Runtime and data flow

```text
CONTROL PLANE                                         DATA PLANE
Matrix/quality/runtime health -> EGRESS_ADMISSION_STATE
Assignments + Policy + Capacity + Authority
                    |                                      |
                    +--> bounded decision / current class -+
                                                           v
CLIENT TRAFFIC -> nft user_class -> class route -> interface -> VERIFY
                                                           |
                                                           v
                                                ASYNC OUTCOME/EVIDENCE
                                                           |
                                                           v
ENGINEERING PLANE: OMP / Reports / Polygon / Learning / Replay
```

The forbidden inverse dependency `failure -> reports/analysis -> routing` does not exist in primary forwarding.

### Ownership matrix

| Responsibility | Canonical existing owner | Input -> output | Lifecycle |
| --- | --- | --- | --- |
| channel/service observation | Matrix/quality/runtime-health owners | probes -> fresh facts | Control Plane async |
| admission projection | same existing health owners composed with policy/capacity | facts -> `EGRESS_ADMISSION_STATE` | logical, not stored |
| assignments | existing Assignment owners | user/current egress -> class membership | Control Plane truth |
| routing decision semantics | existing Routing Core / governed Planner owners | admitted facts -> bounded decision | Control Plane |
| Authority | existing policy/operator-execution owners | contract -> legal effect envelope | Control Plane, fail closed |
| route apply | `v7-routing-sync` / Linux kernel | class map -> forwarding state | Data Plane primary |
| verification | existing routing/kernel and governed verification owners | installed state/outcome -> PASS/STOP | Runtime/Data Plane |
| engineering improvement | OMP and existing evidence/learning owners | async outcomes -> change decision | Engineering Plane only |

### Legacy exceptions and delete/revisit list

| Item | Status | Reason / removal condition |
| --- | --- | --- |
| `legacy_sync` builder | `LEGACY_EXCEPTION` | exact Core fallback; remove only after another proven recovery owner exists |
| `v7-users-autoswitch` + governed transaction | `LEGACY_EXCEPTION` | Authority/rollback safety; `NOT PRIMARY`, `NOT CORE DEPENDENCY`, temporary compatibility until equivalent production proof |
| inactive autoswitch service/timer files | `FUTURE_REVIEW` | manual recovery compatibility; timer must remain inactive |
| OMP/reports/history/campaigns | `KEEP` Engineering Plane | real engineering consumers; never Runtime dependencies |
| 248 legacy individualized kernel objects | `REMOVED` | M9 production deletion proof |
| Core class dataplane | `KEEP` | current production consumer and fallback evidence |

### Architectural truth reconciliation

- `docs/programs/V7_CURRENT_PROGRAM_STATE.md`: `CURRENT_ARCHITECTURE_OWNER` only for volatile Runtime/program state.
- `docs/reference/V7_CANONICAL_REFERENCE.md` and `docs/reference/SYSTEM_MAP.md`: `CURRENT_ARCHITECTURE_OWNER` for durable architecture and topology.
- this report and all M0-M9 Engineering Reports: `HISTORICAL_EVIDENCE`.
- completed/superseded Program sections and older diagrams: `OBSOLETE_REFERENCE` when they claim current execution; their evidence remains historical.
- `FINAL_ARCHITECTURE_MAP` is this reconciled projection consumed into the Canonical Reference/SYSTEM_MAP; it is not Runtime state, CPS, Authority or a new owner.

No conflicting current architecture owner was found after the canonical updates. Future architecture changes update the existing Canonical Reference/SYSTEM_MAP before creating another artifact.

## Stage closure and final gates

| Stage | Consumed output | Result / successor |
| --- | --- | --- |
| M10.1 | exclusive placement ledger | PASS -> M10.2 |
| M10.2 | supported boundary benchmark | PASS -> M10.3 |
| M10.3 | owner-backed admission lifecycle | PASS -> M10.4 |
| M10.4 | minimum dependency graph | PASS -> M10.5 |
| M10.5 | package/caller isolation | PASS -> M10.6 |
| M10.6 | fast/governed/async path split | PASS -> M10.7 |
| M10.7 | retained minimal adapter with safety proof | PASS -> M10.8 |
| M10.8 | before/entry/final metrics and cleanup | PASS -> M10.9 |
| M10.9 | canonical final map and document reconciliation | PASS -> completion evaluation |

- `ARCHITECTURAL_RESPONSIBILITY_BOUNDARY_PASS = PASS`
- `PRIMARY_SYSTEM_SURFACE_REDUCED = PASS`
- `FINAL_RUNTIME_SIMPLIFICATION_PASS = PASS`
- `FINAL_ARCHITECTURE_MAP_COMPLETE = PASS`
- `END_TO_END_CHANGE_COMPLETION_PASS = PASS`
- `SINGLE_SOURCE_OF_ARCHITECTURAL_TRUTH_PASS = PASS`
- `OLD_FAILURE_CAUSES_NOT_REINTRODUCED = PASS`

Self-review found no Authority expansion, no new Runtime/owner/state, no synchronous Engineering dependency, no hidden duplicate primary writer and no orphaned migration tail. Deep audit evidence remains linked rather than copied. The only retained large surfaces have exact governed fallback, deploy/truth or Engineering consumers and explicit removal conditions.

Runtime effects: `NONE_NEW; EXISTING_CORE_PRIMARY_BOUNDARY_CONFIRMED`.

Production effects: `NONE_NEW; EXISTING_CORE_PRIMARY_FOR_124_USERS_AND_M9_PHYSICAL_SHRINK_PRESERVED`.

Authority effects: `NONE; EXACT_EXISTING_PROMOTION_AND_BOUNDED_ACTION_CLASS_CONTRACTS_PRESERVED`.

Residual: `NONE_FOR_RESET_M10`.

Successor: `FINAL_RESET_PROGRAM_COMPLETION_RECONCILIATION`.

Terminal: `RESET_M10_POST_RESET_SYSTEM_SHRINK_AND_RUNTIME_SIMPLIFICATION_PASS`.


---

<!-- Source report: docs/reports/engineering/2026-08-13_370000_rt2_post_reset_operating_profile_contract.md -->

# RT2 Post-Reset Operating Profile Contract Engineering Report

Status: `RT2_POST_RESET_OPERATING_PROFILE_CONTRACT_READY_NOT_ADMITTED`

## Discovery and decision

The requested post-Reset maturity scope already has one canonical Program owner: OMP Section 28 `Runtime Capability Maturation Program / RT2`. CPS maps runtime maturation to existing `CAP-U12`; SYSTEM_MAP assigns measurement, readiness, execution coordination, concurrency, optimization, time and scale responsibilities to RT2 and existing owners.

Therefore `V7_POST_RESET_RUNTIME_MATURITY_AND_OPTIMIZATION_PROGRAM_V1` was not created. It would duplicate RT2, OMP scheduling and capability ownership. The existing RT2 contract was minimally extended with one `Post-Reset Operating Profile`.

## Purpose and dependencies

Reset established and production-proved the architecture. This profile does not revise it; it gives existing RT2 owners a bounded contract for ordinary traffic-path confirmation, evidence-gated legacy reduction, production-package classification, latency/recovery measurement, existing channel-admission hardening, 10k+/50+ scale revalidation and permanent drift prevention.

It consumes:

- `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_COMPLETE`;
- `FINAL_ARCHITECTURE_MAP` through Canonical Reference/SYSTEM_MAP;
- `POST_RESET_REALITY_CHECK_COMPLETE`;
- M6/M7/M8/M9 production, latency, scale, Core-primary, fallback and shrink evidence;
- RT2-S1/S2/S6, Runtime Model, Product Scale, Necessity and Architecture Closed by Default owners.

## Ownership and lifecycle

- Program owner: existing OMP `Runtime Capability Maturation Program / RT2`.
- Volatile admission/frontier owner: existing CPS; unchanged.
- Runtime, routing, health, Assignment, Policy, Capacity, Authority, verification, package and production-truth owners: unchanged.
- Contract status: `CONTRACT_READY_NOT_ADMITTED`.
- Predecessor: completed Reset terminal.
- Development successor edge: `OMP admission/reconciliation -> RT2_POST_RESET_OPERATING_PROFILE`.
- Final successor after evidence-backed execution: `STEADY_STATE_OPERATIONS`.

This is a dormant contract edge, not the current CPS action. It does not preempt protected WIP, natural-evidence waits or dependency ordering.

## Completion contract

The profile completes only when all existing-owner terminals pass:

1. `REAL_TRAFFIC_PATH_CONFIRMED`.
2. `LEGACY_SURFACE_REDUCTION_PASS`.
3. `RUNTIME_PACKAGE_MINIMAL_PASS`.
4. `ROUTING_LATENCY_BASELINE_CONFIRMED`.
5. `CHANNEL_ADMISSION_MODEL_STABLE`.
6. `SCALE_BOUNDARY_CONFIRMED`.
7. `ARCHITECTURE_DRIFT_PROTECTION_ACTIVE`.

Real caller/consumer, production behavior, safety, rollback/recovery, deployment, Authority and residual evidence remain mandatory where applicable. Existing proof is reused unless an exact invalidator requires targeted recheck.

## Boundaries and effects

- No new Program, roadmap, owner, CPS, Runtime, Core, Planner, Health system, audit framework, queue, store or truth source.
- No Reset expansion or architecture modification.
- No Program execution, traffic generation, legacy deletion, refactor, deploy, user movement or Policy/Authority change.
- Runtime effects = `NONE`.
- Production effects = `NONE`.
- Authority effects = `NONE`.

Terminal: `RT2_POST_RESET_OPERATING_PROFILE_CONTRACT_READY_NOT_ADMITTED`.


---

<!-- Source report: docs/reports/engineering/2026-08-13_380000_rt2_deep_simplification_and_automatic_internet_operation_contract.md -->

# RT2 Deep Simplification and Automatic Internet Operation Contract

Status: `RT2_DEEP_SIMPLIFICATION_AUTOMATIC_INTERNET_CONTRACT_READY_NOT_ADMITTED`

## What changed

OMP V4.78 Section 28.9 was extended in place. No `V7_POST_RESET_RUNTIME_MATURITY_AND_OPTIMIZATION_PROGRAM_V1`, `RT2-PR2A`, new stage, roadmap, owner or execution path was created. Existing `RT2-S1 -> RT2-S6` are capability inputs; `RT2-PR1 -> RT2-PR7` remain the only post-Reset execution sequence.

Existing M10 responsibility/benchmark evidence, RT2 production reality, legacy/package/performance/health/scale/drift cells, OMP Production Promotion Matrix, Product Contract, Runtime Model, Work Placement, safety, Authority, rollback, deployment and canonical owners are reused.

The exact missing obligations added are:

- responsibility-level `file/function -> caller -> consumer -> state -> effect -> terminal outcome` proof;
- a closed observation, decision, apply, kernel/traffic verification, stabilization, recovery/rollback, cleanup lifecycle;
- real user-connectivity outcome rather than route/report/test presence alone;
- bounded failure matrix and symmetric failover/recovery closure;
- existing-gate production promotion followed by `NO_DANGLING_LEGACY_RESIDUE_CHECK`;
- explicit legacy-exception removal conditions;
- before/after physical measurement without treating exclusion as deletion;
- net operational-complexity and existing-owner routing security/isolation gates;
- final `AUTOMATIC_INTERNET_OPERATION_READY` acceptance.

Final reconciliation also binds the exact OMP/CPS admission trigger and first PR1 frontier, requires a PR1 pre-mutation baseline before PR2/PR3 changes, assigns every completion gate to a producer and successor, separates controlled-fault, real-production and natural-event evidence, and distinguishes engineering-ready, Authority-ready and production-enabled automatic operation. The stale Canonical Reference statement that production remained legacy was corrected to the M8-M10/Core-primary terminal reality.

The final scope clarification makes `ALL_V7_ENGINE_COMPONENTS` mandatory rather than treating autoswitch and legacy files as the audit boundary. PR2 must reconcile file/function chains into a system-wide upstream/downstream, synchronous/asynchronous, shared-state, process/privilege and failure-propagation graph. Decision-relevant conclusions and accepted final relationships must survive through existing report/generated-evidence/canonical owners, while raw dumps remain temporary. Existing Research/Fit Analysis must compare mature routing-system responsibility, dependency, state, API, restart and failure-containment principles with V7; reference-system difference alone cannot justify code change.

Every future implementation report must now contain one compact `PROGRAMMATIC_CHANGE_DELTA`: program-source LOC separately from documents, tests and generated/data; file and function/class/entrypoint changes; dependency-edge changes; state writer/reader/surface changes; runtime package/unit/process changes; routing-object/writer/planner changes; and physical legacy removal separately from logical/runtime exclusion. Report-only work records `PROGRAMMATIC_CODE_EFFECT = NONE`; unmeasurable aggregate relationship counts remain `NOT_PROVEN` with exact edge evidence rather than invented totals.

PR2 now has an explicit repository-to-function audit hierarchy, responsibility-conflict classifications, function-level decision fields and a logical physical-simplification disposition ledger. Cloudflare-style practices are an optional health/failover reference through existing Research/Fit Analysis only. No separate PR2A, physical-plan document or second shrink-report class was created.

## PROGRAMMATIC_CHANGE_DELTA

Comparison boundary: working-tree contract patch against current `HEAD`.

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| Program source LOC | 0 | 0 | 0 |
| Documentation/report LOC changed by this contract patch | 0 | 323 added / 5 deleted | +318 net |
| Test LOC | 0 | 0 | 0 |
| Program files added / modified / deleted / moved | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 | 0 |
| Documentation files added / modified / deleted / moved | 0 / 0 / 0 / 0 | 1 / 2 / 0 / 0 | +1 added, +2 modified |
| Program functions/classes/entrypoints changed | 0 | 0 | 0 |
| Runtime dependency/state/unit/routing edges changed | 0 | 0 | 0 |

Contract relationships added: exact admission, gate-producer/consumer, evidence-class, whole-engine graph, preservation, reference-comparison and report-delta obligations inside OMP only. These are Engineering Plane contract edges, not Runtime dependency edges.

`PROGRAMMATIC_CODE_EFFECT = NONE`. Physical source deletion, Runtime exclusion, routing-object mutation and legacy removal = `NONE`.

## Risk closed

The contract prevents a structurally cleaner V7 from being declared mature while user traffic, recovery, partial transitions, stale state, hidden writers or legacy residue remain unproven. It also prevents the simplification effort from creating a new audit/report subsystem or using vendor similarity and LOC reduction as success criteria.

## Ownership and boundaries

- Program/orchestration owner: existing OMP `Runtime Capability Maturation Program / RT2`.
- Current-state owner: existing CPS; unchanged.
- Architecture projection: existing `FINAL_ARCHITECTURE_MAP`, Canonical Reference and SYSTEM_MAP; unchanged.
- Runtime, routing, Product Contract, health, measurement, safety, Authority, rollback, deployment and component ownership: existing owners only.
- Admission remains subject to ordinary OMP/CPS dependency reconciliation. The live CPS frontier was not changed.

Completion additionally requires real relationship, closed-lifecycle, user-connectivity, SLO, failure/recovery, residue, complexity, security/isolation and final architecture/runtime alignment gates enumerated in OMP Section 28.9. Any required `NOT_PROVEN` result remains open.

Runtime effects = `NONE`

Production effects = `NONE`

Authority effects = `NONE`


---

<!-- Source report: docs/reports/engineering/2026-08-13_430000_v7_responsibility_realignment_and_simplification_plan.md -->

# V7 Responsibility Realignment and Simplification Plan

**Status:** `RT2_PR2C_RESPONSIBILITY_REALIGNMENT_AND_SIMPLIFICATION_PLAN_PASS_READ_ONLY`
**Scope:** `RT2-PR2C` in `OPERATIONAL_MATURITY_PROGRAM`; plan only.
**Inputs:** PR1 production-reality baseline, PR2 surface audit, PR2A responsibility graph, PR2B alignment audit, `FINAL_ARCHITECTURE_MAP`.
**Owner boundary:** existing component, safety, Authority, Work Placement, Runtime Model, CPS/OMP and canonical architecture owners.
**Runtime effects:** `NONE`
**Production effects:** `NONE`
**Authority effects:** `NONE`

## Decision

The evidence supports a responsibility-realignment plan before any `RT2-PR3 RUNTIME_PACKAGE_SIMPLIFICATION`. It does not authorize a mutation, a new owner, a new Runtime component, a new truth source, or a new document framework.

The governing model remains:

```text
Management Plane: Admin UI/API -> guarded request and read model only
Control Plane: Matrix/Sentinel/health -> policy -> bounded movement/recovery decision
Data Plane: routing-sync -> nft/ip apply -> verification
Engineering Plane: OMP/Polygon/reports/certification -> asynchronous evidence only
```

Existing owners retain their boundaries. A target responsibility below means an existing boundary in which an already-proven responsibility belongs; it never creates an owner.

## Logical simplification matrix

| Component / surface | Current responsibility and material gap | Target responsibility / existing boundary | Plan classification | Migration, validation and old-path closure condition |
| --- | --- | --- | --- | --- |
| `v7-users-autoswitch` | Bounded fallback, rollback, governed execution and some diagnostics/certification are co-located. Removing or moving its safety path would be unsafe. | Preserve movement, rollback, recovery and governed execution under existing safety/Authority boundaries. Diagnostics, certification helpers and engineering evidence may move only to existing Engineering Plane owners. | `KEEP` safety path; `SHRINK`/`MOVE` candidate for proven non-Runtime helpers. | First prove every helper's caller, consumer and state/effect. Then admit a separate existing OMP/CPS mutation, preserve rollback and test the real consumer. Retire old helpers only after imports, CLI/subprocess callers, units, deploy/install configuration, state, locks/leases/barriers, recovery, dashboards, tests and documents have no live dependency. |
| `v7_sync_lib.py` | CPS continuation, OMP/Polygon, deploy and truth-facing interfaces are co-located; file size alone is not a defect. | Keep authoritative interfaces with their existing CPS/OMP/Polygon/deploy/truth boundaries; reduce mixed presentation or diagnostic responsibility only where evidence proves a safe destination. | `SHRINK`/`MOVE` candidate; no new shared library. | Map function -> caller -> consumer -> durable state -> side effect before a separately admitted migration. Require compatibility validation and old import/path closure before any deletion. |
| Admin API / UI dispatch / read model / guarded action | Presentation, API dispatch, read projection and guarded action can be adjacent, creating a risk that management presentation reaches routing effects directly. | Existing Management Plane UI/API boundary for presentation and read model; existing guarded action and Authority/safety boundary for mutations. | `SHRINK`/`MOVE` candidate; guarded action remains `KEEP`. | Separate only after route/UI/consumer and Authority-fencing proof. Preserve backward-compatible callers during migration. Remove old embedded presentation/action tails only after live consumer conversion and residue proof. |
| Operator execution / governed action path | Safety boundary, command execution and recovery coupling are necessary for bounded operator action. | Existing safety, Authority, movement-protection and recovery owners. | `KEEP`; later helper extraction only if independently proven. | No simplification may weaken Authority checks, rollback or recovery. Any future helper move requires affected-owner tests, safe deploy and production verification. |
| Active path guard | Recovery invocation and path protection remain coupled to an existing runtime safety boundary; its exact present consumer must be proven before narrowing it. | Existing recovery and safety boundary; no Engineering Plane substitution. | `LEGACY_EXCEPTION` pending exact failure-matrix and Authority-state proof. | Retain unchanged until PR3-or-later admitted work proves real callers/consumers, failure behavior and replacement closure. No removal merely because it is historical-looking. |
| Direct autosync | Direct-path synchronization/control responsibility is distinct from Routing Core and may be runtime-required. | Existing Direct/control-plane boundary and Runtime package owner. | `KEEP` pending package-truth reconciliation. | Establish deployed consumer, startup dependency, imports and real product effect. Only then may a later admission classify a helper as `SHRINK` or `engineering_only`; no Core expansion. |
| Health Matrix / Sentinel | Health production, fencing and consumers must remain explicit; a health surface cannot become a synchronous Engineering Plane dependency. | Existing Matrix/Sentinel, health, capacity, policy and admission owners in Control Plane. | `KEEP`; `SHRINK_REVIEW` for duplicate projections only. | Identify each writer, reader, freshness/fencing rule and routing consumer. A duplicate projection can be removed only after retained owner mapping, recovery behavior and residue proof pass. |

## Required physical-plan evidence for every future mutation

The matrix above is the single logical plan output. It must be updated through the existing canonical Program/report path rather than copied into new manifests, generators or maps. A later owner-backed change must record:

1. `BEFORE -> AFTER -> DELTA` for files, LOC, imports, callers, consumers, state surfaces, services/timers/processes and dependency edges.
2. The exact old lifecycle end and new lifecycle beginning, joined by consumer, migration and cleanup proof.
3. `NO_DANGLING_LEGACY_RESIDUE_PASS` over static imports, dynamic imports, CLI/subprocess callers, systemd/cron units, deploy/install configuration, state/locks/leases/barriers, rollback/recovery, nft/ip paths, dashboards, tests and documents.
4. The actual real consumer and, where applicable, affected-owner tests, safe deployment, CPS/canonical reconciliation and production verification.

`runtime_excluded`, `engineering_only` and `fallback_only` are logical classifications; none may be reported as physical removal until the physical closure evidence is complete.

## Authorization and successor

```text
PR2C PLAN
  -> existing OMP/CPS admission with exact owner-backed disposition
  -> separately authorized mutation and validation
  -> old-path closure and NO_DANGLING_LEGACY_RESIDUE_PASS
  -> RT2-PR3 RUNTIME_PACKAGE_SIMPLIFICATION
```

`NO_CHANGE_AUTHORIZATION_FROM_PLAN` applies. This report makes no code, Runtime, CPS, production, Authority, deployment or migration-state change. The next contractual successor is `RT2-PR3 RUNTIME_PACKAGE_SIMPLIFICATION`, but only after the existing OMP/CPS admission and exact owner-backed mutation disposition required by the Program.

## Why this closes the present risk

PR2A and PR2B identified mixed responsibilities and valid retained safety paths. Planning their separation before package simplification prevents a cosmetic LOC reduction, a new parallel subsystem, or accidental removal of fallback/recovery behavior. It preserves the evidence depth of the audit while making each future change prove its consumer, owner boundary, transition and residue closure.

## Programmatic delta

| Metric | Value |
| --- | ---: |
| Production source files changed | 0 |
| Production source LOC added/removed | 0 / 0 |
| Runtime services, timers or processes changed | 0 |
| Runtime dependency edges changed | 0 |
| Files deleted, moved or archived | 0 / 0 / 0 |
| Program-contract rows added | 1 (`RT2-PR2C`) |
| Engineering reports added | 1 (this logical plan) |


---

<!-- Source report: docs/reports/engineering/2026-08-13_440000_v7_responsibility_realignment_and_system_simplification_program_contract.md -->

# V7 Responsibility Realignment and System Simplification Program Contract

**Status:** `CONTRACT_READY_NOT_ADMITTED`
**Canonical Program:** `V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1`
**Canonical owner:** existing OMP, with existing component, safety, Authority, CPS, Runtime Model, Work Placement, deploy/package and canonical architecture owners.
**Predecessor evidence:** Reset terminal; `FINAL_ARCHITECTURE_MAP`; accepted RT2 PR1/PR2/PR2A/PR2B/PR2C evidence.
**Runtime effects:** `NONE`
**Production effects:** `NONE`
**Authority effects:** `NONE`

## Why this Program exists

Reset established the Core-primary architecture. RT2 and its PR2 audit family established production-reality, responsibility, dependency and commercial-routing alignment evidence. The resulting gap is no longer discovery: accepted evidence identifies cross-plane mixed responsibilities, historical compatibility surfaces and transitions that require physical closure without weakening Product Contract, recovery or safety.

The new official OMP Program owns that transition discipline. It does not change either completed Reset or the RT2 Post-Reset Operating Profile. RT2 retains its package, measurement and maturity criteria; the new Program consumes its accepted evidence and controls only separately admitted cross-plane realignment and old-path closure.

## Contract shape

The Program has nine ordered phases:

1. Responsibility realignment map.
2. Engineering Plane separation.
3. Control Plane simplification.
4. Recovery boundary simplification.
5. Admin and Management separation.
6. Runtime package minimization using existing RT2/package owners.
7. Individually admitted physical simplification execution.
8. Validation and residue cleanup.
9. Physical shrink closure.

The target boundary is unchanged: Engineering Plane stays asynchronous; Control Plane owns state and decision; Data Plane applies and verifies. No new Core, engine, Planner, Health system, owner, Runtime component, CPS, truth source, registry, queue, roadmap or audit framework is introduced.

## Safety and ownership rules

- A plan, matrix, report or vendor comparison grants no mutation authority.
- Every physical change requires an existing OMP/CPS admission, exact affected owner, validation, safe deploy and real-consumer proof where applicable.
- `CURRENT -> TARGET -> TRANSITION -> NEW CONSUMER -> VALIDATION -> OLD PATH CLOSED` is mandatory.
- `NO_DANGLING_LEGACY_RESIDUE_PASS` covers static/dynamic callers, CLI/subprocess paths, units/timers, deploy/configuration, state/locks/leases/barriers, rollback/recovery, nft/ip paths, dashboards, tests and documentation tails.
- The named matrix, implementation plan, tracker and shrink report are logical projections inside phase/closure reports or linked existing/generated evidence; they are not a new report framework.

## Completion criteria

Completion requires all nine phases to be consumed or legally residualized with an exact existing owner and successor; one existing owner/lifecycle/primary consumer for every changed responsibility; closed duplicate paths or bounded Legacy Exceptions; reconciled Runtime dependency truth; mechanically evidenced physical shrink separate from logical exclusion; preserved Product Contract, safety, Authority, rollback and recovery; and CPS/OMP/canonical agreement.

## Admission state and successor

The Program is not active and does not alter the CPS frontier. It may start only after existing OMP/CPS admission identifies `RS1 RESPONSIBILITY_REALIGNMENT_MAP` as the smallest legal frontier without displacing protected work. Its first execution is read-only. `RS7` is prohibited until an individual owner-backed mutation is separately admitted.

## Programmatic delta

| Metric | Value |
| --- | ---: |
| Production source files changed | 0 |
| Production source LOC added/removed | 0 / 0 |
| Runtime services, timers or processes changed | 0 |
| Runtime dependency/state/routing edges changed | 0 |
| Files deleted, moved or archived | 0 / 0 / 0 |
| OMP Program contracts added | 1 |
| Engineering reports added | 1 (this contract report) |


---

<!-- Source report: docs/reports/engineering/2026-08-13_450000_v7_rs_program_execution_hardening_contract.md -->

# V7 RS Program Execution Hardening Contract

**Status:** `CONTRACT_READY_NOT_ADMITTED`
**Program:** `V7_RESPONSIBILITY_REALIGNMENT_AND_SYSTEM_SIMPLIFICATION_PROGRAM_V1`
**Scope:** OMP §47 contract hardening only; no Program admission or physical execution.
**Runtime effects:** `NONE`
**Production effects:** `NONE`
**Authority effects:** `NONE`

## Closed execution gaps

| Gap | Contractual closure |
| --- | --- |
| incomparable shrink claims | `RS0` requires one immutable source fingerprint/scope/method and a separately timestamped Runtime observation before any mutation. |
| repeated broad archaeology | `RS1A` reuses PR2A/PR2B/PR2C and permits only targeted rechecks for changed, invalidated or unresolved evidence. |
| file-only placement | `RS1B` requires a responsibility/dependency projection with existing owner, producer, consumer, state, effect, layer and migration path. |
| target exists but consumers remain old | `RS7A` follows target implementation and proves consumer migration/behavior before old-edge disconnection. |
| removal before closure | `RS8` prohibits deletion until caller, dynamic invocation, unit/config/state/recovery/test/document tails are closed or owner-backed. |
| report-only complexity claim | every admitted RS7 item records classified `BEFORE -> AFTER -> DELTA`; logical exclusion is never physical reduction. |

## New mandatory gates

`IMMUTABLE_BEFORE_BASELINE_CAPTURED`; `CODE_ARCHAEOLOGY_COMPLETE`; `RESPONSIBILITY_GRAPH_COMPLETE`; `TARGET_OWNERSHIP_MODEL_COMPLETE`; `CONSUMER_MIGRATION_COMPLETE`; `FINAL_COMPLEXITY_DELTA_COMPLETE`; and strengthened `NO_DANGLING_LEGACY_RESIDUE_PASS` are now required before terminal closure.

Existing identifiers are preserved. The dependency order is:

```text
RS0 -> RS1 -> RS1A -> RS1B -> RS2 -> RS3 -> RS4 -> RS5 -> RS6
    -> RS7 target implementation -> RS7A consumer cutover
    -> RS8 old-path closure -> RS9 final validation
```

`RS7` does not delete an old path. `RS7A` migrates consumers after the target exists; `RS8` alone may close the old path after residue proof.

## Boundary preservation

The hardening does not create a metric store, graph engine, audit framework, owner, CPS, Runtime component or parallel report system. Baselines, matrices, trackers, graphs and final closure are logical evidence projections under existing owners. RT2 retains its own maturity/measurement/package criteria; CPS remains the sole volatile owner and has not admitted this Program.

## Programmatic delta

| Metric | Value |
| --- | ---: |
| Production source files changed | 0 |
| Production source LOC added/removed | 0 / 0 |
| Runtime services, timers or processes changed | 0 |
| Runtime dependency/state/routing edges changed | 0 |
| Files deleted, moved or archived | 0 / 0 / 0 |
| Program contract subphases added | 4 (`RS0`, `RS1A`, `RS1B`, `RS7A`) |
| Engineering reports added | 1 (this report) |
