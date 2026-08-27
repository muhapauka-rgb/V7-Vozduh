# L3 Emergency Autonomous Failover

Status: `CANONICAL CAPABILITY SPECIFICATION`
Implementation: `NONE`
Runtime impact: `NONE`
Authority impact: `NONE`
Users moved: `NO`

Owner: OMP / Autonomous Execution Program / Autonomous Runtime Model composition.

This document is the canonical implementation contract for one autonomous capability.

It is not architecture, OMP, Runtime, Planner, Authority, Governance, Truth Source, roadmap, or implementation.

L3 consumes:

- `docs/reference/V7_AUTONOMOUS_EXECUTION_PROGRAM.md`
- `docs/reference/V7_AUTONOMOUS_RUNTIME_MODEL.md`
- `docs/reference/V7_RUNTIME_MODEL.md`
- `docs/reference/V7_DECISION_MODEL.md`
- `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`
- `docs/reference/SYSTEM_MAP.md`

## 1. Purpose

L3 exists to restore user connectivity after confirmed channel failure.

Primary goal:

```text
Restore user connectivity after confirmed current-channel failure.
```

L3 is an emergency failover capability.

It is not rebalance, optimization, preference movement, cleanup, pool optimization, or capacity balancing.

An identity assigned while its source was eligible remains eligible for this
recovery path if that same source later becomes a fresh, confirmed failure.
The existing `users.registry` assignment is the canonical correlation; no
separate client watcher or assignment-history store is used. The existing
Matrix -> Planner -> Candidate/Packet/Lease/Barrier -> Apply owners may move
only users still assigned to that failed source, subject to the normal
freshness, target, capacity, Authority, verification and rollback gates.
Stale, unknown or conflicting evidence, and administrative maintenance or
intentional disablement, remain `STOP_SAFE`.

## 2. Capability Boundary

Allowed:

- detect failed channel;
- detect affected users;
- identify required services affected by the failed current channel;
- find safe target channel;
- perform bounded failover inside certified scope;
- verify route, target, and required services;
- rollback or contain failed execution;
- open, expose, and close incident state;
- record terminal outcome;
- feed learning, Engineering Intelligence, Production Maturity, and OMP.

Forbidden:

- rebalance;
- optimization;
- capacity balancing;
- preference movement;
- manual cleanup;
- pool optimization;
- authority expansion;
- policy expansion;
- class promotion by Runtime;
- target cleanup;
- delayed reuse;
- daemon/timer broad movement;
- movement without fresh failure evidence.

## 3. Entry Conditions

L3 may start only when all mandatory conditions are true:

| Entry condition | Required meaning | Existing owner |
| --- | --- | --- |
| Current channel failed | Current assigned channel is failed for the affected user/service context. | Policy 001 / service evidence / runtime truth owners. |
| Users affected | One or more assigned users are affected by the failed current channel. | Planner/user assignment owners. |
| Required services failed | Required services for affected users fail on current channel. | Service matrix / policy / user-service fit owners. |
| Safe target exists | A target passes service, route, load, quality, policy, and suitability gates. | Planner/autoswitch owners. |
| Fresh evidence | Required evidence is inside certified freshness bounds. | Freshness/evidence owners. |
| Authority allows L3 | L3 emergency failover authority exists for the current scope. | OMP / Policy 004 / delegated authority owners. |
| Restore ready | Restore barrier / clearance path is ready. | Restore barrier owners. |
| Rollback ready | Rollback or certified no-rollback path is ready before apply. | Rollback owners / Policy 007. |

If any entry condition is false or unknown, L3 must `STOP_SAFE`.

## 4. Trigger Model

Approved wake events:

- service regression;
- confirmed hard failure;
- channel unavailable;
- verified incident;
- runtime/state resume for an already-open L3 incident.

Rejected triggers:

- timer;
- cron;
- periodic movement;
- broad autoswitch loop;
- stale signal;
- synthetic trigger;
- optimization signal without confirmed failure.

Wake rule:

```text
Wake may start L3 observation.
Wake may not grant L3 execution.
```

## 5. Runtime Path

L3 consumes the stable Runtime Operating System.

Canonical path:

```text
Wake
  -> Observe
  -> Incident
  -> Planner
  -> Authority
  -> Eligibility
  -> Execute
  -> Verify
  -> Rollback / Contain
  -> Learn
  -> Report
  -> Sleep
```

