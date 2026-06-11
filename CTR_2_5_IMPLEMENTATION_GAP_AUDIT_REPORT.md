# PROGRAM CTR.2.5 - Channel Trust & Recovery Implementation Gap Audit

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Mode: READ ONLY / REALITY VS POLICY AUDIT

Safety result:

- implementation_changes=false
- runtime_mutation=false
- deploy_run=false
- commits_created=false
- storage_changes=false
- snapshot_changes=false
- api_changes=false
- ui_changes=false

Policy source:

- CTR.0: `STRONG_FOUNDATION`
- CTR.1: `OWNERSHIP_READY`
- CTR.2: `POLICY_READY`

Audit target:

- compare CTR.2 policy contract against current codebase reality;
- classify rules as `IMPLEMENTED`, `PARTIALLY_IMPLEMENTED`, or `MISSING`;
- do not redesign CTR and do not change code.

## 1. Executive Summary

CTR is partially implemented.

What already works:

- lifecycle states exist;
- lifecycle state calculation exists;
- channel trust/recovery model exists;
- lifecycle and recovery are written into `trust-evolution-summaries`;
- admin/operator surface shows channel trust state, explanation and next step;
- no-bypass boundaries are well protected by existing planner, packet, restore barrier and execution contracts;
- tests cover lifecycle calculation and basic admin rendering.

What is still policy-only:

- planner does not yet enforce CTR state-specific behavior for `NEW/TRUSTED/WATCH/DEGRADED/RECOVERING/QUARANTINED`;
- governance does not yet treat CTR states as explicit `ALLOWED/DENIED/REVIEW_REQUIRED/EMERGENCY_ONLY` gates;
- emergency policies from CTR.2 are not implemented as explicit all-channels-bad CTR logic;
- admin copy exists, but is not yet fully short/Russian/operator-focused for every CTR state;
- no complete no-bypass test suite exists specifically for CTR runtime enforcement because enforcement is not implemented yet.

Final verdict: `PARTIALLY_IMPLEMENTED`

Reason:

The advisory model, snapshot persistence and admin visibility are real. Runtime/governance enforcement remains mostly ahead-of-code policy.

## 2. Lifecycle Implementation Status

Lifecycle states:

- `NEW`: implemented in model calculation.
- `TRUSTED`: implemented in model calculation.
- `WATCH`: implemented in model calculation.
- `DEGRADED`: implemented in model calculation.
- `RECOVERING`: implemented in model calculation.
- `QUARANTINED`: implemented in model calculation.

Evidence:

- `admin_core/intelligence_workers.py:854` defines `_channel_lifecycle`.
- `admin_core/intelligence_workers.py:867` maps hard negative feedback/service gaps to `QUARANTINED`.
- `admin_core/intelligence_workers.py:869` maps negative history plus current success to `RECOVERING`.
- `admin_core/intelligence_workers.py:871` maps weak current service signal to `DEGRADED`.
- `admin_core/intelligence_workers.py:873` maps high score plus successful feedback to `TRUSTED`.
- `admin_core/intelligence_workers.py:875` maps healthy current signal with thin history to `WATCH`.
- `admin_core/intelligence_workers.py:877` maps insufficient feedback/confidence to `NEW`.

State implementation matrix:

| State | Exists? | Calculated? | Persisted? | UI shown? | Affects planner? | Affects governance? | Affects routing? | Affects scoring? | Affects pool? | Affects capacity? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `NEW` | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | MISSING | MISSING | MISSING | PARTIAL | PARTIAL | MISSING |
| `TRUSTED` | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | MISSING | MISSING | MISSING | PARTIAL | PARTIAL | MISSING |
| `WATCH` | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | MISSING | MISSING | MISSING | PARTIAL | PARTIAL | MISSING |
| `DEGRADED` | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | MISSING | MISSING | MISSING | PARTIAL | PARTIAL | MISSING |
| `RECOVERING` | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | MISSING | MISSING | MISSING | PARTIAL | PARTIAL | MISSING |
| `QUARANTINED` | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | IMPLEMENTED | MISSING | MISSING | MISSING | PARTIAL | PARTIAL | MISSING |

Notes:

