# V7 Service Failure Automation Evolution Program

Version: `5.3`

Status: `CURRENT_PROGRAM_CONTRACT`; the sole current Service Failure health
execution contract is the V5.3 N0–N11 section below. CPS alone owns live
admission and frontier state.

Activation state owner: `CPS`

This file defines capability stages and completion contracts. It must not be
used to infer live execution, wait, stop, Authority or Production Maturity.

## V5.3 bounded Matrix / Health Detection Optimization workstream

Contract status: `REGISTERED_BOUNDED_WORKSTREAM`

Initial disposition at registration: `NOT_ADMITTED`. This is historical
registration context, not a live status field. CPS Section 0 alone owns the
current stage, Mission identity, successor, wait/blocker and admission state.

This is a temporary bounded Engineering stage inside the existing Service
Failure Automation Evolution Program. It contributes to the same broader
failover/recovery latency objective as CT-M0F by measuring and optimizing the
distinct causal segment `FIRST OBSERVABLE FAILURE SIGNAL -> CANONICAL
CONFIRMED FAILURE EVENT`. CT-M0F remains a separate latency and controlled-
validation lane with its own evidence contracts. The two lanes may exchange
evidence only through their existing owners; neither is a Runtime dependency
or completion substitute for the other, and a lane-local blocker in one does
not block the other while independent safe Engineering work is READY.

V5.3 is not a new Program, Matrix, health truth, Planner, Runtime subsystem,
watcher, daemon, queue, registry, event family, Authority owner or governance
ecosystem. Its product objective remains:

```text
BAD CHANNEL
-> FAST CONFIRMED FAILURE
-> SAFE DECISION
-> HEALTHY TARGET
-> S11 SERVER-SIDE RECOVERY VERIFIED
-> T11 CLIENT TRAFFIC RECOVERED only with independent client telemetry
```

The currently provable product KPI is `CONTROLLED FAILURE/OUTAGE ONSET -> S11
SERVER_SIDE_RECOVERY_VERIFIED`. `T0 FAILURE CONFIRMED -> T11 CLIENT TRAFFIC
RECOVERED` remains the future client-observed KPI and requires independent
client telemetry. This workstream additionally owns the Engineering
measurement residual `FIRST OBSERVABLE FAILURE SIGNAL -> CANONICAL CONFIRMED
FAILURE EVENT`; it does not move report/OMP time into Runtime.

### V5.3 current role-based recovery amendment (N0–N11)

**Status:** `CURRENT_EXECUTION_CONTRACT`.  This amendment replaces the
remaining V5.3 execution order where it conflicts with this section.  It is
not a new Program, Mission, Matrix, health truth, Runtime, Planner, queue,
watcher, timer, registry, state store, event family or Authority surface.
Earlier L1–L12 and Phase A–H text is retained only as evidence, historical
candidate rationale and reusable sub-gates; it must not restore the former
meaning of C8 or Full Matrix.

#### Current architecture identity and legacy-contract scope

```text
CURRENT_SERVICE_FAILURE_HEALTH_AND_RECOVERY_ARCHITECTURE
= V5.3 N0–N11 ROLE-BASED FAST RECOVERY ARCHITECTURE
```

```text
CURRENT_ARCHITECTURE_SUPERSESSION_LAW

V5.3 N0–N11 is the sole current Service Failure health, detection,
confirmation, target-readiness and recovery target architecture.

Every older Runtime role describing the same responsibility is superseded by
the corresponding current N0–N11 role. Historical implementation existence
does not preserve historical responsibility. Reusing an owner, primitive or
code path does not preserve its former role.

A superseded Runtime path is not a fallback. A fallback exists only when the
current N0–N11 contract explicitly names it as BACKSTOP, DEEP_BACKGROUND,
FALLBACK or CURRENT_RECOVERY.

Required semantic invariants survive. Superseded implementations survive only
for the bounded replacement window required to prove and migrate their current
consumers, then are removed responsibility by responsibility.

THE REPOSITORY AFTER N0–N11 MUST IMPLEMENT ONE CURRENT SERVICE FAILURE SYSTEM,
NOT A CURRENT SYSTEM PLUS SUPERSEDED DUPLICATE SYSTEMS.
```

An existing semantic law, table, phase order or terminal is strengthened in
place. No second architecture identity, role table, `MODE A / MODE B` contract,
retirement law, N0–N11 order or N terminal may be created beside its current
definition.

This is the only current target architecture for Service Failure health,
detection, confirmation, target readiness and recovery optimization.  Older
headings containing `active`, `current executable`, `retained executable` or
`approved execution plan` are relative to their named historical/narrow
lineage. They do not create another current V5.3 target and cannot dispatch
V5.3 work merely because the wording remains in this Program.

#### Current 2-vCPU HARD-path feasibility branch

This is a durable Program constraint, not a CPS live-status projection.  The
owner accepted `HARD_PATH_3S_FEASIBILITY_EXHAUSTED` for the current frozen
two-vCPU Runtime evidence: the five-sample nearest-rank P95 was `4769.805 ms`,
all functionally valid samples stayed within `5000 ms`, and the best valid
samples were `2393.310 ms` and `2465.968 ms`.  The product SLO remains
unchanged.

The next and only admitted feasibility investigation is
`PERSISTENT_EXISTING_OWNER_PREPARED_VALIDATION_RUNTIME`:

```text
measure exact T0 -> decision residual
-> prove or reject a material repeated process/import/scheduling boundary
-> if justified, keep the already-existing validation responsibility loaded
   inside the existing health/control owner
-> retain every current mutable owner-backed gate
-> focused falsification, Polygon, safe deploy and frozen five-sample proof
```

This branch is expressly forbidden from resizing VDSina, buying CPU/RAM,
adding a server or paid external service, changing cadence, priority, Planner,
Matrix, Authority, verifier, route writer, S11 semantics or the product SLO.
It also may not create a second Planner, Matrix, truth source, queue, timer,
watcher, routing owner, policy owner or a persistent independent control
plane.  A loaded process is only an execution optimization: Matrix generation,
source/identity scope, current assignment, target/service freshness,
capacity/reservation, policy/Authority/topology generation, anti-flap,
operation conflict and Packet/Lease/Barrier identity remain freshly validated
for every decision.  Any mismatch fails closed through the existing fallback.

The feasibility gate is binding.  If measured removable startup/import/
scheduling time cannot credibly make the current three-second HARD-path SLO,
emit `PERSISTENT_VALIDATION_NOT_JUSTIFIED_BY_MEASUREMENT` and return to the
owner without implementation.  If the bounded existing-owner implementation
is correctly deployed and its frozen series still fails, emit
`HARD_PATH_3S_2VCPU_ARCHITECTURE_EXHAUSTED`; no further micro-optimization is
legal.  Only then may an owner choose increased compute, an SLO change or a
materially different control-plane architecture.

| Retained Program family | Valid current/narrow meaning | Cannot do for V5.3 N0–N11 |
| --- | --- | --- |
| prior V5.3 L1–L12 / Phase A–H | evidence, measurements, candidate rationale and reusable acceptance sub-gates | choose architecture, restore Full-before-action, set cadence or claim T11 from server evidence |
| V5.2–V4.6 CT-M0F lineage | exact controlled cutover/sample/continuation contract when fresh CPS selects that lineage | restrict N1–N4 immediate targeted Matrix wake, become the health architecture or replace S11 semantics |
| V4.0 constant-time cohort contract | current data-plane/class/bucket invariants consumed by N5/N7/N9 | become a second health owner, detector, Planner or state surface |
| V3/V2/V1 governed execution and Authority lineage | reusable Candidate/Packet/Lease/Barrier/apply/verification/rollback, blast-radius and Authority safeguards where still owner-backed | define N cadence, health truth, primary detector, target architecture or automatic FAST admission |
| reports, old terminals and superseded revisions | historical evidence with explicit reuse/invalidation test | dispatch work, establish current state, grant Authority or override CPS/this section |

#### Current responsibility disposition

| Existing mechanism/boundary | Sole current N role | Superseded meaning |
| --- | --- | --- |
| Matrix writer/state | single canonical health/state/T0 writer; validates exact definitive evidence or performs targeted confirmation according to the N1/N4/N7 tournament | any second writer or timer-only universal T0 ownership |
| `v7-egress-diagnose` and existing system/local evidence producers | L0/L1 evidence production where owner-backed | direct T0 write, route decision or Apply |
| existing Telegram sentinel | L1T producer only for profiles where Telegram is required | old universal timing, persistence or confirmation semantics after N2 replacement |
| C8 | L3 reconciliation backstop | primary FAST detector |
| Full Matrix | L4 staggered deep background, disagreement and explicit ambiguous fallback | universal primary detector or synchronous Full-before-action gate |
| `users.registry` | current assignment and affected-scope truth | health truth or target decision |
| existing Planner | target suitability/admission and route decision | Matrix-owned route selection |
| existing Candidate/Packet/Lease/Barrier owners | governed execution identity and safety | health detection or duplicate orchestration |
| existing governed Apply path and current mutation owner(s), resolved from SYSTEM_MAP and fresh Runtime | sole legal bounded client/routing mutation boundary | a newly inferred generic `Apply` owner or signal-driven direct mutation |
| existing verification/rollback owners | failure-class-specific S11 proof, containment and rollback trigger | server evidence relabelled as T11 |
| duplicate obsolete callers/consumers after proven replacement | no current role | unnamed compatibility, shadow primary or legacy fallback |

When a retained clause conflicts with this scope table, correct its
interpretation at the clause; do not create a new plan, delete the historical
section wholesale or preserve the conflicting interpretation as a fallback.
Only CPS owns which narrow execution lineage is live.  This Program owns the
durable target contract, not volatile admission.

The product must not be optimized as one large health sweep.  It is a layered,
cost-bounded path under the existing owners:

```text
BAD OR UNUSABLE CURRENT SOURCE
-> EARLY SERVER-SIDE SIGNAL
-> MATRIX-OWNED CERTAINTY HANDLING:
   definitive L0 -> MODE A or tournament-admitted MODE B
   ambiguous L0/L1P/L1T/L2 -> bounded independent targeted confirmation
-> T0 FAILURE CONFIRMED BY MATRIX
-> AFFECTED CLIENT SCOPE + PRE-READY HEALTHY TARGET
-> EXISTING PLANNER / CANDIDATE / PACKET / LEASE / BARRIER / APPLY
-> ROUTE-BOUND SERVICE VERIFICATION
-> S11 SERVER_SIDE_RECOVERY_VERIFIED
```

`T11_CLIENT_TRAFFIC_RECOVERED` remains the product terminal.  Until a client
agent provides independent client telemetry, it is not claimable from server
facts.  The mandatory current terminal is instead:

```text
S11_SERVER_SIDE_RECOVERY_VERIFIED
= assignment changed by the existing governed path
  AND kernel routing is visible on the selected target
  AND a required service succeeds through the exact moved-client routing context
```

For Telegram, that required route-bound service check is a Telegram check.  A
successful generic target check is not a substitute.  S11 is evidence of
server-side recovery only and never relabels itself as T11.

#### Binding SLO classes and asymmetric recovery policy

#### Current 2-vCPU rollout-contract amendment

The historical `<=3 s` / `<=5 s` controlled target remains the future
optimization objective.  It was not achieved by the frozen same-fingerprint
HARD_PATH series recorded in
`docs/reports/engineering/2026-08-26_hard_path_post_fix_residual_causal_reduction.md`.
For the current deployed fingerprint and current two-vCPU substrate only, the
owner accepts a bounded rollout contract of P95 `<=7 s` and no functionally
valid sample above `8 s`.  This amendment changes neither Matrix, Planner,
Authority, Candidate, Packet, Lease, Barrier, Apply nor S11 semantics.  It
does not authorize a wider cohort, a different substrate, a new architecture,
or a claim that the historical target was met.  A functional/safety regression,
Runtime-fingerprint change or explicitly admitted architecture change
invalidates this rollout-contract reuse.

| Class | Minimum causal path | Measured target | Explicit non-goal |
| --- | --- | --- | --- |
| `HARD_PATH` | definitive existing OS/systemd/interface/tunnel/peer/route evidence -> Matrix-owned provenance/freshness/generation validation and, only if the N1/N4 tournament admits it, direct canonical T0 without a redundant source network probe; cheap or ambiguous path liveness -> independent targeted Matrix corroboration -> T0 -> S11 | historical objective P95 `<=3 s`, max `<=5 s`; current two-vCPU rollout contract P95 `<=7 s`, max `<=8 s`; production observation clock retained separately | full deep sweep before an unambiguous failure or treating an ambiguous timeout as definitive evidence |
| `TELEGRAM_CRITICAL` | Telegram is required by the active product/profile contract; fast Telegram evidence -> independent targeted Matrix corroboration -> T0 -> S11 | historical objective P95 `<=3 s`, max `<=5 s`; current two-vCPU rollout contract P95 `<=7 s`, max `<=8 s` only after its own exact controlled series; production observation clock retained separately | treating Telegram as universal for a profile where it is not required |
| `OTHER_REQUIRED_SERVICE` | active source plus distinct active profile-service contract -> lightweight protocol-appropriate sentinel -> targeted Matrix confirmation -> T0 -> S11 | N3-selected physical-failure -> T0 SLO `<=15 s`, with production observation clock and separately measured T0 -> S11 | a 1–3 second promise or a full 14-service probe for every sample |
| `AMBIGUOUS_QUALITY_OPTIONAL` | quality, partial censorship, jitter, loss, optional service or conflicting evidence -> SUSPECT/DEGRADED -> bounded confirmation or Full fallback | prompt safe classification; no fail-open | evacuation merely because an optional or ambiguous service failed |

`TELEGRAM_CRITICAL` is deliberately profile-scoped: it applies only where the
active serving profile declares Telegram required.  It is the only application
service class eligible for the 1–3-second target; Google, Auth, DNS and all
other profile-required services use `OTHER_REQUIRED_SERVICE`.

Every class records two non-interchangeable clocks:

```text
CONTROLLED / POLYGON
CONTROLLED_FAILURE_OR_OUTAGE_ONSET -> S11

PRODUCTION
FIRST_FAILED_SERVER_OBSERVATION -> S11
AND LAST_SUCCESSFUL_OBSERVATION -> FIRST_FAILED_SERVER_OBSERVATION
```

The controlled clock retains the historical target: HARD/PATH and applicable
Telegram must prove P95 `<= 3 s`, **no valid sample > 5 s**, and failure
placement immediately before a probe, immediately after a probe and
mid-interval.  The current two-vCPU rollout contract is the explicit bounded
exception above: it requires its own homogeneous service-class series with P95
`<=7 s` and no valid sample above `8 s`; it is not cross-credit from HARD_PATH
to Telegram.  Production does not invent an unobservable physical-outage
timestamp; it records the observation clock and cadence gap separately, so a
long unseen failure cannot be presented as a 3-second recovery.  For other
required services, N3 selects one exact
`SELECTED_OTHER_REQUIRED_OBSERVATION_SLO <= 15 s` from controlled evidence.
Its acceptance is worst cadence phase plus probe timeout plus confirmation,
not an average interval or an open `10–15 s` range.

`<= 3 s` is a target to be proved in the exact failure class and cohort, not a
configured promise.  Its initial budget envelope is: signal `<= 0.7 s`,
confirmation/T0 `<= 0.6 s`, target decision `<= 0.2 s`, Packet/Lease `<= 0.2
s`, apply `<= 0.6 s`, verification `<= 0.7 s`.  A failed budget remains
STOP_SAFE or falls back; it may not be hidden by averaging unrelated samples.
It is also a failed performance sample, an open Engineering residual and a
bar to the N terminal.  Every N1/N2/N4 confirmation and S11 verification must
declare class-specific timeout, retry and `MAX_WALL` values within the
remaining envelope; no serial retry may exceed it.  Negative probes are
measured independently rather than assumed to cost the same as success.

Failure and recovery remain asymmetric:

```text
FAST_FALL = compact fresh evidence plus Matrix-owned certainty handling:
            definitive L0 uses MODE A or tournament-admitted MODE B;
            ambiguous evidence requires bounded independent confirmation
SLOWER_RISE = existing conservative persistence, stability, anti-flap and
              re-admission semantics
```

No N phase weakens stale/unknown/conflicting fail-closed behavior, recovery
probation, capacity/policy checks, rollback or existing action Authority.

#### Failure-evidence certainty split and direct-T0 tournament

The current Program must not force the same confirmation path onto materially
different evidence classes.  N1, N4 and N7 must compare, rather than assume,
the following two paths under the same Matrix owner and state surface:

```text
DEFINITIVE_LOCAL_HARD_FAILURE
= owner-backed local fact that proves the exact current source responsibility
  is absent or failed, with fresh monotonic time, exact source identity,
  generation continuity and no stale/conflicting evidence
-> existing Matrix owner validates provenance/freshness/identity/generation
-> Matrix atomically records canonical T0 without repeating a source network probe
-> relevant pre-ready hot target is confirmed in parallel

AMBIGUOUS_OR_REMOTE_FAILURE_EVIDENCE
= timeout, loss, generic path miss, Telegram/DNS/application failure,
  partial censorship, quality degradation or any non-authoritative local symptom
-> SUSPECT
-> independent bounded targeted Matrix confirmation of the source/service
-> canonical T0 only after confirmation

STALE / UNKNOWN / CONFLICTING / CORRELATED
-> DEGRADED or STOP_SAFE
-> no client movement; use bounded revalidation or explicit Full fallback
```

An L0 producer never writes T0, changes eligibility or applies a route.  The
Matrix remains the single canonical health/state/T0 writer in both paths.  A
direct canonical T0 is therefore a Matrix-owned consumption mode for exact
definitive evidence, not a second health owner and not a bypass of Planner,
target readiness, Candidate, Packet, Lease, Barrier, Apply, verification,
rollback or Authority.

The Polygon tournament must compare:

```text
MODE A = every hard signal -> repeat source probe -> Matrix T0
MODE B = definitive local hard signal -> Matrix validation/direct T0;
         ambiguous signal -> repeat source probe -> Matrix T0
```

Use the same interface-down, process-death, tunnel-loss, route-loss, stale
event, wrong-generation, restart/replay, transient timeout, endpoint glitch,
Telegram, DNS, partial-service, correlated-provider and recovery scenarios.
Measure controlled onset->T0, onset->S11, false positive/negative, duplicate
episodes, stale/conflict rejection, target-readiness correctness, probes,
CPU/RSS/network/writer pressure and automatic caller/consumer behavior.

`MODE B` is admitted only for the exact definitive classes that prove all of:

- no false-failure, stale-generation, replay or restart-safety regression;
- Matrix remains the only canonical T0 writer and produces the same downstream
  contract consumed by Planner and governed execution;
- source-probe removal yields a material measured latency or load improvement;
- target readiness remains fresh and independently checked before Apply;
- disagreement, missing provenance or incomplete identity falls back to
  `SUSPECT` plus targeted confirmation, never fail-open.

If any condition fails, that class retains `MODE A`.  Vendor immediate-failure
behavior is evidence for the tournament, not authority to select `MODE B`.

#### Canonical layer placement and strict ownership

| Layer | Role | Existing owner/contract reused | Prohibited shortcut |
| --- | --- | --- | --- |
| `L0` | classify fresh owner-backed local evidence as definitive or ambiguous; ambiguous evidence creates `SUSPECT`, while a tournament-admitted definitive class may be consumed by the Matrix owner as direct canonical T0 without a redundant source probe | `v7-egress-diagnose`, existing systemd, interface/tunnel and route/path evidence | a new watcher, direct T0 writer, event truth or direct route apply |
| `L1P` | cheap active-source path liveness | Matrix/diagnose existing-owner inputs | Google/YouTube/full HTTP Matrix as the liveness probe |
| `L1T` | Telegram-critical health of active sources and bounded hot targets | existing Telegram sentinel and Matrix service semantics | a fresh all-target Telegram sweep after T0 |
| `L2` | other required service health by active source and distinct profile contract | Matrix/profile/DNS service semantics | per-user polling or treating optional services as channel failure |
| `L3` | C8 reconciliation backstop | existing bounded C8/deadline-loop Matrix work | calling C8 the primary critical detector |
| `L4` | staggered deep, diagnostic, disagreement, stale/conflict, quality, cold-target and recovery support | existing Matrix canonical writer and Full fallback | global synchronous Full-before-action or a second writer |

L1P/L1T/L2 and every ambiguous L0 observation create `SUSPECT` only.  A fresh
exact definitive L0 class may skip only the redundant source network probe
after its N1/N4/N7 tournament gate passes; it still enters through the Matrix
owner for canonical validation and atomic T0.  Matrix alone retains canonical
health/state and T0 ownership.  Every other fast signal wakes the existing
bounded targeted Matrix confirmation through its legal existing-owner
invocation.  Neither mode bypasses Matrix, Planner, Packet, Lease, Barrier,
apply, verification or rollback.

Correlated evidence is fail-safe and must suppress evacuation storms:

```text
SOURCE TELEGRAM FAIL + COMPATIBLE HOT TARGET TELEGRAM PASS
-> source-specific Telegram suspicion; bounded confirmation may proceed

SOURCE TELEGRAM FAIL + multiple independent compatible hot targets FAIL
-> correlated/global Telegram incident; DEGRADED + bounded revalidation
-> no Telegram-only evacuation

COMMON PATH-PROBE TARGET FAILS ACROSS MANY EGRESS
-> shared-probe/correlated incident; not "all egresses failed"
```

N2/N7/N9 must prove this distinction under endpoint glitch, burst and
correlated-failure cases.  A source-specific action never follows merely from
one shared external endpoint being unavailable.

Historical roles are superseded; only useful primitives survive in explicit
current roles:

```text
C8 30-SECOND FAST PRIMARY                 -> L3 RECONCILIATION BACKSTOP
FULL MATRIX TIMER-DRIVEN FAILURE DETECTOR -> L4 DEEP/FALLBACK FRESHNESS HORIZON
TWO SLOW POLLING SAMPLES AS PRIMARY PROOF -> fallback/reconciliation semantics
```

`KEEP CURRENT PRIMITIVE != KEEP HISTORICAL ROLE`. The former primary-detector,
timer-wait, cadence, synchronous confirmation and orchestration meanings are
not current fallbacks and must disappear after the corresponding N replacement
passes the responsibility-scoped retirement gate.

The deep horizon means every relevant egress receives a deep refresh within
the measured horizon (initially 15 minutes), not one burst at the horizon
boundary.  Any staggered implementation must reuse Matrix state and writer
serialization; it may not add a timer, queue, cache, registry or truth source.
N6 additionally proves: L0/L1/L2/N4 always outrank DEEP; bounded global deep
probes/sec and concurrency; fair coverage without cold-egress starvation; no
catch-up burst; and a missed horizon becoming `STALE` rather than a probe
storm.  DEEP cannot delay decisive HARD/PATH, Telegram or required-service
confirmation.

#### Scale, probe and data-plane invariants

```text
HEALTH_COST = O(active egresses + distinct active profile-service contracts
                + bounded hot targets + active incidents)
HEALTH_COST != O(users)
```

10,000 users on one source with the same profile must consume one health
contract, not 10,000 probes.  A hot target set is bounded by `H <= 2–4` per
active source/profile and is current for path liveness, Telegram readiness
where Telegram is required, capacity, policy, generation and role.  N2/N5
select and measure separate freshness budgets for path, Telegram, capacity,
policy, generation and role; one "current" timestamp is insufficient.  Hot
target health is deduplicated by compatible target-plus-critical-service
fingerprint:

```text
HOT_TARGET_HEALTH_COST = O(distinct compatible target + critical-service contract)
NOT O(source x target relation)
```

Each active source claiming a 3-second class requires at least one fresh,
pre-ready eligible compatible hot target before the failure.  Otherwise the
exact state is `NO_3S_TARGET_CAPACITY`, never a fictional SLO pass.  On
suspicion, source confirmation and relevant hot-target confirmation are
eligible to run in parallel under the existing owner’s bounded concurrency;
state commit remains single-writer.

Every N phase measures and enforces a probe budget: probes/sec, bytes/sec,
processes, sockets, CPU, peak RSS, endpoint pressure, Matrix writes/sec,
writer/lock pressure and timeout/deadline misses.  The mandatory scale matrix
is egresses `7/50/100/1000`, users `250/500/10,000+`, and profile shapes
`one/few/many`, including many-users/few-egresses and many-users/many-egresses.
`1000 x 14 x 1-second` service HTTP is forbidden.  At 1,000 active egresses,
the selected L1 mechanism must prove its bounded implementation and endpoint
budget; spawning a heavyweight process per probe is not a valid result.

The data plane is part of the critical path.  Before a class may claim S11,
the chosen hot target tunnel and routing primitives must already be ready.
N5 consumes the existing V4 constant-time cohort/data-plane contract:
prepared decision, class/bucket identity where applicable, capacity reservation,
bounded kernel commit and no hidden incident-time `O(users)` scan.  Measure
make-before-break and governed apply for compatible cohorts of `1`, `10`,
`100` and `1000` affected clients before N7.  The 3-second result applies to
the eligible compatible routing class/cohort, not merely its first moved
identity.  Exceptional identities may use an explicit slower fallback.  A
batch/cohort optimization is admissible only when the existing
Packet/Lease/Barrier/rollback invariants and per-client verification remain
true.

#### N0–N11 execution order

Each phase is an existing-owner bounded residual, not a new Mission by name.
The current CPS/OMP frontier still controls admission.  Completion of code,
tests, report, deploy or Polygon alone never advances a phase.

| Phase | Required result and gate |
| --- | --- |
| `N0` | Record this product/SLO amendment in the existing Program; reconcile current callers, consumers, state and prior V5.3 evidence against the new roles. |
| `N0a` | **Runtime execution envelope prerequisite.** Profile and reduce the existing governed downstream executor until it completes one controlled causal path without unbounded materialisation, OOM or repeated automatic retries. It is mandatory before N8 controlled Runtime admission and before production activation of a new cadence; it does not block independent N1–N7/N9 Polygon, profiling, implementation or scale work. |
| `N1` | `HARD_FAILURE_EVENT_DRIVEN_SIGNAL_INTEGRATION`: reuse existing local evidence, define exact definitive-versus-ambiguous predicates with provenance/freshness/identity/generation gates, and tournament cheap path liveness at `250 ms/500 ms/1 s/2 s`; choose only measured safe evidence classes and cadence. |
| `N2` | `TELEGRAM_CRITICAL_FAST_HEALTH_V2`: tournament `250 ms/500 ms/1 s`, thresholds and independent evidence against persistent outage, transient loss/timeout, endpoint glitch, correlated failure, 1,000 egresses and hot-target readiness. |
| `N3` | Other-required service sentinels: tournament `5 s/10 s/15 s/30 s` by current source plus distinct required profile contract, using DNS/TCP/TLS/light HTTP only where protocol-appropriate. |
| `N4` | Immediate Matrix-owned confirmation/direct-T0 tournament: compare `MODE A` repeat-source confirmation against `MODE B` direct canonical T0 for exact N1 definitive classes. Ambiguous signals always invoke current-source/service confirmation now; the relevant hot target is checked concurrently where safe; no wait for the next periodic Matrix cycle. |
| `N5` | `PRE_READY_TARGET_AND_PREPARED_DATAPLANE`: pre-failure hot-target readiness for the bounded top-H set plus existing V4 constant-time prepared data-plane proof; include freshness, dedup, coverage, capacity, policy, generation, role and 1/10/100/1000 compatible-cohort readiness. |
| `N6` | Transform Full Matrix from burst semantics to a measured staggered deep-refresh horizon under the existing Matrix writer; retain fallback for disagreement, stale/conflict and ambiguous cases, with FAST priority, fairness, bounded deep rate/concurrency and no catch-up storm. |
| `N7` | Causal Polygon tournament from controlled failure/outage onset to S11: interface/tunnel/path/Telegram/DNS/other-required/multi-service/partial, including the required `MODE A` versus `MODE B` comparison, stale/wrong-generation/replay/restart falsification and proof that only admitted definitive classes skip a redundant source probe. Historical HARD/PATH and applicable Telegram objective remains P95 `<=3 s`, max `<=5 s`; the current two-vCPU rollout contract is P95 `<=7 s`, max `<=8 s`, with a separate exact Telegram series and no cross-credit. Test each cadence phase offset and correlated failure. |
| `N8` | Controlled unattended Runtime proof: signal -> confirmation -> T0 -> selection -> governed apply -> S11 with real caller, consumer, idempotency, duplicate suppression, restart safety and no manual CLI seam. |
| `N9` | Full scale tournament using the mandatory egress/user/profile matrix and all resource/pressure measurements. |
| `N10` | Bounded ordinary rollout only after N8/N9: controlled -> one ordinary-like case -> small cohort -> bounded production, with rollback and no manufactured ordinary failure. Before consuming the one-use Authority, the existing Core-primary owner must read-only prove that the exact 2–4 member move leaves every non-member class and class-egress mapping unchanged. After canonical cohort assignments, that owner must publish one atomic affected-cohort projection commit, retire only the cohort's superseded per-user primary rules, prove exact affected scope and whole-system verification, and require each member's current-profile service/path S11. A per-user full-population rebuild is not an N10 admission. |
| `N11` | `WHOLE_SYSTEM_ZERO_RESIDUE_RECONCILIATION`: final consumer-verified repository reconciliation, not the first cleanup stage. It proves that earlier safe responsibility-scoped replacement closure removed obsolete timer-only critical behavior, duplicate persistence, universal Full-before-action, superseded shadow branches and expired compatibility code. |

#### Per-phase replacement closure

An N phase that replaces a Runtime responsibility cannot claim replacement
closure until the exact superseded responsibility has been safely retired:

```text
OLD RESPONSIBILITY
-> exact caller / consumer / state / fallback / rollback map
-> shared-owner and narrow-CPS-lineage dependency check
-> current N replacement implemented
-> isolated functionality and safety proof
-> SLO/resource proof where applicable
-> same-Matrix Polygon proof
-> integrated end-to-end consumer proof
-> controlled unattended Runtime proof where applicable
-> exact consumer migration
-> one bounded fallback observation window
-> no-caller / no-consumer / no-state-dependency proof for that responsibility
-> obsolete code/config/timer/unit/state/test/fixture/caller removed
-> responsibility residue = 0
-> REPLACEMENT CLOSURE
```

Removing a superseded responsibility never implies deleting a shared file,
owner, primitive or state surface still used by another current responsibility
or a fresh CPS-selected narrow lineage. Static search alone is insufficient.

If N7/N8 supplies integrated evidence needed by an earlier N replacement, that
earlier phase remains `IMPLEMENTED_REPLACEMENT_PENDING_RETIREMENT_PROOF`; it
does not delete its safe predecessor early and does not claim full replacement
closure. N1–N6 name and shrink their own replacement responsibility; N7–N10
prove it does not reappear; N11 only performs final whole-system reconciliation.

For N4 specifically, periodic-wait dependency may be retired only for exact
classes whose immediate handling is proven. `MODE A` remains for every class
that fails direct-T0 admission, and every ambiguous class retains independent
targeted source/service confirmation.

#### Automation, removal and residue-closure law

For every admitted N transition, prove a real automatic chain:

```text
producer -> legal caller -> existing consumer -> canonical state -> next owner
-> idempotent outcome/receipt -> bounded terminal or exact STOP_SAFE
```

Manual invocation may create Engineering evidence but cannot close N8/N10.
Duplicate suppression, restart recovery, deadline/timeout containment and
safe re-entry must be tested at every new automatic edge.

##### V5.3 fast-wake, controlled-evidence and terminology precedence

For N0–N11 only, L0 local failure evidence, L1P path liveness, L1T
profile-required Telegram sentinel and L2 required-service sentinel are legal
immediate wake producers for Matrix-owned certainty handling. A definitive L0
class follows `MODE A` or tournament-admitted `MODE B`; ambiguous L0 and all
L1P/L1T/L2 evidence require bounded targeted source/service confirmation. Legacy
statements that Matrix/timer is the only or sole wake producer apply only to
their expressly named CT-M0F sample-generation or legacy regular-wake
semantics.  They must not delay, prohibit or reinterpret N1–N4 confirmation.
Likewise, a historical Full-Matrix comparison is not an executable
Full-before-action requirement for HARD/PATH, applicable Telegram or decisive
required-service cases.

Evidence classes remain separate:

```text
POLYGON DELIBERATE FAULT INJECTION = allowed Engineering evidence
EXACT-OWNER-AUTHORIZED CONTROLLED CERTIFICATION = allowed only in its admitted envelope
MANUFACTURED ORDINARY PRODUCTION FAILURE = forbidden
REPEATED PRODUCTION ACTION MERELY TO FILL A SAMPLE COUNT = forbidden
```

For N0–N11 consumption only, historical server-bound
`CLIENT_TRAFFIC_RECOVERY_*` / route-bound probe receipts are renamed
`S11_SERVER_SIDE_RECOVERY_*`.  They remain reusable server evidence but cannot
satisfy `T11_CLIENT_TRAFFIC_RECOVERED` or remote client application recovery
without independent client telemetry.

No code is retained merely because it is historical. Before deleting or
deferring a branch, the existing owner must prove its caller(s), consumer(s),
state effect, shared responsibilities, narrow current lineage,
fallback/rollback contribution and replacement. The only legal retirement
sequence is:

```text
CONSUMER MAP -> REPLACEMENT PROVEN -> SAME-MATRIX POLYGON + CONTROLLED RUNTIME
-> ONE BOUNDED FALLBACK WINDOW -> NO-CALLER/NO-CONSUMER/NO-STATE-DEPENDENCY PASS
-> DELETE OR EXPLICITLY DEFER WITH OWNER + RE-ENTRY CONDITION
```

`EXPLICITLY_DEFERRED` is legal only when the exact responsibility, current
owner, current live caller, current live consumer or unfinished integrated
dependency, reason replacement is incomplete, bounded role, re-entry,
deletion and expiry/revalidation conditions are recorded. It is illegal merely
because code may be useful later, is historical, is called compatibility or
has not yet been cleaned. After replacement proof and consumer migration, a
deferred residue for that responsibility must be deleted.

```text
CURRENT_FALLBACK != LEGACY_PATH_LEFT_EXECUTABLE
```

Every surviving fallback names its current owner, caller, consumer, exact
trigger, exit condition and safety role. An obsolete primary cannot survive by
being renamed fallback.

After safe migration of the same responsibility and consumer scope,
`NEW PRIMARY + OLD PRIMARY`, equivalent event and timer primaries, duplicate
confirmation consumers, duplicate FAST persistence, competing current-state
projections, competing target-readiness paths and equivalent mass/per-user
Apply paths are forbidden. Legal multiplicity is one primary plus explicitly
current `BACKSTOP`, `DEEP_BACKGROUND`, `FALLBACK` or `CURRENT_RECOVERY`.

Static search alone is insufficient. Conversely, no legacy function, timer,
branch or compatibility path may remain unclassified: `ACTIVE`, `BACKSTOP`,
`DEEP_BACKGROUND`, `FALLBACK`, `RETIRED_DELETED`, `EXPLICITLY_DEFERRED` or
`EXTERNAL_BLOCKED`, each with owner and consumer.  New code must replace or
integrate an existing edge; it cannot create orphan loops, duplicate requests,
parallel health truth or unbounded work.

#### N-program terminal

`MATRIX_ROLE_BASED_RECOVERY_OPTIMIZATION_TERMINAL_COMPLETE` requires all of:

1. HARD/PATH and applicable Telegram-critical classes meet the active accepted
   controlled contract: historical objective P95 `<=3 s`, max `<=5 s`, or the
   explicitly bounded current two-vCPU rollout contract P95 `<=7 s`, max
   `<=8 s`, with separate class-specific evidence and phase-offset evidence;
   production
   first-failed-observation and last-success->first-failure clocks are stored
   separately.  Other required services have one selected measured detection
   SLO `<=15 s`, including cadence phase, timeout and confirmation.
2. C8 is a proven backstop; Full Matrix is a proven bounded deep/fallback
   horizon and neither blocks decisive unambiguous recovery.
3. Hot targets have fact-specific freshness budgets, global compatible-target
   dedup and SLO coverage; source/target checks remain fail-closed, correlated
   Telegram/shared-probe failure cannot create an evacuation storm, and S11 is
   route-bound, target-identity-bound and failure-class-specific.
4. Existing V4 constant-time data-plane invariants pass for `1/10/100/1000`
   compatible affected identities; no incident-critical `O(users)` path or
   first-identity-only SLO claim remains.  The `7/50/100/1000` and
   `250/500/10,000+` scale matrix proves the remaining dedup and bounded cost.
5. Full Matrix is staggered, bounded and fair, has no catch-up storm and never
   delays FAST. N8 proves an unattended controlled real caller/consumer chain and N10
   proves the lawful ordinary safety boundary.  T11 is claimed only if an
   independent client signal exists.
6. Every old and new code/timer/consumer path has passed the classification
   and retirement law; timer-only wake statements are scoped away from N0–N11,
   legacy server-bound client-recovery names are mapped to S11, and no
   redundant, unreachable or duplicate path remains.
7. Every material hard-failure class has a measured `MODE_A_RETAINED` or
   `MODE_B_DIRECT_T0_ADMITTED` disposition.  Any direct-T0 class proves exact
   provenance, freshness, identity/generation continuity, replay/restart
   safety, single Matrix ownership, unchanged downstream contract, independent
   target readiness and a material latency/load gain; ambiguous evidence can
   never enter direct T0.
8. Each completed replacement responsibility has passed per-phase integrated
   proof, bounded fallback observation, exact consumer migration and zero
   responsibility residue. N11 proves zero unclassified timers/branches,
   duplicate owners/decision paths, superseded wake/confirmation/persistence
   paths, no-caller code, no-consumer outputs, obsolete compatibility/state/test
   surfaces and old executable contracts for the same N responsibilities.

This document contract makes eventual zero superseded Runtime residue binding;
it does not claim current Runtime already satisfies the N11 terminal.

`N0a` completed at deployed commit `f42e2908` with bounded Runtime evidence in
`docs/reports/engineering/2026-08-23_131740_v5_3_n0a_runtime_memory_envelope.md`.
The former 1.7 GiB OOM path now remains below 180 MiB in the current-state
Polygon and performs no automatic retry. This closes only the execution-memory
prerequisite; it does not admit a target, Runtime trigger, route change or S11.

`N1–N4` engineering and Polygon tournament completed at implementation commits
`c6024218` and `92064629`; the exact evidence is recorded in
`docs/reports/engineering/2026-08-23_140500_v5_3_n1_n4_role_signal_tournament.md`.
The selected current target is: one-second HARD scan; Matrix-validated direct
T0 only for fresh identity-bound `INTERFACE_DOWN_OR_MISSING`; one-second
Telegram-required-profile rotation with two distinct failed endpoints;
five-second bounded other-required-service observation with C128 and existing
Matrix targeted confirmation. All ambiguous, stale, replayed, correlated or
conflicting evidence remains fail-closed. These capabilities are deployed but
are not yet the active Runtime caller: exact consumer migration and predecessor
retirement remain N7/N8 responsibilities and cannot be claimed from this block.

`N5–N6` completed at deployed commit `c74db2c8`. Exact evidence is split by
logical responsibility:

