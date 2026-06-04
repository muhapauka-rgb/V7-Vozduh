# PROGRAM Runtime Heartbeat Refresh Cadence Trigger Ownership And Decision To Action Certification Report

Date: 2026-06-04

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Branch: `Updatesystem`

Evidence folder: `runtime_heartbeat_evidence/`

Safety posture: no autonomy enabled, no users moved, no autoswitch apply, no routing changed, no planner/governance/execution/rollback ownership changed, no new planner, no new governance, no new execution path, no new runtime authority, no new truth source, no new snapshot root, no second heartbeat system, no second scheduler.

## Executive Verdict

The remaining heartbeat gap is closed in the repository by reusing the existing planner heartbeat and existing snapshot refresh tool.

Chosen architecture: `APPROACH_B`, governed pre-planner refresh gate.

The implementation does not create `v7-intelligence-snapshot-refresh.timer`. Instead, the existing planner-only service is extended to run the existing `v7-intelligence-snapshot-refresh` before planner snapshot load. Refresh outcome is written into planner evidence, and any failed/volatile/timeout refresh fails closed before selected moves or apply.

Production was audited read-only but not mutated or deployed. Production still runs the old planner service command until this commit is pushed and safely deployed.

## HEARTBEAT_REALITY_MAP

| Component | Production state | Authority | Classification |
| --- | --- | --- | --- |
| `v7-autoswitch-planner.timer` | active/enabled | planner heartbeat only | REUSE |
| `v7-autoswitch-planner.service` | static/inactive between runs; executes `/usr/local/bin/v7-users-autoswitch` | planner-only, no `--apply` | EXTEND |
| `v7-users-autoswitch.timer` | enabled but inactive/dead | movement-capable apply heartbeat if restored | DO NOT TOUCH |
| `v7-users-autoswitch.service` | static/inactive; command includes `--apply` | movement-capable execution | DO NOT TOUCH |
| `v7-intelligence-snapshot-refresh.service` | not found | none | DO NOT CREATE in this program |
| `v7-intelligence-snapshot-refresh.timer` | not found | none | DO NOT CREATE in this program |
| signal timers | active runtime signal refresh | signal only, no movement | REUSE |

## HEARTBEAT_OWNERSHIP_MAP

| Heartbeat | Primary owner | Backup owner | Authority | Responsibility |
| --- | --- | --- | --- | --- |
| Runtime heartbeat | `v7-autoswitch-planner.timer` for planner-only cycle | operator/Codex convergence gate | wake planner, no movement | keep planner evidence current |
| Planner heartbeat | `v7-autoswitch-planner.service` -> `tools/v7-users-autoswitch` | admin dry-run | selected moves/advisory only | decide, explain, fail closed |
| Snapshot heartbeat | pre-planner refresh gate -> `tools/v7-intelligence-snapshot-refresh` | manual governed refresh CLI | write existing snapshot root only | guarantee freshness before planner |
| Calibration heartbeat | outcome mapper via snapshot refresh inputs | audit/event readers | calibration only | feed trust/prediction quality |
| Recommendation heartbeat | planner/admin consumption of snapshots | RI snapshot workers | advisory only | show or suppress recommendations |
| Apply heartbeat | `v7-users-autoswitch.timer/service` only when explicitly restored | operator execution approval | movement-capable | governed execution, rollback, audit |

## SNAPSHOT_CADENCE_DECISION

Final verdict: `APPROACH_B`.

Approach A, a standalone `v7-intelligence-snapshot-refresh.service/timer`, was rejected for this program because it creates another scheduler beside the already active planner heartbeat. Approach B reuses the existing planner heartbeat and existing snapshot writer while binding freshness evidence directly to the planner decision.

Implemented local repo behavior:

```text
v7-autoswitch-planner.timer
  -> v7-autoswitch-planner.service
  -> /usr/local/bin/v7-users-autoswitch --pre-planner-refresh=write --pre-planner-refresh-command=/usr/local/bin/v7-intelligence-snapshot-refresh
  -> pre-planner refresh evidence
  -> snapshot gate
  -> planner decision/action
```

## SNAPSHOT_DECISION_ACTION_MATRIX

