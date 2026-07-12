# Codex Heartbeat Adapter Design And Certification

Mission ID: `V7_OMP_CODEX_HEARTBEAT_ADAPTER_DESIGN_AND_CERTIFICATION_V1`  
Run nonce: `V7_OMP_HEARTBEAT_ADAPTER_DESIGN_V1_82F6A913D4CE`  
Started: `2026-07-12T22:00:30+0700`  
Mission type: architecture design / contract certification  
Implementation performed: `NO`  
Final verdict: `CODEX_HEARTBEAT_ADAPTER_DESIGN_CERTIFIED`

## Current Problem

Codex App thread heartbeat is an existing external activation owner. V7 already owns OMP self-continuation, CPS state, dependency states, READY-frontier calculation, Mission identity, anti-replay and atomic CPS reconciliation. The missing element is a certified adapter contract that prevents a scheduled wakeup from being interpreted as capability readiness, Mission admission or Runtime authority.

The design keeps five stages separate:

```text
platform wakeup
!= dependency change
!= capability READY
!= Mission admitted
!= Runtime action authorized
```

## Exact Lifecycle And Ownership

| Stage | Existing owner | Required behavior | Missing contract | Forbidden responsibility |
| --- | --- | --- | --- | --- |
| Heartbeat scheduling | Codex Automation platform | Wake the target thread on an explicit cadence | Bind automation/thread/project identity | Evidence sufficiency, Mission selection, Runtime authority |
| Context activation | Codex App / existing Codex OMP consumer | Start a new Engineering execution context | Validate wakeup identity and scope | Reuse old Mission/packet/lease identities |
| Fresh state read | ECR + CPS + owner evidence | Read current CPS and canonical evidence sources | Per-capability dependency fingerprint baseline | Mutate Runtime or infer truth from chat/report |
| Dependency validation | Existing capability owner + OMP dependency graph | Decide whether owner-backed evidence changed and is sufficient | Evaluated fingerprint and freshness result | Heartbeat deciding READY |
| Reentry transition | CPS + OMP | Atomically preserve WAITING or transition to READY | Generation-bound transition record | Manual READY override |
| Mission admission | OMP + Mission identity guard | Admit one fresh Mission only when READY exists | Continuation-context compare-and-set | Concurrent/duplicate Mission |
| Execution | Existing Codex OMP consumer | Run normal OMP loop | None beyond activation binding | Authority bypass or direct Runtime execution |
| Report/state closure | Existing report/CPS/OMP owners | Record material outcome and release active Mission state | Wakeup result classification | Report churn for unchanged state |

Canonical flow:

```text
Codex thread heartbeat
-> authenticate automation, thread and project identity
-> read fresh CPS section 0
-> reject active/stale execution context
-> read only named owner evidence for WAITING capabilities
-> compare source generation and dependency fingerprints
-> unchanged: NO_CHANGE and end
-> changed: capability owner evaluates evidence sufficiency
-> insufficient: record evaluated fingerprint only when required; remain WAITING; end
-> sufficient: atomic WAITING -> READY transition
-> recalculate dependency graph and READY frontier
-> no frontier: NO_CHANGE and end
-> frontier exists: atomically acquire existing Mission context fields
-> create fresh Mission identity and run nonce
-> normal OMP admission and execution
-> terminal report and atomic CPS update
-> release Mission context
```

## Activation Contract

