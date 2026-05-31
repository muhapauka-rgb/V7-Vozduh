# Wave 1 UX Review

Verification date: 2026-05-30

Reference: `V7_ADMIN_DESIGN_INTERFACE_NAVIGATION_BRIEF`

## Native Fit

The Evidence drawer mostly fits the V7 Admin philosophy:

- It uses the existing drawer pattern.
- It avoids a new top-level navigation section.
- It keeps Evidence read-only and separated from runtime action.
- It uses progressive disclosure: chip -> object evidence list -> bundle detail.
- It keeps the operator inside the existing admin workflow.

## Visual Hierarchy

PASS:

- Summary appears before raw evidence items.
- Timeline is visually grouped.
- Evidence items are tabular and scannable.
- Safety boundary is visible at the bottom of the drawer.

PARTIAL:

- Several labels remain English-first: `Evidence`, `Timeline`, `Evidence items`.
- In a Russian admin surface, `Evidence` reads as bolted-on rather than native. Recommended copy is `Доказательства` or compact `Доказ.` for chips.

## Noise Level

PASS:

- Evidence does not dominate the page.
- The drawer contains the detail instead of flooding tables.

PARTIAL:

- Check rows show Evidence chips even for checks where the object may return no bundle. This creates a risk of low-value clicks.

## Responsive Behavior

PARTIAL/FAIL:

- In the current admin viewport, Evidence chips in `Пользователи` and `Каналы` exist in DOM but live inside a `.right` table cell that is `display:none`.
- This means operator-visible value is weaker outside the Checks workflow.

## Progressive Disclosure

PASS:

- `Проверки -> Evidence chip -> object drawer -> bundle drawer` is a clean progressive flow.

PARTIAL:

- The same flow is not available from every claimed section.

## UX Verdict

`ux_consistent_with_v7=false`

The core drawer interaction is V7-compatible, but the admin integration is not fully native yet because:

- visible entry points are missing from `Маршруты` and `Логи`
- chips are hidden in user/channel tables at the current width
- English copy makes the feature feel partially bolted on

These are product UX integration issues, not backend blockers.
