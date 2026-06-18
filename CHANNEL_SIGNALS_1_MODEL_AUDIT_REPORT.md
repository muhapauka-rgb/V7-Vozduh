# CHANNEL.SIGNALS.1 Model Audit Report

Project: V7 VOZDUH  
Program: CHANNEL.SIGNALS.1_MODEL_AUDIT  
Mode: architecture only, no implementation

## 1. Signal Inventory

Reference First was completed before this audit. The canonical reference, ADR-002, ADR-003, ADR-004, ADR-005, System Map, `CHANNEL_SCORE_REALITY_AUDIT.md`, and `CHANNEL_ROUTE_COMPONENT_REALITY_AUDIT_REPORT.md` were read before producing a new audit.

New audit was allowed because the reference defined existing concepts, but did not yet define the final A/B/C operator signal classification.

| Signal | Current Meaning |
|---|---|
| V7 Decision / Assignment | Planner-derived role: Use, Keep Current Users, Evacuate, Emergency Only, Blocked. |
| Main Blocker / Reason | Human explanation of the assignment or decision blocker. |
| Technical Health / Channel Score | Mixed 0-100 technical/operational readiness score. Not assignment truth. |
| Services | Service matrix availability and freshness. |
| Stability | Runtime/lifecycle health and planner stability floor context. |
| Capacity / Load | Current/projected user pressure against soft/hard limits. |
| Route | Topology/readiness confidence signal, not direct traffic quality. |
| Runtime Readiness | Whether runtime profile/state is ready and readable. |
| History | Recent trust/decision/evidence state used for explanation. |
| Users | Number of users currently affected by the channel state. |
| Speed | Planner/diagnostic quality signal, especially for complaints or hard gates. |
| Role Flags | Manual/reserve/canary/production-assignment restrictions. |
| Trust / Recovery | Historical/advisory state, not current planner truth by itself. |
| Traffic | Usage volume, not health or assignment truth. |
| Evidence / Logs / Execution | Technical proof and governed action context. |

## 2. Signal Classification

| Signal | Category | Reason |
|---|---|---|
| V7 Decision / Assignment | A - Operator Signal | Answers what V7 wants to do with the channel. |
| Main Blocker / Reason | A - Operator Signal | Explains the decision without requiring internals. |
| Users / Affected Users | A - Operator Signal | Tells the operator how many people are affected. |
| Capacity as Headroom/Full/Overloaded | A - Operator Signal | Best operator wording for "can accept more users". |
| Services as OK/Degraded/Failed | A - Operator Signal when degraded, B when OK | Service failure is directly meaningful; full matrix detail is not. |
| Role as Use/Emergency/Reserve/Blocked | A - Operator Signal | Role changes permitted use. Raw role flags are diagnostic. |
| Technical Health / Mixed Score | B - Supporting Signal | Useful for confidence and investigation, unsafe as primary truth. |
| Stability as human blocker | B - Supporting Signal | Important when it blocks assignment; raw floor/code stays diagnostic. |
| Route | B - Supporting Signal | Readiness confidence and topology context, not primary quality. |
| Runtime Readiness | B - Supporting Signal | Important if not ready; otherwise quiet. |
| Speed | B - Supporting Signal | Important for speed complaints or planner gates; raw values are detail. |
| History | B/C - Supporting or Diagnostic | Useful after a problem is selected; not first-screen truth. |
| Trust / Recovery | C - Diagnostic Only | Advisory/history unless converted into a current decision blocker. |
| Score Components | C - Diagnostic Only | Explain score, but should not drive operator action first. |
| Traffic | C - Diagnostic Only | Usage/analytics, not readiness. |
| Evidence / Logs / Execution | C - Diagnostic Only | Proof and governed flow, not table-level signals. |

## 3. Route Classification

Final route classification: `Supporting Signal`.

Evidence:

- `CHANNEL_ROUTE_COMPONENT_REALITY_AUDIT_REPORT.md` classified Route as `READINESS_CONFIDENCE_SIGNAL`.
- The current route component is calculated from `channelTopologyState(row)`.
- `channelTopologyState(row)` can reduce Route because of service failure or hard capacity/load, even when route reality rows are confirmed.
- Route does not directly measure speed, latency, packet loss, or real user traffic quality.

Therefore Route should not be shown as a top-level "quality" signal. It belongs in compact details or technical diagnostics as route/topology readiness.

## 4. Capacity Model Recommendation

`CAPACITY_MODEL_RECOMMENDATION`: show operator-facing `Load / Headroom`, not raw `Capacity` score.

Best operator language:

| Raw Concept | Operator Signal |
|---|---|
| Below soft limit | Has room |
| At soft limit / warn | Near limit |
| Hard full / over limit | Overloaded |
| Current users | Users on channel |
| Assignment capacity | Can receive users / Cannot receive more |

Why: the operator question is not "what is the capacity component score?", but "can this channel accept more users without overload?"

## 5. Commercial Pattern Report

Mature operator systems do not rely on one mixed score as the only operational answer.

| Product Pattern | Observed Philosophy |
|---|---|
| Cloudflare | Separate status, traffic, security, routing, and incident signals. |
| Datadog | Multiple monitors and facets; one rollup does not replace diagnosis. |
| Grafana | Dashboards show multiple signals and alert states, not one universal score. |
| AWS | Health, capacity, limits, service state, and events are separated. |
| Kubernetes | Conditions, readiness, phase, events, and resource pressure are distinct. |
| Linear | Work is problem/status first; details stay behind the item. |
| PagerDuty | Incident severity and impacted service are primary; metrics are supporting. |

