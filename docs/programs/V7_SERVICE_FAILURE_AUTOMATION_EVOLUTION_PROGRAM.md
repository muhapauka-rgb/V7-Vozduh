# V7 Service Failure Automation Evolution Program

Version: `4.3`

Status: `APPROVED_EXECUTION_PLAN`

Activation state owner: `CPS`

This file defines capability stages and completion contracts. It must not be
used to infer live execution, wait, stop, Authority or Production Maturity.

## V4.3 current-client recovery proof correction

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

The first bounded legacy-path acceptance gate is:

```text
at least three valid controlled certification-only samples
AND CLIENT_TRAFFIC_RECOVERY_LATENCY p95 <= 10,000 ms
AND no valid sample > 15,000 ms
AND HEAVY_CLOSURE_REMOVED_FROM_CLIENT_RECOVERY_PATH
AND zero weakened verification, rollback, Authority or ordinary-user guards
```

One cold and two warm samples are sufficient when their source/target/path and
invalidation identities are explicit. Samples cannot be repeated merely to
obtain a preferred percentile. If an owner-backed external network lower bound
prevents the gate, CT-M0F remains incomplete and publishes the exact interval,
owner, evidence and successor; the threshold is not silently weakened.

Required CT-M0F terminals are all mandatory:

- `CURRENT_SINGLE_USER_CLIENT_RECOVERY_LATENCY_MEASURED`;
- `CURRENT_SINGLE_USER_CRITICAL_PATH_SUBSTANTIALLY_REDUCED`;
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

The existing Matrix lifecycle is the only regular wake source. It may create
the next fresh probe generation and invoke the existing OMP/CPS consumer; this
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

### V4.3 performance ledger and hot-path regression law

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
single-user path and the V4.3 sample/gate contract. Its evidence proves only
current-path latency and fallback operability. It cannot certify class/bucket
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
CT-M0F cannot reach its terminal until every V4.3 current-client terminal is
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

### Mission CT-M8 — bounded controlled-production certification

Production starts only after CT-M7 and an exact existing-owner admission.
Use certification identities/classes only. Ordinary users must never be moved
solely to manufacture evidence.

Controlled production validates only residual blast classes: one bucket,
multiple buckets, multiple targets, exception handling, rollback and forward
recovery. It must not replay every numeric scale already proven by Polygon.

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

### V4.3 dynamic Mission compression

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

### V4.3 production-effect boundary

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

### V4.3 Program completion contract

This capability plan reaches its program terminal only when all current
criteria are owner-backed and consumed:

- current data-plane feasibility and O(N)/O(K)/O(1) model proven;
- current single-user client traffic recovery and reset traffic recovery are
  measured independently from full durable closure;
- the CT-M0F post-deploy controlled legacy benchmark satisfies the V4.3
  numeric gate, or CT-M0F remains open at the exact owner-backed interval;
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
- Authority/Runtime recommendation is independently decided;
- no open stage lacks `next_required_consumer` or `reentry_condition`;
- CPS, OMP and Runtime projections agree;
- local, GitHub and production identity align after any deploy;
- every safe residual has one durable automatic successor.

Only then may OMP emit:

`CONSTANT_TIME_COHORT_FAILOVER_CAPABILITY_FULL_CAUSAL_LOOP_CONSUMED`.

This terminal does not itself mean full production Authority, all-user
movement, Natural L8 sufficiency or Production Maturity increase.
