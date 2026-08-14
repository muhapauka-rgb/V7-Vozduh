# PROGRAM CTR.1 - Canonical Channel Trust & Recovery Ownership And Policy Mapping

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Mode: READ ONLY / POLICY MAPPING ONLY

Safety result:

- implementation_changes=false
- runtime_mutation=false
- deploy_run=false
- commits_created=false
- storage_changes=false
- snapshot_changes=false
- api_changes=false
- ui_changes=false
- new_models_created=false
- new_truth_sources_created=false

Input basis:

- CTR.0 verdict: `STRONG_FOUNDATION`
- CTR.0 rule: do not build a new CTR system
- Existing CTR foundation: `ServiceHistoryStore`, `ExecutionTrustModel`, `trust-summaries`, `risk-summaries`, `blast-radius-summaries`, `trust-evolution-summaries`, `channel_trust_recovery`, operator channel trust UI, runtime trust guards

## 1. Executive Summary

CTR ownership is ready enough to proceed to a controlled design stage, but not ready for runtime enforcement changes yet.

Canonical decision:

- CTR truth should be owned by the existing intelligence snapshot chain.
- The canonical CTR advisory source is `trust-evolution-summaries.channel_trust_recovery`.
- CTR must not create a second trust score, lifecycle model, recovery model, planner, governance path, runtime authority, or snapshot family.
- Runtime authority remains with `tools/v7-users-autoswitch`.
- Governance authority remains with the existing approval packet, restore barrier, and governed execution pipeline.
- Admin/operator visibility remains with `admin_core/operator_decision_surface.py` and existing admin surfaces.

Final verdict: `OWNERSHIP_READY`

Reason:

The authoritative owner and read/write boundaries are clear. Remaining work is policy hardening: mapping CTR lifecycle states into explicit planner/governance behavior and operator actions before any implementation.

## 2. Canonical Ownership Map

Full ownership chain:

`Raw Data -> Worker -> Snapshot -> Runtime -> Admin -> Operator`

| Layer | Canonical owner | Existing component | Writes? | Reads? | Authority |
| --- | --- | --- | --- | --- | --- |
| Raw service truth | Runtime state producers | `service-matrix.json`, `egress-quality-summary.json`, `egress.registry`, `users.registry` | yes, outside CTR | yes | runtime truth only |
| Raw execution history | Runtime/audit/closure owners | switch history, rollback history, audit/closure records | yes, outside CTR | yes | event truth only |
| Service history read model | RI.1 | `ServiceHistoryStore` | no runtime writes | yes | read-only intelligence |
| Trust model | RI.1 / PERF.3 worker | `ExecutionTrustModel`, trust worker | snapshot writes only | yes | advisory/trust guard input |
| Risk model | PERF.3 worker | risk worker | snapshot writes only | yes | required runtime guard input |
| Recovery/lifecycle model | RI6 trust evolution worker | `build_channel_trust_recovery_model()` | snapshot writes only | yes | advisory CTR truth |
| Snapshot store | Intelligence snapshot contract | `admin_core/intelligence_snapshots.py` | atomic snapshot writes by workers | runtime/admin read | truth envelope |
| Runtime planner | Runtime owner | `tools/v7-users-autoswitch` | selected move/apply writes only when governed apply is explicitly invoked | reads compact snapshots | final planner/runtime authority |
| Governance | Operator execution owner | `admin_core/operator_execution.py`, `tools/v7-operator-execution-packet` | packet/restore barrier/audit writes | reads planner packet and runtime state | approval/clearance authority |
| Admin surface | Operator surface owner | `admin_core/operator_decision_surface.py`, `admin/v7-admin-api` | no CTR writes in read views | reads snapshots | operator visibility |
| Operator | Human approval | admin UI workflow | approves bounded action only | sees state/action/evidence | final human approval where required |

Authoritative owners:

| Object | Authoritative owner | Canonical truth source | Writer | Reader |
| --- | --- | --- | --- | --- |
| trust | `trust-summaries` worker / `ExecutionTrustModel` | audit/switch/rollback history -> `trust-summaries.json` | intelligence worker | runtime planner, admin |
| recovery | RI6 trust evolution worker | `trust-evolution-summaries.channel_trust_recovery.recovery` | intelligence worker | admin/operator, future runtime policy reader |
| lifecycle state | RI6 trust evolution worker | `trust-evolution-summaries.channel_trust_recovery.channels[].lifecycle` | intelligence worker | admin/operator |
| recovery state | RI6 trust evolution worker | `channel_trust_recovery.channels[].recovery.state` | intelligence worker | admin/operator |
| trust score | RI6 trust evolution worker for channel-level score; trust worker for global execution trust | `channel_trust_recovery.channels[].trust_score`; `trust-summaries` | intelligence worker | admin/runtime advisory |
| recovery confidence | RI6 trust evolution worker | current confidence fields and evidence confidence | intelligence worker | admin/operator |
| recovery evidence | audit/switch/rollback/service truth owners | decision records, service scores, candidate suitability, best pool | existing producers | intelligence worker, admin |

Evidence:

- `admin_core/intelligence_snapshots.py:350` defines runtime snapshot read contract.
- `admin_core/intelligence_snapshots.py:422` maps snapshot families to required inputs.
- `admin_core/intelligence_workers.py:900` builds `channel_trust_recovery`.
- `tools/v7-users-autoswitch:575` owns runtime planner state loading.
- `admin_core/operator_execution.py:737` owns packet execution/recheck/clearance flow.
- `admin_core/operator_decision_surface.py:346` reads channel trust rows from trust evolution.

## 3. Trust Ownership

Canonical trust ownership:

- global execution trust: `ExecutionTrustModel` and `trust-summaries`;
- channel-level trust: `trust-evolution-summaries.channel_trust_recovery.channels[].trust_score`;
- operator trust display: `operator_decision_surface`;
- runtime trust guard: `tools/v7-users-autoswitch`, reading `trust-summaries` as required intelligence input.

Trust must not be recalculated in runtime from raw history. Runtime may read compact snapshots only. This is already supported by `runtime_read_contract()`, which says planner may read snapshot files and must never read raw history, large JSONL logs, service probe commands, prediction engines, SQLite rollups, network probes, or admin overview recomputation.

Policy:

- Trust score is evidence, not authority.
- Trust score may influence planner scoring only through existing snapshot/advisory paths.
- Trust score must not bypass hard service, capacity, governance, restore barrier, or authority budget gates.

## 4. Recovery Ownership

Canonical recovery owner:

- `admin_core.intelligence_workers.trust-evolution-summaries`

Canonical recovery truth:

- `trust-evolution-summaries.channel_trust_recovery.channels[].recovery`

Existing recovery fields:

- `state`
- `successes_required`
- `safe_to_restore_eligibility`
- `operator_review_required`

Recovery policy:

- `RECOVERING` means current evidence improved after negative history.
- `safe_to_restore_eligibility=true` is advisory until a future governed runtime policy explicitly adopts it.
- Recovery must be proven by fresh service score, sufficient confidence, no hard service gaps, and successful/clean channel feedback.
- Recovery must never directly write selected moves or runtime state.

## 5. Lifecycle Ownership

Canonical lifecycle owner:

- `build_channel_trust_recovery_model()` in `admin_core/intelligence_workers.py`

Canonical lifecycle states:

- `NEW`
- `TRUSTED`
- `WATCH`
- `DEGRADED`
- `RECOVERING`
- `QUARANTINED`

Existing lifecycle calculation evidence:

- `admin_core/intelligence_workers.py:854` defines `_channel_lifecycle`.
- `admin_core/intelligence_workers.py:867` sends hard negative evidence/service gaps to `QUARANTINED`.
- `admin_core/intelligence_workers.py:869` sends improved channel after failures to `RECOVERING`.
- `admin_core/intelligence_workers.py:871` sends weak current service signal to `DEGRADED`.
- `admin_core/intelligence_workers.py:873` sends high score plus successful channel feedback to `TRUSTED`.
- `admin_core/intelligence_workers.py:875` sends healthy but thin history to `WATCH`.
- `admin_core/intelligence_workers.py:877` sends insufficient feedback/confidence to `NEW`.

## 6. Runtime Ownership

Runtime owner:

- `tools/v7-users-autoswitch`

Runtime responsibilities:

- read runtime truth;
- validate snapshot gate;
- enforce hard service, capacity, safety, restore barrier, authority budget and governance constraints;
- produce selected moves in dry-run/planning;
- execute governed apply only when explicitly invoked through existing approval flow.

CTR responsibilities inside runtime:

- today: read trust/risk/blast-radius required snapshots and trust-evolution advisory snapshot;
- future: may consume CTR lifecycle as policy input only through existing snapshot gate;
- never: become a second trust calculator, recovery worker, governance path, or UI fix owner.

Runtime evidence:

- `tools/v7-users-autoswitch:46` lists runtime intelligence snapshot families.
- `tools/v7-users-autoswitch:58` marks `service-scores`, `channel-service-scores`, `risk-summaries`, `trust-summaries`, `blast-radius-summaries` as required.
- `tools/v7-users-autoswitch:3370` reads trust evolution as advisory advice.

## 7. Planner Mapping

Planner owner:

- `tools/v7-users-autoswitch`

Planner treatment by CTR state:

| State | Can place new users there? | Can keep existing users there? | Can evacuate users? | Can propose it? | Can score it? | Emergency only? | Ignore? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `NEW` | Review required | Yes if already there and hard gates pass | Yes if better target exists | Yes, low confidence/advisory only | Yes, capped or neutral | No | No |
| `TRUSTED` | Yes within governance/authority limits | Yes | Yes if another target is better or current degrades | Yes | Yes, normal scoring | No | No |
| `WATCH` | Yes with operator attention and normal gates | Yes | Yes if degradation appears | Yes | Yes, neutral/cautious | No | No |
| `DEGRADED` | No for normal routing | Temporary keep only if no safer target and current assignment is already there | Yes, preferred when safe target exists | Avoid as target | Score as penalty/avoid | Possible emergency fallback only | No |
| `RECOVERING` | Review required | Yes if already there and current hard gates pass | Yes if recovery fails | Yes only with operator review | Yes, cautious/reduced | Possible | No |
| `QUARANTINED` | No | No normal keep; keep only until evacuation/rollback can safely execute | Yes, preferred when safe target exists | No normal proposal | No normal positive score | Emergency only as last resort | No, must show blocker |

Planner rule:

CTR state may narrow or warn about choices, but must not bypass existing hard gates. Hard service/capacity/governance/safety gates dominate CTR optimism.

## 8. Governance Mapping

Governance owner:

- approval packet and restore barrier chain: `admin_core/operator_execution.py` and `tools/v7-operator-execution-packet`

Governance treatment by CTR state:

| State | Governance result | Why |
| --- | --- | --- |
| `NEW` | Review Required | Current checks may pass, but successful governed channel history is thin. |
| `TRUSTED` | Allowed | Recent checks and governed feedback are good, within existing authority budget and packet rules. |
| `WATCH` | Review Required for expansion, Allowed for bounded low-risk moves | Works now, but trust history is still thin. |
| `DEGRADED` | Denied for normal target selection, Review Required for evacuation/temporary keep | Current quality or required services are weak. |
| `RECOVERING` | Review Required | Negative history exists, current signal improved, recovery must be watched. |
| `QUARANTINED` | Denied except emergency evacuation/rollback | Hard negative evidence, repeated failures, rollback failure, missing required services, or very low current quality. |

