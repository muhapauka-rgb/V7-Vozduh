# Wave 1 Admin Verification

Verification date: 2026-05-30

Admin target: `/admin-v2`

Backend target: local verification backend on `127.0.0.1:18083`

## Sections Checked

| Admin section | Evidence visible | Drawer opens | Notes |
| --- | --- | --- | --- |
| `Главная` | PARTIAL | Not fully verified from overview | Evidence chips exist in DOM for users/channels, but in the current viewport they are hidden in responsive table columns. |
| `Пользователи` | PARTIAL | Not usable in current viewport | Evidence chips exist in DOM for both users, but the parent table cell has `display:none` in the current admin width. |
| `Каналы` | PARTIAL | Not fully usable in current viewport | Evidence chips exist in DOM, but the same responsive table behavior hides the action column in the current admin width. |
| `Маршруты` | FAIL | Not available | No visible Evidence chip or equivalent evidence entry point was observed in the Routes section. |
| `Проверки` | PASS | PASS | Evidence chips are present. Diagnostics chip opened the Evidence drawer. |
| `Логи` | FAIL | Not available | Log evidence exists in the API, but no visible Evidence chip or drawer entry point was observed in Logs. |

## Verified Working UI Path

The following path was verified in the admin:

1. Open `/admin-v2`.
2. Navigate to `Проверки`.
3. Open the `Evidence` chip for diagnostics.
4. Evidence drawer opens.
5. The object-level drawer lists the diagnostics bundle.
6. Opening the bundle shows:
   - summary
   - timeline
   - evidence items
   - linked objects
   - safety boundary text

## Drawer Verification

Evidence drawer status:

`evidence_drawer_working=true`

Observed drawer content:

- title: `Доказательства`
- bundle id: `evidence-check-state-freshness`
- summary section
- timeline section
- evidence items table
- linked objects table
- safety boundary text explaining that evidence is read-only and non-authoritative

## Timeline Verification

Evidence timeline rendered in the bundle drawer with records from audit tail:

- `Diagnostics`
- `Service matrix`

CSS class observed:

`evidence-timeline`

Timeline item class observed:

`evidence-timeline-item`

## Screenshots Captured

- `/private/tmp/v7-wave1-verification-evidence-drawer.png`
- `/private/tmp/v7-wave1-verification-admin-sections.png`
- `/private/tmp/v7-wave1-verification-current.png`

## Admin Verdict

`evidence_visible_in_admin=true`

Wave 1 visibly landed in the admin for `Проверки` and the drawer/timeline path works. However, the claimed integration into all listed workflows is not complete:

- `Маршруты` has no visible evidence entry point.
- `Логи` has no visible evidence entry point.
- `Пользователи` and `Каналы` have Evidence chips in DOM, but the chips are hidden by responsive table layout in the current admin viewport.
