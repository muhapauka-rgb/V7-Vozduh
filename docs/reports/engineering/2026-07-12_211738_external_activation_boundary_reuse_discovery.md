# External Activation Boundary Reuse Discovery

Mission ID: `V7_OMP_EXTERNAL_ACTIVATION_BOUNDARY_REUSE_DISCOVERY_V1`  
Run nonce: `V7_OMP_ACTIVATION_REUSE_DISCOVERY_V1_91D74B62E8FA`  
Started: `2026-07-12T21:17:38+0700`  
Mission type: architecture discovery / existing-owner reuse analysis  
Implementation performed: `NO`  
Final verdict: `EXTERNAL_PLATFORM_ACTIVATION_AVAILABLE`

## Current Limitation

V7 can self-continue only inside an active Codex invocation. When the READY frontier is empty and `REAL_WORLD_LIMIT` is proven, the execution context ends. CPS, OMP, validators, Runtime and evidence producers cannot start a new Codex context.

The prior boundary discovery correctly required an explicit Engineering Plane activation boundary. This Mission found an existing external platform capability that can own activation without adding a V7 scheduler or Runtime component: Codex App thread heartbeat automation.

No V7 automation is currently configured. The only local automation instance is the unrelated, paused `nightly-qg-check` for `/Users/ponch/V7-News`.

## Source And Capability Verification

Current-session Codex App capability exposes:

- thread heartbeat automations attached to the current local thread;
- recurring wakeups that return to the same task context;
- platform-owned schedule and automation identity;
- explicit target thread identity;
- status control and deletion through the existing Codex automation owner;
- standalone project automations for cases that do not require thread continuity.

Official OpenAI guidance confirms that Codex automations run automatically on a schedule, can return to the same conversation, and surface results for review. It also states that local automations depend on the machine being awake and Codex running.

Sources:

- https://openai.com/academy/codex-automations/
- https://openai.com/index/introducing-the-codex-app/
- https://cdn.openai.com/pdf/8a9f00cf-d379-4e20-b06f-dd7ba5196a11/OAI_WhitePaper_Codex-maxxing26.pdf

Source limitation: the official Codex manual fetch reached the official endpoint but could not verify the expected response checksum header. The conclusion therefore relies on official OpenAI product documentation plus the callable `codex_app__automation_update` capability exposed in this exact session.

## Existing Entry Point Inventory

