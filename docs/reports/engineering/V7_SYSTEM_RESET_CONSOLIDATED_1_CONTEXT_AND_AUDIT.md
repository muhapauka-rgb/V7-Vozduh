# V7 System Reset — Volume 1: Context and Audit

> Consolidated source set. This volume preserves the included reports verbatim;
> the volume heading and separators are navigational only. It is the compact
> sendable representation of the original report set, not a new authority.

## Reading map

1. Pre-Reset incident/receipt/certification repairs, CT-M0F and routing/failover reality.
2. Reset creation through RESET-M1 portfolio disposition.
3. Post-Reset reality check.
4. RT2 PR1 baseline, PR2 package/relationship audit, deep code audit and
   commercial-routing comparison.

The appended source blocks in this volume are: `015600`, `021146`, `024500`,
`360000`, `390000`, `400000`, `410000` and `420000`.

---

# CT-M0F: repair of the measurement path and topology boundary

Date: 2026-08-13 UTC  
Program: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Parent Mission: `CT-M0F CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_LATENCY`

## Result

`MEASUREMENT_CONSUMER_REPAIRED_DEPLOYED_AND_PRODUCTION_CALLED`.

The first VALID CT-M0F latency sample was **not** manufactured.  The current
legal terminal is:

`SAFE_PREDECESSOR_REQUIRED:EXISTING_CONTROLLED_SOURCE_RESERVATION_AND_CERTIFICATION_GROUP_OWNER`.

## Exact producer-consumer defect repaired

Earlier controlled attempts reached fresh reservation, Candidate, Packet,
lease, route verification and target payload probing, but were terminalized as
`CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_INVALID`.

Two exact failures were proven from existing owner evidence:

1. The Matrix incident shell could be present with zero monotonic failure
   clocks, while the exact matching append-only controlled-condition record
   held the owner-backed clocks.  The consumer only read that record when the
   incident ID was absent.
2. The target-only payload socket already used `SO_BINDTODEVICE`, but its
   route proof asked the main routing table without `oif`.  That truthfully
   returned `ens3`, even though the bound probe path was `awg0` or `awg3`.

Commit `9155006ec5c62b16f9be08164ae883d65d27a169` repairs only existing
owners:

- `tools/v7-users-autoswitch` always loads the exact matching condition for a
  standing CT-M0F contract, preserves Matrix incident identity, and uses its
  clocks only as a non-zero fallback;
- `tools/v7-client-speed-api` adds `oif <target-interface>` only to the
  already target-only, interface-bound payload proof.  Exact-client probes
  remain unchanged.

No new owner, queue, registry, Runtime, Authority, scheduler or VLESS-specific
logic was introduced.

## Verification and deploy

- Focused existing-owner tests: `354` passed.
- Safe deploy manifest: PASS; changed production paths were exactly
  `tools/v7-users-autoswitch` and `tools/v7-client-speed-api`.
- Safe deploy: PASS, deploy ID
  `deploy-z8-14-Updatesystem-9155006-20260813T082420`.
- Production binaries match the deployed hashes; the ordinary
  `v7-autoswitch-planner.timer` remained active and called the existing Matrix
  consumer after deploy.
- Truth and convergence: PASS / `FULLY_ALIGNED` at commit `9155006e` across
  local, GitHub and production.

No routing apply, user movement, restore-barrier write, rollback apply,
Authority expansion or Production Maturity change occurred during this repair.

## Why a first valid sample cannot yet run

The live CT-M0F selector is correctly fail-closed:

- no healthy isolated controlled source with a group-aligned certification
  identity;
- no exact certification identity on such a source;
- no distinct controlled-contract-admitted target.

The topology owner confirms the standing delegated CT-M0F and controlled
topology policies are active and audit-backed.  The blocker is not an Authority
decision and is not VLESS recovery: the former isolated reservation expired;
the 52 certification identities are now spread over ordinary/shared channels;
there is no empty owner-verified source or ready existing draft that may become
the one-user controlled failure domain.  Reusing any occupied source would
violate the proven whole-interface failure isolation invariant.

The existing `RESTORE_CONTROLLED_CERTIFICATION_BASELINE` consumer was also
checked.  It is intentionally limited to the exact prior Packet/Outcome and
its verified forward allocation; it cannot evacuate an arbitrary live group of
five certification identities to manufacture a CT-M0F source.  Extending it
for that purpose would be an unapproved routing action and would invalidate the
measurement.  Therefore no safe internal predecessor remains at this moment.

## Durable next action

Existing owner: `admin/v7-admin-api egress draft lifecycle` followed by the
existing `v7-egress-set-state` reservation owner.

Re-entry condition: an owner-verified egress profile/peer configuration is
available as an existing ready draft or empty isolated source.  The existing
selector then automatically performs:

`source reservation -> one certification identity -> controlled condition -> ordinary Matrix -> Candidate -> Packet -> lease -> cutover -> Time receipt`.

Only then can the measurement loop collect the required five valid samples and
evaluate the p95/max CT-M0F gate.  This report does not claim a latency sample,
client recovery, Natural L8 evidence, or CT-M0F completion.

---

# V7 routing/failover reality audit и архитектурный verdict

Дата: `2026-08-13`  
Production commit: `75aef37213e165f1fe6e32aeb7b8cb433a49570e`  
Режим: read-only; implementation changes `NONE`.

## Решение

**Verdict B — построить минимальный routing core рядом с legacy V7 и
мигрировать поэтапно.** Текущий V7 сохранить как policy/evidence/governance
control plane и legacy exception path, но перестать использовать весь его
engineering lifecycle как синхронный product hot path.

Пять причин:

1. Production Matrix запускается раз в `15 min` с jitter до `60 s`; быстрый
   Telegram sentinel работает раз в `4 s`, но запущен с `--no-autoswitch` и не
   является execution wake.
2. Пять последних no-action Matrix cycles заняли `4:48.892–5:21.934`; advisory
   регулярно исчерпывает свой `90 s` timeout. Это происходит даже без route
   apply.
3. Измеренный successful forward path равен `58.761588 s`, но собственно route
   mutation занимает только `0.857997 s`, а visibility `0.020036 s`.
4. Прямой executable path охватывает 5 крупных файлов / `41,821 LOC`; вместе с
   реально загружаемыми safety/governance owners — 13 файлов / `85,859 LOC`.
5. Текущий per-user writer берёт global lock и полностью переписывает
   `users.registry`; поэтому упрощение orchestration может помочь одному
   пользователю, но не устраняет O(N) cohort architecture.

Дополнительная current-truth проблема: live Matrix projection показывает для
VLESS `affected ordinary scope=0` и `controlled certification scope=11`, тогда
как source CPS всё ещё показывает active incident `affected=40/unresolved=40`.
Следовательно, CPS/OMP projection сейчас не может быть источником
предcutover scope; routing core должен читать текущую assignment/Matrix
generation, а legacy CPS потреблять результат асинхронно.

## Фактический production graph

```text
v7-service-matrix-refresh.timer (15 min + <=60 s jitter)
-> v7-service-matrix-refresh-all
-> 7 x v7-service-matrix-test
-> 98 service probes (7 egress x 14 services)
-> service-matrix.json + service-failure-events.jsonl
-> v7-users-autoswitch --consume-passive-events-only
-> v7-users-autoswitch --consume-service-failure-automation-only
-> v7-truth-check --consume-service-failure-automation-only
-> bounded/availability/topology/CT-M0F consumer selection
-> v7-governed-canary-dry-run-cycle
-> AutoswitchPlanner.plan
-> Candidate -> Packet -> lease -> restore barrier
-> v7-users-autoswitch apply
-> v7-user-switch
-> v7-operator-execution-packet control validation
-> ip route replace
-> route visibility + required service verification
-> Outcome/Replay/Learning/closure
```

`v7-telegram-sentinel.timer` observes every `4 s`, but its production command
contains `--no-autoswitch`; therefore it is currently a parallel observer, not
the beginning of the routing hot path.

## Stage disposition

| Stage | Owner / file / process | Input -> output | Blocking | Measured/available time | Required before apply | POST-APPLY candidate |
| --- | --- | --- | --- | ---: | --- | --- |
| Detection schedule | systemd Matrix timer | time -> Matrix generation | yes | `15 min` cadence + jitter | no; event-driven signal is enough | n/a |
| Service observation | `v7-service-matrix-refresh-all` -> 7 `v7-service-matrix-test` | egresses -> 98 observations | yes | `46.5–48.8 s` Matrix portion | only failed-source confirmation and fresh target receipt | broad inventory/probes yes |
| Incident capture | Matrix event owner | Matrix -> event/scope | yes | included | compact event yes | historical projections yes |
| Passive reconciliation | autoswitch passive consumer | events/stores -> closure projections | yes | `13.6–24.0 s` observed | no | yes |
| Full advisory/Planner | autoswitch advisory | all state/snapshots -> plan/shadow | yes | repeatedly `>=90 s`, timeout | only bounded target decision | full advisory yes |
| OMP consumption | `v7-truth-check` | obligation -> frontier receipt | yes | `3.9–6.8 s` observed | no routing-safety need | yes |
| Policy/action-class gates | Matrix/governed/operator owners | policy/audit -> admission | yes | part of Planner | compact current policy/generation yes | history/reconciliation yes |
| Candidate/Packet/lease | governed + `operator_execution` | decision -> one-use artifacts | yes | `0.235222 s` measured | yes, but may be one compact object/CAS | full evidence expansion yes |
| Restore barrier | operator execution owner | Packet/lease -> clearance | yes | `0.259674 s` | one current safety token yes | lifecycle publication yes |
| Repeat Planner/live reads | autoswitch child | registries/snapshots -> same target | yes | Planner `17.307274 s`; child policy/capacity `3.276124 s`, allocation `6.201925 s` | no full rebuild | yes |
| Kernel apply | `v7-user-switch` | user,target -> route table + assignment | yes | `0.857997 s` forward; `1.262341 s` reset | yes | no |
| Visibility | autoswitch verifier | route truth -> visible | yes | `0.020036 s` | yes | no |
| Full service verification | autoswitch | selected user/target -> service result | yes | `19.844211 s` | one fast payload/route probe only | full matrix yes |
| Audit/feedback/successor | autoswitch/governed/OMP | result -> durable evidence | yes today | `4.64–7.18 s` | only crash-recoverable closure obligation | Outcome/Replay/Learning yes |

## Quantitative current V7

| Metric | Current production reality |
| --- | --- |
| Active executable files | `5` direct product executables; `13` including imported safety/governance owners |
| LOC | `41,821` direct; `85,859` deployed reachable surface |
| Relevant processes | one systemd Matrix process plus at least `7` checker children, passive consumer, advisory, OMP, governed executor, autoswitch child, route writer and packet validator: lower bound `15` launches for an execution cycle |
| Timers | Matrix `15 min`; Telegram observer `4 s`; quality `5 min`; legacy autoswitch timer inactive |
| Producer->consumer hops | `12` through verified route, `9` before kernel apply |
| State surfaces read before apply | lower bound `17` named families: registries, Matrix, policy/org policy, safety, quality/load/activity/reconnect, intelligence snapshots, event/audit/closure, execution control, lease/barrier |
| Durable writes before apply | lower bound `6`: Matrix/event, obligation/audit, Candidate/Packet, lease, clearance/barrier |
| Locks | at least `4` domains: Matrix writer, Planner/service-Matrix, operation/policy audit, global user-switch lock |
| Network probes | `98` per full Matrix generation before routing; later route/payload/service verification adds more |
| Pre-apply governance/evidence stages | at least `7`: capture, passive reconciliation, advisory, OMP, action-class policy, Packet/lease, restore clearance |
| Observed no-action lifecycle | `288.9–321.9 s` wall |
| Measured successful forward | `58.761588 s` excluding detection cadence |
| Measured forward+reset | `141.353447 s` |
| Actual kernel mutation + visibility | about `0.878 s` forward |

Counts are explicit lower bounds where the existing Time owner does not expose
files-opened/fsync counters. Unknown values were not converted to zero.

## Repeated work and classification

Repeated before cutover:

- Matrix/service observations are produced, then target health/capacity is
  resolved again inside Planner and apply child;
- Autoswitch is instantiated for passive capture, advisory and execution;
- policy, capacity, quality, registries and snapshot generations are reread in
  parent and child;
- OMP consumes `NO_PENDING_OBLIGATION` on ordinary routing cycles;
- availability, topology and CT-M0F lanes are evaluated after an action-class
  miss even when they cannot own the ordinary incident;
- fingerprints and compact projections are repeatedly serialized;
- audit/feedback/successor publication blocks transaction completion.

Safety-critical before apply:

- fresh failed-source generation and exact affected scope;
- fresh lawful target health/capacity receipt;
- immutable policy/Authority generation and blast-radius ceiling;
- idempotency key, one active operation/lease, cooldown/anti-flap;
- compact source/target/assignment CAS;
- rollback or forward-recovery readiness;
- immediate route visibility and one exact payload probe.

