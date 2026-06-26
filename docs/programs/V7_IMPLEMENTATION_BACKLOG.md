# V7 Implementation Backlog

Status: ACTIVE
Owner: OMP
Source: Canonical Policy Library Stage 4 V7 Fit Analysis
Need New Owner: FALSE

## Purpose

This backlog is the permanent OMP implementation queue derived from the Canonical Policy Library.

It transforms policy fit analysis into implementation work without creating a new roadmap, planner, governance layer, execution path, runtime owner, truth source, authority expansion, runtime apply, or user movement.

OMP must always choose the highest-priority unfinished backlog item unless it crosses:

- `OPERATIONAL_AUTHORITY`;
- `ENGINEERING_AUTHORITY`;
- `REAL_WORLD_LIMIT`;
- `UNSAFE_IMPLEMENTATION`;
- `FUNDAMENTAL_ARCHITECTURE_GAP`.

## Backlog Rules

1. The backlog is sorted by production leverage, not document order.
2. Every item must reuse an existing owner.
3. Every item starts as `TODO`, becomes `IN_PROGRESS` only during implementation, and becomes `DONE` only after tests, verification, truth, convergence, and required certification.
4. After every completion, OMP must recalculate the backlog using `docs/reference/V7_IMPLEMENTATION_PRIORITY_MODEL.md`.
5. If an item requires exact production action approval, OMP stops at `OPERATIONAL_AUTHORITY`.
6. If an item requires authority expansion, new action class approval, new runtime capability, new autonomous policy, or blast-radius expansion, OMP prepares a recommendation and stops at `ENGINEERING_AUTHORITY`.
7. If implementation evidence proves architecture is insufficient, OMP stops at `FUNDAMENTAL_ARCHITECTURE_GAP`.
8. Documentation-only work is not selected over implementation unless it is the direct implementation blocker.
9. This backlog is the only live engineering queue in V7.
10. Policy documents, reports, ADRs, architecture documents, research documents, product documents, and chat history must not generate implementation work directly.

## Backlog Progress

| Scope | Complete | Total | Status |
| --- | ---: | ---: | --- |
| Tier A | `3` | `6` | `ACTIVE` |
| Tier B | `0` | `21` | `PENDING` |
| Tier C | `0` | `7` | `PENDING` |
| Tier D optional | `0` | `6` | `OPTIONAL` |
| Overall actionable | `3` | `34` | `ACTIVE` |

Implementation maturity:

```text
8.8%
```

Estimated remaining effort:

```text
Moderate
```

Next item:

```text
A4
```

If all actionable backlog items are `DONE`, OMP must answer:

```text
IMPLEMENTATION_COMPLETE
```

and stop.

## Backlog Consistency Audit

Status: `CANONICAL_BACKLOG_MAPPING_CURRENT`

This section records the current mapping from confirmed remaining engineering gaps to the single live implementation queue. It is not a second backlog.

| Confirmed gap / model | Existing owner | Existing backlog item | Existing implementation / canonical knowledge | Decision |
| --- | --- | --- | --- | --- |
| Centralized Policy Arbitration | OMP, Runtime Model, delegated policy preview, action-class runtime enablement | `A6` | Runtime eligibility arbitration across freshness, authority, blast radius, rollback, anti-flap, verification, and learning gates. Narrow supporting items `B19` and `B20` remain sub-policy extensions, not duplicate owners. | `EXTEND_EXISTING` |
| Per-user `AUTO` / `PINNED` / `MANUAL` routing mode | User registry, group/organization policy, planner gates, admin UI | `B21` | Current assignment, group preference, and `manual_only`/`reserve_only` flags exist, but explicit per-user routing control mode is missing. | `ADD_TO_BACKLOG` |
| Runtime-certified Slow-Start Recovery | Recovery admission, blast-radius/action-class ladder | `B10` | Recovery admission and limited recovery blast radius exist; runtime-certified staged re-entry remains unfinished. | `EXTEND_EXISTING` |
| Pool Max-Ejection / Minimum-Health semantics | Planner capacity/load, action-class ladder, blast-radius bounds | `C7` | Capacity/load and authority budgets exist; proxy-style max-ejection/minimum-health mapping remains unfinished. | `EXTEND_EXISTING` |
| State Change Cost Model | Planner/autoswitch, movement protection model, anti-flap owners | `B19` | Already exists semantically as sticky/current-channel bonus, minimum improvement threshold, cooldown, freeze, pair reversal, target block, egress quarantine, rebalance restraint, and authority/blast caps. B19 owns vocabulary consolidation only. | `EXTEND_EXISTING` |

