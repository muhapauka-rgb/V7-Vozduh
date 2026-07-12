# External Continuation Boundary Discovery

Mission ID: `V7_OMP_EXTERNAL_CONTINUATION_BOUNDARY_DISCOVERY_AND_DESIGN_V1`  
Run nonce: `V7_OMP_EXTERNAL_WAKEUP_DISCOVERY_V1_7C91B4E62A8F`  
Started: `2026-07-12T21:02:46+0700`  
Mission type: architecture discovery / boundary definition  
Implementation performed: `NO`  
Final verdict: `EXPLICIT_CONTINUATION_BOUNDARY_REQUIRED`

## Current Model

V7 has two distinct continuation scopes:

```text
active Codex invocation
-> OMP Self-Continuation
-> CPS dependency reconciliation
-> READY frontier execution
-> repeat until a program terminal

REAL_WORLD_LIMIT + READY frontier empty
-> Codex invocation ends
-> external evidence may later change
-> no existing owner starts a new Codex invocation
```

The first scope is complete and owner-backed. The second scope is absent by design. Passive CPS state and OMP rules cannot activate a terminated execution consumer.

## Discovered Limitation

`tools/v7_sync_lib.py::atomic_reconcile_cps` is not called by a production entrypoint; its current callers are tests. Existing systemd timers produce observation or Runtime transaction evidence only. They do not invoke CPS reconciliation or Codex, and their owners must not become OMP Mission schedulers.

The Runtime Model contains a durable design sequence `Outcome -> Learning -> Update CPS -> Notify OMP -> Sleep`, but explicitly states that it does not implement a daemon, timer, event-consumer change, autonomous execution, or apply path. `Notify OMP` is therefore an unimplemented boundary contract, not a dormant trigger.

## Owner Analysis

| Function | Existing owner | Current responsibility | Missing responsibility | Can extend existing owner? |
| --- | --- | --- | --- | --- |
| Store volatile program state | CPS | Current capability, stop, generation and frontier projections | Active wakeup | `NO`; state owner must remain passive |
| Decide continuation | OMP | Dependency lifecycle, frontier and stop/continue law | Start a process after termination | `NO`; program contract is not an executor |
| Execute Missions | Codex OMP consumer | Execute and self-continue inside an active invocation | Receive authenticated external activation | `PARTIAL`; consumer can accept a future validated activation but cannot wake itself |
| Produce evidence | Observation, feedback, learning and Runtime owners | Publish owner-backed production evidence | Start Engineering Plane execution | `NO`; would violate plane ownership |
| Initiate current external continuation | Operator | Issue `Continue OMP` after a valid boundary | Long-lived autonomous activation | `YES` for current manual model only |
| Reconcile source truth | `v7_sync_lib` validators | Validate CPS/OMP/source consistency when invoked | Monitor production and schedule Missions | `NO`; would create hidden orchestration |
| External activation | `NONE_IN_V7` | None | Authenticate, deduplicate and serialize event-to-Codex activation | No existing V7 owner legally owns the full responsibility |

Owner decision: long-lived automatic continuation requires one explicit Engineering Plane activation boundary. It cannot be assigned implicitly to CPS, OMP, Runtime, validators, or the operator. Whether that boundary is provided by an existing external Codex platform facility or a newly governed V7-facing adapter must be proven in a later discovery before implementation.

## Safe Boundary Model

```text
external evidence owner
-> immutable evidence identity and generation
-> explicit continuation activation boundary
-> authentication / scope / freshness / replay / concurrency validation
-> read-only CPS reconciliation
-> capability-owner evidence sufficiency decision
-> WAITING -> READY only after verified dependency change
-> new Codex OMP invocation
-> fresh Mission identity
-> normal OMP admission and authority gates
-> no mutation before all existing validation
```

The activation boundary may request a new Engineering Plane execution context. It may not decide capability readiness, create Candidates or packets, grant Authority, select users, mutate Runtime, or bypass OMP admission.

## Trigger Model Analysis

| Model | Classification | Required boundary | Main result |
| --- | --- | --- | --- |
| A. Operator initiated | `ALLOWED_CURRENT_MODEL` | Operator -> Codex | Safest current implementation; manual continuation remains necessary |
| B. Periodic bounded reconciliation | `REQUIRES_EXPLICIT_AUTHORITY_AND_OWNER` | Approved schedule -> activation boundary | Bounded and simpler to rate-limit, but it is still a scheduler and must be explicit |
| C. Event-driven continuation | `REQUIRES_EXPLICIT_AUTHORITY_AND_OWNER` | Authenticated event receiver -> activation boundary | Lowest latency; requires durable identity, deduplication, concurrency and storm protection |
| D. Runtime-owned continuation | `FORBIDDEN` | Runtime -> OMP Mission execution | Violates Runtime/Engineering separation and creates a hidden Mission scheduler |