`NON_HOT_PATH_CANDIDATE`:

- OMP scheduling and capability reconciliation;
- reports, certification history and Production Maturity;
- Polygon, replay and Learning;
- full service Matrix refresh when a compatible fresh receipt exists;
- broad inventory/snapshot refresh;
- historical incident reconciliation and closure expansion;
- full Outcome Passport materialization;
- percentile/campaign bookkeeping;
- post-action CPS projection.

These remain durable and mandatory where their Programs require them, but they
must consume a compact post-apply closure obligation asynchronously.

## Variant A — simplify current V7

Keep Matrix event schema, registries, policy/Authority validator,
`v7-user-switch`, route verifier and closure consumers. Move passive/OMP/
Learning/history and full service verification after apply; collapse duplicate
Planner reads into one generation snapshot; connect the fast sentinel to a
bounded existing consumer.

Best credible result: `3–10 s` one-user cutover after detection. Runtime stages
can fall from about 12 to 6, state surfaces from >=17 to about 8, and process
launches from >=15 to 4–6. However the 23k-line Planner, 12k-line governed
executor and O(N) registry writer remain coupled. Cohort cost and regression
risk remain high. Estimated change: several thousand lines across at least
5–8 large owners, with a high chance that governance work leaks back into the
critical path.

Minimum safe existing chain:

```text
fresh failure receipt
-> current affected-scope snapshot
-> cached target receipt + compact policy/generation validation
-> compact Packet/lease/CAS
-> v7-user-switch
-> route visibility + one payload probe
-> durable closure obligation
-> asynchronous legacy consumers
```

This is useful as a migration adapter and legacy fallback, not as the final
10,000-user architecture.

## Variant B — minimal routing core beside legacy V7

```text
OBSERVE -> STATE -> PLAN -> APPLY -> VERIFY
                         -> durable closure obligation -> legacy V7 async
```

Estimated shape: `5–7` focused modules, `2,500–5,000 LOC`, one long-lived
process plus the kernel, `3–5` compact state surfaces, no Python/process startup
between decision and apply. Warm prepared-decision target: `<1 s`; conservative
first production gate: `<3 s` from confirmed failure to verified traffic.

Reuse from V7:

- service/failure schema and target health receipts;
- current users/egress identity and policy inputs;
- delegated Authority envelope and blast-radius rules;
- cooldown, anti-flap, capacity and correlation constraints;
- route writer semantics, verification corpus and rollback/forward recovery;
- existing tests, Polygon scenarios and production evidence as acceptance
  corpus.

Minimum core state:

1. generation-bound source/target health and capacity snapshot;
2. current assignment or class-membership generation;
3. immutable active policy generation;
4. one operation lease/idempotency record;
5. append-only compact apply/verify receipt or WAL.

Safety contract inside core: fresh generations, exact source/target identity,
bounded user/cohort ceiling, capacity reserve, one active transaction,
anti-flap/cooldown, idempotent CAS, deterministic rollback/forward recovery,
kernel visibility and payload verification. OMP, reports, Learning, Polygon,
Maturity, replay and expanded evidence stay in legacy V7 asynchronously.

Migration without big bang:

1. Shadow: consume copied V7 inputs and compare decisions; effects zero.
2. One certification user: core prepares decision; existing governed owner
   admits one effect; compare route/outcome with legacy.
3. One ordinary user under existing bounded policy and live circuit breaker.
4. Bounded cohorts with class/bucket kernel indirection; legacy handles pinned,
   contradictory and migration exceptions.
5. Make core primary only after production latency, rollback, crash recovery and
   decision-equivalence gates pass; retire duplicate legacy stages gradually.

Migration complexity is medium, but bounded: the core is additive and can be
disabled instantly while legacy remains authoritative. This is lower risk than
removing interleaved governance from 85k LOC in place.

## Preserve / exclude / reuse / retire

Must preserve: policy and Authority semantics, identity/assignment truth,
capacity and target-health inputs, exact freshness/invalidation rules,
anti-flap/cooldown, circuit breaker, idempotency, rollback/forward recovery,
route and payload verification, append-only evidence lineage.

Must not enter the new hot path: OMP/CPS scheduling, report generation,
Maturity, Learning, Replay, Polygon execution, broad certification history,
full inventories, historical reconciliation, full Matrix when a fresh
compatible receipt exists.

Use as tests/evidence/Polygon corpus: current scenario corpus, Candidate/Packet
contracts, failure classifications, controlled-production outcomes, route and
payload verifier fixtures, rollback/no-rollback histories, Time receipts and
hidden-O(N) guards.

Gradually retire from primary routing: 15-minute Matrix as execution wake,
duplicate Planner construction, repeated snapshot/policy reads, OMP `NO_WORK`
calls in ordinary cycles, per-user process spawning, full registry rewrite per
move, synchronous expanded closure and full service verification before
traffic recovery. Preserve them only as legacy exception/reconciliation paths
until migration evidence closes their consumers.

Final terminal:

`ROUTING_REALITY_AUDIT_CONSUMED_VERDICT_B_MINIMAL_CORE_BESIDE_LEGACY_RECOMMENDED`

---

# V7 System Reset and Routing Core Migration Program Creation

Status: `CREATED_REGISTERED_READY_FOR_RESET_M0`

Program ID: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1`

Program file: `docs/programs/V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM.md`

Exact Program owner: existing `OMP` development-plane orchestrator; CPS remains the sole volatile state owner.

Primary goal: preserve useful V7 knowledge, freeze legacy routing hot-path capability growth, audit and disposition the complete Program/owner/truth portfolio, specify V7 vNext, and only then build and migrate a minimal Routing Core beside legacy.

Freeze state: `LEGACY_V7_ROUTING_HOT_PATH = FROZEN_FOR_CAPABILITY_GROWTH` as a Program-level engineering rule.

Current production: existing legacy V7 Runtime remains production authority and fallback.

Implementation effects: `NONE`.

Runtime / routing / users / Authority / migration effects: `NONE`.

First executable phase: `RESET-M0`.

Next exact successor: `EXECUTE_RESET_M0_FULL_PROGRAM_PORTFOLIO_AUDIT_AND_FREEZE_RECONCILIATION` through existing OMP/CPS lifecycle.

Existing Programs: preserved; their disposition is deferred to `RESET-M0/RESET-M1`.

Creation terminal: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1 = CREATED_REGISTERED_READY_FOR_RESET_M0`.

---

# V7 System Reset Program Intent-Reality and Complexity Contract Update

Status: `UPDATED_WITH_INTENT_REALITY_COMPLEXITY_AND_DEVELOPMENT_SYSTEM_FAILURE_AUDIT_CONTRACTS_READY_FOR_RESET_M0`

Program ID: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1`

Program version/update: existing V1 contract strengthened in place; no new Program created.

Added internal phases: `RESET-M0B — CODE_REALITY_AND_COMPLEXITY_AUDIT`, `RESET-M0C — DUPLICATION_DEAD_CODE_AND_LEGACY_SURFACE_AUDIT`, and `RESET-M1B — OMP_AND_DEVELOPMENT_SYSTEM_FAILURE_ANALYSIS`.

Intent-vs-Reality contract: every Program, Capability, and major owner must prove `INTENDED -> DOCUMENTED -> IMPLEMENTED -> REAL PRODUCER -> REAL NON-TEST CALLER -> REAL CONSUMER -> CONSUMPTION VERIFIED -> BEHAVIOR CHANGED -> PRODUCT EFFECT -> LEGAL TERMINAL / NEXT CONSUMER` and receive an explicit factual verdict.

Development-System Failure Audit: RESET-M1B must explain why local completion and protection rules did not preserve parent/product intent, classify OMP laws, distinguish real safety from legacy development protection, and resolve `RESET_OMP_CONTRACT_CONFLICT` before Core implementation.

System Complexity metrics contract: factual baseline/current/delta fields cover production/hot-path/Core LOC, modules, owners, processes, timers, state surfaces, pre-apply hops/writes, lock domains, and critical-path subprocesses. No synthetic score is created.

Large-file rule: `FILE_SIZE_IS_A_SIGNAL_NOT_A_VERDICT`; decomposition must reduce semantic/system coupling and follow owner-backed responsibility/change-reason/consumer/lifecycle evidence, never mechanical file splitting.

RESET-M9 gate: `LEGACY_RETIREMENT_SYSTEM_SHRINK_AND_PROGRAM_CLEANUP` requires physical surface reduction and disposition of legacy files/functions/modules/CLIs/services/timers/state surfaces/owners/Programs/projections/reconciliation paths while preserving required historical evidence.

OMP conflict rule: owner-backed Reset evidence conflicting with historical OMP architectural assumptions materializes `RESET_OMP_CONTRACT_CONFLICT` for RESET-M1B resolution. Real safety, Authority, rollback, verification, and production-mutation boundaries remain mandatory.

Runtime effects: `NONE`.

Production effects: `NONE`.

Routing/user/Authority/Core/migration/legacy-deletion effects: `NONE`.

First executable phase remains: `RESET-M0 — SYSTEM_REALITY_PROGRAM_INTENT_AND_PRODUCT_CONTRACT_AUDIT`.

Exact first successor remains: `EXECUTE_RESET_M0_FULL_PROGRAM_PORTFOLIO_AUDIT_AND_FREEZE_RECONCILIATION`.

Terminal: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1 = UPDATED_WITH_INTENT_REALITY_COMPLEXITY_AND_DEVELOPMENT_SYSTEM_FAILURE_AUDIT_CONTRACTS READY_FOR_RESET_M0`.

---

# V7 Master Project Handoff Reset Strategy Sync

Status: `COMPLETE_CONSUMED`

Date: `2026-08-13`

Scope: canonical handoff synchronization only.

## Result

The existing `docs/reference/V7_MASTER_PROJECT_HANDOFF.md` was updated in place. No
parallel handoff, Program, roadmap, owner, Runtime, Planner, queue, scheduler or state
store was created.

The handoff now points to CPS Section 0 as the only volatile live-state owner,
registers `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1`, preserves the
accepted routing reality audit and Variant B decision, records the legacy hot-path
freeze, Reset phase structure, OMP audit boundary, Minimal Routing Core positive and
negative contracts, migration safety, Authority law, complexity/shrink requirements,
CT-M0F disposition, exact current snapshot and new-chat startup sequence.

Removed current-state ambiguity: the historical FSSE/safe-deploy frontier is no
longer presented as the current next action. The dated handoff snapshot resolves to
`RESET-M0` and
`EXECUTE_RESET_M0_FULL_PROGRAM_PORTFOLIO_AUDIT_AND_FREEZE_RECONCILIATION`, while
future reads are explicitly required to use fresh CPS Section 0.

## Effects

- Runtime changes: `NONE`
- Routing changes: `NONE`
- User movement: `NONE`
- Authority changes: `NONE`
- Program execution: `NONE`
- RESET-M0 execution: `NONE`
- Routing Core implementation: `NONE`
- Legacy deletion: `NONE`

## Verification

The synchronized handoff plus CPS Section 0 and the active Reset Program now answer:
what V7 is; why Reset is required; what remains production-active; what is frozen;
the vNext target; OMP's role; current phase/successor; forbidden actions; and which
accepted facts must not be rediscovered.

Final terminal:

`V7_MASTER_PROJECT_HANDOFF = CURRENT_SYNCHRONIZED_FOR_SEAMLESS_NEW_CHAT_CONTINUATION`

---

# V7 Reset Program Exhaustive Bounded Audit and Core Safety Update

Status: `COMPLETE_CONSUMED`

Date: `2026-08-13`

