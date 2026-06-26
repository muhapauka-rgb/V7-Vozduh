# Engineering Report: Master Implementation Justification Audit

## Summary

Проведен финальный root-cause audit текущего governed execution path без реализации, runtime apply, user movement, новых owners, новых backlog items или редизайна.

Вывод:

Текущая реализация частично оправдана архитектурой и безопасностью, но не полностью.

`GOVERNED_ONLY` объясняет строгую привязку к exact packet, stop-safe поведение и запрет на замену approved packet после approval. Однако повторная сборка decision/packet перед lease и связь `decision_id` с `packet_id` не являются постоянным архитектурным требованием. Это расхождение с канонической моделью:

```text
Decision Snapshot
  -> Fresh Packet
```

## Action Performed

- Прочитан текущий Product / Runtime / Canonical / OMP контекст.
- Проверены существующие engineering reports по Decision Ownership, Execution Equivalence, Governed Exit, Packet Approval Exit и User Entity.
- Прослежен текущий путь реализации:

```text
Reality
  -> Planner / autoswitch observe
  -> Decision surface
  -> Packet preview
  -> Operator approval
  -> Lease creation command
  -> Lease owner
  -> Restore barrier
  -> Runtime apply owner
  -> Verification
  -> Outcome closure
```

Код не изменялся.

## Objective Observations

### Canonical Architecture

Canonical Reference задает объектную иерархию:

```text
Action Class
  -> Decision Snapshot
  -> Eligibility Decision
  -> Execution Decision
  -> Fresh Packet
```

Runtime Model задает lifecycle:

```text
Read Decision Snapshot
  -> Policy
  -> Safety
  -> Authority
  -> Packet
  -> Execute OR Stop
```

Packet-level approval остается временным fallback только для `GOVERNED_ONLY`.

### Current Implementation

`admin_core/operator_execution_pipeline.py::_preview_packet_for_candidate` создает `packet_id`, `operation_id`, `selected_move_hash` и `decision_id` вместе внутри packet preview.

Текущий `decision_id` строится из:

```text
recommendation_id + packet_id
```

Следствие:

если packet preview пересоздан, `packet_id` может измениться, а вместе с ним меняется и `decision_id`.

`admin_core/operator_execution.py::create_execution_lease_from_preview` корректно сохраняет identity уже переданного preview и fail-closed при mismatch.

`tools/v7-governed-canary-dry-run-cycle --create-execution-lease` перед созданием lease заново строит текущий decision surface / packet preview и только потом пытается связать approval с текущим preview.

`tools/v7-users-autoswitch` корректно потребляет valid approved plan lock во время apply, а при mismatch / stale / unsafe gate fail-closed.

## Implementation Path Classification

| Step | Owner | Why it exists | Classification |
| --- | --- | --- | --- |
| Reality / Current State read | Current Program State / runtime state owners | Runtime cannot act on stale or absent state. | Architecture + safety |
| Planner / autoswitch observe | Planner / autoswitch owner | Finds current candidate and validates present reality. | Architecture + safety |
| Decision surface | Decision/read-model owners | Converts reality into operator/runtime decision context. | Architecture |
| Packet preview creation | Execution packet owner through governed pipeline | Builds bounded executable artifact for current `GOVERNED_ONLY` fallback. | Temporary `GOVERNED_ONLY` + safety |
| Operator approval of exact packet | OMP / Policy 004 / packet owner | First class is not certified for class/policy authority yet. | Temporary `GOVERNED_ONLY` |
| Lease creation after another dry-run | Governed dry-run CLI / packet owner | Revalidates current state before lease, but also rebuilds preview. | Safety intent + implementation detail |
| Execution lease | Packet owner | Freezes approved packet after lease exists. | Architecture + safety |
| Restore barrier | Restore / rollback owner | Prevents unbounded or unprepared mutation. | Architecture + safety |
| Approved plan lock consumption | Autoswitch apply owner | Ensures apply uses the approved selected move, not a new one. | Architecture + safety |
| Runtime stop on mismatch | Runtime / packet / autoswitch owners | Prevents unauthorized stale or changed action. | Architecture + safety |
| Verification / outcome closure | Verification / feedback / learning owners | Converts real action into trusted evidence. | Architecture |

## Special Questions

### Why Planner Executes Again

Because the governed lease creation command rebuilds current decision surface before creating a lease. This is partly a safety revalidation, but it is not architecturally required to regenerate the approved decision identity before lease.

Classification:

`IMPLEMENTATION_DETAIL_WITH_SAFETY_INTENT`

### Why Packet Regenerates

