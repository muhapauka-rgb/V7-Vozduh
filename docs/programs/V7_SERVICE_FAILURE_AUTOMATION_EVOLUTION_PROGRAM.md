# V7 Service Failure Automation Evolution Program

Version: `5.3`

Status: `APPROVED_EXECUTION_PLAN`

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
-> CLIENT TRAFFIC RECOVERED
```

The primary product KPI remains `T0 FAILURE CONFIRMED -> T11 CLIENT TRAFFIC
RECOVERED`. This workstream additionally owns the Engineering measurement
residual `FIRST OBSERVABLE FAILURE SIGNAL -> CANONICAL CONFIRMED FAILURE
EVENT`; it does not redefine T0 or move report/OMP time into Runtime.

### V5.3 current role-based recovery amendment (N0–N11)

**Status:** `CURRENT_EXECUTION_CONTRACT`.  This amendment replaces the
remaining V5.3 execution order where it conflicts with this section.  It is
not a new Program, Mission, Matrix, health truth, Runtime, Planner, queue,
watcher, timer, registry, state store, event family or Authority surface.
Earlier L1–L12 and Phase A–H text is retained only as evidence, historical
candidate rationale and reusable sub-gates; it must not restore the former
meaning of C8 or Full Matrix.

The product must not be optimized as one large health sweep.  It is a layered,
cost-bounded path under the existing owners:

```text
BAD OR UNUSABLE CURRENT SOURCE
-> EARLY SERVER-SIDE SIGNAL
-> BOUNDED INDEPENDENT CONFIRMATION
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

| Class | Minimum causal path | Measured target | Explicit non-goal |
| --- | --- | --- | --- |
| `HARD_PATH` | definitive existing OS/systemd/interface/tunnel/peer/route evidence or cheap path liveness -> independent targeted Matrix corroboration -> T0 -> S11 | controlled failure onset -> S11 P95 `<=3 s`, max `<=5 s`; production observation clock retained separately | full deep sweep before an unambiguous failure |
| `TELEGRAM_CRITICAL` | Telegram is required by the active product/profile contract; fast Telegram evidence -> independent targeted Matrix corroboration -> T0 -> S11 | controlled Telegram outage onset -> S11 P95 `<=3 s`, max `<=5 s`; production observation clock retained separately | treating Telegram as universal for a profile where it is not required |
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

The controlled clock establishes the actual target: HARD/PATH and applicable
Telegram must prove P95 `<= 3 s`, **no valid sample > 5 s**, and failure
placement immediately before a probe, immediately after a probe and
mid-interval.  Production does not invent an unobservable physical-outage
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
FAST_FALL = compact fresh evidence plus bounded independent confirmation
SLOWER_RISE = existing conservative persistence, stability, anti-flap and
              re-admission semantics
