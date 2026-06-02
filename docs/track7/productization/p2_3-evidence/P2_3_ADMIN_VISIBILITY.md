# P2.3 Admin Visibility

## Result

admin_visibility_implemented=true

## Visible surfaces

Главная:
Execution trust card now uses `/api/execution/readiness` so the operator sees readiness, not only stored contract count.

Проверки:
Execution trust surface appears alongside Runtime Trust and Release Trust.

Execution drawer:
Adds `Execution readiness`, `Gate health`, draft contracts, validation preview, stored contracts, timeline, and consistency.

Gate drawer:
Clicking a gate opens adapter-level detail with draft status, reason, and source.

## UX rule

No new top-level navigation was added. The integration remains within the existing V7 Admin pattern and drawer-first workflow.

## Operator value

The operator can now answer:

- Which execution gates exist?
- Which gates are connected to real read-only sources?
- Which gates failed closed?
- Which gates need review?
- Why is readiness not READY?