Program: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1`

## Purpose

Strengthen the existing Reset Program so simplification is exhaustive, evidence-led
and finite: no production function or semantic contract may be lost, but valid work
cannot be repeatedly re-audited and unnecessary legacy surface must eventually be
removed rather than merely bypassed.

## Contract changes

- Added immutable Reset scope snapshot, stable audit identities and complete
  repository/production entrypoint-to-function-to-consumer coverage.
- Added semantic dynamic-dispatch/systemd/subprocess/config reachability and explicit
  unresolved classifications so absence from a static call graph is never deletion
  proof.
- Added `AUDIT_ONCE_UNLESS_EXACT_INVALIDATION_TRIGGER`, delta-ledger reuse and dynamic
  compression to prevent perpetual audit cycles.
- Added mandatory portfolio, reachability, producer-consumer/state-effect,
  duplication/dead/legacy, residual and coverage outputs through existing document
  owners only.
- Added strict evidence requirements before later merge/delete and preservation of
  historical, regression, legal, Learning and Authority provenance.
- Added exact end-to-end recovery clock and exact client-context payload probe.
- Added single-writer/fencing and atomic Legacy/Core ownership-transfer law.
- Added recoverable apply-to-asynchronous-closure crash boundary.
- Added explicit fresh/stale control-input decisions without broad Core
  reconciliation.
- Made `<3 s` the initial end-to-end production gate and prepared compatible
  warm-path `p95 < 1 s` a mandatory RESET-M7/final gate rather than an optional
  evaluation.

## Effects

The existing CPS Program-state projection and OMP Program registration were aligned
with the strengthened contract. They record contract semantics only and do not
advance or execute a Reset phase.

- RESET-M0 execution: `NONE`
- Code audit execution: `NONE`
- Runtime/routing/user effects: `NONE`
- Authority/migration effects: `NONE`
- Core implementation: `NONE`
- Legacy removal: `NONE`

Final terminal:

`V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1 = UPDATED_WITH_EXHAUSTIVE_BOUNDED_AUDIT_AND_SAFE_CORE_MIGRATION_CONTRACTS_READY_FOR_RESET_M0`

---

# V7 Reset Program Deep Relationship and Master Report Closure Update

Status: `COMPLETE_CONSUMED`

Date: `2026-08-13`

Program: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1`

## Finding

The existing Program already required exhaustive inventory, reachability,
producer-consumer/state-effect evidence and bounded audit reuse. It did not yet make
the cross-layer Program/component/function relationship proof or one comprehensive
self-reviewed audit report an explicit collective RESET-M0 through RESET-M1B gate.

## Update

- Added the exact relationship chain from Product goal and Program intent through
  Capability, owner, process, file/function, state/effect and real consumer to product
  result and successor/terminal.
- Added semantic edge fields and relationship types covering direct calls, dynamic
  dispatch, subprocess/systemd, state exchange, probes/APIs, wakeups, Authority,
  Runtime effects, verification, rollback, reports and CPS/OMP successors.
- Required detection of orphan producers/consumers, dead/circular edges, duplicate
  writers, hidden synchronous work, stale projections, manual bridges, sequencing
  errors, no-progress loops and locally successful functions without product effect.
- Added `DEEP_PROGRAM_COMPONENT_FUNCTION_RELATIONSHIP_GRAPH_PROVEN`.
- Added one readable `V7_SYSTEM_RESET_MASTER_AUDIT_REPORT` for RESET-M0 through
  RESET-M1B with executive findings, detailed evidence, portfolio, relationship
  graph, state/effect ownership, complexity, root causes, dispositions and exact
  RESET-M2/M3 inputs.
- Added an internal draft/cross-check/coverage/contradiction/root-cause/product-trace/
  targeted-recheck/final-self-review loop that repeats only exact weak or missing
  criteria and never restarts valid audit work.
- Required phase reports for RESET-M2 through RESET-M9 and one final
  `V7_SYSTEM_RESET_PROGRAM_COMPLETION_REPORT` that proves every original Program
  goal through distinct code, caller, consumer, deploy, Runtime, production, user,
  Authority, recovery and physical-deletion evidence classes.
- Added explicit evidence classifications and prohibited superficial completion by
  report length, headings, tool activity, counts or rendered diagrams alone.
- Aligned CPS and the existing OMP Program registration. No Reset phase was executed.

## Effects

- Runtime/routing/user/Authority effects: `NONE`
- RESET-M0 execution: `NONE`
- Code or legacy removal: `NONE`
- Core implementation/migration: `NONE`

Final terminal:

`V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1 = UPDATED_WITH_DEEP_RELATIONSHIP_AUDIT_AND_MASTER_REPORT_CLOSURE_READY_FOR_RESET_M0`

---

# V7 Reset Overhead Budget and Execution Readiness

Status: `COMPLETE_CONSUMED`

Date: `2026-08-13`

Program: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1`

## Discovery and reuse

The existing Program already prohibited a parallel Runtime/Planner/owner/store,
treated audit matrices/graphs as report projections, required necessity proof and
system shrink, and kept RESET-M0/M0B/M0C disposition-only. The semantic gap was that
temporary Reset overhead, logical-versus-physical outputs, behavior-versus-legacy
structure, risk-proportional depth and audit/mutation separation were not explicit
collective laws.

## Minimal contract update

The existing Program was strengthened in place with `RESET_OVERHEAD_BUDGET`,
`LOGICAL_OUTPUT_NOT_PHYSICAL_SYSTEM`,
`PRESERVE_REQUIRED_BEHAVIOR_NOT_LEGACY_STRUCTURE`,
`QUESTION_NECESSITY_BEFORE_OPTIMIZING_IMPLEMENTATION`,
`EVIDENCE_DEPTH_PROPORTIONAL_TO_RISK`,
`DEFAULT_OUTCOME_OF_RESET = SYSTEM_SHRINK_NOT_CODE_REORGANIZATION`, and
`STRICT_AUDIT_MUTATION_SEPARATION`.

Reset-only artifacts now require purpose, owner, production class, lifetime and
retain/merge/archive/delete disposition. Temporary growth requires an exact later
shrink disposition. Full coverage remains mandatory, while evidence depth follows
production/safety/Authority/migration/deletion risk.

The existing CPS projection, OMP registration and Canonical Reference durable-law
list were aligned. Active Program, phase and successor did not change.

## Current boundary

- Active Program: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1`
- Phase: `RESET-M0`
- Successor: `EXECUTE_RESET_M0_FULL_PROGRAM_PORTFOLIO_AUDIT_AND_FREEZE_RECONCILIATION`
- RESET-M0 execution: `NONE`
- Runtime effects: `NONE`
- Production effects: `NONE`
- Routing effects: `NONE`
- Authority effects: `NONE`

Final terminal:

`V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1 = RESET_PROGRAM_CONTRACT_READY_FOR_EXECUTION`

---

# V7 Reset Report Depth Without Bloat Contract

Status: `RESET_PROGRAM_CONTRACT_READY_FOR_EXECUTION`

Program: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1`

## Change

The existing Reset Program reporting and bounded-audit sections were strengthened in place with `REPORT_DEPTH_WITHOUT_REPORT_BLOAT`, `NECESSARY_DEPTH_WITHOUT_UNIFORM_DEPTH`, and `LOGICAL_OUTPUT_NOT_DOCUMENTATION_EXPLOSION`. Master-report self-review is now explicitly a quality check over failed or unproven criteria followed by targeted recheck and finalization, bounded by `AUDIT_ONCE_UNLESS_EXACT_INVALIDATION_TRIGGER`. Later phase reports remain compact but evidence-complete and do not repeat the Master Audit Report.

## Reason and Risk Closed

The patch preserves exhaustive coverage, deep relationship/root-cause analysis, evidence-driven dispositions and the Master Audit Report while preventing audit projections, repeated representations and self-review from becoming a new permanent documentation subsystem or perpetual audit loop.

## Owners and Effects

Affected owners: existing Reset Program contract and existing Engineering Report evidence owner only. OMP, CPS, Canonical Reference, SYSTEM_MAP, Runtime, routing and Authority ownership are unchanged.

Runtime effects: `NONE`.

Production effects: `NONE`.

Authority effects: `NONE`.

Migration state effects: `NONE`.

First executable phase remains `RESET-M0`.

Exact successor remains `EXECUTE_RESET_M0_FULL_PROGRAM_PORTFOLIO_AUDIT_AND_FREEZE_RECONCILIATION`.

---

# RESET-M0 Scope and Initial Reality Reconciliation

Status: `RESET_M0_IN_PROGRESS_EXHAUSTIVE_COVERAGE_NOT_YET_COMPLETE`

Program: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1`

## Intent

Start the exact CPS successor `EXECUTE_RESET_M0_FULL_PROGRAM_PORTFOLIO_AUDIT_AND_FREEZE_RECONCILIATION` without Runtime, routing, Authority, migration or legacy mutation, and establish the immutable owner-backed audit scope before any disposition or Core design.

## Scope identity

- workspace: `/Users/ponch/Documents/New project`;
- branch: `Updatesystem`;
- source commit: `7ffa4c06bab741f266070e6506987e320e828922`;
- volatile owner: CPS Section 0;
- active Program: `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1`;
- phase: `RESET-M0`;
- production owner: existing legacy Runtime and Authority owners;
- existing documentation-only worktree changes: preserved, not overwritten or treated as Runtime truth.

## Initial evidence and conclusions

1. Program surface contains 16 current-looking files under `docs/programs`; OMP is 11,112 lines, Service Failure Automation 4,793, BDP 2,923, CPS 2,870, AEP 2,265 and Stage 2 2,242. Their file/status labels are inventory evidence only and do not prove live necessity or product effect.
2. The consumed routing reality audit proves a direct executable surface of 41,821 LOC and a reachable safety/governance surface of 85,859 LOC, at least 9 pre-apply hops, 17 state surfaces and 6 durable writes. Kernel mutation plus visibility is approximately 0.878 s while measured successful forward lifecycle is 58.761588 s.
3. Current source files confirm the concentration: `tools/v7_sync_lib.py` 25,279 LOC/306 functions; `tools/v7-users-autoswitch` 23,167/309; `admin_core/autonomy_trust_acceleration.py` 13,892/200; `tools/v7-governed-canary-dry-run-cycle` 12,694/103; `admin_core/operator_execution.py` 8,853/161; `admin_core/operator_execution_pipeline.py` 5,020/95; `tools/v7-service-matrix-refresh-all` 4,350/46. File size is a risk signal, not a disposition.
4. The verified production graph contains scheduled Matrix observation, multiple probe children, passive reconciliation, advisory/Planner, OMP consumption, governed Packet/lease/barrier, repeated reads, per-user writer, visibility/payload verification and synchronous closure. This proves extensive engineering/control-plane placement around a sub-second kernel effect.
5. CPS Section 0 correctly selects Reset M0, but retains service-failure generation/incident/Authority fields that contradict the new Reset frontier and the current Matrix scope. CPS therefore remains the volatile Program owner, but its legacy operational projections require exact classification and cannot become pre-cutover routing truth.
6. Real legacy consumers retain hard-coded Service Failure/Polygon Program identities and normalized CPS defaults in `tools/v7_sync_lib.py`, `tools/v7-users-autoswitch`, `admin_core/operator_execution.py` and governed execution. Reset is registered in CPS/OMP but not consumed consistently by these owners, directly explaining the `ACTIVE_PROGRAM` and continuation divergence.

## Intent Reality state

The fundamental routing Product Contract is `PARTIALLY_REALIZED`: real producers, callers, consumers, route mutation and verification exist, but the end-to-end recovery intent is obstructed by scheduling, repeated broad observation/planning, synchronous engineering reconciliation, duplicated reads/processes, and O(N) assignment persistence. Existing completion/certification claims prove local contracts; they do not prove the primary recovery contract.

## Residual

RESET-M0 is not complete. Required residual is exhaustive Program/Capability/Mission/owner Intent Reality disposition plus complete production entrypoint and dynamic-dispatch coverage. RESET-M0B/M0C must then classify every production-relevant function/service/timer/state/effect and duplication/dead/legacy surface. No portfolio disposition is accepted by this progress report.

## Effects and successor

Runtime effects: `NONE`.

Production effects: `NONE`.

Authority effects: `NONE`.

Routing/user/migration effects: `NONE`.

Owner: existing OMP/CPS Reset lifecycle.

Exact successor: continue `RESET-M0` coverage from the immutable scope, then enter `RESET-M0B` only after the M0 completion contract is proven.

---

# RESET-M0 Completion and RESET-M0B Activation Engineering Report

Status: `RESET_M0_SYSTEM_REALITY_INTENT_AND_PRODUCT_CONTRACT_AUDIT_COMPLETE`

## What changed

The existing Master Audit Report now closes RESET-M0 against its immutable source scope. CPS Section 0 and the two OMP current-state projections advance from RESET-M0 to the existing exact RESET-M0B successor. No new Program, owner, roadmap, truth source, Runtime, Planner, queue, generator or parallel contract was created.

## Why

RESET-M0 now accounts for every Program, capability group, executable tool, `admin_core` module and systemd/process family through an evidence-backed Intent Reality verdict or an exact phase-owned residual. Holding the frontier at RESET-M0 would repeat already-proven audit work and violate `AUDIT_ONCE_UNLESS_EXACT_INVALIDATION_TRIGGER`.

## Risk closed

The transition closes the risk of both premature phase completion and unbounded audit repetition. Function-level and dynamic-edge uncertainty remains explicit and is routed to RESET-M0B; it is not hidden, treated as dead code or used to authorize mutation.

## Owners affected

- CPS remains sole volatile frontier owner.
- OMP remains the existing development-plane orchestrator and pointer projection.
- The Reset Program remains the active Program contract.
- Canonical Reference, SYSTEM_MAP, Runtime, production routing, safety and Authority owners are unchanged.

## Evidence and residual

