# V7 Phase 115 — Post-Enable Safe Next Actions

Date: 2026-05-10

## Goal

After a draft egress is enabled through the guarded flow, the admin UI should show the operator what to do next without moving users automatically or changing routing hiddenly.

## Implemented

- Added a read-only admin action:
  - `/api/actions/users-rebalance-dry-run`
- Added a post-enable next-action panel in the egress draft result drawer:
  - Run service matrix for the enabled egress.
  - Open a controlled manual switch panel for one selected user.
  - Run rebalance dry-run preview.
- The manual switch panel is explicit:
  - operator selects one enabled user;
  - action requires confirmation;
  - it calls the existing guarded `/api/actions/user-switch`;
  - it does not rebalance other users.
- Rebalance dry-run is read-only:
  - runs `v7-users-rebalance-dry-run`;
  - reports `users_moved=0`;
  - writes audit entry without changing routing.

## Safety Boundaries

- No automatic user movement after channel enable.
- No automatic route table changes from the new panel.
- No kill switch changes.
- No service restarts.
- No secret exposure.

## Validation

```bash
PYTHONPYCACHEPREFIX=/private/tmp/v7-pyc python3 -m py_compile admin/v7-admin-api
awk 'BEGIN{n=0} /<script>/{n++; flag=(n==1); next} /<\/script>/{if(flag){exit}; flag=0} flag' admin/v7-admin-api > /private/tmp/v7-admin-v2-phase115.js
node --check /private/tmp/v7-admin-v2-phase115.js
git diff --check
tests/run-local-checks.sh
```

Result:

```text
V7_LOCAL_CHECKS=OK
```

## Manual UI Check

1. Open Admin V2.
2. Go to Egress / draft lifecycle.
3. Enable a ready draft through guarded enable.
4. Confirm Post-Enable Validation shows:
   - Run service matrix
   - Manual switch one user
   - Rebalance dry-run
5. Click Rebalance dry-run and verify it says read-only and `users_moved=0`.
6. Click Manual switch one user and verify it opens a selector instead of applying immediately.

