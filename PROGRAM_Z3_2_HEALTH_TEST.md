# PROGRAM Z3.2 Health Test

## Objective

Test health degradation, health recovery, and autonomy behavior.

## Live Evidence

The selected target was healthy enough for one bounded move:

- target: `awg3`
- avg_mbps: `71.83`
- min_mbps: `55.03`
- stability: `0.766`
- telegram: `OK`
- route verification after move: `OK`
- route verification after rollback: `OK`

## Non-Executed Stress

Z3.2 did not intentionally degrade live target health or force recovery behavior in production runtime.

## Existing Coverage

`tests/unit/test_v7_users_autoswitch_policy.py` covers service degradation handling:

- soft degradation does not trigger failover.
- persistent or hard service failure can trigger bounded failover.
- restore-stage service-signal failover requires approval.
- generation clearance and budget guards can suppress selected moves.

## Verdict

- baseline_health_ok=true
- route_health_verified_after_move=true
- route_health_verified_after_rollback=true
- live_health_degradation_injected=false
- live_health_recovery_tested=false
- health_handling_certified=false

