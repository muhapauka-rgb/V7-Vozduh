# Engineering Report: Decision Commit Point Behavior Contract Audit

## Summary

Проведен Phase 0.5 pre-implementation behavior contract audit для будущего Decision Commit Point.

Код, Runtime, OMP и Backlog не изменялись.

Итог:

`BEHAVIOR_CONTRACT_COMPLETE`

Контракт можно определить через существующие владельцы:

- Product Specification;
- Runtime Model;
- Decision Model;
- OMP;
- Canonical Reference;
- existing packet / lease / apply owners.

Новый owner, backlog item или архитектура не требуются.

## Action Performed

- Выполнен semantic reuse audit существующих canonical contracts.
- Проверены текущие owners:
  - `admin_core/operator_execution_pipeline.py`;
  - `admin_core/operator_execution.py`;
  - `tools/v7-governed-canary-dry-run-cycle`;
  - `tools/v7-users-autoswitch`.
- Сопоставлены результаты:
  - Master Decision Ownership Audit;
  - Master Implementation Justification Audit;
  - Decision Commit Point Phase 0 Safety Audit;
  - Execution Equivalence Audit;
  - Governed Exit Audit;
  - Packet Approval Exit Audit.

## Contract Principle

Future implementation must satisfy one permanent behavioral rule:

```text
Commit the Decision before creating or leasing the execution Packet,
but keep runtime safety validation live until the irreversible commit point.
```

This means:

```text
Decision Commit
  -> Packet Preview / Packet
  -> Operator approval or approved authority envelope
  -> Execution Lease
  -> Live Validation
  -> Restore Barrier
  -> Apply
  -> Verify
  -> Rollback or Outcome
  -> Learning
```

The fix must not convert the Decision Commit into permission to execute.

Decision Commit means:

```text
This is the selected decision identity and semantic move.
```

It does not mean:

```text
Runtime may ignore freshness, authority, rollback, target eligibility, anti-flap, or verification.
```

## Decision Behavior Contract

| Field | Contract |
| --- | --- |
| Current behavior | Decision identity is materialized inside packet preview and can change when packet preview changes before lease. |
| Target behavior | Decision becomes valid when the governed decision surface selects one candidate and all pre-authority decision gates required for READY preview pass. |
| Validity condition | Decision must include subject, source, target, action class, authority tier/generation, selected move hash, rollback/no-rollback expectation, verification requirement, and source/snapshot generation references. |
| Commit point | Decision becomes committed before packet materialization / lease creation. |
| Immutability | After Decision Commit, decision id, selected move hash, subject, source, target, action class, authority generation, rollback target and verification requirement must not silently change. |
| Allowed after commit | Freshness recheck, health recheck, target/source eligibility check, authority generation check, rollback readiness check, verification readiness check, anti-flap/movement protection check, material state change check. |
| Forbidden after commit | Reranking candidates, changing selected user, changing target, changing selected move hash, changing decision id, silently replacing decision with another decision, treating a different packet as approved under exact packet fallback. |
| Safety requirement | If any live validation materially contradicts the committed decision, Runtime must stop safely before mutation. |
| Architecture requirement | Runtime consumes Decision Snapshot; Runtime does not invent or rerank decisions. |

Decision is correct only if:

```text
same semantic decision -> same committed decision identity
different user/source/target/action class/authority/selected move -> different or invalidated decision
```

## Packet Behavior Contract

| Field | Contract |
| --- | --- |
| Purpose | Packet is a bounded execution artifact derived from a committed decision. |
| Lifetime | Transient. It is live only for the current approval/lease/execution window and historical after outcome closure. |
| Ownership | Existing execution packet owner: `admin_core/operator_execution.py`; preview assembly remains in `admin_core/operator_execution_pipeline.py`. |
| Current behavior | Packet preview creates packet id, operation id, decision id and selected move hash together. |
| Target behavior | Packet must preserve the committed decision identity and add only packet/execution metadata. |
| Regeneration rule under `GOVERNED_ONLY` | Packet must not be replaced after exact packet approval. A different packet requires stop / new approval. |
| Regeneration rule under future class/policy authority | Packet may be fresh/regenerated only if it remains inside approved class/policy/authority envelope and all live gates pass. This is not enabled by this contract. |
| Invalidation rule | Packet invalidates on packet identity mismatch, decision mismatch, selected move hash mismatch, subject/source/target mismatch, authority generation mismatch, rollback/verification mismatch, material state change, expiry, or failed safety gate. |
| Safety requirement | A packet is never durable authority. It is executable only when authority and live validation agree. |

Packet must not:

- create a new decision identity after decision commit;
- hide a decision change inside execution metadata;
- be used as long-term product approval object;
- bypass exact approval while the class remains `GOVERNED_ONLY`.

## Lease Behavior Contract