- Evidence: `docs/reports/engineering/V7_SYSTEM_RESET_MASTER_AUDIT_REPORT.md`.
- Consumed intent: RESET-M0 System Reality, Program Intent and Product Contract audit.
- Residual: production-relevant function, caller, state/effect and dynamic-dispatch classification.
- Exact successor: `EXECUTE_RESET_M0B_CODE_REALITY_AND_COMPLEXITY_AUDIT`.

## Effects

- Runtime effects = `NONE`.
- Production effects = `NONE`.
- Authority effects = `NONE`.
- Routing/user/deploy/migration effects = `NONE`.

---

# RESET-M0B Completion and RESET-M0C Activation Engineering Report

Status: `RESET_M0B_CODE_REALITY_COMPLEXITY_AND_RELATIONSHIP_MANIFEST_COMPLETE`

RESET-M0B accounted for 73 parseable code files, 129,532 LOC, 2,290 functions and 34 classes through the existing Master Audit Report. High-impact mutation, recovery and Authority owners received deep responsibility, caller/process, state/effect and large-file disposition analysis; lower-risk UI/read-model/support surfaces retained sufficient owner classification without uniform Runtime-depth analysis.

The phase proves mixed responsibilities and wrong placement in the legacy synchronous lifecycle while preserving required Authority, lease, replay/idempotency, restore, rollback and route/payload verification semantics. It creates no deletion decision and treats static no-caller evidence as insufficient.

Risk closed: large-file decomposition can no longer be justified mechanically, and external/dynamic caller uncertainty cannot silently become dead-code proof.

Owners affected: existing CPS volatile frontier and OMP pointer projection only. Runtime, production routing, canonical ownership, safety and Authority boundaries are unchanged.

- Evidence: `docs/reports/engineering/V7_SYSTEM_RESET_MASTER_AUDIT_REPORT.md`.
- Residual: duplicate/no-live-consumer/manual/test/historical/legacy surface disposition.
- Exact successor: `EXECUTE_RESET_M0C_DUPLICATION_DEAD_CODE_AND_LEGACY_SURFACE_AUDIT`.
- Runtime effects = `NONE`.
- Production effects = `NONE`.
- Authority effects = `NONE`.

---

# RESET-M0C Completion and RESET-M1 Activation Engineering Report

Status: `RESET_M0C_DUPLICATION_DEAD_CODE_AND_LEGACY_DISPOSITION_COMPLETE`

RESET-M0C classified every inventoried code/service/CLI identity through product, async engineering, legacy exception, manual, test, historical, duplicated or exact external-residual classes. No object was marked dead or removable from age, size, name or missing static caller. Required safety, Authority, rollback, recovery and route/payload verification semantics remain protected.

Risk closed: duplication and legacy classification cannot trigger audit-phase deletion or erase external/manual consumers.

Owners affected: CPS volatile frontier and OMP pointer projection only; existing Program, Runtime, production, safety and Authority owners are unchanged.

- Evidence: `docs/reports/engineering/V7_SYSTEM_RESET_MASTER_AUDIT_REPORT.md`.
- Exact successor: `EXECUTE_RESET_M1_PROGRAM_PORTFOLIO_DISPOSITION`.
- Runtime effects = `NONE`.
- Production effects = `NONE`.
- Authority effects = `NONE`.

---

# RESET-M1 Program Portfolio Disposition Engineering Report

Status: `RESET_M1_ALL_EXISTING_PROGRAM_DISPOSITIONS_OWNER_BACKED`

All 16 existing Program/state documents received exactly one target disposition in the Master Audit Report. Permanent owners remain; useful acceptance/safety evidence is preserved; overlapping Polygon and Service Failure lifecycles are directed to later merge; completed lifecycle Programs are directed to later close; OMP and Service Failure execution are directed to redesign. No source document was removed or rewritten by this phase.

Risk closed: useful intent cannot be lost with legacy machinery, and completed or overlapping Programs cannot silently remain permanent parallel roadmaps.

Owners affected: none changed. CPS remains volatile owner, OMP remains development orchestrator, and Runtime/safety/Authority owners remain intact.

- Evidence: `docs/reports/engineering/V7_SYSTEM_RESET_MASTER_AUDIT_REPORT.md`.
- Exact successor: `EXECUTE_RESET_M1B_OMP_AND_DEVELOPMENT_SYSTEM_FAILURE_ANALYSIS`.
- Runtime effects = `NONE`.
- Production effects = `NONE`.
- Authority effects = `NONE`.


---

<!-- Source report: docs/reports/engineering/2026-08-13_360000_post_reset_reality_check.md -->

# POST_RESET_REALITY_CHECK_REPORT

Status: `POST_RESET_REALITY_CHECK_COMPLETE`

## 1. Purpose

Bounded read-only verification that the completed `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_PROGRAM_V1`, its `FINAL_ARCHITECTURE_MAP`, deployed Runtime and observable production behavior still describe the same system. This report creates no Program, architecture, owner, Runtime, state surface or correction cycle and performs no mutation, deployment, refactor or deletion.

Evidence boundary: fresh `tools/v7-truth-check --all --json`; fresh read-only `tools/v7-safe-deploy --json` production hash/delta; production snapshot `.v7/runtime_convergence_snapshot.json` collected `2026-08-13T10:53:32Z`; existing M8/M9 production apply/fallback/kernel evidence; deployed unit definitions and current source caller/effect inspection. Deep evidence remains with those owners and is not copied here.

## 2. Checked surfaces

- primary routing dependency boundary;
- allowlisted active/inactive production services and timers;
- every deployed routing-capable writer in the canonical package;
- M10 legacy exceptions and Engineering Plane dependencies;
- Assignment, Health, Policy, Capacity, Authority, Routing and Verification state;
- channel admission inputs, freshness and invalidation;
- final map and canonical document status;
- cleanup and natural-traffic residual.

## 3. Expected architecture

```text
CONTROL PLANE
assignments + Matrix/quality/runtime health + policy + capacity + Authority
                              |
                              v
DATA PLANE
v7-routing-sync -> nft user/class maps -> fwmark class routes -> interface -> verify
                              |
                              v
ENGINEERING PLANE (async only)
OMP / Reports / Polygon / Learning / Replay / campaigns
```

Governed autoswitch, per-user switch, Packet/lease/barrier and rollback are explicit bounded exceptions. They are not a continuously active second primary routing loop.

## 4. Actual production reality

Fresh truth result: `FULLY_ALIGNED`, CPS consistency `PASS`, zero contradictions, production Runtime truth `KNOWN`, production access `READY`. Local and GitHub point to `d8a2fa436123bd176522974f9861a2cfc376bbb2`; deployed copied-binary basis remains `b343732248f7f1c25d414c1e140e698d42d1cf62`. The difference is classified `DOCS_ONLY_MISMATCH`, `deployment_required=false`.

Fresh production hashes match the canonical package for `v7-routing-sync`, `v7-user-switch`, `v7-users-autoswitch`, `v7_sync_lib.py`, Routing Core, operator execution, Matrix/quality/sentinel tools, admin/read models and deployed systemd definitions. No runtime binary delta exists.

### Active process/timer evidence

| Process / unit | Purpose | Owner | Layer | Real consumer | Observed status / disposition |
| --- | --- | --- | --- | --- | --- |
| `v7-service-matrix-refresh.timer` | refresh current service/health evidence | Matrix owner | Control Plane | health/admission and governed Planner gates | `active (waiting)`; `KEEP_CONTROL_PLANE` |
| `v7-admin-api.service` | operator/read-model presentation and explicit actions | admin/read-model owners | Control/Engineering presentation | operator/API consumers | `active (running)`; `KEEP_CONTROL_PLANE` |
| `v7-users-autoswitch.service` | explicit governed planning/apply invocation | autoswitch/execution owners | Legacy exception | manual or exact governed action | `inactive (dead)`, approved manual mode; `FALLBACK_ONLY` |
| `v7-users-autoswitch.timer` | former periodic autoswitch entry | autoswitch owner | Legacy exception | no admitted primary consumer | enabled definition but `inactive (dead)`; `DISABLED`, must not become primary |
| intelligence snapshot refresh service/timer | prepared engineering/read-model snapshots | intelligence owners | Engineering Plane | Planner/read models when explicitly called | units not loaded in current snapshot; CLI exists; `KEEP_ENGINEERING`, not background primary |
| `v7-routing-sync` | reconcile/apply class dataplane | routing writer | Data Plane | kernel/client forwarding | executable deployed with matching hash; invoked for explicit reconciliation/restart, not a second daemon; `KEEP_RUNTIME` |

The allowlisted production truth contains no active autoswitch scheduler and explicitly reports `scheduler_inactive_approved_manual_mode=true`. No second primary routing loop was observed.

## 5. Matches

### Primary Runtime boundary

`PRIMARY_RUNTIME_BOUNDARY_REALITY_PASS`.

The actual primary forwarding owner consumes Assignment plus exact Core-promotion Policy/Authority and applies/validates nft/ip state. OMP, Reports, Learning, Replay, Polygon, campaigns, Production Maturity and historical reconciliation are absent from `v7-routing-sync` imports, inputs and apply/verify chain. Matrix and quality are asynchronous Control Plane producers; they do not forward traffic.

### Routing writer ownership

`ONE_PRIMARY_ROUTING_WRITER_PASS`.

| Component | Can mutate routing? | Why / owner | Primary or exception |
| --- | --- | --- | --- |
| `v7-routing-sync` | `YES` | exact Core promotion, atomic nft class apply, ip class route/rule apply, verify and fallback; routing writer owner | `PRIMARY` |
| nft/ip kernel | `YES` | forwarding-state executor consumed by routing writer | `PRIMARY DATAPLANE` |
| `v7-user-switch` | `YES` | exact bounded user assignment/route transaction | `EXCEPTION`; callable only through explicit governed/manual action |
| `v7-users-autoswitch` | `YES` only with apply path | Planner plus Authority/Packet/lease/barrier/verification gates | `EXCEPTION`; service/timer inactive |
| `legacy_sync` inside routing sync | `YES` | deterministic fallback restoration | `FALLBACK_ONLY`, not concurrently active primary |
| Matrix, quality, sentinel, OMP, Reports and Learning | `NO` | observation/engineering producers only | not writers |

Multiple mutation-capable binaries exist by design, but only one is primary; all others have an exact inactive, governed or fallback boundary.

### Engineering Plane isolation

`ENGINEERING_PLANE_ISOLATION_REALITY_PASS`.

OMP/CPS/report/learning/replay functions have real engineering consumers and no import/call edge into the Core dataplane apply. Production failure evidence can be consumed by the governed action path, but Report, Learning and History are post-action outputs rather than prerequisites. Neither forbidden chain `Runtime -> OMP -> routing decision` nor `failure -> Report/Learning/History -> switch` was found.

## 6. Mismatches

No architecture/runtime mismatch was found inside the canonical deploy allowlist and available production truth.

Evidence limitation, not an observed mismatch: the production truth owner exposes a bounded command allowlist rather than an unrestricted host-wide `systemctl list-units`, process and cron census. Therefore this report proves absence of a second primary loop across every canonical/deployed V7 owner and known unit, but does not claim omniscience about unrelated or unregistered host jobs. Owner: existing production truth/convergence owner. Impact: audit completeness wording only; current runtime verdict remains PASS. Correction path if independent evidence appears: extend the existing read-only truth owner after owner review, then targeted recheck; do not reopen Reset automatically.

## 7. Legacy exceptions

| Component | Why retained / real consumer | Owner | Not-primary proof | Removal condition |
| --- | --- | --- | --- | --- |
| `v7-users-autoswitch` | governed fallback, certification, exact action-class execution | Planner/autoswitch and execution owners | deployed hash matches; service and timer inactive/manual | equivalent Authority, rollback, verification and recovery semantics proven in production |
| `v7-user-switch` | bounded per-user apply/rollback primitive | Assignment/execution owner | no continuous unit; reached only by explicit governed/manual transaction | no remaining governed/fallback consumer and replacement semantics proven |
| Packet/lease/barrier and operator execution | fencing, exact Authority, stale/duplicate suppression, crash/rollback safety | operator-execution Authority owner | no forwarding without explicit transaction; not a primary daemon | equivalent safety proof under the same Authority owner |
| old Planner logic | target evaluation and governed exception path | Planner owner | autoswitch loop inactive; Core forwarding does not import it | no fallback/certification consumer and owner-backed retirement |
| `v7_sync_lib.py` | deploy/truth/CPS/OMP engineering lifecycle | deploy/truth and OMP owners | deployed library is not imported by `v7-routing-sync` | split/remove only if existing consumers disappear; size alone is insufficient |
| `legacy_sync` | exact deterministic Core fallback | routing writer | invoked only when exact Core Authority is absent or fallback is explicit | alternative verified fallback/recovery owner exists |

