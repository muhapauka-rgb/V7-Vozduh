# V7 VOZDUH — BLOCK 2.2 REPORT
## Controlled Drain & Safe Rebalance Planning

Date: 2026-05-23 Europe/Moscow  
Live VPS: `195.2.79.116`  
Scope: read-only live runtime audit and rebalance planning  
Rule: no datapath, kill switch, route class, Trusted RU/Gosuslugi, or routing architecture changes

--------------------------------------------------
## 1. Live Capacity Map

### Current live finding

The initial Block 2.2 assumption was:

```text
awg3 = overloaded / FAILOVER_FULL
15 users on awg3
```

That is no longer the live state.

Current live state at `2026-05-23T14:50 MSK`:

```text
current_counts:
  vless: 16 users
```

Autoswitch dry-run:

```text
users_total: 16
egress_total: 6
healthy_egress_total: 2
candidate_moves: 0
candidate_moves_total: 0
selected_moves: 0
reconnect_rotation_candidates: 0
rebalance_candidates: 0
```

Dynamic capacity:

```text
active_users: 16
total_channels: 6
healthy_channels: 2
degraded_or_dead_channels: 4
reserve_channels: 1
working_channels: 1
avg_load: 16.0
soft_limit: 19
hard_limit: 24
failover_hard_limit: 32
status: ok
```

Operator summary capacity:

```text
status: healthy
reason: capacity within soft limits
```

### Per-egress user distribution

```text
vless: 16 users, load OK
1: 0 users, load OK
awg0: 0 users, load OK
awg3: 0 users, load OK
openvpn-1779388847-d2ad7c: 0 users, load OK
wireguard-1779454504-c43409: 0 users, load OK
```

### Capacity verdict

There is no current `awg3` overload.

There is still a platform concentration risk:

```text
all active users are on one egress: vless
```

This is not currently over the dynamic soft limit, but it is not a mature balanced posture either. The platform effectively has one preferred working primary and one weaker/partially degraded alternate.

--------------------------------------------------
## 2. awg3 Overload Explanation

### What happened

Block 2.1 observed `awg3` carrying 15 users. By the time Block 2.2 inspected live runtime, autoswitch had already moved users away from `awg3` and concentrated them on `vless`.

Recent safety/switch history shows the platform kept moving through multiple failover pairs earlier in the day.

Switch pairs since `2026-05-23T00:00:00Z`:

```text
awg0 -> 1: 22
1 -> vless: 34
vless -> awg0: 11
vless -> awg3: 3
1 -> awg3: 6
awg3 -> 1: 7
awg3 -> awg0: 5
vless -> 1: 26
awg3 -> vless: 6
awg0 -> awg3: 7
1 -> awg0: 22
awg0 -> vless: 11
```

The final observed wave moved users from `1` to `vless`:

```text
2026-05-23T08:39:17Z  1 -> vless
2026-05-23T08:40:17Z  1 -> vless
2026-05-23T08:54:33Z  1 -> vless
2026-05-23T08:54:53Z  1 -> vless
2026-05-23T08:55:58Z  1 -> vless
2026-05-23T09:05:24Z  1 -> vless
```

### Why `awg3` lost eligibility

Current candidate evaluation rejects `awg3` for all users:

```text
blocked:
  avg_mbps_below_floor: 16 users
  min_mbps_below_floor: 16 users

current observed:
  avg_mbps: ~9.82 Mbps
  min_mbps: ~5.74 Mbps
  stability: ~0.585

policy floors:
  min_avg_mbps: 15.0
  min_floor_mbps: 10.0
  min_stability: 0.45
```

So `awg3` is no longer a safe rebalance target. It was previously dominant because autoswitch failover waves had placed users there, not because it was a stable long-term capacity target.

### Why `vless` became dominant

Current candidates show:

```text
vless:
  eligible_users: 16
  best_score: ~2097
  telegram: OK
  avg_mbps: ~54 Mbps
  min_mbps: ~53 Mbps
  stability: ~0.978
  quality_trend: stable

1:
  eligible_users: 16
  best_score: ~1999
  telegram: DEGRADED
  avg_mbps: ~62 Mbps
  min_mbps: ~60 Mbps
  stability: ~0.962
```