- `docs/reports/engineering/2026-08-23_143052_v5_3_n5_pre_ready_target_and_prepared_dataplane.md`;
- `docs/reports/engineering/2026-08-23_143052_v5_3_n6_staggered_deep_matrix.md`.

The existing Planner now projects a bounded official top-H (`H <= 4`) hot
target/service set with fact-specific freshness and fail-closed
`NO_3S_TARGET_CAPACITY`; the existing V4 Routing Core remains the prepared
data-plane owner. The existing Matrix refresh owner now supports a restart-
stable 15-slice DEEP horizon, bounded concurrency and no catch-up burst while
retaining the explicit Full fallback. Current production advisory evidence has
six prepared semantic classes, four deduplicated hot target/service contracts
and `PREPARED_CLASS_DECISION_FRESH`, with zero route mutation and zero users
moved. These capabilities are deployed but not yet activated as the production
role caller: the predecessor Full/Telegram timers remain until N7 integrated
proof and N8 caller migration prove safe replacement.

`N7` completed at deployed commit `1055f90f`; exact evidence is recorded in
`docs/reports/engineering/2026-08-23_151500_v5_3_n7_causal_polygon_tournament.md`.
The tournament admits direct T0 only for fresh, identity-bound
`INTERFACE_DOWN_OR_MISSING`; all tunnel/path/route, Telegram, DNS, other-service,
multi-service and partial evidence retains targeted confirmation or Full/
`STOP_SAFE`. HARD/PATH and Telegram causal distributions meet their declared
limits, DNS/other/multi remain below 15 seconds, and stale, wrong-generation,
replay, restart, correlated-failure and role-isolation falsification passed.
The official prepared set is two targets (`awg0`, `awg3`); its path probes take
about 70 ms and its four-service role takes 1.492 seconds. Production also
proved that the remaining 3--7 second delay is shared-lock contention from the
still-active predecessor Telegram timer, not probe time. No route changed, no
client moved and N7 claims S11 only.

`N8` completed at deployed commit `4cb03fdf` plus its immediate self-target
selection follow-up. Exact evidence is recorded in
`docs/reports/engineering/2026-08-23_170201_v5_3_n8_unattended_runtime_cutover.md`.
The deployed `v7-health.service` automatically detected an isolated Polygon
failure, woke the existing Matrix/Planner consumer and moved exactly one
certification client through Candidate/Packet/Lease/Barrier/Apply/S11 without
a manual Planner or apply invocation. Route, target-bound payload, Outcome and
Learning passed; the source was restored, ordinary-user delta was zero, and
the repaired consumer peaked near 323.8 MiB instead of the earlier 1.6 GiB
OOM. Full/Telegram predecessor timers remain disabled. The proof is S11 only;
T11 still requires independent client telemetry.

The real automatic sample also measured about 63.4 seconds from Polygon onset
to S11. It therefore closes N8 automation semantics but does **not** satisfy
the terminal 3--5 second latency law. The next executable V5.3 block is
**N9 FULL_SCALE_AND_CRITICAL_PATH_TOURNAMENT**: run the mandatory scale/resource
matrix and compare reuse of the prepared top-H projection plus exact
role/profile-required S11 verification against the currently broad selection
and payload spans. The measured-safe winner is implemented in existing owners;
Full remains the stale/conflict/disagreement fallback.

`N9` completed at deployed commits `d24c7b66`, `63fd4128` and `b8d16492`.
Exact evidence is recorded in
`docs/reports/engineering/2026-08-23_180000_v5_3_n9_full_scale_and_critical_path_tournament.md`.
All 36 mandatory scale cells passed. The worst 1,000-egress/10,000-user/many-
profile prepared projection contains 10,000 compact classes, 40 deduplicated
hot contracts, is 11.15 MB and builds in 0.989 seconds on Polygon. The exact
N3 capacity gate rejects a physically impossible 47-second FAST batch before
opening sockets and retains staggered DEEP. After production deadline
isolation, HARD/Telegram/hot-PATH P95 were respectively 327/736/800 ms and
maxima 524/1,113/1,162 ms, with zero command failures; five skipped one-second
starts preserved an approximately two-second worst observation gap inside the
declared 3/5-second law. No route changed and no client moved in N9. The next
executable phase is `N10_BOUNDED_ORDINARY_ROLLOUT`; T11 remains unclaimed.

### V5.3 integrated T0–T11 latency-optimization track

`V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION` is a bounded track
inside this V5.3 workstream, not a Program, Mission, owner, architecture,
implementation, state surface or Runtime actor. Its question is deliberately
wider than “can Matrix run probes faster?”:

```text
EXTERNAL FAILURE OCCURS
-> FIRST OBSERVABLE SIGNAL
-> CANONICAL CONFIRMED FAILURE
-> SAFE DECISION
-> S11 SERVER-SIDE RECOVERY VERIFIED
-> T11 only when independent client telemetry exists
```

For N0–N11 consumption, every older T0→T11 or client-recovery label in this
retained evidence track is interpreted as T0→S11 when its terminal evidence is
only server-bound route/service verification.  It may satisfy T11 only when an
independent client signal is present.  Where an independently attributable
external failure boundary is available, the track maps controlled onset to
S11; where it is not observable, it says `UNKNOWN`, records first failed
server observation and cadence separately, and never manufactures a live
failure merely to fill the clock. Report/OMP/history/certification tail time
is excluded from the recovery clocks.

This track is retained as the evidence and comparison predecessor of the
current N0–N11 execution contract above.  Its L gates are reusable only where
they do not conflict with the binding role/SLO/terminal, scale and retirement
rules of that amendment.  The previous
`TARGET_ARCHITECTURE_REFINED_EXISTING_OWNER_VARIANT` result remains a
historical, evidence-backed **candidate**, not a winner.  The current CPS/OMP
owner alone decides whether a later residual becomes an admitted Mission.

#### Latency track sequence and terminals

The following gates replace any interpretation that V5.3 should select a FAST
model merely because a benchmark or a candidate exists. They are ordered
evidence inside the existing V5.3 phases; they do not create twelve Missions.
Existing Phase A–H labels remain the implementation-facing sections below.

| Gate | Required output | Existing V5.3 phase/consumer | Terminal |
| --- | --- | --- | --- |
| L1 | Current T0–T11 map: owner, code path, input/output, wait, timeout, retry, persistence, lock, serial/parallel, blocker, placement and measurement status for every span | Phase A → Phase B/E | `CURRENT_T0_T11_LATENCY_MAP` |
| L2 | Seven-class latency matrix: full channel, tunnel-up/Internet-down, Telegram-only, critical-service, quality, recovery and false failure | Phase B → Phase E/F/H | `FAILURE_CLASS_LATENCY_MATRIX` |
| L3 | Detection vs confirmation vs decision vs action responsibility for every signal | Phase A/B → Planner/Matrix consumers | `SIGNAL_RESPONSIBILITY_MODEL` |
| L4 | Test role matrix: failure confirmation, target readiness, quality ranking, recovery, post-switch verification and deep diagnostic | Phase A/B → Phase F/H | `TEST_ROLE_MATRIX` |
| L5 | Root latency contributors A–G: cadence, execution, persistence, freshness, target readiness, ordering and verification | Phase A/B → Phase E | `TOP_T0_T11_LATENCY_CONTRIBUTORS` |
| L6 | Safe optimization register with expected gain, risk, existing owner, test safety, rollback and architecture-decision need | Phase E/F/H | `LATENCY_OPTIMIZATION_REGISTER` |
| L7 | Map each proved V7 problem to a mature-system mechanism; retain or reject duplicate vendor research | Phase C → Phase D/E | `PROBLEM_TO_PATTERN_MAPPING` |
| L8 | Form materially distinct V7 candidate architectures from the proved contributors; no winner is selected at this gate | Phase D → Phase F/G/E | `V7_ARCHITECTURE_CANDIDATES_CONSUMED` |
| L9 | Polygon tournament: run the same failure matrix for every candidate and capture T0→T11, probes, FP/FN, recovery, stale/conflict and safety deltas | Phase F/G → Phase E | `CONTROLLED_LATENCY_TOURNAMENT_CONSUMED` |
| L10 | Scale tournament at 7, 50, 100 and 1,000 egresses: probe count, latency, CPU, RAM, locks, network pressure and complexity | Phase F/G → Phase E | `LATENCY_SCALE_TOURNAMENT_CONSUMED` |
| L11 | Minimal implementation only after a proved root cause, chosen solution, safety proof and baseline; lifecycle is shadow → controlled → production | Phase H → existing owners | normal existing OMP implementation terminal |
| L12 | Before/after proof of client-recovery effect, decision equivalence and safety | existing consumers → CPS | `T0_T11_BEFORE_AFTER_PROOF_CONSUMED` |

L1–L6 may reuse the compact report
`docs/reports/engineering/2026-08-20_235500_v5_3_t0_t11_latency_trace_and_safe_optimization_register.md` only to the extent its evidence is marked static, Polygon or Runtime-unknown. A later Runtime observation must extend the existing evidence/owner-backed report rather than silently promote static timing to production fact. No gate is complete merely because a document names it.

The problem-to-pattern rule is mandatory:

```text
PROVED V7 LATENCY/SAFETY PROBLEM
-> MATCHED MATURE-SYSTEM MECHANISM
-> EXISTING V7 OWNER AND MEASURABLE HYPOTHESIS
-> REUSE / ADAPT / REJECT
-> ARCHITECTURE DECISION ONLY IF A MATERIAL GAP REMAINS
```

Examples are directional, not implementation authority: slow failure
confirmation may justify examining BFD, object tracking or HAProxy fall/rise;
false switching may justify hysteresis and recovery thresholds; quality
degradation may justify Performance-SLA patterns; probe cost may justify
Envoy-style health placement. A commercial mechanism never becomes a V7
candidate before L5 identifies the matching V7 problem.

The read-only Mission `V7_FAILURE_DETECTION_AND_HEALTH_MODEL_OPTIMIZATION_V1`
is consumed as discovery/design evidence from commit `643077b4`. Its verdict
is `RECOMMEND_MODEL_B_FAST_PLUS_DEEP_USING_EXISTING_MATRIX_OWNER`. Repeating
that audit is forbidden unless one of its declared invalidation triggers
fires: the existing Matrix owner cannot express a bounded subset, target
freshness cannot survive Planner revalidation, anti-flap regresses, writer
lock/resource safety fails, or an ordinary failover receipt contradicts the
timing model.

That verdict is a `STRONG_STANDING_ARCHITECTURAL_HYPOTHESIS`, not a final
implementation decision. It proved the dominant current delay and made Model
B the leading hypothesis, but Phase C is not post-hoc justification for a
preselected design. Phase D/E may confirm or narrow Model B, merge Model C into
it, refine an implementation assumption or reject that assumption when
evidence requires. A fundamentally new Model D still requires the existing
measured-gap admission rule.

Invariant:

```text
MODEL_B_IS_LEADING_HYPOTHESIS_NOT_FINAL_IMPLEMENTATION_ARCHITECTURE_UNTIL_PHASE_C_D_E_CONSUMED
```

The first candidate identified at registration is
`V7_MATRIX_FAST_SOURCE_AND_TARGET_PROBE_ADMISSION_V1`. It is not an active
Mission merely because this contract names it. CPS must atomically admit the
exact Mission identity through the existing OMP lifecycle before any source,
Runtime, deploy or production mutation. The current disposition must always be
read from CPS; this Program must never retain or overwrite a volatile Mission
status. Any different current CPS successor continues to win.

### V5.3 owner and truth boundary

| Responsibility | Existing owner reused | Forbidden transfer |
| --- | --- | --- |
| Matrix rows, freshness and canonical failure episode | `tools/v7-service-matrix-refresh-all` and `tools/v7-service-matrix-test` under the existing Matrix writer/lock | OMP, report, fast-path helper or second state writer becoming health truth |
| Protocol/passive fast signals | existing protocol-specific producers, including `tools/v7-telegram-sentinel` where applicable | direct route apply or competing event schema |
| Source scope and target eligibility | existing Matrix, assignment, quality, capacity and Planner owners | Matrix selecting or moving users |
| Persistence, anti-flap and recovery admission | existing Matrix/policy/recovery owners | weakened thresholds inferred from benchmark defaults |
| Decision and execution | existing Planner, Packet, lease, restore-barrier, apply and verification owners | workstream or OMP becoming Runtime dependency |
| Engineering lifecycle | existing OMP admission, Mission completion, CPS atomic projection and Engineering Report owners | parallel lifecycle or volatile truth in this Program |

FAST and DEEP are two work placements under one Matrix truth. They must never
produce competing health states or failure events.

V5.3 optimizes the complete existing decision system, not only service-probe
execution:

```text
V7 CHANNEL HEALTH / TEST / STABILITY / READINESS SYSTEM
```

Mandatory principle:

```text
SERVICE_MATRIX_TESTS_ARE_ONE_EVIDENCE_FAMILY_NOT_THE_WHOLE_HEALTH_SYSTEM
```

The scoped system includes every existing producer, current-state projection
and consumer that can prove transport/interface/process liveness, Internet or
DNS reachability, required-service and partial-service health, latency/loss/
jitter degradation, persistence, flap/recovery state, target suitability,
capacity/reserve, kernel/route correctness or post-switch client recovery.
Runtime-critical, precomputed, diagnostic/background and Engineering-only
work must remain explicitly separated.

### V5.3 lane independence and parallel-frontier rule

Invariant:

```text
MATRIX_HEALTH_OPTIMIZATION_PROGRESS_MUST_NOT_DEPEND_ON_CT_M0F_CONTROLLED_SUBSTRATE_OR_NATURAL_L8_WHILE_INDEPENDENT_ENGINEERING_WORK_IS_READY
```

Absence of an eligible controlled VLESS identity, expiry of a controlled
reservation, lack of a controlled-production opportunity, an unavailable
lawful controlled action or absence of Natural L8 blocks only the exact
criterion that requires that evidence class. It does not block independently
admitted read-only profiling, implementation, focused tests, replay, fault
injection, Polygon Engineering, scale modelling or safe deploy. CT-M0F
controlled-production evidence may satisfy only criteria that explicitly
require that class; it cannot be cross-credited as ordinary/natural evidence.
No ordinary production action, or uncontrolled controlled action, may be
manufactured merely to advance V5.3. Existing-owner Polygon fault injection
and an exact-owner-authorized controlled certification action remain lawful
only within their admitted envelope and never become ordinary evidence.

Under existing OMP `NO_UNNECESSARY_WAITING`, parallel-frontier, dynamic
Mission-compression and arbitration laws, any Matrix criterion blocked by
independent Authority, controlled substrate, external owner, Natural L8,
production-incident absence or unavailable lawful action must be handled as:

```text
EXACT LANE-LOCAL BLOCKER
-> preserve existing owner and re-entry condition
-> recompute remaining V5.3 criteria
-> select the smallest independent READY Matrix Engineering residual
-> continue through the existing OMP/CPS lifecycle
```

The whole workstream may wait only when no safe independent executable
criterion remains. This rule creates no scheduler, queue, owner, Mission or
parallel lifecycle and never weakens Authority, safety or evidence-class
requirements.

### V5.3 ordered evidence phases

These are evidence gates inside one bounded workstream, not eight mandatory
Missions. OMP forms another Mission only when the preceding consumed evidence
proves a real residual with an existing owner.

`V5_3_DECISION_ORDERING_LAW` is mandatory even when several gates are consumed
inside one bounded Mission:

```text
CURRENT REALITY / ATLAS
-> L1 T0-T11 CURRENT LATENCY MAP
-> L2 FAILURE-CLASS LATENCY MATRIX
-> L3 SIGNAL RESPONSIBILITY MODEL
-> L4 TEST ROLE MATRIX
-> L5 PROVED ROOT LATENCY CONTRIBUTORS
-> L6 SAFE OPTIMIZATION REGISTER
-> L7 PROBLEM-TO-PATTERN COMMERCIAL COMPARISON
-> L8 CANDIDATE ARCHITECTURES (NO WINNER)
-> L9 POLYGON TOURNAMENT
-> L10 SCALE / PROBE ECONOMY / PARALLELISM TOURNAMENT
-> PHASE E ARCHITECTURE DECISION
-> L11 PHASE H MINIMAL IMPLEMENTATION, IF ADMITTED
-> L12 BEFORE / AFTER / CLIENT-RECOVERY PROOF
```

Phase A/B retain their Atlas and health-semantics obligations; Phase C is the
L7 problem-to-pattern consumer; Phase D forms L8 candidates; Phase F/G provide
the L9/L10 tournaments; Phase E makes the architecture decision only after
those tournament outputs; and Phase H is L11. This mapping preserves current
section owners and the existing Mission identity while making the causal order
unambiguous. The current CPS may still have an already-admitted Phase F/G
controlled residual; this Program text does not cancel, advance or replace it.

Forbidden:

```text
PRESELECT IMPLEMENTATION -> IMPLEMENT -> USE BENCHMARK AS POST-HOC CONFIRMATION
```

Required:

```text
UNDERSTAND CURRENT T0-T11 PATH -> IDENTIFY ROOT CAUSE
-> REGISTER SAFE OPTIONS -> MATCH PROVED PROBLEM TO PATTERN
-> FORM CANDIDATES -> POLYGON TOURNAMENT -> SCALE TOURNAMENT
-> CHOOSE -> IMPLEMENT -> BEFORE/AFTER -> MEASURE PRODUCTION EFFECT
```

The canonical macro-order for this track is therefore:

```text
CURRENT V7 FACTS (baseline done enough)
-> PROVEN BOTTLENECKS
-> STRONGEST-SYSTEM PATTERNS
-> V7 CANDIDATE ARCHITECTURES
-> POLYGON TOURNAMENT + SCALE TOURNAMENT
-> ARCHITECTURE DECISION
-> IMPLEMENTATION
-> T0->T11 BEFORE/AFTER
-> CONTROLLED/PRODUCTION PROOF
```

The historical Phase E result is an input to the candidate set. Phase E emits
the new architecture decision only after both tournament terminals are
consumed. Production exact-action-context, scope and Runtime evidence are a
later implementation/proof lane; a `STOP_SAFE` there must not block read-only
bottleneck synthesis, candidate construction or Polygon/scale tournament.
This reordering introduces no owner, Runtime, queue, registry, truth source,
cadence change or client movement.

### Historical evidence plan (A–G) — reclassified by N0–N11

This A–G sequence is retained as the provenance of already performed Atlas,
benchmark and Polygon work.  It is not an alternate current execution plan.
Where it names a successor, cadence, fast placement, C8 role, Full-Matrix role
or terminal that differs from N0–N11, the N amendment governs.  An A–G result
may be reused only after N0 records its exact disposition.

The following seven stages are the durable working plan for the existing
`V7_FAILURE_DETECTION_AND_RECOVERY_LATENCY_OPTIMIZATION` track. They make the
macro-order executable without creating seven Missions. Checks and reports are
evidence inside the current stage; they are not reasons to stop between every
microstep.

#### Stage A — unified baseline and provenance

Status: baseline is sufficient to begin Engineering synthesis; deploy-grade
provenance remains open.

Establish one table for CPS/OMP, Runtime snapshot and production version,
Matrix timer/service/caller, the last full Matrix cycle, the complete T0–T11
order, deployed selectors and the evidence class of every fact
(`PRODUCTION`, `POLYGON`, `STATIC` or `UNKNOWN`). This stage separates a real
Matrix bottleneck from a Runtime/provenance blocker. Polygon work may continue
in parallel, but implementation and production claims cannot start until the
relevant provenance gate is closed or one explicit external blocker is
recorded.

#### Stage B — mature-system synthesis and candidate formation

The existing Envoy, HAProxy, Google Cloud, FRR/BFD, Cisco, Fortinet and
MikroTik research is reused. Compare the same fields for active/passive
checks, fall/rise thresholds, cadence, degraded/recovering states, hysteresis,
freshness, quality, target readiness, route eligibility, history, probe budget,
scale and measurement/state/decision separation. For every proven V7
bottleneck record:

```text
mature mechanism -> reason -> existing V7 owner -> REUSE / ADAPT / REJECT
-> falsifiable Polygon measurement
```

The historical architecture results remain candidates. This stage forms
materially distinct A/B/C candidates and admits role-aware/adaptive behavior
only if measurements prove a gap that A–C cannot cover. It does not choose the
winner.

#### Stage C — complete ordinary-failure path in Polygon

Run the same governed path for every admitted candidate, first on one
synthetic client and then on bounded ordinary-like scope:

```text
CONTROLLED FAILURE/OUTAGE ONSET
-> L0/L1/L2 early signal
-> exact source
-> pre-ready exact eligible target
-> required service subset
-> bounded targeted Matrix confirmation
-> T0 failure confirmed
-> decision
-> Candidate -> Packet -> Lease -> Barrier -> Apply
-> failure-class-specific route/service verification
-> S11 server-side recovery verified

full-Matrix comparison -> asynchronous equivalence/fallback evidence
client telemetry -> T11 only when independently present
```

Prove existing Planner source/target selection, ordinary versus
certification-only scope, stale/unknown/conflict fail-closed behavior,
short/full disagreement fallback, recovery/re-admission and mandatory
post-switch verification. Full Matrix comparison is not a synchronous
prerequisite for an unambiguous HARD/PATH, applicable Telegram or decisive
required-service action; disagreement still falls back safely. No route or
client movement is performed merely to manufacture an event.

#### Stage D — Polygon and scale tournament

Use one failure matrix and one result schema across candidates and scales:

| Scale | Required evidence |
| --- | --- |
| 7 egresses | current topology and full/short baseline |
| 50 egresses | working architecture boundary |
| 100 egresses | intermediate load boundary |
| 1,000 egresses | stress model and saturation limits |

Record controlled onset→S11, production observation→S11 and, only where an
independent client signal exists, T0→T11; also record full/short probe count,
detection and recovery time,
short/full agreement, false positives/negatives, stale/conflict behavior,
target readiness, CPU/RAM, writer locks, network pressure, timeout budget,
failure-domain isolation, complexity and safety. Cross-egress concurrency is
an experimental dimension, not an assumed fix; Phase G evidence already
rejects treating concurrency alone as an automatic optimization.

#### Stage E — post-tournament architecture decision and minimal implementation

Only after Stages B–D are consumed does Phase E choose one architecture and
record why each other candidate and mature pattern was rejected. The first
implementation residual may then be admitted:

```text
connect the existing exact service subset and exact egress selection
to the existing refresh-all fast source/target path
```

Implementation proceeds `current -> shadow -> controlled synthetic -> bounded
scope -> production-safe observation -> limited production application`, using
existing owners, full Matrix fallback, rollback and no Authority expansion.
Timers, thresholds and cadence are changed only when the tournament provides a
measured reason and an explicit safety/rollback proof.

#### Stage F — before/after S11 and independently observed T11 proof

Compare old and new with the same measurement method: controlled onset→S11,
production first-failed-observation→S11, Matrix detection, decision and
execution segments, probe count, short/full agreement, target readiness,
false-positive/false-negative rate, CPU/RAM/network, writer contention,
recovery correctness and rollback safety. Measure T11 client traffic recovery
only when independent client telemetry exists. Green tests alone are
insufficient; a Polygon-only improvement remains an Engineering result until
a lawful production observation proves otherwise.

#### Stage G — production evidence and Mission closure

Use only an existing natural ordinary failure if one occurs, or read-only
production observation combined with controlled evidence. Never manufacture a
production failure for a number. Close the Mission only when required S11
before/after, short/full equivalence, target readiness, server-side recovery,
fallback preservation, residual classification and CPS/OMP consumption are all
proven, with an exact successor or lawful terminal. T11 remains a separately
classified client-agent residual when independent telemetry is absent.

Current position in this plan: **Stages A–D are consumed as Engineering
evidence; Stage E post-tournament architecture decision is consumed**.
Its durable output is
`docs/reports/engineering/2026-08-21_100109_v5_3_bottleneck_to_mature_pattern_synthesis.md`.
The Stage C and D outputs are
`docs/reports/engineering/2026-08-21_101349_v5_3_stage_c_candidate_failure_matrix_polygon.md`
and
`docs/reports/engineering/2026-08-21_101600_v5_3_stage_d_polygon_scale_tournament.md`.
Stage E selected
`TARGET_ARCHITECTURE_MODEL_B_PLUS_C_POST_TOURNAMENT_REVALIDATED`; its decision
record is
`docs/reports/engineering/2026-08-21_102100_v5_3_post_tournament_architecture_decision.md`.
Stage F consumed the controlled before/after delta; its record is
`docs/reports/engineering/2026-08-21_102900_v5_3_stage_f_before_after_t0_t11_proof.md`.
Stage G reached its lawful production boundary; its record is
`docs/reports/engineering/2026-08-21_103000_v5_3_stage_g_production_boundary_and_closure.md`.
The selected architecture then passed the bounded causal-latency revalidation
in `docs/reports/engineering/2026-08-21_142954_v5_3_stage_e_latency_causal_revalidation.md`
with terminal `B_PLUS_C_LATENCY_CAUSAL_PROOF_PASS`. That terminal proves the
timing/safety conditions in the deterministic Polygon model only; it does not
enable the automatic FAST consumer or grant production maturity. Production
T0→T11 closure remains `STOP_SAFE` until a natural ordinary failure or a
coherent exact Runtime/action context exists. Controlled gain must remain
separate from production gain, and no client may be moved artificially. This
ordering keeps the work on the switching-time objective and prevents a
historical architecture decision from becoming confirmation bias.
The subsequent fast-signal coverage blocks are recorded in
`docs/reports/engineering/2026-08-21_144720_v5_3_fast_signal_coverage_owner_backed_partial.md`
and
`docs/reports/engineering/2026-08-21_152459_v5_3_nontelegram_trigger_revalidation_partial.md`,
with the owner-side shadow-trigger implementation in
`docs/reports/engineering/2026-08-21_154245_v5_3_service_path_shadow_trigger_implementation_partial.md`
and the current-source producer implementation in
`docs/reports/engineering/2026-08-21_162430_v5_3_current_source_suspicion_producer_partial.md`.
The follow-up profile/service and DNS bounded implementation block is recorded
in `docs/reports/engineering/2026-08-21_164300_v5_3_profile_service_dns_fast_suspicion_implementation_partial.md`.
The consolidated producer implementation is recorded in
`docs/reports/engineering/2026-08-21_171700_v5_3_profile_service_dns_suspicion_producers_consolidated.md`.
The latest terminal is
`ACTION_RELEVANT_FAST_SIGNAL_COVERAGE_PARTIAL_WITH_EXACT_RESIDUAL`: Telegram and hard
local channel/process failures have an existing bounded shadow signal through
the Telegram sentinel or `v7-egress-diagnose` -> `v7-health` -> existing
`v7-users-autoswitch`. The existing Matrix owner now also has a guarded,
observation-only exact-source/exact-subset shadow-trigger contract, and
`v7-egress-diagnose` can produce a bounded current-source suspicion for
`TUNNEL_UP_INTERNET_DEAD`. The same existing Matrix owner now resolves a
profile identity from `service-preferences.json` into an exact service subset.
The existing `v7-egress-diagnose` owner now provides bounded profile-service
and DNS-specific suspicion producers for required-service, other-profile,
partial-censorship and multi-service failures, with repeated evidence,
unknown-state STOP_SAFE and duplicate cooldown. Production FAST admission,
fresh Runtime proof and T0-T11 client recovery evidence remain pending. Quality and recovery remain
separate non-FAST groups. This reclassification does not admit FAST, change
cadence, or alter routes.
This reclassification does not admit FAST, change cadence, or alter routes.

The next bounded pre-deploy validation is recorded in
`docs/reports/engineering/2026-08-21_183000_v5_3_fast_producer_scale_and_failure_to_t0_causal_validation.md`.
It corrected producer scope to active user-serving source plus distinct exact
service contract, eliminating O(users) probing and proving that the former
1,000-row `131.709 s` result combined broad synthetic scope with serial
execution. Its terminal is `PRE_DEPLOY_FAST_OPTIMIZATION_REQUIRED`: a genuinely
1,000-active distinct-contract cohort still requires `80.357 s`, exceeding the
30-second decision deadline, and the normal health lifecycle retains its serial
broad diagnostic tail. The same validation established that two producer
observations plus Matrix's existing universal 180-second persistence duplicate
failure-confirmation latency; the owner-backed alternative remains a
controlled-observation candidate only, with recovery and canonical production
defaults unchanged. The exact next stage is an existing-owner bounded active
cohort execution design and 7/50/100/1000 Polygon tournament. No controlled
deploy or automatic FAST admission is permitted before that terminal passes.

That tournament is recorded in
`docs/reports/engineering/2026-08-21_210000_v5_3_bounded_fast_active_cohort_execution_tournament.md`.
It implemented controlled C8 probe execution inside existing owners: an
ephemeral active-source/exact-service work set, at most eight read-only probes,
streamed per-contract completion, and serialized existing Matrix consequences.
C8 is the smallest tested cap passing a one-pass 1,000-active-contract result
(`29.436 s`, per-contract p95 `27.568 s`); C4/C2/C1 require
`34.618/56.792/70.932 s`. This does not admit production FAST. The exact
terminal is `PREDEPLOY_FAST_OPTIMIZATION_REQUIRED_WITH_EXACT_RESIDUAL` because
the existing health service performs all work and its legacy tail before the
next 30-second sleep: it does not yet prove timely second producer observation
or Failure->T0. The next bounded step is safe existing-owner FAST-phase
publication and next-phase deadline isolation; it may not create a background
orphan, second state surface, timer, queue or owner.

That deadline-isolation implementation is recorded in
`docs/reports/engineering/2026-08-22_001400_v5_3_health_fast_phase_deadline_isolation.md`.
The existing health owner now has a single foreground monotonic-deadline loop:
FAST runs first, while history/stability/load/state work receives only the
remaining phase budget and is synchronously deferred if it would cross the
next deadline.  There is no new scheduler, timer, owner, queue, writer or
state surface; C8 remains controlled-only and Full fallback, Matrix writer
serialization, production persistence and conservative recovery are unchanged.
The source/Polygon lifecycle tests pass.  The accepted three-phase C8 result
is recorded in
`docs/reports/engineering/2026-08-22_004129_v5_3_c8_three_phase_deadline_polygon.md`:
all 1,000-contract phases completed in `19.441/22.324/22.030 s`, below the
30-second deadline, with `max_inflight=8`, no receiver invocation and no
retained process.  The one minimal hot-path repair precomputes the existing
per-profile state key during canonical input parsing; no decision or ownership
boundary changed.  The exact remaining evidence is now the existing controlled
`two fresh same-scope failures -> Matrix -> T0 -> T11` synthetic fixture.
Automatic FAST, deploy and ordinary-client movement remain held until that
boundary is proven.

The subsequent controlled-path and deployment-gate revalidation is recorded in
`docs/reports/engineering/2026-08-22_005023_v5_3_controlled_path_revalidation_and_deploy_gate.md`.
It reconfirms the existing synthetic governed chain, Matrix subset/full
equivalence, two-sample producer-to-Matrix writing and safe executor boundary.
It also reconciles the three CPS generation projections.  The remaining
deployment gate is not an engineering inference: the verified local commits
are not yet published and the Runtime reports an older deployed commit.  No
deploy is admissible until that external version boundary converges.

The subsequent physical controlled-observability block is recorded in
`docs/reports/engineering/2026-08-22_102300_v5_3_controlled_matrix_observability_and_recovery_pool_boundary.md`.
It repaired one existing Matrix-owner gap: a full refresh now includes a
disabled interface only when the existing registry has already classified it
as a controlled-certification source.  A real controlled source failure was
therefore written to fresh Matrix state and safely classified as
certification-only; it caused zero ordinary-user movement and was restored.
The block also proved that the presently available recovery pool cannot supply
the one-user physical T0→T11 sample on the initially selected execution-only
source: it contains five certification users and its candidate reserve drafts
duplicate an unhealthy legacy channel.  A follow-up VLESS reuse audit corrects
the remaining path: VLESS is a real failed source with certification-only
users and zero ordinary users.  The next repair is internal to existing
owners, not a wait for another profile: bind one certification identity to
the current canonical VLESS failure and allow one existing-policy-fenced,
fresh `DEGRADED_USABLE` reserve.  It must preserve zero ordinary-user effect,
full Matrix fallback and the FAST hold.  Polygon and existing Stage A–F
evidence continue independently.

The VLESS selection repair is now implemented and tested: it accepts only a
fresh exact certification-only Matrix event whose compact certification scope
matches the current registry and whose source still has zero ordinary users.
It consumes the existing stage-1 shared-target allocation and standing-policy
semantic gate rather than selecting a target manually; stale, mixed or policy
mismatched state remains STOP_SAFE.  This completes the source/target
selection substep.  The next bounded frontier is not a generic availability
benchmark: its healthy-source reset would return a client to failed VLESS.
Extend the existing Packet/lease/verification consumer only for a one-way
synthetic VLESS recovery, retain the identity on the verified reserve, then
measure and observe the real recovery path before any later reset.

#### V5.3 Runtime shadow deployment and controlled closure -- superseding residual

The deployment boundary subsequently converged through the existing safe deploy
owner.  The result is recorded in
`docs/reports/engineering/2026-08-22_012000_v5_3_runtime_shadow_deploy_and_controlled_closure.md`.
The existing foreground health owner is deployed and has two consecutive
successful observation-only FAST phases (`9.588 s`, `9.951 s`) at a
30-second start-to-start cadence, without deadline miss.  A stale runtime
`v7-egress-diagnose` binary was the only deployment defect; the minimal repair
added that already existing executable to the safe-deploy manifest, then
published and deployed commit `e73aa888149b7cbb76701880bf4efc87e07dc510`.

The existing controlled Matrix/full-subset, producer-to-Matrix and synthetic
governed T0-T11 suites then passed (`139` tests).  Therefore the controlled
`two same-scope failures -> Matrix -> T0 -> T11` engineering obligation is
consumed.  FAST remains observation-only; Full Matrix remains canonical
fallback; the Matrix planner is capture-only; no ordinary customer, route,
Candidate, Packet, lease or execution record changed.  A future natural
ordinary production comparison is an external observation lane, not an open
engineering action and never permission to manufacture a move.

#### V5.3 real controlled-path re-entry: source-readiness correction

The evidence above closes the synthetic controlled obligation, but it does not
make an unhealthy or shared production channel a lawful substitute for the
next real controlled observation. The durable plan continues in this order:

```text
1. existing exact certification identity + healthy isolated source/target
   -> canonical controlled T0 (two FAST observations and Matrix)
2. governed one-user Apply, route/traffic T11 and rollback proof
3. real controlled Full-versus-FAST before/after
4. progressive certification cohorts only after the one-user result
5. remove only a proven redundant synchronous wait for exactly admitted classes
6. bounded ordinary rollout only after the prior gates
7. scale/storm/recovery/restart certification
8. canonical cleanup and Mission closure
```

This is an execution sequence inside the existing V5.3 track, not eight new
Missions or a replacement of CPS/OMP. CPS remains the volatile authority for
whether a particular execution is admitted. Existing Polygon comparison and
scale evidence can continue independently, but it may not be relabelled as a
real client-recovery result.

Current source-readiness evidence is recorded in
`docs/reports/engineering/2026-08-22_095500_v5_3_controlled_source_readiness_and_polygon_revalidation.md`.
It proves that Matrix is fresh and the empty legacy dedicated source is
unhealthy (`0/14` observation-only checks passed; stale handshake diagnosis).
The only ready-looking replacement draft is rejected by the existing native
admin owner as a duplicate of that source. The request to prepare one exact
dedicated source is Authority-approved, but it is not consumable until an
owner-verified **independent healthy egress profile/peer** exists. No ordinary
client, route, channel enablement, Matrix write, Candidate, Packet, lease or
Apply was performed. This is an exact source-substrate blocker, not permission
to weaken the one-user isolation or Full-Matrix fallback laws.

`WORKSTREAM_COMPACTNESS_LAW`: these phases are the complete logical structure.
Do not add a phase, tracker, matrix document, status ledger or report series
when an existing phase/report can preserve the decision, owner, consumer,
evidence and re-entry condition. One admitted Mission produces one compact
Engineering Report; intermediate microsteps remain evidence inside it.

### V5.3 historical Health/Test/Stability revalidation inputs

This section supplies evidence requirements and owner boundaries to N0 and
later N phases.  It does not create a parallel execution sequence or preserve
any older C8/Full-Matrix role that conflicts with the current N amendment.

The consumed 2026-08-20 Phase C/D/E result remains historical valid evidence,
but its architecture disposition is now:

```text
PROVISIONAL_ARCHITECTURE_DECISION_REQUIRES_SYSTEM_LEVEL_HEALTH_TEST_STABILITY_REVALIDATION_BEFORE_AUTOMATIC_FAST_CONSUMER_ENABLEMENT
```

Terminal-precedence law:

```text
V7_MATRIX_HEALTH_TARGET_ARCHITECTURE_DECIDED
= PHASE_E_INTERNAL_ARCHITECTURE_DECISION

PHASE_E_DECISION
-> SYSTEM_LEVEL_EVIDENCE_WEIGHTED_REVALIDATION
-> AUTOMATIC_CONSUMER_ELIGIBILITY

AUTOMATIC_FAST_CONSUMER_ELIGIBILITY
REQUIRES
V7_HEALTH_TEST_STABILITY_TARGET_ARCHITECTURE_EVIDENCE_WEIGHTED_DECISION_CONSUMED
```

`V7_MATRIX_HEALTH_TARGET_ARCHITECTURE_DECIDED` may remain an input to Phase
F/G/H analysis, but is neither a Runtime-admission terminal nor sufficient
authority for automatic FAST consumer enablement. Invariant:

```text
OLD_OR_PROVISIONAL_PHASE_E_TERMINAL_MUST_NOT_UNLOCK_RUNTIME_CONSUMER_AFTER_SYSTEM_LEVEL_GATE_EXISTS
```

Its commercial comparison is `INITIAL_MECHANISM_PATTERN_BENCHMARK`, not the
complete field-by-field basis for detailed Health/Test/Stability architecture.
The already deployed exact `--egresses` / `--services` selectors remain a
safe inert/opt-in primitive and the empty-selector full Matrix behavior remains
the fallback. No automatic role-aware source/target caller, production FAST
schedule, new cadence or threshold is admitted by the previous decision.

Compatibility and hold rule:

```text
EXISTING_FAST_SUBSET_PRIMITIVE = KEEP_DEPLOYED_OPT_IN
AUTOMATIC_FAST_ROLE_CONSUMER = HOLD_PENDING_SYSTEM_LEVEL_REVALIDATION
```

Before any automatic FAST consumer enablement, the existing V5.3/OMP lifecycle
must consume the bounded Engineering output
`V7_COMPLETE_HEALTH_TEST_STABILITY_SYSTEM_ATLAS`. This is an analysis output,
not a new owner, store, Program, Mission, Runtime or source of truth. It must
discover all real mechanisms by producer -> state -> consumer -> behavior,
including but not limited to Matrix probes, Telegram sentinel, transport/
interface/proxy and path-sanity checks, desired-state checks, current/5m/1h
stability projections or equivalents, quality/benchmark latency-loss-jitter,
capacity/reserve, passive failures/timeouts, incident persistence, anti-flap,
cooldown, recovery/re-admission, target readiness, kernel/route verification,
selected-user and post-switch verification, and path guard/recovery checks.