Runtime state path:

```text
IDLE
  -> WAKE
  -> OBSERVE
  -> CLASSIFY
  -> WORLD_READY
  -> PLAN_READY
  -> WAITING_AUTHORITY or READY or STOP_SAFE
  -> EXECUTING
  -> VERIFYING
  -> ROLLBACK or LEARNING
  -> REPORTING
  -> SLEEP or SUSPENDED
```

Runtime OS remains unchanged.

## 6. Planner Contract

Planner responsibilities:

- identify affected users on failed current channel;
- identify candidate target channels;
- reject unsafe targets;
- preserve existing movement protection, anti-flap, policy, service, load, route, quality, and suitability gates;
- produce selected move identity and explanation;
- produce no-action/blocker when no safe target exists.

Runtime responsibilities:

- consume planner output;
- verify authority and live readiness;
- fail closed on stale, missing, mismatched, or materially changed decision/packet/lease/restore evidence;
- execute only through existing execution owners;
- never replace planner or rerun planning after committed execution identity.

Owner boundary:

```text
Planner selects candidate.
Runtime executes or STOP_SAFE.
OMP certifies capability.
Authority owners grant authority.
Runtime never grants authority.
```

## 7. Authority Contract

Authority object:

```text
EMERGENCY_FAILOVER_AUTONOMY
```

Allowed move:

```text
FAILOVER
```

Allowed reason:

```text
CURRENT_CHANNEL_FAILED
```

Everything else is forbidden.

L3 authority does not permit:

- rebalance;
- optimization;
- degraded-channel movement;
- recovery admission;
- capacity balancing;
- policy expansion;
- blast-radius expansion;
- future action reuse;
- action-class promotion.

## 8. Readiness Contract

Mandatory gates:

| Gate | Required behavior |
| --- | --- |
| Freshness | Evidence must be current inside L3-certified bounds. |
| Rollback | Rollback or certified no-rollback must be ready before apply. |
| Verification | Route, target, and required-service verification must be ready. |
| Blast Radius | Scope must stay inside certified L3 budget. |
| Execution Budget | Current execution count/window must be inside certified budget. |
| Restore Barrier | Restore/clearance generation must match the selected decision. |
| Circuit Breaker | No open breaker/suspension may block L3. |
| Source eligibility | Current channel/user/failure evidence must prove L3 entry. |
| Target eligibility | Target must be safe and policy-compatible. |
| Movement protection | Anti-flap, cooldown, state-change cost, and safety gates must pass or explicitly not apply to confirmed hard failure. |

Any failed mandatory gate produces `STOP_SAFE`.

## 9. Execution Contract

Execution requires:

- `operation_id`;
- packet / transaction artifact;
- `selected_move_hash`;
- `restore_generation`;
- `authority_generation`;
- idempotency key;
- one certified bounded execution attempt.

Execution must:

- preserve decision identity;
- preserve packet/transaction identity at apply;
- preserve selected move hash;
- preserve source and target;
- consume existing execution lease / restore barrier owners;
- fail closed on mismatch;
- never silently replace selected move, user, source, target, authority, rollback, verification, or packet/transaction identity.

## 10. Verification Contract

Verification must prove:

- route verification;
- service verification;
- target verification;
- terminal success or terminal failure.

Terminal success means:

```text
Apply completed
AND route verification PASS
AND required-service verification PASS
AND target remains eligible
AND terminal outcome recorded
```

Apply success alone is not terminal success.

## 11. Rollback Contract

Rollback triggers:

- apply failure after mutation risk;
- verification failure;
- target becomes unsafe after apply;
- route/service verification cannot prove success;
- restore/rollback policy requires containment.

Rollback owner:

- existing rollback / restore owners;
- Policy 007;
- execution feedback owners for terminal state classification.

Rollback result must be classified separately:

- `ROLLBACK_SUCCESS`;
- `ROLLBACK_FAILURE`;
- containment/no-rollback state when certified;
- incident escalation when rollback cannot prove safety.

Rollback must never be counted as `SUCCESS`.

## 12. Incident Contract

L3 opens an incident when confirmed current-channel failure affects users.

Incident must expose:

- failed channel;
- affected users/scope;
- failed required services;
- selected target or no-target blocker;
- authority state;
- readiness gates;
- verification state;
- rollback/containment state;
- terminal outcome;
- next action.

Incident closes only when terminal outcome, verification/rollback status, learning, and report are recorded.

## 13. Learning Contract

L3 terminal outcome must feed:

- observed terminal state;
- prediction vs actual;
- failure reason;
- target suitability delta;
- rollback/no-rollback result;
- verification quality;
- Engineering Intelligence;
- Production Maturity;
- OMP certification state.

Learning must preserve separate semantics for:

- `SUCCESS`;
- `ROLLBACK_SUCCESS`;
- `ROLLBACK_FAILURE`;
- `APPLY_FAILURE`;
- `NO_EXECUTION`;
- `STOP_SAFE`.

Synthetic evidence is forbidden.

## 14. Operator Surface

Operator must see:

- incident;
- reason;
- affected users;
- failed current channel;
- target;
- verification plan/status;
- rollback plan/status;
- authority envelope;
- next action;
- terminal outcome.

Operator-facing explanation must be human-readable and must not require source-code inspection.

## 15. Production Behavior Contracts

These contracts integrate production behavior discovered in `docs/research/L3_BEHAVIOR_DISCOVERY.md`.

They are L3 implementation requirements.

They do not create a new Runtime, Planner, Authority, OMP, roadmap, behavior document, owner, or architecture.

They apply only to Emergency Autonomous Failover:

```text
EMERGENCY_FAILOVER_AUTONOMY
FAILOVER
CURRENT_CHANNEL_FAILED
```

They do not grant L4, L5, L6, or L7 behavior.

