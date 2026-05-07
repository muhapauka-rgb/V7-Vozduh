# V7 Phase 42: Service-aware policy apply preview

Date: 2026-05-07

## Goal

Add a safe apply-preview layer for service-aware routing.

This phase prepares V7 for future destination/service routing without changing
live user traffic:

```text
user + destination -> route_class -> planned route behavior
```

No live service-aware `fwmark` routing was enabled in this phase.

## Added

Command:

```text
/usr/local/bin/v7-policy-apply
```

Default behavior:

```bash
v7-policy-apply
```

is a dry-run.

Apply-preview behavior:

```bash
v7-policy-apply --apply
```

does only safe actions:

- refreshes route-class DNS state through `v7-policy-resolve`;
- validates route class registry and active egress references;
- writes `/opt/v7/egress/state/policy-apply-preview.state`;
- refreshes `/opt/v7/egress/state/v7-state.json`;
- writes an audit event when `v7-audit-log` is available.

It does not add live nft mark rules and does not change user routing.

## JSON API

`/usr/local/bin/v7-state-json` now exposes:

```json
"policy_apply_preview": {
  "validation": "OK",
  "live_marks": "disabled",
  "user_routes_changed": "0"
}
```

## Important Safety Detail

The preview initially revealed a priority issue before it became live:

```text
fwmark priority 1071 would be after user rules 100/101
```

That would make service-aware destination overrides ineffective because the
per-user source rule would win first.

The plan was corrected so future service-aware class rules use priorities
before per-user rules, for example:

```text
TRUSTED_RU_SENSITIVE mark 0x78 -> table 71 -> priority 71
```

Current existing direct rule remains:

```text
fwmark 0x77 -> table 70 -> priority 50
```

## Current Preview

Important planned class:

```text
TRUSTED_RU_SENSITIVE
mode=egress
active_egress=vless
mark=0x78
table=71
domains=11
route_would_add=ip route replace default dev tun0 table 71
```

This still records `vless` as temporary. It is not the final trusted-RU
solution.

Generic `.ru` remains handled by the existing direct engine:

```text
DIRECT_RU
mode=direct
active_egress=ens3
mark=0x77
table=70
live_plan=handled_by_existing_direct_engine
```

## Validation

Commands run on VPS:

```bash
v7-policy-apply --apply
curl -sS http://127.0.0.1:7077/state | jq .policy_apply_preview
v7-killswitch-check
v7-system-check
```

Results:

- `policy_apply_preview.validation`: `OK`
- `policy_apply_preview.live_marks`: `disabled`
- `policy_apply_preview.user_routes_changed`: `0`
- `v7-killswitch-check`: `OK`
- `v7-system-check`: `OK`

Current users stayed unchanged:

```text
10.0.0.2 -> awg2 table 100
10.0.0.3 -> vless table 101
```

## Next Phase

Add admin/backend visibility for:

- route class status;
- policy apply preview;
- temporary sensitive-RU dependency warning;
- safe button/command to run `v7-policy-apply --apply`;
- no live marks until a class-by-class rollout is explicitly designed and
  tested.