Governance invariant:

CTR cannot approve execution. It can only provide evidence used by the existing approval packet and restore barrier lifecycle.

## 9. Operator Mapping

Operator surface owner:

- `admin_core/operator_decision_surface.py`
- existing admin UI in `admin/v7-admin-api`

Operator output by state:

| State | State label | Short explanation | Recommended action | Blocked actions | Recovery status | Confidence | Evidence count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `NEW` | New / New channel | Not enough successful channel history yet | Observe, keep bounded, collect successful feedback | blind batch routing | not needed or pending | low/unknown | service + suitability evidence, little/no success feedback |
| `TRUSTED` | Trusted | Recent checks and governed feedback are good | Normal monitored use | bypass governance | not needed | medium/high | service + feedback success evidence |
| `WATCH` | Watch | Works now, trust history still thin | Use with attention, collect more outcomes | large blind expansion | not needed or pending | medium | current service evidence, thin success history |
| `DEGRADED` | Degraded | Current quality or required services are weak | Refresh checks, inspect failing service, avoid as target | normal target selection | blocked until current evidence improves | low/medium | low service/current health evidence |
| `RECOVERING` | Recovering | Was bad before, current checks improve | Continue observation, require operator review | automatic full restore | in progress | medium | negative history + improving current evidence |
| `QUARANTINED` | Quarantined | Hard negative evidence or service gap | Fix underlying service/runtime issue, refresh checks, wait for recovery evidence | new placements and normal routing | blocked/review | low | failures/gaps/rollback failure |

Operator UX policy:

- show short Russian text;
- show one problem, one recommended action;
- if fixable from admin, open one focused modal for that exact issue;
- do not expose raw CTR internals as primary copy;
- keep raw evidence available in details/drawer.

## 10. Recovery Mapping

Recovery state source:

- `trust-evolution-summaries.channel_trust_recovery.channels[].recovery`

Recovery by lifecycle state:

| State | Enters state when | Exits state when | Required evidence | Time windows | Confidence | Safety gates |
| --- | --- | --- | --- | --- | --- | --- |
| `NEW` | insufficient live feedback and low confidence | current evidence improves to `WATCH`, or successful feedback promotes to `TRUSTED` | service score, suitability, at least current checks | current health + short observation | confidence >= 0.35 for `WATCH` | snapshot gate, service gate |
| `TRUSTED` | high current score, enough confidence, successful feedback | service degradation, failures, missing required services, rollback failure | service score >= high floor, confidence, success feedback | current + recent + practical trust window | confidence >= 0.45 plus success | all normal runtime/governance gates |
| `WATCH` | current service looks healthy but history is thin | success feedback to `TRUSTED`, degradation to `DEGRADED`, hard failure to `QUARANTINED` | current score, confidence, no hard gaps | 24-72h observation target; max practical trust window 7 days | confidence >= 0.35 | normal gates plus operator attention |
| `DEGRADED` | verdict not OK, required service low, current score below floor | stable improved current score and no hard gaps to `RECOVERING` or `WATCH` | refreshed service matrix and quality summary | current health and recent stability | enough to prove current signal is real | deny normal placement |
| `RECOVERING` | negative history plus current success/improved signal | enough successful observations to `WATCH`/`TRUSTED`, or new failure to `QUARANTINED` | clean current checks plus successful feedback | 24-72h or two successful observations | medium | operator review required |
| `QUARANTINED` | rollback failure, repeated failures, missing required services, very low score | underlying issue fixed, current service evidence clean, recovery evidence appears | fix evidence, refreshed checks, no repeated failure, recovery observations | no automatic fixed time; evidence-driven | must be sufficient for review | deny normal placement |

## 11. State Transition Matrix

