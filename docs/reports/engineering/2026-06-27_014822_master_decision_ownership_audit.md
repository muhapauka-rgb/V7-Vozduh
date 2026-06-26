# Master Decision Ownership Audit

## Summary

Проведен root-cause audit владения `Decision Identity` без реализации, редизайна, новых owners, новых backlog items, runtime apply, authority expansion или user movement.

Главный вывод:

```text
Decision ownership exists architecturally, but current governed A4 implementation materializes Decision Identity too late and couples it to Packet Identity.
```

Это не требует нового owner, backlog item, runtime path, decision object или architecture extension.

Need New Owner: `FALSE`
Need New Backlog Item: `FALSE`
Need New Architecture: `FALSE`

Final verdict:

```text
DECISION_OWNERSHIP_COMPLETE
```

## Action Performed

Прочитаны и сопоставлены существующие владельцы:

- Product Specification / Business Objectives;
- Decision Model;
- Runtime Model;
- OMP;
- Implementation Backlog;
- Current Program State;
- Canonical Reference / Decision Object Model;
- SYSTEM_MAP;
- Engineering Context Resolver / Knowledge Plane;
- Execution Packet owner: `admin_core/operator_execution.py`;
- Execution Lease owner: `admin_core/operator_execution.py`;
- Runtime Apply owner: `tools/v7-users-autoswitch`;
- Planner owner: `tools/v7-users-autoswitch`;
- Governed Dry Run owner: `tools/v7-governed-canary-dry-run-cycle`, `admin_core/operator_execution_pipeline.py`;
- Movement Protection / Runtime Eligibility owners;
- latest Execution Equivalence, Packet Approval Exit, Decision Model, User Entity, Governed Exit audits.

Код не менялся. Runtime не менялся. OMP не менялся. Backlog не менялся.

## Actual Execution Path

Фактический текущий governed A4 путь:

```text
Reality / current state
  -> operator decision surface
  -> autonomous_dry_run_model
  -> candidate selection
  -> packet preview
  -> decision_id materialized inside packet preview
  -> approval prompt
  -> create execution lease command
  -> governed dry-run wrapper rebuilds current candidate/packet preview
  -> binding check compares approved identity with newly resolved identity
  -> if identity differs, stop before lease/apply
  -> if identity matches, packet owner creates execution lease
  -> restore-barrier clearance
  -> autoswitch apply consumes approved plan lock
  -> verification
  -> rollback/no-rollback
  -> outcome closure
  -> learning
```

Actual implementation evidence:

- `admin_core/operator_execution_pipeline.py::_preview_packet_for_candidate` creates:
  - `packet_id`;
  - `operation_id`;
  - `decision_id`.
- Current `decision_id` is derived from:

```text
recommendation_id + packet_id
```

- Therefore a new packet preview can create a new `decision_id`.
- `tools/v7-governed-canary-dry-run-cycle --create-execution-lease` reruns the dry-run/candidate/packet-preview resolution before creating the lease.
- `admin_core/operator_execution.py::packet_from_preview` preserves a given preview identity correctly if it receives that exact preview.
- `tools/v7-users-autoswitch` can consume an approved plan lock when it is valid and fails closed when it is missing, expired, mismatched, or unsafe.

## Decision Objects