| Behavior | Purpose | Trigger | Expected Runtime Behavior | Terminal Outcome | Existing Owner | STOP_SAFE conditions | Operator visibility | Learning impact |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Event Collapse | Prevent one production failure from spawning many independent L3 cycles. | Multiple wake signals share the same failed source channel, failure family, required-service family, authority envelope, and active generation. | Collapse signals into one active L3 incident/context. Select affected subjects only inside certified blast radius. Do not start a separate execution loop for every repeated signal. | Existing incident remains active; new execution starts only if budget, authority, and state allow. | Autonomous Runtime event dispatch, incident/report lifecycle, CPS, L3 capability owner composition. | Event cannot be mapped to the active generation; event conflicts with current incident state; event would exceed certified budget. | Show collapsed event count, active incident id, failure key, and why no duplicate execution started. | Record duplicate/collapsed signal as observation evidence, not as execution outcome. |
| Incident Merge | Avoid duplicate incidents for the same operational failure. | A new event matches an open L3 incident by failed source, failure family, service family, authority envelope, and generation. | Attach event to existing incident. Preserve one incident owner, one budget, one terminal closure path, and one operator view. | `INCIDENT_OPEN` until terminal closure. | Incident/report lifecycle, CPS, operator visibility owners. | Merge key is incomplete, contradictory, stale, or crosses authority/blast-radius boundary. | Show merged events and affected subject set. | Preserve merged evidence as incident context; do not count as additional outcome. |
| Incident Split | Preserve independent blast scopes and avoid hiding separate failures. | A new event differs by failed source, service family, authority envelope, blast scope, target constraint, or failure generation. | Create a separate incident/context. Do not merge independent failures into one execution budget. | New `INCIDENT_OPEN` or `STOP_SAFE` if split cannot be safely owned. | Incident/report lifecycle, planner subject mapping, blast-radius owners. | Split would exceed certified concurrent incident policy; owner cannot prove independence; authority envelope is unknown. | Show why incident was split and which scope owns each incident. | Separate learning by incident key and failure family. |
| Retry Budget | Prevent infinite or repeated unsafe failover attempts. | L3 considers another attempt after `STOP_SAFE`, failed verification, rollback, timeout, or duplicate/replayed event. | Allow a retry only when certified retry budget remains and the retry is not a duplicate apply. Replays may finish the same attempt; they must not create a new attempt. | `READY` if budget remains; `SUSPENDED` or `BUDGET_EXHAUSTED` when exhausted. | Execution budget, Policy 009, circuit breaker, OMP certification. | Attempt count/window exceeds certified L3 budget; retry would move another user outside scope; retry reason is not owner-mapped. | Show attempts used, attempts remaining, retry reason, and breaker state. | Budget exhaustion becomes safety/anti-flap evidence, not success evidence. |
| Backoff | Prevent retry storms and oscillation after failure. | L3 attempt fails, rollback succeeds/fails, verification times out, or repeated source/target instability appears. | Apply certified L3 backoff/hold-down before another attempt for the same incident key, source, target, or failure family. | `SUSPENDED`, `WAITING_BACKOFF`, or `STOP_SAFE` depending on owner support. | Policy 009, movement protection, circuit breaker, CPS. | Backoff state is active; backoff owner state is unknown; retry would bypass hold-down. | Show backoff reason, scope, start, expiry, and required resume condition. | Backoff records instability and reduces confidence for the same condition. |
| Target Lost Before Apply | Avoid applying to a target that became unsafe after planning. | Target health, service suitability, authority, rollback, verification, or target eligibility changes before irreversible apply. | Revalidate immediately before apply. If target is no longer eligible, do not apply. Do not silently pick a new target inside the same committed execution identity. | `STOP_SAFE`; incident remains open with target-lost blocker. | Runtime eligibility, material state change, freshness, restore barrier, planner/autoswitch owners. | Target eligibility fails; selected target changed; selected move hash changed; authority/rollback/verification generation changed. | Show selected target, changed field, and why apply stopped. | Record failed pre-apply target evidence; do not count as production movement outcome. |
| Partial Success | Prevent incomplete proof from being classified as success. | Apply completes but only some required verification dimensions pass, or some affected services/subjects remain failed. | Keep terminal state non-success. Roll back, contain, or keep incident open according to rollback/no-rollback contract. | `PARTIAL_SUCCESS_UNSAFE`, `ROLLBACK_SUCCESS`, `ROLLBACK_FAILURE`, or `INCIDENT_OPEN`. | Verification, terminal classification, rollback, learning owners. | Required route/service/target verification is incomplete, mixed, timed out, or contradictory. | Show which checks passed, failed, timed out, or remain unknown. | Preserve partial evidence separately; never increase success/promotion metrics from partial proof. |
| Verification Timeout | Avoid hanging L3 after mutation or readiness check. | Verification does not complete inside certified L3 timeout. | Treat timeout as non-success. If mutation risk exists, run rollback/containment. If no mutation occurred, close as `STOP_SAFE`. | `NO_EXECUTION`, `ROLLBACK_SUCCESS`, `ROLLBACK_FAILURE`, or `INCIDENT_OPEN`. | Verification owner, rollback owner, terminal classification owner. | Verification timeout owner missing; timeout state cannot prove whether apply occurred; rollback readiness unknown. | Show timeout duration, verification owner, mutation state, rollback/containment path. | Timeout becomes verification-quality and risk evidence, not success evidence. |
| Unknown State Quarantine | Never guess when required runtime truth is missing or contradictory. | Required source, target, service, route, authority, rollback, verification, or incident state is unknown. | Before apply: stop safely. After apply: keep incident open, quarantine/suspend scope, and require proof before closure or resume. | `STOP_SAFE`, `INCIDENT_OPEN`, or `SUSPENDED`. | Runtime Model, incident/report lifecycle, CPS, truth/freshness owners. | Any mandatory owner returns unknown/contradictory state for a mutating decision. | Show unknown owner, missing evidence, and blocked transition. | Unknown state is safety evidence and must not increase maturity, trust, or promotion readiness. |
| Recovery During Execution | Avoid unnecessary movement before apply and avoid oscillation after apply. | Failed source recovers while L3 cycle is active. | Before apply: abort if emergency condition no longer exists. After apply: verify the actual terminal state and do not automatically move back. Return-to-source belongs to recovery/rebalance policy, not L3. | `NO_EXECUTION`, `SUCCESS`, `ROLLBACK_SUCCESS`, or `INCIDENT_OPEN` depending on mutation and verification state. | Runtime eligibility, verification, terminal classification, Policy 003/Recovery Admission boundary. | Recovery evidence contradicts L3 entry before apply; post-apply state cannot be verified; automatic return would be required. | Show when recovery occurred and why L3 aborted, verified, or refused return movement. | Record recovery timing and prediction quality; no automatic recovery-admission credit. |
| Recovery After Suspend | Resume L3 only after stable proof, not immediately after a breaker clears. | Suspended source/target/incident later appears healthy or operator clears a blocker. | Require certified stable window, recovery admission, authority, and half-open/probe behavior before any new L3 attempt. L3 may resume only inside certified emergency scope. | `SUSPENDED` until resume gates pass; then `WAKE`/`OBSERVE` for a fresh cycle. | Policy 003, Policy 009, OMP certification, circuit breaker, CPS. | Stable window missing; authority missing; resume would perform recovery/rebalance rather than emergency failover. | Show suspension reason, resume gates, and remaining blockers. | Resume evidence informs recovery/admission confidence; it is not failover success evidence. |
| Late Event Handling | Avoid acting on old failure information. | Event generation, timestamp, source version, or incident generation is older than current world/incident state. | Mark event stale/late and do not mutate. Attach to incident history only if useful for diagnosis. | `NO_ACTION` or `STOP_SAFE`. | Freshness, owner-issued version, incident generation, CPS. | Event age/generation cannot be proven; late event would reopen closed incident without fresh failure evidence. | Show event generation, current generation, and stale/late decision. | Record as stale signal quality evidence only. |
| Budget Exhaustion | Make "too many unsafe attempts" an explicit terminal blocker. | Execution, retry, rollback, verification, blast-radius, or incident budget is consumed. | Stop L3 for that scope. Open/keep incident visible. Require OMP/operator/certification path before further execution. | `BUDGET_EXHAUSTED` and `SUSPENDED`. | Blast radius, execution budget, circuit breaker, OMP, CPS. | Any certified L3 budget is exhausted or cannot be read. | Show budget type, limit, consumed count, scope, and reset/review path. | Budget exhaustion reduces confidence and blocks promotion until reviewed. |
| Duplicate Event Suppression | Prevent duplicate events or replay from causing duplicate apply. | Same semantic event/execution key is delivered again, process restarts, or replay resumes an active cycle. | Reuse existing incident/decision/attempt state. Complete existing terminal closure if needed. Never create a second apply for the same semantic execution. | Existing terminal state, `NO_ACTION`, or `STOP_SAFE` if replay state is unsafe. | Execution idempotency, incident owner, decision/packet/lease owners. | Existing attempt state cannot be proven; replay would change user/source/target/selected hash; terminal closure is contradictory. | Show duplicate key, prior attempt state, and whether replay completed closure or no-oped. | Replay may improve closure completeness; it must not add new production outcome count. |