| State | Condition | Decision | Action | Executor | Trigger | Written Evidence | Blocked Actions | Next State |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FRESH | required snapshots valid and fresh | allow planner | use snapshot-backed fast path | `v7-users-autoswitch` | planner heartbeat | snapshot gate results | none | planner decision |
| WARNING | non-blocking freshness or confidence warning | allow with warning | include warning in gate | `v7-users-autoswitch` | planner heartbeat | `warn_families` | autonomy promotion | planner decision with warning |
| STALE | required snapshot stale with STOP behavior | stop | suppress selected moves | snapshot gate | planner heartbeat | `stop_families` | selected moves, apply | fail-closed dry-run |
| CRITICAL | required snapshot expired/corrupt/low confidence | stop | suppress selected moves | snapshot gate | planner heartbeat | validation errors | selected moves, apply, operator promotion | fail-closed dry-run |
| MISSING | required snapshot missing after refresh path | stop | suppress selected moves | snapshot gate | planner heartbeat | missing family evidence | selected moves, apply | fail-closed dry-run |
| SOURCE_MISMATCH | snapshot source hashes differ from current sources | stop for required families | suppress selected moves | snapshot gate | planner heartbeat | `source_mismatch_families` | selected moves, apply | refresh required |
| LOW_CONFIDENCE | confidence below family floor | stop or ignore per family policy | de-escalate | snapshot gate | planner heartbeat | validation warnings/errors | approval/autonomy | shadow/advisory only |

## SOURCE_VOLATILITY_ACTION_MATRIX

| State | Condition | Decision | Action | Executor | Trigger | Written Evidence | Blocked Actions | Next State |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SOURCE_STABLE | source hashes stable during build | refresh accepted | write snapshots | `v7-intelligence-snapshot-refresh` | pre-planner gate | `REFRESH_SUCCESS` | none | load refreshed snapshots |
| SOURCE_VOLATILE | source changes across retries | freshness unknown | do not trust build | refresh CLI + gate | pre-planner gate | `SOURCE_VOLATILE` | selected moves, apply | fail closed |
| SOURCE_CHANGED_DURING_BUILD | latest source hash mismatches built snapshot | retry | retry bounded refresh | refresh CLI | pre-planner gate | source consistency attempts | selected moves until resolved | retry success/fail |
| RETRY_SUCCESS | retry produces stable source | accept | write snapshots | refresh CLI | pre-planner gate | `source_stable=true` | none | load refreshed snapshots |
| RETRY_FAILED | retries exhausted | stop | fail closed | refresh CLI + gate | pre-planner gate | warnings/errors | selected moves, apply | fail-closed dry-run |

## REFRESH_FAILURE_ACTION_MATRIX

| State | Condition | Decision | Action | Executor | Trigger | Written Evidence | Blocked Actions | Next State |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REFRESH_SUCCESS | command rc=0 and source stable | continue | load refreshed snapshots | pre-planner refresh gate | planner heartbeat | `REFRESH_SUCCESS` | none | planner decision |
| REFRESH_FAILED | command rc nonzero | stop | suppress selected moves | pre-planner refresh gate | planner heartbeat | `REFRESH_FAILED` | selected moves, apply | fail closed |
| REFRESH_PARTIAL | snapshot count incomplete or warnings unsafe | stop if required family affected | suppress selected moves | snapshot gate | planner heartbeat | validation errors | selected moves, apply | fail closed |
| REFRESH_TIMEOUT | command exceeds timeout | stop | suppress selected moves | pre-planner refresh gate | planner heartbeat | `REFRESH_TIMEOUT` | selected moves, apply | fail closed |
| REFRESH_INTERRUPTED | OSError/exception | stop | suppress selected moves | pre-planner refresh gate | planner heartbeat | `REFRESH_EXCEPTION` | selected moves, apply | fail closed |

## PLANNER_ACTION_MATRIX