| Object | Owner | Producer | Consumer | Mutator | Invalidator | Freeze point | Lifetime | Class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Business Objective | Product Specification | Product Owner / Product Specification | Policies, OMP | Product owner only | Product change | Product certification | Long-lived | Canonical |
| Canonical Policy | Policy Library | Policy lifecycle | OMP, Runtime gates | Explicit policy update | Policy generation change | Policy certification | Long-lived | Canonical |
| Operational Envelope | OMP / Runtime Model / Policy 004 / Policy 005 | OMP + policy gates | Runtime eligibility | OMP / authority owner | authority/policy/blast/freshness change | Class/policy approval | Long-lived + runtime state | Authority |
| Decision Snapshot | Decision Model + decision/read-model owners | Decision surface / governed pipeline | Runtime, packet owner, OMP | Should not mutate after freeze | stale current state, policy/authority/material change | Intended before packet | Runtime attempt | Runtime-consumed |
| Planner Decision | Planner/autoswitch | `tools/v7-users-autoswitch` | governed dry-run, packet preview | Planner only before freeze | source/freshness/material input change | Before packet preview or lease | Runtime attempt | Implementation |
| Eligibility Decision | Runtime Model + gates | runtime eligibility/read models | execute/stop | Runtime gate only | failed gate | Before execution | Runtime attempt | Runtime |
| Execution Decision | Runtime Model + execution owner | eligibility + authority | apply owner | None after execute starts | authority/gate failure before execute | Commit point | One attempt | Runtime |
| Packet Preview | Execution Packet owner / governed dry-run | `operator_execution_pipeline` | operator, lease owner | Should not mutate after approval | packet/material identity change | Approval/lease | Transient | Execution artifact |
| Execution Lease | Packet owner | `admin_core/operator_execution.py` | governed dry-run, apply owner | packet owner status only | timeout, execution, rollback, cancel, material state change | Lease creation | TTL/session | Runtime guard |
| Approved Plan Lock | Packet/restore owner | packet owner | autoswitch apply | none after clearance | mismatch/expiry/material state change | Restore-barrier clearance | One operation | Runtime guard |
| Operation | Execution owner | packet/apply owner | verification/outcome | terminal status only | duplicate/terminal state | execution start | One attempt | Historical after close |
| Selected Move | Planner + packet owner | planner/packet preview | apply owner | none after lock | user/source/target/hash mismatch | approved plan lock | Transient | Execution artifact |
| Verification Plan | Runtime Model / apply owner | governed dry-run | apply/verification/outcome | none after execution | missing/unsafe verification | before apply | Runtime attempt | Runtime |
| Outcome | feedback owner | execution/verification | learning/OMP | append-only | invalid verification | closure | Historical | Evidence |
| Learning Object | learning/trust owners | outcome closure | future decisions | learning owner | synthetic/unverified outcome | after verified outcome | Long-lived | Knowledge |

## Decision Identity

### Who creates it today

Current code creates `decision_id` in:

```text
admin_core/operator_execution_pipeline.py::_preview_packet_for_candidate
```

and separately mirrors it in:

```text
admin_core/operator_execution_pipeline.py::_outcome_closure_plan
```

The packet owner then preserves it when generating a packet from a preview:

```text
admin_core/operator_execution.py::packet_from_preview
```

### Who owns it

Canonical ownership:

```text
Decision Model + existing decision/read-model owners
```

Implementation ownership for current A4 path:

```text
admin_core/operator_execution_pipeline.py
```

Runtime/packet preservation ownership:

```text
admin_core/operator_execution.py
```

### Can it change?

Architecturally:

```text
NO after Decision Snapshot freeze.
```

Current implementation:

```text
YES before execution lease, because decision_id is regenerated as part of packet preview resolution.
```

After an execution lease is active, the model says decision regeneration is forbidden and lease state reports:

```text
decision_regeneration_allowed = false
planner_regeneration_allowed = false
selected_move_hash_regeneration_allowed = false
target_regeneration_allowed = false
```

### Who may change it?

Before freeze:

- decision/read-model owner;
- governed dry-run owner while preparing current preview.

After freeze:

- no runtime owner should change it;
- packet owner may only preserve or reject it;
- apply owner must consume it indirectly through approved plan lock and must not reselect.

## Decision Freeze

V7 already defines the concept semantically:

- Runtime Model: Runtime reads Decision Snapshot and does not decide.
- Runtime Model Execution Lease: while lease is active, Runtime and OMP must not regenerate the decision, selected move hash, target, or execution packet.
- Canonical Reference Decision Object Model: Decision Snapshot precedes Fresh Packet; Packet is transient runtime artifact.
- Execution Equivalence Audit: class/policy authority may later allow fresh packet generation inside an approved envelope, but current `GOVERNED_ONLY` exact-packet fallback cannot replace Packet A with Packet B.

