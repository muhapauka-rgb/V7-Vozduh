# V7 Phase 121 — Security Guide + Control Map

Date: 2026-05-11

## Goal

Make the `Безопасность` workspace easier to understand:

- keep dangerous actions separated;
- show clear safety controls;
- explain which action is safe, preview-only, or requires typed confirmation.

## Implemented

- Added `Карта защиты` button to the Security hero.
- Added `v2SecurityControls()` as a single source for the security posture table and drawer guide.
- Expanded the security posture table:
  - Control
  - State
  - Operator meaning
  - Next step
  - Action
- Added drawer guide with:
  - Safe mode
  - Kill switch
  - SSH lockout guard
  - Backups
  - Rollback
  - Logs and disk
  - Secrets
- Added direct navigation/action shortcuts to focused zones:
  - backups
  - maintenance
  - rollback preview
  - kill switch check
  - security audit logs

## Safety Notes

- UI only.
- No backup, rollback, cleanup, safe mode, kill switch, or routing mutation is run automatically.
- Existing dangerous actions still require preview and/or typed confirmation.
- Cleanup remains bounded and must not touch configs/secrets/state.

## Validation

```bash
PYTHONPYCACHEPREFIX=/private/tmp/v7-pyc python3 -m py_compile admin/v7-admin-api
awk 'BEGIN{n=0} /<script>/{n++; flag=(n==1); next} /<\/script>/{if(flag){exit}; flag=0} flag' admin/v7-admin-api > /private/tmp/v7-admin-v2-phase121.js
node --check /private/tmp/v7-admin-v2-phase121.js
git diff --check
tests/run-local-checks.sh
```

Result:

```text
V7_LOCAL_CHECKS=OK
```

## Manual UI Check

1. Open Admin V2.
2. Go to `Безопасность`.
3. Click `Карта защиты`.
4. Confirm the drawer explains every security control.
5. Confirm shortcut buttons navigate to focused zones and do not apply changes by themselves.