Need New Owner: `FALSE`.

Need New Document: `FALSE`.

State Change Cost verdict: `ALREADY_EXISTS_SEMANTICALLY`; extend existing B19 vocabulary only, do not create a new owner or new backlog item.

## Current Highest Priority

| Field | Value |
| --- | --- |
| Backlog id | `A4` |
| Task | Materialize representative outcome evidence for the first action class. |
| Policy source | `POLICY_005_ACTION_CLASS_PROMOTION` |
| Owner | OMP promotion engine, feedback/learning, outcome leverage model |
| Files/modules | `admin_core/operator_execution_feedback.py`, `admin_core/autonomy_trust_acceleration.py`, `tools/v7-autonomy-trust-evidence-inventory` |
| Implementation class | `IMPLEMENT_BACKGROUND` |
| Estimated effort | `MODERATE_EXTENSION` |
| Dependencies | Real comparable outcomes, no synthetic evidence. |
| Expected production value | `VERY_HIGH` |
| Expected autonomy gain | `VERY_HIGH` |
| Expected runtime gain | `HIGH` |
| Expected safety gain | `VERY_HIGH` |

## Tier A: Highest Production Leverage

| Id | Status | Task | Policy source | Owner | Files/modules | Implementation class | Estimated effort | Dependencies | Expected production value | Expected autonomy gain | Expected runtime gain | Expected safety gain |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `A1` | `DONE` | Bind canonical hard-failure classification to existing liveness/event evidence. | `POLICY_001_HARD_FAILURE` | Event sources, service matrix, quality compact, planner/autoswitch | `tools/v7-users-autoswitch`, `tools/v7-service-matrix-refresh-all`, `tools/v7-egress-quality-compact`, `admin_core/operator_decision_surface.py`, `admin_core/autonomy_trust_acceleration.py` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | Existing liveness, service, route, runtime evidence. | `VERY_HIGH` | `HIGH` | `HIGH` | `VERY_HIGH` |
| `A2` | `DONE` | Canonicalize per-action-class freshness windows and owner-issued freshness fields. | `POLICY_008_FRESHNESS`, `POLICY_001_HARD_FAILURE`, `POLICY_003_RECOVERY_ADMISSION` | Freshness actionability, delegated policy preview, execution lease | `admin_core/autonomy_trust_acceleration.py`, `admin_core/operator_execution.py`, `tools/v7-autonomy-trust-evidence-inventory` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | Existing freshness classifications, packet lease, runtime fingerprints. | `VERY_HIGH` | `HIGH` | `VERY_HIGH` | `VERY_HIGH` |
| `A3` | `DONE` | Certify class-level rollback/no-rollback evidence for governed candidate movement. | `POLICY_007_ROLLBACK`, `POLICY_005_ACTION_CLASS_PROMOTION` | Restore barrier, rollback manifest, governed execution, feedback/learning | `admin_core/operator_execution.py`, `tools/v7-users-autoswitch`, `admin_core/operator_execution_feedback.py`, `admin_core/autonomy_trust_acceleration.py` | `IMPLEMENT_CERTIFICATION` | `MODERATE_EXTENSION` | Real governed no-rollback outcome closed for packet `pkt_preview_5c4bcfaa59d769ced6d6e5dc`; feedback `execfb_55e330784ad36b513d23e12a`; learning `learn_0c3b5cdd250c64ac7d9b97e7`. | `VERY_HIGH` | `VERY_HIGH` | `HIGH` | `VERY_HIGH` |
| `A4` | `TODO` | Materialize representative outcome evidence for the first action class. | `POLICY_005_ACTION_CLASS_PROMOTION` | OMP promotion engine, feedback/learning, outcome leverage model | `admin_core/operator_execution_feedback.py`, `admin_core/autonomy_trust_acceleration.py`, `tools/v7-autonomy-trust-evidence-inventory` | `IMPLEMENT_BACKGROUND` | `MODERATE_EXTENSION` | Real comparable outcomes, no synthetic evidence. | `VERY_HIGH` | `VERY_HIGH` | `MEDIUM_HIGH` | `HIGH` |
| `A5` | `TODO` | Certify class-level blast-radius evidence beyond the one-user guard. | `POLICY_006_BLAST_RADIUS`, `POLICY_005_ACTION_CLASS_PROMOTION` | Action-class ladder, planner budgets, capacity/load gates | `tools/v7-users-autoswitch`, `admin_core/autonomy_trust_acceleration.py`, `admin_core/operator_execution_pipeline.py` | `IMPLEMENT_VERIFICATION` | `MODERATE_EXTENSION` | Planner move counts, capacity, fallback, policy scope. | `VERY_HIGH` | `HIGH` | `HIGH` | `VERY_HIGH` |
| `A6` | `TODO` | Implement action-class runtime eligibility arbitration using freshness, authority, blast radius, rollback, anti-flap, verification, and learning gates. | `POLICY_004_AUTHORITY`, `POLICY_005_ACTION_CLASS_PROMOTION`, `POLICY_006_BLAST_RADIUS`, `POLICY_007_ROLLBACK`, `POLICY_008_FRESHNESS`, `POLICY_009_ANTI_FLAP` | OMP, delegated policy preview, action-class runtime enablement, Runtime Model | `admin_core/autonomy_trust_acceleration.py`, `tools/v7-autonomy-trust-evidence-inventory`, `admin_core/operator_execution_pipeline.py` | `IMPLEMENT_READ_MODEL` | `MODERATE_EXTENSION` | A1-A5 gate outputs; no runtime apply enabled. | `VERY_HIGH` | `VERY_HIGH` | `VERY_HIGH` | `VERY_HIGH` |

