# V7 Service-Aware Routing Dry Run

Date: 2026-05-08

## What Changed

Added a read-only service-aware route selection engine.

It calculates which route/channel should be used for each traffic class, but does not apply anything.

## Why

V7 now stores:

- egress roles;
- service matrix results;
- route-class fitness;
- policy domain groups.

This dry-run connects those pieces into one decision preview.

## Route Classes

The dry-run currently evaluates:

- `DIRECT_RU`
- `TRUSTED_RU_SENSITIVE`
- `VIDEO_OPTIMIZED`
- `GLOBAL_FAST`
- `GLOBAL_STABLE`
- `LOW_LATENCY`

## Important Safety Behavior

The dry-run never changes:

- routing;
- users;
- kill switch;
- `egress.registry`;
- `users.registry`;
- systemd services.

It only returns a plan.

## Conservative Sensitive RU Rule

`TRUSTED_RU_SENSITIVE` requires an enabled egress with role `TRUSTED_RU_SENSITIVE`.

This is intentional.

A temporary/global VLESS channel must not silently become the official route for Gosuslugi, ESIA, banks, or tax services.

If no dedicated sensitive route exists, dry-run returns:

```text
BLOCKED_REQUIRED_TRUSTED_PATH
```

## Admin UI

In `Service-aware Policy`:

- button: `Service-Aware Dry Run`;
- output: route-class selection table;
- output: domain sample table;
- output: technical JSON.

## API

Endpoint:

```text
POST /api/actions/service-aware-route-dry-run
```

Input:

```json
{
  "user_ip": "10.0.0.3"
}
```

## Verification

Local smoke test confirmed:

- `TRUSTED_RU_SENSITIVE` selects only a dedicated sensitive egress;
- `GLOBAL_FAST` selects a global role egress;
- `DIRECT_RU` stays on `V7_DIRECT_RU`;
- all safety flags are false for changes.

## Next Step

After reviewing dry-run output in real operation, the next phase is an apply-preview generator:

1. convert dry-run route selections into proposed route-class registry updates;
2. show diff;
3. backup;
4. guarded apply;
5. still keep live fwmark routing disabled until an explicit rollout phase.
