# CHANNEL.SCORE.1 REALITY AUDIT

Project: V7 Vozduh

Branch: Updatesystem

Mode: audit only

## 1. Executive Summary

Channel Score in the admin UI is not a pure channel quality score.

It is also not the planner score.

It is a mixed diagnostic score that combines:

- service pass rate
- runtime/lifecycle readiness
- load/capacity pressure
- route/topology warnings
- runtime readiness
- decision/history state

Final verdict:

`MIXED_SCORE`

More precise name:

`technical_operational_readiness_score`

The current label `Technical Health` is only partially correct. A working channel can show `67/100` or `69/100` because overload/capacity penalties reduce the score even when services, runtime and stability are healthy.

## 2. Truth Gate And Current State

Pre-audit truth gate:

- `tools/v7-truth-check --all --json`: PASS
- `tools/v7-convergence-status --json`: PASS
- convergence status: FULLY_ALIGNED
- runtime access: READY
- runtime action status: READY_FOR_RUNTIME_ACTION

Current local state at audit start:

- branch: `Updatesystem`
- commit: `fb2335fb Finalize channel health score explanations`
- dirty state: one unrelated untracked documentation file was present:
  - `V7_VOZDUH_PROJECT_HANDOFF_DOCUMENTATION_2026_06_13.md`

The untracked file was not part of this audit and was not modified.

## 3. Score Source Audit

The admin UI channel score is owned by frontend logic inside:

- `admin/v7-admin-api`

Primary score function:

- `channelSuitability(source = {})`

Main render function:

- `channelSuitabilityCell(source)`

The visible `/100` number is calculated in the admin frontend from overview data. It is not directly taken from planner selected moves, authority budget, restore barrier, autonomy policy, or execution feedback.

Relevant owners:

- admin score UI owner: `admin/v7-admin-api`
- planner decision owner: `tools/v7-users-autoswitch`
- service/channel snapshot owner: `admin_core/intelligence_workers.py`

Important separation:

The admin UI score and planner ranking score are different systems.

## 4. Formula Decomposition

Current admin channel score is composed of six parts.

| Component | Max | Meaning | Primary source |
|---|---:|---|---|
| Services | 30 | Required service pass coverage | service matrix |
| Stability | 20 | Runtime/lifecycle readiness | health and lifecycle state |
| Capacity | 15 | Load pressure against soft/hard limits | user count, load status, capacity flags |
| Route | 15 | Topology/route warning state | topology state |
| Runtime | 10 | Enablement/readiness state | runtime readiness fields |
| History | 10 | Decision/history label | operator decision surface |

Total:

`Services + Stability + Capacity + Route + Runtime + History = 100`

### Services

Maximum: `30`

Meaning:

- how many required services pass on the channel
- scaled as `ok / total * 30`
- if service total is unknown, fallback is `18/30`

This component is closest to real service health.

### Stability

Maximum: `20`

Meaning:

- whether channel is enabled
- whether lifecycle/runtime state is healthy
- whether health state is OK

It is not the same as the planner's long-window transport stability model.

### Capacity

Maximum: `15`

Meaning:

- whether channel load is below soft/hard limits
- hard/overloaded state collapses this component to `2/15`
- soft/warn state gives `9/15`
- OK gives `15/15`

This is not pure quality. It is operational pressure.

### Route

Maximum: `15`

Meaning:

- topology state
- routing warnings
- capacity-related topology problems

This can also collapse when the channel itself works, but the current route/load situation is not suitable.

### Runtime

Maximum: `10`

Meaning:

- whether runtime says the channel is ready/enabled
- ready state gives `10/10`
- unknown gives `6/10`
- explicit bad state gives `2/10`

### History

Maximum: `10`

Meaning:

- decision/history state from operator decision surface
- trusted/ready gives `10/10`
- watch/warn gives `6/10`
- quarantined/bad gives `2/10`
- unknown/default gives `7/10`

This is the clearest proof that the score is not pure technical health.

## 5. Capacity Reality

In the current live overview, several channels are technically working but score lower because capacity and route penalties are active.

Observed examples:

| Channel | Score | Services | Stability | Capacity | Route | Runtime | History | Main reason |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `vless` | 67 | 26 | 20 | 2 | 2 | 10 | 7 | hard full / capacity route problem |
| `awg3` | 69 | 28 | 20 | 2 | 2 | 10 | 7 | hard full / capacity route problem |
| `wireguard-1779454504-c43409` | 69 | 28 | 20 | 2 | 2 | 10 | 7 | hard full / capacity route problem |
| `awg0` | 89 | 28 | 20 | 15 | 9 | 10 | 7 | services mostly OK, route check |
| `openvpn-1779388847-d2ad7c` | 42 | 0 | 8 | 15 | 2 | 10 | 7 | services fail |

Capacity in this score means:

- current assigned user count
- soft/hard limit pressure
- load flags such as `HARD_FULL`
- route/topology pressure caused by capacity

