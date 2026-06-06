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

## Channel Actionable Alerts Update

Problem reported on live page:

- address: `https://v7-admin.195-2-79-116.sslip.io/admin-v2#channels`
- visible issue: channel status `Нужна проверка` was shown as a passive pill;
- expected behavior: clicking any warning/info field should open the exact problem and the immediate resolution path.

Committed and pushed:

- commit: `f86ef4018fd08e50e80033ebc343605ae05ce933`
- subject: `Make channel table alerts open solutions`
- branch: `Updatesystem`
- GitHub push: completed

Safe deploy applied:

- command: `python3 tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --restart-admin-if-changed --json`
- deploy id: `deploy-z8-14-Updatesystem-f86ef40-20260606T095414`
- production target: `/usr/local/bin/v7-admin-api`
- deployed hash: `217d4572b76f3b93ed102bd38ca1e677ddfddf01084c9556afc88f17fef3938a`
- `v7-admin-api.service`: active
- runtime linkage commit: `f86ef4018fd08e50e80033ebc343605ae05ce933`

Live verification:

- authenticated `/admin-v2` HTML title: `V7 Admin v2`
- `openChannelProblem`: present
- `channelProblemContext`: present
- old passive channel status render `if (colId === 'status') return pill(...)`: not found
- channel table services field now opens `openChannelProblem(id, 'services')`
- channel table speed field now opens `openChannelProblem(id, 'speed')`
- channel table load field now opens `openChannelProblem(id, 'load')`

Behavior changed:

1. Channel `Статус` is now clickable.
   - Example: `Нужна проверка` opens a `Решение: <канал>` drawer.
   - The drawer shows the current status, services, speed, load, and runtime readiness.

2. Channel `Сервисы` is now clickable from the table.
   - Degraded values like `0/14` or `13/14` open the same solution drawer.
   - The drawer gives direct actions: `Запустить сервисную матрицу` and `Показать сервисы`.

3. Channel `Скорость` is now clickable from the table.
   - Values like `0.0 Mbps`, `нет замера`, or `ошибка замера` open a speed resolution path.
   - The drawer gives direct actions: `Замерить скорость` and `Панель скорости`.

4. Channel `Нагрузка` is now clickable from the table.
   - Limit/capacity warnings open a resolution path.
   - The drawer gives direct actions: `Показать пользователей` and `Сводка нагрузки`.

5. The new solution drawer is specific to the selected channel.
   - It does not send the operator to a generic window.
   - It lists concrete issues and concrete next buttons for that exact channel.

Verification for this update:

- `PYTHONPYCACHEPREFIX=/tmp/v7_pycache_channel_problem python3 -m py_compile admin/v7-admin-api`
- `python3 -m unittest tests.contracts.endpoint_inventory_test`
- rendered inline JS from `html_page_v2()` and ran `node --check /tmp/v7_admin_inline_channel_problem_check.js`
- `git diff --check`
- production service check: `v7-admin-api.service` active
- production file hash matches deployed hash above

Safety for this update:

| Item | Value |
|---|---|
| runtime_mutation_performed | false |
| routing_changed | false |
| users_moved | false |
| autoswitch_apply_run | false |
| deploy_performed | true |
| systemd_changed | false |

## Channel Speed Inline Recheck Update

Problem reported on live page:

- address: `https://v7-admin.195-2-79-116.sslip.io/admin-v2#channels`
- visible issue: clicking a channel speed cell opened the solution drawer;
- expected behavior: clicking the speed cell should immediately start a background speed recheck, show `замер...` / `замеряется` in the same cell, then show the new result or error without opening any drawer.

Committed and pushed:

- commit: `7d76a534cbcb21ad95466a7b4f033bde5ca2dd48`
- subject: `Run channel speed checks inline`
- branch: `Updatesystem`
- GitHub push: completed

Safe deploy applied:

- command: `python3 tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --restart-admin-if-changed --json`
- deploy id: `deploy-z8-14-Updatesystem-7d76a53-20260606T100222`
- production target: `/usr/local/bin/v7-admin-api`
- deployed hash: `c5dcff501a934ee99c3112921381d761af5b1b6bfa6e314bd6b8e45c33265caf`
- `v7-admin-api.service`: active
- runtime linkage commit: `7d76a534cbcb21ad95466a7b4f033bde5ca2dd48`

