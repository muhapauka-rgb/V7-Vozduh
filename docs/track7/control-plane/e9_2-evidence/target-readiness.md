# E9.2 Target `1` Readiness

Mode: read-only approval packet only.

## Registry Evidence

```text
id=1
protocol=amneziawg
type=interface
interface=v7e356a192b79
enabled=1
role=GLOBAL_FAST
priority=20
weight=100
soft_limit=1
hard_limit=2
manual_only=0
reserve_only=0
exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
```

Interface evidence:

```text
v7e356a192b79: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 state UNKNOWN
```

Health/state evidence:

```text
egress-diagnose: 1_diagnose_reason=OK
egress-diagnose: 1_diagnose_severity=OK
egress-diagnose: 1_diagnose_detail=handshake_age_seconds=96
stability: 1_avg_mbps=60.067
stability: 1_min_mbps=46.59
stability: 1_stability=0.775634
stability: 1_samples=30
load-summary: 1.status=OK
load-summary: operator_status=warm
```

## Readiness Concern

The current target evidence is not perfectly clean:

```text
egress-load.state: 1_users=1
egress-load.state: 1_soft_limit=1
egress-load.state: 1_hard_limit=2
egress-load.state: 1_load_status=SOFT_FULL
egress-load-summary.json: per_egress.1.users=1
```

At the same time, fresh `v7-reconcile-check` shows all enabled users, including `10.7.0.15`, currently on `vless`, and the registry hash stayed at the E9.1 baseline. This means target `1` is interface/health-ready, but load-state has a stale or planner-derived occupancy signal that must be treated as an execution blocker unless explicitly waived.

## Target Verdict

```text
target_1_interface_ready=true
target_1_health_ready=true
target_1_load_state_clean=false
target_1_ready_for_unwaived_live_execution=false
target_1_ready_for_approval_packet=true
```

Target `1` remains the best target for a second mechanics approval packet because it was live-proven in E9. It is not unconditionally ready for E9.3 execution until the stale/soft-full load signal is explained, clears, or receives explicit one-user mechanics waiver.
