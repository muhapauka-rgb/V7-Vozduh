# V7 Agent Capability Existing-Owner Audit And Admission Decision

Discover → Reuse → Extend → Implement.
Continue OMP.

## Authorization

Mission: `V7_AGENT_CAPABILITY_EXISTING_OWNER_AUDIT_AND_ADMISSION_DECISION`
Project: `V7 VOZDUH`
Type: read-only system audit, existing-capability discovery, real caller/consumer/state analysis, reuse/extension/fundamental-gap decision and minimum canonical execution-model recommendation.

This Mission authorizes no Runtime, production, routing, user, code-refactoring, UI, deploy, recovery, CPS, OMP, Planner, Authority, Canonical Reference or SYSTEM_MAP mutation. It authorizes no new Program, owner, truth source, coordinator, queue, scheduler, watcher, daemon, registry, graph, state machine, Runtime or Agent System implementation. It does not implement Stage 1.

## Engineering principle

`OWNER` is an existing canonical V7 responsibility owner. `EXECUTION ROLE` is a bounded temporary role working for an existing Mission. `EXECUTION PROFILE` is its instructions, tools, permissions, evidence and stop conditions. `MODEL` is a replaceable reasoning mechanism and owns no V7 truth or Authority. `AGENT` is only one possible implementation form of an execution profile.

Preferred engineering principle:

`NO NEW AGENT SYSTEM UNLESS REQUIRED`.

The desired outcome is the smallest lawful mechanism:

`REUSE_AS_IS` first;
`EXTEND_EXISTING_OWNER` second;
`NEW_BOUNDED_MECHANISM` only after a proven fundamental gap.

Do not bias the audit toward any verdict. Uncertainty is not permission to create architecture.

## Canonical startup and truth routing

Start from current CPS → OMP → Canonical Reference → SYSTEM_MAP → relevant accepted contracts → fresh Runtime observation where required. Reports and old graphs are historical evidence unless their current producer, consumer and freshness path are proved.

CPS owns volatile Program state; OMP owns orchestration and residual recomputation; Canonical Reference owns durable meaning; SYSTEM_MAP owns topology; accepted product/architecture contracts define TO-BE; fresh Runtime observation defines current behavior.

Do not replace, reorder or shadow the current CPS/OMP frontier. Any future agent mechanism may only be evaluated as a bounded execution profile for an already admitted Mission.

## Mandatory proof standard

For every capability identify its current owner, producer, real caller, real consumer, state effect, behavioral effect, Runtime/deploy path, freshness, Authority boundary and terminal consumer.

A capability is reusable only if its current producer, current consumer and execution path are proven sufficient for the required role.

`DOCUMENTED CAPABILITY WITHOUT A CURRENT EXECUTION CONSUMER DOES NOT SATISFY THE ROLE.`

Tests, reports, commits, pushes, deploy acknowledgements, named consumers and in-process probes alone do not prove current caller, consumption, durable state, Runtime, production, user effect or Mission closure.

## Responsibility-domain and subgraph analysis

Do not design around individual files. For every relevant canonical responsibility map all implementation surfaces, functions, callers, consumers, reads/writes, mutation boundaries, locks/leases, subprocess/process edges, Runtime triggers, deployment units, tests, Authority, current/historical paths, hot-path membership, rollback/re-entry and terminal consumption.

The optimization unit is a `RESPONSIBILITY SUBGRAPH`, not a file.

A responsibility subgraph includes all current implementation surfaces participating in one canonical responsibility, even when they span `tools/`, `admin_core/`, Runtime support, tests, systemd and generated/projection code.

Identify cross-file responsibility coupling before judging any single large file. File size, function count and model-generated complexity scores are signals, not defect verdicts. Dead/unused claims require real caller, consumer, Runtime/deploy and compatibility proof.

## Existing-capability discovery