Every discovered mechanism has one evidence record with these fields:

```text
MECHANISM_ID; OWNER; PRODUCER; INPUT; OUTPUT; WHAT_IT_PROVES;
WHAT_IT_DOES_NOT_PROVE; SOURCE_TARGET_BOTH_OR_POST_SWITCH; TRIGGER; CADENCE;
TIMEOUT; RETRY; PERSISTENCE; FAILURE_THRESHOLD; RECOVERY_THRESHOLD;
SERIAL_OR_PARALLEL; PARALLEL_WITH_WHAT; LOCKS; NETWORK_COST; CPU_COST;
WALL_COST; CURRENT_STATE_SURFACE; HISTORY_DEPENDENCY; FRESHNESS_RULE;
DOWNSTREAM_CONSUMER; EXACT_DECISION_INFLUENCE; CAN_BLOCK_FAILOVER;
CAN_BLOCK_TARGET_ADMISSION; CAN_BLOCK_RECOVERY; FALSE_POSITIVE_RISK;
FALSE_NEGATIVE_RISK; DUPLICATES_OTHER_MECHANISM;
FAST_PRECOMPUTED_DEEP_OR_ENGINEERING; REUSE_ADAPT_BACKGROUND_OR_REJECT;
WRONG_DECISION_IF_REMOVED_FROM_SYNCHRONOUS_PATH
```

If the final field cannot name an exact wrong V7 decision, the mechanism is
not automatically a synchronous hot-path requirement.

The same gate must prove the actual decision-influence graph:

```text
TEST / SIGNAL -> CURRENT STATE -> CONSUMER -> DECISION EFFECT
```

Every edge is classified `REQUIRED`, `OPTIONAL`, `ADVISORY` or
`DEFERRED_BACKGROUND`; distinct meanings must not collapse into a generic
`healthy=true/false`. Required output:
`CURRENT_V7_HEALTH_DECISION_INFLUENCE_GRAPH_PROVEN`.

It must also prove current execution-order and latency maps for hard source
failure, partial service failure, target preparation and recovery/re-entry:
first observer, suspicion, confirmation, canonical event, target readiness,
switch eligibility and post-switch verification. Each interval names owner,
cadence, timeout, retry, serial/parallel work, persistence wait, current or
historical read and blocking status. It explicitly identifies `SERIAL_WAIT`,
`REDUNDANT_RECHECK`, `DUPLICATE_SIGNAL`, `SAME_FACT_DIFFERENT_OWNER`,
`FULL_DEEP_CHECK_BEFORE_SIMPLE_DECISION`, `UNNECESSARY_HISTORY_READ`,
`CADENCE_DOMINATES_LATENCY` and `TIMEOUT_DOMINATES_LATENCY`. Required output:
`CURRENT_HEALTH_TEST_EXECUTION_ORDER_AND_LATENCY_GRAPH_PROVEN`.

Cadence review is per mechanism and per role/state: healthy, degraded, failed,
recovering, hot target and cold target. It distinguishes periodic from
event-driven observation and measures normal, suspicion-confirmation, down and
recovery cadence. Each cadence receives `KEEP`, `ADAPT`,
`MEASURE_BEFORE_DECISION`, `BACKGROUND_ONLY` or
`REMOVE_DUPLICATE_CADENCE` with an owner-backed measurable reason; vendor
defaults are never copied as V7 settings.

For every decision-critical mechanism:

```text
DECISION_CRITICAL_CADENCE_TIMEOUT_RETRY_PERSISTENCE_AND_SERIAL_WAIT
MUST_USE_OBSERVED_OR_CONTROLLED_MEASUREMENT_WHERE_EXECUTABLE
NOT_SOURCE_CODE_DEFAULTS_ALONE
```

Static configuration/source inspection is discovery and intended-behavior
evidence only, except when an executable measurement substrate is unavailable.
The Atlas and timing map then record `CONFIGURED_CADENCE`, `OBSERVED_CADENCE`,
`CONFIGURED_TIMEOUT`, `OBSERVED_ATTEMPT_TIME`, `RETRY_COUNT`,
`PERSISTENCE_WAIT`, `LOCK_WAIT`, `SERIAL_PREDECESSOR_WAIT`, `CONSUMER_DELAY`
and `EFFECTIVE_DECISION_CONTRIBUTION`, classifying each as
`OBSERVED_CONFIRMED`, `CONTROLLED_MEASURED`, `STATIC_ONLY_EXACT_BLOCKER` or
`NOT_DECISION_CRITICAL`. A static-only blocker names its unavailable substrate
and exact re-entry condition. `SOURCE_CODE_SAYS_FAST -> HOT_PATH_FAST` is
forbidden without safe executable observation or controlled measurement.

Parallelism review distinguishes `PARALLEL_OBSERVATION`, `PARALLEL_PROBING`,
`SERIAL_STATE_COMMIT` and `SERIAL_DECISION`. Causality, locks, shared network
resources, external endpoint pressure, writer constraints and correlated
failure domains decide whether work may run concurrently. Required output:
`HEALTH_TEST_DEPENDENCY_AND_PARALLELISM_MODEL_DECIDED`.

Temporal evidence must remain separated as `IMMEDIATE_HEALTH`, `PERSISTENCE`,
`RECENT_STABILITY`, `RECOVERY_PROBATION`, `MEDIUM_TERM_QUALITY`,
`LONG_TERM_RELIABILITY` and `ENGINEERING_HISTORY`, with producer, store,
consumer and exact source-failover/target-admission/ranking influence. Invariant:

```text
FAST_PATH_MUST_CONSUME_COMPACT_CURRENT_STABILITY_FACTS
AND MUST_NOT_SYNCHRONOUSLY_RECONSTRUCT_STABILITY_FROM_RAW_HISTORY
```

The gate produces four separate fail-closed decision contracts with mandatory
and optional evidence, cadence, freshness, thresholds, stability influence and
timeout budget: `SOURCE_FAILURE_CONTRACT`, `TARGET_READINESS_CONTRACT`,
`RECOVERY_READMISSION_CONTRACT` and `POST_SWITCH_RECOVERY_CONTRACT`. One
generic health verdict cannot satisfy all four without exact consumer proof.

The deeper commercial comparison reuses the existing official-source set:
Envoy, HAProxy, Google Cloud, FRRouting/BFD, Cisco BFD/IP SLA/Object Tracking,
FortiGate SD-WAN and MikroTik RouterOS; AWS remains conditional on an unresolved
mechanism class. Each relevant mechanism is compared field-by-field using the
Atlas fields plus active/passive state machine, hysteresis, degraded state,
recent history, quality, source/target difference, eligibility propagation,
parallelism, probe budget, scale and fail-closed behavior. Each row ends:

```text
COMMERCIAL MECHANISM -> CURRENT V7 EQUIVALENT
-> V7 BETTER / WORSE -> GAP -> REUSE / ADAPT / REJECT
-> MEASURABLE REASON
```

Atlas, decision graph, timing map and field comparison must produce at least
three concrete evidence-derived V7 candidate models when materially distinct
designs remain. Every candidate defines source, target, recovery and
post-switch tests; cadence/timeouts/parallelism/persistence; failure/recovery
thresholds; passive/stability/quality/capacity inputs; FAST/precomputed/DEEP
placement; expected detection latency and false-positive/false-negative risk;
probe cost at current, 50 and 1,000 egresses; complexity, owner reuse,
migration risk and full-Matrix fallback.

Architecture selection then uses the existing owner-backed decision method,
not a new scoring engine. Critical gates are failure-detection latency, false
failover, false healthy-target admission, recovery/flap safety and target
freshness. High-weight gates are probe cost, 50/1,000-egress scale, complexity,
existing-owner reuse and rollback/fallback; observability is medium. No critical
UNKNOWN may remain without a bounded revalidation plan, and material timing or
cadence assumptions must be measured or explicitly bounded. Required terminal:

```text
V7_HEALTH_TEST_STABILITY_TARGET_ARCHITECTURE_EVIDENCE_WEIGHTED_DECISION_CONSUMED
```

If the result confirms B+C, emit
`MODEL_B_PLUS_C_REVALIDATED_WITH_SYSTEM_LEVEL_EVIDENCE`. A refinement changes
only proven consumer/placement/cadence semantics compatible with existing
owners. Rejection does not itself remove the harmless opt-in selectors. Until
this terminal, production FAST scheduling, automatic role selection, new
cadence/thresholds, automatic source/target invocation and weakening/removal
of the full Matrix fallback are forbidden.

#### Phase A — existing capability and current-reality map

Phase A is the bounded system Atlas required by the revalidation gate, not a
new truth owner or unbounded archaeology audit. Reuse every still-valid
owner-backed result and inventory every current decision-relevant mechanism:
every probe, signal, state projection, service, protocol, egress role,
cadence, timeout,
retry, persistence/failure/recovery threshold, lock, writer, consumer, state
surface, event producer, passive signal and target-readiness input. Measure
per-probe, per-service, per-egress and full-cycle wall time, CPU, peak RSS and
network work where the existing owner can expose them.

Every check receives exactly one or more product roles:
`FAST_FAILURE_REQUIRED`, `TARGET_READINESS_REQUIRED`,
`ANTI_FLAP_CONFIRMATION`, `DEEP_HEALTH_DIAGNOSTIC`,
`QUALITY_PERFORMANCE`, `CAPACITY_PLANNING` or `ENGINEERING_ONLY`. Its record
must name the Runtime decision consumer, what breaks if it leaves the fast
path, and whether a cheaper existing signal proves the same required fact.
Probe duration alone is never a removal reason.
Phase A stops only when `V7_COMPLETE_HEALTH_TEST_STABILITY_SYSTEM_ATLAS`,
`CURRENT_V7_HEALTH_DECISION_INFLUENCE_GRAPH_PROVEN` and
`CURRENT_HEALTH_TEST_EXECUTION_ORDER_AND_LATENCY_GRAPH_PROVEN` are consumed.
Unrelated historical audits remain closed absent an exact invalidation.

#### Phase B — failure model

Classify at least tunnel/process death; interface-up Internet failure;
required application/service failure; DNS, route and proxy-transport failure;
partial censorship/service-specific failure; loss; excessive latency;
capacity exhaustion; reachable-but-unsuitable target; and stale, unknown or
conflicting evidence. Each class binds:

```text
FAILURE CLASS -> MINIMUM SIGNAL -> CONFIRMATION -> CANONICAL OWNER
-> PERSISTENCE -> STATE TRANSITION -> FAILOVER ELIGIBILITY -> RECOVERY RULE
```

Health must remain protocol/service-aware where the product consumes that
meaning. One generic HTTP success cannot replace a required transport,
application, DNS, route, capacity or suitability fact. Unknown, stale and
conflicting evidence remain fail-closed.
Phase B output is `V7_FAILURE_AND_HEALTH_SEMANTICS_BASELINE_CONSUMED`; it names
the exact existing owner and recovery rule for every material failure class.

#### Phase C — mature-system benchmark

Phase C is L7: it answers a proved V5.3 latency or safety problem with a
matching mature-system pattern. It must not begin as a generic search for the
best FAST model, and it must not repeat the consumed benchmark without a new
invalidator. This benchmark has two complementary layers and compares
mechanisms, not companies or product portfolios. Program text owns only
requirements, terminal and consumers; detailed source evidence and comparison
rows belong to one compact Engineering Report for the exact admitted Mission.
Vendor defaults are contextual evidence, never V7 settings. Only official
documentation, architecture/configuration/reference manuals and primary
technical papers qualify.

`LAYER_1_INFRASTRUCTURE_HEALTH_CONTROL_PATTERNS` requires:

- Envoy active health plus passive/outlier detection and endpoint eligibility;
- HAProxy fall/rise, transitional cadence and asymmetric failure/recovery;
- Google Cloud protocol-specific checks, healthy/unhealthy thresholds and
  endpoint eligibility;
- FRRouting/BFD lightweight fast liveness, detection multiplier and separation
  from full route/policy computation.

`LAYER_2_COMMERCIAL_ROUTING_SDWAN_MULTIWAN` requires:

- Cisco `BFD / IP SLA / Object Tracking / routing consumer`: measurement,
  current tracked state and route-consumer separation;
- Fortinet FortiGate SD-WAN Link Health Monitor / Performance SLA: active and
  passive WAN evidence, latency/jitter/loss, multiple checks, degraded/
  unusable state, member exclusion and recovery/re-entry;
- MikroTik RouterOS: ARP/ICMP/BFD gateway reachability, recursive next-hop
  monitoring, multi-WAN failover, route activation and the separation of
  gateway state from route selection.

AWS ELB/NLB is `CONDITIONAL_REFERENCE`: use it only when a named V7 residual
requires an additional target-health/failover comparison not already closed
by valid evidence. Juniper is not independently mandatory while Cisco plus
FRRouting/BFD cover the same mechanism class. Arista, Palo Alto, Ubiquiti and
other platforms are `BENCHMARK_NOT_REQUIRED_DUPLICATE_PATTERN` unless a named
unresolved V7 decision proves unique coverage.

Before new research, every reference receives exactly one disposition:

```text
RESULT_REUSED_VALID
| TARGETED_GAP_RESEARCH_REQUIRED
| BENCHMARK_NOT_REQUIRED_DUPLICATE_PATTERN
| SOURCE_UNAVAILABLE_EXACT_BLOCKER
```

Only `TARGETED_GAP_RESEARCH_REQUIRED` may create a later bounded research
residual through existing OMP admission. Existing current evidence already
covers the general Envoy, HAProxy, Google Cloud, AWS, FRRouting/BFD and Cisco
classes; a future Mission must revalidate source freshness and exact coverage
rather than repeat them ceremonially. This statement is a discovery baseline,
not completion evidence for the Phase C terminal.

The benchmark covers the whole lifecycle, not only Service Matrix probes:

```text
OBSERVATION -> SIGNAL -> FAILURE SUSPICION
-> CONFIRMATION / PERSISTENCE -> CURRENT HEALTH STATE
-> DEGRADED / UNUSABLE -> ROUTING/PATH ELIGIBILITY CHANGE
-> RECOVERY OBSERVATION -> RISE / HYSTERESIS / RE-ADMISSION

LONGER-TERM STABILITY / QUALITY / FAILURE HISTORY
-> COMPACT CURRENT PROJECTION
-> PLANNER / TARGET-READINESS / ENGINEERING CONSUMER
```

FAST Runtime consumes bounded current state and fingerprints. It must not
synchronously scan or reconstruct channel stability from raw history; existing
DEEP/background persistence, incident, quality and history owners may derive
the compact projection.

Mandatory logical evidence classes are classification only, not new systems:

1. `TRANSPORT_PATH_HEALTH` — tunnel/interface/proxy/gateway/path liveness;
2. `SERVICE_APPLICATION_HEALTH` — required service reachability;
3. `PASSIVE_RUNTIME_SIGNAL` — legally consumable real errors/timeouts/outliers;
4. `TEMPORAL_STABILITY` — persistence, recent instability, flap/recovery state
   and compact history projection;
5. `TARGET_SUITABILITY` — health, freshness, quality, capacity, policy,
   reserve and role.

`SOURCE_HEALTH_NOT_EQUAL_TARGET_READINESS` is mandatory. Active-source
evidence answers whether affected users require rescue; eligible/hot-target
evidence answers whether that target can safely receive them now. The
benchmark must distinguish failed, degraded-but-usable, recently recovered
and quality-acceptable-but-unstable paths and must not impose identical
cadence/depth on source and target roles.

Every material mechanism is recorded compactly as:

```text
PLATFORM; MECHANISM; PROBLEM_SOLVED; SIGNAL_TYPE; ACTIVE_OR_PASSIVE;
STATE_MODEL; FAILURE_CONFIRMATION; RECOVERY_CONFIRMATION; CADENCE_MODEL;
QUALITY_SIGNALS; TARGET_OR_PATH_ELIGIBILITY_EFFECT; ROUTING_CONSUMER;
HISTORY_OR_STABILITY_USAGE; SCALE_MODEL; WHAT_V7_ALREADY_HAS;
V7_EXISTING_OWNER; REUSE_OR_ADAPT_OR_REJECT;
MEASURED_OR_ARCHITECTURAL_REASON; TARGET_ARCHITECTURE_CONSEQUENCE;
INVALIDATION_TRIGGER
```

The final comparison matrix covers fast liveness, service validation, passive
failure evidence, failure/recovery confirmation, degraded state, hysteresis,
temporal stability, target readiness, latency/jitter/loss, gateway/path
reachability, route-eligibility propagation, active/standby differentiation,
adaptive cadence, probe economy, bounded parallelism and scale behavior.

`REUSE` requires an existing owner and consumer that already close the
semantics. `ADAPT` requires a proven V7 gap, existing owner, measurable
product/safety benefit, bounded implementation surface, no duplicate truth,
validation, safe fallback/rollback and invalidation trigger. `REJECT` names
duplicate pattern, absent measurable benefit, wrong responsibility boundary,
unnecessary complexity, incompatible safety/scale assumptions or an
unjustified new-owner/truth requirement. An interesting vendor feature is not
an implementation Candidate by itself.

Required consumer chain:

```text
PROVED V7 PROBLEM -> MATURE-SYSTEM MECHANISM -> V7 COMPARISON
-> REUSE / ADAPT / REJECT -> EXISTING OWNER
-> MEASURABLE HYPOTHESIS OR REJECTION REASON
-> PHASE D / E / F / H CONSUMPTION
-> IMPLEMENTATION ADMISSION ONLY IF A GAP IS PROVEN
```

`TARGET_ARCHITECTURE_CONSEQUENCE` must say whether the mechanism confirms the
current V7 approach, changes health semantics, FAST/DEEP placement,
source/target cadence, stability/recovery treatment or path-eligibility
propagation, or is rejected as unnecessary complexity. Phase C output must be
consumed by Phase D and Phase E before the target architecture is selected;
descriptive vendor coverage alone cannot reach the Phase C terminal.

Phase C terminal (the L7 `PROBLEM_TO_PATTERN_MAPPING` must be attached):

```text
MATURE_HEALTH_AND_COMMERCIAL_ROUTING_MECHANISM_COMPARISON_CONSUMED
```

It requires mandatory reference and mechanism-class coverage, one disposition
for every material row, existing owner, measurable hypothesis or rejection
reason, preserved evidence/source/target semantics, acknowledgement by every
applicable Phase D/E/F/H consumer, closed duplicate-pattern research, no new
owner/truth/Runtime and one exact successor or legal terminal. No separate
vendor report series, new tracker or ceremonial organization count is allowed.
A benchmark cannot create Authority, Model D or a second health system.

The consumed 2026-08-20 comparison is retained as
`INITIAL_MECHANISM_PATTERN_BENCHMARK`. The revalidation terminal additionally
requires the field-by-field comparison contract defined above; paragraph-level
vendor summaries alone cannot select detailed architecture.

#### Phase D — role-aware health model

Phase D synthesizes Phase A current reality, Phase B failure semantics and the
consumed Phase C mechanism decisions; it is not designed from current code
alone. Produce one candidate V7 health model and prove or reject differentiated
work for `ACTIVE_SOURCE`, `ELIGIBLE_HOT_TARGET`,
`COLD_UNUSED_TARGET`, `DEGRADED`, `UNUSABLE`, `RECOVERING` and
`ENGINEERING_CERTIFICATION_ONLY`. Frequent lightweight source usability,
bounded hot-target readiness, slower cold/deep checks, accelerated degradation
confirmation and conservative recovery admission are hypotheses until
measured against existing owner, anti-flap, freshness and consumer contracts.

Phase D must derive and compare materially distinct concrete candidates rather
than immediately returning to Model B. Each candidate must map `TRANSPORT_PATH_HEALTH`,
`SERVICE_APPLICATION_HEALTH`, `PASSIVE_RUNTIME_SIGNAL`,
`TEMPORAL_STABILITY` and `TARGET_SUITABILITY` and state which facts are
synchronous FAST, precomputed/current projections, DEEP/background or
Engineering/Learning only. It must state source/target differences, which
stability history affects immediate admission and the asymmetric failure/
recovery contract. Output:
`V7_ROLE_AND_STABILITY_HEALTH_MODEL_CANDIDATE_CONSUMED_BY_PHASE_E`.

#### Phase E — target architecture decision (after tournaments)

The 2026-08-20 Phase E result is historical input to the candidate set, not a
preselected winner. The system-level Phase E revalidation is the final weighted
architecture-selection gate. It consumes the terminals of Phase A, B, C and D
**plus** the L9 Polygon tournament and L10 scale tournament, then compares at
least:

1. `MODEL_A_CURRENT_IMPROVED_FULL_MATRIX`;
2. `MODEL_B_FAST_PLUS_DEEP_UNDER_EXISTING_MATRIX_OWNER`;
3. `MODEL_C_EXISTING_SIGNAL_ESCALATION_THROUGH_MATRIX_OWNER`.

Model C may be merged into B; it may not become a second event system. A Model
D is eligible only when measured evidence proves A-C insufficient and it adds
no health truth or Runtime ecosystem. Phase E emits exactly one decision:

```text
TARGET_ARCHITECTURE_MODEL_A
| TARGET_ARCHITECTURE_MODEL_B
| TARGET_ARCHITECTURE_MODEL_B_PLUS_C
| TARGET_ARCHITECTURE_REFINED_EXISTING_OWNER_VARIANT
| TARGET_ARCHITECTURE_MODEL_B_PLUS_C_POST_TOURNAMENT_REVALIDATED
| MODEL_D_REQUIRES_MEASURED_GAP_ADMISSION
```

If Model B wins, Phase E records why using the V7 measurements and Phase C
commercial evidence. A refinement records its exact delta from the original
Model B; every rejected candidate and vendor mechanism records why it is
unsuitable. The required terminal is
`V7_MATRIX_HEALTH_TARGET_ARCHITECTURE_DECIDED`. No architecture-committing
Runtime implementation Mission may start before that post-tournament Phase-E
terminal is consumed. Automatic FAST consumer eligibility additionally
requires the dominant system-level weighted terminal above. The standing
hypothesis remains:

```text
existing protocol-specific/passive signal
-> bounded fast confirmation
-> existing Matrix canonical state/failure episode
-> current affected scope
-> existing decision/execution path

deep Matrix -> diagnostics, broad services, quality, capacity detail,
               Learning and Engineering evidence
```

#### Stage E latency-causal revalidation terminal

The provisional B+C selection is consumed only after a same-matrix virtual-clock
check separates the three clocks `FAILURE/FIRST OBSERVABLE -> T0`, `T0 -> T11`
and `FAILURE -> T11`. The accepted terminal is:

```text
B_PLUS_C_LATENCY_CAUSAL_PROOF_PASS
```

The terminal is conditional on fresh, generation-coherent passive or
bounded-fast evidence; a sufficient bounded subset for the failure role;
current target readiness and policy; and an unchanged governed recovery path.
Full DEEP remains asynchronous, fallback or mandatory for ambiguous roles.
Partial degradation, stale/unknown/conflicting evidence, target unavailability
and policy/capacity denial remain `STOP_SAFE`. Required-service failures without
a passive signal retain the configured cadence and gain only the post-T0
barrier reduction.

The `50%` timing threshold and three-sample fast confirmation used in this gate
are Engineering rule-change candidates, not production settings. Any
implementation must first pass shadow and controlled Polygon execution in the
existing Matrix owners, then be separately admitted by Phase H. Until that
admission, `V5_3_AUTOMATIC_FAST_CONSUMER_STATUS` remains held and Full Matrix
remains the live baseline.

#### Stage E residual — historical fast-signal coverage terminal

The next bounded residual consumed the frozen 16-class failure inventory and
revalidated the real caller/owner/consumer path. Its consolidated report is
`docs/reports/engineering/2026-08-21_144720_v5_3_fast_signal_coverage_owner_backed_partial.md`.
Its terminal is:

```text
FAST_SIGNAL_COVERAGE_PARTIAL
```

The existing Telegram sentinel path and the hard local diagnose path are
owner-backed and bounded in shadow. Generic application/service, DNS,
Internet-behind-tunnel, quality and clean-recovery failures without a passive
signal still enter through the ordinary Matrix cadence; the exact service
subset and persistence primitives are now exposed through a guarded
observation-only exact-source/exact-subset contract in the existing Matrix
owner. A current-source producer now covers the tunnel-up/Internet-dead
suspicion class in shadow; required-service, DNS, partial-censorship and
multi-service classes remain the bounded residual. This is not a new generic
audit. No production cadence, threshold, route or automatic FAST consumer is
admitted by this terminal.

#### Current bounded producer implementation — superseding residual

The consolidated implementation report is
`docs/reports/engineering/2026-08-21_171700_v5_3_profile_service_dns_suspicion_producers_consolidated.md`.
The existing `v7-egress-diagnose` owner now provides profile-service and
DNS-specific suspicion producers for the five former residual classes. They
use active `users.registry` assignments, canonical profile services,
repeated-evidence gates, unknown-state STOP_SAFE, stable trigger IDs and
cooldown, then call the existing profile-aware Matrix shadow receiver. The
current terminal is
`ACTION_RELEVANT_FAST_SIGNAL_COVERAGE_PARTIAL_WITH_EXACT_RESIDUAL` because
production deploy/revalidation, automatic FAST admission and real T0→T11
client-recovery evidence remain separate gates.

#### Phase F — Polygon and scale tournament input

The previous `TARGET_ARCHITECTURE_MODEL_B_PLUS_C` and
`TARGET_ARCHITECTURE_REFINED_EXISTING_OWNER_VARIANT` results are candidate
baselines only. FAST and DEEP remain modes of the existing Matrix owner;
passive evidence only escalates bounded confirmation. The exact first
implementation residual remains historical evidence in
`docs/reports/engineering/2026-08-20_130000_v5_3_matrix_health_phase_c_d_e_decision.md`,
not implementation authority.

Phase F runs the pre-decision tournament. For every admitted candidate publish
measured `FAST_DETECTION_COST`, `HEALTH_PROBE_COST_PER_EGRESS`,
`TARGET_READINESS_COST`, `DEEP_MATRIX_COST`, `TOTAL_NETWORK_PROBE_BUDGET`,
expected detection delay, worst-case timeout budget, complexity and safety.
Use the same failure matrix for every candidate. Validate the current
approximately seven-egress topology, model 50 egresses, use 100 where it adds
an intermediate boundary, and stress-model 1,000 egresses. Cost scales by
egress role/action class, never users. Parallel processes alone do not prove
scalability; total probe volume and external service pressure remain bounded.
If scale, budget or safety evidence invalidates a candidate, record the exact
invalidator and exclude or refine that candidate before the Phase E decision;
do not silently redesign it.

#### Phase G — bounded egress parallelism in the tournament

Phase G measures each candidate's concurrency need and safety before the
architecture decision; it does not become an alternative architecture owner.
Evaluate serial cross-egress traversal only after the fast-subset result shows
it remains a material bottleneck. Compare concurrency caps `1`, `2`, `4` and
adaptive only through controlled measurement. Admission requires lock safety,
single-writer/atomic-write proof, CPU/RSS/network budgets, interface/SOCKS/
process isolation, external-service pressure and failure-domain analysis.
Existing bounded inner-service parallelism is reused and is not rewritten
without its own invalidation.
Any material contradiction records the exact invalidation trigger and returns
to the candidate/tournament lane before Phase E emits a decision.

#### Phase H — migration, validation and shrink

Phase H automatic-consumer work starts only after both
`V7_MATRIX_HEALTH_TARGET_ARCHITECTURE_DECIDED` and
`V7_HEALTH_TEST_STABILITY_TARGET_ARCHITECTURE_EVIDENCE_WEIGHTED_DECISION_CONSUMED`
and the relevant Phase F/G constraints are consumed. It is the implementation
contract, not an architecture-selection surface. For each admitted change
prove:

```text
CURRENT -> TARGET -> TRANSITION -> MODIFIED CONSUMERS -> VALIDATION
-> OLD SYNCHRONOUS WORK REMOVED OR DEFERRED -> RESIDUE CLOSED
```

Possible successors are fast active-source subset, bounded target-readiness
refresh, state-aware cadence, bounded cross-egress concurrency, passive-signal
escalation, deep-Matrix deferral/restructure, fault/scale validation and
production detection-latency measurement. None is mandatory merely because it
is listed. Physical removal follows real consumer proof and rollback remains
the current full-Matrix path until its exact replacement is proven.
Only after this plan names existing owners, consumer migration, validation,
fallback and residue may OMP admit the smallest bounded implementation Mission.

### V5.3 historical first-admission candidate

`V7_MATRIX_FAST_SOURCE_AND_TARGET_PROBE_ADMISSION_V1` is historical candidate
evidence.  It is neither the next action nor a standing admission path.  N0a
is the required first executable prerequisite; any later reuse of this
candidate must be recast as the relevant N phase and satisfy its SLO, resource,
automation and retirement contracts.

`V7_MATRIX_FAST_SOURCE_AND_TARGET_PROBE_ADMISSION_V1` is retained as the
leading first implementation candidate generated by previous evidence, not a
pre-decided executable architecture. It becomes admission-eligible only when:

```text
V7_MATRIX_HEALTH_TARGET_ARCHITECTURE_DECIDED
AND FIRST_IMPLEMENTATION_RESIDUAL_CONFIRMED
AND fresh CPS names the same exact Mission identity
```

The Mission has since deployed only the fail-closed exact selector primitive.
That completed portion is retained. Its automatic role-selection consumer
portion is `HOLD_PENDING_SYSTEM_LEVEL_REVALIDATION` and cannot rely on the old
Phase E terminal alone.

If those gates still select it, it must first discover and reuse the tester's
existing service-subset mechanism. It may admit an implementation only if
evidence proves a minimal protocol-appropriate subset for active ordinary
sources and eligible targets while preserving:

- the existing Matrix writer, lock, row/state schema and canonical event;
- existing persistence, anti-flap and conservative recovery semantics;
- stale/unknown/conflicting fail-closed behavior;
- source-scope, target/capacity and Planner ownership;
- the full Matrix fallback and deep diagnostic consumer;
- no `O(N users)` loop and no direct route apply from Matrix;
- before/after detection-segment timing and bounded rollback.

Its expected lifecycle is the standard OMP chain:

```text
DISCOVERY/BDP -> CANDIDATE ADMISSION -> CPS ATOMIC MISSION IDENTITY
-> MISSION_EXECUTION_ALLOWED -> IMPLEMENTATION -> VALIDATION
-> CONSUMER MIGRATION -> RESIDUE CHECK -> BEFORE/AFTER/DELTA
-> SAFE DEPLOY when applicable -> lawful observation -> REPORT
-> NEXT FRONTIER or exact legal terminal
```

`MISSION_ACCEPTED`, a report, a commit, tests or deploy do not imply
`MISSION_EXECUTION_ALLOWED`. Once that state is present, the existing OMP
execution-completion contract continues the bounded Mission through terminal
completion or one exact blocker without microstep prompts.

### V5.3 terminal definition

#### Historical terminal definition

This terminal list is retained as a broad evidence checklist.  The binding
completion contract is `MATRIX_ROLE_BASED_RECOVERY_OPTIMIZATION_TERMINAL_COMPLETE`
in the N amendment.  Where the lists differ, the N terminal prevails; in
particular, server facts can establish S11 but not client-side T11.

This stage may emit `MATRIX_HEALTH_DETECTION_OPTIMIZATION_TERMINAL_COMPLETE`
only when all of the following are consumed by existing owners:

1. All existing Health/Test/Stability mechanisms are Atlas-classified with
   owners, producers, consumers, costs and exact decision influence.
2. Decision graph, execution-order/latency map, cadence/timeout/retry/
   persistence rationale and serial/parallel dependencies are proven.
3. Source failure, target readiness, recovery/re-admission and post-switch
   recovery are separate fail-closed contracts.
4. Immediate health, persistence, stability, recovery probation, quality,
   reliability and Engineering history have explicit placement; raw history
   is absent from the synchronous FAST path.
5. Phase C field-by-field commercial findings are consumed through multiple
   concrete candidates and the weighted Phase D/E gate; exactly one
   evidence-backed target architecture is formally decided, implementation
   matches it, and no benchmark is used as post-hoc justification.
6. Exactly one canonical health/failure-event owner remains.
7. FAST/DEEP, source/target and temporal stability/recovery semantics are
   evidence-backed; active-source detection performs only the minimal bounded
   required work.
8. Target readiness is sufficiently fresh or has one exact external blocker.
9. Anti-flap, false-positive/false-negative and recovery behavior are not
   degraded; stale, unknown and conflicting evidence fail closed.
10. Decision-critical configured values are distinguished from observed and
    effective lifecycle values; source defaults alone never establish hot-path
    latency where safe observation or controlled measurement is executable.
11. The existing selector primitive is classified `REUSE`, `ADAPT` or
   `REJECT`; automatic FAST enablement follows only the new weighted terminal,
   while the full Matrix fallback remains until equivalence/consumer proof.
12. Unneeded synchronous work is deferred/removed after consumer proof and no
    competing health subsystem or Runtime dependency exists.
13. Current-scale probe economy and at least 50-egress architecture pass; the
    large-scale stress model is recorded and either preserves the Phase E
    architecture or its exact refinement is returned to and consumed by Phase E.
14. Controlled failure-model validation is complete to the limit of existing
    owners, with residuals classified rather than hidden.
15. `FIRST OBSERVABLE FAILURE SIGNAL -> CANONICAL CONFIRMED FAILURE EVENT` is
    measured segment by segment.
16. `CURRENT_T0_T11_LATENCY_MAP`, `FAILURE_CLASS_LATENCY_MATRIX`,
    `SIGNAL_RESPONSIBILITY_MODEL`, `TEST_ROLE_MATRIX` and
    `TOP_T0_T11_LATENCY_CONTRIBUTORS` distinguish measured Runtime facts from
    static, Polygon and unknown evidence. The external failure-occurrence
    boundary is never fabricated when production provenance is unavailable.
17. `LATENCY_OPTIMIZATION_REGISTER` and `PROBLEM_TO_PATTERN_MAPPING` link
    every proposed optimization to one proved delay/safety problem, an
    existing owner, expected gain, risk, rollback and a `REUSE`/`ADAPT`/
    `REJECT` disposition before architecture selection or implementation.
18. Before/after client-recovery latency, probe count, decision equivalence
    and safety are measured; divergence automatically falls back to full
    Matrix with a durable reason.
19. A lawful ordinary event, when naturally available, relates detection to
    T0-T11; Natural L8 absence cannot keep the Engineering stage open when all
    Engineering criteria are independently complete.
20. Every leftover is `DONE`, `FUTURE_OPTIONAL`, `EXTERNAL_BLOCKED` or
    `NOT_REQUIRED`, with owner and re-entry condition where applicable.
21. CPS owns an exact successor outside this stage or a legal Program terminal;
    durable knowledge is transferred to existing canonical owners and the OMP
    V5.3 frontier is retired under the existing contract.
22. No Runtime consumer depends on this temporary stage or its reports.

### V5.3 retirement contract

After the terminal is consumed, use the existing lifecycle:

```text
ACTIVE -> TERMINAL_COMPLETE -> DURABLE_KNOWLEDGE_EXTRACTED
-> CPS_SUCCESSOR_ADVANCED -> OMP_ACTIVE_REFERENCES_RETIRED
-> CONSUMER_REFERENCE_RESIDUE_PASS -> ARCHIVED_HISTORICAL
```

Archived status means the workstream is historical Engineering evidence only:
it owns no Runtime state, OMP frontier, Matrix truth or automatic reopening.
A later Matrix improvement requires a new measured invalidation or owner-backed
gap and the ordinary existing OMP admission path. The Program file is retained;
its completed workstream is not deleted merely to reduce document size.

## V5.2 CT-M0F causal continuity and autonomous completion track

V5.2 is an internal mandatory track of this existing Program.  It does not
create a Mission, Program, Runtime actor, Planner, queue, watcher, registry,
Authority, certification identity or production entitlement.  It reuses OMP
§14.1/§14.1A for universal continuation enforcement and the existing CT-M0F
contracts below for the current execution semantics.

Its parent completion goal is the existing CT-M0F operational acceptance:

```text
valid CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER samples
  -> Time owner consumes the measurement
  -> exact latency residual, if any
  -> smallest owner-backed repair
  -> deploy and production consumer proof when required
  -> automatic return to the same CT-M0F parent
  -> next ordinary Matrix sample
  -> >= 5 valid samples, p95 <= 3 s, max <= 5 s
  -> CT-M0F COMPLETE_CONSUMED -> CT-M1 READY
```

For this CT-M0F validation-generation contract only, the ordinary Matrix/timer
remains the only producer of a fresh validation generation. It does not
restrict the V5.3 N0–N11 fast-wake precedence law. Neither Codex nor an
operator may invoke it to manufacture a CT-M0F sample. A current incident,
fresh live gates and the active standing policy
may drive the existing Runtime path; this track never creates Candidate,
Packet, lease, restore-barrier, apply, routing mutation or user movement
outside that exact existing-owner envelope.

Every admitted CT-M0F reservation must persist one exact observation before
reset and terminalization: either `VALID_FORWARD_EVIDENCE` or
`INVALID_DIAGNOSTIC_EVIDENCE` with the last responsible predicate.  An invalid
observation never earns sample credit, but it is not discarded as “evidence
missing”; a bounded attempt budget may close only with a durable repair
frontier for that predicate.

### Internal ordered gates

| Gate | Exact purpose | Required owner-backed output -> consumer | Completion condition |
| --- | --- | --- | --- |
| `A_TRUTH_INTEGRITY` | Derive the minimum active working set from CPS Section 0 and the active CT-M0F/Service Failure frontier. | authoritative owner/generation/fingerprint classification -> existing CPS/OMP reconciliation | `ACTIVE_MISSION_TRUTH_GRAPH_CONSISTENT`; historical material outside the active graph is isolated, not silently ignored. |
| `B_CHAIN_INTEGRITY` | Prove every active producer -> consumer edge through behaviour and successor. | edge receipt -> exact next owner | `ACTIVE_MISSION_PRODUCER_CONSUMER_GRAPH_CLOSED`; an absent consumer is a repair residual. |
| `C_AUTONOMOUS_REENTRY` | Prove successor publication causes the existing OMP/Codex re-entry consumer to run. | trigger -> real caller -> exact consumer acknowledgement -> next output | `OMP_END_TO_END_AUTONOMOUS_MISSION_CONTINUATION_PROVEN`; a marker alone is insufficient. |
| `D_SELF_REPAIR_RETURN` | Keep a consumer/implementation repair subordinate to CT-M0F. | repair verification/deploy evidence -> `RETURN_TO_PARENT_MISSION` | `PARENT_MISSION_AUTOMATIC_RETURN_AFTER_REPAIR_PROVEN`. |
| `E_DEAD_END_GUARD` | Convert a repeated unchanged residual or unarmed successor into a repair, not a report loop. | no-progress/continuation diagnostic -> responsible existing owner | `NO_PROGRESS_AND_DANGLING_SUCCESSOR_GUARD_PROVEN`. |
| `F_REAL_ACCEPTANCE` | Exercise the ordinary owner path end-to-end. | Matrix sample -> Time ledger -> residual or SLO evidence -> OMP | at least one complete measure -> repair/remeasure cycle, when a residual exists, occurs without an operator continuation. |
| `G_SLO_COMPLETION` | Consume the existing CT-M0F sample and latency gate. | Time ledger/SLO result -> CPS/OMP successor | CT-M0F is `COMPLETE_CONSUMED` only at the existing five-sample, p95 and max thresholds; otherwise its exact residual remains active. |

