# V7 VOZDUH — BLOCK 2.1 REPORT
## Autoswitch Signal Refinement & Oscillation Protection

Date: 2026-05-23 Europe/Moscow  
Scope: live production-like VPS runtime + local repository alignment  
Rule: no kill switch, routing, route classes, Trusted RU/Gosuslugi, or datapath changes

--------------------------------------------------
## 1. Historical Quality Influence Analysis

### Previous behavior

`tools/v7-users-autoswitch` treated high historical fail rate as a hard candidate blocker:

- `fail_rate >= 0.75`
- candidate rejected with `quality_history_fail_rate_high`

This was unsafe semantically because historical quality could dominate live usability. A route could be currently usable according to live service checks, but still be excluded as if it were live-broken because of older failure history.

### Risk

This created contradictory switch pressure:

- service matrix/live checks could say route is usable;
- historical quality could say route is unusable;
- autoswitch could over-prefer alternatives based on stale or long-window history;
- operator summary could show live state that does not explain autoswitch behavior.

This violates the Block 2 truth model:

- historical signals should influence confidence;
- live signals should describe current usability;
- hard policy/safety gates should remain separate.

### New behavior

Historical high fail rate is now advisory:

- it adds `quality_history_fail_rate_high_advisory`;
- it does not hard-block a currently usable route by itself;
- it still lowers confidence through explanations and candidate scoring context.

### Before/after semantics

Before:

```text
historical fail_rate high -> candidate blocked
```

After:

```text
historical fail_rate high -> caution/confidence modifier
live usability still decides current viability unless other gates block
```

### Verification evidence

Live dry-run after deployment showed:

```text
QUALITY_HISTORY_ADVISORY_CANDIDATES 32
SELECTED_MOVES 0
```

This confirms historical quality is still visible to the decision engine but no longer functions as a direct live hard blocker.

--------------------------------------------------
## 2. Oscillation Protection Design

### Confirmed problem

Previous live history showed same-pair reversal behavior:

```text
1 -> vless
vless -> 1
```

This is a classic short-window oscillation pattern. It is especially dangerous when health semantics are contradictory or sentinel/service signals are noisy.

### New protection model

Added same-pair reversal guard:

- default window: `900` seconds;
- policy key: `pair_reversal_window_seconds`;
- blocks candidate move when the user's last move was from target egress to current egress within the window.

Example:

```text
last move: A -> B
current: B
candidate: A
within 900s -> block with pair_reversal_stability_window
```

### Safety properties

This does not permanently forbid recovery.

It only requires a stability window before reversing the same pair. Autoswitch can still:

- move to another safe candidate;
- move after the reversal window expires;
- perform legitimate self-healing when supported by stronger persistence and safety signals.

### Verification evidence

Live autoswitch dry-run after deployment:

```text
PAIR_REVERSAL_BLOCKED_CANDIDATES 7
SELECTED_MOVES 0
```

Recent autoswitch journal after deployment showed rejected candidates with:

```text
pair_reversal_stability_window
```

This confirms the guard is active and reducing reversal pressure.

--------------------------------------------------
## 3. Capacity Visibility Implementation

### Previous state

Autoswitch already calculated dynamic load internally, but there was no persisted operator-facing capacity truth. Operator visibility had a gap:

- autoswitch could make load-aware decisions;
- operator summary could not show the same compact capacity state;
- Block 2 contradiction catalog showed missing `egress-load-summary.json`.

### New persisted summary

`tools/v7-users-autoswitch` now writes:

```text
/opt/v7/egress/state/egress-load-summary.json
```

The summary is read-only from an operator perspective and compact by design.

Fields:

- `schema_version`
- `updated`
- `source`
- `authority`
- `operator_status`
- `semantics`
- `summary`

Authority:

```text
capacity_signal
```

### Operator-facing load statuses

The persisted dynamic load summary uses restrained capacity semantics:

- `ok`
- `warm`
- `high`
- `full`
- `overloaded`

