# E9.3.6 Egress 1 Ineligibility Analysis

Mode: read-only autoswitch root-cause analysis.

## Verdict

```text
egress_1_ineligibility_root_cause=service_instagram_failed hard service gate during E9.3.5 final planner sample
root_cause_classification=MIXED_TRANSIENT_SERVICE_SIGNAL_AND_EXPECTED_FAILOVER_BEHAVIOR
confidence=high_for_E9_3_5_abort_sample_medium_for_current_runtime_persistence
```

## Evidence From E9.3.5 Final Planner Sample

The final E9.3.5 planner-only gate showed:

```text
candidate_moves=15
candidate_moves_total=15
selected_moves=3
apply_requested=False
```

For selected candidate decisions, current egress `1` was not eligible. The candidate payload for `1` included:

```text
eligible=false
blocked=["service_instagram_failed"]
reasons=["service_youtube_ok","telegram_degraded","service_google_ok","service_google_auth_ok","route_class_VIDEO_OPTIMIZED_warn"]
telegram.status=DEGRADED
telegram.ok=true
telegram.hard_blocked=false
telegram.score=40.0
role=GLOBAL_FAST
load.status=OK
users=16
```

Interpretation:

- `service_instagram_failed` was the hard blocker.
- Telegram degradation was present, but source semantics treat degraded Telegram as a scoring/reason signal unless hard-blocked.
- Load was not the blocker: load status was `OK`, with users below hard/failover limits.
- Quality was degraded enough to reduce score, but not the specific hard blocker in the selected move records.

## Current Runtime Snapshot

The E9.3.6 read-only snapshot shows:

```text
v7-health.service=active
v7-autoswitch-planner.timer=active
v7-users-autoswitch.timer=inactive
v7-reconcile-check=OK
v7-user-route-check=OK
v7-killswitch-check=OK
v7-provisioning-reconcile-check=OK
```

Current registry and route reality:

```text
all enabled users currently on egress 1
tables 100,101,104,1000-1004,1006-1013 default dev v7e356a192b79
route_get checks use v7e356a192b79
```

Current planner journal evidence sampled in E9.3.6 also includes decisions where egress `1` is again eligible for kept users:

```text
egress=1 eligible=true
blocked=[]
reasons include service_instagram_ok and telegram_down_grace/degraded
selected_moves=[]
apply_result.applied=false
```

This means the E9.3.5 ineligibility was not stable across later planner samples.

## Why VLESS Was Chosen

When current egress is not eligible, autoswitch runs the failover path. In the E9.3.5 sample, `vless` was the highest eligible failover candidate:

```text
vless eligible=true
load.status=OK
users=0
service_youtube_ok=true
service_instagram_ok=true
service_telegram_ok=true
service_google_ok=true
route_class_VIDEO_OPTIMIZED_ok=true
```

Therefore the chosen target was `vless`, not `awg3`.

## Classification

| Candidate Classification | Applies? | Reason |
|---|---:|---|
| REAL_EGRESS_1_DEGRADATION | partial | egress `1` had a real service failure signal for Instagram in the planner sample |
| TRANSIENT_SERVICE_SIGNAL | yes | later evidence shows egress `1` eligible again |
| TELEGRAM_SIGNAL_OVERWEIGHTED | no as hard cause | Telegram degraded score/reason existed but was not the hard eligibility block |
| POLICY_TOO_AGGRESSIVE | conditional | one service failure can mark current egress ineligible for many users |
| EXPECTED_FAILOVER_BEHAVIOR | yes | source logic explicitly failovers when current is not eligible |
| STALE_STATE | not primary | evidence shows live planner signals, not only stale state |
| MIXED | yes | transient service signal plus current policy semantics |

## Restore Implication

```text
apply_restore_safe_now=false
apply_should_remain_held=true
```

The key risk is not that egress `1` is currently broken. The risk is that service signal volatility can turn one transient service failure into 15 failover candidates, with up to 3 selected per apply run under current limits.