| Entry point | Owner | Trigger | Authentication | Current scope | Can start Codex OMP | Validate context | Reject replay | Record result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Manual `Continue OMP` | Operator + Codex App | Authenticated user message | Signed-in Codex session | Current thread | `YES` | `YES`, ECR/CPS | `YES`, Mission identity guards | `YES`, thread/report |
| Normal Codex invocation | Codex App / Codex consumer | User or platform task start | Platform session | One task | `YES` | `YES` | `PARTIAL`, V7 contract required | `YES` |
| Codex thread heartbeat | Existing Codex Automation platform | Platform schedule | Platform account/session and target thread | Same thread, recurring | `YES` | `YES`, prompt invokes ECR/CPS | `PARTIAL`, V7 dependency fingerprint adapter required | `YES`, thread/review surface |
| Codex standalone automation | Existing Codex Automation platform | Platform schedule | Platform account/project target | New local project job | `YES_WITH_NEW_CONTEXT` | `PARTIAL` | `PARTIAL` | `YES`, review surface |
| CI/CD workflow | None in repository | None | None | No `.github/workflows` | `NO_CURRENT_PATH` | `NO` | `NO` | `NO` |
| Programmatic Codex access | External platform capability announced | CI/internal automation request | Scoped workspace token | Not configured or verified for V7 | `NOT_CERTIFIED` | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` |
| Safe deploy hook | Existing deploy owner | Explicit deploy command | Existing deployment access | Deploy approved package | `NO` | Runtime/source only | Deploy identity only | Deploy evidence only |
| Systemd timers | Observation/Runtime owners | Time interval | Host service identity | Evidence and transactions | `NO` | Runtime state only | Not OMP replay | Runtime evidence only |
| Operator execution endpoints | Transaction owners | Explicit bounded operation | Existing operation authority | Packet/apply/verify | `NO` | Transaction context | Packet/operation identity | Transaction result |
| Evidence producers | Observation/feedback/learning owners | Production events | Owner-specific | Evidence generation | `NO` | Evidence only | Source-specific | Evidence record |
| CPS/OMP validators | Source governance owner | Explicit tool invocation | Local engineering context | Read/validate source | `NO` | `YES` | Validate only | Validation result |

## Owner Activation Matrix

| Owner | Can activate | Why | Missing capability | Safe extension? |
| --- | --- | --- | --- | --- |
| CPS | `NO` | Volatile state owner | Active execution and authentication | `NO`; must remain passive |
| OMP | `NO` | Continuation law and dependency owner | Process activation | `NO`; contract is not runner |
| Runtime | `NO` | Observe/execute/verify bounded runtime work | Engineering Mission authority | `FORBIDDEN` |
| Codex OMP consumer | `YES_WHEN_INVOKED` | Executes ECR/OMP/CPS loop | Self-wakeup after termination | `YES` as activation target, not trigger owner |
| Operator | `YES` | Current authenticated boundary | Automatic continuation | Current safe model only |
| Codex Automation platform | `YES` | Existing authenticated heartbeat and thread targeting | V7 evidence/fingerprint admission contract | `YES`, bounded adapter only |
| CI/CD | `NO_CURRENT_PATH` | No repository workflow or certified token integration | Entire V7 activation binding | Not selected |
| Deployment system | `NO` | Deploy-only responsibility | Mission execution | `NO` |
| Validators | `NO` | Validate state when called | Activation lifecycle | `NO` |
| Evidence producers | `NO` | Own production evidence | Engineering execution | `NO` |

Ownership decision:

```text
Activation schedule / thread wakeup owner = existing Codex Automation platform
Activation target = existing Codex OMP consumer
Program state owner = CPS
Continuation/admission law owner = OMP
Evidence sufficiency owner = existing capability owner
Runtime authority = NONE_FROM_ACTIVATION
```

No new V7 owner is required. The required work is a future, explicit boundary adapter contract between existing Codex Automation activation and existing OMP/CPS admission.

## Platform Reuse Analysis

Classification: `AVAILABLE_WITH_BOUNDARY_ADAPTER`.

| Requirement | Platform result | V7 adapter requirement |
| --- | --- | --- |
| Authenticated trigger | `AVAILABLE`; Codex account/local task context | Bind allowed automation and target thread IDs |
| Execution identity | `AVAILABLE`; automation/thread/run context | Bind wakeup to fresh V7 Mission identity |
| Same-context continuation | `AVAILABLE`; thread heartbeat | Re-read CPS; never trust stale chat state |
| Audit/result surface | `AVAILABLE`; thread and review result | Persist only owner-backed Engineering Report/CPS changes when admitted |
| Deduplication | `NOT_PROVEN_FOR_V7_EVENT_IDENTITY` | Dependency fingerprint and consumed-generation guard |
| Concurrency control | `NOT_PROVEN_FOR_V7_MISSION_IDENTITY` | One active OMP activation lease/mission guard |
| Failure reporting | `AVAILABLE_AT_PLATFORM_SURFACE` | Normalize `NO_CHANGE`, `STOP_SAFE`, `ADMITTED`, `FAILED` |
| Bounded retries | `NOT_PROVEN` | No blind retry; each heartbeat is fresh reconciliation |
| External event webhook | `NOT_AVAILABLE_IN_VERIFIED_THREAD_AUTOMATION` | Use periodic bounded reconciliation only |
| Runtime authority | `NONE` | Must remain none |

The platform can supply Option B from the prior discovery: periodic bounded reconciliation. It does not currently certify event-driven Option C.

## Safety Contract

A future heartbeat adapter must carry or derive:

```text
AUTOMATION_ID
TARGET_THREAD_ID
PROJECT_ID
WAKEUP_RUN_ID
EVENT_ID
SOURCE_OWNER
SOURCE_GENERATION
EVENT_TIME
FRESHNESS_RULE
DEPENDENCY_FINGERPRINT_BEFORE
DEPENDENCY_FINGERPRINT_AFTER
DEPENDENCY_CHANGED
TARGET_CAPABILITY
CURRENT_CPS_GENERATION
MISSION_SCOPE
AUTHORIZATION_SCOPE = ENGINEERING_CONTEXT_START_ONLY
REPLAY_PROTECTION
CONCURRENCY_CONTROL
ACTIVATION_RESULT
NO_RUNTIME_AUTHORITY = TRUE
NO_USER_MOVEMENT_AUTHORITY = TRUE
NO_PACKET_AUTHORITY = TRUE
NO_CANDIDATE_AUTHORITY = TRUE
```

Required wakeup behavior:

```text
heartbeat
-> authenticate platform/thread/project identity
-> read fresh CPS and owner evidence
-> compare dependency generation/fingerprint
-> unchanged, stale, duplicate or ambiguous: record NO_CHANGE/STOP_SAFE and end
-> changed: capability owner evaluates evidence sufficiency
-> reconcile dependency graph read-only
-> READY frontier exists: create fresh Mission identity through normal OMP admission
-> no READY frontier: end without mutation
```

Activation may start an Engineering execution context only. It may not select users, create a routing Candidate or packet, grant Authority, apply Runtime, move users, alter thresholds, bypass CPS/OMP/validators, or reuse historical identities.

## Boundary Options

| Option | Safety | Autonomy | Auditability | Hidden scheduler | Plane integrity | Result |
| --- | --- | --- | --- | --- | --- | --- |
| A. Operator boundary | Highest | Manual | High | None | Preserved | `ALLOWED_CURRENT_FALLBACK` |
| B. Codex thread heartbeat | High after adapter certification | Periodic autonomous reentry | Platform thread + V7 report | None; platform automation is explicit | Preserved | `RECOMMENDED_REUSE` |
| C. New V7 activation owner | Potentially high | Full | Must be built | New scheduler risk | Requires architecture | `REJECTED_NOT_NECESSARY` |
| D. Runtime-owned activation | Unsafe | Misplaced | Mixed planes | Hidden Mission scheduler | Violated | `FORBIDDEN` |

## Long-Term Autonomy Compatibility

| Model | Autonomous engineering evolution | Safety/governance | Auditability | No hidden scheduler | Verdict |
| --- | --- | --- | --- | --- | --- |
| Operator | `NO` | `PASS` | `PASS` | `PASS` | Safe fallback |
| Codex thread heartbeat + V7 adapter | `YES_BOUNDED` | `PASS_IF_CERTIFIED` | `PASS` | `PASS`; scheduler is explicit external platform owner | Best fit |
| Standalone Codex project automation | `PARTIAL` | Context reconstruction risk | `PASS` | `PASS` | Secondary option only |
| CI/CD/programmatic dispatch | `POTENTIAL` | Not verified | Potential | Potential | Research required before use |
| New V7 service | `YES` | New architecture risk | Design-dependent | Fails reuse objective | Not justified |
| Runtime trigger | `NO_LEGAL_MODEL` | `FAIL` | Mixed ownership | `FAIL` | Forbidden |

## Recommendation And Readiness

Selected model: reuse the existing Codex App thread heartbeat as the explicit external activation owner, with a future V7-specific fail-closed boundary adapter contract.

Why:

- it can return to this same task without operator prompting;
- scheduling, task activation, authentication context and result surfacing remain outside V7 Runtime;
- it reuses the existing Codex OMP consumer rather than creating a second executor;
- periodic reconciliation is sufficient for `REAL_WORLD_LIMIT` evidence, where low latency is not a Runtime safety requirement;
- every wakeup can remain read-only unless fresh owner-backed evidence creates a legal READY frontier.

Rejected:

- new V7 scheduler/daemon/queue because platform activation already exists;
- Runtime-owned trigger because it violates plane ownership;
- CI/CD/programmatic activation because no V7 path, identity binding or replay contract is currently certified;
- standalone automation as the primary route because same-thread heartbeat preserves the established OMP context while still requiring fresh CPS reads.

Implementation readiness: `NOT_READY_IN_THIS_MISSION`. A separate dry-run Mission must define cadence, automation identity, target thread, no-change behavior, concurrency lease, dependency fingerprint consumption, failure reporting and pause/termination rules. Creating the automation requires explicit implementation authorization.

## Final Output

```text
MISSION_ID = V7_OMP_EXTERNAL_ACTIVATION_BOUNDARY_REUSE_DISCOVERY_V1
RUN_NONCE = V7_OMP_ACTIVATION_REUSE_DISCOVERY_V1_91D74B62E8FA
CURRENT_ACTIVATION_MODEL = OPERATOR_CONTINUE_OMP
AVAILABLE_ENTRY_POINTS = OPERATOR_MESSAGE,CODEX_INVOCATION,CODEX_THREAD_HEARTBEAT,CODEX_STANDALONE_AUTOMATION
OWNER_ACTIVATION_MATRIX = CODEX_AUTOMATION_PLATFORM_CAN_ACTIVATE; CODEX_OMP_CONSUMER_CAN_EXECUTE; CPS_OMP_RUNTIME_CANNOT_ACTIVATE
PLATFORM_REUSE_RESULT = AVAILABLE_WITH_BOUNDARY_ADAPTER
SAFE_BOUNDARY_RESULT = CODEX_THREAD_HEARTBEAT_TO_FRESH_ECR_CPS_OMP_ADMISSION_NO_RUNTIME_AUTHORITY
AUTONOMY_COMPATIBILITY_RESULT = BOUNDED_PERIODIC_AUTONOMY_COMPATIBLE_AFTER_ADAPTER_CERTIFICATION
RECOMMENDED_DIRECTION = REUSE_CODEX_THREAD_HEARTBEAT; KEEP_OPERATOR_AS_FALLBACK; DO_NOT_CREATE_V7_SCHEDULER
IMPLEMENTATION_ALLOWED = NO
NEW_OWNER_REQUIRED = NO
NEW_ARCHITECTURE_REQUIRED = NO_FUNDAMENTAL_ARCHITECTURE; EXPLICIT_INTEGRATION_CONTRACT_REQUIRED
REPORT_PATH = docs/reports/engineering/2026-07-12_211738_external_activation_boundary_reuse_discovery.md
FINAL_VERDICT = EXTERNAL_PLATFORM_ACTIVATION_AVAILABLE
```
