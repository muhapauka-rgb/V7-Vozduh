# V7 Phase 120 — Checks Guide + Unified Check Cards

Date: 2026-05-10

## Goal

Make the `Проверки` workspace clearer for an operator:

- show a compact diagnostics map;
- explain what each check means;
- keep all checks safe/read-only unless a separate guarded apply exists elsewhere.

## Implemented

- Added `Карта проверок` button to the Checks hero.
- Added drawer guide with:
  - check name;
  - status;
  - what it verifies;
  - safe next step;
  - focused action button.
- Unified check definitions in one JS function:
  - `v2CheckDefinitions()`
- The overview cards and readiness table now use the same check source.
- Preserved existing focused result renderers:
  - diagnostics summary;
  - kill switch summary;
  - route/policy matrix;
  - service-aware preview;
  - trusted RU readiness;
  - installer preflight.

## Safety Notes

- UI only.
- Checks remain diagnostic/read-only.
- No routing changes.
- No user movement.
- No nftables or kill switch changes.
- No service restarts.

## Validation

```bash
PYTHONPYCACHEPREFIX=/private/tmp/v7-pyc python3 -m py_compile admin/v7-admin-api
awk 'BEGIN{n=0} /<script>/{n++; flag=(n==1); next} /<\/script>/{if(flag){exit}; flag=0} flag' admin/v7-admin-api > /private/tmp/v7-admin-v2-phase120.js
node --check /private/tmp/v7-admin-v2-phase120.js
git diff --check
tests/run-local-checks.sh
```

Result:

```text
V7_LOCAL_CHECKS=OK
```

## Manual UI Check

1. Open Admin V2.
2. Go to `Проверки`.
3. Click `Карта проверок`.
4. Confirm the drawer explains every check and action.
5. Run one focused check and confirm the result appears in the result workspace.

