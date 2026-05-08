# V7 Service-Aware Guarded Apply

## Purpose

This step adds the first guarded apply action for service-aware routing.

It only updates:

- `/opt/v7/policy/route-classes.registry`

It does not update live nftables marks, ip rules, routing tables, kill switch, users, services, or systemd units.

## What Was Added

- Backend endpoint:
  - `POST /api/actions/service-aware-apply-guarded`

- Admin UI button:
  - `Routes -> Guarded Apply`

- Confirmation phrase:
  - `APPLY_SERVICE_AWARE_ROUTES`

## Safety Behavior

Before writing anything, V7 builds a fresh service-aware apply preview.

The apply is blocked if:

- confirmation is missing;
- the preview has blockers;
- `TRUSTED_RU_SENSITIVE` has no dedicated enabled trusted route;
- registry rows disappear between preview and apply.

When apply succeeds, V7:

1. creates a timestamped backup of `route-classes.registry`;
2. replaces only the registry lines shown in the preview;
3. writes atomically through a temp file and rename;
4. records the action in audit log.

## What It Still Does Not Do

This is not live routing rollout yet.

It intentionally does not:

- create nftables mark rules;
- add `ip rule fwmark` rules;
- change table 66/67/71 routes;
- move users;
- update kill switch allowlists;
- restart V7 services.

## Manual Verification

Syntax and diff:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/v7_pycache python3 -W error -m py_compile admin/v7-admin-api
git diff --check
```

Server function check:

```bash
python3 -c 'import runpy, json; m=runpy.run_path("/usr/local/bin/v7-admin-api", run_name="v7_admin_test"); res=m["service_aware_apply_guarded"]("10.0.0.3", "APPLY_SERVICE_AWARE_ROUTES"); print(json.dumps({"status":res["status"],"safety":res["safety"],"backup":res.get("backup",""),"changed_classes":res.get("changed_classes",[]),"blocked":res.get("blocked",res.get("preview",{}).get("blocked",[]))}, indent=2))'
```

On the current VPS this should remain blocked until a dedicated `TRUSTED_RU_SENSITIVE` route exists.

## Admin UI Verification

1. Open `http://127.0.0.1:7080/login`.
2. Go to Routes.
3. Click `Service-Aware Dry Run`.
4. Click `Apply Preview`.
5. Click `Guarded Apply`.
6. Enter `APPLY_SERVICE_AWARE_ROUTES`.
7. Confirm that blocked Sensitive RU prevents writing when no dedicated route exists.

## Next Step

Next phase is live rollout preview:

- preview nftables sets and marks;
- preview `ip rule fwmark` additions;
- preview table routes;
- preview kill switch impact;
- still do not apply until all checks are green.
