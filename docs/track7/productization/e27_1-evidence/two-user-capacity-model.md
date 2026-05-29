# E27.1 Two User Capacity Model

## Candidate Pair

```text
candidate_user_A=10.7.0.11 table=1009 current=1
candidate_user_B=10.7.0.12 table=1010 current=1
```

## Target

```text
target=amneziawg-exec-20260528-10-8-1-14
interface=v7execwg0
role=EXECUTION_ONLY
```

## Evidence

Pre-requalification quality:

```text
stability.state avg_mbps=65.7833
stability.state min_mbps=55.30
stability.state stability=0.840639
```

Target-local parallel 5MB probe:

```text
probe_count=10
avg_mbps=38.192
min_mbps=13.02
all_samples_above_10=true
```

Post-requalification long window:

```text
sample_count=20
avg_mbps=68.561
min_mbps=19.037
no_sample_below_floor=true
readiness_all_go=true
runtime_checkers_ok=true
target_users_zero=true
```

## Model

Two-user forward movement would temporarily place two explicitly approved users on the execution target. The target now has:

```text
soft_limit=2
hard_limit=2
```

The modeled target state is therefore capacity-aligned with `movement_budget=2`.

## Verdict

`capacity_model_safe=true`