The track has two non-interchangeable terminals:

- `V7_END_TO_END_AUTONOMOUS_ENGINEERING_CONTINUATION_CERTIFIED` proves the
  continuation/repair path;
- `LEGACY_OPERATIONAL_RECOVERY_SLO_CONSUMED` proves the measured current
  CT-M0F performance objective.

This track closes only when both are consumed by their existing CPS/OMP
consumers.  Completion of the first cannot substitute for current
control-plane/kernel-path latency evidence; completion of the second cannot
hide a manual continuation dependency.  Runtime operational `STOP_SAFE` remains valid when the live world
blocks action, while stale reads, lost outputs, misbound generations, missing
consumption or an unreachable successor are engineering defects and must
return through the existing BDP -> OMP repair path.

## V5.1 CT-M0F existing-resource target-admission correction

V5.1 records an owner-backed correction to the CT-M0F substrate law.  The
earlier `STOP_SAFE_CT_M0F_STANDING_CONTROLLED_SOURCE_REQUIRED` snapshot is
historical discovery, not proof that a new substrate or Stage-48 expansion is
needed.  Before declaring an external boundary, the existing
`v7-users-autoswitch` selector must dispose every source, certification
identity and target through its current owners.

For a single CT-M0F certification-only sample, source and target have
different safety predicates.  The source must be isolated from ordinary users
and genuinely failed or controlled as the active CT-M0F envelope permits.  A
distinct target may instead be an existing healthy Planner-shared target when
the existing delegated availability-first policy independently proves all of:

- `certification_identities_only=true`, `max_users=1` and
  `max_concurrent_transactions=1` for the admitted selection;
- zero ordinary-identity and ordinary-route delta;
- current health, capacity, verification and containment gates pass;
- the target is distinct, has no conflicting reservation or active operation;
- shared-target fault injection remains forbidden.

This is an existing selector/target-admission repair only.  It does not create
a target owner, provision an identity, widen Authority, grant Stage-48,
CT-M8, L7/L8 or Maturity credit, or allow a shared target to be deliberately
degraded.  Fresh Candidate, Packet, lease, live gates and ordinary
Matrix-owned wake remain mandatory before any effect.

The source selector must report the exact disposition rather than collapsing
a lawful shared-target candidate into a physical-substrate absence.  A valid
production selector result is `CT_M0F_STANDING_CONTROLLED_FAILURE_READY`; a
source-side isolation failure, target-policy failure, reservation conflict or
stale policy projection remains its own exact `STOP_SAFE` terminal.

The active CT-M0F policy/audit record is authoritative for the contract's
validity. CPS/OMP must consume that owner-backed status through the existing
atomic reconciliation path; a historical request-ready field must never
override an active audited contract. Until this consumer is deployed and
proven, the correct terminal is `DEPLOY_REVIEW_REQUIRED_FOR_CT_M0F_SELECTOR_AND_CPS_RECONCILIATION`,
not an external-substrate or Authority claim.

## V5.0 CT-M0F independent-lane execution and fresh-contract correction

V5.0 clarifies execution of the already admitted bounded CT-M0F validation
campaign. It does not create a Program, Authority, Planner, Runtime, registry,
watcher, queue, certification identity or production entitlement. CPS remains
the only live-state owner; this document defines only the consumer contract.

### Fresh contract and lane-separation law

Before every ordinary Matrix-owned CT-M0F generation, the existing
`admin_core.operator_execution` policy/audit owner must freshly prove the
active contract ID/hash, expiry, revocation state, program binding and exact
envelope. A historical approval, report or local cache is never sufficient.

`CT_M0F_STANDING_CONTROLLED_FAILURE_READY` is independent of Stage-48 only
when the existing owners prove no shared controlled source, target,
certification identity, reservation, active operation or exclusion/lock.
Otherwise the Matrix consumer must emit the exact shared-resource conflict and
must not run the CT-M0F sample concurrently. Stage-48 may not be used as a
generic wait label for an independently runnable CT-M0F sample.

An implementation-only fingerprint may rebind under the active standing
envelope only when the existing policy/audit owner proves that its immutable
envelope, Authority scope, source/target-selection law, verification,
containment, expiry and per-fingerprint budget still match. Any semantic
change is `ENGINEERING_AUTHORITY_REQUIRED`; it is never silently converted to
a standing-policy rebind.

### Existing wake and controlled-condition law

The existing Matrix/timer owner is the sole ordinary CT-M0F wake producer for
this CT-M0F contract. It does not restrict V5.3 N0–N11 fast targeted Matrix
confirmation. Neither an operator nor Codex may invoke Matrix to manufacture
a CT-M0F sample.
The first-failure timestamp must retain its actual provenance. A controlled
source condition may be used only if the active exact contract independently
admits that condition; otherwise no client-recovery claim, sample or inferred
zero timestamp may be written.

When the current controlled-pool owner returns
`STOP_SAFE_CT_M0F_STANDING_CONTROLLED_SOURCE_REQUIRED`, the status means the
following exact predecessor is absent:

```text
healthy isolated controlled source
+ exact group-aligned enabled certification identity
+ distinct current controlled-contract-admitted target
```

It is a physical/owner-backed substrate boundary, not a Stage-48 blockage and
not permission to substitute an ordinary production source, create an
identity, mutate a source or dilute group alignment. The durable successor is
the existing controlled-certification pool/Matrix source-change consumer. It
must automatically re-evaluate on the next owner-backed topology, health,
identity, reservation or policy generation; no Codex/operator continuation is
required. If the required substrate remains absent, the terminal is
`EXTERNAL_OWNER_OR_CONTROLLED_SUBSTRATE_REQUIRED`, with zero production
effects.

### CT-M0F repetition and deploy law

One valid property is never re-run merely to accumulate samples. Each sample
must arise from an independently admitted Matrix generation required by the
active SLO residual; duplicate or no-progress generation delivery is consumed
by the existing exact-once owner. Fresh candidate, Packet, lease, live source,
target, capacity, cooldown, anti-flap, verification and containment checks
remain mandatory for each admitted sample.

Any implementation change follows the existing focused-test -> commit/push ->
`tools/v7-safe-deploy` manifest -> production non-test caller/consumer ->
affected replay/Learning -> truth/convergence route. A failed manifest or an
independent production-deploy reviewer boundary is a deploy stop; it must not
be bypassed through another command, a policy edit or a documentation claim.

## V4.9 bounded standing CT-M0F validation campaign

V4.9 supersedes only the per-generation approval semantics of V4.7/V4.8; the
historical one-generation request and its zero-consumption decision remain
immutable and non-reusable. The existing `admin_core.operator_execution`
standing-policy/audit owner now issues one independently decidable
`CT_M0F_BOUNDED_MULTI_GENERATION_USER_PATH_CUTOVER_VALIDATION` envelope. The
active contract lasts 30 days, permits at most one certification identity and
one concurrent operation, and bounds each implementation fingerprint to five
valid and three invalid/safety-stopped attempts.

Matrix is the existing wake/consumer. Each admitted sample still requires a
fresh validation generation, Candidate, Packet, lease, snapshots and live
gates. Verified forward evidence is durably appended before the existing
cleanup owner performs baseline reset or records verified forward recovery;
only then does the Time budget consume the sample and choose the next cold or
warm residual. Restart first reconciles an active reservation, duplicate
Matrix delivery cannot apply twice, implementation-only changes invalidate
prepared artifacts but do not request new Authority, and successful SLO or
budget/safety terminal stops further sampling.

The envelope rejects ordinary identities, non-isolated controlled sources,
shared-target failure injection, Stage 25/48 or CT-M8 credit, Natural L8,
Authority expansion, Runtime scope expansion and Production Maturity change.
Request publication and contract activation themselves create no Candidate,
Packet, lease, restore barrier, route or user effect. A new independent
decision is required only when this semantic Authority envelope expands.

## V4.8 exact approval consumption and practical expiry

V4.8 closes the producer-to-execution-consumer gap discovered after the first
independent CT-M0F decision. The existing governed L3 owner now validates the
exact approved request before artifacts, atomically consumes it only after a
fresh Packet and lease exist, and passes the same request/generation/Packet/
operation/lease/user/source/target lineage to the existing autoswitch Time
consumer before any payload probe. Duplicate consumption, expiry, mismatch or
use through the generic execution path is `STOP_SAFE` before production
effects. The request decision window is 24 hours: still short-lived and
one-use, but long enough for independent review and the existing deploy/reentry
chain. An expired decided request is never renewed or rebound implicitly.

## V4.7 exact one-generation controlled validation admission

V4.7 closes the producer gap between the CT-M0F engineering consumer and the
existing independent Authority audit. The existing operator-execution owner
may now emit one short-lived `CT_M0F_ONE_GENERATION_KERNEL_CUTOVER_VALIDATION`
request bound to the active Program, current standing-policy contract/hash,
current certification-pool/registry fingerprints, one source, one cold or
warm generation, `max_users=1`, `max_concurrent_transactions=1`, fresh
post-decision Candidate/Packet/lease and one-use semantics.

This request is deliberately narrower than the existing Tier-48 substrate and
progressive-campaign request. It cannot provision identities, advance campaign
stages, select a target before the fresh Planner generation, create execution
artifacts, degrade a source, apply routing, move a user, claim remote recovery,
earn L7/L8 credit, expand Authority or change Production Maturity. The same
append-only Authority audit owns request and exact-once decision provenance;
no new owner, registry, queue, watcher, Planner, Runtime or Authority system is
created. Approval, if independently supplied, only unlocks the existing fresh
Matrix/governed validation consumer for that exact generation.

## V4.6 current-stage cutover object and deferred remote recovery gate

V4.6 corrects the current CT-M0F measurement object without weakening the
V4.5 remote-device evidence contract. Production reality consumed by CT-M0
proves that the current legacy dataplane is owned by server-side per-user
assignment, source-policy rule and routing-table state. An online capable
remote certification client agent is not currently implemented or available.
Therefore remote-device recovery is a future production-validation criterion,
not a prerequisite for current kernel/class engineering.

CT-M0F remains one Mission with two distinct acceptance surfaces:

```text
CT_M0F_KERNEL_CUTOVER_ENGINEERING_CONSUMED
-> may unlock CT-M1 engineering only

FUTURE_REMOTE_CLIENT_AGENT_END_TO_END_RECOVERY_VALIDATION
-> remains required before any remote-device recovery, application recovery,
   existing-flow survival, production class certification, Authority expansion
   or Production Maturity claim
```

The current object is:

```text
CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_LATENCY
= HARD_FAILURE_CONFIRMED
  -> exact decision/Packet/lease/operation binding
  -> canonical certification-identity assignment commit
  -> exact source-policy table kernel visibility
  -> selected target egress fresh payload readiness
  -> cross-owner agreement
```

This current metric may prove that V7 changed the exact identity's canonical
assignment and effective Linux path and that the selected target independently
carried a fresh application payload. It must not be named or reported as
remote-client, application-visible or existing-flow recovery. It may be named
`USER_PATH_CUTOVER` only when the payload itself is proven to have traversed
the exact identity source address plus its fwmark/table/policy context. When
the payload is bound only to the selected target interface, the mandatory
terminal is the narrower
`CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_PASS`.

The prior V4.5 remote metrics and terminals remain visible under:

```text
REMOTE_CLIENT_APPLICATION_RECOVERY_LATENCY=NOT_MEASURED_NO_CLIENT_AGENT
EXISTING_FLOW_RECOVERY_LATENCY=NOT_MEASURED
REMOTE_DEVICE_RECOVERY=DEFERRED_TO_FUTURE_CLIENT_AGENT_CAPABILITY
```

They do not block CT-M1 engineering, but they continue to block every stronger
production/end-user claim named above. They are not PASS, removed evidence or
an Authority/Maturity waiver.

### Current cutover monotonic contract

The existing Time owner consumes one clock domain with these boundaries:

```text
FIRST_FAILED_OBSERVATION
HARD_FAILURE_CONFIRMED
USER_TARGET_DECISION_BOUND
APPLY_ADMITTED
CANONICAL_USER_ASSIGNMENT_COMMITTED
KERNEL_ROUTE_MUTATION_COMPLETED
EXACT_USER_KERNEL_PATH_VISIBLE
TARGET_EGRESS_PAYLOAD_PASS
CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_PASS
DEFERRED_CLOSURE_ACTIVATED
DEFERRED_CLOSURE_COMPLETE
RESET_APPLY_ADMITTED
RESET_CANONICAL_ASSIGNMENT_COMMITTED
RESET_EXACT_USER_KERNEL_PATH_VISIBLE
RESET_TARGET_EGRESS_PAYLOAD_PASS
RESET_CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_PASS
RESET_DEFERRED_CLOSURE_COMPLETE
```

Unknown intervals are `UNKNOWN`, never zero. Wall clock preserves lineage
only; elapsed SLO uses `time.monotonic_ns()`. Assignment, route, payload,
operation, Packet, lease, incident and validation generations must agree or
the result is `USER_PATH_CUTOVER_CROSS_OWNER_MISMATCH`.

The current operational total gate is authoritative:

```text
CONTROL_PLANE_AND_KERNEL_PATH_CUTOVER_LATENCY CONTROLLED_GATE_P95 <= 3000 ms
AND no valid sample > 5000 ms
```

Substage ceilings are diagnostic and may overlap; they must never be added as
independent serial allowances that exceed the total. The ledger must expose at
least decision, admission, assignment CAS, route mutation, visibility and
target-payload intervals, and `UNKNOWN` or unexplained time blocks the gate.
The controlled five-sample p95 uses nearest-rank and is explicitly a bounded
engineering gate, not a statistically representative production percentile.
A p99 claim still requires at least 100 owner-backed observations.

### Current proof composition and probe reuse

The existing assignment/route owner must prove the exact certification
identity, old/new egress, registry and assignment generation, source-policy
rule, routing table, fwmark or explicit none, expected interface, tested
destination and absence of the old effective binding. The existing payload
logic may be reused only as a separately versioned
`target-egress-payload-readiness` receipt bound to the same target/path and
operation generation. Two disconnected receipts never become an exact
identity payload claim merely by sharing a target name.

Fresh compatible Matrix evidence remains reusable. With no declared
invalidation, full Matrix verification before the current cutover terminal is
forbidden; mandatory Outcome/Replay/Learning, temporal verification, reset and
reporting continue through the crash-safe deferred closure successor.

### Authority, Polygon and admission boundaries

An active standing movement policy does not authorize deliberate source
degradation, certification-substrate mutation or controlled-condition
creation. Each such effect requires its exact current existing-owner admission;
expired or broader campaign approvals are non-reusable. No ordinary user may
be used.

When no qualifying current failure generation exists, the existing Permanent
Polygon may select the exact missing controlled latency cell and prepare a
safe L7 opportunity. Only the real bounded Controlled Production transaction
creates current cutover evidence; Polygon output itself grants no L7/L8,
production, Authority or Maturity credit. Natural L8 is never manufactured.

CT-M0F current engineering completes only after at least five distinct valid
certification-only samples spanning two owner-backed generations, including
one cold and two warm samples, consume the current total gate, reset cutover,
deferred closure, hidden-O(N) guard, performance ledger and before/after
contract. Production movement is never performed solely to fill a percentile.

Required current engineering terminal:

```text
CT_M0F_KERNEL_CUTOVER_ENGINEERING_CONSUMED
AND REUSABLE_FAST_PATH_PRIMITIVES_PROVEN_AND_LEGACY_EXCEPTION_FALLBACK_CERTIFIED
-> CT-M1=READY_ENGINEERING_ONLY
```

Required future production residual:

```text
FUTURE_REMOTE_CLIENT_AGENT_END_TO_END_RECOVERY_VALIDATION
-> exact remote route-bound payload and recovery clocks
-> production/end-user claim eligibility only after its own owner consumption
```

## V4.5 exact client recovery measurement contract

CT-M0 is a consumed read-only audit. Its `141.353447 s` baseline is the full
successful forward-plus-reset lifecycle and must not be presented as measured
client outage or as an acceleration result. No current-client speed claim is
legal until the existing Time owner measures `CLIENT_TRAFFIC_RECOVERY_LATENCY`
from the failure signal to the first successful exact route-bound traffic
probe.

CT-M0F remains one Mission, not a new Program or Mission, but has two
machine-ordered internal phases:

1. `CT-M0F-E_ENGINEERING` implements and deploys only the exact existing-owner
   extensions admitted by CT-M0. It has zero routing/user effect.
2. `CT-M0F-V_CONTROLLED_VALIDATION` starts only after E is deployed, its
   focused callers, truth and convergence pass, and one exact current
   owner-backed certification-only contract admits the validation. It measures
   the current legacy single-user path with one certification identity and one
   concurrent transaction. It cannot use an ordinary user, expand Authority,
   certify the future class/bucket path, earn CT-M8 evidence, or change
   Production Maturity.

CT-M0F-E must separate the client critical path from durable closure:

```text
failure signal
-> prepared decision generation check
-> route mutation
-> route visibility
-> exact route-bound traffic recovery probe
-> CLIENT_TRAFFIC_RECOVERY terminal
-> durable deferred verification / Outcome / Replay / Learning / reset closure
```

The current-client clock stops only at the first successful route-bound traffic
probe; route visibility alone is insufficient. The closure clock continues
independently. Reset has its own `RESET_CLIENT_TRAFFIC_RECOVERY_LATENCY` and
must not be folded into the forward recovery metric.

The route-bound probe is valid only under
`EXACT_CLIENT_NETWORK_CONTEXT_TRAFFIC_PROBE_PROVEN`. It must:

- execute in the exact certification identity network context and consume the
  same routing table, source binding, fwmark/policy and exception precedence
  that govern that identity;
- open a fresh connection and never reuse a cached socket;
- avoid the management/default route unless that route is itself the exact
  expected user route under test;
- prove the expected target egress fingerprint through the existing route and
  target-identity owners;
- validate an application payload and response, not merely DNS, TCP connect,
  TLS setup, route visibility or kernel counters;
- use a fresh DNS result or an explicitly still-valid DNS generation and
  record which contract was used;
- carry bounded timeout, retry count and probe cadence; every retry and failed
  attempt remains part of elapsed client recovery time;
- emit `PROBE_INVALID` rather than PASS when exact client context, target
  egress, payload response, freshness or timing cannot be proven.

Failure and recovery timing uses three owner-backed boundaries:

```text
FIRST_FAILED_OBSERVATION_AT
HARD_FAILURE_CONFIRMED_AT
CLIENT_TRAFFIC_RECOVERED_AT
```

`FIRST_FAILED_OBSERVATION_AT` is the first failed observation subsequently
bound to the same confirmed hard-failure generation. An isolated observation
that never becomes that generation is noise and grants no failure sample.
Threshold crossing owns `HARD_FAILURE_CONFIRMED_AT`; it is not allowed to erase
the preceding detection interval.

The existing Time owner derives:

```text
FAILURE_DETECTION_LATENCY
= HARD_FAILURE_CONFIRMED_AT - FIRST_FAILED_OBSERVATION_AT

POST_CONFIRMATION_RECOVERY_LATENCY
= CLIENT_TRAFFIC_RECOVERED_AT - HARD_FAILURE_CONFIRMED_AT

FIRST_FAILURE_EVIDENCE_TO_CLIENT_RECOVERY_LATENCY
= CLIENT_TRAFFIC_RECOVERED_AT - FIRST_FAILED_OBSERVATION_AT
```

The last metric is the primary user-facing end-to-end recovery SLO. Every
sample records `clock_domain_id`, `clock_uncertainty_ms`, `probe_cadence_ms`
and measurement resolution. Monotonic timestamps from different clock domains
must not be subtracted without an owner-backed mapping and uncertainty bound.
If cadence or clock uncertainty could change a gate verdict, the result is
`MEASUREMENT_UNCERTAINTY_STOP_SAFE`, never PASS.

CT-M0F-V must compare the immutable `141.353447 s` full-lifecycle baseline with
the post-deploy lifecycle and publish, at minimum:

- failure signal -> decision;
- decision -> route mutation;
- route mutation -> route visibility;
- visibility -> successful client traffic recovery;
- recovery -> durable closure activation;
- deferred verification and full closure;
- reset mutation -> reset traffic recovery;
- complete reset closure;
- cold/warm sample identity, monotonic clock, unknown time and invalid samples.

The first bounded legacy-path acceptance gate is a transitional ceiling, not
the target SLO and not a CT-M0F completion terminal:

```text
at least three valid controlled certification-only samples
AND CLIENT_TRAFFIC_RECOVERY_LATENCY p95 <= 10,000 ms
AND no valid sample > 15,000 ms
AND HEAVY_CLOSURE_REMOVED_FROM_CLIENT_RECOVERY_PATH
AND zero weakened verification, rollback, Authority or ordinary-user guards
```

Passing that ceiling emits
`TRANSITIONAL_GATE_PASS_OPERATIONAL_LATENCY_RESIDUAL_READY` and automatically
returns the exact measured latency residual to `CT-M0F-E_ENGINEERING` through
the existing BDP/OMP consumer. It must not mark CT-M0F complete, unlock CT-M1
or be described as fast failover.

The required legacy operational gate is:

```text
at least five valid controlled certification-only samples
AND at least one cold and two warm samples
AND the remaining two samples may independently be cold or warm
AND samples span at least two current owner-backed generations
AND FAILURE_DETECTION_LATENCY p95 <= 2,000 ms
AND DECISION_PLUS_ROUTE_COMMIT_LATENCY p95 <= 500 ms
AND CLIENT_TRAFFIC_RECOVERY_LATENCY p95 <= 3,000 ms
AND no valid CLIENT_TRAFFIC_RECOVERY_LATENCY sample > 5,000 ms
AND HEAVY_CLOSURE_REMOVED_FROM_CLIENT_RECOVERY_PATH
AND zero weakened verification, rollback, Authority or ordinary-user guards
```

Only that gate may emit `LEGACY_OPERATIONAL_RECOVERY_SLO_CONSUMED` and complete
the current-client latency part of CT-M0F. A p99 claim requires at least 100
owner-backed observations; production actions must never be manufactured only
to fill a percentile. Until then p99 is `INSUFFICIENT_SAMPLE_COUNT`, never
zero or inferred from p95.

Every controlled sample must arise from a distinct independently admitted
validation generation required by the current unresolved SLO residual. One
sample cannot occupy multiple sample positions. Once an exact property is
proven, an identical generation must not be repeated without an owner-backed
invalidation or a genuinely different required cold/warm, source/target/path,
failure or recovery condition. Production movement must never be performed
only to increase sample count or improve a percentile.

The future prepared class/bucket path has a separate mandatory target:

```text
FAILURE_DETECTION_LATENCY p95 <= 2,000 ms
AND PREPARED_DECISION_VALIDATION_PLUS_KERNEL_COMMIT p95 <= 250 ms
AND ROUTE_VISIBILITY_LATENCY p95 <= 100 ms
AND CLIENT_TRAFFIC_RECOVERY_LATENCY p95 < 1,000 ms
AND CLIENT_TRAFFIC_RECOVERY_LATENCY p99 <= 5,000 ms
    only after at least 100 owner-backed observations
AND 10-member versus 10,000-member cutover delta is within the declared
    constant-time tolerance
```

The `<1,000 ms` class target is certified only through CT-M5/CT-M7/CT-M8
evidence appropriate to each substrate. Logical or kernel Polygon evidence may
prove complexity and cutover behavior, but only controlled production may
prove route-bound client traffic recovery. The legacy `<3,000 ms` gate cannot
substitute for the class target.

One cold and two warm samples are sufficient only for the transitional ceiling
when their source/target/path and invalidation identities are explicit. The
operational gate requires the larger sample contract above. Samples cannot be
repeated merely to obtain a preferred percentile. If an owner-backed external
network lower bound prevents a gate, CT-M0F remains incomplete and publishes
the exact interval, owner, evidence and successor; the threshold is not
silently weakened.

Required CT-M0F terminals are all mandatory:

- `CURRENT_SINGLE_USER_CLIENT_RECOVERY_LATENCY_MEASURED`;
- `EXACT_CLIENT_NETWORK_CONTEXT_TRAFFIC_PROBE_PROVEN`;
- `FIRST_FAILURE_EVIDENCE_TO_CLIENT_RECOVERY_CLOCK_PROVEN`;
- `MEASUREMENT_CADENCE_AND_CLOCK_UNCERTAINTY_PROVEN`;
- `CURRENT_SINGLE_USER_CRITICAL_PATH_SUBSTANTIALLY_REDUCED`;
- `LEGACY_OPERATIONAL_RECOVERY_SLO_CONSUMED`;
- `HEAVY_CLOSURE_REMOVED_FROM_CLIENT_RECOVERY_PATH`;
- `CURRENT_LEGACY_EXCEPTION_PATH_BEFORE_AFTER_PRODUCTION_CONSUMED`;
- `REUSABLE_FAST_PATH_PRIMITIVES_PROVEN_AND_LEGACY_EXCEPTION_FALLBACK_CERTIFIED`.

Functional tests, local microbenchmarks, route visibility without a traffic
probe, a report, deploy, or a faster closure after the client was already
restored cannot substitute for these terminals.

## V3.2 active executable correction — partial cohort recovery and internal drain

V3.2 closes an implementation-only recovery gap in the existing
availability-first Matrix -> governed executor -> audit -> CPS/OMP chain. It
creates no Program, Planner, Runtime, registry, queue, watcher, scheduler,
Authority owner, policy store, executor or evidence store.

If an immutable stage cohort contains both verified forward members and one or
more members that never completed forward execution, the stage is incomplete.
It must never be represented as a completed cohort or receive a stage receipt.
The existing executor must reconstruct every successful member from its exact
Packet, audit, route, switch, Outcome, Replay and Learning lineage; restore
only members still outside the controlled baseline; then immediately re-enter
the existing fresh planner for the same stage. Members with no successful
forward terminal are not reset and are not credited.

All successful recovery/reset steps remain inside the same bounded Matrix
invocation. A new Matrix generation is required only for a material freshness,
capacity, health, lease, circuit-breaker or policy invalidation. Existing
single-user Packet/lease semantics and `max_concurrent_transactions=1` remain
the current safety bound; they do not imply one Matrix generation per user.

The stage receipt is legal only after a fresh complete immutable cohort has
per-user, per-target, aggregate and ordinary-user verification,
Outcome/Replay/Learning and full baseline reset. The next stage is then
consumed by the existing bounded successor loop without operator input.

## V3.1 active executable revision — standing availability-first ladder

V3.1 admits
`STANDING_DELEGATED_AVAILABILITY_FIRST_CONTROLLED_FAILOVER_AND_LADDER_V1`
inside this existing Program. It extends the existing standing-policy,
target-classification, adaptive-capacity, allocation, governed execution,
verification, Outcome/Replay/Learning and CPS/OMP owners. It creates no
Program, Planner, Runtime, registry, queue, watcher, scheduler, Authority
owner, policy store, executor, evidence store or truth source.

### Reuse and invalidation law

Before implementation or repeated verification, the Mission must classify the
existing semantic capability, owner, evidence generation and declared
invalidation trigger. Valid matching knowledge is
`RESULT_REUSED_VALID`. Generic 1/2/4/5/10/25/48 movement evidence may prove
the common movement primitive, but it does not by itself prove
availability-first target admission, shared-target reserve protection,
multi-target allocation or ordinary-user invariance. Only those exact
unclosed semantics are revalidated.

### Authority ordering

Engineering may implement and verify the complete bounded class, then create
one fresh request through the existing standing delegated policy owner.
Before independent activation, the exact legal terminal is
`ENGINEERING_AUTHORITY_STANDING_DELEGATED_AVAILABILITY_FIRST_POLICY_REQUIRED`.
That terminal permits no policy write, Candidate, Packet, lease, restore
barrier, apply, routing mutation, user movement or rollback apply.

Independent activation may add exactly:

`BOUNDED_AVAILABILITY_FIRST_CONTROLLED_FAILOVER`.

It never approves a target, identity, allocation, Packet or campaign stage.
The standing contract defines the immutable safety envelope; the existing
Planner selects fresh exact targets and the existing Packet binds the exact
immutable allocation. Old one-off degraded-target requests are superseded
through the existing append-only Authority audit only after the standing
contract becomes active.

After activation, a conforming fresh action is
`AUTO_ADMITTED_BY_STANDING_DELEGATED_AVAILABILITY_FIRST_POLICY`. A new Codex
turn or operator message is not a wake source. The only continuation is:

```text
Matrix observation
-> fresh inventory and target classification
-> adaptive capacity
-> immutable allocation
-> standing-policy admission
-> fresh Candidate / Packet or packet-set / lease
-> restore barrier
-> bounded certification-only apply
-> per-user / per-target / aggregate / ordinary-user verification
-> containment, redistribution or rollback
-> Outcome / Replay / Learning
-> baseline reset
-> atomic CPS/OMP successor
-> next Matrix generation
```

### Immutable envelope

The availability-first action class is certification-only and has:

- ordinary identity, assignment and route delta equal to zero;
- no ordinary-user reclassification;
- no shared-target fault injection, restart, hard-limit, credential, secret
  or external-resource mutation;
- maximum 48 certification identities per transaction and one concurrent
  transaction;
- fresh inventory, adaptive capacity, immutable allocation, Candidate,
  Packet or packet-set and lease;
- restore barrier before apply;
- per-user, per-target, aggregate and ordinary-user quality verification;
- cohort circuit breaker and partial-target containment;
- bounded redistribution or rollback;
- expiry, revoke, freeze, kill and no-self-expansion semantics.

The maximum 48 is an Authority ceiling, not an execution entitlement. Every
transaction is narrowed by current technical capacity, target-specific proven
scope, verification/containment scope, Runtime scope and the exact requested
stage.

### Target and capacity law

Target states remain `HEALTHY`, `DEGRADED_USABLE`,
`LAST_RESORT_USABLE`, `DEGRADED_OBSERVATION_INSUFFICIENT` and
`HARD_INELIGIBLE`. The actual controlled source is excluded before
allocation. Soft quality alone cannot create `HARD_INELIGIBLE`.

For every target, the existing projection exposes owner, value, fingerprint,
freshness and reason for:

```text
hard capacity remaining
ordinary-user protection margin
throughput-safe increment
quality-safe increment
verification-safe increment
rollback/containment-safe increment
Authority-safe increment
Runtime-safe increment
```

The executable target capacity is their minimum. `DEGRADED_USABLE` and
`LAST_RESORT_USABLE` begin with a one-identity trial ceiling. Growth is
target-specific and requires a real matching Outcome plus ordinary-user
protection PASS. Polygon evidence may verify decisions and failure handling
but never raises production-proven capacity.

### Allocation and ladder law

The canonical ladder is `1 -> 2 -> 5 -> 10 -> 25 -> 48`. Each number is the
exact total cohort of one stage, not an additive delta and not a forced
movement count. Every stage uses a new inventory, allocation, Candidate,
Packet/packet-set and lease after baseline reset. The safe subset may be
smaller only as an owner-backed measured result; it does not falsely complete
the requested stage.

Multi-target allocation is allowed only when per-target reservations are
non-overlapping, correlation domains are explicit, total allocation equals
the exact cohort and partial-target failure can be contained without
invalidating unaffected targets.

The shared-target capacity reservation reuses the existing serialized
Packet/lease owner. It is an immutable per-target capacity claim bound to the
fresh inventory and allocation fingerprints, valid for one active transaction
only, with a mandatory fresh pre-apply capacity check. It is not a second
durable reservation registry. A multi-target stage is one immutable allocation
and a serial packet-set; every subset gets a fresh Candidate, Packet and lease,
while the stage receipt is appended only after all subsets, ordinary-user
assignment/route and target-quality checks, Outcome/Replay/Learning and
baseline reset pass.

Target-specific adaptive growth is derived from the same append-only Authority
audit stage receipts. A receipt stores only compact target identity, verified
scope and target/capacity fingerprints; it stores no raw cohort list. A
degraded or last-resort target begins at one, then may attempt only the next
ladder bound supported by its preceding real receipt and fresh live capacity.

### Production-effect ownership

Discovery, engineering, tests, Polygon and request preparation perform no
production action. Production action is legal only after the standing
contract is independently active and only through the existing Matrix-owned
governed execution path with all fresh gates. Later verification, Replay,
Learning and reconciliation cannot perform an additional action unless a new
fresh Matrix generation independently admits it.

### Legal measured stop

After activation, a generic wait is illegal while any fresh safe allocation
exists. A stop must preserve completed evidence and name every target
classification, per-target and aggregate safe capacity, exact requested
stage, shortfall, limiting owner-backed bounds, attempted alternative
allocations and automatic re-entry trigger.

The final terminal
`SERVICE_FAILURE_CONTROLLED_PRODUCTION_OUTCOMES_CONSUMED_1_2_5_10_25_48`
is legal only after every real stage has exact cohort/allocation lineage,
Runtime apply, per-user/per-target/aggregate/ordinary-user verification,
rollback or certified no-rollback, Outcome, Replay, Learning, baseline reset
and CPS/OMP consumption.

## V3.0 active executable revision — availability-first shared-target admission

V3.0 consumes the existing Matrix, quality, capacity/reserve, target ranking,
standing-policy, Candidate/Packet/lease, controlled campaign and Polygon
owners.  It creates no Program, Planner, Runtime, registry, queue, watcher,
scheduler, Authority owner, policy store, executor or evidence store.

The normal production quality floor remains unchanged.  A target below that
floor is not automatically assigned zero technical capacity merely because its
quality result is soft.  The existing target diagnostic now distinguishes
`HEALTHY`, `DEGRADED_USABLE`, `LAST_RESORT_USABLE`,
`DEGRADED_OBSERVATION_INSUFFICIENT` and `HARD_INELIGIBLE` through owner-backed
reachability, freshness, throughput, capacity/reserve, verification,
containment and source/target-role checks.

`DEGRADED_USABLE` and `LAST_RESORT_USABLE` are read-only technical projections,
capped at one certification identity per target. They never create execution
permission. Their only legal successor is an exact existing standing-policy
Authority decision, followed by a fresh generation and new Candidate, Packet
and lease. `HARD_INELIGIBLE` and insufficient observation retain zero capacity
for that target only. If no distinct target reaches an emergency class, the
legal terminal remains the exact existing capacity-substrate/provisioning
boundary; this Program must not pretend that code can create missing external
capacity.

Before allocation, the existing topology owner must reproject the target set
against the **actual** controlled source selected in that generation. A
historical campaign source is diagnostic lineage only and must never remain in
the destination capacity denominator. If this source-distinct re-projection
leaves only one degraded availability slot, its terminal is
`ENGINEERING_AUTHORITY_EXACT_DEGRADED_SHARED_TARGET_ACTION_CLASS_CONTRACT_REQUIRED`;
it is not a campaign-stage advance, capacity claim, or execution grant.

## V2.9 active executable revision — shared production target capacity and role-safe re-entry

V2.9 consumes the existing target inventory, Matrix, quality, capacity and
topology owners; it introduces no Program, Planner, Runtime, registry, queue,
watcher, scheduler, Authority owner, policy store, execution owner or evidence
store. A controlled source remains isolated because only it may receive a
deliberate controlled condition. A healthy shared egress may be a destination
only when its ordinary-user reserve and SLO gates are owner-backed, its target
is never fault-injected, ordinary assignment and route deltas remain zero, and
every selected target is distinct from the actual controlled source.

Current CPS-derived terminal: `SHARED_TARGET_CAPACITY_CONSUMED_SAFE_REENTRY_PUBLISHED`.
Current terminal report:
`docs/reports/engineering/2026-07-30_111500_shared_production_target_capacity_and_safe_reentry.md`.
Live stop, next action and scheduling remain CPS-owned; this program text is
only the durable operating rule for that existing projection.

Technical capacity is never an implicit policy grant. The projection may only
publish `EXACT_SHARED_PRODUCTION_TARGET_ACTION_CLASS_CONTRACT_REQUIRED`; it
never creates a Candidate, Packet, lease, restore barrier, policy write or
production action. If the only currently feasible allocation equals the actual
controlled source, the terminal is not `EXTERNAL_OWNER_REQUIRED`:

`SAFE_REENTRY_REQUIRED:ACTUAL_SOURCE_DISTINCT_SHARED_TARGET_REVALIDATION`.

The existing Matrix/quality owner automatically re-enters the same topology
diagnostic on its next fresh observation. It may publish a successor only for
a distinct target set satisfying health, stability, capacity/reserve,
verification and rollback gates. Otherwise it preserves this exact safe
boundary. No Authority or production effect is legal at that terminal.

## V2.8 historical executable revision — post-trial full-path topology selection

V2.8 admits the exact residual
`CONTROLLED_TOPOLOGY_CONTINUATION_PATH_AND_DELEGATED_PROVISIONING_V1`
inside this existing Program. It extends the existing topology diagnostic,
campaign target ranking, CPS/OMP projection, standing-policy boundary and
Polygon contract. It creates no new Program, Planner, Runtime, registry,
queue, watcher, scheduler, Authority owner, policy store, execution path,
evidence store or truth source.

The one-identity topology trial is valid production evidence for the already
proved bounded mechanism. It is not evidence that its resource can complete
the controlled campaign. After every trial the existing diagnostic must
publish:

```text
POST_TRIAL_CONTROLLED_TOPOLOGY_DECISION_DIAGNOSTIC
CONTROLLED_CERTIFICATION_CAMPAIGN_TOPOLOGY_PLAN
CONTROLLED_CERTIFICATION_CAMPAIGN_TOPOLOGY_RECOMMENDATION
```

The projection accounts for every identity in the exact campaign group and
keeps source, target/target-set and reset/recovery roles separate. An existing
controlled source with certification-only occupancy is not rejected merely
because it is no longer empty, but it is never executable when its reservation
is expired, its reservation group differs from its assigned certification
group, its campaign binding was not consumed, or the current executor supports
only the initial empty-source bootstrap.

Current-next-action feasibility and full-campaign feasibility are distinct.
A draft whose usable capacity is below the current stage is bootstrap-only.
It must not emit a provisioning Authority request or outrank a topology that
can credibly complete `5 -> 10 -> 25 -> 48`. Every candidate path is ranked by
campaign completion, ordinary-user isolation, independent failure control,
rollback, health/stability, capacity/reserve, external dependencies, reuse,
correlation risk and deterministic teardown.

When no owner-backed target or correlation-distinct target set can support the
completion stage, the exact terminal is:

`EXTERNAL_OWNER_CONTROLLED_CERTIFICATION_FULL_PATH_TARGET_CAPACITY_REQUIRED`.

This terminal supersedes a capacity-insufficient draft recommendation and a
wait for recovery of a historical source. It requests no Authority and permits
no policy write or production effect. Re-entry is:

```text
owner-verified isolated target resource or target set
-> existing admin draft lifecycle
-> fresh Matrix / quality / capacity
-> same topology ranking
-> minimal existing standing-policy request only after full-path proof
```