It does not mean physical bandwidth only.

It also does not mean "cannot work". A channel can work and still receive a capacity penalty because it is already too loaded for new assignments.

## 6. Working Channel Paradox

Question:

How can a channel work but show `64/100`, `67/100`, or `72/100`?

Answer:

Because the score is mixed.

Example:

`vless = 67/100`

Breakdown:

- Services: `26/30`
- Stability: `20/20`
- Runtime: `10/10`
- History: `7/10`
- Capacity: `2/15`
- Route: `2/15`

The channel is technically usable, but it is overloaded or route-constrained. So the score is not saying "vless quality is bad". It is saying "vless is working, but not a good target for more load right now".

This is the core semantic risk for the operator UI.

## 7. Planner Influence Audit

Planner decision owner:

- `tools/v7-users-autoswitch`

Planner scoring includes its own separate components:

- health
- service
- Telegram requirement
- speed
- stability
- latency
- load
- capacity
- quality history
- priority
- sticky bonus
- reserve penalty
- optional routing intelligence

Admin Channel Score is not this planner score.

Direct planner influence on admin score:

- no direct evidence found that planner ranking directly writes this `/100` value

Indirect influence:

- possible through operator decision/history labels
- possible through state surfaces consumed by the admin overview

Policy influence:

- yes
- capacity limits, load flags, enabled flags and route/topology state can reduce the score

Assignment influence:

- yes
- assigned users affect capacity/load pressure
- capacity pressure affects both Capacity and Route components

Conclusion:

Planner does not directly reduce Channel Score, but runtime/policy/assignment state can reduce it.

## 8. Health Vs Decision Separation

There are at least three different concepts in the system:

1. Technical/service health
2. Planner suitability
3. Admin channel score

They should not be treated as identical.

Technical/service health answers:

`Does the channel work?`

Planner suitability answers:

`Should this user be moved to this channel now?`

Admin channel score currently answers:

`How ready and healthy does this channel look as an operational target, considering services, runtime, load, route and history?`

That is a mixed operational readiness concept.

## 9. Trust Test

Question:

Can an operator safely read `72/100` as "channel quality is 72%"?

Answer:

No.

That interpretation is misleading.

A safer reading:

`72/100` means the channel has a mixed technical/operational readiness score of 72 under current service, runtime, load, route and history conditions.

A channel with `72/100` may still be working.

A channel with `89/100` may still be unsuitable for a specific user if planner policy, service requirements, organization rules or sticky behavior disagree.

## 10. Naming Audit

Current UI label:

`Technical Health`

Verdict:

`PARTIALLY_TRUTHFUL`

Why:

- Services, runtime and health are technical.
- Capacity, route pressure and history are operational decision context.
- Therefore the score is not purely technical health.

Better semantic labels:

- `Готовность канала`
- `Техническая готовность`
- `Состояние + нагрузка`
- `Операционная готовность`

No UI rename was implemented in this program.

## 11. Final Verdict

Final classification:

`MIXED_SCORE`

This score is not:

- pure technical quality
- pure service score
- pure planner score
- pure assignment score
- pure trust score
- pure recovery score

This score is:

- a composite channel readiness score
- suitable for quick operator diagnostics
- useful for explaining why a channel is good, degraded, overloaded or blocked
- unsafe as the only answer to "which channel should receive users"

## 12. Recommendation

Do not use this score as the authoritative planner decision.

Do not explain it to operators as "channel quality".

Use it as:

`diagnostic readiness`

Recommended next step, if product clarity is needed:

Create a separate UI semantics pass that clearly separates:

- service health
- load/capacity
- planner recommendation
- current assignment
- operator action needed

No implementation was performed in this audit.

## Final Verification Table

| Area | Status | Notes |
|---|---|---|
| Local | PASS | branch `Updatesystem`, report commit created |
| GitHub | PASS | `Updatesystem` pushed successfully |
| Runtime | NO-GO | runtime commit remains previous deployed commit |
| Truth | NO-GO | `runtime_local_commit_mismatch` caused by this report file being classified as `UNKNOWN` |
| Convergence | NO-GO | runtime action guard says `STOP_REVIEW_CHANGED_FILES` |

Post-commit verification result:

- report commit was pushed to GitHub
- deploy delta contains no runtime binary mismatches
- changed file since production: `CHANNEL_SCORE_REALITY_AUDIT.md`
- classifier verdict for this filename: `UNKNOWN`
- deployment required: `false`
- runtime action safe: `false`

Operational conclusion:

The score audit itself is complete, but the final truth gate exposed a documentation classification gap. The file is a report and should be treated as documentation-only, but the current runtime truth classifier does not recognize this exact report name.

No runtime code was changed.

Recommended next action:

Run a small truth-classification closure program for top-level audit reports, or move future reports into an already recognized documentation/evidence path. Do not deploy for this report-only mismatch.