## Tier B: High Value

| Id | Status | Task | Policy source | Owner | Files/modules | Implementation class | Estimated effort | Dependencies | Expected production value | Expected autonomy gain | Expected runtime gain | Expected safety gain |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `B1` | `TODO` | Aggregate liveness evidence by source family and confidence. | `POLICY_001_HARD_FAILURE` | Service matrix, Telegram sentinel, quality compact, route reality | `tools/v7-service-matrix-refresh-all`, `tools/v7-egress-quality-compact`, `admin_core/intelligence_workers.py` | `IMPLEMENT_BACKGROUND` | `MODERATE_EXTENSION` | A1 classifier shape. | `HIGH` | `HIGH` | `MEDIUM_HIGH` | `HIGH` |
| `B2` | `TODO` | Add hard-failure timer/risk class to policy windows. | `POLICY_001_HARD_FAILURE`, `POLICY_009_ANTI_FLAP` | OMP floors, safety policy, anti-flap overlay | `admin_core/autonomy_trust_acceleration.py`, `tools/v7-autonomy-trust-evidence-inventory` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | A2 freshness windows. | `HIGH` | `MEDIUM_HIGH` | `HIGH` | `HIGH` |
| `B3` | `TODO` | Align soft-degradation trend thresholds to canonical policy vocabulary. | `POLICY_002_SOFT_DEGRADATION` | Planner/autoswitch, quality compact, service matrix | `tools/v7-users-autoswitch`, `tools/v7-egress-quality-compact` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | Existing signal thresholds. | `HIGH` | `MEDIUM` | `MEDIUM_HIGH` | `HIGH` |
| `B4` | `TODO` | Normalize signal-to-policy mapping for degradation evidence. | `POLICY_002_SOFT_DEGRADATION` | Quality compact, service matrix, route/service views | `tools/v7-egress-quality-compact`, `tools/v7-service-matrix-refresh-all`, `admin_core/operator_decision_surface.py` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | Existing signal families. | `HIGH` | `HIGH` | `MEDIUM_HIGH` | `HIGH` |
| `B5` | `TODO` | Complete observed degradation attribution using active and passive evidence. | `POLICY_002_SOFT_DEGRADATION` | Service matrix, quality compact, trust/outcome stores | `admin_core/intelligence_workers.py`, `admin_core/operator_execution_feedback.py`, `admin_core/autonomy_trust_acceleration.py` | `IMPLEMENT_BACKGROUND` | `MODERATE_EXTENSION` | Outcome attribution evidence. | `HIGH` | `HIGH` | `MEDIUM` | `HIGH` |
| `B6` | `TODO` | Map circuit-breaker/outlier-ejection practice to V7-native actions. | `POLICY_002_SOFT_DEGRADATION` | Planner/autoswitch | `tools/v7-users-autoswitch`, `admin_core/operator_decision_surface.py` | `IMPLEMENT_READ_MODEL` | `MODERATE_EXTENSION` | Canonical degradation mapping. | `MEDIUM_HIGH` | `MEDIUM_HIGH` | `HIGH` | `HIGH` |
| `B7` | `TODO` | Bind service objectives to policy thresholds. | `POLICY_002_SOFT_DEGRADATION` | Service-user SLA fit, planner policy gates | `admin_core/autonomy_trust_acceleration.py`, `tools/v7-users-autoswitch` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | Service/user/SLA fit model. | `MEDIUM_HIGH` | `MEDIUM_HIGH` | `MEDIUM` | `HIGH` |
| `B8` | `TODO` | Certify recovery admission with repeated real success/readiness evidence. | `POLICY_003_RECOVERY_ADMISSION` | Recovery admission, service/route/readiness models | `admin_core/autonomy_trust_acceleration.py`, `tools/v7-service-matrix-refresh-all`, `tools/v7-egress-quality-compact` | `IMPLEMENT_CERTIFICATION` | `MODERATE_EXTENSION` | Real recovery outcomes. | `HIGH` | `HIGH` | `HIGH` | `HIGH` |
| `B9` | `TODO` | Require post-admission observation windows. | `POLICY_003_RECOVERY_ADMISSION` | Service matrix, quality compact, recovery admission | `admin_core/autonomy_trust_acceleration.py`, `tools/v7-egress-quality-compact` | `IMPLEMENT_VERIFICATION` | `SMALL_EXTENSION` | Recovery admission owner. | `HIGH` | `MEDIUM_HIGH` | `MEDIUM_HIGH` | `HIGH` |
| `B10` | `TODO` | Define recovery slow-start as V7 user/action-class progression. | `POLICY_003_RECOVERY_ADMISSION`, `POLICY_006_BLAST_RADIUS` | Blast-radius/action-class ladder | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`, `admin_core/autonomy_trust_acceleration.py` | `IMPLEMENT_READ_MODEL` | `MODERATE_EXTENSION` | B8 recovery certification. | `HIGH` | `HIGH` | `HIGH` | `HIGH` |
| `B11` | `TODO` | Complete org/cohort isolation and identity policy integration. | `POLICY_004_AUTHORITY`, `POLICY_006_BLAST_RADIUS` | Planner gates, identity/policy owners, OMP | `admin/v7-admin-api`, `admin_core/operator_decision_surface.py`, `tools/v7-users-autoswitch` | `IMPLEMENT_READ_MODEL` | `MODERATE_EXTENSION` | Identity DB and org policy availability. | `HIGH` | `MEDIUM_HIGH` | `MEDIUM` | `VERY_HIGH` |
| `B12` | `TODO` | Implement next action-class stage only after certification evidence exists. | `POLICY_005_ACTION_CLASS_PROMOTION` | Action-class ladder, OMP | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`, `admin_core/autonomy_trust_acceleration.py` | `IMPLEMENT_CERTIFICATION` | `SMALL_EXTENSION` | A3-A5 certification. | `HIGH` | `VERY_HIGH` | `HIGH` | `HIGH` |
| `B13` | `TODO` | Certify metric reliability for automated promotion recommendations. | `POLICY_005_ACTION_CLASS_PROMOTION` | Trust/confidence, freshness, rollback, eligibility | `admin_core/autonomy_trust_acceleration.py`, `tools/v7-autonomy-trust-evidence-inventory` | `IMPLEMENT_VERIFICATION` | `MODERATE_EXTENSION` | Representative outcome evidence. | `HIGH` | `HIGH` | `MEDIUM_HIGH` | `HIGH` |
| `B14` | `TODO` | Add service/pool/cohort blast-radius scope where required. | `POLICY_006_BLAST_RADIUS` | Planner, capacity/load, action-class ladder | `tools/v7-users-autoswitch`, `admin_core/operator_decision_surface.py`, `admin_core/autonomy_trust_acceleration.py` | `IMPLEMENT_READ_MODEL` | `MODERATE_EXTENSION` | Existing capacity/service owners. | `HIGH` | `HIGH` | `HIGH` | `VERY_HIGH` |
| `B15` | `TODO` | Expose containment/forward-fix classification. | `POLICY_007_ROLLBACK` | Runtime Model, execution packet partial-failure policy | `admin_core/operator_execution.py`, `admin_core/operator_execution_pipeline.py` | `IMPLEMENT_OBSERVABILITY` | `SMALL_EXTENSION` | Existing partial-failure policy. | `HIGH` | `MEDIUM_HIGH` | `HIGH` | `HIGH` |
| `B16` | `TODO` | Certify automatic rollback authority after reliable verification evidence. | `POLICY_007_ROLLBACK` | Autoswitch rollback-on-verify-fail, OMP operational/engineering authority gates | `tools/v7-users-autoswitch`, `admin_core/operator_execution.py`, `admin_core/operator_execution_pipeline.py` | `IMPLEMENT_CERTIFICATION` | `MODERATE_EXTENSION` | Verification reliability and authority approval. | `HIGH` | `HIGH` | `VERY_HIGH` | `VERY_HIGH` |
| `B17` | `TODO` | Preserve stale-read reporting while blocking mutation. | `POLICY_008_FRESHNESS` | Runtime eligibility, truth/convergence, read-only inventory | `admin_core/autonomy_trust_acceleration.py`, `tools/v7-autonomy-trust-evidence-inventory` | `IMPLEMENT_OBSERVABILITY` | `SMALL_EXTENSION` | Existing read-only/action split. | `HIGH` | `MEDIUM` | `MEDIUM` | `HIGH` |
| `B18` | `TODO` | Extend owner-issued version/lease pattern where available. | `POLICY_008_FRESHNESS` | Execution lease, runtime snapshot, intelligence snapshots | `admin_core/operator_execution.py`, `admin_core/intelligence_snapshots.py`, `admin_core/autonomy_trust_acceleration.py` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | Existing lease and snapshot generations. | `HIGH` | `HIGH` | `HIGH` | `VERY_HIGH` |
| `B19` | `TODO` | Centralize hysteresis and state-change-cost mapping across failure, recovery, and movement-protection owners. | `POLICY_009_ANTI_FLAP` | Service signal thresholds, recovery admission, movement protection | `admin_core/autonomy_trust_acceleration.py`, `tools/v7-service-matrix-refresh-all`, `tools/v7-users-autoswitch` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | Existing thresholds, sticky/current bias, cooldown, freeze, pair reversal, and minimum movement improvement. | `HIGH` | `HIGH` | `MEDIUM_HIGH` | `HIGH` |
| `B20` | `TODO` | Encode hard-failure override rule for anti-flap arbitration. | `POLICY_009_ANTI_FLAP`, `POLICY_001_HARD_FAILURE` | OMP, planner, runtime eligibility | `admin_core/autonomy_trust_acceleration.py`, `tools/v7-users-autoswitch` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | A1 hard-failure classifier. | `HIGH` | `HIGH` | `HIGH` | `VERY_HIGH` |
| `B21` | `TODO` | Implement explicit per-user `AUTO` / `PINNED` / `MANUAL` routing control mode through existing user, policy, planner, and admin owners. | `WORLD_EQUIVALENCE_MODEL`, `MOVEMENT_PROTECTION_MODEL`, `POLICY_004_AUTHORITY`, `POLICY_006_BLAST_RADIUS` | User registry, group/organization policy, planner gates, admin operator surface | `admin/v7-admin-api`, `admin_core/operator_decision_surface.py`, `tools/v7-users-autoswitch`, `admin_core/registry_readers.py` | `IMPLEMENT_READ_MODEL` | `MODERATE_EXTENSION` | Current assignment, group preference, `manual_only`/`reserve_only`, org policy, and planner gate semantics. | `HIGH` | `MEDIUM_HIGH` | `MEDIUM_HIGH` | `VERY_HIGH` |

