# CHANNEL.ROUTE.1 COMPONENT REALITY AUDIT

Project: V7 Vozduh

Branch: Updatesystem

Mode: audit only

## 1. Saved State

Current branch:

`Updatesystem`

Current local commit at audit start:

`a723ccb7 Create canonical V7 reference base`

Working tree at audit start:

```text
?? V7_VOZDUH_PROJECT_HANDOFF_DOCUMENTATION_2026_06_13.md
```

The untracked handoff document was present before this audit and was not modified.

No runtime code changes were made by this program.

## 2. Truth Gate

Pre-audit gate:

| Check | Result |
|---|---|
| `tools/v7-truth-check --all --json` | PASS |
| `tools/v7-convergence-status --json` | PASS |
| Local | PASS |
| GitHub | PASS |
| Runtime | PASS |
| Truth | PASS |
| Convergence | FULLY_ALIGNED |

Warnings:

- `documentation_dirty_ignored`
- `runtime_local_commit_docs_only_mismatch_ignored`

Runtime action status:

`READY_FOR_RUNTIME_ACTION`

This audit did not run apply, did not move users, did not change planner/governance/execution/database/UI code.

## 3. Route Source Audit

The visible Route component in the channel score is calculated in:

`admin/v7-admin-api`

Primary function:

```js
function channelSuitabilityRoute(row={}) {
  const state = channelTopologyState(row);
  if (state.group === 'problem') return {check:'Route', score:2, max:15, ...};
  if (state.group === 'check') return {check:'Route', score:9, max:15, ...};
  if (state.group === 'disabled') return {check:'Route', score:6, max:15, ...};
  return {check:'Route', score:15, max:15, ...};
}
```

Source line evidence:

- `admin/v7-admin-api:27128`
- `admin/v7-admin-api:27129`
- `admin/v7-admin-api:27130`
- `admin/v7-admin-api:27131`
- `admin/v7-admin-api:27132`
- `admin/v7-admin-api:27133`

The Route component does not directly calculate route quality. It delegates to:

```js
channelTopologyState(row)
```

Source line evidence:

- `admin/v7-admin-api:30605`

`channelTopologyState(row)` uses:

- registry role/enabled state
- runtime readiness
- lifecycle state
- service matrix
- channel load status
- current assigned user count through topology/load context

It does not directly use speed, latency, packet loss, planner score, selected moves, rollback state or execution history.

Route explanation/drawer evidence function:

```js
function channelScoreRouteEvidence(row={}) {
  const state = channelTopologyState(row);
  const routeRows = (overview.route_reality || []).filter(...);
  ...
}
```

Source line evidence:

- `admin/v7-admin-api:27645`
- `admin/v7-admin-api:27646`
- `admin/v7-admin-api:27647`

Important finding:

`route_reality` is used for explanation rows, but the score itself is decided by `channelTopologyState`, not by confirmed route rows.

## 4. Route Formula Decomposition

Route max score:

`15`

Possible point values:

| Condition | Route Score | Evidence |
|---|---:|---|
| `channelTopologyState(row).group === "working"` | 15/15 | `admin/v7-admin-api:27133`, `admin/v7-admin-api:30624` |
| `group === "check"` | 9/15 | `admin/v7-admin-api:27131`, `admin/v7-admin-api:30621` |
| `group === "disabled"` | 6/15 | `admin/v7-admin-api:27132`, `admin/v7-admin-api:30617` |
| `group === "problem"` | 2/15 | `admin/v7-admin-api:27130`, `admin/v7-admin-api:30618` |
| 0/15 | not produced by current code | no Route branch returns zero |

### Full Score: 15/15

Route receives full score only when topology state is `working`.

That requires:

- channel is not disabled/reserve
- no hard/full/over load
- service matrix is not zero and not partial
- lifecycle is OK
- runtime readiness does not say interface is down

### Partial Score: 9/15

Route receives `9/15` when topology state is `check`.

This happens when:

- lifecycle tone is not OK
- or service matrix is partial
- or load is WARN/SOFT/LIMIT

### Disabled Score: 6/15

Route receives `6/15` when topology state is `disabled`.

This happens when:

- registry `enabled=0`
- or role contains `reserve`

### Problem Score: 2/15

Route receives `2/15` when topology state is `problem`.

This happens when:

- interface is not started and users are assigned
- or service matrix exists and `okCount === 0`
- or load contains `FULL`, `HARD`, or `OVER`

This is the key answer to the critical question:

A working channel can get `Route 2/15` because `Route` is penalized by hard capacity/load state, not only by route failure.

### Fallback Behavior

If none of the negative conditions match, Route defaults to:

`15/15`

There is no explicit "unknown route evidence" score. Unknown route evidence does not by itself force `2/15`.

## 5. Route Truth Source Matrix

