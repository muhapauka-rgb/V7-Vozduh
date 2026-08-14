# PROGRAM CTR.2 - Channel Trust & Recovery Policy Contract And No-Bypass Certification

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Mode: READ ONLY / POLICY CONTRACT ONLY

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
- CTR.1 verdict: `OWNERSHIP_READY`
- Canonical CTR source: `trust-evolution-summaries.channel_trust_recovery`
- Planner/runtime owner: `tools/v7-users-autoswitch`
- Governance owner: existing approval packet + restore barrier chain
- Admin/operator owner: existing operator decision surface and admin API

## 1. Executive Summary

CTR policy is ready as a contract.

CTR is currently:

- Advisory Only: true
- Advisory + Planner Influence: partial, through existing snapshot/advisory scoring only
- Hard Runtime Gate: false
- Governance Gate: policy-defined, not implemented as a new gate
- Execution Authority: false

The complete policy is:

- `TRUSTED` can be used normally inside existing planner, governance, authority and capacity limits.
- `WATCH` can be used cautiously, with operator attention for expansion.
- `NEW` requires review before expansion because history is thin.
- `DEGRADED` should not receive normal new placements; it is mainly for evacuation, temporary keep, or service repair.
- `RECOVERING` is not fully trusted; it requires operator review and more clean evidence.
- `QUARANTINED` is denied for normal routing and allowed only for emergency evacuation/rollback handling.

Final verdict: `POLICY_READY`

Reason:

Every lifecycle state now has product, runtime, governance, operator, recovery, emergency and no-bypass semantics. No implementation is included in this program.

## 2. Product Contract

| State | Product meaning | User impact | Business meaning | Service quality meaning | Channel quality meaning | Trust meaning | Recovery meaning |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `NEW` | Channel exists but V7 has not seen enough successful governed outcomes | User can be routed only with caution and review | Candidate supply grows, but not certified | Current checks may pass, history is thin | Usable signal not yet mature | Low/unknown trust | No recovery needed, evidence accumulation needed |
| `TRUSTED` | Channel has good current service evidence and successful feedback | Normal quality expected within existing gates | Good production routing candidate | Required services are healthy enough | Stable enough for normal governed use | Positive trust | Recovery not needed |
| `WATCH` | Channel works now but trust history is still thin | Usually OK, but operator should watch outcomes | Useful candidate, not fully proven | Current services look healthy | Good current state, limited historical proof | Medium trust | More outcomes can promote it |
| `DEGRADED` | Channel has weak current service or quality evidence | User quality may suffer if placed there | Do not expand usage; inspect issue | Required service or quality signal is below floor | Poor current state | Trust should not override poor current health | Needs current health repair |
| `RECOVERING` | Channel had negative history but current evidence improved | Can work, but risk is still higher than normal | Candidate may return after proof | Recent checks improve | Improving but not certified | Trust rebuilding | Needs clean observations and/or successful outcomes |
| `QUARANTINED` | Channel has hard negative evidence or missing required service | Normal routing unsafe | Remove from normal pool until fixed | Hard service gap, repeated failure, rollback failure, or very low quality | Not acceptable for normal use | Trust blocked | Requires fix plus recovery evidence |

Product invariant:

CTR describes channel confidence and recovery status. It does not sell or promise perfect connectivity. It tells the platform when a channel is normal, questionable, damaged, recovering, or blocked.

## 3. Runtime Contract

Runtime owner:

- `tools/v7-users-autoswitch`

Runtime evidence:

- `tools/v7-users-autoswitch` loads runtime state, service matrix, quality summary, safety, restore barrier and intelligence snapshots.
- `admin_core/intelligence_snapshots.runtime_read_contract()` says runtime may read snapshots and must not read raw history or run prediction engines.
- `tools/v7-users-autoswitch` marks `service-scores`, `channel-service-scores`, `risk-summaries`, `trust-summaries`, and `blast-radius-summaries` as runtime-required families.
- `trust-evolution-summaries` is currently advisory.

Runtime contract by state:

| State | Place new users | Keep users | Evacuate users | Score channel | Suppress channel | Prefer channel | Ignore channel | Evidence | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `NEW` | review required | allowed if hard gates pass | allowed if safer target exists | yes, capped/neutral | no hard suppress | no | no | lifecycle from CTR snapshot, thin feedback | not proven yet |
| `TRUSTED` | allowed | allowed | allowed if better target or degradation appears | yes | no | yes when scores close | no | high score + successful feedback | normal usable state |
| `WATCH` | allowed with caution | allowed | allowed if degradation appears | yes, cautious | no hard suppress | not preferred over trusted | no | good current checks, thin history | works now but not fully proven |
| `DEGRADED` | denied for normal placement | temporary keep only if no safe option | allowed/preferred toward healthier target | penalty/avoid | yes for normal target selection | no | no | weak current service signal | current quality dominates trust |
| `RECOVERING` | review required | allowed if hard gates pass | allowed if recovery fails | yes, reduced/cautious | partial | no normal preference | no | improved current signal after bad history | recovery needs proof |
| `QUARANTINED` | denied | no normal keep; emergency handling only | allowed through governed evacuation/rollback | no positive score | yes | no | no | hard negative evidence | fail closed |

Runtime rule:

CTR can only affect runtime through existing snapshot read paths and existing planner/governance rules. It cannot mutate runtime, write selected moves, apply routing, or create a second planner.

## 4. Governance Contract

Governance owner:

- approval packet lifecycle
- restore barrier lifecycle
- governed apply and rollback contracts

Governance evidence:

- `admin_core/operator_execution.py` validates packets, checks selected moves, writes restore barrier clearance, and appends lifecycle/audit records.
- `admin_core/operator_execution_pipeline.py` states trust is advisory and planner/governance remain authoritative.
- Existing blocked actions include apply without packet, rollback without packet, and execution without restore barrier.

Governance matrix:

| State | New placement | Rebalance | Evacuation | Recovery | Pool participation | Capacity expansion | Batch expansion |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `NEW` | `REVIEW_REQUIRED` | `REVIEW_REQUIRED` | `ALLOWED` if safer target exists | `NOT_APPLICABLE` | `REVIEW_REQUIRED` | `DENIED` until evidence grows | `DENIED` until evidence grows |
| `TRUSTED` | `ALLOWED` | `ALLOWED` | `ALLOWED` | `NOT_APPLICABLE` | `ALLOWED` | `ALLOWED` within capacity | `ALLOWED` within authority |
| `WATCH` | `REVIEW_REQUIRED` for expansion | `ALLOWED` for small bounded moves | `ALLOWED` | `NOT_APPLICABLE` | `ALLOWED_WITH_REVIEW` | `REVIEW_REQUIRED` | `REVIEW_REQUIRED` |
| `DEGRADED` | `DENIED` | `DENIED` as target | `ALLOWED` away from channel | `REVIEW_REQUIRED` | `DENIED` for normal pool | `DENIED` | `DENIED` |
| `RECOVERING` | `REVIEW_REQUIRED` | `REVIEW_REQUIRED` | `ALLOWED` if recovery fails | `REVIEW_REQUIRED` | `REVIEW_REQUIRED` | `DENIED` until recovery complete | `DENIED` until recovery complete |
| `QUARANTINED` | `DENIED` | `DENIED` as target | `EMERGENCY_ONLY` away from channel | `REVIEW_REQUIRED` after fix | `DENIED` | `DENIED` | `DENIED` |

Governance invariant:

Even `TRUSTED` cannot bypass authority budget, approval packet, restore barrier, selected move hash, rollback manifest, service gates or capacity rules.

## 5. Operator Contract

Operator principle:

The operator should see short Russian labels, one clear reason, one recommended action, blocked actions, recovery status, confidence and evidence count. Raw data belongs in the drawer/details, not on the main row.

Operator mapping:

| State | What operator sees | What operator understands | Expected action | Must not do | Can safely ignore |
| --- | --- | --- | --- | --- | --- |
| `NEW` | `Новый канал` | Channel exists, but history is not enough | Watch, run small reviewed checks, collect feedback | Do not use for broad expansion | Minor absence of old history if current checks are fine |
| `TRUSTED` | `Надежный` | Channel is healthy and proven recently | Normal monitored use | Do not bypass governance | No action if no warnings |
| `WATCH` | `Под наблюдением` | Works now, but evidence is still thin | Use cautiously, collect outcomes | Do not expand aggressively | Minor caution if no movement planned |
| `DEGRADED` | `Проблема качества` | Current services/quality are weak | Refresh checks, inspect service issue, avoid new placements | Do not send new users normally | Nothing if channel is unused and not selected |
| `RECOVERING` | `Восстанавливается` | It was bad, now looks better | Keep observing, require review before normal use | Do not mark trusted manually | No action if not in candidate pool |
| `QUARANTINED` | `Заблокирован` | Hard negative evidence blocks normal use | Fix root cause, refresh checks, wait for recovery evidence | Do not force route users there | Nothing only if fully unused and not needed |

Operator must always understand:

- why this state exists;
- what is blocked;
- what one next action is;
- whether it affects users now;
- whether governance review is required.

## 6. Admin Integration Contract

Admin integration rule:

No new top-level sections. CTR must integrate into existing channel/operator surfaces.

Existing admin locations:

- channel state appears through `admin_core/operator_decision_surface.py`;
- existing admin API includes channel state column/drawer coverage verified by tests;
- egress draft quarantine exists as onboarding pipeline and must remain separate from general CTR truth.

Admin contract by state:

| State | Existing admin placement | Drawer should show | Summary should show | Details should show | Hidden by default |
| --- | --- | --- | --- | --- | --- |
| `NEW` | channel row/state cell | short reason, current checks, evidence count | `Нужны успешные наблюдения` | service score, confidence, feedback count | raw JSON hashes |
| `TRUSTED` | channel row/state cell | why trusted, last success, confidence | `Можно использовать по правилам` | trust score, service score, successes | raw audit rows |
| `WATCH` | channel row/state cell | why under watch, expected observation window | `Работает, но история тонкая` | current score, confidence, success/failure count | raw model internals |
| `DEGRADED` | channel row/state cell | failing services/quality reason | `Не отправлять новых пользователей` | required_low, verdict, quality score | unrelated diagnostics |
| `RECOVERING` | channel row/state cell | recovery state and missing proof | `Нужно дождаться подтверждения` | prior failures, current improvement, required successes | raw logs unless opened |
| `QUARANTINED` | channel row/state cell | hard blocker and exact fix category | `Обычная маршрутизация запрещена` | failure/service gap/rollback evidence | direct mutation controls |

Admin action policy:

- one issue opens one focused modal;
- modal fixes only that issue;
- operator copy should be Russian, short and unambiguous;
- details can expose evidence, but not overwhelm the default view;
- admin must not provide direct CTR state override unless a later governed program explicitly creates such a reviewed action.

## 7. Recovery Contract

| State | Entry conditions | Exit conditions | Recovery conditions | Evidence required | Minimum confidence | Operator review? | Governance review? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `NEW` | insufficient feedback and low/unknown confidence | current evidence promotes to `WATCH`, success promotes to `TRUSTED`, failure to `DEGRADED/QUARANTINED` | evidence accumulation | service score, suitability, current checks | >= 0.35 for `WATCH` | yes for expansion | yes for placement expansion |
| `TRUSTED` | high current score, confidence, successful feedback | degradation, hard failure, missing service, rollback failure | not needed | current score, confidence, success feedback | >= 0.45 plus success | no normal review | normal governance only |
| `WATCH` | healthy current services but thin history | success to `TRUSTED`; weak signal to `DEGRADED`; hard failure to `QUARANTINED` | collect more outcomes | service score, confidence, success/failure count | >= 0.35 | yes for broad expansion | yes for expansion |
| `DEGRADED` | weak current service signal, required_low, non-OK verdict, low score | improved evidence to `RECOVERING/WATCH`; hard negative to `QUARANTINED` | fix/refresh current quality | service matrix, quality summary, required service checks | enough to prove improvement | yes | yes |
| `RECOVERING` | prior negative history plus improved current signal | clean evidence to `WATCH/TRUSTED`; new failure to `QUARANTINED` | stable observation or successful outcomes | current checks, successes, no hard gaps | medium; ideally >= 0.45 for trusted promotion | yes | yes |
| `QUARANTINED` | repeated failures, rollback failure, required_missing, very low score | only after root fix and recovery evidence | fix root cause, refresh checks, observe recovery | hard blocker evidence, fix evidence, clean checks | high enough for review, never blind | yes | yes |