## Tier C: Medium

| Id | Status | Task | Policy source | Owner | Files/modules | Implementation class | Estimated effort | Dependencies | Expected production value | Expected autonomy gain | Expected runtime gain | Expected safety gain |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `C1` | `TODO` | Record fail-open/fail-closed behavior per action class. | `POLICY_001_HARD_FAILURE` | Runtime Model, OMP, planner gates | `docs/reference/V7_RUNTIME_MODEL.md`, `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`, `admin_core/autonomy_trust_acceleration.py` | `IMPLEMENT_DOCUMENTATION` | `NONE` | Action-class policy update. | `MEDIUM` | `MEDIUM` | `MEDIUM` | `HIGH` |
| `C2` | `TODO` | Use probabilistic suspicion only as advisory evidence. | `POLICY_002_SOFT_DEGRADATION` | Trust/confidence model, shadow autonomy | `admin_core/shadow_autonomy.py`, `admin_core/autonomy_trust_acceleration.py` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | Signal confidence reliability. | `MEDIUM` | `MEDIUM` | `MEDIUM` | `MEDIUM_HIGH` |
| `C3` | `TODO` | Define break-glass authority as audited exceptional operator policy. | `POLICY_004_AUTHORITY` | OMP, operator authority | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`, `admin_core/operator_execution_pipeline.py` | `IMPLEMENT_DOCUMENTATION` | `SMALL_EXTENSION` | Operator policy approval. | `MEDIUM` | `LOW` | `MEDIUM` | `HIGH` |
| `C4` | `TODO` | Keep all-at-once promotion unavailable for current action classes. | `POLICY_005_ACTION_CLASS_PROMOTION` | OMP, blast-radius gates | `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`, `admin_core/autonomy_trust_acceleration.py` | `IMPLEMENT_VERIFICATION` | `NONE` | Current authority model. | `MEDIUM` | `MEDIUM` | `LOW` | `HIGH` |
| `C5` | `TODO` | Preserve rollback as operational compensation rather than transaction rollback. | `POLICY_007_ROLLBACK` | Runtime Model, rollback policy | `docs/reference/V7_RUNTIME_MODEL.md`, `admin_core/operator_execution.py` | `IMPLEMENT_DOCUMENTATION` | `NONE` | Existing rollback semantics. | `MEDIUM` | `LOW` | `MEDIUM` | `MEDIUM_HIGH` |
| `C6` | `TODO` | Decide bounded stale allowance by action class. | `POLICY_008_FRESHNESS` | Freshness actionability, OMP stop rules | `admin_core/autonomy_trust_acceleration.py`, `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | A2 freshness windows. | `MEDIUM_HIGH` | `MEDIUM` | `MEDIUM` | `HIGH` |
| `C7` | `TODO` | Map pool max-ejection/minimum-health semantics to V7 capacity and blast bounds. | `POLICY_009_ANTI_FLAP`, `POLICY_006_BLAST_RADIUS` | Planner capacity/load, action-class ladder | `tools/v7-users-autoswitch`, `admin_core/autonomy_trust_acceleration.py` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | Capacity/load evidence. | `MEDIUM_HIGH` | `MEDIUM` | `MEDIUM_HIGH` | `HIGH` |