Inspect current equivalents and live execution paths for Function/call/producer-consumer graphs; owner, Authority, state, lock, process and hot-path maps; canonical knowledge; SYSTEM_MAP; source discovery; CPS/OMP; BDP/AEP; simplification-first; responsibility realignment; repository/Runtime minimization; complexity and latency metrics; Architecture, Quality, Safety and Evidence Review; Engineering Truth Lifecycle; handoff; deploy/convergence; exact-once/re-entry; identity/provenance; cancellation/failure recovery; prompt-injection protection; and audit reproducibility.

At minimum inspect the current equivalents of `V7_AUTONOMOUS_MODEL_FUNCTION_GRAPH_APPENDIX`, `V7_CANONICAL_ARCHITECTURE_KNOWLEDGE`, `V7_STAGE2_KNOWLEDGE_ENGINEERING_PROGRAM`, `V7_AUTONOMOUS_EVOLUTION_SOURCE_DISCOVERY_AUDIT`, SYSTEM_MAP, OMP, CPS, current simplification rules, current Engineering Report/handoff and independent review/evidence consumers.

Use verdicts: `REUSE_AS_IS`, `EXTEND_EXISTING_OWNER`, `EXISTING_CAPABILITY_BUT_NO_REAL_CONSUMER`, `STALE_OR_HISTORICAL_ONLY`, `INSUFFICIENT_EVIDENCE`, `FUNDAMENTAL_GAP_PROVEN`.

Produce a matrix:

| Required capability | Existing owner | Artifact/tool | Real caller | Real consumer | State effect | Runtime effect | Current evidence | Reuse | Extend | Fundamental gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Include Function/call/producer-consumer graph, mutation/owner/Authority/state/lock/process/hot-path/test maps, current Runtime and Program truth, complexity/latency, handoff, independent review, deploy/convergence, provenance, idempotency/re-entry, concurrency, cancellation, prompt-injection protection and `CONTINUOUS_COMPLEXITY_REGRESSION_DETECTION`.

## AS-IS, TO-BE and delta

AS-IS comes from current code and fresh Runtime reality. TO-BE comes only from accepted product and architecture contracts across Management, Control, Data and Engineering planes and their existing owners. Do not let implementation define desired architecture and do not create a durable architecture-agent truth.

Classify the delta as required semantic complexity, accidental complexity, responsibility drift, duplicate ownership/state, wrong-plane dependency, obsolete compatibility residue, missing evidence or owner/writer/consumer mismatch.

## Conceptual execution roles

Evaluate Architecture/System Review, Recovery Latency Optimization, Code Optimization, Safety/Regression Review, Evidence Review and future UI Delivery only as conceptual execution roles. Do not assume separate agents, models, processes, owners, state surfaces, queues or files.

For each role determine the existing owner/mechanism/tools/caller/consumer, permitted and prohibited actions, evidence, Authority, terminal consumer, whether a bounded OMP execution profile is sufficient, and any proven residual gap.

Architecture Review is normally read-only and cannot invent owners, mutate architecture/Runtime, select its own Mission or self-certify.

Latency work may operate only inside the admitted recovery-latency Mission, on the current canonical metric and measured P0/P1 contributor, without weakening S11 or deleting timing boundaries. It returns through independent review and the existing OMP consumer.

Code Optimization minimizes accidental complexity while preserving product behavior, safety, performance, observability, owners, rollback, exact-once/re-entry, route/kernel truth and S11. Its order is understand → prove usage → delete → reuse → collapse → narrow → deduplicate → realign to an existing owner → extract only on an existing boundary → add only essential logic.

Safety Review evaluates an immutable change fingerprint and does not improve the submitted code. Evidence Review independently validates provenance, comparability, caller/consumer, state, Runtime, production and user-effect claims. Independence requires separate context, immutable identity, no reliance on implementer conclusions, ability to return insufficient evidence and a real downstream consumer.

UI remains Management Plane and cannot own health, target selection, Planner, Authority, route truth, recovery state or execution frontier.

## Coordination and state admission

Do not create or pre-approve `V7_AGENT_COORDINATOR`. First prove whether existing OMP can perform:

`EXISTING CPS FRONTIER → EXISTING OMP → BOUNDED EXECUTION PROFILE → IMMUTABLE HANDOFF → INDEPENDENT REVIEW → EXISTING OMP CONSUMER → ATOMIC CPS PROJECTION → RESIDUAL RECOMPUTATION → EXACT SUCCESSOR OR LEGAL TERMINAL`.

