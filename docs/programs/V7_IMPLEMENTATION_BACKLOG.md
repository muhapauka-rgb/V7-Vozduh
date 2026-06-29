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
| Tier A | `6` | `6` | `COMPLETE` |
| Tier B | `21` | `21` | `COMPLETE` |
| Tier C | `1` | `7` | `IN_PROGRESS` |
| Tier D optional | `0` | `6` | `OPTIONAL` |
| Overall actionable | `28` | `34` | `ACTIVE` |

Implementation maturity:

```text
82.4%
```

Estimated remaining effort:

```text
Moderate
```

Next item:

```text
C2
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
| Runtime-certified Slow-Start Recovery | Recovery admission, blast-radius/action-class ladder | `B10` | Recovery slow-start progression is defined read-only through existing B8/B9 recovery evidence and B10 blast-radius/action-class stage mapping; runtime consumption remains blocked until later certified implementation/authority. | `EXTEND_EXISTING_DONE_READ_ONLY` |
| Pool Max-Ejection / Minimum-Health semantics | Planner capacity/load, action-class ladder, blast-radius bounds | `C7` | Capacity/load and authority budgets exist; proxy-style max-ejection/minimum-health mapping remains unfinished. | `EXTEND_EXISTING` |
| State Change Cost Model | Planner/autoswitch, movement protection model, anti-flap owners | `B19` | Already exists semantically as sticky/current-channel bonus, minimum improvement threshold, cooldown, freeze, pair reversal, target block, egress quarantine, rebalance restraint, and authority/blast caps. B19 owns vocabulary consolidation only. | `EXTEND_EXISTING` |

Need New Owner: `FALSE`.

Need New Document: `FALSE`.

State Change Cost verdict: `ALREADY_EXISTS_SEMANTICALLY`; extend existing B19 vocabulary only, do not create a new owner or new backlog item.

## Current Highest Priority

| Field | Value |
| --- | --- |
| Backlog id | `C2` |
| Status | `READY` |
| Task | Use probabilistic suspicion only as advisory evidence. |
| Policy source | `POLICY_002_SOFT_DEGRADATION` |
| Owner | Trust/confidence model, shadow autonomy, OMP |
| Files/modules | `admin_core/shadow_autonomy.py`, `admin_core/autonomy_trust_acceleration.py`, `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` |
| Implementation class | `IMPLEMENT_READ_MODEL` |
| Estimated effort | `SMALL_EXTENSION` |
| Dependencies | Signal confidence reliability; C1 fail-open/fail-closed action-class behavior. |
| Expected production value | `MEDIUM` |
| Expected autonomy gain | `MEDIUM` |
| Expected runtime gain | `MEDIUM` |
| Expected safety gain | `MEDIUM_HIGH` |

## Runtime Latency Foundation Placement

Status: `RT_PHASE_1_FULLY_COMPLETE`.

RT Phase 1 did not create a new backlog item.
Runtime latency work must be absorbed by existing owners and backlog items.

Canonical owner:

```text
docs/reference/V7_RUNTIME_MODEL.md
```

Backlog placement:

| RT concern | Existing backlog owner | Reason |
| --- | --- | --- |
| Class-level blast-radius timing and action-size safety | `A5` | Safe low-latency recovery cannot expand action size before blast radius is certified. |
| Runtime eligibility arbitration and live gate ordering | `A6` | The final execute/stop decision owns live safety gates and must preserve the thin runtime path. |
| Metric reliability for promotion and latency-aware recommendations | `B13` | Fast decisions are unsafe unless metrics are reliable enough for promotion recommendations. |
| Rollback authority and verification-dependent compensation | `B16` | Faster execution requires certified rollback/verification handling. |
| Owner-issued freshness and decision lifetime | `B18`, `C6` | Reaction latency depends on freshness without permitting stale unsafe action. |
| Anti-flap, state-change cost, and rate-limit semantics | `B19`, `B20` | Faster reaction must not create oscillation or retry storms. |
| Recovery admission and slow-start timing | `B8`, `B9`, `B10` | Recovered targets must be re-admitted through repeated readiness, observation windows, and staged recovery. |

No new owner, planner, runtime path, execution queue, daemon, authority model, or backlog item is allowed for RT Phase 1.

RT Phase 1 completion includes:

- `RT1` Canonical Time Architecture;
- `RT2` Reaction Latency Model;
- `RT3` Thin Runtime Path Contract;
- `RT4` Latency Ownership & Live/Precompute Matrix;
- `RT5` Engineering Report Latency Requirement;
- `RT6` Phase 2 Automation-Time Contract;
- `RT7` Runtime Latency Engineering Review Checklist;
- `RT8` complete Phase 2 Automation Contract.

Future runtime-latency work must map to the existing backlog owners above unless a complete OMP audit proves reuse impossible.

## Tier A: Highest Production Leverage

| Id | Status | Task | Policy source | Owner | Files/modules | Implementation class | Estimated effort | Dependencies | Expected production value | Expected autonomy gain | Expected runtime gain | Expected safety gain |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `A1` | `DONE` | Bind canonical hard-failure classification to existing liveness/event evidence. | `POLICY_001_HARD_FAILURE` | Event sources, service matrix, quality compact, planner/autoswitch | `tools/v7-users-autoswitch`, `tools/v7-service-matrix-refresh-all`, `tools/v7-egress-quality-compact`, `admin_core/operator_decision_surface.py`, `admin_core/autonomy_trust_acceleration.py` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | Existing liveness, service, route, runtime evidence. | `VERY_HIGH` | `HIGH` | `HIGH` | `VERY_HIGH` |
| `A2` | `DONE` | Canonicalize per-action-class freshness windows and owner-issued freshness fields. | `POLICY_008_FRESHNESS`, `POLICY_001_HARD_FAILURE`, `POLICY_003_RECOVERY_ADMISSION` | Freshness actionability, delegated policy preview, execution lease | `admin_core/autonomy_trust_acceleration.py`, `admin_core/operator_execution.py`, `tools/v7-autonomy-trust-evidence-inventory` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | Existing freshness classifications, packet lease, runtime fingerprints. | `VERY_HIGH` | `HIGH` | `VERY_HIGH` | `VERY_HIGH` |
| `A3` | `DONE` | Certify class-level rollback/no-rollback evidence for governed candidate movement. | `POLICY_007_ROLLBACK`, `POLICY_005_ACTION_CLASS_PROMOTION` | Restore barrier, rollback manifest, governed execution, feedback/learning | `admin_core/operator_execution.py`, `tools/v7-users-autoswitch`, `admin_core/operator_execution_feedback.py`, `admin_core/autonomy_trust_acceleration.py` | `IMPLEMENT_CERTIFICATION` | `MODERATE_EXTENSION` | Real governed no-rollback outcome closed for packet `pkt_preview_5c4bcfaa59d769ced6d6e5dc`; feedback `execfb_55e330784ad36b513d23e12a`; learning `learn_0c3b5cdd250c64ac7d9b97e7`. | `VERY_HIGH` | `VERY_HIGH` | `HIGH` | `VERY_HIGH` |
| `A4` | `DONE` | Materialize representative outcome evidence for the first action class. | `POLICY_005_ACTION_CLASS_PROMOTION` | OMP promotion engine, feedback/learning, outcome leverage model | `admin_core/operator_execution_feedback.py`, `admin_core/autonomy_trust_acceleration.py`, `tools/v7-autonomy-trust-evidence-inventory` | `IMPLEMENT_BACKGROUND` | `MODERATE_EXTENSION` | Real comparable outcomes collected; candidate inventory signal is empty; outcome closure read-model is `COMPLETE`; no synthetic evidence. | `VERY_HIGH` | `VERY_HIGH` | `MEDIUM_HIGH` | `HIGH` |
| `A5` | `DONE` | Certify class-level blast-radius evidence beyond the one-user guard. | `POLICY_006_BLAST_RADIUS`, `POLICY_005_ACTION_CLASS_PROMOTION` | Action-class ladder, planner budgets, capacity/load gates | `tools/v7-users-autoswitch`, `admin_core/autonomy_trust_acceleration.py`, `admin_core/operator_execution_pipeline.py` | `IMPLEMENT_VERIFICATION` | `MODERATE_EXTENSION` | Read-only verifier consumed existing E29 historical governed execution proofs: one-user, two-user, and four-user movement are certified; authority remains unchanged. | `VERY_HIGH` | `HIGH` | `HIGH` | `VERY_HIGH` |
| `A6` | `DONE` | Implement action-class runtime eligibility arbitration using freshness, authority, blast radius, rollback, anti-flap, verification, and learning gates. | `POLICY_004_AUTHORITY`, `POLICY_005_ACTION_CLASS_PROMOTION`, `POLICY_006_BLAST_RADIUS`, `POLICY_007_ROLLBACK`, `POLICY_008_FRESHNESS`, `POLICY_009_ANTI_FLAP` | OMP, delegated policy preview, action-class runtime enablement, Runtime Model | `admin_core/autonomy_trust_acceleration.py`, `tools/v7-autonomy-trust-evidence-inventory`, `admin_core/operator_execution_pipeline.py` | `IMPLEMENT_READ_MODEL` | `MODERATE_EXTENSION` | `runtime_eligibility_arbitration` consumes A1-A5 gate outputs and returns read-only execute-or-stop gate rows; current decision is `STOP_SAFE` at authority/runtime_apply; no runtime apply or authority expansion. | `VERY_HIGH` | `VERY_HIGH` | `VERY_HIGH` | `VERY_HIGH` |

## Tier B: High Value

| Id | Status | Task | Policy source | Owner | Files/modules | Implementation class | Estimated effort | Dependencies | Expected production value | Expected autonomy gain | Expected runtime gain | Expected safety gain |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `B1` | `DONE` | Aggregate liveness evidence by source family and confidence. | `POLICY_001_HARD_FAILURE` | Service matrix, Telegram sentinel, quality compact, route reality | `admin_core/autonomy_trust_acceleration.py::build_liveness_evidence_aggregation`, `tools/v7-service-matrix-refresh-all`, `tools/v7-egress-quality-compact`, `admin_core/intelligence_workers.py` | `IMPLEMENT_BACKGROUND` | `MODERATE_EXTENSION` | A1 classifier shape. | `HIGH` | `HIGH` | `MEDIUM_HIGH` | `HIGH` |
| `B2` | `DONE` | Add hard-failure timer/risk class to policy windows. | `POLICY_001_HARD_FAILURE`, `POLICY_009_ANTI_FLAP` | OMP floors, safety policy, anti-flap overlay | `admin_core/autonomy_trust_acceleration.py::build_hard_failure_policy_windows`, `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | `hard_failure_policy_windows` exposes hard-failure risk classes, reaction window impact, anti-flap blockers, and no-timer-change proof from existing A1/A2/B1 owners; no runtime apply or authority expansion. | `HIGH` | `MEDIUM_HIGH` | `HIGH` | `HIGH` |
| `B3` | `DONE` | Align soft-degradation trend thresholds to canonical policy vocabulary. | `POLICY_002_SOFT_DEGRADATION` | Planner/autoswitch, quality compact, service matrix | `admin_core/autonomy_trust_acceleration.py::build_soft_degradation_threshold_vocabulary_alignment`, `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only`, `tools/v7-users-autoswitch`, `tools/v7-egress-quality-compact` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | `soft_degradation_threshold_vocabulary` maps existing degradation trends/states to canonical policy results and decision vocabulary without threshold/formula changes, runtime apply, authority expansion, synthetic evidence, or user movement. | `HIGH` | `MEDIUM` | `MEDIUM_HIGH` | `HIGH` |
| `B4` | `DONE` | Normalize signal-to-policy mapping for degradation evidence. | `POLICY_002_SOFT_DEGRADATION` | Quality compact, service matrix, route/service views | `admin_core/autonomy_trust_acceleration.py::build_degradation_signal_policy_mapping`, `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only`, `tools/v7-egress-quality-compact`, `tools/v7-service-matrix-refresh-all`, `admin_core/operator_decision_surface.py` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | `degradation_signal_policy_mapping` maps existing latency, error, timeout, loss, jitter, saturation, service-response, and route-readiness signal families to `POLICY_002_SOFT_DEGRADATION` without attribution, threshold/formula changes, runtime apply, authority expansion, synthetic evidence, or user movement. | `HIGH` | `HIGH` | `MEDIUM_HIGH` | `HIGH` |
| `B5` | `DONE` | Complete observed degradation attribution using active and passive evidence. | `POLICY_002_SOFT_DEGRADATION` | Service matrix, quality compact, trust/outcome stores | `admin_core/autonomy_trust_acceleration.py::build_observed_degradation_attribution`, `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only`, `admin_core/intelligence_workers.py`, `admin_core/operator_execution_feedback.py` | `IMPLEMENT_BACKGROUND` | `MODERATE_EXTENSION` | `observed_degradation_attribution` joins existing active service/quality observations with passive feedback/outcome/trust evidence by object, attributes only evidence sources, and forbids root-cause claims, threshold/formula changes, runtime apply, authority expansion, synthetic evidence, or user movement. | `HIGH` | `HIGH` | `MEDIUM` | `HIGH` |
| `B6` | `DONE` | Map circuit-breaker/outlier-ejection practice to V7-native actions. | `POLICY_002_SOFT_DEGRADATION` | Planner/autoswitch | `admin_core/autonomy_trust_acceleration.py::build_v7_native_degradation_response_mapping`, `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only`, `tools/v7-users-autoswitch`, `admin_core/operator_decision_surface.py` | `IMPLEMENT_READ_MODEL` | `MODERATE_EXTENSION` | `v7_native_degradation_response_mapping` maps circuit-breaker and outlier-ejection practice to existing V7 actions such as `ASK_OPERATOR`, `PROBE_ONLY`, `HOLD_MOVEMENT`, `QUARANTINE_FOR_NORMAL_TARGET_USE`, and `REQUIRE_RECOVERY_ADMISSION` without runtime behavior change, threshold/formula changes, authority expansion, synthetic evidence, or user movement. | `MEDIUM_HIGH` | `MEDIUM_HIGH` | `HIGH` | `HIGH` |
| `B7` | `DONE` | Bind service objectives to policy thresholds. | `POLICY_002_SOFT_DEGRADATION` | Service-user SLA fit, planner policy gates | `admin_core/autonomy_trust_acceleration.py::build_service_objective_policy_threshold_binding`, `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only`, `tools/v7-users-autoswitch` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | `service_objective_policy_threshold_binding` binds required services, service freshness, fit score, capacity/headroom, route/runtime safety, soft-degradation policy, and degradation response objectives to existing threshold sources without threshold/formula changes, runtime behavior change, authority expansion, synthetic evidence, or user movement. | `MEDIUM_HIGH` | `MEDIUM_HIGH` | `MEDIUM` | `HIGH` |
| `B8` | `DONE` | Certify recovery admission with repeated real success/readiness evidence. | `POLICY_003_RECOVERY_ADMISSION` | Recovery admission, service/route/readiness models | `admin_core/autonomy_trust_acceleration.py::build_recovery_admission_certification`, `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only`, `tools/v7-service-matrix-refresh-all`, `tools/v7-egress-quality-compact` | `IMPLEMENT_CERTIFICATION` | `MODERATE_EXTENSION` | `recovery_admission_certification` certifies existing recovery admission evidence only when repeated successful checks, service readiness evidence, quality readiness evidence, freshness, and objective binding context are present; it creates no runtime actions, grants no authority, creates no synthetic evidence, and moves no users. | `HIGH` | `HIGH` | `HIGH` | `HIGH` |
| `B9` | `DONE` | Require post-admission observation windows. | `POLICY_003_RECOVERY_ADMISSION` | Service matrix, quality compact, recovery admission | `admin_core/autonomy_trust_acceleration.py::build_post_admission_observation_windows`, `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only`, `tools/v7-egress-quality-compact` | `IMPLEMENT_VERIFICATION` | `SMALL_EXTENSION` | `post_admission_observation_windows` verifies existing post-admission service observation and quality compact `5m`/`1h` windows after B8 certification without admitting traffic, granting authority, creating synthetic evidence, or moving users. | `HIGH` | `MEDIUM_HIGH` | `MEDIUM_HIGH` | `HIGH` |
| `B10` | `DONE` | Define recovery slow-start as V7 user/action-class progression. | `POLICY_003_RECOVERY_ADMISSION`, `POLICY_006_BLAST_RADIUS` | Blast-radius/action-class ladder | `admin_core/autonomy_trust_acceleration.py::build_recovery_slow_start_progression`, `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only`, `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` | `IMPLEMENT_READ_MODEL` | `MODERATE_EXTENSION` | `recovery_slow_start_progression` defines staged recovery as `OBSERVATION_CERTIFIED_READ_ONLY` -> `ONE_USER_GOVERNED_RECOVERY_REVIEW` -> `BEYOND_ONE_USER_ACTION_CLASS_REVIEW`, reusing B8/B9 and class-level blast-radius evidence without runtime apply, authority expansion, synthetic evidence, or user movement. | `HIGH` | `HIGH` | `HIGH` | `HIGH` |
| `B11` | `DONE` | Complete org/cohort isolation and identity policy integration. | `POLICY_004_AUTHORITY`, `POLICY_006_BLAST_RADIUS` | Planner gates, identity/policy owners, OMP | `admin_core/autonomy_trust_acceleration.py::build_org_cohort_identity_policy_integration`, `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only`, `admin/v7-admin-api`, `admin_core/operator_decision_surface.py`, `tools/v7-users-autoswitch` | `IMPLEMENT_READ_MODEL` | `MODERATE_EXTENSION` | `org_cohort_identity_policy_integration` exposes identity -> group/cohort -> allowed/preferred/excluded egress -> exclusive_group/egress ACL/default isolation gates through existing owners without runtime apply, authority expansion, synthetic evidence, or user movement. | `HIGH` | `MEDIUM_HIGH` | `MEDIUM` | `VERY_HIGH` |
| `B12` | `DONE` | Implement next action-class stage only after certification evidence exists. | `POLICY_005_ACTION_CLASS_PROMOTION` | Action-class ladder, OMP | `admin_core/autonomy_trust_acceleration.py::build_next_action_class_stage_certification`, `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only`, `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md` | `IMPLEMENT_CERTIFICATION` | `SMALL_EXTENSION` | `next_action_class_stage_certification` consumes A5 blast-radius evidence, A6 runtime eligibility arbitration, B13 blocking metric reliability, and B11 identity/policy boundaries; it certifies stage readiness for authority review only and keeps Runtime apply, authority expansion, direct class promotion, synthetic evidence, and user movement blocked. | `HIGH` | `VERY_HIGH` | `HIGH` | `HIGH` |
| `B13` | `DONE` | Certify metric reliability for automated promotion recommendations. | `POLICY_005_ACTION_CLASS_PROMOTION` | Trust/confidence, freshness, rollback, eligibility | `admin_core/autonomy_trust_acceleration.py`, `tools/v7-autonomy-trust-evidence-inventory` | `IMPLEMENT_VERIFICATION` | `MODERATE_EXTENSION` | `metric_reliability_certification` certifies reliable blocking recommendations only: current recommendation is `DO_NOT_PROMOTE_COLLECT_REAL_EVIDENCE`; positive promotion remains blocked by partial service/candidate/floor/freshness/runtime/authority evidence; no runtime apply or authority expansion. | `HIGH` | `HIGH` | `MEDIUM_HIGH` | `HIGH` |
| `B14` | `DONE` | Add service/pool/cohort blast-radius scope where required. | `POLICY_006_BLAST_RADIUS` | Planner, capacity/load, action-class ladder | `admin_core/autonomy_trust_acceleration.py::build_service_pool_cohort_blast_radius_scope`, `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only`, `tools/v7-users-autoswitch` capacity/load/dynamic blast-radius owners | `IMPLEMENT_READ_MODEL` | `MODERATE_EXTENSION` | `service_pool_cohort_blast_radius_scope` consumes existing service/user/SLA fit, B11 identity/cohort policy integration, A5 blast-radius certification, and B12 stage certification; it maps service, pool, cohort, capacity, and blast-radius scope read-only while keeping Runtime apply, authority expansion, blast-radius expansion, synthetic evidence, threshold/formula mutation, and user movement blocked. | `HIGH` | `HIGH` | `HIGH` | `VERY_HIGH` |
| `B15` | `DONE` | Expose containment/forward-fix classification. | `POLICY_007_ROLLBACK` | Runtime Model, execution packet partial-failure policy | `admin_core/operator_execution.py::containment_forward_fix_classification`, `admin_core/operator_execution_pipeline.py::rt2_s4_governed_execution_coordination` | `IMPLEMENT_OBSERVABILITY` | `SMALL_EXTENSION` | `containment_forward_fix_classification` exposes terminal containment vs forward-fix states from existing packet, verification, rollback, and partial-failure policy evidence; it keeps Runtime apply, rollback execution, authority expansion, synthetic evidence, and user movement blocked. | `HIGH` | `MEDIUM_HIGH` | `HIGH` | `HIGH` |
| `B16` | `DONE` | Certify automatic rollback authority after reliable verification evidence. | `POLICY_007_ROLLBACK` | Autoswitch rollback-on-verify-fail, OMP operational/engineering authority gates | `tools/v7-users-autoswitch`, `admin_core/operator_execution.py`, `admin_core/operator_execution_pipeline.py`, `admin_core/autonomy_trust_acceleration.py` | `IMPLEMENT_CERTIFICATION` | `MODERATE_EXTENSION` | `rollback_authority_certification` certifies rollback/verification/metric/runtime evidence for authority review only; automatic rollback authority is not granted, runtime apply remains disabled, rollback execution is not performed, and authority/runtime_apply remain STOP gates. | `HIGH` | `HIGH` | `VERY_HIGH` | `VERY_HIGH` |
| `B17` | `DONE` | Preserve stale-read reporting while blocking mutation. | `POLICY_008_FRESHNESS` | Runtime eligibility, truth/convergence, read-only inventory | `admin_core/autonomy_trust_acceleration.py::build_stale_read_mutation_blocking`, `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only` | `IMPLEMENT_OBSERVABILITY` | `SMALL_EXTENSION` | `stale_read_mutation_blocking` preserves stale/unknown freshness visibility as reportable read-only evidence while blocking mutation through existing freshness, runtime eligibility, and routing readiness owners; stale reads cannot authorize runtime apply, authority expansion, synthetic evidence, threshold/formula mutation, or user movement. | `HIGH` | `MEDIUM` | `MEDIUM` | `HIGH` |
| `B18` | `DONE` | Extend owner-issued version/lease pattern where available. | `POLICY_008_FRESHNESS` | Execution lease, runtime snapshot, intelligence snapshots | `admin_core/autonomy_trust_acceleration.py::build_owner_issued_version_lease_pattern`, `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | `owner_issued_version_lease_pattern` exposes owner-issued version/lease/generation/TTL/source-hash coverage by reusing existing execution lease, Runtime Model freshness gates, `SNAPSHOT_FAMILIES`, freshness actionability, action-class freshness windows, and B17 stale-read mutation blocking; it changes no lease behavior, creates no new owner, grants no authority, applies no Runtime changes, and moves no users. | `HIGH` | `HIGH` | `HIGH` | `VERY_HIGH` |
| `B19` | `DONE` | Centralize hysteresis and state-change-cost mapping across failure, recovery, and movement-protection owners. | `POLICY_009_ANTI_FLAP` | Service signal thresholds, recovery admission, movement protection | `admin_core/autonomy_trust_acceleration.py::build_hysteresis_state_change_cost_mapping`, `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | `hysteresis_state_change_cost_mapping` centralizes existing sticky/current bias, minimum improvement, cooldown, observation window, oscillation detection, user freeze, pair reversal, target block/quarantine, recovery thresholds, and freshness identity cost vocabulary without changing thresholds, formulas, Runtime, authority, planner ownership, or users. | `HIGH` | `HIGH` | `MEDIUM_HIGH` | `HIGH` |
| `B20` | `DONE` | Encode hard-failure override rule for anti-flap arbitration. | `POLICY_009_ANTI_FLAP`, `POLICY_001_HARD_FAILURE` | OMP, planner, runtime eligibility | `admin_core/autonomy_trust_acceleration.py::build_hard_failure_override_anti_flap_arbitration`, `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only`, `tools/v7-users-autoswitch` | `IMPLEMENT_READ_MODEL` | `SMALL_EXTENSION` | `hard_failure_override_anti_flap_arbitration` encodes confirmed hard failure as anti-flap override candidate for authority review only; suspected/no hard failure cannot override anti-flap; Runtime apply, authority expansion, hard-failure override execution, threshold/formula mutation, synthetic evidence, new owner, and user movement remain blocked. | `HIGH` | `HIGH` | `HIGH` | `VERY_HIGH` |
| `B21` | `DONE` | Implement explicit per-user `AUTO` / `PINNED` / `MANUAL` routing control mode through existing user, policy, planner, and admin owners. | `WORLD_EQUIVALENCE_MODEL`, `MOVEMENT_PROTECTION_MODEL`, `POLICY_004_AUTHORITY`, `POLICY_006_BLAST_RADIUS` | User registry, group/organization policy, planner gates, admin operator surface | `admin_core/autonomy_trust_acceleration.py::build_per_user_routing_control_mode`, `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only`, `admin/v7-admin-api`, `admin_core/operator_decision_surface.py`, `tools/v7-users-autoswitch`, `admin_core/registry_readers.py` | `IMPLEMENT_READ_MODEL` | `MODERATE_EXTENSION` | `per_user_routing_control_mode` normalizes explicit or inferred `AUTO` / `PINNED` / `MANUAL` per-user routing control mode from existing user registry, org policy, planner, and admin surface owners without registry writes, Runtime apply, authority expansion, planner replacement, synthetic evidence, or user movement. | `HIGH` | `MEDIUM_HIGH` | `MEDIUM_HIGH` | `VERY_HIGH` |

## Tier C: Medium

| Id | Status | Task | Policy source | Owner | Files/modules | Implementation class | Estimated effort | Dependencies | Expected production value | Expected autonomy gain | Expected runtime gain | Expected safety gain |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `C1` | `DONE` | Record fail-open/fail-closed behavior per action class. | `POLICY_001_HARD_FAILURE` | Runtime Model, OMP, planner gates | `docs/reference/V7_RUNTIME_MODEL.md`, `docs/programs/OPERATIONAL_MATURITY_PROGRAM.md`, `admin_core/autonomy_trust_acceleration.py::build_fail_open_fail_closed_action_class_behavior`, `tools/v7-autonomy-trust-evidence-inventory --routing-foundation-only` | `IMPLEMENT_READ_MODEL` | `NONE` | `fail_open_fail_closed_action_class_behavior` records per-action-class fail-closed runtime mutation/apply behavior and read-only fail-open allowance for diagnosis/evidence/report/canonical update, without Runtime changes, authority expansion, planner replacement, synthetic evidence, or user movement. | `MEDIUM` | `MEDIUM` | `MEDIUM` | `HIGH` |
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
