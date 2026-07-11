# Material Decision Churn Discovery And Closure

Дата: `2026-07-11T18:43:57+0700`  
Mission ID: `V7_OMP_MATERIAL_DECISION_CHURN_CLOSURE_V1`  
Статус отчёта: `DEPLOYED_INITIAL_STABILITY_EVIDENCE_COLLECTED`

## Summary

Текущий `REAL_WORLD_LIMIT_OR_EXCESSIVE_DECISION_CHURN` воспроизведён в production read-only серией из 10 cycles. Архитектурный gap не найден. Existing coordinator owner привязывал execution packet к whole-file hashes `v7-state.json` и `candidate-suitability-summary.json` до окончательного candidate selection. Это смешивало material decision state с refresh metadata и unrelated rows. При неизменных selected move и Decision Fingerprint raw suitability hash и `candidate_hash` менялись, создавая false invalidation.

Минимальное исправление выполнено в существующих owners: strict selected identity и decision-relevant runtime/suitability projections стали execution binding; raw whole-file hashes сохранены отдельно как observability provenance. Authority, Runtime apply, Safe Mode, Planner ownership, action class и blast radius не изменены.

## ECR And Baseline

Использованы CPS section 0 и registry, OMP, Canonical Reference, SYSTEM_MAP, Runtime/Decision models, B19/B20, existing planner/autoswitch, governed coordinator, packet/lease, approved-plan-lock, source-bundle lease, Safe Mode, verification/rollback/outcome/learning owners и reports Phase 4A/current-class churn. Current WIP: `CAP-U01-FIRST-GOVERNED-CONTROLLED-RUN`; Safe Mode `OPEN`; user movement `0`; Runtime apply `0`.

Engineering Truth Lifecycle:

| Object | Owner / truth | Validity and reuse |
| --- | --- | --- |
| live candidate/runtime state | production planner, registries and snapshots | fresh cycle only; any selected identity or safety change invalidates |
| Decision Fingerprint | `admin_core.operator_execution_pipeline.py` | semantic selected move/action class/verification contract |
| approved plan/source lease | packet/autoswitch owners | reusable only under materially equivalent state; no Authority transfer |
| prior reports | Engineering Reports | historical evidence only; not live truth |

## Churn Reproduction

Authoritative sampler executed 10 cycles without lease, barrier, apply or movement. Cycles 3-4 returned no packet during overlapping refresh/observe timing and are evidence of producer timing contention, not successful decisions.

| Cycles | Selected decision | Decision Fingerprint | Raw bundle behavior | Result |
| --- | --- | --- | --- | --- |
| 1-2 | `10.7.0.32 wireguard-* -> awg0` | stable `9611f5...bb56` | suitability/bundle changed | `AUTHORITY_BOUNDARY` |
| 3-4 | no packet | none | runtime/suitability refresh in progress | read-only return code `2` |
| 5-10 | `10.0.0.2 vless -> awg3` | stable `993972...9d37` | multiple raw suitability/runtime bundle changes | `AUTHORITY_BOUNDARY` |

Decision Replay: identical semantic selected inputs produced identical selected move hash and Decision Fingerprint. `NON_DETERMINISTIC_DECISION=FALSE`. One real material recommendation transition occurred between cycles 2 and 5 and must continue to invalidate an older packet.

## Source Materiality Matrix

