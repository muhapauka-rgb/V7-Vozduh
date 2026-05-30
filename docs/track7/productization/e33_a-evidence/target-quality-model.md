# E33.A Target Quality Model

target_quality_model_defined=true

## Quality Dimensions

Target quality must include:

- global quality;
- per-service quality;
- per-user required-service quality;
- load;
- capacity status;
- incident state;
- confidence.

## Global Quality

Global target quality includes:

```text
target_reachability
target_throughput
target_latency
target_packet_loss
target_load
capacity_status
incident_state
global_confidence
```

## Per-Service Quality

Per-service target quality joins target and service:

```text
target_id
service_id
service_status
service_latency
service_error_rate
service_timeout_rate
service_confidence
last_checked
```

## Per-User Required-Service Quality

Per-user target quality joins:

```text
user_id
target_id
required_services
service_health_by_required_service
required_service_fit
user_specific_status
```

## Important Rule

A target can be globally OK but user-specific NOT_OK.

Example:

```text
target_global_quality=OK
user_required_services=["youtube","telegram","instagram"]
target.youtube=SERVICE_OK
target.telegram=SERVICE_FAIL
target.instagram=SERVICE_OK
user_specific_health=USER_TARGET_FAIL
```

## Decision

target_quality_model_defined=true