`COMMERCIAL_PATTERN_REPORT`: use multiple simple operator signals. A single mixed score is acceptable only as supporting health context.

## 6. Table Model Options

### Option A: Channel / Decision / Score / Users

Pros:

- Simple.
- Keeps current score visible.

Cons:

- Still implies score explains too much.
- Does not show why a good score can be blocked.
- Weak for capacity/service/route mismatches.

Operator clarity: medium.

### Option B: Channel / Signals / Decision / Users

Pros:

- Exposes multiple signals.
- Makes score less dominant.

Cons:

- Puts signals before the actual decision.
- Operator must interpret before seeing what V7 decided.

Operator clarity: medium-high, but slower.

### Option C: Channel / Decision / Signals / Users

Pros:

- Decision-first.
- Signals explain the decision without replacing it.
- Users column shows impact.
- Mixed score can remain behind Signals/tooltip/details.

Cons:

- Requires compact signal design to avoid density.

Operator clarity: highest.

Recommendation: Option C.

## 7. Drawer Model Options

### Option 1: Decision / Score / Problems / Works / Diagnostics

Clear, but score is still too prominent.

### Option 2: Decision / Signals / Problems / Works / Diagnostics

Best balance. Decision answers the task, signals explain why, problems give investigation entry, diagnostics stay last.

### Option 3: Signals / Decision / Diagnostics

Too object-centric and makes operators infer action.

Recommendation:

```text
Decision
Signals
Problems
Works
Diagnostics
```

Drawer rules:

- Decision is first.
- Signals are compact badges or rows.
- Problems are clickable investigation entries.
- Works is collapsed/compact.
- Diagnostics contains Technical Health, score components, evidence, history, logs, and execution context.

## 8. Sorting Model

Mixed score must not be the default sort.

Final sorting recommendation:

1. Decision severity.
2. Affected users.
3. Worst operator signal.
4. Signal count.
5. Channel name.

Decision severity order:

| Priority | Decision |
|---:|---|
| 1 | Evacuate |
| 2 | Blocked with users |
| 3 | Overloaded / service failed with users |
| 4 | Emergency Only |
| 5 | Keep Current Users |
| 6 | Blocked without users |
| 7 | Use |

Worst signal order:

| Priority | Signal |
|---:|---|
| 1 | Users should leave |
| 2 | Service failure |
| 3 | Overloaded |
| 4 | Runtime not ready |
| 5 | Stability below required level |
| 6 | Route readiness not confirmed |
| 7 | History insufficient |
| 8 | Healthy/working |

## 9. Tooltip Model

Tooltips explain. They do not introduce actions, validators, or new workflows.

| Signal | Tooltip |
|---|---|
| Decision | `V7 planner decision for this channel: use, keep, evacuate, emergency only, or blocked.` |
| Services | `Measured service availability, for example 13/14 services work.` |
| Capacity / Load | `Current users and limits, for example 11 users assigned; new assignments restricted.` |
| Route | `Topology/readiness confidence. This is not direct traffic speed or packet loss.` |
| Runtime | `Whether V7 can prove the channel runtime/profile is ready.` |
| Stability | `Whether channel stability is above the required planner floor.` |
| History | `Recent trust/recovery/evidence state used for confidence.` |
| Technical Health | `Mixed score from services, stability, capacity, route, runtime, and history. Not assignment truth.` |
| Users | `Number of users currently assigned or affected.` |

## 10. Final Recommendation

Final signal list:

| Layer | Signals |
|---|---|
| Primary operator | Decision, reason/blocker, affected users, capacity/load posture, service failure if present. |
| Supporting | Technical Health, route readiness, runtime readiness, stability, speed, service summary, history summary. |
| Diagnostics only | Raw score components, raw trust/recovery, raw route rows, raw service matrix rows, traffic, evidence, logs, execution internals. |

Final table structure:

```text
Channel | Decision | Signals | Users
```

Signal cell should be compact. Example:

```text
Overloaded
Services OK
Route readiness check
```

Final drawer structure:

```text
Decision
Signals
Problems
Works
Diagnostics
```

Final sorting:

```text
Decision severity -> affected users -> worst operator signal -> signal count -> channel name
```

Final tooltip structure:

```text
Signal name
One-sentence meaning
Current value
No action
```

Reference updates:

- `docs/reference/V7_CANONICAL_REFERENCE.md` now includes `Channel Operator Signal Model`.
- `docs/reference/SYSTEM_MAP.md` now includes the signal model module.
- `docs/decisions/ADR-006-channel-operator-signal-model.md` records the decision.

## 11. Final Verdict

`SIGNAL_MODEL_READY`

The final operator model is multi-signal and planner-first:

- V7 Decision is primary.
- Mixed score is supporting/diagnostic.
- Route is supporting readiness confidence.
- Capacity is operator-facing as headroom/load/overload.
- Diagnostics remain deeper.
- No new planner, score, workflow, truth source, storage, UI implementation, or runtime path is required.

## Verification

| Check | Status |
|---|---|
| Local state | PASS at audit start, only unrelated handoff doc untracked |
| GitHub | PASS after escalated truth gate |
| Runtime | PASS, docs-only mismatch ignored |
| Truth | PASS / FULLY_ALIGNED |
| Convergence | PASS / ALIGNED |
