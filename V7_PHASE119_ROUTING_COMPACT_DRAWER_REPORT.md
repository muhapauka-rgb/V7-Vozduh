# V7 Phase 119 — Compact Routing Overview + Drawer Shortcuts

Date: 2026-05-10

## Goal

Make the `Маршруты` workspace easier to understand without hiding important controls.

## Implemented

- Compact route class table:
  - Тип трафика
  - Решение
  - Текущий путь
  - Домены / действие
  - Действие
- Added plain-language route decisions:
  - DIRECT_RU: RU sites bypass V7 on the client in RU_LOCAL.
  - TRUSTED_RU_SENSITIVE: Gosuslugi/banks bypass V7 on the client for Russian users.
  - GLOBAL/VIDEO classes: use healthy/service-tested egresses.
- Added route next-action hints in the overview row.
- Added route drawer shortcuts:
  - Domain groups
  - Run preview
  - Client modes
  - Route reality
  - Route logs

## Safety Notes

- UI only.
- Drawer shortcuts navigate to focused workspaces.
- Preview/check actions remain read-only until guarded apply is explicitly confirmed.
- No routing changes.
- No user movement.
- No nftables or kill switch changes.

## Validation

```bash
PYTHONPYCACHEPREFIX=/private/tmp/v7-pyc python3 -m py_compile admin/v7-admin-api
awk 'BEGIN{n=0} /<script>/{n++; flag=(n==1); next} /<\/script>/{if(flag){exit}; flag=0} flag' admin/v7-admin-api > /private/tmp/v7-admin-v2-phase119.js
node --check /private/tmp/v7-admin-v2-phase119.js
git diff --check
tests/run-local-checks.sh
```

Result:

```text
V7_LOCAL_CHECKS=OK
```

## Manual UI Check

1. Open Admin V2.
2. Go to `Маршруты`.
3. Confirm route class overview is compact.
4. Click a route class row.
5. Confirm drawer shortcuts open the expected workspaces without applying changes.