Only the action classes required by the selected full path may later be added
to the existing standing envelope. Compliant actions become automatic only
after independent activation. The campaign still requires fresh immutable
Candidate, Packet and lease, restore barrier, per-user and aggregate
verification, circuit breaker, rollback/containment, Outcome, Replay,
Learning, baseline reset and CPS/OMP consumption for every stage.

The V2.8 engineering completion contracts are:

`POST_TRIAL_DEDICATED_DRAFT_SELECTION_CAUSALLY_RESOLVED`

and:

`CONTROLLED_TOPOLOGY_FULL_PATH_SELECTION_RUNTIME_CONSUMED`.

## V2.7 active executable revision — Matrix consumption of controlled topology

V2.7 closes the exact producer-consumer residual proven after V2.6 policy
activation:

```text
topology manifest AUTO_ADMITTED
-> Matrix bounded service-failure consumer returned incident not actionable
-> no consumer invoked reservation and generic governed transaction
```

This is an existing-owner integration gap, not missing Authority, missing
channel, a new action class or a new execution architecture. The production
Matrix proved source `1` failed `0/14`, while `vless` was healthy `14/14`,
empty, stable and capacity-safe. The existing topology owner selected
`OPTION_1_REBIND_EXISTING_EMPTY_EGRESS`, exact identity `10.7.0.100`, and
manifest-bound target `vless`.

When the ordinary bounded incident consumer has no actionable movement, the
same Matrix lifecycle now consumes the existing topology diagnostic. It may
continue only when the current standing contract independently validates the
exact topology action class and the diagnostic returns
`AUTO_ADMITTED_BY_STANDING_DELEGATED_CONTROLLED_TOPOLOGY_POLICY`.

The consumer:

1. re-runs the existing topology Planner immediately before execution;
2. binds contract ID/hash, manifest hash, certification identity, source and
   target;
3. uses the existing `v7-egress-set-state` CAS reservation owner;
4. passes the exact selection into the generic governed
   Candidate/Packet/lease/restore-barrier/apply transaction;
5. preserves ordinary assignment and route deltas at zero;
6. verifies the exact user route and persists Outcome/Replay/Learning through
   existing owners;
7. releases the reservation from the owner backup if the transaction stops
   before a successful apply;
8. returns the existing Matrix post-action passive and OMP consumers.

No new Planner, executor, policy store, Authority owner, event store, watcher,
queue, scheduler or Runtime is introduced. A missing, stale, changed,
non-empty, non-certification or non-admitted manifest remains `STOP_SAFE`.

The V2.7 completion contract is:

`ONE_IDENTITY_AUTONOMOUS_CONTROLLED_TOPOLOGY_TRIAL_PROVEN`

followed by owner-backed Outcome, Replay, Learning and atomic CPS/OMP
successor consumption.

## V2.6 active executable revision — bounded autonomous controlled topology

V2.6 admits the exact residual
`BOUNDED_AUTONOMOUS_CONTROLLED_CERTIFICATION_TOPOLOGY_AUTHORITY_V1`
inside this Program. It extends the existing standing delegated policy owner,
topology capability map, Matrix consumer, governed Candidate/Packet/lease
executor, restore barrier, Outcome/Replay/Learning owners and append-only
Authority audit. It creates no Program, Planner, Runtime, registry, queue,
watcher, scheduler, Authority owner, evidence store or truth source.

Discovery proved that the existing standing policy semantically authorizes
only service-failure failover. The V2.5 one-off source-rebind request therefore
remains fail-closed evidence of the intended topology action; it is not a
standing grant and must not be manually or automatically approved after this
revision is activated.

The existing standing policy may be independently replaced by one combined,
profile-aware contract:

```text
existing service-failure action class and bounds
+
bounded autonomous controlled-certification topology action class
```

The topology class initially admits only
`REBIND_CONTROLLED_CERTIFICATION_SOURCE`. Dedicated-source provisioning is
automatic only when the existing draft owner proves a ready disabled resource
without external server, peer, credential, secret or hard-limit mutation;
until that producer-consumer contract is proven, provisioning remains an exact
external/Authority boundary. A per-user policy table is not sufficient
isolation.

The immutable topology envelope is:

```text
certification identities only
max users per transaction = 1
max concurrent transactions = 1
ordinary identity delta = 0
ordinary assignment mutation = forbidden
ordinary route delta = 0
target ordinary users = 0
fresh owner-backed health, stability and capacity required
fresh manifest, Candidate, Packet and lease required
restore barrier before apply required
verification and bounded idempotent rollback required
external resource, credential and hard-limit mutation forbidden
Authority self-expansion forbidden
```

The combined request is produced and registered by the existing
`admin_core/operator_execution.py` standing-policy owner. It remains
non-activating until one exact independent
`APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY` decision is consumed by that
owner. Before activation there is no policy write, reservation, Candidate,
Packet, lease, restore barrier, apply, route/assignment mutation or rollback.
Initial topology scope one cannot automatically expand to two or more; any
larger bound requires a new exact independently decidable standing-policy
request.

Historical service-failure-only contracts retain their exact normalized scope
and hash. Profile-specific fields are included only in combined contracts.
This prevents an engineering deployment from silently reinterpreting,
invalidating or expanding the currently active Tier-48 policy.

After activation, the existing live topology map re-ranks all current options.
A material inventory change invalidates the short-lived allocation and every
Candidate/Packet/lease identity, not the standing policy. A matching one-off
topology request becomes non-actionable and is superseded through the existing
Authority audit owner; it is never reused as execution permission.

The automatic production chain is:

```text
fresh Matrix generation
-> current topology capability map
-> standing-policy admission
-> AUTO_ADMITTED_BY_STANDING_DELEGATED_CONTROLLED_TOPOLOGY_POLICY
-> existing controlled-source reservation owner
-> fresh Candidate / Packet / lease
-> restore barrier
-> exact certification-only apply
-> per-user, aggregate and ordinary-invariance verification
-> rollback or certified no-rollback
-> Outcome / deterministic Replay / Learning
-> atomic CPS/OMP successor
```

Polygon and production reuse the same situation, capability-map, selection,
admission, Candidate, Packet, lease, verification and Outcome schemas and
invariants. Their artifact identities and effect adapters remain separate.
Polygon artifacts never become production Candidate, Packet, lease or
production evidence.

The first production trial is exactly one currently valid certification
identity and performs no ordinary-user effect. It may run only after the
combined standing contract is independently active and every live gate passes.
Its completion is
`ONE_IDENTITY_AUTONOMOUS_CONTROLLED_TOPOLOGY_TRIAL_PROVEN`.
Further progression may continue only inside both current certified capability
and independently delegated Authority; otherwise the exact next expansion
request is the terminal.

One compact Russian Engineering Report is required per material Mission or
legal terminal. Per-action detail remains in the existing append-only audit
and Outcome owners; reports must not become an action log or truth source.

The final V2.6 terminal is:

`STANDING_DELEGATED_CONTROLLED_TOPOLOGY_AUTHORITY_RUNTIME_CONSUMED`

and:

`ONE_IDENTITY_AUTONOMOUS_TRIAL_PROVEN`.

## V2.5 active executable revision — controlled-source non-waiting exit paths

V2.5 admits
`CONTROLLED_SOURCE_RESELECTION_PROVISIONING_AND_SLICE_FEASIBILITY_V1`
inside this existing Program. It does not create a Program, Planner, Runtime,
registry, queue, watcher, scheduler, Authority owner, evidence store or truth
source.

The existing owners must expose one compact
`CONTROLLED_SOURCE_TOPOLOGY_CAPABILITY_MAP` covering:

```text
existing empty egress rebind
existing egress-draft dedicated provisioning
logically isolated slice on an occupied production egress
```

Every option consumes current registry, assignment, Matrix, quality, capacity,
route/policy-table, egress-draft, verification, rollback and Authority truth.
It is hard-rejected when ordinary users can share its induced failure, the
baseline cannot be verified, capacity has no owner, rollback is not bounded,
or private credentials would have to be disclosed.

The existing `v7-egress-set-state` owner provides an exact reversible
controlled-source reservation contract. Reservation is allowed only on an
empty source and is bound by source-line CAS fingerprint, reservation ID,
expiry, certification group and an exact confirmation. It fences ordinary
Planner assignment through the existing `canary_reserved` and
`production_assignment_allowed=false` semantics. Release requires the same
reservation identity, exact current fingerprint, zero assigned users and the
owner-created restore backup. Neither mode moves a user or changes a route.

The preferred current engineering path is an empty healthy existing egress
when it has owner-backed capacity for the full certification pool and the
reservation/release contract is ready. A ready existing egress draft remains
the dedicated-source fallback. A separate per-user policy table alone is not
a controlled slice: slice feasibility requires an independently failing and
reversible peer/interface/runtime boundary.

The topology recommendation may prepare one exact one-identity production
preflight. It must not reuse or re-request Tier-48 capability/campaign
approval. When the source identity changes, the exact external boundary is:

`REBIND_CONTROLLED_CERTIFICATION_SOURCE`.

That independent decision changes only the source binding admitted for the
manifest-bound trial. It does not authorize reservation, assignment,
controlled failure, Candidate, Packet, lease, restore barrier, apply, rollback
or campaign execution by implication. Every later effect still requires its
existing owner, fresh gates and exact packet-bound Authority.

The request and decision lifecycle reuses the existing append-only
`admin_core/operator_execution.py` Authority audit:

```text
fresh current topology map and one-identity manifest
-> v7.controlled-source-topology-authority-request.v1
-> exactly one registered request or one reused active semantic request
-> material preflight change atomically supersedes the stale pending request
-> exact APPROVE_<manifest action> or DECLINE with actor provenance
-> CPS/OMP successor
```

The request is bound to the current campaign ID/hash, exact old and proposed
source, one certification identity, identity-set and manifest fingerprints,
zero ordinary assignment/route delta, capacity reservation, concurrency one,
verification, rollback, lease/expiry, Packet and restore-barrier requirements.
It neither repeats Tier-48 approval nor materializes the topology. Duplicate
or conflicting decisions fail closed. A supersession is an owner-backed
preflight invalidation, not an Authority decision: it is appended through the
same audit, names the stale and replacement request hashes, and makes the stale
request permanently non-decidable. It is legal only when the current compact
map proves a different manifest/action; identical semantic preflights reuse the
active request without another write. Approval publishes only a fresh
Candidate/Packet/lease/restore-barrier preflight successor; packet-bound
Operational Authority still precedes every production mutation.

If an exact option is declined, the same derived map excludes that exact
resource for the current decision lineage and evaluates the remaining safe
options. It must not recreate the declined semantic request or return to
source `1` recovery while another owner-backed option remains.

The legal completion before that decision is:

`CONTROLLED_SOURCE_NON_WAITING_EXIT_PATH_PRODUCTION_PREFLIGHT_READY`.

The legal post-trial completion is:

`CONTROLLED_SOURCE_NON_WAITING_EXIT_PATH_RUNTIME_PROVEN`.

`WAIT_FOR_SOURCE_1_RECOVERY` is not a legal Program frontier while a safe
rebind or dedicated-source option remains feasible.

## V2.4 active executable revision — dynamic controlled-target discovery and reselection

V2.4 consumes
`DYNAMIC_CONTROLLED_TARGET_DISCOVERY_RESELECTION_AND_ALLOCATION_V1` inside the
existing Program. It creates no Program, Mission group, Planner, Runtime,
target registry, queue, watcher, scheduler, Authority owner, evidence store or
truth source.

The controlled campaign must use three different existing-owner projections:

```text
campaign Authority
-> exact approved target envelope or exact-target restriction

fresh Matrix + registry + quality + capacity + assignment truth
-> compact CONTROLLED_TARGET_INVENTORY_SNAPSHOT

fresh Planner decision
-> immutable exact target allocation for one Candidate/Packet/lease
```

Inventory contains every current owner-backed egress, including ordinary,
reserved, controlled-only and ineligible channels. Presence never implies
eligibility. Admission and ranking must consume role/reservation,
controlled-use permission, ordinary-user occupancy, fresh service truth,
current/5m/1h stability, explicit registry and policy capacity, required
reserve, verification, rollback/containment and correlation domain. Missing
mandatory truth fails closed for that target.

ID order is a deterministic final tie-breaker only. It is never a target
selection rule. The ranking order is:

```text
full mandatory eligibility
-> current-stage feasibility
-> campaign-completion feasibility
-> stability and service health
-> free capacity after reserve
-> existing Planner score and risk
-> ID tie-break only
```

Current-stage and campaign-completion feasibility are distinct. A target may
admit Stage 5 while leaving a precise Stage 10/25/48 reselection residual.
Every stage obtains a fresh inventory and allocation. An issued Packet keeps
its immutable target or target set.

Material Matrix, inventory, role, reservation, controlled-use, occupancy,
quality, capacity, reserve, correlation-domain, source-scope or campaign-stage
change invalidates only the short-lived allocation, not the campaign.
Unchanged semantic fingerprints produce
`TARGET_SET_UNCHANGED_REUSE_CURRENT_DECISION` and no OMP churn.

The current campaign Authority is exact-target Authority. It must never be
silently widened into envelope Authority. If a different eligible target or
target set ranks first, the only legal external request is a narrow
`REBIND_CONTROLLED_CAMPAIGN_TARGET`; existing Tier-48 capability approval,
pool, completed stages and campaign lineage are preserved. No Candidate,
Packet, lease or production effect is created before that exact decision.

The existing governed movement path already supports immutable multi-target
selected moves, per-member receipts, per-target verification and aggregate
circuit breaking. Controlled-campaign reuse additionally requires a
correlation-distinct allocation, per-target capacity reservation and separate
Authority when the current exact-target contract does not permit multiple
targets. Generic multi-target engineering evidence never activates this path
by implication.

The exact legal live outcomes are:

```text
CURRENT_EXACT_TARGET_VALID
BETTER_TARGET_SELECTED_INSIDE_APPROVED_ENVELOPE
EXACT_TARGET_REBIND_AUTHORITY_REQUIRED
MULTI_TARGET_ALLOCATION_READY
MULTI_TARGET_EXECUTION_AUTHORITY_REQUIRED
NO_CURRENT_TARGET_CAPACITY_WITH_EXACT_OWNER_BOUNDARY
```

The final outcome is not a generic `REAL_WORLD_LIMIT`. It must list every
target and exclusion reason, name the responsible existing owner and retain
automatic re-entry on a material target-set fingerprint change. Ordinary
customers must never be reassigned or used as certification subjects merely
to make a target eligible.

## V2.3 active executable revision — controlled-source isolation admission

V2.3 extends the existing V2.2 execution map without creating a Program,
Mission, owner, registry, Planner, Runtime, Authority system, queue, watcher
or campaign path.

A deliberate controlled-source condition is legal only when the current route
and registry owners prove that the exact source contains zero enabled
non-certification users. Certification-user count alone is not pool readiness.

```text
exact source
-> current enabled assignments
-> certification-only classification for every assigned identity
-> zero non-certification users
-> controlled-source isolation PASS
```

An approval hash-bound to a source that fails this invariant remains valid only
for its exact source and cannot be consumed for provisioning, assignment,
degradation or campaign execution. OMP must fail closed, preserve zero
production effects, select only an already-existing empty eligible source
candidate through the same registry/assignment owners, and form one fresh
independently decidable exact request. Authority never transfers between
source identities by implication.

## V2.2 retained executable revision — exact M8/M9/M10 ownership and Authority-decision consumption

V2.2 is the retained executable base under V2.3. It extends the existing V2.1
Program and owners; it creates no Program, Mission, Authority owner, policy
owner, Planner, Runtime, registry, evidence store, queue, watcher, scheduler or
execution path.

The exact Mission sequence is:

```text
T48-M8 controlled plan and safe-cohort preparation
-> T48-M9 progressive controlled production proof
-> T48-M10 verification, consumption and reconciliation
-> existing ordinary Runtime decision consumer
```

Each Mission must publish and prove consumption of its existing successor. A
Mission must not absorb its successor's scope. Safe owner-backed transitions
continue without a Codex or operator continuation message.

The campaign advances only to the highest currently legal and evidence-valid
stage. An exact owner-backed live blocker preserves completed lower-stage
evidence and produces a durable partial terminal; it must not be bypassed to
force scope 48.

The coordinated controlled-substrate request lifecycle is owned by the
existing append-only `admin_core/operator_execution.py` Authority audit:

```text
exact request
-> exact independent APPROVE or DECLINE
-> exactly-once decision record with actor provenance
-> existing T48-M8 successor
```

An expiry-only replacement is the same semantic request, not a second
Authority expansion. It must name the superseded request ID/hash, preserve one
semantic fingerprint, never coexist as a second active request and change only
request identity/timestamps/expiry/supersession metadata.

Generic movement evidence is reusable only claim-by-claim through its original
owner, provenance and fingerprint. A generic cohort number never proves
Service Failure detection, incident binding, Planner selection, controlled
source response, scenario-specific containment, Outcome consumption or the
controlled-production maximum.

The canonical delegated/admin final Safe Mode remains `OPEN`. Cohort breaker
health is represented separately: success requires `tripped=false` after
verified reset/re-arm; a contained failure preserves `tripped=true` and stops
remaining forward mutations until owner-backed reset/re-arm.

After T48-M9 the existing ordinary Runtime decision consumer must consume one
V2.1 verdict. A first future genuine ordinary transaction is owned by the
ordinary event-driven incident lane and is not an M8/M9/M10 completion
condition. It must never be manufactured merely to close this Program.

## V2.1 retained executable base — Tier-48 controlled campaign and ordinary Runtime reconciliation

V2.1 supplies the retained executable contracts below. V2.0 and earlier
revisions remain historical owner-backed evidence and implementation context.
They must not dispatch duplicate Missions, repeat valid production movements
or override V2.2 or fresh CPS truth.

V2.1 continues
`V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1` through its existing
`PRODUCT_EVOLUTION_FRONTIER`. It creates no new Program, Mission group,
Planner, Runtime, registry, queue, watcher, scheduler, executor, Authority
owner, certification owner, evidence store or truth owner.

The admitted residual is:

`PROJECT_WIDE_GENERIC_USER_ROUTE_MOVEMENT_CERTIFICATION_TO_TIER_48`.

Its purpose is to:

1. reconcile and normalize the already-existing project-wide generic movement
   primitive;
2. selectively close only its exact engineering guarantee gaps through scope
   48;
3. bind existing scenario adapters to that primitive without duplicating the
   movement ladder;
4. qualify the Service Failure adapter through scope 48;
5. obtain exactly one independent existing-owner Authority decision for the
   resulting Service Failure action class;
6. after Authority and Runtime activation, prove the Service Failure adapter
   bridge with real controlled bounded-cohort production outcomes through
   scope 48;
7. consume Outcome, Replay and Learning and return the result to the existing
   incident, capability, CPS and OMP owners.

### V2.1 current owner-backed baseline

The following are discovery inputs, not permanent assumptions. Mission
`T48-M0` must re-read their current owners and classify each item as
`VALID_REUSABLE`, `STALE`, `INVALIDATED`, `MISMATCHED` or `NOT_FOUND` before
work begins:

- real generic governed movement scopes have been recorded at
  `1,2,4,5,10,25,48`;
- generic assignment mutation, route verification, serial cohort execution
  and Outcome closure have evidence through scope `48`;
- generic Packet identity preservation is directly evidenced through scope
  `25`;
- generic rollback apply and replay/duplicate suppression are directly
  evidenced through scope `4`;
- parallel concurrent transactions are evidenced only at `1`;
- `GENERIC_USER_ROUTE_MOVEMENT_PRIMITIVE` already exists as a normalized
  projection;
- Service Failure is engineering-qualified, Authority-approved and
  Runtime-enabled at maximum four users per transaction, concurrency one;
- the Service Failure production-proven action-class scope is lower than its
current engineering/Authority/Runtime scope until a qualifying positive
cohort outcome exists;
- the last owner-backed VLESS active source scope was empty.

No item may be accepted solely because it appears in this document or a
historical report. CPS owns volatile state. Capability, certification,
assignment, Packet, lease, Outcome, Replay, Learning and Authority owners must
provide the current evidence and dependency fingerprints.

### V2.1 controlled/ordinary dual-axis law

Authority ceiling, controlled-certification Runtime, ordinary-production
Runtime, controlled-production proof and ordinary-production proof are
independent owner-backed axes:

```text
AUTHORITY_APPROVED_MAX
CONTROLLED_CERTIFICATION_RUNTIME_MAX
ORDINARY_PRODUCTION_RUNTIME_MAX
CONTROLLED_PRODUCTION_PROVEN_MAX
ORDINARY_PRODUCTION_PROVEN_MAX
```

An Authority maximum must never become an ordinary-production Runtime maximum
by implication. Until the controlled Service Failure outcomes at
`5 -> 10 -> 25 -> 48` are consumed, the current safe projection is:

```text
AUTHORITY_APPROVED_MAX = 48
CONTROLLED_CERTIFICATION_RUNTIME_MAX = 48
ORDINARY_PRODUCTION_RUNTIME_MAX = 4
CONTROLLED_PRODUCTION_PROVEN_MAX = 0
ORDINARY_PRODUCTION_PROVEN_MAX = 4
```

The exact executor must prove `CONTROLLED_CERTIFICATION_CONTEXT` from the
current controlled-source owner and every immutable cohort member's
certification-only identity. Missing or mixed context selects the ordinary
maximum and fails closed; the contract is neither rewritten nor silently
expanded.

### V2.1 coordinated substrate Authority law

If the existing pool cannot reach 48 through already-authorized owners, one
existing-owner Authority package may coordinate these explicitly independent
subscopes:

1. dedicated identity provisioning;
2. certification-only classification and assignment;
3. deliberate controlled-source condition and restoration;
4. progressive `5 -> 10 -> 25 -> 48` campaign execution.

Approval is non-transitive. Every admitted subscope must be named by the exact
decision; one scope never implicitly grants another. The request covers the
whole Tier-48 substrate once, not one request per campaign stage.

### V2.1 inter-stage reset and re-arm law

Every successful or safely contained stage must close through:

```text
stage Outcome
-> source restoration
-> certification identity baseline restoration
-> assignment verification
-> new incident generation
-> fresh controlled condition
-> next stage
```

Setup, reset and cleanup are not certification evidence. Each stage requires a
fresh Situation, cohort, Candidate, Packet and lease. The effective cohort is
the minimum of every current mandatory owner-backed bound; a missing,
`UNKNOWN`, zero or negative mandatory bound is `STOP_SAFE`.

Full identity lists remain only in existing registry, Packet and Outcome
owners. CPS stores counts, fingerprints and lineage pointers.

### V2.1 ordinary Runtime decision law

Controlled proof through 48 does not automatically activate ordinary Tier 48.
After T48-M9 the existing independent Authority/Runtime owner must consume one
verdict:

- `ACTIVATE_ORDINARY_TIER_48`;
- `HOLD_ORDINARY_TIER_4`;
- `RECOMMEND_NARROW_SCOPE`;
- `DEMOTE_OR_FREEZE`;
- `INSUFFICIENT_EVIDENCE`.

The successful Program terminal requires that verdict to be consumed, not that
Tier 48 necessarily be activated. This extends the same Program completion
contract and creates no new Program or Authority owner.

### V2.1 no-progress law

Three identical engineering-owned no-progress generations route the smallest
producer-consumer repair automatically. An unchanged Authority or external
resource fingerprint remains one durable boundary and must not generate
repeated requests, reports, deploys or heartbeat churn.

### V2.1 global execution law

All engineering-owned gaps discovered by V2.1 continue automatically through
existing owners:

```text
discover exact cause
-> reuse existing capability
-> implement the smallest residual
-> focused verification
-> safe deploy when Runtime code changed
-> real non-test caller and consumer
-> affected replay
-> truth and convergence
-> atomic CPS/OMP projection
-> residual recomputation
-> durable successor
-> event-driven Continue OMP
```

Do not return to the operator for owner discovery, code gaps, missing
producer-consumer links, stale fixtures, test failures, replay gaps, Polygon
scenario gaps, safely repairable deploy issues, CPS/OMP reconciliation or
canonical knowledge updates.

Stop only at:

- one exact independent Authority decision;
- an exact external-owner/access input that cannot be produced by existing
  safe engineering owners;
- an irreducible physical safety boundary.

A report, test, commit, deploy, replay, Mission completion, empty historical
incident, intermediate certification result or heartbeat boundary is not a
Program terminal while a safe engineering successor exists.

### V2.1 knowledge reuse and invalidation law

Before every audit, test, certification lookup, Polygon campaign or
implementation:

1. locate the existing canonical truth object;
2. identify its owner and evidence fingerprint;
3. read its dependency and implementation fingerprints;
4. evaluate only declared invalidation triggers;
5. when no trigger occurred, emit `RESULT_REUSED_VALID`;
6. do not repeat the corresponding real movement, certification or broad test
   campaign;
7. selectively revalidate only the changed property and its consumers.

The following are not invalidation triggers by themselves:

- a new Codex context or report;
- a new incident, Candidate or Packet;
- Packet or lease expiry;
- Runtime restart;
- CPS compaction;
- a different business reason for using the same generic movement primitive.

Real movements at `1,2,4,5,10,25,48` must not be repeated merely to recreate
generic evidence.

### V2.1 evidence and state separation law

The following projections are independent and must never be collapsed:

```text
GENERIC_MOVEMENT_PRODUCTION_EVIDENCE_REUSED_MAX
GENERIC_MOVEMENT_ENGINEERING_CERTIFIED_MAX
SERVICE_FAILURE_ADAPTER_ENGINEERING_COMPATIBLE_MAX
SERVICE_FAILURE_ADAPTER_CONTROLLED_PRODUCTION_PROVEN_MAX
SERVICE_FAILURE_AUTHORITY_APPROVED_MAX
SERVICE_FAILURE_RUNTIME_ENABLED_MAX
CURRENT_LIVE_CAPACITY_SAFE_MAX
```

Generic production evidence proves the shared movement primitive. Service
Failure controlled-production evidence proves only the scenario bridge:

```text
incident
-> exact source/unresolved scope
-> exact bounded cohort
-> safe target and capacity
-> generic movement primitive
-> scenario verification/containment
-> incident scope reconciliation
```

Polygon, deterministic replay, fault injection, shadow execution and process
simulation are Engineering Evidence. They cannot become a production Outcome,
Natural L8 evidence, Authority, Runtime activation or Production Maturity.

### V2.1 numeric scope and action-class identity law

`Tier`, Authority class, action class, `max_users_per_transaction` and observed
cohort size are different fields. A historical class alias or a budget such as
`50` must not silently stand for exact scope `48`.

Every projection and contract must carry:

- exact numeric maximum users per transaction;
- exact maximum concurrent transactions;
- action class and failure class;
- engineering-certified maximum;
- Authority-approved maximum;
- Runtime-enabled maximum;
- currently selected cohort count and fingerprint.

An increased policy number alone is not qualification, Authority or Runtime
enablement.

## V2.1 executable Mission map

### T48-M0 — Fresh owner and evidence reconciliation

Read fresh CPS, OMP, the current program file, generic movement capability
projection, assignment owner, Packet/lease owners, verification,
rollback/containment, Outcome, Replay, Learning, Polygon, controlled-production
and Authority owners.

Produce an exact matrix for scopes `1,2,4,5,10,25,48` covering:

- assignment mutation;
- exact cohort identity;
- Packet identity and generation;
- lease identity;
- exact-once and duplicate suppression;
- partial-scope selection;
- partial-apply recovery;
- route and generic-result verification;
- rollback apply or accepted stronger containment;
- circuit breaker and final safe mode;
- restart recovery and stale-writer rejection;
- Outcome, Replay and Learning;
- serial cohort execution;
- parallel transaction maximum.

Do not infer absence from a missing report field. Inspect current
implementation behavior and immutable owner artifacts first.

Completion:

`TIER48_CURRENT_OWNER_EVIDENCE_AND_EXACT_RESIDUAL_RECONCILED`.

### T48-M1 — Normalize the existing generic movement primitive

Normalize, do not recreate, `GENERIC_USER_ROUTE_MOVEMENT_PRIMITIVE` under the
existing capability and certification owners.

The primitive accepts:

- exact user/cohort identity and fingerprint;
- exact source and target assignments;
- maximum users and concurrency;
- Candidate, Packet generation and lease;
- capacity contract;
- verification contract;
- rollback/containment contract;
- cooldown, anti-flap and final safe-mode contract.

It owns or delegates through existing owners:

```text
cohort input
-> Candidate
-> Packet
-> lease
-> assignment mutation
-> route verification
-> generic result verification
-> rollback/containment
-> Outcome
-> Replay
-> Learning
-> terminal
```

It must not decide why a movement is required, whether a channel failed, which
users belong to a scenario, which target is preferable or whether Authority
permits the action. Those remain scenario-adapter, Planner and policy
responsibilities.

Publish one machine-readable projection through the existing owner:

```text
GENERIC_MOVEMENT_PRIMITIVE_ID
IMPLEMENTATION_OWNER
EXECUTOR_OWNER
ASSIGNMENT_OWNER
PACKET_OWNER
LEASE_OWNER
VERIFICATION_OWNER
ROLLBACK_CONTAINMENT_OWNER
OUTCOME_OWNER
REPLAY_OWNER
LEARNING_OWNER

TECHNICALLY_IMPLEMENTED_MAX_SCOPE
PRODUCTION_PROVEN_MAX_SCOPE
ENGINEERING_CERTIFIED_MAX_SCOPE
PACKET_IDENTITY_PROVEN_MAX_SCOPE
REPLAY_DUPLICATE_PROVEN_MAX_SCOPE
ROLLBACK_OR_CONTAINMENT_PROVEN_MAX_SCOPE
PARTIAL_APPLY_RECOVERY_MAX_SCOPE
RESTART_RECOVERY_MAX_SCOPE
SERIAL_COHORT_MAX_SCOPE
PARALLEL_TRANSACTION_MAXIMUM

EVIDENCE_FINGERPRINTS
DEPENDENCY_FINGERPRINTS
IMPLEMENTATION_FINGERPRINTS
INVALIDATION_TRIGGERS
REUSE_RULE
```

Completion:

`GENERIC_MOVEMENT_PRIMITIVE_CURRENT_CONTRACT_NORMALIZED`.

### T48-M2 — Canonical adaptive cohort selection contract

Reuse the existing Planner, capacity, policy, incident and Authority gates.
Do not create a cohort optimizer or second Planner.

For every fresh incident generation, calculate independently:

```text
incident_required_scope
eligible_source_scope
generic_certified_scope
adapter_compatible_scope
capacity_safe_scope
authority_safe_scope
runtime_safe_scope
verification_safe_scope
rollback_containment_safe_scope
circuit_breaker_safe_scope
request_safe_scope
```

Each bound must contain:

```text
owner
value
fingerprint
measured_at
expires_at or freshness rule
reason
```

`UNKNOWN`, stale or owner-mismatched status for any mandatory bound is
`STOP_SAFE`, never an ignored value.

The numeric limit is:

```text
effective_cohort_limit =
min(all current proven positive mandatory bounds)
```

The exact cohort is selected from:

```text
eligible users
INTERSECT current source scope
INTERSECT unresolved incident scope
INTERSECT current policy scope
INTERSECT target-compatible scope
```

Selection must also satisfy the existing load/capacity owner:

```text
effective_cohort_load
<= target_available_load_after_required_reserve
```

Per-user load may differ. Capacity-safe selection must therefore use the
existing target-capacity and reserve contract, not only a user count.

The durable obligation, Candidate preparation and Runtime caller must expose
the same:

- incident-required count and fingerprint;
- eligible set fingerprint;
- exact selected cohort fingerprint;
- every bound and limiting bound;
- effective cohort count and load;
- selected target allocation;
- exclusion reasons;
- next-tier blocker.

The current placeholder behavior in which
`smallest_necessary_cohort` and `maximum_capacity_safe_cohort` merely mirror an
already chosen list, or `effective_cohort` remains zero despite an actionable
selection, is an exact existing-owner engineering residual.

For a hard-failed source, the overall protection intent may cover the full
unresolved scope while one bounded transaction remains limited by
`effective_cohort_limit`. `max_users_per_transaction` must not become
`max_transactions_per_incident=1`.

Completion:

`ADAPTIVE_COUNT_LOAD_AND_EXACT_COHORT_SELECTION_CONSUMED`.

### T48-M3 — Tier-48 generic engineering guarantee closure through existing evidence and Polygon

Close each exact missing generic guarantee through the smallest safe method,
in this order:

1. reusable historical production evidence;
2. deterministic replay;
3. Permanent Polygon;
4. controlled fault injection;
5. process crash and concurrency simulation;
6. minimal repair of the existing responsible owner;
7. selective controlled production only when the property cannot be proven
   otherwise and current Authority already permits it.

Mandatory Polygon and replay coverage includes:

#### Cohort identity and Packet integrity

- 48 selected users and exact cohort fingerprint;
- reordered input;
- one removed member;
- one added unauthorized member;
- stale incident generation;
- stale or duplicate Packet;
- expired lease;
- mixed source or target cohort.

#### Partial apply and containment

For scopes `5,10,25,48`, inject failure:

- before first mutation;
- after member one;
- at midpoint;
- before the final member;
- after all writes but before verification;
- during verification;
- during rollback;
- after rollback but before Outcome.

Prove exact applied, unapplied and failed sets; no user outside the cohort;
safe preservation of successful members; rollback or bounded containment;
circuit breaker; final safe mode; and no retry with the same Packet.

#### Crash and restart recovery

Inject process termination:

- after Candidate creation;
- after Packet creation;
- after lease acquisition;
- after partial mutation;
- before scope reconciliation;
- after Outcome before Replay;
- after CPS projection before receipt;
- after receipt before successor acknowledgement.

Prove checkpoint recovery, exactly one legal transition and no duplicate user
movement.

#### Duplicate and stale-consumer rejection

At `5,10,25,48`, cover duplicate Event, Candidate, Packet, Matrix wake and
heartbeat; concurrent consumers; and a stale writer following a newer
generation.

#### Capacity and verification

At `5,10,25,48`, cover sufficient capacity, exact reserve boundary, reserve
violation, capacity loss after planning, target degradation during apply,
aggregate failure, one-member exception, multi-member exception and temporal
regression.

A verified bounded containment contract may satisfy the generic safety
requirement when the existing certification owner proves it equal to or
stronger than full rollback. Do not manufacture Natural L8 or relabel Polygon
evidence as production evidence.

Completion requires:

```text
GENERIC_MOVEMENT_PRODUCTION_EVIDENCE_REUSED_MAX = 48
GENERIC_MOVEMENT_ENGINEERING_CERTIFIED_MAX = 48
SERIAL_COHORT_MAX_SCOPE = 48
PACKET_IDENTITY_PROVEN_MAX_SCOPE = 48
REPLAY_DUPLICATE_PROVEN_MAX_SCOPE = 48
ROLLBACK_OR_CONTAINMENT_PROVEN_MAX_SCOPE = 48
PARTIAL_APPLY_RECOVERY_MAX_SCOPE = 48
RESTART_RECOVERY_MAX_SCOPE = 48
PARALLEL_TRANSACTION_MAXIMUM = 1
```

Completion:

`GENERIC_MOVEMENT_ENGINEERING_CERTIFIED_AND_PRODUCTION_EVIDENCE_REUSED_TO_48`.

### T48-M4 — Bounded cohort transaction semantics

The multi-user execution unit is:

`BOUNDED_COHORT_TRANSACTION`.

It is logically one transaction but must not be described as physically atomic
when member mutations are applied serially.

One transaction has:

- one immutable cohort fingerprint;
- one Candidate;
- one Packet and generation;
- one lease;
- one incident/source/target binding;
- per-member subreceipts;
- exact applied, unapplied and failed sets;
- per-member verification;
- aggregate verification;
- circuit breaker;
- partial-apply rollback or containment;
- one final safe-mode decision;
- one cohort Outcome;
- one Replay/Learning lineage;
- one successor.

Crash recovery resumes from the exact owner-backed checkpoint. Packet reuse is
forbidden. Four, ten or 48 internal member operations must not create four, ten
or 48 OMP, Authority or Codex cycles.

`max_concurrent_transactions=1` remains unchanged. Internal serial member
application is not evidence of parallel transaction support and is not a
failure to perform a multi-user cohort transaction.

Completion:

`BOUNDED_COHORT_TRANSACTION_EXACTLY_ONCE_AND_PARTIAL_APPLY_SAFE`.

### T48-M5 — Project-wide adapter inheritance and Service Failure bridge

Discover existing scenario adapters that call, or should call, the same
generic primitive, including Service Failure, planned maintenance,
capacity/load balancing, provider degradation, manual governed recovery and
planned route/provider migration.

Do not create duplicate executors or rerun the generic tier ladder for an
adapter.

For every discovered real adapter project:

```text
ADAPTER_ID
SCENARIO_OWNER
GENERIC_PRIMITIVE_ID
GENERIC_MAX_REUSED
ADAPTER_COMPATIBLE_MAX
SOURCE_SCOPE_CONTRACT
TARGET_SELECTION_CONTRACT
CAPACITY_CONTRACT
SCENARIO_VERIFICATION_DELTA
SCENARIO_ROLLBACK_CONTAINMENT_DELTA
START_CONDITIONS
STOP_CONDITIONS
AUTHORITY_SCOPE
RUNTIME_ENABLED_SCOPE
EXACT_RESIDUAL
```

An unimplemented or hypothetical adapter must not block Service Failure
qualification. Record its exact residual through the existing capability owner
and continue with the active Service Failure bridge.

For Service Failure, reuse the corrected obligation, incident, source-scope and
all-member cohort binding. Close only scenario-specific deltas through
`5,10,25,48`:

- failed-source and unresolved-scope membership;
- target suitability and capacity reserve;
- cohort service verification;
- partial-apply rollback/containment delta;
- Matrix successor and cumulative incident scope reconciliation.

Use Polygon, replay and fault injection for safely simulatable properties. Do
not wait for a new natural outage to close engineering-only requirements. Do
not move ordinary production users merely to manufacture evidence.

Completion:

`PROJECT_WIDE_ADAPTER_INHERITANCE_BOUND`

and:

`SERVICE_FAILURE_ADAPTER_ENGINEERING_COMPATIBLE_TO_48`.

### T48-M6 — Canonical capability, CPS and OMP projection

Publish one compact projection through existing capability, certification, CPS
and OMP owners:

```text
GENERIC_MOVEMENT_PRODUCTION_EVIDENCE_REUSED_MAX
GENERIC_MOVEMENT_ENGINEERING_CERTIFIED_MAX

ADAPTERS:
  adapter identity
  engineering-compatible maximum
  controlled-production-proven maximum
  Authority-approved maximum
  Runtime-enabled maximum
  current live capacity-safe maximum
  exact residual
```

Absence of Authority must not be reported as absence of technical capability.
Absence of a current incident must not invalidate reusable engineering
certification. Valid knowledge with no declared invalidation trigger must be
consumed without another broad audit or movement campaign.

Completion:

`TIER48_GENERIC_AND_ADAPTER_CAPABILITY_TRUTH_ATOMICALLY_CONSUMED`.

### T48-M7 — One independent Authority and Runtime activation decision

After `T48-M3` through `T48-M6` are owner-backed, re-read existing Authority.
If a still-valid exact contract covers Service Failure maximum 48, concurrency
one and every required safety term, consume it as
`EXISTING_AUTHORITY_REUSED`.