```

No N phase weakens stale/unknown/conflicting fail-closed behavior, recovery
probation, capacity/policy checks, rollback or existing action Authority.

#### Canonical layer placement and strict ownership

| Layer | Role | Existing owner/contract reused | Prohibited shortcut |
| --- | --- | --- | --- |
| `L0` | immediately turn definitive existing local failure evidence into `SUSPECT` | `v7-egress-diagnose`, existing systemd, interface/tunnel and route/path evidence | a new watcher, event truth or direct route apply |
| `L1P` | cheap active-source path liveness | Matrix/diagnose existing-owner inputs | Google/YouTube/full HTTP Matrix as the liveness probe |
| `L1T` | Telegram-critical health of active sources and bounded hot targets | existing Telegram sentinel and Matrix service semantics | a fresh all-target Telegram sweep after T0 |
| `L2` | other required service health by active source and distinct profile contract | Matrix/profile/DNS service semantics | per-user polling or treating optional services as channel failure |
| `L3` | C8 reconciliation backstop | existing bounded C8/deadline-loop Matrix work | calling C8 the primary critical detector |
| `L4` | staggered deep, diagnostic, disagreement, stale/conflict, quality, cold-target and recovery support | existing Matrix canonical writer and Full fallback | global synchronous Full-before-action or a second writer |

L0/L1/L2 create `SUSPECT` only.  Matrix alone retains canonical health/state
and T0 ownership.  A fast signal wakes the existing bounded targeted Matrix
confirmation through its legal existing-owner invocation; it does not bypass
Matrix, Planner, Packet, Lease, Barrier, apply, verification or rollback.

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

The old roles are deliberately reclassified, not abandoned:

```text
C8 30-SECOND FAST PRIMARY                 -> L3 RECONCILIATION BACKSTOP
FULL MATRIX TIMER-DRIVEN FAILURE DETECTOR -> L4 DEEP/FALLBACK FRESHNESS HORIZON
TWO SLOW POLLING SAMPLES AS PRIMARY PROOF -> fallback/reconciliation semantics
```

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
| `N1` | `HARD_FAILURE_EVENT_DRIVEN_SIGNAL_INTEGRATION`: reuse existing definitive local evidence and tournament cheap path liveness at `250 ms/500 ms/1 s/2 s`; choose only a measured safe cadence. |
| `N2` | `TELEGRAM_CRITICAL_FAST_HEALTH_V2`: tournament `250 ms/500 ms/1 s`, thresholds and independent evidence against persistent outage, transient loss/timeout, endpoint glitch, correlated failure, 1,000 egresses and hot-target readiness. |
| `N3` | Other-required service sentinels: tournament `5 s/10 s/15 s/30 s` by current source plus distinct required profile contract, using DNS/TCP/TLS/light HTTP only where protocol-appropriate. |
| `N4` | Immediate targeted confirmation: each lawful signal invokes current-source/service confirmation now; source and relevant hot target are checked concurrently where safe; no wait for the next periodic Matrix cycle. |
| `N5` | `PRE_READY_TARGET_AND_PREPARED_DATAPLANE`: pre-failure hot-target readiness for the bounded top-H set plus existing V4 constant-time prepared data-plane proof; include freshness, dedup, coverage, capacity, policy, generation, role and 1/10/100/1000 compatible-cohort readiness. |
| `N6` | Transform Full Matrix from burst semantics to a measured staggered deep-refresh horizon under the existing Matrix writer; retain fallback for disagreement, stale/conflict and ambiguous cases, with FAST priority, fairness, bounded deep rate/concurrency and no catch-up storm. |
| `N7` | Causal Polygon tournament from controlled failure/outage onset to S11: interface/tunnel/path/Telegram/DNS/other-required/multi-service/partial. HARD/PATH and applicable Telegram require P95 `<=3 s` and max `<=5 s`; test each cadence phase offset and correlated failure. |
| `N8` | Controlled unattended Runtime proof: signal -> confirmation -> T0 -> selection -> governed apply -> S11 with real caller, consumer, idempotency, duplicate suppression, restart safety and no manual CLI seam. |
| `N9` | Full scale tournament using the mandatory egress/user/profile matrix and all resource/pressure measurements. |
| `N10` | Bounded ordinary rollout only after N8/N9: controlled -> one ordinary-like case -> small cohort -> bounded production, with rollback and no manufactured ordinary failure. |
| `N11` | `ACTIVE_ARCHITECTURE_REPLACEMENT_AND_PHYSICAL_SHRINK`: consumer-verified replacement, deletion and terminal reconciliation. It cannot finish while a superseded primary, duplicate owner/timer/state surface, obsolete compatibility branch, unclassified executable code or old active Program contract remains. |

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
immediate wake producers for bounded targeted Matrix confirmation.  Legacy
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

No code is retained merely because it is historical.  Before deleting or
deferring a branch, the existing owner must prove its caller(s), consumer(s),
state effect, fallback/rollback contribution and replacement.  The only legal
retirement sequence is:

```text
CONSUMER MAP -> REPLACEMENT PROVEN -> SAME-MATRIX POLYGON + CONTROLLED RUNTIME
-> ONE BOUNDED FALLBACK WINDOW -> NO-CALLER/NO-CONSUMER/NO-STATE-DEPENDENCY PASS
-> DELETE OR EXPLICITLY DEFER WITH OWNER + RE-ENTRY CONDITION
```

Static search alone is insufficient.  Conversely, no legacy function, timer,
branch or compatibility path may remain unclassified: `ACTIVE`, `BACKSTOP`,
`DEEP_BACKGROUND`, `FALLBACK`, `RETIRED_DELETED`, `EXPLICITLY_DEFERRED` or
`EXTERNAL_BLOCKED`, each with owner and consumer.  New code must replace or
integrate an existing edge; it cannot create orphan loops, duplicate requests,
parallel health truth or unbounded work.

##### Active architecture replacement and physical shrink law

N0–N11 is a replacement migration, not an additive architecture layer.  One
Runtime responsibility has one current implementation path.  The only
permitted multiplicity is one named `PRIMARY` plus one independently justified
`BACKSTOP`, `DEEP_BACKGROUND` or `FALLBACK`; parallel `PRIMARY_V1`,
`PRIMARY_V2`, `LEGACY_PRIMARY`, `COMPAT_PRIMARY` or `SHADOW_PRIMARY` paths are
forbidden.

For every admitted mechanism, N11 must record and complete this physical
replacement chain:

```text
OLD RESPONSIBILITY + EVERY CALLER/CONSUMER
-> NEW EXISTING-OWNER IMPLEMENTATION
-> SAME CONSUMERS MIGRATED
-> EQUIVALENCE, SAFETY AND SLO PROVEN
-> BOUNDED FALLBACK WINDOW
-> ZERO CURRENT CALLERS + ZERO CURRENT STATE DEPENDENCY
-> DELETE OLD CODE, IMPORTS, CONFIG, TIMER/UNIT, SCHEMA COMPATIBILITY,
   STATE PROJECTION, TESTS, FIXTURES AND PROGRAM REFERENCES