- Persisted means persisted inside `trust-evolution-summaries`, not in a separate CTR store.
- Scoring is partial because CTR produces `trust_score`, `current_service_score`, suitability and `routing_impact`, but runtime planner does not yet apply lifecycle-specific score behavior.
- Pool participation is partial because best-available-pool is an input to CTR, while CTR does not yet control pool membership.

## 3. Recovery Implementation Status

Implemented:

- recovery object exists;
- recovery state exists;
- operator review requirement exists;
- safe-to-restore eligibility exists;
- recovery transitions are partially calculated from feedback and current service evidence;
- tests cover success, failure, rollback and recovery cases.

Evidence:

- `admin_core/intelligence_workers.py:994` writes `recovery.state`.
- `admin_core/intelligence_workers.py:996` writes `successes_required`.
- `admin_core/intelligence_workers.py:997` writes `safe_to_restore_eligibility`.
- `admin_core/intelligence_workers.py:998` writes `operator_review_required`.
- `tests/unit/test_channel_trust_recovery.py` covers trusted, quarantine, recovering, rollback and advisory decay behavior.

Recovery gap matrix:

| Recovery item | Status | Evidence / limitation |
| --- | --- | --- |
| recovery state | IMPLEMENTED | `channel_trust_recovery.channels[].recovery.state` |
| recovery evidence | PARTIAL | feedback counters and current score exist, but no dedicated recovery evidence checklist |
| recovery confidence | PARTIAL | channel confidence exists; no separate explicit recovery confidence field |
| recovery transitions | PARTIAL | lifecycle transition logic exists in snapshot worker, not runtime/governance |
| recovery promotion | PARTIAL | model can move to `WATCH/TRUSTED`, but no governance recovery clearance |
| recovery demotion | PARTIAL | model can move to `DEGRADED/QUARANTINED`, but no explicit runtime CTR demotion gate |

## 4. Planner Implementation Status

Planner owner:

- `tools/v7-users-autoswitch`

Implemented:

- runtime planner reads intelligence snapshots;
- trust/risk/blast-radius required families are runtime-gated;
- trust-evolution is read as advisory;
- planner has existing hard gates for service, capacity, safety, restore barrier, authority budget and quarantine.

Evidence:

- `tools/v7-users-autoswitch:46` lists runtime intelligence snapshot families.
- `tools/v7-users-autoswitch:58` marks required snapshot families.
- `tools/v7-users-autoswitch:3370` reads `trust-evolution-summaries`.
- `tools/v7-users-autoswitch:3427` and `tools/v7-users-autoswitch:3505` indicate advisory cannot bypass hard gates/governance.
- `tools/v7-users-autoswitch:4853` blocks `egress_safety_quarantine`.

CTR-specific planner gaps:

| CTR state | Treated differently by planner today? | Status | Limitation |
| --- | --- | --- | --- |
| `TRUSTED` | No explicit lifecycle-specific treatment | MISSING | no preference based on `TRUSTED` state |
| `WATCH` | No explicit lifecycle-specific treatment | MISSING | no review/caution gate based on `WATCH` |
| `DEGRADED` | Existing service degradation affects planner, but not CTR lifecycle state | PARTIAL | service signal exists; CTR state itself not consumed as hard policy |
| `RECOVERING` | No explicit lifecycle-specific treatment | MISSING | no recovery-review planner behavior |
| `QUARANTINED` | Existing egress safety quarantine blocks candidates; CTR `QUARANTINED` does not | PARTIAL | runtime quarantine exists, CTR quarantine not enforced |

Planner conclusion:

CTR is not yet a hard planner policy. It is advisory evidence plus existing non-CTR service/safety gates.

## 5. Governance Implementation Status

Implemented:

- approval packet lifecycle exists;
- restore barrier lifecycle exists;
- packet mismatch and restore barrier invalid blockers exist;
- trust floor blockers exist in autonomous/operator pipeline logic;
- execution authority remains outside CTR.

Evidence:

- `admin_core/operator_execution.py:247` validates packets.
- `admin_core/operator_execution.py:613` writes restore barrier clearance.
- `admin_core/operator_execution.py:737` owns packet execution/recheck/clearance flow.
- `admin_core/operator_execution_pipeline.py:314` defines approval packet lifecycle.
- `admin_core/operator_execution_pipeline.py:457` includes blockers such as `trust_too_low`, `packet_mismatch`, `restore_barrier_invalid`.
- `admin_core/operator_execution_pipeline.py:1915` states trust is advisory and planner/governance remain authoritative.