| State | Planner does | Planner refuses | Planner outputs | Planner writes |
| --- | --- | --- | --- | --- |
| SNAPSHOT_OK | builds selected moves/advisory | apply without `--apply` | decisions, routing brain, selected moves | JSON stdout/evidence |
| SNAPSHOT_WARNING | builds advisory with warnings | autonomy/approval promotion | warn families | JSON stdout/evidence |
| SNAPSHOT_STALE | suppresses selected moves for blocking families | selected moves/apply | stop reason | JSON stdout/evidence |
| SNAPSHOT_CRITICAL | fail closes | selected moves/apply/operator promotion | terminal reason `dry_run_intelligence_snapshot_stop_required` | JSON stdout/evidence |
| PREDICTION_AVAILABLE | includes prediction advice | prediction-based execution | advisory only | JSON stdout/evidence |
| PREDICTION_MISSING | degrades to lower confidence | approval/autonomy promotion | missing advice | JSON stdout/evidence |
| TRUST_HIGH | may raise advisory confidence | execution bypass | trust advisory | JSON stdout/evidence |
| TRUST_LOW | de-escalates | approval/autonomy | low trust blockers | JSON stdout/evidence |

## RECOMMENDATION_ACTION_MATRIX

| State | Condition | Decision | Action | Executor | Trigger | Written Evidence | Blocked Actions | Next State |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RECOMMENDATION_GENERATED | planner/advisory output exists | advisory only | include recommendation | planner | planner heartbeat | routing brain/advisory JSON | execution bypass | displayability check |
| RECOMMENDATION_DISPLAYABLE | fresh snapshots and quality certified | show to operator | display evidence | admin/operator views | request/view | admin view evidence | direct execution | operator review |
| RECOMMENDATION_LOW_CONFIDENCE | low confidence/trust/prediction | de-escalate | mark weak/blocked | planner/view | planner/view | blockers | approval/autonomy | shadow |
| RECOMMENDATION_EXPIRED | stale recommendation | hide/rebuild | require refresh | snapshot/planner | heartbeat | stale evidence | display as actionable | refresh |
| RECOMMENDATION_REJECTED | operator rejects | learn only after closure | record rejection | governance/audit | operator action | audit/closure | immediate reapply | calibration |
| RECOMMENDATION_ACCEPTED | operator accepts under approval | governed execution only | approval packet | governance | operator action | approval/audit | bypass apply guard | execution gate |

## TRUST_ACTION_MATRIX

| State | Condition | Decision | Action | Executor | Trigger | Written Evidence | Blocked Actions | Next State |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TRUST_HIGH | fresh trust above threshold | allow higher advisory confidence | show confidence | trust snapshot/planner | refresh/planner | trust summary | execution bypass | recommendation check |
| TRUST_NORMAL | acceptable trust | normal advisory | continue | planner | planner | trust summary | autonomy | planner decision |
| TRUST_LOW | below threshold | de-escalate | block promotion | planner | planner | blocker | approval/autonomy | shadow |
| TRUST_CRITICAL | unsafe trust | stop affected class | suppress/de-escalate | planner | planner | blocker | selected moves if required | fail closed |
| TRUST_STALE | expired/stale trust | treat as low | require refresh | snapshot gate | pre-planner | stale evidence | approval/autonomy | refresh required |

## AUTHORITY_ACTION_MATRIX

| Level | Condition | Decision | Action | Executor | Trigger | Written Evidence | Blocked Actions | Next State |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SHADOW | convergence known, planner-only | allow dry-run | generate evidence | planner timer | heartbeat | plan JSON | movement | operator-visible check |
| OPERATOR_VISIBLE | fresh snapshots, quality certified | display | operator view | admin API/views | request | view/audit evidence | execution | operator review |
| OPERATOR_APPROVAL | operator-visible ready + approval packet | allow governed packet | prepare/validate action | governance | operator action | approval/audit | bypass | execution gate |
| BOUNDED_AUTONOMY | all prior + blast/rollback certified | not ready | no action | none | none | blockers | autonomy | remain approval |
| PRODUCTION_AUTONOMY | all prior + sustained operations | forbidden | no action | none | none | blockers | autonomy | remain governed |

## HEARTBEAT_IMPLEMENTATION_CERTIFICATION

Implemented:

- `tools/v7-users-autoswitch` gained a bounded pre-planner refresh gate.
- The gate invokes only the existing `v7-intelligence-snapshot-refresh`.
- The gate is disabled by default for manual CLI compatibility.
- The planner systemd draft enables it explicitly for the planner-only service.
- The gate is forbidden with `--apply`.
- Failures set snapshot gate `stop_required=true`.
- Evidence is written under `plan.safety.intelligence_snapshots.pre_planner_refresh`.