This is not a raw metrics dump. It is a compact truth source for operator understanding.

### Live capacity result

Current live capacity summary:

```text
operator_status: overloaded
active_users: 16
healthy_channels: 4
working_channels: 3
soft_limit: 7
hard_limit: 10
failover_hard_limit: 11
```

Per-egress:

```text
awg3: users=15 status=FAILOVER_FULL
awg0: users=1 status=OK
others: users=0 status=OK
```

### Interpretation

This is not a datapath failure, but it is an operational imbalance:

- `awg3` carries almost all active users;
- broad autoswitch movement should remain guarded;
- future action should be controlled drain/rebalance, not panic switching.

--------------------------------------------------
## 4. Service Severity Refinement

### Previous issue

`WARN` was too broad. Different service states could collapse into the same operator meaning:

- HTTP limited;
- degraded;
- blocked;
- partial;
- advisory;
- unknown.

This creates ambiguity for autoswitch and operator UX.

### New summary interpretation

`tools/v7-observability-summary` now separates more status semantics:

- `blocked`
- `degraded`
- `partial`
- `advisory`
- `unknown`

Specific limited states such as:

```text
HTTP_LIMITED
RATE_LIMITED
LIMITED
```

now normalize to:

```text
advisory
```

instead of being treated as a broad hard warning.

### Autoswitch interaction

This change does not rewrite service probes or autoswitch architecture. It improves operator truth and reduces pressure from ambiguous service states by making limited/advisory states visibly different from blocked/degraded states.

--------------------------------------------------
## 5. Exact Runtime Changes

### Local files changed

```text
tools/v7-users-autoswitch
tools/v7-observability-summary
```

### Live files changed

```text
/usr/local/bin/v7-users-autoswitch
/usr/local/bin/v7-observability-summary
```

### Live backups

```text
/usr/local/bin/v7-users-autoswitch.backup.block21-20260523-011107
```

The existing live `v7-observability-summary` was also backed up before replacement.

### Runtime state created/updated

```text
/opt/v7/egress/state/egress-load-summary.json
```

### What was not changed

No changes were made to:

- kill switch;
- nftables;
- route tables;
- route classes;
- direct/RU routing;
- Trusted RU/Gosuslugi handling;
- user registry structure;
- autoswitch timer frequency;
- Telegram sentinel timer;
- provisioning logic.

--------------------------------------------------
## 6. Exact Before/After Semantics

### Historical quality

Before:

```text
historical fail_rate >= 0.75 -> hard candidate block
```

After:

```text
historical fail_rate >= 0.75 -> advisory confidence/caution signal
```

### Same-pair reversal

Before:

```text
A -> B -> A possible if other gates allowed it
```

After:

```text
A -> B -> A blocked for pair_reversal_window_seconds, default 900s
```

### Capacity truth

Before:

```text
dynamic load existed inside autoswitch only
operator summary had no authoritative persisted capacity signal
```

After:

```text
autoswitch persists compact capacity signal
observability summary reads it as operator-facing capacity truth
```

### Service severity

Before:

```text
limited/advisory service states could collapse into broad warning semantics
```

After:

```text
limited states normalize to advisory
blocked/degraded remain stronger states
```

--------------------------------------------------
## 7. Verification Results

### Code verification

Local compile:

```text
python3 -m py_compile tools/v7-users-autoswitch tools/v7-observability-summary
OK
```

Live compile:

```text
python3 -m py_compile /usr/local/bin/v7-users-autoswitch /usr/local/bin/v7-observability-summary
OK
```

### Autoswitch dry-run after deployment

```text
users_total: 16
egress_total: 6
healthy_egress_total: 4
candidate_moves: 0
candidate_moves_total: 0
selected_moves: 0
reconnect_rotation_candidates: 0
rebalance_candidates: 0
```

Dynamic load:

```text
status: overloaded
active_users: 16
healthy_channels: 4
working_channels: 3
```

Signal counters:

```text
PAIR_REVERSAL_BLOCKED_CANDIDATES 7
QUALITY_HISTORY_ADVISORY_CANDIDATES 32
```

### Switch history stability

Before deployment:

```text
SWITCH_TOTAL 1171
SWITCH_LAST 2026-05-22T22:03:47.006757+00:00
```

After deployment and wait window:

```text
SWITCH_TOTAL_AFTER_WAIT 1171
SWITCH_LAST_AFTER_WAIT 2026-05-22T22:03:47.006757+00:00
SWITCHES_AFTER_BLOCK21_DEPLOY 0
```

No new switches occurred during the verification window after Block 2.1 deployment.

### Operator summary

`v7-observability-summary --pretty` reported:

```text
system.status: unstable
system.severity: critical
autoswitch_state: degraded
degraded_channels: 2
trusted_ru_state: unknown
```

Capacity group:

```text
status: overloaded
severity: critical
affected: 1
reason: capacity overloaded on 1 egress
suggested_action: avoid broad autoswitch movement
```

Contradictions decreased from 8 to 6 because capacity state is now persisted and visible.

### Runtime safety checks

```text
v7-killswitch-check: OK
v7-user-route-check: OK
v7-provisioning-reconcile-check: OK
```

No datapath regression was observed.

--------------------------------------------------
## 8. Remaining Instability Risks

### 1. Capacity imbalance remains real

`awg3` currently carries 15 users and is marked `FAILOVER_FULL`.

This is the main remaining operational risk after Block 2.1. The autoswitch is now calmer, but the platform is still imbalanced.

Recommended future action:

```text
controlled drain/rebalance plan
```

Not recommended:

```text
broad automatic migration
panic switching
```

### 2. Anti-flap/freeze pressure remains visible

Users are protected from repeated movement, but freeze/cooldown pressure means recovery must be slow and deliberate.

This is safer than oscillation, but operator visibility should continue to show:

- protected/frozen users;
- recent instability;
- skipped movement reason;
- overload state.

### 3. Health semantics are improved but not fully unified

Block 2 and Block 2.1 aligned major semantics, but some sources still remain advisory or partial:

- Trusted RU state remains unknown/unfinished;
- legacy quality entries still exist;
- service matrix and quality history still require continued careful interpretation.

### 4. Timers remain frequent

Autoswitch timer cadence was not changed in Block 2.1. The decision logic is calmer, but frequent runs still mean bad semantics could create pressure again if future changes weaken guards.

--------------------------------------------------
## 9. Did Autoswitch Become Calmer?

Yes, within the verified scope.

Evidence:

- no new switches after Block 2.1 deployment during verification window;
- selected moves stayed at `0`;
- same-pair reversal candidates were blocked;
- historical quality no longer hard-blocks live-usable candidates;
- capacity overload is visible instead of hidden;
- journal shows `applied=false` with `reason=no_selected_moves`.

This does not mean autoswitch is production-perfect. It means the immediate oscillation pressure is materially reduced.

--------------------------------------------------
## 10. Did Oscillation Pressure Decrease?

Yes.

Direct evidence:

```text
PAIR_REVERSAL_BLOCKED_CANDIDATES 7
SWITCHES_AFTER_BLOCK21_DEPLOY 0
```

The exact previously dangerous class of movement:

```text
A -> B -> A
```

now has a bounded stability window before reversal is allowed.

--------------------------------------------------
## 11. Final Verdict

Block 2.1 successfully converted autoswitch behavior from:

```text
bounded but still vulnerable to contradictory signal pressure
```

to:

```text
more cautious, reversal-aware, capacity-visible, and easier to explain
```

Production safety improved without touching datapath, route classes, kill switch, Trusted RU, or provisioning.

The biggest remaining production issue is no longer uncontrolled switch storm pressure. It is now:

```text
capacity imbalance on awg3 plus still-incomplete health semantics
```

The next real stabilization priority should be a controlled operator-visible drain/rebalance plan, not a routing redesign.