`LEGACY_EXCEPTION_REALITY_PASS`.

## 8. State and channel-health reality

| State | Owner/writer | Readers / real consumer | Lifecycle result |
| --- | --- | --- | --- |
| Assignment | users registry / Assignment owner | Routing Core, routing sync, governed Planner | current -> bounded mutation -> reconciliation; no duplicate owner observed |
| Health | Matrix, service test, quality and runtime probe owners | admission/Planner/admin consumers | refreshed asynchronously; generation/freshness bound |
| Policy | `/etc/v7/policy.json` policy owner | Core promotion and governed gates | exact hash/schema/scope; fail closed |
| Capacity | registry/load/capacity owners | target eligibility and governed Planner | fresh bounded decision; unknown blocks selection |
| Authority | policy plus operator-execution audit | apply gates | exact contract/transaction; no self-expansion |
| Routing | nft/ip kernel via `v7-routing-sync` | production packets and verification | apply -> verify; deterministic fallback |
| Verification | routing sync/kernel plus governed verifier | executor, truth and outcome owners | PASS/STOP/rollback terminal |

No orphan or competing current truth was found in these surfaces. Historical reports are evidence only; CPS is volatile state; Canonical Reference/SYSTEM_MAP own current architecture.

`CHANNEL_HEALTH_MODEL_REALITY_PASS`: existing eligibility logic composes transport/interface evidence, required service Matrix/route-class fitness, quality/stability and capacity/load constraints. It enforces freshness and source-generation binding; stale/missing facts stop or return unknown. Ping/TCP reachability alone cannot satisfy service suitability, quality and capacity gates and therefore cannot produce full admission.

## 9. Final map and cleanup verification

`FINAL_ARCHITECTURE_MAP_REALITY_ALIGNMENT_PASS` within the stated production-truth boundary.

Every mapped canonical deploy component exists with matching production hash. Active Matrix/admin surfaces have the documented Control Plane consumers. Autoswitch remains inactive/manual. The primary Core adapter and fallback binaries match the production package. No missing mapped owner or unexpected canonical runtime dependency was found.

Cleanup dispositions:

- `KEEP`: Core class dataplane, assignments, Policy/Authority, health observation and verification.
- `LEGACY_EXCEPTION`: governed autoswitch/user switch/Packet/lease/barrier/rollback and deterministic fallback.
- `ARCHIVE`: completed Programs and reports; none is live architecture or Runtime truth.
- `DISABLED`: periodic autoswitch timer.
- `REMOVE_CANDIDATE`: none admitted by this check; evidence limitations cannot authorize deletion.

Existing M9 proof remains current evidence that 124 legacy source rules and 124 legacy per-user primary routes were removed and Core verification/fallback passed. No new evidence invalidated it. No orphaned migration tail or hidden old primary path was observed.

## 10. Operational residuals and next actions

1. Natural traffic: the earlier limitation remains—no natural client packet arrived during the bounded nft counter window. This does not invalidate installed class maps, marked route proof, M6 payload proof, fallback proof or current architecture. A future ordinary packet may be observed read-only by the existing routing/kernel verification owner to confirm a class counter increment and selected interface. Do not generate traffic, move users or reopen Reset solely to obtain it.
2. Host-wide census: available production truth is bounded to canonical V7 units/commands. Recheck only if the existing truth owner gains an owner-approved host-wide read-only census or independent evidence names an unregistered V7 process/job.
3. Autoswitch timer: preserve inactive/manual state. Any proposal to enable it is a new operational decision requiring current Policy/Authority/safety review; this report grants none.

Recommended successor: `NONE`. Monitor through existing production truth and ordinary health owners. Re-enter only on an exact mismatch, material safety/correctness gap or owner-backed invalidator.

## Completion

- `PRIMARY_RUNTIME_BOUNDARY_REALITY_PASS`
- `ONE_PRIMARY_ROUTING_WRITER_PASS`
- `ENGINEERING_PLANE_ISOLATION_REALITY_PASS`
- `LEGACY_EXCEPTION_REALITY_PASS`
- `STATE_OWNER_REALITY_PASS`
- `CHANNEL_HEALTH_MODEL_REALITY_PASS`
- `FINAL_ARCHITECTURE_MAP_REALITY_ALIGNMENT_PASS`
- `NO_OBSERVED_ORPHANED_MIGRATION_TAILS`
- `NATURAL_TRAFFIC_OBSERVATION_RESIDUAL_NON_BLOCKING`
- `POST_RESET_REALITY_CHECK_COMPLETE`

Runtime effects = `NONE`.

Production effects = `NONE`.

Authority effects = `NONE`.

Reset terminal remains `V7_SYSTEM_RESET_AND_ROUTING_CORE_MIGRATION_COMPLETE`.


---

<!-- Source report: docs/reports/engineering/2026-08-13_390000_rt2_pr1_admission_and_pre_mutation_baseline.md -->

# RT2-PR1 Admission Check and Pre-Mutation Baseline

Status: `RT2_PR1_ADMISSION_NOT_PROJECTED_PRE_MUTATION_BASELINE_CAPTURED_REAL_TRAFFIC_OUTCOME_OPEN`

Scope: only OMP V4.78 Section 28.9 `RT2 Post-Reset Operating Profile`, sequence `RT2-PR1 -> RT2-PR7`. No unrelated OMP/backlog capability is admitted or executed.

## Admission

| Field | Evidence / result |
| --- | --- |
| Trigger | operator explicitly requested execution of the post-Reset profile only |
| Owner | existing OMP admission and CPS projection owners |
| Contract commit | `97e651bb8b414b03d2b1de3b50acc0c9399f2e72`, published to `origin/Updatesystem` |
| Required inputs | Reset terminal, `FINAL_ARCHITECTURE_MAP`, post-Reset reality, local/CPS/runtime truth and measurement owners available |
| First cell | `RT2-PR1 PRODUCTION_REALITY_VALIDATION` |
| Protected WIP | preserved; no CAP-U lane, natural-evidence lane or unrelated OMP item displaced |
| Admission result | `NOT_PROJECTED`: a targeted CPS Section 0 change contradicted the existing mission/registry projections and was reverted; no legal mutation Mission exists |
| Permitted effect | bounded read-only PR1 baseline/observation and independent PR2 analysis only; no Runtime, routing, user, Policy or Authority mutation |

The pre-change truth run proved the Reset terminal and deployed copied-binary identity. A later targeted CPS activation attempt returned `NO-GO` because Section 0, active WIP, registry, mission identity and OMP terminal projections would diverge. Those attempted CPS/OMP pointer changes were reverted rather than hiding the contradiction. Publishing docs-only contract commit `97e651bb` requires no Runtime deploy.

## PRE_MUTATION_BASELINE

Source boundary: Git commit `97e651bb8b414b03d2b1de3b50acc0c9399f2e72`. New `.understand-anything` generated analysis files are excluded from source metrics.

| Source metric | Baseline |
| --- | ---: |
| Tracked files | 8,817 |
| Tracked text files | 8,522 |
| Total tracked text LOC | 21,924,909 |
| Program-source files (`admin/`, `admin_core/`, `tools/`) | 145 |
| Program-source LOC | 182,264 |
| Test files / LOC | 115 / 56,648 |
| Documentation files / LOC | 6,192 / 5,783,121 |
| Config/infra files / LOC under the stated projection | 1,522 / 15,502,763 |
| Python files / functions / classes in program+test projection | 129 / 3,541 / 125 |
| Tracked systemd service/timer declarations | 7 / 5 |

The categories overlap only where explicitly stated by the projection and are not summed to infer handwritten code. Before/after comparisons must reuse the same rules.

## Production runtime baseline

Read-only production target: existing manifest alias `v7-vps`. Capture date: 2026-08-13.

| Metric | Baseline |
| --- | ---: |
| Compatible Core-primary users | 124 |
| Routing classes | 6 |
| Core fwmark rules | 6 |
| Class default routes | 6 |
| Legacy per-user source rules | 0 |
| nft `user_class` elements | 124 |
| nft `class_egress` elements | 6 |
| All `ip rule` entries | 12 |
| All route entries across tables | 47 |
| Discovered V7-named loaded unit rows | 29 |
| Active V7-named unit rows | 19 |
| Snapshot V7-related processes at bounded census | 10 |

`/usr/local/bin/v7-routing-sync --core-primary-verify --json` returned `CORE_PRIMARY_VERIFY_PASS`, exact Authority contract `rcpp_6bfcaa2063bd7567c9554b6d`, `nft_table_present=true`, no missing mark rules, no legacy primary rules and `legacy_fallback_ready=true`.

## Topology finding

The expanded production census invalidates the earlier limited-snapshot wording that the draft planner unit was not loaded:

- `v7-autoswitch-planner.timer` is loaded and `active/running`;
- its service runs `v7-service-matrix-refresh-all --consume-existing-service-failure-events-only`;
- the child path includes `v7-users-autoswitch --consume-passive-events-only`;
- this is a live Control/Engineering consumption path, not by itself a primary routing writer;
- `v7-routing-sync.service` remains the Core-primary apply owner and is `active/exited` after successful apply;
- `v7-users-autoswitch.service` and `.timer` remain inactive;
- additional active V7 timers include direct autosync, quality compact, path guard/sanity, Matrix refresh, Telegram sentinel and traffic collector.

Disposition: `HIDDEN_RUNTIME_DEPENDENCY_CANDIDATE` plus `RUNTIME_PACKAGE_CLASSIFICATION_REQUIRED` for PR2/PR3. No unit is disabled or modified by PR1. Exact caller, consumer, state and mutation effects must be proven before keep/shrink/remove disposition.

## Real traffic outcome

Two bounded read-only reads of nft ingress counters returned `packets=0`, `bytes=0`. Therefore:

- kernel/Core state = `PASS`;
- real ordinary client packet consumption through the class-mark path = `NOT_PROVEN` in this observation window;
- `REAL_USER_CONNECTIVITY_OUTCOME_CONFIRMED` remains open;
- no traffic is generated and no user is moved to manufacture evidence;
- reentry is the next ordinary production packet observed by the existing nft/routing verification owner.

This real-world wait does not invalidate `PRE_MUTATION_BASELINE_CAPTURED` or prevent independent read-only PR2 analysis. It blocks any stronger PR1 production-outcome terminal and any mutation that depends on that proof.

## PR1 disposition

- `PRE_MUTATION_BASELINE_CAPTURED = PASS`.
- `RT2_PROFILE_ADMISSION = NOT_PROJECTED`; mutation cells remain blocked pending one consistent existing-owner OMP/CPS admission transaction.
- `CORE_PRIMARY_KERNEL_STATE = PASS`.
- `RUNTIME_PACKAGE_TOPOLOGY_BASELINE = CAPTURED_WITH_NEW_GAP`.
- `REAL_TRAFFIC_PATH_CONFIRMED = NOT_PROVEN`.
- `REAL_USER_CONNECTIVITY_OUTCOME_CONFIRMED = NOT_PROVEN`.
- Exact safe successor: independent read-only `RT2-PR2` relationship/responsibility audit; PR1 remains open for natural traffic reentry and no mutation cell is admitted.

## PROGRAMMATIC_CHANGE_DELTA

Program source LOC: `0 -> 0 -> 0`.

Documentation/report LOC: `0 -> 118 -> +118`; no CPS/OMP contract line remained changed after the failed activation projection was reverted.

Test LOC: `0 -> 0 -> 0`.

Program files added / modified / deleted / moved: `0 / 0 / 0 / 0`.

Functions/classes/entrypoints added / removed / moved / merged / changed: `0 / 0 / 0 / 0 / 0`.

Runtime dependency/state/unit/routing edges changed: `0`; read-only evidence discovered existing edges only.

`PROGRAMMATIC_CODE_EFFECT = NONE`.

Runtime effects = `NONE`

Production effects = `NONE`

Authority effects = `NONE`


---

<!-- Source report: docs/reports/engineering/2026-08-13_400000_rt2_pr2_engine_relationship_and_runtime_package_audit.md -->

# RT2-PR2 Engine Relationship and Runtime Package Audit

Status: `RT2_PR2_READ_ONLY_AUDIT_COMPLETE_MUTATION_AND_PROFILE_TERMINAL_BLOCKED`

Scope: only OMP §28.9 `RT2 Post-Reset Operating Profile`. This report consumes the Reset terminal and the PR1 baseline. It does not execute another OMP capability, change Runtime, grant Authority, generate traffic, or treat a report as admission.

## Decision

The current Core-primary dataplane is compact and correctly separated, but the installed operating package is materially wider than the simplified M10 projection. The correct optimization is not wholesale deletion of the large legacy files. It is to preserve the 210-line Core writer, make the real asynchronous/mutation-capable package boundary explicit, and admit only owner-backed changes that remove a proven duplicate consumer or mixed responsibility.

