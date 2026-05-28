# E11.7 WireGuard Target Verification

Target:

```text
egress_id=wireguard-1779454504-c43409
interface=v7e06a394c478
canary_reserved=true
reservation_reason=second_canary_target
reservation_owner=control_plane_governance
```

Good target properties:

```text
diagnose=OK
quality_ok=true
interface=UP_LOWER_UP
route_get=OK
exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
waiver_required=false
```

Blocking target properties:

```text
users_count_from_registry=12
users_count_from_load_state=12
load_status=HARD_FULL
zero_user=false
selected_target=NONE
target_readiness_status=NO-GO
```

Current users on target:

```text
10.0.0.2
10.0.0.3
10.0.0.6
10.7.0.2
10.7.0.3
10.7.0.4
10.7.0.5
10.7.0.6
10.7.0.8
10.7.0.9
10.7.0.12
10.7.0.13
```

Verification decision:

```text
wireguard_clean_target=false
wireguard_production_occupied=true
wireguard_target_verification_status=NO-GO
```

The diagnose fix remains successful, but WireGuard cannot be used as a clean
isolated second-canary target while it is occupied by production users.
