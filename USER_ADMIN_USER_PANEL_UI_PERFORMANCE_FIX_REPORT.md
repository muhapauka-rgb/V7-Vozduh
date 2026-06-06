# User Admin Panel UI And Performance Fix Report

Scope: `/admin-v2#users` and `/admin-v2#channels`, user/channel tables and object drawers for proposals, evidence, and execution contracts.

Main file changed:

- `admin/v7-admin-api`

## Live Address Clarification

The screenshots were taken from the live admin addresses:

- `https://v7-admin.195-2-79-116.sslip.io/admin-v2#users`
- `https://v7-admin.195-2-79-116.sslip.io/admin-v2#channels`

The UI change was made in the repository file `admin/v7-admin-api`. Production serves the copied runtime binary at `/usr/local/bin/v7-admin-api`, so the live pages change only after the approved deploy path copies this file to production and restarts `v7-admin-api.service`.

## Deployment Result

Committed and pushed:

- commit: `2626b46f7f6d38c93f7c9b47f2a19228a2163d4f`
- subject: `Fix admin object panels in user and channel tables`
- branch: `Updatesystem`
- GitHub push: completed

Safe deploy applied:

- command: `python3 tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --restart-admin-if-changed --json`
- deploy id: `deploy-z8-14-Updatesystem-2626b46-20260606T093843`
- production target: `/usr/local/bin/v7-admin-api`
- deployed hash: `8f200c811637f762441bca0e1ff2e7648f247bf9e416ad7264a1ff2e6a76ebcd`
- `v7-admin-api.service`: restarted and active
- runtime linkage commit: `2626b46f7f6d38c93f7c9b47f2a19228a2163d4f`

Live verification:

- authenticated `/admin-v2` HTML title: `V7 Admin v2`
- old inline table chip calls for `user` and `channel`: not found
- `userObjectPanelsSection`: present
- `channelObjectPanelsSection`: present
- `loadChannelObjectPanel`: present

Local preservation:

- unrelated autoswitch/test/evidence work was preserved before deploy and restored afterward;
- an unrelated device-label admin change exists in later GitHub history and was not part of this production deploy.

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
- rendered inline JS from `html_page_v2()` and ran `node --check /tmp/v7_admin_inline_rendered_check.js`
- generated endpoint inventory to `/tmp/v7-user-channel-panels-endpoint-inventory.json`

Local fast-path timing check showed user-specific handlers using the new fast path.

## Safety

| Item | Value |
|---|---|
| runtime_mutation_performed | false |
| routing_changed | false |
| users_moved | false |
| systemd_changed | false |
| deploy_performed | true |
| execution_engine_changed | false |