A new coordinator requires a missing responsibility, no existing owner, a real caller/consumer, unambiguous state, failure/re-entry semantics, independent review and proof that extending OMP would violate an accepted boundary. Otherwise: `NO_NEW_COORDINATOR`.

Do not create or pre-approve `AGENT_FRONTIER`. Any admissible execution record must reference rather than copy the canonical Mission, contain immutable provenance/fingerprints/actions/verdicts, select no next Mission, own no current truth, have terminal/retention/idempotency/replay rules, be discardable without losing product truth and have an existing owner/consumer.

## Continuous complexity protection

Determine whether existing owners can continuously detect that a responsibility domain becomes materially more complex after a later patch, compare structural BEFORE/AFTER and trigger review when:

- duplicate responsibility appears;
- a third related special-case branch appears;
- a new state surface appears;
- a new process hop appears;
- superseded compatibility remains after migration proof.

Distinguish a per-Mission completion declaration from an independently produced responsibility-subgraph delta and a real continuous consumer. Do not claim this capability exists merely because a completion form contains complexity fields.

If the current chain is incomplete, route the residual through the existing BDP → OMP admission path unless a fundamental owner gap is independently proved.

## Technical control audit

For every possible execution profile evaluate identity/provenance; least-privilege tools; secret isolation; action-class Authority and STOP_SAFE; Mission locks/leases/idempotency/stale-generation/concurrency/restart/cancellation/timeout/partial-failure; repository/document/log prompt-injection boundaries; path/command/network/output controls; step/time/token/cost/retry budgets; immutable action log; exact failure; fingerprints; and independent replay.

Reuse existing operation-control, Packet/Lease/Barrier, audit and evidence owners before recommending any mechanism.

## Admission decision

Return exactly one overall verdict:

`NO_NEW_SYSTEM` — existing owners and execution profiles suffice.
`EXTEND_EXISTING_EXECUTION_CONTRACT` — a bounded extension is required without a new owner/coordinator/truth/Program/Runtime.
`NEW_BOUNDED_MECHANISM_REQUIRED` — a fundamental residual gap is proved.
`INSUFFICIENT_EVIDENCE_FOR_NEW_MECHANISM` — current evidence cannot justify architecture.

The third verdict requires proof of missing responsibility, absent owner, real caller/consumer, state and Authority, failure/re-entry, independent review, invalidity of extending an existing owner, minimum size and deletion/rollback, and non-duplication of CPS/OMP/Planner/Authority/Runtime truth.

## Output

Create or update one compact Engineering Report named `V7_AGENT_CAPABILITY_EXISTING_OWNER_AUDIT_AND_ADMISSION_DECISION` containing: current frontier and truth classes; capability matrix; real owners/callers/consumers; reuse/extension/stale/no-consumer/gap findings; AS-IS/TO-BE owners and delta; every role admission; coordinator/state verdicts; technical controls; continuous-complexity verdict; handoff; duplication risks; overall admission decision; conditional minimum roadmap; exact existing files/owners that might later change; files/owners not to create; no-Runtime-change verdict; exact smallest next action, owner, consumer, re-entry and independent input.

Separate code existence, caller, consumer, state, behavior, Runtime, production and user effect.

Before finalizing perform Architecture Review, Quality Review and Self Review. Check especially that the audit did not silently design the requested subsystem, mistake role names for owners, recommend files without a proven gap or displace the current CPS/OMP frontier.

Final law:

`REUSE FIRST.`
`EXTEND EXISTING OWNERS SECOND.`
`NEW MECHANISM ONLY AFTER A PROVEN FUNDAMENTAL GAP.`
`NO PARALLEL TRUTH.`
`NO DUPLICATE GRAPH.`
`NO DUPLICATE PROGRAM.`
`NO DUPLICATE COORDINATOR.`
`NO DUPLICATE FRONTIER.`
`NO SELF-CERTIFICATION.`
`NO RUNTIME CHANGE IN THIS MISSION.`
