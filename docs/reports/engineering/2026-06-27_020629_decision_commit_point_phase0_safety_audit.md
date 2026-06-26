# Engineering Report: Decision Commit Point Phase 0 Safety Audit

## Summary

Проведен Phase 0 audit перед возможным изменением Decision Commit Point.

Код, Runtime, OMP, Backlog и формулы не изменялись.

Итоговое решение:

`SAFE_AFTER_SMALL_PREPARATION`

Pre-Lease Decision Commit Point соответствует канонической архитектуре V7, потому что Runtime Model и Canonical Reference уже требуют порядок:

```text
Decision Snapshot
  -> Fresh Packet
```

Но менять реализацию сразу небезопасно без небольшой подготовки тестов и правил обратной совместимости, потому что текущие packet / lease / rollback / verification consumers уже ожидают сохранение `packet_id`, `operation_id`, `decision_id` и `selected_move_hash` в существующем формате.

## Action Performed

- Выполнен semantic reuse audit по существующим canonical owners.
- Просмотрены владельцы реализации:
  - `admin_core/operator_execution_pipeline.py`
  - `admin_core/operator_execution.py`
  - `tools/v7-governed-canary-dry-run-cycle`
  - `tools/v7-users-autoswitch`
- Просмотрены существующие тесты:
  - `tests/unit/test_operator_execution_packet.py`
  - `tests/unit/test_operator_execution_pipeline.py`
  - `tests/unit/test_v7_users_autoswitch_policy.py`
- Выполнен code search по:
  - `decision_id`
  - `packet_id`
  - `operation_id`
  - `selected_move_hash`
  - `execution lease`
  - `approved_plan_lock`
  - `packet_preview`

## Objective Observations

Canonical model already supports a pre-lease commit point:

```text
Decision Snapshot
  -> Packet / Preview
  -> Approval
  -> Execution Lease
  -> Restore Barrier
  -> Apply
```

Current implementation partially implements this after lease:

- execution lease stores immutable packet identity;
- lease sets `decision_regeneration_allowed = false`;
- lease sets `selected_move_hash_regeneration_allowed = false`;
- lease sets `target_regeneration_allowed = false`;
- `tools/v7-users-autoswitch` consumes approved plan lock and fails closed on mismatch.

Current missing piece is before lease:

`tools/v7-governed-canary-dry-run-cycle --create-execution-lease` rebuilds the current governed cycle before binding approval, and current preview generation derives `decision_id` from `packet_id`.

## Existing Implementation Invariants

| Invariant | Current owner | Safety role |
| --- | --- | --- |
| Packet preview must have `packet_id`, `operation_id`, `decision_id`, `authority_generation`, `selected_move_hash`. | `admin_core/operator_execution.py::packet_from_preview` | Prevent incomplete execution artifact. |
| Materialized packet preserves preview `packet_id`, `operation_id`, `decision_id`, `selected_move_hash`. | `packet_from_preview` | Prevent approval-to-execution identity drift. |
| Execution lease stores `immutable_packet_identity`. | `build_execution_lease` | Prevent packet mutation after lease. |
| Execution lease invalidates on packet identity/hash change. | `execution_lease_state` | Fail closed if approved packet changes. |
| Material state gate ignores non-material freshness drift but invalidates material changes. | `material_state_change_gate` | Avoid repeated approvals on non-material changes while preserving safety. |
| Approved plan lock must match packet identity and selected move hash. | `approved_plan_lock_from_selected`, `_approved_plan_lock_validation` | Ensure apply consumes approved move. |
| Restore barrier clearance must match selected move hash and operation context. | `tools/v7-users-autoswitch` | Prevent unapproved mutation. |
| Rollback manifest binds source operation and selected move hash. | `packet_from_preview`, `tools/v7-users-autoswitch` | Preserve rollback correctness. |
| Verification/outcome/learning use operation and packet references. | `operator_execution_feedback`, observability/read models | Preserve auditability and learning lineage. |

No invariant requires:

```text
decision_id == packet_id
```

But existing implementation and tests assume:

```text
packet.decision_id == preview.decision_id
packet.expected.decision_id == preview.decision_id
approved_plan_lock.decision_id == preview.decision_id
lease.immutable_packet_identity.decision_id == packet.decision_id
```

Therefore decoupling `decision_id` from `packet_id` is safe only if the preview still carries a stable `decision_id` and all downstream packet/lease fields preserve it.

## Existing Consumers Of decision_id