| Field | Contract |
| --- | --- |
| Purpose | Bind current authority/approval to one immutable execution packet while active. |
| Input | A packet derived from a committed decision, plus approved identity / authority envelope. |
| Output | Active execution lease with immutable packet identity, material state, source hashes, expiry and fail-closed semantics. |
| Current behavior | Lease correctly freezes packet identity after creation, but the CLI can rebuild preview before creating lease. |
| Target behavior | Lease consumes the committed decision-derived packet/preview; it must not cause or require decision regeneration. |
| Must consume | Committed decision identity, packet identity, operation id, selected move hash, subject, source, target, authority generation, rollback manifest, verification requirement, material state. |
| Must not consume | A freshly reranked planner decision that silently differs from the committed decision. |
| Active lease rule | While active: decision regeneration, selected move hash regeneration, target regeneration and packet regeneration are forbidden. |
| Invalidation | Timeout, execution finished, rollback finished, operator cancel, or material source/state change. |

Lease creation must fail closed if:

- committed decision is missing;
- packet cannot be derived from the committed decision;
- packet identity differs from approved identity under `GOVERNED_ONLY`;
- materialized packet changes decision / operation / selected move / subject / target / authority;
- rollback or verification prerequisites are absent.

## Live Validation Contract

These checks must always remain live after Decision Commit and before irreversible apply:

| Check | Required behavior |
| --- | --- |
| Freshness | Stop if decision inputs are stale beyond certified freshness rules or materially changed. |
| Health | Recheck source/destination health and service availability. |
| Target eligibility | Stop if destination becomes disabled, missing, unhealthy or policy-ineligible. |
| Source eligibility | Stop if subject/source state no longer matches the committed decision. |
| Authority generation | Stop if authority generation changed or no longer permits the operation. |
| Action-class state | Stop if action class is not allowed under current authority model. |
| Blast radius | Stop if selected action exceeds certified/user budget. |
| Rollback readiness | Stop if rollback target/manifest is missing, changed, unsafe, or no-rollback is not certified. |
| Verification readiness | Stop if verification plan cannot run immediately after apply. |
| Anti-flap | Stop if movement violates cooldown/freeze/pair reversal/anti-flap constraints. |
| Movement protection | Stop if net benefit no longer exceeds state change cost when required by current capability. |
| Failure family | Stop if current failure family no longer matches the decision premise. |
| Recovery family | Stop if recovery admission changes the safe action classification. |
| Approved plan lock | Stop if lock is missing, expired, mismatched, missing selected moves, or has material snapshot/source change. |
| Duplicate work | Stop if operation already executed or active lease exists. |
| Loop guard | Stop if retry would repeat an unresolved loop without material new evidence. |

Live validation may block execution.

Live validation may not silently rewrite the committed decision.

## Immutable Contract

After Decision Commit, the following must remain immutable unless the system stops and creates a new decision:

- `decision_id`;
- action class;
- subject/user or approved subject scope;
- source channel;
- target channel;
- selected move hash;
- authority tier;
- authority generation;
- rollback target / no-rollback classification;
- verification requirement;
- blast radius unit and budget;
- committed decision source/snapshot references;
- packet identity after packet materialization;
- operation id after operation materialization;
- approved plan lock after restore-barrier clearance;
- execution lease immutable packet identity after lease creation.

Mutable only as live validation evidence:

- freshness timestamp;
- non-material source hashes;
- service/health observations;
- verification readiness observation;
- runtime diagnostics;
- report/learning metadata after outcome.

## Compatibility Contract

Future implementation must preserve these existing behaviors:

| Existing behavior | Must remain unchanged |
| --- | --- |
| Fail-closed | Any missing/mismatched identity or unsafe gate stops before mutation. |
| Exact `GOVERNED_ONLY` packet approval | Still required until action-class authority is certified and approved. |
| Packet identity preservation | Preview -> packet -> lease preserves packet id, operation id, decision id, authority generation, selected move hash. |
| Approved plan lock | Apply consumes approved selected moves and does not reselect. |
| Material state gate | Non-material drift may keep lease; material change invalidates lease. |
| Rollback | Rollback manifest/source operation/selected move hash remain bound. |
| Verification | Verification remains mandatory and immediate after apply. |
| Learning lineage | Outcome/learning stores stable decision/packet/operation references. |
| Historical compatibility | Existing old packet-coupled records remain readable and auditable. |
| Runtime automation | No runtime automation is enabled by the commit point fix. |
| Authority | No authority expansion occurs as a side effect. |

## Negative Contract

The implementation must never allow:

- planner reruns to replace a committed decision;
- packet regeneration to change `decision_id` under exact `GOVERNED_ONLY` approval;
- Decision Commit to bypass operator approval;
- Decision Commit to bypass class/policy authority;
- Runtime to execute a packet that does not match committed decision and authority;
- Runtime to execute a packet with changed user/source/target/hash/authority;
- apply owner to recompute and use a different selected move;
- rollback manifest identity to change after approval/lease;
- verification requirement to be dropped after commit;
- stale packet to be treated as fresh;
- synthetic evidence to certify decision safety;
- old packet/lease records to be reinterpreted destructively;
- live validation to mutate decision instead of stopping.