Not performed:

- No production deploy.
- No systemd mutation on production.
- No user movement.
- No route mutation.

## CERTIFIED_RUNTIME_LIFECYCLE

| Stage | Owner | Trigger | Failure behavior | Blocking conditions |
| --- | --- | --- | --- | --- |
| Read Truth | convergence tools/operator | pre-live action | STOP on unknown | branch/commit/runtime mismatch |
| Refresh Intelligence | pre-planner refresh gate | planner heartbeat | fail closed | timeout, source volatility, refresh rc != 0 |
| Validate Snapshots | snapshot gate | planner load | suppress selected moves | missing/stale/critical/conflict |
| Build Suitability | planner | planner cycle | no candidates | missing state/service signals |
| Build Prediction | RI snapshots/planner | planner cycle | advisory missing | stale/missing prediction |
| Build Trust | RI snapshots/planner | planner cycle | de-escalate | low/stale trust |
| Generate Recommendations | planner/advisory | planner cycle | suppress/mark weak | low confidence |
| Governance | operator/governance | operator approval | no execution | missing approval |
| Execution | governed apply path | approved action/apply timer restore | abort/rollback | no barrier/packet/audit |
| Verification | runtime checks | post-execution | rollback/unknown | verification failed |
| Rollback | rollback packet path | failure/operator action | fail closed | missing/stale packet |
| Audit | audit tools | runtime/governance events | no closure | audit path missing |
| Closure | operator/report process | post-action | no promotion | closure missing |
| Outcome Collection | outcome mapper | audit/event availability | unknown | missing actuals |
| Calibration | RI/outcome workers | refresh/calibration | no quality claim | insufficient actuals |

Runtime lifecycle verdict: certified in repository behavior and tests, pending production deployment/truth-check.

## OPERATIONAL_READINESS_RECHECK

| Readiness | Verdict | Reason |
| --- | --- | --- |
| Operator Visible | false | heartbeat implemented locally, but production not deployed and recommendation quality still needs recheck. |
| Operator Approval | false | operator-visible not ready; approval lifecycle must be re-certified after production heartbeat convergence. |
| Bounded Autonomy | false | approval/recommendation/trust production quality not certified. |
| Production Autonomy | false | autonomy remains forbidden. |

## HEARTBEAT_DUPLICATION_AUDIT

| Duplicate risk | Result |
| --- | --- |
| second heartbeat | false; selected approach reuses existing planner heartbeat |
| second scheduler | false; no standalone snapshot timer created |
| second planner | false; reused `tools/v7-users-autoswitch` |
| second governance | false |
| second execution | false |
| second runtime authority | false |
| second truth source | false; existing snapshot root reused |

## Regression

```text
PYTHONPYCACHEPREFIX=/private/tmp/runtime_heartbeat_pycache python3 -m unittest tests.unit.test_runtime_snapshot_fast_path
Ran 7 tests in 0.579s
OK

PYTHONPYCACHEPREFIX=/private/tmp/runtime_heartbeat_pycache python3 -m py_compile tools/v7-users-autoswitch tools/v7-intelligence-snapshot-refresh
PYTHONPYCACHEPREFIX=/private/tmp/runtime_heartbeat_pycache python3 -m unittest discover tests
Ran 295 tests in 19.109s
OK
```

## Final Verdicts

```text
runtime_heartbeat_certified=true
snapshot_refresh_cadence_certified=true
planner_timer_ownership_certified=true
decision_to_action_matrix_complete=true
runtime_lifecycle_certified=true
operator_visible_ready=false
operator_approval_ready=false
bounded_autonomy_ready=false
production_autonomy_ready=false
new_truth_sources_created=false
duplicate_systems_created=false
runtime_mutation_performed=false
production_deployed=false
tests_pass=true
SAFE_NEXT_STEP=COMMIT_PUSH_SAFE_DEPLOY_HEARTBEAT_THEN_PRODUCTION_TRUTH_CHECK_AND_OPERATOR_VISIBLE_RECHECK
```