Live verification:

- authenticated `/admin-v2` HTML title: `V7 Admin v2`
- channel table speed cell uses `runV2EgressSpeed(id)` directly
- speed cell title: `Перепроверить скорость в фоне`
- running text in cell: `замер...`
- inline state text in cell: `замеряется`
- no drawer is opened by the speed table cell click

Verification for this update:

- `PYTHONPYCACHEPREFIX=/tmp/v7_pycache_channel_speed_inline python3 -m py_compile admin/v7-admin-api`
- `python3 -m unittest tests.contracts.endpoint_inventory_test`
- rendered inline JS from `html_page_v2()` and ran `node --check /tmp/v7_admin_inline_channel_speed_check.js`
- `git diff --check`
- production service check: `v7-admin-api.service` active
- production file hash matches deployed hash above

Safety for this update:

| Item | Value |
|---|---|
| runtime_mutation_performed | false |
| routing_changed | false |
| users_moved | false |
| autoswitch_apply_run | false |
| deploy_performed | true |
| systemd_changed | false |

## Channel Services Inline Expansion Update

Problem reported on live page:

- address: `https://v7-admin.195-2-79-116.sslip.io/admin-v2#channels`
- expected behavior: clicking a service summary cell such as `7/9`, `13/14`, or `0/14` should expand a service table directly under that channel row;
- second click on the same service cell should collapse the service table;
- behavior should match the existing channel users expansion pattern on the same page.

Committed and pushed:

- commit: `f94e769563a691e99d41c544828cdbd871cb50d5`
- subject: `Expand channel services inline`
- branch: `Updatesystem`
- GitHub push: completed

Safe deploy applied:

- command: `python3 tools/v7-safe-deploy --apply --confirm DEPLOY_V7_APPROVED --update-local-snapshot --restart-admin-if-changed --json`
- deploy id: `deploy-z8-14-Updatesystem-f94e769-20260606T100954`
- production admin target: `/usr/local/bin/v7-admin-api`
- deployed admin hash: `2fb26228153285047520d681e18b2f692ed53d717df67f680e475cc2b6209405`
- production autoswitch target: `/usr/local/bin/v7-users-autoswitch`
- deployed autoswitch hash: `f75c14c8d2e5a8e05293a6af63d44762bd7cd4d1b78ddc60f77b8f7ac03d2762`
- `v7-admin-api.service`: active
- runtime linkage commit: `f94e769563a691e99d41c544828cdbd871cb50d5`

Live verification:

- authenticated `/admin-v2` HTML title: `V7 Admin v2`
- `expandedChannelServices`: present
- `toggleChannelServices`: present
- `channelServicesExpansionRow`: present
- `channel-services-row`: present
- service cell title toggles between `Показать сервисы канала` and `Скрыть сервисы канала`
- old service-cell drawer call `openChannelProblem(id, 'services')`: not present for the table service cell

Behavior changed:

1. Clicking a channel services summary now expands a row under that channel.
2. The expanded row shows a table:
   - service name;
   - status;
   - latency;
   - diagnostic detail;
   - per-service `Проверить` action.
3. Clicking the same summary again hides the service table.
4. Opening services collapses the channel users expansion, and opening users collapses services, so the channel table stays readable.
5. A `Проверить все сервисы` action remains available inside the expanded service row.

Verification for this update:

- `PYTHONPYCACHEPREFIX=/tmp/v7_pycache_channel_services_expand python3 -m py_compile admin/v7-admin-api`
- `python3 -m unittest tests.contracts.endpoint_inventory_test`
- rendered inline JS from `html_page_v2()` and ran `node --check /tmp/v7_admin_inline_channel_services_expand_check.js`
- `git diff --check`
- production service check: `v7-admin-api.service` active
- production file hash matches deployed hash above

Safety for this update:

| Item | Value |
|---|---|
| runtime_mutation_performed | false |
| routing_changed | false |
| users_moved | false |
| autoswitch_apply_run | false |
| deploy_performed | true |
| systemd_changed | false |

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