| Consumer | Purpose | Breakage if commit point changes? |
| --- | --- | --- |
| `admin_core/operator_execution_pipeline.py` | Creates preview `decision_id` and lifecycle decision references. | `YES` if it changes format without preserving field. |
| `admin_core/operator_execution.py` | Validates preview, materializes packet, stores lock/lease identity. | `NO` if `decision_id` remains present and stable. |
| `tools/v7-governed-canary-dry-run-cycle` | Compares approved identity before lease. | `YES` if approved args use old identity and new preview regenerates different identity. |
| `admin_core/operator_execution_feedback.py` | Stores outcome / learning references. | `NO` if field remains stable. |
| `admin_core/shadow_autonomy.py` | Tracks shadow decision history/comparisons. | `NO` for governed packet path if shadow ids untouched. |
| `admin_core/autonomy_trust_acceleration.py` | Evidence / trust inventory references. | `NO` if old records remain readable. |
| Tests | Assert identity preservation preview -> packet -> lock -> lease. | `PARTIAL`; tests need extension, not wholesale removal. |

## Existing Consumers Of packet_id

| Consumer | Purpose | Breakage if commit point changes? |
| --- | --- | --- |
| `admin_core/operator_execution.py` | Packet identity, approval id, lock id, rollback id fallback, lease identity. | `NO` if packet id remains stable after preview. |
| `tools/v7-governed-canary-dry-run-cycle` | Exact packet binding for `GOVERNED_ONLY`. | `NO` if exact fallback remains. |
| `tools/v7-users-autoswitch` | Restore barrier / approved plan lock diagnostics and validation. | `NO` if lock schema unchanged. |
| `operator_execution_feedback.py` | Outcome references. | `NO` if old packet ids retained. |
| `intelligence_platform.py`, workers/read models | Historical references. | `NO` if backward readable. |
| Tests | Exact identity preservation and stale packet rejection. | `PARTIAL`; add tests for stable decision + regenerated packet semantics before lease. |

## Existing Consumers Of operation_id

| Consumer | Purpose | Breakage if commit point changes? |
| --- | --- | --- |
| `operator_execution.py` | Packet, rollback manifest, restore clearance source operation. | `NO` if operation id remains stable inside packet. |
| `tools/v7-users-autoswitch` | Runtime operation context, rollback source operation, audit object ids. | `NO` if operation id remains per execution operation. |
| `operator_observability.py`, `operator_views.py` | Operation detail and audit export lookup. | `NO` if historical ids remain readable. |
| `intelligence_platform.py`, workers | Read-model summaries. | `NO` if records preserve operation id. |
| Tests | Operation id in packet, lifecycle, rollback, audit records. | `NO` if operation id contract unchanged. |

## Existing Consumers Of selected_move_hash

| Consumer | Purpose | Breakage if commit point changes? |
| --- | --- | --- |
| `operator_execution_pipeline.py` | Packet preview semantic selected move identity. | `NO` if hash remains derived from user/source/target. |
| `operator_execution.py` | Expected move hash, lock hash, lease identity, material state. | `NO` if unchanged. |
| `tools/v7-governed-canary-dry-run-cycle` | Approved identity binding. | `NO` if same selected move remains same hash. |
| `tools/v7-users-autoswitch` | Restore barrier, approved plan lock, atomic envelope, rollback verification. | `YES` if changed without preserving approved identity. |
| Tests | Many apply/rollback/lock tests. | `NO` if hash semantics unchanged. |

## Backward Compatibility Analysis

| Capability | Compatibility result | Notes |
| --- | --- | --- |
| Existing packets | `SAFE_WITH_COMPATIBILITY` | Keep consuming old packet schema where `decision_id` was packet-coupled. |
| Existing leases | `SAFE_WITH_COMPATIBILITY` | Lease validation compares stored packet identity; do not reinterpret existing lease ids. |
| Existing rollback manifests | `SAFE` | Rollback binds `source_operation_id` and `selected_move_hash`, not `decision_id == packet_id`. |
| Existing verification | `SAFE` | Verification follows operation/packet references and outcome records. |
| Existing learning | `SAFE_WITH_COMPATIBILITY` | Keep old `decision_id` as historical lineage; new ids must remain stable. |
| Existing reports | `SAFE` | Reports are evidence and should remain readable. |
| Runtime fail-closed | `SAFE` | Existing packet/lock/lease gates remain fail-closed if identity is missing or mismatched. |

## Breakage Analysis