| Source / field | Owner | Materiality | Required binding | Churn contribution |
| --- | --- | --- | --- | --- |
| selected user registry row | registry/assignment owner | `STRICT_IDENTITY` | semantic selected row | material |
| selected source/target egress registry rows | egress owner | `STRICT_IDENTITY` | semantic selected rows | material |
| selected user current/desired state | runtime-state owner | `MATERIAL_SAFETY_INPUT` | semantic projection | material |
| source/target code, health, load, speed/stability/load count | runtime-state owner | `MATERIAL_SAFETY_INPUT` | semantic projection | material |
| selected source/target suitability score/confidence/risk/authority | candidate-suitability owner | `MATERIAL_DECISION_INPUT` | semantic projection | material |
| snapshot generated/expires timestamp bytes | snapshot owner | `VOLATILE_NON_MATERIAL` | freshness gate, not exact byte hash | false invalidation contributor |
| handshake-age diagnostic text | runtime observability | `OBSERVABILITY_ONLY` when status unchanged | raw provenance only | false invalidation contributor |
| unrelated users/channels/suitability rows | respective owners | `OBSERVABILITY_ONLY` for this one-user packet | raw provenance only | false invalidation contributor |
| raw whole-file hashes | source owners | `OBSERVABILITY_ONLY` | retained, `execution_binding=false` | prior overbroad binding |

## Root Cause And Existing Mechanisms

`ROOT_CAUSE=MULTIPLE_ROOT_CAUSES`: `REAL_MATERIAL_REALITY_CHANGE` plus `OVERBROAD_SOURCE_BUNDLE`, `VOLATILE_NON_MATERIAL_HASH_INPUT` and refresh-time producer contention. `last_responsible_link=tools/v7-governed-canary-dry-run-cycle::attach_controlled_execution_source_binding -> atomic execution envelope`.

Existing Decision Fingerprint, deterministic selected-move hash, approved-plan-lock, execution lease, source-bundle lease, freshness, anti-flap, stickiness and B19/B20 remain authoritative. No new hold engine, owner, lifecycle or Authority model was created.

## Implementation And Tests

Changed existing owners only:

- `tools/v7-governed-canary-dry-run-cycle`: binding now occurs after selection; selected registry/runtime/suitability projections are hashed; raw hashes remain provenance.
- `admin_core/operator_execution_pipeline.py`: atomic envelope exposes raw observability bundle with `execution_binding=false`.
- `tests/unit/test_governed_canary_cli.py`: non-material stability and material invalidation coverage.

Verification:

```text
focused owner tests = 75 PASS
planner/autoswitch/packet/sync regression = 291 PASS
full unit discovery = 750 PASS
py_compile = PASS
git diff --check = PASS
safe-deploy allowlist = PASS
production mutation = NO
```

## Deploy And Production Certification

Initial deploy `deploy-z8-14-Updatesystem-f96f294-20260711T184730` delivered the semantic source binding at commit `f96f29486bb5df3608e7dc730220277da2dbc397`; direct production hashes matched and repeated safe-deploy returned `deployment_required=false`, truth `PASS`, convergence `FULLY_ALIGNED`.

The first post-deploy 10-cycle series proved cycles 5-8 kept selected move `10.0.0.2 vless -> awg3`, Decision Fingerprint `993972...9d37` and semantic bundle `612ae1...1fc0` while raw snapshots changed. It also exposed one remaining non-authoritative identity defect: `candidate_hash` still included raw recommendation/source hashes and changed for the same semantic candidate. That field is now normalized in the same existing pipeline owner and requires a final deploy/certification pass. No Safe Mode change, active lease, restore barrier, service/timer change, Runtime apply or user movement occurred.

## Behavior Enforcement And State Transition Verification

Expected behavior change is limited to eliminating false packet invalidation from non-material byte drift. Selected identity, material runtime health/load, suitability decision values, action class, safety verdict and rollback/verification readiness remain fail-closed. Initial/final runtime mutation state remains unchanged.

## Work Placement, Scale And Maturity

Work remains inside active `CAP-U01`; no new capability or backlog item. Projection cost is bounded to one selected user and two egress/candidate rows instead of whole-snapshot execution identity, reducing hash payload size while preserving raw provenance. Production Maturity decision remains pending production stability evidence; no manual score edit.

## Parent Intent And Continue OMP

Parent intent remains `INTENT_NOT_CLOSED` until deploy and production stability certification. CPS/OMP synchronization and automatic `Continue OMP` will be performed only after certification, stopping at the next canonical Authority/real-world/safety boundary.