Recovery invariant:

Recovery is evidence-driven, not time-only. Time windows help explain observation, but clean current evidence and absence of hard blockers are mandatory.

## 8. Emergency Policy Contract

Emergency rule:

Fail closed. Do not invent a shortcut just because the pool is bad.

| Scenario | Fail-closed behavior | Best-available-pool behavior | Emergency routing behavior |
| --- | --- | --- | --- |
| All channels are `DEGRADED` | no normal expansion; operator review required | pool may show least-bad candidates as degraded, not healthy | keep existing users if safer than moving; evacuate only to relatively safer target |
| All channels are `RECOVERING` | no automatic expansion; review required | pool may rank recovering channels as review-only | emergency use only with packet and explicit review |
| All channels are `QUARANTINED` | stop normal planning and mark no safe target | best pool should be empty or blocked | only rollback/evacuation through governance if it reduces risk |
| Only one channel remains | do not overload blindly; respect capacity/service gates | single candidate shown with risk/context | keep service continuity if safe, otherwise stop and require operator |
| Required services unavailable everywhere | deny service-aware placements | pool should show missing required service blockers | no normal move; operator chooses outage handling path |

Emergency invariant:

CTR cannot authorize emergency movement. Emergency routing still needs existing planner, approval packet, restore barrier, runtime owner and rollback readiness.

## 9. No-Bypass Certification

Explicit no-bypass matrix:

| CTR component | Can bypass? | Why? | Protection |
| --- | --- | --- | --- |
| `ServiceHistoryStore` | No | read model only | no runtime writes, no selected moves |
| `ExecutionTrustModel` | No | score/evidence only | `runtime_decision_authority=none_shadow_only` |
| `trust-summaries` | No | snapshot evidence | runtime validates snapshot but planner remains owner |
| `risk-summaries` | No | required risk guard input | STOP/WARN behavior through existing runtime gate |
| `blast-radius-summaries` | No | guard/advisory input | authority budget and packet still dominate |
| `trust-evolution-summaries` | No | advisory snapshot family today | stale/low confidence is IGNORE for advisory family, no execution authority |
| `channel_trust_recovery` | No | lifecycle/recovery evidence only | `runtime_decision_authority=none_evidence_only` |
| operator channel UI | No | read-only display/action guidance | no direct selected move or runtime mutation authority |
| future CTR policy | No | must route through existing planner/governance | no new planner, no new governance, no new runtime owner |

Protected authorities:

| Authority | Protected by |
| --- | --- |
| planner | `tools/v7-users-autoswitch` remains final planner owner |
| governance | approval packet lifecycle remains required |
| approval packet | packet validation and source/selected move hashes |
| restore barrier | restore barrier clearance and generation/hash checks |
| execution authority | governed apply only, no CTR direct apply |
| runtime owner | runtime state and selected moves remain runtime-owned |
| capacity owner | runtime capacity/load policies remain authoritative |
| batch owner | authority budget and batch governance remain authoritative |

Certification:

- ctr_bypasses_planner=false
- ctr_bypasses_governance=false
- ctr_bypasses_approval_packet=false
- ctr_bypasses_restore_barrier=false
- ctr_bypasses_execution_authority=false
- ctr_bypasses_runtime_owner=false
- ctr_bypasses_capacity_owner=false
- ctr_bypasses_batch_owner=false