Otherwise produce exactly one independent existing-owner request:

`EXACT_TIER48_SERVICE_FAILURE_AUTHORITY_DECISION_REQUIRED`.

The request binds:

- generic engineering-certified maximum and reusable production evidence;
- Service Failure engineering-compatible maximum;
- exact maximum users per bounded cohort transaction `48`;
- maximum concurrent transactions `1`;
- exact action and failure classes;
- source and target families selected only by the fresh existing Planner;
- live target capacity and reserve;
- Candidate, Packet, lease and no-reuse law;
- immutable cohort and per-member subreceipts;
- per-member and aggregate verification;
- partial-apply circuit breaker;
- rollback/containment and final safe mode;
- cooldown and anti-flap;
- expiry, freeze, demotion and kill conditions;
- evidence and dependency fingerprints;
- exact policy delta;
- `APPROVE` or `DECLINE`.

No Engineering result may implicitly become Operational Authority. Do not
activate maximum 48 before the independent decision.

After approval, the existing Authority, policy, CPS, OMP and Runtime owners
must atomically expose the same exact maximum and contract identity. Activation
alone is not Service Failure controlled-production certification.

Completion:

`SERVICE_FAILURE_TIER48_AUTHORITY_DECIDED`

and:

`SERVICE_FAILURE_TIER48_RUNTIME_ACTIVATION_DECIDED`.

### T48-M8 — Polygon-prepared controlled production cohort

After Authority and Runtime activation, the Permanent Polygon identifies the
exact missing Service Failure adapter production cells and prepares one
controlled certification plan through existing owners.

Polygon may:

- choose a reproducible controlled Service Failure condition;
- reuse an existing test/certification cohort;
- verify all engineering invariants before production admission;
- prepare fresh Situation, Decision, exact cohorts, targets, capacity
  contracts, verification and rollback/containment;
- hand the plan to the existing controlled-production certification owner.

Polygon may not:

- create a production Outcome itself;
- move ordinary customers solely to manufacture evidence;
- grant Authority;
- bypass Packet, lease, restore-barrier, capacity, verification or containment
  gates;
- relabel controlled evidence as Natural L8.

If the approved controlled source is already the exact isolated failed
condition and an existing `EXECUTION_ONLY` Polygon egress is the only healthy
isolated target, reuse that egress only through the existing coordinated
controlled-certification Authority owner. The exact request must bind source,
target, current pool fingerprint, target reservation owner, zero-user state,
fresh health/capacity gates and the full campaign scope. This exception never
makes the target eligible for ordinary autoswitch, rebalance or production
assignment. Without the exact approved request, the ordinary Planner continues
to reject the target.

If no current certification cohort exists, first determine whether it can be
safely created through the existing Polygon, test-user and certification
owners without moving ordinary customers, acquiring a new external resource or
expanding Authority. When safe and already owner-authorized, create it and
continue automatically.

Only when this is impossible may the Program emit:

`ENGINEERING_COMPLETE_AWAITING_EXACT_CONTROLLED_PRODUCTION_POOL_OR_AUTHORITY`.

That terminal must name the exact missing pool/input, why existing owners
cannot create it safely, the responsible existing owner, the requested input
and the automatic re-entry condition.

Completion:

`CONTROLLED_SERVICE_FAILURE_CERTIFICATION_PLAN_AND_SAFE_COHORT_READY`.

### T48-M9 — Progressive controlled Service Failure adapter proof

Execute one owner-authorized controlled certification plan:

```text
controlled Service Failure condition
-> bounded cohort 5
-> verification and incident reconciliation
-> bounded cohort 10
-> verification and incident reconciliation
-> bounded cohort 25
-> verification and incident reconciliation
-> bounded cohort 48
-> verification and incident reconciliation
-> Outcome
-> Replay
-> Learning
-> capability/CPS/OMP consumption
```

This progression does not repeat generic assignment, exact-once or route
mutation certification. It validates only the Service Failure scenario bridge.

Every next cohort starts automatically after the previous cohort reaches an
owner-backed success terminal and all fresh live gates pass. No new Codex
prompt or Authority decision is required inside the already-approved scope.

Each step requires:

- a fresh incident/scenario generation;
- a fresh exact cohort, Candidate, Packet and lease;
- current target health, capacity and reserve;
- current policy, cooldown and anti-flap;
- per-member and aggregate verification;
- real verifier-driven rollback or accepted containment when triggered;
- one cohort Outcome and incident scope update;
- affected Replay and Learning consumption;
- circuit-breaker stop before the next cohort on any unsafe result.

Do not directly invoke rollback to manufacture a terminal. Do not reuse a
Packet, lease, cohort identity, Outcome or incident generation.

If current safe capacity or an existing controlled cohort is smaller than the
next step, preserve completed lower-step evidence and emit the exact
owner-backed re-entry condition. Do not downgrade engineering compatibility or
repeat completed steps.

Completion:

`SERVICE_FAILURE_CONTROLLED_PRODUCTION_COHORT_OUTCOMES_CONSUMED_THROUGH_48`.

### T48-M10 — Automatic continuation, verification and final closure

Every non-terminal result follows:

```text
verified output
-> existing OMP consumer
-> atomic CPS projection
-> residual recomputation
-> one durable successor
-> one existing event-driven consumer
-> next safe Mission
```

Heartbeat is fallback only. After three unchanged no-progress generations,
record the unchanged input fingerprint, exact blocked property, last
responsible producer-consumer link and smallest repair; execute the repair
automatically when it is engineering-owned.

For every changed owner:

- perform semantic topology discovery;
- run focused tests and affected deterministic replay;
- run only the affected Tier-48 Polygon/fault cells;
- verify cross-process exact-once and forbidden effects;
- commit and push owned changes;
- use `tools/v7-safe-deploy` only when Runtime files changed and its manifest is
  exact;
- prove a real non-test caller and consumer;
- run truth and convergence;
- reconcile local, GitHub and production identities.

Batch logically related owner changes into one bounded verification and deploy
unit. Do not create report/deploy churn after every individual scenario.
Reports are historical evidence only. Durable knowledge and evidence
fingerprints belong to their existing canonical owners.

## V2.1 production-effects boundaries

| Mission | Production effects |
| --- | --- |
| `T48-M0`–`T48-M6` | none; discovery, reuse, implementation, replay, Polygon and certification projection only |
| `T48-M7` | Authority request/decision and exact Runtime activation only through existing independent owners; no user movement |
| `T48-M8` | controlled-plan and safe-cohort preparation only; no production Outcome may be fabricated |
| `T48-M9` | bounded production cohort actions only through the active exact Authority contract and every fresh live gate |
| `T48-M10` | verification/replay only; no additional action except a separately owner-authorized affected replay |

At every phase, forbidden unless explicitly admitted by the current exact
owner-backed contract:

- routing mutation or user movement;
- Packet execution;
- restore-barrier write;
- rollback apply;
- Authority expansion;
- concurrency increase;
- self-expansion;
- Production Maturity change;
- ordinary-customer use solely for certification.

## V2.1 final completion contract

The successful Program terminal is:

```text
GENERIC_MOVEMENT_ENGINEERING_CERTIFIED_TO_48
AND
GENERIC_MOVEMENT_PRODUCTION_EVIDENCE_REUSED_TO_48
AND
PROJECT_WIDE_ADAPTER_INHERITANCE_BOUND
AND
SERVICE_FAILURE_ADAPTER_ENGINEERING_COMPATIBLE_TO_48
AND
SERVICE_FAILURE_TIER48_AUTHORITY_DECIDED
AND
SERVICE_FAILURE_TIER48_RUNTIME_ACTIVATION_DECIDED
AND
SERVICE_FAILURE_CONTROLLED_PRODUCTION_COHORT_OUTCOMES_CONSUMED_THROUGH_48
AND
ORDINARY_PRODUCTION_RUNTIME_DECISION_CONSUMED
```

This terminal proves project-wide generic movement engineering guarantees and
reused generic production evidence through scope 48, plus real controlled
production proof of the Service Failure adapter bridge through scope 48. It
does not claim Natural L8, parallel transaction support above one,
self-expanding Authority, production routing autonomy or increased Production
Maturity.

If the engineering work is complete but no independently admissible controlled
cohort can be created, the only partial terminal is:

`ENGINEERING_COMPLETE_AWAITING_EXACT_CONTROLLED_PRODUCTION_POOL_OR_AUTHORITY`.

It is not Program completion and must retain an exact durable automatic re-entry
condition.

## V1.9 revision record — incident-bound Matrix admission and atomic cohort revalidation

V1.9 closes two existing producer-consumer defects discovered by the first
natural Tier-4 caller. It creates no Program, owner, queue, registry, Planner,
Runtime, certification path or Authority path.

The first post-activation natural Matrix generation reached the existing L3
cohort executor, but its selected moves belonged to ordinary healthy-channel
balancing rather than the current Service Failure obligation. The same
attempt's downstream operation-scoped verifier compared the approved
four-member cohort with a one-member binding. It stopped before apply with
zero movement, but it proved these exact defects:

```text
standing Tier-4 policy
-> generic planner selection not bound to current incident obligation
-> cohort approved from one atomic read
-> downstream revalidation reduced to first member only
-> STOP_SAFE atomic source mismatch
```

The existing owners now enforce:

```text
current durable Service Failure obligation
AND matching OMP consumption
AND fresh capture-only event
AND exact incident/source/scope fingerprint
-> existing planner
-> fresh Candidate/Packet/lease
-> all-member atomic cohort revalidation
```

An empty or unresolved-zero current source scope stops inside the Matrix owner
before invoking the executor. A positive scope may enter the executor only
with the exact obligation, incident, source and scope fingerprint passed by
the Matrix generation and independently re-read from the durable closure and
event owners. Packet lineage carries that causal binding. Every cohort member
is then revalidated from one stable source/snapshot read; no first-member
projection is permitted.

Implementation commits:

- `432fdbbf786b80b2e3f5a1e60efe2139a54b4309` — existing Tier-4 cohort
  execution path and standing-policy binding;
- `038568d4c78b91f108da1f91d154e89f6bdc273e` — exact incident-obligation
  admission plus all-member downstream revalidation.

Production deploy:

- deploy ID:
  `deploy-z8-14-Updatesystem-038568d-20260728T110359`;
- exact changed Runtime files:
  `tools/v7-users-autoswitch`,
  `tools/v7-governed-canary-dry-run-cycle`,
  `tools/v7-service-matrix-refresh-all`,
  `admin_core/operator_execution.py`.

No Matrix command was invoked manually. The first fully post-deploy timer
generation ran from `2026-07-28T04:18:28+00:00` to
`2026-07-28T04:19:46+00:00` and produced:

```text
obligation = sfaob_bbb80ec875743dbf720c8395
source incident = sfinc_79c7265b16283934089d5119f65455dd
source = 1
affected = 0
unresolved = 0
terminal = STOP_SAFE_CURRENT_SOURCE_SCOPE_EMPTY
action_attempted = false
Candidate/Packet/lease = none
restore-barrier write/apply/movement = none
```

The route owner also contains one `current=vless` registry row,
`10.7.0.7`, but it is disabled (`enabled=0`) and therefore is not a member of
the active Service Failure source scope. Current VLESS active affected and
unresolved counts remain zero.

This production result proves the caller and fail-closed empty-scope consumer.
It does not prove a Tier-4 movement outcome. The first genuine positive-scope
incident must still produce fresh Event/Candidate/Packet/lease, per-user and
aggregate verification, circuit-breaker, rollback/no-rollback, Outcome,
Replay, Learning and scope update. Tier 5 remains outside the current
Authority and must not start from this result.

## V1.8 revision record — Tier 4 activated and natural Matrix boundary proven

V1.8 consumes the exact independent decision recorded in V1.7 through the
existing Authority owner. It does not create a Program, owner, queue,
registry, Planner, Runtime, certification path or Authority path.

The active owner-backed contract is:

- contract ID: `sdpc_a3cd9882bf0850010a6e37b5`;
- contract hash:
  `a3cd9882bf0850010a6e37b5e1fbbadcf7e2865fa6002b2fe30a9a2e219a0e25`;
- request ID: `sdpauth_r1_ed99070cd98caa0f054ffb6e`;
- request hash:
  `ed99070cd98caa0f054ffb6e244cf901bde0034a84d0696cd33e5bb1385d820d`;
- policy scope hash:
  `cdd21744e65ad49b69d0a88c9c3df7ee3244766cbdc71bee913bbd2b3c9d4ccb`;
- issued: `2026-07-28T02:06:51.026478+00:00`;
- expires: `2026-08-27T02:06:51.026478+00:00`;
- action class: `channel hard-fail failover`;
- maximum users per transaction: `4`;
- maximum concurrent transactions: `1`;
- source/target: fresh existing-planner safe target only;
- fresh Candidate, Packet and lease required; reuse forbidden;
- live capacity, target-health, cooldown and anti-flap gates required;
- per-user and aggregate verification required;
- rollback or certified no-rollback and cohort circuit breaker required;
- final safe mode: `OPEN`;
- self-expansion: forbidden.

Authority, Runtime, CPS and OMP now independently agree:

| Projection | Current value |
| --- | --- |
| engineering-compatible tier | `Tier 4` |
| Authority-approved tier | `Tier 4` |
| Runtime-enabled tier | `Tier 4`, serial only |
| production-proven action-class tier | `Tier 1`; Tier 4 awaits its first qualifying natural cohort outcome |
| incident frontier | `CURRENT_SOURCE_SCOPE_EMPTY` |
| Product Evolution frontier | `EXACT_TIER_RUNTIME_AUTHORITY_ACTIVATED` |

The existing CPS consumer was extended only to accept an approved tier
transition when the old active request and the new Runtime request differ but
the CPS-preserved pending request preimage exactly matches request ID/hash,
policy scope hash, action class, max users and concurrency. Every other
mismatch remains `STOP_SAFE`.

After activation, no Matrix command was invoked manually. The enabled
`v7-service-matrix-refresh.timer` started the ordinary owner cycle at
`2026-07-28T02:28:48+00:00`. It completed successfully and advanced the VLESS
observation from `2026-07-28T02:13:42.685967+00:00` to
`2026-07-28T02:28:49.259364+00:00`.

The current route-backed VLESS scope is:

```text
affected=0
protected=0
unresolved=0
excluded_or_recovered=0
cumulative packet-bound success lineage=63
```

Therefore the ordinary Matrix owner correctly produced no fresh Candidate,
Packet, lease, target selection, capacity reservation, cohort execution,
verification, rollback/no-rollback, Outcome, Replay or Learning record.
Manufacturing one by moving a user back to VLESS or manually invoking Matrix
is forbidden. The exact legal terminal is:

`CURRENT_SOURCE_SCOPE_EMPTY`.

The durable re-entry remains the existing ordinary Matrix observation. On the
next genuine matching service failure with one or more eligible source users,
the existing planner may select up to four users only if every live gate
passes. That first natural Tier-4 cohort transaction must then produce the
full Event/Candidate/Packet/lease, per-user and aggregate verification,
circuit-breaker, rollback/no-rollback, Outcome, Replay, Learning and updated
scope evidence. It must not repeat the generic 1/2/4/5/10/25/48 ladder.

## V1.7 revision record — adapter bridge consumed and exact Authority handoff

V1.7 records the consumed result of the V1.6 Product Evolution frontier. It
does not create a Program, owner, queue, registry, Planner, Runtime,
certification path or Authority path.

The existing historical evidence owner was reused without repeating the
1/2/4/5/10/25/48 movement ladder. The generic movement evidence fingerprint
remains:

`7ad9511f521e0a906bd0e9dff33de401e9bbf86f4187722d61b27a48c11b7040`.

The existing Service Failure owners were selectively extended and connected:

```text
existing standing-policy Authority audit
-> read-only pending request projection
-> existing autoswitch status owner
-> existing truth-check production caller
-> atomic CPS/OMP consumer
```

The exact engineering result is:

```text
GENERIC_MOVEMENT_CAPABILITY_REUSED
AND
SERVICE_FAILURE_ADAPTER_BRIDGE_QUALIFIED_TO_EXACT_MAXIMUM_TIER
```

The qualified maximum is `Tier 4`, serial execution only. The adapter now
binds the existing incident, exact immutable cohort, fresh Candidate/Packet/
lease identities, existing assignment and route owners, per-user plus
aggregate service verification, cohort circuit breaker, rollback/containment,
Outcome, Replay, Learning and scope reconciliation. Runtime activation did not
change.

The current independent scopes remain:

| Projection | Current value |
| --- | --- |
| generic movement engineering evidence | scopes `1,2,4,5,10,25,48`; serial cohort up to `48` |
| exact Service Failure adapter compatibility | `Tier 4` |
| current Authority-approved tier | `Tier 1` |
| Runtime-enabled tier | `Tier 1`, concurrency `1` |
| current incident lane | `CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN` |
| Product Evolution lane | `EXACT_TIER_AUTHORITY_DECISION_REQUIRED` |

Tiers 5 and above retain exact selective residuals. They require owner-backed
replay/duplicate-suppression evidence above four, partial-apply containment or
rollback evidence above four, and for Tier 48 packet-identity preservation
above 25. These are not grounds to repeat already valid generic movement
certification.

The existing Authority audit owns exactly one pending Tier-4 decision package:

- request: `sdpauth_r1_ed99070cd98caa0f054ffb6e`;
- hash:
  `ed99070cd98caa0f054ffb6e244cf901bde0034a84d0696cd33e5bb1385d820d`;
- expires: `2026-07-28T19:22:36.056237+00:00`;
- requested max users per transaction: `4`;
- max concurrent transactions: `1`;
- action class: `channel hard-fail failover`;
- decision set:
  `APPROVE_STANDING_DELEGATED_OPERATIONAL_POLICY` or `DECLINE`.

This request is a decision input, not Authority. It must not write policy or
activate Runtime unless the existing Authority owner consumes one exact
independent decision while the request remains current. The active Tier-1
Matrix drain remains independent and must not be paused or manually invoked by
Product Evolution work.

## V1.6 revision record — generic movement reuse and adapter qualification

V1.6 extends the existing evidence, CPS, OMP, Matrix, planner, governed
movement, verification, rollback and Learning owners. It creates no Program,
executor, certification system, registry, queue, Runtime or Authority owner.

The revision separates three independently owned limits:

```text
generic movement engineering evidence
service-failure adapter compatibility
current Authority and live safety gates
```

The effective Runtime scope is always:

```text
min(
  generic movement proven scope,
  exact service-failure adapter compatible scope,
  current independently approved Authority scope,
  live target-capacity and verification-safe scope
)
```

Historical movement evidence must be normalized dimension by dimension. A
single maximum is forbidden when different dimensions have different proof:
assignment mutation, route verification, service verification, rollback
applied, certified no-rollback, replay/duplicate suppression, packet identity,
partial-apply recovery, restart recovery, serial cohort size, parallel
transactions, Outcome and Learning must remain separate.

The historical actual scopes are `1, 2, 4, 5, 10, 25, 48`. The four-user
rollback proof is a first-class evidence row; it must not be renamed Tier 5.
The 48-user outcome is an actual 48-user partial-scope selection against a
budget of 50. It is not proof of an exact 50-user execution or of partial-apply
failure recovery.

`GENERIC_USER_ROUTE_MOVEMENT_PRIMITIVE` and
`SERVICE_FAILURE_INCIDENT_DRAIN_ADAPTER` are derived projections inside
existing owners, not new technical or durable objects. The generic projection
may reuse low-level assignment, route verification and governed execution
evidence. Scenario-specific source/target selection, service verification,
capacity and rollback/containment remain adapter obligations.

Engineering compatibility is not Authority. Historical approval, Packet,
lease or action-class scope must never be generalized. Runtime activation
remains owned by the current Authority contract and cannot exceed its
`max_users_per_transaction` or `max_concurrent_transactions`.

Higher engineering compatibility may be calculated immediately, but Runtime
promotion remains evidence-gated and Authority-owned. A recommendation may
name the highest justified ceiling; activation follows the exact approved
tier and uses adaptive waves with fresh live gates after every wave. A real
incident action must be independently justified by service protection and
must never be executed solely to manufacture bridge evidence.

The current legal completion results include:

- `EXACT_TIER_RUNTIME_AUTHORITY_ACTIVATED`;
- `HOLD_CURRENT_TIER_DECISION_CONSUMED`;
- `NARROW_SCOPE_DECISION_CONSUMED`;
- `DECLINE_DECISION_CONSUMED`.

Thus a correct independent decision to retain Tier 1 completes the current
reconciliation generation without pretending that engineering evidence,
Authority or Runtime expanded.

## V1.5 revision record — current executable plan

This revision replaces the V1.4 Mission map as the executable plan. The V1.4
map is retained below only as implemented-owner and historical-contract
context; it must not dispatch work. V1.5 adds no file, database, event bus,
queue, registry, Planner, Runtime or Authority owner.

It corrects the causal-loss defect discovered in production: an attempt
terminal, especially a stale-evidence `STOP_SAFE`, must not be interpreted as
the terminal of the continuing incident. It also adopts a scale-safe model:
existing append-only transition records retain history; a compact existing
current-state projection retains only the latest actionable state and pointers.

## Program identity

`V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_PROGRAM_V1`

## Target

Close the existing production loop:

```text
Service Failure
-> durable incident
-> OMP consumption
-> incident-bound safe decision
-> ACTION / STAY / STOP_SAFE
-> mandatory STOP_SAFE responsibility classification
-> existing BDP/OMP repair or exact Authority boundary
-> bounded shadow decision
-> controlled action only when independently authorized
-> verification and rollback/no-rollback
-> real Outcome Passport
-> replay and Learning
-> affected capability reconciliation
-> next incident or exact legal terminal
```

The target is not a new Automation Gap Engine, Decision Engine, Shadow system,
Planner, Runtime, queue, registry or Authority owner. The target is to connect
the already implemented owners so that a production `STOP_SAFE` cannot end as
only a recorded event, dashboard warning or email.

## Discovery result

The pre-implementation audit proved that most requested capabilities already
exist:

| Capability | Existing owner | Current result |
| --- | --- | --- |
| failure persistence, episode identity, recovery/expiry | service Matrix lifecycle | `IMPLEMENTED_PRODUCTION_CALLED` |
| passive Situation/Decision/Outcome/replay/Learning capture | `tools/v7-users-autoswitch --consume-passive-events-only` | `IMPLEMENTED_PRODUCTION_CALLED` |
| multi-lane engineering action classes | OMP/Permanent Polygon | `5/5 COMPLETE_CONSUMED` |
| capacity, suitability, policy, confidence, rollback and safety gates | `tools/v7-users-autoswitch` | `IMPLEMENTED_TESTED` |
| bounded emergency failover | `emergency_failover_autonomy` in `tools/v7-users-autoswitch` | `IMPLEMENTED_CERTIFIED_INACTIVE` |
| shadow MOVE/KEEP model and durable decision history | `admin_core/shadow_autonomy.py` and existing JSONL owner | `IMPLEMENTED_UNDERFED_MANUAL_CALLER_ONLY` |
| outcome, feedback, replay, Learning and calibration | existing execution/feedback/trust owners | `IMPLEMENTED` |
| STOP/Intent Gap classification and BDP routing law | OMP Automation Gap Closure Cycle | `CONTRACT_COMPLETE_RUNTIME_BINDING_MISSING` |
| Authority recommendation and action-class evolution | existing delegated-policy and L7/L8 owners | `IMPLEMENTED_HOLD_GOVERNED_ONLY` |

### Historical V1.4 discovery residual — closed, non-executable

The following was the V1.4 broken link. It was closed by the durable
obligation and real OMP consumer work and is retained only to explain prior
evidence. M0 must not rediscover or repair it unless a fresh causal-loss audit
proves a regression of this exact link:

```text
service Matrix timer
-> passive event consumer
-> transient Incident/STOP_SAFE product frontier in latest summary
-> NO PROVEN DURABLE OMP CONSUMER
```

An idempotent later Matrix run overwrote the summary with
`NO_NEW_MATERIAL_INCIDENT_OR_ALREADY_CONSUMED`, so a material frontier is not a
durable unconsumed obligation. V1.5's active residual is narrower: the passive
path must share the compact continuing-incident projection with the execution
path, so a consumed attempt or stale evidence never hides an open incident.

## Existing-owner law

1. Discover -> Reuse -> Extend -> Implement.
2. No new service-failure automation architecture may be created.
3. Incident obligations must be derived from or appended through existing
   event, decision, outcome, closure, CPS or certification owners.
4. `service-matrix-refresh-summary.json` is a latest-run projection, not a
   durable work queue or truth source.
5. Shadow history remains the existing shadow owner. Real outcome history
   remains the existing outcome/feedback owner. Neither may replace the other.
6. OMP Automation Gap Closure remains the only STOP/Intent Gap law.
7. The existing autoswitch planner remains the only route decision producer.
8. The existing emergency failover path remains the only bounded failover
   execution capability considered by this Program.
9. CPS remains the only volatile program and Authority state owner.
10. `Incident Frontier` and `Product Evolution Frontier` are two projections
    of the existing OMP product-engineering frontier. They are not new owners,
    registries, queues or schedulers.
11. The existing `closure-records`, event/outcome JSONL families, bounded
    readers, snapshot store and `tools/v7-users-autoswitch` incident state are
    the only permitted storage substrate for this Program. Raw history remains
    append-only and partitionable; current incident state is a compact
    projection, never an ever-growing envelope.

### Mandatory semantic discovery and connection law

Before every implementation, repair, Mission transition or proposed new
artifact, the executing owner must first prove the current semantic topology:

```text
required outcome
-> existing producer
-> durable artifact / identity
-> existing consumer
-> verification
-> terminal / successor
```

The audit must search by behavior and data-flow, not only by filename or
feature name. It must identify all already implemented or deployed owners,
their input/output identities, freshness and one-use constraints, Authority
boundary, caller, consumer, verification and terminal semantics.

The mandatory order is:

1. discover the existing implementation and its live/deployed state;
2. trace every relevant producer -> consumer link and prove the exact broken,
   absent, stale, duplicate or unreachable link;
3. reuse the existing owner when it already provides the required capability;
4. connect or minimally extend the existing owner when capability exists but
   its handoff, invocation, identity binding or consumption is incomplete;
5. implement new code only for the smallest proven residual that no existing
   owner can supply;
6. verify that the resulting output is consumed by a real downstream owner and
   changes an exact successor, legal terminal or product capability projection.

No Mission may create a parallel owner, queue, registry, watcher, Planner,
Runtime, Authority path, Packet path or evidence store merely because an
existing capability was not discovered or connected correctly. A report,
test, deploy or JSON artifact alone is not completion: the intended output
must reach and be consumed by its declared next owner.

## Evidence and authority law

1. Passive capture, synthetic Polygon results and shadow decisions are
   Engineering Evidence only.
2. `EXTERNAL_UNATTRIBUTED`, `OPERATOR_INDUCED`, controlled and natural
   provenance remain separate.
3. A shadow projection such as “N affected users could move” is impact
   analysis, not executable scope.
4. Any actionable recommendation must be bounded by the current delegated
   action-class policy; current default scope is at most one user and one
   transaction.
5. A legacy runtime policy projection cannot override current CPS/OMP
   `GOVERNED_ONLY`.
6. Runtime apply, routing mutation, user movement, Packet execution,
   restore-barrier write and rollback apply are forbidden unless an exact
   current owner-issued one-use contract independently authorizes them.
7. This Program may recommend `HOLD`, `FREEZE`, `DEMOTE`,
   `RECOMMEND_NARROW_SCOPE` or `RECOMMEND_CERTIFIED_FOR_CLASS_APPROVAL`. It
   cannot grant Authority.
8. Production Maturity is unchanged unless its independent canonical owner
   consumes qualifying real evidence.

## Progressive blast-radius expansion contract

The current one-user limit is a certified safety boundary, not a permanent
technical limit. This Program must mature the existing failover action class
through the following evidence-gated ladder:

```text
1 user
-> 2 users
-> 5 users
-> 10 users
-> bounded cohort
-> bounded incident scope
```

The ladder defines maximum authorized scope, not a requirement to move that
many users. Every decision must still select the smallest necessary cohort.

Promotion to the next tier requires:

- real owner-backed outcomes at the current tier;
- correct target selection and sufficient target capacity;
- successful immediate and temporal verification;
- representative rollback and no-rollback behavior;
- acceptable false-positive, false-negative, STOP_SAFE and missed-opportunity
  rates;
- anti-flap, cooldown, retry-budget and correlated-failure protection;
- Shadow comparison against actual outcomes;
- no unresolved source/target/protocol/provider concentration risk;
- an immutable evidence set and independent Authority recommendation;
- CPS consumption of the exact approved tier.

Any failed verification, rollback failure, drift, capacity loss, correlated
incident or confidence regression must hold, narrow, freeze or demote the
current tier. A numeric limit must never be increased directly in policy.

The legacy production projection `XLARGE_BATCH/50` is historical evidence, not
current Service Failure Authority. It must be reconciled with current
`GOVERNED_ONLY` before any tier above one can become executable.

### Current action-class contract binding

The existing `/etc/v7/policy.json` authority owner must carry a fresh,
explicitly scoped `current_action_class_contract` for every runtime Authority
above `CANARY`. This is a policy field and gate inside the existing
`tools/v7-users-autoswitch` owner; it is not a second Authority, registry,
queue or CPS replacement.

The contract must contain:

- schema `v7.current-action-class-contract.v2` (the former v1 is legacy
  compatibility only and can never be emitted by this Program);
- `contract_id`, `contract_hash`, `issuing_owner`, `active_program` and legal
  action class;
- exact `subject.user_ip`, source/target scope, `max_users=1` and
  `max_concurrent_transactions=1`;
- `incident_generation` and the fresh `source_generation` identity
  (`planner_generation_id`, source/snapshot bundle hashes and selected-move
  hash), plus the exact pre-decision policy generation hash and Authority
  ceiling;
- `issued_at`, short unexpired `expires_at`, verification contract,
  rollback/containment contract, cooldown and anti-flap contract;
- immutable `authority_decision` provenance: the exact request id/hash,
  `APPROVE_ONCE_AS_SCOPED`, decision timestamp, decision id and accountable
  actor provenance;
- a one-use consumption state (`ISSUED -> CONSUMED/EXPIRED`) with exactly one
  allowed use and no retry under the same decision.

`admin_core/operator_execution.py` is the existing Authority decision owner
for this issuance. Its explicit issue surface verifies the fresh request,
expected request id/hash and `APPROVE_ONCE_AS_SCOPED`, then alone writes the
policy field. Neither a hand-edited JSON object nor the read-only autoswitch
request template is an Authority decision or an executable contract. The
autoswitch owner only consumes and independently revalidates a v2 contract.
The request itself expires after fifteen minutes; it is not a standing approval
and an expired reconciliation must be produced again from fresh snapshots.
Immediately before its sole forward mutation, it calls back into the same
existing Authority owner to atomically transition `ISSUED -> CONSUMED`, binding
the exact user, source/target and source generation. A failed or interrupted
later apply remains consumed and therefore requires a new reconciliation and
new Authority decision; no retry can silently reuse the previous contract.

The owner holds an interprocess policy-file lock across read, validation and
atomic replace, so competing consumers cannot both observe `ISSUED`. The
already-owned append-only `/opt/v7/audit/operator-execution-audit.jsonl`
records exactly one `APPROVE_ONCE_AS_SCOPED` or `DECLINE` decision with actor
provenance, and records the one-use consumption. The lock is only a transient
coordination primitive; it is not an additional durable owner. Issuance fails
closed if the current policy generation no longer equals the request binding,
the incident identity/generation is incomplete, Authority exceeds its actual
ceiling, required stop conditions are missing, or verification/rollback
contracts do not name their required owner and verifier-triggered behavior.

The autoswitch gate must cap selection by that scope. A missing, malformed,
expired, lower-than-certified or zero-budget contract is
`STOP_SAFE/FROZEN/0` before restore-barrier snapshot or apply. Historical
promotion evidence, including `XLARGE_BATCH/50`, can never substitute for this
contract. Issuing or refreshing a contract remains the exact existing
owner-issued Authority action; this Program cannot issue one itself.

M5a ordering is strict: the absence of an exact fresh Packet or packet-bound
restore barrier must block only the later M5c Operational Authority path. It
must never block a fresh M5a Action Class request when Situation, Decision,
scope, L3 evidence and all contract-specific preconditions are fresh. A valid
contract then causes M5b fresh planner revalidation; it does not create a
Candidate, Packet or lease and it is not consumed by their preparation. Its
single atomic consumption remains immediately before the sole forward Runtime
mutation. Only a later exact fresh Packet may form an
`OPERATIONAL_AUTHORITY_RESTORE_BARRIER_READY` package through the existing
operator-execution owner.

### Standing delegated one-user operational policy

The repeated short-lived M5a approval loop is a compatibility and emergency
fallback, not the target steady state. The existing policy and
operator-execution owners may carry one independently approved standing
delegated contract for the already-certified action class
`single-user governed candidate failover`.

The standing contract:

- is issued only from one exact registered short-lived request and one
  append-only Authority decision with actor provenance;
- is bound to the complete policy template and policy-file generation, not
  only to a numeric user limit;
- permits only a fresh matching production service-failure event, the existing
  planner, one fresh Candidate, one fresh Packet and one fresh lease;
- permits at most one user and one concurrent transaction;
- requires live capacity, service, route, freshness, confidence, anti-flap,
  cooldown, verification, rollback/containment and final-`OPEN` gates;
- never permits Candidate, Packet, lease or historical Authority reuse;
- expires after 30 days and fails closed when missing, malformed, expired,
  audit-unproven or scope-mismatched;
- grants no larger cohort, new failure class, new action class, Authority
  self-expansion or Production Maturity change.

Inside an active standing contract, a qualifying fresh Candidate does not wait
for a new human decision. The existing Service Matrix lifecycle invokes the
existing bounded governed executor, which alone owns:

```text
fresh failure event
-> fresh planner reconciliation
-> Candidate
-> Packet
-> lease
-> restore-barrier clearance
-> one bounded action
-> verification
-> rollback or certified no-rollback
-> Outcome
-> Learning
-> OMP consumption
-> next event or STOP_SAFE
```

No independent autoswitch timer is enabled. The already existing
service-failure producer/consumer lifecycle is the wake source. Absence of a
qualifying event, safe target or any required gate is a normal `STOP_SAFE`
with zero movement.

### Authority-boundary re-entry loop

An `ENGINEERING_AUTHORITY` terminal must not become a manual dead end. The
existing `tools/v7-users-autoswitch --action-class-contract-reconciliation-only`
producer emits a read-only, deterministic request template from the current
Shadow/action-boundary projection. It never writes policy or creates
Authority. Its closed loop is:

`STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED`
`->` read-only request template
`->` existing coherent observe lifecycle holds the shared service-matrix lock,
invokes `v7-intelligence-snapshot-refresh`, and re-runs the planner on the
same source bundle (a standalone refresh followed by an unlocked read is not
sufficient while the Telegram sentinel is a live writer)
`->` existing `/etc/v7/policy.json` authority owner independently issues or
declines a short one-use scoped contract only after the request preflight is
fresh and ready, through the existing `admin_core/operator_execution.py`
Authority decision surface and an exact `APPROVE_ONCE_AS_SCOPED` request/hash
binding
`->` existing event-driven Service Matrix/autoswitch invocation re-reads and
validates that contract
`->` existing action-class boundary returns either another exact `STOP_SAFE`,
`NO_ACTION`, or `PACKET_MATERIALIZATION_ELIGIBLE`
`->` existing Service Failure obligation/OMP consumer.

The request template is intentionally non-durable and cannot substitute for
fresh Situation, Decision Trace, selected-move/snapshot identities, policy
owner confirmation, Candidate, Packet, lease, verification or rollback. A
policy update alone grants no Runtime apply; the same existing consumer must
revalidate every gate against fresh owner-backed inputs.

## Dynamic Mission compression

`M0` is mandatory and is complete through the associated fresh audit.

After every Mission, OMP must recompute exact residuals:

- skip fully consumed criteria as `MISSION_NOT_REQUIRED_ALREADY_CONSUMED`;
- reduce partially consumed Missions to their exact missing producer-consumer
  links;
- merge Missions only when owner, evidence class, isolation, verification and
  terminal semantics remain explicit;
- do not continue ceremonially after a legal program terminal;
- a lane-local Authority or real-world wait cannot block independent safe
  engineering work.

## Automatic successor continuation contract

Every non-terminal result in this Program must close through the existing
owner chain:

```text
verified result
-> existing OMP consumer
-> atomic CPS projection
-> residual recomputation
-> durable exact successor
-> existing runtime or event-driven consumer
```

Transaction terminals, focused repair completion, tests, safe deploy,
production caller verification, replay, Learning, Outcome consumption and a
`CAUSAL_M7_OUTCOME_TIER_DECISION` recommendation are not operator-return points while a safe successor
exists. The existing event-driven Codex Automation Platform owner must receive
one deterministic wake after the atomic successor projection; the watchdog is
fallback only. Consumption and successor publication are interprocess
exact-once through the existing closure owner.

For an active Service Failure drain, the already-enabled production
`v7-service-matrix-refresh.timer` is the primary successor consumer. After
the source CPS has mirrored a verified Outcome and the existing OMP owner has
acknowledged `CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN`, no additional
Codex wake is published: the next fresh revalidation belongs to that Matrix
timer. Codex remains only a source-CPS mirror/watchdog at this boundary; it
does not own Candidate, Packet, lease, apply, routing or user movement.

The wake is suppressed only for an exact independent `ENGINEERING_AUTHORITY`
or `OPERATIONAL_AUTHORITY` decision, a fully reconciled `REAL_WORLD_LIMIT`, an
external owner/access input, or an irreducible safety boundary. These terminals
must preserve the exact re-entry condition. They may not be converted into an
approval or bypassed by this Program.

### Auto-safe continuation execution policy

`CODEX_AUTOMATION_PLATFORM` is the existing watchdog fallback owner for this
Program. It must re-enter the active OMP task on the configured heartbeat when
the task is idle or interrupted; an ended response, connection loss, context
compaction or a completed intermediate tool call is never a Program terminal.

On each wake it must read fresh CPS and use the existing OMP re-entry owner.
When CPS exposes a safe executable successor, it must continue without an
operator message through the complete existing-owner chain: discovery,
smallest repair, focused verification, commit/push, passing safe-deploy
manifest, authorised safe deploy, production caller/consumer verification,
affected replay/Learning, truth/convergence, atomic CPS/OMP/report projection,
residual recomputation and successor dispatch.

The continuation is strictly bounded:

- it must re-read CPS before every successor and preserve the existing
  exact-once lease, duplicate suppression and source-generation checks;
- it must not retry an unchanged failed successor indefinitely; after three
  wakes without owner-backed progress it records the exact
  producer-to-consumer blocker and stops without churn;
- it must not create a new watcher, queue, registry, Planner, Runtime or
  Authority system;
- it must not treat this policy as consent for `ENGINEERING_AUTHORITY`,
  `OPERATIONAL_AUTHORITY`, restore-barrier write, Packet execution, routing
  mutation, user movement, rollback apply, Authority expansion, Production
  Maturity change, external owner/access input or Natural L8 evidence.