| Field | Owner | Producer | Consumer | Validation rule | Failure behavior |
| --- | --- | --- | --- | --- | --- |
| `AUTOMATION_ID` | Codex Automation platform | Automation configuration | Wakeup admission | Exact approved ID | `STOP_SAFE_AUTOMATION_IDENTITY` |
| `TARGET_THREAD_ID` | Codex App | Heartbeat configuration | Codex OMP consumer | Exact current approved thread | `STOP_SAFE_THREAD_IDENTITY` |
| `PROJECT_ID` | Codex App project registry | Automation configuration | ECR/context resolver | Exact canonical workspace project | `STOP_SAFE_PROJECT_IDENTITY` |
| `WAKEUP_RUN_ID` | Codex platform | One scheduled invocation | Replay validator/report | Unique platform run identity when exposed; otherwise deterministic wakeup slot identity | Duplicate -> `NO_CHANGE_DUPLICATE_WAKEUP` |
| `EVENT_ID` | Adapter contract | Automation ID + target thread + scheduled time slot | Replay validator | Deterministic SHA-256 identity | Invalid/missing -> `STOP_SAFE_EVENT_IDENTITY` |
| `EVENT_OWNER` | Adapter contract | Codex Automation platform | OMP admission | Must equal approved activation owner | `STOP_SAFE_OWNER_MISMATCH` |
| `EVENT_SOURCE` | Capability evidence owner | Canonical state/evidence path | Capability owner | Named owner source, never report/chat | `STOP_SAFE_SOURCE_UNKNOWN` |
| `EVENT_GENERATION` | Evidence owner | Owner-backed state | Fingerprint validator | Current generation newer/different from evaluated baseline | Unchanged -> `NO_CHANGE` |
| `EVENT_TIME` | Codex platform / trusted clock | Wakeup context | Freshness validator | RFC3339; inside configured slot tolerance | Stale -> `NO_CHANGE_STALE_WAKEUP` |
| `FRESHNESS_RULE` | Existing evidence owner | Canonical owner contract | Capability owner | Owner-specific rule must be present and pass | `NO_CHANGE_EVIDENCE_NOT_FRESH` |
| `DEPENDENCY_FINGERPRINT_BEFORE` | CPS dependency record | Last evaluated owner evidence | Fingerprint validator | 64 lowercase hex chars | Invalid -> `STOP_SAFE_FINGERPRINT` |
| `DEPENDENCY_FINGERPRINT_AFTER` | Adapter from fresh owner evidence | Read-only reconciliation | Fingerprint validator | Deterministic owner/source/generation/content identity | Invalid -> `STOP_SAFE_FINGERPRINT` |
| `DEPENDENCY_CHANGED` | Fingerprint validator | Before/after comparison | Capability owner | `TRUE` only when exact fingerprints differ | `FALSE` -> `NO_CHANGE` |
| `TARGET_CAPABILITY` | CPS WAITING registry | Deterministic WAITING set | Capability owner/OMP | Must currently be WAITING and owner-mapped | `NO_CHANGE_NOT_WAITING` |
| `CURRENT_CPS_GENERATION` | CPS | Section 0 | Atomic transition guard | Must remain unchanged through admission compare-and-set | Drift -> `STOP_SAFE_CPS_GENERATION` |
| `MISSION_SCOPE` | OMP | READY frontier | Mission admission | Exactly one deterministic frontier capability | Ambiguous -> `STOP_SAFE_SCOPE` |
| `AUTHORIZATION_SCOPE` | Certified adapter contract | Static configuration | All consumers | Exactly `START_ENGINEERING_EXECUTION_CONTEXT_ONLY` | Any expansion -> `STOP_SAFE_AUTHORITY` |
| `REPLAY_PROTECTION` | Mission identity + CPS + adapter | Deterministic identities | Admission validator | Wakeup, fingerprint and Mission identity not consumed/active | Duplicate -> `NO_CHANGE_REPLAY` |
| `CONCURRENCY_CONTROL` | Existing CPS Mission context | Atomic admission | Codex OMP consumer | `CURRENT_EXECUTION_MISSION_ID=NONE` before compare-and-set | Active -> `NO_CHANGE_ALREADY_ACTIVE`; inconsistent -> `STOP_SAFE` |
| `ACTIVATION_RESULT` | Adapter/OMP | Wakeup terminal classification | Thread/review/report owner | One canonical result | Missing -> `STOP_SAFE_RESULT_MISSING` |

Additional required fields:

```text
LAST_EVALUATED_DEPENDENCY_FINGERPRINT
LAST_EVALUATED_SOURCE_GENERATION
WAKEUP_SLOT
ADMISSION_CPS_GENERATION
FRESH_MISSION_ID
FRESH_RUN_NONCE
NO_RUNTIME_AUTHORITY = TRUE
NO_USER_MOVEMENT_AUTHORITY = TRUE
NO_PACKET_AUTHORITY = TRUE
NO_CANDIDATE_AUTHORITY = TRUE
```

## Wakeup Admission Model

```text
heartbeat arrives
-> identity gate: automation/thread/project/event
-> read CPS section 0 from disk
-> verify current program is OMP
-> verify WAITING capabilities exist
-> verify no active execution Mission
-> read named evidence sources only
-> calculate owner-scoped dependency fingerprint
-> check freshness, source generation and replay
-> ask capability owner whether changed evidence satisfies reentry
-> preserve WAITING or atomically transition to READY
-> validate completion order and recalculate frontier
-> if frontier empty: NO_CHANGE
-> if frontier exists: atomic fresh Mission context acquisition
-> rerun identity and CPS generation check
-> start normal OMP Mission
```

