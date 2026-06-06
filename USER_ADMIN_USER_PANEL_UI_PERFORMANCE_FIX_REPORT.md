# User Admin Panel UI And Performance Fix Report

Scope: `/admin-v2#users` and `/admin-v2#channels`, user/channel tables and object drawers for proposals, evidence, and execution contracts.

Main file changed:

- `admin/v7-admin-api`

## Live Address Clarification

The screenshots were taken from the live admin addresses:

- `https://v7-admin.195-2-79-116.sslip.io/admin-v2#users`
- `https://v7-admin.195-2-79-116.sslip.io/admin-v2#channels`

The UI change was made in the local repository file `admin/v7-admin-api`. Production serves the copied runtime binary at `/usr/local/bin/v7-admin-api`, so the live pages will continue to show the old chips until the approved deploy path copies this file to production and restarts only `v7-admin-api.service`.

Safe deploy dry-run found the expected runtime delta:

- local source: `admin/v7-admin-api`
- production target: `/usr/local/bin/v7-admin-api`
- only this approved admin binary differs from production among the checked deploy files

Safe deploy did not apply because the repository gate requires the runtime-critical change to be committed and verified through GitHub first.

Current deploy blockers:

- main workspace has unrelated runtime-critical changes in `tools/v7-users-autoswitch`;
- related unit test changes exist in `tests/unit/test_v7_users_autoswitch_policy.py`;
- those changes are outside this UI/performance fix and must not be silently reverted or deployed together with the Users page change;
- GitHub remote branch `Updatesystem` was verified with network access and currently points to `ca75d12d4ebfa858f4cec8a372454496718568a6`.

Safe next delivery path:

1. preserve the unrelated autoswitch/test changes;
2. commit and push only the Users page UI/performance fix;
3. run `tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --restart-admin-if-changed --json`;
4. verify the live `/admin-v2#users` page after the `v7-admin-api.service` restart.

## What Changed

1. Removed the three inline chips from every user row in the Users table:
   - `Предложения`
   - `Доказательства`
   - `Execution`

2. Removed the same three inline chips from every channel row in the Channels table.

3. Added compact lazy-loaded sections inside the user and channel drawers:
   - title: `Материалы и контракты`
   - buttons: `Предложения`, `Доказательства`, `Execution`
   - each button refreshes its own content inside the same compact section for the selected object.

4. Moved these sections below the main object actions area instead of showing large empty blocks near the top of the drawer.

5. Applied the same compact section to the detailed/live user drawer opened through user checking and to the live channel drawer opened from the Channels page.

6. Made execution object drawer requests parallel instead of sequential.

## Performance Finding

The slow behavior came from object-specific user clicks using broad read models:

- `/api/proposals/by-object/user/<ip>` called the full proposal model.
- The full proposal model could rebuild generated proposals for all users.
- Generated proposals could trigger service recommendations and route status calculations across many users.
- Execution draft previews were derived from the full proposal model.

That made a single user click feel like a system-wide recalculation.

## Performance Fix

Added safe read-only fast paths:

- evidence by user now builds evidence only for the selected IP;
- proposals by user now builds proposals only for the selected IP;
- execution draft previews with `user=<ip>` now use the selected user's proposals;
- shared read-only lists have a short in-memory TTL cache.

No runtime apply, routing change, user movement, systemd change, or execution engine behavior was added.

## Verification

Passed:

- `PYTHONPYCACHEPREFIX=/tmp/v7_pycache_user_panels python3 -m py_compile admin/v7-admin-api`
- `python3 -m unittest tests.contracts.endpoint_inventory_test`
- `git diff --check`
- extracted inline JS and ran `node --check /tmp/v7_admin_inline_check.js`
- generated endpoint inventory to `/tmp/v7-user-panels-endpoint-inventory.json`

Local fast-path timing check showed user-specific handlers using the new fast path.

## Safety

| Item | Value |
|---|---|
| runtime_mutation_performed | false |
| routing_changed | false |
| users_moved | false |
| systemd_changed | false |
| deploy_performed | false |
| execution_engine_changed | false |
