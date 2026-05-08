# V7 Trusted RU Readiness

## Purpose

This step adds a production readiness checklist for `TRUSTED_RU_SENSITIVE`.

This is the route class for Gosuslugi, ESIA, nalog.gov.ru, and banks. It must not be enabled for live policy routing until V7 has a dedicated trusted path.

## What Was Added

- Backend state builder:
  - `trusted_ru_readiness_state()`

- Backend endpoint:
  - `POST /api/actions/trusted-ru-readiness`

- Admin UI:
  - Sensitive RU panel now shows `Production Readiness`;
  - readiness checks are visible next to existing diagnostics;
  - button `Readiness` refreshes the checklist.

## Readiness Checks

The checklist verifies:

- `TRUSTED_RU_SENSITIVE` route class exists;
- route class is enabled;
- route is not marked `temporary=1`;
- dedicated active egress is selected;
- active egress exists in the V7 pool;
- active egress is enabled;
- active egress role is `TRUSTED_RU_SENSITIVE`;
- active egress has an interface;
- required sensitive services passed service-matrix checks.

It also shows warnings when:

- temporary VLESS works only as a diagnostic path;
- direct VPS path is blocked by sensitive RU domains;
- service matrix has missing samples.

## Expected Current VPS Result

Current VPS should show `BLOCKED`, because `TRUSTED_RU_SENSITIVE` is still temporary and points to ordinary `vless`.

This is correct. It prevents accidental production use of a temporary channel for Gosuslugi/banks.

## Manual Verification

Syntax:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/v7_pycache python3 -W error -m py_compile admin/v7-admin-api
git diff --check
```

Server function check:

```bash
python3 -c 'import runpy, json; m=runpy.run_path("/usr/local/bin/v7-admin-api", run_name="v7_admin_test"); res=m["trusted_ru_readiness_state"](); print(json.dumps({"validation":res["validation"],"active_egress":res["active_egress"],"blockers":len(res["blockers"]),"warnings":len(res["warnings"]),"next_step":res["next_step"]}, indent=2))'
```

Admin UI:

1. Open `http://127.0.0.1:7080/login`.
2. Go to Sensitive RU.
3. Check `Production Readiness`.
4. Click `Readiness`.
5. Confirm the status is understandable and blocked until a dedicated trusted route exists.

## Next Step

Next phase is to prepare a dedicated trusted route onboarding path:

- candidate can be tested safely;
- candidate gets role `TRUSTED_RU_SENSITIVE`;
- service matrix must pass Gosuslugi/ESIA/banks;
- only then service-aware live rollout can move forward.