The attempted narrow CPS activation of RT2 was rejected and reverted after `v7-truth-check` proved that Section 0 alone would diverge from active WIP, registry, mission identity and OMP terminal projections. Therefore read-only analysis is legal, while PR2/PR3 source, package and Runtime mutation remains blocked until the existing OMP/CPS owner performs one complete admission transaction.

## Reproducible coverage

The confirmed `.understandignore` excluded `docs/`, evidence/artifact trees, secrets, logs, caches, generated binaries and dependency directories from code-depth analysis. Historical root documents were classified at sufficient documentation depth; production and mutation-capable paths received deeper static and live inspection.

| Evidence | Result |
| --- | ---: |
| Repository entries ignored by the confirmed scope rules | 7,462 |
| In-scope files scanned exactly once | 1,076 |
| Graph nodes | 3,585 |
| Graph edges | 3,979 |
| File/config/document/pipeline nodes | 1,076 |
| Function/class nodes | 2,509 |
| Architectural layers | 8 |
| Guided trace steps | 11 |
| Import edges recovered by deterministic scan | 95 |
| Skipped batches/files | 0 / 0 |
| Validation issues | 0 |
| Edge-less node warnings | 858; retained as orphan candidates, not auto-deletion proof |

Permanent generated evidence: `.understand-anything/knowledge-graph.json`, `meta.json`, `fingerprints.json` and `intermediate/scan-result.json`. Raw batch/analysis material was moved into the skill-prescribed delayed-cleanup `.trash-*` area. Every file-level node belongs to exactly one architectural layer; all layer and tour references resolve.

## Responsibility and interaction findings

| Surface | Real caller / consumer / effect | Classification | Disposition | Removal or recheck trigger |
| --- | --- | --- | --- | --- |
| `tools/runtime-support/v7-routing-sync` (210 LOC) | `v7-routing-sync.service`, path guard on detected routing fault, user-key rotation; programs nft/ip and verifies class state | Data Plane primary, single routing lock, explicit fallback | `KEEP` | only a proven replacement with equivalent atomic apply, verify, fencing and fallback |
| `admin_core/routing_core.py` (265 LOC) | tests, shadow/certification adapters; produces effect-free plan/contracts | Control Plane decision contract | `KEEP` | none; no duplicate live writer proven |
| nft `user_class`/`class_egress`, six fwmark rules/tables | production kernel forwarding for 124 members | Data Plane primary | `KEEP` | proven replacement plus real-traffic observation |
| `v7-users-autoswitch` (23,639 LOC; 317 defs) | governed/manual planning, passive event consumption and bounded `v7-user-switch`; not current primary Core writer | `RESPONSIBILITY_MIXING`; legacy/fallback plus Engineering Plane | `SHRINK/FUTURE_REVIEW`, not whole-file delete | exact function consumers mapped and legal mutation Mission admitted; preserve rollback/Authority paths |
| `v7_sync_lib.py` (25,379 LOC; 306 defs) | truth, deploy, OMP, Polygon and continuation CLIs; writes engineering documents/state, not packet forwarding | `RESPONSIBILITY_MIXING`, Engineering Plane | `SHRINK/FUTURE_REVIEW` | split only where an existing owner consumes a coherent responsibility and tests prove no CLI break |
| `admin/v7-admin-api` (41,024 LOC; 719 defs; 16,528-line HTML function) | active admin service and operator consumers | `RESPONSIBILITY_MIXING`, API/UI/control boundary | `SHRINK/FUTURE_REVIEW` | UI/API extraction under existing admin owner with compatibility tests; unrelated to routing hot path |
| `admin_core/operator_execution.py` + pipeline (14,064 LOC) | Packet/lease/barrier, governed apply, validation, rollback and exact action class | Control Plane safety owner; excluded from primary forwarding | `KEEP` | equivalent bounded Authority, crash recovery and rollback production proof |
| `v7-user-switch` (135 LOC) | governed/manual per-user movement and rollback | fallback mutation adapter | `LEGACY_EXCEPTION` | no remaining bounded movement/rollback consumer |
| `v7-autoswitch-planner.timer` -> Matrix consumer | active every 30s; service consumes existing service-failure events and may enter only governed standing-policy path | name is historical; real edge is Control/Engineering async, not primary writer | `KEEP`, rename only if it removes operator ambiguity without deployment risk | consumer superseded or naming change admitted with unit/deploy proof |
| `v7-service-matrix-refresh.timer` and Telegram sentinel | active async health writers/consumers; sentinel deployed with `--no-autoswitch` | Control Plane observation | `KEEP` | equivalent freshness and failure-event consumer exists |
| `v7-health.service` | active loop for history/stability/load/diagnose/state projections | Control Plane observation with multiple state outputs | `KEEP/SHRINK_REVIEW` | per-output consumer map plus restart/freshness proof |
| `v7-direct-autosync.timer` | active every 10m; can update Direct domain config, restart dnsmasq and write state | `HIDDEN_RUNTIME_DEPENDENCY` relative to M10 compact projection; separate Direct product behavior | `KEEP` under existing Direct owner, explicitly outside routing Core | Direct feature retired or equivalent idempotent config owner proven |
| `v7-path-guard-repair.timer` -> `--apply` | active every 2m; may run sysctl, MSS clamp, Core sync, killswitch, Direct autosync and optional MTU repair | `HIDDEN_RUNTIME_DEPENDENCY`; recovery/safety mutation chain | `LEGACY_EXCEPTION`, no blind disable | failure scenarios, Authority envelope and equivalent recovery consumer proven before any narrowing |
| OMP/reports/history | no import/startup edge to Core writer | Engineering/Historical only | `KEEP_OUTSIDE_RUNTIME` | none |

### Actual production dependency projection

```text
CLIENT PACKETS
  -> nft user_class/class_egress
  -> six fwmark rules/tables
  -> egress interface

ASYNC CONTROL / RECOVERY
  Telegram sentinel -> Matrix state/event
  Matrix timer -> full refresh
  30s planner-named timer -> existing-event consumer -> governed policy path only
  health/quality/benchmark timers -> health and capacity state
  path sanity -> path guard --apply -> bounded repair commands -> routing-sync when required
  Direct autosync -> Direct DNS/config state

ENGINEERING
  OMP / CPS / Reports / Polygon / Learning / Replay
  -X-> synchronous packet forwarding
```

No OMP/report/history import or startup edge into `v7-routing-sync` was found. The principal correction is that `path-guard --apply` and Direct autosync are real installed mutation-capable dependencies even though they are not continuous packet-forwarding dependencies.

## Mature-system fit analysis

Only architectural principles were consumed:

| Reference principle | V7 fit / material gap | Disposition |
| --- | --- | --- |
| Junos separates Routing Engine and Packet Forwarding Engine, keeps forwarding tables local and updates forwarding without interrupting packets | V7 fits through prepared class state -> compact nft/ip writer -> kernel forwarding; Engineering Plane is absent from packet lookup | `KEEP` |
| IOS XR uses modular control processes and a hardware-abstraction boundary that programs the dataplane from RIB state | V7 has a valid small adapter, but large control/engineering executables mix many responsibilities | keep adapter; shrink monoliths only behind existing interfaces and tests |
| FRR zebra owns the RIB/FIB boundary and feeds the kernel through Netlink while protocols remain separate | V7 class state -> one routing writer -> Linux kernel matches the dependency direction | `KEEP`; do not add FRR-like daemons |
| Linux exposes route configuration through rtnetlink and keeps kernel forwarding state distinct from userspace control | V7 `ip`/`nft` adapter is the correct boundary; verification must remain explicit | `KEEP` |
| Cloudflare combines passive/fast failover signals with health checks and load-balancing decisions | V7's sentinel + Matrix + governed consumer is directionally correct; it must not turn the fast signal into unbounded movement Authority | `KEEP` with current fail-closed gate |

Primary references: Juniper Junos OS Architecture Overview (`https://www.juniper.net/documentation/us/en/software/junos/junos-overview/topics/concept/junos-software-architecture.html`); Cisco IOS XR Data Sheet (`https://www.cisco.com/c/en/us/products/collateral/ios-nx-os-software/ios-xr-software/datasheet-c78-743014.html`); FRRouting Zebra documentation (`https://docs.frrouting.org/en/stable-7.2/zebra.html`); Linux `rt-route` Netlink specification (`https://docs.kernel.org/next/netlink/specs/rt-route.html`); Cloudflare health/failover description (`https://blog.cloudflare.com/new-tools-to-monitor-your-server-and-avoid-downtime/`). Architectural difference alone produced no rewrite verdict.

## PR4-PR7 independent evidence consumption

The focused routing, Core promotion, routing-sync, autoswitch policy, user-switch, quality, load-policy and 10k/50 scale unittest set passed with exit 0. No pytest package was available, so the repository's unittest-compatible modules were executed directly. This proves existing technical contracts, not real production traffic or admission.

| Gate | Current result |
| --- | --- |
| `PRE_MUTATION_BASELINE_CAPTURED` | `PASS` |
| `EXHAUSTIVE_V7_ENGINE_COMPONENT_COVERAGE_PASS` | `PASS_FOR_CONFIRMED_SCOPE`; 1,076/1,076 file nodes classified |
| `V7_REAL_CODE_RELATIONSHIP_GRAPH_COMPLETE` | `PASS_WITH_DYNAMIC_RUNTIME_SUPPLEMENT`; static imports alone are not treated as full truth |
| `SYSTEM_WIDE_DEPENDENCY_INTERACTION_GRAPH_COMPLETE` | `PASS_FOR_CRITICAL_RUNTIME_AND_MUTATION_PATHS` |
| `RESPONSIBILITY_AUDIT_COMPLETE` | `PASS` |
| `REFERENCE_SYSTEM_COMPONENT_BOUNDARY_COMPARISON_COMPLETE` | `PASS` |
| `DECISION_RELEVANT_ANALYSIS_PRESERVED` | `PASS` |
| `LEGACY_SURFACE_REDUCTION_PASS` | `NOT_PROVEN`; no deletion justified or admitted |
| `RUNTIME_PACKAGE_MINIMAL_PASS` | `FAIL_CURRENT_PROJECTION_INCOMPLETE`; active package is wider than M10 description |
| `ROUTING_LATENCY_BASELINE_CONFIRMED` | existing M6/M7 evidence retained; PR1 real packet outcome still open |
| `CHANNEL_ADMISSION_MODEL_STABLE` | controlled/unit evidence retained; natural real-traffic outcome open |
| `SCALE_BOUNDARY_CONFIRMED` | test evidence passes for 10k+/50+ contract; production-scale consumption not re-created |
| `ARCHITECTURE_DRIFT_PROTECTION_ACTIVE` | contract active; final alignment blocked by package mismatch |
| `REAL_USER_CONNECTIVITY_OUTCOME_CONFIRMED` | `NOT_PROVEN`; two bounded nft counter reads were zero |
| `AUTOMATIC_INTERNET_OPERATION_READY` | `NOT_PROVEN` |

## Exact blockers and successor

1. `RT2_ADMISSION_PROJECTION_REQUIRED`: the existing OMP/CPS owner must create one consistent Mission/registry/Section 0 transition; a report cannot do this and a partial CPS patch failed closed.
2. `REAL_TRAFFIC_OBSERVATION_REQUIRED`: next ordinary production packet must be observed through the existing class nft/routing verification owner; no traffic or user movement may be manufactured.
3. `RUNTIME_PACKAGE_PROJECTION_RECONCILIATION_REQUIRED`: existing Canonical/SYSTEM_MAP owners must acknowledge path guard, Direct autosync, health/Matrix and planner-named event consumer as actual production dependencies before a minimality terminal.
4. Only after 1–3 may an owner-backed PR3 Mission decide whether any exact responsibility is removed, split, renamed or retained. The present audit authorizes no code, unit or Runtime change.

This is a bounded legal terminal for the current read-only execution, not completion of RT2-PR1 -> PR7 and not `STEADY_STATE_OPERATIONS` graduation.

## PROGRAMMATIC_CHANGE_DELTA

Program source LOC: `0 -> 0 -> 0`.

Documentation/report LOC: `0 -> 269 -> +269` across the PR1 and PR2 Engineering Reports (`118 + 151`).

Generated analysis/data LOC: 126,372 lines in the final graph, fingerprints and preserved scan inventory; reported separately and excluded from documentation/program LOC.

Test LOC: `0 -> 0 -> 0`; existing tests only executed.

Files added / modified / deleted / moved / runtime-excluded: program files `0 / 0 / 0 / 0 / 0`; generated analysis and Engineering Reports are evidence, not product implementation.

Functions/classes/entrypoints added / removed / moved / merged / changed: `0 / 0 / 0 / 0 / 0`.

Dependency edges added / removed / changed: `0 / 0 / 0`; 3,979 repository edges and live unit edges were observed, not mutated.