## Test Contract

Future tests must prove the following groups.

### Decision

- A READY governed decision receives a stable committed `decision_id` before packet/lease.
- Same semantic decision preserves committed `decision_id`.
- Different subject/source/target/action class/authority/selected move invalidates or creates a new decision.
- Decision Commit does not perform runtime mutation.
- Decision Commit does not imply execution permission.

### Packet

- Packet derives from committed decision.
- Packet preserves committed `decision_id`.
- Packet adds execution metadata only.
- Under `GOVERNED_ONLY`, a changed packet cannot reuse old approval.
- Packet-independent `decision_id` remains compatible with packet validation.

### Lease

- Lease creation consumes committed decision-derived packet/preview.
- Lease creation does not rerank or regenerate decision.
- Lease immutable identity equals packet identity.
- Active lease blocks decision/target/selected hash regeneration.
- Material state change invalidates lease; freshness-only drift does not.

### Apply

- Apply consumes approved plan lock.
- Apply does not reselect when approved lock exists.
- Apply fails closed when lock missing, expired, mismatched, or unsafe.
- Apply cannot move any user outside committed subject/scope.
- Apply cannot target any channel outside committed target/scope.

### Rollback

- Rollback manifest remains bound to source operation and selected move hash.
- Rollback target cannot silently change after commit.
- Missing rollback or uncertified no-rollback stops before apply.

### Verification

- Verification plan exists before apply.
- Verification executes immediately after apply.
- Inconclusive verification triggers stop/rollback policy.

### Learning

- Learning records only real observed outcomes.
- Learning preserves decision/packet/operation lineage.
- Learning does not certify trust from approval or packet existence alone.

### Backward Compatibility

- Old packet-coupled `decision_id` records still validate/read as historical.
- Old leases remain fail-closed or valid according to existing immutable identity rules.
- Old reports/outcomes remain readable.

### Regression

- Existing `GOVERNED_ONLY` exact packet approval remains strict.
- Runtime automation remains disabled.
- Authority expansion remains impossible without explicit approval.
- No user movement happens during dry-run, packet generation, decision commit, or lease creation alone.

## Success Contract

Implementation is correct only if all are true:

1. Decision commits before packet/lease.
2. Packet preserves decision identity.
3. Lease consumes committed packet/preview and freezes it.
4. Live validation remains active until apply.
5. Any material mismatch stops safely.
6. Exact `GOVERNED_ONLY` fallback stays strict.
7. Historical packets/leases/reports remain readable.
8. Rollback, verification, outcome and learning lineage remain intact.
9. No new owner, runtime path, planner, governance layer, truth source, backlog item or architecture is introduced.
10. Tests prove both old and new identity behavior.

## Existing Owner Mapping

| Contract area | Existing owner |
| --- | --- |
| Product meaning / packet not long-term authority | `docs/product/V7_PRODUCT_SPECIFICATION.md` |
| Decision semantics | `docs/reference/V7_DECISION_MODEL.md` |
| Runtime lifecycle | `docs/reference/V7_RUNTIME_MODEL.md` |
| Canonical object hierarchy | `docs/reference/V7_CANONICAL_REFERENCE.md` |
| OMP execution discipline and `GOVERNED_ONLY` | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` |
| Packet preview / governed decision surface | `admin_core/operator_execution_pipeline.py` |
| Packet / lease / approved lock | `admin_core/operator_execution.py` |
| Governed dry-run CLI | `tools/v7-governed-canary-dry-run-cycle` |
| Runtime apply / restore barrier / approved plan lock consumption | `tools/v7-users-autoswitch` |
| Current state | `docs/programs/V7_CURRENT_PROGRAM_STATE.md` |
| Owner map | `docs/reference/SYSTEM_MAP.md` |

Need New Owner:

`FALSE`

Need New Backlog:

`FALSE`

Need New Architecture:

`FALSE`

## Canonical Updates

No canonical files were updated.

Reason:

The durable rules already exist in Runtime Model, Decision Model, Canonical Reference, OMP and Product Specification. This report assembles them into a pre-implementation behavior contract for A4/B18 execution.

## Next Step

Continue OMP through existing A4/B18.

Implementation may begin only by extending existing owners and adding the tests required by this contract.

## Re-audit Rule

Do not repeat this contract audit unless:

- Decision Model semantics change;
- Runtime Model lifecycle changes;
- packet/lease schema changes materially;
- `GOVERNED_ONLY` authority semantics change;
- approved plan lock/apply behavior changes materially;
- production evidence disproves this contract;
- explicit operator request.

## Final Verdict

`BEHAVIOR_CONTRACT_COMPLETE`
