# PROGRAM CTR.3 - Runtime And Governance Integration Design

Project: V7 Vozduh

Workspace: `/Users/ponch/Documents/New project`

Mode: READ ONLY / INTEGRATION DESIGN ONLY

Safety result:

- implementation_changes=false
- runtime_mutation=false
- deploy_run=false
- commits_created=false
- storage_changes=false
- snapshot_changes=false
- api_changes=false
- ui_changes=false
- new_truth_sources_created=false
- new_planners_created=false
- new_governance_paths_created=false

Input basis:

- CTR.0 verdict: `STRONG_FOUNDATION`
- CTR.1 verdict: `OWNERSHIP_READY`
- CTR.2 verdict: `POLICY_READY`
- CTR.2.5 verdict: `PARTIALLY_IMPLEMENTED`
- CTR completion: `56%`

Primary design rule:

CTR must influence the existing planner, governance, runtime, pool, services and capacity paths without creating a second planner, second governance path, second runtime authority or second truth source.

## 1. Executive Summary

CTR integration should be staged, not switched on as a hard runtime gate immediately.

Recommended integration model:

1. `TRUSTED`: soft bonus / normal allowed use.
2. `WATCH`: neutral to small soft penalty / review for expansion.
3. `NEW`: soft penalty / review required for new placement and expansion.
4. `DEGRADED`: soft-to-hard suppression as target / evacuation allowed.
5. `RECOVERING`: soft penalty / review required / limited pool participation.
6. `QUARANTINED`: hard deny as normal target / emergency evacuation or rollback only.

Runtime authority remains `tools/v7-users-autoswitch`.

Governance authority remains approval packet + restore barrier + governed apply.

CTR authority remains snapshot-backed evidence and policy input.

Final verdict: `DESIGN_READY`

Reason:

The integration design is clear, but runtime/governance implementation should wait for advisory surface/no-bypass tests and emergency behavior tests.

## 2. Planner Integration Design

Planner owner:

- `tools/v7-users-autoswitch`

CTR source:

- `trust-evolution-summaries.channel_trust_recovery`

Planner integration matrix:

| State | Candidate eligibility | Candidate ranking | Pool participation | New user placement | Existing user retention | Evacuation behavior | Rebalance behavior | Suitability impact | Capacity tie-break | Service-aware impact |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `NEW` | `Review Required` | `Soft Penalty` | `Review Required` | `Review Required` | `Allowed if current hard gates pass` | `Allowed if safer target exists` | `Review Required` | cap/penalty until feedback exists | loses tie to trusted/watch | required services still dominate |
| `TRUSTED` | `Allowed` | `Soft Bonus` | `Allowed` | `Allowed` | `Allowed` | `Allowed if better/safer target exists` | `Allowed` | small positive adjustment | wins tie if load acceptable | can still lose if service quality poor |
| `WATCH` | `Allowed with caution` | `Neutral or small penalty` | `Allowed with review` | `Review Required for expansion` | `Allowed` | `Allowed` | `Allowed if low blast radius` | neutral/cautious | loses tie to trusted if load similar | can rank high when service fit is strong |
| `DEGRADED` | `Hard Gate for normal target` | `Hard/strong penalty` | `Removed from normal pool` | `Denied` | `Temporary keep only` | `Preferred away from channel` | `Denied as target` | strong negative | cannot win tie | required service failure dominates |
| `RECOVERING` | `Review Required` | `Soft Penalty` | `Limited review pool` | `Review Required` | `Allowed if current gates pass` | `Allowed if recovery fails` | `Review Required` | reduced until recovery proof | loses tie unless much better service/load | excellent service can raise to review, not auto-allow |
| `QUARANTINED` | `Hard Gate` | `No positive score` | `Removed` | `Denied` | `Emergency only` | `Allowed away through governed path` | `Denied as target` | hard suppression | cannot win tie | service quality cannot override quarantine |

Planner precedence:

1. Hard runtime safety and restore barrier constraints.
2. Required services.
3. Capacity/load/reservation constraints.
4. CTR hard states (`QUARANTINED`, normal-target `DEGRADED`).
5. Authority budget and batch limits.
6. CTR soft influence (`TRUSTED`, `WATCH`, `NEW`, `RECOVERING`).
7. Suitability/ranking tie-breaks.

Design decision:

- First implementation should be planner advisory fields and dry-run explanations.
- Second implementation can add soft penalties/bonuses.
- Hard gating should be limited to `QUARANTINED` as normal target and `DEGRADED` as normal new placement after tests exist.