| From | Condition | To |
| --- | --- | --- |
| `NEW` | current_score >= 75 and confidence >= 0.35 | `WATCH` |
| `NEW` | current_score >= 80 and confidence >= 0.45 and successes >= 1 | `TRUSTED` |
| `NEW` | required_missing, repeated failures, rollback failure, or current_score < 45 | `QUARANTINED` |
| `TRUSTED` | verdict not OK, required_low, or current_score < 60 | `DEGRADED` |
| `TRUSTED` | repeated failures, rollback failure, required_missing, or current_score < 45 | `QUARANTINED` |
| `WATCH` | successful channel feedback with high score/confidence | `TRUSTED` |
| `WATCH` | service signal below floor | `DEGRADED` |
| `WATCH` | hard negative evidence/service gap | `QUARANTINED` |
| `DEGRADED` | current improves after negative history and last outcome success | `RECOVERING` |
| `DEGRADED` | current improves with no hard negative evidence but thin history | `WATCH` |
| `DEGRADED` | repeated failures/service gap | `QUARANTINED` |
| `RECOVERING` | enough success observations and high current score | `WATCH` or `TRUSTED` |
| `RECOVERING` | new failure or rollback failure | `QUARANTINED` |
| `QUARANTINED` | underlying issue fixed and clean recovery evidence collected | `RECOVERING` |

Current implementation note:

Existing `_channel_lifecycle()` already encodes several of these transitions as read-only/advisory logic. This report does not change those rules.

## 12. Decision To Action Matrix

| State | Condition | Decision | Action | Executor | Evidence | Next State |
| --- | --- | --- | --- | --- | --- | --- |
| `NEW` | insufficient live feedback | observe | collect service checks and governed outcome evidence | intelligence workers + operator | service snapshot, candidate suitability, feedback count | `WATCH` or `TRUSTED` |
| `NEW` | hard negative evidence appears | block | mark not usable for normal routing | existing CTR snapshot chain | missing services/failures | `QUARANTINED` |
| `TRUSTED` | healthy and within gates | allow | normal governed routing may proceed | planner + governance | trust score, service score, successful feedback | `TRUSTED` |
| `TRUSTED` | degradation appears | review | reduce preference and inspect current service truth | planner/admin/operator | required_low/verdict/current_score | `DEGRADED` |
| `WATCH` | healthy but thin history | cautious allow | allow bounded/reviewed use, collect feedback | planner + operator | current score/confidence/thin feedback | `TRUSTED` |
| `WATCH` | failure or service gap | block/review | avoid as target and inspect | planner/admin/operator | failure/service gap | `DEGRADED` or `QUARANTINED` |
| `DEGRADED` | current service below floor | deny normal placement | refresh checks, inspect failing service | operator/admin approved diagnostics | service matrix, quality summary | `RECOVERING` or `WATCH` |
| `DEGRADED` | users already there | evacuate if safe | planner may propose evacuation to healthier target | planner/governance | selected move packet | `RECOVERING` or `QUARANTINED` |
| `RECOVERING` | improved current signal after negative history | review | observe 24-72h or collect two successful observations | operator + intelligence worker | clean current checks, success feedback | `WATCH` or `TRUSTED` |
| `RECOVERING` | new failure | block | stop normal use and inspect issue | operator/admin | failure/rollback evidence | `QUARANTINED` |
| `QUARANTINED` | hard negative evidence | deny | fix underlying service/runtime issue; no normal routing | operator/admin targeted action | failure/gap/rollback evidence | `RECOVERING` after fix evidence |
| `QUARANTINED` | emergency only | emergency review | evacuate/rollback through existing governed path | governance/runtime executor | approved packet/rollback manifest | `RECOVERING` or remain `QUARANTINED` |

## 13. Window Analysis

Current Health Window:

- Supported.
- Existing implementation uses current service matrix, quality summary, freshness, speed and stability fields.
- Runtime loads `service-matrix.json`, `egress-quality-summary.json`, speed, load and service truth files.