| Source | Does Route read it? | Does Planner read it? | Does runtime execution read it? | Can operator action affect it? | Notes |
|---|---|---|---|---|---|
| route table / `ip route get` | NO for score, YES for explanation evidence | NO direct evidence in planner score path | runtime routing itself uses OS routes, but Route score does not execute | indirectly through routing changes | `route_reality` is not primary score input |
| channel egress mapping | YES indirectly through row/id/state | YES | YES | yes, through assignments | used to identify channel row |
| service matrix | YES | YES | NO direct execution gate, but used in planning/safety | indirectly after service refresh | can force `problem` when `okCount === 0`, or `check` when partial |
| planner output | NO | YES | NO | no direct score effect | Route score is admin UI logic, not planner score |
| movement proposal | NO | YES in planner/execution flow | YES in execution flow | yes through approval flow | not Route score input |
| speed test | NO | YES in planner scoring | NO direct Route score effect | indirectly via diagnostics | Route ignores speed |
| latency | NO | YES in planner scoring | NO direct Route score effect | indirectly via diagnostics | Route ignores latency |
| connectivity probe / health | PARTIAL via lifecycle/health tone | YES via health gates | runtime may depend on interface health | yes by fixing channel | Route uses lifecycle tone |
| tunnel health | PARTIAL via runtime readiness/lifecycle | YES via health gates | YES operationally | yes by starting/fixing channel | only certain interface-down condition is direct |
| runtime assignment | PARTIAL through user count/load context | YES | YES | yes | assigned users can drive hard/full load |
| historical movement result | NO direct | YES in trust/quality history | NO direct | indirectly through feedback | Route ignores history directly |
| fallback/default | YES | N/A | N/A | no | default is `working`/15 if no condition triggers |

## 6. Route Meaning Audit

Does Route measure real user traffic quality?

`NO`

It does not read speed, latency, packet loss, client traffic quality or user traffic samples.

Does Route measure service reachability?

`PARTIAL`

It reads service matrix indirectly through topology. But service reachability is already measured by the Services component, so this overlaps with Services.

Does Route measure whether channel is usable for assignment?

`PARTIAL`

It includes load/capacity and service/topology state, which are assignment-readiness signals. But it is not the authoritative planner eligibility model.

Does Route measure whether V7 has enough internal confirmation?

`YES, PARTIAL`

The component expresses internal topology/readiness confidence more than physical route quality.

Does Route affect planner decisions?

`NO DIRECT EVIDENCE`

Planner decisions are owned by `tools/v7-users-autoswitch`, which uses separate gates and scoring. The planner has its own load/service/health/capacity logic.

Does Route affect runtime execution?

`NO`

Removing Route from visible channel score would not itself change runtime execution.

Does Route only affect admin score display?

`YES FOR THIS COMPONENT`

The Route component is part of the admin-visible score and explanation surface. It is not the execution authority.

## 7. Working Channel Paradox Test

Fresh production overview was read from:

`/api/overview`

Fresh operator decision surface was read from:

`/api/operator/decision-surface`

Current examples:

| Channel | Users | Services | Stability/Lifecycle | Runtime/Health | Planner Decision | Route Score | Why Route Low |
|---|---:|---:|---|---|---|---:|---|
| `vless` | 10 | 13/14 | Работает | OK | TRUSTED / ELIGIBLE | 2/15 | `HARD_FULL`, issue `лимит ёмкости` |
| `awg3` | 8 | 13/14 | Работает | OK | TRUSTED / ELIGIBLE | 2/15 | `HARD_FULL`, issue `лимит ёмкости` |
| `1` | 0 | 7/9 | Работает | OK | QUARANTINED / EXCLUDED | 9/15 | partial services, issue `часть сервисов` |
| `openvpn-1779388847-d2ad7c` | 0 | 0/14 | Нужна проверка | warn | QUARANTINED / EXCLUDED | 2/15 | services fail, issue `сервисы не проходят` |
| `wireguard-1779454504-c43409` | 8 | 13/14 | Работает | OK | TRUSTED / ELIGIBLE | 2/15 | `HARD_FULL`, issue `лимит ёмкости` |
| `awg0` | 0 | 13/14 | Работает | OK | TRUSTED / ELIGIBLE | 9/15 | partial services, issue `часть сервисов` |

Route reality evidence contradicts a pure "route failed" interpretation:

| Channel | Route Reality | Route Score |
|---|---:|---:|
| `vless` | 10/10 confirmed | 2/15 |
| `awg3` | 8/8 confirmed | 2/15 |
| `wireguard-1779454504-c43409` | 8/8 confirmed | 2/15 |

Critical answer:

Yes, a channel can be working well for real users while Route is `2/15`.

Reason:

The `2/15` is caused by topology group `problem`, and that group can be caused by `HARD_FULL` capacity/load. It does not require route reality failure.

## 8. Route Removal Impact Test

This is a mental/code-level simulation only. No code was changed.

If Route were removed from the visible score:

| Question | Answer | Reason |
|---|---|---|
| Would planner decision change? | NO | planner does not consume this UI component |
| Would selected moves change? | NO | selected moves are produced by `tools/v7-users-autoswitch` |
| Would runtime execution change? | NO | execution does not call `channelSuitabilityRoute` |
| Would user routing change? | NO | route assignment state is separate |
| Would service availability change? | NO | service matrix/probes are separate |
| Would safety decrease? | NO direct decrease | underlying planner/runtime gates remain |

What would change:

- operator-visible score total
- channel row explanation
- perceived severity of overloaded/partial-service channels

Risk of removal:

- operator might lose a compact warning that topology/load/service state needs attention

Safety impact:

- low for runtime
- medium for operator diagnostics clarity

## 9. Operator Value Test

What can operator do when Route = `2/15`?

Current UI action:

`Открыть канал`

Actual useful action depends on reason:

- if issue is `лимит ёмкости`, operator should inspect users/load/capacity
- if issue is `сервисы не проходят`, operator should inspect service diagnostics
- if issue is `не запущен`, operator should inspect runtime readiness

Problem:

Route itself is not a direct operator action.

For `vless` and `awg3`, the real explanation is not:

`Route not confirmed`

Better explanation:

`Канал работает, но заполнен по лимиту; поэтому он не должен принимать новых пользователей.`

For OpenVPN, better explanation:

`Сервисы на канале не проходят; маршрутный блок показывает topology problem, но первопричина в service matrix.`

Operator value:

Route provides a useful compact warning, but the label `Route` hides the real cause because the signal is often capacity/service topology, not route evidence.

## 10. Score Validity Test

Question:

Is it valid for Route to subtract 13 points from a score labeled `Technical Health`?

Answer:

`NO` for pure technical health.

Reason:

For overloaded but working channels, Route subtracts 13 points because of capacity/load, while route reality can be fully confirmed.

This is not real channel health degradation.

It may be valid for a broader readiness score:

`YES, PARTIAL` for operational readiness.

Reason:

A hard-full channel should not receive more users, so it is reasonable to reduce a "readiness as target" score. But it should not be presented as pure route quality or pure technical health.

## 11. Final Classification

Final classification:

`READINESS_CONFIDENCE_SIGNAL`

Route does not qualify as:

- `REAL_QUALITY_SIGNAL`
- `PLANNER_INTERNAL_SIGNAL`
- `REDUNDANT_SIGNAL`
- `UNKNOWN_OR_BROKEN_SIGNAL`

Why not `REAL_QUALITY_SIGNAL`:

- it does not directly read traffic quality
- it does not directly read speed/latency/packet loss
- confirmed route reality can be 10/10 while Route score is 2/15

Why not pure `PLANNER_INTERNAL_SIGNAL`:

- it is admin UI topology logic, not the planner scoring function

Why not only `REDUNDANT_SIGNAL`:

- it overlaps with Services and Capacity, but also compacts topology/readiness into one operator-visible signal

Why not `UNKNOWN_OR_BROKEN_SIGNAL`:

- the code path is clear and deterministic

Best interpretation:

Route is an operational topology/readiness confidence signal. It says whether the channel looks safe as a routing target under current topology, service and load conditions.

## 12. Recommendation

No implementation in this program.

Recommended future product decision:

Do not keep Route as a strong part of a score labeled only `Technical Health`.

Better options:

1. Split score into:
   - `Health`
   - `Readiness`
   - `Capacity`
   - `Route evidence`

2. Or rename Route to something closer to reality:
   - `Готовность маршрута`
   - `Topology readiness`
   - `Готовность как цель`
   - `Маршрут/нагрузка`

3. Or keep Route in diagnostics only and reduce its visible score weight.

The strongest recommendation:

Split `Health Score` and `Readiness Score`.

Route belongs in readiness/diagnostics, not pure health.

## 13. Final Verdict

Final verdict:

`READINESS_CONFIDENCE_SIGNAL`

Short answer:

Route currently means:

`Can this channel safely be treated as a routing target from the admin topology/readiness perspective?`

It does not mean:

`Does real user traffic route well through this channel?`

It can be `2/15` on a working channel because hard-full load/capacity is classified as topology problem.

Final verification table before report commit:

| Area | Status | Notes |
|---|---|---|
| Local | PASS | only unrelated handoff doc untracked |
| GitHub | PASS | canonical branch aligned |
| Runtime | PASS | runtime code aligned; docs-only mismatch ignored |
| Truth | PASS | no blockers |
| Convergence | FULLY_ALIGNED | runtime action safe |