At any such independent boundary the heartbeat may perform read-only discovery
and prepare the exact existing-owner request, but must preserve the re-entry
condition and stop. A new safe successor or a separately owner-issued scoped
contract is required before it continues.

After each owner-backed controlled outcome, replay and Learning, the existing
`CAUSAL_M7_OUTCOME_TIER_DECISION` owner recomputes the progressive blast-radius ladder. `HOLD`, `FREEZE`,
`DEMOTE` and insufficient-evidence decisions remain exact legal outputs. An
independently approved next tier produces a durable successor for the same
existing execution lifecycle. At most one tier may advance per independently
certified generation: `1 -> 2 -> 5 -> 10 -> bounded cohort`. No policy number
may be raised directly and no historical evidence may substitute for the
current owner decision.

## Parallel frontier and arbitration law

V7 has two simultaneous, existing-owner work projections:

| Projection | Input | Legal outputs |
| --- | --- | --- |
| `INCIDENT_FRONTIER` | real production Situation, incident, ACTION/STAY/STOP_SAFE, recovery or expiry | safe repair, correct-STAY/STOP terminal, exact data/caller/code/Authority/external-owner gap |
| `PRODUCT_EVOLUTION_FRONTIER` | capability residual, Polygon result, replay/coverage gap, valid incident-derived engineering gap | existing BDP -> Candidate -> OMP Mission -> affected verification -> next residual |

Arbitration rules:

1. A material current production incident has safety priority.
2. A correct `STAY` or `STOP_SAFE` closes that incident action only; it does
   not suppress independent Product Evolution work.
3. Product Evolution work cannot relabel, erase or bypass an open production
   incident.
4. Every consumed output recomputes both projections.
5. A `STOP_SAFE` creates a deterministic classification obligation, but BDP
   admission occurs only for a proven automatable engineering gap.
6. Both projections are derived and consumed through existing OMP/CPS owners;
   neither is a durable second backlog.

## V1.5 causal-closure architecture and Mission map

### Proven reuse and exact residual

V1.5 reuses, rather than replaces, these already implemented elements:

| Need | Existing owner | V1.5 use |
| --- | --- | --- |
| immutable observation and transition history | date-partitionable event, closure, outcome and Learning JSONL families | append-only causal transitions; no live action reads all history |
| compact read model | intelligence snapshot store, bounded JSONL readers and autoswitch runtime state | current incident/attempt projection with atomic replace and bounded reads |
| incident identity and partial-scope continuity | `tools/v7-users-autoswitch` L3 incident state | common passive/L3 incident lifecycle; no second incident registry |
| exact-once handoff | existing `closure-records.lock`, receipt and CPS reconciliation owner | lock the complete transition, not just receipt append |
| safe action | existing planner, delegated policy, Candidate, Packet, lease and governed executor | only fresh objects for the same revalidated incident |
| engineering readiness | Permanent Polygon and existing controlled-production owner | reproduce, verify and prepare an opportunity; never manufacture a production outcome |

The exact residual is therefore not missing logs and not missing automation.
The passive service-failure path records a durable terminal but does not yet
share a compact continuing-incident projection with the execution path. A
later `NO_PENDING_OBLIGATION` or stale attempt can consequently hide an open
incident instead of revalidating it. V1.5 closes that producer-to-consumer
gap.

### Scale and retention law

The design must remain safe at 10,000 users and 1,000 channels.

```text
existing append-only event / decision / closure / outcome / Learning records
                       +
compact keyed current-incident projection
                       +
CPS pointers to only the active program frontier
```

The compact projection is an extension of the existing autoswitch incident
state, not a new store. It contains only:

- `incident_id`, `incident_generation`, state and first/last confirmation;
- latest observation generation and failure family;
- affected, protected and unresolved **scope summaries** (counts, cohort
  fingerprint and source pointers, never a growing user list);
- `intent_scope_type`, `intent_scope_fingerprint`, `intent_closure_reason`
  and `intent_closure_evidence_pointer`;
- current certified tier, last attempt pointer and last terminal;
- last responsible link, next consumer, re-entry condition and intent status;
- lineage pointers to immutable records.

It must not embed probe bodies, all decisions, all attempts, all users or all
outcomes. Each transition is appended once through existing owners and refers
back by identity. Existing date-partitioned JSONL-family reads, bounded tail
reads and producer-owned snapshot rotation remain the scale mechanism. M0
must measure file growth, lock hold time and lookup cost before setting any
retention/rollup values; it must not invent numerical retention limits. If a
single current-state partition becomes a measured bottleneck, the existing
JSONL-family/owner may partition by incident/channel generation and publish a
compact rollup — never add a database or a second truth source.

This follows the production pattern of append-only history plus a materialized
current view: Kafka compaction retains a latest keyed value for recovery,
AWS documents event sourcing with materialized views, OpenTelemetry carries
correlation context across components, and Elastic rolls over/downsamples
time-series history rather than letting one live index grow without limit.