Behaviors intentionally excluded from L3:

- degraded-channel autonomy without current-channel failure: L4;
- recovery admission or automatic return-to-source: L5 / Policy 003;
- rebalance, capacity balancing, or optimization: L6 or later;
- policy-level autonomous routing across all action classes: L7;
- broad parallel incident execution beyond certified L3 budgets: later OMP certification only.

Implementation readiness rule:

```text
An L3 implementation may be written from the Autonomous Execution Program,
the Autonomous Runtime Model, and this L3 Capability Specification without
making new architecture decisions.
```

If implementation discovers an unmapped behavior, it must first map to an existing owner. New architecture remains last resort.

## 16. Test Contract

Mandatory implementation tests:

| Test family | Required proof |
| --- | --- |
| Authority OFF | L3 stops safely without authority. |
| Authority ON | L3 may proceed only inside L3 envelope. |
| No target | L3 produces no-action/incident, not unsafe apply. |
| Stale evidence | L3 stops before apply. |
| Rollback failure | L3 opens incident/suspension and does not classify success. |
| Verification failure | L3 triggers rollback/containment. |
| Duplicate event | L3 is idempotent and does not duplicate execution. |
| Circuit breaker | Open breaker blocks execution. |
| Idempotency | Same semantic execution attempt does not create duplicate apply. |
| STOP_SAFE | Every missing mandatory gate stops safely. |
| Event collapse | Repeated same-scope events produce one incident/context and no duplicate apply. |
| Incident merge/split | Same-scope events merge; different authority/blast/failure scopes split. |
| Retry budget/backoff | Exhausted or active budget/backoff blocks execution and exposes reason. |
| Target lost before apply | Changed target eligibility stops before mutation. |
| Partial success | Mixed verification cannot classify as `SUCCESS`. |
| Verification timeout | Timeout produces non-success terminal state and rollback/containment when needed. |
| Unknown state | Unknown mandatory truth quarantines/suspends or stops safely. |
| Recovery during execution | Pre-apply recovery aborts; post-apply recovery verifies terminal state without automatic return. |
| Recovery after suspend | Resume requires stable window, authority, and certified resume gates. |
| Late event | Late/stale events cannot trigger mutation. |
| Budget exhaustion | Exhausted budgets produce `BUDGET_EXHAUSTED` / `SUSPENDED`. |

