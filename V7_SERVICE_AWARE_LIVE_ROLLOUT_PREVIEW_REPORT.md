# V7 Service-Aware Live Rollout Preview

## Purpose

This step adds a read-only preview for the future live service-aware routing rollout.

It shows what V7 would need to create for domain/service based routing:

- nftables destination sets;
- nftables mark rules;
- `ip rule fwmark` rules;
- routing table defaults;
- kill switch allow/deny impact.

It does not apply any live network changes.

## What Was Added

- Backend endpoint:
  - `POST /api/actions/service-aware-live-rollout-preview`

- Admin UI button:
  - `Routes -> Live Rollout Preview`

## Read-Only Safety

The preview returns explicit safety flags:

- `routing_changed=false`
- `users_moved=false`
- `kill_switch_changed=false`
- `registry_changed=false`
- `systemd_changed=false`
- `nftables_changed=false`

## Validation Rules

The preview blocks rollout if:

- `TRUSTED_RU_SENSITIVE` still uses a temporary route;
- `TRUSTED_RU_SENSITIVE` points to an egress that is not role `TRUSTED_RU_SENSITIVE`;
- an active egress is missing or disabled;
- an egress route has no interface;
- a route class has no mark/table;
- the apply preview already has blockers.

This protects Gosuslugi, ESIA, banks, and other sensitive RU services from accidental routing through an ordinary global VPN path.

## Expected Current VPS Result

Current VPS should return:

```json
{
  "validation": "BLOCKED",
  "mode": "live_rollout_preview_read_only"
}
```

That is expected until we add a dedicated trusted RU route.

## Manual Verification

Syntax and diff:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/v7_pycache python3 -W error -m py_compile admin/v7-admin-api
git diff --check
```

Server function check:

```bash
python3 -c 'import runpy, json; m=runpy.run_path("/usr/local/bin/v7-admin-api", run_name="v7_admin_test"); res=m["service_aware_live_rollout_preview"]("10.0.0.3"); print(json.dumps({"mode":res["mode"],"validation":res["validation"],"safety":res["safety"],"blockers":res["blockers"],"nft_sets":len(res["nft"]["sets"]),"ip_rules":len(res["ip_rules"]),"routes":len(res["route_tables"])}, indent=2))'
```

Admin UI:

1. Open `http://127.0.0.1:7080/login`.
2. Go to Routes.
3. Click `Live Rollout Preview`.
4. Confirm it shows nftables sets, ip rules, route tables, and kill switch preview.
5. Confirm it remains read-only.

## Next Step

Next phase is the actual live rollout design:

- decide exact nftables table/chain names;
- decide rule priorities;
- decide rollback strategy for marks and rules;
- add SSH lockout guard;
- add apply only after all preview blockers are solved.