The heartbeat asks only: `Has owner-backed reality changed enough to reevaluate a WAITING capability?` It never answers the question itself.

## Frequency And Lifecycle

Certified initial policy for a future implementation:

| Control | Design |
| --- | --- |
| Default cadence | Every 30 minutes |
| Absolute maximum frequency | Four wakeups per hour |
| Minimum interval | 15 minutes |
| Jitter | Platform-owned if available; no V7 timer |
| Active condition | CPS contains at least one `WAITING_EXTERNAL_DEPENDENCY` capability |
| No-change behavior | End current wakeup; no Mission, report, CPS write, retry or operator escalation |
| Evidence-changed but insufficient | Consume/evaluate exact fingerprint once, remain WAITING, end |
| Expiration | 30 days from enablement unless explicitly renewed |
| Automatic pause | No WAITING capability; program closed; identity mismatch; repeated infrastructure failure; explicit operator pause |
| Manual pause/disable | Codex Automation platform status update/delete |
| Manual override | Operator may run normal `Continue OMP`; cannot force READY or bypass the active-context guard |
| Emergency stop | Pause/delete heartbeat automation; Runtime Circuit Breaker remains separately authoritative for mutation |

The initial adapter may not self-change its cadence. Cadence modification is an explicit automation configuration update, preventing self-amplifying loops.

Repeated `NO_CHANGE` is expected polling behavior, not failure. It creates no Git commit and no Engineering Report. Three consecutive adapter infrastructure errors pause the automation; evidence insufficiency and unchanged fingerprints do not count as infrastructure errors.

## Replay And Concurrency

No new lease system is required. Reuse:

- `CURRENT_EXECUTION_MISSION_ID`;
- `CURRENT_EXECUTION_MISSION_STATE`;
- `CURRENT_STATE_GENERATION`;
- Mission ID + run nonce + start timestamp identity guard;
- atomic CPS reconciliation;
- no-progress fingerprint;
- existing report/path identity validation.

The logical `CONTINUATION_LEASE` is the atomic transition:

```text
expected CPS generation matches
AND CURRENT_EXECUTION_MISSION_ID = NONE
AND CURRENT_EXECUTION_MISSION_STATE = NONE
-> set fresh Mission ID/state with fresh run nonce
```

Rules:

1. Only one active continuation context is legal.
2. Heartbeat and manual `Continue OMP` use the same acquisition rule.
3. An active context returns `NO_CHANGE_ALREADY_ACTIVE`; it is not queued.
4. An inconsistent or apparently stale active context is never stolen automatically; use existing Mission identity/CPS reconciliation and manual review.
5. Mission context is released only by the terminal atomic CPS update.
6. A dependency fingerprint is evaluated once per owner generation.
7. Historical reports, old Missions, packets, Candidates, leases and Authority are never activation inputs.

This is an existing-owner field extension, not a Runtime execution lease and not a second scheduler.

## NO_CHANGE Model

Canonical non-error results:

```text
NO_CHANGE_DEPENDENCY_UNCHANGED
NO_CHANGE_NO_WAITING_CAPABILITY
NO_CHANGE_EVIDENCE_INSUFFICIENT
NO_CHANGE_EVIDENCE_NOT_FRESH
NO_CHANGE_READY_FRONTIER_EMPTY
NO_CHANGE_DUPLICATE_WAKEUP
NO_CHANGE_ALREADY_ACTIVE
```

For every `NO_CHANGE`:

- no Mission is formed;
- no retry occurs inside the wakeup;
- no Candidate or packet is created;
- no Authority is requested or granted;
- no Runtime action occurs;
- no CPS/report/git churn occurs, except a separately admitted atomic evaluated-fingerprint update when fresh changed evidence must be consumed once;
- no operator escalation occurs.

`STOP_SAFE` is reserved for identity, source, generation, contract, atomicity or ownership contradictions. It is not used for ordinary unchanged reality.

## Safety Boundary Review

| Plane/owner | Preserved responsibility | Explicit prohibition | Result |
| --- | --- | --- | --- |
| Runtime | Produce real evidence; execute only separately admitted actions | Start Codex/OMP or gain authority from heartbeat | `PASS` |
| CPS | Own volatile program and dependency state | Schedule or execute | `PASS` |
| OMP | Own reentry, frontier, Mission admission and continuation law | Become background process | `PASS` |
| Codex OMP consumer | Execute admitted Engineering Missions | Treat wakeup as readiness/authority | `PASS` |
| Codex Automation | Wake target thread on explicit cadence | Decide evidence sufficiency, READY or Runtime action | `PASS` |
| Capability owner | Decide evidence sufficiency | Activate platform or grant Runtime authority | `PASS` |
| Operator | Pause/delete/renew automation and retain manual fallback | Force READY or bypass concurrency | `PASS` |