`1` is fast and technically eligible, but it carries Telegram degradation and lower effective score. `vless` wins because it is current/sticky, Telegram OK, stable, and above all quality floors.

--------------------------------------------------
## 3. Candidate Rebalance Targets

### Candidate: `vless`

Status:

```text
current primary
16 users
load OK
Telegram OK
stable quality
```

Verdict:

```text
safe to keep, not a drain target right now
```

### Candidate: `1`

Status:

```text
0 users
eligible for 16 users
score lower than vless
Telegram DEGRADED, but not hard blocked
fast throughput
stable quality
```

Verdict:

```text
possible future controlled alternate, but not safe for automatic drain while Telegram is degraded and all users are frozen
```

### Candidate: `awg0`

Status:

```text
0 users
blocked for 16 users
min_mbps_below_floor
stability_below_floor
```

Verdict:

```text
not a safe rebalance target
```

### Candidate: `awg3`

Status:

```text
0 users
blocked for 16 users
avg_mbps_below_floor
min_mbps_below_floor
```

Verdict:

```text
not a safe rebalance target
```

### Candidate: `openvpn-1779388847-d2ad7c`

Status:

```text
0 users
blocked for 16 users
severity_SUSPECT
historical fail_rate ~0.9998
```

Verdict:

```text
not a safe rebalance target
```

### Candidate: `wireguard-1779454504-c43409`

Status:

```text
0 users
blocked for 16 users
severity_SUSPECT
historical fail_rate ~0.9998
```

Verdict:

```text
not a safe rebalance target
```

--------------------------------------------------
## 4. Dry-Run Migration Plan

### Autoswitch dry-run result

```text
selected_moves: 0
rebalance_candidates: 0
candidate_moves: 0
```

### Recommended dry-run plan

No movement should be applied now.

Reason:

```text
16 users are currently frozen by anti-flap safety
vless is under soft limit
only one alternate is eligible
the eligible alternate has Telegram degradation
all other targets are blocked
```

### Hypothetical future one-wave plan

Only if future checks show:

```text
vless remains near or above soft limit
1 has Telegram OK for a stability window
users are no longer frozen
no recent switch storm
autoswitch dry-run recommends rebalance
```

then a safe one-wave plan could be:

```text
move 1 user from vless -> 1
wait at least 15 minutes
verify route, service matrix, Telegram, reconnect state
stop if any degradation appears
```

This is not justified right now.

--------------------------------------------------
## 5. Safe Migration Rules

For V7, controlled drain/rebalance should follow these rules.

### Hard no-move conditions

Do not move users when:

```text
anti-flap frozen users > 0 for the target cohort
target has Telegram DEGRADED and Telegram is important for those users
target has avg/min throughput below floor
target has severity_SUSPECT
target is quarantined
target is blocked by policy
target would create same-pair reversal
recent failover storm occurred inside the stability window
```

### Wave sizing

For current 16-user platform:

```text
normal drain wave: 1 user
maximum drain wave: 2 users only if confidence is high
minimum wait between waves: 900 seconds
```

### Candidate requirements

A safe target should have:

```text
eligible for route class
Telegram OK if Telegram is important
no severity_SUSPECT
avg/min throughput above floor
stability above floor
no current quarantine
no same-pair reversal
capacity below soft limit after projected move
```

### Rollback posture

Every manual/controlled movement should preserve:

```text
before user -> egress assignment
after user -> egress assignment
reason
actor
timestamp
rollback target
verification result
```

--------------------------------------------------
## 6. Alternative Egress Evaluation

| Egress | Current Users | Eligibility | Main Blocker | Live Verdict |
|---|---:|---:|---|---|
| `vless` | 16 | 16/16 | none | Keep; current safest primary |
| `1` | 0 | 16/16 | Telegram degraded, lower score | Watch as future alternate; no movement now |
| `awg0` | 0 | 0/16 | min Mbps + stability below floor | Not safe |
| `awg3` | 0 | 0/16 | avg/min Mbps below floor | Not safe |
| `openvpn-1779388847-d2ad7c` | 0 | 0/16 | `severity_SUSPECT` | Not safe |
| `wireguard-1779454504-c43409` | 0 | 0/16 | `severity_SUSPECT` | Not safe |

--------------------------------------------------
## 7. Risk Analysis

### Removed risk