## 17. Production Validation

Production validation ladder:

```text
Dry run
  -> 1 user
  -> 2 users
  -> 5 users
  -> 10 users
  -> remaining users
```

Each step requires:

- OMP approval/certification for the scope;
- authority inside current envelope;
- all live gates pass;
- verification;
- rollback/no-rollback closure;
- learning;
- engineering report;
- Current Program State update if state changes.

No step may skip the previous certified step.

## 18. Certification Contract

L3 becomes certified only after:

- tests `PASS`;
- production behavior contracts `PASS`;
- production validation `PASS`;
- rollback `PASS`;
- verification `PASS`;
- learning `PASS`;
- incident/report lifecycle `PASS`;
- OMP approval/certification.

Certification owner:

```text
OMP
```

Runtime consumes certification.

Runtime does not define certification requirements.

## 19. Definition of Done

L3 is complete only if all are true:

- users automatically leave failed channels inside certified L3 authority;
- verification succeeds for certified success cases;
- rollback is proven for failed verification/apply cases;
- production behavior contracts are implemented and tested;
- incident is opened, visible, and closed;
- learning is recorded;
- OMP certification is completed;
- Production Maturity consumes the certification;
- Current Program State records the active certified state.

## 20. Implementation Consumers

| Section | Existing implementation consumer |
| --- | --- |
| Purpose / boundary | OMP, Autonomous Execution Program, Product Specification. |
| Entry conditions | Policy 001, service evidence, planner/autoswitch, freshness, authority, restore, rollback owners. |
| Trigger model | Event/evidence owners and Autonomous Runtime Model wake contract. |
| Runtime path | Autonomous Runtime Model and Runtime Model. |
| Planner contract | `tools/v7-users-autoswitch` and decision surface owners. |
| Authority contract | OMP, Policy 004, Delegated Autonomy Policy, Action-Class Authority owners. |
| Readiness contract | Runtime eligibility, restore barrier, verification, rollback, blast-radius, anti-flap, movement-protection owners. |
| Execution contract | `admin_core/operator_execution.py`, `admin_core/operator_execution_pipeline.py`, packet/lease owners, autoswitch apply owner. |
| Verification contract | existing verification owners and operator execution feedback owners. |
| Rollback contract | rollback / restore owners and Policy 007. |
| Incident contract | OMP report lifecycle and operator visibility owners. |
| Learning contract | feedback, learning, Engineering Intelligence, Production Maturity, OMP. |
| Operator surface | admin/operator UI and explainability owners. |
| Production behavior contracts | Autonomous Runtime event dispatch, incident/report lifecycle, CPS, runtime eligibility, freshness, anti-flap, movement protection, blast-radius, execution budget, verification, rollback, learning owners. |
| Test contract | existing test owners for runtime, planner, execution, verification, rollback, learning. |
| Production validation | OMP and safe deployment/production validation owners. |
| Certification | OMP. |

Need New Owner: `FALSE`.

## 21. Future Evolution

L4, L5, L6, and L7 reuse this capability pattern.

Only capability semantics change:

- L4 changes the action class from hard failure to degraded-channel autonomy.
- L5 changes the action class to recovery autonomy.
- L6 changes the action class to bounded rebalance.
- L7 consumes all certified action classes inside approved policy.

Runtime OS remains unchanged.

Future evolution rule:

```text
New autonomy level = certified capability semantics.
New autonomy level != Runtime OS change.
```

## Validation

Capability Audit: `PASS`.

Owner Audit: `PASS`.

OMP Audit: `PASS`.

Runtime Audit: `PASS`.

Decision Audit: `PASS`.

Execution Audit: `PASS`.

Duplicate Owner Audit: `PASS`.

Conflict Audit: `PASS`.

Implementation Readiness Audit: `PASS`.

Final verdict:

```text
L3_CAPABILITY_LOCKED
```