## 10. State Authority Matrix

| State | Product meaning | Operator meaning | Runtime meaning | Governance meaning | Allowed actions | Denied actions | Recovery path | Next states |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `NEW` | existing but unproven | use carefully | may score cautiously; no blind expansion | review required | observe, bounded reviewed use, collect evidence | broad placement, batch expansion | collect current checks and successful outcomes | `WATCH`, `TRUSTED`, `DEGRADED`, `QUARANTINED` |
| `TRUSTED` | proven healthy enough | normal use | may prefer/score normally | allowed within gates | normal governed routing, rebalance, pool use | bypass governance | none unless degraded | `TRUSTED`, `WATCH`, `DEGRADED`, `QUARANTINED` |
| `WATCH` | healthy now, thin history | watch outcomes | score cautiously | review for expansion | small bounded use, monitoring | aggressive expansion | more successful observations | `TRUSTED`, `DEGRADED`, `QUARANTINED` |
| `DEGRADED` | current quality weak | inspect/fix | avoid as target, evacuate if safe | denied as normal target | refresh checks, inspect, evacuate away | new placement, expansion | fix current service quality | `RECOVERING`, `WATCH`, `QUARANTINED` |
| `RECOVERING` | improving after negative history | review before trust | reduced/cautious scoring | review required | observe, limited reviewed use | automatic full restore, expansion | prove stable clean evidence | `WATCH`, `TRUSTED`, `QUARANTINED` |
| `QUARANTINED` | hard blocked | do not use normally | suppress as target | denied except emergency evacuation/rollback | fix root cause, emergency evacuation away | normal routing, pool expansion, batch expansion | fix plus recovery evidence | `RECOVERING`, eventually `WATCH/TRUSTED` |

Layer authority certification:

| Layer | Current CTR authority |
| --- | --- |
| Product | policy-defined |
| Operator | advisory/display/review guidance |
| Runtime | advisory evidence only, required trust/risk guard families already exist |
| Planner | existing planner influence only; no CTR hard gate yet |
| Governance | policy-defined review/deny semantics, not new implemented gate |
| Execution | no authority |

## 11. Policy Gaps

Remaining gaps before implementation:

- no implemented runtime hard gate for lifecycle states;
- no no-bypass tests specifically named for CTR state enforcement;
- no final admin copy pass in short Russian for all CTR states;
- no focused modal action list for each state;
- no canonical emergency operator packet template for all-channels-bad scenarios;
- no production state inventory showing current channels by CTR lifecycle after this contract.

These are policy-to-implementation gaps, not ownership gaps.

## 12. Recommended Next Stage

Recommended next stage:

`CTR.3 - Advisory Operator Surface And No-Bypass Tests`

Scope:

- keep CTR advisory-only;
- do not change routing behavior;
- do not create new snapshot family;
- add/verify tests that CTR cannot bypass planner, governance, packet, restore barrier or execution;
- make admin text short, Russian and operator-friendly inside existing channel drawer/summary;
- expose one clear recommended action per state;
- no user movement;
- no apply;
- no authority promotion.

Implementation should start advisory/UI/test-only before any planner hard-gate behavior is considered.

## 13. Final Verdict

Final verdict: `POLICY_READY`

Final flags:

- product_contract_defined=true
- runtime_contract_defined=true
- governance_contract_defined=true
- operator_contract_defined=true
- admin_integration_contract_defined=true
- recovery_contract_defined=true
- emergency_policy_defined=true
- no_bypass_certified=true
- ctr_currently_advisory_only=true
- ctr_hard_runtime_gate=false
- ctr_execution_authority=false
- second_trust_score_created=false
- second_lifecycle_created=false
- second_recovery_model_created=false
- second_planner_created=false
- second_governance_path_created=false
- second_runtime_authority_created=false
- second_snapshot_family_created=false
- safe_to_implement_CTR_3_advisory_surface_and_tests=true
- safe_to_enable_CTR_runtime_enforcement=false
- required_next_step=CTR.3_advisory_operator_surface_and_no_bypass_tests