The specific Block 2.1 risk:

```text
awg3 overloaded with 15 users
```

is no longer present.

### Current primary risk

The current risk is:

```text
single-egress concentration on vless
```

This is lower urgency than `FAILOVER_FULL`, because dynamic capacity says `vless` is still within soft limits. But it is still not a resilient platform posture.

### Why movement is risky now

Movement is currently risky because:

```text
16 users are frozen by anti-flap
recent switch history is noisy
alternative egress are mostly unsafe
the only eligible alternate has Telegram degradation
current egress is healthy and below soft capacity
```

### Autoswitch behavior

Autoswitch is behaving calmly now:

```text
apply_result: no_selected_moves
selected_moves: 0
candidate_moves: 0
```

This is the correct behavior under the current conditions.

--------------------------------------------------
## 8. Is Movement Currently Justified?

No.

Any immediate manual move would violate the sprint philosophy:

```text
no panic migration
no broad automatic movement
no movement during ambiguous health
respect anti-flap safety
```

The correct current operator action is:

```text
observe vless capacity
wait for anti-flap freezes to expire
watch egress 1 Telegram status
do not use awg3/awg0/openvpn/wireguard as rebalance targets until blockers clear
```

--------------------------------------------------
## 9. Verification Results

### Required checks

```text
v7-killswitch-check: OK
v7-user-route-check: OK
v7-provisioning-reconcile-check: OK
```

### Route reality

All checked users route through expected `vless/tun0` assignments:

```text
registry assignment: vless
expected interface: tun0
route_get: tun0
```

### Observability summary

```text
system.status: unstable
system.severity: critical
autoswitch_state: degraded
trusted_ru_state: unknown
attention_incidents: 6
```

Autoswitch group:

```text
status: degraded
affected: 16
reason: 16 users frozen by anti-flap safety
```

Capacity group:

```text
status: healthy
reason: capacity within soft limits
```

### Timer status

`v7-users-autoswitch.timer` remains active.

Recent service run:

```text
ExecStart=/usr/local/bin/v7-users-autoswitch --apply
status=0/SUCCESS
apply_result: no_selected_moves
```

No datapath regression was observed.

--------------------------------------------------
## 10. Remaining Instability Risks

### 1. Single viable primary

`vless` is currently carrying all users. It is not overloaded by the current dynamic model, but it is a single concentration point.

### 2. Only one alternate is eligible

`1` is eligible, but Telegram is degraded. It should not be used for a calm rebalance wave yet.

### 3. Four egress are effectively not usable for rebalance

```text
awg0: weak min throughput/stability
awg3: weak avg/min throughput
openvpn: severity_SUSPECT
wireguard: severity_SUSPECT
```

### 4. Anti-flap freeze is still protecting users

This is good safety, but it also means manual rebalance now would fight the safety model.

### 5. Historical switch storm remains in memory

Recent switch history still shows high churn. Even if current state is calmer, the system should remain conservative until history ages out.

--------------------------------------------------
## 11. Final Verdict

Block 2.2 should not perform a migration.

The live platform no longer has the exact `awg3 FAILOVER_FULL` issue. It has evolved into:

```text
vless concentration with capacity OK,
anti-flap freeze active,
and no safe rebalance target except a degraded alternate.
```

The safest controlled drain strategy is:

```text
no movement now
watch vless capacity
wait for anti-flap expiry
promote egress 1 only after Telegram returns OK for a stability window
keep awg0/awg3/openvpn/wireguard excluded until their blockers clear
```

This keeps V7 aligned with Governance:

- stability first;
- no panic balancing;
- no hidden movement;
- no datapath changes;
- bounded operator-visible action only.

--------------------------------------------------
## 12. Recommended Next Engineering Step

Do not rebalance immediately.

Next safe engineering step should be operator visibility, not routing movement:

```text
Capacity: vless carries 16/19 soft limit
Autoswitch: guarded, no selected moves
Users: 16 protected by anti-flap
Safe alternate: none currently recommended
Watch: egress 1 Telegram degradation
```

If a future manual action is needed, it should be a separate explicitly approved one-wave operation:

```text
move exactly 1 user from vless -> 1
only after egress 1 Telegram status is OK
only after anti-flap freeze expires
verify immediately after move
```