Current gap:

```text
Decision Freeze exists after execution lease, but no independent pre-lease Decision Snapshot freeze exists between READY dry-run and lease creation.
```

What becomes immutable today after lease:

- packet id;
- decision id;
- operation id;
- authority generation;
- selected move hash;
- subject;
- target;
- rollback manifest;
- approved plan lock.

What is not independently frozen before lease:

- decision snapshot as a separate object;
- candidate/packet preview selected by the first dry-run command.

## Planner Analysis

Planner/autoswitch may run more than once in the current command flow:

1. First production dry-run builds the current candidate/packet preview.
2. Lease creation through `v7-governed-canary-dry-run-cycle --create-execution-lease` rebuilds current decision surface and packet preview before binding.
3. Apply owner `tools/v7-users-autoswitch` builds a plan again, but if approved plan lock is valid it replaces selected moves with the approved locked moves and reports `planner_recomputed_after_approval = false`.

Therefore:

- Lease owner itself does not need to recompute the decision.
- The governed dry-run lease-creation wrapper does recompute the current preview before it calls the packet owner.
- Apply may compute a planner plan for validation/readiness, but must consume approved locked selected moves when the lock is valid.

## Packet Analysis

Packet is not identical to Decision.

Canonical model:

```text
Decision Snapshot
  -> Packet / Preview
```

Current implementation issue:

```text
decision_id = hash(recommendation_id + packet_id)
```

That couples decision identity to packet identity. It makes packet changes look like decision changes, and it makes decision freeze impossible until packet preview is already selected.

Packet should remain:

```text
Fresh bounded execution artifact
```

Under current `GOVERNED_ONLY`, packet is also the temporary approval object. That is transitional and intentionally strict.

## Authority Analysis

Today the approved object is:

```text
Exact packet / exact operation / exact selected move
```

Reason:

```text
First action class remains GOVERNED_ONLY.
```

Target model already exists:

```text
Business Objective
  -> Canonical Policy
  -> Delegated Autonomy Policy
  -> Action-Class Authority
  -> Runtime Eligibility
  -> Fresh Packet
```

Packet approval is not permanent.

## Hypothesis Falsification

| Hypothesis | Verdict | Evidence |
| --- | --- | --- |
| H1: Decision changes illegally. | `PARTIAL` | Before lease, decision identity can change because it is regenerated with packet preview. This is legal in current implementation but misaligned with intended Decision Snapshot ordering. |
| H2: Planner is called twice. | `SUPPORTED` | Dry-run and lease-creation wrapper both rebuild current candidate/packet preview. |
| H3: Lease recomputes decision. | `FALSIFIED` | `admin_core/operator_execution.py::packet_from_preview` preserves preview identity. The wrapper before lease recomputes. |
| H4: Runtime recomputes planner. | `PARTIAL` | Apply owner computes a plan for validation, but consumes approved lock when valid. It should not reselect after lock. |
| H5: Packet is incorrectly treated as Decision. | `SUPPORTED` | `decision_id` is derived from `packet_id`; current approval surface treats packet as durable fallback authority. |
| H6: Decision Freeze exists but implementation ignores it. | `PARTIAL` | Lease freeze exists and is honored after lease; missing piece is pre-lease decision freeze. |
| H7: Decision Freeze does not exist. | `FALSIFIED` | Runtime Model and lease semantics define it. |
| H8: Current behavior exactly matches architecture. | `FALSIFIED` | Architecture orders Decision Snapshot before Packet; implementation derives decision_id from packet_id. |
| H9: Another root cause. | `SUPPORTED` | The concrete root is not lease recomputation but missing pre-lease frozen decision snapshot / preview handoff in the governed dry-run entrypoint. |

## Commercial Comparison