State writers/readers/surfaces added / removed / merged: `0 / 0 / 0`.

Runtime units/process/package delta: `0`; read-only census only.

Routing object/writer/planner delta: `0`; verification only.

Legacy physical removal vs logical/runtime exclusion: `0` removed; existing Core-primary exclusion remains unchanged.

`PROGRAMMATIC_CODE_EFFECT = NONE`.

Runtime effects = `NONE`

Production effects = `NONE`

Authority effects = `NONE`


---

<!-- Source report: docs/reports/engineering/2026-08-13_410000_v7_code_responsibility_deep_audit_report.md -->

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


---

<!-- Source report: docs/reports/engineering/2026-08-13_420000_v7_commercial_router_alignment_report.md -->

# V7 Commercial Router Alignment Report

Status: `RT2_PR2B_COMMERCIAL_ROUTER_ALIGNMENT_AUDIT_PASS_READ_ONLY`

Scope: existing OMP §28.9 `RT2-PR2B COMMERCIAL ROUTER ARCHITECTURE BENCHMARK AND V7 ALIGNMENT AUDIT`. This consumes PR1 baseline, PR2 package audit, PR2A code-responsibility audit and M10 benchmark. It is comparison and classification only: no code, CPS, Runtime, production, service/timer, routing, cleanup or Authority change occurred.

## 1. Purpose and reference model

The purpose is not vendor imitation. It is to compare stable responsibility boundaries—decision state, forwarding programming, health/admission, failover/recovery and operations—against V7's proven reality, then identify only evidence-backed simplification work.

| Reference | Relevant architectural pattern | Boundary used for V7 comparison |
| --- | --- | --- |
| Junos | Routing Engine owns routing/control state; Packet Forwarding Engine owns packet lookup/forwarding. Active forwarding state is copied to the forwarding engine, which can keep forwarding during a control-plane disruption. | narrow forwarding plane, explicit control state, install/error verification |
| Cisco IOS XR | Manageability, protocol/application, infrastructure/RIB and hardware-abstraction layers are distinct. RIB chooses best routes and installs them to forwarding line cards; the OFA layer programs the dataplane from RIB/LSD state. | management/control/dataplane placement and one direction of programming |
| FRRouting | Protocols supply best routes to Zebra/RIB; Zebra derives FIB and programs the kernel or FPM. A dataplane queue/plugin offloads FIB programming and has explicit installation/debug visibility. | single routing ownership, desired-to-kernel projection, replacement/reconciliation semantics |
| Linux routing | Userspace configures and observes route objects through rtnetlink; the kernel owns forwarding execution. | narrow userspace-to-kernel adapter and observable applied state |
| Cloudflare Load Balancing | Monitors produce health observations; pools aggregate endpoint availability; steering excludes unhealthy targets and handles failover. | health freshness/admission and failure containment only—not router/RIB implementation |