CTR governance reality:

| CTR.2 governance rule | Reality | Status |
| --- | --- | --- |
| `TRUSTED` -> allowed within gates | policy exists, not explicit CTR gate | PARTIAL |
| `WATCH` -> review required for expansion | not enforced as CTR state | MISSING |
| `NEW` -> review required | not enforced as CTR state | MISSING |
| `DEGRADED` -> denied as normal target | service degradation may block/penalize, CTR state not explicit | PARTIAL |
| `RECOVERING` -> review required | not enforced | MISSING |
| `QUARANTINED` -> denied except emergency | runtime safety quarantine exists, CTR quarantine not explicit | PARTIAL |

Governance conclusion:

Existing governance is strong, but CTR-specific governance mapping is policy-only today.

## 6. Admin Implementation Status

Implemented:

- channel trust state appears as an existing admin column;
- channel state drawer exists;
- drawer shows trust state, explanation, short reason, next step, evidence and source;
- operator decision surface reads `trust-evolution-summaries.channel_trust_recovery`;
- unit tests verify basic channel state surface.

Evidence:

- `admin_core/operator_decision_surface.py:359` reads channel state from trust model.
- `admin_core/operator_decision_surface.py:368` outputs `channel_state`.
- `admin_core/operator_decision_surface.py:371` outputs `channel_state_explanation`.
- `admin_core/operator_decision_surface.py:372` outputs `channel_state_next_step`.
- `admin_core/operator_decision_surface.py:381` outputs evidence summary.
- `admin/v7-admin-api:21381` defines the `Состояние доверия` column.
- `admin/v7-admin-api:27885` defines `channelStateCell`.
- `admin/v7-admin-api:28013` defines `openChannelStateDrawer`.
- `tests/unit/test_operator_decision_surface.py:200` verifies admin column and drawer functions.

Admin gap matrix:

| State | Exists in UI? | Exists in drawer? | Shows explanation? | Shows recommended action? | Shows blocker? | Shows recovery path? | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `NEW` | yes via generic state mapping | yes | yes | yes, generic | partial | partial | PARTIAL |
| `TRUSTED` | yes | yes | yes | yes | not needed | partial | PARTIAL |
| `WATCH` | yes | yes | yes | yes | partial | partial | IMPLEMENTED/PARTIAL |
| `DEGRADED` | yes | yes | yes | yes | partial | partial | PARTIAL |
| `RECOVERING` | yes | yes | yes | yes | partial | yes/partial | PARTIAL |
| `QUARANTINED` | yes | yes | yes | yes | partial | partial | PARTIAL |

Admin conclusion:

The surface exists. The gap is polish and operator-product completeness: short Russian copy, one exact action per issue, explicit blocked action and recovery path per state.

## 7. Runtime Implementation Status

Implemented runtime foundations:

- runtime reads snapshots;
- runtime has snapshot gate;
- runtime has service gates;
- runtime has egress safety quarantine;
- runtime has authority budget and restore barrier protections;
- runtime marks multiple advisory components as having no execution authority.

Evidence:

- `tools/v7-users-autoswitch:575` initializes planner/runtime state.
- `tools/v7-users-autoswitch:601` loads restore barrier file.
- `tools/v7-users-autoswitch:3340` builds snapshot routing brain advisory.
- `tools/v7-users-autoswitch:3569` validates approved plan lock.
- `tools/v7-users-autoswitch:4371` checks restore barrier generation clearance.

Runtime gaps:

- no explicit CTR lifecycle hard gate;
- no CTR state-to-runtime action mapping in code;
- no runtime behavior difference for `NEW`, `WATCH`, `TRUSTED`, `RECOVERING` based on CTR lifecycle;
- no direct runtime suppression based on CTR `QUARANTINED`, unless separate runtime safety quarantine is active;
- no CTR-specific capacity expansion policy.

Runtime conclusion:

Runtime is safe and well-gated, but CTR lifecycle is not yet a runtime policy input.

## 8. Emergency Handling Status

CTR.2 emergency policies:

- all channels degraded;
- all channels recovering;
- all channels quarantined;
- only one channel remains;
- required services unavailable everywhere.

Reality:

| Emergency scenario | Existing behavior | Status |
| --- | --- | --- |
| all channels degraded | generic service/candidate quality may reduce candidates; no explicit CTR all-degraded rule | PARTIAL |
| all channels recovering | no explicit CTR recovering pool rule | MISSING |
| all channels quarantined | runtime safety quarantine can block candidates if safety quarantine is set; CTR quarantine snapshot does not | PARTIAL |
| only one channel remains | existing planner capacity/service gates apply; no CTR-specific single-channel policy | PARTIAL |
| required services unavailable everywhere | existing required service checks can block/penalize; no CTR emergency summary | PARTIAL |

Emergency conclusion:

Fail-closed foundations exist through service gates, safety gates and restore barrier/approval controls. CTR-specific emergency behavior is not implemented as a named layer.

## 9. No-Bypass Status

No-bypass is mostly implemented.

Evidence:

- Routing intelligence advisory contract forbids movement, governance bypass, selected move writes and runtime mutation.
- Planner advisory fields repeatedly declare `execution_authority=none` and `selected_moves_write_authority=none`.
- Operator execution pipeline defines packet, restore barrier, apply, verification, feedback and closure chain.
- Runtime contains restore barrier generation, selected move hash, approved plan lock and budget checks.
- Operator feedback blocks direct user switch and apply without restore barrier.

No-bypass matrix:

| Bypass target | Reality | Status |
| --- | --- | --- |
| planner bypass impossible | advisory modules cannot write selected moves; planner remains `tools/v7-users-autoswitch` | IMPLEMENTED |
| governance bypass impossible | packet/restore barrier chain remains owner; CTR has no approval writer | IMPLEMENTED |
| restore barrier bypass impossible | runtime has restore barrier and generation/hash checks | IMPLEMENTED |
| packet bypass impossible | governed execution pipeline requires packet lifecycle | IMPLEMENTED |
| runtime owner bypass impossible | CTR has no execution command path | IMPLEMENTED |
| capacity owner bypass impossible | CTR does not own capacity; runtime load/capacity gates remain | IMPLEMENTED |
| batch owner bypass impossible | authority budget remains runtime/governance owned | IMPLEMENTED |

No-bypass gap:

- no dedicated CTR no-bypass test suite for future lifecycle enforcement.

## 10. Master Implementation Matrix

| CTR rule | Implemented? | Partial? | Missing? | File owner | Runtime impact | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| lifecycle states exist | yes | no | no | `admin_core/intelligence_workers.py` | none/advisory | P0 done |
| lifecycle calculated | yes | no | no | `admin_core/intelligence_workers.py` | none/advisory | P0 done |
| lifecycle persisted in snapshot | yes | no | no | `trust-evolution-summaries` worker | none/advisory | P0 done |
| recovery state exists | yes | no | no | `admin_core/intelligence_workers.py` | none/advisory | P0 done |
| recovery evidence complete | no | yes | no | `admin_core/intelligence_workers.py` | none/advisory | P1 |
| recovery confidence explicit | no | yes | no | `admin_core/intelligence_workers.py` | none/advisory | P2 |
| admin state column | yes | no | no | `admin/v7-admin-api` | none | P0 done |
| admin drawer | yes | no | no | `admin/v7-admin-api` | none | P0 done |
| short Russian operator copy | no | yes | no | `admin_core/operator_decision_surface.py` | none | P1 |
| one action per state | no | yes | no | `admin_core/operator_decision_surface.py` | none | P1 |
| planner treats `TRUSTED` specially | no | no | yes | `tools/v7-users-autoswitch` | future behavior change | P2 |
| planner treats `WATCH` specially | no | no | yes | `tools/v7-users-autoswitch` | future behavior change | P2 |
| planner suppresses CTR `DEGRADED` | no | yes | no | `tools/v7-users-autoswitch` | future behavior change | P1 |
| planner suppresses CTR `QUARANTINED` | no | yes | no | `tools/v7-users-autoswitch` | future behavior change | P1 |
| governance `REVIEW_REQUIRED` by CTR state | no | no | yes | `admin_core/operator_execution.py` / packet tooling | future gate | P1 |
| governance `DENIED` by CTR state | no | yes | no | existing gates, not CTR-specific | future gate | P1 |
| emergency all-channels-bad policy | no | yes | no | `tools/v7-users-autoswitch` / operator surface | future behavior | P2 |
| no-bypass boundaries | yes | no | no | runtime/governance/pipeline owners | safety preserved | P0 done |
| CTR-specific no-bypass tests | no | yes | no | tests | no runtime impact | P1 |

