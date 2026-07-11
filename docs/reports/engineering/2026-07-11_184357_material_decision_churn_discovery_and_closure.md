# Material Decision Churn Discovery And Closure

Дата: `2026-07-11T18:43:57+0700`  
Mission ID: `V7_OMP_MATERIAL_DECISION_CHURN_CLOSURE_V1`  
Статус отчёта: `MATERIAL_DECISION_CHURN_CLOSED_STABILITY_CERTIFIED`

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

Final candidate identity normalization was deployed at commit `62015c156fa2a528b36bdbfb3847f3b9f9ee57c2`, deploy id `deploy-z8-14-Updatesystem-62015c1-20260711T185443`. Repeated safe-deploy returned `deployment_required=false`; truth/convergence were `PASS / FULLY_ALIGNED`.

Final 10-cycle certification:

- cycles 1-4: identical Candidate hash `789344...9d35`, move hash `dea805...8d12` and Decision Fingerprint `518abb...2c16`;
- cycles 2-4: identical semantic bundle `64c57c...791a` while raw suitability snapshots changed;
- later selected-decision switches had distinct selected move, Candidate and Decision fingerprints and therefore remained material/fail-closed;
- no `NON_DETERMINISTIC_DECISION`, unexplained churn, lease, barrier, apply or movement.

Production stability result: `DECISION_STABILITY_CERTIFIED`. False invalidation is removed; material invalidation is preserved.

## Behavior Enforcement And State Transition Verification

Expected behavior change is limited to eliminating false packet invalidation from non-material byte drift. Selected identity, material runtime health/load, suitability decision values, action class, safety verdict and rollback/verification readiness remain fail-closed. Initial/final runtime mutation state remains unchanged.

## Work Placement, Scale And Maturity

Work remains inside active `CAP-U01`; no new capability or backlog item. Projection cost is bounded to one selected user and two egress/candidate rows instead of whole-snapshot execution identity, reducing hash payload size while preserving raw provenance. Production Maturity decision remains pending production stability evidence; no manual score edit.

## Parent Intent And Continue OMP

Engineering Intent is `INTENT_CLOSED`. Automatic `Continue OMP` consumed CPS registry and reran fresh Phase 4A read-only. It reached `OPERATIONAL_AUTHORITY` with `10.0.0.2 vless -> awg0`, packet `pkt_preview_ec8184d73f013b0d0cafe5c6`, decision `decision_commit_518abb7de97b1cbec59f4ac7`, operation `govdry_0eb3bad4dc845bca212eaa98`, selected move hash `dea805...8d12` and bundle `1449da...1768`. No execution authority was granted and no mutation occurred. Active `CAP-U01` remains protected; next action is exact packet approval with final live revalidation.

## Final Verdict

```text
MATERIAL_DECISION_CHURN_CLOSED_STABILITY_CERTIFIED
ARCHITECTURE_CLOSED_BY_DEFAULT = PASS
NEW_OWNER_REQUIRED = NO
CHURN_CYCLES_OBSERVED = 30 bounded cycles plus one automatic Continue OMP cycle
ROOT_CAUSE = MULTIPLE_ROOT_CAUSES
NON_DETERMINISTIC_DECISION = NO
SOURCE_MATERIALITY_RESOLVED = YES
EXISTING_STABILITY_MECHANISMS_REUSED = YES
IMPLEMENTATION_CHANGED = YES; existing coordinator/pipeline owners only
DEPLOY_APPLIED = YES
DEPLOY_ID = deploy-z8-14-Updatesystem-62015c1-20260711T185443
DECISION_REPLAY = PASS
FALSE_INVALIDATION_REMOVED = YES
MATERIAL_INVALIDATION_PRESERVED = YES
PRODUCTION_STABILITY_RESULT = DECISION_STABILITY_CERTIFIED
SAFE_MODE_FINAL_STATE = OPEN
RUNTIME_APPLY = NO
USER_MOVEMENT = NO
PRODUCTION_MATURITY_DECISION = NO_CHANGE; no real movement outcome and no manual score edit
ENGINEERING_INTENT_CLOSURE = INTENT_CLOSED
AUTOMATIC_CONTINUE_OMP_EXECUTED = YES
NEXT_CANONICAL_STOP = OPERATIONAL_AUTHORITY
NEXT_OMP_ACTION = AWAIT_EXACT_OPERATIONAL_AUTHORITY_FOR_FRESH_PACKET_WITH_FINAL_LIVE_REVALIDATION
```
