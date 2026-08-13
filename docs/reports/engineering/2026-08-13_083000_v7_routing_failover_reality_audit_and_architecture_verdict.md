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
