# E25.8 Execution Target Metadata

## Result

`dedicated_execution_target_created=false`

No execution-only egress metadata was created.

Reason:

The replacement candidate did not prove handshake, RX packets, or target-local connectivity. Creating an execution target row for a non-usable profile would create operator confusion and a false readiness signal.

## Intended Metadata If A Candidate Passes

Future usable profile should use:

- `role=EXECUTION_ONLY`
- `soft_limit=1`
- `hard_limit=1`
- `manual_only=1`
- `reserve_only=1`
- `canary_reserved=true`
- `execution_reserved=true`
- `reservation_owner=operator_execution_governance`
- `autoswitch_allowed=false`
- `rebalance_allowed=false`
- `production_assignment_allowed=false`
- `service_tags=governance,execution`
- `exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU`
