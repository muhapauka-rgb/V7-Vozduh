# V7 Operational Maturity Program

Status: `ACTIVE`
Program: `V7.OMP.FINAL.PRODUCTION_PROGRAM`
Created: 2026-06-25
Version: `4.62`
V2.1 baseline reference commit: `7687d506a4a14bf6aed39aa15efd00462b96d980`
Runtime architecture certification commit: `39c46ed379ff4a2ccadb84a49a0dd9dcd2de579b`

This document is the permanent production operating program for V7. It replaces roadmap-driven development, phase-first development, free-form implementation ideas, and architecture-first continuation with continuous production maturity evolution.

Roadmaps, reports, ADRs, and reference files remain evidence and context. The complete autonomy roadmap lives inside this OMP. No additional roadmap document is required to drive V7 from current `TIER_1` governed autonomy to full production autonomy.

This program defines how V7 resolves the current system state, highest bottleneck, highest leverage action, normalized authority class, reality limit, next best action, authority evolution recommendation, and whether Codex may continue automatically. The authoritative volatile values produced by that resolution live in `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

Latest admitted continuation report: `docs/reports/engineering/2026-07-25_112500_l7_repair_generation_v6_preflight_and_admission.md` (`R1_V6_REPAIR_GENERATION_PREFLIGHT_READY_AND_ONE_USE_TRANSACTION_ADMITTED`).
Latest consumed report: `docs/reports/engineering/2026-08-03_233500_final_performance_closure_before_stage48.md` (`STAGE_48_OPTIMIZED_RUNTIME_READY`).
Previous admitted continuation report: `docs/reports/engineering/2026-07-25_112500_l7_repair_generation_v6_preflight_and_admission.md` (`R1_V6_REPAIR_GENERATION_PREFLIGHT_READY_AND_ONE_USE_TRANSACTION_ADMITTED`).
Previous consumed report: `docs/reports/engineering/2026-08-02_141500_stage_25_exact_receipt_and_fastest_safe_path.md` (`AVAILABILITY_FIRST_STAGE_25_PRODUCTION_PROVEN`).
Authoritative transition input: `docs/reports/engineering/2026-07-11_225321_operation_scoped_binding_atomic_snapshot_closure_v3.md` (`V7_OMP_BINDING_ATOMIC_SNAPSHOT_AND_MISSION_IDENTITY_GUARD_V3`; `MISSION_IDENTITY_GUARD_AND_BINDING_STABILITY_CERTIFIED`).
Live continuation and the current bounded delegated policy state are owned only by CPS section 0 and its Authoritative Unfinished Capability Closure Registry.

V4.17 adds the OMP Self-Continuation Contract: a transaction terminal closes only its transaction, while the existing Codex OMP execution consumer must continue the same Engineering Control Loop until a proven program terminal requires external input. It creates no daemon, queue, scheduler, Runtime, Planner, owner, or parallel execution path.

V4.18 adds Dependency-Aware Continuation and Completion Order Protection inside the same OMP/CPS consumer. A capability-local wait is preserved with its owner, evidence, fingerprint and reentry condition, but becomes a program terminal only when no independent READY capability exists. Completion requires all declared dependencies plus Engineering Intent closure, verified consumer consumption, evidence consumption and CPS propagation. No scheduler, queue, graph engine, Planner, Runtime, lifecycle or owner is created.

V4.19 connects existing owner-backed Engineering Polygon Scenario sources to BDP minimal Discovery Economy and the existing L6 continuous lane. The bounded adapter evaluates current validator, dependency, replay, producer/consumer, STOP_SAFE, recovery, coverage, WIP and production-evidence surfaces; materializes only active Engineering Plane failures; deterministically selects one scenario; and routes it through the existing BDP Reality Gate and OMP admission. Historical artifacts and production-only evidence never become scenarios by themselves. This adds no Scenario Engine, queue, scheduler, owner, Runtime, Planner, lifecycle, truth source or backlog.

V4.20 connects bounded proactive verification inputs from existing test, replay, STOP_SAFE, rollback, recovery, truth, dependency and producer/consumer owners to the same Engineering Polygon Scenario Supply. A proactive input is execution metadata, not a Candidate or production evidence. PASS records current contract coverage without a Scenario. Only a current reproducible mismatch may become a Scenario and continue through BDP Reality Gate and OMP admission. Execution is serial, deterministic, no-mutation and budget-bounded; it cannot grant authority, move users, apply packets, write restore barriers or earn Production Maturity. This adds no test engine, replay engine, scenario engine, queue, scheduler, owner, Runtime, Planner, lifecycle, truth source or backlog.

V4.21 replaces finite seed exhaustion with deterministic Engineering Polygon corpus discovery and fallback continuation inside the same existing owners. The bounded consumer projects safe executable verification obligations from the current mapped owner corpus, fingerprints source, fixture, contract, owner implementation and dependencies, revalidates stale coverage, and continues serially until failure, budget boundary or proven full-current-corpus exhaustion. Budget exhaustion preserves the exact next input and is never a `REAL_WORLD_LIMIT`. This adds no corpus registry, test engine, queue, scheduler, owner, Runtime, Planner, lifecycle, truth source or backlog.

V4.22 adds capability-closure reconciliation inside existing OMP Capability Management. `IMPLEMENTATION_COMPLETE` and a global `REAL_WORLD_LIMIT` are legal only after every current unfinished capability criterion is owner-classified and no safe executable engineering criterion remains. Actionable backlog completion proves implementation-scope closure only; it never proves output consumption, behavior change, intent closure, capability certification or production maturity. Capability-local real-world, authority and dependency waits cannot stop independent READY engineering work. CPS remains the sole volatile capability-state owner.

V4.23 adds program execution and consumption reconciliation inside existing OMP continuation. A canonical program is complete only after every mandatory stage produced a valid output, independent acceptance and lock requirements passed, the required consumer confirmed consumption, the next state/output was produced, and terminal evidence exists. Document labels, organized/ready status, backlog completion, isolated tests, reports or partial mechanism reuse never prove program completion. A global `REAL_WORLD_LIMIT` is illegal while an independent safe program stage is READY, in progress, awaiting acceptance or awaiting consumer confirmation. CPS remains the sole volatile program-frontier owner.

V4.24 adds Functional Footprint and Real Consumer Activation enforcement inside the same OMP continuation owner. Implemented, tested, deployed, documented or manually callable code is not automation. `COMPLETE_CONSUMED` requires a real non-test trigger, an active owner-correct entrypoint, actual invocation, consumer behavior change and a next output. Manual `Continue OMP` remains `CODEX_ASSISTED`; it is not independent engineering automation. A paused heartbeat, inactive adapter or unrelated production timer cannot satisfy the consumer contract. Activation remains fail-closed at the existing Engineering Authority boundary.

V4.25 adds the Mission Completion Evidence Gate inside existing OMP, Engineering Intent Closure, State Transition and truth/convergence owners. Every Mission declares one typed completion contract before promotion. Analysis, Discovery, Acceptance and Documentation may close at their exact legal evidence terminal; Implementation remains `IMPLEMENTED_NOT_CONSUMED` until consumption; Integration requires a real non-test caller, consumer, behavior change and next output; Automation additionally requires an independent trigger plus idempotency; Runtime and Production require their own live effects and verification. Tests, reports, deployment and manual Codex runs cannot promote a stronger class. `tools/v7-truth-check` consumes the validator through existing CPS functional-footprint consistency.

V4.26 adds Future-Scale Scenario Engineering to the existing Engineering Polygon and OMP continuation owners. When ordinary safe engineering work is exhausted, OMP immediately builds a deterministic Scenario Frontier from owner-bound machine-readable scenarios, stable invariant identities, current source/dependency fingerprints and current coverage. Scenario results are Engineering Evidence only: they may expose reproducible defects and certify invariant behavior, but cannot claim production outcomes, grant Authority, mutate Runtime, move users or increase Production Maturity. A reproducible mismatch flows through the existing BDP -> Candidate -> OMP Mission lifecycle. No new Polygon, owner, Runtime, Planner, scheduler, queue, truth source or simulation platform is created.

V4.29 corrects Phase 6 terminal semantics inside the existing Program Execution Reconciliation owner. Natural-production evidence wait is lane-local and cannot block independent Phase 6A scenario/future-scale work, Phase 6B controlled-production preparation where safe, or Phase 7 engineering continuous evolution. Evidence classes are criterion-specific and non-interchangeable. Production Authority evolution remains locked; no production action is selected or authorized by this correction.

V4.30 extends the existing Phase 6A FSSE/OMP consumer with owner-backed obligation generations. A generation closes only under its exact source/dependency fingerprints; the next generation is derived from still-uncertified scenario-safe capability criteria, consumed in deterministic obligation order, and remains Engineering Evidence only. Intermediate CPS transitions inside one bounded serial continuation defer external wake creation until the invocation frontier is stable, preventing external reentry from consuming a mixed generation. No Runtime, routing, user, Authority or Production Maturity effect is granted.

V4.31 makes the existing action-class owner separation machine-checkable in CPS. Engineering/scenario readiness, class-promotion certification, Authority recommendation, granted Authority, policy mutation and Runtime enablement are distinct states. Exhausted scenario projections cannot remain a live execution frontier, reports cannot become Authority truth, and an approve/reject question is legal only after current real-world evidence makes a durable exact recommendation ready. Otherwise OMP retains `GOVERNED_ONLY`, stops at `REAL_WORLD_LIMIT` and reenters only on a fresh qualifying controlled/natural outcome or a new owner-backed obligation.

V4.32 consumes the approved Routing Digital Twin Polygon Master Program through the existing Engineering Polygon, FSSE, BDP and OMP owners. One non-test entrypoint performs dynamic Mission compression, criterion-scoped fidelity selection, cross-Mission identity, isolated virtual apply, optional disposable Linux/Docker topology emulation, safety-first counterfactual evaluation, shadow Learning fork/held-out replay/cleanup, sanitized one-way snapshot import, hybrid logical scale, existing repair/reentry and exact next-obligation production. Missing privileged substrate is `POLYGON_SUBSTRATE_LIMIT`, never a global `REAL_WORLD_LIMIT`, while independent criteria remain executable. The integrated program terminal is reserved for post-deploy caller, truth, convergence and local/GitHub/production equality. No production packet, route, user, restore barrier, rollback, Authority or Production Maturity mutation is permitted.

V4.33 activates the certified Routing Digital Twin as the permanent Engineering Validation substrate consumed by OMP. Current unfinished capabilities, presently U02-U22, are only the first seed generation and never the permanent Polygon scope. After every bounded result, OMP derives the next owner-backed obligation from current capability gaps, new Missions, BDP Candidates and Intent Gaps, declared code/dependency/policy/owner changes, controlled or natural outcomes, action classes, product/topology/workload/scale changes, regressions, drift and bounded optimization targets. Capability-level dependency waits cannot hide independent criterion-level L1-L6 work. Each obligation carries minimum sufficient fidelity, source fingerprints, consumer, invalidation triggers, exact L7/L8 remainder and forbidden claims. Duplicate results are suppressed before re-execution; only declared dependencies are selectively invalidated. CPS remains the live frontier owner, BDP remains the gap/Candidate owner, existing component owners implement repairs, and normal safe-deploy/truth/convergence owners remain mandatory. The permanent Polygon creates no Runtime, Planner, owner, scheduler, queue, daemon, truth source, Authority or Production Maturity credit.

V4.34 makes the permanent Polygon lifecycle executable across separate reentry turns. CPS owns criterion-generation records and compare-and-swap; OMP dispatches only explicit owner-backed executor mappings; `ACTIVE` begins only at executor entry; consumed results admit but never pre-start successors. Every successful external turn consumes its wake and materializes a distinct successor wake with monotonic timestamps. Source mismatch fails closed through the existing BDP Candidate and OMP repair admission path before returning to the same obligation. Independent criteria with available executors preempt a missing-adapter criterion; when none remain, the exact missing adapter becomes one deterministic BDP Candidate and admitted OMP repair Mission and can never fall through to an unrelated Phase6A path. Bounded soak, duplicate suppression, behavioral reachability and forbidden-effect checks remain mandatory. No new owner, planner, queue, scheduler, Runtime or truth source is created.

V4.35 extends that same Permanent Polygon into the product design-time lifecycle. An owner-backed product objective or semantic source/policy/topology change is compiled through existing dependency bindings into exact affected Scenario obligations; baseline and proposed source snapshots execute through their native V7 owners and are compared by stable decisions, moves, terminals, invariant verdicts and forbidden effects. Reproducible mismatches are minimized and classified before BDP admission so Polygon model/harness/oracle/generator faults cannot become product repairs. Eligible V7 source repairs must return through tests, commit, `tools/v7-safe-deploy`, production non-test caller, truth/convergence and same/affected replay. Existing outcome/calibration owners feed risk coverage, and every coverage gap becomes an exact successor obligation. The Polygon and the product-development program therefore share one closed consumer loop; synthetic evidence grants no production confidence, Authority or Production Maturity credit, and no second Planner, Runtime, owner, scheduler, queue or truth source is created.

V4.36 records production deployment and real caller/consumer certification of that design-time loop. Exhaustion of the current dependency-bound Scenario corpus is not the target terminal: OMP must materialize the exact owner-backed calibration, protocol-substrate or natural-defect residual, must not ceremonially replay closed Missions, and must reenter only when that exact input exists. Production caller certification grants no production routing autonomy, Authority promotion or Production Maturity credit.

V4.37 activates the approved L7/L8 Production Evidence and Authority Evolution program through CPS and consumes mandatory read-only Mission 0. Existing production inventory, closure, observation, feedback, Learning, Decision Trace, replay, Production Maturity and Authority owners were reconciled before extension. The source-level inventory is reusable, but its aggregate closure rows do not carry a stable current-action-class material identity and cannot bind the two CPS outcomes to their exact operation, temporal, interpretation and replay records. OMP therefore admits only the exact residual Mission 1 record-level Outcome Evidence Passport and opportunity-denominator extension through existing owners; Missions 2 and 3 remain conditional residuals, and event-driven L7/L8 acquisition remains forbidden until its legal activation condition exists. This activation grants no routing, Runtime, user movement, Authority or Production Maturity effect.

V4.38 consumes the complete current L7/L8 evidence cycle through existing production event, outcome, Certification History, feedback, Learning, replay, Production Maturity, Authority and OMP owners. M1 binds both CPS material outcomes to four stable supporting-only passports and a 13,473-identity opportunity denominator; M2 and M3 preserve exact temporal and replay residuals; M4 and M5 remain legal event-driven boundaries without manufactured evidence; M6 emits immutable insufficient set `outset_4f53cda18c2baa0c0354bb5f`; M7 consumes `INSUFFICIENT_EVIDENCE`; M8 is not required by that verdict. The current evidence cycle is terminal and reenters only on qualifying owner-backed evidence closing an exact missing cell. This terminal does not claim L7 sufficiency, L8 representativeness, class approval, Authority expansion, autonomous Runtime or Production Maturity increase.

V4.39 corrects that terminal by making evidence-opportunity engineering an explicit permanent Polygon duty. An exact missing L7 cell activates bounded scenario selection, certification-pool/source resolution and fresh owner-bound Situation/Decision Trace/Candidate/Packet/verification/rollback preparation; only a real owner-authorized bounded production transaction can create L7 evidence. L8 remains natural, but the Polygon must prove and repair passive producer-file discovery and event-to-outcome/Learning/replay consumption before waiting. A combined L7/L8 `REAL_WORLD_LIMIT` is illegal while either preparation lane can continue. Ordinary customers cannot be relabelled to manufacture evidence, deliberate production degradation and certification-pool mutation stop at exact Engineering Authority, and no new event store, watcher, Planner, Runtime, Authority owner or truth source is created.

V4.40 consumes the first Polygon-driven L7 acquisition cycle. Actual date-partitioned L8 producers are discovered and all five passive capture roles pass. One genuine delegated-policy Candidate produced one real bounded one-user `SUCCESS`, complete immediate/5m/1h/steady-state verification, deterministic replay and one eligible controlled Passport. No second fresh Candidate remains: the next deliberate controlled condition/certification-pool change stops at exact independent Engineering Authority, while natural L8 separately remains `REAL_WORLD_LIMIT` with capture readiness complete. M6/M7 retain `INSUFFICIENT_EVIDENCE`, M8 is not required, Authority and Production Maturity remain unchanged, and the four exact representative coverage cells remain explicit.

V4.41 consumes the Polygon-driven L7 calibration floor without converting it into a promotion threshold. Four additional owner-authorized serial one-user controlled transactions produced complete real `SUCCESS` Passports; immediate, 5m, 1h, steady-state, Learning and deterministic replay are complete for all five eligible Passports. Material variation and the numeric floor close, while natural-production and rollback/no-rollback diversity remain explicit. M6 emits immutable insufficient set `outset_428a4e2ff440ed64bde5cb56`; M7 consumes `INSUFFICIENT_EVIDENCE`; M8 is not required. The controlled lane stops only at independent Engineering Authority for an exact deliberate rollback condition, and the natural lane remains capture-ready at `REAL_WORLD_LIMIT`. Authority, Production Maturity and background Runtime are unchanged.

V4.42 closes the notification-only failure gap in the existing design-time Polygon workflow. A failed `semantic-selective-gate` remains red, while its exact workflow/job/step/run/head/log fingerprint is classified and routed through the existing mismatch classifier, BDP Reality Gate and `OMP_CANDIDATE_ADMISSION`. Each distinct producer-consumer defect becomes its own deterministic repair frontier, so product regressions cannot absorb harness/binding defects and repeated runs retain stable identity. The GitHub artifact is engineering evidence, never a registry or live truth owner; CPS remains authoritative. Replaying the already-consumed L7 calibration finalizer with the exact same Mission/report/nonce/generation is also an idempotent `ALREADY_APPLIED_NO_CHANGE`; a conflicting identity still fails closed. The handler creates no watcher, queue, daemon, Runtime, routing, user, Authority or Production Maturity effect and never weakens, skips or converts the failed gate to green.

V4.43 consumes the mandatory R0 canonical projection reconciliation and prepares one exact R1 Engineering Authority request for the remaining controlled rollback-diversity cell. The packet binds one designated certification user, the existing controlled WireGuard source, one vless target, one serial transaction, a real source-failure Candidate, the existing service-matrix lifecycle/verifier, the normal verifier-triggered rollback branch, complete restoration, temporal verification, Passport, replay, Learning and M6/M7 consumers. Its hash, expiry and one-use law prevent implicit renewal or scope drift. Preparation grants no production mutation: R2 remains an independent `ENGINEERING_AUTHORITY` terminal and only its exact unexpired verdict may activate R3.

V4.44 consumes the exact one-use R2 as `STOP_SAFE_BEFORE_APPLY`, without treating governance admission, setup or cleanup as an L7 material outcome. The approval, Packet and lease are non-reusable. The two last-responsible binding defects are repaired through their existing owners and safely deployed: all controlled execution gates use the approved `EMERGENCY_FAILOVER` class, and the low-level control decision rereads the canonical selected-move hash after approved-lock rehydration. Exact cleanup restores the designated certification subject and remains Engineering Evidence only. Because the rollback/no-rollback cell is still open, OMP prepares a new independently decidable R1 v2 contract; no retry, production mutation, Authority expansion or maturity credit follows from this program update.

V4.45 consumes the user's standing exact-scope repair-continuation directive without converting it into a reusable approval. After a one-use controlled request reaches a proven pre-apply `STOP_SAFE`, with zero apply, movement and rollback, exact cleanup, a distinct repaired blocker, focused tests, safe deploy and aligned truth, the existing admission owner may issue and resolve one fresh one-use request for the semantically identical subject, source, target, verifier condition, evidence cell and one-user blast radius. A repeated blocker fingerprint, scope drift, ambiguous state, failed cleanup, ordinary-user selection, direct rollback, failure injection, background Runtime or Authority expansion fails closed. Request v2 remains consumed and non-reusable; fresh v3 is admitted for one foreground transaction only. This rule removes repeated human confirmation for the same safely repaired process while preserving fresh Candidate, Packet, lease, nonce and audit identities on every attempt.

V4.46 consumes the automatically admitted fresh v3 request exactly once. The transaction stopped before apply with zero movement and rollback, exact cleanup restored the certification subject and source, and no L7 credit was created. The repeated outer blocker fingerprint activated the standing policy's mandatory fail-closed terminal, so no v4 request is automatically issued and v3 is never retried. Root-cause resolution remains automatic engineering work: the exact verifier now reads mutable user assignment from `users.registry` and dynamic source lifecycle state from the existing `egress-flags.state` owner, with focused tests, safe deploy and production snapshot verification. Repeated production retries require an independent Engineering Authority decision; this does not weaken automatic continuation for a future distinct repaired blocker and creates no new Runtime, owner, queue, watcher, Authority, routing scope or Production Maturity credit.

V4.47 admits one fresh controlled verification only after the existing Engineering Authority owner proves a distinct deployed repair generation for the same repeated blocker fingerprint. The current repair-generation identity binds commit `c5563d40589cba98c2c8795f2c0338fb92eaaf1c`, deploy `deploy-z8-14-Updatesystem-c5563d4-20260720T093542`, the deployed autoswitch binary hash, one exact certification subject/source/target, one verifier-triggered rollback condition and one transaction. A read-only production preflight must pass before setup; setup and cleanup remain Engineering Evidence only. The request, Packet, lease and nonce remain fresh and one-use, and the same repair generation can never be retried. L7 is `READY` only for this foreground bounded transaction; L8 remains passive capture-ready. No Authority expansion, background Runtime, direct rollback, failure injection, ordinary-customer evidence manufacture or Production Maturity credit is granted.

V4.48 consumes v4 exactly once as `STOP_SAFE_BEFORE_APPLY`. The source bundle and exact operation-scoped identities matched, while only the redundant runtime snapshot hash mismatched because its Packet producer used normalized source identities and its low-level consumer used raw registry-file hashes. The existing consumer now validates operation-scoped snapshots like-for-like while raw envelopes retain byte-level binding and semantic source drift remains independently fail-closed. Focused tests and the full design-time Polygon affected-obligation campaign pass with every forbidden effect absent. V4, its Packet, lease and nonce remain non-reusable; only a safe deployed distinct repair generation may admit fresh v5 in the same exact scope. L7 receives no credit from this stop, L8 remains passive capture-ready, and Authority and Production Maturity do not change.

V4.53 consumes the exact v6 controlled rollback outcome after the repaired verifier, required-service propagation, material-terminal aggregation and delayed-observation consumers are safely deployed. Production replay preserves `ROLLBACK_SUCCESS`, deterministic replay is `NO_DRIFT`, the due delayed observation is written once, and immediate replay writes zero. The locked five-Passport calibration-floor certification plus the new fully eligible rollback Passport form immutable set `outset_48bda484f8f3ef7985e4716f`; raw log retention cannot revoke the prior consumed certification or replace current truth with a smaller diagnostic read set. Rollback/no-rollback diversity closes, while `natural_production_present` remains the only missing representative cell. M6/M7 remain `INSUFFICIENT_EVIDENCE`, M8 is not required, current `GOVERNED_ONLY` remains unchanged, and no Authority or Production Maturity promotion occurs. With no independent declared L7 criterion remaining, the program stops legally only at the passive natural-L8 `REAL_WORLD_LIMIT`.

V4.54 corrects the last single-action-class terminal assumption. A natural-L8 wait belongs only to the action class whose representative cell is open; it must not conceal independently reusable product engineering for another class. The existing Polygon corpus, hard-failure classification and anti-flap arbitration owners now derive one deterministic `channel hard-fail failover` design-time obligation when its exact source bindings exist. Its isolated scenario is consumed through the existing OMP result consumer and records zero Runtime, routing, user, Authority, Production Maturity, L7 or L8 effect. No action-class evidence cross-credit is allowed: a current-class Passport or future natural event cannot certify a different class, and the engineering result does not admit production execution. After every result CPS projects the current action-class evidence frontier, the independent engineering frontier, exact selection and passive L8 observation window; duplicate obligations are suppressed. Only when each selected class has no executable engineering frontier may the program stop at its class-local natural observation boundary. No Planner, queue, scheduler, watcher, truth source, Runtime, Authority owner or Maturity rule is created.

V4.55 closes the service-failure persistence and operator-semantics gap for every egress/action class through existing owners. The service-matrix producer now preserves source-bound failure-episode continuity across processes and emits one passive, unattributed external-event candidate only after its configured persistence threshold. The autoswitch consumer records that candidate as Situation/Decision Trace/STOP_SAFE/temporal/replay/Learning capture with zero Candidate, Packet, user movement, routing mutation, Authority, L7 or L8 credit. Only a later owner-backed provenance and complete legal production outcome may qualify as natural L8. Runtime/config readiness remains a distinct UI dimension and may never be displayed as service availability. Recovery resets the producer episode through the same matrix owner; transient, stale and methodology-limited probes remain non-escalating. No new event store, watcher, Planner, Runtime, Authority owner, queue or truth source is created.

V4.56 closes the remaining production producer-to-consumer liveness defect in that same owner chain. The existing 15-minute service-matrix lifecycle now invokes the existing passive-event consumer through a dedicated capture-only entrypoint after every batch; the entrypoint rejects apply, Packet, lease, rollback and Authority flags and cannot plan, move users, mutate routing or grant L7/L8 credit. Failure-episode continuity is aligned with the timer's randomized delay and batch duration, so one continuing outage is no longer reset to `sample=1` on every run; an unrelated long observation gap still starts a new episode. A missing, failed or explicitly skipped consumer is emitted in the existing matrix summary/event as exact OMP repair frontier `V7_PASSIVE_SERVICE_EVENT_CONSUMER_REPAIR`. This creates no second timer, watcher, event store, queue, Runtime or owner and changes neither Authority nor Production Maturity.

V4.57 closes the service-failure lifecycle and multi-lane product-evolution residual through those same owners. Continuity is now derived from the production cadence, jitter, batch budget and safety allowance; episode identity binds canonical `egress.registry`, a secret-free config generation and the normalized failure family. Repeated service children correlate to one source incident and one bounded Situation chain. Recovery and observation-gap expiry append temporal terminals linked to the original incident instead of erasing it. The passive consumer canonicalizes duplicate deterministic event IDs, preserves operator/external/controlled/synthetic provenance separation, and emits the exact existing OMP product-engineering frontier after a material incident or recovery. The multi-lane selector is no longer a single hard-failure literal: consumed obligation IDs are suppressed and the smallest owner-backed service-plane, transport/protocol, recovery/anti-flap or correlated-provider criterion is selected. Permanent Polygon executes the bounded failure-family matrix and existing scenarios through `OMP_PROGRAM_EXECUTION_RECONCILIATION`; canonical outcome aliases map to the existing SUCCESS/CORRECT_STAY/STOP_SAFE/ROLLBACK/NO_CANDIDATE/MISSED taxonomy. These engineering results grant no Natural L8, Runtime, routing, user movement, Authority or Production Maturity effect. The current external VLESS listener remains a separate `EXTERNAL_ENDPOINT_OWNER_BOUND` lane when its owner is not available.

V4.58 closes the missing durable consumer link from the existing service Matrix lifecycle to OMP. A passive Situation/Decision/Outcome terminal is materialized once as an append-only obligation through the existing closure owner, classified immediately as correct safety, data/evidence, existing capability, implementation, Authority or external-owner responsibility, and consumed once by the standard Continue OMP entrypoint. The same existing autoswitch planner supplies a bounded incident decision and the existing shadow owner receives at most one current-tier counterfactual record; an exact later owner-backed execution outcome is compared automatically, while absence of execution is never fabricated as an outcome. Incident and Product Evolution are parallel projections of one existing OMP frontier. A safe target without a current one-use contract stops at the exact `ENGINEERING_AUTHORITY` boundary. This adds no queue, Planner, Runtime, Authority owner or route action, and grants no L8, routing, user-movement or Production Maturity credit.

V4.61 closes the controlled-certification-substrate Authority producer/consumer gap inside the existing operator-execution audit, standing-policy status and CPS/OMP projection owners. One exact registered request may receive one append-only independently attributed `APPROVE_CONTROLLED_CERTIFICATION_SUBSTRATE_AND_CAMPAIGN` or `DECLINE`; concurrent duplicates are suppressed, stale/hash/scope mismatches fail closed, and an expiry-only replacement preserves one semantic fingerprint without coexisting as a second active request. The ordinary-production scalar remains bounded by the ordinary proven Runtime tier, while the controlled-certification tier is projected on a separate contextual axis. A pending request is the exact top-level CPS/OMP Authority frontier and cannot collapse back into a generic pool-reconciliation loop. Approval only publishes the existing incremental M8 substrate successor; it does not itself provision identities, create a Candidate/Packet/lease, execute a campaign, move users, expand ordinary-production Authority, credit production evidence, or change Production Maturity.

V4.62 makes controlled-source isolation a mandatory producer/consumer
precondition inside the same certification-pool, Authority-status and CPS
owners. An active controlled source is campaign-eligible only when current
registry truth proves zero enabled non-certification users on it. An approval
bound to a mixed source cannot be transferred to another source or consumed
for setup; it fails closed with zero production effects. The existing request
producer may select an already-existing empty eligible source candidate and
register one fresh exact independently decidable request. No new source,
owner, registry, Runtime, Planner, campaign engine or Authority system is
created.

V4.27 connects the standard `Continue OMP` trigger to a bounded single-invocation engineering loop inside the same OMP/Polygon owners. One invocation reads fresh CPS, evaluates ordinary work first, selectively invalidates dependency-bound coverage, executes real-code scenarios, validates and consumes results, updates the frontier atomically, routes an eligible mismatch through existing BDP/Candidate/admission owners, reruns the target and affected subset, and stops only at an exact bounded or legal terminal. It adds no scheduler, daemon, queue, Runtime, Planner, repair engine, Candidate owner or background reentry claim.

V4.28 certifies external reentry for the standard bounded `Continue OMP` consumer. The normal primary path is the event-driven Codex Automation Platform thread signal: a CPS READY transition emits one deterministic wake, starts a separate platform turn, invokes the standard entrypoint and consumes `OMP_PROGRAM_EXECUTION_RECONCILIATION` immediately without waiting for the 30-minute schedule. Execution remains serial under the existing lease; duplicate wakes are suppressed and overlap is forbidden. The existing heartbeat is `WATCHDOG_FALLBACK` only and may recover a lost wake; it is not the normal continuation-latency mechanism. The earlier two distinct natural scheduled events remain supporting certification evidence. External engineering reentry grants no Runtime, routing, packet, user, restore-barrier, rollback, Authority or Production Maturity effect. This creates no scheduler, daemon, queue, owner, Runtime or Planner.

V4 operating questions:

```text
What implementation gives the highest production leverage right now?
What authority tier is certified by real outcomes?
What safe work can continue before an allowed stop condition?
```

V2.1 adds architectural minimalism, semantic reuse, a new-owner gate, architecture duplication detection, and an explicit optimization engine. V2.2 adds Safety-Bounded Authority: trust decides autonomy tier, safety decides bounded action. V2.3 adds Kernel and State Split: permanent operating rules live in Kernel/OMP, volatile current state lives in Current Program State. V3.0 closes architecture-first work and activates implementation-first optimization. V4.0 finalizes OMP as the permanent Production Program and integrates autonomy maturity, implementation, authority evolution, continuous optimization, and continuous knowledge evolution into one operating loop. V4.1 aligns OMP with AEP and BDP so certified Behaviour Discovery outputs can be consumed as implementation input without creating a new queue, owner, Runtime, Planner, or architecture. V4.2 adds Implementation Candidate Identity, Instance-based Mission admission, candidate merge, cohort safety, and reopen rules inside the existing OMP admission model. V4.3 defines the post-BDP-stabilization lifecycle: after BDP architecture is stable, further project evolution must start from OMP consumption and sequencing of existing BDP outputs, not from further BDP expansion unless `FUNDAMENTAL_BDP_ARCHITECTURE_GAP` is proven. V4.4 adds the canonical OMP Candidate Sequencing Algorithm inside existing OMP execution: OMP computes the best admissible Candidate sequence from certified BDP outputs, safety/authority/runtime/rollback boundaries, dependency order, coverage gain, Engineering Value, and System Engineering Value without creating a Planner or manual priority layer. V4.5 adds the OMP Decision Trace Contract: every OMP candidate decision must preserve an evidence-linked explanation of how the existing OMP decision was reached, without creating a Planner, Decision Engine, Recommendation Engine, new owner, or new architecture. V4.6 adds the Decision Reproducibility Law: identical canonical OMP decision inputs must produce identical Decision Trace, sequence, Mission Admission result, STOP, and final verdict, or OMP must stop with `NON_DETERMINISTIC_DECISION`. V4.7 adds the Automation Gap Closure Cycle: every STOP must be classified as a fundamental boundary or routed through existing BDP -> OMP candidate production and admission as a possible automation-removal Implementation Candidate Instance. V4.8 adds Engineering Intent Closure Validation inside Automation Gap Closure: a STOP-derived candidate closes an automation gap only when the original Engineering Intent is achieved, Current State matches Expected State, the original STOP disappears, and the Engineering Chain reaches a Legal Terminal Consumer. V4.9 adds universal Intent Gap Detection: Automation Gap Closure is triggered by any unfinished Engineering Intent, even when no explicit STOP occurred and execution/verification appeared to pass. V4.10 adds Intent Responsibility Resolution: every `INTENT_GAP_DETECTED` must identify the last responsible Engineering Chain link and owner-mapped responsibility class before routing specialized input to BDP. V4.11 adds OMP consumption of the existing Necessity Framework: every owner, capability, function, module, service, CLI, API, read model, dashboard, engineering process, or document must have a certified existence verdict before it can remain permanent. V4.12 adds Capability Maturity Protection: Necessity, merge, removal, value conservation, and architectural minimization cannot alter elements belonging to unfinished capabilities. V4.13 adds Engineering Work In Progress Protection: architectural minimization cannot alter any engineering object that participates in an unfinished Mission, Candidate, Engineering Chain, Behavior Chain, State Transition, Verification, Certification, dependency, root cause, producer/consumer handoff, integration, BDP Discovery, or other existing unfinished lifecycle. V4.14 adds Approved Future Dependency Protection: architectural minimization cannot alter objects already required by accepted future Missions, Candidates, Chains, Capability plans, State Transitions, Verification, Certification, integrations, producers, consumers, behavior chains, runtime transitions, Depends On / Unblocks, or other approved execution dependencies. V4.15 adds Current State Consistency: OMP owns rules and historical snapshots, while `docs/programs/V7_CURRENT_PROGRAM_STATE.md` is the only authoritative volatile current-state owner. V4.16 adds Engineering Truth Lifecycle: any reused engineering truth must have an owner, truth source, validity conditions, invalidation triggers, revalidation route, and reuse rule before OMP may consume it as current. OMP always wins over free-form implementation ideas.

## 1. Project Vision

V7 is an event-driven autonomous routing control plane that protects user connectivity by observing production reality, selecting safe routes through existing owners, acting only under certified authority, verifying outcomes, and learning from real evidence.

This vision is immutable unless a future ADR explicitly supersedes it.

## 2. Program Principles

1. Reality First.
2. Discover -> Reuse -> Extend -> Implement.
3. No duplicate owners.
4. No duplicate planners.
5. No duplicate governance.
6. No synthetic evidence.
7. Tests before certification.
8. Certification before next phase.
9. Documentation after implementation.
10. Continue automatically when possible.

Operational meaning:

- Reports preserve evidence.
- Canonical reference preserves current truth.
- ADRs preserve decisions.
- This program preserves what V7 does next.

## 2.1. Kernel and State Split

V7 separates permanent operating rules from volatile current state.

| Layer | File | Purpose |
| --- | --- | --- |
| V7 Kernel | `docs/reference/V7_KERNEL.md` | Permanent Codex operating contract. |
| OMP | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` | Scheduler and optimizer. |
| Current Program State | `docs/programs/V7_CURRENT_PROGRAM_STATE.md` | Volatile current bottleneck, HLA, packet, normalized authority class, metrics, stop reason, and next automatic action. |
| Canonical Reference | `docs/reference/V7_CANONICAL_REFERENCE.md` | Current system truth. |
| SYSTEM_MAP | `docs/reference/SYSTEM_MAP.md` | Owner/topology map. |
| ADRs | `docs/decisions/` | Accepted decisions. |
| Reports | `docs/reports/` | Evidence and history. |
| Runtime | production/runtime state | Reality and final verification. |

Current volatile state lives in `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

OMP must not become a dumping ground for every packet or state update.

Long packet/state payloads belong in Current Program State. OMP should keep only scheduler/optimizer rules and pointers unless scheduler meaning changes.

### 2.1.1. Current State Consistency Law

There must be exactly one authoritative volatile current state for V7:

```text
docs/programs/V7_CURRENT_PROGRAM_STATE.md
```

OMP owns:

- scheduler rules;
- optimizer rules;
- lifecycle rules;
- authority rules;
- stop rules;
- state transition rules;
- historical snapshots required to explain why rules changed;
- pointers to the authoritative current state.

OMP does not own multiple live current states.

Any OMP section, table, field, or sentence named `Current`, `Current Focus`, `Current Priority`, `Current Stage`, `Current Target`, `Current Action`, `Current Status`, `Next Step`, `Highest Priority`, `Highest Bottleneck`, `Highest Implementation Leverage`, or similar is one of:

1. `PERMANENT_RULE` when it defines how OMP calculates current state;
2. `CURRENT_PROGRAM_STATE_REFERENCE` when it points to CPS;
3. `HISTORICAL_SNAPSHOT` when it preserves an earlier OMP state;
4. `HISTORICAL_MILESTONE` when it records a completed phase, certification, or transition;
5. `HISTORICAL_EXAMPLE` when it illustrates a rule;
6. `DEPRECATED_CURRENT_STATE` when superseded by CPS or a later report.

Only `CURRENT_PROGRAM_STATE_REFERENCE` may be consumed as live current state, and it must resolve to `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

If OMP and CPS appear to disagree:

```text
CPS wins for volatile current state.
OMP wins for scheduler / optimizer / lifecycle rules.
Engineering Reports preserve historical evidence.
Canonical Reference preserves durable truth.
SYSTEM_MAP preserves owner topology.
```

Consumer rule:

Codex, OMP Scheduler, BDP, Mission, Automation Gap Closure, Engineering Intelligence, dashboards, and any future consumer must read the live current state only from CPS. They may read OMP historical snapshots only as evidence, never as active state.

No OMP historical snapshot may start implementation, Mission creation, automation, authority request, runtime action, or scheduler continuation unless the same state is confirmed in CPS.

### 2.1.2. Engineering Truth Lifecycle Law

Every engineering truth consumed by OMP must have a lifecycle.

OMP must not consume an old engineering object as current truth only because the object has an owner, source, producer, or consumer. Before reuse, OMP must resolve whether the object is still valid under existing owners and existing lifecycle mechanisms.

This law creates no new truth owner, Runtime, Planner, Truth Engine, Validity Engine, state engine, or architecture.

It composes existing mechanisms:

- Decision Lifecycle;
- Decision Freshness;
- Reference First;
- Knowledge Plane;
- Current Program State;
- Engineering Reports;
- Behavior Enforcement;
- State Transition Law;
- Capability Lifecycle;
- Production Maturity;
- Verification;
- Certification;
- Re-open Trigger;
- Architecture Closed by Default;
- Need New Owner Gate;
- Semantic Reuse Audit.

Engineering truth objects include existing objects only:

- Capability;
- Mission;
- Engineering Report;
- Canonical Reference entry;
- Decision Trace;
- Decision Fingerprint;
- Current Program State field;
- Production Maturity result;
- Policy;
- Verification result;
- Certification result;
- Behavior Contract;
- State Transition;
- Runtime Readiness result;
- Engineering Knowledge;
- any other existing canonical object consumed by OMP.

For every reused engineering truth object, OMP must resolve:

| Required field | Meaning |
| --- | --- |
| Truth Source | Existing canonical owner, CPS field, report evidence, runtime owner, policy, verification owner, certification owner, or other existing source. |
| Owner | Existing owner responsible for confirming or invalidating the truth. |
| Validity Basis | What makes the object true: acceptance, certification, fresh evidence, current state, terminal owner result, verified consumption, or canonical lock. |
| Invalidation Triggers | Existing conditions that make the object no longer usable as current truth without revalidation. |
| Revalidation Route | Existing owner, verification, certification, report correction, CPS update, policy review, or reference update that can confirm the truth again. |
| Reuse Rule | Whether OMP may reuse it as current, reuse it as historical evidence only, require revalidation, or stop. |

Allowed lifecycle states reuse existing V7 meanings:

| State | Meaning |
| --- | --- |
| `VALID` | Existing owner confirms the object is still usable for the requested OMP consumption. |
| `REVALIDATION_REQUIRED` | Existing trigger, drift, stale evidence, contradiction, changed dependency, changed authority, changed production reality, or confidence limit requires owner confirmation before reuse. |
| `HISTORICAL` | Object remains evidence/history but is not current truth. |
| `SUPERSEDED` | Later accepted owner evidence replaced the object. |
| `RETIRED` | Object has no live consumer or was retired through an existing lifecycle. |
| `NOT_APPLICABLE_WITH_REASON` | Object does not apply to the current task and the reason is recorded. |

OMP must evaluate revalidation before consuming current truth if any of these existing events occurred:

- Product meaning changed;
- Policy changed;
- Runtime changed;
- Capability changed;
- dependency changed;
- architecture changed;
- Production Reality changed;
- Authority changed;
- evidence freshness expired;
- Decision Lifecycle invalidated the decision;
- Decision Fingerprint no longer matches;
- Behavior Chain status changed;
- State Transition was not completed;
- Verification failed, became stale, or was contradicted;
- Certification was superseded, invalidated, or scoped differently;
- Production Maturity returned `BLOCK`, `NO_CHANGE`, `PARTIAL_ACCEPT`, or `INVALID_EVIDENCE`;
- Current Program State contradicts the object;
- Canonical Reference superseded the object;
- SYSTEM_MAP owner topology changed;
- an Engineering Report correction exists;
- an existing Re-open Trigger fired;
- real evidence contradicts the object.

Decision rule:

| Lifecycle result | OMP action |
| --- | --- |
| `VALID` | Reuse through existing owner path. |
| `REVALIDATION_REQUIRED` | Stop current consumption and route to the existing owner / verification / certification path before reuse. |
| `HISTORICAL` | Use as evidence only; never as current truth. |
| `SUPERSEDED` | Use the superseding object or stop if supersession path is unclear. |
| `RETIRED` | Do not use for current execution unless a reactivation lifecycle exists. |
| `NOT_APPLICABLE_WITH_REASON` | Exclude from current reasoning and record why. |

If lifecycle cannot be resolved, OMP must return:

```text
TRUTH_LIFECYCLE_UNRESOLVED
```

and identify the smallest existing owner action required to resolve it.

`Continue OMP` means: execute the complete Engineering Control Loop through existing owners until an allowed stop condition.

### Continue OMP Engineering Control Loop

Status: `CANONICAL`

`Continue OMP` is the single default engineering command for V7.

It must not be interpreted as only:

```text
Continue the backlog.
```

It means:

```text
Execute the complete Engineering Control Loop.
```

The loop is:

```text
Engineering Context Resolver
  -> Knowledge Consumption
  -> Engineering Truth Lifecycle Evaluation
  -> Re-open Evaluation
  -> BDP Implementation Candidate Consumption when present
  -> OMP Execution
  -> Mission Formation
  -> Implementation / Audit / Certification / Verification
  -> Engineering Report
  -> Knowledge Promotion
  -> Current Program State Update
  -> OMP Update
  -> Continue OMP
```

Step responsibilities:

| Step | Required behavior | Existing owner |
| --- | --- | --- |
| Engineering Context Resolver | Classify task, resolve minimum context, load only required owners. | `docs/reference/V7_CONTEXT_RESOLVER.md` |
| Knowledge Consumption | Read Product Specification, Canonical Reference, SYSTEM_MAP, Audit Knowledge State, Current Program State, OMP, current Mission / Backlog item, accepted BDP candidate when present, and Runtime Model only if runtime relevant. | Knowledge Plane / OMP |
| Engineering Truth Lifecycle Evaluation | Resolve owner, truth source, validity basis, invalidation triggers, revalidation route, and reuse rule before any consumed object is used as current truth. | OMP + existing truth owner / verification / certification owner |
| Re-open Evaluation | Determine whether knowledge is already verified, still current, stale, confidence-limited, or re-opened by trigger. | Knowledge Plane / Canonical Reference / relevant owner |
| BDP Implementation Candidate Consumption when present | Consume accepted BDP Implementation Candidate Catalogue entries only as certified implementation input, never as a new queue or Discovery responsibility. | OMP + Behaviour Discovery Program output |
| OMP Execution | Determine highest production-leverage accepted work item from the Implementation Backlog, existing owner, or certified BDP Implementation Candidate; after BDP architecture stabilization, use Candidate Coverage Matrix, Progress Projection, Engineering Chain Dependency Projection, Engineering Value, and System Engineering Value to select the optimal existing-candidate implementation sequence; consume Product Evolution behavior inputs when meaningful; produce an OMP behavior decision; reuse existing owners; do not redesign. | OMP |
| Mission Formation | Convert an approved work item into an OMP Mission with Engineering Intent, expected closure, owner, dependencies, authority, verification, rollback, Runtime, production, and Codex handoff boundaries. | OMP |
| Implementation | Implement only an approved OMP Mission when implementation is the resolved action and the OMP behavior decision allows execution; otherwise record blocked, deferred, rejected, or not-applicable result. | OMP Mission + existing code owner + Codex when assigned |
| Verification | Run relevant tests, truth, convergence, runtime verification, documentation consistency, or knowledge consistency only when required by task class. | OMP + relevant verification owner |
| Certification | Certify only when required by OMP capability, policy, action class, or production maturity. | OMP + certification owner |
| Engineering Report | Create a Russian Engineering Report after every meaningful engineering action, including Product Evolution Field Validation, OMP behavior decision, new output, and Learning trigger when applicable. | OMP report lifecycle |
| Knowledge Promotion | Extract durable knowledge from reports and update canonical owners when needed. | Canonical owner + Canonical Reference + SYSTEM_MAP |
| Current Program State Update | Update only when execution state, bottleneck, authority class, maturity, current task, or stop condition changes. | Current Program State |
| OMP Update | Update only when optimizer, capability, command, stop, or maturity semantics change. | OMP |

Every future engineering task should begin with `Continue OMP` unless the operator explicitly requests a narrower action.

No future engineering work should bypass:

```text
Engineering Context Resolver
  -> Knowledge Plane
  -> OMP
```

unless explicitly requested by the operator.

### Autonomous Execution Canonical Consumption

Status: `CANONICAL_INTEGRATED`

OMP is the only execution program for autonomous execution.

OMP explicitly consumes:

| Canonical input | OMP consumption |
| --- | --- |
| `docs/programs/V7_AUTONOMOUS_EVOLUTION_PROGRAM.md` | Defines the strategic route from locked knowledge through Reality, BDP, Gap/implementation input, and OMP execution; OMP remains the execution operating system. |
| `docs/programs/V7_BEHAVIOUR_DISCOVERY_PROGRAM.md` | Produces accepted Implementation Candidate Catalogue, Automation Break, Intent Closure, and coverage evidence that OMP may consume as implementation input after admission. |
| `docs/reference/V7_AUTONOMOUS_EXECUTION_PROGRAM.md` | Defines when V7 may execute without an operator and the L3 -> L7 autonomy ladder. |
| `docs/reference/V7_AUTONOMOUS_RUNTIME_MODEL.md` | Defines the stable Runtime Operating System, dispatcher/control-loop/state-machine contracts, Architecture Lock, Implementation Handoff, Runtime Stability Law, and implementation consumer ladder. |
| `ARCHITECTURE_LOCKED_FOR_AUTONOMY_IMPLEMENTATION` | Blocks new Runtime, Planner, Authority, OMP, Governance, Truth Source, and roadmap creation by default. |
| `AUTONOMY_ARCHITECTURE_COMPLETE` | Closes autonomy architecture work and routes future work through OMP implementation only. |
| Runtime Stability Law | Requires every new autonomous capability to extend certified action classes, not Runtime OS behavior. |
| Implementation Handoff | Sets the next sequence: Canonical Integration -> OMP Integration -> L3 Emergency Autonomous Failover Design -> L3 Implementation -> L3 Production Validation -> L3 Certification -> L4 -> L5 -> L6 -> L7. |

Future capability ladder:

| Level | OMP meaning |
| --- | --- |
| `L3` | Emergency Autonomous Failover. |
| `L4` | Degraded Channel Autonomy. |
| `L5` | Recovery Autonomy. |
| `L6` | Bounded Rebalance. |
| `L7` | Full Routing Autonomy. |

OMP must not create another autonomy roadmap, Runtime model, Planner model, Authority model, execution architecture, or lifecycle.

Next stage after Canonical Integration:

```text
L3_EMERGENCY_FAILOVER_DESIGN
```

### Behavior Architecture Completion Rule

Status: `CANONICAL`

OMP must treat architecture, implementation, certification, or capability work as complete only when the relevant behavior chain reaches a legal executable terminal consumer.

Architecture diagrams, implementation code, analysis, recommendations, reports, dashboard views, read models, diagnostics, previews, advisory surfaces, or scores alone are not completion.

The required propagation shape is:

```text
Producer
  -> Output Produced
  -> Output Available
  -> Consumer Exists
  -> Consumer Consumed Output
  -> Consumption Verified
  -> Consumer Behavior Changed
  -> Next Output Produced
  -> Next Consumer
  -> Legal Terminal Consumer
```

OMP must distinguish these engineering states:

- `OUTPUT_PRODUCED`;
- `OUTPUT_AVAILABLE`;
- `OUTPUT_CONSUMED`;
- `CONSUMPTION_VERIFIED`;
- `BEHAVIOR_CHANGED`;
- `NEXT_OUTPUT_PRODUCED`.

These states are not interchangeable.
An output that exists is not automatically consumed.
A named consumer is not proof of consumption.
Consumption is not verified until owner state, tests, runtime behavior, certification evidence, Current Program State, or another canonical owner proves that the consumer used the output and changed behavior.

Legal terminal consumers are:

- Runtime Ready For Next Cycle;
- Capability Certified;
- Production Maturity Updated;
- OMP Next Step Produced;
- Capability Locked;
- Capability Retired;
- Terminal `STOP_SAFE`;
- `ENGINEERING_AUTHORITY`;
- `OPERATIONAL_AUTHORITY`;
- `REAL_WORLD_LIMIT`.

Forbidden terminal consumers are:

- read model;
- dashboard;
- Engineering Report;
- diagnostic output;
- recommendation;
- placeholder;
- future work;
- TODO;
- comment;
- preview;
- simulation;
- advisory surface;
- read-only status.

Forbidden terminal consumers may exist only as intermediate evidence when another executable owner consumes them and produces the next executable input.

If a producer has no existing consumer, if the consumer does not consume the output, if consumption cannot be verified, if consumer behavior does not change, if the next output is not produced, if the next output is not consumed, or if the chain cannot reach a legal terminal consumer, OMP must classify the work as `PARTIAL`, `BLOCKED`, `BROKEN`, deferred, or not applicable with reason. OMP must never classify the work as `COMPLETE`.

### Behavior Enforcement Framework

Status: `CANONICAL`

Behavior Enforcement turns documented Behavior Contracts into verifiable engineering gates.

OMP must not assume that a consumer performed the required behavior.
OMP must verify behavior propagation before declaring a meaningful step complete.

Behavior Chain Status values:

| Status | Meaning |
| --- | --- |
| `COMPLETE` | Producer output exists, output is available, intended consumer exists, consumer consumed it, consumption is verified, consumer behavior changed, expected next output exists, downstream consumer exists, legal terminal consumer is reached, and verification evidence exists. |
| `PARTIAL` | Some required behavior occurred, but at least one expected output, downstream consumer, or evidence item remains incomplete. |
| `BLOCKED` | A stop gate, owner, certification, authority, safety, evidence, or state condition prevents behavior propagation. |
| `BROKEN` | Producer output, consumer, behavior change, output, or downstream consumer is missing or contradictory. |
| `UNKNOWN` | Verification evidence is insufficient to classify the chain. |

Every Behavior Contract must define:

| Field | Required meaning |
| --- | --- |
| Trigger | Event, report, OMP decision, certification result, state change, or operator action that starts verification. |
| Expected Consumer | Existing owner expected to consume the producer output. |
| Output Produced | Output the producer emitted, or `NOT_APPLICABLE_WITH_REASON`. |
| Output Available | Proof that the output is reachable by the consumer, or `NOT_APPLICABLE_WITH_REASON`. |
| Consumer Consumed Output | Proof that the consumer read, accepted, loaded, invoked, stored, certified, or otherwise used the output. |
| Consumption Verified | Verification method proving the consumed output changed execution, state, certification, maturity, OMP step, or legal terminal status. |
| Expected Behavior | Required consumer behavior change. |
| Expected Output | Next output the consumer must produce after verified consumption. |
| Terminal Consumer | Legal terminal consumer reached by the chain, or the next executable owner that must consume the output. |
| Verification Method | Report field, owner state, certification result, CPS field, dashboard source, test, truth/convergence, or explicit `NOT_APPLICABLE_WITH_REASON`. |
| Failure Condition | `OUTPUT_NOT_CONSUMED`, `CONSUMPTION_NOT_VERIFIED`, `NO_BEHAVIOR_CHANGE`, `NEXT_OUTPUT_NOT_PRODUCED`, `ORPHAN_OUTPUT`, `ORPHAN_CONSUMER`, missing output, missing evidence, missing legal terminal consumer, contradiction, synthetic evidence, duplicate owner, or forbidden authority/runtime/automation path. |
| Recovery Path | Existing owner re-run, Engineering Report correction, canonical update, CPS update, OMP `DEFER`, OMP `BLOCK`, owner mapping, or explicit `NOT_APPLICABLE_WITH_REASON`. |

Major Behavior Enforcement Gates:

| Producer -> Consumer | Verification gate | Required evidence | Failure output | Blocked output | Recovery output |
| --- | --- | --- | --- | --- | --- |
| Framework -> OMP | Framework outputs referenced and OMP behavior decision recorded. | Product Observation / Product Value / target / gap / evidence fields or `UNKNOWN`; OMP decision. | `BROKEN_FRAMEWORK_TO_OMP` | `BLOCKED_BY_OWNER_OR_EVIDENCE` | OMP Field Validation correction or owner mapping. |
| OMP -> Execution | Execution decision allows existing-owner work or explicit non-execution result exists. | Execution Decision, Blocked Result, Deferred Result, Rejected Result, or `NOT_APPLICABLE`. | `BROKEN_OMP_TO_EXECUTION` | `BLOCKED_BY_STOP_GATE` | Re-run OMP decision or record blocked/deferred result. |
| Execution -> Engineering Report | Meaningful action produced report evidence. | Engineering Report with action, evidence, safety, alternatives, and Product Evolution fields. | `BROKEN_EXECUTION_TO_REPORT` | `BLOCKED_BY_MISSING_REPORT_EVIDENCE` | Create or correct Engineering Report. |
| Engineering Report -> Production Maturity | Maturity-affecting work has Production Maturity Decision or `NOT_APPLICABLE`. | `ACCEPT`, `PARTIAL_ACCEPT`, `BLOCK`, `NO_CHANGE`, `INVALID_EVIDENCE`, or `NOT_APPLICABLE`. | `BROKEN_REPORT_TO_MATURITY` | `BLOCKED_BY_CERTIFICATION_OR_EVIDENCE` | Production Maturity review or report correction. |
| Production Maturity -> CPS | Volatile state changed or explicit no-change recorded. | CPS impact field; current maturity/target/blocker state or no volatile change. | `BROKEN_MATURITY_TO_CPS` | `BLOCKED_BY_VOLATILE_STATE_GAP` | CPS update or explicit no-change reason. |
| CPS -> Product Observation / Framework | Current Product Reality is available or marked `UNKNOWN` / `NOT_APPLICABLE`. | CPS current reality, target, transition, blockers, readiness context. | `BROKEN_CPS_TO_FRAMEWORK` | `BLOCKED_BY_CURRENT_STATE_GAP` | CPS correction or Framework Field Validation `UNKNOWN`. |
| Engineering Report / Learning -> Engineering Intelligence | Learning, prediction-vs-reality, confidence, or recommendation impact is recorded. | Engineering Intelligence learning impact fields. | `BROKEN_LEARNING_TO_EI` | `BLOCKED_BY_OUTCOME_OR_PREDICTION_GAP` | Learning owner review or report correction. |
| Engineering Intelligence -> Dashboard | EI outputs are visible only as read-only advisory context or marked `UNKNOWN` / `NOT_APPLICABLE`. | Dashboard visibility impact and source owner. | `BROKEN_EI_TO_DASHBOARD` | `BLOCKED_BY_VISIBILITY_OWNER_GAP` | Dashboard source mapping correction. |
| Dashboard -> Operator -> OMP | Operator-visible state can be traced to canonical owners and any operator question returns through ECR/OMP. | Dashboard authority check, source owner, operator/engineering observation if any. | `BROKEN_DASHBOARD_TO_OMP` | `BLOCKED_BY_NON_CANONICAL_VISIBILITY` | Remove display, fix owner mapping, or route observation through ECR. |

After every meaningful OMP step, OMP must verify:

- output was produced;
- output is available to the named consumer;
- the named consumer exists;
- the named consumer consumed the output;
- consumption was verified;
- consumer behavior changed;
- next output was produced;
- downstream consumer exists;
- terminal consumer is verified;
- verification evidence exists;
- Behavior Chain Status is recorded.

If verification fails, OMP must not declare the step complete.
It must record `PARTIAL`, `BLOCKED`, `BROKEN`, or `UNKNOWN` with failure condition and recovery path.

### Autonomous Engineering Cycle Execution Certification Ladder

Status: `CANONICAL_OMP_EXTENSION`
Owner: `OMP`
Mode: `EXISTING_OWNER_PATH_ONLY`
Need New Program: `FALSE`
Need New Owner: `FALSE`
Runtime impact: `NONE_BY_DEFAULT`
Production impact: `NONE_BY_DEFAULT`
Authority impact: `NONE_BY_DEFAULT`

The Autonomous Engineering Cycle Execution Certification Ladder reuses OMP Behavior Enforcement, BDP Implementation Candidate Consumption, Mission Formation, Verification, Engineering Report, Knowledge Promotion, Current Program State update, OMP update, and existing canonical owner paths.

It is not a new program, roadmap, queue, Runtime, Planner, owner, truth source, architecture, or implementation backlog.

Purpose:

```text
Prove that BDP-derived Implementation Candidate Instances can move through:

BDP
  -> OMP
  -> Mission
  -> Codex
  -> Implementation / No-Change / Hold
  -> Verification
  -> Outcome
  -> Learning / No-Change
  -> Engineering Report
  -> Canonical Knowledge / CPS / SYSTEM_MAP update-or-no-change
  -> Reality refresh-or-no-change
  -> AEP re-consumption-or-no-change
```

The ladder exists because a structurally valid autonomous engineering cycle is not complete until concrete BDP-derived Candidate Instances are consumed by OMP and carried to legal terminal states with verified consumption.

#### Ladder Ownership Decision

OMP owns this ladder because:

- BDP discovers and packages Candidate Instances but must not create Missions or execute work;
- AEP routes strategic evolution but must not become the execution program;
- Production Maturity consumes maturity impact but must not approve implementation or Runtime action;
- Controlled Production Certification Program owns production/user-movement certification ladders, not documentation-only engineering-cycle proof;
- OMP already owns candidate admission, mission formation, implementation discipline, verification, report lifecycle, knowledge promotion, CPS update, and continuation.

#### Ladder Levels

| Level | Required BDP-derived Candidate Instances | Purpose | Scope Limit |
| --- | ---: | --- | --- |
| `L1` | `1` | Prove one complete candidate cycle. | Prefer read-only, documentation/canonical sync, verification/no-change, report consumption, or CPS/report automation. |
| `L2` | `2` | Prove repeatability across two independent Candidate Instances. | No production mutation unless existing authority already permits it. |
| `L3` | `5` | Prove small batch repeatability and duplicate handling. | Cohort only if OMP Cohort Safety passes. |
| `L4` | `10` | Prove medium batch repeatability and report/learning throughput. | Must preserve per-Instance terminal status. |
| `L5` | `25` | Prove large engineering-cycle throughput under existing owners. | Requires explicit STOP_SAFE, rollback/no-change, and consumer synchronization evidence. |
| `L6` | `continuous mode` | Prove sustained cycle operation through OMP continuation. | Must not bypass OMP admission, authority, verification, or owner consumption. |

#### Per-Level Common Contract

Every level must consume certified candidate evidence for every Candidate Instance.

Execution Certification does not independently revalidate the Implementation Candidate Instance contract. Candidate reality is certified by BDP, and candidate admissibility is certified by OMP admission. Behavior completion is certified by the existing Behavior Enforcement Framework. The ladder verifies only that those certified results exist and may be used as Execution Ladder evidence.

| Field | OMP rule |
| --- | --- |
| Entry Criteria | Previous level passed or L1 selected; candidate has required BDP / OMP certificates and is not a duplicate active Mission according to OMP admission evidence. |
| Candidate Selection Rule | Prefer lowest-risk candidate that proves the missing engineering-cycle link; read-only/no-change/documentation synchronization before runtime or production work. |
| Candidate Identity / Deduplication Rule | Consume OMP identity and duplicate-check evidence. Execution Certification must not resolve identity independently. |
| OMP Admission Rule | Consume an existing OMP Admission Decision or route the candidate to OMP admission before counting it. Execution Certification must not rerun BDP Candidate Reality Gate or OMP admission checks as a third validator. |
| Mission Creation Rule | Mission may be created only after OMP admission. A held, rejected, duplicate, merged, or not-applicable candidate is a legal terminal alternative only when evidence is recorded. |
| Codex Boundary | Codex may act only as assigned implementation assistant for the admitted Mission and must not become owner, Runtime, Planner, Authority, or truth source. |
| Implementation / No-Change / Hold Path | Produce implementation, explicit no-change, hold, rejection, or not-applicable result through existing owners. |
| Verification Rule | Verify schema/docs/tests/runtime/owner state as required by task class; missing verification blocks PASS. |
| Rollback / STOP_SAFE Rule | Runtime or production-affecting candidates require rollback/STOP_SAFE before implementation. Documentation-only candidates may record `ROLLBACK_NOT_APPLICABLE_WITH_REASON`. |
| Outcome Rule | Classify as success, partial, no-change, failure, blocked, or not applicable. |
| Learning / No-Change Rule | Record learning, no-change, insufficient evidence, blocker, or not applicable; Learning cannot mutate Runtime or authority. |
| Engineering Report Rule | Every meaningful ladder action must create an Engineering Report with candidate, admission, execution, verification, outcome, learning, owner consumption, and terminal state. |
| CPS / Canonical / SYSTEM_MAP Rule | Update only when the existing owner requires it; otherwise record explicit no-change with reason. |
| Reality Refresh Rule | Refresh Reality only from verified evidence or record `REALITY_NO_CHANGE_WITH_REASON`. |
| AEP Re-Consumption Rule | AEP re-consumption is satisfied by changed Reality, explicit no-change, or terminal alternative evidence routed through existing owners. |
| Exit Criteria | Required number of Candidate Instances reached legal terminal state with verified consumption according to Behavior Enforcement Framework evidence. |
| PASS Criteria | All required instances satisfy Behavior Chain Status `COMPLETE`, or have a legal terminal consumer with `Terminal Consumer Verified = PASS`, and have all required BDP / OMP certificates. |
| HOLD Criteria | One or more candidates are valid but blocked by dependency, evidence, authority, verification, rollback, Runtime, production, owner, or consumer. |
| FAIL Criteria | Candidate violates architecture, owner, Runtime, Planner, authority, production, evidence, or chain-closure rules; or required consumption cannot be proven. |

#### Automatic-First Rule

Execution Certification must be automatic wherever the candidate is machine-checkable and owner-mapped.

Manual gates are legal only when the existing architecture already requires them:

- authority boundary;
- security boundary;
- production mutation;
- Runtime apply;
- user movement;
- rollback/containment risk;
- owner acceptance where no machine-checkable owner state exists.

If a manual gate is found where all required conditions are machine-checkable and owner-mapped, OMP must classify it as:

```text
AUTOMATION_BREAK
```

and may package it as a future BDP Implementation Candidate. OMP must not normalize unnecessary manual certification.

#### Post-PASS Self-Continuation Rule

Execution Certification Ladder is a self-continuing Engineering Chain.

A level `PASS` is not a ladder stop.

After any level returns `PASS`, OMP must automatically determine the next level and attempt to continue without waiting for operator direction.

Canonical continuation:

```text
L1
  -> PASS
  -> automatic L2 continuation check
  -> L2 certified candidate evidence consumption / selection / OMP admission evidence / mission / execution / verification / report / owner consumption
  -> PASS
  -> automatic L3 continuation check
  -> ...
  -> L6 continuous mode
```

OMP must not write `Prepare L2`, `Next allowed step`, `operator should decide`, or any equivalent non-terminal handoff after a level `PASS` unless a canonical OMP stop is present and recorded.

After every level `PASS`, OMP must automatically:

1. determine the next ladder level;
2. determine the required number of independent Candidate Instances;
3. find certified BDP-derived Candidate Instance records from accepted BDP output and OMP admission evidence; existing Reality, reports, Function Graph evidence, CPS, Canonical Knowledge, and owner paths may point to those records but must not be counted as candidates by themselves;
4. if certified candidates are insufficient, invoke BDP minimal Discovery Economy mode to produce only the missing bounded Candidate Instances for OMP admission;
5. consume Candidate Identity Resolution evidence from OMP;
6. consume duplicate / merge / Cohort Safety evidence from OMP where applicable;
7. verify that OMP Admission Decision exists;
8. create Mission or legal terminal alternative only through OMP;
9. execute through Codex / existing owner only when no canonical stop is present;
10. verify;
11. consume Behavior Chain Status from the existing Behavior Enforcement Framework;
12. count Execution Candidate Evidence only when Behavior Chain Status is `COMPLETE` or legal terminal consumer verification is `PASS`;
13. record outcome;
14. record Learning / no-change / insufficient-evidence state;
15. create Engineering Report;
16. update or explicitly no-change CPS / Canonical Reference / SYSTEM_MAP / Production Maturity / affected owner;
17. refresh Reality or explicitly record `REALITY_NO_CHANGE_WITH_REASON`;
18. record AEP re-consumption or explicit `AEP_RECONSUMPTION_NO_CHANGE_WITH_REASON`;
19. continue to the next level.

If an already discovered candidate is not sufficient for the next level, lack of ready candidates is not a stop by itself. It triggers BDP minimal Discovery Economy mode.

BDP minimal Discovery Economy mode must:

- avoid unnecessary full Discovery;
- search only for enough bounded Candidate Instances to satisfy the next ladder level;
- preserve BDP boundaries;
- produce Candidate Instances, hold reasons, or legal terminal alternatives;
- return output to OMP for admission.

OMP must not run BDP Discovery itself. OMP may invoke or consume BDP output through the existing AEP / BDP / OMP route.

#### Engineering Polygon Scenario Supply Consumption Rule

Status: `CANONICAL_EXISTING_OWNER_INTEGRATION`

When the L6 continuous lane has no current BDP Candidate, the existing Engineering Plane consumer must evaluate bounded scenario sources before returning a production `REAL_WORLD_LIMIT` terminal. Source evaluation reuses current owner validators and canonical contracts; it is not a new discovery program or scenario lifecycle.

Canonical route:

```text
fresh CPS and repository truth
  -> existing owner-backed scenario surfaces
  -> deterministic bounded scenario selection
  -> existing BDP Reality Gate
  -> Candidate or rejection
  -> existing OMP identity / eligibility / admission
  -> Mission lifecycle or legal terminal
```

Only an active, concrete failure or verification gap with owner, producer, consumer, current/expected reality, bounded implementation scope, verification and rollback/STOP_SAFE may become a Scenario Instance. Documents, reports, tests, validators, owners and historical defects are context only unless they prove a current uncovered occurrence. Production-only evidence is excluded and cannot earn Production Maturity or Authority.

Selection is serial and deterministic: current truth contradiction; safety/rollback/STOP_SAFE; producer/consumer break; replay/duplicate; dependency/authority boundary; uncovered canonical rule; uncovered historical defect; ladder coverage; then lower-priority engineering quality. The selector prepares BDP input only. BDP remains Candidate producer, OMP remains admission/Mission owner, and Codex remains bounded implementation consumer.

If every source class is evaluated and no valid current Engineering Plane occurrence exists, the legal scenario result is `NO_VALID_ENGINEERING_SCENARIO`. Only after that result may the unchanged capability frontier return `REAL_WORLD_EVIDENCE_REQUIRED_AFTER_ENGINEERING_SCENARIO_EXHAUSTION`.

#### Proactive Verification Input Consumption Rule

Status: `CANONICAL_EXISTING_OWNER_INTEGRATION`

Before the L6 continuous lane declares engineering-only scenario supply exhausted, it may execute bounded proactive verification inputs owned by existing test, replay, rollback, recovery, STOP_SAFE, truth, dependency and producer/consumer verification surfaces.

Canonical route:

```text
existing owner-backed verification obligation
  -> deterministic bounded input selection
  -> existing verification entrypoint
  -> observed current behavior
  -> PASS_CURRENT with no Scenario
  OR
  -> reproducible current contract mismatch
  -> Engineering Polygon Scenario Instance
  -> BDP Reality Gate
  -> OMP identity / eligibility / admission
  -> prepared Mission or legal terminal
```

A report, historical defect, policy, test name, validator name or missing production evidence is not executable input by itself. The input must name an existing owner, executable entrypoint, target contract, expected behavior, observation method, result consumer, pass/fail criteria and revalidation trigger. Runtime and production mutation, Authority expansion, user movement, packet apply, restore-barrier write and Production Maturity credit are forbidden.

Selection is serial and deterministic: STOP_SAFE/safety negative paths; rollback/partial failure; current truth; producer/consumer confirmation; replay/duplicate; dependency order; recovery; authority/runtime/production boundary; executable historical regression; canonical coverage obligation; then engineering quality. One input is consumed per iteration. PASS creates no Scenario or Candidate. A flaky, unowned, unconsumed or boundary-crossing result stops safely. Only a reproducible current failure may use the existing result-to-scenario adapter.

Coverage remains evidence under existing verification, OMP and report owners; it does not create a new registry. A previous PASS is current only until its owner-defined implementation, fixture, contract or dependency invalidation trigger fires. When the bounded input budget is reached, the legal stop is `PROACTIVE_INPUT_BUDGET_EXHAUSTED`; when all current proactive inputs and active scenario sources are exhausted, the unchanged capability frontier may return `REAL_WORLD_EVIDENCE_REQUIRED_AFTER_PROACTIVE_VERIFICATION_EXHAUSTION`.

#### Engineering Polygon Fallback Continuation Rule

Status: `CANONICAL_EXISTING_OWNER_INTEGRATION`

A finite seed list cannot prove Engineering Polygon exhaustion. When fresh CPS has no READY capability, active Mission, Candidate, actionable real situation or active Engineering Polygon Scenario, the existing L6 consumer must discover the current safe executable verification corpus through mapped existing owners before returning a global `REAL_WORLD_LIMIT`.

Canonical route:

```text
fresh CPS and dependency truth
  -> deterministic existing-owner corpus discovery
  -> safety and environment exclusion with exact reason
  -> source / fixture / contract / owner / dependency fingerprint
  -> FAIL_CURRENT, STALE or NOT_EVALUATED first
  -> bounded serial verification
  -> PASS_CURRENT and automatic next input
  OR reproducible current mismatch -> Scenario -> BDP -> OMP admission
  OR budget boundary with exact next input preserved
  OR proven full-current-corpus exhaustion
```

Corpus order and identity must be deterministic and independent of filesystem enumeration order. Duplicate obligations are suppressed. A prior PASS is reusable only while its full revalidation fingerprint remains current. Unsafe, external, ambiguous, production-mutating or unmapped inputs are excluded with an explicit classification and do not count as evaluated coverage.

Normal OMP work always preempts this fallback. The fallback may not create a queue, scheduler, registry, owner, Engine, Runtime, Planner, lifecycle, Authority, packet, Candidate or production evidence. It may not mutate Runtime, move users, write restore barriers, expand blast radius or earn Production Maturity.

`PROACTIVE_INPUT_BUDGET_EXHAUSTED` is a continuation boundary, not a program terminal: the compact next-input projection must be materialized for the next existing OMP invocation. `REAL_WORLD_EVIDENCE_REQUIRED_AFTER_FULL_CURRENT_CORPUS_EXHAUSTION` is legal only when discovery is complete, every eligible current input is `PASS_CURRENT` or legally not applicable, no stale or unevaluated input remains, and no current Scenario was produced.

#### Future-Scale Scenario Engineering Contract

Status: `CANONICAL_EXISTING_OWNER_INTEGRATION`

Ordinary OMP work has priority: active Mission, accepted Candidate, READY capability, stale real verification and open safe Engineering Intent must be consumed before synthetic scenario work. When that ordinary frontier is exhausted, OMP must inspect the Scenario Frontier immediately and must not return a global `REAL_WORLD_LIMIT` while an uncovered or stale safe scenario exists.

Canonical route:

```text
program_execution_reconciliation
  -> ordinary frontier evaluation
  -> Future-Scale Scenario Frontier
  -> deterministic scenario identity and invariant binding
  -> exact next scenario
  -> existing OMP consumer
  -> FSSE execution-harness next output or legal stop
```

Scenario, replay, load, emulation and fault-injection results are `ENGINEERING_SCENARIO_EVIDENCE`. They may reveal defects, produce BDP inputs, justify bounded code repair, and certify invariant, scale or concurrency behavior. They may not claim real user/provider behavior, grant Runtime or action-class Authority, increase Production Maturity, count as a production outcome, mutate Runtime or move users.

A scenario is legal only when it has deterministic identity/version/seed/fingerprint, future-scale relevance, risk and engineering-value classes, stable invariant IDs, existing responsible owners, source and owner dependency bindings, expected legal terminals and explicit forbidden effects. Meaningless synthetic activity is forbidden.

A previous PASS becomes stale when any bound scenario input, source, consumer, invariant, policy, topology model, generator, dependency or authority rule changes. Frontier exhaustion requires all eligible critical scenarios covered, stale results replayed, reproducible mismatches routed, the bounded budget consumed or a legal stop proven, and no higher-priority safe scenario remaining.

Priority is deterministic and ordinal: safety; route loss/isolation; correlated failure; capacity collapse; stale/contradictory state; recovery/rollback; duplicate/replay/concurrency; future-scale coverage; performance; low-risk optimization. Ordinary OMP work always preempts this ordering.

A reproducible mismatch must flow without report transcription:

```text
Scenario Result
  -> invariant violation
  -> deterministic reproduction
  -> BDP input
  -> Candidate
  -> OMP Mission
```

Scenario batches and repair cycles continue internally inside the active OMP execution. External heartbeat is not an interval between scenario steps. Machine decisions are limited to `SCENARIO_FRONTIER_AVAILABLE`, `SCENARIO_FRONTIER_EXHAUSTED`, `SCENARIO_RESULT_STALE`, `SCENARIO_READY`, `SCENARIO_MISMATCH`, `SCENARIO_BUDGET_REACHED`, `SCENARIO_STOP_SAFE`, `ORDINARY_FRONTIER_SELECTED`, `SCENARIO_FOUNDATION_READY_EXECUTION_HARNESS_REQUIRED`, and `EXTERNAL_REALITY_REQUIRED_AFTER_ENGINEERING_EXHAUSTION`.

High-fidelity validation reuses the same owners to execute a bounded deterministic corpus through real code paths. It may generate scale cases, measure phase cost and resource envelopes, exercise existing lease/replay/concurrency/containment owners, bind results to source dependencies and selectively replay only invalidated scenarios. Its aggregate result is consumed by `OMP_PROGRAM_EXECUTION_RECONCILIATION`; complete current coverage with zero reproducible mismatch produces `V7_OMP_FUTURE_SCALE_AUTONOMOUS_POLYGON_INTEGRATION_AND_CERTIFICATION_V1`. These results remain engineering evidence and never become production outcomes or hardware-equivalent capacity claims.

The standard `Continue OMP` consumer may execute multiple internal safe transitions in one invocation. Every transition has a deterministic identity, bounded budget, atomic CPS update and post-write reread. Transaction PASS, selective invalidation, Scenario consumption, BDP input, Candidate admission, certification repair and affected replay do not return control while a safe next internal action remains. A bounded invocation terminal persists exact `CONTINUE_OMP` state. The existing Codex Automation Platform heartbeat owns the separately certified external reentry boundary and may invoke the standard consumer only after exact identity, replay, concurrency, freshness and CPS gates pass.

#### Execution Certification Candidate Certificate Consumption Rule

Status: `CANONICAL`

This rule replaces duplicate Execution Certification eligibility checking. It is not a new gate, owner, entity, program, or architecture.

Execution Certification Ladder may count only certified BDP-derived Implementation Candidate Instances.

Execution Certification does not validate whether a record is a valid Implementation Candidate Instance. That responsibility is already owned by:

```text
BDP
  -> Candidate Reality Gate
  -> OMP
  -> Implementation Candidate Eligibility / Admission
```

Execution Certification verifies only whether the already certified Candidate Instance has the right to be used as Execution Ladder evidence.

It also consumes the existing Behavior Enforcement Framework result as the only canonical proof that the Candidate really propagated through Producer, Consumer, Behavior Change, Next Output, and legal Terminal Consumer.

Execution Certification has no independent completion model.

Owner responsibility:

| Responsibility | Owner |
| --- | --- |
| Candidate reality | BDP Candidate Reality Gate |
| Candidate schema / current-reality / expected-reality evidence | BDP Candidate Reality Gate |
| Candidate identity | OMP Candidate Identity Resolution |
| Candidate admissibility | OMP Implementation Candidate Admission |
| Terminal path | OMP admission / legal terminal alternative |
| Mission or legal terminal alternative | OMP |
| Behavior Chain completion | Behavior Enforcement Framework |
| Legal terminal consumer verification | Behavior Enforcement Framework |
| Use as Execution Ladder evidence | Execution Certification Ladder |

Execution Certification must not re-analyze the following candidate substance when certified by BDP or OMP:

- Engineering Chain;
- Behaviour;
- Engineering Intent;
- Reality;
- Authority;
- Verification;
- Terminal Path;
- Current Reality;
- Expected Reality;
- owner / consumer suitability;
- implementation readiness;
- evidence sufficiency.

Execution Certification must not independently verify the following Behavior Enforcement substance when certified by the Behavior Enforcement Framework:

- Behavior;
- Producer;
- Consumer;
- Output Produced;
- Output Available;
- Consumer Consumed Output;
- Consumption Verified;
- Behavior Changed;
- Next Output Produced;
- Terminal Consumer;
- Terminal Consumer verification.

A Candidate Instance may be counted as Execution Candidate Evidence only when all certificate requirements are true:

| # | Consumption requirement |
| ---: | --- |
| 1 | `BDP Candidate Reality Gate = PASS`. |
| 2 | `OMP Admission = PASS` or equivalent OMP admission / legal terminal alternative certificate. |
| 3 | `Candidate Identity = RESOLVED`. |
| 4 | `Candidate Terminal Path = RESOLVED`. |
| 5 | `OMP Admission Decision = EXISTS`. |
| 6 | `Behavior Chain Status = COMPLETE`, or legal terminal consumer exists with `Terminal Consumer Verified = PASS`. |

If any required certificate is missing, Execution Certification must not count the record as Execution Candidate Evidence for L2-L6 certification.

Missing certificate outcomes:

| Outcome | Meaning |
| --- | --- |
| `EXECUTION_EVIDENCE_MISSING_BDP_REALITY_CERTIFICATE` | BDP Candidate Reality Gate PASS evidence is missing. Route back to BDP output, not Execution Certification validation. |
| `EXECUTION_EVIDENCE_MISSING_OMP_ADMISSION_CERTIFICATE` | OMP admission / legal terminal alternative evidence is missing. Route to OMP admission, not Execution Certification validation. |
| `EXECUTION_EVIDENCE_MISSING_IDENTITY_RESOLUTION` | OMP Candidate Identity Resolution evidence is missing. Route to OMP identity resolution, not Execution Certification validation. |
| `EXECUTION_EVIDENCE_MISSING_TERMINAL_PATH` | OMP terminal path evidence is missing. Route to OMP admission / terminal alternative resolution. |
| `EXECUTION_EVIDENCE_MISSING_ADMISSION_DECISION` | No OMP admission decision exists. The candidate cannot be counted until OMP records one. |
| `EXECUTION_EVIDENCE_MISSING_BEHAVIOR_CHAIN_COMPLETION` | Behavior Chain Status is `PARTIAL`, `BLOCKED`, `BROKEN`, or `UNKNOWN`. The candidate cannot be counted until Behavior Enforcement records `COMPLETE` or legal terminal consumer verification. |
| `EXECUTION_EVIDENCE_MISSING_TERMINAL_CONSUMER_VERIFICATION` | A legal terminal consumer is claimed but `Terminal Consumer Verified = PASS` is missing. |

Certificate consumption lifecycle:

```text
BDP Candidate Reality Gate PASS
  -> OMP Eligibility / Admission PASS or legal terminal alternative
  -> Candidate Identity RESOLVED
  -> Candidate Terminal Path RESOLVED
  -> OMP Admission Decision EXISTS
  -> Behavior Chain Status COMPLETE or Terminal Consumer Verified PASS
  -> Execution Candidate Evidence COUNTABLE
```

Execution Certification may inspect certificate identifiers, status, owner, source, timestamp / report pointer, Behavior Chain Status, terminal consumer verification status, and provenance pointer. It must not perform a parallel field-by-field candidate or behavior-chain validation.

#### Negative Candidate Rule

Canonical owners, models, documents, reports, indexes, and context artifacts may support Candidate evidence.

They must never be counted as Candidate Instances or Execution Candidate Evidence by themselves.

They are excluded because they cannot carry both required owner certificates:

```text
BDP Candidate Reality Gate PASS
OMP Admission Decision EXISTS
```

Forbidden as Candidate Instances:

- OMP;
- CPS;
- SYSTEM_MAP;
- Canonical Reference;
- Runtime Model;
- Decision Model;
- Function Graph;
- Engineering Chain Model;
- Engineering Entity Model;
- AEP;
- AOS;
- BDP program document;
- STOP condition;
- Engineering Report lifecycle;
- Production Maturity Model;
- any source of knowledge by itself;
- any owner by itself;
- any report by itself;
- any document section by itself.

Correct usage:

```text
Context artifact
  -> evidence/source/owner/consumer/provenance
  -> supports a real Candidate Instance
```

Incorrect usage:

```text
Context artifact
  -> counted as Candidate Instance
```

If a previous ladder run counted context artifacts as Candidate Instances, OMP must invalidate that run for candidate semantics, preserve it as historical evidence, correct CPS, and require a valid BDP-derived rerun.

#### Canonical Ladder STOP Conditions

Execution Certification Ladder may stop only at a canonical OMP stop condition.

Allowed stops:

| Stop | Meaning |
| --- | --- |
| `STOP_SAFE` | Safety, rollback, verification, runtime, evidence, or no-action safety requires a safe stop. |
| `ENGINEERING_AUTHORITY` | Capability, policy, authority, action-class, runtime capability, autonomous policy, or blast-radius approval is required. |
| `OPERATIONAL_AUTHORITY` | Exact restore-barrier write, runtime apply, rollback apply, user movement, packet execution, or other exact production action approval is required. |
| `REAL_WORLD_LIMIT` | Required evidence can be produced only by a real-world condition or observation that cannot be synthesized. |
| `UNSAFE_IMPLEMENTATION` | Existing implementation path is unsafe, incomplete, contradictory, or loses required state. |
| `FUNDAMENTAL_ARCHITECTURE_GAP` | Existing certified owners cannot satisfy the requirement after reuse/extension is proven impossible. |
| Existing OMP stop | Another OMP stop already defined by OMP, Runtime, Authority, Verification, Production Maturity, or CPS and resolved to a legal terminal state. |

Forbidden stops:

- level `PASS`;
- report created;
- recommendation written;
- operator handoff without authority boundary;
- no ready candidate before minimal BDP Discovery Economy;
- dashboard/read-model visibility;
- future work;
- TODO;
- convenience;
- uncertainty without owner/evidence classification.

If continuation stops for any forbidden reason, OMP must classify the stop as:

```text
AUTOMATION_BREAK
```

and create or consume an Implementation Candidate through the existing BDP -> OMP chain.

#### L1 Safe Candidate Preference

L1 must select the first safe BDP-derived Candidate Instance using this order:

1. read-only;
2. documentation/canonical synchronization;
3. Engineering Report automation;
4. verification/no-change automation;
5. CPS/report consumption automation;
6. non-production-affecting;
7. no user movement;
8. no Runtime mutation;
9. no authority expansion.

If no existing Candidate Instance is ready, BDP may run in minimal Discovery Economy mode only to identify one bounded Candidate Instance. BDP must not perform unnecessary full Discovery.

#### Ladder Level Verdicts And Continuation Semantics

Allowed level verdicts:

| Verdict | Meaning |
| --- | --- |
| `EXECUTION_CERTIFICATION_LADDER_READY` | Ladder definition exists and L1 has a selected candidate or legal Mission Proposal. This is not a stop if L1 can run automatically. |
| `EXECUTION_CERTIFICATION_L1_PASS` | One BDP-derived Candidate Instance completed the full cycle or legal terminal alternative with verified consumption. This automatically triggers L2 continuation check. |
| `EXECUTION_CERTIFICATION_L2_PASS` | Two BDP-derived Candidate Instances completed the required cycle or legal terminal alternatives. This automatically triggers L3 continuation check. |
| `EXECUTION_CERTIFICATION_L3_PASS` | Five BDP-derived Candidate Instances completed the required cycle or legal terminal alternatives. This automatically triggers L4 continuation check. |
| `EXECUTION_CERTIFICATION_L4_PASS` | Ten BDP-derived Candidate Instances completed the required cycle or legal terminal alternatives. This automatically triggers L5 continuation check. |
| `EXECUTION_CERTIFICATION_L5_PASS` | Twenty-five BDP-derived Candidate Instances completed the required cycle or legal terminal alternatives. This automatically triggers L6 continuation check. |
| `EXECUTION_CERTIFICATION_L6_CONTINUOUS` | Continuous mode is active and OMP continues until a canonical STOP. |
| `EXECUTION_CERTIFICATION_LEVEL_HOLD` | Current level is valid but blocked by existing owner, authority, evidence, verification, rollback, Runtime, production, or consumer condition. Hold must name the canonical stop or Automation Break. |
| `EXECUTION_CERTIFICATION_BLOCKED` | No legal existing-owner path can admit or terminally classify the candidate without architecture change. |

`PASS` is a level result, not a ladder terminal state.

Allowed ladder terminal states:

```text
L6_CONTINUOUS_MODE_ACTIVE
STOP_SAFE
ENGINEERING_AUTHORITY
OPERATIONAL_AUTHORITY
REAL_WORLD_LIMIT
UNSAFE_IMPLEMENTATION
FUNDAMENTAL_ARCHITECTURE_GAP
EXISTING_OMP_STOP_WITH_REASON
```

### State Transition Law

Status: `CANONICAL`

Every meaningful engineering process must end in exactly one of two states:

```text
State Transition Completed
```

or

```text
State Transition Explained
```

No third state is allowed.

A verified process is not complete unless:

- its behavior is verified; and
- its resulting system state is verified; or
- its inability to change system state is fully explained through existing owners, existing prerequisites, and the next executable OMP action.

State transition verification must distinguish:

- `STATE_PRODUCED`;
- `STATE_AVAILABLE`;
- `STATE_CONSUMED`;
- `STATE_CONSUMPTION_VERIFIED`;
- `NEW_STATE_PRODUCED`.

The required state transition shape is:

```text
State Produced
  -> State Available
  -> State Consumed
  -> Consumption Verified
  -> New State Produced
```

A state that was produced or displayed but not consumed by the next owner is not a completed state transition.

Every meaningful OMP step must answer:

| Question | Allowed values |
| --- | --- |
| Behavior Verified? | `YES`, `NO`, `PARTIAL`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| State Changed? | `YES`, `NO`, `PARTIAL`, `UNKNOWN`, or `NOT_APPLICABLE`. |

If `State Changed?` is `NO`, `PARTIAL`, or `UNKNOWN`, OMP must not stop at diagnosis.
OMP must produce Transition Analysis.

Transition Analysis must include:

| Field | Required value |
| --- | --- |
| Transition Blocker | Exact blocker, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Current State | Current owner-backed state. |
| Required State | State required for transition completion. |
| Missing Preconditions | Prerequisites that must become `TRUE`. |
| Responsible Owner | Existing owner responsible for the missing prerequisite. |
| Required Capability | Existing capability required for transition. |
| Required Evidence | Evidence required by existing owner/certification path. |
| Required Certification | Certification required before transition. |
| Reality Limit | Real-world limit preventing transition, or `NONE`. |
| Authority Limit | Authority boundary preventing transition, or `NONE`. |
| Engineering Limit | Engineering/capability limit preventing transition, or `NONE`. |
| Smallest Existing Next Action | Smallest executable next action through existing owner/backlog/capability/runtime/certification/authority model. |
| Expected State Transition | Next state expected if the action succeeds. |

Transition Preconditions Rule:

The system must identify which prerequisite must become `TRUE` before the state transition becomes possible.
It must not stop at symptoms.

Continue OMP Integration:

OMP must never terminate with diagnosis only.
When state cannot change, OMP must generate `Smallest Existing Next Action` using only:

- existing owners;
- existing backlog;
- existing capability;
- existing Runtime;
- existing certification;
- existing authority model.

If no executable next action exists inside current authority, OMP must record the smallest blocked next action and the exact authority, evidence, certification, or owner prerequisite that must become true.

Automatic stop conditions:

| Condition | Stop meaning |
| --- | --- |
| Operator authority required | Stop with exact engineering or operational authority decision. |
| Runtime apply required | Stop before apply or irreversible production action. |
| Production movement required | Stop before user movement. |
| Architecture contradiction discovered | Stop through Architecture Closed by Default and Root Cause Engine. |
| Canonical owner missing | Stop with Need New Owner audit result; default remains `FALSE`. |
| Re-open trigger fired | Stop or branch into the existing owner re-audit path. |
| Product contradiction discovered | Stop and map to Product Specification owner. |

Automatic continue conditions:

| Condition | Continue behavior |
| --- | --- |
| Only implementation remains | Continue through existing backlog item. |
| Only documentation remains | Continue through existing canonical owner or report lifecycle. |
| Only integration remains | Continue through existing owner integration. |
| Only certification remains | Continue through existing certification path. |
| Only verification remains | Continue through relevant verification owner. |
| Only knowledge promotion remains | Continue through canonical update path. |

This command creates no new owner, planner, governance layer, runtime path, truth source, roadmap, backlog, daemon, timer, apply authority, or user movement authority.

## 2.1.1. Implementation Phase Rule

Architecture Phase is complete.
Research Phase is complete.
Decision Model is complete.
Runtime Model is complete.
System Architecture is complete.

From V3.0 forward, OMP optimizes implementation, not architecture.

From V4.0 forward, OMP is the single permanent production execution program for V7.

The implementation optimizer asks:

```text
What implementation gives the highest production leverage right now?
```

OMP must not ask:

```text
What architecture is missing?
```

Architecture redesign, planner redesign, governance redesign, execution redesign, Runtime redesign, new truth sources, synthetic evidence, and new owners are forbidden unless a real implementation proves `FUNDAMENTAL_ARCHITECTURE_GAP`.

Implementation-first means:

1. choose the highest production-leverage implementation;
2. reuse the existing owner;
3. extend the existing owner only when required;
4. implement the smallest safe increment;
5. test;
6. verify;
7. certify;
8. update Current Program State;
9. update OMP only if optimizer meaning changed;
10. continue automatically until an allowed stop condition.

Reference program: `docs/programs/V7_IMPLEMENTATION_PROGRAM.md`.
Reference model: `docs/reference/V7_IMPLEMENTATION_MODEL.md`.

These files are supporting implementation references under OMP. They are not separate roadmap authorities.

## 2.1.2. Permanent Production Maturity Ladder

OMP owns the complete autonomy roadmap.

No additional roadmap document is required.

| Tier | Name | Scope | Status |
| --- | --- | --- | --- |
| 0 | Architecture foundation | Architecture, Research, Decision Model, Runtime Model, System Architecture. | `COMPLETE` |
| 1 | Governed implementation | Implementation, existing owner integration, testing, certification, production deployment, one-user governed canary, outcome closure, learning. | `ACTIVE` |
| 2 | Low-risk autonomous execution | Only actions proven safe; only bounded blast radius; rollback mandatory; verification mandatory; learning mandatory; no authority expansion without certification. | `LOCKED_UNTIL_CERTIFIED` |
| 3 | Small-batch autonomy | Multiple bounded users/actions only after Tier 2 evidence proves safety, rollback, verification, and learning. | `FUTURE_CERTIFIED_STEP` |
| 4 | Operational autonomy | Runtime performs routine production actions automatically inside certified policy and blast-radius limits. | `FUTURE_CERTIFIED_STEP` |
| 5 | Production autonomy | Operator supervises; Runtime operates; OMP optimizes production leverage and safety. | `FUTURE_CERTIFIED_STEP` |
| 6 | Authority evolution | After every certified outcome, OMP evaluates whether authority should remain unchanged, shrink, or be proposed for expansion. | `PERMANENT_RULE` |
| 7 | Continuous implementation | OMP continuously searches for highest implementation leverage; Codex continuously implements until a stop condition. | `PERMANENT_RULE` |
| 8 | Continuous optimization | OMP continuously searches for performance, simplicity, reuse, latency, runtime cost, readability, testability, and operability improvements. | `PERMANENT_RULE` |
| 9 | Continuous knowledge evolution | Research Framework continues forever; only proven production engineering principles may change V7; research informs OMP. | `PERMANENT_RULE` |
| 10 | Production evolution | Runtime -> Outcome -> Learning -> OMP -> Implementation -> Runtime. | `PERMANENT_RULE` |

Tier progression is evidence-gated.

No tier expands authority automatically.

## 2.1.3. Authority Evolution Rule

After every successful certified outcome, OMP must evaluate:

1. can authority remain unchanged;
2. can authority shrink;
3. should authority expansion be proposed.
4. can packet-level approval be retired for the certified action class.

OMP may recommend authority expansion.

OMP must never silently expand authority.

Authority expansion requires explicit operator approval or certified policy approval.

If expansion is needed before safe continuation, OMP must stop at `ENGINEERING_AUTHORITY`.

Authority shrink may be recommended when verification, rollback, learning, or real outcomes show increased risk.

Packet-level approval is not the permanent product model.

The durable authority object is the Action Class.

Packets are runtime execution artifacts. They are fresh, bounded, validated, and ephemeral. A packet may execute only when it belongs to an already approved Action Class or when the class is still `GOVERNED_ONLY` and the operator explicitly approves the exact packet as a temporary governed fallback.

OMP must treat packet staleness as evidence that packet approval does not scale. Packet approval is acceptable for early governed proof, but it must be eliminated class-by-class after certification and explicit authority approval.

## 2.1.3.1. Authority Boundary Normalization

OMP must never expose raw `AUTHORITY_BOUNDARY` as the primary status.

Raw `AUTHORITY_BOUNDARY` is a legacy technical compatibility detail only. OMP must normalize it into one of two authority classes before reporting status, updating Current Program State, or asking for operator action.

| Authority Class | Meaning | Examples | OMP Status | Engineering Behavior |
| --- | --- | --- | --- | --- |
| `ENGINEERING_AUTHORITY` | Implementation cannot continue because engineering approval is required. | Authority expansion; new action class; new runtime capability; new autonomous policy; blast-radius expansion. | `Engineering Approval Required` | Engineering work pauses until approval or rejection. |
| `OPERATIONAL_AUTHORITY` | Engineering is complete, implementation is ready, Runtime is ready, and only one production operation requires approval. | Approve exact packet; approve exact rollback; approve exact production action. | `Production Action Ready` | Engineering continues after the production action is approved/rejected and closed. |

Authority classification rules:

| Raw blocker or situation | Normalized result |
| --- | --- |
| Exact packet approval | `OPERATIONAL_AUTHORITY` |
| Exact rollback approval | `OPERATIONAL_AUTHORITY` |
| Exact production action approval | `OPERATIONAL_AUTHORITY` |
| Authority expansion | `ENGINEERING_AUTHORITY` |
| New action class approval | `ENGINEERING_AUTHORITY` |
| New runtime capability approval | `ENGINEERING_AUTHORITY` |
| New autonomous policy approval | `ENGINEERING_AUTHORITY` |
| Blast-radius expansion | `ENGINEERING_AUTHORITY` |
| Implementation defect | `UNSAFE_IMPLEMENTATION` |
| Real-world evidence required | `REAL_WORLD_LIMIT` |

Current Program State must store:

- `authority_class`;
- `authority_reason`;
- `authority_owner`;
- `required_action`.

If the class is `ENGINEERING_AUTHORITY`, OMP must output:

```text
Status
Engineering Approval Required

Reason
...

Next engineering task
...
```

If the class is `OPERATIONAL_AUTHORITY`, OMP must output:

```text
Status
Production Action Ready

Authority
Operational

Packet
...

Required operator action
...
```

## 2.1.4. Autonomy Promotion Engine

The Autonomy Promotion Engine is the permanent OMP rule for how action classes become autonomous.

It governs action classes, not individual packets.

It is not runtime apply.
It is not authority expansion.
It is not packet execution.
It is not a new planner, governance layer, execution path, runtime owner, truth source, or authority engine.

The engine reuses OMP, Current Program State, Runtime Model, existing packet/restore/rollback/verification/outcome/learning owners, truth/convergence, ADRs, and certified reports.

Machine-readable Action-Class Runtime Enablement state is exposed through the existing read-only owners:

- `admin_core/autonomy_trust_acceleration.py::build_action_class_runtime_enablement_model`;
- `tools/v7-autonomy-trust-evidence-inventory --action-class-runtime-only`;
- `admin_core/operator_execution_pipeline.py::governed_canary_knowledge_gated_dry_run_cycle`.

These surfaces may classify, map, and recommend. They must not move users, write restore barriers, execute apply, expand authority, create evidence, create planners, create governance, create execution, or create truth sources.

Operator authority must evolve from:

```text
Approve Action Class
  -> Approve Authority Expansion
  -> Approve Product Policy
  -> Operator Supervision Only
```

`Approve Packet` remains only a temporary `GOVERNED_ONLY` fallback while an action class is not yet certified for class approval.
It is not the primary OMP authority model.

Every certified outcome must trigger Autonomy Promotion evaluation.

OMP must automatically ask:

```text
Can this action class move to the next autonomy state?
```

If yes, OMP must prepare a class promotion or authority expansion recommendation.

If no, OMP must state the exact missing evidence, verification, rollback/no-rollback quality, blast-radius certification, safety gate, freshness gate, anti-flap certification, learning quality, trust gap, authority policy, runtime owner path, or duplication blocker.

After every certified action class, OMP must also ask:

```text
Can packet approval for this class be permanently eliminated?
```

If yes, OMP must prepare an Authority Promotion recommendation that moves the class toward runtime capability.

If no, OMP must state the exact missing evidence that still requires packet-level governed fallback.

An action class may become autonomous only if all are true:

- real outcomes exist;
- verification passed;
- rollback/no-rollback path certified;
- blast radius certified;
- safety gates certified;
- freshness gates certified;
- anti-flap certified;
- authority policy approved;
- runtime path exists through existing owners;
- no duplicate planner, governance, execution, or truth is introduced.

Promotion is based only on:

- real outcomes;
- verification;
- rollback quality;
- safety;
- blast radius;
- learning;
- trust;
- authority policy.

Promotion must never be based on synthetic evidence.
Promotion must never be based on reports alone.

Autonomy Promotion loop:

```text
Observe
  -> Collect Outcomes
  -> Verify
  -> Measure
  -> Evaluate
  -> Recommend Promotion
  -> Operator approves CLASS
  -> Runtime capability updated
  -> Runtime generates fresh packets inside policy
  -> Future packets execute only when they match approved class authority
```

Action class states:

| State | Meaning |
| --- | --- |
| `NOT_CERTIFIED` | The class lacks enough evidence, certification, owner wiring, safety, freshness, rollback/no-rollback, blast-radius, learning, trust, or authority basis. |
| `GOVERNED_ONLY` | Temporary proof state. The class requires either explicit packet authority or an explicitly approved bounded governed-learning policy. The current one-user class uses the latter without class promotion. |
| `CERTIFIED_FOR_CLASS_APPROVAL` | The class has enough real evidence for OMP to recommend operator approval of the class, but Runtime must not execute it autonomously yet. |
| `CERTIFIED_FOR_BOUNDED_AUTONOMY` | The class has enough evidence and approved authority policy for bounded autonomous execution to be proposed. This still does not silently enable Runtime. |
| `AUTONOMOUS_RUNTIME` | Runtime may execute this class automatically inside explicitly approved policy, authority, blast-radius, freshness, safety, rollback/no-rollback, verification, and learning bounds. Packet-level operator approval is retired for the class. |

Canonical Action Classes:

- single-user failover;
- two-user failover;
- small batch movement;
- channel hard failure;
- channel degradation;
- recovery admission;
- service failover;
- rollback;
- packet generation;
- verification;
- outcome closure;
- learning refresh;
- other classes only if discovered through existing owners and added without duplicate planner, governance, execution, truth, or runtime ownership.

Action-class ladder:

| Action class | Current status | Required evidence | Required verification | Required rollback | Required blast radius | Required authority | Action class state |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1. Single-user governed candidate failover | TIER_1 governed path exists; one approved leased governed canary outcome has been executed, verified, closed, and learned from; fresh packets still stop at authority. | More real candidate suitability outcomes, service/user outcome, closure record, learning record, source confidence. | Immediate post-move service/user/channel verification plus truth/convergence. | Rollback target or certified no-rollback decision for the class, not only one packet. | Exactly one user. | Explicit operator approval for each exact packet until class approval exists. | `GOVERNED_ONLY` |
| 2. Two-user failover | Not certified. | Multiple successful one-user governed outcomes across comparable conditions. | Per-user and cohort verification. | Per-user rollback/no-rollback path. | Two bounded users only. | Class approval and authority expansion recommendation. | `NOT_CERTIFIED` |
| 3. Five-user failover | Not certified. | Certified two-user outcomes plus stronger candidate/source confidence. | Per-user, cohort, and service verification. | Batch rollback/no-rollback path. | Five bounded users only. | Class approval and authority expansion recommendation. | `NOT_CERTIFIED` |
| 4. Channel hard-fail failover | Read-only/event path exists; autonomous apply not certified. | Real hard-fail events, verified impact, successful governed failover outcomes. | Failure detection, target safety, post-failover service reachability. | Restore or alternate safe route certification. | Bounded affected users or cohort. | Certified policy approval or operator approval. | `GOVERNED_ONLY` |
| 5. Channel degradation failover | Read-only degradation evidence exists; autonomous apply not certified. | Real degradation events, freshness, anti-flap, recovery stage, governed outcomes. | Degradation confirmation and post-move improvement. | Restore/no-rollback decision with anti-flap protection. | Bounded affected users or cohort. | Certified policy approval or operator approval. | `GOVERNED_ONLY` |
| 6. Service-specific failover | Service matrix and service evidence exist; autonomous apply not certified. | Real service-specific failures and successful governed service-targeted outcomes. | Service reachability before/after action. | Service-safe rollback/no-rollback path. | Users affected by the service only. | Certified policy approval or operator approval. | `GOVERNED_ONLY` |
| 7. Recovery admission | Read-only recovery and anti-flap overlays exist. | Real recovery observations, no-flap windows, successful gradual admission outcomes. | Recovery stability and service/user quality checks. | Re-drain or no-rollback decision. | One channel, cohort, or bounded user set per policy. | Certified policy approval or operator approval. | `GOVERNED_ONLY` |
| 8. Small batch movement | Future certified step. | Certified one/two/five-user outcomes with strong suitability, safety, rollback, and learning. | Batch verification and per-user exception handling. | Batch rollback/no-rollback path. | Small certified batch only. | Class approval and authority expansion recommendation. | `NOT_CERTIFIED` |
| 9. Rollback | Existing rollback owner and previews exist; autonomous rollback apply is not broadly certified. | Real rollback/no-rollback outcomes and failure cases. | Post-rollback service/user/channel verification. | Rollback itself must be bounded and idempotent. | Same or smaller than failed action. | Explicit rollback authority or certified policy. | `GOVERNED_ONLY` |
| 10. Packet generation | Existing packet owner exists and is read-only/generation-safe. | Packet identity stability, selected move hash stability, lease behavior, stale invalidation. | Packet validation and identity checks. | N/A unless execution follows. | N/A until packet is executed. | Existing governed packet policy. | `GOVERNED_ONLY` |
| 11. Verification | Existing verification and truth/convergence owners exist. | Real verification results across executed actions. | Verification must prove action effect or inconclusive state. | N/A unless rollback follows. | N/A. | Existing verification policy. | `GOVERNED_ONLY` |
| 12. Outcome closure | Existing feedback/outcome owners exist. | Verified real outcomes and closure records. | Closure completeness and learning eligibility. | N/A. | N/A. | Existing outcome policy. | `GOVERNED_ONLY` |
| 13. Learning refresh | Existing learning/snapshot owners exist. | Verified outcome records only. | Refresh output and truth/convergence. | N/A. | N/A. | Existing learning policy. | `GOVERNED_ONLY` |

Runtime enablement end state:

```text
Certified Action Class
  -> Authority Promotion Recommendation
  -> Operator or certified policy approval
  -> Runtime capability
  -> Fresh packet generated immediately before execution
  -> Packet validated against approved class
  -> Execute or stop safely
```

Packet approval is not the promotion endpoint.
Runtime capability is the promotion endpoint.

Runtime must never depend on a long-lived packet approval for an autonomous or class-approved action.
Runtime must generate or consume a fresh packet immediately before execution and verify:

- action class match;
- authority match;
- policy match;
- subject and target class match;
- freshness;
- safety;
- rollback/no-rollback readiness;
- verification readiness;
- blast-radius bounds;
- no duplicate planner, governance, execution, or truth.

Stop rule:

If Autonomy Promotion requires runtime apply, exact restore-barrier write, exact user movement, or exact rollback apply, OMP must stop at `OPERATIONAL_AUTHORITY`.

If Autonomy Promotion requires class approval, authority expansion, product policy approval, daemon/timer enablement, event-consumer mutation, new runtime capability, autonomous policy approval, or blast-radius expansion, OMP must stop at `ENGINEERING_AUTHORITY`.

OMP must never silently enable runtime automation.

Current first certifiable Action Class:

`single-user governed candidate failover`

Current promotion state:

`GOVERNED_ONLY`

Current promotion target:

`CERTIFIED_FOR_CLASS_APPROVAL`

Evidence needed for next promotion state:

- more real one-user governed candidate outcomes across comparable conditions;
- repeated successful verification and outcome closure;
- certified rollback/no-rollback behavior for the class, not only one packet;
- sustained blast-radius, safety, freshness, and anti-flap certification;
- stronger suitability and source confidence;
- explicit operator approval for the class, or explicit bounded governed-learning policy authority, before packet-level approval can be removed.

Current runtime automation enabled:

`POLICY_BOUNDED_ONLY`

Current machine-readable path status:

`PARTIAL`

The path exists as a read-only registry, packet-to-action-class mapping, authority-to-action-class mapping, runtime capability view, promotion recommendation, and enablement readiness check through existing owners. It is not yet autonomous runtime authority.

## 2.1.5. Delegated Autonomy Policy Model

Delegated Autonomy Policy is the permanent model for replacing repetitive operator approval.

The operator approves bounded policy.
V7 may self-approve operational decisions only inside that approved policy.
V7 may not approve expansion of the policy.

Delegated Autonomy Policy is not runtime apply.
It is not user movement.
It is not authority expansion.
It is not a new planner, governance layer, execution path, runtime owner, truth source, or packet owner.

The policy must define:

- allowed action classes;
- max users per action;
- allowed failure types;
- required freshness;
- required verification;
- required rollback or certified no-rollback path;
- required anti-flap state;
- required suitability, trust, confidence, and prediction floors;
- max blast radius;
- cooldown;
- stop conditions;
- automatic downgrade rules;
- required reporting after action.

Autonomy modes:

| Mode | Meaning |
| --- | --- |
| `MANUAL_PACKET_APPROVAL` | Temporary early governed fallback. Operator approves exact fresh packets. |
| `CLASS_APPROVAL` | Operator approves durable action classes, but Runtime does not execute autonomously. |
| `DELEGATED_AUTONOMY` | Operator approves bounded policy; V7 may make operational decisions inside policy. |
| `PRODUCTION_AUTONOMY` | Operator supervises; Runtime performs routine certified work inside policy. |

Current default policy:

| Field | Value |
| --- | --- |
| Policy id | `dap_default_tier1_readonly` |
| Policy state | `APPROVED` |
| Current mode | `GOVERNED_ONLY` |
| Target mode | `DELEGATED_AUTONOMY` |
| Current action-class contract | `MISSING` |
| Allowed first class | `single-user governed candidate failover` |
| Max users per action | `1` |
| Max concurrent transactions | `1` |
| Candidate approval required | `NO` |
| Packet approval required | `NO` |
| Runtime apply enabled | `NO` |
| Authority expanded | `NO` |

The approved policy is a bounded reference for governed-learning execution; it
is not a current Runtime grant while the exact action-class contract is
missing. The existing policy owner must first issue a fresh scoped contract.
It does not promote the class, authorize another class, permit concurrency, or
increase blast radius. A fresh ephemeral packet, operation-scoped binding,
live safety gates, serial execution lease, verification, rollback/no-rollback,
outcome closure, learning, truth convergence, and final Safe Mode `OPEN`
remain mandatory. Engineering Authority remains mandatory for every policy
expansion.

Runtime may execute automatically only if all are true:

1. action belongs to an approved policy;
2. action class is certified, or policy explicitly allows governed learning mode;
3. fresh packet is generated immediately before execution;
4. packet matches policy;
5. rollback is ready;
6. verification is ready;
7. anti-flap passes;
8. blast radius is within policy;
9. evidence is not stale;
10. failure mode is known.

If any condition fails, Runtime must stop safely.

Self-approval rule:

- V7 may approve operational decisions inside approved policy.
- V7 may not approve policy expansion.
- V7 may not silently increase blast radius.
- V7 may not silently add new action classes.
- V7 may recommend expansion, but it cannot grant expansion.

Machine-readable Delegated Autonomy Policy state is exposed through the existing read-only owners:

- `admin_core/autonomy_trust_acceleration.py::build_delegated_autonomy_policy_preview`;
- `admin_core/autonomy_trust_acceleration.py::build_delegated_autonomy_runtime_eligibility`;
- `admin_core/autonomy_trust_acceleration.py::build_action_class_runtime_enablement_model`;
- `tools/v7-autonomy-trust-evidence-inventory --delegated-autonomy-policy-only`;
- `tools/v7-autonomy-trust-evidence-inventory --delegated-autonomy-eligibility-only`;
- `tools/v7-autonomy-trust-evidence-inventory --action-class-runtime-only`.

## 2.1.6. Decision Explainability

Decision Explainability is the permanent OMP capability for explaining existing decisions before any operator approval request.

It is an explainability layer only.
It does not change decision making.
It does not create a new planner.
It does not create new governance.
It does not create a new Runtime owner.
It does not create a new execution path.
It does not approve packets, approve action classes, expand authority, write restore barriers, apply, roll back, move users, create evidence, or lower floors.

Purpose:

The operator must approve a decision, not a packet.

Before any approval request, Runtime / OMP must explain the decision in human language using existing decision, evidence, policy, safety, rollback, and authority owners.

Operator explanations must be written only in Russian.

Every approval request must answer:

1. Почему вообще рассматривается переключение?
2. Почему именно сейчас?
3. Почему выбран именно этот пользователь?
4. Почему текущий канал считается недостаточно хорошим?
5. Почему выбран именно этот целевой канал?
6. Какие проверки уже прошли успешно: Hard Failure, Soft Degradation, Freshness, Recovery Admission, Blast Radius, Rollback, Anti-Flap, Authority, State Change Cost, Net Benefit?
7. Почему система считает, что лучше переключить, чем оставить как есть?
8. Что произойдет, если ничего не делать?
9. Что произойдет после переключения?
10. Какие риски остаются?
11. Почему Runtime уверен в этом решении?
12. Какое Production Value ожидается?
13. Какой Capability Progress даст успешное выполнение?

Operator view order:

```text
Причина
  -> Доказательства
  -> Ожидаемая польза
  -> Риски
  -> Approve / Reject
```

Language rules:

| Surface | Language |
| --- | --- |
| Operator explanations | Russian only |
| Engineering Reports | Russian only |
| Canonical documents | Existing document language |
| Code comments | Existing project language |

Definition of Done:

Decision Explainability is `COMPLETE` only when the operator can understand every approval request without reading source code and can honestly answer:

```text
Да, я понимаю, почему система хочет сделать именно это.
```

Completion criteria:

- every approval request includes the Russian decision explanation fields listed above;
- explanations are generated from existing evidence owners, not invented;
- every safety gate result is shown as passed, failed, unknown, or not applicable;
- alternatives are explained, including why keeping current state was not selected;
- expected production value and capability progress are shown;
- remaining risk is shown before Approve / Reject;
- no explanation can authorize runtime action by itself;
- missing evidence produces `STOP_SAFE`, not persuasive text.

Current status:

`IN_PROGRESS`.

Current progress:

`20.0%`.

Blocking backlog items:

`A3`, `A6`, `B1`, `B4`, `B13`, `B15`, `B17`, `C2`.

Completion prediction:

Decision Explainability completes after the operator approval surface explains current packet/class/policy decisions in Russian, ties every explanation to existing evidence, shows safety/risk/value before approval, and has been validated by real governed outcomes and operator review.

Current implementation status:

`READ_ONLY_PREVIEW_AND_ELIGIBILITY_CHECK_ONLY`

Current automation state:

`NO_RUNTIME_AUTOMATION_ENABLED`

## 2.1.6. Canonical Policy Library Rule

The Canonical Policy Library is the permanent source for operational behavior policy:

```text
docs/policies/
```

Before implementing or changing any operational behavior, OMP must ask:

```text
Does a Canonical Policy already exist?
```

Decision rule:

| Answer | OMP action |
| --- | --- |
| `YES` | Reuse the policy. |
| `PARTIAL` | Extend the policy through the complete methodology. |
| `NO` | Execute the complete World Research methodology before implementation. |

Complete policy methodology:

```text
DISCOVER
  -> FULL WORLD RESEARCH
  -> KNOWLEDGE NORMALIZATION
  -> INDUSTRY CONSENSUS DETECTION
  -> INDUSTRY DISAGREEMENT DETECTION
  -> CANONICAL POLICY INTERACTION AUDIT
  -> REALITY AUDIT
  -> V7 FIT ANALYSIS
  -> REUSE EXISTING V7 OWNERS
  -> CANONICAL POLICY
  -> IMPLEMENTATION
  -> VERIFICATION
  -> CERTIFICATION
  -> OMP INTEGRATION
```

Operational implementation before certification is forbidden.
The `IMPLEMENTATION` lifecycle step may prepare code or documentation only after a canonical policy exists; runtime enablement waits for `CERTIFICATION` and OMP integration.

After Stage 4 `V7 FIT ANALYSIS`, implementation is driven by:

```text
docs/programs/V7_IMPLEMENTATION_BACKLOG.md
docs/reference/V7_IMPLEMENTATION_PRIORITY_MODEL.md
```

OMP must choose the highest-priority unfinished backlog item.
OMP must not create a new roadmap document for policy implementation.
After a backlog item is completed, OMP must mark it `DONE`, recalculate priority, and continue.

## 2.1.7. Document Lifecycle Rule

Permanent document lifecycle owner:

```text
docs/reference/V7_DOCUMENT_LIFECYCLE.md
```

Document classes:

| Class | Purpose | Examples | OMP rule |
| --- | --- | --- | --- |
| `REFERENCE` | Permanent knowledge. | System Architecture, Runtime Model, Decision Model, Kernel, Context Resolver, Canonical Policy Library. | Frozen after certification; OMP does not edit during normal implementation. |
| `PROGRAMS` | Drive execution. | OMP, Implementation Program, Current Program State. | Live and updated when execution or optimizer state changes. |
| `IMPLEMENTATION` | Approved mission and implementation registry. | Implementation Backlog, Implementation Priority Model, accepted OMP Missions. | OMP selects work only after admission from Backlog, existing owner, or certified BDP Implementation Candidate. |
| `REPORTS` | Execution history and historical evidence only. | Certified reports and engineering reports under `docs/reports/engineering/`. | Not project documents; never planning, never backlog, never roadmap, never canonical owner. |
| `ADR` | Permanent decisions. | Accepted ADRs. | Read-only decision constraints, never queue. |

Permanent rules:

1. Reference documents are frozen after certification.
2. The Canonical Policy Library is frozen after Stage 4 V7 Fit Analysis.
3. OMP must never generate implementation work from policy documents.
4. OMP may admit implementation work only from:

```text
docs/programs/V7_IMPLEMENTATION_BACKLOG.md
or
certified BDP Implementation Candidate consumed by OMP
or
existing owner work explicitly accepted by OMP
```

5. The Implementation Backlog is not a parallel discovery system and not a free-form idea source.

6. The Implementation Backlog records approved OMP Missions, implementation state, owner mapping, priority, verification, and closure.

7. A BDP Implementation Candidate is not a backlog, queue, owner, roadmap, or mission until OMP admits it.

8. After every implementation:

```text
Update backlog
  -> Update Current Program State
  -> Update OMP
  -> Continue
```

9. OMP must never ask:

```text
What should I implement?
```

It must always resolve:

```text
Highest production-leverage admitted work item
```

10. Reports never generate implementation.
11. Policies never generate implementation.
12. Architecture never generates implementation.
13. BDP discovers candidates; OMP admits or rejects missions.
14. Only an OMP-admitted Mission may proceed to implementation.
15. When there is no admitted Mission, no accepted BDP Implementation Candidate, and no existing-owner work accepted by OMP, OMP must answer:

```text
IMPLEMENTATION_COMPLETE
```

and stop.

This generic `IMPLEMENTATION_COMPLETE` stop is forbidden inside an active Execution Certification Ladder while the ladder state is below:

```text
L6_CONTINUOUS_MODE_ACTIVE
```

During active Execution Certification Ladder execution, lack of an admitted Mission, accepted BDP Candidate, or existing-owner work must trigger the ladder-specific continuation path:

```text
Post-PASS Self-Continuation Rule
  -> next level determination
  -> ready candidate search
  -> BDP minimal Discovery Economy when candidates are insufficient
  -> OMP admission
  -> Mission / legal terminal alternative
  -> execution / verification / report / owner consumption
  -> continue
```

The ladder-specific rule has priority over generic `IMPLEMENTATION_COMPLETE` until the ladder reaches `L6_CONTINUOUS_MODE_ACTIVE` or a real canonical OMP stop is recorded.

### 2.1.7.1. BDP Implementation Candidate Consumption Rule

Status: `CANONICAL`

OMP consumes BDP outputs. OMP does not perform BDP Discovery.

Canonical chain:

```text
Reality
  -> AEP
  -> Behaviour Discovery Program
  -> Implementation Candidate Catalogue
  -> OMP
  -> Mission
  -> Codex
  -> Implementation
  -> Verification
  -> Reality
```

BDP Implementation Candidate Catalogue is:

- a BDP output;
- certified implementation input;
- evidence for OMP admission;
- not a queue;
- not a backlog;
- not an owner;
- not a roadmap;
- not an execution permission.

OMP must consume each Implementation Candidate through admission:

```text
Implementation Candidate
  -> Candidate Evidence Review
  -> Candidate Identity Resolution
  -> Instance Duplicate Check
  -> Candidate Merge / Cohort Safety Review
  -> Existing Owner Check
  -> Dependency Review
  -> Authority Review
  -> Verification Review
  -> Rollback / STOP_SAFE Review
  -> Runtime Boundary Review
  -> Production Boundary Review
  -> OMP Admission Decision
  -> Mission or Rejection / Hold
```

Admission outcomes:

| Outcome | Meaning |
| --- | --- |
| `MISSION_ACCEPTED` | Candidate becomes an OMP Mission and may be implemented through existing owners. |
| `MISSION_HOLD` | Candidate is valid but blocked by missing dependency, evidence, authority, verification, rollback, Runtime, production, or owner extension. |
| `MISSION_REJECTED` | Candidate violates architecture, owner, Runtime, Planner, authority, production, or evidence rules. |
| `MISSION_NOT_APPLICABLE` | Candidate no longer needs implementation or has a legal terminal alternative. |

#### BDP Architecture Stabilization Consumption Rule

Status: `CANONICAL`

When Behaviour Discovery Program reaches `BDP_ARCHITECTURE_STABLE` or an equivalent accepted state proving that its architecture can express the current engineering situation, OMP must treat BDP as a stable producer of implementation decision inputs.

After that point, future project evolution must start with OMP consumption of BDP outputs, not with further expansion of BDP.

Stable BDP outputs consumed by OMP include:

- `Implementation Candidate Instance`;
- `Candidate Coverage Matrix`;
- `Progress Projection`;
- `Engineering Chain Dependency Projection`;
- `Engineering Value`;
- `System Engineering Value`;
- Verification evidence;
- Authority evidence;
- Rollback / `STOP_SAFE` evidence;
- Engineering Chain and Producer -> Consumer evidence.

Boundary rule:

| Program | Responsibility |
| --- | --- |
| BDP | Discover what is happening, why it is happening, what is covered, what is blocked, what has engineering value, and what the next candidate step is. |
| OMP | Decide what to do next, in what order, why that order is optimal, and how to maximize maturity gain through existing Candidate Instances. |

OMP must not ask BDP to expand merely because a candidate is blocked, low maturity, high value, or on a critical path.

BDP may be expanded only after OMP applies Architecture Closed by Default and proves:

```text
FUNDAMENTAL_BDP_ARCHITECTURE_GAP
```

`FUNDAMENTAL_BDP_ARCHITECTURE_GAP` requires proof that existing BDP mechanisms cannot express the engineering situation through:

- Engineering Chain Discovery;
- Behaviour Discovery;
- Automation Readiness;
- Implementation Readiness;
- Engineering Intent Closure;
- Engineering Logic Coverage;
- Implementation Candidate Instance;
- Candidate Classification;
- Candidate Coverage Matrix;
- Current View;
- Progress Projection;
- Engineering Value;
- System Engineering Value;
- Engineering Chain Dependency Projection.

If the situation can be expressed by existing BDP outputs, OMP must consume those outputs and select implementation sequence through the existing OMP execution path.

#### BDP-Derived Execution Sequencing Rule

Status: `CANONICAL`

OMP must choose the next implementation sequence from existing admitted or admissible `Implementation Candidate Instance` records.

OMP must not use manual priority when certified BDP value and coverage data exist.

OMP must rank candidate sequences using only existing evidence:

- `Candidate Coverage Matrix`;
- `Progress Projection`;
- `Engineering Chain Dependency Projection`;
- `Engineering Value`;
- `System Engineering Value`;
- Verification status;
- Authority boundary;
- Rollback / `STOP_SAFE` boundary;
- Production boundary;
- Runtime boundary;
- Engineering Chain;
- Producer -> Consumer path.

OMP must answer:

```text
Which sequence of existing Candidate Instances maximizes maturity gain under current resources, authority boundaries, rollback boundaries, runtime boundaries, and production boundaries?
```

Sequence evaluation must include:

| Evaluation Input | OMP use |
| --- | --- |
| `System Engineering Value` | Prefer candidates that unlock the largest verified system improvement without crossing stop boundaries. |
| `Engineering Value` | Prefer candidates with direct coverage, automation, production, verification, and chain closure gain. |
| `Engineering Chain Dependency Projection` | Order candidates so upstream dependencies, critical path blockers, and final-consumer blockers are handled before dependent candidates. |
| `Progress Projection` | Choose candidates whose next legal status is reachable through existing owners and evidence. |
| `Candidate Coverage Matrix` | Prefer work that improves weakest eligible class/depth cells when safety and authority are equal. |
| Verification / Rollback / Authority / Runtime / Production evidence | Stop or hold candidates that cannot safely advance. |

OMP must produce a sequence decision, not a new BDP request, when existing candidates and projections are sufficient.

Allowed sequence decisions:

| Decision | Meaning |
| --- | --- |
| `SEQUENCE_SELECTED` | OMP selected one or more Candidate Instances for Mission admission or cohort review. |
| `SEQUENCE_HOLD` | No safe sequence can advance without resolving an existing blocker. |
| `SEQUENCE_NOT_APPLICABLE` | Existing candidates do not require implementation or have legal terminal alternatives. |
| `BDP_REFRESH_REQUIRED` | Existing BDP evidence is stale or insufficient, but the BDP architecture remains sufficient. |
| `FUNDAMENTAL_BDP_ARCHITECTURE_GAP` | Existing BDP architecture cannot express the situation after Architecture Closed by Default proof. |

OMP must not create a new queue, roadmap, owner, planner, runtime path, graph, or architecture from this sequencing rule.

The output of sequencing is consumed by the existing OMP admission and Mission lifecycle only.

#### OMP Candidate Sequencing Algorithm

Status: `CANONICAL`

The OMP Candidate Sequencing Algorithm is the official method for selecting the best implementation sequence from existing `Implementation Candidate Instance` records.

It is not:

- a new Planner;
- a new architecture;
- a new owner;
- a new program;
- a new queue;
- a new Runtime;
- a replacement for BDP;
- a replacement for Mission Admission;
- a replacement for Execution Certification.

The algorithm reuses mature-system principles normalized for V7:

| Mature-system principle | V7 OMP interpretation |
| --- | --- |
| Feasibility filtering before scoring | Invalid or unsafe candidates must be removed before value comparison. |
| Policy and authority before execution | Authority boundaries outrank value. |
| Health/readiness before traffic or work placement | Verification, rollback, runtime, and production readiness must exist before execution. |
| Preference/scoring after eligibility | Engineering Value and System Engineering Value are used only after eligibility and safety pass. |
| Dependency and reservation before binding | Upstream dependencies, critical path, rollback, and STOP-safe ability are resolved before Mission Admission. |
| Deterministic tie-breaking | Equal candidates are ordered by evidence-backed chain position, unblock effect, maturity delta, and risk boundary; not manual priority. |
| Post-decision verification | Sequence decision is incomplete until Mission Admission, execution, verification, and consumer behavior closure occur. |

Canonical algorithm:

```text
Candidate Pool
  -> Validity Filter
  -> Safety Filter
  -> Authority Filter
  -> Runtime Filter
  -> Rollback / STOP_SAFE Filter
  -> Dependency Ordering
  -> Critical Path Detection
  -> Coverage Optimization
  -> Engineering Value Evaluation
  -> System Engineering Value Evaluation
  -> Sequence Optimization
  -> Mission Admission
  -> Execution / Hold / Rejection / Not Applicable
```

OMP must choose a sequence, not merely a single best candidate, when more than one candidate exists.

##### Candidate Pool

Candidate Pool contains only existing records from:

- admitted OMP Missions;
- Implementation Backlog entries;
- existing owner work accepted by OMP;
- certified BDP-derived `Implementation Candidate Instance` records.

Documents, owners, reports, rules, models, sections, Function Graph nodes, canonical sources, and context artifacts must not enter the Candidate Pool as candidates.

##### Validity Filter

Candidate may proceed only if it has:

- Candidate Instance identity;
- source / producer;
- existing owner;
- existing consumer or legal consumer gap;
- current state;
- expected state;
- terminal path;
- BDP certificate when BDP-derived;
- OMP admission evidence or path to OMP admission.

Failure output:

```text
SEQUENCE_HOLD_INVALID_CANDIDATE
```

##### Safety Filter

Candidate may proceed only if:

- Behavior Chain is complete or has legal terminal consumer path;
- verification path exists or candidate is verification-building;
- rollback / containment / `STOP_SAFE` exists where required;
- production and runtime impact are explicit;
- no hidden user movement, runtime apply, authority expansion, or production mutation is implied.

Failure output:

```text
SEQUENCE_HOLD_UNSAFE
```

##### Authority Filter

Candidate may proceed only inside current certified authority.

If candidate requires authority not currently granted, OMP must return:

```text
ENGINEERING_AUTHORITY
OPERATIONAL_AUTHORITY
REAL_WORLD_LIMIT
```

as applicable.

Authority blockers outrank Engineering Value, System Engineering Value, maturity gain, and critical-path position.

##### Runtime Filter

Runtime-affecting candidates may proceed only when the Runtime owner/path, action class, verification, rollback, and production boundary allow it.

If not, OMP must hold the candidate rather than reclassify the work as architecture.

##### Rollback / STOP_SAFE Filter

Candidate may proceed only if rollback, containment, no-change terminal path, or `STOP_SAFE` is available for the action class.

Lack of rollback does not create a Planner need.

It produces:

```text
SEQUENCE_HOLD_ROLLBACK_BLOCKED
```

##### Dependency Ordering

OMP must order candidates by Engineering Chain dependency evidence:

1. candidates with no unresolved upstream dependencies;
2. candidates that unblock the largest number of downstream candidates;
3. candidates required by a final consumer path;
4. candidates that resolve root causes shared by multiple blocked candidates;
5. dependent candidates only after upstream blockers are resolved.

Dependency order must come from `Engineering Chain Dependency Projection`, not from manual priority, file order, report order, or wording similarity.

##### Critical Path Detection

OMP must mark a candidate as critical path when it:

- is on the longest unresolved Engineering Chain path to Production Certification;
- is the only path to a required final consumer;
- blocks a required authority, verification, rollback, runtime, production, or chain-closure transition;
- or unlocks the highest downstream System Engineering Value.

Critical-path candidates are not automatically executable.

They still must pass safety, authority, runtime, rollback, and Mission Admission.

##### Coverage Optimization

OMP must compute expected coverage delta for each candidate sequence:

| Delta | Source |
| --- | --- |
| `Engineering Maturity Delta` | Candidate Coverage Matrix and BDP project maturity navigation indicators. |
| `Production Maturity Delta` | Production Maturity model, production evidence, and certification result. |
| `Automation Coverage Delta` | Automation Coverage / Progress Projection. |
| `Implementation Coverage Delta` | Candidate Coverage Matrix and Implementation Progress. |
| `Verification Coverage Delta` | Verification evidence and Candidate Coverage Matrix. |
| `Capability Closure Delta` | Behavior Chain, consumer closure, and Capability / Production Maturity evidence. |

OMP must not hand-edit maturity deltas.

##### Engineering Value Evaluation

OMP must evaluate each candidate using certified BDP values:

- `Coverage Gain`;
- `Production Gain`;
- `Automation Gain`;
- `Verification Gain`;
- `Chain Closure Gain`;
- `Engineering Value`.

If BDP values are missing or stale, OMP may return `BDP_REFRESH_REQUIRED`.

##### System Engineering Value Evaluation

OMP must evaluate system-level impact:

- `System Engineering Value`;
- `Unblocked Candidate Count`;
- `Critical Path Impact`;
- `Root Cause Impact`;
- downstream maturity delta;
- expected newly available candidates after execution.

System Engineering Value may select the sequence among safe candidates, but it must not override authority, rollback, runtime, production, or verification blockers.

##### Sequence Optimization

OMP must select the sequence that maximizes verified maturity gain under current constraints.

Sequence optimization rules:

1. Reject invalid candidates before scoring.
2. Hold unsafe candidates before scoring.
3. Stop at authority boundary before scoring if authority is insufficient.
4. Stop at runtime / rollback / production boundary when required.
5. Prefer candidates that resolve upstream dependencies before downstream candidates.
6. Prefer candidates that unlock more candidates when safety and authority are equal.
7. Prefer candidates on the critical path when safety and authority are equal.
8. Prefer higher System Engineering Value when dependency order does not decide.
9. Prefer higher Engineering Value when System Engineering Value is equal.
10. Prefer weakest Candidate Coverage Matrix cells when value and safety are equal.
11. If all computed criteria are equal, choose the candidate with strongest verification evidence and smallest runtime / production blast radius.
12. If still equal, return `SEQUENCE_HOLD_TIE_REQUIRES_EVIDENCE`, not manual priority.

Fixed weights are forbidden unless they come from an existing canonical owner.

Manual priority is forbidden when certified data exists.

##### Required Sequence Decision Output

Every sequence decision must answer:

| Question | Required answer |
| --- | --- |
| Which candidate executes first? | Candidate Instance ID or hold/rejection/not-applicable reason. |
| Why first? | Evidence-backed dependency, safety, authority, value, critical path, or coverage reason. |
| What does it unblock? | Downstream Candidate IDs / chain conditions or `NONE`. |
| What happens after execution? | Expected next Candidate Coverage Matrix update and next sequence candidate. |
| How does Candidate Coverage Matrix change? | Cell delta or `NO_CHANGE_WITH_REASON`. |
| How does Engineering Maturity change? | Computed delta or `NOT_APPLICABLE_WITH_REASON`. |
| How does Production Maturity change? | Computed delta or `NOT_APPLICABLE_WITH_REASON`. |
| Which candidates become available? | Candidate IDs or `NONE`. |
| Which candidates remain blocked? | Candidate IDs and blockers. |
| Which STOP applies if any? | `STOP_SAFE`, `ENGINEERING_AUTHORITY`, `OPERATIONAL_AUTHORITY`, `REAL_WORLD_LIMIT`, or `NONE`. |

##### Mission Admission

Only after sequence selection may OMP route the first selected candidate to Mission Admission.

Sequence selection alone is not execution permission.

Mission Admission remains the legal boundary between candidate analysis and implementation.

##### Relationship With Execution Certification

Execution Certification consumes completed Mission / legal terminal evidence.

It does not choose the sequence.

OMP Sequencing chooses the sequence; Mission Admission admits it; Execution Certification later verifies whether the cycle evidence can count for certification.

#### OMP Decision Trace Contract

Status: `CANONICAL`

The OMP Decision Trace Contract is the mandatory explanation record for every OMP decision that evaluates, sequences, admits, holds, rejects, or marks an `Implementation Candidate Instance` as not applicable.

It is an explanation of an already-made OMP decision.

It is not:

- a new Planner;
- a new Decision Engine;
- a new Recommendation Engine;
- a new architecture;
- a new owner;
- a new program;
- a new queue;
- a new Runtime;
- a new truth source;
- a scoring override;
- an execution permission.

Decision Trace does not change the decision.

Decision Trace records why the existing OMP Candidate Sequencing Algorithm, Mission Admission, authority model, safety model, runtime model, rollback model, Engineering Chain, and owner evidence produced the decision.

##### Reused Decision Principles

OMP Decision Trace reuses mature-system principles normalized for V7:

| Mature-system principle | V7 OMP Decision Trace interpretation |
| --- | --- |
| Filtering before scoring | The trace must show which candidates passed or failed each eligibility filter before value comparison. |
| Phase-based decision process | The trace must preserve the exact decision stage where a candidate moved forward, held, or stopped. |
| Health and readiness gates | Verification, rollback, runtime, production, and safety evidence must be visible as gate outcomes. |
| Policy and authority separation | Authority must be named separately from value, convenience, or implementation desire. |
| Reservation before binding | Dependency, critical-path, rollback, and STOP-safe constraints must be resolved before Mission Admission. |
| Explainable dashboards | Operator-facing explanation must be simple; engineering-facing explanation must preserve full evidence and owner trace. |
| Runtime guard discipline | Runtime guard, safety, and rollback failures must produce explicit hold/block reasons instead of hidden scoring penalties. |

##### Decision Trace Scope

Decision Trace applies to:

- OMP Candidate Sequencing decisions;
- OMP Mission Admission decisions;
- OMP hold, block, reject, and not-applicable decisions for Candidate Instances;
- OMP decisions that select one candidate while leaving alternatives unselected;
- OMP decisions that return an existing canonical STOP.

Decision Trace must not duplicate:

- BDP Candidate Reality Gate;
- OMP Implementation Candidate Eligibility Gate;
- Behavior Enforcement Framework;
- Execution Certification;
- Engineering Report narrative;
- Production Maturity certification;
- Runtime verification.

Responsibility split:

| Owner / mechanism | Responsibility | Decision Trace use |
| --- | --- | --- |
| BDP | Proves candidate reality and candidate substance. | Trace links to BDP certificate; it does not re-prove it. |
| OMP Eligibility / Admission | Decides whether a candidate can enter OMP execution. | Trace records the admission result and reason. |
| OMP Candidate Sequencing Algorithm | Selects the best legal sequence. | Trace records each stage outcome and decisive criteria. |
| Behavior Enforcement Framework | Verifies behavior chain completeness. | Trace records the consumed behavior-chain result. |
| Execution Certification | Certifies completed execution evidence. | Trace records whether execution evidence is later eligible; it does not certify it. |
| Engineering Report | Saves historical action evidence. | Report links to Decision Trace and summarizes the decision. |
| Dashboard | Displays read-only OMP state. | Dashboard consumes trace; it never decides. |

##### Decision Trace Required Fields

Every Decision Trace must include:

| Field | Required value |
| --- | --- |
| Decision Trace ID | Stable identifier for this trace. |
| OMP Decision ID | OMP decision or action identifier. |
| Decision Timestamp | Timestamp or `UNKNOWN_WITH_REASON`. |
| Candidate ID | Candidate Instance ID, or legal terminal alternative ID. |
| Candidate Source | BDP Candidate Catalogue, BDP minimal Discovery Economy output, Implementation Backlog, admitted Mission, existing owner work, or `NOT_APPLICABLE_WITH_REASON`. |
| Decision Status | `SELECTED`, `REJECTED`, `HELD`, `BLOCKED`, `NOT_APPLICABLE`, `ADMITTED`, `NOT_ADMITTED`, or `UNKNOWN`. |
| Decision Stage | Current stage from the canonical Decision Stage list. |
| Decision Result | Final result produced by OMP. |
| Stage Outcome | `PASS`, `FAIL`, `HOLD`, `BLOCKED`, `NOT_APPLICABLE`, or `UNKNOWN`. |
| Reason | Exact engineering reason for the stage outcome. |
| Evidence | Existing evidence pointer or `UNKNOWN_WITH_REASON`. |
| Owner | Existing owner responsible for the evidence or decision input. |
| Authority | Authority state, boundary, or stop condition. |
| Verification | Verification path or legal missing-verification reason. |
| Rollback | Rollback, containment, no-change terminal path, `STOP_SAFE`, or blocker. |
| Production | Production impact, maturity impact, or `NOT_APPLICABLE_WITH_REASON`. |
| Runtime | Runtime impact or `NOT_APPLICABLE_WITH_REASON`. |
| Engineering Chain | Chain segment, dependency, consumer closure state, or legal gap. |
| Candidate Coverage Matrix Delta | Cell delta or `NO_CHANGE_WITH_REASON`. |
| Engineering Maturity Delta | Computed delta or `NOT_APPLICABLE_WITH_REASON`. |
| Production Maturity Delta | Computed delta or `NOT_APPLICABLE_WITH_REASON`. |
| Unblocks | Downstream Candidate IDs, owner transitions, or `NONE_WITH_REASON`. |
| Newly Available Candidates | Candidate IDs or `NONE_WITH_REASON`. |
| Remaining Blockers | Candidate IDs and blockers or `NONE`. |
| Re-admission Conditions | Conditions required for future admissibility or `NOT_APPLICABLE_WITH_REASON`. |
| Alternative Analysis | Why non-selected candidates were not selected. |
| Final Verdict | Final OMP decision verdict. |
| Engineering Report Pointer | Engineering report path or `PENDING_REPORT_WITH_REASON`. |

##### Canonical Decision Stages

Each evaluated candidate must receive a stage outcome for every applicable stage:

```text
Candidate Pool
  -> Validity Filter
  -> Safety Filter
  -> Authority Filter
  -> Runtime Filter
  -> Rollback Filter
  -> Dependency Ordering
  -> Critical Path
  -> Coverage Optimization
  -> Engineering Value
  -> System Engineering Value
  -> Sequence Optimization
  -> Mission Admission
  -> Final Decision
```

Allowed stage outcomes:

| Outcome | Meaning |
| --- | --- |
| `PASS` | Candidate passed this stage through existing evidence and owner rules. |
| `FAIL` | Candidate is eliminated by this stage. |
| `HOLD` | Candidate may become admissible after an existing blocker is resolved. |
| `BLOCKED` | Candidate cannot continue because an owner, authority, evidence, runtime, rollback, production, or consumer condition blocks it. |
| `NOT_APPLICABLE` | Stage does not apply and the trace explains why. |
| `UNKNOWN` | Required evidence is unavailable; OMP must not invent a reason. |

Every non-`PASS` outcome must name:

- eliminating stage;
- exact filter or rule;
- existing owner;
- evidence pointer or missing-evidence reason;
- whether the candidate can become admissible later;
- smallest existing next action required for re-admission, or legal terminal alternative.

##### Rejected Candidate Trace

For every rejected candidate, Decision Trace must state:

| Question | Required answer |
| --- | --- |
| Which stage eliminated it? | Canonical Decision Stage. |
| Which filter or rule eliminated it? | Existing OMP / owner rule. |
| Why was it eliminated? | Exact reason, not a summary preference. |
| Can it become admissible later? | `YES`, `NO`, or `UNKNOWN_WITH_REASON`. |
| What is needed? | Evidence, owner action, authority, verification, rollback, production readiness, consumer closure, or `NOT_APPLICABLE_WITH_REASON`. |

##### Selected Candidate Trace

For every selected candidate, Decision Trace must state:

| Question | Required answer |
| --- | --- |
| Why was it selected? | Decisive criteria from existing OMP stages. |
| Which criteria decided? | Safety, authority, dependency, critical path, coverage, Engineering Value, System Engineering Value, rollback, runtime, verification, or production boundary. |
| What system effect is expected? | Engineering Chain, maturity, production, runtime, verification, rollback, or consumer effect. |
| What does it unblock? | Candidate IDs, owner transitions, mission path, or `NONE_WITH_REASON`. |
| Which candidates become newly available? | Candidate IDs or `NONE_WITH_REASON`. |
| How does Candidate Coverage Matrix change? | Cell delta or `NO_CHANGE_WITH_REASON`. |
| How does Engineering Maturity change? | Delta or `NOT_APPLICABLE_WITH_REASON`. |
| How does Production Maturity change? | Delta or `NOT_APPLICABLE_WITH_REASON`. |

##### Alternative Explanation Rule

When OMP selects candidate `A` over candidates `B`, `C`, or others, the trace must explain the strongest evidence-backed reason each alternative was not selected.

Alternative explanation must not be persuasive text.

It must be one of:

- failed earlier filter;
- held by existing owner blocker;
- lower dependency priority;
- lower critical-path impact;
- lower coverage gain;
- lower Engineering Value;
- lower System Engineering Value;
- higher runtime / production / rollback risk;
- authority boundary;
- missing verification;
- missing consumer closure;
- equal criteria with stronger evidence needed;
- legal terminal alternative.

##### Decision Tree Projection

Decision Trace must expose a deterministic decision-tree projection:

```text
Candidate
  -> Filter
  -> Reason
  -> Next Filter
  -> Reason
  -> Final Verdict
```

The decision tree is a projection of existing OMP logic.

It must not become:

- a new graph;
- a new planner;
- a new recommendation engine;
- a new score model;
- a new execution owner.

##### Traceability Rule

Every Decision Trace step must link to an existing owner.

Trace may reference only:

- OMP;
- BDP;
- AEP when consumed by OMP;
- Current Program State;
- Canonical Reference;
- SYSTEM_MAP;
- Runtime Model;
- Decision Model;
- Production Maturity Model;
- Engineering Entity Model;
- Engineering Chain Model;
- Function Graph as discovery / context evidence;
- Engineering Reports as historical evidence;
- implementation owners named by existing owner maps.

Decision Trace must not create new rules.

Decision Trace must not mutate owner truth.

Decision Trace must not silently promote report evidence to canonical truth.

##### Engineering Report Link Rule

Every Engineering Report created after an OMP decision must include:

- Decision Trace ID;
- Decision Trace Summary;
- selected candidate, if any;
- held / rejected / not-applicable alternatives, if any;
- decisive criteria;
- final OMP decision;
- link or pointer to the full Decision Trace when stored separately;
- `NOT_APPLICABLE_WITH_REASON` when the action did not include an OMP decision.

The Engineering Report remains historical evidence.

Decision Trace remains the structured explanation of the OMP decision.

##### Dashboard Readiness

Decision Trace must be suitable for future OMP Dashboard consumption without creating dashboard authority.

Operator View must be able to show:

- what OMP selected;
- why it selected it;
- why alternatives were not selected;
- whether the decision is safe, held, blocked, rejected, or not applicable;
- next action or STOP;
- source owner.

Engineering View must be able to show:

- full candidate-by-candidate stage trace;
- all stage outcomes;
- evidence and owner pointers;
- authority, verification, rollback, runtime, production, and Engineering Chain context;
- coverage and maturity deltas;
- alternative analysis;
- final verdict.

Dashboard may display Decision Trace only as read-only explanation.

It must never use Decision Trace to approve, rank, mutate Runtime, expand authority, certify evidence, create a queue, or replace OMP.

#### Decision Reproducibility Law

Status: `CANONICAL`

Decision Reproducibility is the permanent OMP law that every OMP engineering decision must be explainable, reproducible, deterministic, and auditable from existing canonical inputs.

It extends the OMP Decision Trace Contract.

It does not create:

- a new architecture;
- a new Planner;
- a new Decision Engine;
- a new Replay Engine;
- a new owner;
- a new program;
- a new model;
- a new truth source;
- a new Runtime path.

Decision Reproducibility reuses:

- OMP Candidate Sequencing Algorithm;
- OMP Decision Trace Contract;
- deterministic tie-breaking in Candidate Sequencing;
- BDP Candidate Reality Gate certificates;
- OMP Implementation Candidate Eligibility / Admission certificates;
- Behavior Enforcement Framework;
- Current Program State;
- Authority, verification, rollback, runtime, production, and Engineering Chain owners;
- Decision Lifecycle / Decision Freshness from Runtime Model;
- Mission Replay and Scheduler Determinism from Execution Mission Protocol when OMP decision becomes an admitted Mission;
- Engineering Reports as historical evidence only.

##### Reproducibility Definition

For any OMP decision, if OMP receives the same canonical inputs, it must produce the same decision.

Canonical inputs are:

| Input | Source |
| --- | --- |
| Candidate Pool | OMP-admissible candidate records from existing owners. |
| BDP Certificate | BDP Candidate Reality Gate output when candidate is BDP-derived. |
| OMP Certificate | OMP Eligibility / Admission certificate. |
| Behavior Chain | Behavior Enforcement Framework result. |
| Current Program State | `docs/programs/V7_CURRENT_PROGRAM_STATE.md`. |
| Authority Boundary | Existing authority owner / OMP authority state. |
| Verification | Existing verification owner / verification path. |
| Rollback Boundary | Rollback, containment, no-change terminal path, or `STOP_SAFE` evidence. |
| Production Boundary | Production Maturity / production owner evidence. |
| Runtime Boundary | Runtime Model / runtime owner evidence where applicable. |
| Engineering Chain | Engineering Chain owner, dependency, consumer, and terminal path evidence. |
| Candidate Coverage Matrix | Existing BDP / OMP coverage evidence when applicable. |
| Engineering Value | Certified candidate value input when present. |
| System Engineering Value | Certified system-level value input when present. |
| OMP Version | The exact OMP version used for the decision. |
| Canonical owner versions / pointers | Existing canonical document or owner pointers used by the decision. |

If these inputs are identical, OMP must produce identical:

- Decision Trace;
- Decision Fingerprint;
- candidate filtering outcomes;
- rejection reasons;
- selection reasons;
- final sequence;
- Mission Admission result;
- STOP result, if any;
- Final Verdict.

##### Decision Fingerprint

Every OMP decision must produce a `Decision Fingerprint`.

Decision Fingerprint is a deterministic identifier computed only from canonical OMP decision inputs.

Decision Fingerprint may include:

- normalized Candidate Pool IDs and candidate identities;
- BDP Certificate IDs / hashes;
- OMP Certificate IDs / hashes;
- Behavior Chain status;
- Current Program State pointer / state hash;
- authority boundary;
- verification boundary;
- rollback boundary;
- production boundary;
- runtime boundary;
- Engineering Chain dependency state;
- Candidate Coverage Matrix state;
- Engineering Value and System Engineering Value inputs;
- OMP version;
- canonical owner pointers used in the decision.

Decision Fingerprint must not include:

- random values;
- wall-clock timestamps;
- session IDs;
- chat IDs;
- unstable temporary identifiers;
- generated prose;
- file ordering unless normalized;
- environment-specific path noise;
- any value not owned by an existing canonical input.

Timestamp may be recorded in Decision Trace for history, but it must not affect Decision Fingerprint.

##### Decision Replay

OMP must be able to replay a decision from its Decision Trace and canonical input snapshot.

Decision Replay must reconstruct:

- Candidate Pool;
- every filter stage;
- every stage outcome;
- every rejection reason;
- every selection reason;
- alternative explanations;
- final sequence;
- Mission Admission result;
- STOP result;
- Final Verdict.

Decision Replay result must be one of:

| Result | Meaning |
| --- | --- |
| `REPLAY_PASS` | Replay reproduced the same Decision Fingerprint, Decision Trace, sequence, admission result, STOP, and final verdict. |
| `REPLAY_FAIL` | Replay did not reproduce the same result. |
| `REPLAY_BLOCKED_MISSING_INPUT` | A required canonical input is unavailable. |
| `REPLAY_NOT_APPLICABLE` | The action did not include an OMP decision. |

Replay is an audit function over existing OMP evidence.

Replay must not decide, rank, admit, execute, certify, mutate Runtime, expand authority, or create a new candidate.

##### Decision Drift

Decision Drift exists when two OMP decisions for the same candidate set or mission context produce different outputs.

Decision Drift is acceptable only when at least one canonical input changed.

OMP must identify the changed input category:

- Candidate Pool;
- BDP Certificate;
- OMP Certificate;
- Behavior Chain;
- Current Program State;
- Authority Boundary;
- Verification;
- Rollback Boundary;
- Production Boundary;
- Runtime Boundary;
- Engineering Chain;
- Candidate Coverage Matrix;
- Engineering Value;
- System Engineering Value;
- OMP Version;
- canonical owner pointer;
- other existing owner input.

If no changed canonical input is identified, the decision is non-deterministic.

##### Non-Deterministic Decision Stop

OMP must never produce different decisions from identical canonical inputs.

If replay detects different Decision Trace, sequence, Mission Admission, STOP, or Final Verdict for identical inputs, OMP must classify the situation as:

```text
NON_DETERMINISTIC_DECISION
```

and stop further execution until the source of non-determinism is identified and corrected through an existing owner.

Allowed outputs after `NON_DETERMINISTIC_DECISION`:

- `STOP_SAFE`;
- `ENGINEERING_AUTHORITY`;
- `REPLAY_BLOCKED_MISSING_INPUT`;
- `EXISTING_OWNER_CORRECTION_REQUIRED`;
- `FUNDAMENTAL_ARCHITECTURE_GAP` only if existing owners cannot express the defect after proof.

OMP must not continue by manual preference, generated explanation, or operator convenience when deterministic replay fails.

##### Decision Audit Requirements

Decision Trace and Decision Replay together must answer at any time:

| Question | Required answer |
| --- | --- |
| Why was this decision made? | Decision Trace stages, reasons, evidence, owners, and final verdict. |
| Can it be repeated? | `REPLAY_PASS`, `REPLAY_FAIL`, `REPLAY_BLOCKED_MISSING_INPUT`, or `REPLAY_NOT_APPLICABLE`. |
| Which inputs were used? | Canonical input snapshot and Decision Fingerprint components. |
| What changed between two decisions? | Decision Drift explanation naming changed canonical inputs. |
| Why did an alternative lose? | Alternative Explanation Rule from Decision Trace. |
| Why did execution stop? | STOP result and owner-mapped reason. |

##### Dashboard Reproducibility Readiness

Future OMP Dashboard may display Decision Reproducibility fields as read-only evidence:

- Decision Fingerprint;
- Replay status;
- Replay PASS / FAIL;
- Decision Drift;
- Difference Explanation;
- changed canonical input category;
- non-determinism stop reason.

Dashboard must not compute decisions from these fields.

Dashboard must not become the Replay owner, Decision owner, Planner, or truth source.

##### Engineering Report Reproducibility Link

Every Engineering Report created after an OMP decision must include:

- Decision Fingerprint;
- Replay Status;
- Decision Drift status;
- Difference Explanation when replay differs from a prior decision;
- `NON_DETERMINISTIC_DECISION` when identical inputs produce different outputs;
- `NOT_APPLICABLE_WITH_REASON` when the action did not include an OMP decision.

#### Implementation Candidate Identity

Status: `CANONICAL`

OMP must prevent duplicate Missions by resolving the engineering identity of every accepted BDP Implementation Candidate before Mission creation.

Implementation Candidate identity is not:

- candidate title;
- report heading;
- file path;
- function name;
- class name;
- document location;
- wording similarity.

Implementation Candidate identity is the normalized engineering meaning of the candidate as consumed by OMP.

OMP must distinguish:

| Identity level | Meaning | OMP rule |
| --- | --- | --- |
| `Implementation Candidate Class` | Reusable engineering problem pattern. | May be shared by multiple real situations. It must not automatically become one Mission. |
| `Implementation Candidate Instance` | One concrete engineering situation that may require implementation. | This is the unit OMP admits, holds, rejects, marks not applicable, reopens, or converts into a Mission. |
| `OMP Mission Identity` | OMP-admitted execution identity derived from one Candidate Instance or one safe Cohort of compatible Instances. | Prevents duplicate in-progress Missions and preserves implementation history. |

Class examples:

- `SERVICE_SPECIFIC_CHANNEL_FAILURE`;
- `VERIFICATION_CHAIN_BREAK`;
- `CONSUMER_CONFIRMATION_MISSING`;
- `AUTHORITY_BOUNDARY_BLOCK`;
- `ROLLBACK_UNCERTAINTY`.

Instance examples:

- Telegram fails for User A on Channel X during Evidence Window N;
- YouTube fails for User B on Channel Y during Evidence Window M;
- Verification is missing for Mission Z after implementation report R.

Different Instances may share one Class. OMP must create, hold, reject, or close Missions by Instance, not by Class.

#### Candidate Identity Components

OMP must resolve identity through the minimum deterministic set of available components.

Core identity components:

| Component | Class / Instance role |
| --- | --- |
| Engineering Intent | Required for both Class and Instance. |
| Automation Break | Required when the candidate comes from automation or Behaviour Discovery evidence. |
| Affected Behaviour | Required when Behaviour is known; otherwise record `UNKNOWN_WITH_REASON`. |
| Affected Capability | Required when capability is known; otherwise record `NOT_APPLICABLE_WITH_REASON`. |
| Affected Owner | Required existing owner or `OWNER_EXTENSION_REQUIRED`. |
| Affected Consumer | Required expected consumer or `CONSUMER_UNKNOWN_WITH_REASON`. |
| Required Service | Class component when service-specific; Instance component when scoped to a concrete service case. |
| Policy Context | Required when policy constrains action. |
| Current State | Instance component. |
| Expected State | Required intent component. |
| Failure Mode | Class component when generalized; Instance component when evidence-specific. |
| Evidence Window | Instance component. |
| Runtime Context | Instance component when runtime relevant. |
| User Scope | Instance component or `NOT_APPLICABLE_WITH_REASON`. |
| Group Scope | Instance component or `NOT_APPLICABLE_WITH_REASON`. |
| Channel Scope | Instance component or `NOT_APPLICABLE_WITH_REASON`. |
| Verification Context | Required before Mission creation. |
| Rollback Context | Required before implementation-bearing Mission creation. |
| Authority Context | Required before Mission creation. |

If identity cannot be resolved deterministically, OMP must return `MISSION_HOLD` with `IDENTITY_UNRESOLVED`.

#### Candidate Class and Instance Rules

OMP must apply these rules before creating a Mission:

1. Same Class and same Instance identity means the candidate is a duplicate or reopen of the same real engineering situation.
2. Same Class with different Instance identity means separate real engineering situations exist.
3. Same title with different Instance identity must not be merged.
4. Different title with same Instance identity must be merged or attached as additional evidence.
5. Same affected function, file, or component is never sufficient to prove same Instance.
6. Same Behaviour is never sufficient to prove same Instance when user, service, channel, evidence window, authority, verification, rollback, or runtime context differs.
7. OMP may not create a Mission from a Class alone.
8. OMP may create a Mission only from a Candidate Instance or from a safe Cohort Mission defined below.

#### Instance Duplicate Check

Before Mission creation OMP must check whether the Candidate Instance:

- already exists as an accepted Mission;
- is already in progress;
- has already been implemented;
- has already been verified and closed;
- has been superseded by a later Instance or owner change;
- is part of an existing Cohort Mission;
- is rejected, held, or not applicable for a still-valid reason.

Duplicate check outcomes:

| Outcome | Meaning | OMP action |
| --- | --- | --- |
| `NEW_INSTANCE` | No equivalent Instance is known. | Continue admission. |
| `DUPLICATE_INSTANCE` | Same Instance already exists and is not materially changed. | Attach evidence; do not create a new Mission. |
| `ACTIVE_INSTANCE` | Same Instance is already in an active Mission. | Attach evidence; keep existing Mission. |
| `CLOSED_INSTANCE_REPEAT` | Same Instance reappeared after closure. | Apply Reopen Rules. |
| `SUPERSEDED_INSTANCE` | Same Instance is covered by a newer accepted Mission or terminal alternative. | Attach evidence to superseding record; do not create a duplicate Mission. |
| `COHORT_MEMBER` | Instance is already covered by a safe Cohort Mission. | Attach evidence to Cohort Mission. |
| `IDENTITY_UNRESOLVED` | Deterministic identity cannot be established. | `MISSION_HOLD`. |

#### Candidate Merge Rule

OMP may merge candidate evidence only when deterministic identity proves the same Candidate Instance.

Merge preserves:

- all source evidence;
- all originating BDP candidate references;
- all Engineering Intent references;
- all affected Behaviour references;
- all owner and consumer evidence;
- all verification, rollback, authority, runtime, policy, and production context;
- original discovery history.

Merge must not:

- erase different Instances;
- merge by name similarity;
- merge by shared Class only;
- merge across different authority, verification, rollback, runtime, policy, user, group, channel, or evidence-window contexts unless Cohort Safety explicitly permits it.

#### Cohort Mission Safety Rule

OMP may combine multiple Candidate Instances into one Cohort Mission only when all of the following are true:

- Engineering Intent is identical;
- Automation Break is identical or not applicable for all members;
- affected Behaviour and Capability are compatible;
- required owner is identical;
- required consumer is identical or explicitly compatible;
- verification path is identical;
- rollback / containment / `STOP_SAFE` path is identical;
- authority boundary is identical;
- policy context is identical;
- runtime context is compatible;
- blast radius permits combined handling;
- per-Instance evidence remains traceable;
- per-Instance terminal status can be recorded.

If any condition fails, OMP must keep Missions separate.

Cohort Mission is not a new queue, owner, Runtime, Planner, or architecture. It is only an OMP Mission form for safely handling multiple compatible Instances through one existing owner path.

#### Implementation Candidate Lifecycle

Every Candidate Instance consumed by OMP must have exactly one current lifecycle state:

| State | Meaning |
| --- | --- |
| `DISCOVERED` | Produced by BDP or another accepted input owner but not normalized by OMP. |
| `NORMALIZED` | Identity components resolved and Class / Instance distinction recorded. |
| `MERGED` | Same Instance evidence attached to an existing record. |
| `MISSION_CREATED` | OMP admitted the Instance or safe Cohort as a Mission. |
| `IN_PROGRESS` | Mission has been assigned or is being executed. |
| `IMPLEMENTED` | Implementation output exists. |
| `VERIFIED` | Required verification evidence exists. |
| `CLOSED` | Legal terminal consumer reached. |
| `SUPERSEDED` | Later accepted Instance, owner change, or terminal alternative replaces the old record. |
| `REOPENED` | Closed Instance became active again due to new evidence or recurrence. |

Candidate Instance lifecycle is stored in the existing Mission / Backlog / report / CPS evidence surfaces as applicable. OMP must not create a parallel Candidate queue.

Mission lifecycle is the OMP-admitted segment of Candidate Instance lifecycle:

```text
MISSION_CREATED
  -> IN_PROGRESS
  -> IMPLEMENTED
  -> VERIFIED
  -> CLOSED / SUPERSEDED / REOPENED / terminal hold
```

Mission lifecycle must never be used to identify a Candidate Class. It tracks execution of one Candidate Instance or one safe Cohort Mission after OMP admission.

#### Mission Reopen Rules

After `CLOSED`, a Candidate Instance may be found again.

OMP must determine:

| Reopen classification | Meaning | OMP action |
| --- | --- | --- |
| `NEW_INSTANCE` | Same Class, but different user, group, channel, service, evidence window, runtime, authority, verification, rollback, or policy context. | Run new admission and create a separate Mission if accepted. |
| `REPEATED_INSTANCE` | Same Instance recurs after closure with materially same identity. | Reopen existing Mission lineage or create a reopened Mission record linked to the original closure. |
| `REGRESSION` | Same Instance returns after verified implementation. | Reopen with regression evidence and verification owner. |
| `SUPERSEDED_BY_CONTEXT` | Prior closure no longer applies because owner, policy, authority, runtime, or verification context changed. | Mark old record `SUPERSEDED`; run new admission. |
| `NOT_APPLICABLE_REPEAT` | Repeat evidence does not require implementation because terminal alternative remains valid. | Preserve evidence; no Mission. |

Reopen must preserve the original identity, closure evidence, repeat evidence, and reason for reopening.

Every OMP Mission produced from BDP must preserve:

- Behaviour;
- Engineering Intent;
- Automation Break when applicable;
- Implementation Candidate ID;
- Implementation Candidate Class;
- Implementation Candidate Instance Identity;
- Mission Identity;
- Candidate lifecycle state;
- duplicate check outcome;
- merge or Cohort decision;
- reopen classification when applicable;
- Expected Intent Closure;
- Owner;
- Producer;
- Consumer;
- dependencies;
- authority boundary;
- verification path;
- rollback / containment / `STOP_SAFE`;
- Runtime impact;
- production impact;
- Codex handoff boundary;
- terminal state.

Mission handoff to Codex:

```text
OMP Mission
  -> Codex Implementation Input
  -> Existing Owner Implementation
  -> Verification
  -> Engineering Report
  -> Current Program State
  -> Reality / BDP evidence refresh when required
```

Codex is an implementation assistant for an approved OMP Mission. Codex is not a Runtime actor, owner, Planner, authority source, backlog owner, or production dependency.

Backlog role after BDP alignment:

- Backlog records admitted Mission state.
- Backlog does not discover candidates.
- Backlog does not replace BDP.
- Backlog does not create a parallel queue.
- Backlog does not self-authorize implementation.
- OMP remains the only mission admission and sequencing authority.

Continuous engineering after Mission completion:

```text
Mission Terminal State
  -> Verification
  -> Engineering Report
  -> Current Program State
  -> Reality evidence updated when applicable
  -> BDP refresh when AEP/OMP/operator requires new Behaviour evidence
  -> new Implementation Candidate Catalogue only if BDP produces one
  -> OMP admission
  -> next Mission or terminal stop
```

OMP may request or consume refreshed BDP output, but OMP must not run Discovery itself and must not automatically create a Mission from any refreshed candidate.

World research must include all relevant successful systems and must not stop after the first example.
Required sources include, where applicable: Cisco, Juniper, Arista, Cloudflare, Google, Google SRE, Google Traffic Engineering, Netflix, AWS, Azure, GCP, Kubernetes, Envoy, Istio, Linkerd, HAProxy, NGINX, Meta, Microsoft, Apple, OpenBSD PF, Linux routing, BGP, OSPF, IS-IS, MPLS, SD-WAN, IETF RFCs, academic papers, production postmortems, large-scale distributed systems, operator best practices, community consensus, and any other highly relevant industry source.

Consensus detection must record:

- consensus;
- strength of consensus;
- supporting systems.

Disagreement detection must record:

- why disagreement exists;
- tradeoffs;
- when each approach is used.

Reality audit must compare world practice against:

- current V7 architecture;
- current Runtime;
- current Product Specification;
- current OMP;
- current implementation.

V7 fit analysis must evaluate:

- compatibility;
- performance;
- safety;
- operator burden;
- autonomy;
- learning;
- scalability;
- complexity;
- reuse potential.

Allowed policy decisions:

- `REUSE`;
- `ADAPT`;
- `REJECT`.

Innovation rule:

V7 may innovate only after proving:

- no stable world consensus exists;
- or world consensus does not fit V7 architecture.

Otherwise:

```text
Reuse world knowledge.
```

Initial first policy selected for research was:

`POLICY_001_HARD_FAILURE`

Current Canonical Policy Library state:

`V7_FIT_ANALYSIS_COMPLETE_IMPLEMENTATION_BACKLOG_READY`

Current policy lifecycle stop:

```text
POLICY_001_HARD_FAILURE
POLICY_002_SOFT_DEGRADATION
POLICY_003_RECOVERY_ADMISSION
POLICY_004_AUTHORITY
POLICY_005_ACTION_CLASS_PROMOTION
POLICY_006_BLAST_RADIUS
POLICY_007_ROLLBACK
POLICY_008_FRESHNESS
POLICY_009_ANTI_FLAP
  -> DISCOVER
  -> FULL WORLD RESEARCH
  -> KNOWLEDGE NORMALIZATION
  -> INDUSTRY CONSENSUS DETECTION
  -> CANONICAL POLICY INTERACTION AUDIT
  -> REALITY AUDIT
  -> V7 FIT ANALYSIS
  -> IMPLEMENTATION BACKLOG READY
  -> STOP
```

Next allowed lifecycle stage:

`IMPLEMENTATION_BACKLOG_EXECUTION`

Runtime behavior remains unchanged.
Authority remains unchanged.
No policy implementation is enabled.

## 2.1.8. Research And Architecture Gating Rules

Research changes implementation only through:

```text
Research
  -> Decision Model
  -> OMP
  -> Implementation
```

Research must not create architecture directly.

Architecture changes require a real implementation to prove `FUNDAMENTAL_ARCHITECTURE_GAP`.

Otherwise:

```text
Reuse
  -> Extend
  -> Implement
```

## 2.2. Safety-Bounded Authority Model

V7 must not wait for global self-trust before every small governed action.

V7 separates:

- Knowledge Maturity
- Execution Authority

Knowledge Maturity controls autonomy tier progression.

Execution Authority controls whether an approved action class may execute a fresh bounded packet now.

Core rule:

```text
Trust decides autonomy tier.
Safety decides whether a fresh packet inside approved authority may execute.
```

Knowledge Maturity answers:

```text
How autonomous may V7 become?
```

Execution Authority answers:

```text
May this action class execute this fresh bounded packet now?
```

`70/70/70` remains the hard floor for `TIER_2+` and autonomous progression.

It is not a universal blocker for a `TIER_1` governed one-user operator-reviewed canary.

A `TIER_1` governed action may be considered only when:

- exact packet exists;
- target user is bound;
- target channel is bound;
- rollback target exists;
- restore barrier preview is ready;
- verification plan is ready;
- outcome closure plan is ready;
- learning path is connected;
- blast radius is bounded;
- policy allows the action;
- truth/convergence pass;
- explicit bounded policy authority exists.

For `GOVERNED_ONLY`, explicit packet approval is the fallback only when no approved bounded governed-learning policy covers the exact action.
For `CERTIFIED_FOR_CLASS_APPROVAL`, `CERTIFIED_FOR_BOUNDED_AUTONOMY`, or `AUTONOMOUS_RUNTIME`, OMP must prefer class authority and policy authority over repeating packet approval.

This model does not authorize restore-barrier writes, runtime apply, user movement, rollback apply, daemon/timer enablement, authority expansion, floor changes, synthetic evidence, or new owners.

## 2.3. Background Builds Knowledge, Runtime Spends Knowledge

Background systems may perform expensive work:

- service intelligence;
- quality snapshots;
- prediction;
- trust;
- suitability;
- recovery;
- history;
- learning;
- evidence inventory.

Runtime must remain thin.

Runtime path:

```text
Event
  -> Current State
  -> Knowledge Snapshot
  -> Policy
  -> Safety Check
  -> Action-Class Authority
  -> Fresh Packet
  -> Execute or Stop
  -> Verify
  -> Rollback if needed
  -> Outcome Closure
  -> Learning
```

Runtime must not perform broad audits, broad historical recomputation, or heavy analytics in the event path.

Scaling rule:

V7 must scale to `10,000+` users by precomputing knowledge into compact read models.

Adding users must not linearly increase event-time decision latency.

### Architecture Closed by Default

Status: `PERMANENT_ENGINEERING_PRINCIPLE`.

The V7 architecture is complete by default.

Every newly discovered problem, idea, regression, optimization, or improvement must first be treated as one of:

- unfinished implementation;
- missing integration;
- missing certification;
- missing runtime consumption;
- missing read-model consumption;
- missing production evidence;
- missing authority maturity;
- missing capability progress;
- missing backlog completion;
- missing canonical-owner update.

Architecture evolution is the last resort.

Before proposing an architectural extension, OMP must prove that the existing:

- OMP;
- Runtime Model;
- Product Specification;
- Canonical Policies;
- Implementation Backlog;
- Canonical Owners;
- SYSTEM_MAP;
- Canonical Reference;

cannot own the finding through reuse, extension, integration, certification, read-model consumption, runtime consumption, authority maturity, or production evidence.

Required Architecture Closed by Default output for meaningful work:

| Field | Required value |
| --- | --- |
| `architecture_closed_by_default` | `PASS`, `FAIL`, or `NOT_APPLICABLE_WITH_REASON`. |
| `first_classification` | `UNFINISHED_IMPLEMENTATION`, `MISSING_INTEGRATION`, `MISSING_CERTIFICATION`, `MISSING_RUNTIME_CONSUMPTION`, `MISSING_READ_MODEL_CONSUMPTION`, `MISSING_PRODUCTION_EVIDENCE`, `MISSING_AUTHORITY_MATURITY`, `MISSING_CAPABILITY_PROGRESS`, `MISSING_BACKLOG_COMPLETION`, `MISSING_CANONICAL_UPDATE`, or `FUNDAMENTAL_ARCHITECTURE_GAP_PROVEN`. |
| `existing_owner_mapping` | Existing OMP capability, backlog item, canonical owner, runtime section, policy, reference section, or `NONE_PROVEN_AFTER_AUDIT`. |
| `architecture_extension` | Default `FALSE`; may become `TRUE` only after complete audit proves reuse and extension impossible. |

If the gate fails, OMP must not redesign V7. It must return to the existing owner/backlog/capability path.

### Production Scale First

Status: `PERMANENT_ENGINEERING_PRINCIPLE`.

Production Scale First is an OMP execution discipline.

The canonical source is `V7_PRODUCT_SPECIFICATION.md` -> `Product Scale Model`.

Product Scale Model defines the product-level non-functional requirement.

Product Scale Objectives define the long-term optimization target.

Production Scale First is the execution gate that applies that product truth to every OMP decision.

Every future audit, implementation, test, report, policy change, runtime change, evidence model change, learning change, read model, UI/API data-loading change, storage change, background job, canonical update, and OMP decision must answer:

```text
Will this remain efficient, safe, and maintainable at 10,000+ users and 100+ channels?
```

Scale target:

- `10,000+` users;
- `100+` channels;
- millions of runtime decisions;
- long-lived evidence, telemetry, reports, and learning history.

OMP Production Scale First gate:

| Check | Required answer |
| --- | --- |
| Algorithmic complexity | State expected complexity. Avoid `O(N^2)` behavior and full rescans where possible. Prefer `O(1)`, `O(log N)`, bounded scans, incremental updates, indexes, and summaries. |
| Runtime path safety | Runtime must remain thin. Expensive work belongs to background jobs, pre-aggregation, read models, or offline analysis. Runtime consumes prepared and certified data. |
| Storage discipline | Store evidence once and derive summaries. Avoid duplicate durable data and unbounded growth without retention or compaction strategy. Distinguish hot, warm, and cold data where relevant. |
| Read-model discipline | UI, API, and operator views must use summaries, indexes, and drill-down. Normal views must not read massive raw histories. |
| Evidence and learning scale | Do not require full enumeration of all user-to-channel combinations as a permanent autonomy condition. Prefer representative action-class evidence, risk segmentation, blast radius, rollback/no-rollback proof, and learning quality. Enumeration metrics may remain useful signals but must not become non-scalable promotion blockers unless explicitly justified. |
| Reporting discipline | Engineering reports are compact evidence. Durable knowledge goes to canonical owners. Large raw outputs should be referenced or summarized, not duplicated into reports. |
| Indexing and query discipline | Every new persistent data shape must declare its expected lookup pattern. Data that can grow with users, channels, or time must declare an indexing or aggregation strategy. |
| Resource budget | Consider CPU, memory, disk, IO, latency, and write amplification before implementation is considered complete. |

Production scale validation questions:

1. Does runtime cost grow with user count?
2. Does storage grow without bounds?
3. Does CPU cost grow linearly?
4. Does memory growth remain controlled?
5. Can reports grow indefinitely?
6. Can telemetry be aggregated?
7. Can read models be precomputed?
8. Are indexes sufficient?
9. Can expensive work move out of Runtime?
10. Will this still be operationally efficient at production scale?

If the answer proves the proposal is not suitable for production scale, OMP must redesign the implementation approach through existing owners before implementation. It must not lower scale expectations.

Every OMP audit, implementation, report, and backlog decision must evaluate compliance with Product Scale Model. If a proposed solution creates linear or worse growth with users, channels, or time, it must be justified, bounded, indexed, aggregated, or redesigned through existing owners before implementation.

Every future implementation must explicitly state whether it moves V7 toward Product Scale Objectives or away from them.

Required OMP output for meaningful work:

| Field | Required value |
| --- | --- |
| `production_scale_first` | `PASS`, `FAIL`, or `NOT_APPLICABLE_WITH_REASON`. |
| `scale_impact` | Whether the change is bounded or grows with users, channels, or time. |
| `runtime_path_impact` | `NONE`, `READ_MODEL_ONLY`, `RUNTIME_CALCULATION`, or `HEAVY_RUNTIME_CALCULATION_FORBIDDEN`. |
| `storage_index_plan` | Existing summary, existing index, proposed extension through an existing owner, or no persistent data. |
| `resource_budget` | Expected CPU, memory, disk, IO, latency, and write-amplification impact. |
| `evidence_model_scale` | Representative action-class evidence or a justified enumeration signal. |
| `product_scale_objectives_direction` | `TOWARD`, `AWAY`, or `NEUTRAL_WITH_REASON`. |
| `need_new_owner` | Default `FALSE`; if `TRUE`, prove through the New Owner Gate. |
| `need_new_backlog_item` | Default `FALSE`; if `TRUE`, prove through the Backlog Consistency Audit. |

### Runtime Time Architecture Discipline

Status: `RT_PHASE_1_FULLY_COMPLETE`.

OMP consumes Runtime Time Architecture from `docs/reference/V7_RUNTIME_MODEL.md`.
OMP does not own a second time model.

RT Phase 1 implemented the permanent foundation:

| Step | Status | Canonical owner | Completion condition |
| --- | --- | --- | --- |
| `RT1` Canonical Time Architecture | `COMPLETE` | Runtime Model | Observation, World Model, Planning, Execution, Verification, Feedback/Learning, and OMP/Certification planes are named and mapped to existing owners. |
| `RT2` Reaction Latency Model | `COMPLETE` | Runtime Model | Reaction Latency and all components are defined without numeric SLOs or runtime gates. |
| `RT3` Thin Runtime Path Contract | `COMPLETE` | Runtime Model | Runtime remains short, deterministic, lease-bound, fail-closed, and does only live safety work. |
| `RT4` Latency Ownership & Live/Precompute Matrix | `COMPLETE` | Runtime Model | Every current runtime path stage has owner, precompute/live classification, safety reason, future optimization path, and measurement field. |
| `RT5` Engineering Report Latency Requirement | `COMPLETE` | OMP Engineering Report Lifecycle | Every future meaningful engineering report must include Latency Impact. |
| `RT6` Phase 2 Automation-Time Contract | `COMPLETE` | Runtime Model + OMP | Phase 2 scope, dependencies, owners, safety conditions, and expected outputs are defined without implementation. |
| `RT7` Engineering Review Rule | `COMPLETE` | Runtime Model + OMP Engineering Report Lifecycle | Every future engineering activity must answer the Runtime Latency Engineering Review Checklist. |
| `RT8` Phase 2 Automation Contract | `COMPLETE` | Runtime Model + OMP | Phase 2 entry criteria, forbidden pre-entry behavior, complete item contracts, exit criteria, owners, dependencies, safety constraints, and success criteria are defined without implementation. |

OMP execution rule:

```text
Every future audit, implementation, verification, certification, deploy, production action, and OMP status update must preserve the thin runtime path.
```

Work Placement execution rule:

```text
Every future OMP task must identify the canonical execution plane for every meaningful computation it touches.
```

Required placement outputs:

| Field | Required value |
| --- | --- |
| `computation` | The work being introduced, audited, moved, or certified. |
| `canonical_plane` | Observation, World Model, Planning, Execution, Verification, Feedback/Learning, OMP/Certification, or `NOT_APPLICABLE_WITH_REASON`. |
| `canonical_owner` | Existing owner responsible for the computation. |
| `runtime_placement_allowed` | `YES_ONLY_IF_LIVE_SAFETY_REQUIRED`, `NO`, or `NOT_APPLICABLE`. |
| `can_move_earlier` | `YES`, `NO_WITH_SAFETY_REASON`, or `ALREADY_PREPARED`. |
| `reaction_latency_impact` | Observation, Decision, Execution, Verification, Feedback/Learning, Reaction, `NONE`, or `UNKNOWN_WITH_MEASUREMENT_PLAN`. |

Product Evolution Review Gate:

Every future OMP task must pass these reviews before implementation is considered complete:

| Review | Required output |
| --- | --- |
| Certification Review | Mandatory, supporting, optional, or not applicable evidence, according to the canonical certification owner. |
| Work Placement Review | Canonical plane and owner for each meaningful computation. |
| Runtime Latency Review | Reaction Latency component affected, or `NONE`. |
| Runtime Cost Review | CPU, memory, IO, blocking, lock contention, execution cost, rollback cost, and runtime cost impact. |
| Decision Freshness Review | Birth/fresh/stale/invalid/destroyed state and owner for runtime-relevant decision objects. |
| Safety Review | Live gates that remain live and exact `STOP_SAFE` triggers. |

If any review cannot map to an existing owner, OMP must stop and run owner mapping before implementation.

Product Evolution Field Validation:

After every meaningful OMP execution step, implementation, certification, audit, or production validation, the Engineering Report must include Product Evolution Field Validation.

This block validates the design-only Product Evolution Framework as an observational lens.

It does not canonicalize the framework.

It does not activate Operational Campaigns, Evolution Engine, Target Management, Decision Score, Dashboard behavior, Runtime behavior, automation, authority, user movement, OMP sequence changes, Production Maturity writes, Current Program State changes, new owners, new roadmaps, or new planners.

Product Evolution OMP Behavior Gate:

Every meaningful OMP step is the first execution consumer of Product Evolution Framework behavior contracts.

OMP must consume Framework outputs before the step can be considered behavior-complete:

| Framework input | Required handling |
| --- | --- |
| Product Observation | Existing owner value, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Product Value | Existing Business Objective / Product Intent value, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Current Active Target | Existing Current Program State / OMP target, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Production Maturity Gap | Existing Production Maturity / target gap, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Capability Gap | Existing capability owner gap, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Evidence Gap | Existing evidence / certification owner gap, `UNKNOWN`, or `NOT_APPLICABLE`. |

If an input is unavailable, OMP must write `UNKNOWN`.
If an input does not apply to the task class, OMP must write `NOT_APPLICABLE`.
OMP must not invent Product Value, Target, Capability Gap, Evidence Gap, owner, evidence, or maturity state.

OMP must then make exactly one behavior decision:

| Decision | Meaning |
| --- | --- |
| `ACCEPT` | Framework inputs are sufficient for the resolved existing OMP action to proceed. |
| `REJECT` | Framework inputs would force duplicate owner, roadmap, planner, authority, Runtime logic, synthetic evidence, or non-canonical execution. |
| `DEFER` | The action belongs to existing architecture but required owner state, evidence, validation, or timing is not ready. |
| `BLOCK` | The action cannot proceed because a stop gate, safety boundary, authority boundary, certification boundary, or owner mapping condition blocks it. |
| `NOT_APPLICABLE` | The task class does not produce Product Evolution behavior inputs, with explicit reason. |

Every decision must include:

- consumed Framework inputs;
- decision value;
- justification;
- existing owner path;
- safety / authority / Runtime boundary;
- reason later steps remain blocked when applicable.

OMP must produce the corresponding new output:

| OMP output | Produced when |
| --- | --- |
| Execution Decision | `ACCEPT` permits implementation, audit, certification, verification, or documentation execution through existing owners. |
| Evidence Collection Decision | `ACCEPT` or `DEFER` identifies existing evidence owner, certification owner, and missing proof without creating a campaign. |
| Blocked Result | `BLOCK` records the gate, owner, and condition that stopped the step. |
| Deferred Result | `DEFER` records what owner state, evidence, or validation must exist before reconsideration. |
| Rejected Result | `REJECT` records which forbidden architecture expansion or duplicate responsibility was prevented. |
| Engineering Report Requirement | Every decision requires an Engineering Report entry with Product Evolution behavior fields. |

Behavior propagation path:

```text
Product Evolution Framework
  -> OMP behavior decision
  -> Execution / Blocked / Deferred / Rejected / Not Applicable result
  -> Engineering Report
  -> Learning
  -> Product Evolution Framework as new reality
```

An OMP step is complete only when:

```text
Framework output consumed
  -> OMP behavior changed
  -> Execution performed or explicitly blocked / deferred / rejected / marked not applicable
  -> Engineering Report produced
  -> Learning updated or explicitly marked NOT_APPLICABLE
  -> Framework receives new reality through future Product Observation / Field Validation
```

Otherwise the OMP step remains incomplete.

Every future change must answer:

1. Does this increase Runtime work?
2. Can this work be safely prepared earlier?
3. Which latency component is affected?
4. Which live safety gate must remain live?
5. Does the change move V7 toward lower safe Reaction Latency or away from it?

Mandatory Runtime Latency Engineering Review:

| Question | Required answer |
| --- | --- |
| Does this work increase the Runtime execution path? | `YES`, `NO`, or `UNKNOWN_WITH_MEASUREMENT_PLAN`. |
| Can this work move into Observation, World Model, Planning, read model, or background computation? | `YES`, `NO_WITH_SAFETY_REASON`, or `NOT_APPLICABLE`. |
| If it must stay live, why? | Existing safety gate, live eligibility, irreversible apply, verification, rollback, authority, freshness, or `NOT_APPLICABLE`. |
| Which latency components change? | Observation, Decision, Execution, Verification, Feedback, Learning, Reaction, or `NONE`. |
| Does it reduce any latency? | Component name and reason, or `NO`. |
| Does it create a wait state or blocking dependency? | `YES_WITH_OWNER`, `NO`, or `UNKNOWN_WITH_MEASUREMENT_PLAN`. |
| Does it change safety gates? | Freshness, restore barrier, rollback, verification, authority, anti-flap, blast radius, source/target eligibility, or `NONE`. |
| Does it preserve Thin Runtime Path? | `YES` required; `NO` blocks implementation. |
| Can computation be precomputed safely? | `YES`, `NO_WITH_SAFETY_REASON`, or `UNKNOWN_WITH_MEASUREMENT_PLAN`. |
| If latency impact is unknown, how will it be measured later? | Existing field, existing owner extension, or explicit `NOT_APPLICABLE` reason. |

This checklist is mandatory for implementation, audit, verification, test, deployment, certification, owner extension, planner change, runtime change, feedback change, learning change, read-model change, policy change, and OMP change.

Phase 1 forbids:

- runtime automation;
- user movement;
- production apply;
- authority expansion;
- batch movement;
- parallel movement;
- execution queues;
- latency SLOs as gates;
- planner rewrite;
- runtime behavior change.

Phase 2 is deferred, not optional.
It may start only after bounded automation, runtime eligibility, verification, rollback, blast radius, metric reliability, reaction latency measurement, and explicit authority are certified or approved through existing owners.

### Pre-Phase-2 Readiness

Status: `CANONICAL_PROGRAM`
Owner: OMP.
Canonical foundation owner: `docs/reference/V7_RUNTIME_MODEL.md`.

Purpose:

Prepare V7 for Runtime Phase 2 Automation & Runtime Optimization without starting Phase 2, enabling runtime automation, expanding authority, moving users, creating a new owner, or creating a new backlog item.

Pre-Phase-2 Readiness is an implementation-readiness program inside OMP.
It does not replace RT Phase 1, RT6, RT8, A5, A6, B13, B16, or the Implementation Backlog.
It consumes them and decides whether Phase 2 may be opened later.

Foundation status:

| Foundation | Status | Canonical owner | Current integration |
| --- | --- | --- | --- |
| `DL1` Decision Lifetime Model | `EXISTS` | Runtime Model | Canonicalized in Decision Lifecycle And Runtime Foundation; consumed by OMP/report lifecycle. |
| `DL2` Decision Freshness Contract | `EXISTS` | Runtime Model | Canonical states `BORN`, `FRESH`, `STALE`, `INVALID`, `DESTROYED`; consumed by freshness, lease, material-change, and OMP review owners. |
| `DL3` World Model Ownership | `EXISTS` | Runtime Model + SYSTEM_MAP reference | Plane-based ownership exists; SYSTEM_MAP maps current owners. |
| `DL4` Desired Safe State Contract | `EXISTS_PARTIAL` | Runtime Model + Decision Model | Desired State exists; Desired Safe State artifact belongs to Phase 2 and must wait for A6/B13/authority. |
| `DL5` Runtime Cost Model | `EXISTS` | Runtime Model | Runtime cost review is mandatory in Product Evolution Review; measurement remains pre-Phase-2/Phase-2 work. |
| `DL6` Runtime Budget Allocation | `EXISTS_PARTIAL` | Runtime Model | Budget categories exist; numeric budgets are forbidden before measurement and Phase 2 entry. |
| `DL7` Product Evolution Review Gate | `EXISTS` | Runtime Model + OMP | Mandatory for future OMP tasks and Engineering Reports. |

Readiness stages:

| Stage | Goal | Dependencies | Existing owner | Completion criteria | Validation | Relationship to A5/A6/B13/B16/RT Phase 2 |
| --- | --- | --- | --- | --- | --- | --- |
| `DL1` Decision Lifetime Implementation | Make all runtime-relevant decision objects traceable from birth to terminal state. | Decision Lifecycle Foundation, packet/lease/outcome owners. | Runtime Model, packet/lease/governed transaction owners. | Objects have owner, valid-while rule, invalidation rule, and terminal state. | Tests/truth/convergence/report when implementation touches behavior. | Required before A6 can arbitrate live execute/stop reliably. |
| `DL2` Decision Freshness Implementation | Ensure every decision object has a freshness state and material-change semantics. | A2, material-state gate, freshness owners. | Freshness/lease/runtime eligibility owners. | Freshness changes and material invalidation are separated. | Freshness tests, material-change tests, truth/convergence. | Required for A6 and Phase 2 decision freshness lifetime. |
| `DL3` World Model Ownership | Ensure every state family has one plane owner and no silent owner replacement. | SYSTEM_MAP, Work Placement Law, read-model owners. | Runtime Model + SYSTEM_MAP + OMP. | Observation, World Model, Planning, Execution, Verification, Feedback/Learning, and OMP ownership are explicit. | Work Placement review and duplicate-owner checks. | Required before continuous world model work in Phase 2. |
| `DL4` Desired Safe State | Define desired safe state without self-authorizing execution. | Business Objectives, policies, A6, B13, authority model. | Runtime Model, Decision Model, OMP, planner owners. | Desired Safe State is bounded by policy, blast radius, authority, rollback, verification, and runtime eligibility. | Product Evolution Review and safety review. | Cannot become runtime behavior before A6/B13/B16 and authority; Phase 2 consumes it later. |
| `DL5` Runtime Cost Model | Make runtime cost visible before optimization. | Work Placement, Runtime Latency Review, Product Scale. | Runtime Model + OMP. | CPU, memory, IO, blocking, lock contention, execution, rollback, and runtime cost are reviewed. | Engineering Report Runtime Cost Review. | Required before any Phase 2 runtime optimization. |
| `DL6` Runtime Budget Allocation | Keep budget categories ready without premature SLO gates. | Runtime Cost Model, Reaction Latency measurements. | Runtime Model + Production Maturity/OMP owners. | Observation, World Model, Planning, Execution, Verification, Learning, and OMP budgets are categorized; numeric gates remain deferred. | Reported as measurement category, not authority. | Numeric budgets wait for Phase 2 entry evidence. |
| `DL7` Product Evolution Review Gate | Ensure every future change passes certification, placement, time, cost, freshness, and safety review. | Engineering Report Lifecycle, OMP. | OMP + Runtime Model. | Every meaningful action records Product Evolution Review or explicit not-applicable reason. | Engineering Report completeness and truth/convergence. | Guards A5/A6/B13/B16 and all Phase 2 readiness work. |

Pre-Phase-2 Readiness is complete only when:

- RT Phase 1 is `FULLY_COMPLETE`;
- Work Placement Law is canonical;
- Decision Lifecycle And Runtime Foundation is canonical;
- Engineering Report Lifecycle requires Product Evolution Review, Work Placement, Latency Impact, Runtime Cost Review, and Decision Freshness Review;
- A5 is complete;
- A6 is complete;
- B13 is complete;
- B16 is complete;
- bounded automation is certified or explicitly approved through existing authority owners;
- Reaction Latency is measurable;
- Runtime Cost is measurable;
- World Model ownership is canonical and consumed by implementation owners;
- Desired Safe State is canonical and bounded by policy/authority/safety;
- OMP explicitly authorizes Phase 2 entry.

Phase 2 entry contract:

```text
Phase 2 may begin only when:
RT Phase 1 COMPLETE
AND Work Placement COMPLETE
AND Decision Lifecycle COMPLETE
AND Pre-Phase-2 Readiness COMPLETE
AND A5 COMPLETE
AND A6 COMPLETE
AND B13 COMPLETE
AND B16 COMPLETE
AND Reaction Latency measurable
AND Runtime Cost measurable
AND World Model canonical
AND Desired Safe State canonical
AND Engineering Review active
AND explicit authority permits Phase 2 work.
```

If any condition is missing, OMP must continue through the existing highest-priority backlog item and must not start Phase 2.

Before Phase 2 entry, OMP forbids:

- parallel movement;
- batch movement;
- continuous apply;
- execution queues;
- desired-state runtime;
- latency SLO gates;
- planner rewrite;
- authority expansion.

Phase 2 completion requires:

- end-to-end Reaction Latency measurement;
- per-plane latency visibility;
- Desired-State Delta implemented through existing planner owners;
- Execution Queue certification;
- Bounded Parallelism certification;
- fail-closed Runtime preserved;
- rollback and verification preserved unless separately certified;
- authority unchanged unless separately approved.

## 2.4. Architectural Laws

These laws are immutable unless a future ADR explicitly supersedes them:

| Law | Rule |
| --- | --- |
| Law 1 | Reality First. |
| Law 2 | Reuse before Extend. |
| Law 3 | Extend before Create. |
| Law 4 | No duplicate systems. |
| Law 5 | No duplicate owners. |
| Law 6 | No duplicate planners. |
| Law 7 | No duplicate governance. |
| Law 8 | No duplicate execution. |
| Law 9 | No synthetic evidence. |
| Law 10 | Every implementation must increase at least one of: Knowledge, Decision Quality, Outcome Quality, Learning Quality, Operational Maturity, or Automation. Otherwise the implementation should not exist. |
| Law 11 | Production Scale First. Every change must remain efficient, safe, and maintainable at `10,000+` users and `100+` channels. Runtime stays thin; scale work belongs to read models, indexes, background jobs, summaries, and existing owners. |
| Law 12 | Architecture Closed by Default. V7 architecture is complete unless a complete audit proves that existing OMP capabilities, backlog items, runtime model, product specification, canonical policies, canonical owners, SYSTEM_MAP, and Canonical Reference cannot own the finding. |
| Law 13 | Behavior Propagation Law. Every component must change the behavior of another existing component before completion. |
| Law 14 | State Transition Law. Every verified behavior must either change system state or explain why state cannot yet change. |
| Law 15 | Continue OMP Law. If state cannot change, OMP must identify the smallest executable next action through existing owners. |
| Law 16 | Necessity Law. Every owner, capability, function, module, service, CLI, API, read model, dashboard, engineering process, or document must prove why it deserves to exist through the existing Necessity Framework before it can remain permanent. |
| Law 17 | Capability Maturity Protection Law. No Necessity, Merge, Remove, Value Conservation, Collapse, Owner Elimination, Function Elimination, or architectural minimization may alter an element that belongs to an unfinished capability. |
| Law 18 | Engineering Work In Progress Protection Law. No Necessity, Merge, Remove, Value Conservation, Collapse, Owner Elimination, Function Elimination, Module Elimination, Document Elimination, Capability Elimination, or architectural minimization may alter an engineering object that participates in any unfinished engineering lifecycle. |
| Law 19 | Approved Future Dependency Protection Law. No Necessity, Merge, Remove, Value Conservation, Collapse, Owner Elimination, Function Elimination, Module Elimination, Document Elimination, Capability Elimination, or architectural minimization may alter an engineering object that is already required by an approved future execution plan or canonical dependency. |

### Architectural Design Methodology Execution

OMP does not own a separate architectural law.
OMP executes the complete methodology preserved in `docs/reference/V7_CANONICAL_REFERENCE.md` under `ARCHITECTURAL_DESIGN_METHODOLOGY`.

For every meaningful future capability, OMP must prove:

| Review | Required OMP answer |
| --- | --- |
| Product intent | Which Business Objective and Product Scale Objective are affected. |
| Existing owner | Which owner in SYSTEM_MAP, Canonical Reference, OMP, policy, ADR, Runtime Model, Decision Model, or backlog already owns the capability. |
| Work placement | Which plane owns the computation and whether it can safely move earlier. |
| Decision lifecycle | Which objects are born, fresh, stale, invalid, destroyed, committed, or terminal. |
| Certification truth | Which canonical owner declares mandatory, supporting, optional, inventory, or optimization evidence. |
| Runtime time / cost | Which Reaction Latency component and Runtime Cost dimension are affected. |
| Product scale | Whether the design remains suitable for `10,000+` users, `100+` channels, millions of decisions, and long-lived evidence. |
| Safety | Which live gates remain live and what forces `STOP_SAFE`. |
| Automation / authority | Whether the work changes authority, autonomy, runtime apply, or production movement. |
| Execution queue | Which existing backlog item or OMP capability owns the implementation. |

If any answer requires a new owner, new backlog item, new runtime path, or new architecture, OMP must first run Architecture Closed by Default and the Root Cause Engine.

## 2.5. Project Philosophy

V7 is not allowed to become larger unless it first becomes smarter.

This means new architecture is a last resort. The default posture is to make existing owners more capable, more connected, more explainable, and more mature.

## 2.6. Architectural Minimalism

Immutable project law:

A new architectural component may appear only after proving that existing architecture cannot provide the same capability through extension.

Creation priority:

```text
Reuse
  -> Extend
  -> Merge
  -> Implement
  -> Create New
```

New components are forbidden until reuse, extension, and merge options have been explicitly evaluated.

## 2.7. Semantic Reuse Audit

Before every implementation, OMP must execute this audit:

| Step | Requirement | Output |
| --- | --- | --- |
| 1 | Find existing owners. | Owner list. |
| 2 | Find semantically equivalent owners, regardless of name. | Semantic owner list. |
| 3 | Find combinations of existing owners that together already implement the desired capability. | Composition strategy. |
| 4 | Estimate semantic coverage. | Coverage %, owner list, reuse strategy, extension strategy. |
| 5 | Allow new owner only if semantic coverage is insufficient. | `Need New Owner = TRUE/FALSE`. |

Current semantic reuse audit for OMP V2.1:

| Field | Current Value |
| --- | --- |
| Existing owner | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` |
| Semantically equivalent owners | Canonical reference, SYSTEM_MAP, certified reports, ADRs |
| Composition strategy | Extend existing OMP and update reference pointers only |
| Semantic coverage | `100%` |
| Reuse strategy | Reuse OMP as the permanent program owner |
| Extension strategy | Add V2.1 optimizer/minimalism/gate/detector sections in place |
| Need New Owner | `FALSE` |

Current semantic reuse audit for OMP V2.2:

| Field | Current Value |
| --- | --- |
| Desired capability | Add Safety-Bounded Authority as the operating model for separating Knowledge Maturity from Execution Authority. |
| Existing owner | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` |
| Semantically equivalent owners | `docs/reference/V7_ENGINEERING_PRINCIPLES.md`, Canonical Reference, SYSTEM_MAP, Autonomy Blueprint, Ideal Autonomous Routing Model, Knowledge Quality Model, ADR-V7-SAFETY-BOUNDED-AUTHORITY |
| Composition strategy | Extend existing OMP in place and align it with the existing principles/reference/ADR documents. |
| Semantic coverage | `100%` |
| Reuse strategy | Reuse OMP as execution authority; reuse principles/reference/ADR as meaning sources. |
| Extension strategy | Add Safety-Bounded Authority, background/runtime split, safe automatic preparation rule, and Codex execution contract to OMP. |
| Need New Owner | `FALSE` |

Current semantic reuse audit for OMP V2.3:

| Field | Current Value |
| --- | --- |
| Desired capability | Separate permanent Codex operating contract and volatile OMP state from stable scheduler/optimizer rules. |
| Existing owner | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` |
| Semantically equivalent owners | OMP, Canonical Reference, SYSTEM_MAP, ADRs, handoff files, Engineering Principles |
| Composition strategy | Extend OMP in place, add Kernel as the permanent Codex operating contract, add Current Program State as volatile program state, and keep runtime/code owners unchanged. |
| Semantic coverage | `100%` for documentation/control-plane structure |
| Reuse strategy | Reuse OMP as scheduler/optimizer; reuse handoff/current snapshot values as state evidence; reuse reference/ADR map for truth. |
| Extension strategy | Add Kernel/State split section, add pointers, and move volatile packet/state details out of OMP into `docs/programs/V7_CURRENT_PROGRAM_STATE.md`. |
| Need New Runtime Owner | `FALSE` |

Latest semantic reuse audit for optimizer iteration `2026-06-25`:

| Field | Current Value |
| --- | --- |
| Desired capability | Validate the current highest leverage action and execute any safer maturity-gaining portion before the normalized authority gate. |
| Existing owners found | `v7-autonomy-trust-evidence-inventory`, `v7-governed-canary-dry-run-cycle`, `v7-egress-quality-compact`, `v7-service-matrix-refresh-all`, `v7-intelligence-snapshot-refresh`, existing packet/restore/verification/outcome/learning owners. |
| Semantic equivalent owners | Existing service matrix / quality snapshot owners cover service verification and freshness; existing governed canary dry-run covers packet/restore/outcome/learning preview; existing inventory covers OMP recalculation. |
| Composition strategy | Recalculate with inventory, challenge with governed dry-run, execute only existing service/quality/snapshot refresh owners, then recalculate. |
| Semantic coverage | `100%` |
| Reuse strategy | Reuse production owners as-is; no new CLI, API, storage, read model, planner, governance, execution, or truth source. |
| Extension strategy | None required for the safe portion. |
| Need New Owner | `FALSE` |

Historical semantic reuse audit for OMP V3.0:

| Field | Current Value |
| --- | --- |
| Desired capability | Transition V7 from architecture-first continuation to implementation-first production leverage optimization. |
| Existing owner | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` |
| Semantically equivalent owners | `docs/reference/V7_SYSTEM_ARCHITECTURE.md`, `docs/reference/V7_RUNTIME_MODEL.md`, `docs/reference/V7_DECISION_MODEL.md`, `docs/reference/V7_ENGINEERING_PRINCIPLES.md`, `docs/reference/V7_CANONICAL_REFERENCE.md`, `docs/reference/SYSTEM_MAP.md`, relevant ADRs |
| Composition strategy | Extend OMP in place, add `docs/programs/V7_IMPLEMENTATION_PROGRAM.md`, add `docs/reference/V7_IMPLEMENTATION_MODEL.md`, and preserve existing owner boundaries. |
| Semantic coverage | `100%` |
| Reuse strategy | Reuse OMP as implementation optimizer; reuse Current Program State as volatile implementation state; reuse existing runtime/planner/knowledge/learning owners for code work. |
| Extension strategy | Add implementation-first question, implementation classes, implementation prioritization, implementation optimizer, and first production-leverage implementation task. |
| Need New Owner | `FALSE` |

Current semantic reuse audit for OMP V4.0:

| Field | Current Value |
| --- | --- |
| Desired capability | Finalize OMP as the permanent production operating program and single execution program without creating a separate roadmap owner. |
| Existing owner | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` |
| Semantically equivalent owners | `docs/programs/V7_IMPLEMENTATION_PROGRAM.md`, `docs/reference/V7_IMPLEMENTATION_MODEL.md`, `docs/reference/V7_SYSTEM_ARCHITECTURE.md`, `docs/reference/V7_RUNTIME_MODEL.md`, `docs/reference/V7_DECISION_MODEL.md`, `docs/programs/V7_CURRENT_PROGRAM_STATE.md`, Canonical Reference, SYSTEM_MAP, relevant ADRs |
| Composition strategy | Extend OMP in place; keep Implementation Program and Implementation Model as supporting references; keep volatile packet and metrics in Current Program State. |
| Semantic coverage | `100%` |
| Reuse strategy | Reuse OMP as the production operating program; reuse Current Program State as volatile state; reuse existing research, decision, runtime, planner, governance, execution, truth, evidence, and learning owners. |
| Extension strategy | Add production maturity ladder, authority evaluation, continuous optimization, continuous knowledge evolution, and permanent command surface to OMP. |
| Need New Owner | `FALSE` |

### 2.7.1 Necessity Framework Consumption

Status: `CANONICAL_OMP_CONSUMPTION_RULE`.

Canonical framework:

```text
docs/reference/V7_NECESSITY_FRAMEWORK.md
```

OMP does not create a Necessity Engine, Necessity Program, Necessity Planner, Necessity Runtime, new owner, graph, queue, or Candidate type.

OMP consumes the existing Necessity Framework as the mandatory existence filter for:

- owners;
- capabilities;
- functions;
- modules;
- services;
- CLIs;
- APIs;
- read models;
- dashboards;
- engineering processes;
- documents.

Necessity Framework Consumption reuses:

- Behavior Enforcement;
- State Transition Verification;
- Automation Gap Closure;
- Intent Responsibility Resolution;
- Need New Owner Gate;
- Architecture Closed by Default;
- Semantic Reuse Audit;
- BDP candidate production;
- OMP Mission admission.

#### Engineering Work In Progress Protection

Before any Necessity Analysis, Merge Test, Removal Test, Value Conservation, Collapse, Owner Elimination, Function Elimination, Module Elimination, Document Elimination, Capability Elimination, or architectural minimization, OMP must determine whether the object participates in unfinished engineering work.

This is not a Protection Engine, Work Engine, Lifecycle Engine, new owner, new program, Runtime, Planner, graph, queue, or new architecture.

It reuses:

- Capability Lifecycle;
- Mission Lifecycle;
- Implementation Candidate lifecycle;
- Engineering Chain;
- Engineering Chain Dependency Projection;
- `Depends On` and `Unblocks` relationships;
- BDP Discovery outputs;
- OMP Mission admission;
- Automation Gap Closure;
- Intent Responsibility Resolution;
- Behavior Enforcement;
- State Transition Verification;
- Verification;
- Certification;
- Root Cause Engine;
- SYSTEM_MAP owner mapping;
- Current Program State;
- Necessity Framework.

Required pre-check:

| Question | Required answer |
| --- | --- |
| Does the object participate in unfinished engineering work? | `YES`, `NO`, or `UNKNOWN_WITH_REASON`. |
| Which lifecycle is unfinished? | Existing lifecycle name or `NONE`. |
| Which owner owns the unfinished lifecycle? | Existing owner or `UNKNOWN_WITH_REASON`. |
| What is the current lifecycle state? | Existing state from OMP / BDP / Mission / Chain / Verification / Certification / CPS. |
| What must complete before minimization? | Exact completion, closure, verification, certification, consumer, or terminal condition. |
| Is architectural minimization allowed? | `YES` only when no unfinished lifecycle remains. |

An object is protected when at least one of the following is true:

- related Capability is not complete / certified / locked / terminal;
- Mission is active;
- Engineering Chain is not complete;
- Behavior Chain is not `COMPLETE`;
- State Transition is not completed or explained;
- Engineering Intent is not closed;
- `Depends On` is open;
- `Unblocks` is open;
- Implementation Candidate is open, active, held, in progress, reopened, or not terminal;
- object participates in open BDP Discovery;
- object participates in open OMP Mission;
- Verification is unfinished;
- Certification is unfinished;
- Root Cause is active;
- expected Consumer is pending;
- expected Producer is pending;
- integration is unfinished;
- any other existing engineering lifecycle involving the object has not reached its existing terminal state or legal terminal consumer.

If any condition is true, OMP must return:

```text
PROTECTED_BY_ENGINEERING_WORK_IN_PROGRESS
```

`PROTECTED_BY_ENGINEERING_WORK_IN_PROGRESS` is a protection status, not a Necessity verdict and not a new lifecycle state.

While protection is active, OMP must not perform:

- `MERGE`;
- `REMOVE`;
- Collapse;
- Value Conservation;
- Necessity Removal;
- Owner Elimination;
- Function Elimination;
- Module Elimination;
- Document Elimination;
- Capability Elimination;
- any architectural minimization that changes or removes the protected object.

OMP must record:

- protected object;
- unfinished lifecycle;
- lifecycle owner;
- lifecycle state;
- open dependency / producer / consumer / verification / certification / root cause when applicable;
- smallest existing next action;
- exact terminal condition required before minimization can be reconsidered.

If OMP cannot determine whether the object participates in unfinished engineering work, it must not proceed with minimization.

Instead, OMP must route ordinary Implementation Candidate Instance work to resolve missing lifecycle mapping:

```text
Engineering work mapping unknown
  -> BDP candidate production when discovery is required
  -> OMP candidate consumption
  -> Mission Admission
  -> lifecycle mapping correction / hold / rejection / not applicable
  -> verification
  -> Engineering Report
```

Architectural minimization becomes allowed only after the object no longer participates in any unfinished engineering lifecycle.

#### Approved Future Dependency Protection

Before any Necessity Analysis, Merge Test, Removal Test, Value Conservation, Collapse, Owner Elimination, Function Elimination, Module Elimination, Document Elimination, Capability Elimination, or architectural minimization, OMP must determine whether the object is required by an approved future execution plan or canonical dependency.

This is not a Protection Engine, Work Engine, Lifecycle Engine, new owner, new program, Runtime, Planner, graph, queue, or new architecture.

It reuses:

- Approved OMP Mission;
- Approved Implementation Candidate;
- Planned Mission;
- Approved Engineering Chain;
- Approved Capability;
- Planned State Transition;
- Approved Verification;
- Approved Certification;
- Planned Integration;
- Planned Producer;
- Planned Consumer;
- Planned Behavior Chain;
- Planned Runtime Transition;
- `Depends On` and `Unblocks`;
- Engineering Chain Dependency Projection;
- Current Program State;
- SYSTEM_MAP owner mapping;
- OMP Mission admission;
- BDP Candidate evidence;
- Necessity Framework.

Required pre-check:

| Question | Required answer |
| --- | --- |
| Is the object part of an approved future execution plan? | `YES`, `NO`, or `UNKNOWN_WITH_REASON`. |
| Which approved plan requires it? | Approved Mission, Candidate, Chain, Capability, Transition, Verification, Certification, Integration, Producer, Consumer, Behavior Chain, Runtime Transition, dependency, or `NONE`. |
| Which owner approved or accepted the plan? | Existing owner or `UNKNOWN_WITH_REASON`. |
| What future dependency uses the object? | Existing dependency name / edge / plan field. |
| What must complete or be cancelled before minimization? | Plan completion, official cancellation, supersession, rejection, or legal terminal alternative. |
| Is architectural minimization allowed? | `YES` only when no approved future dependency remains. |

An object is protected when it is part of:

- Approved OMP Mission;
- Approved Implementation Candidate;
- Planned Mission;
- Approved Engineering Chain;
- Approved Capability;
- Planned State Transition;
- Approved Verification;
- Approved Certification;
- Planned Integration;
- Planned Producer;
- Planned Consumer;
- Planned Behavior Chain;
- Planned Runtime Transition;
- `Depends On`;
- `Unblocks`;
- Engineering Chain Dependency Projection;
- any other existing canonical dependency accepted for future execution.

If any approved future dependency exists, OMP must return:

```text
PROTECTED_BY_APPROVED_FUTURE_DEPENDENCY
```

`PROTECTED_BY_APPROVED_FUTURE_DEPENDENCY` is a protection status, not a Necessity verdict and not a new lifecycle state.

While protection is active, OMP must not perform:

- `MERGE`;
- `REMOVE`;
- Collapse;
- Value Conservation;
- Necessity Removal;
- Owner Elimination;
- Function Elimination;
- Module Elimination;
- Document Elimination;
- Capability Elimination;
- any architectural minimization that changes or removes the protected object.

Protection may be removed only when the approved future plan:

- completed successfully;
- was officially cancelled through the existing OMP lifecycle;
- was superseded by an approved replacement that no longer requires the object;
- reached a legal terminal alternative.

Protection must not be removed merely because the object has no current runtime use, current consumer, or current downstream value.

OMP must record:

- protected object;
- approved future plan;
- approving / accepting owner;
- dependency type;
- dependency evidence;
- plan state;
- required completion / cancellation / supersession / terminal condition;
- smallest existing next action.

If OMP cannot determine whether the object belongs to an approved future dependency, it must not proceed with minimization.

Instead, OMP must route ordinary Implementation Candidate Instance work to resolve missing future dependency mapping:

```text
Future dependency mapping unknown
  -> BDP candidate production when discovery is required
  -> OMP candidate consumption
  -> Mission Admission
  -> dependency mapping correction / hold / rejection / not applicable
  -> verification
  -> Engineering Report
```

Unified protection rule:

```text
Object is protected if:
  Engineering Work In Progress Protection = PROTECTED_BY_ENGINEERING_WORK_IN_PROGRESS
  OR Approved Future Dependency Protection = PROTECTED_BY_APPROVED_FUTURE_DEPENDENCY
```

Only when both protections are clear may OMP continue to Necessity, Merge, Remove, Value Conservation, or another architectural minimization mechanism.

#### Capability Maturity Protection

Before any Necessity Analysis, Merge Test, Removal Test, Value Conservation, Collapse, Owner Elimination, Function Elimination, or architectural minimization, OMP must determine whether the element belongs to an existing capability.

This is not a Protection Engine, Capability Engine, Lifecycle Engine, Optimization Engine, new owner, Runtime, Planner, graph, queue, or new program.

It reuses:

- Capability Management;
- Capability status values;
- Capability Certification;
- Capability Lock;
- Current Program State capability progress;
- SYSTEM_MAP owner mapping;
- Necessity Framework;
- Architecture Closed by Default;
- Need New Owner Gate;
- Semantic Reuse Audit;
- OMP.

Required pre-check:

| Question | Required answer |
| --- | --- |
| Is the element part of a capability? | `YES`, `NO`, or `UNKNOWN_WITH_REASON`. |
| If yes, which capability? | Existing capability name. |
| What is the capability status? | Existing Capability Management status. |
| Is the capability complete/certified/locked? | `YES`, `NO`, or `UNKNOWN_WITH_REASON`. |
| Is architectural minimization allowed? | `YES` only after completion/certification/lock, otherwise `NO`. |

If the element is not part of a capability, OMP continues with ordinary Necessity Framework Consumption.

If the element is part of a capability whose status is unfinished, OMP must return:

```text
PROTECTED_BY_CAPABILITY_MATURITY
```

`PROTECTED_BY_CAPABILITY_MATURITY` is a protection status, not a Necessity verdict and not a new lifecycle state.

Unfinished capability states include:

- `Idea`;
- `Need Identified`;
- `Creation Justified`;
- `Implemented`;
- `Integrated`;
- `Necessity Verified`;
- `IN_PROGRESS`;
- `OPEN`;
- `PARTIAL`;
- `BLOCKED`;
- `BROKEN`;
- any existing capability status that has not reached capability completion, certification, lock, retirement, or another legal terminal consumer.

While protection is active, OMP must not perform:

- `MERGE`;
- `REMOVE`;
- Collapse;
- Value Conservation;
- Necessity Removal;
- Owner Elimination;
- Function Elimination;
- any architectural minimization that changes or removes the protected element.

OMP must record:

- protected element;
- capability name;
- capability status;
- remaining Definition of Done / certification blocker;
- why the capability is still developing;
- smallest existing next action.

Architectural minimization becomes allowed only when the capability has reached an existing complete or terminal state, such as:

- `COMPLETE`;
- `Capability Certified`;
- `LOCKED`;
- `Capability Locked`;
- `Capability Retired`;
- another existing legal terminal consumer recorded by Capability Management.

If OMP cannot determine whether the element belongs to a capability, it must not proceed with minimization.

Instead, OMP must route ordinary Implementation Candidate Instance work to resolve missing capability mapping:

```text
Capability mapping unknown
  -> BDP candidate production when discovery is required
  -> OMP candidate consumption
  -> Mission Admission
  -> mapping correction / hold / rejection / not applicable
  -> verification
  -> Engineering Report
```

#### Mandatory Necessity Questions

When an element is created, kept permanent, locked, merged, removed, deprecated, made historical, or promoted to canonical status, OMP must answer:

| Question | Required answer |
| --- | --- |
| Why does the element exist? | Existence Justification from the Necessity Framework. |
| What problem does it solve? | Unique engineering problem or `INCOMPLETE_WITH_REASON`. |
| Who consumes it? | Existing consumer owner or `CONSUMER_MISSING`. |
| What happens if it is removed? | Removal Test result. |
| What happens if it is merged into an existing owner? | Merge Test result. |
| Which existing owner can already provide the same value? | Owner name or `NONE_WITH_REASON`. |
| Does its behavior reach Legal Terminal Consumer? | Chain Test result. |

#### Mandatory Necessity Fields

Every Necessity evaluation must record:

| Field | Required value |
| --- | --- |
| `existence_justification` | Unique reason the element exists, not implementation history. |
| `semantic_necessity` | Whether the element produces unique meaning/value. |
| `consumer_value` | Existing consumer and consumed output. |
| `system_effect` | Behavior change, blocked unsafe action, state update, certification, visibility, or `MISSING`. |
| `state_transition_contribution` | `STATE_TRANSITION_COMPLETED`, `STATE_TRANSITION_EXPLAINED`, or blocker. |
| `production_value` | Safety, Reliability, Performance, Knowledge, Decision Quality, Operator Effectiveness, Automation Readiness, Production Maturity, Business Objective, or `MISSING`. |
| `creation_test` | `YES`, `NO`, or `NOT_APPLICABLE_WITH_REASON`. |
| `removal_test` | What becomes impossible if the element is removed. |
| `merge_test` | Existing owner merge possibility or `NO_WITH_REASON`. |
| `chain_test` | Whether behavior reaches Legal Terminal Consumer. |
| `necessity_verdict` | One allowed verdict. |
| `necessity_certification_state` | Existing owner acceptance state. |

#### Allowed Necessity Verdicts

OMP may return only:

| Verdict | Meaning |
| --- | --- |
| `REQUIRED` | Element creates unique downstream value that cannot be safely replaced by an existing owner. |
| `MERGE` | Element is not semantically unique and should be merged into an existing owner. |
| `REMOVE` | Element has no justified remaining purpose and removal does not remove behavior, state transition, or Production Value. |
| `INCOMPLETE` | Element exists but does not yet create complete downstream value. |
| `DEFERRED_BY_REALITY` | Element is necessary in principle, but current production reality does not justify active implementation. |
| `HISTORICAL` | Element is preserved only as evidence and must not act as live owner, Runtime, Planner, roadmap, or truth source. |

Any other result is architecturally incomplete.

#### Necessity Lifecycle Consumption

OMP consumes the existing lifecycle:

```text
Idea
  -> Need Identified
  -> Creation Justified
  -> Implemented
  -> Integrated
  -> Necessity Verified
  -> Necessity Certified
  -> Locked
  -> Deprecated
  -> Historical
  -> Removed
```

Nothing may be created without Creation Test.
Nothing may remain permanent without Necessity Certification.
Nothing may become canonical solely because it was implemented.

#### MERGE / REMOVE Routing

If Necessity verdict is `MERGE` or `REMOVE`, OMP must not create a new Candidate type.

If existing architecture can express the work, OMP routes the result through the ordinary Implementation Candidate Instance path:

```text
Necessity verdict MERGE / REMOVE
  -> BDP candidate production when behaviour/implementation discovery is required
  -> OMP candidate consumption
  -> Mission Admission
  -> implementation / no-change / hold / rejection / not applicable
  -> verification
  -> Engineering Report
  -> canonical owner update or explicit no-change
```

Merge and removal must preserve:

- provenance;
- owner mapping;
- consumer behavior;
- state transition;
- Production Value;
- historical evidence;
- rollback / STOP_SAFE when runtime or production surfaces are affected.

OMP must not remove or merge an element if the Removal Test shows lost required behavior, state transition, Production Value, or legal terminal consumer without a certified replacement.

#### Trigger Rule

Necessity Framework Consumption is mandatory when:

- new owner, capability, function, module, service, CLI, API, read model, dashboard, process, or document is proposed;
- an element is promoted to canonical status;
- an element is locked;
- an element is marked permanent;
- duplicate, overlap, or semantic reuse pressure is detected;
- removal, merge, deprecation, or historical-only status is proposed;
- Value Conservation, Collapse, Owner Elimination, Function Elimination, or architectural minimization is proposed;
- an object may participate in active Mission, open Candidate, incomplete Engineering Chain, incomplete Behavior Chain, open dependency, pending producer/consumer handoff, unfinished Verification, unfinished Certification, active Root Cause, or open BDP Discovery;
- an object may be required by Approved OMP Mission, Approved Implementation Candidate, Planned Mission, Approved Engineering Chain, Approved Capability, Planned State Transition, Approved Verification, Approved Certification, Planned Integration, Planned Producer, Planned Consumer, Planned Behavior Chain, Planned Runtime Transition, Depends On, Unblocks, Engineering Chain Dependency Projection, or another approved future dependency;
- Behavior Propagation, State Transition, Intent Responsibility Resolution, or Automation Gap Closure reveals an element with no verified consumer or no Production Value.

#### Completion Rule

An element is necessity-complete only when:

```text
Existence Justification
  -> Semantic Necessity
  -> Consumer Value
  -> System Effect
  -> State Transition Contribution
  -> Production Value
  -> Creation / Removal / Merge / Chain Test
  -> Necessity Verdict
  -> Necessity Certification
```

If any link is missing, OMP must classify the element as `INCOMPLETE`, `MERGE`, `REMOVE`, `DEFERRED_BY_REALITY`, or `HISTORICAL`, and must record the smallest existing next action.

If Engineering Work In Progress Protection returns `PROTECTED_BY_ENGINEERING_WORK_IN_PROGRESS`, OMP must stop Necessity minimization for that object until every related engineering lifecycle reaches its existing terminal state or legal terminal consumer.

If Approved Future Dependency Protection returns `PROTECTED_BY_APPROVED_FUTURE_DEPENDENCY`, OMP must stop Necessity minimization for that object until the approved future plan completes, is officially cancelled, is superseded by an approved replacement, or reaches a legal terminal alternative.

If Capability Maturity Protection returns `PROTECTED_BY_CAPABILITY_MATURITY`, OMP must stop Necessity minimization for that element until the owning capability is complete, certified, locked, retired, or has another legal terminal consumer.

## 2.8. New Owner Gate

Before creating any new owner, backlog item, policy, runtime path, architectural element, knowledge model, planner, engine, pipeline, API, CLI, storage, snapshot, or truth source, OMP must prove:

```text
Need New Owner = TRUE
Need New Backlog Item = TRUE
Architecture Extension = REQUIRED
```

`Need New Owner` may be true only when existing semantic coverage is insufficient.

If semantic coverage is sufficient, creation is forbidden.

Permanent OMP engineering rule:

```text
Discover
-> Verify
-> Map
-> Reuse
-> Extend Existing
-> Implement
-> Certify
```

Before proposing any new owner, backlog item, policy, runtime path, planner, governance layer, execution path, truth source, or architectural element, OMP must first audit and map the finding to existing canonical ownership.

Required mapping order:

1. OMP Capability
2. Implementation Backlog
3. Canonical Owner
4. Runtime Model
5. Canonical Policy
6. Canonical Reference
7. SYSTEM_MAP or ADR if ownership or decision meaning is involved

Default verdicts:

| Field | Default |
| --- | --- |
| Need New Owner | `FALSE` |
| Need New Backlog Item | `FALSE` |
| Architecture Extension | `LAST_RESORT` |

If an existing owner, capability, backlog item, policy, model, or reference covers the finding, OMP must:

- map the finding to that owner;
- continue through the existing OMP;
- extend the existing owner only;
- avoid creating new architecture, owner, queue, policy, runtime path, planner, governance, execution, or truth source.

Only after complete mapping proves no existing canonical owner, OMP Mission, accepted BDP Implementation Candidate, or backlog registry entry can cover the finding may OMP propose `CREATE_NEW`. That proposal must include proof of impossible reuse and must stop for explicit operator review.

Permanent queue rule:

OMP remains the single execution program.

Implementation Backlog remains the single post-admission engineering registry. OMP Mission admission remains the single route from candidate to implementation.

Reports, policies, reference documents, architecture documents, and canonical knowledge never generate implementation work directly. They may only update canonical owners or implementation registry state through OMP. BDP may generate Implementation Candidates, but OMP must admit them before implementation.

Required gate output:

| Field | Required |
| --- | --- |
| Desired capability | Clear capability statement. |
| Existing semantic coverage | Percent and evidence. |
| OMP Capability mapping | Existing capability or `NONE_PROVEN`. |
| Implementation Backlog mapping | Existing backlog item or `NONE_PROVEN`. |
| Canonical Owner mapping | Existing canonical owner or `NONE_PROVEN`. |
| Runtime Model mapping | Existing runtime section or `NONE_PROVEN`. |
| Canonical Policy mapping | Existing policy or `NONE_PROVEN`. |
| Canonical Reference mapping | Existing canonical section or `NONE_PROVEN`. |
| Reuse candidate owners | List. |
| Extension strategy | How existing owners can be extended. |
| Merge strategy | How duplicate/overlapping owners can be merged. |
| Need New Owner | `TRUE` or `FALSE`. |
| Need New Backlog Item | `TRUE` or `FALSE`. |
| Architecture Extension | `NONE`, `EXTEND_EXISTING`, or `LAST_RESORT`. |
| Decision | `REUSE`, `EXTEND`, `MERGE`, or `CREATE_NEW`. |

Current gate result:

| Field | Current Value |
| --- | --- |
| Need New Owner | `FALSE` |
| Reason | OMP V2.1 is fully expressible by extending the existing OMP document and existing reference pointers. |

## 2.9. Architectural Duplication Detector

After every implementation, OMP must check for duplication across:

- duplicate owners;
- duplicate planners;
- duplicate governance;
- duplicate execution;
- duplicate lifecycle;
- duplicate APIs;
- duplicate CLI;
- duplicate knowledge models;
- duplicate routing logic;
- duplicate learning logic;
- duplicate truth sources;
- duplicate evidence collectors;
- duplicate packet builders;
- duplicate decision surfaces;
- duplicate maturity models.

Detector verdicts:

| Verdict | Meaning |
| --- | --- |
| `NONE` | No duplication detected. |
| `MERGE_REQUIRED` | Overlap exists and a safe merge path should be implemented. |
| `REMOVE_DUPLICATION` | Duplication is unsafe or already harmful and must be removed. |

If duplication exists and safe merge is possible, implement the merge before adding more capability.

Current detector result:

| Field | Current Value |
| --- | --- |
| Duplicate owners | `NONE` |
| Duplicate planners | `NONE` |
| Duplicate governance | `NONE` |
| Duplicate execution | `NONE` |
| Duplicate truth sources | `NONE` |
| Duplicate maturity models | `NONE` |
| Verdict | `NONE` |

## 2.10. Implementation Prioritization Rules

OMP must choose implementation work in this order:

| Priority | Class | Rule |
| --- | --- | --- |
| A | Existing owner implementation | Implement missing behavior inside the existing owner first. |
| B | Existing owner integration | Connect existing owners when the behavior already exists but is disconnected. |
| C | Existing owner optimization | Improve correctness, safety, speed, or clarity inside an existing owner. |
| D | Read-model improvements | Add read-only fields or summaries that help existing owners decide, stop, verify, or learn. |
| E | Testing | Add focused tests for implemented behavior, state transitions, safety, idempotency, and stop reasons. |
| F | Certification | Certify the implemented behavior with truth, convergence, and project-specific verification. |

Never redesign architecture unless implementation evidence proves `FUNDAMENTAL_ARCHITECTURE_GAP`.

## 2.11. Implementation Classes

Every future implementation task must be classified as exactly one primary implementation class:

| Class | Meaning |
| --- | --- |
| `IMPLEMENT_RUNTIME` | Runtime lifecycle, wakeup, stop, idempotency, verification, rollback, OMP notification, or runtime preview behavior through existing owners. |
| `IMPLEMENT_BACKGROUND` | Background knowledge, snapshots, intelligence, trust, suitability, prediction, service, route, capacity, or evidence processing. |
| `IMPLEMENT_READ_MODEL` | Read-only surfaces that expose state, decisions, safety, authority, verification, learning, or operator visibility. |
| `IMPLEMENT_TEST` | Tests, fixtures, regression coverage, state-machine coverage, or safety/idempotency coverage. |
| `IMPLEMENT_VERIFICATION` | Verification logic, read-only checks, convergence gates, truth checks, readiness checks, or post-action validation. |
| `IMPLEMENT_OBSERVABILITY` | Lifecycle ids, stage visibility, stop reasons, audit records, operator traces, or non-truth-source observability. |
| `IMPLEMENT_UI` | Operator-facing UI work that consumes existing truth/read models without becoming a decision owner. |
| `IMPLEMENT_DOCUMENTATION` | Documentation required by an implementation, never a substitute for implementation. |
| `IMPLEMENT_CERTIFICATION` | Certification reports, truth/convergence confirmation, and release readiness after implemented behavior. |

Documentation-only tasks may support implementation, but they are not the implementation optimizer target unless documentation is the actual highest production-leverage work.

## 2.12. Implementation Optimizer

OMP optimizes Production Leverage.

Production Leverage means the expected improvement to production autonomy, safety, verifiability, learning, operator effectiveness, or implementation readiness per unit of risk and effort.

Ranking inputs:

1. current bottleneck;
2. current authority class;
3. current reality limit;
4. existing owner availability;
5. production safety;
6. expected maturity gain;
7. implementation effort;
8. reversibility;
9. testability;
10. truth/convergence impact;
11. whether the task moves V7 toward Production Autonomy without crossing forbidden boundaries.

Canonical Policy Library Stage 4 adds a permanent backlog-backed selection rule:

```text
Read Implementation Backlog
  -> Apply Implementation Priority Model
  -> Select highest-priority unfinished item
  -> Semantic Reuse Audit
  -> Reuse existing owner
  -> Implement
  -> Test
  -> Verify
  -> Truth
  -> Convergence
  -> Certification if required
  -> Mark backlog item DONE
  -> Recalculate backlog
  -> Continue
```

The implementation backlog is:

```text
docs/programs/V7_IMPLEMENTATION_BACKLOG.md
```

The priority model is:

```text
docs/reference/V7_IMPLEMENTATION_PRIORITY_MODEL.md
```

OMP must not select implementation work by document order.
OMP must select by production leverage.
If the highest item crosses authority, real-world, unsafe-implementation, or fundamental-architecture boundaries, OMP stops with the exact stop condition and may choose the next highest item only when the blocked item cannot progress.

Current backlog progress:

| Scope | Complete | Total | Status |
| --- | ---: | ---: | --- |
| Tier A | `6` | `6` | `COMPLETE` |
| Tier B | `21` | `21` | `COMPLETE` |
| Tier C | `6` | `7` | `IN_PROGRESS` |
| Tier D optional | `0` | `6` | `OPTIONAL` |
| Overall actionable | `34` | `34` | `COMPLETE` |

Implementation maturity:

```text
100.0%
```

Estimated remaining effort:

```text
None for actionable backlog
```

Next backlog item:

```text
IMPLEMENTATION_COMPLETE
```

## 2.12.1. Engineering and Production Maturity

Permanent maturity model:

```text
docs/reference/V7_PRODUCTION_MATURITY_MODEL.md
```

OMP must track two independent maturity dimensions:

1. `ENGINEERING MATURITY`
2. `PRODUCTION MATURITY`

Engineering Maturity measures completed engineering knowledge.

Production Maturity measures production readiness.

Engineering completion does not imply production autonomy.

Production Maturity must increase only through real implementation, deploy, testing, verification, certification, production outcomes, authority decisions, and certified autonomy.

Backlog completion must increase only Production Maturity.

Reference documents must never change Engineering Maturity after certification unless industry consensus changes, implementation proves `FUNDAMENTAL_ARCHITECTURE_GAP`, or the operator explicitly requests a reference update.

OMP must recalculate both maturity dimensions after every:

- implementation;
- deploy;
- truth;
- convergence;
- certification;
- production outcome;
- authority decision.

Engineering Maturity is the weighted total of:

- Architecture;
- Decision Model;
- Runtime Model;
- System Architecture;
- Research;
- Canonical Policies;
- OMP.

Production Maturity is the weighted total of:

- Implementation;
- Production Deployment;
- Testing;
- Certification;
- Authority Evolution;
- Production Outcomes;
- Production Autonomy;
- Implementation Backlog Completion.

Current engineering snapshot:

| Category | Current % | Target % | Weight |
| --- | ---: | ---: | ---: |
| Architecture | `100` | `100` | `15` |
| Decision Model | `100` | `100` | `15` |
| Runtime Model | `100` | `100` | `15` |
| System Architecture | `100` | `100` | `15` |
| Research | `100` | `100` | `15` |
| Canonical Policy Library | `100` | `100` | `15` |
| OMP | `100` | `100` | `10` |

Engineering Maturity:

```text
Current: 100.0%
Status: ENGINEERING_COMPLETE
```

Current production snapshot:

| Category | Current % | Target % | Weight |
| --- | ---: | ---: | ---: |
| Implementation | `100.0` | `100` | `20` |
| Testing | `74` | `100` | `10` |
| Production Deployments | `100` | `100` | `10` |
| Production Outcomes | `25` | `100` | `15` |
| Certification | `95` | `100` | `15` |
| Authority Evolution | `15` | `100` | `10` |
| Production Autonomy | `0` | `100` | `10` |
| Implementation Backlog Completion | `100.0` | `100` | `10` |

Production Maturity:

```text
Current: 66.9%
Target: 100%
Remaining: 33.1%
```

Backlog:

```text
Tier A: 6 / 6 complete
Tier B: 21 / 21 complete
Tier C: 7 / 7 complete
Tier D: 0 / 6 optional complete
Overall: 34 / 34 actionable complete
```

Current highest implementation task:

```text
IMPLEMENTATION_COMPLETE
```

Estimated remaining effort:

```text
None for actionable backlog
```

Current autonomy tier:

```text
TIER_1_GOVERNED
```

Next milestone:

```text
80%: Runtime Production Ready
```

Milestones:

Engineering milestones finish at:

```text
ENGINEERING_COMPLETE
```

Production milestones finish at:

```text
PRODUCTION_AUTONOMY_CERTIFIED
```

| Production milestone | Meaning |
| ---: | --- |
| `20%` | First Implementation Certified |
| `35%` | Runtime Eligibility Implemented |
| `50%` | Implementation Half Complete |
| `65%` | Certification Half Complete |
| `80%` | Runtime Production Ready |
| `90%` | Bounded Production Autonomy |
| `100%` | Production Autonomy Certified |

## 2.12.2. V7 Production Status

OMP must print this block after every execution:

### 2.12.2.1 Historical Production Status Example

Classification: `HISTORICAL_EXAMPLE`.
Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

```text
V7 PRODUCTION STATUS

ENGINEERING

Architecture
100%

Research
100%

Policies
100%

Engineering Maturity
100.0%

PRODUCTION

Implementation
100.0%

Certification
95%

Autonomy
0%

Production Maturity
66.9%

Overall Status
ENGINEERING_COMPLETE / PRODUCTION_IN_PROGRESS

Current Focus
IMPLEMENTATION_COMPLETE

Backlog
Tier A
6 / 6
Tier B
21 / 21
Tier C
7 / 7
Tier D
0 / 6 optional
Overall
34 / 34 complete

Current Tier
TIER_1_GOVERNED

Highest Priority Task
IMPLEMENTATION_COMPLETE

Status
C7 DONE_READ_ONLY / ACTIONABLE BACKLOG COMPLETE

Authority
No expansion active

Required Action
No actionable implementation item remains. Continue only for status reporting or explicit operator-approved new scope.

Engineering
READY

Runtime
READY_READ_ONLY

Packet
NONE_ACTIVE

Estimated Remaining Work
None for actionable implementation backlog

Expected Next Milestone
80%: Runtime Production Ready
```

### 2.12.2.2 Permanent Production Status Rules

Classification: `PERMANENT_RULE`.

Progress calculation must be automatic.
The displayed percentage must come from `docs/reference/V7_PRODUCTION_MATURITY_MODEL.md`.
Backlog progress must come from `docs/programs/V7_IMPLEMENTATION_BACKLOG.md`.
Current volatile state must come from `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

OMP must recalculate Production Status after:

- backlog completion;
- deploy;
- truth;
- convergence;
- certification;
- production outcome;
- authority decision.

Current focus values:

- `IMPLEMENTATION`
- `IMPLEMENTATION_COMPLETE`
- `CERTIFICATION`
- `AUTHORITY`
- `AUTONOMY`
- `PRODUCTION`

Focus transition:

```text
IMPLEMENTATION
  -> IMPLEMENTATION_COMPLETE
  -> CERTIFICATION
  -> AUTHORITY EVOLUTION
  -> PRODUCTION AUTONOMY
  -> CONTINUOUS IMPROVEMENT
```

Completion outputs:

| Condition | OMP output |
| --- | --- |
| Every mandatory implementation item is complete | `IMPLEMENTATION_COMPLETE` |
| Every certification is complete | `CERTIFICATION_COMPLETE` |
| Bounded autonomy is certified | `PRODUCTION_AUTONOMY_READY` |
| Production autonomy is certified | `PRODUCTION_AUTONOMY_CERTIFIED` |

Future normal operator commands:

- `Continue OMP`
- `Status`
- `Approve packet`
- `Approve authority expansion`

OMP must never request a new roadmap.
OMP must never request a new implementation plan.
OMP must continue using the existing backlog until completion.

## 2.12.3. Capability Management

OMP is capability-oriented.

Tasks are the execution unit.

Capabilities are the maturity unit.

OMP must always know:

1. what capability is currently being built;
2. how complete it is;
3. what blocks completion;
4. which backlog items belong to it;
5. when it becomes `COMPLETE`;
6. when it becomes `LOCKED`;
7. when future work is forbidden unless a re-open trigger is present.

No capability may remain permanently `IN_PROGRESS`.

Every capability record must contain:

- Capability Name;
- Purpose;
- Ideal Target State;
- Current State;
- Current %;
- Target %;
- Definition of Done;
- Completed Criteria;
- Remaining Criteria;
- Blocking Backlog Items;
- Expected Completion Point;
- Canonical Owner;
- Production Value;
- Autonomy Impact;
- Output Produced;
- Output Available;
- Consumer;
- Output Consumed;
- Consumption Verified;
- Behavior Changed;
- Next Output;
- Terminal Consumer;
- Production Promotion State;
- Current Status;
- Re-open Triggers.

Capability status values:

| Status | Meaning |
| --- | --- |
| `IN_PROGRESS` | The capability has unfinished Definition of Done criteria or unfinished required backlog items. |
| `COMPLETE` | Every Definition of Done criterion has completion evidence, Output Produced is `PASS`, Output Consumed is `PASS`, Consumption Verified is `PASS`, Behavior Changed is `PASS`, Next Output Produced is `PASS`, executable closure is `PASS`, consumer chain is `PASS`, Terminal Consumer Verified is `PASS`, Production Promotion is `PASS` when the capability requires production certification, and Capability Certification is accepted by the existing certification owner. |
| `LOCKED` | The capability is complete, canonical, and future engineering is prohibited unless a re-open trigger is present. |

General capability rules:

1. Every backlog item must belong to at least one capability.
2. OMP must maintain `Capability -> Backlog Items -> Current % -> Remaining % -> Expected Completion`.
3. OMP must calculate capability progress from Definition of Done criteria and existing backlog status.
4. OMP must not invent work to fill a capability.
5. OMP must use only the existing backlog, existing policies, existing Runtime, and existing canonical knowledge.
6. After every completed backlog item, OMP must update capability progress in Current Program State.
7. If a Definition of Done becomes satisfied, OMP must mark the capability `COMPLETE`, then `LOCKED`, then update Canonical Reference.
8. Locked capabilities may be reopened only if production evidence disproves the capability, architecture materially changes, or the operator explicitly requests reopening.
9. Capability Progress Reports are historical engineering reports only; they must never become a second backlog or roadmap.
10. Every capability must define how Runtime, OMP, operators, or knowledge owners behave when the capability reaches `100%`.
11. OMP must never stop because implementation code exists or tests pass alone.
12. OMP may stop only when Capability Closure is complete or when an allowed stop condition is reached.
13. A capability remains `OPEN`, `PARTIAL`, `BLOCKED`, or `BROKEN` if any output is read-model-only, diagnostic-only, report-only, documentation-only, placeholder-only, future-work-only, manually bridged, or orphaned.
14. Capability Closure requires:

```text
Design
  -> Implementation
  -> Output Produced
  -> Output Consumed
  -> Consumption Verified
  -> Runtime Consumption
  -> Behavior Changed
  -> Verification
  -> Rollback or Success
  -> Learning
  -> Evidence
  -> Production Maturity
  -> OMP
  -> Capability State
  -> Next Runtime Cycle
```

15. If any transition in the Capability Closure chain is not applicable, the capability must record the legal terminal consumer that replaces it: Runtime Ready For Next Cycle, Capability Certified, Production Maturity Updated, OMP Next Step Produced, Capability Locked, Capability Retired, Terminal `STOP_SAFE`, `ENGINEERING_AUTHORITY`, `OPERATIONAL_AUTHORITY`, or `REAL_WORLD_LIMIT`.
16. A capability must not reach `COMPLETE` because an implementation, read model, diagnostic, dashboard, report, or API response exists. It reaches `COMPLETE` only after the next executable owner consumed the output and changed behavior.
17. If the old L3 pattern appears again, where implementation code, diagnostics, reports, or read models exist but Runtime, OMP, Learning, Certification, or the next capability has not verifiably consumed them, OMP must classify the capability as `PARTIAL` or `BROKEN`, never `COMPLETE`.
18. Engineering Complete alone is never a terminal capability state when the capability is intended for production behavior. The capability must pass Production Promotion, Capability Certification, Production Maturity consumption, and Current Program State propagation, or stop at a legal terminal condition with reason.
19. Production Candidate is an OMP lifecycle state only. It means the intended capability output has passed implementation/test evidence and is ready to be sealed into canonical source through existing safe commit, safe push, truth, safe deploy, and convergence owners. It creates no deployment mechanics, owner, lifecycle, runtime path, authority, or document.
20. The Production Promotion Matrix in the Capability Production Contract applies to L3, L4, L5, L6, L7, and any future capability. Capability-specific documents may define validation evidence, but OMP owns the reusable promotion sequence.

#### Capability Closure Versus Implementation Complete Reconciliation Rule

Status: `CANONICAL_EXISTING_OWNER_INTEGRATION`.

Before OMP accepts `IMPLEMENTATION_COMPLETE` or a global `REAL_WORLD_LIMIT`, it must reconcile every unfinished CPS capability criterion against its current owner, actionable Backlog state, producer/consumer closure, Behavior Chain, State Transition, Engineering Intent Closure, certification, Production Maturity consumption and exact legal terminal consumer.

Each current criterion must have exactly one primary classification: engineering implementation, integration, verification, certification, consumption, intent closure or canonical reconciliation remaining; real-world evidence; operational or engineering Authority; production certification; dependency wait; stale completed projection; not applicable; or unknown with reason.

`34/34 actionable COMPLETE` proves only that the current implementation backlog has no unfinished actionable item. A `DONE` item cannot close a capability unless the capability output is consumed, consumption is verified, behavior changes, the next output is produced, Engineering Intent closes and the legal terminal consumer accepts the result. Conversely, a completed backlog ID must not remain a live blocker merely because a historical capability table was not refreshed.

Any safe engineering classification enters the existing responsibility -> BDP when Discovery is required -> Candidate -> OMP admission -> Mission -> Codex -> verification -> intent closure path. Real-world, Authority and dependency waits remain capability-local while any independent criterion is READY. Unknown or contradictory classification stops safely. No parallel registry, backlog, queue, scheduler, owner, Planner, Runtime, Engine or lifecycle is created.

Capability Dashboard must be printed from the sole volatile owner:

```text
Capability Dashboard Source: CPS Authoritative Unfinished Capability Closure Registry
Live values: docs/programs/V7_CURRENT_PROGRAM_STATE.md
Scheduling authority: CPS-derived READY frontier consumed by OMP
Historical OMP capability tables: context only; no current-state or scheduling authority
```

#### Program Execution And Consumption Reconciliation Rule

Status: `CANONICAL_EXISTING_OWNER_INTEGRATION`.

Before OMP accepts a program completion claim, `IMPLEMENTATION_COMPLETE`, `GLOBAL_ENGINEERING_TERMINAL` or a global `REAL_WORLD_LIMIT`, it must reconcile every current canonical program and mandatory stage against the program's existing execution owner, state owner, acceptance owner, required outputs, required consumers, state transition and legal terminal evidence.

Program document status and program execution status are separate. `ORGANIZED`, `READY`, `CANONICAL`, `ACTIVE`, an existing report, an implemented adapter, isolated tests or a completed implementation backlog do not prove that a program was activated, executed, accepted, consumed or terminally closed. A program file cannot certify its own execution merely by declaring a status.

Functional footprint is part of completion evidence. OMP must prove all of: `REAL_TRIGGER_OCCURRED`, `REAL_ENTRYPOINT_INVOKED`, `RECONCILIATION_CALLED`, `CONSUMER_INVOKED`, `CONSUMER_BEHAVIOR_CHANGED`, and `NEXT_OUTPUT_CREATED`. A test call, shell call, manual Codex continuation, deployed library, paused automation or report claim cannot substitute for any missing proof. When no real caller exists, the maximum legal state is `IMPLEMENTED_MANUALLY_CALLABLE`; the next stage remains blocked and CPS must expose the exact activation boundary.

Every mandatory stage must resolve to exactly one current execution state: not activated; ready; in progress; output missing; ready for acceptance; acceptance missing; consumer missing; consumption unconfirmed; complete and consumed; blocked by a real-world, Authority or dependency boundary; not applicable; superseded; or unknown with reason. A stage is complete only when its entry conditions passed, required output exists and validates, independent acceptance/lock obligations passed, the named consumer confirmed consumption, the state transition completed and the next output or legal terminal alternative exists.

Program-level producer/consumer closure follows the existing route:

```text
Stage 2 Locked Knowledge
  -> AEP Foundation / accepted ideal model
  -> Current Autonomous Behaviour Reality through existing BDP discovery
  -> Certified Autonomous Behaviour Gap Register
  -> OMP Mission Generation and Admission
  -> existing-owner Implementation and Verification
  -> Production Certification and Production Maturity
  -> CPS
  -> AEP continuous evolution / OMP continuation
```

Any safe incomplete program stage enters the existing OMP execution frontier and preempts capability-local waits without erasing or reordering protected capability WIP. Broken output consumption is routed through existing owners; BDP is invoked only when fresh discovery is required. Global `REAL_WORLD_LIMIT` is legal only when no independent program stage is ready, in progress, acceptance-ready, or safely consumer-repairable. CPS is the sole volatile owner of the current program stage and program execution frontier. No parallel program registry, roadmap, backlog, queue, scheduler, Planner, Runtime, owner, lifecycle or truth source is created.

#### Mission Completion Evidence Gate

Status: `ACTIVE_EXISTING_OWNER_INTEGRATION`.

Before OMP, AEP, BDP, CPS or a capability owner promotes a Mission to `COMPLETE`, `COMPLETE_CONSUMED`, `LOCKED`, `AUTOMATION_ACTIVE`, `PHASE_COMPLETE`, `CAPABILITY_COMPLETE` or `PROGRAM_TERMINAL`, the Mission must declare one primary contract: `ANALYSIS_COMPLETION`, `DISCOVERY_COMPLETION`, `ACCEPTANCE_COMPLETION`, `DOCUMENTATION_COMPLETION`, `IMPLEMENTATION_COMPLETION`, `INTEGRATION_COMPLETION`, `AUTOMATION_COMPLETION`, `RUNTIME_COMPLETION` or `PRODUCTION_COMPLETION`.

The machine-checkable owner is `tools/v7_sync_lib.py::mission_completion_evidence_gate`, consumed by `omp_functional_footprint_consistency` and the existing `v7-truth-check` CPS path. It checks applicable real caller, consumer, behavior change, next output, deployment, Runtime, Production and legal-terminal evidence. Missing evidence fails closed to `PREPARED_NOT_CONSUMED`, `IMPLEMENTED_NOT_CONSUMED`, `INTEGRATION_INCOMPLETE`, `AUTOMATION_INCOMPLETE`, `RUNTIME_INCOMPLETE`, `PRODUCTION_INCOMPLETE` or `COMPLETION_TRUTH_UNRESOLVED`.

Forbidden direct promotions:

```text
TESTS_PASS -> COMPLETE_CONSUMED
DEPLOYED -> AUTOMATION_ACTIVE
REPORT_CREATED -> CONSUMER_CONFIRMED
MANUAL_CODEX_RUN -> SELF_CONTINUATION_ACTIVE
```

Acceptance and lock are not demoted for lacking Runtime effect when Runtime is outside their declared contract. An exact owner-backed legal terminal may close a Mission without implementation, but cannot claim a stronger effect class. Reports remain historical evidence; current caller and consumer truth wins. No new engine, owner, lifecycle, registry, queue, scheduler, Runtime, Planner or truth source is created.

Historical capability baseline (non-authoritative; retained for provenance only):

This baseline records the state when Capability Management was introduced. It has `scheduling_authority=NONE`, must not be read as current `IN_PROGRESS` state, and cannot override the CPS Authoritative Unfinished Capability Closure Registry.

| Capability | Purpose | Current % | Target % | Current Status | Canonical Owner | Production Value | Autonomy Impact | Blocking Backlog Items | Expected Completion Point | Re-open Triggers |
| --- | --- | ---: | ---: | --- | --- | --- | --- | --- | --- | --- |
| Movement Protection | Prevent chaotic user movement while preserving fast reaction to real failures. | `83.0` | `100` | `IN_PROGRESS` | OMP, Movement Protection Model, Runtime Model, Canonical Policy Library | `VERY_HIGH` | `VERY_HIGH` | Future authority/runtime/certification and production outcome evidence | Actionable implementation prerequisites are complete through C7; movement remains blocked until certified authority/runtime scope exists. | Production evidence disproves behavior; planner/runtime architecture materially changes; explicit operator request. |
| Runtime Eligibility | Decide whether Runtime may execute or must stop using certified gates. | `61.0` | `100` | `IN_PROGRESS` | Runtime Model, OMP, delegated policy preview, action-class enablement owners | `VERY_HIGH` | `VERY_HIGH` | `B17`, `B18`, `C1`, `C6` | Action-class runtime eligibility arbitration is implemented; freshness/reporting semantics remain to be certified. | Runtime architecture changes; production eligibility failure; explicit operator request. |
| Authority Evolution | Move from packet approval to bounded class/policy authority without silent expansion. | `68.0` | `100` | `IN_PROGRESS` | OMP, Authority policy, Runtime Model, action-class ladder | `VERY_HIGH` | `VERY_HIGH` | `B12`, `B16`, `B21`, `C3`, `C4` | Certified class evidence supports authority recommendation and operator/certified policy approval. | Authority incident; operator policy change; explicit authority expansion/shrink request. |
| Rollback | Guarantee safe compensation or certified no-rollback behavior for production actions. | `49.0` | `100` | `IN_PROGRESS` | Restore barrier, rollback manifest, Runtime Model, execution feedback | `VERY_HIGH` | `HIGH` | `A3`, `B15`, `B16` | Rollback/no-rollback class evidence and automatic rollback authority are certified; C5 compensation semantics are complete. | Failed rollback; verification failure pattern; explicit operator request. |
| Recovery Admission | Admit recovered channels safely without oscillation or premature scale. | `78.0` | `100` | `IN_PROGRESS` | Recovery admission owner, service matrix, quality compact, blast-radius/action-class ladder | `HIGH` | `HIGH` | `D2`, `D3` if optional recovery scope changes | Repeated real readiness evidence, observation windows, and read-only slow-start progression are complete; runtime consumption remains future authority/implementation work. | Recovery incident; service evidence changes; explicit operator request. |
| Learning | Convert real outcomes into future decision quality without synthetic evidence. | `63.0` | `100` | `IN_PROGRESS` | Feedback/learning owner, OMP, Canonical Reference | `VERY_HIGH` | `VERY_HIGH` | `A3` | Representative real outcomes and metric reliability support promotion recommendations. | Learning regression; synthetic evidence risk; explicit operator request. |
| Production Readiness | Make V7 deployable, operable, verifiable, and certifiable as a production system. | `66.9` | `100` | `IN_PROGRESS` | OMP, Production Maturity Model, Implementation Backlog | `VERY_HIGH` | `HIGH` | Future authority/runtime/certification and production outcome evidence; optional `D1`-`D6` only if scope changes | Production Maturity reaches `100%` and outputs `PRODUCTION_AUTONOMY_CERTIFIED`. | Production safety incident; deploy model change; explicit operator request. |
| Production Autonomy | Enable Runtime to operate inside certified authority while operator supervises. | `0.0` | `100` | `IN_PROGRESS` | OMP, Runtime Model, Authority Evolution, action-class promotion | `VERY_HIGH` | `VERY_HIGH` | `A3`, `A4`, `A5`, `A6`, `B10`, `B12`, `B16`, `C4` | Bounded autonomy and then production autonomy are certified by real outcomes and approved authority. | Autonomy incident; authority policy change; explicit operator request. |
| Knowledge System | Preserve verified project knowledge and prevent repeated rediscovery. | `100.0` | `100` | `LOCKED` | Canonical Reference, Context Resolver, Research Framework, Policy Library, Document Lifecycle | `HIGH` | `MEDIUM_HIGH` | None current. | Current knowledge owners remain canonical and read-only under document lifecycle rules. | Industry consensus changes; `FUNDAMENTAL_ARCHITECTURE_GAP`; explicit operator request. |
| Observability | Expose enough read-only truth for operators, OMP, Runtime, and certification. | `35.0` | `100` | `IN_PROGRESS` | Admin read models, trust/evidence inventory, truth/convergence | `HIGH` | `MEDIUM_HIGH` | `B1`, `B4`, `B9`, `B15`, `B17`, `C2` | Read-only evidence shows eligibility, rollback, stale reads, promotion quality, and runtime readiness. | Operator cannot diagnose; evidence disagreement; explicit operator request. |
| Decision Explainability | Explain existing Runtime / OMP decisions to the operator before any approval request. | `25.0` | `100` | `IN_PROGRESS` | OMP, Current Program State, Runtime Model, evidence read models | `HIGH` | `HIGH` | `B1`, `B4`, `B13`, `B15`, `B17`, `C2` | Every approval request explains reason, evidence, expected value, risks, alternatives, and capability impact in Russian before Approve / Reject. | Operator cannot understand approval reason; explanation contradicts evidence; explicit operator request. |
| Implementation Discipline | Ensure work flows only through OMP Mission admission, Backlog registry, Priority Model, tests, truth, convergence, deployment, and certification. | `100.0` | `100` | `COMPLETE` | OMP, Implementation Backlog, Implementation Priority Model, Current Program State | `VERY_HIGH` | `MEDIUM` | None current. | OMP + Mission admission + Backlog registry + Current Program State remain sufficient for execution. | OMP Mission admission is bypassed; a parallel queue appears; operator requests process change. |
| Engineering Knowledge Preservation | Freeze certified reference knowledge and keep reports/ADRs from becoming roadmaps. | `100.0` | `100` | `LOCKED` | Document Lifecycle, Canonical Reference, SYSTEM_MAP | `HIGH` | `MEDIUM` | None current. | Reference, report, ADR, policy, and backlog roles remain normalized. | Reference contradiction; material architecture change; explicit operator request. |

Ideal Target State by capability:

| Capability | Ideal Target State |
| --- | --- |
| Movement Protection | Runtime evaluates current state, candidate quality, failure/degradation, freshness, recovery, blast radius, rollback, anti-flap, authority, State Change Cost, and Net Benefit before any movement; it moves only when `NET_BENEFIT > CHANGE_COST`, otherwise it keeps the current state. |
| Runtime Eligibility | Runtime consumes prepared certified decisions and fresh evidence, then returns `EXECUTE` or `STOP_SAFE`; it never invents decisions, bypasses policy, or mutates from stale/unknown evidence. |
| Authority Evolution | Operators approve policy, class, or authority boundaries; Runtime self-approves only operational decisions inside approved bounds; authority expansion never happens silently. |
| Rollback | Every production action has rollback ready or certified no-rollback semantics before execution; verification failure leads to rollback or explicit safe stop through existing owners. |
| Recovery Admission | Recovered channels re-enter through repeated readiness evidence, observation windows, bounded blast radius, and runtime-certified slow start instead of immediate full trust. |
| Learning | Only real observed outcomes update knowledge, confidence, suitability, promotion readiness, and future decisions; synthetic evidence is never accepted. |
| Production Readiness | V7 is deployable, testable, observable, certifiable, and operationally safe; OMP can move from implementation through certification and authority evolution to production autonomy. |
| Production Autonomy | Runtime executes certified action classes inside delegated policy; the operator supervises, approves expansion, and handles exceptional cases. |
| Knowledge System | Canonical Reference, SYSTEM_MAP, Context Resolver, Research Framework, Policy Library, and Document Lifecycle preserve verified knowledge and prevent rediscovery or duplicate owners. |
| Observability | Operators, OMP, and Runtime can inspect liveness, degradation, recovery, rollback, stale reads, eligibility, promotion readiness, and evidence quality without mutation. |
| Decision Explainability | Operators receive a Russian, evidence-linked explanation of every approval request before Approve / Reject; the explanation covers reason, timing, user, source, target, passed gates, alternatives, risks, confidence, production value, and capability progress. |
| Implementation Discipline | OMP always selects the highest unfinished backlog item, uses existing owners, verifies with tests/truth/convergence, marks completion, recalculates capability progress, and continues or stops only at allowed boundaries. |
| Engineering Knowledge Preservation | Durable knowledge is promoted from reports into canonical owners; reports remain evidence, ADRs remain decisions, references remain knowledge, and Backlog remains the post-admission implementation registry. |

Definition of Done by capability:

Definitions are durable. The `Completed Criteria` and `Remaining Criteria` columns below are the non-authoritative baseline captured when Capability Management was introduced. Current criterion classification, blockers, waits, percentages and closure state are owned only by the CPS Authoritative Unfinished Capability Closure Registry and its named capability owners.

| Capability | Definition of Done | Completed Criteria | Remaining Criteria |
| --- | --- | --- | --- |
| Movement Protection | Hard Failure certified; Soft Degradation certified; Recovery Admission certified; Freshness integrated; Rollback certified; Blast Radius certified; Anti-Flap certified; Stickiness implemented; Minimum Improvement Threshold implemented; State Change Cost Model implemented; Central Policy Arbitration implemented; `AUTO` / `PINNED` / `MANUAL` routing implemented; Runtime-certified Slow Start implemented; Pool Health semantics completed or explicitly `NOT_APPLICABLE`. | Hard Failure classification; Freshness integration; Stickiness; Minimum Improvement Threshold; State Change Cost Model. | Soft Degradation certification; Recovery Admission certification; Rollback certification; Blast Radius certification; Anti-Flap certification; Central Policy Arbitration; `AUTO` / `PINNED` / `MANUAL`; Runtime-certified Slow Start; Pool Health semantics. |
| Runtime Eligibility | Freshness windows exist; owner-issued freshness exists; authority, blast, rollback, anti-flap, verification, and learning gates are arbitrated; stale read reporting is preserved; bounded stale allowance is decided by action class. | Runtime Model; A2 freshness windows; A6 read-only execute-or-stop arbitration. | B17 stale-read reporting; B18 owner lease extension; C1 fail-open/fail-closed; C6 bounded stale allowance. |
| Authority Evolution | Operational and engineering authority are separated; packet approval is retired class-by-class; class approval and delegated policy approval require certified evidence; authority never expands silently. | Authority normalization; action-class ladder; packet approval classified as temporary governed fallback; A3-A5 evidence; A6 read-only eligibility; B13 blocking recommendation metric reliability. | B11 isolation; B12 staged promotion; B16 rollback authority; B21 user mode; C3/C4 authority constraints. |
| Rollback | Restore barrier works; rollback manifest exists; exact selected move identity is preserved; rollback/no-rollback evidence is certified; automatic rollback authority is certified only after reliable verification. | Restore barrier; rollback manifest; exact packet/lease identity path. | A3 class evidence; B15 containment/forward-fix classification; B16 automatic rollback authority; C5 compensation semantics. |
| Recovery Admission | Recovered channels require repeated real success/readiness evidence; post-admission observation exists; slow-start recovery is runtime-certified. | Recovery admission read model; limited recovery blast radius. | B8 certification; B9 observation windows; B10 slow-start progression. |
| Learning | Only real observed outcomes feed learning; outcome closure exists; representative evidence exists; metric reliability supports promotion recommendations. | Real-only learning rule; feedback owner; outcome closure path; B13 blocking recommendation metric reliability. | A3/A4 real outcomes; B5 attribution. |
| Production Readiness | Implementation, deploy, tests, truth, convergence, certification, outcomes, authority, and autonomy reach Production Maturity `100%`. | Engineering Maturity `100%`; safe deployment owner; truth/convergence; A1/A2 complete. | Remaining actionable backlog; production outcomes; certification; authority evolution; autonomy certification. |
| Production Autonomy | Runtime acts automatically only inside approved policy and certified action classes; operator supervises; production autonomy is certified. | Product and Runtime models define target; runtime automation remains disabled. | Class evidence; runtime eligibility; authority approval; rollback certification; bounded autonomy; production autonomy certification. |
| Knowledge System | Context Resolver, Research Framework, Canonical Policy Library, Canonical Reference, SYSTEM_MAP, and Document Lifecycle preserve verified knowledge without creating duplicate owners. | All listed knowledge owners exist and are canonical. | None current. |
| Observability | Operators and OMP can inspect liveness, degradation, recovery, rollback, stale reads, runtime eligibility, promotion readiness, and evidence quality without mutation. | Truth/convergence; admin read models; evidence inventory; service matrix. | B1/B4/B9/B13/B15/B17/C2 observability/read-model items. |
| Decision Explainability | Every approval request explains the decision in Russian before Approve / Reject; explanations are generated from existing evidence owners; safety gates show passed/failed/unknown/not applicable; alternatives and keep-current-state reasoning are visible; expected Production Value, Capability Progress, and remaining risk are shown; missing evidence stops safely instead of producing persuasive text. | OMP owns the capability; Russian-only operator explanation requirements; Russian-only Engineering Report requirements. | A3/A6/B1/B4/B13/B15/B17/C2 must provide enough evidence/read-model coverage for complete operator-facing explanations and real governed validation. |
| Implementation Discipline | OMP always selects the highest production-leverage admitted Mission, updates Current Program State, runs tests/truth/convergence, marks terminal state, recalculates, and continues or stops only at allowed stop conditions. | OMP Mission admission; Backlog registry; Priority Model; Root Cause Engine; normalized authority; document lifecycle; capability framework. | None current. |
| Engineering Knowledge Preservation | Certified reference knowledge is frozen; reports and ADRs remain evidence; only OMP-admitted Missions drive implementation. | Canonical Reference; Document Lifecycle; SYSTEM_MAP ownership; no-reaudit triggers. | None current. |

## 2.12.3.1. Master Integration Program

Status: `MASTER_INTEGRATION_PROGRAM_COMPLETE`

Purpose:

Turn existing completed V7 capabilities into one coherent production operating system through existing owners only.

This program does not create a new owner, new roadmap, new architecture, new planner, new governance, new execution path, new Runtime owner, new truth source, new policy, or duplicate backlog.

Source facts:

- `SYSTEM_INVENTORY_COMPLETE`;
- `SYSTEM_INTEGRATION_ANALYSIS_COMPLETE`;
- `docs/reference/SYSTEM_MAP.md` -> `Master Integration Atlas`;
- `docs/reference/V7_CANONICAL_REFERENCE.md` -> `MASTER_SYSTEM_INTEGRATION_AUDIT_PART_1` and `MASTER_SYSTEM_INTEGRATION_AUDIT_PART_2`.

Execution rule:

OMP must execute integration by selecting the highest unfinished existing backlog item that closes the next required integration in the Master Integration Atlas.

Every integration task must map to:

```text
Existing owner
  -> Existing capability
  -> Existing backlog item
  -> Integration action
  -> Expected production result
```

Need New Backlog Item:

`FALSE`

Reason:

All discovered integration work maps to existing backlog items. No mathematically unavoidable new backlog item was found.

Execution groups:

| Group | Purpose | Existing owner | Related backlog | Expected result |
| --- | --- | --- | --- | --- |
| Product Layer Integration | Make Business Objectives the primary operating language before technical artifacts. | Product Specification, Decision Explainability, Observability | `B1`, `B4`, `B13`, `B15`, `B17`, `C2` | Product Owner and operator see business reason, evidence, risk, value, and result first. |
| Policy Integration | Convert canonical policy rules into runtime-readable gate decisions. | Canonical Policy Library, OMP, Runtime Model | `A6`, `B19`, `B20`, `C1`, `C6` | Policies become executable eligibility inputs without new policy owners. |
| Capability Integration | Keep capability maturity, backlog, Current Program State, and OMP status synchronized. | OMP, Current Program State, Implementation Backlog | Existing mapped backlog | Capability progress updates after every real implementation/certification outcome. |
| Runtime Integration | Connect Runtime Model semantics to existing read models and guarded execution owners. | Runtime Model, action-class enablement, delegated policy preview | `A6`, `B17`, `B18`, `C1`, `C6` | Runtime can produce one `EXECUTE` or `STOP_SAFE` result from certified gates. |
| Runtime Explainability | Explain decisions in Russian before approval using existing evidence. | OMP, Decision Explainability, read models | `A3`, `A6`, `B1`, `B4`, `B13`, `B15`, `B17`, `C2` | Operator approves decisions, not opaque packets. |
| Operator Experience | Keep engineering details secondary, read-only, and expandable. | Product Specification, UI/read-model owners, OMP | `B1`, `B4`, `B13`, `B15`, `B17`, `C2` | Operator interface uses business language first. |
| Certification | Close rollback/no-rollback, blast-radius, recovery, anti-flap, and authority evidence. | OMP, Backlog, policy owners | `A3`, `A4`, `A5`, `B8`, `B10`, `B12`, `B13`, `B16` | Action classes become eligible for authority promotion. |
| Production Evidence | Feed only real observed outcomes into learning and promotion. | Feedback/learning owners, OMP | `A3`, `A4`, `B5`, `B13` | Promotion decisions are based on real outcomes, not synthetic evidence. |
| Autonomy Readiness | Move from governed packet fallback to class/policy authority. | OMP, Runtime Model, Authority Evolution | `A3`, `A4`, `A5`, `A6`, `B10`, `B12`, `B16`, `C4` | Runtime can eventually operate certified routine actions inside approved policy. |

Execution order:

| Order | Existing owner | Existing backlog | Integration work | Expected capability | Expected production impact | Expected maturity increase |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | Restore barrier, rollback manifest, governed execution, feedback/learning | `A3` | Certify class-level rollback/no-rollback evidence for governed candidate movement. | Rollback; Learning; Authority Evolution; Movement Protection | First real class evidence toward retiring packet approval. | High Production Maturity and Authority Evolution gain. |
| 2 | OMP promotion engine, feedback/learning, outcome leverage model | `A4` | Materialize representative outcome evidence for the first action class. | Learning; Authority Evolution; Production Readiness | Gives promotion decisions enough real evidence. | High autonomy and production evidence gain. |
| 3 | Action-class ladder, planner budgets, capacity/load gates | `A5` | Certify class-level blast-radius evidence beyond one-user guard. | Movement Protection; Authority Evolution; Runtime Eligibility | Allows safe scope reasoning for next authority step. | High safety and authority gain. |
| 4 | OMP, delegated policy preview, action-class runtime enablement, Runtime Model | `A6` | Implement action-class runtime eligibility arbitration using certified gates. | Runtime Eligibility; Production Autonomy | Converts separated gates into one execute-or-stop decision. | Very high runtime/autonomy gain. |
| 5 | Service matrix, quality compact, trust/outcome stores | `B5` | Complete observed degradation attribution using active and passive evidence. | Learning; Movement Protection; Observability | Improves quality of soft-degradation decisions. | Medium-high production gain. |
| 6 | Recovery admission, service/route/readiness models | `B8` | Certify recovery admission with repeated real success/readiness evidence. | Recovery Admission; Movement Protection | Prevents premature recovery movement. | High stability gain. |
| 7 | Blast-radius/action-class ladder | `B10` | Define runtime-certified recovery slow-start as V7 progression. | Recovery Admission; Production Autonomy | Enables bounded recovery re-entry. | High autonomy and stability gain. |
| 8 | Action-class ladder, OMP | `B12` | Implement next action-class stage only after certification evidence exists. | Authority Evolution; Production Autonomy | Advances class authority without silent expansion. | High autonomy gain. |
| 9 | Trust/confidence, freshness, rollback, eligibility | `B13` | Certify metric reliability for automated promotion recommendations. | Learning; Observability; Authority Evolution | Prevents bad promotion from weak metrics. | High safety gain. |
| 10 | Runtime Model, execution packet partial-failure policy | `B15` | Expose containment/forward-fix classification. | Rollback; Observability; Decision Explainability | Makes rollback alternatives visible and explainable. | Medium-high safety gain. |
| 11 | Autoswitch rollback-on-verify-fail, OMP authority gates | `B16` | Certify automatic rollback authority after reliable verification evidence. | Rollback; Production Autonomy; Authority Evolution | Enables safe rollback inside policy. | Very high runtime safety gain. |
| 12 | Runtime eligibility, truth/convergence, read-only inventory | `B17` | Preserve stale-read reporting while blocking mutation. | Runtime Eligibility; Observability; Decision Explainability | Improves operator trust without unsafe action. | Medium production gain. |
| 13 | Execution lease, runtime snapshot, intelligence snapshots | `B18` | Extend owner-issued version/lease pattern where available. | Runtime Eligibility; Freshness | Strengthens safe present-tense execution. | High safety gain. |
| 14 | Service signal thresholds, recovery admission, movement protection | `B19` | Centralize hysteresis and state-change-cost vocabulary. | Movement Protection; Runtime Eligibility | Prevents oscillation and noisy movement. | High stability gain. |
| 15 | OMP, planner, runtime eligibility | `B20` | Encode hard-failure override rule for anti-flap arbitration. | Movement Protection; Runtime Eligibility | Allows fast failure reaction without false oscillation. | High safety and recovery gain. |
| 16 | User registry, policy, planner, admin surface | `B21` | Implement explicit per-user `AUTO` / `PINNED` / `MANUAL` routing mode. | Movement Protection; Authority Evolution; Production Readiness | Makes user movement intent explicit. | Medium-high operational safety gain. |
| 17 | Runtime Model, OMP, planner gates | `C1` | Record fail-open/fail-closed behavior per action class. | Runtime Eligibility | Makes stop/continue semantics explicit. | Medium safety gain. |
| 18 | Trust/confidence model, shadow autonomy | `C2` | Use probabilistic suspicion only as advisory evidence. | Decision Explainability; Observability | Prevents weak signals from becoming unsafe actions. | Medium safety gain. |
| 19 | OMP, operator authority | `C3` | Define break-glass authority as audited exceptional operator policy. | Authority Evolution | Keeps emergency paths bounded and explicit. | Medium authority safety gain. |
| 20 | OMP, blast-radius gates | `C4` | Keep all-at-once promotion unavailable for current action classes. | Production Autonomy; Authority Evolution | Prevents unsafe expansion. | Medium safety gain. |
| 21 | Runtime Model, rollback policy | `C5` | Preserve rollback as operational compensation rather than transaction rollback. | Rollback | Clarifies safe recovery semantics. | Medium safety gain. |
| 22 | Freshness actionability, OMP stop rules | `C6` | Decide bounded stale allowance by action class. | Runtime Eligibility; Freshness | Avoids unsafe stale mutation while preserving useful reads. | Medium-high runtime gain. |
| 23 | Planner capacity/load, action-class ladder | `C7` | Map pool max-ejection/minimum-health semantics to V7 capacity and blast bounds. | Movement Protection; Production Readiness | Prevents over-evacuation and pool instability. | Medium-high stability gain. |

Dependency rule:

1. `A3` must precede `A4`, `A5`, `A6`, `B12`, and `B16`.
2. `A4` and `B13` must precede authority expansion recommendations.
3. `A6` must precede runtime autonomy readiness.
4. `B8` must precede `B10`.
5. `B16` must not be enabled before rollback/no-rollback evidence and verification reliability exist.
6. `C3` and `C4` are authority guardrails, not runtime enablement.

Parallel work:

The only safe parallel work is read-only observability/explainability work that does not mutate runtime, authority, policy, users, restore barrier, or evidence:

- `B1`, `B4`, `B15`, `B17`, `C2`;
- documentation-only clarifications `C1`, `C4`, `C5` when they do not change runtime behavior.

Runtime validation:

Runtime may consume only:

- Canonical Policies;
- Certified Action Classes;
- Delegated Autonomy Policy;
- Runtime Eligibility;
- Authority;
- Freshness;
- Rollback;
- Verification;
- Learning.

Runtime must never consume raw Product Owner text, raw Business Objectives, subjective operator wishes, packet approval as durable policy, or unverified report-only knowledge.

Product Owner experience target:

Product Owner interacts only with:

- Business Objectives;
- Business Status;
- Business Risk;
- Business Profile;
- Business Results;
- Business Exceptions.

Product Owner must never be required to understand packets, planner, lease, rollback internals, blast-radius internals, routing algorithms, runtime internals, or protocol engineering.

Operator experience target:

Operator UI must use business language first. Engineering details are secondary, read-only, expandable, and never the primary operating language.

OMP normalization:

After this program, normal operation must require only:

- `Status`;
- `Continue OMP`;
- `Approve authority expansion`;
- `Production Action`.

OMP must not request a new roadmap, new integration plan, or new semantic audit for already mapped work.

Master verification:

| Verification item | Result |
| --- | --- |
| Duplicate owners | `NONE_FOUND` |
| Duplicate permanent documents | `NONE_CREATED` |
| Duplicate policies | `NONE_FOUND` |
| Duplicate capabilities | `NONE_FOUND` |
| Duplicate truth sources | `NONE_FOUND` |
| Orphan knowledge | `NONE_FOUND` |
| Orphan capability | `NONE_FOUND` |
| Orphan backlog | `NONE_FOUND` |
| Disconnected integration | `NONE_UNMAPPED`; remaining gaps map to existing backlog/capabilities |

## 2.12.4. Movement Protection Target State

Purpose:

Define the final runtime behavior for Movement Protection after all required backlog items are complete.

This is the Definition of Done.

This is not an implementation plan.

This section does not create a new planner, Runtime owner, governance owner, execution owner, truth source, or document owner.

Movement Protection target state:

Users must not experience chaotic oscillation while V7 still reacts quickly to real production failures.

Runtime must prefer stability unless changing state has proven production value greater than transition cost.

Final Runtime decision pipeline:

```text
User
  -> Current Channel
  -> Candidate Discovery
  -> Hard Failure
  -> Soft Degradation
  -> Freshness
  -> Recovery Admission
  -> Blast Radius
  -> Rollback Readiness
  -> Anti-Flap
  -> Authority
  -> State Change Cost Evaluation
  -> Net Benefit Evaluation
  -> Worth Changing State?
  -> YES
  -> Execution
  -> Verification
  -> Outcome
  -> Learning
  -> Planner Improvement
```

Runtime pipeline stage contract:

| Stage | Purpose | Owner | Required evidence | Possible outputs | Interaction with previous stage | Interaction with next stage |
| --- | --- | --- | --- | --- | --- | --- |
| User | Identify the exact subject whose state may change. | User registry, planner/autoswitch owner, admin read models. | User identity, current assignment, org/group policy, manual/pinned state when implemented. | `USER_ELIGIBLE`, `USER_INELIGIBLE`, `USER_PINNED`, `USER_MANUAL_REVIEW`. | Starts the pipeline from a concrete production subject. | Passes subject constraints to Current Channel. |
| Current Channel | Preserve known current state before considering movement. | `tools/v7-users-autoswitch`, registry readers, Movement Protection Model. | Current egress/channel, recent movement history, sticky score, current-channel health. | `CURRENT_STABLE`, `CURRENT_SUSPECT`, `CURRENT_FAILED`, `CURRENT_UNKNOWN`. | Receives user constraints. | Defines baseline for Candidate Discovery and future net benefit comparison. |
| Candidate Discovery | Find valid target candidates without deciding to move yet. | Planner/autoswitch, service matrix, quality compact, route reality. | Candidate channels, service suitability, capacity/load, fallback availability, route reality. | `CANDIDATES_AVAILABLE`, `NO_SAFE_CANDIDATE`, `CANDIDATE_SET_UNKNOWN`. | Uses current channel as baseline. | Passes candidate set to failure/degradation gates. |
| Hard Failure | Detect complete failure requiring fast reaction. | `POLICY_001_HARD_FAILURE`, liveness/event evidence, service matrix, planner/autoswitch. | Liveness failure, explicit down/unavailable evidence, repeated failed checks, route/service hard-fail classification. | `HARD_FAILURE`, `NO_HARD_FAILURE`, `INSUFFICIENT_LIVENESS_EVIDENCE`. | Evaluates current and candidates discovered upstream. | If hard failure exists, Soft Degradation must not weaken the need to protect availability. |
| Soft Degradation | Detect meaningful degradation without treating noise as failure. | `POLICY_002_SOFT_DEGRADATION`, quality compact, service matrix, planner/autoswitch. | Active/passive degradation evidence, trend thresholds, service objective mapping, attribution evidence. | `SOFT_DEGRADATION`, `NO_DEGRADATION`, `NOISY_OR_ATTRIBUTION_UNKNOWN`. | Refines Hard Failure result; does not override proven hard failure. | Passes degradation severity to Freshness. |
| Freshness | Prove evidence is current enough for the action risk. | `POLICY_008_FRESHNESS`, Runtime Model, delegated policy preview, execution lease. | Owner-issued freshness fields, age, TTL/window, snapshot generation, lease/version where available. | `FRESH`, `STALE_READ_ONLY`, `UNKNOWN_FRESHNESS`, `STOP`. | Validates evidence from failure/degradation stages. | Only fresh or explicitly allowed evidence may continue to Recovery Admission. |
| Recovery Admission | Prevent premature use of recovered channels. | `POLICY_003_RECOVERY_ADMISSION`, recovery admission owner, service matrix, quality compact. | Repeated successful checks, readiness state, recovery cooldown, observation window, limited recovery blast radius. | `RECOVERY_ADMITTED`, `RECOVERY_HOLD`, `RECOVERY_UNKNOWN`, `RECOVERY_NOT_RELEVANT`. | Uses fresh evidence and candidate set. | Passes admitted candidate constraints to Blast Radius. |
| Blast Radius | Bound the size and scope of possible change. | `POLICY_006_BLAST_RADIUS`, action-class ladder, planner budgets, OMP. | Selected move count, action class, authority budget, capacity/load, org/cohort/service scope. | `WITHIN_BLAST_RADIUS`, `BLAST_RADIUS_EXCEEDED`, `SCOPE_REQUIRES_AUTHORITY`. | Uses candidate and recovery eligibility. | Defines maximum allowed movement before rollback and anti-flap checks. |
| Rollback Readiness | Confirm the system can compensate or has certified no-rollback semantics. | `POLICY_007_ROLLBACK`, restore barrier, rollback manifest, execution feedback. | Rollback target, restore barrier readiness, rollback manifest, selected-move identity, no-rollback certification where applicable. | `ROLLBACK_READY`, `NO_ROLLBACK_CERTIFIED`, `ROLLBACK_NOT_READY`, `STOP`. | Uses bounded action scope. | Only rollback-ready or certified no-rollback actions may proceed to Anti-Flap. |
| Anti-Flap | Block repeated oscillation and unsafe rapid reversals. | `POLICY_009_ANTI_FLAP`, movement protection owner, anti-flap read model. | Cooldown, freeze, pair reversal, target block, oscillation history, anti-flap window. | `ANTI_FLAP_PASS`, `COOLDOWN_ACTIVE`, `FREEZE_ACTIVE`, `REVERSAL_BLOCKED`, `TARGET_BLOCKED`. | Uses rollback-safe action candidate. | Passes stable candidate to Authority. |
| Authority | Verify the action is allowed without expanding authority silently. | `POLICY_004_AUTHORITY`, OMP, Runtime Model, action-class authority. | Operational/engineering authority class, action-class state, delegated policy, operator approval when required. | `AUTHORITY_PASS`, `OPERATIONAL_AUTHORITY_REQUIRED`, `ENGINEERING_AUTHORITY_REQUIRED`, `AUTHORITY_DENIED`. | Uses anti-flap-safe candidate and blast-radius scope. | Only authorized candidates may reach State Change Cost Evaluation. |
| State Change Cost Evaluation | Calculate the cost of changing from current state to target state. | Movement Protection Model, planner/autoswitch, OMP, Runtime eligibility owners. | Stickiness, threshold, recent movement penalty, cooldown, freeze, reversal risk, rollback risk, verification uncertainty, expected user impact, confidence floors. | `CHANGE_COST`, `KEEP_CURRENT_STATE`, `COST_UNKNOWN_STOP`. | Uses authority-cleared candidate and current-state baseline. | Supplies cost to Net Benefit Evaluation. |
| Net Benefit Evaluation | Compare expected benefit against transition cost. | Planner/autoswitch, Decision Model, Runtime Model, Movement Protection Model. | Candidate score delta, service benefit, failure severity, confidence, suitability, prediction confidence, user impact, rollback risk. | `NET_BENEFIT`, `NET_BENEFIT_NOT_PROVEN`, `KEEP_CURRENT_STATE`. | Consumes explicit change cost. | Only proven benefit can reach Worth Changing State. |
| Worth Changing State? | Make the final movement/no-movement decision. | Runtime Model executing Decision Model output through existing owners. | `NET_BENEFIT`, `CHANGE_COST`, authority, freshness, rollback, anti-flap, blast-radius results. | `EXECUTE`, `KEEP_CURRENT_STATE`, `STOP_SAFE`. | Compares net benefit to change cost. | If `EXECUTE`, passes exact bounded action to Execution. |
| Execution | Perform only the approved/certified movement through existing owners. | Existing execution/autoswitch owners. | Exact selected move, packet/lease identity when governed, rollback readiness, authority clearance. | `EXECUTED`, `NOOP_EXPLICIT_SAFE_STOP`, `EXECUTION_FAILED`. | Receives final execute decision. | Immediately triggers Verification. |
| Verification | Prove the action worked or failed. | Verification owner, service matrix, user/service checks, truth/convergence. | Post-action service/user/channel evidence, verification result, runtime truth. | `VERIFY_PASS`, `VERIFY_FAILED`, `ROLLBACK_REQUIRED`. | Observes execution outcome. | Feeds Outcome and rollback if required. |
| Outcome | Close the action with real observed result only. | Feedback/outcome owner, OMP, Current Program State. | Real verification, movement result, rollback/no-rollback classification, user impact. | `OUTCOME_CLOSED`, `OUTCOME_INCOMPLETE`, `REAL_WORLD_LIMIT`. | Consumes verification evidence. | Feeds Learning. |
| Learning | Convert outcome into future decision quality. | Feedback/learning owner, Canonical Reference where canonical meaning changes, OMP. | Real outcome, verification, rollback result, suitability correctness, trust/confidence deltas. | `LEARNING_UPDATED`, `NO_LEARNING_WITHOUT_REALITY`. | Uses closed outcome only. | Feeds Planner Improvement. |
| Planner Improvement | Improve future recommendations without rewriting architecture. | Planner/autoswitch, OMP, Implementation Backlog, knowledge owners. | Learned outcome, updated confidence/trust/suitability, canonical constraints. | `PLANNER_IMPROVED`, `BACKLOG_ITEM_UPDATED`, `NO_CHANGE`. | Uses learning from real outcomes. | Closes the loop back to Candidate Discovery for future decisions. |

State Change Cost canonical runtime principle:

Changing state has a cost.

Runtime must evaluate not only:

```text
Is another channel better?
```

Runtime must also evaluate:

```text
Is changing state worth the cost?
```

The State Change Cost must include at minimum:

- stickiness;
- minimum improvement threshold;
- recent movement penalty;
- cooldown;
- freeze;
- pair reversal;
- target block;
- rollback risk;
- verification uncertainty;
- expected user impact;
- planner confidence;
- prediction confidence;
- suitability confidence.

Canonical comparison:

```text
NET_BENEFIT = expected production value of the candidate movement.
CHANGE_COST = operational cost and risk of changing state.

Runtime may continue only if:

NET_BENEFIT > CHANGE_COST
```

If `NET_BENEFIT <= CHANGE_COST`, Runtime must output:

```text
KEEP_CURRENT_STATE
```

If `CHANGE_COST` cannot be calculated safely, Runtime must output:

```text
COST_UNKNOWN_STOP
```

Movement Protection completion behavior:

Movement Protection becomes `COMPLETE` only when Runtime satisfies all of the following:

- does not move because of tiny score differences;
- does not oscillate;
- does not undo its own actions repeatedly;
- does not chase temporary noise;
- reacts quickly to real failures;
- keeps users stable whenever stability is better than optimization;
- automatically prefers `stay` unless a move has proven production value;
- every movement has measurable expected benefit greater than transition cost.

World-practice comparison:

| Mature system family | Matching production principle | V7 target-state match | Backlog owner if incomplete |
| --- | --- | --- | --- |
| Cisco | Liveness evidence, protocol/object tracking, hold-down/dampening, bounded failover. | Matches through hard-failure classification, cooldown, movement protection, blast-radius and rollback gates. | Read-only mapping complete through `A5`, `B19`, and `C7`; future runtime consumption requires authority/certification. |
| Juniper | BFD/liveness, damping, timers, routing policy, explicit operational controls. | Matches through liveness/freshness gates, cooldown/dampening, authority separation, and state-change cost. | `A6`, `B19` for arbitration and vocabulary consolidation. |
| Cloudflare | Health checks, fallback pools, consecutive success/failure, pool health, traffic safety. | Matches through hard failure, recovery admission, freshness, blast radius, rollback, and pool-health target semantics. | Read-only mapping complete through `B8`, `B10`, and `C7`; future runtime consumption requires authority/certification. |
| Google SRE | Avoid cascading failure, verify changes, rollback before trust, canary, gradual recovery, learn from outcomes. | Matches through rollback, verification, learning, action-class promotion, and real-outcome-only certification. | `A3`, `A4`, `B13`, `B16`. |
| Kubernetes | Desired/current state separation, readiness, probes, rollout bounds, reconciliation, backoff. | Matches through Runtime executing prepared decisions, freshness/readiness, recovery admission, anti-flap, and stop-safe semantics. | `A6`, `B8`, `B9`, `B10`, `C1`, `C6`. |
| Envoy | Outlier detection, ejection, max ejection percent, min health, active health checking, circuit breaking. | Matches through degradation/anti-flap target state and V7-native capacity/blast bounds; proxy-specific max-ejection/min-health mapping is complete as read-only C7 semantics, not runtime ejection behavior. | Read-only mapping complete through `B3`, `B4`, `B5`, `B6`, and `C7`; future runtime consumption requires authority/certification. |

World-practice verdict:

The target state fully matches mature production engineering principles at the model level.

No new owner is required.

No new document is required.

No new backlog item is required.

Remaining real engineering gaps are already represented in the Implementation Backlog:

| Remaining gap | Existing backlog item |
| --- | --- |
| Rollback/no-rollback production certification | `A3`, `B16` |
| Soft Degradation certification and mapping | `B3`, `B4`, `B5`, `B6`, `B7` |
| Recovery Admission certification | `B8`, `B9`, `B10` |
| Blast Radius certification and scope | `A5`, `B14` |
| Anti-Flap certification and arbitration | `B19`, `B20` |
| Central Policy Arbitration | `A6` |
| Per-user `AUTO` / `PINNED` / `MANUAL` routing mode | `B21` |
| Runtime-certified Slow Start Recovery | `B10` |
| Pool Max-Ejection / Minimum-Health semantics | `C7` |

Movement Protection Definition of Done:

Movement Protection is `COMPLETE` only when all are true:

1. all required Movement Protection backlog items are `DONE`;
2. all runtime behaviors listed in this target state are implemented through existing owners;
3. all relevant production certifications pass;
4. real production evidence confirms stable behavior;
5. Production Maturity reflects completion;
6. Canonical Reference records the completed capability;
7. OMP marks Movement Protection `COMPLETE`, then `LOCKED`.

Movement Protection remains `IN_PROGRESS`.

Current estimated Movement Protection completion:

```text
33.1%
```

Backlog-to-capability coverage:

| Backlog item | Capability ownership |
| --- | --- |
| `A1` | Movement Protection; Runtime Eligibility; Knowledge System |
| `A2` | Runtime Eligibility; Movement Protection; Recovery Admission |
| `A3` | Rollback; Movement Protection; Learning; Authority Evolution |
| `A4` | Learning; Authority Evolution; Production Readiness; Production Autonomy |
| `A5` | Movement Protection; Authority Evolution; Runtime Eligibility |
| `A6` | Runtime Eligibility; Authority Evolution; Movement Protection; Production Autonomy |
| `B1` | Observability; Knowledge System; Movement Protection |
| `B2` | Runtime Eligibility; Movement Protection |
| `B3` | Movement Protection; Observability |
| `B4` | Movement Protection; Observability |
| `B5` | Movement Protection; Learning; Observability |
| `B6` | Movement Protection; Runtime Eligibility |
| `B7` | Runtime Eligibility; Movement Protection |
| `B8` | Recovery Admission; Movement Protection |
| `B9` | Recovery Admission; Observability |
| `B10` | Recovery Admission; Movement Protection; Production Autonomy |
| `B11` | Authority Evolution; Runtime Eligibility; Production Readiness |
| `B12` | Authority Evolution; Production Autonomy; Implementation Discipline |
| `B13` | Authority Evolution; Learning; Observability |
| `B14` | Authority Evolution; Movement Protection; Production Readiness |
| `B15` | Rollback; Observability |
| `B16` | Rollback; Authority Evolution; Production Autonomy |
| `B17` | Runtime Eligibility; Observability |
| `B18` | Runtime Eligibility |
| `B19` | Movement Protection; Runtime Eligibility |
| `B20` | Movement Protection; Runtime Eligibility |
| `B21` | Movement Protection; Authority Evolution; Production Readiness |
| `C1` | Runtime Eligibility; Authority Evolution |
| `C2` | Knowledge System; Observability |
| `C3` | Authority Evolution |
| `C4` | Authority Evolution; Production Autonomy |
| `C5` | Rollback |
| `C6` | Runtime Eligibility |
| `C7` | Movement Protection; Production Readiness |
| `D1` | Production Readiness; Movement Protection, only if substrate scope changes |
| `D2` | Recovery Admission, only if provider lifecycle becomes product scope |
| `D3` | Recovery Admission, only if DNS failover becomes product scope |
| `D4` | Authority Evolution, only if distributed operator control becomes product scope |
| `D5` | Movement Protection, only if split-traffic routing becomes product scope |
| `D6` | Movement Protection, only if routing-protocol ownership becomes product scope |

Engineering Report Lifecycle:

Engineering Reports are not project documents.

Engineering Reports are execution history.

Therefore the rule:

```text
Do NOT create a new document
```

does not apply to Engineering Reports.

Engineering Reports must be created automatically after every meaningful engineering action.

Engineering Reports must be written only in Russian.

Project documents include only:

- `REFERENCE`;
- `PROGRAMS`;
- `POLICIES`;
- `ADR`;
- `BACKLOG`;
- `PRODUCT`;
- `SYSTEM MAP`;
- `CANONICAL REFERENCE`;
- Runtime Model;
- Decision Model.

Engineering Reports belong only to:

```text
docs/reports/engineering/
```

They are historical evidence.

They never become:

- backlog;
- roadmap;
- canonical owner;
- reference document.

Report types:

| Type | Trigger | Purpose | Length |
| --- | --- | --- | --- |
| Type 1: Engineering Report | Automatically after implementation, audit, semantic audit, test, verification, deploy, truth, convergence, certification, runtime investigation, root cause analysis, capability progress change, or production action. | Historical engineering evidence. | Short. |
| Type 2: Milestone Report | Automatically only when a capability becomes `COMPLETE`, a capability becomes `LOCKED`, a major certification completes, a Production Maturity milestone is reached, or an autonomy tier is promoted. | Summarize an engineering milestone. | Detailed. |

After every meaningful engineering action, OMP must create and save an engineering report as historical evidence.

Applicable actions:

- implementation;
- semantic audit;
- testing;
- verification;
- certification;
- deploy;
- truth;
- convergence;
- runtime investigation;
- root cause analysis;
- production action;
- capability progress update;
- OMP behavior decision;
- OMP Candidate Sequencing decision;
- OMP Mission Admission decision;
- OMP hold / block / reject / not-applicable decision.

Report location:

```text
docs/reports/engineering/
```

Filename format:

```text
YYYY-MM-DD_HHMMSS_<topic>.md
```

Engineering Report must include:

- Summary;
- Action Performed;
- Objective Observations;
- Engineering Conclusions;
- Business Objective affected;
- Capability affected;
- Backlog affected;
- Canonical knowledge affected;
- Production impact;
- User impact;
- Почему система приняла именно такое решение;
- Почему решение считается безопасным;
- Почему решение считается полезным;
- Почему система НЕ выбрала альтернативные варианты;
- Decision Trace ID, or `NOT_APPLICABLE_WITH_REASON`;
- Decision Trace Summary, when the action includes an OMP decision;
- Selected Candidate, held / rejected / not-applicable alternatives, and decisive criteria when the action includes an OMP decision;
- Decision Fingerprint, or `NOT_APPLICABLE_WITH_REASON`;
- Replay Status, when the action includes an OMP decision;
- Decision Drift status and Difference Explanation when replay differs from a prior OMP decision;
- Automation Gap Closure status when the action includes a STOP or Intent Gap;
- STOP Classification and Human Intervention Detection when the action includes a STOP;
- Intent Gap Detection status after any completed Engineering Chain, Mission, Capability, Behavior, Execution, Verification, Certification, State Transition, Implementation, or OMP meaningful step;
- Intent Gap Classification when Engineering Intent is not achieved;
- Intent Responsibility Resolution status after any `INTENT_GAP_DETECTED`;
- responsibility_failure_class;
- last_responsible_link;
- responsible_owner;
- failed_contract_field;
- expected_owner_behavior;
- observed_owner_behavior;
- missing_evidence;
- smallest_existing_next_action;
- BDP input specialization;
- automation_feasibility_result;
- STOP-derived or Intent-Gap-derived BDP input route, or `NOT_APPLICABLE_WITH_REASON`;
- Engineering Intent Closure status when the action completes a STOP-derived or Intent-Gap-derived Candidate;
- Original STOP / Intent Gap resolved, Expected State reached, Current State matches Expected State, and Legal Terminal Consumer verified when the action completes a STOP-derived or Intent-Gap-derived Candidate;
- Impact on Runtime;
- Impact on OMP;
- Impact on Backlog;
- Impact on Capability;
- Impact on Production;
- Capability Progress;
- Backlog Progress;
- Production Maturity;
- Production Maturity Decision when maturity-affecting;
- Current Program State impact;
- Engineering Intelligence learning impact;
- Dashboard visibility impact;
- Behavior Enforcement;
- State Transition Verification;
- Necessity Framework Consumption status when the action creates, keeps, locks, canonicalizes, merges, removes, deprecates, or historicalizes an element;
- Approved Future Dependency Protection status before any Necessity, Merge, Remove, Value Conservation, Collapse, Owner Elimination, Function Elimination, Module Elimination, Document Elimination, Capability Elimination, or architectural minimization action;
- protected_future_dependency_object;
- approved_future_plan;
- future_dependency_owner;
- future_dependency_type;
- future_dependency_state;
- future_dependency_terminal_condition;
- Engineering Work In Progress Protection status before any Necessity, Merge, Remove, Value Conservation, Collapse, Owner Elimination, Function Elimination, Module Elimination, Document Elimination, Capability Elimination, or architectural minimization action;
- protected_engineering_object;
- unfinished_engineering_lifecycle;
- engineering_lifecycle_owner;
- engineering_lifecycle_state;
- engineering_wip_terminal_condition;
- Capability Maturity Protection status before any Necessity, Merge, Remove, Value Conservation, Collapse, Owner Elimination, Function Elimination, or architectural minimization action;
- protected_capability;
- protected_element;
- capability_maturity_status;
- capability_mapping_status;
- capability_completion_required_before_minimization;
- existence_justification;
- semantic_necessity;
- consumer_value;
- system_effect;
- state_transition_contribution;
- production_value;
- creation_test;
- removal_test;
- merge_test;
- chain_test;
- necessity_verdict;
- necessity_certification_state;
- Product Evolution Review;
- Product Evolution Field Validation;
- Product Evolution OMP Behavior;
- Work Placement;
- Latency Impact;
- Canonical Knowledge;
- Evidence: tests, truth, convergence, deploy, production outcome where applicable;
- Next Step;
- Re-audit Rule.

Latency Impact must include:

| Field | Required value |
| --- | --- |
| Observation Latency | `measured`, `estimated`, `unknown`, or `not applicable`. |
| Decision Latency | `measured`, `estimated`, `unknown`, or `not applicable`. |
| Execution Latency | `measured`, `estimated`, `unknown`, or `not applicable`. |
| Verification Latency | `measured`, `estimated`, `unknown`, or `not applicable`. |
| Feedback / Learning Latency | `measured`, `estimated`, `unknown`, or `not applicable`. |
| Reaction Latency | `measured`, `estimated`, `unknown`, or `not applicable`. |
| Runtime path impact | `increased`, `decreased`, `unchanged`, or `not applicable`. |
| Precompute opportunity | `YES` or `NO`. |
| Live gate impact | `YES` or `NO`. |
| Wait-state impact | `YES_WITH_OWNER`, `NO`, or `UNKNOWN_WITH_MEASUREMENT_PLAN`. |
| Measurement plan | Existing measurement field, existing owner extension, or `NOT_APPLICABLE_WITH_REASON`. |
| Notes | Short explanation. |

`UNKNOWN` is acceptable in RT Phase 1.
Omitting Latency Impact is not acceptable after RT Phase 1.

Engineering Reports must use the canonical Runtime Latency Engineering Review Checklist from `docs/reference/V7_RUNTIME_MODEL.md`.

Work Placement must include:

| Field | Required value |
| --- | --- |
| Computation | Meaningful computation touched by the action, or `NOT_APPLICABLE_WITH_REASON`. |
| Canonical Plane | Observation, World Model, Planning, Execution, Verification, Feedback/Learning, OMP/Certification, or `NOT_APPLICABLE_WITH_REASON`. |
| Canonical Owner | Existing owner responsible for the computation. |
| Runtime Placement | `YES_ONLY_IF_LIVE_SAFETY_REQUIRED`, `NO`, or `NOT_APPLICABLE`. |
| Move Earlier? | `YES`, `NO_WITH_SAFETY_REASON`, or `ALREADY_PREPARED`. |
| Reaction Latency Impact | Observation, Decision, Execution, Verification, Feedback/Learning, Reaction, `NONE`, or `UNKNOWN_WITH_MEASUREMENT_PLAN`. |

Product Evolution Review must include:

| Field | Required value |
| --- | --- |
| Certification Review | Mandatory, supporting, optional, or not applicable evidence with owner. |
| Work Placement Review | `PASS`, `FAIL`, or `NOT_APPLICABLE_WITH_REASON`. |
| Runtime Latency Review | Affected component or `NONE`. |
| Runtime Cost Review | CPU, memory, IO, blocking, lock contention, execution cost, rollback cost, runtime cost, or `NONE`. |
| Decision Freshness Review | Relevant lifecycle states and owner, or `NOT_APPLICABLE_WITH_REASON`. |
| Safety Review | Live gates and `STOP_SAFE` triggers, or `NOT_APPLICABLE_WITH_REASON`. |

Product Evolution Field Validation must include:

| Question | Required answer |
| --- | --- |
| What Product Observation appeared? | Product observation, `UNKNOWN`, or `NOT_APPLICABLE`. |
| What Product Value was improved or protected? | Product Value, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Which Current Active Target did this support? | Target name, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Which Production Maturity Gap did this address? | Production Maturity Gap, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Which Capability Goal advanced? | Capability Goal, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Which Capability Gap was reduced? | Capability Gap, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Which Evidence Gap was reduced? | Evidence Gap, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Did the Product Evolution Framework correctly predict the work, evidence, risk, and expected outcome? | `YES`, `NO`, `PARTIAL`, `UNKNOWN`, or `NOT_APPLICABLE`, with short reason. |
| What should be improved inside the framework? | Improvement, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Did any concept attempt to become roadmap, planner, authority, Runtime logic, or duplicate owner? | `YES_WITH_EXPLANATION`, `NO`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| OMP Decision | Exactly one of `ACCEPT`, `REJECT`, `DEFER`, `BLOCK`, or `NOT_APPLICABLE`, with short justification. |
| Behavior Changed | How OMP behavior changed because it consumed the Framework output, or `NOT_APPLICABLE_WITH_REASON`. |
| New Output Produced | Execution Decision, Evidence Collection Decision, Blocked Result, Deferred Result, Rejected Result, Engineering Report Requirement, or `NOT_APPLICABLE_WITH_REASON`. |
| Production Effect | `DIRECT`, `INDIRECT`, `SUPPORTS`, `NO_CHANGE_WITH_REASON`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Learning Trigger | Learning update, framework improvement signal, `NONE_WITH_REASON`, `UNKNOWN`, or `NOT_APPLICABLE`. |

Rules:

- if the answer is unknown, write `UNKNOWN`;
- if not applicable, write `NOT_APPLICABLE`;
- do not invent Product Value, Target, Gap, or Evidence;
- Product Evolution OMP Behavior is part of this same block and must not duplicate the Field Validation section;
- OMP Decision must be exactly one of `ACCEPT`, `REJECT`, `DEFER`, `BLOCK`, or `NOT_APPLICABLE`;
- New Output Produced must identify the downstream consumer for execution, evidence, blocked/deferred/rejected result, Engineering Report, or Learning;
- Field Validation is observational and advisory only;
- Field Validation cannot update Production Maturity, approve authority, approve Runtime apply, create campaigns, change OMP sequence, change Current Program State, become roadmap, become planner, or become owner.

Production Maturity Decision must include when the work is maturity-affecting:

| Field | Required value |
| --- | --- |
| Capability Advancement | Existing owner result, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Certification Result | Existing certification owner result, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Evidence Economy | Certification-grade, duplicate, stale, invalid, synthetic, insufficient, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Production Maturity Decision | Exactly one of `ACCEPT`, `PARTIAL_ACCEPT`, `BLOCK`, `NO_CHANGE`, `INVALID_EVIDENCE`, or `NOT_APPLICABLE`. |
| Current Maturity State | Current Production Maturity owner value, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Current Target Status | Existing CPS / OMP target status, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Current Blockers | Blocker list, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| CPS Impact | Volatile state updated, no volatile state change, `UNKNOWN`, or `NOT_APPLICABLE`. |

Current Program State impact must record whether Production Maturity produced a state change, blocked result, no-change result, target-status change, blocker change, readiness-context change, or no volatile change.

Engineering Intelligence learning impact must include when recommendation, prediction, confidence, evidence, or learning changed:

| Field | Required value |
| --- | --- |
| Learning consumed | Learning record, Engineering Report, outcome, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Prediction vs Reality | Match, mismatch, partial, drift, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Confidence update | Increased, decreased, unchanged, blocked, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Recommendation adjustment | Improved, degraded, drifted, retired, unchanged, blocked-by-evidence, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Evidence quality feedback | Certification-grade, duplicate, stale, invalid, insufficient, synthetic-forbidden, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Framework improvement signal | Improvement, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |

Dashboard visibility impact must include when current state, blockers, confidence, target, recommendation, or learning visibility changed:

| Field | Required value |
| --- | --- |
| Operator Visibility | Changed, unchanged, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Engineering Visibility | Changed, unchanged, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Blocker Visibility | Changed, unchanged, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Confidence Visibility | Changed, unchanged, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Target Visibility | Changed, unchanged, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Learning Visibility | Changed, unchanged, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Dashboard authority check | `READ_ONLY_CONFIRMED`, `VIOLATION_WITH_EXPLANATION`, `UNKNOWN`, or `NOT_APPLICABLE`. |

Behavior Enforcement must include:

| Field | Required value |
| --- | --- |
| Behavior Chain Verified | `YES`, `NO`, `PARTIAL`, `UNKNOWN`, or `NOT_APPLICABLE`, with reason. |
| Behavior Chain Status | `COMPLETE`, `PARTIAL`, `BLOCKED`, `BROKEN`, or `UNKNOWN`. |
| Producer | Existing producer owner/component, or `NOT_APPLICABLE`. |
| Output Produced | Produced output, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Output Available | `YES`, `NO`, `PARTIAL`, `UNKNOWN`, or `NOT_APPLICABLE`, with source. |
| Consumer | Existing consumer owner/component, `MISSING_WITH_REASON`, or `NOT_APPLICABLE`. |
| Consumer Consumed Output | `YES`, `NO`, `PARTIAL`, `UNKNOWN`, or `NOT_APPLICABLE`, with consuming owner and evidence. |
| Consumption Verified | `PASS`, `FAIL`, `PARTIAL`, `BLOCKED`, `UNKNOWN`, or `NOT_APPLICABLE`, with verification method. |
| Behavior Changed | `YES`, `NO`, `PARTIAL`, `UNKNOWN`, or `NOT_APPLICABLE`, with changed behavior. |
| Expected Behavior Change | Required consumer behavior, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Expected Output | Required output, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Output Consumed | `YES`, `NO`, `PARTIAL`, `UNKNOWN`, or `NOT_APPLICABLE`, with consuming owner. |
| Next Output Produced | Produced next output, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Terminal Consumer | Runtime Ready For Next Cycle, Capability Certified, Production Maturity Updated, OMP Next Step Produced, Capability Locked, Capability Retired, Terminal `STOP_SAFE`, `ENGINEERING_AUTHORITY`, `OPERATIONAL_AUTHORITY`, `REAL_WORLD_LIMIT`, or `NOT_APPLICABLE_WITH_REASON`. |
| Terminal Consumer Verified | `PASS`, `FAIL`, `PARTIAL`, `BLOCKED`, `UNKNOWN`, or `NOT_APPLICABLE`, with evidence. |
| Verification Method | Report field, owner state, certification result, CPS field, dashboard source, test, truth/convergence, or `NOT_APPLICABLE_WITH_REASON`. |
| Verification Result | `PASS`, `FAIL`, `PARTIAL`, `BLOCKED`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Broken Contracts | Contract id/list, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Missing Consumer | Consumer, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Missing Output | Output, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Orphan Output | Output without executable consumer, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Forbidden Completion Claim | Read model, dashboard, Engineering Report, diagnostic output, recommendation, placeholder, future work, TODO, comment, preview, simulation, advisory surface, read-only status, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Failure Condition | `OUTPUT_NOT_CONSUMED`, `CONSUMPTION_NOT_VERIFIED`, `NO_BEHAVIOR_CHANGE`, `NEXT_OUTPUT_NOT_PRODUCED`, `ORPHAN_OUTPUT`, `ORPHAN_CONSUMER`, missing output, missing evidence, missing legal terminal consumer, contradiction, forbidden authority/runtime/automation path, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Recovery Path | Existing owner re-run, Engineering Report correction, canonical update, CPS update, OMP `DEFER`, OMP `BLOCK`, owner mapping, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |

State Transition Verification must include:

| Field | Required value |
| --- | --- |
| Behavior Verified | `YES`, `NO`, `PARTIAL`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| State Produced | `YES`, `NO`, `PARTIAL`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| State Consumed | `YES`, `NO`, `PARTIAL`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| State Consumption Verified | `PASS`, `FAIL`, `PARTIAL`, `BLOCKED`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| New State Produced | `YES`, `NO`, `PARTIAL`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| State Changed | `YES`, `NO`, `PARTIAL`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Transition Result | `STATE_TRANSITION_COMPLETED`, `STATE_TRANSITION_EXPLAINED`, or `NOT_APPLICABLE_WITH_REASON`. |
| Transition Blocker | Exact blocker, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Current State | Owner-backed current state, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Required State | Required target state, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Missing Preconditions | Preconditions that must become `TRUE`, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Responsible Owner | Existing owner, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Required Capability | Existing capability, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Required Evidence | Required evidence, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Required Certification | Required certification, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Reality Limit | Reality limit, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Authority Limit | Authority boundary, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Engineering Limit | Engineering/capability limit, `NONE`, `UNKNOWN`, or `NOT_APPLICABLE`. |
| Next OMP Action | Smallest existing next action, smallest blocked next action with prerequisite, or `NOT_APPLICABLE_WITH_REASON`. |
| Expected State Transition | Expected next state if next action succeeds, `UNKNOWN`, or `NOT_APPLICABLE`. |

Architectural Methodology Review must include:

| Field | Required value |
| --- | --- |
| Methodology status | `COMPLETE`, `REUSED`, or `BLOCKED_WITH_REASON`. |
| Existing laws used | Product intent, owner reuse, Work Placement, Decision Lifecycle, Certification Truth, Runtime Time, Product Scale, Safety, Authority, and OMP/backlog path, or `NOT_APPLICABLE_WITH_REASON`. |
| Missing law | `NONE` unless a complete Architecture Closed by Default audit proves otherwise. |
| New owner/backlog/architecture | `FALSE` unless explicitly proven. |

Pre-Phase-2 Readiness Review must include:

| Field | Required value |
| --- | --- |
| DL1-DL7 impact | Affected foundation or `NONE`. |
| Phase 2 readiness impact | `TOWARD`, `AWAY`, or `NEUTRAL_WITH_REASON`. |
| Entry contract impact | Which Phase 2 entry criterion changed, or `NONE`. |
| Runtime automation impact | `NO` unless explicit authority and certification exist. |

Milestone Report must include:

- Capability;
- Reason for milestone;
- What became `COMPLETE`;
- What became `LOCKED`;
- Canonical knowledge created;
- Production impact;
- Autonomy impact;
- Lessons learned;
- Remaining capabilities.

Reports are historical evidence only.

Reports must never become a roadmap, planner, governance layer, execution owner, truth source, or second implementation queue.

Canonical update workflow:

If durable knowledge is discovered during any meaningful engineering action, Codex must update the appropriate existing canonical owner before the work is considered complete:

- `docs/reference/V7_CANONICAL_REFERENCE.md` for system truth;
- `docs/reference/SYSTEM_MAP.md` for ownership/topology changes;
- `docs/decisions/` ADR only when project meaning changes;
- `docs/reference/V7_RUNTIME_MODEL.md` only when Runtime semantics change by explicit approved design;
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` when OMP operating behavior changes.

Durable knowledge must never remain only inside reports.

Knowledge Plane Operationalization:

The Knowledge Plane is operational, but it is not a new owner, roadmap, truth source, audit registry, planner, governance layer, execution path, or runtime subsystem.

It is the daily consumption contract across existing owners:

```text
Product Specification
  -> Audit Knowledge State
  -> Canonical Reference
  -> Current Program State
  -> OMP
  -> Implementation Backlog
  -> Runtime Model
  -> Implementation
```

Production rule:

| Concept | Meaning | Owner |
| --- | --- | --- |
| Knowledge State | Current durable knowledge state for future engineering and Codex work. | Canonical Reference + SYSTEM_MAP + OMP knowledge workflow. |
| Engineering Reports | Historical evidence only. | `docs/reports/engineering/`. |
| Current Program State | Current runtime/program situation. | `docs/programs/V7_CURRENT_PROGRAM_STATE.md`. |
| Canonical Reference | Durable project truth. | `docs/reference/V7_CANONICAL_REFERENCE.md`. |
| OMP | Execution program. | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`. |
| Implementation Backlog | Post-admission implementation registry for OMP Missions. | `docs/programs/V7_IMPLEMENTATION_BACKLOG.md`. |

Mandatory engineering workflow:

```text
Read Product Specification
  -> Read Audit Knowledge State
  -> Read Canonical Reference
  -> Read Current Program State
  -> Read OMP
  -> Read current OMP Mission / Implementation Backlog registry
  -> Read accepted BDP Implementation Candidate when present
  -> Determine:
       Already known?
       Still valid?
       Re-open required?
       Implementation required?
  -> Continue only through existing owner / OMP Mission path
```

Mandatory audit workflow:

```text
Read Audit Knowledge State
  -> Check Confidence
  -> Check Freshness
  -> Check Re-open Triggers
  -> Reuse Existing Knowledge
  -> Audit Only Unknown Knowledge
  -> Update Canonical Owners when durable knowledge changes
  -> Update Audit Knowledge State
  -> Create Historical Engineering Report
```

Mandatory implementation workflow:

```text
Read Knowledge Plane
  -> Implement existing backlog item
  -> Verify
  -> Certify when required
  -> Engineering Report
  -> Canonical Update if durable knowledge changed
  -> Knowledge State Update
  -> Current Program State Update
  -> OMP Update
```

Mandatory certification workflow:

```text
Certification
  -> Update Knowledge State
  -> Update Capability State
  -> Update Production State
  -> Update Current Program State
  -> Create Historical Evidence
```

Knowledge promotion workflow:

```text
Temporary Investigation
  -> Engineering Report
  -> Verified
  -> Canonical Owner
  -> Audit Knowledge State
  -> OMP Consumption
  -> Future Codex / Future AI Agent Consumption
```

Knowledge invalidation workflow:

| Trigger | Existing owner responsible for invalidation decision |
| --- | --- |
| Runtime Model changes | Runtime Model owner + OMP + SYSTEM_MAP. |
| Product changes | Product Specification owner + Canonical Reference. |
| Policy changes | Canonical Policy Library + OMP. |
| Production evidence contradicts current knowledge | Current Program State + Production Maturity Model + OMP Root Cause Engine. |
| Implementation changes material behavior | Implementation Backlog owner + OMP + relevant code owner. |
| Operator decision changes approved boundary | OMP authority model + Current Program State. |
| Architecture changes | Architecture Closed by Default gate + Canonical Reference + SYSTEM_MAP. |
| Product Scale Model changes | Product Specification + Production Scale First gate. |

Knowledge consumption rule:

Future Codex and future AI agents must never start work by reading historical reports as current truth. Reports may be read only as supporting evidence after the Knowledge Plane identifies that evidence is required.

Future work must first consume:

```text
Product Specification
  -> Audit Knowledge State
  -> Canonical Reference
  -> Current Program State
  -> OMP
  -> Implementation Backlog
```

Then consume `Runtime Model`, implementation files, reports, ADRs, policies, or tools only when the resolved task requires them.

Knowledge Plane validation gate:

Every meaningful OMP action must answer:

1. Is this already known?
2. Which existing owner holds it?
3. Is the knowledge still fresh enough?
4. What confidence/certification state applies?
5. Does any re-open trigger apply?
6. Does durable knowledge need promotion from report to owner?
7. Is implementation required, and if yes, which existing backlog item owns it?
8. Need New Owner? Default `FALSE`.
9. Need New Backlog Item? Default `FALSE`.

If the answer cannot be mapped after complete audit, OMP may report a gap. Architecture extension remains the last resort.

Engineering Context Resolver integration:

Before any OMP engineering action, OMP must use `docs/reference/V7_CONTEXT_RESOLVER.md` as the Engineering Context Resolver.

Required ECR outputs:

| Field | Required value |
| --- | --- |
| `task_class` | One of Architecture, Knowledge, Product, Policy, Implementation, Runtime, Production, Certification, Audit, Scale, Bug, Investigation, Operator Request, Research. |
| `mandatory_context` | Minimum documents/owners required for the class. |
| `optional_context` | Only loaded if mandatory context cannot answer safely. |
| `forbidden_by_default_context` | Reports, packet state, runtime state, implementation files, or research that must not be loaded unless the class requires it. |
| `authoritative_owner` | Existing owner from SYSTEM_MAP / Canonical Reference. |
| `already_verified` | `YES`, `NO`, or `UNKNOWN`. |
| `still_current` | `CURRENT`, `STALE_RECHECK_REQUIRED`, `HISTORY_ONLY`, or `UNKNOWN`. |
| `reopen_required` | `TRUE` or `FALSE`, with trigger if true. |
| `implementation_required` | Existing backlog item or `NO`. |
| `certification_required` | Existing capability/policy/certification path or `NO`. |
| `runtime_investigation_required` | Existing runtime owner or `NO`. |
| `need_new_owner` | Default `FALSE`. |
| `need_new_backlog_item` | Default `FALSE`. |

For `Continue OMP`, ECR must resolve the default working set to:

```text
Product Specification
  -> Audit Knowledge State
  -> Canonical Reference
  -> Current Program State
  -> OMP
  -> Current Backlog Item
```

Nothing else is loaded unless OMP maps the current item to a specific owner or a re-open trigger fires.

### 2.12.3.2 Historical Implementation And Certification Trace

Classification: `HISTORICAL_MILESTONE`.
Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

Historical implementation optimizer result:

| Field | Current Value |
| --- | --- |
| Highest implementation leverage task | `A5_CERTIFY_CLASS_LEVEL_BLAST_RADIUS_EVIDENCE_BEYOND_ONE_USER_GUARD` |
| Implementation class | `IMPLEMENT_VERIFICATION` |
| Exact owner | Action-class ladder, planner budgets, capacity/load gates, blast-radius evidence owner |
| Exact module | Canonical Policy Library Stage 4 implementation backlog and existing action-class/blast-radius owners |
| Exact files | `tools/v7-users-autoswitch`, `admin_core/autonomy_trust_acceleration.py`, `admin_core/operator_execution_pipeline.py` |
| Implementation status | `A4_DONE_A5_READY` |
| Backlog source | `docs/programs/V7_IMPLEMENTATION_BACKLOG.md` item `A5` |
| Priority model | `docs/reference/V7_IMPLEMENTATION_PRIORITY_MODEL.md` |
| Truth/convergence | Latest run after A4 closure read-model deploy: truth `PASS`; convergence `ALIGNED`. |
| New highest implementation leverage task | `A5_CERTIFY_CLASS_LEVEL_BLAST_RADIUS_EVIDENCE_BEYOND_ONE_USER_GUARD` |
| Stop boundary | `NONE`: continue A5 certification analysis through existing owners; do not expand authority or runtime automation. |

Current A4 bounded authority envelope:

| Field | Current Value |
| --- | --- |
| Authority status | `ACTIVE` |
| Approved scope | Current A4 bounded evidence collection only |
| Max successful evidence outcomes requested | `63` remaining at start of latest bounded run |
| One-user limit | `YES` |
| Runtime automation | `NO` |
| Authority expansion | `NO` |
| Packet-by-packet approval | `NO` inside this bounded envelope |
| Stop rule | Stop on first failed gate, failed verification, rollback need, duplicate, non-missing candidate, scope expansion, or runtime automation attempt |
| Current stop | `REAL_WORLD_LIMIT_A4_NO_GAP_REDUCING_CANDIDATE`; evidence-gap guard stopped before lease, restore-barrier write, or apply |

Latest bounded A4 collection continuation:

| Field | Current Value |
| --- | --- |
| Engineering report | `docs/reports/engineering/2026-06-27_170227_a4_bounded_collection_outcome.md` |
| Final verdict | `A4_BOUNDED_EVIDENCE_COLLECTION_STOPPED` |
| Stop reason | `duplicate_transaction_candidate` |
| Successful verified outcomes | `1` |
| Successful move | `10.7.0.25 vless -> awg3` |
| Verification | `PASS` |
| Rollback | `NOT_REQUIRED` |
| A4 evidence | `94 / 156 = 60.3%`; missing `62 / 156 = 39.7%` |
| Runtime automation | `NO` |
| Authority expansion | `NO` |
| Current next action | Continue A4 bounded collection under the existing approved envelope; do not ask for packet approval. |

Latest bounded A4 gap-guard stop:

| Field | Current Value |
| --- | --- |
| Engineering report | `docs/reports/engineering/2026-06-27_170634_a4_gap_guard_stop.md` |
| Final verdict | `A4_BOUNDED_EVIDENCE_COLLECTION_STOPPED` |
| Stop reason | `candidate_not_missing_a4_evidence` |
| Candidate | `10.7.0.5 awg0 -> vless` |
| Successful verified outcomes | `0` |
| Apply | `NO` |
| Restore barrier | `NO` |
| Users moved | `0` |
| A4 evidence | `94 / 156 = 60.3%`; missing `62 / 156 = 39.7%` |
| Runtime automation | `NO` |
| Authority expansion | `NO` |
| Current next action | Wait for a fresh gap-reducing candidate or read-model refresh through existing owners; do not request packet approval and do not synthesize evidence. |

Latest A4 gap-directed candidate existence audit:

| Field | Current Value |
| --- | --- |
| Engineering report | `docs/reports/engineering/2026-06-27_174442_a4_gap_directed_candidate_existence_audit.md` |
| Missing A4 candidate keys | `62` |
| Eligible candidate rows | `40` |
| Gap-reducing eligible candidate rows | `18` |
| Planner-selected candidate | `10.7.0.5 -> vless` |
| Planner-selected candidate missing? | `NO` |
| Users moved | `0` |
| Runtime automation | `NO` |
| Authority expansion | `NO` |
| Verdict | `GAP_REDUCING_CANDIDATES_EXIST_BUT_NOT_SELECTED` |
| Existing owner | `tools/v7-governed-canary-dry-run-cycle`; `admin_core.autonomy_trust_acceleration`; `admin_core.intelligence_workers` |
| Next OMP action | Extend existing A4 governed selection to choose a safe gap-reducing candidate before attempting bounded transaction execution. |

Latest A4 goal-directed selection implementation:

| Field | Current Value |
| --- | --- |
| Engineering report | `docs/reports/engineering/2026-06-27_180848_a4_goal_directed_selection_fix.md` |
| Code commit | `1db9267d862675d85742339532ed8180b10552ef` |
| Deploy id | `deploy-z8-14-Updatesystem-1db9267-20260627T180506` |
| Owner reused | `tools/v7-governed-canary-dry-run-cycle` |
| Missing keys loaded before selection | `YES` |
| Eligible universe scanned | `YES` |
| Non-missing candidate skipped | `YES` |
| Gap-reducing candidate selected when available | `YES` |
| Explicit stop when none available | `NO_SAFE_GAP_REDUCING_A4_CANDIDATE` |
| Runtime automation | `NO` |
| Authority expansion | `NO` |
| Users moved during implementation | `0` |
| Truth | `PASS` |
| Convergence | `PASS / ALIGNED` |
| Next OMP action | Resume A4 bounded representative evidence collection through the existing governed transaction owner. |

Latest A4 evidence requirement sanity audit:

| Field | Current Value |
| --- | --- |
| Engineering report | `docs/reports/engineering/2026-06-27_181934_a4_evidence_requirement_sanity_audit.md` |
| Final verdict | `A4_EVIDENCE_REQUIREMENT_OVERSCOPED` |
| `candidate_count` origin | Dynamic count of concrete `user -> candidate_channel` keys from `candidate-suitability-summary` |
| Current count | `94 / 156 = 60.3%`; missing inventory keys `62` |
| Canonical finding | The `156` keys are inventory coverage, not a canonical A4 completion threshold. |
| A4 intent | Representative action-class evidence for the first action class, not exhaustive full-matrix enumeration. |
| Product Scale alignment | Full user-channel enumeration must not become a permanent autonomy blocker unless explicitly justified. |
| Existing owners | `A4`; `B13`; `A5`; `A6`; `POLICY_005_ACTION_CLASS_PROMOTION`; Product Scale Model |
| Need New Owner | `FALSE` |
| Need New Backlog Item | `FALSE` |
| Runtime changed | `NO` |
| Next OMP action | Extend existing A4/B13 evidence owners to separate representative completion from candidate inventory coverage before continuing bounded collection as a completion strategy. |

Latest Master Action Class Certification Model audit:

| Field | Current Value |
| --- | --- |
| Engineering report | `docs/reports/engineering/2026-06-27_182735_master_action_class_certification_model_audit.md` |
| Final verdict | `ACTION_CLASS_CERTIFICATION_MODEL_COMPLETE` |
| Canonical A4 objective | Materialize representative real outcome evidence for the first action class. |
| First action class | `single-user governed candidate failover` |
| Full certification chain | `A4 -> A5 -> A6 -> B13 -> B12/authority` |
| `missing_candidate_outcomes` role | Inventory coverage / supporting evidence / learning input; not canonical hard gate |
| Current implementation mismatch | `readiness_impact.exact_outcome_deficit_blocks_canary = missing_candidate_outcomes` over-converts inventory deficit into a hard blocker |
| Need New Owner | `FALSE` |
| Need New Backlog Item | `FALSE` |
| Need New Architecture | `FALSE` |
| Next OMP action | `A4_CERTIFICATION_GATE_ALIGNMENT_IN_EXISTING_EVIDENCE_OWNER`; do not move users solely to exhaust all remaining inventory keys. |

Latest Master OMP Certification Alignment implementation:

| Field | Current Value |
| --- | --- |
| Engineering report | `docs/reports/engineering/2026-06-27_215615_master_omp_certification_alignment_implementation.md` |
| Implementation owner | `admin_core.autonomy_trust_acceleration` |
| Existing owners reused | `YES` |
| New owner | `NO` |
| New backlog item | `NO` |
| New architecture | `NO` |
| Runtime behavior changed | `NO` |
| Canonical alignment | `missing_candidate_outcomes` remains visible as `INVENTORY_SIGNAL`; it is no longer exposed as mandatory `missing_evidence` for A4 certification/runtime enablement. |
| Downstream alignment | A5 consumes certified A4 outputs; A6 consumes certified gates and live runtime safety, not exhaustive inventory deficits; B13 consumes representative evidence/reliability. |
| Validation | `python3 -m unittest tests.unit.test_autonomy_trust_acceleration`; `python3 -m unittest tests.unit.test_governed_canary_cli tests.unit.test_operator_execution_pipeline`; `tools/v7-autonomy-trust-evidence-inventory --action-class-runtime-only --pretty` |
| Next OMP action | `A4_REPRESENTATIVE_CERTIFICATION_VALIDATION_AND_CONTINUE_OMP` |

Latest A4 representative certification validation access correction:

| Field | Current Value |
| --- | --- |
| Engineering report | `docs/reports/engineering/2026-06-27_222642_a4_representative_certification_validation.md` |
| Existing owner | `tools/v7-governed-canary-dry-run-cycle`; `admin_core.autonomy_trust_acceleration` |
| Bounded collection command | `tools/v7-governed-canary-dry-run-cycle --execute-a4-bounded-evidence-collection --confirm-a4-bounded-evidence-collection EXECUTE_A4_BOUNDED_EVIDENCE_COLLECTION_APPROVED --max-users 1 --max-evidence-outcomes 68 --pretty` |
| Collection status | `LOCAL_RUN_INVALID_FOR_PRODUCTION_EVIDENCE` |
| Stop reason | `local_runtime_state_unavailable` |
| Current missing A4 candidate keys | `NOT_VERIFIED`; local `0` was caused by absent local `/opt/v7` state and must not be treated as production evidence |
| Transactions attempted | `0` |
| Users moved | `0` |
| Runtime automation enabled | `NO` |
| Authority expanded | `NO` |
| Truth | `PASS` |
| Convergence | `PASS` |
| Production access | Direct SSH read-only attempt to production was denied by authentication; existing production-side owner must be run where `/opt/v7` state is available. |
| OMP meaning | Do not infer A4 candidate absence from local missing runtime state; continue only through authenticated production-side validation. |
| Next OMP action | `A4_PRODUCTION_SIDE_CERTIFICATION_VALIDATION` |

Latest A4 collection input guard implementation:

| Field | Current Value |
| --- | --- |
| Engineering report | `docs/reports/engineering/2026-06-27_224128_a4_collection_input_guard.md` |
| Existing owner | `tools/v7-governed-canary-dry-run-cycle` |
| Implementation | A4 bounded collection now checks required runtime state, candidate snapshot, and evidence sources before calculating missing candidate keys. |
| Stop reason when inputs are unavailable | `runtime_state_unavailable` |
| False completion prevented | Local missing `/opt/v7` state can no longer be interpreted as `no_missing_a4_candidate_outcomes`. |
| Runtime automation enabled | `NO` |
| Users moved | `0` |
| Authority expanded | `NO` |
| Next OMP action | `A4_PRODUCTION_SIDE_CERTIFICATION_VALIDATION` through production-side existing owners. |

Previous bounded A4 collection result:

| Field | Current Value |
| --- | --- |
| Collection status | `STOP_SAFE` after bounded production execution |
| Successful outcomes | `2` |
| Users moved | `10.7.0.20 vless -> awg3`; `10.7.0.21 vless -> awg3` |
| Verification | `PASS` for both governed transactions |
| Rollback | `NOT_REQUIRED` for both governed transactions |
| A4 evidence | `90 / 156 = 57.7%`; missing `66 / 156 = 42.3%` |
| Stop reason | `duplicate_transaction_candidate`; duplicate guard stopped before another lease, restore-barrier write, or apply |
| Runtime automation | `NO`; still disabled |
| Authority expansion | `NO` |
| Current next action | Continue A4 only when a fresh non-duplicate candidate exists; do not synthesize evidence or repeat the duplicate candidate |

Previous single approved A4 transaction:

| Field | Current Value |
| --- | --- |
| Packet | `pkt_preview_a61462aaffb4510b6237fb95` |
| User moved | `10.7.0.5 awg3 -> awg0` |
| Apply | `PASS` |
| Verification | `PASS` |
| Rollback | `NOT_REQUIRED` |
| Outcome closure | `CLOSED`; feedback and learning records written from real observed outcome |
| Users moved | `1` |
| Runtime automation | `NO` |
| Authority expansion | `NO` |
| A4 coverage after outcome | `90 / 156 = 57.7%`; missing `66 / 156 = 42.3%` |
| Progression note | Real outcome was recorded, but representative coverage did not increase; continue with the next fresh A4 candidate through existing OMP. |

Previous bounded A4 authority-envelope run:

| Field | Current Value |
| --- | --- |
| Final verdict | `A4_BOUNDED_EVIDENCE_COLLECTION_STOPPED` |
| Stop reason | `transaction_verification_failed` |
| Transactions attempted | `3` |
| Successful verified outcomes | `2` |
| Successful moves | `10.7.0.22 vless -> awg3`; `10.7.0.23 vless -> awg3` |
| Failed transaction | `10.7.0.24 vless -> awg3` |
| Verification | `FAIL` for `10.7.0.24` |
| Rollback | `ROLLBACK_COMPLETED`; user returned to `vless` |
| A4 evidence | `93 / 156 = 59.6%`; missing `63 / 156 = 40.4%` |
| Runtime automation | `NO` |
| Authority expansion | `NO` |
| Current next action | Do not ask for packet approval. Continue bounded A4 collection under the existing approved envelope. |

Latest rollback learning audit:

| Field | Current Value |
| --- | --- |
| Audit report | `docs/reports/engineering/2026-06-27_162929_master_rollback_learning_audit.md` |
| Rollback behavior | `EXPECTED_RUNTIME_PROTECTION`; verification failed and rollback completed to `vless` |
| Exact verification failure | Assignment expected `awg3`, but table route and route_get for `10.7.0.24` still used `tun0` after apply |
| Planner verdict | No planner defect proven; candidate was in A4 scope and passed pre-apply guards |
| Feedback defect | Fixed and deployed: `tools/v7-governed-canary-dry-run-cycle::materialize_governed_transaction_feedback` now materializes terminal outcome classification and `admin_core.operator_execution_feedback` consumes terminal state before feedback/learning |
| Incorrect learning result | Previous behavior produced `outcome_status=success`, `outcome_quality=SUCCESS`, positive trust/recommendation deltas |
| Correct learning result | `ROLLBACK_SUCCESS` / rollback learning; preserve rollback success evidence; do not count as successful move evidence or promotion success |
| Existing owner | `tools/v7-governed-canary-dry-run-cycle`; `admin_core/operator_execution_feedback.py`; A4 evidence owners |
| Need New Owner | `FALSE` |
| Need New Backlog | `FALSE` |
| Current next action | Continue bounded A4 collection without packet-by-packet approval; preserve terminal classifications for every real outcome |

Non-blocking A4 optimization note:

| Field | Current Value |
| --- | --- |
| Optimization | `A4_MARGINAL_EVIDENCE_VALUE_RANKING` |
| Status | `RECORDED_NOT_BLOCKING` |
| Classification | `FUTURE_EFFICIENCY_WORK` |
| Blocks A4 | `NO` |
| Creates backlog item | `NO` |
| Current behavior | Bounded A4 collection asks: `Does this fresh candidate reduce the current A4 evidence gap?` |
| Future behavior | Rank currently eligible candidates by marginal evidence value and prefer the highest-value safe one. |
| Marginal Evidence Value | Expected reduction of the current A4 representative evidence gap + verified learning value + new cohort/user/channel coverage value - movement/risk/cost/anti-flap penalty. |
| Boundaries | No new authority; no runtime automation; no batch movement; one user per governed A4 transaction; stop on any failed live gate; no synthetic evidence; no threshold or formula change now. |
| Existing owners | A4 evidence matcher/read-model owners; governed dry-run owner; intelligence workers; outcome leverage model; OMP. |
| Current OMP action | Continue current bounded evidence collection; this note must not delay A4 evidence collection. |

Latest safe deployment result:

| Field | Current Value |
| --- | --- |
| Deployed commit | `19882a14d81cc8a6d05e8e46d40fc63ae7ed5446` |
| Deploy id | `deploy-z8-14-Updatesystem-19882a1-20260627T125619` |
| Deployed backlog items | `A1`, `A2`; A3 approval-to-execution lease binding fix; A3 approved plan lock snapshot-gate consumption fix; A3 real no-rollback outcome closure; A4 governed transaction feedback materialization; A4 bounded evidence collection mode; A4 bounded collection evidence/duplicate pre-apply guard |
| Safety | Bounded collection mode reuses the existing one-user governed transaction owner, requires explicit confirmation, stops before lease/restore/apply for non-missing or duplicate candidates, keeps runtime automation disabled, and does not expand authority. |
| Truth | Full `tools/v7-truth-check --all --json` with network access: `PASS`; local, GitHub, and production all at `19882a14d81cc8a6d05e8e46d40fc63ae7ed5446`. |
| Convergence | Runtime aligned; deploy delta empty; runtime action guard `READY_FOR_RUNTIME_ACTION`. |
| Current stop | `NONE_FOR_CLASSIFICATION_FIX`: terminal classification fix is implemented, tested, deployed, and verified; continue A4 bounded evidence collection |

Latest A4 completion:

| Field | Current Value |
| --- | --- |
| Engineering report | `docs/reports/engineering/2026-06-27_232150_a4_closure_read_model_filter.md` |
| Final A4 state | `DONE` |
| Real evidence | A4 bounded collection reduced missing candidate inventory to `0`; inventory signals are empty. |
| Outcome closure | `COMPLETE`; production replay showed `387` valid closure candidates, `0` missing closure records, and `8011` non-closure history records ignored. |
| Deploy | `deploy-z8-14-Updatesystem-f49f4fa-20260627T232657` |
| Commit | `f49f4fa8d4ffe0d582bd807f0b45e7e48d724b38` |
| Truth/convergence | Truth `PASS`; convergence `ALIGNED`. |
| Runtime automation | `NO` |
| Authority expanded | `NO` |
| Users moved by read-model fix | `0` |
| Next OMP action | `A5_CERTIFY_CLASS_LEVEL_BLAST_RADIUS_EVIDENCE_BEYOND_ONE_USER_GUARD` |

## 2.13. Implementation Program Loop

Future production implementation loop:

```text
Read Kernel
  -> Read OMP
  -> Read Current Program State
  -> Read Implementation Backlog
  -> Apply Implementation Priority Model
  -> Determine highest unfinished implementation leverage
  -> Semantic Reuse Audit
  -> Reuse
  -> Extend
  -> Implement
  -> Deploy
  -> Truth
  -> Convergence
  -> Certification
  -> Update Current Program State
  -> Update OMP
  -> Mark backlog item DONE
  -> Recalculate backlog
  -> Authority Evaluation
  -> Continue
```

Stop only at:

- `OPERATIONAL_AUTHORITY`
- `ENGINEERING_AUTHORITY`
- `REAL_WORLD_LIMIT`
- `UNSAFE_IMPLEMENTATION`
- `FUNDAMENTAL_ARCHITECTURE_GAP`

Latest optimizer iteration duplication result `2026-06-25`:

| Field | Current Value |
| --- | --- |
| Duplicate owners | `NONE` |
| Duplicate planners | `NONE` |
| Duplicate governance | `NONE` |
| Duplicate execution | `NONE` |
| Duplicate knowledge | `NONE` |
| Duplicate lifecycle | `NONE` |
| Duplicate API | `NONE` |
| Duplicate CLI | `NONE` |
| Duplicate read model | `NONE` |
| Verdict | `NONE` |

Latest OMP V2.2 duplication result:

| Field | Current Value |
| --- | --- |
| Duplicate owners | `NONE` |
| Duplicate planners | `NONE` |
| Duplicate governance | `NONE` |
| Duplicate execution | `NONE` |
| Duplicate truth sources | `NONE` |
| Duplicate architecture | `NONE` |
| Verdict | `NONE` |

Latest OMP V2.3 duplication result:

| Field | Current Value |
| --- | --- |
| Duplicate runtime owners | `NONE` |
| Duplicate planners | `NONE` |
| Duplicate governance | `NONE` |
| Duplicate execution | `NONE` |
| Duplicate truth sources | `NONE` |
| Duplicate architecture | `NONE` |
| Documentation split | `V7_KERNEL` and `V7_CURRENT_PROGRAM_STATE` are control-plane documentation owners, not runtime/code owners. |
| Verdict | `NONE` |

## 3. Program States

| State | Meaning |
| --- | --- |
| `NOT_STARTED` | Phase is known but no implementation or verification has begun. |
| `ACTIVE` | Phase is the current work item and may proceed under the stop conditions below. |
| `BLOCKED` | Phase hit an allowed stop condition. |
| `CERTIFIED` | Phase passed tests, truth, convergence, and evidence review. |
| `COMPLETED` | Phase is certified and its results are absorbed into reference/program state. |

## 4. Active Program Rule

`Operational Maturity`

Purpose:

Move V7 from architecture-complete / authority-bound autonomy to production maturity through continuous bottleneck reduction.

The program no longer asks "what is the next phase?" first and no longer asks "what architecture is missing?" first.

The program asks:

```text
Current System State
  -> Current Highest Bottleneck
  -> Current Highest Implementation Leverage
  -> Current Authority Class
  -> Current Real World Limit
  -> Next Best Action
```

## 5. Historical System State Snapshot

Classification: `HISTORICAL_SNAPSHOT`.

Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

This section preserves an earlier recalculated OMP state. It must not be consumed as authoritative live current state unless the same value is present in `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

Live current state is resolved only from CPS.

Historical field names preserve snapshot terminology only. Live volatile state must be read from CPS.

| Maturity Area | Snapshot State At Capture | Evidence |
| --- | --- | --- |
| Architecture maturity | `ARCHITECTURE_COMPLETE` | Final system architecture synthesis: remaining architectural weaknesses `0`; optional improvements are not implementation blockers. |
| Knowledge maturity | `ADVANCED_BUT_NOT_AUTONOMY_COMPLETE` | Knowledge quality model exists; safety is autonomy-grade; several knowledge classes still need real outcomes, service/user/SLA fit depth, client observation, cohort/SLA scale, and aging/retirement. |
| Decision maturity | `READY_UNTIL_OPERATIONAL_AUTHORITY` | Planner, knowledge-to-decision, governed dry-run, packet preview, restore/rollback preview, and self-stop are connected. |
| Outcome maturity | `REAL_OUTCOMES_REQUIRED` | Candidate outcome gap remains `72`; missing candidate outcomes are not hidden, they have not happened yet. |
| Learning maturity | `CONNECTED_AFTER_OUTCOME` | Feedback, outcome closure, trust evolution, and learning refresh owners exist and are connected, but need real governed/manual outcomes. |
| Suitability maturity | `HIGHEST_BOTTLENECK` | Suitability cannot become autonomy-grade without more real candidate outcomes and stronger candidate source confidence. |
| Authority maturity | `OPERATIONAL_AUTHORITY_REACHED` | Production governed dry-run reaches exact packet approval boundary before restore-barrier write or apply. |
| Operational maturity | `PRODUCTION_PROGRAM_ACTIVE` | OMP V4.0 optimizes production leverage through existing-owner implementation and authority evolution; no daemon, no autonomous apply, no user movement without authority. |

## 6. Historical Highest Bottleneck Snapshot

Classification: `HISTORICAL_SNAPSHOT`.

Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

Live highest bottleneck is resolved only from `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

Exactly one bottleneck:

`Suitability`

Why this bottleneck is highest right now:

| Evidence | Meaning |
| --- | --- |
| Missing candidate outcomes: `72` | The main weak object is real candidate suitability evidence. |
| Maximum projected current suitability remains below TIER_2 even after current missing outcomes | More rows alone are not enough; correctness/source confidence must improve too. |
| Architecture missing classes: none | The limiting factor is not architecture. |
| Governed dry-run reaches `OPERATIONAL_AUTHORITY` | The limiting factor is not disconnected planner/packet/restore/learning owners. |
| Confidence/trust/prediction are also below floor | They matter, but suitability is the bottleneck that specifically requires real candidate outcome closure. |

Recompute rule:

After every certification, classify bottlenecks across `Architecture`, `Knowledge`, `Decision`, `Outcome`, `Learning`, `Suitability`, `Prediction`, `Authority`, `Operational`, and `Scale`. Select exactly one class based on the largest maturity gain that cannot be obtained by already-certified safe automation.

## 7. Historical Highest Implementation Leverage Snapshot

Classification: `HISTORICAL_SNAPSHOT`.

Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

Live HIL is resolved only from `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

Implementation:

`IMPLEMENT_AUTHORITY_BOUNDARY_APPROVAL_PROMPT`

This is implementation work, not research and not architecture.

Definition:

Emit a ready-to-copy exact operator approval prompt inside the existing governed canary dry-run cycle whenever the cycle stops at `OPERATIONAL_AUTHORITY` with a ready packet.

Exact owner:

`Governed Canary Knowledge-Gated Dry-Run Cycle / Runtime Model composition`

Exact module:

`admin_core/operator_execution_pipeline.py::governed_canary_knowledge_gated_dry_run_cycle`

Exact files:

- `admin_core/operator_execution_pipeline.py`
- focused tests for governed dry-run authority-bound prompt output

Why this is first:

| Criterion | Result |
| --- | --- |
| Production leverage | Removes the last safe implementation gap before authority-bound governed canary execution. |
| Existing owner reuse | Uses the existing governed canary dry-run cycle and Runtime Model composition. |
| Architecture risk | None; architecture is complete and unchanged. |
| Runtime safety | Read-only approval prompt output only; no restore-barrier write, no apply, no user movement, no daemon, no timer. |
| Bottleneck relevance | Gives the operator an exact current packet command so the next real outcome can proceed only through explicit authority. |
| Testability | Authority boundary prompt emission, stale approval invalidation, unsafe stop suppression, and no-mutation guarantees can be tested without mutation. |
| Certification path | Truth and convergence can certify no runtime mutation and no user movement. |

Required approval prompt fields:

- packet preview id;
- decision id;
- operation id;
- selected move hash;
- user;
- current channel;
- target channel;
- rollback target;
- rollback manifest id;
- authority tier;
- authority status;
- allowed action;
- forbidden actions;
- final exact approval command text.

Expected implementation order:

1. Add read-only authority-bound approval prompt output to existing governed canary dry-run cycle.
2. Add focused tests for prompt emission, changed-packet invalidation, unsafe stop suppression, and no movement/apply.
3. Add read-only verification for the approval prompt output.
4. Certify with truth and convergence.
5. Update Current Program State.

The old bottleneck action, governed candidate suitability outcome closure, remains the highest real-outcome action. The approval-to-execution lease binding defect is fixed and deployed; the current blocker is now an unsafe implementation defect inside the existing autoswitch owner.
The current implementation-first optimizer must fix approved plan lock consumption through the intelligence snapshot gate before requesting another packet approval or attempting apply again.

## 8. Historical Authority Class Snapshot

Classification: `HISTORICAL_SNAPSHOT`.

Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

Live authority class is resolved only from `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

| Field | Current Value |
| --- | --- |
| Current authority level | `NONE`; current stop is engineering safety, not authority. |
| Current stop reason | `UNSAFE_IMPLEMENTATION` |
| Boundary location | After approved packet consumption and restore-barrier clearance, before mutation inside `tools/v7-users-autoswitch` intelligence snapshot gate. |
| Current exact runtime posture | Restore-barrier clearance was written for the approved packet, guarded apply failed closed before movement, no autonomous apply, no daemon enablement. |
| Next authority action | None until the existing autoswitch owner preserves approved locked selected moves through the intelligence snapshot gate. |

Current production evidence:

- approval-to-execution lease binding fix is deployed and production truth/convergence pass;
- operator approved exact packet `pkt_preview_4eb137c926917c2761faadb4`;
- execution lease `execlease_19550ea3b6750ed163344f8a` preserved packet identity;
- restore-barrier clearance `rbclear_1951ca727830c155efc8cf0e` was written through the existing owner;
- guarded apply denied mutation with `approved_plan_lock_selected_moves_missing` and unsafe blocker `approved_plan_lock_snapshot_gate_stop_required`;
- selected moves were present before restore-barrier clearance and zero after the intelligence snapshot gate;
- no user movement, daemon, timer, or authority expansion occurred;
- `apply=false`;
- `users_moved=0`;
- `runtime_mutation=false`.

## 9. Historical Reality Limit Snapshot

Classification: `HISTORICAL_SNAPSHOT`.

Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

Live reality limit is resolved only from `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

Current limit:

`REAL_CANDIDATE_OUTCOMES_HAVE_NOT_HAPPENED`

What cannot honestly improve much more without more real-world activity:

| Limit | Evidence |
| --- | --- |
| Candidate suitability correctness | Missing candidate outcomes are current user -> candidate-channel pairs that require governed/manual action before they can become evidence. |
| Candidate source confidence | Existing consumed candidate outcomes are not strong enough to certify autonomy-grade suitability. |
| TIER_2 suitability | Even converting all current missing outcomes at current assumptions does not guarantee floor closure. |
| Client observation / cohort / SLA depth | These remain future/scale enrichments, not current architecture blockers. |

What does not require new architecture:

- planner;
- governance preview;
- packet generation;
- restore/rollback preview;
- verification plan;
- outcome closure;
- feedback;
- learning refresh;
- truth/convergence.

## 10. Program Optimizer

After every completed implementation, Codex must recalculate:

1. Current system state.
2. Current highest bottleneck.
3. Current highest implementation leverage.
4. Current authority class.
5. Current reality limit.
6. Next best action.
7. Whether automatic continuation is allowed.

Optimizer rules:

| Condition | Program Response |
| --- | --- |
| Highest implementation leverage is read-only | Continue automatically. |
| Highest implementation leverage is safe existing-owner implementation with no runtime apply | Continue automatically. |
| Highest implementation leverage requires exact restore-barrier write for an approved packet | Stop at `OPERATIONAL_AUTHORITY`. |
| Highest implementation leverage requires exact runtime apply | Stop at `OPERATIONAL_AUTHORITY`. |
| Highest implementation leverage requires exact user movement | Stop at `OPERATIONAL_AUTHORITY`. |
| Highest implementation leverage requires exact rollback apply | Stop at `OPERATIONAL_AUTHORITY`. |
| Highest implementation leverage requires authority expansion | Stop at `ENGINEERING_AUTHORITY`. |
| Highest implementation leverage requires new action class, new runtime capability, new autonomous policy, or blast-radius expansion | Stop at `ENGINEERING_AUTHORITY`. |
| Highest implementation leverage requires more users/channels/services/reality | Stop at `REAL_WORLD_LIMIT`. |
| Highest implementation leverage would create duplicate planner/governance/execution/truth | Stop at `UNSAFE_IMPLEMENTATION`. |
| Certified reports reveal a fundamental missing owner | Stop at `FUNDAMENTAL_ARCHITECTURE_GAP`. |

Safety-Bounded Authority split rule:

When the highest leverage action requires real outcomes, Codex must split it into:

| Portion | Work | Program Response |
| --- | --- | --- |
| Safe automatic preparation | Refresh evidence; refresh packet preview; verify restore/rollback preview; verify verification plan; verify outcome closure plan; verify learning path; update OMP; present exact authority decision. | Continue automatically. |
| Operational-authority execution | Exact restore-barrier write; exact runtime apply; exact user movement; exact rollback apply; exact production action. | Stop at `OPERATIONAL_AUTHORITY`. |
| Engineering-authority change | Authority expansion; new action class; new runtime capability; new autonomous policy; blast-radius expansion; daemon/timer enablement. | Stop at `ENGINEERING_AUTHORITY`. |

The safe automatic portion continues automatically.

The authority-bound portion stops at the normalized authority class: `OPERATIONAL_AUTHORITY` for exact production action approval, or `ENGINEERING_AUTHORITY` for capability/policy/authority expansion.

## 10.1. Root Cause Engine

OMP must run the Root Cause Engine before exposing any stop condition.

Raw blocker codes are technical details only. They must never be the primary result of an OMP stop.

Primary stop output must always be:

```text
Root Cause
  -> Owner
  -> Fix
  -> Expected Evidence
  -> Next Action
```

Root Cause Engine workflow:

```text
Blocker
  -> Root Cause Analysis
  -> Owner Attribution
  -> Implementation Classification
  -> Concrete Engineering Task
  -> Expected Completion Evidence
  -> Continue Decision
```

Required stop record:

| Field | Requirement |
| --- | --- |
| Root Cause | Concrete cause, not a generic blocker code. |
| Responsible owner | Exact existing owner, module, and function when known. |
| Why it happened | Specific mechanism that created the stop. |
| Why existing safety worked | Which gate prevented unsafe runtime behavior. |
| Can existing owner be extended? | `YES` or `NO`; default is `YES` unless proven otherwise. |
| Need New Owner | `FALSE` unless a proven `FUNDAMENTAL_ARCHITECTURE_GAP` requires a new owner. |
| Implementation Class | One of `BUG`, `OWNER_EXTENSION`, `CONFIGURATION`, `CERTIFICATION`, `REAL_WORLD_LIMIT`, `AUTHORITY`, `DOCUMENTATION`. |
| Concrete implementation task | Backlog-ready task, not a recommendation. |
| Expected completion evidence | Observable evidence required to close the task. |
| Automatic continuation | Whether OMP may continue automatically after the task completes. |
| Intent Gap Detection status | `INTENT_GAP_DETECTED`, `NO_INTENT_GAP`, `INTENT_GAP_UNKNOWN_WITH_REASON`, or `NOT_APPLICABLE_WITH_REASON`. |
| Intent Responsibility Resolution status | `RESPONSIBILITY_RESOLVED`, `RESPONSIBILITY_UNKNOWN_WITH_REASON`, `BOUNDARY_CONFIRMED`, or `NOT_APPLICABLE_WITH_REASON`. |
| Responsibility failure class | Failure class from Intent Responsibility Resolution, or `NOT_APPLICABLE_WITH_REASON`. |
| Last responsible link | Owner-mapped last failed Engineering Chain link, or `UNKNOWN_WITH_REASON`. |
| Automation Gap Closure status | `FUNDAMENTAL_ARCHITECTURE_BOUNDARY`, `STOP_DERIVED_BDP_INPUT_ROUTED`, `IMPLEMENTATION_CANDIDATE_CONSUMED`, or `AUTOMATION_GAP_CLOSURE_BLOCKED_WITH_REASON`. |
| Engineering Intent Closure status | `INTENT_CLOSED`, `INTENT_NOT_CLOSED`, `FUNDAMENTAL_ARCHITECTURE_BOUNDARY`, or `NOT_APPLICABLE_WITH_REASON`. |
| Human intervention classification | `FUNDAMENTAL_BOUNDARY`, `AUTOMATABLE_WITH_EXISTING_ARCHITECTURE`, `AUTHORITY_REQUIRED`, `REAL_WORLD_REQUIRED`, or `UNKNOWN_WITH_REASON`. |
| BDP route decision | Existing BDP route to produce / update Candidate Instance, or `NOT_APPLICABLE_WITH_REASON`. |

Automatic classification:

| Stop Condition | Primary Classification | OMP Meaning | Next Action |
| --- | --- | --- | --- |
| `UNSAFE_IMPLEMENTATION` | `BUG` or `OWNER_EXTENSION` | Existing implementation path is unsafe, incomplete, or loses required state. | Fix the responsible existing owner, test, deploy if required, then resume OMP. |
| `OPERATIONAL_AUTHORITY` | `AUTHORITY` | Engineering is complete and the next action is one exact production operation, such as packet execution, rollback, restore-barrier write, runtime apply, or user movement. | Produce exact approve/reject decision for the current production action. |
| `ENGINEERING_AUTHORITY` | `AUTHORITY` | Engineering cannot continue because capability, policy, authority, action-class, runtime, or blast-radius approval is required. | Produce exact engineering approval or authority expansion request. |
| Legacy raw `AUTHORITY_BOUNDARY` | normalize before output | Compatibility-only blocker code. | Convert to `OPERATIONAL_AUTHORITY` or `ENGINEERING_AUTHORITY` before reporting status. |
| `REAL_WORLD_LIMIT` | `REAL_WORLD_LIMIT` | The next maturity gain requires real production evidence that cannot be synthesized. | Identify exact real-world action or observation required. |
| `FUNDAMENTAL_ARCHITECTURE_GAP` | `OWNER_EXTENSION` or architecture review | Existing certified owners cannot satisfy the requirement. | Prove why reuse/extension is impossible before any architecture change. |

Root Cause Engine constraints:

- reuse existing owners first;
- never create a new planner;
- never create new governance;
- never create new execution;
- never create a new truth source;
- never treat reports, policies, or architecture documents as implementation queues;
- never expose only `UNSAFE_IMPLEMENTATION`, `REAL_WORLD_LIMIT`, legacy raw `AUTHORITY_BOUNDARY`, or `FUNDAMENTAL_ARCHITECTURE_GAP` as the OMP result.

### Automation Gap Closure Cycle

Status: `CANONICAL`

Automation Gap Closure Cycle is the mandatory OMP continuation law for every unfinished Engineering Intent in any Engineering Chain.

STOP is one possible signal of unfinished Engineering Intent.

STOP is not the only trigger.

It does not create:

- a new program;
- a new owner;
- a new architecture;
- a new Planner;
- a new Runtime;
- a new automation system;
- an Automation Candidate;
- an Automation Graph.

It reuses:

- Root Cause Engine;
- Automatic-First Rule;
- Architecture Closed by Default;
- BDP Candidate Reality Gate;
- BDP minimal Discovery Economy;
- OMP Implementation Candidate Identity;
- OMP Implementation Candidate Eligibility / Admission;
- Mission Formation;
- Behavior Enforcement Framework;
- Execution Certification;
- State Transition Verification;
- Engineering Intent Closure Validation;
- Intent Responsibility Resolution;
- Engineering Report Lifecycle;
- Current Program State;
- existing authority, verification, rollback, runtime, production, and Engineering Chain owners.

Purpose:

```text
Every Engineering Intent must automatically answer:

Was the Engineering Intent achieved?
If not, why not?
Was there an explicit STOP?
If yes, why did the STOP happen?
Is it a fundamental system boundary?
Or is it a non-automated engineering process inside existing architecture?
Can existing owners/capabilities/missions/verification/authority/rollback/runtime/Engineering Chain express the fix?
If yes, route intent-gap input to existing BDP -> OMP candidate production and admission.
If no, prove the fundamental boundary before recording FUNDAMENTAL_ARCHITECTURE_GAP.
```

#### Intent Gap Detection

After any completed Engineering Chain, Mission, Capability, Behavior, Execution, Verification, Certification, State Transition, Implementation, or OMP meaningful step, OMP must automatically determine whether the original Engineering Intent was achieved.

This detection reuses Behavior Enforcement, State Transition Verification, Execution Certification, Automation Gap Closure, Engineering Intent Closure Validation, BDP, and OMP.

It does not create an Intent Gap Engine, Automation Engine, Intent Monitor, Background Scanner, new program, or new owner.

Intent Gap Detection must run even when:

- function completed;
- Execution returned `PASS`;
- Verification returned `PASS`;
- no explicit STOP exists;
- implementation completed;
- certification completed;
- report was created.

Any of the following conditions creates Automation Gap Analysis:

| Condition | Meaning |
| --- | --- |
| Expected State does not match Current State | Formal success did not produce the intended state. |
| Engineering Chain did not reach Legal Terminal Consumer | Chain remains incomplete. |
| Behavior Chain is not `COMPLETE` | Behavior propagation is partial, blocked, broken, or unknown. |
| Output Produced but Output Consumed is not verified | Existing output is not proven to affect consumer behavior. |
| Consumer did not change behavior | Consumption did not produce the intended behavior. |
| Next Output was not produced | Chain failed to continue. |
| State Transition did not complete | Current state did not move to required / expected state. |
| Root Cause still exists | Original cause remains. |
| Automation Gap is not closed | Previous gap is still intermediate or blocked. |
| Engineering Intent is not achieved | Declared intent remains unmet. |

Allowed detection results:

| Result | Meaning | Next action |
| --- | --- | --- |
| `NO_INTENT_GAP` | Intent achieved and no automation gap remains. | Continue OMP. |
| `INTENT_GAP_DETECTED` | Intent not achieved, whether or not STOP exists. | Run Automation Gap Closure Cycle. |
| `INTENT_GAP_UNKNOWN_WITH_REASON` | Evidence is insufficient to determine intent closure. | Hold with missing owner/evidence and smallest existing next action. |

`INTENT_GAP_DETECTED` must trigger Automation Gap Closure.

OMP must not treat a formal `PASS` as closure when Intent Gap Detection finds unmet intent.

#### Intent Responsibility Resolution

After every `INTENT_GAP_DETECTED`, OMP must resolve which Engineering Chain link last failed its contract before routing the gap into BDP.

Intent Responsibility Resolution is not a Responsibility Engine, graph, owner, queue, Planner, Runtime, Intent Engine, Automation Engine, or new Candidate type.

It reuses:

- Behavior Enforcement fields;
- State Transition Verification fields;
- Root Cause Engine;
- Engineering Intent Closure Validation;
- Automation Gap Closure Cycle;
- BDP Candidate Reality Gate;
- Engineering Chain Dependency Projection;
- Function Graph as discovery / context evidence only;
- SYSTEM_MAP ownership mapping;
- Current Program State.

Intent Responsibility Resolution must answer:

1. Which Engineering Intent was not achieved?
2. Which Engineering Chain should have closed it?
3. Which Producer should have produced Output?
4. Was Output Produced?
5. Was Output Available?
6. Which Consumer should have consumed Output?
7. Does Consumer exist?
8. Did Consumer consume Output?
9. Was Consumption verified?
10. Did Consumer behavior change?
11. Was Next Output produced?
12. Was Legal Terminal Consumer reached?
13. Which owner last failed its contract?
14. Is the failure automatable or a fundamental / legal boundary?

##### Responsibility Failure Classes

Allowed responsibility failure classes:

| Failure class | Meaning |
| --- | --- |
| `PRODUCER_OUTPUT_MISSING` | Producer should have produced Output, but Output is absent. |
| `PRODUCER_OUTPUT_UNAVAILABLE` | Output exists but is unavailable to the Consumer. |
| `CONSUMER_MISSING` | Expected Consumer is absent or not owner-mapped. |
| `CONSUMER_DID_NOT_CONSUME` | Consumer exists but did not consume Output. |
| `CONSUMPTION_NOT_VERIFIED` | Consumption is claimed or assumed but not proven. |
| `CONSUMER_BEHAVIOR_NOT_CHANGED` | Consumer consumed Output, but behavior did not change. |
| `NEXT_OUTPUT_NOT_PRODUCED` | Consumer behavior should have produced the next Output, but it did not. |
| `LEGAL_TERMINAL_CONSUMER_NOT_REACHED` | Engineering Chain did not reach Legal Terminal Consumer. |
| `STATE_TRANSITION_NOT_COMPLETED` | State Transition Verification did not complete. |
| `EXPECTED_STATE_NOT_REACHED` | Expected State does not match Current State. |
| `ROOT_CAUSE_STILL_EXISTS` | Original root cause remains. |
| `VERIFICATION_FAILURE` | Verification owner did not confirm the required result. |
| `ROLLBACK_OR_STOP_SAFE_BOUNDARY` | Progress is legally blocked by rollback, containment, or STOP_SAFE boundary. |
| `RUNTIME_BOUNDARY` | Runtime boundary legally blocks continuation. |
| `PRODUCTION_BOUNDARY` | Production boundary legally blocks continuation. |
| `AUTHORITY_BOUNDARY` | Legal authority boundary is required before continuation. |
| `REAL_WORLD_BOUNDARY` | Real event, observation, or production evidence is required. |
| `FUNDAMENTAL_ARCHITECTURE_BOUNDARY` | Existing architecture cannot express the behavior after full reuse/extension proof. |
| `UNKNOWN_WITH_REASON` | Evidence is insufficient; missing owner/evidence and smallest existing next action must be named. |

##### Last Responsible Link

Every Intent Gap must produce `last_responsible_link`.

Required format:

| Field | Required value |
| --- | --- |
| producer_owner | Existing producer owner or `UNKNOWN_WITH_REASON`. |
| producer_output | Expected / actual output or `MISSING_WITH_REASON`. |
| consumer_owner | Existing expected consumer or `MISSING_WITH_REASON`. |
| expected_consumption | Required consumption action. |
| expected_behavior_change | Required consumer behavior change. |
| expected_next_output | Required next output. |
| failure_class | Responsibility Failure Class. |
| evidence_pointer | Existing evidence pointer or `UNKNOWN_WITH_REASON`. |
| missing_evidence | Missing owner/evidence or `NONE`. |
| responsible_owner | Existing owner responsible for the failed contract field. |
| smallest_existing_next_action | Smallest existing action to resolve or prove boundary. |

##### Resolution Order

Intent Responsibility Resolution must inspect the chain in this order:

```text
Engineering Intent
  -> Expected State
  -> Engineering Chain
  -> Producer
  -> Output Produced
  -> Output Available
  -> Expected Consumer
  -> Consumer Exists
  -> Consumer Consumed Output
  -> Consumption Verified
  -> Consumer Behavior Changed
  -> Next Output Produced
  -> State Transition Completed
  -> Legal Terminal Consumer
  -> Intent Closed
```

At the first failed mandatory link, OMP must record:

- `failure_class`;
- `responsible_owner`;
- evidence;
- missing evidence;
- automation feasibility;
- BDP input specialization.

##### Automatable Responsibility Classes

If failure class is one of:

- `PRODUCER_OUTPUT_MISSING`;
- `PRODUCER_OUTPUT_UNAVAILABLE`;
- `CONSUMER_MISSING`;
- `CONSUMER_DID_NOT_CONSUME`;
- `CONSUMPTION_NOT_VERIFIED`;
- `CONSUMER_BEHAVIOR_NOT_CHANGED`;
- `NEXT_OUTPUT_NOT_PRODUCED`;
- `LEGAL_TERMINAL_CONSUMER_NOT_REACHED`;
- `STATE_TRANSITION_NOT_COMPLETED`;
- `EXPECTED_STATE_NOT_REACHED`;
- `ROOT_CAUSE_STILL_EXISTS`;
- `VERIFICATION_FAILURE`;

and existing owners can express the correction, OMP must route a specialized input package to BDP.

##### Boundary Responsibility Classes

If failure class is one of:

- `AUTHORITY_BOUNDARY`;
- `REAL_WORLD_BOUNDARY`;
- `RUNTIME_BOUNDARY`;
- `PRODUCTION_BOUNDARY`;
- `ROLLBACK_OR_STOP_SAFE_BOUNDARY`;

OMP must not create a Candidate automatically and must not call the condition an Automation Gap by default.

OMP must record the legal boundary and produce the exact authority, real-world, safety, runtime, production, rollback, or STOP_SAFE requirement.

##### Unknown Responsibility

If OMP cannot resolve responsibility, it must record:

```text
UNKNOWN_WITH_REASON
```

with:

- missing owner;
- missing evidence;
- failed or unknown chain segment;
- smallest existing next action.

No generic Automation Gap may be routed to BDP while responsibility remains unknown.

#### Cycle

After each STOP or detected Intent Gap, OMP must automatically run:

```text
Engineering Intent
  -> Intent Gap Detection
  -> Intent Responsibility Resolution
  -> STOP Classification if STOP exists
  -> Intent Gap Classification if STOP does not exist
  -> Root Cause Analysis
  -> Human Intervention Detection
  -> Architecture Boundary Check
  -> Automation Feasibility Check
  -> Reuse Existing Capability Check
  -> STOP-Derived or Intent-Gap-Derived BDP Input Routing when automation is possible
  -> Implementation Candidate Instance consumed by OMP when BDP produces it
  -> Mission / Implementation / Verification / Execution Certification
  -> Engineering Intent Closure Validation
  -> Fundamental Boundary Confirmation when automation is impossible
```

#### STOP Classification

OMP must classify every STOP as exactly one of:

| Classification | Meaning | Required result |
| --- | --- | --- |
| `FUNDAMENTAL_ARCHITECTURE_BOUNDARY` | Existing architecture cannot express the needed behavior after reuse/extension proof. | Record proof and stop with existing canonical boundary. |
| `AUTOMATABLE_WITH_EXISTING_ARCHITECTURE` | STOP is caused by a manual or non-automated engineering step that existing owners can express. | Route STOP-derived input to existing BDP -> OMP candidate path. |
| `AUTHORITY_REQUIRED` | STOP is a legitimate authority boundary. | Produce exact authority decision context; do not create architecture. |
| `REAL_WORLD_REQUIRED` | STOP requires real production observation or action that cannot be synthesized. | Produce exact real-world action / observation requirement. |
| `UNKNOWN_WITH_REASON` | Required evidence is missing. | Hold with missing owner/evidence and smallest existing next action. |

OMP must not leave a STOP or Intent Gap in an unexplained manual state.

#### Intent Gap Classification Without STOP

If no explicit STOP exists, OMP must classify the unfinished Engineering Intent by the failed closure condition:

| Classification | Trigger |
| --- | --- |
| `EXPECTED_STATE_NOT_REACHED` | Expected State differs from Current State. |
| `LEGAL_TERMINAL_CONSUMER_NOT_REACHED` | Engineering Chain did not reach Legal Terminal Consumer. |
| `BEHAVIOR_CHAIN_NOT_COMPLETE` | Behavior Chain Status is not `COMPLETE`. |
| `OUTPUT_NOT_CONSUMED` | Produced output lacks verified consumption. |
| `CONSUMER_BEHAVIOR_NOT_CHANGED` | Consumer did not change behavior. |
| `NEXT_OUTPUT_NOT_PRODUCED` | Chain did not produce the expected next output. |
| `STATE_TRANSITION_NOT_COMPLETED` | State Transition Verification did not complete. |
| `ROOT_CAUSE_STILL_EXISTS` | Original root cause remains. |
| `AUTOMATION_GAP_NOT_CLOSED` | Existing automation gap remains intermediate or blocked. |
| `ENGINEERING_INTENT_NOT_ACHIEVED` | Intent remains unmet for another owner-mapped reason. |

#### Human Intervention Detection

OMP must determine whether the STOP or Intent Gap requires human action because of:

- legitimate operational authority;
- legitimate engineering authority;
- real-world evidence that cannot be synthesized;
- safety / rollback / verification / runtime boundary;
- missing owner evidence;
- a manual process that could be automated using existing architecture.

If the human step is legitimate authority or real-world evidence, it is not an automation gap.

If the human step exists only because an engineering transition is not automated, it is an automation gap.

#### Automation Feasibility Check

Before classifying any STOP as fundamental, OMP must check whether the work can be expressed through existing:

- owner;
- capability;
- Mission;
- verification;
- authority;
- rollback;
- Runtime;
- Engineering Chain;
- Behavior Chain;
- Current Program State;
- Production Maturity;
- Engineering Report;
- BDP Candidate production path.

If any existing path can express the fix, `FUNDAMENTAL_ARCHITECTURE_GAP` is forbidden.

#### STOP-Derived Or Intent-Gap-Derived BDP Input Routing

OMP must not directly create an `Implementation Candidate Instance` when candidate production is owned by BDP.

When a STOP or Intent Gap is automatable with existing architecture, OMP must automatically produce a STOP-derived or Intent-Gap-derived input package for the existing BDP route.

The package must include:

| Field | Required value |
| --- | --- |
| Origin ID / decision ID | Existing OMP stop, intent gap, chain, mission, behavior, verification, certification, state transition, or implementation identifier. |
| Origin Type | `STOP`, `INTENT_GAP`, `BEHAVIOR_GAP`, `STATE_TRANSITION_GAP`, `EXECUTION_GAP`, `VERIFICATION_GAP`, `CERTIFICATION_GAP`, or `IMPLEMENTATION_GAP`. |
| STOP Classification | Result of STOP Classification, or `NOT_APPLICABLE_NO_STOP`. |
| Intent Gap Classification | Result of Intent Gap Classification, or `NOT_APPLICABLE_WITH_REASON`. |
| Responsibility failure class | Intent Responsibility Resolution failure class, or `UNKNOWN_WITH_REASON`. |
| Last responsible link | `last_responsible_link` record. |
| Responsible owner | Owner responsible for the failed contract field. |
| Failed contract field | Producer, Output, Consumer, Consumption, Behavior Change, Next Output, State Transition, Legal Terminal Consumer, Verification, Rollback, Runtime, Production, Authority, Real World, or Architecture field. |
| Failed chain segment | Exact Engineering Chain segment that failed. |
| Expected owner behavior | Owner behavior required by the contract. |
| Observed owner behavior | Behavior observed in evidence. |
| Missing evidence | Missing evidence or `NONE`. |
| Smallest existing next action | Smallest existing next action to resolve or prove boundary. |
| Root Cause | Root Cause Engine output. |
| Human Intervention Detection | Whether the manual step is legitimate or automatable. |
| Existing owner | Owner that can express or consume the fix. |
| Affected Behaviour / Engineering Chain | Existing chain segment or `UNKNOWN_WITH_REASON`. |
| Current state | Current observed state. |
| Expected state | Desired state after automation removal. |
| Verification context | Existing verification owner/path. |
| Authority context | Existing authority boundary. |
| Rollback / STOP_SAFE context | Existing rollback, containment, no-change path, or STOP_SAFE. |
| Runtime / Production boundary | Existing boundary or `NOT_APPLICABLE_WITH_REASON`. |
| Candidate production route | Existing BDP route that may produce Candidate Instance. |

BDP must not receive only a generic `Automation Gap` when OMP can determine a concrete responsibility failure class.

If responsibility can be resolved, OMP must specialize the BDP input by failure class and last responsible link.

If responsibility cannot be resolved, OMP must record `UNKNOWN_WITH_REASON` with missing owner/evidence and smallest existing next action before any BDP routing.

BDP may then produce:

- `Implementation Candidate Instance`;
- hold reason;
- rejection reason;
- not-applicable result;
- legal terminal alternative.

OMP consumes the resulting Candidate Instance only through existing OMP identity, eligibility, admission, sequencing, Mission, verification, report, and certification rules.

#### Engineering Intent Closure Validation

After any STOP-derived or Intent-Gap-derived `Implementation Candidate Instance` reaches Mission, Implementation, Verification, and Execution Certification, OMP must automatically validate whether the original Engineering Intent was actually achieved.

This is not a new Intent Engine or Validation Engine.

Engineering Intent Closure Validation reuses:

- Engineering Intent from the Candidate Instance;
- original STOP record;
- Intent Gap Detection result when no STOP existed;
- Root Cause Engine output;
- Expected State from the STOP-derived or Intent-Gap-derived input package;
- Current State from existing owners / CPS;
- Behavior Enforcement Framework;
- State Transition Verification;
- Execution Certification;
- Engineering Chain evidence;
- Legal Terminal Consumer verification.

Validation questions:

| Question | Required answer |
| --- | --- |
| Did the original STOP disappear? | `YES`, `NO`, `UNKNOWN`, or `NOT_APPLICABLE_WITH_REASON`. |
| Was the original Engineering Intent achieved? | `YES`, `NO`, `PARTIAL`, `UNKNOWN`, or `NOT_APPLICABLE_WITH_REASON`. |
| Was Expected State reached? | `YES`, `NO`, `PARTIAL`, `UNKNOWN`, or `NOT_APPLICABLE_WITH_REASON`. |
| Does Current State match Expected State? | `YES`, `NO`, `PARTIAL`, `UNKNOWN`, or `NOT_APPLICABLE_WITH_REASON`. |
| Does the same STOP still exist? | `YES`, `NO`, `UNKNOWN`, or `NOT_APPLICABLE_WITH_REASON`. |
| Does the same Intent Gap still exist? | `YES`, `NO`, `UNKNOWN`, or `NOT_APPLICABLE_WITH_REASON`. |
| Did the Engineering Chain reach Legal Terminal Consumer? | `YES`, `NO`, `PARTIAL`, `UNKNOWN`, or `NOT_APPLICABLE_WITH_REASON`. |
| Was Behavior Chain Status `COMPLETE` or legal terminal consumer verification `PASS`? | `YES`, `NO`, `PARTIAL`, `UNKNOWN`, or `NOT_APPLICABLE_WITH_REASON`. |

Allowed validation results:

| Result | Meaning | Next action |
| --- | --- | --- |
| `INTENT_CLOSED` | Engineering Intent is achieved, original STOP / Intent Gap disappeared, Expected State matches Current State, Engineering Chain reached Legal Terminal Consumer, and Automation Gap is closed. | Continue OMP. |
| `INTENT_NOT_CLOSED` | Engineering Intent is not achieved, same STOP / Intent Gap still exists, Expected State does not match Current State, or Engineering Chain still breaks. | Automatically rerun Automation Gap Closure Cycle. |
| `FUNDAMENTAL_ARCHITECTURE_BOUNDARY` | Closure cannot be expressed through existing owners after proof. | Stop with fundamental boundary proof. |

STOP absence or STOP disappearance alone is not sufficient.

Automation Gap is closed only when Engineering Intent is closed.

If STOP disappears, never existed, or formal execution passes but the Engineering Intent remains unmet, OMP must classify:

```text
INTENT_NOT_CLOSED
```

and automatically rerun:

```text
STOP or unresolved Engineering Intent
  -> Automation Gap Closure
  -> BDP
  -> OMP
  -> Mission
  -> Implementation
  -> Verification
  -> Execution Certification
  -> Engineering Intent Closure Validation
```

The cycle repeats until:

- `INTENT_CLOSED`; or
- `FUNDAMENTAL_ARCHITECTURE_BOUNDARY`.

No other final state is allowed for a STOP-derived automation gap.

#### Fundamental Boundary Confirmation

If automation is impossible, OMP must prove all of the following before recording a fundamental boundary:

- no existing owner can express the behavior;
- no existing capability can be extended;
- no existing Mission path can execute it safely;
- no existing verification path can prove it;
- no existing authority model can authorize it;
- no existing rollback / STOP_SAFE / containment path can protect it;
- no existing Runtime boundary can represent it;
- no existing Engineering Chain can consume it;
- no existing BDP route can produce a valid Candidate Instance.

Only after this proof may OMP record:

```text
FUNDAMENTAL_ARCHITECTURE_GAP
```

#### Completion Criteria

Automation Gap Closure for a STOP or Intent Gap is complete only when it has one of these terminal states:

| Terminal state | Meaning |
| --- | --- |
| `INTENT_CLOSED` | Original Engineering Intent is achieved, original STOP / Intent Gap is gone, Current State matches Expected State, and Legal Terminal Consumer is verified. |
| `FUNDAMENTAL_ARCHITECTURE_BOUNDARY` | Fundamental boundary proof is recorded. |

No third permanent state is allowed.

`STOP_DERIVED_BDP_INPUT_ROUTED`, `IMPLEMENTATION_CANDIDATE_CONSUMED`, and `INTENT_NOT_CLOSED` are intermediate states, not final closure.

`AUTOMATION_GAP_CLOSURE_BLOCKED_WITH_REASON` is temporary and must name the missing owner/evidence and smallest existing next action.

#### Continuous Mode

Automation Gap Closure Cycle runs after every new STOP and every detected unfinished Engineering Intent.

The goal is not statistics, learning, or new feature discovery.

The goal is to remove every non-fundamental manual engineering action that can be replaced by the existing architecture.

OMP must continue to use the ordinary route:

```text
STOP-derived or Intent-Gap-derived input
  -> BDP candidate production
  -> OMP candidate consumption
  -> Mission Admission
  -> Execution / Hold / Rejection / Not Applicable
  -> Verification
  -> Execution Certification
  -> Engineering Intent Closure Validation
  -> Engineering Report
  -> Certification
```

Current Program State storage:

`docs/programs/V7_CURRENT_PROGRAM_STATE.md` must store:

- `root_cause`;
- `responsible_owner`;
- `authority_class`;
- `authority_reason`;
- `authority_owner`;
- `required_action`;
- `intent_gap_detection_status`;
- `intent_gap_classification`;
- `intent_responsibility_resolution_status`;
- `responsibility_failure_class`;
- `last_responsible_link`;
- `failed_contract_field`;
- `expected_owner_behavior`;
- `observed_owner_behavior`;
- `missing_evidence`;
- `smallest_existing_next_action`;
- `bdp_input_specialization`;
- `automation_gap_closure_status`;
- `engineering_intent_closure_status`;
- `original_stop_resolved`;
- `expected_state_reached`;
- `current_state_matches_expected_state`;
- `human_intervention_classification`;
- `bdp_stop_input_route`;
- `approved_future_dependency_protection_status`;
- `protected_future_dependency_object`;
- `approved_future_plan`;
- `future_dependency_owner`;
- `future_dependency_type`;
- `future_dependency_state`;
- `future_dependency_terminal_condition`;
- `engineering_work_in_progress_protection_status`;
- `protected_engineering_object`;
- `unfinished_engineering_lifecycle`;
- `engineering_lifecycle_owner`;
- `engineering_lifecycle_state`;
- `engineering_wip_terminal_condition`;
- `capability_maturity_protection_status`;
- `protected_capability`;
- `protected_element`;
- `capability_maturity_status`;
- `capability_mapping_status`;
- `capability_completion_required_before_minimization`;
- `necessity_framework_consumption_status`;
- `existence_justification`;
- `semantic_necessity`;
- `consumer_value`;
- `system_effect`;
- `state_transition_contribution`;
- `production_value`;
- `creation_test`;
- `removal_test`;
- `merge_test`;
- `chain_test`;
- `necessity_verdict`;
- `necessity_certification_state`;
- `implementation_class`;
- `next_engineering_task`;
- `expected_completion_evidence`.

Continuation rule:

| Classification | Automatic Continuation |
| --- | --- |
| `BUG` | Continue after implementation, tests, deployment if required, truth, and convergence. |
| `OWNER_EXTENSION` | Continue if extension stays inside existing owner boundaries and does not require authority expansion. |
| `CONFIGURATION` | Continue if read-only or safe configuration update is authorized by existing policy. |
| `CERTIFICATION` | Continue until real evidence, authority, or unsafe implementation boundary is reached. |
| `REAL_WORLD_LIMIT` | Stop with exact required production evidence. |
| `AUTHORITY` with `OPERATIONAL_AUTHORITY` | Stop with exact approve/reject command for the current production action. |
| `AUTHORITY` with `ENGINEERING_AUTHORITY` | Stop with exact engineering approval or authority expansion decision. |
| `DOCUMENTATION` | Continue if documentation is the active backlog item and no runtime mutation occurs. |

## 11. Implementation Optimization Target Rule

The current target is no longer `Current Phase` and no longer `Architectural Completeness`.

The current optimization target is:

`Highest Production Leverage per unit risk`

OMP must rank potential targets across:

- runtime implementation;
- background implementation;
- read-model improvements;
- verification;
- observability;
- testing;
- UI;
- documentation required by implementation;
- certification.

Current optimization target is a rule. The live target value is resolved from `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

Historical optimization snapshot:

| Field | Current Value |
| --- | --- |
| Optimization target | Current HIL in `docs/programs/V7_CURRENT_PROGRAM_STATE.md` |
| Target class | Volatile current state |
| Gain type | Determined by OMP after reading Current Program State |
| Risk | Determined by current packet, implementation task, normalized authority class, and stop condition |
| Effort | Determined by current OMP recalculation |
| Authority | Stop at `OPERATIONAL_AUTHORITY` before exact restore-barrier write, apply, user movement, rollback apply, or production action; stop at `ENGINEERING_AUTHORITY` before daemon/timer, event consumer mutation, runtime capability, autonomous policy, blast-radius, action-class, or authority expansion |
| Safe automatic portion | Continue only through work that remains inside existing owners and does not cross the current stop boundary |

Latest optimization iteration `2026-06-25`:

| Field | Current Value |
| --- | --- |
| Recalculation source | Production `v7-autonomy-trust-evidence-inventory` after service/quality/snapshot refresh. |
| Challenged action | `Governed candidate suitability outcome closure`. |
| Best lower-risk challenger | `Service verification and quality snapshot refresh`. |
| Safe portion executed | `v7-egress-quality-compact`, `v7-service-matrix-refresh-all`, `v7-intelligence-snapshot-refresh`. |
| Runtime apply | `FALSE` |
| Users moved | `0` |
| New owner created | `FALSE` |
| New planner/governance/execution/truth | `FALSE` |
| Post-refresh maturity score | `84.167` |
| Post-refresh largest floor gap | `Suitability`: current `29.11`, gap `40.89` to floor `70`. |
| Post-refresh candidate gap | `72` missing candidate outcomes, coverage ratio `0.5385`. |
| Post-refresh dry-run verdict | `AUTONOMOUS_DRY_RUN_CYCLE_REACHES_AUTHORITY_BOUNDARY`; normalized OMP stop `OPERATIONAL_AUTHORITY`. |
| Post-refresh packet state | Packet preview ready; restore/rollback preview ready; verification plan ready; outcome closure plan ready; learning path connected. |
| Optimizer conclusion | Safe challenger completed; final HLA remains governed candidate suitability outcome closure and stops at `OPERATIONAL_AUTHORITY`. |

## 12. Architecture Health

Maintain continuously:

| Metric | Current Value | Evidence |
| --- | --- | --- |
| Architecture Completeness | `100% fundamental / future optional extensions remain` | Final architecture certification reports no fundamental missing classes. |
| Knowledge Completeness | `PARTIAL_FOR_AUTONOMY` | Knowledge objects exist; real outcome depth remains insufficient. |
| Reuse Ratio | `100%` | Current OMP V2.1 upgrade reuses existing OMP/reference owners and creates no new owner. |
| Extension Ratio | `100%` | Current capability is delivered by extending existing documents in place. |
| Duplicate Ratio | `0% known introduced` | Duplication detector verdict is `NONE`. |
| Automation Ratio | `84.167%` | Autonomous knowledge growth program maturity score. |
| Authority Ratio | `OPERATIONAL_AUTHORITY_REACHED / NOT_EXPANDED` | Governed dry-run reaches exact packet approval boundary; no apply authority granted. |
| Operational Maturity | `OPTIMIZATION_ACTIVE` | OMP now drives bottleneck optimization rather than fixed phases. |

## 13. Self-Improvement Loop

Every implementation must follow:

```text
Read Kernel
  -> Read OMP
  -> Read Current Program State
  -> Determine highest implementation leverage
  -> Semantic Reuse Audit
  -> Reuse
  -> Extend
  -> Implement
  -> Deploy
  -> Truth
  -> Convergence
  -> Certification
  -> Update Current Program State
  -> Update OMP
  -> Authority Evaluation
  -> Continue
```

No future prompt may bypass OMP. OMP always wins over free-form implementation ideas.

## 14. Automatic Continuation Rule

Codex must continue automatically while the highest leverage action does not require external input. Runtime apply, restore-barrier write, or one-user movement already admitted by an active approved delegated policy are not program terminals. Actions outside policy, authority or blast-radius expansion, missing real-world evidence, fundamental architecture boundaries, unresolved external access/security boundaries, and irreducible non-determinism remain program terminals.

Codex must continue automatically through:

1. docs/reference updates;
2. ADR updates;
3. read-only verification;
4. truth/convergence checks;
5. inventory refresh;
6. quality/service/snapshot refresh;
7. existing-owner implementation;
8. tests;
9. duplication detection;
10. OMP recalculation;
11. packet preview refresh;
12. restore/rollback preview verification;
13. outcome closure plan verification;
14. learning path verification.

Codex must stop only at a proven `PROGRAM_TERMINAL`: `OPERATIONAL_AUTHORITY` for an action outside active policy, `ENGINEERING_AUTHORITY`, `REAL_WORLD_LIMIT`, `FUNDAMENTAL_ARCHITECTURE_BOUNDARY`, unresolved external security/access input, or irreducible `NON_DETERMINISTIC_DECISION`. `STOP_SAFE`, `ROLLBACK_SUCCESS`, `NO_EXECUTION`, safe verification failure, recoverable `BUG`/`OWNER_EXTENSION`, route-integrity failure, packet invalidation, and freshness/binding mismatch are `TRANSACTION_TERMINAL` and must automatically continue through Root Cause Engine and Automation Gap Closure.

Before stopping, Codex must run the Root Cause Engine and expose the structured stop record as the primary output.

If the highest leverage action crosses an authority gate, Codex must:

1. stop before the boundary;
2. update this OMP;
3. normalize the boundary into `OPERATIONAL_AUTHORITY` or `ENGINEERING_AUTHORITY`;
4. report root cause, responsible owner, expected evidence, and exact next action;
5. wait for explicit operator authority for the exact action or engineering approval.

Production program loop for every future task:

```text
READ KERNEL
  -> READ OMP
  -> READ CURRENT PROGRAM STATE
  -> DETERMINE HIGHEST IMPLEMENTATION LEVERAGE
  -> SEMANTIC REUSE AUDIT
  -> REUSE
  -> EXTEND
  -> IMPLEMENT
  -> DEPLOY
  -> TRUTH
  -> CONVERGENCE
  -> CERTIFICATION
  -> UPDATE CURRENT PROGRAM STATE
  -> UPDATE OMP
  -> AUTHORITY EVALUATION
  -> CONTINUE
```

This replaces phase-first and roadmap-first thinking with optimization-first thinking.

### 14.1 OMP Self-Continuation Contract

Status: `CANONICAL_EXECUTABLE_CONSUMER_CONTRACT`

Execution consumer: existing Codex OMP consumer governed by OMP, ECR and CPS. `admin_core/operator_execution_pipeline.py` remains a transaction owner and must not become a Mission scheduler. No daemon, queue, hidden retry worker, second Planner, or parallel executor is created.

```text
Mission terminal
  -> classify TRANSACTION_TERMINAL or PROGRAM_TERMINAL
  -> rollback/containment and mandatory final Safe Mode OPEN
  -> outcome/learning/maturity
  -> Engineering Report
  -> atomic CPS update
  -> read fresh CURRENT_NEXT_ACTION_ID
  -> reconcile unfinished capability registry and dependency graph
  -> classify WAITING and propagate BLOCKED_BY_DEPENDENCY
  -> calculate READY execution frontier
  -> Root Cause Engine / Automation Gap Closure when intent remains open
  -> form and admit next Mission
  -> execute next Mission
  -> repeat until PROGRAM_TERMINAL
```

Transaction terminal classes are `STOP_SAFE`, `ROLLBACK_SUCCESS`, `NO_EXECUTION`, safe verification failure, recoverable `BUG`, recoverable `OWNER_EXTENSION`, route-integrity failure, packet invalidation, and freshness/binding mismatch. They close only the current transaction and cannot return control to the operator when an existing-owner next action remains executable.

Program terminal classes are `ENGINEERING_AUTHORITY`, `OPERATIONAL_AUTHORITY_OUTSIDE_ACTIVE_POLICY`, `REAL_WORLD_LIMIT`, `FUNDAMENTAL_ARCHITECTURE_BOUNDARY`, unresolved external `SECURITY_OR_ACCESS_INPUT`, and irreducible `NON_DETERMINISTIC_DECISION`. They return control exactly once with the precise external input required.

`REAL_WORLD_LIMIT` and other external boundaries are capability-local while another independent READY capability exists. `WAITING_EXTERNAL_DEPENDENCY` is not a program terminal by itself. OMP may continue only through READY capabilities whose required dependencies are `COMPLETED`; dependents remain `BLOCKED_BY_DEPENDENCY`.

Dependency-aware continuation algorithm:

```text
load CPS capability graph
  -> remove COMPLETED from executable work
  -> preserve WAITING with owner/evidence/fingerprint/reentry
  -> propagate BLOCKED_BY_DEPENDENCY
  -> compute deterministic READY frontier
  -> execute first READY capability through existing owners
  -> validate completion order
  -> update CPS and recalculate
  -> stop only when READY frontier is empty and a proven program boundary remains
```

Canonical dependency states are `READY`, `WAITING_EXTERNAL_DEPENDENCY`, `BLOCKED_BY_DEPENDENCY`, `EXECUTING`, `COMPLETED`, `FAILED_REQUIRES_REPAIR`, and `BLOCKED_AUTHORITY`. Historical snapshots cannot contribute graph state. A WAITING capability must define a reentry condition and cannot create a Candidate, packet, Authority request or mutation.

Completion is legal only when:

```text
ALL_DEPENDENCIES_COMPLETED
AND INTENT_CLOSED
AND CONSUMER_VERIFIED
AND EVIDENCE_CONSUMED
AND CPS_UPDATED
```

Required fail-closed results are `DEPENDENCY_NOT_COMPLETED`, `COMPLETION_ORDER_VIOLATION`, `INTENT_CHAIN_INCOMPLETE`, `CONSUMER_MISSING`, and `EVIDENCE_NOT_CONSUMED`.

Required CPS machine fields:

```text
OMP_CONTINUATION_REQUIRED
EXTERNAL_INPUT_REQUIRED
EXTERNAL_INPUT_TYPE
TRANSACTION_TERMINAL_CLASS
PROGRAM_TERMINAL_CLASS
NEXT_MISSION_FORMED
NEXT_MISSION_ID
PREMATURE_OPERATOR_RETURN
CONTINUATION_ITERATION
CONTINUATION_STOP_REASON
NO_PROGRESS_FINGERPRINT
DEPENDENCY_GRAPH_VERSION
CURRENT_EXECUTION_FRONTIER
WAITING_CAPABILITIES
READY_CAPABILITIES
BLOCKED_CAPABILITIES
CONTINUATION_DECISION
NEXT_EXECUTABLE_CAPABILITY
PROGRAM_TERMINAL_STATE
```

Fail-closed law:

```text
CURRENT_NEXT_ACTION_ID = CONTINUE_OMP
AND EXTERNAL_INPUT_REQUIRED = FALSE
AND OMP_CONTINUATION_REQUIRED != TRUE
=> PREMATURE_OMP_RETURN_TO_OPERATOR
```

A verdict containing `CONTINUE_OMP_READY` is intermediate when `EXTERNAL_INPUT_REQUIRED=FALSE`. The consumer must form the next Mission in the same invocation. Terminal packet, Candidate, decision, operation, lease and binding identities are never reused.

No-progress protection reuses Mission identity, anti-replay, Decision Reproducibility, Root Cause Engine, Intent Responsibility Resolution and Automation Gap Closure. The deterministic fingerprint is computed from stop, responsible owner, Current State, Expected State and next action. Repeated fingerprints trigger owner-backed root-cause work, never blind production mutation retry or an operator `Continue OMP` retry request.

## 15. OMP Execution Contract For Codex

Codex must not ask:

```text
what phase should I execute?
```

Codex must:

1. read OMP;
2. recalculate current bottleneck;
3. find safe automatic portion;
4. execute safe portion through existing owners;
5. deploy completed and tested changes when project policy requires deployment;
6. run truth and convergence;
7. certify;
8. update Current Program State;
9. update OMP, reference, system map, or ADR if meaning changed;
10. evaluate authority;
11. recalculate;
12. continue;
13. stop only at an allowed stop condition.

If blocked by any allowed stop condition, Codex must output the Root Cause Engine record first:

- root cause;
- responsible owner;
- exact module and function when known;
- why it happened;
- why existing safety worked;
- whether the existing owner can be extended;
- Need New Owner verdict;
- implementation class;
- concrete engineering task;
- expected completion evidence;
- whether OMP can continue automatically after completion.

If blocked by `OPERATIONAL_AUTHORITY`, Codex must also output:

- exact packet;
- exact action;
- exact user;
- exact source;
- exact target;
- exact rollback target;
- exact command shape that must not run without approval;
- exact approval question.

If blocked by `ENGINEERING_AUTHORITY`, Codex must also output:

- exact authority expansion, action class, runtime capability, autonomous policy, or blast-radius change;
- owner requesting the approval;
- why engineering cannot continue without it;
- what remains unchanged if approval is rejected;
- exact approve/reject question.

This contract is constrained by Safety-Bounded Authority:

```text
Trust decides autonomy tier.
Safety decides bounded action.
```

Permanent operator command surface:

| Command | Meaning |
| --- | --- |
| `Continue OMP` | Execute the complete Engineering Control Loop: ECR -> Knowledge Plane -> re-open evaluation -> OMP execution -> implementation/audit/certification/verification -> Engineering Report -> knowledge promotion -> Current Program State/OMP update -> next highest-leverage action, until an allowed stop condition. |
| `Status` | Print the current `V7 PRODUCTION STATUS` block without changing runtime state. |
| `Approve authority expansion` | Approve a specific authority expansion only after OMP recommends it from certified evidence. |

These commands are sufficient for future production operation unless a real implementation proves `FUNDAMENTAL_ARCHITECTURE_GAP`.

## 16. Historical Program Health Snapshot

Classification: `HISTORICAL_SNAPSHOT`.
Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

| Health Dimension | Current Value | Notes |
| --- | --- | --- |
| Architecture completeness | `COMPLETE` | Fundamental architecture exists; future extensions remain optional/scale-related. |
| Knowledge completeness | `PARTIAL_FOR_AUTONOMY` | Knowledge objects exist but real outcome depth is insufficient for autonomy-grade suitability. |
| Cycle automation % | `84.167` | Autonomous knowledge growth program certified 12 cycles and maturity score `84.167`. |
| Authority maturity | `OPERATIONAL_AUTHORITY_REACHED` | Safe preparation reaches production action approval; apply authority is not granted. |
| Operational maturity | `OPTIMIZATION_ACTIVE` | OMP now optimizes bottleneck reduction rather than executing a fixed roadmap. |
| Remaining architecture uncertainty | `NONE_FUNDAMENTAL` | Partial classes are future/scale/authority extensions, not missing architecture. |
| Current optimization velocity | `OPERATIONAL_AUTHORITY_AFTER_SAFE_REFRESH` | Safe service/quality/snapshot refresh completed through existing owners; real candidate outcome gain needs exact packet approval. |

## 17. Historical Phase Anchor

Classification: `HISTORICAL_SNAPSHOT`.
Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

`GOVERNED_CANDIDATE_OUTCOME_EXECUTION_AND_CLOSURE`

Source:

- `docs/reports/V7_FINAL_AUTONOMOUS_ROUTING_ARCHITECTURE_CERTIFICATION_REPORT.md`
- `docs/reports/V7_GOVERNED_CANARY_KNOWLEDGE_GATED_AUTONOMOUS_DRY_RUN_CYCLE_REPORT.md`
- `docs/reference/SYSTEM_MAP.md`

Reason:

The final architecture certification says V7 has no fundamental architecture gap. The governed dry-run reaches `OPERATIONAL_AUTHORITY` with packet preview, restore/rollback preview, verification plan, outcome closure plan, and learning path connected. The next maturity gain requires real governed candidate outcome evidence.

## 18. Historical Objective

Classification: `HISTORICAL_SNAPSHOT`.
Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

Use existing owners to create and close one real governed candidate outcome only after explicit operator authority.

The phase must:

1. reuse the existing planner;
2. reuse the existing governed packet owner;
3. reuse the existing restore barrier;
4. reuse the existing rollback preview;
5. reuse the existing verification plan;
6. reuse the existing feedback/outcome closure owner;
7. reuse the existing learning refresh owner;
8. re-evaluate confidence, trust, prediction, and suitability after outcome closure.

No autonomous apply is approved by this program state.

## 19. Success Criteria

| Criterion | Required State |
| --- | --- |
| Exact packet authority | Explicit operator approval exists for the exact packet before any restore-barrier write or apply. |
| Runtime safety | No movement occurs before authority; no hidden daemon or timer apply is enabled. |
| Existing owners | Planner, packet, restore barrier, rollback, feedback, learning, and truth/convergence owners are reused. |
| Real outcome | The candidate outcome is observed after a real governed/manual action, not synthesized. |
| Closure | Outcome, verification, rollback/no-rollback decision, feedback, and learning are recorded through existing paths. |
| Certification | Tests, `tools/v7-truth-check --all --json`, and `tools/v7-convergence-status --json` pass after the phase. |
| Documentation | Canonical reference, system map, ADRs, and this program are updated when meaning changes. |

## 20. Stop Conditions

Classification: `PERMANENT_RULE`.

Only these stop conditions are allowed:

1. `OPERATIONAL_AUTHORITY`
2. `ENGINEERING_AUTHORITY`
3. `REAL_WORLD_LIMIT`
4. `UNSAFE_IMPLEMENTATION`
5. `FUNDAMENTAL_ARCHITECTURE_GAP`

Legacy raw `AUTHORITY_BOUNDARY` may appear in older reports or compatibility tool output, but OMP must normalize it before presenting status.

### 20.1 Historical Stop Conditions Snapshot

Classification: `HISTORICAL_SNAPSHOT`.
Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

Historical blocker:

`UNSAFE_IMPLEMENTATION`

Historical details:

- approval-to-execution lease binding is fixed, tested, deployed, and verified;
- operator approved exact packet `pkt_preview_4eb137c926917c2761faadb4`;
- selected move hash is `e1e09d2c95fc6c9b0b77e9ecaaf0def20e9759150eb35db8d70f95e107eb52cd`;
- user is `10.7.0.17`, move is `vless -> awg0`;
- restore-barrier clearance was written through the existing owner;
- guarded apply failed closed before movement because the existing autoswitch owner lost the approved selected move at the intelligence snapshot gate;
- no additional operator approval is useful until this owner defect is fixed;
- no new owner is required.

### 20.2 Current Stop Reference

Classification: `CURRENT_PROGRAM_STATE_REFERENCE`.
Authoritative owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `CPS_ONLY`
Execution Authority: `NONE`
Resolved current stop: `EXTERNAL_OWNER_REQUIRED`
Resolved current next action: `WAITING_INPUT:STAGE_48_EXISTING_OWNER_ADMISSION`
Resolved contract state: CPS proves immutable performance receipt `perfclose_1f91af0c6253c6fe75e028c5`, fastest-safe-path production consumption and `STAGE_48_OPTIMIZED_RUNTIME_READY_NOT_EXECUTED`. Stage 48 is not a formed Mission and cannot start until a separate existing-owner admission is consumed. This pointer grants no Authority or mutation.

These values are validated against CPS section 0. This subsection is a pointer projection and cannot independently select a Mission, Candidate, packet, Authority, stop, or next action.

## 21. Phase History

| Phase | Certified Result | State | Evidence |
| --- | --- | --- | --- |
| Canonical Reference Base | Reference and ADR system created | `COMPLETED` | `docs/reference/V7_CANONICAL_REFERENCE.md`, `docs/reference/SYSTEM_MAP.md` |
| Reference First Rule | Future audits must read reference before re-auditing | `COMPLETED` | `docs/decisions/ADR-005-reference-first-rule.md` |
| Event-Driven Autonomy Contract | Timer-only movement rejected; event-driven model accepted | `COMPLETED` | `docs/decisions/ADR-EVENT-DRIVEN-AUTONOMY.md`, `docs/reports/POOL.3_RUNTIME_DISCOVER.md` |
| Knowledge Quality Model | Data/signal/knowledge/action authority separated | `COMPLETED` | `docs/reference/V7_KNOWLEDGE_QUALITY_MODEL.md` |
| Autonomous Routing Foundation | Fit, outcome, recovery, anti-flap, freshness models exposed read-only | `COMPLETED` | `docs/reports/V7_AUTONOMOUS_ROUTING_FIT_OUTCOME_RECOVERY_FOUNDATION_REPORT.md` |
| Knowledge To Decision Integration | Routing knowledge can influence read-only decisions without apply | `COMPLETED` | `docs/reports/V7_KNOWLEDGE_TO_DECISION_INTEGRATION_REPORT.md` |
| Decision To Outcome To Learning Integration | Outcome quality and learning path connected | `COMPLETED` | `docs/reports/V7_DECISION_TO_OUTCOME_TO_LEARNING_INTEGRATION_REPORT.md` |
| Highest Leverage Outcome Growth | Verdict `MIXED_PATH`; suitability needs real candidate outcomes | `COMPLETED` | `docs/reports/V7_HIGHEST_LEVERAGE_OUTCOME_GROWTH_REPORT.md` |
| Autonomy-Grade Suitability Program | Suitability growth requires real candidate outcome closure | `COMPLETED` | `docs/reports/V7_AUTONOMY_GRADE_SUITABILITY_PROGRAM_REPORT.md` |
| Autonomous Knowledge Growth Program | 12 cycles verified; maturity score `84.167`; boundary remains authority | `COMPLETED` | `docs/reports/V7_AUTONOMOUS_KNOWLEDGE_GROWTH_PROGRAM_REPORT.md` |
| Autonomous Routing Evolution Program | TIER_2 remains blocked by confidence/trust/prediction/suitability and real outcomes | `COMPLETED` | `docs/reports/V7_AUTONOMOUS_ROUTING_EVOLUTION_PROGRAM_REPORT.md` |
| Maximum Reality Knowledge Extraction | `72` candidate outcomes are not hidden; they require governed/manual action | `COMPLETED` | `docs/reports/V7_MAXIMUM_REALITY_KNOWLEDGE_EXTRACTION_REPORT.md` |
| Final Autonomous Routing Architecture Certification | Superseded by final system synthesis: `ARCHITECTURE_COMPLETE`; optional improvements remain non-blocking | `CERTIFIED` | `docs/reports/V7_FINAL_AUTONOMOUS_ROUTING_ARCHITECTURE_CERTIFICATION_REPORT.md`, `docs/reference/V7_SYSTEM_ARCHITECTURE.md`, `docs/decisions/ADR-V7-SYSTEM-ARCHITECTURE.md` |
| Governed Canary Knowledge-Gated Dry-Run Cycle | Production reaches legacy dry-run boundary; normalized OMP stop `OPERATIONAL_AUTHORITY`; no apply, no movement | `CERTIFIED` | `docs/reports/V7_GOVERNED_CANARY_KNOWLEDGE_GATED_AUTONOMOUS_DRY_RUN_CYCLE_REPORT.md` |
| Runtime Latency Foundation | RT1-RT8 complete: Runtime Time Architecture, Reaction Latency, Thin Runtime Path Contract, live/precompute matrix, Engineering Report Latency Impact, Phase 2 Automation-Time Contract, Runtime Latency Engineering Review Checklist, and complete Phase 2 Automation Contract embedded through existing owners | `COMPLETED` | `docs/reference/V7_RUNTIME_MODEL.md`, `docs/reports/engineering/2026-06-28_003325_rt_phase1_runtime_latency_foundation.md`, `docs/reports/engineering/2026-06-28_004129_rt_phase1_extension_rt7_rt8.md` |

## 22. Historical Next Best Action Snapshot

Classification: `HISTORICAL_SNAPSHOT`.

Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

Live next best action is resolved only from `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

`IMPLEMENT_READ_ONLY_RUNTIME_LIFECYCLE_PREVIEW`

Program interpretation:

This is the first implementation-phase coding task. It is not research, architecture, planning, governance redesign, execution redesign, runtime redesign, apply, daemon work, timer work, or user movement.

The task implements production leverage by exposing the completed Runtime Model through the existing governed dry-run owner.

Safe automatic target:

```text
implement read-only Runtime lifecycle preview
  -> reuse governed_canary_knowledge_gated_dry_run_cycle
  -> emit lifecycle, stage, stop, idempotency, duplicate, loop, verification, rollback, learning, and OMP-notification status
  -> add focused tests
  -> verify no apply, no user movement, no runtime mutation
  -> run truth
  -> run convergence
  -> update Current Program State and OMP
```

The implementation target is:

```text
admin_core/operator_execution_pipeline.py
  -> governed_canary_knowledge_gated_dry_run_cycle
  -> tools/v7-governed-canary-dry-run-cycle
  -> focused governed dry-run lifecycle tests
```

If an exact restore-barrier write, apply, user movement, rollback apply, or production action is required, stop at `OPERATIONAL_AUTHORITY`.

If daemon, timer, event consumer mutation, autonomous execution, action-class expansion, blast-radius expansion, runtime capability expansion, autonomous policy approval, or authority expansion is required, stop at `ENGINEERING_AUTHORITY`.

## 23. Historical Next Best Action Entry Criteria

Classification: `HISTORICAL_SNAPSHOT`.

Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

These entry criteria are preserved as historical evidence for the corresponding snapshot. Live entry criteria must be taken from CPS, an admitted Mission, or the current owner-backed OMP decision.

| Entry Criterion | Required |
| --- | --- |
| Existing owner | Reuse `governed_canary_knowledge_gated_dry_run_cycle`; do not create a duplicate runtime owner. |
| Scope | Read-only lifecycle preview only. |
| Runtime model | Emit fields that map to `V7_RUNTIME_MODEL.md` lifecycle, state, stop, restart, duplicate, loop, idempotency, verification, rollback, learning, and OMP-notification semantics. |
| Apply path | Forbidden. No restore-barrier write, apply, rollback apply, or user movement. |
| Operational authority | Exact packet, rollback, restore-barrier, apply, or production action approval stops at `OPERATIONAL_AUTHORITY`. |
| Engineering authority | Authority expansion, action-class expansion, autonomous policy, runtime capability, daemon/timer, event-consumer mutation, or blast-radius expansion approval stops at `ENGINEERING_AUTHORITY`. |
| Tests | Focused tests must prove the lifecycle output is read-only and idempotency-aware. |
| Safety | No daemon enablement, no timers, no event consumer mutation, no duplicate planner/governance/execution. |

## 24. Historical Program Certification Snapshot

Classification: `HISTORICAL_SNAPSHOT`.

Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

This table preserves a prior OMP certification/status view. Live certification and blocker values are resolved from CPS and the latest accepted owner evidence.

Historical field names preserve snapshot terminology only. Live volatile state must be read from CPS.

| Historical Field | Preserved Snapshot Value |
| --- | --- |
| Completed phases | Architecture foundation, Research Framework, Decision Model, Runtime Model, System Architecture, Implementation Phase activation, OMP Production Program integration. |
| Certified phases | Decision Model; Runtime Model; System Architecture; governed knowledge-gated dry-run cycle; OMP Production Program rule set. |
| Current bottleneck | Actionable implementation backlog is complete; future work requires explicit operator-approved scope and OMP admission. |
| Current highest leverage action | Stop actionable backlog execution; report status or wait for explicit operator-approved new scope. |
| Current reuse ratio | `100%`. |
| Current duplicate ratio | `0% known introduced`. |
| Current automation ratio | `84.167%`. |
| Current blockers | Actionable backlog is complete; Runtime apply, blast-radius expansion, authority expansion, threshold/formula mutation, automation, synthetic evidence, user movement, planner replacement, and new owner creation remain blocked without explicit future authority/scope. |
| Current maturity | Tier 0 `COMPLETE`; Tier 1 `ACTIVE`; Production Maturity `66.9%`; Tier A backlog `6 / 6`; Tier B backlog `21 / 21`; Tier C backlog `7 / 7`; overall backlog `34 / 34`. |
| Current runtime posture | No autonomous apply, no daemon enablement, no authority expansion; local validation moved `0` users and now stops explicitly with `runtime_state_unavailable` when local `/opt/v7` state is absent. |
| Current next best action | `IMPLEMENTATION_COMPLETE`; no runtime apply, no automation, no authority expansion, no blast-radius expansion, no threshold/formula mutation, no synthetic evidence, no user movement, no planner replacement, no new owner, no new backlog, no architecture change. |
| Last optimizer iteration | `2026-06-29`: RT2-S6 evidence-based continuous improvement implemented as read-only owner-mapped advisory recommendation; current result is `DONE_READ_ONLY_OWNER_MAPPED_RECOMMENDATION`; tests passed. |

## 24.1 Capability Transition Contract

Status: `ACTIVE_CANONICAL`.

Owner: OMP.

Purpose:

OMP must permanently explain not only what the next step is, but why that step is now available, which capability produced the unlocking evidence, which owner may consume it, and why later steps remain forbidden.

This contract is not a new lifecycle, roadmap, owner, planner, runtime, truth source, capability program, dashboard authority, automation mode, or implementation queue.

Transition audit:

| Item | Classification | Existing expression | Required extension |
| --- | --- | --- | --- |
| Execution order | `EXISTS_COMPLETE` | `A5 -> A6 -> B13 -> B16 -> Runtime Capability Maturation Program`. | None. |
| RT2 entry criteria | `EXISTS_COMPLETE` | Section 28.1 entry criteria. | None. |
| Workstream flow | `EXISTS_COMPLETE` | Section 28.3 workstream table and OMP engineering lifecycle. | None. |
| Transition explanation | `EXISTS_PARTIAL` | CPS and OMP state show the next step and produced evidence, but not a durable transition reason table. | Add this contract inside OMP. |
| Transition owner mapping | `EXISTS_PARTIAL` | SYSTEM_MAP maps owners but not transition ownership as a first-class lookup. | Add SYSTEM_MAP transition row. |
| Durable transition rule | `EXISTS_PARTIAL` | Canonical Reference preserves execution order and current state. | Add durable rule that reports must not be the only transition explanation. |

Transition rule:

1. A step becomes available only when the previous step produced real or read-only certified evidence accepted by its canonical owner.
2. A step may consume only the evidence named for that transition.
3. Unlocking a step never unlocks later steps by implication.
4. Runtime apply, automation, authority expansion, user movement, dashboard authority, synthetic evidence, and new ownership remain forbidden unless the specific transition explicitly produces certified authority for them.
5. If the next step cannot explain current capability, produced evidence, consumed evidence, unlocked capability, blocked capability, and safety reason, OMP must stop and extend this contract before continuing.

Major capability transitions:

| From step | Current capability | Produced evidence | Consumed evidence | Unlocked capability | Still blocked capability | Why next step is available | Why later steps remain forbidden |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `A5` -> `A6` | Blast-radius certification. | Class-level blast-radius evidence beyond one-user guard; historical E29 one/two/four-user proofs consumed read-only. | A3 rollback/no-rollback evidence, A4 representative outcome evidence, action-class ladder, policy/blast-radius owners. | Runtime eligibility arbitration. | Runtime apply, authority expansion, automation, concurrency, class promotion. | A6 can safely arbitrate execute-or-stop only after blast-radius evidence is no longer unknown. | A5 proves evidence shape only; it does not approve execution, authority, positive promotion, or runtime mutation. |
| `A6` -> `B13` | Runtime eligibility arbitration. | Read-only execute-or-stop gate rows across freshness, authority, blast radius, rollback/no-rollback, anti-flap, verification, learning, routing readiness, and runtime_apply. | A1-A5 certification outputs, freshness owners, authority owners, runtime_apply boundary. | Metric reliability certification for promotion recommendations. | Positive promotion, automatic execution, authority expansion, runtime apply. | B13 may consume A6 because metric reliability needs one canonical gate answer before metrics can support promotion recommendations. | A6 result is `STOP_SAFE` at authority/runtime_apply; it cannot unlock execution or authority by itself. |
| `B13` -> `B16` | Metric reliability certification. | Reliable blocking recommendation certification; positive promotion remains blocked. | Trust/confidence, source confidence, rollback evidence, blast-radius evidence, closure, learning, A6 runtime eligibility. | Rollback authority readiness certification. | Positive promotion, automatic rollback authority, runtime apply, action-class authority, automation. | B16 may start because rollback authority review needs reliable metric and evidence classification before evaluating rollback readiness. | B13 certifies blocking recommendations only; it does not certify authority, rollback execution, or movement. |
| `B16` -> `RT2-S1` | Rollback authority readiness. | Rollback/verification/metric/runtime evidence certified for authority review only; authority/runtime_apply remain STOP gates. | Rollback evidence, verification closure, no-rollback learning, B13 metric reliability, A6 runtime eligibility. | RT2-S1 Measurement & Observability Foundation. | RT2-S2 through RT2-S6 execution, runtime apply, automation, dashboard authority, concurrency, authority expansion. | RT2-S1 may begin because measurement can safely consume certified rollback/verification evidence as read-only context without granting authority. | B16 does not grant automatic rollback authority; only read-only measurement becomes safe, and later RT2 workstreams still require S1 outputs and their own completion criteria. |
| `RT2-S1` -> `RT2-S2` | Measurement and observability. | Runtime cost, runtime time, reaction latency, stop reasons, lifecycle, wait states, dependency topology, Time-To-Safe-Recovery, and bottlenecks visible or owner-mapped as missing. | Execution contracts, events, read models, timestamps, duration fields, latency fields, CPS, truth/convergence. | World and readiness maturation. | Desired-state delta, governed execution coordination, concurrency, recommendations, runtime apply. | S2 may begin only after measurement blockers are owner-mapped so world/readiness can consume known observability gaps safely. | Measurement fields are read-only; dashboards/read models cannot decide, approve, rank execution, mutate, or certify later workstreams. |
| `RT2-S2` -> `RT2-S3` | World and readiness maturation. | Fresh prepared state and readiness summaries bounded for runtime consumption. | Observation outputs, snapshots, freshness, service matrix, quality compact, user/channel/policy state. | Desired-state delta preparedness. | Execution coordination, queue behavior, concurrency, authority expansion, runtime mutation. | S3 may begin when readiness is prepared and bounded, allowing deltas to reference current state without raw runtime scans. | Prepared world/readiness state cannot approve movement, become a planner, or bypass live gates. |
| `RT2-S3` -> `RT2-S4` | Desired-state delta preparedness. | Advisory desired-state delta or bounded prepared plan. | Business Objectives, policies, current state, action-class certification, movement protection. | Governed execution coordination. | Concurrency, automation, runtime queue, authority expansion. | S4 may begin only when a prepared plan can be consumed safely by existing packet/lease/verification owners. | Desired State and deltas remain advisory and non-authorizing; they cannot become Runtime behavior. |
| `RT2-S4` -> `RT2-S5` | Governed execution coordination. | Idempotent governed execution coordination and terminal classification. | Prepared plan, packet, lease, restore barrier, verification plan, rollback/no-rollback state. | Certified concurrency ladder. | Parallelism, blast-radius expansion, automatic execution without authority. | S5 may begin only after one bounded action can move from approval to terminal outcome without stale loops. | Coordination proof for one bounded path does not certify parallelism, wider blast radius, or authority. |
| `RT2-S5` -> `RT2-S6` | Certified concurrency ladder. | Certified concurrency level or explicit STOP_SAFE. | Blast-radius evidence, rollback capacity, verification capacity, policy scope, authority envelope, anti-flap state. | Evidence-based continuous improvement. | Runtime self-optimization, automatic recommendations, authority lowering, safety gate weakening. | S6 may begin after concurrency is certified or explicitly deferred, because recommendations need known safe execution limits. | Parallelism is safety certification only; recommendations cannot mutate runtime, expand authority, or convert metrics into authority. |
| `RT2-S6` -> graduate or return to OMP | Evidence-based continuous improvement. | Owner-mapped recommendation or explicit no-change verdict with safety, latency, cost, time, evidence, and canonical update. | Outcomes, reports, latency/cost/time/topology data, fit analysis, maturity gaps. | Graduation or return to highest unfinished OMP/backlog owner. | New roadmap, new owner, Runtime self-optimization, direct implementation without OMP. | Graduation is allowed only when S6 produces a no-change or owner-mapped recommendation that has been canonically preserved. | S6 output is advisory until OMP routes approved implementation to an existing owner or backlog item. |
| `B9` -> `B10` | Post-admission observation windows. | `post_admission_observation_windows = DONE_READ_ONLY_OWNER_MAPPED`; verified service observation and quality compact `5m`/`1h` windows. | B8 recovery admission certification, service matrix, quality compact. | Recovery slow-start progression. | Runtime apply, traffic admission, authority expansion, queue, synthetic evidence, user movement. | B10 could safely define slow-start only after observation windows were owner-mapped and tested. | B9 only verified observation windows; it could not grant runtime behavior or authority. |
| `B10` -> `B11` | Recovery slow-start progression. | `recovery_slow_start_progression = DONE_READ_ONLY_OWNER_MAPPED`; staged progression `OBSERVATION_CERTIFIED_READ_ONLY` -> `ONE_USER_GOVERNED_RECOVERY_REVIEW` -> `BEYOND_ONE_USER_ACTION_CLASS_REVIEW`. | B8 recovery certification, B9 observation windows, class-level blast-radius certification, action-class ladder. | Org/cohort isolation and identity policy integration. | Runtime apply, traffic admission, automation, authority expansion, concurrency, queue, synthetic evidence, user movement. | B11 may start because B10 defines the recovery progression boundary and keeps identity/cohort scope as the next policy integration gap. | B10 is read-only progression only; it cannot approve recovery traffic, expand authority, or bypass identity/cohort policy gates. |
| `B11` -> `B12` | Org/cohort identity policy integration. | `org_cohort_identity_policy_integration = DONE_READ_ONLY_OWNER_MAPPED`; existing identity -> group/cohort -> allowed/preferred/excluded egress -> exclusive_group/egress ACL/default isolation gates are integrated read-only. | B10 recovery slow-start progression, existing planner gates, identity policy, org policy, channel policy, action-class ladder, authority policy owners. | Next action-class stage certification. | Runtime apply, traffic admission, automation, authority expansion, concurrency, queue, synthetic evidence, user movement, direct class promotion. | B12 may start because B11 proves identity/cohort policy boundaries are visible through existing owners before action-class certification can consume them. | B11 is read-only policy integration only; it cannot grant action-class authority, promote a class, admit traffic, move users, or bypass certification evidence. |
| `B12` -> `B14` | Next action-class stage certification. | `next_action_class_stage_certification = DONE_READ_ONLY_STAGE_GATE_IMPLEMENTED`; A5/A6/B13/B11 evidence is consumed into a stage-review gate that cannot grant authority or runtime apply. | A5 blast-radius evidence, A6 runtime eligibility arbitration, B13 blocking metric reliability, B11 identity/policy boundaries, action-class ladder. | Service/pool/cohort blast-radius scope. | Runtime apply, traffic admission, automation, authority expansion, concurrency, queue, synthetic evidence, user movement, direct class promotion, blast-radius expansion. | B14 may start because B12 proves next-stage work is bounded by certification evidence and explicit authority/runtime STOP gates. | B12 is a read-only stage gate only; it cannot approve class authority, expand blast radius, mutate Runtime, or bypass service/pool/cohort blast-radius review. |
| `B17` -> `B18` | Stale-read reporting with mutation blocking. | `stale_read_mutation_blocking = DONE_READ_ONLY_STALE_READ_MUTATION_BLOCKING`; stale/unknown freshness remains reportable as read-only evidence while mutation stays blocked. | Freshness actionability, runtime eligibility arbitration, routing recommendation readiness, truth/convergence, read-only inventory, OMP. | Owner-issued version/lease pattern extension. | Runtime apply, automation, mutation from stale read, authority expansion, concurrency, queue, planner replacement, synthetic evidence, threshold/formula mutation, user movement. | B18 may start because B17 proves stale reads remain visible but cannot authorize mutation, so lease/version extension can consume freshness and snapshot identity safely. | B17 is observability and gating only; it cannot grant runtime apply, change lease semantics, create a new owner, mutate thresholds/formulas, or move users. |
| `B18` -> `B19` | Owner-issued version/lease pattern. | `owner_issued_version_lease_pattern = DONE_READ_ONLY_OWNER_ISSUED_VERSION_LEASE_PATTERN`; owner-issued version/lease/generation/TTL/source-hash coverage is visible without lease behavior change. | Execution lease, Runtime Model freshness gates, `SNAPSHOT_FAMILIES`, freshness actionability, action-class freshness windows, B17 stale-read mutation blocking, OMP. | Hysteresis and state-change-cost mapping. | Runtime apply, automation, authority expansion, threshold/formula mutation, lease behavior change, new owner, concurrency, queue, planner replacement, synthetic evidence, user movement. | B19 may start because B18 makes freshness/lease identity coverage explicit, allowing state-change-cost and hysteresis mapping to consume currentness boundaries safely. | B18 is read-only coverage only; it cannot change lease behavior, become a truth source, mutate thresholds/formulas, or authorize movement. |
| `B19` -> `B20` | Hysteresis and state-change-cost mapping. | `hysteresis_state_change_cost_mapping = DONE_READ_ONLY_HYSTERESIS_STATE_CHANGE_COST_MAPPING`; existing sticky/current bias, minimum improvement, cooldown, observation window, oscillation detection, user freeze, pair reversal, target block/quarantine, recovery thresholds, and freshness identity cost vocabulary are centralized. | Anti-flap, recovery admission, service threshold, movement-protection, autoswitch safety, OMP. | Hard-failure override anti-flap arbitration. | Runtime apply, automation, authority expansion, threshold/formula mutation, new owner, concurrency, queue, planner replacement, synthetic evidence, user movement. | B20 may start because B19 defines the anti-flap/state-change-cost vocabulary that hard-failure override must arbitrate against. | B19 is read-only vocabulary only; it cannot implement hard-failure override, mutate thresholds/formulas, or authorize movement. |
| `B20` -> `B21` | Hard-failure override anti-flap arbitration. | `hard_failure_override_anti_flap_arbitration = DONE_READ_ONLY_HARD_FAILURE_OVERRIDE_ANTI_FLAP_ARBITRATION`; confirmed hard failure is encoded as anti-flap override candidate for authority review only, while suspected/no hard failure cannot override anti-flap. | Hard-failure classification, hard-failure policy windows, anti-flap, B19 hysteresis/state-change-cost mapping, planner/runtime eligibility, OMP. | Per-user routing control mode. | Runtime apply, automation, authority expansion, hard-failure override execution, threshold/formula mutation, new owner, concurrency, queue, planner replacement, synthetic evidence, user movement. | B21 may start because B20 makes hard-failure/anti-flap arbitration explicit and non-authorizing, so per-user routing control can consume clear safety boundaries. | B20 is read-only arbitration only; it cannot execute override, mutate Runtime, change thresholds/formulas, expand authority, or move users. |
| `B21` -> `C1` | Per-user routing control mode. | `per_user_routing_control_mode = DONE_READ_ONLY_PER_USER_ROUTING_CONTROL_MODE`; explicit or inferred per-user `AUTO` / `PINNED` / `MANUAL` routing control semantics are visible through existing owners. | User registry, group/org policy, planner gates, admin operator surface, B11 identity/cohort policy, B20 hard-failure/anti-flap arbitration, OMP. | Fail-open/fail-closed action-class behavior. | Runtime apply, automation, authority expansion, registry write, planner replacement, new owner, concurrency, queue, synthetic evidence, user movement. | C1 may start because B21 makes user-control mode explicit and non-authorizing, so action-class fail behavior can be recorded against known movement/authority boundaries. | B21 is read-only routing control evidence only; it cannot write the registry, mutate Runtime, expand authority, replace Planner, synthesize evidence, or move users. |
| `C1` -> `C2` | Fail-open/fail-closed action-class behavior. | `fail_open_fail_closed_action_class_behavior = DONE_READ_ONLY_FAIL_OPEN_FAIL_CLOSED_ACTION_CLASS_BEHAVIOR`; every action class records fail-closed Runtime mutation/apply behavior and read-only fail-open allowances for diagnosis, evidence collection, operator explanation, engineering report, and canonical update. | Runtime Model, OMP, planner gates, action-class policy, B21 user mode, stale-read/lease owners, hard-failure arbitration, read-only inventory. | Probabilistic suspicion advisory evidence. | Runtime apply, automation, authority expansion, fail-open runtime mutation, planner replacement, new owner, concurrency, queue, synthetic evidence, user movement. | C2 may start because C1 makes stop/continue behavior explicit and non-authorizing, so weak probabilistic suspicion can be classified advisory-only against a known fail behavior contract. | C1 records behavior only; it cannot make suspicion actionable, grant authority, mutate Runtime, replace Planner, synthesize evidence, or move users. |
| `C2` -> `C3` | Probabilistic suspicion advisory evidence. | `probabilistic_suspicion_advisory_evidence = DONE_READ_ONLY_PROBABILISTIC_SUSPICION_ADVISORY_EVIDENCE`; shadow autonomy, source-confidence, and soft-degradation suspicion have direct blocking power `NONE` and direct execution power `NONE`. | Trust/confidence model, shadow autonomy, soft-degradation policy, OMP, read-only inventory, C1 fail-closed behavior. | Break-glass authority audited exceptional operator policy. | Runtime apply, automation, direct suspicion blocking, authority expansion, planner replacement, threshold/formula mutation, synthetic evidence, user movement. | C3 may start because C2 proves weak/probabilistic suspicion cannot become action authority, so exceptional authority can be documented against a non-silent advisory boundary. | C2 is advisory read-only evidence only; it cannot grant emergency authority, mutate Runtime, lower gates, replace Planner, synthesize evidence, or move users. |
| `C3` -> `C4` | Break-glass authority audited exceptional operator policy. | `break_glass_authority_policy_contract = DONE_READ_ONLY_AUDITED_EXCEPTIONAL_OPERATOR_POLICY`; break-glass is disabled by default, exceptional, audited, operator-policy controlled, and non-authorizing by itself. | OMP, operator authority, governed execution pipeline, observability/audit, feedback/closure, packet/rollback evidence, C2 advisory-only boundary. | All-at-once promotion unavailable verification. | Runtime apply, automation, silent authority expansion, all-at-once promotion, blast-radius expansion, direct class promotion, planner replacement, synthetic evidence, rollback/apply execution, user movement. | C4 may start because C3 proves exceptional authority cannot silently become runtime/class authority, so all-at-once promotion can be verified as unavailable against an explicit non-silent authority boundary. | C3 defines policy only; it cannot invoke break-glass, write restore barrier, execute apply/rollback, expand authority, synthesize evidence, or move users. |
| `C4` -> `C5` | All-at-once promotion unavailable verification. | `all_at_once_promotion_unavailable_verification = DONE_READ_ONLY_ALL_AT_ONCE_PROMOTION_UNAVAILABLE`; current action classes have no all-at-once/direct promotion path and remain class-by-class/authority-review bounded. | Action-class runtime enablement, A5 blast-radius certification, B12 stage certification, B14 service/pool/cohort scope, C3 break-glass policy boundary, OMP. | Rollback as operational compensation preservation. | Runtime apply, automation, silent authority expansion, all-at-once promotion, direct class promotion, blast-radius expansion, rollback/apply execution, planner replacement, synthetic evidence, user movement. | C5 may start because C4 proves promotion cannot silently widen authority, so rollback semantics can be preserved as compensation rather than transaction rollback against a stable non-promoting action-class boundary. | C4 is read-only verification only; it cannot promote classes, widen blast radius, mutate Runtime, grant authority, execute rollback/apply, synthesize evidence, or move users. |
| `C5` -> `C6` | Rollback as operational compensation preservation. | `rollback_operational_compensation_contract = DONE_READ_ONLY_ROLLBACK_OPERATIONAL_COMPENSATION_PRESERVED`; rollback is operational compensation, not database transaction/global rewind. | Runtime Model rollback semantics, rollback policy, B15 containment/forward-fix classification, B16 authority review boundary, C4 promotion-boundary evidence, OMP. | Bounded stale allowance by action class. | Runtime apply, automation, stale-read mutation, authority expansion, automatic rollback execution, transaction rollback abstraction, planner replacement, synthetic evidence, user movement. | C6 may start because C5 proves rollback/recovery semantics are explicit and non-authorizing, so stale-read allowance can be decided by action class without confusing stale evidence with rollback or transaction-rewind authority. | C5 is a read-only contract only; it cannot execute rollback, mutate Runtime, grant stale-read mutation authority, create transaction rollback semantics, expand authority, synthesize evidence, or move users. |

Current transition state:

| Field | Value |
| --- | --- |
| Last completed transition | `C7 -> IMPLEMENTATION_COMPLETE` |
| Produced evidence | `pool_health_capacity_blast_bounds = DONE_READ_ONLY_POOL_HEALTH_CAPACITY_BLAST_BOUNDS_MAPPED`; C7 maps max-ejection/minimum-health semantics to existing capacity/load, action-class, freshness, certified blast-radius, and STOP_SAFE bounds. |
| Current unlocked step | `IMPLEMENTATION_COMPLETE` |
| Current forbidden later steps | Runtime self-optimization; automatic recommendations; direct implementation without OMP; authority lowering; safety-gate weakening; Runtime apply; automation; concurrency enablement; authority expansion; stale-read mutation; blast-radius expansion; all-at-once promotion; queue daemon; planner replacement; registry write; stale mutation authority; user movement |
| Safety reason | Only actionable backlog closure is unlocked; C7 output is read-only capacity/blast-bound evidence and cannot mutate Runtime, authorize pool movement, expand authority, synthesize evidence, start implementation outside OMP, create a new owner, replace Planner, widen blast radius, or move users. |

## 24.2 Capability Production Contract

Status: `ACTIVE_CANONICAL`.

Owner: OMP.

Purpose:

OMP must permanently explain not only what stage comes next and why it becomes available, but what capability each stage produces, who owns that capability, who consumes it, what future capability it unlocks, what remains blocked, and why.

This contract is not a new lifecycle, roadmap, owner, planner, runtime, truth source, capability program, dashboard authority, automation mode, or implementation queue.

Capability production audit:

| Item | Classification | Existing expression | Required extension |
| --- | --- | --- | --- |
| Stage execution order | `EXISTS_COMPLETE` | OMP order and transition contract already define `A5 -> A6 -> B13 -> B16 -> RT2-S1 -> RT2-S6`. | None. |
| Produced evidence | `EXISTS_COMPLETE` | Transition contract names evidence produced by each prior stage. | Reuse. |
| Capability owner | `EXISTS_PARTIAL` | Workstream tables and SYSTEM_MAP name owners, but not as a production graph. | Add production contract and graph. |
| Capability consumers | `EXISTS_PARTIAL` | Workstream tables name consumers, but not one producer / owner / consumer validation. | Add producer-consumer matrix. |
| Blocked capability rule | `EXISTS_PARTIAL` | Transition contract names blocked later stages. | Extend into capability-production terms. |
| Durable production rule | `MISSING` | Reports recorded production evidence, but OMP did not permanently state that production knowledge cannot remain report-only. | Add OMP rule and Canonical Reference durable conclusion. |

Capability production rule:

1. Every produced capability must have exactly one stage producer.
2. Every produced capability must have one canonical owner.
3. Every produced capability must have one or more named consumers.
4. A named consumer is not enough; OMP must verify that the consumer actually consumed the produced capability.
5. A consumer may use only the evidence and capability named by the producing stage.
6. Producing a capability unlocks only the named next capability and never unlocks later capabilities by implication.
7. Blocked capabilities remain blocked until their own producing stage emits accepted evidence.
8. If a capability has no owner, no consumer, duplicate producers, or circular production, OMP must stop before continuing.
9. Engineering reports may record evidence, but the Capability Production Graph, producer/consumer relationships, and unlocked/blocked rules must live in OMP/SYSTEM_MAP/Canonical Reference/CPS.
10. Every producer must have a consumer.
11. Every consumer must consume the produced output, verify consumption, change behavior, and produce the next executable input.
12. Every capability must terminate in a closed executable loop or an allowed stop condition.
13. A produced capability is not `COMPLETE` if its last output is a read model, dashboard, Engineering Report, diagnostic output, recommendation, placeholder, future work, TODO, comment, preview, simulation, advisory surface, or read-only status without another executable consumer.
14. Legal terminal consumers are limited to Runtime Ready For Next Cycle, Capability Certified, Production Maturity Updated, OMP Next Step Produced, Capability Locked, Capability Retired, Terminal `STOP_SAFE`, `ENGINEERING_AUTHORITY`, `OPERATIONAL_AUTHORITY`, and `REAL_WORLD_LIMIT`.
15. If an output has no executable consumer, OMP must mark the capability `PARTIAL`, `BLOCKED`, or `BROKEN`; it must not mark it `COMPLETE`.
16. If an output has a named consumer but consumption is not verified, OMP must emit `CONSUMPTION_NOT_VERIFIED` and keep the capability open.
17. If consumption is verified but no behavior changes, OMP must emit `NO_BEHAVIOR_CHANGE` and keep the capability open.
18. If behavior changes but the next executable output is missing, OMP must emit `NEXT_OUTPUT_NOT_PRODUCED` and keep the capability open.

Capability production completion shape:

```text
Produced Capability
  -> Consumed Capability
  -> Consumption Verified
  -> Capability Behavior Changed
  -> Next Capability Produced
  -> Next Consumer
  -> Legal Terminal Consumer
```

Production promotion shape:

```text
Engineering Complete
  -> Production Candidate
  -> Canonical Source
  -> Safe Deploy
  -> Production Runtime
  -> Truth
  -> Convergence
  -> Runtime Validation
  -> Production Validation
  -> Production Certification
  -> Capability Certified
  -> Production Maturity
  -> Next Capability
```

This shape is an OMP integration of existing owners. It is not a new lifecycle, deployment flow, truth source, certification flow, owner, roadmap, Runtime, Planner, or authority model.

Production Candidate is the OMP state between Engineering Complete and Canonical Source. It is materialized only by existing owners:

- `tools/v7-safe-commit`;
- `tools/v7-safe-push`;
- `tools/v7-truth-check`;
- `tools/v7-safe-deploy`;
- `tools/v7-convergence-status`.

Production Candidate must not bypass tests, truth, convergence, safe deploy, production validation, authority, runtime validation, rollback, learning, Production Maturity, or Current Program State.

Production Promotion Matrix:

| Lifecycle Stage | Owner | Consumer | Evidence | Legal Exit Condition | Next Stage |
| --- | --- | --- | --- | --- | --- |
| Engineering Complete | Existing implementation owner + OMP + Production Maturity Model | OMP | Implementation closure, tests, verification, Engineering Report, owner evidence | `ENGINEERING_COMPLETE`, or legal stop condition | Production Candidate |
| Production Candidate | OMP + safe commit/push owners | Canonical Source | Clean intended change set, passing tests, report evidence, deployable files known | Clean canonical candidate, or `UNSAFE_DEPLOY` / `ENGINEERING_AUTHORITY` | Canonical Source |
| Canonical Source | `tools/v7-safe-commit`, `tools/v7-safe-push`, `tools/v7-truth-check.local_check`, `tools/v7-truth-check.github_check` | Safe Deploy / Truth | Clean workspace, canonical branch, remote branch aligned, no runtime-critical dirtiness | Source truth `PASS`, or `UNSAFE_DEPLOY` / truth blocker | Safe Deploy |
| Safe Deploy | `tools/v7-safe-deploy`, `tools/v7_sync_lib.safe_deploy_plan` | Production Runtime | Allowlist, deploy delta, deploy manifest, runtime linkage, runtime fingerprint, rollback/backup path | Deploy `PASS`, or `UNSAFE_DEPLOY` | Production Runtime |
| Production Runtime | Runtime Model + safe deploy runtime fingerprint owner | Truth / Convergence / Runtime Validation | Deployed files, runtime commit, runtime hashes, runtime snapshot | Runtime identity known, or `RUNTIME_FAIL` / `TRUTH_FAIL` | Truth |
| Truth | `tools/v7-truth-check` | Convergence / OMP | Local, GitHub, runtime checks | Truth `PASS`, or `TRUTH_FAIL` | Convergence |
| Convergence | `tools/v7-convergence-status`, runtime action guard | Runtime Validation / OMP | Local/GitHub/production alignment, deploy delta, runtime action guard | Convergence `PASS`, or `CONVERGENCE_FAIL` | Runtime Validation |
| Runtime Validation | Runtime Model + existing runtime owners | Production Validation | Executable chain evidence, no orphan outputs, verified consumption, live runtime readiness | Runtime validation `PASS`, or `RUNTIME_FAIL` | Production Validation |
| Production Validation | Capability owner + OMP + production validation owners | Production Certification | Real production evidence, behavior contracts, verification, rollback/no-rollback, learning, report | Production validation `PASS`, or `PRODUCTION_VALIDATION_FAIL` / `REAL_WORLD_LIMIT` / authority stop | Production Certification |
| Production Certification | OMP + capability certification owner + Production Maturity Model | Capability State / CPS | Tests, deploy, truth, convergence, runtime validation, production validation, execution closure, verified consumption | Certification accepted, or certification blocker | Capability Certified |
| Capability Certified | OMP legal terminal consumer | Production Maturity / CPS / next capability | Certified capability state and certification report | `Capability Certified`, or legal stop condition | Production Maturity |
| Production Maturity | Production Maturity Model | Current Program State / OMP | `ACCEPT`, `PARTIAL_ACCEPT`, `BLOCK`, `NO_CHANGE`, or `INVALID_EVIDENCE` decision | Maturity decision recorded | Next Capability |
| Next Capability | OMP Capability Production Contract + CPS | Existing next capability owner | Updated capability state, next OMP step, remaining blockers | Next capability selected, locked, retired, or legal stop condition | Continue OMP |

Production promotion completion rule:

```text
Capability COMPLETE =
  Engineering Complete
  AND Production Promotion PASS when production behavior is in scope
  AND Capability Certified
  AND Production Maturity consumed the certification
  AND Current Program State recorded the resulting state
  AND the next capability or legal terminal consumer is known.
```

If a capability is documentation-only, read-only, research-only, design-only, or explicitly not intended for production behavior, OMP must record the legal terminal consumer that replaces Production Promotion. Otherwise Production Promotion is mandatory.

OMP architecture freeze audit:

| Responsibility | OMP ownership after integration | Verdict |
| --- | --- | --- |
| Capability Engineering | Capability Management + Implementation Discipline + existing owners. | `OWNED` |
| Capability Closure | Behavior Architecture Completion Rule + Capability Management. | `OWNED` |
| Verified Consumption | Behavior Enforcement Framework + Verified Consumption states. | `OWNED` |
| Execution Closure | Capability Closure chain + legal terminal consumers. | `OWNED` |
| Production Promotion | Production Promotion Matrix in this Capability Production Contract. | `OWNED` |
| Capability Certification | OMP + capability certification owner + Production Maturity Model. | `OWNED` |
| Capability Progression | Capability Production Contract + Current Program State + next capability selection. | `OWNED` |

Architecture freeze recommendation:

```text
OMP_ARCHITECTURE_FROZEN
```

OMP is the canonical execution framework for all future V7 capabilities.
Future changes should occur only when a real implementation reveals an architectural gap that cannot be solved by existing OMP structures, or when the operator explicitly requests architecture review.

Capability production failure reasons:

- `OUTPUT_NOT_CONSUMED`;
- `CONSUMPTION_NOT_VERIFIED`;
- `NO_BEHAVIOR_CHANGE`;
- `NEXT_OUTPUT_NOT_PRODUCED`;
- `ORPHAN_OUTPUT`;
- `ORPHAN_CONSUMER`.

Capability production graph:

```text
A5 Blast-Radius Certification
  -> A6 Runtime Eligibility Arbitration
  -> B13 Metric Reliability Certification
  -> B16 Rollback Authority Certification
  -> RT2-S1 Measurement & Observability Foundation
  -> RT2-S2 Prepared World & Readiness
  -> RT2-S3 Prepared Delta / Prepared Plan
  -> RT2-S4 Governed Execution Coordination
  -> RT2-S5 Certified Concurrency
  -> RT2-S6 Engineering Recommendation / Engineering Learning
  -> OMP continuation or existing-owner backlog implementation
  -> B1/B2/B3/B4/B5/B6/B7/B8/B9/B10/B11/B12/B14/B15/B17/B18/B19/B20/B21/C1 implementation queue continuation
```

Producer / consumer matrix:

| Stage | Produced Capability | Produced Evidence | Capability Owner | Capability Consumers | Unlocked Capability | Unlocked Stage | Blocked Capability | Blocked Stage | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `A5` | Blast-Radius Certification. | `class_level_blast_radius_certification`; E29 one/two/four-user historical proof consumed read-only. | OMP + blast-radius/action-class owners. | `A6`, Runtime Model, Production Maturity, OMP. | Runtime Eligibility Arbitration. | `A6` | Runtime apply, automation, authority expansion, class promotion, concurrency. | `B13+`, RT2, runtime apply. | Blast-radius evidence shape is certified, but it does not grant execution or authority. |
| `A6` | Runtime Eligibility Arbitration. | `runtime_eligibility_arbitration`; execute-or-stop gate rows. | Runtime Model + OMP + delegated policy/action-class owners. | `B13`, Runtime Model, Production Maturity, OMP. | Metric Reliability Certification. | `B13` | Positive promotion, automatic execution, authority expansion, runtime apply. | `B16+`, RT2, runtime apply. | Metric reliability can consume one canonical STOP/execute answer; A6 itself stops at authority/runtime_apply. |
| `B13` | Metric Reliability Certification. | `metric_reliability_certification`; reliable blocking recommendation evidence. | OMP + metric/promotion evidence owners. | `B16`, Production Maturity, Engineering Intelligence, OMP. | Rollback Authority Certification. | `B16` | Positive promotion, automatic rollback authority, action-class authority, runtime apply. | RT2 and runtime apply. | Rollback authority review needs reliable metric classification; B13 certifies blocking recommendations only. |
| `B16` | Rollback Authority Certification. | `rollback_authority_certification`; rollback evidence certified for authority review only. | Rollback authority/certification owners + OMP. | `RT2-S1`, Runtime Model, Engineering Intelligence, OMP. | Measurement Foundation. | `RT2-S1` | Runtime apply, automation, authority expansion, user movement, RT2-S2+. | `RT2-S2+`, runtime apply. | Measurement may safely consume rollback evidence read-only; authority is not granted. |
| `RT2-S1` | Measurement Evidence, Time Domains, Runtime Observability. | `rt2_s1_measurement_observability_foundation`; cost/time/latency/stop/lifecycle/topology fields visible or owner-mapped. | OMP + Runtime Model + measurement/read-model owners. | `RT2-S2`, `RT2-S6`, Runtime Model, Engineering Intelligence, operator dashboards as read-only surfaces. | Prepared World & Readiness. | `RT2-S2` | Desired-state delta, governed execution coordination, concurrency, recommendations, runtime apply. | `RT2-S3+`, runtime apply. | S2 can consume known measurement/observability gaps; measurement cannot decide or mutate. |
| `RT2-S2` | Prepared World, Prepared Readiness. | `rt2_s2_world_readiness_maturation`; compact state, freshness/readiness, policy gate ownership, trust/learning context. | World Model Plane + Runtime Model placement rules + OMP. | `RT2-S3`, Runtime consumption contract, `RT2-S6`, Engineering Intelligence. | Prepared Delta / Prepared Plan. | `RT2-S3` | Execution coordination, queue behavior, concurrency, authority expansion, runtime mutation. | `RT2-S4+`, runtime apply. | S3 may reference bounded current/readiness state; prepared state cannot approve or bypass gates. |
| `RT2-S3` | Prepared Delta, Prepared Execution Plan. | `rt2_s3_desired_state_delta_preparedness`; advisory desired-state delta and preview-only prepared plan. | Decision Model + existing planner/autoswitch owners + OMP. | `RT2-S4`, Runtime live-gate validation, packet/preview owners. | Governed Execution Coordination. | `RT2-S4` | Concurrency, automation, runtime queue, authority expansion, user movement. | `RT2-S5+`, runtime apply. | S4 may consume a bounded prepared plan; desired state and deltas remain advisory and non-authorizing. |
| `RT2-S4` | Governed Execution Coordination. | `rt2_s4_governed_execution_coordination`; read-only owner-mapped bounded decision-to-terminal-outcome coordination and terminal classification. | Runtime Model + existing execution owners + OMP. | `RT2-S5`, feedback/learning owners, Production Maturity, OMP. | Certified Concurrency. | `RT2-S5` | Parallelism, blast-radius expansion, automatic execution without authority. | `RT2-S6` and runtime apply. | One bounded path is owner-mapped; concurrency still needs its own proof, authority, and capacity certification. |
| `RT2-S5` | Certified Concurrency. | `rt2_s5_certified_concurrency_ladder`; serial-only read-only boundary certified and wider levels explicitly STOP_SAFE. | OMP + action-class/blast-radius/rollback/verification owners + `admin_core.autonomy_trust_acceleration`. | `RT2-S6`, Runtime execution owners, authority model, CPS, Production Maturity. | Evidence-Based Continuous Improvement. | `RT2-S6` | Runtime self-optimization, automatic recommendations, authority lowering, safety gate weakening, runtime apply, concurrency enablement. | `RT2-S6` recommendation effects and runtime apply. | Recommendations now have known safe execution limits; concurrency certification remains safety boundary, not performance-only parallelism or authority. |
| `RT2-S6` | Engineering Recommendation, Engineering Learning, Recommendation Confidence. | `rt2_s6_evidence_based_continuous_improvement`; owner-mapped recommendation to return OMP to existing backlog item `B1`. | OMP + Backlog + Production Maturity + Research Framework/Process + canonical owners + `admin_core.autonomy_trust_acceleration`. | OMP, Engineering Intelligence, future capability evolution, `B1`, Current Program State, Production Maturity. | OMP backlog continuation. | `B1`. | New roadmap, new owner, Runtime self-optimization, direct implementation without OMP, authority lowering, safety-gate weakening. | Any parallel lifecycle. | S6 output is advisory and canonically preserved; OMP now routes continuation to existing backlog item B1. |
| `B9` | Post-Admission Observation Window Verification. | `post_admission_observation_windows`; existing service observation and quality compact `5m`/`1h` windows verified after B8. | Existing recovery admission, service matrix, quality compact owners + OMP + Backlog + Production Maturity. | OMP, `B10`, Current Program State, Production Maturity, Canonical Reference, Movement Protection, Observability, Recovery Admission, Runtime Eligibility. | Recovery Slow-Start Progression. | `B10` | Runtime apply, automation, traffic admission, authority expansion, queue, synthetic evidence, user movement. | `B11+`, runtime apply. | Observation windows are verified read-only; they only unlock slow-start progression design. |
| `B10` | Recovery Slow-Start Progression. | `recovery_slow_start_progression`; staged mapping to existing recovery admission and blast-radius/action-class ladder. | Existing recovery admission, blast-radius/action-class ladder owners + OMP + Backlog + Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `B11`, Current Program State, Production Maturity, Canonical Reference, Movement Protection, Recovery Admission, Runtime Eligibility, Authority Evolution. | Org/Cohort Isolation and Identity Policy Integration. | `B11` | Runtime apply, automation, traffic admission, authority expansion, concurrency, queue, synthetic evidence, user movement. | `B12+`, runtime apply. | Slow-start is defined as a read-only progression only; identity/cohort policy boundaries are now the next integration gap. |
| `B11` | Org/Cohort Identity Policy Integration. | `org_cohort_identity_policy_integration`; existing identity, org/cohort, allowed/preferred/excluded egress, exclusive group, ACL, and default isolation gates integrated read-only. | Existing planner gates, identity/policy owners, OMP, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `B12`, Current Program State, Production Maturity, Canonical Reference, Movement Protection, Runtime Eligibility, Authority Evolution, Production Autonomy. | Next Action-Class Stage Certification. | `B12` | Runtime apply, automation, traffic admission, authority expansion, concurrency, queue, synthetic evidence, user movement, direct class promotion. | `B13+`, runtime apply. | Identity/cohort policy boundaries are now visible to action-class certification; B11 does not grant authority or promote a class. |
| `B12` | Next Action-Class Stage Certification. | `next_action_class_stage_certification`; A5/A6/B13/B11 evidence consumed into a read-only stage certification gate. | Existing action-class ladder, A5/A6/B13/B11 evidence owners, OMP, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `B14`, Current Program State, Production Maturity, Canonical Reference, Movement Protection, Runtime Eligibility, Authority Evolution, Blast Radius, Production Autonomy. | Service/Pool/Cohort Blast-Radius Scope. | `B14` | Runtime apply, automation, traffic admission, authority expansion, concurrency, queue, synthetic evidence, user movement, direct class promotion, blast-radius expansion. | `B15+`, runtime apply. | B12 guarantees next-stage work consumes certification evidence and stops at authority/runtime boundaries; B14 must still model service/pool/cohort scope before any wider blast radius can exist. |
| `B14` | Service/Pool/Cohort Blast-Radius Scope. | `service_pool_cohort_blast_radius_scope`; service/user/SLA fit, B11 identity/cohort policy, A5 blast-radius certification, B12 stage certification, and autoswitch capacity/load owners consumed read-only. | Existing planner capacity/load, service/user/SLA, B11 identity/cohort, A5 blast-radius, B12 stage-certification, autoswitch dynamic blast-radius owners, OMP, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `B15`, Current Program State, Production Maturity, Canonical Reference, Movement Protection, Runtime Eligibility, Authority Evolution, Blast Radius, Production Autonomy. | Containment / Forward-Fix Classification. | `B15` | Runtime apply, automation, traffic admission, authority expansion, concurrency, queue, synthetic evidence, user movement, direct class promotion, blast-radius expansion, threshold/formula mutation. | `B16+`, runtime apply. | B14 makes blast-radius scope visible across service, pool, and cohort dimensions, but does not widen scope or grant authority; B15 may now classify containment/forward-fix outcomes through existing rollback/execution owners. |
| `B15` | Containment / Forward-Fix Classification. | `containment_forward_fix_classification`; terminal containment vs forward-fix states exposed from packet, verification, rollback, and partial-failure policy evidence. | Existing Runtime Model, execution packet, verification, rollback, partial-failure policy, RT2-S4 owners, OMP, Backlog, Production Maturity + `admin_core.operator_execution` and `admin_core.operator_execution_pipeline`. | OMP, `B17`, Current Program State, Production Maturity, Canonical Reference, Movement Protection, Runtime Eligibility, Rollback, Decision Explainability, Production Autonomy. | Stale-Read Reporting With Mutation Blocking. | `B17` | Runtime apply, rollback execution, automation, traffic admission, authority expansion, concurrency, queue, synthetic evidence, user movement, planner replacement, threshold/formula mutation. | `B18+`, runtime apply. | B15 makes terminal containment and forward-fix outcomes visible and explainable, but does not execute rollback or grant authority; B17 may now preserve stale-read reporting while keeping mutation blocked. |
| `B17` | Stale-Read Reporting With Mutation Blocking. | `stale_read_mutation_blocking`; stale/unknown freshness visibility is preserved as reportable read-only evidence while mutation remains blocked. | Existing freshness actionability, runtime eligibility, routing readiness, truth/convergence, read-only inventory owners, OMP, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `B18`, Current Program State, Production Maturity, Canonical Reference, Freshness, Runtime Eligibility, Observability, Decision Explainability, Production Autonomy. | Owner-Issued Version / Lease Pattern. | `B18` | Runtime apply, automation, mutation from stale read, traffic admission, authority expansion, concurrency, queue, synthetic evidence, user movement, planner replacement, threshold/formula mutation, new owner. | `B19+`, runtime apply. | B17 proves stale reads can remain visible without becoming mutation authority; B18 may now extend existing lease/version semantics where owner-issued fields already exist. |
| `B18` | Owner-Issued Version / Lease Pattern. | `owner_issued_version_lease_pattern`; owner-issued version/lease/generation/TTL/source-hash coverage exposed without changing lease behavior. | Existing execution lease, Runtime Model freshness gates, `SNAPSHOT_FAMILIES`, freshness actionability, action-class freshness windows, B17 stale-read mutation blocking, OMP, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `B19`, Current Program State, Production Maturity, Canonical Reference, Freshness, Runtime Eligibility, Observability, Decision Explainability, Production Autonomy. | Hysteresis and State-Change-Cost Mapping. | `B19` | Runtime apply, automation, authority expansion, threshold/formula mutation, lease behavior change, new owner, traffic admission, concurrency, queue, synthetic evidence, user movement, planner replacement. | `B20+`, runtime apply. | B18 makes owner-issued currentness and identity coverage visible; B19 may now centralize existing state-change-cost vocabulary without changing formulas or authority. |
| `B19` | Hysteresis and State-Change-Cost Mapping. | `hysteresis_state_change_cost_mapping`; sticky/current bias, minimum improvement, cooldown, observation window, oscillation detection, user freeze, pair reversal, target block/quarantine, recovery thresholds, and freshness identity cost vocabulary centralized read-only. | Existing anti-flap, recovery admission, service threshold, movement-protection, autoswitch safety, OMP, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `B20`, Current Program State, Production Maturity, Canonical Reference, Movement Protection, Runtime Eligibility, Observability, Decision Explainability, Production Autonomy. | Hard-Failure Override Anti-Flap Arbitration. | `B20` | Runtime apply, automation, authority expansion, hard-failure override execution, threshold/formula mutation, new owner, traffic admission, concurrency, queue, synthetic evidence, user movement, planner replacement. | `B21+`, runtime apply. | B19 proves the existing anti-flap/state-change-cost vocabulary is centralized; B20 may now encode hard-failure override arbitration without creating a new policy owner. |
| `B20` | Hard-Failure Override Anti-Flap Arbitration. | `hard_failure_override_anti_flap_arbitration`; confirmed hard failure becomes anti-flap override candidate for authority review only, while suspected/no hard failure cannot override anti-flap. | Existing hard-failure, hard-failure policy window, anti-flap, B19 hysteresis/state-change-cost, planner/runtime eligibility owners, OMP, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `B21`, Current Program State, Production Maturity, Canonical Reference, Movement Protection, Runtime Eligibility, Observability, Decision Explainability, Production Autonomy. | Per-User Routing Control Mode. | `B21` | Runtime apply, automation, authority expansion, hard-failure override execution, threshold/formula mutation, new owner, traffic admission, concurrency, queue, synthetic evidence, user movement, planner replacement. | `C1+`, runtime apply. | B20 proves hard-failure/anti-flap arbitration is explicit and non-authorizing; B21 may now expose user-level routing control mode without creating a new planner or owner. |
| `B21` | Per-User Routing Control Mode. | `per_user_routing_control_mode`; explicit or inferred per-user `AUTO` / `PINNED` / `MANUAL` routing control semantics are exposed read-only. | Existing user registry, group/org policy, planner gate, admin operator surface, B11 identity/cohort policy, B20 hard-failure/anti-flap arbitration, OMP, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `C1`, Current Program State, Production Maturity, Canonical Reference, Movement Protection, Runtime Eligibility, Authority Evolution, Decision Explainability, Production Autonomy. | Fail-Open / Fail-Closed Action-Class Behavior. | `C1` | Runtime apply, automation, authority expansion, registry write, new owner, traffic admission, concurrency, queue, synthetic evidence, user movement, planner replacement. | `C2+`, runtime apply. | B21 proves user-control boundaries are explicit and non-authorizing; C1 may now record action-class fail behavior without creating a new planner, registry owner, or runtime behavior. |
| `C1` | Fail-Open / Fail-Closed Action-Class Behavior. | `fail_open_fail_closed_action_class_behavior`; per-action-class fail-closed Runtime mutation/apply behavior and read-only fail-open allowance are recorded. | Existing Runtime Model, OMP, planner gates, action-class policy, B21 user mode, stale-read/lease, hard-failure arbitration, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `C2`, Current Program State, Production Maturity, Canonical Reference, Runtime Eligibility, Authority Evolution, Movement Protection, Decision Explainability, Production Autonomy. | Probabilistic Suspicion Advisory Evidence. | `C2` | Runtime apply, automation, authority expansion, fail-open runtime mutation, traffic admission, concurrency, queue, synthetic evidence, user movement, planner replacement. | `C3+`, runtime apply. | C1 makes stop/continue semantics explicit without authorizing execution; C2 may now constrain probabilistic suspicion as advisory-only evidence. |
| `C2` | Probabilistic Suspicion Advisory Evidence. | `probabilistic_suspicion_advisory_evidence`; shadow autonomy, source-confidence, and soft-degradation suspicion are advisory-only with direct blocking power `NONE` and direct execution power `NONE`. | Existing trust/confidence model, shadow autonomy, soft-degradation policy, OMP, read-only inventory, C1 fail-closed behavior, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `C3`, Current Program State, Production Maturity, Canonical Reference, Decision Explainability, Observability, Authority Evolution, Production Autonomy. | Break-Glass Authority Audited Exceptional Operator Policy. | `C3` | Runtime apply, automation, direct suspicion blocking, authority expansion, threshold/formula mutation, traffic admission, concurrency, queue, synthetic evidence, user movement, planner replacement. | `C4+`, runtime apply. | C2 makes weak/probabilistic suspicion non-authorizing; C3 may now define exceptional authority boundaries without allowing suspicion to become action authority. |
| `C3` | Break-Glass Authority Audited Exceptional Operator Policy. | `break_glass_authority_policy_contract`; break-glass is disabled-by-default, audited, exceptional operator policy only, requiring explicit operator policy, incident context, audit, verification/closure, truth/convergence, OMP, and CPS updates. | Existing OMP, operator authority, governed execution pipeline, audit/observability, feedback/closure, packet/rollback owners, Backlog, Production Maturity + `admin_core.operator_execution_pipeline`. | OMP, `C4`, Current Program State, Production Maturity, Canonical Reference, Authority Evolution, Blast Radius, Decision Explainability, Observability, Production Autonomy. | All-at-Once Promotion Unavailable Verification. | `C4` | Runtime apply, automation, silent authority expansion, all-at-once promotion, blast-radius expansion, direct class promotion, rollback/apply execution, synthetic evidence, user movement, planner replacement. | `C5+`, runtime apply. | C3 makes exceptional authority explicit and non-authorizing; C4 may now verify broad promotion remains unavailable under a non-silent authority boundary. |
| `C4` | All-at-Once Promotion Unavailable Verification. | `all_at_once_promotion_unavailable_verification`; current action classes have all-at-once/direct promotion unavailable and class-by-class authority review remains required. | Existing OMP, blast-radius/action-class gates, A5/B12/B14 evidence owners, C3 break-glass policy boundary, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `C5`, Current Program State, Production Maturity, Canonical Reference, Authority Evolution, Blast Radius, Decision Explainability, Observability, Production Autonomy. | Rollback As Operational Compensation. | `C5` | Runtime apply, automation, silent authority expansion, all-at-once promotion, direct class promotion, blast-radius expansion, rollback/apply execution, synthetic evidence, user movement, planner replacement. | `C6+`, runtime apply. | C4 proves broad promotion is unavailable without authorizing anything; C5 may now preserve rollback semantics against stable authority/promotion boundaries. |
| `C5` | Rollback Operational Compensation Contract. | `rollback_operational_compensation_contract`; rollback is preserved as operational compensation, not database transaction/global rewind. | Existing Runtime Model, rollback policy, OMP, Backlog, Production Maturity + `admin_core.operator_execution`. | OMP, `C6`, Current Program State, Production Maturity, Canonical Reference, Runtime Eligibility, Rollback, Decision Explainability, Observability, Production Autonomy. | Bounded Stale Allowance By Action Class. | `C6` | Runtime apply, automation, stale-read mutation, authority expansion, automatic rollback execution, transaction rollback abstraction, synthetic evidence, user movement, planner replacement. | `C7+`, runtime apply. | C5 preserves rollback semantics without authorizing anything; C6 may now decide stale-read allowance by action class against explicit freshness and compensation boundaries. |
| `C6` | Bounded Stale Allowance By Action Class. | `bounded_stale_allowance_by_action_class`; stale/unknown evidence is observable, diagnosable, and reportable, but stale mutation allowance is `0` and fresh evidence inside existing action-class windows is required before mutation review. | Existing freshness actionability, Runtime Model freshness gates, OMP stop rules, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, `C7`, Current Program State, Production Maturity, Canonical Reference, Runtime Eligibility, Decision Explainability, Observability, Production Autonomy. | Pool Max-Ejection / Minimum-Health Capacity and Blast Bounds. | `C7` | Runtime apply, automation, stale-read mutation, authority expansion, threshold/formula mutation, blast-radius expansion, synthetic evidence, user movement, planner replacement. | Runtime apply and post-C7 implementation. | C6 makes stale-read allowance explicit without authorizing stale mutation; C7 may now map pool health/capacity semantics against known freshness and blast boundaries. |
| `C7` | Pool Max-Ejection / Minimum-Health Capacity and Blast Bounds. | `pool_health_capacity_blast_bounds`; proxy-style max-ejection maps to action-class and certified blast-radius user bounds, and minimum-health maps to capacity/load, service-fit, freshness, and STOP_SAFE bounds. | Existing planner capacity/load, action-class ladder, Runtime Model freshness/blast bounds, OMP, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration`. | OMP, Current Program State, Production Maturity, Canonical Reference, Runtime Eligibility, Movement Protection, Blast Radius, Decision Explainability, Observability, Production Autonomy. | Actionable Implementation Backlog Complete. | `IMPLEMENTATION_COMPLETE` | Runtime apply, automation, authority expansion, blast-radius expansion, threshold/formula mutation, synthetic evidence, new owner, planner replacement, pool-level movement, user movement. | Explicit operator-approved future scope only. | C7 closes the final actionable backlog mapping without authorizing execution or changing Runtime behavior; OMP now stops actionable backlog execution. |

Capability graph validation:

| Check | Result | Evidence |
| --- | --- | --- |
| One producer per capability | `PASS` | Each produced capability is tied to exactly one stage in the matrix. |
| One canonical owner per capability | `PASS` | Owners are existing OMP/Runtime/Decision/workstream owners; no new owner is introduced. |
| One or more consumers per capability | `PASS` | Every row names at least one consumer. |
| No orphan capability | `PASS` | Every produced capability unlocks one stage or returns to OMP/existing owner flow. |
| No duplicated producer | `PASS` | Related concepts may be consumed later, but production belongs to one stage only. |
| No circular production | `PASS` | The graph is linear through RT2-S6, then returns to OMP continuation; it does not loop back as a producer of earlier stages. |

Current produced capability state:

| Field | Value |
| --- | --- |
| Last produced capability | Pool Max-Ejection / Minimum-Health Capacity and Blast Bounds |
| Producer stage | `C7` |
| Produced evidence | `pool_health_capacity_blast_bounds = DONE_READ_ONLY_POOL_HEALTH_CAPACITY_BLAST_BOUNDS_MAPPED`; actionable implementation backlog is complete. |
| Capability owner | Existing planner capacity/load, action-class ladder, Runtime Model freshness/blast bounds, OMP stop rules, Backlog, Production Maturity + `admin_core.autonomy_trust_acceleration` |
| Current consumers | OMP, Current Program State, Production Maturity, Canonical Reference, Runtime Eligibility, Movement Protection, Blast Radius, Decision Explainability, Observability, Production Autonomy |
| Current unlocked capability | `IMPLEMENTATION_COMPLETE` |
| Current blocked capabilities | Runtime apply, automation, stale-read mutation, authority expansion, threshold/formula mutation, blast-radius expansion, new owner, queue daemon, planner replacement, synthetic evidence, pool-level movement, user movement |

## 24.3 OMP Progress Dashboard Model

Status: `ACTIVE_CANONICAL_READ_ONLY`.

Owner: OMP.

Purpose:

OMP must provide a permanent read-only dashboard model so an operator can understand current project state within one minute without reading historical reports.

This dashboard model is not a Runtime, Planner, owner, truth source, roadmap, master program, capability program, authority surface, automation mode, implementation queue, or scoring engine. It consumes canonical owners only.

This section defines presentation structure only. Live dashboard values are produced by CPS; labels such as `Current OMP State`, `Current Step`, and `Next Step` do not create a second Current State authority.

Dashboard audit:

| Dashboard area | Classification | Existing expression | Required extension |
| --- | --- | --- | --- |
| Overall OMP Progress | `EXISTS_PARTIAL` | V7 Production Status, Production Maturity, backlog progress, and CPS metrics. | Define one read-only visual grouping. |
| Current OMP State | `EXISTS_PARTIAL` | CPS current state, transition state, produced capability state. | Define mandatory current-state dashboard fields. |
| Capability Progress | `EXISTS_PARTIAL` | Capability Dashboard and CPS capability progress. | Reuse existing capability registry and status terms. |
| Capability Production Graph | `EXISTS_COMPLETE` | OMP Capability Production Contract. | Reuse graph as dashboard source. |
| RT2 Progress | `EXISTS_PARTIAL` | RT2 workstreams and CPS RT2 statuses. | Define compact S1-S6 visual status. |
| Production Maturity | `EXISTS_PARTIAL` | Production Maturity Model and CPS metrics. | Define visual score, target, remaining, and trend fields. |
| Engineering Intelligence | `EXISTS_PARTIAL` | Runtime Model, OMP lifecycle, Production Maturity, SYSTEM_MAP, CPS. | Define compact maturity view. |
| Current Stop Gates | `EXISTS_PARTIAL` | CPS stop reason, OMP stop conditions, Runtime/authority boundaries. | Define operator-visible gate list. |
| Transition Explanation | `EXISTS_COMPLETE` | OMP Capability Transition Contract. | Reuse current transition explanation in dashboard. |
| Capability Quality Future View | `MISSING` | Quality/confidence/readiness/reliability may exist per owner but not as a dashboard read-model placeholder. | Add future-ready read-only placeholder; no scoring yet. |

Dashboard source map:

| Dashboard data | Permanent source | Dashboard use |
| --- | --- | --- |
| Scheduler rules, execution order, transition explanation, production graph | OMP | Explain why current and next steps exist. |
| Current step, previous step, next step, stop reason, current metrics | Current Program State | Display volatile current state only. |
| Owner lookup | SYSTEM_MAP | Show where evidence and capabilities belong. |
| Durable conclusions | Canonical Reference | Prevent report-only dashboard knowledge. |
| Production maturity score | Production Maturity Model | Display current score, target, remaining, and trend. |
| Capability state | OMP capability registry + CPS snapshot | Display capability status without creating a second backlog. |

Visual grammar:

| Visual element | Required meaning |
| --- | --- |
| Progress bar | Shows current value against target only; it is not authority and not certification by itself. |
| Status color | Green = complete/certified, blue = current, amber = waiting/partial, red = blocked/STOP, gray = not started. |
| Capability graph | Displays producer -> produced capability -> owner -> consumers -> unlocked stage -> blocked stage. |
| Compact card | Displays one dashboard area with source owner and current state. |
| Expandable details | May reveal evidence, owner, consumers, stop reason, and source document. |

Dual-view visualization audit:

| Item | Classification | Existing expression | Required extension |
| --- | --- | --- | --- |
| Operator-facing project view | `EXISTS_PARTIAL` | V7 Production Status, CPS snapshot, UI Operator Surface principle. | Add Operator View contract inside the existing dashboard model. |
| Engineering trace view | `EXISTS_PARTIAL` | Capability Production Contract, Transition Contract, SYSTEM_MAP ownership lookup, Engineering Surface principle. | Add Engineering View contract inside the existing dashboard model. |
| Shared canonical data | `EXISTS_COMPLETE` | OMP, SYSTEM_MAP, CPS, Production Maturity Model, Canonical Reference. | Reuse only; no duplicated read model. |
| View synchronization rule | `MISSING` | Current dashboard says sources, but not that both views use identical data. | Add explicit synchronization rule. |
| Future-ready quality/confidence placeholders | `EXISTS_PARTIAL` | Capability Quality future view exists; Recommendation Confidence exists through RT2-S6/confidence owners. | Expose placeholders in both views without scoring. |

Dual-view rule:

1. OMP Dashboard has exactly two presentation views: `OPERATOR_VIEW` and `ENGINEERING_VIEW`.
2. Both views consume the same canonical data from OMP, SYSTEM_MAP, Current Program State, Production Maturity Model, and Canonical Reference.
3. The views may differ only by presentation density, labels, grouping, and default expansion level.
4. Neither view may duplicate state, create a read model, create a truth source, change priority, approve work, certify evidence, mutate Runtime, expand authority, create a queue, or replace Planner.
5. If the two views disagree, the dashboard must treat the mismatch as a visualization defect and resolve back to canonical owners before display.

Synchronization model:

| Shared data | Operator View presentation | Engineering View presentation | Canonical owner |
| --- | --- | --- | --- |
| Overall OMP Progress | Progress bars and status cards. | Score components, backlog counts, maturity source. | OMP + CPS + Production Maturity Model. |
| Current Step / Previous Step / Next Step | Simple current-state card. | Transition contract row with evidence and blockers. | CPS + OMP. |
| Current Production Maturity | One score, target, trend. | Score inputs, target, remaining, next milestone. | Production Maturity Model + CPS. |
| RT2 stage | Compact S1-S6 progress. | RT2 workstream table, owners, inputs, outputs, consumers. | OMP + CPS. |
| Engineering Intelligence stage | Compact maturity strip. | EI ownership lookup, lifecycle, validation/adaptation status. | Runtime Model + OMP + SYSTEM_MAP + CPS. |
| Stop Gates | Red/amber gate cards with reason. | Gate owner, evidence, stop condition, blocked capability. | OMP + Runtime Model + CPS. |
| Produced / Unlocked / Blocked Capability | Simple capability graph. | Capability Production Graph and producer/consumer matrix. | OMP + SYSTEM_MAP + CPS. |
| Current Risks | Short risk cards. | Evidence gaps, blockers, owners, canonical references. | CPS + OMP + Canonical Reference. |
| Current Recommendation | Plain recommendation card. | Recommendation evidence, owner, confidence placeholder, consumers. | OMP + RT2-S6 + CPS. |
| Capability Quality future fields | Placeholder chips only. | Owner-mapped placeholder table. | Existing future read-model owners through SYSTEM_MAP. |

Operator View contract:

| Area | Required display | Default presentation |
| --- | --- | --- |
| Overall OMP Progress | Architecture, Tier A, Tier B, RT2, Engineering Intelligence, Overall Progress, Production Maturity. | Progress bars and compact cards. |
| Current Step | Current Step, Previous Step, Next Step, Reason. | One current-state card with expandable detail. |
| Current Production Maturity | Current score, target, remaining, trend. | Progress bar and milestone label. |
| Current RT2 stage | S1-S6 status. | Compact stage strip. |
| Current Engineering Intelligence stage | Observation, Process, Time, Recommendation, Validation, Adaptation. | Compact maturity strip. |
| Current Stop Gates | Runtime Apply, Automation, Authority, User Movement, Planner, Queue, Concurrency, Desired State. | Color-coded gate cards. |
| Capability state | Current Produced Capability, Current Unlocked Capability, Current Blocked Capability. | Simple capability graph. |
| Current Risks | Active stop risks and forbidden later steps. | Short risk cards. |
| Current Recommendation | Current OMP recommendation and required action. | Plain-language recommendation card. |
| Expandable details | Source owner, evidence pointer, blocker reason. | Hidden by default. |

Operator View principles:

1. Minimal.
2. Fast.
3. Visually understandable.
4. Uses progress bars, cards, color coding, and a simple capability graph.
5. No engineering noise by default.
6. Every card can expand to show its source owner.

Engineering View contract:

| Area | Required display | Default presentation |
| --- | --- | --- |
| Capability Graph | Current capability dependency graph. | Expanded graph. |
| Capability Production Graph | Stage -> Produced Capability -> Owner -> Consumers -> Unlocked Stage -> Blocked Stage. | Full production graph. |
| Producer / Consumer Matrix | Producer, produced evidence, owner, consumers, blockers. | Full matrix. |
| Transition Contracts | Why next step is available and why later steps remain blocked. | Full transition rows. |
| Capability Contracts | Capability status, DoD, remaining criteria, reopen triggers. | Traceable tables. |
| Capability Quality future-ready | Quality, Confidence, Readiness, Reliability, Recommendation Confidence. | Placeholder table; no scoring. |
| Owner Mapping | Canonical owner, existing read owners, forbidden ownership. | SYSTEM_MAP links. |
| Engineering Intelligence | Observation, Process, Time, Recommendation, Validation, Adaptation. | Owner and lifecycle trace. |
| RT2 Workstreams | Purpose, owners, inputs, outputs, consumers, criteria, evidence. | Full workstream rows. |
| Dependency Graph | Produced capability, consumed evidence, blocked future capabilities. | Expanded dependency view. |
| Current Evidence | Current produced evidence and consumers. | Evidence trace table. |
| Current Blockers | Stop gates, blocked capabilities, unsafe later steps. | Blocker matrix. |

Engineering View principles:

1. Complete.
2. Traceable.
3. Explainable.
4. Evidence based.
5. Every displayed field must point back to OMP, SYSTEM_MAP, CPS, Production Maturity Model, Canonical Reference, or an existing owner named by those documents.

Dashboard sections:

| Section | Required display | Canonical source |
| --- | --- | --- |
| Overall OMP Progress | Architecture, Tier A, Tier B, RT2, Engineering Intelligence, Overall Progress, Production Maturity. | OMP + CPS + Production Maturity Model. |
| Current OMP State | Current Step, Previous Step, Next Step, Reason, Current Stop, Current Capability Produced, Current Capability Consumed. | CPS + OMP transition/production contracts. |
| Capability Progress | Status for each major capability: `NOT_STARTED`, `IN_PROGRESS`, `COMPLETED`, `BLOCKED`, `WAITING`, `CERTIFIED`, `CONSUMED`. | OMP capability registry + CPS. |
| Capability Production Graph | Stage -> Produced Capability -> Capability Owner -> Consumers -> Unlocked Stage -> Blocked Stage. | OMP Capability Production Contract + SYSTEM_MAP. |
| RT2 Progress | `RT2-S1` through `RT2-S6` and current maturity. | OMP RT2 workstreams + CPS. |
| Production Maturity | Current score, target score, remaining score, latest trend, next milestone. | Production Maturity Model + CPS. |
| Engineering Intelligence | Observation, Process, Time, Recommendation, Validation, Adaptation, current maturity. | Runtime Model + OMP + Production Maturity + CPS. |
| Current Stop Gates | Runtime Apply, Automation, Authority, User Movement, Planner, Queue, Concurrency, Desired State, and why each is blocked or open. | OMP stop rules + Runtime Model + CPS. |
| Transition Explanation | Current stage -> Produced capability -> Why next stage unlocked -> Why later stages remain blocked. | OMP Capability Transition Contract. |
| Capability Quality Future View | Capability Quality, Confidence, Readiness, Reliability as reserved read-model fields only. | Future existing-owner read models; no score until certified. |

### 24.3.1 Historical Dashboard Snapshot

Classification: `HISTORICAL_SNAPSHOT`.
Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

Historical dashboard snapshot:

| Area | Current display |
| --- | --- |
| Architecture | `[##########] 100% COMPLETE` |
| Tier A | `[##########] 6 / 6 COMPLETE` |
| Tier B | `[##########] 21 / 21 COMPLETE` |
| RT2 | `[##########] 6 / 6 COMPLETE_READ_ONLY` |
| Engineering Intelligence | `[########--] FINAL_CANONICAL_STATE / implementation evidence future` |
| Overall actionable backlog | `34 / 34 complete` |
| Production Maturity | `[#######---] 66.9 / 100; target 100; remaining 33.1` |
| Current step | `IMPLEMENTATION_COMPLETE` |
| Previous step | `C7_MAP_POOL_MAX_EJECTION_MINIMUM_HEALTH_SEMANTICS_TO_V7_CAPACITY_AND_BLAST_BOUNDS` |
| Reason current step is available | C7 produced pool health capacity and blast-bound evidence without granting Runtime apply, authority, blast-radius expansion, threshold/formula mutation, synthetic evidence, or user movement. |
| Current stop | `ACTIONABLE_BACKLOG_COMPLETE` |

RT2 dashboard:

| Workstream | Status | Current maturity | Dashboard note |
| --- | --- | --- | --- |
| `RT2-S1` | `DONE_READ_ONLY` | Complete | Measurement/observability visible or owner-mapped. |
| `RT2-S2` | `DONE_READ_ONLY` | Complete | Prepared world/readiness is read-only and non-authorizing. |
| `RT2-S3` | `DONE_READ_ONLY` | Complete | Desired-state delta remains advisory. |
| `RT2-S4` | `DONE_READ_ONLY` | Complete | Governed coordination is owner-mapped without queue creation. |
| `RT2-S5` | `DONE_READ_ONLY` | Complete | Wider concurrency remains STOP_SAFE. |
| `RT2-S6` | `DONE_READ_ONLY` | Complete | Recommendation returns OMP to `B1`; advisory only. |

Engineering Intelligence dashboard:

| Capability | Current maturity | Source |
| --- | --- | --- |
| Observation | `MEASURED_PARTIAL` | `RT2-S1`, existing observation/read-model owners. |
| Process | `UNDERSTOOD_EXPRESSED` | Runtime Model + Work Placement + Decision Lifecycle + OMP. |
| Time | `CANONICALIZED_INSIDE_RT2` | Runtime Model + `RT2-S1` + `RT2-S6`. |
| Recommendation | `MATERIALIZED_ADVISORY` | `RT2-S6` + OMP + Backlog. |
| Validation | `UNDERSTOOD_PARTIAL_VALIDATION` | Engineering Intelligence Phase 2 owners. |
| Adaptation | `ADAPTIVE_ENGINEERING_READY_IMPLEMENTATION_FUTURE` | Engineering Intelligence Phase 3 owners. |

Historical stop gates dashboard:

| Gate | Display status | Why |
| --- | --- | --- |
| Runtime Apply | `BLOCKED` | No runtime apply authority or certification is active. |
| Automation | `BLOCKED` | Production autonomy is not certified. |
| Authority | `BLOCKED` | No authority expansion is active. |
| User Movement | `BLOCKED` | No approved packet or movement authority is active. |
| Planner | `BLOCKED` | Existing planner/autoswitch owners remain; no replacement is allowed. |
| Queue | `BLOCKED` | No queue daemon or hidden retry engine is certified. |
| Concurrency | `BLOCKED` | Current certified boundary is serial-only/read-only. |
| Desired State | `ADVISORY_ONLY` | Desired state and deltas cannot authorize movement or mutate Runtime. |

Capability quality future view:

| Field | Current status | Rule |
| --- | --- | --- |
| Capability Quality | `RESERVED_READ_MODEL_ONLY` | No score until an existing owner produces certified quality evidence. |
| Capability Confidence | `RESERVED_READ_MODEL_ONLY` | May display existing confidence only; cannot become authority. |
| Capability Readiness | `RESERVED_READ_MODEL_ONLY` | May display readiness from canonical owners only. |
| Capability Reliability | `RESERVED_READ_MODEL_ONLY` | May display reliability after verification/certification evidence exists. |

### 24.3.2 Permanent Dashboard Rules

Classification: `PERMANENT_RULE`.

Dashboard rules:

1. Dashboard is read-only.
2. Dashboard consumes canonical owners only.
3. Dashboard cannot decide, approve, rank implementation, mutate Runtime, certify evidence, expand authority, create a queue, create a planner, create a roadmap, or become a truth source.
4. Dashboard status must name its source owner.
5. Dashboard may show future-ready placeholders only as `RESERVED_READ_MODEL_ONLY`; placeholders cannot affect OMP priority or authority.
6. Engineering reports may record dashboard audit evidence, but the dashboard model must live in OMP and the current snapshot must live in Current Program State.
7. Deleting the engineering report must not remove any important dashboard structure, ownership rule, current state field, or durable conclusion.

Product Evolution Dashboard Behavior Contract:

Dashboard is the read-only visibility consumer in the Product Evolution behavior loop.

Dashboard must consume:

| Input | Required source |
| --- | --- |
| Current Program State | Current step, target, transition, blockers, readiness context, and dashboard snapshot. |
| Production Maturity | Current maturity, target, remaining score, milestone, blockers, and maturity decision when present. |
| Framework outputs | Product Observation, Product Value, Target, Capability Gap, Evidence Gap, and Field Validation results when present in Engineering Reports. |
| Engineering Intelligence outputs | Recommendation Confidence, Prediction Quality, Recommendation Adjustment, Evidence Quality Feedback, Reasoning Improvement, and Framework Improvement Signal. |
| Engineering Reports | Historical evidence, latest decision, validation, blockers, and learning trigger. |

Dashboard must produce:

| Output | Meaning |
| --- | --- |
| Operator Visibility | One-minute current reality, target, stop gates, blockers, recommendation, and confidence context. |
| Engineering Visibility | Traceable owner/evidence/recommendation/learning graph for engineers. |
| Blocker Visibility | Current blocked capability, stop gate, owner, and reason. |
| Confidence Visibility | Read-only recommendation confidence, prediction quality, and uncertainty context. |
| Target Visibility | Current active target, target status, maturity gap, and next visible target context. |
| Learning Visibility | What changed, what was learned, what prediction differed, and what future recommendation changed. |

Dashboard behavior contract:

- Operator may use Dashboard output to ask better questions, choose what to inspect, or request OMP continuation.
- Engineering reviewer may use Dashboard output to find owners, blockers, evidence, confidence, and learning context.
- OMP may consume operator questions and engineering observations as inputs to the next Engineering Context Resolver.
- Dashboard output itself must never become approval, priority, certification, execution permission, maturity write, authority, automation, Runtime logic, routing logic, planner behavior, evidence, or truth source.

Dashboard completion rule:

```text
Canonical state consumed
  -> Operator / engineer visibility changed
  -> Operator question or engineering observation becomes clearer
  -> OMP decision is better informed through existing Engineering Context Resolver
  -> Engineering Report records the decision and whether visibility helped
```

If Dashboard output cannot be traced back to canonical owners, Dashboard is incomplete for that displayed field and must show the field as `UNKNOWN`, `NOT_APPLICABLE`, or owner-mapping defect.

Behavior Chain Dashboard Readiness:

Dashboard must expose read-only Behavior Chain visibility when the data exists:

| Display field | Required source | Rule |
| --- | --- | --- |
| Behavior Chain Status | Engineering Report Behavior Enforcement section + OMP. | Display `COMPLETE`, `PARTIAL`, `BLOCKED`, `BROKEN`, or `UNKNOWN`; never decide. |
| Producer status | SYSTEM_MAP Behavior Propagation Ownership Matrix + report evidence. | Show source owner and output state. |
| Consumer status | SYSTEM_MAP + report evidence. | Show consumed, missing, blocked, or unknown. |
| Behavior change status | Engineering Report Behavior Enforcement section. | Show pass/fail/partial/unknown only. |
| Output status | Engineering Report / CPS / Production Maturity / EI output field. | Show produced, missing, blocked, or not applicable. |
| Recovery path | OMP or Engineering Report recovery field. | Show next verification path; never execute it. |

Dashboard must not hide `PARTIAL`, `BLOCKED`, `BROKEN`, or `UNKNOWN` chain status behind positive progress indicators.
Dashboard may show checkmarks only when the source Behavior Chain Status is `COMPLETE`.

### Dashboard UI Foundation Contract

Status: `ACTIVE_CANONICAL_UI_FOUNDATION`.

Owner: OMP.

Purpose:

The OMP Dashboard is the canonical V7 OMP section inside the admin panel. It lives behind the separate top-level admin navigation item `OMP` and route `/admin/omp`; it does not replace the existing admin home / overview screen. Inside the OMP tab, Executive View is the top layer, followed by synchronized Operator View and Engineering View, all from the same canonical data.

The UI foundation is not dashboard implementation code, a Runtime, Planner, owner, truth source, roadmap, scoring engine, authority surface, automation surface, queue, or implementation path.

UI discovery audit:

| Existing UI/read-model area | Classification | Reuse decision | Dashboard role |
| --- | --- | --- | --- |
| Existing admin Overview / dashboard schema | `EXISTS_PARTIAL` | Reuse read-only summary, health, route, service, and alert patterns from `admin_core.overview_views` and `v7.admin.dashboard.v1`. | Existing admin home / overview remains unchanged; OMP is a separate top-level tab. |
| Existing admin navigation | `EXISTS_UNDER_OTHER_NAME` | Reuse simple top-level sections and one-click section switching. | Add/reuse top-level `OMP` tab; do not create a second shell or replace the home screen. |
| Existing Operator surfaces | `EXISTS_PARTIAL` | Reuse recommendation, evidence, blocker, drawer, and progressive-disclosure patterns from operator view/decision/observability surfaces. | Operator View language and expandable details. |
| Existing Execution surfaces | `EXISTS_PARTIAL` | Reuse governed execution, packet, lease, rollback, evidence, and terminal-state trace as details. | Engineering View trace links only; no execution control. |
| Existing Health / Checks / Runtime read views | `EXISTS_PARTIAL` | Reuse read-only health, runtime-summary, service, route, and diagnostic contracts. | Drill-down evidence panels and stop-gate explanations. |
| Existing design HTML dashboards | `EXISTS_UNDER_OTHER_NAME` | Reuse layout vocabulary only: top navigation, compact metrics, status chips, cards, tables, alerts, topology, responsive grid. | Visual reference only; no state, owner, or implementation truth. |
| OMP Dashboard Model and Dual-View Model | `EXISTS_COMPLETE` | Reuse as canonical dashboard data contract and presentation split. | Permanent model for the OMP tab. |
| Canonical OMP navigation rule | `MISSING` | Add inside OMP. | `OMP_DASHBOARD` is a separate top-level admin section, not the global home page. |

OMP tab rule:

1. The existing V7 admin home / overview page remains unchanged.
2. `OMP_DASHBOARD` is reached through the top-level `OMP` admin tab and route `/admin/omp`.
3. Executive View is the first layer inside the OMP tab.
4. Operator View and Engineering View are synchronized modes on the same OMP page, not separate sources, read models, or dashboards.
5. Existing Overview, Health, Operator, Routing, Users, Channels, Checks, Execution, Logs, Settings, and Security surfaces keep their existing navigation meaning and may be drill-down destinations.
6. A secondary surface may display domain-specific state only from its existing owner; it must not override OMP Dashboard state.
7. If a secondary surface and OMP Dashboard disagree, the disagreement is a visualization/data wiring defect and must resolve back to canonical owners.

Dashboard hierarchy:

| Layer | UI responsibility | Required content | Source |
| --- | --- | --- | --- |
| App shell | Provide stable navigation. | Existing home / overview remains default; top-level `OMP` tab opens `/admin/omp`; drill-downs reuse existing admin sections. | OMP + SYSTEM_MAP. |
| Page header | Show current program identity inside OMP tab. | V7, Product Execution Mode, current step, Executive/Operator/Engineering view toggle, source timestamp, read-only badge. | CPS + OMP. |
| Operator summary band | One-minute status. | Overall progress, Production Maturity, RT2, Engineering Intelligence, current step, next step, stop gates. | CPS + OMP + Production Maturity. |
| Current work area | Explain why now. | Previous/current/next step, reason, produced capability, consumed capability, unlocked capability, blocked capability, recommendation, risk. | OMP transition/production contracts + CPS. |
| Capability visual area | Show system flow. | Simple capability graph in Operator View; full production/dependency graph in Engineering View. | OMP + SYSTEM_MAP. |
| Detail drawer / expandable rows | Preserve traceability without noise. | Owner, evidence, consumers, blockers, source document, related report, current verification state. | SYSTEM_MAP + CPS + Canonical Reference + existing owners. |

Operator View UI foundation:

| Region | Required widgets | Rule |
| --- | --- | --- |
| Status strip | Production Maturity indicator, current step badge, read-only badge, stop-gate summary. | Must fit one scan; no raw engineering tables by default. |
| Progress row | Overall OMP progress, Tier A/B/C, RT2, Engineering Intelligence, backlog completion. | Progress bars only; progress is not authority. |
| Current work card | Previous step, current step, next step, reason current step is available. | Plain operator language. |
| Capability card | Produced, consumed, unlocked, blocked capability. | Simple graph or stacked cards. |
| Stop gates | Runtime Apply, Automation, Authority, User Movement, Planner, Queue, Concurrency, Desired State. | Red/amber/blue/green/gray status colors with reason. |
| Recommendation / risk cards | Current recommendation, current risks, why later steps remain forbidden. | Short by default; expandable details. |
| Drill-down links | Operator, Execution, Health, Evidence, Canonical owner. | One click from the card; no duplicated state. |

Engineering View UI foundation:

| Region | Required widgets | Rule |
| --- | --- | --- |
| Capability graph | Capability dependency graph and current position. | Trace every node to owner. |
| Production graph | Stage -> produced capability -> owner -> consumers -> unlocked stage -> blocked stage. | Reuse OMP Capability Production Contract. |
| Producer / consumer matrix | Producer, evidence, consumers, blockers, owner. | Full trace table. |
| Transition contracts | Why next step is available; why later steps remain blocked. | Reuse OMP Capability Transition Contract. |
| RT2 / Engineering Intelligence | Workstream and EI maturity details. | Read-only/advisory boundaries visible. |
| Evidence and blocker panes | Produced evidence, consumed evidence, stop gates, missing proof. | Link to existing reports/owners; no synthetic evidence. |
| Owner mapping | Canonical owner and existing read owners. | SYSTEM_MAP owns lookup. |
| Future quality placeholders | Quality, confidence, readiness, reliability, recommendation confidence. | `RESERVED_READ_MODEL_ONLY`; no scoring. |

Navigation model:

| Navigation target | User meaning | Source rule |
| --- | --- | --- |
| `OMP` | See complete project state and current OMP step. | Top-level admin tab at `/admin/omp`; consumes canonical owners only and does not replace existing home. |
| `Current Step` | Jump to current backlog/work item context. | CPS current step + OMP. |
| `Current Report` | Open latest relevant Engineering Report as evidence. | Report is evidence only. |
| `Canonical Owner` | Open the document that owns the displayed rule. | SYSTEM_MAP + Canonical Reference. |
| `Evidence` | Open evidence, tests, or read-only payload behind a card. | Existing evidence/read-model owner. |
| `Operator` | Open operator-facing recommendation/workflow details. | Existing operator surfaces. |
| `Execution` | Open governed execution/packet trace when relevant. | Existing execution owners; no apply control from dashboard. |
| `Health / Read Models` | Open health, route, service, runtime, and diagnostic details. | Existing read-only owners. |

Visual foundation:

| Component | Required use | Forbidden use |
| --- | --- | --- |
| Progress bar | Show percent/count against canonical target. | Authority, certification, or hidden scoring. |
| Timeline | Show previous/current/next OMP stage. | New roadmap or alternate queue. |
| Stage card | Show one OMP capability/stage with owner and status. | Duplicated backlog item. |
| Badge/chip | Show status, owner, gate, or maturity. | Substitute for evidence. |
| Capability graph | Explain producer/consumer/unlock/block flow. | Planner or dependency executor. |
| Producer -> consumer graph | Show traceability. | Automation trigger. |
| Stop-gate indicator | Show why something is blocked/open. | Gate decision or authority change. |
| Expandable detail | Show source, evidence, owner, blockers. | Hide missing ownership. |
| Charts | Reserved for later implementation. | Do not implement or require charts in this task. |

UX principles:

1. Modern engineering platform: calm, fast, readable, sparse, and high signal.
2. Operator View is minimal and beautiful enough to understand in one minute.
3. Engineering View is complete, traceable, and evidence based.
4. Both views use identical canonical data.
5. No duplicated widgets when a single shared widget can change presentation density.
6. No duplicated read model, state, truth, score, priority, or authority.
7. Default view hides engineering noise but keeps one-click traceability.
8. Dashboard is read-only and must visibly say so.
9. Charts are not part of this foundation; only the UI model is canonicalized.
10. Existing admin surfaces remain useful, and the OMP Dashboard is a separate top-level admin section rather than the home screen.

### Dashboard Design System

Status: `ACTIVE_CANONICAL_DESIGN_SYSTEM`.

Owner: OMP.

Purpose:

The Dashboard Design System defines the permanent visual language for future OMP Dashboard implementation. It does not implement UI, React, HTML, Runtime behavior, OMP logic, new read models, new data models, new authority, or new architecture.

Dashboard philosophy:

The dashboard must answer immediately:

1. Where are we?
2. Why are we here?
3. What is blocked?
4. What was produced?
5. What comes next?
6. Why?
7. What changed today?
8. What is the current maturity?

Reference-product research:

| Reference | Reuse for V7 | Avoid for V7 |
| --- | --- | --- |
| Linear | Focused workspace, restrained density, keyboard-fast feel, low visual noise, elegant status language. | Ambiguous beauty without explicit evidence trace. |
| GitHub Projects | Multiple synchronized views over the same underlying items: table, board, roadmap, filters, fields. | Turning view configuration into a second planning system. |
| Stripe Dashboard | Clear home surface, sidebar navigation, search/command access, strong hierarchy, operational polish. | Business-metric cards that imply authority without evidence. |
| Datadog | Dashboard purpose, widgets, grouping, drill-down, operational status visualization. | Metric overload, duplicated dashboards, noisy wallboards. |
| Grafana | Time-series/dashboard discipline, panels, variables, reusable views, drill-down by data source. | Chart-first UI before V7 has certified chart read models. |
| Apple HIG / modern macOS / modern iOS | Clarity, hierarchy, spacing, legibility, calm color, accessible targets, dark/light mode quality. | Decorative motion, low contrast, tiny hit targets, excessive translucency. |

V7 visual language:

| Dimension | Canonical rule |
| --- | --- |
| Tone | Calm, precise, production-grade, minimal, not decorative. |
| Density | Operator View is sparse; Engineering View is dense but structured. |
| Typography | Large readable headings, compact labels, numeric emphasis only for canonical metrics. |
| Spacing | Consistent 8px rhythm; card interiors breathe; engineering tables remain scan-friendly. |
| Radius | Small radius, preferably `6-8px`; no large bubbly cards. |
| Color | Soft semantic palette: green complete, blue current/info, amber waiting/risk, red blocked/STOP, gray inactive. |
| Dark mode | First-class, low-glare, high-contrast text, restrained borders, no heavy gradients. |
| Light mode | First-class, quiet background, clear cards, same semantic colors. |
| Icons | Use simple recognizable icons for status/navigation when implemented; text labels remain required for safety-critical status. |
| Motion | Minimal and functional only: expansion, focus, selection, graph highlight. |
| Visual noise | No decorative blobs, no chart clutter, no duplicated widgets, no irrelevant metrics. |

Dashboard layout system:

| Surface | Layout |
| --- | --- |
| Operator Home Screen | Header + status strip + progress row + current stage card + stop-gate/risk row + simple capability graph + expandable details. |
| Engineering View | Header + graph/matrix split + transition/production contracts + RT2/EI panels + evidence/blocker/owner tables + expandable technical detail. |
| Capability Graph | Left-to-right flow: stage -> produced capability -> owner -> consumers -> unlocked stage -> blocked stage. |
| Production Maturity | One large maturity indicator with target, remaining, next milestone, and source owner. |
| RT2 Progress | Six-stage horizontal strip with complete/current/blocked markers and workstream detail expansion. |
| Engineering Intelligence | Six-part maturity strip: Observation, Process, Time, Recommendation, Validation, Adaptation. |
| Current Stage | Timeline card: previous -> current -> next, plus why current is available. |
| Current Stop Gates | Grid of gate cards with status, reason, owner, and blocked capability. |

Operator Home Screen conceptual mockup:

```text
V7 / OMP Dashboard                                      READ ONLY
Product Execution Mode             Operator View | Engineering View

[Production Maturity 66.9/100] [Current: IMPLEMENTATION_COMPLETE] [RT2 Complete] [EI Canonical]

Overall Progress
Architecture [##########]  Tier A [##########]  Tier B [######----]
RT2          [##########]  Backlog [######----] Production [#####-----]

Current Stage
C7 completed -> IMPLEMENTATION_COMPLETE -> Stop actionable backlog execution
Why now: C7 produced owner-mapped pool health capacity and blast-bound evidence.

Capability
Produced: Probabilistic Suspicion Advisory Evidence
Consumed by: C3 break-glass authority audited exceptional operator policy
Unlocked: Break-Glass Authority Audited Exceptional Operator Policy
Blocked: Runtime apply, automation, authority, queue, concurrency, registry write, user movement, new owner

Stop Gates
[BLOCKED Runtime Apply] [BLOCKED Automation] [BLOCKED Authority] [BLOCKED User Movement]
[BLOCKED Planner] [BLOCKED Queue] [BLOCKED Concurrency] [ADVISORY Desired State]

Recommendation
Execute C3 through existing OMP, operator authority, documentation, and canonical update owners.
```

Engineering View conceptual mockup:

```text
V7 / OMP Dashboard                                      READ ONLY
Engineering View

Capability Production Graph
B12 -> Next Action-Class Stage Certification -> existing action-class ladder/A5/A6/B13/B11 evidence owners
   -> consumers: OMP, B14, CPS, Production Maturity, Canonical Reference
   -> unlocks: B14
   -> blocks: runtime apply, automation, authority expansion, queue, user movement, direct class promotion, blast-radius expansion

Producer / Consumer Matrix
| Producer | Evidence | Owner | Consumers | Unlocked | Blocked |

Transition Contract
Why C3 is available: C2 evidence is read-only, owner-mapped, tested, and safe to consume.
Why later steps remain forbidden: no runtime apply, authority, registry write, concurrency, planner replacement, user movement, or new-owner proof.

Panels
[RT2 S1-S6] [Engineering Intelligence] [Production Maturity] [Stop Gates]
[Evidence] [Canonical Owners] [Risks] [Expandable Technical Detail]
```

Component design:

| Component | Visual rule | Interaction |
| --- | --- | --- |
| Progress bar | Thin, labeled, source-owned, no hidden formula. | Hover/focus shows source and last update. |
| Timeline | Previous/current/next only by default. | Click current opens transition detail. |
| Capability card | Status, owner, produced/consumed/unlocked/blocked. | Expand for evidence and consumers. |
| Capability graph | Simple in Operator View; full in Engineering View. | Select node to show owner/evidence/details. |
| Stage graph | Horizontal OMP/RT2 stage flow. | Click stage opens workstream/contract detail. |
| Dependency graph | Engineering-only by default. | Filter by owner, blocker, consumer. |
| Status badge | Semantic color plus text. | Never color-only. |
| Maturity indicator | Score, target, remaining, next milestone. | Expand to category breakdown. |
| Risk indicator | Amber/red card with reason and owner. | Expand to mitigation/blocked capability. |
| Stop Gate card | Gate status, reason, owner, blocked capability. | Expand to rule/evidence. |
| Engineering card | Dense trace card with owner and source. | Expand/collapse technical details. |
| Recommendation card | Plain-language recommendation plus safety boundary. | Expand for evidence/confidence placeholder. |
| Expandable section | Progressive disclosure. | Default closed unless current blocker. |

Interaction model:

1. Default view is `OPERATOR_VIEW`.
2. `ENGINEERING_VIEW` is a mode switch, not a new page or data source.
3. Every card supports one-click drill-down to owner/evidence when implemented.
4. Search is global across current step, capability, owner, evidence, gate, report, and canonical reference.
5. Filters exist only in Engineering View by default: owner, status, stage, blocker, consumer, evidence type.
6. Timeline interaction shows previous/current/next; deeper history is an expansion.
7. Capability graph interaction highlights producer, produced capability, owner, consumers, unlocked stage, and blocked stages.
8. Mobile adaptation stacks status strip, current stage, stop gates, and recommendation first; graph becomes scrollable/summary-first.
9. Keyboard access and visible focus are required in future implementation.
10. Dashboard interactions cannot mutate Runtime, approve work, rank implementation, or change authority.

Design Do / Do Not:

| Do | Do not |
| --- | --- |
| Use clear hierarchy, calm contrast, compact status language. | Create decorative hero/marketing UI. |
| Show source owner for every important field. | Present unsourced numbers. |
| Prefer progress bars, timelines, cards, badges, and simple graphs. | Require charts before chart read models exist. |
| Use progressive disclosure. | Dump full engineering tables into Operator View. |
| Preserve identical data across both views. | Duplicate state, truth, read models, or widgets. |
| Make blocked state explicit. | Hide STOP gates behind green progress. |
| Keep dark and light modes equally polished. | Treat dark mode as an afterthought. |

## 25. Program Rule For Future Work

Before starting any future implementation task, Codex must treat this file as the first program source. If a prompt conflicts with this program, the optimizer wins unless the user explicitly changes the program through a new ADR/reference update.

OMP itself is a continuously learning system.

Every optimization decision
must later be evaluated
against the real outcome.

OMP is allowed to improve
its future prioritization
using only real historical evidence.

## 26. Current Volatile State Pointer

Classification: `CURRENT_PROGRAM_STATE_REFERENCE`.
Authoritative owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `CPS_ONLY`
Execution Authority: `NONE`
Resolved current stop: `EXTERNAL_OWNER_REQUIRED`
Resolved current next action: `WAITING_INPUT:STAGE_48_EXISTING_OWNER_ADMISSION`
Current terminal report: `docs/reports/engineering/2026-08-03_233500_final_performance_closure_before_stage48.md`
Latest consumed report: `docs/reports/engineering/2026-08-03_233500_final_performance_closure_before_stage48.md`
Previous admitted continuation report: `docs/reports/engineering/2026-07-25_112500_l7_repair_generation_v6_preflight_and_admission.md`
Previous consumed report: `docs/reports/engineering/2026-08-02_141500_stage_25_exact_receipt_and_fastest_safe_path.md`
Authoritative transition input report: `docs/reports/engineering/2026-07-11_225321_operation_scoped_binding_atomic_snapshot_closure_v3.md`

Current volatile state lives in:

`docs/programs/V7_CURRENT_PROGRAM_STATE.md`

That file owns the current bottleneck, HLA, normalized authority class, reality limit, metrics, ephemeral packet state, stop reason, and policy boundary.

OMP owns the scheduler and optimizer rules.

OMP also owns the permanent production maturity ladder, implementation loop, authority evaluation rule, continuous optimization rule, and research-to-implementation gate.

When packet fields, metrics, or stop reason change, update `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.

Update OMP only when scheduler/optimizer meaning changes.

Before selecting any next capability or Mission, OMP must consume:

`CPS -> Authoritative Unfinished Capability Closure Registry`.

OMP must preserve protected active WIP first, select from the registry's unfinished deterministic sequence, and rerun reconciliation after every capability closure, legal stop, authority decision, production outcome, certification, owner revalidation, or accepted Candidate change. Historical OMP snapshots must never be used as current capability state. Capability details and percentages remain in CPS and their existing canonical owners, not in OMP.

## 27. Permanent Production Command Verdict

V7 can continue production evolution using only:

1. `Continue OMP`;
2. `Status`;
3. `Approve authority expansion`.

Candidate, packet, hash, decision and operation approval are not operator commands inside the approved bounded one-user policy.

No additional roadmap document is required.

This remains true unless a real implementation proves `FUNDAMENTAL_ARCHITECTURE_GAP`.

## 28. Runtime Capability Maturation Program / RT Phase 2

Status: `DISCOVERED_VALIDATED_REFINED_NOT_IMPLEMENTED`.

Canonical name:

```text
Runtime Capability Maturation Program
```

Alias:

```text
RT Phase 2
```

Purpose:
Mature existing runtime capabilities through OMP without creating a new Runtime, Planner, World Model, Truth Source, Owner, Backlog, roadmap, dashboard authority, queue daemon, or automation path.

Historical execution order snapshot:

```text
A5 -> A6 -> B13 -> B16 -> Runtime Capability Maturation Program
```

RT2 execution must not begin until OMP proves all entry criteria below.
The entry chain is complete or explicitly scoped through A5/A6/B13/B16. RT2-S1 through RT2-S6 are complete as read-only/advisory owner-mapped surfaces. RT2 produced an owner-mapped recommendation to return OMP to existing backlog item `B1_AGGREGATE_LIVENESS_EVIDENCE_BY_SOURCE_FAMILY_AND_CONFIDENCE`.

### 28.1 Entry Criteria

| Criterion | Required state |
| --- | --- |
| A5 | Class-level blast-radius evidence beyond one-user guard complete. |
| A6 | Runtime eligibility arbitration complete. |
| B13 | Metric reliability for promotion recommendations certified. |
| B16 | Automatic rollback authority after reliable verification evidence certified or explicitly scoped. |
| Runtime automation | Still disabled until explicit authority/certification exists. |
| Authority | No silent expansion; required class/policy/blast authority explicitly approved. |
| Measurement readiness | Runtime cost and reaction-latency measurement owners available through existing read models. |
| Safety readiness | Freshness, authority, verification, rollback, blast radius, anti-flap, and STOP_SAFE gates preserved. |
| Owner reuse | Existing owners cover the work; Need New Owner remains `FALSE`. |

### 28.2 Stop Conditions

RT2 must stop at the existing OMP stop conditions:

1. `OPERATIONAL_AUTHORITY`
2. `ENGINEERING_AUTHORITY`
3. `REAL_WORLD_LIMIT`
4. `UNSAFE_IMPLEMENTATION`
5. `FUNDAMENTAL_ARCHITECTURE_GAP`

Additional RT2-specific stop rules:

- stop if a workstream requires a new runtime/planner/truth-source/owner before reuse is proven impossible;
- stop if a queue, dashboard, desired-state artifact, latency metric, or improvement recommendation starts granting authority;
- stop if automation, concurrency, blast-radius expansion, or runtime behavior change is requested without certification and explicit authority;
- stop if evidence is synthetic or not tied to observed outcomes.

### 28.3 Workstreams

| Workstream | Purpose | Existing owners | Inputs | Outputs | Consumers | Completion criteria | Safety gates | Evidence requirements | Report requirements | Canonical promotion rule | Next OMP step |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `RT2-S1` Measurement & Observability Foundation | Make runtime cost, runtime time, reaction latency, stop reasons, lifecycle, wait states, dependency topology, Time-To-Safe-Recovery, and bottlenecks visible without hot-path cost. | OMP, Runtime Model, `admin_core/runtime_read_views.py`, `admin_core/operator_execution_pipeline.py`, `admin/v7-admin-api`, `admin_core/autonomy_trust_acceleration.py`. | Execution contracts, events, planner durations, read models, CPS, truth/convergence, existing timestamps, duration fields, latency fields, and blocker/wait reasons. | Read-only measurement, topology explanation, and dashboard payloads. Current implementation surface: `rt2_s1_measurement_observability_foundation`. | OMP, Engineering Reports, Runtime Model, Production Maturity, operator dashboards as read-only surfaces. | `DONE_READ_ONLY`; required latency/cost/time/topology fields are visible or explicitly marked missing with owner. | Dashboard/read model cannot decide, approve, rank execution, certify, or mutate. | Existing event/contract/read-model fields; no synthetic metrics. | Engineering report with Latency Impact, Work Placement, Runtime Cost Review, and Time Topology owner mapping when applicable. | Durable measurement semantics go to Runtime Model/OMP; UI field meaning goes to SYSTEM_MAP only if ownership changes. | `RT2-S2` is unlocked; S3+ remain blocked until S2 evidence exists. |
| `RT2-S2` World & Readiness Maturation | Mature prepared world/readiness state for runtime consumption. | World Model Plane, `admin_core/intelligence_snapshots.py`, `admin_core/intelligence_workers.py`, `admin_core/runtime_read_views.py`, `tools/v7-users-autoswitch`, `admin_core/operator_decision_surface.py`. | Observation, snapshots, freshness, service matrix, quality compact, user/channel/policy state. | Fresh/bounded prepared state and readiness summaries. Current implementation surface: `rt2_s2_world_readiness_maturation`. | Runtime consumption contract, planner/autoswitch owners, decision surface, OMP readiness review. | `DONE_READ_ONLY`; Runtime can consume compact state as READY/STOP; live gates remain live. | Prepared state cannot approve movement or authority. | Freshness and source hashes from existing owners. | Report freshness/readiness owners and stale behavior. | Durable state semantics to Runtime Model; ownership lookup to SYSTEM_MAP. | `RT2-S3` is unlocked; S4+ remain blocked until S3 evidence exists. |
| `RT2-S3` Desired-State Delta Preparedness | Prepare bounded deltas from current state toward Desired Safe State through existing planner owners. | Product Specification, policies, Decision Model, Runtime Model, `tools/v7-users-autoswitch`, `admin_core/operator_decision_surface.py`, OMP. | Business Objectives, policies, current state, action-class certification, movement protection. | Advisory desired-state delta / prepared plan. Current implementation surface: `rt2_s3_desired_state_delta_preparedness`. | Existing planner/autoswitch, packet/preview owners, Runtime live-gate validation, OMP. | `DONE_READ_ONLY`; delta is bounded, explainable, owner-mapped, and non-authorizing. | Desired State cannot become authority, planner, or runtime mutation. | Decision freshness, policy basis, gate status, real outcome requirements. | Report decision semantics and owner reuse. | Decision semantics to Decision Model; execution rules remain Runtime/OMP. | `RT2-S4` is unlocked; S5+ remain blocked until S4 evidence exists. |
| `RT2-S4` Governed Execution Coordination | Mature the bounded decision-to-terminal-outcome path. | `admin_core/operator_execution.py`, `admin_core/operator_execution_pipeline.py`, `tools/v7-governed-canary-dry-run-cycle`, `tools/v7-users-autoswitch`, `admin_core/operator_execution_feedback.py`. | Prepared plan, packet, lease, restore barrier, verification plan, rollback/no-rollback state. | Idempotent governed execution coordination and terminal classification. Current implementation surface: `rt2_s4_governed_execution_coordination`. | Feedback/learning owners, OMP, CPS, Runtime Model execution contract. | `DONE_READ_ONLY`; one bounded action path is owner-mapped from packet/recheck/restore/apply/verify/rollback/feedback/closure without stale loops or new execution path. | Queue is not created; every live action would still revalidate gates and require explicit authority. | Lease, packet identity, verification, rollback/no-rollback, feedback, terminal classification. | Report terminal state, STOP_SAFE, rollback and learning paths. | Durable execution contract to Runtime Model/OMP; no new execution path. | `RT2-S5` is unlocked; S6+ remain blocked until S5 evidence exists. |
| `RT2-S5` Certified Concurrency Ladder | Certify safe levels beyond one action only when evidence supports it. | OMP, action-class ladder, Policy 006, A5/A6/B13/B16 owners, `tools/v7-users-autoswitch`, `admin_core/autonomy_trust_acceleration.py`. | Blast-radius evidence, rollback capacity, verification capacity, policy scope, authority envelope, anti-flap state. | Certified concurrency level or STOP_SAFE. Current implementation surface: `build_rt2_s5_certified_concurrency_ladder`. | Runtime execution owners, authority model, CPS, Production Maturity, operator approval surface. | `DONE_READ_ONLY`; current certified level is `SERIAL_ONLY_READ_ONLY`, wider levels are explicit `STOP_SAFE`, and no silent blast expansion exists. | Parallelism is safety certification, not performance optimization; concurrency enablement remains forbidden without explicit authority. | Real outcomes, capacity/load, rollback, verification, metric reliability, authority. | Report class, level, proof, limits, and stop condition. | Certification results go through OMP/Current Program State; no backlog fork. | `RT2-S6` is unlocked; runtime apply/concurrency enablement remain blocked. |
| `RT2-S6` Evidence-Based Continuous Improvement | Convert measured evidence into OMP-owned recommendations, including Runtime Time Intelligence recommendations that reduce safe recovery time. | OMP, Backlog, Production Maturity Model, Engineering Reports, Research Framework/Process, Canonical Reference, `admin_core/autonomy_trust_acceleration.py`. | Outcomes, reports, latency/cost/time/topology data, fit analysis, maturity gaps, RT2-S5 safe execution limits. | Owner-mapped recommendations or explicit no-change verdict. Current implementation surface: `build_rt2_s6_evidence_based_continuous_improvement`. | OMP optimizer, Backlog, Canonical Reference, Research Framework, Current Program State. | `DONE_READ_ONLY`; recommendation is owner-mapped to existing backlog item `B1` and remains advisory. | Recommendations cannot mutate runtime, expand authority, lower gates, create synthetic evidence, convert latency metrics into authority, or start direct implementation. | Real evidence, fit analysis, Product Evolution Review, Work Placement Review, Safety/Authority/Verification/Rollback/STOP_SAFE review. | Report recommendation, owner, safety, latency/cost/time impact, and canonical update. | Durable conclusions promoted to canonical owner; reports remain historical evidence only. | Return to existing backlog item `B1`. |

Every RT2 workstream executes the same OMP engineering lifecycle:

```text
Resolve current workstream
  -> consume canonical knowledge and research inventory
  -> verify existing implementation and owner coverage
  -> reuse existing owner if sufficient
  -> extend existing owner only when evidence proves a gap
  -> implement only the minimal safe change allowed by current authority
  -> verify tests, truth, convergence, safety, latency, cost, freshness, rollback, and STOP_SAFE
  -> create Engineering Report
  -> promote durable conclusions through canonical owner update
  -> update Current Program State when state changes
  -> continue next RT2 workstream or graduate
```

### 28.4 Old RT2 Mapping

The old RT2.1-RT2.12 proposal is superseded as an active roadmap.
Its content is preserved only as absorbed responsibilities:

| Old item | Canonical workstream |
| --- | --- |
| RT2.1 Continuous World Model | `RT2-S2` |
| RT2.2 Continuous Readiness | `RT2-S2` |
| RT2.3 Desired State Engine | `RT2-S3` |
| RT2.4 Continuous Planning | `RT2-S3` |
| RT2.5 Execution Orchestration | `RT2-S4` |
| RT2.6 Safe Execution Queue | `RT2-S4` as queue feasibility only |
| RT2.7 Bounded Parallelism | `RT2-S5` |
| RT2.8 Runtime Cost Intelligence | `RT2-S1` |
| RT2.9 Runtime Intelligence / Latency Intelligence | `RT2-S1` |
| RT2.10 Runtime Evolution Engine | `RT2-S6` |
| RT2.11 Runtime Performance Dashboard | `RT2-S1` as read-only consumer |
| RT2.12 Continuous Runtime Evolution Framework | `RT2-S6` |

### 28.4.1 Runtime Time Intelligence Placement

Runtime Time Intelligence fits existing RT2 architecture.
It does not create a new Runtime, Planner, Owner, Truth Source, roadmap, or automation mode.

Placement:

| Capability | Canonical placement | Rule |
| --- | --- | --- |
| Runtime Time Model | Runtime Model + `RT2-S1` | Defines time domains as read-only measurement categories. |
| Time Topology | Runtime Model + `RT2-S1` | Explains why time is spent by mapping waits/dependencies to existing owners. |
| Time Domains | Runtime Model | Observation, World Update, Readiness, Planning, Decision, Execution Wait, Execution, Verification, Rollback, Learning, Engineering Report, Canonical Update, and OMP Progress Time. |
| Recommendation Model | `RT2-S6` | Recommends move-earlier, remove-duplicate, reduce-blocking, reduce-waiting, reduce-cost, or reduce-latency changes only through existing owners. |
| Time/Latency/Cost read models | Existing read-model/admin/runtime owners under `RT2-S1` | Read-only evidence; no decision authority or truth-source promotion. |

All Runtime Time Intelligence work must preserve Safety, Authority, Verification, Rollback, and `STOP_SAFE`.
If a proposed time optimization requires new authority, runtime behavior, queue behavior, or user movement, OMP stops and maps the gap before implementation.

### 28.4.2 Runtime Time Intelligence Capability Maturation

Status: `CANONICALIZED_INSIDE_RT2`.

Runtime Time Intelligence matures only inside `RT2-S1` and `RT2-S6`.
It is not a new phase, roadmap, owner, planner, runtime, truth source, dashboard authority, or implementation queue.

| Level | Maturity capability | RT2 owner | OMP rule |
| --- | --- | --- | --- |
| 1 | Time Measurement | `RT2-S1` | Measure or mark missing with owner. |
| 2 | Time Domains | `RT2-S1` + Runtime Model | Map each field to one canonical domain. |
| 3 | Time Topology | `RT2-S1` + Runtime Model | Explain dependency/wait cause without ranking or approval. |
| 4 | Critical Path | `RT2-S1` | Identify longest safe-recovery path or missing evidence. |
| 5 | Time Budget | Runtime Model + OMP/Production Maturity | Categorize budgets without unsafe numeric gates. |
| 6 | Dependency Weight | `RT2-S1` evidence + `RT2-S6` use | Estimate bottleneck contribution with uncertainty. |
| 7 | Impact Prediction | `RT2-S6` | Predict effect only as advisory engineering evidence. |
| 8 | Engineering Recommendation | `RT2-S6` | Produce owner-mapped recommendation/no-change verdict. |
| 9 | Certification | OMP + Production Maturity + relevant owner | Certify implemented change only after separate implementation approval. |
| 10 | Continuous Runtime Optimization Recommendation Loop | `RT2-S6` + Learning owners | Feed certified measurements back into future recommendations; Runtime never self-optimizes. |

Required lifecycle:

```text
Measurement
  -> domains
  -> topology
  -> critical path
  -> budget category
  -> dependency weight
  -> impact prediction
  -> engineering recommendation
  -> OMP/backlog/canonical owner
  -> implementation only after separate approval
  -> certification
  -> measured learning
  -> future recommendation or no-change
```

Every level must produce an Engineering Report when it changes durable knowledge, owner mapping, certification state, or future implementation placement.
No level may change Runtime behavior, authority, safety gates, verification, rollback, `STOP_SAFE`, users, or automation.

### 28.5 RT2 Continue OMP Loop

When OMP reaches RT2, it must execute:

```text
Resolve current RT2 workstream
  -> consume Research Framework / canonical owners
  -> verify existing implementation
  -> reuse or extend existing owner
  -> implement minimal safe change
  -> verify tests / truth / convergence / safety
  -> create Engineering Report
  -> promote durable knowledge to canonical owner when needed
  -> update Current Program State
  -> continue next workstream or graduate
```

Unfinished RT2 work must be resumed, closed, or explicitly deferred by OMP before unrelated new work is selected.

### 28.6 External Model Loop

External runtime/control-plane practices enter V7 only through:

```text
Research Framework / Research Process
  -> research inventory inside existing research owner
  -> V7 Fit Analysis
  -> Work Placement Review
  -> Safety / Authority / Verification / Rollback / Freshness Review
  -> canonical owner or backlog mapping only if applicable
```

External models never override V7 architecture directly.
Vendor-specific mechanisms are examples, not authority.
Research may update OMP only when scheduler or optimizer meaning changes.

### 28.7 Graduation Criteria

RT2 graduates when all six workstreams are complete, explicitly deferred with safety reason, or marked not applicable by OMP, and Runtime can:

- consume prepared world/readiness/desired-state/planning knowledge;
- perform only live validation, bounded mutation, verification, rollback/STOP_SAFE, and outcome collection;
- expose runtime cost/reaction latency/stop reason visibility through read models;
- coordinate bounded certified execution through existing owners;
- feed real outcomes back into OMP without creating new architecture.

No `RT3` program is created by default.
Future runtime improvement after graduation proceeds through Product Evolution Review, Engineering Review, OMP, Backlog, production evidence, certification, and explicit authority where required.

### 28.8 Historical RT2 Status Snapshot

Classification: `HISTORICAL_SNAPSHOT`.

Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

Live RT2 / runtime capability state is resolved only from `docs/programs/V7_CURRENT_PROGRAM_STATE.md` and current owner evidence.

RT2 Program Integration: `CANONICALIZED_DOCS_ONLY`.

RT2 implementation: `FUTURE_NOT_ACTIVE`.

Current practical next OMP step: `A5_CERTIFY_CLASS_LEVEL_BLAST_RADIUS_EVIDENCE_BEYOND_ONE_USER_GUARD`.

## 29. Master OMP Completeness Certification

Status: `MASTER_2_COMPLETE`.

Purpose:
Certify OMP as the only long-term execution program of V7.

This section does not create a new roadmap, master program, runtime, planner, owner, truth source, phase, automation path, authority path, or implementation queue.

OMP remains the operating system of V7 development:

```text
Future capability
  -> Engineering Context Resolver
  -> Knowledge Plane
  -> OMP placement
  -> existing owner / backlog / canonical owner
  -> implementation or audit only when required
  -> verification / certification
  -> Engineering Report
  -> Canonical Update
  -> Current Program State
  -> next OMP step
```

### 29.1 Future Capability Coverage

Every future capability class must enter through the existing OMP path below.

| Future activity | OMP entry | Existing owner destination | Canonical destination | Completion evidence |
| --- | --- | --- | --- | --- |
| Runtime evolution | RT2 / Runtime Eligibility / Authority Evolution | Runtime Model, existing runtime owners, Backlog | Runtime Model, OMP, CPS | Tests, truth/convergence, safety, authority, Engineering Report |
| Routing evolution | Movement Protection / Routing capability backlog | Autoswitch/planner, policies, service matrix owners | OMP, SYSTEM_MAP, policies | Real outcomes, rollback/verification, production evidence |
| Research / world practices | Research integration gate | Research Framework / Research Process | Canonical owner or OMP only if durable | Fit Analysis, Work Placement, Safety Review, Engineering Report |
| Product evolution | Product Evolution Review | Product Specification, OMP, Backlog | Product Specification, Canonical Reference | Business Objective mapping and certification review |
| Runtime optimization | Continuous optimization / RT2 | Runtime Model, read models, existing runtime owners | Runtime Model or OMP | Runtime cost, latency, safety, no live gate bypass |
| Latency optimization | Runtime Latency Review | Runtime Model, Work Placement owners | Runtime Model / OMP | Latency Impact and measurement owner |
| Runtime cost optimization | Product Evolution Review / RT2-S1 | Runtime Model, Production Maturity, read models | Runtime Model / Production Maturity | Cost dimension evidence and report |
| Decision evolution | Decision Lifecycle / Decision Explainability | Decision Model, decision surface, planner owners | Decision Model / OMP | Freshness, lifecycle, authority separation |
| Policy evolution | Policy library to OMP gate | Canonical Policy Library, Backlog, Runtime gates | Policies, OMP, Canonical Reference | Policy fit, interaction audit, certification |
| UX evolution | Business Operator Experience / Decision Explainability | Product Specification, UI/read-model owners, OMP | Product Specification / SYSTEM_MAP if ownership changes | Operator evidence, no truth-source promotion |
| Dashboard evolution | Observability / read-model discipline | Admin read models, OMP, Runtime Model | SYSTEM_MAP only if owner meaning changes | Read-only evidence, no authority |
| Read-model evolution | Observability / Knowledge System | Existing read-model owners | SYSTEM_MAP / Canonical Reference if durable | Scale, freshness, truth consistency |
| Observability | Observability capability | Admin read models, truth/convergence, evidence inventory | OMP / SYSTEM_MAP | Read-only safety evidence coverage |
| Deployment | Production Readiness | Safe deploy, truth/convergence, production owners | CPS, Production Maturity | Deploy verification and no unapproved mutation |
| Certification | Certification workflow | OMP, policies, action-class owners | CPS, Production Maturity, Canonical Reference | Mandatory/supporting evidence closed |
| Production maturity | Production Maturity ladder | Production Maturity Model, Backlog, CPS | CPS / Production Maturity Model | Score recalculation from real state |
| Operator workflow | Decision Explainability / Operator Responsibility | Product Specification, UI/read-model owners, OMP | Product Specification / Canonical Reference | Russian explanation, risk/value/evidence |
| AI-assisted engineering | ECR / Knowledge Plane / Continue OMP | Kernel, Context Resolver, OMP, reports | OMP / Canonical Reference if durable | Existing-owner mapping and report |
| Future protocols | Architecture Closed by Default / Movement Protection | Policies, Runtime Model, routing owners, Backlog | Policies / Runtime Model / SYSTEM_MAP | Reuse proof, certification, production evidence |
| Future routing methods | Movement Protection / Routing evolution | Autoswitch/planner, policy, service matrix owners | OMP / SYSTEM_MAP / policies | Safety gates, rollback, verification, outcomes |
| Capability change / merge / split / deprecation / retirement | Product Evolution Review / Capability state | Owning capability, Backlog, CPS | OMP / CPS / Canonical Reference | Consumer inventory, ownership review, safety and rollback review |

If a future activity cannot be mapped to this table, OMP must run Architecture Closed by Default before proposing any new owner or roadmap.

Capability lifecycle state changes use this same table.
Changing, merging, splitting, deprecating, or retiring a capability is normal Product Execution work when the existing owner, consumer inventory, evidence, report, canonical update, CPS update, and next OMP step are clear.
If any of those are unclear, OMP stops at owner/evidence discovery before architecture is reopened.

### 29.2 Growth Readiness

OMP may grow for years only by extending existing owner sections.

Forbidden growth patterns:

- duplicate roadmap;
- duplicate OMP;
- duplicate capability program;
- nested master program;
- repeated stage sequence with a new name;
- dead stage without owner, evidence, report, and canonical destination;
- parallel implementation queue;
- report-only truth;
- dashboard authority;
- research-driven runtime change without OMP placement.

Allowed growth patterns:

- add a row to an existing capability table;
- extend an existing owner contract;
- add backlog mapping through OMP;
- promote durable report findings to canonical owners;
- update CPS for volatile state;
- retire or deprecate capability wording when no live consumer remains.

### 29.3 OMP Engineering Language

Canonical OMP vocabulary for future work:

| Term | Meaning |
| --- | --- |
| Discovery | Find current reality and existing owners. |
| Behaviour Discovery | BDP-owned discovery of observed Behaviour, Automation Readiness, Intent Closure, Automation Breaks, Implementation Candidates, and Engineering Logic Coverage. OMP consumes accepted outputs only. |
| Research | Collect mature outside practice through Research Framework. |
| Fit Analysis | Compare research to V7 constraints, owners, product intent, and safety. |
| Reuse | Use existing owner without new architecture. |
| Extension | Add capability to an existing owner when reuse is insufficient. |
| Implementation Candidate | Certified BDP implementation input that OMP may admit, hold, reject, or mark not applicable. It is not a queue, backlog, owner, or mission. |
| Implementation Candidate Class | Reusable engineering problem pattern shared by one or more Candidate Instances. A Class alone never becomes a Mission. |
| Implementation Candidate Instance | Concrete engineering situation identified by intent, break, affected Behaviour/capability/owner/consumer, state, scope, evidence, runtime, verification, rollback, authority, and policy context. This is the OMP admission unit. |
| Candidate Merge | OMP evidence consolidation for the same Candidate Instance. It preserves all provenance and does not merge separate real situations. |
| Cohort Mission | One OMP Mission that safely handles multiple compatible Candidate Instances only when intent, break, owner, consumer, verification, rollback, authority, policy, runtime, and blast radius are compatible. |
| OMP Mission | OMP-admitted implementation unit with owner, intent, dependencies, authority, verification, rollback, Runtime, production, Codex handoff, and terminal state. |
| Mission Identity | OMP execution identity derived from one Candidate Instance or one safe Cohort Mission; used to prevent duplicate active Missions. |
| Automation Break | BDP evidence that existing logic stops before its engineering intent is achieved. It is not a certified Gap or OMP mission until OMP admits implementation work. |
| Implementation | Change existing code/doc owner only after OMP placement. |
| Verification | Prove behavior, truth, convergence, safety, and no unintended mutation. |
| Certification | Close required evidence for capability, policy, action class, or maturity. |
| Production | Real deployed/runtime state and observed outcomes. |
| Learning | Feed real outcomes into existing evidence and OMP owners. |
| Engineering Report | Historical evidence saved after meaningful action. |
| Canonical Update | Durable knowledge promoted from reports to existing canonical owner. |
| Current Program State | Volatile current bottleneck, task, authority, metrics, and stop reason. |
| Product Evolution | Product Review -> OMP -> Backlog/canonical owner update. |
| Retirement | Mark a capability path complete, superseded, or no longer active. |
| Deprecation | Remove active recommendation status while preserving history. |

### 29.4 Self-Evolution Rule

OMP improves only through:

```text
Engineering Report
  -> durable conclusion extracted
  -> Canonical Update
  -> Current Program State when state changes
  -> next OMP step
  -> future Engineering Report
```

Reports may trigger OMP improvement, but reports never become OMP, backlog, roadmap, truth source, or owner.

OMP update is required only when scheduler, optimizer, capability, command, stop condition, maturity, or canonical placement semantics change.

### 29.5 Completeness Verdict

OMP completeness score: `100 / 100`.

Architecture completeness score inside OMP: `100 / 100`.

Growth readiness: `READY`.

Future evolution readiness: `READY_THROUGH_EXISTING_OMP`.

No second roadmap is justified.
No parallel capability program is justified.
No MASTER 3 was started by this certification at that time.

Historical practical implementation next step at that time:

```text
A5_CERTIFY_CLASS_LEVEL_BLAST_RADIUS_EVIDENCE_BEYOND_ONE_USER_GUARD
```

## 30. OMP Resilience Certification / Master 3

Status: `MASTER_3_COMPLETE`.

Purpose:
Record the destructive stress test of OMP.

MASTER 3 does not create a new canonicalization layer, integration layer, roadmap, master program, runtime, planner, owner, truth source, automation path, authority path, or capability program.

### 30.1 Stress Test Results

| Test | Break attempt | Result | Required invariant |
| --- | --- | --- | --- |
| Duplicate Test | Split OMP into another roadmap/program or duplicate capability flow. | `FAILED_TO_BREAK`; duplicate would create conflicting scheduler/queue/authority. | OMP remains the only execution program; Backlog remains the only post-admission implementation registry. |
| Dependency Test | Remove ECR, Knowledge Plane, Backlog, Runtime Model, Decision Model, SYSTEM_MAP, Canonical Reference, CPS, reports, or truth/convergence. | `FAILED_TO_BREAK`; each removal loses placement, owner, state, evidence, or verification. | Dependencies are mandatory by task class and loaded through ECR. |
| Completion Criteria Test | Mark stages complete without criteria. | `FAILED_TO_BREAK`; stage remains incomplete without owner, evidence, report, and canonical destination. | Every stage needs objective completion criteria. |
| Evidence Test | Execute stages without evidence. | `FAILED_TO_BREAK`; OMP stops at safety, authority, certification, or real-world limit. | No evidence means no certification or authority promotion. |
| Owner Test | Remove owners from stages. | `FAILED_TO_BREAK`; responsibility becomes ambiguous. | Every stage maps to existing owner, existing backlog, or canonical owner. |
| Engineering Report Test | Remove reports. | `FAILED_TO_BREAK`; history, why, safety, and verification context are lost. | Every meaningful action creates a report. |
| Canonical Update Test | Remove canonical updates. | `FAILED_TO_BREAK`; durable knowledge stays trapped in history. | Durable findings must be promoted to existing canonical owners. |
| Capability Injection Test | Inject future capabilities. | `PASSED`; all tested capabilities enter OMP through existing placement. | New capability starts with ECR -> OMP placement -> existing owner. |
| Evolution Pressure Test | Run V7 for 1/3/5/10 years. | `PASSED_WITH_INVARIANT`; pressure to create OMP2/Roadmap2 is blocked. | Extend existing OMP sections; never create parallel program. |
| Growth Test | Simplify, merge, remove, shorten. | `NO_SAFE_SIMPLIFICATION_FOUND`; removal loses owner/evidence/report/canonical/state function. | Growth by rows and owner extensions only. |
| Failure Test | Remove one master, capability, lifecycle, owner, criterion, or flow. | `FAILED_TO_BREAK`; each removal loses a required invariant. | No required invariant may be optionalized. |
| Architecture Pressure Test | Invent future architecture. | `PASSED`; proposed architecture must map to existing OMP or stop at Architecture Closed by Default. | New architecture is last resort after impossible reuse proof. |
| Self-Evolution Test | Remove Engineering Report -> Canonical Update -> CPS -> next OMP step -> future report loop. | `FAILED_TO_BREAK`; OMP stops learning and future work rediscovers history. | OMP self-evolves only through report, canonical promotion, CPS update, and next OMP step. |
| Knowledge Preservation Test | Leave durable knowledge only in reports, audits, research, or implementation notes. | `FAILED_TO_BREAK`; future agents lose durable truth or treat history as current truth. | Durable conclusions must have a canonical destination before closure. |

### 30.2 Required Resilience Invariants

OMP is resilient only while all invariants remain true:

1. OMP is the only long-term execution program.
2. Implementation Backlog is the only post-admission implementation registry; BDP Implementation Candidate Catalogue is an input, not a queue.
3. Current Program State owns volatile current state.
4. Canonical Reference and SYSTEM_MAP own durable truth and owner lookup.
5. Engineering Reports are historical evidence only and mandatory after meaningful work.
6. Durable findings never remain only in reports.
7. Every stage has owner, completion criteria, evidence, engineering report, and canonical destination.
8. Runtime remains thin; OMP never authorizes runtime behavior without certification and explicit authority.
9. Research cannot bypass Fit Analysis, Work Placement, owner mapping, and OMP.
10. Dashboard, UX, read model, telemetry, and AI assistance never become truth source or authority.
11. Retirement and deprecation preserve history and require no live consumer plus safety review.
12. Any unmappable future capability stops at Architecture Closed by Default.

### 30.3 Capability Injection Matrix

| Injected future capability | OMP entry | Existing owner | Production path | Canonical path |
| --- | --- | --- | --- | --- |
| New routing protocol | Future protocols / Movement Protection | Policies, Runtime Model, autoswitch/planner, Backlog | Certification, rollback, verification, real outcomes | Policies / Runtime Model / SYSTEM_MAP |
| New VPN protocol | Future protocols / Product Evolution Review | Product Specification, policies, service matrix, routing owners | Backlog, safe deploy, truth/convergence, production evidence | Product Specification / policies / SYSTEM_MAP |
| New transport | Future protocols / Product Evolution Review | Product Specification, policies, Runtime Model, routing owners | Backlog, compatibility tests, verification, production evidence | Product Specification / Runtime Model / SYSTEM_MAP |
| New telemetry | Observability / read-model discipline | Admin read models, evidence inventory, Runtime Model | Read-only rollout, truth consistency, no authority | SYSTEM_MAP / Runtime Model if semantics change |
| New runtime optimization | Continuous optimization / RT2 | Runtime Model, existing runtime/read-model owners | Tests, latency/cost review, no live gate bypass | Runtime Model / OMP |
| New latency optimization | Runtime Latency Review / Work Placement | Runtime Model, Work Placement owners, OMP | Measurement plan, tests, no live safety bypass | Runtime Model / OMP |
| New Runtime Cost optimization | Runtime Cost Review / Product Evolution Review | Runtime Model, Production Maturity, read-model owners | Cost evidence, safety review, no authority expansion | Runtime Model / Production Maturity |
| New dashboard | Observability / Dashboard evolution | Admin API/read-model owners, OMP | Read-only UI/API, no decision authority | SYSTEM_MAP only if owner meaning changes |
| New UX | Business Operator Experience / Decision Explainability | Product Specification, UI/read-model owners | Operator validation, evidence-linked explanation | Product Specification / Canonical Reference |
| New AI subsystem | AI-assisted engineering / ECR | Kernel, Context Resolver, OMP, Research Framework | Advisory use only, report, no authority | OMP / Canonical Reference if durable |
| New policy | Policy evolution | Canonical Policy Library, Research Framework, OMP | Fit Analysis, interaction audit, backlog/certification | Policies / OMP / Canonical Reference |
| New routing algorithm | Routing evolution | Autoswitch/planner, policies, service matrix | Backlog, tests, rollback/verification, outcomes | OMP / SYSTEM_MAP / policies |
| New verification | Certification workflow | Verification owners, truth/convergence, Runtime Model | Evidence validation before certification | Runtime Model / OMP / SYSTEM_MAP |
| New rollback strategy | Rollback / Movement Protection | Restore barrier, rollback owners, Runtime Model | Governed proof, rollback/no-rollback evidence | Runtime Model / policies / SYSTEM_MAP |
| New deployment model | Production Readiness | Safe deploy, truth/convergence, Production Maturity | Deploy verification, no unapproved mutation | CPS / Production Maturity / Canonical Reference |
| New observability source | Observability / Knowledge System | Read-model/evidence owners, SYSTEM_MAP | Read-only evidence, freshness and source validation | SYSTEM_MAP / Canonical Reference |
| New Research result | Research integration gate | Research Framework, Research Process, OMP | Fit Analysis, owner mapping, implementation only through OMP Mission admission if required | Canonical owner / OMP only when durable |
| New Client capability | Product Evolution Review / Business Operator Experience | Product Specification, policies, UI/read-model/routing owners | Backlog, tests, operator validation, production evidence | Product Specification / SYSTEM_MAP / Canonical Reference |
| New Server capability | Product Evolution Review / Production Readiness | Product Specification, Runtime Model, deploy/runtime owners | Backlog, tests, safe deploy, truth/convergence | Runtime Model / SYSTEM_MAP / Production Maturity |

### 30.4 Growth Pressure Verdict

For 1 year, 3 years, 5 years, and 10 years, OMP must resist creation of `OMP2`, `Roadmap2`, a new master program, or a new capability program.

The correct growth action is:

```text
Extend existing OMP section
  -> map to existing owner
  -> admit Mission through OMP when implementation is required
  -> report
  -> canonical update
  -> Current Program State
```

If this path cannot hold a future capability, OMP must stop at `FUNDAMENTAL_ARCHITECTURE_GAP`; it must not silently create parallel structure.

### 30.4.1 Failure Injection Results

| Removed item | What breaks |
| --- | --- |
| One MASTER conclusion | Closure chain loses proof that prior architecture/canonicalization/resilience work is complete. |
| One capability | Backlog-to-maturity mapping loses production purpose and progress visibility. |
| One lifecycle | Work can skip owner mapping, verification, report, canonical update, or CPS. |
| One owner | Responsibility becomes ambiguous and duplicate owners become tempting. |
| One completion criterion | Two engineers can close the same stage differently. |
| One engineering report | Historical reason, safety, evidence, and alternative analysis disappear. |
| One canonical update | Durable knowledge remains trapped in report/audit/research history. |
| One dependency | Context, placement, owner lookup, runtime semantics, decision semantics, state, or verification becomes unbounded. |

### 30.4.2 Architecture Pressure Results

Invented future architectures tested:

| Future architecture pressure | OMP result |
| --- | --- |
| Event-driven autonomous runtime expansion | Maps to Runtime Model, RT2, Authority Evolution, and explicit authority; no new runtime by default. |
| Multi-protocol routing substrate | Maps to Product Evolution, policies, Movement Protection, Runtime Model, and Backlog. |
| AI engineering assistant subsystem | Maps to ECR, Knowledge Plane, Research Framework, OMP, and reports as advisory-only. |
| New observability/control dashboard plane | Maps to Observability/read-model owners; dashboard cannot become truth or authority. |
| Distributed deployment model | Maps to Production Readiness, safe deploy, truth/convergence, CPS, and Production Maturity. |

No tested future architecture requires a new architecture proposal.

### 30.4.3 Knowledge Preservation Results

Durable knowledge must never remain only inside:

- Engineering Reports;
- audits;
- research;
- implementation notes;
- chat handoffs.

Required preservation path:

```text
Historical evidence
  -> durable conclusion extraction
  -> canonical owner update
  -> SYSTEM_MAP only if ownership/topology changes
  -> Current Program State only if volatile state changes
  -> OMP only if scheduler/optimizer/capability semantics change
```

### 30.5 Resilience Verdict

OMP resilience score: `100 / 100`.

OMP simplicity score: `100 / 100`.

OMP long-term evolution score: `100 / 100`.

Weaknesses found: `1`; stress-test invariants and injected-capability examples were implicit rather than explicit.

Improvements made: `1`; this section records destructive test results, required invariants, injection matrix, and growth pressure verdict.

Simplifications performed: `0`; no safe merge/removal preserved owner, evidence, report, canonical, and state invariants.

Merges performed: `0`; existing flows are layered responsibilities, not duplicates.

MASTER 4 later completed; this historical Master 3 section did not itself start it.

## 31. Architecture Graduation & Product Transition / Master 4

Status: `MASTER_4_COMPLETE`.

Purpose:
Certify that V7 architecture is complete and graduate V7 from Architecture Mode to Product Execution Mode.

MASTER 4 does not create a new roadmap, master program, runtime, planner, owner, truth source, capability program, implementation queue, automation path, authority path, or runtime behavior.

### 31.1 Architecture Graduation Certification

Architecture Graduation Score: `100 / 100`.

Graduation checks:

| Area | Verdict | Owner |
| --- | --- | --- |
| Runtime architecture | `COMPLETE` | Runtime Model |
| Decision architecture | `COMPLETE` | Decision Model |
| OMP | `COMPLETE` | OMP |
| Work Placement | `COMPLETE` | Runtime Model + OMP |
| RT2 integration | `COMPLETE_DOCS_ONLY` | OMP + Runtime Model |
| Capability ownership | `COMPLETE` | SYSTEM_MAP + OMP |
| Canonical ownership | `COMPLETE` | Canonical Reference + SYSTEM_MAP |
| Research flow | `COMPLETE` | Research Framework / Research Process |
| Knowledge preservation | `COMPLETE` | Canonical Reference + Document Lifecycle + OMP |

No architecture gap remains inside MASTER 4 scope.

### 31.2 Architecture Constitution

Architecture exists to preserve:

- Reality;
- Safety;
- Authority;
- Certification;
- Verification;
- Knowledge;
- Evolution.

Architecture does not own:

- backlog execution;
- runtime mutations;
- deployments;
- user movement;
- engineering tasks;
- implementation selection;
- production operations;
- engineering history.

Architecture is now closed by default.
It changes only when existing architecture cannot express a capability after complete owner, OMP, canonical, policy, runtime, decision, research, and backlog reuse review.

### 31.3 Architecture Change Protocol

Normal change path:

```text
Idea
  -> Existing Owner Check
  -> Reuse / Extend Existing Owner
  -> OMP
  -> Implementation only if approved and backlog-owned
  -> Verification
  -> Engineering Report
  -> Canonical Update
  -> Current Program State
  -> Continue OMP
```

Architecture proposal path:

```text
Existing architecture cannot express capability
  -> Architecture Proposal
  -> Discovery
  -> Validation
  -> OMP Integration
  -> Implementation only through existing or newly certified owner
```

Architecture changes must never bypass OMP, Engineering Report, Canonical Update, or Current Program State.

### 31.4 Capability Admission Rule

Every future capability must answer:

```text
Why can the existing owner not express this capability?
```

If the answer is missing, incomplete, speculative, implementation-convenience-only, or based on preference, new capability ownership is forbidden.

Default result:

```text
Need New Owner = FALSE
Need New Roadmap = FALSE
Need New Architecture = FALSE
```

Only a proven `FUNDAMENTAL_ARCHITECTURE_GAP` may change the default.

Engineering Review capability injection:

| Future capability | Existing entry | Existing owner destination |
| --- | --- | --- |
| Runtime Time Intelligence | `RT2-S1` / `RT2-S6` | Runtime Model, OMP, read-model owners, Production Maturity |
| Client Intelligence | Product Evolution Review / Client capability | Product Specification, UI/client/read-model owners, OMP |
| Future Routing | Movement Protection / routing evolution | Autoswitch/planner, policies, service matrix, Runtime Model |
| AI Engineering | ECR / Knowledge Plane / Research Framework | Kernel, Context Resolver, OMP, Research Framework, Canonical Reference if durable |
| Future Telemetry | Observability / read-model discipline | Admin read models, evidence inventory, Runtime Model, SYSTEM_MAP if ownership changes |
| Advanced Recovery | Recovery Admission / Rollback / Movement Protection | Restore barrier, rollback owners, Runtime Model, policies, OMP |
| New Dashboard | Observability / dashboard evolution | Admin API/read-model owners, OMP, SYSTEM_MAP if owner meaning changes |
| New Verification | Certification workflow | Verification owners, truth/convergence, Runtime Model, OMP |
| New Research | Research integration gate | Research Framework, Research Process, OMP, canonical owner if durable |

All injected examples enter existing architecture.
None justifies reopening architecture.

### 31.5 Knowledge Preservation Contract

Durable knowledge must never remain only inside:

- reports;
- audits;
- research;
- chats;
- implementation notes;
- handoff notes.

Every durable conclusion must have exactly one canonical owner.

Required preservation path:

```text
Historical evidence
  -> durable conclusion extraction
  -> exactly one canonical owner
  -> SYSTEM_MAP only if ownership/topology changes
  -> Current Program State only if volatile state changes
  -> OMP only if scheduler/optimizer/capability semantics change
```

Reports remain historical evidence.
Canonical owners preserve durable truth.

### 31.6 Product Execution Contract

Product Execution Mode is active after MASTER 4.

The only normal engineering workflow is:

```text
OMP
  -> admitted Mission from Implementation Backlog, existing owner, or BDP Implementation Candidate
  -> Codex when assigned by OMP/operator
  -> Verification
  -> Engineering Report
  -> Canonical Update
  -> Current Program State
  -> Continue OMP
```

No parallel workflow is allowed.
Future architecture work is exceptional and must pass Architecture Closed by Default first.

Capability lifecycle certification:

```text
Reality / AEP / BDP output or existing owner need
  -> Existing Owner Check
  -> Architecture Fit
  -> OMP Admission
  -> Capability Classification
  -> Owner Mapping
  -> Canonical Integration
  -> OMP Mission
  -> Codex when assigned by OMP/operator
  -> Implementation only after approval
  -> Verification / Certification
  -> Engineering Report
  -> Canonical Update
  -> Current Program State
  -> Continue OMP
```

Capability evolution, including measurement, topology, critical path, budget, recommendation, certification, optimization, change, merge, split, deprecation, and retirement, must reuse this same Product Execution workflow.

Governance mapping:

| Question | Existing answer |
| --- | --- |
| Who approves? | OMP / operator approval where authority is required. |
| Who owns? | Existing canonical owner identified by SYSTEM_MAP and OMP owner check. |
| Who implements? | Existing owner through an OMP Mission; Codex may assist only when assigned by OMP/operator. |
| Who certifies? | OMP, Production Maturity, policy/action-class owner, or affected canonical owner. |
| Who preserves knowledge? | Exactly one canonical owner; reports remain evidence. |
| Who updates Current Program State? | OMP through `docs/programs/V7_CURRENT_PROGRAM_STATE.md`. |
| Who continues work? | `Continue OMP`. |

No separate capability lifecycle, roadmap, owner, or master program is allowed.

### 31.7 Program Navigation

Separate `ARCHITECTURAL_INVARIANTS.md` and `PROGRAM_MAP.md` files are not created.

Existing navigation is sufficient:

| Navigation need | Existing owner |
| --- | --- |
| Architectural invariants | OMP, Canonical Reference, Runtime Model, Decision Model, Kernel |
| Program map | OMP, SYSTEM_MAP, Current Program State, Document Lifecycle |
| Document roles | SYSTEM_MAP + Document Lifecycle |
| Current execution state | Current Program State |
| Future capability routing | OMP + SYSTEM_MAP |

Future engineer navigation:

| Question | Destination |
| --- | --- |
| Where to implement? | OMP selects Implementation Backlog item or existing owner. |
| Where to document? | Engineering Report for evidence; canonical owner for durable conclusion. |
| Where to certify? | OMP, Production Maturity, policy/action-class owner, or affected canonical owner. |
| Where to report? | `docs/reports/engineering/` after meaningful work. |
| Where to preserve knowledge? | Exactly one canonical owner; SYSTEM_MAP only for ownership/topology; CPS only for volatile state. |
| Where to continue? | `Continue OMP`. |

Creating additional navigation files would duplicate existing owners.

### 31.8 Boundary Review

Architecture owns:

- laws;
- contracts;
- ownership;
- structure;
- evolution rules.

Architecture does not own:

- implementation;
- runtime mutation;
- deployment;
- production operations;
- user movement;
- engineering history;
- backlog ranking;
- certification evidence execution.

### 31.9 Graduation Review

Attempt to reopen architecture: `FAILED`.

Future work can continue without modifying architecture because:

- OMP is complete and self-evolving;
- SYSTEM_MAP owns future capability placement;
- Canonical Reference owns durable conclusions;
- Current Program State owns volatile state;
- Engineering Reports preserve historical evidence;
- Architecture Closed by Default blocks speculative redesign;
- Product Execution Mode routes work through OMP and existing owners.

Graduation verdict:

```text
MASTER_4_COMPLETE
```

Product Execution Mode is active.
Do not begin A5 from MASTER 4.

## 32. Engineering Intelligence Materialization / Phase 1

Status: `PHASE_1_COMPLETE`.

Engineering Intelligence Materialization turns existing architecture into explicit engineering capability.
It does not create a new Runtime, Planner, Owner, Truth Source, roadmap, master program, capability program, automation mode, or implementation queue.

Gate 0 classification:

| Target | Classification | Existing owner reused |
| --- | --- | --- |
| Observation Intelligence | `EXISTS_UNDER_OTHER_NAME` | Observation Plane owners + `RT2-S1` |
| Process Intelligence | `EXISTS_UNDER_OTHER_NAME` | Runtime Model + Work Placement + Decision Lifecycle + `RT2-S1` |
| Runtime Time Intelligence | `EXISTS_COMPLETE` | Runtime Model + `RT2-S1` + `RT2-S6` |
| Recommendation Intelligence | `EXISTS_PARTIAL` | `RT2-S6` + OMP + Backlog + Engineering Reports |
| Execution Intelligence | `EXISTS_UNDER_OTHER_NAME` | Runtime Model + execution/lease/packet/verification/rollback owners |
| Prediction Intelligence | `EXISTS_COMPLETE` | Prediction Evidence / Confidence owners |
| Confidence Intelligence | `EXISTS_COMPLETE` | Autonomy Root Confidence / Trust owners |
| Adaptive Engineering Intelligence | `EXISTS_PARTIAL` | Decision To Outcome To Learning + feedback/learning owners + `RT2-S6` |

### Engineering Intelligence Lifecycle

Engineering Intelligence lifecycle:

```text
Observation
  -> Process Understanding
  -> Runtime Time Understanding
  -> Recommendation
  -> Implementation through OMP if approved
  -> Outcome
  -> Prediction vs Reality
  -> Confidence Update
  -> Recommendation Evolution
```

Materialization rule:

Only `EXISTS_PARTIAL` read-model or lifecycle surfaces may be extended, and only under the existing owner.
`EXISTS_COMPLETE` and `EXISTS_UNDER_OTHER_NAME` surfaces must be reused.
Recommendation evolution remains advisory until OMP selects an implementation owner and later certification proves the outcome.

### RT2-S1 Engineering Measurement Contract

`RT2-S1` owns Engineering Measurement for Engineering Intelligence.
It materializes only read-only evidence:

- observation evidence;
- time fields;
- process/topology/critical-path fields;
- wait and blocker evidence;
- missing-field owner mapping;
- measurement reliability status.

`RT2-S1` must not decide, approve, rank execution, certify, mutate Runtime, create synthetic evidence, or become a truth source.

### RT2-S6 Engineering Recommendation Contract

`RT2-S6` owns Engineering Recommendation for Engineering Intelligence.
It materializes:

- owner-mapped recommendation;
- explicit no-change verdict;
- missing-evidence verdict;
- expected measurement plan;
- Product Evolution Review;
- Work Placement Review;
- Safety/Authority/Verification/Rollback/STOP_SAFE review.

`RT2-S6` recommendations are advisory until OMP routes approved implementation to an existing owner or Backlog.
`RT2-S6` must not mutate Runtime, expand authority, bypass verification, create a parallel roadmap, or replace OMP prioritization.

Engineering Intelligence maturity states:

```text
Measured
  -> Understood
  -> Recommended
  -> Validated
  -> Predictive
  -> Adaptive
```

The current Phase 1 materialization state is `UNDERSTOOD_PARTIAL_RECOMMENDED`: observation/process/time/prediction/confidence owners exist; recommendation and adaptive loops exist but need future measured implementation outcomes before `VALIDATED`, `PREDICTIVE`, or `ADAPTIVE` can be claimed for Engineering Intelligence as an operating capability.

## 33. Engineering Intelligence Materialization / Phase 2

Status: `PHASE_2_COMPLETE`.

Phase 2 materializes the Engineering Validation Loop.
It does not create a new Runtime, Planner, Owner, Truth Source, roadmap, master program, capability program, automation mode, or implementation queue.

Gate 0 classification:

| Target | Classification | Existing owner reused |
| --- | --- | --- |
| Prediction History | `EXISTS_COMPLETE` | Prediction Evidence / Confidence owners |
| Prediction vs Reality | `EXISTS_COMPLETE` | Prediction Evidence / Confidence + feedback/outcome owners |
| Recommendation History | `EXISTS_PARTIAL` | OMP + Engineering Reports + Backlog |
| Outcome History | `EXISTS_COMPLETE` | Feedback/outcome/learning owners |
| Confidence History | `EXISTS_COMPLETE` | Autonomy Root Confidence / Trust owners |
| Engineering Validation | `EXISTS_PARTIAL` | OMP + Runtime Model + Engineering Reports |
| Recommendation Accuracy | `EXISTS_PARTIAL` | `RT2-S6` + Prediction Evidence / Confidence |
| Recommendation Success | `EXISTS_PARTIAL` | `RT2-S6` + outcome owners |
| Recommendation Failure | `EXISTS_PARTIAL` | `RT2-S6` + outcome owners |
| Recommendation Drift | `MISSING` -> materialized | `RT2-S6` + OMP + confidence owners |
| Recommendation Confidence | `EXISTS_PARTIAL` | `RT2-S6` + Autonomy Root Confidence / Trust |
| Prediction Confidence | `EXISTS_COMPLETE` | Prediction Evidence / Confidence owners |
| Engineering Validation Loop | `EXISTS_PARTIAL` | OMP |

### Engineering Validation Lifecycle

Engineering Validation uses the existing OMP lifecycle.
No second engineering lifecycle is allowed.

```text
Recommendation
  -> Implementation through OMP if approved
  -> Outcome
  -> Prediction vs Reality
  -> Difference
  -> Confidence Update
  -> Recommendation Evolution
```

### Recommendation Validation Lifecycle

Every implemented recommendation must eventually be classified:

| Validation class | Meaning | Required evidence |
| --- | --- | --- |
| `RECOMMENDATION_SUCCESS` | Observed outcome supports the recommendation. | Verification/outcome evidence and expected-result match. |
| `RECOMMENDATION_FAILURE` | Observed outcome contradicts the recommendation or harms safety/product objective. | Verification/outcome evidence and contradiction. |
| `RECOMMENDATION_PARTIAL` | Outcome is mixed or incomplete. | Known pass/fail/unknown evidence split. |
| `RECOMMENDATION_DRIFT` | Recommendation assumptions changed before or after implementation. | Material state, owner, freshness, or evidence-version difference. |
| `RECOMMENDATION_UNVALIDATED` | Implementation/outcome evidence is missing. | Explicit missing owner/evidence reason. |

Recommendation validation must report expected result, observed result, difference, confidence delta, evidence source, owner, and canonical update need.
Validation cannot approve runtime action, expand authority, certify automation, or replace verification.

### Phase 2 Knowledge Preservation Rule

Validation-loop knowledge must survive report deletion through existing owners:

- Runtime Model owns Prediction, Validation, and Confidence contracts.
- OMP owns Engineering Validation Lifecycle and Recommendation Validation Lifecycle.
- Production Maturity owns Engineering Intelligence Validation Maturity.
- SYSTEM_MAP owns validation ownership lookup.
- Canonical Reference owns durable conclusions only.
- CPS owns current Engineering Intelligence validation maturity.

## 34. Engineering Intelligence Materialization / Phase 3

Status: `PHASE_3_COMPLETE`.

Phase 3 materializes Adaptive Engineering and closes the Engineering Intelligence materialization roadmap.
It does not create a new Runtime, Planner, Owner, Truth Source, roadmap, master program, capability family, automation mode, or implementation queue.
Runtime never self-improves.
Only Engineering Intelligence evolves through OMP and existing owners.

Gate 0 classification:

| Target | Classification | Existing owner reused |
| --- | --- | --- |
| Engineering Adaptation | `EXISTS_PARTIAL` | OMP + `RT2-S6` + Production Maturity |
| Recommendation Evolution | `EXISTS_PARTIAL` | `RT2-S6` + OMP |
| Recommendation Confidence Evolution | `EXISTS_PARTIAL` | `RT2-S6` + confidence owners |
| Engineering Learning | `EXISTS_PARTIAL` | Decision To Outcome To Learning + OMP |
| Recommendation Drift | `EXISTS_COMPLETE` | OMP + `RT2-S6` + affected owner |
| Recommendation Improvement | `EXISTS_PARTIAL` | `RT2-S6` + validation/outcome owners |
| Prediction Improvement | `EXISTS_UNDER_OTHER_NAME` | Prediction Evidence / Confidence owners |
| Adaptive Engineering | `EXISTS_PARTIAL` | Runtime Model + OMP + Production Maturity |
| Engineering Feedback Loop | `EXISTS_UNDER_OTHER_NAME` | Engineering Report -> Canonical Update -> CPS -> Continue OMP |
| Engineering Recommendation Quality | `EXISTS_PARTIAL` | `RT2-S6` + validation/outcome owners |
| Engineering Recommendation Confidence | `EXISTS_PARTIAL` | `RT2-S6` + confidence owners |

### Adaptive Engineering Lifecycle

Adaptive Engineering uses the existing OMP lifecycle.
No second engineering loop is allowed.

```text
Recommendation
  -> Implementation through OMP if approved
  -> Outcome
  -> Prediction vs Reality
  -> Confidence Update
  -> Recommendation Improvement
  -> Future Recommendation
  -> Engineering Learning
  -> Future Engineering
```

### Recommendation Evolution Lifecycle

Recommendation Evolution belongs to `RT2-S6` and OMP.

| Stage | Owner | Output |
| --- | --- | --- |
| Recommendation Version | `RT2-S6` + Engineering Report | Versioned recommendation basis. |
| Recommendation Confidence | `RT2-S6` + confidence owners | Advisory confidence. |
| Recommendation History | OMP + Engineering Reports + Backlog | Historical evidence and implementation state. |
| Recommendation Quality | `RT2-S6` + validation/outcome owners | Quality classification from real outcomes. |
| Recommendation Evolution | `RT2-S6` + OMP | Improved, degraded, drifted, retired, unchanged, or blocked. |
| Future Recommendation | `RT2-S6` + OMP | Owner-mapped future recommendation/no-change/missing-evidence verdict. |

### Engineering Learning Lifecycle

Engineering Learning is a documentation/control-plane learning loop.
It reuses existing learning owners but does not modify Runtime Learning.

```text
Outcome
  -> Engineering Learning
  -> Recommendation Confidence
  -> Recommendation Evolution
  -> Future Recommendation
```

Engineering Learning must name the outcome, prediction difference, confidence delta, recommendation quality, affected owner, canonical update need, and future recommendation state.
It cannot mutate Runtime, expand authority, approve implementation, create synthetic evidence, or replace OMP.

### Adaptive Read Models

Adaptive read models remain future read-only surfaces under existing owners.

| Possible read model | Existing owner | Phase 3 status |
| --- | --- | --- |
| Recommendation Confidence Trend | `RT2-S6` + confidence owners | `EXISTS_PARTIAL` |
| Recommendation Quality Trend | `RT2-S6` + outcome/validation owners | `EXISTS_PARTIAL` |
| Prediction Accuracy Trend | Prediction Evidence / Confidence owners | `EXISTS_COMPLETE` |
| Engineering Learning History | OMP + Engineering Reports + learning owners | `EXISTS_PARTIAL` |
| Recommendation Evolution History | OMP + Engineering Reports + Backlog | `EXISTS_PARTIAL` |
| Engineering Confidence History | Autonomy Root Confidence / Trust owners | `EXISTS_COMPLETE` |
| Engineering Improvement History | OMP + Engineering Reports + Production Maturity | `EXISTS_PARTIAL` |

Adaptive read models must not decide, approve, rank execution, mutate Runtime, certify themselves, or become a truth source.

### Engineering Intelligence Final State

Engineering Intelligence materialization is complete at the architecture/canonical level.
Remaining work is future implementation and evidence collection only.
Final canonical state: `MEASURED_UNDERSTOOD_RECOMMENDED_VALIDATION_MATERIALIZED_ADAPTIVE_ENGINEERING_READY`.

## 35. Historical Autonomous Execution Circuit Breaker Phase 2B Consumption Milestone

Classification: `HISTORICAL_MILESTONE`.
Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

Status: `IMPLEMENTATION_CERTIFIED_READ_ONLY`.

OMP consumes the Phase 2B implementation certification through existing owners. Repository code and isolated tests close the known Admin, direct CLI, governed/systemd, batch, rollback, Authority-promotion, and low-level primitive bypasses. Admin Safe Mode remains the sole operator-controlled stop state; Runtime consumers fail closed and do not gain Authority.

Production Maturity decision: `NO_CHANGE`. No deploy, production apply, user movement, Authority change, systemd change, production-state change, or real production outcome occurred.

OMP decision:

```text
CURRENT_STEP = CIRCUIT_BREAKER_IMPLEMENTATION_CERTIFIED_READ_ONLY
STOP_CONDITION = CIRCUIT_BREAKER_NOT_DEPLOYED_OR_PRODUCTION_VERIFIED
NEXT_LEGAL_STEP = SEPARATE_SAFE_DEPLOY_AND_PRODUCTION_CERTIFICATION_MISSION
OMP_CONTROLLED_RUN_ALLOWED = NO
```

This section records execution-program consumption only. It changes no Runtime, Planner, Authority, lifecycle, capability, architecture, policy threshold, blast radius, or canonical circuit-breaker semantics.

## 36. Historical Autonomous Execution Circuit Breaker Phase 3 Consumption Milestone

Classification: `HISTORICAL_MILESTONE`.
Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

Status: `PRODUCTION_CERTIFIED_OPEN`.

OMP consumed the Phase 3 safe-deploy, production fail-closed evidence, Production Maturity `ACCEPT`, and CPS live state. The canonical implementation is deployed, local/GitHub/runtime truth is aligned, and Admin Safe Mode v2 remains `OPEN`. No Runtime apply, user movement, Authority expansion, Planner change, route mutation, restore-barrier write, execution lease, or rollback apply occurred.

```text
CIRCUIT_BREAKER_CONTROLLED_RUN_GATE = PASS
OMP_CONTROLLED_RUN_ALLOWED = YES
ENGINEERING_INTENT_CLOSURE = INTENT_CLOSED
NEXT_LEGAL_STEP = PREPARE_SEPARATE_GOVERNED_OMP_CONTROLLED_RUN_MISSION
```

`YES` permits only a separate Mission to revalidate all existing Authority, Runtime, rollback, verification, blast-radius and operator-window gates. It does not authorize execution here. Phase 3 leaves the breaker `OPEN` and changes no OMP rule, owner, capability, lifecycle, policy threshold, Authority or runtime behavior beyond the already certified circuit-breaker enforcement.

## 37. Historical Recovery Artifact Combined Deploy Revalidation Consumption Milestone

Classification: `HISTORICAL_MILESTONE`.
Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

Status: `ADMITTED_ALREADY_DEPLOYED_REVALIDATED`.

OMP consumed the Phase 3A full-hunk audit, current tests, production hashes, truth/convergence, Production Maturity `NO_CHANGE`, and CPS. The historical accumulated deploy artifact `admin_core/autonomy_trust_acceleration.py` contains only two certified existing-owner read-only families: Stage 1 Diagnosis / Owner Resolution projection and Recovery B8/B9/B10-to-A6 integration. No unowned, uncertified, contradictory or mutation-capable hunk was found.

```text
RECOVERY_ARTIFACT_ADMISSION = PASS
COMBINED_DEPLOY_ADMISSION = PASS
CIRCUIT_BREAKER_CONTROLLED_RUN_GATE = PASS
OMP_CONTROLLED_RUN_ALLOWED = YES
ENGINEERING_INTENT_CLOSURE = INTENT_CLOSED
NEXT_LEGAL_STEP = PREPARE_SEPARATE_GOVERNED_OMP_CONTROLLED_RUN_MISSION
```

The current runtime delta is empty, so OMP does not request a duplicate deploy. This consumption changes no scheduler/optimizer rule, Runtime, Planner, Authority, capability, lifecycle, threshold, formula, blast radius or execution permission.

## 38. Historical First Governed OMP Controlled Run Phase 4A Consumption Milestone

Classification: `HISTORICAL_MILESTONE`.
Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

Status: `UNSAFE_IMPLEMENTATION`.

OMP consumed current production truth and a read-only governed candidate cycle. Candidate `candidate_7b48ef45c5f19af91a317fcd` (`10.0.0.2`, `vless -> awg3`) is a real bounded one-user opportunity, but it is not admitted for operational authority. Existing packet preview `pkt_preview_59a3c22747a4edb843be3863` lacks complete source/snapshot binding, routing readiness contains STOP_SAFE conditions, and the current Admin Safe Mode plus governed execution owners do not prove an operation-scoped generation-bound window with mandatory final `OPEN` for every terminal path.

```text
CURRENT_STEP = CONTROLLED_RUN_PREPARATION_STOPPED_UNSAFE_IMPLEMENTATION
STOP_CONDITION = UNSAFE_IMPLEMENTATION_CONTROL_WINDOW_NOT_CLOSED
RESPONSIBILITY_CLASS = EXISTING_OWNER_IMPLEMENTATION_GAP
AUTHORITY_REQUIRED_NOW = NO
CANDIDATE_SELECTED = YES
MISSION_ADMITTED = NO
PACKET_PREPARED = NO
CONTROLLED_WINDOW_CONTRACT = FAIL
OMP_CONTROLLED_RUN_ALLOWED = NO
NEXT_LEGAL_STEP = IMPLEMENT_AND_CERTIFY_OPERATION_SCOPED_CONTROLLED_WINDOW_AND_PACKET_SOURCE_BINDING
```

Production Maturity decision: `BLOCK`, score unchanged. Safe Mode remained `OPEN`; no operational Authority request, lease, restore barrier, apply, movement, rollback, systemd change or production mutation occurred. OMP rules, owners, capability, lifecycle, Runtime, Planner, Authority and blast radius are unchanged.

## 39. Historical Polygon-Driven L7 Calibration Floor Consumption Milestone

Classification: `HISTORICAL_MILESTONE`.
Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`
Authority expansion: `NONE`

Status: `CALIBRATION_FLOOR_CONSUMED_EXACT_RESIDUAL_PRESERVED`.

OMP consumed immutable eligibility set `outset_428a4e2ff440ed64bde5cb56` with five eligible controlled Passports. Four additional real bounded one-user transactions completed immediate, 5m, 1h, steady-state, Learning and replay verification. The floor and material variation are closed; natural production and rollback/no-rollback diversity are not.

```text
M4 = COMPLETE_CONSUMED_CALIBRATION_FLOOR
M5 = EVENT_DRIVEN_CAPTURE_READY_REAL_WORLD_LIMIT
M6 = INSUFFICIENT_EVIDENCE
M7 = COMPLETE_CONSUMED_INSUFFICIENT_EVIDENCE
M8 = MISSION_NOT_REQUIRED_BY_AUTHORITY_VERDICT
CONTROLLED_LANE_NEXT = REQUEST_EXACT_CONTROLLED_ROLLBACK_CONDITION_ENGINEERING_AUTHORITY
NATURAL_LANE_NEXT = PASSIVELY_CONSUME_QUALIFYING_NATURAL_EVENT
PRODUCTION_MATURITY = NO_CHANGE
```

Five remains a calibration floor rather than a promotion threshold. This milestone grants no class approval, Authority expansion, bounded autonomy, autonomous Runtime or Production Maturity credit.

## 40. Historical Design-Time Semantic Gate Repair And Automatic OMP Routing Milestone

Classification: `HISTORICAL_MILESTONE`.
Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`
Authority expansion: `NONE`

Status: `EXACT_RED_GATE_REPAIRED_AND_FAILURE_TO_OMP_ROUTING_INSTALLED`.

GitHub Actions run `29682110261` at source commit `7ab18749` failed in `semantic-selective-gate` for two independent reasons: `functional_footprint_mismatch:AEP_PHASE_6_STATUS` and `polygon_design_time_m8_frontier_not_active`. Existing owner repairs in commit `28970ba3` restored the CPS functional-footprint producer contract and made the M8 fixture stage its exact required frontier; exact workflow replay `29685043993` passed without gate weakening.

The same workflow now preserves a red job and automatically materializes distinct deterministic BDP/OMP repair frontiers for every detected producer-consumer failure class. The failure log and repair-frontier JSON are uploaded through the existing GitHub Actions artifact owner. They are evidence only and do not mutate CPS.

```text
FAILURE_1 = PRODUCT_SEMANTIC_REGRESSION -> LAST_RESPONSIBLE_REAL_SOURCE_OWNER
FAILURE_2 = STALE_SOURCE_DEPENDENCY_BINDING -> PERMANENT_POLYGON_DESIGN_TIME_ENGINEERING
CONSUMER = OMP_CANDIDATE_ADMISSION
SAME_GATE_REPLAY = PASS
CI_GATE_WEAKENED = NO
NEW_TRUTH_SOURCE = NO
PRODUCTION_EFFECT = NONE
```

## 41. Service Failure Legacy Runtime Authority Projection Fail-Closed Repair

Classification: `PERMANENT_RULE`.
Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.
Scheduling Authority: `NONE`.
Execution Authority: `NONE`.
Authority expansion: `NONE`.

Production read-only planning discovered that the existing policy owner still
contained a historical `XLARGE_BATCH/50` projection promoted on 2026-07-03,
while CPS current truth is `GOVERNED_ONLY` and the active Program is at
`ENGINEERING_AUTHORITY`. This was a latent producer-to-consumer disagreement:
historical promotion evidence could otherwise be interpreted as present action
Authority.

The existing `tools/v7-users-autoswitch` authority gate now requires a fresh,
bounded `v7.current-action-class-contract.v2` for new Authority above `CANARY`.
Only the existing `admin_core/operator_execution.py` Authority decision owner
may issue it from an exact `APPROVE_ONCE_AS_SCOPED` request/hash binding. It
validates issuer, decision provenance, exact user/source/target, source or
incident generation, `max_users=1`, `max_concurrent_transactions=1`, expiry,
verification/rollback/cooldown/anti-flap contracts and one-use state before the
restore-barrier or apply path. Missing or stale contracts force `FROZEN/0` and record
`block_all_selected_moves_current_action_class_contract_required`.

```text
HISTORICAL_XLARGE_POLICY -> CURRENT_ACTION_CLASS_CONTRACT_GATE -> FROZEN_OR_BOUNDED_SCOPE
MUTATION = 0
USER_MOVEMENT = 0
ROUTING_CHANGE = 0
AUTHORITY_GRANT = 0
NEXT_LEGAL_STEP = EXISTING_OWNER_ISSUES_EXACT_UNEXPIRED_ONE_USE_CONTRACT_OR_REMAINS_STOP_SAFE
```

The repair changes neither the CPS Authority decision nor Production Maturity.
It removes an unsafe stale projection; it cannot issue a contract, apply a
Packet, move a user, write a restore barrier or enable a service/timer.

## 42. Generic Movement Evidence Reuse And Service-Failure Adapter Law

Classification: `PERMANENT_RULE`.
Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.
Evidence owner: existing historical movement/certification owners.
Execution owner: existing governed movement lifecycle.
Authority owner: existing delegated-policy Authority owner.

Historical movement evidence must be consumed as a dimension matrix, not as
one scalar tier. The existing owner projects:

```text
GENERIC_USER_ROUTE_MOVEMENT_PRIMITIVE
SERVICE_FAILURE_INCIDENT_DRAIN_ADAPTER
CURRENT_AUTHORITY
RUNTIME_ENABLED_TIER
```

These names are projections inside existing owners. They are not new
capabilities, registries, executors, certification systems or Authority
objects.

The generic projection may retain reusable assignment mutation, route
verification, rollback/no-rollback, replay/duplicate suppression, packet
identity, serial cohort, Outcome and Learning pipeline evidence. It must retain
their different maxima. Service verification, capacity, source/target choice
and incident-scope correctness remain adapter-bound.

The exact historical actual scopes are `1,2,4,5,10,25,48`. Four-user
rollback-applied evidence is preserved separately. A 48-user outcome against a
50-user budget is partial-scope selection, not exact 50-user proof and not
partial-apply failure recovery. Serial cohort evidence never proves parallel
transaction concurrency.

Runtime is fail-closed:

```text
RUNTIME_ENABLED_TIER =
min(
  GENERIC_CAPABILITY_MAX,
  EXACT_ADAPTER_COMPATIBLE_MAX,
  CURRENT_AUTHORITY_MAX,
  LIVE_CAPACITY_AND_VERIFICATION_SAFE_MAX
)
```

Historical Authority, Packet, lease or action-class identity is never
generalized. Valid generic evidence may prevent a repeated certification
ladder, but cannot activate a larger tier. Higher-tier activation requires the
existing independent M7 Authority decision and fresh policy generation.

Engineering compatibility and Authority recommendation may identify a larger
ceiling. Runtime activation remains the exact approved tier and proceeds only
through adaptive waves with fresh live gates. Every real action must be
independently justified by service protection, not by a desire to manufacture
evidence.

Legal consumed outcomes are:

- `EXACT_TIER_RUNTIME_AUTHORITY_ACTIVATED`;
- `HOLD_CURRENT_TIER_DECISION_CONSUMED`;
- `NARROW_SCOPE_DECISION_CONSUMED`;
- `DECLINE_DECISION_CONSUMED`.

The current Matrix-owned incident drain remains independent and continues
under its exact active Tier-4 standing policy while this evidence projection
is reconciled. Runtime remains serial and every attempt retains the current
incident, scope and live-gate contracts.

## 43. Incident-Bound Tier Cohort Admission And Atomic Revalidation Law

Classification: `PERMANENT_RULE`.
Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.
Incident owner: existing Service Failure obligation and OMP consumption
owners.
Execution owner: existing governed movement lifecycle.
Authority owner: existing delegated-policy Authority owner.

A standing delegated policy is necessary but is not sufficient to enter the
Service Failure cohort planner. Every bounded production attempt must also be
bound to one current durable incident obligation, its exact OMP consumption
receipt and one fresh matching capture-only event.

```text
VALID_STANDING_POLICY
AND
CURRENT_DURABLE_OBLIGATION
AND
MATCHING_OMP_CONSUMPTION
AND
FRESH_MATCHING_CAPTURE_EVENT
AND
POSITIVE_CURRENT_SOURCE_SCOPE
-> PLANNER_MATERIALIZATION_ELIGIBLE
```

Missing, stale, mismatched or empty incident scope stops before Candidate,
Packet, lease, restore-barrier write or apply. A generic balancing
recommendation must never enter a Service Failure action merely because the
standing tier permits the same movement count.

For a cohort, operation-scoped source and snapshot truth is one atomic
all-member binding. Both Packet creation and restore-barrier revalidation must
use the same deterministic cohort projection. Reducing a cohort to its first
member is invalid.

The Matrix lifecycle owns compact caller/consumer pointers only. Complete
Packet, execution, Outcome and Learning facts remain in their existing
specialized owners. Empty-scope production proof is a valid safe terminal but
is not a Tier movement Outcome and cannot advance the production-proven tier.

The legal empty-scope terminal is:

`STOP_SAFE_CURRENT_SOURCE_SCOPE_EMPTY`.

The durable successor remains the ordinary enabled Matrix timer. The next
genuine positive-scope matching incident may automatically re-enter the
existing planner under the current exact tier, without Codex or operator
continuation and without reusing any Candidate, Packet or lease.

## 44. Tier-48 Generic Movement And Adaptive Cohort Separation Law

Classification: `PERMANENT_RULE`.
Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.
Generic capability owner:
`admin_core.autonomy_trust_acceleration.build_historical_blast_radius_evidence`.
Scenario adapter and Runtime owner: the existing Service Matrix, Planner,
autoswitch, Packet, lease, verification, rollback/containment, Outcome,
Replay and Learning owners.
Authority owner: the existing delegated-policy Authority owner.

Production evidence, Engineering certification, scenario-adapter
compatibility, Authority and Runtime are independent axes. An Engineering
Polygon or implementation guarantee can raise only the engineering-certified
maximum. It cannot rewrite historical production evidence, grant Authority,
enable Runtime, move a user or increase Production Maturity.

The generic bounded cohort transaction is one logical transaction with one
immutable cohort fingerprint, Candidate, Packet, lease, source/target binding,
per-member subreceipts, exact applied/unapplied/failed sets, circuit breaker,
rollback or bounded containment, final safe-mode decision, Outcome,
Replay/Learning lineage and successor. Member writes may remain serial.
`max_concurrent_transactions=1` is unchanged. A checkpoint from the same
operation forbids duplicate forward apply and routes causal closure through
the existing owners; Packet reuse is never a restart mechanism.

For every current incident generation the existing Planner computes:

```text
effective_cohort_limit =
min(
  incident_required_scope,
  eligible_source_scope,
  generic_engineering_certified_scope,
  adapter_compatible_scope,
  capacity_safe_scope,
  authority_safe_scope,
  runtime_safe_scope,
  verification_safe_scope,
  rollback_containment_safe_scope,
  circuit_breaker_safe_scope,
  request_safe_scope
)
```

Every bound carries its existing owner, value, fingerprint, freshness and
reason. Unknown or stale mandatory bounds fail closed. Count alone is
insufficient: selected member load must remain within the existing target
capacity and reserve contract. The durable obligation, Candidate preparation
and Runtime caller must preserve the same exact selected cohort fingerprint,
bound set and limiting bound.

Generic mechanics may be reused by Service Failure, governed movement,
maintenance, recovery, migration and capacity adapters, but every adapter
retains its own trigger, source scope, target selection, capacity,
verification, containment and Authority delta. An unqualified adapter is an
explicit residual; it does not invalidate the generic primitive or block an
independent qualified adapter.

When the generic and Service Failure engineering maxima reach 48 while current
Authority is smaller, the only legal Product Evolution frontier is:

`EXACT_TIER48_SERVICE_FAILURE_AUTHORITY_DECISION_REQUIRED`.

That independent request may bind maximum 48 and concurrency one. Approval
does not itself certify Service Failure production behavior. Controlled
adapter outcomes progress `5 -> 10 -> 25 -> 48`, each with fresh identities
and live gates, and stop on the first unsafe terminal. Valid generic
certification is reused and must not be ceremonially rerun.

## 45. Runtime Time Reuse And Availability Cohort Critical-Path Law

Classification: `PERMANENT_RULE`.
Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.
Time semantics owner: `docs/reference/V7_RUNTIME_MODEL.md`.
Analysis owner: `admin_core.operator_execution_pipeline.execution_performance_foundation`.
Runtime producer: `tools/v7-governed-canary-dry-run-cycle`.

Wall-clock timestamps own audit ordering only. Exact elapsed performance uses
one process-local monotonic clock. Wall-clock, freshness age, deadline/TTL and
event ordering must never be substituted for monotonic elapsed duration.

Availability-first governed transactions publish a compact five-stage timing
projection through their existing receipt: planner, Packet/lease,
restore-barrier, apply/verification and feedback/Learning. The projection is
consumed by the existing performance foundation and is stored once per cohort
Packet, never once per member. No second ledger, metrics registry, watcher or
truth source is created.

When the current standing policy, exact immutable allocation and all live
gates admit more than one certification identity on one target subset, the
existing cohort-capable L3 executor owns one fresh Candidate, Packet and lease
for that exact subset. `max_concurrent_transactions=1`, per-user apply results,
verification, rollback/containment, circuit breaker, Outcome, Replay and
Learning remain mandatory. Repeating the entire governed lifecycle once per
member is forbidden unless an owner-backed invalidation proves that cohort
binding is unsafe for that exact action class.

Historical Stage-25 receipt `afstage_2595c3494c52f5fa6ba96592` remains
immutable and must not be repeated for benchmarking. Its observed forward
member windows of approximately 92.882–147.411 seconds established the
baseline; post-repair production p50/p95 requires a new independently admitted
owner-driven cohort transaction and cannot be inferred from tests.

Stage 48 remains STOP_SAFE while the controlled source is absent from current
topology truth or fewer than 48 current certification identities occupy its
source scope. The ordinary Matrix timer owns automatic revalidation. Identities
must not be moved merely to manufacture latency or Stage-48 evidence.

### 45.1 One-Governed-Transaction Latency Forensics And Repair

Mission identity:
`ONE_GOVERNED_TRANSACTION_SECOND_BY_SECOND_LATENCY_FORENSICS_AND_REPAIR_V1`.
Program owner remains
`V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`; this subsection creates
no Program, Planner, Runtime, Time owner, registry, watcher or evidence store.

The immutable Stage-25 receipt exposed 92.882--147.411 second member windows.
Existing-owner forensics proved that the dominant avoidable producer was
service verification: fourteen required services were executed through
fourteen sequential Python process launches, Matrix lock acquisitions and
durable writes, although the existing service-matrix owner already supported
bounded parallel probes.

Production commit `347cacbfb6e44679e626579ab662a5af9f391a4a` extends the
existing owners with process-local monotonic spans and replaces that sequence
with one exact bounded service subset, one parallel probe generation and one
Matrix durable write. The exact fourteen-service comparison is owner-consumed:

| Path | Elapsed | Result |
| --- | ---: | --- |
| backward-compatible sequential verifier | `91.965611 s` | `14/14 PASS` |
| repaired bounded parallel verifier | `8.786229 s` | `14/14 PASS` |

The repaired span assigns `7.521070 s` to parallel network/service probes,
`1.265159 s` to the Matrix lock and durable write, `0.000374 s` to module
initialization, and about `0.050091 s` to process CPU. This is a measured
component terminal, not a fabricated full governed-transaction terminal.

Stage 48 is blocked by the Time consumer until one lawful fresh existing-policy
single-user governed transaction publishes and consumes the deployed nested
monotonic timeline. Packet, lease, Authority, user and topology identities must
be fresh. Stage 25 must not be repeated. Ordinary users must not be moved for
benchmarking. If the existing controlled-topology owner reports incomplete
source/target identity, the exact terminal is
`FRESH_LAWFUL_CONTROLLED_SINGLE_TRANSACTION_BENCHMARK_SOURCE_TARGET_IDENTITY_REQUIRED`.
Its durable re-entry is the next existing-owner topology generation where
`source_target_identity_complete=true`; that output is consumed by the existing
Matrix/governed-transaction path without a new Program or manual benchmark
shortcut.

Only after the full transaction proves every interval over one second, low
level mutation versus governance overhead, same-path before/after improvement,
and existing performance-foundation consumption may OMP emit
`ONE_GOVERNED_TRANSACTION_FASTEST_SAFE_PATH_PROVEN` and release the Time side
of the Stage-48 gate.

### 45.2 Final Performance Closure Production Consumption

Classification: `HISTORICAL_MILESTONE`.
Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`
Scheduling Authority: `NONE`
Execution Authority: `NONE`

The ordinary enabled Matrix timer completed the required certification-only
full-path transaction without a manual Matrix invocation. Certification user
`10.7.0.107` moved `vless -> awg3`, passed verification, Outcome, Replay and
Learning consumption, and returned `awg3 -> vless` through the existing reset
owner. Forward Packet `pkt_d51d30891a225ed0827a5664`, reset Packet
`pkt_preview_66d91f764ec9c5b46c49c0f1` and receipt
`perfclose_1f91af0c6253c6fe75e028c5` are owner-backed and non-reusable.

The full cycle consumed `227.573707 s`; the nested governed forward path
consumed `92.054652 s`. Every interval over one second has an explicit
existing owner. The existing performance foundation consumed the monotonic
timeline under `v7.execution-performance-foundation.v1`.

The exact fourteen-service same-path repair remains `91.965611 s ->
8.786229 s`, `14/14 PASS`, speedup `10.47x`. Matrix evidence is canonical
`EGRESS_PATH_AND_CHANNEL_PROFILE` evidence and is inherited only with exact
path/config/egress/service-set identity plus independent user route-binding
verification.

The resulting terminals are:

- `ONE_GOVERNED_TRANSACTION_FASTEST_SAFE_PATH_PROVEN`;
- `STAGE_48_OPTIMIZED_RUNTIME_READY`.

Receipt semantics are readiness only. `campaign_stage_credit=false`, Stage 48
was not executed, no Natural L8 credit exists, and no Authority or Production
Maturity changed. Runtime must expose
`STAGE_48_OPTIMIZED_RUNTIME_READY_NOT_EXECUTED` until a separate existing-owner
Stage-48 admission is consumed.