Recent Stability Window:

- Partially supported.
- Existing service history supports `1h` and `24h` windows.
- Operator copy already references 24-72h recovery observation.
- Gap: no final canonical CTR policy states exactly when 24h/72h evidence is sufficient for runtime policy.

Long-Term Trust Window:

- Partially supported.
- `ServiceHistoryStore` supports `7d` and `30d`.
- Operator channel state policy caps practical trust window at 7 days.
- Gap: 7d/30d are used as intelligence context, not yet formally mapped into governance decisions.

Window verdict:

- current_health_window=SUPPORTED
- recent_stability_window=PARTIAL
- long_term_trust_window=PARTIAL

## 14. Duplication Safety Review

This ownership model does not create:

- second trust score: false
- second lifecycle: false
- second recovery model: false
- second planner: false
- second governance path: false
- second runtime authority: false
- second snapshot family: false

Duplication safety certification:

| Risk | Result | Reason |
| --- | --- | --- |
| duplicate trust score | SAFE | uses `trust-summaries` and `channel_trust_recovery.trust_score` |
| duplicate lifecycle | SAFE | uses existing CTR lifecycle states |
| duplicate recovery model | SAFE | uses existing `recovery` object in trust evolution |
| duplicate planner | SAFE | planner remains `tools/v7-users-autoswitch` |
| duplicate governance | SAFE | packet/restore barrier owners unchanged |
| duplicate runtime authority | SAFE | runtime owner unchanged |
| duplicate snapshot family | SAFE | no new snapshot family proposed |

Highest risk if future implementation ignores this report:

- creating a new `channel-trust.json` or separate CTR database would be a HIGH-risk duplicate truth source;
- adding planner logic that recomputes CTR from raw logs would violate the snapshot read contract;
- adding admin actions that directly mutate channel state would bypass the existing worker/snapshot/runtime ownership chain.

## 15. Missing Policy Gaps

Remaining gaps before implementation:

- no final runtime policy contract for whether `DEGRADED`, `RECOVERING`, and `QUARANTINED` become hard gates or advisory penalties;
- no canonical recovery clearance packet/checklist yet;
- no explicit policy for emergency-only use of `QUARANTINED` channels;
- no final Russian operator copy standard for each state/action;
- no one-click focused admin action mapping for each state;
- no tests yet proving that CTR policy cannot bypass planner/governance/runtime owners;
- no production evidence report showing current channel distribution by CTR state after this policy map.

## 16. Recommended Next Stage

Recommended next stage:

`CTR.2 - Channel Trust & Recovery Operator Policy Contract And No-Bypass Test Plan`

Scope:

- no runtime mutation;
- no user movement;
- no new truth source;
- define exact future runtime policy contract;
- define admin/operator action map in short Russian;
- define no-bypass tests;
- decide whether CTR enforcement should start as advisory-only UI, planner penalty, governance review requirement, or hard deny for specific states.

Implementation should still wait until CTR.2 closes the policy gaps.

## 17. Final Verdict

Final verdict: `OWNERSHIP_READY`

Final flags:

- ctr_owner_known=true
- canonical_ctr_source=`trust-evolution-summaries.channel_trust_recovery`
- runtime_owner=`tools/v7-users-autoswitch`
- planner_owner=`tools/v7-users-autoswitch`
- governance_owner=`admin_core/operator_execution.py + tools/v7-operator-execution-packet`
- admin_owner=`admin_core/operator_decision_surface.py + admin/v7-admin-api`
- trust_owner_known=true
- recovery_owner_known=true
- lifecycle_owner_known=true
- planner_mapping_defined=true
- governance_mapping_defined=true
- operator_mapping_defined=true
- recovery_mapping_defined=true
- duplication_safe=true
- safe_to_implement_now=false
- safe_to_begin_CTR_2=true
- required_next_step=CTR.2_operator_policy_contract_and_no_bypass_test_plan