## 3. Governance Integration Design

Governance owner:

- `admin_core/operator_execution.py`
- `tools/v7-operator-execution-packet`
- restore barrier lifecycle

Governance matrix:

| State | Placement | Rebalance | Evacuation | Recovery | Capacity promotion | Batch expansion | Pool participation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `NEW` | `Review Required` | `Review Required` | `Allowed` | `Not Applicable` | `Denied until evidence` | `Denied until evidence` | `Review Required` |
| `TRUSTED` | `Allowed` | `Allowed` | `Allowed` | `Not Applicable` | `Allowed within capacity` | `Allowed within authority` | `Allowed` |
| `WATCH` | `Review Required` for expansion | `Allowed` for bounded low-risk moves | `Allowed` | `Not Applicable` | `Review Required` | `Review Required` | `Allowed with review` |
| `DEGRADED` | `Denied` as normal target | `Denied` as target | `Allowed` away | `Review Required` | `Denied` | `Denied` | `Denied` normal pool |
| `RECOVERING` | `Review Required` | `Review Required` | `Allowed` if recovery fails | `Review Required` | `Denied until recovered` | `Denied until recovered` | `Limited review pool` |
| `QUARANTINED` | `Denied` | `Denied` as target | `Emergency Only` away | `Review Required after fix` | `Denied` | `Denied` | `Denied` |

Governance packet design:

- CTR state should be recorded inside packet evidence.
- CTR must not approve packet by itself.
- `REVIEW_REQUIRED` means packet must include explicit operator acknowledgement of the channel state.
- `DENIED` means packet generation should fail or mark candidate blocked.
- `EMERGENCY_ONLY` means packet must be evacuation/rollback-scoped, not normal placement-scoped.

## 4. Best Available Pool Integration

Current principle:

- Best Available Pool should choose healthy, eligible, high-quality options without inventing a second pool owner.

CTR pool behavior:

| State | Pool entry | Pool ranking | Pool expansion | Pool removal | Pool recovery | Pool re-entry |
| --- | --- | --- | --- | --- | --- | --- |
| `NEW` | review pool only | below `WATCH/TRUSTED` | no expansion | remove if failure appears | collect evidence | after `WATCH/TRUSTED` |
| `TRUSTED` | normal pool | bonus among similar candidates | allowed within capacity | remove if degraded/quarantined | not needed | stays/re-enters normally |
| `WATCH` | normal/review pool | neutral/cautious | review required | remove if degraded | collect success feedback | after stable evidence |
| `DEGRADED` | no normal pool | suppressed | denied | remove from normal pool | fix current service truth | after `RECOVERING/WATCH` |
| `RECOVERING` | limited review pool | below `WATCH` | denied | remove if failure repeats | observe recovery | after `WATCH/TRUSTED` |
| `QUARANTINED` | no pool | none | denied | remove immediately from normal pool | root-cause fix required | only through `RECOVERING` |

Pool design invariant:

CTR can influence pool entry/ranking through existing best-available-pool logic only. It must not create a second pool file or second selection path.

## 5. Service-Aware Routing Integration

Current V7 principle:

- Required Services first.

Precedence:

1. If a required service is unavailable on a channel, trust cannot override it.
2. If a channel is `TRUSTED` but service quality is poor for Telegram/YouTube/Instagram/ChatGPT/Google, it loses ranking or becomes blocked for that service profile.
3. If a channel is `RECOVERING` but service quality is excellent, it may become review-required candidate, not automatic winner.
4. If a channel is `QUARANTINED`, service quality cannot restore normal eligibility by itself.
5. Future services inherit the same rule: service fit is mandatory; CTR trust is a risk/recovery layer, not service compatibility.

Service examples:

| Situation | Design behavior |
| --- | --- |
| `TRUSTED` channel, Telegram poor | no Telegram placement; rank lower or block for Telegram-required users |
| `TRUSTED` channel, YouTube overloaded/poor | lose to lower-trust channel if required YouTube quality is better and safe |
| `WATCH` channel, all required services excellent | may rank high but requires review for expansion |
| `RECOVERING` channel, ChatGPT excellent | review-required candidate only |
| `QUARANTINED` channel, Google excellent | still denied as normal target |

Answer to mandatory questions:

- Can a `TRUSTED` channel still lose ranking because service quality is poor? Yes.
- Can a `RECOVERING` channel win because service quality is excellent? It can win review ranking, but not automatic placement.

## 6. Capacity Integration

Capacity owner:

- existing runtime load/capacity logic in `tools/v7-users-autoswitch`

Capacity precedence:

1. Hard capacity and reservation limits beat CTR trust.
2. CTR can break ties only after capacity and required service gates pass.
3. Recovery state should not justify overloading a channel.

Capacity scenarios:

| Scenario | Design behavior |
| --- | --- |
| `TRUSTED` but overloaded | do not place new users; keep only if safer than movement; prefer less loaded safe channel |
| `WATCH` but lightly loaded | may be selected for small bounded/reviewed moves if service fit is good |
| `RECOVERING` but empty | review-required; can be used only after recovery evidence, not because it is empty |
| `QUARANTINED` but only remaining channel | fail closed for normal placement; emergency continuity requires explicit operator/governance path |
| reserved channel is `TRUSTED` | reservation policy still wins; trust does not unlock reserved capacity |
| projected load exceeds hard limit | deny regardless of CTR state |

Capacity tie-break:

- `TRUSTED` can win ties when load is acceptable.
- `WATCH` can beat overloaded `TRUSTED` if services and capacity are clearly better.
- `RECOVERING` cannot win tie without review.
- `QUARANTINED` cannot win tie.

## 7. Emergency Design

Emergency policy:

- Fail closed by default.
- Fail open is not allowed for normal placement.
- Best Available Pool may show least-bad options only as emergency/review candidates, not healthy candidates.

Emergency matrix:

| Scenario | Fail closed? | Best Available? | Emergency pool? | Runtime behavior | Governance behavior |
| --- | --- | --- | --- | --- | --- |
| All channels degraded | yes for expansion | show ranked degraded candidates as blocked/review | yes, review-only | keep existing users if safer; evacuate only to less-bad safe target | explicit review packet |
| All channels recovering | yes for expansion | show recovery candidates as review-only | yes | no automatic movement | review required |
| All channels quarantined | yes | no normal pool | emergency evacuation/rollback only | stop normal planning | emergency-only packet |
| Single surviving channel | conditional fail closed | single candidate with warnings | yes if service/capacity passes | avoid overload; preserve continuity if safest | review if expansion |
| Required services unavailable everywhere | yes | no service-aware healthy pool | outage handling only | no normal service-aware move | operator outage decision |
| Operator unavailable | yes | no apply | no live movement | dry-run/report only | no approval, no execution |

Emergency invariant:

No CTR state can authorize movement when operator approval, packet, restore barrier or runtime owner is unavailable.

## 8. Runtime Integration Design

Recommended runtime mode by state:

| State | Advisory Only | Planner Influence | Governance Gate | Runtime Gate | Execution Authority | Exact owner |
| --- | --- | --- | --- | --- | --- | --- |
| `NEW` | yes | soft penalty | review-required evidence | no hard gate initially | none | planner + governance packet |
| `TRUSTED` | yes | soft bonus | normal evidence | no hard gate | none | planner |
| `WATCH` | yes | neutral/small penalty | review for expansion | no hard gate initially | none | planner + governance packet |
| `DEGRADED` | yes | strong penalty | deny normal placement | hard gate later for normal target | none | planner/runtime with governance evidence |
| `RECOVERING` | yes | soft penalty | review required | no hard gate initially | none | planner + governance packet |
| `QUARANTINED` | yes | hard suppression | deny normal placement | hard gate later for normal target | none | runtime planner gate |

Combination decision:

- CTR should become `Advisory + Planner Influence + Governance Gate`.
- CTR should become a narrow `Runtime Gate` only for normal target suppression of `QUARANTINED` and possibly `DEGRADED`.
- CTR must never become `Execution Authority`.

Implementation safety sequence:

1. Advisory payload and UI/test contract.
2. Planner dry-run explanations only.
3. Soft scoring influence.
4. Governance review/deny in packet generation.
5. Hard runtime target suppression for `QUARANTINED`.
6. Hard runtime target suppression for `DEGRADED` normal placement.

## 9. Decision To Action Matrix