| Dependency | Will break? | Why |
| --- | --- | --- |
| Packet materialization from preview | `NO` | It preserves any supplied `decision_id`; it does not require `decision_id` to derive from `packet_id`. |
| Lease from packet | `NO` | It freezes the packet identity it receives. |
| Approved identity binding | `PARTIAL` | It will reject old approvals if a new commit point changes ids between approval and lease; must keep exact approved identity stable. |
| Apply owner | `NO` | It consumes approved plan lock and selected move hash. |
| Restore barrier | `NO` | It keys safety on packet/operation/selected hash and generation. |
| Rollback | `NO` | It uses operation id and selected move hash. |
| Outcome learning | `NO` | It can consume stable decision ids; old records remain historical. |
| Tests expecting packet-coupled changed packet prompt | `PARTIAL` | Some tests should remain for material packet changes; add tests for stable decision commit when semantic decision is unchanged. |

## Existing Test Coverage

Already covered:

- packet from preview preserves semantic identity;
- packet from full governed cycle extracts preview identity;
- execution lease from approved packet uses same packet id;
- execution lease from packet never regenerates packet;
- changed preview identity is rejected;
- create lease requires matching approved identity;
- apply consumes identical packet from execution lease;
- freshness-only change preserves lease;
- regenerated packet with identical semantic plan does not invalidate active lease;
- target / rollback / policy / authority / selected hash changes invalidate lease;
- approved plan lock valid path is consumed by apply;
- approved plan lock selected hash mismatch fails closed;
- changed user/source/target scope fails closed;
- expired lock fails closed.

Coverage gap:

- no test yet proving a pre-lease Decision Commit Point can freeze a stable decision before packet materialization;
- no test yet proving `decision_id` can be packet-independent while packet/lease/apply still preserve identity;
- no test yet proving old packet-coupled records remain readable;
- no CLI-level test proving `--create-execution-lease` consumes the committed decision/preview instead of rebuilding a different one;
- no test proving exact `GOVERNED_ONLY` packet fallback remains strict after introducing pre-lease commit.

## Root Risks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Breaking exact packet approval fallback. | Medium | High | Preserve packet identity binding and add CLI-level regression test. |
| Breaking old packet/lease records. | Medium | Medium | Backward-compatible reader: accept old packet-coupled `decision_id` as historical. |
| Accidentally allowing packet replacement under `GOVERNED_ONLY`. | Low/Medium | High | Keep approved binding over packet, operation, decision, selected hash, subject, target, authority generation. |
| Confusing Decision Snapshot identity with execution operation identity. | Medium | Medium | Keep separate names and tests for decision id vs operation id. |
| Weakening apply fail-closed behavior. | Low | High | Do not change `tools/v7-users-autoswitch` lock validation except tests if needed. |
| Test suite masking old behavior. | Medium | Medium | Add explicit tests for old and new identity modes. |

## Final Safety Decision

`SAFE_AFTER_SMALL_PREPARATION`

The existing implementation may safely introduce a Pre-Lease Decision Commit Point only after these preparations:

1. Add tests for packet-independent stable `decision_id`.
2. Add backward-compatibility tests for old packet-coupled previews/packets/leases.
3. Add CLI-level test proving lease creation consumes the committed preview/decision and does not rebuild a different identity.
4. Add regression test that exact `GOVERNED_ONLY` approval still rejects any changed packet/user/target/selected move/authority.
5. Keep all existing fail-closed gates active.

## Existing Owner

Primary owners:

- `admin_core/operator_execution_pipeline.py`
- `tools/v7-governed-canary-dry-run-cycle`
- `admin_core/operator_execution.py`

Safety/apply owner:

- `tools/v7-users-autoswitch`

Canonical owners:

- Runtime Model
- Decision Model
- OMP
- Canonical Reference

Need New Owner:

`FALSE`

## Existing Backlog Owner

Primary:

`A4`

Secondary / generalized:

`B18`

Need New Backlog:

`FALSE`

## Canonical Knowledge

No canonical owner update required.

The durable rule already exists:

```text
Decision Snapshot
  -> Fresh Packet
```

This report only confirms safety conditions before implementation.

## Next Step

Continue OMP through existing A4/B18.

Before implementation, write the missing tests listed above.

Do not change Runtime behavior until tests prove:

- old packet-coupled records still work;
- new pre-lease decision commit does not weaken exact governed packet authority;
- apply continues to fail closed on any identity or safety mismatch.

## Re-audit Rule

Do not repeat this Phase 0 audit unless:

- packet/lease identity schema changes materially;
- `tools/v7-governed-canary-dry-run-cycle` changes materially;
- `admin_core/operator_execution.py` packet/lease semantics change materially;
- `tools/v7-users-autoswitch` approved lock semantics change materially;
- production evidence disproves this safety decision;
- explicit operator request.

## Final Verdict

`SAFE_AFTER_SMALL_PREPARATION`