Primary design references (inform the pattern; they do not introduce those
products into V7): [Apache Kafka log compaction](https://kafka.apache.org/40/design/design/),
[AWS event sourcing and materialized views](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/event-sourcing-pattern.html),
[OpenTelemetry context propagation](https://opentelemetry.io/docs/concepts/context-propagation/)
and [Elastic data-stream lifecycle](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/data-stream-lifecycle.html).

### Current-source scope, cumulative lineage and knowledge reuse

The existing L3 incident record has two non-interchangeable compact views;
both are derived from existing `users.registry`, Matrix and immutable
execution/outcome owners.

| View | Permitted meaning | Never permitted to do |
| --- | --- | --- |
| `CURRENT_SOURCE_SCOPE` | Current enabled users on the presently failed source generation, with `affected = protected + unresolved + excluded_or_recovered` backed by current route truth and the exact source fingerprint | count a historical packet success as a current member merely because it is old, successful, or has the same channel name |
| `INCIDENT_CUMULATIVE_SCOPE` | Compact packet-bound lineage across the incident: feedback/Packet/Learning pointers and exactly one classification per success | become a second denominator, store a growing user list, or fabricate a missing causal binding |

The cumulative classifications are exactly
`CURRENT_INCIDENT_PROTECTED`, `HISTORICAL_PROTECTED_PRE_BASELINE`,
`HISTORICAL_MOVED_INCIDENT_BINDING_MISSING`, `RETURNED_TO_SOURCE`,
`RECOVERED_OR_EXCLUDED` and `OTHER_INCIDENT`. An unbound historical movement
may remain visible only as `HISTORICAL_MOVED_INCIDENT_BINDING_MISSING`; it
does not reduce the current source scope. Every packet-bound success therefore
remains discoverable through existing immutable evidence while no historical
success can silently manufacture present protection.

### Step 2 automatic-drain invariants

`CONTINUE_ACTIVE_INCIDENT_REVALIDATION_AND_DRAIN` is an executable durable
successor, not an operator-return state. For every bounded Tier-1 transaction,
the existing owners must preserve one exact causal tuple across
`Event -> Candidate -> Packet -> Outcome`: `source_incident_id`, fresh
observation generation, source channel, and compact current-source scope
count/fingerprint. An incomplete tuple is `STOP_SAFE`; a historical Packet,
Candidate, lease, approval or route observation may never fill the gap.

For this legacy regular-wake lifecycle, the existing Matrix lifecycle is the
only regular wake source. It does not restrict V5.3 N0–N11 legal immediate
signals from waking bounded targeted Matrix confirmation. It may create the
next fresh probe generation and invoke the existing OMP/CPS consumer; this
Program must not enable a timer, create a watcher or use an operator/Codex
message as a required re-entry mechanism. Every transaction still independently
checks source degradation, user/source membership, healthy target, capacity,
standing policy, cooldown/anti-flap, fresh Candidate/Packet/lease, verification
and rollback readiness.

`max_users=1` and `max_concurrent_transactions=1` bound each transaction;
they do not cap the number of transactions in one continuing incident. The
runtime terminal `BOUNDED_AUTOMATIC_INCIDENT_DRAIN_RUNTIME_CONSUMED` proves an
automatic successor-to-successor sequence, not whole-incident closure. Whole
incident closure requires `CURRENT_SOURCE_SCOPE_EMPTY`, verified source
recovery, or one exact owner-backed live blocker with durable automatic
re-entry.

Before every audit, test, certification lookup, owner discovery or capability
decision, the existing Knowledge Plane is consumed through Canonical Reference,
SYSTEM_MAP, Engineering Truth Lifecycle, ADRs, CPS, OMP and the relevant
capability/certification owner. The resulting compact decision is
`KNOWLEDGE_REUSE_AND_SELECTIVE_REVALIDATION`, with one classification for each
Tier `1`, `2`, `5`, `10` and bounded cohort: `REUSABLE`, `APPROVED`,
`INACTIVE`, `MISMATCHED`, `STALE` or `INVALIDATED`.

The decision may request a revalidation only after an existing owner-backed
invalidation trigger: a relevant implementation/dependency or policy/authority
generation change, source/target topology or service-class change, a material
scope/contract change, contradictory production evidence, a real
verification/rollback failure, or a new approved tier. A new Codex turn,
report, observation, incident, Candidate, Packet, lease expiry or prior
successful attempt is never by itself an invalidation trigger. This is a
derived field of existing owners, not an audit database or certification
registry.

### Dual lifecycle and causal-lineage contract

Every relevant record carries the applicable subset of this lineage:

```text
incident_id, incident_generation, observation_generation,
situation_id, decision_trace_id, obligation_id, action_opportunity_id,
attempt_id, candidate_id, packet_id, lease_id, outcome_id, learning_id,
parent_transition_id
```

This is identity metadata inside existing records, not a graph database.
The invariant is mandatory:

```text
every current frontier -> traceable backward to its incident
every open incident -> traceable forward to its next required consumer
```

Failure of either direction is `CAUSAL_LINEAGE_BROKEN`, an engineering defect
with a last responsible producer-consumer link; it is never `NO_WORK`.

Two independent state axes are required:

| Axis | States | Meaning |
| --- | --- | --- |
| Incident lifecycle | `OPEN_OBSERVED`, `OPEN_REVALIDATION_REQUIRED`, `OPEN_ACTION_REQUIRED`, `OPEN_AUTHORITY_REQUIRED`, `OPEN_EXTERNAL_OWNER_REQUIRED`, `ACTION_IN_PROGRESS`, `PARTIALLY_PROTECTED`, `RECOVERY_VERIFYING`, `INTENT_CLOSED` | status of the actual service/user-protection problem |
| Attempt terminal | `SUCCESS`, `STOP_SAFE`, `NO_CANDIDATE`, `PACKET_EXPIRED`, `AUTHORITY_REQUIRED`, `ROLLBACK_SUCCESS`, `VERIFICATION_FAILED`, `NO_EXECUTION` | result of one fresh decision/execution attempt |

`attempt terminal != incident terminal`. A one-user success for a forty-user
channel incident is `PARTIALLY_PROTECTED`; an expired packet is normally
`OPEN_REVALIDATION_REQUIRED`, not incident closure.

Protection scope has three distinct levels:

```text
Channel incident
-> cohort protection intent
-> user protection intent
```

For example, a successful action for user `U` may close only `U`'s intent;
the channel remains `OPEN/PARTIALLY_PROTECTED` while another cohort is
unresolved. A correct `STAY` is equally scoped: it closes only the exact fresh
intent proven safe, never a wider channel incident by implication.

The following invariants are mandatory and machine-checkable:

```text
incident_state != INTENT_CLOSED AND next_required_consumer is empty
-> INVALID_OPEN_INCIDENT_NO_SUCCESSOR

incident_state != INTENT_CLOSED AND reentry_condition is empty
-> CAUSAL_LINEAGE_BROKEN
```

### Active-incident revalidation law

The required missing transition is:

```text
same incident_id + fresh failed probes + same source/failure family
+ no verified recovery + valid current action class + safe target
-> CURRENT_ACTIVE_INCIDENT_REVALIDATED
-> new observation generation -> new Situation -> new Decision
-> fresh action opportunity -> fresh Candidate / Packet / lease only if legal
```

No new outage is required. Fresh confirmation that the same incident remains
open is sufficient. The historical incident identity persists; every live
execution identity is recreated. A verified recovery instead enters
`RECOVERY_VERIFYING` and may close the relevant protection intent only after
its existing recovery owner proves it.

### Intent and no-progress law

Every `STOP_SAFE` first answers whether the exact user-protection intent is
closed. A fresh proof that no target is safer, or that the user is already on
the best permitted route, is a correct intent closure and must not create BDP
churn. BDP/OMP is admitted only when all are true:

```text
intent remains open
AND last responsible link is engineering
AND an existing owner can change the result
```

Authority, external-owner and Natural L8 boundaries preserve the incident as
open with their exact re-entry condition. For every open incident, retain
`first_seen`, `last_progress_at`, `last_observation_at`, `blocked_since`,
`next_reentry_due` and `same_blocker_count`. Repeated unchanged blocking input
becomes `NO_PROGRESS_CAUSAL_CHAIN_DEFECT` after the existing bounded
no-progress rule, routing the last responsible link to repair instead of
blind refresh.

### M0 — Causal-loss and storage-topology audit

Semantic Mission ID: `CAUSAL_M0_CAUSAL_LOSS_AND_STORAGE_AUDIT`.

Read CPS/OMP, source, production state and every existing owner by behavior.
For each current/recent material incident, prove the full lineage from Matrix
observation to next consumer or exact terminal. Measure append growth,
partition availability, compact-projection size, lock duration and bounded
lookup cost. Classify each missing link as producer, consumer, identity,
freshness, projection, concurrency or external boundary.

Completion: `CAUSAL_LOSS_AND_SCALE_RESIDUAL_EXACTLY_PROVEN`.

### M1 — Dual lifecycle and compact incident projection

Semantic Mission ID: `CAUSAL_M1_DUAL_LIFECYCLE_COMPACT_PROJECTION`.

Extend the existing autoswitch incident state and existing closure transition
records with the two axes, compact fields, scope summaries and lineage
pointers. Preserve append-only history externally; migrate/reconcile current
open incidents without fabricating a new observation or outcome. Ensure a
single-user outcome leaves a wider channel incident `PARTIALLY_PROTECTED`.

Completion: `DUAL_LIFECYCLE_COMPACT_PROJECTION_CONSUMED_WITHOUT_SECOND_STORE`.

### M2 — Atomic causal transition and successor publication

Semantic Mission ID: `CAUSAL_M2_ATOMIC_CAUSAL_TRANSITION`.

Use the existing lock/CAS owner across selection of the current incident,
generation validation, incident-state update, successor publication, CPS
projection and receipt append. A crash between any stages must recover
idempotently without a duplicate successor. Old writers after a newer
generation fail closed.

Completion: `INCIDENT_TRANSITION_EXACTLY_ONCE_AND_RECOVERABLE`.

### M3 — Current active incident revalidation

Semantic Mission ID: `CAUSAL_M3_ACTIVE_INCIDENT_REVALIDATION`.

Implement the active-incident revalidation transition through existing Matrix,
passive capture and planner owners. Fresh failed probes of a continuing,
unrecovered incident must create a new observation generation and fresh
read-only action opportunity, rather than requiring a second outage. Existing
standing policy is revalidated as a gate; it neither reuses a Candidate nor
grants a Packet.

Completion: `CURRENT_ACTIVE_INCIDENT_REVALIDATED_TO_FRESH_SUCCESSOR_OR_EXACT_STOP_SAFE`.

### M4 — Intent-aware STOP_SAFE and Automation Gap routing

Semantic Mission ID: `CAUSAL_M4_INTENT_AWARE_GAP_ROUTING`.

Classify each attempt terminal against the continuing incident and its exact
protection intent. Route only open engineering gaps through existing BDP/OMP;
retain correct-STAY, Authority, external-owner and Natural L8 states as
explicit re-entry boundaries. Reconcile both `INCIDENT_FRONTIER` and
`PRODUCT_EVOLUTION_FRONTIER` after every transition.

Completion: `OPEN_INTENT_GAP_ROUTED_OR_CORRECT_INTENT_CLOSURE_PROVEN`.

### M5 — Polygon as engineering-closure substrate

Semantic Mission ID: `CAUSAL_M5_POLYGON_ENGINEERING_CLOSURE`.

Polygon receives the exact unresolved engineering cell and lineage. It may
replay the causal chain, test target/capacity/rollback/anti-flap/partial-scope
logic and prepare a controlled L7 opportunity for the existing production
owner. It cannot close the production incident, create an Outcome Passport,
claim L7 credit or manufacture Natural L8.

Completion: `UNRESOLVED_ENGINEERING_CELL_REPLAYED_AND_OWNER_HANDOFF_READY`.

### Production-effects boundary by Mission

| Missions | Permitted production effect | Ownership rule |
| --- | --- | --- |
| `CAUSAL_M0`–`CAUSAL_M5` | none | discovery, projections, lineage, Polygon engineering work and controlled-opportunity preparation are read-only/non-mutating |
| `CAUSAL_M6_CONTROLLED_ATTEMPT` | at most one bounded action | only through an active standing delegated policy and every existing fresh live gate; this Mission is the sole V1.5 execution owner |
| `CAUSAL_M7`–`CAUSAL_M9` | no additional action | only owner-authorized observation, verification, rollback/no-rollback evidence, replay or Learning for the already-created attempt |
| `CAUSAL_M10_VLESS_ACCEPTANCE` | no separate execution path | acceptance invokes the already deployed and verified `CAUSAL_M6_CONTROLLED_ATTEMPT` path; it may observe one bounded action only if that path independently admits it |

No Mission may use this table to bypass Authority, freshness, Packet/lease,
restore-barrier, rollback, capacity or blast-radius gates.

### M6 — Existing controlled action path and partial-scope handling

Semantic Mission ID: `CAUSAL_M6_CONTROLLED_ATTEMPT`.

Only when current policy and all fresh gates allow, use the existing planner →
Candidate → Packet → lease → bounded executor path. A one-user outcome updates
protected/unresolved scope and returns to the same incident; tier progression
remains independent from incident closure. A non-action terminal updates the
attempt axis and continues through M3/M4.

Completion: `FRESH_BOUNDED_ATTEMPT_OUTCOME_OR_EXACT_CONTINUING_INCIDENT_STOP`.

### M7 — Outcome, replay, Learning and tier recommendation

Semantic Mission ID: `CAUSAL_M7_OUTCOME_TIER_DECISION`.

Reuse existing Outcome Passport, temporal verification, replay, Learning and
the `CAUSAL_M7_OUTCOME_TIER_DECISION` recommendation owner. Consume only the affected capability criteria;
compare shadow with actual outcome; update the exact tier recommendation.
No whole capability, Authority or Production Maturity may advance implicitly.

Completion: `OUTCOME_LINEAGE_TO_LEARNING_AND_AFFECTED_TIER_DECISION_CONSUMED`.

### M8 — CPS/runtime/OMP pointer reconciliation

Semantic Mission ID: `CAUSAL_M8_LIVE_POINTER_RECONCILIATION`.

CPS holds only live pointers: active contract ID, incident ID/state, current
attempt ID, next consumer, re-entry condition and frontier. Runtime policy
remains owned by its policy owner; incidents by their lifecycle owner; outcomes
by outcome owners. Any disagreement is `RUNTIME_CPS_PROJECTION_MISMATCH` and
routes through the existing reconciliation owner, never a manual text patch.

Completion: `LIVE_POINTERS_MATCH_OWNER_BACKED_RUNTIME_AND_INCIDENT_TRUTH`.

### M9 — Restart, concurrency and no-progress campaign

Semantic Mission ID: `CAUSAL_M9_CONCURRENCY_RECOVERY_CAMPAIGN`.

Prove two revalidators yield one observation generation; two opportunity
producers yield one fresh attempt; stale writers are rejected; and each crash
boundary reconciles without duplicate successor. Prove correct STOP_SAFE does
not create BDP churn, while repeated unchanged blockers produce a causal-chain
repair frontier.

Completion: `CAUSAL_CLOSURE_CONCURRENCY_RECOVERY_AND_NO_PROGRESS_PROVEN`.

### M10 — Current VLESS production acceptance and implementation terminal

Semantic Mission ID: `CAUSAL_M10_VLESS_ACCEPTANCE`.

Use the current VLESS incident as the acceptance subject: prove it remains
open or recovered; obtain fresh failed probes if still open; materialize
`CURRENT_ACTIVE_INCIDENT_REVALIDATED`; check the active standing policy; then
obtain a fresh Candidate/Packet/lease or exact live STOP_SAFE. Execute one
bounded action only if existing policy and runtime gates independently permit
it. Consume verification, Outcome, Replay, Learning, scope update and the
affected `CAUSAL_M7_OUTCOME_TIER_DECISION` tier decision.

#### VLESS continuing-failure scope-binding law

For a continuing certification-only VLESS failure, use **Model B**. The
existing Matrix owner is canonical for the fresh health result, failure
episode and immutable observation event. `users.registry` is canonical for
the *current* assignment membership. A Matrix event's compact source-scope
fingerprint is therefore historical observation evidence, not a live
membership lock and not a reason to rewrite or re-emit Matrix state whenever
a controlled identity moves.

The existing controlled selector must first prove a fresh currently-failed
Matrix source and one matching fresh capture-only Matrix event whose correlated
service remains failed, then read the current `users.registry` scope. It stops safely for an empty scope,
any ordinary user, an uncontrolled source, stale/recovered/ambiguous Matrix
state, a stale event, or an event from another incident. Only after that
read-only binding may the existing Candidate/Packet/lease chain freeze the
one exact certification identity, source and target immediately before apply.
The ordinary L3/passive path and its current-scope accounting remain unchanged.

This preserves separation of responsibilities: Matrix never becomes a second
user-assignment owner; the selector does not become an event writer; and a
Packet/lease never reuses an old selection after membership, health, target,
policy or authority changes.

The implementation terminal is:

`PERSISTENT_INCIDENT_CAUSAL_CLOSURE_RUNTIME_CONSUMED`

It requires all of the following:

- every current open incident is compactly projected;
- the current VLESS incident is reconciled as open/recovered with its exact
  scope and re-entry result;
- no open incident lacks `next_required_consumer` or `reentry_condition`;
- CPS/runtime/OMP pointers are owner-backed and aligned;
- `CAUSAL_M7_OUTCOME_TIER_DECISION` is consumed for the affected tier;
- a future non-test producer/consumer is certified to enter the same invariant.

It does not claim that no future incidents will arise or that all future
actions are authorized.

### V1.5 verification requirements

Every Mission follows the existing focused tests, production caller/consumer,
safe-deploy, replay, truth and convergence sequence. In addition, each must
prove bounded storage growth, no full user list in the current projection,
lineage in both directions, dual-axis correctness, partial-scope correctness,
and zero forbidden effects unless an existing current contract allows the
specific bounded action.

## Historical Mission map — V1.4, non-executable context

### M0 — Existing capability and production binding reconciliation

Status in this plan: `DISCOVERY_COMPLETE_AWAITING_CPS_ADMISSION`.

Required result:

- prove current CPS/OMP, repository and production caller state;
- inventory capability owners by semantics, not filenames;
- distinguish implemented, tested, deployed, production-called, consumed and
  Authority-active states;
- identify the last responsible producer-consumer link.

Completion contract:

`EXISTING_AUTOMATION_INVENTORIED_AND_EXACT_RESIDUAL_PROVEN`

### M1 — Durable Situation / Incident / STOP_SAFE obligation and real OMP consumer

Extend the existing passive records so every material Situation, incident,
ACTION, `STAY`, `STOP_SAFE`, recovery or expiry exposes one deterministic
obligation identity through an existing durable owner. Do not create an
opportunity store, queue or registry.

The existing OMP continuation consumer must:

1. discover the unconsumed durable Situation/Incident/STOP_SAFE obligation;
2. verify source identity, provenance, freshness and generation;
3. consume it exactly once across processes;
4. preserve recovery/expiry links;
5. classify every `STOP_SAFE` before selecting a successor;
6. emit the exact Incident and Product Evolution projection outputs;
7. preserve an unconsumed obligation when a later Matrix run has no new event.

The mandatory first classification is:

```text
STOP_SAFE
-> CORRECT_SAFE_TERMINAL
or DATA_OR_EVIDENCE_GAP
or EXISTING_CAPABILITY_NOT_CALLED
or ENGINEERING_IMPLEMENTATION_GAP
or AUTHORITY_REQUIRED
or EXTERNAL_OWNER_REQUIRED
```

`CORRECT_SAFE_TERMINAL` is a successful safety outcome, not a BDP Candidate.
Only a proven automatable engineering gap enters the existing BDP -> Candidate
-> OMP path.

The durable obligation must also preserve affected-user count, current
certified blast-radius tier, requested tier, target-capacity snapshot and the
exact evidence cell blocking the next tier. These are projections through
existing owners, not a new Authority registry.

Required production proof:

```text
real Matrix timer
-> passive consumer
-> durable obligation
-> independent OMP caller
-> consumer behavior change
-> successor or legal terminal
```

Completion contract:

`PRODUCTION_SITUATION_STOP_SAFE_OBLIGATION_DURABLE_AND_OMP_CONSUMED`

### M2 — Incident-bound Decision Matrix and early Automation Gap adapter

Do not build another Decision Matrix. Bind the durable incident to the existing
autoswitch planner and its current gates in read-only mode.

For the exact source and affected scope, calculate:

- source hard/partial failure classification;
- healthy target availability;
- target service suitability and capacity;
- policy eligibility;
- evidence freshness;
- confidence;
- anti-flap and cooldown;
- verification and rollback feasibility;
- current action-class Authority;
- bounded executable scope and separate aggregate impact scope.

For every incident, the adapter must calculate:

- the smallest necessary cohort;
- the maximum capacity-safe cohort;
- the current Authority-safe cohort;
- the effective cohort as the minimum of those bounds;
- why the next ladder tier is allowed or blocked.

The legal decision taxonomy is:

- `MOVE_READY_WITHIN_EXISTING_AUTHORITY`;
- `STAY_CORRECT_CURRENT_ROUTE`;
- `STOP_SAFE_NO_SAFE_TARGET`;
- `STOP_SAFE_DATA_OR_EVIDENCE_GAP`;
- `STOP_SAFE_EXISTING_CAPABILITY_NOT_CALLED`;
- `STOP_SAFE_ENGINEERING_IMPLEMENTATION_GAP`;
- `STOP_SAFE_AUTHORITY_REQUIRED`;
- `STOP_SAFE_EXTERNAL_OWNER_REQUIRED`.

Every STOP must include:

- `last_responsible_link`;
- owner;
- exact missing artifact;
- existing consumer;
- reentry condition;
- whether Polygon can close the engineering part;
- forbidden effects.

Before any MOVE-capable output, reconcile the current CPS delegated policy with
the older production runtime authority projection. A broader legacy batch
budget must fail closed and cannot become current action-class Authority.

M2 consumes the early classification emitted by M1. It must not postpone
Automation Gap Closure until a later implementation Mission. M4 only routes,
repairs and revalidates a gap that M1/M2 already proved.

Completion contract:

`INCIDENT_BOUND_SAFE_DECISION_AND_RESPONSIBILITY_CLASSIFICATION_CONSUMED`

### M3 — Automatic bounded Shadow production and outcome reconciliation

Reuse `admin_core/shadow_autonomy.py` and its current durable owner. Remove
dependence on an operator opening an admin endpoint as the only producer.

The event-driven OMP incident consumer must produce:

- one deduplicated bounded shadow recommendation for the exact current
  delegated scope;
- a separate aggregate affected-user impact projection;
- MOVE/STAY/STOP_SAFE reason and gate snapshot;
- source, target, Situation, Decision Trace and incident identities;
- zero apply, zero movement and zero Authority effect.

Shadow must evaluate the ladder without granting it: current-tier behavior,
counterfactual `2/5/10/bounded cohort` behavior, capacity pressure, rollback
exposure and correlated-failure risk. Only the current certified tier may be
presented as potentially executable; all higher tiers remain counterfactual.

The existing outcome/feedback owner must automatically compare a later
owner-backed outcome with the matching shadow decision. Observed outcomes are
primary evidence. Human comparison remains secondary supervised evidence and
must not be fabricated to fill a threshold.

Completion requires more than model invocation:

- a real non-test incident produces a durable shadow record;
- duplicate invocations append zero duplicates;
- a matching controlled or natural outcome, when present, reaches the existing
  comparison/Learning consumer;
- the next capability state changes or the exact evidence gap is emitted.

Completion contract:

`EVENT_DRIVEN_SHADOW_DECISION_AND_REAL_OUTCOME_RECONCILIATION_PRODUCTION_CONSUMED`

### M4 — Existing Automation Gap Closure routing, repair and revalidation

Consume the M1/M2 classification through the missing real caller/consumer for
the OMP V4.7-V4.10 contract. Do not repeat classification or create a second
gap engine.

Routing by classification:

| Classification | Existing route |
| --- | --- |
| correct STOP/no safe target | close as legal safety terminal and monitor the same incident generation |
| missing/stale data | responsible producer repair -> tests -> deploy -> affected replay |
| existing capability not called | repair the producer-consumer binding |
| engineering implementation gap | existing BDP -> Candidate -> OMP Mission |
| Authority required | exact action-class recommendation/request; no implicit grant |
| external owner required | owner-bound terminal with exact reentry event |

If the current tier succeeds but the next tier is blocked, Automation Gap
Closure must classify the exact reason as evidence, capacity, implementation,
consumer binding, Authority or external-owner gap. It must not reduce every
promotion blocker to generic `AUTHORITY_REQUIRED`.

A repair closes only when the original incident is replayed and the original
STOP/Intent Gap changes to its expected state. Tests or reports alone do not
close it.

Completion contract:

`STOP_SAFE_AUTOMATION_GAP_ROUTED_AND_ORIGINAL_INTENT_REVALIDATED`

### M5 — Conditional bounded controlled automation

Do not rebuild emergency failover. Reuse the existing
`emergency_failover_autonomy` gates, standing delegated action-class contract
and per-operation one-use Candidate/Packet/lease identities.

M5 has three non-interchangeable sub-stages. They are not a new Program,
Authority, Planner, queue, registry or execution path.

#### M5a — Action-class contract reconciliation

The existing policy, CPS and OMP owners must state the legal action class for
the exact failure family before any Packet-capable output. The target steady
state is one independently issued standing one-user delegated contract; the
short-lived exact-user M5a contract remains the fallback. Either contract must
bind maximum users, concurrency, allowed failure/action classes, freshness,
verification, rollback, cooldown, anti-flap, expiry and concrete stop
conditions. A missing, stale or audit-unproven contract is
`STOP_SAFE/FROZEN/0`; historical promotion evidence is never a substitute.

#### M5b — Shadow versus allowed-action boundary

Every Shadow recommendation must be compared with the action class actually
allowed now. The read-only output is exactly one of:

- `NO_ACTION_NO_SHADOW_CANDIDATE`;
- `STOP_SAFE_CURRENT_ACTION_CLASS_CONTRACT_REQUIRED`;
- `STOP_SAFE_OTHER_EXECUTION_GATE_REQUIRED`;
- `PACKET_MATERIALIZATION_ELIGIBLE`.

`PACKET_MATERIALIZATION_ELIGIBLE` is not `MOVE_READY` and grants no execution
permission. It means only that a fresh Candidate, Packet, lease, verification
and rollback gate may be prepared by their existing owners.

#### M5c — Execution-boundary preparation

Candidate, Packet and lease preparation may occur only after M5a/M5b, using
fresh Situation and Decision Trace identities. Under the standing contract,
the fresh Packet, lease, restore-barrier clearance and operation-scoped
execution window are the exact one-use operational boundary; no per-Candidate
human approval is required. Without that standing contract, Runtime apply
remains a separate exact one-use operational decision. `ENGINEERING_AUTHORITY`
cannot silently become `OPERATIONAL_AUTHORITY`.

This Mission runs only when M1-M4 prove:

- a genuine production need;
- a safe target;
- fresh service evidence;
- current action-class Authority;
- exact one-user/one-transaction budget;
- fresh Candidate, Packet, lease and snapshots;
- verification and rollback readiness;
- accepted event-driven wake;
- no legacy-policy/CPS conflict.

Controlled progression is one tier per independently certified evidence
generation. A Mission may skip a nominal tier only when existing owner-backed
evidence already proves every completion criterion for that tier; the skip
must be recorded as `TIER_NOT_REQUIRED_ALREADY_CERTIFIED`.

Every controlled tier run must preserve:

- one operation-scoped cohort identity;
- per-user and cohort-level verification;
- target capacity before, during and after execution;
- partial-apply handling;
- cohort rollback semantics;
- circuit breaker and immediate demotion path;
- exact evidence separation from ordinary production and Natural L8.

The inactive periodic autoswitch timer must not be enabled merely to satisfy
automation. The existing event-driven incident/OMP path should invoke one
bounded run. Timer/cron/blind polling remain rejected wake sources unless a
separate Authority program changes that contract.

If standing Authority is absent, the legal terminal is an exact standing
policy Authority request or the legacy exact-user `ENGINEERING_AUTHORITY`
fallback, not a fake execution and not a global engineering stop.

The Authority terminal itself has the explicit re-entry loop above. It closes
only when the existing policy owner either declines/lets the request expire
(which returns a fresh `STOP_SAFE`) or issues a valid short one-use contract
that the existing autoswitch boundary consumes and revalidates. No new
Authority owner, registry, queue, watcher or timer is introduced.

Completion contract:

`BOUNDED_SERVICE_FAILURE_ACTION_REAL_OUTCOME_CONSUMED`

or, when legitimately blocked:

`BOUNDED_SERVICE_FAILURE_ACTION_EXACT_AUTHORITY_BOUNDARY_PROVEN`

### M6 — Learning, capability maturation and Authority recommendation

Reuse Outcome Passport, temporal verification, deterministic replay, Learning,
calibration and action-class Authority owners.

After every new incident outcome:

1. reconcile the affected CAP-U criteria only;
2. preserve provenance and action-class separation;
3. compare shadow recommendation with actual outcome;
4. recalculate false-positive, false-negative, correct-STAY, STOP_SAFE,
   rollback/no-rollback and missed-opportunity coverage;
5. recompute confidence and risk by action class;
6. emit exactly one of:
   - `HOLD_GOVERNED_ONLY`;
   - `FREEZE`;
   - `DEMOTE`;
   - `RECOMMEND_NARROW_SCOPE`;
   - `INSUFFICIENT_EVIDENCE`;
   - `RECOMMEND_CERTIFIED_FOR_CLASS_APPROVAL`.

The recommendation must include an exact blast-radius result:

- `HOLD_CURRENT_TIER`;
- `DEMOTE_TO_<N>`;
- `RECOMMEND_TIER_<N>`;
- `RECOMMEND_BOUNDED_COHORT`;
- `RECOMMEND_BOUNDED_INCIDENT_SCOPE`;
- `INSUFFICIENT_TIER_EVIDENCE`.

It must bind the maximum users per transaction, maximum concurrent
transactions, source/target families, failure classes, capacity reserve,
cooldown, rollback trigger, circuit breaker, demotion rule and expiry.

Unrelated whole capabilities must not advance.

Completion contract:

`CURRENT_SERVICE_FAILURE_EVIDENCE_CONSUMED_AND_ACTION_CLASS_AUTHORITY_RECOMMENDATION_DECIDED`

### M7 — Separate Authority-owned activation

This Mission is conditional and outside any implicit continuation.

It starts only if M6 emits
`RECOMMEND_CERTIFIED_FOR_CLASS_APPROVAL`. Activation must use a distinct
existing-owner Program identity, fresh CPS admission and independent Authority
decision. It must define blast radius, event classes, evidence floors,
cooldowns, rollback, circuit breakers, demotion and kill conditions.

Activation may grant only the exact recommended ladder tier. Approval of tier
`N` does not approve a larger cohort, another action class, another
source/target family, parallel execution or full-incident automation.

After activation, the next real qualifying incident must verify the granted
tier in production. Its outcome returns to M6; success may form the next-tier
recommendation, while failure automatically holds, narrows, freezes or demotes
the class through the existing Authority owner.

`HOLD`, `FREEZE`, `DEMOTE`, `RECOMMEND_NARROW_SCOPE` and
`INSUFFICIENT_EVIDENCE` legally skip M7.

Completion contract:

`ACTION_CLASS_AUTHORITY_DECISION_INDEPENDENTLY_CONSUMED`

## Historical V1.4 verification campaign — retained controls

Every implementation Mission must run:

1. focused unit tests for the changed owner;
2. the exact service-failure episode and passive consumer tests;
3. the exact incident-bound planner/shadow replay;
4. duplicate and cross-process idempotency tests;
5. forbidden-effects verification;
6. affected Permanent Polygon scenarios;
7. commit and push;
8. `tools/v7-safe-deploy` only for the exact approved manifest;
9. a fresh non-test production caller and consumer;
10. affected incident replay;
11. `tools/v7-truth-check --all --json`;
12. `tools/v7-convergence-status --json`;
13. local/GitHub/production commit and runtime snapshot reconciliation.

No Mission may claim `COMPLETE_CONSUMED` from tests, reports, deploy or an
in-process probe alone.

## Forbidden shortcuts

- a second event/opportunity store;
- a second decision or automation-gap engine;
- treating latest-run summary as a queue;
- `continue-on-error`, skipped gates or weakened assertions;
- enabling a timer to manufacture independent automation evidence;
- bulk executable shadow recommendations outside delegated scope;
- directly changing `max_users_per_run`, `max_users_per_channel` or a legacy
  batch budget without current-tier evidence and independent Authority;
- promoting more than one unproven blast-radius tier at once;
- reusing Candidate, Packet, lease, nonce or Authority;
- directly invoking rollback to manufacture a terminal;
- moving ordinary customers solely to create certification evidence;
- relabeling synthetic, operator-induced or unattributed events as Natural L8;
- using legacy runtime policy as current CPS Authority;
- changing Production Maturity from Engineering or shadow evidence.

## Historical V1.4 program terminal — non-executable context

`SERVICE_FAILURE_AUTOMATION_EVOLUTION_LOOP_PRODUCTION_CONSUMED_AND_CERTIFIED_BLAST_RADIUS_TIER_DECIDED`

This terminal means the current Incident and Product Evolution projections are
both reconciled: the incident-to-OMP-to-decision-to-gap-to-shadow-to-outcome-to-
Learning loop is production-consumed, all independent product residuals are
either consumed or explicitly owned, and the current action-class Authority
recommendation, including the exact certified blast-radius tier, has been
independently decided.

It does not necessarily mean autonomous routing is enabled, Natural L8 is
sufficient, Authority expanded or Production Maturity increased.

## Historical V1.4 first frontier — superseded

`V7_SERVICE_FAILURE_AUTOMATION_EVOLUTION_M1_DURABLE_INCIDENT_FRONTIER_AND_OMP_CONSUMER_V1`

V1.5 replaces this with:

`V7_INCIDENT_CAUSAL_CLOSURE_M0_CAUSAL_LOSS_AND_STORAGE_TOPOLOGY_AUDIT_V1`

M0 is read-only. It must prove the exact live location and semantic owner of
the compact incident projection before any schema, retention, partition or
consumer change is proposed.

## V3.1 final performance-closure revision record

The updated final performance-closure Mission before Stage 48 is
`COMPLETE_CONSUMED`. Existing Matrix/path evidence reuse, lightweight user
route binding, a lawful certification-only full transaction, baseline reset,
Outcome/Replay/Learning and Time consumption are production-proven by receipt
`perfclose_1f91af0c6253c6fe75e028c5`.

Exact terminal:

`ONE_GOVERNED_TRANSACTION_FASTEST_SAFE_PATH_PROVEN`

`STAGE_48_OPTIMIZED_RUNTIME_READY`

This revision grants no Stage-48 execution, campaign-stage credit, Natural L8,
Authority expansion or Production Maturity change. The next boundary is the
separate existing-owner admission `STAGE_48_EXISTING_OWNER_ADMISSION_REQUIRED`.

## V3.2 second-level performance revalidation record

Classification: `COMPLETE_CONSUMED`.
Live state owner: `docs/programs/V7_CURRENT_PROGRAM_STATE.md`.
Evidence: `docs/reports/engineering/2026-08-04_155200_second_level_performance_closure_before_stage48.md`.

The existing Time, Matrix, Planner, Packet, lease, governed execution, reset,
Outcome, Replay, Learning, CPS and OMP owners consumed production generation
`stage48-second-level-critical-path-v3` and immutable receipt
`perfclose_6e6c4fa62f834a8d4b88da24`.

The successful forward-and-reset critical path changed from `227.573707 s` to
`141.353447 s`: reduction `86.220260 s` (`37.887%`), speedup `1.61x`.
The complete active-work timeline including a real fail-closed reset and the
automatic recovery generation was `248.210655 s`; this safety/recovery cost is
preserved as evidence and is not misreported as an optimization win.

Existing-owner repairs bounded rotated-history reads, bounded Planner lock
waiting, removed duplicate reset surface construction, and preserved complete
recovery-reset timing. Required verification, Candidate, Packet, lease,
restore-barrier and reset semantics remain intact. The affected suite is green
(`165` tests) and production timing overhead is below `0.016 ms` per recorded
transaction timeline.

Exact terminals:

- `PLANNER_INTERNAL_CRITICAL_PATH_PROVEN`;
- `PACKET_LEASE_INTERNAL_CRITICAL_PATH_PROVEN`;
- `APPLY_VERIFICATION_INTERNAL_CRITICAL_PATH_PROVEN`;
- `RESET_INTERNAL_CRITICAL_PATH_PROVEN`;
- `EVERY_FULL_CYCLE_GT_1_SECOND_INTERVAL_OWNER_ATTRIBUTED`;
- `DOMINANT_REMAINING_AVOIDABLE_LATENCY_REPAIRED`;
- `FULL_GOVERNED_FORWARD_AND_RESET_BEFORE_AFTER_REBENCHMARK_CONSUMED`;
- `TIME_OPTIMIZATION_LOOP_PRODUCTION_RECONSUMED`;
- `FULL_GOVERNED_FORWARD_AND_RESET_FASTEST_SAFE_PATH_PROVEN`;
- `STAGE_48_OPTIMIZED_RUNTIME_READY_REVALIDATED`.

Receipt semantics remain readiness only. `stage_48_executed=false`,
`campaign_stage_credit=false`, no Natural L8 credit, Authority expansion or
Production Maturity change exists. The exact next boundary remains
`WAITING_INPUT:STAGE_48_EXISTING_OWNER_ADMISSION`.

## V4.0 constant-time cohort failover execution plan

Status: `APPROVED_EXECUTION_PLAN`.
Activation state owner: `CPS`.
OMP integration owner: `V7.OMP.FINAL.PRODUCTION_PROGRAM`.

This section defines the approved capability stages for making service-failure
recovery independent of user count. It does not activate a Mission, grant
Authority, change Runtime, migrate users, write policy, create a Packet or
execute Stage 48. CPS remains the sole live frontier owner.

The target architecture extends existing route, registry, Matrix, Planner,
Candidate, Packet, lease, execution, verification, rollback, Outcome, Replay,
Learning, Polygon, OMP and CPS owners. It must not create a second route owner,
user registry, Planner, Runtime, event bus, watcher, queue, scheduler, evidence
store, Authority owner or truth source.

### V4.0 primary engineering intent

Replace the current user-linear governed mutation model:

```text
N users
-> N route intents
-> repeated validation / mutation / reset work
```

with a class/bucket generation model:

```text
user membership generation
+ semantic routing class
+ bounded exception overlay
-> class/bucket to egress generation
-> one bounded kernel commit per affected bucket
```

The required complexity invariant is:

`CUTOVER_COMPLEXITY_INDEPENDENT_OF_USER_COUNT_AND_BOUNDED_BY_CERTIFIED_BUCKET_AND_TARGET_COUNT`.

The Program must prove the invariant. It must not assume that the current
Linux data plane can express it.

### V4.0 current measured reason for admission

The immutable production baseline is `227.573707 s`. Second-level
revalidation receipt `perfclose_6e6c4fa62f834a8d4b88da24` proves a successful
forward-and-reset critical path of `141.353447 s`, but the current low-level
writer still consumes one user identity, takes a shared lock, validates one
execution control, writes one route and rewrites the user registry. Current
availability-first cleanup iterates reset transactions per moved user. Further
small optimization of this model cannot establish 10,000-user recovery.

This evidence admits architecture/reality reconciliation. It does not prove a
specific nftables, fwmark, route-table, namespace, peer-routing or other kernel
solution.

### V4.0 non-negotiable closure law

No Mission, function, adapter, projection, kernel primitive, migration step,
verification step or report is complete merely because code or output exists.
Every stage must close this exact chain:

```text
owner-backed trigger
-> producer invoked
-> output produced
-> output durably reachable
-> named existing consumer invoked
-> consumer acknowledges exact generation
-> consumer behavior changes or exact STOP_SAFE is produced
-> verification consumes observed behavior
-> next output is produced
-> atomic CPS projection
-> OMP residual recomputation
-> durable exact successor or legal terminal
```

The following states are invalid:

```text
output exists AND consumer is empty
consumer acknowledged AND next output is empty
non-terminal stage AND successor is empty
open migration generation AND re-entry condition is empty
kernel generation differs from canonical generation AND recovery owner is empty
active routing class AND verification/rollback consumer is empty
```

Any such state is `BROKEN_CAUSAL_LINEAGE`, not `COMPLETE`, `NO_WORK`,
`REAL_WORLD_LIMIT` or `PROGRAM_TERMINAL`.

Reports are historical evidence only. Tests, commit, deploy and read models are
intermediate outputs until their named non-test consumers have acted.

### V4.0 routing-class semantic identity

A routing class is not merely all users currently on one source. Its identity
must be derived through existing owners from every material compatibility
dimension:

- policy and service-routing profile;
- current source and allowed targets;
- country/geography restrictions;
- DNS, mark, table, tunnel, MTU, NAT and conntrack semantics;
- rollback or forward-recovery class;
- Authority tier and blast contract;
- target/path/config/Matrix fingerprints;
- membership and exception generations.

The eligible cohort formula is immutable for one execution generation:

```text
source-compatible members
- operator-pinned users
- incompatible path/profile identities
- capacity exclusions
- active-transaction subjects
- contradictory or stale identities
- explicit exception overlay
= exact eligible routing-class cohort
```

The class default may be overridden only by an exact existing-owner exception
record. A shared source alone never authorizes shared movement.

### V4.0 truth and storage model

The existing user registry remains the canonical membership owner, but an
emergency class cutover must not rewrite every user row. Canonical state is:

```text
user -> routing_class_id / membership_generation
routing_class -> desired_egress / class_generation
exception overlay -> exact user override / exception_generation
effective route = membership + class generation + exception overlay
```

The existing owner may publish a compact current projection containing class
ID, count, membership fingerprint, immutable snapshot pointer, exception
fingerprint, demand envelope, source binding, target allocation and rollback /
forward-recovery bindings. Fast-path execution must not scan all users.

One cohort Packet must not duplicate 10,000 user objects. It binds the exact
membership snapshot pointer and fingerprint, count, bucket allocation,
exceptions fingerprint, capacity reservation, policy/Authority envelope,
verification contract and recovery generation. Exact replay must remain
possible through the existing membership owner; a hash with no recoverable
snapshot is insufficient.

### V4.0 atomic commit protocol

`atomic` means one observable kernel generation per bounded bucket, no mixed
old/new generation inside that bucket, and deterministic crash recovery. It
does not claim that filesystem and kernel writes share one transaction.

The required protocol is:

```text
PREPARED durable intent
-> canonical generation compare-and-swap
-> bounded kernel transaction
-> observed kernel generation / effective path
-> COMMITTED receipt
-> verification
-> Outcome / Replay / Learning
```

Crash reconciliation must classify:

- crash before CAS: cancel or supersede PREPARED intent;
- crash after CAS but before kernel commit: complete or revert from current
  canonical and kernel truth;
- crash after kernel commit but before receipt: observe kernel state and close
  the same idempotent operation;
- unknown or mixed state: `STOP_SAFE_KERNEL_CANONICAL_RECONCILIATION_REQUIRED`;
- duplicate invocation: consume the original terminal without a second apply.

Required terminal:
`KERNEL_AND_CANONICAL_GENERATION_COMMIT_PROTOCOL_PROVEN`.

### V4.0 capacity and multi-target law

Capacity is reserved before cutover using demand, not only user count:

`reserved_capacity >= eligible_cohort_demand + certified_safety_reserve`.

For multiple targets, complexity is O(K), where K is a bounded certified
bucket/target count independent of N users. The existing Planner must produce
deterministic partitioned classes or buckets, target allocation, spillover and
exception decisions before the incident fast path. No event-time global
reallocation or user scan is allowed.

One all-user target switch is legal only when one target can safely own the
entire eligible cohort. Otherwise the execution uses a bounded number of
precomputed buckets and trips the existing circuit breaker before expanding to
another bucket after a failed verification.

### V4.0 verification and session law

The cutover path may reuse heavy service evidence only when the existing Matrix
receipt has matching path/config/egress/service-set fingerprints, freshness,
target-health, invalidation and capacity semantics.

Synchronous verification includes:

- live policy/Authority/generation match;
- current target and reservation match;
- kernel generation and route visibility;
- lightweight binding/counter evidence;
- circuit-breaker readiness.

Path-level service verification, cohort reconciliation, exception discovery,
Outcome, Replay and Learning may continue after cutover through their existing
consumers. Deferred does not mean optional: failure must produce recovery or
containment and a legal terminal.

Separate measured SLO domains are mandatory:

- failure detection latency;
- decision/admission latency;
- kernel generation commit latency;
- new-flow recovery latency;
- existing-flow/conntrack recovery latency;
- application-visible recovery latency;
- asynchronous evidence closure latency.

Conntrack mutation is forbidden until the existing owner proves whether
sessions survive egress changes and whether exact class-scoped invalidation is
safe. New-flow recovery must not be reported as existing-flow or application
recovery.

Rollback has two distinct forms:

- generation rollback to a still-eligible previous source;
- forward recovery to another precomputed target when the source is dead,
  invalid, uncredentialed, capacity-unsafe or policy-ineligible.

Direct rollback to a failed source is forbidden.

### V4.0 measured SLO law

Initial subsecond values are `TARGET_SLO_HYPOTHESIS`, not certification truth.
M0 and Polygon establish the measured lower bound and owner-backed SLO.

The primary invariant is independence from N. Absolute targets are admitted
only after measurement. The initial engineering hypotheses are:

- prepared decision/admission: sub-100 ms;
- bounded class/bucket kernel commit: sub-250 ms;
- route visibility: sub-100 ms;
- new-flow recovery: sub-second where tunnel/NAT semantics permit;
- heavy service and evidence closure: outside the cutover critical path.

p50/p95/p99 must not be fabricated from insufficient samples.

### V4.1 M0 hot-path, invalidation and foundation refinement

V4.1 narrows the first execution step. It does not assume that users sharing
one source already form one routing class, does not preselect a kernel
primitive and does not create a Foundation Mission ceremonially. CT-M0 must
first prove the current producer-consumer reality and classify every reusable
primitive by semantics, not by name.

The required hot-path dependency graph is:

```text
failure signal
-> prepared decision
-> hot validation
-> cohort Packet
-> cohort lease
-> generation commit
-> kernel visibility
-> fast verification
-> deferred closure
```

For every edge CT-M0 records the actual producer, consumer, schema, freshness,
invalidation conditions, blocking/deferred class, `O(1)`/`O(K)`/`O(N)` cost,
production caller and exact failure terminal. Serialization, hashing, audit
materialization and membership-list handling count as hot-path work when they
block the next edge; hidden `O(N)` work is forbidden.

Prepared decisions are caches, not truth. Their exact invalidators include at
least target-health generation, Matrix/path fingerprint, capacity/reservation,
policy/Authority generation, cohort membership, exclusions, source-incident
generation, anti-flap state, target correlation domain, active operation and
rollback-target availability. The hot validator compares these bounded
generations and fingerprints; it must not rebuild the whole World Model.

Class identity is an M0 output, not an input assumption. M0 determines whether
a class is defined by source channel, channel profile/path fingerprint, policy
set, target-eligibility set, capacity bucket, service-routing compatibility
and exception boundary. Users on one source may belong to different classes.

Deferred closure is durable and crash-recoverable. The `PREPARED` intent must
already carry a closure seed containing operation/generation identity,
expected kernel transition, verification contract, exception reconciliation,
Outcome/Replay/Learning consumers and recovery law:

```text
PREPARED + closure seed
-> generation CAS
-> kernel commit
-> COMMITTED
-> durable closure obligation activation
-> independent existing consumer
-> service verification
-> exception reconciliation
-> Outcome / Replay / Learning
-> bounded terminal
```

A crash before apply closes the seed as `NOT_APPLIED`. A crash after kernel
commit reactivates exactly one closure obligation from canonical generation
and kernel truth. Duplicate recovery must not create a second obligation.

Mass compatible incidents select the class path. The legacy per-user path is
allowed only for pinned users, incompatible fingerprints, membership
migration, partial class failure, contradictory identity, exception overlays,
reconciliation or unsupported legacy membership. The machine invariant is:

`LEGACY_PER_USER_PATH_FOR_MASS_COMPATIBLE_INCIDENT_FORBIDDEN`.

### V4.5 performance ledger and hot-path regression law

Every CT Mission must update
`CONSTANT_TIME_FAILOVER_PERFORMANCE_LEDGER`, a projection of the existing
`execution_performance_foundation` and canonical Time owner. It is not a new
store, registry, log owner or truth source. The existing OMP consumer must
consume each projection before the Mission may close.

Every stage row contains:

- old and new critical path, removed and remaining blocking work;
- `O(1)`/`O(K)`/`O(N)` classification and the exact cause;
- detection, prepared-decision validation, Packet/lease, canonical CAS,
  kernel commit, visibility, fast verification, new-flow recovery, closure
  activation, deferred verification, rollback and forward-recovery latency;
- measured 10-member and 10,000-member time, difference and cause, or exact
  not-yet-measurable reason;
- dependence on N and K;
- bytes/records scanned, registry rows rewritten, synchronous audit records,
  member probes, Candidates/Packets/leases, process count, lock count and
  network probes;
- monotonic start/end boundaries, cold/warm classification, sample count,
  p50/p95/p99 where statistically valid, CPU/load/substrate fingerprint;
- first-failed-observation, confirmed-failure and recovered-client boundaries,
  clock domain/uncertainty, probe cadence/resolution and probe validity;
- operation/class/bucket/generation identity;
- unknown time and the next exact latency residual.

Wall-clock timestamps preserve lineage; elapsed SLO measurement uses the
existing monotonic Time contract. Unknown time is `UNKNOWN`, never zero.
Improvement in one interval cannot hide an undeclared regression in another:
`LATENCY_REGRESSION_WITHOUT_EXACT_RESIDUAL_FORBIDDEN`.

The legacy exception path receives its own measured contract. CT-M0 must split
the current baseline, including the observed approximately 141-second path,
into necessary safety checks, duplicated work, waits, probes, locks and unknown
time. It then emits `LEGACY_EXCEPTION_PATH_REQUIRED_SLO`; the value is derived
from evidence, not selected in advance. Safe but operationally unusable
latency remains an engineering residual. Required M0 terminal:
`LEGACY_EXCEPTION_PATH_BASELINE_AND_REQUIRED_SLO_PROVEN`.

Prepared decisions must exist before a failure. Existing Matrix, topology,
capacity, policy and membership generation owners drive selective refresh:

```text
owner generation change
-> selective prepared-decision invalidation
-> refreshed prepared decision
-> freshness consumer acknowledgement
-> READY_FOR_HOT_VALIDATION
```

No new daemon is permitted. A missing or stale prepared decision fails the
class fast path with an exact reason; it must not silently place the full
Planner on the incident critical path. Required terminal:
`PREPARED_DECISION_CONTINUOUS_PRODUCER_AND_FRESHNESS_CONSUMER_PROVEN`.

Full service verification is forbidden before cutover when a fresh compatible
Matrix receipt exists and no declared invalidator fired. Full or bounded
revalidation is legal only for an exact stale receipt, fingerprint mismatch,
changed target, service set, DNS/routing/config generation or contradictory
evidence, and must follow the existing safety owner. Required terminal:
`FRESH_MATRIX_RECEIPT_HOT_PATH_REUSE_GUARD_PROVEN`.

The class cutover hot path must not serialize or hash the full member list,
scan the registry, rewrite registry rows, generate per-member audit records,
verify every member synchronously or create per-member Candidate, Packet or
lease objects. Membership fingerprint and snapshot generation are prepared
before the incident; cutover performs only bounded validation. Instrumented
counters enforce: `CUTOVER_HIDDEN_O_N_GUARD_PROVEN`.

### Mission CT-M0 — current owner, data-plane and O(N) audit

Mission ID:
`V7_CONSTANT_TIME_COHORT_FAILOVER_M0_CURRENT_OWNER_DATAPLANE_AND_O_N_COST_RECONCILIATION_V1`.

Execution class: `DISCOVERY_COMPLETION`, read-only.

Required discovery:

1. Exact current forward and reset process/lock/read/write/mutation graph.
2. O(N), O(K) and O(1) operations and measured cost.
3. Existing `ip rule`, tables, fwmark, nftables, map/set, namespace, peer and
   policy-routing primitives actually present on production and Polygon.
4. Whether current data plane can express class-to-egress indirection.
5. Existing route/registry owner extension point; no second owner.
6. Canonical membership and compact projection feasibility.
7. Semantic class and exception formula.
8. Single-target and multi-target deterministic partitioning.
9. Capacity demand/reservation owner and safety reserve.
10. Kernel/canonical generation and crash reconciliation feasibility.
11. Existing-flow, NAT and conntrack behavior.
12. Existing hard-failure event producer, event generation, consumer,
    duplicate/stale suppression, anti-flap and watchdog route.
13. Matrix receipt reuse/freshness/invalidation rules.
14. Coexistence, migration, fallback and rollback plan.
15. Available logical and privileged Polygon substrate.
16. The complete hot-path dependency graph and every blocking/deferred edge.
17. Prepared-decision invalidation generations and bounded hot-validator law.
18. Durable closure seed, activation and crash-recovery ownership.
19. Legacy/class selection law and exact legacy exception scope.
20. Semantic routing-class identity dimensions proven by current data.
21. Disposition of every existing primitive without duplicate ownership.
22. Existing Time/execution performance projection owner and baseline ledger.
23. Legacy exception-path latency decomposition and evidence-derived SLO.
24. Existing event producers and freshness consumer for continuously prepared
    decisions.
25. Matrix receipt reuse guard and exact invalidation-only revalidation path.
26. Instrumented hidden-O(N) operation counters and regression thresholds.

Every primitive receives exactly one disposition:

- `REUSE_VALID` — record and do not modify;
- `EXTEND_FOR_CLASS_OPERATION` — include only the missing semantic delta in
  the conditional Foundation Mission;
- `REPLACE_INTERNAL_PRIMITIVE_WITHIN_EXISTING_OWNER` — replace only inside the
  canonical owner with migration/rollback proof;
- `LEGACY_EXCEPTION_PATH_ONLY` — certify its exact exception scope and exclude
  it from the mass hot path;
- `NOT_REQUIRED_FOR_FAST_PATH` — bind it to deferred closure or leave it
  outside the critical path;
- `BLOCKS_CONSTANT_TIME_MODEL` — publish the exact mandatory architecture
  residual and continue every independent criterion.

Positive kernel feasibility is emitted as
`KERNEL_CLASS_INDIRECTION_FEASIBILITY_PROVEN`. A non-positive result must name
the exact `REUSE`, `EXTEND`, `MIGRATION` or `BLOCKS_CONSTANT_TIME_MODEL`
verdict; feasibility must never be implied by plan text.

Producer: existing route/registry/Matrix/Planner/Runtime read-only owners.
Output: one machine-readable M0 contract containing all of:

- `REUSABLE_PRIMITIVE_DISPOSITION_MATRIX`;
- `CURRENT_O_N_AND_O_1_COST_MODEL_PROVEN`;
- `KERNEL_CLASS_INDIRECTION_FEASIBILITY_DECIDED`;
- `CONSTANT_TIME_HOT_PATH_PRODUCER_CONSUMER_GRAPH_PROVEN`;
- `PREPARED_DECISION_INVALIDATION_CONTRACT_PROVEN`;
- `ROUTING_CLASS_SEMANTIC_IDENTITY_CONTRACT_PROVEN`;
- `LEGACY_EXCEPTION_SCOPE_DEFINED`;
- `DEFERRED_CLOSURE_DURABLE_SUCCESSOR_CONTRACT_DEFINED`;
- `CONSTANT_TIME_FAILOVER_PERFORMANCE_LEDGER` baseline projection;
- `LEGACY_EXCEPTION_PATH_BASELINE_AND_REQUIRED_SLO_PROVEN`;
- `PREPARED_DECISION_CONTINUOUS_PRODUCER_AND_FRESHNESS_CONSUMER_PROVEN` or the
  exact existing-owner Foundation residual required to prove it;
- `FRESH_MATRIX_RECEIPT_HOT_PATH_REUSE_GUARD_PROVEN` or its exact residual;
- `CUTOVER_HIDDEN_O_N_GUARD_PROVEN` or its exact instrumentation residual;
- the explicit list of forbidden duplicate owners;
- the exact conditional Foundation residual, if any;
- the exact CT-M1 identity and dependency state;
- exactly one executable successor.

Consumer: BDP Reality Gate -> OMP Candidate Admission.
Expected next output is machine-exclusive:

- when any `EXTEND_FOR_CLASS_OPERATION` or
  `REPLACE_INTERNAL_PRIMITIVE_WITHIN_EXISTING_OWNER` residual exists, admit
  CT-M0F as `READY` and form CT-M1 as `FORMED_DEPENDENCY_BLOCKED`;
- when no Foundation residual exists, admit CT-M1 as `READY`;
- when a constant-time blocker remains, publish that exact residual with
  durable re-entry while continuing independent safe criteria.

CT-M0F and CT-M1 must never both be `READY`.

M0 cannot complete at an Engineering Report. Required terminal:
`CURRENT_DATAPLANE_CLASS_INDIRECTION_FEASIBILITY_AND_MINIMAL_IMPLEMENTATION_FRONTIER_CONSUMED`,
with every required M0 subterminal above consumed.

### Conditional Mission CT-M0F — reusable fast primitives closure

Mission ID:
`V7_CONSTANT_TIME_COHORT_FAILOVER_REUSABLE_FAST_PRIMITIVES_CLOSURE_V1`.

This Mission exists only when CT-M0 proves an `EXTEND` or owner-internal
`REPLACE` residual. It reuses current Planner preparation/fallback, failure
validation, Packet/lease, Matrix, lightweight verification, route/reset safety,
Outcome/Replay/Learning and Time owners where semantically valid. The current
per-user writer and sequential reset remain legacy exception paths unless M0
proves otherwise. These are hypotheses for M0 classification, not advance
verdicts.

The Mission closes only the exact missing existing-owner links required for
class operation, the prepared-decision invalidation contract, closure seed and
legacy selection law. It also closes only proven residuals for the performance
ledger projection, legacy fallback SLO, continuous prepared-decision producer,
Matrix receipt guard and hidden-O(N) instrumentation. It may not create a route
owner, registry, queue, watcher, Planner, Runtime, Authority system or parallel
truth source.

Internal phase `CT-M0F-E_ENGINEERING` must implement and deploy prepared
decision production, bounded generation validation, the fresh-Matrix hot-path
guard, bounded legacy registry mutation, traffic-recovery instrumentation,
deferred closure activation and hidden-O(N) counters through the existing
owners. It cannot create or execute a production Packet.

Internal phase `CT-M0F-V_CONTROLLED_VALIDATION` must then use the existing
Controlled Production Certification Program for exactly the current legacy
single-user path and the V4.5 ordered SLO and measurement contract. Its
evidence proves only current-path latency and fallback operability. It cannot
certify class/bucket
indirection, satisfy CT-M8, manufacture Natural L8, expand Runtime scope or
advance Authority/Production Maturity.

Producer: exact existing owners named by the M0 disposition matrix.
Output: repaired/reused fast primitives plus certified legacy exception
selection contract.
Consumer: focused non-test owner callers -> safe deploy/truth/convergence ->
existing Controlled Production Certification owner -> Time/Outcome/Replay/
Learning -> BDP/OMP residual recomputation.
Terminal:
`REUSABLE_FAST_PATH_PRIMITIVES_PROVEN_AND_LEGACY_EXCEPTION_FALLBACK_CERTIFIED`.
Successor: CT-M1 becomes `READY` only after this terminal is consumed.

Every CT-M0F result must include a consumed performance-ledger delta. Passing
functional tests without old/new critical-path evidence is incomplete.
CT-M0F cannot reach its terminal until every V4.5 current-client terminal is
consumed. CT-M1 remains `FORMED_DEPENDENCY_BLOCKED` while either E or V is
incomplete.

### Mission CT-M1 — Polygon kernel primitive and generation protocol

Reuse or extend only the existing route owner. Prove in isolated Polygon:

```text
membership generation
-> class/bucket generation CAS
-> kernel commit
-> visibility
-> new-flow verification
-> generation rollback / forward recovery
```

Test 10 and 10,000 logical members against the same bounded bucket count, then
use the highest honest available kernel substrate. Measure N-independence,
kernel cost, memory, audit volume and crash points. Missing privileged
substrate preserves a specific kernel criterion but cannot block independent
logical, identity, migration or recovery work.

Producer: existing route owner extension plus existing Polygon executor.
Output: isolated primitive receipt and exact residuals.
Consumer: Polygon result consumer -> BDP/OMP mismatch or CT-M2 admission.
Terminal:
`CONSTANT_TIME_CLASS_BUCKET_KERNEL_PRIMITIVE_AND_CRASH_PROTOCOL_POLYGON_CONSUMED`.

### Mission CT-M2 — canonical membership, exceptions and compact projection

Extend the existing registry/read-model owner so membership, class generation,
exceptions, demand and immutable snapshot lineage are explicit without event-
time full scans or mass route rewrites.

Prove duplicate suppression, snapshot replay, exception priority, pinned users,
contradictory identities, active transactions, class reclassification and
compact audit retention at 10,000 members.

Producer: existing registry and routing-class projection owner.
Output: generation-bound membership/exception projection.
Consumer: existing Planner, Packet and migration owners.
Terminal:
`ROUTING_CLASS_MEMBERSHIP_EXCEPTION_AND_COMPACT_PROJECTION_CONSUMED`.

### Mission CT-M3 — shadow parity and bounded migration

One-time migration is allowed to be O(N); incident cutover is not. Migration
must be incremental and independently reversible:

```text
legacy per-user route
-> shadow class effective-route projection
-> parity verification
-> bounded migration batch
-> kernel/canonical verification
-> next batch or rollback
```

Legacy and class models may coexist only with one explicit authoritative
runtime generation and deterministic precedence. Mixed truth is forbidden.
The old path remains fallback until the migrated scope passes parity,
restart/crash, rollback and no-regression verification.

Producer: existing migration-capable route/registry owner.
Output: verified migrated membership generation and exception set.
Consumer: existing Runtime/verification owner -> OMP residual recomputation.
Terminal:
`BOUNDED_ROUTING_CLASS_MIGRATION_AND_LEGACY_FALLBACK_PARITY_CONSUMED`.

### Mission CT-M4 — cohort Packet, lease and fast apply

Extend the existing Candidate/Packet/lease/governed execution owners so one
fresh Packet binds one immutable class/bucket operation rather than repeating
one full lifecycle per member.

Live source, target, policy, Authority, capacity, freshness, anti-flap,
restore/forward-recovery and verification gates remain mandatory. One Packet
must never become permission for another generation, class, target or bucket.

Producer: existing Planner/Candidate/Packet/lease owners.
Output: exact class/bucket execution intent.
Consumer: existing governed route owner.
Terminal:
`ONE_CLASS_BUCKET_ONE_PACKET_ONE_LEASE_FAST_APPLY_CONSUMED`.

### Mission CT-M5 — event-driven fast path and verification split

Discover and reuse the current hard-failure producer. Repair only a missing
producer-consumer binding. Do not introduce an event bus, watcher or daemon.

Required chain:

```text
hard-failure generation
-> existing event owner
-> duplicate/stale/anti-flap arbitration
-> prepared class/bucket decision
-> fresh governed admission
-> kernel commit
-> fast verification
-> durable deferred verification successor
```

Timer remains watchdog. It is not the primary cutover wake.

The measured hot path must enforce the V4.5 class-path engineering budgets:
failure detection p95 <= `2,000 ms`, prepared-decision validation plus kernel
commit p95 <= `250 ms`, route visibility p95 <= `100 ms`, and zero hidden full
Planner or O(N) member work. CT-M5 evidence does not by itself claim
route-bound production client recovery.

Producer: existing failure/Matrix/Sentinel event owner.
Output: exact fast-path trigger and operation generation.
Consumer: existing governed executor, verification and successor owners.
Terminal:
`HARD_FAILURE_EVENT_TO_FAST_CUTOVER_AND_DEFERRED_VERIFICATION_CHAIN_CONSUMED`.

### Mission CT-M6 — constant-time recovery and causal closure

Prove both generation rollback and forward recovery, including dead source,
target failure, partial bucket expansion, service verification failure,
duplicate invocation, restart and terminal loss.

Every operation must close through Outcome, Replay, Learning, compact cohort
receipt, exception reconciliation, CPS and OMP. Deferred evidence may outlive
cutover but may not be abandoned.

Producer: existing verification/recovery owner.
Output: verified success, rollback, forward recovery or containment terminal.
Consumer: Outcome/Replay/Learning -> CPS/OMP.
Terminal:
`CONSTANT_TIME_RECOVERY_AND_FULL_CAUSAL_CLOSURE_CONSUMED`.

### Mission CT-M7 — 10,000-member Polygon scale certification

Polygon coverage must include:

- 10 versus 10,000 members with equal certified bucket count;
- one and multiple targets;
- capacity exhaustion and spillover;
- pinned and incompatible exceptions;
- stale/mismatched membership and Matrix generations;
- simultaneous incidents, event storms, duplicates and anti-flap;
- crash before CAS, after CAS, after kernel commit and before receipt;
- kernel partial/mixed-state detection;
- target failure, rollback and forward recovery;
- process restart and deterministic replay;
- audit/storage/memory growth;
- new-flow and, where safely supported, existing-flow behavior.

Logical simulation alone cannot close kernel scale. Real kernel substrate alone
cannot close semantic membership and recovery. Both evidence classes remain
explicit.

Certification is residual-based. Identical effects are not ceremonially
repeated at 1/2/5/10/25/48/100/500/1000. A scale point exists only when it
closes a new memory, membership, audit, capacity, exception, kernel, recovery
or blast residual.

Producer: existing Polygon and component owners.
Output: scale/latency/behavior receipt with measured SLO.
Consumer: OMP certification and Product Evolution Frontier.
Terminal:
`TEN_THOUSAND_MEMBER_N_INDEPENDENT_FAILOVER_POLYGON_CERTIFIED`.

For equal certified bucket count, 10 versus 10,000 members must preserve the
declared constant-time tolerance for validation, kernel commit and visibility.
Polygon may certify the subsecond engineering path; it cannot manufacture the
CT-M8 production traffic-recovery receipt.

### Mission CT-M8 — bounded controlled-production certification

Production starts only after CT-M7 and an exact existing-owner admission.
Use certification identities/classes only. Ordinary users must never be moved
solely to manufacture evidence.

Controlled production validates only residual blast classes: one bucket,
multiple buckets, multiple targets, exception handling, rollback and forward
recovery. It must not replay every numeric scale already proven by Polygon.

The controlled-production Time owner must measure exact route-bound traffic.
The class target is p95 `<1,000 ms`; p99 `<=5,000 ms` becomes a legal claim only
after at least 100 owner-backed observations. A smaller sample set preserves
`INSUFFICIENT_SAMPLE_COUNT` for p99 without blocking independently proven p95,
safety, recovery or causal-closure criteria. No production action may be
created only to populate this distribution.

Producer: existing Controlled Production Certification Program.
Output: owner-backed Outcome Passports and measured recovery SLO.
Consumer: existing calibration, Learning, Production Maturity evidence and
Authority recommendation owners.
Terminal:
`CONSTANT_TIME_COHORT_FAILOVER_CONTROLLED_PRODUCTION_EVIDENCE_RECONCILED`.

### Mission CT-M9 — Authority and Runtime recommendation

Existing Authority owner independently returns one of:

- `RECOMMEND_CERTIFIED_CLASS_BUCKET_SCOPE`;
- `RECOMMEND_NARROW_SCOPE`;
- `HOLD_GOVERNED_ONLY`;
- `FREEZE`;
- `DEMOTE`;
- `INSUFFICIENT_EVIDENCE`.

Engineering, Polygon, CPS and OMP cannot grant Authority. Approval, if any,
must name exact class identities, bucket/target ceiling, demand/capacity
reserve, concurrency, expiry, verification, recovery, exception and circuit-
breaker contracts. Self-expansion is forbidden.

Producer: existing evidence/calibration owner.
Output: immutable eligibility set and recommendation.
Consumer: independent Authority owner; Runtime enablement remains separately
owned.
Terminal:
`CONSTANT_TIME_COHORT_FAILOVER_AUTHORITY_AND_RUNTIME_RECOMMENDATION_DECIDED`.

### V4.5 dynamic Mission compression

CT-M0 is mandatory. CT-M0F is conditional on the exact M0 disposition matrix.
CT-M1 through CT-M9 are capability stages, not mandatory empty containers.
Exactly one stage may be `READY`; a downstream stage may be formed as
`FORMED_DEPENDENCY_BLOCKED` but cannot execute early. After each consumed
output OMP must:

1. re-read CPS and current owners;
2. recompute remaining criteria;
3. mark already consumed stages `MISSION_NOT_REQUIRED_ALREADY_CONSUMED`;
4. reduce partially closed stages to exact residual producer-consumer links;
5. merge stages only when owner, evidence class, isolation, verification,
   recovery and terminal semantics remain explicit;
6. publish and consume the smallest safe successor;
7. stop only at a legal terminal with exact re-entry.

Dynamic compression may reuse valid functional evidence, but it may not skip a
missing stage performance-ledger projection or hide a latency regression.

An unavailable kernel/privileged substrate cannot stop independent logical,
identity, migration, projection, replay or model work. It is
`POLYGON_SUBSTRATE_LIMIT` for the exact criterion, never global
`REAL_WORLD_LIMIT` while independent safe work exists.

### V4.5 production-effect boundary

| Mission | Production routing/user effect |
| --- | --- |
| CT-M0 | forbidden; read-only |
| CT-M0F-E | forbidden; engineering/Polygon and non-test owner callers only |
| CT-M0F-V | one certification identity only through an exact existing-owner controlled-production contract; legacy latency proof only; no CT-M8/class/Authority/Maturity credit |
| CT-M1 | forbidden; isolated Polygon only |
| CT-M2 | forbidden; projection/shadow only |
| CT-M3 | only separately admitted bounded migration; otherwise shadow |
| CT-M4 | no production apply until existing Authority and Runtime gates pass |
| CT-M5 | production action only through the already approved exact class contract |
| CT-M6 | rollback/forward recovery only for the exact admitted operation |
| CT-M7 | forbidden; Polygon only |
| CT-M8 | bounded certification-only production through existing owner |
| CT-M9 | recommendation only; no Authority or Runtime mutation |

Forbidden without the exact current owner-backed contract remain policy write,
Authority expansion, Packet execution, restore-barrier write, routing
mutation, user movement, rollback/forward-recovery apply, ordinary-user
certification use and Production Maturity change.

### V4.5 Program completion contract

This capability plan reaches its program terminal only when all current
criteria are owner-backed and consumed:

- current data-plane feasibility and O(N)/O(K)/O(1) model proven;
- current single-user client traffic recovery and reset traffic recovery are
  measured independently from full durable closure;
- the CT-M0F post-deploy controlled legacy benchmark consumes both the V4.5
  transitional ceiling and operational `<3,000 ms` gate, or CT-M0F remains
  open at the exact owner-backed latency residual;
- heavy verification, Outcome/Replay/Learning and reset closure do not retain
  the client recovery terminal;
- the existing Time owner has consumed a performance-ledger row for every
  executed or compressed CT stage;
- old/new critical paths, 10/10,000 comparison, hidden-operation counters and
  next latency residual are explicit;
- legacy exception fallback has an evidence-derived bounded SLO;
- prepared decisions are continuously produced and freshness-consumed before
  incidents without a new daemon;
- fresh compatible Matrix receipts prevent full pre-cutover verification;
- no hidden incident-time member serialization, hashing, scanning, rewrite,
  per-member audit/verification or per-member Packet lifecycle remains;
- hot-path producer-consumer graph and hidden blocking work proven;
- prepared-decision invalidation contract consumed;
- semantic routing-class identity and legacy exception scope proven;
- durable closure seed/successor crash contract and runtime behavior proven;
- every primitive disposition consumed without duplicate owners;
- conditional Foundation Mission completed or proven unnecessary;
- existing-owner class/bucket primitive selected and implemented;
- kernel/canonical crash protocol consumed;
- canonical membership, exceptions and immutable snapshot replay consumed;
- migration and fallback parity consumed;
- mass compatible incidents select the class path and legacy fallback is
  production-certified only for explicit exceptions;
- one Packet/lease class operation consumed;
- event-to-fast-path consumer production-proven;
- fast and deferred verification both close;
- rollback and forward recovery close;
- 10,000-member logical and kernel Polygon criteria close;
- controlled-production residuals are reconciled or exact Authority/
  real-world boundaries remain;
- the prepared class/bucket path proves `<1,000 ms` p95 route-bound client
  recovery in CT-M8; any p99 claim follows the V4.5 sample-count law;
- Authority/Runtime recommendation is independently decided;
- no open stage lacks `next_required_consumer` or `reentry_condition`;
- CPS, OMP and Runtime projections agree;
- local, GitHub and production identity align after any deploy;
- every safe residual has one durable automatic successor.

Only then may OMP emit:

`CONSTANT_TIME_COHORT_FAILOVER_CAPABILITY_FULL_CAUSAL_LOOP_CONSUMED`.

This terminal does not itself mean full production Authority, all-user
movement, Natural L8 sufficiency or Production Maturity increase.