No automatic model is allowed merely by adding CPS fields or validators. Models B and C are future architecture candidates, not approved implementations.

## Automatic Continuation Risk Matrix

| Risk | Required control | Boundary result |
| --- | --- | --- |
| Replay | Event ID, source generation, consumed-event record, fresh Mission identity | Duplicate event cannot start a second Mission |
| Stale evidence | Owner timestamp/version, freshness rule, current CPS generation | Stale report or historical evidence is rejected |
| Duplicate execution | Single active continuation lease and idempotency key | At most one activation for the same dependency generation |
| Infinite loop | No-progress fingerprint, bounded attempts, program-terminal classification | Same unchanged dependency cannot retrigger |
| Event storm | Coalescing by capability/dependency generation, rate and concurrency limits | Bursts produce one bounded reconciliation |
| Dependency oscillation | Stable owner generation plus explicit transition verification | READY cannot flap on uncommitted observations |
| Authority bypass | Activation grants no operational or engineering authority | Normal OMP/Authority gates remain mandatory |
| Plane violation | Runtime emits evidence only; Engineering Plane owns activation | Runtime cannot execute Missions |
| Accidental mutation | Reconciliation is read-only until Mission admission completes | No Candidate, packet, user movement or Runtime apply at activation |
| Lost activation | Durable accepted/rejected activation result and observable reason | Failure is explicit, not silently dropped |

## Large-Scale System Principles

Only engineering principles were mapped; no external architecture is imported.

- Kubernetes controllers are explicit long-running control loops that watch declared resources and reconcile current toward desired state. The active controller is separate from the observed objects; passive state does not execute itself. Controllers also scope ownership to the resources they control.
- GitHub Actions separates event trigger, workflow definition, runner execution and concurrency policy. External activity requires an explicit `repository_dispatch` event; multiple triggers can create multiple runs unless concurrency is governed.
- AWS Step Functions makes execution start an explicit API boundary. Standard workflow starts use execution identity and idempotency semantics; event retries are safe only when idempotency is designed.
- Google Eventarc explicitly routes authenticated events to Workflows, passes a structured CloudEvent, uses an invoking service account and provides a bounded deduplication window. Event delivery and workflow execution remain separate lifecycle stages.
- Google SRE recommends autonomy for well-scoped known procedures, but warns that automation centralizes mistakes and should be owned by the teams that own the affected services, with fine-grained access control and introspection.

Primary sources:

- https://kubernetes.io/docs/concepts/architecture/controller/
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency
- https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html
- https://docs.aws.amazon.com/step-functions/latest/dg/connect-eventbridge.html
- https://docs.cloud.google.com/workflows/docs/trigger-workflow-eventarc
- https://sre.google/sre-book/automation-at-google/

## REAL_WORLD_LIMIT Semantics

Recommended model: conditional terminal with separate capability and execution semantics.

```text
For one capability:
REAL_WORLD_LIMIT = WAITING_EXTERNAL_DEPENDENCY

For the active Codex invocation:
READY frontier empty = execution context terminal

For the program:
READY frontier empty
+ no approved external continuation mechanism
= PROGRAM_TERMINAL_REAL_WORLD_LIMIT

Future approved activation boundary:
external dependency generation changes
-> start a new invocation
-> reconcile from fresh CPS/evidence
```

The old execution context must never remain logically alive while waiting. A future trigger starts a new invocation with new identity; it does not resume packet, Candidate, lease, Authority, or Mission identity.

## Required Future Contract

If automatic continuation is approved later, the minimum activation contract is:

| Field | Requirement |
| --- | --- |
| `CONTINUATION_EVENT` | Immutable event identity and type |
| `EVENT_OWNER` | Existing evidence owner that emitted the state change |
| `EVENT_SOURCE` | Canonical owner-backed source, never a report |
| `EVENT_GENERATION` | Monotonic/versioned source generation |
| `EVENT_FRESHNESS` | Owner-defined freshness and observed timestamp |
| `DEPENDENCY_CHANGED` | Exact dependency fingerprint delta |
| `REENTRY_REASON` | Capability-specific deterministic reason |
| `TARGET_CAPABILITY` | One WAITING capability or bounded coalesced set |
| `NEW_MISSION_ALLOWED` | Result of activation admission, not evidence production |
| `AUTHORITY_REQUIRED` | Explicit class; activation itself grants none |
| `VERIFICATION_REQUIRED` | Reconciliation and Mission outcome verification |
| `REPLAY_PROTECTION` | Event/owner/generation/CPS identity plus consumption state |
| `NO_MUTATION_BEFORE_VALIDATION` | Mandatory `TRUE` |
| `CONCURRENCY_KEY` | One active activation per program/generation |
| `ACTIVATION_RESULT` | Accepted, coalesced, stale, duplicate, rejected or stop-safe |