| System family | Immutable object between decision and execute |
| --- | --- |
| Cisco NSO | Service transaction / intended config diff / commit plan; device commands are execution artifacts. |
| Cisco Crosswork | Intent/policy workflow and validated change scope; concrete operations are artifacts. |
| Juniper Apstra | Intent and validated desired state; realization artifacts are regenerated under intent constraints. |
| Google SRE | Change intent, rollout/canary envelope, SLO/rollback gates; individual low-level actions are not the authority object. |
| AWS control planes | API request / policy-scoped intent / idempotency token; tasks may be scheduled/reconciled under constraints. |
| Cloudflare | API/policy/zone/account-scoped operation; runtime implementation is validated under policy. |
| Kubernetes | Desired state object + resourceVersion/UID; controller reconciles current execution, but validates generation and state before commit. |

Common production pattern:

```text
Freeze intent / desired state / decision envelope.
Generate execution artifacts under that frozen envelope.
Revalidate until commit.
After commit, verify, rollback, or recover; do not silently change the decision.
```

V7 architecture already matches this pattern. The current governed fallback implementation only partially matches because the decision identity is packet-coupled before freeze.

## Root Cause

Primary root cause:

```text
Decision Identity is currently generated inside packet preview and includes packet_id, so the governed lease-creation path can produce a different Decision Identity when it reruns dry-run before lease.
```

Ranked contributing causes:

1. No independent pre-lease Decision Snapshot freeze in current governed A4 path.
2. `v7-governed-canary-dry-run-cycle --create-execution-lease` rebuilds the current packet preview before lease binding instead of consuming the exact frozen preview from the immediately preceding dry-run.
3. `decision_id` is packet-coupled, so packet drift becomes decision drift.
4. Exact packet authority is still required because the first action class is `GOVERNED_ONLY`.

## Minimal Fix

Do not create a new owner, backlog item, decision object, planner, runtime path, or architecture.

Minimal implementation through existing owners:

1. Extend `admin_core/operator_execution_pipeline.py` / `tools/v7-governed-canary-dry-run-cycle` so the READY dry-run output can be consumed as the frozen Decision Snapshot / packet preview for immediate lease creation.
2. Ensure lease creation binds to the exact already-produced preview without re-running candidate/packet selection.
3. Keep `admin_core/operator_execution.py` as the packet/lease owner that preserves identity and fails closed on mismatch.
4. Later, under existing A6/B18 work, decouple `decision_id` from `packet_id` so Decision Identity derives from semantic decision inputs, not the packet artifact.

Existing owner:

```text
admin_core/operator_execution_pipeline.py
admin_core/operator_execution.py
tools/v7-governed-canary-dry-run-cycle
```

Existing backlog:

```text
A4 current blocker, with B18 as the broader owner-issued version/lease pattern follow-up.
```

No new backlog item is required.

## Capability Impact

- A4 remains blocked until a real governed outcome can complete without stale packet/decision drift.
- A5, B13, A6 remain downstream.
- Runtime automation remains disabled.
- Authority remains unchanged.
- Production Maturity unchanged.

## Validation

Need New Owner: `FALSE`
Need New Backlog: `FALSE`
Need New Runtime Path: `FALSE`
Need New Decision Object: `FALSE`
Need New Architecture: `FALSE`

## Next Step

Continue OMP from A4. The next safe implementation step is not a new design; it is an existing-owner fix:

```text
A4_FIX_PRE_LEASE_DECISION_SNAPSHOT_FREEZE_IN_EXISTING_GOVERNED_DRY_RUN_OWNER
```

Expected completion evidence:

- fresh READY dry-run produces one decision/packet preview;
- immediate lease creation consumes that exact preview;
- no second packet/decision is generated before lease;
- lease preserves packet_id, operation_id, decision_id, selected_move_hash, subject, target, and authority_generation;
- apply still consumes approved plan lock and fails closed on material mismatch;
- tests prove no user movement during preparation and no synthetic evidence.

## Re-audit Rule

Do not re-audit Decision Ownership unless:

- Decision Model ownership changes;
- governed dry-run / packet / lease owner changes materially;
- A6 introduces class/policy authority execution equivalence;
- production evidence disproves this lifecycle;
- operator explicitly requests re-audit.