-> TRUTH CHECK + PHYSICAL SHRINK RECEIPT
```

`C8` and Full Matrix remain only with their current named roles (`BACKSTOP`
and `DEEP_BACKGROUND/FALLBACK`).  Their former primary-detector code, timer
semantics, synchronous callers and configuration must be deleted once their
replacement passes this chain.  The same rule applies to universal persistence
on admitted hard/Telegram paths: remove it from those synchronous paths only
after its class-specific replacement is proven, while retaining it where
recovery or ambiguous evidence still consumes it.

Compatibility is temporary, never a precautionary permanent path.  Every
reader/writer/translator/flag/schema branch has a migration owner, live
consumer list, expiry and deletion condition.  When the consumer list is empty,
delete the compatibility code and its fixtures.  Runtime state inventory must
classify every file/projection as canonical current Matrix state, another
current owner state, historical evidence or delete; two current health truths
are forbidden.

N11 inventories every systemd unit, timer, cron entry, foreground loop,
sentinel, health loop, Matrix/autoswitch trigger and runtime state surface:

```text
OWNER; PURPOSE_NOW; CALLER; CONSUMER; CADENCE; STATE_EFFECT; CURRENT_ROLE
```

`historical`, `unknown`, `redundant`, `no consumer` and `duplicate` are not
runtime roles: absent an exact external physical blocker, they are deleted.
After every major N migration, record files/LOC, executable paths, timers,
branches, active tests/fixtures, state surfaces and dependencies before/after.
Growth without retired responsibility is an architecture residual, not success.

The active Program contains only the current product goal, architecture,
owners, SLOs, N0–N11, safety/automation laws and terminal.  Historical
V1–V5.2 and superseded V5.3 material belongs in the historical archive and
Git history: it may inform discovery, but cannot dispatch Runtime work,
override N0–N11 or act as a current cadence/Authority contract.

#### N-program terminal

`MATRIX_ROLE_BASED_RECOVERY_OPTIMIZATION_TERMINAL_COMPLETE` requires all of:

1. HARD/PATH and applicable Telegram-critical classes meet controlled
   onset->S11 P95 `<=3 s`, max `<=5 s` and phase-offset evidence; production
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
6. Physical shrink is proven: `OLD_RUNTIME_PRIMARY_PATHS=0`,
   `DUPLICATE_HEALTH_OWNERS=0`, `DUPLICATE_DECISION_PATHS=0`,
   `UNCLASSIFIED_TIMERS=0`, `UNCLASSIFIED_RUNTIME_BRANCHES=0`,
   `NO_CALLER_RUNTIME_CODE=0`, `NO_CONSUMER_RUNTIME_OUTPUTS=0`,
   `OBSOLETE_COMPATIBILITY_BRANCHES=0`, `OBSOLETE_STATE_SURFACES=0`,
   `OBSOLETE_ACTIVE_TEST_FIXTURES=0` and `OLD_EXECUTABLE_PROGRAM_CONTRACTS=0`.
   Every survivor is `PRIMARY`, `BACKSTOP`, `DEEP_BACKGROUND`, `FALLBACK` or
   `CURRENT_RECOVERY` with owner and consumer. Timer-only wake statements are
   scoped away from N0–N11, legacy server-bound client-recovery names are
   mapped to S11, and no redundant, unreachable or duplicate path remains.

The next executable V5.3 action after this amendment is **N0a**, not a timer
or cadence increase.