Required lifecycle:

```text
PRODUCED
-> AUTHENTICATED
-> FRESHNESS_VALIDATED
-> DEDUPLICATED
-> RECONCILED
-> ACTIVATION_ADMITTED | REJECTED
-> NEW_INVOCATION_STARTED
-> RESULT_RECORDED
```

## Impact And Requirements

- OMP impact now: `NONE`.
- CPS impact now: `NONE`.
- Runtime impact now: `NONE`.
- Authority impact now: `NONE`.
- Implementation allowed: `NO`.
- New owner required: `CONDITIONALLY_YES`; only if no existing external Codex activation facility can be certified as the explicit boundary.
- New architecture required: `YES_FOR_AUTOMATIC_EXTERNAL_CONTINUATION`; narrow Engineering Plane activation boundary only.
- CPS change required later: `POSSIBLE`, only after owner/lifecycle approval; CPS must not become the trigger.
- Runtime change required later: `NO`; evidence producers remain unchanged unless a separate owner contract proves otherwise.

## Rejected Designs

- CPS as scheduler or event consumer.
- OMP document as active executor.
- Runtime or autoswitch timer invoking Codex Missions.
- `atomic_reconcile_cps` polling production state.
- Hidden queue, watcher, retry loop or daemon.
- Reusing historical Mission, packet, Candidate, decision, operation, lease or Authority identity.
- Treating any evidence change as automatic Authority or mutation permission.

## Final Output

```text
MISSION_ID = V7_OMP_EXTERNAL_CONTINUATION_BOUNDARY_DISCOVERY_AND_DESIGN_V1
RUN_NONCE = V7_OMP_EXTERNAL_WAKEUP_DISCOVERY_V1_7C91B4E62A8F
CURRENT_CONTINUATION_MODEL = CODEX_SELF_CONTINUATION_INSIDE_ACTIVE_INVOCATION_PLUS_OPERATOR_REENTRY_AFTER_PROGRAM_TERMINAL
LIMITATION_IDENTIFIED = NO_ACTIVE_OWNER_CAN_START_A_NEW_CODEX_OMP_CONTEXT_FROM_EXTERNAL_EVIDENCE
OWNER_ANALYSIS_RESULT = NO_EXISTING_V7_OWNER_OWNS_EXTERNAL_ACTIVATION_END_TO_END
SAFE_BOUNDARY_MODEL = EXPLICIT_ENGINEERING_PLANE_ACTIVATION_BOUNDARY_BEFORE_NEW_CODEX_INVOCATION
TRIGGER_MODEL_ANALYSIS = OPERATOR_ALLOWED; PERIODIC_OR_EVENT_DRIVEN_REQUIRE_EXPLICIT_OWNER_AND_AUTHORITY; RUNTIME_OWNED_FORBIDDEN
AUTOMATIC_CONTINUATION_RISK_RESULT = CONTROLLABLE_ONLY_WITH_IDENTITY_FRESHNESS_DEDUPLICATION_CONCURRENCY_AND_NO_MUTATION_GATE
REAL_WORLD_LIMIT_SEMANTICS = CONDITIONAL_PROGRAM_TERMINAL_AND_CAPABILITY_LOCAL_WAITING_STATE
RECOMMENDED_DIRECTION = KEEP_OPERATOR_BOUNDARY_UNTIL_EXPLICIT_ACTIVATION_BOUNDARY_IS_APPROVED_AND_CERTIFIED
IMPLEMENTATION_ALLOWED = NO
NEW_OWNER_REQUIRED = CONDITIONALLY_YES_IF_NO_CERTIFIABLE_EXTERNAL_CODEX_ACTIVATION_OWNER_EXISTS
NEW_ARCHITECTURE_REQUIRED = YES_NARROW_EXPLICIT_ACTIVATION_BOUNDARY_FOR_AUTOMATIC_MODE
CPS_CHANGE_REQUIRED = NO_NOW
RUNTIME_CHANGE_REQUIRED = NO
REPORT_PATH = docs/reports/engineering/2026-07-12_210246_external_continuation_boundary_discovery.md
FINAL_VERDICT = EXPLICIT_CONTINUATION_BOUNDARY_REQUIRED
```