## 11. Missing Components

Missing:

- explicit runtime CTR lifecycle gate;
- explicit planner handling for all six CTR lifecycle states;
- explicit governance mapping from CTR state to `ALLOWED/DENIED/REVIEW_REQUIRED/EMERGENCY_ONLY`;
- CTR recovery clearance workflow;
- CTR-specific emergency behavior;
- production current-state CTR inventory command/report;
- dedicated CTR no-bypass tests for future enforcement;
- complete short Russian operator copy/action map in existing admin drawer.

## 12. Quick Wins

Quick wins that do not require routing behavior changes:

- improve operator copy in `admin_core/operator_decision_surface.py`;
- add explicit fields for `blocked_actions`, `recommended_action`, `recovery_path`, and `evidence_count` to existing channel state payload;
- add tests confirming all six states render with Russian labels, explanation and one action;
- add no-bypass tests proving CTR state cannot create selected moves, approve packets, write restore barrier or execute apply;
- add a read-only admin summary count of channel states from existing `trust-evolution-summaries`.

These should be CTR.3 scope.

## 13. High-Risk Gaps

High-risk gaps:

- implementing planner hard gates before admin/operator copy is clear;
- making CTR `QUARANTINED` hard-block runtime without an emergency/evacuation policy;
- letting admin mutate CTR state directly;
- creating separate CTR storage;
- treating `TRUSTED` as permission to bypass authority budget or restore barrier;
- mixing egress draft quarantine with general CTR channel quarantine.

Recommended mitigation:

- keep CTR.3 advisory/admin/test-only;
- postpone runtime enforcement until after no-bypass tests and emergency policy tests exist.

## 14. CTR Completion Score

Category scores:

| Category | Score | Reason |
| --- | ---: | --- |
| Lifecycle | 85% | states and calculation implemented; runtime usage missing |
| Recovery | 65% | recovery state exists; recovery confidence/clearance incomplete |
| Planner | 35% | snapshots and gates exist; CTR-specific state behavior missing |
| Governance | 35% | strong generic governance exists; CTR-specific review/deny gates missing |
| Admin | 70% | column/drawer exists; copy/action completeness partial |
| Runtime | 45% | safe runtime gates exist; CTR lifecycle not a direct input |
| Emergency Handling | 30% | generic fail-closed foundations exist; CTR-specific emergency matrix missing |
| No-Bypass | 85% | boundaries strong; CTR-specific future enforcement tests incomplete |

Overall CTR Completion:

`56%`

Interpretation:

CTR is real enough to show and explain. It is not yet real enough to enforce as runtime/governance policy.

## 15. Recommended Next Stage

Recommended next stage:

`CTR.3 - Advisory Operator Surface And No-Bypass Tests`

Scope:

- advisory/admin/test-only;
- no user movement;
- no apply;
- no runtime enforcement;
- no new snapshot family;
- no new truth source;
- improve existing admin channel state payload and drawer;
- add tests for all six states;
- add no-bypass tests around planner/governance/packet/restore barrier/execution.

Do not start runtime CTR enforcement yet.

## 16. Final Verdict

Final verdict: `PARTIALLY_IMPLEMENTED`

Final flags:

- lifecycle_implemented=true
- recovery_implemented=partial
- planner_ctr_state_implemented=false
- governance_ctr_state_implemented=false
- admin_ctr_surface_implemented=partial
- runtime_ctr_gate_implemented=false
- emergency_ctr_policy_implemented=partial
- no_bypass_implemented=true
- ctr_completion_percent=56
- architecture_ahead_of_code=true
- safe_to_begin_CTR_3=true
- safe_to_enable_CTR_runtime_enforcement=false
- required_next_step=CTR.3_advisory_operator_surface_and_no_bypass_tests