Primary sources: [Junos Architecture Overview](https://www.juniper.net/documentation/us/en/software/junos/junos-overview/topics/concept/junos-software-architecture.html), [Junos forwarding-table continuity](https://www.juniper.net/documentation/us/en/software/junos/cli-reference/topics/ref/command/show-pfe-data.html), [Cisco IOS XR architecture](https://www.cisco.com/c/en/us/products/collateral/ios-nx-os-software/ios-xr-software/datasheet-c78-743014.html), [Cisco IOS XR RIB monitoring](https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/routing/configuration-guide/routing-config-cisco8000/implementing-and-monitoring-rib.html), [FRR Zebra](https://docs.frrouting.org/en/stable-7.2/zebra.html), [Linux rt-route Netlink](https://docs.kernel.org/next/networking/netlink_spec/rt_route.html), and [Cloudflare health/pool model](https://developers.cloudflare.com/load-balancing/understand-basics/health-details/).

## 2. Common mature-system patterns

| Question | Common pattern | V7 evaluation criterion |
| --- | --- | --- |
| Routing decision | A bounded Control Plane/RIB selects desired forwarding state from owned policy, topology and health facts. | no independent UI, report, health probe or legacy helper may silently become a second primary routing decision owner |
| Plane separation | Management requests/observes; Control decides; Data Plane forwards from installed state. Engineering improves asynchronously. | packet forwarding must not synchronously require OMP, report, learning, Polygon or replay |
| Health/admission | Probe/telemetry producers update freshness-bound state; policy consumes it to admit or exclude a target. | a signal is not movement authority; stale/partial state fails closed |
| Failover | detect -> update state -> select -> program forwarding -> verify. | each edge must have one owner, bounded scope and terminal |
| Recovery | retain a known good forwarding state; fence writers; reconcile install failure; roll back only through the safety owner. | recovery may be separate but must not become an unbounded parallel primary path |
| Scale | forwarding cardinality and synchronous work are bounded independently of operational history; RIB/FIB update and verification are observable. | V7 must retain class routing and avoid per-user primary rules/tables or O(N) hot-path reconciliation |

## 3. Reference-system comparison

| Reference | Routing decision / state owner | Management / Control / Data separation | Health, failover and recovery | Scaling conclusion |
| --- | --- | --- | --- | --- |
| Junos | Routing Engine maintains routing and forwarding tables; PFE uses a local forwarding copy. | management/routing operations remain on Routing Engine; PFE forwards packets. | PFE installation feedback can identify RIB/FIB discrepancy; local FIB preserves forwarding through control interruption. | data packet processing does not traverse management/routing processes per packet. |
| IOS XR | protocols/RIB select best routes; infrastructure layer exposes routing state; OFA programs hardware from that state. | CLI/YANG management, protocol layer, infrastructure/RIB and hardware abstraction are explicit. | RIB/forwarding comparison supports inconsistency troubleshooting. | modular layers and a common RIB avoid each API or protocol programming a separate forwarding truth. |
| FRR | Zebra owns RIB/FIB mediation; protocols do not individually own kernel programming. | protocol daemons -> Zebra -> kernel/FPM. | FIB programming is explicit; replace semantics and reconnection/full-table refeed support convergence. | a dedicated dataplane execution boundary avoids putting FIB work in every protocol path. |
| Linux | userspace requests routes; kernel FIB forwards. | rtnetlink is the control/configuration API, not the forwarding loop. | `getroute`, create and delete route operations make installed state observable. | kernel forwarding cardinality/lookup is separate from userspace workflow history. |
| Cloudflare-style LB | monitors/pools own endpoint health; steering chooses eligible pool/endpoint. | management configures monitors/pools; health observation informs steering; request path uses that decision. | health state excludes unhealthy endpoints; failover is bounded by pool/steering policy. | health aggregation and steering avoid every request needing engineering history. |

## 4. V7 current mapping and decisions

| Responsibility | Commercial pattern | V7 current implementation | Gap | Recommended action |
| --- | --- | --- | --- | --- |
| Health | dedicated observation updates freshness-bound health state | Matrix refresh, Telegram sentinel (`--no-autoswitch`), quality and health loops produce/control health facts | multiple producers and a health loop with several outputs need writer/reader fencing; not a duplicate primary router | `KEEP` producers; `SHRINK` only after per-state ownership map |
| Admission | policy/RIB consumes current health/capacity, not a bare probe | existing Matrix/quality + policy/capacity/Authority gates; `EGRESS_ADMISSION_STATE` is logical projection | current runtime package projection under-describes active path-guard and Direct chains | `KEEP`; reconcile existing package/topology truth |
| Routing decision | one Control Plane selects desired forwarding state | assignments, policy/capacity/Authority, Routing Core and governed planner paths | `v7-users-autoswitch` still co-locates planning, diagnostics, certification and fallback movement | `SHRINK` planner responsibilities; preserve exact governed decision owner |
| Dataplane apply | narrow adapter programs FIB/kernel from approved state | `v7-routing-sync` applies nft class maps and six fwmark/table classes under one lock | none proven in primary Core path | `KEEP`; do not create Core v2 or a second writer |
| Verification | applied FIB/kernel state and traffic outcome are independently checked | Core verify checks nft/ip state; PR1 real ordinary traffic counter remains unproven | kernel verification cannot substitute for user traffic outcome | `KEEP`; wait for ordinary traffic evidence without manufacturing it |
| Recovery | fenced bounded recovery with install/reconciliation proof | Packet/lease/barrier plus `v7-user-switch` fallback; path guard can call repair actions | active path guard is a hidden mutation-capable dependency relative to M10 description | `LEGACY_EXCEPTION`; reconcile scope/Authority/failure matrix before narrowing |
| Learning | asynchronous feedback, never forwarding prerequisite | OMP, Reports, Polygon, Learning and Replay are outside Core packet path | no primary-path violation found; large engineering modules co-locate concerns | `KEEP_ENGINEERING`; `SHRINK` interfaces, not add machinery |
| Engineering tooling | separate from live RIB/FIB and management operations | `v7_sync_lib.py` owns CPS/OMP/Polygon/deploy helpers | co-location increases audit/mutation blast radius | `MOVE/SHRINK` by existing interfaces after admission |
| Admin/control API | management layer issues guarded requests; it is not a routing engine | `admin/v7-admin-api` serves UI, read models and guarded actions | 16,528-line embedded UI plus route/action/config logic in one executable | `SHRINK` by presentation and route-group extraction; retain one guarded API boundary |

## 5. Correct existing decisions to preserve

- `v7-routing-sync` is a narrow, single-lock userspace-to-nft/ip adapter. It is V7's correct equivalent of a constrained FIB-programming boundary, not a decision engine.
- Primary forwarding uses six classes and nft membership rather than per-user primary rules/tables. This preserves the M7/M9 scale simplification.
- OMP, reports, Polygon, learning and replay are not synchronous Core forwarding dependencies.
- `operator_execution` owns packet/lease/barrier, exact action class, replay prevention and rollback compensation. This is a necessary safety boundary, not removable ceremony.
- Matrix/sentinel health signals remain evidence producers; sentinel deployment with `--no-autoswitch` preserves the rule that a fast observation is not itself movement Authority.

## 6. Gap and component placement analysis

| V7 surface | Mature-system placement | Current V7 reality | Classification | Future disposition |
| --- | --- | --- | --- | --- |
| `v7-users-autoswitch` | Control Plane decision plus separately bounded recovery; diagnostics outside routing engine | mixes event consumption, planning, fallback movement, rollback, certification and diagnostics | `RESPONSIBILITY_MIXING` | `SHRINK`; move diagnostics/certification to existing Engineering owner, retain fallback execution |
| `v7_sync_lib.py` | separate management/truth, orchestration, verification and release interfaces | CPS reconciliation, continuation, Polygon and deploy co-located | `RESPONSIBILITY_MIXING` | `MOVE/SHRINK` through existing public interfaces; no Runtime move |
| `admin/v7-admin-api` | Management Plane UI/API separate from control logic | UI rendering, read models, dispatch and component action adapters co-located | `RESPONSIBILITY_MIXING` | `SHRINK`; move presentation and route groups, retain guarded operator boundary |
| `v7-path-guard-repair` | recovery/repair subsystem with strict writer fence | timer may invoke sysctl, MSS, routing-sync, killswitch and Direct autosync | `HIDDEN_RUNTIME_DEPENDENCY`, `LEGACY_EXCEPTION` | `KEEP` pending authoritative failure/recovery matrix; no blind disable |
| Direct autosync | separate Direct-service control subsystem | timer updates Direct config/DNS and state | `CONTROL_PLANE`, not Routing Core | `KEEP_RUNTIME`; state its boundary in existing package truth |
| Matrix refresh / sentinel / health | health observation and admission inputs | several producers/consumers, with sentinel no-autoswitch | potential state-writer overlap, no proven duplicate forwarding writer | `KEEP`; first map writer fencing and output consumers |

## 7. Classification register

### KEEP

- Core dataplane adapter, class routing, explicit nft/ip verification and one routing lock.
- Existing Assignment/Policy/Capacity/Authority gates.
- `operator_execution` Packet/lease/barrier/rollback boundary.
- Matrix/sentinel observation model and Engineering Plane exclusion from forwarding.

### MERGE

No merge is admitted. Candidate review only: equivalent health-state writers and duplicated API/read-model shaping require evidence of same state, same consumer and same failure contract before consolidation.

### MOVE

- planner-hosted diagnostics/certification responsibilities -> existing Engineering Plane owner;
- embedded admin presentation -> existing UI/presentation boundary;
- `v7_sync_lib.py` responsibility groups -> existing CPS, continuation, Polygon and deploy interfaces.

### SHRINK

- `v7-users-autoswitch`: separate event/diagnostic/certification from governed fallback movement;
- `v7_sync_lib.py`: split public interfaces without multiplying truth owners;
- `admin/v7-admin-api`: separate UI asset and route groups;
- health loop: only after output-level ownership proof.

### REMOVE CANDIDATE

`NONE`. No reviewed surface satisfies all four requirements: no consumer, no product effect, no safety effect and no lifecycle obligation.

## 8. Recommended cleanup order (not executed)

```text
EXISTING OMP/CPS ADMISSION
  -> reconcile actual active runtime package/topology
  -> map health state writers/readers and path-guard recovery authority
  -> isolate one low-risk Engineering or UI responsibility group
  -> affected tests and existing promotion ladder
  -> safe deploy / observation / residue proof
  -> only then consider a separate function-level removal candidate
```

This sequence keeps the proven fast path intact and gives precedence to truth/recovery boundaries over LOC reduction.

## 9. Completion and residual

- Reference architecture model selected from primary vendor/kernel/operator documentation: `PASS`.
- Mature routing, health/failover and state/plane patterns compared to PR1/PR2/PR2A reality: `PASS`.
- V7 gap and simplification classification register created: `PASS`.
- No code, Runtime, production, CPS, Authority or cleanup operation performed: `PASS`.
- `COMMERCIAL_ROUTER_ALIGNMENT_AUDIT_PASS = PASS`.

Residual: `RT2-PR3` is still not admitted. Its prerequisites remain the existing OMP/CPS transaction, real ordinary traffic observation and runtime-package truth reconciliation. Vendor comparison is not an implementation authorization.

## PROGRAMMATIC_CHANGE_DELTA

Program source LOC: `0 -> 0 -> 0`.

Documentation/report LOC: `0 -> 145 -> +145` for this report; the OMP contract row is reported separately from program source.

Test LOC: `0 -> 0 -> 0`.

Files/functions/classes/entrypoints/dependency edges/state surfaces/runtime units/routing objects added, removed, moved or changed: `0` program changes; read-only classification only.

`PROGRAMMATIC_CODE_EFFECT = NONE`.

Runtime effects = `NONE`

Production effects = `NONE`

Authority effects = `NONE`


---

<!-- Source report: docs/reports/engineering/2026-08-13_015600_active_incident_revisioned_obligation_consumer_repair.md -->

# Отчёт: revision-aware consumption active incident obligation

Дата: 2026-08-13 01:56 MSK  
Программа: `V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`  
Родительская Mission: `CT-M0F CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_LATENCY`

## Результат

`PASS — ACTIVE_INCIDENT_REVISIONED_OBLIGATION_CONSUMER_REPAIRED_AND_PRODUCTION_CONSUMED`.

Исправлена общая причинная связь существующего append-only owner:

`changed current incident scope/classification → new semantic fingerprint → one OMP consumption → CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN`.

Новые owner, queue, watcher, timer, registry, policy или Runtime path не созданы.

## Root cause

Producer `tools/v7-users-autoswitch` уже умел дописывать изменившуюся семантику active obligation, но consumer в `tools/v7_sync_lib.py` считал любой исторически потреблённый `automation_obligation_id` окончательно потреблённым. Поэтому новая current projection того же immutable lineage могла не попасть к OMP consumer.

Исправление вводит `automation_consumption_fingerprint` только для новых producer projections. Exact-once теперь действует на semantic revision; historical rows без fingerprint сохраняют прежнюю ID-scoped дедупликацию и не переинтерпретируются после deploy.

## Verification

- Focused tests: `3/3 PASS`, включая changed-scope re-entry и cross-process exact-once.
- Full `tests.unit.test_service_failure_automation_evolution`: `PASS`.
- Deploy manifests: `PASS`; изменялись только `tools/v7_sync_lib.py` и `tools/v7-users-autoswitch`.
- Production deploys: `4f16345c`, затем совместимый migration fix `adc4356e`.
- Production ordinary consumer, без ручного Matrix/autoswitch:
  - obligation `sfaob_3fad990568f118aab69e4ce6`;
  - fingerprint `a0f486aa6043e2bc1c947807d3448add6e629a9843cc260c210d87f42271d014`;
  - source incident `sfinc_ab1dda90210a824d7698c84c822caa2f`;
  - current scope: affected `12`, unresolved `12`, protected `0`;
  - receipt `sfomp_2fe82a0265071da132ee3c8d` at `2026-08-12T22:54:35Z`;
  - successor: `CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN`.
- `tools/v7-truth-check --all --json`: `PASS`, `FULLY_ALIGNED`.
- `tools/v7-convergence-status --json`: `PASS`; local, GitHub and production runtime all at `adc4356efa4cdfcf86b4b1ef6aea9724fefb97f8`.

## Safety and CT-M0F status

No Candidate, Packet, lease, restore-barrier write, apply, routing mutation, user movement, Authority expansion or Production Maturity change was made by this repair.

The receipt correctly ends at `STOP_SAFE_FRESH_EVENT_REVALIDATION_REQUIRED`; it does **not** constitute a CT-M0F latency sample. The live next consumer must revalidate fresh target health/capacity and the standing policy before it may create fresh execution artifacts. A valid `Time receipt` has not been produced in this repair.

## Exact next frontier

`CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN` through the existing ordinary Matrix/Planner chain:

`fresh Matrix observation → live target/capacity gates → fresh Candidate → Packet → lease → permitted bounded cutover → exact client-context Time receipt`.

If any live gate fails, the existing consumer must emit its predicate-level `STOP_SAFE` with automatic re-entry; it must not fabricate a latency sample or wait for operator continuation.


---

<!-- Source report: docs/reports/engineering/2026-08-13_021146_omp_receipt_to_bounded_executor_handoff_repair.md -->

# Repair: OMP receipt → bounded executor handoff

Дата: 2026-08-13

## Итог

`PASS_DEPLOYED_AND_PRODUCTION_CONSUMED`.

Исправлена существующая связь внутри ordinary Matrix path:

`service_failure_automation_obligation`
→ `OMP_CONSUMED receipt`
→ `tools/v7-service-matrix-refresh-all`
→ `tools/v7-users-autoswitch` bounded executor.

Ранее второй и последующие Matrix cycles корректно не создавали новую
obligation, но ошибочно передавали executor пустой вход и завершались
`STOP_SAFE_NO_CURRENT_SERVICE_FAILURE_OBLIGATION`.

## Причина и ремонт

Причина: immutable OMP exact-once receipt считался terminal для Matrix caller,
хотя он является durable handoff для следующего существующего consumer.

Ремонт в существующих owners:

- `tools/v7_sync_lib.py` читает только existing `closure-records.jsonl` и
  `l3-runtime-state.json`, возвращая obligation только при точном совпадении
  semantic fingerprint, Incident/Situation/Decision identity и текущего
  accounted scope;
- `tools/v7-service-matrix-refresh-all` использует этот handoff только когда
  advisory не выдал новую obligation;
- stale receipt, scope drift, recovery или identity mismatch остаются
  `NO_CURRENT_CONSUMED_HANDOFF` без Runtime effect.

Не созданы новые timer, queue, watcher, store, Planner, Authority или policy.

## Проверка

- Focused и полный `test_service_failure_automation_evolution` и
  `test_service_failure_episode`: `PASS`.
- Commit: `f2d84377`.
- Safe-deploy manifest: только `tools/v7_sync_lib.py` и
  `tools/v7-service-matrix-refresh-all`; forbidden effects отсутствуют.
- Production deploy: `deploy-z8-14-Updatesystem-f2d8437-20260813T020829`.
- Обычный systemd Matrix consumer (без ручного Matrix/autoswitch запуска)
  дошёл до existing bounded executor. Старый terminal исчез; получен честный
  terminal `STOP_SAFE_CURRENT_INCIDENT_NOT_ACTIONABLE` для
  `sfinc_762b70efa00784030a875fb3809300f8`.

## Текущий residual

Incident остаётся active с 11 users на failed source. Executor получил точную
current obligation, но Planner не выдал owner-backed actionable recommendation:
`current_incident_has_no_owner_backed_actionable_recommendation`.

Это не failure handoff и не разрешение на движение. Следующий existing consumer
— ordinary Matrix/Planner revalidation: при fresh healthy target, capacity,
policy и anti-flap gates он формирует новый Candidate/Packet/lease; иначе
сохраняется этот predicate-level STOP_SAFE с automatic re-entry на изменение
target/capacity/policy generations.

## Consistency

`tools/v7-truth-check --all --json`: `PASS`, `FULLY_ALIGNED`.

`tools/v7-convergence-status --json`: local/GitHub/production commit
`f2d84377a797cd88a6ca9d218cb5033c99a23992`, `PASS`.


---

<!-- Source report: docs/reports/engineering/2026-08-13_024500_certification_scope_partition_and_legacy_incident_reconciliation.md -->

# Partition certification scope and reconcile legacy active incident

Date: 2026-08-13

## Result

`PASS`: the ordinary Service Failure consumer no longer treats a source that
contains only certification identities as an ordinary-user failover cohort.

The correction is channel-agnostic. It applies to every source because it is
derived only from the existing `users.registry` classification and the existing
Matrix/L3/OMP owners.

## Root cause

The Matrix source-scope contract previously represented all enabled identities
on a failed source as one denominator. The existing controlled-certification
pool already knew how to distinguish certification identities, but that fact
was not connected to the passive failure -> ordinary advisory consumer chain.

For the active legacy incident, current production truth was:

```
affected = 12
protected = 1  (existing verified packet-bound Outcome)
ordinary unresolved = 0
certification-only remainder = 11
```

Before the repair, the 11 controlled identities appeared as unresolved ordinary
users and repeatedly selected `CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN`.
There was no lawful ordinary action to take, so the bounded executor correctly
stopped with no actionable recommendation, but the consumer loop was misleading.

## Implemented existing-owner extension

1. `tools/v7-service-matrix-test` v2 source scope now records compact,
   no-raw-list partitions:
   - `ordinary_production_scope`;
   - `controlled_certification_scope`;
   - `total_assigned_scope`;
   - `scope_classification`.
   Compatibility `affected_scope_*` fields are the ordinary production
   denominator, the only scope admitted to ordinary failover.
2. `tools/v7-service-matrix-refresh-all` preserves certification-only failures
   for passive reconciliation, while preventing them from being admitted to
   ordinary action.
3. `tools/v7-users-autoswitch` consumes the partition in the existing L3
   incident projection and advisory.
4. A bounded legacy reconciliation preserves proven packet Outcome lineage and
   classifies the remaining live certification identities as
   `explicitly_excluded_or_recovered_scope`, not as protected or disappeared.

No new owner, timer, scheduler, queue, registry, Planner, Authority contract,
or runtime execution path was created.

## Production verification

Safe deploy manifests were strictly limited to the following approved owners:

| Commit | Deploy ID | Runtime files |
| --- | --- | --- |
| `6addb25c` | `deploy-z8-14-Updatesystem-6addb25-20260813T023315` | `tools/v7-service-matrix-test`, `tools/v7-service-matrix-refresh-all`, `tools/v7-users-autoswitch` |
| `fd5ee65d` | `deploy-z8-14-Updatesystem-fd5ee65-20260813T023816` | `tools/v7-users-autoswitch` |
| `75aef372` | `deploy-z8-14-Updatesystem-75aef37-20260813T024223` | `tools/v7-users-autoswitch` |

The next ordinary `v7-autoswitch-planner.timer` cycle, not a manual Matrix or
autoswitch invocation, produced the final compact owner-backed record:

```
incident_state = INTENT_CLOSED
attempt_terminal = CURRENT_SOURCE_SCOPE_EMPTY_NO_ACTION
affected_scope_count = 12
protected_scope_count = 1
unresolved_scope_count = 0
explicitly_excluded_or_recovered_scope_count = 11
scope_classification = CERTIFICATION_ONLY
scope_membership_law = LEGACY_ALL_ASSIGNED_SCOPE_RECONCILED_TO_CONTROLLED_CERTIFICATION_EXCLUSION
```

The invariant `affected = protected + unresolved + excluded` therefore holds.
The existing Matrix retains the channel failure as passive diagnostic evidence;
the repair does not call it recovery and does not erase historical events.

## Forbidden-effect proof

All deploys and the confirming ordinary production cycle reported:

- Candidate/Packet/lease created: `false`;
- Runtime apply/routing mutation/rollback apply: `false`;
- users moved: `0`;
- Authority expansion: `false`;
- Production Maturity change: `false`.

## Tests and truth

Focused affected suites passed:

```
tests.unit.test_service_failure_automation_evolution
tests.unit.test_service_failure_episode
tests.unit.test_operator_induced_passive_capture
```

They cover ordinary/certification partitioning, certification-only fast-consumer
reconciliation, legacy all-assigned reconciliation, and preservation of an
already verified Outcome while excluding the remaining controlled identities.

## Exact successor

`CT-M0F` remains a controlled-validation latency Mission. A normal production
failover requires a fresh failed source with a non-zero ordinary production
scope. A certification-only source is not a substitute and must be consumed
only through the existing controlled-certification owner and its active,
independently authorized contract.