## Tier D: Optional

| Id | Status | Task | Policy source | Owner | Files/modules | Implementation class | Estimated effort | Dependencies | Expected production value | Expected autonomy gain | Expected runtime gain | Expected safety gain |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `D1` | `OPTIONAL` | Revisit MPLS/router-local repair only if V7 substrate changes. | `POLICY_001_HARD_FAILURE`, `POLICY_006_BLAST_RADIUS` | Future route/planner owner only if needed | None current | `IMPLEMENT_DOCUMENTATION` | `NONE` | Future substrate change. | `LOW` | `LOW` | `LOW` | `LOW` |
| `D2` | `OPTIONAL` | Revisit provider replacement as a platform operation. | `POLICY_003_RECOVERY_ADMISSION` | Future platform/provider owner only if needed | None current | `IMPLEMENT_DOCUMENTATION` | `NONE` | Future provider lifecycle scope. | `LOW` | `LOW` | `LOW` | `MEDIUM` |
| `D3` | `OPTIONAL` | Revisit DNS-level recovery only if DNS failover becomes product scope. | `POLICY_003_RECOVERY_ADMISSION` | Future DNS/platform owner only if needed | None current | `IMPLEMENT_DOCUMENTATION` | `NONE` | Future DNS failover scope. | `LOW` | `LOW` | `LOW` | `LOW` |
| `D4` | `OPTIONAL` | Revisit quorum/leader authority only for distributed operator control. | `POLICY_004_AUTHORITY` | Execution lease owner, future distributed authority owner only if proven | None current | `IMPLEMENT_DOCUMENTATION` | `NONE` | Future distributed control-plane need. | `LOW` | `LOW` | `LOW` | `MEDIUM` |
| `D5` | `OPTIONAL` | Revisit weighted traffic split only if V7 supports split traffic instead of user movement. | `POLICY_006_BLAST_RADIUS` | Planner/autoswitch if future scope requires it | None current | `IMPLEMENT_DOCUMENTATION` | `NONE` | Future split-traffic product scope. | `LOW` | `LOW` | `MEDIUM` | `MEDIUM` |
| `D6` | `OPTIONAL` | Revisit BGP route-flap damping only if V7 owns routing-protocol behavior. | `POLICY_009_ANTI_FLAP` | Future route owner only if needed | None current | `IMPLEMENT_DOCUMENTATION` | `NONE` | Future routing-protocol owner. | `LOW` | `LOW` | `LOW` | `LOW` |

## Backlog Verdict

The backlog is implementable through existing V7 owners.

Need New Owner: `FALSE`.

Fundamental architecture gap: `NO`.

Runtime automation enabled by this backlog: `NO`.

User movement enabled by this backlog: `NO`.

Authority expansion enabled by this backlog: `NO`.