| CTR State | Condition | Planner Decision | Governance Decision | Runtime Behavior | Operator Action | Recovery Action | Next State |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `NEW` | insufficient success history | candidate with penalty/review | review required | dry-run allowed; apply only after packet | inspect evidence, approve only small scope | collect outcomes | `WATCH` or `TRUSTED` |
| `TRUSTED` | high score + successful feedback | normal candidate/bonus | allowed within gates | normal governed runtime path | monitor | none | stays or drops on degradation |
| `WATCH` | healthy now, thin history | cautious candidate | review for expansion | governed path only | monitor and collect feedback | successful observations | `TRUSTED` |
| `DEGRADED` | current service weak | suppress as target; evacuate away | deny normal placement | no normal target apply | fix service/checks | refreshed clean evidence | `RECOVERING` or `WATCH` |
| `RECOVERING` | improved after negative history | review candidate with penalty | review required | governed path only | observe 24-72h or two successes | prove recovery | `WATCH` or `TRUSTED` |
| `QUARANTINED` | hard negative evidence | hard suppress as target | deny except emergency away | no normal apply to target | fix root cause | recovery evidence after fix | `RECOVERING` |

## 10. No-Bypass Review

Design protections:

| Protected owner/path | Can CTR bypass? | Design protection |
| --- | --- | --- |
| planner owner | no | CTR state is input to `tools/v7-users-autoswitch`, not a planner replacement |
| governance owner | no | CTR review/deny must be represented in existing packet flow |
| approval packet | no | no CTR movement without approval packet |
| restore barrier | no | no CTR apply without restore barrier clearance |
| execution authority | no | CTR never runs apply or rollback |
| runtime owner | no | runtime remains sole selected-move/apply owner |
| capacity owner | no | capacity/load rules dominate CTR trust |
| batch owner | no | authority budget and batch governance dominate CTR |

No-bypass test requirements before implementation:

- CTR cannot write selected moves.
- CTR cannot create approval packets directly.
- CTR cannot write restore barrier.
- CTR cannot call apply.
- CTR cannot override capacity gates.
- CTR cannot override required service gates.
- CTR cannot make `QUARANTINED` eligible through service score alone.

## 11. Implementation Readiness Matrix

| Proposed integration | Classification | Reason |
| --- | --- | --- |
| add CTR state to dry-run explanation | `READY_TO_IMPLEMENT` | advisory-only, no behavior change |
| add admin/operator action text from existing state | `READY_TO_IMPLEMENT` | existing surface exists |
| add no-bypass tests | `READY_TO_IMPLEMENT` | safety scaffolding exists |
| add planner soft bonus for `TRUSTED` | `NEEDS_MORE_POLICY` | must calibrate score impact |
| add planner soft penalty for `NEW/WATCH/RECOVERING` | `NEEDS_MORE_POLICY` | needs calibration and test data |
| remove `DEGRADED` from normal best pool | `NEEDS_MORE_POLICY` | emergency behavior must be tested |
| remove `QUARANTINED` from normal best pool | `READY_TO_IMPLEMENT` after tests | aligns with policy, but needs no-bypass tests |
| governance review-required packet field | `READY_TO_IMPLEMENT` after tests | no new governance path required |
| hard runtime gate for `QUARANTINED` target | `HIGH_RISK` until emergency tests exist | can strand users if no safe alternative |
| hard runtime gate for `DEGRADED` target | `HIGH_RISK` until emergency tests exist | degradation can be transient |
| capacity tie-break using CTR | `NEEDS_MORE_POLICY` | avoid overload bias |
| emergency pool behavior | `NEEDS_MORE_POLICY` | must define exact operator path |

## 12. Recommended Implementation Order

Recommended order:

1. CTR.4: advisory surface + dry-run explanation + no-bypass tests.
2. CTR.5: governance packet evidence fields and review-required semantics, no hard deny.
3. CTR.6: best-available-pool soft integration, no hard runtime gate.
4. CTR.7: emergency scenario dry-run tests for all degraded/recovering/quarantined/single-channel/service-outage.
5. CTR.8: hard normal-target suppression for `QUARANTINED`.
6. CTR.9: conditional hard normal-target suppression for `DEGRADED`.
7. CTR.10: capacity/service CTR calibration after production observation.

Do not enable hard runtime enforcement before CTR.7 emergency tests pass.

## 13. Final Verdict

Final verdict: `DESIGN_READY`

Final flags:

- planner_integration_designed=true
- governance_integration_designed=true
- runtime_integration_designed=true
- best_available_pool_integration_designed=true
- service_aware_routing_integration_designed=true
- capacity_integration_designed=true
- emergency_design_defined=true
- no_bypass_design_review_pass=true
- creates_second_planner=false
- creates_second_governance=false
- creates_second_authority=false
- creates_second_routing_system=false
- implementation_ready_for_advisory_surface_and_tests=true
- implementation_ready_for_hard_runtime_gate=false
- safe_next_step=CTR.4_advisory_surface_dry_run_explanations_and_no_bypass_tests
