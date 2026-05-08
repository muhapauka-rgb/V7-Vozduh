# V7 Service-Aware Apply Preview

## Purpose

This step adds a read-only apply preview for service-aware routing.

The preview answers a simple question before any real change:

> If V7 applies the current service-aware route decision, what would change in `/opt/v7/policy/route-classes.registry`?

It does not change routing, users, nftables, ip rules, kill switch, services, or files.

## What Was Added

- Backend endpoint:
  - `POST /api/actions/service-aware-apply-preview`

- Admin UI button:
  - `Routes -> Apply Preview`

- Backend helper functions:
  - read current route-class registry rows;
  - compare current registry lines with proposed service-aware decisions;
  - return a diff-style preview;
  - keep safety flags explicit and false.

## Safety Rules

The apply preview is read-only:

- `routing_changed=false`
- `users_moved=false`
- `kill_switch_changed=false`
- `registry_changed=false`
- `systemd_changed=false`

If `TRUSTED_RU_SENSITIVE` has no dedicated enabled trusted route, the preview is blocked.
V7 must not silently route Gosuslugi, ESIA, banks, or other sensitive RU traffic through a temporary global VLESS path.

## Expected Results

When a dedicated trusted RU route is missing:

```json
{
  "validation": "BLOCKED",
  "next_step": "fix_blockers"
}
```

When a valid dedicated trusted RU route exists:

```json
{
  "validation": "OK",
  "next_step": "guarded_apply_after_backup"
}
```

Warnings may appear if optional route classes are not present in the registry yet.

## Manual Verification

Local syntax check:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/v7_pycache python3 -W error -m py_compile admin/v7-admin-api
git diff --check
```

Server function check:

```bash
python3 -c 'import runpy, json; m=runpy.run_path("/usr/local/bin/v7-admin-api", run_name="v7_admin_test"); res=m["service_aware_apply_preview"]("10.0.0.3"); print(json.dumps({"mode":res["mode"],"validation":res["validation"],"safety":res["safety"],"blocked":res["blocked"],"changes":len(res["changes"]),"next_step":res["next_step"]}, indent=2))'
```

Admin UI:

1. Open `http://127.0.0.1:7080/login`.
2. Go to Routes.
3. Click `Service-Aware Dry Run`.
4. Click `Apply Preview`.
5. Confirm that the result shows registry diff preview and safety says read-only.

## Next Step

Next phase is guarded apply:

- create backup first;
- write only `/opt/v7/policy/route-classes.registry`;
- keep routing/ip rules/nftables unchanged;
- audit the action;
- provide rollback for the last registry update.