The existing production Circuit Breaker remains independent. A heartbeat may perform read-only reconciliation while Safe Mode is not OPEN, but no resulting Mission gains mutation permission; all Runtime work remains subject to the existing Circuit Breaker, Authority, packet, lease and verification gates.

## Option Comparison

| Option | Safety | Ownership | Complexity | Autonomy | Auditability | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| A. Operator only | Highest | Existing | Lowest | Manual | High | Retain as fallback |
| B. Codex thread heartbeat + adapter | High with certified contract | Existing platform + existing V7 owners | Bounded | Periodic autonomous reentry | High | Selected |
| C. New V7 activation service | Unproven | New owner | High | High | Must be built | Rejected; unnecessary |
| D. Runtime trigger | Unsafe | Plane violation | Hidden coupling | Misplaced | Mixed | Forbidden |

## Recommended Implementation Path

The design is complete enough to admit a separate implementation dry run. That Mission may only:

1. extend existing OMP/CPS dependency fields with owner-scoped evaluated fingerprints and heartbeat admission state;
2. extend existing validators for identity, freshness, replay, atomic context acquisition and `NO_CHANGE` behavior;
3. test heartbeat/manual concurrency and fail-closed paths;
4. create one explicit Codex thread heartbeat automation after dry-run approval;
5. execute read-only wakeup certification before enabling any automatic Mission admission;
6. preserve operator pause/delete and the 30-day expiration;
7. prohibit Runtime, routing, Authority, Candidate, packet and user changes.

Implementation is allowed only as `BOUNDARY_ADAPTER_AND_READ_ONLY_HEARTBEAT_CERTIFICATION`. Runtime execution automation remains outside scope.

## Final Output

```text
MISSION_ID = V7_OMP_CODEX_HEARTBEAT_ADAPTER_DESIGN_AND_CERTIFICATION_V1
RUN_NONCE = V7_OMP_HEARTBEAT_ADAPTER_DESIGN_V1_82F6A913D4CE
CURRENT_MODEL = OPERATOR_REENTRY_PLUS_CODEX_SELF_CONTINUATION_INSIDE_ACTIVE_INVOCATION
ACTIVATION_OWNER = EXISTING_CODEX_AUTOMATION_PLATFORM
ACTIVATION_TARGET = EXISTING_CODEX_OMP_CONSUMER_IN_APPROVED_TARGET_THREAD
CONTRACT_STATUS = COMPLETE_CERTIFIED_DESIGN
FIELDS_DEFINED = 20_REQUIRED_PLUS_10_ADDITIONAL_FIELDS
REPLAY_MODEL = AUTOMATION_THREAD_SLOT_EVENT_PLUS_OWNER_GENERATION_DEPENDENCY_FINGERPRINT_AND_FRESH_MISSION_ID
CONCURRENCY_MODEL = REUSE_ATOMIC_CPS_CURRENT_EXECUTION_MISSION_CONTEXT_NO_AUTOMATIC_STEAL
NO_CHANGE_MODEL = TERMINAL_NON_ERROR_NO_MISSION_NO_RETRY_NO_MUTATION_NO_OPERATOR_ESCALATION
SAFETY_BOUNDARY_RESULT = PASS_ALL_OWNER_AND_PLANE_BOUNDARIES_PRESERVED
OPTION_COMPARISON = OPTION_B_SELECTED; OPTION_A_FALLBACK; OPTION_C_REJECTED; OPTION_D_FORBIDDEN
RECOMMENDED_MODEL = CODEX_THREAD_HEARTBEAT_PLUS_FAIL_CLOSED_V7_BOUNDARY_ADAPTER
IMPLEMENTATION_ALLOWED = YES_BOUNDARY_ADAPTER_AND_READ_ONLY_HEARTBEAT_CERTIFICATION_ONLY
NEW_OWNER_REQUIRED = NO
NEW_ARCHITECTURE_REQUIRED = NO
REPORT_PATH = docs/reports/engineering/2026-07-12_220030_codex_heartbeat_adapter_design_and_certification.md
FINAL_VERDICT = CODEX_HEARTBEAT_ADAPTER_DESIGN_CERTIFIED
```