Because the lease creation entrypoint reuses the dry-run cycle machinery instead of consuming the exact previously produced READY preview as the frozen decision/packet handoff.

Classification:

`IMPLEMENTATION_DETAIL`

### Why Decision Regenerates

Because `decision_id` is generated inside packet preview and includes `packet_id`.

Classification:

`IMPLEMENTATION_DIVERGENCE`

### Why Lease Is Created After Another Dry-Run

Because the current CLI path treats lease creation as a fresh governed dry-run cycle plus identity binding, not as direct consumption of an already frozen preview.

Classification:

`IMPLEMENTATION_DETAIL`

### Why Packet Is Coupled To Decision ID

The code derives `decision_id` from `recommendation_id` and `packet_id`.

Architecture does not require this. Canonical model says Decision Snapshot precedes Packet.

Classification:

`IMPLEMENTATION_DIVERGENCE`

### Why Decision ID Is Coupled To Packet ID

Same cause: decision identity is materialized inside `_preview_packet_for_candidate`.

Classification:

`IMPLEMENTATION_DIVERGENCE`

### Why Runtime Stops

Runtime stops because exact packet approval is still the temporary `GOVERNED_ONLY` authority boundary. A changed packet / decision / selected move cannot be treated as approved.

Classification:

`ARCHITECTURE_AND_SAFETY_JUSTIFIED`

### Why Runtime Does Not Freeze Earlier

The architecture already wants Decision Snapshot before Packet, but current governed A4 implementation lacks a separate pre-lease frozen Decision Snapshot / preview handoff.

Classification:

`INCOMPLETE_IMPLEMENTATION_OF_EXISTING_ARCHITECTURE`

### Why Approval Is Attached To Packet

Because first action class is still `GOVERNED_ONLY`; Action-Class Authority / Delegated Autonomy Policy is not certified or approved yet.

Classification:

`TEMPORARY_GOVERNED_ONLY`

## Hypothesis Falsification

| Hypothesis | Result | Reason |
| --- | --- | --- |
| H1: Decision may legitimately change before apply. | `PARTIAL` | It may be revalidated before lease, but not regenerate identity after a frozen Decision Snapshot. |
| H2: Planner rerun is required by architecture. | `FALSIFIED` | Revalidation is required; identity-regenerating planner rerun before lease is an implementation choice. |
| H3: Lease owner regenerates the packet. | `FALSIFIED` | Packet owner preserves preview identity; the wrapper rebuilds preview before lease. |
| H4: Apply owner ignores approval. | `FALSIFIED` | Apply consumes valid approved plan lock and fails closed on mismatch. |
| H5: Packet is the correct durable authority object. | `FALSIFIED` | Product/OMP say packet approval is transitional. |
| H6: Exact packet approval is permanent. | `FALSIFIED` | It is temporary `GOVERNED_ONLY`. |
| H7: Runtime stop is a bug. | `FALSIFIED` | Stop on mismatch is correct safety behavior. |
| H8: Current implementation exactly matches architecture. | `FALSIFIED` | Architecture orders Decision Snapshot before Packet; implementation derives decision from Packet. |
| H9: New architecture is required. | `FALSIFIED` | Existing owners and backlog already cover this path. |

## Commercial Comparison

| System family | Authority object | Execution object | Comparison to V7 |
| --- | --- | --- | --- |
| Cisco NSO | Service intent / transaction constraints | Concrete device changes | Does not approve packet-like artifacts as durable authority. |
| Cisco Crosswork | Operational intent / policy | Current execution plan | Revalidates before execution, but authority is policy/intent. |
| Juniper Apstra | Intent / blueprint | Rendered config / operations | Intent persists; execution artifacts are regenerated safely. |
| AWS control planes | API request / policy / IAM bounds | Current control-plane operation | Revalidates until commit; stale generated artifacts are not durable authority. |
| Google SRE | Policy / SLO / operational envelope | Current mitigation action | Human approval tends to bind risk envelope, not packet identity. |
| Cloudflare | Policy / rollout / traffic control envelope | Fresh routing / mitigation action | Uses bounded progressive execution and rollback, not durable packet approval. |
| Kubernetes | Desired state / admission / policy | Reconciler action | Reconcile loop regenerates actions inside policy; stops on admission or safety failure. |

V7's target architecture matches mature systems:

```text
Authority envelope
  -> fresh runtime decision
  -> fresh packet
  -> execute or stop
```

The current exact packet fallback is acceptable only as early governed proof.

## Root Cause

The single root cause is:

```text
The current governed execution path lacks a pre-lease frozen Decision Snapshot / approved preview handoff, while current decision_id is generated inside packet preview and includes packet_id. Therefore the lease-creation entrypoint can rebuild a semantically current but identity-different packet/decision before freeze, causing approval mismatch and stop-safe behavior.
```

## Existing Owner Mapping

| Responsibility | Existing owner |
| --- | --- |
| Decision semantics | `docs/reference/V7_DECISION_MODEL.md` |
| Runtime lifecycle | `docs/reference/V7_RUNTIME_MODEL.md` |
| Packet / lease owner | `admin_core/operator_execution.py` |
| Governed preview / decision surface path | `admin_core/operator_execution_pipeline.py` |
| Governed lease CLI entrypoint | `tools/v7-governed-canary-dry-run-cycle` |
| Apply / approved plan lock consumption | `tools/v7-users-autoswitch` |
| Authority transition | OMP, `POLICY_004_AUTHORITY.md`, `POLICY_005_ACTION_CLASS_PROMOTION.md` |

Need New Owner:

`FALSE`

## Existing Backlog Mapping

Primary existing owner:

`A4`

Reason:

A4 is the current governed action-class evidence path and currently exposes the packet approval / lease binding problem.

Secondary existing owner:

`B18`

Reason:

B18 owns broader owner-issued version / lease / read-model discipline once A4 evidence work moves into generalized runtime capability.

Need New Backlog Item:

`FALSE`

## Temporary Or Permanent

Temporary:

- exact packet approval;
- exact user binding;
- packet as approval object;
- strict approval mismatch stop in `GOVERNED_ONLY`;
- repeated operator approval while class is uncertified.

Permanent:

- Decision Snapshot must precede Packet;
- Runtime must not invent decisions;
- Runtime must revalidate until commit;
- Runtime must stop before unsafe mutation;
- Packet is a transient execution artifact in the target model;
- durable authority moves toward Action Class / Delegated Policy / Business Objective constraints.

## Engineering Conclusions

Current implementation is not fully architecturally justified.

Correctly justified:

- stop-safe behavior;
- no replacement of exact approved packet under `GOVERNED_ONLY`;
- execution lease immutability after creation;
- approved plan lock validation before apply;
- restore barrier and verification gates;
- refusal to move users on identity mismatch.

Not architecturally justified as final design:

- decision identity generated inside packet preview;
- `decision_id` derived from `packet_id`;
- lease creation entrypoint rebuilding packet/decision preview instead of consuming a frozen READY decision/preview handoff;
- treating packet identity as if it were the durable decision identity.

## Impact

Production impact:

No runtime change was made. Current behavior remains safe because Runtime stops before mutation.

Product impact:

The audit confirms that the stale packet approval loop is not a product architecture target. It is a temporary governed fallback plus incomplete implementation of the existing Decision Snapshot before Packet model.

Runtime impact:

No runtime behavior changed.

Backlog impact:

No new backlog item required.

Canonical impact:

No canonical owner update required. Existing Product Specification, Runtime Model and Canonical Reference already state the durable model.

## Evidence

- `docs/product/V7_PRODUCT_SPECIFICATION.md`: packet approval is transitional and not the long-term product model.
- `docs/reference/V7_RUNTIME_MODEL.md`: Runtime reads Decision Snapshot before Packet and execution lease freezes approved packet identity while active.
- `docs/reference/V7_CANONICAL_REFERENCE.md`: canonical hierarchy places Decision Snapshot before Fresh Packet and defines Packet as transient runtime artifact.
- `admin_core/operator_execution_pipeline.py::_preview_packet_for_candidate`: current implementation derives `decision_id` from `packet_id`.
- `admin_core/operator_execution.py::create_execution_lease_from_preview`: packet owner preserves supplied preview identity and fails closed on binding mismatch.
- `tools/v7-users-autoswitch`: apply owner consumes approved plan lock when valid and fails closed when gates are unsafe.
- `docs/reports/engineering/2026-06-27_014822_master_decision_ownership_audit.md`: prior root-cause evidence for decision identity coupling.

## Next Step

Continue OMP through existing A4 / B18 ownership.

Do not create new architecture.

Do not create new owner.

Do not create new backlog item.

Do not weaken stop-safe behavior.

## Re-audit Rule

Do not repeat this audit unless one of the following changes:

- governed dry-run / lease creation path changes materially;
- Decision Snapshot ownership changes materially;
- packet identity generation changes materially;
- production evidence disproves this classification;
- explicit operator request.

## Final Verdict

`IMPLEMENTATION_DIVERGES_FROM_ARCHITECTURE`
