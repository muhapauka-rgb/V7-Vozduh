# V7 Admin Public and Mobile QA Report

Date: 2026-05-12

## Scope

Checked the public V7 Admin URL, authorization gate, all main Admin V2 tabs, key non-destructive buttons, and mobile layout for users/channels.

Public URL:

`https://v7-admin.195-2-79-116.sslip.io/admin-v2`

## Fixes Applied

- Added hash navigation handling so direct links like `/admin-v2#users` and browser refresh keep the selected tab.
- Added compact mobile tables for users and channels.
- On mobile, users and channels no longer require horizontal scrolling.
- User/channel rows stay single-line on phone width.
- Fixed load-error fallback targets so failures render in the actual visible blocks.

## Automated Checks

Viewport pass:

- 1720px desktop
- 1440px desktop
- 1200px laptop
- 900px tablet
- 720px tablet
- 390px phone

Checked tabs:

- Overview
- Users
- Channels
- Routing
- Checks
- Security
- Settings
- Logs

## Results

- Public `/admin-v2` without session redirects to `/login`.
- Public `/login` returns HTTP 200.
- `v7-admin-api` service is active.
- Caddy service is active.
- Admin health endpoint returns OK.
- No browser console errors.
- No page JavaScript errors.
- No failed browser requests during the QA run.
- No `[object Object]` text in the tested visible pages.
- Users table on 390px: no horizontal table overflow.
- Channels table on 390px: no horizontal table overflow.
- Overview users/channels tables on 390px: no horizontal table overflow.

## Button Checks

Passed:

- Top alerts open a central problem/action view.
- User row opens user details.
- Add user opens profile issue workspace.
- Channel row opens channel details.
- Add channel opens channel onboarding.
- Route row opens route details.

## Notes

For safety, the automated UI pass used a temporary server-side session token instead of submitting the admin password in the public login form. The public login gate itself was verified.

Some secondary technical tables, such as Logs and Security details, still use internal horizontal scrolling on mobile. The main requested mobile surfaces, Users and Channels, are compact and fit phone width.
