# E25.6 Disabled Draft Target Plan

## Result

- `disabled_draft_target_prepared=true`
- `target_activation_deferred=true`
- `runtime_registry_mutation=false`
- `egress_registry_mutation=false`

No live metadata row was written in E25.6. This is the exact draft shape for the next block.

## Draft Metadata

```json
{
  "target_name": "wireguard-exec-20260528-10-89-0-2",
  "protocol": "wireguard",
  "role": "EXECUTION_ONLY",
  "enabled": 0,
  "soft_limit": 1,
  "hard_limit": 1,
  "manual_only": 1,
  "reserve_only": 1,
  "canary_reserved": true,
  "execution_reserved": true,
  "reservation_owner": "operator_execution_governance",
  "autoswitch_allowed": false,
  "rebalance_allowed": false,
  "production_assignment_allowed": false,
  "service_tags": ["governance", "execution"],
  "exclude_route_classes": ["TRUSTED_RU_SENSITIVE", "DIRECT_RU"],
  "source_profile_hash": "666cf51365f7e145726f7db7c503577ff2b5a872ae7351486cb41fd1316e0ff1",
  "interface_name": "v7execwg0",
  "route_table": 1250
}
```

## Activation Gate

Activation remains forbidden until E25.7 performs:

- normalized profile write;
- interface activation;
- zero-user validation;
- target readiness validation;
- long stability window;
- governance isolation validation;
- restore-settle validation.

