# V7 Phase 102 — Egress Roles And Usage Policy

Date: 2026-05-08

## What Changed

Phase 102 adds route-purpose metadata to every new egress draft and disabled pool entry.

This does not change routing, kill switch rules, users, or running services by itself. It prepares V7 for service-aware routing by making every channel a typed V7 object instead of just a VPN config.

## Added Channel Fields

- `role`
- `priority`
- `weight`
- `soft_limit`
- `hard_limit`
- `manual_only`
- `reserve_only`
- `service_tags`
- `exclude_route_classes`

## Supported Roles

- `GLOBAL_FAST`
- `GLOBAL_STABLE`
- `VIDEO_OPTIMIZED`
- `LOW_LATENCY`
- `DIRECT_RU`
- `TRUSTED_RU_SENSITIVE`
- `RESERVE`
- `MANUAL_ONLY`

## Safety Rules Preserved

- New egress still starts as draft.
- Pool apply still adds only `enabled=0`.
- Runtime profile provisioning is still separate.
- Enable is still a separate guarded action.
- Existing egresses are not rewritten.
- Users are not moved.
- Routing is not changed.
- Kill switch is not changed.
- Secrets are not displayed in UI result cards.

## Admin UI Changes

The Add Egress wizard now includes a Role step:

- role selector
- priority
- weight
- soft/hard user limits
- service tags
- route-class exclusions
- reserve-only flag
- manual-only flag

The egress table now shows the channel role, and the egress detail modal shows pool policy fields.

## Registry Compatibility

The fields are appended to `egress.registry` as ordinary `key=value` tokens. Existing scripts that do not know these keys continue to work.

Example:

```text
id=example protocol=vless type=proxy interface= test=socks5://127.0.0.1:21001 enabled=0 config=/etc/v7/egress-runtime/example/config.json role=GLOBAL_FAST priority=20 weight=100 soft_limit=1 hard_limit=2 manual_only=0 reserve_only=0 service_tags=google,telegram,instagram,global exclude_route_classes=TRUSTED_RU_SENSITIVE,DIRECT_RU
```

## Verification

Local checks:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/v7_pycache python3 -W error -m py_compile admin/v7-admin-api hardening/v7-egress-draft-runtime-helper
git diff --check
```

Manual admin checks:

1. Open `http://127.0.0.1:7080/login`.
2. Go to `Egress`.
3. Click `Add Egress Draft`.
4. Paste a supported VPN URI or config.
5. Pick a role, for example `RESERVE`.
6. Click `Detect`.
7. Confirm the result card shows `Usage Policy`.
8. Click `Save Draft`.
9. Confirm the saved drafts table shows the selected role.

## Next Phase

Phase 103 should use these roles in service-aware onboarding and show the per-service matrix as route-class fitness, not just generic OK/FAIL.
